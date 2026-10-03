# Chapter 77. Data Engineering & Data System Design Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the pipeline, data-modeling, and system-design questions that come up in Data Engineer interviews · design a batch or streaming pipeline live, under time pressure, the way an interviewer actually wants · reason correctly about idempotency, partitioning, and schema evolution, not just define the terms · walk through a full system design case end to end, stating trade-offs out loud.
>
> **Before you start:** Chapter 69 (the three answer tiers and the twelve extra-point moves). The questions test Part 5 (Chapters 45–52: ingestion, pipelines, data quality, distributed compute, storage, streaming, activation and deployment) and Chapter 28 (query plans, grain, the star schema, slowly changing dimensions). They also link to Chapter 12, section 12.13 (the upsert), Chapter 33 (queues and graphs), Chapter 61 (partitioning and sharding), and the two banks this one leans on, Chapter 71 (SQL) and Chapter 72A (complexity). This chapter tests those skills; it doesn't teach them again, with one exception: Q77-018 builds topological sort step by step, because no earlier chapter does.
>
> **Time needed:** 5–6 hours for a first pass (about 10 minutes per core question, including running its code, and 1–2 minutes per rapid-fire row), plus 1 hour for the final-week list. Section 77.8 adds about 1½ hours and is best done with a notebook open.
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

## 77.8 Predict the output: what happens to rows on the way in

The rest of this chapter is about pipeline design: idempotency, delivery guarantees, modelling, orchestration, scale. This section is about the smaller, meaner thing that breaks pipelines that are designed perfectly well — what the file reader, the type system and the clock do to rows while nobody is looking.

Every question below is a load that completes successfully. No exception, no alert, no failed task. The rows are simply not the rows that were in the source, and the first person to notice is usually a finance analyst three weeks later asking why a total moved.

Read the setup, say what comes out, then read on.

**How these were run.** pandas 3.0.2, numpy 2.4.3, pyarrow for Parquet, on Python 3.12. The setup cell:

```python
import io, os, time, csv
import numpy as np
import pandas as pd
```

### Q77-036 · A CSV of customer codes with leading zeros, read with `pd.read_csv`

**Level:** Fresher · **Roles:** DE, AE, DA

**Remember it as:** *A reader that guesses types will guess "number" for anything that looks like one, and a number has no leading zeros to keep.*

**Answer in one line:** The codes come back as **123, 456 and 1000** as `int64` — the leading zeros are gone, and any join against the source system's `'00123'` now matches nothing at all.

```python
csv_text = "customer_code,name\n00123,Sharma\n00456,Patel\n01000,Metro\n"

df = pd.read_csv(io.StringIO(csv_text))
print(f"default     : {df.customer_code.tolist()}   dtype {df.customer_code.dtype}")

df2 = pd.read_csv(io.StringIO(csv_text), dtype={'customer_code': str})
print(f"dtype=str   : {df2.customer_code.tolist()}   dtype {df2.customer_code.dtype}")

print(f"overlap     : {set(df.customer_code.astype(str)) & set(df2.customer_code)}")
```

```
default     : [123, 456, 1000]   dtype int64
dtype=str   : ['00123', '00456', '01000']   dtype str
overlap     : set()
```

That last line is the one to remember. Convert the inferred integers back to strings and **not a single value matches** the original codes. An inner join drops every row; a left join fills every column with nulls. Nothing errors.

The columns this happens to are exactly the ones you join on: customer codes, product SKUs, postcodes, phone numbers, bank account numbers, GST numbers. They are identifiers that happen to be made of digits, and an identifier is a string even when it looks like a number — you never add two of them together.

The fix is to say so at the boundary, and to say it for the whole file rather than per column once the file is wide:

```python
pd.read_csv(path, dtype=str)                      # everything as text, cast deliberately after
pd.read_csv(path, dtype={'customer_code': str})   # or name the identifier columns
```

| Tier | What to say |
|---|---|
| Passes | "The leading zeros get dropped" |
| Strong | + that the join then silently matches nothing, and names `dtype=` at read time as the fix rather than a repair afterwards |
| Extra points | **[+Business]** an inner join that returns zero rows is noticed; a left join that returns nulls is often not, and gets reported as missing data · **[+Edge cases]** you cannot repair it afterwards without knowing the original width — `zfill(5)` is a guess · **[+Validate]** compare the distinct-count of a key before and after load; it should not change · **[+Scale]** Parquet carries the type with it, so a Parquet source never has this problem (Q77-041) |

