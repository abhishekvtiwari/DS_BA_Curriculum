# Chapter 74. Machine Learning Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the ML questions that come up across screening calls, live-coding rounds, and case interviews for Data Scientist, ML Engineer, and analytics-adjacent roles · explain bias and variance, not just define them · spot data leakage before a model's score fools you · read a confusion matrix, an ROC curve, and a calibration plot the way an interviewer actually wants · debug a model that "worked in training and broke in production."
>
> **Before you start:** Part 4 (Chapters 35–43), which teaches every idea in this bank; Chapter 53, section 53.3 (early stopping) and Chapter 56 (monitoring, drift, training-serving skew) for section 74.6; Chapter 69 for the three answer tiers and the twelve extra-point tags. This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** 6–8 hours for a first pass: about 10 minutes per core question answered aloud, 1–2 minutes per rapid-fire row, and about an hour to run the four code demos yourself. Plus 1 hour for the final-week list.
>
> **How this chapter is built.** Same format as every question bank in Part 8 (Chapters 70–82). Every **core question** gives a memory hook ("Remember it as…"), a one-line answer you can recall under pressure, and a tier table: what **passes**, what's **strong**, and the **extra points** (Chapter 69's moves, tagged the same way: **[+Clarify]**, **[+Edge cases]**, **[+Validate]** and so on). Then come the likely follow-ups, the red flag, and where to learn it. Every **rapid-fire section** is a scan table: question, one-line answer, one extra point, level, and where to learn it (a bare number such as 37.2 means that section). Every **Learn it in** pointer names the section of Part 4 (or Chapter 53 or 56) that teaches the idea, and the numbers quoted are the ones you produced there. The four **Run it yourself** demos are complete cells: copy one into a fresh notebook and it prints what's shown (scikit-learn 1.9.1, the version installed in Chapter 35, section 35.9). Ideas no earlier chapter teaches are marked **Beyond the book** and carry their own short explanation and example.
>
> **Levels and roles.** Each question carries a level and the roles that usually ask it. **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds. **DS** data scientist · **MLE** machine learning engineer · **DA** data analyst (and other analytics roles that work next to a model). Within each section the core questions run from easier to harder, and the sections do too: the basic-but-tricky questions come first.
>
> **A note on scope.** This is an *interview* bank, testing whether you can explain and reason about ML concepts under time pressure, not a re-teaching of the algorithms themselves (that's Chapters 35–43 in full). Read this chapter after those, not instead of them.

---

## 74.1 Basic-but-tricky ML questions

### Q74-007 · Is a model with 95% accuracy always a good model?

**Level:** Fresher · **Roles:** DS, DA, MLE

**Remember it as:** *Always ask the base rate before believing an accuracy number. Predicting "no" for everyone on a 5%-positive problem is already 95% accurate.*

**Answer in one line:** No: on an imbalanced problem, a model that predicts the majority class for every single row can achieve very high accuracy while catching zero of the minority class it was actually built to find.

**From Chapter 37, section 37.0:** 484 of Riverstone's 5,000 accounts churned in 2025, a churn rate of 9.7%. So predicting "no churn" for every account is already **90.3%** accurate (4,516 ÷ 5,000).

| Tier | What to say |
|---|---|
| Passes | "Accuracy isn't everything" (correct, no concrete demonstration) |
| Strong | Computes or cites the actual base-rate accuracy, showing how little a headline accuracy number proves on its own |
| Extra points | **[+Clarify]** "What's the positive rate?" before reacting to any accuracy figure<br>**[+Business]** 90.3% is the real bar Riverstone's own churn model had to beat, and it's why Chapter 39 uses precision, recall, and PR-AUC instead of accuracy on any imbalanced problem |

**Likely follow-ups:** What metrics would you ask for instead? How imbalanced does a problem need to be before accuracy becomes actively misleading?
**Red flag:** treating a single accuracy number as sufficient evidence of a good model with no mention of the base rate.
**Learn it in:** Chapter 37, section 37.0 (the 9.7% churn rate) and Chapter 39, sections 39.1–39.2.

### Q74-008 · Can a model have a good ROC-AUC and still be a bad choice for the business?

**Level:** Mid · **Roles:** DS, DA

**Remember it as:** *ROC-AUC measures whether a model ranks well. It says nothing about whether the threshold you'll actually use makes money.*

**Answer in one line:** Yes: ROC-AUC measures a model's ability to *rank* positive cases above negative ones across every possible threshold, but says nothing about calibration, about performance at the *one* threshold you'll actually deploy, or about whether the business cost of a false positive versus a false negative makes that threshold worthwhile at all.

| Tier | What to say |
|---|---|
| Passes | "AUC only tells you ranking, not the actual threshold" (correct, no elaboration) |
| Strong | Names the specific gaps: calibration (Q74-014), threshold-specific cost trade-offs, and PR-AUC's sensitivity to the base rate that plain ROC-AUC hides |
| Extra points | **[+Business]** Riverstone's lead model has an ROC-AUC of 0.823, which sounds strong, and its business value only became visible once a cost-based threshold was applied: working all 2,225 validation leads makes ₹10.8 lakh, working the 627 leads above the best threshold makes ₹24.5 lakh<br>**[+Limits]** even that threshold gave way to capacity: the team can work about 504 leads in six months, so the real rule is "the top 504" |

**Likely follow-ups:** What would you look at alongside AUC to judge business readiness? When is a lower-AUC but better-calibrated model the right choice?
**Red flag:** treating AUC as a complete summary of "is this model good."
**Learn it in:** Chapter 39, sections 39.2 (ROC and PR curves) and 39.5 (the profit curve and capacity).

### Rapid-fire, 74.1

Roles: DS and DA for every row; MLE for Q74-011 and Q74-012.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q74-009 | Does a higher R² always mean a better regression model? | No: *training* R² never goes down when you add a feature, even a useless one. Judge with held-out R² or adjusted R² (below), which charges for each extra feature | **[+Validate]** Chapter 37 reports *test* R², which can fall: 0.9546 with one feature, 0.9593 with many | Mid · 37.1; adjusted R² is Beyond the book |
| Q74-010 | Is a model with zero training error a good sign? | Usually a red flag: it often means the model has memorized the training set rather than learned a pattern that generalizes | **[+Evidence]** an unlimited decision tree on the churn accounts: training AUC 1.000, validation 0.557 | Fresher · 37.6 |
| Q74-011 | Do you always need to scale features before training a model? | Depends on the algorithm: distance- and penalty-based methods (k-NN, k-means, SVM, regularized linear models) need it; tree-based methods (random forest, gradient boosting) generally don't | **[+Evidence]** k-NN on the churn accounts: AUC 0.765 scaled, 0.633 unscaled, because revenue in rupees swamps every distance | Fresher · 37.4 |
| Q74-012 | Is a random forest always better than a single decision tree? | No, but it's very often more stable: a single tree is high-variance and sensitive to its exact training sample; averaging many trees reduces that variance, at some cost in interpretability | **[+Trade-offs]** you give up a tree you can print and read (section 37.6's depth-2 tree) for a score you can trust more | Fresher · 37.7 |

