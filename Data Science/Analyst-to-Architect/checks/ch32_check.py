#!/usr/bin/env python3
"""ch32_check.py - checks Chapter 32's numbers: the dbt marts against the source and against Chapter 28's star schema.

Run after building the companion project (companion/ch32/riverstone_dbt) with `dbt build` against riverstone_2025
(target dev) and `dbt run --target large --select +fct_daily_sales --full-refresh`, and after section 32.9's
snapshot demonstration (Evergreen Mart, customer 18, reclassified as Wholesale in raw_crm.customers).
"""
import pathlib, subprocess
ok = 0
def q(sql, db='riverstone_2025'):
    return subprocess.run(['su', 'postgres', '-c', f"psql -X -At -F'|' -d {db}"], input=sql,
                          capture_output=True, text=True, cwd='/tmp').stdout.strip()
def check(label, got, want):
    global ok
    assert got == want, f'{label}: {got!r} != {want!r}'
    ok += 1
check('stand-in CRM extract', q("SELECT COUNT(*) FROM raw_crm.customers;"), '24')
check('fact rows and revenue', q("SELECT COUNT(*), ROUND(SUM(net_revenue)) FROM dbt_dev_marts.fct_sales_line;"), '326|4335471')
check('customer versions in the fact', q("SELECT COUNT(DISTINCT customer_key) FROM dbt_dev_marts.fct_sales_line;"), '23')
check('matches chapter 28 star', q("SELECT ROUND(SUM(net_revenue)) FROM dw.fact_sales_line;"), '4335471')
check('matches the source view', q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines;"), '4335471')
check('daily model', q("SELECT COUNT(*), MIN(order_date), MAX(order_date), ROUND(SUM(net_revenue)) FROM dbt_dev_marts.fct_daily_sales;"),
      '132|2025-01-02|2025-12-23|4335471')
check('latest order in the source', q("SELECT MAX(order_date) FROM orders;"), '2025-12-23')
check('monthly pivot', q("SELECT COUNT(*), ROUND(SUM(revenue_storage + revenue_kitchen + revenue_industrial + revenue_furniture)) FROM dbt_dev_marts.mart_sales_monthly;"),
      '12|4335471')
check('date dimension', q("SELECT COUNT(*) FROM dbt_dev_marts.dim_date;"), '365')
check('product dimension', q("SELECT COUNT(*) FROM dbt_dev_marts.dim_product;"), '8')
check('sales rep dimension', q("SELECT COUNT(*) FROM dbt_dev_marts.dim_sales_rep;"), '6')
check('customer dimension after the demo', q("SELECT COUNT(*) FROM dbt_dev_marts.dim_customer;"), '25')
check('snapshot gave Evergreen Mart two versions',
      q("SELECT string_agg(segment || ':' || is_current, ',' ORDER BY valid_from) FROM dbt_dev_marts.dim_customer WHERE customer_id = 18;"),
      'Retail:false,Wholesale:true')
check('one current row per customer',
      q("SELECT COUNT(*) FROM (SELECT customer_id FROM dbt_dev_marts.dim_customer WHERE is_current GROUP BY 1 HAVING COUNT(*) > 1) AS x;"), '0')
check('Metro Mart all in Mumbai (no audit history)',
      q("SELECT string_agg(DISTINCT c.city, ',') FROM dbt_dev_marts.fct_sales_line f JOIN dbt_dev_marts.dim_customer c USING (customer_key) WHERE c.customer_id = 5;"), 'Mumbai')
check('quarter x segment cells add to 4,335,473',
      q("SELECT SUM(r) FROM (SELECT ROUND(SUM(f.net_revenue)) r FROM dbt_dev_marts.fct_sales_line f JOIN dbt_dev_marts.dim_date d USING (date_key) JOIN dbt_dev_marts.dim_customer c USING (customer_key) GROUP BY d.quarter_label, c.segment) x;"), '4335473')
check('large incremental model', q("SELECT COUNT(*) FROM dbt_large_marts.fct_daily_sales;", 'riverstone_perf'), '1096')
check('large database lines', q("SELECT COUNT(*) FROM order_items;", 'riverstone_perf'), '1926847')
check('december 2025 net revenue', q("SELECT SUM(net_revenue) FROM dbt_dev_marts.fct_daily_sales WHERE order_date >= '2025-12-01';"), '439823.50')
check('two cancelled orders, four lines', q("SELECT COUNT(*) FROM order_items oi JOIN orders o USING (order_id) WHERE o.status = 'Cancelled';"), '4')
project = pathlib.Path(__file__).resolve().parents[1] / 'companion' / 'ch32' / 'riverstone_dbt'
models = sorted(p.name for p in (project / 'models').rglob('*.sql'))
check('models in the project', len(models), 10)
check('macro defines net revenue once',
      (project / 'macros' / 'net_revenue.sql').read_text().count('macro net_revenue'), 1)
yaml = (project / 'models' / 'marts' / 'schema.yml').read_text() + (project / 'models' / 'staging' / 'schema.yml').read_text() \
       + (project / 'models' / 'staging' / 'sources.yml').read_text()
check('generic tests declared', sum(yaml.count(t) for t in ['unique', 'not_null', 'relationships', 'accepted_values']), 25)
check('no database pinned in sources', 'database:' in yaml, False)
check('profiles.yml has dev, large and ci targets',
      all(f'    {t}:' in (project / 'profiles.yml').read_text() for t in ('dev', 'large', 'ci')), True)
import re
check('every password in profiles.yml comes from the environment',
      all('env_var' in l for l in (project / 'profiles.yml').read_text().splitlines() if re.match(r'\s*password:', l)), True)
check('no .env file in the companion project', (project / '.env').exists(), False)
print(f'ch32_check.py: {ok} checks passed')