**Likely follow-ups:** How would you detect this in an automated pipeline? What does a schema or data contract do about it? *(Q77-004 — it declares the type so the reader does not have to guess.)* What happens in Spark? *(The same inference, with the same result.)*
**Red flag:** repairing with `zfill` without knowing the source width.
**Learn it in:** Chapter 14, section 14.2 (profiling); Chapter 47, section 47.3 (ingestion).

### Q77-037 · An order id of 9,007,199,254,740,993 arrives in a float column

**Level:** Brain-racking · **Roles:** DE, AE, MLE

**Remember it as:** *A float64 has 53 bits for the digits. Above 2⁵³ it cannot count by ones any more, so consecutive ids start sharing a value.*

**Answer in one line:** Two of the three ids become **the same number** — 9007199254740993 is stored as 9007199254740992, so three distinct orders become two, and a `COUNT(DISTINCT)` quietly drops one.

```python
ids = [9007199254740992, 9007199254740993, 9007199254740994]
as_float = np.array(ids, dtype='float64')

print(f"originals     : {ids}")
print(f"as float64    : {[int(x) for x in as_float]}")
print(f"still distinct: {len(set(int(x) for x in as_float))} of {len(ids)}")
print(f"2**53         = {2**53:,}")
```

```
originals     : [9007199254740992, 9007199254740993, 9007199254740994]
as float64    : [9007199254740992, 9007199254740992, 9007199254740994]
still distinct: 2 of 3
2**53         = 9,007,199,254,740,992
```

Above 2⁵³ a float64 can represent only every second integer, then every fourth, and so on. The middle id has nowhere to land and is rounded to its neighbour.

The question that matters is **how an integer id ends up in a float column at all**, because nobody writes `float` on purpose for an id. The answer is that one missing value does it:

```python
csv_text = "order_id,qty\n9007199254740993,5\n9007199254740994,\n"
d = pd.read_csv(io.StringIO(csv_text))
print(d.dtypes.to_dict())
```

```
{'order_id': dtype('int64'), 'qty': dtype('float64')}
```

`qty` had one blank, so it is `float64`. `order_id` was complete, so it stayed `int64` and is safe. Blank out one id and it becomes `float64` too — and from that moment the ids are approximate.

This is a very modern problem. Snowflake ids, Twitter-style ids, and anything derived from a nanosecond timestamp are all 18 to 19 digits, comfortably past 2⁵³. Order 9007199254740993 is not a contrived example; it is a plausible id from any system minted after about 2010.

The fix is the nullable integer type, which holds missing values without leaving the integers:

```python
d2 = pd.read_csv(io.StringIO(csv_text), dtype={'order_id': 'Int64', 'qty': 'Int64'})
print(d2.order_id.tolist(), d2.qty.tolist())
```

```
[9007199254740993, 9007199254740994] [5, <NA>]
```

Capital-I `Int64` is pandas' nullable integer; lower-case `int64` is NumPy's and cannot hold a null. One letter.

| Tier | What to say |
|---|---|
| Passes | "Floats lose precision on big numbers" |
| Strong | + names 2⁵³ as the boundary, shows two ids collapsing into one, and explains that a single missing value is what turns an integer column into a float one |
| Extra points | **[+Edge cases]** `Int64` (nullable) against `int64` (NumPy) is one capital letter and is the whole fix · **[+Business]** `COUNT(DISTINCT order_id)` silently falls, so a reconciliation against the source is off by a few rows with no error anywhere · **[+Scale]** ids minted from nanosecond timestamps or Snowflake schemes are routinely past 2⁵³ · **[+Validate]** read ids as strings if you never do arithmetic on them, which is almost always |

**Likely follow-ups:** What is the largest exactly representable integer in a float64? Why does JSON have this problem too? *(JavaScript numbers are float64, so ids past 2⁵³ corrupt in any JS client.)* How would you store these in Postgres? *(`BIGINT`, which is exact to 2⁶³.)*
**Red flag:** not connecting the float column to the single missing value that caused it.
**Learn it in:** Chapter 33, section 33.3 (how numbers are stored); Chapter 72, Q72-010.

### Q77-038 · A region column where `NA` means North America

**Level:** Mid · **Roles:** DE, AE, DA

**Remember it as:** *The reader has a list of 19 strings it treats as missing, and `NA` and `NULL` are both on it. A real value that matches the list is destroyed on the way in.*

**Answer in one line:** The `NA` and `NULL` rows become **missing** — pandas recognises 19 strings as null markers by default, so two legitimate region codes vanish and only EMEA and APAC survive as values.