**Beyond the book: adjusted R².** Chapter 37 judges regression on held-out rows, which is the better habit. Some interviewers still ask for **adjusted R²**, which penalizes R² for the number of features *p* given the number of rows *n*:

> adjusted R² = 1 − (1 − R²) × (*n* − 1) ÷ (*n* − *p* − 1)

A model with R² 0.90 on *n* = 50 rows using *p* = 10 features: 1 − 0.10 × 49 ÷ 39 = 1 − 0.126 = **0.874**. Add a useless eleventh feature that nudges R² to 0.901 and adjusted R² *falls*, to 1 − 0.099 × 49 ÷ 38 = **0.872**: the penalty for the extra feature outweighs the gain.

---

## 74.2 Bias, variance, and the shape of a good model

### Q74-001 · Explain the bias-variance trade-off, and show it on a real model

**Level:** Fresher · **Roles:** DS, MLE

**Remember it as:** *Too simple, and the model can't learn the pattern even from the training data (high bias). Too complex, and it memorizes the training data's noise instead of the real pattern (high variance).*

**Answer in one line:** **Bias** is error from a model too simple to capture the real pattern, showing up as poor performance on *both* training and held-out data; **variance** is error from a model too sensitive to the specific training sample, showing up as a large gap between strong training performance and weak held-out performance.

**From Chapter 37, section 37.6:** decision trees of growing depth on Riverstone's churn accounts (3,000 training, 1,000 validation):

| `max_depth` | Train AUC | Validation AUC | Leaves |
|---|---:|---:|---:|
| 1 | 0.696 | 0.651 | 2 |
| 2 | 0.759 | 0.708 | 4 |
| 3 | 0.791 | **0.752** | 8 |
| 4 | 0.829 | 0.748 | 16 |
| 5 | 0.865 | 0.750 | 29 |
| 6 | 0.886 | 0.733 | 48 |
| 8 | 0.934 | 0.672 | 97 |
| 10 | 0.969 | 0.609 | 161 |
| 14 | 0.994 | 0.543 | 230 |
| None (no limit) | 1.000 | 0.557 | 277 |

Depth 1 is high bias: both scores are low and close together. The unlimited tree is high variance: perfect on training, barely better than a coin on validation. Depth 3 is the sweet spot on this data, with 4 and 5 close behind.

| Tier | What to say |
|---|---|
| Passes | Defines both terms correctly, can't demonstrate the trade-off with numbers |
| Strong | The sweep above: depth 1 underfits (both scores low and close), unlimited depth overfits (perfect training, a large gap to validation), and the best validation score sits in between, at depth 3 |
| Extra points | **[+Evidence]** these are measured numbers from your own work, not a textbook sketch<br>**[+Signpost]** name the second tool: section 37.10's learning curves show logistic regression limited by bias (training and CV scores meet at about 0.81 and stay there) and boosting by variance (training 0.945 against CV 0.836, still closing as rows are added)<br>**[+Business]** this is why "just add more model complexity" isn't a free lunch |

**Likely follow-ups:** How would you diagnose which one your model has, without a controlled sweep like this? What's the relationship between bias-variance and a learning curve?
**Red flag:** defining the terms correctly but being unable to say which symptom (both scores low vs. a train-validation gap) points to which problem.
**Learn it in:** Chapter 37, sections 37.0 ("Two ways to be wrong"), 37.6 (depth and overfitting), and 37.10 (bias, variance, and learning curves).

### Q74-002 · Why can a model reach perfect training AUC on pure noise, with enough features and too few samples?

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *Give a model enough dimensions relative to how much data it has, and it can always find some combination that happens to separate the training rows perfectly, real pattern or not.*

**Answer in one line:** With enough features relative to the sample size, a flexible model can find a combination of features that perfectly separates the training labels by chance alone, even when the features carry zero real signal: the **curse of dimensionality** meeting overfitting.

**Run it yourself.** 200 rows of pure noise, with a target that has no relationship to any feature. The function below builds one such dataset, splits it 70/30, fits a logistic regression with almost no penalty, and returns the training and test AUC:

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


def noise_run(n_features, seed):
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, (200, n_features))
    y = rng.integers(0, 2, 200)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=seed)
    model = LogisticRegression(C=1_000_000, max_iter=10_000).fit(X_tr, y_tr)
    train_auc = roc_auc_score(y_tr, model.predict_proba(X_tr)[:, 1])
    test_auc = roc_auc_score(y_te, model.predict_proba(X_te)[:, 1])
    return train_auc, test_auc


for n_features in [5, 50, 200]:
    train_auc, test_auc = noise_run(n_features, seed=0)
    print(f"{n_features:>3} features: train AUC {train_auc:.3f}   test AUC {test_auc:.3f}")
```

```
  5 features: train AUC 0.620   test AUC 0.576
 50 features: train AUC 0.894   test AUC 0.498
