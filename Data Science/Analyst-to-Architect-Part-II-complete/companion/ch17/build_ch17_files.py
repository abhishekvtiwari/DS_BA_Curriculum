"""
Analyst to Architect — Chapter 17: Python from Zero
build_ch17_files.py — builds the small practice files this chapter reads.

Run from this folder:  python3 build_ch17_files.py     (needs pandas + pyarrow; reads ../full/*.parquet)
Creates:
  sales_exports/riverstone_2025_01.csv … _12.csv   one file per month, the 24 key accounts' 2025 order lines
  sales_exports/README.txt                          a non-CSV file, so folder code has to filter
  products.json                                     the product list as JSON
  targets_2025.csv                                  the key accounts' 2025 monthly targets (₹4,240,000 for the year)
  broken_export.csv                                 a file with a bad row, for the error-handling section
Riverstone Supplies is fictional; every name and number is invented.
"""
import json, pathlib, pandas as pd
HERE = pathlib.Path(__file__).resolve().parent
FULL = HERE.parent / "full"
OUT = HERE / "sales_exports"; OUT.mkdir(exist_ok=True)
O = pd.read_parquet(FULL / "orders.parquet"); I = pd.read_parquet(FULL / "order_items.parquet")
C = pd.read_parquet(FULL / "customers.parquet"); P = pd.read_parquet(FULL / "products.parquet")
# the 24 key accounts' own 2025 targets (from the one-year database, not the company-wide ones)

lines = (I.merge(O, on="order_id").merge(C[["customer_id", "customer_name", "city", "segment"]], on="customer_id")
           .merge(P[["product_id", "product_name"]], on="product_id"))
lines = lines[(lines.customer_id <= 24) & (lines.order_date >= "2025-01-01")].copy()
lines["net_revenue"] = (lines.quantity * lines.unit_price * (1 - lines.discount_pct / 100)).round(2)
cols = ["order_id", "order_date", "customer_name", "city", "segment", "product_name", "quantity", "unit_price", "discount_pct", "status", "net_revenue"]
for month, part in lines.groupby(lines.order_date.dt.month):
    part.sort_values(["order_date", "order_id", "product_name"])[cols].to_csv(
        OUT / f"riverstone_2025_{month:02d}.csv", index=False, date_format="%Y-%m-%d")
(OUT / "README.txt").write_text("Monthly order-line exports for Riverstone's 24 key accounts, 2025.\nOne row per order line. Amounts in rupees.\n", encoding="utf-8")
(HERE / "products.json").write_text(json.dumps(
    [{"product_id": int(r.product_id), "name": r.product_name, "category": r.category,
      "unit_price": float(r.unit_price), "unit_cost": float(r.unit_cost)} for r in P.itertuples()], indent=2), encoding="utf-8")
import os, runpy, tempfile
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp); one = runpy.run_path(str(HERE.parent / "generate_riverstone_2025.py")); os.chdir(cwd)
pd.DataFrame([(m.strftime("%Y-%m"), t) for m, t in one["targets"]], columns=["target_month", "target_revenue"]).to_csv(HERE / "targets_2025.csv", index=False)
broken = (OUT / "riverstone_2025_03.csv").read_text(encoding="utf-8").splitlines()
broken.insert(6, "10099,not-a-date,Metro Mart,Mumbai,Retail,Storage Box 25L,twenty,430,0,Delivered,")
(HERE / "broken_export.csv").write_text("\n".join(broken) + "\n", encoding="utf-8")
print("months:", len(list(OUT.glob('*.csv'))), "| lines:", len(lines))
