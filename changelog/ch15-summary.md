# Chapter 15, Data Visualization Principles: summary (Part 2 build)

**Result:** 43 register rows for Ch 15 (plus RJ-S1-5, which is held Open by the register and was not touched). 33 applied in this build (25 content, 8 visual), 9 layout rows already done by the style pass and re-checked here, 1 multi-chapter row left Open (RJ-S2-9). Rebuilt PDF: 48 pages, `layout_check.py` clean (no stranded headings or lead-ins, no sparse pages, no small text, no clipped lists, tofu 0, chapter map 21/21 numbered); `fig_check.py`: 0 figures under 7 pt; `restructure.py --check`: in order.

## What changed

- **Python moved to Ch 18** (approved decision). The §15.14 subsection "A first look at charts in code", exercise 22 and its answer, the `style_chart` stretch goal, the pandas clause of answer 13, and every "or Python" route were cut verbatim into `manuscript/_parked/ch15-moved-out.md` (nine blocks, each "→ Ch 18 §18.11" with what it depends on). §15.14 is now "Building charts in Excel and Google Sheets"; "Where this leads" says "Chapter 18 draws these charts in Python." Build scripts are no longer named as reader files.
- **Teaching gaps closed for a reader who knows spreadsheets and SQL but not statistics or Python:** quartiles worked by hand on nine real orders, then `QUARTILE.INC`/`MEDIAN` (with `FILTER` from Ch 11) for the three segments; `PERCENTILE_CONT` kept as an optional, fully explained PostgreSQL box; correlation and `=CORREL` defined before first use; `FLOOR` with a worked value; `GROUP BY 1` explained; the first query of the chapter and the target query each built in steps with real output.
- **New §15.15 "Running this chapter's SQL in MySQL"**, with real MySQL output, and `companion/ch15/ch15_queries_mysql.sql`.
- **Histogram:** the ₹25,000 query is now a coarse first look; the ₹5,000 query (29 bins, predict-first) is the main one, matching the chapter's own 20–40 bins advice.
- **Corrections:** the story's Q4 note (33% was October's uplift; Q4's was 29%); IQR is the box's length, not width; "Chapter 4 showed…" now matches Ch 4; ₹14.7 million → ₹1.47 crore; log-scale range fits Riverstone's data; Figure 15.2's footer matches the text; Ch 76 → 76B; "Appendix G" drafting note removed; lakh grouping for amounts ≥ ₹1,00,000.
- **Figures:** all 16 redrawn at print width. Smallest printed text is now 7.19 pt (Figure 15.2) and 7.6 pt (matplotlib figures), where it was 2–6.4 pt. Figures 15.15 and 15.16 (the project pack and its answer) are two per row with the fifth chart full width, and every label is readable; the "before" charts still show their bad choices. Figure 15.13 is 2 + 1, Anscombe 2 × 2, and the missing-city bucket is "City missing" everywhere. Three figures were moved after the text that introduces them, so no page is left a quarter empty.

## Skipped, and why

- **RJ-S2-9** (story date, "first week of January 2026"): needs the book calendar in the unapproved fact sheet → left Open.
- **15.4's preferred option** (teach `PERCENTILE_CONT` in Ch 13): Ch 13 isn't this agent's file. The finding's alternative was applied here and works whether or not Ch 13 changes. See questions.
- **Cross-chapter edits** passed to the integrator: Ch 14 "₹14.7 million" (15.20), Ch 16 "Region missing" (V15.16), a Ch 18 chart notebook (15.9).

## Option picks

15.4 alternative (spreadsheet route + optional SQL), because the preferred option needs Ch 13; 15.15 (a); 15.17 two cells in CTE form; 15.22 first wording, fitted to the real data range.

## Time needed

Unchanged at **12–15 hours over two weeks**. About an hour of Python was removed. About as much was added back: quartiles by hand, the correlation paragraph, the stepwise queries, the ₹5,000 histogram and the MySQL section. The review predicted this balance.

## Code verification

- `verify_sql.py`: 11 statements run (9 PostgreSQL, 2 MySQL), 11 outputs checked, **0 mismatches**. `verify_python.py` and `verify_shell.py`: no blocks left, as intended.
- `checks/ch15_spreadsheet_check.py` (LibreOffice 24.2 headless) confirms every spreadsheet result the chapter quotes: Palm Trading quartiles 19,292 / 25,865 / 39,975; segment quartiles (Wholesale 13,340 / 25,762.5 / 43,826.25); `CORREL` 0.9158; B14 0.98260; title "2025 finished at 98.3% of target"; Anscombe means 7.50 and correlations 0.816–0.817.
- The companion MySQL file was run end to end on `riverstone_full`, and all results match.
- `check_code_teaching.py` flags two repeats: the ₹5,000 histogram, which is the ₹25,000 query with one number changed, and the MySQL target query, which is §15.11's query with one function swapped. Both are explained through the difference from the earlier block. These are deliberate exceptions.
