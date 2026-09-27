#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 31 · Causal Inference Without Experiments
File: generate_ch31_data.py - builds the three observational datasets the chapter uses.
What: writes three CSV files under causal_data/:
        region_month.csv     24 months of orders and revenue for Riverstone's four sales regions.
                             North's list prices rose about 6% from 1 October 2025. TRUE effect on order
                             volume: -8.0% (a log effect of -0.0834). Sections 31.3, 31.4, 31.7.
        qbr_program.csv      240 key accounts, some given quarterly business reviews in 2025. The program
                             went to the largest, fastest-growing accounts. TRUE effect: +7.0% revenue.
                             Section 31.5.
        delivery_threshold.csv  60,000 orders around the ₹25,000 free-delivery threshold. TRUE jump in the
                             chance of a repeat order within 90 days: +6.0 percentage points. Section 31.6.
How:  python3 generate_ch31_data.py [--out causal_data]     (standard library only)
Seed: 31 (fixed). The true effects above are what the chapter's methods are trying to recover.
Tested on: Python 3.12.3 (Ubuntu 24.04).
Riverstone Supplies is fictional; every number here is invented.
"""
import argparse, csv, math, os, random
from datetime import date

ap = argparse.ArgumentParser()
ap.add_argument('--out', default='causal_data')
a = ap.parse_args()
rng = random.Random(31)                 # the panel
rng_qbr = random.Random(312)            # the programme's customers
rng_rdd = random.Random(313)            # orders around the threshold
os.makedirs(a.out, exist_ok=True)

# ---------------------------------------------------------------- region-month panel
REGIONS = {'West': 8.05, 'South': 7.75, 'North': 7.55, 'East': 7.25}     # log level of monthly orders
MONTHS = [date(2024 + (6 + i) // 12, (6 + i) % 12 + 1, 1) for i in range(24)]   # 2024-07 .. 2026-06
TREATED, PRICE_CHANGE = 'North', date(2025, 10, 1)
TRUE_EFFECT = math.log(0.92)            # -8% on order volume
SEASON = {1: -0.06, 2: -0.04, 3: 0.02, 4: -0.02, 5: -0.03, 6: -0.05,
          7: -0.02, 8: 0.01, 9: 0.06, 10: 0.11, 11: 0.08, 12: 0.03}     # festive peak in Oct-Nov
rows = []
for region, level in REGIONS.items():
    for t, month in enumerate(MONTHS):
        log_orders = level + 0.008 * t + SEASON[month.month] + rng.gauss(0, 0.035)
        treated_now = int(region == TREATED and month >= PRICE_CHANGE)
        log_orders += TRUE_EFFECT * treated_now
        orders = round(math.exp(log_orders))
        price_index = 1.06 if treated_now else 1.0
        avg_value = round(rng.gauss(24800, 900) * price_index, 2)
        rows.append((region, month.isoformat(), orders, round(orders * avg_value, 2), avg_value,
                     treated_now, int(region == TREATED), int(month >= PRICE_CHANGE)))
with open(f'{a.out}/region_month.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['region', 'month', 'orders', 'revenue', 'avg_order_value', 'price_rise_active', 'is_north', 'is_after'])
    w.writerows(rows)

# ---------------------------------------------------------------- quarterly business review program
QBR_EFFECT = math.log(1.07)             # +7% revenue for accounts in the program
SEGMENTS = ['Retail'] * 5 + ['Hospitality'] * 3 + ['Wholesale'] * 2
prog = []
for cid in range(1, 241):
    segment = rng_qbr.choice(SEGMENTS)
    region = rng_qbr.choice(list(REGIONS))
    size = rng_qbr.lognormvariate(13.4, 0.75)                     # 2024 revenue
    growth = rng_qbr.gauss(0.05, 0.12)                            # 2024 growth rate
    years = rng_qbr.randint(1, 9)
    # The sales team chose the biggest, fastest-growing accounts: selection, not randomization.
    score = -14.2 + 0.95 * math.log(size) + 3.1 * growth + 0.05 * years
    joined = int(rng_qbr.random() < 1 / (1 + math.exp(-score)))
    log_2025 = math.log(size) + growth + rng_qbr.gauss(0.03, 0.10) + QBR_EFFECT * joined
    prog.append((cid, segment, region, years, round(size, 2), round(growth, 4), joined,
                 round(math.exp(log_2025), 2)))
with open(f'{a.out}/qbr_program.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['customer_id', 'segment', 'region', 'years_as_customer', 'revenue_2024', 'growth_2024',
                'in_qbr_program', 'revenue_2025'])
    w.writerows(prog)

# ---------------------------------------------------------------- free-delivery threshold
THRESHOLD, JUMP = 25000, 0.06           # orders at or above 25,000 get free delivery
orders = []
for oid in range(1, 60001):
    value = round(THRESHOLD + rng_rdd.gauss(0, 4200), 2)          # values either side, no bunching
    if value <= 4000:
        continue
    centred = (value - THRESHOLD) / 1000
    p = 0.34 + 0.012 * centred + JUMP * (value >= THRESHOLD) + rng_rdd.gauss(0, 0.02)
    repeat = int(rng_rdd.random() < min(max(p, 0.02), 0.95))
    orders.append((oid, round(value, 2), int(value >= THRESHOLD), repeat,
                   rng_rdd.choice(['Retail', 'Hospitality', 'Wholesale']), rng_rdd.choice(list(REGIONS))))
with open(f'{a.out}/delivery_threshold.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['order_id', 'order_value', 'free_delivery', 'repeat_within_90_days', 'segment', 'region'])
    w.writerows(orders)

print(f'region_month {len(rows)} rows · qbr_program {len(prog)} customers '
      f'({sum(p[6] for p in prog)} in the program) · delivery_threshold {len(orders)} orders')
