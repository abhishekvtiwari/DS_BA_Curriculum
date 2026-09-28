# Ch 32 — Analytics Engineering with dbt: summary

**Result:** 35 of the 38 content rows fixed (32 Verified, 3 Fixed), 3 held Open for reading order (32.1, 32.17, 32.24). RJ-S2-12 fixed and verified. Visual: V32.1–V32.3 redrawn and verified; V32.4–V32.13 (style pass) confirmed in the rebuilt PDF. Rebuilt PDF: 48 pages (was 35), layout check clean (no stranded heads or lead-ins, no sparse pages, no small text, map 19/19, tofu 0).

## What changed
- **The chapter is now a build-along a first-timer can finish.** Every build runs on exactly the files written so far, and every output is real (dbt Core 1.12.5, dbt-postgres 1.11.0, SQLFluff 4.3.0, Python 3.14.7, PostgreSQL 16, run 28 Sep 2026). Install is `mkdir` → `uv init --bare` → `uv add` → activate → `dbt --version`. The macro file is created in §32.3, where it's first used. The snapshot and `dim_customer` come before the fact table in §32.5, whose first `dbt build` shows the real 13 nodes. The finished project's 37-node build closes §32.12.
- **Missing pieces added:** the `raw_crm.customers` stand-in (new `companion/ch32/setup_raw_crm.sql`, with psql taught at first use), `stg_products`, the staging `schema.yml`, file paths on every block, and a `ci` target in `profiles.yml`.
- **New primers where they're first needed:** "Jinja in two minutes" (§32.2) and "YAML, part 2" (§32.3). There are also line-by-line lists for `profiles.yml`, `dbt_project.yml`, `sources.yml`, the snapshot, the macro, the Jinja loop (with its real compiled output), `.sqlfluff` and the CI workflow.
- **Consistency with Ch 28:** a real query now shows that the totals match but Metro Mart's city history doesn't. The snapshot demo uses Evergreen Mart (no Ch 28 history, a segment change) and says the date is the day you run it (RJ-S2-12).
- **Correctness:**
  - the incremental timings are re-measured (2.19 s against 0.55 s, about four times, not 13.91 s against 0.90 s);
  - the full SQLFluff output is shown: 10 violations, with `fix` and a clean re-lint;
  - answer 12 (incremental fact plus a per-day drift test) is rewritten and tested;
  - answers 2, 11 and 15 are corrected (the `target/run` wrapper, the `__dbt__cte__` name, the last order on 23 December);
  - `--profiles-dir .` is gone, because dbt reads `profiles.yml` from the current folder (documented), so the exercises now run as written;
  - the password lives in a `.env` file (Ch 34's rule).
- **Figures 32.1–32.3 redrawn** at 7.4–8.6 pt. 32.1 now matches the code, with arrows and no edge crossing a label. 32.3 uses ✗/✓ and FAIL/SKIPPED.
- **Companion:** the project is synced with the tested files. `stg_customers` is removed, and `mart_sales_monthly`, the `ci` target, a README, `pyproject.toml` and `requirements-pinned.txt` are added. `checks/ch32_check.py` is rewritten and passes 27 checks.

## Skipped, and why
- **32.1, 32.17, 32.24: held Open** (`review/reading-order-conflicts.md`). Ch 34 now precedes Ch 32, so its references stay.
- **32.24's defects are real under any order.** The CI workflow still calls an unshown `./load_test_data.sh`, gives psql no `PGPASSWORD`, and lints before `dbt deps`. These are raised as a question for Abhishek.

## Option picks
- 32.8: (a), a companion SQL file.
- 32.9: (b), first alternative: the snapshot and `dim_customer` move before the fact.
- 32.12: (a), drop `stg_customers`.
- 32.23: (a), add a `ci` output.
- 32.30: correct the wrong date (the data has no orders after 23 December).
- 32.6/32.32: modified. dbt's documented current-folder lookup replaces `export DBT_PROFILES_DIR=.`; same outcome.

## Time needed
Was 16–22 h. **Now 18–22 hours over three weeks**, in four sittings (5–6, 4–5, 4–5, and 5–6 h for the project), as 32.36 asked. The chapter grew from 35 to 48 pages, mostly from real outputs and the line-by-line lists.

## Verification
- `verify_sql.py --db riverstone_2025`: 5 statements, 5 outputs, 0 mismatches.
- Terminal blocks are `run: none`. dbt prints clock times and timings, so they can't be compared; each was pasted from a real run, and the logs are kept in the scratch folder.
- `ch32_check.py`: 27 checks pass. They cover 326 lines and ₹43,35,471, 132 days, December ₹4,39,823.50, and 1,096 days on `riverstone_perf`.
- `check_code_teaching.py`: 6 soft flags remain, on answer blocks and short config-style blocks.
- `fig_check.py`: 0 figures under 7 pt.
- `restructure.py --check`: in order.
- The chapter map is numbered 19/19.
- Mismatches left: none.
