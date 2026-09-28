# monthly_report.py - Riverstone's monthly sales report, as a first working script.
# Analyst to Architect · Chapter 29 · the "before" version: it works, and it has every problem section 29.1 lists.
# How: python3 monthly_report.py   (needs riverstone_2025 in PostgreSQL, pandas, openpyxl, SQLAlchemy, psycopg)
# Tested on: Python 3.14.7, pandas 3.0.6, openpyxl 3.1.5, SQLAlchemy 2.1.1, psycopg 3.3.6, PostgreSQL 16.
# Riverstone Supplies is fictional; every name and number is invented.
import pandas as pd
from sqlalchemy import create_engine

conn = create_engine("postgresql+psycopg://postgres:riverstone123@localhost/riverstone_2025")
month = "2025-12"

df = pd.read_sql("SELECT sl.*, c.customer_name, p.category AS cat FROM sales_lines sl "
                 "JOIN customers c ON c.customer_id = sl.customer_id "
                 "JOIN products p ON p.product_id = sl.product_id", conn)
df["order_date"] = pd.to_datetime(df["order_date"])
df = df[df["order_date"].dt.strftime("%Y-%m") == month]

total = df["net_revenue"].astype(float).sum()
orders = df["order_id"].nunique()
print("Revenue:", total)
print("Orders:", orders)

try:
    t = pd.read_sql("SELECT target_revenue FROM sales_targets WHERE target_month = '" + month + "-01'", conn)
    target = float(t.iloc[0, 0])
except:
    target = 0

cats = df.groupby("cat")["net_revenue"].sum().astype(float).reset_index()
cats["share"] = cats["net_revenue"] / total
cats = cats.sort_values("net_revenue", ascending=False)

top = df.groupby("customer_name")["net_revenue"].sum().astype(float).sort_values(ascending=False).head(5).reset_index()

with pd.ExcelWriter("Monthly_Report_Dec_FINAL.xlsx") as w:
    pd.DataFrame({"metric": ["Revenue", "Orders", "Target", "% of target"],
                  "value": [total, orders, target, total / target * 100]}).to_excel(w, sheet_name="Summary", index=False)
    cats.to_excel(w, sheet_name="Categories", index=False)
    top.to_excel(w, sheet_name="Top customers", index=False)
print("done")
