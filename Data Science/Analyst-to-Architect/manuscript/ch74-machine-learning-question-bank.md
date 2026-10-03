# Chapter 74. Machine Learning Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the ML questions that come up across screening calls, live-coding rounds, and case interviews for Data Scientist, ML Engineer, and analytics-adjacent roles · explain bias and variance, not just define them · spot data leakage before a model's score fools you · read a confusion matrix, an ROC curve, and a calibration plot the way an interviewer actually wants · debug a model that "worked in training and broke in production."
>
> **Before you start:** Part 4 (Chapters 35–43), which teaches every idea in this bank; Chapter 53, section 53.3 (early stopping) and Chapter 56 (monitoring, drift, training-serving skew) for section 74.6; Chapter 69 for the three answer tiers and the twelve extra-point tags. This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** 8–10 hours for a first pass: about 10 minutes per core question answered aloud, 1–2 minutes per rapid-fire row, and about an hour to run the four code demos yourself. Section 74.8 adds about 1½ hours and is worth a sitting of its own, with the code running beside you. Plus 1 hour for the final-week list.
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

## 74.8 Predict the number: what the library did that you did not ask for

The rest of this chapter tests whether you understand the modelling: bias and variance, leakage, calibration, thresholds. This section tests something narrower. Every question below is a model that trains without warning, scores plausibly, and reports a number that is not what you think it is — because scikit-learn made a choice on your behalf and did not mention it.

That is a different skill from knowing the theory, and it is the one that shows up in a live-coding round. An interviewer who hands you a notebook and asks "what will this print?" is finding out whether you have read the defaults or only the tutorials.

Read the setup, say the number, then read on.

**How these were run.** scikit-learn 1.9.0, numpy 2.4.3, pandas 3.0.2, every random state fixed, so each cell reproduces. The setup cell for this section:

```python
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

rng = np.random.default_rng(74)
```

### Q74-037 · `clf.score(X, y)` and `reg.score(X, y)`: are they the same metric?

**Level:** Fresher · **Roles:** DA, DS, MLE

**Remember it as:** *`.score()` means accuracy on a classifier and R² on a regressor. Same method name, different number, no warning.*

**Answer in one line:** No — a classifier's `.score()` returns accuracy and a regressor's returns R², so the same call on two models gives two numbers that are not comparable and are not labelled.

```python
clf = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
print(f"classifier .score() = {clf.score(X_te, y_te):.4f}")
print(f"accuracy_score      = {accuracy_score(y_te, clf.predict(X_te)):.4f}")

reg = LinearRegression().fit(X_tr2, y_tr2)
print(f"regressor .score()  = {reg.score(X_te2, y_te2):.4f}")
print(f"r2_score            = {r2_score(y_te2, reg.predict(X_te2)):.4f}")
```

```
classifier .score() = 0.9222
accuracy_score      = 0.9222
regressor .score()  = 0.9365
r2_score            = 0.9365
```

Both land near 0.93 and they mean entirely different things. 0.9222 is "92% of labels correct". 0.9365 is "the model explains 94% of the variance". One is bounded at 1 and floored at 0; the other is bounded at 1 and has no floor at all (Q74-038).

The practical damage is in comparison tables. A notebook that loops over models and collects `.score()` into a dataframe produces a column with no unit, and if the loop ever mixes a classifier with a regressor the column silently mixes metrics. The same applies to `cross_val_score` without an explicit `scoring=`, which defaults to the estimator's own `.score`.

Always name the metric:

```python
cross_val_score(model, X, y, cv=5, scoring='roc_auc')
```

| Tier | What to say |
|---|---|
| Passes | "One's accuracy and one's R²" |
| Strong | + that `cross_val_score` inherits the same default, so an unlabelled score column can mix metrics, and that passing `scoring=` explicitly is the fix |
| Extra points | **[+Validate]** a results table whose metric column has no name is the smell · **[+Business]** accuracy and R² near 0.93 tell a stakeholder nothing comparable, and reading them as the same number is an easy mistake to invite · **[+Edge cases]** a clustering estimator's `.score()` is different again, and some have none |

**Likely follow-ups:** What does `cross_val_score` default to? How would you compare a classifier and a regressor fairly? *(You cannot directly; pick a metric that answers the business question.)*
**Red flag:** reporting `.score()` without saying what it is.
**Learn it in:** Chapter 36, section 36.7 (evaluation); Chapter 74, section 74.3.

### Q74-038 · Can R² be negative?

**Level:** Fresher · **Roles:** DA, DS, MLE

**Remember it as:** *R² is not r squared. It is 1 minus (your error ÷ the error of predicting the mean), and if you are worse than the mean it goes below zero.*

**Answer in one line:** **Yes** — R² is −3.0 for a model that is worse than predicting the mean, 0 for predicting the mean exactly, and 1 for a perfect fit; the "squared" in the name refers to squared errors, not to a quantity that must be positive.

