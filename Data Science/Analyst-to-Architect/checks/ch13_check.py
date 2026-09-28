#!/usr/bin/env python3
"""ch13_check.py - checks for Chapter 13 outputs that tools/verify_sql.py cannot run.

verify_sql.py runs each block in a fresh session and skips CREATE statements, so these
session-dependent demonstrations (section 13.2) are replayed here in ONE session each:
  1. CREATE TEMP TABLE ... AS SELECT  -> 'SELECT 7', then COUNT(*) = 7 (same session)
  2. the same COUNT(*) in a new session -> relation does not exist
  3. CREATE VIEW sales_lines a second time -> already exists (PostgreSQL and MySQL)
  4. the MySQL temporary-table spelling and its error after reconnecting
It also checks the calendar tables (Pattern 5, exercise 16) in both engines.
Run as root on the book's verification machine:  python3 checks/ch13_check.py
"""
import subprocess, sys

def pg(sql, db='riverstone'):
    r = subprocess.run(['su', 'postgres', '-c', f'psql -X -d {db}'], input=sql, capture_output=True, text=True, cwd='/tmp')
    return r.stdout + r.stderr

def my(sql, db='riverstone'):
    r = subprocess.run(['mysql', '-uroot', '-t', db], input=sql, capture_output=True, text=True)
    return r.stdout + r.stderr

checks = []
def expect(name, out, *needles):
    ok = all(n in out for n in needles)
    checks.append(ok)
    print(('OK   ' if ok else 'FAIL ') + name)
    if not ok:
        print(out)

temp = """CREATE TEMP TABLE customer_revenue_tmp AS
SELECT customer_id, SUM(net_revenue) AS revenue
FROM sales_lines
GROUP BY customer_id;
SELECT COUNT(*) AS customers FROM customer_revenue_tmp;
"""
expect('temp table, same session', pg(temp), 'SELECT 7', '         7')
expect('temp table, new session', pg('SELECT COUNT(*) AS customers FROM customer_revenue_tmp;'),
       'ERROR:  relation "customer_revenue_tmp" does not exist')
expect('view created twice (PostgreSQL)', pg('CREATE VIEW sales_lines AS SELECT 1;'),
       'ERROR:  relation "sales_lines" already exists')
expect('view created twice (MySQL)', my('CREATE VIEW sales_lines AS SELECT 1;'),
       "Table 'sales_lines' already exists")
expect('MySQL temporary table, same session',
       my(temp.replace('CREATE TEMP TABLE', 'CREATE TEMPORARY TABLE')), '|         7 |')
expect('MySQL temporary table, new session', my('SELECT COUNT(*) FROM customer_revenue_tmp;'),
       "Table 'riverstone.customer_revenue_tmp' doesn't exist")
cal = 'SELECT COUNT(*) AS n FROM calendar_months; SELECT COUNT(*) AS n FROM calendar_days;'
expect('calendar tables (PostgreSQL)', pg(cal, 'riverstone_2025'), ' 12\n', ' 365\n')
expect('calendar tables (MySQL)', my(cal, 'riverstone_2025'), '| 12 |', '| 365 |')
print(f'{sum(checks)} of {len(checks)} checks passed')
sys.exit(0 if all(checks) else 1)
