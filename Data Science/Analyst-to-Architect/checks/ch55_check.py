#!/usr/bin/env python3
"""ch55_check.py - checks Chapter 55's numbers against the corpus, the retrieval module and the assistant."""
import json, pathlib, sys
C = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1] / 'companion' / 'ch55')
sys.path.insert(0, str(C))
import os
os.chdir(C)
import re
from retrieval import (BM25, VectorIndex, build_chunks, chunk_fixed, chunk_sections, chunk_sentences,
                       chunk_sentences_titled, hybrid_scores, load_documents, rank)
from assistant import SupportAssistant
from tools import propose_tool_call, run_tool_call
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    assert (abs(got - want) <= tol) if isinstance(want, float) else got == want, f'{label}: {got} != {want}'
    ok += 1
documents = load_documents()
questions = json.load(open('corpus/questions.json', encoding='utf-8'))
answerable = [q for q in questions if q['doc']]
check('documents', len(documents), 28)
check('questions', len(questions), 65)
check('answerable', len(answerable), 55)
check('superseded policy is present', 'policy_delivery_rev3_superseded' in documents, True)
def evaluate(chunker, method, k=5):
    pairs = build_chunks(documents, chunker)
    texts = [c for _, c in pairs]; names = [n for n, _ in pairs]
    bm25, vectors = BM25(texts), VectorIndex(texts)
    hits1 = hitsk = rr = 0
    for q in answerable:
        scores = (bm25.scores(q['question']) if method == 'bm25' else
                  vectors.scores(q['question']) if method == 'vector' else
                  hybrid_scores(bm25, vectors, q['question']))
        top = [names[i] for i in rank(scores, k)]
        hits1 += top[0] == q['doc']
        if q['doc'] in top:
            hitsk += 1; rr += 1 / (top.index(q['doc']) + 1)
    n = len(answerable)
    return len(texts), round(hits1 / n, 2), round(hitsk / n, 2), round(rr / n, 3)
for chunker, method, want in ((chunk_fixed, 'hybrid', (52, 0.85, 1.00, 0.918)),
                              (chunk_sentences, 'bm25', (70, 0.91, 1.00, 0.949)),
                              (chunk_sentences, 'vector', (70, 0.87, 1.00, 0.932)),
                              (chunk_sections, 'vector', (60, 0.85, 0.98, 0.912)),
                              (chunk_sections, 'bm25', (60, 0.89, 1.00, 0.938)),
                              (chunk_sentences_titled, 'bm25', (70, 0.95, 1.00, 0.965)),
                              (chunk_sentences_titled, 'hybrid', (70, 0.91, 1.00, 0.952))):
    check(f'{chunker.__name__} {method}', evaluate(chunker, method), want)
assistant = SupportAssistant()
answered = right_source = has_fact = refused = 0
for q in questions:
    result = assistant.answer(q['question'])
    if q['doc'] is None:
        refused += not result['grounded']
    else:
        if result['grounded']:
            answered += 1
            if result['source'] == q['doc']:
                right_source += 1
                key = re.escape(q['answer'].lower().replace('rs ', '').split()[0].strip('%,'))
                has_fact += re.search(rf'\b{key}\b', result['answer'].lower()) is not None
check('answered', answered, 50); check('right source', right_source, 38)
check('contained the fact', has_fact, 12); check('correctly refused', refused, 7)
check('score kept for Chapter 57', 'score' in assistant.answer('How long is the standard warranty?'), True)
b, c = assistant.confidence('Do you accept cryptocurrency?')
check('unanswerable scores low', b < 8 or c < 0.6, True)
b, c = assistant.confidence('How long is the warranty on the Industrial Crate?')
check('answerable scores high', b >= 8 and c >= 0.6, True)
check('order tool', run_tool_call(propose_tool_call('Where is order SO-4472?'))['status'], 'packing')
check('whitelist', 'error' in run_tool_call(propose_tool_call('What would 1200 units of product 102 cost?'), allowed={'order_status'}), True)
quote = run_tool_call(propose_tool_call('What would 1200 units of product 102 cost?'))
check('price tool discount', quote['discount_pct'], 8.0)
check('price tool total', quote['total_with_gst'], 977040.0)
check('unknown order handled', 'error' in run_tool_call(propose_tool_call('Check SO-9999 please')), True)
check('no tool for a policy question', propose_tool_call('How long is the warranty?'), None)
current = {n: t for n, t in documents.items() if 'superseded' not in n}
pairs = build_chunks(current, chunk_sentences)
names = [n for n, _ in pairs]; texts = [c for _, c in pairs]
bm25, vectors = BM25(texts), VectorIndex(texts)
top = [names[i] for i in rank(hybrid_scores(bm25, vectors, 'Is delivery free above a certain order value?'), 3)]
check('filtering removes the dead policy', 'policy_delivery_rev3_superseded' in top, False)
print(f'ch55_check.py: {ok} checks passed')