```python
y_true = np.array([10.0, 12, 14, 16, 18])
for name, pred in [('worse than the mean', np.array([18.0, 16, 14, 12, 10])),
                   ('the mean itself',     np.full(5, y_true.mean())),
                   ('perfect',             y_true.copy())]:
    print(f"{name:<22} R2 = {r2_score(y_true, pred):+.4f}")
```

```
worse than the mean    R2 = -3.0000
the mean itself        R2 = +0.0000
perfect                R2 = +1.0000
```

The formula is 1 − SS_res/SS_tot. Predicting the mean makes those two equal, so R² is 0 — that is the baseline, not the floor. Do worse and the ratio exceeds 1, and R² goes negative without limit.

Where you actually meet a negative R² is on the **test set**, and it is one of the most informative numbers in machine learning when you do. It says your model is worse than a constant. That usually means one of three things: the model is overfit beyond rescue, the test set comes from a different distribution than the training set, or something is wrong with the pipeline — a shuffled target, a misaligned index after a join, a scaler fitted in the wrong place.

The name confusion is worth clearing up out loud: for a simple linear regression with an intercept, R² does happen to equal the square of Pearson's r. That coincidence is where the name comes from, and it stops being true for any other model.

| Tier | What to say |
|---|---|
| Passes | "Yes, if the model is worse than the mean" |
| Strong | + the formula and the three reference points (−3, 0, 1), and that 0 is the baseline rather than the floor |
| Extra points | **[+Validate]** a negative test R² is a strong signal of a pipeline bug, not just a weak model — check for a shuffled target or a misaligned index first · **[+Edge cases]** R² equals r² only for simple linear regression with an intercept · **[+Business]** "the model explains −300% of the variance" is not a sentence to put in a slide; say "worse than guessing the average" |

**Likely follow-ups:** What is adjusted R²? Can it be negative too? *(Yes, more easily.)* Why does adding a feature never decrease *training* R²?
**Learn it in:** Chapter 22, section 22.10 (regression); Chapter 74, Q74-009.

### Q74-039 · Halve every predicted probability. What happens to AUC, and to accuracy?

**Level:** Brain-racking · **Roles:** DS, MLE

**Remember it as:** *AUC only reads the order of the scores. Accuracy reads the scores against a threshold. Rescale and one does not move at all while the other collapses.*

**Answer in one line:** AUC is **completely unchanged** at 0.949532 — through halving, cubing, and taking logs — while accuracy at a 0.5 threshold falls from 0.9222 to 0.6500, because AUC depends only on the ranking and accuracy depends on where the scores sit relative to the cut-off.

```python
p = clf.predict_proba(X_te)[:, 1]

print(f"AUC with p        = {roc_auc_score(y_te, p):.6f}")
print(f"AUC with p/2      = {roc_auc_score(y_te, p/2):.6f}")
print(f"AUC with p**3     = {roc_auc_score(y_te, p**3):.6f}")
print(f"AUC with log(p)   = {roc_auc_score(y_te, np.log(p)):.6f}")
print(f"accuracy on p     = {accuracy_score(y_te, (p > 0.5).astype(int)):.4f}")
print(f"accuracy on p/2   = {accuracy_score(y_te, (p/2 > 0.5).astype(int)):.4f}")
```

```
AUC with p        = 0.949532
AUC with p/2      = 0.949532
AUC with p**3     = 0.949532
AUC with log(p)   = 0.949532
accuracy on p     = 0.9222
accuracy on p/2   = 0.6500
```

Four transformations, six decimal places, not one digit different. Halving, cubing and logging are all **monotonic**: they change the values and preserve the order. AUC is computed entirely from the order — it is the probability that a randomly chosen positive outranks a randomly chosen negative — so none of them touches it.

Accuracy is a different kind of measurement. It asks whether each score is above 0.5, and halving every score pushes most of them below, so a quarter of the test set changes class and accuracy falls 27 points.

Three consequences, and they are what the question is really testing:

**AUC cannot detect a calibration problem.** A model whose probabilities are all systematically too low — a common result of training on resampled data — has perfect AUC and useless probabilities. If anyone downstream multiplies the probability by a value to get an expected return, AUC will never warn them. That is Q74-014's point arriving from the other side.

**AUC cannot be improved by changing the threshold**, because it already summarises every threshold at once. "We tuned the threshold and AUC went up" is not possible, and hearing it is a useful signal.

**A model can have better AUC and worse accuracy than another**, and neither number is lying. They answer different questions: can it rank, and does it decide correctly at this cut-off.

