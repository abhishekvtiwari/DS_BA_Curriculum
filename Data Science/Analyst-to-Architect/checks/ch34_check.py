#!/usr/bin/env python3
"""ch34_check.py - checks the numbers quoted in Chapter 34's prose against the practice folder."""
import csv, pathlib, subprocess, sys
P = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1] / 'companion' / 'ch34')
ok = 0
def check(label, got, want):
    global ok
    assert got == want, f'{label}: {got!r} != {want!r}'
    ok += 1
rows = list(csv.DictReader(open(P / 'sales_lines_2025.csv', newline='', encoding='utf-8')))
check('order lines', len(rows), 326)
check('total revenue', round(sum(float(r['net_revenue']) for r in rows), 2), 4335471.00)
check('customers', len({r['customer_name'] for r in rows}), 23)
check('cities (Figure 34.2)', len({r['city'] for r in rows}), 16)
check('Mumbai lines', sum(r['city'] == 'Mumbai' for r in rows), 74)
check('Pune lines', sum(r['city'] == 'Pune' for r in rows), 42)
check('Bengaluru lines', sum(r['city'] == 'Bengaluru' for r in rows), 34)
check('unassigned lines', sum(r['sales_rep'] == 'unassigned' for r in rows), 16)
dec = [r for r in rows if r['order_date'].startswith('2025-12')]
nov = [r for r in rows if r['order_date'].startswith('2025-11')]
check('December revenue', round(sum(float(r['net_revenue']) for r in dec), 2), 439823.50)
check('November lines', len(nov), 35)
by_cat = {}
for r in dec:
    by_cat[r['category']] = round(by_cat.get(r['category'], 0) + float(r['net_revenue']), 2)
check('December by category', by_cat, {'Storage': 220363.50, 'Kitchen': 142180.00, 'Industrial': 77280.00})
by_seg = {}
for r in dec:
    by_seg[r['segment']] = round(by_seg.get(r['segment'], 0) + float(r['net_revenue']), 2)
check('December by segment', by_seg, {'Wholesale': 205238.50, 'Hospitality': 131080.00, 'Retail': 103505.00})
day = [r for r in rows if r['order_date'] == '2025-12-16']
check('16 December lines', len(day), 7)
check('16 December revenue', round(sum(float(r['net_revenue']) for r in day), 2), 89800.00)
check('16 December customers', len({r['customer_name'] for r in day}), 3)
check('biggest line', max(round(float(r['net_revenue']), 2) for r in rows), 56700.00)
practice = P / 'practice'
exports = sorted(practice.glob('exports/*.csv'))
check('export files', len(exports), 61)
check('November files', len([f for f in exports if '2025-11' in f.name]), 30)
check('header-only file size (LF line endings)', exports[0].stat().st_size, 123)
check('no CRLF line endings', sum(b'\r' in f.read_bytes() for f in exports), 0)
check('empty December files', sum(1 for f in exports if '2025-12' in f.name and len(open(f).readlines()) == 1), 17)
log = (practice / 'logs' / 'report.log').read_text().splitlines()
check('log lines', len(log), 187)
check('ERROR lines', sum(' ERROR ' in l for l in log), 1)
check('WARNING lines', sum(' WARNING ' in l for l in log), 37)
check('INFO lines', sum(' INFO ' in l for l in log), 149)
empty_days = sum(1 for f in exports if len(open(f).readlines()) == 1)
check('empty-day warnings = empty days other than the failed 9 Nov', sum('no sales lines' in l for l in log), empty_days - ('2025-11-09' in {f.name[7:17] for f in exports if len(open(f).readlines()) == 1}))
week = ['2025-12-%02d' % d for d in range(15, 22)]
check('week revenue', round(sum(float(r['net_revenue']) for r in rows if r['order_date'] in week), 2), 159783.00)
print(f'ch34_check.py: {ok} checks passed')
