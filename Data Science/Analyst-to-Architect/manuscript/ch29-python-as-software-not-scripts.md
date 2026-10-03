# Chapter 29. Python as Software, Not Scripts

*Part 3 — Advanced Analytics & Analytics Engineering*

> **Chapter at a glance**
>
> **You will learn to:** recognize the signs that a script has outgrown being a script · split a script into small functions and modules with one job each · lay out a project with `src/`, `tests/`, and `pyproject.toml` · keep passwords and settings out of code · create reproducible environments with `venv`, pinned requirements, and a lockfile managed by `uv` · write small classes and data classes, and know when not to · add type hints and let `mypy` find bugs before users do · write fast, focused tests with `pytest`, fixtures, and parametrized cases, and run them on every push · raise meaningful exceptions and log instead of printing · build an API client that handles pagination, timeouts, retries, and rate limits · review code, and have your code reviewed, with a checklist.
>
> **Before you start:** Chapter 17 (functions, files, errors, packages), Chapter 18 (pandas and the monthly report), Chapter 34 (the terminal, environment variables, exit codes), Chapter 12 (connecting to PostgreSQL), Chapter 2 (what an API is), and Chapter 26 (Git, pull requests, and the automated check of section 26.8).
>
> **Time needed:** 20–24 hours of reading and practice, over three weeks, in four sittings marked "Stop here": sections 29.1–29.3 (about 5 hours), 29.4–29.6 (5 hours), 29.7–29.8 (6 hours), and 29.9–29.10 with the project (6–8 hours). Classes, type hints, a lockfile, and a test framework are all new here, so type the examples rather than reading them.
>
> **Tools:** Python 3.14 (Chapter 17), `uv` (section 29.4), VS Code with its Python and Jupyter extensions, and the `riverstone_2025` database from Chapter 13.
>
> **Practice data:** the companion folder `ch29/`: the starting script `start/monthly_report.py`, the finished package `riverstone-report/`, and a local mock CRM API, `mock_crm_api.py`, with 43 leads. Every command was run, and every output shown is real.

---

## Why this matters

Riverstone's monthly report still runs from Imran's original script, the one that Chapter 18's version was written to replace. It pulls December's sales, adds them up, and writes a workbook. Then this happens:

- *"Can Priya run it while you're on leave?"* It needs your password, your folder, and the exact versions of pandas on your laptop.
- *"The January report says revenue was zero."* The script found no data, wrote a report full of zeros anyway, printed `done`, and overwrote December's file.
- *"Can we also pull leads from the CRM?"* The CRM's API returns 10 leads per page, sometimes fails, and blocks you if you ask too often.
- *"Finance changed the revenue rule. Did anything break?"* Nobody knows until someone reads every number.

If you finished Chapter 18, your own script already fixes part of this: its password is in `.env`, its SQL uses parameters, it logs, and it returns an exit code. This chapter goes the rest of the way.

None of these are problems with Python. They're problems with treating code that a business depends on as a one-off script. This chapter turns the report into **software**: code that someone else can install, run, understand, change, and trust. The techniques are the everyday habits of data engineers and analytics engineers, and the questions interviewers use to tell them apart from people who have only written notebooks: *"How do you structure a Python project?"*, *"How would you test this function?"*, *"What happens when the API returns a 429?"*

---

## In plain English

**A script is a recipe scribbled on the back of an envelope. Software is a restaurant kitchen.**

The envelope works when you cook alone. It says "a handful of salt" because you know your hand. It lists the steps in one long paragraph. If the shop is out of an ingredient, you improvise. Nobody else could cook from it.

A restaurant kitchen is built so that any trained cook can produce the same dish every night:

- The work is divided into **stations**: one prepares vegetables, one grills, one plates. Each has one job. In code, these are **functions** and **modules**.
- Ingredients come from **named suppliers with fixed specifications**, so tonight's dish tastes like last week's. That's a **lockfile** pinning exact package versions.
- The **head chef tastes every station's output** before it leaves the kitchen, the same way every time. Those are **tests**.
- Recipes state **exactly what goes in and comes out** ("200 g, diced"), not "some onions". That's **type hints**.
- When something goes wrong, the kitchen doesn't quietly serve a bad plate. It **stops and says why**, and someone writes it in the **log book**. Those are **exceptions** and **logging**.
- Deliveries are late sometimes. The kitchen **calls again after a sensible wait**, not every ten seconds, and doesn't give up on the first try. That's a **robust API client**.
- A new recipe isn't added to the menu until **another chef has read it**. That's **code review**.

---

## 29.1 The script that works until it doesn't

Work the way Chapter 18 did: copy the folder `companion/ch29` into `work`, so you have `work/ch29` to practise in. Here is the starting point, `start/monthly_report.py`. It's the monthly report as Imran left it, and it runs:

<!-- run: none -->
```python
# monthly_report.py - Riverstone's monthly sales report, as a first working script.
# Analyst to Architect · Chapter 29 · the "before" version: it works, and it has every problem section 29.1 lists.
# How: python3 monthly_report.py   (needs riverstone_2025 in PostgreSQL, pandas, openpyxl, SQLAlchemy, psycopg)
# Tested on: Python 3.14.7, pandas 3.0.6, openpyxl 3.1.5, SQLAlchemy 2.1.1, psycopg 3.3.6, PostgreSQL 16.
# Riverstone Supplies is fictional; every name and number is invented.
import pandas as pd
from sqlalchemy import create_engine

conn = create_engine("postgresql+psycopg://postgres:riverstone123@localhost/riverstone_2025")
month = "2025-12"

df = pd.read_sql("SELECT sl.*, c.customer_name, p.category AS cat FROM sales_lines sl "
                 "JOIN customers c ON c.customer_id = sl.customer_id "
                 "JOIN products p ON p.product_id = sl.product_id", conn)
df["order_date"] = pd.to_datetime(df["order_date"])
df = df[df["order_date"].dt.strftime("%Y-%m") == month]

total = df["net_revenue"].astype(float).sum()
orders = df["order_id"].nunique()
print("Revenue:", total)
print("Orders:", orders)

try:
    t = pd.read_sql("SELECT target_revenue FROM sales_targets WHERE target_month = '" + month + "-01'", conn)
    target = float(t.iloc[0, 0])
except:
    target = 0

cats = df.groupby("cat")["net_revenue"].sum().astype(float).reset_index()
cats["share"] = cats["net_revenue"] / total
cats = cats.sort_values("net_revenue", ascending=False)

top = df.groupby("customer_name")["net_revenue"].sum().astype(float).sort_values(ascending=False).head(5).reset_index()

with pd.ExcelWriter("Monthly_Report_Dec_FINAL.xlsx") as w:
    pd.DataFrame({"metric": ["Revenue", "Orders", "Target", "% of target"],
                  "value": [total, orders, target, total / target * 100]}).to_excel(w, sheet_name="Summary", index=False)
    cats.to_excel(w, sheet_name="Categories", index=False)
    top.to_excel(w, sheet_name="Top customers", index=False)
print("done")
```

The password in its `create_engine` line is Imran's. To run it, change `riverstone123` to your own PostgreSQL password, which is already the first of its problems. Then run it from a terminal in `work/ch29/start`, with the book's `.venv` active (Chapter 17, section 17.0):

<!-- run: none -->
```
# terminal, in work/ch29/start
$ python monthly_report.py
Revenue: 439823.5
Orders: 18
done
```

December's numbers are right: ₹4,39,823.50 (Chapter 13 showed it rounded, as ₹4,39,824) from 18 orders. Now it's the first week of February, and someone changes `month` to `"2026-01"` to produce January's report. Riverstone's `riverstone_2025` database ends on 31 December 2025, so there is no January data, exactly as there would be if the nightly load had failed:

<!-- run: none -->
```
# terminal, in work/ch29/start
$ python monthly_report.py
Revenue: 0.0
Orders: 0
/home/meera/ch29/start/monthly_report.py:37: RuntimeWarning: invalid value encountered in scalar divide
  "value": [total, orders, target, total / target * 100]}).to_excel(w, sheet_name="Summary", index=False)
done
```

It printed `done`. The exit code was 0, so a scheduler would record success. And because the file name is fixed, it replaced `Monthly_Report_Dec_FINAL.xlsx`, the good December report, with a January report showing zero revenue and a percentage of target that isn't a number. (The warning names the script's full path, which on your computer is your own `work/ch29/start` folder.)

Here's every problem in those 40 lines, and the section that fixes it:

| Problem in the script | Why it hurts | Fixed in |
|---|---|---|
| Everything runs at the top level, in one file | Can't test a calculation without a database, can't reuse a piece | 29.2, 29.3 |
| Password and connection details in the code | Anyone with the file has the password; it ends up in Git | 29.3 |
| Month and file name typed into the code | Every run means editing code; files overwrite each other | 29.3, 29.5 |
| No record of which package versions it needs | "Works on my machine"; breaks after an upgrade (it already broke once: pandas 3 requires `sheet_name=` by name) | 29.4 |
| No tests | Nobody knows whether a change broke a number | 29.7 |
| `except:` catches everything and sets `target = 0` | Hides the real cause, and produces a wrong percentage | 29.8 |
| `print` instead of logging; exit code 0 on failure | Scheduled runs look successful when they aren't | 29.8 |
| SQL built by gluing strings (`"… = '" + month + "-01'"`) | Breaks on unexpected input, and is how SQL injection happens | 29.2 |
| Loads every order line of the year, then filters in pandas | Fine for 326 lines, slow for 2 million (Chapter 28) | 29.2 |
| Joins `products` although the `sales_lines` view already has `category` | Two category columns (`category` and `cat`); a reader can't tell which is right | 29.2 |

> **Simplification note.** Scripts aren't bad. A script you run once, or a notebook for exploring data, doesn't need a package, tests, and a lockfile. The signal to change is when **other people depend on the output, it runs on a schedule, or it will be changed by someone other than its author**. Section 29.10 comes back to this judgment.

---

## 29.2 Functions and modules: one job each

The first step is always the same: pull each job into a **function** with a clear name, inputs, and a return value. A function that only calculates from its inputs, without reading files, databases, clocks, or global variables, and without changing anything outside itself, is called a **pure function**. Pure functions are the easiest code in the world to test, because the same input always gives the same output.

The report has four jobs, and they separate cleanly:

1. **Configure**: which month, which database, where to write.
2. **Read**: fetch the month's sales lines and target from the database.
3. **Transform**: summarize, break down by category, rank customers. *Pure.*
4. **Write**: produce the formatted workbook.

Start with the transform job, in a notebook, one function per cell. Create `ch29.ipynb` in `work/ch29` and choose the book's `.venv` kernel, as in Chapter 18.

### Five lines you can add up in your head

A pure function doesn't need the database, so try each one on a DataFrame small enough to check by hand:

<!-- py: reset -->
```python
import pandas as pd

lines = pd.DataFrame({
    "order_id":      [1, 1, 2, 3, 3],
    "customer_name": ["Sharma Hardware", "Sharma Hardware", "Metro Mart",
                      "Green Leaf Hotels", "Green Leaf Hotels"],
    "category":      ["Storage", "Kitchen", "Storage", "Kitchen", "Furniture"],
    "net_revenue":   [10000.0, 2500.0, 6000.0, 1500.0, 5000.0],
})
print(lines)
```

```
   order_id      customer_name   category  net_revenue
0         1    Sharma Hardware    Storage      10000.0
1         1    Sharma Hardware    Kitchen       2500.0
2         2         Metro Mart    Storage       6000.0
3         3  Green Leaf Hotels    Kitchen       1500.0
4         3  Green Leaf Hotels  Furniture       5000.0
```

Five order lines from three orders: Sharma Hardware's order 1 has two lines (₹10,000 + ₹2,500), and so does Green Leaf Hotels' order 3. The columns are the four the report needs from the `sales_lines` view.

### The summary, as a function

Before you run the next cell, write down the revenue, the number of orders, and the percentage of a ₹20,000 target you expect.

```python
def summarize(lines, target):
    revenue = round(float(lines["net_revenue"].sum()), 2)
    return {
        "revenue": revenue,
        "orders": int(lines["order_id"].nunique()),
        "customers": int(lines["customer_name"].nunique()),
        "pct_of_target": round(100 * revenue / target, 1),
    }


print(summarize(lines, 20000.0))
```

```
{'revenue': 25000.0, 'orders': 3, 'customers': 3, 'pct_of_target': 125.0}
```

How it works:

- **`def summarize(lines, target):`** takes the month's lines and its target, and **returns** a dictionary (Chapter 17, section 17.7) instead of printing, so other code can use the result.
- **`nunique()`** counts **orders**, not lines: five lines, three orders. That's Chapter 12's grain lesson, now written once in a function everyone uses.
- **`float(...)`** and **`int(...)`** turn pandas' own number types into plain Python numbers, so the dictionary prints as `25000.0` rather than `np.float64(25000.0)`.
- ₹25,000 ÷ ₹20,000 = 125.0%. ✓

### Categories and customers

The category table uses the named aggregation of Chapter 18, section 18.6:

```python
def revenue_by_category(lines):
    result = (lines.groupby("category", as_index=False)
                   .agg(net_revenue=("net_revenue", "sum"))
                   .sort_values(["net_revenue", "category"], ascending=[False, True],
                                ignore_index=True))
    total = result["net_revenue"].sum()
    result["share_pct"] = (100 * result["net_revenue"] / total).round(1)
    return result


print(revenue_by_category(lines))
```

```
    category  net_revenue  share_pct
0    Storage      16000.0       64.0
1  Furniture       5000.0       20.0
2    Kitchen       4000.0       16.0
```

How it works:

- **`.agg(net_revenue=("net_revenue", "sum"))`** is a named aggregation: the new column's name on the left, and on the right the column to use and what to do with it. **`as_index=False`** keeps `category` as an ordinary column.
- **`.sort_values(["net_revenue", "category"], ascending=[False, True], ...)`** sorts by two columns: revenue, largest first, and then by name, A to Z. The second key makes the order stable when two categories tie, the same reason Chapter 13 added tie-breakers to `ROW_NUMBER`.
- **`ignore_index=True`** numbers the sorted rows 0, 1, 2 afresh, as it did for `concat` in Chapter 18.
- The shares add to 100.0% (64.0 + 20.0 + 16.0). ✓

The customer ranking is the same pattern, cut to the top `n`:

```python
def top_customers(lines, n=5):
    totals = (lines.groupby("customer_name", as_index=False)
                   .agg(net_revenue=("net_revenue", "sum")))
    ranked = totals.sort_values(["net_revenue", "customer_name"], ascending=[False, True],
                                ignore_index=True)
    return ranked.head(n)


print(top_customers(lines, n=2))
```

```
       customer_name  net_revenue
0    Sharma Hardware      12500.0
1  Green Leaf Hotels       6500.0
```

`n=5` in the `def` line is a **default**: leave `n` out and you get the top five. Sharma Hardware's two lines add to ₹12,500, so it comes first.

### An empty month must stop, not print zeros

What does `summarize` do with January, when there's no data? `lines.iloc[0:0]` makes the test case: `iloc` picks rows by position (Chapter 18), and `0:0` is the empty range, so it's a DataFrame with the same columns and no rows.

```python
print(summarize(lines.iloc[0:0], 20000.0))
```

```
{'revenue': 0.0, 'orders': 0, 'customers': 0, 'pct_of_target': 0.0}
```

That's the script's bug, reproduced in one line: no data, and a summary that looks like a real month with zero sales. The fix is a function that checks the lines first and **raises** an exception (Chapter 17, section 17.10) when they can't make a correct report:

```python
REQUIRED_COLUMNS = {"order_id", "customer_name", "category", "net_revenue"}


def check_lines(lines):
    missing = REQUIRED_COLUMNS - set(lines.columns)
    if missing:
        raise ValueError(f"sales lines are missing columns: {sorted(missing)}")
    if lines.empty:
        raise ValueError("no sales lines for this month")


check_lines(lines)
print("five lines: OK")
check_lines(lines.iloc[0:0])
```

```
five lines: OK
ValueError: no sales lines for this month
```

How it works:

- **`REQUIRED_COLUMNS - set(lines.columns)`** is set difference (Chapter 17, section 17.7): the names that are required but not present. An empty set is false, so `if missing:` only fires when something is absent.
- **`sorted(missing)`** lists the missing names in a fixed order, so the message reads the same every time.
- **`lines.empty`** is `True` when the DataFrame has no rows.
- **`raise ValueError(...)`** stops with a message instead of carrying on. The last line of the cell raised it, so the notebook shows the error under the cell.

### From cells to a module

Each job goes in its own **module**, a `.py` file you can `import`. The four cells above become the first version of `transform.py`, with one change: every function calls `check_lines` before it calculates.