| Tier | What to say |
|---|---|
| Passes | "AUC doesn't change, it's rank-based" |
| Strong | + that *any* monotonic transform leaves it identical, with accuracy's collapse as the contrast, and the definition of AUC as a ranking probability |
| Extra points | **[+Business]** AUC is blind to calibration, so a model used for expected-value decisions needs Brier score or a reliability curve as well · **[+Validate]** "we improved AUC by moving the threshold" is impossible and signals a misunderstanding · **[+Edge cases]** a *non*-monotonic transform does change AUC, which is why a poorly chosen feature transform can hurt ranking |

**Likely follow-ups:** What transform *would* change AUC? How would you measure calibration? *(Brier score, reliability curve.)* Does this apply to PR-AUC? *(Yes, also rank-based.)*
**Red flag:** saying AUC falls. It is the answer that follows from treating AUC as "accuracy, but better".
**Learn it in:** Chapter 74, section 74.3 (metrics and calibration); Chapter 36, section 36.7.

### Q74-040 · `train_test_split` on data that is 5% positive, with no `stratify`

**Level:** Mid · **Roles:** DA, DS, MLE

**Remember it as:** *A random split is random about the rare class too. On 5% positives it will hand you a test set with anywhere from 4% to 10%.*

**Answer in one line:** The test set's positive rate ranges from **4.0% to 10.0%** across eight seeds — 8 positives in one split and 20 in another, out of the same data — so a model's apparent performance moves with the seed and not with the model.

```python
print(f"overall positive rate: {y.mean():.4f}")

rates = []
for seed in range(8):
    _, _, _, y_te = train_test_split(X, y, test_size=0.2, random_state=seed)
    rates.append(y_te.mean())
print(f"no stratify: min {min(rates):.4f}, max {max(rates):.4f}")
print(f"positives in the test set: {[int(r*200) for r in rates]}")

srates = [train_test_split(X, y, test_size=0.2, random_state=s, stratify=y)[3].mean()
          for s in range(8)]
print(f"stratify=y:  min {min(srates):.4f}, max {max(srates):.4f}")
```

```
overall positive rate: 0.0500
no stratify: min 0.0400, max 0.1000
positives in the test set: [9, 8, 8, 10, 8, 10, 20, 14]
stratify=y:  min 0.0500, max 0.0500
```

Look at that list of counts. One seed gives the test set 8 positives; another gives it 20. Every metric that depends on the positive class — recall, precision, PR-AUC — is being computed on a sample that varies by a factor of two and a half, for reasons that have nothing to do with the model.

`stratify=y` pins the proportion exactly in both halves, at no cost. It should be the default thing you type for any classification problem, and it matters more the rarer the class: at 0.5% positive, a 20% test set of 1,000 rows expects 10 positives and will routinely get 4 or 16.

The same applies to cross-validation, and there scikit-learn is on your side: `cross_val_score` with a classifier uses `StratifiedKFold` automatically. It does not do the same for `train_test_split`, which is exactly the inconsistency that catches people.

| Tier | What to say |
|---|---|
| Passes | "You should use `stratify`" |
| Strong | + the measured spread (4% to 10%, 8 to 20 positives), and that every positive-class metric inherits that variance |
| Extra points | **[+Edge cases]** `cross_val_score` stratifies automatically for classifiers but `train_test_split` does not, which is why the habit does not transfer · **[+Scale]** the rarer the class, the worse it gets; below about 1% a single split is not a reliable estimate at all · **[+Trade-offs]** with very few positives, repeated stratified CV beats any single split · **[+Validate]** print the positive count in each split before trusting a comparison |

**Likely follow-ups:** How would you split time-ordered data? *(Not randomly at all — Q74-020.)* What if you have groups, like multiple rows per customer? *(`GroupKFold`, or you leak.)* Does stratify work for regression? *(Not directly; bin the target first.)*
**Learn it in:** Chapter 36, section 36.3 (splitting); Chapter 74, section 74.4.

### Q74-041 · `cross_val_score(model, X, y, cv=5)` on data sorted by the target

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *`cv=5` does not shuffle. On a classifier it stratifies and hides the problem; on a regressor it does not, and each fold gets its own slice of the target range.*

**Answer in one line:** **0.930 against 0.997** — the folds are contiguous blocks of a sorted target, so each one trains on a range that excludes the range it is tested on, and the score understates the model by seven points for no modelling reason.

```python
X, y = make_regression(n_samples=500, n_features=5, noise=10, random_state=74)
order = np.argsort(y)
X_sorted, y_sorted = X[order], y[order]

no_shuffle = cross_val_score(LinearRegression(), X_sorted, y_sorted, cv=5)
shuffled   = cross_val_score(LinearRegression(), X_sorted, y_sorted,
                             cv=KFold(5, shuffle=True, random_state=74))

print(f"cv=5, no shuffle:        {np.round(no_shuffle, 3)}  mean {no_shuffle.mean():.3f}")
print(f"KFold(shuffle=True):     {np.round(shuffled, 3)}  mean {shuffled.mean():.3f}")
```

