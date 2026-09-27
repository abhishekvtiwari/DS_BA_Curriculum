#!/usr/bin/env python3
"""ch29_check.py - checks the numbers quoted in Chapter 29's prose against the companion files and the database."""
import ast, json, pathlib, re, subprocess, tomllib
C = pathlib.Path('/home/claude/book/companion/ch29'); P = C / 'riverstone-report'
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    assert abs(got - want) <= tol if isinstance(want, (int, float)) else got == want, f'{label}: {got} != {want}'
    ok += 1
check('script lines', len((C / 'start/monthly_report.py').read_text().splitlines()), 40)
check('Dec pct of target', round(100 * 439823.50 / 380000, 1), 115.7)
check('test fixture revenue', 10000 + 2500 + 6000 + 1500 + 5000, 25000)
check('fixture pct', 100 * 25000 / 20000, 125.0)
check('shares', round(100 * 16000 / 25000, 1) + round(100 * 5000 / 25000, 1) + round(100 * 4000 / 25000, 1), 100.0, 0.001)
check('AOV', round(25000 / 3, 2), 8333.33); check('line mean', 25000 / 5, 5000)
check('order 10005 line', round(15 * 430 * 0.95, 2), 6127.5)
leads = json.loads((C / 'leads.json').read_text())
check('leads', len(leads), 43); check('website leads', sum(l['source'] == 'Website' for l in leads), 27)
check('pages at 10', -(-43 // 10), 5); check('last page items', 43 - 40, 3)
check('skipped page would report', 43 - 10, 33)
deps = tomllib.loads((P / 'pyproject.toml').read_text())['project']['dependencies']
check('direct deps', len(deps), 5)
lock = (P / 'uv.lock').read_text()
names = re.findall(r'^name = "([^"]+)"', lock, re.M)
check('lock packages', len(names), 32)
tests = {}
for f in (P / 'tests').glob('test_*.py'):
    tree = ast.parse(f.read_text())
    for fn in [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith('test_')]:
        cases = 1
        for d in fn.decorator_list:
            if isinstance(d, ast.Call) and getattr(d.func, 'attr', '') == 'parametrize':
                cases = len(d.args[1].elts)
        tests[fn.name] = cases
check('total test cases', sum(tests.values()), 23)
check('parametrized functions', sum(1 for v in tests.values() if v > 1), 3)
check('parametrized cases', sum(v for v in tests.values() if v > 1), 8)
check('plain unit tests', sum(1 for k, v in tests.items() if v == 1 and 'december_2025' not in k), 14)
check('ex12 wait range', 0.5 + 1 + 2, 3.5); check('ex12 max', (0.5 + 1 + 2) * 1.5, 5.25)
check('ex12 actual waits', round(0.619 + 1.329 + 2.666, 3), 4.614)
check('first wait in bounds', 0.5 <= 0.637 <= 0.75, True)
out = subprocess.run(['su', 'postgres', '-c', 'psql -X -At -d riverstone_2025'], input=
    "SELECT ROUND(SUM(net_revenue),2), COUNT(DISTINCT order_id), COUNT(*) FROM sales_lines WHERE order_date >= '2025-12-01';",
    capture_output=True, text=True, cwd='/tmp').stdout.strip()
check('December from database', out, '439823.50|18|35')
print(f'ch29_check.py: {ok} checks passed')
