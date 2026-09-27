"""
Analyst to Architect — Chapter 22: Statistics Without Fooling Yourself
build_ch22_files.py — builds the two datasets this chapter reasons about.

Run from this folder:  python3 build_ch22_files.py     (needs pandas, numpy)
Seed 202201, so every number in the chapter is reproducible.

Creates:
  ab_test_2026.csv          an A/B test of two subject lines on Riverstone's February 2026 offer email:
                            one row per recipient, with variant, opened, ordered and order value
  transporters_q4_2025.csv  Q4 2025 deliveries split by transporter and route type, with an on-time flag
                            (built to contain a genuine Simpson's paradox, for section 22.6)

Both datasets are invented for this chapter: Riverstone's ERP has no campaign or transporter data.
Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
rng = np.random.default_rng(202201)

# ---- 1. the A/B test -------------------------------------------------------------------------
n_a, n_b = 4200, 4200
open_rate = {"A": 0.242, "B": 0.268}          # B's subject line is genuinely a little better
order_rate_given_open = {"A": 0.086, "B": 0.084}   # ... but it does not convert better
rows = []
for variant, n in (("A", n_a), ("B", n_b)):
    opened = rng.random(n) < open_rate[variant]
    ordered = opened & (rng.random(n) < order_rate_given_open[variant])
    values = np.where(ordered, np.round(rng.lognormal(np.log(18000), 0.6, n), -1), 0.0)
    rows.append(pd.DataFrame({"recipient_id": np.arange(len(rows) * 100000, len(rows) * 100000 + n) + 1,
                              "variant": variant, "opened": opened, "ordered": ordered, "order_value": values}))
ab = pd.concat(rows, ignore_index=True)
ab.to_csv(HERE / "ab_test_2026.csv", index=False)

# ---- 2. transporters, with a Simpson's paradox ------------------------------------------------
# SwiftLine handles mostly easy metro routes; BlueCart handles mostly hard upcountry routes.
plan = [("SwiftLine", "Metro", 5200, 0.94), ("SwiftLine", "Upcountry", 900, 0.71),
        ("BlueCart", "Metro", 1100, 0.96), ("BlueCart", "Upcountry", 4400, 0.75)]
parts = []
order_id = 900001
for transporter, route, n, p in plan:
    on_time = rng.random(n) < p
    parts.append(pd.DataFrame({"order_id": np.arange(order_id, order_id + n), "transporter": transporter,
                               "route": route, "on_time": on_time}))
    order_id += n
tr = pd.concat(parts, ignore_index=True).sample(frac=1, random_state=22).reset_index(drop=True)
tr.to_csv(HERE / "transporters_q4_2025.csv", index=False)

print("A/B test:", len(ab), "recipients")
print(ab.groupby("variant").agg(sent=("opened", "size"), opens=("opened", "sum"),
                                orders=("ordered", "sum"), revenue=("order_value", "sum")).round(0))
print("\nTransporters:", len(tr), "deliveries")
print(tr.groupby("transporter").on_time.mean().round(4).to_dict())
print(tr.groupby(["transporter", "route"]).on_time.agg(["size", "mean"]).round(4))
