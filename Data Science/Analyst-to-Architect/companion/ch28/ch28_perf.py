#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 28 · Advanced SQL, Performance & Data Modeling
File: ch28_perf.py - reruns the chapter's performance experiments on riverstone_perf (PostgreSQL, and MySQL for
      section 28.13), in the same order as sections 28.5, 28.6 and 28.11, so the indexes that exist at each step
      are the ones the chapter has created by then. Each query runs 7 times (5 for the slow trend query); the
      median execution time is reported, and one full plan per experiment is saved to ch28_perf_log.txt,
      next to this script. Every plan and timing quoted in Chapter 28 comes from that log.
How:  python3 ch28_perf.py            (needs riverstone_perf loaded in PostgreSQL; MySQL part is skipped if absent)
      Runs psql and mysql as the local superusers (su postgres / mysql -uroot); edit PG_CMD / MY_CMD for your setup.
Tested on: Python 3.11, PostgreSQL 16.13, MySQL 8.0.46, Ubuntu 24.04, 4 virtual processors, 16 GB memory.
Your timings will differ; the plans and the ratios between slow and fast versions are what should match.
Riverstone Supplies is fictional; every name and number is invented.
"""
import os, re, statistics, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = open(os.path.join(HERE, 'ch28_perf_log.txt'), 'w')
PG_CMD = ['su', 'postgres', '-c', 'psql -X -q -d riverstone_perf']
MY_CMD = ['mysql', '-uroot', 'riverstone_perf']

def pg(sql):
    r = subprocess.run(PG_CMD, input=sql, capture_output=True, text=True, cwd='/tmp')
    if 'ERROR' in r.stderr: print(r.stderr); sys.exit(1)
    return r.stdout
def my(sql):
    r = subprocess.run(MY_CMD, input=sql, capture_output=True, text=True)
    if r.returncode: print(r.stderr); sys.exit(1)
    return r.stdout
def log(title, text):
    LOG.write(f'\n===== {title} =====\n{text}\n'); LOG.flush(); print(f'== {title}\n{text}')

def pg_time(label, query, runs=7, opts='ANALYZE, COSTS OFF'):
    times, plan = [], ''
    for _ in range(runs):
        plan = pg(f'EXPLAIN ({opts}) ' + query)
        times.append(float(re.search(r'Execution Time: ([\d.]+) ms', plan).group(1)))
    med = statistics.median(times)
    log(f'PG {label}: median {med:.2f} ms over {runs} runs', plan)
    return med

def my_time(label, query, runs=7):
    times, out = [], ''
    for _ in range(runs):
        out = my('EXPLAIN ANALYZE ' + query)
        times.append(float(re.search(r'actual time=[\d.]+\.\.([\d.]+)', out).group(1)))
    med = statistics.median(times)
    log(f'MySQL {label}: median {med:.2f} ms over {runs} runs', out.replace('\\n', '\n'))
    return med

def timed(sql):
    t = time.perf_counter(); pg(sql); return (time.perf_counter() - t) * 1000

# start from the state the chapter assumes: primary keys only
pg('DROP MATERIALIZED VIEW IF EXISTS monthly_category_revenue; DROP TABLE IF EXISTS oi_copy_0, oi_copy_4;')
for idx in ['idx_orders_customer_id', 'idx_order_items_order_id', 'idx_orders_order_date', 'idx_orders_customer_date',
            'idx_orders_customer_date_incl', 'idx_orders_pending', 'idx_orders_date_customer', 'idx_customers_upper_city']:
    pg(f'DROP INDEX IF EXISTS {idx};')
pg('VACUUM ANALYZE;')
R = {}

# ---- section 28.5: one customer's orders, before and after an index
Q1 = "SELECT order_id, order_date, status FROM orders WHERE customer_id = 2718;"
log('P1 plan with costs', pg('EXPLAIN ' + Q1))
R['p1_seq'] = pg_time('P1 one customer, no index', Q1)
log('P1 buffers, no index', pg('EXPLAIN (ANALYZE, BUFFERS, COSTS OFF) ' + Q1))
t = timed('CREATE INDEX idx_orders_customer_id ON orders (customer_id);'); pg('ANALYZE orders;')
log('P1 index build', f'{t:.0f} ms')
R['p1_idx'] = pg_time('P1 one customer, with index', Q1)
log('P1 buffers, with index', pg('EXPLAIN (ANALYZE, BUFFERS, COSTS OFF) ' + Q1))
R['p2_big'] = pg_time('P2 biggest customer 4534 with index', "SELECT order_id, order_date, status FROM orders WHERE customer_id = 4534;")
log('P2 delivered plan', pg("EXPLAIN SELECT order_id FROM orders WHERE status = 'Delivered';"))
log('P2 status counts', pg("SELECT status, COUNT(*) FROM orders GROUP BY status ORDER BY 2 DESC;"))

# ---- Figure 28.4 and experiment 1: the join, before and after an index on order_items.order_id
Q3b = ("SELECT SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS net_revenue "
       "FROM orders AS o JOIN order_items AS oi ON oi.order_id = o.order_id WHERE o.customer_id = 2718;")
Q3 = "SELECT order_item_id, product_id, quantity FROM order_items WHERE order_id = 500000;"
R['p3b_seq'] = pg_time('P3b one customer revenue, no FK index', Q3b)
R['p3_seq'] = pg_time('P3 lines of one order, no FK index', Q3)
t = timed('CREATE INDEX idx_order_items_order_id ON order_items (order_id);'); pg('ANALYZE order_items;')
log('P3 index build', f'{t:.0f} ms')
R['p3b_idx'] = pg_time('P3b one customer revenue, with FK index', Q3b)
R['p3_idx'] = pg_time('P3 lines of one order, with FK index', Q3)
log('P3 result', pg(Q3))

# ---- experiment 2: EXTRACT versus a date range
pg('CREATE INDEX idx_orders_order_date ON orders (order_date); ANALYZE orders;')
Q4a = "SELECT COUNT(*) FROM orders WHERE EXTRACT(YEAR FROM order_date) = 2025 AND EXTRACT(MONTH FROM order_date) = 12;"
Q4b = "SELECT COUNT(*) FROM orders WHERE order_date >= DATE '2025-12-01' AND order_date < DATE '2026-01-01';"
R['p4_fn'] = pg_time('P4 December via EXTRACT', Q4a)
R['p4_range'] = pg_time('P4 December via range', Q4b)
log('P4 counts', pg(Q4a) + pg(Q4b))

# ---- experiment 3: a composite index, on the big customer
Q6 = "SELECT order_date, status FROM orders WHERE customer_id = 4534 AND order_date >= DATE '2025-01-01';"
R['p6_single'] = pg_time('P6 big customer 2025, single-column indexes only', Q6)
pg('CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date); ANALYZE orders;')
R['p6_comp'] = pg_time('P6 big customer 2025, composite (customer_id, order_date)', Q6)
log('P6 buffers, composite', pg('EXPLAIN (ANALYZE, BUFFERS, COSTS OFF) ' + Q6))

# ---- experiment 4: the covering index replaces the plain composite one
pg('DROP INDEX idx_orders_customer_date;')
pg('CREATE INDEX idx_orders_customer_date_incl ON orders (customer_id, order_date) INCLUDE (status);')
pg('VACUUM ANALYZE orders;')
R['p6_cover'] = pg_time('P6 big customer 2025, covering INCLUDE (status)', Q6)

# ---- experiment 5: a partial index
Q7 = "SELECT order_id, customer_id, order_date FROM orders WHERE status = 'Pending' ORDER BY order_date;"
R['p7_seq'] = pg_time('P7 pending orders, no status index', Q7)
pg("CREATE INDEX idx_orders_pending ON orders (order_date) WHERE status = 'Pending'; ANALYZE orders;")
R['p7_partial'] = pg_time('P7 pending orders, partial index', Q7)
log('index sizes', pg("SELECT indexrelname AS index_name, pg_size_pretty(pg_relation_size(indexrelid)) AS size "
                      "FROM pg_stat_user_indexes WHERE relname IN ('orders','order_items') "
                      "ORDER BY pg_relation_size(indexrelid) DESC;"))
log('table sizes', pg("SELECT relname, pg_size_pretty(pg_relation_size(oid)) AS size, relpages FROM pg_class "
                      "WHERE relname IN ('orders','order_items');"))

# ---- experiment 6: the cost of indexes on writes (the SQL printed in section 28.6)
w0, w4 = [], []
for _ in range(3):
    pg('DROP TABLE IF EXISTS oi_copy_0, oi_copy_4;'
       'CREATE TABLE oi_copy_0 (LIKE order_items);'
       'CREATE TABLE oi_copy_4 (LIKE order_items INCLUDING INDEXES);'
       'CREATE INDEX ON oi_copy_4 (product_id);'
       'CREATE INDEX ON oi_copy_4 (order_id, product_id);')
    w0.append(timed('INSERT INTO oi_copy_0 SELECT * FROM order_items WHERE order_item_id <= 500000;'))
    w4.append(timed('INSERT INTO oi_copy_4 SELECT * FROM order_items WHERE order_item_id <= 500000;'))
log('write cost indexes on oi_copy_4', pg("SELECT indexname FROM pg_indexes WHERE tablename = 'oi_copy_4' ORDER BY indexname;"))
R['w0'], R['w4'] = statistics.median(w0), statistics.median(w4)
log('write cost 500k rows', f'no indexes median {R["w0"]:.0f} ms {[round(x) for x in w0]}; '
                           f'four indexes median {R["w4"]:.0f} ms {[round(x) for x in w4]}')
pg('DROP TABLE oi_copy_0, oi_copy_4;')

# ---- section 28.11: materialized view
Q9 = ("SELECT DATE_TRUNC('month', o.order_date)::date AS month, p.category, "
      "SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS net_revenue "
      "FROM orders AS o JOIN order_items AS oi ON oi.order_id = o.order_id "
      "JOIN products AS p ON p.product_id = oi.product_id WHERE o.status <> 'Cancelled' GROUP BY 1, 2;")
R['p9_live'] = pg_time('P9 monthly revenue by category, live', Q9, runs=5)
log('P9 buffers, live', pg('EXPLAIN (ANALYZE, BUFFERS, COSTS OFF) ' + Q9))
R['p9_build'] = timed('CREATE MATERIALIZED VIEW monthly_category_revenue AS ' + Q9)
pg('ANALYZE monthly_category_revenue;')
R['p9_mv'] = pg_time('P9 one month from materialized view',
                     "SELECT month, category, ROUND(net_revenue) AS net_revenue FROM monthly_category_revenue "
                     "WHERE month = DATE '2025-12-01' ORDER BY net_revenue DESC;")
R['p9_refresh'] = timed('REFRESH MATERIALIZED VIEW monthly_category_revenue;')
log('P9 build/refresh', f'build {R["p9_build"]:.0f} ms, refresh {R["p9_refresh"]:.0f} ms')
log('P9 mv rows', pg("SELECT COUNT(*) FROM monthly_category_revenue;"))
log('P9 counts', pg("SELECT COUNT(*) FROM orders WHERE status <> 'Cancelled';"
                    "SELECT COUNT(*) FROM orders o JOIN order_items oi ON oi.order_id = o.order_id WHERE o.status <> 'Cancelled';"))

# ---- section 28.13: MySQL (skipped if riverstone_perf isn't loaded there)
if subprocess.run(MY_CMD + ['-e', 'SELECT 1 FROM orders LIMIT 1'], capture_output=True).returncode == 0:
    if 'idx_orders_order_date' in my('SHOW INDEX FROM orders;'):
        my('DROP INDEX idx_orders_order_date ON orders;')
    log('MySQL indexes before', my('SHOW INDEX FROM orders;'))
    R['my_p1'] = my_time('P1 one customer (FK index exists)', Q1.rstrip(';'))
    my('CREATE INDEX idx_orders_order_date ON orders (order_date);')
    R['my_p4_fn'] = my_time('P4 December via EXTRACT', Q4a.rstrip(';'))
    R['my_p4_range'] = my_time('P4 December via range', Q4b.rstrip(';'))
    my('DROP INDEX idx_orders_order_date ON orders;')

log('SUMMARY', '\n'.join(f'{k}: {v:.2f}' for k, v in R.items()))
