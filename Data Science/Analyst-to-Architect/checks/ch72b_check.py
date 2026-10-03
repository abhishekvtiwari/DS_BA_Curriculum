#!/usr/bin/env python3
"""ch72b_check.py - recompute every measured figure in Chapter 72B and assert the chapter quotes it.

Usage: python3 checks/ch72b_check.py        (run from the book folder)

Chapter 72B's whole argument is that a cleaning figure is only trustworthy if it was produced by
running something. This script is that claim applied to the chapter itself: every number it states
is re-derived here from the two files it uses, and the chapter text is searched for the result. A
future edit that changes a figure, or a pandas release that changes a behaviour, fails here.

Sources (both ship with Chapter 14):
  companion/ch14/orders_q4_2025_export.csv     the messy export
  companion/ch14/customers_crm_export.csv      the messy customer master
  companion/ch14/clean_truth_orders_q4_2025.csv  the correct answer

What it checks:
  1. Row accounting: 25,976 rows = 25,832 genuine + 137 duplicates + 6 headers + 1 footer.
  2. Date shapes (20,890 / 3,227 / 1,812 / 40) sum to the 25,969-row body, and the NaT counts
     produced by the four one-liners (17,089 / 5,088 / 49 / 49).
  3. dayfirst=True corrupts the ISO values; format dispatch leaves exactly the 9 impossible dates
     and only the three real months.
  4. Categories: 18 status spellings -> 7 normalised -> 4 mapped; 17 branch -> 12 -> 4; 880
     trailing-space sales_rep rows turning 12 reps into 23.
  5. Money: the three gross totals (Rs 41.87 / 43.89 / 46.01 crore), the Rs. -> 0.14 regex trap,
     and the discount fraction bug (Rs 19.57 lakh, 0.44%).
  6. Keys: 537 failing rows, 94 distinct codes, Rs 91.7 lakh, and zfill(4) -> 0 failures.
  7. Units: 141 carton rows summing to 540 raw and 5,400 in the truth file (factor 10).
  8. Q72B-069's reconciliation decomposition, and that it is within 0.28% of truth for the wrong
     reasons.
  9. The answer_key.json differences the chapter documents in section 72B.10 are still the
     differences that exist.
Exit code 1 on any failure.
"""
import json
import sys
import warnings
from pathlib import Path

import pandas as pd

warnings.simplefilter('ignore')

BOOK = Path(__file__).resolve().parents[1]
C14 = BOOK / 'companion' / 'ch14'
MD = next((BOOK / 'manuscript').glob('ch72b-*.md')).read_text(encoding='utf-8')
CR, LAKH = 1e7, 1e5
ok = True


def check(name, cond, detail=''):
    global ok
    ok &= bool(cond)
    print(('PASS ' if cond else 'FAIL ') + name + (f'  ({detail})' if detail and not cond else ''))


def quoted(s, name=None):
    """The chapter must contain this figure, written as the chapter writes it."""
    check(f'chapter quotes {name or s}', s in MD, f'{s!r} not in ch72b')


# ---------------------------------------------------------------- load
raw = pd.read_csv(C14 / 'orders_q4_2025_export.csv', dtype=str, keep_default_na=False)
cust = pd.read_csv(C14 / 'customers_crm_export.csv', dtype=str, keep_default_na=False)
truth = pd.read_csv(C14 / 'clean_truth_orders_q4_2025.csv')
key = json.loads((C14 / 'answer_key.json').read_text(encoding='utf-8'))

hdr = raw['order_item_id'] == 'order_item_id'
foot = raw['order_item_id'] == ''
body = raw[~hdr & ~foot].copy()
s = body['order_date']

# ---------------------------------------------------------------- 1. row accounting
dups = body.duplicated(subset=['order_item_id']).sum()
genuine = len(body) - dups
check('25,976 rows below the header', len(raw) == 25976, len(raw))
check('6 repeated header rows', hdr.sum() == 6, hdr.sum())
check('1 footer row', foot.sum() == 1, foot.sum())
check('137 duplicate order lines', dups == 137, dups)
check('25,832 genuine lines', genuine == 25832, genuine)
check('the four categories sum to 25,976',
      hdr.sum() + foot.sum() + dups + genuine == len(raw))
