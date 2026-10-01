-- Chapter 77. Data Engineering & Data System Design Bank
-- Practice SQL for MYSQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_mysql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch77-data-engineering-and-data-system-design-bank.md


-- =============================================================================================
-- Chapter 77. Data Engineering & Data System Design Bank
-- =============================================================================================

-- Part 8 — Be Interview Ready

-- > Chapter at a glance > > You will learn to: answer the pipeline, data-modeling, and system-
-- design questions that come up in Data Engineer interviews · design a batch or streaming pipeline
-- live, under time pressure, the way an interviewer actually wants · reason correctly about
-- idempotency, partitioning, and schema evolution, not just define the terms · walk through a full
-- system design case end to end, stating trade-offs out loud. > > Before you start: Chapter 69
-- (the three answer tiers and the twelve extra-point moves). The questions test Part 5 (Chapters
-- 45–52: ingestion, pipelines, data quality, distributed compute, storage, streaming, activation
-- and deployment) and Chapter 28 (query plans, grain, the star schema, slowly changing
-- dimensions). They also link to Chapter 12, section 12.13 (the upsert), Chapter 33 (queues and
-- graphs), Chapter 61 (partitioning and sharding), and the two banks this one leans on, Chapter 71
-- (SQL) and Chapter 72A (complexity). This chapter tests those skills; it doesn't teach them
-- again, with one exception: Q77-018 builds topological sort step by step, because no earlier
-- chapter does. > > Time needed: 3–4 hours for a first pass (about 10 minutes per core question,
-- including running its code, and 1–2 minutes per rapid-fire row), plus 1 hour for the final-week
-- list. > > How this chapter is built. Same format as the other question banks in Part 8 (Chapters
-- 70 onward): every core question leads with a "Remember it as…" hook, then a one-line answer,
-- then a compact tier table (what passes, what's strong, and the extra points, tagged with Chapter
-- 69's moves: [+Trade-offs], [+Edge cases], [+Validate] and so on). Rapid-fire sections are scan
-- tables: question, one-line answer, one extra point, level, and where to learn it. Every SQL
-- result shown was run on PostgreSQL 16 in riverstone_lab, the practice database you created in
-- Chapter 12, section 12.13; each demo drops its tables at the end. Every Python output is real,
-- from Python 3.11.15 with the standard library only (the book recommends Python 3.14, Chapter 17,
-- section 17.0; nothing here depends on the version). The sections run from pipeline fundamentals
-- to modeling, reliability, orchestration, scale and quality, and end with full system-design
-- walk-throughs. > > Levels and roles. Each core question carries a level and the roles that
-- usually ask it. Fresher: screening calls and first-job interviews. Mid: one to three years in
-- the role. Senior: lead or specialist rounds. DE data engineer · AE analytics engineer · MLE
-- machine learning engineer · ARCH data architect. Learn it in pointers name the chapter and
-- section where each idea is taught, mostly Part 5 (Chapters 45–52) and Chapter 28 (data
-- modeling); where another bank drills it, a Practise it with pointer follows.

-- ---

-- =============================================================================================
-- 77.1 Pipeline fundamentals
-- =============================================================================================

-- =============================================================================================
-- Q77-001 · ETL vs. ELT: what's the actual difference, and when does it matter which you pick?
-- =============================================================================================

-- Level: Fresher · Roles: DE, AE

-- Remember it as: ETL transforms before loading, in a separate processing step. ELT loads raw data
-- first and transforms inside the warehouse itself, using the warehouse's own compute.

-- Answer in one line: ETL (Extract, Transform, Load) transforms data in a separate processing
-- layer before it ever reaches the destination system; ELT (Extract, Load, Transform) loads raw
-- data into the destination (usually a modern cloud warehouse) first, then transforms it there
-- using the warehouse's own compute power, which became the dominant pattern once cloud warehouses
-- got cheap and powerful enough to make that practical.

-- | Tier | What to say | |---|---| | Passes | "ETL and ELT do the same three steps in a different
-- order" (technically true, misses why the order matters) | | Strong | + explains the practical
-- driver: ELT keeps a full copy of raw data in the warehouse (useful for reprocessing or auditing
-- later), and pushes transformation compute onto the warehouse rather than a separate processing
-- cluster | | Extra points | + [+Trade-offs] ELT's "load everything raw first" approach means raw,
-- unvalidated data briefly exists in the warehouse before transformation, a real consideration for
-- compliance-sensitive data + [+Business] the choice is rarely purely technical anymore; it's
-- often driven by which the team's existing tooling (dbt, Airflow, a specific cloud warehouse) is
-- already built around |

-- Likely follow-ups: Name a scenario where ETL is still clearly the better choice today. What's
-- reverse ETL, and how does it relate to either pattern? Red flag: treating the two as
-- interchangeable synonyms. Learn it in: Chapter 32, §32.1 (ETL versus ELT) and Chapter 45, §45.1
-- (where company data comes from, and the warehouse's layers). Reverse ETL: Chapter 51.

-- =============================================================================================
-- Q77-002 · Batch vs. streaming: how do you decide which a new pipeline actually needs?
-- =============================================================================================

-- Level: Fresher · Roles: DE, MLE

-- Remember it as: Ask how fresh the answer actually needs to be, in business terms, before
-- assuming streaming is the more impressive, more correct choice.

-- Answer in one line: Batch processing runs on a schedule (hourly, daily), processing accumulated
-- data in one pass, simpler to build and debug; streaming processes events continuously as they
-- arrive, needed when a decision genuinely can't wait for the next batch window, and the right
-- choice depends entirely on how fresh the downstream decision actually needs to be, not on which
-- technology is more modern.

-- | Tier | What to say | |---|---| | Passes | "Streaming is more real-time and modern, so it's
-- generally better" | | Strong | The freshness-driven decision above, with a concrete example
-- each: a daily sales summary report is a natural batch case; a fraud-detection system blocking a
-- transaction in real time is a natural streaming case | | Extra points | + [+Business] streaming
-- systems are meaningfully harder to build, test, and debug correctly (exactly-once semantics,
-- out-of-order events, windowing) than batch ones; choosing streaming for a problem that doesn't
-- actually need sub-minute freshness is real, avoidable added complexity, not a sign of
-- engineering sophistication |

-- Likely follow-ups: What's micro-batching, and where does it sit between the two? How would you
-- migrate an existing batch pipeline to streaming without a risky big-bang rewrite? Red flag:
-- recommending streaming by default without asking what freshness the actual decision requires.
-- Learn it in: Chapter 50, §50.1 (what "real-time" actually means) and §50.8 (when Riverstone
-- would not build a stream).

-- =============================================================================================
-- Rapid-fire, 77.1
-- =============================================================================================

-- Roles: DE and AE for every row.

-- | # | Question | One-line answer | Extra point | Level · learn it in | |---|---|---|---|---| |
-- Q77-003 | What's a data warehouse vs. a data lake vs. a lakehouse? | Structured, schema-on-
-- write, optimized for analytics queries / raw, schema-on-read, stores any format cheaply / a
-- hybrid combining a lake's flexible storage with a warehouse's structured querying and
-- transaction support | [+Trade-offs] a lakehouse is a lake plus a table format (Delta Lake,
-- Iceberg) that gives plain files transactions, schema changes and time travel | Fresher · 49.1,
-- 49.5, 49.7; star schema 28.9 | | Q77-004 | What's a data contract? | An explicit agreement
-- between a data producer and consumer about a dataset's schema, format, and update cadence, so
-- downstream pipelines don't silently break when the source changes | [+Business] the DE-team
-- equivalent of an API contract between two services | Mid · 47.7 | | Q77-005 | What's the
-- difference between a full load and an incremental load? | A full load reprocesses the entire
-- source every run; an incremental load processes only new or changed records since the last run,
-- using a timestamp or change-tracking mechanism | [+Trade-offs] full loads are simpler and self-
-- healing but don't scale to large sources; incremental loads scale but need careful handling of
-- updates and deletes, not just new rows | Fresher · 45.3–45.4 | | Q77-006 | What's CDC (Change
-- Data Capture)? | A technique for detecting and capturing row-level changes (inserts, updates,
-- deletes) in a source database, often by reading its transaction log, to drive incremental
-- pipelines without querying the whole source table | [+Business] CDC avoids the "how do I know
-- what changed" problem incremental loading otherwise has to solve with timestamps, which can miss
-- deletes entirely | Mid · 45.6 |

-- ---

-- =============================================================================================
-- 77.2 Basic-but-tricky data engineering questions
-- =============================================================================================

-- =============================================================================================
-- Q77-007 · Your pipeline runs on a schedule, but if it fails and gets re-run, it duplicates every row it already loaded. What's the fix?
-- =============================================================================================

-- Level: Fresher · Roles: DE, AE

-- Remember it as: A pipeline that can safely run twice with the same input and produce the same
-- result is idempotent. One that can't, isn't safe to retry, ever.

-- Answer in one line: Make the load step idempotent: use an upsert (insert-or-update) keyed on a
-- unique identifier instead of a plain insert, so re-running the same load with the same data
-- updates existing rows instead of duplicating them.

-- Verified, in riverstone_lab. First the table. The primary key on order_date is what makes "the
-- same day" detectable:

-- <!-- Verifier setup, not printed: the lab database the reader made in Chapter 12.

CREATE DATABASE riverstone_lab;


-- -->

CREATE TABLE daily_summary (
    order_date     DATE PRIMARY KEY,
    total_revenue  NUMERIC(12,2) NOT NULL
);


-- Now the load step. ₹20,900 is Riverstone's real net revenue on 5 January 2025 (one order, in
-- riverstone_2025):

