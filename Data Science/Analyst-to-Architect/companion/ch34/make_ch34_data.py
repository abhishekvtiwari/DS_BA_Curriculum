#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 34 · The Command Line, Linux & Networking Basics
File: make_ch34_data.py - builds the practice folder used throughout the chapter.
What: reads sales_lines_2025.csv (one row per non-cancelled order line of 2025, exported from riverstone_2025)
      and writes, under practice/:
        exports/orders_YYYY-MM-DD.csv   one file per day of November and December 2025 (header only on quiet days)
        reference/customers.csv, reference/products.csv
        logs/report.log                 the daily summary job's log for Nov-Dec 2025
        incoming/, archive/             empty folders for the chapter's project
How:  python3 make_ch34_data.py [--out practice]     (standard library only; no database needed)
Everything is deterministic: the same input file always produces the same practice folder.
Tested on: Python 3.12.3 (Ubuntu 24.04).
Riverstone Supplies is fictional; every name and number is invented.
"""
import argparse, csv, os, pathlib, re, shutil
from datetime import datetime
from collections import defaultdict
from datetime import date, timedelta

ap = argparse.ArgumentParser()
ap.add_argument('--out', default='practice')
ap.add_argument('--source', default='sales_lines_2025.csv')
a = ap.parse_args()
out = pathlib.Path(a.out)
if out.exists():
    shutil.rmtree(out)
for folder in ('exports', 'reference', 'logs', 'incoming', 'archive'):
    (out / folder).mkdir(parents=True)

rows = list(csv.DictReader(open(a.source, newline='', encoding='utf-8')))
fields = list(rows[0].keys())
by_day = defaultdict(list)
for row in rows:
    by_day[row['order_date']].append(row)

day = date(2025, 11, 1)
while day <= date(2025, 12, 31):
    with open(out / 'exports' / f'orders_{day}.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')   # Unix line endings
        writer.writeheader()
        writer.writerows(by_day.get(str(day), []))
    day += timedelta(days=1)

customers = {(r['customer_id'], r['customer_name'], r['city'], r['segment']) for r in rows}
with open(out / 'reference' / 'customers.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n'); w.writerow(['customer_id', 'customer_name', 'city', 'segment'])
    w.writerows(sorted(customers, key=lambda c: int(c[0])))
products = {(r['product_id'], r['product_name'], r['category']) for r in rows}
with open(out / 'reference' / 'products.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n'); w.writerow(['product_id', 'product_name', 'category'])
    w.writerows(sorted(products, key=lambda p: int(p[0])))

# The daily summary job's log: one run each morning at 07:00. A day with no orders is a WARNING (the job ran
# and correctly wrote an empty summary); a slow database is a WARNING; only a real failure is an ERROR.
FAILED = {date(2025, 11, 9): 'database connection refused'}
SLOW = {date(2025, 11, 18), date(2025, 12, 2), date(2025, 12, 16), date(2025, 12, 17)}
with open(out / 'logs' / 'report.log', 'w', encoding='utf-8') as f:
    day = date(2025, 11, 1)
    while day <= date(2025, 12, 31):
        lines = len(by_day.get(str(day), []))
        stamp = f'{day} 07:00:0'
        f.write(f'{stamp}1 INFO daily_summary: starting for {day}\n')
        if day in SLOW:
            f.write(f'{stamp}3 WARNING daily_summary: database slow to answer; retrying in 2 s\n')
        if day in FAILED:
            f.write(f'{stamp}4 ERROR daily_summary: {FAILED[day]}\n')
            f.write(f'{stamp}4 INFO daily_summary: exit code 1\n')
        else:
            if lines == 0:
                f.write(f'{stamp}4 WARNING daily_summary: no sales lines for {day}; wrote an empty summary\n')
            else:
                f.write(f'{stamp}4 INFO daily_summary: read {lines} sales lines for {day}\n')
            f.write(f'{stamp}5 INFO daily_summary: wrote summaries/summary_{day}.txt\n')
        day += timedelta(days=1)
# Give every file a fixed timestamp and the usual data-file permissions, so listings look the same on every machine.
STAMP = datetime(2026, 1, 5, 7, 0).timestamp()
for path in sorted(out.rglob('*')):
    if path.is_file():
        day = re.search(r'orders_(\d{4}-\d{2}-\d{2})', path.name)
        when = datetime.fromisoformat(f'{day.group(1)} 07:05') .timestamp() if day else STAMP
        os.utime(path, (when, when))
        path.chmod(0o644)          # data files: owner reads and writes, everyone else reads (section 34.5)

print(f'practice folder ready: {len(rows)} order lines, {len(customers)} customers, '
      f'{len(list((out / "exports").glob("*.csv")))} daily export files')
