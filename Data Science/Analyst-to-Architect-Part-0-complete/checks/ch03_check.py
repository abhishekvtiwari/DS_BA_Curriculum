# Chapter 3 number checks: every figure quoted in the chapter is recomputed here from the mini database.
import subprocess
def q(sql):
    r = subprocess.run(['su','postgres','-c',"psql -X -q -At -F '|' -d riverstone"], input=sql, capture_output=True, text=True, cwd='/tmp')
    return [l.split('|') for l in r.stdout.strip().splitlines()]
LINE = "oi.quantity*oi.unit_price*(1-oi.discount_pct/100)"
print('bookings all statuses by month', q(f"SELECT to_char(o.order_date,'YYYY-MM'), SUM({LINE}) FROM orders o JOIN order_items oi USING(order_id) GROUP BY 1 ORDER BY 1;"))
print('bookings excl cancelled by month', q(f"SELECT to_char(o.order_date,'YYYY-MM'), SUM({LINE}) FROM orders o JOIN order_items oi USING(order_id) WHERE status<>'Cancelled' GROUP BY 1 ORDER BY 1;"))
print('billings by month', q("SELECT to_char(invoice_date,'YYYY-MM'), SUM(amount) FROM invoices GROUP BY 1 ORDER BY 1;"))
print('collections by month', q("SELECT to_char(payment_date,'YYYY-MM'), SUM(amount) FROM payments GROUP BY 1 ORDER BY 1;"))
print('totals', q(f"SELECT (SELECT SUM({LINE}) FROM orders o JOIN order_items oi USING(order_id)), (SELECT SUM(amount) FROM invoices), (SELECT SUM(amount) FROM payments);"))
inv = q("SELECT COUNT(*), SUM(amount) FROM invoices;")[0]
print('invoiced orders, amount, AOV', inv, float(inv[1])/int(inv[0]))
print('orders total, cancelled', q("SELECT COUNT(*), COUNT(*) FILTER (WHERE status='Cancelled'), COUNT(*) FILTER (WHERE status='Pending') FROM orders;"))
print('customers with non-cancelled order', q("SELECT COUNT(DISTINCT customer_id) FROM orders WHERE status<>'Cancelled';"))
print('gross margin on invoiced (Delivered+Shipped)', q(f"SELECT SUM({LINE}), SUM(oi.quantity*p.unit_cost), ROUND(100*(SUM({LINE})-SUM(oi.quantity*p.unit_cost))/SUM({LINE}),1) FROM orders o JOIN order_items oi USING(order_id) JOIN products p USING(product_id) WHERE status IN ('Delivered','Shipped');"))
print('collected pct', 197250/297710*100)
print('overdue as of 2026-03-31', q("SELECT SUM(i.amount-COALESCE(p.paid,0)) FROM invoices i LEFT JOIN (SELECT invoice_id,SUM(amount) paid FROM payments GROUP BY 1) p USING(invoice_id) WHERE i.due_date < DATE '2026-03-31';"))
print('outstanding total', q("SELECT SUM(i.amount-COALESCE(p.paid,0)) FROM invoices i LEFT JOIN (SELECT invoice_id,SUM(amount) paid FROM payments GROUP BY 1) p USING(invoice_id);"))
print('order 5001 lines', q(f"SELECT product_id, quantity, unit_price, discount_pct, {LINE} FROM order_items oi WHERE order_id=5001;"))
print('days order->invoice->payment 5001', (__import__('datetime').date(2026,1,6)-__import__('datetime').date(2026,1,5)).days, (__import__('datetime').date(2026,2,2)-__import__('datetime').date(2026,1,6)).days, (__import__('datetime').date(2026,2,2)-__import__('datetime').date(2026,1,5)).days)
# manual work estimate (illustrative assumptions stated in the chapter)
orders_per_week, minutes_each, weeks = 40, 6, 50
print('retyping hours per week', orders_per_week*minutes_each/60, 'per year', orders_per_week*minutes_each/60*weeks)
print('avg days to pay (invoice->last payment for fully paid invoices)', q("SELECT ROUND(AVG(lastpay - invoice_date),1) FROM (SELECT i.invoice_id, i.invoice_date, i.amount, MAX(p.payment_date) lastpay, SUM(p.amount) paid FROM invoices i JOIN payments p USING(invoice_id) GROUP BY 1,2,3 HAVING SUM(p.amount)=i.amount) x;"))
print('fully paid invoices', q("SELECT i.invoice_id, i.invoice_date, MAX(p.payment_date), MAX(p.payment_date)-i.invoice_date FROM invoices i JOIN payments p USING(invoice_id) GROUP BY i.invoice_id,i.invoice_date,i.amount HAVING SUM(p.amount)=i.amount ORDER BY 1;"))
print('Jan orders detail', q(f"SELECT o.order_id, c.customer_name, o.status, SUM({LINE}) FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) WHERE o.order_date < '2026-02-01' GROUP BY 1,2,3 ORDER BY 1;"))
# ---- added while writing ----
import datetime as dt
D=dt.date
print('enquiry->payment days', (D(2026,2,2)-D(2025,10,22)).days, 'enquiry->report', (D(2026,2,3)-D(2025,10,22)).days)
print('Feb orders', q(f"SELECT o.order_id, c.customer_name, o.status, SUM({LINE}) FROM orders o JOIN customers c USING(customer_id) JOIN order_items oi USING(order_id) WHERE o.order_date BETWEEN '2026-02-01' AND '2026-02-28' GROUP BY 1,2,3 ORDER BY 1;"))
print('Feb collections by invoice', q("SELECT invoice_id, payment_date, amount FROM payments WHERE payment_date BETWEEN '2026-02-01' AND '2026-02-28' ORDER BY 2;"))
print('Mar orders', q(f"SELECT o.order_id, o.status, SUM({LINE}) FROM orders o JOIN order_items oi USING(order_id) WHERE o.order_date >= '2026-03-01' GROUP BY 1,2 ORDER BY 1;"))
print('overdue by invoice', q("SELECT i.invoice_id, i.due_date, i.amount-COALESCE(p.paid,0), DATE '2026-03-31'-i.due_date FROM invoices i LEFT JOIN (SELECT invoice_id,SUM(amount) paid FROM payments GROUP BY 1) p USING(invoice_id) WHERE i.amount-COALESCE(p.paid,0)>0 ORDER BY 1;"))
print('AOV on non-cancelled orders', 323930/11, 'reconcile bookings-pending', 323930-26220, 'collections+outstanding', 197250+100460)
print('discounts by order', q("SELECT order_id, MAX(discount_pct), (SELECT sales_rep_id FROM orders o WHERE o.order_id=oi.order_id) FROM order_items oi GROUP BY order_id HAVING MAX(discount_pct)>0 ORDER BY 1;"))
for disc in (0,12,15):
    p=1450*(1-disc/100); print('crate margin at', disc, '% discount: price', p, 'margin %', round((p-1100)/p*100,1))
print('manual invoices per month hours', 25*3*22/60)
print('Q1 bookings incl cancelled minus cancelled', 335930-12000)
print('March AOV billed', 31800/2, 'March AOV booked', 58020/3)
print('5009 owed', 76560-30000, 'days overdue', (D(2026,3,31)-D(2026,3,28)).days, 'order 5009 value check 60*1450*0.88', 60*1450*0.88)
print('Feb collected share of Jan invoices', 14700+40000+10000, 'remaining Jan invoices open end Feb', 104210-64700)
