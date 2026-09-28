# Parked: blocks moved out of Chapter 14 (Python and terminal content)

Not a reader-facing file and not built. Approved decision (CLAUDE.md §3, Abhishek 28 Sep): the Python in Ch 14 §14.13 moves to Ch 18, and finding 14.2 moves every other pandas mention in Ch 14 with it; finding 14.1 moves the terminal load commands to Ch 26 §26.0; findings 14.22 and 14.23 move the Python compare script and the rebuild-with-a-new-seed idea out of the reader's path. In the reading order the reader meets Ch 14 before Python (Ch 17–18) and before the terminal (Ch 17 §17.0 minimal, Ch 26 §26.0 full), so none of this can stay in Ch 14.

Every block below is **verbatim** from Ch 14 as it stood before the Part 2 build (commit `bd8a0f2`), labelled with its destination and a one-line note of what it depends on. The destination chapter's agent places it (rewritten only as far as its new home needs) and records that it landed.

Labels: **→ Destination** (still to be placed) · **Landed** (placed in its chapter; kept here for the record).

Shared context for all the Ch 18 blocks: the files are in `companion/ch14/` (`orders_q4_2025_export.csv`, `customers_crm_export.csv`, `clean_truth_orders_q4_2025.csv`, `clean_orders_pandas.py`, which writes `clean_order_lines_pandas.csv` and `dq_order_issues_pandas.csv`). Ch 18 already reads `../ch14/orders_q4_2025_export.csv` in §18.2 and §18.10, so the relative path `../ch14/` is the one to use from `companion/ch18`. The SQL numbers these blocks compare against (25,969 data rows, 137 duplicates, 25,832 lines, 37 logged issues, ₹423,561,010.50) are all in Ch 14 and still true. Rupee amounts in reader text use lakh grouping from the Part 2 build on: ₹42,35,61,010.50.

---

## 1. Old §14.13 "A first look at cleaning in pandas" (the whole section)

**Landed** in Ch 18 §18.10, "Load as text, and profile" (Part 2/3 build).

**→ Ch 18 §18.10 "Cleaning in pandas".** Depends on: pandas `read_csv` with `dtype=str` and `keep_default_na` (Ch 18 §18.2), `.str` methods and `value_counts()` (Ch 18 §18.3–18.5), `duplicated()`/`drop_duplicates()`, `pd.to_numeric`. Finding 14.2 asks Ch 18 to keep the four cells and their outputs and add line-by-line explanations (`dtype=str`, `keep_default_na`, `.str.fullmatch`, `duplicated()`, `value_counts()`, `pd.to_numeric`, `zfill`). The `<!-- py: reset -->` marker and the code run from `companion/ch14`; from `companion/ch18` the file names need `../ch14/`. The outputs were produced with pandas 3.0.2; re-run them in Ch 18's environment. The opening paragraph's "If you're reading in file order and haven't reached them yet, treat this section as a preview" no longer applies.

## 14.13 A first look at cleaning in pandas

Python is taught in its own block: Chapter 17 covers the language from zero and Chapter 18 covers **pandas**, the library for working with tables in Python. If you're reading in file order and haven't reached them yet, treat this section as a preview and come back to it afterwards. This preview shows that the method (load as text, profile, fix, validate, reconcile) is the same in Python, and that a script is as repeatable as a query. The code runs from `companion/ch14`; `clean_orders_pandas.py` holds the complete pipeline.

<!-- py: reset -->
```python
import pandas as pd
raw = pd.read_csv("orders_q4_2025_export.csv", dtype=str, keep_default_na=False)
print(raw.shape)
```

```
(25976, 13)
```

`dtype=str` loads every column as text and `keep_default_na=False` keeps empty fields as empty strings instead of guessing: the staging-table idea in one line. The file has 25,976 rows and 13 columns.

