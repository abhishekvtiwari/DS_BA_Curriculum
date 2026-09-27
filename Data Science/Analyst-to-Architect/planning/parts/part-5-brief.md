# Part Brief — Part V — Data Engineering, Integration & Scale

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-5-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 45–52**.

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P5-45 | 45 | Data Ingestion & Integration | B | 4,000 | Not started | `manuscript/ch45-data-ingestion-and-integration.md` |
| P5-46 | 46 | Pipelines & Orchestration | B | 4,500 | Not started | `manuscript/ch46-pipelines-and-orchestration.md` |
| P5-47 | 47 | Data Quality, Observability & Contracts | B | 3,500 | Not started | `manuscript/ch47-data-quality-observability-and-contracts.md` |
| P5-48 | 48 | Big Data & Distributed Compute | B | 4,500 | Not started | `manuscript/ch48-big-data-and-distributed-compute.md` |
| P5-49 | 49 | Storage, Warehouses & Lakehouses | B | 5,000 | Not started | `manuscript/ch49-storage-warehouses-and-lakehouses.md` |
| P5-50 | 50 | Streaming & Real-Time | B | 4,500 | Not started | `manuscript/ch50-streaming-and-real-time.md` |
| P5-51 | 51 | Data Activation: Reverse ETL, APIs & System Integration | B | 5,500 | Not started | `manuscript/ch51-data-activation-reverse-etl-apis-and-system-integration.md` |
| P5-52 | 52 | The Cloud, Containers & Infrastructure as Code | B | 5,500 | Not started | `manuscript/ch52-the-cloud-containers-and-infrastructure-as-code.md` |

## Reference chapters for this part

Chapter 13 (class B) and Chapter 2 (formats, APIs, measured tests).

## Guidance specific to this part

- **Assumes Parts II–III.** Chapter 2 introduced formats, compression, the cloud, APIs, and hashes: build on those sections directly.
- **Runnable locally wherever possible:** DuckDB, PostgreSQL, Python, Parquet, a local orchestrator (for example Dagster or Airflow in a local mode), Spark in local mode, a local Kafka-compatible broker if feasible. Where a managed cloud service is needed, show the concept provider-neutrally and label code that wasn't executed; list it under "Manual checks needed".
- **Cloud provider is an open decision** (instructions, section 2). Use the default and flag it before writing Chapter 52.
- **Promises to deliver:** Chapter 45 change detection with hashes and robust CSV/Parquet loading (Chapter 2, Chapter 12 project); Chapter 47 turning Chapter 13's data-quality checks into automated tests; Chapter 49 ACID properly (Chapter 12 transactions); Chapter 51 system integration, reverse ETL, and APIs (Chapter 2).
- **Automation thread:** this part connects analyst-level automation (Chapter 20) to production pipelines; show the same Riverstone daily report evolving into an orchestrated, tested, monitored pipeline.

## Sequencing and dependencies

Start after Part III Chapter 32 (dbt) is written, or in parallel from the blueprint with a check afterwards.

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

**Ch 45. Data Ingestion & Integration** · NEW · 4,000 words
Sources: databases, files, APIs, events, SaaS tools · full vs incremental loads · change data capture · managed connectors vs custom code (build vs buy) · loading CSV and Parquet reliably · schema changes · web data and its legal and ethical limits.
*Project:* Incrementally ingest Riverstone orders and CRM data into a warehouse.

**Ch 46. Pipelines & Orchestration** · EXPANDED from draft Ch 19 · 4,500 words
Kept concepts; added a full Airflow (or Dagster) example, idempotency demonstrated with a failure test, backfills, alerting · triggering downstream delivery (reports, emails, syncs) only after the data passes its checks.

**Ch 47. Data Quality, Observability & Contracts** · NEW · 3,500 words
Dimensions of data quality · testing data in pipelines · anomaly and freshness monitoring · lineage · data contracts in practice · incident handling for data.
*Project:* Add quality checks and freshness alerts to the Ch 46 pipeline.

