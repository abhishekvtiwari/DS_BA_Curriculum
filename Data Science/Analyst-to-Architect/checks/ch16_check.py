#!/usr/bin/env python3
"""ch16_check.py - recompute every number Chapter 16 prints for a DAX measure or a Power BI visual.

Power BI can't run here, so each measure is recomputed with SQL on riverstone_full (PostgreSQL),
following the DAX semantics described in the chapter, and the CSV route (Power Query merges) is
replayed with duckdb on companion/full/*.csv. Run:  python3 checks/ch16_check.py
"""
import subprocess, pathlib, duckdb

BOOK = pathlib.Path(__file__).resolve().parents[1]

def q(sql):
    r = subprocess.run(['su', 'postgres', '-c', 'psql -X -q -At -F"|" -d riverstone_full'],
                       input=sql, capture_output=True, text=True, cwd='/tmp')
    if r.stderr.strip():
        raise SystemExit(r.stderr)
    return [l.split('|') for l in r.stdout.strip().splitlines()]

def show(title, sql):
    print(f'\n## {title}')
    for row in q(sql):
        print('  ' + ' | '.join(row))

REGION = "(SELECT * FROM (VALUES " + ",".join(
    f"('{c}','{r}')" for c, r in (l.split(',') for l in
    (BOOK / 'companion/ch16/city_region.csv').read_text().split()[1:])) + ") AS r(city, region))"
Y25 = "order_date BETWEEN '2025-01-01' AND '2025-12-31'"

show('16.0 first report: customers by segment', "SELECT segment, COUNT(customer_id) FROM customers GROUP BY 1 ORDER BY 1; SELECT COUNT(*) FROM customers;")
show('16.2 Sales rows (sales_lines): all years, 2025', f"SELECT COUNT(*), COUNT(*) FILTER (WHERE {Y25}), COUNT(DISTINCT order_id) FILTER (WHERE {Y25}) FROM sales_lines;")
show('16.2 raw order_items rows, orders rows', "SELECT (SELECT COUNT(*) FROM order_items), (SELECT COUNT(*) FROM orders);")
show('16.2 Customer.Region counts (all customers, after merge)', f"SELECT COALESCE(r.region,'City missing'), COUNT(*) FROM customers c LEFT JOIN {REGION} r ON r.city=c.city GROUP BY 1 ORDER BY 2 DESC;")
show('16.3 date table rows', "SELECT COUNT(*) FROM generate_series('2023-01-01'::date,'2025-12-31','1 day');")
show('16.4 base measures 2025: revenue, cost, margin, GM%, lines, orders, customers, AOV',
     f"SELECT ROUND(SUM(net_revenue)), ROUND(SUM(product_cost)), ROUND(SUM(net_revenue)-SUM(product_cost)), ROUND(100*(1-SUM(product_cost)/SUM(net_revenue)),1), COUNT(*), COUNT(DISTINCT order_id), COUNT(DISTINCT customer_id), ROUND(SUM(net_revenue)/COUNT(DISTINCT order_id),2) FROM sales_lines WHERE {Y25};")