```python
data = raw[raw["order_item_id"].str.fullmatch(r"\d+")]
print(len(data), "data rows;", data.duplicated().sum(), "exact duplicates")
data = data.drop_duplicates()
print(data["order_date"].str.replace(r"\d", "9", regex=True).value_counts())
```

```
25969 data rows; 137 exact duplicates
order_date
99-99-9999    20782
9999-99-99     3210
99/99/9999     1800
99999            40
Name: count, dtype: int64
```

The same seven non-data rows and 137 duplicates as SQL. The pattern counts are smaller than section 14.2's because the duplicates are already gone.

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

Normalizing with `.str.strip().str.lower()` leaves the seven spellings a mapping table must handle.

```python
price = pd.to_numeric(data["unit_price"].str.replace(r"^[^0-9]+", "", regex=True).str.replace(",", ""))
print(price.value_counts().sort_index())
```

```
unit_price
115.0     3606
290.0     5082
380.0     3583
430.0     4985
620.0     3575
750.0     3621
1400.0    1380
Name: count, dtype: int64
```

Every converted price is one of Riverstone's seven list prices for the products sold in Q4 (no garden chairs sell in winter), which is a validation rule passed.

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

`zfill(4)` pads with zeros on the left, like `LPAD`. After padding, every code has four characters.

Run the whole script with `python3 clean_orders_pandas.py`; it prints the same 37 logged issues and ₹423,561,010.50 as SQL, and writes `clean_order_lines_pandas.csv` and `dq_order_issues_pandas.csv`.

> **Tool note.** Tested with Python 3.12 and pandas 3.0.2. pandas 2.x gives the same results; in versions before 2.0, `value_counts()` prints its header differently.

---

## 2. Old §14.3 table "Missing values in each tool": the pandas column

**Landed** in Ch 18 §18.10, "Chapter 14's moves in pandas" (merged with the cleaning-verbs table) (Part 2/3 build).

**→ Ch 18 §18.10, as a recap table** (finding 14.2 (2)). Depends on: `isna`, `replace`, `fillna`, `dropna`, `ffill` (Ch 18). The header said "pandas (section 14.11)", a wrong reference (finding 14.32, moot now). The Excel/Power Query and SQL columns stay in Ch 14.

| Task | Excel / Power Query | SQL | pandas (section 14.11) |
|---|---|---|---|
| Count blanks | `COUNTBLANK`; Power Query **Column quality** | `COUNT(*) FILTER (WHERE col IS NULL OR col = '')` | `df[col].isna().sum()` |
| Placeholders to blank | **Transform → Replace Values** (`N/A` → empty) | `NULLIF(TRIM(col), '')`, or a mapping table | `df[col].replace(["N/A", "-"], None)` |
| Keep and label | `=IF(A2="","(unassigned)",A2)`; **Replace Values** `null` → `(unassigned)` for display | `COALESCE(sales_rep, '(unassigned)')` | `df[col].fillna("(unassigned)")` |
| Remove rows | **Home → Remove Rows → Remove Blank Rows** (whole row blank only); filter a column | `WHERE quantity IS NOT NULL` | `df.dropna(subset=["quantity"])` |
| Fill down (group labels) | **Transform → Fill → Down** | `LAST_VALUE(...) IGNORE NULLS` is limited; use a window with `COUNT` (Chapter 13) | `df[col].ffill()` |

---

## 3. pandas clauses cut from the body of Ch 14

**Landed** in Ch 18 §18.10's table (`drop_duplicates`, `rapidfuzz`, outliers, `zfill`), §18.9 (`tz_convert`), §18.2 (`thousands`/`decimal`) and exercise 33 (the column-by-column comparison) (Part 2/3 build).

**→ Ch 18 §18.10** (each is one clause of a sentence in Ch 14; Ch 14 keeps the rest of the sentence). Depends on: the pandas basics of Ch 18 §18.1–18.9; `rapidfuzz` is a third-party library (install with pip) that Ch 18 would introduce if it keeps the clause.