**Ch 48. Big Data & Distributed Compute** · EXPANDED from draft Ch 20 · 4,500 words
Kept "most big data isn't"; added PySpark code on the sensor dataset, reading a query plan, finding a shuffle, and a timed comparison with DuckDB and Polars.

**Ch 49. Storage, Warehouses & Lakehouses** · EXPANDED from draft Ch 21 · 5,000 words
Added ACID explained properly · row vs columnar storage demonstrated · partitioning and file sizing · table formats hands-on · warehouse cost and performance basics. Fixes the draft's broken "Chapter 2" reference.

**Ch 50. Streaming & Real-Time** · EXPANDED from draft Ch 22 · 4,500 words
Added a working Kafka producer/consumer example, windowing and late data demonstrated, and a plant sensor-monitoring case.

**Ch 51. Data Activation: Reverse ETL, APIs & System Integration** · NEW · 5,500 words
Why data sitting in a dashboard changes nothing on its own: closing the loop from source to action · the full flow: source systems → ingestion → warehouse → data products (reports, emails, dashboards) → **back into operational systems** · reverse ETL: syncing warehouse data (lead scores, customer health, credit limits, reorder flags) into CRM, ERP, and marketing tools · writing to systems through APIs: authentication (API keys, OAuth), upserts, pagination, rate limits, retries, idempotent writes, choosing the system of record and conflict rules · webhooks and event-driven triggers · integration patterns: point-to-point, hub-and-spoke, message queues, integration platforms (iPaaS) · choosing between custom code, orchestrator tasks, low-code/iPaaS tools, and enterprise integration platforms · RPA for systems with no API, and why it's fragile · file-based integrations (SFTP drops, EDI) that remain common in manufacturing and B2B · audit trails, reconciliation reports, and rollback · keeping credentials secure.
*Project:* A nightly, idempotent sync of Riverstone lead scores and overdue-invoice flags into a sandbox CRM through its API, with a reconciliation report, plus a webhook that alerts sales within a minute when a high-value lead arrives.

**Ch 52. The Cloud, Containers & Infrastructure as Code** · EXPANDED from draft Ch 23 · 5,500 words
Added cloud fundamentals (regions, identity and access, networking) · a Dockerfile built step by step · Kubernetes concepts · a small Terraform example · CI/CD with GitHub Actions. Fixes the "Parts V so far" typo and the FinOps forward reference (now to Ch 65).

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 45

- *(from Ch 2)* Data pipelines use them to detect whether a file has changed since yesterday (Chapter 45).
- *(from Ch 2)* Part V (Chapters 45–52) builds on formats, compression, the cloud, and APIs at company scale; Chapter 64 covers security, privacy, and governance in depth.
- *(from Ch 12)* Chapter 45 covers loading large and messy files reliably.
- *(from Ch 12)* (For CSV files, DBeaver's import wizard works; Chapter 45 covers robust loading.) Run `COUNT(*)` on each table and compare it with the source.

#### Chapter 47

- *(from Ch 1)* This is why analysts check data before they trust it. Chapter 14 teaches how to find and fix these problems at scale, and Chapter 47 shows how data teams catch them automatically before a report goes out.
- *(from Ch 13)* Chapter 47 turns them into automated tests.

#### Chapter 49

- *(from Ch 12)* Snowflake, Google BigQuery, Amazon Redshift, Databricks SQL: cloud *data warehouses* built for analysis (Chapter 49).
- *(from Ch 12)* That guarantee is part of the ACID properties you'll study in Chapter 49.
- *(from Ch 12)* Later in the book: a cloud data warehouse (Chapter 49), where the same SQL runs on billions of rows.

#### Chapter 51

- *(from Ch 2)* You'll call real APIs from Python in Chapter 18, automate reports with them in Chapter 20, and design how whole systems exchange data in Chapter 51.

#### Chapter 52

- *(from Ch 2)* Part V (Chapters 45–52) builds on formats, compression, the cloud, and APIs at company scale; Chapter 64 covers security, privacy, and governance in depth.

## Kickoff prompt

```
You are writing Part V — Data Engineering, Integration & Scale of the book "Analyst to Architect" (Chapters 45–52).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-5-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-5-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```