INSERT INTO daily_summary VALUES ('2025-01-05', 20900.00)
    ON CONFLICT (order_date)
    DO UPDATE SET total_revenue = EXCLUDED.total_revenue;

SELECT * FROM daily_summary;

/* The chapter shows:
    order_date | total_revenue
   ------------+---------------
    2025-01-05 |      20900.00
   (1 row)
*/


-- - ON CONFLICT (order_date) names the unique column to check. If a row for that date already
-- exists, PostgreSQL doesn't insert; it runs the DO UPDATE part instead. - EXCLUDED means "the row
-- you tried to insert" (Chapter 12, section 12.13), so total_revenue = EXCLUDED.total_revenue
-- copies the new value onto the existing row.

-- The job fails later that night and gets re-run. Run the exact same statement a second time, then
-- count the rows:

INSERT INTO daily_summary VALUES ('2025-01-05', 20900.00)
    ON CONFLICT (order_date)
    DO UPDATE SET total_revenue = EXCLUDED.total_revenue;

SELECT COUNT(*) FROM daily_summary;

/* The chapter shows:
    count
   -------
        1
   (1 row)
*/


-- One row, not two. What if the table had no primary key? Try the same upsert on a copy without
-- one, and predict what happens before you run it:

CREATE TABLE daily_summary_nokey (
    order_date     DATE,
    total_revenue  NUMERIC(12,2) NOT NULL
);