check('body is 25,969 rows', len(body) == 25969, len(body))
check('14,372 distinct orders', truth['order_id'].nunique() == 14372)
check('1.80 lines per order', round(len(truth) / truth['order_id'].nunique(), 2) == 1.80)
for f in ('25,976', '25,969', '25,832', '14,372', '1.80'):
    quoted(f)

# ---------------------------------------------------------------- 2. date shapes and NaT
shapes = {
    'dd-mm-yyyy': s.str.match(r'^\d{2}-\d{2}-\d{4}$').sum(),
    'iso': s.str.match(r'^\d{4}-\d{2}-\d{2}$').sum(),
    'dd/mm/yyyy': s.str.match(r'^\d{2}/\d{2}/\d{4}$').sum(),
    'serial': s.str.match(r'^\d{5}$').sum(),
}
check('date shapes 20,890 / 3,227 / 1,812 / 40',
      list(shapes.values()) == [20890, 3227, 1812, 40], shapes)
check('the four shapes account for every body row', sum(shapes.values()) == len(body))
nats = {}
for label, kw in [('defaults', {}), ('dayfirst', {'dayfirst': True}),
                  ('mixed', {'format': 'mixed'}),
                  ('mixed+dayfirst', {'format': 'mixed', 'dayfirst': True})]:
    nats[label] = pd.to_datetime(s, errors='coerce', **kw).isna().sum()
check('to_datetime defaults -> 17,089 NaT', nats['defaults'] == 17089, nats['defaults'])
check('dayfirst=True -> 5,088 NaT', nats['dayfirst'] == 5088, nats['dayfirst'])
check('both format="mixed" variants -> 49 NaT',
      nats['mixed'] == nats['mixed+dayfirst'] == 49, nats)
check('66% of the column destroyed by the defaults', round(17089 / len(body) * 100) == 66)
for f in ('17,089', '5,088', '20890', '3227', '1812'):
    quoted(f)

# ---------------------------------------------------------------- 3. dayfirst corrupts ISO
iso = s.str.match(r'^\d{4}-\d{2}-\d{2}$')
p_day = pd.to_datetime(s, errors='coerce', format='mixed', dayfirst=True)
check("dayfirst turns 2025-10-01 into 2025-01-10",
      str(p_day[iso & (s == '2025-10-01')].iloc[0].date()) == '2025-01-10')

parsed = pd.Series(pd.NaT, index=s.index, dtype='datetime64[ns]')
for rx, fmt in [(r'^\d{2}-\d{2}-\d{4}$', '%d-%m-%Y'), (r'^\d{2}/\d{2}/\d{4}$', '%d/%m/%Y'),
                (r'^\d{4}-\d{2}-\d{2}$', '%Y-%m-%d')]:
    m = s.str.match(rx)
    parsed[m] = pd.to_datetime(s[m], format=fmt, errors='coerce')
m = s.str.match(r'^\d{5}$')
parsed[m] = pd.Timestamp('1899-12-30') + pd.to_timedelta(pd.to_numeric(s[m]), unit='D')

p_mix = pd.to_datetime(s, errors='coerce', format='mixed')
both = p_mix.notna() & parsed.notna()
check('format="mixed" disagrees with the correct parse on 8,804 rows (34.0%)',
      (p_mix[both] != parsed[both]).sum() == 8804)
check('dayfirst=True disagrees on 1,330 rows (5.1%)',
      (p_day[both] != parsed[both]).sum() == 1330)
check('format dispatch leaves exactly 9 NaT', parsed.isna().sum() == 9)
check('the 9 unparsed are the impossible dates',
      sorted(s[parsed.isna()].unique()) == ['31-09-2025', '31-11-2025', '32-10-2025'])
