# Ch 21 — Descriptive Statistics & Probability: summary

**Findings:** 54 rows (40 content, 14 visual). 40 content + 7 visual applied in this pass; 7 visual rows were already done by the style pass. None skipped.

**What changed**
- **By hand first.** New §21.0 "Seven deliveries, by hand": how to read Σ, xᵢ, x̄, μ, s and σ; mean, median, mode, range, a deviations table, variance (with why n − 1), SD, quartiles and IQR worked with a pencil. It uses Chapter 15's quartile method and shows that it agrees with `QUARTILE.INC` here. Then the same numbers in a spreadsheet and in pandas, and a "what if you change it" cell.
- **Formulas kept as promised.** Every measure now has a formula followed by an explanation in words: mean, variance, SD, IQR, CV, z-score, SE, binomial with C(n, k), Poisson with e and k!, and total probability.
- **Code taught cell by cell.** The big blocks are split: load, mode, branch summary with lambda and named aggregation, and sampling in three steps. The section now has 38 Python cells, and each is explained line by line.
- **scipy installed where it is first used** (§21.5), in the book's venv from Chapter 17.
- **scipy functions explained.** A "Four questions, four functions" table (pmf, pdf, cdf, ppf) and a binomial case worked by hand. Each call now has its spreadsheet equivalent.
- **Probability from counts.** A 2×2 count table and `pd.crosstab` come before the Boolean algebra. Bayes is now taught in the order counts → tree (new Figure 21.4) → named parts → total probability → formula → code.
- **Corrections:** 12% → 18%; the Poisson ppf label; the direction of the z-rule; the confusion of the inverse vs the base rate fallacy; Kolkata's share is 12.5%; broken cross-references to Ch 24, Ch 73 and the Parts; the Appendix G leftover.
- **Answers:** 10, 11, 17, 20, 23 and 26 now carry computed numbers. The two new checkpoints have answers.
- **Figures:** all four existing figures are redrawn at print width, with text at 7.5–9.2 pt. The labels in Figure 21.1 no longer collide, and the annotations in Figure 21.2 have their own column. There is a new Bayes tree figure (21.4); the CLT figure is now 21.5.
- **Also done here:** the Ch 21 halves of Ch 73 rows 73.13 (mutually exclusive, expected value) and 73.4 option (a) ("Two famous puzzles").

**Option picks:** the full formula set for 21.1 (not the fallback). 73.4 uses (a), the recommended option. Everywhere else the finding's recommended change was applied. In three places I placed the content differently from the finding, and noted why in the changelog: the data dictionary goes in §21.1, the scipy install goes at its first use in §21.5, and the expected value goes in §21.5 rather than §21.1 (sequence test).

**Real data surprise:** the order-value mode is a tie between ₹1,725 and ₹5,800, 219 orders each. pandas lists ₹1,725 first, but `MODE.SNGL` returns ₹5,800 (checked in LibreOffice). The chapter now says so, and answer 7 and the timed-challenge answer say so too.

**Time needed:** 15–18 h → **20–23 h** over three weeks, in two halves of about 9 h and 12 h. The chapter grew from 25 to 45 PDF pages, mostly with the hand-worked section, the cell-by-cell code and its outputs. `tools/hours_table.py` reads 20–23.

**Verification:**
- `verify_python`: 38 blocks run, 38 outputs checked, 0 mismatches.
- `verify_sql` on `riverstone_full`: 1/1 correct, 0 mismatches.
- Every spreadsheet result was recalculated in LibreOffice.
- `check_code_teaching`: 41 blocks, 0 flagged.
- `restructure --check`: in order.
- `fig_check`, plus the figure script's own size report: 0 figures under 7 pt.
- `layout_check`: map 16/16, with no stranded headings or lead-ins, no sparse pages, no small text, no draft labels and tofu 0.
- `prescan`: clean. The only hyphen breaks are at real hyphens.
