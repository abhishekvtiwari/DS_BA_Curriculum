# Chapter 46, Pipelines & Orchestration: summary

**What changed.** The chapter's design teaching is unchanged; its executable half was rebuilt so that every printed output comes from a real run and agrees with the prose.

- **The run-breaking bug is gone** (46.1): the practice CRM API now stays up until the last cell, so the retry demo succeeds on attempt 2, the bad-morning alert names only the check and the dispatch file, and the fixed re-run succeeds.
- **Set-up a beginner can follow** (46.2): practice folder, venv, `dagster==1.13.23` *and* `dagster-webserver==1.13.23`, a checked `dagster --version`, a fresh notebook.
- **Nothing hidden** (46.4): `ingest.py` is shown and walked through; the listings are tested against the file by `checks/ch46_check.py`.
- **One idea per cell** (46.10, 46.11, 46.14): the ingestion and Flash blocks are split into cells, each run and shown; the Flash's SQL is printed once filled in.
- **Correct concepts**: the schedule builds yesterday (shown by evaluating the 6:30 tick, 46.5); ingestion that syncs whole tables is now unpartitioned, while dispatch, Flash and delivery are per day (46.6); the transaction test crashes between DELETE and INSERT and shows the empty-day danger without a transaction (46.9); revenue rounded on both sides (46.12); bookings wording matches Ch 3/Ch 20 (46.13).
- **New, runnable**: a file sensor with `run_key` (46.16); fail-fast with `allow_retries=False` after a real demo of retries wasting four attempts on a 401 (46.18); labelled corrections (46.26); actionable per-step next steps (46.25).
- **Dagster's web interface for real** (46.3, 46.29): new `companion/ch46/riverstone_pipeline.py`, run with `dagster asset materialize` and `dagster dev`; the failure sensor fired and wrote its alert (shown). Running it exposed a DuckDB lock clash between parallel steps, fixed with `in_process_executor`.
- **Airflow 3** (46.23, 46.24): the DAG now targets Airflow 3 and was run with Airflow 3.3.2 (`airflow dags test`). A real Airflow 3 change was caught: plain cron strings now give a logical date equal to the run time, so the DAG uses `CronDataIntervalTimetable`, and the Watch-out explains it.
- Figures 46.1–46.4 redrawn at ≥ 7.46 pt, ✓/✗ marks instead of colour alone, ₹ instead of Rs, figure 46.3 matches what the reader actually sees.

**Skipped, and why.**
- RJ-S2-18 (Part 5's undated stories, scale, unnamed engineers): needs the book calendar and cast from the fact sheet, which isn't approved. Left Open.
- 46.3's "include one screenshot of the asset graph": no browser in this environment; the steps are in the text, and the screenshot is listed for Abhishek (V12).
- 46.31 (use thousands grouping) was overridden by the book-wide option pick 67.9: the chapter now uses lakh grouping throughout.

**Option picks.** 46.6: unpartitioned ingestion (the finding's "better still"). 46.7: prose + figure fix (a). 46.8: exclude `raw_dispatch` from the backfill. 46.22: add `ingest.run_sql`. 46.23: update to Airflow 3 (first option). 46.28: reuse Ch 45's table. 46.31: option 67.9 (lakh).

**Time needed.** 14–18 h → **16–20 h** over two to three weeks, in four sittings (46.1–46.3; 46.4–46.5; 46.6–46.7; 46.8–46.10 + project).

**Verification.**
- `tools/verify_python.py` (Python 3.14.7, Dagster 1.13.23, DuckDB 1.5.6, PostgreSQL 16, fresh database): 30 blocks run, 27 outputs checked, **0 mismatches**; no warnings on stderr.
- `tools/verify_shell.py`: 1 command, 0 mismatches. `checks/ch46_check.py`: all checks pass (arithmetic, time zones, listings = companion files).
- `riverstone_pipeline.py`: `dagster definitions validate` passed; `dagster asset materialize --select '*' --partition 2026-01-02` succeeded and wrote the Flash; under `dagster dev` a failing run triggered `flash_failure_alert`.
- Airflow DAG: `airflow dags test daily_flash_pipeline 2026-01-02` under Airflow 3.3.2 succeeded (all tasks; Flash 2 orders, ₹38,710.00).
- Build: 49 pages; `layout_check`: no stranded headings or lead-ins, no sparse pages, no small text, tofu 0, map numbers 16/16; `fig_check`: 0 figures under 7 pt; `restructure.py --check`: in order.
- `check_code_teaching.py`: 5 remaining flags, all deliberate: the three `ingest.py` listings (a file the reader reads, walked through bullet by bullet), the `riverstone_pipeline.py` excerpt, and the 39-line Airflow DAG (not run in the book, explained bullet by bullet).