200 features: train AUC 1.000   test AUC 0.578
```

**How it works:**

- `np.random.default_rng(seed)` is a seeded random generator (Chapter 21), so every run with the same seed draws the same numbers. `rng.normal(0, 1, (200, n_features))` fills a 200-row table with standard normal noise; `rng.integers(0, 2, 200)` draws 200 random 0s and 1s, the target. Nothing links them.
- `train_test_split(..., test_size=0.3, random_state=seed)` keeps 140 rows for training and 60 for testing (Chapter 36, section 36.3).
- `LogisticRegression(C=1_000_000, ...)`: `C` is the inverse of the penalty strength (Chapter 37, section 37.3), so a million means almost no regularization. `max_iter=10_000` gives the optimizer room to finish.
- `roc_auc_score` is Chapter 36's AUC; `[:, 1]` keeps the probability of class 1.

With 200 noise features and only 140 training rows, the model scores a **perfect 1.000** on the rows it learned from. But one test set of 60 rows is small, and a single test AUC swings a lot by chance: 0.576 and 0.578 aren't signs of learning. Before you run the next cell, predict: averaged over 20 different random datasets, where will the test AUC land?

```python
for n_features in [5, 50, 200]:
    runs = np.array([noise_run(n_features, seed) for seed in range(20)])
    print(
        f"{n_features:>3} features: mean train AUC {runs[:, 0].mean():.3f}   "
        f"mean test AUC {runs[:, 1].mean():.3f} "
        f"(range {runs[:, 1].min():.2f} to {runs[:, 1].max():.2f})"
    )
```

```
  5 features: mean train AUC 0.595   mean test AUC 0.524 (range 0.32 to 0.69)
 50 features: mean train AUC 0.860   mean test AUC 0.519 (range 0.37 to 0.69)
