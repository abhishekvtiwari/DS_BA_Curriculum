"""
Analyst to Architect — Chapter 14: Data Cleaning & Preparation
build_ch14_sql.py — writes the SQL load scripts that put the chapter's CSV files into the database.

How to run (from this folder, after build_ch14_files.py and build_ch14_q3_export.py):  python3 build_ch14_sql.py
Needs: Python 3.10+ (standard library only).

Creates, in sql/:
  ch14_load_postgresql.sql     staging tables (every column TEXT), the four mapping tables and truth_order_lines,
  ch14_load_mysql.sql          with every CSV line written out as INSERT statements. These scripts need no file
                               paths and no special settings, so they run in DBeaver with Execute SQL Script
                               (Chapter 12, section 12.3), like any other script.
  ch14_load_q3_postgresql.sql  replaces stg_orders_raw with orders_q3_2025_export.csv (the project's stretch goal)
  ch14_load_q3_mysql.sql
  terminal/ch14_load_postgresql.sql   the same loads as psql \\copy and MySQL LOAD DATA LOCAL INFILE commands,
  terminal/ch14_load_mysql.sql        which read the CSV files directly (run from companion/ch14 in a terminal)

Empty fields are stored the way each database's own CSV loader stores them: NULL in PostgreSQL (an unquoted
empty field), an empty string in MySQL. The INSERT scripts keep the text NULL (24 CRM cities) as text in both databases;
MySQL's LOAD DATA in the terminal version reads an unquoted NULL as a real NULL, the only difference between the two.
Riverstone Supplies is fictional; every name and number is invented.
"""
import csv, pathlib

HERE = pathlib.Path(__file__).resolve().parent
SQL = HERE / "sql"; (SQL / "terminal").mkdir(parents=True, exist_ok=True)
BATCH = 500

ORDER_COLS = ["order_item_id", "order_id", "order_date", "customer_code", "product_id", "quantity", "qty_unit",
              "unit_price", "discount_pct", "status", "sales_rep", "branch", "entered_at_utc"]
CUST_COLS = ["customer_code", "customer_name", "city", "segment", "email", "signup_date"]

PG_STG = """CREATE TABLE stg_orders_raw (
  order_item_id TEXT, order_id TEXT, order_date TEXT, customer_code TEXT, product_id TEXT, quantity TEXT,
  qty_unit TEXT, unit_price TEXT, discount_pct TEXT, status TEXT, sales_rep TEXT, branch TEXT, entered_at_utc TEXT);"""
PG_CUST = "CREATE TABLE stg_customers_raw (customer_code TEXT, customer_name TEXT, city TEXT, segment TEXT, email TEXT, signup_date TEXT);"
MY_STG = """CREATE TABLE stg_orders_raw (
  order_item_id VARCHAR(20), order_id VARCHAR(20), order_date VARCHAR(20), customer_code VARCHAR(20), product_id VARCHAR(20),
  quantity VARCHAR(20), qty_unit VARCHAR(10), unit_price VARCHAR(30), discount_pct VARCHAR(20), status VARCHAR(30),
  sales_rep VARCHAR(100), branch VARCHAR(50), entered_at_utc VARCHAR(80)) CHARACTER SET utf8mb4;"""
MY_CUST = """CREATE TABLE stg_customers_raw (customer_code VARCHAR(20), customer_name VARCHAR(150), city VARCHAR(80), segment VARCHAR(40),
  email VARCHAR(150), signup_date VARCHAR(20)) CHARACTER SET utf8mb4;"""

