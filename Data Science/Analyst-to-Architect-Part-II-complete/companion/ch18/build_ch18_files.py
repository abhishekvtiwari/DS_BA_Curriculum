"""
Analyst to Architect — Chapter 18: Python for Analysts (pandas & Automation)
build_ch18_files.py — builds the few extra files this chapter needs.

Run from this folder:  python3 build_ch18_files.py    (needs pandas + pyarrow; reads ../full/*.parquet)
Creates:
  api_response.json      a sample API payload (two pages of orders), for the requests section
  report_template.md     the Markdown skeleton the automation writes into
The chapter also reads ../full/*.parquet and *.csv, ../ch14/orders_q4_2025_export.csv and ../ch17/sales_exports/.
Riverstone Supplies is fictional; every name and number is invented.
"""
import json, pathlib, pandas as pd
HERE = pathlib.Path(__file__).resolve().parent
FULL = HERE.parent / "full"
O = pd.read_parquet(FULL / "orders.parquet"); I = pd.read_parquet(FULL / "order_items.parquet")
lines = I.merge(O, on="order_id")
lines = lines[(lines.order_date >= "2025-12-01") & (lines.order_date <= "2025-12-03")].head(8)
payload = {
    "page": 1, "pages": 2, "count": 8,
    "results": [
        {"order_id": int(r.order_id), "order_date": r.order_date.strftime("%Y-%m-%d"),
         "customer_id": int(r.customer_id), "product_id": int(r.product_id),
         "quantity": int(r.quantity), "unit_price": float(r.unit_price),
         "discount_pct": float(r.discount_pct), "status": r.status}
        for r in lines.itertuples()
    ],
}
(HERE / "api_response.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
(HERE / "report_template.md").write_text(
    "# Riverstone monthly sales report\n\n_Month: {month}_  ·  _Generated: {generated}_\n\n"
    "## Headlines\n\n{headlines}\n\n## Revenue by region\n\n{region_table}\n\n## Data quality\n\n{quality}\n",
    encoding="utf-8")
print("wrote api_response.json and report_template.md")
