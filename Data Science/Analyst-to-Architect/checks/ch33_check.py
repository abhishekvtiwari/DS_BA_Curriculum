#!/usr/bin/env python3
"""ch33_check.py - checks the numbers quoted in Chapter 33 against the generated data and the timing log."""
import csv, pathlib, re, sys
from collections import Counter
D = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/book/companion/ch33')
ok = 0
def check(label, got, want):
    global ok
    assert got == want, f'{label}: {got!r} != {want!r}'
    ok += 1
lines = list(csv.DictReader(open(D / 'match_data' / 'order_lines.csv', newline='', encoding='utf-8')))
invoices = list(csv.DictReader(open(D / 'match_data' / 'supplier_invoices.csv', newline='', encoding='utf-8')))
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
log = (pathlib.Path('/home/claude/book/checks/ch33_timings_log.txt')).read_text()
for quoted in ['0.96 s', '7.51 s', '0.045 s', '0.009 s', '1.451 s', '0.873 s', '0.003 s', '242785' if False else '0.226 s']:
    check(f'timing {quoted} in the log', quoted in log, True)
check('naive doubles with the invoices', round(7.51 / 3.73, 1), 2.0)
check('predicted full file', round(7.51 * 10), 75)
print(f'ch33_check.py: {ok} checks passed')