<!-- run: none -->
```python
"""Pure calculations: DataFrames in, results out. No database, no files, so easy to test."""

REQUIRED_COLUMNS = {"order_id", "customer_name", "category", "net_revenue"}


def check_lines(lines):
    missing = REQUIRED_COLUMNS - set(lines.columns)
    if missing:
        raise ValueError(f"sales lines are missing columns: {sorted(missing)}")
    if lines.empty:
        raise ValueError("no sales lines for this month")


def summarize(lines, target):
    check_lines(lines)
    revenue = round(float(lines["net_revenue"].sum()), 2)
    return {
        "revenue": revenue,
        "orders": int(lines["order_id"].nunique()),
        "customers": int(lines["customer_name"].nunique()),
        "pct_of_target": round(100 * revenue / target, 1),
    }


def revenue_by_category(lines):
    check_lines(lines)
    result = (lines.groupby("category", as_index=False)
                   .agg(net_revenue=("net_revenue", "sum"))
                   .sort_values(["net_revenue", "category"], ascending=[False, True],
                                ignore_index=True))
    total = result["net_revenue"].sum()
    result["share_pct"] = (100 * result["net_revenue"] / total).round(1)
    return result


def top_customers(lines, n=5):
    if n < 1:
        raise ValueError("n must be at least 1")
    check_lines(lines)
    totals = (lines.groupby("customer_name", as_index=False)
                   .agg(net_revenue=("net_revenue", "sum")))
    ranked = totals.sort_values(["net_revenue", "customer_name"], ascending=[False, True],
                                ignore_index=True)
    return ranked.head(n)
```

- The text in triple quotes on the first line is the module's **docstring**: what the file is for, the first thing a colleague reads.
- **`if n < 1: raise ValueError(...)`** refuses a nonsense request (the top zero customers) instead of returning an empty table.
- The file doesn't import pandas: it only calls methods on the DataFrames it's given.

This is the first of three versions. Section 29.5 turns the dictionary into a small class, section 29.6 adds type hints, and section 29.8 gives the empty month its own kind of error. The finished file is `riverstone-report/src/riverstone_report/transform.py`.

### The read job

The read module is the only place that knows SQL. It fixes three problems from the script: it asks the database for **only the month's rows**; it passes the dates as **query parameters** (`:month_start`, Chapter 18, section 18.13), so values are never glued into the SQL text; and it takes `category` from the `sales_lines` view, without the extra join.

Connect the notebook first. The finished package keeps its settings in a `.env` file (Chapter 18, section 18.13) inside `riverstone-report`: copy `riverstone-report/.env.example` to `riverstone-report/.env` and put your own PostgreSQL password in place of `YOUR_PASSWORD`. The file has two lines:

```text
RIVERSTONE_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost/riverstone_2025
RIVERSTONE_OUTPUT_DIR=reports
```

```python
import os
from datetime import date

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv("riverstone-report/.env")
engine = create_engine(os.environ["RIVERSTONE_DATABASE_URL"])
print(engine.dialect.name, engine.url.database)
```

```
postgresql riverstone_2025
```

- **`load_dotenv("riverstone-report/.env")`** reads that file into the environment. Given a path, it reads exactly that file instead of searching for one.
- This package uses its own variable, **`RIVERSTONE_DATABASE_URL`**, because it reads `riverstone_2025`, not the `riverstone_full` that Chapter 18's `RIVERSTONE_DB` points at.
- **`engine.url.database`** is the database name from the URL. Printing it, rather than the whole URL, confirms the connection without showing the password.

Now the two read functions, in one cell:

```python
SALES_LINES_SQL = text("""
    SELECT sl.order_id, sl.order_date, c.customer_name, sl.category, sl.net_revenue
    FROM sales_lines AS sl
    JOIN customers AS c ON c.customer_id = sl.customer_id
    WHERE sl.order_date >= :month_start AND sl.order_date < :next_month
""")

TARGET_SQL = text("SELECT target_revenue FROM sales_targets WHERE target_month = :month_start")


def fetch_sales_lines(engine, month_start, next_month):
    """One row per non-cancelled order line in the month, with net_revenue as a float."""
    with engine.connect() as conn:
        lines = pd.read_sql(SALES_LINES_SQL, conn,
                            params={"month_start": month_start, "next_month": next_month})
    return lines.astype({"net_revenue": "float64"})


def fetch_target(engine, month_start):
    """The month's revenue target, or None if no target was set."""
    with engine.connect() as conn:
        value = conn.execute(TARGET_SQL, {"month_start": month_start}).scalar_one_or_none()
    return None if value is None else float(value)


december = fetch_sales_lines(engine, date(2025, 12, 1), date(2026, 1, 1))
print(december.shape, round(december["net_revenue"].sum(), 2))
print(fetch_target(engine, date(2025, 12, 1)))
print(fetch_target(engine, date(2026, 1, 1)))
```

```
(35, 5) 439823.5
380000.0
None
```

How it works:

- **`text("""...""")`** and the **`:month_start`** and **`:next_month`** slots are Chapter 18's parameters. The month is a range, `>=` the first day and `<` the first day of the next month, so every date and time inside the month counts and nothing outside it does.
- **`with engine.connect() as conn:`** opens one connection and closes it when the block ends, even if the query fails.
- **`conn.execute(TARGET_SQL, {...})`** runs a query without pandas, and **`.scalar_one_or_none()`** returns the single value it found, or `None` if there was no row. January 2026 has no target row, so the last line prints `None`, not 0.
- **`.astype({"net_revenue": "float64"})`**: PostgreSQL's `NUMERIC` arrives in Python as `Decimal` values, which don't mix with ordinary numbers in every calculation; `float64` makes the column ordinary decimal numbers.
- December: 35 lines, ₹4,39,823.50, and a target of ₹3,80,000. ✓

The real month goes through the same pure functions as the five made-up lines:

```python
print(summarize(december, fetch_target(engine, date(2025, 12, 1))))
```

```
{'revenue': 439823.5, 'orders': 18, 'customers': 15, 'pct_of_target': 115.7}
```

18 orders from 15 customers, 115.7% of target. The two read functions become `db.py`, the only module that imports SQLAlchemy.

> **Watch out: never build SQL by adding strings.** `"WHERE target_month = '" + month + "-01'"` works until `month` contains a quote, or until someone passes `2025-12' OR '1'='1`. That's **SQL injection**, one of the most common security holes in software. Parameters (`:month_start` with SQLAlchemy's `text`, `%s` with psycopg directly) send the value separately from the SQL, so it's always treated as a value.

### `if __name__ == "__main__"`

Chapter 17, section 17.12, used this line to separate a script's command from its functions. It matters more in a package. When Python runs a file directly, it sets the special variable `__name__` to `"__main__"`; when the same file is imported, `__name__` is the module's name. So code under `if __name__ == "__main__":` runs only when the file is executed, not when a test imports it. The script had all its code at the top level, so importing it to test one calculation would have connected to the database and written a file. Every module in the package defines functions and nothing else at the top level; only `cli.py` has a `__main__` block.

---

## 29.3 Project structure and configuration

### The layout

The finished package is in `work/ch29/riverstone-report`. List every file in it with Chapter 34's `find`, piped into `sort` so the list is in a fixed order:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ find . -type f | sort
./.env
./.env.example
./.gitignore
./.python-version
./README.md
./pyproject.toml
./src/riverstone_report/__init__.py
./src/riverstone_report/cli.py
./src/riverstone_report/config.py
./src/riverstone_report/crm_client.py
./src/riverstone_report/db.py
./src/riverstone_report/errors.py
./src/riverstone_report/excel.py
./src/riverstone_report/headline.py
./src/riverstone_report/transform.py
./tests/conftest.py
./tests/test_config.py
./tests/test_crm_client.py
./tests/test_reconcile.py
./tests/test_transform.py
./uv.lock
```

`.env` is there because you made it in section 29.2; everything else came with the companion files.

![Left: the original script as seven stacked steps, four highlighted as problems. Right: the package tree with pyproject.toml, uv.lock, a src folder of single-purpose modules, and a tests folder](figures/fig29-1-script-to-package.svg)

*Figure 29.1 — The same report, split so that each file has one job.*

- A **package** is a folder of modules that Python can import as one unit. `src/riverstone_report/` is the package. Its `__init__.py` marks the folder as a package and says what it offers.
- The **`src/` layout** puts the package one level down, so tests import the *installed* package rather than whatever happens to be in the current folder. It catches a whole class of "passes on my machine" mistakes, and it's what `uv init --package` creates.
- **`tests/`** sits beside `src/`, not inside it, so tests aren't shipped with the package.
- **`pyproject.toml`** is the standard file describing a Python project: its name, version, dependencies, entry points, and settings for tools like `pytest` and `mypy`.
- **`.gitignore`** keeps the virtual environment, caches, `.env`, and generated reports out of version control. **`.env.example`** is the same file as `.env` with the password replaced by a placeholder, so a colleague knows which settings to supply.

`__init__.py` is three lines:

<!-- run: none -->
```python
"""Riverstone's monthly sales report, as a tested package (Analyst to Architect, Ch. 29)."""
from riverstone_report.cli import main

__all__ = ["main"]
```

- **`from riverstone_report.cli import main`** makes `main`, the function that runs the report (section 29.8), available as `riverstone_report.main`.
- **`__all__`** lists the names the package offers to other code. It's a statement of intent: everything else inside is the package's own business.

### `pyproject.toml`, and TOML in one minute

`pyproject.toml` is written in **TOML**, a format for settings files that is easier to read than JSON. Six rules cover everything in this file.

> **TOML in one minute.**
> - `[project]` on its own line starts a **section**; everything below it, up to the next header, belongs to it.
> - `name = "riverstone-report"` sets a **key** to a **value**. Text goes in double quotes; numbers and `true`/`false` don't.
> - `["tests"]` in square brackets is a **list**; it may run over several lines, with a comma after each item.
> - `{ name = "Meera Iyer", email = "…" }` in curly braces is a small group of keys on one line.
> - A dotted header such as `[tool.mypy]` means "the `mypy` part of the `tool` section".
> - A line starting with `#` is a comment.

Here is the package's file. `uv init --package` wrote the first version, and `uv add` filled in the dependencies (section 29.4):

<!-- run: none -->
```toml
[project]
name = "riverstone-report"
version = "0.1.0"
description = "Riverstone's monthly sales report: database → tested summary → Excel workbook."
readme = "README.md"
authors = [
    { name = "Meera Iyer", email = "meera@riverstone.example" }
]
requires-python = ">=3.14"
dependencies = [
    "openpyxl>=3.1.5",
    "pandas>=3.0.6",
    "psycopg[binary]>=3.3.6",
    "requests>=2.34.2",
    "sqlalchemy>=2.1.1",
]

[project.scripts]
riverstone-report = "riverstone_report:main"

[build-system]
requires = ["uv_build>=0.12.19,<0.13.0"]
build-backend = "uv_build"

[dependency-groups]
dev = [
    "ipykernel>=7.3.0",
    "mypy>=2.3.1",
    "pandas-stubs>=3.0.5.260914",
    "pytest>=9.1.1",
    "types-openpyxl>=3.1.5.20260827",
    "types-requests>=2.33.0.20260906",
]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.mypy]
strict = true
files = ["src"]
```

| Section | What it says |
|---|---|
| `[project]` | The package itself: `name`, `version`, a one-line `description`, the `readme` file, the `authors`, the Python it needs (`requires-python = ">=3.14"`: 3.14 or later), and its `dependencies`. `>=3.0.6` means "this version or newer". `psycopg[binary]` means psycopg plus its optional ready-built "binary" part, so nothing has to be compiled on your computer |
| `[project.scripts]` | A command to create when the package is installed: `riverstone-report` runs the `main` function that `__init__.py` imports from `cli.py` |
| `[build-system]` | How to turn the folder into an installable package. uv fills this in; you don't edit it |
| `[dependency-groups]` | Extra packages needed only while developing: the **dev** group holds the test runner, the type checker and its helpers, and `ipykernel` for the notebook (section 29.4) |
| `[tool.pytest.ini_options]` | Settings for pytest: look for tests in the `tests` folder |
| `[tool.mypy]` | Settings for mypy (section 29.6): check strictly, and check the `src` folder |

`uv init` writes `description = "Add your description here"`; replace it with one sentence that says what the package does, as here. The `authors` line comes from your Git settings (Chapter 26), so yours shows your name.

### Configuration: settings belong outside the code

The script had three kinds of setting mixed into its code: the **secret** (the password), the **environment** (which database), and the **run** (which month). They change for different reasons and at different times, so they come from different places:

| Setting | Changes when | Comes from |
|---|---|---|
| Month to report | every run | a command-line argument: `--month 2025-12` |
| Database URL (with password) | per machine or server; must stay secret | an **environment variable**, `RIVERSTONE_DATABASE_URL` |
| Output folder | per machine | an environment variable with a default, `RIVERSTONE_OUTPUT_DIR` |
| Number of top customers | rarely; a business decision | a default in code |

An **environment variable** is a named value that the operating system passes to every program you start from that terminal, as Chapter 34 showed. Setting one in a bash terminal (macOS, Linux, or Git Bash and WSL on Windows):

<!-- run: none -->
```
# terminal
$ export RIVERSTONE_DATABASE_URL="postgresql+psycopg://postgres:YOUR_PASSWORD@localhost/riverstone_2025"
```

Typing that in every new terminal is tedious, and it puts the password in your shell's history. So this package keeps its settings in the **`.env` file** you made in section 29.2, which is listed in `.gitignore`. The package itself never reads `.env`: its code reads only environment variables, which keeps it working unchanged on a server where the settings come from somewhere else. Instead, `uv` loads the file for one command at a time:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run --env-file .env riverstone-report --month 2025-12
```

**`--env-file .env`** tells `uv run` to read `.env` into the environment of that one command, and of nothing else. Section 29.4 introduces `uv run`, and section 29.8 shows what this command prints. On servers and schedulers, the platform's **secrets manager** supplies the variables instead. Either way, the rule is the same: **a password never appears in a file that goes into version control.**

> **PowerShell instead?** This chapter's terminal commands are written for bash, as in Chapter 34. In Windows PowerShell three of them are different: set a variable with `$env:RIVERSTONE_DATABASE_URL = "…"`; activate an environment with `.venv\Scripts\Activate.ps1` (with the execution-policy fix of Chapter 17, section 17.0); and print the last exit code with `echo "exit code: $LASTEXITCODE"`, because PowerShell's `$?` prints `True` or `False`, not the number.

> **Watch out: a password committed once is exposed forever.** Deleting it in a later commit doesn't remove it from Git's history, and public repositories are scanned for credentials within minutes. If a secret is ever committed, treat it as leaked: change the password first, then clean up.

> **Stop here: sitting 1 of 4.** You've seen the script fail, rebuilt its calculations as pure functions in a notebook, and met the package's layout, its `pyproject.toml`, and where its settings live.

---

## 29.4 Environments and lockfiles

### Why "pip install pandas" isn't enough

Every Python project depends on packages, and those packages depend on others. The report needs 5 packages directly, and on Linux they pull in 10 more. When you type `pip install pandas`, you get whatever version is newest *today*, installed into whatever Python you happen to be using. Six months later a colleague installs the "same" requirements and gets pandas 3.1 instead of 3.0, and something behaves differently. The starting script has already been bitten once: written for pandas 2, it stopped running under pandas 3, because `to_excel` now requires the sheet name to be passed by keyword.

Two tools solve two different problems:

- A **virtual environment** is a private folder of packages for one project, with its own copy of the `python` and `pip` commands (Chapter 17, section 17.0). Projects stop interfering with each other.
- A **lockfile** records the **exact version of every package**, including the indirect ones, so every installation is identical.

### Recap from Chapter 17: venv and pinned requirements

Python ships with `venv`, and Chapter 17 used it to make the book's environment. It works everywhere, including locked-down company laptops. For a project of its own, the report's environment would be made the same way, in the project folder, with the report's five packages:

<!-- run: none -->
```
# terminal, in a new project folder
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ python -m pip install pandas openpyxl sqlalchemy "psycopg[binary]" requests
(.venv) $ python -m pip freeze
certifi==2026.7.22
charset-normalizer==3.5.1
et_xmlfile==2.0.0
idna==3.20
numpy==2.5.3
openpyxl==3.1.5
pandas==3.0.6
psycopg==3.3.6
psycopg-binary==3.3.6
python-dateutil==2.9.0.post0
requests==2.34.2
six==1.17.0
SQLAlchemy==2.1.1
typing_extensions==4.16.0
urllib3==2.8.0
(.venv) $ python -m pip freeze > requirements.txt
(.venv) $ deactivate
```

- On Windows in Git Bash, the activate line is `source .venv/Scripts/activate`. Once it's active, the prompt starts with `(.venv)`.
- `pip install` prints a long list of downloads and ends with a line starting `Successfully installed`.
- **`pip freeze`** lists every package installed, with its exact version: the 5 you asked for and the 10 they need. `> requirements.txt` saves the list.

A colleague then creates and activates their own `.venv` and runs `python -m pip install -r requirements.txt`. That makes `requirements.txt` a simple lockfile. Its weaknesses: it can't tell which packages you asked for and which came along as dependencies, it doesn't record which versions work on other operating systems, and keeping it up to date is manual.

### The modern way: uv, pyproject.toml, and uv.lock

**`uv`** is a fast, free package and project manager from Astral that does the whole job: it creates the virtual environment, resolves versions, writes a cross-platform lockfile, and runs commands inside the environment. It was version 0.12.19 when this chapter was tested (released on 25 September 2026). Install it from the official instructions at `docs.astral.sh/uv` (a one-line installer on each operating system, or `pip install uv`).

Build a package of your own from nothing, beside the finished one, so you can compare them. `mkdir` makes a folder, and `uv init --package` turns the folder you're in into a package:

<!-- run: none -->
```
# terminal, in work/ch29
$ uv --version
uv 0.12.19 (x86_64-unknown-linux-gnu)
$ mkdir mine
$ cd mine
$ mkdir riverstone-report
$ cd riverstone-report
$ uv init --package
Initialized project `riverstone-report`
$ ls -a
.
..
.git
.gitignore
.python-version
README.md
pyproject.toml
src
```

- **`uv init --package`** creates the `src/` layout with a starter `__init__.py`, a `pyproject.toml` named after the folder, a `.gitignore`, an empty `README.md`, and **`.python-version`**, which records the Python the project uses (`3.14`; if it isn't installed, uv downloads it the first time it needs it).
- It also runs `git init` (Chapter 26), which is the `.git` folder: the project is a repository from the start.

Now add the report's packages, and then the tools that are only needed while developing:

<!-- run: none -->
```
# terminal, in work/ch29/mine/riverstone-report
$ uv add pandas openpyxl sqlalchemy "psycopg[binary]" requests
Using CPython 3.14.7
Creating virtual environment at: .venv
Resolved 17 packages in 10ms
…
Installed 16 packages in 28ms
 + certifi==2026.7.22
 + charset-normalizer==3.5.1
 + et-xmlfile==2.0.0
 + idna==3.20
 + numpy==2.5.3
 + openpyxl==3.1.5
 + pandas==3.0.6
 + psycopg==3.3.6
 + psycopg-binary==3.3.6
 + python-dateutil==2.9.0.post0
 + requests==2.34.2
