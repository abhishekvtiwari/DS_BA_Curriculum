# Chapter 47. Data Quality, Observability & Contracts

*Part 5 — Data Engineering, Integration & Scale*

> **Chapter at a glance**
>
> **You will learn to:** name the dimensions of data quality and write a test for each · build a small test framework where every test is a query that returns the rows that break a rule · choose severities so that only real problems stop a pipeline · use write–audit–publish so bad data never reaches the tables people read · monitor freshness and volume, and spot unusual days against history · trace lineage to see which reports a broken table affects · write a data contract with a source owner and check it automatically · run a data incident: severity, communication, fix, and review · keep alerts few enough that people still read them · run the same rules in dbt, Great Expectations, and Soda, and know where observability platforms fit.
>
> **Before you start:** Chapter 45 (ingestion and reconciliation), Chapter 46 (the orchestrated pipeline), Chapter 32 (dbt), and Chapter 14 (finding and fixing data problems as an analyst).
>
> **Time needed:** 14–18 hours of reading and practice, spread over two to three weeks, in four sittings: sections 47.1–47.3; section 47.4; sections 47.5–47.7; sections 47.8–47.10 and the project.
>
> **Tools:** Python 3.14 in the virtual environment from Chapter 17, with `duckdb` and `psycopg2` (installed in Chapter 45, section 45.2); PostgreSQL 16; Jupyter; and the Chapter 47 companion folder. Section 47.10 adds two optional libraries, `great_expectations` and `soda-duckdb`. Everything runs on your own computer. No data quality product is needed for the main thread: the tests are SQL.
>
> **Practice data:** the Chapter 45 and 46 environment: `riverstone_source` (the ERP), the dispatch files, and the warehouse you've been building.

---

## Why this matters

Chapter 1 told you that analysts check data before they trust it, and promised that Chapter 47 would show how data teams do that automatically. Chapter 13 built the habit of reconciling every number against a source. Chapter 46 added one check to a pipeline and used it to stop a wrong report from being sent.

This chapter turns those habits into a system, because as soon as more than one person depends on the data, checking by hand stops working. Somebody is on leave. Somebody assumes somebody else looked. And the failures that matter most are the quiet ones: a load that brings in nothing, a status nobody agreed to, a file that's three days old, a column renamed by a helpful colleague.

There's also a gap left over from Chapter 46. When the check failed on 5 January, the report wasn't sent, which was right. But the wrong row was still sitting in the table, visible to anyone who queried it. This chapter closes that gap, and adds the monitoring, lineage, contracts, and incident habits that make a data platform something people trust.

---

## In plain English

Think about a factory's quality department, because Riverstone has one.

- **Specifications** say what "good" means: this crate weighs between 4.8 and 5.2 kg, this lid fits this base. Data has specifications too, and writing them down is most of the work.
- **Checks on the line** catch problems while the product is being made, not after it ships. That's **testing data inside the pipeline**.
- **Quarantine** holds a doubtful batch until someone inspects it. Nothing doubtful goes to customers. That's **write–audit–publish**.
- **A goods-inward check** confirms what arrived from a supplier matches what was agreed. That's a **data contract**.
- **A gauge that hasn't moved in three days** is more worrying than a gauge reading badly, because nobody noticed. That's **freshness monitoring**.
- **Batch tracing** tells you which customers got product from a faulty batch. That's **lineage**.
- **An alarm that rings all day** gets switched off, and then nobody hears the real one. That's **alert fatigue**.

A data team is the quality department for the numbers. This chapter is its handbook.

---

## 47.1 The dimensions of data quality

"Quality" is too vague to test. Break it into dimensions, and each one becomes a rule you can write in SQL.

| Dimension | The question it answers | Riverstone example | Typical test |
|---|---|---|---|
| **Accuracy** | Do the numbers match reality, or a trusted source? | Warehouse revenue for a day equals the ERP's | Reconciliation against the source |
| **Completeness** | Is anything missing? | Every order has at least one order line; every order has a customer | Missing values; counts against the source |
| **Validity** | Does each value follow its rules? | `status` is one of Pending, Shipped, Delivered, Cancelled; quantities are positive | Accepted values; ranges |
| **Uniqueness** | Is anything counted twice? | One row per order in `raw.orders`; one Flash row per day | Duplicate key tests |
| **Consistency** | Do related things agree? | Every order line points at an order that exists; dispatch rows point at known orders | Relationship tests across tables |
| **Timeliness** | Is it here, and recent enough? | Yesterday's orders are loaded by 6:30 a.m.; the dispatch file arrived last night | Freshness checks |

Two more properties matter and aren't tested the same way. **Usability** is whether people can find and understand the data: names, definitions, and documentation (Chapter 32 and Chapter 64). **Trust** is whether they believe it, which is earned by the other dimensions holding for months.

> **Simplification note.** Different books and tools name these slightly differently, and some add dimensions such as integrity or conformity. The names matter less than the habit: for every important table, write down what "good" means, then test it.

---

## 47.2 Testing data inside the pipeline

A **data test** is a rule about data, expressed so a computer can judge it. The most useful way to write one is this:

> **Write a query that returns the rows that break the rule. If it returns no rows, the test passes.**

That single idea covers almost everything: duplicates, missing values, invalid values, broken relationships, and totals that don't match a source. It also gives you something valuable when a test fails: the offending rows, which is where investigation starts. It's also how dbt's tests work underneath (Chapter 32): each one compiles to exactly this kind of query.

### Severity: stop, or warn?

Not every problem should stop a pipeline at 6:30 a.m. Each test gets a **severity**, and this chapter's code writes it as one of two strings, `"error"` or `"warn"`:

- **Error** (`"error"`): the data is wrong in a way that would mislead someone. Stop, and don't publish. Example: the warehouse's revenue doesn't match the ERP.
- **Warning** (`"warn"`): something is odd and worth a look, but publishing is still better than not publishing. Example: one dispatch row points at an order the warehouse doesn't have yet.

Start strict on the numbers people act on, and lenient on the edges. A test whose failures are routinely ignored should either be fixed, downgraded to a warning, or deleted. Tests nobody acts on are worse than no tests, because they train people to ignore red.

### Where checks belong

| Layer | What to test | Why here |
|---|---|---|
| **Raw** | Structure and load completeness: expected columns, row counts against the source, keys unique | Catches ingestion problems before anything is built on them |
| **Staging** | Validity and consistency: types converted, accepted values, relationships between tables | Catches source data problems and conversion mistakes |
| **Mart** | Business rules and reconciliation: one row per day, totals match the source, no negative revenue | Catches modeling mistakes, and protects the numbers people read |
| **Before delivery** | The blocking checks from Chapter 46 | Nothing wrong leaves the platform |

---

## 47.3 A check library for Riverstone

### Setting up

The companion folder `companion/ch47/` is the Chapter 46 environment without Dagster. This chapter doesn't need the orchestrator, only the functions its steps call:

| File | What it does |
|---|---|
| `reset_ch47.py` | Recreates `riverstone_source` from `riverstone_2025`, and empties the warehouse, `exports`, `outbox`, and `alerts` folders, then writes the two dispatch files again |
| `ingest.py` | Chapter 46's packaged loads (section 46.3): `fetch_rows()` (run a query on the ERP), `sync_table()` (hash comparison and upsert), `load_dispatch()` (with a column check) |
| `apply_day.py`, `make_files.py`, `mock_crm_api.py` | Copied from Chapter 45 |

Before you start, make sure PostgreSQL is running and `riverstone_2025` is loaded (Chapter 45, section 45.2), and activate the book's virtual environment. Then open a Jupyter notebook in `companion/ch47/` (Chapter 17, section 17.0), and run each code block in this chapter as its own cell, top to bottom, without restarting the kernel. Later cells use names that earlier cells create, such as `wh`, `run_tests`, and `TESTS`.

The first cell resets the practice environment and opens the warehouse:

```python
import duckdb
from reset_ch47 import reset
import ingest

reset()
wh = duckdb.connect("warehouse/riverstone_wh.duckdb")
print("ERP orders after reset:", ingest.fetch_rows("SELECT COUNT(*) FROM orders")[0][0])
```

```
ERP orders after reset: 175
```

**How it works.**

- `from reset_ch47 import reset` and `import ingest` load two of the companion files as modules (Chapter 29, section 29.2).
- `reset()` puts everything back to the start: a fresh copy of the ERP, an empty warehouse, and the two dispatch files. Run this cell again whenever you want to start over.
- `duckdb.connect()` opens the warehouse file, as in Chapter 45. `wh` is the connection every later cell uses.
- `ingest.fetch_rows(sql)` runs a query on the ERP and returns its rows as a list of tuples. `[0][0]` takes the first value of the first row. 175 orders is the one-year database, before any of the January business days.

If this cell fails with a connection error, PostgreSQL isn't running, or `riverstone_2025` isn't loaded.

Next, replay the 2 January business day from Chapter 46 and load it:

```python
from apply_day import apply_day

apply_day(1)                                  # the 2 January business day (Chapter 45)
for table in ["orders", "order_items"]:
    ingest.sync_table(wh, table)
print("dispatch:", ingest.load_dispatch(wh, "2026-01-02"))
```

```
dispatch: 5 rows (the day's rows replaced)
```

**How it works.**

- `apply_day(1)` changes the ERP the way 2 January did in Chapters 45 and 46: two new orders with three lines, one order delivered, one cancelled.
- `ingest.sync_table(wh, table)` is Chapter 45's hash comparison and upsert (section 45.5), packaged as a function in Chapter 46: it makes the warehouse's `raw` copy of the table match the ERP, inserting, updating, and deleting.
- `ingest.load_dispatch(wh, day)` loads that day's dispatch file into `raw.dispatch`, after checking its columns (Chapter 45, section 45.8), and replaces any rows an earlier load of the same day left. It returns a short message: here, the number of rows loaded.

Now count what arrived:

```python
print("rows loaded:", wh.execute("""
    SELECT (SELECT COUNT(*) FROM raw.orders),
           (SELECT COUNT(*) FROM raw.order_items),
           (SELECT COUNT(*) FROM raw.dispatch)""").fetchone())
```

```
rows loaded: (177, 333, 5)
```

The query is three `COUNT(*)` queries in one `SELECT`, each in its own brackets. Each bracketed query returns one number (a **scalar subquery**, Chapter 12, section 12.12), so the result is one row with three values. `.fetchone()` returns that row as a tuple. The warehouse now holds the 2 January state from Chapter 46: 177 orders, 333 order lines, and 5 dispatch rows.

### A tiny test framework

Every test is a query. The first function only records a test; it doesn't run anything yet:

```python
def data_test(name, sql, severity="error", description=""):
    """A data test is a query that returns the rows that BREAK a rule.
    Zero rows means the test passed."""
    assert severity in ("error", "warn"), "severity must be 'error' or 'warn'"
    return {"name": name, "sql": sql, "severity": severity, "description": description}

print(data_test("demo", "SELECT 1 WHERE FALSE"))
```

```
{'name': 'demo', 'sql': 'SELECT 1 WHERE FALSE', 'severity': 'error', 'description': ''}
```

**How it works.**

- The text in triple quotes under `def` is a **docstring** (Chapter 17, section 17.8): the function's one-paragraph description.
- `data_test()` returns a dictionary with the test's name, the query that returns *failing* rows, its severity, and a plain-English description of the rule. Writing the description first is a good habit: if you can't say the rule in one sentence, you don't have a rule yet.
- `severity="error"` is a default: a test is an error unless you say otherwise.
- `assert` stops with a message when its condition is false. Here it catches a misspelled severity, which would otherwise be silently ignored.

What happens if you change `"warn"` to the natural spelling, `"warning"`? Try it:

```python
data_test("demo", "SELECT 1 WHERE FALSE", severity="warning")
```

```
AssertionError: severity must be 'error' or 'warn'
```

Without the `assert`, this test would be created, and when it failed it would be counted neither as an error nor as a warning, because the runner below only knows those two words.

The second function runs a list of tests and reports:

```python
def run_tests(tests, show_rows=2):
    results = []
    for t in tests:
        rows = wh.execute(t["sql"]).fetchall()
        results.append({"name": t["name"], "severity": t["severity"],
                        "failing_rows": len(rows), "sample": rows[:show_rows]})
    width = max(len(r["name"]) for r in results)
    for r in results:
        status = "PASS" if r["failing_rows"] == 0 else r["severity"].upper()
        example = f"  e.g. {r['sample']}" if r["failing_rows"] else ""
        print(f"{r['name']:<{width}}  {status:<5}  failing rows: {r['failing_rows']}{example}")
    passed = [r for r in results if r["failing_rows"] == 0]
    errors = [r for r in results if r["failing_rows"] and r["severity"] == "error"]
    warnings = [r for r in results if r["failing_rows"] and r["severity"] == "warn"]
    print(f"\n{len(results)} tests, {len(passed)} passed, "
          f"{len(errors)} failed as errors, {len(warnings)} warnings")
    return results

print("test framework ready")
```