200 features: mean train AUC 1.000   mean test AUC 0.499 (range 0.32 to 0.72)
```

**How it works:** the list comprehension runs `noise_run` for seeds 0 to 19, and `np.array` stacks the 20 (train, test) pairs into a 20-by-2 array. `runs[:, 0]` is the training column and `runs[:, 1]` the test column; `.mean()`, `.min()` and `.max()` summarize each.

**Reading it.** The training AUC climbs with the number of features, from 0.595 to a perfect 1.000 at every one of the 20 seeds with 200 features. The test AUC stays at about 0.5, a coin toss, whatever the number of features, and any single run can land anywhere from about 0.3 to 0.7. More features bought a perfect training score on data with no signal at all.

| Tier | What to say |
|---|---|
| Passes | "More features can cause overfitting" (true, no demonstration of the mechanism or size of the effect) |
| Strong | Explains the mechanism: with enough dimensions, there's almost always *some* direction in feature space that happens to line up with the training labels by chance |
| Extra points | **[+Validate]** perfect training AUC on data built to have zero signal, and a test AUC that averages 0.5<br>**[+Edge cases]** a single test AUC on 60 rows can read 0.58 or 0.32 by luck; average over several splits (or cross-validate) before calling it a trend<br>**[+Business]** a model with hundreds of engineered features and only a few thousand rows needs regularization and honest held-out validation, not a high training score, before anyone trusts it |

**Likely follow-ups:** How does regularization (L1/L2) address this specifically? What sample-to-feature ratio would make you nervous?
**Red flag:** treating a high training score alone as evidence a model is good.
**Learn it in:** Chapter 37, sections 37.2 (ridge, lasso, and elastic net) and 37.10; Chapter 36, section 36.5 (cross-validation).

### Rapid-fire, 74.2

Roles: DS and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q74-003 | What's regularization, in one sentence? | A penalty added to the loss that discourages large model weights, trading a little training fit for better generalization | **[+Signpost]** name the three kinds (ridge, lasso, elastic net) and the one setting that controls the strength (α) | Fresher · 37.2 |
| Q74-004 | L1 vs. L2 regularization: what's the practical difference? | L1 (lasso) can shrink coefficients exactly to zero, performing feature selection; L2 (ridge) shrinks them toward zero but rarely to exactly zero | **[+Evidence]** Chapter 37's lasso path (Figure 37.2): 14 features kept at α = 0.001, 5 at 0.01, 1 at 0.2, with almost the same accuracy at 5 as at 14 | Fresher · 37.2 |
| Q74-005 | What's a learning curve, and what does a persistent gap between train and validation lines tell you? | A plot of training and validation score against training-set size; a large gap signals high variance, and if the validation line is still rising, more data should help | **[+Edge cases]** two lines that meet early and stay flat mean high bias: more data won't help (logistic regression on the churn accounts, gap 0.013) | Mid · 37.10 |
| Q74-006 | Does adding more training data fix high bias? | No: high bias means the model itself is too simple for the pattern; more data of the same kind won't change that, a more expressive model or better features will | **[+Evidence]** four engineered features lifted logistic regression's cross-validated AUC on the churn accounts from 0.807 to 0.849; more rows hadn't moved it | Mid · 37.10 |

---

## 74.3 Metrics, calibration, and thresholds

### Q74-013 · Build a confusion matrix by hand and derive precision, recall, and F1 from it

**Level:** Fresher · **Roles:** DS, DA, MLE

**Remember it as:** *Precision reads across the "predicted positive" row. Recall reads down the "actually positive" column. They answer different questions and usually trade against each other.*

**Answer in one line:** Given TP, FP, FN, TN: **precision** = TP/(TP+FP) (of what you flagged, how much was right), **recall** = TP/(TP+FN) (of what was actually positive, how much did you catch), **F1** = the harmonic mean of the two.

**From Chapter 39, section 39.1:** Riverstone's lead model on 2,225 validation leads, at a threshold of 0.1:

```
TP=100  FP=386  FN=46  TN=1693
precision = 100/486 = 0.206
recall    = 100/146 = 0.685
F1        = 2 × 0.206 × 0.685 / (0.206 + 0.685) = 0.317   (0.316 unrounded)
```

| Tier | What to say |
|---|---|
| Passes | States the formulas correctly, makes an arithmetic error applying them |
| Strong | The correct worked calculation above, matching a real model's real confusion matrix |
| Extra points | **[+Edge cases]** layouts differ: Chapter 39's table puts predictions on the rows, but scikit-learn's `confusion_matrix` puts the *actual* classes on the rows, so there precision reads *down* the predicted-positive column. Always say which axis is which before reading one<br>**[+Business]** at this threshold only 1 in 5 flagged leads is won (20.6% precision), but the model catches over two-thirds of all wins (68.5% recall); whether that's right depends on what a wasted call costs against a missed win, which is Chapter 39's cost-based threshold |

**Likely follow-ups:** What happens to precision and recall as you raise the threshold? Why can't you maximize both at once, in general?
**Red flag:** computing precision and recall with the numerator and denominator swapped, a very common slip under time pressure.
**Learn it in:** Chapter 39, section 39.1.

### Q74-014 · What does it mean for a model's probabilities to be "well calibrated," and why can a model with good ranking still be poorly calibrated?

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *Ranking asks "did the model put the right cases higher than the wrong ones?" Calibration asks "when it says 70%, does that group of cases actually convert 70% of the time?" Different questions, no guaranteed relationship.*

**Answer in one line:** A model is well calibrated if, among all the cases it gives a certain probability (say, 70%), roughly that share turn out positive; a model can rank cases well (a good AUC) while being badly calibrated, if its probabilities are systematically too high or too low (Naive Bayes says 94% where the truth is 27%).

**From Chapter 39, section 39.4**, two models on the same 2,225 validation leads, where 6.6% were won:

| Model | ROC-AUC | Mean predicted probability | Log loss |
|---|---:|---:|---:|
| Logistic regression | 0.823 | 6.9% | 0.1948 |
| Naive Bayes | 0.806 | 18.0% | 0.4830 |

Naive Bayes ranks reasonably well (0.806 AUC) while being **dramatically overconfident**: its top tenth of leads is given a 94% chance of being won, and only 27% of them are.

| Tier | What to say |
|---|---|
| Passes | "Calibration means the probabilities are accurate" (vague, no example of the ranking/calibration gap) |
| Strong | The real example above: a model can have a good AUC and still be badly, provably miscalibrated |
| Extra points | **[+Business]** a rep told "94% chance" who wins one in four stops trusting the model entirely<br>**[+Evidence]** isotonic calibration fixed it: log loss from 0.483 to 0.202, with the ranking almost unchanged (ROC-AUC 0.806 to 0.802) |

**Likely follow-ups:** How do you check calibration in practice? What's the difference between Platt scaling and isotonic regression?
**Red flag:** assuming a high AUC implies trustworthy probabilities.
**Learn it in:** Chapter 39, section 39.4.

### Rapid-fire, 74.3

Roles: DS and DA for every row; MLE for Q74-015 and Q74-018.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q74-015 | ROC-AUC vs. PR-AUC: when does the choice matter most? | They tell a similar story on balanced data; on imbalanced data, PR-AUC reflects what users actually experience (precision) far better than ROC-AUC, which stays high | **[+Evidence]** the same lead model scores ROC-AUC 0.823 and PR-AUC 0.302; a random model would score 0.5 and 0.066 (the base rate) | Mid · 39.2 |
| Q74-016 | What's the harm in always using 0.5 as a classification threshold? | It's an arbitrary default with no link to the cost of a false positive vs. a false negative. On Riverstone's lead data it flags only 7 of 2,225 leads, catching 4 of 146 wins; its 93.5% accuracy is no better than predicting "no" for everyone (93.4%) | **[+Business]** set the threshold from the costs (break-even at 0.05 for the leads), then cap it by team capacity | Fresher · 39.1, 39.5 |
| Q74-017 | MAE vs. RMSE: what's the difference, and when do they disagree the most? | Mean absolute error weights every error equally; root mean squared error punishes large errors far more (it squares them), so they diverge most when a few large errors exist | **[+Evidence]** Riverstone's revenue model: MAE ₹92,933, RMSE ₹2,32,567, because one account is off by about ₹37 lakh | Fresher · 39.3 |
| Q74-018 | What's the difference between macro and weighted F1 for a multi-class problem? | Macro averages each class's F1 equally regardless of class size; weighted averages them by each class's support (number of examples), so a poor score on a rare class matters less in the weighted version | **[+Business]** per-class F1 of 0.9, 0.8 and 0.2 with 800, 150 and 50 examples: macro 0.633, weighted 0.850. Report macro (or the per-class table) when the rare class is the one you care about | Mid · 39.1 ("More than two classes") |

---

## 74.4 Data leakage

### Q74-019 · Demonstrate target leakage: build a model with and without a leaked feature, and show the difference

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *If a feature couldn't have existed at the moment you're predicting, it doesn't belong in the model, however good it makes the score look.*

**Answer in one line:** **Target leakage** happens when a feature is influenced by, or nearly a copy of, the outcome you're trying to predict, giving the model information it would never have at prediction time and inflating its score in a way that won't hold up in production.

**Run it yourself.** First, a dataset with one honest feature, `signal`, that drives the outcome, and one leaked feature: the outcome itself plus a little noise, like a status field that's only set *after* the outcome is known.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(74)
n = 2_000
signal = rng.normal(0, 1, n)
y = (signal + rng.normal(0, 0.5, n) > 1).astype(int)
leaked = y + rng.normal(0, 0.1, n)
X = pd.DataFrame({"signal": signal, "leaked": leaked})
print(f"{n:,} rows, {y.mean():.1%} positive")
```

```
2,000 rows, 19.6% positive
```

**How it works:**

- `rng = np.random.default_rng(74)` seeds the generator, so you get exactly these rows.
- `signal` is 2,000 draws of standard normal noise. The outcome `y` is 1 when `signal` plus some extra noise (`rng.normal(0, 0.5, n)`) is above 1, so `signal` predicts `y` well but not perfectly. `.astype(int)` turns True/False into 1/0.
- `leaked` is `y` plus a tiny bit of noise (standard deviation 0.1): almost a copy of the answer.
- `pd.DataFrame({...})` puts the two features in one table with named columns.

