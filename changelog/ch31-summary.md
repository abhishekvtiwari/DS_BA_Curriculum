# Chapter 31 summary: Causal Inference Without Experiments

**Findings handled:** 52 rows (37 content, 11 visual, 4 Reader's Journey). 34 Verified, 14 Fixed, 3 Approved (their remaining half belongs elsewhere), 1 Open (RJ-S2-16, story calendar). V31.12/V31.13 were already fixed by the style pass.

## What changed
- **New §31.0 "Logs in ten minutes"** (31.2): ln turns multiplying into adding; by hand with North's 2,032 → 2,067; `LN`/`EXP` in a spreadsheet; `np.log`/`np.exp`; where the shortcut breaks (0.56 is +75%, not +56%); why DiD works in logs.
- **Section order (31.36):** synthetic control moved up to §31.5, straight after DiD and parallel trends, so the chapter reads in two parts: **A, comparisons over time** (§31.0–31.5, ends with a by-hand DiD checkpoint) and **B, comparisons across units** (§31.6 matching, §31.7 RD, §31.8 IV, §31.9 trust). Figures renumbered and renamed to stay in page order (31.2 synthetic, 31.3 balance, 31.4 RD).
- **Every big block split and taught** (31.3, 31.4, 31.8, 31.12, 31.13, 31.18, 31.19, 31.21): dummy table and coefficient-to-cell map for the DiD regression; fixed effects in three cells with "absorbed" explained; pre-trend drift with §22.10's `linregress`; logistic score worked by hand to the same 0.3351 as `predict`; a paper matching example, then four matching cells (with `itertuples`, Ch 18's advice); RD lines written out; bunching bins `right=False`; synthetic control built by hand in a spreadsheet (loss 0.0192 → 0.0044, Solver), then pandas, then `@`, then `minimize` argument by argument.
- **Numbers corrected** against the chapter's own output: 1.6× not "twice"; +75% (log) vs +72% (plain); "last three" months; quarter −1 dip stated honestly; drift "about a third"; ~0.75%/month growth; West 1.6× North; answer 2's mix shift; margin **up** (~14% gross profit at Riverstone's 26.2% margin), not flat; answer 8's "two points high"; answer 11's "first of two".
- **Regression adjustment now includes segment** (31.14): +7.7% → **+7.5%** (CI +4.4% to +10.7%); sensitivity (31.17) is now demonstrated: dropping prior size gives +75.1%, dropping growth +8.7%.
- **Answer 13** uses `treated:t` (no rank-deficiency warning): −4.8% (CI −10.5% to +1.3%).
- **Reader-facing:** Appendix G line and `ch31_check.py` gone from reader text; broken cross-references fixed (Ch 43, 19, 55, 69, 73, Ch 3's non-existent free-delivery rule); format-spec box; data setup cell and column tables; "Chapter 30 installed/Chapter 17's pandas" prerequisites replaced; Anita Rao (Sales Head) instead of an unnamed "sales director".
- **Figures** redrawn at 700 px (min 7.4 pt), every number computed from the data in `make_figs31.py`; hollow/filled shapes plus colour; axis titles; real minus signs; evidence labels in text; footnote duplicating the caption removed.

## Skipped, and why
- **RJ-S2-16:** the April 2026 board-meeting date stays until the book calendar in the fact sheet is approved.
- **RJ-S3-35, RJ-S3-34, RJ-S2-12:** Ch 31's part done; the bible, an appendix dataset list and Ch 32 hold the rest.

## Option picks
31.8 `linregress`; 31.14 add segment; 31.19 `right=False`; 31.20 introduce the rule here (Ch 3 not edited); 31.22 `round(float(...))`; 31.26 26.2% gross margin (Ch 4/§11.6); 31.29 delete the Ch 43 bullet; 31.32 `treated:t`; 31.33 remove from reader list.

## Time needed
Was 10–14 hours over two weeks; now **15–18 hours over two and a half weeks, in two parts** (~8 h + ~8 h + 2 h project), the review's estimate, because of §31.0, the by-hand steps and the split cells.

## Verification
- `verify_python.py`: 59 blocks run, 59 outputs checked, **0 mismatches** (Python 3.11.15, pandas 3.0.6, numpy 2.4.6, scipy 1.17.1, statsmodels 0.15.0).
- `verify_shell.py`: 2 commands, 0 mismatches (run in a fresh `companion/ch31`).
- Spreadsheet formulas (LN/EXP, blend, loss 0.0192 and 0.0044, logistic 0.3351) recalculated in LibreOffice headless.
- `checks/ch31_check.py`: 34 checks pass (new checks for the margin, sensitivity, losses, §31.0 numbers).
- `fig_check.py`: 0 figures under 7 pt. `restructure.py --check`: in order. `layout_check.py`: map 16/16, no stranded heads/lead-ins, no sparse pages, no small text, tofu 0, no draft labels; 49 pages.