```python
csv_text = "region,sales\nNA,100\nEMEA,200\nAPAC,300\nNULL,400\n"
d = pd.read_csv(io.StringIO(csv_text))
print(d.to_string(index=False))
print(f"nulls in region: {d.region.isna().sum()} of {len(d)}")
print(f"regions pandas sees: {d.region.dropna().unique().tolist()}")
```

```
region  sales
   NaN    100
  EMEA    200
  APAC    300
   NaN    400
nulls in region: 2 of 4
regions pandas sees: ['EMEA', 'APAC']
```

The sales figures are intact. The labels are gone. A `groupby('region')` now drops 500 of the 1,000 in revenue into a group that does not exist, and the regional report is missing North America entirely — while still balancing, because the rows are there.

The default marker list is longer than people expect:

```python
print(len(pd._libs.parsers.STR_NA_VALUES))
print(sorted(pd._libs.parsers.STR_NA_VALUES)[:12])
```

```
19
['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A']
```

`NA`, `NULL`, `None`, `NaN`, `nan`, `null` and the Excel error strings are all on it. Any of them can be a real value: `NA` for North America, `NULL` as a product code, `None` as a free-text answer.

Two fixes, and they differ:

```python
pd.read_csv(path, keep_default_na=False)                 # nothing is missing unless you say so
pd.read_csv(path, na_values=[''], keep_default_na=False) # only a blank is missing
```

`keep_default_na=False` is the blunt one and is usually right for a categorical column. Note that it makes *blanks* into empty strings too, so if you want blanks to be null you must say so, which is the second line.

| Tier | What to say |
|---|---|
| Passes | "`NA` is being read as null" |
| Strong | + that there are 19 default markers including `NULL` and `None`, that the numbers survive while the labels do not, and names `keep_default_na=False` |
| Extra points | **[+Business]** the report still balances, because only the labels were lost, which is why nobody catches it · **[+Validate]** compare the distinct count of a categorical column against the source system's list · **[+Edge cases]** the same list applies to Excel reads; and a two-letter country code column has `NA` for Namibia as well as North America |

**Likely follow-ups:** How would a data contract prevent this? What does `keep_default_na=False` do to genuine blanks? *(They become empty strings.)* Does Spark have the same list? *(A shorter one, and configurable — so a file can read differently in two engines.)*
**Red flag:** trusting that a successful load means the values are the source's values.
**Learn it in:** Chapter 14, section 14.3 (missing values); Chapter 77, Q77-004 (data contracts).

### Q77-039 · Splitting a CSV line on commas

**Level:** Fresher · **Roles:** DE, AE

**Remember it as:** *A CSV is not "text with commas". It is a format with quoting and escaping rules, and `split(',')` knows none of them.*

**Answer in one line:** `split(',')` gives **5 fields** where there are really **4**, because it breaks the quoted address in half and leaves stray quote characters on both pieces.

```python
line = 'ORD-1,"Sharma Hardware, Mumbai",1500,"He said ""ok"""'

print(f"split(',')  -> {len(line.split(','))} fields: {line.split(',')}")
print(f"csv.reader  -> ", end='')
parsed = next(csv.reader([line]))
print(f"{len(parsed)} fields: {parsed}")
```

```
split(',')  -> 5 fields: ['ORD-1', '"Sharma Hardware', ' Mumbai"', '1500', '"He said ""ok"""']
csv.reader  -> 4 fields: ['ORD-1', 'Sharma Hardware, Mumbai', '1500', 'He said "ok"']
```

The parser does three things the split does not: it keeps the quoted comma inside its field, it removes the surrounding quotes, and it turns the doubled `""` into a single literal quote.

The reason this is worth a question in a data engineering interview is the failure mode. A file of a million rows where **nine** addresses contain a comma does not fail; it produces nine rows with one extra field. Depending on how the loader handles that, those rows are skipped, or truncated, or — worst — shifted, so the value in `amount` is really part of an address and the whole row is silently wrong from that column onward.

The same applies to embedded newlines, which are legal inside a quoted CSV field and which break any pipeline that assumes one line is one record — including `wc -l`, `split`, and most shell-based row counts.

The rule: never hand-parse a CSV. Use `csv.reader`, `pandas.read_csv`, or the engine's own reader, and if you control the format, prefer one that does not need quoting at all (Q77-041).

| Tier | What to say |
|---|---|
| Passes | "You should use a proper CSV parser" |
| Strong | + names the three rules a parser applies — quoted separators, quote stripping, doubled-quote escaping — and describes field-shift as the dangerous failure |
| Extra points | **[+Edge cases]** a quoted field may contain a newline, so one line is not one record and `wc -l` is not a row count · **[+Business]** a shifted row puts text in a numeric column and is usually caught by a type error several steps downstream, far from the cause · **[+Scale]** Parquet or Avro have no quoting problem at all, because they are not text |

