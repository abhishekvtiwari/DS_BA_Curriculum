# Chapter 46. Pipelines & Orchestration

*Part 5 — Data Engineering, Integration & Scale*

> **Chapter at a glance**
>
> **You will learn to:** explain what an orchestrator adds to scheduled scripts · describe a pipeline as a graph of assets with dependencies, schedules, and partitions · build Riverstone's daily pipeline in Dagster, from ingestion to a delivered Daily Sales Flash · prove a pipeline step is idempotent with a deliberate failure test, and show what happens when it isn't · rebuild history with a backfill without re-sending old reports · use retries for transient failures without hiding real bugs · stop delivery when the data fails its checks, and send an alert that tells someone what to do · handle late-arriving corrections · read and write the same pipeline in Airflow · choose an orchestrator, and run pipelines responsibly.
>
> **Before you start:** Chapter 45 (ingestion, hashes, upserts, idempotency; your ingestion project), Chapter 20 (the Daily Sales Flash, cron, and scheduling), Chapter 29 (modules, decorators, generators, tests), Chapter 32 (dbt's DAG), Chapter 12 (transactions: `BEGIN`, `COMMIT`, `ROLLBACK`), Chapter 26, section 26.0 (the terminal), and Chapter 17 (the virtual environment and Jupyter).
>
> **Time needed:** 16–20 hours of reading and practice, spread over two to three weeks, in four sittings: sections 46.1–46.3 (the ideas and the first run); 46.4–46.5 (idempotency, backfills, late data); 46.6–46.7 (retries, sensors, checks, alerts); 46.8–46.10 and the project.
>
> **Tools:** Python in the book's virtual environment (Chapter 17) with `duckdb`, `psycopg2`, and `requests` from Chapter 45, plus `dagster` and `dagster-webserver`, which section 46.3 installs; PostgreSQL 16; and the Chapter 46 companion folder. Everything runs on your own computer.
>
> **Practice data:** the `riverstone_source` database from Chapter 45 (a private copy of the one-year database, playing the ERP and CRM), Bhiwandi Main's dispatch files, and the practice CRM API. Every output shown is from a real run.

---

## Why this matters

In Chapter 20, the Daily Sales Flash became a script that runs every morning and emails the managers. In Chapter 45, you built the loads that bring orders, dispatches, and leads into the warehouse. Each piece works on its own. Now they have to work *together*, every day, in the right order, without anyone watching.

That's harder than it sounds. The dispatch file arrives late. The CRM drops a connection. The order-line load hits a bug on the same morning a manager is waiting for the numbers. A script scheduled for 6:30 a.m. doesn't know that the orders it's reporting on haven't finished loading. And when something fails at 6:31, someone has to know what failed, what's safe to re-run, and whether the managers already received a wrong email.

An **orchestrator** is the software that runs these steps in the right order, on schedule, and keeps a record of every run. Good orchestration turns a collection of scripts into a **pipeline**: something you can trust, re-run, repair, and explain. This chapter builds Riverstone's first real pipeline, breaks it on purpose, one fault at a time, and shows how a well-designed pipeline survives each one.

---

## In plain English

Think about how a restaurant kitchen gets dinner out.

- The **recipe** says what depends on what: the sauce needs the stock, the plate needs the sauce and the rice. That's the **dependency graph** of a pipeline.
- The **head chef** doesn't cook everything. The head chef makes sure each station starts at the right time, in the right order, and knows when something's gone wrong. That's the **orchestrator**.
- Each **service** (Monday lunch, Monday dinner) is prepared separately. That's a **partition**: one day's run of the pipeline.
- If the rice burns, you remake the rice. You don't serve two plates of rice, and you don't throw away the sauce. Remaking a step without doubling anything is **idempotency**.
- Before a plate leaves the kitchen, someone checks it. A bad plate goes back; it never reaches the table. That's a **check that blocks delivery**.
- If the fish supplier is late, a runner calls again in five minutes. That's a **retry**. But if the fish is off, calling again won't fix it.
- Reprinting last month's menus for the archive isn't the same as handing them to today's customers. Rebuilding history without re-sending it is a **backfill**.

The Daily Sales Flash is a plate that leaves the kitchen every morning at 6:30. This chapter is about making sure it's the right plate.

---

## 46.1 From scheduled scripts to pipelines

The simplest scheduler is **cron**, which you used in Chapter 20 (section 20.7): the tool on Linux and macOS that runs a command at set times. A cron line such as `30 6 * * * cd /opt/riverstone && .venv/bin/python daily_flash.py` runs the Flash script at 6:30 every morning, by the server's clock. cron starts in your home folder with almost no settings, so the line first moves into the project folder and then names the project's own Python, as Chapter 20 explained. Windows Task Scheduler (Chapter 20) and Apps Script's time-driven triggers (Chapter 19, section 19.13) do the same job.

For a single script, that's often enough. Problems start when there are several steps that depend on each other:

- **Order.** If orders load at 6:00 and the Flash runs at 6:30, what happens on the day orders take 40 minutes?
- **Failure handling.** If the order-line load fails, does the Flash still run on stale data?
- **Retries.** If the CRM drops the connection, who tries again?
- **Re-running.** If you fix a bug and re-run, do you get duplicate rows or duplicate emails?
- **History.** Which runs succeeded last week? How long did each step take? What did it load?
- **Backfills.** How do you rebuild March after fixing a calculation, without re-sending March's emails?
- **Visibility.** Which reports depend on the dispatch file? If it breaks, what else is affected?

An orchestrator answers all of these in one place.

| Need | Cron plus scripts | An orchestrator |
|---|---|---|
| Run steps in dependency order | You wire it by hand, often with time gaps | Declared once; the orchestrator waits for upstream steps |
| Skip downstream steps when something fails | Each script has to check | Built in |
| Retry transient failures | Custom code in every script | A retry policy per step |
| Run history, logs, durations | Scattered log files, if any | Every run recorded and searchable |
| Re-run one day, or rebuild a date range | Manual, error-prone | Partitions and backfills |
| See what depends on what | In people's heads | A graph you can view |
| Alert the right person | Custom code | Failure hooks and sensors (section 46.2) |

> **Simplification note.** Cron isn't wrong. A single report with no dependencies, run by one person who checks it, doesn't need an orchestrator. Section 46.9 covers when plain scheduling is the better choice.

---

## 46.2 The core ideas

### Pipelines as graphs

A pipeline is a **directed acyclic graph** (DAG): a set of steps connected by arrows that show which step needs which, with no loops. "Acyclic" means you can never follow the arrows back to where you started, so there's always a valid order to run things in.

You met a DAG in Chapter 32: dbt built its models in the order their `ref()`s implied. Try the idea by hand with four boxes: orders, order lines, Flash, and deliver. The Flash needs orders and order lines; delivery needs the Flash. Two run orders are valid: orders, order lines, Flash, deliver; or order lines, orders, Flash, deliver. Both work, because orders and order lines don't need each other. Now add one more arrow, from deliver back to orders ("load orders only after the Flash has gone out"). Orders now needs deliver, deliver needs the Flash, and the Flash needs orders: there's no step you can start with, so no valid order exists. That loop is a **cycle**, and it's why a pipeline must be acyclic.

![A graph of the Riverstone daily pipeline. Four ingestion assets on the left: raw_orders, raw_order_items and raw_crm_leads bring whole tables up to date on every run, and raw_dispatch loads one day's file. Arrows from raw_orders and raw_order_items lead to daily_flash. A check, flash_matches_erp, is attached to daily_flash and marked as blocking. An arrow from daily_flash leads to deliver_flash, which writes to the outbox. raw_dispatch and raw_crm_leads have no arrows into the Flash. A schedule label at the top says 06:30 Asia/Kolkata, and that the 6:30 run on 6 January builds partition 2026-01-05.](figures/fig46-1-riverstone-pipeline-graph.svg)

*Figure 46.1 — Riverstone's daily pipeline as a graph. Notice what the Flash does and doesn't depend on: a problem with the dispatch file shouldn't stop the sales numbers.*

### Tasks and assets

There are two ways to think about the steps.

- **Task-based** orchestrators, such as Airflow, describe *what to run*: "run the load script, then run the report script". The data each task produces is implied.
- **Asset-based** orchestrators, such as Dagster, describe *what should exist*: "the table `raw.orders` should exist, built from the ERP; the `daily_flash` table depends on `raw.orders` and `raw.order_items`". An **asset** is a piece of data that the pipeline produces and keeps: a table, a file, a model, a report.

Both work, and both end up as a DAG. The asset view makes it easier to answer questions such as "which reports use this table?" and "is this table up to date?", which is why this chapter builds in Dagster. Section 46.8 shows the same pipeline written as Airflow tasks.

### Schedules, time zones, and partitions

A **schedule** says when a pipeline runs. It's usually written as a **cron expression**: the five fields you met in Chapter 20, for minute, hour, day of month, month, and day of week.

| Expression | Meaning |
|---|---|
| `30 6 * * *` | 6:30 every day |
| `0 7 * * 1` | 7:00 every Monday |
| `0 */2 * * *` | Every two hours, on the hour |
| `15 22 1 * *` | 10:15 p.m. on the 1st of every month |

A cron expression means nothing without a **time zone**, as Chapter 20 found with cron on a server. Servers usually run in **UTC** (Coordinated Universal Time); Riverstone runs on **IST** (India Standard Time, `Asia/Kolkata`), which is UTC plus 5 hours 30 minutes. A schedule of `30 6 * * *` in UTC would run at noon in Mumbai.

A **partition** is one slice of the pipeline's work that runs as a unit, most often one day. Partitioning means each run knows exactly which day it's building, so you can re-run 5 January without touching 2 January, and rebuild a whole month one day at a time. This isn't the `PARTITION BY` of Chapter 13's window functions (section 13.3): here a partition is one day's slice of the pipeline's work. Chapter 48 uses the word a third way, for the pieces of a large dataset spread across machines.

> **Watch out: "yesterday" depends on where you are.** At 3:00 a.m. IST on 6 January, it's still 5 January in UTC. A pipeline that computes "yesterday" from the server clock in UTC will build the wrong day for five and a half hours every night. Set the time zone explicitly on schedules and partitions, and pass the partition date into every step that works on one day, instead of reading the clock.

### Sensors: runs triggered by events

A schedule starts a run because the clock says so. A **sensor** starts one because something happened. It's a small function that the orchestrator calls every few minutes; if the function finds something (a new file, a finished upstream job, a failed run), it asks for a run or sends a message. The dispatch file that arrives late is the classic case: instead of guessing a time, a sensor watches the folder and starts the dispatch load when the file appears.

Someone has to watch the clock and call the sensors, even when nobody is looking at the pipeline. In Dagster that's the **daemon**: a background program that checks the schedules and sensors and starts the runs they ask for. Section 46.6 builds a sensor.

---

## 46.3 Building Riverstone's daily pipeline

### Setting up

Chapter 45 set up the practice source, `riverstone_source`, and the practice CRM API. This chapter reuses both, and adds Dagster.

**Step 1. Your practice folder.** As in Chapter 45, copy the folder `companion/ch46` and paste it inside `work`, so you have `work/ch46`. If you made a `.env` file in `work/ch45` (Chapter 45, section 45.2), copy it into `work/ch46` too: this chapter's files read the same `RIVERSTONE_SOURCE` connection string.

**Step 2. Install Dagster.** Open a terminal, go into your practice folder, and activate the book's virtual environment:

<!-- run: none -->
```
# terminal
$ cd work/ch46
$ source ../../.venv/bin/activate
$ python -m pip install dagster==1.13.23 dagster-webserver==1.13.23
```

- **`dagster`** is the library you write pipelines with: assets, checks, schedules, and sensors, and the code that runs them.
- **`dagster-webserver`** is the local web page that shows your pipeline, its runs, and its schedules. You need it for the `dagster dev` command at the end of this section; without it, `dagster dev` stops with an error.
- `==1.13.23` asks for the version used for this chapter's outputs. Dagster works on Windows, macOS, and Linux; on Windows PowerShell, activate with `..\..\.venv\Scripts\Activate.ps1`, as in Chapter 45.

Add both packages to your `requirements.txt`, one per line. Then check the install:

```
# terminal
$ dagster --version
dagster, version 1.13.23
```

If the terminal says it can't find `dagster`, the environment wasn't active when you installed: activate it and install again.

**Step 3. A new notebook.** If Chapter 45's notebook is still open, shut down its kernel first. It holds its own warehouse file open and its practice API on port 8045, and a second notebook can't use either while the first one has them. Then create a new notebook, choose the `.venv` kernel, and save it as `ch46.ipynb` in `work/ch46`. Run every code block in this chapter as its own cell, top to bottom, without restarting the kernel.

The practice folder holds these files:

| File | What it does |
|---|---|
| `reset_ch46.py` | Recreates `riverstone_source`, and empties the warehouse, the `outbox` folder (where delivered reports go), and the `alerts` folder |
| `ingest.py` | Your Chapter 45 loads, tidied into functions (next subsection) |
| `riverstone_pipeline.py` | The finished pipeline as one file, for Dagster's web page (end of this section) |
| `apply_day.py`, `make_files.py`, `mock_crm_api.py` | Copied from Chapter 45 |

### What's in `ingest.py`

Every pipeline step in this chapter calls a function from `ingest.py`, so read it before you use it. It's your Chapter 45 project, tidied into functions. It starts with three settings:

<!-- run: none -->
```python
SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
BROKEN_ITEMS_SYNC = False    # section 46.7 turns this on: a faulty order-line load
CONFIRMED_RENAMES = {}       # section 46.7 fills this in: a confirmed column rename
```

- `SRC` is the connection string, read from the environment (your `.env` file) as in Chapter 45.
- `BROKEN_ITEMS_SYNC` and `CONFIRMED_RENAMES` are two **switches** this chapter flips to simulate a fault and a fix. Nothing uses them until section 46.7.

Then two small functions for the source:

<!-- run: none -->
```python
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
```

- `fetch_rows()` is Chapter 45's function (section 45.3) with one change: it returns **just the rows**, not `(columns, rows)`. `params` holds the values for any `%s` placeholders in the SQL, as in Chapter 45. So `fetch_rows(sql)[0]` is the first row.
- `run_sql()` runs a statement that changes the source and commits it. Section 46.5 uses it to correct an order in the ERP.

The tables are loaded by the hash comparison and upsert from Chapter 45, section 45.5:

<!-- run: none -->
```python
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
```

- `TABLES` (a dictionary near the top of the file) holds, for `orders` and `order_items`, the key column, the columns to copy, and the warehouse table's column definitions.
- `row_hash()` is section 45.5's row fingerprint, computed in Python: the row's values joined with `|`, then `md5`. Both sides are built by the same Python code, so they match whenever the values match.
- `sync_table()` reads the **whole** table from the source and from the warehouse, and sorts every key into new, changed, or deleted, exactly as in section 45.5. Then it applies all of them with an upsert and deletes, inside one transaction. It returns the three counts, so a step can report them.
- The `BROKEN_ITEMS_SYNC` line is the simulated bug: when the switch is on, the order-line load quietly does nothing.

The dispatch file is loaded with the column check from section 45.8, and the day's rows are replaced:

<!-- run: none -->
```python
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
```

- The function works on **one day's file**, `exports/dispatch_<day>.csv`. A day with no file (a holiday, a weekend) isn't an error: it returns a message saying so.
- `DESCRIBE SELECT * FROM read_csv(...)` lists the file's columns, as in section 45.7. `renamed` maps each file column to the name the load expects, using `CONFIRMED_RENAMES` for any rename someone has confirmed. `EXPECTED_DISPATCH` (near the top of the file) lists the six columns the file must have. If any is missing, the load **stops with a clear error** instead of guessing (section 45.8).
- `qty_column` is the file's name for the quantity column: `qty_units`, or whatever a confirmed rename says.
- The load **replaces** the day's rows: delete that day, then insert the file, in one transaction. Running it again gives the same rows, so it's idempotent. It doesn't skip unchanged files by their hash, as section 45.5's file log did; the file is small, and replacing it is simpler.

The CRM leads come from the practice API, as in section 45.9:

<!-- run: none -->
```python
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
```

- `fetch_leads()` is section 45.9's pagination loop. `base` is the API's address, and `headers` carries the token in the `Authorization` header, as in section 45.9. The token defaults to the `CRM_API_TOKEN` environment variable, or the practice token if it isn't set. It waits and tries again when the API answers **429**, and `raise_for_status()` turns any other error, such as a 401, into an exception.
- `load_leads()` replaces the whole `raw.crm_leads` table with the leads it's given, using Chapter 45's table definition. `CURRENT_DATE` fills `loaded_for` with the day the load ran. It returns the number of rows now in the table.

### The first cell

With `ingest.py` read, start the notebook:

```python
import os, hashlib
import duckdb, requests, dagster as dg
from dotenv import load_dotenv

load_dotenv()
from reset_ch46 import reset
from apply_day import apply_day
from mock_crm_api import start_server
import ingest

STEP_ORDER = ["raw_orders", "raw_order_items", "raw_dispatch", "raw_crm_leads",
              "daily_flash", "flash_matches_erp", "deliver_flash"]
RUN_LOG = []

def log(step, message):
    RUN_LOG.append((step, message))

def show_log():
    """Print this run's messages in pipeline order, then clear them."""
    for step, message in sorted(RUN_LOG, key=lambda e: STEP_ORDER.index(e[0])):
        print(message)
    RUN_LOG.clear()

reset()
apply_day(1)                          # the ERP's business day of 2 January
wh = duckdb.connect("warehouse/riverstone_wh.duckdb")
api = start_server()
print("environment ready")
```

```
environment ready
```

**How it works, line by line.**

- The imports are Chapter 45's, plus `dagster`, imported under the short name `dg`, as its documentation does. `requests` is there for its error type, which section 46.6 uses. `load_dotenv()` reads your `.env` file, if there is one, before the companion files read `RIVERSTONE_SOURCE`.
- The new part is a small **run log**. Each step records a message with `log()`, and `show_log()` prints them in pipeline order. Steps that don't depend on each other can run in any order, so printing messages as they happen would show them in a different sequence each time. `sorted(..., key=lambda e: STEP_ORDER.index(e[0]))` sorts the messages by their step's position in `STEP_ORDER` (the `lambda` from Chapter 18). Dagster keeps its own detailed event log too; this one keeps the book's outputs short.
- `reset()` rebuilds `riverstone_source` and empties the four folders. `apply_day(1)` then plays the ERP's business day of 2 January, as in Chapter 45: two new orders and two status changes. The story starts on the **morning of 3 January**, with 2 January's orders in the ERP and nothing yet in the warehouse.
- `start_server()` starts the practice CRM API in the background, and `api` keeps hold of it so the last cell of section 46.7 can stop it.

> **Tool note.** Outputs in this chapter were produced with Python 3.14.7, Dagster 1.13.23, DuckDB 1.5.6, psycopg2 2.9.13, requests 2.33.1, and PostgreSQL 16. Dagster's API changes between versions; if a name doesn't exist in your version, check its documentation for the current equivalent.

### A first asset

A Dagster asset is an ordinary Python function with `@dg.asset` on the line above it. That line is a **decorator** (Chapter 29, section 29.5): it hands the function to Dagster, which from then on runs it for you and records the result. The function's name becomes the asset's name. Start with the two ERP tables:

```python
@dg.asset
def raw_orders():
    new, changed, deleted = ingest.sync_table(wh, "orders")
    log("raw_orders", f"raw_orders: {new} new, {changed} changed, {deleted} deleted")

@dg.asset
def raw_order_items():
    new, changed, deleted = ingest.sync_table(wh, "order_items")
    log("raw_order_items", f"raw_order_items: {new} new, {changed} changed, {deleted} deleted")

result = dg.materialize([raw_orders, raw_order_items])
show_log()
print("run succeeded:", result.success)
```

```
raw_orders: 177 new, 0 changed, 0 deleted
raw_order_items: 333 new, 0 changed, 0 deleted
run succeeded: True
```

**How it works.**

- Each function calls `ingest.sync_table()` and logs the three counts it returns.
- `dg.materialize([...])` runs the listed assets once, now, inside this notebook. **Materialize** is Dagster's word for "build this asset". It returns a result object, and `result.success` is `True` only if every step succeeded.

**Reading it.** The first run loaded all 177 orders and 333 order lines into the empty warehouse: Chapter 45's 175 orders and 330 lines, plus the two orders and three lines of 2 January.

Below your printed lines, the notebook also shows many lines of Dagster's own event log, one or more for each thing that happened in the run: the step started, the asset was stored, the step succeeded. That's Dagster's record of the run, and the book leaves it out. `materialize()` keeps that record only while Python is running; `dagster dev` (at the end of this section) stores every run permanently.

These two assets always bring the whole table up to date, whichever day the pipeline is building: Chapter 45's hash comparison finds every change, whenever it was made. They don't need to know the day.

### One partition per day

Some work does belong to one day. The dispatch file is one day's file, and the Flash reports one day's orders. For those, Dagster needs to know which days exist:

```python
daily = dg.DailyPartitionsDefinition(start_date="2026-01-01", end_date="2026-01-06", timezone="Asia/Kolkata")
print(daily.get_partition_keys())
```

```
['2026-01-01', '2026-01-02', '2026-01-03', '2026-01-04', '2026-01-05']
```

- `DailyPartitionsDefinition` declares **one partition per day**, from `start_date` 1 January to 5 January 2026 (the `end_date`, 6 January, isn't included), **in IST** (`timezone`). A real pipeline would have no end date; this one stops so the practice data stays small.
- `get_partition_keys()` lists the days. Each **partition key** is the day as text, which is what a step receives when it builds that day.

Now the dispatch file, as a daily asset:

```python
@dg.asset(partitions_def=daily)
def raw_dispatch(context):
    day = context.partition_key
    try:
        outcome = ingest.load_dispatch(wh, day)
    except ValueError as e:
        log("raw_dispatch", f"[{day}] raw_dispatch: FAILED, {e}")
        raise
    log("raw_dispatch", f"[{day}] raw_dispatch: {outcome}")

result = dg.materialize([raw_dispatch], partition_key="2026-01-02")
show_log()
print("run succeeded:", result.success)
```

```
[2026-01-02] raw_dispatch: 5 rows (the day's rows replaced)
run succeeded: True
```

**How it works, line by line.**

- `@dg.asset(partitions_def=daily)` is the same decorator, given a setting: this asset is built one day at a time.
- `context` is passed in by Dagster when it runs the function. It has to be the function's first parameter and be called `context`; that name is how Dagster knows to pass it. `context.partition_key` is the day being built, as text: `"2026-01-02"`. The step uses it instead of reading the clock.
- `try` / `except ValueError as e` catches the schema-change error from `load_dispatch()` and logs it. The bare **`raise`** on its own line then raises the **same** error again, so Dagster still marks the step as failed. Log it, then re-raise it: catching an error without re-raising would hide the failure.
- `dg.materialize(..., partition_key="2026-01-02")` builds that one day.

**Reading it.** The 2 January file's 5 rows loaded, replacing anything that was there for that day.

### A step that talks to the CRM

The last ingestion asset calls the CRM API, which can drop a connection. First, two practice settings for it:

```python
CRM = {"fail_next": False, "token": os.environ.get("CRM_API_TOKEN", "practice-token-45")}
```

`CRM` is a dictionary of two settings. `fail_next` lets section 46.6 simulate a dropped connection. `token` is the CRM token, read from `CRM_API_TOKEN` with the practice token as the default, as in Chapter 45, section 45.9; section 46.6 swaps in a wrong one. It's a dictionary rather than two plain variables because the step will **change** `fail_next`, and a function can change what's inside a dictionary defined outside it without any extra keyword. (Assigning to a plain outside variable would need `global`.)

Now the step. Dagster can retry it when it fails:

```python
@dg.asset(retry_policy=dg.RetryPolicy(max_retries=3, delay=1))
def raw_crm_leads(context):
    attempt = context.retry_number + 1
    try:
        if CRM["fail_next"]:
            CRM["fail_next"] = False
            raise ConnectionError("connection dropped")
        leads = ingest.fetch_leads(token=CRM["token"])
    except Exception as e:
        log("raw_crm_leads", f"raw_crm_leads: FAILED, {e} (attempt {attempt})")
        raise
    n = ingest.load_leads(wh, leads)
    log("raw_crm_leads", f"raw_crm_leads: {n} leads (attempt {attempt})")

result = dg.materialize([raw_crm_leads])
show_log()
print("run succeeded:", result.success)
```

```
raw_crm_leads: 43 leads (attempt 1)
run succeeded: True
```

**How it works, line by line.**

- `retry_policy=dg.RetryPolicy(max_retries=3, delay=1)` gives this step a **retry policy**: if it raises an error, Dagster runs it again, up to three more times, waiting one second between attempts.
- `context.retry_number` counts the retries, starting from 0 on the first attempt, so `attempt` is 1, 2, 3, or 4.
- The `try` block does the risky part: the simulated drop, then `fetch_leads()`. The `except` logs whatever went wrong and re-raises it, as in `raw_dispatch`, so Dagster sees the failure and can retry.
- `load_leads()` replaces the table and returns the row count.

**Reading it.** All 43 leads arrived on the first attempt. The practice API's first answer for page 2 is a 429, as in Chapter 45; `fetch_leads()` waited and asked again inside the same attempt, so the step never failed.

### The Flash and its check

The Flash is built by one query, written once with gaps for the table names, so the **same** definition runs against the warehouse and against the ERP:

```python
FLASH_SQL = """
    SELECT COUNT(DISTINCT o.order_id) AS orders_booked,
           ROUND(COALESCE(SUM(i.quantity * i.unit_price * (1 - i.discount_pct / 100)), 0), 2)
               AS revenue_booked
    FROM {orders} AS o
    JOIN {items} AS i ON i.order_id = o.order_id
    WHERE o.order_date = {day}
      AND o.status <> 'Cancelled'"""

INSERT_FLASH = ("INSERT INTO mart.daily_flash SELECT CAST(? AS DATE), * FROM ("
                + FLASH_SQL.format(orders="raw.orders", items="raw.order_items", day="?") + ")")
print(INSERT_FLASH)
```

```
INSERT INTO mart.daily_flash SELECT CAST(? AS DATE), * FROM (
    SELECT COUNT(DISTINCT o.order_id) AS orders_booked,
           ROUND(COALESCE(SUM(i.quantity * i.unit_price * (1 - i.discount_pct / 100)), 0), 2)
               AS revenue_booked
    FROM raw.orders AS o
    JOIN raw.order_items AS i ON i.order_id = o.order_id
    WHERE o.order_date = ?
      AND o.status <> 'Cancelled')
```

**How it works, line by line.**

- `FLASH_SQL` counts the day's orders and adds up quantity × unit price × (1 − discount%), leaving out cancelled orders. That's **net bookings**: Chapter 3 showed that bookings can be counted with or without cancelled orders, and its KPI table leaves them out; the Flash does the same, as Chapter 20's Flash did. Chapter 20's Flash had four numbers; this one keeps two, so the outputs stay short.
- `ROUND(..., 2)` rounds revenue to paise. Both sides of the check below will run this same query, so both round the same way. Compare numbers the way they'll be reported: section 45.5 made the same point about hashes, where both sides must build the value identically.
- `{orders}`, `{items}`, and `{day}` are gaps that `.format()` fills with text. It fills in **table names**, which placeholders can't do. The day is different: it's a value, so it becomes a `?` placeholder, and the real day is passed separately, as Chapter 45 did.
- `INSERT_FLASH` puts the day in front of the query's two numbers and inserts the row. The printout shows the finished statement: the table names are filled in, and two `?`s wait for values, the date and the `WHERE` day, so it's run with `[day, day]`. `CAST(? AS DATE)` turns the text `"2026-01-02"` into a date.

Now the asset that runs it:

```python
@dg.asset(partitions_def=daily, deps=[raw_orders, raw_order_items])
def daily_flash(context):
    day = context.partition_key
    wh.execute("CREATE SCHEMA IF NOT EXISTS mart")
    wh.execute("""CREATE TABLE IF NOT EXISTS mart.daily_flash (
                      flash_date DATE, orders_booked INTEGER, revenue_booked DECIMAL(12,2))""")
    wh.execute("BEGIN")
    try:
        wh.execute("DELETE FROM mart.daily_flash WHERE flash_date = ?", [day])
        wh.execute(INSERT_FLASH, [day, day])
        wh.execute("COMMIT")
    except Exception:
        wh.execute("ROLLBACK")
        raise
    n, rev = wh.execute("SELECT orders_booked, revenue_booked FROM mart.daily_flash WHERE flash_date = ?",
                        [day]).fetchone()
    log("daily_flash", f"[{day}] daily_flash: orders={n}, revenue=Rs {rev:,.2f}")

result = dg.materialize([daily_flash], partition_key="2026-01-02")
show_log()
```

```
[2026-01-02] daily_flash: orders=2, revenue=Rs 38,710.00
```

**How it works, line by line.**

- `deps=[raw_orders, raw_order_items]` declares the Flash's **dependencies**: when they're in the same run, it runs only after both have succeeded.
- The day's row is built with **delete-then-insert inside one transaction** (`BEGIN`, `COMMIT`, and `ROLLBACK` if anything fails, as in Chapter 12, section 12.13). Re-running a day replaces that day's row, and a failure halfway leaves the table as it was. Section 46.4 tests both claims.
- The step then reads its own row back and logs it. `{rev:,.2f}` prints the number with commas and two decimals.

**Reading it.** The 2 January Flash: 2 orders, ₹38,710.00.

> **Dialect note: rupees in outputs.** The code prints `Rs` rather than the ₹ symbol, because some terminals and email systems don't display ₹ correctly. The prose uses ₹ as elsewhere in the book. Python's `,` format groups digits in thousands, so an amount of a lakh or more prints as, say, `Rs 154,840.00`; the prose writes the same amount the Indian way, ₹1,54,840.00.

A **check** is a test attached to an asset. This one recomputes the Flash from the ERP and compares:

```python
@dg.asset_check(asset=daily_flash, blocking=True)
def flash_matches_erp(context):
    day = context.partition_key
    src_n, src_rev = ingest.fetch_rows(
        FLASH_SQL.format(orders="orders", items="order_items", day="%s"), [day])[0]
    rows = wh.execute("SELECT orders_booked, revenue_booked FROM mart.daily_flash WHERE flash_date = ?",
                      [day]).fetchall()
    passed = len(rows) == 1 and rows[0][0] == src_n and rows[0][1] == src_rev
    if len(rows) == 1:
        wh_text = f"orders={rows[0][0]}, revenue=Rs {rows[0][1]:,.2f}"
    else:
        wh_text = f"{len(rows)} rows"
    log("flash_matches_erp", f"[{day}] check flash_matches_erp: {'PASSED' if passed else 'FAILED'} "
                             f"(ERP: orders={src_n}, revenue=Rs {src_rev:,.2f} | warehouse: {wh_text})")
    return dg.AssetCheckResult(passed=passed)

result = dg.materialize([daily_flash, flash_matches_erp], partition_key="2026-01-02")
show_log()
```

```
[2026-01-02] daily_flash: orders=2, revenue=Rs 38,710.00
[2026-01-02] check flash_matches_erp: PASSED (ERP: orders=2, revenue=Rs 38,710.00 | warehouse: orders=2, revenue=Rs 38,710.00)
```

**How it works, line by line.**

- `@dg.asset_check(asset=daily_flash, blocking=True)` attaches the check to the Flash. `blocking=True` means that if the check fails, **nothing downstream of `daily_flash` runs**.
- The ERP side runs the same `FLASH_SQL` against the source tables, `orders` and `order_items`. psycopg2 spells the placeholder `%s` instead of `?`, which is why the day gap is filled with `"%s"` here. `[0]` takes the first (and only) row, which holds the two numbers.
- The warehouse side reads the day's rows. The check passes only if there's **exactly one** row and both numbers match.
- `wh_text` describes the warehouse side for the message: the numbers when there's one row, or the row count when there isn't.
- `dg.AssetCheckResult(passed=passed)` reports the result to Dagster.

**Reading it.** The check recomputed the numbers from the ERP, and they matched.

### Delivery

Delivery writes the report to the `outbox` folder, which stands in for the email that Chapter 20 showed how to send. It must never send the same report twice, so it keeps a **delivery log**: a table recording, for every report sent, a hash of its content. First, the report itself:

```python
def flash_body(day):
    n, rev = wh.execute("SELECT orders_booked, revenue_booked FROM mart.daily_flash WHERE flash_date = ?",
                        [day]).fetchone()
    body = (f"Riverstone Daily Sales Flash - {day}\n"
            f"Orders booked: {n}\n"
            f"Net bookings (excl. cancelled, net of discounts): Rs {rev:,.2f}\n")
    return rev, body

rev, body = flash_body("2026-01-02")
print(body)
print("content hash:", hashlib.sha256(body.encode()).hexdigest()[:16], "...")
```

```
Riverstone Daily Sales Flash - 2026-01-02
Orders booked: 2
Net bookings (excl. cancelled, net of discounts): Rs 38,710.00

content hash: bb49a92871a565ba ...
```

- `flash_body()` reads the day's row and builds the report's text, returning the revenue and the text.
- `hashlib.sha256(body.encode()).hexdigest()` is the content fingerprint from Chapter 45, section 45.5: any change to the report, even one digit, gives a completely different hash. The print shows only its first 16 characters.

Now the delivery step:

```python
@dg.asset(partitions_def=daily, deps=[daily_flash])
def deliver_flash(context):
    day = context.partition_key
    rev, body = flash_body(day)
    digest = hashlib.sha256(body.encode()).hexdigest()
    wh.execute("""CREATE TABLE IF NOT EXISTS mart.delivery_log (
                      flash_date DATE, delivery_no INTEGER, content_sha VARCHAR,
                      revenue DECIMAL(12,2), file_name VARCHAR)""")
    sent = wh.execute("""SELECT content_sha, revenue FROM mart.delivery_log
                         WHERE flash_date = ? ORDER BY delivery_no""", [day]).fetchall()
    if digest in [s[0] for s in sent]:
        log("deliver_flash", f"[{day}] deliver_flash: already delivered, skipped")
        return
    if sent:
        old = sent[-1][1]
        body = (f"CORRECTION to the Flash sent earlier for {day}: "
                f"revenue changed from Rs {old:,.2f} to Rs {rev:,.2f}.\n\n" + body)
        name = f"flash_{day}_correction_{len(sent)}.txt"
    else:
        name = f"flash_{day}.txt"
    with open(f"outbox/{name}", "w") as f:
        f.write(body)
    wh.execute("INSERT INTO mart.delivery_log VALUES (?, ?, ?, ?, ?)", [day, len(sent) + 1, digest, rev, name])
    log("deliver_flash", f"[{day}] deliver_flash: wrote outbox/{name}")
```

**How it works, line by line.**

- `deps=[daily_flash]`: delivery runs only after the Flash has been built, and, because the check is blocking, only after the check has passed.
- `digest` is the report's content hash. `mart.delivery_log` has one row per report sent: the day, a delivery number (1 for the first, 2 for the next), the hash, the revenue, and the file name.
- `sent` is the list of earlier deliveries for this day, oldest first. If this exact content was already delivered (`digest in [...]`), the step logs that and stops: `return` ends the function early.
- If something was sent for the day but with **different** content, this is a **correction**. The report gets a first line saying what changed, from the last revenue sent (`sent[-1][1]`, the last delivery's revenue) to the new one, and a file name that says `correction`.
- The step writes the file, records the delivery, and logs it. The step has no output of its own yet; it runs in the first run below.

### Declaring the job and its schedule

```python
ALL = [raw_orders, raw_order_items, raw_dispatch, raw_crm_leads, daily_flash, flash_matches_erp, deliver_flash]
flash_job = dg.define_asset_job("daily_flash_job", selection=[raw_orders, raw_order_items, raw_dispatch,
                                                               raw_crm_leads, daily_flash, deliver_flash])
flash_schedule = dg.build_schedule_from_partitioned_job(flash_job, hour_of_day=6, minute_of_hour=30)
defs = dg.Definitions(assets=[raw_orders, raw_order_items, raw_dispatch, raw_crm_leads, daily_flash, deliver_flash],
                      asset_checks=[flash_matches_erp], jobs=[flash_job], schedules=[flash_schedule])
schedule = defs.resolve_schedule_def("daily_flash_job_schedule")
print("job     :", flash_job.name)
print("schedule:", schedule.cron_schedule, schedule.execution_timezone)
```

```
job     : daily_flash_job
schedule: 30 6 * * * Asia/Kolkata
```

**How it works, line by line.**

- `ALL` lists every step, for running the whole pipeline in this notebook.
- A **job** is a named selection of assets that run together. `define_asset_job` builds one. Checks on the selected assets come along automatically, so the list doesn't name the check, and the job takes its partitions from the assets.
- `build_schedule_from_partitioned_job` creates a schedule for the job: every day at 6:30 (`hour_of_day=6, minute_of_hour=30`), in the time zone of the partitions, `Asia/Kolkata`.
- `Definitions` bundles everything Dagster needs to know about: the assets, the checks (`asset_checks`), the jobs, and the schedules. Dagster checks the graph when it's built, so a missing dependency or a duplicate name fails here instead of at 6:30 a.m.
- `resolve_schedule_def()` fetches the finished schedule by its name, which Dagster made from the job's name plus `_schedule`.

**Which day does the 6:30 run build?** Before you run the next cell, predict: on 3 January at 6:30, which partition will the schedule ask for?

```python
from datetime import datetime
from zoneinfo import ZoneInfo

tick = datetime(2026, 1, 3, 6, 30, tzinfo=ZoneInfo("Asia/Kolkata"))
tick_context = dg.build_schedule_context(scheduled_execution_time=tick, repository_def=defs.get_repository_def())
print([r.partition_key for r in schedule.evaluate_tick(tick_context).run_requests])
```

```
['2026-01-02']
```

- `tick` is 6:30 a.m. on 3 January, India time. `tzinfo=ZoneInfo("Asia/Kolkata")` attaches the time zone, as in Chapter 20, so Python knows which 6:30 is meant.
- `build_schedule_context` builds the information the daemon would hand the schedule at that moment: the time of the tick (`scheduled_execution_time`) and the definitions it belongs to (`repository_def`, which `defs.get_repository_def()` supplies), and `evaluate_tick` asks the schedule what it would run. `run_requests` is the list of runs it asks for; the code prints each one's partition.

**Reading it.** The 6:30 run on 3 January builds **2 January**, the last complete day, not 3 January. That's what a morning Flash about yesterday needs: 3 January has barely started. Manual runs, like the ones in this chapter, can build any day you name.

### The first run

It's the morning of 3 January, and the ERP has had its 2 January business day. Run the whole pipeline for 2 January:

```python
result = dg.materialize(ALL, partition_key="2026-01-02", raise_on_error=False)
show_log()
print("run succeeded:", result.success)
print()
print(open("outbox/flash_2026-01-02.txt").read())
```

```
raw_orders: 0 new, 0 changed, 0 deleted
raw_order_items: 0 new, 0 changed, 0 deleted
[2026-01-02] raw_dispatch: 5 rows (the day's rows replaced)
raw_crm_leads: 43 leads (attempt 1)
[2026-01-02] daily_flash: orders=2, revenue=Rs 38,710.00
[2026-01-02] check flash_matches_erp: PASSED (ERP: orders=2, revenue=Rs 38,710.00 | warehouse: orders=2, revenue=Rs 38,710.00)
[2026-01-02] deliver_flash: wrote outbox/flash_2026-01-02.txt
run succeeded: True

Riverstone Daily Sales Flash - 2026-01-02
Orders booked: 2
Net bookings (excl. cancelled, net of discounts): Rs 38,710.00
```

- `raise_on_error=False` tells `materialize()` to return the result even when a step fails, instead of stopping the notebook with an error. The result's `success` then says what happened. Every run from here on uses it.

**Reading it.** The steps ran in dependency order. The ingestion steps found nothing new, because you loaded everything while building them. The dispatch file's rows were replaced, and the leads reloaded. The Flash shows 2 orders booked for ₹38,710.00. The check recomputed the same numbers from the ERP and they matched, so delivery ran and wrote the report.

Notice the dates in the log: the lines that start with `[2026-01-02]` belong to one day's partition. The ingestion lines have no date, because those steps always bring whole tables up to date.

### Running it again

What happens if the scheduler runs the same day twice, or someone presses "run" again?

```python
result = dg.materialize(ALL, partition_key="2026-01-02", raise_on_error=False)
show_log()
print("run succeeded:", result.success)
print("flash rows for the day:", wh.execute("SELECT COUNT(*) FROM mart.daily_flash WHERE flash_date = '2026-01-02'").fetchone()[0])
print("files in outbox:", sorted(os.listdir("outbox")))
```

```
raw_orders: 0 new, 0 changed, 0 deleted
raw_order_items: 0 new, 0 changed, 0 deleted
[2026-01-02] raw_dispatch: 5 rows (the day's rows replaced)
raw_crm_leads: 43 leads (attempt 1)
[2026-01-02] daily_flash: orders=2, revenue=Rs 38,710.00
[2026-01-02] check flash_matches_erp: PASSED (ERP: orders=2, revenue=Rs 38,710.00 | warehouse: orders=2, revenue=Rs 38,710.00)
[2026-01-02] deliver_flash: already delivered, skipped
run succeeded: True
flash rows for the day: 1
files in outbox: ['flash_2026-01-02.txt']
```

Nothing changed: no rows loaded, one Flash row for the day, and delivery recognized that exactly this report was already sent. That's the behavior you want from every scheduled pipeline, and it isn't an accident. The next section shows what it takes.

### Running it in Dagster's web interface

`materialize()` is how you build and test a pipeline in a notebook. To see the graph, turn the schedule on, and keep a permanent history of runs, Dagster runs the same definitions from a **file**, with `dagster dev`. The practice folder has that file, `riverstone_pipeline.py`. It holds the same assets, check, job, and schedule, without the practice switches (`CRM`, `CRASH`), and with four differences from the notebook:

<!-- run: none -->
```python
WAREHOUSE = "warehouse/riverstone_wh.duckdb"

def warehouse():
    """Open the warehouse for one step; each step closes it again when it finishes."""
    return duckdb.connect(WAREHOUSE)

@dg.asset
def raw_orders(context):
    with warehouse() as wh:
        new, changed, deleted = ingest.sync_table(wh, "orders")
    context.log.info(f"raw_orders: {new} new, {changed} changed, {deleted} deleted")

# ... the other assets, the check, and the job follow the same pattern ...

defs = dg.Definitions(assets=[raw_orders, raw_order_items, raw_dispatch, raw_crm_leads, daily_flash, deliver_flash],
                      asset_checks=[flash_matches_erp], jobs=[flash_job], schedules=[flash_schedule],
                      sensors=[dispatch_file_sensor, flash_failure_alert],
                      executor=dg.in_process_executor)     # one step at a time: DuckDB allows one writer
```

- **Nothing runs when the file is loaded.** No `reset()`, no `apply_day()`, no API server: `dagster dev` loads the file to read the definitions, and it may load it more than once.
- **Each step opens the warehouse itself** and closes it at the end (`with warehouse() as wh:`). `dagster dev` runs the pipeline in its own Python process, not in your notebook, so there's no shared `wh` to borrow.
- **Steps run one at a time.** Left to itself, Dagster runs independent steps side by side, each in its own process. DuckDB lets only one process write to a file at a time, so two steps opening the warehouse together would fail with "Could not set lock on file". `executor=dg.in_process_executor` tells Dagster to run the steps one after another, in one process.
- **Steps log with `context.log.info()`**, Dagster's own log, instead of the notebook's `RUN_LOG`. The messages appear on each run's page.
- `Definitions` also lists the two sensors from section 46.6.

To run it:

1. Shut down the notebook's kernel, so it releases the warehouse file and port 8045.
2. In one terminal, in `work/ch46` with the environment active, start the practice API: `python mock_crm_api.py`.
3. In a second terminal, same folder: `dagster dev -f riverstone_pipeline.py`. When it's ready, it prints a line saying `Serving dagster-webserver on http://127.0.0.1:3000`. Leave both terminals running.
4. Open `http://127.0.0.1:3000` in your browser. **Assets** shows the graph, as in Figure 46.1. Choose **Materialize all**; for the daily assets, Dagster asks which partition to build: pick 2026-01-02.
5. Open **Automation** (the schedules and sensors page). Schedules and sensors start **stopped**, so nothing runs by surprise; switch `daily_flash_job_schedule` on to start it, and the two sensors of section 46.6 the same way. The practice partitions end on 5 January, so it won't find a new day to build; in a real pipeline, with no end date, it would run every morning at 6:30.

`dagster dev` starts two programs: the web server that draws the page, and the **daemon** (section 46.2) that fires schedules and sensors. It also keeps every run's history in a folder on your computer, so the runs are still there after you restart. Press Ctrl+C in each terminal to stop.

---

## 46.4 Idempotency, proven with a failure test

Chapter 45 defined an **idempotent** step as one you can run again with the same result. In a pipeline, the question that matters is sharper: **if a step fails halfway and is retried, is the result still correct?** The only honest way to answer is to make it fail on purpose.

![Two timelines side by side. On the left, the naive step: it inserts the day's row, then the worker is lost before the step reports success; the orchestrator retries, the step inserts the row again, and the table ends with two rows for 2 January and revenue of ₹77,420 instead of ₹38,710, marked with a cross. On the right, the safe step: begin transaction, delete the day's rows, the worker is lost between the DELETE and the INSERT, the transaction rolls back and the old row is still there; the retry commits, and the table ends with one row and ₹38,710, marked with a tick.](figures/fig46-2-failure-test-naive-vs-safe.svg)

*Figure 46.2 — The same kind of failure, two designs. The naive step's retry doubles the day; the safe step's retry is harmless.*

### A step that isn't idempotent

Here's a common first version of a report step: it **appends** the day's numbers. To test it, the step crashes *after* writing, as happens when a machine is lost or a network call times out after the database has already committed.

```python
CRASH = {"now": False}

@dg.asset(partitions_def=daily, deps=[raw_orders, raw_order_items])
def flash_naive(context):
    day = context.partition_key
    wh.execute("""CREATE TABLE IF NOT EXISTS mart.flash_naive (
                      flash_date DATE, orders_booked INTEGER, revenue_booked DECIMAL(12,2))""")
    wh.execute(INSERT_FLASH.replace("mart.daily_flash", "mart.flash_naive"), [day, day])
    if CRASH["now"]:
        raise RuntimeError("worker lost after writing (simulated)")

CRASH["now"] = True
first = dg.materialize([flash_naive], partition_key="2026-01-02", raise_on_error=False)
CRASH["now"] = False
second = dg.materialize([flash_naive], partition_key="2026-01-02", raise_on_error=False)
print("first run succeeded :", first.success)
print("second run succeeded:", second.success)
print(wh.execute("""SELECT COUNT(*) AS rows_for_day, SUM(revenue_booked) AS revenue_reported
                    FROM mart.flash_naive WHERE flash_date = '2026-01-02'""").fetchall())
```

```
first run succeeded : False
second run succeeded: True
[(2, Decimal('77420.00'))]
```

**How it works.** `flash_naive` inserts the day's row into its own table, `mart.flash_naive`, with the same insert as the Flash (`.replace()` swaps the table name in the SQL text). There's no delete first and no transaction. `CRASH` is a switch like `CRM`: when it's on, the step raises an error just after the insert. The cell runs the step once with the crash, then once without it, the way a scheduler's retry would.

**Reading it.** The first run failed, so the retry (here, a second run) did its job and succeeded. But the table now has **two rows** for 2 January, and anything that sums revenue reports **₹77,420.00**, exactly double the true ₹38,710.00. Nothing looks broken until someone compares the report with the ERP.

> **Try it.** In `flash_naive`, move the two lines `if CRASH["now"]:` and `raise ...` above the `INSERT`, re-run the cell that defines it, and run the test again. Does the naive step still double the revenue? What does that tell you about when a non-idempotent step is dangerous?

### Delete, then insert: the gap in the middle

The Flash in section 46.3 deletes the day's row and inserts it again, which can't double anything. But there's a moment between the delete and the insert when the day has **no row at all**. First, a small helper to look at the table between steps:

```python
def rows_for(day):
    return wh.execute("SELECT COUNT(*), SUM(revenue_booked) FROM mart.daily_flash WHERE flash_date = ?",
                      [day]).fetchall()

print(rows_for("2026-01-02"))
```

```
[(1, Decimal('38710.00'))]
```

`rows_for()` returns the number of Flash rows for a day and their total revenue: right now, one row and ₹38,710.00. Now crash between the delete and the insert, without a transaction:

```python
def build_flash_no_transaction(day, crash=False):
    wh.execute("DELETE FROM mart.daily_flash WHERE flash_date = ?", [day])
    if crash:
        raise RuntimeError("worker lost between DELETE and INSERT (simulated)")
    wh.execute(INSERT_FLASH, [day, day])

try:
    build_flash_no_transaction("2026-01-02", crash=True)
except RuntimeError as e:
    print("run failed:", e)
print("after the crash:", rows_for("2026-01-02"))
build_flash_no_transaction("2026-01-02")
print("after the retry:", rows_for("2026-01-02"))
```

```
run failed: worker lost between DELETE and INSERT (simulated)
after the crash: [(0, None)]
after the retry: [(1, Decimal('38710.00'))]
```

`build_flash_no_transaction()` is the Flash's delete-then-insert with no `BEGIN` or `COMMIT`: each statement is kept as soon as it runs. With `crash=True`, it stops between the two.

**Reading it.** After the crash, 2 January has **0 rows**, and `SUM` of nothing is `None`. If a dashboard refreshed at 6:31, it would show an empty day. The retry put the row back, but only because someone retried.

### The same step, made safe

Now the design from section 46.3: the delete and the insert inside one transaction. The same crash, at the same point:

```python
def build_flash_safely(day, crash=False):
    wh.execute("BEGIN")
    try:
        wh.execute("DELETE FROM mart.daily_flash WHERE flash_date = ?", [day])
        if crash:
            raise RuntimeError("worker lost between DELETE and INSERT (simulated)")
        wh.execute(INSERT_FLASH, [day, day])
        wh.execute("COMMIT")
    except Exception as e:
        wh.execute("ROLLBACK")
        print("run failed and rolled back:", e)

build_flash_safely("2026-01-02", crash=True)
print("after the crash:", rows_for("2026-01-02"))
build_flash_safely("2026-01-02")
print("after the retry:", rows_for("2026-01-02"))
```

```
run failed and rolled back: worker lost between DELETE and INSERT (simulated)
after the crash: [(1, Decimal('38710.00'))]
after the retry: [(1, Decimal('38710.00'))]
```

**Reading it.** When the step crashed, the transaction **rolled back**: the delete was undone, so the old row was still there, and anyone reading the table at that moment saw the right number. The retry then committed. There's one row, with the correct ₹38,710.00, before and after.

**How it works.** A **transaction** groups statements so they succeed or fail together (Chapter 12, section 12.13). `BEGIN` starts one; `COMMIT` makes it permanent; `ROLLBACK` discards everything since `BEGIN`. The combination of **replace the whole partition** and **one transaction** is the standard pattern for idempotent pipeline steps. Chapter 49 covers how warehouses guarantee it, under the name ACID.

### Patterns for idempotent steps

| Pattern | How it works | Use it for |
|---|---|---|
| **Partition overwrite** | Delete (or overwrite) the partition, then insert, in one transaction | Daily reports, aggregates, anything built per day |
| **Upsert by key** | Insert new keys, update existing ones (Chapter 45) | Raw tables copied from sources |
| **Write to a new location, then swap** | Build the result as a new table or file; replace the old one in a single step when complete | Large rebuilds, where a half-built table must never be visible |
| **Delivery log** | Record what was sent (with a content hash); skip exact repeats | Emails, messages, API calls, CRM updates |
| **Idempotency keys** | Send a unique key with each external request so the receiver ignores duplicates | Payments and external APIs that support it (Chapter 51) |

> **Watch out: side effects outside the database can't be rolled back.** A transaction can undo a table write. It can't un-send an email, un-post a message, or un-call an API. That's why `deliver_flash` checks a delivery log first, and why delivery should always be the *last* step, after every check has passed.

---

## 46.5 Partitions and backfills

A **backfill** runs a pipeline for past partitions: to build history for a new pipeline, to rebuild after fixing a bug, or to fill a gap after an outage.

Backfills bring one important rule: **rebuild history, don't re-deliver it.** Nobody wants five old Sales Flash emails arriving at once. So the backfill below leaves out delivery. It leaves out the ingestion steps too: they bring whole tables up to date, so running them once is enough, and running them again for every day would only re-read the ERP five times.

![A row of five daily partitions, 1 to 5 January 2026, each shown as a box with its Flash: 1 January 0 orders (holiday), 2 January 2 orders and ₹38,710, 3 and 4 January 0 orders (weekend), 5 January 0 orders because the ERP's 5 January business day hasn't happened yet. A bracket over all five is labeled backfill: rebuild the Flash and its check, no delivery. Only 2 January has an outbox envelope, delivered by its daily run. Below, a late correction on 6 January runs from the 2 January box to a new envelope marked correction_1, ₹40,110.](figures/fig46-3-partitions-backfill-corrections.svg)

*Figure 46.3 — Partitions, a backfill, and a late correction. The backfill fills in history quietly; only real changes to already-delivered numbers produce a new message.*

```python
BACKFILL = [daily_flash, flash_matches_erp]          # rebuild history, don't email it

for day in daily.get_partition_keys():
    r = dg.materialize(BACKFILL, partition_key=day, raise_on_error=False)
    print(day, "ok" if r.success else "FAILED")
RUN_LOG.clear()
for row in wh.execute("SELECT flash_date, orders_booked, revenue_booked FROM mart.daily_flash ORDER BY flash_date").fetchall():
    print(row)
print("files in outbox:", sorted(os.listdir("outbox")))
```

```
2026-01-01 ok
2026-01-02 ok
2026-01-03 ok
2026-01-04 ok
2026-01-05 ok
(datetime.date(2026, 1, 1), 0, Decimal('0.00'))
(datetime.date(2026, 1, 2), 2, Decimal('38710.00'))
(datetime.date(2026, 1, 3), 0, Decimal('0.00'))
(datetime.date(2026, 1, 4), 0, Decimal('0.00'))
(datetime.date(2026, 1, 5), 0, Decimal('0.00'))
files in outbox: ['flash_2026-01-02.txt']
```

**How it works.** `BACKFILL` is the Flash and its check, nothing else. The loop builds each day in turn and prints whether that day's run succeeded: a backfill is judged day by day, like any other run. `RUN_LOG.clear()` throws away the steps' messages, which the per-day lines summarize. In a deployed Dagster instance, you'd select a date range in the web interface, or run `dagster job backfill` from the command line, and Dagster would queue the runs and track each one.

**Reading it.** Every day's run succeeded, and the Flash now has a row for every day from 1 to 5 January. Three days have no bookings in the practice data: 1 January, a holiday, and the weekend of 3–4 January. 5 January also shows 0, because in the story it's still the morning of 3 January: the ERP's 5 January business day hasn't happened yet (it happens in section 46.7), and the check agreed with the ERP's 0. No new file appeared in the outbox: the only report is the one the 2 January daily run delivered.

### Backfill etiquette

- **Check that every step is idempotent first.** A backfill runs every step again for every day. A non-idempotent step turns a one-day bug into a month of doubled numbers.
- **Exclude side effects:** emails, CRM updates, messages, API writes. Run them only for the days that truly need re-sending, with a clear "correction" label.
- **Mind the source.** Thirty days of backfill can mean thirty full reads of the ERP. Run large backfills outside business hours, limit how many partitions run at once, and tell the source system's owner.
- **Keep days independent.** A per-day step that reads "the latest" data instead of "the partition's" data gives every backfilled day today's numbers.
- **Record why.** Note who ran the backfill, which dates, and why, next to the run.

### Late-arriving data

Data doesn't always arrive on the day it describes. On 6 January, the sales team discovers that order 10177, booked on 2 January, was for 7 industrial crates, not 6, and corrects it in the ERP. The 2 January Flash is now wrong.

First, find the order line to correct:

```python
print(ingest.fetch_rows("SELECT order_item_id, order_id, product_id, quantity, unit_price "
                        "FROM order_items WHERE order_id = %s", [10177]))
```

```
[(333, 10177, 105, 6, Decimal('1400.00'))]
```

Order 10177 has one line, `order_item_id` 333: 6 crates at ₹1,400. Correct it in the ERP, then re-run that one day:

```python
ingest.run_sql("UPDATE order_items SET quantity = %s WHERE order_item_id = %s", [7, 333])

result = dg.materialize(ALL, partition_key="2026-01-02", raise_on_error=False)
show_log()
print()
print(open("outbox/flash_2026-01-02_correction_1.txt").read())
```

```
raw_orders: 0 new, 0 changed, 0 deleted
raw_order_items: 0 new, 1 changed, 0 deleted
[2026-01-02] raw_dispatch: 5 rows (the day's rows replaced)
raw_crm_leads: 43 leads (attempt 1)
[2026-01-02] daily_flash: orders=2, revenue=Rs 40,110.00
[2026-01-02] check flash_matches_erp: PASSED (ERP: orders=2, revenue=Rs 40,110.00 | warehouse: orders=2, revenue=Rs 40,110.00)
[2026-01-02] deliver_flash: wrote outbox/flash_2026-01-02_correction_1.txt

CORRECTION to the Flash sent earlier for 2026-01-02: revenue changed from Rs 38,710.00 to Rs 40,110.00.

Riverstone Daily Sales Flash - 2026-01-02
Orders booked: 2
Net bookings (excl. cancelled, net of discounts): Rs 40,110.00
```

**Reading it.** The order-line load found one changed row. The Flash for 2 January was rebuilt at ₹40,110.00, ₹1,400.00 more than before: one more crate at ₹1,400. The check passed against the ERP. Delivery saw that the content differed from what was sent on 2 January, so it wrote a separate, clearly named correction, whose first line says what changed, instead of silently replacing the original.

**Deciding how far back to look.** A pipeline can't re-run every past day every morning. Common approaches: re-run a fixed **look-back window** each day (for example, the last 7 days), which catches most late changes automatically; re-run specific days when a change is detected (for example, with the hash comparison from Chapter 45 grouped by order date); or accept that some numbers are final after a closing date, as finance teams do with month-end.

---

## 46.6 Retries, timeouts, and alerting

### Retries: for problems that go away

Some failures are **transient**: a dropped connection, a busy API, a database restarting. Trying again a little later usually works. That's what the retry policy on `raw_crm_leads` is for. Simulate a dropped connection:

```python
CRM["fail_next"] = True
result = dg.materialize([raw_crm_leads], raise_on_error=False)
show_log()
print("run succeeded:", result.success)
```

```
raw_crm_leads: FAILED, connection dropped (attempt 1)
raw_crm_leads: 43 leads (attempt 2)
run succeeded: True
```

**Reading it.** The first attempt failed with a dropped connection. Dagster waited one second, retried, and the second attempt loaded all 43 leads. The run succeeded without anyone being woken up.

Retries have a cost, and a trap. The trap first: a retry policy retries **every** error, including ones that will never go away. Try a wrong token, which the CRM will refuse every time:

```python
CRM["token"] = "expired-token"
result = dg.materialize([raw_crm_leads], raise_on_error=False)
show_log()
print("run succeeded:", result.success)
```

```
raw_crm_leads: FAILED, 401 Client Error: Unauthorized for url: http://127.0.0.1:8045/api/leads?page=1&page_size=20 (attempt 1)
raw_crm_leads: FAILED, 401 Client Error: Unauthorized for url: http://127.0.0.1:8045/api/leads?page=1&page_size=20 (attempt 2)
raw_crm_leads: FAILED, 401 Client Error: Unauthorized for url: http://127.0.0.1:8045/api/leads?page=1&page_size=20 (attempt 3)
raw_crm_leads: FAILED, 401 Client Error: Unauthorized for url: http://127.0.0.1:8045/api/leads?page=1&page_size=20 (attempt 4)
run succeeded: False
```

**Reading it.** Four attempts, four identical 401s, three seconds of waiting, and the same failure at the end. Here that's only wasted time; against a real system, repeated wrong logins can lock the account.

Chapter 45's rule applies to whole steps too: **retry what might succeed next time, and fail fast on what won't.** Replace the asset with a version that tells Dagster not to retry a refusal:

```python
@dg.asset(retry_policy=dg.RetryPolicy(max_retries=3, delay=1))
def raw_crm_leads(context):
    attempt = context.retry_number + 1
    try:
        if CRM["fail_next"]:
            CRM["fail_next"] = False
            raise ConnectionError("connection dropped")
        leads = ingest.fetch_leads(token=CRM["token"])
    except requests.HTTPError as e:
        code = e.response.status_code
        log("raw_crm_leads", f"raw_crm_leads: FAILED, CRM refused the request ({code}) (attempt {attempt})")
        if code in (400, 401, 403, 404):
            raise dg.Failure(description=f"CRM refused the request ({code})", allow_retries=False)
        raise
    except Exception as e:
        log("raw_crm_leads", f"raw_crm_leads: FAILED, {e} (attempt {attempt})")
        raise
    n = ingest.load_leads(wh, leads)
    log("raw_crm_leads", f"raw_crm_leads: {n} leads (attempt {attempt})")

ALL = [raw_orders, raw_order_items, raw_dispatch, raw_crm_leads, daily_flash, flash_matches_erp, deliver_flash]
result = dg.materialize([raw_crm_leads], raise_on_error=False)
show_log()
print("run succeeded:", result.success)
```

```
raw_crm_leads: FAILED, CRM refused the request (401) (attempt 1)
run succeeded: False
```

**How it works, line by line.**

- The first `except` catches only `requests.HTTPError`, the error `raise_for_status()` raises when the API answers with an error code. `e.response.status_code` is that code.
- For 400, 401, 403, and 404, which mean "your request is wrong" rather than "try later", it raises **`dg.Failure`** with **`allow_retries=False`**: Dagster marks the step failed and **skips the retry policy**. Any other HTTP error (a 503, say) is re-raised with a bare `raise`, so it's retried.
- The second `except` handles everything else, such as the dropped connection, exactly as before.
- Defining `raw_crm_leads` again replaces the old version in the notebook, so the cell also rebuilds `ALL`, which still held the old one.

**Reading it.** One attempt, no retries, a clear message.

> **Try it.** What happens if you change `max_retries=3` to `max_retries=0` in the cell above, re-run it, and then run the dropped-connection cell again? Predict the output first, then run it, and put the setting back afterwards.

Put the right token back before going on:

```python
CRM["token"] = os.environ.get("CRM_API_TOKEN", "practice-token-45")
```

Three more things to know about retries:

- **Retries hide bugs.** While building this chapter's pipeline, `raw_crm_leads` first failed because it tried to create a table in a schema that didn't exist yet on a brand-new warehouse. The retry succeeded, because another step had created the schema in the meantime. The run looked healthy; the bug was real. Log every retry, and treat frequent retries as a problem to investigate.
- **Retries at two levels multiply.** `fetch_leads()` already retries a 429 inside each attempt, and Dagster retries the whole step up to three more times. A request that keeps failing can be tried many times over before anyone hears about it. Keep the total waiting time bounded, and know which level retries what.
- **Retries need idempotent steps.** A retry is a re-run. Section 46.4 is what makes retries safe.

### Timeouts: for problems that never end

A step that hangs (waiting forever on a network call, or a query that locks) is worse than one that fails, because nothing downstream runs and no alert fires. Set timeouts at every level: on network calls (Chapter 45), on database statements, and on whole runs, so a run that takes far longer than usual is stopped and reported. Dagster supports run-level timeouts through tags such as `dagster/max_runtime` in a deployed instance; check your version's documentation.

### A sensor that watches for the dispatch file

Section 46.2 described a **sensor**: a function the daemon calls every few minutes to see whether something has happened. Bhiwandi Main's dispatch file arrives when the warehouse team saves it, not at a fixed time. A sensor can start the dispatch load when the file appears:

```python
dispatch_job = dg.define_asset_job("dispatch_job", selection=[raw_dispatch])

@dg.sensor(job=dispatch_job, minimum_interval_seconds=300)
def dispatch_file_sensor(context):
    for name in sorted(os.listdir("exports")):
        if name.startswith("dispatch_"):
            yield dg.RunRequest(run_key=name, partition_key=name[9:19])

for request in dispatch_file_sensor(dg.build_sensor_context()):
    print(request.run_key, "->", request.partition_key)
```

```
dispatch_2026-01-02.csv -> 2026-01-02
dispatch_2026-01-05.csv -> 2026-01-05
```

**How it works, line by line.**

- `dispatch_job` is a job with just the dispatch load.
- `@dg.sensor(job=dispatch_job, minimum_interval_seconds=300)` turns the function into a sensor for that job, called at most every 300 seconds (five minutes).
- The function looks at every file in `exports`. For each dispatch file, it asks for a run with `yield dg.RunRequest(...)`. **`yield`** hands back one request and carries on with the loop, so one call can ask for several runs: the function is a generator (Chapter 29, section 29.9).
- `partition_key=name[9:19]` cuts the date out of the file name: characters 9 to 18 of `dispatch_2026-01-02.csv` are `2026-01-02`.
- **`run_key=name`** is the important part. Dagster remembers every run key it has seen and never starts a second run for the same key. The daemon calls the sensor every five minutes, and the file is there every time, but the load runs **once per file**. That's idempotency again, for triggers.
- `dg.build_sensor_context()` builds what the daemon would pass in, so the notebook can call the sensor once and print the runs it asks for, without starting them.

**Reading it.** The sensor found both practice files and asked for one run each, for the right days. In `riverstone_pipeline.py`, it's registered in `Definitions`, and under `dagster dev` the daemon calls it every five minutes. It's switched off at first, like the schedule.

### Alerting: telling someone what to do

An **alert** is a message sent to a person when something needs attention. A good alert is:

- **Actionable:** it says what failed, what the impact is, and what to do next.
- **Rare:** alerts that fire for things nobody needs to act on teach people to ignore alerts.
- **Routed:** it goes to the person or team that owns the fix, not to everyone.
- **Linked:** it points to the run, the logs, and a **runbook**, a short document that explains how to diagnose and fix a known problem.

Section 46.7 shows an alert from a real failed run. In a deployed Dagster instance, alerts are usually sent by a second kind of sensor, a **run failure sensor**, which the daemon calls whenever a run fails. This one is in `riverstone_pipeline.py`:

<!-- run: none -->
```python
def send_message(to, subject, body):
    """Stand-in for email, Slack, or Teams: write the message to the alerts folder."""
    with open(f"alerts/{subject[:40].replace(' ', '_').replace(':', '')}.txt", "w") as f:
        f.write(f"To: {to}\nSubject: {subject}\n\n{body}\n")

@dg.run_failure_sensor(monitored_jobs=[flash_job])
def flash_failure_alert(context: dg.RunFailureSensorContext):
    run = context.dagster_run
    send_message(to="data-oncall@riverstone.example",
                 subject=f"Daily Sales Flash failed: run {run.run_id[:8]}",
                 body=f"Failed job: {run.job_name}\nError: {context.failure_event.message}\n"
                      f"Runbook: docs/runbooks/daily_flash.md")
```

- `send_message()` is **your** function, not Dagster's: here a three-line stand-in that writes the message to the `alerts` folder. In production it would send an email (Chapter 20) or a chat message.
- `@dg.run_failure_sensor(monitored_jobs=[flash_job])` is Dagster's: it calls the function whenever a run of `flash_job` fails. `context.dagster_run` is the failed run, and `context.failure_event.message` is Dagster's description of the failure.
- It works only when it's registered in `Definitions` (`sensors=[...]`, as in the file) and the daemon is running, so it isn't run in the notebook.

Under `dagster dev`, with this sensor switched on and the practice API **not** started, a run of `daily_flash_job` for 2 January failed at `raw_crm_leads` (after its retries), and shortly afterwards the sensor wrote this file to `alerts/`. The run ID is different every time:

```text
To: data-oncall@riverstone.example
Subject: Daily Sales Flash failed: run da07a425

Failed job: daily_flash_job
Error: Execution of run for "daily_flash_job" failed. Steps failed: ['raw_crm_leads'].
Runbook: docs/runbooks/daily_flash.md
```

The same run still delivered the 2 January Flash, because the Flash doesn't depend on the CRM: the run failed, but only the part of it that needed the CRM.

---

## 46.7 Delivery only after the data passes its checks

This is the most important design rule in this chapter: **nothing leaves the pipeline until the data has passed its checks.** Reports, emails, dashboard refreshes that people act on, and syncs into the CRM all come *after* the checks, and depend on them.

![A left-to-right flow: ingest, then build the Flash, then the check flash_matches_erp. From the check, a path marked with a tick and the word passed leads to deliver_flash and the outbox. A path marked with a cross and the word failed leads to a stop sign labeled delivery blocked, and to an alert sent to the pipeline owner with the failed check, the numbers from both sides, the next step, and the runbook link. A note under the check says: the same query runs against the ERP and the warehouse.](figures/fig46-4-checks-gate-delivery.svg)

*Figure 46.4 — Checks gate delivery. When a check fails, the report isn't sent, and the owner gets an alert that says what to do.*

### A bad morning

It's the morning of 6 January. The ERP has had its business day of 5 January (`apply_day(2)`), and two things go wrong at once: a bug in the order-line load means it loads nothing, and Bhiwandi Main has changed the columns in its dispatch file (Chapter 45, section 45.8).

```python
apply_day(2)
ingest.BROKEN_ITEMS_SYNC = True          # simulate a faulty order-line load

result = dg.materialize(ALL, partition_key="2026-01-05", raise_on_error=False)
show_log()
print("run succeeded:", result.success)
print("files in outbox:", sorted(os.listdir("outbox")))
```

```
raw_orders: 1 new, 1 changed, 0 deleted
raw_order_items: 0 new, 0 changed, 0 deleted
[2026-01-05] raw_dispatch: FAILED, schema change in exports/dispatch_2026-01-05.csv: missing ['qty_units']
raw_crm_leads: 43 leads (attempt 1)
[2026-01-05] daily_flash: orders=0, revenue=Rs 0.00
[2026-01-05] check flash_matches_erp: FAILED (ERP: orders=1, revenue=Rs 18,750.00 | warehouse: orders=0, revenue=Rs 0.00)
run succeeded: False
files in outbox: ['flash_2026-01-02.txt', 'flash_2026-01-02_correction_1.txt']
```

**Reading it, step by step.**

- `raw_orders` loaded the new order 10178 and the change to order 10176, correctly.
- `raw_order_items` loaded **nothing**: the simulated bug. Nothing in its own output says it's wrong: "0 new" is a normal message on a quiet day.
- `raw_dispatch` **failed loudly** with a clear message: the expected `qty_units` column is missing. That's the column check from Chapter 45 doing its job.
- `raw_crm_leads` succeeded.
- `daily_flash` **ran**, because both of its dependencies succeeded, and built a row with 0 orders and ₹0.00, because the new order had no lines in the warehouse.
- The check **failed**: the ERP says 1 order for ₹18,750.00; the warehouse says 0.
- `deliver_flash` **didn't run**. The outbox still holds only the 2 January reports. No manager received a Flash saying Riverstone sold nothing on 5 January.

Notice two things. First, the dispatch failure didn't stop the Flash, because the Flash doesn't depend on dispatches: the dependency graph limited the damage. Second, the order-line bug didn't raise any error at all. Only the check, comparing the result against the ERP, caught it. **Checks catch the failures that don't crash.**

> **Watch out: a blocked delivery isn't a clean table.** The check stopped the email, but `mart.daily_flash` now holds a wrong row for 5 January, and anyone querying that table directly would see it. Chapter 47 covers the **write–audit–publish** pattern, which builds new data in a staging area, checks it, and only then makes it visible, so failed data never reaches readers at all.

### An alert someone can act on

```python
NEXT_STEP = {
    "daily_flash_flash_matches_erp": "compare raw.order_items with the ERP, fix the load, then re-run the day",
    "raw_dispatch": "confirm the column change with Bhiwandi Main, add the mapping, then re-run the day",
    "raw_crm_leads": "check the CRM token and the API's status page, then re-run raw_crm_leads",
}

def alert_on_failure(result, day):
    if result.success:
        return None
    failed_checks = [c.check_name for c in result.get_asset_check_evaluations() if not c.passed]
    failed_steps = sorted({e.step_key for e in result.all_events if e.event_type_value == "STEP_FAILURE"})
    lines = [f"Daily Sales Flash for {day} was NOT sent.",
             f"Failed checks: {failed_checks or 'none'}",
             f"Failed steps: {failed_steps}",
             "Next steps:"]
    for step in failed_steps:
        lines.append(f"  - {step}: {NEXT_STEP.get(step, 'read the run log')}")
    lines.append("Runbook: docs/runbooks/daily_flash.md")
    message = "\n".join(lines)
    with open(f"alerts/flash_{day}.txt", "w") as f:
        f.write(message)
    return message

print(alert_on_failure(result, "2026-01-05"))
```

```
Daily Sales Flash for 2026-01-05 was NOT sent.
Failed checks: ['flash_matches_erp']
Failed steps: ['daily_flash_flash_matches_erp', 'raw_dispatch']
Next steps:
  - daily_flash_flash_matches_erp: compare raw.order_items with the ERP, fix the load, then re-run the day
  - raw_dispatch: confirm the column change with Bhiwandi Main, add the mapping, then re-run the day
Runbook: docs/runbooks/daily_flash.md
```

**How it works, line by line.**

- `NEXT_STEP` maps each step that can fail to the first thing to do about it. Dagster names a check's step after its asset and its check, so the check's step is `daily_flash_flash_matches_erp`.
- `alert_on_failure()` returns `None` straight away if the run succeeded: no alert for a good run.
- `result.get_asset_check_evaluations()` lists the checks that ran; the code keeps the names of those that didn't pass.
- `result.all_events` is Dagster's event log for the run. Each failed step leaves a `STEP_FAILURE` event, whose `step_key` names the step. The set `{...}` removes repeats, and `sorted` puts them in order.
- For each failed step, the alert adds that step's next step from `NEXT_STEP`. `.get(step, 'read the run log')` gives a default for a step that isn't in the dictionary.
- `"\n".join(lines)` joins the lines into one message, which is written to the `alerts` folder and returned.

**Reading it.** The alert says what didn't happen (the Flash wasn't sent), what failed, and one next step for each failure, and where the runbook is. A different failure, such as a CRM 401, would get its own next step. In production, the same message would be sent by email or chat, as the run failure sensor in section 46.6 does.

### Fixing and re-running

The pipeline owner fixes the order-line bug, and confirms with Bhiwandi Main that the renamed column `units` means the same as `qty_units`. Both fixes are small; the re-run is one command:

```python
ingest.BROKEN_ITEMS_SYNC = False
ingest.CONFIRMED_RENAMES = {"units": "qty_units"}    # confirmed with Bhiwandi Main
result = dg.materialize(ALL, partition_key="2026-01-05", raise_on_error=False)
show_log()
print("run succeeded:", result.success)
api.shutdown()
```

```
raw_orders: 0 new, 0 changed, 0 deleted
raw_order_items: 1 new, 0 changed, 0 deleted
[2026-01-05] raw_dispatch: 2 rows (the day's rows replaced)
raw_crm_leads: 43 leads (attempt 1)
[2026-01-05] daily_flash: orders=1, revenue=Rs 18,750.00
[2026-01-05] check flash_matches_erp: PASSED (ERP: orders=1, revenue=Rs 18,750.00 | warehouse: orders=1, revenue=Rs 18,750.00)
[2026-01-05] deliver_flash: wrote outbox/flash_2026-01-05.txt
run succeeded: True
```

**Reading it.** The order-line load picked up the missing line for order 10178. The dispatch file loaded with the confirmed column mapping. The Flash was rebuilt at 1 order for ₹18,750.00, the check passed, the report was delivered, and the run as a whole succeeded. Because every step is idempotent, re-running the whole day was safe: `raw_orders` found nothing new to do. The last line, `api.shutdown()`, stops the practice CRM API, which the chapter no longer needs.

### What to check before delivery

| Check | Catches | Chapter |
|---|---|---|
| **Reconciliation** with the source (counts, totals) | Loads that silently miss or duplicate data | 45, this section |
| **Uniqueness** of keys (one row per day, per order) | Double-counting from non-idempotent steps | 46.4, 47 |
| **Freshness:** the newest data is from the expected day | Stale sources, stuck loads | 47 |
| **Volume:** row counts within a normal range | Empty loads that don't error | 47 |
| **Validity:** no negative quantities, known statuses only | Bad data from sources | 47 |
| **Schema:** expected columns present | Source changes | 45 |

---

## 46.8 The same pipeline in Airflow

**Apache Airflow** is the orchestrator most often named in data engineering job descriptions. It's task-based: you define a DAG of tasks, and each task runs a function or a command. Here's Riverstone's pipeline written for **Airflow 3**, the current major version (3.0 came out in April 2025), using its TaskFlow style.

<!-- run: none -->
```python
# dags/daily_flash.py  (Airflow 3, TaskFlow API)
import pendulum
from datetime import timedelta
from airflow.sdk import dag, task
from airflow.sdk.exceptions import AirflowFailException
from airflow.timetables.interval import CronDataIntervalTimetable

import ingest, flash                                   # the same companion functions

@dag(
    schedule=CronDataIntervalTimetable("30 6 * * *", timezone="Asia/Kolkata"),
    start_date=pendulum.datetime(2026, 1, 1, tz="Asia/Kolkata"),
    catchup=False,                                     # don't run every missed day automatically
    tags=["riverstone", "daily-flash"],
)
def daily_flash_pipeline():

    @task
    def raw_orders():
        return ingest.sync_table(flash.warehouse(), "orders")

    @task
    def raw_order_items():
        return ingest.sync_table(flash.warehouse(), "order_items")

    @task
    def raw_dispatch(ds=None):                         # ds = the run's logical date, "YYYY-MM-DD"
        return ingest.load_dispatch(flash.warehouse(), ds)

    @task(retries=3, retry_delay=timedelta(seconds=60))
    def raw_crm_leads():
        return ingest.load_leads(flash.warehouse(), ingest.fetch_leads())

    @task
    def build_flash(ds=None):
        flash.build_flash_safely(ds)                   # delete-then-insert in one transaction

    @task
    def check_flash(ds=None):
        if not flash.matches_erp(ds):
            raise AirflowFailException(f"Flash for {ds} does not match the ERP")  # fail, no retry

    @task
    def deliver_flash(ds=None):
        flash.deliver(ds)                              # skips if already delivered

    raw_dispatch()                                     # no arrow into the Flash, as in Figure 46.1
    raw_crm_leads()
    [raw_orders(), raw_order_items()] >> build_flash() >> check_flash() >> deliver_flash()

daily_flash_pipeline()
```

**How it works.**

- `from airflow.sdk import dag, task` brings in the two decorators. `@dag` turns the outer function into a DAG; `@task` turns each inner function into a task.
- `schedule=CronDataIntervalTimetable("30 6 * * *", timezone="Asia/Kolkata")` runs the DAG at 6:30 India time, and makes each run's **logical date** the day it reports on (the Watch-out below explains why that needs saying). `start_date` is the first day the DAG exists; `catchup=False` stops Airflow from running every missed day since then on its own.
- `ds` is the run's logical date as text, `"2026-01-02"`: Airflow's version of `context.partition_key`. A task receives it by having a parameter called `ds`.
- `@task(retries=3, retry_delay=timedelta(seconds=60))` gives **only** the CRM task a retry policy, as the project asks. `AirflowFailException` fails the check task at once, without using any retries.
- The last lines draw the graph. `>>` means "then": the two ERP loads, then the Flash, then the check, then delivery. `raw_dispatch()` and `raw_crm_leads()` are called without any arrow into the Flash, as in Figure 46.1, so their failures don't stop it.
- `flash` is a helper module you would write from this chapter's Dagster code: `warehouse()`, `build_flash_safely()`, `matches_erp()`, and `deliver()`.

**How it maps to the Dagster version.**

| Idea | Dagster (this chapter) | Airflow |
|---|---|---|
| Unit of work | Asset (a table or file that should exist) | Task (a function to run) |
| Dependencies | `deps=[...]` on the asset | `>>` between tasks |
| Which day | `context.partition_key` | `ds` (the logical date), or `data_interval_start` |
| Schedule | A schedule built from the job (section 46.3) | `schedule=` on the DAG |
| Time zone | On the partitions definition | On the timetable and `start_date` |
| Retries | `RetryPolicy` per asset | `retries` and `retry_delay` per task (or for every task, in `default_args`) |
| Checks that block delivery | `@asset_check(blocking=True)` | A check task upstream of delivery; `AirflowFailException` fails without retrying |
| Backfill | Select partitions; `dagster job backfill` | `airflow backfill create --dag-id daily_flash_pipeline --from-date 2026-01-01 --to-date 2026-01-05` |
| Run one day for testing | `materialize(..., partition_key=...)` | `airflow dags test daily_flash_pipeline 2026-01-02` |

> **Watch out: which day is the logical date?** In Airflow 2, a daily DAG's logical date was the **start of the interval** it processes: the run on the morning of 3 January had a `ds` of 2 January. Airflow 3 changed the default for a plain cron string: the logical date is now **the moment the run starts**, so that same run has a `ds` of 3 January, and a Flash built from `ds` would report a day that has barely begun. `CronDataIntervalTimetable` asks for the Airflow 2 behavior, which is what a report about yesterday needs. Dagster's partitioned schedule behaves the same way (section 46.3); Airflow just names it differently. Whichever you use, test with `airflow dags test` and print `ds` before trusting it.

> **Simplification note.** This Airflow code isn't executed in the book: Airflow needs its own installation, a metadata database, and a scheduler process, and it imports the helper module `flash` described above. It was checked against Airflow 3.3.2 with such a helper: `airflow dags test daily_flash_pipeline 2026-01-02` ran every task and delivered the 2 January Flash, 2 orders for ₹38,710.00. To try it yourself, install Airflow in a **separate** virtual environment, because it pins many libraries to exact versions: `python -m pip install "apache-airflow==3.3.2" --constraint https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.14.txt` (the last part names your Python version), then `airflow standalone` starts everything on your computer. Airflow doesn't run directly on Windows; use WSL (Chapter 34, section 34.1) or a container (Chapter 52). In Airflow 2, which you will still meet at many companies, the decorators are imported from `airflow.decorators` and a backfill is `airflow dags backfill -s 2026-01-01 -e 2026-01-05 daily_flash_pipeline`.

> **Interview extra point.** If an interviewer asks about Airflow and you've used Dagster (or the reverse), map the ideas: DAG and dependencies, logical date or partition, retries, backfills with side effects excluded, checks before delivery, and idempotent tasks. Interviewers care far more about whether you'd design the pipeline safely than about which decorator you'd type. Chapter 77 includes pipeline design questions.

---

## 46.9 Choosing an orchestrator

| Option | Model | Strengths | Watch for | A good fit when |
|---|---|---|---|---|
| **Cron / Task Scheduler** | Time-based commands | Simple, everywhere, nothing to run | No dependencies, retries, history, or backfills; failures are silent unless you add alerts | One or two independent scripts with an owner who checks them |
| **Apache Airflow** | Task DAGs | Very widely used; huge library of operators; managed versions on every major cloud | Heavier to run; the logical-date model; asset lineage is less central | Teams with many varied workflows, or where the platform already runs it |
| **Dagster** | Asset graphs | Assets, partitions, and checks built in; quick local testing; clear lineage | Smaller community than Airflow; concepts to learn | Data platforms built around tables and models, including dbt projects |
| **Prefect** | Python flows | Pythonic and lightweight; good for dynamic workflows | Fewer data-asset features built in | Python-heavy teams wanting minimal ceremony |
| **Cloud schedulers and workflow services** | Varies | Managed, integrated with one cloud | Tied to one provider; features vary | Small pipelines already on one cloud (Chapter 52) |
| **Built-in schedulers in tools** (dbt Cloud, warehouse tasks, BI refresh schedules) | Per tool | Nothing extra to run | Each tool schedules only itself; cross-tool dependencies get lost | A single tool's work, not a cross-system pipeline |

A few questions settle most choices:

1. **How many steps depend on each other, across how many systems?** Few and independent: a scheduler may be enough. Many and connected: an orchestrator.
2. **What does the team already run and know?** A well-run Airflow beats a half-adopted new tool.
3. **Is the work about data assets (tables, models) or about actions (jobs, scripts)?** Assets lean toward Dagster; varied actions lean toward Airflow or Prefect.
4. **Who will operate it?** Self-hosting any orchestrator means upgrades, a metadata database, and monitoring. Managed services cost money and save that effort.

> **Real-life example: the report that outgrew cron.** Many teams start exactly like Riverstone: a handful of cron jobs at 6:00, 6:15, and 6:30, spaced to "leave enough time". It works until month-end volumes make the 6:00 job run long, and the 6:30 report quietly uses half-loaded data. Moving to an orchestrator usually starts with that one incident, and the first win is replacing time gaps with real dependencies.

---

## 46.10 Operating pipelines

A pipeline that runs is not the same as a pipeline that's operated well. A few habits make the difference.

- **Every pipeline has an owner.** A named person or team who gets the alerts and decides what happens when it fails.
- **Every important output has a deadline.** A **service-level agreement** (SLA) or objective states when data must be ready, such as "Daily Sales Flash delivered by 7:30 a.m. IST on working days". Alert when the deadline is at risk, not only when a step fails.
- **Every known failure has a runbook.** What the alert means, how to check the cause, how to fix it, how to re-run safely, and whom to tell. The alert in section 46.7 links to one.
- **Every re-run and backfill is recorded.** Who ran what, for which dates, and why.
- **Changes are tested before they're deployed.** Run the pipeline for a known partition in a test environment and compare outputs with the previous version (Chapter 29's testing habits, applied to data).
- **Pipelines are code.** Definitions live in Git, go through review, and are deployed the same way every time (Chapter 52).
- **Downstream readers know the status.** When the Flash is late, tell the sales team before 7:30, rather than letting them discover it.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Spacing cron jobs by time instead of dependencies | Reports built on half-loaded data on busy days | Declare dependencies in an orchestrator (46.1) |
| Leaving schedules in the server's time zone | Runs at the wrong local time; "yesterday" is wrong for hours each night | Set `Asia/Kolkata` (or your zone) explicitly (46.2) |
| Steps that read the clock instead of the partition | Backfilled days get today's numbers | Pass the partition date into every step |
| Appending results in a step that can be retried | Doubled rows and revenue after a failure (46.4) | Partition overwrite in a transaction, or upserts |
| Assuming idempotency without testing it | Surprise duplicates at the first real failure | Crash a step on purpose and re-run (46.4) |
| Sending emails or syncs before checks | Wrong numbers reach managers or the CRM | Delivery last, blocked by checks (46.7) |
| Re-delivering history during backfills | Dozens of old reports arrive at once | Exclude side effects from backfills (46.5) |
| Silently overwriting delivered numbers after a correction | People act on the old figure without knowing it changed | Send a labeled correction; keep a delivery log (46.5) |
| Retrying every failure | Bugs hidden by lucky retries; wrong passwords retried until accounts lock | Retry transient errors only; log and review retries (46.6) |
| No timeouts | A stuck run blocks everything and no alert fires | Timeouts on calls, statements, and runs |
| Alerts without context | People ignore alerts or can't act on them | What failed, impact, next step, runbook link (46.7) |
| Trusting "0 rows loaded" | Empty loads pass unnoticed | Reconciliation and volume checks (46.7, Ch 47) |
| Making everything depend on everything | One broken file stops every report | Declare only real dependencies (Figure 46.1) |
| Pipelines without owners or deadlines | Failures noticed by the business, days later | Owner, SLA, runbook (46.10) |

---

## In the real world: the Flash that went out twice

Two months after the pipeline went live, Anita forwarded Meera an email at 7:10 a.m. with one line: "Which one is right?"

Below it were two copies of the Daily Sales Flash for the previous day, sent eleven minutes apart. The first said ₹3,12,400 in bookings. The second said ₹3,24,900.

Meera opened the run history. The 6:30 run had failed at 6:41 when the warehouse connection dropped, and the orchestrator had retried it automatically. Both runs had reached delivery. The difference was easy to explain once she saw it: between the first and second runs, a sales executive had entered a late order from the previous afternoon, so the second run's numbers were more complete. But the email step had no memory. It sent whatever it was asked to send, every time it ran.

"So the second one is right," Anita said when Meera called her. "But the managers don't know that. Two of them have already replied to the first one."

Meera and the data engineer made three changes that week.

First, **delivery got a memory.** Every sent report was recorded with a hash of its content. An identical report wouldn't be sent twice. A report whose numbers changed would be sent with the subject line "CORRECTION: Daily Sales Flash", and a first line saying what changed and why.

Second, **delivery moved behind a cut-off check.** The Flash now waited until the ERP's end-of-day close flag was set before building, so late entries from the previous afternoon were included in the first send, not discovered by a retry.

Third, **retries became visible.** Any run that needed a retry now posted a one-line note in the data team's channel, so a flaky warehouse connection would be noticed and fixed, not silently absorbed.

The next month, the warehouse connection dropped again during a run. The retry succeeded, the content hash matched what had already been prepared, and nothing was sent twice. The only sign was a single line in the data team's channel, which led the engineer to a network setting that had been causing the drops all along.

**What made this work.**

- **Meera read the run history before guessing.** The orchestrator's record of both runs explained the duplicate in minutes.
- **They fixed the design, not only the incident:** idempotent delivery, a clear correction path, and a real readiness condition instead of a clock time.
- **They made retries visible,** so the underlying problem got fixed instead of hidden.

---

## Project: orchestrate Riverstone's ingestion

**Goal:** turn your Chapter 45 ingestion job into an orchestrated, partitioned, tested pipeline that delivers the Daily Sales Flash only when the data is right. Chapter 47 will add a fuller set of quality checks and monitoring on top.

### Tools you'll need

- **Dagster**, installed in section 46.3 with `python -m pip install dagster==1.13.23 dagster-webserver==1.13.23`. `dagster` is the library; `dagster-webserver` is the local web page that `dagster dev -f riverstone_pipeline.py` opens. `dagster dev` also starts the daemon that runs schedules and sensors.
- **Python** in the book's virtual environment (Chapter 17), with **DuckDB**, **psycopg2**, and **requests**, and **PostgreSQL 16**, as in Chapter 45.
- **The Chapter 46 companion folder** (`companion/ch46/`), copied to `work/ch46`: `reset_ch46.py`, `ingest.py`, `riverstone_pipeline.py`, and the three helpers copied from Chapter 45. Run the notebook from that folder. If your PostgreSQL needs a user or password, copy your `.env` file from `work/ch45` (Chapter 45, section 45.2).
- **Versions used for the outputs shown:** Python 3.14.7, Dagster 1.13.23, DuckDB 1.5.6, psycopg2 2.9.13, requests 2.33.1, PostgreSQL 16.
- **Apache Airflow** (not needed for this chapter): section 46.8's Simplification note gives the install command, in a separate virtual environment; managed versions exist on the major clouds.

**Option A: Riverstone.** Use the companion environment and your Chapter 45 project.

**Option B: your own pipeline.** Use a report you currently produce on a schedule, with data you have permission to use. Keep credentials out of code.

**Steps**

1. **Draw the graph first.** List every asset (raw tables, staging tables, the Flash, delivery) and its real dependencies. Mark which failures should stop which outputs.
2. **Define daily partitions** in `Asia/Kolkata` (or your time zone). Make every step that works on one day (the dispatch file, the Flash, delivery) use the partition date, never the clock; leave the loads that bring whole tables up to date unpartitioned.
3. **Wrap your Chapter 45 loads as assets.** Add `customers` and `products` as full loads.
4. **Build the Flash** with partition overwrite in a transaction. Add a second measure of your choice, such as orders by segment.
5. **Add at least two blocking checks:** reconciliation with the ERP, and exactly one row per day.
6. **Add delivery** with a delivery log and a correction path.
7. **Add a retry policy** to the API step only, and log every retry.
8. **Write the failure test:** crash the Flash step after writing, re-run, and assert that there's one row and the revenue matches the ERP. Then do the same with an append version and record what goes wrong.
9. **Run a backfill** for 1–5 January without delivery, and show the outbox is unchanged.
10. **Simulate a bad morning:** break one load, confirm the check blocks delivery, and produce an alert with a next step and a runbook link. Write the runbook (half a page).
11. **Schedule it** for 6:30 IST. Put your definitions in one file, as `riverstone_pipeline.py` does (section 46.3), run it with `dagster dev`, switch the schedule on, and take a screenshot of the graph and a successful run.

**Stretch goals**

- Translate your pipeline to Airflow and run it with `airflow dags test` for 2 January.
- Add a 7-day look-back: each daily run also rebuilds the previous six days, and only sends corrections when numbers change.
- Add a deadline: if the Flash hasn't been delivered by 7:30 IST, write an alert even if nothing has failed.

---

## Recap

- An **orchestrator** runs pipeline steps in dependency order, on schedule, with retries, history, backfills, and alerts. **Cron** is enough for simple, independent jobs.
- A pipeline is a **DAG**. **Task-based** tools (Airflow) describe what to run; **asset-based** tools (Dagster) describe what data should exist.
- **Schedules** use **cron expressions** and need explicit **time zones**. **Partitions** split runs by day, so each run knows exactly what it's building.
- **Idempotency** must be proven with a **failure test**. An append step retried after a crash doubled revenue to ₹77,420.00; **partition overwrite in a transaction** kept it at ₹38,710.00.
- **Side effects** (emails, syncs) can't be rolled back: put them last, behind checks, with a **delivery log**.
- **Backfills** rebuild history; exclude delivery. **Late corrections** re-run one partition and send a labeled correction.
- **Retries** handle transient failures, and can hide bugs; log them, and **fail fast** on errors that won't go away (`allow_retries=False`). **Timeouts** stop runs that never end.
- **Sensors** start runs when something happens, such as a file arriving; a **run key** makes sure each event triggers one run. The **daemon** runs schedules and sensors.
- **Checks that block delivery** catch failures that don't crash: an order-line load that loaded nothing raised no error, and only the reconciliation check stopped a ₹0 Flash reaching managers.
- Good **alerts** are actionable, rare, routed, and linked to a **runbook**.
- Airflow expresses the same design with tasks, `ds`, retries, and a check task before delivery.
- Operate pipelines with **owners**, **SLAs**, **runbooks**, recorded re-runs, and code review.

---

## Key terms

orchestrator · pipeline · cron · directed acyclic graph (DAG) · cycle · task · asset · materialize · dependency · schedule · cron expression · time zone (UTC, IST) · partition · partition key · sensor · daemon · run key · job · executor · retry policy · fail fast · asset check · blocking check · idempotent · failure test · transaction (BEGIN, COMMIT, ROLLBACK) · partition overwrite · delivery log · idempotency key · side effect · backfill · late-arriving data · look-back window · transient failure · timeout · alert · runbook · run failure sensor · logical date (Airflow `ds`) · catchup · service-level agreement (SLA) · write–audit–publish

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can explain what an orchestrator adds to cron, with at least four examples.
- [ ] You can draw a pipeline as a DAG and explain why only real dependencies belong in it.
- [ ] You can explain the difference between task-based and asset-based orchestration.
- [ ] You can read and write cron expressions, and set time zones explicitly.
- [ ] You can build partitioned assets in Dagster that use the partition date instead of the clock.
- [ ] You can prove a step is idempotent with a deliberate failure test, and explain why the append version doubled revenue.
- [ ] You can list idempotency patterns for tables and for side effects such as emails.
- [ ] You can run a backfill that rebuilds history without re-delivering it.
- [ ] You can handle a late correction by re-running one partition and sending a labeled correction.
- [ ] You can explain when retries help, when they hide bugs, how to fail fast, and why timeouts matter.
- [ ] You can write a sensor that starts one run per new file, and explain what the daemon does.
- [ ] You can make checks block delivery, and explain why the failed order-line load raised no error.
- [ ] You can write an actionable alert with a next step and a runbook link.
- [ ] You can map the pipeline between Dagster and Airflow, including Airflow's logical date.
- [ ] You can recommend an orchestrator for a given team and explain why.

---

## Exercises

Run `reset()` and re-run the definitions blocks before each exercise that uses the companion environment, unless it says otherwise.

### Warm-up

1. Write cron expressions for: (a) 7:15 every weekday (Monday to Friday); (b) every 30 minutes; (c) 9:00 on the first day of every quarter (January, April, July, October).
2. A schedule is set to `0 1 * * *` in UTC. At what time does it run in Mumbai (IST)? Which calendar date is it in IST when it runs?
3. For each step, say whether it's idempotent as described, and why: (a) `INSERT INTO mart.daily_flash ...` for the partition day; (b) `INSERT OR REPLACE` by primary key; (c) sending an email every time the step runs; (d) delete the partition's rows, then insert, in one transaction.

### Core

4. In section 46.4, the naive table ended with two rows for 2 January. If the naive step had been retried three times after three crashes, and then succeeded, how many rows would there be, and what revenue would a `SUM` report?
5. Add a second blocking check to the pipeline, `one_flash_row_per_day`, that passes only when `mart.daily_flash` has exactly one row for the partition. Why is this check useful even though `flash_matches_erp` already compares the row with the ERP?
6. In section 46.7's bad morning, why did `daily_flash` run at all, and why did `raw_dispatch`'s failure not stop it? Draw (or describe) the dependency change that would make a dispatch failure block the Flash, and argue whether that would be a good idea.
7. After the correction in section 46.5, what would `deliver_flash` do if the ERP were corrected *back* to 6 crates and the 2 January partition re-run? Trace it through the delivery log.
8. Rewrite the alert in section 46.7 for a different failure: the CRM API returned 401 Unauthorized. Include what failed, the impact on the Flash, the next step, and a runbook link.
9. A colleague proposes adding `retry_policy=dg.RetryPolicy(max_retries=5)` to `daily_flash` "to make the pipeline more reliable". Explain what this would and wouldn't help with, using the section 46.7 bad morning as an example.

### Stretch

10. Design a 7-day look-back for the Flash: each morning's run rebuilds today's partition and the previous six, but only delivers today's Flash and any *corrections* to earlier days. Describe the assets and selections, and what the delivery log must store.
11. Riverstone's month-end finance pack must use numbers that don't change after the 5th of the following month. Describe how you'd combine partitions, a closing rule, and checks so late corrections after the 5th are reported for review rather than silently changing the pack.
12. Translate the section 46.7 check-then-deliver behavior into Airflow terms precisely: which task fails, which exception, which retries apply, and what state the delivery task ends in.

### Think about it (no code needed)

13. Riverstone's data team has six cron jobs today and one part-time engineer. Make the case for staying with cron for another six months, then the case for moving to an orchestrator now. Which would you choose, and what single incident would change your mind?
14. Why is "delivery last, behind checks" a rule for more than emails? Give two examples from Chapter 51's world (writing data back into business systems) where breaking it would be worse than a wrong email.

---

## Answers

**1.** (a) `15 7 * * 1-5`. (b) `*/30 * * * *`. (c) `0 9 1 1,4,7,10 *`. The common slip in (a) is `* 7 * * 1-5`, which runs every minute from 7:00 to 7:59.

**2.** 1:00 UTC is **6:30 a.m. IST** (UTC + 5:30), on the **same calendar date**. The reverse trap is a schedule at 20:00 UTC, which runs at 1:30 a.m. IST on the *next* day.

**3.** (a) **Not idempotent:** each run inserts another row for the day, as section 46.4 showed. (b) **Idempotent:** the same keys end with the same values however often it runs. (c) **Not idempotent:** each run sends another email; the delivery log in section 46.3 is what makes it safe. (d) **Idempotent:** every run leaves exactly the rows for that partition, and a failure rolls back.

**4.** Each of the three crashed runs inserted a row before crashing, and the successful run inserted one more: **4 rows**. A `SUM` would report 4 × ₹38,710.00 = **₹1,54,840.00**.

**5.** A sample check:

<!-- run: none -->

```python
@dg.asset_check(asset=daily_flash, blocking=True)
def one_flash_row_per_day(context):
    day = context.partition_key
    n = wh.execute("SELECT COUNT(*) FROM mart.daily_flash WHERE flash_date = ?", [day]).fetchone()[0]
    return dg.AssetCheckResult(passed=(n == 1), metadata={"rows": n})
```

Like `flash_matches_erp`, it runs one `COUNT(*)` for the partition's day and returns an `AssetCheckResult`; `metadata={"rows": n}` attaches the count, which Dagster shows beside the result. It's useful because it names the problem precisely. `flash_matches_erp` also fails when there are duplicate rows, but its message only says the numbers don't match; the uniqueness check says *why*, which points straight to a non-idempotent step. Separate checks for separate failure modes make alerts actionable. It also protects readers who query the table directly and sum it.

**6.** `daily_flash` depends only on `raw_orders` and `raw_order_items`, and both **succeeded** (the order-line load loaded nothing, but didn't raise an error). `raw_dispatch` isn't a dependency of the Flash, so its failure only affects assets downstream of it. To make a dispatch failure block the Flash, you'd add `raw_dispatch` to `daily_flash`'s `deps`. That would usually be a **bad idea**: the Flash reports bookings, which don't use dispatch data, so a warehouse spreadsheet problem would stop the sales team's numbers for no reason. Add a dependency only when the output really uses the input; a dispatch report, by contrast, *should* depend on `raw_dispatch`.

**7.** The Flash would be rebuilt at ₹38,710.00. `deliver_flash` computes the content hash and finds that **exactly this content was already delivered** (the original 2 January report, recorded on the first run), so it logs "already delivered, skipped" and sends nothing. The managers' latest message is still the correction for ₹40,110.00, which is now wrong. That's a gap in this simple design: "already delivered" should compare with the *most recent* delivery, not any past delivery. A fix is to compare the new hash with the latest entry for that day, and send a second correction when they differ.

**8.** A sample alert: *"Daily Sales Flash for 2026-01-05: CRM leads were NOT loaded. The CRM API returned 401 Unauthorized (the token is missing, wrong, or expired), so the step failed at once, without retrying. Impact: the Flash itself is unaffected and has been delivered; lead figures in the weekly pipeline report will be stale until this is fixed. Next step: check whether the CRM API token was rotated, update the secret `CRM_API_TOKEN`, then re-run `raw_crm_leads` only. Runbook: docs/runbooks/crm_ingestion.md."* A good answer says the Flash wasn't affected, because `raw_crm_leads` isn't one of its dependencies, and notes that a 401 shouldn't be retried at all, which is why the step fails fast (section 46.6).

**9.** Retries on `daily_flash` would help only if the step itself failed **transiently**, for example a dropped warehouse connection during the build, and only because the step is idempotent. They wouldn't help on the bad morning at all: `daily_flash` **didn't fail**. It succeeded with wrong numbers, because its input was incomplete. The problem was caught by the check, and retrying a check that compares wrong data with the ERP gives the same failure every time. Five retries would also delay the alert. Reliability comes from checks, idempotency, and fixing root causes; retries only cover transient faults.

**10.** One design: keep the daily partitions. The morning run materializes ingestion once (it isn't per-day), then `daily_flash` and its checks for **seven partition keys**: today and the previous six. Delivery runs for **today's** partition as normal, plus a `deliver_corrections` step that, for each of the six earlier days, compares the new content hash with the **latest** delivery for that day and sends a labeled correction only when it differs. The delivery log must store the day, the content hash, the time sent, and the type (original or correction), so "latest" can be found. Checks must pass for every rebuilt day before any correction is sent.

**11.** One approach: keep daily (or monthly) partitions and a **closing table** that records when each month was closed (the 5th of the following month). The pipeline still re-runs late partitions when source data changes, but a **blocking check** on the month-end pack compares the new numbers with the closed version: if the month is closed and numbers changed, the check fails *for the pack*, the pack isn't regenerated, and an alert goes to finance with the difference and the orders involved. Finance then decides whether to reopen the month or book an adjustment in the next one. The daily Flash can still show corrected operational numbers; the closed pack stays as reported.

**12.** In Airflow, the check is a task (`check_flash`) upstream of `deliver_flash`. When the numbers don't match, it raises **`AirflowFailException`**, which marks the task **failed immediately, without using its retries**. (A normal exception would be retried according to `retries`, which is wasteful for a data mismatch.) Because `deliver_flash` depends on `check_flash` with Airflow's default trigger rule (`all_success`), it ends in the **`upstream_failed`** state and never runs. The DAG run is marked failed, and a failure callback or alerting integration notifies the owner.

**13.** *Stay with cron:* six jobs and one part-time engineer means an orchestrator adds a system to install, upgrade, and learn; if the jobs are independent and each has alerts and a runbook, the risk is low, and the engineer's time may be better spent on checks. *Move now:* the Flash already depends on several loads, cron spacing will fail on a busy day, and adding checks, retries, and backfills by hand in six scripts costs more than adopting a tool once; a managed or simple local deployment keeps the operational burden small. A reasonable choice is to move the Flash's steps to an orchestrator now and leave truly independent jobs on cron. The incident that would change a "stay" decision: any day when a report goes out built on half-loaded or stale data because a job ran long.

**14.** Because anything that leaves the pipeline changes something outside it, and many of those changes can't be undone. Examples: (1) syncing **credit limits** from the warehouse into the ERP: a failed load that sets limits to zero would block real customers' orders until someone notices; (2) pushing **lead scores** or "customer at risk" flags into the CRM: wrong scores would send sales reps to the wrong customers and trigger automated emails, and the CRM keeps the history. Other good examples include reorder flags that trigger purchase orders, and marketing lists that send messages. In each case, a check that blocks the sync costs minutes; a wrong sync can cost orders, money, or customer trust.

---

## Where this leads

- **Chapter 47, Data Quality, Observability & Contracts,** turns this chapter's checks into a full testing and monitoring layer: freshness, volume, and validity checks, write–audit–publish, data contracts, and alert fatigue.
- **Chapter 48, Big Data & Distributed Compute,** runs heavier steps on Spark and DuckDB at scale, inside pipelines like this one.
- **Chapter 49, Storage, Warehouses & Lakehouses,** explains the transactions (ACID) and table formats that make partition overwrites safe at scale.
- **Chapter 50, Streaming & Real-Time,** covers pipelines that run continuously instead of once a day.
- **Chapter 51, Data Activation,** adds CRM and ERP syncs as downstream steps, gated by checks and made idempotent with delivery logs and idempotency keys.
- **Chapter 52, The Cloud, Containers & Infrastructure as Code,** deploys pipelines like this one: containers, secrets, and environments.
- **Chapter 63, Automation Architecture & Governance,** looks at orchestration across a whole company: ownership, governance, and choosing tools.
- **Part 8:** pipeline and orchestration questions appear in the data engineering and system design interview chapters (Chapter 77).
