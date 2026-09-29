#!/usr/bin/env python3
"""
ch64_sql_check.py - run Chapter 64's access-control lab (section 64.3) for real and compare every
printed result with PostgreSQL's actual output.

Why a separate check: the lab creates roles and row-level security policies, and it needs the
companion's setup script first, so tools/verify_sql.py (which skips DDL outside its own lab
database) can't run it; the chapter marks those blocks <!-- run: none --> for verify_sql.

What it does:
  1. drops and recreates the database riverstone_access and runs companion/ch64/access_lab_setup.sql
     (which also drops the lab roles), so every run starts from nothing;
  2. runs every ```sql block of the chapter, in order, each in its own psql session (as the reader's
     SET ROLE ... RESET ROLE blocks expect), skipping CREATE DATABASE;
  3. compares each block's output with the plain ``` block after it, using verify_sql's rules;
  4. runs exercise 13's answer and checks that Delhi's staff see exactly order 9004.

Usage (from the book folder):
  python3 checks/ch64_sql_check.py [--host /tmp/ch64pg --port 5464]
Needs psql and the right to run it as the postgres user (CREATE ROLE needs a superuser).
The roles it creates (branch_staff, analytics, kolkata_staff, mumbai_staff, delhi_staff) are
server-wide; the setup script drops them at the start of the next run.
"""
import argparse, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(BOOK, "tools"))
from verify_sql import compare, norm  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--host", default=None, help="socket directory or host (default: psql's default)")
ap.add_argument("--port", default=None)
a = ap.parse_args()
conn = (f" -h {a.host}" if a.host else "") + (f" -p {a.port}" if a.port else "")


def psql(sql, db):
    r = subprocess.run(["su", "postgres", "-c", f"psql -X -q{conn} -d {db}"], input=sql,
                       capture_output=True, text=True, cwd="/tmp")
    return r.stdout + r.stderr


chapter = os.path.join(BOOK, "manuscript", "ch64-security-privacy-governance-and-responsible-ai.md")
md = open(chapter, encoding="utf-8").read()
setup = open(os.path.join(BOOK, "companion", "ch64", "access_lab_setup.sql"), encoding="utf-8").read()

psql("DROP DATABASE IF EXISTS riverstone_access;", "postgres")
psql("CREATE DATABASE riverstone_access;", "postgres")
out = psql(setup, "riverstone_access")
errors = [l for l in out.splitlines() if "ERROR" in l]
if errors:
    print("setup failed:", errors[:3]); sys.exit(1)

token = re.compile(r"^```(\w*)\n(.*?)^```$", re.S | re.M)
last = None; ran = checked = bad = 0
for m in token.finditer(md):
    line = md[:m.start()].count("\n") + 1
    lang, body = m.group(1), m.group(2)
    if lang == "sql":
        if re.search(r"\bCREATE DATABASE\b", body):
            last = None; continue
        last = psql(body, "riverstone_access"); ran += 1
        continue
    if lang == "" and last is not None:
        checked += 1
        if not compare(body, last):
            bad += 1
            print(f"MISMATCH at line {line}"); print("  expected:", norm(body)[:6]); print("  got     :", norm(last)[:6])
        last = None
        continue
    last = None

# Exercise 13's answer: the plain block after "**13.**" in the Answers
answers = md[md.index("## Answers"):]
ex13 = re.search(r"\*\*13\.\*\*.*?^```\n(.*?)^```$", answers, re.S | re.M).group(1)
got = psql(ex13, "riverstone_access")
rows = [l for l in got.splitlines() if re.match(r"\s*\d{4}\s*\|", l)]
ok13 = len(rows) == 1 and "9004" in rows[0] and "Delhi" in rows[0]
print("exercise 13 answer:", "OK, " + rows[0].strip() if ok13 else "FAILED: " + got)
bad += 0 if ok13 else 1
print(f"{os.path.relpath(chapter, BOOK)}: SQL blocks run {ran}, outputs checked {checked}, mismatches {bad}")
sys.exit(1 if bad else 0)
