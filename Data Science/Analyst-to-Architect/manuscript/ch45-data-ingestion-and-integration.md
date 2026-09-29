# Chapter 45. Data Ingestion & Integration

*Part 5 — Data Engineering, Integration & Scale*

> **Chapter at a glance**
>
> **You will learn to:** name the kinds of source systems a data platform ingests from, and what makes each one hard · choose between full loads, incremental loads, and change data capture, and explain what each one can miss · show, with a real test, why a "new rows only" load silently loses updates · compute and use SHA-256 and MD5 fingerprints · detect inserted, changed, and deleted rows with hashes, and skip files that haven't changed · read real change events from PostgreSQL's log · load messy CSV files without silent type errors, and reconcile what you loaded against the file · recognize schema changes before they break a load · pull data from a paginated, authenticated, rate-limited API with retries · decide when to build a connector and when to buy one · judge the legal and ethical limits of collecting web data.
>
> **Before you start:** Chapter 2 (formats; the idea of a file fingerprint; what an API is). Chapter 12 (transactions, upsert, loading a CSV). Chapters 13 and 28 (SQL). Chapter 17 (the virtual environment and Jupyter). Chapter 18 (calling an API, `.env` files). Chapter 20 (idempotency with a run key). Chapter 26 section 26.0 (the terminal). Chapter 29 (Python as software; the CRM client). Chapter 32 (dbt) helps but isn't required.
>
> **Time needed:** 15–20 hours of reading and practice, spread over two to three weeks. Plan four sittings: sections 45.1–45.4; sections 45.5–45.6 (hashes, upserts, change data capture); sections 45.7–45.8 (files and schema changes); sections 45.9–45.11 and the project.
>
> **Tools:** PostgreSQL 16, and Python in the book's virtual environment (Chapter 17) with `requests` and `python-dotenv` (Chapter 18), plus two libraries you install in section 45.2: `psycopg2` and `duckdb`. The Chapter 45 companion folder. Everything runs on your own computer.
>
> **Practice data:** `riverstone_source`, a private copy of the Riverstone one-year database that plays the part of the ERP and the CRM; two dispatch files from the Bhiwandi Main warehouse; and a small local API that stands in for the CRM. Every output shown is from a real run.
---

## Why this matters

Every report, dashboard, model, and automation you've built so far started with data that was already sitting in a table. Somebody put it there. In most companies, that somebody is a data engineer, and the first job is **ingestion**: getting data out of the systems where the business runs and into a place built for analysis, correctly, every day, without anyone copying files by hand.

Ingestion looks simple and isn't. The ERP doesn't tell you which orders changed yesterday. The warehouse's dispatch file arrives with dates in a different format and quantities written as text. The CRM's API only returns 20 records at a time, and refuses your requests if you ask too quickly. A source system adds a column on a Tuesday and your load breaks on Wednesday, or worse, keeps running with the wrong numbers.

The failures that hurt most in ingestion aren't crashes. They're loads that succeed and quietly deliver the wrong data. This chapter shows three of them happening on Riverstone data, and how to catch each one. Get this layer right and everything built on top of it can be trusted. Get it wrong and every chart in the company is wrong in ways nobody notices.

---

## In plain English

Think about how a large kitchen gets its ingredients.

- Ingredients arrive from many **suppliers**: a vegetable vendor, a dairy, a spice wholesaler. Each delivers differently: some bring crates, some send a list and a truck, some you must collect. Those are **source systems**, each with its own way of handing over data.
- On the first day, the kitchen takes **everything** each supplier has. That's a **full load**.
- After that, it only wants what's **new or different** since yesterday. That's an **incremental load**. But if a supplier quietly swaps yesterday's milk for a different brand and keeps the same crate number, a kitchen that only counts new crates will never notice. That's the update a naive incremental load misses.
- A careful kitchen compares a **fingerprint** of each item against yesterday's: same weight, same label, same batch code. Any difference is a change. That's **change detection with hashes**.
- The best suppliers send a **delivery log** listing every change as it happens: "added two crates, replaced one". That's **change data capture**.
- At the receiving door, someone checks each delivery against the delivery note, sets aside anything damaged, and writes down what arrived. That's **reconciliation** and a **load log**.
- One supplier changes its packaging without warning. If the receiving clerk only checks crate counts, the new packaging sails through. That's a **schema change**.

Ingestion is the receiving door of the data platform. This chapter is about running it well.

---

## 45.1 Where company data comes from

Before you design any load, know what kind of source you're dealing with. Each kind fails in its own way.