- Old §14.4 (exact duplicates), end of sentence: "…, or `drop_duplicates()` in pandas."
- Old §14.4 (real fuzzy matching), bullet: - **Excel's Fuzzy Lookup add-in** from Microsoft does the same in older versions; **pandas** users reach for libraries such as `rapidfuzz` (Chapter 18).
  (Ch 14 keeps "Excel's Fuzzy Lookup add-in from Microsoft does the same in older versions".)
- Old §14.6 (methods for spotting outliers), last sentence of the paragraph: "In pandas: `df[df.quantity > 90]`."
- Old §14.7 (time zones), end of sentence: "…; pandas uses `tz_convert("Asia/Kolkata")`." **→ Ch 18 §18.9 (Dates and time series)** fits better.
- Old §14.7 (thousands and decimal separators), end of the Watch out: "…; in pandas, `thousands=","` and `decimal="."` in `read_csv`." **→ Ch 18 §18.2 (Reading data from anywhere)** fits better.
- Old §14.8 (joining messy sources), end of sentence: "…; pandas: `.str.strip().str.zfill(4)`."
- Old §14.10 (reconcile), last sentence of the paragraph after the reconciliation output: "The companion check `checks/ch14_compare_clean.py` goes further and compares every column of every line, including dates, codes, statuses, branches, and reps: zero mismatches, for the PostgreSQL, MySQL, and pandas versions alike."
  Ch 14 now does the full-column comparison in SQL (`companion/ch14/sql/ch14_compare_clean.sql`, `EXCEPT`, 20 rows = the quarantined lines). Finding 14.22: "A pandas comparison can live in Ch 18." `checks/ch14_compare_clean.py` is a build check, not a reader file: if Ch 18 wants a reader version, write it in `companion/ch18/` (a `merge` with `indicator=True`, then one comparison per column).
- Old §14.11 (Google Sheets paragraph): "For a dataset this size, clean in SQL or Python and bring the result into Sheets" (Ch 14 now says "clean in SQL").

---

## 4. Tools and companion lines

**Landed** in Ch 18's Chapter at a glance box and project Tools list, without version numbers (Part 2/3 build).

**→ Ch 18 (its own Tools box and project Tools list).** Depends on nothing; RJ-S3-18 asks for one sentence on the book's Python version in Ch 17 §17.2 and the others to defer to it, so drop the version numbers when placing these.

- Chapter at a glance, **Tools:** "…; Python 3.12 with pandas for section 14.13's preview."
- Chapter at a glance, **You will learn to:** "… do all of it in Excel and Power Query, in SQL (PostgreSQL and MySQL), and in a first look at pandas."
- Project, Tools you'll need: - **Python 3.12** with **pandas 3.0.2** (pandas 2.x works) for section 14.13.
- Project, Tools you'll need, companion files: "`clean_orders_pandas.py`: the pandas pipeline." (the line was: - `companion/ch14/clean_orders.pq`: the Power Query pipeline. `clean_orders_pandas.py`: the pandas pipeline.)
- Project, Tools you'll need: - `checks/ch14_compare_clean.py`: compares your cleaned table with the truth, column by column. (a build script named as a reader file; finding 14.22 deletes it from Ch 14.)

---

## 5. Project and review lines

**Landed** in Ch 18's Check yourself (Part 2/3 build).

**→ Ch 18's project or exercises** (optional; they only make sense next to §18.10). Depends on: §18.10.

- Project step 1: 1. **Load as text** in the tool of your choice: SQL staging tables, Power Query with no type detection, or pandas with `dtype=str`.
- Project step 5: 5. **Reconcile.** For the order export, compare with `riverstone_full` (or `clean_truth_orders_q4_2025.csv`) using `checks/ch14_compare_clean.py`. Explain every remaining difference. (Ch 14 now uses `sql/ch14_compare_clean.sql`.)
- Check yourself: - [ ] You can do the core steps in at least two of Power Query, SQL (PostgreSQL or MySQL), and pandas.
- Exercises intro: Unless an exercise says otherwise, use the staging tables and cleaned tables in `riverstone_full` (PostgreSQL or MySQL), Power Query, or pandas, and the files in `companion/ch14/`.
- Recap and "You've got it" wording: "…in Power Query, SQL, and pandas" (Ch 14 now says "in Power Query and SQL").

