# Chapter 18. Python for Analysts: pandas & Automation

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** think in whole columns instead of loops, starting with NumPy arrays · load data from CSV, Excel, JSON, Parquet, a database, and an API · profile a DataFrame in five lines · select, filter, and create columns without falling into pandas' classic traps · aggregate with `groupby`, combine with `merge`, and reshape with `pivot_table` and `melt` · work with dates, resampling, and rolling windows · redo Chapter 14's cleaning in pandas and reconcile it to the rupee · draw Chapter 15's charts with matplotlib and seaborn through one reusable style function · write formatted, multi-sheet Excel files people are glad to receive · call an API, page through its results, and handle its status codes · turn the whole thing into one script with logging, checks, and a Markdown summary · know when to push work back to SQL and when to stop using pandas.
>
> **Before you start:** Chapter 17 (Python, the notebook, and the terminal from section 17.0), Chapters 12–13 (SQL and the `sales_lines` view), Chapter 14 (cleaning), Chapter 15 (chart choice and design), Chapter 16 (Power BI, whose measures pandas mirrors), and Chapters 10, 11, and 19 for the spreadsheet ideas pandas mirrors.
>
> **Time needed:** 40–45 hours, spread over four weeks. Type every example. A plan that works: week 1, sections 18.1–18.5 (NumPy, reading, looking, filtering, new columns); week 2, sections 18.6–18.9 (grouping, joining, reshaping, dates); week 3, sections 18.10–18.12 (cleaning, charts, Excel); week 4, sections 18.13–18.16, the project, and the timed challenge. Each week ends with a short checkpoint.
>
> **Tools:** the Python, VS Code, and Jupyter you installed in Chapter 17 (section 17.0), in the book's virtual environment, with `pandas`, `numpy`, `pyarrow`, `matplotlib`, `seaborn`, `openpyxl`, `xlsxwriter`, `tabulate`, `SQLAlchemy`, a database driver (`psycopg[binary]` for PostgreSQL, `mysql-connector-python` for MySQL), `requests`, and `python-dotenv`. Section 18.1 gives the one install command.
>
> **Practice data:** the full Riverstone dataset (`companion/full/`, CSV and Parquet, and the `riverstone_full` database from Chapter 14), Chapter 14's messy export, Chapter 15's chart data, Chapter 16's city-to-region table, Chapter 17's twelve monthly files, and `companion/ch18/` (a small demonstration API, a saved API reply, the cleaning script, and the finished monthly report script).

---

## Why this matters

Chapter 17 gave you Python. This chapter gives you the reason analysts use it.

**pandas** is a table in memory with a hundred useful verbs attached. It reads almost any format, groups and joins like SQL, reshapes like a pivot table, cleans like Power Query, charts like Excel, and writes a formatted workbook at the end — all in code you can rerun, schedule, review, and version.

That combination is what makes the difference in a job. The monthly pack that took a day becomes a script that takes four seconds and never forgets a step. The question "can you do this for all three years and every branch?" stops being a problem. And the boundary between analyst work and data engineering (Part 3) or data science (Part 4) is mostly this library and the habits around it.

pandas also has sharp edges: the same task can be written five ways, four of which are slow or subtly wrong, and its error messages are not kind. This chapter teaches the way that scales, and names the traps as they arrive.

---

## In plain English

A spreadsheet has a grid, and you work a cell at a time: write a formula, drag it down, watch it fill. That "drag it down" is the idea pandas turns into a habit.

In pandas you don't drag anything. You say *"the net revenue column is quantity times price times one minus discount"*, once, and it applies to all 209,006 rows at once. You say *"group by region and add up revenue"*, once, and it does what a pivot table does. You say *"join this to the customer list"*, once, and it does what XLOOKUP does, but for every row at the same time, and it tells you how many didn't match.

Three ideas carry most of the chapter:

- **A column is a thing.** You operate on whole columns, not cells. This is called **vectorized** work, and it's both faster and easier to read.
- **A table has an index** (the row labels). It's how pandas lines up rows when you combine things, and it's the source of half the confusion when you're new. When in doubt, `reset_index()`.
- **Most operations return a new table** rather than changing the old one. You build a pipeline of small steps, each one checkable, instead of editing in place.

---

## 18.1 DataFrames, Series, and vectorized thinking

### Set up the chapter's folder

Work the way Chapter 17 did (section 17.0): copy the folder `companion/ch18` into `work`, so you have `work/ch18` to practise in and the companion files stay untouched. Open the book folder in VS Code, open a terminal (**View → Terminal**), check that the prompt starts with `(.venv)`, and install this chapter's packages into the book's environment, all in one command:

<!-- run: none -->
```
# terminal
$ python -m pip install pandas numpy pyarrow matplotlib seaborn openpyxl xlsxwriter tabulate sqlalchemy "psycopg[binary]" requests python-dotenv
```

Add `mysql-connector-python` to the end if your database is MySQL. pip prints a long list of what it downloaded and ends with a line starting `Successfully installed`. Then run `python -m pip freeze > requirements.txt` again, as in Chapter 17, so the list of packages stays up to date. Finally create a notebook (**File → New File… → Jupyter Notebook**), choose the `.venv` kernel, and save it as `ch18.ipynb` in `work/ch18`. Every notebook cell in this chapter runs there.

The data this chapter reads lives in other chapters' companion folders: the full Riverstone dataset in `companion/full`, Chapter 14's messy export in `companion/ch14`, and so on. From `work/ch18`, `..` is `work` and `../..` is the book folder, so `../../companion` reaches all of them (Chapter 17, section 17.0). Give that path a name once, and check both where the notebook is running and that the path finds the data:

<!-- py: reset -->
```python
from pathlib import Path

COMPANION = Path("../../companion")
print(Path.cwd().name)
print((COMPANION / "full" / "orders.parquet").exists())
```

```
ch18
True
```

- **`Path.cwd()`** is the notebook's working folder (Chapter 17, section 17.9), and **`.name`** is its last part. It must be `ch18`.
- **`COMPANION`** is written in capitals because it never changes while the notebook runs (a Python convention for fixed values). **`/`** joins path parts, as in Chapter 17, so `COMPANION / "full" / "orders.parquet"` is the file `../../companion/full/orders.parquet`.
- **`.exists()`** is `True` when the file is there. If either line prints something else, move the notebook into `work/ch18` before going on: every `FileNotFoundError` in this chapter's first hour comes from this.

### NumPy first: arrays that do arithmetic on whole columns

pandas is built on a lower-level library called **NumPy** (Numerical Python). You'll rarely call NumPy directly, but three of its ideas show up in every pandas table, so one page on it saves hours of confusion later.

Start with the problem. In Chapter 17 a list held several values, and arithmetic on a list does something surprising. Before you run this, predict what `quantities * 2` prints.

```python
quantities = [10, 55, 25]
print(quantities * 2)
```

```
[10, 55, 25, 10, 55, 25]
```

A list times 2 is the list **repeated**, not doubled. To double each value in plain Python you need a loop or a list comprehension (Chapter 17, section 17.6). A NumPy **array** is a list-like container built for arithmetic instead:

```python
import numpy as np

quantities = np.array([10, 55, 25])
prices = np.array([290, 380, 430])
print(quantities * 2)
print(quantities * prices)
```

```
[ 20 110  50]
[ 2900 20900 10750]
```

How it works:

- **`import numpy as np`** loads NumPy under the short name `np`, which everyone uses.
- **`np.array([...])`** turns a list into an array.
- **`quantities * 2`** multiplies every value by 2, with no loop.
- **`quantities * prices`** multiplies the two arrays **position by position**: 10 × 290, 55 × 380, 25 × 430. That's the three line values of Riverstone's first three order lines in 2025, and it's exactly what a spreadsheet does when you write `=B2*C2` and fill it down.

This is **vectorized** arithmetic: one expression for the whole column. It runs in fast compiled code instead of a Python loop, which is why it's quicker as well as shorter.

Every array has one **dtype** (data type) for all its values, and a **shape**:

```python
print(quantities.dtype, quantities.shape)

discounts = np.array([0, 0, 12.5])
print(discounts.dtype, discounts)
```

```
int64 (3,)
float64 [ 0.   0.  12.5]
```

- **`int64`** means whole numbers stored in 64 bits; **`float64`** means numbers with decimals. One decimal value (12.5) makes the whole array `float64`, because an array holds one type.
- **`shape`** is the size: `(3,)` means three values in one dimension. A table has two dimensions, rows and columns.
- The trailing dots (`0.`, `12.5`) are how NumPy prints floats.

Missing numbers need a value that means "not known". NumPy's is **`np.nan`** ("not a number"), and it behaves like SQL's `NULL` in one surprising way:

```python
readings = np.array([10, np.nan, 25])
print(readings.dtype)
print(readings.sum(), np.nansum(readings))
print(np.nan == np.nan)
```

```
float64
nan 35.0
False
```

- `np.nan` is a float, so an array with a gap becomes `float64` even if every real value is whole. You'll see this in pandas too: a column of whole numbers with one blank prints as `10.0`.
- **`readings.sum()`** is `nan`: one unknown value makes the total unknown. **`np.nansum()`** skips the gaps, like SQL's `SUM`, which ignores `NULL`.
- **`np.nan == np.nan` is `False`**. An unknown is never equal to anything, not even another unknown, just as `NULL = NULL` isn't true in SQL (Chapter 12, section 12.7). That's why pandas gives you `.isna()` to find missing values instead of `== np.nan`.

The vectorized `IF` is **`np.where(condition, value_if_true, value_if_false)`**, and for more than two outcomes **`np.select`**:

```python
values = quantities * prices
print(values > 15000)
print(np.where(values > 15000, "large", "small"))

size = np.select([values >= 20000, values >= 10000], ["big", "medium"], default="small")
print(size)
```

```
[False  True False]
['small' 'large' 'small']
['small' 'big' 'medium']
```

How it works:

- **`values > 15000`** compares every value at once and gives an array of `True`/`False`, one per value. This is called a **boolean mask**, and you'll use it constantly in pandas to pick rows.
- **`np.where(mask, "large", "small")`** chooses `"large"` where the mask is `True` and `"small"` where it's `False`: Excel's `=IF(D2>15000,"large","small")`, filled down.
- **`np.select([condition1, condition2], [choice1, choice2], default=...)`** checks the conditions **in order** and takes the choice of the first one that's true; `default` is used where none is. It's Excel's `IFS` (Chapter 11). 20,900 passes the first test; 10,750 fails it and passes the second; 2,900 passes neither.

Two more NumPy names appear later: **`np.inf`**, a number larger than any other ("infinity"), useful as the top edge of a band, and `np.nan` again whenever a value is missing. That's all the NumPy this chapter needs. Chapters 21 and 22 use a little more.

### DataFrames and Series

A **DataFrame** is a table: named columns, labeled rows. A **Series** is one column (with its row labels). Everything in pandas is one of the two, and every column of a DataFrame is a NumPy array with a name and labels attached.

You can build a small DataFrame by hand from a dictionary, where each key is a column name and each value is the column's list. Here are Riverstone's 2025 net revenue totals by segment, the figures Chapter 16's report showed:

```python
import pandas as pd

segments = pd.DataFrame({
    "segment": ["Retail", "Wholesale", "Hospitality"],
    "net_revenue": [556436453.75, 312728492.50, 277476705.00],
})
print(segments)
print(type(segments), type(segments["net_revenue"]))
```

```
       segment   net_revenue
0       Retail  5.564365e+08
1    Wholesale  3.127285e+08
2  Hospitality  2.774767e+08
<class 'pandas.DataFrame'> <class 'pandas.Series'>
```

- **`pd.DataFrame({...})`** builds a table from a dictionary of equal-length lists. You'll use this to make tiny test tables throughout the chapter.
- **The numbers on the left (0, 1, 2) are the index**, pandas' row labels. A new table gets 0, 1, 2, … automatically.
- **`segments["net_revenue"]`**, one column, is a **Series**.
- **Numbers like `5.564365e+08`** are in **scientific notation**: 5.564365 × 10⁸, which is ₹55,64,36,500 to the seven digits shown. pandas switches to it when a column's numbers are large, which makes rupee totals hard to read.

Tell pandas how to print, once, at the top of every notebook:

```python
pd.set_option("display.float_format", "{:,.2f}".format)
pd.set_option("display.width", 100)
pd.set_option("display.max_columns", 12)
print(segments)
```

```
       segment    net_revenue
0       Retail 556,436,453.75
1    Wholesale 312,728,492.50
2  Hospitality 277,476,705.00
```

- **`display.float_format`** takes a formatting rule for decimals. `"{:,.2f}".format` is the f-string pattern from Chapter 17 (`:,` adds thousands separators, `.2f` keeps two decimals). It changes only how numbers **print**; the values stay exact.
- **`display.width`** and **`display.max_columns`** stop wide tables from wrapping or hiding columns behind `...`.

These options stay set for the rest of the notebook, so every table below prints in this style.

### Riverstone's tables

Now the real data. The full Riverstone dataset (Chapter 14) is in `companion/full`, as CSV and as Parquet, a format section 18.2 explains:

```python
orders = pd.read_parquet(COMPANION / "full" / "orders.parquet")
print(orders.shape)
print(orders.head(3))
```

```
(116194, 5)
   order_id  customer_id order_date     status  sales_rep_id
0    200001           32 2023-01-01  Cancelled             4
1    200002          209 2023-01-01  Delivered             4
2    200003          216 2023-01-01  Delivered             3
```

- **`pd.read_parquet(path)`** reads a file into a DataFrame.
- **`shape`** is (rows, columns): 116,194 orders with five columns each.
- **`head(3)`** shows the first three rows; `tail()` shows the last ones.

The order IDs start at 200001 in 2023, yet the order-line file below starts with order 10001 in 2025. That's not a mistake: the 175 orders of the 24 key accounts in Chapter 13's one-year database kept their original numbers (10001 to 10175), and every other order was numbered from 200001 in date order. So order IDs are not in date order across the whole table: sort by `order_date`, never by `order_id`, when you want time order.

```python
items = pd.read_parquet(COMPANION / "full" / "order_items.parquet")
print(items.shape)
print(items.head(3))
```

```
(209006, 6)
   order_item_id  order_id  product_id  quantity  unit_price  discount_pct
0              1     10001         108        10         290             0
1              2     10002         107        55         380             0
2              3     10003         101        25         430             0
```

Each row of `items` is one **order line**: one product on one order. To know each line's date, customer, and status, attach its order. That's a **join** (Chapter 12, section 12.10), and in pandas it's called `merge`:

```python
lines = items.merge(orders, on="order_id")
print(lines.shape)
print(len(items) == len(lines))
```

```
(209006, 10)
True
```

- **`items.merge(orders, on="order_id")`** joins the two tables on their shared column `order_id`, like `JOIN orders ON items.order_id = orders.order_id`.
- By default `merge` keeps only rows that match on both sides, an **inner join**. Every line has an order, so nothing is lost: still 209,006 rows, now with the order's four other columns attached (11 columns in all).
- **Always compare the row count before and after a join.** Section 18.7 shows what to do when it changes.

### Whole columns, not loops

Chapter 17 computed a line's value one row at a time. In pandas you write the formula once:

```python
lines["net_revenue"] = lines["quantity"] * lines["unit_price"] * (1 - lines["discount_pct"] / 100)

print(lines[["order_id", "quantity", "unit_price", "discount_pct", "net_revenue"]].head(3))
print(round(lines["net_revenue"].sum(), 2))
```

```
   order_id  quantity  unit_price  discount_pct  net_revenue
0     10001        10         290             0     2,900.00
1     10002        55         380             0    20,900.00
2     10003        25         430             0    10,750.00
2777685790.75
```

- **`lines["net_revenue"] = ...`** creates a new column. The right-hand side is NumPy arithmetic on three whole columns, so it runs over all 209,006 rows at once.
- **`lines[["order_id", ...]]`**, with a *list* of names inside the brackets, picks several columns (section 18.4).
- **`.sum()`** adds a whole column. The total, ₹2,77,76,85,790.75, includes cancelled lines; section 18.6 takes them out.

A Series gives its NumPy array back with **`.to_numpy()`**, which you'll need when another library wants plain arrays:

```python
print(lines["quantity"].to_numpy()[:3])
```

```
[10 55 25]
```

The rule of thumb: **if you're writing a `for` loop over the rows of a DataFrame, there's almost always a better way**. To see why, time a loop against the vectorized version. First the loop, over only the first 20,000 lines:

<!-- run: none -->
```python
import time

start = time.perf_counter()
total_loop = 0.0
for row in lines.head(20000).itertuples():
    total_loop += row.quantity * row.unit_price * (1 - row.discount_pct / 100)
loop_seconds = time.perf_counter() - start

print(f"loop: {len(lines.head(20000)):,} rows in {loop_seconds * 1000:.1f} ms")
```

```
loop: 20,000 rows in 45.3 ms
```

