# Analyst to Architect - Chapter 47 checks (prose numbers and exercise answers).
# Run from the book root with PostgreSQL running:  PYTHONPATH=companion/ch47 python3 checks/ch47_check.py
# Riverstone Supplies is fictional; every name and number is invented.
import os, sys
from datetime import datetime
os.chdir('companion/ch47'); sys.path.insert(0, '.')
import duckdb
from reset_ch47 import reset
from apply_day import apply_day
import ingest
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
reset(); wh=duckdb.connect('warehouse/check47.duckdb')
apply_day(1)
for t in ["orders","order_items"]: ingest.sync_table(wh,t)
ingest.load_dispatch(wh,"2026-01-02")
check('rows loaded', wh.execute("SELECT (SELECT COUNT(*) FROM raw.orders), (SELECT COUNT(*) FROM raw.order_items), (SELECT COUNT(*) FROM raw.dispatch)").fetchone(), (177,333,5))
daily = wh.execute("""SELECT o.order_date, SUM(i.quantity*i.unit_price*(1-i.discount_pct/100)) rev
    FROM raw.orders o JOIN raw.order_items i ON i.order_id=o.order_id
    WHERE o.status <> 'Cancelled' AND o.order_date BETWEEN DATE '2025-01-01' AND DATE '2025-12-31'
    GROUP BY 1""").fetchall()
revs=sorted(r[1] for r in daily)
median=revs[len(revs)//2]
check('days with orders in 2025', len(daily), 131)
check('median daily revenue', float(median), 27442.50)
check('days above 3x median', sum(1 for r in revs if r > 3*median), 10)
check('largest day', float(max(revs)), 175895.00)
check('quarter of median (Ex 9)', int(float(median)/4), 6860)
check('five times median (Ex 9)', int(float(median)*5), 137212)
# freshness arithmetic from 47.5 (NOW = 2026-01-06 06:30)
now=datetime(2026,1,6,6,30)
check('orders age hours', round((now-datetime(2026,1,5)).total_seconds()/3600,1), 30.5)
check('dispatch age hours', round((now-datetime(2026,1,2)).total_seconds()/3600,1), 102.5)
check('Flash 2 Jan revenue', float(wh.execute("""SELECT SUM(i.quantity*i.unit_price*(1-i.discount_pct/100))
    FROM raw.orders o JOIN raw.order_items i ON i.order_id=o.order_id
    WHERE o.order_date=DATE '2026-01-02' AND o.status<>'Cancelled'""").fetchone()[0]), 38710.00)
# freshness by working day (47.5, Answer 8)
from datetime import date
check('2 Jan 2026 is a Friday', date(2026,1,2).strftime('%A'), 'Friday')
check('Monday run age of Friday data', round((datetime(2026,1,5,6,30)-datetime(2026,1,2)).total_seconds()/3600,1), 78.5)
check('16 and 9 Nov 2025 are Sundays, 13 Sep a Saturday', [date(2025,11,16).strftime('%a'), date(2025,11,9).strftime('%a'), date(2025,9,13).strftime('%a')], ['Sun','Sun','Sat'])
check('8 Jan 2026 is a Thursday, four days after 4 Jan', (date(2026,1,8).strftime('%A'), (date(2026,1,8)-date(2026,1,4)).days), ('Thursday', 4))
check('fractional-paisa example (47.4)', 3*1234.50*(1-7.5/100), 3425.7375)
check('every 2025 order has lines (47.24: no date filter needed)', wh.execute("""SELECT COUNT(*) FROM raw.orders o
    WHERE NOT EXISTS (SELECT 1 FROM raw.order_items i WHERE i.order_id=o.order_id)""").fetchone()[0], 0)
wh.close(); os.remove('warehouse/check47.duckdb')
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
