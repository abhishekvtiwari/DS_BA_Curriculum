"""Chapter 46 companion (copied for Chapter 47): your Chapter 45 loads, tidied into functions.
Each load is idempotent: running it again with no source changes changes nothing.
Riverstone Supplies is fictional; every name and number is invented."""
import os, time, hashlib, psycopg2, requests

SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
BROKEN_ITEMS_SYNC = False    # section 46.7 turns this on: a faulty order-line load
CONFIRMED_RENAMES = {}       # section 46.7 fills this in: a confirmed column rename


# --- Reading and changing the source (the ERP) ---

def fetch_rows(sql, params=None):
    """Run one query on the source and return just its rows (a list of tuples)."""
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    conn.close()
    return rows

def run_sql(sql, params=None):
    """Run one statement that changes the source, such as an UPDATE, and commit it."""
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:
        cur.execute(sql, params)
    conn.close()


# --- Tables: compare row hashes, then upsert (Chapter 45, section 45.5) ---

TABLES = {
    "orders": ("order_id", ["order_id", "customer_id", "order_date", "status", "sales_rep_id"],
               "order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date DATE, status VARCHAR, sales_rep_id INTEGER"),
    "order_items": ("order_item_id", ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct"],
                    "order_item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER, "
                    "unit_price DECIMAL(10,2), discount_pct DECIMAL(5,2)"),
}

def row_hash(row):
    """One fingerprint per row: every column as text, joined, then hashed."""
    return hashlib.md5("|".join(str(v) for v in row).encode()).hexdigest()

def sync_table(wh, table):
    """Bring raw.<table> up to date with the source. Returns (new, changed, deleted)."""
    key, cols, ddl = TABLES[table]
    wh.execute("CREATE SCHEMA IF NOT EXISTS raw")
    wh.execute(f"CREATE TABLE IF NOT EXISTS raw.{table} ({ddl})")
    if table == "order_items" and BROKEN_ITEMS_SYNC:
        return (0, 0, 0)                  # the simulated bug: load nothing, say nothing
    col_list = ", ".join(cols)
    src = {r[0]: r for r in fetch_rows(f"SELECT {col_list} FROM {table}")}
    tgt = {r[0]: r for r in wh.execute(f"SELECT {col_list} FROM raw.{table}").fetchall()}
    new = [k for k in src if k not in tgt]
    changed = [k for k in src if k in tgt and row_hash(src[k]) != row_hash(tgt[k])]
    deleted = [k for k in tgt if k not in src]
    wh.execute("BEGIN")
    try:
        if new or changed:
            wh.executemany(f"INSERT OR REPLACE INTO raw.{table} VALUES ({', '.join('?' * len(cols))})",
                           [src[k] for k in new + changed])
        for k in deleted:
            wh.execute(f"DELETE FROM raw.{table} WHERE {key} = ?", [k])
        wh.execute("COMMIT")
    except Exception:
        wh.execute("ROLLBACK")
        raise
    return (len(new), len(changed), len(deleted))


# --- Files: check the columns, then replace the day's rows (Chapter 45, sections 45.7 and 45.8) ---

EXPECTED_DISPATCH = ["dispatch_id", "order_id", "dispatch_date", "warehouse", "qty_units", "remarks"]

def load_dispatch(wh, day):
    """Load exports/dispatch_<day>.csv into raw.dispatch, replacing that day's rows."""
    path = f"exports/dispatch_{day}.csv"
    wh.execute("CREATE SCHEMA IF NOT EXISTS raw")
    wh.execute("CREATE TABLE IF NOT EXISTS raw.dispatch (dispatch_id VARCHAR PRIMARY KEY, order_id INTEGER, "
               "dispatch_date VARCHAR, qty_units VARCHAR, file_day DATE)")
    if not os.path.exists(path):
        return "no file for this day, nothing to load"
    columns = [r[0] for r in wh.execute(f"DESCRIBE SELECT * FROM read_csv('{path}', all_varchar = true)").fetchall()]
    renamed = {c: CONFIRMED_RENAMES.get(c, c) for c in columns}    # file name -> expected name
    missing = [c for c in EXPECTED_DISPATCH if c not in renamed.values()]
    if missing:
        raise ValueError(f"schema change in {path}: missing {missing}")
    qty_column = next(c for c, name in renamed.items() if name == "qty_units")
    wh.execute("BEGIN")
    try:
        wh.execute("DELETE FROM raw.dispatch WHERE file_day = ?", [day])
        wh.execute(f"""INSERT INTO raw.dispatch
                       SELECT dispatch_id, order_id, dispatch_date, {qty_column}, CAST(? AS DATE)
                       FROM read_csv('{path}', header = true, all_varchar = true)""", [day])
        wh.execute("COMMIT")
    except Exception:
        wh.execute("ROLLBACK")
        raise
    n = wh.execute("SELECT COUNT(*) FROM raw.dispatch WHERE file_day = ?", [day]).fetchone()[0]
    return f"{n} rows (the day's rows replaced)"


# --- The CRM API: pages, token, 429 retries (Chapter 45, section 45.9) ---

def fetch_leads(base="http://127.0.0.1:8045/api/leads",
                token=os.environ.get("CRM_API_TOKEN", "practice-token-45")):
    """Read every lead, page by page. Waits and retries on 429; raises on any other error."""
    headers = {"Authorization": f"Bearer {token}"}
    leads, page = [], 1
    while page is not None:
        resp = requests.get(base, params={"page": page, "page_size": 20}, headers=headers, timeout=10)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", "1")))
            continue
        resp.raise_for_status()
        body = resp.json()
        leads.extend(body["data"])
        page = body["next_page"]
    return leads

def load_leads(wh, leads):
    """Replace raw.crm_leads with this list of leads: the same table as Chapter 45."""
    wh.execute("CREATE SCHEMA IF NOT EXISTS raw")
    wh.execute("""CREATE OR REPLACE TABLE raw.crm_leads (
                      lead_id INTEGER PRIMARY KEY, created_at TIMESTAMP, company_name VARCHAR,
                      email VARCHAR, source VARCHAR, owner_id INTEGER, loaded_for DATE)""")
    wh.executemany("INSERT INTO raw.crm_leads VALUES (?, ?, ?, ?, ?, ?, CURRENT_DATE)",
                   [(l["lead_id"], l["created_at"], l["company_name"], l["email"], l["source"], l["owner_id"])
                    for l in leads])
    return wh.execute("SELECT COUNT(*) FROM raw.crm_leads").fetchone()[0]
