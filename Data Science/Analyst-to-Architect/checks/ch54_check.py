#!/usr/bin/env python3
"""ch54_check.py - checks Chapter 54's headline numbers against the generated emails and the chapter's own code.
Usage: python3 ch54_check.py [path/to/companion/ch54]   (run generate_order_emails.py there first)"""
import pathlib, sys
import numpy as np

C = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1] / 'companion' / 'ch54')
sys.path.insert(0, str(C.resolve()))
from mock_llm import complete
from extraction import NAIVE, INSTRUCTED, WITH_EXAMPLE, truth, emails, parse, mark, evaluate

ok = 0
def check(label, got, want):
    global ok
    assert got == want, f'{label}: {got} != {want}'
    ok += 1

check('emails', len(truth), 60)
check('order lines', sum(len(v['items']) for v in truth.values()), 110)
check('total characters', sum(len(t) for t in emails.values()), 19038)
check('no file name in any prompt', any('{name}' in t for t in (NAIVE, INSTRUCTED, WITH_EXAMPLE)), False)
for label, template, want in (('naive', NAIVE, (13, 161, 3)), ('instructed', INSTRUCTED, (35, 215, 0)),
                              ('with example', WITH_EXAMPLE, (47, 227, 0))):
    check(f'{label} prompt', evaluate(template, list(truth)), want)
answers = {n: parse(complete(WITH_EXAMPLE + '\nEMAIL:\n' + emails[n])) for n in truth}
check('parsed with the example prompt', sum(a is not None for a in answers.values()), 60)
check('golden set (exercise 14)', evaluate(WITH_EXAMPLE, ['email_001', 'email_002', 'email_003', 'email_004',
      'email_005', 'email_008', 'email_010', 'email_011', 'email_012', 'email_014']), (9, 39, 0))

# softmax and sampling numbers quoted in 54.1 and 54.5
logits = np.array([3.2, 2.9, 1.4, 2.1, -0.5, -4.0])
p = np.exp(logits - logits.max()); p /= p.sum()
check('top token probability', round(float(p[0]), 3), 0.442)
def counts(temperature=1.0, top_p=1.0, draws=10_000, seed=54):
    scaled = logits / temperature
    q = np.exp(scaled - scaled.max()); q /= q.sum()
    order = np.argsort(-q)
    before = np.cumsum(q[order]) - q[order]
    allowed = order[before < top_p]
    r = q[allowed] / q[allowed].sum()
    picks = np.random.default_rng(seed).choice(allowed, size=draws, p=r)
    return np.bincount(picks, minlength=len(logits)) / draws
check('temperature 0.2 top share', round(float(counts(temperature=0.2)[0]), 3), 0.816)
check('top_p 0.9 keeps three tokens', int((counts(top_p=0.9) > 0).sum()), 3)
check('top_p 0.9 frequencies', [round(float(v), 3) for v in counts(top_p=0.9)], [0.484, 0.359, 0.0, 0.158, 0.0, 0.0])
# temperature by hand (54.5)
for t, want in ((1, 0.574), (0.5, 0.646), (2, 0.537)):
    a, b = 3.2 / t, 2.9 / t
    check(f'two-token softmax at T={t}', round(float(np.exp(a) / (np.exp(a) + np.exp(b))), 3), want)
# LoRA arithmetic (54.9)
check('LoRA share', round(2 * 4096 * 8 / 4096 ** 2 * 100, 2), 0.39)
# the stand-in's documented habits
check('chat wrapper when JSON is not demanded', '```json' in complete(NAIVE + '\nEMAIL:\n' + emails['email_001']), True)
check('json only when demanded', complete(INSTRUCTED + '\nEMAIL:\n' + emails['email_001']).lstrip().startswith('{'), True)
check('one in fifteen replies broken without JSON-only',
      sum(parse(complete(NAIVE + '\nEMAIL:\n' + t)) is None for t in emails.values()), 3)
# cost arithmetic quoted in the answers
tokens = sum(len(t) for t in emails.values()) / 4
check('tokens over the corpus', round(tokens), 4760)
check('cost at $2 per million', round(tokens / 1e6 * 2, 4), 0.0095)
print(f'ch54_check.py: {ok} checks passed')
