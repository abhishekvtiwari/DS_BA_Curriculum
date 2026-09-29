#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 55 · the support assistant, end to end.
Retrieve, ground, answer with a citation, or refuse. The "model" here is a local stand-in, like
Chapter 54's: it can only return a sentence that appears in the retrieved text, which is the behaviour
a grounded prompt asks a real model for. It cannot paraphrase, and it cannot invent. Section 55.6
prints every method of this class; checks/ch55_code_sync.py keeps the chapter and this file in step.
"""
import re

from retrieval import (BM25, VectorIndex, build_chunks, chunk_sentences, hybrid_scores,
                       load_documents, tokenize)

STOP = {"what", "is", "the", "of", "a", "an", "for", "to", "do", "does", "can", "i", "you",
        "are", "how", "much", "many", "long", "when", "who", "and", "in", "on", "my", "we",
        "your", "be"}
REFUSAL = ("I don't have that in Riverstone's documents. "
           "The customer support desk (support@riverstone.example) can help.")


class SupportAssistant:
    def __init__(self, bm25_floor=8.0, cosine_floor=0.60, k=3):
        pairs = build_chunks(load_documents(), chunk_sentences)
        self.names = [name for name, _ in pairs]
        self.texts = [chunk for _, chunk in pairs]
        self.bm25 = BM25(self.texts)
        self.vectors = VectorIndex(self.texts)
        self.bm25_floor = bm25_floor        # absolute scores, not normalized ones
        self.cosine_floor = cosine_floor
        self.k = k                          # how many chunks to hand to the model

    def confidence(self, question):
        """The two absolute signals that say whether this corpus can answer at all."""
        keyword_top = self.bm25.scores(question).max()
        meaning_top = self.vectors.scores(question).max()
        return float(keyword_top), float(meaning_top)

    def retrieve(self, question):
        """The k best chunks by hybrid score, as (document name, chunk text) pairs."""
        scores = hybrid_scores(self.bm25, self.vectors, question)
        best = scores.argsort()[::-1][:self.k]
        return [(self.names[i], self.texts[i]) for i in best]

    def answer(self, question):
        """Refuse, or return the retrieved sentence that best matches the question."""
        keyword_top, meaning_top = self.confidence(question)
        score = min(keyword_top / 20, meaning_top)      # one number for monitoring
        if keyword_top < self.bm25_floor or meaning_top < self.cosine_floor:
            return {"answer": REFUSAL, "grounded": False, "source": None, "score": score}
        words = {w for w in tokenize(question) if w not in STOP}
        best_sentence, best_overlap, best_source = None, 0, None
        for name, chunk in self.retrieve(question):
            for sentence in re.split(r"(?<=[.!?])\s+|\n", chunk):
                sentence = sentence.strip(" -|")
                if len(sentence) < 15:
                    continue
                overlap = sum(1 for word in words if word in sentence.lower())
                if overlap > best_overlap:
                    best_sentence, best_overlap, best_source = sentence, overlap, name
        if best_sentence is None:
            return {"answer": REFUSAL, "grounded": False, "source": None, "score": score}
        return {"answer": best_sentence, "grounded": True, "source": best_source,
                "score": score}
