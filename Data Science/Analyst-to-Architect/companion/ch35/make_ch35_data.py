"""
Analyst to Architect · Chapter 35 · The Math Under the Models
make_ch35_data.py: builds the three small CSV files the chapter's Python examples read.

Run:     python3 make_ch35_data.py          (from companion/ch35/; needs ../generate_riverstone_2025.py)
Writes:  customers_2025.csv, orders_2025.csv, leads_2025.csv
Source:  the one-year Riverstone database (riverstone_2025), rebuilt in memory from its seeded
         generator (seed 20251), so the numbers match Chapter 13's queries exactly.
Tested:  Python 3.12.3, pandas 3.0.2 (16 September 2026)

Riverstone Supplies is fictional; every name and number is invented.
"""
import os, pathlib, tempfile
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
GEN = HERE.parent / "generate_riverstone_2025.py"

ns = {}
old = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:          # the generator also writes its SQL file; keep it out of the way
    os.chdir(tmp)
    exec(compile(GEN.read_text(encoding="utf-8"), str(GEN), "exec"), ns)
    os.chdir(old)

customers = pd.DataFrame([c[:5] for c in ns["customers"]],
                         columns=["customer_id", "customer_name", "city", "segment", "signup_date"])
products = pd.DataFrame(ns["products"], columns=["product_id", "product_name", "category", "list_price", "unit_cost"])
orders = pd.DataFrame(ns["new_orders"], columns=["order_id", "customer_id", "order_date", "status", "sales_rep_id"])
items = pd.DataFrame(ns["items"], columns=["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct"])
leads = pd.DataFrame(ns["leads"], columns=["lead_id", "created_at", "company_name", "email", "source", "owner_id"])
history = pd.DataFrame(ns["hist"], columns=["lead_id", "stage", "entered_at"])

# sales_lines: one row per non-cancelled order line, as in Chapter 13
lines = (items.merge(orders, on="order_id")
              .merge(products[["product_id", "category"]], on="product_id"))
lines = lines[lines["status"] != "Cancelled"].copy()
lines["gross"] = lines["quantity"] * lines["unit_price"]
lines["net_revenue"] = lines["gross"] * (1 - lines["discount_pct"] / 100)

# orders_2025.csv: one row per non-cancelled order
order_values = (lines.groupby(["order_id", "customer_id", "order_date"], as_index=False)
                     .agg(order_value=("net_revenue", "sum")))
order_values["order_value"] = order_values["order_value"].round(2)
order_values.to_csv(HERE / "orders_2025.csv", index=False)

# customers_2025.csv: one row per customer who ordered in 2025
per_cust = lines.groupby("customer_id").agg(orders=("order_id", "nunique"),
                                            revenue=("net_revenue", "sum"),
                                            units=("quantity", "sum"),
                                            gross=("gross", "sum"))
per_cust["avg_order_value"] = per_cust["revenue"] / per_cust["orders"]
per_cust["avg_discount_pct"] = 100 * (1 - per_cust["revenue"] / per_cust["gross"])
mix = lines.pivot_table(index="customer_id", columns="category", values="net_revenue", aggfunc="sum", fill_value=0)
for cat in ["Storage", "Kitchen", "Industrial", "Furniture"]:
    per_cust[cat.lower() + "_share"] = (mix[cat] / mix.sum(axis=1)).round(3)
out = customers[["customer_id", "customer_name", "segment"]].merge(per_cust.reset_index(), on="customer_id")
out["revenue"] = out["revenue"].round(0).astype(int)
out["avg_order_value"] = out["avg_order_value"].round(0).astype(int)
out["avg_discount_pct"] = out["avg_discount_pct"].round(2)
out = out.drop(columns="gross")
out.to_csv(HERE / "customers_2025.csv", index=False)

# leads_2025.csv: one row per real enquiry (duplicates removed: earliest record per email), won = 1 or 0
first = leads.sort_values(["email", "created_at"]).drop_duplicates("email")
won_ids = set(history.loc[history["stage"] == "Won", "lead_id"])
first = first.assign(won=first["lead_id"].isin(won_ids).astype(int)).sort_values("lead_id")
first[["lead_id", "company_name", "source", "won"]].to_csv(HERE / "leads_2025.csv", index=False)

print(len(out), "customers ·", len(order_values), "orders ·", len(first), "unique leads")