…
 + six==1.17.0
 + sqlalchemy==2.1.1
 + typing-extensions==4.16.0
 + urllib3==2.8.0
$ uv add --dev pytest mypy pandas-stubs types-requests types-openpyxl ipykernel
Resolved 58 packages in 451ms
…
Installed 38 packages in 80ms
 + ast-serialize==0.11.2
 + asttokens==3.0.2
 …
```

*(Shortened: the lines left out name your project's own folder, and the second list goes on to all 38 packages.)*

- **`uv add`** adds each package to `pyproject.toml`'s `dependencies` with a minimum version (`pandas>=3.0.6`), works out every indirect dependency, writes **`uv.lock`**, and installs everything into a `.venv` it creates the first time. The 16 installed are the 5 you named, the 10 they need, and your own package.
- **`uv add --dev`** puts tools that are only needed while developing in the **dev dependency group**: pytest (section 29.7), mypy and the type information for pandas, requests and openpyxl (section 29.6), and `ipykernel`, which lets a notebook use this environment (below).

`cat pyproject.toml` now shows the same file as section 29.3's, apart from the description you haven't edited yet and the two `[tool]` sections, which you add by hand.

`pyproject.toml` says what the project *needs*; `uv.lock` says exactly what was *installed*. Here's the start of one entry in the lockfile, with the long download addresses and fingerprints cut short:

<!-- run: none -->
```toml
[[package]]
name = "pandas"
version = "3.0.6"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "numpy" },
    { name = "python-dateutil" },
    { name = "tzdata", marker = "sys_platform == 'emscripten' or sys_platform == 'win32'" },
]
sdist = { url = "https://files.pythonhosted.org/packages/…/pandas-3.0.6.tar.gz", hash = "sha256:66b07ef7…", … }
```

- **`[[package]]`** in double brackets starts one entry in a *list* of entries: the file has one for every package.
- **`dependencies`** are the packages pandas itself needs. `tzdata` has a **marker**: it's installed only on Windows (and in browsers), which is why the file works on every operating system.
- **`hash`** is a fingerprint of the exact file. If a download doesn't match it, uv refuses to install it, so nobody can slip in a tampered copy.

Both files go into version control. The payoff is on someone else's machine. Your copy of the finished package, `work/ch29/riverstone-report`, has no `.venv` yet, exactly like a colleague's fresh copy. Set it up from the lockfile:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv sync --locked
Using CPython 3.14.7
Creating virtual environment at: .venv
Resolved 58 packages in 1ms
…
Installed 53 packages in 102ms
 + ast-serialize==0.11.2
 + asttokens==3.0.2
 + certifi==2026.7.22
 + charset-normalizer==3.5.1
 + comm==0.2.3
 …
$ uv run python -c "import pandas, openpyxl, requests; print(pandas.__version__, openpyxl.__version__, requests.__version__)"
3.0.6 3.1.5 2.34.2
```