INSERT INTO daily_summary_nokey VALUES ('2025-01-05', 20900.00)
    ON CONFLICT (order_date)
    DO UPDATE SET total_revenue = EXCLUDED.total_revenue;

/* The chapter shows:
   ERROR:  there is no unique or exclusion constraint matching the ON CONFLICT specification
*/


-- ON CONFLICT only works when the conflict column is declared unique: without the key, the
-- database has no way to tell that two rows are "the same day". Clean up:

DROP TABLE daily_summary, daily_summary_nokey;


-- | Tier | What to say | |---|---| | Passes | "Add a check to skip rows that already exist" (a
-- partial fix, misses the case where a value genuinely needs updating on retry) | | Strong | The
-- upsert pattern above, explaining that idempotency means safe retry, not just avoiding duplicates
-- on first run, and that the upsert needs a unique key on the business key (here, the date) | |
-- Extra points | + [+Validate] the real proof above: the same statement run twice leaves exactly
-- one row, not two + [+Business] idempotency is what makes "just re-run the failed job" a safe,
-- boring operational response instead of a risky one that needs careful manual cleanup first |

-- Likely follow-ups: How would you make a multi-step pipeline (not just one insert) idempotent end
-- to end? What's the difference between idempotency and exactly-once processing? Red flag: a fix
-- that only prevents duplicates on a clean re-run, not one that's genuinely safe to retry after a
-- partial failure mid-load. Learn it in: Chapter 12, §12.13 (step 7, the upsert); Chapter 45,
-- §45.5 (why upserts make loads safe to repeat); Chapter 46, §46.4 (idempotency, proven with a
-- failure test).