check('only the three real months remain',
      sorted(parsed.dropna().dt.to_period('M').astype(str).unique())
      == ['2025-10', '2025-11', '2025-12'])
check('serial 45933 is 2025-10-03',
      str((pd.Timestamp('1899-12-30') + pd.Timedelta(days=45933)).date()) == '2025-10-03')
for f in ('8,804', '1,330', '34.0%', '5.1%', '45933', '2025-10-03', '1899-12-30'):
    quoted(f)

# the phantom nine months
qty = pd.to_numeric(body['quantity'], errors='coerce')
price = pd.to_numeric(body['unit_price'].str.replace(r'(?i)^rs\.?\s*', '', regex=True)
                      .str.replace('₹', '', regex=False)
                      .str.replace(',', '', regex=False), errors='coerce')
gross = qty * price
gm = gross.groupby(p_mix.dt.to_period('M')).sum().dropna()
phantom = gm[[x for x in gm.index if str(x) < '2025-10']].sum()
check('the naive parse invents Rs 12.78 crore before October',
      round(phantom / CR, 2) == 12.78, round(phantom / CR, 2))
quoted('12.78')

# ---------------------------------------------------------------- 4. categories
check('18 status spellings', body['status'].nunique() == 18)
norm = body['status'].str.strip().str.lower()
check('7 after trim + lower', norm.nunique() == 7)
smap = {'delivered': 'Delivered', 'dlvd': 'Delivered', 'canceled': 'Cancelled',
        'cancelled': 'Cancelled', 'cxl': 'Cancelled', 'shipped': 'Shipped', 'pending': 'Pending'}
mapped = norm.map(smap)
check('the 7-entry map leaves nothing unmapped', mapped.isna().sum() == 0)
check('dropping cxl leaves 32 rows unmapped',
      norm.map({k: v for k, v in smap.items() if k != 'cxl'}).isna().sum() == 32)
check('mapped status counts 22,551 / 1,174 / 1,144 / 1,100',
      [mapped.value_counts()[k] for k in ('Delivered', 'Pending', 'Shipped', 'Cancelled')]
      == [22551, 1174, 1144, 1100])
check('naive groupby shows Delivered as 19,835',
      body['status'].value_counts()['Delivered'] == 19835)
check('17 branch spellings -> 12 normalised',
      body['branch'].nunique() == 17 and body['branch'].str.strip().str.lower().nunique() == 12)
check('880 trailing-space sales_rep rows, 23 reps becoming 12',
      (body['sales_rep'] != body['sales_rep'].str.strip()).sum() == 880
      and body['sales_rep'].nunique() == 23
      and body['sales_rep'].str.strip().nunique() == 12)
check('12 segment variants map to 3',
      cust['segment'].nunique() == 12
      and cust['segment'].str.strip().str.lower()
      .replace({'horeca': 'hospitality', 'hotel/restaurant': 'hospitality',
                'distributor': 'wholesale'}).nunique() == 3)
for f in ('22551', '19835', '1,100', '880'):
    quoted(f)

# ---------------------------------------------------------------- 5. money
lazy = pd.to_numeric(body['unit_price'], errors='coerce')
naive = pd.to_numeric(body['unit_price'].str.replace(r'[^0-9.]', '', regex=True), errors='coerce')
check('2,316 currency-text prices', lazy.isna().sum() == 2316, lazy.isna().sum())
check('1,205 Rs.-prefixed and 1,111 rupee-sign rows',
      body['unit_price'].str.startswith('Rs').sum() == 1205
      and body['unit_price'].str.startswith('₹').sum() == 1111)
check("the naive regex turns 'Rs. 1,400' into 0.14",
      float(pd.to_numeric(pd.Series(['Rs. 1,400']).str.replace(r'[^0-9.]', '', regex=True))[0]) == 0.14)
