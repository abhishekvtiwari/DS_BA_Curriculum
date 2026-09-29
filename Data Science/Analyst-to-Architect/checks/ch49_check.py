# Analyst to Architect - Chapter 49 checks. Run from the book root: PYTHONPATH=companion/ch49 python3 checks/ch49_check.py
# Needs the Chapter 48 sensor data. Riverstone Supplies is fictional; every name and number is invented.
import os, sys
os.chdir('companion/ch49'); sys.path.insert(0, '.')
from setup_ch49 import build
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
rows = build()
size = lambda f: round(os.path.getsize(os.path.join('storage', f)) / 1e6, 1)
check('one day rows', rows, 216000)
check('csv MB', size('day.csv'), 14.6)
check('parquet MB', size('day.parquet'), 1.3)
check('sqlite MB', size('day.sqlite'), 16.3)
check('Ex2 csv/parquet ratio', round(size('day.csv')/size('day.parquet'),1), 11.2)
check('Ex2 sqlite/parquet ratio', round(size('day.sqlite')/size('day.parquet'),1), 12.5)
# cost arithmetic from 49.8 and exercises 9-10 (prices: S3 Standard $0.023/GB-month, BigQuery $6.25/TiB, checked 29 Sep 2026)
b = 1.3e6 / 216_000
check('bytes per reading', round(b, 1), 6.0)
check('today readings a year', 25 * 8_640 * 365, 78_840_000)
check('today GB a year', round(25 * 8_640 * 365 * b / 1e9, 2), 0.47)
check('rollout readings a day', 1_460 * 86_400, 126_144_000)
year_gb = 1_460 * 86_400 * 365 * b / 1e9
check('rollout GB a year', round(year_gb), 277)
check('storage USD per month', round(year_gb * 0.023, 2), 6.37)
check('storage INR per month (83/USD)', round(year_gb * 0.023 * 83, -1), 530)
check('week GB', round(year_gb / 52, 1), 5.3)
full = year_gb / 1_099.5 * 6.25; week = year_gb / 52 / 1_099.5 * 6.25
check('full scan USD per run', round(full, 2), 1.58)
check('week scan USD per run', round(week, 3), 0.030)
check('ratio', round(full / week), 52)
check('Ex9 full scan per month', round(full * 30, 2), 47.26)
check('Ex9 week scan per month', round(week * 30, 2), 0.91)
check('Ex10 MB a day at 40 machines', round(40 * 8_640 * b / 1e6, 1), 2.1)
check('Ex10 MB a month', round(40 * 8_640 * 30 * b / 1e6), 62)
check('Ex10 GB five years', round(40 * 8_640 * 365 * 5 * b / 1e9, 1), 3.8)
check('Ex10 machine partitions five years', 40 * 12 * 5, 2_400)
check('story days', 11 + 8 + 23, 42)
check('M-07 day rows', 86_400 // 10, 8_640)
check('hourly batch rows', 25 * 360, 9_000)
check('temperature code bits', (4729 - 1).bit_length(), 13)
check('13-bit codes KB', round(122_880 * 13 / 8 / 1e3), 200)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