show('16.4 all years revenue', "SELECT ROUND(SUM(net_revenue)) FROM sales_lines;")
show('16.5 segment matrix 2025 (Net Revenue); Retail Revenue replaces -> Retail total on every row', f"SELECT c.segment, ROUND(SUM(net_revenue)) FROM sales_lines s JOIN customers c USING (customer_id) WHERE {Y25} GROUP BY 1 ORDER BY 1;")
show('16.5 Share of Segment: top customer of 2025 vs its segment', f"""WITH t AS (SELECT c.customer_name, c.segment, SUM(net_revenue) rev FROM sales_lines s JOIN customers c USING (customer_id) WHERE {Y25} GROUP BY 1,2)
SELECT customer_name, segment, ROUND(rev,2), ROUND(100*rev/SUM(rev) OVER (PARTITION BY segment),2) FROM t ORDER BY rev DESC LIMIT 3;""")
show('16.5 ALLSELECTED: product share within West, 2025', f"""WITH t AS (SELECT p.product_name, SUM(net_revenue) rev FROM sales_lines s JOIN customers c USING (customer_id) JOIN {REGION} r ON r.city=c.city JOIN products p USING (product_id) WHERE {Y25} AND r.region='West' GROUP BY 1)
SELECT product_name, ROUND(rev), ROUND(100*rev/SUM(rev) OVER (),1) FROM t ORDER BY rev DESC LIMIT 3;""")
show('16.5 Avg Customer Revenue 2025 (AVERAGEX over customers, blanks skipped)', f"SELECT ROUND(AVG(rev),2) FROM (SELECT customer_id, SUM(net_revenue) rev FROM sales_lines WHERE {Y25} GROUP BY 1) t;")
show('16.5 Product Share % 2025', f"SELECT p.product_name, ROUND(SUM(net_revenue)), ROUND(100*SUM(net_revenue)/SUM(SUM(net_revenue)) OVER (),1) FROM sales_lines s JOIN products p USING (product_id) WHERE {Y25} GROUP BY 1 ORDER BY 2 DESC LIMIT 4;")
show('16.6 month matrix Jan-Jun 2025: rev, YTD, LY, YTD LY, YoY %, 3M rolling, target, % target', """
WITH m AS (SELECT date_trunc('month',order_date)::date mo, SUM(net_revenue) rev FROM sales_lines GROUP BY 1),
x AS (SELECT mo, rev,
  SUM(rev) OVER (PARTITION BY extract(year from mo) ORDER BY mo) ytd,
  LAG(rev,12) OVER (ORDER BY mo) ly,
  SUM(rev) OVER (ORDER BY mo ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) r3 FROM m),
y AS (SELECT *, LAG(ytd,12) OVER (ORDER BY mo) ytdly FROM x)
SELECT to_char(mo,'Mon YYYY'), ROUND(rev), ROUND(ytd), ROUND(ly), ROUND(ytdly), ROUND(100*(rev/ly-1),1), ROUND(r3), t.target_revenue, ROUND(100*rev/t.target_revenue,1)
FROM y JOIN sales_targets t ON t.target_month=y.mo WHERE mo BETWEEN '2025-01-01' AND '2025-06-01' ORDER BY mo;""")
show('16.6 year 2025: target, % of target, gap, LY, YoY', f"SELECT (SELECT SUM(target_revenue) FROM sales_targets WHERE target_month BETWEEN '2025-01-01' AND '2025-12-01'), ROUND(100*SUM(net_revenue) FILTER (WHERE {Y25})/(SELECT SUM(target_revenue) FROM sales_targets WHERE target_month BETWEEN '2025-01-01' AND '2025-12-01'),1), ROUND(SUM(net_revenue) FILTER (WHERE {Y25}) - (SELECT SUM(target_revenue) FROM sales_targets WHERE target_month BETWEEN '2025-01-01' AND '2025-12-01')), ROUND(SUM(net_revenue) FILTER (WHERE order_date < '2025-01-01' AND order_date >= '2024-01-01')), ROUND(100*(SUM(net_revenue) FILTER (WHERE {Y25})/SUM(net_revenue) FILTER (WHERE order_date < '2025-01-01' AND order_date >= '2024-01-01')-1),1) FROM sales_lines;")
show('16.6 YoY Change 2023 (LY blank) vs 2025', "SELECT extract(year from order_date), ROUND(SUM(net_revenue)) FROM sales_lines GROUP BY 1 ORDER BY 1;")
show('16.8 title: all years revenue in crore and % of all targets', "SELECT ROUND(SUM(net_revenue)/1e7,1), ROUND(100*SUM(net_revenue)/(SELECT SUM(target_revenue) FROM sales_targets),1) FROM sales_lines;")
show('16.8 title 2025 in crore', f"SELECT ROUND(SUM(net_revenue)/1e7,1) FROM sales_lines WHERE {Y25};")
show('16.8 region bar 2025 (label City missing)', f"SELECT COALESCE(r.region,'City missing'), ROUND(SUM(net_revenue)), COUNT(DISTINCT s.customer_id) FROM sales_lines s JOIN customers c USING (customer_id) LEFT JOIN {REGION} r ON r.city=c.city WHERE {Y25} GROUP BY 1 ORDER BY 2 DESC;")
show('16.10 RLS: West+East, South, North, All regions', f"SELECT r.region IN ('West','East'), r.region, ROUND(SUM(net_revenue)), COUNT(DISTINCT s.customer_id) FROM sales_lines s JOIN customers c USING (customer_id) LEFT JOIN {REGION} r ON r.city=c.city WHERE {Y25} GROUP BY ROLLUP(1,2) ORDER BY 1,2;")
show('16.10 West+East customers', f"SELECT ROUND(SUM(net_revenue)), COUNT(DISTINCT s.customer_id) FROM sales_lines s JOIN customers c USING (customer_id) JOIN {REGION} r ON r.city=c.city WHERE {Y25} AND r.region IN ('West','East');")
show('16.11 last order date in Sales', "SELECT MAX(order_date) FROM sales_lines;")
show('16.11 cancelled 2025', f"SELECT COUNT(DISTINCT o.order_id), ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100))) FROM orders o JOIN order_items oi USING (order_id) WHERE o.status='Cancelled' AND o.{Y25};")
show('Ans 13 no rep 2025', f"SELECT ROUND(SUM(net_revenue)), COUNT(*), ROUND(100*SUM(net_revenue)/(SELECT SUM(net_revenue) FROM sales_lines WHERE {Y25}),1) FROM sales_lines WHERE sales_rep_id IS NULL AND {Y25};")
show('Ans 22 top customer 2025', f"SELECT c.customer_name, ROUND(SUM(net_revenue),2) FROM sales_lines s JOIN customers c USING (customer_id) WHERE {Y25} GROUP BY 1 ORDER BY 2 DESC LIMIT 2;")
show('Ans 23 FY2026 to 31 Dec 2025', "SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE order_date BETWEEN '2025-04-01' AND '2025-12-31';")
show('Timed challenge Q4 2025', """SELECT ROUND(SUM(net_revenue)), COUNT(DISTINCT order_id), COUNT(DISTINCT customer_id), ROUND(SUM(net_revenue)/COUNT(DISTINCT order_id),2), ROUND(100*(1-SUM(product_cost)/SUM(net_revenue)),1),
 (SELECT SUM(target_revenue) FROM sales_targets WHERE target_month BETWEEN '2025-10-01' AND '2025-12-01') FROM sales_lines WHERE order_date BETWEEN '2025-10-01' AND '2025-12-31';""")