-- =============================================================================================
-- Q77-008 · What's the difference between "at-least-once," "at-most-once," and "exactly-once" delivery, and which is actually achievable?
-- =============================================================================================

-- Level: Mid · Roles: DE, MLE

-- Remember it as: At-least-once can duplicate. At-most-once can lose data. Exactly-once, in the
-- strict sense, usually isn't really achievable end to end, only effectively achievable by
-- combining at-least-once delivery with idempotent processing on the receiving end.

-- Answer in one line: At-least-once guarantees a message is delivered, possibly more than once
-- (safe against loss, risks duplication); at-most-once guarantees no duplication, possibly at the
-- cost of losing a message entirely (safe against duplication, risks loss); true exactly-once
-- delivery across a genuinely distributed system is famously difficult and, in most real systems,
-- achieved in practice by combining at-least-once delivery with idempotent processing downstream
-- (Q77-007), not by a delivery mechanism that's magically exactly-once on its own.

-- | Tier | What to say | |---|---| | Passes | Defines at-least-once and at-most-once correctly,
-- but treats exactly-once as a setting you switch on | | Strong | The three-way distinction above,
-- and specifically names idempotent processing as the real mechanism behind most practical
-- "exactly-once" claims | | Extra points | + [+Signpost] this is precisely why Q77-007's upsert
-- pattern matters beyond just convenience: it's what turns an honestly at-least-once delivery
-- guarantee into an effectively exactly-once outcome + [+Trade-offs] the other route, used by
-- Spark checkpoints and Kafka transactions (Chapter 50, §50.3), commits the output and the read
-- position together in one transaction: real exactly-once, but narrower and slower |

-- Likely follow-ups: Which would you choose for a financial transaction log, and why? What's a
-- real system that claims exactly-once, and how does it actually achieve it under the hood? Red
-- flag: treating "exactly-once" as a simple guarantee some systems just have and others don't,
-- with no understanding of how it's actually achieved. Learn it in: Chapter 50, §50.3 (delivery
-- guarantees, and the duplicates you will get) and Chapter 51, §51.4 (making writes idempotent,
-- and proving it).

-- =============================================================================================
-- Rapid-fire, 77.2
-- =============================================================================================

-- Roles: DE and AE for every row.

-- | # | Question | One-line answer | Extra point | Level · learn it in | |---|---|---|---|---| |
-- Q77-009 | What's schema drift, and why is it dangerous in an automated pipeline? | A source
-- system's schema changing (a renamed column, a new field, a changed data type) without the
-- downstream pipeline being updated to match, often causing a silent failure or silently wrong
-- data rather than a loud error | [+Business] a pipeline that fails loudly on schema drift is far
-- safer than one that silently adapts (or silently drops the new column), which can hide the
-- problem for weeks | Mid · 45.8; contracts 47.7 | | Q77-010 | What's backfilling, and why does it
-- need special care? | Reprocessing historical data, usually after a bug fix or a new metric
-- definition; needs care because it can be expensive at scale, and because downstream reports or
-- dashboards using the old values need a plan for the transition, not just silently different
-- historical numbers | [+Edge cases] a backfill that changes historical numbers without any
-- announcement is a fast way to lose a stakeholder's trust in a dashboard | Mid · 46.5 | | Q77-011
-- | Why can't you always trust a source system's own "last modified" timestamp for incremental
-- loading? | Clock skew between systems, a source that doesn't update the timestamp on every field
-- change, or a source that allows backdated edits can all make a naive timestamp-based incremental
-- load silently miss real changes | [+Edge cases] no timestamp ever shows a deleted row, because
-- nothing is left to carry one; CDC (Q77-006) reads deletes from the log | Mid · 45.4–45.6 | |
-- Q77-012 | What's a dead-letter queue? | A separate holding location for messages or records that
-- failed processing repeatedly, so they don't block the rest of the pipeline and can be
-- investigated separately | [+Business] without one, a single malformed record can silently halt
-- an entire stream or repeatedly retry and fail forever | Fresher · 50.7 (the dead-letter path) |

