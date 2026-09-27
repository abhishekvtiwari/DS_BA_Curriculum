"""Chapter 11, section 11.14: competition case 'Riverstone Rewards' — reference solution in pandas.
Run from the book root:  python3 checks/ch11_rewards_case.py"""
import pandas as pd, numpy as np
S = pd.read_excel("companion/ch11/ch11_practice.xlsx", sheet_name="Sales", dtype={"customer_code": str})
ok = S[S.status != "Cancelled"]
O = ok.groupby("order_id").agg(order_date=("order_date","first"), customer=("customer_name","first"),
                               value=("net_revenue","sum"), lines=("order_id","size")).reset_index().sort_values("order_id")
assert O.order_date.is_monotonic_increasing
O["month"] = O.order_date.dt.to_period("M")
A = {}
# L1
A["L1 orders"] = len(O); A["L1 orders >= 25000"] = int((O.value >= 25000).sum()); A["L1 value total"] = round(O.value.sum(), 2)
# L2 base points
O["base"] = np.floor(O.value / 100).astype(int); A["L2 total base points"] = int(O.base.sum())
top = O.groupby("customer").base.sum().sort_values(ascending=False); A["L2 top customer base"] = (top.index[0], int(top.iloc[0]))
# L3 tier from previous spend
O["prev_spend"] = O.groupby("customer").value.cumsum() - O.value
O["tier"] = np.select([O.prev_spend >= 250000, O.prev_spend >= 100000], ["Gold", "Silver"], "Standard")
O["mult"] = O.tier.map({"Standard": 1.0, "Silver": 1.25, "Gold": 1.5})
A["L3 tier counts"] = O.tier.value_counts().to_dict()
# L4 multiplied points
O["tier_pts"] = np.floor(O.base * O.mult).astype(int); A["L4 total after multipliers"] = int(O.tier_pts.sum())
# L5 streak bonus
cm = set(zip(O.customer, O.month))
O["streak"] = [(c, m - 1) in cm for c, m in zip(O.customer, O.month)]
A["L5 streak orders"] = int(O.streak.sum())
O["pts_after_streak"] = O.tier_pts + 200 * O.streak; A["L5 total after streak"] = int(O.pts_after_streak.sum())
# L6 basket bonus
O["basket"] = O.lines >= 3; A["L6 basket orders"] = int(O.basket.sum())
O["points"] = O.pts_after_streak + 100 * O.basket; A["L6 total points earned"] = int(O.points.sum())
# L7 expiry
q4 = set(O[O.order_date >= "2025-10-01"].customer)
early = O[O.order_date < "2025-07-01"].groupby("customer").points.sum()
lose = early[~early.index.isin(q4)]
A["L7 customers losing points"] = sorted(lose.index.tolist()); A["L7 expired points"] = int(lose.sum())
# L8 balances
bal = O.groupby("customer").points.sum()
bal = bal - lose.reindex(bal.index).fillna(0).astype(int)
bal = bal.sort_values(ascending=False)
A["L8 top balance"] = (bal.index[0], int(bal.iloc[0])); A["L8 customers >= 4000"] = int((bal >= 4000).sum())
A["L8 top 5"] = {k: int(v) for k, v in bal.head(5).items()}
# Bonus 1: first customer whose running earned points (before expiry) reach 5,000
O["run_pts"] = O.groupby("customer").points.cumsum()
hit = O[O.run_pts >= 5000].sort_values("order_id").iloc[0]
A["B1 first to 5000"] = (hit.customer, str(hit.order_date.date()), int(hit.order_id), int(hit.run_pts))
# Bonus 2: month with most points earned
mp = O.groupby("month").points.sum().sort_values(ascending=False); A["B2 top month"] = (str(mp.index[0]), int(mp.iloc[0]))
# Bonus 3: longest run of consecutive months with at least one order
best = (None, 0)
for c, g in O.groupby("customer"):
    ms = sorted(set(m.month for m in g.month)); run = 1; mx = 1
    for a, b in zip(ms, ms[1:]):
        run = run + 1 if b == a + 1 else 1; mx = max(mx, run)
    if mx > best[1] or (mx == best[1] and c < best[0]): best = (c, mx)
longest = {c: None for c in []}
A["B3 longest monthly streak"] = best
runs = {}
for c, g in O.groupby("customer"):
    ms = sorted(set(m.month for m in g.month)); run = 1; mx = 1
    for a, b in zip(ms, ms[1:]):
        run = run + 1 if b == a + 1 else 1; mx = max(mx, run)
    runs[c] = mx
A["B3 all with max"] = sorted([c for c, v in runs.items() if v == max(runs.values())])
# Bonus 4: rank of Metro Mart by final balance (1 = highest; ties share rank)
A["B4 Metro Mart rank"] = int(bal.rank(ascending=False, method="min")["Metro Mart"]); A["B4 Metro Mart balance"] = int(bal["Metro Mart"])
for k, v in A.items(): print(f"{k}: {v}")
print(O.head(8).to_string())
print(O[O.customer=="Sharma Hardware"][["order_id","order_date","value","base","prev_spend","tier","tier_pts","streak","basket","points","run_pts"]].to_string())
O.to_csv("/tmp/rewards_orders.csv", index=False)