show('Timed challenge Q4 2025 no rep (Level 7, Q4 version)', "SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE sales_rep_id IS NULL AND order_date BETWEEN '2025-10-01' AND '2025-12-31';")

# The CSV route, replayed step by step with duckdb (Power Query's Merge = LEFT OUTER JOIN)
print('\n## CSV route (duckdb on companion/full)')
d = duckdb.connect(); F = BOOK / 'companion/full'
for t in ('orders', 'order_items', 'products'):
    d.execute(f"CREATE VIEW {t} AS SELECT * FROM read_csv_auto('{F}/{t}.csv')")
print('  order_items rows', d.execute("SELECT COUNT(*) FROM order_items").fetchone())
print('  after merge with orders', d.execute("SELECT COUNT(*) FROM order_items LEFT JOIN orders USING (order_id)").fetchone())
print('  after status filter', d.execute("SELECT COUNT(*) FROM order_items LEFT JOIN orders USING (order_id) WHERE status <> 'Cancelled'").fetchone())
print('  revenue 2025 via custom columns', d.execute("""SELECT ROUND(SUM(quantity*oi.unit_price*(1-discount_pct/100))), ROUND(SUM(quantity*p.unit_cost))
 FROM order_items oi LEFT JOIN orders o USING (order_id) LEFT JOIN products p USING (product_id)
 WHERE status <> 'Cancelled' AND order_date BETWEEN '2025-01-01' AND '2025-12-31'""").fetchone())