**Likely follow-ups:** What happens with an embedded newline? How would you count rows in a CSV safely? What is the advantage of a tab or pipe delimiter? *(Less likely in the data — but not impossible, so it is a mitigation, not a fix.)*
**Learn it in:** Chapter 14, section 14.8 (joining messy sources); Chapter 47, section 47.3.

### Q77-040 · An incremental load using `WHERE updated_at >= last_watermark`

**Level:** Brain-racking · **Roles:** DE, AE

**Remember it as:** *`>=` reloads the boundary row every run. `>` skips any row that shares the boundary second. Neither is safe on a timestamp alone.*

**Answer in one line:** `>=` picks up ids **1, 2 and 3** — reloading row 2, which was already loaded — and switching to `>` fixes that but **loses a row entirely** whenever two records share the watermark second.

```python
ts = pd.to_datetime(['2025-06-01 10:00:00', '2025-06-01 10:00:00', '2025-06-01 11:00:00'])
tbl = pd.DataFrame({'id': [1, 2, 3], 'updated_at': ts})
watermark = ts[1]

print(f"with >= : {tbl[tbl.updated_at >= watermark].id.tolist()}")
print(f"with >  : {tbl[tbl.updated_at >  watermark].id.tolist()}")
```

```
with >= : [1, 2, 3]
with >  : [3]
```

Now the other half, which is the part people miss. If the last run ended on a second that two rows share:

```python
ts2 = pd.to_datetime(['2025-06-01 10:00:00', '2025-06-01 10:00:00'])
t2 = pd.DataFrame({'id': [1, 2], 'updated_at': ts2})
print(f"'>' from that second: {t2[t2.updated_at > ts2[0]].id.tolist()}")
```

```
'>' from that second: []
```

Row 2 is never loaded. Not reloaded — **lost**, permanently, because the next run's watermark has already moved past it.

So the two options are "duplicate rows sometimes" and "lose rows sometimes", and which you get depends on whether the source writes more than one row per second, which it certainly does.

That is why the real answer is not a choice of operator. It is one of:

| Approach | Why it works |
|---|---|
| **`>=` plus an idempotent merge** | Reload the boundary, and let a `MERGE`/upsert on the primary key make the duplicate harmless. This is the usual answer and ties to Q77-007 |
| **A strictly increasing sequence**, not a timestamp | A monotonic id or a change-log sequence number has no ties, so `>` is exact |
| **A watermark plus a tiebreaker** | `WHERE (updated_at, id) > (last_ts, last_id)`, which orders the ties |
| **CDC** (Q77-006) | The source tells you what changed, so no watermark is needed |

Note what all four have in common: none of them makes the extraction exact on its own. Three of them make the *load* tolerant of imprecision instead, which is the data engineering lesson generally — at-least-once delivery plus idempotent writes beats trying to achieve exactly-once in the extract (Q77-008).

| Tier | What to say |
|---|---|
| Passes | "`>=` will duplicate the boundary row" |
| Strong | + that `>` loses rows when timestamps tie, so the operator alone cannot fix it, and names idempotent merge as the real answer |
| Extra points | **[+Edge cases]** clock skew between source and loader can move the watermark backwards, making it worse than either · **[+Edge cases]** a source `updated_at` that the application forgets to set on some paths is Q77-011's problem, underneath this one · **[+Business]** a lost row is far worse than a duplicated one, because the duplicate is detectable and the loss is not · **[+Scale]** `(updated_at, id)` as a composite watermark is cheap and removes the tie entirely |

**Likely follow-ups:** How does a merge make the duplicate harmless? What if the source's clock is behind yours? How would you detect a lost row after the fact? *(Row counts against the source, per window.)*
**Learn it in:** Chapter 77, Q77-007 (idempotency); Chapter 47, section 47.5 (incremental loads).

### Q77-041 · The same 300,000-row table as CSV and as Parquet

**Level:** Mid · **Roles:** DE, AE

**Remember it as:** *Parquet is smaller, keeps its types, and reads one column almost free. It is not automatically faster at reading everything.*

**Answer in one line:** Parquet is **3.3× smaller** and reading a single column takes **5 ms against 325 ms** for all four — but reading the whole table was actually *slower* than the CSV here, and the real win is that the CSV loses the date type entirely.

