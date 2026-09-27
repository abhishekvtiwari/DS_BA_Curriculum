# Analyst to Architect - Chapter 7 number checks. Run as root with PostgreSQL loaded (tools/setup_databases.sh).
# Riverstone Supplies is fictional; every name and number is invented.
import subprocess, datetime as dt
def q(sql):
    r=subprocess.run(['su','postgres','-c','psql -X -q -At -F"|" -d riverstone_2025'],input=sql,capture_output=True,text=True,cwd='/tmp')
    return [l.split('|') for l in r.stdout.strip().splitlines()]
ok=True
def check(label,got,exp):
    global ok
    good = got==exp
    ok &= good
    print(('OK  ' if good else 'FAIL'),label,got,'' if good else f'(expected {exp})')
check('customers in riverstone_2025', q("SELECT COUNT(*) FROM customers")[0][0], '24')
rows=q("""SELECT c.customer_name, MAX(o.order_date), DATE '2025-12-31'-MAX(o.order_date)
FROM customers c LEFT JOIN orders o ON c.customer_id=o.customer_id AND o.status<>'Cancelled'
GROUP BY c.customer_id,c.customer_name HAVING MAX(o.order_date)<DATE '2025-11-01' OR MAX(o.order_date) IS NULL ORDER BY 2 NULLS FIRST""")
check('quiet customers (60-day rule)', len(rows), 5)
check('90-day rule count (Ex 11)', sum(1 for r in rows if r[2]=='' or int(r[2])>90), 4)
rev=dict((r[0],(r[1],r[2])) for r in q("""SELECT c.customer_name, COUNT(DISTINCT s.order_id), ROUND(SUM(s.net_revenue),2)
FROM customers c LEFT JOIN sales_lines s USING(customer_id) GROUP BY 1"""))
check('Sunrise orders/revenue', rev['Sunrise Caterers'], ('4','47673.75'))
check('Om Sai orders/revenue', rev['Om Sai Provisions'], ('4','66398.75'))
check('City Needs Store orders/revenue', rev['City Needs Store'], ('2','55650.00'))
check('Tasty Tiffins orders/revenue', rev['Tasty Tiffins'], ('2','44850.00'))
total=float(q("SELECT SUM(net_revenue) FROM sales_lines")[0][0])
check('total 2025 net revenue', round(total), 4335471)
both=47673.75+66398.75
check('Sunrise+Om Sai', both, 114072.5)
check('share of year revenue %', round(100*both/total,1), 2.6)
check('Tasty Tiffins days (Ex 5)', (dt.date(2025,12,31)-dt.date(2025,10,26)).days, 66)
check('Home Plus signup', q("SELECT signup_date FROM customers WHERE customer_name='Home Plus'")[0][0], '2025-06-18')
check('Friday-flash hours: 40 min x 250 days', round(40*250/60), 167)
check('Ex 7 hours: 25 min x 250 days', round(25*250/60,1), 104.2)
check('Ex 7 working weeks at 40 h', round(25*250/60/40,1), 2.6)
print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
