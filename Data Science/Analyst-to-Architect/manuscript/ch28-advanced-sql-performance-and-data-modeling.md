# Chapter 28. Advanced SQL, Performance & Data Modeling

*Part 3 — Advanced Analytics & Analytics Engineering*

> **Chapter at a glance**
>
> **You will learn to:** walk org charts and bills of materials of any depth with recursive CTEs · protect a recursive query against loops · choose between `ROWS`, `RANGE`, and `GROUPS` frames, and use `EXCLUDE` and named windows · read a query plan with `EXPLAIN` and `EXPLAIN ANALYZE` · decide which indexes to create (single-column, composite, covering, partial) and which to avoid · recognize queries that can't use an index, and rewrite them · normalize a messy table to first, second, and third normal form · declare and test the grain of any table · design a star schema with facts, dimensions, and a date dimension · build slowly changing dimensions of types 1, 2, and 3 · decide when denormalizing is worth it · change a production database safely with versioned migration scripts.
>
> **Before you start:** Chapter 12 (joins, keys, `CREATE TABLE`, `ALTER TABLE`, transactions, the fan-out trap) and Chapter 13 (CTEs, views, window functions, the `sales_lines` view). The chapter also leans on Chapter 4 (the median), Chapters 15 and 21 (percentiles in SQL, sections 15.5 and 21.3), Chapter 16 (section 16.3, the star schema you built in Power BI), Chapter 17 (running a Python script), and Chapter 26 (section 26.0, the terminal).
>
> **Time needed:** 22–30 hours of reading and practice, including the project, spread over four to five weeks.
>
> **Tools:** PostgreSQL 15 or later (every query was run on PostgreSQL 16) and DBeaver, as in Chapter 12, plus PostgreSQL's command-line client, `psql`, which you installed with the server in section 12.3. MySQL works for most of the chapter; section 28.13 shows what changes.
>
> **Practice data:** the one-year database `riverstone_2025` with three new companion tables, a large generated database `riverstone_perf` (1.9 million order lines) that you build in section 28.1, and the `riverstone_lab` database you build yourself. Every query was run, and every result shown is the real output. Timings were measured on the author's test machine and are labeled as such.

> **Plan your sittings.** This is the longest chapter in Part 3: six topics that are each a chapter elsewhere. Take it in six sittings, and stop at the end of one rather than in the middle:
>
> 1. Sections 28.1 (the one-year tables) to 28.3: recursive queries and advanced windows, 5–6 hours.
> 2. Section 28.1's box "Build riverstone_perf", then sections 28.4 to 28.6: plans and indexes, 5–6 hours.
> 3. Sections 28.7 and 28.8: normalization and grain, about 3 hours.
> 4. Sections 28.9 to 28.11: the star schema, slowly changing dimensions, and denormalization, 5–6 hours.
> 5. Sections 28.12 and 28.13: migrations and MySQL, about 3 hours.
> 6. The project, 4–6 hours.
>
> Each sitting ends at a line marked **Good place to stop**.

---

## Why this matters

The queries in Chapters 12 and 13 answer questions. This chapter is about what happens when those queries become part of how a company runs:

- *"Show me everyone who reports to the Head of Production, however many levels down."* A plain join handles one level. Real org charts, product structures, and account hierarchies have as many levels as they like.
- *"The dashboard took two seconds last year. Now it takes forty."* The query didn't change. The data grew, and nobody looked at how the database was finding the rows.
- *"Why does the sales report show Sharma Hardware in two cities?"* Somebody stored the same fact in two places, and updated only one of them.
- *"Revenue by segment for last year changed, and nobody touched last year's orders."* A customer was reclassified, and the report quietly rewrote history.
- *"Can you add a column to the orders table this afternoon?"* On a live system, with reports and applications reading that table, the honest answer is: yes, with a reviewed script, in the right order, and a way back.

These are the problems that separate someone who writes SQL from someone who is trusted with a company's data. They are also the topics that turn up in interviews for senior analyst, analytics engineer, and data engineer roles: *"How would you speed up this query?"*, *"What is the grain of this table?"*, *"Explain a type 2 slowly changing dimension."* You'll be able to answer all three with examples you've built yourself.

---

## In plain English

**A database is a large library, and your query is a request at the front desk.**

Some requests are about **family trees**: *"find this book, then every book that cites it, then every book that cites those."* The librarian can't answer in one trip. She fetches the first shelf, reads it, and goes back for the next, until a trip brings back nothing new. That's a **recursive query**.

For every request, the librarian makes a **plan**. If you ask for one author's books, she can walk every aisle and look at every spine (a **scan**), or she can use the **catalog cards**, sorted by author, which tell her exactly which shelves to visit (an **index**). The catalog makes finding faster, but every new book now means writing a card too, so a library with a catalog for every possible question would spend all day filing cards. You can ask her to **explain her plan** before she sets off.

How the books are organized decides how hard the library is to keep correct. If each book's publisher address is written inside every book, a publisher that moves means correcting thousands of books. So you keep a publisher list and write only the publisher's name in each book. That's **normalization**: every fact in one place.

The reading room upstairs is organized differently. Readers there want to count and compare, not edit, so the librarian keeps a big **ledger of loans** (one line per loan: a **fact**) surrounded by small, friendly lookup lists: dates, readers, books (the **dimensions**). When a reader moves house, the lists keep the old address for old loans and the new address for new ones, so last year's report still describes last year. That's a **slowly changing dimension**.

And when the library wants a new shelf layout, it doesn't move books at random on a busy afternoon. It writes a numbered plan, gets it checked, and carries it out in order, noting each step in a logbook. That's a **migration**.

Keep the library in mind. Recursive queries, plans, indexes, normalization, dimensional models, and migrations are all in this chapter, and each one is a way of keeping a very large library fast and correct.

---

## 28.1 Three practice databases

This chapter uses three databases. Each section says which one it uses.

**The one-year database (`riverstone_2025`)** is Chapter 13's: the 24 key accounts, 175 orders in 2025, monthly targets, and leads, with the `sales_lines` view. (It is one slice of Riverstone, not the whole company: the key accounts the Chapter 13 team looks after.) For this chapter you add three tables to it by running `ch28_2025_addons.sql` from the companion files (`ch28_2025_addons_mysql.sql` for MySQL):

| Table | One row is | Where it comes from | Used in |
|---|---|---|---|
| `staff` | one person on Riverstone's payroll, with their manager | the HR system (HRMS) | section 28.2 |
| `parts` and `bom_lines` | a part (product, assembly, or bought material); one parent-and-child link in a product's structure | production | section 28.2 |
| `customer_changes` | one change to a customer's city or segment during 2025 | the ERP's audit log | sections 28.9–28.10 |

The `staff` table is Riverstone's reporting lines, from the managing director, Arvind Kapoor, down to the machine operators at the Taloja and Chakan plants: 35 people, including the key accounts sales team and the three regional sales managers. The five sales people you know from the `employees` table are in it too, with their `employee_id` filled in, so you can connect the two systems. (In the ERP's `employees` table Anita Rao has no manager, because the ERP only knows the sales team. In the HR system she reports to the managing director. Both are true; they're different systems with different scopes.)

**The large database (`riverstone_perf`)** exists to make performance visible. Indexes don't matter on 175 orders: every query is instant. So the companion script `generate_riverstone_perf.py` builds three years of Riverstone-like sales (2023 to 2025) with the same tables and columns as `riverstone_2025`:

| Table | Rows |
|---|---|
| `customers` | 5,000 |
| `products` | 8 |
| `employees` | 5 |
| `orders` | 714,285 |
| `order_items` | 1,926,847 |

It uses a fixed seed (28), so your data is identical to the book's. If you have the book's full three-year dataset loaded, every command in sections 28.4 to 28.6 works on that instead; only the numbers change. The data takes about 200 MB in PostgreSQL. Apart from primary keys, the tables start with **no indexes**, because adding them is the lesson. You build it at the start of sitting 2, with the box below; skip it until then.

**The lab database (`riverstone_lab`)** is a scratch database you create and change freely, as in section 12.13. Sections 28.7, 28.10, and 28.12 build tables in it step by step. If you still have Chapter 12's lab, the first lab step drops and recreates it.

> **Watch out: timings are measurements, not facts.** Every timing in this chapter was measured on the author's test machine: four virtual processors and 16 GB of memory, running PostgreSQL 16 and MySQL 8.0.46 on Ubuntu 24.04, with other work running alongside. Each query was run seven times and the median is reported. Your laptop will give different numbers. What should match is the *plan* the database chooses and the *ratio* between a slow and a fast version. The companion script `ch28_perf.py` reruns every experiment on your machine and writes its plans and timings to `ch28_perf_log.txt`.

### Build riverstone_perf (about 20 minutes)

This is the chapter's only setup that needs the terminal. You need three things from earlier chapters: a terminal open in a folder (section 26.0), Python (Chapter 17), and your PostgreSQL password (section 12.3).

**Step 1. Create the empty database.** In DBeaver, on your usual PostgreSQL connection, run:

<!-- run: none -->
```sql
CREATE DATABASE riverstone_perf;
```

**Step 2. Generate the data.** In the terminal, move into the chapter's companion folder and run the generator (type `python` instead of `python3` on Windows, as in Chapter 17). It takes about half a minute and prints one line:

<!-- run: none -->
```
# terminal, in the companion files folder
$ cd ch28
$ python3 generate_riverstone_perf.py
customers 5,000  orders 714,285  order lines 1,926,847  (seed 28)
```

It has written a folder `perf_data` next to the script: five CSV files (about 80 MB) and two load scripts, `load_postgresql.sql` and `load_mysql.sql`.

**Step 3. Find `psql`.** The load script uses `\copy`, a command only PostgreSQL's command-line client understands. The client was installed with the server in section 12.3 (on Windows, the *Command Line Tools* component). Check that the terminal can find it:

<!-- run: none -->
```
# terminal
$ psql --version
psql (PostgreSQL) 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
```

Your version line will differ. If the terminal says *command not found* instead:

- **Windows:** type the full path in place of `psql`, in quotes, for example `"C:\Program Files\PostgreSQL\16\bin\psql.exe" --version` (change `16` to your version). Chapter 34 shows how to add that folder to your `PATH` so the short name works.
- **macOS:** with Postgres.app, use `/Applications/Postgres.app/Contents/Versions/latest/bin/psql`; with Homebrew, `brew install libpq` installs the client.
- **Linux:** `sudo apt install postgresql-client`.

**Step 4. Load the data.** Still in the `ch28` folder:

<!-- run: none -->
```
# terminal
$ psql -U postgres -d riverstone_perf -f perf_data/load_postgresql.sql
Password for user postgres:
psql:perf_data/load_postgresql.sql:2: NOTICE:  table "order_items" does not exist, skipping
psql:perf_data/load_postgresql.sql:2: NOTICE:  table "orders" does not exist, skipping
psql:perf_data/load_postgresql.sql:2: NOTICE:  table "employees" does not exist, skipping
psql:perf_data/load_postgresql.sql:2: NOTICE:  table "products" does not exist, skipping
psql:perf_data/load_postgresql.sql:2: NOTICE:  table "customers" does not exist, skipping
DROP TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
COPY 5000
COPY 8
COPY 5
COPY 714285
COPY 1926847
ANALYZE
```

**What each part does:**

- **`-U postgres`** connects as the user `postgres`, the administrator account from section 12.3. psql asks for its password; nothing appears on the screen while you type it, which is normal.
- **`-d riverstone_perf`** chooses the database, the one you created in step 1.
- **`-f perf_data/load_postgresql.sql`** runs every statement in that file, in order, and prints what each one did.
- The five **`NOTICE`** lines are harmless: the script starts by dropping the tables in case you run it twice, and on the first run there's nothing to drop. **`COPY 714285`** means 714,285 rows were read from `orders.csv`. The load takes under a minute; the final `ANALYZE` collects the statistics section 28.5 explains.

**Step 5. One setting.** Back in DBeaver, run:

<!-- run: none -->
```sql
ALTER DATABASE riverstone_perf SET max_parallel_workers_per_gather = 0;
```

It turns off *parallel query*, which PostgreSQL uses on machines with several processor cores. Parallel plans are correct but longer to read, and they make timings jump about. The book's plans were all made with this setting. It applies to connections opened *after* you run it, so disconnect and reconnect DBeaver's `riverstone_perf` connection. You can reset it later with `ALTER DATABASE riverstone_perf RESET max_parallel_workers_per_gather;`.

**Step 6. Check it.** Make a DBeaver connection to `riverstone_perf` (as in section 12.3, with *Database* set to `riverstone_perf`) and run:

<!-- db: riverstone_perf -->

```sql
SELECT COUNT(*) FROM order_items;
```

```
  count
---------
 1926847
(1 row)
```

If you see 1,926,847, you're ready for section 28.4.

> **No terminal access?** DBeaver can do the load instead. Run the five `CREATE TABLE` statements from `load_postgresql.sql` in DBeaver, then right-click each table → *Import Data* → *CSV*, and load the files in this order, so every foreign key finds its row: `customers.csv`, `products.csv`, `employees.csv`, `orders.csv`, `order_items.csv`. The files have no header row, so untick *Header*. It's slower, but the result is the same.

> **Using MySQL?** The same steps, with MySQL's client. The server must allow file loading once: as the `root` user, run `SET GLOBAL local_infile = 1;` in DBeaver. Then, in the `ch28` folder, `mysql -u root -p --local-infile=1 < perf_data/load_mysql.sql`. Here `-u root` is the user, `-p` makes the client ask for the password, `--local-infile=1` lets the client send files from your computer, and `<` feeds the script to the client as its input. The script creates the database itself. Section 28.13 uses it.

---

## 28.2 Recursive CTEs: walking trees of any depth

A **recursive CTE** is a CTE that refers to itself. It is how SQL walks data where rows point at other rows of the same table: org charts, product structures, account hierarchies. It can also build a list, such as every month of a year, when no table holds one. This section starts with the smallest recursive query there is, then climbs to Riverstone's org chart and its bills of materials.

### Your first recursive query: counting to five

The plan: start with the number 1, and keep adding 1 until you reach 5. In the one-year database (any database works; this query reads no tables):

<!-- db: riverstone_2025 -->

```sql
WITH RECURSIVE numbers AS (
    SELECT 1 AS n        -- anchor: runs once
    UNION ALL
    SELECT n + 1         -- recursive part: runs again and again
    FROM numbers
    WHERE n < 5          -- stop rule
)
SELECT n FROM numbers;
```

```
 n
---
 1
 2
 3
 4
 5
(5 rows)
```

**How it works, line by line:**

