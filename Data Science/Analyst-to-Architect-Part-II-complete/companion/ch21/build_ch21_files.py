"""
Analyst to Architect — Chapter 21: Descriptive Statistics & Probability
build_ch21_files.py — builds the delivery-time data the chapter and its project need.

Run from this folder:  python3 build_ch21_files.py       (needs pandas, numpy, pyarrow)
Reads ../full/*.parquet. Seed 202101, so the numbers never move.

Creates delivery_times_2025.csv: one row per delivered 2025 order, with
  order_id, order_date, branch, customer_id, order_value, promised_days, delivery_days, on_time
Delivery lead time is invented for this chapter (the ERP data has no delivery dates): a lognormal
shape per branch, plus a small festive-season penalty in October and November, plus 1.5% of orders
that go badly wrong. Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
FULL = HERE.parent / "full"
rng = np.random.default_rng(202101)

O = pd.read_parquet(FULL / "orders.parquet")
I = pd.read_parquet(FULL / "order_items.parquet")
C = pd.read_parquet(FULL / "customers.parquet")

REGION = {}
for region, cities in {
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nashik", "Nagpur", "Indore", "Goa", "Vadodara", "Rajkot", "Thane", "Aurangabad"],
    "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore", "Mysuru", "Visakhapatnam", "Madurai", "Mangaluru", "Thiruvananthapuram"],
    "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh", "Udaipur", "Kanpur", "Ludhiana", "Dehradun", "Agra", "Noida", "Gurugram"],
    "East": ["Kolkata", "Bhubaneswar", "Patna", "Guwahati", "Ranchi", "Raipur"]}.items():
    for city in cities:
        REGION[city] = region
BRANCH = {"West": "Mumbai HO", "South": "Bengaluru", "North": "Delhi", "East": "Kolkata"}

lines = I.merge(O, on="order_id")
lines["net_revenue"] = lines.quantity * lines.unit_price * (1 - lines.discount_pct / 100)
orders = (lines[(lines.status == "Delivered") & (lines.order_date >= "2025-01-01")]
          .groupby(["order_id", "customer_id", "order_date"], as_index=False)["net_revenue"].sum()
          .rename(columns={"net_revenue": "order_value"}))
orders = orders.merge(C[["customer_id", "city"]], on="customer_id", how="left")
orders["branch"] = orders.city.map(lambda c: BRANCH.get(REGION.get(c), "Mumbai HO"))

# lead time: lognormal per branch (median days), + festive penalty, + rare failures
median_days = {"Mumbai HO": 3.0, "Bengaluru": 3.6, "Delhi": 4.2, "Kolkata": 5.4}
sigma = {"Mumbai HO": 0.30, "Bengaluru": 0.32, "Delhi": 0.36, "Kolkata": 0.45}
mu = orders.branch.map(lambda b: np.log(median_days[b])).to_numpy()
sd = orders.branch.map(lambda b: sigma[b]).to_numpy()
days = rng.lognormal(mu, sd)
festive = orders.order_date.dt.month.isin([10, 11]).to_numpy()
days = days + festive * rng.gamma(2.0, 0.55, len(orders))
failures = rng.random(len(orders)) < 0.015
days = days + failures * rng.gamma(3.0, 3.0, failures.sum() if failures.sum() == len(days) else len(days)) * failures
orders["delivery_days"] = np.round(np.clip(days, 1, None), 1)
orders["promised_days"] = orders.branch.map({"Mumbai HO": 5, "Bengaluru": 5, "Delhi": 6, "Kolkata": 7})
orders["on_time"] = orders.delivery_days <= orders.promised_days

out = orders[["order_id", "order_date", "branch", "customer_id", "order_value", "promised_days",
              "delivery_days", "on_time"]].sort_values("order_id")
out.to_csv(HERE / "delivery_times_2025.csv", index=False, date_format="%Y-%m-%d")
print(f"{len(out):,} delivered orders; median {out.delivery_days.median():.1f} days; "
      f"on time {out.on_time.mean()*100:.1f}%")
