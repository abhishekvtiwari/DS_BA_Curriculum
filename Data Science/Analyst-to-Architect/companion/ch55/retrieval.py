#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 55 · the retrieval this chapter builds and measures.
Chunking, BM25, vector search and hybrid scoring, in one small module so the chapter can import it
instead of repeating forty lines in every section. Standard library plus numpy and scikit-learn.
"""
from __future__ import annotations

import math
import pathlib
import re
from collections import Counter

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

DOCS = pathlib.Path(__file__).parent / 'corpus' / 'docs'


def load_documents(folder: pathlib.Path = DOCS) -> dict[str, str]:
    return {path.stem: path.read_text(encoding='utf-8') for path in sorted(folder.glob('*.md'))}


def chunk_fixed(text: str, size: int = 400, overlap: int = 80) -> list[str]:
    """Cut every `size` characters, repeating `overlap` characters so a sentence is not split in half."""
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size].strip())
        start += size - overlap
    return [chunk for chunk in chunks if chunk]


def chunk_sentences(text: str, per_chunk: int = 4) -> list[str]:
    """Group whole sentences, so a chunk never ends mid-thought."""
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n(?=[-|#])', text) if s.strip()]
    return [' '.join(sentences[i:i + per_chunk]) for i in range(0, len(sentences), per_chunk)]


def chunk_sections(text: str) -> list[str]:
    """Split on markdown headings, so each chunk is one section with its title attached."""
    parts = re.split(r'\n(?=#{1,3}\s)', text)
    title = text.splitlines()[0].lstrip('# ').strip()
    return [part.strip() if part.strip().startswith('#') else f'{title}\n{part.strip()}'
            for part in parts if part.strip()]


def build_chunks(documents: dict[str, str], chunker) -> list[tuple[str, str]]:
    """Return (document name, chunk text) pairs, which is what every search below indexes."""
    return [(name, chunk) for name, text in documents.items() for chunk in chunker(text)]


def tokenize(text: str) -> list[str]:
    return re.findall(r'[a-z0-9]+', text.lower())


class BM25:
    """Keyword search, the algorithm behind most search boxes, in about twenty lines."""

    def __init__(self, chunks: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.documents = [tokenize(chunk) for chunk in chunks]
        self.lengths = np.array([len(d) for d in self.documents], dtype=float)
        self.average_length = self.lengths.mean()
        self.frequencies = [Counter(d) for d in self.documents]
        appearances = Counter(word for document in self.documents for word in set(document))
        n = len(self.documents)
        self.idf = {word: math.log(1 + (n - count + 0.5) / (count + 0.5))
                    for word, count in appearances.items()}

    def scores(self, query: str) -> np.ndarray:
        result = np.zeros(len(self.documents))
        for word in tokenize(query):
            if word not in self.idf:
                continue
            idf = self.idf[word]
            for i, frequency in enumerate(self.frequencies):
                count = frequency.get(word, 0)
                if count:
                    denominator = count + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.average_length)
                    result[i] += idf * count * (self.k1 + 1) / denominator
        return result


class VectorIndex:
    """Meaning-ish search: TF-IDF reduced with SVD, then cosine similarity (Chapter 54, section 54.8)."""

    def __init__(self, chunks: list[str], dimensions: int = 60):
        self.vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
        counts = self.vectorizer.fit_transform(chunks)
        self.svd = TruncatedSVD(n_components=min(dimensions, counts.shape[1] - 1), random_state=55)
        self.vectors = normalize(self.svd.fit_transform(counts))

    def scores(self, query: str) -> np.ndarray:
        vector = normalize(self.svd.transform(self.vectorizer.transform([query])))
        return self.vectors @ vector[0]


def rank(scores: np.ndarray, k: int = 5) -> list[int]:
    return list(np.argsort(-scores)[:k])


def normalized(scores: np.ndarray) -> np.ndarray:
    """Put scores on a 0-1 scale so two different searches can be added together."""
    lowest, highest = scores.min(), scores.max()
    return (scores - lowest) / (highest - lowest) if highest > lowest else np.zeros_like(scores)


def hybrid_scores(bm25: BM25, vectors: VectorIndex, query: str, weight: float = 0.5) -> np.ndarray:
    return weight * normalized(bm25.scores(query)) + (1 - weight) * normalized(vectors.scores(query))
