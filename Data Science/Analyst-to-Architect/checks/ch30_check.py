#!/usr/bin/env python3
"""ch30_check.py - checks the numbers quoted in Chapter 30's prose against the generated website data."""
import numpy as np, pandas as pd, pathlib, sys
from scipy import stats
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize, proportions_ztest
P = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / 'companion' / 'ch30') / 'web_data'
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    assert (abs(got - want) <= tol) if isinstance(want, (int, float)) else got == want, f'{label}: {got} != {want}'
    ok += 1
s = pd.read_csv(P / 'web_sessions.csv', parse_dates=['started_at'])
a = pd.read_csv(P / 'ab_test_assignments.csv')
e = pd.read_csv(P / 'web_events.csv')
check('sessions', len(s), 214528); check('events', len(e), 622090); check('assignments', len(a), 47286)
check('overall session rate', round(s.enquiry_submitted.mean(), 4), 0.0359)
check("mean duration", round(s.duration_seconds.mean(), 2), 96.17)
check("sd duration", round(s.duration_seconds.std(ddof=1), 2), 114.91)
v = s.groupby('visitor_id').enquiry_submitted.max()
check('visitors', len(v), 176000); check('visitor rate', round(v.mean(), 4), 0.0434)
t = s.merge(a, on='visitor_id')
day = t.started_at.dt.date
t = t[(day >= pd.Timestamp('2026-02-02').date()) & (day <= pd.Timestamp('2026-02-15').date())]
g = t.groupby(['variant', 'visitor_id']).enquiry_submitted.max().reset_index().groupby('variant').agg(
    n=('visitor_id', 'count'), k=('enquiry_submitted', 'sum'))
check('control visitors', int(g.n['control']), 24036); check('variant visitors', int(g.n['variant_b']), 23250)
check('control enquiries', int(g.k['control']), 937); check('variant enquiries', int(g.k['variant_b']), 1035)
p1, p2 = g.k['control'] / g.n['control'], g.k['variant_b'] / g.n['variant_b']
check('control rate', round(p1, 4), 0.039); check('variant rate', round(p2, 4), 0.0445)
diff = p2 - p1
se = np.sqrt(p1 * (1 - p1) / g.n['control'] + p2 * (1 - p2) / g.n['variant_b'])
check('absolute lift pp', round(100 * diff, 2), 0.55)
check('relative lift %', round(100 * diff / p1, 1), 14.2)
check('CI low pp', round(100 * (diff - 1.96 * se), 2), 0.19)
check('CI high pp', round(100 * (diff + 1.96 * se), 2), 0.91)
check('CI low rel', round(100 * (diff - 1.96 * se) / p1, 1), 4.9)
check('CI high rel', round(100 * (diff + 1.96 * se) / p1, 1), 23.4)
check('z', round(proportions_ztest([g.k['variant_b'], g.k['control']], [g.n['variant_b'], g.n['control']])[0], 3), 3.009)
check('srm p', round(stats.chisquare(g.n.to_numpy())[1], 5), 0.0003)
check('srm split', round(100 * g.n['control'] / g.n.sum(), 3), 50.831)
n80 = NormalIndPower().solve_power(effect_size=proportion_effectsize(0.044, 0.039), alpha=0.05, power=0.80)
check('sample size per group', round(n80), 24955)
check('extra enquiries a month', round(0.0055 * 3400 * 30), 561)
check('visitors a day', round(len(a) / 14), 3378)
first = t.sort_values('started_at').drop_duplicates('visitor_id')
saf = pd.crosstab(first.browser, first.variant).loc['Safari']
check('safari split', round(100 * saf['control'] / saf.sum(), 1), 53.1)
early = t[t.started_at.dt.date <= pd.Timestamp('2026-02-03').date()]
ge = early.groupby(['variant', 'visitor_id']).enquiry_submitted.max().reset_index().groupby('variant').agg(
    n=('visitor_id', 'count'), k=('enquiry_submitted', 'sum'))
lift_early = 100 * ((ge.k['variant_b'] / ge.n['variant_b']) / (ge.k['control'] / ge.n['control']) - 1)
check('early visitors', int(ge.n.sum()), 7592); check('early lift', round(lift_early), 36)
check('bonferroni n', round(NormalIndPower().solve_power(
    effect_size=proportion_effectsize(0.044, 0.039), alpha=0.05 / 3, power=0.80)), 33286)
# Numbers added or corrected in the September 2026 rewrite (findings 30.10-30.32).
check('ratio largest to median enquiry', round(s.enquiry_value.max() / s.loc[s.enquiry_submitted == 1, 'enquiry_value'].median()), 193)
check('srm one in N', round(1 / stats.chisquare(g.n.to_numpy())[1], -2), 3300)
p = g.k.sum() / g.n.sum(); sep = np.sqrt(p * (1 - p) * (1 / g.n['control'] + 1 / g.n['variant_b']))
check('pooled se', round(sep, 6), 0.001839); check('unpooled se', round(se, 6), 0.001841)
lr = np.log(p2 / p1); sel = np.sqrt(1 / g.k['control'] - 1 / g.n['control'] + 1 / g.k['variant_b'] - 1 / g.n['variant_b'])
check('log-ratio CI low', round(100 * (np.exp(lr - 1.96 * sel) - 1), 1), 4.7); check('log-ratio CI high', round(100 * (np.exp(lr + 1.96 * sel) - 1), 1), 24.5)
check('enquiries a month, low end', round((diff - 1.96 * se) * 3400 * 30, -1), 200)
check('enquiries a month, high end', round((diff + 1.96 * se) * 3400 * 30, -1), 930)
pv = t.groupby(['variant', 'visitor_id']).enquiry_submitted.max().rename('enquired').reset_index()
dev = pv.merge(first[['visitor_id', 'device']], on='visitor_id').groupby(['device', 'variant']).enquired.mean().unstack()
check('tablet lift %', round(100 * (dev.loc['tablet', 'variant_b'] / dev.loc['tablet', 'control'] - 1)), 35)
wk = first.assign(week=np.where(first.started_at < '2026-02-09', 1, 2))
wr = pv.merge(wk[['visitor_id', 'week']], on='visitor_id').groupby(['week', 'variant']).enquired.mean().unstack()
lift = 100 * (wr.variant_b / wr.control - 1)
check('week 1 lift', round(lift[1]), 22); check('week 2 lift', round(lift[2]), 5)
h = NormalIndPower().solve_power(nobs1=(3912 + 3680) / 2, alpha=0.05, power=0.80)
from scipy.optimize import brentq
mde = brentq(lambda q: 2 * np.arcsin(np.sqrt(q)) - 2 * np.arcsin(np.sqrt(0.039)) - h, 0.039, 0.2) - 0.039
check('early-test MDE pp', round(100 * mde, 1), 1.3)
saf = pd.crosstab(first.browser, first.device)
check('share of Safari on mobile', round(saf.loc['Safari', 'mobile'] / saf.loc['Safari'].sum(), 2), 0.68)
check('email share of visitors', round(100 * (v.index.isin(s.loc[s.channel == 'email', 'visitor_id'])).mean()), 7)
print(f'ch30_check.py: {ok} checks passed')
