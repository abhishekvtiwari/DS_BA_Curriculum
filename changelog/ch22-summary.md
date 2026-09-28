# Ch 22 — Statistics Without Fooling Yourself: summary

**What changed.** All 32 content findings and the 7 visual findings still open are applied. Every technique now follows the book's order: idea, then by hand, then spreadsheet, then Python.
- Formula boxes cover the t-distribution, the chi-square test, the power formula, correlation and Benjamini-Hochberg.
- Big code blocks are split into Jupyter-style cells, each explained line by line.
- The A/B write-up is now consistent: open rate is the pre-declared primary metric (22.9, option A).
- statsmodels is installed in §22.2 and used for the z-test.
- New bootstrap and real-data regression-to-the-mean cells.

A new **§22.10 "Fitting a line: regression basics"** (decision D3) teaches:
- slope, intercept, least squares, residuals and R², by hand on six customers;
- the same in a spreadsheet (checked in LibreOffice) and in Python (`linregress`, slope CI, residual plot);
- the real customer table (₹26,700 per order, R² 0.84);
- a 0/1 dummy for Kolkata (slope = difference in means = t-test);
- honest reading, and one paragraph on multiple regression.

It comes with new exercises, Key terms, Recap, Check yourself, Common mistakes and a timed-challenge level.

All six figures are redrawn at print width, with text of at least 7.7 pt and no colour-only meaning; two are new (Fig 22.5 correlation, Fig 22.6 regression line). There is a new companion workbook, `companion/ch22/ch22_by_hand.xlsx`, built by `build_ch22_workbook.py`.

**Skipped, and why.**
- 22.5's optional permutation cell: Figure 22.2 already shows the null by simulation.
- 22.30(m): the edits it asks for in Ch 30, 31, 37 and 53 belong to other chapters, so they are handed to the integrator.
- RJ-S2-9 stays Open, because it needs the unapproved Riverstone calendar.

**Option picks.**
- 22.9: A (recommended).
- 22.10: install statsmodels.
- 22.14: 4,500 tests.
- 22.22: ±1.6.

**Time needed.** Was 15–18 h. It is now **20–23 hours over two and a half weeks**, in two parts:
- Part A (§22.1–22.4), about 11 h;
- Part B (§22.5–22.10), about 10 h, of which §22.10 is about 4 h;
- the project, about 2 h more.

**Verification.**
- `verify_python.py`: 46 blocks run, 45 outputs checked, **0 mismatches**. Every output was pasted from a real run.
- `check_code_teaching.py`: 0 flagged.
- `restructure.py --check`: in order.
- The figure sizes were measured in `make_figs22.py`: the smallest text prints at 7.69 pt.
- The rebuilt PDF (53 pages, was 26):
  - `layout_check` is clean: map_numbers 16/16, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0;
  - prescan shows no text near the edge.
- Answer numbers were recomputed: 2, 11, 14, 16 (now 31% at 30 checkpoints, was 27%), 19, 20, 21, 23, 24, 25, 28 (power 18%) and 31, and the checkpoint.