*(Shortened: the full output names the project's folder and lists all 53 packages.)*

- **`--locked`** means *"install exactly what the lockfile says, and fail if `pyproject.toml` and `uv.lock` disagree"*. That's the command for servers and automated test runs.
- **`uv run`** runs any command inside the project's environment without activating it: `uv run pytest`, `uv run mypy`, `uv run riverstone-report --help`. **`python -c "…"`** runs the Python code in quotes and exits, which is handy for a one-line check.
- The numbers reconcile. The lockfile has 58 entries: your package, the 15 it needs, the dev tools and everything they need, plus 5 packages used only on Windows or macOS. On Linux, 53 of them are installed.
- **`uv sync` installs the dev group too**, which is why it installed 53 packages, not 16. On a server that only runs the report, use `uv sync --locked --no-dev`: it installs the 16.

If a system needs a `requirements.txt` (some older deployment tools do), `uv export --no-dev --no-hashes` produces one from the lockfile.

| Task | venv + pip | uv |
|---|---|---|
| Create environment | `python -m venv .venv` | automatic on `uv sync`, `uv add`, or `uv run` |
| Add a package | `pip install pandas`, then update `requirements.txt` by hand | `uv add pandas` |
| Record exact versions | `pip freeze > requirements.txt` | `uv.lock`, updated automatically |
| Install on another machine | `pip install -r requirements.txt` | `uv sync --locked` |
| Install without dev tools | a separate requirements file, by hand | `uv sync --locked --no-dev` |
| Run a tool | activate, then `pytest` | `uv run pytest` |
| Upgrade one package | `pip install -U pandas`, refreeze | `uv lock --upgrade-package pandas`, then `uv sync` |

### Use the package from your notebook

Your notebook still runs on the book's `.venv`, which doesn't have this package. Switch it: in VS Code, click the kernel name at the top right of `ch29.ipynb`, choose **Select Another Kernel → Python Environments**, and pick the one in `riverstone-report/.venv`. That environment can run a notebook because `ipykernel` is in its dev group.

A new kernel starts empty, so run the cell with the five-line `lines` DataFrame from section 29.2 again. Then import from the package instead of defining the functions in cells:

```python
from riverstone_report.transform import check_lines, revenue_by_category

print(revenue_by_category(lines))
```

```
    category  net_revenue  share_pct
0    Storage      16000.0       64.0
1  Furniture       5000.0       20.0
2    Kitchen       4000.0       16.0
```

The same table as in section 29.2, now from `src/riverstone_report/transform.py`. The import works because `uv sync` installed your package into its own environment in **editable** mode: Python reads the files in `src/` where they are, so an edit to a module is seen the next time it's imported. (A notebook imports a module only once, so after editing one, restart the kernel.)

> **Tool note.** **Poetry** and **PDM** are older project managers that do similar jobs with their own lockfiles, and you'll meet them in existing company projects. **conda** manages non-Python dependencies too and is common in scientific computing. The ideas transfer: a project file for what you need, a lockfile for what you got, an isolated environment, and one command to reproduce it.

---

## 29.5 Classes, when they help

A **class** bundles data with the functions that work on it. Analysts coming from notebooks either never write one, or suddenly write classes for everything. The useful middle is small.

Chapter 18, section 18.17, introduced classes on the monthly report: `__init__` and `self`, data classes for settings, composition, and inheritance for the two writers. This section assumes that and asks the next question: now that the report is a **package** rather than a notebook, where do classes actually earn their place, and where is a plain function still the better answer? The recap below is deliberately quick; if any of it is new, read section 18.17 first.

### Classes in twenty minutes, recapped

Run each cell in your notebook. A **class** is a template; an **instance** is one object made from it:

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


box = Product("Storage Box 10L", 430.0)
print(box.name, box.price)
```

```
Storage Box 10L 430.0
```

- **`class Product:`** defines the template. By convention, class names start with a capital letter.
- **`__init__`** (two underscores each side) is the function Python runs when you create an instance. You never call it by name: `Product("Storage Box 10L", 430.0)` calls it for you.
- **`self`** is the particular object being created or used. Python passes it in as the first argument automatically, which is why `Product(...)` has two arguments and `__init__` has three.
- **`self.name = name`** stores a value on the object. A value stored this way is an **attribute**, read with a dot: `box.name`.

A function written inside a class is a **method**. It receives the object as `self`, so it can use the object's attributes:

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def price_after(self, discount_pct):
        return round(self.price * (1 - discount_pct / 100), 2)


box = Product("Storage Box 10L", 430.0)
print(box.price_after(5))
```

```
408.5
```

`box.price_after(5)` passes `box` as `self` and `5` as `discount_pct`: ₹430 less 5% is ₹408.50. ✓

A line starting with `@` just above a `def` or a `class` is a **decorator**: it hands what follows to another function, which adds some behaviour to it. The first one you need is **`@property`**, which lets a method be read like an attribute, without brackets:

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def label(self):
        return f"{self.name} (₹{self.price:,.0f})"


box = Product("Storage Box 10L", 430.0)
print(box.label)
```

```
Storage Box 10L (₹430)
```

`box.label` is calculated each time it's read, from the current name and price, so it can never be out of date.

Writing `__init__` by hand gets tedious. A **data class** writes it for you, from a list of fields:

```python
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float


box = Product("Storage Box 10L", 430.0)
print(box)
print(box == Product("Storage Box 10L", 430.0))
```

```
Product(name='Storage Box 10L', price=430.0)
True
```

- **`@dataclass`** reads the fields listed in the class and writes `__init__`, a readable print (the first line), and equality (the second: two products with the same fields are equal).
- **`name: str`** and **`price: float`** are the fields. The part after the colon is a **type hint**, which says what kind of value belongs there; a data class needs one for every field. Section 29.6 explains hints.

Add `frozen=True`, and nothing can change an instance after it's made. This cell fails on purpose:

```python
@dataclass(frozen=True)
class Product:
    name: str
    price: float


box = Product("Storage Box 10L", 430.0)
box.price = 450.0
```

```
dataclasses.FrozenInstanceError: cannot assign to field 'price'
```

A frozen object is **immutable**. That's what you want for a settings bundle or a result: nothing can change it halfway through a run by accident.

One class can build on another. `class NoDataError(ReportError):` makes `NoDataError` a kind of `ReportError`, which is itself a kind of `Exception`; this is **inheritance**. It's how you make your own exceptions, and section 29.8 uses exactly these:

```python
class ReportError(Exception):
    pass


class NoDataError(ReportError):
    pass


try:
    raise NoDataError("no sales lines for this month")
except ReportError as exc:
    print("caught:", exc)
    print(isinstance(exc, ReportError), isinstance(exc, NoDataError))
```

```
caught: no sales lines for this month
True True
```

- **`pass`** means "nothing more to add": these classes get everything from `Exception`.
- **`except ReportError`** caught a `NoDataError`, because a `NoDataError` *is* a `ReportError`. **`isinstance(object, class)`** asks exactly that question.

Last, a second way to build an object. A method marked **`@classmethod`** receives the class itself, by convention named **`cls`**, instead of an instance, and is usually used as an **alternative constructor**: a named way to build the object from something else.

```python
@dataclass(frozen=True)
class Product:
    name: str
    price: float

    @classmethod
    def from_text(cls, text):
        name, price = text.split(";")
        return cls(name, float(price))


print(Product.from_text("Garden Chair;1150"))
```

```
Product(name='Garden Chair', price=1150.0)
```

`Product.from_text(...)` is called on the class, not on an instance; `cls(name, float(price))` is the same as `Product(name, float(price))`. That's every piece of class syntax this chapter uses.

### Data classes: named bundles of values

Now use them on the report. `summarize` returns a dictionary, and its `pct_of_target` has two problems. It's stored when the summary is made, so it can disagree with `revenue` if someone changes one and not the other. And a month with no target (`None`) or a zero target crashes the division. A frozen data class with a property fixes both:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class MonthSummary:
    revenue: float
    orders: int
    customers: int
    target: float | None

    @property
    def pct_of_target(self):
        if not self.target:
            return None
        return round(100 * self.revenue / self.target, 1)


def summarize(lines, target):
    check_lines(lines)
    return MonthSummary(
        revenue=round(float(lines["net_revenue"].sum()), 2),
        orders=int(lines["order_id"].nunique()),
        customers=int(lines["customer_name"].nunique()),
        target=target,
    )


summary = summarize(lines, 20000.0)
print(summary)
print(summary.pct_of_target)
print(summarize(lines, None).pct_of_target)
```

```
MonthSummary(revenue=25000.0, orders=3, customers=3, target=20000.0)
125.0
None
```

- **`target: float | None`** says the target is a number, or `None` when no target was set.
- **`if not self.target:`** is true for both `None` and 0, so neither reaches the division; the property returns `None`, and the report can say "no target set".
- `MonthSummary(revenue=..., orders=..., ...)` passes each field by name, so the values can't arrive in the wrong order.

`MonthSummary` and this `summarize` replace the dictionary version in `transform.py`. Section 29.6 shows the whole file.

> **Watch out: don't store what you can calculate.** If `MonthSummary` stored `pct_of_target` as a field, someone could change `revenue` and forget to update it. As a property, it's calculated from the current values every time. This is Chapter 28's normalization rule (store each fact once) applied to code.

### The configuration as a data class

The report passes the same four settings everywhere. As loose variables, a function call looks like `run("2025-12", url, "reports", 5)`, and nothing stops the arguments arriving in the wrong order. `config.py` bundles them:

<!-- run: none -->
```python
"""Settings for one report run, read from arguments and environment variables."""
import os
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from riverstone_report.errors import ConfigError


def parse_month(text: str) -> date:
    """Turn '2025-12' into date(2025, 12, 1). Raise ConfigError for anything else."""
    try:
        year, month = (int(part) for part in text.split("-"))
        return date(year, month, 1)
    except ValueError:
        raise ConfigError(f"month must look like YYYY-MM, got {text!r}") from None


@dataclass(frozen=True)
class ReportConfig:
    month: date
    database_url: str
    output_dir: Path = Path("reports")
    top_n: int = 5

    @classmethod
    def from_env(cls, month: str, env: Mapping[str, str] = os.environ) -> ReportConfig:
        url = env.get("RIVERSTONE_DATABASE_URL")
        if not url:
            raise ConfigError("set RIVERSTONE_DATABASE_URL to the database connection URL")
        return cls(
            month=parse_month(month),
            database_url=url,
            output_dir=Path(env.get("RIVERSTONE_OUTPUT_DIR", "reports")),
        )

    @property
    def next_month(self) -> date:
        if self.month.month == 12:
            return date(self.month.year + 1, 1, 1)
        return date(self.month.year, self.month.month + 1, 1)

    @property
    def output_path(self) -> Path:
        return self.output_dir / f"riverstone_monthly_{self.month:%Y-%m}.xlsx"
```

How it works:

- **`parse_month`** splits `"2025-12"` at the `-` and turns each part into a whole number. Anything that doesn't give exactly two numbers making a real date raises a `ValueError` inside the `try`, and the `except` turns every such error into one kind, `ConfigError`, with a clear message. **`from None`** hides the less helpful internal `ValueError` from the traceback.
- **`{text!r}`** inside an f-string shows the value the way Python would type it, with quotes: `'Dec 2025'`, so an empty or space-padded input is visible in the message.
- **`output_dir: Path = Path("reports")`** and **`top_n: int = 5`** are fields with defaults, so they can be left out when a `ReportConfig` is made.
- **`from_env`** is an alternative constructor. The `env` parameter defaults to the real `os.environ`, but a test can pass a plain dictionary, as the next cell does, and no test has to change your real environment variables. `env.get(name)` returns `None` when the name is missing; `env.get(name, "reports")` returns the default instead.
- **`next_month`** and **`output_path`** are properties. December correctly rolls into January of the next year. **`{self.month:%Y-%m}`** formats the date inside the f-string with the date codes of Chapter 17 (`2025-12`), and **`/`** between a `Path` and text joins them into a longer path (Chapter 17, section 17.9). The file name always contains the month, so two runs for different months can't overwrite each other.
- The type hints (`text: str`, `-> date`, `Mapping[str, str]`) are explained in section 29.6. `-> ReportConfig` on `from_env` names the class inside its own definition, which Python 3.14 allows.

Try it, one cell at a time. Build a configuration from a dictionary that stands in for the environment:

```python
from riverstone_report.config import ReportConfig, parse_month
from riverstone_report.errors import ConfigError

env = {"RIVERSTONE_DATABASE_URL": "postgresql+psycopg://user:secret@db.example/riverstone"}
config = ReportConfig.from_env("2025-12", env=env)
print(config.month, config.next_month, config.output_path)
```

```
2025-12-01 2026-01-01 reports/riverstone_monthly_2025-12.xlsx
```

(On Windows the path prints as `reports\riverstone_monthly_2025-12.xlsx`.) A month in the wrong format:

```python
try:
    parse_month("Dec 2025")
except ConfigError as exc:
    print("ConfigError:", exc)
```

```
ConfigError: month must look like YYYY-MM, got 'Dec 2025'
```

And the frozen data class at work. This cell fails on purpose:

```python
config.month = parse_month("2026-01")
```

```
dataclasses.FrozenInstanceError: cannot assign to field 'month'
```

Once a run's configuration is built, nothing can change it halfway through.

### A class with behavior: the API client

Section 29.9's `CrmClient` is a class for a different reason: it holds **state that several methods share** (the base URL, the API key, an open network session, retry settings) and it's created once and used many times. That's the test: **use a class when data and the functions that use it travel together.** For a calculation, a function is simpler. `transform.py` has no classes except the `MonthSummary` data class, and doesn't need any.

---

## 29.6 Type hints

A **type hint** declares what a variable, parameter, or return value is supposed to be: `def parse_month(text: str) -> date:` takes text and returns a date. Python **doesn't enforce** hints when the code runs; they're documentation that tools can check. Their value comes from a **type checker**, a program that reads your code without running it and reports places where the types can't work.

The hints this chapter uses:

| Hint | Means |
|---|---|
| `int`, `float`, `str`, `bool`, `date` | that type |
| `list[str]`, `dict[str, int]`, `tuple[float, float]` | a container of that type |
| `float \| None` | a float, or `None` (older code writes `Optional[float]`) |
| `SomeClass \| None` | an object of that class, or `None`, such as `requests.Session \| None` |
| `pd.DataFrame` | a pandas DataFrame (checked with the `pandas-stubs` package) |
| `Mapping[str, str]` | anything dictionary-like that is only read: `os.environ` or a plain dict |
| `Iterator[X]` | something you loop over that hands out one `X` at a time (a generator, section 29.9) |
| `Callable[[float], None]` | a function taking a float and returning nothing (section 29.9) |
| `Any` | any type at all: the checker stops checking here |
| `-> None` | the function returns nothing |

`Mapping`, `Iterator`, and `Callable` are imported from `collections.abc`, and `Any` from `typing`, both in the standard library.

Here's `transform.py` with its data class and its hints, the second of its three versions:

<!-- run: none -->
```python
"""Pure calculations: DataFrames in, results out. No database, no files, so easy to test."""
from dataclasses import dataclass

import pandas as pd

REQUIRED_COLUMNS = {"order_id", "customer_name", "category", "net_revenue"}


@dataclass(frozen=True)
class MonthSummary:
    revenue: float
    orders: int
    customers: int
    target: float | None

    @property
    def pct_of_target(self) -> float | None:
        if not self.target:
            return None
        return round(100 * self.revenue / self.target, 1)


def check_lines(lines: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(lines.columns)
    if missing:
        raise ValueError(f"sales lines are missing columns: {sorted(missing)}")
    if lines.empty:
        raise ValueError("no sales lines for this month")


def summarize(lines: pd.DataFrame, target: float | None) -> MonthSummary:
    check_lines(lines)
    return MonthSummary(
        revenue=round(float(lines["net_revenue"].sum()), 2),
        orders=int(lines["order_id"].nunique()),
        customers=int(lines["customer_name"].nunique()),
        target=target,
    )


def revenue_by_category(lines: pd.DataFrame) -> pd.DataFrame:
    check_lines(lines)
    result = (lines.groupby("category", as_index=False)
                   .agg(net_revenue=("net_revenue", "sum"))
                   .sort_values(["net_revenue", "category"], ascending=[False, True],
                                ignore_index=True))
    total = result["net_revenue"].sum()
    result["share_pct"] = (100 * result["net_revenue"] / total).round(1)
    return result


def top_customers(lines: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    if n < 1:
        raise ValueError("n must be at least 1")
    check_lines(lines)
    totals = (lines.groupby("customer_name", as_index=False)
                   .agg(net_revenue=("net_revenue", "sum")))
    ranked = totals.sort_values(["net_revenue", "customer_name"], ascending=[False, True],
                                ignore_index=True)
    return ranked.head(n)
```

- **`import pandas as pd`** is back, because the hints name `pd.DataFrame`.
- **`-> None`** on `check_lines`: it returns nothing; it either passes quietly or raises.
- **`-> MonthSummary`** on `summarize`: the dictionary has become the data class.
- **`n: int = 5`**: a hint and a default together.

Why `.agg(net_revenue=("net_revenue", "sum"))` rather than a shorter spelling: the named aggregation always returns a DataFrame, which is what the hints promise, while some shorter pandas spellings return a Series in some cases, and the type checker would flag the mismatch.

Here's the bug a type checker is best at catching. Someone adds `headline.py`, a function to write a one-line headline for emails:

<!-- run: none -->
```python
def headline(summary: MonthSummary) -> str:
    gap = summary.pct_of_target - 100
    return f"Revenue ₹{summary.revenue:,.0f}, {gap:+.1f} points against target"
```

`{gap:+.1f}` shows the number with a sign and one decimal place: `+15.7`. It works for December. Run **`mypy`**, the most widely used Python type checker, in strict mode (the `[tool.mypy]` settings in `pyproject.toml`):

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run mypy
src/riverstone_report/headline.py:6: error: Unsupported operand types for - ("None" and "int")  [operator]
src/riverstone_report/headline.py:6: note: Left operand is of type "float | None"
Found 1 error in 1 file (checked 9 source files)
```

`pct_of_target` is `float | None`, because a month can have no target. For such a month the function would crash with a `TypeError`, on the day the email goes out. `mypy` found it without a database, a test, or a run. The fix handles the `None` case explicitly:

<!-- run: none -->
```python
"""A one-line headline for emails (section 29.6)."""
from riverstone_report.transform import MonthSummary


def headline(summary: MonthSummary) -> str:
    if summary.pct_of_target is None:
        return f"Revenue ₹{summary.revenue:,.0f} (no target set)"
    gap = summary.pct_of_target - 100
    return f"Revenue ₹{summary.revenue:,.0f}, {gap:+.1f} points against target"
```

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run mypy
Success: no issues found in 9 source files
```

After the `is None` check returns, `mypy` knows that `pct_of_target` must be a float on the next line.

> **Tool note.** Your editor uses the same hints: VS Code's Python extension underlines type errors as you type, and completes `summary.` with the right fields. Other checkers include **Pyright** (used by VS Code) and newer, faster ones appearing each year. Hints cost a few characters per function and pay back on every change, so add them to any code that more than one person maintains.

**Checkpoint.** In `work/ch29/riverstone-report`, `uv run mypy` says *Success*, and `uv run python -c "import riverstone_report"` prints nothing, which means the package imports cleanly.

> **Stop here: sitting 2 of 4.** You can set up a project with uv, reproduce it from its lockfile, write a small class or data class, and let `mypy` check your hints.

---

## 29.7 Testing with pytest

A **test** is code that runs your code with known inputs and checks the result. **`pytest`** is the standard Python test runner: it finds files named `test_*.py`, runs every function named `test_*`, and reports what failed. Tests turn *"I think it still works"* into a command anyone can run. Chapter 17's exercise 28 wrote a few `assert` lines in a file; pytest is the same idea, organized.

### A first test

In `work/ch29/riverstone-report`, create the file `tests/test_first.py` with one test in it:

<!-- run: none -->
```python
import pandas as pd

from riverstone_report.transform import summarize


def test_orders_counted():
    lines = pd.DataFrame({
        "order_id":      [1, 1, 2, 3, 3],
        "customer_name": ["Sharma Hardware", "Sharma Hardware", "Metro Mart",
                          "Green Leaf Hotels", "Green Leaf Hotels"],
        "category":      ["Storage", "Kitchen", "Storage", "Kitchen", "Furniture"],
        "net_revenue":   [10000.0, 2500.0, 6000.0, 1500.0, 5000.0],
    })
    summary = summarize(lines, 20000.0)
    assert summary.orders == 3
```

- A test is an ordinary function whose name starts with `test_`. It builds its own data, calls the code, and checks the answer.
- **`assert condition`** does nothing when the condition is true, and stops the test with a failure when it's false.
- The file imports `summarize` from the package. That works in a test for the same reason it worked in your notebook: `uv sync` installed the package into `.venv` in editable mode.

Run it, asking for one line per test with `-v` (verbose):

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run pytest tests/test_first.py -v
============================= test session starts ==============================
…
cachedir: .pytest_cache
…
configfile: pyproject.toml
plugins: platformdirs-4.12.1
collecting ... collected 1 item

tests/test_first.py::test_orders_counted PASSED                          [100%]

============================== 1 passed in 0.18s ===============================
```

*(Shortened: the two lines left out show folders on your computer.)* Read the header once:

- The first line left out starts with **`platform`**: your operating system and the versions of Python, pytest, and pluggy (a part of pytest), and, with `-v`, the full path of the Python it ran. The next run shows it without the path.
- **`cachedir`** is where pytest remembers the last run. The second line left out is **`rootdir`**, the project folder.
- **`configfile: pyproject.toml`** says pytest read its settings from there; **`plugins`** lists extras that other installed packages add to pytest, which you can ignore.
- **`collected 1 item`**: pytest found one test.

Then the result. **`tests/test_first.py::test_orders_counted`** is the test's **node ID**: the file, two colons, the function. Any node ID can be run on its own: `uv run pytest tests/test_first.py::test_orders_counted`.

### A failing test

Before you run it, predict what pytest will print if the test expects the wrong number. Change the last line to `assert summary.orders == 5` and run the file again, without `-v`:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run pytest tests/test_first.py
============================= test session starts ==============================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
…
configfile: pyproject.toml
plugins: platformdirs-4.12.1
collected 1 item

tests/test_first.py F                                                    [100%]

=================================== FAILURES ===================================
_____________________________ test_orders_counted ______________________________

    def test_orders_counted():
        lines = pd.DataFrame({
            "order_id":      [1, 1, 2, 3, 3],
            "customer_name": ["Sharma Hardware", "Sharma Hardware", "Metro Mart",
                              "Green Leaf Hotels", "Green Leaf Hotels"],
            "category":      ["Storage", "Kitchen", "Storage", "Kitchen", "Furniture"],
            "net_revenue":   [10000.0, 2500.0, 6000.0, 1500.0, 5000.0],
        })
        summary = summarize(lines, 20000.0)
>       assert summary.orders == 5
E       assert 3 == 5
E        +  where 3 = MonthSummary(revenue=25000.0, orders=3, customers=3, target=20000.0).orders

tests/test_first.py:15: AssertionError
=========================== short test summary info ============================
FAILED tests/test_first.py::test_orders_counted - assert 3 == 5
============================== 1 failed in 0.23s ===============================
```

Read it from the top:

- Without `-v`, each test is one character: **`F`** for failed (a pass is a dot).
- Under **FAILURES**, pytest prints the failing test's code, with **`>`** on the line that failed.
- The **`E`** lines are the explanation: `assert 3 == 5` is the comparison with the real values filled in, and `where 3 = MonthSummary(...).orders` says where the 3 came from.
- **`tests/test_first.py:15`** is the file and line number.
- The **short test summary** repeats every failure in one line, which is what you read first when there are many.

For a shorter report, add **`--tb=short`** (the traceback, shortened to the failing line and the `E` lines) and **`-q`** (quiet: no header). You'll use both below. Change the line back to `== 3` before going on.

### Fixtures: shared test data

A second test needs the same five lines. Instead of copying them, move them into a **fixture**: a function marked **`@pytest.fixture`** that builds test data. A test asks for a fixture by using its name as a parameter, and pytest calls the fixture and passes in the result. Replace `tests/test_first.py` with:

<!-- run: none -->
```python
import pandas as pd
import pytest

from riverstone_report.transform import summarize


@pytest.fixture
def lines():
    return pd.DataFrame({
        "order_id":      [1, 1, 2, 3, 3],
        "customer_name": ["Sharma Hardware", "Sharma Hardware", "Metro Mart",
                          "Green Leaf Hotels", "Green Leaf Hotels"],
        "category":      ["Storage", "Kitchen", "Storage", "Kitchen", "Furniture"],
        "net_revenue":   [10000.0, 2500.0, 6000.0, 1500.0, 5000.0],
    })


def test_orders_counted(lines):
    assert summarize(lines, 20000.0).orders == 3


def test_revenue_added_up(lines):
    assert summarize(lines, 20000.0).revenue == 25000.0
```

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run pytest tests/test_first.py -v
…
collecting ... collected 2 items

tests/test_first.py::test_orders_counted PASSED                          [ 50%]
tests/test_first.py::test_revenue_added_up PASSED                        [100%]

============================== 2 passed in 0.22s ===============================
```

pytest calls `lines()` afresh for each test, so one test can't spoil the data for the next. A fixture that several test files need goes in **`tests/conftest.py`**, a file pytest loads automatically; its fixtures are available to every test file without an import. The finished package's `conftest.py` has exactly this `lines` fixture, with a docstring: *"Five order lines from three orders: small enough to check every number by hand."* And its `tests/test_transform.py` already has these two checks, in a test named `test_summarize_counts_orders_not_lines`. So delete `tests/test_first.py`: it has done its job.

### Testing many cases and testing failures

`tests/test_config.py` tests `config.py` with two more tools:

<!-- run: none -->
```python
from datetime import date
from pathlib import Path

import pytest

from riverstone_report.config import ReportConfig, parse_month
from riverstone_report.errors import ConfigError


@pytest.mark.parametrize("text, expected", [("2025-12", date(2025, 12, 1)),
                                            ("2026-01", date(2026, 1, 1))])
def test_parse_month(text, expected):
    assert parse_month(text) == expected


@pytest.mark.parametrize("bad", ["Dec 2025", "2025-13", "2025", ""])
def test_parse_month_rejects_bad_input(bad):
    with pytest.raises(ConfigError):
        parse_month(bad)


def test_from_env_needs_database_url():
    with pytest.raises(ConfigError, match="RIVERSTONE_DATABASE_URL"):
        ReportConfig.from_env("2025-12", env={})


def test_december_rolls_into_next_year():
    env = {"RIVERSTONE_DATABASE_URL": "postgresql://example"}
    config = ReportConfig.from_env("2025-12", env=env)
    assert config.next_month == date(2026, 1, 1)
    assert config.output_path == Path("reports/riverstone_monthly_2025-12.xlsx")
```

- **`@pytest.mark.parametrize("text, expected", [...])`** runs one test function once per item in the list, passing each item's values in as `text` and `expected`. Four bad month formats are four separate test results.
- **`with pytest.raises(ConfigError):`** passes only if the code inside raises `ConfigError`. Testing that `parse_month("2025-13")` fails *the right way* is as important as testing that `"2025-12"` works, because the original script's bugs were all on the failure path.
- **`match="RIVERSTONE_DATABASE_URL"`** also checks that the error message contains that text, so the message stays helpful.
- `env={}` tests a missing environment variable without touching the real environment.

Run the file with `-v` to see every case:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run pytest tests/test_config.py -v
…
collecting ... collected 8 items

tests/test_config.py::test_parse_month[2025-12-expected0] PASSED         [ 12%]
tests/test_config.py::test_parse_month[2026-01-expected1] PASSED         [ 25%]
tests/test_config.py::test_parse_month_rejects_bad_input[Dec 2025] PASSED [ 37%]
tests/test_config.py::test_parse_month_rejects_bad_input[2025-13] PASSED [ 50%]
tests/test_config.py::test_parse_month_rejects_bad_input[2025] PASSED    [ 62%]
tests/test_config.py::test_parse_month_rejects_bad_input[] PASSED        [ 75%]
tests/test_config.py::test_from_env_needs_database_url PASSED            [ 87%]
tests/test_config.py::test_december_rolls_into_next_year PASSED          [100%]

============================== 8 passed in 0.30s ===============================
```

Each parametrized case gets its own node ID, with the values in square brackets: `[Dec 2025]` is the bad input. A value pytest can't write simply, such as a date, becomes the parameter's name and a number: `expected0`, `expected1`. The empty string shows as `[]`. If one case fails, pytest names the input that failed.

### The integration test: reconcile to a known number

Unit tests use made-up data. One test should prove the whole path works against the real database, and the best check is one this book already trusts: December 2025's net revenue of ₹4,39,823.50, 115.7% of its ₹3,80,000 target (Chapter 28's answer to exercise 11). That test is `tests/test_reconcile.py`:

<!-- run: none -->
```python
"""Integration test: runs only when RIVERSTONE_DATABASE_URL points at riverstone_2025."""
import os

import pytest
from sqlalchemy import create_engine

from riverstone_report import db, transform
from riverstone_report.config import ReportConfig

pytestmark = pytest.mark.skipif(not os.environ.get("RIVERSTONE_DATABASE_URL"),
                                reason="no database configured")


def test_december_2025_matches_the_book():
    config = ReportConfig.from_env("2025-12")
    engine = create_engine(config.database_url)
    lines = db.fetch_sales_lines(engine, config.month, config.next_month)
    summary = transform.summarize(lines, db.fetch_target(engine, config.month))
    assert summary.revenue == 439823.50
    assert summary.pct_of_target == 115.7
    categories = transform.revenue_by_category(lines)
    assert categories["net_revenue"].sum() == pytest.approx(summary.revenue)
```

