#!/usr/bin/env python3
"""ch58_check.py - checks Chapter 58's companion and the numbers its prose quotes.

Usage: python3 checks/ch58_check.py [path/to/companion/ch58]
  * the functions the chapter writes out (decide, write, run) are the ones intake.py holds;
  * intake outcomes, replay, audit counts, accuracy by segment, answer 6's schema experiments;
  * the ROI, break-even and threshold arithmetic quoted in sections 58.5 and 58.7 and the answers.
Every chapter output itself is checked by tools/verify_python.py; this file checks the prose around them."""
import pathlib, re, sys

BOOK = pathlib.Path(__file__).resolve().parents[1]
C = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BOOK / 'companion' / 'ch58'
sys.path.insert(0, str(C))
import erp, intake
from intake import run, validate

ok = 0
def check(label, got, want, tol=0.0):
    global ok
    if isinstance(want, float):
        assert abs(got - want) <= tol + 1e-9, f'{label}: {got} != {want}'
    else:
        assert got == want, f'{label}: {got!r} != {want!r}'
    ok += 1

# 1. The chapter's code is intake.py's code.
md = (BOOK / 'manuscript' / 'ch58-intelligent-automation.md').read_text(encoding='utf-8')
module = (C / 'intake.py').read_text(encoding='utf-8')
blocks = re.findall(r'^```python\n(.*?)^```$', md, re.S | re.M)
for name in ('decide', 'write'):
    block = next(b for b in blocks if f'def {name}(' in b)
    body = block[block.index(f'def {name}('):].split('\n\nprint(')[0].strip()
    check(f'chapter {name}() is intake.py\'s', body in module, True)
run_block = next(b for b in blocks if 'def run(' in b)
chapter_run = run_block[run_block.index('def run('):].strip()
breaker = re.search(r'        processed = sum.*?raise BatchAborted\(message\)\n', module, re.S).group(0)
module_run = module[module.index('def run('):module.index('\n\nif __name__')].replace(breaker, '').strip()
chapter_run = chapter_run.replace('run_id="2026-03-02T06:00:00"', 'run_id=FIRST_RUN')
check('chapter run() is intake.py\'s without the breaker', chapter_run, module_run)
for line in ('BREAKER_SHARE = 0.2', 'BREAKER_MINIMUM = 10', 'class BatchAborted(Exception):'):
    check(f'breaker snippet: {line}', line in md and line in module, True)
schema_in_md = ''.join(re.findall(r'^```sql\n(.*?)^```$', md, re.S | re.M))
for statement in re.findall(r'CREATE TABLE.*?\);', erp.SCHEMA, re.S):
    check(f'schema shown: {statement[:25]}', statement in schema_in_md, True)

# 2. Outcomes, replay and audit.
truth, emails = intake.load_emails()
erp.rebuild()
counts = run(emails)['counts']
check('outcomes', counts, {'loaded': 53, 'awaiting_approval': 6, 'held': 1})
replay = run(emails, run_id='2026-03-02T06:05:12')['counts']
check('replay', replay, {'duplicate_ignored': 59, 'held': 1})
connection = erp.connect()
audit = {r['action']: r['n'] for r in connection.execute('SELECT action, COUNT(*) AS n FROM audit_log GROUP BY action')}
check('audit after two runs', audit, {'proposed': 120, 'loaded': 53, 'awaiting_approval': 6, 'held': 2,
                                       'duplicate_ignored': 59})
connection.close()

# 3. Accuracy, overall and by style.
def is_correct(connection, row):
    want = truth[row['source_email']]
    lines = connection.execute('SELECT product_code, quantity FROM order_lines WHERE order_id = ?',
                               (row['order_id'],)).fetchall()
    return (row['po_number'] == want['po_number'] and row['customer'] == want['customer']
            and row['delivery_date'] == want['delivery_date']
            and sorted((l['product_code'], l['quantity']) for l in lines)
            == sorted((i['product_code'], i['quantity']) for i in want['items']))
erp.rebuild(); run(emails)
connection = erp.connect()
rows = connection.execute("SELECT * FROM orders WHERE status = 'loaded'").fetchall()
wrong = sum(not is_correct(connection, r) for r in rows)
check('silently wrong', (len(rows), wrong), (53, 10))
def style(text):
    if '|' in text: return 'table'
    if re.search(r'^- ', text, re.MULTILINE): return 'bullets'
    if 'Forwarded message' in text: return 'forwarded'
    if 'would like to order' in text: return 'prose'
    return 'terse'
