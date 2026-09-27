#!/usr/bin/env python3
"""ch28_perf.py - Chapter 28 performance experiments on riverstone_perf (PostgreSQL 16 and MySQL 8.0).
Runs each query 7 times, reports the median execution time, and saves one full plan per experiment
to ch28_perf_log.txt. Every timing and plan quoted in Chapter 28 comes from this log.
Machine: sandbox, 1 vCPU, 3 GB RAM, Ubuntu 24.04. Database: riverstone_perf (generate_riverstone_perf.py, seed 28)."""
import re, statistics, subprocess, sys

LOG = open('/home/claude/book/checks/ch28_perf_log.txt', 'w')
def pg(sql):
    r = subprocess.run(['su', 'postgres', '-c', 'psql -X -q -d riverstone_perf'], input=sql, capture_output=True, text=True, cwd='/tmp')
    if 'ERROR' in r.stderr: print(r.stderr); sys.exit(1)
    return r.stdout
def my(sql):
    r = subprocess.run(['mysql', '-uroot', 'riverstone_perf'], input=sql, capture_output=True, text=True)
    if r.returncode: print(r.stderr); sys.exit(1)
    return r.stdout
def log(title, text):
    LOG.write(f'\n===== {title} =====\n{text}\n'); LOG.flush(); print(f'== {title}\n{text}')

def pg_time(label, query, runs=7):
    times, plan = [], ''
    for _ in range(runs):
        plan = pg('EXPLAIN (ANALYZE, COSTS OFF) ' + query)
        times.append(float(re.search(r'Execution Time: ([\d.]+) ms', plan).group(1)))
    med = statistics.median(times)
    log(f'PG {label}: median {med:.2f} ms over {runs} runs', plan)
    return med

def my_time(label, query, runs=7):
    times, out = [], ''
    for _ in range(runs):
        out = my('EXPLAIN ANALYZE ' + query)
        # top line: actual time=first..last
        times.append(float(re.search(r'actual time=[\d.]+\.\.([\d.]+)', out).group(1)))
    med = statistics.median(times)
    log(f'MySQL {label}: median {med:.2f} ms over {runs} runs', out.replace('\\n', '\n'))
    return med

pg('DROP MATERIALIZED VIEW IF EXISTS monthly_category_revenue; DROP TABLE IF EXISTS items_copy_0, items_copy_4;')
for idx in ['idx_orders_customer_id', 'idx_order_items_order_id', 'idx_orders_order_date', 'idx_orders_customer_date',
            'idx_orders_customer_date_incl', 'idx_orders_pending', 'idx_orders_date_customer']:
    pg(f'DROP INDEX IF EXISTS {idx};')
pg('VACUUM ANALYZE;')

R = {}
Q1 = "SELECT order_id, order_date, status FROM orders WHERE customer_id = 2718;"
R['p1_seq'] = pg_time('P1 one customer, no index', Q1)
log('P1 plan with costs', pg('EXPLAIN ' + Q1))
pg('CREATE INDEX idx_orders_customer_id ON orders (customer_id); ANALYZE orders;')
R['p1_idx'] = pg_time('P1 one customer, with index', Q1)
R['p2_big'] = pg_time('P2 biggest customer 4534 with index', "SELECT order_id, order_date, status FROM orders WHERE customer_id = 4534;")
log('P2 delivered plan', pg("EXPLAIN SELECT order_id FROM orders WHERE status = 'Delivered';"))

Q3 = """SELECT p.product_name, oi.quantity FROM order_items AS oi JOIN products AS p ON p.product_id = oi.product_id WHERE oi.order_id = 500000;"""
R['p3_seq'] = pg_time('P3 lines of one order, no FK index', Q3)
Q3b = """SELECT SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS net_revenue FROM orders AS o JOIN order_items AS oi ON oi.order_id = o.order_id WHERE o.customer_id = 2718;"""
R['p3b_seq'] = pg_time('P3b one customer revenue, no FK index', Q3b)
pg('CREATE INDEX idx_order_items_order_id ON order_items (order_id); ANALYZE order_items;')
R['p3_idx'] = pg_time('P3 lines of one order, with FK index', Q3)
R['p3b_idx'] = pg_time('P3b one customer revenue, with FK index', Q3b)

pg('CREATE INDEX idx_orders_order_date ON orders (order_date); ANALYZE orders;')
Q4a = "SELECT COUNT(*) FROM orders WHERE EXTRACT(YEAR FROM order_date) = 2025 AND EXTRACT(MONTH FROM order_date) = 12;"
Q4b = "SELECT COUNT(*) FROM orders WHERE order_date >= DATE '2025-12-01' AND order_date < DATE '2026-01-01';"
R['p4_fn'] = pg_time('P4 December via EXTRACT', Q4a)
R['p4_range'] = pg_time('P4 December via range', Q4b)
log('P4 counts', pg(Q4a) + pg(Q4b))

