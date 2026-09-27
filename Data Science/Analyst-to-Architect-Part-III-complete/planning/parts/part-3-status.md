# Part III — Status (Chapters 28–34)

Owner: Part III chat. Instructions: `planning/chapter-writing-instructions.md` §14.1.
Last updated: 18 September 2026 — **all seven Part III chapters drafted; six approved**. Only Ch 29 awaits review.

Writing order (coordinator brief, 17 Sep 2026): **28 → 34 → 29 → 32 → 33 → 30 → 31.** File numbers unchanged.

## Chapters

| ID | No. | Title | Class | Status | Notes |
|---|---|---|---|---|---|
| P3-28 | 28 | Advanced SQL, Performance & Data Modeling | A | Approved v1; **v1.1 issued 17 Sep** (canon fixes below) | 82 pages; re-verified 63 outputs, 40 checks |
| P3-29 | 29 | Python as Software, Not Scripts | B | **Draft v1.1, awaiting review** (~12.8k words) | 43 pages; now assumes Ch 34 |
| P3-30 | 30 | Inference & Experiments | B | **Approved (v1), 17 Sep 2026** (~11.8k words) | `Ch30-Inference-and-Experiments-v1-approved.pdf`, 37 pages; owns the digital domain |
| P3-31 | 31 | Causal Inference Without Experiments | B | **Approved (v1), 17 Sep 2026** (~10.2k words) | `Ch31-Causal-Inference-Without-Experiments-v1-approved.pdf`, 32 pages |
| P3-32 | 32 | Analytics Engineering with dbt | A | **Approved (v1), 18 Sep 2026** (~11.0k words) | `Ch32-Analytics-Engineering-with-dbt-v1-approved.pdf`, 35 pages |
| P3-33 | 33 | The Computer Science You Actually Need | B | **Approved (v1), 18 Sep 2026** (~9.4k words) | `Ch33-The-Computer-Science-You-Actually-Need-v1-approved.pdf`, 31 pages |
| P3-34 | 34 | The Command Line, Linux & Networking Basics | B | **Approved (v1), 17 Sep 2026** (~9.8k words) | `Ch34-The-Command-Line-Linux-and-Networking-Basics-v1-approved.pdf`, 33 pages |

## Chapter 28 report (approved v1)

**Sections:** 28.1 Three practice databases · 28.2 Recursive CTEs (org chart, walking up, people below, team revenue, BOM explosion, cost roll-up, where-used, loops and `CYCLE`) · 28.3 Advanced frames (ROWS/RANGE/GROUPS, interval ranges, EXCLUDE, WINDOW clause, LAST_VALUE, PERCENTILE_CONT, NTILE) · 28.4 How a database finds rows · 28.5 EXPLAIN / EXPLAIN ANALYZE, join methods · 28.6 Six index experiments + checklist · 28.7 Normalization 0NF→3NF in the lab · 28.8 Grain discipline · 28.9 Star schema `dw` (date, product, rep, SCD2 customer, fact) · 28.10 SCD types 1/2/3 · 28.11 Denormalization, materialized views · 28.12 Migrations, expand/contract, tools · 28.13 The same SQL in MySQL · full template back matter · 22 exercises with worked answers.

**Files**
- `manuscript/ch28-advanced-sql-performance-and-data-modeling.md`
- `figures/make_figs28.py` → fig28-1 … fig28-6 (all rendered and visually checked)
- `companion/ch28/`: `ch28_2025_addons.sql`, `ch28_star_schema.sql`, `generate_riverstone_perf.py` (seed 28; generated data NOT saved: ~77 MB, regenerate), `ch28_perf.py`, `ch28_perf_log.txt`, `migrate.py`, `migrations/` (V1–V5, R__)
- `companion/mysql/`: `ch28_2025_addons_mysql.sql`, `ch28_queries_mysql.sql`
- `checks/ch28_check.py` (40 checks), `checks/ch28_build.py`, `checks/ch28_fill.py` (author helper)