Now train the same random forest twice, once on `signal` alone and once with `leaked` added. Before you run it, predict: how much will the test AUC rise, and which feature will the forest say matters most?

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3, random_state=74, stratify=y
)
for cols in [["signal"], ["signal", "leaked"]]:
    forest = RandomForestClassifier(
        n_estimators=200, min_samples_leaf=5, random_state=74
    ).fit(X_tr[cols], y_tr)
    auc = roc_auc_score(y_te, forest.predict_proba(X_te[cols])[:, 1])
    importances = forest.feature_importances_.round(2)
    print(f"{' + '.join(cols):<16} test AUC {auc:.3f}   importances {importances}")
```

```
signal           test AUC 0.932   importances [1.]
signal + leaked  test AUC 1.000   importances [0.29 0.71]
```

**How it works:**

- `stratify=y` keeps the 19.6% positive rate the same in the training and test rows (Chapter 36, section 36.3).
- The loop fits one forest per feature list. `X_tr[cols]` picks just those columns. `n_estimators=200` trees, `min_samples_leaf=5` and `random_state=74` are the kind of settings Chapter 37, section 37.7 uses.
- `feature_importances_` has one number per feature, adding up to 1 (section 37.7); `.round(2)` keeps two decimals. With one feature it's `[1.]`.
- `' + '.join(cols)` writes the feature list as "signal + leaked"; `:<16` pads it to 16 characters so the columns line up.

**Reading it.** One noisy copy of the answer pushes the test AUC from 0.932 to a **perfect 1.000**, and takes 71% of the importance away from the feature that really drives the outcome. A score that's suspiciously perfect plus one dominant feature: that's the profile of a leak, not of a powerful predictor.

| Tier | What to say |
|---|---|
| Passes | "Leakage is when future information gets into training" (correct, no demonstration) |
| Strong | The worked comparison above, and the diagnostic instinct it teaches: a suspiciously high score (especially near-perfect) plus one feature dominating importance is the classic leakage fingerprint |
| Extra points | **[+Validate]** the measured jump from 0.932 to 1.000 and the 0.29/0.71 importance split, not an assumed pattern<br>**[+Evidence]** the same thing on Riverstone's leads: adding `has_quote`, filled in only for leads already going well, lifts validation AUC from 0.823 to 0.978 |

**Likely follow-ups:** Name three real-world sources of target leakage beyond a literal copy of the label. How would you catch this without already suspecting a specific column?
**Red flag:** treating a near-perfect score as good news rather than the first thing to investigate.
**Learn it in:** Chapter 36, section 36.7 (three leaky features and one contaminated encoding, each added one at a time with its AUC, and the leakage checklist); Chapter 37, section 37.7 (random forests and `feature_importances_`).

### Q74-020 · What's temporal leakage, and why is a random train/test split dangerous for time-ordered data?

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *A model trained on the future to predict the past will look brilliant and mean nothing. Always split by time when time is part of the story.*

**Answer in one line:** **Temporal leakage** happens when information from *after* the prediction moment sneaks into training, most commonly through a random (not time-based) train/test split on time-series or event data, letting the model learn from outcomes that hadn't happened yet at the point it's meant to predict.

| Tier | What to say |
|---|---|
| Passes | "You should split time series data by time, not randomly" (correct, no reasoning given) |
| Strong | Explains that a random split puts rows from *after* a test row's date in the training set, so features that quietly encode "what eventually happened" leak through |
| Extra points | **[+Evidence]** Riverstone's lead model scored *lower* on a random split (0.791) than on the proper time split (0.823), the *opposite* of what leakage usually does<br>**[+Limits]** the honest explanation: it wasn't leakage, it was a real shift in the lead mix over time. A lower score isn't automatically "more honest"; you have to know *why* the numbers differ |

**Likely follow-ups:** How would you build a time-respecting cross-validation scheme, not just a single split? What's a rolling-origin backtest?
**Red flag:** assuming every score difference between a random and a time-based split is explained by leakage.
**Learn it in:** Chapter 36, sections 36.3 (split by time) and 36.10 ("Back to the random split"); Chapter 40, section 40.7 (backtesting).

### Rapid-fire, 74.4

Roles: DS and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q74-021 | What's target encoding leakage? | Encoding a categorical feature with the target's mean computed on the *same* rows being scored, silently baking outcome information into the feature | **[+Evidence]** company win rates computed on all leads lift validation AUC from 0.823 to 0.845, on company names that carry no real signal; `TargetEncoder` inside the pipeline gives the honest 0.823 | Mid · 36.7 ("Contamination") |
| Q74-022 | Why is fitting a scaler or encoder on the full dataset before splitting a leakage risk? | Its learned values (mean, standard deviation, category list, category win rates) are computed partly from test rows, so a little of the test set shapes training | **[+Evidence]** fitting the *target encoder* before cross-validation inflated AUC from 0.78 to 0.82; a scaler fitted on all rows leaks far less, but the fix is the same pipeline | Mid · 36.9 |
| Q74-023 | What's the fastest sanity check for suspected leakage in a model that scores too well? | Check what the score does as you remove features one at a time, especially any that are suspiciously predictive alone, or recorded at or after the outcome moment | **[+Signpost]** start with the one feature carrying a large share of the importance, especially one that "sounds like" the answer; permutation importance is the more reliable way to find it | Mid · 36.7; 39.8 |
| Q74-024 | Can leakage happen even with a properly time-ordered split? | Yes: a feature aggregated "as of today" that includes same-day or future data (a rolling window without a shift, say) leaks even inside a correctly time-split pipeline | **[+Limits]** leaks aren't always dramatic: Chapter 40's leaky rolling means made the forecast look only half a point better (WAPE 8.9% against an honest 9.4%) | Mid · 40.6 (the `.shift(1)` before `.rolling()` rule) and its exercise 10 |

---

## 74.5 Feature engineering

### Q74-025 · A categorical feature has 500 unique values. What are your options, and what's the trade-off for each?

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *One-hot blows up your feature count. Target encoding risks leakage. Frequency or hashing keeps it small and safe, at the cost of some information.*

**Answer in one line:** One-hot encoding (500 new columns, sparse and unwieldy for a high-cardinality feature), target encoding (compact, but a real leakage risk unless it's fitted inside the pipeline, Q74-021), frequency encoding (replace each category with how often it appears: simple and safe, but loses category-specific signal), or feature hashing (a fixed number of columns, at the cost of occasional collisions between unrelated categories).

**Beyond the book: frequency encoding and feature hashing.** Chapter 36 teaches one-hot and target encoding; these two are new here. **Frequency encoding** replaces each category with its share of the rows. **Feature hashing** runs each category through a hash function (Chapter 45, section 45.5) and uses the result to pick one of a fixed number of columns, so 500 categories, or 50,000, still make, say, 32 columns. Two different categories can land in the same column: a **collision**. Here are both on four company names:

```python
import pandas as pd
from sklearn.feature_extraction import FeatureHasher