Q6 = "SELECT order_id, order_date, status FROM orders WHERE customer_id = 2718 AND order_date >= DATE '2025-01-01';"
pg('DROP INDEX IF EXISTS idx_orders_order_date; CREATE INDEX idx_orders_date_customer ON orders (order_date, customer_id); ANALYZE orders;')
R['p6_wrong_order'] = pg_time('P6 one customer 2025, composite (order_date, customer_id)', Q6)
pg('DROP INDEX idx_orders_date_customer; CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date); ANALYZE orders;')
R['p6_right_order'] = pg_time('P6 one customer 2025, composite (customer_id, order_date)', Q6)
Q6c = "SELECT order_date, status FROM orders WHERE customer_id = 4534 AND order_date >= DATE '2025-01-01';"
R['p6c_comp'] = pg_time('P6c big customer 2025, composite', Q6c)
pg('CREATE INDEX idx_orders_customer_date_incl ON orders (customer_id, order_date) INCLUDE (status); VACUUM ANALYZE orders;')
R['p6c_cover'] = pg_time('P6c big customer 2025, covering INCLUDE (status)', Q6c)
pg('DROP INDEX idx_orders_customer_date_incl; CREATE INDEX idx_orders_order_date ON orders (order_date); ANALYZE orders;')

Q7 = "SELECT order_id, customer_id, order_date FROM orders WHERE status = 'Pending' ORDER BY order_date;"
R['p7_seq'] = pg_time('P7 pending orders, no status index', Q7)
pg("CREATE INDEX idx_orders_pending ON orders (order_date) WHERE status = 'Pending'; ANALYZE orders;")
R['p7_partial'] = pg_time('P7 pending orders, partial index', Q7)
log('index sizes', pg("SELECT indexrelname AS index_name, pg_size_pretty(pg_relation_size(indexrelid)) AS size FROM pg_stat_user_indexes WHERE relname IN ('orders','order_items') ORDER BY pg_relation_size(indexrelid) DESC;"))

# write cost: load 500,000 rows into an empty copy of order_items with no extra index vs four extra indexes
import time
def timed(sql):
    t = time.perf_counter(); pg(sql); return (time.perf_counter() - t) * 1000
w0, w4 = [], []
for _ in range(3):
    pg('DROP TABLE IF EXISTS items_copy_0, items_copy_4; CREATE TABLE items_copy_0 (LIKE order_items INCLUDING DEFAULTS); CREATE TABLE items_copy_4 (LIKE order_items INCLUDING DEFAULTS);'
       'CREATE INDEX ON items_copy_4 (order_id); CREATE INDEX ON items_copy_4 (product_id); CREATE INDEX ON items_copy_4 (order_id, product_id); CREATE INDEX ON items_copy_4 (unit_price);')
    w0.append(timed('INSERT INTO items_copy_0 SELECT * FROM order_items WHERE order_item_id <= 500000;'))
    w4.append(timed('INSERT INTO items_copy_4 SELECT * FROM order_items WHERE order_item_id <= 500000;'))
R['w0'], R['w4'] = statistics.median(w0), statistics.median(w4)
log('write cost 500k rows', f'no indexes median {R["w0"]:.0f} ms {w0}; four indexes median {R["w4"]:.0f} ms {w4}')
pg('DROP TABLE items_copy_0, items_copy_4;')

Q9 = """SELECT date_trunc('month', o.order_date)::date AS month, p.category, SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS net_revenue FROM orders AS o JOIN order_items AS oi ON oi.order_id = o.order_id JOIN products AS p ON p.product_id = oi.product_id WHERE o.status <> 'Cancelled' GROUP BY 1, 2;"""
R['p9_live'] = pg_time('P9 monthly revenue by category, live', Q9, runs=5)
t = time.perf_counter(); pg('CREATE MATERIALIZED VIEW monthly_category_revenue AS ' + Q9); R['p9_build'] = (time.perf_counter() - t) * 1000
pg('ANALYZE monthly_category_revenue;')
R['p9_mv'] = pg_time('P9 monthly revenue by category, from materialized view', "SELECT * FROM monthly_category_revenue WHERE month >= DATE '2025-01-01';")
t = time.perf_counter(); pg('REFRESH MATERIALIZED VIEW monthly_category_revenue;'); R['p9_refresh'] = (time.perf_counter() - t) * 1000
log('P9 build/refresh', f'build {R["p9_build"]:.0f} ms, refresh {R["p9_refresh"]:.0f} ms')
log('P9 mv rows', pg("SELECT COUNT(*) FROM monthly_category_revenue;"))

# MySQL: the same customer lookup and the EXTRACT trap
my('DROP INDEX idx_orders_order_date ON orders;') if 'idx_orders_order_date' in my('SHOW INDEX FROM orders;') else None
for name in ['idx_orders_customer_date']:
    pass
log('MySQL indexes before', my('SHOW INDEX FROM orders;'))
R['my_p1'] = my_time('P1 one customer (FK index exists)', Q1.replace(';', ''))
log('MySQL P1 tree', my('EXPLAIN FORMAT=TREE ' + Q1).replace('\\n', '\n'))
my('CREATE INDEX idx_orders_order_date ON orders (order_date);')
R['my_p4_fn'] = my_time('P4 December via EXTRACT', Q4a.replace(';', ''))
R['my_p4_range'] = my_time('P4 December via range', Q4b.replace(';', ''))
my('DROP INDEX idx_orders_order_date ON orders;')

log('SUMMARY', '\n'.join(f'{k}: {v:.2f}' for k, v in R.items()))
