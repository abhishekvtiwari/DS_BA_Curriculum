# Chapter 11 summary: The Spreadsheet, Mastered (Part 2 build)

**Findings handled:** 34 content (all applied, 11.29 verified with no change needed), 9 visual rows still Approved (V11.6–V11.13, V11.25: all fixed), 4 Reader's Journey rows (RJ-S2-9 left Open, RJ-S2-10 and RJ-S3-10 held Open by the reading order, RJ-S3-12 already fixed in Ch 6). The 17 visual rows the layout pass had already fixed or verified were rechecked in the rebuild.

## What changed
- **Load and pacing (11.1, 11.24):** Time needed is now **35–45 hours over five to six weeks** (was 25–30 h over three to four), with a 12-sitting plan and a core / second-pass split. The second-pass parts are marked where they start. The championship case (old §11.14) moved after the project as an optional **Timed challenge**, so the numbered sections are now 11.1–11.13.
- **No SQL before Chapter 12 (11.2, 11.17):** five SQL link boxes, the SQL column of Fig 11.3, the SQL recap bullet and the SQL-only warm-up are gone. QUERY is taught as a small query language on its own terms.
- **Code taught cell by cell (11.3, 11.13, 11.14, 11.19, 11.20, 11.23):** the SUMPRODUCT OR count in four cells with real results; the two-way lookup grid built before it's used; INDIRECT's text built in a cell first; REDUCE's offset subtraction shown on its own; the Stockroom minimum found first with conditional formatting, then with a formula explained piece by piece.
- **Runnable instructions (11.4, 11.5, 11.6):** §11.3's examples carry `Sales!`; the Power Query and the data model now live in one workbook (`ch11_practice.xlsx`) with checkpoints.
- **Correctness (11.8, 11.15, 11.22):** answer 33's formula double-counted (Hospitality 11); it's fixed and recomputed (9/8/6). The numbers-as-text rule is honest. Level 2's instructions no longer lead to wrong answers.
- **Chapter 4 follow-through (11.19):** the weighted average (SUMPRODUCT) and a "Back to Chapter 4" subsection (points vs percent change, rounded shares, the mode, the denominator) on `numbers_practice.xlsx`.
- **Function tables (11.11, 11.12):** every table has argument lists; the rarely used functions are in a reference card; ROW/ROWS/COLUMN are taught.
- **Figures (V11.6–V11.13):** all eight redrawn at print width, smallest text 7.2 pt (Fig 11.4: 8.6 pt). Fig 11.3 has no SQL, Fig 11.8 has a dashed second series, and Fig 11.4's notes moved into the text.
- **House rules:** lakh grouping for rupee amounts; Chapter 10 cross-references match Ch 10's new numbering; no forward references standing in for earlier chapters (Ch 3, Ch 4, Ch 15 now cited).

## Skipped, and why
- **RJ-S2-9** (stagger the story dates): this needs the book calendar in `review/riverstone-facts.md`, which isn't approved yet. Left Open.
- **11.1 alternative (split into 11 and 11A)** and **11.24's "consider moving Rewards to Ch 27/70"**: these are author decisions. The main fixes are applied instead.
- **Cross-chapter halves of 11.2 and 11.17** (the SQL pivot exercise and the back-pointing boxes in Ch 12/13): these belong to the Ch 12/13 agents and are listed for the integrator.

## Option picks
- 11.7: option (a), cutting the M block from the page and keeping it in the companion file. No option was marked recommended.
- 11.1: the main recommendation, restate the time and mark core and second pass. It is not the split.

## Verification
- `checks/ch11_fixes_tests.py`: 79 results computed by LibreOffice 24.2 headless and pandas on `ch11_practice.xlsx`, `month_end_pack_2025_messy.xlsx` and Chapter 4's `numbers_practice.xlsx`. Every result printed in the new text matches.
- The old answer-33 formula gives 6/8/11. The fixed one gives 6/8/9.
- Cell 3's 151 holds only with the status condition; without it the count is 153.
- XLOOKUP results can't run in LibreOffice 24.2, so they were checked with pandas.
- `check_code_teaching.py`: 75 blocks, 0 flagged. `verify_sql` and `verify_python`: nothing to run, because the chapter has no SQL or Python.
- `fig_check.py`: 0 figures under 7 pt. `restructure.py --check`: already in order.
- Build: 77 pages. `layout_check`: no stranded heads or lead-ins, no sparse pages, tofu 0, map 19/19, no draft labels. Its only `small_text` hits are the builder's "↩" continuation marks (6.3–6.9 pt), which is a shared-tool issue. `prescan`: nothing near the edges, no sparse pages.