-- ---

-- =============================================================================================
-- 77.3 Data modeling for pipelines and warehouses
-- =============================================================================================

-- =============================================================================================
-- Q77-013 · Implement Slowly Changing Dimension (SCD) Type 2 for a customer whose segment changes, and explain why Type 1 wouldn't preserve history
-- =============================================================================================

-- Level: Mid · Roles: DE, AE

-- Remember it as: Type 1 overwrites, so the past is gone. Type 2 closes the old row and opens a
-- new one, so you can always ask "what did we believe was true on this date."

-- Answer in one line: SCD Type 1 overwrites the old value in place, losing all history of what it
-- used to be; SCD Type 2 keeps every historical version as its own row, with validity date ranges
-- (and usually a current-flag), so you can query the dimension as it looked at any point in the
-- past, not just as it looks today.

-- Verified, in riverstone_lab. The change is a real one: riverstone_2025's customer_changes table
-- (Chapter 28, section 28.1) records Harbour Traders, customer 11, moving from Retail to Wholesale
-- on 1 September 2025. First the dimension, holding the customer's first version:

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


-- - customer_key is the surrogate key: the database numbers the versions 1, 2, 3… by itself, as in
-- Chapter 28, section 28.10. customer_id is the business key, and it repeats, once per version. -
-- valid_from and valid_to form a half-open period: the version is true from valid_from up to, but
-- not including, valid_to. So valid_to is the first day the row is no longer true, and 9999-12-31
-- means "still true". 9 April 2025 is the day Harbour Traders signed up.

-- Now the change: close the old version and open the new one, inside one transaction, so nobody
-- ever sees the customer with no current row:

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

/* The chapter shows:
    customer_key | customer_id |  customer_name  |  segment  | valid_from |  valid_to  | is_current
   --------------+-------------+-----------------+-----------+------------+------------+------------
               1 |          11 | Harbour Traders | Retail    | 2025-04-09 | 2025-09-01 | f
               2 |          11 | Harbour Traders | Wholesale | 2025-09-01 | 9999-12-31 | t
   (2 rows)
*/


-- BEGIN and COMMIT make the two statements one transaction (Chapter 12, section 12.13, step 8):
-- either both happen or neither does. The UPDATE closes version 1 by setting its valid_to to the
-- change date and is_current to FALSE; AND is_current makes sure only the open version is touched.
-- The INSERT adds version 2, and its customer_key, valid_to and is_current take their defaults.
-- The old row closes on the same date the new one opens. Check the two days either side of the
-- change with the same half-open test a fact table join uses (date >= valid_from AND date <
-- valid_to):

SELECT segment FROM customer_history
WHERE customer_id = 11
  AND DATE '2025-08-31' >= valid_from
  AND DATE '2025-08-31' <  valid_to;

SELECT segment FROM customer_history
WHERE customer_id = 11
  AND DATE '2025-09-01' >= valid_from
  AND DATE '2025-09-01' <  valid_to;

/* The chapter shows:
    segment
   ---------
    Retail
   (1 row)
   
     segment
   -----------
    Wholesale
   (1 row)
*/


-- Every day falls in exactly one version: no gap, no overlap. Clean up:

DROP TABLE customer_history;


-- dict(dag) makes a copy, so the original dag is untouched. Only extract_customers could start;
-- the other five tasks wait on each other in a loop and never reach 0.

