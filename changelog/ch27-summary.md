# Ch 27 — Capstone: Your Analyst Portfolio: summary

**What changed.** Every number the capstone prints now comes from code shown in the chapter and run on `riverstone_full`: a reconciliation query (46,356 orders and ₹1,14,66,41,651.25, both ways), a profiling query for the cleaning table, the duplicate merge as two SQL cells, the Wholesale t-test / CI / correlation as three Python cells, a margin-by-segment query, and answer 5's composition as a Python cell. `NTILE` is taught as new on nine hand-countable rows (nothing in Part 2 taught it). The merged/as-loaded contradiction is resolved as a recorded decision (option B). The script is named (`discount_analysis.py`), reads `companion/full/` and is shown run both from the terminal and imported into a notebook; a check cell shows the table first. A within-Retail check (median split, 9.5 vs 9.1 orders) closes the analytical gap; memo, dashboard, FINDINGS and answers follow it. About twelve section references fixed for the renumbered Ch 12, 14, 17, 18, 22 and 15; the rest re-checked. Three figures redrawn at ≥ 7.4 pt. Tools line defers to Ch 17's Python rule.

**Option picks.** 27.1 minimum alternative (teach in §27.4); 27.4 option B; 27.9 Retail median what-if + dashboard object change; 27.17 keep `>= 5` and record it; 27.18 align with Ch 9's question; V27.4 redraw (not drop).

**New Time needed.** Reading and running the worked project 2–3 h (about ten more cells than before); own portfolio 20–30 h over one to two weeks, deep project alone 8–12 h (27.23).

**Code verification.** `verify_sql.py --db riverstone_full`: 10 statements, 10 outputs, 0 mismatches. `verify_python.py --cwd companion/ch27`: 13 blocks, 12 outputs, 0 mismatches (fresh-namespace import of the companion module included). `verify_shell.py --cwd .`: 2 commands, 0 mismatches. All 10 SQL blocks also re-run on MySQL 8 (with `YEAR()`/`CAST … AS SIGNED`), identical results. `restructure.py --check`: in order. `fig_check`: 0 under 7 pt. `layout_check` / prescan on the 39-page build: clean.

**References checked** (current files): Ch 3 §3.6; Ch 12 §12.6, 12.8, 12.9, 12.10, 12.12; Ch 13 §13.2, 13.3, 13.4; Ch 14 §14.4, 14.11; Ch 15 §15.11; Ch 17 §17.8, 17.11, 17.12; Ch 18 §18.1, 18.2, 18.3, 18.4, 18.9, 18.13; Ch 22 §22.1–22.5, 22.8; Ch 24 §24.4; Ch 26 §26.9, 26.11 (Ch 26 is being rebuilt: see questions file).

**Skipped / left.** RJ-S2-7 (Where-this-leads chapter numbers) belongs to the final renumbering pass. No row left Open. The memo date (12 February 2026) is untouched pending the fact sheet.