check('the correct cleaner leaves exactly 7 prices and no nulls',
      sorted(price.unique()) == [115.0, 290.0, 380.0, 430.0, 620.0, 750.0, 1400.0]
      and price.isna().sum() == 0)
g_lazy, g_naive, g_ok = (qty * lazy).sum(), (qty * naive).sum(), gross.sum()
check('gross: 41.87 / 43.89 / 46.01 crore',
      [round(v / CR, 2) for v in (g_lazy, g_naive, g_ok)] == [41.87, 43.89, 46.01],
      [round(v / CR, 2) for v in (g_lazy, g_naive, g_ok)])
check('lazy to_numeric hides Rs 4.14 crore (9.0%)',
      round((g_ok - g_lazy) / CR, 2) == 4.14 and round((g_ok - g_lazy) / g_ok * 100, 1) == 9.0)
check('the regex bug hides Rs 2.13 crore (4.6%)',
      round((g_ok - g_naive) / CR, 2) == 2.13 and round((g_ok - g_naive) / g_ok * 100, 1) == 4.6)
disc = pd.to_numeric(body['discount_pct'], errors='coerce')
check('1,371 fractional discounts', ((disc > 0) & (disc < 1)).sum() == 1371)
dfix = disc.where(disc > 1, disc * 100)
r_lazy = (qty * price * (1 - disc / 100)).sum()
r_fix = (qty * price * (1 - dfix / 100)).sum()
check('the discount bug overstates by Rs 19.57 lakh (0.44%)',
      round((r_lazy - r_fix) / LAKH, 2) == 19.57
      and round((r_lazy / r_fix - 1) * 100, 2) == 0.44)
for f in ('2,316', '1,205', '1,111', '0.14', '41.87', '43.89', '46.01', '4.14', '2.13', '1371', '1,956,636', '19.6 lakh'):
    quoted(f)

# ---------------------------------------------------------------- 6. keys
master = set(cust['customer_code'])
fail = ~body['customer_code'].isin(master)
check('537 rows fail the exact join', fail.sum() == 537, fail.sum())
check('94 distinct codes lost', body['customer_code'][fail].nunique() == 94)
check('they carry Rs 91.7 lakh (1.99%)',
      round(gross[fail].sum() / LAKH, 1) == 91.7
      and round(gross[fail].sum() / gross.sum() * 100, 2) == 1.99)
check('zfill(4) takes the failures to zero',
      (~body['customer_code'].str.zfill(4).isin(master)).sum() == 0)
check('code lengths 40 two-char and 497 three-char',
      dict(body['customer_code'].str.len().value_counts()).get(2) == 40
      and dict(body['customer_code'].str.len().value_counts()).get(3) == 497)
check('master is uniformly 4 characters', cust['customer_code'].str.len().eq(4).all())
check('customer_code is unique in the master', cust['customer_code'].duplicated().sum() == 0)
check('48 duplicate customer records by normalised name',
      cust['customer_name'].str.strip().str.replace(r'\s+', ' ', regex=True).str.lower()
      .str.replace(r'\s*(pvt\.?\s*ltd\.?|private\s+limited)$', '', regex=True)
      .str.strip().duplicated().sum() == 48)
for f in ('537', '94', '91.7', '1.99%'):
    quoted(f)

# ---------------------------------------------------------------- 7. units and typos
ctn = body['qty_unit'] == 'CTN'
check('141 carton rows summing to 540', ctn.sum() == 141 and qty[ctn].sum() == 540)
ctn_ids = pd.to_numeric(body['order_item_id'][ctn])
check('the truth file gives those rows 5,400, so the factor is 10',
      truth[truth['order_item_id'].isin(ctn_ids)]['quantity'].sum() == 5400)
ez = [187761, 191340, 200981, 205978, 206224, 209166]
iid = pd.to_numeric(body['order_item_id'], errors='coerce')
check('6 extra-zero rows, inflating quantity by 2,205 units',
      qty[iid.isin(ez)].sum() - truth[truth['order_item_id'].isin(ez)]['quantity'].sum() == 2205)
