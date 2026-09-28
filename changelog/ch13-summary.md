# Chapter 13, SQL for Real Analysis: summary of the Part 2 build

**Findings handled:** 27 content (13.1–13.27), 6 visual (V13.2–V13.5, V13.14, V13.19), 5 Reader's Journey rows.
Fixed or verified: all 27 content rows and all 6 visual rows. Reader's Journey: 1 fixed here (RJ-S3-15, Ch 13 half),
3 belong to other chapters (RJ-S1-9 → Ch 23, RJ-S3-23 → Ch 25, RJ-S3-32 → Ch 30), 1 left Open (RJ-S2-9).

## What changed

- **Recursive CTEs moved out (13.1).** The date spine now uses two calendar tables (`calendar_months`, `calendar_days`),
  created by new companion files and loaded into `riverstone_2025`. Pattern 5, the MySQL section and exercise 16 use them.
  The recursive-CTE material is parked for Ch 28.
- **Missing demonstrations added.** Ch 12's nested "before" query (13.6), the view's output, a row-count check and the
  "already exists" case (13.5), temporary tables in three cells (13.4), `SUM(SUM()) OVER ()` (13.7), `LEAD` (13.22),
  and the `sales_targets` columns (13.13). Every output is real.
- **Order and load.** §13.6 now runs MoM → moving average → running total (explicit `ROWS` frame) → frame trap (13.2).
  The pattern library is split into §13.7 (Patterns 1–4) and §13.8 (Patterns 5–10), and MySQL is now §13.9, with
  "Stop here" exercise checkpoints (13.8). Pattern 7 is built in three checked steps (13.9).
- **Correctness.** The 80% claim (13.3), 80.04% (13.14), `LAG(…, 12)` with no 0 default (13.12), `COUNT(DISTINCT lead_id)`
  (13.16), `order_days` (13.18), the MySQL date-subtraction trap in ageing (13.10), answer 15 (13.27), and 175 vs 173
  orders stated explicitly.
- **Polish.** Magic IDs looked up (13.19), `b.*`, simple CASE, INTERVAL and `::date` explained (13.23, 13.16, 13.17),
  cancelled orders in "latest order" (13.21), Tools list trimmed (13.24, 13.25), the Appendix G leftover gone (13.26).
- **Figures.** All four were redrawn on 720 px canvases, with the smallest text at 7.2 pt (it was 5.2–5.6 pt). The frame
  labels were corrected, the table border was closed, and the island IDs are now printed, not shown by colour only.
  Rupee amounts use lakh grouping.

## Skipped or changed from the finding, and why

- **RJ-S2-9 (story dates) left Open.** It needs the book calendar in the unapproved Riverstone fact sheet.
- **13.8, deviation.** Pattern 10 stays at the end of §13.8 instead of joining §13.7. Other chapters (8, 20, 25, 28, 29)
  cite pattern numbers, so the numbers were kept stable. See the questions file.
- **13.15.** Used the finding's second alternative (a sentence), not the planted upper-case email. Planting it would change
  shared data and the lead counts in Ch 23 and Ch 29.
- **13.22.** `LEAD` got its own cell rather than a sixth column, so each cell has one idea and the output fits the page.
- **13.24.** The Ch 16 back-pointer box is for the Ch 16 agent.

## Option picks

V13.4: (a) enlarge (kept the figure). V13.19: both (row labels and a bracket). 13.15: second alternative (reason above).
67.9: lakh grouping.

## Time needed

It stays at **15–20 hours over three weeks**, now with a sitting plan (Week 1: 13.1–13.5; Week 2: 13.6–13.7; Week 3:
13.8–13.9 and the project). The additions (about 12 short cells) are partly offset by removing the recursive CTE, its
watch-out and the recursive exercise. Net, about one more hour of reading and practice, which fits inside the stated range.

## Verification

- `tools/verify_sql.py manuscript/ch13-*.md`: **56 statements run, 56 outputs checked, 0 mismatches**. This covers both
  engines and the `riverstone` / `riverstone_2025` markers.
- `checks/ch13_check.py`: the session-dependent demos (temp table, view created twice, MySQL spellings, calendar tables).
  **8 of 8 pass.**
- `companion/ch13/make_mysql_queries.py` regenerated `companion/mysql/ch13_queries_mysql.sql` from the chapter and
  compared every MySQL result with the chapter's printed output: **55 compared, 0 mismatches**. The whole file runs clean.
- `tools/pdf/fig_check.py`: 0 figures under 7 pt. `tools/restructure.py --check`: already in order.
- Rebuilt PDF (59 pages): `layout_check.py` and `prescan.py` are clean. There are no stranded heads or lead-ins, no sparse
  pages, no small text and no tofu, and the map numbers are 15/15. `check_code_teaching.py` still flags 19 of 60 blocks
  with its keyword heuristic (it flagged 17 of 45 before) (every line of those blocks is explained in prose or bullets).
