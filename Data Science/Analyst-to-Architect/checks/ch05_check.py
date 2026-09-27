# Chapter 5 number checks. Mini database (Q1 2026) for the March issue tree; one-year database (2025) for the story.
import subprocess, datetime as dt
def q(sql, db='riverstone'):
    r = subprocess.run(['su','postgres','-c',f"psql -X -q -At -F '|' -d {db}"], input=sql, capture_output=True, text=True, cwd='/tmp')
    if r.stderr.strip(): print('ERR', r.stderr)
    return [l.split('|') for l in r.stdout.strip().splitlines()]
LINE="oi.quantity*oi.unit_price*(1-oi.discount_pct/100)"
print('billed by month', q("SELECT to_char(invoice_date,'MM'), COUNT(*), SUM(amount) FROM invoices GROUP BY 1 ORDER BY 1;"))
feb, mar, jan = 161700, 31800, 104210
print('Feb->Mar', round((mar-feb)/feb*100,1), 'Jan->Mar', round((mar-jan)/jan*100,1), 'Q1 avg month', round((jan+feb+mar)/3), 'Mar vs avg', round((mar-(jan+feb+mar)/3)/((jan+feb+mar)/3)*100,1))
print('AOV Feb', feb/5, 'Mar', mar/2, 'Jan', jan/3)
print('count effect', feb - 2*feb/5, 'size effect', 2*feb/5 - mar, 'sum', feb-mar)
print('orders placed by month with segment', q(f"SELECT to_char(o.order_date,'MM'), o.order_id, c.customer_name, c.segment, o.status, SUM({LINE}), o.sales_rep_id FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) GROUP BY 1,2,3,4,5,7 ORDER BY 2;"))
print('Feb wholesale', 32625+76560, round((32625+76560)/feb*100,1), 'Northgate share of Feb', round(76560/feb*100,1), 'Feb without Northgate', feb-76560)
print('booked Mar', 58020, 'booked change', round((58020-feb)/feb*100,1), 'Mar billed + pending', mar+26220)
# reorder gaps
print('order dates by customer', q("SELECT c.customer_name, string_agg(o.order_date::text || ':' || o.status, ', ' ORDER BY o.order_date) FROM customers c LEFT JOIN orders o USING(customer_id) GROUP BY 1 ORDER BY 1;"))
D=dt.date
print('Coastal gap', (D(2026,2,11)-D(2026,1,9)).days, 'since last', (D(2026,3,31)-D(2026,2,11)).days, 'Sharma gaps', (D(2026,2,2)-D(2026,1,5)).days, (D(2026,3,10)-D(2026,2,2)).days, 'Northgate since', (D(2026,3,31)-D(2026,2,25)).days, 'Sunrise since', (D(2026,3,31)-D(2026,2,19)).days)
print('balances at 3/31 by customer', q("SELECT c.customer_name, c.segment, SUM(i.amount-COALESCE(p.paid,0)) owed, SUM(CASE WHEN i.due_date<DATE '2026-03-31' THEN i.amount-COALESCE(p.paid,0) ELSE 0 END) overdue FROM invoices i JOIN orders o USING(order_id) JOIN customers c USING(customer_id) LEFT JOIN (SELECT invoice_id,SUM(amount) paid FROM payments GROUP BY 1) p USING(invoice_id) GROUP BY 1,2 HAVING SUM(i.amount-COALESCE(p.paid,0))>0 ORDER BY 3 DESC;"))
print('discount vs line size (mini)', q("SELECT CASE WHEN quantity*unit_price>=20000 THEN 'big' ELSE 'small' END, ROUND(AVG(discount_pct),2), COUNT(*) FROM order_items GROUP BY 1;"))
# ---- story: one-year database leads ----
L = q("""WITH u AS (SELECT * FROM (SELECT l.*, ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY created_at, lead_id) rn FROM leads l) x WHERE rn=1),
s AS (SELECT lead_id, MIN(CASE WHEN stage='Contacted' THEN entered_at END) contacted, MIN(CASE WHEN stage='Quoted' THEN entered_at END) quoted, MIN(CASE WHEN stage='Won' THEN entered_at END) won FROM lead_stage_history GROUP BY 1)
SELECT u.lead_id, u.company_name, u.source, u.created_at::date, e.employee_name, EXTRACT(EPOCH FROM contacted-created_at)/86400, quoted IS NOT NULL, won IS NOT NULL FROM u LEFT JOIN s USING(lead_id) LEFT JOIN employees e ON e.employee_id=u.owner_id ORDER BY u.created_at;""", 'riverstone_2025')
rows=[(r[0],r[1],r[2],r[3],r[4], float(r[5]) if r[5] else None, r[6]=='t', r[7]=='t') for r in L]
print('lead rows', q("SELECT COUNT(*) FROM leads;",'riverstone_2025'), 'unique', len(rows))
unc=[r for r in rows if r[5] is None]; print('never contacted', len(unc), round(len(unc)/len(rows)*100,1), [(r[1],r[2],r[3],r[4]) for r in unc])
con=[r for r in rows if r[5] is not None]
print('avg days to contact', round(sum(r[5] for r in con)/len(con),1), 'median', sorted(r[5] for r in con)[len(con)//2-1:len(con)//2+1])
fast=[r for r in con if r[5]<=7]; slow=[r for r in con if r[5]>7]
print('fast<=7', len(fast), sum(r[7] for r in fast), 'slow', len(slow), sum(r[7] for r in slow), round(sum(r[7] for r in fast)/len(fast)*100,1), round(sum(r[7] for r in slow)/len(slow)*100,1))
print('won of contacted', sum(r[7] for r in con), len(con), round(sum(r[7] for r in con)/len(con)*100,1))
for who in ('Neha Kulkarni','Rahul Mehta','Farah Khan'):
    rr=[r for r in rows if r[4]==who]; c=[r for r in rr if r[5] is not None]
    print(who, 'leads', len(rr), 'uncontacted', len(rr)-len(c), 'won', sum(r[7] for r in rr), 'avg days', round(sum(r[5] for r in c)/len(c),1))
for src in ('Website','Referral','Trade fair','Cold call','IndiaMART listing'):
    rr=[r for r in rows if r[2]==src]; print(src, len(rr), 'uncontacted', sum(1 for r in rr if r[5] is None), 'won', sum(r[7] for r in rr))
print('per month', round(30/12,1), 'per exec per month', round(30/12/3,2))
print('rep orders 2025', q("SELECT e.employee_name, COUNT(*) FROM orders o LEFT JOIN employees e ON e.employee_id=o.sales_rep_id WHERE status<>'Cancelled' GROUP BY 1 ORDER BY 2 DESC;",'riverstone_2025'))
print('days Jasmine uncontacted at 12-31', (D(2025,12,31)-D(2025,11,9)).days, 'Tulip', (D(2025,12,31)-D(2025,9,23)).days)
print('Neha website leads', sum(1 for r in rows if r[4]=='Neha Kulkarni' and r[2]=='Website'), 'Neha uncontacted website', sum(1 for r in rows if r[4]=='Neha Kulkarni' and r[2]=='Website' and r[5] is None))
print('customers', q("SELECT customer_name, city, segment, signup_date FROM customers ORDER BY 1;"))
print('contacted within 2 days', sum(1 for r in con if r[5]<=2), 'within 3', sum(1 for r in con if r[5]<=3.5))
ja=104210/3; print('ex6 Jan AOV', round(ja,2), 'change', 161700-104210, 'count effect', round(2*ja), 'size effect', round(5*(32340-ja)), 'sum', round(2*ja)+round(5*(32340-ja)))
print('Ch3 collections share', round(197250/297710*100,1))
print('Hospitality Q1 mini', q("SELECT to_char(o.order_date,'MM'), SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)) FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) WHERE c.segment='Hospitality' AND o.status<>'Cancelled' GROUP BY 1 ORDER BY 1;"))
print('fast vs slow won', '3/8', '3/14')
print('Blue Bay days since signup', (D(2026,3,31)-D(2026,3,1)).days)
print('count share of fall', round(97020/129900*100,1), 'size share', round(32880/129900*100,1), 'Feb AOV x2', 2*32340)
p=1450*0.95; print('crate 5% off margin', round((p-1100)/p*100,1), 'list', round(350/1450*100,1))
print('big lines mini detail', q("SELECT order_id, quantity*unit_price, discount_pct FROM order_items WHERE quantity*unit_price>=20000 ORDER BY 1;"))
