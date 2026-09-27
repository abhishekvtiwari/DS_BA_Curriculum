"""Consistency checks for the full Riverstone dataset (companion/full/).
Needs riverstone_full and riverstone_2025 loaded in PostgreSQL (user postgres) and riverstone_full in MySQL (root).
Run from the book root:  python3 checks/full_dataset_checks.py"""
import subprocess, sys
def pg(sql, db="riverstone_full"):
    r = subprocess.run(["su", "postgres", "-c", f"psql -X -tA -F '|' -d {db}"], input=sql, capture_output=True, text=True, cwd="/tmp")
    if r.stderr.strip(): print("PG ERROR", r.stderr); sys.exit(1)
    return r.stdout.strip()
def my(sql, db="riverstone_full"):
    r = subprocess.run(["mysql", "-uroot", "-N", "-B", db], input=sql, capture_output=True, text=True)
    if r.stderr.strip(): print("MYSQL ERROR", r.stderr); sys.exit(1)
    return r.stdout.strip().replace("\t", "|")
ok = True
def check(name, cond, detail=""):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))

# 1. the named customers' 2025 data is identical to the one-year database
q_orders = "SELECT order_id, customer_id, order_date, status, COALESCE(sales_rep_id,0) FROM orders WHERE customer_id <= 24 AND order_date >= '2025-01-01' ORDER BY order_id;"
q_items = ("SELECT oi.order_item_id, oi.order_id, oi.product_id, oi.quantity, oi.unit_price, oi.discount_pct FROM order_items oi "
           "JOIN orders o ON o.order_id = oi.order_id WHERE o.customer_id <= 24 AND o.order_date >= '2025-01-01' ORDER BY 1;")
check("named 2025 orders identical to riverstone_2025", pg(q_orders) == pg(q_orders, "riverstone_2025"))
check("named 2025 order lines identical to riverstone_2025", pg(q_items) == pg(q_items, "riverstone_2025"))
for t in ["customers", "products", "employees", "leads", "lead_stage_history"]:
    key = {"customers": "customer_id <= 24", "employees": "employee_id <= 5"}.get(t, "TRUE")
    q = f"SELECT * FROM {t} WHERE {key} ORDER BY 1,2;"
    check(f"{t}: one-year rows unchanged", pg(q) == pg(q, "riverstone_2025"))
named_rev = "SELECT ROUND(SUM(net_revenue),2) FROM sales_lines WHERE customer_id <= 24 AND order_date BETWEEN '2025-01-01' AND '2025-12-31';"
check("named customers 2025 net revenue = 4,335,471", pg(named_rev) == "4335471.00", pg(named_rev))

# 2. integrity (PostgreSQL enforces keys; MySQL was loaded with FOREIGN_KEY_CHECKS = 0, so check there)
orphans = ("SELECT (SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON c.customer_id=o.customer_id WHERE c.customer_id IS NULL)"
           " + (SELECT COUNT(*) FROM order_items i LEFT JOIN orders o ON o.order_id=i.order_id WHERE o.order_id IS NULL)"
           " + (SELECT COUNT(*) FROM order_items i LEFT JOIN products p ON p.product_id=i.product_id WHERE p.product_id IS NULL)"
           " + (SELECT COUNT(*) FROM orders o LEFT JOIN employees e ON e.employee_id=o.sales_rep_id WHERE o.sales_rep_id IS NOT NULL AND e.employee_id IS NULL);")
check("MySQL: no orphan keys", my(orphans) == "0", my(orphans))
check("every order has at least one line", pg("SELECT COUNT(*) FROM orders o WHERE NOT EXISTS (SELECT 1 FROM order_items i WHERE i.order_id=o.order_id);") == "0")
check("order dates within 2023-2025", pg("SELECT COUNT(*) FROM orders WHERE order_date < '2023-01-01' OR order_date > '2025-12-31';") == "0")
check("orders on or after signup", pg("SELECT COUNT(*) FROM orders o JOIN customers c USING (customer_id) WHERE o.order_date < c.signup_date;") == "0")

