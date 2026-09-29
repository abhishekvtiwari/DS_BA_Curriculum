# Chapter 35, The Math Under the Models: summary (Parts 4–8 build)

**Result:** all 37 content findings (35.1–35.37) and all open visual findings applied; nothing skipped. Rebuilt PDF: 57 pages (was 44), clean layout check (map 17/17, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0), 0 figures under 7 pt, stage order confirmed by `restructure.py --check`.

## What changed

- **scikit-learn installed just in time** in a new §35.9 subsection, right before its first use: venv, `python -m pip install scikit-learn`, `requirements.txt`, a version cell (1.9.1). Its two uses (log loss, PCA) are explained line by line, including the reader's first `.fit()`.
- **Builds on earlier chapters instead of re-teaching:** NumPy points to Ch 18 §18.1; distributions now use `scipy.stats` as in Ch 21 §21.5; logs start from Ch 31 §31.0 and add only what probabilities need (negative logs, power rule, ln 0, log₂); least squares links to Ch 22 §22.10, with a table for the letter clash (slope *b* there, *w* here).
- **Steps that were stated are now built:** the slope formula (from nudging a square), the closed-form best *w*, matrix × matrix and the shape rule, entropy from "surprise", and the eigenvector (try directions, then check "stretch without turning").
- **Code taught like Jupyter:** big blocks split (cosine 2 cells, weekly counts 2 cells, small PCA 4 cells, standardized PCA 4 cells), new cells for the valley, the gradient in matrix form, matrix × matrix, logs, the learning-rate plot and the sklearn install. `descend` now takes `y_values`. Every output is from a real run.
- **Story fixed:** Meera's vendor check now uses Riverstone's full CRM (7.3% win rate on matured 2025 leads). "Always no" is 92.7% accurate, better than the vendor's 91%, and the benchmark log loss is 0.26. All of these are recomputed by `checks/ch35_check.py`.
- **Figures:** all six redrawn at ≥ 7.46 pt. A new Figure 35.2 shows the loss valley, so the later figures are renumbered 35.3–35.7. The PCA scatter uses shapes as well as colours, and the overlapping labels are fixed.
- **Polish:** Appendix G leftover removed; accuracy and threshold defined; lakh grouping in prose; Bernoulli box on two lines; long formulas broken at "=".

## Option picks

- 35.14: option (a), switch to `scipy.stats`.
- 35.3: sub-points (a)–(e), as written.
- 35.1: the finding pins scikit-learn 1.8.0. This machine has 1.9.1, so the text says the outputs were checked on 1.9.1. That is the version actually run, so no version was invented.

## Skipped, or left for elsewhere

- **RJ-S3-41** (resolve the vendor pilot): nothing to change in Ch 35. Ch 36 §36.1 now picks up the running pilot; its outcome belongs in Ch 39.
- **RJ-S2-15 and RJ-S2-16** are `Open` in the register, so they were not touched. The story now does say that the full CRM differs from the one-year database.
- **35.1's extra row in Ch 17's package table** is in another chapter. It is listed for the integrator.

## Time needed

Was 10–14 h over two weeks. Now **14–17 h over two to three weeks**, in four sittings: A §35.1–35.3 about 3 h; B §35.4–35.6 about 4 h; C §35.7–35.9 about 4 h; D §35.10–35.11 about 3 h; then the project. The chapter grew by about 13 pages: the logs facts, the derivative build-up, matrix × matrix, the eigen check, the install, and the split cells. That added load matches the review's estimate of about 3 hours.

## Verification

- `verify_python.py`: 45 blocks run, 43 outputs checked, **0 mismatches**. The two blocks without output are matplotlib `plt.show()` cells.
- `check_code_teaching.py`: 46 blocks, 0 flagged.
- `checks/ch35_check.py`: all checks pass, including the new ones (valley, §22.10 sums, checkpoints, Poisson hand rows, logs, try-directions, CRM story figures).
- `verify_shell.py`: no shell outputs to check (the install block is `bash`, with nothing printed).