check('the historical maximum of 90 catches exactly those 6 rows',
      (qty > 90).sum() == 6 and sorted(iid[qty > 90].astype(int)) == sorted(ez))
check('median 35, p95 70, p99 85, max 700',
      [int(qty.median()), int(qty.quantile(.95)), int(qty.quantile(.99)), int(qty.max())]
      == [35, 70, 85, 700])
check('14 blank quantity and 8 blank product_id',
      (body['quantity'] == '').sum() == 14 and (body['product_id'] == '').sum() == 8)
check('price identifies product one-to-one',
      all(len(v) == 1 for v in body[body['product_id'] != '']
          .groupby(price[body['product_id'] != ''])['product_id'].unique()))
for f in ('141', '540', '5,400', '2,205', '700'):
    quoted(f)

# ---------------------------------------------------------------- 8. UTC/IST and reconciliation
utc = pd.to_datetime(body['entered_at_utc'], format='ISO8601', utc=True)
ist = utc.dt.tz_convert('Asia/Kolkata')
check('1,604 rows where the UTC date is not the IST date (6.2%)',
      (utc.dt.date != ist.dt.date).sum() == 1604
      and round((utc.dt.date != ist.dt.date).mean() * 100, 1) == 6.2)
ta, tn = truth['net_revenue'].sum(), truth[truth['status'] != 'Cancelled']['net_revenue'].sum()
check('truth: 44.26 crore all lines, 42.39 crore non-cancelled',
      [round(ta / CR, 2), round(tn / CR, 2)] == [44.26, 42.39])
check('prices+discounts cleaned gives 44.38 crore, +0.28% of truth',
      round(r_fix / CR, 2) == 44.38 and round((r_fix / ta - 1) * 100, 2) == 0.28)
dup_mask = body.duplicated(subset=['order_item_id'])
net = qty * price * (1 - dfix / 100)
d1 = net[dup_mask].sum()
d2 = (net[iid.isin(ez) & ~dup_mask]
      - (net[iid.isin(ez) & ~dup_mask] / qty[iid.isin(ez) & ~dup_mask]
         * iid[iid.isin(ez) & ~dup_mask].map(truth.set_index('order_item_id')['quantity']))).sum()
d3 = -(net[ctn & ~dup_mask] * 9).sum()
check('decomposition +0.25 / +0.11 / -0.22 crore',
      [round(d1 / CR, 2), round(d2 / CR, 2), round(d3 / CR, 2)] == [0.25, 0.11, -0.22],
      [round(d1 / CR, 2), round(d2 / CR, 2), round(d3 / CR, 2)])
check('inflating 0.36 crore against understating 0.22 crore',
      round((d1 + d2) / CR, 2) == 0.36 and round(-d3 / CR, 2) == 0.22)
for f in ('1,604', '6.2%', '44.26', '42.39', '44.38', '0.28%'):
    quoted(f)

# ---------------------------------------------------------------- 9. answer_key differences
k = key['orders_export']
check('answer_key still records 137 planted duplicates and 9 impossible dates',
      k['duplicate_rows_planted'] == 137 and k['dates_impossible'] == 9)
check('the documented price_as_text difference is still 2,300 vs 2,316',
      k['price_as_text'] == 2300)
check('the documented discount difference is still 1,362 vs 1,371',
      k['discount_as_fraction'] == 1362)
check('the documented UTC/IST difference is still 1,598 vs 1,604',
      k['utc_date_differs_from_ist_date'] == 1598)
check('codes_without_leading_zeros is still the Kolkata line count, not 537',
      k['codes_without_leading_zeros'] == 3210
      and (truth['branch'] == 'Kolkata').sum() == 3210)
check('section 72B.10 documents all four differences',
      all(x in MD for x in ('2,300', '1,362', '1,598', '3,210')))

print()
print('ALL PASS' if ok else 'SOME CHECKS FAILED')
sys.exit(0 if ok else 1)
