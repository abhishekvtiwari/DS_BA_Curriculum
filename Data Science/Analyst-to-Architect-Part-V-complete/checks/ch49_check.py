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
# cost arithmetic from 49.8 and exercise 9
year_gb = round(126_000_000 * 365 / 216_000 * 1.3 / 1000)
check('archive GB per year', year_gb, 277)
check('storage USD per month', round(277*0.023,2), 6.37)
check('week scanned GB', round(277/52,1), 5.3)
check('full scan USD per run', round(0.277*5,3), 1.385)
check('week scan USD per run', round(0.0053*5,4), 0.0265)
check('Ex9 full scan per month', round(0.277*5*30,2), 41.55)
check('Ex9 ratio', round(277/5.3), 52)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
