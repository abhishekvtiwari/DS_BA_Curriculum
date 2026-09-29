#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 55 · the retrieval this chapter builds and measures.
Every function here is the one the chapter writes, cell by cell, in sections 55.1 to 55.5, saved in one
small module so that assistant.py and the exercises can import it instead of repeating it.
checks/ch55_code_sync.py confirms that this file and the chapter's cells hold the same code.
Standard library plus NumPy and scikit-learn.
"""
import math
import pathlib
import re
from collections import Counter

import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

DOCS = pathlib.Path(__file__).parent / "corpus" / "docs"


def load_documents(folder=DOCS):
    """Read every .md file in the folder into a dictionary: file name -> text."""
    return {path.stem: path.read_text(encoding="utf-8")
            for path in sorted(pathlib.Path(folder).glob("*.md"))}


def chunk_fixed(text, size=400, overlap=80):
    """Cut every `size` characters; neighbours share `overlap` characters."""
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + size].strip())
        start += size - overlap
    return [chunk for chunk in chunks if chunk]


def chunk_sentences(text, per_chunk=4):
    """Group whole sentences, so a chunk never ends mid-thought."""
    pieces = re.split(r"(?<=[.!?])\s+|\n(?=[-|#])", text)
    sentences = [s.strip() for s in pieces if s.strip()]
    return [" ".join(sentences[i:i + per_chunk])
            for i in range(0, len(sentences), per_chunk)]


def chunk_sections(text):
    """Split on markdown headings, and put the document's title on every section."""
    parts = [p.strip() for p in re.split(r"\n(?=#{1,3}\s)", text) if p.strip()]
    title = text.splitlines()[0].lstrip("# ").strip()
    return [parts[0]] + [f"{title}\n{part}" for part in parts[1:]]


def chunk_sentences_titled(text, per_chunk=4):
    """Sentence chunks, each with the document's title in front."""
    title = text.splitlines()[0].lstrip("# ").strip()
    return [f"{title}\n{chunk}" for chunk in chunk_sentences(text, per_chunk)]


def build_chunks(documents, chunker):
    """Return (document name, chunk text) pairs for every chunk of every document."""
    return [(name, chunk) for name, text in documents.items()
            for chunk in chunker(text)]


def tokenize(text):
    """Lower-case the text and keep its runs of letters and digits."""
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25:
    """Keyword search: the algorithm behind most search boxes."""

    def __init__(self, chunks, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.documents = [tokenize(chunk) for chunk in chunks]
        self.lengths = np.array([len(d) for d in self.documents], dtype=float)
        self.average_length = self.lengths.mean()
        self.frequencies = [Counter(d) for d in self.documents]
        appearances = Counter(word for d in self.documents for word in set(d))
        n = len(self.documents)
        self.idf = {word: math.log(1 + (n - count + 0.5) / (count + 0.5))
                    for word, count in appearances.items()}

    def scores(self, query):
        result = np.zeros(len(self.documents))
        for word in tokenize(query):
            if word not in self.idf:
                continue
            idf = self.idf[word]
            for i, frequency in enumerate(self.frequencies):
                count = frequency.get(word, 0)
                if count:
                    length_ratio = self.lengths[i] / self.average_length
                    denominator = count + self.k1 * (1 - self.b + self.b * length_ratio)
                    result[i] += idf * count * (self.k1 + 1) / denominator
        return result


class VectorIndex:
    """Meaning search, stand-in version: TF-IDF, then SVD, compared by cosine."""

    def __init__(self, chunks, dimensions=60):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        counts = self.vectorizer.fit_transform(chunks)
        n_components = min(dimensions, counts.shape[1] - 1)
        self.svd = TruncatedSVD(n_components=n_components, random_state=55)
        self.vectors = normalize(self.svd.fit_transform(counts))

    def scores(self, query):
        query_counts = self.vectorizer.transform([query])
        query_vector = normalize(self.svd.transform(query_counts))
        return self.vectors @ query_vector[0]


def rank(scores, k=5):
    """Positions of the k highest scores, highest first."""
    return [int(i) for i in np.argsort(-scores)[:k]]


def normalized(scores):
    """Put scores on a 0-1 scale so two different searches can be added together."""
    lowest, highest = scores.min(), scores.max()
    if highest == lowest:
        return np.zeros_like(scores)
    return (scores - lowest) / (highest - lowest)


def hybrid_scores(bm25, vectors, query, weight=0.5):
    """Add the normalized scores: `weight` for keywords, the rest for meaning."""
    return (weight * normalized(bm25.scores(query))
            + (1 - weight) * normalized(vectors.scores(query)))
