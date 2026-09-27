"""Chapter 46 companion: the ingestion steps built in Chapter 45, packaged as functions.
Each function is idempotent: running it again with no source changes changes nothing.
Riverstone Supplies is fictional; every name and number is invented."""
import os, time, hashlib, psycopg2, requests

SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
BROKEN_ITEMS_SYNC = False       # set True to simulate a faulty order-line load (section 46.7)

def fetch_rows(sql, params=None):
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    conn.close()
    return rows

TABLES = {
    "orders": ("order_id", ["order_id", "customer_id", "order_date", "status", "sales_rep_id"],
               "order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date DATE, status VARCHAR, sales_rep_id INTEGER"),
    "order_items": ("order_item_id", ["order_item_id", "order_id", "product_id", "quantity", "unit_price", "discount_pct"],
                    "order_item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER, "
                    "unit_price DECIMAL(10,2), discount_pct DECIMAL(5,2)"),
}

def sync_table(wh, table):
    """Hash comparison + upsert (Chapter 45, section 45.5). Returns (new, changed, deleted)."""
    key, cols, ddl = TABLES[table]
    wh.execute("CREATE SCHEMA IF NOT EXISTS raw")
    wh.execute(f"CREATE TABLE IF NOT EXISTS raw.{table} ({ddl})")
    if table == "order_items" and BROKEN_ITEMS_SYNC:
        return (0, 0, 0)
    col_list = ", ".join(cols)
    src = {r[0]: r[1:] for r in fetch_rows(f"SELECT {col_list} FROM {table}")}
    tgt = {r[0]: r[1:] for r in wh.execute(f"SELECT {col_list} FROM raw.{table}").fetchall()}
    norm = lambda row: tuple(str(v) for v in row)
    new = [k for k in src if k not in tgt]
    changed = [k for k in src if k in tgt and norm(src[k]) != norm(tgt[k])]
    deleted = [k for k in tgt if k not in src]
    wh.execute("BEGIN")
    try:
        rows = [(k, *src[k]) for k in new + changed]
        if rows:
            wh.executemany(f"INSERT OR REPLACE INTO raw.{table} VALUES ({', '.join('?' * len(cols))})", rows)
        for k in deleted:
            wh.execute(f"DELETE FROM raw.{table} WHERE {key} = ?", [k])
        wh.execute("COMMIT")
    except Exception:
        wh.execute("ROLLBACK"); raise
    return (len(new), len(changed), len(deleted))

EXPECTED_DISPATCH = ["dispatch_id", "order_id", "dispatch_date", "warehouse", "qty_units", "remarks"]
CONFIRMED_RENAMES = {}          # e.g. {"units": "qty_units"} once the source owner confirms a rename

def load_dispatch(wh, day):
    """Load exports/dispatch_<day>.csv into raw.dispatch for that day, if the file exists.
    Stops with a clear error if an expected column is missing (Chapter 45, section 45.8)."""
    path = f"exports/dispatch_{day}.csv"
    wh.execute("CREATE SCHEMA IF NOT EXISTS raw")
    wh.execute("CREATE TABLE IF NOT EXISTS raw.dispatch (dispatch_id VARCHAR PRIMARY KEY, order_id INTEGER, "
               "dispatch_date VARCHAR, qty_units VARCHAR, file_day DATE)")
    if not os.path.exists(path):
        return "no file"
    original = [r[0] for r in wh.execute(f"DESCRIBE SELECT * FROM read_csv('{path}', all_varchar = true)").fetchall()]
    renamed = {c: CONFIRMED_RENAMES.get(c, c) for c in original}          # file column -> expected name
    missing = [c for c in EXPECTED_DISPATCH if c not in renamed.values()]
    if missing:
        raise ValueError(f"schema change in {path}: missing {missing}")
    qty_source = next(c for c, name in renamed.items() if name == "qty_units")
    wh.execute("BEGIN")
    try:
        wh.execute("DELETE FROM raw.dispatch WHERE file_day = ?", [day])
        wh.execute(f"""INSERT INTO raw.dispatch
            SELECT dispatch_id, order_id, dispatch_date, {qty_source}, DATE '{day}'
            FROM read_csv('{path}', header = true, all_varchar = true)""")
        wh.execute("COMMIT")
    except Exception:
        wh.execute("ROLLBACK"); raise
    return f"{wh.execute('SELECT COUNT(*) FROM raw.dispatch WHERE file_day = ?', [day]).fetchone()[0]} rows"

def fetch_leads(base="http://127.0.0.1:8045/api/leads", token="practice-token-45"):
    headers = {"Authorization": f"Bearer {token}"}
    leads, page = [], 1
    while page is not None:
        resp = requests.get(base, params={"page": page, "page_size": 20}, headers=headers, timeout=10)
        if resp.status_code == 429:
            time.sleep(int(resp.headers.get("Retry-After", "1"))); continue
        resp.raise_for_status()
        body = resp.json(); leads.extend(body["data"]); page = body["next_page"]
    return leads
