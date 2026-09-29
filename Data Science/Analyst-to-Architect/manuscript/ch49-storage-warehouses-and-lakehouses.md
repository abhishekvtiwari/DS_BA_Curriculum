# Chapter 49. Storage, Warehouses & Lakehouses

*Part 5 — Data Engineering, Integration & Scale*

> **Chapter at a glance**
>
> **You will learn to:** say where each kind of data belongs: files, object storage, databases, warehouses, lakes, lakehouses · explain row versus columnar storage, and show the difference in file size, read time, and what a query has to read · read a Parquet file's internals: row groups, column chunks, encodings, compression, statistics · explain ACID properly, and why plain files don't have it · turn a folder of Parquet into a real table with a transaction log, then overwrite one machine's data atomically, travel back to an earlier version, restore it, change the schema safely, and compact small files · choose partition columns and file sizes on purpose · explain how cloud warehouses separate storage from compute, and what actually drives their bills.
>
> **Before you start:** Chapter 12 (transactions: `BEGIN`, `COMMIT`, `ROLLBACK`), Chapter 17 (the virtual environment and Jupyter), Chapter 45 (DuckDB from Python, files and Parquet), Chapter 46 (idempotent writes), Chapter 47 (write–audit–publish), and Chapter 48 (partitions, pruning, and the sensor dataset).
>
> **Time needed:** 14–17 hours of reading and practice, spread over two to three weeks. Plan three sittings: sections 49.0–49.4 (setting up, where data sits, row versus columnar, inside a Parquet file, ACID); section 49.5 (table formats, the longest section); sections 49.6 onwards and the project.
>
> **Tools:** Python in the book's virtual environment with `deltalake` (installed in section 49.0), `duckdb` (Chapter 45), and `pyarrow` and `pandas` (Chapter 18). No Spark, no Java, no cloud account.
>
> **Practice data:** the Chapter 48 sensor archive. The companion script rebuilds one day of it (2025-12-01, 216,000 readings) as CSV, Parquet, and a row-store database table, so the three can be compared directly.

---

## Why this matters

Chapter 48 ended with a story where the engine wasn't the problem: the storage layout was. That's the normal case. Most "we need a bigger cluster" conversations are really "we stored this badly" conversations, and the fix costs a day rather than a monthly bill.

Storage decisions also outlive everything else. A tool can be swapped in a quarter. A format and layout, once a year of data is in it and forty reports read it, is what you live with. Getting it right means understanding four things that this chapter demonstrates rather than asserts: **how columnar files work**, **what ACID actually guarantees**, **what a table format adds to a folder of files**, and **what you're paying for in a warehouse**.

This is also where Part 5's promises land. Chapter 46 needed writes that replace a partition atomically. Chapter 47 needed to publish only after checks pass, and to roll back when something slips through. Both of those are storage features, and this chapter is where you get them.

---

## In plain English

Think about how a warehouse stores stock, which Riverstone's does.

- **Loose boxes on a floor** are files in a folder. Anyone can put one down or take one away. Nothing stops two people leaving half-finished piles.
- **Racking with labelled bays** is partitioning: when someone asks for the October stock, you walk to the October bay instead of searching the floor.
- **A stock register** is a **transaction log**: a written record of what's officially in the warehouse right now, and what changed when. The boxes matter, but the register decides what counts.
- **Never counting a half-finished delivery** is **atomicity**: a delivery is either registered in full or not at all.
- **Two people counting at once and both getting the right answer** is **isolation**.
- **The register surviving a power cut** is **durability**.
- **Being able to say what the stock was last Tuesday** is **time travel**.
- **A thousand tiny parcels instead of twenty pallets** is the small files problem: same goods, far slower to handle.

A **lakehouse** is exactly this: cheap floor space (object storage, section 49.1) plus a stock register (a table format, section 49.5) that makes it behave like a proper warehouse.

---

## 49.0 Setting up

This chapter needs one new library, **`deltalake`**, and the sensor data you generated in Chapter 48.

### Step 1. Your practice folder

Work the way Chapter 48 did. In your file manager, copy the folder `companion/ch49` and paste it inside `work`, so you have `work/ch49` next to `work/ch48`. It holds two files:

| File | What it does |
|---|---|
| `setup_ch49.py` | Rebuilds one day of the Chapter 48 sensor data (2025-12-01) as CSV, Parquet, and SQLite, in a folder called `storage`. |
| `format_test.py` | Saves the same day in five formats and times reading each one back (section 49.2). |

`setup_ch49.py` reads the day from `work/ch48/sensor_readings`, so the Chapter 48 dataset must exist (Chapter 48, section 48.0, step 4). If you deleted it, run `python make_sensor_data.py` in `work/ch48` again: the seed makes it identical.

### Step 2. Install deltalake

Open a terminal (Chapter 26, section 26.0), go to your practice folder, activate the book's virtual environment (Chapter 17), and install:

<!-- run: none -->
```
# terminal
$ cd work/ch49
$ source ../../.venv/bin/activate
$ python -m pip install deltalake==1.6.6
```

- **`source ../../.venv/bin/activate`** activates the environment, two levels up; on Windows PowerShell it's `..\..\.venv\Scripts\Activate.ps1`.
- **`deltalake`** is the Python package for **Delta Lake** tables (section 49.5). It needs no Spark and no Java, unlike Chapter 48.
- `==1.6.6` asks for the exact version used for this chapter's outputs. `duckdb` is already installed from Chapter 45 (this chapter needs version 1.4 or later), and `pyarrow` and `pandas` from Chapter 18.

Add `deltalake` to your `requirements.txt` (Chapter 26). Then check that it imports:

<!-- run: none -->
```
# terminal
$ python -c "import deltalake; print(deltalake.__version__)"
1.6.6
```

### Step 3. The notebook and the first cell

In VS Code, create a notebook `ch49.ipynb` in `work/ch49` and choose the `.venv` kernel (Chapter 17, section 17.0). Its working folder is then `work/ch49`, where `setup_ch49.py` sits, which is what lets the notebook import it. Run each code block in this chapter as its own cell, top to bottom, without restarting the kernel: later cells use names that earlier ones create, such as `con` and `dt`.

```python
import os
import duckdb
from setup_ch49 import build

con = duckdb.connect()
print("ready")
```

```
ready
```

- **`import os`** brings in Python's module for files and folders (Chapter 17), used here to list folders and read file sizes.
- **`from setup_ch49 import build`** imports the function `build` from the companion file `setup_ch49.py`. Python finds the file because it sits in the notebook's working folder.
- **`duckdb.connect()`**, with nothing in the brackets, opens a DuckDB database **in memory**: nothing is saved to a file, and it disappears when the kernel stops. That's all this chapter needs, because every query reads files directly. (Chapter 45 passed a file name, to keep a warehouse.)

Each later cell imports what it needs the first time it needs it.

> **Tool note.** The outputs in this chapter were produced with Python 3.11.15, deltalake 1.6.6, DuckDB 1.5.6, PyArrow 25.0.1, pandas 3.0.6, and SQLite 3.45.1. Newer versions may format a few outputs slightly differently.

---

## 49.1 Where data sits

### Object storage in five sentences

One place in the table below is new in this book, and the rest of the chapter depends on it.

1. **Object storage** is cloud storage for files, organised into **buckets**: a bucket is a named container, such as `riverstone-sensors`.
2. Each file, called an **object**, is stored under a **key**, its full name inside the bucket, such as `sensor/reading_date=2025-12-01/part-0.parquet`. The slashes look like folders, but they're only part of the name.
3. You can put, get, list, and delete whole objects, but you can't change bytes inside one: to edit an object, you write a new one in its place.
4. Every request is a call across the network, so 10,000 tiny objects cost 10,000 calls, and listing a bucket with millions of keys is slow.
5. **Amazon S3**, **Google Cloud Storage** (GCS), and **Azure Blob Storage** are the three big services; Chapter 52 sets one up.

| Place | What it is | Good at | Poor at |
|---|---|---|---|
| **Files on a disk or share** | CSV, Excel, Parquet in folders | Simple, universal, cheap | No transactions, no access control, no schema guarantees |
| **Object storage** (S3, GCS, Azure Blob) | Files (objects) in buckets, addressed by key, in the cloud | Very cheap, endlessly scalable, durable | Objects can't be edited in place; listing is slow; no transactions by itself |
| **Operational database** (PostgreSQL, MySQL) | Row-oriented, transactional (Chapter 12) | Many small reads and writes; running the business | Large scans; analytics over billions of rows |
| **Data warehouse** (Snowflake, BigQuery, Redshift) | Columnar, SQL, managed compute | Analytics at scale; concurrency; governance | Cost if used carelessly; less suited to non-tabular data |
| **Data lake** | Files in object storage, usually Parquet | Cheap, any format, any engine | Without discipline, a swamp: no transactions, no schema, no history |
| **Lakehouse** | A lake plus a table format (Delta, Iceberg, Hudi; section 49.5) | Warehouse behavior on lake storage; many engines | More moving parts to understand |

Riverstone's layout by the end of Part 5 is typical of a mid-sized company: orders and customers in the ERP's PostgreSQL (the system of record), a warehouse for analytics (raw, staging, mart), and the sensor archive as Parquet in object storage, exposed as a lakehouse table so it can be corrected, versioned, and read by whichever engine suits the job.

> **Watch out: "the warehouse" means two things.** In this book, Riverstone's physical warehouse at Bhiwandi Main stores crates; the data warehouse stores tables. The chapter names the physical one explicitly when it means crates.

---

## 49.2 Row versus columnar, measured

The most important storage idea is also the easiest to demonstrate: **how the bytes are arranged decides what a query has to read.**

- **Row-oriented** storage keeps each record's fields together. Reading one whole record is cheap; reading one field of every record means touching everything. Operational databases and CSV are row-oriented.
- **Columnar** storage keeps each column's values together. Reading one column of every record is cheap, and values of the same type sit side by side, so they compress extremely well. Parquet, and every analytics warehouse, is columnar.