-- | Tier | What to say | |---|---| | Passes | Describes the dependencies in English, produces an
-- order by eyeballing it rather than a systematic method | | Strong | Names topological sort
-- explicitly and produces a genuinely valid order, acknowledging more than one valid order can
-- exist (the two extracts could run in either order, or in parallel) | | Extra points | +
-- [+Validate] the real, algorithmically-produced order above, not a guessed one, and a cycle check
-- that fails loudly + [+Business] this is exactly what an orchestrator such as Dagster or Airflow
-- does automatically from a declared DAG: the engineer states dependencies, the scheduler
-- determines (and often parallelizes) a valid execution order, rather than the engineer hard-
-- coding a sequence |

-- Likely follow-ups: How would you detect a cycle in a dependency graph, meaning the DAG isn't
-- actually valid? Which of these tasks could safely run in parallel? Red flag: producing an order
-- that violates a stated dependency, or being unable to name the standard algorithm for this
-- problem. Learn it in: Chapter 46, §46.2 (pipelines as graphs, and why they must be acyclic);
-- Chapter 33, §33.4 (queues and deque) and §33.6 (walking graphs, cycles). Topological sort itself
-- is built in this question. Practise it with: Chapter 72A, Q72A-028 (BFS and DFS).

-- =============================================================================================
-- Rapid-fire, 77.4
-- =============================================================================================

-- Roles: DE and AE for every row.

-- | # | Question | One-line answer | Extra point | Level · learn it in | |---|---|---|---|---| |
-- Q77-019 | What does DAG stand for, and why must a pipeline's dependency graph be acyclic? |
-- Directed Acyclic Graph; a cycle (task A depends on B, which depends on A) has no valid execution
-- order at all, since neither could ever go first | [+Edge cases] a cycle is easy to create by
-- accident (a load that waits for the report that reads it); Q77-018's topo_order catches it,
-- because tasks in a loop never reach in-degree 0 | Fresher · 46.2 (practise: Q72A-028) | |
-- Q77-020 | What's a sensor (or a "wait for" task) in an orchestration tool? | Something that
-- reacts to an event outside the schedule. In Airflow a sensor is a task that waits for a
-- condition (a file to arrive, an upstream job to finish) before the rest of the pipeline
-- proceeds; in Dagster (Chapter 46, §46.6) a sensor watches for an event and starts a run or sends
-- an alert | [+Business] sensors are how a pipeline safely depends on something outside its own
-- DAG, like a third-party data delivery with no guaranteed exact timing | Mid · 46.2, 46.6, 46.8 |
-- | Q77-021 | What's the risk of a pipeline with a single point of failure at its very first task?
-- | Every single downstream task, however independent it looks, silently can't run if that one
-- upstream task fails, making the whole day's pipeline as fragile as its weakest single link |
-- [+Business] designing for partial success (independent tasks can still run and deliver partial
-- value even if one branch fails) is often worth the added complexity for a pipeline with many
-- independent downstream consumers | Mid · 46.10; 61.6–61.7 | | Q77-022 | What's backpressure, in
-- a streaming context? | A mechanism for a slower downstream consumer to signal an upstream
-- producer to slow down, preventing the consumer from being overwhelmed by data arriving faster
-- than it can process. With a log such as Kafka (Chapter 50), producers aren't slowed down: the
-- consumer reads at its own pace, and the gap shows up as consumer lag, which is why section 50.7
-- tells you to monitor lag | [+Business] without backpressure handling, a slow consumer either
-- falls further and further behind or crashes outright under load it can't keep up with | Mid ·
-- 50.2, 50.7 (lag) |

-- ---

-- =============================================================================================
-- 77.5 Scale, partitioning, and performance
-- =============================================================================================

-- =============================================================================================
-- Q77-023 · A table has grown to hundreds of millions of rows and queries filtering on date are slow. Walk through partitioning as a fix, and prove it works
-- =============================================================================================

-- Level: Mid · Roles: DE, AE