```python
csv_path, pq_path = 'orders.csv', 'orders.parquet'
big.to_csv(csv_path, index=False)
big.to_parquet(pq_path, index=False)

print(f"CSV     {os.path.getsize(csv_path)/1024/1024:6.1f} MB")
print(f"Parquet {os.path.getsize(pq_path)/1024/1024:6.1f} MB")
print(f"read all columns  -> csv {rc*1000:.0f} ms, parquet {rp*1000:.0f} ms")
print(f"read one column   -> parquet {rp1*1000:.0f} ms")
print(f"dtypes from parquet: {pd.read_parquet(pq_path).order_date.dtype}")
print(f"dtypes from csv    : {pd.read_csv(csv_path).order_date.dtype}")
```

```
CSV       10.1 MB
Parquet    3.0 MB
read all columns  -> csv 159 ms, parquet 325 ms
read one column   -> parquet 5 ms
dtypes from parquet: datetime64[us]
dtypes from csv    : str
```

Three findings, and the honest one is the middle.

**Size: 3.3× smaller.** Parquet stores a column together and compresses it, and a column of four repeated status strings compresses to almost nothing where a CSV repeats the word on every row.

**Reading everything: not faster.** 325 ms against 159 ms on this file. Parquet has to decompress, and at 300,000 rows the CSV parser is quick. The "Parquet is faster" claim comes from queries that read a few columns from a large file, not from reading everything from a small one.

**Reading one column: 5 ms, roughly 65× faster than reading all four.** This is the real advantage, and it is structural rather than incidental: a columnar file lets the reader skip the columns it was not asked for. A table with 80 columns where your query needs 3 is where this becomes the difference between a dashboard that loads and one that does not — and it is also why `SELECT *` costs more on columnar storage than people expect (Q77-026).

**And the types survive.** The CSV round-trip returned `order_date` as a string. Every consumer now has to re-parse it, with its own idea of the date format, which is a class of bug Parquet removes by carrying the schema in the file.

| Tier | What to say |
|---|---|
| Passes | "Parquet is columnar, so it's smaller and faster" |
| Strong | + that it is not faster for a full read of a small file, and that the real wins are column pruning and schema preservation |
| Extra points | **[+Scale]** the advantage grows with the number of columns you *do not* read, so it is largest on wide tables · **[+Validate]** a CSV round-trip losing the date type is a silent correctness issue, not a performance one · **[+Trade-offs]** CSV is still right when a human must open the file, or when the consumer cannot read Parquet · **[+Edge cases]** Parquet also stores per-column statistics, so a reader can skip whole row groups that cannot match a filter — predicate pushdown |

**Likely follow-ups:** What is predicate pushdown? When would you still choose CSV? How does partitioning interact with it? *(Q77-023 — partition pruning skips files, column pruning skips columns, and you want both.)*
**Learn it in:** Chapter 48, section 48.3 (file formats); Chapter 77, Q77-027.

### Q77-042 · A daily job scheduled at 01:30, in London, on 30 March

**Level:** Brain-racking · **Roles:** DE, AE

**Remember it as:** *Twice a year, one local hour does not exist and another happens twice. A job scheduled in local time is scheduled into a gap.*

**Answer in one line:** **It never runs** — 01:30 does not exist on 30 March in London, because the clocks jump from 01:00 straight to 02:00, and asking pandas for that timestamp raises `ValueError: nonexistent time`.

```python
idx = pd.date_range('2025-03-30 00:00', periods=6, freq='h', tz='Europe/London')
print([t.strftime('%H:%M') for t in idx])

pd.Timestamp('2025-03-30 01:30', tz='Europe/London')
```

```
['00:00', '02:00', '03:00', '04:00', '05:00', '06:00']

ValueError: 2025-03-30 01:30:00 is a nonexistent time due to daylight savings time
```

Look at the hours: midnight, then **02:00**. The 01:00 hour is not there. A cron entry for `30 1 * * *` on a server in local time simply does not fire that day, and a daily pipeline silently has a one-day hole.

Seven months later the opposite happens. On 26 October, 01:30 occurs **twice**, and the timestamp is ambiguous:

```python
s = pd.Series(pd.to_datetime(['2025-10-26 01:30']))
for amb in (True, False):
    out = s.dt.tz_localize('Europe/London', ambiguous=np.array([amb]))
    print(f"ambiguous={amb} -> {out.iloc[0]}  (UTC {out.dt.tz_convert('UTC').iloc[0]})")

s.dt.tz_localize('Europe/London')
```

```
ambiguous=True  -> 2025-10-26 01:30:00+01:00  (UTC 2025-10-26 00:30:00+00:00)
ambiguous=False -> 2025-10-26 01:30:00+00:00  (UTC 2025-10-26 01:30:00+00:00)

ValueError: Cannot infer dst time from 2025-10-26 01:30:00, try using the 'ambiguous' argument
```

