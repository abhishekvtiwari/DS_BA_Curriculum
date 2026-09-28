#!/usr/bin/env python3
"""ch12_companion.py - build Chapter 12's two query companion files from the chapter, and check them.

    python3 sql/ch12_companion.py            # write the files, run every query in both databases, compare

Writes
  companion/postgresql/ch12_queries_postgresql.sql   every reading query in the chapter, PostgreSQL spelling
  companion/mysql/ch12_queries_mysql.sql             the same queries in MySQL spelling
(Section 12.13's lab statements live in ch12_lab_postgresql.sql / ch12_lab_mysql.sql, not here.)

How the MySQL file is made: a ```mysql block in the chapter is used as printed; a ```sql block is translated
with the few spelling changes section 12.16 teaches (DATEDIFF, DATE_FORMAT, CONCAT, IS NULL sorting).
Blocks that only make sense in one database (casts to double precision, FULL OUTER JOIN, pg_database) are
kept in that database's file only. Statements that fail on purpose in the book are commented out.
Every query is then run in both databases and the results compared, row by row; the known, documented
differences (NULL sort order, case-insensitive comparison, integer division) are listed, not hidden.
"""
import re, subprocess, pathlib, sys

BOOK = pathlib.Path(__file__).resolve().parent.parent
MD = BOOK / 'manuscript' / 'ch12-databases-and-sql-foundations.md'
PG_OUT = BOOK / 'companion' / 'postgresql' / 'ch12_queries_postgresql.sql'
MY_OUT = BOOK / 'companion' / 'mysql' / 'ch12_queries_mysql.sql'

DML = re.compile(r'^\s*(BEGIN|START TRANSACTION|CREATE|INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE|RENAME)\b', re.I | re.M)
PG_ONLY = re.compile(r'double precision|FULL OUTER JOIN|pg_database', re.I)
KNOWN = {  # reason printed when the two results differ; keyed by a fragment of the query
    "SELECT DISTINCT city": 'MySQL sorts the NULL city first (section 12.16)',
    "WHERE status = 'delivered'": "MySQL's default collation ignores case: 8, not 0 (section 12.16, Trap 2)",
    "7 / 2": 'MySQL division always gives a decimal (section 12.4)',
    "AVG(amount)       AS avg_invoice": 'same value; MySQL prints fewer decimal places',
    "WHERE customer_id = 6": "MySQL's CONCAT returns NULL when any piece is NULL (section 12.8, exercise 21)",
    "SELECT city FROM customers WHERE segment": 'MySQL sorts the NULL city first (section 12.16)',
}

HEADER_PG = """-- =====================================================================
-- Analyst to Architect · Chapter 12 · Databases & SQL Foundations
-- Every reading query in the chapter, in PostgreSQL, in book order.
-- Built from the chapter by sql/ch12_companion.py; don't edit by hand.
--
-- Setup: section 12.3 (riverstone_setup.sql). Exercises 30 and 32 use the one-year database
-- (riverstone_2025_setup.sql); the file switches to it with \\c, which works in psql. In DBeaver,
-- open those queries in an editor connected to riverstone_2025 instead.
-- Section 12.13's statements are in ch12_lab_postgresql.sql.
-- Queries that fail on purpose in the book are commented out, with the error you'd see.
-- Riverstone Supplies is fictional; every name and number is invented.
-- =====================================================================
"""
HEADER_MY = """-- =====================================================================
-- Analyst to Architect · Chapter 12 · Databases & SQL Foundations
-- Every reading query in the chapter, rewritten for MySQL, in book order.
-- Built from the chapter by sql/ch12_companion.py; don't edit by hand.
--
-- Setup: run riverstone_setup_mysql.sql first (it creates the `riverstone` database).
-- Exercises 30 and 32 use riverstone_2025 (riverstone_2025_setup_mysql.sql).
-- Tested on MySQL 8.0.46; uses only features that work the same in MySQL 8.4 LTS and 9.x
-- (EXCEPT needs 8.0.31 or later). Results match the PostgreSQL outputs printed in the chapter,
-- except where a comment says otherwise. Queries that fail on purpose in the book are
-- commented out. Section 12.13's statements are in ch12_lab_mysql.sql.
-- Riverstone Supplies is fictional; every name and number is invented.
-- =====================================================================
"""


def to_mysql(q):
    """Translate a PostgreSQL query from the chapter into MySQL, using section 12.16's rules."""
    d = r"(?:DATE '\d{4}-\d\d-\d\d'|MAX\([\w.]+\)|MIN\([\w.]+\)|[\w.]*date)"
    q = re.sub(rf"({d})\s+-\s+({d})", r"DATEDIFF(\1, \2)", q)
    q = re.sub(r"DATE_TRUNC\('month', ([\w.]+)\)::date", r"CAST(DATE_FORMAT(\1, '%Y-%m-01') AS DATE)", q)
    q = re.sub(r"GROUP BY DATE_TRUNC\('month', ([\w.]+)\)", r"GROUP BY month", q)
    q = re.sub(r"ORDER BY ([\w.]+) NULLS FIRST", r"ORDER BY \1 IS NULL DESC, \1", q)

    def concat(m):
        parts = [p.strip() for p in m.group(2).split('||')]
        return f"{m.group(1)}CONCAT({', '.join(parts)}) AS {m.group(3)}{m.group(4)}"
    q = re.sub(r"^(\s*)(.+?\|\|.+?)\s+AS (\w+)(,?)$", concat, q, flags=re.M)
    return q


