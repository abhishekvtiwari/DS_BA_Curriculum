#!/usr/bin/env python3
"""ch12_lab_companion.py - rebuild section 12.13's lab files from the chapter, then run them end to end.

    python3 sql/ch12_lab_companion.py

Writes companion/postgresql/ch12_lab_postgresql.sql and companion/mysql/ch12_lab_mysql.sql: every statement
inside the chapter's <!-- lab:start --> regions (section 12.13 and the answers to exercises 23-27), in book
order, for the engine the chapter runs it in (<!-- run: pg|mysql|both -->). Statements whose printed output
is an error are commented out with that error, so each file runs start to finish. Both files are then run
in a fresh riverstone_lab database; the script stops with an error if either fails.
"""
import re, subprocess, pathlib, sys

BOOK = pathlib.Path(__file__).resolve().parent.parent
MD = BOOK / 'manuscript' / 'ch12-databases-and-sql-foundations.md'
PG_OUT = BOOK / 'companion' / 'postgresql' / 'ch12_lab_postgresql.sql'
MY_OUT = BOOK / 'companion' / 'mysql' / 'ch12_lab_mysql.sql'

PG_HEAD = """-- =====================================================================
-- Analyst to Architect · Chapter 12 · Section 12.13 lab, PostgreSQL version
-- Every statement from "Building and changing a database" and exercises 23-27, in book order.
-- Built from the chapter by sql/ch12_lab_companion.py; don't edit by hand.
-- Run it with psql:   psql -U postgres -d postgres -f ch12_lab_postgresql.sql
-- In DBeaver: run the CREATE DATABASE statement, connect to riverstone_lab, then run the rest
-- (skip the \\c line, which only psql understands).
-- Statements that fail on purpose in the book are commented out, with the error you'd see.
-- Riverstone Supplies is fictional; every name and number is invented.
-- =====================================================================

DROP DATABASE IF EXISTS riverstone_lab;
"""
MY_HEAD = """-- =====================================================================
-- Analyst to Architect · Chapter 12 · Section 12.13 lab, MySQL version
-- Every statement from "Building and changing a database" and exercises 23-27, in book order.
-- Built from the chapter by sql/ch12_lab_companion.py; don't edit by hand.
-- Run it with:   mysql -u root -p < ch12_lab_mysql.sql
-- or open it in MySQL Workbench or DBeaver and execute the whole script.
-- Tested on MySQL 8.0.46; uses only features available in MySQL 8.4 LTS and 9.x.
-- Statements that fail on purpose in the book are commented out, with the error you'd see.
-- Riverstone Supplies is fictional; every name and number is invented.
-- =====================================================================

DROP DATABASE IF EXISTS riverstone_lab;
DROP DATABASE IF EXISTS archive;
"""


def main():
    md = MD.read_text()
    tok = re.compile(r'<!-- (run|out): (\w+) -->|<!-- lab:(start|end) -->|^### ([^\n]+)$|^\*\*(\d+)\.\*\*|^```(\w*)\n(.*?)^```$', re.S | re.M)
    in_lab = False; run = None; out = None; label = ''; stmts = []  # [label, engine, code, {engine: error}]
    last = None
    for m in tok.finditer(md):
        if m.group(3): in_lab = m.group(3) == 'start'; continue
        if m.group(4): label = m.group(4).strip(); continue
        if m.group(5): label = f'Exercise {m.group(5)}'; continue
        if not in_lab: continue
        if m.group(1) == 'run': run = m.group(2); continue
        if m.group(1) == 'out': out = m.group(2); continue
        lang, body = m.group(6), m.group(7)
        if lang in ('sql', 'mysql'):
            eng = run or ('mysql' if lang == 'mysql' else 'pg'); run = None
            if eng == 'none': last = None; continue
            last = [label, eng, body.rstrip('\n'), {}, 'mysql' if eng == 'mysql' else 'pg']
            stmts.append(last)
        elif lang == '' and last:
            target = out or last[4]; out = None
            if 'ERROR' in body:
                last[3][target] = [l for l in body.splitlines() if 'ERROR' in l][0].strip()
            last[4] = None
    pg, my = [PG_HEAD], [MY_HEAD]
    for label, eng, code, errs in [s[:4] for s in stmts]:
        for e, buf in (('pg', pg), ('mysql', my)):
            if eng not in (e, 'both'): continue
            c = code
            if e == 'pg' and 'CREATE DATABASE riverstone_lab' in c: c += '\n\\c riverstone_lab'
            if e == 'mysql' and 'CREATE DATABASE riverstone_lab' in c: c += '\nUSE riverstone_lab;'
            if e in errs:
                c = f'-- Fails on purpose: {errs[e]}\n' + '\n'.join('-- ' + l for l in code.splitlines())
            buf.append(f'\n-- {label}\n{c}\n')
    tail = "\n-- When you've finished the lab (PostgreSQL: connect to another database first):\n-- DROP DATABASE IF EXISTS riverstone_lab;\n"
    PG_OUT.write_text(''.join(pg) + tail); MY_OUT.write_text(''.join(my) + tail)
    r1 = subprocess.run(['su', 'postgres', '-c', f'psql -X -q -v ON_ERROR_STOP=1 -d postgres -f "{PG_OUT}"'], capture_output=True, text=True, cwd='/tmp')
    r2 = subprocess.run(['mysql', '-uroot'], stdin=open(MY_OUT), capture_output=True, text=True)
    ok = r1.returncode == 0 and r2.returncode == 0
    print('PostgreSQL lab file:', 'ran clean' if r1.returncode == 0 else r1.stderr[-400:])
    print('MySQL lab file:', 'ran clean' if r2.returncode == 0 else r2.stderr[-400:])
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