- **`WITH RECURSIVE numbers AS (…)`** is a CTE, as in section 13.2, with one new word. **`RECURSIVE`** tells the database that a CTE in this `WITH` list may refer to itself. It is written once, straight after `WITH`, and covers the whole list, even when some of the CTEs in it aren't recursive (you'll see that in "Guarding against loops").
- **`SELECT 1 AS n`** is the **anchor**. It runs once and produces the starting row. Its column names and types fix the CTE's columns: there is one column, `n`, and it holds whole numbers.
- **`UNION ALL`** glues each pass's rows onto the result.
- **`SELECT n + 1 FROM numbers WHERE n < 5`** is the **recursive part**. Inside it, `numbers` does not mean the whole result so far. It means only the rows the **previous pass** produced (the database's name for them is the *working table*). So each pass reads one row and makes the next number.
- **The stop rule:** when a pass produces no rows, the query ends. `WHERE n < 5` is what makes that happen.
- The final **`SELECT n FROM numbers`** reads everything the passes produced, like any CTE.

Trace it pass by pass:

| Pass | Reads (the previous pass's rows) | Produces |
|---|---|---|
| anchor | nothing | 1 |
| 1 | 1 | 2 |
| 2 | 2 | 3 |
| 3 | 3 | 4 |
| 4 | 4 | 5 |
| 5 | 5 | nothing, because `5 < 5` is false: stop |

**What happens if you change it?** Predict before you run it: what does the query do without `WHERE n < 5`? Nothing ever stops the passes. In PostgreSQL the query keeps going until you cancel it (DBeaver's *Cancel* button, next to the results) or the numbers grow too large for their type. MySQL protects you. It stops any recursive CTE that runs more than 1,000 passes, a limit held in the setting **`cte_max_recursion_depth`**:

```mysql
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers
)
SELECT COUNT(*) FROM numbers;
```

```
ERROR 3636 (HY000): Recursive query aborted after 1001 iterations. Try increasing @@cte_max_recursion_depth to a larger value.
```

For a legitimate walk longer than 1,000 steps, raise the limit for your session first: `SET SESSION cte_max_recursion_depth = 10000;`. PostgreSQL has no such limit, which is why "Guarding against loops", later in this section, matters there.

> **UNION or UNION ALL?** Plain `UNION` (section 12.12) would remove duplicate rows on every pass. Use `UNION ALL` unless you have a reason not to: it's faster, and it keeps repeats that are real. You'll see one in the bill of materials below, where steel tube legitimately appears twice.

### A list of months when there's no calendar table

Chapter 13's Pattern 5 filled in the missing months with a **date spine**, and used the calendar table `calendar_months` for it. Most companies have one; when yours doesn't, a recursive CTE builds the same list. Change the counter to count months: start at 1 January 2025 and add one month per pass until December.

```sql
WITH RECURSIVE months AS (
    SELECT DATE '2025-01-01' AS month
    UNION ALL
    SELECT month + INTERVAL '1 month'
    FROM months
    WHERE month < DATE '2025-12-01'
)
SELECT month FROM months;
```

```
ERROR:  recursive query "months" column 1 has type date in non-recursive term but type timestamp without time zone overall
```

A real error, and a useful one. The anchor's `DATE '2025-01-01'` is a `date`, but `month + INTERVAL '1 month'` gives a timestamp (a date with a time of day, as `generate_series` did in Pattern 5). The anchor fixes the column's type, so the recursive part must produce the same type. `CAST(… AS DATE)` (section 12.8) turns each new month back into a date:

```sql
WITH RECURSIVE months AS (
    SELECT DATE '2025-01-01' AS month
    UNION ALL
    SELECT CAST(month + INTERVAL '1 month' AS DATE)
    FROM months
    WHERE month < DATE '2025-12-01'
)
SELECT COUNT(*) AS months, MIN(month) AS first_month, MAX(month) AS last_month
FROM months;
```

```
 months | first_month | last_month
--------+-------------+------------
     12 | 2025-01-01  | 2025-12-01
(1 row)
```

Twelve months, the same rows as `calendar_months`. Pass 11 produces 1 December; pass 12 reads it, finds `month < '2025-12-01'` false, and produces nothing. To use it, put this `months` step where Pattern 5 had `calendar_months`. In MySQL only the step changes spelling (`month + INTERVAL 1 MONTH`, and no `CAST` is needed, because MySQL keeps a date plus a month as a date). Here is Pattern 5's Garden Chair query in MySQL with that spine:

```mysql
WITH RECURSIVE months AS (
    SELECT DATE '2025-01-01' AS month           -- the first month
    UNION ALL
    SELECT month + INTERVAL 1 MONTH             -- add one month...
    FROM months
    WHERE month < DATE '2025-12-01'             -- ...until December
),
furniture AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month,
           SUM(net_revenue)                                  AS revenue
    FROM sales_lines
    WHERE category = 'Furniture'
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
),
filled AS (
    SELECT m.month,
           COALESCE(f.revenue, 0)                              AS revenue,
           LAG(COALESCE(f.revenue, 0)) OVER (ORDER BY m.month) AS previous_month
    FROM months AS m
    LEFT JOIN furniture AS f ON f.month = m.month
)
SELECT month, ROUND(revenue, 0) AS revenue, ROUND(previous_month, 0) AS previous_month
FROM filled
WHERE month BETWEEN '2025-02-01' AND '2025-06-01'
ORDER BY month;
```

```
+------------+---------+----------------+
| month      | revenue | previous_month |
+------------+---------+----------------+
| 2025-02-01 |       0 |              0 |
| 2025-03-01 |   16388 |              0 |
| 2025-04-01 |       0 |          16388 |
| 2025-05-01 |   17250 |              0 |
| 2025-06-01 |       0 |          17250 |
+------------+---------+----------------+
```

The same five rows as Pattern 5. Only the first CTE is recursive, and `WITH RECURSIVE` is still written once, at the start of the list. `DATE_FORMAT(order_date, '%Y-%m-01')` is Chapter 13's MySQL spelling of "the first of the month" (section 13.9). A monthly spine needs 11 passes, far below MySQL's limit; a *daily* spine for three years needs 1,095 and would stop with error 3636 unless you raise `cte_max_recursion_depth` first. For dates you'll use again and again, a permanent calendar table is still the better answer.

Counting and listing months are warm-ups. The real power of recursion is walking **hierarchies**.

### The problem

*"List everyone at Riverstone with their level in the organization."*

Each `staff` row stores only its own manager:

<!-- db: riverstone_2025 -->

```sql
SELECT staff_id, staff_name, job_title, manager_id
FROM staff
WHERE staff_name IN ('Arvind Kapoor', 'Harpreet Sethi', 'Ramesh Patil', 'Ajay Kumar', 'Gopal Sahu')
ORDER BY staff_id;
```

```
 staff_id |   staff_name   |       job_title       | manager_id
----------+----------------+-----------------------+------------
      100 | Arvind Kapoor  | Managing Director     |
      130 | Harpreet Sethi | Head of Production    |        100
      131 | Ramesh Patil   | Plant Manager, Taloja |        130
      133 | Ajay Kumar     | Shift Supervisor      |        131
      136 | Gopal Sahu     | Machine Operator      |        133
(5 rows)
```

A self-join (section 12.10) gets you one level: each person and their manager. Two self-joins get you two levels. But the org chart is five levels deep today and may be six next year, and you can't write a query with a join for every level that might exist. You need a query that keeps going until it runs out of people.

### The org chart, level by level

The same shape as the counter. The anchor is the one person with no manager. The recursive part finds everyone whose manager was found on the previous pass, and adds 1 to the level, where the counter added 1 to `n`.

Here is the query:

```sql
WITH RECURSIVE org AS (
    -- anchor: the person with no manager
    SELECT staff_id, staff_name, job_title, manager_id,
           1 AS level
    FROM staff
    WHERE manager_id IS NULL
    UNION ALL
    -- recursive part: everyone whose manager is already in org
    SELECT s.staff_id, s.staff_name, s.job_title, s.manager_id,
           o.level + 1
    FROM staff AS s
    JOIN org AS o ON s.manager_id = o.staff_id
)
SELECT level, staff_name, job_title
FROM org
ORDER BY level, staff_id;
```

```
 level |   staff_name   |           job_title
-------+----------------+-------------------------------
     1 | Arvind Kapoor  | Managing Director
     2 | Anita Rao      | Sales Head
     2 | Suresh Menon   | Finance Manager
     2 | Harpreet Sethi | Head of Production
     2 | Joseph D'Souza | Purchasing Manager
     2 | Mahesh Yadav   | Warehouse & Dispatch Manager
     2 | Lakshmi Reddy  | HR Manager
     2 | Zoya Mirza     | Marketing Manager
     2 | Tenzin Dorji   | Customer Support Lead
     3 | Vikram Singh   | Sales Manager, Key Accounts
     3 | Farah Khan     | Sales Executive
     3 | Meera Iyer     | Sales Coordinator
     3 | Arjun Nair     | Regional Sales Manager, South
     3 | Pooja Desai    | Regional Sales Manager, West
     3 | Sandeep Gill   | Regional Sales Manager, North
     3 | Priya Nambiar  | Accounts Executive
     3 | Ramesh Patil   | Plant Manager, Taloja
     3 | Kiran Bhosale  | Plant Manager, Chakan
     3 | Mohan Das      | Dispatch Supervisor
     4 | Neha Kulkarni  | Sales Executive
     4 | Rahul Mehta    | Sales Executive
     4 | Ajay Kumar     | Shift Supervisor
     4 | Farhan Ali     | Quality Inspector
     4 | Swati Joshi    | Shift Supervisor
     4 | Divya Krishnan | Sales Executive
     4 | Vivek Chandran | Sales Executive
     4 | Sneha Pillai   | Sales Executive
     4 | Nisha Bhatt    | Sales Executive
     4 | Aditya Verma   | Sales Executive
     4 | Rohit Kamat    | Sales Executive
     4 | Karan Ahuja    | Sales Executive
     4 | Ritu Bansal    | Sales Executive
     5 | Gopal Sahu     | Machine Operator
     5 | Sunita Pawar   | Machine Operator
     5 | Farid Shaikh   | Machine Operator
(35 rows)
```

**How it works:**

- A recursive CTE has two queries joined by `UNION ALL`. The first is the **anchor**: it runs once and produces the starting rows. Here that's Arvind Kapoor, the only person with no manager.
- The second is the **recursive part**. It refers to `org`, the CTE's own name. On each pass it sees only the rows the *previous* pass produced, and joins `staff` to them: "who reports to someone we found last time?"
- `o.level + 1` carries information down the tree. Each person's level is their manager's level plus one.
- The recursion stops by itself when a pass finds no new rows. After the machine operators, nobody reports to anybody new, so pass 5 returns nothing and the query ends.
- The final `SELECT` reads the whole accumulated result like any other CTE.

The passes, counted from the output:

| Pass | Reads | Finds | Who they are |
|---|---|---|---|
| anchor | nothing | 1 | the managing director (level 1) |
| 1 | 1 | 8 | the eight department heads (level 2) |
| 2 | 8 | 10 | the ten people at level 3: six managers, and four people who manage no one |
| 3 | 10 | 13 | level 4: supervisors, an inspector, and the sales executives |
| 4 | 13 | 3 | the three machine operators (level 5) |
| 5 | 3 | 0 | nobody reports to an operator: stop |

1 + 8 + 10 + 13 + 3 = 35 people.

![An organization chart of 16 of Riverstone's 35 staff in five levels, each level labeled with its number and the pass that finds it, from the managing director at the top through department heads, managers, supervisors, and machine operators](figures/fig28-1-org-chart-levels.svg)

*Figure 28.1 — Each pass of the recursive part adds one level. The query stops when a pass finds nobody new. The chart shows 16 of the 35 people; the query returns all of them.*

Check a number by hand: Farah Khan reports directly to Anita Rao, who reports to Arvind Kapoor. Level 1, 2, 3. ✓ And the row count, 35, matches `SELECT COUNT(*) FROM staff`, so nobody was lost. That check matters more than it looks: a person whose `manager_id` points to someone who doesn't exist would silently disappear from a recursive walk. Exercise 4 asks you to find such orphans.

### Walking up instead of down

*"Who is in Gopal Sahu's chain of command?"* Reverse the join: start from one person and repeatedly fetch *their manager*.

```sql
WITH RECURSIVE chain AS (
    SELECT staff_id, staff_name, manager_id, 0 AS steps_up
    FROM staff
    WHERE staff_name = 'Gopal Sahu'
    UNION ALL
    SELECT m.staff_id, m.staff_name, m.manager_id, c.steps_up + 1
    FROM staff AS m
    JOIN chain AS c ON m.staff_id = c.manager_id
)
SELECT steps_up, staff_name
FROM chain
ORDER BY steps_up;
```

```
 steps_up |   staff_name
----------+----------------
        0 | Gopal Sahu
        1 | Ajay Kumar
        2 | Ramesh Patil
        3 | Harpreet Sethi
        4 | Arvind Kapoor
(5 rows)
```

The only change is the join direction: `m.staff_id = c.manager_id` ("the person whose id is my manager's id") instead of `s.manager_id = o.staff_id`. An approval workflow uses exactly this walk. Riverstone's discount rules (Chapter 3) send large discounts up the chain until they reach someone with enough authority.

### Counting everyone below each manager

*"How many people does each manager have under them, directly or indirectly?"* The trick is to pair every manager with every person below them.

Start each person as "under themselves", then walk down:

```sql
WITH RECURSIVE under AS (
    SELECT staff_id AS manager_id, staff_id AS member_id
    FROM staff
    UNION ALL
    SELECT u.manager_id, s.staff_id
    FROM under AS u
    JOIN staff AS s ON s.manager_id = u.member_id
)
SELECT m.staff_name,
       m.job_title,
       COUNT(*) - 1 AS people_below
FROM under AS u
JOIN staff AS m ON m.staff_id = u.manager_id
GROUP BY m.staff_id, m.staff_name, m.job_title
HAVING COUNT(*) > 1
ORDER BY people_below DESC, m.staff_id;
```

```
   staff_name   |           job_title           | people_below
----------------+-------------------------------+--------------
 Arvind Kapoor  | Managing Director             |           34
 Anita Rao      | Sales Head                    |           16
 Harpreet Sethi | Head of Production            |            8
 Ramesh Patil   | Plant Manager, Taloja         |            4
 Arjun Nair     | Regional Sales Manager, South |            3
 Pooja Desai    | Regional Sales Manager, West  |            3
 Vikram Singh   | Sales Manager, Key Accounts   |            2
 Sandeep Gill   | Regional Sales Manager, North |            2
 Kiran Bhosale  | Plant Manager, Chakan         |            2
 Ajay Kumar     | Shift Supervisor              |            2
 Suresh Menon   | Finance Manager               |            1
 Swati Joshi    | Shift Supervisor              |            1
 Mahesh Yadav   | Warehouse & Dispatch Manager  |            1
(13 rows)
```

**How it works:**

- The anchor has one row per person: `(manager_id = me, member_id = me)`. That's 35 rows.
- Each pass takes every pair and adds the member's direct reports as new members of the same manager. Arvind's pairs grow to include everyone; Ajay Kumar's grow to include his two operators.
- `COUNT(*) - 1` removes the "under myself" row. `HAVING COUNT(*) > 1` keeps only people who manage somebody.
- Reconcile: the managing director has 34 people below him, which is everyone except himself (35 − 1). ✓ Harpreet Sethi's 8 is the two plant managers, two supervisors, one inspector, and three operators.

### Combining a hierarchy with facts

Now join the tree to numbers. *"What did Anita Rao's key accounts team sell in 2025?"* Anita's branch of the tree now includes the regional sales managers and their executives, but the one-year database holds only the key accounts, so the query keeps the five people the ERP knows by their `employee_id`.

```sql
WITH RECURSIVE sales_team AS (
    SELECT staff_id, staff_name, employee_id
    FROM staff
    WHERE staff_name = 'Anita Rao'
    UNION ALL
    SELECT s.staff_id, s.staff_name, s.employee_id
    FROM staff AS s
    JOIN sales_team AS t ON s.manager_id = t.staff_id
)
SELECT t.staff_name,
       COUNT(DISTINCT sl.order_id) AS orders,
       ROUND(SUM(sl.net_revenue))  AS net_revenue
FROM sales_team AS t
LEFT JOIN sales_lines AS sl ON sl.sales_rep_id = t.employee_id
WHERE t.employee_id IS NOT NULL      -- the ERP knows only the key accounts team
GROUP BY t.staff_name
ORDER BY net_revenue DESC NULLS LAST;
```

```
  staff_name   | orders | net_revenue
---------------+--------+-------------
 Rahul Mehta   |     53 |     1494001
 Farah Khan    |     64 |     1489073
 Neha Kulkarni |     46 |     1147895
 Anita Rao     |      0 |
 Vikram Singh  |      0 |
(5 rows)
```

The three executives' revenue adds up to ₹41,30,969. Chapter 13's total for 2025 is ₹43,35,471, so ₹2,04,502 belongs to orders with no sales rep recorded (Chapter 13's data-quality check, Pattern 10, found 11 orders with no rep; 10 of them are not cancelled, and those hold the ₹2,04,502). The team walk is right; the gap is a data problem, and it's exactly the kind of gap you should explain before anyone else finds it. Meera Iyer isn't in the result at all: she has no `employee_id`, because a coordinator doesn't take orders. Vikram Singh has no orders recorded under his own name in 2025; his team's orders are credited to the executives who took them.

> **Watch out: a recursive CTE's column types must match.** You met this with the list of months. It bites again in the next example: if the anchor returns `quantity` as `NUMERIC(8,3)` and the recursive part multiplies it (giving plain `NUMERIC`), PostgreSQL stops with *ERROR: recursive query "explode" column 3 has type numeric(8,3) in non-recursive term but type numeric overall*. The fix is to cast the anchor's column to the wider type, `CAST(b.quantity AS NUMERIC)`. MySQL has the opposite problem: it sizes text columns from the anchor, so a path string that grows on each pass fails with a *Data too long* error unless you `CAST` it to a long enough `CHAR` in the anchor (section 28.13).

### Bills of materials

Riverstone's production team keeps a **bill of materials** (BOM): the list of parts that make each product, where some parts are themselves made of parts. The `bom_lines` table stores one link per row: "one unit of *parent* needs *quantity* units of *child*". The `parts` table says what each part is:

```sql
SELECT part_type, COUNT(*) AS parts
FROM parts
GROUP BY part_type
ORDER BY part_type;
```

```
 part_type | parts
-----------+-------
 Assembly  |     9
 Material  |     6
 Product   |     5
(3 rows)
```

Five products, nine assemblies made in-house (a box body, a lid, a steel frame), and six materials bought from the suppliers you met in Chapter 12's lab.

*"What does it take to make one Garden Chair?"* This is called **exploding** the BOM. It's the org-chart walk with one addition: quantities multiply on the way down.

```sql
WITH RECURSIVE explode AS (
    SELECT b.parent_part_id AS product_id,
           b.child_part_id,
           CAST(b.quantity AS NUMERIC) AS qty_per_product,
           1 AS depth
    FROM bom_lines AS b
    WHERE b.parent_part_id = 106          -- 106 = Garden Chair
    UNION ALL
    SELECT e.product_id,
           b.child_part_id,
           e.qty_per_product * b.quantity,
           e.depth + 1
    FROM explode AS e
    JOIN bom_lines AS b ON b.parent_part_id = e.child_part_id
)
SELECT e.depth,
       p.part_name,
       p.part_type,
       CAST(e.qty_per_product AS NUMERIC(8,3)) AS qty_per_chair,
       p.unit
FROM explode AS e
JOIN parts AS p ON p.part_id = e.child_part_id
ORDER BY e.depth, p.part_id;
```

```
 depth |       part_name        | part_type | qty_per_chair | unit
-------+------------------------+-----------+---------------+------
     1 | Seat shell             | Assembly  |         1.000 | each
     1 | Steel frame            | Assembly  |         1.000 | each
     1 | Product label          | Material  |         1.000 | each
     1 | Shipping carton        | Material  |         1.000 | each
     2 | Leg assembly           | Assembly  |         2.000 | each
     2 | Polypropylene granules | Material  |         2.200 | kg
     2 | Color masterbatch      | Material  |         0.080 | kg
     2 | Steel tube             | Material  |         1.000 | kg
     2 | Fastener pack          | Material  |         1.000 | each
     3 | Steel tube             | Material  |         2.400 | kg
     3 | Fastener pack          | Material  |         2.000 | each
(11 rows)
```

![A tree diagram: the Garden Chair splits into seat shell, steel frame, label, and carton; the frame splits into two leg assemblies, steel tube, and fasteners; each leg assembly needs 1.2 kg of steel tube, so the chair needs 2.4 kg through its legs. A side panel totals the material cost at ₹647.80](figures/fig28-2-bill-of-materials.svg)

*Figure 28.2 — Quantities multiply down the tree: 2 leg assemblies × 1.2 kg each = 2.4 kg of steel tube.*

**How it works:**

- The anchor fetches the chair's direct children (depth 1).
- The recursive part fetches each child's own children and multiplies: the frame needs 2 leg assemblies, each leg assembly needs 1.2 kg of steel tube, so through the legs one chair needs 2 × 1.2 = 2.4 kg. That's the steel tube row at depth 3, the shaded box in Figure 28.2.
- Steel tube appears twice (1.0 kg directly in the frame, 2.4 kg in the legs). That's correct: it's used in two places. To buy steel, you add them: 3.4 kg per chair.
- Assemblies appear in the list, but you don't buy them. For purchasing, keep only `part_type = 'Material'`.

### Rolling up material cost

*"What are the materials in each product worth, compared with its standard cost?"* Explode every product at once, keep the materials, multiply by their cost, and add up per product:

```sql
WITH RECURSIVE explode AS (
    SELECT b.parent_part_id AS product_id,
           b.child_part_id,
           CAST(b.quantity AS NUMERIC) AS qty_per_product
    FROM bom_lines AS b
    WHERE b.parent_part_id IN (SELECT part_id FROM parts WHERE part_type = 'Product')
    UNION ALL
    SELECT e.product_id,
           b.child_part_id,
           e.qty_per_product * b.quantity
    FROM explode AS e
    JOIN bom_lines AS b ON b.parent_part_id = e.child_part_id
)
SELECT p.part_id    AS product_id,
       p.part_name  AS product_name,
       CAST(SUM(e.qty_per_product * m.material_cost) AS NUMERIC(10,2)) AS material_cost,
       pr.unit_cost AS standard_cost
FROM explode AS e
JOIN parts    AS m  ON m.part_id = e.child_part_id AND m.part_type = 'Material'
JOIN parts    AS p  ON p.part_id = e.product_id
JOIN products AS pr ON pr.product_id = p.part_id
GROUP BY p.part_id, p.part_name, pr.unit_cost
ORDER BY p.part_id;
```

```
 product_id |    product_name    | material_cost | standard_cost
------------+--------------------+---------------+---------------
        101 | Storage Box 10L    |        110.30 |        300.00
        102 | Storage Box 25L    |        199.30 |        540.00
        104 | Food Container Set |         59.42 |        430.00
        106 | Garden Chair       |        647.80 |        850.00
        108 | Stackable Bin      |         55.40 |        190.00
(5 rows)
```

The last join works because Riverstone numbered its parts to match its products: part 106 *is* product 106, the Garden Chair, so `pr.product_id = p.part_id` fetches the product's standard cost from Chapter 12's `products` table. Products 103, 105, and 107 are missing from the result because the `parts` table holds the bills of materials for only five of the eight products.

Check the chair by hand, using the explosion above: polypropylene 2.2 kg × ₹110 = ₹242.00, masterbatch 0.08 kg × ₹260 = ₹20.80, steel tube 3.4 kg × ₹95 = ₹323.00, fasteners 3 × ₹14 = ₹42.00, label ₹2.00, carton ₹18.00. Total ₹647.80. ✓

**What to tell the production head.** Materials are three-quarters of the Garden Chair's ₹850 standard cost (₹647.80, or 76.2%), and half of that (₹323.00, 49.9%) is steel tube. A 10% rise in the steel price would add ₹32.30 to every chair, while the same rise in polypropylene would add ₹24.20. For the Food Container Set, materials are only ₹59.42 of ₹430: the cost is in molding time, not plastic. Those are two different conversations with two different suppliers. (Standard cost also includes labor, machine time, and overheads, which the BOM doesn't hold.)

### Where is a part used?

The reverse question matters when a supplier has a problem: *"Kaveri Steel Works can't deliver steel tube this month. Which products are affected, and how much tube does each unit need?"* Walk *up* from the part:

```sql
WITH RECURSIVE uses AS (
    SELECT b.parent_part_id, CAST(b.quantity AS NUMERIC) AS qty
    FROM bom_lines AS b
    WHERE b.child_part_id = 305           -- 305 = Steel tube
    UNION ALL
    SELECT b.parent_part_id, u.qty * b.quantity
    FROM uses AS u
    JOIN bom_lines AS b ON b.child_part_id = u.parent_part_id
)
SELECT p.part_name,
       CAST(SUM(u.qty) AS NUMERIC(8,3)) AS kg_steel_tube_per_unit
FROM uses AS u
JOIN parts AS p ON p.part_id = u.parent_part_id
WHERE p.part_type = 'Product'
GROUP BY p.part_name;
```

```
  part_name   | kg_steel_tube_per_unit
--------------+------------------------
 Garden Chair |                  3.400
(1 row)
```

Only the Garden Chair, at 3.4 kg per unit, matching the explosion. ✓ This is called a **where-used** query.

### Guarding against loops

A tree has no loops: nobody is their own manager's manager. But data entered by people can contain one. Suppose, by mistake, person 1 reports to 3, 3 reports to 2, and 2 reports to 1. To experiment safely, build those three rows as a tiny table inside the query, with `VALUES`:

```sql
WITH bad_staff (staff_id, manager_id) AS (
    VALUES (1, 3), (2, 1), (3, 2)
)
SELECT * FROM bad_staff;
```

```
 staff_id | manager_id
----------+------------
        1 |          3
        2 |          1
        3 |          2
(3 rows)
```

**How it works:** `VALUES (1, 3), (2, 1), (3, 2)` builds a three-row table from typed-in values, exactly as in section 14.3. There you named its columns with `AS v(row_no, branch, line)`; here the names go in brackets after the CTE's name, `bad_staff (staff_id, manager_id)`. It's the quickest way to make test data that no real table holds.

Now walk up the chain from person 1, as in "Walking up instead of down". The loop means the walk would go round forever, so `LIMIT` stops the output after seven rows:

```sql
WITH RECURSIVE bad_staff (staff_id, manager_id) AS (
    VALUES (1, 3), (2, 1), (3, 2)
),
chain AS (
    SELECT staff_id, manager_id, 1 AS steps
    FROM bad_staff
    WHERE staff_id = 1
    UNION ALL
    SELECT b.staff_id, b.manager_id, c.steps + 1
    FROM bad_staff AS b
    JOIN chain AS c ON b.staff_id = c.manager_id
)
SELECT * FROM chain LIMIT 7;
```

```
 staff_id | manager_id | steps
----------+------------+-------
        1 |          3 |     1
        3 |          2 |     2
        2 |          1 |     3
        1 |          3 |     4
        3 |          2 |     5
        2 |          1 |     6
        1 |          3 |     7
(7 rows)
```

`bad_staff` isn't recursive, but `WITH RECURSIVE` covers the whole list, so `chain` can refer to itself. Without the `LIMIT`, the query never ends in PostgreSQL (until it runs out of memory or someone cancels it). There are three defenses.

**Defense 1: a depth limit.** Add a condition on the level to the recursive part, so the passes stop at a set depth:

```sql
WITH RECURSIVE bad_staff (staff_id, manager_id) AS (
    VALUES (1, 3), (2, 1), (3, 2)
),
chain AS (
    SELECT staff_id, manager_id, 1 AS steps
    FROM bad_staff
    WHERE staff_id = 1
    UNION ALL
    SELECT b.staff_id, b.manager_id, c.steps + 1
    FROM bad_staff AS b
    JOIN chain AS c ON b.staff_id = c.manager_id
    WHERE c.steps < 7                -- defense 1: a depth limit
)
SELECT * FROM chain;
```

```
 staff_id | manager_id | steps
----------+------------+-------
        1 |          3 |     1
        3 |          2 |     2
        2 |          1 |     3
        1 |          3 |     4
        3 |          2 |     5
        2 |          1 |     6
        1 |          3 |     7
(7 rows)
```

The same seven rows, but now the query stops on its own: the pass that reads the row with `steps = 7` finds `7 < 7` false and produces nothing. It's simple and works in every database. The catch: it also stops a *legitimate* tree that's deeper than the limit, and it doesn't tell you there was a loop. Set it well above the real depth (Riverstone's org chart has five levels; 20 is a safe limit).

**Defense 2: remember the path.** Carry the ids visited so far in a text column, and refuse to visit an id that's already in it:

```sql
WITH RECURSIVE bad_staff (staff_id, manager_id) AS (
    VALUES (1, 3), (2, 1), (3, 2)
),
chain AS (
    SELECT staff_id, manager_id,
           CAST(staff_id AS VARCHAR(200)) AS path
    FROM bad_staff
    WHERE staff_id = 1
    UNION ALL
    SELECT b.staff_id, b.manager_id,
           CAST(c.path || '/' || b.staff_id AS VARCHAR(200))
    FROM bad_staff AS b
    JOIN chain AS c ON b.staff_id = c.manager_id
    WHERE '/' || c.path || '/' NOT LIKE '%/' || b.staff_id || '/%'   -- defense 2
)
SELECT * FROM chain;
```

```
 staff_id | manager_id | path
----------+------------+-------
        1 |          3 | 1
        3 |          2 | 1/3
        2 |          1 | 1/3/2
(3 rows)
```

**How it works:**

- The anchor starts the path with the first id, `'1'`. Each pass adds `/` and the new id with `||`, PostgreSQL's operator for joining text (section 12.8), so the path grows `1`, `1/3`, `1/3/2`.
- The `CAST(… AS VARCHAR(200))` in both parts keeps the column's type the same on every pass (the rule you met with the list of months).
- The `WHERE` wraps the path in slashes (`/1/3/2/`) and asks, with `NOT LIKE` (section 12.6), whether `/1/` is already in it. It is, so the fourth row is never made and the walk stops after three rows, each person once.

The same idea works in MySQL (with `CONCAT` instead of `||`); section 28.13 uses it.

**Defense 3: PostgreSQL's `CYCLE` clause** (PostgreSQL 14 and later) does the path check for you:

```sql
WITH RECURSIVE bad_staff (staff_id, manager_id) AS (
    VALUES (1, 3), (2, 1), (3, 2)
),
chain AS (
    SELECT staff_id, manager_id
    FROM bad_staff
    WHERE staff_id = 1
    UNION ALL
    SELECT b.staff_id, b.manager_id
    FROM bad_staff AS b
    JOIN chain AS c ON b.staff_id = c.manager_id
)
CYCLE staff_id SET is_loop USING visited
SELECT staff_id, manager_id, is_loop, visited
FROM chain;
```

```
 staff_id | manager_id | is_loop |      visited
----------+------------+---------+-------------------
        1 |          3 | f       | {(1)}
        3 |          2 | f       | {(1),(3)}
        2 |          1 | f       | {(1),(3),(2)}
        1 |          3 | t       | {(1),(3),(2),(1)}
(4 rows)
```

**How it works:** `CYCLE staff_id` watches that column. `SET is_loop` names a new true/false column, and `USING visited` names the column that holds the path. When a row's `staff_id` is already in its path, it's marked `is_loop = t` and not followed further. PostgreSQL prints the path as a list in curly braces, `{(1),(3)}`; each id sits in its own round brackets because `CYCLE` can watch several columns at once, and then each entry would hold several values. Filter `WHERE is_loop` to list the loops so someone can fix the data.

### Ordering a tree: SEARCH DEPTH FIRST

The org chart query sorted people by level: everyone at level 2, then everyone at level 3. An indented org chart is drawn differently: each manager, followed straight away by their whole team. PostgreSQL's `SEARCH` clause (PostgreSQL 14 and later) produces that order. Here's Anita Rao's branch:

```sql
WITH RECURSIVE org AS (
    SELECT staff_id, staff_name, 1 AS level
    FROM staff
    WHERE staff_name = 'Anita Rao'
    UNION ALL
    SELECT s.staff_id, s.staff_name, o.level + 1
    FROM staff AS s
    JOIN org AS o ON s.manager_id = o.staff_id
)
SEARCH DEPTH FIRST BY staff_id SET visit_order
SELECT REPEAT('    ', level - 1) || staff_name AS team
FROM org
ORDER BY visit_order;
```

```
          team
------------------------
 Anita Rao
     Vikram Singh
         Neha Kulkarni
         Rahul Mehta
     Farah Khan
     Meera Iyer
     Arjun Nair
         Divya Krishnan
         Vivek Chandran
         Sneha Pillai
     Pooja Desai
         Nisha Bhatt
         Aditya Verma
         Rohit Kamat
     Sandeep Gill
         Karan Ahuja
         Ritu Bansal
(17 rows)
```

**How it works:**

- **`SEARCH DEPTH FIRST BY staff_id`** goes down each branch to the bottom before moving to the next branch ("depth first"), taking people with the same manager in `staff_id` order.
- **`SET visit_order`** names a new column that records that order. You don't show it; you sort by it with `ORDER BY visit_order`.
- **`SEARCH BREADTH FIRST BY staff_id`** would sort level by level instead, like the org chart query above.
- **`REPEAT('    ', level - 1)`** repeats four spaces once per level below the top, so each team is indented under its manager; `||` joins the spaces to the name.

Anita has 16 people below her plus herself: 17 rows. ✓ MySQL has neither `SEARCH` nor `CYCLE`; section 28.13 builds the same order with a sort path, which works in both databases.

---

## 28.3 Advanced window frames

Section 13.6 introduced frames and the trap of the default `RANGE` frame. This section completes the picture: the three frame types, frames measured in days, excluding rows, reusing window definitions, and the percentile functions.

### ROWS, RANGE, and GROUPS

A frame answers *"which rows around me count?"*, and there are three ways to measure "around":

| Frame type | Counts in units of | "1 PRECEDING" means |
|---|---|---|
| `ROWS` | physical rows | the one row before me |
| `GROUPS` | groups of rows with the same `ORDER BY` value | every row in the previous distinct value (a *peer group*) |
| `RANGE` | the `ORDER BY` value itself | every row whose value is within the offset of mine; on a date column the offset must be an interval, such as `INTERVAL '1 day'` |

The difference only shows when values repeat or have gaps. On 16, 17, and 20 February 2025, Riverstone received two orders each. Take the three frame types one at a time, starting with `ROWS`:

```sql
SELECT o.order_date,
       o.order_id,
       COUNT(*) OVER (ORDER BY o.order_date, o.order_id
                      ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS rows_in_frame
FROM orders AS o
WHERE o.order_date BETWEEN DATE '2025-02-14' AND DATE '2025-02-21'
ORDER BY o.order_date, o.order_id;
```

```
 order_date | order_id | rows_in_frame
------------+----------+---------------
 2025-02-16 |    10011 |             1
 2025-02-16 |    10012 |             2
 2025-02-17 |    10013 |             2
 2025-02-17 |    10014 |             2
 2025-02-20 |    10015 |             2
 2025-02-20 |    10016 |             2
(6 rows)
```

**Reading it:** `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW` counts the row before and this row: always 2 after the first row, whatever the dates. The window orders by `order_date, order_id`, so the order of two same-day orders is fixed; without `order_id`, which of them counts as "first" would be up to the database. The first row has no row before it, because **windows are calculated after `WHERE`**: the frame can't see rows the `WHERE` removed. (14 and 15 February had no orders anyway.)

Now add a `GROUPS` column beside it:

```sql
SELECT o.order_date,
       o.order_id,
       COUNT(*) OVER (ORDER BY o.order_date, o.order_id
                      ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)   AS rows_in_frame,
       COUNT(*) OVER (ORDER BY o.order_date
                      GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) AS rows_in_2_dates
FROM orders AS o
WHERE o.order_date BETWEEN DATE '2025-02-14' AND DATE '2025-02-21'
ORDER BY o.order_date, o.order_id;
```

```
 order_date | order_id | rows_in_frame | rows_in_2_dates
------------+----------+---------------+-----------------
 2025-02-16 |    10011 |             1 |               2
 2025-02-16 |    10012 |             2 |               2
 2025-02-17 |    10013 |             2 |               4
 2025-02-17 |    10014 |             2 |               4
 2025-02-20 |    10015 |             2 |               4
 2025-02-20 |    10016 |             2 |               4
(6 rows)
```

**Reading it:** rows with the same `ORDER BY` value are **peers**, and each set of peers is a **peer group**: here, one date's orders. This window orders by date alone, so that it has peers to count. `GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW` counts this date's peer group plus the previous one, the previous *date that has orders*. On 20 February that's 20 Feb and 17 Feb: 4 orders, even though 17 Feb is three days earlier.

Finally, `RANGE` with an interval. Three windows with three frames make a long `SELECT`, so name them with the `WINDOW` clause from section 13.6, where you named one window `w`. Each `OVER` then refers to a window by name:

```sql
SELECT o.order_date,
       o.order_id,
       COUNT(*) OVER w_rows   AS rows_in_frame,
       COUNT(*) OVER w_groups AS rows_in_2_dates,
       COUNT(*) OVER w_range  AS rows_in_2_days
FROM orders AS o
WHERE o.order_date BETWEEN DATE '2025-02-14' AND DATE '2025-02-21'
WINDOW w_rows   AS (ORDER BY o.order_date, o.order_id ROWS BETWEEN 1 PRECEDING AND CURRENT ROW),
       w_groups AS (ORDER BY o.order_date GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW),
       w_range  AS (ORDER BY o.order_date RANGE BETWEEN INTERVAL '1 day' PRECEDING AND CURRENT ROW)
ORDER BY o.order_date, o.order_id;
```

```
 order_date | order_id | rows_in_frame | rows_in_2_dates | rows_in_2_days
------------+----------+---------------+-----------------+----------------
 2025-02-16 |    10011 |             1 |               2 |              2
 2025-02-16 |    10012 |             2 |               2 |              2
 2025-02-17 |    10013 |             2 |               4 |              4
 2025-02-17 |    10014 |             2 |               4 |              4
 2025-02-20 |    10015 |             2 |               4 |              2
 2025-02-20 |    10016 |             2 |               4 |              2
(6 rows)
```

**Reading it:**

- The first two columns are unchanged: naming a window changes nothing about what it calculates. Several windows go in one `WINDOW` clause, separated by commas.
- **`RANGE BETWEEN INTERVAL '1 day' PRECEDING AND CURRENT ROW`** counts orders from yesterday and today, measured on the calendar. On 20 February, 19 February had no orders, so only today's 2 count. On 17 February, 16 February is exactly one day earlier: 4.
- On a date column, the offset must be an interval. Write `RANGE BETWEEN 1 PRECEDING …` and PostgreSQL refuses: *RANGE with offset PRECEDING/FOLLOWING is not supported for column type date and offset type integer*.

Use `ROWS` for "the last N records", `GROUPS` for "the last N distinct dates that had activity", and `RANGE` with an interval for "the last N calendar days". You can also extend a named window: `OVER (w ROWS BETWEEN …)` adds a frame to a window that defines only the partition and order. You'll use that in "FIRST_VALUE, LAST_VALUE, and the default frame" below.

### Calendar windows with RANGE and intervals

*"What was revenue over the last seven days, on each day we took orders?"* Riverstone doesn't take orders every day, so "the last seven rows" is not "the last seven days":

```sql
WITH daily AS (
    SELECT order_date, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE order_date BETWEEN DATE '2025-11-20' AND DATE '2025-12-10'
    GROUP BY order_date
)
SELECT order_date,
       ROUND(revenue) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY order_date
             ROWS BETWEEN 2 PRECEDING AND CURRENT ROW))                  AS last_3_rows,
       ROUND(SUM(revenue) OVER (ORDER BY order_date
             RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW)) AS last_7_days
FROM daily
ORDER BY order_date;
```

```
 order_date | revenue | last_3_rows | last_7_days
------------+---------+-------------+-------------
 2025-11-22 |   86615 |       86615 |       86615
 2025-11-23 |    2731 |       89346 |       89346
 2025-11-25 |   10213 |       99559 |       99559
 2025-11-26 |   10060 |       23004 |      109619
 2025-11-28 |   17200 |       37473 |      126819
 2025-12-01 |   71862 |       99122 |      109334
 2025-12-04 |    9809 |       98870 |       98870
 2025-12-05 |   13705 |       95375 |       95375
 2025-12-08 |   65818 |       89331 |       89331
 2025-12-10 |    7698 |       87221 |       97029
(10 rows)
```

Hand-check 26 November. The last three rows are 23, 25, and 26 November: ₹2,731 + ₹10,213 + ₹10,060 = ₹23,004. ✓ The last seven days run from 20 to 26 November, which includes the big ₹86,615 order on the 22nd: ₹86,615 + ₹2,731 + ₹10,213 + ₹10,060 = ₹1,09,619. ✓ On 1 December, the seven days (25 November to 1 December) include 25, 26, and 28 November and 1 December: ₹1,09,334. ✓

This is Chapter 13's date-spine problem (Pattern 5) solved without a spine: `RANGE` with an interval measures by the calendar, so missing days take care of themselves. Because the frame begins before the query's first date, the first few rows here only see part of their window, which is why 22 November shows a single order. In a real report, start the `WHERE` six days earlier and filter the output afterwards.

> **Dialect note.** PostgreSQL writes `INTERVAL '6 days'`; MySQL writes `INTERVAL 6 DAY`. MySQL supports `RANGE` with intervals but not `GROUPS` (section 28.13). SQL Server supports neither interval ranges nor `GROUPS`; there, use a date spine.

### Excluding the current row

*"Was this month unusual compared with the other months of its quarter?"* Comparing a month with an average that includes itself dilutes the comparison.

`EXCLUDE CURRENT ROW` leaves the month itself out:

```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month,
           SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY 1
)
SELECT month,
       ROUND(revenue) AS revenue,
       ROUND(AVG(revenue) OVER (
             PARTITION BY DATE_TRUNC('quarter', month)
             ORDER BY month
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
             EXCLUDE CURRENT ROW)) AS avg_other_months_in_quarter
FROM monthly
WHERE month >= DATE '2025-07-01'
ORDER BY month;
```

```
   month    | revenue | avg_other_months_in_quarter
------------+---------+-----------------------------
 2025-07-01 |  232692 |                      443798
 2025-08-01 |  329282 |                      395504
 2025-09-01 |  558315 |                      280987
 2025-10-01 |  681071 |                      536616
 2025-11-01 |  633408 |                      560447
 2025-12-01 |  439824 |                      657239
(6 rows)
```

September's ₹5,58,315 against the other two months of Q3 (₹2,32,692 and ₹3,29,282, averaging ₹2,80,987) shows the festive season starting in September, not October. (Check: (2,32,692 + 3,29,282) ÷ 2 = 2,80,987. ✓) `DATE_TRUNC('quarter', month)` works like the `'month'` version from Chapter 13: it returns the first day of the quarter, so each quarter's three months form one partition. `EXCLUDE` has four forms: `CURRENT ROW`, `GROUP` (the current row and its peers), `TIES` (the peers but not the current row), and `NO OTHERS` (the default). It is PostgreSQL only; MySQL has no `EXCLUDE` (section 28.13).

### FIRST_VALUE, LAST_VALUE, and the default frame

Chapter 13's mistakes table warned that `LAST_VALUE` with the default frame returns the current row. Here it is on Patel Kitchenware's orders, with the fix beside it:

```sql
WITH order_values AS (
    SELECT o.customer_id, o.order_id, o.order_date, SUM(sl.net_revenue) AS order_value
    FROM orders AS o
    JOIN sales_lines AS sl ON sl.order_id = o.order_id
    WHERE o.customer_id = 2               -- 2 = Patel Kitchenware
    GROUP BY o.customer_id, o.order_id, o.order_date
)
SELECT order_date,
       ROUND(order_value) AS order_value,
       ROUND(FIRST_VALUE(order_value) OVER w) AS first_order,
       ROUND(LAST_VALUE(order_value)  OVER w) AS last_value_default,
       ROUND(LAST_VALUE(order_value)  OVER (w ROWS BETWEEN UNBOUNDED PRECEDING
                                             AND UNBOUNDED FOLLOWING)) AS latest_order
FROM order_values
WINDOW w AS (PARTITION BY customer_id ORDER BY order_date, order_id)
ORDER BY order_date;
```

```
 order_date | order_value | first_order | last_value_default | latest_order
------------+-------------+-------------+--------------------+--------------
 2025-01-02 |        2900 |        2900 |               2900 |        39870
 2025-03-28 |       35138 |        2900 |              35138 |        39870
 2025-04-11 |       19825 |        2900 |              19825 |        39870
 2025-05-04 |       23650 |        2900 |              23650 |        39870
 2025-06-10 |       14155 |        2900 |              14155 |        39870
 2025-08-14 |       38610 |        2900 |              38610 |        39870
 2025-11-09 |       39870 |        2900 |              39870 |        39870
(7 rows)
```

With an `ORDER BY` and no frame, the frame ends at the current row, so "the last value in the frame" is always the current row: `last_value_default` copies `order_value`. Extending the frame to `UNBOUNDED FOLLOWING` gives the real latest order, ₹39,870 on 9 November. `FIRST_VALUE` works with the default frame because the frame always starts at the first row. `NTH_VALUE(order_value, 2)` gives the second order, with the same frame caution.

### Percentiles and quartiles

*"What's a typical order worth?"* Chapter 4 explained why the median is often more honest than the mean, Chapter 15 (section 15.5) used `PERCENTILE_CONT` for medians and quartiles, and Chapter 21 (section 21.3) added `PERCENTILE_DISC`. This is a recap, with a name for the family. Functions written with `WITHIN GROUP (ORDER BY …)` are called **ordered-set aggregates**: aggregates that need their input sorted first. Here are the mean, the median, and the 90th percentile of the year's order values:

```sql
WITH order_values AS (
    SELECT order_id, SUM(net_revenue) AS order_value
    FROM sales_lines
    GROUP BY order_id
)
SELECT COUNT(*)                AS orders,
       ROUND(AVG(order_value)) AS mean_value,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_value)::NUMERIC) AS median_value,
       ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY order_value)::NUMERIC) AS p90_value
FROM order_values;
```

```
 orders | mean_value | median_value | p90_value
--------+------------+--------------+-----------
    173 |      25061 |        21375 |     48334
(1 row)
```

There are 173 orders here, not the 175 of section 28.1, because `sales_lines` leaves out the two cancelled ones. The mean (₹25,061) is above the median (₹21,375), because a few large orders pull it up. One order in ten is worth more than ₹48,334. As in section 21.3, `::NUMERIC` converts the percentile before rounding: `PERCENTILE_CONT` returns a type (`double precision`) that `ROUND` accepts only without a number of decimals, and the cast keeps this query working if you later ask for `ROUND(…, 2)`.

The difference between the two percentile functions, on four numbers you can check by eye:

```sql
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x) AS cont_median,
       PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY x) AS disc_median
FROM (VALUES (10), (20), (30), (40)) AS v(x);
```

```
 cont_median | disc_median
-------------+-------------
          25 |          20
(1 row)
```

`PERCENTILE_CONT` interpolates between the two middle values, 20 and 30, and returns 25, a value that isn't in the data. `PERCENTILE_DISC` returns an actual value: the first one at or past the halfway mark, 20. These are aggregates, not window functions: in PostgreSQL they can't take `OVER`.

To put every order into a band instead, use the window function **`NTILE(n)`**, which Chapter 27 introduced (section 27.4). As a reminder, it splits the ordered rows into *n* groups as equal in size as possible and numbers them 1 to *n*:

```sql
WITH order_values AS (
    SELECT order_id, SUM(net_revenue) AS order_value
    FROM sales_lines
    GROUP BY order_id
),
banded AS (
    SELECT order_value, NTILE(4) OVER (ORDER BY order_value) AS quartile
    FROM order_values
)
SELECT quartile,
       COUNT(*)                AS orders,
       ROUND(MIN(order_value)) AS smallest,
       ROUND(MAX(order_value)) AS largest,
       ROUND(SUM(order_value)) AS revenue
FROM banded
GROUP BY quartile
ORDER BY quartile;
```

```
 quartile | orders | smallest | largest | revenue
----------+--------+----------+---------+---------
        1 |     44 |     1378 |   12355 |  307338
        2 |     43 |    12398 |   21375 |  716217
        3 |     43 |    21650 |   35138 | 1196060
        4 |     43 |    35300 |  100278 | 2115857
(4 rows)
```

173 orders don't divide by 4, so the first band gets the extra order (44 + 43 + 43 + 43 = 173 ✓). The revenue column tells the story: the largest quarter of orders brings ₹21,15,857, almost half of the year's ₹43,35,471 (48.8%), and the smallest quarter brings 7.1%. The bands add up to the year's total: 3,07,338 + 7,16,217 + 11,96,060 + 21,15,857 = 43,35,472, one rupee more than the total because each band was rounded separately. ✓

> **Watch out: NTILE splits by count, not by value.** If many orders have the same value, `NTILE` may put identical values into different bands, because it only cares about getting equal-sized groups. For value-based bands, compute the cut points with `PERCENTILE_CONT` and use `CASE`.

**Good place to stop.**

---

## 28.4 How a database finds rows

To speed up a query, you need a picture of what the database does with it. The picture is simpler than you might expect.

### Tables live in pages

PostgreSQL stores a table as a file divided into **pages** (also called blocks) of 8 KB each. Rows are packed into pages in roughly the order they were inserted, not in any useful order. `riverstone_perf`'s `orders` table is 41 MB, which is about 5,200 pages; `order_items` is about 101 MB. Reading pages from disk (or even from memory) is most of the work a query does, so the question behind every performance problem is: **how many pages did the database have to read to find the rows it needed?**

### Scanning

With no other help, the only way to find customer 2718's orders is a **sequential scan** (in PostgreSQL's plans, `Seq Scan`): read every page and check every row. For 714,285 orders, that's every one of them, to keep 40. It is slow when you want a few rows, but it isn't always wrong. To total *all* the year's revenue, reading everything is exactly the job, and a scan does it in the most efficient order.

### Indexes

An **index** is a separate structure that stores one column's values (or several columns') in sorted order, each with a pointer to where its row lives in the table. It works like the index at the back of a printed book: to find "grain", you don't read every page, you look it up and go straight to the right page.

The standard kind is the **B-tree** (balanced tree). Its top page, the root, divides the key range into a few hundred slices and points to a page for each; those pages divide their slices again, until the bottom **leaf** pages list individual values and row pointers. Because each page fans out into hundreds of children, even millions of values need only three or four levels. Finding customer 2718 means reading the root, a page or two below it, a leaf, and then the 40 table pages holding those rows.

![Two panels. Left: a grid of table rows scanned end to end, with two matching rows highlighted, labeled 714,285 rows checked and median 38.77 ms. Right: a B-tree from a root page through narrower key ranges down to a leaf containing 2718, leading to 40 row pointers, labeled median 0.18 ms](figures/fig28-3-scan-vs-index.svg)

*Figure 28.3 — The same question answered two ways. On the test machine the index made it about 200 times faster.*

### What indexes cost

Indexes aren't free, which is why databases don't index every column automatically:

- **Space.** The index on `orders.customer_id` takes 4,960 kB; the primary key index on `order_items` takes 41 MB, almost half the size of the table itself.
- **Slower writes.** Every `INSERT`, every `DELETE`, and every `UPDATE` of an indexed column must update each index too. Section 28.6 measures this.
- **Choices for the planner.** More indexes mean more plans to consider, and occasionally a poor choice.

A **primary key** always has an index, because the database needs one to enforce uniqueness. So does a `UNIQUE` constraint. Everything else is your decision.

> **Watch out: PostgreSQL does not index foreign keys for you.** Declaring `order_items.order_id REFERENCES orders(order_id)` creates a rule, not an index. Joins on that column, and every delete from `orders` (which must check for lines that still point at the order), then scan the whole `order_items` table. MySQL's InnoDB engine *does* create an index for each foreign key automatically. Section 28.13 shows the difference on real data.

---

## 28.5 Reading query plans with EXPLAIN

Chapter 12 (section 12.11) promised you'd see what the database actually does with a query. From here to the end of section 28.6, work in `riverstone_perf`, the database you built in section 28.1. Put **`EXPLAIN`** in front of any query, and PostgreSQL shows its **query plan**, the steps it has chosen, without running the query:

<!-- run: none -->
```sql
EXPLAIN
SELECT order_id, order_date, status
FROM orders
WHERE customer_id = 2718;
```

```
                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on orders  (cost=0.00..14149.56 rows=97 width=17)
   Filter: (customer_id = 2718)
(2 rows)
```

*(Customer 2718 is a typical customer, with 40 orders. There is no index on `customer_id` yet. The plans in sections 28.5 and 28.6 are copied from the recorded runs in `ch28_perf_log.txt`, because timings change on every run; the costs and row counts on your machine should match or come very close.)*

**Reading it:**

- **`Seq Scan on orders`**: the step, a sequential scan of the whole table.
- **`Filter: (customer_id = 2718)`**: the condition checked on each row as it's read.
- **`cost=0.00..14149.56`**: the planner's *estimate* of effort, in arbitrary units (roughly, the cost of reading one page in order is 1). The first number is the cost before the first row can be returned; the second is the cost to return all rows. Costs let the planner compare plans. They are not milliseconds.
- **`rows=97`**: the estimated number of rows returned. The planner guesses from **statistics** it keeps about each column (how many distinct values, which are most common), refreshed by `ANALYZE`. The real answer is 40, so the estimate is in the right neighborhood.
- **`width=17`**: the estimated average size of each row in bytes.

### EXPLAIN ANALYZE: run it and measure

**`EXPLAIN ANALYZE`** runs the query for real and adds what actually happened. Options go in brackets after `EXPLAIN`; the option `COSTS OFF` hides the estimates to keep lines short:

<!-- run: none -->
```sql
EXPLAIN (ANALYZE, COSTS OFF)
SELECT order_id, order_date, status
FROM orders
WHERE customer_id = 2718;
```

```
                           QUERY PLAN
----------------------------------------------------------------
 Seq Scan on orders (actual time=1.051..47.426 rows=40 loops=1)
   Filter: (customer_id = 2718)
   Rows Removed by Filter: 714245
 Planning Time: 0.260 ms
 Execution Time: 47.479 ms
(5 rows)
```

- **`actual time=1.051..47.426`**: milliseconds until the first row, and until the last row.
- **`rows=40 loops=1`**: rows actually returned, and how many times this step ran.
- **`Rows Removed by Filter: 714245`**: the tell-tale sign. The database read 714,285 rows to keep 40. When you see a filter throwing away almost everything, an index on the filtered column is the first thing to consider.
- **`Planning Time`**: the time spent choosing the plan, before anything ran.
- **`Execution Time`**: the whole query, 47.5 ms on this run. Across seven runs the median was 38.77 ms.

> **Watch out: EXPLAIN ANALYZE really runs the statement.** `EXPLAIN ANALYZE DELETE FROM orders …` deletes the rows. To measure a change safely, wrap it: `BEGIN; EXPLAIN ANALYZE …; ROLLBACK;`.

Now create an index and ask again:

<!-- run: none -->
```sql
CREATE INDEX idx_orders_customer_id ON orders (customer_id);

EXPLAIN (ANALYZE, COSTS OFF)
SELECT order_id, order_date, status
FROM orders
WHERE customer_id = 2718;
```

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Bitmap Heap Scan on orders (actual time=0.023..0.132 rows=40 loops=1)
   Recheck Cond: (customer_id = 2718)
   Heap Blocks: exact=40
   ->  Bitmap Index Scan on idx_orders_customer_id (actual time=0.010..0.011 rows=40 loops=1)
         Index Cond: (customer_id = 2718)
 Planning Time: 0.303 ms
 Execution Time: 0.179 ms
(7 rows)
```

Building the index took about a quarter of a second. The query's median fell from 38.77 ms to 0.18 ms. **Read plans from the most indented line outwards**: the innermost step runs first and feeds the one above it.

- **`Bitmap Index Scan`** reads the index and collects the locations of the 40 matching rows. **`Index Cond`** is the condition the index answered.
- **`Bitmap Heap Scan`** then visits those locations in page order. (The *heap* is PostgreSQL's name for the table's own pages.) **`Heap Blocks: exact=40`** says it read 40 table pages: this customer's orders are scattered, one per page.
- **`Recheck Cond`** is the condition the heap scan would check again on each row if memory ran short. Then the bitmap remembers only *which pages* to read, not which rows (PostgreSQL calls that *lossy*), and every row on those pages must be rechecked. `exact=40` means every location was exact, so no rechecking was needed.

### The planner chooses, and it can say no

PostgreSQL has several ways to use an index, and chooses by estimated cost:

| Plan node | What it does | Typical when |
|---|---|---|
| `Seq Scan` | reads every page | most rows are needed, or no useful index |
| `Index Scan` | walks the index, fetching each row as it goes | few rows, or rows wanted in index order |
| `Bitmap Index Scan` + `Bitmap Heap Scan` | collects all matching locations first, then reads pages in order | a moderate number of rows |
| `Index Only Scan` | answers from the index alone, never touching the table | every column needed is in the index |

Try the customer with the most orders, customer 4534, who has 23,526 of them:

<!-- run: none -->
```sql
EXPLAIN (ANALYZE, COSTS OFF)
SELECT order_id, order_date, status
FROM orders
WHERE customer_id = 4534;
```

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Bitmap Heap Scan on orders (actual time=1.851..14.610 rows=23526 loops=1)
   Recheck Cond: (customer_id = 4534)
   Heap Blocks: exact=5170
   ->  Bitmap Index Scan on idx_orders_customer_id (actual time=1.123..1.124 rows=23526 loops=1)
         Index Cond: (customer_id = 4534)
 Planning Time: 0.319 ms
 Execution Time: 15.571 ms
(7 rows)
```

The same index is used, but `Heap Blocks: exact=5170` says it read 5,170 of the table's 5,221 pages, because this customer has an order on almost every page. The median was 15.26 ms. And for a condition that matches almost everything, the planner ignores the index entirely, even when one exists:

<!-- run: none -->
```sql
EXPLAIN
SELECT order_id FROM orders WHERE status = 'Delivered';
```

```
                          QUERY PLAN
---------------------------------------------------------------
 Seq Scan on orders  (cost=0.00..14149.56 rows=688214 width=4)
   Filter: ((status)::text = 'Delivered'::text)
(2 rows)
```

(PostgreSQL prints the column and the text it's compared with as type `text`, with `::text`; that's how it displays the comparison, not something you wrote.) 689,050 of the 714,285 orders are delivered (96.5%). Jumping from an index to a table page 689,050 times would be slower than reading the table from start to end, and the planner knows it from its statistics. **An index helps when a condition is selective**, meaning it keeps a small fraction of rows.

### Joins in a plan

Plans for joins have one more thing to read: the **join method**. Here's *"customer 2718's total revenue"*, which joins orders to their lines. `order_items.order_id` has no index yet:

<!-- run: none -->
```sql
EXPLAIN (ANALYZE, COSTS OFF)
SELECT SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS net_revenue
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
WHERE o.customer_id = 2718;
```

Figure 28.4 shows its plan, with the steps numbered in the order they run.

![An EXPLAIN ANALYZE plan with numbered callouts: 1, a bitmap index scan finds 40 orders; 2, their ids go into a hash; 3, a sequential scan reads all 1,926,847 order lines in 142 ms; 4, the hash join keeps 108 of them; 5, the aggregate at the top finishes at 285 ms](figures/fig28-4-reading-a-plan.svg)

*Figure 28.4 — Read the plan from the inside out, and look for the step where the time jumps. (One run; the median of seven was 262.47 ms.)*

PostgreSQL uses three join methods:

- **Nested loop**: for each row on one side, look up matches on the other. Excellent when one side is small *and* the other side has an index on the join column. Disastrous when the other side must be scanned each time.
- **Hash join**: load the smaller side into an in-memory hash table, then scan the larger side once, probing the table. Good for large, unindexed joins. That's what Figure 28.4 shows: the planner had no index to look lines up by `order_id`, so it scanned all 1.9 million lines to find 108.
- **Merge join**: sort both sides on the join key, then walk them together. Good when both sides are already sorted, for example by an index.

You don't choose the method; the planner does. Your job is to give it the indexes that make the cheap methods possible, and then check that it used them.

> **Try it.** Run `EXPLAIN SELECT * FROM sales_lines;` in `riverstone_2025`. A view is replaced by its query before planning, so the plan shows the joins inside `sales_lines`. With tables this small you'll mostly see sequential scans and a hash join, and that's the right choice: reading a few pages whole is cheaper than using an index.

---

## 28.6 Indexes in practice

This section runs six experiments on `riverstone_perf`. Each one starts from a question, measures it, changes one thing, and measures again. Run them in order: each experiment keeps the indexes the earlier ones created, as a real database would. The table at the end collects the results.

### 1. Index the foreign keys you join on

The query from Figure 28.4, unchanged, run after one new index:

<!-- run: none -->
```sql
CREATE INDEX idx_order_items_order_id ON order_items (order_id);

EXPLAIN (ANALYZE, COSTS OFF)
SELECT SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS net_revenue
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
WHERE o.customer_id = 2718;
```

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Aggregate (actual time=0.541..0.541 rows=1 loops=1)
   ->  Nested Loop (actual time=0.050..0.468 rows=108 loops=1)
         ->  Bitmap Heap Scan on orders o (actual time=0.027..0.132 rows=40 loops=1)
               Recheck Cond: (customer_id = 2718)
               Heap Blocks: exact=40
               ->  Bitmap Index Scan on idx_orders_customer_id (actual time=0.017..0.017 rows=40 loops=1)
                     Index Cond: (customer_id = 2718)
         ->  Index Scan using idx_order_items_order_id on order_items oi (actual time=0.007..0.008 rows=3 loops=40)
               Index Cond: (order_id = o.order_id)
 Planning Time: 0.798 ms
 Execution Time: 0.601 ms
(11 rows)
```

The median fell from 262.47 ms to 0.64 ms. The join method changed from a hash join to a **nested loop**: for each of the 40 orders (`loops=40`), look up its lines in the new index, about 3 lines each (40 × 3 is close to the 108 lines found; `rows=3` is a rounded average).

The same index serves a simpler question that a screen in an order-entry system asks thousands of times a day, *"show me one order's lines"*:

<!-- run: none -->
```sql
EXPLAIN (ANALYZE, COSTS OFF)
SELECT order_item_id, product_id, quantity
FROM order_items
WHERE order_id = 500000;
```

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Index Scan using idx_order_items_order_id on order_items (actual time=0.023..0.023 rows=1 loops=1)
   Index Cond: (order_id = 500000)
 Planning Time: 0.283 ms
 Execution Time: 0.053 ms
(4 rows)
```

Before the index, the same query was a `Seq Scan` that removed 1,926,846 rows to keep 1, with a median of 109.78 ms. With it, the median is 0.06 ms.

**The rule:** in PostgreSQL, index every foreign key column that you join on or delete through. It's the single most common missing index.

### 2. Don't wrap the indexed column in a function

*"How many orders came in December 2025?"* First give `order_date` an index:

<!-- run: none -->
```sql
CREATE INDEX idx_orders_order_date ON orders (order_date);
```

Now two ways to write the filter, each with its plan:

<!-- run: none -->
```sql
-- version A: extract parts of the date
EXPLAIN (ANALYZE, COSTS OFF)
SELECT COUNT(*) FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2025 AND EXTRACT(MONTH FROM order_date) = 12;

-- version B: a date range
EXPLAIN (ANALYZE, COSTS OFF)
SELECT COUNT(*) FROM orders
WHERE order_date >= DATE '2025-12-01' AND order_date < DATE '2026-01-01';
```

Without `EXPLAIN`, both return 25,078. Their plans are very different. Version A's plan:

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Aggregate (actual time=131.698..131.701 rows=1 loops=1)
   ->  Seq Scan on orders (actual time=123.024..130.388 rows=25078 loops=1)
         Filter: ((EXTRACT(year FROM order_date) = '2025'::numeric) AND (EXTRACT(month FROM order_date) = '12'::numeric))
         Rows Removed by Filter: 689207
 Planning Time: 0.432 ms
 Execution Time: 131.749 ms
(6 rows)
```

Version B's plan:

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Aggregate (actual time=2.797..2.797 rows=1 loops=1)
   ->  Index Only Scan using idx_orders_order_date on orders (actual time=0.021..1.672 rows=25078 loops=1)
         Index Cond: ((order_date >= '2025-12-01'::date) AND (order_date < '2026-01-01'::date))
         Heap Fetches: 0
 Planning Time: 0.383 ms
 Execution Time: 2.834 ms
(6 rows)
```

- **Version A** scans the whole table (median 131.33 ms), although the index exists.
- **Version B** uses the index (median 2.95 ms), about 45 times faster. It's an **`Index Only Scan`**: `COUNT(*)` needs no column values, so the index alone answers it. **`Heap Fetches: 0`** means no table page was visited; experiment 4 explains when that's possible.

The index stores dates sorted, so it can find "from 1 December up to (but not including) 1 January" directly. It does not store "the month part of each date", so it can't help with `EXTRACT(MONTH …) = 12`. A condition the database can answer from an index is called **sargable** (from *search argument*).

The same trap appears in many disguises. Each pair below returns the same rows, but only the second form can use a plain index on the column:

| Not sargable (the condition after `WHERE`) | Sargable |
|---|---|
| `EXTRACT(YEAR FROM order_date) = 2025` | `order_date >= '2025-01-01'` `AND order_date < '2026-01-01'` |
| `order_date::text LIKE '2025-12%'` | the date range above |
| `UPPER(city) = 'PUNE'` | store city in one agreed case, then `city = 'Pune'` |
| `quantity * unit_price > 50000` | often unavoidable; see *expression indexes* below |
| `customer_name LIKE '%Hardware'` | `LIKE 'Sharma%'` can use an index; a leading `%` can't |

The half-open range (`>=` the start, `<` the next start) is also the correct form for timestamps, which `BETWEEN … AND '2025-12-31'` gets wrong by missing everything after midnight on the 31st (section 12.6's warning).

If a function in the filter is truly needed, you can index the expression itself, an **expression index**. In PostgreSQL: `CREATE INDEX idx_customers_upper_city ON customers (UPPER(city));`. MySQL (8.0.13 and later) needs an extra pair of brackets around the expression: `CREATE INDEX idx_customers_upper_city ON customers ((UPPER(city)));`. Either way, the query must then use exactly the same expression.

### 3. Composite indexes: order matters

*"Customer 4534's orders since 1 January 2025."* This filters on two columns. With the indexes you have so far (one on `customer_id`, one on `order_date`), here's the plan:

<!-- run: none -->
```sql
EXPLAIN (ANALYZE, COSTS OFF)
SELECT order_date, status
FROM orders
WHERE customer_id = 4534 AND order_date >= DATE '2025-01-01';
```

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Bitmap Heap Scan on orders (actual time=10.308..16.677 rows=9301 loops=1)
   Recheck Cond: (customer_id = 4534)
   Filter: (order_date >= '2025-01-01'::date)
   Rows Removed by Filter: 14225
   Heap Blocks: exact=5170
   ->  Bitmap Index Scan on idx_orders_customer_id (actual time=1.513..1.513 rows=23526 loops=1)
         Index Cond: (customer_id = 4534)
 Planning Time: 0.400 ms
 Execution Time: 17.093 ms
(9 rows)
```

The index finds all 23,526 of the customer's orders; the table pages are then read and each order's date checked, and 14,225 are thrown away (23,526 − 9,301). A **composite index** stores several columns sorted together, like a phone book sorted by surname and then first name:

<!-- run: none -->
```sql
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_date);
```

The same `EXPLAIN` now gives:

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Bitmap Heap Scan on orders (actual time=0.786..7.325 rows=9301 loops=1)
   Recheck Cond: ((customer_id = 4534) AND (order_date >= '2025-01-01'::date))
   Heap Blocks: exact=2047
   ->  Bitmap Index Scan on idx_orders_customer_date (actual time=0.516..0.517 rows=9301 loops=1)
         Index Cond: ((customer_id = 4534) AND (order_date >= '2025-01-01'::date))
 Planning Time: 0.399 ms
 Execution Time: 7.776 ms
(7 rows)
```

Both conditions are now in the `Index Cond`, there's no `Filter` line, and only the 9,301 matching orders are fetched, from 2,047 pages instead of 5,170. The median fell from 16.15 ms to 7.78 ms. (For a typical customer such as 2718, with 40 orders, the saving is tiny: the index lets you skip 28 unwanted rows.)

The column order decides which questions an index can answer. An index on `(customer_id, order_date)` is sorted by customer first:

- ✓ `WHERE customer_id = 4534` (the first column alone).
- ✓ `WHERE customer_id = 4534 AND order_date >= '2025-01-01'` (equality on the first, range on the second).
- ✓ `WHERE customer_id = 4534 ORDER BY order_date DESC LIMIT 5` (the rows are already in date order within the customer).
- ✗ `WHERE order_date >= '2025-12-01'` on its own. The dates are sorted *within each customer*, not overall, like trying to find everyone named Priya in a phone book sorted by surname.

The usual guideline: put columns you test with `=` first, and a column you test with a range (`>=`, `<`, `BETWEEN`) last.

> **Watch out: extra indexes are often redundant.** Once `(customer_id, order_date)` exists, a separate index on `customer_id` alone is almost never needed, because the composite index answers the same lookups. Dropping the redundant one saves space and speeds up writes.

### 4. Covering indexes: never touch the table

The query in experiment 3 still read 2,047 table pages, only to fetch `status`. If every column a query needs is inside the index, the database can skip the table altogether. PostgreSQL lets you carry extra columns in an index without sorting by them, using `INCLUDE`. The new index answers everything the plain composite one did, so it replaces it:

<!-- run: none -->
```sql
DROP INDEX idx_orders_customer_date;

CREATE INDEX idx_orders_customer_date_incl
    ON orders (customer_id, order_date) INCLUDE (status);
VACUUM ANALYZE orders;

EXPLAIN (ANALYZE, COSTS OFF)
SELECT order_date, status
FROM orders
WHERE customer_id = 4534 AND order_date >= DATE '2025-01-01';
```

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Index Only Scan using idx_orders_customer_date_incl on orders (actual time=0.032..1.029 rows=9301 loops=1)
   Index Cond: ((customer_id = 4534) AND (order_date >= '2025-01-01'::date))
   Heap Fetches: 0
 Planning Time: 0.363 ms
 Execution Time: 1.374 ms
(5 rows)
```

**`Index Only Scan`** with **`Heap Fetches: 0`**: all 9,301 rows came from the index. The median fell from 7.78 ms (composite index, reading 2,047 table pages) to 1.68 ms. The `VACUUM` matters: PostgreSQL can only skip a table page if it knows every row on it is visible to everyone, and `VACUUM` records that. On a busy table, autovacuum does this in the background.

A covering index is a strong tool for one important, frequent query. It's a poor default, because every included column makes the index bigger.

### 5. Partial indexes: index only the rows you ask about

The warehouse screen asks one question all day: *"Which orders are still pending, oldest first?"* Only 3,930 of 714,285 orders are pending. Without help, the plan scans all 714,285 orders, removes 710,355 of them, and sorts the rest: a median of 44.12 ms. An index on `status` would mostly store the word *Delivered*. A **partial index** stores only the rows that match its `WHERE`:

<!-- run: none -->
```sql
CREATE INDEX idx_orders_pending ON orders (order_date) WHERE status = 'Pending';

EXPLAIN (ANALYZE, COSTS OFF)
SELECT order_id, customer_id, order_date
FROM orders
WHERE status = 'Pending'
ORDER BY order_date;
```

```
                                        QUERY PLAN
------------------------------------------------------------------------------------------
 Index Scan using idx_orders_pending on orders (actual time=0.015..0.596 rows=3930 loops=1)
 Planning Time: 0.404 ms
 Execution Time: 0.746 ms
(3 rows)
```

The median fell from 44.12 ms to 0.75 ms, and the plan has no sort step because the index already stores the pending orders in date order. There's no `Index Cond` or `Filter` line either: every entry in a partial index already satisfies `status = 'Pending'`, so the planner has nothing left to check. The query's `WHERE` must imply the index's `WHERE`, or the index can't be used. The index is 48 kB, against 5,056 kB for the index on all order dates. As orders move from Pending to Shipped, they drop out of the index automatically. MySQL has no partial indexes (section 28.13).

### 6. Measure what indexes cost on writes

*"How much slower do writes get?"* Copy the first 500,000 order lines into two empty tables: one with no indexes at all, and one with four. `CREATE TABLE … (LIKE order_items)` makes an empty table with the same columns; `INCLUDING INDEXES` also copies `order_items`' two indexes (its primary key and `idx_order_items_order_id` from experiment 1), and two more are added:

<!-- run: none -->
```sql
CREATE TABLE oi_copy_0 (LIKE order_items);
CREATE TABLE oi_copy_4 (LIKE order_items INCLUDING INDEXES);
CREATE INDEX ON oi_copy_4 (product_id);
CREATE INDEX ON oi_copy_4 (order_id, product_id);

INSERT INTO oi_copy_0 SELECT * FROM order_items WHERE order_item_id <= 500000;
INSERT INTO oi_copy_4 SELECT * FROM order_items WHERE order_item_id <= 500000;
```

`CREATE INDEX ON` with no name lets PostgreSQL choose one. Time each `INSERT` (DBeaver shows the time under the results; `ch28_perf.py` repeats the whole thing three times). The medians of three rounds:

| Table | Median time to insert 500,000 rows |
|---|---|
| `oi_copy_0`, no indexes | 416 ms |
| `oi_copy_4`, four indexes (primary key, `order_id`, `product_id`, `(order_id, product_id)`) | 2,301 ms |

About five and a half times slower. Each index is a sorted structure that must be updated for every row. That's why data loads often **drop indexes, load, and recreate them**, and why "add an index for every column someone might filter on" is bad advice for a table that receives thousands of writes a minute. Drop the copies when you're done: `DROP TABLE oi_copy_0, oi_copy_4;`.

### The experiments in one table

| Question (riverstone_perf) | Before | After | Change made |
|---|---|---|---|
| One customer's orders (40 rows) | 38.77 ms | 0.18 ms | index on `orders.customer_id` |
| One customer's revenue (join) | 262.47 ms | 0.64 ms | index on `order_items.order_id` |
| One order's lines | 109.78 ms | 0.06 ms | same index |
| December's order count | 131.33 ms | 2.95 ms | rewrote `EXTRACT` as a date range |
| Big customer's 2025 orders | 16.15 ms | 7.78 ms | composite index `(customer_id, order_date)` |
| Big customer's 2025 orders | 7.78 ms | 1.68 ms | covering index with `INCLUDE (status)` |
| Pending orders, oldest first | 44.12 ms | 0.75 ms | partial index |
| Insert 500,000 lines | 416 ms | 2,301 ms | four indexes (the cost) |

### A checklist for a slow query

1. **Confirm it's the query.** Time it in DBeaver, which shows the execution time under the results (in `psql`, type `\timing on` first). A slow dashboard can be slow for reasons outside the database.
2. **Run `EXPLAIN (ANALYZE, BUFFERS)`** on a copy of production-sized data. `BUFFERS` adds how many pages each step read (see the example below the list).
3. **Find the expensive step**: where the time jumps, where `Rows Removed by Filter` is huge, where estimated and actual rows differ by ten times or more.
4. **Estimates far off?** Run `ANALYZE table_name` so the statistics are current, then plan again.
5. **Scan with a selective filter?** Check the filter is sargable; then consider an index (composite if several columns).
6. **Big join without an index on the join column?** Index the foreign key.
7. **Still slow because the question itself reads millions of rows?** No index will fix that. Pre-aggregate (section 28.11).
8. **Measure again**, and write down the before and after. Then check that writes to the table haven't become a problem.

Here is what `BUFFERS` adds, on section 28.5's first query as it ran before `idx_orders_customer_id` existed (recorded output):

<!-- run: none -->
```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF)
SELECT order_id, order_date, status
FROM orders
WHERE customer_id = 2718;
```

```
                           QUERY PLAN