```
cv=5, no shuffle:        [0.988 0.912 0.881 0.888 0.981]  mean 0.930
KFold(shuffle=True):     [0.997 0.997 0.997 0.996 0.998]  mean 0.997
```

The middle folds are the worst, which is the signature: fold 3 holds the middle of the target range and trains on the two tails, so it has to interpolate from data on either side. The outer folds hold the extremes and do better because the model extrapolates from a contiguous range next to them.

Here the damage is mild because the relationship is genuinely linear and extrapolates well. Change the model to something that cannot extrapolate — a tree, a random forest, anything that predicts within the range it saw — and a fold holding the top 20% of the target becomes unscoreable, because the model has never seen a value that large.

The asymmetry is the part worth memorising: **`cv=5` means `StratifiedKFold` for a classifier and plain `KFold` for a regressor.** So the identical mistake is invisible on classification and expensive on regression. Pass the splitter explicitly and the question does not arise.

And sorted data is not exotic. A dataframe that arrived from a `SELECT ... ORDER BY`, a file written by date, anything grouped by customer — all of them have structure that contiguous folds will find.

| Tier | What to say |
|---|---|
| Passes | "You should shuffle" |
| Strong | + that `cv=5` does not shuffle, that it stratifies for classifiers and not for regressors, with both means |
| Extra points | **[+Edge cases]** a tree-based model cannot extrapolate, so the same split can give a strongly negative R² rather than a mild dip · **[+Validate]** fold scores that vary systematically rather than randomly — worst in the middle, best at the ends — are the tell · **[+Trade-offs]** do *not* shuffle time-ordered data; use `TimeSeriesSplit`, where contiguous folds are the whole point · **[+Edge cases]** with repeated customers, shuffling leaks instead; `GroupKFold` is the right tool |

**Likely follow-ups:** When is not shuffling correct? *(Time series — and then you want `TimeSeriesSplit`.)* What does `StratifiedKFold` do for regression? *(Nothing; bin the target yourself.)* What is `GroupKFold` for?
**Learn it in:** Chapter 36, section 36.3 (cross-validation); Chapter 74, section 74.4.

### Q74-042 · Does `LogisticRegression()` regularise by default?

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *scikit-learn's logistic regression is penalised out of the box. `C=1.0` is already shrinking your coefficients, and `C` is the inverse of the penalty.*

**Answer in one line:** **Yes** — the default `C=1.0` applies an L2 penalty, and on 60 samples with 40 features it shrinks the largest coefficient from 7.677 to 1.403, so coefficients from an untouched `LogisticRegression()` are not the maximum-likelihood estimates a statistics course would give you.

```python
X, y = make_classification(n_samples=60, n_features=40, n_informative=5, random_state=74)
for C in (0.01, 1.0, 1e6):
    m = LogisticRegression(C=C, max_iter=20000).fit(X, y)
    print(f"C={C:<8g} max|coef| = {np.abs(m.coef_).max():7.3f}   "
          f"sum|coef| = {np.abs(m.coef_).sum():8.3f}   train acc = {m.score(X, y):.3f}")
print(f"default C = {LogisticRegression().C}")
```

```
C=0.01     max|coef| =   0.138   sum|coef| =    1.107   train acc = 0.817
C=1        max|coef| =   1.403   sum|coef| =   15.675   train acc = 1.000
C=1e+06    max|coef| =   7.677   sum|coef| =   99.796   train acc = 1.000
```

`C=1e6` is effectively no penalty, and it is the setting that matches what `statsmodels`' `Logit` or R's `glm` would give you. The default is five and a half times smaller on the largest coefficient and six times smaller in total.

Two things follow.

**Your coefficients are not comparable across tools.** Fit the same data in scikit-learn and in statsmodels and the numbers differ, not because either is wrong but because one is penalised. If you are interpreting coefficients — reporting an odds ratio, arguing that a feature matters — that difference is the whole result.

**`C` is backwards from what people expect.** It is the *inverse* of regularisation strength: small `C` is strong shrinkage. The row at `C=0.01` has almost flattened the model, and its training accuracy has dropped to 0.817 as a result.

Note also that the penalty is applied to all coefficients on their own scale, which is why unscaled features get penalised unevenly — a feature measured in rupees is shrunk far harder than one measured in units. Scaling is not optional for a penalised linear model, which is the part of Q74-011's answer that matters most.

| Tier | What to say |
|---|---|
| Passes | "Yes, there's an L2 penalty by default" |
| Strong | + that `C` is the inverse of the strength, and what the default actually does to the coefficients, with numbers |
| Extra points | **[+Business]** coefficients reported as odds ratios from a default fit are penalised estimates, and differ from statsmodels or R · **[+Edge cases]** the penalty acts on the raw coefficient scale, so unscaled features are regularised unevenly · **[+Trade-offs]** for prediction the default is usually a good one; for interpretation, fit without a penalty and say so |

