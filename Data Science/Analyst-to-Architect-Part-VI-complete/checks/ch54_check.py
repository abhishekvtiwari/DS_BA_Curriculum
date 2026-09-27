#!/usr/bin/env python3
"""ch54_check.py - checks Chapter 54's numbers against the generated emails and the chapter's own code."""
import json, pathlib, sys
import numpy as np
C = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/book/companion/ch54')
sys.path.insert(0, str(C))
from mock_llm import complete
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    assert (abs(got - want) <= tol) if isinstance(want, (int, float)) and not isinstance(want, bool) else got == want, \
        f'{label}: {got} != {want}'
    ok += 1
truth = json.load(open(C / 'order_data' / 'ground_truth.json', encoding='utf-8'))
emails = {name: (C / 'order_data' / 'emails' / f'{name}.txt').read_text(encoding='utf-8') for name in truth}
check('emails', len(truth), 60)
check('order lines', sum(len(v['items']) for v in truth.values()), 110)
check('total characters', sum(len(t) for t in emails.values()), 19038)
NAIVE = "Extract the order from this email ({name})."
INSTRUCTED = ("Extract the order from this email ({name}). Return JSON only, no prose, with keys "
              "customer, po_number, delivery_date (YYYY-MM-DD), items (product_code, quantity). "
              "Use null when a value is missing.")
WITH_EXAMPLE = INSTRUCTED + """

EXAMPLE
Email: PO-12345: 101 x 20, 107 x 5
Answer: {{"customer": null, "po_number": "PO-12345", "delivery_date": null,
 "items": [{{"product_code": "101", "quantity": 20}}, {{"product_code": "107", "quantity": 5}}]}}"""
def parse(reply):
    text = reply.split('```json')[-1].split('```')[0] if '```' in reply else reply
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
def evaluate(template):
    exact = fields = unparseable = 0
    for name, want in truth.items():
        got = parse(complete(template.format(name=name) + '\nEMAIL:\n' + emails[name]))
        if got is None:
            unparseable += 1
            continue
        checks = (got.get('customer') == want['customer'], got.get('po_number') == want['po_number'],
                  got.get('delivery_date') == want['delivery_date'],
                  sorted((i['product_code'], i['quantity']) for i in got.get('items') or [])
                  == sorted((i['product_code'], i['quantity']) for i in want['items']))
        fields += sum(checks); exact += all(checks)
    return exact, fields, unparseable
for label, template, want in (('naive', NAIVE, (12, 156, 4)), ('instructed', INSTRUCTED, (35, 215, 0)),
                              ('with example', WITH_EXAMPLE, (47, 227, 0))):
    check(f'{label} prompt', evaluate(template), want)
# softmax and sampling numbers quoted in 54.1 and 54.5
logits = np.array([3.2, 2.9, 1.4, 2.1, -0.5, -4.0])
p = np.exp(logits - logits.max()); p /= p.sum()
check('top token probability', round(float(p[0]), 3), 0.442)
check('probabilities sum to 1', round(float(p.sum()), 6), 1.0)
def counts(temperature=1.0, top_p=1.0, draws=10_000, seed=54):
    scaled = logits / temperature
    q = np.exp(scaled - scaled.max()); q /= q.sum()
    order = np.argsort(-q); keep = np.cumsum(q[order]) <= top_p; keep[0] = True
    allowed = order[keep]; r = q[allowed] / q[allowed].sum()
    picks = np.random.default_rng(seed).choice(allowed, size=draws, p=r)
    return np.bincount(picks, minlength=len(logits)) / draws
check('temperature 0.2 top share', round(float(counts(temperature=0.2)[0]), 3), 0.816)
check('top_p 0.9 keeps two tokens', int((counts(top_p=0.9) > 0).sum()), 2)
check('adding a constant does not change softmax',
      bool(np.allclose(np.exp(logits) / np.exp(logits).sum(), np.exp(logits + 10) / np.exp(logits + 10).sum())), True)
# the mock's documented failure modes
check('chat wrapper when JSON is not demanded', '```json' in complete('Extract (email_001).\nEMAIL:\n' + emails['email_001']), True)
check('json only when demanded', complete(INSTRUCTED.format(name='email_001') + '\nEMAIL:\n' + emails['email_001']).lstrip().startswith('{'), True)
check('email_007 breaks the JSON', parse(complete('Extract (email_007).\nEMAIL:\n' + emails['email_007'])) is None, True)
# cost arithmetic quoted in the answers
tokens = sum(len(t) for t in emails.values()) / 4
check('tokens over the corpus', round(tokens), 4760)
check('cost at $2 per million', round(tokens / 1e6 * 2, 4), 0.0095)
print(f'ch54_check.py: {ok} checks passed')
