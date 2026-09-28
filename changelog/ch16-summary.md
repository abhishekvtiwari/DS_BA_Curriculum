# Chapter 16 summary: Business Intelligence with Power BI

**What changed.** The chapter now installs Power BI Desktop itself: a new §16.0 has the requirements, the Microsoft Store route (recommended, no admin rights), the Mac and Linux options, a tour of the screen, and a five-minute first report checked against the data. The model is built from one path, the `sales_lines` view, with every click and row count given. A CSV route sits in a box. Region comes from `city_region.csv`, labelled "City missing" as in Ch 15. The date table is built in five steps. DAX comes one measure at a time, each with its expected value. Row context, context transition, KEEPFILTERS and ALLSELECTED each get a worked example with a result. Time intelligence is shown as a January–June matrix. Four broken DAX items are fixed: the crore title format, Last Refreshed (now a refresh-time calculated table plus the data date), the RLS "no role sees all" claim (an All regions role was added), and the Answer 22 measure. Wrong chapter references are fixed, and no Python or pandas remains (D1). Every rupee amount uses lakh grouping. All six figures were redrawn at 7.3 pt or larger, with corrected content.

**Option picks.** Recommended or (a) throughout. Those that mattered: the `sales_lines` view path (16.5), quoting `'Date'` (16.8), a worked context-transition example (16.14), deleting the List.Dates option (16.32), and clearing the Q4 filter for Level 7 (16.34).

**Skipped or deviated.** 16.24 asked to mark Ex 3 as needing a work account. I didn't, because it's a licensing question that needs no Service. 16.1 asked for a screenshot of the Desktop screen, which can't be made here, so it's in the questions file. RJ-S3-17 is Ch 23's fix. No row was left Open.

**Time needed.** 22–26 hours over three weeks (was 18–22).

**Verification.**
- `verify_sql`: 7 statements, 7 outputs, 0 mismatches.
- `check_code_teaching`: 41 blocks, 0 flagged.
- `fig_check`: 0 figures under 7 pt.
- `restructure --check`: in order.
- `layout_check`: `map_numbers` 20/20, `toc_wrong` empty, no stranded heads or lead-ins, no small text, `tofu` 0. One page is 57% full: a figure page whose next list is kept with its lead-in. The `draft_labels` hits are reader text ("draft measures", "Treat generated DAX as a draft").
- Every DAX and visual number was recomputed with SQL in `checks/ch16_check.py`, and the CSV route was replayed with duckdb, giving the same totals.
- DAX behaviour follows Microsoft documentation, listed in the change log. learn.microsoft.com is blocked here, so those pages were read through search text. microsoft.com's download and pricing pages were fetched directly.
- Nothing in DAX could be executed.
