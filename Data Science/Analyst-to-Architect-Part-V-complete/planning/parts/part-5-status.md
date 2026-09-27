# Part V — Data Engineering, Integration & Scale · Status

Owner: Part V work (continued in the Part I chat at the author's request, 16 Sep 2026). Chapters 45–52. Instructions: `planning/chapter-writing-instructions.md`.

| ID | No. | Title | Class | Status | Words | Manuscript |
|---|---|---|---|---|---|---|
| P5-45 | 45 | Data Ingestion & Integration | B | **Approved (v1)** (16 Sep 2026) | ~12,000 incl. code and answers | `manuscript/ch45-data-ingestion-and-integration.md` |
| P5-46 | 46 | Pipelines & Orchestration | B | **Approved (v1)** (17 Sep 2026) | ~11,200 incl. code and answers | `manuscript/ch46-pipelines-and-orchestration.md` |
| P5-47 | 47 | Data Quality, Observability & Contracts | B | **Approved (v1)** (17 Sep 2026) | ~10,300 incl. code and answers | `manuscript/ch47-data-quality-observability-and-contracts.md` |
| P5-48 | 48 | Big Data & Distributed Compute | B | **Approved (v1)** (18 Sep 2026) | ~7,700 incl. code and answers | `manuscript/ch48-big-data-and-distributed-compute.md` |
| P5-49 | 49 | Storage, Warehouses & Lakehouses | B | **Approved (v1)** (18 Sep 2026) | ~7,700 incl. code and answers | `manuscript/ch49-storage-warehouses-and-lakehouses.md` |
| P5-50 | 50 | Streaming & Real-Time | B | **Approved (v1)** (18 Sep 2026) | ~7,900 incl. code and answers | `manuscript/ch50-streaming-and-real-time.md` |
| P5-51 | 51 | Data Activation: Reverse ETL, APIs & System Integration | B | **Approved (v1)** (19 Sep 2026) | ~8,400 incl. code and answers | `manuscript/ch51-data-activation.md` |
| P5-52 | 52 | The Cloud, Containers & Infrastructure as Code | B | **Approved (v1)** (19 Sep 2026) | ~9,400 incl. code and answers | `manuscript/ch52-the-cloud-containers-and-infrastructure-as-code.md` | |

---

## Chapter 45 report — Data Ingestion & Integration (v1, approved 16 Sep 2026)

**Approved by the author on 16 Sep 2026.** Approved PDF: `Ch45-Data-Ingestion-and-Integration-v1-approved.pdf`. Proposed Riverstone facts accepted with the chapter; coordinator to confirm against Part II's Ch 20 timeline.

### Contents
At a glance · Why · Plain English (kitchen receiving door) · 45.1 Source types, system of record, raw/staging/modeled · 45.2 Practice environment · 45.3 Full loads + reconciliation by status · 45.4 Incremental by ID watermark, **demonstrated missing two updates** (10174, 10175); updated_at pitfalls, look-back · 45.5 Row hashes (finds exactly the missed updates), upserts, idempotency demonstrated (plain INSERT fails on PK; upsert twice = 177 rows), cost of hashing, file hashes with a load log (promise from Ch 2) · 45.6 CDC with PostgreSQL logical decoding (`test_decoding`, real slot output), hash vs CDC agreement, abandoned-slot risk, strategy table · 45.7 Reliable CSV loading (promise from Ch 12): auto-detect silently types quantity as text; declared columns → raw text → typed staging with strptime/TRY_CAST → rejects list → reconciliation (5 lines, 5 loaded, 4 usable, 3,425 units); checklist; Parquet types (and why it's larger for a 5-row file) · 45.8 Schema drift detection and responses; data contracts → Ch 47 · 45.9 API ingestion: token, pagination, 429 retry with Retry-After (real run), 401 fail-fast, reconciliation (43 leads), offset pagination trap, checklist · 45.10 Build vs buy · 45.11 Web data legal/ethical limits (DPDP Act 2023, GDPR, ToS, robots.txt, copyright; not legal advice) · Common mistakes (15) · Real world: *The orders that never cancelled* · Tools · Project: incremental ingestion for Riverstone · Checklist · Recap · 14 exercises with worked answers · Key terms · Where this leads.

### Files
- `manuscript/ch45-data-ingestion-and-integration.md`
- `companion/ch45/`: `reset_ch45.py`, `apply_day.py`, `mock_crm_api.py`, `make_files.py` (generated `exports/` and `warehouse/` are recreated by reset; don't store them)
- `figures/make_figs45.py` (imports make_figs07.py) → fig45-1 … fig45-4
- `checks/ch45_check.py`
- PDF: `Ch45-Data-Ingestion-and-Integration.pdf` (34 pages)

### Verification
- `verify_python.py` (run with `PYTHONPATH=companion/ch45 … --cwd companion/ch45`): **21 blocks run, 21 outputs checked, 0 mismatches**. Three answer fragments marked `run: none` (exercise answers 5, 8, 10 reference the chapter namespace).
- `checks/ch45_check.py`: 10 checks pass (exercise 4 hash result after two unloaded days, date parsing, totals, backoff waits, lead count).
- Versions: Python 3.12.3, DuckDB 1.5.5, psycopg2 2.9.13, requests 2.33.1, PostgreSQL 16 with `wal_level = logical`.
- Figures rendered and inspected (column overflow in 45.3 and cut-off card in 45.4 fixed). Style: no em dashes in prose, banned words removed.
- **Note for the verifier tool owner:** `verify_python.py` doesn't put `--cwd` on `sys.path`; companion imports need `PYTHONPATH`. Suggest adding `sys.path.insert(0, os.getcwd())` after `os.chdir` (coordinator-owned file, not edited).

### Manual checks needed
- Section 45.6 setup steps (finding `postgresql.conf`, restart) vary by OS; tested only on Ubuntu 24.04.
- Managed connector and cloud warehouse mentions are conceptual (not executed).

### New Riverstone facts (proposed)
1. `riverstone_source` companion database and simulated ERP days 2 Jan 2026 (orders 10176–10177; 10175 → Delivered; 10174 → Cancelled) and 5 Jan 2026 (10176 → Shipped; order 10178, line 334).
2. Bhiwandi Main daily dispatch sheet format (dispatch IDs D-26xx, dd-mm-yyyy, qty_units), and the 5 Jan change (`units`, `vehicle_no`).
3. CRM REST API shape (bearer token, page_size 20, 429 with Retry-After) — practice stand-in.
4. Real-world story: first warehouse pipeline went live "in February" (year unstated) built by a contract data engineer with Meera as business owner; customer "Hotel Sai Palace" (new name); 214 stale orders found; nightly 90-day hash + Sunday full comparison; Flash held by reconciliation check. **Please check against Part II/III timelines (Ch 20 Flash automation).**

### Dependencies
- Ch 20 (analyst-level Flash automation) and Ch 32 (dbt) not yet written; references follow the blueprint. Check links when written.
- Ch 29 includes robust API clients; 45.9 refers back to it and applies the pattern to ingestion.

### Promises delivered
Ch 2: file change detection with hashes (45.5) and formats/APIs at scale · Ch 12: robust CSV loading and count comparison (45.3, 45.7).

### Promises made to later chapters
Ch 46: orchestration, deliberate-failure idempotency test, backfills, Flash sent only after checks · Ch 47: reconciliation as automated tests, slot-lag and freshness monitoring, data contracts · Ch 49: raw/staging storage, ACID, cloud warehouses · Ch 50: CDC as a continuous stream · Ch 51: writing back with idempotency, retries, system of record · Ch 52/64: secrets in production · Ch 64: privacy law behind 45.11 · Ch 77: system design questions (interview extra point).

---

## Chapter 46 report — Pipelines & Orchestration (v1, approved 17 Sep 2026)

**Approved by the author on 17 Sep 2026.** Approved PDF: `Ch46-Pipelines-and-Orchestration-v1-approved.pdf`. Coordinator to confirm the proposed ERP end-of-day close flag against Ch 3.

### Decision recorded
Orchestrator: **Dagster** as the main tool (author's choice, 16 Sep 2026), with an Airflow translation in 46.8.

### Contents
At a glance · Why · Plain English (kitchen) · 46.1 Cron vs orchestrator · 46.2 DAGs, tasks vs assets, cron expressions, time zones (IST/UTC trap), partitions · 46.3 Riverstone daily pipeline in Dagster (4 ingestion assets, daily_flash with partition overwrite, blocking check flash_matches_erp, deliver_flash with delivery log; job + schedule 30 6 * * * Asia/Kolkata; first run Rs 38,710.00; idempotent re-run) · 46.4 Failure test: append version doubles to Rs 77,420.00; transaction version stays Rs 38,710.00; idempotency patterns · 46.5 Backfill without delivery (outbox unchanged); late correction on order 10177 → Rs 40,110.00 and labeled correction file; look-back approaches · 46.6 Retries (real retry run), retries hiding bugs (true incident from building the chapter), timeouts, alerting, run_failure_sensor (not executed) · 46.7 Bad morning on 5 Jan: silent empty order-line load + dispatch schema change; check blocks delivery; actionable alert; fix (confirmed rename) and re-run delivers Rs 18,750.00; pre-delivery checks table; write-audit-publish pointer · 46.8 Airflow 2 TaskFlow version (not executed), concept mapping, logical-date trap · 46.9 Choosing an orchestrator · 46.10 Operating pipelines (owner, SLA, runbooks) · Common mistakes (14) · Real world: *The Flash that went out twice* · Tools · Project · Checklist · Recap · 14 exercises with answers · Key terms · Where this leads.

### Files
- `manuscript/ch46-pipelines-and-orchestration.md`
- `companion/ch46/`: `reset_ch46.py`, `ingest.py` (sync_table, load_dispatch with column check and CONFIRMED_RENAMES, fetch_leads), plus `apply_day.py`, `make_files.py`, `mock_crm_api.py` copied from ch45
- `figures/make_figs46.py` (imports make_figs07.py) → fig46-1 … fig46-4
- `checks/ch46_check.py` (12 checks: Flash revenues from order lines, doubling, exercise 4, time-zone conversions, weekday)
- PDF: `Ch46-Pipelines-and-Orchestration.pdf`

### Verification
- `verify_python.py` with `PYTHONPATH=companion/ch46 --cwd companion/ch46`: **14 blocks run, 14 outputs checked, 0 mismatches**. Blocks marked `run: none`: run_failure_sensor, Airflow DAG, exercise 5 answer.
- Deterministic output: step messages collected in a run log and printed in pipeline order (Dagster may execute independent steps in any order).
- `checks/ch46_check.py`: all pass. Figures rendered and inspected; PDF spot-checked.
- Versions: Python 3.12.3, Dagster 1.13.23, DuckDB 1.5.5, psycopg2 2.9.13, requests 2.33.1, PostgreSQL 16.

### Manual checks needed
- Airflow code (46.8, exercise 12 answer) not executed: follows Airflow 2 TaskFlow API; check against the version readers use (Airflow 3 changed details).
- `run_failure_sensor`, `dagster dev`, `dagster job backfill`, and the `dagster/max_runtime` tag need a deployed Dagster instance; not executed.

### New Riverstone facts (proposed)
1. Daily Sales Flash pipeline scheduled 06:30 IST; SLA "delivered by 7:00 a.m. IST on working days".
2. Simulated 5 Jan 2026: Bhiwandi Main confirms `units` = `qty_units`; correction on 6 Jan to order 10177 (6 → 7 crates, line 333).
3. Story (two months after go-live): duplicate Flash emails (Rs 3,12,400 vs Rs 3,24,900) from an automatic retry; fixes: delivery log with content hash, CORRECTION subject line, ERP end-of-day close flag as readiness condition, retry notices in the data team channel. **New fact: the ERP has an end-of-day close flag** — coordinator to confirm with Ch 3.

### Promises delivered
Ch 45 → Ch 46: orchestration, deliberate-failure idempotency test, backfills, Flash sent only after checks. Brief: full Dagster example; triggering downstream delivery only after checks; automation thread (Ch 20 script → orchestrated pipeline).

### Promises made to later chapters
Ch 47: write-audit-publish, freshness/volume/validity checks, alert fatigue · Ch 48: heavy steps inside pipelines · Ch 49: ACID behind partition overwrites · Ch 50: continuous pipelines · Ch 51: CRM/ERP syncs gated by checks, idempotency keys · Ch 52: deploying pipelines, secrets · Ch 63: company-wide orchestration governance · Ch 77: pipeline design interview questions.

---

## Chapter 47 report — Data Quality, Observability & Contracts (v1, approved 17 Sep 2026)

**Approved by the author on 17 Sep 2026.** Approved PDF: `Ch47-Data-Quality-Observability-and-Contracts-v1-approved.pdf`.

### Decision recorded
Quality tooling for runnable code: **plain SQL tests run from Python** (author's choice, 17 Sep 2026), with dbt test YAML shown (not executed) and Great Expectations / Soda / observability platforms compared in 47.10.

### Contents
At a glance · Why (closes the Ch 46 gap: wrong row left visible) · Plain English (factory quality department) · 47.1 Six dimensions with Riverstone examples · 47.2 A data test = a query returning failing rows; severity; where checks belong · 47.3 15-line test framework + 7-test library, all passing; failures demonstrated (ERP foreign key refuses the orphan line, so the warehouse is broken instead); re-sync self-heals; same tests as dbt YAML (not executed) · 47.4 Write-audit-publish, with the 5 Jan failure now leaving mart.daily_flash untouched; variations; "missing day looks like a zero day" warning · 47.5 Freshness (real ages: orders 30.5 h, dispatch and Flash 102.5 h) and volume/anomaly on 2025 data (131 days with orders, median Rs 27,442.50, 10 days above 3x, max Rs 175,895.00); "unusual is not wrong" · 47.6 Lineage and impact analysis · 47.7 Data contract for the dispatch sheet, checked automatically (Jan 5 file: 3 violations); working with producers · 47.8 Incident flow, S1-S3 severities, containment message · 47.9 One incident, one alert; grouped alert built from test results, freshness and contract failures; anti-fatigue rules · 47.10 Tools landscape · Common mistakes (15) · Real world: *The dashboard that was right but late* · Tools · Project · Checklist · Recap · 14 exercises with answers · Key terms · Where this leads.

### Files
- `manuscript/ch47-data-quality-observability-and-contracts.md`
- `companion/ch47/`: `reset_ch47.py` plus `ingest.py`, `apply_day.py`, `make_files.py`, `mock_crm_api.py` (Ch 46 environment)
- `figures/make_figs47.py` (imports make_figs07.py) → fig47-1 … fig47-4
- `checks/ch47_check.py`
- PDF: `Ch47-Data-Quality-Observability-and-Contracts.pdf`

### Verification
- `verify_python.py` with `PYTHONPATH=companion/ch47 --cwd companion/ch47`: **12 blocks run, 12 outputs checked, 0 mismatches**. Non-Python blocks (dbt YAML, SQL answer) carry no run marker; the Python answer block is marked `run: none`.
- `checks/ch47_check.py`: 11 checks pass (load counts, 2025 median and anomaly counts, freshness arithmetic, exercise 9 thresholds, 2 Jan revenue).
- Figures rendered and inspected (label and overflow fixes applied). Style checks clean.
- Versions: Python 3.12.3, DuckDB 1.5.5, psycopg2 2.9.13, PostgreSQL 16.

### Tooling note for the coordinator (important)
`tools/verify_python.py` (and my fill helper) treat `<!-- run: none -->` as a flag that is only cleared by the next **Python** block. If a `run: none` marker precedes a non-Python block (yaml, sql), the flag stays set and the **next Python block is silently skipped** — it is neither run nor checked. Found while writing this chapter; the Ch 47 manuscript avoids it by not marking non-Python blocks. Suggested fix in the tool: clear the skip flag on any fenced block, not only Python ones. Chapters 45 and 46 were re-checked and are not affected.

### Manual checks needed
- dbt test YAML (47.3) and the tool comparisons in 47.10 are not executed.
- Freshness examples use a fixed clock (`NOW = 2026-01-06 06:30`) so outputs are deterministic.

### New Riverstone facts (proposed)
1. Dispatch data contract terms: file `dispatch_YYYY-MM-DD.csv` by 20:00 IST on working days, 10 working days' notice for renames/removals, owner = Bhiwandi Main warehouse supervisor.
2. Severity scale S1–S3 for Riverstone data incidents; on-call data team; runbook path `docs/runbooks/daily_flash.md`.
3. Story: sales dashboard stale for three days after an internal column rename; fixes = freshness checks on read tables, alert cleanup (successes off, warnings to a weekly digest), a "data current to…" banner driven by a load-status table, and internal contracts for shared models. Two further reports named in the lineage example: `dispatch_report`, `weekly_pipeline_report`.

### Promises delivered
Ch 1: data teams catch data problems automatically · Ch 13: checking habits become automated tests · Ch 45: data contracts in practice · Ch 46: write-audit-publish, freshness monitoring, alert fatigue.

### Promises made to later chapters
Ch 48: tests at scale · Ch 49: snapshots/time travel for publish and rollback · Ch 50: checking continuous data · Ch 51: S1 incidents when wrong data reaches business systems · Ch 32: dbt tests and contracts · Ch 64: ownership and governance · Ch 77: "walk me through a wrong dashboard".

---

## Chapter 48 report — Big Data & Distributed Compute (v1, approved 18 Sep 2026)

**Approved by the author on 18 Sep 2026** (length accepted as is; the 'Imran Shaikh' supervisor name was not changed — coordinator may still rename it). Approved PDF: `Ch48-Big-Data-and-Distributed-Compute-v1-approved.pdf`. **Timings must be re-measured on a multi-core machine before publication.**

### Decisions recorded
Practice dataset size: **~20 million readings** (author's choice, 18 Sep 2026) — 25 machines x 92 days x 8,640 readings = **19,872,000**, 114 MB Parquet partitioned by reading_date. PySpark in local mode is the main tool, with DuckDB and Polars for comparison.

### Contents
At a glance · Why · Plain English (counting votes) · 48.1 Most big data isn't; size table; four questions · 48.2 Partitions, workers, driver, narrow vs wide, lazy execution · 48.3 PySpark on the sensor data (19,872,000 rows; scrap by plant and line type; lazy execution with 8,143,256 readings above 200 C) · 48.4 Reading a physical plan and finding the Exchange · 48.5 Partition pruning (92 folders to 1; 129,600 rows), pushed filters, SortMergeJoin vs BroadcastHashJoin, skew and salting (outline, not executed) · 48.6 Same question in DuckDB, Polars and Spark: identical answers, measured timings · 48.7 collect(), small files, caching, UDFs, testing on one partition · 48.8 Landscape (Databricks, EMR, Dataproc, Fabric, Trino, Ray, Hadoop, warehouses) · Common mistakes (12) · Real world: *The cluster that was slower than the laptop* · Tools · Project · Checklist · Recap · 14 exercises with answers · Key terms · Where this leads.

### Length
~7,700 words. Shorter than Ch 45-47 (10-12k) because the teaching load sits in plans and measured comparisons rather than prose; blueprint target was 4,500. Say if you want it expanded — the obvious additions are a worked skew demonstration and a Spark Structured Streaming preview (currently left to Ch 50).

### Files
- `manuscript/ch48-big-data-and-distributed-compute.md`
- `companion/ch48/`: `make_sensor_data.py` (generator; `--small` for one day), `time_three_tools.py` (timing script). Generated `sensor_readings/` folders are NOT stored — readers generate them (2-4 min).
- `figures/make_figs48.py` (imports make_figs07.py) → fig48-1, fig48-2
- `checks/ch48_check.py`
- PDF: `Ch48-Big-Data-and-Distributed-Compute.pdf`

### Verification
- `verify_python.py --cwd companion/ch48`: **9 blocks run, 9 outputs checked, 0 mismatches**. Spark plans are made reproducible by a `plan()` helper that strips attribute ids, plan ids and the absolute file path — worth keeping for Ch 50.
- `checks/ch48_check.py`: 8 checks pass (row counts, 200 C count, pruned-day count, aggregate values, timing ratios in exercise 8).
- Figures rendered and inspected; monospace plan lines use non-breaking spaces so indentation survives SVG rendering.
- Versions: Python 3.12.3, PySpark 4.2.0, DuckDB 1.5.5, Polars 1.44.2, PyArrow 25.0.1, Java 21, PostgreSQL not needed.

### Measured, not reproducible (stated in the chapter)
Timings in 48.6 were measured on the writing container: **1 CPU core, 3 GB RAM**. 216,000 rows: DuckDB 0.01 s, Polars 0.00 s, Spark 0.73 s. 19,872,000 rows: DuckDB 0.38 s, Polars 0.47 s, Spark 2.01 s (fastest of three runs). The chapter states the hardware, explains that one core gives Spark nowhere to parallelize, and tells readers to run `time_three_tools.py` themselves. **Re-measure on a multi-core machine before publication** and update the table and exercise 8.

### Manual checks needed
- Salting outline (48.5), exercise answers 4, 9 (`coalesce`) marked `run: none`.
- Spark UI (localhost:4040) references not executed.

### New Riverstone facts (proposed)
1. Sensor dataset shape: 25 machines (M-01..M-25), 15 at Bhiwandi Main and 10 at Chakan Pune, line types Injection/Extrusion/Blow, one reading per 10 seconds, Oct-Dec 2025; fields machine_id, plant, line_type, reading_ts, temperature_c, pressure_bar, units_made, scrap_flag.
2. Three machine supervisors named in the join example: Anil Deshmukh (M-01), Sunita Rao (M-02), Imran Shaikh (M-03). **Imran Shaikh** reuses the name of the sales-ops Imran from Ch 1 — coordinator may want a different name here.
3. Story: a contractor built a Spark cluster for a weekly plant report (26 minutes) because the archive was partitioned by machine, not date; rewritten by date, the report runs in under a minute in DuckDB; Spark kept for the yearly full-archive rebuild. Archive size stated as ~300 million readings.

### Promises made to later chapters
Ch 49: partitioning, file sizes, table formats, small-files problem, cloud warehouse costs · Ch 50: same sensor data as a stream, Structured Streaming · Ch 52: running Spark off the laptop and what it costs · Ch 56: distributed training and feature pipelines · Ch 77: "how would you process X" design cases.

---

## Chapter 49 report — Storage, Warehouses & Lakehouses (v1, approved 18 Sep 2026)

**Approved by the author on 18 Sep 2026.** Approved PDF: `Ch49-Storage-Warehouses-and-Lakehouses-v1-approved.pdf`. **Cloud prices in 49.8 must be re-checked and dated before publication.**

### Decision recorded
Table format for the hands-on part: **Delta Lake via `deltalake` (delta-rs)** — author's choice, 18 Sep 2026. No Spark or JVM needed. Iceberg and Hudi covered by comparison (49.5, 49.6, exercise 12).

### Contents
At a glance · Why · Plain English (warehouse stock register) · 49.1 Where data sits (files, object storage, database, warehouse, lake, lakehouse) · 49.2 Row vs columnar measured: same day as CSV 14.6 MB, SQLite 16.3 MB, Parquet 1.3 MB, all three giving 196.49 C · 49.3 Inside a Parquet file: 2 row groups, per-column compressed sizes and min/max statistics (plant 0.1 KB vs temperature_c 219.4 KB) · 49.4 ACID properly, and what plain files lack · 49.5 Delta hands-on: create (v0, 1 file), read the log actions, atomic predicate overwrite correcting M-07 (196.0 → 197.5 C, still 216,000 rows, v1), time travel, schema merge (new `shift` column, 8,640 rows), compaction (24 files @114 KB → 1 file @529 KB) · 49.6 Partitioning and file sizing rules; hidden partitioning and liquid clustering · 49.7 Warehouses: storage/compute separation, tuning table · 49.8 Cost: four components plus a worked Riverstone estimate (277 GB/year, ~$6.40/month storage; weekly report $0.027 vs $1.39 a run) · 49.9 Choosing a layout · Common mistakes (11) · Real world: *The table nobody could fix* · Tools · Project · Checklist · Recap · 14 exercises with answers · Key terms · Where this leads. Draft's broken "Chapter 2" reference is gone: 49.2 now carries the row-vs-columnar demonstration itself.

### Files
- `manuscript/ch49-storage-warehouses-and-lakehouses.md`
- `companion/ch49/setup_ch49.py` (builds storage/day.csv, day.parquet, day.sqlite from the Ch 48 data; set CH48_SENSORS if the path differs)
- `figures/make_figs49.py` (imports make_figs07.py) → fig49-1, fig49-2
- `checks/ch49_check.py`
- PDF: `Ch49-Storage-Warehouses-and-Lakehouses.pdf` (22 pages)

### Verification
- `verify_python.py --cwd companion/ch49` with PYTHONPATH: **9 blocks run, 9 outputs checked, 0 mismatches**.
- `checks/ch49_check.py`: 13 checks pass (file sizes, ratios in exercise 2, cost arithmetic in 49.8 and exercise 9).
- Figures rendered and inspected; PDF built.
- Versions: Python 3.12.3, deltalake 1.6.3, DuckDB 1.5.5, PyArrow 25.0.1.
- API note for later chapters: `deltalake` 1.6 has `file_uris()` (not `files()`), `.arrow()` results must be `read_all()`-ed before counting, and DuckDB's `delta_scan` needs an extension download, so the chapter registers `to_pyarrow_dataset()` with DuckDB instead.

### Length
~7,700 words (blueprint target 5,000). Same shape as Ch 48: dense code and measured outputs rather than long prose.

### Manual checks needed
- Cloud prices in 49.8 are illustrative list prices ($0.023/GB-month storage, $5/TB scanned, ₹83/$). **Re-check before publication** and mark as of a date.
- Warehouse comparison table (49.7) and Iceberg/Hudi comparisons are descriptive, not executed.

### New Riverstone facts (proposed)
1. Sensor archive is kept as a Delta table in object storage, partitioned by reading_date, compacted weekly, one year of time travel; orders stay in the warehouse.
2. Machine M-07's temperature probe read 1.5 C low and was corrected (used in 49.5 and the story).
3. Story: a six-week correction to M-07 failed mid-run under plain Parquet, leaving 11 days corrected, 8 days missing and 23 unchanged; recovery took two days via object-storage versioning; the archive was then moved to Delta.

### Promises delivered
Ch 46: partition overwrite that is genuinely atomic · Ch 47: rollback by restoring a version · Ch 48: file sizing and the small files problem.

### Promises made to later chapters
Ch 50: streaming writes, compaction pressure · Ch 51: reading published tables · Ch 52: object storage, permissions, cost management · Ch 62/63: platform economics and architecture · Ch 77: storage layout design cases.

---

## Chapter 50 report — Streaming & Real-Time (v1, approved 18 Sep 2026)

**Approved by the author on 18 Sep 2026**, including the mini-log approach to Kafka. If a broker-backed environment becomes available, sections 50.2-50.3 can be re-done against it. Approved PDF: `Ch50-Streaming-and-Real-Time-v1-approved.pdf`.

### Constraint and decision (please note)
**A Kafka broker cannot be installed in the book's practice environment** (no access to Apache download servers; no container runtime). The blueprint asks for "a working Kafka producer/consumer example". Delivered as: (a) `companion/ch50/mini_log.py`, an 80-line append-only log implementing Kafka's core ideas — topics, partitions, key-based routing, offsets, consumer groups, committed offsets, at-least-once — which runs and is fully verified; plus (b) real `kafka-python` producer and consumer code in 50.3, marked `run: none`, with the settings that matter (acks, enable_idempotence, auto_offset_reset, manual commit). The chapter states this openly in a note at the top. **If you want genuine broker-backed examples, that needs an environment with Docker or a managed Kafka, and I'd re-do 50.2-50.3 against it.**

### Contents
At a glance (with the Kafka note) · Why · Plain English (restaurant order spike) · 50.1 What real-time means: latency table and three questions · 50.2 Topics, partitions, keys, offsets, groups, lag, retention; 300 events split 144/156, M-07 always partition 1; consume and commit · 50.3 At-most/at-least/exactly-once; crash before commit re-sends all 82 alerts; de-duplication key fixes it; real Kafka client code (not executed) · 50.4 Structured Streaming: declared schema, file source, triggers, checkpoints · 50.5 Event vs processing time, tumbling windows, watermarks; first batch emits nothing (append mode); late data counted (456 vs 450) then dropped once the watermark passes; progress metrics (1 state row dropped from 6 events) · 50.6 Streaming into a table: 9 sink files → 4 Delta files → 1 after compaction · 50.7 Operating a stream: lag, watermark age, drops, state size, dead-letter, schema registry · 50.8 Riverstone plant monitoring case, including when not to build it · Common mistakes (13) · Real world: *The alert that cried wolf* (1,900 alerts in two days → 11) · Tools · Project · Checklist · Recap · 14 exercises with answers · Key terms · Where this leads.

### Files
- `manuscript/ch50-streaming-and-real-time.md`
- `companion/ch50/`: `mini_log.py`, `sensor_events.py` (replays the Ch 48 archive as events, including late ones)
- `figures/make_figs50.py` (imports make_figs07.py) → fig50-1, fig50-2
- `checks/ch50_check.py`
- PDF: `Ch50-Streaming-and-Real-Time.pdf` (23 pages)

### Verification
- `verify_python.py --cwd companion/ch50` with PYTHONPATH: **9 blocks run, 9 outputs checked, 0 mismatches**. Deterministic by design: `trigger(availableNow=True)`, fixed input batches, and only counts/watermarks printed from progress metrics (no durations or timestamps of the run).
- `checks/ch50_check.py`: 13 checks pass (batch sizes, partition split, 82 hot readings, late-event counts, watermark arithmetic for exercise 7, files-per-day for exercise 9).
- Figures rendered and inspected (overlap and spacing fixed). Versions: Python 3.12.3, PySpark 4.2.0, deltalake 1.6.3, Java 21.

### Manual checks needed
- Kafka client code (50.3) not executed; check against the `kafka-python` version readers use.
- Managed-service names in Tools (MSK, Confluent Cloud, Event Hubs, Pub/Sub) and Flink/Kafka Streams mentions are descriptive.

### New Riverstone facts (proposed)
1. Plant monitoring design (50.8): machine controllers publish a reading every 10 seconds to a `sensor-readings` topic keyed by machine; alerting consumer with 2-minute windows and per-machine limits owned by the plant team; 5-minute/10-minute-watermark aggregation into the Ch 49 Delta table; daily batch correction path.
2. Story: the first alerting release sent 1,900 messages in two days and was muted; fixes were 2-minute windows, de-duplication by machine+window with 30-minute suppression, and per-machine limits; the same period would then have produced 11 alerts, one catching a failing heater.

### Promises delivered
Ch 48: same sensor data as a stream · Ch 49: streaming writes and compaction pressure · Ch 45: CDC as a continuous stream (referenced).

### Promises made to later chapters
Ch 51: at-least-once becomes idempotency keys against CRM/ERP · Ch 52: running a stream that stays up, secrets, cost · Ch 47: freshness on the streaming sink, alert fatigue · Ch 58: the alerting decision with AI in the loop · Ch 77: "design a real-time alerting system".

---

## Chapter 52 report — The Cloud, Containers & Infrastructure as Code (v1, approved 19 Sep 2026)

**Approved by the author on 19 Sep 2026,** including the shown-and-validated-not-executed approach to Docker/Kubernetes/Terraform/cloud. Approved PDF: `Ch52-The-Cloud-Containers-and-Infrastructure-as-Code-v1-approved.pdf`. If an environment with real cloud/Docker credentials becomes available, the coordinator may wish to re-verify 52.2-52.5 against live infrastructure before final publication.

### Constraint and approach (please read)
**No Docker daemon, Kubernetes cluster, Terraform provider registry, or cloud account is reachable from this sandbox** (confirmed: no `docker`/`kubectl`/`terraform` binaries; Docker Hub, the Terraform registry, and every cloud API are outside the allowed network domains even if the binaries existed). Author was informed of this before starting and said to proceed. Handled as follows, stated openly in the chapter's own opening note:
- **Really executed and verified:** the Dockerfile (parsed with `dockerfile-parse`: base image, 6 layers, non-root user confirmed), the docker-compose file (parsed as YAML, service dependency confirmed), the Kubernetes manifest (parsed as YAML, both documents, replicas, resource requests/limits, secret references all confirmed), the Terraform configuration (parsed with a real HCL parser: 5 resources, IAM role and policy all confirmed), the GitHub Actions workflow's **trigger and `if` logic**, simulated in Python against the real YAML for three real event/branch combinations, all real CIDR/subnetting arithmetic (65,536 addresses, 256 /24 subnets, 251 usable hosts), and the full cost model (24.3x always-on vs scheduled, $7.09/month total).
- **Explicitly marked as not executed:** an actual `docker build`, `kubectl apply`, `terraform apply`, and a real GitHub Actions run of the build/push/deploy jobs. This mirrors the precedent already set in Ch 46 (Airflow) and Ch 50 (Kafka).

### Contents
At a glance (with the execution note) · Why · Plain English (a second warehouse) · 52.1 Regions/AZs, shared responsibility, IAM/least privilege, VPC/subnet/security-group design with real CIDR math (fig 52.1, fig 52.2) · 52.2 Containers: why they exist, a full Dockerfile for the Ch46 pipeline built and explained line by line (fig 52.3), validated with a real parser, Docker Compose for local dev · 52.3 Kubernetes: Pod/Deployment/Service/Secret/Namespace table, a full manifest for the pipeline, validated, "when you don't need it" · 52.4 Terraform: a complete configuration for the Ch49 sensor archive's S3 bucket + versioning + lifecycle + least-privilege IAM role, validated with python-hcl2, plan/apply/state discipline · 52.5 CI/CD: a full GitHub Actions workflow, its trigger logic simulated for real across 3 event/branch combinations · 52.6 Secrets at every layer (table) · 52.7 Cost: compute added to Ch49's storage estimate, real always-on-vs-scheduled arithmetic · 52.8 Choosing a deployment target · Common mistakes (11) · Real world: *The afternoon the warehouse went dark* (a Terraform security-group removal breaking pipeline-to-database connectivity) · Tools · Project · Checklist · Recap · 14 exercises with worked answers · Key terms · Where this leads.

### Files
- `manuscript/ch52-the-cloud-containers-and-infrastructure-as-code.md`
- `companion/ch52/`: `pipeline_image/` (Dockerfile, requirements.txt, docker-compose.yml), `k8s/pipeline-deployment.yaml`, `terraform/main.tf`, `.github_workflows/deploy.yml`, `simulate_workflow.py`, `networking_math.py`, `cost_estimate.py`
- `figures/make_figs52.py` (imports make_figs07.py) → fig52-1 (shared responsibility), fig52-2 (VPC/subnets), fig52-3 (Dockerfile layers)
- `checks/ch52_check.py`
- PDF: `Ch52-The-Cloud-Containers-and-Infrastructure-as-Code.pdf` (29 pages)

### Verification
- `verify_python.py --cwd companion/ch52` with PYTHONPATH: **7 blocks run, 7 outputs checked, 0 mismatches**. No PostgreSQL dependency in this chapter at all.
- `checks/ch52_check.py`: **25 checks pass**, covering the Dockerfile/compose/k8s/Terraform parses, all CIDR arithmetic, the full cost model, and all three workflow-trigger simulations (including both exercise-5 cases).
- **One real bug caught and fixed while building the VPC figure:** my first diagram used `"A" in az_name` to distinguish availability zone A from zone B, but the string "Availability zone B" also contains the letter "A" (from "Availability" itself), so both zones rendered identical CIDRs. Fixed by passing an explicit zone-letter parameter instead of substring-matching the label. Caught by visually reviewing the rendered figure before shipping, not by any automated check, flagging this as a reminder that figures need the same scrutiny as code output.
- Style: matched house convention exactly (em dashes only in the Part-title line and figure captions, confirmed by grep after the fact); one flagged word ("silently" reads fine per house usage in other chapters, but I found and fixed an unrelated stray "honestly").
- Versions: Python 3.12.3, PyYAML 6.0.3, python-hcl2, dockerfile-parse. No Java/Spark/Delta/Dagster dependency.

### Manual checks needed (cannot be resolved without real infrastructure)
- An actual `docker build` of `pipeline_image/Dockerfile` (needs a container runtime and network access to Docker Hub).
- An actual `terraform plan`/`apply` of `terraform/main.tf` against a real AWS account.
- An actual `kubectl apply` of `k8s/pipeline-deployment.yaml` against a real or local cluster.
- An actual run of `.github_workflows/deploy.yml`'s `build-and-push` and `deploy` jobs in a real GitHub repository.
- Current AWS pricing referenced in 52.7 (compute $/vCPU-hour and $/GB-hour figures are illustrative, consistent with Ch49's storage figures) — **re-check before publication, same flag as Ch49**.
- **Recommend:** if a future session has real cloud credentials or a Docker-capable environment, re-run and re-verify this chapter's infrastructure blocks against real services before final publication, upgrading them from "validated" to "executed".

### New Riverstone facts (proposed)
1. The pipeline is packaged as `riverstone/pipeline`, versioned by tag (e.g. `1.4.0`, or by commit SHA in CI), deployed via a Dockerfile built from `python:3.12-slim`.
2. Riverstone's cloud region is `ap-south-1` (Mumbai) — first explicit statement of a specific AWS region in the book; ties to the still-open cloud-provider decision.
3. Story: a contract data engineer's Terraform cleanup removed a security-group rule that had only ever existed via manual console changes (never in code), breaking pipeline-to-database connectivity for an afternoon; fixed by importing all existing resources into Terraform, requiring full plan output in PR review, and adding a synthetic connectivity health check.

### Promises delivered
Ch 45's "tokens don't belong in code" extended to a full per-layer secrets table (52.6) · Ch 46's pipeline given an actual deployment target · Ch 47's incident process (detect/classify/contain/fix/review) applied to a leaked-secret scenario · Ch 49's storage-cost estimate extended to include compute, and its bucket versioning/lifecycle shown as Terraform · Ch 51's CRM token given a concrete home in the deployment (52.6).

### Promises made to later chapters
Ch 62/65: FinOps and platform economics, referenced but not duplicated · Ch 63: deployment-target choice at whole-company scale · Ch 64: shared responsibility and least privilege as governance foundations · Ch 77: deployment/system-design interview cases.

### Decision this chapter needed from the author (resolved)
Whether to proceed on this sandbox's shown-and-validated-not-executed basis, or wait for an environment with real cloud/Docker credentials. **Author chose to proceed now** (this turn). Recommend flagging for a future editorial pass with real infrastructure access, per "Manual checks needed" above.

## Part V is now complete and fully approved
All 8 chapters (45-52) have manuscripts, companion code, figures, checks, and PDFs, and all 8 are author-approved as of 19 Sep 2026. This status file should be handed to the coordinator alongside the chapter map for final sign-off, and the chapter-map / progress-tracker updated to mark P5-45 through P5-52 approved.

## Open decisions
- **Cloud provider** for hands-on examples (default: provider-neutral concepts; AWS unless targeting Microsoft-heavy employers). Needed before Chapter 52.

---

## Chapter 51 report — Data Activation: Reverse ETL, APIs & System Integration (v1, approved 19 Sep 2026)

**Approved by the author on 19 Sep 2026.** Approved PDF: `Ch51-Data-Activation-v1-approved.pdf`.

### Contents
At a glance · Why · Plain English (factory whiteboard) · 51.1 The full loop, and where most companies stop · 51.2 Computing lead scores (43 leads, fully worked, hand-checked) and overdue-payment flags (4 customers in a 45-75 day aging bucket, explicitly labeled as a placeholder for a real AR feed) · 51.3 Writing through APIs: OAuth vs the sandbox's bearer token; sandbox setup; first sync of 6 leads · 51.4 Idempotency: a genuine 503-then-retry on a brand-new lead (7), and a genuine replay on an already-synced lead (4), both with real CRM responses · 51.5 System of record and conflict rules · 51.6 Webhooks: registering a hook, creating a high-value lead, measuring real delivery time to a local inbox · 51.7 Write reconciliation (catches a deliberately introduced mismatch on lead 4) and audit trails · 51.8 Integration patterns (point-to-point, hub-and-spoke, queue, iPaaS) · 51.9 Build vs buy for integration · 51.10 RPA and file-based integration (SFTP, EDI) · Common mistakes (11) · Real world: *The sync that erased a discount* · Tools · Project · Checklist · Recap · 14 exercises with worked answers · Key terms · Where this leads.

### Length
~8,400 words including code and answers. Below the blueprint's 5,500-word target's usual 2x expansion but consistent with Ch45-50's density (code-heavy, fewer long prose asides).

### Files
- `manuscript/ch51-data-activation.md`
- `companion/ch51/`: `reset_ch51.py`, `crm_sandbox.py` (sandbox CRM with PATCH/POST, idempotency-key caching, one-shot 503 simulation, webhook firing), `webhook_receiver.py` (local inbox), `sync_leads.py` (lead scoring + overdue-flag logic, fully documented rules)
- `figures/make_figs51.py` (imports make_figs07.py) → fig51-1, fig51-2
- `checks/ch51_check.py`
- PDF: `Ch51-Data-Activation.pdf` (23 pages)

### Verification
- `verify_python.py --cwd companion/ch51` with PYTHONPATH: **8 blocks run, 8 outputs checked, 0 mismatches**.
- `checks/ch51_check.py`: 8 checks pass (lead counts, specific lead scores including the Won-capped-at-100 case, the overdue bucket's exact 4 customer ids, and the exercise 4 hand-computation).
- **One real bug caught and fixed during drafting:** my first prose pass claimed lead 2's source was "Referral" and flagged a fake discrepancy as a teaching moment. The real source (checked against the database) is "Website" (55 + 10 = 65), which matches the code's output exactly with no discrepancy. Rewrote that passage to walk the correct, matching arithmetic instead of a fabricated inconsistency — flagging this here in case it reveals a wider habit worth watching for.
- **Style pass:** found and removed an em-dash drift (25+ instances in prose, versus 3-5 in Ch45-47) and a few flagged filler words before finalizing; the chapter now matches the established house style (em dashes only in the Part-title line and Figure captions).
- Figures rendered and inspected (fig51-1's return-loop arrow was redrawn after the first pass overlapped the row). PDF reviewed page by page.
- Versions: Python 3.12.3, requests 2.33.1, PostgreSQL 16. No Spark/Dagster/Delta dependency in this chapter.

### Manual checks needed
- None outstanding. All runnable code was executed against the sandbox CRM; no blocks were marked `run: none` except two short illustrative exercise-answer snippets (exercise 6's key function, explicitly a sketch).

### New Riverstone facts (proposed)
1. Lead-scoring rule (stage + source + 14-day recency bonus, capped at 100) and the specific point tables, used as the canon scoring logic for any later chapter touching lead prioritization.
2. Overdue-payment approximation (45-75 day aging bucket on most-recent Delivered order), **explicitly labeled in-chapter as a placeholder for finance's real AR data** — recommend NOT treating this as canon for a future chapter that gets real invoice data; flagging for the coordinator to note if/when a payments table is ever added to the schema.
3. Sandbox CRM behavior (idempotency-key caching, PATCH semantics, webhook-on-high-value-lead) as a reusable pattern for Ch 52 if a deployed version of this sync is shown.
4. Story: a second, earlier reverse-ETL sync (built by "a different contractor" six weeks prior) used `PUT` instead of `PATCH` and erased a negotiated discount field; fixed by moving every sync to explicit `PATCH`, naming a system of record per field, and adding reconciliation to the segment sync.

### Promises delivered
Ch 7's "process automation and integration" and "reorder flags" mentions given full treatment · Ch 45's idempotency and API patterns extended to writes · Ch 46's gating-before-delivery pattern applied to syncs · Ch 47's reconciliation and audit-trail habits applied to writes · Ch 50's at-least-once vocabulary reused for webhooks · the blueprint's exact project (nightly idempotent CRM sync + reconciliation + sub-minute webhook) delivered as specified.

### Promises made to later chapters
Ch 52: deploying this sync (secrets for the CRM token, containers, scheduled infrastructure) · Ch 58: AI-driven actions on top of the activation layer, same idempotency/system-of-record discipline · Ch 63: integration patterns at whole-company scale · Ch 77: system design cases built on this loop.

## Open decisions carried forward
- **Cloud provider** for Ch 52: still open (see Ch 45's original flag). My recommendation stands: provider-neutral concepts with AWS as the primary named example. Ch 52 cannot execute any code in this sandbox (no cloud access) — everything there will be shown and explained, not run and verified, unless done in an environment with real cloud credentials.