company = pd.Series(["Lotus Kitchenware", "Metro Mart", "Lotus Kitchenware", "Sharma Hardware"])
share = company.value_counts(normalize=True)
print("frequency:", company.map(share).to_list())

hasher = FeatureHasher(n_features=8, input_type="string", alternate_sign=False)
hashed = hasher.transform([[name] for name in company]).toarray()
print("hashed column for each row:", hashed.argmax(axis=1))
```

```
frequency: [0.5, 0.25, 0.5, 0.25]
hashed column for each row: [7 7 7 5]
```

**How it works:**

- `value_counts(normalize=True)` gives each name's share of the rows instead of its count (Chapter 18); `.map(share)` looks up each row's name in that table, and `.to_list()` prints the result as a plain list. Lotus Kitchenware is half the rows, so it becomes 0.5.
- `FeatureHasher(n_features=8, ...)` will make 8 columns. `input_type="string"` says each row is a list of text values, which is why each name is wrapped in its own list, `[name]`. `alternate_sign=False` keeps every entry at +1 (by default some are −1, a trick that makes collisions cancel out on average).
- `.transform(...)` returns a sparse matrix (mostly zeros, stored compactly); `.toarray()` turns it into an ordinary NumPy array. Each row has a single 1, in the column its name hashed to, and `.argmax(axis=1)` finds that column: the position of the largest value in each row (Chapter 35, section 35.8).

**Reading it.** Two different companies, Lotus Kitchenware and Metro Mart, landed in the same column, 7: a collision, so the model can't tell them apart. **What happens if you change it:** give the hasher 16 columns instead of 8.

```python
hasher16 = FeatureHasher(n_features=16, input_type="string", alternate_sign=False)
print(hasher16.transform([[name] for name in company]).toarray().argmax(axis=1))
```

```
[ 7 15  7  5]
```

`hasher16` is the same `FeatureHasher` call with `n_features=16`, and the same `.transform(...)`, `.toarray()` and `.argmax(axis=1)` on the four `company` rows. Metro Mart moves to column 15 and the collision is gone. More columns mean fewer collisions, at the cost of a wider table; with 500 real categories, a few collisions are the price of a small, fixed table.

| Tier | What to say |
|---|---|
| Passes | Names one-hot encoding as the only option, without acknowledging it scales poorly with cardinality |
| Strong | Names at least two alternatives with the trade-off for each, as above |
| Extra points | **[+Trade-offs]** the right choice depends on the model: tree-based models cope with compact encodings (target or frequency) well; linear and distance-based models need the number of columns actively managed<br>**[+Edge cases]** a category that appears in test data but never in training: one-hot gives it all zeros (`handle_unknown="ignore"`), target encoding falls back to the overall mean, and hashing still gives it a column |

**Likely follow-ups:** How would you safely do target encoding without leaking? What's the risk of a rare category appearing in test data but not training data?
**Red flag:** treating one-hot encoding as the universal default regardless of cardinality.
**Learn it in:** Chapter 36, sections 36.4 (`OneHotEncoder`), 36.6 ("Categories": one-hot, ordinal, and the high-cardinality row) and 36.7 (target encoding inside the pipeline). Frequency encoding and hashing are new here.

### Rapid-fire, 74.5

Roles: DS and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q74-026 | Why log-transform a skewed numeric feature like quantity or revenue before modeling? | It compresses a long right tail, reduces the pull of extreme values on linear-model coefficients and distances, and often makes the relationship with the target closer to linear | **[+Edge cases]** use `np.log1p` (the log of 1 + *x*) so zeros are allowed, and cap impossible values first | Fresher · 36.6 |
| Q74-027 | What's an interaction feature, and when do you need one explicitly? | A feature built from two others (a product, a ratio, a flag for "both") to capture an effect that depends on both together; needed explicitly for linear models, which don't discover interactions the way trees can | **[+Evidence]** hospitality leads in August–October are won 8.9% of the time against 6.4% in other months: an interaction of segment and month | Mid · 36.6 ("Dates and times") |
| Q74-028 | Should missing values always be imputed with the mean? | No: sometimes the fact that a value is *missing* is itself informative (worth a separate missing-indicator flag), and imputing blindly can hide that signal | **[+Evidence]** leads with no quantity are won 5.71% of the time against 8.06% when it's given, because marketplace forms let buyers skip the box | Fresher · 36.8 |
| Q74-029 | What's the risk of engineering features "as of today" instead of "as of the prediction moment"? | It silently recreates temporal leakage (Q74-020): a feature aggregated from data that didn't exist yet at the real prediction time | **[+Edge cases]** use the time an event was *logged*, not when it's said to have happened; backdated entries leak | Mid · 36.6 ("Aggregates from activity logs") |

---

## 74.6 Model debugging

### Q74-030 · A model scores well in offline evaluation but performs noticeably worse once deployed. Walk through how you'd debug it

**Level:** Senior · **Roles:** MLE, DS

**Remember it as:** *"It worked in training" and "it works in production" are different claims. The gap is almost always a difference between what the model saw then and what it's seeing now.*

**Answer in one line:** Check, in order: (1) **training-serving skew**, the same feature computed differently in training and in production (different code, different timing, different defaults for blanks); (2) **data drift**, the inputs have shifted since training; (3) **feature availability**, a feature present in training but missing or late at serving time; (4) **label delay**, the outcomes arrive weeks later, so live accuracy can't be measured yet (monitor the inputs and predictions until it can); and (5) **silent pipeline bugs**, a join, a default value, or a type conversion behaving differently in production.

| Tier | What to say |
|---|---|
| Passes | "Maybe the data changed" (a reasonable first guess, no structured process) |
| Strong | The five-category checklist above, with a proposed order to check them in |
| Extra points | **[+Evidence]** the churn forest's top features (days since the last order, then late-payment days) are the first ones to recompute in production and compare against their training distributions<br>**[+Limits]** input drift isn't model decay: in Chapter 56's six months, new lamps pushed PSI to 4.4 while recall held (96.8% → 96.5%); then a new mould cut recall to 84.4% with no input alarm at all. Monitor outcomes, not just inputs<br>**[+Simple first]** the fastest check is comparing a production feature's distribution with its training-time distribution for the same population, before touching the model |

**Likely follow-ups:** How would you set up ongoing monitoring to catch this before a stakeholder notices? What's the difference between concept drift and data drift?
**Red flag:** jumping to "retrain the model" as the first response, before diagnosing what actually changed.
**Learn it in:** Chapter 56, sections 56.1 (data and concept drift), 56.7 (monitoring in three layers), 56.8 (drift, measured) and 56.11 (training-serving skew and feature stores); Chapter 39, section 39.10 (model cards); Chapter 37, section 37.7 (the churn forest's feature importances).

### Rapid-fire, 74.6

Roles: DS and MLE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q74-031 | Your model's feature importances put a customer ID or row-order column near the top. What does that suggest? | A strong sign of leakage or a pipeline bug (an unshuffled split, an ID that tracks signup date, duplicates across train and test), not a real predictive relationship | **[+Business]** an ID should never be predictive on its own; if it looks like it is, something upstream is wrong | Mid · 36.7 (leakage checklist) |
| Q74-032 | Training loss keeps falling but validation loss starts rising partway through training. What's happening, and what do you do? | Overfitting in progress; use early stopping (keep the model from the epoch with the best validation score) rather than training to the lowest possible training loss | **[+Evidence]** Chapter 43's churn network: validation AUC peaks at 0.773 around epoch 200 and slides to 0.730 by epoch 500 while training loss keeps falling | Mid · 43.5 and its exercise 8; 53.3, 53.6 (`early_stopping=True`) |
| Q74-033 | A model performs very differently across two customer segments. Is that automatically a problem? | Not automatically, but it needs investigating: check whether it reflects a real difference in the segments' base rates (calibrated correctly for both) or an unfair, uncalibrated gap | **[+Clarify]** "Different how: in ranking, in calibration, or in who gets flagged?" Each has its own fix | Senior · 39.9 |
| Q74-034 | You retrain a model monthly and its performance quietly degrades over several cycles. What would you check first? | Whether the data itself has drifted (a changing lead mix, a new customer segment, a process change upstream) before assuming the modeling approach has stopped working | **[+Evidence]** the marketplace's share of Riverstone's leads rose from 30.1% (2023) to 44.5% (2025), and its win rate halved in 2025 | Mid · 36.3; 56.9 |

---

## 74.7 ML case studies and live-coding walk-throughs

### Q74-035 · Case study: a vendor pitches a "91% accurate" deep-learning churn model. Walk through how you'd evaluate the claim, live

**Level:** Mid · **Roles:** DS, DA

**What they're really testing:** whether you reach for the base rate and the right metrics before being impressed by a headline number, under real conversational pressure.

**Talked through live:** "First question: what's the actual churn rate in their data? If it's anywhere near 9%, predicting 'no churn' for everyone would already be about 91% accurate, so that number alone tells me almost nothing yet."

**From Chapter 37, section 37.0:** Riverstone's churn rate is 9.7% (484 of 5,000 accounts), so predicting "no churn" for everyone is **90.3%** accurate.

**Talked through, live:** "Their 91% is barely above the do-nothing baseline of 90.3%. I'd ask for AUC and log loss, compared against that same baseline, not accuracy, and I'd ask what their model was trained on. 'Deep learning' on its own tells me nothing about whether it beats a well-tuned simpler model: on our own churn accounts, a small neural network scored a test AUC of 0.818, against 0.797 for logistic regression and 0.821 for gradient boosting."

**Extra-point moves shown:** **[+Clarify]** asked for the base rate before reacting to the headline number. **[+Validate]** the real comparison, not an assumed one. **[+Business]** proposed the concrete next step (ask for AUC and log loss against the baseline) rather than just expressing skepticism.

**Likely follow-ups:** What if the vendor's AUC actually did beat your own model's? What questions would you ask about their training data before trusting it?
**Red flag:** being impressed by a percentage with no base-rate context.
**Learn it in:** Chapter 43's "In the real world" (a conference talk's 91% accuracy claim, with the base-rate check as the deciding question) and Chapter 35's "In the real world" (a vendor's 91% lead score, turned into a pilot with a pass mark).

### Q74-036 · Case study: which algorithm would you reach for first, and how would you know if you're wrong?

**Level:** Senior · **Roles:** DS, MLE

**What they're really testing:** whether "it depends" gets followed by an actual decision process, not left as a dodge.

**Talked through live:** "For a first pass on a new tabular business problem, I'd start with logistic regression as a fast, interpretable baseline, then try gradient boosting as the strong default, and I'd know I picked wrong if boosting doesn't clearly beat the baseline on held-out data. That would suggest the relationships in the data are mostly additive, and the added complexity isn't earning its keep."

**From Chapter 37, sections 37.11 and 37.12**, test AUC, each scored once:

| Data | Plain logistic regression | Tuned gradient boosting | Logistic + engineered features |
|---|---:|---:|---:|
| Churn accounts (37.11) | 0.797 | 0.838 | **0.850** |
| Leads (37.12) | **0.838** | 0.830 | — |

**Talked through, live:** "On churn, boosting beat the *plain* baseline by 0.04, but a logistic model with engineered features beat boosting, and it's explainable. On leads, boosting didn't win at all; the signal is mostly additive. That's why I always run the baseline, and a *good* baseline, before trusting the complex model."

**Extra-point moves shown:** **[+Trade-offs]** named a concrete decision rule ("did the complex model clearly beat the baseline?") instead of a vague "try a few things." **[+Evidence]** cited two different, real outcomes from the same body of work, showing the answer depends on the data rather than reciting "boosting always wins." **[+Validate]** added a third data point: in Chapter 43, a small neural network on the churn accounts landed between logistic regression and boosting (validation AUC 0.764, 0.773, 0.786).

**Likely follow-ups:** How would you decide "clearly beat," in numbers? What would make you skip straight to a more complex model without trying logistic regression first?
**Red flag:** naming one algorithm as a universal answer with no acknowledgment that it depends on the data.
**Learn it in:** Chapter 37, sections 37.10 ("Fixing bias with features"), 37.11 (tuning and the one-time test) and 37.12 (lead scoring, baseline vs boosting); Chapter 43, section 43.5 (the honest comparison).

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Reporting accuracy alone on an imbalanced problem | A headline number barely above the base rate | Always state the base rate; use precision, recall, PR-AUC |
| Treating high AUC as proof of trustworthy probabilities | A confidently wrong "94% chance" shown to a stakeholder | Check calibration separately from ranking (Q74-014) |
| A suspiciously perfect or near-perfect score | The model has learned the target from a leaked feature | Check feature importance for one dominant column; question the top feature specifically |
| A random train/test split on time-ordered data | An offline score that doesn't hold up once deployed | Split by time; backtest with rolling origins |
| Jumping to "retrain the model" when production performance drops | The real cause (a pipeline bug, drifted inputs) goes unaddressed | Check training-serving skew and data drift before retraining |
| Assuming more features always helps | Perfect training score, poor test score, especially with few rows | Check the rows-to-features ratio; regularize; validate on held-out data |
| Judging a model on one small test set | A "trend" that's really luck (0.58 one run, 0.32 the next) | Cross-validate, or average several splits, before comparing |
| Picking a complex model without a baseline | No way to tell whether the complexity was worth it | Always run the simplest reasonable baseline first, and compare |

---

## In the real world: the feature importance that gave away the bug

Priyanka, a Data Scientist candidate, is shown a model with a suspiciously strong 0.97 AUC and asked to find what's wrong. Rather than guessing, she asks to see the feature importance table first, and immediately flags the top feature: `days_since_status_change`, contributing nearly half the model's total importance.

She reasons out loud: "That column name suggests it's updated *when* the status changes, which for a churn model probably means it gets updated right around, or even after, the churn event itself. If that's true, the model isn't predicting churn, it's detecting that churn has already been recorded." The interviewer confirms: the feature was indeed set at the moment an account was marked churned, a close cousin of this chapter's own leaked-feature demonstration.

The interviewer's note afterward: *"Went straight to feature importance, and reasoned about the specific column name rather than asking to see more code. Diagnosed the leak from the name and the number alone, before we even opened the data."* That's this chapter's whole method in miniature: a suspicious score plus a dominant feature is the fingerprint, and naming *why* a specific feature is suspicious, not just that leakage is possible in general, is what separates a strong answer from a correct-sounding one.

---

## Project

**Goal:** reproduce this chapter's core demonstrations on your own model or data.

### Tools you'll need

**scikit-learn**, **pandas**, and **NumPy**, the same stack used throughout Chapters 35–43 (scikit-learn is installed in Chapter 35, section 35.9). No new tools: `FeatureHasher` is part of scikit-learn.

1. Run your own bias-variance sweep (varying maximum depth, regularization strength, or a similar complexity setting) on a real model, and find where the sweet spot actually sits, not where you'd guess it sits.
2. Deliberately leak a feature into a model you control (a noisy copy of the target, or a feature computed after the outcome) and measure exactly how much the score inflates.
3. Take a model you've built with a random split and rebuild it with a time-based split if your data has any time order; compare the two honestly.
4. Pick one of your own models and write a two-sentence "how I'd debug this in production" plan, using the five-category checklist of Q74-030, before you need it for real.

---

## Key terms

bias-variance trade-off · underfitting · overfitting · regularization (L1/L2) · learning curve · curse of dimensionality · adjusted R² · base rate · confusion matrix · precision · recall · F1 score · macro and weighted F1 · ROC-AUC · PR-AUC · calibration · target leakage · temporal leakage · target encoding leakage · training-serving skew · data drift · concept drift · label delay · feature importance · early stopping · one-hot encoding · frequency encoding · feature hashing · hash collision · interaction feature · missing-value indicator

---

## Final-week revision list

Q74-001, Q74-002, Q74-007, Q74-008, Q74-013, Q74-014, Q74-015, Q74-016, Q74-019, Q74-020, Q74-021, Q74-025, Q74-030, Q74-031, Q74-035, Q74-036.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 79, GenAI, LLM & MLOps Question Bank,** takes Q74-030's monitoring and skew questions into feature stores and LLM-based systems.
- **Chapters 35–43** are where every technique this bank draws on was taught in full; this chapter tests them, it doesn't re-teach them. When an interview pushes past "the model predicts X" into "does changing X actually cause the outcome?", go back to **Chapter 30** (experiments) and **Chapter 31** (causal inference).
