"""
Analyst to Architect — Chapter 14: Data Cleaning & Preparation
build_ch14_q3_export.py — builds a SECOND messy order export, for the project's stretch goal
("run your pipeline, unchanged, on another quarter").

How to run (from this folder):  python3 build_ch14_q3_export.py
Needs: Python 3.10+, pandas, pyarrow. Reads ../full/*.parquet (generate_riverstone_full.py, seed 20230101).
Seed for the damage: 20250714 (a different seed from the Q4 export's 20251014, so different rows are damaged).

Creates:
  orders_q3_2025_export.csv       the ERP's Q3 2025 (July-September) order-line export, damaged in the same KINDS of ways
                                  as orders_q4_2025_export.csv (same branch habits), but on different rows and in
                                  proportionally smaller numbers
  clean_truth_orders_q3_2025.csv  the correct clean table (for checking your work only)

The Q4 files are built by build_ch14_files.py and are not touched by this script.
Riverstone Supplies is fictional; every name and number is invented.
"""
import csv, random, pathlib, datetime as dt
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
FULL = HERE.parent / "full"
random.seed(20250714)

C = pd.read_parquet(FULL / "customers.parquet")
E = pd.read_parquet(FULL / "employees.parquet"); O = pd.read_parquet(FULL / "orders.parquet")
I = pd.read_parquet(FULL / "order_items.parquet")

REGION = {}
for r, cs in {"West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nashik", "Nagpur", "Indore", "Goa", "Vadodara", "Rajkot", "Thane", "Aurangabad"],
              "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore", "Mysuru", "Visakhapatnam", "Madurai", "Mangaluru", "Thiruvananthapuram"],
              "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh", "Udaipur", "Kanpur", "Ludhiana", "Dehradun", "Agra", "Noida", "Gurugram"],
              "East": ["Kolkata", "Bhubaneswar", "Patna", "Guwahati", "Ranchi", "Raipur"]}.items():
    for c in cs: REGION[c] = r
BRANCH = {"West": "Mumbai HO", "South": "Bengaluru", "North": "Delhi", "East": "Kolkata", None: "Mumbai HO"}

# ---- truth: Q3 2025 order lines ---------------------------------------------------------------------
t = (I.merge(O, on="order_id").merge(C[["customer_id", "city"]], on="customer_id")
       .merge(E[["employee_id", "employee_name"]], left_on="sales_rep_id", right_on="employee_id", how="left"))
t = t[(t.order_date >= "2025-07-01") & (t.order_date < "2025-10-01")]
t = t.sort_values(["order_date", "order_id", "order_item_id"]).reset_index(drop=True)
t["customer_code"] = t.customer_id.map(lambda v: f"{v:04d}")
t["branch"] = t.city.map(lambda c: BRANCH[REGION.get(c)])
t["sales_rep"] = t.employee_name.fillna("")
t["net_revenue"] = t.quantity * t.unit_price * (1 - t.discount_pct / 100)
ist = [dt.datetime.combine(d.date(), dt.time(0, 5)) + dt.timedelta(minutes=random.randint(0, 320)) if random.random() < 0.06
       else dt.datetime.combine(d.date(), dt.time(9, 0)) + dt.timedelta(minutes=random.randint(0, 870)) for d in t.order_date]
t["entered_at_utc"] = [x - dt.timedelta(hours=5, minutes=30) for x in ist]
truth = t[["order_item_id", "order_id", "order_date", "customer_code", "product_id", "quantity", "unit_price",
           "discount_pct", "status", "sales_rep", "branch", "entered_at_utc", "net_revenue"]].copy()
truth.to_csv(HERE / "clean_truth_orders_q3_2025.csv", index=False, date_format="%Y-%m-%d %H:%M:%S")

# ---- damage (same kinds as the Q4 export, scaled to the number of lines) ------------------------------
n = len(truth); idx = list(range(n)); scale = n / 25832
def k(x): return max(1, round(x * scale))
def pick(count, pool=None):
    pool = pool if pool is not None else idx
    return set(random.sample(pool, count))

kolkata = [i for i in idx if truth.at[i, "branch"] == "Kolkata"]
delhi = [i for i in idx if truth.at[i, "branch"] == "Delhi"]
others = [i for i in idx if truth.at[i, "branch"] not in ("Kolkata", "Delhi")]

dmy_slash = pick(k(1800), others)
serial = pick(k(40), [i for i in others if i not in dmy_slash])
iso_dates = set(kolkata)
impossible = pick(k(9), [i for i in others if i not in dmy_slash | serial and truth.at[i, "order_date"].day >= 28])
code_no_zero = set(kolkata)
disc_fraction = set(i for i in kolkata if truth.at[i, "discount_pct"] > 0)
cartons = pick(k(260), delhi)
cartons = set(i for i in cartons if truth.at[i, "quantity"] % 10 == 0)
money_text = pick(k(2300), others)
status_variant = pick(k(3100))
extra_zero = pick(k(6), [i for i in others if i not in cartons])
qty_blank = pick(k(14), [i for i in others if i not in extra_zero])
prod_blank = pick(k(8), [i for i in others if i not in qty_blank | extra_zero])
rep_space = pick(k(900))
branch_variant = pick(k(1400))
dup_rows = sorted(pick(k(137)))
page_headers = [4000, 8000, 12000, 16000, 20000]

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
    if i in impossible: ds = random.choice(["31-09-2025", "31-06-2025", "32-08-2025"])
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
lines = [header] + out + [["", "", "", "", "", "", "", "", "", "", "", "", f"Report generated 01-10-2025 02:00; rows: {len(out)}"]]
with open(HERE / "orders_q3_2025_export.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(lines)
print(f"orders_q3_2025_export.csv: {len(lines)} lines ({n} true order lines, {len(dup_rows)} duplicates, "
      f"{len(page_headers)} repeated headers, 1 footer)")
