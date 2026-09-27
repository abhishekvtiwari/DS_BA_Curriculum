#!/usr/bin/env python3
"""ch32_check.py - checks Chapter 32's numbers: the dbt marts against the source and against Chapter 28's star schema."""
import pathlib, re, subprocess, sys
ok = 0
def q(sql, db='riverstone_2025'):
    return subprocess.run(['su', 'postgres', '-c', f"psql -X -At -F'|' -d {db}"], input=sql,
                          capture_output=True, text=True, cwd='/tmp').stdout.strip()
def check(label, got, want):
    global ok
    assert got == want, f'{label}: {got!r} != {want!r}'
    ok += 1
check('fact rows and revenue', q("SELECT COUNT(*), ROUND(SUM(net_revenue)) FROM dbt_dev_marts.fct_sales_line;"), '326|4335471')
check('matches chapter 28 star', q("SELECT ROUND(SUM(net_revenue)) FROM dw.fact_sales_line;"), '4335471')
check('matches the source view', q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines;"), '4335471')
check('daily model', q("SELECT COUNT(*), ROUND(SUM(net_revenue)) FROM dbt_dev_marts.fct_daily_sales;"), '132|4335471')
check('date dimension', q("SELECT COUNT(*) FROM dbt_dev_marts.dim_date;"), '365')
check('product dimension', q("SELECT COUNT(*) FROM dbt_dev_marts.dim_product;"), '8')
check('sales rep dimension', q("SELECT COUNT(*) FROM dbt_dev_marts.dim_sales_rep;"), '6')
check('snapshot gave Metro Mart two versions',
      q("SELECT COUNT(*) FROM dbt_dev_marts.dim_customer WHERE customer_id = 5;"), '2')
check('one current row per customer',
      q("SELECT COUNT(*) FROM (SELECT customer_id FROM dbt_dev_marts.dim_customer WHERE is_current GROUP BY 1 HAVING COUNT(*) > 1) AS x;"), '0')
check('large incremental model', q("SELECT COUNT(*) FROM dbt_large_marts.fct_daily_sales;", 'riverstone_perf'), '1096')
project = pathlib.Path('/home/claude/book/companion/ch32/riverstone_dbt')
models = sorted(p.name for p in (project / 'models').rglob('*.sql'))
check('models in the project', len(models), 10)
check('macro defines net revenue once',
      (project / 'macros' / 'net_revenue.sql').read_text().count('macro net_revenue'), 1)
yaml = (project / 'models' / 'marts' / 'schema.yml').read_text() + (project / 'models' / 'staging' / 'schema.yml').read_text() \
       + (project / 'models' / 'staging' / 'sources.yml').read_text()
check('generic tests declared', sum(yaml.count(t) for t in ['unique', 'not_null', 'relationships', 'accepted_values']), 24)
check('no database pinned in sources', 'database:' in yaml, False)
check('no password in the project',
      any('riverstone123' in p.read_text() for p in project.rglob('*') if p.is_file()), False)
print(f'ch32_check.py: {ok} checks passed')