```
test framework ready
```

**How it works, line by line.**

- `wh.execute(t["sql"]).fetchall()` runs the test's query on the warehouse and returns every row as a list of tuples. `wh` is the connection from the setup cell; the function reads it from the notebook. (Passing the connection in as an argument would be cleaner, as Chapter 29 recommends; here it keeps each test call short.)
- `len(rows)` is the number of failing rows. `rows[:show_rows]` keeps the first two as examples, so a test with ten thousand failures doesn't flood the screen.
- `width = max(len(r["name"]) for r in results)` finds the length of the longest test name. The expression inside `max()` works like a list comprehension without the square brackets: it produces each name's length in turn.
- `status` is a **conditional expression** (Chapter 17, section 17.5): `"PASS"` if nothing failed, otherwise the severity in capitals, `ERROR` or `WARN`. `example` is either the sample rows or empty text.
- In the f-string, `:<{width}` means "left-align in `width` characters", and `:<5` pads the status to five, so the columns line up (Chapter 17, section 17.7).
- The three list comprehensions sort the results into passed, errors, and warnings, and the last `print` counts them. `"\n"` starts with a blank line.
- `return results` hands the results back, so a pipeline can decide what to do. Section 47.4 uses the count of **errors** to decide whether to publish.

This is a teaching version, in about 20 lines. dbt, Great Expectations, and Soda add scheduling, storage of results, history, and reporting. dbt's tests compile to failing-rows queries like these; Great Expectations and Soda compute counts of failing values and report them, which is the same rule expressed as a measurement. Section 47.10 runs one rule in each.

### The tests

```python
TESTS = [
  data_test("orders_unique_key", """
      SELECT order_id, COUNT(*) AS n FROM raw.orders GROUP BY order_id HAVING COUNT(*) > 1""",
      description="uniqueness: one row per order"),
  data_test("orders_customer_not_null", """
      SELECT order_id FROM raw.orders WHERE customer_id IS NULL""",
      description="completeness: every order has a customer"),
  data_test("orders_status_accepted", """
      SELECT order_id, status FROM raw.orders
      WHERE status NOT IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')""",
      description="validity: only known statuses"),
  data_test("order_items_have_an_order", """
      SELECT i.order_item_id, i.order_id FROM raw.order_items AS i
      LEFT JOIN raw.orders AS o ON o.order_id = i.order_id
      WHERE o.order_id IS NULL""",
      description="consistency: every order line belongs to an order"),
  data_test("order_items_quantity_positive", """
      SELECT order_item_id, quantity FROM raw.order_items WHERE quantity <= 0""",
      description="validity: quantities are positive"),
  data_test("orders_have_at_least_one_line", """
      SELECT o.order_id FROM raw.orders AS o
      LEFT JOIN raw.order_items AS i ON i.order_id = o.order_id
      WHERE i.order_item_id IS NULL""",
      description="completeness: every order has at least one order line"),
  data_test("dispatch_order_known", """
      SELECT d.dispatch_id FROM raw.dispatch AS d
      LEFT JOIN raw.orders AS o ON o.order_id = d.order_id
      WHERE o.order_id IS NULL""",
      severity="warn",
      description="consistency: dispatches point at known orders"),
]
results = run_tests(TESTS)
```

```
orders_unique_key              PASS   failing rows: 0
orders_customer_not_null       PASS   failing rows: 0
orders_status_accepted         PASS   failing rows: 0
order_items_have_an_order      PASS   failing rows: 0
order_items_quantity_positive  PASS   failing rows: 0
orders_have_at_least_one_line  PASS   failing rows: 0
dispatch_order_known           PASS   failing rows: 0

7 tests, 7 passed, 0 failed as errors, 0 warnings
```

**Reading it.** Seven rules, covering four of the six dimensions: uniqueness, completeness, validity, and consistency. Accuracy (reconciliation with the ERP) comes in section 47.4, and timeliness (freshness) in section 47.5. All seven pass on today's data. Each query is SQL you already know:

- `GROUP BY … HAVING COUNT(*) > 1` returns keys that appear more than once (Chapter 12).
- `LEFT JOIN … WHERE o.order_id IS NULL` is the **anti-join** from Chapter 12, section 12.10: it keeps the rows that found no partner. Two tests use it in each direction: order lines with no order, and orders with no lines.
- `dispatch_order_known` is a **warning**: dispatch rows can legitimately arrive for an order the warehouse hasn't loaded yet, so it's worth seeing but shouldn't stop the Flash.

Notice also what these tests are *not*: they aren't a check that the pipeline ran. Chapter 46's checks answered "did this step produce the right numbers?"; these answer "is the data in the warehouse sane?" Both matter, and both run in the pipeline.

### Watching them fail

A test suite nobody has seen fail is a test suite you don't know works. Break things on purpose. First, try to put an order line for an order that doesn't exist into the ERP itself:

```python
import psycopg2

conn = psycopg2.connect(ingest.SRC)
try:
    with conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO order_items
                           (order_item_id, order_id, product_id, quantity, unit_price, discount_pct)
                       VALUES (335, 99999, 101, 12, 430.00, 0.00)""")
except psycopg2.Error as e:
    print("the ERP refused it:", str(e).splitlines()[0])
finally:
    conn.close()
```

```
the ERP refused it: insert or update on table "order_items" violates foreign key constraint "order_items_order_id_fkey"
```

**How it works.**

- `ingest.SRC` is the ERP's connection string, the same one Chapter 45 set up (section 45.2). `psycopg2.connect()` opens the connection.
- The `INSERT` names its columns, so you can read the values: line 335 claims to belong to order 99999, for 12 units of product 101 at ₹430.00 with no discount. There is no order 99999.
- In psycopg2, `with conn` wraps the statements in a **transaction**: it commits if they succeed and rolls back if one fails. It does *not* close the connection. That's why `conn.close()` sits in **`finally`**, which runs whether the insert worked or raised an error (Chapter 17, section 17.10).
- `except psycopg2.Error as e` catches the database's refusal. `str(e).splitlines()[0]` keeps the first line of the error message; the rest is detail.

The ERP **refused** the orphan order line: the source database has a **foreign key** (Chapter 12) preventing a line from pointing at an order that doesn't exist. Source systems often have constraints like this, which is why many warehouse problems come from the loading, not from the source.

So break the *warehouse* instead, the way a half-finished load, a bad manual fix, or a bug in a transformation would. Before you run the next cell, predict which of the seven tests will fail:

```python
wh.execute("""INSERT INTO raw.order_items
                  (order_item_id, order_id, product_id, quantity, unit_price, discount_pct)
              VALUES (335, 99999, 101, 12, 430.00, 0.00)""")     # an order that isn't there
wh.execute("""INSERT INTO raw.order_items
                  (order_item_id, order_id, product_id, quantity, unit_price, discount_pct)
              VALUES (336, 10176, 103, -8, 115.00, 0.00)""")     # a negative quantity
wh.execute("UPDATE raw.orders SET status = 'On Hold' WHERE order_id = 10177")   # a status nobody agreed
results = run_tests(TESTS)
```

```
orders_unique_key              PASS   failing rows: 0
orders_customer_not_null       PASS   failing rows: 0
orders_status_accepted         ERROR  failing rows: 1  e.g. [(10177, 'On Hold')]
order_items_have_an_order      ERROR  failing rows: 1  e.g. [(335, 99999)]
order_items_quantity_positive  ERROR  failing rows: 1  e.g. [(336, -8)]
orders_have_at_least_one_line  PASS   failing rows: 0
dispatch_order_known           PASS   failing rows: 0

7 tests, 4 passed, 3 failed as errors, 0 warnings
```

**Reading it.** The warehouse has no foreign key, so it accepted all three changes. Three tests caught three different problems: an unknown status, an order line with no order, and a negative quantity. Each failure shows the rows involved, so the investigation starts with facts.

### Self-healing loads

Because Chapter 45's hash comparison makes the warehouse match the source (inserting, updating, *and* deleting), re-running the load repairs damage of this kind:

```python
ingest.sync_table(wh, "orders")
ingest.sync_table(wh, "order_items")
results = run_tests(TESTS)
```

```
orders_unique_key              PASS   failing rows: 0
orders_customer_not_null       PASS   failing rows: 0
orders_status_accepted         PASS   failing rows: 0
order_items_have_an_order      PASS   failing rows: 0
order_items_quantity_positive  PASS   failing rows: 0
orders_have_at_least_one_line  PASS   failing rows: 0
dispatch_order_known           PASS   failing rows: 0

7 tests, 7 passed, 0 failed as errors, 0 warnings
```

The cell re-runs `sync_table()` for both tables, then the same `run_tests(TESTS)`. The load deleted the two invented order lines, which exist nowhere in the ERP, and set order 10177's status back to the ERP's value. That's worth knowing during an incident: for tables loaded by full comparison, "re-run the load" is often the fix, and it's safe because the load is idempotent (Chapter 46).

### The same tests as dbt tests