---

## 6. Exercise 23 and its answer

**Landed** in Ch 18 as exercise 17 (Part 2/3 build).

**→ Ch 18 exercises (Core).** Depends on: `.str.strip()`, `.str.lower()`, `.nunique()`/`value_counts()` (Ch 18 §18.3–18.5), and the file `../ch14/orders_q4_2025_export.csv` loaded with `dtype=str, keep_default_na=False`. Note that the answer counts distinct values after removing non-data rows (7 values); on the raw column the header text `order_item_id` would be an eighth.

23. In pandas, normalize `status` with `.str.strip().str.lower()`. How many distinct values remain?

**23.** **7**: delivered, pending, shipped, cancelled, dlvd, cxl, canceled.

---

## 7. Stretch goal: rebuild the export with a new seed

**Landed** in Ch 18 as exercise 32, using Ch 14's existing Q3 export instead of a new seed (Part 2/3 build).

**→ Ch 18 exercises (Stretch)** (finding 14.23: "move the rebuild idea to Ch 18's exercises"). Depends on: running a Python script (Ch 17 §17.0), editing a constant in it, and `pandas`/`pyarrow` for `build_ch14_files.py`, which reads `../full/*.parquet`. Ch 14's stretch goal now uses a second pre-built export instead (`companion/ch14/orders_q3_2025_export.csv`, built by `build_ch14_q3_export.py`, seed 20250714).

- Make the pipeline run on a second quarter: change the planted-damage seed in `build_ch14_files.py`, rebuild, and rerun without editing your cleaning code. Whatever breaks is a rule that was too specific.

Tools line that went with it (Ch 14 now lists the build scripts as "for instructors; Python"):

- `companion/ch14/build_ch14_files.py`: rebuilds the exports from the full dataset (seed 20251014).

---

## 8. Loading the exports from the terminal

**→ Ch 26 §26.0 "The terminal in 20 minutes", as an exercise ("now load it from the terminal")** (finding 14.1). Depends on: `cd`, running a program with arguments, the `psql` and `mysql` command-line clients (installed with the servers in Ch 12 §12.3), and for MySQL the `local_infile` setting on both sides. Ch 14 now loads through DBeaver with self-contained scripts (`companion/ch14/sql/ch14_load_postgresql.sql`, `ch14_load_mysql.sql`, INSERT statements, no file paths). The terminal versions that read the CSV files directly are kept at `companion/ch14/sql/terminal/ch14_load_postgresql.sql` and `ch14_load_mysql.sql` (they also load `truth_order_lines`), so the commands below need the path `sql/terminal/…` when placed:

**SQL.** The companion scripts create staging tables where every column is text, then load the CSVs:

```
psql -d riverstone_full -f sql/ch14_load_postgresql.sql
mysql --local-infile=1 -u root -p riverstone_full < sql/ch14_load_mysql.sql
```

Run them from `companion/ch14`. They create `stg_orders_raw` and `stg_customers_raw`, plus four small mapping tables used in section 14.5. The table definition shows the idea:

and from old §14.12 (Running this chapter in MySQL), the loading paragraph:

**Loading.** `LOAD DATA LOCAL INFILE` needs local loading enabled on both sides (`SET GLOBAL local_infile = 1;` on the server, `--local-infile=1` on the client), `LINES TERMINATED BY '\r\n'` for Windows line endings, and `CHARACTER SET utf8mb4` for `₹`. Empty CSV fields load as empty strings, not NULL, so the cleaning uses `NULLIF(col, '')` everywhere.

(Ch 14 §14.13 keeps a shorter version of that paragraph about the empty-string behaviour.)