**Verification**
- `verify_sql.py`: 70 statements run, **63 outputs checked, 0 mismatches** (PostgreSQL 16 + MySQL 8.0.46). Prerequisite: load `ch28_2025_addons.sql`, `ch28_star_schema.sql`, and `riverstone_perf` (with `ch28_perf.py` run once, which leaves the materialized view) before verifying.
- Timings and EXPLAIN ANALYZE plans (sections 28.5, 28.6, 28.11, 28.13) are marked `run: none` and quoted verbatim from `ch28_perf_log.txt` (7-run medians; machine: 1 vCPU, 3 GB RAM, Ubuntu 24.04).
- `ch28_queries_mysql.sql` runs end to end with no errors; results match PostgreSQL (BOM costs, fact total ₹4,335,471, SCD2 segment difference ₹84,842, normalization ₹129,040, median ₹21,375, quarter averages).
- `migrate.py` run for real: first run applies V1–V5, second run applies nothing, edited V3 triggers the checksum error (output in chapter is verbatim).
- `ch28_check.py`: 40 checks passed. Style: 0 em dashes in prose, banned words removed, American spelling checked.
- PDF built (81 pages); pages spot-checked. Known cosmetic issue: psql dashed header lines on the widest EXPLAIN plans wrap in the PDF (content intact).

**Sources checked (fast-changing facts)**
- Flyway naming (V/R prefixes), schema history table, checksums, info/validate/repair: https://documentation.red-gate.com/fd/flyway-schema-history-table-273973417.html · https://documentation.red-gate.com/fd/info-277578881.html · https://github.com/flyway/flywaydb.org/blob/gh-pages/documentation/concepts/migrations.md
- Flyway release cadence (12.x/13.x in 2026): https://documentation.red-gate.com/flyway/release-notes-and-older-versions/flyway-desktop-9-release-notes · https://www.componentsource.com/product/flyway/releases
- PostgreSQL/MySQL feature facts (MERGE 15+, CYCLE/SEARCH 14+, no GROUPS/EXCLUDE in MySQL, InnoDB FK indexes, MySQL NOT NULL implicit default, cte_max_recursion_depth) were confirmed by running them on the test servers, not only from docs.

**Manual checks needed**
1. Flyway could not be downloaded in the sandbox (Redgate domains blocked): confirm the Flyway description in 28.12 against a real install, and the free-edition wording in *Tools*.
2. "Power BI's documentation recommends star schemas" (28.9): confirm against Microsoft Learn "Understand star schema and the importance for Power BI".
3. MySQL 8.4 LTS behavior claimed "the same" for the features used (tested on 8.0.46 only).
4. PostgreSQL: `CREATE INDEX` blocking writes / `CONCURRENTLY` (28.6, real-world story) taken from knowledge of PostgreSQL docs; not demonstrated with concurrent sessions.

## New Riverstone facts (proposed, used in Ch 28)

- **Arvind Nair**, Managing Director (top of the org chart).
- Department heads reporting to the MD: Anita Rao (Sales Head), Suresh Menon (Finance Manager), **Harpreet Gill** (Head of Production, Taloja), **Joseph D'Souza** (Purchasing Manager), **Sandeep Yadav** (Warehouse & Dispatch Manager, Bhiwandi Main), **Lakshmi Reddy** (HR Manager), **Zoya Mirza** (Marketing Manager), **Tenzin Dorji** (Customer Support Lead).
- Others: Priya Nambiar (Accounts Executive), Ramesh Patil (Plant Manager, Taloja), Kiran Bhosale (Plant Manager, Chakan), Ajay Kumar and Swati Joshi (Shift Supervisors), Farhan Ali (Quality Inspector, Taloja), Gopal Sahu, Sunita Pawar, Irfan Shaikh (Machine Operators), Mohan Das (Dispatch Supervisor). Meera Iyer reports to Anita Rao.
- `staff` (HRMS view, 24 people) coexists with the ERP's 5-row `employees` table; in the HRMS Anita reports to the MD. Location value "Head office" (no city assigned).
- BOM for products 101, 102, 104, 106, 108 with materials from Western Polymers, Gujarat Pigments, Sagar Labels, Deccan Cartons, Kaveri Steel Works (costs in `ch28_2025_addons.sql`). Garden Chair material cost ₹647.80.
- 2025 customer changes (ERP audit log): Patel Kitchenware Wholesale→Retail 2025-04-01; Metro Mart Thane→Mumbai 2025-07-01; Harbour Traders Retail→Wholesale 2025-09-01. `customers` shows values after the changes.
- `riverstone_perf` (2023–2025, 1.93M lines) is a volume dataset, not canonical; its totals are unrealistic by design.