erp.rebuild(); run(emails, approval_limit=10 ** 9)
connection = erp.connect()
per = {}
for r in connection.execute('SELECT * FROM orders').fetchall():
    per.setdefault(style(emails[r['source_email']]), [0, 0])[0 if is_correct(connection, r) else 1] += 1
check('segments', per, {'bullets': [13, 0], 'forwarded': [14, 0], 'terse': [10, 0], 'table': [7, 4], 'prose': [3, 8]})
check('perfect segment share', round(37 / 60, 2), 0.62)
check('rule of three', round(3 / 37, 3), 0.081)
check('customer and PO right on all 60 (story)', all(
    (lambda o: o['customer'] == truth[n]['customer'] and o['po_number'] == truth[n]['po_number'])(
        intake.tolerant_parse(intake.call(intake.build_prompt('v3', t)))) for n, t in emails.items()), True)

# 4. Answer 6: the two keys, removed one at a time.
original = erp.SCHEMA
no_email_key = original.replace('NOT NULL UNIQUE,  -- the idempotency key', 'NOT NULL,  -- the idempotency key')
no_keys = no_email_key.replace(',\n    UNIQUE (customer, po_number)                 -- one PO, one order', '')
for label, schema, want_counts, want_orders in (
        ('no email key', no_email_key, {'duplicate_ignored': 59, 'held': 1}, 59),
        ('no keys', no_keys, {'loaded': 53, 'awaiting_approval': 6, 'held': 1}, 118)):
    assert schema != original
    erp.SCHEMA = schema; erp.rebuild(); run(emails)
    check(f'answer 6, {label}', run(emails, run_id='2026-03-02T06:05:12')['counts'], want_counts)
    check(f'answer 6, {label}: orders', erp.connect().execute('SELECT COUNT(*) FROM orders').fetchone()[0], want_orders)
erp.SCHEMA = original; erp.rebuild()

# 5. The arithmetic in sections 58.5 and 58.7, and answers 9, 11, 15.
st, er = 53 / 60, 10 / 53
E, rate = 40, 300 / 60
labour = {'manual': E * 3.0 * rate, 'assisted': (E * 0.75 + E * (1 - st) * 2.0) * rate, 'straight': E * (1 - st) * 2.0 * rate}
unseen = E * st * er; missed = unseen * 0.1
check('manual ₹600', round(labour['manual']), 600)
check('assisted ₹1,530', round(labour['assisted'] + missed * 2000), 1530)
check('straight ₹13,380', round(labour['straight'] + unseen * 2000), 13380)
check('about 80 minutes saved', round(E * 3.0 - (E * 0.75 + E * (1 - st) * 2.0)), 81)
saved = labour['assisted'] - labour['straight']
check('break-even rate 1 in ~424', round(1 / (saved / (E * st * 0.9 * 2000))), 424)
check('break-even cost ₹25', round(saved / (unseen * 0.9)), 25)
check('beats typing below ₹83', round((labour['manual'] - labour['straight']) / unseen), 83)
check('factor of about 80', round(er / (saved / (E * st * 0.9 * 2000))), 80)
check('catch rate needed 97%', round(1 - (labour['manual'] - labour['assisted']) / (unseen * 2000), 2), 0.97)
check('answer 11: ₹200 an error', float(round(labour['straight'] + unseen * 200, -1)), 1380.0)
check('answer 15: ₹2,280', round(40 * 0.95 * 0.03 * 2000), 2280)
check('threshold: 1 in 200', 2000 / (2.0 * rate), 200.0)
check('story: 41 s x 40 is about 27 minutes', round(41 * 40 / 60), 27)
check('answer 5 ratios', (round(363550 / 57950, 1), round(579050 / 363550, 1)), (6.3, 1.6))
check('validation catches a bad order', bool(validate({'po_number': '1', 'customer': '', 'delivery_date': '04 Mar',
                                                       'items': [{'product_code': '999', 'quantity': -5}]})), True)
print(f'ch58_check.py: {ok} checks passed')
