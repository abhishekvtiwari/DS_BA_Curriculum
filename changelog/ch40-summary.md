# Chapter 40 · Time Series & Forecasting · summary

**Result:** all 43 content findings and the 13 open visual findings applied; the Ch 40 part of RJ-S3-40 done; RJ-S3-46 needs nothing in this chapter. Nothing left `Open`. Rebuilt PDF: 52 pages (was 37), layout check clean, every figure at 7.2 pt or more. Details line by line: `changelog/ch40.md`.

## What changed

- **Setting up (new §40.0).** The reader runs the two seeded generators from `companion/ch40/` and sees their real output; Prophet is installed in a shown terminal step in §40.5, just before it is first used.
- **First-time reader.** Hand-worked examples before every new tool: a decomposition on a two-year quarterly toy, autocorrelation on six numbers (r = 0.30 by hand, `CORREL`, `autocorr`), differencing on five numbers, WAPE and MAPE on three months, a 3-month moving average, one Holt step, MASE on the toy, and the exponentially weighted mean in words. AIC, the SARIMAX summary table, the ADF statistic, PACF and the ±2/√n band are now defined where they're used, each pointing back to the chapter that taught the underlying idea (§22.1, §22.2, §22.5, §30.11, §35.8).
- **Code taught like Jupyter.** The big blocks (data load, ML features, backtest, anomaly rules, answer 12) are split into cells with output after each and line-by-line explanations; 55 blocks, 0 flagged by the teaching check.
- **Correctness.** Residual bug fixed (largest deviation is 36.8% in May 2020, not "1.249 in Feb 2020"); trend "about 60%", Holt–Winters "7–20% below", October 40% / November 30%; the airline model named correctly; over-differencing diagnosed (MA ≈ −1) and tested in exercise 7 (d = 0 with a constant scores 3.9%); week-to-month bookkeeping shown (true weekly units summed by Monday are 9.5% off the monthly series); heater timeline printed minute by minute; answer 13's Monday alerts traced to an immature baseline and checked with `min_periods=1440`; answers 2, 7, 10, 11 and 12 rewritten to match what the code shows (answer 12 now compares like with like).
- **Warnings shown, not silenced.** The global `warnings.filterwarnings("ignore")` is gone; the statsmodels and Prophet warnings the code really raises are quoted and explained where they appear.
- **References.** Wrong pointers fixed: Ch 48's dataset (option (a)), Ch 45 → Ch 23, Ch 52 → Ch 46 and Ch 56, capstone promises removed, Ch 74 bullet made true; planning-file and "Appendix G" leftovers removed.
- **Figures.** All four redrawn from `figures/make_figs40.py` at ≥ 7.2 pt; Figure 40.2 no longer relies on colour and its caption matches the bars; Figure 40.4's band, baseline and stoppage fixed.

## Skipped, and why

- Nothing skipped. RJ-S3-46's remaining work (adding Deepak Nair to the story bible, the Priya surnames) belongs to the fact sheet and Ch 33/41, not this chapter.
- The Deepak story keeps "July 2026": story dates wait for the fact sheet (not yet approved).

## Option picks

- 40.34: option (a), describe Ch 48's real dataset and drop the 4.8-million-row/`--full` claims (no option marked recommended).
- 40.36: delete the planning-file sentence (first option).
- 40.38: first option, rewrite the second case to actuals 50, 100, 150; the asymmetry case added as the finding also asks.
- 40.42: first option, change the code so both columns are scored on the same weeks at the same horizon.
- 40.26: first option, simplify the print.
- 40.1: done as a subsection opening §40.2 (renamed "Autocorrelation and stationarity") instead of a new "§40.2a", so no section numbers change.

## Time needed

10–14 hours → **16–20 hours over three weeks, in four sittings** (40.0–40.3; 40.4–40.5; 40.6–40.9; 40.10 and the project). The review's own estimate was 15–20 hours once the by-hand steps were added; the chapter grew from 37 to 52 pages, with 26 more code cells (27 → 53) and a new setup section.

## Code verification

- `verify_python.py manuscript/ch40-*.md --cwd companion/ch40`: 53 blocks run, 49 outputs checked, **0 mismatches** (Python 3.11.15, pandas 3.0.6, statsmodels 0.15.0, scikit-learn 1.9.1, Prophet 1.4.0). Run with `OMP_NUM_THREADS=1`; the whole chapter takes under a minute.
- `checks/ch40_check.py`: all checks pass (prose numbers recomputed); `verify_shell.py`: no checked shell blocks (the terminal steps are marked `run: none`, their outputs copied from a real run).
- Outputs that changed with scikit-learn 1.9.1: one-week-ahead 9.3% → 9.4%, recursive 8.9% → 9.3%, monthly-summed 13.6% → 14.3%, leaky 9.2% → 8.9%, answer 12's table. Prose follows the new numbers.