The same wall-clock time maps to two different UTC instants an hour apart. A job scheduled then runs twice, and if it is not idempotent it double-loads a day (Q77-007).

India is the easy case and worth saying so: **Asia/Kolkata has no daylight saving**, so none of this happens there. That is exactly why an engineer who has only run pipelines in India can be caught by it, and why the question gets asked.

The rules that follow are short:

- **Schedule and store in UTC.** Convert to local only for display.
- Where a business day genuinely must be local — a daily revenue cut-off — store the timezone with it and be explicit about the two broken days a year.
- Never do date arithmetic on a naive timestamp that came from somewhere with DST.

| Tier | What to say |
|---|---|
| Passes | "Daylight saving causes problems" |
| Strong | + both failures named — a missing hour in spring and a repeated hour in autumn — with the consequence for a scheduled job, and "run in UTC" as the rule |
| Extra points | **[+Edge cases]** Asia/Kolkata has no DST, so the bug is invisible to an India-only team until a European source appears · **[+Business]** the autumn case double-loads a day unless the job is idempotent, which links straight to Q77-007 · **[+Edge cases]** timezone rules change by legislation, so a stale `tzdata` package produces wrong conversions for future dates · **[+Validate]** a daily row count with exactly one missing day in late March is the signature |

**Likely follow-ups:** What does `ambiguous='infer'` do? How do you store a future appointment in local time? *(Store the local time and the zone, not the UTC instant — because the rules may change.)* Why does `tzdata` need updating?
**Learn it in:** Chapter 14, section 14.7 (dates and time zones); Chapter 47, section 47.6 (scheduling).

### Q77-043 · 31 January plus one month, minus one month

**Level:** Mid · **Roles:** DE, AE, DA

**Remember it as:** *Month arithmetic clamps to the end of the shorter month, and clamping does not undo. You cannot get back to where you started.*

**Answer in one line:** **28 January**, not 31 January — adding a month clamps to 28 February, and subtracting one from there goes back to 28 January, so the operation is not reversible and a "same period last month" calculation drifts.

```python
d0 = pd.Timestamp('2025-01-31')
print(f"+ DateOffset(months=1) = {(d0 + pd.DateOffset(months=1)).date()}")
print(f"+ Timedelta(days=30)   = {(d0 + pd.Timedelta(days=30)).date()}")

back = (d0 + pd.DateOffset(months=1)) - pd.DateOffset(months=1)
print(f"+1 month then -1 month = {back.date()}")
```

```
+ DateOffset(months=1) = 2025-02-28
+ Timedelta(days=30)   = 2025-03-02
+1 month then -1 month = 2025-01-28
```

Three different notions of "a month" in three lines. `DateOffset(months=1)` moves the calendar month and clamps the day. `Timedelta(days=30)` adds exactly 30 days and sails past the end of February into March. And the round trip loses three days.

Where it bites is month-on-month comparison. A report that computes "this period last month" by subtracting one month from each end of the window will, on the 29th, 30th and 31st, compare against a window that does not line up — and because February is the only month short enough to clamp hard, the error appears once a year and in one direction, which makes it look like a seasonal effect rather than a bug.

The reliable way to express a month is the half-open range on month boundaries, which is the same discipline as Chapter 71's date filters:

```python
start = pd.Timestamp('2025-01-01')
end   = start + pd.offsets.MonthBegin(1)
print(f"{start.date()} <= order_date < {end.date()}")
```

```
2025-01-01 <= order_date < 2025-02-01
```

No clamping, no ambiguity, and it works identically for every month length including February in a leap year.

| Tier | What to say |
|---|---|
| Passes | "Adding a month to 31 January gives 28 February" |
| Strong | + that the operation does not round-trip, and that `Timedelta(days=30)` is a third, different answer |
| Extra points | **[+Business]** month-on-month windows drift on the 29th to 31st, and the error looks seasonal because only February clamps hard · **[+Validate]** a half-open range on month boundaries removes the question entirely · **[+Edge cases]** `MonthEnd` against `MonthBegin` against `DateOffset(months=1)` are three different operators, and SQL engines disagree with each other too — `ADD_MONTHS` clamps, naive date addition does not |

**Likely follow-ups:** What does SQL's `ADD_MONTHS` do? *(Clamps, like `DateOffset`.)* How would you define "the same day last month" for the 31st? *(You have to decide, and write it down.)* What about leap years?
**Learn it in:** Chapter 14, section 14.7 (dates); Chapter 71, Q71-108 (half-open ranges).

### Q77-044 · A column that is integer for 10,000 rows and then has one blank

