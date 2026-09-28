#!/usr/bin/env python3
"""ch29_check.py - author's check for Chapter 29: the numbers quoted in the prose, the companion package
(lockfile, tests, type check, command line), and every Python output in the chapter.

Usage:  python3 checks/ch29_check.py            (from the book folder, Analyst-to-Architect)
Needs:  uv 0.12 or later on PATH (or UV=/path/to/uv), PostgreSQL with riverstone_2025, and the
        postgres password in RIVERSTONE_PG_PASSWORD (default "postgres").
It writes companion/ch29/riverstone-report/.env (git-ignored) and the December workbook in
companion/ch29/riverstone-report/reports/ (also git-ignored), which the chapter's last Python cells read.
"""
import ast, json, os, pathlib, re, subprocess, sys, tomllib

BOOK = pathlib.Path(__file__).resolve().parent.parent
C = BOOK / 'companion/ch29'; P = C / 'riverstone-report'
CHAPTER = BOOK / 'manuscript/ch29-python-as-software-not-scripts.md'
UV = os.environ.get('UV', 'uv')
ok = 0


def check(label, got, want, tol=0.0):
    global ok
    good = abs(got - want) <= tol if isinstance(want, (int, float)) and not isinstance(want, bool) else got == want
    assert good, f'{label}: {got!r} != {want!r}'
    ok += 1


def run(cmd, **kw):
    env = {k: v for k, v in os.environ.items() if k not in ('VIRTUAL_ENV', 'UV_NATIVE_TLS')}
    return subprocess.run(cmd, cwd=P, capture_output=True, text=True, env=env, **kw)


# --- numbers in the prose -------------------------------------------------------------------------
check('script lines', len((C / 'start/monthly_report.py').read_text().splitlines()), 40)
check('Dec pct of target', round(100 * 439823.50 / 380000, 1), 115.7)
check('test fixture revenue', 10000 + 2500 + 6000 + 1500 + 5000, 25000)
check('fixture pct', 100 * 25000 / 20000, 125.0)
check('shares', round(100 * 16000 / 25000, 1) + round(100 * 5000 / 25000, 1) + round(100 * 4000 / 25000, 1), 100.0, 0.001)
check('AOV', round(25000 / 3, 2), 8333.33); check('line mean', 25000 / 5, 5000)
check('order 10005 line', round(15 * 430 * 0.95, 2), 6127.5)
check('price after 5%', round(430 * 0.95, 2), 408.5)
leads = json.loads((C / 'leads.json').read_text())
check('leads', len(leads), 43); check('website leads', sum(l['source'] == 'Website' for l in leads), 27)
check('pages at 10', -(-43 // 10), 5); check('last page items', 43 - 40, 3)
check('skipped page would report', 43 - 10, 33)
import random
r = random.Random(29); waits = [round(b + r.uniform(0, b / 2), 3) for b in (0.5, 1.0, 2.0)]
check('seed 29 waits', waits, [0.637, 1.173, 2.845])
r = random.Random(12); waits = [round(b + r.uniform(0, b / 2), 3) for b in (0.5, 1.0, 2.0)]
check('seed 12 waits (answer 12)', waits, [0.619, 1.329, 2.666])
check('ex12 bounds', (0.5 + 1 + 2, (0.5 + 1 + 2) * 1.5), (3.5, 5.25))

# --- the package: dependencies, lockfile, tests -----------------------------------------------------
project = tomllib.loads((P / 'pyproject.toml').read_text())
check('direct deps', len(project['project']['dependencies']), 5)
check('requires-python', project['project']['requires-python'], '>=3.14')
lock = (P / 'uv.lock').read_text()
check('lock packages', len(re.findall(r'^name = "([^"]+)"', lock, re.M)), 58)
tests = {}
for f in (P / 'tests').glob('test_*.py'):
    for fn in [n for n in ast.parse(f.read_text()).body if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]:
        cases = 1
        for d in fn.decorator_list:
            if isinstance(d, ast.Call) and getattr(d.func, 'attr', '') == 'parametrize':
                cases = len(d.args[1].elts)
        tests[fn.name] = cases
check('total test cases', sum(tests.values()), 23)
check('parametrized functions', sum(1 for v in tests.values() if v > 1), 3)
check('parametrized cases', sum(v for v in tests.values() if v > 1), 8)
check('plain unit tests', sum(1 for k, v in tests.items() if v == 1 and 'december_2025' not in k), 14)

# --- the database ---------------------------------------------------------------------------------
out = subprocess.run(['su', 'postgres', '-c', 'psql -X -At -d riverstone_2025'], input=
    "SELECT ROUND(SUM(net_revenue),2), COUNT(DISTINCT order_id), COUNT(*), COUNT(DISTINCT customer_id) "
    "FROM sales_lines WHERE order_date >= '2025-12-01';", capture_output=True, text=True, cwd='/tmp').stdout.strip()
check('December from database', out, '439823.50|18|35|15')

# --- run the package the way the chapter does -------------------------------------------------------
password = os.environ.get('RIVERSTONE_PG_PASSWORD', 'postgres')
(P / '.env').write_text((P / '.env.example').read_text().replace('YOUR_PASSWORD', password))
res = run([UV, 'sync', '--locked']); check('uv sync --locked', res.returncode, 0)
res = run([UV, 'run', 'pytest', '-q']); check('pytest without database', res.stdout.strip().splitlines()[-1].split(' in ')[0], '22 passed, 1 skipped')
res = run([UV, 'run', '--env-file', '.env', 'pytest', '-q']); check('pytest with database', res.stdout.strip().splitlines()[-1].split(' in ')[0], '23 passed')
res = run([UV, 'run', 'mypy']); check('mypy', res.stdout.strip(), 'Success: no issues found in 9 source files')
res = run([UV, 'run', 'riverstone-report']); check('missing --month exit code', res.returncode, 2)
for month, code in (('2025-12', 0), ('2026-01', 1), ('Dec-2025', 1)):
    res = run([UV, 'run', '--env-file', '.env', 'riverstone-report', '--month', month])
    check(f'exit code for {month}', res.returncode, code)
check('December workbook', (P / 'reports/riverstone_monthly_2025-12.xlsx').exists(), True)

# --- every Python output in the chapter, in the package's environment plus python-dotenv -----------------
res = run([UV, 'run', '--with', 'python-dotenv', 'python', str(BOOK / 'tools/verify_python.py'), str(CHAPTER), '--cwd', str(C)])
print(res.stdout.strip().splitlines()[-1])
check('verify_python mismatches', res.returncode, 0)
print(f'ch29_check.py: {ok} checks passed')
