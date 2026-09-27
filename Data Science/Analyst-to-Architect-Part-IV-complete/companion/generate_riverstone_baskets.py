"""
Analyst to Architect · Riverstone order baskets (first used in Chapter 38; reused in Chapter 42)
generate_riverstone_baskets.py: one row per order line for 2025, so a basket is one order.

Run:     python3 generate_riverstone_baskets.py      (writes into companion/baskets/)
Writes:  baskets/order_lines.csv, baskets/products.csv
Seed:    20238
Tested:  Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (18 September 2026)
Spec:    planning/data/riverstone-baskets.md

Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd

rng = np.random.default_rng(20238)
OUT = pathlib.Path(__file__).resolve().parent / "baskets"
OUT.mkdir(exist_ok=True)

products = [
    ("P01", "Storage Crate 50L", "Storage", 620), ("P02", "Storage Crate 80L", "Storage", 840),
    ("P03", "Crate Lid (50L)", "Storage", 145), ("P04", "Crate Lid (80L)", "Storage", 180),
    ("P05", "Stacking Bin Small", "Storage", 210), ("P06", "Stacking Bin Large", "Storage", 330),
    ("P07", "Food Container 2L", "Kitchen", 95), ("P08", "Food Container 5L", "Kitchen", 150),
    ("P09", "Airtight Seal Pack", "Kitchen", 60), ("P10", "Serving Tray", "Kitchen", 240),
    ("P11", "Chopping Board", "Kitchen", 320), ("P12", "Insulated Jug 5L", "Kitchen", 780),
    ("P13", "Industrial Crate 200L", "Industrial", 2450), ("P14", "Pallet Box", "Industrial", 3900),
    ("P15", "Crate Trolley", "Industrial", 4600), ("P16", "Dolly Wheels (set)", "Industrial", 950),
    ("P17", "Drum 60L", "Industrial", 1650), ("P18", "Drum Tap Fitting", "Industrial", 260),
    ("P19", "Garden Chair", "Furniture", 1100), ("P20", "Garden Table", "Furniture", 2600),
    ("P21", "Chair Cushion Set", "Furniture", 450), ("P22", "Folding Stool", "Furniture", 690),
    ("P23", "Shelf Unit 4-Tier", "Furniture", 1850), ("P24", "Shoe Rack", "Furniture", 980),
]
prod = pd.DataFrame(products, columns=["product_id", "product_name", "category", "unit_price"])
prod.to_csv(OUT / "products.csv", index=False)
ids = prod["product_id"].to_numpy()
cat_of = dict(zip(prod["product_id"], prod["category"]))

# how often each product is the first thing in a basket, by segment
base_pop = {"Retail": {"Storage": 0.40, "Kitchen": 0.35, "Industrial": 0.05, "Furniture": 0.20},
            "Hospitality": {"Storage": 0.20, "Kitchen": 0.62, "Industrial": 0.03, "Furniture": 0.15},
            "Wholesale": {"Storage": 0.33, "Kitchen": 0.12, "Industrial": 0.50, "Furniture": 0.05}}
# planted co-purchase rules: if the basket has A, B often joins it
RULES = {"P01": [("P03", 0.62)], "P02": [("P04", 0.58)], "P07": [("P09", 0.55)], "P08": [("P09", 0.50)],
         "P13": [("P16", 0.34)], "P14": [("P16", 0.30)], "P17": [("P18", 0.66)],
         "P19": [("P21", 0.45), ("P20", 0.28)], "P20": [("P19", 0.40)], "P05": [("P06", 0.30)]}

accounts = pd.read_csv(pathlib.Path(__file__).resolve().parent / "accounts" / "accounts.csv")
accounts = accounts[accounts["churned_2025"] == 0]
rows = []
order_id = 900001
for acc_id, segment, revenue in zip(accounts["account_id"], accounts["segment"], accounts["revenue_2025"]):
    n_orders = int(np.clip(rng.poisson(max(1.0, revenue / 60_000)), 1, 40))
    weights = np.array([base_pop[segment][cat_of[p]] for p in ids])
    weights = weights / weights.sum()
    for _ in range(n_orders):
        n_lines = 1 + rng.poisson(1.3)
        basket = set(rng.choice(ids, size=min(n_lines, 6), replace=False, p=weights))
        for seed_product in list(basket):
            for partner, chance in RULES.get(seed_product, []):
                if rng.random() < chance:
                    basket.add(partner)
        date = pd.Timestamp("2025-01-01") + pd.Timedelta(days=int(rng.integers(0, 365)))
        for p in sorted(basket):
            qty = int(np.clip(rng.lognormal(np.log(12), 0.9), 1, 400))
            rows.append((order_id, acc_id, date.date().isoformat(), p, qty))
        order_id += 1

lines = pd.DataFrame(rows, columns=["order_id", "account_id", "order_date", "product_id", "quantity"])
lines.to_csv(OUT / "order_lines.csv", index=False)
print(f"{lines['order_id'].nunique():,} orders · {len(lines):,} order lines · "
      f"{lines['account_id'].nunique():,} accounts · average basket {len(lines) / lines['order_id'].nunique():.2f} lines")
