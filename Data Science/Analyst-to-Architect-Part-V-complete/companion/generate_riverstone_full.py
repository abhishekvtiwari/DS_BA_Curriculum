"""
Analyst to Architect — Riverstone Supplies full sales dataset (2023–2025).
generate_riverstone_full.py — builds the full-size version promised in Chapters 12 and 13 and used from Chapter 14 on.

How to run (from the companion folder):   python3 generate_riverstone_full.py
Needs: Python 3.10+, pandas, pyarrow (for Parquet). Runtime: under a minute.
Seed: 20230101. The same seed always produces the same data.

What it keeps from the one-year database (generate_riverstone_2025.py, seed 20251):
  - customers 1–24, products 101–108, employees 1–5, leads and lead_stage_history, unchanged;
  - every 2025 order and order line of customers 1–24, with the same IDs (orders 10001–10175, lines 1–330),
    so every Chapter 10–13 figure about those customers still holds inside the full data.
What it adds:
  - about 4,950 more customers (IDs 25+), 2023–2025 orders for them, and 2024 orders for the named customers
    who signed up in 2024; 11 more sales staff (employees 6–16); company-level monthly targets for 2023–2025;
  - yearly list prices (2023 = 92% and 2024 = 96% of today's price, rounded to ₹5);
  - documented planted problems (see full/DATA_SPEC.md): duplicate customer records with name variants,
    missing cities, orders without a sales rep, stale "Pending" orders.

Writes to ./full/: one CSV and one Parquet file per table, riverstone_full_setup_postgresql.sql,
riverstone_full_setup_mysql.sql. Riverstone Supplies is fictional; every name and number is invented.
"""
import os, random, runpy, tempfile, pathlib, datetime as dt, csv
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "full"; OUT.mkdir(exist_ok=True)
D = dt.date

# ---- 1. the one-year data, unchanged -------------------------------------------------------------
cwd = os.getcwd()
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp); one = runpy.run_path(str(HERE / "generate_riverstone_2025.py")); os.chdir(cwd)
named = one["customers"]; products = one["products"]; season = one["season"]
price_now = {p[0]: p[3] for p in products}

random.seed(20230101)

# ---- 2. people ------------------------------------------------------------------------------------
employees = list(one["employees"]) + [
    (6, "Arjun Nair", "Regional Sales Manager (South)", 1), (7, "Pooja Desai", "Regional Sales Manager (West)", 1),
    (8, "Sandeep Gill", "Regional Sales Manager (North)", 1),
    (9, "Kavitha Reddy", "Sales Executive", 6), (10, "Irfan Sheikh", "Sales Executive", 6),
    (11, "Meenal Joshi", "Sales Executive", 7), (12, "Rohit Verma", "Sales Executive", 7),
    (13, "Divya Menon", "Sales Executive", 6), (14, "Aakash Jain", "Sales Executive", 8),
    (15, "Simran Kaur", "Sales Executive", 8), (16, "Tarun Bose", "Sales Executive", 7),
]
region_of_city = {}
REGIONS = {
    "West": ["Mumbai", "Pune", "Ahmedabad", "Surat", "Nashik", "Nagpur", "Indore", "Goa", "Vadodara", "Rajkot", "Thane", "Aurangabad"],
    "South": ["Bengaluru", "Chennai", "Hyderabad", "Kochi", "Coimbatore", "Mysuru", "Visakhapatnam", "Madurai", "Mangaluru", "Thiruvananthapuram"],
    "North": ["Delhi", "Jaipur", "Lucknow", "Chandigarh", "Udaipur", "Kanpur", "Ludhiana", "Dehradun", "Agra", "Noida", "Gurugram"],
    "East": ["Kolkata", "Bhubaneswar", "Patna", "Guwahati", "Ranchi", "Raipur"],
}
CITY_W = {"Mumbai": 9, "Delhi": 8, "Bengaluru": 7, "Pune": 6, "Chennai": 6, "Hyderabad": 6, "Ahmedabad": 5, "Kolkata": 5}
for r, cs in REGIONS.items():
    for c in cs: region_of_city[c] = r
