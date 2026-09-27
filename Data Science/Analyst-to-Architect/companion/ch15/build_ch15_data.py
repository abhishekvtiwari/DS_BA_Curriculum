"""
Analyst to Architect — Chapter 15: Data Visualization Principles
build_ch15_data.py — prepares every table the chapter's charts are drawn from.

How to run (from this folder):  python3 build_ch15_data.py
Needs: Python 3.10+, pandas, pyarrow, openpyxl. Reads ../full/*.parquet (generate_riverstone_full.py, seed 20230101).
Writes: ch15_chart_data.xlsx (one sheet per chart, for building the charts yourself in Excel or Google Sheets)
        and chart_data/*.csv (the same tables). Riverstone Supplies is fictional; every number is invented.
"""
import pathlib, pandas as pd, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; FULL = HERE.parent / "full"; OUT = HERE / "chart_data"; OUT.mkdir(exist_ok=True)
C = pd.read_parquet(FULL / "customers.parquet"); P = pd.read_parquet(FULL / "products.parquet")
O = pd.read_parquet(FULL / "orders.parquet"); I = pd.read_parquet(FULL / "order_items.parquet")
T = pd.read_parquet(FULL / "sales_targets.parquet"); E = pd.read_parquet(FULL / "employees.parquet")
REGIONS = {"West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nashik", "Nagpur", "Indore", "Goa", "Vadodara", "Rajkot", "Thane", "Aurangabad"],
           "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore", "Mysuru", "Visakhapatnam", "Madurai", "Mangaluru", "Thiruvananthapuram"],
           "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh", "Udaipur", "Kanpur", "Ludhiana", "Dehradun", "Agra", "Noida", "Gurugram"],
           "East": ["Kolkata", "Bhubaneswar", "Patna", "Guwahati", "Ranchi", "Raipur"]}
region = {c: r for r, cs in REGIONS.items() for c in cs}

L = (I.merge(O, on="order_id").merge(C[["customer_id", "city", "segment"]], on="customer_id")
       .merge(P[["product_id", "product_name", "category", "unit_cost"]], on="product_id"))
L = L[L.status != "Cancelled"].copy()
L["net_revenue"] = L.quantity * L.unit_price * (1 - L.discount_pct / 100)
L["cost"] = L.quantity * L.unit_cost
L["year"] = L.order_date.dt.year; L["month"] = L.order_date.dt.month
L["region"] = L.city.map(region).fillna("Unknown")
tables = {}

# 1. revenue by segment, 2025
seg = L[L.year == 2025].groupby("segment").net_revenue.sum().sort_values(ascending=False)
tables["segment_2025"] = pd.DataFrame({"segment": seg.index, "net_revenue": seg.round(0).values, "share_pct": (seg / seg.sum() * 100).round(1).values})
# 2. monthly revenue and target, 2023–2025
mon = L.groupby(["year", "month"]).net_revenue.sum().reset_index()
mon["target_revenue"] = T.sort_values("target_month").target_revenue.values
mon["attainment_pct"] = (mon.net_revenue / mon.target_revenue * 100).round(1)
mon["net_revenue"] = mon.net_revenue.round(0)
tables["monthly_2023_2025"] = mon
# 3. order values, 2025 (one row per non-cancelled order)
ov = L[L.year == 2025].groupby(["order_id", "segment"]).net_revenue.sum().reset_index().rename(columns={"net_revenue": "order_value"})
tables["order_values_2025"] = ov
q = ov.groupby("segment").order_value.describe(percentiles=[.25, .5, .75]).round(0)
tables["order_value_summary_2025"] = q.reset_index()
# 4. customers 2025: orders vs revenue
cu = L[L.year == 2025].groupby(["customer_id", "segment"]).agg(orders=("order_id", "nunique"), net_revenue=("net_revenue", "sum")).reset_index()
cu["net_revenue"] = cu.net_revenue.round(0)
tables["customers_2025"] = cu
# 5. bridge 2024 -> 2025 by segment
yb = L[L.year.isin([2024, 2025])].groupby(["segment", "year"]).net_revenue.sum().unstack().round(0)
tables["bridge_2024_2025"] = yb.reset_index().assign(change=lambda d: d[2025] - d[2024])
# 6. month x region 2025
hm = L[L.year == 2025].pivot_table(index="region", columns="month", values="net_revenue", aggfunc="sum").round(0)
tables["region_month_2025"] = hm.reset_index()
# 7. product category by month 2025
cat = L[L.year == 2025].pivot_table(index="month", columns="category", values="net_revenue", aggfunc="sum").round(0)
tables["category_month_2025"] = cat.reset_index()
# 8. top cities 2025
city = L[L.year == 2025].assign(city=lambda d: d.city.fillna("(city missing)")).groupby("city").net_revenue.sum().sort_values(ascending=False).round(0)
tables["city_2025"] = city.reset_index()
# 9. region totals 2025 and gross margin by year
tables["region_2025"] = L[L.year == 2025].groupby("region").net_revenue.sum().round(0).sort_values(ascending=False).reset_index()
gm = L.groupby("year").agg(net_revenue=("net_revenue", "sum"), cost=("cost", "sum"))
gm["gross_margin_pct"] = ((1 - gm.cost / gm.net_revenue) * 100).round(1)
tables["margin_by_year"] = gm.round({"net_revenue": 0, "cost": 0}).reset_index()
# 10. rep revenue by month 2025
L2 = L.merge(E[["employee_id", "employee_name"]], left_on="sales_rep_id", right_on="employee_id", how="left")
tables["rep_month_2025"] = L2[L2.year == 2025].pivot_table(index="month", columns="employee_name", values="net_revenue", aggfunc="sum").round(0).reset_index()
tables["product_2025"] = L[L.year == 2025].groupby("product_name").net_revenue.sum().round(0).sort_values(ascending=False).reset_index()
# 11. Anscombe's quartet (Anscombe, 1973)
x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
tables["anscombe"] = pd.DataFrame({
    "x_1_2_3": x, "y1": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68],
    "y2": [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74],
    "y3": [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73],
    "x4": [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], "y4": [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]})

with pd.ExcelWriter(HERE / "ch15_chart_data.xlsx") as xw:
    for n, df in tables.items():
        df.to_csv(OUT / f"{n}.csv", index=False)
        df.to_excel(xw, sheet_name=n[:31], index=False)
print("tables:", len(tables))
