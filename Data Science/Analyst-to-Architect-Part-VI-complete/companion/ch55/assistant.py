#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 55 · the support assistant, end to end.
Retrieve, ground, answer with a citation, or refuse. The "model" here is the same kind of local
stand-in as Chapter 54's: it can only return a sentence that appears in the retrieved text, which is
exactly the behaviour a grounded prompt asks a real model for. It cannot paraphrase, and it cannot
invent - the second of which is the point being taught. Section 55.6 says what a real model adds.
"""
from __future__ import annotations

import re

from retrieval import BM25, VectorIndex, build_chunks, chunk_sentences, hybrid_scores, load_documents, tokenize

STOP = {'what', 'is', 'the', 'of', 'a', 'an', 'for', 'to', 'do', 'does', 'can', 'i', 'you', 'are',
        'how', 'much', 'many', 'long', 'when', 'who', 'and', 'in', 'on', 'my', 'we', 'your', 'be'}


class SupportAssistant:
    def __init__(self, bm25_floor: float = 8.0, cosine_floor: float = 0.60, k: int = 3):
        documents = load_documents()
        self.pairs = build_chunks(documents, chunk_sentences)
        self.texts = [chunk for _, chunk in self.pairs]
        self.names = [name for name, _ in self.pairs]
        self.bm25 = BM25(self.texts)
        self.vectors = VectorIndex(self.texts)
        self.bm25_floor = bm25_floor          # absolute scores, not per-question normalized ones:
        self.cosine_floor = cosine_floor      # a normalized top score is always 1.0 and says nothing
        self.k = k

    def confidence(self, question: str) -> tuple[float, float]:
        """The two absolute signals that say whether this corpus can answer at all."""
        return float(self.bm25.scores(question).max()), float(self.vectors.scores(question).max())

    def retrieve(self, question: str):
        scores = hybrid_scores(self.bm25, self.vectors, question)
        order = scores.argsort()[::-1][:self.k]
        return [(self.names[i], self.texts[i], float(scores[i])) for i in order]

    def answer(self, question: str) -> dict:
        keyword_score, meaning_score = self.confidence(question)
        retrieved = self.retrieve(question)
        best_score = min(keyword_score / 20, meaning_score)
        if keyword_score < self.bm25_floor or meaning_score < self.cosine_floor:
            return {'answer': "I don't have that in Riverstone's documents. The customer support desk "
                              "(support@riverstone.example) can help.",
                    'grounded': False, 'source': None, 'score': best_score}
        words = [w for w in tokenize(question) if w not in STOP]
        best_sentence, best_overlap, best_source = None, 0, None
        for name, chunk, _ in retrieved:
            for sentence in re.split(r'(?<=[.!?])\s+|\n', chunk):
                sentence = sentence.strip(' -|')
                if len(sentence) < 15:
                    continue
                overlap = sum(1 for word in set(words) if word in sentence.lower())
                if overlap > best_overlap:
                    best_sentence, best_overlap, best_source = sentence, overlap, name
        if best_sentence is None:
            return {'answer': "I couldn't find that in the documents I have.", 'grounded': False,
                    'source': None, 'score': best_score}
        return {'answer': best_sentence, 'grounded': True, 'source': best_source, 'score': best_score}