def blocks():
    """Yield (section, lang, code, expected_output, db) for every reading query outside the lab."""
    md = MD.read_text()
    tok = re.compile(r'<!-- (db|run): (\w+) -->|<!-- lab:(start|end) -->|^(#{2,3}) ([^\n]+)$|^```(\w*)\n(.*?)^```$', re.S | re.M)
    section, db, in_lab, run, pending = '', 'riverstone', False, None, None
    for m in tok.finditer(md):
        if m.group(1) == 'db': db = m.group(2); continue
        if m.group(1) == 'run': run = m.group(2); continue
        if m.group(3): in_lab = m.group(3) == 'start'; continue
        if m.group(4):
            if len(m.group(4)) == 2: section = m.group(5).strip()
            continue
        lang, body = m.group(6), m.group(7)
        if lang in ('sql', 'mysql'):
            if pending: yield pending
            skip = in_lab or run == 'none' or DML.search(body)
            pending = None if skip else [section, lang, body.rstrip('\n'), None, db]
            run = None
        elif lang == '' and pending:
            pending[3] = body; yield pending; pending = None
        else:
            run = None
    if pending: yield pending


def run_pg(q, db):
    r = subprocess.run(['su', 'postgres', '-c', f'psql -X -q -A -t -F "|" -d {db}'], input=q, capture_output=True, text=True, cwd='/tmp')
    return r.stdout, r.stderr


def run_my(q, db):
    r = subprocess.run(['mysql', '-uroot', '-B', '-N', db], input=q, capture_output=True, text=True)
    return r.stdout, r.stderr


def norm(rows):
    out = []
    for l in rows.strip().splitlines():
        cells = []
        for c in re.split(r'[|\t]', l):
            c = c.strip()
            if c in ('', 'NULL', '\\N'): c = ''
            elif c in ('t', 'f'): c = '1.0' if c == 't' else '0.0'
            else:
                try: c = repr(round(float(c), 6))
                except ValueError: pass
            cells.append(c)
        out.append('|'.join(cells))
    return out


def main():
    pg, my = [HEADER_PG], [HEADER_MY]
    last_sec = None; pairs = []; cur = [None]

    def use(db):
        if cur[0] == db: return ''
        cur[0] = db; return f'USE {db};\n'
    items = list(blocks())
    for i, (sec, lang, code, expected, db) in enumerate(items):
        fails = expected is not None and 'ERROR' in expected
        head = f"\n-- ---------------------------------------------------------------\n-- {sec}\n"
        if sec != last_sec:
            pg.append(head); my.append(head); last_sec = sec
        if lang == 'mysql':
            if fails:
                my.append('-- Fails on purpose in the book:\n' + '\n'.join('-- ' + l for l in code.splitlines()) + '\n')
            else:
                if 'USE ' in code: cur[0] = re.search(r'USE (\w+);', code).group(1); my.append(code + '\n')
                else: my.append(use(db) + code.rstrip().rstrip(';') + ';\n')
            continue
        # a PostgreSQL block
        pg_code = code if code.rstrip().endswith(';') else code + ';'
        if fails:
            err = [l for l in expected.splitlines() if 'ERROR' in l][0].strip()
            c = '\n'.join('-- ' + l for l in pg_code.splitlines())
            pg.append(f'-- Fails on purpose in the book ({err}):\n{c}\n')
            my.append(f'-- Fails on purpose in the book:\n{c}\n')
            continue
        pg.append((f'\\c {db}\n' if db != 'riverstone' else '') + pg_code + '\n')
        if PG_ONLY.search(code) or re.search(r'CREATE DATABASE', code):
            my.append('-- (PostgreSQL only; the MySQL form is the next query, or isn\'t needed.)\n')
            continue
        mq = to_mysql(pg_code)
        why = next((v for k, v in KNOWN.items() if k in pg_code), None)
        my.append(use(db) + (f'-- Differs from the PostgreSQL result on purpose: {why}.\n' if why else '') + mq + '\n')
        pairs.append((sec, pg_code, mq, db))
    my_text = ''.join(my)
    PG_OUT.write_text(''.join(pg))
    MY_OUT.write_text(my_text)
    # compare
    bad = 0
    for sec, pq, mq, db in pairs:
        a, ea = run_pg(pq, db); b, eb = run_my(mq, db)
        if ea.strip() or eb.strip():
            print(f'ERROR in {sec}:\n  pg: {ea.strip()[:200]}\n  my: {eb.strip()[:200]}\n  {mq[:200]}'); bad += 1; continue
        if norm(a) != norm(b):
            why = next((v for k, v in KNOWN.items() if k in pq), None)
            if why:
                print(f'known difference ({sec}): {why}')
            else:
                bad += 1; print(f'DIFFERENT in {sec}:\n{pq}\n  pg: {norm(a)[:4]}\n  my: {norm(b)[:4]}')
    print(f'{len(pairs)} queries compared; unexplained differences: {bad}')
    print(f'wrote {PG_OUT.relative_to(BOOK)} and {MY_OUT.relative_to(BOOK)}')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
