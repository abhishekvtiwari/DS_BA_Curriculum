#!/usr/bin/env python3
"""ch31_check.py - checks the numbers quoted in Chapter 31 against the generated datasets and the true effects."""
import numpy as np, pandas as pd, pathlib, sys
import statsmodels.formula.api as smf
from scipy.optimize import minimize
D = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1] / 'companion' / 'ch31') / 'causal_data'
ok = 0
def check(label, got, want, tol=0.0):
    global ok
    assert abs(got - want) <= tol, f'{label}: {got} != {want}'
    ok += 1
panel = pd.read_csv(D / 'region_month.csv', parse_dates=['month'])
qbr = pd.read_csv(D / 'qbr_program.csv')
orders = pd.read_csv(D / 'delivery_threshold.csv')
check('region-months', len(panel), 96); check('accounts', len(qbr), 240)
check('in programme', int(qbr.in_qbr_program.sum()), 68); check('orders', len(orders), 60000)
panel['log_orders'] = np.log(panel.orders); panel['treated'] = (panel.region == 'North').astype(int)
north = panel[panel.region == 'North']
check('naive before/after %', round(100 * (north[north.is_after == 1].orders.mean() /
                                           north[north.is_after == 0].orders.mean() - 1), 1), 1.7)
post = panel[panel.is_after == 1]
check('naive cross-section %', round(100 * (post[post.region == 'North'].orders.mean() /
                                            post[post.region != 'North'].orders.mean() - 1), 1), -23.0)
cells = panel.pivot_table(index='treated', columns='is_after', values='log_orders')
did = (cells.loc[1, 1] - cells.loc[1, 0]) - (cells.loc[0, 1] - cells.loc[0, 0])
check('DiD log', round(did, 4), -0.0729, 0.0001)
check('DiD %', round(100 * (np.exp(did) - 1), 1), -7.0)
fe = smf.ols('log_orders ~ treated:is_after + C(region) + C(month)', data=panel).fit()
lo, hi = fe.conf_int().loc['treated:is_after']
check('FE effect', round(fe.params['treated:is_after'], 4), -0.0729, 0.0001)
check('FE CI low %', round(100 * (np.exp(lo) - 1), 1), -10.1); check('FE CI high %', round(100 * (np.exp(hi) - 1), 1), -3.9)
check('true effect %', round(100 * (0.92 - 1), 1), -8.0)
qbr['log_2025'] = np.log(qbr.revenue_2025); qbr['log_2024'] = np.log(qbr.revenue_2024)
gap = qbr.groupby('in_qbr_program').log_2025.mean().diff().iloc[-1]
check('naive QBR %', round(100 * (np.exp(gap) - 1), 1), 75.0)
adj = smf.ols('log_2025 ~ in_qbr_program + log_2024 + growth_2024 + years_as_customer + C(segment)', data=qbr).fit()
check('adjusted QBR %', round(100 * (np.exp(adj.params['in_qbr_program']) - 1), 1), 7.5)
lo, hi = adj.conf_int().loc['in_qbr_program']
check('adjusted CI low %', round(100 * (np.exp(lo) - 1), 1), 4.4); check('adjusted CI high %', round(100 * (np.exp(hi) - 1), 1), 10.7)
check('selection share %', round(100 * (1 - round(100 * (np.exp(adj.params['in_qbr_program']) - 1), 1) / 75.0)), 90)
nosize = smf.ols('log_2025 ~ in_qbr_program + growth_2024 + years_as_customer + C(segment)', data=qbr).fit()
check('without size %', round(100 * (np.exp(nosize.params['in_qbr_program']) - 1), 1), 75.1)
nogrowth = smf.ols('log_2025 ~ in_qbr_program + log_2024 + years_as_customer + C(segment)', data=qbr).fit()
check('without growth %', round(100 * (np.exp(nogrowth.params['in_qbr_program']) - 1), 1), 8.7)
check('arithmetic 2025 ratio %', round(100 * (qbr.groupby('in_qbr_program').revenue_2025.mean().iloc[1] /
                                             qbr.groupby('in_qbr_program').revenue_2025.mean().iloc[0] - 1)), 72)
check('QBR size ratio', round(qbr.groupby('in_qbr_program').revenue_2024.mean().iloc[1] /
                              qbr.groupby('in_qbr_program').revenue_2024.mean().iloc[0], 2), 1.62)
orders['centred'] = (orders.order_value - 25000) / 1000
wide = orders[orders.centred.abs() <= 5]
rd = smf.ols('repeat_within_90_days ~ free_delivery + centred + free_delivery:centred', data=wide).fit()
check('RD jump pts', round(100 * rd.params['free_delivery'], 1), 7.3)
check('RD orders', len(wide), 46054)
near = orders[orders.centred.abs() <= 1]
check('bunching ratio', round((near.centred >= 0).sum() / (near.centred < 0).sum(), 3), 0.999, 0.002)
wp = panel.pivot_table(index='month', columns='region', values='log_orders')
pre = wp[wp.index < '2025-10-01']; donors = ['West', 'South', 'East']
best = minimize(lambda w: float(np.mean((pre['North'].to_numpy() - pre[donors].to_numpy() @ w) ** 2)),
                np.repeat(1 / 3, 3), bounds=[(0, 1)] * 3,
                constraints=[{'type': 'eq', 'fun': lambda w: w.sum() - 1}], method='SLSQP')
synth = wp[donors].to_numpy() @ best.x
gap_after = (wp['North'].to_numpy() - synth)[wp.index >= '2025-10-01'].mean()
check('synthetic gap %', round(100 * (np.exp(gap_after) - 1), 1), -6.6, 0.1)
check('synthetic weight East', round(best.x[2], 2), 0.51, 0.01)
# section 31.0 and the story's arithmetic
check('log diff 2032->2067', round(np.log(2067) - np.log(2032), 4), 0.0171)
check('exp(0.56)-1 %', round(100 * (np.exp(0.56) - 1), 1), 75.1)
check('ln(1.08)', round(np.log(1.08), 3), 0.077)
check('equal-weight loss', round(float(np.mean((pre['North'] - pre[donors].mean(axis=1)) ** 2)), 4), 0.0192)
check('South+East loss', round(float(np.mean((pre['North'] - (pre['South'] + pre['East']) / 2) ** 2)), 4), 0.0044)
vol = np.exp(fe.params['treated:is_after'])
check('price-only revenue %', round(100 * (0.93 * 1.06 - 1), 1), -1.4)
check('gross profit change % at 26.2% margin', round(100 * (vol * (1.06 - 0.738) / 0.262 - 1)), 14)
tr = smf.ols('log_orders ~ treated:is_after + C(region) + C(month) + treated:t',
             data=panel.assign(t=(panel.month.dt.year - 2024) * 12 + panel.month.dt.month)).fit()
check('North-trend effect %', round(100 * (np.exp(tr.params['treated:is_after']) - 1), 1), -4.8)
print(f'ch31_check.py: {ok} checks passed')
