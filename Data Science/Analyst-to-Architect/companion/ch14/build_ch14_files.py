"""
Analyst to Architect — Chapter 14: Data Cleaning & Preparation
build_ch14_files.py — builds the messy exports that Chapter 14 cleans, and an answer key.

How to run (from this folder):  python3 build_ch14_files.py
Needs: Python 3.10+, pandas, pyarrow. Reads ../full/*.parquet (generate_riverstone_full.py, seed 20230101).
Seed for the damage: 20251014. Same seed, same mess.

Creates:
  orders_q4_2025_export.csv      the ERP's Q4 2025 order-line export, with the data-entry habits of four branch sales offices (messy)
  customers_crm_export.csv       the CRM's customer list (messy)
  city_map.csv, status_map.csv, branch_map.csv   starter mapping tables, columns raw_value and clean_value
                                 (incomplete on purpose; the chapter and its exercises complete them)
  answer_key.json                every planted problem with its count, plus the true clean totals
  clean_truth_orders_q4_2025.csv the correct clean table (for checking your work only)

The truth is the full dataset itself: after cleaning, the export must reconcile to riverstone_full's Q4 2025
order lines. Riverstone Supplies is fictional; every name and number is invented.
"""
import json, random, pathlib, datetime as dt
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
FULL = HERE.parent / "full"
random.seed(20251014)

C = pd.read_parquet(FULL / "customers.parquet"); P = pd.read_parquet(FULL / "products.parquet")
E = pd.read_parquet(FULL / "employees.parquet"); O = pd.read_parquet(FULL / "orders.parquet")
I = pd.read_parquet(FULL / "order_items.parquet")

REGION = {}
for r, cs in {"West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nashik", "Nagpur", "Indore", "Goa", "Vadodara", "Rajkot", "Thane", "Aurangabad"],
              "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore", "Mysuru", "Visakhapatnam", "Madurai", "Mangaluru", "Thiruvananthapuram"],
              "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh", "Udaipur", "Kanpur", "Ludhiana", "Dehradun", "Agra", "Noida", "Gurugram"],
              "East": ["Kolkata", "Bhubaneswar", "Patna", "Guwahati", "Ranchi", "Raipur"]}.items():
    for c in cs: REGION[c] = r
BRANCH = {"West": "Mumbai HO", "South": "Bengaluru", "North": "Delhi", "East": "Kolkata", None: "Mumbai HO"}

# ---- truth: Q4 2025 order lines -------------------------------------------------------------------
t = (I.merge(O, on="order_id").merge(C[["customer_id", "city"]], on="customer_id")
       .merge(E[["employee_id", "employee_name"]], left_on="sales_rep_id", right_on="employee_id", how="left"))
t = t[t.order_date >= "2025-10-01"].sort_values(["order_date", "order_id", "order_item_id"]).reset_index(drop=True)
t["customer_code"] = t.customer_id.map(lambda v: f"{v:04d}")
t["branch"] = t.city.map(lambda c: BRANCH[REGION.get(c)])
t["sales_rep"] = t.employee_name.fillna("")
t["net_revenue"] = t.quantity * t.unit_price * (1 - t.discount_pct / 100)
# entry timestamps in UTC: order entered between 09:00 and 23:30 IST on the order date
ist = [dt.datetime.combine(d.date(), dt.time(0, 5)) + dt.timedelta(minutes=random.randint(0, 320)) if random.random() < 0.06
       else dt.datetime.combine(d.date(), dt.time(9, 0)) + dt.timedelta(minutes=random.randint(0, 870)) for d in t.order_date]
# ~6% are web-portal entries made between 00:05 and 05:25 IST, which fall on the previous day in UTC
t["entered_at_utc"] = [x - dt.timedelta(hours=5, minutes=30) for x in ist]
truth = t[["order_item_id", "order_id", "order_date", "customer_code", "product_id", "quantity", "unit_price",
           "discount_pct", "status", "sales_rep", "branch", "entered_at_utc", "net_revenue"]].copy()
truth.to_csv(HERE / "clean_truth_orders_q4_2025.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")

# ---- damage --------------------------------------------------------------------------------------
key = {}
rows = []
n = len(truth)
idx = list(range(n))
def pick(k, pool=None):
    pool = pool if pool is not None else idx
    return set(random.sample(pool, k))

kolkata = [i for i in idx if truth.at[i, "branch"] == "Kolkata"]
delhi = [i for i in idx if truth.at[i, "branch"] == "Delhi"]
others = [i for i in idx if truth.at[i, "branch"] not in ("Kolkata", "Delhi")]