## Chapter 29 report (draft v1)

**Sections:** 29.1 The script that works until it doesn't · 29.2 Functions and modules · 29.3 Project structure and configuration · 29.4 Environments and lockfiles (venv, uv) · 29.5 Classes, when they help · 29.6 Type hints (mypy) · 29.7 Testing with pytest · 29.8 Errors and logging · 29.9 Robust API clients · 29.10 Code review · full template back matter · 15 exercises with answers.

**Files**
- `manuscript/ch29-python-as-software-not-scripts.md`; `figures/make_figs29.py` → fig29-1 … fig29-4 (rendered and checked)
- `companion/ch29/`: `start/monthly_report.py` (the "Ch 18 script"), `riverstone-report/` (uv package: pyproject.toml, uv.lock, src with 8 modules, 23 tests), `mock_crm_api.py` + `leads.json`, `ch29_check.py`

**Verification**
- `verify_python.py --cwd companion/ch29`: 11 blocks, 11 outputs checked, 0 mismatches (needs riverstone_2025 only for nothing in the blocks; the mock API binds 127.0.0.1:8029).
- Package: `uv run pytest` 23 passed (integration test needs RIVERSTONE_DATABASE_URL); `uv run mypy` strict: no issues in 9 files; fresh `uv sync --locked` reproduces 30 packages.
- All shell outputs (script runs, uv, mypy error and fix, pytest pass and deliberate failure, CLI exit codes) pasted from real runs, captured under a neutral user folder (/home/meera).
- `ch29_check.py`: 24 checks passed. Style: no em dashes, banned words removed.

**Sources checked:** uv project workflow (uv init --package, uv add, uv.lock, uv sync, uv run): https://docs.astral.sh/uv/guides/projects/ · https://docs.astral.sh/uv/ . All library versions taken from the lockfile of the tested run.

**Manual checks needed**
1. Windows commands (PowerShell env var, venv activation) not run on Windows.
2. `httpx`, `tenacity`, Ruff, Pyright, Poetry/PDM described from general knowledge, not run.

**Decisions taken (D6–D8, defaults):** Ch 29 ships its own starting script; venv + pip taught first, then uv; requests with hand-written retries.