# 3. PostgreSQL and MySQL agree
agg = ("SELECT EXTRACT(YEAR FROM order_date) AS y, COUNT(*), COUNT(DISTINCT order_id), ROUND(SUM(net_revenue),2), ROUND(SUM(product_cost),2) "
       "FROM sales_lines GROUP BY EXTRACT(YEAR FROM order_date) ORDER BY 1;")
a_pg = pg(agg); a_my = my(agg)
check("PostgreSQL and MySQL yearly aggregates match", a_pg.replace(".0|", "|") == a_my.replace(".0|", "|") or a_pg.split() == a_my.split(), f"\nPG:\n{a_pg}\nMY:\n{a_my}")

# 4. key numbers for DATA_SPEC.md
print("\n-- key numbers")
for label, q in [
    ("rows customers/products/employees/orders/order_items/targets",
     "SELECT (SELECT COUNT(*) FROM customers),(SELECT COUNT(*) FROM products),(SELECT COUNT(*) FROM employees),(SELECT COUNT(*) FROM orders),(SELECT COUNT(*) FROM order_items),(SELECT COUNT(*) FROM sales_targets);"),
    ("orders by status", "SELECT status, COUNT(*) FROM orders GROUP BY status ORDER BY 2 DESC;"),
    ("yearly: lines|orders|net revenue|gross margin %", "SELECT EXTRACT(YEAR FROM order_date), COUNT(*), COUNT(DISTINCT order_id), ROUND(SUM(net_revenue)), ROUND(100*(1-SUM(product_cost)/SUM(net_revenue)),1) FROM sales_lines GROUP BY 1 ORDER BY 1;"),
    ("yearly targets and attainment %", "SELECT EXTRACT(YEAR FROM t.target_month), SUM(t.target_revenue), ROUND(100*SUM(a.rev)/SUM(t.target_revenue),1) FROM sales_targets t JOIN (SELECT DATE_TRUNC('month',order_date)::date m, SUM(net_revenue) rev FROM sales_lines GROUP BY 1) a ON a.m=t.target_month GROUP BY 1 ORDER BY 1;"),
    ("2025 revenue share by segment %", "SELECT c.segment, ROUND(100*SUM(s.net_revenue)/(SELECT SUM(net_revenue) FROM sales_lines WHERE order_date>='2025-01-01'),1) FROM sales_lines s JOIN customers c USING (customer_id) WHERE s.order_date>='2025-01-01' GROUP BY 1 ORDER BY 2 DESC;"),
    ("active customers by year", "SELECT EXTRACT(YEAR FROM order_date), COUNT(DISTINCT customer_id) FROM sales_lines GROUP BY 1 ORDER BY 1;"),
    ("customers by segment", "SELECT segment, COUNT(*) FROM customers GROUP BY 1 ORDER BY 2 DESC;"),
    ("orders without sales rep / customers without city / duplicate-customer rows / stale pending (<2025-06)",
     "SELECT (SELECT COUNT(*) FROM orders WHERE sales_rep_id IS NULL),(SELECT COUNT(*) FROM customers WHERE city IS NULL),(SELECT COUNT(*) FROM customers WHERE customer_id > 4979),(SELECT COUNT(*) FROM orders WHERE status='Pending' AND order_date < '2025-06-01');"),
    ("customers with no orders", "SELECT COUNT(*) FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id);"),
    ("list price of product 101 by year", "SELECT EXTRACT(YEAR FROM o.order_date), MIN(i.unit_price), MAX(i.unit_price) FROM order_items i JOIN orders o USING (order_id) WHERE i.product_id=101 GROUP BY 1 ORDER BY 1;"),
    ("order_id ranges", "SELECT MIN(order_id), MAX(order_id), COUNT(*) FILTER (WHERE order_id < 200000) FROM orders;"),
]:
    print(label); print(pg(q))
print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED"); sys.exit(0 if ok else 1)