dmy_slash = pick(1800, others)                        # 25/10/2025 instead of 25-10-2025
serial = pick(40, [i for i in others if i not in dmy_slash])
iso_dates = set(kolkata)                              # Kolkata's spreadsheet upload writes YYYY-MM-DD
impossible = pick(9, [i for i in others if i not in dmy_slash | serial and truth.at[i, "order_date"].day >= 28])
code_no_zero = set(kolkata)                           # Kolkata's spreadsheet upload drops leading zeros
disc_fraction = set(i for i in kolkata if truth.at[i, "discount_pct"] > 0)   # 5 -> 0.05
cartons = pick(260, delhi)                            # Delhi enters Wholesale quantities in cartons of 10 ...
cartons = set(i for i in cartons if truth.at[i, "quantity"] % 10 == 0)
money_text = pick(2300, others)                       # "₹1,400.00" or "Rs. 430"
status_variant = pick(3100)
extra_zero = pick(6, [i for i in others if i not in cartons])   # 30 -> 300 typed with an extra zero
qty_blank = pick(14, [i for i in others if i not in extra_zero])
prod_blank = pick(8, [i for i in others if i not in qty_blank | extra_zero])
rep_space = pick(900)
branch_variant = pick(1400)
dup_rows = sorted(pick(137))                          # exported twice (identical lines)
page_headers = [4000, 8000, 12000, 16000, 20000, 24000]

STATUS_VARIANTS = {"Delivered": ["delivered", "DELIVERED", "Delivered ", "Dlvd"], "Cancelled": ["Canceled", "cancelled", "CANCELLED", "Cxl"],
                   "Shipped": ["shipped", "SHIPPED", "Shipped "], "Pending": ["pending", "PENDING", "Pending "]}
BRANCH_VARIANTS = {"Mumbai HO": ["mumbai ho", "MUMBAI HO", "Mumbai H.O.", "Mumbai"], "Bengaluru": ["Bangalore", "bengaluru", "BLR"],
                   "Delhi": ["New Delhi", "delhi", "DEL"], "Kolkata": ["Calcutta", "kolkata", "KOL"]}

header = ["order_item_id", "order_id", "order_date", "customer_code", "product_id", "quantity", "qty_unit", "unit_price",
          "discount_pct", "status", "sales_rep", "branch", "entered_at_utc"]
out = []
for i in idx:
    r = truth.iloc[i]
    d = r.order_date
    if i in iso_dates: ds = d.strftime("%Y-%m-%d")
    elif i in serial: ds = str((d.date() - dt.date(1899, 12, 30)).days)
    elif i in dmy_slash: ds = d.strftime("%d/%m/%Y")
    else: ds = d.strftime("%d-%m-%Y")
    if i in impossible: ds = random.choice(["31-11-2025", "32-10-2025", "31-09-2025"])
    code = str(int(r.customer_code)) if i in code_no_zero else r.customer_code
    q = int(r.quantity); unit = "PCS"
    if i in cartons: q = q // 10; unit = "CTN"
    if i in extra_zero: q = q * 10
    qs = "" if i in qty_blank else str(q)
    price = float(r.unit_price)
    ps = (random.choice([f"₹{price:,.2f}", f"Rs. {price:,.0f}"]) if i in money_text else f"{price:.0f}")
    dsc = float(r.discount_pct)
    dstr = (f"{dsc/100:.2f}" if i in disc_fraction else f"{dsc:g}")
    st = random.choice(STATUS_VARIANTS[r.status]) if i in status_variant else r.status
    rep = (r.sales_rep + " ") if (i in rep_space and r.sales_rep) else r.sales_rep
    br = random.choice(BRANCH_VARIANTS[r.branch]) if i in branch_variant else r.branch
    pid = "" if i in prod_blank else str(int(r.product_id))
    out.append([int(r.order_item_id), int(r.order_id), ds, code, pid, qs, unit, ps, dstr, st, rep, br,
                r.entered_at_utc.strftime("%Y-%m-%dT%H:%M:%SZ")])
    if i in dup_rows: out.append(list(out[-1]))
    if i + 1 in page_headers: out.append(list(header))
