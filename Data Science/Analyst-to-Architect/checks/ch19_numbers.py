#!/usr/bin/env python3
"""ch19_numbers.py - recomputes chapter 19's numbers from the companion files and checks the chapter
states them (in Indian grouping). Covers what LibreOffice can't run: CleanMaster's count, the pivot's
grand total, and every total in the project, answers and timed challenge.  Run from the book folder."""
import os, re, pathlib
import pandas as pd
BOOK = pathlib.Path(__file__).resolve().parent.parent
md = (BOOK / 'manuscript/ch19-spreadsheet-automation.md').read_text(encoding='utf-8')
src = BOOK / 'companion/ch19/branch_files'

def lakh(v):
    i, _, d = f"{v:.2f}".partition('.')
    if len(i) > 3:
        head, tail = i[:-3], i[-3:]
        i = ','.join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + ',' + tail
    return f"₹{i}.{d}"

frames = []
for f in sorted([f for f in os.listdir(src) if f.lower().endswith('.xlsx')], key=str.upper):
    d = pd.read_excel(src / f, dtype={'customer_code': str}); d['source_file'] = f; frames.append(d)
m = pd.concat(frames, ignore_index=True)
ok = m[m.status != 'Cancelled']
m['branch'] = m.source_file.str.extract(r'Riverstone_(.+)_\d{4}-\d{2}\.xlsx')[0].str.replace('_', ' ')
ok = m[m.status != 'Cancelled']
checks = {
    'data rows 25,832': len(m) == 25832,
    'non-cancelled 24,738': len(ok) == 24738,
    'CleanMaster: 0 unmapped': m.status.str.strip().str.lower().isin(
        ['delivered', 'dlvd', 'cancelled', 'canceled', 'cxl', 'shipped', 'pending']).all(),
    'pivot grand total 44,25,77,334': round(m.net_revenue.sum()) == 442577334,
    'customer codes are 4-digit text': m.customer_code.str.fullmatch(r'\d{4}').all(),
}
amounts = [ok.net_revenue.sum(), m.net_revenue.sum()] + list(ok.groupby('branch').net_revenue.sum())
amounts.append(ok.groupby('branch').net_revenue.sum()['Mumbai HO'] - ok.groupby('branch').net_revenue.sum()['Kolkata'])
for a in amounts:
    checks[f'chapter states {lakh(a)}'] = lakh(a) in md
kd = m[m.source_file == 'Riverstone_Kolkata_2025-11.xlsx']
checks['story: Kolkata Nov file ≈ ₹1.88 crore'] = round(kd[kd.status != 'Cancelled'].net_revenue.sum() / 1e7, 2) == 1.88
p = pd.read_excel(BOOK / 'companion/ch19/ch19_practice.xlsx', sheet_name='Master')
checks['LoopDemo total 12,025,947.25 over 994 rows'] = (len(p) == 994 and f"{p.net_revenue.sum():,.2f}" == '12,025,947.25')
months = ok.assign(month=ok.source_file.str[-12:-5]).groupby('month').net_revenue.sum()
print('month totals (unrounded):', {k: lakh(v) for k, v in months.items()})
print('October share: {:.1%}'.format(months['2025-10'] / ok.net_revenue.sum()))
bad = [k for k, v in checks.items() if not v]
for k, v in checks.items():
    print('ok  ' if v else 'FAIL', k)
raise SystemExit(1 if bad else 0)