cities = sorted(region_of_city); city_weights = [CITY_W.get(c, 2) for c in cities]
reps_by_region = {"West": [11, 12, 16, 3, 4], "South": [9, 10, 13, 5], "North": [14, 15, 4], "East": [15, 16, 13]}

# ---- 3. customers ---------------------------------------------------------------------------------
PRE = ["Shree", "Sai", "Om", "Balaji", "Ganesh", "Laxmi", "Royal", "New", "City", "Metro", "Green", "Blue", "Golden", "Silver", "Sunrise",
       "Evergreen", "Prime", "Star", "Classic", "Modern", "Urban", "Coastal", "Heritage", "Lotus", "Sapphire", "Crystal", "Maple", "Orchid",
       "Pearl", "Saffron", "Tulsi", "Nandi", "Krishna", "Mahalaxmi", "Vijay", "Jai Hind", "Bharat", "National", "Supreme", "United", "Galaxy",
       "Rainbow", "Silk Route", "Harbour", "Hill View", "Lake View", "River Side", "Palm", "Coconut Grove", "Spice Garden"]
TYPE = {"Retail": ["Stores", "Mart", "Home Needs", "Provisions", "General Store", "Supermarket", "Kitchenware", "Traders", "Emporium", "Bazaar"],
        "Hospitality": ["Hotels", "Resorts", "Caterers", "Restaurant", "Cafe", "Banquets", "Kitchens", "Foods", "Inn", "Tiffin Services"],
        "Wholesale": ["Distributors", "Wholesale", "Agencies", "Logistics", "Packaging", "Enterprises", "Suppliers", "Trading Co", "Depot", "Exports"]}
PROFILE_W = {"Retail": [("steady", 30), ("occasional", 40), ("churn", 18), ("seasonal", 12)],
             "Hospitality": [("steady", 30), ("occasional", 30), ("churn", 20), ("seasonal", 20)],
             "Wholesale": [("steady", 25), ("big", 45), ("occasional", 15), ("churn", 15)]}

customers = [c[:5] for c in named]                 # (id, name, city, segment, signup)
cinfo = {}                                          # id -> (segment, profile, rep, churn_date, city)
for (cid, name, city, seg, signup, prof, rep, churn) in named:
    cinfo[cid] = dict(seg=seg, prof=prof, rep=rep, churn=None, city=city, signup=signup, named=True)
used = {c[1].lower() for c in customers}
N_NEW = 4955
for i in range(N_NEW):
    cid = 25 + i
    seg = random.choices(["Retail", "Hospitality", "Wholesale"], [55, 30, 15])[0]
    city = random.choices(cities, city_weights)[0]
    for _ in range(50):
        nm = f"{random.choice(PRE)} {random.choice(TYPE[seg])}"
        if nm.lower() in used: nm = f"{nm} {city}"
        if nm.lower() not in used: break
        nm = f"{random.choice(PRE)} {random.choice(PRE)} {random.choice(TYPE[seg])}"
        if nm.lower() not in used: break
    used.add(nm.lower())
    # signups: a base of older customers, then steady acquisition through 2025
    r = random.random()
    if r < 0.48: signup = D(2020, 1, 1) + dt.timedelta(days=random.randint(0, 1095))       # 2020–2022
    elif r < 0.68: signup = D(2023, 1, 1) + dt.timedelta(days=random.randint(0, 364))
    elif r < 0.86: signup = D(2024, 1, 1) + dt.timedelta(days=random.randint(0, 365))
    else: signup = D(2025, 1, 1) + dt.timedelta(days=random.randint(0, 334))
    prof = random.choices(*zip(*PROFILE_W[seg]))[0]
    churn = None
    if prof == "churn":
        start = max(signup, D(2023, 1, 1))
        churn = start + dt.timedelta(days=random.randint(60, max(61, (D(2025, 12, 31) - start).days)))
    rep = random.choice(reps_by_region[region_of_city[city]])
    customers.append((cid, nm, city, seg, signup))
    cinfo[cid] = dict(seg=seg, prof=prof, rep=rep, churn=churn, city=city, signup=signup, named=False)