lines = [header] + out + [["", "", "", "", "", "", "", "", "", "", "", "", f"Report generated 01-01-2026 02:00; rows: {len(out)}"]]
import csv
with open(HERE / "orders_q4_2025_export.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(lines)

# ---- customers CRM export ----------------------------------------------------------------------------
dupkey = pd.read_csv(FULL / "_answer_key_duplicate_customers.csv")
CITY_VARIANTS = {"Mumbai": ["Bombay", "mumbai", "MUMBAI", "Mumbai "], "Bengaluru": ["Bangalore", "bengaluru", "Bengaluru "],
                 "Gurugram": ["Gurgaon"], "Kolkata": ["Calcutta", "kolkata"], "Chennai": ["Madras", "chennai"],
                 "Thiruvananthapuram": ["Trivandrum"], "Visakhapatnam": ["Vizag"], "Mysuru": ["Mysore"], "Delhi": ["New Delhi", "delhi"],
                 "Pune": ["Poona", "pune"], "Hyderabad": ["hyderabad", "Hyderabad "]}
cc = C.copy()
cvar = set(random.sample(list(cc.index), 700))
missing_tokens = ["", "N/A", "-", "unknown", "NULL"]
seg_var = set(random.sample(list(cc.index), 450))
SEG_VARIANTS = {"Retail": ["retail", "RETAIL", "Retail "], "Hospitality": ["Hotel/Restaurant", "hospitality", "HoReCa"],
                "Wholesale": ["wholesale", "Distributor", "WHOLESALE"]}
bad_email = set(random.sample(list(cc.index), 60)); no_email = set(random.sample(list(cc.index), 150))
future_signup = set(random.sample(list(cc.index), 5)); slash_signup = set(random.sample(list(cc.index), 400))
cust_rows = []
for i, r in cc.iterrows():
    slug = "".join(ch for ch in r.customer_name.lower() if ch.isalnum())[:24]
    email = f"accounts@{slug}.example.com"
    if i in bad_email: email = email.replace("@", ".")
    if i in no_email: email = ""
    city = r.city if r.city is not None and not pd.isna(r.city) else random.choice(missing_tokens)
    if i in cvar and isinstance(r.city, str) and r.city in CITY_VARIANTS: city = random.choice(CITY_VARIANTS[r.city])
    seg = random.choice(SEG_VARIANTS[r.segment]) if i in seg_var else r.segment
    sd = r.signup_date
    sds = sd.strftime("%d/%m/%Y") if i in slash_signup else sd.strftime("%Y-%m-%d")
    if i in future_signup: sds = sd.strftime("%Y-%m-%d").replace("202", "206", 1)
    cust_rows.append([f"{int(r.customer_id):04d}", r.customer_name, city, seg, email, sds])
with open(HERE / "customers_crm_export.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["customer_code", "customer_name", "city", "segment", "email", "signup_date"]); w.writerows(cust_rows)

pd.DataFrame([("bombay", "Mumbai"), ("bangalore", "Bengaluru"), ("gurgaon", "Gurugram"), ("calcutta", "Kolkata")],
             columns=["raw_value", "clean_value"]).to_csv(HERE / "city_map.csv", index=False)
pd.DataFrame([("delivered", "Delivered"), ("dlvd", "Delivered"), ("canceled", "Cancelled"), ("cancelled", "Cancelled"),
              ("shipped", "Shipped"), ("pending", "Pending")], columns=["raw_value", "clean_value"]).to_csv(HERE / "status_map.csv", index=False)
# starter branch map (incomplete on purpose: Exercise 7 completes it to 12 rows); same columns as the SQL map_ tables
pd.DataFrame([("mumbai ho", "Mumbai HO"), ("bengaluru", "Bengaluru"), ("bangalore", "Bengaluru"), ("delhi", "Delhi"),
              ("kolkata", "Kolkata"), ("calcutta", "Kolkata")], columns=["raw_value", "clean_value"]).to_csv(HERE / "branch_map.csv", index=False)

valid = truth[truth.status != "Cancelled"]
key = {
    "orders_export": {
        "data_rows_in_file": len(out), "true_order_lines": n, "true_orders": int(truth.order_id.nunique()),
        "duplicate_rows_planted": len(dup_rows), "repeated_header_rows": len(page_headers), "footer_rows": 1,
        "dates_iso_kolkata": len(iso_dates), "dates_dd_mm_yyyy_slash": len(dmy_slash - impossible), "dates_excel_serial": len(serial),
        "dates_impossible": len(impossible), "impossible_date_rows": sorted(int(truth.at[i, "order_item_id"]) for i in impossible),
        "codes_without_leading_zeros": len(code_no_zero), "discount_as_fraction": len(disc_fraction),
        "quantity_in_cartons": len(cartons), "quantity_extra_zero": len(extra_zero),
        "extra_zero_rows": sorted(int(truth.at[i, "order_item_id"]) for i in extra_zero),
        "quantity_blank": len(qty_blank), "product_id_blank": len(prod_blank),
        "price_as_text": len(money_text), "status_variants": len(status_variant), "sales_rep_trailing_space": len(rep_space),
        "branch_variants": len(branch_variant),
        "utc_date_differs_from_ist_date": int((truth.entered_at_utc.dt.date != truth.order_date.dt.date).sum()),
        "true_net_revenue_non_cancelled": round(float(valid.net_revenue.sum()), 2),
        "true_net_revenue_all": round(float(truth.net_revenue.sum()), 2),
        "true_status_lines": truth.status.value_counts().to_dict(),
        "true_lines_by_branch": truth.branch.value_counts().to_dict(),
    },
    "customers_export": {
        "rows": len(cust_rows), "planted_duplicate_records": len(dupkey), "city_variants_rows": len(cvar),
        "segment_variants_rows": len(seg_var), "invalid_email_no_at": len(bad_email - no_email), "email_blank": len(no_email),
        "signup_future_206x": len(future_signup), "signup_dd_mm_yyyy_slash": len(slash_signup - future_signup),
        "true_city_missing": int(C.city.isna().sum()),
    },
}
(HERE / "answer_key.json").write_text(json.dumps(key, indent=2, default=str), encoding="utf-8")
print(json.dumps(key["orders_export"], indent=1, default=str)[:1500])
