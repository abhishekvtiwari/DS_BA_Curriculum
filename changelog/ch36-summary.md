# Ch 36 summary · The Machine Learning Workflow & Feature Engineering

**What changed.** The chapter now gives the reader a proper first scikit-learn lesson before anything is combined. A new **§36.4 "scikit-learn, one piece at a time"** fits a `LogisticRegression` on one column, then shows `predict`, `predict_proba`, `classes_` and `[:, 1]`, then `StandardScaler`, `SimpleImputer`, `OneHotEncoder`, `Pipeline` and `ColumnTransformer`, one per cell with real output. After that it builds `make_model` from named sub-pipelines, explained in a line-by-line table. `train_test_split` is taught in §36.3, and a `split()` helper is used everywhere. AUC is worked by hand, and you can see what each cross-validation fold contains. Features are built one cell per family in §36.6, and the leakage section now comes after them (§36.7), so nothing is used before it's taught. Every `%` print is now an f-string. Wrong cross-references are fixed (52 → 56, 47 → 46). The false HistGradientBoosting/sparse claim is fixed with `sparse_output=False`. Drafting leftovers are removed, the key terms are defined in the text, and the story picks up Chapter 35's vendor pilot. All five figures were redrawn at 7.4 pt minimum; Fig 36.5 bars now start at 0. The chapter was renumbered internally: 36.4 → 36.5 (CV), 36.5 → 36.7 (leakage), 36.7 → 36.8, 36.8 → 36.9, 36.9 → 36.10.

**Findings.** 31 content rows and 8 open visual rows (V36.1–5, 13, 14, 19) were applied, plus RJ-S3-41 (Ch 36 part). V36.9 and V36.18 (earlier layout-pass fixes) were re-checked in the rebuilt PDF. Nothing was skipped.

**Deviations, with reasons.**
- 36.3: no pinned `pip install scikit-learn==1.8.0`. Ch 35 §35.9 installs scikit-learn, so this chapter checks the version (1.9.1) at first use.
- 36.26: the median-imputer demo uses `est_quantity`, because `log_quantity` isn't built until §36.6.
- 36.19: the `stage_history.csv` check found 821 of 826 wins; 5 Won leads have histories ending Lost. This is reported as a real data disagreement.
- RJ-S2-15 and RJ-S2-16 (Open, need the unapproved fact sheet): untouched.

**Option picks.** 36.10: move leakage after feature engineering (the alternative leaves a forward reference). 36.14 (a): `sparse_output=False`. 36.19 (a): add the check. 36.20 (a): delete the sentence. 36.31 (a): rename to `gmail`. V36.19 (a): start the axis at 0.

**Time needed.** Was 8–12 h; now **14–18 hours over two weeks**, in three sittings (A §36.1–36.4 ≈ 4 h, B §36.5–36.7 ≈ 5 h, C §36.8–36.10 ≈ 3 h) plus the project (4–6 h). This is the review's estimate. It is justified by the on-ramp (about 10 new cells) and the split-out feature cells.

**Verification.**
- `verify_python`: 57 blocks run, 57 outputs checked, **0 mismatches** (Python 3.11.15, pandas 3.0.6, NumPy 2.4.6, scikit-learn 1.9.1, data from `generate_riverstone_crm.py`, seed 20236).
- `checks/ch36_check.py`: all pass (4 new checks added).
- `fig_check`: 0 figures under 7 pt.
- `restructure --check`: in order.
- `layout_check`: map 16/16, no stranded heads or lead-ins, no sparse pages, no small text, no draft labels, tofu 0; prescan clean. The PDF is 47 pages (was 41).
