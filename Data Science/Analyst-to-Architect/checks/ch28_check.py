#!/usr/bin/env python3
"""ch28_check.py - checks the numbers quoted in Chapter 28's prose: arithmetic, percentages, reconciliations
(against riverstone_2025 in PostgreSQL) and ratios of the recorded timings in ch28_perf_log.txt."""
import re, subprocess
ok = 0
def check(label, got, want, tol=0.05):
    global ok
    assert abs(got - want) <= tol, f'{label}: got {got}, want {want}'
    ok += 1
def q(sql):
    return subprocess.run(['su', 'postgres', '-c', 'psql -X -At -d riverstone_2025'], input=sql,
                          capture_output=True, text=True, cwd='/tmp').stdout.strip()

# 28.2 bill of materials
chair = 2.2*110 + 0.08*260 + 3.4*95 + 3*14 + 2 + 18
check('chair material cost', chair, 647.80, 0.001)
check('materials share of 850', 100*chair/850, 76.2)
check('steel share of materials', 100*323/chair, 49.9)
check('10% steel rise', 0.1*3.4*95, 32.30, 0.001); check('10% PP rise', 0.1*2.2*110, 24.20, 0.001)
check('box 25L', 1.5*110 + 0.055*260 + 2 + 18, 199.30, 0.001)
check('PP for plan', 500*2.2 + 1000*0.75, 1850, 0.001)
team = int(q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE sales_rep_id IN (3,4,5)"))
total = int(q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines"))
check('team revenue', team, 1494001+1489073+1147895, 1); check('total', total, 4335471, 0)
check('no-rep revenue', total - team, 204502, 1)
check('no-rep revenue direct', int(q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE sales_rep_id IS NULL")), 204502, 1)
# 28.3 frames and quartiles
check('last 3 rows 26 Nov', 2731+10213+10060, 23004, 0); check('last 7 days 26 Nov', 86615+2731+10213+10060, 109619, 0)
check('avg other Q3', (232692+329282)/2, 280987, 0.5)
check('quartile orders', 44+43+43+43, 173, 0); check('quartile revenue', 307338+716217+1196060+2115857, 4335472, 0)
check('top quartile share', 100*2115857/4335471, 48.8); check('bottom quartile share', 100*307338/4335471, 7.1)
# 28.4-28.6 timings (medians in the log)
import os
log = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'companion', 'ch28', 'ch28_perf_log.txt')).read()
med = {k: float(v) for k, v in re.findall(r'^(\w+): ([\d.]+)$', log.split('===== SUMMARY =====')[1], re.M)}
check('index speed-up ~200x', med['p1_seq']/med['p1_idx'], 215, 5)
check('EXTRACT vs range ~45x', med['p4_fn']/med['p4_range'], 44.5, 0.5)
check('writes 5.5x slower', med['w4']/med['w0'], 5.5, 0.1)
check('delivered share', 100*689050/714285, 96.5)
check('pages in orders', 41*1024/8, 5248, 0); check('heap blocks 4534 of 5221', 5170/5221*100, 99.0, 0.1)
check('rows removed composite', 23526-9301, 14225, 0)
dash_before = med['p3b_seq'] + med['p4_fn'] + med['p7_seq'] + med['p9_live']
dash_after = med['p3b_idx'] + med['p4_range'] + med['p7_partial'] + med['p9_mv']
check('dashboard before', dash_before, 3064, 1); check('trend share', 100*med['p9_live']/dash_before, 85.7)
check('dashboard after under 5 ms', dash_after, 4.44, 0.01)
check('hash join remainder', 285.266-142.289, 143, 0.5)
# 28.7 normalization
check('order sheet revenue', 2900 + 20900 + 15*430*0.95 + 25*750*0.95 + 45*430 + 20*750 + 20*290 + 30*430 + 25*750 + 25*380, 129040, 0.001)
# 28.8 grain
check('fan-out target', 15*300000, 4500000, 0)
check('Jan lines', int(q("SELECT COUNT(*) FROM sales_lines WHERE order_date < '2025-02-01'")), 15, 0)
check('Jan pct', 100*202640/300000, 67.5)
# 28.9-28.10 star and SCD
check('Q4 revenue', 435551+562000+756751, 1754302, 0); check('Q4 share', 100*1754302/4335471, 40.5)
patel_before = int(q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE customer_id = 2 AND order_date < '2025-04-01'"))
harbour_retail = int(q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE customer_id = 11 AND order_date < '2025-09-01'"))
check('Patel before April', patel_before, 38038, 1); check('Harbour as Retail', harbour_retail, 122880, 1)
check('segment difference', patel_before - harbour_retail, -84842, 1)
check('SCD2 trap total', 90000+18000+90000, 198000, 0); check('SCD2 true total', 42000+12500+35500+18000, 108000, 0)
check('Sharma both versions', 42000+12500+35500, 90000, 0)
metro = int(q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE customer_id = 5 AND order_date < '2025-07-01'"))
check('Metro Mart in Thane', metro, 152040, 1); check('Mumbai difference', 1080800-928760, 152040, 0)
check('Q4 from star equals view', int(q("SELECT ROUND(SUM(net_revenue)) FROM sales_lines WHERE order_date >= '2025-10-01'")), 1754302, 1)
print(f'ch28_check.py: {ok} checks passed')

# every QUERY PLAN / MySQL tree printed in the chapter must appear, line for line, in the recorded log
md = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'manuscript',
                       'ch28-advanced-sql-performance-and-data-modeling.md')).read()
norm = lambda t: [re.sub(r'\s+', ' ', l).strip() for l in t.strip().splitlines() if l.strip() and not re.fullmatch(r'[-\s]+', l)]
logn = '\n'.join(norm(log))
plans = [b for lang, b in re.findall(r'^```(\w*)\n(.*?)^```$', md, re.S | re.M) if not lang and ('QUERY PLAN' in b or b.startswith('-> '))]
for b in plans:
    assert '\n'.join(norm(b)) in logn, 'plan not in log:\n' + b[:300]
    ok += 1
print(f'ch28_check.py: {ok} checks passed, including {len(plans)} plans found in the log')