MAPS = {
 "pg": """CREATE TABLE map_status (raw_value TEXT PRIMARY KEY, clean_value TEXT NOT NULL);
CREATE TABLE map_branch (raw_value TEXT PRIMARY KEY, clean_value TEXT NOT NULL);
CREATE TABLE map_city (raw_value TEXT PRIMARY KEY, clean_value TEXT);
CREATE TABLE map_segment (raw_value TEXT PRIMARY KEY, clean_value TEXT NOT NULL);""",
 "my": """CREATE TABLE map_status (raw_value VARCHAR(30) PRIMARY KEY, clean_value VARCHAR(30) NOT NULL);
CREATE TABLE map_branch (raw_value VARCHAR(50) PRIMARY KEY, clean_value VARCHAR(50) NOT NULL);
CREATE TABLE map_city (raw_value VARCHAR(80) PRIMARY KEY, clean_value VARCHAR(80));
CREATE TABLE map_segment (raw_value VARCHAR(40) PRIMARY KEY, clean_value VARCHAR(40) NOT NULL);"""}
MAP_ROWS = """INSERT INTO map_status VALUES ('delivered','Delivered'),('dlvd','Delivered'),('cancelled','Cancelled'),('canceled','Cancelled'),
  ('cxl','Cancelled'),('shipped','Shipped'),('pending','Pending');
INSERT INTO map_branch VALUES ('mumbai ho','Mumbai HO'),('mumbai h.o.','Mumbai HO'),('mumbai','Mumbai HO'),('bengaluru','Bengaluru'),
  ('bangalore','Bengaluru'),('blr','Bengaluru'),('delhi','Delhi'),('new delhi','Delhi'),('del','Delhi'),('kolkata','Kolkata'),
  ('calcutta','Kolkata'),('kol','Kolkata');
INSERT INTO map_city VALUES ('bombay','Mumbai'),('bangalore','Bengaluru'),('gurgaon','Gurugram'),('calcutta','Kolkata'),
  ('madras','Chennai'),('trivandrum','Thiruvananthapuram'),('vizag','Visakhapatnam'),('mysore','Mysuru'),('new delhi','Delhi'),
  ('poona','Pune'),('n/a',NULL),('-',NULL),('unknown',NULL),('null',NULL);
INSERT INTO map_segment VALUES ('retail','Retail'),('hospitality','Hospitality'),('hotel/restaurant','Hospitality'),('horeca','Hospitality'),
  ('wholesale','Wholesale'),('distributor','Wholesale');"""
TRUTH = {
 "pg": """CREATE TABLE truth_order_lines (order_item_id INTEGER PRIMARY KEY, order_id INTEGER, order_date DATE, customer_code TEXT,
  product_id INTEGER, quantity INTEGER, unit_price NUMERIC(10,2), discount_pct NUMERIC(5,2), status TEXT, sales_rep TEXT,
  branch TEXT, entered_at_utc TIMESTAMP, net_revenue NUMERIC(14,2));""",
 "my": """CREATE TABLE truth_order_lines (order_item_id INTEGER PRIMARY KEY, order_id INTEGER, order_date DATE, customer_code VARCHAR(4),
  product_id INTEGER, quantity INTEGER, unit_price DECIMAL(10,2), discount_pct DECIMAL(5,2), status VARCHAR(20), sales_rep VARCHAR(100),
  branch VARCHAR(20), entered_at_utc DATETIME, net_revenue DECIMAL(14,2)) CHARACTER SET utf8mb4;"""}
DROPS = "DROP TABLE IF EXISTS stg_orders_raw, stg_customers_raw, map_status, map_branch, map_city, map_segment, truth_order_lines;"

def lit(v, engine, empty_null):
    if v == "" and empty_null: return "NULL"
    v = v.replace("'", "''")
    if engine == "my": v = v.replace("\\", "\\\\")
    return f"'{v}'"

def inserts(table, rows, engine, empty_null, typed=None):
    out = []
    for s in range(0, len(rows), BATCH):
        vals = []
        for r in rows[s:s + BATCH]:
            if typed: vals.append("(" + ",".join(typed(r)) + ")")
            else: vals.append("(" + ",".join(lit(v, engine, empty_null) for v in r) + ")")
        out.append(f"INSERT INTO {table} VALUES\n" + ",\n".join(vals) + ";")
    return "\n".join(out)

def read(name):
    with open(HERE / name, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]

def truth_row(engine):
    def f(r):
        (oi, o, d, cc, p, q, up, dp, st, rep, br, ts, nr) = r
        rep_sql = "NULL" if rep == "" else lit(rep, engine, False)
        return [oi, o, f"'{d[:10]}'", f"'{cc}'", p, q, up, dp, lit(st, engine, False), rep_sql, lit(br, engine, False), f"'{ts}'",
                f"{round(float(nr), 2):.2f}"]
    return f

HEAD = """-- Analyst to Architect, Chapter 14 — {what} ({db}).
-- Written by build_ch14_sql.py from the CSV files in companion/ch14. Don't edit by hand: rebuild it.
-- How to run: in DBeaver, make {target} the active database, open this file, and choose Execute SQL Script (Alt+X).
-- Every staging column is text: a staging table must accept anything the export contains. Empty fields are stored
-- the way {db}'s own CSV loader stores them ({empty}).
-- Riverstone Supplies is fictional; every name and number is invented.
"""

