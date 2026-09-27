"""Analyst to Architect, Chapter 14 — the same cleaning pipeline in pandas (a preview of Chapter 18).
Run from companion/ch14:  python3 clean_orders_pandas.py
Writes clean_order_lines_pandas.csv and dq_order_issues_pandas.csv. Needs pandas 2+.
Riverstone Supplies is fictional; every name and number is invented."""
import pandas as pd

raw = pd.read_csv("orders_q4_2025_export.csv", dtype=str, keep_default_na=False)   # 1. everything as text
print("rows read:", len(raw))

df = raw[raw["order_item_id"].str.fullmatch(r"\d+")]                               # 2. drop headers and footer
df = df.drop_duplicates()                                                          # 3. exact duplicates
print("data rows:", len(df))

# 4. dates: parse each known format separately; anything else stays missing (NaT)
d = df["order_date"]
parsed = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
for pattern, fmt in [(r"\d{2}-\d{2}-\d{4}", "%d-%m-%Y"), (r"\d{2}/\d{2}/\d{4}", "%d/%m/%Y"), (r"\d{4}-\d{2}-\d{2}", "%Y-%m-%d")]:
    mask = d.str.fullmatch(pattern)
    parsed[mask] = pd.to_datetime(d[mask], format=fmt, errors="coerce")
serial = d.str.fullmatch(r"\d{5}")
parsed[serial] = pd.Timestamp("1899-12-30") + pd.to_timedelta(d[serial].astype(int), unit="D")
entered_ist = (pd.to_datetime(df["entered_at_utc"], utc=True).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None))
date_repaired = parsed.isna()
parsed = parsed.fillna(entered_ist.dt.normalize())

# 5. numbers stored as text
price = pd.to_numeric(df["unit_price"].str.replace(r"^[^0-9]+", "", regex=True).str.replace(",", ""))
disc = pd.to_numeric(df["discount_pct"])
disc = disc.where(~disc.between(0, 1, inclusive="neither"), disc * 100)
qty = pd.to_numeric(df["quantity"].replace("", None)) * df["qty_unit"].map({"CTN": 10}).fillna(1)
price_to_product = {430: 101, 750: 102, 115: 103, 620: 104, 1400: 105, 1150: 106, 380: 107, 290: 108}
product = pd.to_numeric(df["product_id"].replace("", None)).fillna(price.map(price_to_product))

# 6. categories through mapping tables
status_map = {"delivered": "Delivered", "dlvd": "Delivered", "cancelled": "Cancelled", "canceled": "Cancelled", "cxl": "Cancelled",
              "shipped": "Shipped", "pending": "Pending"}
branch_map = {"mumbai ho": "Mumbai HO", "mumbai h.o.": "Mumbai HO", "mumbai": "Mumbai HO", "bengaluru": "Bengaluru", "bangalore": "Bengaluru",
              "blr": "Bengaluru", "delhi": "Delhi", "new delhi": "Delhi", "del": "Delhi", "kolkata": "Kolkata", "calcutta": "Kolkata", "kol": "Kolkata"}

clean = pd.DataFrame({
    "order_item_id": df["order_item_id"].astype(int),
    "order_id": df["order_id"].astype(int),
    "order_date": parsed.dt.date,
    "date_repaired": date_repaired,
    "customer_code": df["customer_code"].str.strip().str.zfill(4),
    "product_id": product.astype("Int64"),
    "product_repaired": df["product_id"].eq(""),
    "quantity": qty.astype("Int64"),
    "unit_price": price,
    "discount_pct": disc,
    "status": df["status"].str.strip().str.lower().map(status_map),
    "sales_rep": df["sales_rep"].str.strip().replace("", None),
    "branch": df["branch"].str.strip().str.lower().map(branch_map),
    "entered_at_ist": entered_ist,
})

# 7. validation: every mapped column must be filled
unmapped = clean[["status", "branch"]].isna().sum()
assert unmapped.sum() == 0, f"unmapped values: {unmapped.to_dict()}"

# 8. quarantine and repair log
hist_max = 90   # highest quantity on any order line before Q4 2025 (checked in SQL, section 14.6)
issues = pd.concat([
    clean.loc[clean.quantity.isna(), ["order_item_id"]].assign(issue="quantity missing", action="quarantined"),
    clean.loc[clean.quantity > hist_max, ["order_item_id"]].assign(issue="quantity above historical maximum", action="quarantined"),
    clean.loc[clean.date_repaired, ["order_item_id"]].assign(issue="impossible or unreadable date", action="repaired from entry time (IST)"),
    clean.loc[clean.product_repaired, ["order_item_id"]].assign(issue="product_id missing", action="repaired from unit price"),
])
clean.to_csv("clean_order_lines_pandas.csv", index=False)
issues.sort_values(["order_item_id", "issue"]).to_csv("dq_order_issues_pandas.csv", index=False)

ok = clean[(clean.status != "Cancelled") & ~clean.order_item_id.isin(issues.loc[issues.action == "quarantined", "order_item_id"])]
print("clean rows:", len(clean), "| issues:", issues.issue.value_counts().to_dict())
print("net revenue, non-cancelled, excluding quarantined:", round((ok.quantity * ok.unit_price * (1 - ok.discount_pct / 100)).sum(), 2))
