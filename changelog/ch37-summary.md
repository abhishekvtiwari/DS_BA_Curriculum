# Chapter 37 · Supervised Learning Algorithms · summary

**76 register rows handled:** 73 Verified (57 content, 16 visual), 3 reader-journey rows left Approved because the rest of their fix belongs to other chapters or to a decision (RJ-S3-40, RJ-S3-42, RJ-S3-47). Nothing skipped.

## What changed

- **Setup and data (§37.0, retitled "Setting up, and the data").** A setup section at the start: the terminal in `companion/ch37/`, building the data if it's missing, a shown `python -m pip install xgboost lightgbm catboost optuna` cell, and starting Jupyter. Also a "Two ways to be wrong" box (underfitting/overfitting), a 20-column data dictionary, and the first code block split into five cells. The warnings filter is gone.
- **Every family now has a by-hand step:** a weighted sum, ridge/lasso shrinkage on four rows, the odds box, k-NN on five points, a Naive Bayes posterior reproduced with `BernoulliNB`, Gini, a three-stump bootstrap forest, one boosting round done in full, and a 1-D SVM margin.
- **Code taught like Jupyter.** The multi-job blocks are split: many-feature regression into 4 cells, logistic into 4, the tree into 3, the libraries into 1 cell per library plus a shared settings table, and random search into 3. Every argument the review listed is now explained. `reg_pipeline`/`clf_pipeline` take a `nums=` argument, which replaces the 30-line engineered pipeline and the global rebinding in the answers.
- **M.11:** MAE is defined with a formula and a worked example before its first use. SHAP and permutation importance get a one-line gloss at first mention, and both still point to Ch 39 (§39.3, §39.8).
- **Honesty and correctness.** Paired fold differences replace the "spreads are smaller than the gaps" claim. Each engineered feature is now derived on screen from the training accounts (option a). The ridge/lasso α scales are explained. The Optuna result is called a tie. The GaussianNB densifier is removed, since it wasn't needed. `SVC(probability=True)`, deprecated in scikit-learn 1.9, is replaced by `CalibratedClassifierCV(SVC(...), ensemble=False)`. The story now scores each model once on the same split, with no Chapter 40 promise.
- **Cross-references:** statsmodels intervals now point to Ch 30 §30.11 and §22.10. Ch 36 and Ch 39 section numbers are updated to their new layouts. Bayes' rule points to §21.7 and the bootstrap to Ch 22.
- **Exercises:** three new hand warm-ups (k-NN, ridge, one boosting round), so there are now 19 exercises. The Appendix G note and the planning-file reference are removed.
- **Figures:** a new Figure 37.1 (residual plot). The lasso figure is now two stacked panels with values printed. The tree-depth figure uses all ten printed depths, with the "best" label anchored by a leader line. The learning curves are stacked. All text is 8.1–9.6 pt, and lines are told apart by solid vs dashed style and circle vs square markers as well as colour.

## Option picks

- 37.7: print `pred[0]`.
- 37.28: add a sentence.
- 37.33: add the missing depths to the printed loop.
- 37.36 (a): print the toy rows and choose a new sample.
- 37.38: CatBoost now uses 300 iterations.
- 37.42 (a): derive the features on screen.
- 37.49: print the count.
- 37.51: no chapter reference.
- V37.1: stacked panels.
- V37.3: stack the panels.
- V37.16: keep 37.0 as a setup section, the book's NN.0 convention.

## Modified findings

- **37.50:** a run disproved the finding's premise. GaussianNB gives AUC 0.740 scaled and 0.732 unscaled, because `var_smoothing` is sized from the largest variance. The table now says "No (in scikit-learn, slightly)", and §37.5 shows both runs.
- **37.39:** the SVM code changed because of the scikit-learn 1.9 deprecation. The AUCs are unchanged.

## Time needed

Now **20–24 hours over three weeks**, in Part A (§37.0–37.5, 9–10 h) and Part B (§37.6–37.12 plus the project, 11–13 h), with a hand-work checkpoint after each part. This follows 37.47. The chapter grew from 48 to 70 PDF pages: six new by-hand steps, twice as many cells, and three new exercises.

## Verification

- `verify_python.py`: 73 blocks run, 68 outputs checked, **0 mismatches**. Run on Python 3.11.15, scikit-learn 1.9.1, XGBoost 3.2.0, LightGBM 4.7.0, CatBoost 1.2.10, Optuna 5.0.0, with `OMP_NUM_THREADS=1`. No warnings appear in any cell.
- `checks/ch37_check.py`: all hand numbers and figure data pass.
- `layout_check`: clean (map 19/19, no stranded heads or lead-ins, no sparse pages, tofu 0).
- `fig_check`: 0 figures under 7 pt.
- `restructure --check`: already in order.
- `check_code_teaching`: 8 residual flags. They are coverage-ratio noise on column names, or answer blocks that reuse ideas already taught.
- **Number changes from scikit-learn 1.9.1:**
  - tuned HGB validation 0.788 → 0.786, and its CV SD 0.018 → 0.016;
  - tuned boosting test AUC 0.839 → 0.838;
  - Optuna 0.844 → 0.843;
  - leads boosting VALID 0.829 → 0.826 and TEST 0.832 → 0.830;
  - CatBoost at 300 iterations 0.796 → 0.797.

  The prose follows the new outputs.