# planted: duplicate customer records (same business keyed twice, name variant, same city)
dups = []
dup_sources = random.sample(range(25, 25 + N_NEW), 48)
next_id = 25 + N_NEW
for k, src in enumerate(dup_sources):
    c = customers[src - 1]
    variant = [c[1].upper(), c[1] + " ", c[1].replace(" ", "  ", 1), c[1] + " Pvt Ltd", c[1].replace("and", "&")][k % 5]
    signup = c[4] + dt.timedelta(days=random.randint(30, 400))
    if signup > D(2025, 11, 30): signup = D(2025, 11, 30)
    customers.append((next_id, variant, c[2], c[3], signup))
    info = dict(cinfo[src]); info.update(signup=signup, prof="occasional", churn=None, named=False)
    cinfo[next_id] = info; dups.append((next_id, src)); next_id += 1
# planted: missing city for about 2% of new customers
city_missing = set(random.sample(range(25, next_id), 100))
customers = [(c[0], c[1], None if c[0] in city_missing else c[2], c[3], c[4]) for c in customers]

# ---- 4. orders and lines --------------------------------------------------------------------------
def list_price(pid, year):
    f = {2023: 0.92, 2024: 0.96, 2025: 1.0}[year]
    return int(round(price_now[pid] * f / 5.0)) * 5