----------------------------------------------------------------
 Seq Scan on orders (actual time=0.763..41.560 rows=40 loops=1)
   Filter: (customer_id = 2718)
   Rows Removed by Filter: 714245
   Buffers: shared hit=2421 read=2800
 Planning:
   Buffers: shared hit=69
 Planning Time: 0.255 ms
 Execution Time: 41.611 ms
(8 rows)
```

**`Buffers: shared hit=2421 read=2800`** counts pages: 2,421 were already in PostgreSQL's memory (**hit**), and 2,800 had to be fetched from outside it, from the operating system or the disk (**read**). Together, 5,221: every page of the table. After the index, the same query touched 43 pages (`shared hit=43`). The `Planning:` lines count the pages read while choosing the plan. Run the query twice and the `read` number usually drops, because the first run left the pages in memory; that's one reason to take the median of several runs.

> **Real-life example: the index that took down checkout.** A common story: an analyst notices a slow report and adds an index on a busy production table in the middle of the day. In PostgreSQL, a plain `CREATE INDEX` blocks inserts and updates to the table until it finishes, so on a very large table, orders stop being saved for minutes. `CREATE INDEX CONCURRENTLY` builds the index without blocking writes (slower, and it can't run inside a transaction). Changes to production tables go through a reviewed migration (section 28.12), not a query window.

**Good place to stop.**

---

## 28.7 Normalization, worked properly

Chapter 12 (section 12.1) gave you the intuition: **store each fact once, and link to it.** Normalization turns that intuition into rules you can check, called **normal forms**. Each form removes one kind of problem. You'll take one messy table all the way through the first three, in the lab database.

### The starting point: an order sheet

Before Riverstone's order entry was cleaned up, someone kept a tracking sheet of January's orders like this. It's a table in the lab, built from real orders in the one-year database. Start the lab afresh. Run these two lines from your `riverstone_2025` connection, not from a lab connection, because PostgreSQL refuses to drop the database you're connected to:

<!-- lab:start -->

```sql
DROP DATABASE IF EXISTS riverstone_lab;
CREATE DATABASE riverstone_lab;
```

If PostgreSQL answers *database "riverstone_lab" is being accessed by other users*, DBeaver still has Chapter 12's lab connection open: right-click that connection → *Disconnect*, and run the two lines again. (PostgreSQL 13 and later also accept `DROP DATABASE IF EXISTS riverstone_lab WITH (FORCE);`, which closes other connections first.)

Then connect to the new database: in DBeaver, edit your lab connection (or create one) so its *Database* is `riverstone_lab`, as in section 12.13, and open an SQL editor on it. (In `psql`, the same switch is `\c riverstone_lab`.) Now build the order sheet:

```sql
CREATE TABLE order_sheet (
    order_id    INTEGER,
    order_date  DATE,
    customer    VARCHAR(100),
    city        VARCHAR(50),
    sales_rep   VARCHAR(100),
    products    VARCHAR(300)
);