**Likely follow-ups:** How does this differ from statsmodels' `Logit`? What does `penalty='l1'` change? Does `LinearRegression` regularise? *(No — `Ridge` and `Lasso` are the penalised versions.)*
**Red flag:** interpreting default scikit-learn coefficients as unbiased estimates.
**Learn it in:** Chapter 36, section 36.6 (regularisation); Chapter 74, Q74-003 and Q74-004.

### Q74-043 · Shuffle the target, retrain, and score. What AUC do you get?

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *Destroy the signal and the model should land at a coin flip. Not zero — zero would mean it learned the relationship and reversed it.*

**Answer in one line:** About **0.47**, scattered around 0.5 — a model trained on a randomly permuted target has no information, and AUC for no information is 0.5, not 0.

```python
real = RandomForestClassifier(n_estimators=100, random_state=74).fit(X_tr, y_tr)
print(f"AUC, real target     = {roc_auc_score(y_te, real.predict_proba(X_te)[:,1]):.4f}")

aucs = []
for s in range(5):
    y_shuffled = np.random.default_rng(s).permutation(y_tr)
    m = RandomForestClassifier(n_estimators=100, random_state=74).fit(X_tr, y_shuffled)
    aucs.append(roc_auc_score(y_te, m.predict_proba(X_te)[:,1]))
print(f"AUC, shuffled target = {np.mean(aucs):.4f}  ({', '.join(f'{a:.3f}' for a in aucs)})")
```

```
AUC, real target     = 0.9791
AUC, shuffled target = 0.4707  (0.406, 0.520, 0.513, 0.529, 0.386)
```

The five shuffles range from 0.386 to 0.529 — scattered either side of 0.5, which is what no information looks like. An AUC *below* 0.5 is not worse than useless; it is noise, and if it were consistently and substantially below 0.5 you would have a model that had learned the relationship backwards, which usually means a flipped label.

This is the single most valuable diagnostic in the chapter, because it is a test of your **pipeline**, not your model. Run it before you trust a surprisingly good result:

- If the shuffled AUC comes back near 0.5, as it should, your evaluation is wired correctly.
- If the shuffled AUC comes back high — 0.8, 0.9 — then your pipeline can predict a *random* target, which is impossible unless information is leaking from the test set into training. A scaler fitted before the split, a feature computed over the whole dataframe, a duplicated row appearing on both sides.

That second case is the one worth rehearsing out loud, because "I permute the target as a sanity check" is a short sentence that tells an interviewer you have been burned by leakage and built a habit from it.

| Tier | What to say |
|---|---|
| Passes | "About 0.5" |
| Strong | + why 0.5 rather than 0, that individual runs scatter either side of it, and that this is a leakage test for the pipeline |
| Extra points | **[+Validate]** a high AUC on a shuffled target proves leakage, because no model can predict noise · **[+Edge cases]** consistently *below* 0.5 suggests inverted labels rather than a bad model · **[+Scale]** this is the cheap version of a permutation test; several shuffles give you a null distribution to compare the real score against · **[+Business]** run it before presenting any result that seems too good |

**Likely follow-ups:** What would a high shuffled AUC tell you? How many permutations for a proper test? What is the equivalent check for a regressor? *(R² near 0, or negative.)*
**Learn it in:** Chapter 74, section 74.4 (leakage); Chapter 36, section 36.7.

### Q74-044 · Add a column of pure random noise. What feature importance does it get?

**Level:** Brain-racking · **Roles:** DS, MLE

**Remember it as:** *Importances are shares of a fixed total, so they always add to 1 and nothing can get zero. A noise column takes its cut.*

**Answer in one line:** **0.0271**, which ranks it **5th of 11** — above the least useful genuine feature at 0.0205 — because a random forest's importances are a normalised split of a fixed budget and noise still gets chosen at some splits deep in the trees.

```python
X_noise = np.column_stack([X_tr, np.random.default_rng(74).normal(size=len(X_tr))])
rf = RandomForestClassifier(n_estimators=200, random_state=74).fit(X_noise, y_tr)
imp = rf.feature_importances_

print(f"noise column importance          = {imp[-1]:.4f}")
print(f"smallest real-feature importance = {imp[:-1].min():.4f}")
print(f"importances sum to                 {imp.sum():.4f}")
```

```
noise column importance          = 0.0271
smallest real-feature importance = 0.0205
importances sum to                 1.0000
```

A column with no relationship to the target whatsoever is rated more important than one of the real features. It is not a bug: the forest grows deep trees, and far down a tree any column can produce a split that happens to separate the handful of rows in that node.

Two properties of the default importance explain it, and naming both is the strong answer.

**They are normalised.** The sum is exactly 1.0000. Importances are shares, not evidence — adding a column takes some share from the others regardless of whether it helps.