![A diagram with five source types on the left feeding an ingestion layer in the middle, which writes to a warehouse on the right with raw, staging and modeled layers. Sources: databases such as the ERP, files such as the warehouse dispatch sheet, APIs such as the CRM, events such as website clicks and sensor readings, and SaaS tools such as email marketing and support desks. Under each source, one typical difficulty: databases don't say what changed; files arrive late, twice, or malformed; APIs page, throttle and expire tokens; events arrive out of order or twice; SaaS tools change their schemas and limits. A load log and reconciliation checks sit under the ingestion layer.](figures/fig45-1-sources-to-warehouse.svg)

*Figure 45.1 — The main kinds of source, and the difficulty each brings. Ingestion writes to a raw layer first, so the original data is kept even when later steps change.*

| Source type | Riverstone example | How you usually read it | What makes it hard |
|---|---|---|---|
| **Operational databases** | The ERP's orders, order lines, customers | SQL queries, or the database's change log | They're built to run the business, not to tell you what changed; heavy queries can slow the business down |
| **Files** | Bhiwandi Main's daily dispatch sheet; bank statements | Reading CSV, Excel, JSON, or Parquet files from a folder, SFTP server, or cloud storage | Late, duplicated, renamed, or malformed files; formats chosen by a person, not a system |
| **APIs** | The CRM's leads | HTTP requests with authentication (Chapter 2) | Pagination, rate limits, expiring tokens, changing versions |
| **Events** | Website enquiries; plant sensor readings (Chapter 50) | Streams and message queues | Huge volumes; events arrive late, out of order, or twice |
| **SaaS tools** | Email marketing, the support desk | Their APIs, usually through a connector | Limits and schemas you don't control, and change without notice |

Two terms appear throughout this part of the book.

- A **source system** is any system where data is first recorded: the ERP, the CRM, a spreadsheet the warehouse maintains.
- A **system of record** is the source that's officially correct for a piece of data. Riverstone's ERP is the system of record for orders; the CRM is the system of record for leads. When two systems disagree, the system of record wins. Chapter 51 relies on this when data flows back the other way.

### Layers in the warehouse

Ingested data lands in layers, each with a purpose.

- The **raw** layer holds data as it arrived, with as little change as possible. If a later step is wrong, you can rebuild from raw without asking the source again.
- The **staging** layer holds the same data cleaned and typed: dates as dates, quantities as numbers, consistent names.
- The **modeled** layer holds the business-ready tables that reports use, often built with dbt (Chapter 32).

This chapter covers raw and staging. Chapter 49 covers how the warehouse stores these layers, and Chapter 32 covers modeling on top of them.

> **Simplification note.** The chapter uses a local DuckDB file as the warehouse, so everything runs on your computer for free. The patterns are the same on cloud warehouses such as Snowflake, BigQuery, Redshift, or Databricks; Chapter 49 compares them.

---

## 45.2 Setting up the practice environment

The companion folder `companion/ch45/` contains four small helper files. You'll use them, but you won't need to change them.

| File | What it does |
|---|---|
| `reset_ch45.py` | Creates `riverstone_source`, a private copy of `riverstone_2025`, deletes the local warehouse, and writes the practice files. Run it any time to start again. |
| `apply_day.py` | Simulates later business days in the ERP: new orders, and status changes to existing ones. |
| `mock_crm_api.py` | A tiny local web server that behaves like the CRM's API, including authentication, pagination, and rate limiting. |
| `make_files.py` | Writes Bhiwandi Main's dispatch files, messy in realistic ways. |

Your copy of `riverstone_source` is disposable. The shared practice databases from Chapter 12 are never changed.

Change data capture in section 45.6 needs one PostgreSQL setting, `wal_level = logical`. It's covered there, with the exact steps.

### Step 1. Your practice folder

Work the way Chapter 17 did. In your file manager, copy the folder `companion/ch45` and paste it inside `work`, so you have `work/ch45` to practise in and the original stays untouched.

### Step 2. Install two new libraries

Open a terminal (Chapter 26, section 26.0), go to the book folder, then into your practice folder, and activate the book's virtual environment:

<!-- run: none -->
```
# terminal
$ cd work/ch45
$ source ../../.venv/bin/activate
$ python -m pip install psycopg2-binary==2.9.13 duckdb==1.5.6
```

How it works:

- **`cd work/ch45`** moves into your practice folder. **`source ../../.venv/bin/activate`** activates the environment from Chapter 17, two levels up; on Windows PowerShell it's `..\..\.venv\Scripts\Activate.ps1`. The prompt starts with `(.venv)` when it's active.
- **`psycopg2-binary`** is a PostgreSQL **driver**: the library Python uses to talk to PostgreSQL directly. "Binary" means it comes pre-built, so nothing needs compiling. Chapter 18 installed a newer driver, `psycopg` (version 3), for SQLAlchemy to use. This chapter's companion files, and the next chapters that build on them, use the older and still very common psycopg2. The two work almost the same way.
- **`duckdb`** is the analytical database this chapter uses as its warehouse (section 45.1's simplification note).
- `==2.9.13` and `==1.5.6` ask for the exact versions used for this chapter's outputs. `requests` and `python-dotenv` are already installed, from Chapter 18.

Add `psycopg2-binary` and `duckdb` to your `requirements.txt`, one per line, so the environment can be rebuilt (Chapter 26). Then check that both libraries import:

```
# terminal
$ python -c "import psycopg2, duckdb; print(duckdb.__version__)"
1.5.6
```

**`python -c`** runs the Python code in quotes and exits. If both imports work, it prints DuckDB's version. An error such as `ModuleNotFoundError` means the environment wasn't active when you installed: activate it and install again.

### Step 3. Tell Python where the source database is

Python finds `riverstone_source` through a **connection string**: space-separated `key=value` pairs, such as `dbname=riverstone_source user=postgres password=your-password host=localhost port=5432`. Any key you leave out takes a default: your computer's login name as the user, this computer as the host, and port 5432. On Windows, the PostgreSQL installer from Chapter 12 set a password for the `postgres` user, so you need `user` and `password`.

Keep the string out of your code. Put it in a `.env` file in `work/ch45`, as Chapter 18 did, with your own password in place of `your-password`:

```text
RIVERSTONE_SOURCE=dbname=riverstone_source user=postgres password=your-password host=localhost
```

The notebook reads it with `load_dotenv()`. If your PostgreSQL needs no password (common with Postgres.app and on Linux), you can skip the file: the code falls back to plain `dbname=riverstone_source`.

### Step 4. Start the notebook

In VS Code, open the `analyst-to-architect` folder, create a new Jupyter notebook, choose the `.venv` kernel, and save it as `ch45.ipynb` in `work/ch45` (Chapter 17, section 17.0). Its working folder is then `work/ch45`, where the companion files are.

Run each code block in this chapter as its own cell, top to bottom, **without restarting the kernel**. Later cells use names that earlier cells create, such as `wh`, `fetch_rows`, and `new_rows`. If you restart, run the cells again from the top.

The first cell:

```python
import os, time, hashlib
import psycopg2, duckdb, requests
from dotenv import load_dotenv

load_dotenv()
from reset_ch45 import reset
from apply_day import apply_day

reset()
SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
wh = duckdb.connect("warehouse/riverstone_wh.duckdb")
print("source and warehouse ready")
```

```
source and warehouse ready
```

**How it works, line by line.**

- `os` reads environment variables and file sizes; `time` lets the code wait (section 45.9); `hashlib` computes fingerprints (section 45.5). All three come with Python.
- `psycopg2` talks to PostgreSQL, `duckdb` is the warehouse, and `requests` calls APIs (Chapter 18).
- `load_dotenv()` copies the `.env` file's variables into the environment, exactly as in Chapter 18. It comes before the companion imports, because they read `RIVERSTONE_SOURCE` when they load.
- `reset()` builds a fresh environment. It copies `riverstone_2025` into a new `riverstone_source` with `CREATE DATABASE ... TEMPLATE`, deletes the old warehouse, and creates the folders `warehouse/` and `exports/`, with the two dispatch files in `exports/`. PostgreSQL copies a database only while nobody else is connected to it, so `reset()` first closes any other connection to `riverstone_2025` or `riverstone_source`, such as an open DBeaver tab (DBeaver reconnects the next time you use it). It needs a user that may create databases; the local `postgres` user can. It reads the same `RIVERSTONE_SOURCE` string as the notebook.
- `SRC` is the connection string: the one from `.env` if there is one, otherwise the default. `os.environ.get(name, default)` returns the default instead of stopping when the variable isn't set.
- `duckdb.connect()` opens (or creates) the warehouse as a single file. **DuckDB** is an analytical database that runs inside your Python process, with no server to install.

### Talking to DuckDB from Python

Chapter 18 mentioned DuckDB; this is its first real use. Three calls show everything the chapter needs:

```python
print(wh.execute("SELECT 1 + 1").fetchone())
print(wh.execute("SELECT 42 AS x, 'a' AS y").fetchall())
print(wh.execute("SELECT ?::INTEGER * 2", [21]).fetchone())
```

```
(2,)
[(42, 'a')]
(42,)
```

- `wh.execute(sql)` runs one SQL statement and returns its result. **`.fetchone()`** takes the first row, as a tuple: `(2,)` is a tuple with one item, which is why it has a comma.
- **`.fetchall()`** takes every row, as a list of tuples: here one row with two columns.
- **`?`** marks a value you pass separately, in a list after the SQL: `[21]` fills the one `?`. `::INTEGER` is the cast shorthand from Chapter 28; DuckDB accepts it too.

> **Tool note.** The outputs in this chapter were produced with Python 3.11.15, DuckDB 1.5.6, psycopg2 2.9.13, requests 2.33.1, python-dotenv 1.2.3, and PostgreSQL 16.13. Newer versions may format a few outputs slightly differently.

---

## 45.3 Full loads

A **full load** copies everything from a source table into the warehouse, replacing what was there. It's the simplest pattern, and often the right one.

### Talking to PostgreSQL from Python

First, one query to the source, with nothing hidden:

```python
conn = psycopg2.connect(SRC)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM orders")
print(cur.fetchone())
conn.close()
```

```
(175,)
```

- **`psycopg2.connect(SRC)`** opens a **connection**: the line to the database. It uses the connection string from section 45.2.
- **`conn.cursor()`** creates a **cursor**: the pen you write queries with. A connection can have several.
- **`cur.execute(...)`** sends one query. **`cur.fetchone()`** takes the first row of the answer, as a tuple, exactly as in DuckDB: 175 orders.
- **`conn.close()`** hangs up. Every connection you open, close.

The two libraries mark values you pass separately with different symbols. It's an easy slip, so keep this in mind:

| Library | Placeholder | Example |
|---|---|---|
| psycopg2 (PostgreSQL) | `%s` | `cur.execute("... WHERE order_id > %s", (10175,))` |
| DuckDB | `?` | `wh.execute("... WHERE order_id > ?", [10175])` |

### A small helper, then the load

Every query to the source opens a connection, runs, and closes. A function saves repeating that:

```python
def fetch_rows(sql, params=None):
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
    conn.close()
    return cols, rows

cols, rows = fetch_rows(
    "SELECT order_id, customer_id, order_date, status, sales_rep_id FROM orders")
print(cols)
print(rows[0])
```

```
['order_id', 'customer_id', 'order_date', 'status', 'sales_rep_id']
(10001, 2, datetime.date(2025, 1, 2), 'Delivered', 3)
```

**How it works, line by line.**

- `params=None` lets you pass values for `%s` placeholders; with none, the query runs as written.
- **`with conn, conn.cursor() as cur:`** opens two things at once. `with conn` commits the work if the block succeeds and rolls it back if anything fails (Chapter 12's transactions), but it does **not** close the connection; that's why `conn.close()` follows. `conn.cursor() as cur` creates the cursor and closes it at the end of the block.
- `cur.fetchall()` returns every row as a list of tuples.
- **`cur.description`** describes the answer's columns, one entry per column; `d[0]` is each column's name.
- The function returns two things, and `cols, rows = ...` unpacks them into two names. The first row is order 10001: psycopg2 turns a PostgreSQL `date` into a Python `datetime.date`.

Now load those rows into the warehouse:

```python
wh.execute("CREATE SCHEMA IF NOT EXISTS raw")
wh.execute("""
    CREATE OR REPLACE TABLE raw.orders (
        order_id     INTEGER PRIMARY KEY,
        customer_id  INTEGER NOT NULL,
        order_date   DATE NOT NULL,
        status       VARCHAR NOT NULL,
        sales_rep_id INTEGER
    )""")
wh.executemany("INSERT INTO raw.orders VALUES (?, ?, ?, ?, ?)", rows)

print("rows read from source :", len(rows))
print("rows in raw.orders    :",
      wh.execute("SELECT COUNT(*) FROM raw.orders").fetchone()[0])
```

```
rows read from source : 175
rows in raw.orders    : 175
```

**How it works, line by line.**

- `CREATE SCHEMA IF NOT EXISTS raw` makes the raw layer, a schema as in Chapter 12.
- `CREATE OR REPLACE TABLE` throws away yesterday's copy and creates an empty table with explicit types. Declaring types, instead of letting the tool guess, is the first habit of reliable ingestion.
- `executemany()` runs the same `INSERT` once for every tuple in `rows`. The `?` placeholders keep values separate from the SQL text, which avoids quoting mistakes and SQL injection.
- The last two lines compare the count read with the count stored. `.fetchone()[0]` takes the first item of the first row. Chapter 12 asked you to run `COUNT(*)` against the source after loading; this is the same check, automated.

### Reconcile more than the row count

Row counts can match while the contents don't. A slightly stronger check compares counts by a meaningful category. You'll run it again after every load, so it's a function:

```python
def compare_status():
    cols, status_rows = fetch_rows("SELECT status, COUNT(*) FROM orders GROUP BY status")
    src_status = dict(status_rows)
    wh_status = dict(wh.execute(
        "SELECT status, COUNT(*) FROM raw.orders GROUP BY status").fetchall())
    for s in sorted(set(src_status) | set(wh_status)):
        src_n, wh_n = src_status.get(s, 0), wh_status.get(s, 0)
        flag = "" if src_n == wh_n else "   <-- differs"
        print(f"{s:<10} source={src_n:>3}  warehouse={wh_n:>3}{flag}")

compare_status()
```

```
Cancelled  source=  2  warehouse=  2
Delivered  source=171  warehouse=171
Pending    source=  1  warehouse=  1
Shipped    source=  1  warehouse=  1
```

**How it works, line by line.**

- Each query returns rows like `('Delivered', 171)`. **`dict(...)`** turns a list of two-item tuples into a dictionary: `'Delivered'` becomes a key and `171` its value.
- **`set(src_status) | set(wh_status)`** is every status found on *either* side (`|` is set union). Loop over both sides, or a status that exists only in the warehouse is invisible to the check.
- **`.get(s, 0)`** reads a count, or 0 when that side has no such status.
- `flag` is empty when the counts agree and points at them when they don't. `{s:<10}` pads the status to 10 characters, left-aligned, and `{src_n:>3}` right-aligns a number in 3 (Chapter 17's f-strings).

Everything matches: 175 orders, 171 of them delivered. A **reconciliation check** like this compares a summary of the source with the same summary of the warehouse. It's cheap, and it catches a surprising number of problems.

### When a full load is the right choice

Full loads are **simple**, **self-correcting** (every run fixes any earlier mistake), and they **capture updates and deletes** automatically, because the whole table is replaced. Choose them when:

- the table is small or medium: Riverstone's customers, products, and employees are ideal;
- the source can handle reading the whole table without slowing the business down;
- the load finishes comfortably inside the time you have.

They stop being practical when a table is large, changes slowly, or sits in a busy production system. Reading a hundred million order lines every night to find the few thousand that changed is slow, expensive, and hard on the ERP. That's where incremental loads come in.

---

## 45.4 Incremental loads, and the update they miss

An **incremental load** reads only the rows that are new or changed since the last load. To know what "since the last load" means, it keeps a **watermark**: a stored value marking how far the previous load got, such as the highest ID or the latest timestamp it saw.

### By hand first

Take a tiny orders table. On day 1 the warehouse loaded all four orders, so the watermark is 4, the highest ID it saw. By day 2, the source has changed:

| order_id | In the warehouse after day 1 | In the source on day 2 |
|---|---|---|
| 1 | Delivered | Delivered |
| 2 | Delivered | Delivered |
| 3 | Pending | **Cancelled** |
| 4 | Shipped | Shipped |
| 5 | (not there) | **Pending** (new) |

Before reading on, answer two questions. The day-2 load reads `WHERE order_id > 4`: which rows does it read? And after it, what does the warehouse say about order 3?

It reads only order 5. The warehouse still says order 3 is Pending, which is wrong: the change happened below the watermark, where the load never looks. Figure 45.2 draws the same thing for the real orders you're about to load.

![A timeline for 1 and 2 January. On 1 January the warehouse has orders up to 10175 and the watermark is set at 10175. On 2 January the ERP inserts orders 10176 and 10177 above the watermark, and updates orders 10174 and 10175 below it. The incremental load reads only the band above the watermark, marked with a tick and the word READ, and loads the two new orders. The two updates, in the band below the watermark, are marked with a cross and the word MISSED.](figures/fig45-2-watermark-misses-updates.svg)

*Figure 45.2 — Why an ID watermark misses updates. The load only looks above the line; changes to older rows happen below it.*

### The same thing, on Riverstone's orders

It's now 2 January 2026. The ERP has had a business day. Apply it, then run the most common incremental pattern: load rows with an ID above the watermark.

```python
apply_day(1)

watermark = wh.execute("SELECT MAX(order_id) FROM raw.orders").fetchone()[0]
cols, new_rows = fetch_rows("""
    SELECT order_id, customer_id, order_date, status, sales_rep_id
    FROM orders
    WHERE order_id > %s
    ORDER BY order_id""", (watermark,))
wh.executemany("INSERT INTO raw.orders VALUES (?, ?, ?, ?, ?)", new_rows)

print("watermark before load:", watermark)
print("new rows loaded      :", [r[0] for r in new_rows])
```

```
watermark before load: 10175
new rows loaded      : [10176, 10177]
```

**How it works.**

- `apply_day(1)` runs 2 January's changes in the ERP.
- The watermark is the highest `order_id` already in the warehouse.
- `%s` in the query is filled from `(watermark,)`, a tuple with one item: the trailing comma is what makes it a tuple. psycopg2 sends the value separately from the SQL, as section 45.3's placeholder table showed.
- `[r[0] for r in new_rows]` lists the first item, the order ID, of each new row.

The load ran, found two new orders, and finished without errors. Now run the reconciliation check from section 45.3 again, and look at two older orders:

```python
compare_status()
print(wh.execute("SELECT order_id, status FROM raw.orders "
                 "WHERE order_id IN (10174, 10175) ORDER BY order_id").fetchall())
```

```
Cancelled  source=  3  warehouse=  2   <-- differs
Delivered  source=172  warehouse=171   <-- differs
Pending    source=  2  warehouse=  3   <-- differs
Shipped    source=  0  warehouse=  1   <-- differs
[(10174, 'Pending'), (10175, 'Shipped')]
```

**Reading it.** The row counts match (177 in both), but four status counts don't. On 2 January, the ERP also *updated* two existing orders: order 10174 was cancelled, and order 10175 was delivered. Their IDs are below the watermark, so the load never looked at them. The warehouse still says 10174 is Pending and 10175 is Shipped, so it has a Shipped order that the source no longer has. A dashboard built on it would count a cancelled order as open business.

> **Watch out: a successful load is not a correct load.** The watermark load above raised no error and loaded exactly the rows it was designed to load. Only a reconciliation check against the source revealed the problem. Never judge a pipeline by whether it finished.

### Better watermarks, and their limits

The usual fix is a **last-updated timestamp**: a column such as `updated_at` that the source sets every time a row changes. Then the load reads `WHERE updated_at > watermark`, and updates are caught.

Riverstone's `orders` table, like many real ERP tables, has no such column. And where one exists, check three things before trusting it:

- **Does every change update it?** Bulk fixes run directly in the database often skip it.
- **Is it set when the change is committed, or when it started?** A long transaction that began before your last load can commit a timestamp you've already passed.
- **What about deletes?** A deleted row has no timestamp to find. Incremental loads by timestamp never see deletes.

A common safety margin is to **look back**: load rows where `updated_at > watermark - interval '1 hour'` and let the upsert (section 45.5) absorb the duplicates. When no reliable column exists, you need a different way to detect change, which is the next section.

---

## 45.5 Detecting change with hashes

### What a hash is

Chapter 2 introduced the idea: a **hash** is a fixed-length fingerprint of any data. The same data always gives the same fingerprint, and the smallest change gives a completely different one. Chapter 2 showed two payment lines with different fingerprints. Here is how they were made:

```python
text = "Pay Rs 14,700 to Riverstone Supplies"
print(hashlib.sha256(text.encode("utf-8")).hexdigest())
```

```
f4251ff3fb7191f7e79677f3b1871db06c0935c3cc08164496995f1f909f6f71
```

- **`text.encode("utf-8")`** turns the text into bytes (Chapter 2's bytes), because hashes work on bytes, not on letters.
- **`hashlib.sha256(...)`** runs the **SHA-256** algorithm on those bytes. `hashlib` comes with Python; the setup cell imported it.
- **`.hexdigest()`** gives the fingerprint as 64 hexadecimal characters (0–9 and a–f). Each character carries 4 bits, so 64 of them are 256 bits: the "256" in the name.

What happens if you change the text? Change it to the second payment line, `Pay Rs 17,400 ...`, and then run the first line again:

```python
print(hashlib.sha256("Pay Rs 17,400 to Riverstone Supplies".encode("utf-8")).hexdigest())
print(hashlib.sha256("Pay Rs 14,700 to Riverstone Supplies".encode("utf-8")).hexdigest())
```

```
9d2f842c50110e140abd578e7e8460d1f6f2bbca7eba341ce1e5bee43566d0fa
f4251ff3fb7191f7e79677f3b1871db06c0935c3cc08164496995f1f909f6f71
```

Swapping two digits changed every part of the fingerprint. Running the first line again gave exactly the same fingerprint as before. Does a longer input give a longer fingerprint? Predict, then run:

```python
for sample in ["Riverstone", "x" * 1000000]:
    digest = hashlib.sha256(sample.encode("utf-8")).hexdigest()
    print(len(sample), "characters in,", len(digest), "characters out")
```

```
10 characters in, 64 characters out
1000000 characters in, 64 characters out
```

`"x" * 1000000` repeats the letter a million times: about 1 MB of text. Both fingerprints are 64 characters long.

> **Four properties of a hash.**
> - **Deterministic:** the same input always gives the same fingerprint, on any computer.
> - **Fixed length:** one word or a million characters, SHA-256 always gives 64 characters.
> - **Avalanche:** a tiny change to the input changes the whole fingerprint, not just one part of it.
> - **One-way:** you can't work back from a fingerprint to the text.
>
> Two different inputs *could* in theory share a fingerprint (a **collision**), but with SHA-256 it's not something you will ever meet.

**Where hashes are used.**

- **Checking downloads.** A **checksum** is a hash published next to a file, such as the SHA-256 listed beside the Python installer. Hash what you downloaded; if it matches, the file arrived undamaged.
- **Checking backups** against the original (Chapter 2's exercise 9).
- **Passwords.** Systems store a fingerprint of your password, not the password. Real systems use a deliberately *slow* hash with a random extra value mixed in (a **salt**), such as bcrypt or Argon2, never plain SHA-256 or MD5, so that stolen fingerprints can't be tested against billions of guesses a second.
- **Pipelines.** Fingerprints of rows and of files tell you what changed since yesterday. That's the rest of this section.

You'll also meet an older algorithm, **MD5**. It's the one databases offer as a function called `md5()`:

```python
print(hashlib.md5(text.encode("utf-8")).hexdigest())
```

```
f3e2b15a5bacba44d562207000e67838
```

| Algorithm | Length | Speed | Use it for |
|---|---|---|---|
| **MD5** | 32 hex characters (128 bits) | Fast | Change detection. It's broken for security: people can deliberately make two different inputs with the same MD5 |
| **SHA-256** | 64 hex characters (256 bits) | Fast enough | Anything security-related, and files you must be sure of |

### Row hashes, by hand

Go back to the tiny table in section 45.4. Build one string from order 3's values, with a `|` between them, and fingerprint it before and after the change:

```python
print(hashlib.md5("3|Pending".encode("utf-8")).hexdigest())
print(hashlib.md5("3|Cancelled".encode("utf-8")).hexdigest())
```

```
b8379e4c6efbe5b331ea3a2fdb9858e5
c6777f82bb14454418119822ba5680a0
```

Different strings, different fingerprints. Keep yesterday's fingerprint of every row, compute today's, and every row whose fingerprint differs has changed, whatever its ID. No watermark is needed.

### Row hashes in SQL

Both databases can build the string and hash it themselves, so only the fingerprints travel. One detail first. SQL's `concat_ws` (concatenate with separator) joins values with a separator, but it **skips NULLs**:

```python
print(wh.execute("SELECT concat_ws('|', 1, NULL, 3), "
                 "concat_ws('|', 1, coalesce(NULL::text, '∅'), 3)").fetchone())
```

```
('1|3', '1|∅|3')
```

`1|3` loses the fact that the middle value was missing, so a value changing to or from NULL could go unnoticed. **`coalesce(value, '∅')`** (Chapter 12) puts a marker in place of a NULL, so the string keeps its shape. `sales_rep_id` is the one column in `orders` that can be NULL, so it gets the marker. Now fingerprint every order, on both sides, and look at an unchanged order and a changed one:

```python
HASH_SQL = """
    SELECT order_id,
           md5(concat_ws('|', order_id, customer_id, order_date, status,
                         coalesce(sales_rep_id::text, '∅'))) AS row_hash
    FROM orders"""
WH_HASH_SQL = """
    SELECT order_id,
           md5(concat_ws('|', order_id, customer_id,
                         strftime(order_date, '%Y-%m-%d'), status,
                         coalesce(sales_rep_id::text, '∅'))) AS row_hash
    FROM raw.orders"""

cols, hash_rows = fetch_rows(HASH_SQL)
source_hashes = dict(hash_rows)
wh_hashes = dict(wh.execute(WH_HASH_SQL).fetchall())
for order_id in [10173, 10174]:
    print(order_id, "source   :", source_hashes[order_id])
    print(order_id, "warehouse:", wh_hashes[order_id])
```

```
10173 source   : 31e3dbe0caabc12b48bed4c669ee5886
10173 warehouse: 31e3dbe0caabc12b48bed4c669ee5886
10174 source   : ce97b59465f0cd081ee9a4803c26bd63
10174 warehouse: 600caf6f8c577cd8f16ebfc0cfe0c939
```

**How it works.**

- `concat_ws('|', ...)` joins a row's values into one string with `|` between them, for example `10174|9|2025-12-21|Pending|5`. The separator matters: without it, the values `1` and `23` would join to the same `123` as `12` and `3`.
- `sales_rep_id::text` casts the number to text, so `coalesce` can offer the text marker as the alternative.
- `md5()` turns the string into a 32-character fingerprint. MD5 is fine for detecting change; it isn't safe for security, as the table above explains.
- PostgreSQL writes a date in its DateStyle setting, `2025-12-21` by default. On the warehouse side, `strftime(order_date, '%Y-%m-%d')` makes DuckDB write exactly the same. **Both sides must build the string identically**, or every row will look changed.
- `dict(...)` gives two dictionaries, order ID → fingerprint. Order 10173 didn't change, so both sides agree. Order 10174 was cancelled in the source, so its fingerprints differ.

Comparing the two dictionaries finds every difference at once. You'll need this again in section 45.6, so it's a function:

```python
def compare_hashes():
    cols, hash_rows = fetch_rows(HASH_SQL)
    source_hashes = dict(hash_rows)
    wh_hashes = dict(wh.execute(WH_HASH_SQL).fetchall())
    inserted = sorted(set(source_hashes) - set(wh_hashes))
    deleted = sorted(set(wh_hashes) - set(source_hashes))
    changed = sorted(k for k in set(source_hashes) & set(wh_hashes)
                     if source_hashes[k] != wh_hashes[k])
    return inserted, deleted, changed

inserted, deleted, changed = compare_hashes()
print("inserted:", inserted)
print("deleted :", deleted)
print("changed :", changed)
```

```
inserted: []
deleted : []
changed : [10174, 10175]
```

**How it works.**

- `set(source_hashes)` is the set of the dictionary's keys, the order IDs.
- **`-`** between sets keeps what's in the first and not the second: a key only in the source was **inserted**; a key only in the warehouse was **deleted**.
- **`&`** keeps what's in both. Of those, a key whose two fingerprints differ was **changed**. The `for ... if ...` inside `sorted()` works like a list comprehension without the brackets.
- The function returns three lists, and `inserted, deleted, changed = ...` unpacks them.

**Reading it.** The hash comparison finds exactly the two orders the watermark load missed, 10174 and 10175, and confirms there were no deletes. (The two new orders were already loaded, so they're not "inserted" here.)

### Applying the changes with an upsert

You wrote an **upsert** in Chapter 12: insert a row if its key is new, update it if the key already exists, with PostgreSQL's `INSERT ... ON CONFLICT ... DO UPDATE`. DuckDB has a shorthand, `INSERT OR REPLACE`, which replaces every column of the existing row. That's what a raw copy wants. Fetch the current version of the changed orders, and upsert them:

```python
cols, fresh = fetch_rows("""
    SELECT order_id, customer_id, order_date, status, sales_rep_id
    FROM orders WHERE order_id = ANY(%s)""", (changed,))
wh.executemany("INSERT OR REPLACE INTO raw.orders VALUES (?, ?, ?, ?, ?)", fresh)
print(wh.execute("SELECT order_id, status FROM raw.orders "
                 "WHERE order_id IN (10174, 10175) ORDER BY order_id").fetchall())
```

```
[(10174, 'Cancelled'), (10175, 'Delivered')]
```

- **`= ANY(%s)`** with `(changed,)`: psycopg2 turns the Python list `[10174, 10175]` into a PostgreSQL array, and `order_id = ANY(array)` matches any ID in it. It's the placeholder version of `IN (10174, 10175)`.
- `INSERT OR REPLACE` updates both rows in place.

Both orders are now correct. DuckDB also accepts Chapter 12's long form. It does the same job here, and lets you choose which columns to update:

```python
wh.executemany("""
    INSERT INTO raw.orders VALUES (?, ?, ?, ?, ?)
    ON CONFLICT (order_id) DO UPDATE SET
        customer_id = EXCLUDED.customer_id, order_date = EXCLUDED.order_date,
        status = EXCLUDED.status, sales_rep_id = EXCLUDED.sales_rep_id""", fresh)
print(wh.execute("SELECT order_id, status FROM raw.orders "
                 "WHERE order_id IN (10174, 10175) ORDER BY order_id").fetchall())
```

```
[(10174, 'Cancelled'), (10175, 'Delivered')]
```

As in Chapter 12, `EXCLUDED` means "the row you tried to insert". Many cloud warehouses spell the same idea `MERGE`.

### Why upserts make loads safe to repeat

A load that can be run twice with the same result is **idempotent**. Chapter 20 made the Flash email idempotent with a run key; here is the same property for a table load. It matters because loads fail halfway and get re-run, schedulers retry, and people press "run" again. A plain `INSERT` isn't idempotent. What do you expect if yesterday's two new orders are inserted a second time? Run it:

```python
try:
    wh.executemany("INSERT INTO raw.orders VALUES (?, ?, ?, ?, ?)", new_rows)
except duckdb.ConstraintException as e:
    print("plain INSERT, second run:", e)

wh.executemany("INSERT OR REPLACE INTO raw.orders VALUES (?, ?, ?, ?, ?)", new_rows)
wh.executemany("INSERT OR REPLACE INTO raw.orders VALUES (?, ?, ?, ?, ?)", new_rows)
print("upsert, run twice   :",
      wh.execute("SELECT COUNT(*) FROM raw.orders").fetchone()[0], "rows")
```

```
plain INSERT, second run: Constraint Error: Duplicate key "order_id: 10176" violates primary key constraint.
upsert, run twice   : 177 rows
```

- **`except duckdb.ConstraintException as e:`** catches only this kind of error, a broken constraint such as a duplicate primary key, and names it `e`. Any other error still stops the cell (Chapter 17's `try` and `except`).
- The upsert then runs twice, and the count is unchanged.

Here the primary key stopped the duplicate, which is exactly why raw tables should have one. Without a primary key, the plain insert would have silently doubled two orders. The upsert can run any number of times and leave 177 rows. Chapter 46 builds whole pipelines on this property, and tests it by making a run fail on purpose.

### The cost of row hashing

Hash comparison catches inserts, updates, and deletes without any help from the source. The price is that it reads **every row's key and hash** on every run. For Riverstone's 177 orders that's nothing; for a table of hundreds of millions of rows, it's a heavy scan of a production database each night. Common compromises:

- hash only a recent window, such as the last 90 days, where changes usually happen, plus a full comparison once a week;
- hash in chunks (by month or ID range), compare chunk hashes first, and drill into rows only where a chunk differs;
- use change data capture instead (section 45.6), which doesn't need to scan at all.

### File hashes: skipping files that haven't changed

The same idea applies to whole files. Bhiwandi Main saves its dispatch sheet into a shared folder every evening. Sometimes someone saves it twice; sometimes the file is re-sent unchanged. A file hash tells you whether you've already loaded exactly this content.

For a small file, read it all and hash it:

```python
path = "exports/dispatch_2026-01-02.csv"
h = hashlib.sha256()
with open(path, "rb") as f:
    h.update(f.read())
print(h.hexdigest())
```

```
56ac5c9f3112a1bdeed5e1f95e8cc7e5530c5a91bbe24c606c5accc5e1001d0b
```

- **`"rb"`** opens the file to read **bytes**, not text, so nothing is changed by decoding: the hash covers exactly what's on disk.
- **`h.update(...)`** feeds bytes into the hash; `hexdigest()` reads the fingerprint out.

A large file shouldn't be read into memory in one go. `update` can be called many times, and gives the same result as hashing everything at once, so read the file in pieces:

```python
def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

print(file_sha256(path))
```

```
56ac5c9f3112a1bdeed5e1f95e8cc7e5530c5a91bbe24c606c5accc5e1001d0b
```

- `f.read(65536)` reads at most 65,536 bytes (64 KB). At the end of the file it returns nothing, an empty bytes value, which counts as false, so `if not chunk: break` leaves the loop.
- The fingerprint is identical to the one above. This version works on files far larger than memory.

Now a **load log**: a table recording each file that was loaded, its fingerprint, and the day it was loaded for.

```python
wh.execute("""
    CREATE TABLE IF NOT EXISTS raw.file_log (
        file_name   VARCHAR,
        sha256      VARCHAR,
        loaded_for  DATE,
        rows_loaded INTEGER,
        loaded_at   TIMESTAMP,
        PRIMARY KEY (sha256, loaded_for))""")

def already_loaded(digest, loaded_for):
    row = wh.execute(
        "SELECT file_name FROM raw.file_log WHERE sha256 = ? AND loaded_for = ?",
        [digest, loaded_for]).fetchone()
    return row[0] if row else None

def record_loaded(path, digest, loaded_for, rows_loaded):
    wh.execute("INSERT INTO raw.file_log VALUES (?, ?, ?, ?, current_timestamp)",
               [os.path.basename(path), digest, loaded_for, rows_loaded])

print("already loaded?", already_loaded(file_sha256(path), "2026-01-02"))
```

```
already loaded? None
```

**How it works.**

- The key is the **pair** of fingerprint and day, `PRIMARY KEY (sha256, loaded_for)`: the same content may legitimately arrive for two different days (see the Watch out below).
- `already_loaded()` only *reads* the log. It returns the name of a file with the same content already loaded for that day, or `None`. `fetchone()` returns `None` when there's no row, so `row[0] if row else None` handles both cases.
- `record_loaded()` writes one line to the log, with the number of rows and the time (`current_timestamp`). `os.path.basename(path)` keeps just the file name.
- The two jobs are separate on purpose. Record a file only **after** it has loaded successfully. A log that records the file first, and then fails to load it, would make every later run skip the file as "already loaded", and its data would be lost without a sound.

Nothing has been loaded yet, so the answer is `None`. Section 45.7 loads this file, and only then records it.

> **Watch out: the same content isn't always the same file.** A hash tells you the *content* is identical. If a warehouse legitimately sends two identical dispatch files for two different days (no dispatches on both), skipping the second would be wrong. That's why the log's key includes the day the file was loaded for. Decide explicitly what "already loaded" means for each source.

---

## 45.6 Change data capture

Every change to a PostgreSQL database is first written to a **write-ahead log** (WAL): a running record of every insert, update, and delete, used for crash recovery and replication. **Change data capture** (CDC) reads changes from that log instead of querying tables. It sees every insert, update, and delete, in commit order, without scanning anything.

Here are the four ways to keep a warehouse table in step with its source, side by side. Notice which ones can see deletes.

| | Full load | Incremental (watermark) | Hash comparison | Change data capture |
|---|---|---|---|---|
| **Reads** | The whole table | Rows past the last ID or time | Every key and hash | The database's change log |
| **Sees inserts** | ✓ Yes | ✓ Yes | ✓ Yes | ✓ Yes |
| **Sees updates** | ✓ Yes | ✗ Only with a reliable `updated_at` | ✓ Yes | ✓ Yes, in order |
| **Sees deletes** | ✓ Yes | ✗ No | ✓ Yes | ✓ Yes |
| **Load on the source** | ✗ Heavy for big tables | ✓ Light | Medium to heavy | ✓ Very light |
| **Complexity** | ✓ Simplest | ✗ Simple, but misses changes silently | Moderate | ✗ Settings, permissions, slots |

### Turning CDC on

CDC needs PostgreSQL to write enough detail into the log. That's controlled by one setting, `wal_level`, which needs a server restart. The default is `replica`.

1. In DBeaver's SQL editor (Chapter 12), connected as `postgres`, run `ALTER SYSTEM SET wal_level = logical;`. **`ALTER SYSTEM`** writes the setting into a file PostgreSQL reads when it starts (`postgresql.auto.conf`), so you don't have to find and edit configuration files by hand.
2. Restart PostgreSQL. **Windows:** open the Services app, find `postgresql-x64-16`, and choose Restart. **macOS with Homebrew:** `brew services restart postgresql@16`; **with Postgres.app:** Stop, then Start. **Linux:** `sudo systemctl restart postgresql`.
3. Check from the notebook, in the next cell.

Your local `postgres` user is a **superuser**, allowed to do anything, including creating the replication slot below. On a company database this is a change for the database administrator, not for you: it increases log volume, and CDC needs a user with the `REPLICATION` permission. Managed cloud databases expose the same setting under a different name; check the provider's documentation.

```python
cdc_conn = psycopg2.connect(SRC)
cdc_conn.autocommit = True
cur = cdc_conn.cursor()
cur.execute("SHOW wal_level")
print(cur.fetchone())
```

```
('logical',)
```

- `cdc_conn` is a connection kept open for this section, named so it doesn't clash with other names.
- **`cdc_conn.autocommit = True`** makes every statement take effect the moment it runs. By default psycopg2 opens a transaction and waits for `commit()`; that suits `fetch_rows()`, which commits and closes at once, but not a connection you keep open and use cell by cell. It also matters for the slot below: PostgreSQL refuses to create a slot inside a transaction that has already written anything, and with autocommit every statement is a transaction of its own.
- `SHOW wal_level` reads the setting. If it says `('replica',)`, the restart hasn't happened yet.

> **Simplification note.** Production CDC usually runs through a dedicated tool, such as the open-source Debezium, or through a managed connector, and it streams changes continuously (Chapter 50). This section uses PostgreSQL's built-in `test_decoding` plugin, which prints changes as readable text. It's meant for learning and testing, not for production pipelines.

### Reading real changes

A **replication slot** is a bookmark in the log. PostgreSQL keeps every change after the bookmark until a reader consumes it, so nothing is lost between reads. Create a slot, then let the ERP have another business day (5 January 2026):

```python
cur.execute("SELECT slot_name "
            "FROM pg_create_logical_replication_slot('ch45_slot', 'test_decoding')")
print("slot created:", cur.fetchone()[0])

apply_day(2)

cur.execute("SELECT data FROM pg_logical_slot_get_changes('ch45_slot', NULL, NULL)")
for (line,) in cur.fetchall():
    if line.startswith("table "):
        print(line)
```

```
slot created: ch45_slot
table public.orders: UPDATE: order_id[integer]:10176 customer_id[integer]:9 order_date[date]:'2026-01-02' status[character varying]:'Shipped' sales_rep_id[integer]:5
table public.orders: INSERT: order_id[integer]:10178 customer_id[integer]:17 order_date[date]:'2026-01-05' status[character varying]:'Pending' sales_rep_id[integer]:3
table public.order_items: INSERT: order_item_id[integer]:334 order_id[integer]:10178 product_id[integer]:102 quantity[integer]:25 unit_price[numeric]:750.00 discount_pct[numeric]:0.00
```

**How it works.**

- `pg_create_logical_replication_slot()` creates the bookmark and names the plugin that turns log records into text.
- `apply_day(2)` runs the day's changes in the ERP, in one transaction.
- `pg_logical_slot_get_changes()` returns every change since the bookmark, then moves the bookmark forward. The two `NULL`s mean "no limit": read everything waiting.
- Each row comes back as a one-item tuple; **`for (line,) in ...`** unpacks that one item into `line`.
- The plugin also returns `BEGIN` and `COMMIT` lines with transaction numbers, which change on every run, so **`line.startswith("table ")`** keeps only the table changes.

**Reading a change line.** Each one reads `table <schema>.<table>: <INSERT|UPDATE|DELETE>: column[type]:value ...`. An INSERT or UPDATE carries the full new row. A DELETE carries only the primary key, for example `table public.orders: DELETE: order_id[integer]:10150`, which is all you need to delete the row from the warehouse.

**Reading it.** Three changes, in the order they were committed: order 10176 moved to Shipped, a new order 10178 was created, and its order line was inserted. The warehouse can apply each one with an upsert. No table was scanned.

Read the slot again, and there's nothing waiting:

```python
cur.execute("SELECT data FROM pg_logical_slot_get_changes('ch45_slot', NULL, NULL)")
print("changes waiting:", len(cur.fetchall()))
```

```
changes waiting: 0
```

### Both methods agree

As a check, run the hash comparison from section 45.5. It should find what CDC found.

```python
inserted, deleted, changed = compare_hashes()
print("inserted:", inserted, " deleted:", deleted, " changed:", changed)
```

```
inserted: [10178]  deleted: []  changed: [10176]
```

The hash comparison, which scanned every order, found the same two changes to `orders` that CDC reported from the log.

### Watching a slot

PostgreSQL keeps every log record a slot hasn't consumed. So the one thing to monitor is how far each slot is **behind**: how much log is waiting for it.

```python
cur.execute("""
    SELECT slot_name, active,
           pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(),
                                          confirmed_flush_lsn)) AS behind
    FROM pg_replication_slots""")
print(cur.fetchall())
cdc_conn.close()
```

```
[('ch45_slot', False, '0 bytes')]
```

- **`pg_replication_slots`** lists every slot. `active` says whether a reader is connected right now.
- `pg_current_wal_lsn()` is the log's current position, and `confirmed_flush_lsn` is how far the slot has read. **`pg_wal_lsn_diff()`** is the distance between them in bytes, and `pg_size_pretty()` writes it for people. Nothing is waiting, because the cell above read everything; if the database has written a little since, you may see a few bytes.
- `cdc_conn.close()` closes this section's connection.

Run this check on a schedule, and **alert when `behind` grows day after day**: it means the reader has stopped.

> **Watch out: an abandoned slot fills the disk.** If a CDC reader stops for days and nobody notices, the log grows until the database server runs out of disk space, and the ERP stops. Watch slot lag with the query above, and drop slots you no longer use: `SELECT pg_drop_replication_slot('ch45_slot');`. The companion's `reset()` does this for you.

### Choosing a strategy

| If… | Consider |
|---|---|
| The table is small, or you're not sure | A **full load** |
| Rows are only ever added, never changed (events, log entries) | **Incremental by ID or timestamp** |
| Rows change, and a trustworthy `updated_at` exists | **Incremental by timestamp**, with a look-back window and an upsert |
| Rows change, no trustworthy column, table not huge | **Hash comparison** |
| Rows change, the table is large or busy, or you need deletes and low delay | **Change data capture** |

Many platforms mix them: CDC for the big, busy order tables; full loads for products and employees; files and APIs for everything else.

---

## 45.7 Loading files reliably

Chapter 12 promised this chapter would cover loading large and messy files reliably. Files are still one of the most common ways data arrives, especially from spreadsheets, partners, banks, and older systems.

Bhiwandi Main's dispatch sheet for 2 January 2026 was saved from a spreadsheet. Here's the file as it appears in a text editor:

```text
dispatch_id,order_id,dispatch_date,warehouse,qty_units,remarks
D-2601,10175,02-01-2026,Bhiwandi Main,100,"Delivered to site, signed"
D-2602,10173,02-01-2026,Bhiwandi Main,"1,200",Part load
D-2603,10172,02-01-2026,Bhiwandi Main,N/A,Awaiting count
D-2604,10171,02-01-2026,Bhiwandi Main,85,
D-2605,10170,02-01-2026,Bhiwandi Main,"2,040","Two trucks; second at 4 pm"
```

It looks tidy. It has five traps: an invisible **byte-order mark** (BOM) at the very start, which some tools read as part of the first column name; dates written day-first (`02-01-2026` is 2 January, not 1 February); quantities with thousands separators, which have to be quoted; a quantity of `N/A`; and Windows line endings with a blank line at the end.

### What an automatic reader does

Modern readers try to detect everything for you. DuckDB's `read_csv` is good at it. This cell prints the first three rows, one per line, and then each column's name and detected type:

```python
for row in wh.execute(
        "SELECT * FROM read_csv('exports/dispatch_2026-01-02.csv') LIMIT 3").fetchall():
    print(row)
for row in wh.execute(
        "DESCRIBE SELECT * FROM read_csv('exports/dispatch_2026-01-02.csv')").fetchall():
    print(row[:2])
```

```
('D-2601', 10175, datetime.date(2026, 1, 2), 'Bhiwandi Main', '100', 'Delivered to site, signed')
('D-2602', 10173, datetime.date(2026, 1, 2), 'Bhiwandi Main', '1,200', 'Part load')
('D-2603', 10172, datetime.date(2026, 1, 2), 'Bhiwandi Main', 'N/A', 'Awaiting count')
('dispatch_id', 'VARCHAR')
('order_id', 'BIGINT')
('dispatch_date', 'DATE')
('warehouse', 'VARCHAR')
('qty_units', 'VARCHAR')
('remarks', 'VARCHAR')
```

- **`read_csv('...')`** reads a CSV file as if it were a table, so you can `SELECT` from it.
- **`DESCRIBE`** lists the columns a query would return, with their types. Each of its rows has six items; `row[:2]` keeps the first two, the name and the type.

**Reading it.** DuckDB handled the byte-order mark, the quoted commas, and the blank line. For the dates, it *guessed* day-first. It had no way to know, because `02-01-2026` fits both orders. It happened to be right for an Indian file; a file from a US system would have been silently wrong. And look at the types: `qty_units` came in as **VARCHAR**, text, because of `"1,200"` and `N/A`. Nothing failed. A report that sums this column will either error much later or, in a spreadsheet, quietly skip the text values. Automatic detection is a helpful first look, and a risky way to run a daily load, because tomorrow's file may be guessed differently.

> **Watch out: guessed types change from file to file.** If tomorrow's file happens to contain only plain numbers, the same column will be detected as an integer; the day after, as text again. Downstream code that worked yesterday breaks, or worse, silently changes behavior. In a scheduled load, declare the columns.

### Declare the columns, keep the raw text, then type in staging

A reliable file load has two steps. First, load into raw with **declared columns**, keeping awkward fields as text so that nothing is lost or guessed. Second, convert to proper types in staging, and **set aside** the values that can't be converted.

The raw table is created once. Besides the file's six columns, every row records the file it came from and when it was loaded, so any number can be traced back:

```python
wh.execute("""
    CREATE TABLE IF NOT EXISTS raw.dispatch (
        dispatch_id   VARCHAR,
        order_id      INTEGER,
        dispatch_date VARCHAR,
        warehouse     VARCHAR,
        qty_units     VARCHAR,
        remarks       VARCHAR,
        source_file   VARCHAR,
        loaded_at     TIMESTAMP)""")
```

`dispatch_date` and `qty_units` are text on purpose: raw keeps exactly what the file says. Now the load, using the load log from section 45.5:

```python
def load_dispatch(path, day):
    digest = file_sha256(path)
    seen = already_loaded(digest, day)
    if seen:
        return f"skip: same content as {seen}, already loaded for {day}"
    wh.execute("DELETE FROM raw.dispatch WHERE source_file = ?", [path])
    wh.execute("""
        INSERT INTO raw.dispatch
        SELECT *, current_timestamp
        FROM read_csv(?, header = true, filename = true,
            columns = {'dispatch_id': 'VARCHAR', 'order_id': 'INTEGER',
                       'dispatch_date': 'VARCHAR', 'warehouse': 'VARCHAR',
                       'qty_units': 'VARCHAR', 'remarks': 'VARCHAR'})""", [path])
    n = wh.execute("SELECT COUNT(*) FROM raw.dispatch WHERE source_file = ?",
                   [path]).fetchone()[0]
    record_loaded(path, digest, day, n)
    return f"loaded {n} rows from {path}"

print(load_dispatch("exports/dispatch_2026-01-02.csv", "2026-01-02"))
print(load_dispatch("exports/dispatch_2026-01-02.csv", "2026-01-02"))
```

```
loaded 5 rows from exports/dispatch_2026-01-02.csv
skip: same content as dispatch_2026-01-02.csv, already loaded for 2026-01-02
```

**How it works, line by line.**

- The function first asks the load log whether this content was already loaded for this day. The second call finds it, and skips.
- `DELETE FROM raw.dispatch WHERE source_file = ?` removes any rows an earlier load of the same file left. If a *corrected* file arrives under the same name, its content and fingerprint are new, so it loads, and the delete stops its rows from doubling up. Delete-then-insert by file makes the reload idempotent, like the upsert in section 45.5.
- `read_csv(?, ...)` takes the file name as a parameter. **`header = true`** says the first line holds column names. **`columns = {...}`** declares every column's name and type, as `'name': 'TYPE'` pairs inside braces; DuckDB then guesses nothing.
- **`filename = true`** adds one more column, the path of the file each row came from. With `current_timestamp` after `SELECT *`, the rows match the raw table's eight columns: the file's six, then `source_file`, then `loaded_at`.
- Only after the insert succeeds does `record_loaded()` write to the load log, with the real row count.

Look at what landed:

```python
for row in wh.execute("SELECT dispatch_id, dispatch_date, qty_units, remarks, source_file "
                      "FROM raw.dispatch").fetchall():
    print(row)
```

```
('D-2601', '02-01-2026', '100', 'Delivered to site, signed', 'exports/dispatch_2026-01-02.csv')
('D-2602', '02-01-2026', '1,200', 'Part load', 'exports/dispatch_2026-01-02.csv')
('D-2603', '02-01-2026', 'N/A', 'Awaiting count', 'exports/dispatch_2026-01-02.csv')
('D-2604', '02-01-2026', '85', None, 'exports/dispatch_2026-01-02.csv')
('D-2605', '02-01-2026', '2,040', 'Two trucks; second at 4 pm', 'exports/dispatch_2026-01-02.csv')
```

The raw table holds exactly what the warehouse team wrote, including `N/A`, and each row names its file. Now convert in staging:

```python
wh.execute("CREATE SCHEMA IF NOT EXISTS staging")
wh.execute("""
    CREATE OR REPLACE TABLE staging.dispatch AS
    SELECT dispatch_id,
           order_id,
           strptime(dispatch_date, '%d-%m-%Y')::DATE          AS dispatch_date,
           warehouse,
           TRY_CAST(replace(qty_units, ',', '') AS INTEGER)   AS qty_units,
           remarks
    FROM raw.dispatch""")
bad = wh.execute("""
    SELECT dispatch_id, qty_units
    FROM raw.dispatch
    WHERE TRY_CAST(replace(qty_units, ',', '') AS INTEGER) IS NULL""").fetchall()
for row in wh.execute("SELECT dispatch_id, dispatch_date, qty_units "
                      "FROM staging.dispatch ORDER BY dispatch_id").fetchall():
    print(row)
print("rows needing attention:", bad)
```

```
('D-2601', datetime.date(2026, 1, 2), 100)
('D-2602', datetime.date(2026, 1, 2), 1200)
('D-2603', datetime.date(2026, 1, 2), None)
('D-2604', datetime.date(2026, 1, 2), 85)
('D-2605', datetime.date(2026, 1, 2), 2040)
rows needing attention: [('D-2603', 'N/A')]
```

**How it works, line by line.**

- `strptime(dispatch_date, '%d-%m-%Y')` reads the date with an **explicit format**: day, month, year. If a date doesn't match, the load fails loudly instead of swapping day and month. `strptime` returns a date *and time* (midnight); `::DATE` keeps only the date. `::` is the cast shorthand from Chapter 28, which DuckDB accepts too.
- `replace(qty_units, ',', '')` removes the thousands separators, so `"1,200"` becomes `1200`.
- `TRY_CAST(... AS INTEGER)` converts to a whole number, and returns NULL instead of an error when it can't. A plain `CAST` would stop the whole load on `N/A`.
- The second query lists the rows where conversion failed, so a person can follow up.

### Reconcile the file

Now prove the load is complete: compare what's in the file with what's in the tables.

```python
with open("exports/dispatch_2026-01-02.csv", encoding="utf-8-sig") as f:
    data_lines = [line for line in f.read().splitlines()[1:] if line.strip()]
loaded = wh.execute("SELECT COUNT(*) FROM staging.dispatch").fetchone()[0]
usable = wh.execute(
    "SELECT COUNT(*) FROM staging.dispatch WHERE qty_units IS NOT NULL").fetchone()[0]
print("data lines in file :", len(data_lines))
print("rows loaded        :", loaded)
print("rows with a usable quantity:", usable)
print("total units (usable rows):",
      wh.execute("SELECT SUM(qty_units) FROM staging.dispatch").fetchone()[0])
```

```
data lines in file : 5
rows loaded        : 5
rows with a usable quantity: 4
total units (usable rows): 3425
```

- **`encoding="utf-8-sig"`** reads UTF-8 and drops the invisible byte-order mark if there is one: the fix for the first trap.
- `f.read().splitlines()` splits the file into lines, and **`[1:]`** keeps everything after the header line.
- **`if line.strip()`** skips lines that are empty or only spaces, such as the blank line at the end. `strip()` removes spaces from both ends, and an empty result counts as false.
- The three queries count the loaded rows, the rows with a quantity, and the total units.

**What to tell the dispatch supervisor.** All five dispatches were loaded. Four have quantities, totaling 3,425 units. Dispatch D-2603 for order 10172 has no quantity ("N/A, awaiting count"), so it's excluded from unit totals until the count arrives. Please send the corrected quantity, or update the sheet before tonight's load.

> **Simplification note.** Counting lines works here because no field contains a line break. Real files sometimes do (an address or a remark typed over two lines, inside quotes), so production reconciliation counts *records* with a proper CSV parser, not raw lines, and compares against a count or total supplied by the sender when one exists.

### A robust file-loading checklist

![A left-to-right checklist for loading a file, in six numbered boxes. Receive: check the name pattern, hash the file and skip exact repeats, and record it in the load log after loading. Read: declare encoding, delimiter, header and column types; read awkward fields as text. Land raw: store exactly what arrived, plus file name and load date. Type in staging: explicit date formats, remove separators, TRY_CAST, and set aside failures. Reconcile: records in the file equal rows loaded, rejected rows listed, totals compared with the sender's. Alert or proceed: a person is told about rejects before anything downstream runs.](figures/fig45-3-reliable-file-loading.svg)

*Figure 45.3 — A reliable file load, step by step. Every step either proves something or records something.*

1. **Receive:** check the file name matches the expected pattern and date; hash it; skip exact repeats; record it in the load log once it has loaded.
2. **Read with declared settings:** encoding, delimiter, quote character, header, and column names and types. Don't rely on guessing in a scheduled load.
3. **Land raw:** keep the original values, plus the file name and load date on every row, so any number can be traced back to its file.
4. **Type in staging:** explicit date formats, clean separators, `TRY_CAST`, and a list of values that failed.
5. **Reconcile:** records in the file against rows loaded; rejected rows listed; totals checked against any control total the sender provides.
6. **Alert or proceed:** if anything was rejected or doesn't reconcile, tell a person before reports and emails run. Chapter 46 wires this into a pipeline.

### Parquet: when files are designed for data

Chapter 2 introduced **Parquet**, a columnar file format that stores types, compresses well, and reads fast. Once a file has been cleaned, writing it as Parquet keeps its types for every later reader:

```python
wh.execute("COPY staging.dispatch TO 'warehouse/dispatch_2026-01-02.parquet' "
           "(FORMAT parquet)")
for row in wh.execute(
        "DESCRIBE SELECT * FROM 'warehouse/dispatch_2026-01-02.parquet'").fetchall():
    print(row[:2])
print("bytes: csv =", os.path.getsize("exports/dispatch_2026-01-02.csv"),
      " parquet =", os.path.getsize("warehouse/dispatch_2026-01-02.parquet"))
```

```
('dispatch_id', 'VARCHAR')
('order_id', 'INTEGER')
('dispatch_date', 'DATE')
('warehouse', 'VARCHAR')
('qty_units', 'INTEGER')
('remarks', 'VARCHAR')
bytes: csv = 374  parquet = 1208
```

- **`COPY table TO 'file' (FORMAT parquet)`** writes a table to a Parquet file.
- `SELECT * FROM 'file.parquet'` reads it straight back; `DESCRIBE` shows the types it stored.
- `os.path.getsize()` gives a file's size in bytes.

**Reading it.** The Parquet file carries its types with it: `dispatch_date` is a DATE and `qty_units` an INTEGER, so no later reader has to guess. For this five-row file, Parquet is *larger* than the CSV, because it stores metadata and structure that only pays off with more data, just as Chapter 2 found for four orders. Chapter 49 measures large files, where Parquet is far smaller and faster than CSV. Choose Parquet for data at scale and for types; don't expect it to shrink a tiny file.

> **Dialect note: other tools.** The same ideas apply in other tools, with different syntax. In pandas, pass `dtype=`, `parse_dates=` with `dayfirst=True`, and `thousands=","` to `read_csv`. In PostgreSQL, `COPY ... FROM ... WITH (FORMAT csv, HEADER true)` loads into a table whose types you've declared, and rejects the whole file on the first bad value, so load into a text-typed raw table first.

---

## 45.8 When the source changes shape

A **schema** is the structure of a dataset: its column names, types, and order. A **schema change** (or **schema drift**) is when a source changes that structure: a column is added, removed, renamed, or changes type.

On 5 January, Bhiwandi Main started recording which truck carried each dispatch, and someone tidied up a column name. The new file begins:

```text
dispatch_id,order_id,dispatch_date,warehouse,units,remarks,vehicle_no
```

Compare its columns with what the load expects, before loading anything:

```python
EXPECTED = ["dispatch_id", "order_id", "dispatch_date", "warehouse", "qty_units", "remarks"]
new_cols = [r[0] for r in wh.execute(
    "DESCRIBE SELECT * FROM "
    "read_csv('exports/dispatch_2026-01-05.csv', all_varchar = true)").fetchall()]
print("missing columns:", [c for c in EXPECTED if c not in new_cols])
print("new columns    :", [c for c in new_cols if c not in EXPECTED])
```

```
missing columns: ['qty_units']
new columns    : ['units', 'vehicle_no']
```

- **`all_varchar = true`** reads every column as text, so the check looks only at names and never fails on a value.
- `[r[0] for r in ...]` keeps each column's name from `DESCRIBE`.
- The two list comprehensions find expected columns that are missing, and columns that are new.

**Reading it.** One expected column is missing (`qty_units`), and two new ones appeared (`units` and `vehicle_no`). Matching columns by *position* happens to work today, because `units` sits where `qty_units` was. But the extra seventh column makes DuckDB's declared-columns read stop with a confusing "sniffing" error, not a clear message. And the next time someone inserts a column before `units`, a positional load would put `remarks` where quantities belong. Matching by name finds no `qty_units` at all. The column check turns all of these into one clear message, before loading.

### How to handle schema changes

Different changes deserve different responses.

| Change | Usually safe? | Sensible response |
|---|---|---|
| **New column added** | Yes, if you match columns by name | Load known columns; log the new one; add it to raw when someone confirms what it means |
| **Column removed** | No | Stop the load and alert; downstream reports depend on it |
| **Column renamed** | No, because it looks like one removed and one added | Stop and alert; map the new name only after confirming it means the same thing |
| **Type changed** (number becomes text) | No | Raw keeps text, so it loads; staging's rejected-values check will catch it; alert |
| **Column order changed** | Yes, if you match by name | Always match by name, never by position |

Here, the right response is to **stop**, tell the warehouse team and the pipeline's owner, confirm that `units` means the same as `qty_units`, add the mapping, and add `vehicle_no` to the raw table. That conversation is part of a **data contract**: an agreement with a source's owner about what they'll send and how they'll warn you before changing it. Chapter 47 covers data contracts in practice.

> **Real-life example: the tidy-up that cost a week.** A common story in data teams: someone renames a spreadsheet column to make it clearer, a nightly load keeps "succeeding", and a dashboard shows zero sales for a region for several days before anyone asks why. The fix takes minutes. Finding it takes days, because nothing failed. A column check like the one above turns that into an alert on the first night.

---

## 45.9 Pulling data from APIs

Chapter 2 introduced APIs and Chapter 18 called one from Python. Ingesting from an API adds four practical problems: **authentication**, **pagination**, **rate limits**, and **transient failures**, the temporary kind that may succeed if you try again.

Riverstone's CRM exposes its leads through a REST API. The companion's `mock_crm_api.py` behaves like a typical one: it needs a token, returns at most 20 leads per request, and, like real APIs under load, sometimes answers "too many requests".

Chapter 29 built `CrmClient`, a class with the same retry, backoff, and pagination logic, for a practice API with a different key header and page format. We write the loop out again here so every line is visible. In your project, you can adapt `CrmClient` to this API instead.

Start the practice API, and set up the token:

```python
from mock_crm_api import start_server
server = start_server()
BASE = "http://127.0.0.1:8045/api/leads"
TOKEN = os.environ.get("CRM_API_TOKEN", "practice-token-45")   # practice default only
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
print(server.server_address)
```

```
('127.0.0.1', 8045)
```

- `start_server()` starts the practice API in the background of the notebook, at port 8045 on this computer; `server_address` confirms where. Against a real CRM, you'd skip this and use its address.
- `HEADERS` carries the **token** that proves who you are. **Bearer** is the standard word for "whoever holds this token". Real tokens are secrets: never write them into code or commit them to Git. The token is read from the environment variable `CRM_API_TOKEN`, which you'd put in `.env` as in Chapter 18. The default after it is the practice API's public token, and exists only so this notebook runs without one; Chapters 52 and 64 cover secrets in production.

The function that makes one request, and retries only what might succeed next time:

```python
RETRY_STATUSES = {429, 503}

def get_with_retry(url, params, max_attempts=4):
    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        except (requests.Timeout, requests.ConnectionError) as e:
            problem, wait = type(e).__name__, 2 ** (attempt - 1)
        else:
            if resp.status_code not in RETRY_STATUSES:
                resp.raise_for_status()
                return resp.json()
            problem = f"{resp.status_code} {resp.reason}"
            wait = int(resp.headers.get("Retry-After", 2 ** (attempt - 1)))
        if attempt == max_attempts:
            break
        print(f"  page {params['page']}: {problem}, waiting {wait}s (attempt {attempt})")
        time.sleep(wait)
    raise RuntimeError(f"gave up after {max_attempts} attempts (last: {problem})")
```

**How it works, line by line.**

- `timeout=10` stops a request waiting forever for an answer: after 10 seconds it raises `requests.Timeout`.
- **`except (requests.Timeout, requests.ConnectionError)`** catches a timeout or a dropped connection. Both are worth another try; `type(e).__name__` is the error's name, for the message.
- **`else:`** runs only when the request didn't raise. A status outside `RETRY_STATUSES` is final: `raise_for_status()` turns an error such as 401, 404, or 500 into an exception, so a failure is never mistaken for empty data, and a success returns the JSON.
- **429 Too Many Requests** and **503 Service Unavailable** are temporary. `resp.reason` is the status's name. If the server sends a **`Retry-After`** header, the wait is that many seconds; otherwise it's `2 ** (attempt - 1)`: 1, 2, then 4 seconds. Waits that double each time are called **exponential backoff**.
- **`max_attempts=4`** is the number of tries in all, including the first. On the last attempt there's no point waiting, so `break` leaves the loop, and the function raises a clear error.

Some APIs send `Retry-After` as a date instead of a number of seconds, and `int()` would fail on it. Production code handles both; the `tenacity` package does this for you.

Now follow the pages:

```python
leads, page = [], 1
while page is not None:
    body = get_with_retry(BASE, {"page": page, "page_size": 20})
    print(f"  page {page}: {len(body['data'])} leads")
    leads.extend(body["data"])
    page = body["next_page"]
print("leads fetched:", len(leads))
```

```
  page 1: 20 leads
  page 2: 429 Too Many Requests, waiting 1s (attempt 1)
  page 2: 20 leads
  page 3: 3 leads
leads fetched: 43
```

- The `while` loop follows **pagination**: it asks for page 1, then whatever `next_page` the API returns, until `next_page` is empty (`None`).
- `leads.extend(...)` adds the page's leads to the list.

**Reading it.** The API returned 20, 20, and 3 leads. Page 2 was rate limited once; the code waited and retried, and nothing was lost. That's 43 leads in total.

### What happens without a token

```python
resp = requests.get(BASE, params={"page": 1}, timeout=10)
print(resp.status_code, resp.json())
```

```
401 {'error': 'missing or invalid token'}
```

A **401 Unauthorized** response means the token is missing, wrong, or expired. Retrying won't help, which is why `get_with_retry()` doesn't retry it. The rule: **retry what might succeed next time** (429, 503, timeouts, and dropped connections; a 500 at most once or twice), and **fail fast on other 4xx errors** (400, 401, 403, 404).

### Load and reconcile

```python
wh.execute("""
    CREATE OR REPLACE TABLE raw.crm_leads (
        lead_id      INTEGER PRIMARY KEY,
        created_at   TIMESTAMP,
        company_name VARCHAR,
        email        VARCHAR,
        source       VARCHAR,
        owner_id     INTEGER,
        loaded_for   DATE)""")
wh.executemany("INSERT INTO raw.crm_leads VALUES (?, ?, ?, ?, ?, ?, DATE '2026-01-05')",
               [(lead["lead_id"], lead["created_at"], lead["company_name"], lead["email"],
                 lead["source"], lead["owner_id"])
                for lead in leads])
cols, count_rows = fetch_rows("SELECT COUNT(*) FROM leads")
src_count = count_rows[0][0]   # first row, first column
wh_count = wh.execute("SELECT COUNT(*) FROM raw.crm_leads").fetchone()[0]
print("source:", src_count, " warehouse:", wh_count, " match:", src_count == wh_count)
server.shutdown()
```

```
source: 43  warehouse: 43  match: True
```

- `raw.crm_leads` declares the API's six fields with their types, plus `loaded_for`, and `lead_id` as its primary key.
- Each lead is a dictionary from the API's JSON; the list comprehension turns each one into a tuple in the table's column order. `DATE '2026-01-05'` fills `loaded_for`, the day this load is for.
- `count_rows[0][0]` is the first column of the first row: the count.
- `server.shutdown()` stops the practice API. (The CDC connection was closed at the end of section 45.6.)

All 43 leads arrived. Against a real CRM you usually can't count the source directly; instead, compare with the total the API reports (many APIs return one), or with a count exported from the CRM's own screen.

> **Watch out: offset pagination and moving data.** This API pages by position ("records 21–40"). If a lead is added or removed while you're reading, every later record shifts by one, and you can skip or repeat a record. For data that changes during the read, prefer APIs that page with a **cursor** (a token pointing at the next record) or filter by a stable key or timestamp, and always reconcile the final count.

### API ingestion checklist

- Keep **credentials** out of code; rotate them; use the least access the load needs.
- Always set **timeouts**.
- **Retry** 429, 503, timeouts, and dropped connections with increasing waits, respecting `Retry-After`; a 500 at most once or twice; fail fast on other 4xx errors (400, 401, 403, 404).
- Follow **pagination** to the end, and prefer cursor pagination for changing data.
- Ask for **only what changed** when the API supports it (for example `updated_since=`), with a look-back window.
- Land the **raw response** (or its fields) with a load date, so you can re-process without calling the API again.
- **Reconcile** against a total from the source.
- Respect the provider's **limits and terms**. Some APIs charge per call or suspend keys that exceed limits.

---

## 45.10 Build or buy: connectors versus custom code

Everything in this chapter so far was custom code. In practice, many companies don't write ingestion for common tools at all. They use **managed connectors**: services and open-source tools that already know how to extract data from hundreds of popular databases and SaaS products, handle pagination, schema changes, and CDC, and load into a warehouse. Well-known examples include Fivetran and Airbyte, and cloud providers offer their own.

| Question | Leans toward a managed connector | Leans toward custom code |
|---|---|---|
| Is the source a popular product with a maintained connector? | Yes | No, or the connector lacks what you need |
| How much engineering time do you have? | Little | Enough to build *and* maintain |
| How much data, and how does the tool charge? | Moderate volumes where pricing is affordable | Very high volumes where per-row pricing becomes expensive |
| How unusual is the source? | Standard APIs and databases | Custom files, older systems, internal tools, odd formats |
| Where can the data go? | Allowed to pass through a vendor's service | Must stay inside your network or country |
| Who fixes it when it breaks? | The vendor, for connector bugs | You |

The honest summary: **buying saves building, not owning.** A connector still needs someone to choose what to sync, watch costs, reconcile results, and respond when a source changes. And custom code is rarely "free": the first version takes days; keeping it working as sources change takes years.

For Riverstone, a reasonable split would be a managed connector for the CRM if a maintained one exists for its product, CDC or scheduled queries for the ERP, and custom loading for the warehouse's dispatch sheet, which no vendor will ever have a connector for.

> **Interview extra point.** When asked "how would you ingest data from X?", don't start with a tool. Ask three questions first: how big is it, how does it change (append-only, updates, deletes), and how fresh does it need to be? Then choose full, incremental, hash, or CDC, and say how you'd reconcile it. Chapter 77 has data engineering system design questions that use exactly this structure.

---

## 45.11 Web data: legal and ethical limits

Sometimes the data a business wants isn't in any of its systems: competitors' published prices, public tender notices, product reviews. Collecting data from websites automatically is **web scraping**. It can be legitimate, and it has real limits.

Before collecting any web data, check these, in order.

1. **Is there an official way?** An API, a data download, or a licensed data feed is almost always better: more reliable, and clearly permitted.
2. **What do the site's terms of use say?** Many sites prohibit automated collection. Breaking terms of use can have legal consequences, and it can get your company's network blocked.
3. **What does `robots.txt` say?** Most sites publish a file at `/robots.txt` saying which parts automated tools may visit. Respecting it is the minimum standard of good behavior.
4. **Does the data include personal information?** Names, phone numbers, email addresses, and profile details are personal data. Data protection laws, including India's Digital Personal Data Protection Act, 2023, and the EU's GDPR, apply to collecting and using personal data even when it's publicly visible. Treat personal data as off-limits unless your legal or compliance team has confirmed a lawful basis.
5. **Is the content protected by copyright?** Reviews, articles, images, and databases can be. Collecting facts is different from copying creative content.
6. **Will your collection harm the site?** Send requests slowly, identify your tool truthfully, and never try to get around logins, paywalls, or blocking measures.

When in doubt, ask your company's legal or compliance team before collecting anything. This section is general guidance, not legal advice; laws differ between countries and change over time. Chapter 64 covers privacy and data governance in depth.

> **Watch out: "it's public" is not permission.** Being visible in a browser doesn't make data free to collect, store, and reuse. The questions above apply to public pages too.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Judging a load by whether it finished | Dashboards drift from the source; nobody knows since when | Reconcile counts and totals against the source after every load (45.3) |
| Incremental load by ID on rows that get updated | Status counts differ from the source; cancelled orders still open (45.4) | Use `updated_at` with a look-back, hash comparison, or CDC |
| Trusting `updated_at` without checking it | Occasional missing changes, especially after bulk fixes | Test it against a hash comparison before relying on it |
| Forgetting deletes | Rows deleted in the source live forever in the warehouse | Full load, hash comparison, or CDC; or a source "deleted" flag |
| Plain `INSERT` in a re-runnable load | Duplicate rows after a retry | Primary keys in raw, and upserts (45.5) |
| Building hash strings differently on each side | Every row looks changed | Same columns, order, separator, and date format on both sides |
| NULLs dropped from the hash string | A change to or from NULL goes unnoticed | Wrap nullable columns in `coalesce(... , '∅')` on both sides (45.5) |
| Recording a file as loaded before loading it | A failed load is skipped forever as "already loaded" | Record in the load log only after the load succeeds (45.5) |
| Leaving a CDC slot unconsumed | Source database disk fills; the ERP stops | Monitor slot lag; drop unused slots (45.6) |
| Letting a reader guess column types in a daily load | Columns switch between number and text from day to day | Declare columns; type in staging (45.7) |
| Parsing dates without an explicit format | 2 January loaded as 1 February | `strptime` with the source's exact format |
| `CAST` on messy values | One bad value stops the whole load | `TRY_CAST`, and list the failures |
| Matching file columns by position | Values land in the wrong columns after a change | Match by name; check expected columns first (45.8) |
| Retrying every error | Endless retries on a bad token; accounts locked | Retry 429, 503, and timeouts; fail fast on other 4xx errors (400, 401, 403, 404) |
| No timeout on API calls | A load hangs all night | Always set a timeout |
| Tokens in code | A secret leaks through Git | Environment variables or a secrets manager |
| Scraping without checking terms or personal data | Legal risk, blocked networks | Official sources first; check terms, robots.txt, privacy law (45.11) |

---

## In the real world: the orders that never cancelled

Riverstone's first proper data pipeline went live in February, built by a data engineer the company had hired on contract, with Meera as the business owner. Every night it loaded new orders from the ERP into the warehouse, and every morning the Daily Sales Flash came from the warehouse instead of from Meera's spreadsheet. It was fast, it never failed, and for three weeks everyone was pleased.

Then Vikram brought a printout to the Monday sales review. "The Flash says we have eleven open orders for Green Leaf Hotels. Their buyer told me on Friday they cancelled six of those in January."

Meera opened the ERP. The six orders were marked Cancelled. She opened the warehouse. The same six orders said Pending.

She'd read enough about ingestion to guess the cause before she found it. The pipeline loaded orders with an ID higher than the last one it had seen. Cancelling an order changes its status, not its ID. Every cancellation, every delivery, every correction made to an existing order after its first night had never reached the warehouse.

"How many orders are wrong?" Anita asked.

"I don't know yet," Meera said. "That's the worse problem. Nothing told us."

That afternoon, the engineer and Meera did three things. First, they measured the damage: a hash comparison across every order since the pipeline started. It found 214 orders whose status in the warehouse didn't match the ERP. (This was the real ERP, which takes about 4,000 orders a month, not the 175-order practice copy you've been using.) Second, they fixed the data, with an upsert of every changed row, and re-ran the Flash for the affected days, so the sales team had correct history. Third, they fixed the design. The ERP had no reliable last-updated column, so the engineer set up a nightly hash comparison over the last 90 days of orders, plus a full comparison every Sunday, and added a reconciliation check: order counts by status in the warehouse must match the ERP before the Flash is sent.

The check failed once more, two weeks later, when someone corrected a batch of orders from the previous quarter, outside the 90-day window. This time nothing reached the sales team. The Flash was held, an alert went to Meera at 6:10 a.m., the Sunday full comparison was run early, and the Flash went out at 7:30 with the right numbers.

At the monthly review, Anita asked the question Meera had been expecting. "Why didn't the pipeline do this from the start?"

"Because it looked like it worked," Meera said. "It loaded exactly what it was built to load. We built it to load the wrong thing, and never checked it against the ERP."

**What made this work.**

- **Meera recognized the pattern:** a load that never fails, with numbers that drift, points to what the load isn't reading.
- **They measured before fixing:** the hash comparison showed the full size of the problem, not only the six orders someone happened to notice.
- **They fixed data, design, and detection:** corrected history, a change-detection method that catches updates, and a reconciliation check that stops bad numbers before they're sent.
- **The check proved its value** the next time something changed outside the plan.

---

## Project: incremental ingestion for Riverstone

**Goal:** a small, re-runnable ingestion job that loads Riverstone orders, order lines, CRM leads, and dispatch files into the warehouse, detects changes correctly, and proves every load with a reconciliation report. Chapter 46 turns it into an orchestrated pipeline, and Chapter 47 adds quality checks and freshness alerts.

### Tools you'll need

- **PostgreSQL 16**, with `wal_level = logical` for section 45.6. On a company database, ask the administrator; don't change it yourself.
- **Python** in the book's virtual environment (Chapter 17), with `psycopg2` (PostgreSQL driver) and `duckdb` (local analytical database), installed in section 45.2 with `python -m pip install psycopg2-binary==2.9.13 duckdb==1.5.6`, and `requests` and `python-dotenv` from Chapter 18.
- **The Chapter 45 companion folder** (`companion/ch45/`): `reset_ch45.py`, `apply_day.py`, `mock_crm_api.py`, `make_files.py`, copied to `work/ch45`. Run the notebook from that folder. If your PostgreSQL needs a user or password, put the connection string in `work/ch45/.env` as `RIVERSTONE_SOURCE=dbname=riverstone_source user=postgres password=your-password host=localhost` (section 45.2). The notebook, `reset()`, `apply_day()`, and the practice API all read it.
- **Versions used for the outputs shown:** Python 3.11.15, DuckDB 1.5.6, psycopg2 2.9.13, requests 2.33.1, python-dotenv 1.2.3, PostgreSQL 16.13.
- **Worth knowing about, not needed here:** Debezium for production CDC; managed connectors such as Fivetran and Airbyte; `dlt` and Singer-style tools for writing connectors in Python.

**Option A: Riverstone.** Use the companion environment.

**Option B: your own data.** Use a database, API, or regular file you have permission to read. Don't use production systems for practice without your administrator's agreement, and keep credentials out of anything you share.

**Steps**

1. **Plan the sources.** For each of `orders`, `order_items`, `customers`, `products`, CRM leads, and dispatch files, write down: source type, system of record, size, whether rows are updated or deleted, and your chosen strategy (full, incremental, hash, CDC) with one sentence of reasoning.
2. **Create the raw tables** in the warehouse with declared types and primary keys, plus `loaded_at_run` (a run ID) on every table.
3. **Build a load log table:** run ID, source, strategy, rows read, rows inserted, rows updated, rows rejected, reconciliation result.
4. **Full loads** for `customers` and `products`.
5. **Change detection for `orders` and `order_items`,** using hash comparison or CDC, applied with upserts.
6. **The CRM leads API,** with authentication from `.env`, pagination, retries on 429, 503, and timeouts, and a final count check.
7. **Dispatch files,** with file hashing, declared columns, typed staging, a rejected-rows list, and a column check that stops the load on missing or renamed columns.
8. **A reconciliation report,** printed at the end of every run: for each source, rows in the source (or file), rows in the warehouse, and order counts by status. Mark any mismatch clearly.
9. **Test it:** run `reset()`, run your job, `apply_day(1)`, run it again, `apply_day(2)`, run it again, then run it a fourth time with no changes. The reconciliation report must match the source every time, and the fourth run must change nothing.
10. **Break it on purpose:** load `dispatch_2026-01-05.csv` and confirm your column check stops it with a clear message.

**Stretch goals**

- Replace the hash comparison for orders with the CDC slot, applying each change with an upsert.
- Add a deleted order to `apply_day` (in your own copy) and show which strategies notice it.
- Add a look-back window to an `updated_at`-style incremental load of lead stage history, and show it handles a late change.

---

## Recap

- **Ingestion** moves data from source systems into the warehouse. Its dangerous failures are loads that succeed with wrong data.
- Sources include **databases**, **files**, **APIs**, **events**, and **SaaS tools**; the **system of record** is the source that's officially correct.
- Data lands in a **raw** layer as it arrived, then a typed **staging** layer, then **modeled** tables.
- A **full load** replaces everything: simple, self-correcting, and sees updates and deletes. It stops being practical for large or busy tables.
- An **incremental load** uses a **watermark**. By ID it misses **updates** and **deletes**; `updated_at` helps, with a **look-back** window, if it's trustworthy.
- A **hash** is a fixed-length fingerprint of any data: the same data always gives the same fingerprint, and the smallest change gives a completely different one. **SHA-256** gives 64 hex characters; **MD5** gives 32 and is fine for change detection, not for security.
- **Row hashes** detect inserts, updates, and deletes without help from the source, at the cost of scanning keys; wrap nullable columns so NULLs aren't dropped. **File hashes** skip content already loaded, recorded in a load log only after a successful load.
- **Upserts** make loads **idempotent**: safe to run again.
- **Change data capture** reads the database's **write-ahead log** through a **replication slot**: every change, in order, without scanning. Unconsumed slots fill disks.
- **Reliable file loads** declare columns, keep raw text, type in staging with explicit formats and `TRY_CAST`, list rejects, and **reconcile** against the file.
- **Schema changes** should be detected before loading; match columns **by name**, and stop on removed or renamed columns.
- **API ingestion** needs secure **authentication**, **timeouts**, **pagination**, and **retries** only for temporary failures: 429, 503, and timeouts.
- **Managed connectors** save building, not owning.
- **Web data** needs an official source where possible, and checks on terms, robots.txt, personal data, and copyright.

---

## Key terms

ingestion · source system · system of record · raw layer · staging layer · modeled layer · DuckDB · full load · reconciliation check · incremental load · watermark · last-updated timestamp · look-back window · hash (row hash, file hash) · SHA-256 · MD5 · checksum · hexdigest · connection string · cursor · upsert · idempotent · load log · write-ahead log (WAL) · change data capture (CDC) · replication slot · slot lag · byte-order mark (BOM) · declared columns · `TRY_CAST` · rejected rows · Parquet · schema · schema change (schema drift) · data contract · authentication token · pagination (offset, cursor) · rate limit (429) · `Retry-After` · exponential backoff · timeout · managed connector · web scraping · `robots.txt` · personal data

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can name the main kinds of source system and one typical difficulty of each.
- [ ] You can explain raw, staging, and modeled layers, and why raw keeps data as it arrived.
- [ ] You can write a full load with declared types and reconcile it by count and by category.
- [ ] You can explain, and demonstrate, why an incremental load by ID misses updates and deletes.
- [ ] You can list three ways an `updated_at` watermark can still miss changes.
- [ ] You can compute a SHA-256 fingerprint in Python and explain why a one-character change alters all of it.
- [ ] You can detect inserted, changed, and deleted rows with row hashes, and explain why both sides must build the string identically.
- [ ] You can explain idempotency and show that an upsert can be safely re-run.
- [ ] You can skip already-loaded files with a file hash, and say when that would be wrong.
- [ ] You can explain change data capture, replication slots, and the risk of an abandoned slot.
- [ ] You can choose between full, incremental, hash, and CDC for a given table, with reasons.
- [ ] You can load a messy CSV with declared columns, explicit date formats, `TRY_CAST`, and a rejected-rows list, and reconcile it against the file.
- [ ] You can detect a schema change before loading and choose the right response.
- [ ] You can ingest from a paginated, authenticated, rate-limited API with retries and timeouts.
- [ ] You can argue build versus buy for a given source.
- [ ] You can list the checks to make before collecting web data.

---

## Exercises

Run `reset()` before each exercise that uses the companion environment, unless it says otherwise.

### Warm-up

1. For each Riverstone table or source, choose a loading strategy (full, incremental by ID, incremental by timestamp, hash comparison, or CDC) and give one reason: (a) `products`; (b) website enquiry events that are only ever added; (c) `orders`, which are updated but have no `updated_at`; (d) the CRM's lead stage history, where every stage change adds a row with a timestamp.
2. Which HTTP status codes should an ingestion job retry, and which should make it fail immediately? Classify: 200, 401, 404, 429, 500, 503, and a timeout.
3. Explain in two sentences why `concat_ws('|', ...)` uses a separator when building a row hash.
4. Hash `Pay Rs 14,700 to Riverstone Supplies` with SHA-256, with and without a space at the end. How many of the 64 characters of the two fingerprints match, position by position? Is that what you expected?

### Core

5. After `reset()` and a full load of orders, run `apply_day(1)` and then `apply_day(2)` *without loading in between*. Using the hash comparison from section 45.5, which order IDs will be inserted and which changed? Explain why order 10176 appears in only one of the lists.
6. Write a function `load_orders_full()` that performs a full load of `orders` into `raw.orders` and returns the source and warehouse counts by status. Why does a full load not need a separate method for detecting updates?
7. A dispatch file has the line `D-2610,10180,13-01-2026,Bhiwandi Main,"3,150",`. What will `staging.dispatch` contain for `dispatch_date` and `qty_units`? What would happen if the date were parsed with the format `'%m-%d-%Y'`?
8. Using the reconciliation output in section 45.7, a manager asks: "What were total units dispatched on 2 January?" Write the answer you'd send, including what's missing.
9. `get_with_retry()` in section 45.9 waits 1, 2, then 4 seconds between attempts when the server sends no `Retry-After` header. Chapter 29's `CrmClient` also added a small random amount to each wait, called **jitter**. Change `get_with_retry()` so each of those waits is `2 ** (attempt - 1)` plus a random amount of up to half of that. Why is waiting longer each time better than retrying immediately, and what does the jitter add?
10. Explain why the plain `INSERT` in section 45.5 raised an error on the second run. What would have happened if `raw.orders` had no primary key?

### Stretch

11. Extend the column check from section 45.8 into a function `check_columns(path, expected)` that returns `"ok"`, `"new columns only"` (safe to load known columns), or `"stop"` (a column is missing), and a list of the differences. Run it on both dispatch files.
12. Design a strategy for an `invoices` table with 80 million rows, where invoices are sometimes corrected up to 60 days after they're raised, rows are never deleted, and there's no trustworthy `updated_at`. The ERP team won't allow CDC. Describe what you'd load nightly and weekly, and how you'd reconcile.
13. The CRM API pages by offset, and leads are added and removed while you read. Describe a sequence in which a lead is skipped, using page size 20, and propose two fixes.

### Think about it (no code needed)

14. Riverstone is choosing between a managed connector for its CRM and custom code. List three questions you'd ask before deciding, and what answer would push you each way.
15. A marketing colleague wants to collect the names and phone numbers of shop owners listed on a public business directory, to call them about Riverstone's products. What would you tell them before anything is collected?

---

## Answers

**1.** (a) **Full load**: `products` is small and changes occasionally, so reloading it is cheap and always correct. (b) **Incremental by ID or timestamp**: rows are only ever added, so a watermark can't miss updates. (c) **Hash comparison** (or CDC if the ERP team allows it): rows are updated, and there's no trustworthy column to find the changes. (d) **Incremental by timestamp** on the stage-change timestamp column (in Riverstone's `lead_stage_history` table, `entered_at`), with a look-back window: each change adds a new row with a timestamp. A full load is also reasonable for (d) at Riverstone's size.

**2.** Retry: **429** (rate limited), **503** (temporarily unavailable), and **timeouts**. **500** is borderline: retry at most once or twice, because it's sometimes temporary, then fail. Fail immediately on the other 4xx errors: **401** (authentication won't fix itself) and **404** (the address is wrong). **200** is success: no retry.

**3.** Without a separator, different rows can produce the same string: values `1` and `23` join to `123`, exactly like `12` and `3`, so a change could go unnoticed. A separator that doesn't appear in the data keeps each value's boundaries, so different rows give different strings and different hashes.

**4.** Only **2** of the 64 positions match. The fingerprints are:

```text
f4251ff3fb7191f7e79677f3b1871db06c0935c3cc08164496995f1f909f6f71   no space
71e96ba2039f8e4139716f2287b78cfe1e12842a28e6f3dfab748321bbcaa77a   one space at the end
```

That's the avalanche property: one invisible character changes the whole fingerprint. Any position has a 1 in 16 chance of matching by luck (16 possible hex characters), so about 4 matches is what chance alone gives; 2 is well within that. It's also a warning: a trailing space in a file makes it a different file to a hash.

**5.** Inserted: **10176, 10177, 10178**. Changed: **10174, 10175**. Order 10176 was created on day 1 and changed on day 2, but the warehouse never saw its first version, so it counts as new: its latest version is inserted. Hash comparison sees the *current* difference between source and warehouse, not the history of changes in between; CDC would report both the insert and the update.

**6.** A sample answer:

<!-- run: none -->

```python
def load_orders_full():
    cols, rows = fetch_rows(
        "SELECT order_id, customer_id, order_date, status, sales_rep_id FROM orders")
    wh.execute("DELETE FROM raw.orders")
    wh.executemany("INSERT INTO raw.orders VALUES (?, ?, ?, ?, ?)", rows)
    src = dict(fetch_rows("SELECT status, COUNT(*) FROM orders GROUP BY status")[1])
    tgt = dict(wh.execute(
        "SELECT status, COUNT(*) FROM raw.orders GROUP BY status").fetchall())
    return src, tgt
```

A full load replaces every row with the source's current version, so updated rows arrive in their new state and deleted rows disappear. There's nothing to detect. For a production version, wrap the delete and insert in one transaction, so readers never see an empty table.

**7.** `dispatch_date` = **2026-01-13** (13 January 2026), and `qty_units` = **3150**. With `'%m-%d-%Y'`, the parser would read month 13, which doesn't exist, so the load would fail with an error. That failure is useful: with a day of 12 or less, the wrong format would *not* fail, and would silently swap day and month.

**8.** *"Bhiwandi Main recorded five dispatches on 2 January. Four have quantities, totaling 3,425 units. The fifth, D-2603 for order 10172, has no quantity yet (marked 'awaiting count'), so the true total is 3,425 plus that dispatch. I've asked the warehouse for the count and will update the figure once it arrives."* The key points are the total, what's excluded, and that it's being followed up.

**9.** A sample answer:

<!-- run: none -->

```python
import random

def get_with_retry(url, params, max_attempts=4):
    for attempt in range(1, max_attempts + 1):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
        except (requests.Timeout, requests.ConnectionError) as e:
            problem, retry_after = type(e).__name__, None
        else:
            if resp.status_code not in RETRY_STATUSES:
                resp.raise_for_status()
                return resp.json()
            problem = f"{resp.status_code} {resp.reason}"
            retry_after = resp.headers.get("Retry-After")
        if attempt == max_attempts:
            break
        if retry_after is not None:
            wait = int(retry_after)
        else:
            base = 2 ** (attempt - 1)
            wait = base + random.uniform(0, base / 2)
        time.sleep(wait)
    raise RuntimeError(f"gave up after {max_attempts} attempts (last: {problem})")
```

Without a `Retry-After` header, the waits between the four attempts are 1, 2, and 4 seconds, each plus up to half as much again. `random.uniform(a, b)` returns a random number between `a` and `b`. There's no wait after the fourth attempt, because the function gives up then. This is **exponential backoff** with **jitter**. Retrying immediately hits a server that's already overloaded or limiting you, which usually fails again and can make things worse for everyone; waiting longer each time gives it room to recover. The jitter spreads out many clients that failed at the same moment, so they don't all retry at the same moment too.

**10.** `raw.orders` has `order_id` as its **primary key**, and orders 10176 and 10177 already existed, so inserting them again violated the key and DuckDB refused. Without a primary key, the insert would have **succeeded silently**, creating duplicate rows: order counts and revenue for those orders would be doubled in every report, with no error anywhere.

**11.** A sample answer:

<!-- run: none -->

```python
def check_columns(path, expected):
    cols = [r[0] for r in wh.execute(
        f"DESCRIBE SELECT * FROM read_csv('{path}', all_varchar = true)").fetchall()]
    missing = [c for c in expected if c not in cols]
    extra = [c for c in cols if c not in expected]
    if missing:
        return "stop", {"missing": missing, "new": extra}
    if extra:
        return "new columns only", {"new": extra}
    return "ok", {}
```

On `dispatch_2026-01-02.csv`, it returns **`ok`**. On `dispatch_2026-01-05.csv`, it returns **`stop`**, with `qty_units` missing and `units` and `vehicle_no` new. The rename is reported as one missing and one new column, which is why it must stop rather than guess.

**12.** One reasonable design: **Nightly**, compute row hashes for invoices raised in the **last 60 days** (the correction window) plus a small margin, say 70 days, compare with the warehouse, and upsert changes; load new invoices in the same step. **Weekly**, compare hashes for the whole table **in monthly chunks**: compute one hash per month (for example, a hash of the sorted row hashes) on both sides, and only compare row by row for months whose chunk hash differs. **Reconcile** every night: invoice count and total amount by month for the last 70 days, and for all months weekly. Run the heavy queries against a read replica or outside business hours, with the ERP team's agreement. Because rows are never deleted, delete detection can be weekly only. Other designs are acceptable if they cover the 60-day correction window, limit the load on the ERP, and reconcile.

**13.** The practice API has 43 leads. Suppose it lists them newest first, 20 per page. You read page 1 (positions 1–20). Before you ask for page 2, a lead in positions 1–20 is **deleted**, or merged into another. Everything after it moves up one place: the lead that was at position 21 is now at 20, and page 2 (positions 21–40) never returns it. It is **skipped**. (A new lead arriving at position 1 does the opposite: the old 20 becomes 21 and is read **twice**.) Fixes: (1) **cursor pagination**, or a stable filter such as `lead_id > last_seen_id` read in `lead_id` order, which isn't affected by changes elsewhere in the list; (2) de-duplicate by `lead_id` on load and **reconcile** the final count against the API's total, re-reading if it doesn't match.

**14.** Useful questions: (a) *Is there a maintained connector for our exact CRM product, covering the objects we need?* Yes pushes toward buying; no, or only partly, toward custom code. (b) *What will it cost at our data volume and sync frequency, and what does our engineering time cost?* Affordable pricing and little engineering time push toward buying; high per-row costs at large volumes, or spare engineering capacity, push toward building. (c) *Is our customer and lead data allowed to pass through a vendor's service, and where is it processed?* If policy or law requires it to stay inside our systems or country, that pushes toward custom code or a self-hosted tool. Other good questions: who fixes it when it breaks, how quickly it handles schema changes, and whether it supports incremental syncs.

**15.** Tell them to stop and check before collecting anything. **Names and phone numbers are personal data**, and data protection laws such as India's Digital Personal Data Protection Act, 2023, apply even when the directory is public; using them for sales calls needs a lawful basis, which the company's legal or compliance team must confirm. Check the directory's **terms of use**, which often prohibit automated collection and commercial reuse, and its `robots.txt`. Ask whether there's an **official route**: a paid listing service, a licensed data provider, or the directory's own advertising options. And note that India's rules on unsolicited commercial calls also apply. The safest recommendation is to involve legal or compliance first, and to prefer sources where shop owners have agreed to be contacted.

---

## Where this leads

- **Chapter 46, Pipelines & Orchestration,** turns this chapter's loads into a scheduled, orchestrated pipeline, with idempotency tested by a deliberate failure, backfills, alerts, and the Daily Sales Flash sent only after its data passes checks.
- **Chapter 47, Data Quality, Observability & Contracts,** turns reconciliation checks into automated tests, adds freshness monitoring, and puts data contracts like the one in section 45.8 into practice.
- **Chapter 49, Storage, Warehouses & Lakehouses,** explains how warehouses store raw and staging layers, and covers ACID transactions, partitioning, and cloud warehouse costs.
- **Chapter 50, Streaming & Real-Time,** takes change data capture from a daily read to a continuous stream.
- **Chapter 51, Data Activation,** reverses the direction: writing warehouse data back into the CRM and ERP through APIs, with the same care for idempotency, retries, and systems of record.
- **Chapter 64** covers privacy, security, and governance, including the rules behind section 45.11.
- **Part 8:** ingestion and system design questions appear in Chapter 77, and API and webhook integration questions in Chapter 78.
