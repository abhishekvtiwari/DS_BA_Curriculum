#!/usr/bin/env python3
"""make_mysql_queries.py - rebuild companion/mysql/ch13_queries_mysql.sql from Chapter 13 and test it.

Reads manuscript/ch13-sql-for-real-analysis.md, takes every ```sql block (PostgreSQL) and every ```mysql
block in book order, rewrites the PostgreSQL spellings for MySQL 8 (the table in section 13.9), writes
the companion file, then runs every query in MySQL and compares its result with the output printed in the
chapter (blank = NULL). Blocks that change the database or fail on purpose are written as comments.

Run from the book folder:  python3 companion/ch13/make_mysql_queries.py
Needs: a mysql client with root access and the riverstone / riverstone_2025 databases, including the
calendar tables from companion/ch13/calendar_tables_mysql.sql.
Exit code 0 when every result matches.
"""
import re, subprocess, sys
from pathlib import Path

BOOK = Path(__file__).resolve().parents[2]
CHAPTER = BOOK / 'manuscript' / 'ch13-sql-for-real-analysis.md'
OUT = BOOK / 'companion' / 'mysql' / 'ch13_queries_mysql.sql'

def balanced(s, i):
    """Index just after the parenthesis that closes the one opening at s[i]."""
    depth = 0
    for j in range(i, len(s)):
        depth += {'(': 1, ')': -1}.get(s[j], 0)
        if depth == 0:
            return j + 1
    raise ValueError('unbalanced')

def date_trunc(sql):
    while True:
        m = re.search(r"DATE_TRUNC\('month', ", sql)
        if not m:
            return sql
        end = balanced(sql, m.end() - len("'month', ") - 1)
        inner = sql[m.end():end - 1]
        tail = end + (6 if sql[end:end + 6] == '::date' else 0)
        sql = sql[:m.start()] + f"CAST(DATE_FORMAT({inner}, '%Y-%m-01') AS DATE)" + sql[tail:]

def filter_clause(sql):
    return re.sub(r"SUM\((\w+)\) FILTER \(WHERE (.+?)\)(, 0\))", r"SUM(CASE WHEN \2 THEN \1 END)\3", sql)

SUBTRACTIONS = [  # PostgreSQL date subtraction -> DATEDIFF(later, earlier)
    (r"DATE '2026-03-31' - i\.due_date", "DATEDIFF(DATE '2026-03-31', i.due_date)"),
    (r"(o\.order_date|order_date) - (LAG\(\1\) OVER \([^)]*\))", r"DATEDIFF(\1, \2)"),
    (r"DATE '2025-12-31' - r\.last_order", "DATEDIFF(DATE '2025-12-31', r.last_order)"),
    (r"w\.next_order_date - w\.order_date", "DATEDIFF(w.next_order_date, w.order_date)"),
    (r"gap_end - gap_start", "DATEDIFF(gap_end, gap_start)"),
]

def to_mysql(sql):
    sql = date_trunc(sql)
    sql = filter_clause(sql)
    for a, b in SUBTRACTIONS:
        sql = re.sub(a, b, sql)
    sql = re.sub(r"'Q' \|\| (EXTRACT\(QUARTER FROM [\w.]+\)|quarter)", r"CONCAT('Q', \1)", sql)
    sql = re.sub(r"SELECT generate_series\(DATE '2025-01-01', DATE '2025-12-01', INTERVAL '1 month'\)::date AS month",
                 "SELECT month FROM calendar_months  -- MySQL has no generate_series: use the calendar table", sql)
    assert '::' not in sql and '||' not in sql and 'FILTER' not in sql, sql
    return sql

def cells(block):
    """Rows of a psql or mysql -t result, as lists of cell strings (NULL shown as blank)."""
    rows = []
    for line in block.strip().splitlines():
        s = line.strip()
        if not s or re.fullmatch(r'[-+| ]+', s) or re.fullmatch(r'\(\d+ rows?\)', s):
            continue
        s = s.strip('|')
        rows.append(['' if c.strip() == 'NULL' else c.strip() for c in s.split('|')])
    width = max((len(r) for r in rows), default=0)   # psql drops trailing blank cells
    return [r + [''] * (width - len(r)) for r in rows]