**They favour high-cardinality features.** The default is mean decrease in impurity, which rewards a column with many distinct values because it offers many possible split points. A continuous noise column has as many split points as there are rows. This is the same mechanism that puts a customer ID at the top of an importance table (Q74-031).

So "feature importance" from this attribute answers "how much did the trees use this column", not "does this column carry information". For the second question, use something that measures it directly:

| Method | What it measures |
|---|---|
| Permutation importance on a **held-out** set | How much the score drops when that column is shuffled — the question you meant |
| SHAP values | Contribution per prediction, with direction, not just magnitude |
| Adding a known noise column | Any feature ranked below it is not demonstrably useful — a cheap, blunt, effective cut-off |

That last row is the practical trick worth stealing: deliberately include a random column, and treat its importance as the noise floor.

| Tier | What to say |
|---|---|
| Passes | "It won't be zero" |
| Strong | + the number, the fact that it beats a real feature, and both mechanisms: normalised shares and the bias towards high-cardinality columns |
| Extra points | **[+Validate]** adding a deliberate noise column gives you a noise floor to compare against · **[+Trade-offs]** permutation importance on held-out data answers the question people think they are asking, at the cost of refitting or rescoring · **[+Edge cases]** impurity importance is computed on the *training* data, so it reflects fit rather than generalisation · **[+Business]** an importance table shown to stakeholders implies "these are the drivers", which this attribute does not support |

**Likely follow-ups:** What is permutation importance? Why does it need a held-out set? How do correlated features split importance between them? *(They share it, so both look weak — related to Q74-045.)*
**Learn it in:** Chapter 36, section 36.5 (feature importance); Chapter 74, Q74-031.

### Q74-045 · Two nearly identical features. What coefficients does linear regression give them?

**Level:** Brain-racking · **Roles:** DS, MLE

**Remember it as:** *When two columns are the same, the model only needs their sum to be right. It can pick any pair that adds up — including one large positive and one negative.*

**Answer in one line:** **−1.170 and +4.166** — one coefficient comes out *negative* on a feature with a strongly positive relationship to the target, because with `corr = 0.999948` the model is free to split the true coefficient of 3 any way it likes as long as the two add to it.

```python
x1 = rng.normal(size=500)
x2 = x1 + rng.normal(0, 0.01, 500)        # x1 with a tiny jitter
y  = 3 * x1 + rng.normal(0, 0.5, 500)

lin = LinearRegression().fit(np.column_stack([x1, x2]), y)
print(f"corr(x1, x2) = {np.corrcoef(x1, x2)[0,1]:.6f}")
print(f"both features: {lin.coef_.round(3)}   sum {lin.coef_.sum():.3f}")
print(f"x1 alone:      {LinearRegression().fit(x1.reshape(-1,1), y).coef_.round(3)}")
print(f"Ridge(alpha=1):{Ridge(alpha=1.0).fit(np.column_stack([x1, x2]), y).coef_.round(3)}")
```

```
corr(x1, x2) = 0.999948
both features: [-1.17   4.166]   sum 2.996
x1 alone:      [2.997]
Ridge(alpha=1):[1.427 1.567]   sum 2.994
```

Three numbers tell the whole story. Fitted alone, x1 gets **2.997** — essentially the true 3. Fitted together with its near-twin, the pair gets **−1.170 and +4.166**, which sum to **2.996**. The model's predictions are just as good; it has simply distributed the same total differently, and the distribution is driven by the tiny jitter rather than by anything real.

That negative coefficient is the danger. Read literally it says "more of x1 means less of y", the exact opposite of the truth, and it is the sort of thing that gets reported to a business as a finding. Collinearity does not damage predictions — it damages *interpretation*, and only interpretation.

Ridge fixes it, and the last line shows how: the L2 penalty prefers small coefficients, so of all the pairs that sum to 3 it picks the balanced one, 1.427 and 1.567. Both are now positive and the sign is readable. That is the main reason to use Ridge on correlated features even when prediction is fine.

How to spot it before it embarrasses you:

- A coefficient whose **sign contradicts** the simple two-variable relationship.
- Coefficients that **change a lot** when you add or drop one feature.
- **Large standard errors** on individually insignificant coefficients while the model's overall fit is strong.
- A **variance inflation factor** above about 5 or 10.

| Tier | What to say |
|---|---|
| Passes | "Multicollinearity makes coefficients unstable" |
| Strong | + reads off the sign flip, notes that the *sum* is still correct and predictions are unaffected, and names Ridge as the fix |
| Extra points | **[+Business]** a reported negative driver that is really positive is worse than no model, because someone will act on it · **[+Validate]** VIF, or simply refitting with one feature removed and watching the other move · **[+Trade-offs]** collinearity is harmless if you only want predictions; drop a feature or use Ridge when you want to interpret · **[+Edge cases]** tree models are unaffected in prediction but split importance between the twins, making both look unimportant (Q74-044) |