**Requests for the coordinator (Ch 29)**
- **Chapter 18 (Part II) should end its project with a script matching `companion/ch29/start/monthly_report.py`** (December 2025 report from riverstone_2025 to Excel: revenue ₹439,823.50, 18 orders, 115.7% of target), or Ch 29 §29.1 must be updated to match what Ch 18 produces.
- New mock API: `mock_crm_api.py` (leads endpoint, page/page_size, X-API-Key demo-key, planned 503/429). The blueprint's Automation sandbox (mock CRM/ERP API) could absorb it.
- New Riverstone story facts: the monthly report runs by Windows Task Scheduler on the 2nd of each month; Feb 2026 "January was zero" incident caused by a failed ERP→reporting load (consistent with Ch 3's January figures).
- Promises made: Ch 20 (schedules this package, alerts on exit code), Ch 26 (PRs, CI), Ch 32, Ch 33, Ch 34 (env vars, exit codes, HTTP), Ch 46, Ch 47, Ch 51 (idempotency keys, writing to systems), Ch 56, Ch 72.

## Chapter 34 report (approved v1)

**Sections:** 34.1 Opening a terminal · 34.2 Where am I, and what's here · 34.3 Pipes, redirection, exit codes · 34.4 Searching and summarizing text (grep, wc, sort, uniq, cut, awk) · 34.5 Permissions · 34.6 Environment variables and PATH · 34.7 Shell scripts · 34.8 SSH · 34.9 Networking in plain English · full template · 16 exercises with answers · 4 figures.

**Files:** `manuscript/ch34-…md`; `figures/make_figs34.py` + fig34-1…4; `companion/ch34/` (`make_ch34_data.py`, `sales_lines_2025.csv`, `practice/` with 61 daily exports and a 187-line job log, `daily_file_server.py`, `daily_summary.sh`, `weekly_summary.sh`, `fetch_daily.sh`); `checks/ch34_check.py`; **`checks/verify_shell.py` (new tool, see below)**.

**Verification:** 104 terminal commands run, 104 outputs checked, 0 mismatches, from a freshly generated practice folder, as an ordinary user (not root). Real SSH with keys, real `scp`/`rsync`, real `curl` against the local file server, real `ss`. `ch34_check.py`: 24 checks passed. Shell answers reconcile with the database (2025 ₹4,335,471; December ₹439,823.50 and its category split, matching Ch 29's report).

**Reproducing:** rerun `make_ch34_data.py` before verifying (the chapter's commands archive files and create scripts), then
`python3 checks/verify_shell.py manuscript/ch34-….md --cwd <copy of companion/ch34> --user <a normal user>`. Needs `sshd` running with the user's key in `authorized_keys` and a `reportserver` entry in `~/.ssh/config`.

**Proposed tools addition:** `checks/verify_shell.py` → `tools/verify_shell.py`. Same contract as the SQL and Python verifiers (`# terminal` blocks, `$` commands, `<!-- run: none -->`, `--fill` for the author). One bash session per chapter, `LC_ALL=C`, each command's stdin from `/dev/null` (otherwise `ssh` swallows the session), background jobs don't block shutdown. Limitation: a blank line ends an expected output, so `ls a b` must be two commands.

**Manual checks needed:** WSL install and macOS BSD tool differences (described, not run); `cron` examples (syntax checked, not scheduled).

**New story fact:** February 2026, the report server's disk fills because the daily download never archived or deleted anything (84 files × 412 MB); found and fixed over SSH. Follows Ch 29's alerting.

**Promise made:** Ch 50 (IP, ports, SSH keys for cloud machines); Ch 73 (permissions, exit codes, debugging a failed job).

## Chapter 33 report (approved v1)

**Sections:** 33.1 Big-O · 33.2 The four structures you'll use every day · 33.3 Stacks and queues · 33.4 Trees and graphs · 33.5 Searching and sorting · 33.6 Recursion · 33.7 Hashing · 33.8 Memoization, dynamic programming, greedy · 33.9 Memory and the other costs · 33.10 What coding interviews test · full template · 18 exercises with answers · 3 figures.

**New data and scripts:** `companion/ch33/generate_ch33_data.py` (seed 33; 176,110 order lines and 20,000 supplier invoice lines, 19,500 of which should match), `match_slow.py` and `match_fast.py` (the project's before and after), and `checks/ch33_timings.py`, which reproduces every timing quoted.

**Measured, not asserted (1 vCPU sandbox):** naive matching 0.96 / 1.84 / 3.73 / 7.51 s at 250 / 500 / 1,000 / 2,000 invoices (so ~75 s for the full file); dictionary index 0.045 s to build, 0.009 s to match all 20,000; `in` on a list 1.451 s vs 0.00004 s on a set; `list.pop(0)` 0.873 s vs `deque.popleft()` 0.003 s; 200 linear searches 0.713 s vs 10,000 binary searches 0.0061 s; plain `fib(32)` 0.226 s vs 0.000023 s memoized; a million-row list 40.4 MB vs a generator 0.0005 MB.

**Reconciles with earlier chapters:** the recursive bill-of-materials example returns 3.4 kg of steel tube per Garden Chair, the same as Chapter 28's recursive CTE; the hashing section connects `dict` lookups to Chapter 28's `Hash Join`.

**Verification:** `verify_python.py --cwd companion/ch33`: 22 blocks, 22 outputs, 0 mismatches. `ch33_check.py`: 22 checks passed. Style checks clean. Generated CSVs excluded from the zip (5.9 MB); the generator rebuilds them identically.

**Tooling note for the coordinator:** `tools/verify_python.py` has the same marker bug I found in my shell verifier — a `<!-- run: none -->` before a non-Python fenced block is spent on the *next Python* block, silently skipping it. I worked around it by making the affected blocks self-contained, but a one-line fix (clear the flag when the next fence isn't Python) would prevent a subtle class of unverified chapters. My `checks/py_fill.py` has the fix and is in the Ch 33 zip.

**Manual checks needed:** `cProfile`, `snakeviz`, `py-spy`, Polars and DuckDB are named in *Tools* but not run.

**Promises made:** Ch 72 (coding questions), Ch 69 (talking through a problem).

## Chapter 32 report (approved v1)

**Sections:** 32.1 What analytics engineering is (ETL vs ELT) · 32.2 Your first project · 32.3 Models, sources and `ref` · 32.4 Layers · 32.5 Building the star schema as models · 32.6 Materializations · 32.7 Tests · 32.8 Docs and lineage · 32.9 Snapshots · 32.10 Incremental models · 32.11 Macros · 32.12 Linting and CI · 32.13 What dbt is not, and the semantic layer · full template · 18 exercises with answers · 3 figures.

**The project is real and runnable:** `companion/ch32/riverstone_dbt`, built on `riverstone_2025` with dbt Core 1.12.5 and dbt-postgres 1.11.0. `dbt build` runs **36 nodes, 0 errors**: 4 staging views, 5 marts tables, 1 incremental model, 1 snapshot, 25 tests. Every model file printed in the chapter is pulled from the project at assembly time, so text and code cannot drift.

**Delivers the promises made to this chapter:** Ch 12's "you'll see that layout" (staging/marts), Ch 13's SQL linting (SQLFluff 4.3.0 with the dbt templater, real output), Ch 13's "dbt models replacing shared views" (`sales_lines` becomes `stg_order_items` plus `fct_sales_line`), and Ch 28's star schema rebuilt as models with the same reconciliation (326 rows, ₹4,335,471).

**Everything demonstrated was run:** a failing reconciliation test (`FAIL 1` plus the path to the compiled SQL); a snapshot capturing Metro Mart's move to Thane (one row becomes two, one closed and one current); an incremental model on the 1.9M-line database (**full refresh 13.91 s vs incremental 0.90 s**, ~15×); `dbt compile` showing the macro expanded; SQLFluff reporting ten real issues.

**Verification:** `verify_sql.py` checks the chapter's query outputs (model listings are marked `run: none`, since they are Jinja, not SQL). `ch32_check.py`: 15 checks passed, including that the dbt marts match Chapter 28's `dw` schema and the `sales_lines` view to the rupee, that each customer has exactly one current row, and that **no password appears anywhere in the project**.

**Manual checks needed:** dbt Cloud plans and the semantic layer / MetricFlow state are described, not used (both change fast; flagged in the text and for the refresh list). `dbt_utils`, `dbt_expectations`, `codegen` and `elementary` are named but not installed. The GitHub Actions workflow is written to the current syntax but not run in CI.

**Refresh items:** dbt Core version and command names; SQLFluff rules; adapter list; dbt Cloud pricing.

## Chapter 31 report (approved v1)

**Sections:** 31.1 The data and the three true answers · 31.2 Why the two obvious comparisons mislead · 31.3 Difference-in-differences · 31.4 Parallel trends and a quarter-by-quarter view · 31.5 Matching and propensity scores · 31.6 Regression discontinuity · 31.7 Synthetic control · 31.8 Instrumental variables (intuition) · 31.9 How much to trust each answer · full template · 18 exercises with answers.

**New dataset:** `companion/ch31/generate_ch31_data.py` (seed 31, standard library only) builds three linked datasets, each with a **known true effect** so every method can be marked:

| Data | Event | True effect | Naive answer | Method's answer |
|---|---|---|---|---|
| 96 region-months | North's prices rose 6% on 1 Oct 2025 | volume −8.0% | +1.7% (before/after), −23% (cross-section) | DiD −7.0% (CI −10.1% to −3.9%); synthetic control −6.6% |
| 240 key accounts | quarterly business reviews | revenue +7.0% | +75.0% | matched +7.1%, adjusted +7.7% (CI +4.6% to +10.9%) |
| 60,000 orders | free delivery at ₹25,000 | +6.0 points | — | RD +7.3 points (CI +5.6 to +8.9), stable across bandwidths |

**Honest findings kept in the chapter rather than tuned away:** matching moves between +0.4%, +7.1% and +12.2% depending on the caliper (exercise 9), which is why section 31.9 ranks it below RD and DiD; region-specific trends shrink the DiD to −4.8% with an interval crossing zero (exercise 13); two of the three synthetic-control placebos have useless pre-fit, so only one placebo is informative (exercise 11); the two-by-two DiD regression gives a CI of −0.365 to +0.219 before fixed effects.

**Verification:** `verify_python.py --cwd companion/ch31`: 32 blocks, 32 outputs, 0 mismatches. `ch31_check.py`: 20 checks passed. Style checks clean. Generated CSVs excluded from the zip (2 MB); the generator rebuilds them identically.

**Manual checks needed:** `DoWhy`, `EconML`, `CausalImpact` and `linearmodels` are named in *Tools* but not run; the instrumental-variables section is intuition only, by design.

**Promises made:** Ch 43 (pricing and elasticity), Ch 55, Ch 73 (three "you can't A/B test this" cases).

## Chapter 30 report (approved v1)

**Order note:** written out of the coordinator's sequence at the author's request (28 → 34 → 29 → **30**); nothing in it depends on Ch 32 or 33, and both remain queued.

**Sections:** 30.1 The data and the question · 30.2 Standard error and confidence intervals · 30.3 The t-test · 30.4 Effect size · 30.5 Proportions and chi-square · 30.6 ANOVA and post-hoc tests · 30.7 Power and sample size · 30.8 Designing an experiment · 30.9 The website test end to end · 30.10 Peeking, multiple testing, novelty, SRM and outliers, by simulation · 30.11 Regression for inference · 30.12 Writing the result up · full template · 18 exercises with answers · 4 figures.

**New canonical dataset (Part III now owns the blueprint's digital domain, also used by Ch 42):** `companion/ch30/generate_riverstone_web.py`, seed 30, standard library only. 214,528 sessions, 622,090 events, 47,286 visitors in the A/B test `enquiry_form_2026_02` (2–15 Feb 2026), 176,000 visitors overall. Loads into PostgreSQL as `riverstone_web`. The blueprint says ~2M events; this is 622k so the whole chapter runs in seconds on a laptop — **confirm or ask for the larger size.**

**The test result (all chapter numbers reconcile to it):** control 3.90% (937 of 24,036), variant_b 4.45% (1,035 of 23,250); +0.55 pp (95% CI 0.19 to 0.91), +14.2% relative (95% CI +4.9% to +23.4%), z = 3.009, p = 0.0026. Planned sample size 24,955 per group for a 0.5 pp MDE at 80% power, which is where the fortnight came from.

**Deliberate teaching faults in the data:** a novelty effect (week 1 lift 24%, week 2 5%); a sample-ratio mismatch caused by a Safari tagging bug (53.1/46.9 on Safari, p = 0.0003 overall); enquiry values where the top 1% hold 16.6% of the total. The peeking simulation measures 25.5% false positives against a nominal 5%.

**Verification:** `verify_python.py --cwd companion/ch30`: 39 blocks, 39 outputs checked, 0 mismatches. `ch30_check.py`: 30 checks passed. Style checks clean. Generated CSVs are not in the zip (46 MB); the generator rebuilds them identically.

**Manual checks needed:** experiment-platform names in *Tools* (Optimizely, VWO, GrowthBook, Statsig) not verified against current products; the Bayesian box is descriptive only.

**Promises made:** Ch 31 (same questions without randomization), Ch 42 (same website data for funnels and attribution), Ch 55 (experiments on models), Ch 73 (three A/B debugging cases built on section 30.10's faults).

## Chapter 28 and 29 v1.1 (canon fixes, 17 Sep 2026)

Applied after reading `cross-part-issues.md` and the coordinator note:

- **Ch 28 name clashes resolved** in `staff`: Arvind Nair → **Arvind Kapoor** (the full dataset has Arjun Nair, RSM South); Harpreet Gill → **Harpreet Sethi** (Sandeep Gill, RSM North); Sandeep Yadav → **Mahesh Yadav**; Irfan Shaikh → **Farid Shaikh** (issue 1's proposed *Irfan Sheikh*).
- **Ch 28 `staff` now matches issue 3's sales organization**: 35 people, with Vikram Singh as *Sales Manager, Key Accounts* and a regional branch under Anita Rao — Arjun Nair (South), Pooja Desai (West), Sandeep Gill (North) and eight executives (Divya Krishnan, Vivek Chandran, Sneha Pillai, Nisha Bhatt, Aditya Verma, Rohit Kamat, Karan Ahuja, Ritu Bansal). If Part II-A names the regional executives differently, this table follows theirs.
- **Ch 28 acknowledges issue 5**: §28.1 now says `riverstone_2025` is the key accounts' slice, and the team-revenue query filters to the five reps the ERP knows, explaining why.
- **Ch 28 and the full dataset**: the performance sections still use the chapter's own generated `riverstone_perf` (5,000 customers, 714,285 orders, 1,926,847 lines, seed 28) because `riverstone_full` isn't in the project yet. §28.1 says the same commands work on the full dataset. **Ask:** when `generate_riverstone_full.py` lands, should Ch 28 switch to it and drop `riverstone_perf`?
- **Ch 29 v1.1** now assumes Ch 34 (terminal, environment variables, exit codes) instead of pointing forward to it.
- All three chapters re-verified after the changes: Ch 28 63 SQL outputs / 40 number checks / MySQL companion clean; Ch 29 11 Python outputs / 23 package tests / mypy strict / 24 number checks.

## Refresh items to add to planning/pre-publication-refresh.md

| Chapter | What to refresh | Tested on |
|---|---|---|
| 28 | PostgreSQL 18 and MySQL 9.7 LTS behavior for `MERGE`, `CYCLE`, partial and covering indexes, plans | PostgreSQL 16, MySQL 8.0.46 |
| 28 | Flyway edition and command names (`info`, `validate`, `repair`), Liquibase and Alembic descriptions | Redgate docs, 17 Sep 2026 |
| 29 | uv (0.12.15), pandas 3.0.5, pytest 9.1.1, mypy 2.3.1, requests 2.34.2; Python 3.13/3.14 | Python 3.12.3 |
| 34 | WSL install command, macOS GNU-tool differences, `ss`/`netstat` availability | Ubuntu 24.04, bash 5.2 |

## Decisions requested (Chapter 29)

- **D6** Chapter 18 isn't written, but Ch 29's project refactors "the Ch 18 script". Default: Ch 29 ships a script-style `monthly_report.py` in `companion/ch29/start/` matching Ch 18's blueprint project; Part II writes Ch 18's project to match (or Ch 29 is updated).
- **D7** Environment and lockfile tool: default venv + pip (requirements) taught first, then uv (`pyproject.toml` + `uv.lock`) as the recommended workflow; Poetry mentioned. Verify current docs before writing.
- **D8** HTTP client: default `requests` (what analysts meet first) with retries/backoff written explicitly; `httpx` mentioned.

## Requests for the coordinator

- **Promises made to other chapters:** Ch 14 (splitting 0NF data), Ch 16 (reads the `dw` star), Ch 29 (packages migrate.py/generator), **Ch 32 (rebuild `dw` as dbt models; dbt snapshots for SCD2)**, Ch 47 (grain tests as automated checks), Ch 49 (materialized views in cloud warehouses), Ch 62, Ch 71 (SQL bank), Ch 77.
- `tools/setup_databases.sh` does not load Ch 28's add-ons, star schema, or `riverstone_perf`; consider adding them (verification prerequisite above).
- Proposed tools improvement: PDF CSS for smaller mono font in very wide output blocks (plan lines wrap).
- Saving: this session cannot write to the project; all files delivered as downloads.

## Issues found in other chapters

- **`tools/verify_python.py`**: a `<!-- run: none -->` placed before a non-Python fenced block (a terminal session, say) is spent on the *next Python* block, which is then silently skipped and never verified. Found while writing Ch 33; `checks/py_fill.py` in the Part III package carries the one-line fix (clear the flag when the next fence isn't Python). The same bug existed in the first version of `verify_shell.py` and is fixed there.
- Ch 13's "11 orders missing a sales rep" counts one cancelled order; 10 are non-cancelled. Ch 28 states both.

- None. (Ch 13's "11 orders missing a sales rep" counts one cancelled order; 10 are non-cancelled. Ch 28 states both.)