**Level:** Fresher · **Roles:** DE, AE, DA

**Remember it as:** *NumPy's integer type has no room for a missing value, so one blank converts the whole column to float.*

**Answer in one line:** The column becomes **`float64`**, with the values rendered as `5.0` instead of `5` — because `int64` cannot hold a null, so pandas promotes the entire column to float to make space for one.

```python
csv_text = "order_id,qty\n9007199254740993,5\n9007199254740994,\n"
d = pd.read_csv(io.StringIO(csv_text))
print(d.dtypes.to_dict())
print(f"qty values: {d.qty.tolist()}")

d2 = pd.read_csv(io.StringIO(csv_text), dtype={'order_id': 'Int64', 'qty': 'Int64'})
print(f"with Int64: {d2.qty.tolist()}")
```

```
{'order_id': dtype('int64'), 'qty': dtype('float64')}
qty values: [5.0, nan]
with Int64: [5, <NA>]
```

On a quantity column the damage is cosmetic — `5.0` in a report instead of `5`, which someone will eventually ask about. On an **id** column it is not cosmetic at all, because that is exactly how a 19-digit id ends up in a float and starts colliding (Q77-037).

It is also a type the next step did not expect. A downstream `CREATE TABLE ... qty INTEGER` load rejects `5.0`, or truncates it, depending on the target; a join between an `int64` key on one side and a `float64` key on the other matches nothing in some engines and silently casts in others.

The pattern is worth generalising, because it is the root of the three questions before this one: **a reader that infers types will infer them from the data it happens to see.** One blank, one `'N/A'`, one leading zero, and the column's type changes for every row. Declaring the schema at the boundary — `dtype=`, a data contract, or a self-describing format like Parquet — is the single habit that removes all of them.

| Tier | What to say |
|---|---|
| Passes | "It becomes a float because of the null" |
| Strong | + that NumPy's `int64` has no null representation, with `Int64` as the nullable alternative, and connects it to the id-precision problem |
| Extra points | **[+Edge cases]** the same promotion happens on a `groupby` that produces empty groups, and after a left join that does not match · **[+Business]** `5.0` reaching a report is the visible symptom; a corrupted id is the invisible one · **[+Scale]** declaring `dtype` at read time is also faster, because the reader stops guessing |

**Likely follow-ups:** What is the difference between `np.nan` and `pd.NA`? Why does a left join turn integer columns into floats? What does Arrow do differently? *(It has nullable integers natively, which is why pandas is moving that way.)*
**Learn it in:** Chapter 18, section 18.1 (NumPy and dtypes); Chapter 14, section 14.3.

### Rapid-fire, 77.8: things that silently change your rows

Roles: DE and AE for every row.