![Two blocks of storage. At the top, row oriented: four rows of eight small boxes, one row per reading, with the temperature box of each row highlighted; a key explains the short labels, and a line marked with a cross says a query for average temperature reads every box. Below, columnar: eight separate stripes, one per field with its full name, the temperature stripe highlighted as the only stripe read; a line marked with a tick says the same query reads one stripe. A box on the right lists the sizes of the same 216,000 readings: CSV 14.6 MB, SQLite table 16.3 MB, Parquet 1.3 MB.](figures/fig49-1-row-vs-columnar.svg)

*Figure 49.1 — The same 216,000 readings, two arrangements. The query is the same; the work isn't.*

The companion function `build()` writes one day of sensor readings three ways, into a folder called `storage`, and returns how many readings it wrote:

```python
rows = build()
print(f"{rows:,} readings, one day, 25 machines")
```

```
216,000 readings, one day, 25 machines
```

`build()` reads the day's Parquet file from the Chapter 48 archive with DuckDB, then writes `storage/day.csv` (text, row by row), `storage/day.parquet` (columnar, compressed with Snappy, section 49.3), and `storage/day.sqlite`, a small database file holding one table called `readings`. It deletes and rebuilds the folder on every run, so running the cell twice is safe. Now compare the three files' sizes:

```python
for f in sorted(os.listdir("storage")):
    size_mb = os.path.getsize(os.path.join("storage", f)) / 1e6
    print(f"{f:<12} {size_mb:>7.1f} MB")
```

```
day.csv         14.6 MB
day.parquet      1.3 MB
day.sqlite      16.3 MB
```

- **`os.listdir("storage")`** lists the names of the files in the folder; `sorted()` puts them in alphabetical order.
- **`os.path.getsize(...)`** returns a file's size in bytes, and `os.path.join` builds the path with the right separator for your system. Dividing by **`1e6`** (one million, written in scientific notation) turns bytes into megabytes.
- In the f-string, **`:<12`** pads the name to 12 characters, lined up on the left, and **`:>7.1f`** prints the size right-aligned in 7 characters with one decimal place (Chapter 17).

**Reading it.** Identical data: **14.6 MB as CSV**, **16.3 MB in a row-store database table**, and **1.3 MB as Parquet**. Parquet is about **11 times smaller than the CSV** and **12 times smaller than the row store**, because each column is stored on its own and shrinks on its own: the plant name repeats, the timestamps follow a pattern, and the machine ids come from a set of 25. Section 49.3 shows exactly how.

All three give the same answer, of course. First Parquet and CSV, through DuckDB:

```python
CSV     = "read_csv('storage/day.csv')"
PARQUET = "'storage/day.parquet'"

print("average temperature, from Parquet:",
      con.execute(f"SELECT ROUND(AVG(temperature_c), 2) FROM {PARQUET}").fetchone()[0])
print("average temperature, from CSV    :",
      con.execute(f"SELECT ROUND(AVG(temperature_c), 2) FROM {CSV}").fetchone()[0])
```

```
average temperature, from Parquet: 196.49
average temperature, from CSV    : 196.49
```

- **DuckDB lets you put a file where a table name would go.** For a CSV you call `read_csv('...')`, which reads the file and guesses the column types; for a Parquet file the quoted path alone is enough, because the file carries its own types. That's why `PARQUET` holds a path *inside* single quotes: the single quotes belong to the SQL, the double quotes to Python.
- Keeping each `FROM` clause in a variable means the query text is otherwise identical. The f-string pastes it in, so the first query that actually runs is `SELECT ROUND(AVG(temperature_c), 2) FROM 'storage/day.parquet'`.
- **`.fetchone()[0]`** takes the first row of the result as a tuple, and `[0]` its first value (Chapter 45).

Then the row store. **SQLite** is a small row-oriented database that lives in a single file, with no server (Chapter 12 named it, and Chapter 18 wrote to one through pandas). Python comes with a module, **`sqlite3`**, to talk to it directly. Here it plays the part of an operational database:

```python
import sqlite3

lite = sqlite3.connect("storage/day.sqlite")
avg = lite.execute("SELECT AVG(temperature_c) FROM readings").fetchone()[0]
print("average temperature, from SQLite :", round(avg, 2))
lite.close()
```

```
average temperature, from SQLite : 196.49
```

