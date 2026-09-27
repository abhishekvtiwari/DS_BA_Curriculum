# Analyst to Architect — Part V: Data Engineering, Integration & Scale — complete bundle

Chapters 45–52, **all eight approved**. About 75,100 words, 23 figures, 8 approved PDFs.

| Ch | Title | Class | Status | Words |
|---|---|---|---|---|
| 45 | Data Ingestion & Integration | B | Approved v1 (16 Sep 2026) | ~12,000 |
| 46 | Pipelines & Orchestration | B | Approved v1 (17 Sep 2026) | ~11,300 |
| 47 | Data Quality, Observability & Contracts | B | Approved v1 (17 Sep 2026) | ~10,400 |
| 48 | Big Data & Distributed Compute | B | Approved v1 (18 Sep 2026) | ~7,800 |
| 49 | Storage, Warehouses & Lakehouses | B | Approved v1 (18 Sep 2026) | ~7,800 |
| 50 | Streaming & Real-Time | B | Approved v1 (18 Sep 2026) | ~7,900 |
| 51 | Data Activation: Reverse ETL, APIs & System Integration | B | Approved v1 (19 Sep 2026) | ~8,500 |
| 52 | The Cloud, Containers & Infrastructure as Code | B | Approved v1 (19 Sep 2026) | ~9,300 |

Written in the Part I chat at the author's request. Part V is content-complete and fully approved; the part-completion review pass (§15.1) is what remains.

## What makes this part work

The chapters demonstrate failures rather than describing them, and the failures are real runs: an ID watermark that actually misses orders 10174 and 10175, a plain `INSERT` that actually fails on the primary key, an append-style pipeline that actually doubles the daily flash to ₹77,420 while the transactional version holds at ₹38,710, a real 503-then-retry on a new lead, a webhook delivery timed to a local inbox, and a write reconciliation that catches a deliberately introduced mismatch.

## What's where

| Folder | Contents |
|---|---|
| `manuscript/` | The eight chapters as Markdown |
| `pdf/` | The eight approved chapter PDFs |
| `figures/` | 23 figures as SVG plus the `make_figs*.py` scripts that draw them |
| `companion/` | Per-chapter practice environments, reset scripts, mock APIs and generators; the shared PostgreSQL and MySQL setup files |
| `checks/` | One number-check script per chapter |
| `tools/` | The verifiers (`verify_sql.py`, `verify_python.py`, `verify_shell.py`, `check_code_teaching.py`), `setup_databases.sh`, and the PDF builder |
| `planning/` | Chapter map, writing instructions, progress tracker, bible additions, cross-part issues, refresh list, promises, and the §6.5 note |
| `planning/parts/` | Part V's brief, status file and the coordinator's reply |

Generated practice data is rebuilt by each chapter's reset script rather than stored.

## Rebuilding and verifying

```
bash tools/setup_databases.sh companion            # riverstone, riverstone_2025
cd companion/ch45 && python3 reset_ch45.py         # each chapter has its own reset/setup script

cd ../../figures && for f in make_figs4*.py make_figs5*.py; do python3 "$f"; done

python3 tools/verify_python.py manuscript/ch45-data-ingestion-and-integration.md --cwd companion/ch45
for f in checks/ch*_check.py; do python3 "$f"; done
python3 tools/check_code_teaching.py manuscript/ch46-pipelines-and-orchestration.md
```

`verify_python.py` now puts `--cwd` on `sys.path`, so companion imports work without setting `PYTHONPATH`; that fix came from this part.

Environment: Python 3.12.3, DuckDB 1.5.5, psycopg2 2.9.13, requests 2.33.1, PostgreSQL 16 with `wal_level = logical` (Chapter 45's logical decoding section), Dagster and Airflow for Chapter 46.

## Coordinator checks on this part

All 21 figure references resolve. The style scan is the cleanest in the book for em dashes: two in 75,100 words. To fix in the review pass: fifteen uses of the banned word *genuinely* (Ch 47, 48, 49, 50, 51, 52), one *honestly* (Ch 52), and four American-spelling fixes (`centre`, `labelled`, `behaviour`).

`tools/check_code_teaching.py` (§6.5), for the review pass:

| Ch | Code blocks | Blocks flagged | Ch | Code blocks | Blocks flagged |
|---|---|---|---|---|---|
| 45 | 24 | 8 | 49 | 9 | 6 |
| 46 | 17 | 15 | 50 | 10 | 7 |
| 47 | 14 | 6 | 51 | 9 | 5 |
| 48 | 12 | 8 | 52 | 7 | 2 |

In proportion these are the best counts of any part written before §6.5 existed. Chapter 46 is the one to look at first.

## Open items

- **The §6.5 code-teaching standard never reached this part.** The coordinator's note of 18 September went to the Part II-A and Part III chats only, so no Part V chapter has the settings table it requires, and only Chapter 48 has a predict-before-you-run prompt. That is a coordinator routing error, logged as cross-part issue 16; the settings tables belong in the review pass, not in reopening approved chapters.
- **Chapter 52 is the only chapter in the book whose code has never been run.** The sandbox had no cloud access, so the Dockerfile, Kubernetes manifest, Terraform configuration and GitHub Actions workflow are parser-validated and trigger-simulated, not executed. Cross-part issue 17: either run the chapter's project once on a real account before publication, or say in the chapter that the examples are validated but unexecuted.
- **The cloud provider for Chapter 52** is an open author decision. Part V recommends provider-neutral concepts with AWS as the primary named example.
- Manual checks: PostgreSQL logical decoding setup steps by operating system (tested on Ubuntu 24.04 only), and the DPDP Act 2023 and GDPR wording in §45.11.
- Chapter 45's proposed Riverstone facts need checking against Part II's Chapter 20 timeline.

`planning/parts/part-5-coordinator-reply.md` has the full reply; `planning/parts/part-5-status.md` has the per-chapter reports.

## The rules every chapter follows

`planning/chapter-writing-instructions.md` is the master brief. Two sections matter most:

- **§6.5** — teach code and formulas line by line: the question in plain words, the plan before any code, short code, the real output and how to read it, then one bullet per line, plus a settings table with "what happens if you change it" and at least one measured what-if.
- **§15.1** — the part-completion review pass: read the part straight through as a reader would, work out the cause of each problem at the level of the part, and only then fix in place.

Riverstone Supplies is fictional. Every person, customer, product and number in the data is invented.
