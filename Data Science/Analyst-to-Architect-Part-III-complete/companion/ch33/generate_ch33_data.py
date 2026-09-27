#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 33 · The Computer Science You Actually Need
File: generate_ch33_data.py - builds the two files the chapter's matching project uses.
What: writes, under match_data/:
        order_lines.csv        200,000 order lines from Riverstone's ERP (order_id, product_id, quantity, net_revenue, order_date)
        supplier_invoices.csv   20,000 invoice lines a supplier sent, each billing one order line, plus 500 that match nothing
How:  python3 generate_ch33_data.py [--lines 200000] [--invoices 20000]
Seed: 33 (fixed), so timings and match counts are comparable with the book's.
Tested on: Python 3.12.3 (Ubuntu 24.04). Standard library only.
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
# One order can bill the same product only once, which is the grain from Chapter 28.
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
with open(f'{a.out}/supplier_invoices.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['invoice_line_id', 'order_id', 'product_id', 'amount'])
    w.writerows(invoices)

print(f'order lines {len(unique_lines):,}  invoice lines {len(invoices):,} '
      f'({len(invoices) - 500:,} should match, 500 should not)')