**Likely follow-ups:** What is VIF? Does this hurt prediction? *(No.)* What happens with perfectly collinear columns? *(The solution is not unique; scikit-learn returns one via the pseudo-inverse rather than erroring.)* How do tree models handle it?
**Learn it in:** Chapter 22, section 22.10 (regression); Chapter 36, section 36.6 (Ridge).

### Q74-046 · k-means on age in years and income in rupees, unscaled

**Level:** Mid · **Roles:** DA, DS, MLE

**Remember it as:** *k-means measures straight-line distance. A column with a bigger range has a bigger say, and rupees beat years by a factor of two hundred million.*

**Answer in one line:** The clusters split on **income only** — the three cluster means are 767k, 592k and 410k with the age mean stuck at 40 or 41 in all three — because income's variance is 209 million times age's and Euclidean distance is dominated by whichever column has the larger numbers.

```python
raw = np.column_stack([age, income])
labels_raw    = KMeans(n_clusters=3, n_init=10, random_state=74).fit_predict(raw)
labels_scaled = KMeans(n_clusters=3, n_init=10, random_state=74).fit_predict(
                    StandardScaler().fit_transform(raw))

df = pd.DataFrame({'age': age, 'income': income, 'raw': labels_raw, 'scaled': labels_scaled})
print(df.groupby('raw')[['age', 'income']].mean().round(0).to_string())
print(df.groupby('scaled')[['age', 'income']].mean().round(0).to_string())
print(f"variance: age {age.var():,.0f}, income {income.var():,.0f}")
```

```
      age    income
raw
0    40.0  767391.0
1    41.0  410448.0
2    41.0  592122.0

         age    income
scaled
0       50.0  541810.0
1       38.0  743781.0
2       30.0  487883.0

variance: age 102, income 21,305,692,647
```

The first table is three income bands. Age is 40, 41, 41 — the algorithm has not used it at all. You could have produced the same segmentation with a single `pd.qcut` on income, and it would have been clearer and faster.

The second table is a real segmentation: a 50-year-old mid-income group, a 38-year-old high-income group, a 30-year-old lower-income group. Those are three different customers. The first table describes one variable three times.

The mechanism is the variance ratio in the last line: **209 million to one**. Euclidean distance squares the differences and adds them, so a 100,000-rupee gap contributes 10¹⁰ while a 20-year gap contributes 400. Age is not outvoted; it is invisible.

This applies to every distance-based or penalised method — k-means, kNN, SVM with an RBF kernel, PCA, and any regularised linear model (Q74-042). Tree-based models are the exception: they split one column at a time on thresholds, so the units never interact.

A caution worth adding, because it is the mature version of the answer: scaling is a **decision**, not a formality. `StandardScaler` declares that one standard deviation of age matters as much as one standard deviation of income. That is a reasonable default and it is still a claim about the business. If income genuinely should dominate, say so deliberately and weight it, rather than arriving there by leaving the units alone.

| Tier | What to say |
|---|---|
| Passes | "You need to scale first" |
| Strong | + reads both tables, names the variance ratio, and shows the unscaled version is really just income bands |
| Extra points | **[+Business]** an unscaled clustering sold as "customer segments" is a single-variable split wearing a fancier name · **[+Edge cases]** trees and gradient boosting are scale-invariant, so the same data needs no scaling there · **[+Trade-offs]** `StandardScaler` against `MinMaxScaler` against `RobustScaler` is a choice about outliers; `RobustScaler` where income has a long tail · **[+Clarify]** scaling encodes a judgement about what matters equally, so it is worth stating rather than assuming |

**Likely follow-ups:** Which scaler for skewed income? *(`RobustScaler`, or log first.)* Does this affect decision trees? *(No.)* What about PCA? *(Yes, strongly — PCA on unscaled data finds the biggest-variance column.)*
**Learn it in:** Chapter 36, section 36.4 (scaling); Chapter 39, section 39.2 (clustering).

### Rapid-fire, 74.8: defaults worth knowing

Roles: DS and MLE for every row unless stated. Everything below was run.