def run_mysql(sql, db):
    r = subprocess.run(['mysql', '-uroot', '-t', db], input=sql, capture_output=True, text=True)
    return r.stdout + r.stderr

def main():
    md = CHAPTER.read_text(encoding='utf-8')
    token = re.compile(r'<!-- db: (\w+) -->|<!-- run: (\w+) -->|^(#{2,3}) ([^\n]+)$|^```(\w*)\n(.*?)^```$', re.S | re.M)
    db, h2, h3, run_none = 'riverstone', '', '', False
    items, last = [], None          # items: [heading, db, mysql_sql, kind, expected_output]
    for m in token.finditer(md):
        if m.group(1):
            db = m.group(1); continue
        if m.group(2):
            run_none = m.group(2) == 'none'; continue
        if m.group(3):
            if m.group(3) == '##': h2, h3 = m.group(4), ''
            else: h3 = m.group(4)
            last = None; continue
        lang, body = m.group(5), m.group(6)
        line = md[:m.start()].count('\n') + 1
        if lang in ('sql', 'mysql'):
            where = f"{h2} › {h3}" if h3 else h2
            if h2 == 'Answers':
                where = 'Answers'
            kind = 'query'
            sql = body if lang == 'mysql' else to_mysql(body)
            if 'CREATE TEMP TABLE' in body or run_none:
                kind = 'session'
            elif re.match(r'\s*CREATE VIEW', body):
                kind = 'view'
            elif 'OVER' in body and re.search(r'WHERE ROW_NUMBER\(\)', body):
                kind = 'error'
            last = [f'{where} (book line {line})', db, sql.rstrip(), kind, None]
            items.append(last); run_none = False
        elif lang == '' and last is not None and last[4] is None:
            last[4] = body
            last = None
    # write the companion file
    out = ["-- =====================================================================",
           "-- Analyst to Architect · Chapter 13 · SQL for Real Analysis",
           "-- Every query in the chapter, rewritten for MySQL, in book order.",
           "--",
           "-- Setup: run riverstone_setup_mysql.sql and riverstone_2025_setup_mysql.sql first, and the",
           "-- calendar tables (Pattern 5) from ch13/calendar_tables_mysql.sql if your setup script predates them.",
           "-- This file creates the sales_lines view in both databases (section 13.2).",
           "-- Tested on MySQL 8.0; uses only features that work the same in MySQL 8.4 LTS and 9.x.",
           "-- Results match the PostgreSQL outputs printed in the chapter.",
           "-- Queries that fail on purpose, or only make sense typed one by one in a session, are comments.",
           "-- Riverstone Supplies is fictional; every name and number is invented.",
           "-- Generated by ch13/make_mysql_queries.py from the chapter; do not edit by hand.",
           "-- ====================================================================="]
    cur = None
    for where, idb, sql, kind, _ in items:
        out += ["", "-- ---------------------------------------------------------------", f"-- {where}"]
        if kind == 'view':
            for vdb in ('riverstone', 'riverstone_2025'):
                out += [f"USE {vdb};", sql.replace('CREATE VIEW', 'CREATE OR REPLACE VIEW', 1)]
            cur = 'riverstone_2025'
            continue
        if kind in ('error', 'session'):
            note = ("-- Fails on purpose, as in the book. MySQL says: ERROR 3593: You cannot use the window function "
                    "'row_number' in this context." if kind == 'error' else
                    "-- Session demonstration (section 13.2): type these one at a time in one connection."
                    " MySQL spells it CREATE TEMPORARY TABLE.")
            sql = sql.replace('CREATE TEMP TABLE', 'CREATE TEMPORARY TABLE')
            out += [note] + ['-- ' + l for l in sql.splitlines()]
            continue
        if idb != cur:
            out.append(f"USE {idb};"); cur = idb
        out.append(sql if sql.endswith(';') else sql + ';')
    OUT.write_text('\n'.join(out) + '\n', encoding='utf-8')
    # run and compare
    checked = bad = 0
    for where, idb, sql, kind, expected in items:
        if kind != 'query' or expected is None:
            continue
        got = run_mysql(sql, idb)
        checked += 1
        if 'ERROR' in got or cells(got) != cells(expected):
            bad += 1
            print('MISMATCH', where); print(got[:800])
    print(f'{OUT.relative_to(BOOK)}: {len(items)} blocks written, {checked} results compared, {bad} mismatches')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
