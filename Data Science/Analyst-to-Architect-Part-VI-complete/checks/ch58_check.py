#!/usr/bin/env python3
"""ch58_check.py - checks Chapter 58's numbers: intake outcomes, idempotency, accuracy by segment, and the ROI table."""
import os, pathlib, re, sys
C = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/book/companion/ch58')
os.chdir(C); sys.path.insert(0, str(C))
import erp
from intake import run, validate
from pipeline import load_emails
from provider import Meter
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    if isinstance(want, float) and isinstance(got, float):
        assert abs(got - want) <= tol + 1e-9, f'{label}: {got} != {want}'
    else:
        assert got == want, f'{label}: {got} != {want}'
    ok += 1
truth, emails = load_emails()
erp.rebuild()
meter = Meter()
result = run(emails, truth, meter=meter)
counts = result['counts']
check('emails', len(emails), 60)
check('loaded', counts['loaded'], 53)
check('awaiting approval', counts['awaiting_approval'], 6)
check('held for review', counts['held_for_review'], 1)
check('straight-through rate', round(counts['loaded'] / 60, 2), 0.88)
check('model cost of a run', round(meter.cost_rupees(), 2), 4.74, tol=0.01)
connection = erp.connect()
check('orders written', connection.execute('SELECT COUNT(*) AS n FROM orders').fetchone()['n'], 59)
before = 59
run(emails, truth)
after = erp.connect().execute('SELECT COUNT(*) AS n FROM orders').fetchone()['n']
check('replay writes nothing', after, before)
check('duplicates are recorded',
      erp.connect().execute("SELECT COUNT(*) AS n FROM audit_log WHERE action='duplicate_ignored'").fetchone()['n'], 59)
def accuracy(connection, where="status = 'loaded'"):
    right = wrong = 0
    for row in connection.execute(f'SELECT order_id, source_email, po_number, customer, delivery_date FROM orders WHERE {where}'):
        want = truth[row['source_email']]
        lines = [(l['product_code'], l['quantity']) for l in
                 connection.execute('SELECT product_code, quantity FROM order_lines WHERE order_id = ?', (row['order_id'],))]
        matches = (row['po_number'] == want['po_number'] and row['customer'] == want['customer']
                   and row['delivery_date'] == want['delivery_date']
                   and sorted(lines) == sorted((i['product_code'], i['quantity']) for i in want['items']))
        right += matches; wrong += not matches
    return right, wrong
erp.rebuild(); run(emails, truth)
right, wrong = accuracy(erp.connect())
check('auto-loaded correct', right, 43)
check('auto-loaded silently wrong', wrong, 10)
check('silent error rate', round(wrong / (right + wrong), 2), 0.19)
def style(text):
    if '|' in text: return 'table'
    if re.search(r'^- ', text, re.MULTILINE): return 'bullets'
    if 'Forwarded message' in text: return 'forwarded'
    if 'would like to order' in text: return 'prose'
    return 'terse'
erp.rebuild(); run(emails, truth, approval_limit=10 ** 9)
connection = erp.connect()
styles = {name: style(text) for name, text in emails.items()}
per_style = {}
for row in connection.execute('SELECT order_id, source_email, po_number, customer, delivery_date FROM orders'):
    want = truth[row['source_email']]
    lines = [(l['product_code'], l['quantity']) for l in
             connection.execute('SELECT product_code, quantity FROM order_lines WHERE order_id = ?', (row['order_id'],))]
    matches = (row['po_number'] == want['po_number'] and row['customer'] == want['customer']
               and row['delivery_date'] == want['delivery_date']
               and sorted(lines) == sorted((i['product_code'], i['quantity']) for i in want['items']))
    entry = per_style.setdefault(styles[row['source_email']], [0, 0])
    entry[0 if matches else 1] += 1
for name, want in (('bullets', [13, 0]), ('forwarded', [14, 0]), ('terse', [10, 0]),
                   ('table', [7, 4]), ('prose', [3, 8])):
    check(f'{name} emails', per_style[name], want)
check('perfect styles cover 62% of volume', round(sum(per_style[s][0] for s in ('bullets', 'forwarded', 'terse')) / 60, 2), 0.62)
# the ROI arithmetic quoted in section 58.7
straight_through, error_rate = 53 / 60, 10 / 53
check('manual cost per day', round(40 * 3.0 / 60 * 300), 600)
check('assisted cost per day', round((40 * 0.75 + 40 * 0.12 * 2.0) / 60 * 300), 198)
errors = 40 * straight_through * error_rate
check('errors per day if unattended', round(errors, 1), 6.7)
check('straight-through cost per day', round(40 * (1 - straight_through) * 2.0 / 60 * 300 + errors * 2000), 13380)
check('validation catches a bad order', bool(validate({'po_number': '1', 'customer': '', 'delivery_date': '04 Mar',
                                                       'items': [{'product_code': '999', 'quantity': -5}]})), True)
check('validation passes a good one', validate({'po_number': 'PO-12345', 'customer': 'Metro Mart',
                                                'delivery_date': '2026-03-04',
                                                'items': [{'product_code': '101', 'quantity': 20}]}), [])
print(f'ch58_check.py: {ok} checks passed')