| # | Question | The answer, and why | Extra point |
|---|---|---|---|
| Q74-047 | `cross_val_score(m, X, y, cv=5)` — what metric? | The estimator's own `.score`: accuracy for a classifier, R² for a regressor. Pass `scoring=` explicitly | **[+Validate]** an unnamed metric column is the smell → Q74-037 |
| Q74-048 | Does `LinearRegression` regularise? | No. `Ridge`, `Lasso` and `ElasticNet` are the penalised versions; only `LogisticRegression` is penalised by default | **[+Edge cases]** which makes the two APIs inconsistent, and that inconsistency is the trap → Q74-042 |
| Q74-049 | `RandomForestClassifier` default `max_depth`? | `None` — trees grow until leaves are pure, so training accuracy is usually 1.0 and means nothing | **[+Validate]** the forest still generalises, because averaging many overfit trees is the point → Ch 37 §37.6 |
| Q74-050 | Do feature importances sum to 1? | Yes, exactly. They are shares of a fixed budget, so adding any column takes from the others | **[+Business]** a share is not evidence of a driver → Q74-044 |
| Q74-051 | `predict_proba` on a default `SVC`? | `AttributeError: This 'SVC' has no attribute 'predict_proba'`. An SVM gives a decision function, not probabilities; getting probabilities means an extra Platt-scaling fit | **[+Trade-offs]** `decision_function` is enough when you only need ranking, and costs nothing → Ch 37 §37.7 |
| Q74-052 | What does `random_state=None` mean for comparing two models? | Their scores differ by run, so a 1-point gap may be noise. Fix the seed, or compare across repeated CV | **[+Validate]** report a spread, not a single number → Ch 36 §36.3 |
| Q74-053 | `StandardScaler` fitted before the split — how bad? | Test statistics leak into training. Usually a small inflation, and it is still wrong; use a `Pipeline` so it cannot happen | **[+Scale]** `Pipeline` makes the right thing the easy thing → Q74-022 |
| Q74-054 | Accuracy of a model predicting the majority class on 99:1 data? | 99%. Which is why accuracy is the wrong headline for rare events — the same arithmetic as the rare-disease test | **[+Business]** quote precision, recall or PR-AUC instead → Q74-007, Ch 73 Q73-005 |
| Q74-055 | `n_jobs=-1` — what does it change about results? | Speed only, not the answer, provided `random_state` is fixed. A changed result means an unseeded source of randomness | **[+Validate]** results that move with `n_jobs` are a bug worth chasing → Ch 36 §36.8 |
| Q74-056 | Why might a pipeline score worse after you add a feature? | The split is fixed, so a useless feature adds variance and can lower the score by chance; and with trees it dilutes importances | **[+Edge cases]** training R² never falls when you add a feature, but test R² can → Q74-038 |

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
| Splitting an imbalanced dataset without `stratify` | Positive-class metrics move with the seed, not the model | `stratify=y` on every classification split (Q74-040) |
| `cross_val_score(..., cv=5)` on ordered data | Folds become contiguous blocks; stratified for classifiers, not for regressors | Pass the splitter explicitly, and shuffle unless the data is a time series (Q74-041) |
| Reading default `LogisticRegression` coefficients as unbiased | They are penalised at `C=1.0`, and differ from statsmodels or R | Fit with a very large `C` when you intend to interpret, and say so (Q74-042) |
| Treating `feature_importances_` as evidence a feature matters | A pure noise column scored 0.0271 and beat a real feature | Permutation importance on held-out data, or include a noise column as the floor (Q74-044) |
| Interpreting coefficients on correlated features | Signs flip; a positive driver is reported as negative | Check VIF, drop one, or use Ridge (Q74-045) |

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

bias-variance trade-off · underfitting · overfitting · regularization (L1/L2) · learning curve · curse of dimensionality · adjusted R² · base rate · confusion matrix · precision · recall · F1 score · macro and weighted F1 · ROC-AUC · PR-AUC · calibration · target leakage · temporal leakage · target encoding leakage · training-serving skew · data drift · concept drift · label delay · feature importance · early stopping · one-hot encoding · frequency encoding · feature hashing · hash collision · interaction feature · missing-value indicator · `.score()` · `scoring=` · negative R² · monotonic transform · rank-based metric · `stratify` · `StratifiedKFold` against `KFold` · `shuffle=False` · `GroupKFold` · `TimeSeriesSplit` · inverse regularisation strength (`C`) · permuted-target check · mean decrease in impurity · permutation importance · noise floor · multicollinearity · variance inflation factor (VIF) · coefficient sign flip · scale invariance · `Pipeline`

---

## Final-week revision list

Q74-001, Q74-002, Q74-007, Q74-008, Q74-013, Q74-014, Q74-015, Q74-016, Q74-019, Q74-020, Q74-021, Q74-025, Q74-030, Q74-031, Q74-035, Q74-036, Q74-039, Q74-043, Q74-045.

The last three are the predict-the-number questions that pay for themselves: AUC being untouched by any monotonic transform (Q74-039), the permuted-target check that proves your pipeline is wired correctly (Q74-043), and the coefficient sign flip that turns a positive driver into a negative one in a report (Q74-045).

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 79, GenAI, LLM & MLOps Question Bank,** takes Q74-030's monitoring and skew questions into feature stores and LLM-based systems.
- **Chapters 35–43** are where every technique this bank draws on was taught in full; this chapter tests them, it doesn't re-teach them. When an interview pushes past "the model predicts X" into "does changing X actually cause the outcome?", go back to **Chapter 30** (experiments) and **Chapter 31** (causal inference).