- **`sqlite3.connect(path)`** opens the database file (and would create it if it didn't exist).
- **`lite.execute(sql)`** runs one SQL statement; `readings` is the table `build()` created. **`fetchone()`** returns the first row as a tuple, and `[0]` takes its first value.
- **`round(avg, 2)`** rounds in Python, because this query doesn't round in SQL. **`lite.close()`** releases the file, so nothing else is blocked from using it.

**What differs is the work underneath.** To average one column, the CSV reader must read and parse every byte of all eight fields; the row store must walk every row; Parquet reads one column chunk and skips the rest, which Chapter 48's `ReadSchema` line made visible in Spark's plans.

### The same test across formats, with timing

Chapter 2 introduced Parquet as column-by-column storage and promised the full measurement. Time the two DuckDB queries first. **Before you run it, predict:** how many times faster will the Parquet read be?

```python
import time

def seconds(sql):
    start = time.perf_counter()
    con.execute(sql).fetchone()
    return time.perf_counter() - start

csv_seconds = seconds(f"SELECT AVG(temperature_c) FROM {CSV}")
parquet_seconds = seconds(f"SELECT AVG(temperature_c) FROM {PARQUET}")
print("Parquet read faster than CSV:", parquet_seconds < csv_seconds)
```

```
Parquet read faster than CSV: True
```

- **`time.perf_counter()`** reads a precise clock, in seconds (Chapter 48). The difference between two readings is how long the code between them took.
- **`seconds(sql)`** is a small function that runs one query and returns how long it took.
- The cell prints a comparison rather than the times, because your times will differ from the book's. Print `csv_seconds / parquet_seconds` to see your ratio: on the book's test machine it was between 7 and 12 on repeated runs, with the CSV read taking about a tenth of a second.

The companion script `format_test.py` does the same for five formats: it saves the day as CSV, as CSV compressed with **gzip** (the usual tool for zipping a single file, the `.gz` you meet on downloads), as JSON with one reading per line, as Excel, and as Parquet, then reads each back with pandas (Chapter 18), timing each read three times and keeping the fastest. On the book's test machine (4 shared processor cores) it printed:

| Format | File size | Time to read everything | Time to read one column |
|---|--:|--:|--:|
| CSV | 14.6 MB | 0.175 s | 0.075 s |
| CSV, compressed with gzip | 1.8 MB | 0.202 s | 0.106 s |
| JSON | 39.8 MB | 0.844 s | — |
| Excel (.xlsx) | 8.5 MB | 12.765 s | — |
| **Parquet** | **1.3 MB** | **0.019 s** | **0.003 s** |

*The 216,000 sensor readings of 2025-12-01 (8 columns), read with pandas 3.0.6. pandas can't read one column of a JSON or Excel file without reading the rest, hence the dashes.*

Exact times depend on the computer, but the pattern holds everywhere. **Parquet was the smallest file, and about nine times faster than CSV to read in full**, and reading one column of it took three thousandths of a second. Excel took about seventy times longer than CSV, because every cell has to be unpacked from zipped XML. JSON was the largest, because it repeats all eight column names on every one of the 216,000 readings. The gzip CSV is small, but it must still be unzipped and parsed in full before anything can be read. Run `python format_test.py` in your practice folder to see your own numbers; it takes a minute or two, most of it spent on Excel.

**When row storage is right.** Fetching one order and its lines by id, writing a new order, updating a status: row storage wins, which is why Riverstone's ERP is PostgreSQL and not a pile of Parquet. The rule of thumb: **row for running the business, columnar for understanding it.**

---

## 49.3 Inside a Parquet file

Parquet isn't only "columnar". Its internal structure is what lets engines skip work, and what makes the file small.

### Two layers of shrinking

Parquet shrinks each column in two steps. Work them by hand first, on eight values.

**Layer 1: encoding** rewrites the values in a shorter form, using what's known about the column.

- **Dictionary encoding.** Eight values of `plant` are all `Bhiwandi Main`. Store the string once in a dictionary, `{0: "Bhiwandi Main"}`, and then a small code per row: `0 0 0 0 0 0 0 0`.
- **Run-length encoding.** Those eight codes are one value repeated, so write them as a run: "8 × 0". Eight machine ids `M-01 M-01 M-01 M-02 M-02 M-02 M-02 M-03` become a dictionary `{0: M-01, 1: M-02, 2: M-03}` and three runs: (3 × 0) (4 × 1) (1 × 2).
- **Bit-packing.** A code only needs as many bits as the dictionary is big: 3 values fit in 2 bits, 25 in 5. Eight true/false values fit in one byte, one bit each.

**Layer 2: a compression codec** then squeezes the encoded bytes further. A **codec** (compressor–decompressor) is a general-purpose method for writing repeated patterns more efficiently, the same idea that zipping a file uses: gzip cut the CSV above from 14.6 MB to 1.8 MB, because columns like `plant` and `line_type` repeat the same few words 216,000 times. Parquet's usual codecs are **Snappy** (fast, and the default in most tools), **zstd** (smaller files, a little more work), and **gzip** (small, but slowest to read). Parquet's codecs are all lossless (Chapter 2): you get back exactly the bytes that went in.

Now read the real file. PyArrow (Chapter 18) can open a Parquet file's **metadata**, the description of the file that Parquet keeps in a **footer** at the end of the file. Reading it touches a few kilobytes, not the data:

```python
import pyarrow.parquet as pq

meta = pq.ParquetFile("storage/day.parquet").metadata
print("rows       :", f"{meta.num_rows:,}")
print("row groups :", meta.num_row_groups)
print("columns    :", meta.num_columns)
```

```
rows       : 216,000
row groups : 2
columns    : 8
```

- **`pq.ParquetFile(path)`** opens the file without reading its data; **`.metadata`** reads the footer.
- **`num_rows`**, **`num_row_groups`**, and **`num_columns`** are three facts from the footer. A **row group** is a horizontal slice of the file: a block of rows stored together.

The file has two row groups. Look at the first:

```python
group = meta.row_group(0)
on_disk = sum(group.column(i).total_compressed_size for i in range(meta.num_columns))
print(f"row group 0 : {group.num_rows:,} rows")
print(f"  before compression: {group.total_byte_size / 1e6:.2f} MB")
print(f"  on disk           : {on_disk / 1e6:.2f} MB")
```

```
row group 0 : 122,880 rows
  before compression: 0.80 MB
  on disk           : 0.69 MB
```

- **`meta.row_group(0)`** picks the first row group (counting from 0, like a Python list).
- **`group.total_byte_size`** is the size of the row group's data **after encoding but before compression**: 0.80 MB.
- **`group.column(i).total_compressed_size`** is the size of column `i` as it sits in the file. `sum(... for i in range(meta.num_columns))` adds it up over all eight columns: **0.69 MB on disk**.
- **122,880** is DuckDB's standard row-group size (it writes groups of that many rows), which is why the day's 216,000 readings made two groups: 122,880 and 93,120.

Now each column of that row group, with the encoding the file used and the size before and after compression:

```python
for i in range(meta.num_columns):
    col = group.column(i)
    before = col.total_uncompressed_size / 1e3
    after = col.total_compressed_size / 1e3
    print(f"{col.path_in_schema:<14} {col.encodings[0]:<17} {before:>6.1f} KB {after:>6.1f} KB")
```

```
machine_id     PLAIN_DICTIONARY     0.2 KB    0.2 KB
plant          PLAIN_DICTIONARY     0.1 KB    0.1 KB
line_type      PLAIN_DICTIONARY     0.1 KB    0.1 KB
reading_ts     PLAIN_DICTIONARY   284.7 KB  209.3 KB
temperature_c  PLAIN_DICTIONARY   238.0 KB  219.4 KB
pressure_bar   PLAIN_DICTIONARY   202.3 KB  193.8 KB
units_made     PLAIN_DICTIONARY    62.0 KB   62.0 KB
scrap_flag     PLAIN               15.4 KB    4.1 KB
```

- **`group.column(i)`** is one **column chunk**: one column's values inside one row group.
- **`col.path_in_schema`** is the column's name. **`col.encodings`** lists the encodings used; `[0]` takes the first. **`total_uncompressed_size`** and **`total_compressed_size`** are the chunk's size before and after the codec, divided by `1e3` to give kilobytes.

**How to read it.**

- **Every column except `scrap_flag` is dictionary encoded** (`PLAIN_DICTIONARY`). `plant` has one value in this row group, so it needs a one-entry dictionary and one long run: 0.1 KB for 122,880 values.
- **`temperature_c` takes 219 KB because it has thousands of different values**: every 0.01 °C between about 170 and 223. The dictionary is big, and each row still needs a 13-bit code into it (the next cell counts them). Few distinct values means a small column; many means a big one.
- **`scrap_flag`** isn't dictionary encoded: 122,880 true/false values are simply bit-packed, 8 to a byte, which is the 15.4 KB. They're almost all false, so Snappy then squeezes the long runs of zero bits down to 4.1 KB.
- **For most columns, the size before and after compression is close.** The encoding did most of the work; the codec adds a little.

Each column chunk also carries **statistics**: its minimum and maximum, and, in files DuckDB writes, a count of distinct values:

```python
for i in range(meta.num_columns):
    stats = group.column(i).statistics
    print(f"{group.column(i).path_in_schema:<14} min={stats.min}  max={stats.max}  "
          f"distinct={stats.distinct_count}")
```

```
machine_id     min=M-01  max=M-15  distinct=15
plant          min=Bhiwandi Main  max=Bhiwandi Main  distinct=1
line_type      min=Blow  max=Injection  distinct=3
reading_ts     min=2025-12-01 00:00:00  max=2025-12-01 23:59:50  distinct=8640
temperature_c  min=169.88  max=223.06  distinct=4729
pressure_bar   min=81.36  max=111.66  distinct=2184
units_made     min=0  max=14  distinct=15
scrap_flag     min=False  max=True  distinct=None
```

- **`.statistics`** holds the chunk's statistics; **`stats.min`**, **`stats.max`**, and **`stats.distinct_count`** are three of them. `None` means the writer didn't record that one.
- The second `print` argument continues on a new line inside the brackets; Python joins the two f-strings into one.

**Reading it.**

- `temperature_c` has **4,729 distinct values** in this row group. Codes for 4,729 values need 13 bits each (12 bits only reach 4,096), and 122,880 × 13 bits is about 200 KB: most of its size.
- The statistics are what make Chapter 48's pushed filters work. A query for readings above 230 °C can skip this row group entirely, because its maximum is 223.06.
- **This file happens to be sorted by machine.** Row group 0 holds M-01 to M-15 only (the last one partly), and row group 1 holds M-15 to M-25. So a query for M-20 skips row group 0 without reading it. If the rows were shuffled, both groups would say `min=M-01 max=M-25`, and nothing could be skipped.

**What this means in practice.**

- **Sort data by the column people filter on** before writing. Statistics only help when values are grouped: if every row group contains machines M-01 to M-25, no row group can ever be skipped by machine.
- **Choose row group size deliberately.** Tiny row groups mean lots of metadata; huge ones mean less skipping. 128 MB per row group is a common target. You set it in rows: in DuckDB, `COPY ... TO 'x.parquet' (FORMAT parquet, ROW_GROUP_SIZE 500000)`; in PyArrow, `pq.write_table(table, 'x.parquet', row_group_size=500_000)`. Rows translate to MB through your row width: here about 6 bytes a reading, so 128 MB is roughly 20 million readings.
- **Pick a codec every engine you use can read.** Snappy is fast and universal, zstd compresses more at some CPU cost, and gzip is slowest to read. Inside Parquet, each column chunk is compressed on its own, so several workers can still read different row groups at once. (A whole-file gzip, such as a `.csv.gz`, is different: one worker must read it from the start, which is one reason Chapter 48's engines prefer Parquet.)

---

## 49.4 ACID, properly

**ACID** is four guarantees, and they matter more the moment two processes touch the same data.

| Letter | Guarantee | What goes wrong without it |
|---|---|---|
| **Atomicity** | A change happens completely or not at all | A job dies after deleting yesterday's files and before writing today's: the day is gone |
| **Consistency** | Every committed change leaves the data obeying its declared rules: types, required columns, keys, checks | A job writes a reading with no `machine_id`, or `units_made = -3`, and nothing stops it |
| **Isolation** | Concurrent readers and writers don't see each other's half-done work | A dashboard runs while a table is being replaced and shows 40% of the numbers |
| **Durability** | Once committed, it survives crashes and restarts | A "successful" write lost on a machine restart |

Chapter 12 showed the first of these with `BEGIN`, `COMMIT`, and `ROLLBACK`: the two open purchase orders vanished inside the transaction and came back after `ROLLBACK`. That was atomicity. PostgreSQL gives you all four by default. On plain files, **you don't have any of them**. A folder of Parquet files has no notion of a commit: `rm` then `write` is two separate acts, and anyone reading in between sees whatever happens to be on disk.

That's exactly the gap Chapter 46 worked around with careful ordering, and Chapter 47 worked around with write–audit–publish. A **table format** closes most of it properly: it gives you atomicity, isolation, and durability, and it enforces the schema, so a write with the wrong columns or types is rejected (section 49.5 shows one). Business rules, such as "units made is never negative", are still Chapter 47's tests.

---

## 49.5 Table formats: a folder of files that behaves like a table

**Delta Lake**, **Apache Iceberg**, and **Apache Hudi** all do the same core thing: they keep a **transaction log** beside the data files that records which files make up the table right now, and what changed in each version. Readers consult the log, not the folder. That single move buys atomicity, isolation, time travel, schema evolution, and safe compaction.

This chapter uses Delta through the `deltalake` package from section 49.0. The ideas transfer directly to Iceberg (a one-page tour closes this section) and Hudi.

![Two columns. On the left, the folder: three ordinary Parquet files, part-0000 (1.25 MB, 216,000 readings), part-0001 (1.25 MB, the same readings with M-07 corrected) and part-0002 (0.11 MB, 8,640 readings of M-01). On the right, the log: four numbered versions, each a JSON file in _delta_log. Version 0 records the schema of 8 columns and adds part-0000. Version 1 removes part-0000 and adds part-0001, the M-07 correction in one atomic commit. Version 2 is a restore: it removes part-0001 and adds part-0000 again. Version 3 records a schema of 9 columns and adds part-0002, an append with a new column, shift. Each version has an arrow to the file it adds. A note says readers follow the log, not the folder, so a commit becomes visible all at once; time travel reads an older version's list, and vacuum deletes files no kept version needs.](figures/fig49-2-transaction-log.svg)

*Figure 49.2 — A table format is a folder of ordinary Parquet plus a log that says which files each version contains. These are the four versions this section builds.*

### Creating a table

A Delta table is written from data held in memory, so first read the day into memory. DuckDB can hand a result over as an **Arrow table**: the in-memory columnar form that DuckDB, pandas, Polars, and `deltalake` all share, so data passes between them without being converted.

```python
day1 = con.execute("SELECT * FROM 'storage/day.parquet'").arrow().read_all()
print(f"{day1.num_rows:,} rows")
print(day1.schema.names)
```

```
216,000 rows
['machine_id', 'plant', 'line_type', 'reading_ts', 'temperature_c', 'pressure_bar', 'units_made', 'scrap_flag']
```

- **`.arrow()`** returns the query's result as a stream of Arrow batches (a *reader*), so a huge result doesn't have to fit in memory at once. **`.read_all()`** collects the whole stream into one Arrow table. (DuckDB versions before 1.4 returned the table directly.)
- **`day1.num_rows`** is the row count, and **`day1.schema.names`** the column names.

Now write it as a Delta table:

```python
import shutil
from deltalake import DeltaTable, write_deltalake

shutil.rmtree("delta_readings", ignore_errors=True)
write_deltalake("delta_readings", day1, mode="overwrite")
for name in sorted(os.listdir("delta_readings")):
    print(name[:10])
```

```
_delta_log
part-00000
```

- **`shutil.rmtree(folder, ignore_errors=True)`** deletes a folder and everything in it; `ignore_errors=True` means "and don't complain if it isn't there". It gives the cell a clean start on every run. (`shutil` comes with Python.)
- **`write_deltalake(path, data, mode=...)`** writes `data` as a Delta table in the folder `path`, creating the folder if needed. **`mode="overwrite"`** means "replace whatever the table holds"; on a folder that doesn't exist yet, it simply creates the table. The other common mode, `"append"`, adds rows.
- The loop prints the first 10 characters of each name in the folder. The data file's full name continues with a random id, like `part-00000-a9ea…-c000.snappy.parquet`, which would differ on your computer.

**Reading it.** The folder holds one ordinary Parquet file and a folder called **`_delta_log`**. Any engine can read the Parquet file; the log is what makes it a table. Open the table and look at it the way readers do:

```python
dt = DeltaTable("delta_readings")
con.register("readings_delta", dt.to_pyarrow_dataset())
print("version    :", dt.version())
print("rows       :", f"{con.execute('SELECT COUNT(*) FROM readings_delta').fetchone()[0]:,}")
print("data files :", len(dt.file_uris()))
```

```
version    : 0
rows       : 216,000
data files : 1
```

- **`DeltaTable(path)`** opens the table by reading its log. **`dt.version()`** is its current version number: a new table starts at 0.
- **`dt.to_pyarrow_dataset()`** describes the files that make up the current version, and **`con.register(name, dataset)`** gives DuckDB a table name for them, so SQL can say `FROM readings_delta`. A registered dataset is a **snapshot** of one version: after every write, open the table again and register it again, as the later cells do.
- **`dt.file_uris()`** lists the data files the current version uses; `len()` counts them.

### What's in the log

The log folder holds one JSON file per version, numbered from `00000000000000000000.json`. Each line of the file is one JSON object, called an **action**. Look at the raw text first:

```python
log_file = "delta_readings/_delta_log/00000000000000000000.json"
with open(log_file, encoding="utf-8") as f:
    lines = f.read().splitlines()
print(len(lines), "actions")
print(lines[1])
```

```
4 actions
{"protocol":{"minReaderVersion":3,"minWriterVersion":7,"readerFeatures":["timestampNtz"],"writerFeatures":["timestampNtz"]}}
```

- **`with open(...) as f`** opens the file and closes it afterwards (Chapter 17); **`f.read().splitlines()`** reads the text and splits it into a list of lines.
- **`lines[1]`** is the second line, printed whole. It's the `protocol` action: which versions of the Delta rules a reader and a writer must understand. `timestampNtz` means the table uses timestamps with no time zone, like `reading_ts`.

The other three lines are longer, and they contain a timestamp and random ids that would differ on your computer. Read the useful part of each with `json.loads` (Chapter 17):

```python
import json

for line in lines:
    action = json.loads(line)
    kind = list(action)[0]
    if kind == "add":
        stats = json.loads(action["add"]["stats"])
        print(f"add       : {action['add']['size'] / 1e6:.2f} MB, {stats['numRecords']:,} records")
    elif kind == "metaData":
        schema = json.loads(action["metaData"]["schemaString"])
        print("metaData  :", len(schema["fields"]), "columns")
    elif kind == "commitInfo":
        print("commitInfo:", action["commitInfo"]["operation"])
    else:
        print("protocol  : reader version", action["protocol"]["minReaderVersion"])
```

```
commitInfo: WRITE
protocol  : reader version 3
metaData  : 8 columns
add       : 1.25 MB, 216,000 records
```

- **`json.loads(line)`** turns one line into a dictionary. Each action's dictionary has a single key, the action's kind, so **`list(action)[0]`** (the dictionary's keys as a list, first item) is that kind.
- Two values are **JSON text stored inside JSON**: the file's statistics (`stats`) and the table's schema (`schemaString`). They are strings, so each needs a second `json.loads` before you can look inside.
- The `if`/`elif` chain prints one line per kind of action.

**Reading it.** Four kinds of action in one commit: `commitInfo` (what operation ran), `protocol` (which reader versions can understand this table), `metaData` (the schema, 8 columns), and one `add` per data file, with its size and row count. A later commit will contain `remove` actions for files that are no longer part of the table. **Nothing is edited in place**; each version is a new log file describing the change.

### An atomic correction

The plant team reports that machine M-07's temperature probe reads 1.5 °C low. That's a correction to one machine's readings, in the middle of a day's data. First, M-07's average as recorded:

```python
before = con.execute("""
    SELECT ROUND(AVG(temperature_c), 2) FROM 'storage/day.parquet'
    WHERE machine_id = 'M-07'""").fetchone()[0]
print("M-07 average before:", before)
```

```
M-07 average before: 196.0
```

Then the corrected rows, M-07's readings with 1.5 °C added:

```python
corrected = con.execute("""
    SELECT * REPLACE (temperature_c + 1.5 AS temperature_c)
    FROM 'storage/day.parquet'
    WHERE machine_id = 'M-07'""").arrow().read_all()
print(f"{corrected.num_rows:,} corrected rows")
```

```
8,640 corrected rows
```

- **`SELECT * REPLACE (expression AS column)`** is DuckDB's shorthand for "all the columns, but with this column swapped for a new expression". Standard SQL would list all eight columns and write `temperature_c + 1.5 AS temperature_c` in the middle.
- 8,640 rows is one machine's day: one reading every 10 seconds.

Now the write that matters:

```python
write_deltalake("delta_readings", corrected, mode="overwrite",
                predicate="machine_id = 'M-07'")
dt = DeltaTable("delta_readings")
print("version now:", dt.version())
```

```
version now: 1
```

- **`predicate="machine_id = 'M-07'"`** turns the overwrite into a partial one: delete the rows that match the predicate, and add the new rows, **in one commit**. Rows for the other 24 machines are kept.
- Reopening the table shows the new version: 1.

Check the result through a fresh snapshot. The M-07 query goes in a variable, because later cells reuse it:

```python
con.register("readings_delta", dt.to_pyarrow_dataset())
m07_avg = """SELECT ROUND(AVG(temperature_c), 2) FROM readings_delta
             WHERE machine_id = 'M-07'"""
print("rows now          :", f"{con.execute('SELECT COUNT(*) FROM readings_delta').fetchone()[0]:,}")
print("M-07 average now  :", con.execute(m07_avg).fetchone()[0])
print("data files        :", len(dt.file_uris()))
```

```
rows now          : 216,000
M-07 average now  : 197.5
data files        : 1
```

**Reading it.** The write replaced only the rows matching `machine_id = 'M-07'`, and the table went from version 0 to version 1. M-07's average moved from 196.0 °C to 197.5 °C, and the table still holds all 216,000 rows. Because the table had a single file, `deltalake` wrote a new file with the other machines' rows plus the corrected ones, and the commit swapped one file for the other. At no point could a reader see a table missing M-07, because the change became visible only when the commit landed. With plain Parquet files, the same correction means deleting and rewriting files, with a window where the data is wrong or missing.

> **Watch out: the log is the table.** Don't add, delete, or "tidy up" Parquet files inside a table's folder by hand. Readers follow the log, so a file you add is invisible and a file you delete makes the table unreadable. Use the table's own API (append, overwrite, delete, optimize, vacuum).

**Two writers at once.** Each writer prepares its data files, then tries to create the next log file, say `00000000000000000002.json`. Only one can create it; the other finds it already exists, re-reads the log, and retries, or fails if the two changes clash (both rewrote M-07, say). This is called **optimistic concurrency**: writers don't lock the table, they check at the moment of committing. Readers are never affected: they see version 1 or version 2, never a mixture. That's isolation. (On object storage, "only one can create it" needs support from the storage service, or a small extra service that hands out locks; each table format's documentation says what it relies on.)

### Time travel

Every version stays readable. Open version 0 by number and compare:

```python
con.register("v0", DeltaTable("delta_readings", version=0).to_pyarrow_dataset())
v0_avg = con.execute("""SELECT ROUND(AVG(temperature_c), 2) FROM v0
                        WHERE machine_id = 'M-07'""").fetchone()[0]
print("version 0, M-07 average:", v0_avg)
print("version 1, M-07 average:", con.execute(m07_avg).fetchone()[0])
for entry in dt.history():
    print("version", entry["version"], "-", entry["operation"], "-",
          entry["operationParameters"].get("predicate", "whole table"))
```

```
version 0, M-07 average: 196.0
version 1, M-07 average: 197.5
version 1 - WRITE - machine_id = 'M-07'
version 0 - WRITE - whole table
```

- **`DeltaTable(path, version=0)`** opens the table as it was at version 0, by reading the log only up to that version.
- **`dt.history()`** returns a list of dictionaries, newest first, one per commit. `operationParameters` holds the write's settings; **`.get("predicate", "whole table")`** returns the predicate, or "whole table" for a write that had none (Chapter 17's `get` with a default).

**Reading it.** Version 0 still shows the original 196.0 °C, and version 1 the corrected 197.5 °C. The history lists both commits and what each one touched. It's also how you answer "what did this report say last Tuesday?"

### Restoring a version

Time travel is what makes Chapter 47's promise of a quick rollback real: if a bad load publishes, you **restore** the previous version instead of rebuilding from source. Suppose the plant team now says the probe was fine after all, and the correction must be undone:

```python
dt.restore(0)
dt = DeltaTable("delta_readings")
con.register("readings_delta", dt.to_pyarrow_dataset())
print("version now      :", dt.version())
print("M-07 average now :", con.execute(m07_avg).fetchone()[0])
```

```
version now      : 2
M-07 average now : 196.0
```

- **`dt.restore(0)`** makes the table's content match version 0 again. Then the cell reopens and re-registers the table, as after every write.
- **The restore is itself a new commit, version 2.** It removes version 1's file and adds version 0's file back. Nothing is erased from the history: versions 0 and 1 can still be read, and the log records that someone restored.

### Vacuum: deleting old files

Old versions cost storage, because their files stay in the folder. **Vacuum** deletes data files that no version inside a **retention window** still needs. The window is 7 days (168 hours) by default in Delta. **`dry_run=True`** lists what vacuum *would* delete, without deleting anything:

```python
print(dt.vacuum(dry_run=True))
```

```
[]
```

Nothing: every file here is minutes old, so all of them are inside the 7-day window. Ask for a one-hour window instead:

```python
dt.vacuum(retention_hours=1, dry_run=True)
```

```
_internal.DeltaError: Generic error: Invalid retention period, minimum retention for vacuum is configured to be greater than 168 hours, got 1 hours
```

**`retention_hours=1`** sets the window to one hour, and `deltalake` refuses. Running vacuum with a short retention destroys your ability to time travel, and can break long-running readers that are still reading older files. The check can be switched off with `enforce_retention_duration=False`, which is exactly the setting to be suspicious of when you see it in someone's code.

### Schema changes

The plant team wants a `shift` column: A before noon, B after. Build one machine's readings with the new column, and append them the way you would any other rows:

```python
import traceback

with_shift = con.execute("""
    SELECT *, CASE WHEN EXTRACT(hour FROM reading_ts) < 12 THEN 'A' ELSE 'B' END AS shift
    FROM 'storage/day.parquet' WHERE machine_id = 'M-01'""").arrow().read_all()
try:
    write_deltalake("delta_readings", with_shift, mode="append")
except Exception:
    print(traceback.format_exc().splitlines()[-1])
```

```
_internal.SchemaMismatchError: Cannot cast schema, number of fields does not match: 9 vs 8
```

- **`CASE WHEN ... THEN 'A' ELSE 'B' END AS shift`** (Chapter 13) makes the new column, and **`EXTRACT(hour FROM reading_ts)`** takes the hour from the timestamp.
- The append is rejected: the data has 9 columns and the table 8. That's the schema enforcement from section 49.4, and it's what you want by default.
- **`try`/`except`** (Chapter 17) catches the error, and **`traceback.format_exc().splitlines()[-1]`** prints just its last line, so the notebook doesn't fill with a long error message.

To grow the schema on purpose, say so:

```python
write_deltalake("delta_readings", with_shift, mode="append", schema_mode="merge")
dt = DeltaTable("delta_readings")
con.register("readings_delta", dt.to_pyarrow_dataset())
print("version:", dt.version())
print("columns:", dt.schema().to_arrow().names)
```

```
version: 3
columns: ['machine_id', 'plant', 'line_type', 'reading_ts', 'temperature_c', 'pressure_bar', 'units_made', 'scrap_flag', 'shift']
```

- **`schema_mode="merge"`** tells the write to add any new columns to the table's schema. **`dt.schema().to_arrow().names`** lists the table's columns.

What do the existing rows hold in the new column?

```python
print(con.execute("SELECT shift, COUNT(*) FROM readings_delta GROUP BY shift ORDER BY shift").fetchall())
```

```
[('A', 4320), ('B', 4320), (None, 216000)]
```

**Reading it.** The 8,640 appended rows have a shift, half A and half B. The 216,000 existing rows have `shift` as NULL (`None` in Python): nothing was rewritten, the table simply knows the old files lack the column. Adding a column is safe. Renaming or removing one, or changing a type, is not: those need a new version of the table's contract with the people reading it (Chapter 47).

### Compaction, and the small files problem

Streaming and frequent appends produce many small files. Every reader then pays for opening each one, which on object storage means a network round trip apiece (section 49.1). Make the problem: 24 appends, one per hour of the day, as an hourly job would.

```python
shutil.rmtree("delta_small", ignore_errors=True)
for hour in range(24):                      # 24 hourly appends
    batch = con.execute(f"""SELECT * FROM 'storage/day.parquet'
                            WHERE EXTRACT(hour FROM reading_ts) = {hour}""").arrow().read_all()
    write_deltalake("delta_small", batch, mode="append")
print("version:", DeltaTable("delta_small").version())
```

```
version: 23
```

- Each pass of the loop selects one hour's readings, 9,000 of them (25 machines × 360), and appends them. The first append creates the table, as version 0, so 24 appends end at version 23.

A small helper reports a table's files. It reads each file's size from the log itself, through **`get_add_actions`**, one row per data file:

```python
import pyarrow as pa

def file_report(path, label):
    dt = DeltaTable(path)
    sizes = pa.table(dt.get_add_actions(flatten=True)).column("size_bytes").to_pylist()
    files = "file" if len(sizes) == 1 else "files"
    print(f"{label}: {len(sizes)} {files}, average {sum(sizes) / len(sizes) / 1e6:.2f} MB, "
          f"total {sum(sizes) / 1e6:.2f} MB")

file_report("delta_small", "before")
```

```
before: 24 files, average 0.06 MB, total 1.41 MB
```

- **`dt.get_add_actions(flatten=True)`** returns the current version's `add` actions as a table, one row per file, with columns such as `path`, `size_bytes`, and `num_records`. **`pa.table(...)`** turns it into a PyArrow table, whose **`.column("size_bytes").to_pylist()`** gives the sizes as a Python list.
- Reading sizes from the log, rather than asking the disk, works the same on Windows, on a Mac, and on object storage, and it's one more example of "the log is the table".
- `files` is a conditional expression (Chapter 17), so one file prints as "1 file".

**Before you run the next cell, predict:** after merging the 24 files into one, will the total be the same 1.41 MB, larger, or smaller?

```python
DeltaTable("delta_small").optimize.compact()
file_report("delta_small", "after ")
con.register("small_delta", DeltaTable("delta_small").to_pyarrow_dataset())
print("rows unchanged:", f"{con.execute('SELECT COUNT(*) FROM small_delta').fetchone()[0]:,}")
print("table version :", DeltaTable("delta_small").version())
```

```
after : 1 file, average 0.82 MB, total 0.82 MB
rows unchanged: 216,000
table version : 24
```

- **`.optimize.compact()`** is **compaction**: it merges small files into larger ones and commits the swap as a new version. (In Spark and SQL engines the same operation is called `OPTIMIZE`.)

**Reading it.** Twenty-four appends left **24 files averaging 0.06 MB** (about 59 KB); compaction merged them into **1 file of 0.82 MB**, and the total shrank from 1.41 MB to 0.82 MB, about 40% less. Two things did that. Each small file carried its own footer, schema, and dictionaries, repeated 24 times. And one large file encodes better: a column like `reading_ts` or `temperature_c` gets one dictionary and long runs across the whole day instead of 24 short ones. The row count is unchanged, and the compaction is itself a new version, so readers switch over atomically. (The merged file's exact size can differ by a kilobyte or two between runs, because compaction may interleave the small files' rows in a slightly different order; that's why the report rounds to 0.01 MB.) What happens if you change the loop to 96 appends, one per 15 minutes? Try it: the files get smaller, and compaction saves more.

Real tables aim for files of **128 MB to 512 MB**. Run compaction as a scheduled maintenance job (Chapter 46), not by hand, and pair it with vacuum to remove the files it replaced.

### Iceberg in one page

Apache Iceberg solves the same problem with a deeper tree of metadata instead of one log folder:

- **Data files** are ordinary Parquet, as in Delta.
- **Manifests** list data files, with each file's partition values and column statistics.
- A **manifest list** names the manifests that make up one **snapshot**, Iceberg's word for a version.
- A **metadata file** (JSON) holds the schema, the partition rules, and the list of snapshots, including which one is current.
- A **catalog** is a small service or database that stores one thing per table: where its current metadata file is. A commit writes new metadata and then swaps the catalog's pointer, and only one writer can win that swap, which is Iceberg's atomic commit. A catalog is the one extra piece Delta doesn't need; in Python, the PyIceberg library can keep one in a local SQLite file.

Two features follow from this design. **Hidden partitioning:** the table records how partitions derive from a column, such as "the day of `reading_ts`", so a query that filters on `reading_ts` is pruned without the person writing it knowing the layout (section 49.6). **Column ids:** every column has a number as well as a name, and data files refer to the number, so renaming a column changes only metadata. (Newer Delta tables can do the same, with a feature called column mapping.) Spark, Trino, Flink, and several cloud warehouses can read and write Iceberg tables.

---

## 49.6 Partitioning and file sizing

Chapter 48 showed partition pruning saving 91 folders out of 92. Choosing the partition column is therefore one of the highest-leverage decisions in a platform.

**Choose the column that most queries filter on.** For events, readings, orders, and logs, that's almost always a **date**. Secondary partitioning (date and plant) helps only if queries regularly filter on both.

**Don't over-partition.** A partition per machine per hour across a year is 219,000 folders, each with a tiny file. Listing them takes longer than reading the data, and every engine slows down. Rules of thumb:

| Guide | Why |
|---|---|
| Aim for partitions of at least a few hundred MB | Small partitions waste more time in overhead than they save in skipping |
| Keep total partitions in the thousands, not millions | Listing and metadata dominate above that |
| Target files of 128–512 MB | Fewer, larger reads; fewer round trips on object storage |
| Sort within files by a common filter column | Lets row-group statistics skip work (section 49.3) |
| Never partition by a high-cardinality id | One folder per customer is the classic disaster |

**Rules of thumb are for big tables.** Riverstone's 25 machines produce about 1.3 MB of Parquet a day, so a whole year is under half a gigabyte. At that size, partition by **month** (or not at all) and let row-group statistics do the rest; switch to daily partitions when a day reaches a few hundred MB.

**If queries don't filter on your partition column, partitioning buys nothing.** That was the Chapter 48 story: an archive partitioned by machine, queried by date.

A Delta table is partitioned when you write it, with **`partition_by`**. The day's file has no date column (in Chapter 48 the date lived in the folder name), so derive one:

```python
by_date = con.execute("""
    SELECT *, CAST(reading_ts AS DATE) AS reading_date
    FROM 'storage/day.parquet'""").arrow().read_all()
shutil.rmtree("delta_by_date", ignore_errors=True)
write_deltalake("delta_by_date", by_date, partition_by=["reading_date"], mode="overwrite")
print(sorted(os.listdir("delta_by_date")))
```

```
['_delta_log', 'reading_date=2025-12-01']
```

- **`CAST(reading_ts AS DATE)`** keeps only the date part of the timestamp, as a new column `reading_date`.
- **`partition_by=["reading_date"]`** writes one folder per distinct value, named `column=value`: the Hive-style naming from Chapter 48, which is what lets engines skip folders (the `PartitionFilters` in Chapter 48's plans). The log records each file's partition value too, so a reader can prune without listing any folders.
- For Riverstone's real archive, you'd use `DATE_TRUNC('month', reading_ts)` instead of `CAST(reading_ts AS DATE)`, which gives one partition per month.

Iceberg's **hidden partitioning** (section 49.5) and Delta's **liquid clustering**, an alternative to fixed partition columns in which the table keeps data clustered by the columns you name and can change them later, both exist because fixed partition columns chosen early are hard to change later.

---

## 49.7 Warehouses: storage and compute, separated

Cloud warehouses (Snowflake, BigQuery, Redshift, Databricks SQL, Microsoft Fabric) share one architectural idea: **storage and compute are separate**. Your tables live in cheap object storage; queries run on **compute**, processors and memory you rent while queries run, often billed by the second, sized independently, and several teams can run at once without fighting for the same machine. It's the same split you used in section 49.2, where DuckDB in your notebook (the compute) read files in a folder (the storage).

That's why a warehouse can be idle at 3 a.m. and cost almost nothing, and why a badly written query at 10 a.m. can cost real money.

| Idea | Snowflake | BigQuery | Redshift |
|---|---|---|---|
| Compute unit | Virtual warehouse (sized XS to 6XL) | Slots (on-demand or reserved) | Cluster or serverless workgroup |
| Data organization | Micro-partitions, automatic | Columnar storage, partitioning and clustering | Sort keys and distribution styles |
| You tune by | Clustering keys, warehouse size, auto-suspend | Partitioning, clustering, avoiding `SELECT *` | Sort/dist keys, vacuum, WLM |
| Typical billing | Per second of compute, per TB stored | Per TB scanned (on-demand) or per slot-hour | Per node-hour or per RPU-second |

The product names and units are here so you recognise them, not to memorise. In plain words:

- **Virtual warehouse** (Snowflake): a named block of compute you start, resize, and stop; nothing to do with a physical warehouse. **Auto-suspend** stops it after a few idle minutes.
- **Slot** (BigQuery): its unit of query compute; think of one slot as one worker.
- **Micro-partitions** (Snowflake): small blocks of columnar data, with min/max statistics like a Parquet row group, made automatically. **Clustering keys** tell it which column to keep sorted, so the statistics can skip blocks (section 49.3).
- **Sort keys** and **distribution styles** (Redshift): which column each table is sorted by, and how rows are spread across the cluster's machines.
- **WLM**, workload management (Redshift): queues that stop one heavy query from starving the rest.
- **Node-hour** and **RPU** (Redshift): a cluster is billed per machine (node) per hour; serverless Redshift is billed in Redshift Processing Units per second instead.

Chapter 65 treats billing models properly. Two habits matter in all of them.

- **Prune before you compute.** Filter on the partitioning or clustering column, select only needed columns, and avoid `SELECT *` on wide tables. On a per-TB-scanned model this is literally the bill.
- **Let compute sleep.** Auto-suspend idle warehouses, and don't leave a large cluster running for a dashboard that refreshes hourly.

---

## 49.8 What it costs

Cloud bills have four parts.

| You pay for | Roughly | Habits that cut it |
|---|---|---|
| **Storage** | Cheap: cents per GB-month | Compress (Parquet), expire old versions, vacuum |
| **Compute** | The main cost | Prune, size compute to the job, auto-suspend, avoid rerunning the same query |
| **Data scanned** | On some services, the whole bill | Partition, cluster, select fewer columns |
| **Data transfer out (egress)** | Small but surprising | Keep processing next to the data; don't export whole tables to laptops |

### A worked estimate for Riverstone

Start from what the chapter measured: 1.3 MB of Parquet for 216,000 readings. Today's archive, 25 machines at one reading every 10 seconds, is tiny. So suppose instead that a plant-wide rollout puts **1,460 sensors** on the lines, each reporting **once a second**:

```python
bytes_per_reading = 1.3e6 / 216_000              # measured in section 49.2
today = 25 * 8_640 * 365                          # readings a year now
rollout_per_day = 1_460 * 86_400                  # 1,460 sensors, one reading a second
year_gb = rollout_per_day * 365 * bytes_per_reading / 1e9

print(f"bytes a reading      : {bytes_per_reading:.1f}")
print(f"today, a year        : {today:,} readings, {today * bytes_per_reading / 1e9:.2f} GB")
print(f"rollout, a day       : {rollout_per_day:,} readings")
print(f"rollout, a year      : {year_gb:.0f} GB")
```

```
bytes a reading      : 6.0
today, a year        : 78,840,000 readings, 0.47 GB
rollout, a day       : 126,144,000 readings
rollout, a year      : 277 GB
```

- **`1.3e6 / 216_000`** is bytes per reading: 1.3 million bytes shared among 216,000 readings. Python lets you write underscores inside a number, as in `216_000`, to make it easier to read.
- 8,640 is a day's readings from one machine (one every 10 seconds), and 86,400 the seconds in a day.
- `year_gb` multiplies readings a day by 365 days and by bytes per reading, then divides by `1e9` (a thousand million) to get gigabytes.

**Reading it.** At about **6 bytes a reading**, today's 25 machines produce 78.8 million readings a year: under half a gigabyte, whose storage costs almost nothing. The rollout produces **126 million readings a day**, which is **277 GB a year**. Now price it. Two list prices, as published in September 2026: **Amazon S3 Standard** storage costs **$0.023 per GB-month** (for the first 50 TB, in AWS's US East region), and **BigQuery**'s on-demand queries cost **$6.25 per TiB scanned**, where a TiB (tebibyte, 2 to the power 40 bytes) is about 1,099.5 GB, with the first TiB each month free.

```python
GB_PER_TIB = 1_099.5
storage_month = year_gb * 0.023                   # dollars a month
week_gb = year_gb / 52
week_scan = week_gb / GB_PER_TIB * 6.25           # dollars a run
year_scan = year_gb / GB_PER_TIB * 6.25

print(f"storage             : ${storage_month:.2f} a month")
print(f"weekly report, 1 wk : {week_gb:.1f} GB scanned, ${week_scan:.3f} a run")
print(f"weekly report, all  : {year_gb:.0f} GB scanned, ${year_scan:.2f} a run")
print(f"ratio               : {year_scan / week_scan:.0f}")
```

```
storage             : $6.37 a month
weekly report, 1 wk : 5.3 GB scanned, $0.030 a run
weekly report, all  : 277 GB scanned, $1.58 a run
ratio               : 52
```

- **`GB_PER_TIB`** holds the conversion, written in capitals because it's a fixed value, not something the code changes. **`storage_month`** is the year's gigabytes times the monthly price per gigabyte. **`week_gb`** is one week's share of the year; dividing it by `GB_PER_TIB` gives tebibytes, and multiplying by 6.25 gives dollars, which is **`week_scan`**. **`year_scan`** does the same for a report that reads the whole year.
- The `print` lines format the dollars with 2 or 3 decimal places (`:.2f`, `:.3f`), and the last line divides one cost by the other.

**Reading it.**

- **Storage:** 277 GB at $0.023 per GB-month is about **$6.37 a month**, roughly ₹530 at ₹83 to the dollar. Storage is almost never the problem.
- **Query cost on a per-TB-scanned service:** the weekly plant report reads one week, 277 GB ÷ 52 ≈ 5.3 GB, which costs about **$0.03 a run**, a few rupees. The same report written to read the whole archive scans 277 GB, about **$1.58 a run**: **52 times** as much, for the same answer. The ratio is simply the ratio of data scanned.
- **The lesson in one line:** you don't optimize a data platform's cost by buying cheaper storage; you optimize it by not reading data you don't need.

> **Simplification note.** Prices, units, and free tiers change and differ by region and provider, and this estimate ignores BigQuery's free first TiB each month. It also assumes a query scans as many bytes as the Parquet files hold; BigQuery actually counts the uncompressed size of the columns a query reads, which can be several times more. Treat these as an illustration of the *shape* of a bill, not as a quote: check your provider's calculator. Chapter 52 adds compute to this estimate, and Chapter 65 (FinOps) covers cost management properly.

---

## 49.9 Choosing a layout

| Situation | Store it as | Why |
|---|---|---|
| The business's live records (orders, customers) | Operational database, row-oriented | Many small reads and writes; ACID by default |
| Analytics tables that people query all day | Warehouse tables, columnar | Managed, concurrent, governed |
| Large event or sensor archives | Parquet in object storage, as a table format | Cheap, any engine, correctable, versioned |
| Data you receive from partners | Raw files, kept as they arrived, plus a typed table | Reprocessing without asking again (Chapter 45) |
| Intermediate results in a pipeline | The warehouse, or Parquet | Rebuildable; don't over-engineer |
| A one-off analysis | A local Parquet file | No platform needed |

For Riverstone, the honest answer is: keep orders in the warehouse (a few hundred thousand rows will never be a problem), and keep sensor readings as a Delta table in object storage, partitioned by month, sorted by machine and time within each file, compacted weekly, with a year's retention for time travel.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| CSV as a storage format for analytics | Slow queries, huge files, type guessing | Parquet, with declared types (49.2) |
| Editing files inside a table's folder | Readers see stale or broken tables | Use the table API; the log is the table (49.5) |
| Treating a file overwrite as atomic | A failed job leaves a day missing or half-written | A table format, or write–audit–publish (49.4–49.5) |
| Never compacting | Reads get slower every week; thousands of tiny files | Scheduled compaction plus vacuum (49.5) |
| Vacuuming with a short retention | Time travel gone; long-running readers fail | Keep a retention window that matches your rollback needs |
| Partitioning by a high-cardinality column | Hundreds of thousands of folders; listing dominates | Partition by date or month; sort within files (49.6) |
| Partitioning by a column nobody filters on | Pruning never happens | Match partitions to the queries (49.6, Ch 48 story) |
| `SELECT *` on wide tables | Big bills on per-TB services | Select what you need |
| Leaving compute running | A bill with nothing to show for it | Auto-suspend; size to the job (49.7) |
| Optimizing storage price instead of scan volume | Savings of rupees while scans cost hundreds | Reduce what's read (49.8) |
| Renaming or dropping columns silently | Downstream reports break | Additive changes; contracts for the rest (49.5, Ch 47) |

---

## In the real world: the table nobody could fix

Riverstone's sensor archive lived as plain Parquet in object storage, one folder per day, written by a nightly job.

One Tuesday the plant team asked for a correction: machine M-07's probe had been reading low for six weeks, and every report using it was wrong. The data engineer wrote a job to rewrite those 42 days with corrected temperatures.

It ran for 20 minutes and then failed, because the machine it ran on was restarted during a deployment. By that time it had deleted the files for 19 days and written replacements for 11 of them.

The archive was now in three states: 11 days corrected, 8 days **missing entirely**, and 23 days uncorrected. The nightly job had already run, so some reports had been built from the half-repaired archive. Nobody could say which reports had used which version, because plain files have no history.

Recovering took two days: restoring the missing days from object storage's own versioning (which happened to be enabled), rebuilding the reports, and a difficult conversation with the plant manager about which of last week's numbers had been right.

The fix afterwards was the content of this chapter. The archive became a Delta table: corrections are one atomic commit, a failed job leaves the table exactly as it was, every version is recorded with its timestamp, and "what did this report see on Tuesday?" is a query rather than a guess. Compaction and vacuum run weekly, with retention set to a year.

Six months later a similar correction was needed for a pressure sensor. It was one statement, it took four minutes, and the only sign anything had happened was a new row in the table's history.

**What made this work.**

- **The failure wasn't unusual;** a deployment restarted a machine. The design assumed that would never happen mid-job.
- **Plain files gave no atomicity and no history,** so neither recovery nor investigation was possible.
- **A transaction log turned a two-day incident into a routine commit.**

---

## Project: turn the sensor archive into a table

**Goal:** convert the Chapter 48 archive into a versioned, correctable table, and prove the properties this chapter claims.

### Tools you'll need

- **Python** in the book's virtual environment, with `deltalake` (section 49.0: `python -m pip install deltalake==1.6.6`), `duckdb` (Chapter 45), and `pyarrow` and `pandas` (Chapter 18). No Spark, no Java, no cloud account.
- **The Chapter 49 companion folder** (`companion/ch49/`): `setup_ch49.py`, which rebuilds one day of the Chapter 48 sensor data as CSV, Parquet, and SQLite, and `format_test.py`, the five-format timing test. Generate the Chapter 48 dataset first.
- **Versions used for the outputs shown:** Python 3.11.15, deltalake 1.6.6, DuckDB 1.5.6, PyArrow 25.0.1, pandas 3.0.6, SQLite 3.45.1, on 29 September 2026. The timings came from a shared test machine with 4 cores.
- **Worth knowing about:** Apache Iceberg (PyIceberg), Apache Hudi, and the warehouse products in section 49.7.

**Option A: Riverstone.** Use the sensor archive: all 92 days, 19,872,000 readings.

**Option B: your own data.** Any Parquet dataset you're allowed to use, with at least a few million rows.

**Steps**

1. **Measure the starting point:** rows, file count, total size, and the time to answer one question.
2. **Create a Delta table** from the archive, partitioned by month (section 49.6: derive a column with `DATE_TRUNC('month', reading_ts)`), and confirm the row count matches.
3. **Correct one machine's readings** for one month with an atomic overwrite, then show the row count is unchanged and the average moved.
4. **Break a write on purpose** (raise an exception between two writes) and show the table is still at the previous version and fully readable.
5. **Time travel:** answer the same question at the version before the correction and after it. Then restore the earlier version and show the history.
6. **Make small files:** append 50 small batches, measure the file count and average size, compact, and measure again, including query time before and after.
7. **Add a column** with `schema_mode="merge"` and show old rows get NULLs.
8. **Write a retention policy:** how long you keep old versions, when vacuum runs, and what would be lost if it ran with a one-hour retention. Show a `dry_run` of your vacuum.
9. **Estimate the monthly cost** of your table at ten times its current size, using your provider's published prices, for storage and for one weekly query, partitioned and unpartitioned.

**Stretch goals**

- Repeat step 6 with an Iceberg table via PyIceberg and compare the workflow.
- Sort each month's data by `machine_id` before writing, and measure whether queries filtering by machine get faster (check the row group statistics, section 49.3).
- Add the Chapter 47 tests to run before each commit, so a failing correction never becomes a version.

---

## Recap

- **Object storage** keeps whole files (objects) under keys in buckets: cheap and durable, but no edits in place and a network call per request.
- **Row storage** suits running the business; **columnar** suits analyzing it. The same day of readings is 14.6 MB as CSV, 16.3 MB in a row store, and **1.3 MB as Parquet**, and reading it in full was about nine times faster than CSV.
- Parquet shrinks each column twice: **encoding** (dictionary, run-length, bit-packing) and then a **compression codec** (Snappy, zstd, gzip). Its **row groups**, **column chunks**, and **statistics** let engines skip work; sort by the column people filter on so the statistics can help.
- **ACID** means atomicity, consistency, isolation, durability. Plain files in a folder have none of them.
- A **table format** (Delta, Iceberg, Hudi) adds a **transaction log** that lists the files making up each version. The log is the table: never edit files inside it by hand.
- Table formats give **atomic partial overwrites**, **time travel** and **restore**, **schema enforcement and evolution**, and **compaction**. A correction to one machine moved its average from 196.0 °C to 197.5 °C as a single new version, and a restore put it back as another.
- **Compaction** turned 24 hourly files averaging 0.06 MB into 1 file of 0.82 MB with the same rows, 40% smaller in total; target 128–512 MB files.
- **Partition by what queries filter on** (usually a date), at a grain that gives partitions of a few hundred MB: for Riverstone, a month. Never partition by a high-cardinality id.
- Warehouses **separate storage from compute**; bills are driven by compute time and data scanned, not by storage price.
- The cheapest optimization is **not reading data you don't need**: a weekly report that scans a week instead of a year costs 52 times less.

---

## Key terms

row-oriented storage · columnar storage · Parquet · footer (metadata) · row group · column chunk · encoding · dictionary encoding · run-length encoding · bit-packing · compression codec (Snappy, zstd, gzip) · statistics (min/max, distinct count) · ACID (atomicity, consistency, isolation, durability) · schema enforcement · transaction log · action (add, remove, metaData, protocol, commitInfo) · commit · version · table format · Delta Lake · Apache Iceberg · Apache Hudi · Arrow table · predicate overwrite · optimistic concurrency · time travel · restore · vacuum · retention · dry run · schema evolution · schema merge · compaction (OPTIMIZE) · small files problem · manifest · snapshot · catalog · partitioning · over-partitioning · hidden partitioning · liquid clustering · object storage · bucket · key (object storage) · data lake · lakehouse · separation of storage and compute · compute · data scanned · egress

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can name six places data can sit and say what each is good and bad at, including what a bucket and a key are.
- [ ] You can explain row versus columnar storage, and quote a real size and speed comparison.
- [ ] You can work dictionary encoding, run-length encoding, and bit-packing by hand, and say what a codec adds.
- [ ] You can read Parquet metadata: row groups, column chunks, encodings, statistics, compressed and uncompressed sizes.
- [ ] You can explain each letter of ACID and what goes wrong without it on plain files.
- [ ] You can create a table format table, read its log, and say what `add`, `remove`, and `metaData` mean.
- [ ] You can correct part of a table atomically, and explain what a reader sees during the change and what happens when two writers commit at once.
- [ ] You can use time travel to answer "what did it say before?", restore a version, and say what vacuum would destroy.
- [ ] You can add a column safely and explain why renaming one isn't safe.
- [ ] You can explain the small files problem and fix it with compaction.
- [ ] You can choose a partition column, a partition grain, and a file size, and defend all three.
- [ ] You can explain how warehouses separate storage from compute and what drives the bill.
- [ ] You can estimate a monthly cost and show why scan volume matters more than storage price.

---

## Exercises

### Warm-up

1. For each, say whether row or columnar storage fits better, and why: (a) fetching one order and its lines by id; (b) the average temperature by machine for a year; (c) inserting a new order; (d) counting scrap readings per plant per month.
2. Using the sizes in section 49.2, how many times smaller is the Parquet file than the CSV, and than the SQLite table? Give both to one decimal place.
3. Name the four ACID properties, and for each give one thing that can go wrong on plain files in a folder.

### Core

4. From the row-group output in section 49.3, explain why `plant` takes 0.1 KB while `temperature_c` takes 219.4 KB for the same number of values. What would happen to `machine_id`'s size if machine ids were random 36-character identifiers instead of M-01 to M-25?
5. A query asks for readings above 230 °C. Using the statistics shown in section 49.3, explain what the engine does with row group 0, and what it would have to do if the file had no statistics.
6. In section 49.5's correction, the table stayed at 216,000 rows and moved to version 1. Describe precisely what a reader querying the table halfway through that write would see, and why.
7. After compaction, the 24 hourly files (1.41 MB in total) became one file of 0.82 MB with the same rows. Give two reasons the total shrank, and say which rows of section 49.3's column output you'd expect to shrink most.
8. Riverstone keeps 30 days of time travel. Someone runs vacuum with a retention of 1 hour to free space. List three things that break, and say what you'd have done instead.
9. Using the cost estimate in section 49.8, calculate the monthly cost of scanning the full year (277 GB) once a day for 30 days at $6.25 per TiB (1,099.5 GB), and compare it with scanning one week's data daily. Ignore the free tier. State the ratio.

### Stretch

10. Design the storage for Riverstone's sensor archive at 40 machines and five years, one reading every 10 seconds: partition columns, sort order within files, target file size, compaction and vacuum schedule, and retention. Justify each choice with numbers, and say what you'd change if most queries were per-machine rather than per-period.
11. The plant team wants to correct six weeks of readings for one machine, as in the real-world story. Write the sequence of steps you'd follow with a table format, including what you'd test before committing (Chapter 47) and how you'd let people know.
12. Using section 49.5, including "Iceberg in one page", compare Delta and Iceberg for a company whose data is read by Spark and by a cloud warehouse, on: what extra pieces each needs, how each partitions, how each handles renaming a column, and how each commits. Say which you'd choose for Riverstone and why the answer might differ for a larger company.

### Think about it (no code needed)

13. "The log is the table." Explain what that sentence means to a colleague who has been tidying up Parquet files in a table folder to save space, and what they should do instead.
14. Storage is cheap and compute is expensive, yet most teams spend their optimization effort on compression settings. Why does that happen, and what would you measure first instead?

---

## Answers

**1.** (a) **Row**: all the fields of one record sit together, so it's one read. (b) **Columnar**: one column across many rows, and it compresses well. (c) **Row**: inserting a whole record touches one place; columnar formats are written in bulk, not row by row. (d) **Columnar**: two columns (plant, scrap flag) over many rows, with date pruning.

**2.** 14.6 ÷ 1.3 = **11.2 times** smaller than the CSV. 16.3 ÷ 1.3 = **12.5 times** smaller than the SQLite table. (Exact ratios depend on rounding of the printed sizes; anything close is right.)

**3.** **Atomicity:** a job dies between deleting old files and writing new ones, leaving the day missing. **Consistency:** nothing checks what's written, so a file with a missing `machine_id` or a negative `units_made` is accepted like any other. **Isolation:** a dashboard queries the folder while files are being replaced and averages a mixture of old and new. **Durability:** a write reported as finished is lost when the machine restarts before the data is flushed.

**4.** `plant` has only one distinct value in that row group ("Bhiwandi Main"), so **dictionary encoding** stores the value once, and **run-length encoding** turns 122,880 identical codes into a single run. `temperature_c` has 4,729 distinct values (every 0.01 °C between about 170 and 223), so the dictionary is large and every row still needs its own 13-bit code, about 200 KB; Snappy can't squeeze that much further. If machine ids were random 36-character identifiers, `machine_id` would grow dramatically: tens of thousands of distinct values, so a huge dictionary and long codes, and no runs to fold away. It could easily become the largest column in the file.

**5.** Row group 0's statistics say `temperature_c` has a maximum of 223.06, which is below 230, so **no row in that row group can match**: the engine skips the whole row group without reading its column chunks. Without statistics, the engine would have to read and decompress the temperature column for every row group and test each value, which is the difference between reading kilobytes of metadata and megabytes of data.

**6.** A reader sees **version 0, complete and consistent**, until the commit lands, and **version 1, complete and consistent**, afterwards. It never sees a mixture. That's because a reader resolves the table by reading the log: until the new log file is written, the old entry defines the table, and the new data file sitting in the folder is simply not part of it yet. The commit is a single atomic act of adding one log file.

**7.** (1) **Less per-file overhead:** each of the 24 files carried its own footer, schema, and statistics; one file carries them once. Measured with section 49.3's metadata code, the footers alone fell from 45 KB to 2 KB. (2) **Better encoding across more rows:** in one file, a column gets one dictionary for the whole day, instead of 24 dictionaries rebuilt every hour with mostly the same values in them. So the columns with thousands of distinct values shrink most: `temperature_c` fell from 692 KB across the 24 files to about 364 KB, and `pressure_bar` from 453 KB to about 316 KB. Columns such as `plant`, with one value, were tiny either way.

**8.** Breaks: (1) **Time travel beyond one hour is gone**, so a rollback after a bad publish is impossible; (2) **long-running readers fail**, because files they're still reading are deleted underneath them; (3) **audits and "what did the report say last week?" questions can't be answered**, and any consumer pinned to an older version breaks. `deltalake` refuses such a vacuum by default (section 49.5); getting past it takes `enforce_retention_duration=False`, a deliberate act. Better: keep retention at least as long as your rollback need (30 days here), run vacuum on a schedule with that retention, and if space is genuinely the issue, compact first and check what the old versions actually cost, which is usually small compared with the risk.

**9.** Full year daily: 277 GB ÷ 1,099.5 = 0.252 TiB × $6.25 = **$1.58 a run**, × 30 = **$47.26 a month**. One week's data daily: 5.3 GB ÷ 1,099.5 × $6.25 ≈ **$0.03 a run**, × 30 ≈ **$0.91 a month**. The ratio is **52 times**, which is exactly the ratio of data scanned (52 weeks in a year). The point: the query's cost is set by how much it reads, and partitioning is what decides that.

**10.** Size first: 40 machines × 8,640 readings × about 6 bytes is about **2.1 MB a day**, 62 MB a month, and 3.8 GB over five years. A defensible design: **partition by month** (60 partitions over five years), because reports are time-based and a day is far too small to be a partition; **sort by `machine_id`, then `reading_ts`** within each month's files, so row-group statistics can skip machines; **one file per month** after compaction (62 MB is below the usual 128–512 MB target, which is fine: the target is a ceiling on the number of files, and one file per partition is already the minimum); **compact weekly**, because daily appends leave small files in the current month; **vacuum weekly with a retention of 30 days**; **retain** raw data for five years in the table, with cold storage for older years if costs justify it. If most queries were per-machine rather than per-period, the cleanest answer is *still* to partition by month but sort primarily by machine (so statistics prune machines), or to use Iceberg's hidden partitioning or Delta's liquid clustering to cluster by both; partitioning by machine directly would create 40 partitions a month, 2,400 over five years, each holding about 1.6 MB a month.

**11.** A sensible sequence: (1) **Reproduce the problem**: confirm the probe offset with the plant team and agree the exact machine, date range, and correction. (2) **Build the corrected data into a staging table**, not the live one. (3) **Test it** (Chapter 47): row counts match the original range, the correction moved values by the expected amount and no other machine changed, and reconciliation against the source still holds. (4) **Commit one atomic overwrite** restricted to that machine and date range, and note the version number. (5) **Verify** by querying both versions (time travel) and comparing; if something is wrong, **restore** the earlier version. (6) **Rebuild the affected reports** for the six weeks (Chapter 46's backfill, without re-sending the daily emails), and (7) **tell the people who used the old numbers** which reports changed, by how much, and that a corrected version is available: a labeled correction, exactly as in Chapter 46's story.

**12.** **Extra pieces:** Delta needs only the folder and its `_delta_log`; Iceberg also needs a **catalog** that points at each table's current metadata file. **Partitioning:** Iceberg has **hidden partitioning**, so the table knows how partitions derive from a column and queries filter on the column itself; Delta uses partition columns you write (section 49.6) or, as an alternative, liquid clustering. **Renaming a column:** Iceberg identifies columns by **id**, so a rename changes only metadata; newer Delta tables can do the same with column mapping. **Committing:** Delta writes the next numbered log file, and only one writer can create it; Iceberg swaps the catalog's pointer to new metadata, and only one writer can win the swap. For Riverstone: **Delta**, because the team already uses Python and Spark, `deltalake` needs no extra services, and the tables are read mostly by DuckDB and Spark. For a larger company whose data is read by several engines and warehouses, **Iceberg** is often the safer bet, because a shared catalog lets every engine find the same tables and no single engine is the centre of gravity. Check each engine's current documentation before deciding: support for both formats keeps changing.

**13.** It means the folder of Parquet files isn't the table; the log is, and the log lists exactly which files belong to which version. Deleting a file the log still references doesn't save space in any useful sense: it makes the table unreadable, because a reader will look for a file that no longer exists. Adding a file by hand does nothing either, since no reader will see it. If space is the problem, the right tools are **compaction** (merge small files into large ones, as a new version) and **vacuum** (delete files no version within the retention window needs). Both are operations the table supports and records, so readers never break.

**14.** Compression settings are visible, quick to change, and feel like engineering; scan volume is invisible unless someone measures it, and fixing it means changing layouts and rewriting queries, which touches other people's work. There's also an anchoring effect: storage bills come with a clear GB number, while compute bills are diffuse. What to measure first: **bytes scanned per query** (or slot/compute seconds), broken down by the top ten most frequent and most expensive queries, and how much of what they scan they actually use after filtering. That measurement almost always points at a missing filter, a wrong partition column, or `SELECT *`, each of which is worth more than any compression codec choice.

---

## Where this leads

- **Chapter 50, Streaming & Real-Time,** writes continuously into tables like these, which is where compaction and small files stop being theoretical.
- **Chapter 51, Data Activation,** reads from the published tables to push data into business systems.
- **Chapter 52, The Cloud, Containers & Infrastructure as Code,** sets up object storage and permissions in practice, and adds compute to section 49.8's cost estimate.
- **Chapter 47** gains its rollback: a failed publish can now be reversed by restoring a version.
- **Chapter 62, Data Architecture Patterns,** organizes a lakehouse into the medallion layers, and **Chapter 65, FinOps: The Economics of Data Platforms,** builds on section 49.8's cost arithmetic.
- **Part 8:** storage and file format questions appear in the data engineering interview chapters, and layout design cases in Chapter 77.