- **`time.perf_counter()`** reads a precise stopwatch, in seconds. Reading it before and after, and subtracting, gives the time the code in between took.
- **`.itertuples()`** hands you one row at a time as a small named record, so **`row.quantity`** reads that row's `quantity`. It's the fastest of pandas' row loops, which isn't saying much. (`.iterrows()` is the slower one you'll see in old tutorials.)
- `* 1000` turns seconds into milliseconds, and `:.1f` prints one decimal.

Now the vectorized version, over **all** 209,006 lines:

<!-- run: none -->
```python
start = time.perf_counter()
total_vec = (lines["quantity"] * lines["unit_price"] * (1 - lines["discount_pct"] / 100)).sum()
vec_seconds = time.perf_counter() - start

print(f"vectorized: {len(lines):,} rows in {vec_seconds * 1000:.1f} ms")
print(f"per row, the loop was about {(loop_seconds / 20000) / (vec_seconds / len(lines)):,.0f} times slower")
```

```
vectorized: 209,006 rows in 2.8 ms
per row, the loop was about 167 times slower
```

Timings are the one kind of output in this book that changes every run: these are from the machine used to write it, and yours will differ, but the loop stays far slower per row. The loop handled a tenth of the data and still took longer. On a million rows the difference is minutes against milliseconds.

> **Watch out: pandas is memory-hungry.** A DataFrame lives in RAM, and a rough rule is that it needs several times the file size on disk. Riverstone's 209,006 lines are nothing; a 5 GB CSV on a 16 GB laptop is a problem, and section 18.16 gives the options.

---

## 18.2 Reading data from anywhere

```python
customers = pd.read_csv(COMPANION / "full" / "customers.csv", parse_dates=["signup_date"])
products = pd.read_parquet(COMPANION / "full" / "products.parquet")
print(customers.shape, products.shape)
print(customers.dtypes)
```

```
(5027, 5) (8, 5)
customer_id               int64
customer_name               str
city                        str
segment                     str
signup_date      datetime64[us]
dtype: object
```

- **`parse_dates=["signup_date"]`** tells `read_csv` to turn that column into dates. A CSV file is only text, so without it the dates stay text.
- **`.dtypes`** lists each column's type. The ones you'll meet:

| dtype | Means |
|---|---|
| `int64` | whole numbers |
| `float64` | numbers with decimals; also a whole-number column with any blanks, because the blank is `NaN` (section 18.1) |
| `str` | text (pandas 3; older versions print `object` for text) |
| `datetime64[us]` | dates and times; the part in brackets is only the precision (`us` microseconds, `ms` milliseconds), and it doesn't change how you use the column |
| `Int64` (capital I) | whole numbers that are allowed to have blanks, shown as `<NA>` (section 18.10) |

`read_csv` has a hundred parameters; six matter most:

| Parameter | Use |
|---|---|
| `dtype={"customer_code": "string"}` | Stop pandas guessing; keep codes as text so leading zeros survive |
| `parse_dates=["order_date"]`, `date_format="%d-%m-%Y"` | Parse dates explicitly, never by guessing |
| `encoding="utf-8"` | As in Chapter 17; `encoding="latin-1"` rescues some legacy exports |
| `usecols=[...]`, `nrows=1000` | Read only what you need, or a sample while developing |
| `na_values=["N/A", "-", "unknown"]`, `keep_default_na=False` | Decide what counts as missing (Chapter 14, section 14.3) |
| `thousands=","`, `decimal="."` | Numbers written with separators, such as `1,400` |

The first one matters more than it looks. Chapter 14's messy export stores customer codes as four characters, `0124`. Read five rows of it with and without `dtype`:

```python
guessed = pd.read_csv(COMPANION / "ch14" / "orders_q4_2025_export.csv", usecols=["customer_code"], nrows=5)
as_text = pd.read_csv(COMPANION / "ch14" / "orders_q4_2025_export.csv", usecols=["customer_code"], nrows=5, dtype=str)
print(guessed["customer_code"].tolist())
print(as_text["customer_code"].tolist())
```

```
[124, 124, 153, 153, 161]
['0124', '0124', '0153', '0153', '0161']
```

- **`usecols=["customer_code"]`** reads only that column, and **`nrows=5`** only five rows: a fast sample while you're exploring.
- Without `dtype`, pandas saw digits, guessed "number", and the leading zero was lost, the same accident Chapter 10 warned about when opening a CSV in Excel. **`dtype=str`** keeps every value exactly as written.

The same pattern works for the other formats:

| Source | Read | Write |
|---|---|---|
| CSV | `pd.read_csv` | `df.to_csv(index=False)` |
| Excel | `pd.read_excel(path, sheet_name="Data")` | `df.to_excel` / `ExcelWriter` (section 18.12) |
| JSON | `pd.read_json`, `pd.json_normalize` (section 18.14) | `df.to_json(orient="records")` |
| Parquet | `pd.read_parquet` | `df.to_parquet` |
| SQL | `pd.read_sql` (section 18.13) | `df.to_sql` |
| Clipboard | `pd.read_clipboard()` | `df.to_clipboard()` |
| HTML tables | `pd.read_html(url)` | `df.to_html()` |

**Parquet deserves a habit.** It's a file format that stores a table column by column, compressed, and keeps each column's type, so a Parquet file reads in a fraction of the time of the same CSV and doesn't need `dtype` arguments. Use CSV to exchange data with people, Parquet to store it between steps of your own work.

```python
print("csv    ", (COMPANION / "full" / "order_items.csv").stat().st_size // 1024, "KB")
print("parquet", (COMPANION / "full" / "order_items.parquet").stat().st_size // 1024, "KB")
```

```
csv     5434 KB
parquet 2358 KB
```

`.stat().st_size` is a file's size in bytes, and `// 1024` divides by 1,024 and drops the remainder, giving kilobytes. The Parquet file is less than half the size, for the same 209,006 rows.

---

## 18.3 Looking at a DataFrame

Before any analysis, profile: the pandas version of Chapter 14, section 14.2. Start with the size and the types:

```python
print(lines.shape)
print(lines.dtypes)
```

```
(209006, 11)
order_item_id             int64
order_id                  int64
product_id                int64
quantity                  int64
unit_price                int64
discount_pct              int64
customer_id               int64
order_date       datetime64[ms]
status                      str
sales_rep_id              Int64
net_revenue             float64
dtype: object
```

`sales_rep_id` is `Int64` with a capital I: whole numbers with some blanks, which the next cells count. `order_date` is a date column, because Parquet kept the type.

Then what's in the columns:

```python
print(lines["status"].value_counts())
print(lines["quantity"].describe())
```

```
status
Delivered    197971
Cancelled      8625
Pending        1272
Shipped        1138
Name: count, dtype: int64
count   209,006.00
mean         29.91
std          15.89
min           5.00
25%          15.00
50%          30.00
75%          40.00
max          90.00
Name: quantity, dtype: float64
```

- **`.value_counts()`** counts each distinct value, largest first: the `GROUP BY status` with `COUNT(*)` of Chapter 12, in one call. Add `normalize=True` for shares and `dropna=False` to count blanks too.
- **`.describe()`** summarizes a numeric column: the count, mean, standard deviation (`std`, the typical distance from the mean; Chapter 21 covers it), minimum, quartiles (Chapter 15), and maximum. Quantities run from 5 to 90, with a median of 30.

For text columns, **`.describe(include="str")`** gives the count, number of distinct values, the most frequent one, and how often it appears. (pandas 3 stores text as `str`; in older versions write `include="object"`.)

```python
print(customers.describe(include="str"))
```

```
                     customer_name    city segment
count                         5027    4927    5027
unique                        5018      39       3
top     River Side Tiffin Services  Mumbai  Retail
freq                             2     409    2791
```

5,027 records hold only 5,018 different names, so some businesses are listed more than once (the most frequent name appears twice), and 100 cities are missing (5,027 − 4,927): the same findings as Chapter 14.

Next, the gaps and the grain:

```python
print(lines.isna().sum())
```

```
order_item_id       0
order_id            0
product_id          0
quantity            0
unit_price          0
discount_pct        0
customer_id         0
order_date          0
status              0
sales_rep_id     6213
net_revenue         0
dtype: int64
```

**`.isna()`** marks every missing value as `True`, and **`.sum()`** counts the `True`s in each column, because `True` counts as 1. Only `sales_rep_id` has gaps: 6,213 lines on orders that no rep handled.

```python
print(customers["city"].isna().sum(), "customer records with no city")
print(lines["order_date"].min().date(), "→", lines["order_date"].max().date())
print(lines["customer_id"].nunique(), "customers,", lines["order_id"].nunique(), "orders,", len(lines), "lines")
```

```
100 customer records with no city
2023-01-01 → 2025-12-28
5020 customers, 116194 orders, 209006 lines
```

- **100 customer records have no city.** Chapter 14 found the same 100 in the customer list; Chapter 16 found that 91 of them ordered in 2025. Different populations, both right.
- **`.min()`** and **`.max()`** of a date column give the first and last dates; **`.date()`** drops the time part for printing.
- **`.nunique()`** answers "how many distinct?", which is how you check the grain (Chapter 1): 209,006 rows and 116,194 distinct orders, so the table is one row per line, not per order.

**`.info()`** gives the types, the non-blank count of every column, and the memory used, in one call:

```python
lines.info()
```

```
<class 'pandas.DataFrame'>
RangeIndex: 209006 entries, 0 to 209005
Data columns (total 11 columns):
 #   Column         Non-Null Count   Dtype         
---  ------         --------------   -----         
 0   order_item_id  209006 non-null  int64         
 1   order_id       209006 non-null  int64         
 2   product_id     209006 non-null  int64         
 3   quantity       209006 non-null  int64         
 4   unit_price     209006 non-null  int64         
 5   discount_pct   209006 non-null  int64         
 6   customer_id    209006 non-null  int64         
 7   order_date     209006 non-null  datetime64[ms]
 8   status         209006 non-null  str           
 9   sales_rep_id   202793 non-null  Int64         
 10  net_revenue    209006 non-null  float64       
dtypes: Int64(1), datetime64[ms](1), float64(1), int64(7), str(1)
memory usage: 19.6 MB
```

`.info()` prints its report itself, so it needs no `print()`. `Non-Null Count` shows the gaps at a glance: every column has 209,006 values except `sales_rep_id`.

---

## 18.4 Selecting and filtering

```python
print(lines[["order_id", "order_date", "net_revenue"]].head(3))
print(lines["net_revenue"].head(3).tolist())
```

```
   order_id order_date  net_revenue
0     10001 2025-01-02     2,900.00
1     10002 2025-01-05    20,900.00
2     10003 2025-01-12    10,750.00
[2900.0, 20900.0, 10750.0]
```

- **`df[["a", "b"]]`**, with a list inside the brackets, returns a DataFrame with those columns.
- **`df["a"]`**, one name, returns a Series; **`.tolist()`** turns it into a plain Python list.

To pick **rows**, give the brackets a boolean mask (section 18.1): one `True` or `False` per row.

```python
is_big = lines["net_revenue"] >= 50000
print(is_big.head(3).tolist())

big = lines[is_big]
print(len(big), round(big["net_revenue"].sum(), 2))
print(big[["order_id", "order_date", "quantity", "unit_price", "net_revenue"]].head(3))
```

```
[False, False, False]
2080 123323786.25
     order_id order_date  quantity  unit_price  net_revenue
204     10107 2025-09-13        45        1400    56,700.00
244     10126 2025-10-13        40        1400    51,520.00
305     10162 2025-12-08        40        1400    51,520.00
```

- **`lines["net_revenue"] >= 50000`** is the mask: `True` for every line worth ₹50,000 or more.
- **`lines[is_big]`** keeps the rows where the mask is `True`, like `WHERE net_revenue >= 50000`.
- 2,080 lines are worth ₹50,000 or more, ₹12,33,23,786.25 between them. The first three lines of the table aren't among them, which is why the mask starts `False, False, False`.
- The row labels on the left (204, 244, 305) are the original index values: filtering keeps each row's label, which is why they're no longer 0, 1, 2.

Combine conditions with **`&`** (and), **`|`** (or), and **`~`** (not), and **wrap each condition in brackets**:

```python
q4_not_cancelled = lines[(lines["order_date"] >= "2025-10-01") & (lines["status"] != "Cancelled")]
print(len(q4_not_cancelled))
```

```
24738
```

- The brackets matter because `&` binds more tightly than `>=`. Python's words `and`/`or` don't work on a Series at all, and forgetting the brackets is the most common pandas `ValueError`.
- **`lines["order_date"] >= "2025-10-01"`** compares a date column with text: pandas turns the text into a date first. Write dates as `YYYY-MM-DD` so there's nothing to guess.

**`.isin()`** replaces a long chain of `|`, **`.between()`** replaces two comparisons, and **`.query()`** takes the whole condition as text:

```python
south = customers[customers["city"].isin(["Bengaluru", "Chennai", "Hyderabad"])]
print(len(south))

mid = lines[lines["quantity"].between(20, 40)]
print(len(mid), mid["quantity"].min(), mid["quantity"].max())

print(lines.query("status == 'Delivered' and quantity > 80").shape)
```

```
807
113328 20 40
(721, 11)
```

- **`.isin([...])`** is SQL's `IN (...)`.
- **`.between(20, 40)`** includes both ends, like SQL's `BETWEEN`: the minimum is 20 and the maximum 40.
- **`.query("...")`** reads like a `WHERE` clause, and inside the text `and` is allowed. It's handy for quick looks; masks are clearer when conditions are built up in steps.

### `loc` and `iloc`

```python
sample = lines.head(5).copy()
print(sample.loc[0, "order_id"], sample.iloc[0, 0])
print(sample.loc[0:2, ["order_id", "quantity"]])
print(sample.iloc[0:2, 0:2])
```

```
10001 1
   order_id  quantity
0     10001        10
1     10002        55
2     10003        25
   order_item_id  order_id
0              1     10001
1              2     10002
```

- **`.copy()`** makes `sample` a separate table, so nothing done to it touches `lines`.
- **`.loc[rows, columns]`** works by **label**: `0` is the row labelled 0, `"order_id"` the column of that name. With a slice it **includes** the end label, so `0:2` gives three rows.
- **`.iloc[rows, columns]`** works by **position**, and excludes the end, like normal Python slicing: `0:2` gives two rows. Column 0 is `order_item_id`, the first column.
- Use `.loc` for almost everything. `.iloc` is for "the first five rows" and similar.

**`.loc` is also how you change values in a filtered part of a table.** Here is the trap it avoids, on the copy:

```python
sample[sample["quantity"] > 20]["quantity"] = 0
print(sample["quantity"].tolist())

sample.loc[sample["quantity"] > 20, "quantity"] = 0
print(sample["quantity"].tolist())
```

```
[10, 55, 25, 45, 10]
[10, 0, 0, 0, 10]
```

- The first line is **chained assignment**: `sample[...]` filters (step 1), then `["quantity"] = 0` sets values on the result of that filter (step 2). In pandas 3 a filtered table always behaves as a separate copy, so step 2 changes the copy and `sample` is untouched: the quantities are still 10, 55, 25, 45, 10. Beneath the cell, pandas prints a warning that starts `ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment`.
- **`sample.loc[mask, "quantity"] = 0`** does it in one step, on `sample` itself, and works: the three quantities above 20 are now 0.

> **Watch out: old advice about `SettingWithCopyWarning`.** Tutorials written for pandas 1 and 2 describe a `SettingWithCopyWarning` and say chained assignment "may" work. In pandas 3 that warning is gone and chained assignment never changes the original. The fix is the same in every version: one `.loc[rows, column] = value`, and `.copy()` when you mean a new table.

---

## 18.5 Creating and changing columns

You've already made one column (`net_revenue`) by assigning to a new name. The rest of this section adds more to a working copy, so `lines` stays as it was:

```python
work = lines.copy()
work["year"] = work["order_date"].dt.year
work["status_clean"] = work["status"].str.strip().str.title()
print(work[["order_date", "year", "status", "status_clean"]].head(3))
```

```
  order_date  year     status status_clean
0 2025-01-02  2025  Delivered    Delivered
1 2025-01-05  2025  Delivered    Delivered
2 2025-01-12  2025  Delivered    Delivered
```

- **`.dt`** exposes date parts on a datetime column: `.dt.year`, `.dt.month`, `.dt.day_name()`, and more.
- **`.str`** gives the string methods of Chapter 17 applied to a whole column: `.strip()`, `.lower()`, `.title()`, `.replace()`, `.contains()`, `.startswith()`. Here the statuses were already clean; in section 18.10 they won't be.

A line's **cost** is its quantity times the product's unit cost, which lives in the `products` table. That's a lookup, so it's a `merge`. Choose the two columns you need and say what kind of match you expect:

```python
work = work.merge(products[["product_id", "unit_cost"]], on="product_id", how="left", validate="many_to_one")
print(len(lines) == len(work))

work["line_cost"] = work["quantity"] * work["unit_cost"]
work["margin"] = work["net_revenue"] - work["line_cost"]
print(work[["product_id", "quantity", "unit_cost", "line_cost", "net_revenue", "margin"]].head(3))
```

```
True
   product_id  quantity  unit_cost  line_cost  net_revenue   margin
0         108        10        190       1900     2,900.00 1,000.00
1         107        55        240      13200    20,900.00 7,700.00
2         101        25        300       7500    10,750.00 3,250.00
```

- **`products[["product_id", "unit_cost"]]`** takes only the key and the one column you want, so nothing else crowds into `work`.
- **`how="left"`** keeps every line even if its product were missing from `products` (a left join, Chapter 12). Section 18.7 covers the choices.
- **`validate="many_to_one"`** tells pandas what you expect: many lines per product, **one** row per product in `products`. If `products` ever had a duplicate `product_id`, the merge would stop with an error instead of silently duplicating lines.
- **`len(lines) == len(work)`** is `True`: the lookup added columns, not rows.

**Bands** turn a number into a category. Riverstone's size bands include the lower edge (Chapter 19): from ₹10,000 is medium, from ₹25,000 large, from ₹50,000 very large.

```python
work["size_band"] = pd.cut(work["net_revenue"], bins=[0, 10000, 25000, 50000, np.inf],
                           labels=["small", "medium", "large", "very large"], right=False)
print(work["size_band"].value_counts().sort_index())
```

```
size_band
small         99974
medium        83065
large         23887
very large     2080
Name: count, dtype: int64
```

- **`pd.cut(column, bins=[...], labels=[...])`** puts each value into a band. The four bands run between the five edges: 0 to 10,000, 10,000 to 25,000, and so on, with **`np.inf`** as an upper edge nothing can pass.
- **`right=False`** makes each band include its **left** edge and exclude its right one, so exactly ₹25,000 is "large", the same rule as Chapter 19's `BandBySize`. Without it, `pd.cut` includes the right edge instead, and ₹25,000 would be "medium". Always check which edge a band tool includes.
- **`.sort_index()`** lists the bands in their own order rather than by count. It's the nested `IF` or `IFS` of Chapter 11, for 209,006 rows at once.

What happens if you change it? Before you run this, predict which band exactly ₹25,000 lands in each time:

```python
edges = pd.Series([9999.5, 10000, 25000, 50000])
bands = ["small", "medium", "large", "very large"]
print(pd.cut(edges, bins=[0, 10000, 25000, 50000, np.inf], labels=bands, right=False).tolist())
print(pd.cut(edges, bins=[0, 10000, 25000, 50000, np.inf], labels=bands).tolist())
```

```
['small', 'medium', 'large', 'very large']
['small', 'small', 'medium', 'large']
```

With `right=False` each edge value starts the next band up; without it, each edge value ends the band below. Only values sitting exactly on an edge change band, which makes the mistake easy to miss.

**Lookups with a dictionary.** Each order has a `sales_rep_id`; the names are in the employees table (Chapter 12; the full dataset has 16 people). Build a dictionary from it, then map:

```python
employees = pd.read_parquet(COMPANION / "full" / "employees.parquet")
rep_names = dict(zip(employees["employee_id"], employees["employee_name"]))

work["rep"] = work["sales_rep_id"].map(rep_names).fillna("(no rep)")
print(work["rep"].value_counts())
```

```
rep
Rahul Mehta      30304
Simran Kaur      24954
Tarun Bose       23391
Divya Menon      22853
Aakash Jain      15422
Neha Kulkarni    15291
Kavitha Reddy    14918
Irfan Sheikh     14588
Meenal Joshi     14286
Farah Khan       13816
Rohit Verma      12970
(no rep)          6213
Name: count, dtype: int64
```

- **`dict(zip(ids, names))`** pairs the two columns into `{1: "Anita Rao", 2: "Vikram Singh", …}`, using `zip` from Chapter 17.
- **`.map(rep_names)`** looks each ID up in the dictionary: exactly Chapter 14's mapping table. An ID that isn't in the dictionary, including a blank, comes back as missing, which is how you find the unmapped ones.
- **`.fillna("(no rep)")`** replaces the missing values with a label, so the 6,213 lines with no rep stay visible as their own group instead of vanishing (Chapter 15's rule for missing categories).

The vectorized `IF` from section 18.1 works on columns too:

```python
work["flag"] = np.where(work["net_revenue"] >= 50000, "review", "ok")
print(work["flag"].value_counts())

def flag_one(value):                  # the slow way, for comparison
    return "review" if value >= 50000 else "ok"

print(work["net_revenue"].head(5).apply(flag_one).tolist())
```

```
flag
ok        206926
review      2080
Name: count, dtype: int64
['ok', 'ok', 'ok', 'ok', 'ok']
```

`np.where` flags the same lines as the "very large" band: every line from ₹50,000 up. **`.apply(function)`** runs an ordinary Python function once per value. It's flexible, readable, and **slow**: it's a loop wearing a costume. Use it when there's no vectorized equivalent, and reach first for arithmetic, `.str`, `.dt`, `.map`, `np.where`, and `np.select`.

### Checkpoint: week 1

Without looking back, in a fresh notebook cell: read `products.parquet` from `COMPANION / "full"`, add a column `margin_pct` = (unit price − unit cost) ÷ unit price × 100, and show the products sorted from highest to lowest margin with `sort_values("margin_pct", ascending=False)`. Then count how many lines of `work` from 2025 are "large" or "very large" (use `isin`). The answers are with the exercise answers at the end of the chapter.

---

## 18.6 `groupby`: split, apply, combine

`groupby` is SQL's `GROUP BY` and Excel's pivot table, in one verb. Start by keeping only the orders that count as sales, as the `sales_lines` view does (Chapter 13):

```python
sales = lines[lines["status"] != "Cancelled"].copy()
sales["year"] = sales["order_date"].dt.year

by_year = sales.groupby("year")["net_revenue"].sum()
print(by_year)
```

```
year
2023     613,833,108.25
2024     903,015,475.25
2025   1,146,641,651.25
Name: net_revenue, dtype: float64
```

Read it in three parts: **split** the rows into groups by `year`, take the `net_revenue` column, and **combine** each group with `.sum()`. Those are Riverstone's three years: ₹61.4 crore, ₹90.3 crore, ₹114.7 crore, matching Chapters 15 and 16 exactly. (Without the display option from section 18.1 you'd see `6.138331e+08` here.)

Several measures at once, with names you choose:

```python
summary = (sales.groupby("year")
                .agg(net_revenue=("net_revenue", "sum"),
                     orders=("order_id", "nunique"),
                     lines=("order_id", "size"),
                     customers=("customer_id", "nunique"),
                     avg_line=("net_revenue", "mean")))
print(summary)
```

```
          net_revenue  orders  lines  customers  avg_line
year                                                     
2023   613,833,108.25   26986  48439       3334 12,672.29
2024   903,015,475.25   38086  68498       4104 13,183.09
2025 1,146,641,651.25   46356  83444       4599 13,741.45
```

- **Named aggregation**, `new_name=("column", "function")`, is the clearest form: each output column says what it is and how it was made. Here `orders` counts distinct order IDs, `lines` counts rows, and `avg_line` is the mean value of a line.
- The brackets around the whole expression let it run over several lines, one step per line.
- The functions you'll use: `sum`, `mean`, `median`, `min`, `max`, `count` (non-blank values), `size` (rows), `nunique`, `std`, and **`quantile`**, shown below.

A **quantile** is the value below which a given share of the data falls: the 0.9 quantile (the 90th percentile) is the order value that 90% of orders are below. First make one row per order, then ask:

```python
cust = customers[["customer_id", "segment", "city"]]
sales2025 = sales[sales["year"] == 2025].merge(cust, on="customer_id", how="left")

order_values = sales2025.groupby("order_id")["net_revenue"].sum()
print(len(order_values), round(order_values.quantile(0.9), 2), round(order_values.median(), 2))
```

```
46356 49550.0 20615.0
```

- **`sales2025`** is 2025's non-cancelled lines with each customer's segment and city attached; the rest of this section and section 18.11 use it.
- **`groupby("order_id")["net_revenue"].sum()`** adds up each order's lines: 46,356 orders in 2025.
- **`.quantile(0.9)`** finds the 90th percentile. When it falls between two orders, pandas interpolates in a straight line between them, the same method as Excel's `PERCENTILE.INC` and `QUARTILE.INC` (Chapter 15) and SQL's `PERCENTILE_CONT`. `.median()` is `.quantile(0.5)`.

### Grouping by two columns

Grouping by segment **and** month gives one number per pair. Add the month as a column first, then group by both:

```python
sales2025["month"] = sales2025["order_date"].dt.month
by_seg_month = sales2025.groupby(["segment", "month"])["net_revenue"].sum()
print(by_seg_month.head(4))
```

```
segment      month
Hospitality  1       20,097,757.50
             2       19,543,963.75
             3       21,701,085.00
             4       20,926,241.25
Name: net_revenue, dtype: float64
```

The result is a Series with a **two-level index**: segment on the outside, month inside, printed with the segment shown once per group. It's long and thin, which is good for further work and poor for reading.

**`.unstack()`** turns one level of the index into columns, the way a pivot table puts a field in its Columns area:

```python
table = by_seg_month.unstack("month")
print(table.iloc[:, :6].round(0))
```

```
month                   1             2             3             4             5             6
segment                                                                                        
Hospitality 20,097,758.00 19,543,964.00 21,701,085.00 20,926,241.00 19,591,321.00 12,388,498.00
Retail      40,432,825.00 36,932,976.00 52,355,854.00 50,138,972.00 45,413,214.00 25,502,201.00
Wholesale   24,664,938.00 22,105,639.00 26,952,128.00 24,129,496.00 22,245,032.00 14,081,784.00
```

`unstack("month")` moves the months across the top, leaving one row per segment. `.iloc[:, :6]` (all rows, the first six columns) keeps the print narrow, and `.round(0)` rounds for display only.

Adding **across** each row gives each segment's year:

```python
print(table.sum(axis=1).round(2))
```

```
segment
Hospitality   277,476,705.00
Retail        556,436,453.75
Wholesale     312,728,492.50
dtype: float64
```

**`axis`** says which way to go. `axis=0`, the default, works **down** each column (one answer per column, like a total row under a table); `axis=1` works **across** each row (one answer per row, like a total column at the right). So `table.sum(axis=1)` adds the twelve months of each segment: Retail's year is ₹55,64,36,453.75.

### Functions without names: `lambda`

Some pandas methods take a small function as an argument. For a one-line function you don't want to name, Python has **`lambda`**:

```python
def times_two(x):
    return x * 2

times_two_again = lambda x: x * 2
print(times_two(21), times_two_again(21))
```

```
42 42
```

`lambda x: x * 2` is the whole of `def times_two(x): return x * 2`, written inline: the word `lambda`, the parameter, a colon, and the expression to return. You'll see it most with **`.assign()`**, which adds columns inside a chain and returns a new table:

```python
with_month = sales2025.assign(quarter=lambda d: d["order_date"].dt.quarter)
print(with_month[["order_date", "month", "quarter"]].head(3))
```

```
  order_date  month  quarter
0 2025-01-02      1        1
1 2025-01-05      1        1
2 2025-01-12      1        1
```

- **`.assign(quarter=...)`** returns a copy of the table with a new column `quarter`; `sales2025` itself is unchanged.
- **`lambda d: d["order_date"].dt.quarter`** receives the table as `d` and returns the new column. The lambda matters in long chains, where the table at that step has no name of its own yet.

### `transform`: a group value on every row

Sometimes each row needs its group's total beside it, to work out a share. **`transform`** gives one value per group, repeated on every row of that group:

```python
segment_total = sales2025.groupby("segment")["net_revenue"].transform("sum")
print(segment_total.head(3))
```

```
0   556,436,453.75
1   277,476,705.00
2   556,436,453.75
Name: net_revenue, dtype: float64
```

The result has as many rows as `sales2025`, and each row carries its segment's total. That's the window function of Chapter 13, `SUM(net_revenue) OVER (PARTITION BY segment)`. Now the share is plain arithmetic:

```python
sales2025["pct_of_segment"] = sales2025["net_revenue"] / segment_total * 100
print(sales2025[["segment", "net_revenue", "pct_of_segment"]].head(3))
```

```
       segment  net_revenue  pct_of_segment
0       Retail     2,900.00            0.00
1  Hospitality    20,900.00            0.01
2       Retail    10,750.00            0.00
```

Each line is a tiny share of its segment, less than 0.01%, as you'd expect when 83,444 lines share the year. `rank`, `cumsum`, and `shift` also work per group, which is how you write "each customer's previous order" or "running total" without a loop.

And the biggest customers:

```python
top_customers = (sales2025.groupby("customer_id")["net_revenue"].sum()
                          .sort_values(ascending=False).head(5))
print(top_customers)
```

```
customer_id
1423   1,073,806.50
3497     993,853.00
3699     955,337.50
1932     920,777.00
3578     909,521.00
Name: net_revenue, dtype: float64
```

**`.sort_values(ascending=False)`** sorts largest first, like `ORDER BY … DESC`; `.head(5)` keeps the top five.

---

## 18.7 Combining tables: `merge` and `concat`

`merge` is SQL's `JOIN` (Chapter 12) and the spreadsheet's XLOOKUP (Chapter 11), with one important habit attached: **measure the match rate**.

```python
joined = lines.merge(customers, on="customer_id", how="left", indicator=True)
print(joined["_merge"].value_counts())
print(len(lines), "lines in,", len(joined), "lines out")
```

```
_merge
both          209006
left_only          0
right_only         0
Name: count, dtype: int64
209006 lines in, 209006 lines out
```

- **`how=`** is the join type: `"left"` (keep all left rows), `"inner"` (only matches, the default), `"right"`, `"outer"` (everything from both sides).
- **`indicator=True`** adds a `_merge` column saying where each row came from: `both`, `left_only` (no match on the right), or `right_only`. It's the fastest way to see unmatched rows.
- **The row count must be explained.** If `merge` returns more rows than it started with, the right-hand table has duplicate keys and the join **fanned out** (Chapter 12). That's the single most dangerous silent error in analyst code.

To see a fan-out, build a small right-hand table by hand with customer 1 in it twice:

```python
dupes = pd.DataFrame({"customer_id": [1, 1, 2], "note": ["a", "b", "c"]})
print(lines.head(10)["customer_id"].value_counts().sort_index().to_dict())

fanned = lines.head(10).merge(dupes, on="customer_id", how="left")
print(len(fanned), "rows from 10:", fanned["customer_id"].value_counts().sort_index().to_dict())
```

```
{1: 1, 2: 1, 3: 2, 4: 1, 5: 5}
11 rows from 10: {1: 2, 2: 1, 3: 2, 4: 1, 5: 5}
```

The first ten lines include one line for customer 1. After the join, that line appears **twice**, once for each matching row in `dupes`, so 10 lines become 11. Every total computed after this join would count that line twice.

Other joining tools:

```python
q4 = sales[sales["order_date"] >= "2025-10-01"]
q3 = sales[(sales["order_date"] >= "2025-07-01") & (sales["order_date"] < "2025-10-01")]
stacked = pd.concat([q3.assign(quarter="Q3"), q4.assign(quarter="Q4")], ignore_index=True)
print(stacked["quarter"].value_counts().to_dict(), len(stacked))
```

```
{'Q4': 24738, 'Q3': 19855} 44593
```

- **`pd.concat([...])`** stacks tables with the same columns on top of each other, like SQL's `UNION ALL`: the folder-of-files pattern from Chapter 17, done in one line.
- **`.assign(quarter="Q3")`** labels each part before stacking, so you can still tell them apart. A fixed value needs no `lambda`.
- **`ignore_index=True`** numbers the stacked rows 0, 1, 2, … afresh instead of keeping both parts' old labels.

When you need only one column from another table, map through a Series:

```python
names = customers.set_index("customer_id")["customer_name"]
print(lines.head(3)["customer_id"].map(names).tolist())
```

```
['Patel Kitchenware', 'Green Leaf Hotels', 'Metro Mart']
```

- **`.set_index("customer_id")`** makes the customer ID the row label, so `names` is a Series of names labelled by ID.
- **`.map(names)`** looks each ID up by label, like `.map(dict)` in section 18.5. `merge` is better when you need several columns.

One more for later: **`pd.merge_asof`** joins each row to the nearest *earlier* key, which is how you attach the price list that was valid on an order's date.

> **Watch out: check the key's type and shape.** A merge on `customer_id` as text against `customer_id` as integer stops with an error in pandas; a merge on text keys that differ by a space or a lost zero (`"124"` against `"0124"`) matches nothing, silently, and produces a table full of blanks. Check `df["key"].dtype` on both sides, strip and pad text keys as in Chapter 14, and always look at the `_merge` counts before trusting the result.

---

## 18.8 Reshaping: `pivot_table`, `melt`, and tidy data

A pivot table's **Columns** area needs a field, so first add the quarter as a column of `sales2025`:

```python
sales2025 = sales2025.assign(quarter=sales2025["order_date"].dt.quarter)
print(sales2025[["order_date", "quarter"]].head(3))
```

```
  order_date  quarter
0 2025-01-02        1
1 2025-01-05        1
2 2025-01-12        1
```

Then the pivot:

```python
pivot = pd.pivot_table(sales2025, index="segment", columns="quarter", values="net_revenue",
                       aggfunc="sum", margins=True, margins_name="Total")
print(pivot.round(0))
```

```
quarter                  1              2              3              4            Total
segment                                                                                 
Hospitality  61,342,806.00  52,906,060.00  56,167,475.00 107,060,364.00   277,476,705.00
Retail      129,721,655.00 121,054,388.00 105,901,998.00 199,758,414.00   556,436,454.00
Wholesale    73,722,704.00  60,456,312.00  61,495,446.00 117,054,030.00   312,728,492.00
Total       264,787,166.00 234,416,760.00 223,564,918.00 423,872,808.00 1,146,641,651.00
```

`pivot_table` takes the same four choices as a spreadsheet pivot table, one argument each:

- **`index="segment"`** is the **Rows** area: one row per segment.
- **`columns="quarter"`** is the **Columns** area. It must be the **name** of a column in the table, which is why the quarter was added as a column first.
- **`values="net_revenue"`** is the **Values** field, and **`aggfunc="sum"`** how to summarize it.
- **`margins=True`** adds totals for every row and column, and **`margins_name="Total"`** names them.

The result is an ordinary DataFrame you can keep working with. It's the fastest way to look at a two-way question.

Going the other way, to **long** format:

```python
wide = pivot.drop(index="Total").drop(columns="Total").reset_index()
long = wide.melt(id_vars="segment", var_name="quarter", value_name="net_revenue")
print(long.head(4))
print(long.shape)
```

```
       segment quarter    net_revenue
0  Hospitality       1  61,342,806.25
1       Retail       1 129,721,655.00
2    Wholesale       1  73,722,704.50
3  Hospitality       2  52,906,060.00
(12, 3)
```

- **`.drop(index="Total")`** removes the total row and **`.drop(columns="Total")`** the total column: totals don't belong in a long table.
- **`.reset_index()`** turns the row labels (the segments) back into an ordinary column.
- **`.melt(id_vars="segment", var_name="quarter", value_name="net_revenue")`** unpivots: `id_vars` are the columns to keep as they are, every other column becomes rows, `var_name` names the new column that holds the old column headings, and `value_name` names the column of values. 3 segments × 4 quarters = 12 rows.

**Wide** (a column per period) reads well on a slide. **Long** (one row per combination) is what charting libraries, databases, and statistical tools want. **Tidy data** means one row per observation and one column per variable; `melt` and `pivot_table` move between the two, and knowing which shape a tool wants saves hours.

---

## 18.9 Dates and time series

A **time series** is a set of values in time order. pandas handles one best when the dates are the row labels:

```python
ts = sales.set_index("order_date")["net_revenue"].sort_index()
monthly = ts.resample("MS").sum()
print(monthly.head(4))
print(monthly.tail(3))
```

```
order_date
2023-01-01   42,419,703.50
2023-02-01   37,963,392.50
2023-03-01   50,617,494.50
2023-04-01   48,469,812.25
Freq: MS, Name: net_revenue, dtype: float64
order_date
2025-10-01   180,620,102.75
2025-11-01   155,985,901.50
2025-12-01    87,266,803.75
Freq: MS, Name: net_revenue, dtype: float64
```

- **`.set_index("order_date")`** makes the dates the index, and **`.sort_index()`** puts them in time order (order IDs aren't, section 18.1).
- **`.resample("MS")`** groups by time period: `"D"` day, `"W"` week, `"MS"` month start, `"QS"` quarter start, `"YS"` year start. It needs a datetime index. `.sum()` adds each month.
- **`Freq: MS`** under the output confirms each row is one month, labelled by its first day.

Moving averages and year-over-year comparisons are one line each:

```python
frame = monthly.to_frame("net_revenue")
frame["rolling_3m"] = frame["net_revenue"].rolling(3).mean()
frame["same_month_last_year"] = frame["net_revenue"].shift(12)
frame["yoy_pct"] = (frame["net_revenue"] / frame["same_month_last_year"] - 1) * 100
print(frame.loc["2025-09":"2025-12"])
```

```
              net_revenue     rolling_3m  same_month_last_year  yoy_pct
order_date                                                             
2025-09-01 111,701,478.75  74,521,639.33         87,548,908.00    27.59
2025-10-01 180,620,102.75 121,385,642.50        147,221,565.50    22.69
2025-11-01 155,985,901.50 149,435,827.67        127,896,564.25    21.96
2025-12-01  87,266,803.75 141,290,936.00         72,822,551.75    19.83
```

- **`.to_frame("net_revenue")`** turns the Series into a one-column table, so more columns can be added.
- **`.rolling(3).mean()`** averages each month with the two before it: a three-month moving average, like Chapter 13's `AVG(...) OVER (ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`.
- **`.shift(12)`** moves the whole column down twelve rows, so each month sits beside the same month a year earlier, like `LAG(…, 12)`.
- **`frame.loc["2025-09":"2025-12"]`** picks rows by date text: with a date index, `.loc` accepts a slice of months and includes both ends.

October 2025 grew 22.7% over October 2024, the number Chapter 15's story turned on, computed here in one line.

```python
print(sales["order_date"].dt.day_name().value_counts().head(3))
print(sales["order_date"].dt.to_period("Q").value_counts().sort_index().tail(4))
```

```
order_date
Monday       28871
Tuesday      28818
Wednesday    28713
Name: count, dtype: int64
order_date
2025Q1    19841
2025Q2    19010
2025Q3    19855
2025Q4    24738
Freq: Q-DEC, Name: count, dtype: int64
```

`.dt.day_name()` gives the weekday's name. `.dt.to_period("Q")` gives real quarter labels such as `2025Q4`, which sort correctly. Time zones follow the same pattern: `.dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")` is Chapter 14's conversion from UTC to Indian time, and section 18.10 uses it.

### Checkpoint: week 2

From `sales`, build a table with one row per product (use `product_id`) and one column per year, holding net revenue, using `pivot_table`. Which product grew most from 2024 to 2025, in rupees? Then use `resample` to find 2025's weakest week. The answers are at the end of the chapter.

---
## 18.10 Cleaning in pandas

Chapter 14 cleaned Riverstone's messy Q4 export twice: in SQL, and in Excel with Power Query. Here is the third tool, doing the same cleaning in the same order, and it must land on the same answer: **₹42,35,61,010.50** of non-cancelled revenue once the quarantined lines are set aside. The method doesn't change: load as text, profile, fix, validate, reconcile. What pandas adds is that every step is a line of code you can rerun on next quarter's file.

### Load as text, and profile

```python
raw = pd.read_csv(COMPANION / "ch14" / "orders_q4_2025_export.csv", dtype=str, keep_default_na=False)
print(raw.shape)
```

```
(25976, 13)
```

- **`dtype=str`** loads every column as text, so nothing is guessed and nothing is lost: codes keep their zeros and the odd dates stay exactly as typed. It's the staging table of Chapter 14, where every column was text.
- **`keep_default_na=False`** keeps empty fields as empty text `""` instead of turning them into missing values. You decide later what counts as missing.
- The file has 25,976 rows and 13 columns, including the repeated header rows and the footer Chapter 14 found.

Keep only the data rows, and count the exact duplicates before removing them:

```python
data = raw[raw["order_item_id"].str.fullmatch(r"\d+")]
print(len(data), "data rows;", data.duplicated().sum(), "exact duplicates")
data = data.drop_duplicates()
print(len(data), "rows after removing them")
```

```
25969 data rows; 137 exact duplicates
25832 rows after removing them
```

- **`.str.fullmatch(r"\d+")`** is `True` when the **whole** ID is digits, the regular expression `^\d+$` of Chapter 14 (section 14.2, "Patterns in ten minutes"). `fullmatch` supplies the `^` and `$` itself. The `r` before the quotes makes a **raw string**, so Python leaves the backslash in `\d` alone.
- **`.duplicated()`** marks every row that is an exact copy of an earlier one; `.sum()` counts them. **`.drop_duplicates()`** removes them and keeps the first copy, like `SELECT DISTINCT *`.
- The same 7 non-data rows (25,976 − 25,969) and 137 duplicates as Chapter 14's SQL, leaving 25,832 order lines.

Now the columns Chapter 14 had to fix. The statuses first:

```python
print(data["status"].str.strip().str.lower().value_counts())
```

```
status
delivered    21744
pending       1166
shipped       1138
cancelled     1034
dlvd           690
cxl             32
canceled        28
Name: count, dtype: int64
```

Trimmed and lower-cased, seven spellings remain for four real statuses: the mapping table of Chapter 14 must handle `dlvd`, `cxl`, and `canceled` as well as the four proper words.

Then the prices, which arrive as text such as `Rs. 1,400`:

```python
price = pd.to_numeric(data["unit_price"].str.replace(r"^[^0-9]+", "", regex=True).str.replace(",", ""))
print(price.value_counts().sort_index())
```

```
unit_price
115.00      3606
290.00      5082
380.00      3583
430.00      4985
620.00      3575
750.00      3621
1,400.00    1380
Name: count, dtype: int64
```

- **`.str.replace(r"^[^0-9]+", "", regex=True)`** deletes any non-digits at the start (`^` start, `[^0-9]` not a digit, `+` one or more), so `Rs. 1,400` becomes `1,400`. `regex=True` says the first argument is a pattern, not literal text.
- **`.str.replace(",", "")`** then removes the thousands separator.
- **`pd.to_numeric(...)`** turns the cleaned text into numbers; add `errors="coerce"` to turn anything unreadable into a missing value instead of stopping.
- Every converted price is one of Riverstone's seven list prices for the products sold in Q4 (no garden chairs sell in winter): a validation rule passed.

And the customer codes, which should be four characters:

```python
print(data["customer_code"].str.len().value_counts().sort_index())
print(data["customer_code"].str.zfill(4).str.len().value_counts())
```

```
customer_code
2       40
3      493
4    25299
Name: count, dtype: int64
customer_code
4    25832
Name: count, dtype: int64
```

**`.str.len()`** counts characters. 533 codes lost their leading zeros. **`.str.zfill(4)`** pads with zeros on the left to four characters, like `LPAD(code, 4, '0')` in Chapter 14; after padding every code has four.

### Dates, one format at a time

Chapter 14's pattern profile replaced every digit with `9` to see the shapes of the dates. The same trick in pandas:

```python
print(data["order_date"].str.replace(r"\d", "9", regex=True).value_counts())
```

```
order_date
99-99-9999    20782
9999-99-99     3210
99/99/9999     1800
99999            40
Name: count, dtype: int64
```

Four shapes: day-first with dashes, year-first, day-first with slashes, and five-digit Excel serial numbers. Each needs its own rule, and a regular expression picks out the rows of each shape. Here is the first shape on its own, with three rows before and after:

```python
dash = data["order_date"].str.fullmatch(r"\d{2}-\d{2}-\d{4}")
first = pd.to_datetime(data.loc[dash, "order_date"], format="%d-%m-%Y", errors="coerce")
print(dash.sum(), "rows in this shape")
print(pd.DataFrame({"text": data.loc[dash, "order_date"], "date": first}).head(3))
```

```
20782 rows in this shape
         text       date
0  01-10-2025 2025-10-01
1  01-10-2025 2025-10-01
3  01-10-2025 2025-10-01
```

- **`\d{2}-\d{2}-\d{4}`** means two digits, a dash, two digits, a dash, four digits (`{2}` is "exactly twice").
- **`pd.to_datetime(text, format="%d-%m-%Y")`** reads the text with exactly this pattern, using the `strptime` codes of Chapter 17, section 17.11 (`%d` day, `%m` month, `%Y` year). Stating the format is the whole point: `05-11-2025` is 5 November, never 11 May.
- **`errors="coerce"`** turns a value that fits the shape but isn't a real date, such as `31-11-2025`, into **`NaT`** ("not a time"), the date version of `NaN`, instead of stopping.
- The `pd.DataFrame({...})` puts the text and the parsed date side by side, only to look at them.

Now all three text shapes, in a loop, filling one column of results:

```python
parsed = pd.Series(pd.NaT, index=data.index, dtype="datetime64[ns]")
shapes = [(r"\d{2}-\d{2}-\d{4}", "%d-%m-%Y"), (r"\d{2}/\d{2}/\d{4}", "%d/%m/%Y"), (r"\d{4}-\d{2}-\d{2}", "%Y-%m-%d")]
for pattern, fmt in shapes:
    mask = data["order_date"].str.fullmatch(pattern)
    parsed[mask] = pd.to_datetime(data.loc[mask, "order_date"], format=fmt, errors="coerce")
    print(fmt, "→ still missing:", parsed.isna().sum())
```

```
%d-%m-%Y → still missing: 5059
%d/%m/%Y → still missing: 3259
%Y-%m-%d → still missing: 49
```

- **`pd.Series(pd.NaT, index=data.index, dtype="datetime64[ns]")`** makes an empty date column, all `NaT`, with the same row labels as `data`, so results land on the right rows.
- **`shapes`** is a list of (pattern, format) pairs, and **`for pattern, fmt in shapes:`** unpacks each pair (Chapter 17, section 17.4).
- **`parsed[mask] = ...`** fills only the rows of that shape. After each shape the count of still-missing dates falls. The 49 left at the end are the 40 Excel serials and 9 dates that fit a shape but don't exist.

Excel stores a date as the number of days since 30 December 1899 (Chapter 10), so `45940` is 10 October 2025. Check one by hand, then convert all of them:

```python
print(pd.Timestamp("1899-12-30") + pd.Timedelta(days=45940))

serial = data["order_date"].str.fullmatch(r"\d{5}")
parsed[serial] = pd.Timestamp("1899-12-30") + pd.to_timedelta(data.loc[serial, "order_date"].astype(int), unit="D")
print(serial.sum(), "serials converted; still missing:", parsed.isna().sum())
```

```
2025-10-10 00:00:00
40 serials converted; still missing: 9
```

- **`pd.Timestamp("1899-12-30")`** is one date and time; **`pd.Timedelta(days=45940)`** is a length of time. Adding them gives the date, as `DATE '1899-12-30' + 45940` did in SQL.
- **`.astype(int)`** turns the five-digit text into numbers, and **`pd.to_timedelta(..., unit="D")`** turns each number into that many days.
- Nine dates are still missing: the impossible ones, such as 31 November.

Chapter 14 repaired those nine from the entry timestamp, because Riverstone's orders are entered on the order date, in Indian time. The timestamp is in UTC (the `Z` at the end means UTC), so convert it first:

```python
entered_ist = pd.to_datetime(data["entered_at_utc"], utc=True).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None)
repaired = parsed.isna()
parsed = parsed.fillna(entered_ist.dt.normalize())
print(repaired.sum(), "dates repaired from the entry timestamp")
print(pd.DataFrame({"text": data.loc[repaired, "order_date"], "entered_utc": data.loc[repaired, "entered_at_utc"],
                    "repaired": parsed[repaired].dt.date}))
```

```
9 dates repaired from the entry timestamp
             text           entered_utc    repaired
9128   31-09-2025  2025-10-28T13:53:00Z  2025-10-28
9178   31-11-2025  2025-10-28T03:36:00Z  2025-10-28
9182   32-10-2025  2025-10-28T05:23:00Z  2025-10-28
9187   32-10-2025  2025-10-28T15:21:00Z  2025-10-28
18221  31-11-2025  2025-11-28T16:35:00Z  2025-11-28
18272  31-11-2025  2025-11-28T10:31:00Z  2025-11-28
18323  32-10-2025  2025-11-30T04:59:00Z  2025-11-30
25894  31-11-2025  2025-12-28T15:09:00Z  2025-12-28
25903  31-09-2025  2025-12-28T07:13:00Z  2025-12-28
```

- **`pd.to_datetime(..., utc=True)`** reads the text as a time **in UTC**.
- **`.dt.tz_convert("Asia/Kolkata")`** moves it to Indian time, 5½ hours ahead, which can move a late-evening UTC entry onto the next day.
- **`.dt.tz_localize(None)`** then drops the time-zone label, keeping the Indian clock time, so it can sit in the same column as the other dates, which have no zone.
- **`repaired = parsed.isna()`** remembers which rows were missing **before** the repair, for the cleaning log.
- **`.dt.normalize()`** sets the time to midnight, keeping only the date, and **`.fillna(...)`** fills only the missing dates.

### The other columns, one at a time

**Discounts** are percentages, except where someone typed a fraction (`0.05` for 5%):

```python
discount = pd.to_numeric(data["discount_pct"])
is_fraction = discount.between(0, 1, inclusive="neither")
discount = pd.Series(np.where(is_fraction, discount * 100, discount), index=data.index)
print(is_fraction.sum(), "fractions converted;", sorted(discount.unique().tolist()))
```

```
1362 fractions converted; [0.0, 5.0, 8.0, 10.0, 12.0]
```

- **`inclusive="neither"`** makes `between` exclude both ends: 0 and 1 aren't fractions (0% and 1% are real discounts), but 0.05 is.
- **`np.where(is_fraction, discount * 100, discount)`**: where it's a fraction, multiply by 100; otherwise keep it. `np.where` returns a bare NumPy array, so **`pd.Series(..., index=data.index)`** gives it back its row labels.
- **`.unique().tolist()`** lists the distinct values as a plain Python list, and `sorted` puts them in order: only Riverstone's five real discount levels remain.

**Quantities** are in pieces, except 141 lines entered in cartons of 10, and a few are blank:

```python
quantity = pd.to_numeric(data["quantity"].replace("", None)) * data["qty_unit"].map({"CTN": 10}).fillna(1)
print((data["qty_unit"] == "CTN").sum(), "carton lines;", quantity.isna().sum(), "blank quantities")
```

```
141 carton lines; 14 blank quantities
```

- **`.replace("", None)`** turns empty text into a real missing value, so `pd.to_numeric` doesn't stop on it.
- **`.map({"CTN": 10}).fillna(1)`** gives 10 for carton lines and 1 for everything else, so multiplying converts cartons to pieces and leaves pieces alone.

**Products** are missing on a few lines, but each Q4 product has its own list price, so the price identifies it:

```python
price_to_product = {430: 101, 750: 102, 115: 103, 620: 104, 1400: 105, 1150: 106, 380: 107, 290: 108}
product_blank = data["product_id"].eq("")
product = pd.to_numeric(data["product_id"].replace("", None)).fillna(price.map(price_to_product))
print(product_blank.sum(), "products filled from the price;", product.isna().sum(), "still missing")
```

```
8 products filled from the price; 0 still missing
```

`.eq("")` is `== ""` written as a method. The dictionary is Riverstone's price list turned around (price → product), and `.fillna(price.map(...))` fills each blank product from its own row's price.

**Statuses** go through the mapping table:

```python
status_map = {"delivered": "Delivered", "dlvd": "Delivered", "cancelled": "Cancelled", "canceled": "Cancelled",
              "cxl": "Cancelled", "shipped": "Shipped", "pending": "Pending"}
status = data["status"].str.strip().str.lower().map(status_map)
print("unmapped statuses:", status.isna().sum())
print(status.value_counts().to_dict())
```

```
unmapped statuses: 0
{'Delivered': 22434, 'Pending': 1166, 'Shipped': 1138, 'Cancelled': 1094}
```

Zero unmapped: every spelling found in the profile has a row in the map. If next quarter's file brings a new spelling, this count stops being zero, which is the signal to extend the map.

### Build, validate, reconcile

```python
clean = pd.DataFrame({
    "order_item_id": data["order_item_id"].astype(int),
    "order_id": data["order_id"].astype(int),
    "order_date": parsed.dt.date,
    "customer_code": data["customer_code"].str.strip().str.zfill(4),
    "product_id": product.astype("Int64"),
    "quantity": quantity.astype("Int64"),
    "unit_price": price,
    "discount_pct": discount,
    "status": status,
})
clean["net_revenue"] = clean["quantity"] * clean["unit_price"] * (1 - clean["discount_pct"] / 100)
print(clean.shape)
print(clean.dtypes)
```

```
(25832, 10)
order_item_id      int64
order_id           int64
order_date        object
customer_code        str
product_id         Int64
quantity           Int64
unit_price       float64
discount_pct     float64
status               str
net_revenue      Float64
dtype: object
```

- **`pd.DataFrame({...})`** assembles the clean table from the cleaned columns; they all share `data`'s row labels, so each value lands on its own row.
- **`.astype("Int64")`**, with a capital I, is pandas' whole-number type that allows blanks (`<NA>`). Plain `int64` can't hold a blank, and the 14 blank quantities would force the column to `float64`.
- **`parsed.dt.date`** keeps only the date part; the column then holds Python dates, shown as `object`.

Chapter 14 quarantined the lines whose quantity was blank or above the historical maximum of 90 pieces. Set them aside, drop the cancelled lines, and reconcile:

```python
quarantine = clean["quantity"].isna() | (clean["quantity"] > 90)
ok = clean[(clean["status"] != "Cancelled") & ~quarantine]
print(len(clean), "clean lines;", int(quarantine.sum()), "quarantined")
print("net revenue excluding cancelled and quarantined:", round(ok["net_revenue"].sum(), 2))
```

```
25832 clean lines; 20 quarantined
net revenue excluding cancelled and quarantined: 423561010.5
```

- **`|`** combines the two reasons; **`~quarantine`** means "not quarantined".
- `int(...)` prints the count as a plain whole number.

**₹42,35,61,010.50**, to the paisa, the same figure as the SQL and Power Query pipelines in Chapter 14. That's what reconciliation looks like: three tools, one answer.

The companion script `clean_orders_pandas.py` holds the whole pipeline as one file, including the branch mapping and the cleaning log. Run it from `work/ch18` with `python clean_orders_pandas.py`, as Chapter 17 ran its scripts. It prints the same totals, logs 37 issues (20 quarantined lines, 9 repaired dates, 8 repaired products), and writes `clean_order_lines_pandas.csv` and `dq_order_issues_pandas.csv`, the pandas version of Chapter 14's cleaning log.

### Chapter 14's moves in pandas

| Task | SQL (Chapter 14) | pandas |
|---|---|---|
| Count blanks | `COUNT(*) FILTER (WHERE col IS NULL OR col = '')` | `df[col].isna().sum()` |
| Placeholders to blank | `NULLIF(TRIM(col), '')` | `df[col].replace(["N/A", "-", ""], None)` |
| Keep and label | `COALESCE(sales_rep, '(unassigned)')` | `df[col].fillna("(unassigned)")` |
| Remove rows | `WHERE quantity IS NOT NULL` | `df.dropna(subset=["quantity"])` |
| Fill down group labels | a window with `COUNT` (Chapter 13) | `df[col].ffill()` |
| Trim and normalize text | `LOWER(TRIM(col))` | `.str.strip()`, `.str.lower()`, `.str.replace()` |
| Map variants to standard values | a mapping table and a join | `.map(dict)`, then check `.isna()` for unmapped |
| Convert types safely | `CAST`, `CASE` with a pattern test | `pd.to_numeric(..., errors="coerce")`, `pd.to_datetime(..., format=...)` |
| Remove exact duplicates | `SELECT DISTINCT *` | `.drop_duplicates()`; `.duplicated(subset=[...], keep="last")` to choose |
| Find outliers | `WHERE quantity > 90` | `df[df["quantity"] > 90]` |
| Pad codes | `LPAD(TRIM(code), 4, '0')` | `.str.strip().str.zfill(4)` |
| Band or bucket | `CASE WHEN … THEN …` | `pd.cut`, `pd.qcut` |
| Conditional values | `CASE` | `np.where`, `np.select` |
| Fuzzy duplicates | similarity functions | a library such as `rapidfuzz` (`pip install rapidfuzz`) |

`.ffill()` ("forward fill") copies the last value above into each blank below it, Power Query's **Fill → Down**. `pd.qcut` makes bands with equal numbers of rows instead of fixed edges.

---

## 18.11 Charts with matplotlib and seaborn

Chapter 15 decided *which* chart and *how it should look*, and built the charts in a spreadsheet. This section draws the same charts in code. Code has one advantage over clicking: the rules can live in a function, so every chart obeys them.

**matplotlib** is Python's main charting library. Start with the chart Chapter 15 built in section 15.14: 2025's monthly revenue against target, from the same chart data:

```python
monthly_chart = pd.read_csv(COMPANION / "ch15" / "chart_data" / "monthly_2023_2025.csv")
m25 = monthly_chart[monthly_chart["year"] == 2025]
print(m25[["month", "net_revenue", "target_revenue"]].head(3).to_string(index=False))
print(round(m25["net_revenue"].sum() / m25["target_revenue"].sum() * 100, 1))
```

```
 month    net_revenue  target_revenue
     1  85,195,520.00        77350000
     2  78,582,579.00        70000000
     3 101,009,066.00       108050000
98.3
```

`.to_string(index=False)` prints the table without its row labels. The year finished at 98.3% of target, as in Chapter 15. (January shows ₹8,51,95,520 here and ₹8,51,95,521 in SQL, because each tool rounded the unrounded ₹8,51,95,520.50 differently.)

Now draw it, one step at a time. First, an empty figure with one chart area, and the actual line:

```python
import matplotlib
matplotlib.use("Agg")                       # draw to a file, not a window
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m25["month"], m25["net_revenue"] / 1e7, color="#0f5c8c", linewidth=2.5)
print(type(fig).__name__, type(ax).__name__)
```

```
Figure Axes
```

- **`matplotlib.use("Agg")`** tells matplotlib to draw into memory and files rather than open a window, which is what a script or a scheduled job needs. In a Jupyter notebook you can leave this line out: the chart then appears under the cell.
- **`import matplotlib.pyplot as plt`** is the usual short name.
- **`plt.subplots(figsize=(8, 4))`** creates a **figure** (the whole image, 8 × 4 inches) and one **axes** (the chart area inside it, with its own axes, lines, and labels). Everything below draws on `ax`.
- **`ax.plot(x, y, ...)`** draws a line through the points: months along the bottom, revenue up the side. Dividing by `1e7` (10⁷, one crore) shows crore instead of rupees. `color` takes a hex code and `linewidth` is in points.

Add the target as a dashed line, and label both lines directly instead of using a legend (Chapter 15, section 15.11):

```python
ax.plot(m25["month"], m25["target_revenue"] / 1e7, color="#5b6475", linewidth=1.5, linestyle="--")
ax.text(12.2, m25["net_revenue"].iloc[-1] / 1e7, "Actual", color="#0f5c8c", va="top")
ax.text(12.2, m25["target_revenue"].iloc[-1] / 1e7, "Target", color="#5b6475", va="bottom")
print(len(ax.lines), "lines,", len(ax.texts), "labels")
```

```
2 lines, 2 labels
```

- **`linestyle="--"`** dashes the target line, so it differs from the actual line by shape as well as color, which keeps it readable in gray print and for color-blind readers (Chapter 15, section 15.13).
- **`ax.text(x, y, "text", ...)`** writes text at a point on the chart. `12.2` is just right of December, and `.iloc[-1]` is the last value, December's. December's actual (₹8.7 crore) and target (₹9.2 crore) are close, so the labels would collide: **`va="top"`** hangs "Actual" just below its point and **`va="bottom"`** stands "Target" just above its own (`va` is the vertical alignment).

Then the words and the axis, following Chapter 15's rules: an action title, a unit on the axis, a zero baseline, and no box around the chart:

```python
ax.set_title("2025 finished at 98.3% of target", loc="left", fontweight="bold")
ax.set_ylabel("Net revenue (₹ crore)")
ax.set_ylim(0, 22)
ax.set_xticks(range(1, 13))
ax.spines[["top", "right"]].set_visible(False)
fig.savefig("revenue_vs_target_2025.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(Path("revenue_vs_target_2025.png").exists())
```

```
True
```

- **`set_title(..., loc="left", fontweight="bold")`** puts a bold title at the left, where the eye starts.
- **`set_ylim(0, 22)`** starts the value axis at zero. A line chart doesn't strictly need a zero baseline (Chapter 15, section 15.4), but when the size of a gap matters, such as actual against target, starting at zero stops a 2% miss looking like a collapse (section 15.12).
- **`set_xticks(range(1, 13))`** puts a mark at every month, 1 to 12.
- **`ax.spines[["top", "right"]]`** are the top and right edges of the chart's box; `set_visible(False)` hides them.
- **`fig.savefig(path, dpi=150, bbox_inches="tight")`** saves the image: `dpi` (dots per inch) sets the sharpness, and `bbox_inches="tight"` trims the empty margin. **`plt.close(fig)`** frees the memory, which matters in a script that draws dozens of charts.

Figure 18.1 shows the chart after the first step and when finished.

![Two line charts of Riverstone's 2025 monthly net revenue in crore. Left, after step 1: one blue line with default axes and a box around it, the value axis starting near 4. Right, finished: the blue actual line and a dashed gray target line, labeled Actual and Target at the right end, a bold left-aligned title "2025 finished at 98.3% of target", the value axis from 0 to 22 crore titled "Net revenue (₹ crore)", months 1 to 12 marked, and no top or right border](figures/fig18-1-chart-steps.svg)

*Figure 18.1 — The same chart after step 1 and when finished. Every change on the right is one line of code: the dashed target, the direct labels, the action title, the unit, the zero baseline, and the missing top and right edges.*

### Put the rules in a function

Every chart needs the same styling lines, so write them once, as a function, and call it for every chart. The cell below defines `style_axes` and then uses it to draw 2025's revenue on its own, with a gridline behind the data this time.

```python
INK, MUTED, ACC, LIGHT, GRAY = "#1d2330", "#5b6475", "#0f5c8c", "#dfe5ec", "#9aa3af"

def style_axes(ax, title, ylabel=None):
    """Apply Chapter 15's rules: left-aligned action title, no top or right edge, light gridlines."""
    ax.set_title(title, loc="left", fontweight="bold", color=INK)
    if ylabel:
        ax.set_ylabel(ylabel, color=MUTED)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=LIGHT, linewidth=0.8)
    ax.set_axisbelow(True)
    return ax

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(m25["month"], m25["net_revenue"] / 1e7, color=ACC, linewidth=2.5)
style_axes(ax, "2025 revenue peaked in October at ₹18.1 crore", "₹ crore")
ax.set_ylim(bottom=0)
ax.set_xticks(range(1, 13))
fig.savefig("revenue_2025.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(round(m25["net_revenue"].max() / 1e7, 2))
```

```
18.06
```

- **Named colors** at the top (`INK`, `ACC`, …) keep the palette in one place. Assigning five names from five values in one line is the unpacking of Chapter 17.
- **`style_axes(ax, title, ylabel=None)`** takes the chart area and applies the rules. `ylabel=None` makes the axis title optional, and **`if ylabel:`** skips it when none is given (Chapter 17's truthiness).
- **`ax.grid(axis="y", ...)`** draws light horizontal gridlines only, and **`set_axisbelow(True)`** keeps them behind the data.
- **`set_ylim(bottom=0)`** fixes only the bottom of the axis at zero and lets matplotlib choose the top.

The pattern is always the same: **`fig, ax = plt.subplots()`**, draw onto `ax`, style it, save, close. Working with the `ax` object rather than the `plt.…` shortcuts you'll see in tutorials is what lets you put several charts on one figure and write helpers like `style_axes`.

### Bars: revenue by region

The database has no region, only a city. Chapter 16 mapped each of Riverstone's 39 cities to a region with `companion/ch16/city_region.csv`; use the same file, so the numbers agree:

```python
city_region = pd.read_csv(COMPANION / "ch16" / "city_region.csv")
region_of = city_region.set_index("city")["region"]
print(len(region_of), region_of.head(3).to_dict())

with_region = sales2025.assign(region=sales2025["city"].map(region_of).fillna("City missing"))
by_region = with_region.groupby("region")["net_revenue"].sum().sort_values() / 1e7
print(by_region.round(1))
```

```
39 {'Mumbai': 'West', 'Pune': 'West', 'Ahmedabad': 'West'}
region
City missing    2.30
East           14.20
North          27.90
South          31.90
West           38.40
Name: net_revenue, dtype: float64
```

- **`region_of`** is a Series of regions labelled by city, the lookup of section 18.7.
- **`.fillna("City missing")`** labels the customers with no city, as Chapter 16 did in Power Query, so their revenue stays visible instead of disappearing: ₹2.3 crore from 91 customers.
- **`.sort_values()`** sorts smallest first, because a horizontal bar chart draws its first bar at the bottom.

```python
colors = [GRAY if region == "City missing" else ACC for region in by_region.index]

fig, ax = plt.subplots(figsize=(7, 3))
ax.barh(by_region.index, by_region.values, color=colors)
for y, v in enumerate(by_region.values):
    ax.text(v + 0.3, y, f"{v:,.1f}", va="center", color=INK, fontsize=9)
style_axes(ax, "West brought the most revenue in 2025 (₹ crore)")
ax.grid(False)
ax.set_xticks([])
fig.savefig("region_2025.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(colors)
```

```
['#9aa3af', '#0f5c8c', '#0f5c8c', '#0f5c8c', '#0f5c8c']
```

- **The list comprehension** (Chapter 17) picks gray for "City missing" and blue for the regions, Chapter 15's rule for a missing category: shown, but not competing. The bar also says "City missing" in words, so the meaning doesn't depend on color.
- **`ax.barh(labels, values, color=...)`** draws horizontal bars.
- **`for y, v in enumerate(...)`** walks the values with their position (0 for the bottom bar, 1 for the next), and **`ax.text(v + 0.3, y, ...)`** writes each value just past the end of its bar. `fontsize=9` is in points.
- **`ax.grid(False)`** and **`ax.set_xticks([])`** remove the gridlines and the value axis: with the numbers on the bars, they're clutter. Figure 18.2 is the result.

![A horizontal bar chart titled "West brought the most revenue in 2025 (₹ crore)": West 38.4, South 31.9, North 27.9, East 14.2 in blue, and City missing 2.3 in gray at the bottom, each value written at the end of its bar, with no value axis](figures/fig18-2-region-bars.svg)

*Figure 18.2 — Revenue by region, drawn by the code above. The five bars add up to the year's ₹114.7 crore; the customers with no city are shown, labeled, and grayed rather than dropped.*

### seaborn: statistical charts in one line

**seaborn** sits on top of matplotlib and draws statistical charts, such as the box plots of Chapter 15, in one call. It takes long-format data (section 18.8): one row per order, with the segment in a column.

```python
import seaborn as sns

order_values = sales2025.groupby(["order_id", "segment"], as_index=False)["net_revenue"].sum()
print(order_values.head(3))
print(order_values["net_revenue"].max())
```

```
   order_id      segment  net_revenue
0     10001       Retail     2,900.00
1     10002  Hospitality    20,900.00
2     10003       Retail    45,712.50
143175.0
```

- **`as_index=False`** keeps `order_id` and `segment` as ordinary columns instead of making them the index, which is the shape seaborn wants.
- The largest 2025 order is ₹1,43,175, which tells you how wide the chart's value axis must be.

```python
fig, ax = plt.subplots(figsize=(8, 3))
sns.boxplot(data=order_values, x="net_revenue", y="segment", ax=ax, color="#e3edf5", fliersize=2)
style_axes(ax, "Wholesale orders are larger and more spread out")
ax.set_xlim(left=0)
ax.set_xlabel("Order value (₹)")
ax.set_ylabel("")
fig.savefig("order_values.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print(order_values.groupby("segment")["net_revenue"].median())
```

```
segment
Hospitality   19,121.88
Retail        19,425.00
Wholesale     25,762.50
Name: net_revenue, dtype: float64
```

- **`sns.boxplot(data=..., x=..., y=..., ax=ax)`** names the table and the columns, and draws onto your `ax`, so `style_axes` still works. `fliersize=2` makes the outlier dots small.
- **`ax.set_xlim(left=0)`** starts the value axis at zero and leaves the top to matplotlib, so every order, up to the largest, stays on the chart. If you ever cut an axis short to make the boxes readable, say so on the chart and give the number of orders hidden, because a cut axis hides data (Chapter 15, section 15.12).
- **`set_xlabel`** names the axis and its unit; **`set_ylabel("")`** removes the label seaborn added, because the segment names speak for themselves.

Figure 18.3 shows the chart. The medians are Chapter 15's figures again: Wholesale ₹25,762.50, Retail ₹19,425, Hospitality ₹19,121.88. Chapter 15 rounded them to the rupee; pandas' median averages the middle two orders when there's an even number, exactly as `MEDIAN` and `QUARTILE.INC` do.

![Horizontal box plots of 2025 order values for Retail, Hospitality, and Wholesale, on an axis from 0 to about 1,45,000 rupees. Wholesale's box sits further right and is wider; all three have many small dots to the right of their whiskers](figures/fig18-3-order-value-boxes.svg)

*Figure 18.3 — The box plots from `sns.boxplot`, styled by `style_axes`. The dots are large orders beyond the whiskers; the biggest, ₹1,43,175, is a Wholesale order.*

| Chart (Chapter 15) | matplotlib | seaborn |
|---|---|---|
| Bar | `ax.bar` / `ax.barh` | `sns.barplot` |
| Line | `ax.plot` | `sns.lineplot` |
| Histogram | `ax.hist` | `sns.histplot` |
| Box plot | `ax.boxplot` | `sns.boxplot` |
| Scatter | `ax.scatter` | `sns.scatterplot` |
| Heatmap | `ax.imshow` | `sns.heatmap` |
| Small multiples | `plt.subplots(2, 3)` | `sns.FacetGrid`, `sns.relplot(col=...)` |

`df.plot()` (pandas' own shortcut to matplotlib) is the quickest way to look at something while exploring; for anything a colleague will see, write it out with `subplots` and a style function. For maps with city-level symbols or custom boundaries, Power BI's map visuals (Chapter 16) are usually quicker than Python's map libraries.

---
## 18.12 Writing Excel people are glad to receive

A CSV is data. A workbook with formatted numbers, a frozen header, sensible column widths, and a chart is a deliverable. This section builds one in four steps: the data, the headings, the layout, and the chart.

First, the two tables it will hold:

```python
region_table = (with_region.groupby("region")
                .agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
                .sort_values("net_revenue", ascending=False).reset_index())
monthly_table = (sales2025.groupby("month")
                 .agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
                 .reset_index())
print(region_table)
print(monthly_table.shape)
```

```
         region    net_revenue  orders
0          West 383,840,548.50   15405
1         South 318,624,642.00   12916
2         North 279,250,231.25   11333
3          East 142,256,284.00    5797
4  City missing  22,669,945.50     905
(12, 3)
```

Both are the named aggregations of section 18.6: revenue summed and orders counted with `nunique`, one table by region (largest first) and one by month. `.reset_index()` turns the group labels (region, month) back into ordinary columns, so they're written to the sheet as data.

**Step 1: the data.** An **`ExcelWriter`** is an open workbook that several tables can be written into, one sheet each:

```python
writer = pd.ExcelWriter("riverstone_2025.xlsx", engine="xlsxwriter")
region_table.to_excel(writer, sheet_name="By region", index=False, startrow=2)
monthly_table.to_excel(writer, sheet_name="By month", index=False, startrow=2)
print(list(writer.sheets))
```

```
['By region', 'By month']
```

- **`engine="xlsxwriter"`** chooses the library that writes the file. xlsxwriter is the one for formatting and charts when you **create** a file; `engine="openpyxl"` is for adding to an **existing** workbook (`mode="a"`).
- **`index=False`** leaves out the row labels 0, 1, 2, … which mean nothing to a reader.
- **`startrow=2`** starts the table on the third row, leaving room for a title. Rows and columns here count from **zero**: row 0 is Excel's row 1.
- **`writer.sheets`** holds the sheets written so far.

The file isn't saved until the writer is closed, in step 4. (Written as `with pd.ExcelWriter(...) as writer:`, the `with` block of Chapter 17 closes it for you; here the work is spread over four cells, so it's closed by hand.)

**Step 2: a title and a formatted header row.** xlsxwriter describes a format as a dictionary of settings, and writes one cell at a time:

```python
book = writer.book
title = book.add_format({"bold": True, "font_size": 14, "font_color": "#1d2330"})
header = book.add_format({"bold": True, "bg_color": "#0f5c8c", "font_color": "white"})

for sheet_name, table in [("By region", region_table), ("By month", monthly_table)]:
    sheet = writer.sheets[sheet_name]
    sheet.write(0, 0, f"Riverstone 2025: revenue {sheet_name.lower()}", title)
    for col, name in enumerate(table.columns):
        sheet.write(2, col, name.replace("_", " ").title(), header)
print([name.replace("_", " ").title() for name in region_table.columns])
```

```
['Region', 'Net Revenue', 'Orders']
```

- **`writer.book`** is the workbook itself, and **`book.add_format({...})`** makes a format: `bold`, `font_size` in points, `font_color` and `bg_color` (the fill) as hex codes.
- **`sheet.write(row, col, value, format)`** writes one cell. `(0, 0)` is **A1**: row 0, column 0.
- The header row is row 2 (Excel's row 3), where `startrow=2` put it. Writing it again, formatted, replaces pandas' plain header. **`.replace("_", " ").title()`** also turns `net_revenue` into `Net Revenue`, so the sheet's headings are no longer the DataFrame's column names; remember that when you read the file back.

**Step 3: widths, number format, and a frozen header:**

```python
money = book.add_format({"num_format": "#,##0"})
for sheet_name in ["By region", "By month"]:
    sheet = writer.sheets[sheet_name]
    sheet.set_column(0, 0, 16)
    sheet.set_column(1, 1, 16, money)
    sheet.set_column(2, 2, 10)
    sheet.freeze_panes(3, 0)
print("widths, formats, and panes set")
```

```
widths, formats, and panes set
```

- **`num_format`** takes an Excel number format (Chapter 10): `#,##0` shows whole rupees with separators. The value in the cell stays exact; only its display changes.
- **`set_column(first, last, width, format)`** sets the width of columns `first` to `last` (0 is A), and optionally their format.
- **`freeze_panes(3, 0)`** freezes everything above row 3 (Excel's row 4), so the title and header stay in view while scrolling.

**Step 4: a chart, then save:**

```python
chart = book.add_chart({"type": "column"})
chart.add_series({"categories": ["By month", 3, 0, 14, 0], "values": ["By month", 3, 1, 14, 1],
                  "name": "Net revenue", "fill": {"color": "#0f5c8c"}})
chart.set_title({"name": "2025 revenue by month"})
chart.set_legend({"none": True})
writer.sheets["By month"].insert_chart("E4", chart, {"x_scale": 1.3, "y_scale": 1.3})
writer.close()
print(Path("riverstone_2025.xlsx").exists())
```

```
True
```

- **`book.add_chart({"type": "column"})`** creates an Excel column chart, a real chart that stays linked to the cells.
- **`add_series`** tells it where the data is, as `[sheet, first_row, first_col, last_row, last_col]`, counting from zero. `["By month", 3, 0, 14, 0]` is rows 3 to 14 of column 0, which is **A4:A15**, the twelve months; `["By month", 3, 1, 14, 1]` is B4:B15, their revenue.
- **`"name"`** labels the series and **`"fill"`** colors its columns, with the same blue as the charts in section 18.11.
- **`set_title`** gives the chart its title, and **`set_legend({"none": True})`** hides the legend: one series needs no key, because the title says what it is.
- **`insert_chart("E4", chart, {...})`** places the chart with its top-left corner at E4, scaled to 130%. **`writer.close()`** saves the file.

Read it back, which is how you check an export without opening Excel:

```python
check = pd.read_excel("riverstone_2025.xlsx", sheet_name="By month", header=2)
print(check.shape, check.columns.tolist())
print(round(check["Net Revenue"].sum(), 2) == round(sales2025["net_revenue"].sum(), 2))
```

```
(12, 3) ['Month', 'Net Revenue', 'Orders']
True
```

- **`header=2`** says the column headings are on row 2 (Excel's row 3), under the title.
- The columns are called `Net Revenue`, not `net_revenue`, because step 2 rewrote the header row.
- The total in the file equals the total in pandas: nothing was lost or rounded on the way.

The habits behind the code:

- **Number formats** belong in the file (`#,##0`), not in the values: never round the underlying numbers to make them look tidy.
- **Freeze panes, column widths, and a title** take five lines and are the difference between "a dump" and "a report".

> **Watch out: openpyxl can't preserve everything.** Opening a workbook full of pivot tables, macros, or conditional formatting and saving it again through openpyxl can drop features. When the destination is a template with formatting you must keep, write only the data sheet, or use a tool that edits in place, such as the VBA and Office Scripts of Chapter 19.

### Checkpoint: week 3

Write a workbook with one sheet, "By segment", holding 2025 revenue and orders per segment from `sales2025`, with a title in A1, a formatted header, a `#,##0` money column, and a frozen header. Read it back and prove the total is ₹1,14,66,41,651.25. The answer is at the end of the chapter.

---

## 18.13 Reading from a database

The best pandas code often starts with SQL. Let the database filter and aggregate; bring back what you actually need.

### Keep the password out of the code

A connection needs the database's address, your user name, and your password: in Chapter 12's setup, the `postgres` user (or MySQL's `root`) and the password you chose. A password written into a notebook ends up in every copy of that notebook, and in version control forever (Chapter 26). So it goes in an **environment variable** instead: a named value that the operating system hands to every program you start, outside your code.

The simplest way to set one for a project is a **`.env` file**: a plain text file in the project folder, one `NAME=value` per line. Create `work/ch18/.env` in VS Code with this line, putting your own password in place of `your-password`:

```text
RIVERSTONE_DB=postgresql+psycopg://postgres:your-password@localhost:5432/riverstone_full
```

That line is a **connection URL**, SQLAlchemy's way of writing all the connection details as one piece of text: `dialect+driver://user:password@host:port/database`. Here the dialect is `postgresql`, the driver `psycopg`, the host `localhost` (this computer, as in Chapter 12), and the port 5432. For MySQL, write `mysql+mysqlconnector://root:your-password@localhost:3306/riverstone_full`.

The package `python-dotenv` reads that file into the environment, and `os.environ` reads the variable back:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.environ["RIVERSTONE_DB"])
print(engine.dialect.name)
```

```
postgresql
```

- **`load_dotenv()`** looks for a `.env` file in the current folder (and, if there's none, in the folders above it) and copies its variables into the environment. A variable that's already set is left alone, so a scheduler or a colleague can set it another way.
- **`os.environ["RIVERSTONE_DB"]`** reads the variable, like a dictionary. If it isn't set, this stops with a `KeyError` naming it, which is the right error.
- **`create_engine(url)`** from **SQLAlchemy** makes an **engine**: an object that knows how to reach the database and opens connections when pandas needs them. It doesn't connect yet.
- **`engine.dialect.name`** confirms which kind of database it's for, without printing the password.

> **Setting an environment variable in the terminal.** Instead of a `.env` file you can set the variable for the current terminal session. Windows PowerShell: `$env:RIVERSTONE_DB = "postgresql+psycopg://…"`. macOS or Linux: `export RIVERSTONE_DB="postgresql+psycopg://…"`. It lasts until you close that terminal. Either way, add `.env` to the project's `.gitignore` so it never reaches Git (Chapter 26).

### A query with parameters

The query below is Chapter 13's kind of SQL, on the `sales_lines` view (Chapter 13, section 13.2; the full dataset's setup script from Chapter 14 creates it in `riverstone_full` too). It has one new part: **`:start`**, a **bound parameter**. Instead of pasting a date into the SQL text, you leave a named slot and pass the value separately. The database receives the value as a value, never as part of the SQL, so a quote or a date format can't break the query, and nobody can slip extra SQL in through it (**SQL injection**).

```python
query = text("""
    SELECT c.segment, DATE_TRUNC('month', s.order_date)::date AS month,
           SUM(s.net_revenue) AS net_revenue, COUNT(DISTINCT s.order_id) AS orders
    FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
    WHERE s.order_date >= :start
    GROUP BY 1, 2 ORDER BY 1, 2
""")
by_segment = pd.read_sql(query, engine, params={"start": "2025-01-01"}, parse_dates=["month"])

print(by_segment.shape)
print(by_segment.head(3))
print(by_segment.groupby("segment")["net_revenue"].sum())
```

```
(36, 4)
       segment      month   net_revenue  orders
0  Hospitality 2025-01-01 20,097,757.50     964
1  Hospitality 2025-02-01 19,543,963.75     946
2  Hospitality 2025-03-01 21,701,085.00     986
segment
Hospitality   277,476,705.00
Retail        556,436,453.75
Wholesale     312,728,492.50
Name: net_revenue, dtype: float64
```

- **`text("""...""")`** wraps the SQL so SQLAlchemy knows it contains `:name` parameters. The triple quotes let it run over several lines.
- **`pd.read_sql(query, engine, params={...})`** runs the query and returns a DataFrame. `params` fills each `:name` slot.
- **`parse_dates=["month"]`** makes the month column a date column, as in `read_csv`.
- The segment totals match `sales2025` above to within a rupee: the SQL added up the months after rounding each one, pandas added the unrounded lines.

**In MySQL**, only the month expression changes: `DATE_TRUNC('month', …)::date` is PostgreSQL. Chapter 15 wrote MySQL's version with `DATE_FORMAT`:

<!-- run: none -->
```python
query_mysql = text("""
    SELECT c.segment, CAST(DATE_FORMAT(s.order_date, '%Y-%m-01') AS DATE) AS month,
           SUM(s.net_revenue) AS net_revenue, COUNT(DISTINCT s.order_id) AS orders
    FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
    WHERE s.order_date >= :start
    GROUP BY 1, 2 ORDER BY 1, 2
""")
by_segment = pd.read_sql(query_mysql, engine, params={"start": "2025-01-01"}, parse_dates=["month"])
print(by_segment.shape)
print(by_segment.head(3))
```

```
(36, 4)
       segment      month   net_revenue  orders
0  Hospitality 2025-01-01 20,097,757.50     964
1  Hospitality 2025-02-01 19,543,963.75     946
2  Hospitality 2025-03-01 21,701,085.00     986
```

`DATE_FORMAT(s.order_date, '%Y-%m-01')` writes each date as the first of its month, as text, and `CAST(... AS DATE)` turns that text back into a date, the MySQL route of Chapter 15, section 15.15. Run this cell instead of the one above if your `RIVERSTONE_DB` points at MySQL; it returns the same 36 rows.

The habits behind the code:

- **Never paste credentials into code.** Environment variables or a `.env` file that Git ignores.
- **Pass values with `:name` and `params={...}`**, never by building the SQL with f-strings. That's how SQL injection happens, and it also breaks on dates and quotes.
- **`chunksize=100000`** in `read_sql` streams a large result in pieces instead of loading it all at once.

### Writing a table back

`to_sql` writes a DataFrame into a database table. It's one line, and worth thinking about before you use it on a shared database: most analysts may read the warehouse but not write to it (Part 3). To practise, write into **SQLite**, a small database that lives in one file on your computer and comes built into Python, so there's no server and nothing to break:

```python
summary = by_segment.groupby("segment", as_index=False)["net_revenue"].sum()

scratch = create_engine("sqlite:///ch18_scratch.db")
summary.to_sql("segment_summary", scratch, if_exists="replace", index=False)

back = pd.read_sql(text("SELECT * FROM segment_summary ORDER BY net_revenue DESC"), scratch)
print(back)
```

```
       segment    net_revenue
0       Retail 556,436,453.75
1    Wholesale 312,728,492.50
2  Hospitality 277,476,705.00
```

- **`sqlite:///ch18_scratch.db`** is SQLite's connection URL: three slashes, then a file name. The file is created the first time.
- **`to_sql(name, engine, if_exists="replace", index=False)`** creates the table and inserts the rows. `if_exists="replace"` drops and recreates the table if it exists; `"append"` adds rows; the default, `"fail"`, stops with an error.
- The same line with your `RIVERSTONE_DB` engine would write into PostgreSQL or MySQL, if you're allowed to.

`to_sql` is fine for small results (a summary, a mapping table, a list of exceptions) in a schema you're allowed to write to. It is not a data-loading tool: for volume, use the database's own loader, and for anything that becomes a permanent table, talk to whoever owns the warehouse (Part 3).

**Where should the work happen?** In the database when it's filtering, joining large tables, and aggregating: it has indexes and it's designed for it. In pandas when you need reshaping, string handling, charts, Excel output, or anything statistical. The pattern that scales is a query that returns thousands of rows, not millions.

---

## 18.14 Calling an API

Chapter 2 described an **API**: a way for one program to ask another for data over the web, with a request that names what you want and a reply that's usually **JSON** (Chapter 17, section 17.9). Every reply also carries a three-digit **status code** that says how it went. Chapter 2 showed the main ones; here is the full table you'll use when a script calls an API:

| Code | Meaning | Whose problem | What the script should do |
|---|---|---|---|
| `200 OK` | it worked; the data is in the reply | nobody's | read the reply |
| `201 Created` | a new record was created | nobody's | note the new record's ID |
| `204 No Content` | it worked, and there's nothing to send back | nobody's | carry on |
| `400 Bad Request` | the request is malformed | yours | fix what you sent; don't retry |
| `401 Unauthorized` | no token, or a wrong or expired one | yours | check the token |
| `403 Forbidden` | you're recognized, but not allowed to do this | yours | ask for the right permission; don't retry |
| `404 Not Found` | no such address or record | yours | check the address |
| `429 Too Many Requests` | you're calling too fast | yours, for now | wait, then retry |
| `500`, `502`, `503` | the server failed | theirs | wait, then retry a few times |

The first digit tells you most of it: 2 is success, 4 is a problem with your request, 5 is a problem at the other end.

### A demonstration API on your own computer

Real APIs sit on the internet, need an account, and change. So the companion folder includes a tiny demonstration API for Riverstone that runs on your own computer: `api_demo.py`. It serves Riverstone's order lines for any dates you ask for, a page at a time, and it wants a token, like a real one. Open a **second** terminal in VS Code (the **+** in the terminal panel), activate the environment, and start it:

<!-- run: none -->
```
# terminal
$ python api_demo.py
Riverstone demo API on http://localhost:8018  (Ctrl+C to stop)
```

Leave it running. It listens at `http://localhost:8018`: the address is this computer, and 8018 is the port it listens on. Its token is `demo-token-18`. A real API's token is as secret as a password, so treat this one the same way and add it to `.env`:

```text
API_TOKEN=demo-token-18
```

### Your first request

**`requests`** is the package that sends web requests from Python. Ask the API for the order lines of 1 December 2025:

```python
import requests

load_dotenv()
BASE = "http://localhost:8018/v1/orders"
headers = {"Authorization": f"Bearer {os.environ['API_TOKEN']}", "Accept": "application/json"}

response = requests.get(BASE, params={"from": "2025-12-01", "to": "2025-12-01", "page": 1, "page_size": 100},
                        headers=headers, timeout=30)
print(response.status_code)
payload = response.json()
print(payload["page"], "of", payload["pages"], "pages;", payload["count"], "lines in all;",
      len(payload["results"]), "on this page")
print(payload["results"][0])
```

```
200
1 of 3 pages; 296 lines in all; 100 on this page
{'order_item_id': 296, 'order_id': 10158, 'order_date': '2025-12-01', 'customer_id': 23, 'product_id': 103, 'quantity': 5, 'unit_price': 115.0, 'discount_pct': 0.0, 'status': 'Delivered'}
```

- **`load_dotenv()`** again, because `.env` gained a line since section 18.13.
- **`requests.get(url, params=..., headers=..., timeout=...)`** sends a GET request, the kind that asks for data.
  - **`params`** become the part of the address after `?`: `?from=2025-12-01&to=2025-12-01&page=1&page_size=100`. `requests` writes it correctly for you.
  - **`headers`** travel with the request. **`Authorization: Bearer <token>`** is the most common way to present a token; `Accept` says you want JSON back.
  - **`timeout=30`** gives up after 30 seconds. Without it, a server that never answers hangs your script forever.
- **`response.status_code`** is the code from the table: 200.
- **`response.json()`** turns the JSON reply into Python dictionaries and lists (Chapter 17). This API's reply says which page it is, how many pages and lines there are, and holds the lines in `results`.

What if the token is missing?

```python
no_token = requests.get(BASE, params={"from": "2025-12-01", "to": "2025-12-01"}, timeout=30)
print(no_token.status_code, no_token.json())

try:
    no_token.raise_for_status()
except requests.HTTPError as error:
    print("stopped:", error)
```

```
401 {'error': 'missing or invalid token'}
stopped: 401 Client Error: Unauthorized for url: http://localhost:8018/v1/orders?from=2025-12-01&to=2025-12-01
```

- The API answered, but with **401** and an error message instead of data. A script that doesn't look at the status code would carry on and try to read orders from an error message.
- **`raise_for_status()`** raises an exception (Chapter 17, section 17.10) for any 4xx or 5xx code, and does nothing for a 2xx. Call it after every request, so a failed call stops the script instead of producing a "successful" run with no data.

### Paging through the results

Almost every API returns long results in **pages**, and says how many there are. Ask for page 1, 2, 3, … until you've had them all:

```python
all_rows = []
page = 1
while True:
    reply = requests.get(BASE, params={"from": "2025-12-01", "to": "2025-12-01", "page": page, "page_size": 100},
                         headers=headers, timeout=30)
    reply.raise_for_status()
    data = reply.json()
    all_rows.extend(data["results"])
    print("page", page, "of", data["pages"], "→", len(data["results"]), "lines")
    if page >= data["pages"]:
        break
    page += 1

print(len(all_rows), "lines collected")
```

```
page 1 of 3 → 100 lines
page 2 of 3 → 100 lines
page 3 of 3 → 96 lines
296 lines collected
```

- **`while True:`** repeats until a **`break`** (Chapter 17, section 17.6). The loop stops when the page just read is the last one, `data["pages"]`.
- **`all_rows.extend(...)`** adds the page's lines to the list; `append` would add the whole page as one item.
- 100 + 100 + 96 = 296 lines, the `count` the first reply promised. Always compare what you collected with the count the API reports.

Now turn the list into a table:

```python
rows = pd.json_normalize(all_rows)
rows["order_date"] = pd.to_datetime(rows["order_date"])
rows["net_revenue"] = rows["quantity"] * rows["unit_price"] * (1 - rows["discount_pct"] / 100)
print(rows.shape)
print(rows[["order_id", "order_date", "quantity", "unit_price", "net_revenue"]].head(3))
print(round(rows.loc[rows["status"] != "Cancelled", "net_revenue"].sum(), 2))
```

```
(296, 10)
   order_id order_date  quantity  unit_price  net_revenue
0     10158 2025-12-01         5      115.00       575.00
1     10158 2025-12-01        40      620.00    24,800.00
2     10159 2025-12-01        35      430.00    13,545.00
3477046.0
```

**`pd.json_normalize(list_of_records)`** turns a list of JSON records into a DataFrame, one row per record. The next two lines are section 18.1's date and revenue steps; `rows.loc[rows["status"] != "Cancelled", "net_revenue"]` picks the revenue of the lines that weren't cancelled, ₹34,77,046 for 1 December. These records are flat, so `pd.DataFrame(all_rows)` would work too; `json_normalize` earns its name with **nested** JSON, where a record holds another record or a list: `record_path=` digs into a list inside each record, and `meta=` carries parent fields down to each row.

### Being polite, and surviving failures

Real APIs limit how fast you may call them. When you go too fast they answer **429**, and when they're overloaded **5xx**. Both are worth a retry after a pause, and the pause should grow each time. A small helper does it:

```python
import time

def get_with_retry(url, params, headers, attempts=4):
    """GET with a timeout; wait and retry on 429 and 5xx; stop on any other error."""
    for attempt in range(1, attempts + 1):
        reply = requests.get(url, params=params, headers=headers, timeout=30)
        print("attempt", attempt, "→", reply.status_code)
        if reply.status_code == 429 or reply.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        reply.raise_for_status()
        return reply.json()
    raise RuntimeError(f"gave up after {attempts} attempts")

first_page = get_with_retry(BASE, {"from": "2025-12-01", "to": "2025-12-01", "page": 1}, headers)
print(first_page["count"])
```

```
attempt 1 → 200
296
```

- **`for attempt in range(1, attempts + 1):`** tries up to four times.
- On **429 or any 5xx**, **`time.sleep(2 ** attempt)`** waits 2, 4, 8, then 16 seconds (`**` is "to the power of") before **`continue`** starts the next attempt. Growing waits give an overloaded server room to recover.
- Any other error, such as 401 or 404, is **your** problem, so `raise_for_status()` stops at once: retrying a bad request only repeats it.
- If every attempt fails, **`raise RuntimeError(...)`** stops the script with a clear message. Here the demo API answered the first time.

The companion file `api_response.json` is a saved copy of page 1 of this same reply. Saving the raw reply before you parse it is a good habit: when a number looks wrong next month, you can see exactly what the API sent.

```python
import json

saved = json.loads(Path("api_response.json").read_text(encoding="utf-8"))
print(saved["page"], "of", saved["pages"], "pages;", len(saved["results"]), "lines")
print(saved["results"] == payload["results"])
```

```
1 of 3 pages; 100 lines
True
```

`json.loads` turns JSON text into Python objects (Chapter 17, section 17.9), and the saved page is identical to the page the API sent a moment ago. When you've finished with the demo API, press **Ctrl+C** in its terminal to stop it.

---
## 18.15 The whole thing as one script

Everything so far has been pieces. Here they are assembled the way an automated monthly report actually looks: load, check, summarize, write, and report on itself. Chapter 17 (section 17.12) turned a notebook into a script with functions, an argument from `sys.argv`, and an exit code. This section does the same with pandas, in six steps, and adds the two standard-library modules that scripts which run unattended rely on: `logging` and `argparse`. Each step is one function, written and tried in the notebook first. At the end they go into one file, `monthly_report.py`, which is in the companion folder, finished.

### Step 1: load the month

The report needs the month's order lines, the same month a year earlier (for a check), and the month's target:

```python
import logging
from datetime import datetime

log = logging.getLogger("monthly_report")

QUERY = text("""
    SELECT s.order_date, s.order_id, s.customer_id, c.segment, p.product_name,
           s.quantity, s.net_revenue, s.product_cost
    FROM sales_lines s
    JOIN customers c ON c.customer_id = s.customer_id
    JOIN products  p ON p.product_id  = s.product_id
    WHERE s.order_date >= :start AND s.order_date < :end
""")
TARGET_QUERY = text("SELECT target_revenue FROM sales_targets WHERE target_month = :month")


def month_range(month):
    """Return the first day of the month, and the first day of the next month."""
    start = pd.Timestamp(month + "-01")
    end = start + pd.offsets.MonthBegin(1)
    return start.date(), end.date()


print(month_range("2025-12"))
```

```
(datetime.date(2025, 12, 1), datetime.date(2026, 1, 1))
```

- A **log** is a list of timestamped messages a script writes as it works, so that when it runs at 7 a.m. with nobody watching, you can read afterwards what it did. The standard library's **`logging`** module writes them. **`log = logging.getLogger("monthly_report")`** makes a named **logger**; `log.info(...)` will write an ordinary message and `log.error(...)` a problem. Step 6 decides what the lines look like.
- **`QUERY`** and **`TARGET_QUERY`** are written in capitals because they're fixed for the whole script (a Python convention for constants). The query has two bound parameters.
- **`WHERE s.order_date >= :start AND s.order_date < :end`** is a **half-open range**: from the first day of the month, up to but **not including** the first day of the next. It catches every moment of the month and nothing of the next, whatever time of day a date carries. The story at the end of this chapter is about the bug `<=` causes.
- **`pd.Timestamp(month + "-01")`** turns `"2025-12"` into 1 December 2025. **`pd.offsets.MonthBegin(1)`** moves forward to the start of the next month, so the end is 1 January 2026, even across a year boundary.

```python
def load(engine, month):
    """Return the month's order lines, the same month last year, and the month's target (or None)."""
    start, end = month_range(month)
    lines = pd.read_sql(QUERY, engine, params={"start": start, "end": end}, parse_dates=["order_date"])
    last_start, last_end = month_range(f"{start.year - 1}-{start.month:02d}")
    last_year = pd.read_sql(QUERY, engine, params={"start": last_start, "end": last_end})
    target = pd.read_sql(TARGET_QUERY, engine, params={"month": start})
    target_value = float(target["target_revenue"].iloc[0]) if len(target) > 0 else None
    return lines, last_year, target_value


dec_lines, dec_last_year, dec_target = load(engine, "2025-12")
print(dec_lines.shape, dec_last_year.shape, dec_target)
```

```
(7278, 8) (6322, 8) 92400000.0
```

- **`start, end = month_range(month)`** unpacks the two dates the function returns.
- **`f"{start.year - 1}-{start.month:02d}"`** builds last year's month as text, `"2024-12"`; `:02d` pads the month to two digits.
- **`... if len(target) > 0 else None`** gives the target when the table has one for this month, and `None` when it doesn't, so a missing target doesn't crash the report. `float()` turns the NumPy number into a plain Python one.
- The function **returns three things**; the call unpacks them into three names. December 2025 has 7,278 lines, and its target is ₹9,24,00,000.

### Step 2: check before publishing

A report that's wrong but on time does more harm than one that's late. So before it writes anything, the script runs six checks on the data, and it writes nothing unless every one of them passes. Each check gives back three things: its name, whether it passed, and a detail for the log.

```python
def check(lines, last_year, month):
    """Return a list of (name, passed, detail) checks. The report is written only if all pass."""
    if len(lines) == 0:
        return [("rows returned", False, "0 lines")]
    revenue = lines["net_revenue"].sum()
    last = last_year["net_revenue"].sum()
    change = (revenue / last - 1) * 100 if last > 0 else None
    months_found = list(lines["order_date"].dt.strftime("%Y-%m").unique())
    return [
        ("rows returned", True, f"{len(lines):,} lines"),
        ("all dates inside the month", months_found == [month], ", ".join(months_found)),
        ("no missing revenue", bool(lines["net_revenue"].notna().all()), f"{lines['net_revenue'].isna().sum()} missing"),
        ("all quantities positive", bool((lines["quantity"] > 0).all()), f"smallest {lines['quantity'].min()}"),
        ("every line has a customer", bool(lines["customer_id"].notna().all()), f"{lines['customer_id'].nunique():,} customers"),
        ("within 50% of last year", change is not None and abs(change) <= 50,
         "no sales last year" if change is None else f"{change:+.1f}%"),
    ]


for name, ok, detail in check(dec_lines, dec_last_year, "2025-12"):
    print(ok, name, detail)
```

```
True rows returned 7,278 lines
True all dates inside the month 2025-12
True no missing revenue 0 missing
True all quantities positive smallest 5
True every line has a customer 3,240 customers
True within 50% of last year +19.8%
```

- Each check is a **tuple** of three things (Chapter 17, section 17.4): its name, `True` or `False`, and a detail for the log.
- **`if len(lines) == 0: return [...]`** stops early when the month has no data at all. Without it, the later checks would try to find the smallest quantity of nothing, and the script would crash instead of reporting a clean failure.
- **`.dt.strftime("%Y-%m")`** writes each date as `2025-12`, and **`.unique()`** keeps the distinct values; the check passes only if the one month found is the month asked for.
- **`.notna().all()`** is `True` when no value is missing. `.all()` asks "is every value true?"; **`bool(...)`** turns pandas' answer into a plain `True` or `False`.
- **`abs(change) <= 50`** allows a rise or a fall of up to 50% on the same month last year. Riverstone grew 20–34% a month in 2025 (December was up 19.8%), so real growth passes; a month that suddenly doubles or halves doesn't. A big jump doesn't prove the data is wrong, but it's exactly what a date-range bug looks like, so the script stops and a person looks. Choose the band from your own business's history, not from this book.
- **`f"{change:+.1f}%"`** prints the change with its sign, `+19.8%`.

### Step 3: summarize

```python
def summarize(lines, target):
    """Return the headline numbers (a dictionary) and revenue by segment (a table)."""
    revenue = float(lines["net_revenue"].sum())
    orders = int(lines["order_id"].nunique())
    headlines = {
        "Net revenue (₹)": round(revenue, 2),
        "Orders": orders,
        "Customers": int(lines["customer_id"].nunique()),
        "Average order value (₹)": round(revenue / orders, 2),
        "Gross margin (%)": round((1 - float(lines["product_cost"].sum()) / revenue) * 100, 1),
        "Share of target (%)": round(revenue / target * 100, 1) if target else None,
    }
    by_segment = (lines.groupby("segment", as_index=False)
                       .agg(net_revenue=("net_revenue", "sum"), orders=("order_id", "nunique"))
                       .sort_values("net_revenue", ascending=False))
    return headlines, by_segment


dec_headlines, dec_by_segment = summarize(dec_lines, dec_target)
print(dec_headlines)
print(dec_by_segment)
```

```
{'Net revenue (₹)': 87266803.75, 'Orders': 4047, 'Customers': 3240, 'Average order value (₹)': 21563.33, 'Gross margin (%)': 27.6, 'Share of target (%)': 94.4}
       segment   net_revenue  orders
1       Retail 42,213,835.00    2106
2    Wholesale 23,584,620.00     855
0  Hospitality 21,468,348.75    1086
```

- **`headlines`** is a dictionary whose keys are the labels a reader will see. `float()` and `int()` turn pandas' NumPy numbers into plain Python numbers, which print and save cleanly.
- **`... if target else None`**: with no target for the month, the share is `None` rather than a division error.
- December 2025: ₹8,72,66,803.75 from 4,047 orders, 94.4% of target, and the same segment split as Chapter 16's report.

### Step 4: the workbook

```python
def write_excel(path, headlines, by_segment, lines):
    """Write a three-sheet workbook: headlines, revenue by segment, and revenue by product."""
    by_product = (lines.groupby("product_name", as_index=False)["net_revenue"].sum()
                       .sort_values("net_revenue", ascending=False))
    headline_table = pd.DataFrame({"measure": list(headlines), "value": list(headlines.values())})
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        headline_table.to_excel(writer, sheet_name="Headlines", index=False)
        by_segment.to_excel(writer, sheet_name="By segment", index=False)
        by_product.to_excel(writer, sheet_name="By product", index=False)
        money = writer.book.add_format({"num_format": "#,##0.00"})
        writer.sheets["Headlines"].set_column(0, 1, 26)
        for name in ("By segment", "By product"):
            writer.sheets[name].set_column(0, 0, 22)
            writer.sheets[name].set_column(1, 1, 18, money)
    return path


reports = Path("reports")
reports.mkdir(exist_ok=True)
xlsx = write_excel(reports / "riverstone_2025-12.xlsx", dec_headlines, dec_by_segment, dec_lines)
print(pd.ExcelFile(xlsx).sheet_names)
```

```
['Headlines', 'By segment', 'By product']
```

- **`list(headlines)`** is the dictionary's keys and **`list(headlines.values())`** its values: two columns for a small "measure, value" table.
- **`with pd.ExcelWriter(...) as writer:`** is section 18.12's writer in its usual form: the file is saved when the `with` block ends.
- **`reports / "riverstone_2025-12.xlsx"`** joins a folder and a file name with `/`, as `pathlib` does (Chapter 17). **`mkdir(exist_ok=True)`** makes the folder, and doesn't complain if it's already there.
- **`pd.ExcelFile(path).sheet_names`** lists a workbook's sheets without reading them: a quick check that the file is what you meant.

### Step 5: the summary a person reads

```python
def write_markdown(path, month, headlines, by_segment, checks):
    """Write a short Markdown summary that a person can read in an email."""
    out = [f"# Riverstone sales, {month}", "", f"_Generated {datetime.now():%d %b %Y %H:%M}_", "", "## Headlines", ""]
    for name, value in headlines.items():
        shown = "not available" if value is None else f"{value:,}"
        out.append(f"- **{name}:** {shown}")
    out += ["", "## By segment", "", by_segment.to_markdown(index=False, floatfmt=",.2f"), "", "## Checks", ""]
    for name, ok, detail in checks:
        out.append(f"- {'PASS' if ok else 'FAIL'}: {name} ({detail})")
    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8")
    return path


dec_checks = check(dec_lines, dec_last_year, "2025-12")
md = write_markdown(reports / "riverstone_2025-12.md", "2025-12", dec_headlines, dec_by_segment, dec_checks)
print("\n".join([line for line in md.read_text(encoding="utf-8").splitlines() if not line.startswith("_Generated")]))
```

```
# Riverstone sales, 2025-12


## Headlines

- **Net revenue (₹):** 87,266,803.75
- **Orders:** 4,047
- **Customers:** 3,240
- **Average order value (₹):** 21,563.33
- **Gross margin (%):** 27.6
- **Share of target (%):** 94.4

## By segment

| segment     |   net_revenue |   orders |
|:------------|--------------:|---------:|
| Retail      | 42,213,835.00 |     2106 |
| Wholesale   | 23,584,620.00 |      855 |
| Hospitality | 21,468,348.75 |     1086 |

## Checks

- PASS: rows returned (7,278 lines)
- PASS: all dates inside the month (2025-12)
- PASS: no missing revenue (0 missing)
- PASS: all quantities positive (smallest 5)
- PASS: every line has a customer (3,240 customers)
- PASS: within 50% of last year (+19.8%)
```

- **Markdown** is plain text with light marks for formatting: `#` for a heading, `-` for a list item, `**…**` for bold. Email tools, chat tools, and GitHub all display it neatly, and it's still readable as plain text.
- **`out`** collects the lines of the file, starting with a heading and the time stamp. The first loop adds one list line per headline: **`shown`** is "not available" when the value is `None` (a month with no target) and otherwise the number with thousands separators, and **`out.append(...)`** adds the line. **`out += [...]`** adds several lines at once, and the second loop adds one line per check.
- **`"\n".join(out)`** joins the lines with line breaks into one text, which **`write_text`** saves.
- **`datetime.now():%d %b %Y %H:%M`** stamps the time the report was made, using the `strftime` codes of Chapter 17 (section 17.11). (The last line of the cell prints the file back, and its list comprehension leaves out that line, because it changes every run.)
- **`by_segment.to_markdown(index=False, floatfmt=",.2f")`** writes the table as a Markdown table. `to_markdown` borrows a small package, **`tabulate`**, to draw it, which is why it's in the install line; `floatfmt=",.2f"` formats the decimals with separators, so no scientific notation reaches the reader.

### Step 6: `main`, which runs the steps in order

```python
def main(month, out_dir):
    """Run the report for one month. Return 0 if it worked, 1 if a check failed, 2 if it isn't set up."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
    load_dotenv()
    url = os.environ.get("RIVERSTONE_DB")
    if not url:
        log.error("RIVERSTONE_DB is not set")
        return 2
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    engine = create_engine(url)

    log.info("loading %s", month)
    lines, last_year, target = load(engine, month)
    checks = check(lines, last_year, month)
    for name, ok, detail in checks:
        if ok:
            log.info("check passed: %s (%s)", name, detail)
        else:
            log.error("check FAILED: %s (%s)", name, detail)
    if not all([ok for name, ok, detail in checks]):
        log.error("checks failed; no report written")
        return 1

    headlines, by_segment = summarize(lines, target)
    xlsx = write_excel(out / f"riverstone_{month}.xlsx", headlines, by_segment, lines)
    md = write_markdown(out / f"riverstone_{month}.md", month, headlines, by_segment, checks)
    log.info("wrote %s and %s", xlsx.name, md.name)
    print(f"{month}: net revenue {headlines['Net revenue (₹)']:,.2f} from {headlines['Orders']:,} orders")
    return 0


print("exit code:", main("2025-12", "reports"))
```

```
2025-12: net revenue 87,266,803.75 from 4,047 orders
exit code: 0
```

- **`logging.basicConfig(...)`** sets up logging once, for the whole script. **`level=logging.INFO`** shows messages at the INFO level and above; the levels, from lowest to highest, are DEBUG, INFO, WARNING, and ERROR, so turning the level down to DEBUG shows more detail when you're hunting a problem. **`format`** is the pattern of each line: `%(asctime)s` the time, `%(levelname)s` the level, `%(message)s` the message. **`datefmt="%H:%M:%S"`** keeps only the clock time.
- **`log.info("loading %s", month)`** writes a message; logging puts `month` where `%s` is. Logging has its own placeholders instead of f-strings, so the text is only built when the message is actually shown.
- **`os.environ.get("RIVERSTONE_DB")`** returns `None` instead of stopping when the variable isn't set, so the script can log a clear message and return **2**.
- **`mkdir(parents=True, exist_ok=True)`** also creates any missing folders above the output folder.
- **The checks are logged one by one**, as `INFO` when they pass and `ERROR` when they fail, so the log shows exactly which check stopped the run.
- **`all([ok for name, ok, detail in checks])`**: the list comprehension (Chapter 17) collects the `True`/`False` of every check, and **`all(...)`** is `True` only if every one is. If any failed, nothing is written and the function returns **1**.
- The return values are the script's **exit codes** (Chapter 17, section 17.12): 0 for success, and a different non-zero number for each kind of failure, so a scheduler knows whether to alert someone (Chapter 20).
- Log lines go to a separate channel from `print()`, the one programs use for errors and messages, so in the notebook they appear under the cell on a pale red background. The printed summary line and the returned 0 are the output shown here; the log appears in the terminal run below.

### The finished file, run from the terminal

`monthly_report.py` in the companion folder is these pieces in one file. Open it in VS Code. It starts with a docstring and the imports, then the two queries and the six functions exactly as above, and it ends with four lines that make it a command. Here are the beginning and the end, with the middle left out.

<!-- run: none -->
```python
"""Riverstone monthly sales report: database, checks, Excel workbook, Markdown summary.

Usage:  python monthly_report.py 2025-12 [--out reports]
Needs:  RIVERSTONE_DB, a SQLAlchemy database URL, in the environment or in a .env file.
"""
import argparse
import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# ... QUERY, TARGET_QUERY, and the six functions from steps 1 to 6 ...

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Riverstone monthly sales report")
    parser.add_argument("month", help="the month to report, as YYYY-MM")
    parser.add_argument("--out", default="reports", help="the folder to write the files to")
    args = parser.parse_args()
    raise SystemExit(main(args.month, args.out))
```

- The **docstring** at the top says what the script does, how to run it, and what it needs: the first thing a colleague reads.
- **`if __name__ == "__main__":`**, from Chapter 17, runs the last block only when the file is run as a command, so another script can `import monthly_report` and use `summarize()` without running a report.
- **`argparse`** is the standard library's reader for the words typed after a script's name, the `sys.argv` of Chapter 17 with the work done for you. **`argparse.ArgumentParser(description=...)`** makes the reader. **`add_argument("month", help=...)`** declares a required argument, taken by position; **`add_argument("--out", default="reports", help=...)`** declares an optional one, written with two dashes and a value, which is `reports` when left out. **`parser.parse_args()`** reads the command line and returns `args`, with `args.month` and `args.out`. If the month is missing, argparse stops with a usage message; `python monthly_report.py --help` prints the `help` texts.
- **`raise SystemExit(main(...))`** ends the program with `main`'s return value as its exit code.

Run it from the terminal in `work/ch18`, the way a scheduler would:

<!-- run: none -->
```
# terminal
$ python monthly_report.py 2025-12 --out reports
18:44:29 INFO loading 2025-12
18:44:29 INFO check passed: rows returned (7,278 lines)
18:44:29 INFO check passed: all dates inside the month (2025-12)
18:44:29 INFO check passed: no missing revenue (0 missing)
18:44:29 INFO check passed: all quantities positive (smallest 5)
18:44:29 INFO check passed: every line has a customer (3,240 customers)
18:44:29 INFO check passed: within 50% of last year (+19.8%)
18:44:29 INFO wrote riverstone_2025-12.xlsx and riverstone_2025-12.md
2025-12: net revenue 87,266,803.75 from 4,047 orders
```

The lines with times are the log; the last line is the script's own printed summary. Your times will differ. To see the exit code in the terminal, run `echo $?` straight afterwards on macOS or Linux, or `echo $LASTEXITCODE` in Windows PowerShell: it prints `0`.

A program can run the script too, and read its exit code, which is what Chapter 20's scheduler does:

```python
import subprocess, sys

run = subprocess.run([sys.executable, "monthly_report.py", "2025-12", "--out", "reports"],
                     capture_output=True, text=True)
print("exit code:", run.returncode)
print(run.stdout.strip())
print(sorted([p.name for p in Path("reports").glob("riverstone_2025-12.*")]))
```

```
exit code: 0
2025-12: net revenue 87,266,803.75 from 4,047 orders
['riverstone_2025-12.md', 'riverstone_2025-12.xlsx']
```

- The standard library's **`subprocess`** module runs another program, as if you'd typed the command in a terminal. **`subprocess.run([...])`** takes the command as a list of words.
- **`sys.executable`** is the full path of the Python running the notebook, so the script runs in the same environment.
- **`capture_output=True, text=True`** collects what the script prints, as text, in `run.stdout` (and its log in `run.stderr`), instead of letting it scroll past.
- **`run.returncode`** is the script's exit code.
- **`Path("reports").glob("riverstone_2025-12.*")`** finds the files whose names match the wildcard (Chapter 17), and the list comprehension keeps their names.

The script finds `RIVERSTONE_DB` the same way the notebook did, from `.env`, so no password appears anywhere in the code.

What makes it an automation rather than a script that happens to run:

- **Inputs are arguments and environment variables.** The month is on the command line; the database address and password are in the environment. Nothing is specific to your laptop.
- **It checks before it publishes.** Six checks run first, and a failure means no file is written and a non-zero exit code, so the scheduler can alert someone (Chapter 20).
- **It logs what it did**, with timestamps, at a level you can turn up when debugging.
- **It writes both a machine format (Excel) and a human summary (Markdown)**, so the email in Chapter 20 has something to say.
- **Functions are small and testable.** `summarize()` can be run on a DataFrame you build by hand in a test (Chapter 29).

---

## 18.16 Performance, habits, and when to stop using pandas

### Make it faster

```python
narrow = lines[["order_date", "customer_id", "product_id", "quantity", "net_revenue", "status"]].copy()
before = narrow.memory_usage(deep=True).sum() / 1024**2
narrow["status"] = narrow["status"].astype("category")
narrow["customer_id"] = pd.to_numeric(narrow["customer_id"], downcast="integer")
narrow["product_id"] = pd.to_numeric(narrow["product_id"], downcast="integer")
after = narrow.memory_usage(deep=True).sum() / 1024**2
print(f"{before:.1f} MB → {after:.1f} MB")
```

```
11.4 MB → 5.6 MB
```

- **`.memory_usage(deep=True)`** gives each column's memory in bytes, counting the text itself (`deep=True`); `.sum() / 1024**2` turns the total into megabytes.
- **`.astype("category")`** stores a column with few distinct values, such as the four statuses, as small numbers plus one list of the words, instead of the words on every row.
- **`pd.to_numeric(..., downcast="integer")`** stores whole numbers in the smallest integer type that fits them: product IDs up to 108 fit in 8 bits instead of 64.

The habits that matter, roughly in order of payoff:

1. **Read less.** `usecols`, a `WHERE` in the SQL, and Parquet instead of CSV.
2. **Vectorize.** Arithmetic, `.str`, `.dt`, `.map`, `np.where` before `.apply`, and `.apply` before a loop.
3. **Right-size types.** `category` for repeated text, smaller integers, `float32` where precision allows.
4. **Avoid growing a DataFrame in a loop.** Build a list of frames and `pd.concat` once; adding to a table in a loop copies the whole table every time.
5. **Chain, but name the steps.** A pipeline of five clear steps beats a twenty-line expression nobody can debug.
6. **Measure before optimizing:** `%timeit` in a notebook, or `time.perf_counter()` in a script (section 18.1).

### When pandas isn't the answer

| Situation | Better |
|---|---|
| The data is larger than memory | Chunked reading, DuckDB, Polars, or push the work to the database |
| The work is filtering and aggregating a huge table | SQL, where the indexes are |
| Several people need the same numbers | A semantic model (Chapter 16) or a warehouse table (Part 3) |
| The output is a shared dashboard | Power BI, not a script that mails a workbook |
| The pipeline has many steps, dependencies, and schedules | An orchestrator (Chapter 46) |

**DuckDB** deserves a mention: it runs SQL directly over Parquet and CSV files, inside Python, and often replaces a memory-hungry pandas step with a query that reads only the columns it needs. **Polars** is a faster DataFrame library with a similar way of thinking. Both are worth an afternoon once pandas is comfortable, and both make the same point: pandas is a tool, not the whole job.

### Checkpoint: week 4

Run `monthly_report.py` for November 2025 from the terminal. Does every check pass? Open the Markdown file: what share of target did November reach? The answer is at the end of the chapter.

---
## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Looping over rows | Minutes where there should be milliseconds | Arithmetic on whole columns; `.str`, `.dt`, `.map`, `np.where` |
| `.apply()` as the first resort | Slow, and often less readable | Vectorized methods first; `.apply` when there's no alternative |
| Letting `read_csv` guess types | Codes lose leading zeros; dates flip | `dtype=`, `parse_dates=`, `date_format=` |
| Opening the notebook in the wrong folder | `FileNotFoundError` on the first data file | Check `Path.cwd()`; keep the notebook in `work/ch18` |
| Chained assignment (`df[mask]["col"] = …`) | The change silently doesn't happen; a `ChainedAssignmentError` warning | `df.loc[mask, "col"] = …` |
| Forgetting brackets in a condition | `ValueError: The truth value of a Series…` | `(a > 1) & (b < 2)`, never `and`/`or` |
| Comparing with `np.nan` | `x == np.nan` is never true | `.isna()`, `.notna()` |
| Merging without checking | Row count grows; totals inflate | `indicator=True`, `validate=`, compare `len()` before and after |
| Merging on mismatched keys | Everything is NaN, or an error | Check `dtype` on both sides; pad and strip text keys |
| Not knowing which edge a band includes | A value on the boundary lands in the wrong band | `pd.cut(..., right=False)` for "from ₹25,000 is large" |
| `inplace=True` everywhere | Harder to read, and no speed benefit; discouraged, and likely to be deprecated | Assign the result: `df = df.something()` |
| Ignoring the index | Values line up wrongly after a filter | `reset_index(drop=True)` when the labels stop meaning anything |
| `df.append` in a loop | Quadratic slowdown (and it's gone in pandas 2+) | Collect frames in a list, `pd.concat` once |
| Rounding the data to make it look neat | Totals that don't reconcile | Round at presentation; format in Excel |
| Writing a CSV when they wanted a report | "Can you make it look like last month's?" | Formatted Excel (section 18.12) |
| Credentials in the script | A password in Git forever | Environment variables, `.env` outside version control |
| Building SQL with f-strings | Injection, and broken quotes and dates | Bound parameters (`:name`, `params=`) |
| An API call with no timeout or status check | A hung script, or a "successful" run on an error page | `timeout=`, `raise_for_status()` |
| Reading only the first page of an API | Totals that are a fraction of the truth | Loop until the last page; compare with the reported count |
| No checks before publishing | A wrong report, delivered on time | Checks that stop the script (section 18.15) |
| A notebook as the deliverable | Cells out of order, can't be scheduled | A script with arguments, logging, exit codes |
| pandas for everything | A 5 GB CSV, a 16 GB laptop, and an afternoon | Push to SQL, chunk, or use DuckDB/Polars |

---

## In the real world: the report that ran itself

Riverstone's monthly sales pack had a routine. On the second working day, Meera exported four files, pasted them into a workbook, refreshed three pivots, fixed the branch spellings by hand, wrote a summary, and emailed it by lunch. Three to four hours, every month, and twice in the last year the wrong month's export had gone out because the file names differ by one digit.

She rebuilt it as a script over two weeks, in the order this chapter teaches.

**Week one, the boring part.** She moved the extract into one SQL query (Chapter 13), so the four exports became one result, and wrote the cleaning steps in pandas from the mapping tables Chapter 14 had already produced. It took longer than doing the month by hand, which it always does the first time.

**Week two, the useful part.** She added six checks: rows came back, the month's dates are inside the month, no missing revenue, all quantities positive, every line has a customer, and the total is within 50% of the same month last year. Then the Excel writer, a Markdown summary, and logging.

The first automated run failed the last check. The script wrote nothing, logged `check FAILED: within 50% of last year (+61.4%)`, and returned exit code 1. She looked: the query's date filter used `<=` on the end of the month, and December had swept in the first orders of January because of the entry-timestamp column she'd joined on by mistake. Ten minutes to fix, with the half-open range of section 18.15, and the check had caught in one run a class of error that had been possible for years.

The pack now takes **four seconds**, runs at 07:00 on the second working day (Chapter 20 does the scheduling and the email), and has an audit trail: which query, which checks, which files, at what time.

Three things she noticed afterwards:

- **The checks mattered more than the speed.** Time saved was the selling point; correctness was the actual benefit.
- **The script became a place to put decisions.** When Finance asked to exclude internal accounts, that became one line, one comment, and a note in the summary, not a habit in someone's head.
- **Nobody asked for the workbook to look "the same as before".** It looked better, because the formatting was written once and never rushed.

Her own summary of the change: *"I used to produce the report. Now I own it."*

---

## Project: automate Riverstone's monthly report

**Goal:** one command that turns the database into a formatted workbook and a written summary, with checks that stop it when the data is wrong.

### Tools you'll need

- **Python** and the book's virtual environment, as installed in Chapter 17 (section 17.0, which also sets the book's rule on Python versions). This chapter's code was run and checked on **Python 3.14.7** and **3.11.15**, with `pandas` 3.0.6, `numpy` 2.5.3 and 2.4.6, `pyarrow` 25.0.1, `matplotlib` 3.11.2 and 3.10.8, `seaborn` 0.13.2, `openpyxl` 3.1.5, `xlsxwriter` 3.2.9, `tabulate` 0.10.0, `SQLAlchemy` 2.1.1, `psycopg` 3.3.6, `mysql-connector-python` 26.7.0, `requests` 2.34.2 and 2.33.1, and `python-dotenv` 1.2.3, against PostgreSQL 16 and MySQL 8.
- `python -m pip install pandas numpy pyarrow matplotlib seaborn openpyxl xlsxwriter tabulate sqlalchemy "psycopg[binary]" requests python-dotenv` (add `mysql-connector-python` for MySQL), as in section 18.1.
- A database with `riverstone_full` loaded (Chapter 14), or the CSV and Parquet files in `companion/full/`.
- **Companion files (`companion/ch18/`):** `api_demo.py` (the demonstration API of section 18.14), `api_response.json` (a saved page of its reply), `clean_orders_pandas.py` (section 18.10's cleaning as one script), and `monthly_report.py` (section 18.15's finished report). The chapter also reads `companion/full/`, `companion/ch14/orders_q4_2025_export.csv`, `companion/ch15/chart_data/`, `companion/ch16/city_region.csv`, and `companion/ch17/sales_exports/`. For instructors: `build_ch18_files.py` rebuilds `api_response.json`.
- **Worth knowing about:** `ruff` (formatting and linting), `duckdb` and `polars` (section 18.16), and `great-expectations` or plain assertions for data checks (Chapter 47).

**Option A: your own report.** Pick the report you produce most often. Time yourself doing it manually once, then automate it.

**Option B: Riverstone.** Use `riverstone_full` (or the CSV files) and build `monthly_report.py` yourself before opening the companion version.

**Steps**

1. **One query** that returns the month's order lines with the columns the report needs. Filter in SQL, not in pandas.
2. **Checks that must pass:** at least five, including one that compares the total with the same month last year and one that proves the date range is right.
3. **Summarize:** headline numbers (revenue, orders, customers, average order value, gross margin, % of target) and at least three breakdowns (segment, region, product).
4. **One chart** saved as PNG, using a style function that applies Chapter 15's rules.
5. **A formatted workbook:** a headline sheet, a sheet per breakdown, number formats, column widths, a frozen header, and the chart embedded.
6. **A Markdown or HTML summary** with the headlines, the biggest movers versus last month, and the check results.
7. **Make it a proper script:** the month as an argument, the database URL from the environment, logging, exit codes, and small functions.
8. **Prove it:** run it for December 2025 and reconcile the headline against SQL. December 2025 is **₹8,72,66,803.75** from **4,047** orders; the year is **₹1,14,66,41,651.25** from **46,356** orders.

**Stretch goals**

- Add a `--compare 2024-12` option that puts last year's numbers beside this year's.
- Write the output to Parquet as well, so next month's script can compare without re-querying.
- Add a `tests.py` with three tests for `summarize()` using a small DataFrame you build by hand.
- Make the script idempotent: running it twice produces the same files, and never half-writes one.
- Rebuild the five redesigned charts of Chapter 15's project with `style_axes`, so every chart comes out consistent.

---

## Timed challenge: forty minutes with pandas

Use `companion/full/` (Parquet or CSV) and pandas only; no SQL. Answers at the end of the chapter.

- **Level 1:** 2025 net revenue, orders, customers, and average order value, excluding cancelled orders.
- **Level 2:** 2025 revenue by segment, and each segment's share.
- **Level 3:** The three best-selling products of 2025 by revenue.
- **Level 4:** The best and worst month of 2025, with their revenue.
- **Level 5:** 2025 revenue growth over 2024, as a percentage.
- **Level 6:** The median order value per segment in 2025, and the 90th percentile across all orders.
- **Level 7:** The top five customers of 2025 by revenue, with their share of the year.
- **Bonus:** A three-month rolling average of monthly revenue for 2025, and the month where it peaks.

---

## Recap

- **NumPy arrays** do arithmetic on whole columns at once; every array has one dtype; `np.nan` marks a missing number and is never equal to anything; `np.where` and `np.select` are the vectorized `IF` and `IFS`.
- **pandas is a table with verbs.** A DataFrame holds columns (Series); you operate on whole columns, which is faster and clearer than looping.
- **Read deliberately:** `dtype`, `parse_dates`, `encoding`, `usecols`. Parquet for your own intermediate storage, CSV for exchanging with people. Run the notebook from its own folder.
- **Profile first:** `shape`, `dtypes`, `value_counts`, `isna().sum()`, `nunique`, `describe`, `info`.
- **Filter with masks** and brackets; select and change values with `.loc`; never chain an assignment.
- **Create columns** with arithmetic, `.str`, `.dt`, `.map`, `np.where`, and `pd.cut` (know which edge a band includes); keep `.apply` for the cases nothing else covers.
- **`groupby` + named aggregations** is SQL's `GROUP BY`; `unstack` and `axis=1` reshape and total across; `transform` is its window function; `lambda` writes a small function inline.
- **`merge` is a join**: choose `how`, state `validate`, check the row count, use `indicator=True`, and watch for fan-out.
- **`pivot_table` and `melt`** move between wide and long; tools want long, slides want wide.
- **Time series:** a datetime index plus `resample`, `rolling`, and `shift` give monthly totals, moving averages, and year-over-year.
- **Cleaning in pandas** reproduces Chapter 14 exactly: ₹42,35,61,010.50 from the same messy export, in a third tool.
- **Charts** follow Chapter 15's rules through a style function; **Excel** gets formats, widths, frozen panes, and an embedded chart.
- **Databases** through SQLAlchemy with bound parameters and credentials from the environment; do the heavy filtering in SQL.
- **APIs** with `requests`: timeouts, status codes, `raise_for_status()`, paging to the last page, retries with growing waits, tokens from the environment.
- **An automation** is a script with arguments, checks that can stop it, logging, exit codes, and outputs for both machines and people.
- **Know when to stop:** memory limits, SQL, DuckDB, Polars, a BI model, or an orchestrator.

---

## Key terms

NumPy · array · dtype · shape · `np.nan` · `np.where` · `np.select` · `np.inf` · pandas · DataFrame · Series · index · vectorized operation · scientific notation · `read_csv` parameters · Parquet · profiling · `value_counts` · `describe` · `info` · boolean mask · `.loc` · `.iloc` · `query` · chained assignment · `.copy()` · `.str` accessor · `.dt` accessor · `.map` · `validate` · `pd.cut` · `.apply` · `groupby` · named aggregation · quantile · two-level index · `unstack` · `axis` · `lambda` · `assign` · `transform` · `merge` · join type · `indicator` · fan-out · `concat` · `merge_asof` · `pivot_table` · `melt` · wide and long · tidy data · time series · datetime index · `resample` · `rolling` · `shift` · `NaT` · nullable integer (`Int64`) · matplotlib · figure and axes · seaborn · `ExcelWriter` · xlsxwriter · openpyxl · environment variable · `.env` file · connection URL · SQLAlchemy engine · bound parameters · SQL injection · `to_sql` · SQLite · API · status code · `requests` · timeout · `raise_for_status` · paging · rate limit · retry with backoff · `json_normalize` · half-open date range · logging · exit code · Markdown · categorical dtype · downcasting · chunking · DuckDB · Polars

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You reach for a whole-column operation before a loop, and can explain why with a NumPy array.
- [ ] You load CSV, Excel, JSON, Parquet, and SQL results with the types and dates you intended.
- [ ] You profile a new DataFrame in five lines and can state its grain.
- [ ] You filter with masks and `.loc`, and never write chained assignment.
- [ ] You use `groupby` with named aggregations, and `transform` when the result must line up with the rows.
- [ ] You check row counts and match rates on every merge.
- [ ] You move between wide and long with `pivot_table` and `melt` without guessing.
- [ ] You resample, roll, and shift a time series to get year-over-year and moving averages.
- [ ] You can do Chapter 14's cleaning in pandas and reconcile it to the SQL answer.
- [ ] You can apply Chapter 15's chart rules in matplotlib, and your charts come out of a style function.
- [ ] Your Excel files have formats, widths, and a frozen header.
- [ ] Your database code uses bound parameters and credentials from the environment.
- [ ] Your API code has a timeout, checks the status, and reads every page.
- [ ] Your script has arguments, checks, logging, and an exit code, and you'd be comfortable if it ran without you.

---

## Exercises

Use `companion/full/`, `companion/ch14/`, `companion/ch15/`, and `companion/ch17/`, from a notebook in `work/ch18`. Check totals against Chapters 14–16 where they overlap.

### Warm-up

1. Load `orders.parquet` and `order_items.parquet`. How many rows and columns does each have, and what is the grain of each?
2. Add a `net_revenue` column to the merged lines without a loop. What is the total across all three years, including cancelled lines?
3. Which columns of the merged table have missing values, and how many are missing in each? How many customer records have no city?
4. Show the difference between `df["a"]` and `df[["a"]]`, and say when each is what you want.
5. Why does `lines[lines["quantity"] > 50 and lines["status"] == "Delivered"]` fail, and what's the correct form?
6. Explain what `.loc[0:2]` returns compared with `.iloc[0:2]`.
7. Make a NumPy array of the quantities `[5, 40, 35]` and prices `[115, 620, 430]`. Print each line's value and the total, then use `np.where` to label each line "small" or "not small" at ₹10,000.

### Core

8. Excluding cancelled orders, compute 2025 net revenue, orders, customers, and average order value. (They should match Chapter 16: ₹1,14,66,41,651.25, 46,356, 4,599, ₹24,735.56.)
9. Build a year-by-segment table of net revenue with `groupby` and `unstack`. Which segment grew most between 2024 and 2025?
10. Using named aggregation, produce a per-month 2025 table with revenue, orders, lines, and average order value.
11. Merge lines with customers using `indicator=True`. Does the row count change, and what does that tell you?
12. Create a deliberately fanned-out merge with a small duplicate table, and explain the row count.
13. Compute each customer's 2025 revenue and their share of the year with `transform`. What share do the top five hold?
14. Build a `pivot_table` of 2025 revenue by segment (rows) and quarter (columns) with totals, then `melt` it back to long format.
15. Resample 2025 revenue to months, add a three-month rolling average and a year-over-year column, and find October's growth.
16. Using Chapter 17's twelve monthly files, read them all with `pd.concat` in three lines. How many rows, and what is the non-cancelled total?
17. In the messy export, normalize `status` with `.str.strip().str.lower()` after removing the non-data rows. How many distinct values remain?
18. Do Chapter 14's date parsing in pandas for the messy export. How many rows are in each date format, and how many dates need repairing?
19. Convert the messy export's price column and prove, in one line, that every value is one of Riverstone's list prices.
20. Produce the full clean table from the messy export and reconcile the non-cancelled, non-quarantined revenue with Chapter 14's ₹42,35,61,010.50.
21. Draw a monthly revenue line chart for 2025 with a style function, an action title, and a zero baseline; save it as PNG.
22. Draw box plots of 2025 order values by segment with seaborn. What are the three medians?
23. Check Chapter 15's correlation between a customer's number of orders and their revenue, using `companion/ch15/chart_data/customers_2025.csv` and `.corr()`.
24. Write a two-sheet formatted workbook (by region, by month) with number formats, a frozen header, and a title row. Read it back and check the totals.
25. Query the database for 2025 revenue by month with bound parameters, and compare the result with the same calculation done in pandas from Parquet.
26. With the demonstration API running, collect every order line for 1 to 3 December 2025 with `page_size=250`. How many pages and lines, and what is the non-cancelled net revenue?
27. Parse `api_response.json` into a DataFrame with `json_normalize`, add `net_revenue`, and state the total of the non-cancelled lines.
28. Run `monthly_report.py` for January 2026. What does the log say, what is the exit code, and which files are written?

### Stretch

29. Reduce the memory footprint of the merged lines table by at least a third using categoricals and downcast integers. Report before and after.
30. Compute, for each customer, the days between consecutive 2025 orders, using `groupby` and `shift`. Among customers with at least three 2025 orders, which three have the longest average gap?
31. Write `highlight_lines(ax, df, focus)`: it draws every column of a month-by-rep table in light gray and the `focus` column in orange with a direct label. Use it on `companion/ch15/chart_data/rep_month_2025.csv` for two different reps, side by side (Chapter 15's highlight idea).
32. Run your cleaning cells, unchanged, on Chapter 14's second export, `orders_q3_2025_export.csv` in `companion/ch14`. Does anything break? What is the non-cancelled, non-quarantined revenue?
33. Compare your clean Q4 table with Chapter 14's `clean_truth_orders_q4_2025.csv` in `companion/ch14`: merge on `order_item_id` with `indicator=True`, then count, column by column, the lines where the values differ.
34. Write the monthly report script yourself (project step 7) and run it for three months in a loop, checking the exit code each time.
35. Rewrite exercise 9 in DuckDB over the Parquet files and compare the code and the timing.

### Think about it

36. A colleague's pandas script gives a different revenue total from Power BI. What are the five things you'd check, in order?
37. When would you keep a report in Excel or Power BI rather than automating it in Python, even though you could?

---

## Answers

**Checkpoints.** *Week 1:* Water Bottle 1L has the highest margin (39.1%), then Lunch Box Set (36.8%), Stackable Bin (34.5%), Food Container Set (30.6%), Storage Box 10L (30.2%), Storage Box 25L (28.0%), Garden Chair (26.1%), and Industrial Crate (21.4%). In `work`, 11,515 lines of 2025 are "large" or "very large" (`work[(work["year"] == 2025) & work["size_band"].isin(["large", "very large"])]`; 11,033 of them on orders that weren't cancelled). *Week 2:* Storage Box 25L (product 102) grew most, by ₹4,84,98,025.50; the weakest week of 2025 is the one ending Sunday 6 July, with ₹86,21,427.50 (`resample("W")` labels each week by its Sunday). *Week 3:* Retail ₹55,64,36,453.75 from 23,865 orders, Wholesale ₹31,27,28,492.50 from 10,059, Hospitality ₹27,74,76,705.00 from 12,432; read back with `header=2` and the column name you wrote, the total is ₹1,14,66,41,651.25. *Week 4:* every check passes (November is up 22.0% on November 2024), and November reached **98.1%** of its target.

**1.** `orders`: 116,194 rows × 5 columns, grain = one order. `order_items`: 209,006 rows × 6 columns, grain = one order line. Merged: 209,006 rows, still one per line.

**2.** `lines["net_revenue"] = lines["quantity"] * lines["unit_price"] * (1 - lines["discount_pct"] / 100)`; the total including cancelled lines is **₹2,77,76,85,790.75**, of which ₹2,66,34,90,234.75 is not cancelled (Chapter 16).

**3.** Only `sales_rep_id` has missing values in the merged table: **6,213** lines (on 3,414 orders without a rep). `customers["city"].isna().sum()` gives **100** customer records with no city. Everything else is complete, which is itself worth stating in a report.

**4.** `df["a"]` returns a Series (one column, no column header in the output); `df[["a"]]` returns a DataFrame with one column. Use the Series for calculations, the DataFrame when you want to keep working in table form or write it out.

**5.** Python's `and` needs a single True or False, and a Series has many values, so it raises `ValueError: The truth value of a Series is ambiguous`. Correct: `lines[(lines["quantity"] > 50) & (lines["status"] == "Delivered")]`.

**6.** `.loc[0:2]` uses **labels** and includes 2, so three rows (when the index is the default 0, 1, 2, …). `.iloc[0:2]` uses **positions** and excludes 2, so two rows.

**7.** `q = np.array([5, 40, 35])`, `p = np.array([115, 620, 430])`: `q * p` is `[575 24800 15050]`, `(q * p).sum()` is 40425, and `np.where(q * p < 10000, "small", "not small")` gives `['small' 'not small' 'not small']`.

**8.** ₹1,14,66,41,651.25 · 46,356 orders · 4,599 customers · ₹24,735.56 average order value, from 83,444 lines.

**9.** Wholesale, from ₹23,84,57,929 to ₹31,27,28,492.50 (+31.1%), against Retail +25.4% and Hospitality +25.7%.

**10.** Revenue by month (₹): Jan 8,51,95,520.50 · Feb 7,85,82,579 · Mar 10,10,09,066.25 · Apr 9,51,94,709.25 · May 8,72,49,567.50 · Jun 5,19,72,482.75 · Jul 4,00,28,093.25 · Aug 7,18,35,346 · Sep 11,17,01,478.75 · Oct 18,06,20,102.75 · Nov 15,59,85,901.50 · Dec 8,72,66,803.75. Orders run from 3,018 (July) to 4,974 (October), and the average order value from ₹13,263.12 (July) to ₹36,312.85 (October).

**11.** The row count stays at 209,006 and `_merge` is `both` for every row: `customer_id` is unique in the customer table, so the join can't fan out and no line is orphaned.

**12.** With a right-hand table containing `customer_id` 1 twice, every left row for customer 1 appears twice. The count grows because a left join returns one row per **matching pair**, which is Chapter 12's fan-out.

**13.** The top five customers hold about **0.42%** of 2025 revenue: with 4,599 active customers and no dominant account, revenue is spread thin, which is a finding in itself.

**14.** `pd.pivot_table(sales2025, index="segment", columns="quarter", values="net_revenue", aggfunc="sum", margins=True)`, after adding the `quarter` column; then `melt(id_vars="segment")` after dropping the margin row and column. Long format has 12 rows for three segments and four quarters.

**15.** October 2025 was **+22.7%** on October 2024 (₹18,06,20,102.75 against ₹14,72,21,565.50). The three-month rolling average peaks in November 2025.

**16.** `pd.concat([pd.read_csv(p) for p in sorted((COMPANION / "ch17" / "sales_exports").glob("*.csv"))], ignore_index=True)`: **330** rows, non-cancelled total **₹43,35,471.00**, the 24 key accounts of Chapter 17.

**17.** **7**: delivered, pending, shipped, cancelled, dlvd, cxl, canceled. (`data["status"].str.strip().str.lower().nunique()`; on the raw column, before removing the non-data rows, the header text `status` would be an eighth.)

**18.** `99-99-9999` 20,782 · `9999-99-99` 3,210 · `99/99/9999` 1,800 · `99999` 40 (after removing duplicates and non-data rows), and **9** dates need repairing from the entry timestamp.

**19.** After stripping the leading non-digits and commas, every price is one of 115, 290, 380, 430, 620, 750, 1400: the seven products sold in Q4 (no garden chairs in winter). That's the validation rule of Chapter 14, section 14.10, in one line: `set(price.unique()) <= set(products["unit_price"])` is `True`.

**20.** ₹42,35,61,010.50 from 25,832 clean lines with 20 quarantined, exactly as in section 18.10 and Chapter 14.

**21.** Any chart following section 18.11's pattern; the line should peak at 18.06 crore in October, the value axis should start at 0 (`set_ylim(bottom=0)`), and the title should say what the chart shows.

**22.** Wholesale ₹25,762.50 · Retail ₹19,425.00 · Hospitality ₹19,121.88.

**23.** `customers_2025[["orders", "net_revenue"]].corr()` gives **0.916**, the same as Chapter 15's `=CORREL`.

**24.** See section 18.12. The check is `round(read_back["Net Revenue"].sum(), 2) == round(original["net_revenue"].sum(), 2)`: the header row was rewritten in Title Case, so the column in the file is `Net Revenue`.

**25.** Both give the monthly figures in answer 10. Any difference means the SQL and the pandas filter disagree about dates or cancelled orders, which is the first thing to check when two tools disagree.

**26.** **4 pages** (250 + 250 + 250 + 74) and **824** lines; the non-cancelled lines are worth **₹95,31,803.50**. Loop exactly as in section 18.14, with `"from": "2025-12-01", "to": "2025-12-03", "page_size": 250`.

**27.** 100 lines, page 1 of 3 of the reply for 1 December 2025. The non-cancelled lines total **₹12,12,809.50** (₹12,40,709.50 with the cancelled ones).

**28.** The log shows `ERROR check FAILED: rows returned (0 lines)` and `ERROR checks failed; no report written`; the exit code is **1**, and no files are written, because `riverstone_full` has no orders after December 2025. The early return in `check()` is what turns "no data" into a clean failure instead of a crash.

**29.** Converting `status` to a category and downcasting the integer keys cuts the memory of the narrow table from 11.4 MB to 5.6 MB, about half. Report the before and after from `memory_usage(deep=True)`.

**30.** One row per order first, then the gap to the same customer's previous order:

```python
orders_2025 = (sales2025.drop_duplicates("order_id")[["customer_id", "order_id", "order_date"]]
                        .sort_values(["customer_id", "order_date"]))
orders_2025["gap_days"] = (orders_2025["order_date"]
                           - orders_2025.groupby("customer_id")["order_date"].shift()).dt.days
counts = orders_2025.groupby("customer_id")["order_id"].count()
gaps = orders_2025.groupby("customer_id")["gap_days"].mean()
print(gaps[counts[counts >= 3].index].sort_values(ascending=False).head(3))
```

```
customer_id
2642   161.00
4812   155.50
2076   152.50
Name: gap_days, dtype: float64
```

`drop_duplicates("order_id")` keeps one row per order, and sorting by customer and date puts each customer's orders in time order. `groupby("customer_id")["order_date"].shift()` is each order's previous order date for the same customer, so subtracting gives the gap, and `.dt.days` turns it into a number of days. `counts` holds each customer's number of orders, and `gaps[counts[counts >= 3].index]` keeps the customers with at least three. Of those, customers 2642, 4812, and 2076 wait longest between orders, about five months on average.

**31.** The function takes the chart area first, like `style_axes`. Figure 18.4 shows the result:

```python
def highlight_lines(ax, df, focus):
    """Every column of df in light gray, the focus column in orange with a direct label."""
    for col in df.columns:
        if col != focus:
            ax.plot(df.index, df[col] / 1e7, color="#dfe5ec", linewidth=1)
    ax.plot(df.index, df[focus] / 1e7, color="#c0662b", linewidth=2.5)
    ax.text(df.index[-1] + 0.2, df[focus].iloc[-1] / 1e7, focus, color="#c0662b", va="center")
    ax.set_title(f"{focus} vs the team", loc="left", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xticks(range(1, 13))

rep = pd.read_csv(COMPANION / "ch15" / "chart_data" / "rep_month_2025.csv").set_index("month")
fig, (left, right) = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)
highlight_lines(left, rep, "Rahul Mehta")
highlight_lines(right, rep, "Simran Kaur")
left.set_ylabel("₹ crore")
fig.subplots_adjust(wspace=0.4)
fig.savefig("reps_highlight.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(rep.shape, rep[["Rahul Mehta", "Simran Kaur"]].sum().round(0).to_dict())
```

```
(12, 11) {'Rahul Mehta': 167315885.0, 'Simran Kaur': 135665049.0}
```

`plt.subplots(1, 2, ...)` makes one row of two chart areas, unpacked into `left` and `right`; `sharey=True` gives them the same value axis, so the two charts can be compared, and `fig.subplots_adjust(wspace=0.4)` widens the gap between them to make room for the labels. The orange line stands out by color, by thickness, and by its label, so it doesn't depend on color alone.

![Two line charts side by side of monthly 2025 revenue in crore for eleven sales reps. On the left, Rahul Mehta's line is thick and orange, labeled at its right end, and the other ten reps are thin light-gray lines; he is above the rest for most of the year, peaking at about 2.6 crore in October. On the right, Simran Kaur is highlighted the same way, near the top of the group](figures/fig18-4-highlight-lines.svg)

*Figure 18.4 — `highlight_lines` used twice. One rep stands out by color, thickness, and a label; the rest of the team stays visible as context.*

**32.** Nothing breaks: the Q3 export has the same kinds of damage, and every rule still applies. 20,720 clean lines, 7 dates repaired, 16 lines quarantined, no unmapped statuses, and **₹22,34,33,478.00** of non-cancelled revenue once the quarantined lines are set aside. A rule that did break would be one written too narrowly for Q4, such as a fixed list of dates.

**33.** All 25,832 lines match on `order_item_id` (`_merge` is `both` for every line), and every column agrees except `quantity` and `net_revenue`, on exactly **20** lines: the 20 quarantined lines, 14 with a blank quantity and 6 with an extra zero (700 for 70). That's the same 20 rows Chapter 14's SQL comparison found. Compare each column with `(both[col] != both[col + "_truth"]).fillna(True).sum()`; the `fillna(True)` counts a blank on one side as a difference.

**34.** Loop over `["2025-10", "2025-11", "2025-12"]`, call the script with `subprocess.run`, and check `returncode == 0` each time. All three pass. A non-zero code means the checks failed, which is what you want a scheduler to see.

**35.** `duckdb.sql("SELECT ... FROM '../../companion/full/order_items.parquet' ...")` reads only the columns the query needs. The code is SQL you already know from Chapters 12–13, and on this dataset both are fast; the difference shows up when the files are larger than memory.

**36.** In order: (1) the date range and whether it's inclusive at both ends; (2) cancelled or excluded rows; (3) the grain (lines versus orders) and any fan-out in a join; (4) the filters applied in the BI model that aren't in the script (or the reverse); (5) rounding and currency handling. Reconcile on one small slice (one month, one region) rather than comparing totals.

**37.** When the audience needs to explore it themselves (Power BI), when the process is truly one-off, when the numbers must live inside a workbook that other people edit, or when nobody but you could maintain the script. Automation that only one person understands is a risk, not an asset; Chapter 20's handover section says what to write down before it becomes one.

**Timed challenge answers.** Level 1: ₹1,14,66,41,651.25 · 46,356 orders · 4,599 customers · ₹24,735.56. Level 2: Retail ₹55,64,36,453.75 (48.5%) · Wholesale ₹31,27,28,492.50 (27.3%) · Hospitality ₹27,74,76,705.00 (24.2%). Level 3: Storage Box 25L ₹23,11,04,137.50 · Food Container Set ₹21,43,80,655 · Storage Box 10L ₹19,63,81,989. Level 4: best October ₹18,06,20,102.75; worst July ₹4,00,28,093.25. Level 5: **+27.0%** on 2024's ₹90,30,15,475.25. Level 6: medians Wholesale ₹25,762.50 · Retail ₹19,425.00 · Hospitality ₹19,121.88; 90th percentile of all 2025 orders ₹49,550.00. Level 7: about 0.42% of the year between them. Bonus: the three-month rolling average peaks in November 2025, at ₹14,94,35,827.67.

---

## Where this leads

- **Chapter 20, Automating Reports & Delivering Insights:** scheduling this script, HTML email, alerts, failure handling, and handover.
- **Chapters 21 and 22:** statistics with pandas and NumPy, and simulations.
- **Chapter 26, Git:** versioning scripts, and keeping `.env` out of the repository.
- **Chapter 29, Python as Software:** modules, packaging, tests, and type hints once a script becomes a tool.
- **Part 4:** scikit-learn and modelling, all of which start from a DataFrame.
- **Interview preparation:** the Python & pandas Question Bank (Chapter 72) covers `groupby`, `merge`, reshaping, and "make this faster".