| # | Question | The answer, and why | Extra point |
|---|---|---|---|
| Q77-045 | `wc -l` on a CSV — is that the row count? | No. A quoted field may contain a newline, so one line is not one record. Use the parser's count | **[+Validate]** disagreeing counts between `wc -l` and the loader is the tell → Q77-039 |
| Q77-046 | Two sources, one with naive timestamps and one with UTC offsets. Joining on time? | Anything from an exact match to a 5½-hour error for IST. Normalise to UTC at ingestion, always | **[+Edge cases]** a naive timestamp has no meaning without knowing its source zone → Q77-042 |
| Q77-047 | `df.drop_duplicates()` on a float key | Unreliable: two values that print the same can differ in the last bit. Deduplicate on an exact type | **[+Business]** which is another reason ids should never be floats → Q77-037 |
| Q77-048 | A left join that matches nothing — what happens to the integer columns? | They become float, filled with NaN. The dtype change is often noticed before the missing match is | **[+Validate]** check row counts and null counts after every join → Q77-044 |
| Q77-049 | UTF-8 BOM at the start of a CSV from Excel | Depends on the reader: pandas 3.0 strips it, but `csv.DictReader` on `utf-8` makes the first field `'﻿customer_id'` so `row['customer_id']` is a `KeyError`, and `json.loads` raises `Unexpected UTF-8 BOM`. Read with `encoding='utf-8-sig'` | **[+Business]** the same file works in one tool and fails in the next, which is the worst kind of bug to triage → Ch 47 §47.3 |
| Q77-050 | Does `ORDER BY` in a subquery or CTE survive into the outer query? | Not guaranteed. The optimiser may discard it. Sort in the outermost query only | **[+Scale]** a sort you did not need is also expensive at volume → Ch 28 §28.5 |
| Q77-051 | A pipeline runs at 00:05 for "yesterday". What happens when it is late? | It still asks for yesterday relative to *now*, so a run at 00:02 the next day skips a whole day. Pass the logical date in, never compute it from the clock | **[+Business]** this is why orchestrators supply an execution date → Ch 47 §47.6 |
| Q77-052 | Two ids that differ only in case, or by a trailing space | Distinct in most engines, equal in MySQL's default collation and after an Excel round trip. Normalise keys on ingestion | **[+Edge cases]** the same split as Ch 71 Q71-100 → Ch 14 §14.5 |
| Q77-053 | `float` revenue summed per group, then summed again overall | The two totals can differ in the last decimals, so a reconciliation check with `==` fails on correct data | **[+Validate]** reconcile with a tolerance, or store money as integer paise → Ch 12 §12.8 |
| Q77-054 | A schema change adds a column in the middle of a CSV | Positional readers shift every column after it; named readers are fine. This is schema drift with no error | **[+Business]** read by name, never by position, and validate the header → Q77-009 |
| Q77-055 | Compression: does gzip let you read part of a file? | Not usefully — gzip is not splittable, so a big gzipped CSV cannot be read in parallel. Snappy Parquet can | **[+Scale]** one 10 GB gzip file is a single-threaded job whatever the cluster size → Ch 48 §48.3 |
| Q77-056 | A `MERGE` keyed on a column that has duplicates in the source | Engines differ: some raise, some pick arbitrarily. Deduplicate the source before merging, deliberately | **[+Validate]** assert the key is unique before the merge, as a pipeline test → Q77-007 |

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
| Reading identifier columns without `dtype=str` | Leading zeros vanish and the join silently matches nothing | Declare the type at read time, or use a self-describing format (Q77-036) |
| Letting one blank turn an id column into a float | Ids past 2⁵³ collide, so `COUNT(DISTINCT)` quietly falls | pandas `Int64`, or read ids as text (Q77-037, Q77-044) |
| Trusting a reader's default missing-value list | A real `NA` or `NULL` value is destroyed on the way in | `keep_default_na=False`, and validate the distinct set against the source (Q77-038) |
| An incremental watermark with `>=` or `>` alone | Duplicates the boundary row, or loses a row that ties on the second | `>=` plus an idempotent merge, or a composite `(updated_at, id)` watermark (Q77-040) |
| Scheduling a job in local time | It never runs on the spring-forward day and runs twice in autumn | Schedule and store in UTC; take the logical date from the orchestrator (Q77-042) |
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

ETL vs. ELT · batch vs. streaming · data warehouse vs. data lake vs. lakehouse · data contract · CDC (Change Data Capture) · idempotency · upsert (`ON CONFLICT`, `EXCLUDED`) · at-least-once / at-most-once / exactly-once delivery · schema drift · backfilling · dead-letter queue · SCD Type 1/2/3 · surrogate key · half-open validity period · fact table grain · junk dimension · DAG (Directed Acyclic Graph) · topological sort · Kahn's algorithm · in-degree · sensor (orchestration) · backpressure · consumer lag · partitioning · partition pruning · sharding · materialized view · columnar storage · data observability · data lineage · heartbeat (dead-man's switch) · alert fatigue · write–audit–publish · watermark · blocking (deduplication) · type inference · `dtype=` at read time · nullable integer (`Int64`) · 2⁵³ precision limit · default NA markers · `keep_default_na` · CSV quoting and escaping · field shift · columnar format · column pruning · predicate pushdown · splittable compression · nonexistent and ambiguous local times · UTC-first scheduling · logical (execution) date · month-end clamping · half-open date range · byte-order mark (BOM)

---

## Final-week revision list

Q77-001, Q77-002, Q77-007, Q77-008, Q77-013, Q77-018, Q77-023, Q77-028, Q77-033, Q77-034, Q77-035, Q77-037, Q77-040, Q77-042.

The last three are the loads that complete successfully and are still wrong: a 19-digit id losing precision in a float column (Q77-037), a watermark that either duplicates or loses the boundary row (Q77-040), and a job scheduled into an hour that does not exist (Q77-042).

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 71, SQL Question Bank,** already covers the join-cardinality, indexing (section 71.9), and materialized-view foundations this chapter builds directly on.
- **Chapter 72A, Data Structures & Algorithms Question Bank,** supplies the complexity reasoning (O(n²) scaling, walking graphs with BFS and DFS) this chapter's design questions reuse explicitly.
- **Chapter 78, Automation & Integration Question Bank,** applies this chapter's idempotency, retry and monitoring answers to business automations and integrations.
- **Part 5 of this book** (data engineering proper) teaches every technique this bank draws on, in full; this chapter tests it, it doesn't re-teach it from scratch.
