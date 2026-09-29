# Ch 39 · Evaluation, Tuning, Interpretation & Honesty: summary

**What changed.** Every metric now starts from a tiny example worked by hand before any scikit-learn code:
- ten leads for the confusion matrix, precision, recall, F1 and specificity, plus a threshold sweep, ROC-AUC by counting pairs and average precision;
- four accounts for MAE, RMSE, MAPE, R² and WAPE;
- three leads for Brier and log loss;
- six leads for permutation importance;
- a two-feature linear model for SHAP;
- three accounts for partial dependence.

The title's promise is kept by a new **§39.6a "Tuning honestly"**: a small `GridSearchCV` on logistic regression's `C`, with every argument explained, the hyperparameter-vs-threshold distinction, and why the scoring rule matters. The result is honest: the C values tie, so the chapter keeps C = 1.

**Permutation importance is taught in the body** (§39.7), and exercise 12 is now a variation on it. Other changes:
- Every long block is split into cells, each with a "How it works".
- Plotting cells are added for the ROC/PR, reliability and profit curves.
- `imbalanced-learn` and `shap` are installed where they are first used.
- The churn pipeline moves into a new companion helper, `companion/ch39/churn_data.py`.
- The fairness tables keep the blank segment with `dropna=False` (108 leads) and label groups with `.rename`.
- Recalibrating a rebalanced model is shown.
- A short macro/weighted F1 subsection is added (for Ch 41 and Ch 74).

All five figures are redrawn at ≥ 7.1 pt, with no labels on data and no colour-only meaning. Figure 39.3 gains marker shapes and a zoom panel.

**Wrong numbers and references fixed:**
- 660 → 627 leads;
- the measured 5% band;
- 4 leads per team-day;
- 43% vs 9% misses ("nearly five times");
- ₹8.1 lakh (not 0.9 million);
- Platt scaling has two parameters;
- "no better than" (not "worse than") the all-lost accuracy;
- §39.4/§39.5 references;
- Chapter 52 → 56 and Chapter 61 → 64;
- the model card no longer claims a city check.

Rupee prose uses lakh grouping (₹24.5 lakh, ₹2,32,567); program output is left as printed, with one sentence explaining Python's grouping. Ch 36's `free_email` → `gmail` rename and its new section numbers are followed.

**Skipped or partial, and why:**
- 39.22: the SMOTENC rerun (optional) was not done; there is a Watch-out instead.
- RJ-S3-42: nothing to change in Ch 39, because its Tools list has no statsmodels pointer.
- RJ-S3-41: the vendor pilot is closed in one sentence with no invented numbers. It is flagged for Abhishek because the story outcome is new.

**Option picks:**
- 39.1 (b) new section;
- 39.11 define WAPE here;
- 39.18 state the measured band;
- 39.19 soften and show the bins;
- 39.35 reword the card;
- 39.33 `dropna=False`;
- 74.9 add the example to Ch 39;
- 39.7 plain matplotlib rather than Display classes.

**Time needed:** was 10–14 h. Now **16–20 hours over two to three weeks**, in four sittings of 4–5 h: §39.1–39.3; §39.4–39.6a; §39.7–39.9; exercises and project. The PDF grew from 34 to 55 pages, with about 20 new code cells and six by-hand examples.

**Verification:**
- `verify_python`: 48 blocks run, 45 outputs checked, **0 mismatches** (scikit-learn 1.9.1, shap 0.51.0, imbalanced-learn 0.14.2, Python 3.11.15).
- `checks/ch39_check.py`: all ~60 prose numbers pass.
- `restructure --check`: in order.
- `fig_check`: 0 under 7 pt.
- `layout_check`: clean (map 16/16, no stranded or sparse pages, tofu 0).
- `check_code_teaching`: 2 flags left, both repeat cells whose ideas were explained earlier (the churn TreeExplainer cell and answer 13).