- **`pytestmark = pytest.mark.skipif(condition, reason=...)`** applies to every test in the file: if the condition is true (no database URL is set), pytest skips them instead of running them. The fast unit tests still run anywhere, on a colleague's laptop or in the automated check below.
- **`pytest.approx(summary.revenue)`**: decimal numbers that should be equal can differ in the fifteenth digit after a sum (Chapter 17, section 17.3), so `approx` allows a tiny tolerance. The categories' total must equal the summary's revenue, to within a whisker.

### Running the tests

Run the whole suite with `-v`, reading the database settings from `.env`, and the output lists every test by name, which is a fair description of what the package promises:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run --env-file .env pytest -v
…
configfile: pyproject.toml
testpaths: tests
plugins: platformdirs-4.12.1
collecting ... collected 23 items

tests/test_config.py::test_parse_month[2025-12-expected0] PASSED         [  4%]
tests/test_config.py::test_parse_month[2026-01-expected1] PASSED         [  8%]
tests/test_config.py::test_parse_month_rejects_bad_input[Dec 2025] PASSED [ 13%]
tests/test_config.py::test_parse_month_rejects_bad_input[2025-13] PASSED [ 17%]
tests/test_config.py::test_parse_month_rejects_bad_input[2025] PASSED    [ 21%]
tests/test_config.py::test_parse_month_rejects_bad_input[] PASSED        [ 26%]
tests/test_config.py::test_from_env_needs_database_url PASSED            [ 30%]
tests/test_config.py::test_december_rolls_into_next_year PASSED          [ 34%]
tests/test_crm_client.py::test_follows_pages_until_next_page_is_none PASSED [ 39%]
tests/test_crm_client.py::test_retries_server_errors_then_succeeds PASSED [ 43%]
tests/test_crm_client.py::test_honors_retry_after_on_429 PASSED          [ 47%]
tests/test_crm_client.py::test_does_not_retry_a_bad_api_key PASSED       [ 52%]
tests/test_crm_client.py::test_gives_up_after_max_attempts PASSED        [ 56%]
tests/test_reconcile.py::test_december_2025_matches_the_book PASSED      [ 60%]
tests/test_transform.py::test_summarize_counts_orders_not_lines PASSED   [ 65%]
tests/test_transform.py::test_no_target_gives_no_percentage PASSED       [ 69%]
tests/test_transform.py::test_categories_are_sorted_and_shares_add_up PASSED [ 73%]
tests/test_transform.py::test_top_customers[1-expected0] PASSED          [ 78%]
tests/test_transform.py::test_top_customers[2-expected1] PASSED          [ 82%]
tests/test_transform.py::test_top_customers_rejects_zero PASSED          [ 86%]
tests/test_transform.py::test_empty_month_raises_no_data PASSED          [ 91%]
tests/test_transform.py::test_missing_column_is_reported PASSED          [ 95%]
tests/test_transform.py::test_zero_target_gives_no_percentage PASSED     [100%]

============================== 23 passed in 0.36s ==============================
```

`testpaths: tests` is the setting from `pyproject.toml`: with no file named, pytest looked in `tests`. The client tests belong to section 29.9. Now run it the way a colleague without the database would, without `.env` and without `-v`:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run pytest
============================= test session starts ==============================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
…
configfile: pyproject.toml
testpaths: tests
plugins: platformdirs-4.12.1
collected 23 items

tests/test_config.py ........                                            [ 34%]
tests/test_crm_client.py .....                                           [ 56%]
tests/test_reconcile.py s                                                [ 60%]
tests/test_transform.py .........                                        [100%]

======================== 22 passed, 1 skipped in 0.26s =========================
```

Each dot is a passing test and the **`s`** is the skipped integration test. 23 tests in under half a second, so there's no reason not to run them after every change.

### What a failure looks like

Suppose someone "simplifies" `summarize` and writes `orders=len(lines)`, counting lines instead of orders:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run pytest -q --tb=short tests/test_transform.py
F........                                                                [100%]
=================================== FAILURES ===================================
____________________ test_summarize_counts_orders_not_lines ____________________
tests/test_transform.py:11: in test_summarize_counts_orders_not_lines
    assert summary.orders == 3
E   assert 5 == 3
E    +  where 5 = MonthSummary(revenue=25000.0, orders=5, customers=3, target=20000.0).orders
=========================== short test summary info ============================
FAILED tests/test_transform.py::test_summarize_counts_orders_not_lines - asse...
1 failed, 8 passed in 0.24s
```

The test's name says what rule was broken, and the output shows the wrong value (5) and where it came from. This is the fan-out mistake from Chapter 12, caught in a quarter of a second instead of in a board meeting.

![A diagram with cli.py at the top calling config.py, db.py, transform.py, and excel.py; db.py connects to PostgreSQL and excel.py writes to a reports folder, while transform.py is highlighted as tested with a 5-row DataFrame](figures/fig29-2-pure-core-layers.svg)

*Figure 29.2 — The design that makes testing cheap: business rules in pure functions, input and output at the edges.*

![Three bands: 14 unit tests for transform, config, and the API client with a fake session; 3 parametrized test functions expanding to 8 cases; 1 integration test against riverstone_2025 that is skipped without a database](figures/fig29-3-tests-by-kind.svg)

*Figure 29.3 — Many fast tests on the pure core, a few slow ones on the edges.*

### What to test

- **Business rules**: every calculation someone would argue about (what counts as an order, how shares round, what happens with no target).
- **Edge cases**: empty input, a single row, ties, the last month of the year, `None`.
- **Failures**: bad input raises the right exception with a helpful message.
- **One reconciliation** against a known total, run when the database is available.
- **Not** third-party libraries (pandas' `groupby` is tested by pandas), and not every line for its own sake. A number called "coverage" measures which lines tests ran (`pytest-cov` reports it); treat it as a way to find untested code, not as a target.

> **Where this leads.** Chapter 47 applies the same idea to data itself: automated checks that run against every day's data, not only against your code.

### Run the tests on every push

Chapter 26, section 26.8, set up an automated check that runs on every push and every pull request. Now the project has tests, a lockfile, and a type checker, so the check can run all three. The workflow file goes at the top of the repository that holds the package, as `.github/workflows/checks.yml`; for a package in a repository of its own, as `uv init` makes it (section 29.4), that's the package folder:

<!-- run: none -->
```yaml
name: checks
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: astral-sh/setup-uv@v10.2.0
      - run: uv sync --locked
      - run: uv run pytest -q
      - run: uv run mypy
```

What changed from Chapter 26's version (the job name, `check`, and the `checkout` line stay the same):

- **`uses: astral-sh/setup-uv@v10.2.0`** installs uv on the fresh machine. It replaces `actions/setup-python`: uv reads `.python-version` and fetches that Python itself. The action publishes no short `@v10` tag, so the full version is pinned instead of the major version Chapter 26 recommends: a stricter pin, updated the same way. (10.2.0 was the current version on 28 September 2026; check the action's page for newer ones.)
- **`run: uv sync --locked`** replaces `pip install -r requirements.txt`: the machine gets exactly the versions in `uv.lock`, and the check fails if `pyproject.toml` and the lockfile disagree.
- **`run: uv run pytest -q`** runs the tests quietly. The machine has no database and no `.env`, so the integration test shows as skipped, and 22 tests must pass.
- **`run: uv run mypy`** fails the check if a type error comes in. With the `pytest` step, it replaces Chapter 26's `compileall` and `--help` steps.

If any step exits with a non-zero code, the check fails and the pull request shows a red cross, as in Chapter 26. These are the same three commands you can run yourself before pushing:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run pytest -q
.............s.........                                                  [100%]
22 passed, 1 skipped in 0.27s
$ uv run mypy
Success: no issues found in 9 source files
```

Push a change that breaks `summarize`, like the `len(lines)` one above, and the check's `pytest` step fails with the same report as on your machine; the pull request shows a red cross until it's fixed.

---

## 29.8 Errors and logging

### Fail loudly, with a reason

The script's worst line was `except: target = 0`. It caught *every* possible error (a typo in the SQL, a lost connection, even the user pressing Ctrl+C), replaced it with a plausible-looking wrong value, and carried on. The rules the package follows instead:

1. **Catch only exceptions you can do something about**, by name: `except ConfigError:`, never a bare `except:`.
2. **Don't turn an error into a default value** unless the default is truly correct. A missing target isn't zero; it's `None`, and the report says "no target set".
3. **Define your own exceptions** for failures the business cares about, so callers can handle them as a group.
4. **Stop at the top**: one place (the command-line entry point) catches `ReportError`, logs it, and exits with a non-zero **exit code** (Chapter 17, section 17.12, and Chapter 34). Schedulers, automated checks, and shell scripts read it.

The package's own exceptions are in `errors.py`, built by inheritance exactly as in section 29.5, with a docstring in place of `pass`:

<!-- run: none -->
```python
"""Exceptions the report can raise. Callers catch ReportError to handle any of them."""


class ReportError(Exception):
    """Base class for every expected failure of the monthly report."""


class ConfigError(ReportError):
    """A setting is missing or invalid."""


class NoDataError(ReportError):
    """The requested month has no sales, so a report would be misleading."""


class CrmApiError(ReportError):
    """The CRM API kept failing after all retries, or refused the request."""
```

Because `NoDataError` and `ConfigError` both inherit from `ReportError`, `except ReportError` handles all of them, while a genuine bug (a `KeyError`, say) is *not* caught and crashes with a full traceback, which is what you want for a bug.

That gives `transform.py` its third and final version. An empty month is an expected failure, not a bug, so `check_lines` raises `NoDataError` for it instead of `ValueError`; a missing column stays a `ValueError`, because it means the code or the query is wrong. Two lines change:

<!-- run: none -->
```python
from riverstone_report.errors import NoDataError      # added below "import pandas as pd"

    if lines.empty:
        raise NoDataError("no sales lines for this month")    # was ValueError
```

Try it in the notebook, with the package's `summarize`:

```python
from riverstone_report.errors import NoDataError, ReportError
from riverstone_report.transform import summarize

try:
    summarize(lines.iloc[0:0], target=380000.0)
except ReportError as exc:
    print(type(exc).__name__, "is a ReportError:", exc)
    print(isinstance(exc, NoDataError))
```

```
NoDataError is a ReportError: no sales lines for this month
True
```

`lines.iloc[0:0]` is section 29.2's empty month. **`type(exc).__name__`** is the name of the exception's class, so the message says which kind of `ReportError` arrived.

### Logging, one logger per module

Chapter 18 (section 18.15) and Chapter 20 (section 20.11) replaced `print` with **logging**: messages with a **level**, a timestamp, and a logger's name, configured once by `logging.basicConfig`, with `%s` placeholders instead of f-strings. The five levels, with an example of each from the report:

| Level | Use for | Example from the report |
|---|---|---|
| `DEBUG` | detail you only want while investigating | the SQL parameters used |
| `INFO` | normal progress worth a record | "read 35 sales lines for 2025-12" |
| `WARNING` | something odd that was handled | an API call failed and will be retried |
| `ERROR` | this run failed | "no sales lines for this month" |
| `CRITICAL` | the whole system is in trouble | rarely used in reports |

A package adds one habit. Each module asks for its own logger with **`logging.getLogger(__name__)`**. Inside a module, `__name__` is the module's full name (section 29.2), so the logger in `cli.py` is called `riverstone_report.cli` and the one in `crm_client.py` is `riverstone_report.crm_client`, and every log line says which file wrote it. Only the program's entry point decides where messages go and which levels to show.

### The write job

The fourth job, writing the workbook, is `excel.py`. It's Chapter 18's formatting (section 18.12), in one function:

<!-- run: none -->
```python
"""Writing the formatted workbook."""
from pathlib import Path

import pandas as pd
from openpyxl.styles import Font

from riverstone_report.transform import MonthSummary

RUPEES = '"₹"#,##0'


def write_report(summary: MonthSummary, categories: pd.DataFrame,
                 customers: pd.DataFrame, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    headline = pd.DataFrame({
        "metric": ["Net revenue", "Orders", "Customers", "Target", "% of target"],
        "value": [summary.revenue, summary.orders, summary.customers,
                  summary.target, summary.pct_of_target],
    })
    sheets = [("Summary", headline), ("Categories", categories), ("Top customers", customers)]
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet, frame in sheets:
            frame.to_excel(writer, sheet_name=sheet, index=False)
            ws = writer.sheets[sheet]
            for cell in ws[1]:
                cell.font = Font(bold=True)
            ws.column_dimensions["A"].width = 26
            ws.column_dimensions["B"].width = 16
        for row in (2, 5):
            writer.sheets["Summary"].cell(row=row, column=2).number_format = RUPEES
        for sheet in ("Categories", "Top customers"):
            for cell in writer.sheets[sheet]["B"][1:]:
                cell.number_format = RUPEES
    return path
```

- **`path.parent.mkdir(parents=True, exist_ok=True)`** makes the output folder, and any missing folders above it, if they aren't there yet.
- **`headline`** is the Summary sheet as a two-column table, built from the `MonthSummary`; a month with no target leaves the last two cells empty.
- **`pd.ExcelWriter(path, engine="openpyxl")`** opens one workbook for all three sheets; **`writer.sheets[sheet]`** is the openpyxl worksheet just written, which is where the formatting goes.
- **`ws[1]`** is the first row: the headers, made bold. **`column_dimensions["A"].width`** widens columns A and B.
- **`RUPEES = '"₹"#,##0'`** is an Excel number format: a ₹ sign and thousands separators, no decimals. It's applied to the revenue and target cells (rows 2 and 5 of the Summary) and to column B of the other two sheets, skipping the header (`[1:]`).
- It returns the path it wrote, so the caller can log it.

### The entry point

`cli.py` puts the jobs together and is the one place that catches `ReportError`:

<!-- run: none -->
```python
"""Command-line entry point: riverstone-report --month 2025-12"""
import argparse
import logging
import sys

from sqlalchemy import create_engine

from riverstone_report import db, excel, transform
from riverstone_report.config import ReportConfig
from riverstone_report.errors import ReportError

log = logging.getLogger(__name__)


def run(config: ReportConfig) -> None:
    engine = create_engine(config.database_url)
    lines = db.fetch_sales_lines(engine, config.month, config.next_month)
    log.info("read %d sales lines for %s", len(lines), f"{config.month:%Y-%m}")
    summary = transform.summarize(lines, db.fetch_target(engine, config.month))
    path = excel.write_report(summary, transform.revenue_by_category(lines),
                              transform.top_customers(lines, config.top_n), config.output_path)
    log.info("net revenue %.2f from %d orders; wrote %s",
             summary.revenue, summary.orders, path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="riverstone-report",
                                     description="Build Riverstone's monthly sales report.")
    parser.add_argument("--month", required=True, help="the month to report, as YYYY-MM")
    parser.add_argument("--verbose", action="store_true", help="show debug messages")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    try:
        run(ReportConfig.from_env(args.month))
    except ReportError as exc:
        log.error("%s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

How it works:

- **`run(config)`** is the four jobs in order: connect, read, transform, write. It knows nothing about the command line, so a test or another program can call it with any `ReportConfig`.
- **`argparse.ArgumentParser(prog=..., description=...)`**, from Chapter 18, section 18.15: `prog` is the command's name and `description` one line about it, both printed by `--help`.
- **`add_argument("--month", required=True, ...)`**: an option written with two dashes is normally optional; `required=True` makes argparse refuse to run without it.
- **`add_argument("--verbose", action="store_true", ...)`** is a switch with no value, as in Chapter 20: `True` if typed, `False` if not. Here it turns on `DEBUG` messages.
- **`parse_args(argv)`**: when `argv` is `None`, the default, argparse reads the real command line. A list lets a test call `main(["--month", "2025-12"])` without a terminal.
- **`format="%(asctime)s %(levelname)s %(name)s: %(message)s"`** puts the time, the level, the logger's name, and the message on each line.
- **`log.info("read %d sales lines for %s", len(lines), ...)`** fills the placeholders from the values after the message. Three placeholders appear in this file:

| Placeholder | Shows |
|---|---|
| `%d` | a whole number: `35` |
| `%s` | anything, as text: `2025-12` |
| `%.2f` | a number with two decimal places: `439823.50` |

- **`except ReportError`** is the one catch, at the top: it logs the reason and returns 1. Anything else is a bug, and crashes with its traceback.
- **`sys.exit(main())`** is the same as Chapter 17's `raise SystemExit(main())`: it ends the program with `main`'s return value as the exit code.

`--help` shows what argparse built from those lines:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run riverstone-report --help
usage: riverstone-report [-h] --month MONTH [--verbose]

Build Riverstone's monthly sales report.

options:
  -h, --help     show this help message and exit
  --month MONTH  the month to report, as YYYY-MM
  --verbose      show debug messages
$ uv run riverstone-report
usage: riverstone-report [-h] --month MONTH [--verbose]
riverstone-report: error: the following arguments are required: --month
$ echo "exit code: $?"
exit code: 2
```