growth = {2023: 0.80, 2024: 0.92, 2025: 1.0}
base = {"steady": 0.97, "occasional": 0.68, "big": 0.97, "churn": 0.95, "seasonal": 0.50}
orders = []; lines = []
for cid, info in cinfo.items():
    if info["named"] and info["signup"].year == 2025: continue
    years = [2024] if info["named"] else [2023, 2024, 2025]
    for y in years:
        for m in range(1, 13):
            ms = D(y, m, 1)
            if ms < D(info["signup"].year, info["signup"].month, 1): continue
            if info["named"] and ms < D(info["signup"].year, info["signup"].month, 1): continue
            if info["churn"] and ms > info["churn"]: continue
            p = base[info["prof"]] * min(1.0, 0.55 + 0.45 * season[m]) * growth[y]
            if info["prof"] == "seasonal": p = (0.12 if m < 9 else min(0.9, 0.3 * season[m] * 2.2)) * growth[y]
            n = 1 if random.random() < min(p, 0.97) else 0
            if info["prof"] in ("big", "steady") and random.random() < 0.50 * season[m]: n += 1
            if info["prof"] == "big" and random.random() < 0.30 * season[m]: n += 1
            for _ in range(n):
                day = random.randint(1, 28)
                if ms == D(info["signup"].year, info["signup"].month, 1): day = max(day, info["signup"].day)
                od = D(y, m, day)
                status = "Delivered"
                if random.random() < 0.04: status = "Cancelled"
                elif od >= D(2025, 12, 20): status = random.choice(["Shipped", "Pending"])
                rep = info["rep"]
                if rep and random.random() < 0.03: rep = None
                orders.append([None, cid, od, status, rep])
                seg = info["seg"]
                if seg == "Wholesale": pool = [105, 105, 102, 108, 101]; qty = (10, 45); disc = [5, 8, 10, 12]
                elif seg == "Hospitality": pool = [103, 104, 107, 101, 108]; qty = (10, 60); disc = [0, 0, 5]
                else:
                    pool = [101, 103, 104, 107, 108, 102]; qty = (10, 50); disc = [0, 0, 0, 5]
                    if m in (3, 4, 5): pool += [106, 106]
                if info["prof"] == "seasonal" and m in (10, 11): pool += [107, 104]
                chosen = random.sample(sorted(set(pool)), k=min(len(set(pool)), random.choice([1, 1, 2, 2, 3])))
                for pid in chosen:
                    q = max(5, int(random.randint(*qty) * season[m]) // 5 * 5)
                    lines.append([len(orders) - 1, pid, q, list_price(pid, y), random.choice(disc)])

# planted: stale "Pending" orders from long ago (never updated in the ERP)
old_idx = [i for i, o in enumerate(orders) if o[2] < D(2025, 6, 1) and o[3] == "Delivered"]
for i in random.sample(old_idx, 60): orders[i][3] = "Pending"

# chronological IDs for generated orders; the named customers' 2025 orders keep 10001–10175
order_idx = sorted(range(len(orders)), key=lambda i: (orders[i][2], orders[i][1]))
new_id = {}
for k, i in enumerate(order_idx): new_id[i] = 200001 + k
orders_out = [(new_id[i], o[1], o[2], o[3], o[4]) for i, o in enumerate(orders)]
lines_sorted = sorted(lines, key=lambda l: (new_id[l[0]], l[1]))
items_out = [(1001 + k, new_id[l[0]], l[1], l[2], l[3], l[4]) for k, l in enumerate(lines_sorted)]
orders_out += list(one["new_orders"]); items_out += list(one["items"])
orders_out.sort(key=lambda o: (o[2], o[0])); items_out.sort(key=lambda it: it[0])

# ---- 5. targets: plan = previous year's actual for the month x that year's planned growth x a planning error,
#         rounded to ₹50,000 (2023 plans use 2023 actuals with a planning error, as no 2022 data is included)
odf = pd.DataFrame(orders_out, columns=["order_id", "customer_id", "order_date", "status", "sales_rep_id"])
idf = pd.DataFrame(items_out, columns=["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct"])
m = idf.merge(odf, on="order_id")
m = m[m.status != "Cancelled"]
m["rev"] = m.quantity * m.unit_price * (1 - m.discount_pct / 100)
m["ym"] = pd.to_datetime(m.order_date).dt.to_period("M")
actual = m.groupby("ym").rev.sum()
yearly = m.groupby(pd.to_datetime(m.order_date).dt.year).rev.sum()
targets = []
for y in (2023, 2024, 2025):
    plan_growth = 1.0 if y == 2023 else yearly[y] / yearly[y - 1]
    for mo in range(1, 13):
        base_m = actual[pd.Period(f"{y}-{mo:02d}", "M")] if y == 2023 else actual[pd.Period(f"{y-1}-{mo:02d}", "M")]
        err = random.uniform(0.94, 1.09)
        targets.append((D(y, mo, 1), round(base_m * plan_growth * err / 50000) * 50000))

tables = {
    "customers": (["customer_id", "customer_name", "city", "segment", "signup_date"], customers),
    "products": (["product_id", "product_name", "category", "unit_price", "unit_cost"], [tuple(p) for p in products]),
    "employees": (["employee_id", "employee_name", "job_title", "manager_id"], employees),
    "orders": (["order_id", "customer_id", "order_date", "status", "sales_rep_id"], orders_out),
    "order_items": (["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct"], items_out),
    "sales_targets": (["target_month", "target_revenue"], targets),
    "leads": (["lead_id", "created_at", "company_name", "email", "source", "owner_id"], one["leads"]),
    "lead_stage_history": (["lead_id", "stage", "entered_at"], one["hist"]),
}
for name, (cols, rows) in tables.items():
    df = pd.DataFrame(rows, columns=cols)
    for c in df.columns:                      # nullable ID columns stay whole numbers (not 1.0) in CSV
        if c.endswith("_id") and df[c].dtype == float: df[c] = df[c].astype("Int64")
    csv_df = df.copy()
    for c in csv_df.columns:                  # dates as YYYY-MM-DD, timestamps as YYYY-MM-DD HH:MM:SS
        if csv_df[c].dtype == object:
            csv_df[c] = csv_df[c].map(lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, dt.datetime)
                                      else (v.strftime("%Y-%m-%d") if isinstance(v, dt.date) else v))
    csv_df.to_csv(OUT / f"{name}.csv", index=False)
    for c in df.columns:
        if df[c].dtype == object and df[c].map(lambda v: isinstance(v, (dt.date, dt.datetime))).any():
            df[c] = pd.to_datetime(df[c])
    df.to_parquet(OUT / f"{name}.parquet", index=False)
pd.DataFrame(dups, columns=["duplicate_customer_id", "original_customer_id"]).to_csv(OUT / "_answer_key_duplicate_customers.csv", index=False)

