# Chapter 77. Data Engineering & Data System Design Bank

*Part 8 — The Interview Playbook*

> **Chapter at a glance**
>
> **You will learn to:** answer the pipeline, data-modeling, and system-design questions that come up in Data Engineer interviews · design a batch or streaming pipeline live, under time pressure, the way an interviewer actually wants · reason correctly about idempotency, partitioning, and schema evolution, not just define the terms · walk through a full system design case end to end, stating trade-offs out loud.
>
> **Before you start:** Chapter 69 (the three answer tiers and the twelve extra-point moves). The questions test Part 5 (Chapters 45–52: ingestion, pipelines, data quality, distributed compute, storage, streaming, activation and deployment) and Chapter 28 (query plans, grain, the star schema, slowly changing dimensions). They also link to Chapter 12, section 12.13 (the upsert), Chapter 33 (queues and graphs), Chapter 61 (partitioning and sharding), and the two banks this one leans on, Chapter 71 (SQL) and Chapter 72A (complexity). This chapter tests those skills; it doesn't teach them again, with one exception: Q77-018 builds topological sort step by step, because no earlier chapter does.
>
> **Time needed:** 3–4 hours for a first pass (about 10 minutes per core question, including running its code, and 1–2 minutes per rapid-fire row), plus 1 hour for the final-week list.
>
> **How this chapter is built.** Same format as the other question banks in Part 8 (Chapters 70 onward): every core question leads with a **"Remember it as…"** hook, then a one-line answer, then a compact tier table (what **passes**, what's **strong**, and the **extra points**, tagged with Chapter 69's moves: **[+Trade-offs]**, **[+Edge cases]**, **[+Validate]** and so on). Rapid-fire sections are scan tables: question, one-line answer, one extra point, level, and where to learn it. **Every SQL result shown was run on PostgreSQL 16** in `riverstone_lab`, the practice database you created in Chapter 12, section 12.13; each demo drops its tables at the end. **Every Python output is real**, from Python 3.11.15 with the standard library only (the book recommends Python 3.14, Chapter 17, section 17.0; nothing here depends on the version). The sections run from pipeline fundamentals to modeling, reliability, orchestration, scale and quality, and end with full system-design walk-throughs.
>
> **Levels and roles.** Each core question carries a level and the roles that usually ask it. **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds. **DE** data engineer · **AE** analytics engineer · **MLE** machine learning engineer · **ARCH** data architect. **Learn it in** pointers name the chapter and section where each idea is taught, mostly Part 5 (Chapters 45–52) and Chapter 28 (data modeling); where another bank drills it, a **Practise it with** pointer follows.

---

## 77.1 Pipeline fundamentals

### Q77-001 · ETL vs. ELT: what's the actual difference, and when does it matter which you pick?

**Level:** Fresher · **Roles:** DE, AE

**Remember it as:** *ETL transforms before loading, in a separate processing step. ELT loads raw data first and transforms inside the warehouse itself, using the warehouse's own compute.*

**Answer in one line:** **ETL** (Extract, Transform, Load) transforms data in a separate processing layer before it ever reaches the destination system; **ELT** (Extract, Load, Transform) loads raw data into the destination (usually a modern cloud warehouse) first, then transforms it there using the warehouse's own compute power, which became the dominant pattern once cloud warehouses got cheap and powerful enough to make that practical.

| Tier | What to say |
|---|---|
| Passes | "ETL and ELT do the same three steps in a different order" (technically true, misses why the order matters) |
| Strong | + explains the practical driver: ELT keeps a full copy of raw data in the warehouse (useful for reprocessing or auditing later), and pushes transformation compute onto the warehouse rather than a separate processing cluster |
| Extra points | + **[+Trade-offs]** ELT's "load everything raw first" approach means raw, unvalidated data briefly exists in the warehouse before transformation, a real consideration for compliance-sensitive data + **[+Business]** the choice is rarely purely technical anymore; it's often driven by which the team's existing tooling (dbt, Airflow, a specific cloud warehouse) is already built around |