Without `--month`, argparse stops before any of the report's code runs, and uses exit code 2, its code for "the command was typed wrongly".

The command now behaves like software a scheduler can trust. Run it for December, January, and a mistyped month, printing the exit code after each:

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run --env-file .env riverstone-report --month 2025-12
2026-09-28 19:11:00,876 INFO riverstone_report.cli: read 35 sales lines for 2025-12
2026-09-28 19:11:00,897 INFO riverstone_report.cli: net revenue 439823.50 from 18 orders; wrote reports/riverstone_monthly_2025-12.xlsx
$ echo "exit code: $?"
exit code: 0
$ uv run --env-file .env riverstone-report --month 2026-01
2026-09-28 19:11:01,656 INFO riverstone_report.cli: read 0 sales lines for 2026-01
2026-09-28 19:11:01,657 ERROR riverstone_report.cli: no sales lines for this month
$ echo "exit code: $?"
exit code: 1
$ uv run --env-file .env riverstone-report --month Dec-2025
2026-09-28 19:11:02,298 ERROR riverstone_report.cli: month must look like YYYY-MM, got 'Dec-2025'
$ echo "exit code: $?"
exit code: 1
```

January now fails with a reason and exit code 1, and writes nothing, so December's report is safe. The workbook for December is in `reports`; read it back in the notebook:

```python
import pandas as pd

report = pd.read_excel("riverstone-report/reports/riverstone_monthly_2025-12.xlsx", sheet_name=None)
for sheet, frame in report.items():
    print(sheet)
    print(frame, end="\n\n")
```

```
Summary
        metric     value
0  Net revenue  439823.5
1       Orders      18.0
2    Customers      15.0
3       Target  380000.0
4  % of target     115.7

Categories
     category  net_revenue  share_pct
0     Storage     220363.5       50.1
1     Kitchen     142180.0       32.3
2  Industrial      77280.0       17.6

Top customers
            customer_name  net_revenue
0  Northgate Distributors      75626.0
1         Prime Wholesale      65521.5
2        Sea Breeze Hotel      60675.0
3          Royal Banquets      38050.0
4        Deccan Packaging      37628.0
```

**`sheet_name=None`** reads every sheet, as a dictionary from sheet name to DataFrame (Chapter 18 read one sheet at a time). ₹4,39,823.50 from 18 orders and 15 customers, 115.7% of target, and the three categories add up to the total. ✓

To run it every month, schedule it the way Chapter 20, section 20.7, scheduled the Flash. A crontab line for 07:00 on the 2nd of each month, by the server's clock, reporting on the month before:

<!-- run: none -->
```bash
0 7 2 * *  cd /home/meera/riverstone-report && /home/meera/.local/bin/uv run --env-file .env riverstone-report --month "$(date -d 'last month' +\%Y-\%m)" >> cron.log 2>&1
```

- **`$(date -d 'last month' +\%Y-\%m)`** is Chapter 34's command substitution: on 2 February it becomes `2026-01`. The `%` signs are written `\%` because cron treats a bare `%` as a line break (Chapter 20).
- **`/home/meera/.local/bin/uv`** is uv by its full path, because cron's `PATH` is short (Chapter 34, section 34.6); `which uv` prints yours.
- When the month has no data, the command exits with 1, and the failure alert of Chapter 20, section 20.11, fires.

> **Watch out: never log secrets.** `log.info("connecting to %s", config.database_url)` writes the database password into a log file that many more people can read than the password itself. Log *which* database (`db.example/riverstone`), not the full connection string, and never log API keys or personal data.

> **Stop here: sitting 3 of 4.** You can write and run tests, read a failure, test the failure paths, and build a command that logs, fails loudly, and reports its result as an exit code.

---

## 29.9 Robust API clients

Chapter 18, section 18.14, called an API: it checked status codes, set a timeout, followed pages, and retried 429 and 5xx answers after a growing wait. Real APIs used by scheduled code need four more things:

1. **Pagination that can't lose a page.** An API returns large lists in **pages** (10, 100, or 1,000 items at a time) and tells you how to ask for the next one. A failure on page 3 must stop the run or be retried, never skip the page.
2. **Transient failures beyond status codes.** Servers restart, networks drop, gateways time out. The same request a second later usually works, even when no status code came back at all. These are errors worth **retrying**.
3. **Rate limits.** APIs cap how many requests you may make. Exceed it and you get **HTTP 429 Too Many Requests**, often with a **`Retry-After`** header saying how many seconds to wait.
4. **Retries you can test**, without waiting for real seconds to pass.

### The practice API

Riverstone's CRM (Chapter 3) isn't connected to anything you can reach, so the companion folder has a local stand-in, `mock_crm_api.py`. It serves the 43 leads from `riverstone_2025` at `GET /leads?page=N&page_size=M`, requires the header `X-API-Key: demo-key`, and misbehaves on purpose: the first request for page 2 gets **503 Service Unavailable**, and the first request for page 3 gets **429** with `Retry-After: 1`. It runs on your own machine and sends nothing anywhere.

A response looks like this:

```json
{"page": 5, "items": [{"lead_id": 41, "created_at": "2025-01-06T09:35:00", "company_name": "Crown Hotels", "source": "Referral"}], "next_page": null, "total": 43}
```

*(One item shown; page 5 has three.)*

Your notebook runs in `work/ch29`, the folder that holds `mock_crm_api.py`, so it can import it. **`start_server(8029)`** starts the mock API in the background of the notebook, listening at `http://127.0.0.1:8029` (127.0.0.1 always means "this computer", Chapter 34, section 34.9; 8029 is the port). It returns the server object and its address. **`server.shutdown()`** stops it and frees the port. If you ever see *Address already in use*, a server from an earlier cell is still running: restart the kernel.

### The naive client

Here's how most first API calls are written:

```python
import requests
from mock_crm_api import start_server

server, base_url = start_server(8029)

leads, page = [], 1
while page is not None:
    response = requests.get(f"{base_url}/leads", params={"page": page, "page_size": 10},
                            headers={"X-API-Key": "demo-key"})
    data = response.json()
    leads.extend(data["items"])
    page = data["next_page"]
print(len(leads))
```

```
KeyError: 'items'
```

In the notebook the error arrives as a traceback (Chapter 17, section 17.10). Its last lines are:

```text
---> 11     leads.extend(data["items"])
     12     page = data["next_page"]
     13 print(len(leads))

KeyError: 'items'
```

Page 2 returned a 503 whose body is `{"error": "temporarily unavailable"}`, the code never checked the status, and it crashed looking for a key that isn't there. Worse variants don't crash: they skip the page and report 33 leads as if that were all of them. And this call has **no timeout**: `requests` waits forever by default, so if the server stops responding, a scheduled job hangs until someone notices.

The robust client is built in five small steps below, each run against the mock API, and then gathered into one class.

### Step 1: one page, checked

Before you run it, predict which of the two `get_page` calls fails.

```python
from riverstone_report.errors import CrmApiError


def get_page(session, url, page):
    response = session.get(url, params={"page": page, "page_size": 10}, timeout=(3.05, 10.0))
    if response.status_code != 200:
        raise CrmApiError(f"{url} returned {response.status_code}")
    return response.json()


server.shutdown()
server, base_url = start_server(8029)          # a fresh server, with its planned failures reset
session = requests.Session()
session.headers["X-API-Key"] = "demo-key"

print(len(get_page(session, f"{base_url}/leads", 1)["items"]), "leads on page 1")
get_page(session, f"{base_url}/leads", 2)
```

```
10 leads on page 1
riverstone_report.errors.CrmApiError: http://127.0.0.1:8029/leads returned 503
```

- **`requests.Session()`** is an object that keeps one network connection open across requests and remembers settings. **`session.headers["X-API-Key"] = "demo-key"`** stores the key once; every request through the session sends it.
- **`params={"page": page, "page_size": 10}`** becomes the part of the address after `?`, as in Chapter 18.
- **`timeout=(3.05, 10.0)`**: give up if connecting takes more than about 3 seconds, or if the server goes silent for 10 once connected. Every network call in production code needs a timeout (Chapter 18).
- **`CrmApiError`** is the package's own exception (section 29.8), so the caller can catch it with the report's other failures.

### Step 2: retry, with `try`, `except`, and `else`

A request can fail in two different ways: the server answers with an error status, or no answer comes at all and `requests` raises an exception (`ConnectionError`, `Timeout`). Handling both neatly needs one more part of `try`, which Chapter 17 mentioned: **`else`** runs only if nothing in the `try` raised. A toy first:

```python
for text in ["430", "four"]:
    try:
        price = float(text)
    except ValueError:
        print(text, "-> not a number")
    else:
        print(text, "-> worked:", price)
```

```
430 -> worked: 430.0
four -> not a number
```

The `else` block is for code that should run only when the risky line succeeded. Keeping it out of the `try` means a mistake inside it isn't mistaken for the failure you meant to catch. Now the retrying version, with a fixed wait for the moment:

```python
import time

RETRY_STATUSES = {429, 500, 502, 503, 504}


def get_page_retrying(session, url, page, attempts=4):
    for attempt in range(1, attempts + 1):
        try:
            response = session.get(url, params={"page": page, "page_size": 10},
                                   timeout=(3.05, 10.0))
        except (requests.ConnectionError, requests.Timeout) as exc:
            problem = type(exc).__name__
        else:
            if response.status_code == 200:
                return response.json()
            if response.status_code not in RETRY_STATUSES:
                raise CrmApiError(f"{url} returned {response.status_code}")
            problem = f"HTTP {response.status_code}"
        print(f"attempt {attempt} for page {page} failed ({problem}); waiting 0.5 s")
        time.sleep(0.5)
    raise CrmApiError(f"page {page} failed after {attempts} attempts")


server.shutdown()
server, base_url = start_server(8029)
data = get_page_retrying(session, f"{base_url}/leads", 2)
print(len(data["items"]), "leads on page", data["page"])
```

```
attempt 1 for page 2 failed (HTTP 503); waiting 0.5 s
10 leads on page 2
```

- **`except (requests.ConnectionError, requests.Timeout) as exc:`** catches either of two exception types, listed in a tuple. `type(exc).__name__` records which one it was.
- In the **`else`** branch a response did arrive: 200 returns the data; a status not in **`RETRY_STATUSES`** (401 bad key, 403 not allowed, 404 wrong address) raises at once, because it will fail identically every time; anything else is noted as the problem and retried.
- After the loop, **`raise CrmApiError(...)`** gives up with a message. Retrying forever turns a failure into a hang.

### Step 3: exponential backoff with jitter

Chapter 18 waited 2, 4, 8, then 16 seconds. The same doubling from a smaller start is **exponential backoff**: 0.5 s after the first failure, then 1 s, then 2 s, so a struggling server gets breathing room. **Jitter** adds a random extra of up to half the wait, so a hundred clients that failed together don't all retry at the same instant. A **seed** makes the waits repeatable, as it made Chapter 21's samples repeatable; here the generator comes from the standard library's `random` module rather than from NumPy:

```python
import random

rng = random.Random(29)
for attempt in (1, 2, 3):
    base = 0.5 * 2 ** (attempt - 1)
    print(attempt, base, round(base + rng.uniform(0, base / 2), 3))
```

```
1 0.5 0.637
2 1.0 1.173
3 2.0 2.845
```

- **`2 ** (attempt - 1)`** is 1, 2, 4 (`**` is "to the power of"), so `base` is 0.5, 1.0, 2.0.
- **`rng.uniform(0, base / 2)`** is a random decimal number between 0 and half the base; **`random.Random(29)`** is a generator started from the seed 29, so it gives the same numbers every run.

What happens if you change the seed? The jitter changes, but every wait stays between the base and one and a half times it:

```python
rng = random.Random(30)
print([round(base + rng.uniform(0, base / 2), 3) for base in (0.5, 1.0, 2.0)])
```

```
[0.635, 1.145, 2.03]
```

The list comprehension (Chapter 17, section 17.6) runs the same calculation for each base. `round(..., 3)` dropped the last zero of 2.030.

### Step 4: respect `Retry-After`

A 429 often says exactly how long to wait. When it does, that beats any backoff:

```python
def wait_time(attempt, response, rng, backoff=0.5):
    if response is not None and response.status_code == 429:
        retry_after = response.headers.get("Retry-After", "")
        if retry_after.isdigit():
            return float(retry_after)
    base = backoff * 2 ** (attempt - 1)
    return round(base + rng.uniform(0, base / 2), 3)


page_3 = session.get(f"{base_url}/leads", params={"page": 3, "page_size": 10}, timeout=(3.05, 10.0))
print(page_3.status_code, page_3.headers["Retry-After"], wait_time(1, page_3, random.Random(29)))
print(wait_time(1, None, random.Random(29)))
```

```
429 1 1.0
0.637
```

- **`response.headers.get("Retry-After", "")`** reads the header, or an empty string if there isn't one. **`.isdigit()`** is `True` only for a whole number of seconds; the header can also be a date, which this version ignores (exercise 10).
- **`response is not None`** covers the case where no response arrived at all (a connection error): then there's no header to read, and the backoff decides.
- The first request for page 3 got its planned 429 with `Retry-After: 1`, so the wait is exactly 1 second. With no response, attempt 1 waits 0.637 s, as in step 3.

### Step 5: a generator hands out the leads

The caller wants leads, not pages. A **generator** is a function that hands out values one at a time with **`yield`** instead of returning them all at once; Python pauses it after each value and resumes it when the next one is wanted. A toy:

```python
def count_up(n):
    for i in range(n):
        yield i


def two_pages():
    yield from ["lead 1", "lead 2"]
    yield from ["lead 3"]


print(list(count_up(3)))
print(list(two_pages()))
```

```
[0, 1, 2]
['lead 1', 'lead 2', 'lead 3']
```

**`yield from`** hands out every item of a list (or of another generator), one by one. `list(...)` collects everything a generator yields; a `for` loop takes the items one at a time. A lead generator yields each page's items and then asks for the next page, so a caller can write `for lead in client.iter_leads():` without knowing pages exist.

### The robust client, as a class

The five steps share the same settings: the address, the key, the session, the number of attempts, the backoff, the random generator. That is section 29.5's test for a class: data and the functions that use it travel together. `crm_client.py` gathers the steps into one:

<!-- run: none -->
```python
"""A careful client for the CRM leads API: pages, timeouts, retries, backoff, rate limits."""
import logging
import random
import time
from collections.abc import Callable, Iterator
from typing import Any

import requests

from riverstone_report.errors import CrmApiError

log = logging.getLogger(__name__)

RETRY_STATUSES = {429, 500, 502, 503, 504}


class CrmClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        session: requests.Session | None = None,
        max_attempts: int = 4,
        backoff_seconds: float = 0.5,
        timeout: tuple[float, float] = (3.05, 10.0),
        sleep: Callable[[float], None] = time.sleep,
        rng: random.Random | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.session.headers["X-API-Key"] = api_key
        self.max_attempts = max_attempts
        self.backoff_seconds = backoff_seconds
        self.timeout = timeout
        self.sleep = sleep
        self.rng = rng or random.Random()

    def _wait_time(self, attempt: int, response: requests.Response | None) -> float:
        if response is not None and response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "")
            if retry_after.isdigit():
                return float(retry_after)
        base: float = self.backoff_seconds * 2 ** (attempt - 1)
        return round(base + self.rng.uniform(0, base / 2), 3)

    def get_json(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        for attempt in range(1, self.max_attempts + 1):
            response: requests.Response | None = None
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
            except (requests.ConnectionError, requests.Timeout) as exc:
                problem = type(exc).__name__
            else:
                if response.status_code == 200:
                    data: dict[str, Any] = response.json()
                    return data
                if response.status_code not in RETRY_STATUSES:
                    raise CrmApiError(
                        f"{url} returned {response.status_code}: {response.text[:100]}")
                problem = f"HTTP {response.status_code}"
            if attempt == self.max_attempts:
                raise CrmApiError(f"{url} failed after {attempt} attempts (last: {problem})")
            wait = self._wait_time(attempt, response)
            log.warning("attempt %d for %s failed (%s); retrying in %.3f s",
                        attempt, params, problem, wait)
            self.sleep(wait)
        raise AssertionError("unreachable")

    def iter_leads(self, page_size: int = 10) -> Iterator[dict[str, Any]]:
        page = 1
        while True:
            data = self.get_json("/leads", {"page": page, "page_size": page_size})
            yield from data["items"]
            if data["next_page"] is None:
                return
            page = data["next_page"]
```

How it works, beyond the five steps:

- **`*,`** in the parameter list means that everything after it must be passed by name: `CrmClient(url, key, max_attempts=6)`, never `CrmClient(url, key, None, 6)`. With six settings, names are the only readable way.
- **`session or requests.Session()`**: `or` gives the left value unless it's `None` (or empty), and otherwise the right one. So a caller may hand in a session, and a test does; normally the client makes its own. `rng or random.Random()` works the same way.
- **`base_url.rstrip("/")`** removes a trailing `/`, so `http://…/` and `http://…` both work when the path is added.
- **`_wait_time`** is step 4 as a method. The leading underscore is a convention meaning "internal: for this class's own use, not for callers".
- **`get_json`** is steps 2 and 4 together, for any path. It logs each retry as a `WARNING` instead of printing, sleeps with `self.sleep`, and on the last attempt raises `CrmApiError` with the last problem. A non-retryable status also includes the first 100 characters of the server's reply (`response.text[:100]`), which usually says why.
- **`raise AssertionError("unreachable")`** after the loop can never run: the loop always returns or raises. It's there for `mypy`, which checks that every path through a function returns a value of the promised type or raises.
- **`iter_leads`** is step 5: it yields each page's items and stops when **`next_page`** is `null` (`None` in Python).
- **`sleep` and `rng` are parameters.** Normally they're `time.sleep` and a real random generator. A test hands in its own, so a test of four retries runs instantly and checks the exact waits (below).

The same fetch, with the robust client, logging to the screen:

```python
import logging
import sys

from riverstone_report.crm_client import CrmClient

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s", force=True)

server.shutdown()
server, base_url = start_server(8029)

client = CrmClient(base_url, "demo-key", rng=random.Random(29))
leads = list(client.iter_leads(page_size=10))
print(len(leads), "leads; last:", leads[-1]["company_name"], leads[-1]["created_at"])
```

```
WARNING riverstone_report.crm_client: attempt 1 for {'page': 2, 'page_size': 10} failed (HTTP 503); retrying in 0.637 s
WARNING riverstone_report.crm_client: attempt 1 for {'page': 3, 'page_size': 10} failed (HTTP 429); retrying in 1.000 s
43 leads; last: Daily Fresh Mart 2025-11-25T10:50:00
```

`stream=sys.stdout` and `force=True` are Chapter 20's notebook settings for logging. Both failures were logged, waited out, and retried, and all 43 leads arrived. ✓ The 43 matches Chapter 13's count of lead records (30 real leads plus 13 duplicates, which is Chapter 13's Pattern 3 problem, not the client's). The waits were 0.637 s (0.5 s backoff plus jitter) and exactly 1 s for the 429.

![A timeline of seven requests: page 1 succeeds; page 2 returns 503, waits 0.637 seconds, then succeeds; page 3 returns 429, waits 1 second as Retry-After asked, then succeeds; pages 4 and 5 succeed, page 5 with next_page null. A side panel lists which errors to retry and how long to wait](figures/fig29-4-retries-and-pages.svg)

*Figure 29.4 — Retry what might work next time, wait sensibly, and stop when the API says there are no more pages.*

And the failure the client must *not* retry:

```python
from riverstone_report.errors import ReportError

bad_client = CrmClient(base_url, "wrong-key", rng=random.Random(29))
try:
    list(bad_client.iter_leads())
except ReportError as exc:
    print(type(exc).__name__ + ":", exc)
server.shutdown()
```

```
CrmApiError: http://127.0.0.1:8029/leads returned 401: {"error": "invalid or missing API key"}
```

No retries, no waiting: a wrong key won't become right in two seconds.

### Testing the client without a network

`tests/test_crm_client.py` tests every retry rule in a fraction of a second, with no server at all. It replaces the network with a **test double**: an object that stands in for a real one in a test. This kind, which gives canned answers, is called a **fake**:

<!-- run: none -->
```python
import random

import pytest
import requests

from riverstone_report.crm_client import CrmClient
from riverstone_report.errors import CrmApiError


class FakeResponse:
    """Just enough of a requests.Response for CrmClient: a status, headers, a body."""
    def __init__(self, status_code, body=None, headers=None):
        self.status_code = status_code
        self._body = body or {}
        self.headers = headers or {}
        self.text = str(self._body)

    def json(self):
        return self._body


class FakeSession:
    """Plays back a list of responses (or exceptions) instead of calling a real server."""
    def __init__(self, replies):
        self.replies = list(replies)
        self.headers = {}
        self.calls = []

    def get(self, url, params, timeout):
        self.calls.append(params)
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


def make_client(replies, sleeps):
    """A CrmClient that talks to a FakeSession and records its waits instead of sleeping."""
    return CrmClient("https://crm.example", "test-key", session=FakeSession(replies),
                     sleep=sleeps.append, rng=random.Random(29))


def test_retries_server_errors_then_succeeds():
    sleeps = []
    client = make_client([FakeResponse(503), requests.ConnectionError(),
                          FakeResponse(200, {"items": [], "next_page": None})], sleeps)
    assert list(client.iter_leads()) == []
    assert sleeps == [0.637, 1.173]
```

- **`FakeResponse`** has the four things `CrmClient` uses from a real response: `status_code`, `headers`, `text`, and `json()`. **`FakeSession`** has the one method it uses, `get`, which hands back the next reply in its list with **`pop(0)`**, or raises it if the reply is an exception. It also records each call's parameters in `calls`.
- **`make_client`** passes the fake session in, and **`sleep=sleeps.append`**: instead of sleeping, the client appends each wait to the list `sleeps`. A test of four retries takes no time, and the test can check the waits.
- The test plays back a 503, then a connection error, then success. The client must retry twice and end with no leads; with the seed 29, the waits are exactly 0.637 s and 1.173 s, as in step 3.

The file's other four tests follow the same pattern: pages followed until `next_page` is `None`, `Retry-After: 7` obeyed exactly, a 401 not retried, and four 500s giving up after four attempts.

<!-- run: none -->
```
# terminal, in work/ch29/riverstone-report
$ uv run pytest -q tests/test_crm_client.py
.....                                                                    [100%]
5 passed in 0.22s
```

> **Watch out: retries must be safe to repeat.** Reading leads twice does no harm. *Creating* an order twice does. A request that can be repeated without changing the outcome is **idempotent** (Chapter 20). GET requests normally are; POST requests that create things normally aren't. Before retrying a write, check whether the API supports an **idempotency key** (a unique id sent with the request so the server ignores duplicates). Chapter 51 covers writing to other systems safely.

> **Tool note.** `urllib3`'s `Retry` class can add retries and backoff to a `requests.Session` in a few lines, and the `tenacity` package provides retry decorators. **`httpx`** is a newer HTTP client with a similar interface that also supports asynchronous code. Writing the loop by hand once, as here, is how you learn what those tools configure.

---

## 29.10 Code review

**Code review** means another person reads a change before it's merged into the shared code. It catches bugs, but its bigger value is that at least two people understand every part of the system, and that standards spread without anyone writing a manual. On most teams, changes arrive as **pull requests** (Chapter 26): a set of commits with a description, which reviewers comment on line by line.

### As the author

1. **Keep changes small**: one purpose per pull request. A reviewer can check 200 lines properly; 2,000 lines get a skim and an approval.
2. **Explain the why** in the description, and how you tested it: *"Counts orders with nunique(), not rows. Added test_summarize_counts_orders_not_lines. Reconciles to ₹4,39,823.50 for December."*
3. **Run the checks first**: tests, type checker, formatter. Don't spend a reviewer's time on what a tool can find.
4. **Point to the risky part**: *"Please look closely at the retry logic."*

### As the reviewer

| Ask | For example, in this chapter's package |
|---|---|
| Is it correct for the business rule? | Orders counted with `nunique`; cancelled orders excluded (by the `sales_lines` view) |
| What happens on the failure path? | Empty month raises `NoDataError`; 401 not retried |
| Could it leak a secret or personal data? | No password in code or logs; `.env` in `.gitignore` |
| Is it tested, and do the tests test the rule? | A test named after the rule, with hand-checkable data |
| Will the next person understand it? | Names say what things are; comments say why |
| Does it handle scale? | Query filters by month in SQL, not in pandas |
| Is it the simplest thing that works? | A dataclass, not a class hierarchy |

**How to comment.** Comment on the code, never the person. Ask rather than instruct when you might be missing context (*"What happens if the target row is missing here?"*), label optional suggestions (*"nit:"* for trivial style points), and say what's good as well. Approve when the change is correct and safe, not when it's exactly how you'd have written it.

> **Real-life example: the review comment that saved a quarter's numbers.** A common catch in analytics teams: a pull request changes a revenue calculation to "include pending orders so the dashboard updates sooner". The code is clean and the tests pass, because the tests were updated too. The reviewer asks one question: *"Has finance agreed to count pending orders as revenue?"* They hadn't. Review isn't only about code; it's the moment someone checks that a business rule changed on purpose.

### Formatting and linting

Arguments about spacing and quote styles waste review time, so teams hand them to tools. A **formatter** rewrites code into a consistent style automatically, and a **linter** flags likely mistakes (unused imports, undefined names, a bare `except`). **Ruff** does both and is widely used with `uv` (`uv add --dev ruff`, then `uv run ruff check` and `uv run ruff format`). Run them before review, and in automated checks on every pull request (Chapter 32 does the same for SQL).

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| All code at the top level of one file | Importing it to test anything connects to the database and writes files | Functions in modules; a `__main__` block or entry point only in the CLI |
| Password or API key in the code | It appears in Git history, screenshots, and emails | Environment variables or a secrets manager; `.env` in `.gitignore` |
| Month or file name typed into the code | Every run edits code; reports overwrite each other | Command-line arguments; file names built from the settings |
| Installing packages into the system Python | Projects break each other; "works on my machine" | One virtual environment per project |
| No lockfile, or not committing it | A new install gets different versions and behaves differently | Commit `uv.lock` (or pinned requirements); install with `uv sync --locked` |
| SQL built by adding strings | Breaks on quotes; SQL injection | Query parameters |
| Bare `except:` or `except Exception: pass` | Wrong results with no error; Ctrl+C doesn't stop the program | Catch named exceptions you can handle; let bugs crash |
| Turning a failure into a default value (`target = 0`) | Plausible-looking wrong numbers | Raise, or use `None` and handle it visibly |
| `print` in scheduled code | No timestamps, no levels, nothing saved; scheduler thinks it succeeded | `logging`, and a non-zero exit code on failure |
| Calling `logging.basicConfig` inside a library module | Other programs' logging settings get overridden | Configure logging once, in the entry point |
| Tests that need the database for every calculation | Tests are slow, flaky, and skipped | Pure functions tested with tiny DataFrames; one integration test |
| Test data too large to check by hand | Nobody can tell whether the expected value is right | Five rows you can add up in your head |
| Tests that only cover the happy path | Failures surprise you in production | `pytest.raises` for bad input, empty data, and missing settings |
| No timeout on an HTTP call | A job hangs forever when the server stops responding | Always pass `timeout=` |
| Not checking the HTTP status | `KeyError`, or silently missing pages | Check `status_code`; raise or retry |
| Retrying every error, forever, immediately | Bans for hammering the API; hangs; duplicate writes | Retry only transient errors, with backoff, a limit, and `Retry-After` |
| Retrying non-idempotent requests | Duplicate records in the other system | Retry only safe requests, or use idempotency keys |
| Classes for everything | Code is harder to follow than the script it replaced | Functions for calculations; data classes for bundles; classes for shared state |
| Ignoring type checker errors about `None` | Crash on the first month with no target | Handle the `None` case explicitly |

---

## In the real world: the report that said January was zero

It's Tuesday, 3 February 2026. At 9:10 the managing director forwards Riverstone's monthly report to Anita Rao with one line: *"Revenue zero in January?"*

Meera Iyer runs the report. Since Imran left, it's a copy of his script, scheduled with Windows Task Scheduler to run on the second of each month. She opens the log folder: there isn't one. The scheduler's history says the task **completed successfully**. The shared drive has one file, `Monthly_Report_Dec_FINAL.xlsx`, dated yesterday, showing January with ₹0 revenue and a blank percentage of target.

It takes her an hour to piece together:

1. The load from the ERP to the reporting database had been failing since the last day of December, and nobody was alerted. The reporting copy had no January orders at all.
2. The script found no rows, summed them to zero, and divided zero by a target of zero, because `except: target = 0` had also hidden the fact that January's target row hadn't been entered yet.
3. It printed `done` and exited with code 0, so the scheduler recorded success.
4. It saved over the file with the fixed name, so December's good report was gone too. (IT restored it from the previous night's backup, as Chapter 2 hoped someone would.)

The data team reloads the database, and Meera reruns the script by hand. January's report goes out at 2 p.m., with the real numbers.

Then she fixes the cause, not the symptom, in three pull requests over the following two weeks, each reviewed by the data engineer:

- **Fail loudly.** The report became the package in this chapter. An empty month raises `NoDataError`, a missing target shows "no target set" instead of 0, and every failure exits with code 1. The scheduler now emails her when the exit code isn't 0.
- **Stop guessing.** Tests for the rules that bit her: orders counted, not lines; empty month; missing target; December rolling into January. And one reconciliation test against a month everyone agrees on.
- **Make it runnable by anyone.** The password moved into an environment variable on the report server. `uv.lock` pins the versions, so the server and her laptop run the same code. Output files are named by month, so no report can overwrite another.

On 2 March, the nightly load fails again. At 07:00 the report runs, logs `ERROR riverstone_report: no sales lines for this month`, exits with code 1, and Meera has an email before she reaches her desk. The MD never sees a wrong number.

**What she tells Anita:** *"The report used to succeed even when it had nothing to report. Now, if the data isn't there, it stops, tells me, and leaves last month's file alone. It also has tests for the rules finance cares about, so when someone changes a calculation, we'll know the same day."*

Notice that the fix wasn't clever code. It was ordinary habits: explicit failures, a meaningful exit code, tests for real rules, settings outside the code, and a second pair of eyes.

---

## Project: turn a script into a tested package

**Goal:** a script you (or your team) depend on becomes a package that someone else can install and run with one command, with tests that protect its business rules.

### Tools you'll need

Versions used for this chapter, checked on 28 September 2026:

- **Python 3.14.7**, as installed in Chapter 17. The package's `.python-version` asks for 3.14, and uv downloads it if it's missing.
- **uv 0.12.19** (released on 25 September 2026), installed from `docs.astral.sh/uv`. uv releases frequently; check the documentation for current installation commands.
- **Packages** (as locked in `uv.lock`): pandas 3.0.6, openpyxl 3.1.5, SQLAlchemy 2.1.1, psycopg 3.3.6, requests 2.34.2; for development, pytest 9.1.1, mypy 2.3.1, ipykernel 7.3.0, pandas-stubs, types-requests, types-openpyxl.
- **An editor with Python support**, such as VS Code with the Python and Jupyter extensions (runs tests and notebooks, shows type errors as you type).
- **Ruff** (optional) for formatting and linting.
- **Git and a GitHub account** (Chapter 26) for version control, pull requests, and the automated check.
- **Companion files** in `ch29/`: `start/monthly_report.py` (the starting script), `riverstone-report/` (the finished package with `pyproject.toml`, `uv.lock`, `.env.example`, source, and 23 tests), and `mock_crm_api.py` and `leads.json` (the practice API).

**Option A: your own script.** Choose a real script or notebook that produces something people use. Work in a private copy; remove passwords, server names, and personal data before sharing it with anyone, including in a portfolio.

**Option B: Riverstone.** Start from `start/monthly_report.py` and rebuild the package yourself in `work/ch29/mine/riverstone-report` (section 29.4) without looking at `riverstone-report/`, then compare.

**Steps:**

1. **List the problems** in the original, using section 29.1's table as a checklist.
2. **Create the project** with `uv init --package`, and add dependencies with `uv add`. Commit `pyproject.toml` and `uv.lock`.
3. **Split the jobs** into modules: configuration, reading, transforming (pure), writing, and a command-line entry point.
4. **Move settings out of the code**: arguments for each run, environment variables for secrets and machine-specific settings.
5. **Write tests first for the rules that matter**, with a fixture of five to ten rows you can check by hand. Include at least three failure cases.
6. **Add type hints** and get `uv run mypy` passing in strict mode.
7. **Replace print with logging**, catch your own exceptions at the entry point, and return an exit code.
8. **Reconcile** one real run against a number you already trust.
9. **Run the checks on every push**: add section 29.7's workflow to the repository, push, and confirm that the pull request shows a green check.
10. **Write a README**: what it does, how to install (`uv sync`), how to run, which environment variables it needs, how to run the tests.
11. **Ask someone to review it** with section 29.10's checklist, and act on the comments.

**Deliverables:** the repository with its passing check, the test output, the reconciliation, and a half-page note listing each problem from step 1 and how it was fixed.

**Stretch goals:**

- Add a `--dry-run` flag that runs everything except writing the file.
- Pull the month's new leads from the mock CRM API with `CrmClient` and add a "Leads by source" sheet.
- Add Ruff and a pre-commit hook that runs Ruff and the tests before every commit.

---

## Recap

