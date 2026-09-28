# Ch 28 summary — Advanced SQL, Performance & Data Modeling

**Rows:** 42 content + 19 visual + 6 Reader's Journey. Fixed/verified: all 42 content rows, all 19 visual rows, RJ-S3-28. Belong to other chapters (Ch 28 half needs nothing): RJ-S2-12 (Ch 32), RJ-S3-30 (Ch 33), RJ-S3-34 (appendix). Left Open: RJ-S2-15 and RJ-S2-16 (both need the unapproved Riverstone fact sheet).

## What changed
- **Recursion taught from zero (28.1, 28.10–28.12).** New first subsection "counting to five" with a pass table, the RECURSIVE keyword, anchor types, working table and stop rule; MySQL's 1,000-pass limit moved here; the parked Ch 13 date-spine block now lives here as "A list of months when there's no calendar table" (PostgreSQL error → CAST fix → MySQL Pattern 5 query); VALUES test data, all three loop defenses run in full, and a taught `SEARCH DEPTH FIRST` example.
- **Performance sections re-measured.** `riverstone_perf` was generated and loaded (PostgreSQL and MySQL); `ch28_perf.py` was rewritten to follow the chapter's order and re-run. Every plan and timing in §28.5, §28.6, §28.11, §28.13, Figures 28.3–28.4 and the real-world case now comes from that run, which is printed in `ch28_perf_log.txt`; a check confirms all 16 printed plans appear in the log. The machine is described honestly (4 vCPU, 16 GB, shared). Experiments 2, 3 and 6 are now complete (created indexes, labelled plans, the 4534 composite experiment, the write-cost SQL); a BUFFERS plan is explained.
- **Setup the reader can actually do (28.3, 28.4, 28.21).** A "Build riverstone_perf" box with every step and real output (psql located on each OS, flags explained, DBeaver fallback, MySQL route); migrations section shows the file contents, migrate.py's core in four pieces, PGUSER/PGPASSWORD, the `>>` edit and three real runs; the lab reset explains how to drop a database DBeaver still holds.
- **Correctness (28.2, 28.5).** The type 2 load now stores the next version's start in `valid_to` (a 31 March order proves the fix); failed migrations now show the aborted-transaction state and ROLLBACK.
- **Load (28.6, 28.13, 28.23, 28.26).** dim_customer built in five checked steps; frames in three cells; dim_date explained and checked; six sittings with stop points.
- **Recaps, not re-teaching (28.7–28.9).** NTILE (Ch 27 §27.4), percentiles (Ch 15 §15.5, Ch 21 §21.3), WINDOW (Ch 13 §13.6), star schema (Ch 16 §16.3).
- **Dialect table** completed (28.24); MySQL version facts updated with sources (28.25); IDENTITY instead of SERIAL (28.22).
- **Visual:** six figures redrawn at 7.4 pt minimum (star schema with visible spokes, plan at code size, B-tree "one branch shown", level/pass and material/assembly labels so colour isn't the only signal); Answer 15 output fits; QUERY PLAN rules trimmed; sargable table no longer wraps mid-token; three lead-ins split so none is stranded.

## Skipped and why
- RJ-S2-15, RJ-S2-16: need the fact sheet (regional sales team size; Part 3 story calendar). Questions filed.
- 28.7's Ch 13 half (teach NTILE in §13.4): not done; Ch 27 §27.4 now teaches it, so Ch 28 recaps from there.

## Option picks
28.28: "a customer new to this extract" (keep Coastal Foods; ids stated). 28.32: drop "(Chapter 29)". 28.11: defense 2 taught with a text path (works in both databases) rather than PostgreSQL arrays. 28.17: the (order_date, customer_id) sentence deleted rather than shown. Otherwise the finding's single recommended change.

## Time needed
18–24 h → **22–30 h including the project** (six sittings: 5–6, 5–6, 3, 5–6, 3, 4–6 h). Reason: the recursion introduction, the database build, split cells and complete experiments add material; the chapter is 105 pages (was 82).

## Verification
- `verify_sql.py --db riverstone_2025`: 92 statements, 83 outputs, **0 mismatches** (PostgreSQL and MySQL, including the stateful lab and a new MySQL lab region).
- `checks/ch28_check.py`: 60 checks pass (arithmetic, reconciliations against the database, timing ratios, 16 plans found verbatim in the log). `checks/ch28_build.py` rebuilds `dw` from the printed code; `ch28_star_schema.sql` regenerated from it (₹43,35,471, 326 lines).
- `verify_shell.py` / `verify_python.py`: nothing runnable (terminal and Python blocks are `run: none`; their outputs were captured from real runs of the generator, psql, and migrate.py).
- `check_code_teaching.py`: 32 of 130 blocks flagged by its keyword heuristic; the long ones (dim_date build, final dim_customer INSERT, fact load) are assembled from steps taught just before them. Accepted as exceptions.
- PDF (105 pages): layout_check clean (map 19/19, toc_wrong empty, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0; "coordinator" hits are Meera's job title). fig_check: 0 figures under 7 pt. restructure --check: already in order.