DDL = """CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, customer_name VARCHAR(100) NOT NULL, city VARCHAR(50), segment VARCHAR(30) NOT NULL, signup_date DATE NOT NULL);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, product_name VARCHAR(100) NOT NULL, category VARCHAR(30) NOT NULL, unit_price NUMERIC(10,2) NOT NULL, unit_cost NUMERIC(10,2) NOT NULL);
CREATE TABLE employees (employee_id INTEGER PRIMARY KEY, employee_name VARCHAR(100) NOT NULL, job_title VARCHAR(50) NOT NULL, manager_id INTEGER REFERENCES employees(employee_id));
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id), order_date DATE NOT NULL, status VARCHAR(20) NOT NULL, sales_rep_id INTEGER REFERENCES employees(employee_id));
CREATE TABLE order_items (order_item_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(order_id), product_id INTEGER NOT NULL REFERENCES products(product_id), quantity INTEGER NOT NULL, unit_price NUMERIC(10,2) NOT NULL, discount_pct NUMERIC(5,2) NOT NULL DEFAULT 0);
CREATE TABLE sales_targets (target_month DATE PRIMARY KEY, target_revenue NUMERIC(12,2) NOT NULL);
CREATE TABLE leads (lead_id INTEGER PRIMARY KEY, created_at TIMESTAMP NOT NULL, company_name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL, source VARCHAR(30) NOT NULL, owner_id INTEGER REFERENCES employees(employee_id));
CREATE TABLE lead_stage_history (lead_id INTEGER NOT NULL REFERENCES leads(lead_id), stage VARCHAR(20) NOT NULL, entered_at TIMESTAMP NOT NULL, PRIMARY KEY (lead_id, stage));
"""
VIEW = """CREATE VIEW sales_lines AS
SELECT o.order_id, o.order_date, o.customer_id, o.sales_rep_id, o.status,
       oi.product_id, p.category, oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS net_revenue,
       oi.quantity * p.unit_cost AS product_cost
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled';
"""
ORDER = ["employees", "customers", "products", "orders", "order_items", "sales_targets", "leads", "lead_stage_history"]
pg = ["-- Riverstone Supplies (fictional) — full sales dataset 2023–2025 (PostgreSQL 16+).",
      "-- Generated by generate_riverstone_full.py (seed 20230101). Every name and number is invented.",
      "-- Run from the folder that holds the CSV files:",
      "--   createdb riverstone_full   (or: CREATE DATABASE riverstone_full;)",
      "--   psql -d riverstone_full -f riverstone_full_setup_postgresql.sql",
      "DROP VIEW IF EXISTS sales_lines;",
      "DROP TABLE IF EXISTS lead_stage_history, leads, sales_targets, order_items, orders, products, customers, employees;", DDL]
for t in ORDER:
    cols = ", ".join(tables[t][0])
    pg.append(f"\\copy {t} ({cols}) FROM '{t}.csv' WITH (FORMAT csv, HEADER true, NULL '')")
pg += [VIEW, "ANALYZE;"]
(OUT / "riverstone_full_setup_postgresql.sql").write_text("\n".join(pg) + "\n", encoding="utf-8")

my = ["-- Riverstone Supplies (fictional) — full sales dataset 2023–2025 (MySQL 8.0+).",
      "-- Generated by generate_riverstone_full.py (seed 20230101). Every name and number is invented.",
      "-- Run from the folder that holds the CSV files, with local loading allowed on both client and server:",
      "--   mysql --local-infile=1 -u root -p < riverstone_full_setup_mysql.sql",
      "--   (server: SET GLOBAL local_infile = 1;)",
      "DROP DATABASE IF EXISTS riverstone_full;", "CREATE DATABASE riverstone_full;", "USE riverstone_full;",
      "SET FOREIGN_KEY_CHECKS = 0;", DDL]
for t in ORDER:
    cols = tables[t][0]
    varcols = ", ".join("@" + c for c in cols)
    sets = ", ".join(f"{c} = NULLIF(@{c}, '')" for c in cols)
    my.append(f"LOAD DATA LOCAL INFILE '{t}.csv' INTO TABLE {t} CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' "
              f"LINES TERMINATED BY '\\n' IGNORE 1 LINES ({varcols}) SET {sets};")
my += ["SET FOREIGN_KEY_CHECKS = 1;", VIEW]
(OUT / "riverstone_full_setup_mysql.sql").write_text("\n".join(my) + "\n", encoding="utf-8")

print(f"customers {len(customers)}  orders {len(orders_out)}  order_items {len(items_out)}  targets {len(targets)}")
