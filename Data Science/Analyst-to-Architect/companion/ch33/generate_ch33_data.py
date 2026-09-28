#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 33 · The Computer Science You Actually Need
File: generate_ch33_data.py - builds the two files the chapter's matching project uses.
What: writes, under match_data/:
        order_lines.csv              176,110 order lines (order_id, product_id, quantity, net_revenue, order_date):
                                     200,000 drawn, minus repeats of the same product on one order
        carrier_invoice_lines.csv     20,000 lines the logistics partner billed (invoice_line_id, order_id,
                                     product_id, amount): 19,500 bill a real order line, 500 match nothing
      The data is a synthetic, scaled-up Riverstone (about 66,700 orders over 23 months), big enough for
      the slow version to be slow; its amounts are not Riverstone's real revenue.
How:  python generate_ch33_data.py [--lines 200000] [--invoices 20000]
Seed: 33 (fixed), so timings and match counts are comparable with the book's.
Tested on: Python 3.11.15, 3.12 and 3.13 (Ubuntu 24.04). Standard library only.
Riverstone Supplies is fictional; every number here is invented.
"""
import argparse, csv, os, random
from datetime import date, timedelta

ap = argparse.ArgumentParser()
ap.add_argument('--lines', type=int, default=200_000)
ap.add_argument('--invoices', type=int, default=20_000)
ap.add_argument('--out', default='match_data')
a = ap.parse_args()
rng = random.Random(33)
os.makedirs(a.out, exist_ok=True)

PRODUCTS = [101, 102, 103, 104, 105, 106, 107, 108]
START = date(2024, 1, 1)
lines = []
for i in range(a.lines):
    order_id = 100_000 + i // 3
    product_id = rng.choice(PRODUCTS)
    quantity = rng.choice([5, 10, 20, 25, 50, 100])
    unit_price = rng.choice([290, 380, 430, 620, 750, 1150, 1400])
    order_date = START + timedelta(days=rng.randrange(700))
    lines.append((order_id, product_id, quantity, round(quantity * unit_price, 2), order_date.isoformat()))
# One order has at most one line per product: the grain (Chapter 14).
seen = set()
unique_lines = []
for row in lines:
    if (row[0], row[1]) in seen:
        continue
    seen.add((row[0], row[1]))
    unique_lines.append(row)

with open(f'{a.out}/order_lines.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['order_id', 'product_id', 'quantity', 'net_revenue', 'order_date'])
    w.writerows(unique_lines)

invoices = []
billed = rng.sample(unique_lines, k=min(a.invoices - 500, len(unique_lines)))
for n, row in enumerate(billed, start=1):
    amount = row[3] * rng.choice([1.0, 1.0, 1.0, 0.98, 1.02])       # some invoices disagree slightly
    invoices.append((f'INV{n:06d}', row[0], row[1], round(amount, 2)))
for n in range(len(invoices) + 1, len(invoices) + 501):             # invoices for orders that don't exist
    invoices.append((f'INV{n:06d}', rng.randrange(900_000, 999_999), rng.choice(PRODUCTS),
                     round(rng.uniform(2000, 90000), 2)))
rng.shuffle(invoices)
with open(f'{a.out}/carrier_invoice_lines.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['invoice_line_id', 'order_id', 'product_id', 'amount'])
    w.writerows(invoices)

print(f'wrote {a.out}/order_lines.csv: {len(unique_lines):,} order lines')
print(f'wrote {a.out}/carrier_invoice_lines.csv: {len(invoices):,} invoice lines '
      f'({len(invoices) - 500:,} should match, 500 should not)')
