# Analyst to Architect - Chapter 45 checks (exercise answers and prose numbers).
# Run from the book root with PostgreSQL running:  PYTHONPATH=companion/ch45 python3 checks/ch45_check.py
# Riverstone Supplies is fictional; every name and number is invented.
import os, sys, datetime as dt
os.chdir('companion/ch45'); sys.path.insert(0, '.')
import psycopg2, duckdb
from reset_ch45 import reset
from apply_day import apply_day
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
reset()
SRC="dbname=riverstone_source"; wh=duckdb.connect('warehouse/check.duckdb')
def q(sql):
    c=psycopg2.connect(SRC)
    with c, c.cursor() as cur: cur.execute(sql); r=cur.fetchall()
    c.close(); return r
wh.execute("CREATE OR REPLACE TABLE o (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date DATE, status VARCHAR, sales_rep_id INTEGER)")
wh.executemany("INSERT INTO o VALUES (?,?,?,?,?)", q("SELECT order_id, customer_id, order_date, status, sales_rep_id FROM orders"))
check('full load rows',wh.execute("SELECT COUNT(*) FROM o").fetchone()[0],175)
apply_day(1); apply_day(2)
H="SELECT order_id, md5(concat_ws('|', order_id, customer_id, order_date, status, sales_rep_id)) FROM orders"
s=dict(q(H)); w=dict(wh.execute("SELECT order_id, md5(concat_ws('|', order_id, customer_id, strftime(order_date,'%Y-%m-%d'), status, sales_rep_id)) FROM o").fetchall())
check('Ex4 inserted',sorted(set(s)-set(w)),[10176,10177,10178])
check('Ex4 changed',sorted(k for k in set(s)&set(w) if s[k]!=w[k]),[10174,10175])
check('Ex4 deleted',sorted(set(w)-set(s)),[])
check('Ex6 date',dt.datetime.strptime('13-01-2026','%d-%m-%Y').date().isoformat(),'2026-01-13')
check('Ex6 qty',int('3,150'.replace(',','')),3150)
try: dt.datetime.strptime('13-01-2026','%m-%d-%Y'); r='parsed'
except ValueError: r='error'
check('Ex6 wrong format fails',r,'error')
check('Ex7 total units',100+1200+85+2040,3425)
check('Ex8 backoff waits',[2**(a-1) for a in range(1,6)],[1,2,4,8,16])
check('leads pages 20/20/3',20+20+3,q("SELECT COUNT(*) FROM leads")[0][0])
wh.close(); os.remove('warehouse/check.duckdb')
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