INSERT INTO order_sheet VALUES
(10001, '2025-01-02', 'Patel Kitchenware', 'Ahmedabad', 'Neha Kulkarni', '108 Stackable Bin x10 @290'),
(10002, '2025-01-05', 'Green Leaf Hotels', 'Pune',      'Farah Khan',    '107 Lunch Box Set x55 @380'),
(10005, '2025-01-20', 'Green Leaf Hotels', 'Pune',      'Farah Khan',    '101 Storage Box 10L x15 @430 less 5%'),
(10006, '2025-01-21', 'Coastal Foods',     'Chennai',   'Rahul Mehta',   '102 Storage Box 25L x25 @750 less 5%'),
(10007, '2025-01-24', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', '101 Storage Box 10L x45 @430; 102 Storage Box 25L x20 @750; 108 Stackable Bin x20 @290'),
(10008, '2025-01-26', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', '101 Storage Box 10L x30 @430; 102 Storage Box 25L x25 @750; 107 Lunch Box Set x25 @380');
```

It's readable, and for a person it works. For a database it's a dead end. You can count the orders that mention a product:

```sql
SELECT COUNT(*) AS storage_box_10l_orders
FROM order_sheet
WHERE products LIKE '%Storage Box 10L%';
```

```
 storage_box_10l_orders
------------------------
                      3
(1 row)
```

But you can't add up how many Storage Boxes were ordered, or the value of the orders, without taking the text apart. And the `LIKE` is fragile: an order typed as "Storage box 10 L" would be missed.

### First normal form (1NF): one value per cell

A table is in **first normal form** when:

1. every cell holds a **single value** (no lists, no "x45 @430" packed into text), and
2. every row is **unique**, identified by a key.

The `products` column breaks rule 1: it holds a list of order lines, each with four facts (product, quantity, price, discount). The fix is one row per order line, with each fact in its own column:

```sql
CREATE TABLE order_lines_1nf (
    order_id      INTEGER,
    order_date    DATE,
    customer      VARCHAR(100),
    city          VARCHAR(50),
    sales_rep     VARCHAR(100),
    product_id    INTEGER,
    product_name  VARCHAR(100),
    quantity      INTEGER,
    unit_price    NUMERIC(10,2),
    discount_pct  NUMERIC(5,2),
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO order_lines_1nf VALUES
(10001, '2025-01-02', 'Patel Kitchenware', 'Ahmedabad', 'Neha Kulkarni', 108, 'Stackable Bin',   10, 290, 0),
(10002, '2025-01-05', 'Green Leaf Hotels', 'Pune',      'Farah Khan',    107, 'Lunch Box Set',   55, 380, 0),
(10005, '2025-01-20', 'Green Leaf Hotels', 'Pune',      'Farah Khan',    101, 'Storage Box 10L', 15, 430, 5),
(10006, '2025-01-21', 'Coastal Foods',     'Chennai',   'Rahul Mehta',   102, 'Storage Box 25L', 25, 750, 5),
(10007, '2025-01-24', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 101, 'Storage Box 10L', 45, 430, 0),
(10007, '2025-01-24', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 102, 'Storage Box 25L', 20, 750, 0),
(10007, '2025-01-24', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 108, 'Stackable Bin',   20, 290, 0),
(10008, '2025-01-26', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 101, 'Storage Box 10L', 30, 430, 0),
(10008, '2025-01-26', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 102, 'Storage Box 25L', 25, 750, 0),
(10008, '2025-01-26', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 107, 'Lunch Box Set',   25, 380, 0);
```

The key is `(order_id, product_id)`: one order can have many products, and a product appears once per order. Now arithmetic works:

```sql
SELECT COUNT(DISTINCT order_id) AS storage_box_10l_orders,
       SUM(quantity)            AS units
FROM order_lines_1nf
WHERE product_id = 101;
```

```
 storage_box_10l_orders | units
------------------------+-------
                      3 |    90
(1 row)
```

(15 + 45 + 30 = 90 units. ✓) Most tables you meet in databases are already in 1NF. You'll meet data that breaks it (sometimes called 0NF) mainly in spreadsheets, form exports, and JSON.

### The anomalies 1NF still allows

Look at what `order_lines_1nf` repeats: Sharma Hardware's city is stored on six rows, and "Storage Box 10L" is spelled out three times. Section 12.1 named the three problems this causes. Here's the first one, happening:

```sql
UPDATE order_lines_1nf
SET city = 'Thane'
WHERE order_id = 10008 AND product_id = 101;

SELECT customer, city, COUNT(*) AS lines
FROM order_lines_1nf
WHERE customer = 'Sharma Hardware'
GROUP BY customer, city;
```

```
    customer     |  city  | lines
-----------------+--------+-------
 Sharma Hardware | Mumbai |     5
 Sharma Hardware | Thane  |     1
(2 rows)
```

An **update anomaly**: someone corrected the city on one row, and now the same customer is in two cities. Nothing in the table's design prevents it. The other two are the **insert anomaly** (you can't record a new product until someone orders it, because the product has nowhere to live without an order line) and the **delete anomaly** (delete Patel Kitchenware's only order, and you lose the fact that they're in Ahmedabad).

### Second normal form (2NF): every column depends on the whole key

To find the cause, ask of each column: **what does it depend on?** A column **depends on** another (a **functional dependency**, written `A → B`) when knowing A tells you B.

- `order_date`, `customer`, `city`, `sales_rep` depend on `order_id` alone. Order 10007 has one date, whichever product you look at.
- `product_name` depends on `product_id` alone.
- `quantity`, `unit_price`, `discount_pct` depend on **both**: they describe one product within one order.

A table is in **second normal form** when it's in 1NF and **no column depends on only part of a composite key**. `order_lines_1nf` has **partial dependencies** (on `order_id` alone, and on `product_id` alone), so it isn't. The fix is to give each group of facts a table keyed by what it depends on:

```sql
UPDATE order_lines_1nf SET city = 'Mumbai' WHERE order_id = 10008;

CREATE TABLE orders_2nf AS
SELECT DISTINCT order_id, order_date, customer, city, sales_rep
FROM order_lines_1nf;

CREATE TABLE products_2nf AS
SELECT DISTINCT product_id, product_name
FROM order_lines_1nf;

CREATE TABLE order_lines_2nf AS
SELECT order_id, product_id, quantity, unit_price, discount_pct
FROM order_lines_1nf;

SELECT 'orders' AS table_name, COUNT(*) AS row_count FROM orders_2nf
UNION ALL SELECT 'products', COUNT(*) FROM products_2nf
UNION ALL SELECT 'order_lines', COUNT(*) FROM order_lines_2nf;
```

```
 table_name  | row_count
-------------+-----------
 orders      |         6
 products    |         4
 order_lines |        10
(3 rows)
```

(The first line undoes the bad update, so the split starts from clean data. `CREATE TABLE … AS SELECT` copies the data but not keys; in a real design you'd add `PRIMARY KEY` and `REFERENCES` constraints, as Chapter 12 did.)

Six orders, four products, ten order lines. A product's name is now stored once, and a product can exist before anyone orders it.

> **Watch out: unit_price is not a partial dependency here.** It's tempting to move `unit_price` to the products table, because every product has a price. But the price *charged on an order* is a fact about that order line: next year's list price will change, and last year's orders must keep what the customer actually paid. The list price belongs in `products`; the charged price belongs in `order_lines`. Riverstone's real tables do exactly this. Normalization is about what the data *means*, which the column names alone won't tell you.

### Third normal form (3NF): no column depends on another non-key column

`orders_2nf` still stores `city` on every order. City depends on `order_id`, but only *through* the customer: `order_id → customer → city`. That's a **transitive dependency**. A table is in **third normal form** when it's in 2NF and **no non-key column depends on another non-key column**. A common way to remember 2NF and 3NF together: every non-key column must depend on *the key, the whole key, and nothing but the key*.

Move the customer's facts into their own table, with a **surrogate key** (an id with no business meaning, created only to identify the row), and keep only the id on the order:

```sql
CREATE TABLE customers_3nf (
    customer_id  INTEGER PRIMARY KEY,
    customer     VARCHAR(100) NOT NULL UNIQUE,
    city         VARCHAR(50)
);

INSERT INTO customers_3nf
SELECT ROW_NUMBER() OVER (ORDER BY customer), customer, city
FROM (SELECT DISTINCT customer, city FROM orders_2nf) AS c;

CREATE TABLE orders_3nf AS
SELECT o.order_id, o.order_date, c.customer_id, o.sales_rep
FROM orders_2nf AS o
JOIN customers_3nf AS c ON c.customer = o.customer;

SELECT * FROM customers_3nf ORDER BY customer_id;
```

```
 customer_id |     customer      |   city
-------------+-------------------+-----------
           1 | Coastal Foods     | Chennai
           2 | Green Leaf Hotels | Pune
           3 | Patel Kitchenware | Ahmedabad
           4 | Sharma Hardware   | Mumbai
(4 rows)
```

`ROW_NUMBER() OVER (ORDER BY customer)` (section 13.4) numbers the four customers 1 to 4 in name order, and the numbers become their surrogate keys. It's used here rather than an automatic identity column (section 12.13) because the rows already exist and you choose the order they're numbered in; section 28.9 uses identity columns for tables that are filled as they go. Now Sharma Hardware's city is stored once. The update anomaly from earlier can't happen, because there's only one row to update. (`sales_rep` has the same problem as `city`, since a rep's details depend on the rep, and exercise 9 asks you to fix it.)

### Proving nothing was lost

Normalization splits tables without losing information: joining them back must reproduce the original. Reconcile the revenue:

```sql
SELECT 'flat 1NF table' AS source,
       ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS net_revenue
FROM order_lines_1nf
UNION ALL
SELECT '3NF tables joined',
       ROUND(SUM(l.quantity * l.unit_price * (1 - l.discount_pct / 100)), 2)
FROM order_lines_2nf AS l
JOIN orders_3nf      AS o ON o.order_id = l.order_id
JOIN customers_3nf   AS c ON c.customer_id = o.customer_id
JOIN products_2nf    AS p ON p.product_id = l.product_id;
```

```
      source       | net_revenue
-------------------+-------------
 flat 1NF table    |   129040.00
 3NF tables joined |   129040.00
(2 rows)
```

<!-- lab:end -->

Both ₹1,29,040. ✓ Check one line by hand: order 10005 is 15 × ₹430 less 5% = ₹6,127.50.

![Four boxes left to right: 0NF order_sheet with products packed in one cell; 1NF with one row per order line; 2NF split into orders, products, and order lines; 3NF with customers in their own table](figures/fig28-5-normalization-steps.svg)

*Figure 28.5 — Each normal form removes one kind of repetition. The total never changes.*

### Beyond 3NF, and when to stop

There are stricter forms. **Boyce–Codd normal form (BCNF)** tightens 3NF for tables with several overlapping candidate keys (a **candidate key** is any column, or set of columns, that could serve as the primary key), and fourth and fifth normal forms deal with multi-valued facts. They're worth knowing by name for interviews; in business databases, a design in 3NF is almost always in BCNF too.

3NF is the standard target for **transactional systems** (the ERP, the CRM), where data is written constantly and must stay consistent. Reporting systems deliberately bend the rules, for speed and simplicity. That's sections 28.9 and 28.11.

| Normal form | The rule | Problem it removes | Riverstone fix |
|---|---|---|---|
| 1NF | one value per cell; rows unique | can't filter, count, or add | one row per order line |
| 2NF | no column depends on part of the key | product names repeated; can't add a product without an order | products table |
| 3NF | no column depends on a non-key column | customer's city repeated and able to disagree | customers table |

---

## 28.8 The grain discipline

Chapter 12 (section 12.10) named the idea: the **grain** of a table is what one row represents. Chapter 12 used it to explain fan-out, and promised a whole discipline. Here it is, in four habits.

### Habit 1: state the grain in one sentence, before anything else

Every table, view, and query result should have a grain you can say out loud:

| Table | Grain | Key that proves it |
|---|---|---|
| `orders` | one order | `order_id` |
| `order_items` | one product line within one order | `order_item_id`, and `(order_id, product_id)` should also be unique |
| `sales_lines` (view) | one non-cancelled order line | `order_id, product_id` |
| `sales_targets` | one calendar month | `target_month` |
| `lead_stage_history` | one lead entering one stage | `(lead_id, stage)` |
| `staff` | one person | `staff_id` |

If you can't write the sentence, you don't understand the table yet, and any total you compute from it is a guess.

### Habit 2: test the grain, don't assume it

A grain is a claim about the data, and data breaks claims. The test is a `GROUP BY` on the columns that should be unique. Back in `riverstone_2025`:

<!-- db: riverstone_2025 -->

```sql
SELECT order_id, product_id, COUNT(*) AS copies
FROM order_items
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;
```

```
 order_id | product_id | copies
----------+------------+--------
(0 rows)
```

No rows: each product appears at most once per order, so the grain holds. Chapter 13's Pattern 3 found the opposite in `leads`, where 43 rows held 30 real leads. Chapter 47 turns tests like this into automated checks that run every day, and Chapter 32 writes them as dbt tests.

### Habit 3: never join tables of different grains and then add

Here's the trap in its most common business form. *"Show January's order lines next to January's target."* The target's grain is one month; the lines' grain is one order line. Join them and sum the target:

```sql
SELECT ROUND(SUM(t.target_revenue)) AS target_summed_after_join
FROM sales_lines AS sl
JOIN sales_targets AS t
  ON t.target_month = DATE_TRUNC('month', sl.order_date)
WHERE sl.order_date < DATE '2025-02-01';
```

```
 target_summed_after_join
--------------------------
                  4500000
(1 row)
```

January's target is ₹3,00,000, not ₹45,00,000. The join copied the one monthly target onto each of January's 15 order lines, and `SUM` added all 15 copies (15 × ₹3,00,000). The query ran without error and returned a believable-looking number. This is the fan-out trap from section 12.10 in a new form, and it's the reason for habit 4.

### Habit 4: bring both sides to the same grain, then join

Aggregate the finer table up to the coarser grain first, then join one row to one row:

```sql
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month,
           SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY 1
)
SELECT m.month,
       ROUND(m.revenue)        AS revenue,
       ROUND(t.target_revenue) AS target,
       ROUND(100 * m.revenue / t.target_revenue, 1) AS pct_of_target
FROM monthly_sales AS m
JOIN sales_targets AS t ON t.target_month = m.month
WHERE m.month < DATE '2025-04-01'
ORDER BY m.month;
```

```
   month    | revenue | target | pct_of_target
------------+---------+--------+---------------
 2025-01-01 |  202640 | 300000 |          67.5
 2025-02-01 |  253664 | 300000 |          84.6
 2025-03-01 |  278008 | 320000 |          86.9
(3 rows)
```

January: ₹2,02,640 of ₹3,00,000 is 67.5%. ✓ Both sides now have the grain "one month", so the join can't multiply anything.

> **Interview extra point.** When an interviewer gives you two tables and a question, say the grain of each table before you write a join: *"orders is one row per order, order_items is one row per line, so if I join them I'll aggregate the lines first."* It shows the habit that prevents the most common wrong answer, and it's the kind of move Part 8's SQL bank (Chapter 71) scores as an extra point.

**Good place to stop.**

---

## 28.9 Dimensional modeling: facts, dimensions, and the star schema

Chapter 16 (section 16.3) built a star schema inside Power BI: a fact table, dimensions around it, and a date table. This section builds one in SQL, from the design method up, and adds what Power BI kept out of sight: surrogate keys, history (slowly changing dimensions), and loading. The first few ideas are a recap.

Normalized tables are built for *writing*: each fact once, so updates are safe. Analysts mostly *read*, and reading a normalized database means long chains of joins, repeated in every report and often subtly wrong. **Dimensional modeling**, popularized by Ralph Kimball, organizes the same data for reading. It's how most data warehouses, Power BI models (Chapter 16), and dbt marts (Chapter 32) are laid out.

### Facts and dimensions

Every business question has two kinds of words in it. *"What was **net revenue** by **customer segment** and **quarter**?"*

- **Facts** (or **measures**) are the numbers you add up: net revenue, quantity, cost. They come from business events: an order line, a payment, a delivery.
- **Dimensions** are the words you slice by: segment, quarter, product category, sales rep. They describe the *who, what, where, and when* of each event.

A **fact table** holds one row per event at a declared grain, with the measures and a key for each dimension. A **dimension table** holds one row per member of the dimension (one per customer, one per day), with every descriptive column a report might need. Arrange the dimensions around the fact table and draw lines to it, and the diagram looks like a star: a **star schema**.

### The four design steps

Kimball's method is four questions, asked in order:

1. **Choose the business process.** Not "sales data" but a specific event: *taking orders*.
2. **Declare the grain.** *One row per non-cancelled order line.* This is section 28.8's habit, and it comes before choosing any columns.
3. **Identify the dimensions.** What describes one order line? When (date), who bought (customer), what (product), who sold (sales rep).
4. **Identify the facts.** What numbers belong to one order line? Quantity, net revenue, product cost.

The answers give Riverstone's first star schema. You'll build it in a schema called `dw` (for *data warehouse*) inside `riverstone_2025`, next to the source tables, as section 12.13's schemas lesson suggested.

![A star schema: fact_sales_line in the center with keys to dim_date, dim_customer, dim_product, and dim_sales_rep around it. A side panel shows Metro Mart's two dim_customer rows: key 6 in Thane until 2025-07-01 and key 7 in Mumbai from then on](figures/fig28-6-star-schema-scd2.svg)

*Figure 28.6 — The fact table holds the events; each dimension describes one side of them. Metro Mart has two customer rows because it moved.*

### The date dimension

The most useful dimension, and the one people most often skip, is a **date dimension**: one row per calendar day, with every way the business describes a date already worked out.

<!-- build: dw -->
```sql
DROP SCHEMA IF EXISTS dw CASCADE;
CREATE SCHEMA dw;

CREATE TABLE dw.dim_date (
    date_key      INTEGER PRIMARY KEY,
    full_date     DATE NOT NULL UNIQUE,
    day_name      VARCHAR(9) NOT NULL,
    month_start   DATE NOT NULL,
    month_name    VARCHAR(9) NOT NULL,
    quarter_label CHAR(7) NOT NULL,
    is_weekend    BOOLEAN NOT NULL
);

INSERT INTO dw.dim_date
SELECT TO_CHAR(d, 'YYYYMMDD')::INTEGER,
       d::date,
       TRIM(TO_CHAR(d, 'Day')),
       DATE_TRUNC('month', d)::date,
       TRIM(TO_CHAR(d, 'Month')),
       TO_CHAR(d, 'YYYY-"Q"Q'),
       EXTRACT(ISODOW FROM d) IN (6, 7)
FROM generate_series(DATE '2025-01-01', DATE '2025-12-31', INTERVAL '1 day') AS d;
```

**How it works:**

- **`DROP SCHEMA IF EXISTS dw CASCADE`** drops the schema *and everything in it*: `CASCADE` means "and every table inside". That makes the build safe to rerun, and it's safe here only because `dw` holds nothing but this chapter's build. Never write `CASCADE` against a schema you didn't create.
- **`generate_series`** (Chapter 13, Pattern 5) produces every day of 2025, including days with no orders, so a report on "orders by weekday" or "days without sales" has every day to count. It returns timestamps, so `d::date` turns each one into a plain date.
- **`date_key`** is a whole number like `20250315`: `TO_CHAR(d, 'YYYYMMDD')` writes the date as the text `'20250315'`, and `::INTEGER` turns that text into a number. It's readable, sorts correctly, and joins fast. Using a meaningful number for dates is a common exception to the rule that surrogate keys carry no meaning.
- **`TO_CHAR(d, 'Day')`** gives the weekday name, padded with spaces to nine characters (`'Saturday '`), so **`TRIM`** removes the padding; `'Month'` works the same way.
- **`'YYYY-"Q"Q'`**: inside a `TO_CHAR` format, text in double quotes is printed as it is, so `"Q"` prints the letter Q, and the plain `Q` is the quarter number: `2025-Q1`.
- **`EXTRACT(ISODOW FROM d)`** numbers the weekdays Monday = 1 to Sunday = 7, so `IN (6, 7)` is true on Saturdays and Sundays.

Each descriptive column is computed once here instead of in every report. Real date dimensions add fiscal year (April to March, for most Indian companies), holiday flags, and week numbers. When finance decides that the festive season starts in October, you change one table, not fifty reports. Check three rows:

```sql
SELECT *
FROM dw.dim_date
WHERE full_date IN ('2025-01-01', '2025-03-15', '2025-12-31')
ORDER BY full_date;
```

```
 date_key | full_date  | day_name  | month_start | month_name | quarter_label | is_weekend
----------+------------+-----------+-------------+------------+---------------+------------
 20250101 | 2025-01-01 | Wednesday | 2025-01-01  | January    | 2025-Q1       | f
 20250315 | 2025-03-15 | Saturday  | 2025-03-01  | March      | 2025-Q1       | t
 20251231 | 2025-12-31 | Wednesday | 2025-12-01  | December   | 2025-Q4       | f
(3 rows)
```

### Product and sales rep dimensions

<!-- build: dw -->
```sql
CREATE TABLE dw.dim_product (
    product_key   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id    INTEGER NOT NULL UNIQUE,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(30) NOT NULL
);
INSERT INTO dw.dim_product (product_id, product_name, category)
SELECT product_id, product_name, category FROM products ORDER BY product_id;

CREATE TABLE dw.dim_sales_rep (
    sales_rep_key  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id    INTEGER UNIQUE,
    rep_name       VARCHAR(100) NOT NULL,
    job_title      VARCHAR(50) NOT NULL
);
INSERT INTO dw.dim_sales_rep (employee_id, rep_name, job_title)
VALUES (NULL, 'No rep recorded', 'Unknown');
INSERT INTO dw.dim_sales_rep (employee_id, rep_name, job_title)
SELECT employee_id, employee_name, job_title FROM employees ORDER BY employee_id;
```

Each dimension gets its own **surrogate key** (`product_key`, `sales_rep_key`), separate from the source system's id. `INTEGER GENERATED ALWAYS AS IDENTITY` is section 12.13's automatic numbering: the database numbers the rows 1, 2, 3… as they arrive, which is why neither `INSERT` lists the key column. (You'll often see `SERIAL` in older PostgreSQL code; it's the older shorthand for the same thing.) Section 28.10 shows why a separate key is essential for customers. The sales rep dimension also has a row for *"No rep recorded"*, inserted first so it gets key 1, because 11 orders have no rep (10 of them not cancelled): the fact table can then always point to a real dimension row, and reports show an honest "No rep recorded" instead of silently dropping those orders in an inner join.

```sql
SELECT * FROM dw.dim_sales_rep ORDER BY sales_rep_key;
```

```
 sales_rep_key | employee_id |    rep_name     |    job_title
---------------+-------------+-----------------+-----------------
             1 |             | No rep recorded | Unknown
             2 |           1 | Anita Rao       | Sales Head
             3 |           2 | Vikram Singh    | Sales Manager
             4 |           3 | Neha Kulkarni   | Sales Executive
             5 |           4 | Rahul Mehta     | Sales Executive
             6 |           5 | Farah Khan      | Sales Executive
(6 rows)
```

### The customer dimension

Customers are harder, because they change: in 2025 Patel Kitchenware was reclassified from Wholesale to Retail, Metro Mart moved from Thane to Mumbai, and Harbour Traders moved from Retail to Wholesale. The ERP's `customers` table only holds the values as they are now; the history is in `customer_changes`:

```sql
SELECT change_id, customer_id, changed_on, column_name, old_value, new_value
FROM customer_changes
ORDER BY changed_on;
```

```
 change_id | customer_id | changed_on | column_name | old_value | new_value
-----------+-------------+------------+-------------+-----------+-----------
         1 |           2 | 2025-04-01 | segment     | Wholesale | Retail
         2 |           5 | 2025-07-01 | city        | Thane     | Mumbai
         3 |          11 | 2025-09-01 | segment     | Retail    | Wholesale
(3 rows)
```

The dimension keeps a separate row for each version of each customer. Section 28.10 explains the design (it's a *type 2 slowly changing dimension*); for now, read it as "one row per customer per period in which their details stayed the same". First the table:

<!-- build: dw -->
```sql
CREATE TABLE dw.dim_customer (
    customer_key   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id    INTEGER NOT NULL,
    customer_name  VARCHAR(100) NOT NULL,
    city           VARCHAR(50),
    segment        VARCHAR(30) NOT NULL,
    valid_from     DATE NOT NULL,
    valid_to       DATE NOT NULL,
    is_current     BOOLEAN NOT NULL
);
```

Filling it takes one long query. Build it in four steps, each run on its own and checked on the three customers who changed (2, 5, and 11), before putting it into the table.

**Step 1: when could each version start?** On the signup date, and on every change date:

```sql
WITH version_starts AS (
    SELECT customer_id, signup_date AS valid_from FROM customers
    UNION
    SELECT customer_id, changed_on FROM customer_changes
)
SELECT customer_id, valid_from
FROM version_starts
WHERE customer_id IN (2, 5, 11)
ORDER BY customer_id, valid_from;
```

```
 customer_id | valid_from
-------------+------------
           2 | 2024-12-15
           2 | 2025-04-01
           5 | 2024-12-22
           5 | 2025-07-01
          11 | 2025-04-09
          11 | 2025-09-01
(6 rows)
```

Each changed customer has two start dates: signup and the change. `UNION` (not `UNION ALL`) removes duplicates, so if a customer changed on the day they signed up, the two identical start dates would become one, not two versions of one day.

**Step 2: when does each version end?** On the day the next one starts:

```sql
WITH version_starts AS (
    SELECT customer_id, signup_date AS valid_from FROM customers
    UNION
    SELECT customer_id, changed_on FROM customer_changes
),
versions AS (
    SELECT customer_id,
           valid_from,
           LEAD(valid_from, 1, DATE '9999-12-31')
               OVER (PARTITION BY customer_id ORDER BY valid_from) AS valid_to
    FROM version_starts
)
SELECT customer_id, valid_from, valid_to
FROM versions
WHERE customer_id IN (2, 5, 11)
ORDER BY customer_id, valid_from;
```

```
 customer_id | valid_from |  valid_to
-------------+------------+------------
           2 | 2024-12-15 | 2025-04-01
           2 | 2025-04-01 | 9999-12-31
           5 | 2024-12-22 | 2025-07-01
           5 | 2025-07-01 | 9999-12-31
          11 | 2025-04-09 | 2025-09-01
          11 | 2025-09-01 | 9999-12-31
(6 rows)
```

`LEAD` (section 13.5) looks at the next row of the customer's own versions. Section 13.5 used it with one argument; here it has three. The second, `1`, says how many rows ahead to look. The third, `DATE '9999-12-31'`, is the value to use when there is no next row: the latest version gets this far-future date, which means "still current".

**Step 3: which city was in effect?** For each version, find the latest city change on or before its start. Try it by hand for Metro Mart (customer 5), whose city changed from Thane to Mumbai on 1 July 2025:

```sql
SELECT
    (SELECT ch.new_value FROM customer_changes AS ch
     WHERE ch.customer_id = 5 AND ch.column_name = 'city'
       AND ch.changed_on <= DATE '2025-07-01'
     ORDER BY ch.changed_on DESC LIMIT 1)          AS city_on_2025_07_01,
    (SELECT ch.new_value FROM customer_changes AS ch
     WHERE ch.customer_id = 5 AND ch.column_name = 'city'
       AND ch.changed_on <= DATE '2024-12-22'
     ORDER BY ch.changed_on DESC LIMIT 1)          AS city_on_2024_12_22,
    (SELECT ch.old_value FROM customer_changes AS ch
     WHERE ch.customer_id = 5 AND ch.column_name = 'city'
     ORDER BY ch.changed_on LIMIT 1)               AS city_before_first_change;
```

```
 city_on_2025_07_01 | city_on_2024_12_22 | city_before_first_change
--------------------+--------------------+--------------------------
 Mumbai             |                    | Thane
(1 row)
```

**How it works:** each column is a scalar subquery (section 12.12), a query that returns one value.

- `ORDER BY ch.changed_on DESC LIMIT 1` keeps the latest change, and `ch.changed_on <= …` keeps only changes on or before the date. Together they mean *"the latest change on or before this date"*. For the version starting 1 July 2025, that's the move itself, so its `new_value` is Mumbai.
- For the version starting 22 December 2024 there was no change yet, so the subquery finds nothing and returns NULL.
- For that case, the third subquery takes the *old* value of the customer's *first* change (`ORDER BY ch.changed_on`, ascending): the city before anything changed, Thane.
- A customer who never changed has no rows in `customer_changes` at all; then the city in `customers` is right.

**Step 4: put the pieces together.** `COALESCE` (section 12.7) takes the first of those three answers that isn't NULL. The same three-way fallback finds the segment:

```sql
WITH version_starts AS (
    SELECT customer_id, signup_date AS valid_from FROM customers
    UNION
    SELECT customer_id, changed_on FROM customer_changes
),
versions AS (
    SELECT customer_id,
           valid_from,
           LEAD(valid_from, 1, DATE '9999-12-31')
               OVER (PARTITION BY customer_id ORDER BY valid_from) AS valid_to
    FROM version_starts
)
SELECT v.customer_id,
       c.customer_name,
       COALESCE(
           (SELECT ch.new_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'city'
              AND ch.changed_on <= v.valid_from
            ORDER BY ch.changed_on DESC LIMIT 1),
           (SELECT ch.old_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'city'
            ORDER BY ch.changed_on LIMIT 1),
           c.city)                                   AS city,
       COALESCE(
           (SELECT ch.new_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'segment'
              AND ch.changed_on <= v.valid_from
            ORDER BY ch.changed_on DESC LIMIT 1),
           (SELECT ch.old_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'segment'
            ORDER BY ch.changed_on LIMIT 1),
           c.segment)                                AS segment,
       v.valid_from,
       v.valid_to,
       v.valid_to = DATE '9999-12-31'                AS is_current
FROM versions AS v
JOIN customers AS c ON c.customer_id = v.customer_id
WHERE v.customer_id IN (2, 5, 11)
ORDER BY v.customer_id, v.valid_from;
```

```
 customer_id |   customer_name   |   city    |  segment  | valid_from |  valid_to  | is_current
-------------+-------------------+-----------+-----------+------------+------------+------------
           2 | Patel Kitchenware | Ahmedabad | Wholesale | 2024-12-15 | 2025-04-01 | f
           2 | Patel Kitchenware | Ahmedabad | Retail    | 2025-04-01 | 9999-12-31 | t
           5 | Metro Mart        | Thane     | Retail    | 2024-12-22 | 2025-07-01 | f
           5 | Metro Mart        | Mumbai    | Retail    | 2025-07-01 | 9999-12-31 | t
          11 | Harbour Traders   | Kochi     | Retail    | 2025-04-09 | 2025-09-01 | f
          11 | Harbour Traders   | Kochi     | Wholesale | 2025-09-01 | 9999-12-31 | t
(6 rows)
```

Patel Kitchenware is Wholesale until 1 April 2025 and Retail from then on; Metro Mart is in Thane until 1 July. The last column is new: **`v.valid_to = DATE '9999-12-31' AS is_current`**. A comparison is itself a value, true or false, so it can be a column: true for the version that hasn't ended.

**Step 5: load the table.** `INSERT INTO … (columns)` can take any query, including one that starts with `WITH`. Drop the test filter and insert every customer's versions:

<!-- build: dw -->
```sql
INSERT INTO dw.dim_customer
    (customer_id, customer_name, city, segment, valid_from, valid_to, is_current)
WITH version_starts AS (
    SELECT customer_id, signup_date AS valid_from FROM customers
    UNION
    SELECT customer_id, changed_on FROM customer_changes
),
versions AS (
    SELECT customer_id,
           valid_from,
           LEAD(valid_from, 1, DATE '9999-12-31')
               OVER (PARTITION BY customer_id ORDER BY valid_from) AS valid_to
    FROM version_starts
)
SELECT v.customer_id,
       c.customer_name,
       COALESCE(
           (SELECT ch.new_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'city'
              AND ch.changed_on <= v.valid_from
            ORDER BY ch.changed_on DESC LIMIT 1),
           (SELECT ch.old_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'city'
            ORDER BY ch.changed_on LIMIT 1),
           c.city)                                   AS city,
       COALESCE(
           (SELECT ch.new_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'segment'
              AND ch.changed_on <= v.valid_from
            ORDER BY ch.changed_on DESC LIMIT 1),
           (SELECT ch.old_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'segment'
            ORDER BY ch.changed_on LIMIT 1),
           c.segment)                                AS segment,
       v.valid_from,
       v.valid_to,
       v.valid_to = DATE '9999-12-31'                AS is_current
FROM versions AS v
JOIN customers AS c ON c.customer_id = v.customer_id
ORDER BY v.customer_id, v.valid_from;
```

`customer_key` isn't listed, so the identity column numbers the rows in the order they arrive, customer by customer and oldest version first.

### The fact table

<!-- build: dw -->
```sql
CREATE TABLE dw.fact_sales_line (
    order_item_id  INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL,
    date_key       INTEGER NOT NULL REFERENCES dw.dim_date (date_key),
    customer_key   INTEGER NOT NULL REFERENCES dw.dim_customer (customer_key),
    product_key    INTEGER NOT NULL REFERENCES dw.dim_product (product_key),
    sales_rep_key  INTEGER NOT NULL REFERENCES dw.dim_sales_rep (sales_rep_key),
    quantity       INTEGER NOT NULL,
    net_revenue    NUMERIC(12,2) NOT NULL,
    product_cost   NUMERIC(12,2) NOT NULL
);

INSERT INTO dw.fact_sales_line
SELECT oi.order_item_id,
       o.order_id,
       TO_CHAR(o.order_date, 'YYYYMMDD')::INTEGER,
       dc.customer_key,
       dp.product_key,
       dr.sales_rep_key,
       oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100),
       oi.quantity * p.unit_cost
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products    AS p  ON p.product_id = oi.product_id
JOIN dw.dim_customer AS dc
  ON dc.customer_id = o.customer_id
 AND o.order_date >= dc.valid_from AND o.order_date < dc.valid_to
JOIN dw.dim_product  AS dp ON dp.product_id = oi.product_id
JOIN dw.dim_sales_rep AS dr
  ON dr.employee_id IS NOT DISTINCT FROM o.sales_rep_id
WHERE o.status <> 'Cancelled';
```

The critical line is the join to `dw.dim_customer`: `o.order_date >= dc.valid_from AND o.order_date < dc.valid_to`. Each order line gets the key of the customer version **in effect on the order date**. Once that key is stored, the fact row never needs to look at the date range again. `IS NOT DISTINCT FROM` is a null-safe equals: unlike `=`, it treats two NULLs as equal, so orders with no rep match the "No rep recorded" row.

### Check the build

A warehouse you haven't reconciled is a warehouse nobody should trust. Three checks:

<!-- db: riverstone_2025 -->

```sql
SELECT 'dim_date' AS table_name, COUNT(*) AS row_count FROM dw.dim_date
UNION ALL SELECT 'dim_customer',    COUNT(*) FROM dw.dim_customer
UNION ALL SELECT 'dim_product',     COUNT(*) FROM dw.dim_product
UNION ALL SELECT 'dim_sales_rep',   COUNT(*) FROM dw.dim_sales_rep
UNION ALL SELECT 'fact_sales_line', COUNT(*) FROM dw.fact_sales_line;
```

```
   table_name    | row_count
-----------------+-----------
 dim_date        |       365
 dim_customer    |        27
 dim_product     |         8
 dim_sales_rep   |         6
 fact_sales_line |       326
(5 rows)
```

365 days. 27 customer rows: 24 customers, plus one extra version for each of the three who changed. ✓

```sql
SELECT customer_key, customer_name, city, segment, valid_from, valid_to, is_current
FROM dw.dim_customer
WHERE customer_id IN (2, 5, 11)
ORDER BY customer_id, valid_from;
```

```
 customer_key |   customer_name   |   city    |  segment  | valid_from |  valid_to  | is_current
--------------+-------------------+-----------+-----------+------------+------------+------------
            2 | Patel Kitchenware | Ahmedabad | Wholesale | 2024-12-15 | 2025-04-01 | f
            3 | Patel Kitchenware | Ahmedabad | Retail    | 2025-04-01 | 9999-12-31 | t
            6 | Metro Mart        | Thane     | Retail    | 2024-12-22 | 2025-07-01 | f
            7 | Metro Mart        | Mumbai    | Retail    | 2025-07-01 | 9999-12-31 | t
           13 | Harbour Traders   | Kochi     | Retail    | 2025-04-09 | 2025-09-01 | f
           14 | Harbour Traders   | Kochi     | Wholesale | 2025-09-01 | 9999-12-31 | t
(6 rows)
```

Each changed customer has one closed version and one current version, and each version ends on the day the next begins. ✓

```sql
SELECT (SELECT ROUND(SUM(net_revenue)) FROM sales_lines)        AS view_total,
       (SELECT ROUND(SUM(net_revenue)) FROM dw.fact_sales_line) AS fact_total,
       (SELECT COUNT(*) FROM sales_lines)                        AS view_lines,
       (SELECT COUNT(*) FROM dw.fact_sales_line)                 AS fact_lines;
```

```
 view_total | fact_total | view_lines | fact_lines
------------+------------+------------+------------
    4335471 |    4335471 |        326 |        326
(1 row)
```

₹43,35,471 and 326 lines in both. ✓ If any order line had failed to find a customer version (a gap between one version's end and the next one's start, for instance), the inner join would have dropped it and the fact total would be lower. This one query catches that.

### Querying the star

Every report now has the same simple shape: the fact table, joined to the dimensions you need, grouped by their columns.

```sql
SELECT d.quarter_label,
       c.segment,
       ROUND(SUM(f.net_revenue)) AS net_revenue
FROM dw.fact_sales_line AS f
JOIN dw.dim_date     AS d ON d.date_key = f.date_key
JOIN dw.dim_customer AS c ON c.customer_key = f.customer_key
GROUP BY d.quarter_label, c.segment
ORDER BY d.quarter_label, c.segment;
```

```
 quarter_label |   segment   | net_revenue
---------------+-------------+-------------
 2025-Q1       | Hospitality |      149040
 2025-Q1       | Retail      |      356290
 2025-Q1       | Wholesale   |      228982
 2025-Q2       | Hospitality |      252170
 2025-Q2       | Retail      |      271031
 2025-Q2       | Wholesale   |      203367
 2025-Q3       | Hospitality |      307278
 2025-Q3       | Retail      |      384294
 2025-Q3       | Wholesale   |      428718
 2025-Q4       | Hospitality |      435551
 2025-Q4       | Retail      |      562000
 2025-Q4       | Wholesale   |      756751
(12 rows)
```

No `DATE_TRUNC`, no `CASE`, no joins through orders to reach customers. The quarters add up to the year: Q4 alone is ₹17,54,302 (4,35,551 + 5,62,000 + 7,56,751), 40.5% of the total, which matches Chapter 13's festive-season finding.

### Star or snowflake?

In a star schema, each dimension is one wide table, even if that repeats values: `category` is stored on every product row. A **snowflake schema** normalizes the dimensions too (`dim_product` points to a `dim_category` table), so the diagram branches like a snowflake.

| | Star | Snowflake |
|---|---|---|
| Dimension tables | one wide table per dimension | split into sub-dimensions |
| Joins in a report | one per dimension | more |
| Repetition in dimensions | yes, deliberately | less |
| Easier for BI tools and business users | yes | no |
| Typical use | most warehouses and Power BI models | very large dimensions with many shared levels |

Dimension tables are small (Riverstone's biggest has 27 rows; a large company's customer dimension might have a few million), so the repetition costs little, and the simpler joins help everyone who writes reports. **Default to a star.** Power BI's documentation recommends star schemas for its models, which is why Chapter 16's model looked like this one.

### Other kinds of fact tables

`fact_sales_line` is a **transaction fact table**: one row per event, added once and never changed. Two other kinds cover questions it can't answer well:

- A **periodic snapshot** records the state of something at regular intervals: stock on hand at each warehouse at the end of each day, or receivables outstanding at each month-end. You can't add snapshots across time (adding daily stock levels makes no sense), but you can average them or take the latest.
- An **accumulating snapshot** has one row per process instance, updated as it moves through fixed milestones: one row per order with the dates it was placed, invoiced, shipped, delivered, and paid. It's the natural home for Chapter 3's order-to-cash durations.

And one more design term you'll hear: **conformed dimensions** are dimensions shared by several fact tables with the same keys and meanings. If the sales facts and the payments facts both use the same `dim_customer` and `dim_date`, a report can put revenue and collections side by side and trust that "Retail, 2025-Q3" means the same thing in both.

---

## 28.10 Slowly changing dimensions

Customers move, get reclassified, change their names. Products move between categories. Sales reps change teams. Dimensions change slowly (compared with facts, which arrive every minute), and how you handle those changes decides whether last year's reports still say what they said last year. The standard catalog of techniques is called **slowly changing dimension (SCD) types**. Three matter in practice.

To see each one clearly, go back to the lab and use the example from section 12.1: suppose Sharma Hardware moves from Mumbai to Thane, effective 1 April 2026. A nightly extract from the ERP (`customer_extract`) brings the new city, along with a customer the lab's small dimension doesn't hold yet, Coastal Foods. (The ids are the `customer_id`s from `riverstone_2025`: Sharma Hardware 1, Green Leaf Hotels 3, Coastal Foods 4. They are not the surrogate keys `customers_3nf` gave in section 28.7.)

<!-- lab:start -->

```sql
CREATE TABLE dim_customer_t1 (
    customer_id  INTEGER PRIMARY KEY,
    customer     VARCHAR(100) NOT NULL,
    city         VARCHAR(50),
    segment      VARCHAR(30)
);

INSERT INTO dim_customer_t1 VALUES
(1, 'Sharma Hardware',   'Mumbai', 'Retail'),
(3, 'Green Leaf Hotels', 'Pune',   'Hospitality');

CREATE TABLE customer_extract (
    customer_id  INTEGER PRIMARY KEY,
    customer     VARCHAR(100) NOT NULL,
    city         VARCHAR(50),
    segment      VARCHAR(30)
);

INSERT INTO customer_extract VALUES
(1, 'Sharma Hardware',   'Thane',   'Retail'),
(3, 'Green Leaf Hotels', 'Pune',    'Hospitality'),
(4, 'Coastal Foods',     'Chennai', 'Wholesale');
```

### Type 1: overwrite

**Type 1** replaces the old value with the new one. No history is kept. It's right for **corrections** (a misspelled name, a wrong PIN code) and for attributes nobody reports history on.

The tidiest way to apply an extract is **`MERGE`** (PostgreSQL 15 and later), which updates rows that match and inserts rows that don't, in one statement:

```sql
MERGE INTO dim_customer_t1 AS d
USING customer_extract AS x
ON d.customer_id = x.customer_id
WHEN MATCHED AND (d.city IS DISTINCT FROM x.city OR d.segment IS DISTINCT FROM x.segment) THEN
    UPDATE SET city = x.city, segment = x.segment
WHEN NOT MATCHED THEN
    INSERT (customer_id, customer, city, segment)
    VALUES (x.customer_id, x.customer, x.city, x.segment);

SELECT * FROM dim_customer_t1 ORDER BY customer_id;
```

```
 customer_id |     customer      |  city   |   segment
-------------+-------------------+---------+-------------
           1 | Sharma Hardware   | Thane   | Retail
           3 | Green Leaf Hotels | Pune    | Hospitality
           4 | Coastal Foods     | Chennai | Wholesale
(3 rows)
```

**How it works:** `USING` names the incoming data and `ON` says how to match it. `WHEN MATCHED AND …` updates only rows that really changed (`IS DISTINCT FROM` treats two NULLs as equal, so unchanged NULLs don't count as changes). `WHEN NOT MATCHED` inserts new customers. Sharma Hardware is now in Thane, and **every past sale of Sharma Hardware now reports as Thane**, including sales made in Mumbai in 2025. For a correction, that's exactly right. For a real move, it rewrites history.

### Type 2: add a new row

**Type 2** keeps history by closing the current row and inserting a new one. Each row is a *version*, with its own surrogate key and a validity period. This is what `dw.dim_customer` did in section 28.9.

```sql
CREATE TABLE dim_customer_t2 (
    customer_key  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id   INTEGER NOT NULL,
    customer      VARCHAR(100) NOT NULL,
    city          VARCHAR(50),
    segment       VARCHAR(30),
    valid_from    DATE NOT NULL,
    valid_to      DATE NOT NULL DEFAULT '9999-12-31',
    is_current    BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO dim_customer_t2 (customer_id, customer, city, segment, valid_from) VALUES
(1, 'Sharma Hardware',   'Mumbai', 'Retail',      '2024-11-04'),
(3, 'Green Leaf Hotels', 'Pune',   'Hospitality', '2024-09-08');

CREATE UNIQUE INDEX one_current_row ON dim_customer_t2 (customer_id) WHERE is_current;
```

The columns that make it type 2:

- **`customer_key`**: the surrogate key. `customer_id` (the **natural key** or **business key** from the ERP) is no longer unique, because one customer can have several versions. Facts store `customer_key`, which points to exactly one version.
- **`valid_from` and `valid_to`**: the period the version was true. A half-open period (from `valid_from`, up to but not including `valid_to`) means consecutive versions never overlap and never leave a gap.
- **`is_current`**: a convenience flag for "the latest version".
- The **partial unique index** (section 28.6) makes the database enforce the rule that each customer has at most one current row.

Applying the extract is two steps, in one transaction so nobody ever sees a customer with no current row:

```sql
BEGIN;

-- step 1: close the current version of customers whose details changed
UPDATE dim_customer_t2 AS d
SET valid_to = DATE '2026-04-01',
    is_current = FALSE
FROM customer_extract AS x
WHERE d.customer_id = x.customer_id
  AND d.is_current
  AND (d.city IS DISTINCT FROM x.city OR d.segment IS DISTINCT FROM x.segment);

-- step 2: insert a new current version for every customer without one
INSERT INTO dim_customer_t2 (customer_id, customer, city, segment, valid_from)
SELECT x.customer_id, x.customer, x.city, x.segment, DATE '2026-04-01'
FROM customer_extract AS x
LEFT JOIN dim_customer_t2 AS d
       ON d.customer_id = x.customer_id AND d.is_current
WHERE d.customer_id IS NULL;

COMMIT;

SELECT customer_key, customer_id, customer, city, valid_from, valid_to, is_current
FROM dim_customer_t2
ORDER BY customer_id, valid_from;
```

```
 customer_key | customer_id |     customer      |  city   | valid_from |  valid_to  | is_current
--------------+-------------+-------------------+---------+------------+------------+------------
            1 |           1 | Sharma Hardware   | Mumbai  | 2024-11-04 | 2026-04-01 | f
            3 |           1 | Sharma Hardware   | Thane   | 2026-04-01 | 9999-12-31 | t
            2 |           3 | Green Leaf Hotels | Pune    | 2024-09-08 | 9999-12-31 | t
            4 |           4 | Coastal Foods     | Chennai | 2026-04-01 | 9999-12-31 | t
(4 rows)
```

**How it works:** step 1 closes Sharma Hardware's Mumbai version. Its `valid_to` is set to 1 April 2026, the day the new version starts: with half-open periods, `valid_to` is the first day the version is *no longer* true, so the Mumbai version covers everything up to and including 31 March. `UPDATE … FROM` (section 12.13's dialect table) lets the `UPDATE` read a second table, here the extract. Green Leaf Hotels didn't change, so it's left alone. Step 2 then looks for extract rows with no current version: that's Sharma Hardware (whose current version step 1 closed) and Coastal Foods (new to this dimension). Both get a new row. Green Leaf still has its current row, so the `LEFT JOIN … IS NULL` skips it.

> **Simplification note.** This version compares two columns and hard-codes the dates. A production load compares every tracked column (often by comparing a hash of them), takes the dates from the extract, handles customers deleted from the source, and runs as a scheduled job. Chapter 32 shows dbt's *snapshots*, which implement type 2 this way from a short configuration.

### Joining facts to a type 2 dimension

Four orders: two before the move (one of them on 31 March, the last day in Mumbai), and two after.

```sql
CREATE TABLE fact_sales (
    order_id      INTEGER,
    order_date    DATE,
    customer_id   INTEGER,
    net_revenue   NUMERIC(12,2)
);

INSERT INTO fact_sales VALUES
(20001, '2026-03-18', 1, 42000),
(20002, '2026-03-31', 1, 12500),
(20003, '2026-04-09', 1, 35500),
(20004, '2026-04-10', 3, 18000);

SELECT f.order_id,
       f.order_date,
       d.customer_key,
       d.city AS city_at_order_time,
       f.net_revenue
FROM fact_sales AS f
JOIN dim_customer_t2 AS d
  ON d.customer_id = f.customer_id
 AND f.order_date >= d.valid_from
 AND f.order_date <  d.valid_to
ORDER BY f.order_id;
```

```
 order_id | order_date | customer_key | city_at_order_time | net_revenue
----------+------------+--------------+--------------------+-------------
    20001 | 2026-03-18 |            1 | Mumbai             |    42000.00
    20002 | 2026-03-31 |            1 | Mumbai             |    12500.00
    20003 | 2026-04-09 |            3 | Thane              |    35500.00
    20004 | 2026-04-10 |            2 | Pune               |    18000.00
(4 rows)
```

The March orders belong to Mumbai, including the one on 31 March, the last day of the Mumbai version; the April order belongs to Thane. This is a **point-in-time join**. Had step 1 stored 31 March as `valid_to`, order 20002 would match neither version (31 March is not *before* 31 March), and the inner join would silently drop it. In a warehouse you do it once, when loading facts, and store the `customer_key`, as `dw.fact_sales_line` did.

Now the trap. Join on the business key alone, forgetting the dates:

```sql
SELECT d.city, SUM(f.net_revenue) AS net_revenue
FROM fact_sales AS f
JOIN dim_customer_t2 AS d ON d.customer_id = f.customer_id
GROUP BY d.city
ORDER BY d.city;
```

```
  city  | net_revenue
--------+-------------
 Mumbai |    90000.00
 Pune   |    18000.00
 Thane  |    90000.00
(3 rows)
```

Total revenue should be ₹1,08,000. This shows ₹1,98,000. Each of Sharma Hardware's three orders matched both versions, so ₹90,000 (₹42,000 + ₹12,500 + ₹35,500) was counted in Mumbai *and* in Thane. It's the fan-out trap again: a type 2 dimension's grain is *one customer version*, not *one customer*, and joining on `customer_id` alone ignores that.

### Type 3: add a "previous" column

**Type 3** keeps limited history in extra columns: the current value and the one before it.

```sql
CREATE TABLE dim_customer_t3 (
    customer_id     INTEGER PRIMARY KEY,
    customer        VARCHAR(100) NOT NULL,
    city            VARCHAR(50),
    previous_city   VARCHAR(50),
    city_changed_on DATE
);

INSERT INTO dim_customer_t3 VALUES (1, 'Sharma Hardware', 'Mumbai', NULL, NULL);

UPDATE dim_customer_t3
SET previous_city   = city,
    city            = 'Thane',
    city_changed_on = DATE '2026-04-01'
WHERE customer_id = 1;

SELECT * FROM dim_customer_t3;
```

```
 customer_id |    customer     | city  | previous_city | city_changed_on
-------------+-----------------+-------+---------------+-----------------
           1 | Sharma Hardware | Thane | Mumbai        | 2026-04-01
(1 row)
```

<!-- lab:end -->

In PostgreSQL's `UPDATE`, every right-hand side sees the row's *old* values, so `previous_city = city` copies Mumbai even though `city` is assigned in the same statement.

Type 3 answers one specific question well: *"Show this year's sales under both the old and the new territory map."* It can't tell you where a customer was two moves ago, and it doesn't split sales by date.

### Choosing a type

| Type | What happens on a change | History kept | Use it for | Watch out for |
|---|---|---|---|---|
| 1 | overwrite | none | corrections; attributes nobody reports history on (phone, contact name) | silently restates past reports |
| 2 | close old row, add new row | full | attributes reports are sliced by, where history matters (segment, city, sales territory, product category) | join facts through the surrogate key or with a date range, never on the business key alone |
| 3 | move old value to a "previous" column | one step back | a planned, one-time reorganization compared side by side | only one previous value |

A single dimension usually mixes types: in Riverstone's customer dimension, a corrected phone number would be type 1, and a segment change type 2.

### Why type 2 changes the numbers: a real Riverstone result

Back in `riverstone_2025`: *"What did each segment sell in 2025?"* There are two honest answers, and the star schema can give both. **As it was** uses the version on each fact row. **As it is** re-labels every sale with each customer's current segment.

<!-- db: riverstone_2025 -->

```sql
WITH as_it_was AS (
    SELECT c.segment, SUM(f.net_revenue) AS revenue
    FROM dw.fact_sales_line AS f
    JOIN dw.dim_customer AS c ON c.customer_key = f.customer_key
    GROUP BY c.segment
),
as_it_is AS (
    SELECT cur.segment, SUM(f.net_revenue) AS revenue
    FROM dw.fact_sales_line AS f
    JOIN dw.dim_customer AS c   ON c.customer_key = f.customer_key
    JOIN dw.dim_customer AS cur ON cur.customer_id = c.customer_id AND cur.is_current
    GROUP BY cur.segment
)
SELECT w.segment,
       ROUND(w.revenue) AS revenue_as_it_was,
       ROUND(i.revenue) AS revenue_as_it_is,
       ROUND(i.revenue - w.revenue) AS difference
FROM as_it_was AS w
JOIN as_it_is  AS i ON i.segment = w.segment
ORDER BY w.segment;
```

```
   segment   | revenue_as_it_was | revenue_as_it_is | difference
-------------+-------------------+------------------+------------
 Hospitality |           1144039 |          1144039 |          0
 Retail      |           1573615 |          1488774 |     -84842
 Wholesale   |           1617817 |          1702659 |      84842
(3 rows)
```

**Reading it.** Retail's 2025 revenue is ₹15,73,615 as it was, or ₹14,88,774 if you re-label history with today's segments: ₹84,842 apart. Reconcile the difference by hand from the monthly figures: Patel Kitchenware's orders before 1 April (₹2,900 in January and ₹35,138 in March, ₹38,038) move *into* Retail, and Harbour Traders' orders from April to August (₹1,22,880) move *out*. ₹38,038 − ₹1,22,880 = −₹84,842. ✓ Both columns total ₹43,35,471.

Neither column is wrong. They answer different questions: *"How did the Retail team's customers perform at the time?"* versus *"How much have the customers who are Retail today bought?"* A type 1 dimension can only give the second answer, and it would give it without telling anyone. **What to tell Anita:** say which view a report uses, in its title.

---

## 28.11 Denormalization trade-offs

**Denormalization** means deliberately storing data more than once, or storing results that could be calculated, to make reading faster or simpler. A star schema is already denormalized (category repeated on every product row). This section is about the other common form: storing **pre-computed results**.

### The problem: a question that reads everything

*"Monthly revenue by product category, for the last three years."* On `riverstone_perf` that joins 700,070 non-cancelled orders to 1,888,466 lines and groups them into 144 rows. No index helps, because the question needs every row. Median time: 2,626 ms. For one analyst once a month, fine. For a dashboard opened by forty people every morning, it's forty queries of two and a half seconds, each reading 140 MB, for numbers that only change once a day.

### A summary table or materialized view

A **materialized view** is a view whose result is stored as a table and refreshed on request. Still in `riverstone_perf`:

<!-- run: none -->
```sql
CREATE MATERIALIZED VIEW monthly_category_revenue AS
SELECT DATE_TRUNC('month', o.order_date)::date AS month,
       p.category,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS net_revenue
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products    AS p  ON p.product_id = oi.product_id
WHERE o.status <> 'Cancelled'
GROUP BY 1, 2;
```

**How it works:** the query is the live one, unchanged. `CREATE MATERIALIZED VIEW … AS` runs it once and stores its 144 rows. A plain view (section 13.2) stores only the query and runs it every time; a materialized view stores the answer. `GROUP BY 1, 2` groups by the first and second columns of the `SELECT`.

The stored rows don't change when new orders arrive. Tomorrow, and every night after, one statement recomputes them:

<!-- run: none -->
```sql
REFRESH MATERIALIZED VIEW monthly_category_revenue;
```

Once built, it's read like any table:

<!-- db: riverstone_perf -->

```sql
SELECT month, category, ROUND(net_revenue) AS net_revenue
FROM monthly_category_revenue
WHERE month = DATE '2025-12-01'
ORDER BY net_revenue DESC;
```

```
   month    |  category  | net_revenue
------------+------------+-------------
 2025-12-01 | Storage    |   292916949
 2025-12-01 | Industrial |   286297690
 2025-12-01 | Furniture  |   230339308
 2025-12-01 | Kitchen    |   226362946
(4 rows)
```

(The amounts are far larger than Riverstone's real 2025 figures in `riverstone_2025`: the large database was generated to have realistic *volume*, not realistic totals.)

The measured trade-off on the test machine:

| Step | Time |
|---|---|
| Live query (median of 5) | 2,626 ms |
| Build the materialized view | 2,321 ms |
| Read one month (4 rows) from the materialized view (median of 7) | 0.10 ms |
| `REFRESH MATERIALIZED VIEW` | 2,300 ms |

One refresh a night costs about two seconds; every read after that is effectively free. The price is **staleness**: until the next refresh, the view doesn't show today's orders. For a monthly trend that's fine. For "orders taken in the last hour", it isn't.

### The trade-offs, laid out

| Technique | Faster reads because | You pay with | Good for |
|---|---|---|---|
| Star schema (repeated attributes) | fewer joins | more storage; updates to a dimension attribute touch many rows | all reporting |
| Summary table / materialized view | results already computed | staleness; refresh time; another object to maintain | dashboards, recurring reports on large data |
| Copying a column onto another table (for example customer segment onto orders) | saves a join | the two copies can disagree (section 28.7's update anomaly) | rarely; only with an automatic process keeping it in sync |
| Storing derived columns (for example `net_revenue` on order lines) | no calculation at read time | must be recomputed if inputs change | expensive, stable calculations |

Three rules keep denormalization safe:

1. **Normalize first.** The source of truth stays normalized. Denormalized copies are derived from it and can always be rebuilt.
2. **Denormalize for a measured problem**, not in advance. The table above started with a 2.6-second query, not a guess.
3. **Automate the refresh and make staleness visible.** Put "data as of 06:00" on the dashboard. A summary nobody refreshes becomes a wrong number that everyone trusts.

> **Dialect note.** PostgreSQL's `REFRESH MATERIALIZED VIEW CONCURRENTLY` lets people keep reading during a refresh (it needs a unique index on the view). MySQL has no materialized views: create a summary table and refresh it with a scheduled `DELETE` and `INSERT … SELECT` in a transaction, or an event (section 28.13). Warehouses such as Snowflake and BigQuery have their own materialized views with automatic refresh, and dbt builds summary tables as *models* on a schedule (Chapter 32).

**Good place to stop.**

---

## 28.12 Schema migrations: changing a live database safely

Section 12.13 ended with a checklist for changing a table's structure, and promised the tools teams use to do it every week without breaking things. Here they are.

### The problem migrations solve

Riverstone now has the ERP database, a reporting copy, a test copy, and every developer's laptop copy. A developer adds a column on their laptop. Does the test copy have it? Production? Which changes were run on production, in which order, by whom? When the answer lives in people's memories and old emails, databases **drift** apart, and one Monday a report fails in production that worked perfectly in test.

A **migration** is a small script that moves a database's structure from one version to the next. The discipline is:

1. **Every change is a file**, never typed into a query window on a shared database.
2. **Files are numbered**, and always applied in number order.
3. **The database records which migrations it has run**, in a history table.
4. **A migration never changes once applied.** A mistake is fixed by a *new* migration.
5. **Every migration is reviewed** (a pull request, Chapter 26) and run on test before production.

### Building the idea by hand

Before using a tool, see that there's no magic. Continue in the lab:

<!-- lab:start -->

```sql
CREATE TABLE schema_migrations (
    version      INTEGER PRIMARY KEY,
    description  VARCHAR(100) NOT NULL,
    checksum     CHAR(32) NOT NULL,
    applied_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Migrations 1 and 2 create a table and add its first rows. Each runs in a transaction together with its history row, so either both happen or neither does. (In a real project, `checksum` is a hash of the migration file's contents; here it's computed from a stand-in string.)

```sql
BEGIN;
CREATE TABLE suppliers (
    supplier_id    INTEGER PRIMARY KEY,
    supplier_name  VARCHAR(100) NOT NULL,
    city           VARCHAR(50)  NOT NULL
);
INSERT INTO schema_migrations (version, description, checksum)
VALUES (1, 'create suppliers', md5('V1__create_suppliers.sql contents'));
COMMIT;

BEGIN;
INSERT INTO suppliers VALUES
(1, 'Western Polymers', 'Vapi'),
(2, 'Deccan Cartons',   'Pune'),
(3, 'Sagar Labels',     'Mumbai');
INSERT INTO schema_migrations (version, description, checksum)
VALUES (2, 'seed suppliers', md5('V2__seed_suppliers.sql contents'));
COMMIT;
```

Migration 3 adds a column. Section 12.13's rule applies: a new `NOT NULL` column on a table with rows needs a `DEFAULT`, or existing rows break the constraint:

```sql
BEGIN;
ALTER TABLE suppliers ADD COLUMN payment_terms_days INTEGER NOT NULL DEFAULT 30;
INSERT INTO schema_migrations (version, description, checksum)
VALUES (3, 'add payment terms', md5('V3__add_payment_terms.sql contents'));
COMMIT;

SELECT version, description FROM schema_migrations ORDER BY version;
```

```
 version |    description
---------+-------------------
       1 | create suppliers
       2 | seed suppliers
       3 | add payment terms
(3 rows)
```

Any copy of the database can now answer *"which version are you on?"* with `SELECT MAX(version) FROM schema_migrations;`, and a tool can apply only the files with a higher number.

And here's the failure the `DEFAULT` rule prevents, in a migration someone forgot to test against real data:

```sql
BEGIN;
ALTER TABLE suppliers ADD COLUMN gst_number VARCHAR(15) NOT NULL;
SELECT MAX(version) FROM schema_migrations;
ROLLBACK;
```

```
BEGIN
ERROR:  column "gst_number" of relation "suppliers" contains null values
ERROR:  current transaction is aborted, commands ignored until end of transaction block
ROLLBACK
```

**Reading it:**

- The `ALTER` fails: three suppliers exist, and a new `NOT NULL` column with no default would leave them holding nothing.
- After an error inside a transaction, PostgreSQL refuses **every** further statement until you end the transaction. Even the harmless `SELECT` fails with *current transaction is aborted*. It's a safety catch: nothing more can happen on top of a half-finished change.
- **`ROLLBACK`** (section 12.13) ends the transaction and undoes everything since `BEGIN`. Always run it after an error inside `BEGIN`, before anything else. (`COMMIT` would also end it, but after an error PostgreSQL treats it as a rollback anyway.)

Check that nothing was left behind:

```sql
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'suppliers'
ORDER BY ordinal_position;

SELECT MAX(version) AS current_version FROM schema_migrations;
```

```
    column_name
--------------------
 supplier_id
 supplier_name
 city
 payment_terms_days
(4 rows)

 current_version
-----------------
               3
(1 row)
```

No `gst_number` column, and the database is still at version 3. Because the migration ran inside a transaction, the error left nothing half-done: no column, no history row. PostgreSQL can roll back structure changes like this; MySQL can't (section 28.13), which is one more reason to test migrations on a copy first.

> **Tool note: running migrations in DBeaver.** Run each migration block with *Execute script* (Alt+X), which runs the statements one after another. If the script stops on an error, the transaction is still open: run `ROLLBACK;` before anything else, or every later statement fails the same way.

> **Dialect note: the same migration in MySQL.** MySQL 8.0 doesn't raise this error. It adds the column and fills the existing rows with the type's implicit default, an empty string for `VARCHAR`, even in strict mode (tested on 8.0.46). The migration "succeeds", and three suppliers now have a GST number of `''` that no validation will ever flag. Same script, same intent, a silent data problem in one database and a loud error in the other: test migrations on every database engine you deploy to.

### Renaming without breaking anyone: expand, then contract

Suppose the team wants to rename `suppliers.city` to `supplier_city`. `ALTER TABLE … RENAME COLUMN` takes a moment, but every report, application, and dbt model that reads `city` breaks at that moment. On a system other people depend on, split the change into steps that are each safe on their own. This is the **expand and contract** pattern (also called *parallel change*):

1. **Expand:** add the new column and copy the data. Old readers still work.
2. **Migrate readers:** change each report and application to use the new column, in their own time. (Keep writers filling both columns meanwhile.)
3. **Contract:** once nothing reads the old column, drop it.

```sql
BEGIN;
ALTER TABLE suppliers ADD COLUMN supplier_city VARCHAR(50);
UPDATE suppliers SET supplier_city = city;
INSERT INTO schema_migrations (version, description, checksum)
VALUES (4, 'expand: add supplier_city', md5('V4 contents'));
COMMIT;

SELECT supplier_name, city, supplier_city FROM suppliers ORDER BY supplier_id;
```

```
  supplier_name   |  city  | supplier_city
------------------+--------+---------------
 Western Polymers | Vapi   | Vapi
 Deccan Cartons   | Pune   | Pune
 Sagar Labels     | Mumbai | Mumbai
(3 rows)
```

Days or weeks later, after every reader has moved:

```sql
BEGIN;
ALTER TABLE suppliers ALTER COLUMN supplier_city SET NOT NULL;
ALTER TABLE suppliers DROP COLUMN city;
INSERT INTO schema_migrations (version, description, checksum)
VALUES (5, 'contract: drop old city column', md5('V5 contents'));
COMMIT;

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'suppliers'
ORDER BY ordinal_position;
```

```
    column_name     |     data_type     | is_nullable
--------------------+-------------------+-------------
 supplier_id        | integer           | NO
 supplier_name      | character varying | NO
 payment_terms_days | integer           | NO
 supplier_city      | character varying | NO
(4 rows)
```

<!-- lab:end -->

### Migration tools

Nobody writes those `INSERT INTO schema_migrations` lines by hand in a real project. A **migration tool** reads a folder of numbered files, compares it with the history table, and applies what's missing. The ideas above are all the tools do; they differ in style:

| Tool | How migrations are written | Common with |
|---|---|---|
| **Flyway** (Redgate) | plain SQL files named `V1__create_suppliers.sql`, `V2__seed_suppliers.sql` | Java and SQL-first teams; widely used with PostgreSQL, MySQL, SQL Server, Oracle |
| **Liquibase** | *changelogs* in SQL, XML, YAML, or JSON, with changesets | enterprises needing detailed change tracking across many databases |
| **Alembic** | Python files, usually generated from SQLAlchemy models | Python applications that use SQLAlchemy |
| Framework tools (Django, Rails, Laravel, Entity Framework) | code in the application's language | teams whose database belongs to one application |
| **dbt** | not a migration tool: it rebuilds analytical models from `SELECT` statements | warehouses (Chapter 32) |

Flyway shows the conventions most clearly. Versioned migration files are named with a `V`, a version number, two underscores, and a description, like `V3__add_payment_terms.sql`, and are applied once each, in version order. Flyway records each one in a **schema history table** (`flyway_schema_history`) with a **checksum** of the file, so if someone edits a file after it was applied, `flyway validate` reports the mismatch instead of silently letting environments drift. `flyway info` lists applied and pending migrations. **Repeatable migrations**, named `R__description.sql`, have no version and are re-applied whenever their checksum changes, which suits views. (Check Redgate's documentation for the current version and edition.)

A migration project for Riverstone's reporting database looks like this:

```
reporting-db/
├── migrations/
│   ├── V1__create_suppliers.sql
│   ├── V2__seed_suppliers.sql
│   ├── V3__add_payment_terms.sql
│   ├── V4__expand_add_supplier_city.sql
│   ├── V5__contract_drop_city.sql
│   └── R__view_supplier_summary.sql
└── README.md
```

The companion file `migrate.py` is a runner of about 50 lines that applies a folder like this to PostgreSQL in the same way, with checksums, so you can watch the mechanism work before adopting a real tool. (It applies only `V` files; the `R__` file shows Flyway's naming.) The migration files hold **only the change**. Here's one:

<!-- run: none -->
```
# terminal, in the companion files folder
$ cd ch28
$ cat migrations/V3__add_payment_terms.sql
ALTER TABLE suppliers ADD COLUMN payment_terms_days INTEGER NOT NULL DEFAULT 30;
```

(`cat` prints a file, as in section 26.0; in Windows PowerShell, `type` does the same.) There's no `BEGIN`, no `COMMIT`, and no `INSERT INTO schema_migrations`: the runner adds those around each file. Its core is four short pieces. First, find the files and sort them by number:

<!-- run: none -->
```python
files = []
for f in pathlib.Path(a.folder).glob('V*__*.sql'):
    m = re.fullmatch(r'V(\d+)__(.+)\.sql', f.name)
    if m: files.append((int(m.group(1)), m.group(2).replace('_', ' '), f))
files.sort()
```

`glob('V*__*.sql')` lists the files whose names fit Flyway's pattern (Chapter 17 used `glob` for CSV files). `re.fullmatch` checks the whole name against a regular expression, the pattern language of section 14.2, just as pandas' `.str.fullmatch` did in Chapter 18: `(\d+)` captures the digits and `(.+)` the description, so `V3__add_payment_terms.sql` gives the number 3 and `add payment terms`. Sorting on the number puts `V10` after `V9`, where sorting the names as text would not. Second, read what the database has already run:

<!-- run: none -->
```python
applied = {int(v): c for v, c in (line.split('|') for line in psql(
    'SELECT version, checksum FROM schema_migrations;').splitlines() if line)}
```

`psql(…)` is a small function in the file that sends SQL to the `psql` client and returns what it prints. The result is a dictionary from version number to checksum. Third, for each file, compare checksums and stop on a mismatch:

<!-- run: none -->
```python
    body = f.read_text()
    checksum = hashlib.md5(body.encode()).hexdigest()
    if version in applied:
        if applied[version] != checksum:
            sys.exit(f'checksum mismatch: {f.name} was changed after it was applied. Write a new migration instead.')
        continue
```

`hashlib.md5(…).hexdigest()` turns the file's contents into a 32-character fingerprint; change one character of the file and the fingerprint changes. An applied file with the same fingerprint is skipped; one with a different fingerprint stops the run (`sys.exit`). Fourth, run a new file and its history row in one transaction:

<!-- run: none -->
```python
    psql('BEGIN;\n' + body + f"\nINSERT INTO schema_migrations (version, description, checksum) "
         f"VALUES ({version}, '{description}', '{checksum}');\nCOMMIT;\n")
    print(f'applied  {f.name}'); ran += 1
```

That's exactly what you typed by hand above: `BEGIN`, the change, the history row, `COMMIT`. The `psql` function runs the client with `-v ON_ERROR_STOP=1`, so the first error stops the file, and the transaction is rolled back. The whole file, with comments, is `migrate.py` in the companion folder.

**Try it.** Create an empty database for it in DBeaver: `CREATE DATABASE riverstone_lab_migrations;`. The runner connects through `psql` (section 28.1's box), which takes the user and password from two **environment variables** (section 26.4): `PGUSER` and `PGPASSWORD`. In the terminal, set them for this session (Git Bash, macOS, and Linux shown; in PowerShell write `$env:PGUSER = "postgres"`), putting your own password in place of the placeholder:

<!-- run: none -->
```
# terminal, in companion/ch28
$ export PGUSER=postgres
$ export PGPASSWORD='your-postgres-password'
```

They last until you close the terminal, and they never go into a file that could be shared. If `psql` isn't on your `PATH` (section 28.1, step 3), add `--psql` and the full path to it after `migrate.py`. Now run the runner twice, then make a quiet edit to V3 and run it a third time (type `python` instead of `python3` on Windows):

<!-- run: none -->
```
# terminal, in companion/ch28
$ python3 migrate.py --db riverstone_lab_migrations migrations
applied  V1__create_suppliers.sql
applied  V2__seed_suppliers.sql
applied  V3__add_payment_terms.sql
applied  V4__expand_add_supplier_city.sql
applied  V5__contract_drop_city.sql
database is at version 5
$ python3 migrate.py --db riverstone_lab_migrations migrations
nothing to apply; database is at version 5
$ echo "-- reviewed" >> migrations/V3__add_payment_terms.sql
$ cat migrations/V3__add_payment_terms.sql
ALTER TABLE suppliers ADD COLUMN payment_terms_days INTEGER NOT NULL DEFAULT 30;
-- reviewed
$ python3 migrate.py --db riverstone_lab_migrations migrations
checksum mismatch: V3__add_payment_terms.sql was changed after it was applied. Write a new migration instead.
```

**What each command does:**

- **`--db riverstone_lab_migrations`** names the database; **`migrations`** is the folder of files.
- The **first run** applies all five files in number order and reports the version reached.
- The **second run** is the point of the history table: running migrations is **idempotent** (running it again changes nothing).
- **`echo "-- reviewed" >> …`** adds a comment line to the end of V3. `>>` *appends* to a file; a single `>` would replace the whole file. The edit changes nothing about what V3 does, but it changes the file's fingerprint.
- The **third run** is the point of the checksum: a quiet edit to an applied migration would mean this database and every other copy now disagree about what "version 3" means, so the runner refuses to continue.

To tidy up, remove the comment line from V3 in your editor (or copy the file back from the companion download).

### Reviewing a migration

Before approving a migration, a reviewer asks:

1. **Does it run on a copy with realistic data?** Constraints that pass on an empty test table fail on real rows, as `gst_number` did.
2. **Does it lock a busy table?** Adding an index without `CONCURRENTLY`, changing a column's type, or adding a `NOT NULL` column can block writes on large tables. Test the duration on production-sized data.
3. **Does it break a reader?** Renames and drops go through expand and contract. Search the reports, views, and dbt models for the column name.
4. **Is data preserved?** A type change (`VARCHAR` to `INTEGER`) or a split column needs a data check before and after: row counts and a total.
5. **Is there a way back?** Either a written reverse migration, or a backup taken immediately before, with the restore tested (section 2.9).
6. **Is it one change?** Small migrations are quick to review and quick to fix. "V7__misc_changes.sql" is a warning sign.

---

## 28.13 The same SQL in MySQL

The ideas in this chapter all carry over to MySQL 8.0: recursive CTEs, frames, plans, indexes, normalization, grain, star schemas, and type 2 dimensions built with `UPDATE` and `INSERT`. The spellings below change. The companion file `ch28_queries_mysql.sql` has a tested MySQL version of every query. Everything here was run on MySQL 8.0.46. MySQL 8.0 reached the end of Oracle's standard support in April 2026; the current long-term-support releases are 8.4 and 9.7 (section 12.3), and the book's MySQL outputs have not been rerun on them, so check anything version-sensitive against the MySQL documentation for your release.

### Setting up

Load `riverstone_2025_setup_mysql.sql`, then `ch28_2025_addons_mysql.sql`. For the large database, follow section 28.1's box "Build riverstone_perf", using its MySQL note.

### What changes

| Feature | PostgreSQL | MySQL 8.0 |
|---|---|---|
| Recursive CTE | `WITH RECURSIVE` | same; recursion stops after 1,000 passes by default (`cte_max_recursion_depth`, section 28.2) |
| Column sizes in a recursive CTE | taken from both parts; types must match | taken from the anchor; `CAST` growing strings in the anchor |
| `SEARCH` / `CYCLE` clauses | yes (14+) | no; build a path string and check it |
| `GROUPS` frames, `EXCLUDE` | yes | no |
| `RANGE` with interval | `INTERVAL '6 days'` | `INTERVAL 6 DAY` |
| `PERCENTILE_CONT` | yes | no; use `NTILE` or `ROW_NUMBER` with `COUNT` |
| First of the month | `DATE_TRUNC('month', d)` | `CAST(DATE_FORMAT(d, '%Y-%m-01') AS DATE)` |
| Date as a number | `TO_CHAR(d, 'YYYYMMDD')` | `DATE_FORMAT(d, '%Y%m%d')` |
| A list of dates | `generate_series(…)` | a recursive CTE (section 28.2) or a calendar table |
| Type conversion | `x::date` or `CAST(x AS DATE)` | `CAST(x AS DATE)` only |
| Null-safe equals | `a IS NOT DISTINCT FROM b` | `a <=> b` |
| Null-safe "differs" | `a IS DISTINCT FROM b` | `NOT (a <=> b)` |
| Update from another table | `UPDATE t SET … FROM other WHERE …` | `UPDATE t JOIN other ON … SET …` |
| Automatic key | `INTEGER GENERATED ALWAYS AS IDENTITY` | `INT AUTO_INCREMENT` |
| A schema for the warehouse | `CREATE SCHEMA dw`; `DROP SCHEMA dw CASCADE` | a schema *is* a database: `CREATE DATABASE dw`; `DROP DATABASE dw` |
| Expression index | `ON customers (UPPER(city))` | `ON customers ((UPPER(city)))`, 8.0.13+ |
| Foreign key indexes | not automatic | created automatically by InnoDB |
| Partial indexes | yes | no (a functional index on a `CASE` expression can imitate one) |
| Covering index | `INCLUDE (…)` | no `INCLUDE`; add the columns to the index key |
| `EXPLAIN` output | text tree | `EXPLAIN FORMAT=TREE`; `EXPLAIN ANALYZE` (8.0.18+) |
| `MERGE` | yes (15+) | no; `INSERT … ON DUPLICATE KEY UPDATE` for type 1 |
| Materialized views | yes | no; summary tables |
| Transactional structure changes | yes: `ALTER` can be rolled back | no: each `ALTER`/`CREATE` commits immediately |
| Adding a `NOT NULL` column with no default to a table with rows | error | succeeds, filling rows with `''`, `0`, or a zero date |

### A tree in MySQL

<!-- db: riverstone_2025 -->

With no `SEARCH` clause, order an org chart by building a **sort path** of zero-padded ids. The anchor's `CAST(… AS CHAR(200))` sets the column's size; without it, MySQL sizes the column from the anchor's four-character first value, and the query stops with *ERROR 1406 (22001): Data too long for column 'sort_path' at row 1* as soon as the path grows.

```mysql
WITH RECURSIVE org AS (
    SELECT staff_id, staff_name, 1 AS level,
           CAST(LPAD(staff_id, 4, '0') AS CHAR(200)) AS sort_path
    FROM staff
    WHERE manager_id IS NULL
    UNION ALL
    SELECT s.staff_id, s.staff_name, o.level + 1,
           CONCAT(o.sort_path, '/', LPAD(s.staff_id, 4, '0'))
    FROM staff AS s
    JOIN org AS o ON s.manager_id = o.staff_id
)
SELECT CONCAT(REPEAT('    ', level - 1), staff_name) AS org_chart
FROM org
WHERE sort_path LIKE '0100/0110%'
ORDER BY sort_path;
```

```
+----------------------------+
| org_chart                  |
+----------------------------+
|     Anita Rao              |
|         Vikram Singh       |
|             Neha Kulkarni  |
|             Rahul Mehta    |
|         Farah Khan         |
|         Meera Iyer         |
|         Arjun Nair         |
|             Divya Krishnan |
|             Vivek Chandran |
|             Sneha Pillai   |
|         Pooja Desai        |
|             Nisha Bhatt    |
|             Aditya Verma   |
|             Rohit Kamat    |
|         Sandeep Gill       |
|             Karan Ahuja    |
|             Ritu Bansal    |
+----------------------------+
```

`WHERE sort_path LIKE '0100/0110%'` keeps Anita Rao's branch (staff 110 under 100). The same path string is also the loop check of section 28.2's defense 2: in the recursive part, add `WHERE LOCATE(LPAD(s.staff_id, 4, '0'), o.sort_path) = 0`. `LOCATE(text, path)` returns where `text` first appears in `path`, or 0 if it doesn't, so the walk never visits an id twice; on Riverstone's clean data it still returns all 35 people.

MySQL's safety limit for runaway recursion, `cte_max_recursion_depth`, is in section 28.2's first example.

### Frames

`RANGE` with an interval works:

```mysql
SELECT order_date,
       COUNT(*) OVER (ORDER BY order_date
                      RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW) AS orders_last_7_days
FROM orders
WHERE order_date BETWEEN '2025-02-14' AND '2025-02-21'
ORDER BY order_date, order_id;
```

```
+------------+--------------------+
| order_date | orders_last_7_days |
+------------+--------------------+
| 2025-02-16 |                  2 |
| 2025-02-16 |                  2 |
| 2025-02-17 |                  4 |
| 2025-02-17 |                  4 |
| 2025-02-20 |                  6 |
| 2025-02-20 |                  6 |
+------------+--------------------+
```

`GROUPS` does not:

```mysql
SELECT order_date,
       COUNT(*) OVER (ORDER BY order_date GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW) AS orders_in_frame
FROM orders
LIMIT 3;
```

```
ERROR 1235 (42000): This version of MySQL doesn't yet support 'GROUPS'
```

### Plans in MySQL

MySQL's tree format reads the same way as PostgreSQL's, inside out. Here are the December queries from section 28.6 on `riverstone_perf` in MySQL, after `CREATE INDEX idx_orders_order_date ON orders (order_date);` (recorded output, test machine). `EXPLAIN ANALYZE` runs the query and prints the tree:

<!-- run: none -->
```mysql
EXPLAIN ANALYZE
SELECT COUNT(*) FROM orders
WHERE EXTRACT(YEAR FROM order_date) = 2025 AND EXTRACT(MONTH FROM order_date) = 12;
```

```
-> Aggregate: count(0)  (cost=143003 rows=1) (actual time=131..131 rows=1 loops=1)
    -> Filter: ((extract(year from orders.order_date) = 2025) and (extract(month from orders.order_date) = 12))  (cost=71803 rows=712008) (actual time=125..129 rows=25078 loops=1)
        -> Covering index scan on orders using idx_orders_order_date  (cost=71803 rows=712008) (actual time=0.548..81 rows=714285 loops=1)
```

<!-- run: none -->
```mysql
EXPLAIN ANALYZE
SELECT COUNT(*) FROM orders
WHERE order_date >= '2025-12-01' AND order_date < '2026-01-01';
```

```
-> Aggregate: count(0)  (cost=14488 rows=1) (actual time=6.74..6.74 rows=1 loops=1)
    -> Filter: ((orders.order_date >= DATE'2025-12-01') and (orders.order_date < DATE'2026-01-01'))  (cost=9672 rows=48152) (actual time=0.308..5.62 rows=25078 loops=1)
        -> Covering index range scan on orders using idx_orders_order_date over ('2025-12-01' <= order_date < '2026-01-01')  (cost=9672 rows=48152) (actual time=0.306..3.19 rows=25078 loops=1)
```

The lesson transfers exactly. The `EXTRACT` version reads all 714,285 index entries (MySQL is clever enough to scan the small index instead of the table, but it still reads everything), with a median of 136 ms; the range reads only December's 25,078, with a median of 7.09 ms. And MySQL needed no index for the single-customer lookup: its automatic foreign-key index on `customer_id` gave a median of 0.17 ms straight after loading, the same as PostgreSQL's after section 28.5 added one.

### Type 1 without MERGE

MySQL's upsert updates a row when the primary key already exists, and inserts it otherwise. To try it, build section 28.10's two starting tables in your MySQL lab. The lab database from Chapter 12 may already exist; `IF NOT EXISTS` makes the first line safe either way:

<!-- lab:start -->

<!-- run: mysql -->
```sql
CREATE DATABASE IF NOT EXISTS riverstone_lab;
```

Then, connected to `riverstone_lab` in MySQL, the same statements as section 28.10:

```mysql
CREATE TABLE dim_customer_t1 (
    customer_id  INTEGER PRIMARY KEY,
    customer     VARCHAR(100) NOT NULL,
    city         VARCHAR(50),
    segment      VARCHAR(30)
);

INSERT INTO dim_customer_t1 VALUES
(1, 'Sharma Hardware',   'Mumbai', 'Retail'),
(3, 'Green Leaf Hotels', 'Pune',   'Hospitality');

CREATE TABLE customer_extract (
    customer_id  INTEGER PRIMARY KEY,
    customer     VARCHAR(100) NOT NULL,
    city         VARCHAR(50),
    segment      VARCHAR(30)
);

INSERT INTO customer_extract VALUES
(1, 'Sharma Hardware',   'Thane',   'Retail'),
(3, 'Green Leaf Hotels', 'Pune',    'Hospitality'),
(4, 'Coastal Foods',     'Chennai', 'Wholesale');
```

Now the upsert, and the result:

```mysql
INSERT INTO dim_customer_t1 (customer_id, customer, city, segment)
SELECT customer_id, customer, city, segment
FROM customer_extract AS x
ON DUPLICATE KEY UPDATE city = x.city, segment = x.segment;

SELECT * FROM dim_customer_t1 ORDER BY customer_id;
```

```
+-------------+-------------------+---------+-------------+
| customer_id | customer          | city    | segment     |
+-------------+-------------------+---------+-------------+
|           1 | Sharma Hardware   | Thane   | Retail      |
|           3 | Green Leaf Hotels | Pune    | Hospitality |
|           4 | Coastal Foods     | Chennai | Wholesale   |
+-------------+-------------------+---------+-------------+
```

<!-- lab:end -->

**How it works:** the `INSERT … SELECT` tries to insert every extract row. Rows 1 and 3 already exist, so their primary keys clash, and instead of an error, `ON DUPLICATE KEY UPDATE` runs: it sets the city and segment from the extract row (`x.city`). Row 4 is new and is simply inserted. The same result as `MERGE` in section 28.10. Unlike `MERGE`, it has no `WHEN MATCHED AND …` condition, so every clashing row goes through the update, changed or not.

The type 2 load (close, then insert) works as in section 28.10, except that MySQL's multi-table `UPDATE` is written `UPDATE dim_customer_t2 AS d JOIN customer_extract AS x ON … SET …`. Both versions are in `ch28_queries_mysql.sql`.

> **Watch out: MySQL can't roll back an ALTER TABLE.** In MySQL, `CREATE`, `ALTER`, and `DROP` commit immediately, even inside `BEGIN … COMMIT`. A migration that fails halfway leaves the first half applied. Keep each MySQL migration to one structure change, and test it on a copy.

**Good place to stop.**

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Recursive CTE with no loop protection | Query runs until cancelled, or MySQL stops after 1,000 passes | Add a depth limit, a path check, or PostgreSQL's `CYCLE` clause |
| Anchor and recursive part with different column types | *recursive query … has type numeric(8,3) in non-recursive term* (PostgreSQL); *Data too long* (MySQL) | `CAST` the anchor's columns to the wider type |
| Adding BOM quantities instead of multiplying them down the tree | Material needs far too low for multi-level products | Multiply each child's quantity by its parent's running quantity |
| Walking a hierarchy with orphan rows | Some people or parts silently missing from the result | Compare the walk's row count with the table; `LEFT JOIN` to find missing managers |
| `LAST_VALUE` with the default frame | "Latest" value equals the current row | Frame `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` |
| `ROWS` frame on data with missing days | "Last 7 days" really covers several weeks | `RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW` |
| Tuning on a tiny test database | Every plan is a sequential scan and every query is instant; production is slow | Test plans on production-sized data |
| Function wrapped around an indexed column | `Seq Scan` with a huge `Rows Removed by Filter`, although an index exists | Rewrite as a range, or create an expression index |
| No index on a PostgreSQL foreign key | Joins and deletes on the child table slow down as it grows | Index foreign key columns you join or delete through |
| Composite index in the wrong column order | Index exists but isn't used for the query | Equality columns first, range column last |
| Indexing every column "just in case" | Loads and inserts get slower; indexes bigger than the table | Index for measured, frequent queries; drop redundant indexes |
| Trusting estimated costs as timings | Surprise when a "cheap" plan is slow | Use `EXPLAIN ANALYZE`; costs are relative units |
| `EXPLAIN ANALYZE` on a `DELETE` or `UPDATE` | Rows really changed | Wrap in `BEGIN; … ROLLBACK;` |
| Moving the charged price into the products table while normalizing | Past orders show today's prices | Separate list price (product) from price charged (order line) |
| Joining tables of different grains, then summing | Totals several times too large, with no error (₹45,00,000 target for January) | Aggregate to a common grain first |
| `valid_to` set to the last day of a version, with a half-open join | Facts dated on the last day of the old version vanish from inner joins | Store the next version's start date in `valid_to` |
| Joining facts to a type 2 dimension on the business key | Revenue counted once per customer version | Join on the surrogate key, or on the key plus the date range |
| Using type 1 for attributes reports are sliced by | Last year's segment or territory totals change without new data | Use type 2 and say which view the report shows |
| Materialized view nobody refreshes | Dashboard numbers stop moving; everyone trusts them | Schedule the refresh and show "data as of" |
| Editing a migration that was already applied | Databases drift; tools report checksum errors | Never edit; add a new migration |
| Renaming or dropping a column in one step | Reports and applications break the moment it runs | Expand, migrate readers, then contract |
| Adding `NOT NULL` without a default to a table with rows | PostgreSQL: *column … contains null values*; MySQL: no error, rows silently get `''` or `0` | Add a `DEFAULT`, or add nullable, backfill, then set `NOT NULL` |

---

## In the real world: the dashboard that got slower every month

It's March 2026. Vikram Singh opens the sales dashboard in the Monday review and waits. The customer page, the December comparison, and the three-year trend each take a few seconds, and the whole team watches the spinner. *"This was instant when we launched it,"* he says. *"Can someone look at it before next Monday?"*

Meera Iyer takes it. She's tempted to start adding indexes, but she has seen that go wrong: an index on the busy orders table during working hours would block order entry while it builds. So she works the checklist from section 28.6, on a copy of the reporting database, which (like `riverstone_perf`) holds three years of orders.

**First, find where the time goes.** She copies the dashboard's four queries out of the report and runs each with `EXPLAIN (ANALYZE, BUFFERS)`. The numbers below are the chapter's measured medians, from queries of the same shape:

| Dashboard tile | Median | What the plan shows |
|---|---|---|
| Customer page: one customer's revenue | 262.47 ms | `Seq Scan on order_items`: 1.9 million lines read for 108 |
| December orders compared with last year | 131.33 ms | `Seq Scan on orders` with `EXTRACT(YEAR …)` in the filter |
| Pending orders list | 44.12 ms | `Seq Scan`, 710,355 rows removed |
| Three-year monthly trend by category | 2,626 ms | Hash joins over every non-cancelled line |

The trend tile is 85.7% of the 3,064 ms total. That's the headline for Vikram: one tile is the problem, and it's a different kind of problem from the other three.

**Second, fix each for the right reason.**

- *Customer page.* `order_items.order_id` has no index. The ERP vendor's MySQL version had one automatically; the PostgreSQL reporting copy doesn't. One index: 0.64 ms.
- *December comparison.* No index is missing: the filter can't use the one on `order_date`. She rewrites `EXTRACT(YEAR FROM order_date) = 2025 AND EXTRACT(MONTH FROM order_date) = 12` as a date range. 2.95 ms, no database change needed.
- *Pending list.* A partial index on pending orders: 48 kB, 0.75 ms.
- *Trend.* No index can help a question that reads three years of lines. The numbers only change once a day, so a materialized view refreshed at 06:00 turns it into a 144-row table. Refresh: about 2 seconds a night. Reading it: 0.10 ms.

**Third, check she hasn't broken anything.** The trend from the materialized view matches the live query for every month and category. She measures the cost to writes too: the reporting copy is loaded nightly, and the chapter's test showed four indexes making a large insert about five and a half times slower. One new index and one partial index add seconds to a load that runs once a night, which is acceptable, and she writes that down.

**Fourth, ship it properly.** She doesn't run anything on the reporting database herself. She writes three migrations, `V14__index_order_items_order_id.sql` and `V15__index_orders_pending.sql` (each with `CREATE INDEX CONCURRENTLY`, each in its own non-transactional migration) and `V16__monthly_category_revenue.sql`, and a change to the dashboard's December query. The data engineer reviews them against section 28.12's checklist and applies them on Wednesday evening. The refresh joins the nightly job, and the trend tile gets a caption: *"Data as of 06:00 today."*

**What she tells Vikram:** *"The dashboard's four tiles took about 3 seconds of database time; they now take under 5 milliseconds. Three fixes were missing or misused indexes. The fourth was the trend chart re-adding three years of orders every time anyone opened it; it now reads a summary refreshed every morning, so it won't show today's orders until tomorrow. Nothing changes for anyone entering orders."*

Notice what made it work. The measurement came first, so she fixed the tile that mattered most. Each fix matched its cause, rather than "add indexes until it's fast". Every change went through a reviewed migration. And the one trade-off, a trend that's a day old, was put in front of the person who owns the decision.

---

## Project: a star schema with history

**Goal:** a small, reconciled data warehouse for one business process, with a type 2 dimension, that a BI tool can read without knowing anything about the source tables.

### Tools you'll need

Versions used for this chapter, checked in September 2026:

- **PostgreSQL 15 or later** (every query was run on PostgreSQL 16 on Ubuntu 24.04; the current release is 18, section 12.3). `CYCLE` and `SEARCH` need 14 or later, `MERGE` needs 15 or later. The `psql` client comes with the server.
- **MySQL** (every MySQL query was run on 8.0.46). MySQL 8.0 reached the end of Oracle's standard support in April 2026; install a current long-term-support release (8.4 or 9.7, section 12.3). `EXPLAIN ANALYZE` needs 8.0.18 or later, and expression indexes need 8.0.13 or later.
- **DBeaver** for running queries. Its *Explain execution plan* button shows plans as a tree; `EXPLAIN (ANALYZE, BUFFERS)` in the editor gives the full text.
- **Python** (Chapter 17's installation; tested on 3.11 and 3.12) for `generate_riverstone_perf.py`, `migrate.py`, and `ch28_perf.py`. All three use only the standard library; `migrate.py` and `ch28_perf.py` call the `psql` client.
- **A plan visualizer (optional).** Several free tools turn PostgreSQL's `EXPLAIN (ANALYZE, FORMAT JSON)` output into a diagram. Paste plans only from practice data, never from a production database containing customer data.
- **Migration tools.** Flyway (Redgate; the free edition covers versioned SQL migrations), Liquibase, and Alembic for Python projects. Check the current release and edition details on each tool's documentation site before you install. This chapter describes Flyway's conventions from Redgate's documentation; `migrate.py` demonstrates the same mechanism.
- **Companion files for this chapter:** `ch28_2025_addons.sql` and `ch28_2025_addons_mysql.sql` (staff, parts, BOM, customer changes), `generate_riverstone_perf.py` (the large database), `ch28_perf.py` (reruns every timing experiment and writes `ch28_perf_log.txt`), `ch28_star_schema.sql` (the `dw` schema from section 28.9), `migrate.py` with its `migrations/` folder, and `ch28_queries_mysql.sql` (every query in MySQL).

**Option A: your own work data.** Choose a process you report on (orders, tickets, payments) and a dimension that changes over time (customer segment, account owner, region). Work on a copy, never the production database, and remove or mask personal data before you start. Keep the project on your own machine unless your employer has agreed otherwise.

**Option B: Riverstone.** Use `riverstone_2025` and the tables from this chapter.

**Steps:**

1. **Write the design on one page:** the business process, the grain of the fact table in one sentence, the dimensions, the facts, and for each dimension attribute whether changes are type 1 or type 2, with a reason.
2. **Build the date dimension** for your period, with at least day name, month, quarter, and fiscal year (April to March).
3. **Build the other dimensions**, each with a surrogate key. Add an "unknown" row wherever the source has missing values.
4. **Build the type 2 dimension** from your change history (Riverstone: `customer_changes`). Check that each business key has exactly one current row and no gaps or overlaps between versions.
5. **Load the fact table** with a point-in-time join to the type 2 dimension.
6. **Reconcile.** Row counts and totals against the source (Riverstone: ₹43,35,471 and 326 lines). Hand-check one fact row end to end.
7. **Answer three business questions** from the star: one by date attribute, one "as it was" versus "as it is" by the changing attribute, one that uses the unknown row.
8. **Make it repeatable.** Put the build into numbered migration files for the structures and one load script for the data, so the whole warehouse can be dropped and rebuilt from nothing.

**Deliverables:** the one-page design, the SQL files, the reconciliation query and its output, and a half-page note with the three answers.

**Stretch goals:**

- Add a second fact table at a different grain (monthly targets, or invoices) that shares `dim_date`, and build a report that puts both side by side correctly.
- Write the type 2 load as an *incremental* script: given tomorrow's extract, it closes and inserts only what changed. Run it twice to prove that the second run changes nothing.
- Load the star into Power BI (Chapter 16) and confirm that the model view shows a star.
- Build the same warehouse in MySQL and list every change you had to make.

---

## Recap

- A **recursive CTE** has an **anchor** and a **recursive part** joined by `UNION ALL`; each pass reads only the previous pass's rows, and it repeats until a pass finds nothing new. The anchor fixes the columns' types. It can build lists (a date spine) as well as walk trees. Use it for org charts, **bills of materials** (multiply quantities down the tree), and **where-used** queries. Guard against loops with a depth limit, a path, or `CYCLE` (MySQL stops at 1,000 passes); order a tree with `SEARCH DEPTH FIRST`.
- **Frames:** `ROWS` counts rows, `GROUPS` counts peer groups, `RANGE` measures values (with intervals for calendar windows). `EXCLUDE` removes the current row or its peers; the `WINDOW` clause names a window for reuse. Windows see only the rows `WHERE` kept. `PERCENTILE_CONT` interpolates, `PERCENTILE_DISC` returns a real value; `NTILE` gives equal-count bands.
- Tables live in **pages**. A **sequential scan** reads them all; a **B-tree index** finds rows through sorted keys. `EXPLAIN` shows the plan and estimates; `EXPLAIN ANALYZE` runs it and measures.
- Index **foreign keys** you join on (PostgreSQL doesn't do it for you), keep filters **sargable**, order **composite** indexes equality-first, and use **covering** and **partial** indexes for important, frequent queries. Every index slows writes.
- **Normalization:** **1NF** one value per cell; **2NF** no partial dependencies; **3NF** no transitive dependencies. It removes update, insert, and delete anomalies.
- **Grain:** say it, test it, never join different grains and then sum, and aggregate to a common grain first.
- **Dimensional modeling:** a **fact table** at a declared grain, surrounded by **dimensions** with **surrogate keys**, including a **date dimension**. Prefer a **star** to a **snowflake**. Facts come as transactions, periodic snapshots, or accumulating snapshots.
- **Slowly changing dimensions:** **type 1** overwrites, **type 2** adds a version with validity dates (`valid_to` = the next version's `valid_from`), **type 3** keeps a previous value. Join type 2 dimensions on the surrogate key or with a **point-in-time join**.
- **Denormalize** only for a measured problem, from a normalized source, with an automated refresh and visible staleness. **Materialized views** trade freshness for speed.
- **Migrations** are numbered, reviewed, never-edited scripts recorded in a history table. Change live structures with **expand and contract**.

---

## Key terms

recursive CTE · `RECURSIVE` · anchor · recursive part · working table (previous pass) · `cte_max_recursion_depth` · `UNION ALL` in recursion · hierarchy · bill of materials (BOM) · exploding a BOM · where-used query · `CYCLE` clause · `SEARCH DEPTH FIRST` · frame type · `GROUPS` frame · peer group · `EXCLUDE` · `WINDOW` clause (recap) · ordered-set aggregate · `PERCENTILE_CONT` (recap) · `PERCENTILE_DISC` · `NTILE` (recap) · page · sequential scan · index · B-tree · leaf page · statistics · query plan · `EXPLAIN` · `EXPLAIN ANALYZE` · cost · heap · index scan · bitmap scan · index-only scan · nested loop join · hash join · merge join · selective · sargable · expression index · composite index · covering index · partial index · normal form · first normal form (1NF) · update anomaly · insert anomaly · delete anomaly · functional dependency · partial dependency · second normal form (2NF) · transitive dependency · third normal form (3NF) · Boyce–Codd normal form (BCNF) · candidate key · surrogate key · natural (business) key · grain (recap) · dimensional modeling · fact · measure · dimension · fact table (recap) · dimension table (recap) · star schema (recap) · snowflake schema · date dimension (recap) · transaction fact table · periodic snapshot · accumulating snapshot · conformed dimension · slowly changing dimension (SCD) · type 1 · type 2 · type 3 · `MERGE` · point-in-time join · denormalization · materialized view · staleness · migration · drift · schema history table · checksum · repeatable migration · idempotent · expand and contract

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can write a recursive CTE that walks down or up a hierarchy, and explain the anchor, the recursive part, and when it stops.
- [ ] I multiply quantities down a bill of materials and can reconcile a rolled-up cost by hand.
- [ ] I protect recursive queries against loops, and I check that no rows went missing.
- [ ] I choose `ROWS`, `RANGE`, or `GROUPS` deliberately, and use intervals for calendar windows.
- [ ] I can read an `EXPLAIN ANALYZE` plan from the inside out and point to the expensive step.
- [ ] I know why a function on an indexed column prevents index use, and how to rewrite it.
- [ ] I can justify an index (single, composite, covering, or partial) with a before-and-after measurement, and I know what it costs.
- [ ] I can take a table to 3NF and name the dependency each step removes.
- [ ] I state the grain of every table before joining it, and test it with a query.
- [ ] I can design a star schema and load a type 2 dimension with a point-in-time join.
- [ ] I can explain when to denormalize and how to keep a summary honest.
- [ ] I never change a shared database by hand; I write a numbered, reviewed migration, and I use expand and contract for renames.

---

## Exercises

Use `riverstone_2025` (with this chapter's companion tables and the `dw` schema from section 28.9) unless an exercise says otherwise. Exercises 9 and 15 continue in `riverstone_lab`. Predict the shape of each result before running it.

### Warm-up

1. Using a recursive CTE, list everyone who reports to Ramesh Patil, directly or indirectly, with their level *relative to him* (his direct reports are level 1).
2. How many people are at each level of the whole organization? Check that the levels add up to 35.
3. State the grain of `lead_stage_history` in one sentence, and write a query that tests it.
4. Find any staff whose `manager_id` points to a staff member who doesn't exist. (A correct query can return no rows. Explain how you know it would catch an orphan.)

### Core

5. Produce the whole company as an indented org chart, each manager followed by their team, using PostgreSQL's `SEARCH DEPTH FIRST BY` clause.
6. For the Storage Box 25L, list each bought material, its total quantity per box, and its cost per box. Check that the costs add up to the material cost in section 28.2.
7. Purchasing plans to make 500 Garden Chairs and 1,000 Storage Box 10L next month. How many kilograms of polypropylene granules are needed?
8. For each day in December 2025 that had orders, show that day's number of orders and the number of orders in the 30 days up to and including that day.
9. *(Lab.)* In section 28.7, `orders_3nf` still stores the sales rep's name. Create `sales_reps_3nf` (with a surrogate key) and `orders_3nf_v2` that stores only the rep's key, then show that orders per rep are unchanged.
10. Using the star schema, show 2025 net revenue by customer city **as it was** and **as it is** for the cities where the two differ.

### Stretch

11. Build a monthly sales-versus-target report from the star schema: one row per month, with revenue, target, and percentage of target. Explain in one sentence why you aggregated before joining.
12. Show the median order value for each customer segment (as it was) using `PERCENTILE_CONT`, and compare it with the mean.
13. Here's a staff extract with a data-entry error. Use `CYCLE` to find the loop, and list the ids that are in it: `(10, NULL), (11, 10), (12, 14), (13, 12), (14, 13), (15, 11)`, as `(staff_id, manager_id)`.
14. For each month of 2025, show revenue and the average revenue of the **other** months in the same half-year (January–June or July–December).
15. *(Lab.)* Continue section 28.10's type 2 dimension. A new extract on 1 May 2026 changes Green Leaf Hotels' segment from Hospitality to Retail, and nothing else. Apply it with the same two steps, then show every version of every customer.

### Think about it (no SQL needed)

16. A query plan shows `Seq Scan on orders … Filter: (status = 'Delivered') … Rows Removed by Filter: 25235`, on a table where 96% of orders are delivered. A colleague wants to add an index on `status`. What do you tell them?
17. Rewrite each condition so it can use a plain index on its column, or explain why it can't be done: (a) `WHERE DATE(created_at) = '2025-12-15'` on a timestamp column; (b) `WHERE order_date + INTERVAL '30 days' > DATE '2025-12-31'`; (c) `WHERE LOWER(email) = 'rakesh@sharmahardware.example'`; (d) `WHERE customer_name LIKE '%Traders'`.
18. Vikram asks for the customer's segment to be copied onto every row of `orders` "so reports don't need a join". Give two risks and a better alternative.
19. For each attribute, choose SCD type 1, 2, or 3, with a reason: (a) customer phone number; (b) customer's sales territory, used for commission reports; (c) product category, after a one-off reorganization that management wants to compare side by side for a year; (d) a misspelled customer name.
20. Review this migration for a 700,000-row, busy `orders` table and list what's wrong: `ALTER TABLE orders RENAME COLUMN status TO order_status; ALTER TABLE orders ADD COLUMN channel VARCHAR(20) NOT NULL; CREATE INDEX idx_orders_channel ON orders (channel);`

### MySQL track (optional)

21. *(MySQL.)* Write exercise 2 (people per level) in MySQL.
22. *(MySQL.)* Write the where-used query for the fastener pack (part 306) in MySQL: which products use it, and how many packs per unit?
23. *(MySQL.)* Build a **daily** date spine for December 2025 with a recursive CTE. Use it to show how many days the month had, how many of those days had no orders, and the month's total revenue. Check the total against Chapter 13 (section 13.6).

---

## Answers

**1.** Start the anchor at Ramesh Patil's direct reports, not at Ramesh himself:

<!-- db: riverstone_2025 -->

```sql
WITH RECURSIVE team AS (
    SELECT staff_id, staff_name, job_title, 1 AS level
    FROM staff
    WHERE manager_id = (SELECT staff_id FROM staff WHERE staff_name = 'Ramesh Patil')
    UNION ALL
    SELECT s.staff_id, s.staff_name, s.job_title, t.level + 1
    FROM staff AS s
    JOIN team AS t ON s.manager_id = t.staff_id
)
SELECT level, staff_name, job_title
FROM team
ORDER BY level, staff_id;
```

```
 level |  staff_name  |     job_title
-------+--------------+-------------------
     1 | Ajay Kumar   | Shift Supervisor
     1 | Farhan Ali   | Quality Inspector
     2 | Gopal Sahu   | Machine Operator
     2 | Sunita Pawar | Machine Operator
(4 rows)
```

Four people, matching Ramesh Patil's `people_below` of 4 in section 28.2. ✓ A common mistake is to anchor on Ramesh himself and forget to exclude him, which returns five rows.

**2.**

```sql
WITH RECURSIVE org AS (
    SELECT staff_id, 1 AS level FROM staff WHERE manager_id IS NULL
    UNION ALL
    SELECT s.staff_id, o.level + 1
    FROM staff AS s
    JOIN org AS o ON s.manager_id = o.staff_id
)
SELECT level, COUNT(*) AS people
FROM org
GROUP BY level
ORDER BY level;
```

```
 level | people
-------+--------
     1 |      1
     2 |      8
     3 |     10
     4 |     13
     5 |      3
(5 rows)
```

1 + 8 + 10 + 13 + 3 = 35. ✓

**3.** Grain: *one lead entering one stage.* If that's true, `(lead_id, stage)` is unique:

```sql
SELECT lead_id, stage, COUNT(*) AS copies
FROM lead_stage_history
GROUP BY lead_id, stage
HAVING COUNT(*) > 1;
```

```
 lead_id | stage | copies
---------+-------+--------
(0 rows)
```

No rows: the grain holds. (The table's primary key already enforces it, but the test still belongs in a data-quality check, because keys are often missing from warehouse copies.)

**4.**

```sql
SELECT s.staff_id, s.staff_name, s.manager_id
FROM staff AS s
LEFT JOIN staff AS m ON m.staff_id = s.manager_id
WHERE s.manager_id IS NOT NULL
  AND m.staff_id IS NULL;
```

```
 staff_id | staff_name | manager_id
----------+------------+------------
(0 rows)
```

No orphans. The query would catch one because the `LEFT JOIN` keeps every person, and a `manager_id` with no matching staff row leaves `m.staff_id` NULL. The `manager_id IS NOT NULL` condition stops the managing director, who legitimately has no manager, from being reported. (The foreign key on `manager_id` prevents orphans in this table; copies loaded into spreadsheets or warehouses often lack it.)

**5.**

```sql
WITH RECURSIVE org AS (
    SELECT staff_id, staff_name, manager_id, 1 AS level
    FROM staff
    WHERE manager_id IS NULL
    UNION ALL
    SELECT s.staff_id, s.staff_name, s.manager_id, o.level + 1
    FROM staff AS s
    JOIN org AS o ON s.manager_id = o.staff_id
)
SEARCH DEPTH FIRST BY staff_id SET visit_order
SELECT repeat('    ', level - 1) || staff_name AS org_chart
FROM org
ORDER BY visit_order;
```

```
          org_chart
------------------------------
 Arvind Kapoor
     Anita Rao
         Vikram Singh
             Neha Kulkarni
             Rahul Mehta
         Farah Khan
         Meera Iyer
         Arjun Nair
             Divya Krishnan
             Vivek Chandran
             Sneha Pillai
         Pooja Desai
             Nisha Bhatt
             Aditya Verma
             Rohit Kamat
         Sandeep Gill
             Karan Ahuja
             Ritu Bansal
     Suresh Menon
         Priya Nambiar
     Harpreet Sethi
         Ramesh Patil
             Ajay Kumar
                 Gopal Sahu
                 Sunita Pawar
             Farhan Ali
         Kiran Bhosale
             Swati Joshi
                 Farid Shaikh
     Joseph D'Souza
     Mahesh Yadav
         Mohan Das
     Lakshmi Reddy
     Zoya Mirza
     Tenzin Dorji
(35 rows)
```

`SEARCH DEPTH FIRST BY staff_id` adds a hidden column, here named `visit_order`, that sorts each person immediately after their manager, with siblings in `staff_id` order. `SEARCH BREADTH FIRST` would sort level by level instead, like section 28.2's org chart query.

**6.**

```sql
WITH RECURSIVE explode AS (
    SELECT b.child_part_id, CAST(b.quantity AS NUMERIC) AS qty
    FROM bom_lines AS b
    WHERE b.parent_part_id = 102
    UNION ALL
    SELECT b.child_part_id, e.qty * b.quantity
    FROM explode AS e
    JOIN bom_lines AS b ON b.parent_part_id = e.child_part_id
)
SELECT p.part_name,
       CAST(SUM(e.qty) AS NUMERIC(8,3))                   AS qty_per_box,
       p.unit,
       CAST(SUM(e.qty) * p.material_cost AS NUMERIC(10,2)) AS cost_per_box
FROM explode AS e
JOIN parts AS p ON p.part_id = e.child_part_id
WHERE p.part_type = 'Material'
GROUP BY p.part_id, p.part_name, p.unit, p.material_cost
ORDER BY p.part_id;
```

```
       part_name        | qty_per_box | unit | cost_per_box
------------------------+-------------+------+--------------
 Polypropylene granules |       1.500 | kg   |       165.00
 Color masterbatch      |       0.055 | kg   |        14.30
 Product label          |       1.000 | each |         2.00
 Shipping carton        |       1.000 | each |        18.00
(4 rows)
```

₹165.00 + ₹14.30 + ₹2.00 + ₹18.00 = ₹199.30, matching section 28.2. ✓ The granules are 1.1 kg in the body plus 0.4 kg in the lid, so group by part before multiplying by cost.

**7.**

```sql
WITH RECURSIVE plan (product_id, units) AS (
    VALUES (106, 500), (101, 1000)
),
explode AS (
    SELECT b.child_part_id, CAST(b.quantity * p.units AS NUMERIC) AS qty
    FROM plan AS p
    JOIN bom_lines AS b ON b.parent_part_id = p.product_id
    UNION ALL
    SELECT b.child_part_id, e.qty * b.quantity
    FROM explode AS e
    JOIN bom_lines AS b ON b.parent_part_id = e.child_part_id
)
SELECT CAST(SUM(qty) AS NUMERIC(10,1)) AS kg_polypropylene
FROM explode
WHERE child_part_id = 301;
```

```
 kg_polypropylene
------------------
           1850.0
(1 row)
```

Hand-check: a chair needs 2.2 kg (500 × 2.2 = 1,100 kg); a 10-litre box needs 0.55 + 0.20 = 0.75 kg (1,000 × 0.75 = 750 kg). Total 1,850 kg. ✓ Putting the production plan into a `VALUES` list at the start makes the anchor multiply by planned units, so the rest of the query is unchanged. (The first CTE isn't recursive; `WITH RECURSIVE` is written once for the whole list.)

**8.** Count orders per day first (the grain is one day), then use a `RANGE` frame. Starting the daily counts 29 days before December makes the first December rows see a full 30 days:

```sql
WITH daily AS (
    SELECT order_date, COUNT(DISTINCT order_id) AS orders
    FROM sales_lines
    WHERE order_date >= DATE '2025-11-02'
    GROUP BY order_date
),
rolling AS (
    SELECT order_date,
           orders,
           SUM(orders) OVER (ORDER BY order_date
                             RANGE BETWEEN INTERVAL '29 days' PRECEDING AND CURRENT ROW) AS orders_last_30_days
    FROM daily
)
SELECT *
FROM rolling
WHERE order_date >= DATE '2025-12-01'
ORDER BY order_date;
```

```
 order_date | orders | orders_last_30_days
------------+--------+---------------------
 2025-12-01 |      2 |                  23
 2025-12-04 |      1 |                  23
 2025-12-05 |      1 |                  23
 2025-12-08 |      1 |                  23
 2025-12-10 |      2 |                  22
 2025-12-12 |      1 |                  20
 2025-12-13 |      1 |                  21
 2025-12-14 |      1 |                  22
 2025-12-16 |      3 |                  22
 2025-12-17 |      1 |                  23
 2025-12-18 |      1 |                  23
 2025-12-19 |      1 |                  23
 2025-12-21 |      1 |                  24
 2025-12-23 |      1 |                  22
(14 rows)
```

`INTERVAL '29 days' PRECEDING AND CURRENT ROW` covers 30 days including today. The common wrong answer is `ROWS BETWEEN 29 PRECEDING AND CURRENT ROW`, which covers 30 *order days*, more than a month in this data.

**9.**

<!-- lab:start -->

```sql
CREATE TABLE sales_reps_3nf (
    sales_rep_id  INTEGER PRIMARY KEY,
    sales_rep     VARCHAR(100) NOT NULL UNIQUE
);

INSERT INTO sales_reps_3nf
SELECT ROW_NUMBER() OVER (ORDER BY sales_rep), sales_rep
FROM (SELECT DISTINCT sales_rep FROM orders_3nf) AS r;

CREATE TABLE orders_3nf_v2 AS
SELECT o.order_id, o.order_date, o.customer_id, r.sales_rep_id
FROM orders_3nf AS o
JOIN sales_reps_3nf AS r ON r.sales_rep = o.sales_rep;

SELECT 'before' AS version, sales_rep, COUNT(*) AS orders
FROM orders_3nf
GROUP BY sales_rep
UNION ALL
SELECT 'after', r.sales_rep, COUNT(*)
FROM orders_3nf_v2 AS o
JOIN sales_reps_3nf AS r ON r.sales_rep_id = o.sales_rep_id
GROUP BY r.sales_rep
ORDER BY sales_rep, version DESC;
```

```
 version |   sales_rep   | orders
---------+---------------+--------
 before  | Farah Khan    |      2
 after   | Farah Khan    |      2
 before  | Neha Kulkarni |      3
 after   | Neha Kulkarni |      3
 before  | Rahul Mehta   |      1
 after   | Rahul Mehta   |      1
(6 rows)
```

Same counts before and after (2 + 1 + 3 = 6 orders). ✓ The rep's name now lives in one row, so a corrected spelling fixes every order at once.

<!-- lab:end -->

**10.**

```sql
WITH was AS (
    SELECT c.city, SUM(f.net_revenue) AS revenue
    FROM dw.fact_sales_line AS f
    JOIN dw.dim_customer AS c ON c.customer_key = f.customer_key
    GROUP BY c.city
),
is_now AS (
    SELECT cur.city, SUM(f.net_revenue) AS revenue
    FROM dw.fact_sales_line AS f
    JOIN dw.dim_customer AS c   ON c.customer_key = f.customer_key
    JOIN dw.dim_customer AS cur ON cur.customer_id = c.customer_id AND cur.is_current
    GROUP BY cur.city
)
SELECT COALESCE(w.city, i.city) AS city,
       ROUND(w.revenue)         AS revenue_as_it_was,
       ROUND(i.revenue)         AS revenue_as_it_is
FROM was AS w
FULL JOIN is_now AS i ON i.city = w.city
WHERE w.revenue IS DISTINCT FROM i.revenue
ORDER BY city;
```

```
  city  | revenue_as_it_was | revenue_as_it_is
--------+-------------------+------------------
 Mumbai |            928760 |          1080800
 Thane  |            152040 |
(2 rows)
```

Only Metro Mart moved city, so only Mumbai and Thane differ: Metro Mart's orders from January to June 2025 count under Thane as they were. The `FULL JOIN` matters: Thane has no revenue "as it is" (no current customer is in Thane), and an inner join would drop it.

**11.**

```sql
WITH monthly AS (
    SELECT d.month_start, SUM(f.net_revenue) AS revenue
    FROM dw.fact_sales_line AS f
    JOIN dw.dim_date AS d ON d.date_key = f.date_key
    GROUP BY d.month_start
)
SELECT m.month_start,
       ROUND(m.revenue)        AS revenue,
       ROUND(t.target_revenue) AS target,
       ROUND(100 * m.revenue / t.target_revenue, 1) AS pct_of_target
FROM monthly AS m
JOIN sales_targets AS t ON t.target_month = m.month_start
ORDER BY m.month_start;
```

```
 month_start | revenue | target | pct_of_target
-------------+---------+--------+---------------
 2025-01-01  |  202640 | 300000 |          67.5
 2025-02-01  |  253664 | 300000 |          84.6
 2025-03-01  |  278008 | 320000 |          86.9
 2025-04-01  |  210282 | 320000 |          65.7
 2025-05-01  |  329359 | 320000 |         102.9
 2025-06-01  |  186928 | 300000 |          62.3
 2025-07-01  |  232692 | 280000 |          83.1
 2025-08-01  |  329282 | 320000 |         102.9
 2025-09-01  |  558315 | 380000 |         146.9
 2025-10-01  |  681071 | 520000 |         131.0
 2025-11-01  |  633408 | 500000 |         126.7
 2025-12-01  |  439824 | 380000 |         115.7
(12 rows)
```

The fact table's grain is one order line and the target's grain is one month; aggregating the facts to months first makes the join one-to-one, so the target is counted once (section 28.8). January's 67.5% matches section 28.8. ✓

**12.**

```sql
WITH order_values AS (
    SELECT c.segment, f.order_id, SUM(f.net_revenue) AS order_value
    FROM dw.fact_sales_line AS f
    JOIN dw.dim_customer AS c ON c.customer_key = f.customer_key
    GROUP BY c.segment, f.order_id
)
SELECT segment,
       COUNT(*)                AS orders,
       ROUND(AVG(order_value)) AS mean_value,
       ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_value)::NUMERIC) AS median_value
FROM order_values
GROUP BY segment
ORDER BY segment;
```

```
   segment   | orders | mean_value | median_value
-------------+--------+------------+--------------
 Hospitality |     59 |      19390 |        17589
 Retail      |     62 |      25381 |        22649
 Wholesale   |     52 |      31112 |        29199
(3 rows)
```

The order counts add up to 173. ✓ In every segment the mean is above the median, so each segment has a few large orders pulling its average up. `PERCENTILE_CONT` is an aggregate, so it works with `GROUP BY` like `AVG`.

**13.**

```sql
WITH RECURSIVE extract_rows (staff_id, manager_id) AS (
    VALUES (10, NULL), (11, 10), (12, 14), (13, 12), (14, 13), (15, 11)
),
walk AS (
    SELECT staff_id, manager_id, staff_id AS started_at
    FROM extract_rows
    UNION ALL
    SELECT e.staff_id, e.manager_id, w.started_at
    FROM extract_rows AS e
    JOIN walk AS w ON e.staff_id = w.manager_id
)
CYCLE staff_id SET is_loop USING visited
SELECT DISTINCT started_at AS staff_in_loop
FROM walk
WHERE is_loop AND staff_id = started_at
ORDER BY started_at;
```

```
 staff_in_loop
---------------
            12
            13
            14
(3 rows)
```

The walk starts at every person and goes up the chain. People 10, 11, and 15 reach the top (10 has no manager). Starting from 12, 13, or 14, the walk comes back to its starting person, so those three form the loop (12 → 14 → 13 → 12). Filtering on `staff_id = started_at` keeps only people who return to themselves; someone *below* a loop would reach it without returning to their own id.

**14.**

```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month,
           SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY 1
)
SELECT month,
       ROUND(revenue) AS revenue,
       ROUND(AVG(revenue) OVER (
             PARTITION BY EXTRACT(MONTH FROM month) <= 6
             ORDER BY month
             ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
             EXCLUDE CURRENT ROW)) AS avg_other_months_in_half
FROM monthly
ORDER BY month;
```

```
   month    | revenue | avg_other_months_in_half
------------+---------+--------------------------
 2025-01-01 |  202640 |                   251648
 2025-02-01 |  253664 |                   241443
 2025-03-01 |  278008 |                   236574
 2025-04-01 |  210282 |                   250120
 2025-05-01 |  329359 |                   226304
 2025-06-01 |  186928 |                   254790
 2025-07-01 |  232692 |                   528380
 2025-08-01 |  329282 |                   509062
 2025-09-01 |  558315 |                   463255
 2025-10-01 |  681071 |                   438704
 2025-11-01 |  633408 |                   448237
 2025-12-01 |  439824 |                   486954
(12 rows)
```

Partitioning by the true/false expression `EXTRACT(MONTH FROM month) <= 6` makes two halves. Each month is compared with the five others in its half.

**15.**

<!-- lab:start -->

```sql
DELETE FROM customer_extract;
INSERT INTO customer_extract VALUES
(1, 'Sharma Hardware',   'Thane',   'Retail'),
(3, 'Green Leaf Hotels', 'Pune',    'Retail'),
(4, 'Coastal Foods',     'Chennai', 'Wholesale');

BEGIN;

UPDATE dim_customer_t2 AS d
SET valid_to = DATE '2026-05-01',
    is_current = FALSE
FROM customer_extract AS x
WHERE d.customer_id = x.customer_id
  AND d.is_current
  AND (d.city IS DISTINCT FROM x.city OR d.segment IS DISTINCT FROM x.segment);

INSERT INTO dim_customer_t2 (customer_id, customer, city, segment, valid_from)
SELECT x.customer_id, x.customer, x.city, x.segment, DATE '2026-05-01'
FROM customer_extract AS x
LEFT JOIN dim_customer_t2 AS d
       ON d.customer_id = x.customer_id AND d.is_current
WHERE d.customer_id IS NULL;

COMMIT;

SELECT customer_key, customer, city, segment, valid_from, valid_to, is_current
FROM dim_customer_t2
ORDER BY customer_id, valid_from;
```

```
 customer_key |     customer      |  city   |   segment   | valid_from |  valid_to  | is_current
--------------+-------------------+---------+-------------+------------+------------+------------
            1 | Sharma Hardware   | Mumbai  | Retail      | 2024-11-04 | 2026-04-01 | f
            3 | Sharma Hardware   | Thane   | Retail      | 2026-04-01 | 9999-12-31 | t
            2 | Green Leaf Hotels | Pune    | Hospitality | 2024-09-08 | 2026-05-01 | f
            5 | Green Leaf Hotels | Pune    | Retail      | 2026-05-01 | 9999-12-31 | t
            4 | Coastal Foods     | Chennai | Wholesale   | 2026-04-01 | 9999-12-31 | t
(5 rows)
```

<!-- lab:end -->

Only Green Leaf Hotels gets a new version. Sharma Hardware and Coastal Foods are unchanged, so step 1 leaves their current rows open and step 2 finds they already have one. Running the same two steps a second time would change nothing, which is how you check a load is idempotent. (`valid_to` stores the first day the version is no longer true, which is the next version's `valid_from`, as in `dw.dim_customer`. With half-open joins (`>= valid_from AND < valid_to`) there is then no gap and no overlap. If you store the last day a version was true instead (an inclusive convention, 2026-04-30), you must join with `<= valid_to`. Mixing the two drops or doubles rows at every change.)

**16.** Don't add it. The filter keeps 96% of rows, so an index on `status` would be slower than scanning: the planner would ignore it, as it did for `'Delivered'` in section 28.5, and every insert and status change would pay to maintain it. If a query really needs the rare statuses (pending or cancelled), a **partial index** on those rows is the right tool. And if the delivered query is slow, the fix is elsewhere: a summary table, or not reading every delivered order.

**17.**
(a) `WHERE created_at >= '2025-12-15' AND created_at < '2025-12-16'`. The half-open range also includes times after midnight, which `BETWEEN '2025-12-15' AND '2025-12-15'` would miss.
(b) Move the arithmetic to the constant side: `WHERE order_date > DATE '2025-12-31' - INTERVAL '30 days'`, which is `order_date > '2025-12-01'`.
(c) Store emails in one case when they're saved and compare directly, or create an expression index on `LOWER(email)` and keep the query as written.
(d) A plain B-tree index can't find text by its *ending*. Options: a reversed-text expression index, a trigram index (PostgreSQL's `pg_trgm` extension), or a separate `business_type` column. The common wrong answer is "add an index on `customer_name`", which the planner would not use for a leading `%`.

**18.** Risks: (1) the copies disagree when a customer's segment changes and not every order is updated, an update anomaly (section 28.7); (2) it's unclear whether an order should show the segment at the time of the order or today's, and the copy silently picks one. Better alternatives: a star schema with a type 2 customer dimension (both views available, section 28.10), or a view that joins orders to customers so reports don't write the join themselves. If the join is truly too slow, a materialized view refreshed on a schedule keeps the copy derived and rebuildable.

**19.**
(a) Type 1. Nobody reports sales by old phone numbers; the new one replaces it.
(b) Type 2. Commission is calculated on who owned the customer when the sale happened, so history must be kept.
(c) Type 3. A `previous_category` column lets reports show this year's sales under both the old and new categories side by side, which is exactly the request. (If they later wanted the full history, type 2 would be needed.)
(d) Type 1. It's a correction: the misspelled name was never true, so there's no history to keep.

**20.** Five problems. (1) The rename breaks every report, view, and application that reads `status`, at the moment it runs: use expand and contract. (2) `channel VARCHAR(20) NOT NULL` with no default fails on a table with rows (*column "channel" … contains null values*): add a default, or add it nullable, backfill, then set `NOT NULL`. (3) A plain `CREATE INDEX` blocks writes on a busy table while it builds: use `CREATE INDEX CONCURRENTLY`, in its own migration outside a transaction. (4) Three unrelated changes in one migration: split them. (5) An index on `channel` before anyone has measured a query that needs it: add it only for a known query, preferably with a before-and-after plan.

**21.**

```mysql
WITH RECURSIVE org AS (
    SELECT staff_id, 1 AS level FROM staff WHERE manager_id IS NULL
    UNION ALL
    SELECT s.staff_id, o.level + 1
    FROM staff AS s
    JOIN org AS o ON s.manager_id = o.staff_id
)
SELECT level, COUNT(*) AS people
FROM org
GROUP BY level
ORDER BY level;
```

```
+-------+--------+
| level | people |
+-------+--------+
|     1 |      1 |
|     2 |      8 |
|     3 |     10 |
|     4 |     13 |
|     5 |      3 |
+-------+--------+
```

Identical to PostgreSQL's result in exercise 2. No `CAST` is needed, because `level` is a number and doesn't grow in size.

**22.**

```mysql
WITH RECURSIVE uses AS (
    SELECT b.parent_part_id, CAST(b.quantity AS DECIMAL(12,3)) AS qty
    FROM bom_lines AS b
    WHERE b.child_part_id = 306
    UNION ALL
    SELECT b.parent_part_id, CAST(u.qty * b.quantity AS DECIMAL(12,3))
    FROM uses AS u
    JOIN bom_lines AS b ON b.child_part_id = u.parent_part_id
)
SELECT p.part_name, SUM(u.qty) AS packs_per_unit
FROM uses AS u
JOIN parts AS p ON p.part_id = u.parent_part_id
WHERE p.part_type = 'Product'
GROUP BY p.part_name;
```

```
+--------------+----------------+
| part_name    | packs_per_unit |
+--------------+----------------+
| Garden Chair |          3.000 |
+--------------+----------------+
```

Three packs per Garden Chair: one in the frame and one in each of the two leg assemblies (Figure 28.2). ✓ In MySQL, the `CAST` in both parts keeps the column's type fixed, so the multiplied quantities aren't cut to the anchor's precision.

**23.** A recursive CTE produces the 31 days; a left join keeps the days with no sales:

```mysql
WITH RECURSIVE days AS (
    SELECT DATE '2025-12-01' AS day
    UNION ALL
    SELECT day + INTERVAL 1 DAY
    FROM days
    WHERE day < DATE '2025-12-31'
),
daily_sales AS (
    SELECT order_date, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE order_date >= '2025-12-01' AND order_date < '2026-01-01'
    GROUP BY order_date
)
SELECT COUNT(*)                                          AS days_in_month,
       SUM(CASE WHEN s.order_date IS NULL THEN 1 ELSE 0 END) AS days_without_orders,
       ROUND(SUM(COALESCE(s.revenue, 0)), 0)             AS month_revenue
FROM days AS d
LEFT JOIN daily_sales AS s ON s.order_date = d.day;
```

```
+---------------+---------------------+---------------+
| days_in_month | days_without_orders | month_revenue |
+---------------+---------------------+---------------+
|            31 |                  17 |        439824 |
+---------------+---------------------+---------------+
```

The revenue matches December in section 13.6 (₹4,39,824). ✓ Orders came in on only 14 of December's 31 days, which is normal for a B2B supplier whose customers order every few weeks, and a reason daily charts for this kind of business need a date spine: without one, the 17 empty days would simply vanish. `SUM(CASE WHEN s.order_date IS NULL THEN 1 ELSE 0 END)` counts the unmatched days. A 31-row spine needs 30 passes, well within MySQL's 1,000-pass limit, so no setting needs changing.

---

## Where this leads

- **Chapter 34, The Command Line, Linux & Networking Basics,** comes next in Part 3's reading order. It takes the terminal you used for `riverstone_perf` and `migrate.py` further: `PATH`, shell scripts, servers, and the network between you and a database.
- **Chapter 29, Python as Software, Not Scripts,** turns scripts like `migrate.py` and `generate_riverstone_perf.py` into tested, packaged code.
- **Chapter 32, Analytics Engineering with dbt,** rebuilds this chapter's star schema as dbt models with tests, documentation, and snapshots for type 2 history, replacing hand-written load scripts.
- **Chapter 47, Data Quality, Observability & Contracts,** turns grain tests and reconciliations into automated daily checks.
- **Chapter 49, Storage, Warehouses & Lakehouses,** takes the same questions of speed and cost to cloud warehouses, partitioning, and columnar storage.
- **Chapter 62, Data Architecture Patterns,** compares warehouse modeling approaches at the architect's level.
- **Chapter 71, SQL Question Bank,** has interview questions on recursive CTEs, indexes, query plans, normalization, grain, and slowly changing dimensions; **Chapter 77** covers data modeling in data engineering and system design interviews.