If your transformations live in dbt (Chapter 32), most of these tests are one or two lines of YAML, and dbt writes the SQL. In your Chapter 32 project, `stg_orders` and `stg_order_items` are the staging models over the ERP's two tables. Written in Chapter 32's style (`data_tests:`, with a test's settings under `arguments:`), the rules in `models/staging/schema.yml` look like this:

<!-- run: none -->
```yaml
# models/staging/schema.yml (the stg_orders and stg_order_items entries)
version: 2
models:
  - name: stg_orders
    description: "One row per order, from the ERP"
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: customer_id
        data_tests: [not_null]
      - name: status
        data_tests:
          - accepted_values:
              arguments:
                values: ["Pending", "Shipped", "Delivered", "Cancelled"]
  - name: stg_order_items
    columns:
      - name: order_id
        data_tests:
          - relationships:
              arguments:
                to: ref('stg_orders')
                field: order_id
      - name: quantity
        data_tests:
          - dbt_utils.accepted_range:
              arguments:
                min_value: 1
```

- `unique`, `not_null`, `accepted_values`, and `relationships` are the generic tests Chapter 32 used (section 32.7). `relationships` is the anti-join: every `order_id` in the order lines must exist in `stg_orders`.
- `dbt_utils.accepted_range` comes from the `dbt_utils` package. It must be listed in `packages.yml` and downloaded with `dbt deps`, as Chapter 32 showed (section 32.11). `min_value: 1` means quantities of 1 or more pass.

The rule "every order has at least one line" has no generic test, so it's a **singular test** (Chapter 32): a SQL file in the project's `tests/` folder that returns the failing rows, the counterpart of `data_test()`:

<!-- run: none -->
```sql
-- tests/assert_orders_have_lines.sql
-- Every order has at least one order line. A dbt test passes when it returns no rows.
select o.order_id
from {{ ref('stg_orders') }} as o
left join {{ ref('stg_order_items') }} as i on i.order_id = o.order_id
where i.order_item_id is null
```

Run just these models' tests (the Chapter 32 project reads `riverstone_2025`, so there are no January orders here):

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt test --threads 1 --select stg_orders stg_order_items
04:11:22  Running with dbt=1.12.5
04:11:23  Found 10 models, 27 data tests, 1 snapshot, 5 sources, 594 macros
04:11:23  1 of 7 PASS accepted_values_stg_orders_status__Pending__Shipped__Delivered__Cancelled  [PASS in 0.06s]
04:11:23  2 of 7 PASS assert_orders_have_lines ........................................... [PASS in 0.02s]
04:11:23  3 of 7 PASS dbt_utils_accepted_range_stg_order_items_quantity__1 ............... [PASS in 0.02s]
04:11:23  4 of 7 PASS not_null_stg_orders_customer_id .................................... [PASS in 0.02s]
04:11:23  5 of 7 PASS not_null_stg_orders_order_id ....................................... [PASS in 0.02s]
04:11:23  6 of 7 PASS relationships_stg_order_items_order_id__order_id__ref_stg_orders_ .. [PASS in 0.03s]
04:11:23  7 of 7 PASS unique_stg_orders_order_id ......................................... [PASS in 0.02s]
04:11:23  Done. PASS=7 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=7
```

*(Trimmed: dbt also prints a "START" line before each test, and a few setup lines.)* `--threads 1` runs the tests one at a time, so they print in a steady order; `--select` picks the two models, and dbt runs every test attached to them. dbt names each generic test after the rule, the model, and the column.

To see that dbt writes the same kind of query as `data_test()`, open the compiled SQL for one test, in `target/compiled/riverstone_dbt/models/staging/schema.yml/unique_stg_orders_order_id.sql`:

<!-- run: none -->
```sql
select
    order_id as unique_field,
    count(*) as n_records

from "riverstone_2025"."dbt_dev_staging"."stg_orders"
where order_id is not null
group by order_id
having count(*) > 1
```

It's `orders_unique_key` with different names: dbt calls the key `unique_field` and the count `n_records`, and names the model in full as database, schema, and view, `"riverstone_2025"."dbt_dev_staging"."stg_orders"` (Chapter 32's development schema). Severity works the same way too: a test that should warn rather than stop gets one more setting. In dbt, `config: {severity: warn}` under a test is the counterpart of `severity="warn"`:

<!-- run: none -->
```yaml
      - name: order_id
        data_tests:
          - relationships:
              arguments:
                to: ref('stg_orders')
                field: order_id
              config:
                severity: warn
```

`dbt build` then reports that test as `WARN` instead of `ERROR` when it finds rows, and doesn't stop the models downstream of it.

---

## 47.4 Write–audit–publish

Chapter 46 left a gap. The check stopped the email, but the wrong row stayed in `mart.daily_flash`, where any dashboard or analyst could read it. **Write–audit–publish** (WAP) closes it:

1. **Write** the new data somewhere readers don't look (an audit or staging schema).
2. **Audit** it: run the tests against the new data.
3. **Publish** only if the tests pass: swap it into the table people read, in one transaction.

![Three stages left to right. Write: the pipeline builds audit.daily_flash_new, a table nobody reads. Audit: tests run on the new table: one row per day, revenue not negative, orders and revenue match the ERP. From the audit, one arrow leads to Publish, labelled all pass: one transaction replaces the day in mart.daily_flash, which dashboards and analysts read. Another arrow leads to a box labelled any error: blocked, where mart.daily_flash keeps its last good data and an incident alert goes to the owner. A note says readers of the published table only ever see data that passed its tests, while in Chapter 46 the same failure left a wrong row where anyone could query it.](figures/fig47-1-write-audit-publish.svg)

*Figure 47.1 — Write–audit–publish. Readers of the published table only ever see data that passed its tests.*

The code comes in four small steps, one for each part of the figure and one to put them together.

### Write: build the day where nobody reads it

```python
def build_flash_staging(day):
    """Write: build one day's Flash into the audit schema, where nobody reads it."""
    wh.execute("CREATE SCHEMA IF NOT EXISTS audit")
    wh.execute("""
        CREATE OR REPLACE TABLE audit.daily_flash_new AS
        SELECT CAST(? AS DATE) AS flash_date,
               COUNT(DISTINCT o.order_id) AS orders_booked,
               CAST(ROUND(COALESCE(SUM(i.quantity * i.unit_price
                                       * (1 - i.discount_pct / 100)), 0), 2)
                    AS DECIMAL(12,2)) AS revenue_booked
        FROM raw.orders AS o
        JOIN raw.order_items AS i ON i.order_id = o.order_id
        WHERE o.order_date = CAST(? AS DATE) AND o.status <> 'Cancelled'""", [day, day])

build_flash_staging("2026-01-02")
print(wh.execute("SELECT * FROM audit.daily_flash_new").fetchall())
```

```
[(datetime.date(2026, 1, 2), 2, Decimal('38710.00'))]
```

**How it works.**

- **`CREATE SCHEMA IF NOT EXISTS audit`** makes a separate schema, a named folder of tables inside the warehouse (Chapter 45 used `raw`; Chapter 46 used `mart`). Dashboards and analysts are pointed at `mart`, never at `audit`, so whatever is built here is invisible to them until it's published.
- **`CREATE OR REPLACE TABLE … AS SELECT`** builds a table from a query's result, replacing any earlier version. Each run starts from a clean audit table.
- The query is Chapter 46's Flash: orders booked and revenue net of discounts, excluding cancelled orders, for one day.
- The two **`?`** marks are **parameters**, filled in order from the list `[day, day]`. The day's text never becomes part of the SQL itself (Chapter 45, section 45.3). `CAST(? AS DATE)` turns the text `"2026-01-02"` into a date.
- **`ROUND(…, 2)`** and **`CAST(… AS DECIMAL(12,2))`** store revenue as an exact amount in rupees and paise. The sum by itself is a floating-point number, because dividing by 100 produces one. The next step explains why that matters.

The result is one row: 2 January, 2 orders, ₹38,710.00, exactly as in Chapter 46.

### The ERP's own answer

The audit needs something to compare with. This is the same Flash query, run on the ERP:

```python
ERP_FLASH_SQL = """
    SELECT COUNT(DISTINCT o.order_id),
           ROUND(COALESCE(SUM(i.quantity * i.unit_price * (1 - i.discount_pct / 100)), 0), 2)
    FROM orders AS o JOIN order_items AS i ON i.order_id = o.order_id
    WHERE o.order_date = %s AND o.status <> 'Cancelled'"""

print(ingest.fetch_rows(ERP_FLASH_SQL, ["2026-01-02"]))
```

```
[(2, Decimal('38710.00'))]
```

**How it works.** `ingest.fetch_rows(sql, params)` runs the query on the ERP and returns its rows. **`%s`** is psycopg2's placeholder, where DuckDB uses `?`: two libraries, two placeholder styles, as Chapter 45's placeholder table showed (section 45.3), and both keep the value out of the SQL text. The ERP's tables have no `raw.` prefix, because they're the source itself. PostgreSQL returns money as a `Decimal`, an exact number, and `ROUND(…, 2)` keeps it to the paisa.

Why round both sides? Because comparing floating-point numbers exactly is a trap. Before you run this, predict the two answers:

```python
print(wh.execute("""
    SELECT 0.1::DOUBLE + 0.2::DOUBLE = 0.3::DOUBLE,
           0.1::DECIMAL(12,2) + 0.2::DECIMAL(12,2) = 0.3::DECIMAL(12,2)""").fetchone())
```

```
(False, True)
```

A **`DOUBLE`** is a floating-point number, which stores most decimals only approximately (Chapter 17, section 17.3): 0.1 + 0.2 comes out a hair above 0.3, so the comparison is false. `x::DOUBLE` is shorthand for `CAST(x AS DOUBLE)`, borrowed from PostgreSQL. A `DECIMAL(12,2)` stores exact paise, so the same sum equals 0.3. Money is compared at two decimal places, as exact decimals. Without the rounding, a day whose revenue had a fraction of a paisa in the middle of the arithmetic (3 units at ₹1,234.50 with 7.5% off is ₹3,425.7375) could fail the reconciliation even when both systems agree.

### Audit: run the tests on the new data

```python
AUDIT_TESTS = [
  data_test("flash_one_row", """
      SELECT flash_date, COUNT(*) FROM audit.daily_flash_new
      GROUP BY flash_date HAVING COUNT(*) <> 1""",
      description="uniqueness: exactly one row for the day"),
  data_test("flash_revenue_not_negative", """
      SELECT flash_date, revenue_booked FROM audit.daily_flash_new WHERE revenue_booked < 0""",
      description="validity: revenue is never negative"),
  data_test("flash_matches_erp", """
      SELECT n.orders_booked AS warehouse_orders, e.orders_booked AS erp_orders,
             n.revenue_booked AS warehouse_revenue, e.revenue_booked AS erp_revenue
      FROM audit.daily_flash_new AS n, audit.erp_expected AS e
      WHERE n.orders_booked <> e.orders_booked OR n.revenue_booked <> e.revenue_booked""",
      description="accuracy: orders and revenue equal the ERP's"),
]

def audit_flash(day):
    """Audit: store the ERP's answer next to the new data, run the audit tests,
    and return True only if no error-severity test failed."""
    erp_orders, erp_revenue = ingest.fetch_rows(ERP_FLASH_SQL, [day])[0]
    wh.execute("""CREATE OR REPLACE TABLE audit.erp_expected AS
                  SELECT CAST(? AS INTEGER) AS orders_booked,
                         CAST(? AS DECIMAL(12,2)) AS revenue_booked""", [erp_orders, erp_revenue])
    results = run_tests(AUDIT_TESTS)
    return not any(r["failing_rows"] and r["severity"] == "error" for r in results)

print("safe to publish:", audit_flash("2026-01-02"))
```

```
flash_one_row               PASS   failing rows: 0
flash_revenue_not_negative  PASS   failing rows: 0
flash_matches_erp           PASS   failing rows: 0

3 tests, 3 passed, 0 failed as errors, 0 warnings
safe to publish: True
```

**How it works.**

- The three audit tests are ordinary data tests, pointed at the audit table: one row for the day, no negative revenue, and a reconciliation with the ERP. Together they add the sixth dimension, **accuracy**.
- `audit_flash()` first fetches the ERP's answer, and **unpacks** the one row into two names (Chapter 17, section 17.4). It stores them as a one-row table, `audit.erp_expected`, so the reconciliation can be a query like every other test.
- `FROM audit.daily_flash_new AS n, audit.erp_expected AS e` lists two tables with a comma and no `ON`. That pairs every row of the first with every row of the second (a **cross join**, the comma form Chapter 32's reconciliation test used). Both tables have exactly one row, so the result is exactly one pair, and the `WHERE` keeps it only if the numbers differ.
- `any(…)` is `True` if at least one test failed as an error (the same pattern as `run_tests()`'s list comprehensions, without the brackets). `not any(…)` is therefore "safe to publish".

### Publish: swap it in, in one transaction

```python
def publish_flash(day):
    """Write, audit, and publish one day of the Flash. Returns True if it was published."""
    print(f"--- write-audit-publish for {day} ---")
    build_flash_staging(day)
    if not audit_flash(day):
        print("PUBLISH BLOCKED: mart.daily_flash left untouched")
        return False
    wh.execute("CREATE SCHEMA IF NOT EXISTS mart")
    wh.execute("""CREATE TABLE IF NOT EXISTS mart.daily_flash (
                      flash_date DATE, orders_booked INTEGER, revenue_booked DECIMAL(12,2))""")
    wh.execute("BEGIN")
    try:
        wh.execute("DELETE FROM mart.daily_flash WHERE flash_date = ?", [day])
        wh.execute("""INSERT INTO mart.daily_flash (flash_date, orders_booked, revenue_booked)
                      SELECT flash_date, orders_booked, revenue_booked FROM audit.daily_flash_new""")
        wh.execute("COMMIT")
    except Exception:
        wh.execute("ROLLBACK")
        raise
    print("PUBLISHED")
    return True

publish_flash("2026-01-02")
print("mart.daily_flash:", wh.execute("SELECT * FROM mart.daily_flash ORDER BY flash_date").fetchall())
```

```
--- write-audit-publish for 2026-01-02 ---
flash_one_row               PASS   failing rows: 0
flash_revenue_not_negative  PASS   failing rows: 0
flash_matches_erp           PASS   failing rows: 0

3 tests, 3 passed, 0 failed as errors, 0 warnings
PUBLISHED
mart.daily_flash: [(datetime.date(2026, 1, 2), 2, Decimal('38710.00'))]
```

**How it works.**

- `publish_flash()` runs the three stages in order: write, audit, and, only if the audit passed, publish. If any error-severity test failed, it prints why and returns `False` without touching `mart.daily_flash`.
- `CREATE TABLE IF NOT EXISTS` makes the published table the first time only.
- **`BEGIN` … `COMMIT`** is a transaction: the delete and the insert happen together or not at all, so a reader never sees the day missing halfway through a swap.
- Deleting the day before inserting it makes the step **idempotent**, exactly as in Chapter 46 (section 46.4): publishing the same day twice leaves one row, not two.
- The `INSERT` names its columns in both lists, so it still works if someone later adds a column to either table in a different position.
- **`try` / `except`** with **`ROLLBACK`**: if the delete or insert fails, the transaction is undone, so the connection isn't left half-way through it, and `raise` passes the original error on so it isn't hidden.

### The same bad morning, with WAP

Now repeat Chapter 46's 5 January failure: the order-line load silently loads nothing.

```python
apply_day(2)                                    # the 5 January business day (Chapter 45)
ingest.BROKEN_ITEMS_SYNC = True                 # Chapter 46's bug: the order-line load loads nothing
ingest.sync_table(wh, "orders")
ingest.sync_table(wh, "order_items")

publish_flash("2026-01-05")
print("mart.daily_flash:", wh.execute("SELECT * FROM mart.daily_flash ORDER BY flash_date").fetchall())
print("readers of mart.daily_flash never saw the 5 January row:",
      wh.execute("SELECT COUNT(*) FROM mart.daily_flash WHERE flash_date = '2026-01-05'").fetchone()[0] == 0)
```

```
--- write-audit-publish for 2026-01-05 ---
flash_one_row               PASS   failing rows: 0
flash_revenue_not_negative  PASS   failing rows: 0
flash_matches_erp           ERROR  failing rows: 1  e.g. [(0, 1, Decimal('0.00'), Decimal('18750.00'))]

3 tests, 2 passed, 1 failed as errors, 0 warnings
PUBLISH BLOCKED: mart.daily_flash left untouched
mart.daily_flash: [(datetime.date(2026, 1, 2), 2, Decimal('38710.00'))]
readers of mart.daily_flash never saw the 5 January row: True
```

**Reading it.** `ingest.BROKEN_ITEMS_SYNC = True` switches on the simulated bug in the companion module, the same switch Chapter 46 used (section 46.7). The reconciliation test failed: the ERP has 1 order for ₹18,750.00, the new data has 0 orders and ₹0.00. Publishing was blocked, and `mart.daily_flash` still holds only the good 2 January row. In Chapter 46, the same failure left a wrong row in the published table. Now readers never see it: they see the last good data, and the freshness check in the next section is what tells them (and the on-call engineer) that today's is missing.

The bug stays switched on until section 47.9 fixes it and publishes the day, so sections 47.5 to 47.9 find the problem the way a real team would.

> **Watch out: "no data" is also a state people can misread.** A missing day can look like a zero day on a chart. Publish a status alongside the data (for example, a `load_status` table saying which days are published, late, or failed), and show it on dashboards, so "we don't know yet" never looks like "we sold nothing".

### Variations

- **Blue/green tables:** build a whole new table, test it, then swap names. Good for full rebuilds.
- **Table snapshots or time travel:** warehouses such as Snowflake, BigQuery, and Delta or Iceberg tables (Chapter 49) can keep previous versions, so publishing is a metadata change and rolling back is quick.
- **Views over the last good partition:** readers query a view that points at published partitions only.

---

## 47.5 Observability: freshness, volume, and unusual values

Tests answer "is this data right?" **Observability** answers "is the platform behaving normally?" Three signals carry most of the value.

### Freshness

**Freshness** is the age of the newest data. Stale data is one of the most common data incidents, and the hardest to notice, because nothing failed: a report keeps showing last Tuesday's numbers.

A freshness check needs a date column that says which day each row belongs to. For orders it's `order_date`. For the dispatch file, look at what `raw.dispatch` holds:

```python
for row in wh.execute("DESCRIBE raw.dispatch").fetchall():
    print(row[:2])
```

```
('dispatch_id', 'VARCHAR')
('order_id', 'INTEGER')
('dispatch_date', 'VARCHAR')
('qty_units', 'VARCHAR')
('file_day', 'DATE')
```

`DESCRIBE` lists a table's columns and types (Chapter 45, section 45.7), and `row[:2]` keeps the name and the type. The last column, **`file_day`**, isn't in the file: `load_dispatch()` (Chapter 46, section 46.3) stamps every row with the date in the file's name, `dispatch_2026-01-02.csv`, which is also how it replaces a day's rows when the same file is loaded again. `dispatch_date` stays as text, because the file writes dates as dd-mm-yyyy (Chapter 45 types it in staging). So `file_day` is the column that says how fresh the dispatch data is.

How fresh is fresh enough? Riverstone's Flash is promised on **working days**, Monday to Friday. At the 6:30 a.m. run, the newest data should be from the previous working day. That day is easy to work out:

```python
from datetime import date, datetime, time, timedelta

def previous_working_day(day):
    """The last Monday-to-Friday date before `day`."""
    day = day - timedelta(days=1)
    while day.weekday() >= 5:            # Monday is 0 ... Saturday is 5, Sunday is 6
        day = day - timedelta(days=1)
    return day

print("the run on Tuesday 6 January expects:", previous_working_day(date(2026, 1, 6)))
print("the run on Monday 5 January expects: ", previous_working_day(date(2026, 1, 5)))
```

```
the run on Tuesday 6 January expects: 2026-01-05
the run on Monday 5 January expects:  2026-01-02
```

**How it works.** `timedelta(days=1)` is one day (Chapter 17, section 17.11), so `day - timedelta(days=1)` is the day before. `.weekday()` numbers the days of the week from Monday, 0, to Sunday, 6. The `while` loop keeps stepping back over Saturday and Sunday, so on a Monday the answer is the Friday before. (Public holidays need a list of their own; the loop would skip those dates too.)

Now the check itself:

```python
NOW = datetime(2026, 1, 6, 6, 30)        # the 6:30 a.m. run on Tuesday 6 January, as a fixed clock

def freshness_check(table, date_column, now=NOW):
    newest = wh.execute(f"SELECT MAX({date_column}) FROM {table}").fetchone()[0]
    expected = previous_working_day(now.date())
    age_hours = (now - datetime.combine(newest, time(0, 0))).total_seconds() / 3600
    status = "PASS" if newest >= expected else "STALE"
    print(f"{table:<17} newest {newest}  expected {expected}  age {age_hours:5.1f} h  {status}")
    return (table, age_hours, status)

freshness = [freshness_check("raw.orders", "order_date"),
             freshness_check("raw.dispatch", "file_day"),
             freshness_check("mart.daily_flash", "flash_date")]
```

```
raw.orders        newest 2026-01-05  expected 2026-01-05  age  30.5 h  PASS
raw.dispatch      newest 2026-01-02  expected 2026-01-05  age 102.5 h  STALE
mart.daily_flash  newest 2026-01-02  expected 2026-01-05  age 102.5 h  STALE
```

**How it works, line by line.**

- **`NOW`** is a fixed clock: 6:30 a.m. on Tuesday 6 January. With a fixed time, the output is the same every time you run it. In production, `now` would be `datetime.now()`.
- `f"SELECT MAX({date_column}) FROM {table}"` puts the table and column **names** into the SQL text. Parameters (`?`) can only stand for values, not names, so names have to be pasted in. Only pass names you control, never text typed by a user (Chapter 45).
- `expected` is the previous working day, from the helper above. The status is **PASS** if the newest date is that day or later, and **STALE** if it's older.
- `age_hours` is for people reading the report. A date has no time of day, so `datetime.combine(newest, time(0, 0))` treats it as midnight at the start of that day. `now - …` is a `timedelta`, `.total_seconds()` turns it into seconds, and dividing by 3,600 gives hours. So yesterday's orders are already 24 + 6.5 = 30.5 hours old at 6:30 this morning.
- `{age_hours:5.1f}` prints the hours with one decimal place in five characters, and `{table:<17}` lines up the names.
- The function returns the table, its age, and its status as a tuple, so section 47.9 can build its alert from these real results.

**Reading it.** Orders are fresh: the newest is from 5 January, the previous working day. Two things are stale. `raw.dispatch` hasn't been loaded since 2 January: the 5 January file did arrive, but with changed columns (section 47.7), so it wasn't loaded. A load that fails or never runs looks exactly like a file that never came, and freshness catches both. And `mart.daily_flash` has no 5 January row, because publishing was blocked. Both are real problems that no test on the *contents* would find.

**Setting limits.** Base each limit on the promise made to users, not on how the pipeline usually behaves. Riverstone's Flash promise is "sent by 7:30 a.m. IST on working days", so at the 6:30 run the newest day must be the previous working day. Why not a limit in hours? Because the hours move with the calendar:

```python
tuesday_age = datetime(2026, 1, 6, 6, 30) - datetime(2026, 1, 5)     # Tuesday's run, Monday's data
monday_age = datetime(2026, 1, 5, 6, 30) - datetime(2026, 1, 2)      # Monday's run, Friday's data
print("Monday's data at Tuesday's run:", tuesday_age.total_seconds() / 3600, "hours")
print("Friday's data at Monday's run: ", monday_age.total_seconds() / 3600, "hours")
```

```
Monday's data at Tuesday's run: 30.5 hours
Friday's data at Monday's run:  78.5 hours
```

Perfectly fresh data is 30.5 hours old on a Tuesday morning, and 78.5 hours old on a Monday morning, because 2 January 2026 is a Friday. A limit of "under 24 hours" would call good data stale every morning; a limit of 48 hours would call it stale every Monday and after every holiday. If you must use hours, you need two limits (about 32 hours on Tuesday to Friday, 80 on Mondays). Comparing with the previous working day says the promise directly. Check freshness *before* using a table, and monitor it separately from the pipeline, so a pipeline that never starts is noticed too.

### Volume and unusual values

**Volume checks** compare the size of today's data with what's normal: rows loaded, orders booked, revenue. The classic silent failure is a load that brings in far less than usual, or nothing at all.

Comparing against history needs a baseline. A **median** is a good one, because a single huge day doesn't drag it around the way an average does (Chapter 21). The warehouse holds all of 2025 as well as the January days, so first get each 2025 day's orders and revenue:

```python
import statistics

daily = wh.execute("""
    SELECT o.order_date, COUNT(DISTINCT o.order_id) AS orders,
           SUM(i.quantity * i.unit_price * (1 - i.discount_pct / 100)) AS revenue
    FROM raw.orders AS o JOIN raw.order_items AS i ON i.order_id = o.order_id
    WHERE o.status <> 'Cancelled' AND o.order_date BETWEEN DATE '2025-01-01' AND DATE '2025-12-31'
    GROUP BY o.order_date""").fetchall()
median = statistics.median(rev for d, n, rev in daily)
unusual = [(str(d), rev) for d, n, rev in daily if rev > 3 * median]
print("days with orders in 2025:", len(daily))
print("median day's revenue    : Rs", f"{median:,.2f}")
print("days above 3x the median:", len(unusual))
for day, rev in sorted(unusual, key=lambda pair: pair[1], reverse=True)[:3]:
    print(f"  {day}  Rs {rev:,.2f}")
```

```
days with orders in 2025: 131
median day's revenue    : Rs 27,442.50
days above 3x the median: 10
  2025-11-16  Rs 175,895.00
  2025-11-09  Rs 115,847.50
  2025-09-13  Rs 108,735.00
```

**How it works.**

- The query returns one row per 2025 day with orders: the date, the number of orders, and the revenue. `.fetchall()` gives a list of those three-item tuples.
- `for d, n, rev in daily` **unpacks** each tuple into three names (Chapter 17, section 17.4). The median only needs `rev`.
- `statistics.median()` (Chapter 17, section 17.11) sorts the values and takes the middle one, or the average of the two middle ones when the count is even. Here 131 days means the 66th value.
- `unusual` keeps the days above three times the median. `str(d)` turns each date into text for printing. The revenue here is a floating-point number, which is fine for a rough comparison like this one; only published money is kept exact.
- `sorted(…, key=lambda pair: pair[1], reverse=True)` sorts by the second item of each pair, the revenue, largest first. `lambda` is a one-line function without a name (Chapter 18). `[:3]` keeps the top three.
- The program prints `Rs` rather than `₹` so the output reads correctly in any terminal, and Python's `,` format groups digits in threes; in the text, amounts use the book's lakh grouping.

**Reading it.** Across 2025, Riverstone had orders on 131 days, and a typical day brought ₹27,442.50. Ten days were more than three times that, the biggest being ₹1,75,895.00 on 16 November. Those aren't errors: they're large orders and seasonal peaks. That's the lesson of anomaly detection on business data: **unusual is not the same as wrong**. Use these signals to prompt a look, not to block a pipeline.

Sensible volume rules for Riverstone:

- Error if a load that should bring new rows brings **zero** on a working day.
- Error if a published day's revenue is **negative**.
- Warn if a day's revenue is **outside a wide band** around the median of recent days (for example, below a quarter or above five times).
- Warn if row counts in a raw table **fall** compared with the previous load, since sources rarely lose rows.

> **Watch out: don't learn your baseline from broken days.** If the baseline is the average of recent days and last week was broken, "normal" quietly moves toward broken. Exclude days with failed loads from the baseline, or use a longer window and a median.

### The three questions to monitor

1. **Did it run?** Pipeline success or failure, and run duration (a run that suddenly takes three times longer is a warning).
2. **Is it fresh?** Age of the newest data in each important table.
3. **Does it look normal?** Row counts and key totals against recent history.

Chapter 46's orchestrator answers the first. This section answers the other two. Together they're what "observability" means for data.

---

## 47.6 Lineage: what breaks when this breaks

**Lineage** is the record of where data comes from and where it goes: which sources feed a table, and which tables, dashboards, and reports depend on it. It answers two questions that come up in every incident:

- **Impact:** this table is wrong. What else is wrong, and who should be told?
- **Cause:** this number is wrong. Which upstream table or source could explain it?

Chapter 46's pipeline already declares its dependencies (each asset's `deps`), and Dagster's web interface draws them as a graph. Here the graph is copied by hand from Chapter 46's asset definitions into a dictionary, with two more reports added to show the point:

```python
GRAPH = {                                    # asset -> what it is built from (Chapter 46's pipeline)
    "raw_orders": [], "raw_order_items": [], "raw_dispatch": [], "raw_crm_leads": [],
    "daily_flash": ["raw_orders", "raw_order_items"],
    "deliver_flash": ["daily_flash"],
    "dispatch_report": ["raw_dispatch", "raw_orders"],
    "weekly_pipeline_report": ["raw_crm_leads", "raw_orders"],
}

def downstream_of(asset, graph=GRAPH):
    """Every asset built, directly or indirectly, from `asset`."""
    affected, queue = set(), [asset]
    while queue:
        current = queue.pop()
        for name, parents in graph.items():
            if current in parents and name not in affected:
                affected.add(name)
                queue.append(name)
    return sorted(affected)

for broken in ["raw_order_items", "raw_dispatch"]:
    print(f"{broken} is broken -> affected: {downstream_of(broken)}")
```

```
raw_order_items is broken -> affected: ['daily_flash', 'deliver_flash']
raw_dispatch is broken -> affected: ['dispatch_report']
```

**How it works, line by line.**

- `GRAPH` maps each asset to the list of assets it's built from: its **parents**. The four raw tables have none.
- `affected` is a **set** (Chapter 17, section 17.7) of assets found so far; a set can't hold the same name twice. `queue` is a list of assets still to look at, starting with the broken one.
- `while queue:` repeats until the queue is empty. `queue.pop()` takes the last name off the list.
- The `for` loop looks through every asset and its parents. If the current asset is one of its parents, that asset is affected: add it to the set, and put it on the queue so *its* children are found too.
- By hand, for `raw_order_items`: the queue starts as `["raw_order_items"]`. Taking it off finds `daily_flash`, which lists it as a parent; `daily_flash` goes on the queue. Taking `daily_flash` off finds `deliver_flash`. Taking `deliver_flash` off finds nothing new. The queue is empty, so the answer is `['daily_flash', 'deliver_flash']`.

The other question, **cause**, walks the same graph the other way, from a wrong output back to everything it's built from:

```python
def upstream_of(asset, graph=GRAPH):
    """Every asset that `asset` is built from, directly or indirectly."""
    found, queue = set(), [asset]
    while queue:
        current = queue.pop()
        for parent in graph[current]:
            if parent not in found:
                found.add(parent)
                queue.append(parent)
    return sorted(found)

print("deliver_flash is built from:", upstream_of("deliver_flash"))
```

```
deliver_flash is built from: ['daily_flash', 'raw_order_items', 'raw_orders']
```

The loop is the same; only the direction changes. Instead of searching for assets that list the current one as a parent, it reads the current asset's own parents, `graph[current]`.

**Reading it.** Broken order lines affect the Flash and its delivery. A broken dispatch file affects only the dispatch report. That's the difference between an alert to the sales managers and a quiet note to the warehouse team, and it's why the Flash isn't wired to depend on dispatches. And if the Flash's number is wrong, only three things could explain it: `daily_flash` itself, `raw_order_items`, or `raw_orders`. The CRM and the dispatch file can be ruled out without looking.

In a real platform, lineage comes from the orchestrator's graph (Dagster's asset graph, Airflow datasets), from dbt's model graph (Chapter 32, section 32.8), and from tools that read query logs to see which dashboards touched which tables. **Column-level lineage** goes further, tracing which source column feeds which report field, which helps when a single measure looks wrong.

> **Interview extra point.** "A dashboard shows wrong numbers. Walk me through it." A strong answer starts with lineage and freshness: which tables feed it, when were they last loaded, did their tests pass, and what changed upstream today. Chapter 77 has more of these.

---

## 47.7 Data contracts in practice

Chapter 45 ended with Bhiwandi Main renaming a column and breaking a load. A **data contract** is a written agreement between a data producer and the data team about what will be delivered: the fields, their types and rules, when it arrives, who owns it, and how much notice you get before it changes.

Contracts work best when they're small, written in plain language, and **checked automatically**, so a violation is caught by the pipeline, not by an argument in a meeting. First, the contract itself, written as a Python dictionary so the pipeline can read it:

```python
DISPATCH_CONTRACT = {
    "dataset": "bhiwandi_dispatch_sheet",
    "owner": "Bhiwandi Main warehouse supervisor",
    "consumer": "data team (raw.dispatch)",
    "delivered_by": "20:00 IST on the day of dispatch",
    "change_notice_days": 10,
    "columns": {
        "dispatch_id": {"type": "text", "unique": True, "nullable": False},
        "order_id": {"type": "integer", "nullable": False},
        "dispatch_date": {"type": "date dd-mm-yyyy", "nullable": False},
        "warehouse": {"type": "text", "nullable": False},
        "qty_units": {"type": "integer", "nullable": True, "note": "blank allowed while a count is pending"},
        "remarks": {"type": "text", "nullable": True},
    },
}
print(len(DISPATCH_CONTRACT["columns"]), "columns promised by", DISPATCH_CONTRACT["owner"])
```

```
6 columns promised by Bhiwandi Main warehouse supervisor
```

Each column has a type, whether it may be blank (`nullable`), and, for `dispatch_id`, a promise that no value repeats (`unique`). The first check compares the file's columns with the contract's:

```python
import os

def check_contract(path, contract):
    header = wh.execute(f"DESCRIBE SELECT * FROM read_csv('{path}', all_varchar = true)").fetchall()
    found = [r[0] for r in header]
    expected = list(contract["columns"])
    violations = [f"missing column: {c}" for c in expected if c not in found]
    violations += [f"undeclared column: {c}" for c in found if c not in expected]
    return violations

for f in ["exports/dispatch_2026-01-02.csv", "exports/dispatch_2026-01-05.csv"]:
    v = check_contract(f, DISPATCH_CONTRACT)
    print(f"{os.path.basename(f)}: {'columns match the contract' if not v else v}")
```

```
dispatch_2026-01-02.csv: columns match the contract
dispatch_2026-01-05.csv: ['missing column: qty_units', 'undeclared column: units', 'undeclared column: vehicle_no']
```

**How it works.**

- `read_csv(path, all_varchar = true)` reads the file with every column as text (Chapter 45, section 45.8), so DuckDB's guesses about types can't fail or hide anything. Only the header matters here.
- `DESCRIBE SELECT …` returns one row per column the query would produce; `r[0]` is the column's name. The list comprehension collects the names into `found`.
- `list(contract["columns"])` lists the dictionary's keys: the six promised names.
- The two comprehensions find names that are promised but missing, and names that appear without being promised. An empty list means the columns match.
- `os.path.basename(f)` keeps the file name without its folder, for a shorter line.

**Reading it.** The 2 January file has the agreed columns. The 5 January file breaks the contract in three ways: the agreed `qty_units` column is gone, and two columns nobody agreed to have appeared. The pipeline stops, the owner is told exactly what changed, and nobody has to guess whether `units` means the same thing.

Matching column names is only half of what the contract promises. The rules about **values** can be checked too, with the failing-rows idea from section 47.2. This function checks three of them for every column: no blanks where blanks aren't allowed, no repeats where values must be unique, and whole numbers where the type is an integer:

```python
def check_contract_values(path, contract):
    source = f"read_csv('{path}', header = true, all_varchar = true)"
    violations = []
    for col, rules in contract["columns"].items():
        if not rules["nullable"]:
            blanks = wh.execute(f"SELECT COUNT(*) FROM {source} WHERE {col} IS NULL").fetchone()[0]
            if blanks:
                violations.append(f"{col}: {blanks} blank value(s)")
        if rules.get("unique"):
            repeats = wh.execute(f"SELECT COUNT(*) - COUNT(DISTINCT {col}) FROM {source}").fetchone()[0]
            if repeats:
                violations.append(f"{col}: {repeats} repeated value(s)")
        if rules["type"] == "integer":
            bad = wh.execute(f"""SELECT {col} FROM {source}
                                 WHERE {col} IS NOT NULL
                                   AND TRY_CAST(replace({col}, ',', '') AS INTEGER) IS NULL""").fetchall()
            if bad:
                violations.append(f"{col}: not a whole number: {[b[0] for b in bad]}")
    return violations

print(check_contract_values("exports/dispatch_2026-01-02.csv", DISPATCH_CONTRACT))
```

```
["qty_units: not a whole number: ['N/A']"]
```

**How it works.**

- `.items()` gives each column's name and its rules together (Chapter 17, section 17.7).
- **Blanks:** for a column with `"nullable": False`, count the rows where it's empty. Any count above zero is a violation.
- **Repeats:** `COUNT(*) - COUNT(DISTINCT dispatch_id)` is the number of rows whose value has appeared before; zero means every value is unique. `rules.get("unique")` returns `None` for columns without that rule, so they're skipped.
- **Whole numbers:** Chapter 45's pattern (section 45.7). `replace(qty_units, ',', '')` removes the thousands separator from `"1,200"`, and `TRY_CAST(… AS INTEGER)` returns NULL instead of an error when the text isn't a number. A value that isn't blank but can't be converted breaks the rule.
- The function only makes sense on a file whose columns already match; the 5 January file has no `qty_units` column to check.

**Reading it.** The 2 January file matches the contract's columns, but not its values: one row says `N/A` where the contract says a pending count is left **blank**. Chapter 45 quietly turned `N/A` into a missing value in staging. The contract turns it into a conversation: either the sheet leaves the cell empty, or the contract adds `N/A` as an agreed marker. Either answer is fine; what matters is that it's written down.

The contract's other promises need other tools. The **date format** could be checked the same way, with DuckDB's `TRY_STRPTIME`. The **delivery deadline**, 20:00 IST, is a freshness promise: the freshness monitor from section 47.5 checks it, by asking whether that day's file has been loaded.

### What a good contract contains

| Part | Riverstone's dispatch sheet |
|---|---|
| **Dataset and purpose** | Daily dispatch sheet; feeds `raw.dispatch` and the dispatch report |
| **Producer and consumer** | Bhiwandi Main warehouse supervisor → data team |
| **Fields** | Names, types, whether blanks are allowed, and what each means |
| **Rules** | `dispatch_id` unique; `order_id` exists in the ERP; quantity a whole number |
| **Delivery** | One file per working day by 20:00 IST, named `dispatch_YYYY-MM-DD.csv` |
| **Change process** | 10 working days' notice; new columns may be added, existing ones not renamed or removed without agreement |
| **What happens on a breach** | Load stops; alert to both sides; previous data stays published |
| **Review** | Revisited every six months, or when the process changes |

### Contracts inside the warehouse

Contracts aren't only for files from outside. A dbt model that other models and dashboards read is a promise too, and dbt can enforce it. A **model contract** lists the model's columns and their types, and dbt refuses to build the model if its SQL no longer produces exactly those:

<!-- run: none -->
```yaml
  - name: stg_orders
    config:
      contract: {enforced: true}
    columns:
      - {name: order_id, data_type: integer}
      - {name: customer_id, data_type: integer}
      - {name: sales_rep_id, data_type: integer}
      - {name: order_date, data_type: date}
      - {name: status, data_type: varchar}
      - {name: is_counted, data_type: boolean}
```

`{…}` is YAML's way of writing a small map on one line: `{name: order_id, data_type: integer}` means the same as two lines, `name: order_id` and `data_type: integer`. With `enforced: true`, every column the model produces must be listed with its `data_type`. If someone renames `status` to `order_status` in `stg_orders.sql`, `dbt run` stops before replacing the model, with a table of the differences:

<!-- run: none -->
```
# terminal, in riverstone_dbt
$ dbt run --threads 1 --select stg_orders
04:16:15  1 of 1 ERROR creating sql view model dbt_dev_staging.stg_orders ................ [ERROR in 0.09s]
04:16:16    Compilation Error in model stg_orders (models/staging/stg_orders.sql)
  This model has an enforced contract that failed.
  Please ensure the name, data_type, and number of columns in your contract match the columns in your model's definition.
  
  | column_name  | definition_type | contract_type | mismatch_reason       |
  | ------------ | --------------- | ------------- | --------------------- |
  | order_status | TEXT            |               | missing in contract   |
  | status       |                 | TEXT          | missing in definition |
```

*(Trimmed: dbt also prints its setup lines, and the list of macros that raised the error.)* The rename is caught before any dashboard reads the new column name, which is exactly where a contract should catch it.

### Making contracts work with people

- **Write it with the producer, not at them.** The warehouse supervisor isn't trying to break your pipeline; they added a column because a manager asked for vehicle numbers.
- **Explain the cost of a surprise change** in their terms: "when the column changed, the dispatch report was unavailable for a day."
- **Make the safe path the obvious one:** adding columns is always allowed; renaming needs a note. Most breakages come from renames and type changes.
- **Version the contract,** and keep it in Git next to the pipeline code.
- **Contracts go both ways.** When your team publishes data others depend on (Chapter 51), you owe them the same promises.

---

## 47.8 Handling a data incident

When a check fails at 6:30 a.m., what happens next should be routine, not improvised.

![A five-step incident flow drawn as rows. Detect: a failed test, a stale table, or a person saying a number looks wrong. Classify: S1 wrong data reached people or systems; S2 an output is late or blocked and nothing wrong was sent; S3 a minor problem or a warning-level failure. Contain: stop publishing and syncs, and tell the people who use the data before they find out for themselves. Fix and verify: repair the cause, re-run the affected days, run the same tests, then publish. Review: a blameless write-up with the timeline, cause, impact, and the checks added to catch it sooner. A note says people forgive late data far more than wrong data they already acted on, so communication happens at step 3, not after step 4.](figures/fig47-2-data-incident-flow.svg)

*Figure 47.2 — A data incident, step by step. Communication happens before the fix, not after.*

**1. Detect.** From a failed test, a freshness alert, or a person. Treat "a manager says the number looks wrong" as an incident: it means detection failed.

**2. Classify.** Severity decides how much noise to make.

| Severity | Meaning | Riverstone example | Response |
|---|---|---|---|
| **S1** | Wrong data has reached people or another system | Wrong credit limits synced into the ERP; the Flash sent with wrong numbers | Immediate: tell recipients, correct, then fix |
| **S2** | A daily output is late or blocked; no wrong numbers went out | 5 January's Flash not published | Same morning; tell users the report is late |
| **S3** | A non-critical problem or a warning-level test failure | One dispatch row points at an unknown order | Next working day; fix in normal work |

**3. Contain.** Stop publishing and stop side effects: the blocked publish in section 47.4 is containment. Then tell the people who use the data, in their words: *"The Daily Sales Flash for 5 January is delayed. The order lines didn't load, so the numbers would have shown zero sales. Nothing has been sent. We expect it by 11:00."* People forgive late data far more than wrong data they acted on.

**4. Fix and verify.** Repair the cause, re-run the affected days (Chapter 46's partitions and idempotency), run the same tests, and publish. Section 47.9 does exactly this for 5 January, after the alert goes out. If wrong numbers did go out, send a labeled correction.

**5. Review.** A short write-up, within a few days, blameless and factual: what happened, the timeline, the cause, the impact, what was done, and what will stop it or catch it faster next time. For the 5 January incident, the review adds `orders_have_at_least_one_line` to the blocking audit before publishing (it existed as a data test, but didn't gate the Flash), plus a volume check for "zero new order lines on a day with new orders".

> **Real-life example: the missing piece in most incidents.** Teams usually fix the data and forget step 5. Six weeks later the same failure happens, and nobody remembers the fix. Ten minutes of writing, kept next to the runbook, is what turns an incident into an improvement.

---

## 47.9 Alerts people still read

Alerting fails in two directions: too few, and too many. **Alert fatigue** is what happens when a channel fills with messages nobody acts on, and the real one scrolls past.

### Grouping one incident into one message

A single failure usually trips several signals. Sending five messages makes it look like five problems. This function gathers the morning's real results, from the tests, the freshness checks, and the contract check, into one message:

```python
SEVERITY_MEANING = {"S1": "wrong data reached people or systems",
                    "S2": "a daily report is late or blocked; no wrong numbers were sent",
                    "S3": "a minor problem or a warning"}

def group_into_one_alert(day, test_results, freshness_results, contract_violations, severity="S2"):
    errors = [r for r in test_results if r["failing_rows"] and r["severity"] == "error"]
    warnings = [r for r in test_results if r["failing_rows"] and r["severity"] == "warn"]
    stale = [f"{table} ({hours:.0f} h old)"
             for table, hours, status in freshness_results if status == "STALE"]
    if not (errors or warnings or stale or contract_violations):
        return None
    lines = [f"DATA INCIDENT - {day} - Daily Sales Flash not published",
             f"Severity: {severity} ({SEVERITY_MEANING[severity]})", ""]
    if errors:
        lines.append("Failed tests (errors):")
        lines += [f"  - {r['name']}: {r['failing_rows']} failing row(s)" for r in errors]
    if warnings:
        lines.append("Warnings (not blocking):")
        lines += [f"  - {r['name']}: {r['failing_rows']} row(s)" for r in warnings]
    if stale:
        lines.append("Stale data: " + ", ".join(stale))
    if contract_violations:
        lines.append("Contract violations: " + "; ".join(contract_violations))
    lines += ["", "Impact: sales managers have no Flash for this day; mart.daily_flash is unchanged.",
              "Next step: fix the order-line load, re-run the day, and publish.",
              "Owner: data team on-call. Runbook: docs/runbooks/daily_flash.md"]
    return "\n".join(lines)

print(group_into_one_alert("2026-01-05", [], [], []))
```

```
None
```

The function is long, but it only collects and formats; there's no new idea in it. Called with nothing to report, as above, it returns `None`: no message at all is the right message on a good morning.

**How it works.**

- `SEVERITY_MEANING` is a dictionary from each severity to its meaning, so the message always explains itself. `severity="S2"` is the default, because a blocked Flash with nothing wrong sent is an S2 (section 47.8); an S1 would pass `severity="S1"`.
- The first three assignments sort the inputs: failed error tests, failed warnings, and the tables whose freshness status is `STALE`. `for table, hours, status in freshness_results` unpacks each tuple that `freshness_check()` returned in section 47.5, and `{hours:.0f}` rounds the age to whole hours.
- If there is something to report, it builds the message as a list of lines, adding each part only if it has something in it, and `"\n".join(lines)` joins them with line breaks into one text.

Now call it with the morning's real results:

```python
test_results = run_tests(TESTS) + run_tests(AUDIT_TESTS)
alert = group_into_one_alert("2026-01-05", test_results, freshness,
                             check_contract("exports/dispatch_2026-01-05.csv", DISPATCH_CONTRACT))
print()
print(alert)
```

```
orders_unique_key              PASS   failing rows: 0
orders_customer_not_null       PASS   failing rows: 0
orders_status_accepted         PASS   failing rows: 0
order_items_have_an_order      PASS   failing rows: 0
order_items_quantity_positive  PASS   failing rows: 0
orders_have_at_least_one_line  ERROR  failing rows: 1  e.g. [(10178,)]
dispatch_order_known           PASS   failing rows: 0

7 tests, 6 passed, 1 failed as errors, 0 warnings
flash_one_row               PASS   failing rows: 0
flash_revenue_not_negative  PASS   failing rows: 0
flash_matches_erp           ERROR  failing rows: 1  e.g. [(0, 1, Decimal('0.00'), Decimal('18750.00'))]

3 tests, 2 passed, 1 failed as errors, 0 warnings

DATA INCIDENT - 2026-01-05 - Daily Sales Flash not published
Severity: S2 (a daily report is late or blocked; no wrong numbers were sent)

Failed tests (errors):
  - orders_have_at_least_one_line: 1 failing row(s)
  - flash_matches_erp: 1 failing row(s)
Stale data: raw.dispatch (102 h old), mart.daily_flash (102 h old)
Contract violations: missing column: qty_units; undeclared column: units; undeclared column: vehicle_no

Impact: sales managers have no Flash for this day; mart.daily_flash is unchanged.
Next step: fix the order-line load, re-run the day, and publish.
Owner: data team on-call. Runbook: docs/runbooks/daily_flash.md
```

**How it works.** `run_tests(TESTS) + run_tests(AUDIT_TESTS)` runs both suites against the warehouse as it stands on 5 January and adds the two lists of results together. `freshness` is the list of results from section 47.5, and the contract violations come straight from `check_contract()` in section 47.7.

**Reading it.** One message: both failed tests, the two stale tables, the contract violation, the impact, the next step, the owner, and the runbook. `flash_matches_erp` is the test that blocked publishing; `orders_have_at_least_one_line` points at the cause, order 10178 with no lines. In a real deployment this goes to the on-call channel and, for an S1, to the people who received wrong numbers.

The run groups everything into one message, but not everything in it has the same owner. The contract breach is also sent, as a separate message, to its owner, `DISPATCH_CONTRACT["owner"]`, the Bhiwandi Main supervisor: it happened on the same morning as the Flash incident, but it has a different cause.

### Closing the incident: fix, verify, publish

The alert's next step is the fix. The order-line bug is repaired (in the companion, by switching the simulated bug off), the day is re-run, and write–audit–publish decides whether it's now safe to publish:

```python
ingest.BROKEN_ITEMS_SYNC = False                # the order-line bug is fixed
print("order lines (new, changed, deleted):", ingest.sync_table(wh, "order_items"))
publish_flash("2026-01-05")
print("mart.daily_flash:", wh.execute("SELECT * FROM mart.daily_flash ORDER BY flash_date").fetchall())
flash_freshness = freshness_check("mart.daily_flash", "flash_date")
```

```
order lines (new, changed, deleted): (1, 0, 0)
--- write-audit-publish for 2026-01-05 ---
flash_one_row               PASS   failing rows: 0
flash_revenue_not_negative  PASS   failing rows: 0
flash_matches_erp           PASS   failing rows: 0

3 tests, 3 passed, 0 failed as errors, 0 warnings
PUBLISHED
mart.daily_flash: [(datetime.date(2026, 1, 2), 2, Decimal('38710.00')), (datetime.date(2026, 1, 5), 1, Decimal('18750.00'))]
mart.daily_flash  newest 2026-01-05  expected 2026-01-05  age  30.5 h  PASS
```

**Reading it.** The re-run load found the one missing order line (order 10178's line 334). The same three audit tests now pass, so the day was published: 1 order for ₹18,750.00, the same numbers Chapter 46's fixed re-run produced. The published table's freshness check passes again. That's step 4 of section 47.8: repair, re-run, verify with the same tests, publish. The dispatch file is still waiting for the warehouse supervisor to confirm the rename, which is the contract conversation, not the data team's fix.

### Rules that keep alerts useful

- **One incident, one alert.** Group by run and by root cause, as above.
- **Only alert on things someone will do something about.** Everything else goes on a dashboard and is reviewed weekly.
- **Route by owner.** The dispatch contract breach belongs to the warehouse team, not the whole data channel.
- **Say what to do.** Every alert names the next step and links a runbook.
- **Suppress repeats.** While an incident is open, don't re-send the same alert every 15 minutes.
- **Review noisy alerts monthly.** Any alert that fired more than a few times without action is fixed, downgraded, or deleted.
- **Alert on the absence of runs**, not only on failures, or a pipeline that never starts goes unnoticed.

---

## 47.10 The tools landscape

Everything in this chapter is SQL, Python, and habits, which is why it works anywhere. Tools add scheduling, history, reporting, and someone else's maintenance.

| Tool | What it is | Strengths | Watch for |
|---|---|---|---|
| **dbt tests** | Tests declared next to your models (47.3) | Free with dbt; runs where your models run; version-controlled; most tests in one line | Only covers data dbt builds; results need somewhere to live |
| **Great Expectations** | A Python library of "expectations" with data docs | Large library of checks; profiling; readable reports | Heavier to set up; the API has changed a lot between versions |
| **Soda** | Checks written as YAML contracts, run by a command-line tool or a Python library | Readable checks; works across warehouses; hosted option | Another service to run; advanced features are paid |
| **Observability platforms** (for example Monte Carlo, Metaplane, Elementary) | Monitor freshness, volume, schema, and lineage automatically | Little to write; anomaly detection and lineage out of the box | Cost; alerts you didn't design; still needs owners |
| **Orchestrator checks** (Dagster asset checks, Airflow tasks) | Checks attached to pipeline steps (Chapter 46) | Naturally blocking; visible with the run | Not a full test library on their own |
| **Warehouse constraints** | Primary keys, not-null, foreign keys in the database | Stops bad data being written at all | Support varies by warehouse; some are declarative only |

A practical combination for a team Riverstone's size: **dbt tests** for the models, **orchestrator checks** for the blocking ones before delivery, **a few freshness and volume monitors**, and **contracts** with the two or three sources that break most often. Add a platform when the number of tables outgrows the team's attention.

### Optional: the same rule in Great Expectations and Soda

To see how the two libraries differ from this chapter's failing-rows tests, run one rule, "status is one of the four agreed values", in each. Both are optional installs, into the same virtual environment:

<!-- run: none -->
```
# terminal
$ python -m pip install great_expectations==1.23.2 soda-duckdb==4.25.0
```

`great_expectations` is Great Expectations; `soda-duckdb` is Soda's library with its DuckDB connector. The versions are the ones used for the outputs below. Both change often, and Great Expectations' current API (version 1) differs a lot from the version 0 code you'll still find online, so check the documentation for your version. Add both to `requirements.txt` if you keep them.

First, break the rule again, so there's something to find:

```python
wh.execute("UPDATE raw.orders SET status = 'On Hold' WHERE order_id = 10177")   # a status nobody agreed
on_hold = wh.execute("SELECT COUNT(*) FROM raw.orders WHERE status = 'On Hold'").fetchone()[0]
print("orders on hold:", on_hold)
```

```
orders on hold: 1
```

**Great Expectations** checks a table you hand it, here as a pandas DataFrame (Chapter 18):

<!-- run: none -->
```python
import great_expectations as gx

orders = wh.execute("SELECT order_id, status FROM raw.orders").df()
context = gx.get_context(mode="ephemeral")
batch = (context.data_sources.add_pandas("warehouse")
         .add_dataframe_asset("raw_orders")
         .add_batch_definition_whole_dataframe("all rows")
         .get_batch(batch_parameters={"dataframe": orders}))
rule = gx.expectations.ExpectColumnValuesToBeInSet(
    column="status", value_set=["Pending", "Shipped", "Delivered", "Cancelled"])
result = batch.validate(rule)
print("success:", result.success)
print("rows checked:", result.result["element_count"],
      "| unexpected:", result.result["unexpected_count"],
      f"({result.result['unexpected_percent']:.2f}%)",
      "| examples:", result.result["partial_unexpected_list"])
```

```
success: False
rows checked: 178 | unexpected: 1 (0.56%) | examples: ['On Hold']
```

**How it works.**

- `.df()` turns a DuckDB result into a pandas DataFrame.
- `gx.get_context(mode="ephemeral")` starts Great Expectations without creating any project files; its settings live only in memory.
- The chain of four calls tells it where the data comes from: a pandas **data source**, a DataFrame **asset**, a **batch definition** that takes the whole DataFrame, and a **batch**, the actual rows for this run, passed in as `batch_parameters`.
- `ExpectColumnValuesToBeInSet` is an **expectation**, Great Expectations' word for a rule: every value in `status` should be in `value_set`.
- `batch.validate(rule)` runs it. `result.success` is the verdict, and `result.result` holds the measurements. While it works, Great Expectations shows a progress bar ("Calculating Metrics"); that isn't part of the printed output.

**Soda** reads a contract written in YAML, and connects to the warehouse itself. The companion folder has two small files. `soda/warehouse.yml` says where the data is:

<!-- run: none -->
```yaml
type: duckdb
name: riverstone_wh
connection:
  database: warehouse/riverstone_wh.duckdb
```

and `soda/orders_contract.yml` says what the table promises:

<!-- run: none -->
```yaml
dataset: riverstone_wh/raw/orders
columns:
  - name: order_id
    checks:
      - missing:
      - duplicate:
  - name: status
    checks:
      - invalid:
          valid_values: [Pending, Shipped, Delivered, Cancelled]
```

`dataset:` names the table as data source / schema / table. Each column lists its **checks**: `missing` (no blanks), `duplicate` (no repeats), and `invalid` with the allowed values. Now verify the contract:

<!-- run: none -->
```python
from soda_core.contracts import verify_contract_locally

check = verify_contract_locally(data_source_file_path="soda/warehouse.yml",
                                contract_file_path="soda/orders_contract.yml")
for r in check.contract_verification_results[0].check_results:
    counts = {k: v for k, v in r.diagnostic_metric_values.items() if k.endswith("_count")}
    print(f"{r.check.name:<20} {r.outcome.name:<7} {counts}")
```

```
No missing values    PASSED  {'missing_count': 0}
No duplicate values  PASSED  {'duplicate_count': 0, 'missing_count': 0}
No invalid values    FAILED  {'invalid_count': 1, 'missing_count': 0}
```

**How it works.** `verify_contract_locally()` connects to the warehouse file named in `data_source_file_path`, runs every check in the contract file named in `contract_file_path`, and returns the results. "Locally" means on your computer, rather than on Soda's hosted service. There's one contract here, so `contract_verification_results[0]` is its result, and `check_results` has one entry per check. Each has a name, an outcome (`PASSED` or `FAILED`), and the measurements behind it in `diagnostic_metric_values`, a dictionary. The dictionary comprehension (Chapter 17, section 17.7) keeps only the counts; the full dictionary also has percentages and the number of rows tested, 178. (Soda sends anonymous usage data by default; setting the environment variable `SODA_CORE_TELEMETRY_ENABLED` to `false` before starting Jupyter turns that off.)

**Reading it.** Both tools found the one order on hold. Notice *how* they report it. `data_test()` returns the failing rows. Great Expectations and Soda return **measurements**: a count and a percentage of values that break the rule, with a few examples. It's the same rule, expressed as a metric, and a metric is what lets these tools keep a history, draw a trend, or pass a check while a small percentage fails. Which style to use is a team's choice; the rule itself, written down and tested on every load, is what matters.

Put the order back before you go on:

```python
print("orders (new, changed, deleted):", ingest.sync_table(wh, "orders"))
```

```
orders (new, changed, deleted): (0, 1, 0)
```

The hash comparison found the one changed order and set its status back to the ERP's value.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Testing only that the pipeline ran | Green runs, wrong numbers | Test the data, not only the job (47.2) |
| Publishing first and checking after | Wrong rows visible while you investigate | Write–audit–publish (47.4) |
| Every test an error | Pipelines blocked by trivia; people disable tests | Severity per test; warnings for edges (47.2) |
| Tests that have never failed | False confidence | Break things on purpose and watch them fail (47.3) |
| No freshness monitoring | Dashboards quietly show last week | Monitor age of newest data per table (47.5) |
| Baselines learned from broken days | "Normal" drifts toward broken | Exclude failed days; use medians over longer windows |
| Treating unusual as wrong | Blocked pipelines on genuine big sales days | Anomalies warn; only hard rules block (47.5) |
| A missing day that looks like a zero day | Charts show a dip that never happened | Publish load status alongside data (47.4) |
| No lineage | "Is anything else affected?" takes hours | Declare dependencies; use the orchestrator graph (47.6) |
| Contracts as documents nobody checks | Same breakage every quarter | Check the contract in the pipeline (47.7) |
| Blaming the source's owner | Cooperation stops; surprises continue | Make the safe path the obvious one; explain impact in their terms |
| Fixing without telling users | People act on numbers they didn't know were wrong | Communicate at containment, before the fix (47.8) |
| Skipping the review | The same incident twice | Ten-minute blameless write-up, kept with the runbook |
| One alert per failed signal | Five messages for one problem; fatigue | Group by incident; route by owner (47.9) |
| Alerting on everything | The channel becomes noise | Alert only what someone will act on; review monthly |

---

## In the real world: the dashboard that was right but late

Riverstone's sales dashboard had been correct for months, so when Vikram opened it on a Thursday to prepare for a customer call, he didn't check the date on it. He told the customer their last order had been in November.

It had been in January. The dashboard was showing data that stopped on 4 January, four days earlier.

Meera traced it in twenty minutes. On the Monday, a change in the warehouse had renamed a column in the staging model. The nightly pipeline's transformation step had failed at 2:10 a.m. That failure had sent an alert, exactly as designed, into the data team's channel, where it sat among the eleven other messages the pipeline sent every night: three warnings about dispatch rows with unknown orders, a note about API retries, a long "run finished" message, and a nightly summary nobody read. The failure was message seven.

Meanwhile, every test that ran was green, because the tests all ran against tables that had stopped being updated. Their data was perfectly consistent, and three days old.

The fixes were small, and they're the ones in this chapter.

- **Freshness checks on the tables people read,** not only tests on their contents. The dashboard's own table now fails a check if its newest day is older than the previous working day.
- **Fewer alerts, better routed.** Successes stopped being announced. Warnings moved to a weekly digest. Failures went to the on-call person with a subject line naming the table and the impact.
- **A status banner on the dashboard,** driven by the load status table: "Data current to 7 January, 6:35 a.m." Vikram's habit of glancing at the top-right corner now catches in one second what took three days.
- **A contract conversation** with the analytics engineer who had renamed the column, agreeing that renames in shared models need a note and a deprecation window, exactly as for external sources.

At the next sales review, Anita asked whether the data was reliable now. "It fails more often than it used to," Meera said. "That's the point. When it's wrong, it stops and tells us, instead of looking right."

**What made this work.**

- **They monitored freshness, not only correctness.** The data was correct; that was never the problem.
- **They treated alert noise as a real defect**, because it's what hid the failure.
- **They put the status where the users look**, so trust didn't depend on the data team noticing first.
- **They applied contracts internally**, where most surprise changes actually come from.

---

## Project: quality, monitoring, and a contract for the Riverstone pipeline

**Goal:** make the Chapter 46 pipeline trustworthy: nothing wrong gets published, staleness is noticed, one incident produces one useful alert, and the dispatch file has a contract that's checked automatically.

### Tools you'll need

- **Python** 3.14 in the virtual environment from Chapter 17, with `duckdb` and `psycopg2` (Chapter 45, section 45.2); **PostgreSQL 16**; **Jupyter**; the **Chapter 47 companion folder** (`companion/ch47/`), which is Chapter 46's environment without Dagster, plus `reset_ch47.py` and the two Soda files. Open your notebook in that folder.
- **No data quality product needed:** every test in the main thread is SQL run from Python.
- **Optional:** `great_expectations` and `soda-duckdb` (section 47.10), and your Chapter 32 dbt project for the dbt tests and the model contract.
- **Versions used for the outputs shown:** Python 3.11.15, DuckDB 1.5.6, psycopg2 2.9.13, PostgreSQL 16.13, Great Expectations 1.23.2, Soda Core 4.25.0, dbt Core 1.12.5 with dbt-postgres 1.11.0 and dbt_utils 1.4.1, on 29 September 2026. Your Python 3.14 environment gives the same outputs.

**Option A: Riverstone.** Extend your Chapter 46 pipeline.

**Option B: your own pipeline.** Apply the same layers to a report you produce, using data you're allowed to use.

**Steps**

1. **Write the specification** for two tables: what "good" means, in sentences, for at least four dimensions from section 47.1.
2. **Build a test suite** of at least ten tests across raw, staging, and mart, each with a severity and a one-line description.
3. **Break each rule on purpose** and confirm every test fails when it should. Note any test that didn't catch what you expected.
4. **Convert the pipeline to write–audit–publish** for the Flash, and prove a failing day leaves the published table untouched.
5. **Add freshness checks** for every table people read, with limits based on the promise to users, and a `load_status` table the dashboard can show.
6. **Add two volume checks:** zero rows on a working day (error), and a wide band around the median of recent days (warning).
7. **Add lineage:** list, for each source, which outputs it affects, and use it in your alert text.
8. **Write a data contract** for the dispatch file with the warehouse team's view in mind, and check it in the pipeline.
9. **Run an incident:** break the pipeline, produce one grouped alert, write the user-facing message, fix, re-run, and write the review (half a page).
10. **Count your alerts.** Over a week of runs, how many messages would a person receive? If it's more than a handful, cut them.

**Stretch goals**

- Store every test result in a `test_results` table with the run and day, and chart pass rates over time.
- Add a check that compares this week's revenue by segment with last week's and warns on large shifts.
- Write the same tests as dbt tests and run both, comparing effort and output.

---

## Recap

- Data quality has **dimensions**: accuracy, completeness, validity, uniqueness, consistency, and timeliness. Each becomes a test.
- A **data test** is a query that returns the rows that break a rule; zero rows means it passed. dbt's tests compile to exactly these queries; Great Expectations and Soda report the same rule as a measurement, a count of the values that break it.
- **Severity** decides what stops a pipeline. Warnings are for edges; errors are for numbers people act on. Tests nobody acts on should be fixed, downgraded, or deleted.
- Tests belong at every layer: structure in **raw**, validity and consistency in **staging**, business rules and reconciliation in **mart**, and blocking checks **before delivery**.
- **Break your tests on purpose.** A suite that has never failed hasn't been tested.
- **Write–audit–publish** keeps failed data out of the tables people read; the same 5 January failure that left a wrong row in Chapter 46 now leaves the published table untouched.
- **Observability** answers three questions: did it run, is it **fresh**, does its **volume** look normal. Stale data is one of the most common incidents, and the least noticed. Freshness is judged against the promise to users, such as "yesterday's working day is loaded by 6:30", not a fixed number of hours.
- **Unusual is not wrong.** Anomalies warn; only hard rules block.
- **Lineage** tells you what a broken table affects, and where a wrong number could come from.
- **Data contracts** state fields, rules, delivery, change notice, and what happens on a breach, and are checked in the pipeline: columns and values. They apply to internal producers too, where dbt's model contracts enforce them.
- **Incidents** follow detect, classify, contain, fix and verify, review. Tell users at containment, before the fix.
- **Alert fatigue** hides real failures: one incident, one alert; route by owner; alert only what someone will act on.

---

## Key terms

data quality dimensions (accuracy, completeness, validity, uniqueness, consistency, timeliness) · data test · failing rows · severity (error, warning) · raw, staging, mart layers · reconciliation · anti-join · foreign key · self-healing load · dbt test · singular test · write–audit–publish (WAP) · audit schema · cross join · floating-point comparison · publish swap · blue/green tables · load status · observability · freshness · previous working day · staleness limit · volume check · baseline · median · anomaly · lineage · column-level lineage · impact analysis · data contract · model contract · change notice · breach · data incident · severity levels (S1, S2, S3) · containment · blameless review · alert fatigue · alert grouping · runbook · expectation (Great Expectations) · check (Soda)

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can name the six data quality dimensions and write a test for each on Riverstone data.
- [ ] You can explain why a data test is "a query that returns the rows that break the rule".
- [ ] You can choose error or warning severity for a test, and defend the choice.
- [ ] You can say which checks belong in raw, staging, mart, and before delivery.
- [ ] You can break a rule on purpose and show the test catching it.
- [ ] You can implement write–audit–publish and prove readers never see failed data.
- [ ] You can explain why a re-run repairs a table loaded by hash comparison.
- [ ] You can set freshness limits from a promise to users, and explain why stale data is the hardest failure to notice.
- [ ] You can build a volume baseline with a median, and explain why unusual is not the same as wrong.
- [ ] You can use lineage to say who is affected by a broken table.
- [ ] You can write a data contract and check it automatically.
- [ ] You can classify an incident's severity, write the user-facing message, and run the review.
- [ ] You can group one incident into one alert and explain three rules that prevent alert fatigue.
- [ ] You can write the same rule as a dbt test, a Great Expectations expectation, and a Soda check, and say how their results differ.
- [ ] You can recommend a starting set of tools for a small data team.

---

## Exercises

Run `reset()` and re-run the setup and test blocks before each exercise that uses the companion environment.

### Warm-up

1. Name the data quality dimension each rule belongs to: (a) every order line points at an order that exists; (b) `status` is one of four values; (c) yesterday's orders are loaded by 6:30 a.m.; (d) the warehouse's revenue for a day equals the ERP's; (e) one row per order.
2. Write the failing-rows query for: (a) duplicate `dispatch_id` values in `raw.dispatch`; (b) orders with a `sales_rep_id` that doesn't exist in a `raw.employees` table.
3. For each, choose error or warning and give a reason: (a) revenue doesn't match the ERP; (b) a dispatch row points at an unknown order; (c) a customer's email is missing; (d) `mart.daily_flash` has two rows for one day.

### Core

4. Add a test `flash_revenue_matches_lines` that fails when a published Flash row's revenue doesn't equal the revenue recomputed from `raw.orders` and `raw.order_items` for that day. Would this have caught the 5 January failure? Would it have caught a wrong *discount* in the source?
5. In section 47.3 the ERP refused the orphan order line, and the warehouse accepted it. Explain why, and say what you'd add to the warehouse to make it refuse too. What's the trade-off of adding it?
6. After the `resync` block, all seven tests pass again. Explain, in terms of Chapter 45's hash comparison, why re-running the load repaired the warehouse. Which of the three broken things would a load with an ID watermark have repaired?
7. The freshness check flagged `mart.daily_flash` as stale at 6:30 a.m. on 6 January. Write the user-facing message the sales team should receive, in three sentences.
8. Set freshness limits for: (a) `raw.orders`; (b) `raw.dispatch`; (c) `raw.crm_leads`, given the Flash is promised by 7:30 a.m. IST on working days, the dispatch file is due at 20:00 IST daily, and lead figures are used in a Monday report. State your assumption about weekends.
9. Using the 2025 numbers in section 47.5 (median ₹27,442.50, 131 days with orders), design two volume rules: one error and one warning. Say what each would have done on 16 November 2025 (₹175,895.00) and on a day the load brought in nothing.

### Stretch

10. Design the `load_status` table mentioned in section 47.4: columns, one row per what, and how a dashboard would use it to show "data current to…". Include how it distinguishes "not published yet", "published", and "failed".
11. Write the full dispatch data contract as a document the warehouse supervisor would accept: fields, rules, delivery, change process, breach handling, review. Then list the three checks you'd automate first, and why those three.
12. An analytics engineer renames a column in a shared staging model, breaking two downstream reports. Design an internal contract process for shared models: what's promised, how changes are announced, how long the old name survives, and how the pipeline enforces it.

### Think about it (no code needed)

13. Riverstone's pipeline now fails more often than it used to, because it stops when data is wrong. Write the paragraph you'd use to explain to Anita why that's an improvement, and what you'd show her each month to prove it.
14. Which is worse: a wrong number delivered on time, or no number at all? Argue both sides using examples from this chapter, then say what design choice follows from your answer.

---

## Answers

**1.** (a) Consistency (a relationship between tables). (b) Validity. (c) Timeliness. (d) Accuracy. (e) Uniqueness. Completeness would cover "every order has a customer".

**2.** Sample answers:

```sql
-- (a) duplicate dispatch_id
SELECT dispatch_id, COUNT(*) AS n
FROM raw.dispatch
GROUP BY dispatch_id
HAVING COUNT(*) > 1;

-- (b) orders whose sales rep is unknown
SELECT o.order_id, o.sales_rep_id
FROM raw.orders AS o
LEFT JOIN raw.employees AS e ON e.employee_id = o.sales_rep_id
WHERE o.sales_rep_id IS NOT NULL AND e.employee_id IS NULL;
```

Both follow the rule: return the rows that break the rule, so zero rows means the test passed. In (b), the `IS NOT NULL` keeps "no rep assigned" out of this test; that's a separate completeness rule.

**3.** (a) **Error**: the Flash would mislead the sales team. (b) **Warning**: a dispatch may legitimately arrive before its order is loaded, and holding the Flash for it would be worse than publishing. (c) **Warning** in most cases: a missing email doesn't make the sales numbers wrong, though it would be an error for a table that feeds an email campaign. (d) **Error**: duplicate rows double revenue, and it signals a non-idempotent step.

**4.** A sample test:

<!-- run: none -->

```python
data_test("flash_revenue_matches_lines", """
    SELECT f.flash_date, f.revenue_booked, COALESCE(c.revenue, 0) AS recomputed
    FROM mart.daily_flash AS f
    LEFT JOIN (
        SELECT o.order_date, SUM(i.quantity * i.unit_price * (1 - i.discount_pct / 100)) AS revenue
        FROM raw.orders AS o JOIN raw.order_items AS i ON i.order_id = o.order_id
        WHERE o.status <> 'Cancelled' GROUP BY o.order_date) AS c
      ON c.order_date = f.flash_date
    WHERE f.revenue_booked <> CAST(ROUND(COALESCE(c.revenue, 0), 2) AS DECIMAL(12,2))""")
```

The recomputed revenue is rounded to the paisa and made an exact decimal before the comparison, for the reason in section 47.4: the raw sum is a floating-point number. It would **not** have caught the 5 January failure on its own: the Flash was built *from* those same warehouse tables, so both sides would have agreed on ₹0. That's why the reconciliation test compares with the **ERP**, not with the warehouse. (The `LEFT JOIN` keeps a published day even if no lines are found for it, and `COALESCE` turns that missing revenue into 0, so such a day fails the test.) It also would **not** catch a wrong discount in the source, for the same reason: the warehouse faithfully copies the source's mistake. It's still useful, because it catches a wrong transformation, publishing the wrong day, or a stale Flash row.

**5.** The ERP has a **foreign key** on `order_items.order_id`, so the database itself refuses a line whose order doesn't exist. The warehouse table has no such constraint, so it accepted the row. You could add one in DuckDB or your warehouse where supported. In DuckDB a foreign key must be declared when the table is created (`order_id INTEGER REFERENCES raw.orders(order_id)`); it can't be added to an existing table with `ALTER TABLE`, so the raw tables would have to be created again. The trade-offs: constraints are checked on every write, which slows large loads; they force load *order* (orders before lines) and make partial loads fail rather than land; and many cloud warehouses don't enforce them at all, which is why data tests exist. A common compromise is a primary key on raw tables (Chapter 45's idempotency needs it) plus relationship tests instead of enforced foreign keys.

**6.** The hash comparison builds the full picture of what the source contains and makes the warehouse match it: rows in the warehouse but not the source are **deleted**, and rows whose values differ are **updated**. The two invented order lines existed nowhere in the source, so they were deleted; order 10177's status differed, so it was updated back to the source's value. An **ID watermark** load would have repaired **none of them**: it only inserts rows with IDs above the watermark, so it never deletes and never updates. That's Chapter 45's lesson again, now visible as a data quality property.

**7.** A sample message: *"The Daily Sales Flash for 5 January hasn't been published. Yesterday's order lines didn't load, so today's figures would have shown no sales, which would be wrong. We're fixing the load now and expect the Flash by 11:00; the dashboard still shows data up to 2 January."* Three things make it good: no jargon, the reason the report was held, and when to expect it.

**8.** Assumption: orders can arrive on any day (2025 had big Sunday orders: 16 and 9 November), but the Flash is promised only on working days, and the checks run at 6:30 a.m. (a) `raw.orders`: on a working-day run, the newest `order_date` must be on or after the previous working day. In hours, that's 30.5 hours on Tuesday to Friday (a date counts from midnight) and 78.5 hours on a Monday, so an hour limit needs about 32 and 80. (b) `raw.dispatch`: the file for day D is due at 20:00 on D, so at the next 6:30 run the newest `file_day` must be on or after D, the previous working day; check it only after working days. (c) `raw.crm_leads`: the Monday report needs last Friday's leads by Monday at 6:30 (78.5 hours, so about 80); make it an error on Monday mornings and a warning on other days. Any answer is acceptable if the limit comes from a promise and the weekend assumption is stated.

**9.** **Error rule:** on a working day, the day's booked revenue is **zero** while the ERP has orders for that day, or the published revenue is negative. On 16 November this does nothing (₹175,895.00 is not zero); on the day the load brought nothing, it fires and blocks publishing. **Warning rule:** the day's revenue is below **a quarter** of the recent median (₹6,860) or above **five times** it (₹137,212). On 16 November this warns, and a human confirms that a genuinely large order arrived; on the empty-load day the error rule has already blocked it. Using three times the median as an *error* would have blocked ten legitimate days in 2025, which is exactly the mistake section 47.5 warns against.

**10.** A sample design: one row per **table and day** (or per published partition): `table_name`, `business_date`, `status` (`pending`, `published`, `failed`, `late`), `run_id`, `published_at`, `rows`, `failed_tests`, `note`. The pipeline inserts `pending` when a run starts, updates to `published` after a successful publish, and `failed` when the audit blocks it; a separate freshness monitor marks a `pending` row `late` when it passes its deadline. A dashboard reads the latest `published` row for its table to show "Data current to 7 January, 6:35 a.m.", and shows an amber banner when today's status is `late` or `failed`. The important part is that "we have no data for today" is a *recorded state*, not an absence, so charts can show it instead of drawing a zero.

**11.** A good answer covers: **dataset and purpose** (daily dispatch sheet, feeds the dispatch report used by customer service); **fields** with types, meanings, and whether blanks are allowed, including that `qty_units` may be blank while a count is pending; **rules** (`dispatch_id` unique, `order_id` exists in the ERP, quantities whole numbers, date as dd-mm-yyyy); **delivery** (one file per working day by 20:00 IST, named `dispatch_YYYY-MM-DD.csv`, in the shared folder); **change process** (new columns allowed any time; renames, removals, and type changes need 10 working days' notice and a quick call); **breach handling** (load stops, both sides alerted, previous data stays published, the day is loaded once corrected); **review** every six months; **contacts** on both sides. The three checks to automate first: (1) **columns match the contract**, because renames caused the last two breakages; (2) **file arrived by the deadline**, because a missing file is the most common and least visible failure; (3) **`dispatch_id` unique**, because duplicates silently double dispatched quantities. Each is cheap and catches a failure that has already happened.

**12.** A workable internal process: shared models are **owned** by a named person, and their column names are treated as an interface. Changes are announced in the data channel and in the model's documentation, with the reason. A rename is done as **add, then deprecate**: the new column is added alongside the old one, the old one is marked deprecated with a removal date at least two weeks out, consumers are told which reports use it (from lineage), and only then is it removed. Enforcement lives in the pipeline: a test asserts that every column listed in the model's contract file still exists, so a removal without a contract change fails in the pull request, not at 6:30 a.m. dbt's model contracts (section 47.7) and Chapter 29's code review make this routine rather than personal.

**13.** A sample paragraph: *"The pipeline stops more often because we added checks that compare our numbers with the ERP before anything is published. When it stops, the old numbers stay up and you get a message telling you what's late and when to expect it. Before, the same problems still happened; we published them, and someone found out in a meeting. What I'd like to show you each month: how many times we stopped publication and why, how many wrong numbers reached anyone (the number I want at zero), and how long it took us to publish after a problem. If the first number is high and the second is zero, the system is working."* The key move is to reframe visible failures as caught failures, with metrics that separate the two.

**14.** *A wrong number on time is worse* in most business settings: people act on it, decisions are made, and the error spreads into other systems and into trust, as the Chapter 46 story of duplicate emails showed. *No number is worse* when a decision must be made at a fixed time and a rough figure would be better than nothing, for example a dispatch cut-off, or where the absence itself misleads (a chart showing zero sales). The design that follows from the first view is this chapter's: block publication, keep the last good data, tell people, and fix. The design that follows from the second is to publish with an explicit, visible warning about what's missing or provisional, so people can decide for themselves. A good answer picks one and names the conditions where it would switch.

---

## Where this leads

- **Chapter 48, Big Data & Distributed Compute,** scales the pipeline's heavy steps, where tests must run on far more data than fits in memory.
- **Chapter 49, Storage, Warehouses & Lakehouses,** provides the transactions, snapshots, and time travel that make publishing and rollback quick.
- **Chapter 50, Streaming & Real-Time,** asks how to check data that never stops arriving.
- **Chapter 51, Data Activation,** sends warehouse data into the CRM and ERP, where an S1 incident means wrong data in a business system, not only a wrong chart.
- **Chapter 32** covers dbt models, tests, and documentation; **Chapter 14** covers the analyst-level version of this work.
- **Chapter 64, Security, Privacy, Governance & Responsible AI,** covers ownership, stewardship, and the governance that data contracts sit inside.
- **Part 8:** data quality and incident questions appear in the data engineering interview chapters, and "walk me through a wrong dashboard" is a standard system design question (Chapter 77).
