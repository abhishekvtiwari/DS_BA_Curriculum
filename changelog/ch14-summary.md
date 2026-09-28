# Chapter 14, Data Cleaning & Preparation: summary of the Part 2 build

**Reading position:** after Ch 10, 11, 19, 12, 13. The reader knows spreadsheets, Power Query and SQL, and no Python yet.

## What changed
- **Python out.** §14.13 "A first look at cleaning in pandas" and every other pandas mention (a table column, five clauses, two Tools lines, a project step, Check yourself, Exercise 23) moved verbatim to `manuscript/_parked/ch14-moved-out.md` for Ch 18 §18.10. Ch 14 now points to Ch 18 in "Where this leads".
- **Loading without a terminal.** §14.1 now uses DBeaver steps: create `riverstone_full`, run the setup script, run the Ch 14 load script, and check two counts. The Ch 14 load scripts are now self-contained INSERT scripts that DBeaver can run. The terminal versions are kept for the Ch 26 §26.0 exercise.
- **Regular expressions taught before use.** A new §14.2 subsection, "Patterns in ten minutes", has a table of 9 tokens and 4 runnable cells.
- **The pipeline is shown, not just referred to.** A new **§14.9 "The whole pipeline in SQL"** prints and explains the whole cleaning script, with row-count checks. The old §14.9–14.12 became §14.10–14.13.
- **Fragments made runnable.** The date parsing (3 cells), the mapping table (2 cells), the match key, units, discounts, time-zone conversion and a fill-down window example are all now runnable with real output. Every one-line query is reformatted one clause per line. GROUP BY 1, NULLIF, casts, USING, VALUES, STRING_AGG, EXCEPT and timestamptz are explained at first use.
- **Reconciliation in SQL.** An `EXCEPT` query against `truth_order_lines` shows that exactly 20 lines differ, all of them quarantined, each with a true quantity one tenth of the exported one. This replaces the Python check script. `sql/ch14_compare_clean.sql` is shipped.
- **One tool per idea.** SQL is the teaching path in §14.2–14.11. The spreadsheet material is gathered in §14.12, which now explains every M function and shows before/after rows. Time needed stays at 20–25 h, with a new 3-week plan.
- **Corrections:**
  - the footer/distinct-ID reason;
  - the 85–90 lines are Hospitality lines, not Wholesale crates;
  - the "slip of a key" and "web portal" wording;
  - PostgreSQL has no `IGNORE NULLS`;
  - MySQL grouping now uses `COLLATE utf8mb4_0900_bin`, because `BINARY` is deprecated and `utf8mb4_bin` would hide trailing spaces;
  - the log counts are shown to be exact;
  - Chapter 76 → 76B;
  - the draft Appendix G note is removed;
  - the report-gap placeholder is replaced with model wording;
  - references to Ch 10, 12 and 13 now match their rebuilt numbering;
  - rupee amounts use lakh grouping, and "₹14.7 million" etc. now read in crore/lakh.
- **Figures:**
  - 14.1 is redrawn as 2×3, with the loop pointing to Profile;
  - 14.2 and 14.3 are redrawn at 700 px, and 14.3's steps are in code order;
  - 14.4 is enlarged.

  All text is now ≥ 7 pt (the smallest is 7.06 pt).
- **Companion:**
  - the exports are regenerated, which restores the CRLF line endings;
  - the map CSVs now use `raw_value`/`clean_value`, and a new `branch_map.csv` is added;
  - a second export (Q3 2025) is added for the stretch goal;
  - a SQL-script builder is added.

## Option picks
- 14.13: (a), a worked SQL fill-down example.
- 14.15: (a), a product whose history reaches 90.
- 14.30: (a), ship `branch_map.csv`.

None of the three had a recommended option.

## Skipped or left open
- **14.32:** held Open by the register. It is now moot, because the pandas column is gone.
- **RJ-S2-9:** the story date depends on the unapproved fact-sheet calendar. Open, with a question.
- **RJ rows whose fix is elsewhere** (S2-7 rest, S2-15, S3-18 rest, S3-22, S3-24, S3-34, S3-78): left Approved for their chapters.
- **Integrator needed:**
  - `companion/full` setup scripts need DBeaver-runnable versions. They are generated and verified in `scratchpad/part23/ch14-for-integrator/`.
  - Ch 16 and Ch 27 cite renumbered sections.

## Verification
- `verify_sql.py`: 55 statements, 54 outputs checked, **0 mismatches** (PostgreSQL and MySQL, database `scratch_ch14` = `riverstone_full` + Ch 14 scripts).
- `fig_check.py`: 0 figures under 7 pt.
- `layout_check.py`: clean. The contents map is 19/19, and there are no stranded headings, sparse pages or tofu.
- `restructure.py --check`: in order.
- The cleaning script was reformatted; its results are identical to the old script (EXCEPT ALL both ways = 0).
- The Q3 stretch goal was tested.
- Power Query and DBeaver could not be run here.

**Status:** 32 Fixed/Verified content rows, 12 visual rows Verified, 2 Open, 7 left Approved for other chapters. See `changelog/ch14.md`.