def main():
    oh, orders = read("orders_q4_2025_export.csv"); assert oh == ORDER_COLS
    ch, custs = read("customers_crm_export.csv"); assert ch == CUST_COLS
    th, truth = read("clean_truth_orders_q4_2025.csv")
    qh, q3 = read("orders_q3_2025_export.csv"); assert qh == ORDER_COLS
    for eng, db, empty in (("pg", "PostgreSQL 16+", "an empty field becomes NULL"),
                           ("my", "MySQL 8.0+", "an empty field becomes an empty string")):
        en = eng == "pg"
        pre = "" if en else "SET NAMES utf8mb4;\n"
        body = [HEAD.format(what="load the messy exports, the mapping tables and the truth table", db=db, target="riverstone_full", empty=empty),
                pre + DROPS, PG_STG if en else MY_STG, inserts("stg_orders_raw", orders, eng, en),
                PG_CUST if en else MY_CUST, inserts("stg_customers_raw", custs, eng, en),
                MAPS[eng], MAP_ROWS, TRUTH[eng], inserts("truth_order_lines", truth, eng, en, truth_row(eng)),
                "-- Check: SELECT COUNT(*) FROM stg_orders_raw;  returns 25976"]
        name = "ch14_load_postgresql.sql" if en else "ch14_load_mysql.sql"
        (SQL / name).write_text("\n".join(body) + "\n", encoding="utf-8")
        body = [HEAD.format(what="replace stg_orders_raw with the Q3 2025 export (project stretch goal)", db=db, target="riverstone_full", empty=empty),
                pre + "DROP TABLE IF EXISTS stg_orders_raw;", PG_STG if en else MY_STG, inserts("stg_orders_raw", q3, eng, en),
                f"-- Check: SELECT COUNT(*) FROM stg_orders_raw;  returns {len(q3)}",
                "-- To go back to the Q4 export, run ch14_load_postgresql.sql (or ch14_load_mysql.sql) again."]
        name = "ch14_load_q3_postgresql.sql" if en else "ch14_load_q3_mysql.sql"
        (SQL / name).write_text("\n".join(body) + "\n", encoding="utf-8")
    # terminal versions: read the CSV files directly
    (SQL / "terminal" / "ch14_load_postgresql.sql").write_text(
        "-- Analyst to Architect, Chapter 14 — terminal version of ch14_load_postgresql.sql (psql's \\copy reads the CSV files).\n"
        "-- Run from companion/ch14:  psql -d riverstone_full -f sql/terminal/ch14_load_postgresql.sql\n"
        + DROPS + "\n" + PG_STG + "\n\\copy stg_orders_raw FROM 'orders_q4_2025_export.csv' WITH (FORMAT csv, HEADER true)\n"
        + PG_CUST + "\n\\copy stg_customers_raw FROM 'customers_crm_export.csv' WITH (FORMAT csv, HEADER true)\n"
        + MAPS["pg"] + "\n" + MAP_ROWS + "\n" + TRUTH["pg"]
        + "\n\\copy truth_order_lines FROM 'clean_truth_orders_q4_2025.csv' WITH (FORMAT csv, HEADER true)\n", encoding="utf-8")
    (SQL / "terminal" / "ch14_load_mysql.sql").write_text(
        "-- Analyst to Architect, Chapter 14 — terminal version of ch14_load_mysql.sql (LOAD DATA LOCAL INFILE reads the CSV files).\n"
        "-- Run from companion/ch14:  mysql --local-infile=1 -u root -p riverstone_full < sql/terminal/ch14_load_mysql.sql\n"
        "-- (server, once: SET GLOBAL local_infile = 1;). The exports have Windows line endings (\\r\\n).\n"
        + DROPS + "\n" + MY_STG + "\nLOAD DATA LOCAL INFILE 'orders_q4_2025_export.csv' INTO TABLE stg_orders_raw CHARACTER SET utf8mb4\n"
        "  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES;\n"
        + MY_CUST + "\nLOAD DATA LOCAL INFILE 'customers_crm_export.csv' INTO TABLE stg_customers_raw CHARACTER SET utf8mb4\n"
        "  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\\r\\n' IGNORE 1 LINES;\n"
        + MAPS["my"] + "\n" + MAP_ROWS + "\n" + TRUTH["my"]
        + "\nLOAD DATA LOCAL INFILE 'clean_truth_orders_q4_2025.csv' INTO TABLE truth_order_lines CHARACTER SET utf8mb4\n"
          "  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' LINES TERMINATED BY '\\n' IGNORE 1 LINES\n"
          "  (order_item_id, order_id, @d, customer_code, product_id, quantity, unit_price, discount_pct, status, @rep, branch, entered_at_utc, net_revenue)\n"
          "  SET order_date = DATE(@d), sales_rep = NULLIF(@rep, '');\n", encoding="utf-8")
    for p in sorted(SQL.rglob("*.sql")): print(f"{p.relative_to(HERE)}: {p.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
