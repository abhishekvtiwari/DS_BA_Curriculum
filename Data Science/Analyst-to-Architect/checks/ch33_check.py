#!/usr/bin/env python3
"""ch33_check.py - checks the numbers quoted in Chapter 33 against the generated data and the timing log."""
import csv, pathlib, re, sys
from collections import Counter
BOOK = pathlib.Path(__file__).resolve().parents[1]
D = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BOOK / 'companion' / 'ch33'
ok = 0
def check(label, got, want):
    global ok
    assert got == want, f'{label}: {got!r} != {want!r}'
    ok += 1
lines = list(csv.DictReader(open(D / 'match_data' / 'order_lines.csv', newline='', encoding='utf-8')))
invoices = list(csv.DictReader(open(D / 'match_data' / 'carrier_invoice_lines.csv', newline='', encoding='utf-8')))
check('order lines', len(lines), 176110)
check('invoice lines', len(invoices), 20000)
index = {(l['order_id'], l['product_id']): l for l in lines}
check('index keys', len(index), 176110)
matched = sum(1 for i in invoices if (i['order_id'], i['product_id']) in index)
check('matched', matched, 19500); check('unmatched', len(invoices) - matched, 500)
check('orders', len({l['order_id'] for l in lines}), 66667)
check('most invoiced products', Counter(i['product_id'] for i in invoices).most_common(3),
      [('101', 2607), ('107', 2561), ('104', 2514)])
check('lines above 50,000', sum(1 for l in lines if float(l['net_revenue']) > 50_000), 25133)
check('distinct order dates', len({l['order_date'] for l in lines}), 700)
# the bill of materials in section 33.6 must match Chapter 28's SQL
parts = {"Garden Chair": [("Seat shell", 1), ("Steel frame", 1), ("Product label", 1), ("Shipping carton", 1)],
         "Seat shell": [("PP granules", 2.2), ("Masterbatch", 0.08)],
         "Steel frame": [("Leg assembly", 2), ("Steel tube", 1.0), ("Fastener pack", 1)],
         "Leg assembly": [("Steel tube", 1.2), ("Fastener pack", 1)]}
def explode(part, quantity=1.0):
    if part not in parts:
        return {part: quantity}
    totals = {}
    for child, q in parts[part]:
        for material, amount in explode(child, quantity * q).items():
            totals[material] = totals.get(material, 0) + amount
    return totals
bom = explode("Garden Chair")
check('steel tube per chair (Chapter 28)', round(bom['Steel tube'], 2), 3.4)
check('fastener packs per chair', round(bom['Fastener pack'], 2), 3.0)
# fibonacci call counts quoted in section 33.8
calls = 0
def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)
fib(25)
check('plain fib(25) calls', calls, 242785)
# the timing log exists and holds the quoted measurements
log = (BOOK / 'checks' / 'ch33_timings_log.txt').read_text()
for quoted in ['1.48 s', '11.62 s', '0.050 s', '0.007 s', '0.805 s', '0.004 s', '0.248 s', '2.15 s',
               '0.657 s', '0.0070 s', '0.048 s', '0.006 s', '941x', '40.4 MB', '0.0005 MB']:
    check(f'timing {quoted} in the log', quoted in log, True)
check('naive roughly doubles with the invoices', round(11.62 / 5.71, 1), 2.0)
check('predicted full file (s)', round(11.62 * 10), 116)
check('when the business doubles (s)', round(116 * 4), 464)
# the story's growth arithmetic (33.4)
check('invoices grew', round(20_000 / 3_000, 1), 6.7)
check('lines grew', round(176_000 / 40_000, 1), 4.4)
check('work grew', round(20_000 / 3_000 * 176_000 / 40_000), 29)
# the hand-worked DP table for Rs 60 with notes 50, 20, 10
def fewest(amount, notes):
    best = [0] + [None] * amount
    for v in range(1, amount + 1):
        opts = [best[v - n] + 1 for n in notes if n <= v and best[v - n] is not None]
        best[v] = min(opts) if opts else None
    return best
b = fewest(60, (50, 20, 10))
check('DP table', [b[v] for v in range(0, 61, 10)], [0, 1, 1, 2, 2, 1, 2])
# greedy = DP with and without the Rs 2000 note, every multiple of 10 up to 5,000
def greedy(amount, notes):
    c = 0
    for n in notes:
        c, amount = c + amount // n, amount % n
    return c if amount == 0 else None
for notes in [(2000, 500, 200, 100, 50, 20, 10), (500, 200, 100, 50, 20, 10)]:
    best = fewest(5000, notes)
    check(f'greedy optimal for {notes[0]}', all(greedy(a, notes) == best[a] for a in range(0, 5001, 10)), True)
    check('same answers without 2000', [best[a] for a in (760, 2750)], [4, 4] if notes[0] == 2000 else [4, 7])
# 66,667 orders against the one-year database's 175 orders
check('scale vs one-year database', round(66_667 / 175), 381)
print(f'ch33_check.py: {ok} checks passed')
