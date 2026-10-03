"""Load the chapter's own riverstone_2025 database into DuckDB and confirm it reproduces the
figures Chapter 71 already prints (24 customers, 11 NULL sales_rep_id, 0 then 2 reps, 1 of 24).

Foreign-key clauses are stripped on the way in. DuckDB checks a foreign key as each row is
inserted, so the self-referencing employees.manager_id and the multi-row VALUES lists fail there
although PostgreSQL accepts them. The constraints are not what any of these questions test.

If the four figures come back right, DuckDB is a sound place to verify new questions for this
chapter, and anything DuckDB and PostgreSQL genuinely disagree about is flagged by hand instead.
"""
import pathlib
import re
import sys
import duckdb

SKIP_PREFIXES = ('CREATE DATABASE', 'DROP DATABASE', 'USE ')
META = chr(92)          # a lone backslash: psql meta-commands such as \c and \dt


def strip_fks(stmt):
    """Remove FOREIGN KEY ... clauses and any REFERENCES ... that follows a column definition."""
    if 'CREATE TABLE' not in stmt.upper():
        return stmt
    # a table-level constraint, possibly spanning lines, up to the next comma at depth 0 or the end
    stmt = re.sub(r',\s*FOREIGN\s+KEY\s*\([^)]*\)\s*REFERENCES\s+\w+\s*\([^)]*\)', '', stmt,
                  flags=re.IGNORECASE)
    # an inline column-level reference
    stmt = re.sub(r'\s+REFERENCES\s+\w+\s*\([^)]*\)', '', stmt, flags=re.IGNORECASE)
    return stmt


ROOT = pathlib.Path(__file__).resolve().parents[2]
CANDIDATES = [
    ROOT / 'Data Science' / 'Analyst-to-Architect' / 'companion' / 'riverstone_2025_setup.sql',
    ROOT / 'companion' / 'riverstone_2025_setup.sql',
    pathlib.Path('companion/riverstone_2025_setup.sql'),
]
setup = next((p for p in CANDIDATES if p.exists()), None)
if setup is None:
    raise SystemExit('cannot find riverstone_2025_setup.sql; looked in:'
                     + ''.join(chr(10) + '  ' + str(p) for p in CANDIDATES))
print(f'setup: {setup}')

sql = setup.read_text(encoding='utf-8')
con = duckdb.connect(sys.argv[1] if len(sys.argv) > 1 else ':memory:')

kept = []
for ln in sql.splitlines():
    s = ln.strip()
    if s.startswith(META) or s.upper().startswith(SKIP_PREFIXES):
        continue
    kept.append(ln)

ok = bad = 0
errs = []
for stmt in [s.strip() for s in '\n'.join(kept).split(';')]:
    if not stmt or stmt.startswith('--'):
        continue
    try:
        con.execute(strip_fks(stmt))
        ok += 1
    except Exception as e:
        bad += 1
        if len(errs) < 8:
            errs.append(f"{type(e).__name__}: {str(e)[:150]} :: {stmt[:90]}")

print(f"statements: {ok} ok, {bad} failed")
for e in errs:
    print("  !", e)

print("\n### row counts")
for t in ['customers', 'products', 'employees', 'orders', 'order_items',
          'sales_targets', 'leads', 'lead_stage_history']:
    try:
        n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        print(f"  {t:<20} {n:>8,}")
    except Exception as ex:
        print(f"  {t:<20} missing ({type(ex).__name__})")

print("\n### the four figures Chapter 71 already prints")
checks = [
    ("NULL sales_rep_id", 11,
     "SELECT count(*) FROM orders WHERE sales_rep_id IS NULL"),
    ("NOT IN answer (the trap)", 0,
     "SELECT count(*) FROM employees WHERE employee_id NOT IN (SELECT sales_rep_id FROM orders)"),
    ("corrected answer", 2,
     "SELECT count(*) FROM employees WHERE employee_id NOT IN "
     "(SELECT sales_rep_id FROM orders WHERE sales_rep_id IS NOT NULL)"),
    ("customers with no orders", 1,
     "SELECT count(*) FROM customers c LEFT JOIN orders o "
     "ON c.customer_id = o.customer_id WHERE o.order_id IS NULL"),
]
allgood = True
for label, expected, q in checks:
    got = con.execute(q).fetchone()[0]
    mark = 'MATCHES' if got == expected else 'DIFFERS'
    allgood &= (got == expected)
    print(f"  {label:<28} chapter {expected:>3}   duckdb {got:>3}   {mark}")
print("\nverdict:", "DuckDB reproduces the chapter's database" if allgood
      else "DO NOT TRUST: the loaded data does not match the chapter")
