# Chapter 47 · Data Quality, Observability & Contracts · summary

**Result:** all 32 content findings and the two open visual findings (V47.1, V47.2) applied and verified; the style-pass rows re-checked in the rebuilt PDF. The Ch 47 part of RJ-S2-18 is half done (the date arithmetic); the rest waits for the fact sheet. Rebuilt PDF: 45 pages, layout check clean, both figures at 7.9 pt or more. Details line by line: `changelog/ch47.md`.

## What changed

- **Code taught like Jupyter.** The setup is three cells (reset and connect, the 2 January loads, the row counts); `data_test()` asserts its severity and has a "what if you change it" cell; `run_tests()` is explained line by line; the ERP-refusal cell names its columns and closes its connection in `finally`. Write–audit–publish is four cells (write, the ERP's answer, audit, publish) with a predict-first cell on floating-point comparison. The freshness, lineage, contract and alert functions each have line-by-line explanations. 31 blocks run, 0 mismatches.
- **Freshness fixed.** A date column counts from midnight, so "under 24 hours" and "48 hours for weekends" were both wrong. The check now compares the newest date with the **previous working day** (a four-line helper, shown and run), prints the age in hours for people, and a new cell works out 30.5 h (Tuesday) and 78.5 h (Monday). The real-world fix and Answer 8 follow the same rule.
- **Money compared exactly.** The Flash revenue is rounded and stored as `DECIMAL(12,2)` on both sides, so the reconciliation can't fail on a fraction of a paisa; Answer 4 does the same.
- **The incident is closed.** The chapter now fixes 5 January and publishes it through write–audit–publish at the end of §47.9 (1 order, ₹18,750.00; freshness PASS). The alert is built from real results: both failed tests, "raw.dispatch (102 h old), mart.daily_flash (102 h old)", and the contract breach, with severity as a parameter.
- **Contracts check values too.** A second function checks blanks, repeats and whole numbers. On the 2 January file it finds `N/A` in `qty_units`, which the text turns into a contract conversation. dbt **model contracts** are taught in §47.7, with the real `dbt run` failure when a column is renamed; Answer 12 now points there.
- **Tools actually run.** The dbt YAML uses Ch 32's `data_tests:`/`arguments:` style, with a singular test, a real `dbt test` run (PASS=7), the compiled SQL of one test, and severity in dbt. An optional subsection runs the same status rule in Great Expectations 1.23.2 and Soda 4.25.0, and the claims about how they work are corrected (they report measurements, not failing rows).
- **Flash deadline** is now "sent by 7:30 a.m. IST" (coordinator, 29 Sep), matching Parts 0–3; the 6:30 run and every number stay the same.
- **Smaller fixes.** Four dimensions, not five; the 2026 date filter dropped (every 2025 order has lines); `file_day` introduced with `DESCRIBE raw.dispatch`; the dispatch staleness explained correctly; `statistics.median`; `upstream_of()` for the "Cause" question; S1/S2 no longer overlap; step 5 wording; DuckDB foreign keys only at CREATE TABLE; "four days earlier"; softened "most common incident"; drafting leftover removed; tools box and versions true.
- **Figures.** 47.1 and 47.2 redrawn on 720 px canvases (7.88 pt minimum, was 5.5–5.9 pt). Figure 47.1's branches are labelled in words, so nothing is clipped and nothing depends on colour.

## Skipped, and why

- **RJ-S2-18, Ch 47 part:** dating the real-world story on the book calendar and naming "the analytics engineer" need the Riverstone fact sheet, which isn't approved. Left `Open`.
- **47.18's optional extra** (reading the graph from Dagster's definitions) not added: this chapter no longer loads Dagster. The text says the graph is copied by hand and that Dagster draws it.
- Two code blocks stay longer than the teaching checker likes: the list of seven tests (each 3–4 lines of SQL already taught, explained test by test) and the alert formatter (split into a definition cell and a call cell; no new idea in it).

## Option picks

- 47.1: option (A), the previous working day (marked recommended).
- 47.13: option (a), add the Great Expectations and Soda box, run for real (no option marked).
- 47.27: option (a) in substance (teach dbt model contracts before citing them), placed in Ch 47 §47.7 rather than Ch 32, because Part 3 is closed. The literal alternative is in the questions file.
- 47.29: the first option, "four days earlier".
- 47.21: the first option, one sentence on routing the breach to its owner.
- 47.22: the first option, remove "or a critical output is unavailable".
- 47.4: round and cast both sides (the tolerance alternative was optional and not used).

## Time needed

12–16 hours → **14–18 hours over two to three weeks, in four sittings** (47.1–47.3; 47.4; 47.5–47.7; 47.8–47.10 and the project), as the review estimated. The chapter grew from about 28 to 45 pages: code cells went from 12 to 31 (plus the optional dbt, Great Expectations and Soda runs), each with its explanation.

## Code verification

- `verify_python.py manuscript/ch47-*.md --cwd companion/ch47`: 31 blocks run, 31 outputs checked, **0 mismatches** (Python 3.11.15, DuckDB 1.5.6, psycopg2 2.9.13, PostgreSQL 16.13).
- `checks/ch47_tools_check.py` (new): the chapter re-run with the two optional blocks switched on, in a virtual environment with Great Expectations 1.23.2 and Soda Core/soda-duckdb 4.25.0: 33 blocks, 33 outputs, **0 mismatches**.
- `checks/ch47_check.py`: all checks pass, including the new ones (weekdays of 2 Jan, 16 and 9 Nov, 13 Sep, 8 Jan; 78.5 h; ₹3,425.7375; no 2025 order without lines). The review's worked amount ₹3,425.4375 was wrong; the text uses ₹3,425.7375.
- dbt: `dbt test` (PASS=7) and the model-contract failure are real runs of a copy of the Ch 32 project against `riverstone_2025` (dbt Core 1.12.5, dbt-postgres 1.11.0, dbt_utils 1.4.1), shown trimmed and marked `run: none`.
- `verify_shell.py`: nothing to check (all terminal blocks are `run: none`); `verify_sql.py`: 0 mismatches. `check_code_teaching.py`: 40 blocks, 2 flagged (the deliberate exceptions above).
- `companion/ch47/ingest.py` was refreshed from Chapter 46's rewritten module (same functions; the dispatch loader's message now reads "5 rows (the day's rows replaced)").