- **Software** is code others can install, run, understand, change, and trust. The time to write it is when people depend on the output, it runs on a schedule, or someone else will change it.
- Split code into **functions** and **modules** with one job each. Keep business rules in **pure functions**; put databases, files, and networks at the edges.
- Use the **`src/` layout**, a **`pyproject.toml`**, and **environment variables** for secrets and machine settings. Use query **parameters**, never string-built SQL.
- A **virtual environment** isolates a project's packages; a **lockfile** pins every version. **`uv`** manages both (`uv add`, `uv sync --locked`, `uv run`); `venv` with pinned requirements is the universal fallback.
- A **class** is a template for objects: `__init__` sets an instance's attributes, **methods** receive the object as `self`, and **decorators** such as `@property` and `@classmethod` add behaviour. **Data classes** bundle values with names and types; **properties** calculate instead of storing; `frozen=True` prevents accidental changes.
- **Type hints** document intent, and **`mypy`** checks them without running code, catching bugs such as unhandled `None`.
- **`pytest`** runs `test_*` functions; **fixtures** supply fresh test data; **parametrize** tests many inputs; **`pytest.raises`** tests failures. Many fast unit tests, one reconciliation against a known total, and all of them run on every push.
- Catch **named exceptions**, never bare `except`. Define your own (`ReportError`), handle them at the entry point, and return an **exit code**. Use **logging** with levels, configured once, and never log secrets.
- **Robust API clients** use a session, **timeouts**, **pagination**, and **retries** for transient errors (429, 5xx, connection errors) with **exponential backoff**, **jitter**, **`Retry-After`**, and a limit. Retry only **idempotent** requests.
- **Code review**: small, explained changes; reviewers check rules, failures, secrets, tests, and clarity. Formatters and linters handle style.

---

## Key terms

software · script · pure function · module · docstring · package · `__name__` · SQL injection · query parameter · `src/` layout · `pyproject.toml` · TOML · entry point · environment variable · `.env` file · secrets manager · virtual environment · `venv` · lockfile · pinned requirements · `uv` · `uv.lock` · dependency group · dev dependency · editable install · class · instance · attribute · method · `self` · decorator · inheritance · class method · data class · immutable · property · alternative constructor · type hint · type checker · `mypy` · test · `pytest` · assertion · node ID · fixture · parametrize · unit test · integration test · coverage · exception · custom exception · exit code · logging · log level · logger · pagination · transient failure · rate limit · HTTP 429 · `Retry-After` · timeout · retry · exponential backoff · jitter · session · keyword-only argument · generator · test double · fake · idempotent · idempotency key · code review · pull request · formatter · linter · Ruff

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can say when a script should become a package, and when it shouldn't.
- [ ] My business calculations are pure functions that I can run on a five-row DataFrame.
- [ ] My projects have a `src/` layout, a `pyproject.toml`, and a committed lockfile.
- [ ] I can recreate a project's exact environment on a new machine with one command.
- [ ] No password or key appears in my code, my Git history, or my logs.
- [ ] I can write a small class with `__init__`, a method, and a property, and I use data classes for bundles of settings and results, and classes only when data and behavior belong together.
- [ ] I add type hints and fix what `mypy` finds, especially `None` cases.
- [ ] I write tests for business rules, edge cases, and failures, using fixtures and parametrize, and they run on every push.
- [ ] My scheduled code logs with levels and exits with a non-zero code on failure.
- [ ] My API clients set timeouts, follow pages, retry only transient errors with backoff, and respect `Retry-After`.
- [ ] I review code with a checklist, and write pull requests that are quick to review.

---

## Exercises

Run code exercises in your `ch29.ipynb` notebook in `work/ch29`, with the `riverstone-report/.venv` kernel (section 29.4), or inside the package with `uv run`. Exercises that need the database say so.

### Warm-up

1. Write a pure function `net_revenue(quantity: int, unit_price: float, discount_pct: float) -> float` that returns the net value of one order line, rounded to 2 decimal places. Check it on order 10005's line from Chapter 28: 15 boxes at ₹430 with 5% discount.
2. Predict what each call prints or raises, then run them: `parse_month("2025-02")`, `parse_month("2025-2")`, `parse_month("2025/02")`.
3. Read the starting script's `except:` block. Name three different problems that would all end up as `target = 0`.

### Core

4. Add a function `average_order_value(lines: pd.DataFrame) -> float` to your own copy of `transform.py`: net revenue divided by the number of orders, rounded to 2 decimals. What does it return for the five-line test DataFrame? Write its test.
5. Write a parametrized test for `net_revenue` from exercise 1 with three cases, including a 0% and a 100% discount.
6. Change the logging setup so that `INFO` and above go to the screen and `DEBUG` and above also go to a file called `report.log`. Show the code.
7. Use `CrmClient` against the mock API to count leads by `source`, most common first. How many leads came from the website?
8. Extend `ReportConfig.from_env` to read an optional `RIVERSTONE_TOP_N`. It must be a whole number from 1 to 20; anything else raises `ConfigError`. Show what happens with `"25"` and `"five"`.
9. `mypy` reports: `error: Argument 1 to "round" has incompatible type "float | None"; expected "_SupportsRound1[int]"  [arg-type]` for `round(summary.pct_of_target)`. Explain the problem in one sentence and fix the line.

### Stretch

10. A server sends `Retry-After: Wed, 21 Oct 2026 07:28:00 GMT` (a date instead of a number of seconds). What does `CrmClient._wait_time` do with it? Write a test that proves your answer.
11. Make `write_report` safe against half-written files: write to a temporary file in the same folder, then rename it to the final name. Explain why that matters for a report someone might open while it's being written.
12. The mock API can be started with a different failure plan: `start_server(failures={2: [500, 500, 500, 500]})`. Predict what `CrmClient` with the default settings does, then run it. How many seconds does it spend waiting, roughly?

### Think about it (no code needed)

13. A colleague says: *"Logging is overkill; my script prints what it's doing and I can see it."* When is she right, and when isn't she?
14. Give two situations where turning a script into a package with tests would be a waste of time.
15. You're reviewing a pull request that changes `revenue_by_category` to exclude the Furniture category "because it's being discontinued", with the test updated to match. What do you ask before approving?

---

## Answers

**1.**

<!-- py: reset -->

```python
def net_revenue(quantity: int, unit_price: float, discount_pct: float) -> float:
    """Net value of one order line, rounded to paise."""
    return round(quantity * unit_price * (1 - discount_pct / 100), 2)


print(net_revenue(15, 430, 5))
```

```
6127.5
```

₹6,127.50, the same as the hand check in section 28.7. ✓ It's pure: no database, no global variables, and the same inputs always give the same output.

**2.**

```python
from riverstone_report.config import parse_month
from riverstone_report.errors import ConfigError

for text in ["2025-02", "2025-2", "2025/02"]:
    try:
        print(text, "->", parse_month(text))
    except ConfigError as exc:
        print(text, "-> ConfigError:", exc)
```

```
2025-02 -> 2025-02-01
2025-2 -> 2025-02-01
2025/02 -> ConfigError: month must look like YYYY-MM, got '2025/02'
```

`"2025-2"` works, because `int("2")` is 2. `"2025/02"` fails because splitting on `-` gives one part, which can't be unpacked into `year, month`, a `ValueError` that `parse_month` turns into a `ConfigError`. If you want to insist on two-digit months, that's a rule to add *and* a test to write.

**3.** Any three of: the `sales_targets` table doesn't exist in the database the script connected to; the target row for that month hasn't been entered yet (`iloc[0, 0]` raises `IndexError`); a typo in the SQL; the database connection dropped; the value can't be converted to float; the user pressed Ctrl+C at that moment (a bare `except` even catches `KeyboardInterrupt`). They all need different responses, and the script gave every one of them the same wrong answer.

**4.**

```python
import pandas as pd


def average_order_value(lines: pd.DataFrame) -> float:
    orders = lines["order_id"].nunique()
    if orders == 0:
        raise ValueError("no orders to average")
    return round(float(lines["net_revenue"].sum()) / orders, 2)


lines = pd.DataFrame({
    "order_id":      [1, 1, 2, 3, 3],
    "customer_name": ["Sharma Hardware", "Sharma Hardware", "Metro Mart",
                      "Green Leaf Hotels", "Green Leaf Hotels"],
    "category":      ["Storage", "Kitchen", "Storage", "Kitchen", "Furniture"],
    "net_revenue":   [10000.0, 2500.0, 6000.0, 1500.0, 5000.0],
})
print(average_order_value(lines))
```

```
8333.33
```

₹25,000 ÷ 3 orders = ₹8,333.33. The common wrong answer is `lines["net_revenue"].mean()`, which averages *lines* (₹5,000). The tests, in `tests/test_transform.py`, where the `lines` fixture comes from `conftest.py`:

<!-- run: none -->
```python
import pytest

from riverstone_report.transform import average_order_value


def test_average_order_value_divides_by_orders(lines):
    assert average_order_value(lines) == 8333.33


def test_average_order_value_of_no_orders(lines):
    with pytest.raises(ValueError):
        average_order_value(lines.iloc[0:0])
```

**5.**

<!-- run: none -->
```python
import pytest

from riverstone_report.transform import net_revenue


@pytest.mark.parametrize("quantity, unit_price, discount_pct, expected", [
    (15, 430.0, 5.0, 6127.50),
    (20, 450.0, 0.0, 9000.00),
    (10, 380.0, 100.0, 0.00),
])
def test_net_revenue(quantity, unit_price, discount_pct, expected):
    assert net_revenue(quantity, unit_price, discount_pct) == expected
```

Three results in pytest's output, one per row. (This assumes you added `net_revenue` to `transform.py`.) Consider adding a case that should *fail*, such as a discount of 120%, and deciding whether `net_revenue` should raise for it.

**6.** Configure a handler for each destination, each with its own level, and set the logger's level to the lowest:

<!-- run: none -->
```python
import logging

formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logfile = logging.FileHandler("report.log", encoding="utf-8")
logfile.setLevel(logging.DEBUG)
logfile.setFormatter(formatter)

root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(console)
root.addHandler(logfile)
```

`encoding="utf-8"` lets the file hold `₹`, as in Chapter 20. This replaces `logging.basicConfig(...)` in `main`. A common mistake is setting only the handlers' levels: the logger's own level (default `WARNING`) is checked first, so `DEBUG` messages would never reach the file.

**7.**

```python
import random
from collections import Counter

from mock_crm_api import start_server
from riverstone_report.crm_client import CrmClient

server, base_url = start_server(8029, failures={})   # no planned failures for this exercise
client = CrmClient(base_url, "demo-key", rng=random.Random(7))
by_source = Counter(lead["source"] for lead in client.iter_leads(page_size=20))
server.shutdown()
for source, count in by_source.most_common():
    print(f"{source:<18} {count}")
print("total", sum(by_source.values()))
```

```
Website            27
Referral           5
Trade fair         5
Cold call          3
IndiaMART listing  3
total 43
```

27 of the 43 lead records came from the website. The counts include Chapter 13's duplicate lead records, because the API returns what the CRM holds; deduplicate (Chapter 13, Pattern 3) before reporting leads by source to anyone.

**8.**

<!-- run: none -->
```python
top_n_text = env.get("RIVERSTONE_TOP_N", "5")
if not top_n_text.isdigit() or not 1 <= int(top_n_text) <= 20:
    raise ConfigError(f"RIVERSTONE_TOP_N must be a whole number from 1 to 20, got {top_n_text!r}")
# then pass top_n=int(top_n_text) to cls(...)
```

With this added to `from_env`, a value of `"25"` raises *ConfigError: RIVERSTONE_TOP_N must be a whole number from 1 to 20, got '25'*, and `"five"` raises the same message with `'five'`. `isdigit()` is checked first, so `int()` is never called on text that isn't a number.

**9.** `pct_of_target` is `None` when a month has no target, and `round(None)` fails, so the code must decide what to show in that case: `round(summary.pct_of_target) if summary.pct_of_target is not None else "no target"`. After the `is not None` check, `mypy` knows the value is a float. `_SupportsRound1` is mypy's name for "anything that can be rounded"; `None` can't.

**10.** `"Wed, 21 Oct 2026 07:28:00 GMT".isdigit()` is `False`, so `_wait_time` ignores the header and falls back to exponential backoff. The HTTP standard allows `Retry-After` to be either a number of seconds or a date. The test, added to `tests/test_crm_client.py`:

<!-- run: none -->
```python
def test_retry_after_as_a_date_falls_back_to_backoff():
    sleeps = []
    client = make_client([FakeResponse(429, headers={"Retry-After": "Wed, 21 Oct 2026 07:28:00 GMT"}),
                          FakeResponse(200, {"items": [], "next_page": None})], sleeps)
    list(client.iter_leads())
    assert len(sleeps) == 1 and 0.5 <= sleeps[0] <= 0.75
```

With `backoff_seconds=0.5`, the first wait is 0.5 s plus jitter of up to 0.25 s. Supporting the date form is a reasonable improvement: parse it with `email.utils.parsedate_to_datetime` and wait until that moment.

**11.**

<!-- run: none -->
```python
import os
import tempfile

# inside write_report, replacing the direct write:
fd, temp_name = tempfile.mkstemp(suffix=".xlsx", dir=path.parent)
os.close(fd)
temp_path = Path(temp_name)
try:
    with pd.ExcelWriter(temp_path, engine="openpyxl") as writer:
        ...                                   # the same sheets and formatting as before
    os.replace(temp_path, path)              # swap in the finished file in one step
except BaseException:
    temp_path.unlink(missing_ok=True)
    raise
```

**`tempfile.mkstemp(suffix=".xlsx", dir=path.parent)`** creates an empty temporary file with that ending, in the report's own folder, and returns an open file number and the file's name; **`os.close(fd)`** closes it so pandas can write to it; **`temp_path.unlink(missing_ok=True)`** deletes it, without an error if it's already gone. `except BaseException:` rather than `except Exception:` because the clean-up must also happen when someone presses Ctrl+C, which raises `KeyboardInterrupt`, a `BaseException` but not an `Exception`; `raise` on its own then re-raises the same exception, so nothing is hidden. If the program crashes or is stopped halfway, a direct write leaves a damaged workbook under the real name, and anyone opening it (or an email job attaching it) gets a broken file. Writing to a temporary file and then replacing the final file means the real name only ever points to a complete report. `os.replace` works as a single step when both files are in the same folder, which is why the temporary file is created in `path.parent`.

**12.** Four 500s for page 2 exhaust all four attempts, so the client raises `CrmApiError` after waiting three times: about 0.5, 1, and 2 seconds plus jitter, between 3.5 and 5.25 seconds in total. Page 1's 20 leads are fetched first, but because `iter_leads` is consumed by `list(...)`, the caller gets the exception, not a partial list:

```python
import logging
import random
import sys
import time

from mock_crm_api import start_server
from riverstone_report.crm_client import CrmClient
from riverstone_report.errors import ReportError

logging.basicConfig(stream=sys.stdout, level=logging.WARNING,
                    format="%(levelname)s %(name)s: %(message)s", force=True)

server, base_url = start_server(8029, failures={2: [500, 500, 500, 500]})
client = CrmClient(base_url, "demo-key", rng=random.Random(12))
started = time.perf_counter()
try:
    leads = list(client.iter_leads(page_size=20))
except ReportError as exc:
    print(type(exc).__name__ + ":", exc)
waited = time.perf_counter() - started
print("between 3.5 and 5.3 seconds:", 3.5 <= waited <= 5.3)
server.shutdown()
```

```
WARNING riverstone_report.crm_client: attempt 1 for {'page': 2, 'page_size': 20} failed (HTTP 500); retrying in 0.619 s
WARNING riverstone_report.crm_client: attempt 2 for {'page': 2, 'page_size': 20} failed (HTTP 500); retrying in 1.329 s
WARNING riverstone_report.crm_client: attempt 3 for {'page': 2, 'page_size': 20} failed (HTTP 500); retrying in 2.666 s
CrmApiError: http://127.0.0.1:8029/leads failed after 4 attempts (last: HTTP 500)
between 3.5 and 5.3 seconds: True
```

The three warnings show the growing waits; the fourth failure ends the attempts. `CrmApiError` is a `ReportError`, so catching the base class works.

**13.** She's right for code she runs by hand and watches, once. She isn't when it runs on a schedule or on a server: nobody is watching the screen, prints have no timestamps or levels, nothing is kept after the window closes, and a scheduler can't tell a printed error from success. Logging costs two lines per module, and turns the same messages into a record you can search on the day something goes wrong.

**14.** Two of: a one-off analysis for a single question that won't be repeated; exploring a new dataset in a notebook to decide whether it's worth anything; a throwaway conversion of a file that will be deleted afterwards; a quick prototype whose purpose is to find out whether an idea works at all. The test is whether anyone will run, depend on, or change it again. When the answer changes to yes, that's the moment to refactor.

**15.** Whether the business decision has been made and by whom (Anita? finance?); whether "discontinued" means past Furniture revenue should disappear from historical reports too, or only future sales stop; whether this should be a filter in the report at all, or a product status in the data so every report agrees; and whether the total revenue on the Summary sheet will still reconcile with the categories. Updating a test to match changed code proves only that the code does what it now says, not that it should.

---

## Where this leads

- **Chapter 32, Analytics Engineering with dbt,** applies these habits to SQL: version control, tests, review, and automated checks.
- **Chapter 33, The Computer Science You Actually Need,** explains why some Python code is slow and how to measure and fix it.
- **Chapter 30, Inference & Experiments,** uses Python for statistics; its final stretch goal turns the analysis into a tested package.
- **Chapter 46, Pipelines & Orchestration,** and **Chapter 56, MLOps,** build on packages, lockfiles, logging, and retries at production scale.
- **Chapter 72, Python & pandas Question Bank,** has interview questions on project structure, testing, error handling, and API clients.
