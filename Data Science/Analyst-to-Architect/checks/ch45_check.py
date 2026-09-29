# Analyst to Architect - Chapter 45 checks (exercise answers and prose numbers).
# Run from the book root with PostgreSQL running:  PYTHONPATH=companion/ch45 python3 checks/ch45_check.py
# Riverstone Supplies is fictional; every name and number is invented.
import os, sys, datetime as dt
os.chdir('companion/ch45'); sys.path.insert(0, '.')
import psycopg2, duckdb, hashlib
from reset_ch45 import reset
from apply_day import apply_day
ok=True
def check(label,got,exp):
    global ok; good=(got==exp); ok&=good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
reset()
SRC=os.environ.get("RIVERSTONE_SOURCE","dbname=riverstone_source"); wh=duckdb.connect('warehouse/check.duckdb')
def q(sql):
    c=psycopg2.connect(SRC)
    with c, c.cursor() as cur: cur.execute(sql); r=cur.fetchall()
    c.close(); return r
wh.execute("CREATE OR REPLACE TABLE o (order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date DATE, status VARCHAR, sales_rep_id INTEGER)")
wh.executemany("INSERT INTO o VALUES (?,?,?,?,?)", q("SELECT order_id, customer_id, order_date, status, sales_rep_id FROM orders"))
check('full load rows',wh.execute("SELECT COUNT(*) FROM o").fetchone()[0],175)
apply_day(1); apply_day(2)
H="SELECT order_id, md5(concat_ws('|', order_id, customer_id, order_date, status, coalesce(sales_rep_id::text, '∅'))) FROM orders"
s=dict(q(H)); w=dict(wh.execute("SELECT order_id, md5(concat_ws('|', order_id, customer_id, strftime(order_date,'%Y-%m-%d'), status, coalesce(sales_rep_id::text, '∅'))) FROM o").fetchall())
check('Ex5 inserted',sorted(set(s)-set(w)),[10176,10177,10178])
check('Ex5 changed',sorted(k for k in set(s)&set(w) if s[k]!=w[k]),[10174,10175])
check('Ex5 deleted',sorted(set(w)-set(s)),[])
check('Ex7 date',dt.datetime.strptime('13-01-2026','%d-%m-%Y').date().isoformat(),'2026-01-13')
check('Ex7 qty',int('3,150'.replace(',','')),3150)
try: dt.datetime.strptime('13-01-2026','%m-%d-%Y'); r='parsed'
except ValueError: r='error'
check('Ex7 wrong format fails',r,'error')
check('Ex8 total units',100+1200+85+2040,3425)
check('Ex9 backoff waits between 4 attempts',[2**(a-1) for a in range(1,4)],[1,2,4])
a=hashlib.sha256(b'Pay Rs 14,700 to Riverstone Supplies').hexdigest(); b=hashlib.sha256(b'Pay Rs 14,700 to Riverstone Supplies ').hexdigest()
check('45.5 sha256 14,700',a,'f4251ff3fb7191f7e79677f3b1871db06c0935c3cc08164496995f1f909f6f71')
check('Ex4 trailing-space matches',sum(x==y for x,y in zip(a,b)),2)
check('Ex4 trailing-space hash',b,'71e96ba2039f8e4139716f2287b78cfe1e12842a28e6f3dfab748321bbcaa77a')
check('45.5 concat_ws skips NULL',wh.execute("SELECT concat_ws('|',1,NULL,3)").fetchone()[0],'1|3')
check('Story: full ERP orders a month (about 4,000)',round(48312/12),4026)
check('leads pages 20/20/3',20+20+3,q("SELECT COUNT(*) FROM leads")[0][0])
wh.close(); os.remove('warehouse/check.duckdb')
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