-- Remember it as: A partitioned table lets the database skip entire partitions it knows can't
-- contain a match, instead of scanning rows one at a time to find out.

-- Answer in one line: Range partitioning by date splits a large table into smaller physical sub-
-- tables, each holding a specific date range; a query filtering on date lets the query planner
-- skip (prune) any partition that can't possibly contain a match, dramatically reducing how much
-- data actually needs to be scanned.

-- Verified, in riverstone_lab. A small events table, partitioned by month:

CREATE TABLE events_partitioned (
    id          INTEGER GENERATED ALWAYS AS IDENTITY,
    event_date  DATE NOT NULL,
    payload     TEXT
) PARTITION BY RANGE (event_date);

CREATE TABLE events_2025_01 PARTITION OF events_partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE events_2025_02 PARTITION OF events_partitioned
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');


-- This is PostgreSQL's own partitioning syntax, which no earlier chapter uses:

-- - PARTITION BY RANGE (event_date) declares the parent table. It holds no rows itself; it says
-- which column decides where each row goes. - PARTITION OF events_partitioned FOR VALUES FROM (a)
-- TO (b) creates a child table, a partition, for the dates from a (included) up to b (excluded):
-- the same half-open rule as Q77-013, so 1 February belongs to February only. - On INSERT into the
-- parent, each row is routed to its child automatically.

-- Load 1,000 events into each month, then count what landed in each partition:

INSERT INTO events_partitioned (event_date, payload)
SELECT DATE '2025-01-01' + (n % 31), 'event ' || n
FROM generate_series(1, 1000) AS n;

INSERT INTO events_partitioned (event_date, payload)
SELECT DATE '2025-02-01' + (n % 28), 'event ' || n
FROM generate_series(1, 1000) AS n;

SELECT COUNT(*) AS january_rows FROM events_2025_01;
SELECT COUNT(*) AS february_rows FROM events_2025_02;

/* The chapter shows:
    january_rows
   --------------
            1000
   (1 row)
   
    february_rows
   ---------------
             1000
   (1 row)
*/


-- generate_series(1, 1000) (Chapter 13, section 13.8) makes the numbers 1 to 1,000, one row each,
-- called n. n % 31 is the remainder after dividing by 31 (0 to 30), and adding a whole number to a
-- DATE moves it forward that many days, so the rows spread across January's 31 days. 'event ' || n
-- joins text to the number. The rows went into the parent, and every one was routed to the right
-- month. Now collect statistics and ask for the plan:

ANALYZE events_partitioned;

EXPLAIN SELECT * FROM events_partitioned WHERE event_date = '2025-01-15';

/* The chapter shows:
                                        QUERY PLAN
   ------------------------------------------------------------------------------------
    Seq Scan on events_2025_01 events_partitioned  (cost=0.00..19.50 rows=32 width=17)
      Filter: (event_date = '2025-01-15'::date)
   (2 rows)
*/


-- ANALYZE counts the rows and samples their values, the statistics the planner uses to estimate
-- (Chapter 28, section 28.5). The numbers in brackets are those estimates; here only the partition
-- name matters. The query plan touches only the January partition, events_2025_01; the February
-- partition is never scanned at all, real, confirmed partition pruning.

-- What if the query doesn't filter on the partition key?

EXPLAIN SELECT * FROM events_partitioned WHERE payload = 'event 7';

/* The chapter shows:
                                           QUERY PLAN
   -------------------------------------------------------------------------------------------
    Append  (cost=0.00..39.01 rows=2 width=17)
      ->  Seq Scan on events_2025_01 events_partitioned_1  (cost=0.00..19.50 rows=1 width=17)
            Filter: (payload = 'event 7'::text)
      ->  Seq Scan on events_2025_02 events_partitioned_2  (cost=0.00..19.50 rows=1 width=17)
            Filter: (payload = 'event 7'::text)
   (5 rows)
*/


-- Both partitions are scanned, and Append glues their results together: with no date in the
-- filter, the planner can't rule out either month. Clean up (dropping the parent drops its
-- partitions too):

DROP TABLE events_partitioned;