**Likely follow-ups:** Name a scenario where ETL is still clearly the better choice today. What's reverse ETL, and how does it relate to either pattern?
**Red flag:** treating the two as interchangeable synonyms.
**Learn it in:** Chapter 32, §32.1 (ETL versus ELT) and Chapter 45, §45.1 (where company data comes from, and the warehouse's layers). Reverse ETL: Chapter 51.

### Q77-002 · Batch vs. streaming: how do you decide which a new pipeline actually needs?

**Level:** Fresher · **Roles:** DE, MLE

**Remember it as:** *Ask how fresh the answer actually needs to be, in business terms, before assuming streaming is the more impressive, more correct choice.*

**Answer in one line:** **Batch** processing runs on a schedule (hourly, daily), processing accumulated data in one pass, simpler to build and debug; **streaming** processes events continuously as they arrive, needed when a decision genuinely can't wait for the next batch window, and the right choice depends entirely on how fresh the downstream decision actually needs to be, not on which technology is more modern.

| Tier | What to say |
|---|---|
| Passes | "Streaming is more real-time and modern, so it's generally better" |
| Strong | The freshness-driven decision above, with a concrete example each: a daily sales summary report is a natural batch case; a fraud-detection system blocking a transaction in real time is a natural streaming case |
| Extra points | + **[+Business]** streaming systems are meaningfully harder to build, test, and debug correctly (exactly-once semantics, out-of-order events, windowing) than batch ones; choosing streaming for a problem that doesn't actually need sub-minute freshness is real, avoidable added complexity, not a sign of engineering sophistication |

**Likely follow-ups:** What's micro-batching, and where does it sit between the two? How would you migrate an existing batch pipeline to streaming without a risky big-bang rewrite?
**Red flag:** recommending streaming by default without asking what freshness the actual decision requires.
**Learn it in:** Chapter 50, §50.1 (what "real-time" actually means) and §50.8 (when Riverstone would not build a stream).

### Rapid-fire, 77.1

Roles: DE and AE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q77-003 | What's a data warehouse vs. a data lake vs. a lakehouse? | Structured, schema-on-write, optimized for analytics queries / raw, schema-on-read, stores any format cheaply / a hybrid combining a lake's flexible storage with a warehouse's structured querying and transaction support | **[+Trade-offs]** a lakehouse is a lake plus a table format (Delta Lake, Iceberg) that gives plain files transactions, schema changes and time travel | Fresher · 49.1, 49.5, 49.7; star schema 28.9 |
| Q77-004 | What's a data contract? | An explicit agreement between a data producer and consumer about a dataset's schema, format, and update cadence, so downstream pipelines don't silently break when the source changes | **[+Business]** the DE-team equivalent of an API contract between two services | Mid · 47.7 |
| Q77-005 | What's the difference between a full load and an incremental load? | A full load reprocesses the entire source every run; an incremental load processes only new or changed records since the last run, using a timestamp or change-tracking mechanism | **[+Trade-offs]** full loads are simpler and self-healing but don't scale to large sources; incremental loads scale but need careful handling of updates and deletes, not just new rows | Fresher · 45.3–45.4 |
| Q77-006 | What's CDC (Change Data Capture)? | A technique for detecting and capturing row-level changes (inserts, updates, deletes) in a source database, often by reading its transaction log, to drive incremental pipelines without querying the whole source table | **[+Business]** CDC avoids the "how do I know what changed" problem incremental loading otherwise has to solve with timestamps, which can miss deletes entirely | Mid · 45.6 |

---

## 77.2 Basic-but-tricky data engineering questions

### Q77-007 · Your pipeline runs on a schedule, but if it fails and gets re-run, it duplicates every row it already loaded. What's the fix?

**Level:** Fresher · **Roles:** DE, AE

**Remember it as:** *A pipeline that can safely run twice with the same input and produce the same result is idempotent. One that can't, isn't safe to retry, ever.*

**Answer in one line:** Make the load step **idempotent**: use an upsert (insert-or-update) keyed on a unique identifier instead of a plain insert, so re-running the same load with the same data updates existing rows instead of duplicating them.

**Verified, in `riverstone_lab`.** First the table. The primary key on `order_date` is what makes "the same day" detectable:

<!-- lab:start -->

<!-- Verifier setup, not printed: the lab database the reader made in Chapter 12.
```sql
CREATE DATABASE riverstone_lab;
```
-->

```sql
CREATE TABLE daily_summary (
    order_date     DATE PRIMARY KEY,
    total_revenue  NUMERIC(12,2) NOT NULL
);
```

Now the load step. ₹20,900 is Riverstone's real net revenue on 5 January 2025 (one order, in `riverstone_2025`):

```sql
INSERT INTO daily_summary VALUES ('2025-01-05', 20900.00)
    ON CONFLICT (order_date)
    DO UPDATE SET total_revenue = EXCLUDED.total_revenue;

SELECT * FROM daily_summary;
```

```
 order_date | total_revenue
------------+---------------
 2025-01-05 |      20900.00
(1 row)
```

- **`ON CONFLICT (order_date)`** names the unique column to check. If a row for that date already exists, PostgreSQL doesn't insert; it runs the `DO UPDATE` part instead.
- **`EXCLUDED`** means "the row you tried to insert" (Chapter 12, section 12.13), so `total_revenue = EXCLUDED.total_revenue` copies the new value onto the existing row.

The job fails later that night and gets re-run. Run the exact same statement a second time, then count the rows:

```sql
INSERT INTO daily_summary VALUES ('2025-01-05', 20900.00)
    ON CONFLICT (order_date)
    DO UPDATE SET total_revenue = EXCLUDED.total_revenue;

SELECT COUNT(*) FROM daily_summary;
```

```
 count
-------
     1
(1 row)
```

One row, not two. **What if the table had no primary key?** Try the same upsert on a copy without one, and predict what happens before you run it:

```sql
CREATE TABLE daily_summary_nokey (
    order_date     DATE,
    total_revenue  NUMERIC(12,2) NOT NULL
);

INSERT INTO daily_summary_nokey VALUES ('2025-01-05', 20900.00)
    ON CONFLICT (order_date)
    DO UPDATE SET total_revenue = EXCLUDED.total_revenue;
```

```
ERROR:  there is no unique or exclusion constraint matching the ON CONFLICT specification
```

`ON CONFLICT` only works when the conflict column is declared unique: without the key, the database has no way to tell that two rows are "the same day". Clean up:

```sql
DROP TABLE daily_summary, daily_summary_nokey;
```

<!-- lab:end -->

| Tier | What to say |
|---|---|
| Passes | "Add a check to skip rows that already exist" (a partial fix, misses the case where a value genuinely needs updating on retry) |
| Strong | The upsert pattern above, explaining that idempotency means safe *retry*, not just avoiding duplicates on first run, and that the upsert needs a unique key on the business key (here, the date) |
| Extra points | + **[+Validate]** the real proof above: the same statement run twice leaves exactly one row, not two + **[+Business]** idempotency is what makes "just re-run the failed job" a safe, boring operational response instead of a risky one that needs careful manual cleanup first |

**Likely follow-ups:** How would you make a multi-step pipeline (not just one insert) idempotent end to end? What's the difference between idempotency and exactly-once processing?
**Red flag:** a fix that only prevents duplicates on a clean re-run, not one that's genuinely safe to retry after a partial failure mid-load.
**Learn it in:** Chapter 12, §12.13 (step 7, the upsert); Chapter 45, §45.5 (why upserts make loads safe to repeat); Chapter 46, §46.4 (idempotency, proven with a failure test).

### Q77-008 · What's the difference between "at-least-once," "at-most-once," and "exactly-once" delivery, and which is actually achievable?

**Level:** Mid · **Roles:** DE, MLE

**Remember it as:** *At-least-once can duplicate. At-most-once can lose data. Exactly-once, in the strict sense, usually isn't really achievable end to end, only effectively achievable by combining at-least-once delivery with idempotent processing on the receiving end.*

**Answer in one line:** **At-least-once** guarantees a message is delivered, possibly more than once (safe against loss, risks duplication); **at-most-once** guarantees no duplication, possibly at the cost of losing a message entirely (safe against duplication, risks loss); true **exactly-once** delivery across a genuinely distributed system is famously difficult and, in most real systems, achieved in practice by combining at-least-once delivery with idempotent processing downstream (Q77-007), not by a delivery mechanism that's magically exactly-once on its own.

| Tier | What to say |
|---|---|
| Passes | Defines at-least-once and at-most-once correctly, but treats exactly-once as a setting you switch on |
| Strong | The three-way distinction above, and specifically names idempotent processing as the real mechanism behind most practical "exactly-once" claims |
| Extra points | + **[+Signpost]** this is precisely why Q77-007's upsert pattern matters beyond just convenience: it's what turns an honestly at-least-once delivery guarantee into an effectively exactly-once *outcome* + **[+Trade-offs]** the other route, used by Spark checkpoints and Kafka transactions (Chapter 50, §50.3), commits the output and the read position together in one transaction: real exactly-once, but narrower and slower |

**Likely follow-ups:** Which would you choose for a financial transaction log, and why? What's a real system that claims exactly-once, and how does it actually achieve it under the hood?
**Red flag:** treating "exactly-once" as a simple guarantee some systems just have and others don't, with no understanding of how it's actually achieved.
**Learn it in:** Chapter 50, §50.3 (delivery guarantees, and the duplicates you will get) and Chapter 51, §51.4 (making writes idempotent, and proving it).

### Rapid-fire, 77.2

Roles: DE and AE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q77-009 | What's schema drift, and why is it dangerous in an automated pipeline? | A source system's schema changing (a renamed column, a new field, a changed data type) without the downstream pipeline being updated to match, often causing a silent failure or silently wrong data rather than a loud error | **[+Business]** a pipeline that fails loudly on schema drift is far safer than one that silently adapts (or silently drops the new column), which can hide the problem for weeks | Mid · 45.8; contracts 47.7 |
| Q77-010 | What's backfilling, and why does it need special care? | Reprocessing historical data, usually after a bug fix or a new metric definition; needs care because it can be expensive at scale, and because downstream reports or dashboards using the old values need a plan for the transition, not just silently different historical numbers | **[+Edge cases]** a backfill that changes historical numbers without any announcement is a fast way to lose a stakeholder's trust in a dashboard | Mid · 46.5 |
| Q77-011 | Why can't you always trust a source system's own "last modified" timestamp for incremental loading? | Clock skew between systems, a source that doesn't update the timestamp on every field change, or a source that allows backdated edits can all make a naive timestamp-based incremental load silently miss real changes | **[+Edge cases]** no timestamp ever shows a deleted row, because nothing is left to carry one; CDC (Q77-006) reads deletes from the log | Mid · 45.4–45.6 |
| Q77-012 | What's a dead-letter queue? | A separate holding location for messages or records that failed processing repeatedly, so they don't block the rest of the pipeline and can be investigated separately | **[+Business]** without one, a single malformed record can silently halt an entire stream or repeatedly retry and fail forever | Fresher · 50.7 (the dead-letter path) |

---

## 77.3 Data modeling for pipelines and warehouses

### Q77-013 · Implement Slowly Changing Dimension (SCD) Type 2 for a customer whose segment changes, and explain why Type 1 wouldn't preserve history

**Level:** Mid · **Roles:** DE, AE

**Remember it as:** *Type 1 overwrites, so the past is gone. Type 2 closes the old row and opens a new one, so you can always ask "what did we believe was true on this date."*

**Answer in one line:** **SCD Type 1** overwrites the old value in place, losing all history of what it used to be; **SCD Type 2** keeps every historical version as its own row, with validity date ranges (and usually a current-flag), so you can query the dimension as it looked at any point in the past, not just as it looks today.

**Verified, in `riverstone_lab`.** The change is a real one: `riverstone_2025`'s `customer_changes` table (Chapter 28, section 28.1) records Harbour Traders, customer 11, moving from Retail to Wholesale on 1 September 2025. First the dimension, holding the customer's first version:

<!-- lab:start -->

```sql
CREATE TABLE customer_history (
    customer_key   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id    INTEGER NOT NULL,
    customer_name  VARCHAR(100) NOT NULL,
    segment        VARCHAR(30) NOT NULL,
    valid_from     DATE NOT NULL,
    valid_to       DATE NOT NULL DEFAULT '9999-12-31',
    is_current     BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO customer_history (customer_id, customer_name, segment, valid_from)
VALUES (11, 'Harbour Traders', 'Retail', '2025-04-09');
```

- **`customer_key`** is the surrogate key: the database numbers the versions 1, 2, 3… by itself, as in Chapter 28, section 28.10. `customer_id` is the business key, and it repeats, once per version.
- **`valid_from` and `valid_to`** form a half-open period: the version is true from `valid_from` up to, but not including, `valid_to`. So **`valid_to` is the first day the row is no longer true**, and `9999-12-31` means "still true". 9 April 2025 is the day Harbour Traders signed up.

Now the change: close the old version and open the new one, inside one transaction, so nobody ever sees the customer with no current row:

```sql
BEGIN;

UPDATE customer_history
SET valid_to   = '2025-09-01',
    is_current = FALSE
WHERE customer_id = 11
  AND is_current;

INSERT INTO customer_history (customer_id, customer_name, segment, valid_from)
VALUES (11, 'Harbour Traders', 'Wholesale', '2025-09-01');

COMMIT;

SELECT * FROM customer_history ORDER BY customer_key;
```

```
 customer_key | customer_id |  customer_name  |  segment  | valid_from |  valid_to  | is_current
--------------+-------------+-----------------+-----------+------------+------------+------------
            1 |          11 | Harbour Traders | Retail    | 2025-04-09 | 2025-09-01 | f
            2 |          11 | Harbour Traders | Wholesale | 2025-09-01 | 9999-12-31 | t
(2 rows)
```

`BEGIN` and `COMMIT` make the two statements one transaction (Chapter 12, section 12.13, step 8): either both happen or neither does. The `UPDATE` closes version 1 by setting its `valid_to` to the change date and `is_current` to `FALSE`; `AND is_current` makes sure only the open version is touched. The `INSERT` adds version 2, and its `customer_key`, `valid_to` and `is_current` take their defaults. The old row closes on the same date the new one opens. Check the two days either side of the change with the same half-open test a fact table join uses (`date >= valid_from AND date < valid_to`):

```sql
SELECT segment FROM customer_history
WHERE customer_id = 11
  AND DATE '2025-08-31' >= valid_from
  AND DATE '2025-08-31' <  valid_to;

SELECT segment FROM customer_history
WHERE customer_id = 11
  AND DATE '2025-09-01' >= valid_from
  AND DATE '2025-09-01' <  valid_to;
```

```
 segment
---------
 Retail
(1 row)

  segment
-----------
 Wholesale
(1 row)
```

Every day falls in exactly one version: no gap, no overlap. Clean up:

```sql
DROP TABLE customer_history;
```

<!-- lab:end -->

| Tier | What to say |
|---|---|
| Passes | Can define Type 1 vs Type 2 in the abstract, can't produce a working implementation |
| Strong | The working two-statement pattern above: close the current row, insert the new one, both inside the same transaction, with a surrogate key for each version |
| Extra points | + **[+Validate]** the real output above shows both the historical (Retail, closed) and current (Wholesale, open) rows coexisting, which is the entire point, and the two date checks show the half-open periods leave no gap + **[+Business]** this is exactly why "what was this customer's segment when they placed order X" is answerable with Type 2 history and not with Type 1, which would show only ever the current segment regardless of when the order was placed, silently misattributing every historical order to the wrong segment |

**Likely follow-ups:** What's SCD Type 3, and when would you use it instead of Type 2? How would you handle a fact table that needs to join to the *correct historical version* of a Type 2 dimension, not just the current one?
**Red flag:** implementing this with a plain `UPDATE` that overwrites the segment in place, silently losing history despite believing Type 2 was implemented.
**Learn it in:** Chapter 28, §28.9–28.10 (dimensional modeling; slowly changing dimensions), and Chapter 32, §32.9 (dbt snapshots do Type 2 for you).

### Rapid-fire, 77.3

Roles: DE and AE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q77-014 | Star schema vs. snowflake schema? | A star schema's dimension tables are fully denormalized (flat); a snowflake schema further normalizes dimensions into sub-tables, trading some query simplicity for reduced redundancy | **[+Trade-offs]** dimension tables are small, so a star's repetition costs little, and BI tools such as Power BI work best with a star: default to it | Fresher · 28.9, 16.3 (practise: 70.7) |
| Q77-015 | What's a surrogate key, and why use one instead of a natural key? | A system-generated, meaningless identifier (often a sequential integer) used as a table's primary key, instead of a real-world identifier like an email or SSN that could change, be reused, or vary in format across sources | **[+Business]** a surrogate key is exactly what makes SCD Type 2 workable: the natural business key (customer_id) repeats across history rows, but each row still needs its own unique surrogate key | Fresher · 28.7, 28.10 |
| Q77-016 | What's a fact table's grain, and why must it be decided before building anything else? | The level of detail one row represents (one order line, one daily summary, one customer-month); every measure and every join in the model depends on the grain being consistent and explicit | **[+Edge cases]** mixing grains in one fact table (some rows per-order, some pre-aggregated per-day) is a common, subtle modeling error that silently breaks any `SUM` across the whole table | Mid · 28.8 |
| Q77-017 | What's a junk dimension? | A single dimension table combining several small, low-cardinality flags or indicators that don't deserve their own separate dimension tables (for Riverstone's order lines, the order status and a yes/no "discounted" flag), reducing the number of tables a fact table needs to join against | **[+Trade-offs]** trades a slightly less "clean" model for meaningfully fewer joins in every query against the fact table | Mid · 28.9 (junk dimensions) |

---

## 77.4 Orchestration and scheduling

### Q77-018 · Given this pipeline's task dependencies, determine a valid execution order

**Level:** Mid · **Roles:** DE, AE

**Remember it as:** *A pipeline's tasks form a graph, not a list. The valid order is whatever a topological sort of that graph says it is, and there can be more than one right answer.*

**Answer in one line:** Build a dependency graph (which tasks must finish before which others can start) and run a **topological sort**, an ordering in which every task comes after all the tasks it depends on; any order that respects every dependency edge is valid, and there's often more than one correct answer, not a single "the" order.

**Topological sort, built one step at a time.** No earlier chapter builds this algorithm, so here it is, cell by cell, in a notebook. The standard method is **Kahn's algorithm**: count how many tasks each task is waiting for, start with the tasks that wait for nothing, and each time a task finishes, tell the tasks that were waiting for it. First, the pipeline as a dictionary. Each key is a task; its list holds the tasks it needs first:

```python
dag = {
    "extract_orders": [],
    "extract_customers": [],
    "clean_orders": ["extract_orders"],
    "join_orders_customers": ["clean_orders", "extract_customers"],
    "compute_daily_summary": ["join_orders_customers"],
    "load_to_warehouse": ["compute_daily_summary"],
}
print(len(dag), "tasks")
```

```
6 tasks
```

A task's **in-degree** is the number of tasks it's waiting for, which is simply the length of its list. A dictionary comprehension (Chapter 17, section 17.7) builds all six counts:

```python
in_degree = {task: len(needs) for task, needs in dag.items()}
for task, count in in_degree.items():
    print(f"{task:22} {count}")
```

```
extract_orders         0
extract_customers      0
clean_orders           1
join_orders_customers  2
compute_daily_summary  1
load_to_warehouse      1
```

`{task:22}` pads each name to 22 characters so the counts line up. The dictionary says who each task *needs*; the algorithm also has to know the opposite, who is *waiting for* each task. Build that map, the task's **children**:

```python
children = {task: [] for task in dag}
for task, needs in dag.items():
    for parent in needs:
        children[parent].append(task)
for task, kids in children.items():
    print(f"{task:22} -> {kids}")
```

```
extract_orders         -> ['clean_orders']
extract_customers      -> ['join_orders_customers']
clean_orders           -> ['join_orders_customers']
join_orders_customers  -> ['compute_daily_summary']
compute_daily_summary  -> ['load_to_warehouse']
load_to_warehouse      -> []
```

The first line starts every task with an empty list. The loop then reads each dependency backwards: `clean_orders` needs `extract_orders`, so `clean_orders` is a child of `extract_orders`. Now put every task with in-degree 0, the tasks that can start straight away, in a queue:

```python
from collections import deque

ready = deque(task for task, count in in_degree.items() if count == 0)
print(list(ready))
```

```
['extract_orders', 'extract_customers']
```

`deque` is the queue from Chapter 33, section 33.4: first in, first out, with `popleft()` taking from the front. The expression inside `deque(…)` is a comprehension without the square brackets; it hands the queue each task whose count is 0. The main loop takes the next ready task, adds it to the order, and lowers each child's count by one. A child whose count reaches 0 has nothing left to wait for, so it joins the queue:

```python
order = []
while ready:
    task = ready.popleft()
    order.append(task)
    for child in children[task]:
        in_degree[child] -= 1
        if in_degree[child] == 0:
            ready.append(child)
for step, task in enumerate(order, start=1):
    print(step, task)
```

```
1 extract_orders
2 extract_customers
3 clean_orders
4 join_orders_customers
5 compute_daily_summary
6 load_to_warehouse
```

Why does `extract_orders` come before `extract_customers`? Only because it was put in the dictionary first (dictionaries keep the order you insert keys in) and the queue is first in, first out. Put `extract_customers` first in `dag` and it comes out first. Both orders are valid, and that's the point of the question: nothing makes one extract wait for the other, so they could also run in parallel.

Last, the same steps as one function, with a cycle check. If the graph has a cycle, the tasks in it never reach in-degree 0, so the order comes out shorter than the task list:

```python
def topo_order(dag):
    in_degree = {task: len(needs) for task, needs in dag.items()}
    children = {task: [] for task in dag}
    for task, needs in dag.items():
        for parent in needs:
            children[parent].append(task)
    ready = deque(task for task, count in in_degree.items() if count == 0)
    order = []
    while ready:
        task = ready.popleft()
        order.append(task)
        for child in children[task]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                ready.append(child)
    if len(order) < len(dag):
        raise ValueError("cycle found: no valid order exists")
    return order

print(topo_order(dag) == order)
```

```
True
```

The function builds its own counts, because the loop above used up the first ones (every count is 0 now). `raise ValueError(…)` stops with an error, as in Chapter 29, section 29.2. Now break the graph on purpose: make `extract_orders` wait for `load_to_warehouse`, which itself waits, step by step, for `extract_orders`. Before you run it, predict which tasks could still start:

```python
looped = dict(dag)
looped["extract_orders"] = ["load_to_warehouse"]
try:
    topo_order(looped)
except ValueError as err:
    print("error:", err)
```

```
error: cycle found: no valid order exists
```

`dict(dag)` makes a copy, so the original `dag` is untouched. Only `extract_customers` could start; the other five tasks wait on each other in a loop and never reach 0.

| Tier | What to say |
|---|---|
| Passes | Describes the dependencies in English, produces an order by eyeballing it rather than a systematic method |
| Strong | Names topological sort explicitly and produces a genuinely valid order, acknowledging more than one valid order can exist (the two extracts could run in either order, or in parallel) |
| Extra points | + **[+Validate]** the real, algorithmically-produced order above, not a guessed one, and a cycle check that fails loudly + **[+Business]** this is exactly what an orchestrator such as Dagster or Airflow does automatically from a declared DAG: the engineer states dependencies, the scheduler determines (and often parallelizes) a valid execution order, rather than the engineer hard-coding a sequence |

**Likely follow-ups:** How would you detect a cycle in a dependency graph, meaning the DAG isn't actually valid? Which of these tasks could safely run in parallel?
**Red flag:** producing an order that violates a stated dependency, or being unable to name the standard algorithm for this problem.
**Learn it in:** Chapter 46, §46.2 (pipelines as graphs, and why they must be acyclic); Chapter 33, §33.4 (queues and `deque`) and §33.6 (walking graphs, cycles). Topological sort itself is built in this question. **Practise it with:** Chapter 72A, Q72A-028 (BFS and DFS).

### Rapid-fire, 77.4

Roles: DE and AE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q77-019 | What does DAG stand for, and why must a pipeline's dependency graph be acyclic? | Directed Acyclic Graph; a cycle (task A depends on B, which depends on A) has no valid execution order at all, since neither could ever go first | **[+Edge cases]** a cycle is easy to create by accident (a load that waits for the report that reads it); Q77-018's `topo_order` catches it, because tasks in a loop never reach in-degree 0 | Fresher · 46.2 (practise: Q72A-028) |
| Q77-020 | What's a sensor (or a "wait for" task) in an orchestration tool? | Something that reacts to an event outside the schedule. In Airflow a sensor is a task that *waits* for a condition (a file to arrive, an upstream job to finish) before the rest of the pipeline proceeds; in Dagster (Chapter 46, §46.6) a sensor *watches* for an event and starts a run or sends an alert | **[+Business]** sensors are how a pipeline safely depends on something outside its own DAG, like a third-party data delivery with no guaranteed exact timing | Mid · 46.2, 46.6, 46.8 |
| Q77-021 | What's the risk of a pipeline with a single point of failure at its very first task? | Every single downstream task, however independent it looks, silently can't run if that one upstream task fails, making the whole day's pipeline as fragile as its weakest single link | **[+Business]** designing for partial success (independent tasks can still run and deliver partial value even if one branch fails) is often worth the added complexity for a pipeline with many independent downstream consumers | Mid · 46.10; 61.6–61.7 |
| Q77-022 | What's backpressure, in a streaming context? | A mechanism for a slower downstream consumer to signal an upstream producer to slow down, preventing the consumer from being overwhelmed by data arriving faster than it can process. With a log such as Kafka (Chapter 50), producers aren't slowed down: the consumer reads at its own pace, and the gap shows up as **consumer lag**, which is why section 50.7 tells you to monitor lag | **[+Business]** without backpressure handling, a slow consumer either falls further and further behind or crashes outright under load it can't keep up with | Mid · 50.2, 50.7 (lag) |

---

## 77.5 Scale, partitioning, and performance

### Q77-023 · A table has grown to hundreds of millions of rows and queries filtering on date are slow. Walk through partitioning as a fix, and prove it works

**Level:** Mid · **Roles:** DE, AE

**Remember it as:** *A partitioned table lets the database skip entire partitions it knows can't contain a match, instead of scanning rows one at a time to find out.*

**Answer in one line:** **Range partitioning** by date splits a large table into smaller physical sub-tables, each holding a specific date range; a query filtering on date lets the query planner skip (prune) any partition that can't possibly contain a match, dramatically reducing how much data actually needs to be scanned.

**Verified, in `riverstone_lab`.** A small events table, partitioned by month:

<!-- lab:start -->

```sql
CREATE TABLE events_partitioned (
    id          INTEGER GENERATED ALWAYS AS IDENTITY,
    event_date  DATE NOT NULL,
    payload     TEXT
) PARTITION BY RANGE (event_date);

CREATE TABLE events_2025_01 PARTITION OF events_partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE events_2025_02 PARTITION OF events_partitioned
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
```

This is PostgreSQL's own partitioning syntax, which no earlier chapter uses:

- **`PARTITION BY RANGE (event_date)`** declares the parent table. It holds no rows itself; it says which column decides where each row goes.
- **`PARTITION OF events_partitioned FOR VALUES FROM (a) TO (b)`** creates a child table, a **partition**, for the dates from `a` (included) up to `b` (excluded): the same half-open rule as Q77-013, so 1 February belongs to February only.
- On `INSERT` into the parent, each row is **routed** to its child automatically.

Load 1,000 events into each month, then count what landed in each partition:

```sql
INSERT INTO events_partitioned (event_date, payload)
SELECT DATE '2025-01-01' + (n % 31), 'event ' || n
FROM generate_series(1, 1000) AS n;

INSERT INTO events_partitioned (event_date, payload)
SELECT DATE '2025-02-01' + (n % 28), 'event ' || n
FROM generate_series(1, 1000) AS n;

SELECT COUNT(*) AS january_rows FROM events_2025_01;
SELECT COUNT(*) AS february_rows FROM events_2025_02;
```

```
 january_rows
--------------
         1000
(1 row)

 february_rows
---------------
          1000
(1 row)
```

`generate_series(1, 1000)` (Chapter 13, section 13.8) makes the numbers 1 to 1,000, one row each, called `n`. `n % 31` is the remainder after dividing by 31 (0 to 30), and adding a whole number to a `DATE` moves it forward that many days, so the rows spread across January's 31 days. `'event ' || n` joins text to the number. The rows went into the parent, and every one was routed to the right month. Now collect statistics and ask for the plan:

```sql
ANALYZE events_partitioned;

EXPLAIN SELECT * FROM events_partitioned WHERE event_date = '2025-01-15';
```

```
                                     QUERY PLAN
------------------------------------------------------------------------------------
 Seq Scan on events_2025_01 events_partitioned  (cost=0.00..19.50 rows=32 width=17)
   Filter: (event_date = '2025-01-15'::date)
(2 rows)
```

`ANALYZE` counts the rows and samples their values, the statistics the planner uses to estimate (Chapter 28, section 28.5). The numbers in brackets are those estimates; here only the partition name matters. The query plan touches **only the January partition**, `events_2025_01`; the February partition is never scanned at all, real, confirmed partition pruning.

**What if the query doesn't filter on the partition key?**

```sql
EXPLAIN SELECT * FROM events_partitioned WHERE payload = 'event 7';
```

```
                                        QUERY PLAN
-------------------------------------------------------------------------------------------
 Append  (cost=0.00..39.01 rows=2 width=17)
   ->  Seq Scan on events_2025_01 events_partitioned_1  (cost=0.00..19.50 rows=1 width=17)
         Filter: (payload = 'event 7'::text)
   ->  Seq Scan on events_2025_02 events_partitioned_2  (cost=0.00..19.50 rows=1 width=17)
         Filter: (payload = 'event 7'::text)
(5 rows)
```

Both partitions are scanned, and `Append` glues their results together: with no date in the filter, the planner can't rule out either month. Clean up (dropping the parent drops its partitions too):

```sql
DROP TABLE events_partitioned;
```

<!-- lab:end -->

| Tier | What to say |
|---|---|
| Passes | "Partitioning makes queries faster" (true, no proof of the actual mechanism) |
| Strong | The pruning explanation above, correctly identifying that the *query planner* is what decides to skip irrelevant partitions, not the query itself doing anything different |
| Extra points | + **[+Validate]** the real query plan above shows only one partition's name (`events_2025_01`) in the plan at all, direct proof of pruning, not an assumed benefit + **[+Business]** partitioning also makes bulk operations dramatically cheaper: retiring an entire month's stale data is `ALTER TABLE events_partitioned DETACH PARTITION events_2025_01` (then archive it, or `DROP TABLE`) instead of a slow, logged `DELETE` scanning and removing millions of individual rows |

**Likely follow-ups:** How would you choose the partition granularity (daily vs. monthly vs. yearly)? What happens to a query that doesn't filter on the partition key at all?
**Red flag:** claiming partitioning always speeds up every query, without the "the query must filter on the partition key" caveat.
**Learn it in:** Chapter 49, §49.6 (partitioning and file sizing); Chapter 48, §48.5 (partition pruning: don't open boxes you don't need); Chapter 28, §28.5 (reading query plans with EXPLAIN). **Practise it with:** Chapter 71, §71.9 (query optimization and indexes).

### Rapid-fire, 77.5

Roles: DE, AE and ARCH for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q77-024 | What's sharding, and how is it different from partitioning? | Table partitioning (as in Q77-023) splits a table into pieces inside one database; sharding spreads the data across *separate database servers*, adding a routing layer to know which shard holds which data. In Spark and Kafka (Chapters 48 and 50), "partition" also means a piece of data that can live on a different machine: the word depends on the system | **[+Trade-offs]** sharding solves a scale problem partitioning alone can't (a single machine's storage/compute limit), at the cost of real added complexity: cross-shard queries and joins become much harder | Mid · 61.5; Spark and Kafka partitions 48.2, 50.2 |
| Q77-025 | What's a materialized view, and when does it help at scale? | A pre-computed, physically stored query result, refreshed periodically, trading data freshness for query speed on an expensive aggregation run frequently | **[+Trade-offs]** the answer is stale between refreshes, and each refresh re-runs the whole query; PostgreSQL's `REFRESH MATERIALIZED VIEW CONCURRENTLY` lets people keep reading during a refresh, but needs a unique index | Mid · 28.11 (practise: Q71-049, Q71-055) |
| Q77-026 | Why does `SELECT *` become a bigger problem at scale than it is on a small table? | Pulling every column, including large or unused ones, multiplies I/O cost linearly with row count; on a small table the waste is invisible, on a billion-row table it's a real, measurable cost | **[+Edge cases]** on a columnar format, `SELECT *` throws away the main advantage: every column's data is read (Q77-027) | Fresher · 49.2 (see also Q71-015, `SELECT *` with `GROUP BY`) |
| Q77-027 | What's a columnar storage format (like Parquet), and why does it suit analytical queries specifically? | Stores each column's values together on disk, rather than each row together; an analytical query that only needs 3 of a table's 50 columns reads only those 3 columns' data, not the other 47 | **[+Business]** this is the storage-layer reason a data warehouse or lakehouse built on columnar formats is dramatically faster for typical `GROUP BY`/aggregation-heavy analytical queries than a row-oriented format built for fast single-row lookups | Fresher · 49.2–49.3 |

---

## 77.6 Data quality and monitoring

### Q77-028 · Design a data quality check that would have caught a real Riverstone data problem: a pipeline that silently produced negative revenue values

**Level:** Fresher · **Roles:** DE, AE

**Remember it as:** *A data quality check needs to run automatically, on every load, and fail loudly, not depend on someone noticing a wrong number weeks later.*

**Answer in one line:** Build automated, scheduled checks (not manual, occasional ones) that assert specific, testable properties of the data on every pipeline run, revenue should never be negative, order counts shouldn't drop to zero unexpectedly, a key column shouldn't suddenly have nulls, and fail the pipeline run loudly (alerting someone) rather than silently loading bad data.

**Worked example**, a concrete check:

> "A simple assertion: `SELECT COUNT(*) FROM daily_summary WHERE total_revenue < 0` should always return 0; if it doesn't, fail the pipeline run and alert before the bad data ever reaches a dashboard. I'd also add a volume check: today's row count shouldn't be, say, more than 50% below the trailing 7-day average, which catches a source system silently sending a truncated file, a different kind of failure the negative-revenue check wouldn't catch at all."

| Tier | What to say |
|---|---|
| Passes | Names one sensible check (e.g. no negative revenue) but runs it by hand, after the fact |
| Strong | At least one concrete, automatable assertion (the negative-revenue check above), run on every pipeline execution, not manually |
| Extra points | + **[+Edge cases]** names a *second*, different kind of check (a volume/row-count anomaly check) unprompted, since a single check type only catches one failure mode, and real pipeline failures come in more than one shape + **[+Edge cases]** computes the baseline from days that passed their checks, or uses the same weekday over the last four weeks, so a run of bad days can't drag the baseline down with it: after a week of zero-row days, a plain trailing average is near zero too, and the check stops firing + **[+Business]** ties the check to failing the pipeline loudly, not just logging a warning that nobody reads until the damage is already visible downstream |

**Likely follow-ups:** How would you decide the right threshold for a volume-anomaly check without too many false alarms? What's the difference between a data quality check and a schema validation check?
**Red flag:** proposing manual, human-driven spot-checks as the primary quality control for an automated pipeline.
**Learn it in:** Chapter 47, §47.2–47.3 (tests in the pipeline, a check library) and §47.5 (volume, and "don't learn your baseline from broken days"); Chapter 14, §14.10 (checks that must return zero). See also Chapter 36, §36.8's missing-value discipline (the modeling-side cousin of the same "detect before you trust" habit).

### Rapid-fire, 77.6

Roles: DE and AE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q77-029 | What's the difference between data quality monitoring and data observability? | Data quality monitoring checks specific, predefined rules against the data itself; data observability more broadly tracks the health of the whole pipeline system (freshness, volume, schema, lineage) to catch problems you didn't think to write a specific rule for | **[+Business]** observability is meant to catch the failure mode nobody anticipated; quality checks catch the ones you did | Mid · 47.5 |
| Q77-030 | What's data lineage, and why does an on-call engineer need it at 2am? | A traceable record of where a piece of data came from and what transformed it along the way; at 2am, debugging a wrong number starts with lineage, tracing backward from the bad number to find exactly which upstream step introduced it | **[+Evidence]** without lineage, debugging a wrong number in a large pipeline can mean manually checking every step in order, instead of jumping straight to the likely source | Mid · 47.6 |
| Q77-031 | Why does a monitoring setup need a heartbeat, an alert when a pipeline or monitor has gone silent, and not just failure alerts? | A **heartbeat** (or dead-man's switch) is a signal that must keep arriving on time; its absence is the alert. A monitoring system that itself silently stops running produces no alerts at all, which can be mistaken for "everything's fine" when it actually means nobody would know if something broke | **[+Business]** Chapter 47's freshness check is a heartbeat for data: it fires when the newest data is older than the previous working day, even though nothing "failed" | Mid · 47.5 (freshness) |
| Q77-032 | What's the cost of alert fatigue, and how does it actually cause outages? | Too many low-value or false-positive alerts trains the on-call team to ignore or mute them, so a real, important alert gets missed in the noise exactly when it matters most | **[+Business]** a smaller number of carefully-tuned, high-signal alerts is more reliable in practice than a comprehensive but noisy set that gets tuned out | Fresher · 47.9, 20.8 |

---

## 77.7 Full system design walk-throughs

### Q77-033 · Design a daily sales pipeline for Riverstone, end to end

**Level:** Mid · **Roles:** DE, AE

**What they're really testing:** whether a complete, coherent pipeline design comes out under time pressure, touching every stage, not just the interesting parts.

**Talked through live, start to finish:**

> "Source: the transactional order database. Extraction: a scheduled incremental pull each night, using an updated-at timestamp or CDC if available, rather than a full reload of the whole orders table every time. Landing: raw extracted data lands in a staging area first, unmodified, so I always have an unaltered copy to reprocess from if a downstream transformation bug is found later. Transformation: clean and join orders with customers and products, compute daily aggregates, handling the exact fan-out risk Chapter 71 already covers if this joins through any one-to-many relationship carelessly. Load: upsert into the daily_summary fact table, keyed on date, so a re-run is safe (Q77-007). Quality checks: the negative-revenue and volume-anomaly checks from Q77-028, run automatically on the new data before anyone can read it, and only then published: write–audit–publish. Orchestration: an Airflow-style DAG with the dependency order Q77-018 worked through, scheduled to run after the source database's own nightly maintenance window closes, with a sensor task waiting for that to complete rather than a fixed clock time that could run too early. Monitoring: alert on failure, alert on the monitor itself going silent (Q77-031), and a lineage-traceable record of exactly which run produced which row in the final table."

**Extra-points moves demonstrated:** **[+Signpost]** covered every stage (extract, land, transform, load, quality, orchestrate, monitor) explicitly, not just the transformation logic, and tied the stages to answers already given in this chapter (Q77-007, Q77-018, Q77-028, Q77-031), showing the concepts as one coherent system, not isolated trivia. **[+Business]** justified the staging-area decision with a specific reason (safe reprocessing), not just "it's best practice."

**Likely follow-ups:** How would this change if the source database couldn't support CDC at all? What's your rollback plan if a bug is found in the transformation logic three days after it shipped?
**Red flag:** a design that only covers the transformation SQL, with no mention of scheduling, quality checks, or failure handling.
**Learn it in:** Chapter 46, §46.3–46.7 (Riverstone's daily pipeline, built); Chapter 47, §47.4 (write–audit–publish); this chapter's §77.1–77.6, pulled together.

### Q77-034 · Design a real-time pipeline for monitoring sensor data from Riverstone's plant machines

**Level:** Senior · **Roles:** DE, MLE, ARCH

**What they're really testing:** whether the candidate correctly identifies this as a genuinely streaming problem (Q77-002) and reasons about the specific challenges streaming introduces that batch doesn't have.

**Talked through live, start to finish:**

> "First, I'd confirm this genuinely needs streaming: if the goal is alerting on equipment failure within seconds, not next-day reporting, then yes, batch wouldn't meet the actual business need here, unlike the daily sales case. Ingestion: sensors publish to a message queue (Kafka or similar), which decouples the sensors from whatever's consuming their data and buffers against a consumer temporarily falling behind. Processing: a stream processor consumes the queue, computing rolling windows (say, a 5-minute rolling average temperature per machine) rather than reacting to every single raw reading, which would be noisy. Out-of-order handling: sensor data over a real network can arrive out of order or late; I'd use event time, not processing time, for the windows, with a defined lateness tolerance (a watermark), rather than assuming perfectly ordered arrival. Alerting: when a rolling average crosses a threshold, publish an alert event, itself handled idempotently (Q77-007) so a reprocessed or retried alert doesn't spam the on-call team twice for the same real event. Storage: raw sensor events also land in cheap, durable storage (a data lake) for later batch analysis and model training, alongside the real-time alerting path, since the two paths serve genuinely different purposes."

**Extra-points moves demonstrated:** **[+Clarify]** explicitly validated that streaming was the right call before designing for it, rather than assuming. **[+Edge cases]** named out-of-order and late-arriving data unprompted, a genuinely common real pitfall specific to streaming that a batch-only background can easily miss. **[+Business]** justified the dual raw-storage-plus-real-time-path design with the different purposes each actually serves.

**Likely follow-ups:** How would you size the rolling window, and what trade-off does that involve? What happens if the message queue itself goes down, does data get lost?
**Red flag:** a design that processes each raw sensor reading individually with no windowing, or no acknowledgment that streaming data can arrive out of order.
**Learn it in:** Chapter 50, §50.5 (event time, windows, and watermarks) and §50.8 (Riverstone's plant monitoring case), plus §77.1–77.2 of this chapter.

### Q77-035 · Design a system to detect and merge duplicate customer records at scale

**Level:** Senior · **Roles:** DE, AE, ARCH

**What they're really testing:** whether "just check if the names match" gets recognized as inadequate for a real, messy production dataset, and a genuinely scalable approach is proposed instead.

**Talked through live, start to finish:**

> "Exact-match deduplication (Chapter 71's `GROUP BY` approach) catches identical records, but real duplicates are messier: 'Sharma Hardware' vs. 'Sharma Hardware Pvt Ltd,' a trailing space, a different phone number format for the same company. I'd approach this in two stages. First, blocking: instead of comparing every pair of records against every other (which is O(n²) and doesn't scale, Chapter 72A's exact lesson), group records into smaller candidate 'blocks' likely to contain real duplicates, say by the first few characters of the normalized name plus the same city (the same match-key idea as Chapter 14's), so only records within the same block get compared pairwise. Second, within each block, score candidate pairs on similarity (normalized name distance, matching phone or email, matching address) and flag pairs above a threshold for either automatic merge (very high confidence) or human review (medium confidence). I'd deliberately avoid fully automatic merging at anything but very high confidence, since an incorrectly merged pair of genuinely different customers is a much more damaging, harder-to-undo mistake than leaving two real duplicates unmerged a little longer."

**Extra-points moves demonstrated:** **[+Scale]** explicitly named the O(n²) scaling problem a naive pairwise-comparison approach would hit, and proposed blocking as the specific fix, directly reusing Chapter 72A's own complexity reasoning. **[+Business]** made an explicit, justified risk trade-off (false-merge cost vs. missed-duplicate cost) rather than optimizing purely for automation.

**Likely follow-ups:** What similarity algorithm would you actually use for the name comparison? How would you handle a customer who insists two "duplicate" records are actually two genuinely different but related businesses?
**Red flag:** proposing a pairwise comparison across the entire dataset with no blocking strategy, ignoring the scaling problem entirely.
**Learn it in:** Chapter 14, §14.4 (exact and fuzzy duplicates, match keys, and why a wrong merge is worse than a missed one); Chapter 71, Q71-041 (exact-match dedup); Chapter 33, §33.1 and Chapter 72A, Q72A-002 (the O(n²) cost this design specifically avoids).

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| A load step using plain `INSERT` with no conflict handling | Re-running a failed pipeline duplicates every row | Use an idempotent upsert keyed on a unique identifier |
| Choosing streaming by default for a problem that doesn't need it | Real, avoidable added complexity with no business benefit | Ask how fresh the downstream decision genuinely needs to be first |
| SCD Type 1 used where history actually matters | Historical reports silently reflect only the current state | Use Type 2, closing old rows instead of overwriting them |
| A dependency graph hard-coded as one linear sequence | Independent tasks run needlessly serially, wasting time | Declare true dependencies; let the orchestrator determine (and parallelize) a valid order |
| Partitioning on a column queries don't actually filter on | No pruning benefit at all, despite the added complexity | Partition on the column your queries actually filter by |
| Manual, occasional data quality spot-checks | A bad number reaches a dashboard before anyone notices | Automated, scheduled checks that fail the pipeline loudly |
| A dedup design comparing every record pair with no blocking | Doesn't scale past a small dataset | Block first, compare only within blocks |

---

## In the real world: the pipeline that failed silently for three weeks

Arjun, a Data Engineer, is asked in an interview to describe a real production incident. He describes a pipeline that had been quietly loading zero rows for a source that had actually stopped sending data three weeks earlier, an upstream vendor had changed their export format without notice, and the pipeline's extraction step had been silently succeeding (technically, "zero rows extracted" isn't an error) and loading nothing, night after night, with no alert firing because nothing had technically failed.

He walks through exactly what he changed: a volume-anomaly check (Q77-028's second check), alerting if a day's row count dropped more than 50% below the trailing average, which would have caught this within a day instead of three weeks. He's asked the natural follow-up: why hadn't a check like that existed before the incident? His honest answer: "Because the team, including me, had only ever built checks for data that looked *wrong*, never for data that looked *absent*. It's an easy blind spot: a pipeline that runs successfully and loads nothing doesn't look like a failure from the outside, it looks exactly like a quiet day."

The interviewer's note: *"Didn't just describe the fix, explained the actual blind spot in the team's thinking that let it happen in the first place."* That's the difference this chapter's whole method is built around: a correct technical fix is table stakes; naming the reasoning gap that let the problem exist unnoticed is what shows real production experience.

---

## Project

**Goal:** apply this chapter's method to a real or realistic pipeline of your own.

### Tools you'll need

**PostgreSQL 16** and **Python**, the same environment Chapters 71 and 72A use; every SQL result and every topological-sort output in this chapter was produced in them. In real production work: Airflow, Dagster, or Prefect for orchestration; Kafka or a managed equivalent for streaming; dbt for transformation; a cloud warehouse (Snowflake, BigQuery, Redshift) or lakehouse (Databricks) for storage and compute.

1. Implement SCD Type 2 for one real dimension in your own data (or Riverstone's), and prove the historical version is queryable, the way Q77-013 did.
2. Make one real pipeline step idempotent using an upsert pattern, and prove a duplicate re-run doesn't duplicate rows.
3. Write two automated data quality checks for a real dataset: one checking a specific value constraint, one checking for an unexpected volume anomaly.
4. Pick one of this chapter's system design questions (daily pipeline, streaming sensors, or deduplication) and write your own full design for a different, real scenario from your own work.

---

## Key terms

ETL vs. ELT · batch vs. streaming · data warehouse vs. data lake vs. lakehouse · data contract · CDC (Change Data Capture) · idempotency · upsert (`ON CONFLICT`, `EXCLUDED`) · at-least-once / at-most-once / exactly-once delivery · schema drift · backfilling · dead-letter queue · SCD Type 1/2/3 · surrogate key · half-open validity period · fact table grain · junk dimension · DAG (Directed Acyclic Graph) · topological sort · Kahn's algorithm · in-degree · sensor (orchestration) · backpressure · consumer lag · partitioning · partition pruning · sharding · materialized view · columnar storage · data observability · data lineage · heartbeat (dead-man's switch) · alert fatigue · write–audit–publish · watermark · blocking (deduplication)

---

## Final-week revision list

Q77-001, Q77-002, Q77-007, Q77-008, Q77-013, Q77-018, Q77-023, Q77-028, Q77-033, Q77-034, Q77-035.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 71, SQL Question Bank,** already covers the join-cardinality, indexing (section 71.9), and materialized-view foundations this chapter builds directly on.
- **Chapter 72A, Data Structures & Algorithms Question Bank,** supplies the complexity reasoning (O(n²) scaling, walking graphs with BFS and DFS) this chapter's design questions reuse explicitly.
- **Chapter 78, Automation & Integration Question Bank,** applies this chapter's idempotency, retry and monitoring answers to business automations and integrations.
- **Part 5 of this book** (data engineering proper) teaches every technique this bank draws on, in full; this chapter tests it, it doesn't re-teach it from scratch.
