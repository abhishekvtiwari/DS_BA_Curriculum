# Analyst to Architect — Part III: Advanced Analytics & Analytics Engineering — complete bundle

Chapters 28–34. About 92,100 words, 293 PDF pages, 29 figures. Six chapters approved; **Chapter 29 is at v1.1 and awaiting the author's review**.

| Ch | Title | Class | Status | Words |
|---|---|---|---|---|
| 28 | Advanced SQL, Performance & Data Modeling | A | Approved v1.1 | ~26,900 |
| 29 | Python as Software, Not Scripts | B | **Draft v1.1, awaiting review** | ~12,800 |
| 30 | Inference & Experiments | B | Approved v1 | ~11,800 |
| 31 | Causal Inference Without Experiments | B | Approved v1 | ~10,200 |
| 32 | Analytics Engineering with dbt | A | Approved v1 | ~11,000 |
| 33 | The Computer Science You Actually Need | B | Approved v1 | ~9,400 |
| 34 | The Command Line, Linux & Networking Basics | B | Approved v1 | ~10,000 |

Written in the order 28 → 34 → 29 → 32 → 33 → 30 → 31, which is also the reading order; the file numbers are unchanged until final assembly.

## Databases and datasets

| Name | What it is | Used by |
|---|---|---|
| `riverstone_2025` | the one-year key accounts dataset | 28, 29 |
| `riverstone_perf` | a synthetic volume dataset (714,285 orders, 1,926,847 lines, seed 28), **not canon** | 28's performance work |
| the `dw` star schema | built by `ch28_star_schema.sql`, rebuilt as dbt models | 28, 32 |
| the digital domain | 214,528 sessions, 622,090 events, a two-week A/B test (seed 30) | 30 |
| the causal datasets | a region-month panel, a selected customer program, a threshold dataset, each with a known true effect (seed 31) | 31 |

Large generated data is not included; every generator is seeded, so rebuilding reproduces the exact numbers printed in the chapters.

## Rebuilding

```
# datasets
cd companion/ch28 && python3 generate_riverstone_perf.py
cd ../ch30 && python3 generate_riverstone_web.py
cd ../ch31 && python3 generate_ch31_data.py
cd ../ch33 && python3 generate_ch33_data.py
cd ../ch34 && python3 make_ch34_data.py

# databases
bash tools/setup_databases.sh companion          # riverstone_2025 + Ch 28 add-ons + the dw star schema
createdb riverstone_perf && psql -d riverstone_perf -f companion/ch28/perf_data/load_postgresql.sql
cd companion/ch32/riverstone_dbt && RIVERSTONE_PASSWORD=... dbt build --profiles-dir .

# verify
python3 tools/verify_sql.py    manuscript/ch28-advanced-sql-performance-and-data-modeling.md
python3 tools/verify_python.py manuscript/ch30-inference-and-experiments.md --cwd companion/ch30
python3 tools/verify_shell.py  manuscript/ch34-the-command-line-linux-and-networking-basics.md \
        --cwd <a copy of companion/ch34> --user <a normal user>
for c in 28 29 30 31 32 33 34; do python3 checks/ch${c}_check.py; done
```

Totals when everything is in place: **63 SQL outputs, 104 terminal outputs, 104 Python outputs, 0 mismatches**, plus **175 number checks**. Chapter 34 mutates its practice folder as it runs, so regenerate it before each run and start `sshd`. Timings and query plans are marked `run: none` and quoted from `checks/ch28_perf_log.txt` and `checks/ch33_timings_log.txt`.

Prerequisites: PostgreSQL 16 with `riverstone_2025` loaded, MySQL 8.0 for Chapter 28's dialect section, Python 3.12 with pandas, numpy, scipy, statsmodels, sqlalchemy, psycopg, openpyxl, requests, pytest, mypy, dbt-core, dbt-postgres, sqlfluff; and for Chapter 34 bash, curl, ssh/sshd, rsync, iproute2 and a normal user account.

## Coordinator checks on this part

All 29 figure references resolve, every companion file named in a chapter is present, and the style scan found two words in 92,000: one `analyse` in Chapter 29 and one `honestly` in Chapter 30, with no em dashes in prose anywhere.

`tools/check_code_teaching.py` (§6.5), after being corrected to recognize terminal sessions:

| Ch | Code blocks | Blocks flagged |
|---|---|---|
| 28 | 88 | 40 |
| 29 | 39 | 28 |
| 30 | 40 | 38 |
| 31 | 32 | 30 |
| 32 | 33 | 16 |
| 33 | 28 | 26 |
| 34 | 43 | 10 |

Chapter 34 is the model. A flag is a question, not a verdict; these are the input to the part-completion review pass.

## Open items

- **Chapter 29 v1.1** needs the author's review.
- **Cross-part issue 9:** Chapter 29 refactors "the Chapter 18 script", but Chapter 18 now exists and its script is already reasonable. Decision pending.
- **Cross-part issue 10:** Chapter 28's eight regional sales executives need the full dataset's names and `employee_id` 9–16.
- **Issue 11, decided:** Chapter 28 keeps `riverstone_perf` rather than switching its timings to `riverstone_full`.
- `tools/verify_python.py` carries Part III's fix for the skipped-block bug; Chapters 29–33 should be re-verified with it.
- Refresh items for Chapters 28, 29, 32 and 34 are in `planning/pre-publication-refresh.md`.

See `planning/parts/part-3-coordinator-reply.md` for the full list and `planning/parts/part-3-status.md` for the per-chapter reports.

## What's where

| Folder | Contents |
|---|---|
| `manuscript/` | The chapters as Markdown (the source of truth for the text) |
| `pdf/` | One built PDF per chapter; `*-approved.pdf` is the approved version |
| `figures/` | `fig*.svg` as used in the PDFs, `png/` renders for slides, and the `make_figs*.py` scripts that draw them |
| `companion/` | Everything a reader downloads for these chapters |
| `checks/` | Number-check scripts: every figure quoted in the text is recomputed from the data |
| `tools/` | The verifiers (`verify_sql.py`, `verify_python.py`, `verify_shell.py`, `check_code_teaching.py`), `setup_databases.sh`, and the PDF builder |
| `planning/` | Chapter map, progress tracker, writing instructions, Riverstone bible additions, cross-part issues, pre-publication refresh list |
| `planning/parts/` | This part's brief and status file |

## Reading order versus chapter numbers

Chapters keep the numbers they were written with; the coordinator renumbers the whole book in one pass at final assembly. The mapping is at the top of `planning/chapter-map.md`.

## The rules every chapter follows

`planning/chapter-writing-instructions.md` is the master brief. Two sections matter most:

- **§6.5** — teach code and formulas line by line: the question in plain words, the plan before any code, short code, the real output and how to read it, then one bullet per line, plus a settings table with "what happens if you change it" and at least one measured what-if.
- **§15.1** — the part-completion review pass: when a part's last chapter is approved, read it straight through as a reader would, work out the cause of each problem at the level of the part, and only then fix in place.

Riverstone Supplies is fictional. Every person, customer, product and number in the data is invented.
