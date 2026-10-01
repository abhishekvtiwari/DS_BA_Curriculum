"""Build companion/ch37/ch37-supervised-learning.ipynb and execute it, so every output is real.

Teaching shape follows the book's own rule (CLAUDE.md section 2): plain idea first, then one new
idea per cell, each cell run, its real output shown, and every line and argument explained.
"""
import pathlib, sys
import nbformat as nbf
from nbclient import NotebookClient

CH = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('.')
OUT = CH / 'ch37-supervised-learning.ipynb'

md = lambda s: nbf.v4.new_markdown_cell(s.strip())
code = lambda s: nbf.v4.new_code_cell(s.strip())

cells = []

cells.append(md(r"""
# Chapter 37 · Supervised Learning Algorithms

**What this notebook is.** The runnable half of Chapter 37. Read the chapter for the reasoning and
the worked-by-hand examples; run this to see each algorithm actually fit Riverstone's data and to
compare them on the same split.

**Before you start.** You need `accounts.csv`. Build it once from the repository root:

```
cd companion
python generate_riverstone_accounts.py
```

That writes `companion/accounts/accounts.csv`: 5,000 accounts, 9.7% of them churned. The generator
is seeded, so you get the same file every time, and the same numbers this notebook prints.

**How to read a cell.** Every code cell below is preceded by what it does and why. Run them in
order, top to bottom: each one uses names made by the cells before it.

**The question this chapter answers.** Given what Riverstone knew about an account on
31 December 2024, can we predict what happened in 2025? Two targets, so two kinds of problem:

| Target | Meaning | Kind of problem |
|---|---|---|
| `churned_2025` | 1 if the account placed no order in 2025 | **Classification**: predict a label |
| `revenue_2025` | the account's 2025 revenue in rupees | **Regression**: predict a number |

Every algorithm in this notebook is aimed at one or the other.
"""))

cells.append(md(r"""
## Setting up

One import block, so the rest of the notebook is about ideas rather than plumbing.

- `pathlib` builds file paths that work on Windows, macOS and Linux alike.
- `pandas` holds the table; `numpy` does the arithmetic underneath it.
- From `sklearn`, we import only as we go, so you can see which algorithm each name belongs to.
- `warnings.filterwarnings` hides one noisy convergence message from an under-trained model later;
  it changes nothing about the results, only the amount of red text.
""".strip()))

cells.append(code(r"""
import pathlib
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)
pd.set_option("display.width", 110)
pd.set_option("display.max_columns", 30)

print("pandas", pd.__version__, "· numpy", np.__version__)
"""))

cells.append(md(r"""
## 37.0 The data

`accounts.csv` has one row per account, describing it **as of 31 December 2024**, which the chapter
calls the *prediction moment*. Nothing in the row is from 2025, because at the moment of predicting
you would not have had it. That discipline is what stops the model learning from the future, the
mistake Chapter 36 calls leakage.

The two 2025 columns are the targets, and they are the only columns from 2025.
"""))

cells.append(code(r"""
ACCOUNTS = pathlib.Path("..") / "accounts" / "accounts.csv"
accounts = pd.read_csv(ACCOUNTS)

print(f"{len(accounts):,} accounts · {len(accounts.columns)} columns")
print(f"churn rate: {accounts['churned_2025'].mean():.1%}")
print(f"median 2025 revenue: Rs {accounts['revenue_2025'].median():,.0f}")
accounts.head(3)
"""))

cells.append(md(r"""
### What is in each column

`dtypes` tells you what pandas decided each column is. `object` means text, which for us means a
category. `int64` and `float64` are numbers. The distinction matters because most algorithms only
accept numbers, so every text column has to be turned into numbers before fitting: that is the
one-hot encoding two cells below.

`isna().sum()` counts blanks per column. There is exactly one column with blanks here, and the
reason is in the data's own design: `revenue_2023` is blank for accounts that joined during 2024,
because they did not exist in 2023. A blank that *means* something is different from a blank that
is an accident, and it needs filling deliberately rather than dropping the row.
"""))

cells.append(code(r"""
summary = pd.DataFrame({
    "dtype": accounts.dtypes.astype(str),
    "blanks": accounts.isna().sum(),
    "distinct": accounts.nunique(),
})
summary
"""))

cells.append(md(r"""
### Choosing the columns to learn from

Three groups:

- **`NUMS`**, the numeric columns. Counts, amounts and gaps in days. These go in as they are.
- **`CATS`**, the categorical columns. Segment, city tier, company size and which rep owns the
  account. Each becomes a set of 0/1 columns.
- **Excluded.** `account_id` and `account_name` identify the row rather than describe it. An id can
  correlate with the target by accident of how the data was created, and a model that leans on it
  learns nothing transferable. The two 2025 columns are the targets, so they are never inputs.

`rep_id` is a number in the file but a category in meaning: rep 9 is not "more" than rep 4, it is
the inside sales desk. Leaving it numeric would invite the model to treat it as an ordered scale,
so it goes in `CATS`.
"""))

cells.append(code(r"""
TARGET_CLS = "churned_2025"
TARGET_REG = "revenue_2025"

CATS = ["segment", "city_tier", "company_size", "rep_id"]
NUMS = ["tenure_months", "orders_2024", "units_2024", "revenue_2023", "revenue_2024",
        "avg_discount_pct", "late_payment_days", "complaints_2024", "categories_bought",
        "days_since_last_order", "website_logins_2024", "catalog_downloads_2024"]

print(f"{len(CATS)} categorical + {len(NUMS)} numeric = {len(CATS) + len(NUMS)} input columns")
print("excluded on purpose:", ["account_id", "account_name", TARGET_CLS, TARGET_REG])
"""))

cells.append(md(r"""
### The split: train, validation, test

Three parts, each with a different job, and the rule that makes the whole chapter honest.

- **Train (60%).** The model fits on this.
- **Validation (20%).** You compare algorithms and settings on this. You may look at it many times.
- **Test (20%).** You look at it **once**, at the very end. Every time you make a choice based on a
  score, that score becomes a little optimistic, because you have fitted your own decisions to it.
  Keeping a set you never chose anything on is the only way to get an honest final number.

The arguments:

- `test_size=0.2` holds back a fifth; applying `train_test_split` twice gives 60/20/20.
- `stratify=` keeps the churn rate the same in every part. Without it, random chance could put
  noticeably more churners in one part, and the scores would not be comparable. It matters here
  because only 9.7% of accounts churned, and the rarer the class the more a split can drift.
- `random_state=37` fixes the shuffle so you get these exact rows, and these exact numbers.
"""))

cells.append(code(r"""
from sklearn.model_selection import train_test_split

train_full, test = train_test_split(
    accounts, test_size=0.2, stratify=accounts[TARGET_CLS], random_state=37)
train, valid = train_test_split(
    train_full, test_size=0.25, stratify=train_full[TARGET_CLS], random_state=37)

for name, part in [("train", train), ("valid", valid), ("test", test)]:
    print(f"{name:<6} {len(part):>5,} rows · churn {part[TARGET_CLS].mean():.1%}")
"""))

cells.append(md(r"""
### One preparation pipeline, reused by every algorithm

Every algorithm below needs the same preparation, so it is built once:

- `SimpleImputer(strategy="median")` fills the blanks in `revenue_2023` with the median of the
  column. The median rather than the mean because revenue is skewed: a few very large accounts
  would drag a mean upward and put an implausible value into every blank.
- `StandardScaler` rescales each numeric column to mean 0 and standard deviation 1. Distance-based
  and penalty-based algorithms need this: without it, `units_2024` in the thousands would dominate
  `complaints_2024` in single digits purely because of its units. Trees do not care, but it does
  them no harm.
- `OneHotEncoder` turns each category into one 0/1 column per value. `handle_unknown="ignore"`
  means a category seen only in validation or test produces all zeros rather than an error, which
  is what you want in production when a new city tier appears.
- `ColumnTransformer` applies the numeric steps to `NUMS` and the categorical step to `CATS`, and
  glues the results back into one matrix.

Wrapping preparation and model together in a `Pipeline` matters for a reason beyond tidiness: the
imputer's median and the scaler's mean are *learned* from the training rows. Inside a pipeline they
are learned during `fit` and merely applied during `predict`, so validation rows can never leak
their statistics into the preparation.
"""))

cells.append(code(r"""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def make_prep(scale=True):
    'Preparation for the account columns. scale=False for trees, which do not need it.'
    num_steps = [("fill", SimpleImputer(strategy="median"))]
    if scale:
        num_steps.append(("scale", StandardScaler()))
    return ColumnTransformer([
        ("num", Pipeline(num_steps), NUMS),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATS),
    ])


X_train, y_train = train[NUMS + CATS], train[TARGET_CLS]
X_valid, y_valid = valid[NUMS + CATS], valid[TARGET_CLS]
X_test, y_test = test[NUMS + CATS], test[TARGET_CLS]

prepared = make_prep().fit_transform(X_train)
print(f"{len(NUMS) + len(CATS)} input columns became {prepared.shape[1]} numeric columns")
print("the extra columns are the one-hot 0/1 columns, one per category value")
"""))

cells.append(md(r"""
## Two ways to be wrong

Before any algorithm, the idea you will measure in every section.

- **Underfitting.** The model is too simple for the pattern. It scores badly on the training data
  *and* on new data. A straight line through a curve underfits.
- **Overfitting.** The model is flexible enough to memorise the training rows, noise included. It
  scores very well on training and poorly on new data.

You tell them apart by comparing the two scores. A large gap means overfitting; two low scores
mean underfitting. Section 37.10 gives this the names **variance** and **bias**.

Keep that comparison in mind from here on: every model below is scored on train *and* validation,
and the gap is as informative as the score.
"""))

cells.append(md(r"""
## 37.1 Linear regression

**The idea.** Predict a number as a weighted sum of the inputs: multiply each column by its own
weight, add them up, add a constant. Fitting means choosing the weights that make the total squared
error smallest.

Here the target is `revenue_2025`, a number, so this is regression.

**How to read the scores.**

- **MAE**, mean absolute error, is the average miss in rupees. It is in the units of the thing you
  are predicting, which makes it the number to quote to a colleague.
- **R²** is the share of the variation the model explains, from 1.0 (perfect) down through 0.0 (no
  better than always predicting the mean) and into negatives (worse than the mean).

Both are computed on validation, never on training alone.
"""))

cells.append(code(r"""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

yr_train, yr_valid = train[TARGET_REG], valid[TARGET_REG]

linreg = Pipeline([("prep", make_prep()), ("model", LinearRegression())])
linreg.fit(X_train, yr_train)

for name, X, y in [("train", X_train, yr_train), ("valid", X_valid, yr_valid)]:
    pred = linreg.predict(X)
    print(f"{name:<6} MAE Rs {mean_absolute_error(y, pred):>10,.0f}   R2 {r2_score(y, pred):.3f}")

baseline = np.full(len(yr_valid), yr_train.median())
print(f"\nalways predict the median: MAE Rs {mean_absolute_error(yr_valid, baseline):,.0f}")
print("a model that cannot beat that line is not yet worth having")
"""))

cells.append(md(r"""
### Which columns is it leaning on?

The fitted weights say how much each column moves the prediction, but only after scaling makes them
comparable: a weight on a scaled column is "rupees per standard deviation of this column", so the
sizes can be read against each other.

`get_feature_names_out()` recovers the column names after one-hot encoding, so the weights can be
labelled. Sorting by absolute size puts the strongest influences first, in either direction.
"""))

cells.append(code(r"""
names = linreg.named_steps["prep"].get_feature_names_out()
weights = pd.Series(linreg.named_steps["model"].coef_, index=names)
top = weights.reindex(weights.abs().sort_values(ascending=False).index).head(8)
pd.DataFrame({"weight (Rs per sd)": top.round(0)})
"""))

cells.append(md(r"""
## 37.2 Regularization: ridge and lasso

**The problem.** Plain linear regression chases the training data. With many columns, some
correlated, it can give large opposing weights that cancel out on training rows and behave wildly
on new ones.

**The fix.** Add a penalty on the size of the weights, so the fit has to justify every large one.

- **Ridge** penalises the sum of squared weights. It shrinks weights towards zero without reaching
  it. Good when many columns each matter a little.
- **Lasso** penalises the sum of absolute weights, which drives some to exactly zero. That makes it
  a selector as well as a fitter: the columns left with non-zero weights are the ones it kept.

`alpha` sets the strength. Larger means a heavier penalty and a simpler model. `alpha=0` would be
plain linear regression. Picking it is section 37.11's job; here two fixed values show the effect.
"""))

cells.append(code(r"""
from sklearn.linear_model import Lasso, Ridge

rows = []
for label, model in [("linear", LinearRegression()),
                     ("ridge  alpha=10", Ridge(alpha=10)),
                     ("lasso  alpha=1000", Lasso(alpha=1000, max_iter=5000))]:
    pipe = Pipeline([("prep", make_prep()), ("model", model)]).fit(X_train, yr_train)
    coefs = pipe.named_steps["model"].coef_
    rows.append({
        "model": label,
        "train R2": round(r2_score(yr_train, pipe.predict(X_train)), 3),
        "valid R2": round(r2_score(yr_valid, pipe.predict(X_valid)), 3),
        "valid MAE": round(mean_absolute_error(yr_valid, pipe.predict(X_valid))),
        "weights at zero": int((np.abs(coefs) < 1e-8).sum()),
    })
pd.DataFrame(rows)
"""))

cells.append(md(r"""
## 37.3 Logistic regression

**The idea.** The same weighted sum as linear regression, then squeezed through a curve that maps
any number onto the range 0 to 1, so it can be read as a probability. Fitting chooses weights that
make the observed labels most likely.

The target switches to `churned_2025`, so from here on we are classifying.

**Why accuracy is the wrong score here.** Only 9.7% of accounts churned, so a model that predicts
"nobody churns" is right 90.3% of the time and useless. Three better numbers:

- **ROC AUC**: the chance that a randomly chosen churner is scored above a randomly chosen
  non-churner. 0.5 is a coin flip, 1.0 is perfect. It does not depend on where you set the
  threshold, which makes it the right number for comparing models.
- **Average precision**: the area under the precision-recall curve. It pays attention to the rare
  class specifically, so it moves when a model gets better at the thing you actually care about.
- **Recall at a threshold**: of the accounts that did churn, what share did we flag. This is the
  one the business feels, and it depends entirely on the threshold you choose.

`max_iter=1000` raises the solver's iteration limit; the default sometimes stops before the fit has
settled on data of this width and prints a warning.
"""))

cells.append(code(r"""
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

logreg = Pipeline([("prep", make_prep()),
                   ("model", LogisticRegression(max_iter=1000))]).fit(X_train, y_train)

for name, X, y in [("train", X_train, y_train), ("valid", X_valid, y_valid)]:
    p = logreg.predict_proba(X)[:, 1]
    print(f"{name:<6} AUC {roc_auc_score(y, p):.3f}   avg precision {average_precision_score(y, p):.3f}")

print(f"\nalways predict 'no churn' would be accurate {1 - y_valid.mean():.1%} of the time,")
print("and would catch none of the churners at all")
"""))

cells.append(md(r"""
### The threshold is a business decision, not a model one

`predict_proba` gives a probability. Turning it into an action needs a cut-off, and the cut-off is
a choice about which mistake costs more.

- A **low** threshold flags many accounts: high recall, but the team wastes calls on accounts that
  were never going to leave.
- A **high** threshold flags few: almost every flag is real, but you miss churners.

The table shows what each cut-off would have meant on the validation accounts. Nothing about the
model changes between rows; only the line you draw through its output.
"""))

cells.append(code(r"""
from sklearn.metrics import precision_score, recall_score

p_valid = logreg.predict_proba(X_valid)[:, 1]
rows = []
for t in [0.10, 0.20, 0.30, 0.50]:
    flag = (p_valid >= t).astype(int)
    rows.append({
        "threshold": t,
        "accounts flagged": int(flag.sum()),
        "of them really churned": int(((flag == 1) & (y_valid == 1)).sum()),
        "precision": round(precision_score(y_valid, flag, zero_division=0), 3),
        "recall": round(recall_score(y_valid, flag), 3),
    })
pd.DataFrame(rows)
"""))

cells.append(md(r"""
## 37.4 k-nearest neighbours

**The idea.** No fitting in the usual sense. To predict for an account, find the `k` most similar
accounts in the training set and let them vote.

**Why scaling is not optional here.** "Similar" means close in distance, and distance adds up the
differences across every column. An unscaled `units_2024` in the thousands would swamp
`complaints_2024` in single digits, so the neighbours would be chosen almost entirely by order
volume. The scaler in our pipeline is doing real work for this algorithm.

`n_neighbors` is the `k`. Small k follows the training data closely and is noisy; large k smooths
and can wash out a small class like churners.
"""))

cells.append(code(r"""
from sklearn.neighbors import KNeighborsClassifier

rows = []
for k in [5, 25, 100]:
    pipe = Pipeline([("prep", make_prep()),
                     ("model", KNeighborsClassifier(n_neighbors=k))]).fit(X_train, y_train)
    rows.append({
        "k": k,
        "train AUC": round(roc_auc_score(y_train, pipe.predict_proba(X_train)[:, 1]), 3),
        "valid AUC": round(roc_auc_score(y_valid, pipe.predict_proba(X_valid)[:, 1]), 3),
    })
knn_scores = pd.DataFrame(rows)
knn_scores["gap"] = (knn_scores["train AUC"] - knn_scores["valid AUC"]).round(3)
knn_scores
"""))

cells.append(md(r"""
Read the `gap` column. At `k=5` the training score is far above validation, which is overfitting:
with five neighbours the model can trace every local quirk of the training rows. As `k` grows the
gap narrows, because averaging over more neighbours smooths those quirks away. That is the
bias-variance trade-off from section 37.10, visible in three rows.
"""))

cells.append(md(r"""
## 37.6 Decision trees

**The idea.** Ask a series of yes/no questions about one column at a time, splitting the accounts
into smaller groups, and predict the majority of whatever group a new account lands in. Fitting
means choosing which question to ask at each step, by looking for the split that best separates
churners from the rest.

**Why trees need no scaling.** A tree only ever asks "is this column above or below a value", so
the units do not matter. We pass `scale=False`, which keeps the imputer and drops the scaler.

`max_depth` caps how many questions deep the tree can go, and it is the main control on
overfitting: an unlimited tree will keep splitting until the groups are pure, which means it has
memorised the training set.

Trees have one property nothing else here matches: you can read the whole decision out loud.
"""))

cells.append(code(r"""
from sklearn.tree import DecisionTreeClassifier, export_text

rows = []
for depth in [2, 4, 8, None]:
    pipe = Pipeline([("prep", make_prep(scale=False)),
                     ("model", DecisionTreeClassifier(max_depth=depth, random_state=37))])
    pipe.fit(X_train, y_train)
    rows.append({
        "max_depth": "unlimited" if depth is None else depth,
        "train AUC": round(roc_auc_score(y_train, pipe.predict_proba(X_train)[:, 1]), 3),
        "valid AUC": round(roc_auc_score(y_valid, pipe.predict_proba(X_valid)[:, 1]), 3),
    })
tree_scores = pd.DataFrame(rows)
tree_scores["gap"] = (tree_scores["train AUC"] - tree_scores["valid AUC"]).round(3)
tree_scores
"""))

cells.append(md(r"""
The unlimited tree reaches a near-perfect training score and the worst validation score of the four.
That is overfitting in its clearest form, and it is why depth is capped in practice.

Now read the shallow tree. `export_text` prints the questions in order; each line is one branch,
and the indentation is the depth. `value=` shows how many training accounts of each class reached
that leaf.
"""))

cells.append(code(r"""
small = Pipeline([("prep", make_prep(scale=False)),
                  ("model", DecisionTreeClassifier(max_depth=2, random_state=37))]).fit(X_train, y_train)
feature_names = list(small.named_steps["prep"].get_feature_names_out())
print(export_text(small.named_steps["model"], feature_names=feature_names, decimals=0))
"""))

cells.append(md(r"""
## 37.7 Random forests

**The idea.** One deep tree overfits. Build hundreds of them, each on a random sample of the rows
and allowed to consider only a random subset of the columns at each split, then average their
votes. The individual trees are still overfitted; their errors are made in different directions, so
averaging cancels much of the noise and keeps the signal.

The arguments that matter:

- `n_estimators=300`: how many trees. More is steadily better and steadily slower, with
  diminishing returns; it is not a setting that overfits.
- `min_samples_leaf=5`: a leaf must hold at least five accounts, which stops the trees carving out
  single-account leaves.
- `n_jobs=-1`: use every processor core. Pure speed, no effect on the result.
- `random_state=37`: fixes the randomness, so the forest is reproducible.
"""))

cells.append(code(r"""
from sklearn.ensemble import RandomForestClassifier

forest = Pipeline([("prep", make_prep(scale=False)),
                   ("model", RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
                                                    n_jobs=-1, random_state=37))])
forest.fit(X_train, y_train)

for name, X, y in [("train", X_train, y_train), ("valid", X_valid, y_valid)]:
    print(f"{name:<6} AUC {roc_auc_score(y, forest.predict_proba(X)[:, 1]):.3f}")
"""))

cells.append(md(r"""
### What the forest leaned on

A forest cannot be read like a single tree, but it can report how much each column contributed to
reducing impurity across all the splits in all the trees.

Treat this as a rough ranking, not a measurement. Impurity-based importance is known to favour
columns with many distinct values, so a high-cardinality numeric column can look more important
than it is. Chapter 39 replaces it with permutation importance and SHAP, which are harder to fool.
"""))

cells.append(code(r"""
imp = pd.Series(forest.named_steps["model"].feature_importances_,
                index=forest.named_steps["prep"].get_feature_names_out())
pd.DataFrame({"importance": imp.sort_values(ascending=False).head(10).round(4)})
"""))

cells.append(md(r"""
## 37.8 Gradient boosting

**The idea.** A forest builds its trees independently and averages them. Boosting builds them one
after another, each new tree fitted to the errors the model has made so far, and added in scaled
down by a learning rate. Hundreds of small corrections, each one aimed at what is still wrong.

The chapter works round one by hand on eight accounts; this is the same procedure at full scale.

The settings, and the trade-off between the first two:

- `n_estimators=400`: how many rounds, so how many corrections.
- `learning_rate=0.05`: how much of each correction to take. Smaller is more careful and needs more
  rounds. The pair moves together: halve the rate and you roughly need to double the rounds.
- `max_depth=3`: each tree stays small. Boosting wants weak learners; depth belongs to the
  ensemble, not the individual tree.
- `subsample=0.8` and `colsample_bytree=0.8`: each tree sees 80% of the rows and 80% of the
  columns, which adds randomness and guards against overfitting.
- `eval_metric="auc"`: what XGBoost reports while training.
"""))

cells.append(code(r"""
from xgboost import XGBClassifier

boost = Pipeline([("prep", make_prep(scale=False)),
                  ("model", XGBClassifier(n_estimators=400, learning_rate=0.05, max_depth=3,
                                          subsample=0.8, colsample_bytree=0.8,
                                          eval_metric="auc", random_state=37))])
boost.fit(X_train, y_train)

for name, X, y in [("train", X_train, y_train), ("valid", X_valid, y_valid)]:
    p = boost.predict_proba(X)[:, 1]
    print(f"{name:<6} AUC {roc_auc_score(y, p):.3f}   avg precision {average_precision_score(y, p):.3f}")
"""))

cells.append(md(r"""
**A note on the libraries.** The chapter also uses LightGBM and CatBoost, and Optuna for tuning.
They are not installed in this environment, so this notebook uses XGBoost, which the chapter leads
with, and scikit-learn's own `HistGradientBoostingClassifier` as a second opinion. Install the
others with `python -m pip install lightgbm catboost optuna` if you want to follow those sections
too; the ideas are identical and the arguments are named almost the same.
"""))

cells.append(code(r"""
from sklearn.ensemble import HistGradientBoostingClassifier

hgb = Pipeline([("prep", make_prep(scale=False)),
                ("model", HistGradientBoostingClassifier(max_iter=400, learning_rate=0.05,
                                                         max_depth=3, random_state=37))])
hgb.fit(X_train, y_train)
print(f"scikit-learn HistGradientBoosting · valid AUC "
      f"{roc_auc_score(y_valid, hgb.predict_proba(X_valid)[:, 1]):.3f}")
"""))

cells.append(md(r"""
## 37.10 Bias, variance and learning curves

A **learning curve** fits the same model to more and more training rows and plots both scores. The
shape tells you what to do next, which is the most practical use of the whole idea:

- Two curves that **converge on a low score**: high bias, underfitting. More rows will not help.
  Use a more flexible model, or better columns.
- A **wide and persistent gap**: high variance, overfitting. More rows probably will help, and so
  will constraining the model.

`train_sizes` asks for five points between 10% and 100% of the training rows. `cv=5` fits five
times at each point on different folds, so the line is an average rather than one lucky split.
"""))

cells.append(code(r"""
from sklearn.model_selection import learning_curve

sizes, train_scores, valid_scores = learning_curve(
    Pipeline([("prep", make_prep(scale=False)),
              ("model", DecisionTreeClassifier(max_depth=None, random_state=37))]),
    X_train, y_train, train_sizes=np.linspace(0.1, 1.0, 5), cv=5,
    scoring="roc_auc", n_jobs=-1, random_state=37, shuffle=True)

curve = pd.DataFrame({
    "training rows": sizes,
    "train AUC": train_scores.mean(axis=1).round(3),
    "valid AUC": valid_scores.mean(axis=1).round(3),
})
curve["gap"] = (curve["train AUC"] - curve["valid AUC"]).round(3)
curve
"""))

cells.append(md(r"""
The unlimited tree sits near 1.0 on training at every size while validation stays far below. The gap
barely closes as rows are added, which is the signature of a model that is too flexible rather than
one that is short of data. The fix is the one section 37.6 showed: cap the depth, or average many
trees as sections 37.7 and 37.8 do.
"""))

cells.append(md(r"""
## 37.11 Hyperparameter tuning

Settings like `max_depth` and `learning_rate` are not learned from the data; you choose them. Doing
that by hand on the validation set works, but it is slow and it quietly fits your choices to that
one split.

`GridSearchCV` does it properly: for every combination in the grid it runs cross-validation inside
the training set, and reports the average. Nothing touches validation or test.

- `cv=3`: three folds. More is steadier and slower.
- `scoring="roc_auc"`: optimise ranking quality, not accuracy, for the reason in section 37.3.
- `n_jobs=-1`: use every core.
- The grid below is 2 × 2 × 2 = 8 combinations, each fitted 3 times, so 24 fits.
"""))

cells.append(code(r"""
from sklearn.model_selection import GridSearchCV

grid = {
    "model__n_estimators": [200, 400],
    "model__learning_rate": [0.05, 0.10],
    "model__max_depth": [2, 4],
}
search = GridSearchCV(
    Pipeline([("prep", make_prep(scale=False)),
              ("model", XGBClassifier(subsample=0.8, colsample_bytree=0.8,
                                      eval_metric="auc", random_state=37))]),
    grid, cv=3, scoring="roc_auc", n_jobs=-1)
search.fit(X_train, y_train)

print("best settings:")
for k, v in search.best_params_.items():
    print(f"   {k.replace('model__', '')}: {v}")
print(f"\nbest cross-validated AUC inside training: {search.best_score_:.3f}")
print(f"the same model on validation:              "
      f"{roc_auc_score(y_valid, search.predict_proba(X_valid)[:, 1]):.3f}")
"""))

cells.append(md(r"""
## 37.12 All of them on the same split

The comparison the chapter builds to. Every model has seen the same training rows and is scored on
the same validation rows, so the differences are about the algorithms and nothing else.

Read it with the gap in mind, not just the score: a model that wins on validation while showing a
large train-to-validation gap is winning on a split it may not repeat.
"""))

cells.append(code(r"""
candidates = {
    "logistic regression": logreg,
    "k-NN (k=25)": Pipeline([("prep", make_prep()),
                             ("model", KNeighborsClassifier(n_neighbors=25))]).fit(X_train, y_train),
    "decision tree (depth 4)": Pipeline([("prep", make_prep(scale=False)),
                                         ("model", DecisionTreeClassifier(max_depth=4, random_state=37))
                                         ]).fit(X_train, y_train),
    "random forest": forest,
    "gradient boosting (XGBoost)": boost,
    "boosting, tuned": search.best_estimator_,
}

rows = []
for label, model in candidates.items():
    pt = model.predict_proba(X_train)[:, 1]
    pv = model.predict_proba(X_valid)[:, 1]
    rows.append({
        "model": label,
        "train AUC": round(roc_auc_score(y_train, pt), 3),
        "valid AUC": round(roc_auc_score(y_valid, pv), 3),
        "gap": round(roc_auc_score(y_train, pt) - roc_auc_score(y_valid, pv), 3),
        "valid avg precision": round(average_precision_score(y_valid, pv), 3),
    })
comparison = pd.DataFrame(rows).sort_values("valid AUC", ascending=False).reset_index(drop=True)
comparison
"""))

cells.append(md(r"""
### The test set, once

Pick the winner on validation, then score it on test a single time. This is the number you would
quote, and the only one that has not been influenced by any choice you made.

If the test score is close to validation, your choices generalised. If it is markedly lower, you
tuned to the validation split, and the honest figure is the test one.
"""))

cells.append(code(r"""
best_label = comparison.iloc[0]["model"]
best_model = candidates[best_label]
p_test = best_model.predict_proba(X_test)[:, 1]

print(f"chosen on validation: {best_label}")
print(f"   valid AUC {comparison.iloc[0]['valid AUC']:.3f}")
print(f"   test  AUC {roc_auc_score(y_test, p_test):.3f}")
print(f"   test  avg precision {average_precision_score(y_test, p_test):.3f}")

flag = (p_test >= 0.20).astype(int)
print(f"\nat a 0.20 threshold on the {len(test):,} test accounts:")
print(f"   flagged {flag.sum()}, of which {int(((flag == 1) & (y_test == 1)).sum())} really churned")
print(f"   recall {recall_score(y_test, flag):.1%} of the {int(y_test.sum())} churners")
"""))

cells.append(md(r"""
## Which algorithm when

What the comparison above tends to show, and why, as the chapter's summary puts it:

| Algorithm | Reach for it when | Watch out for |
|---|---|---|
| Linear / logistic regression | You need to explain the model, or you have few rows | Misses curves and interactions unless you build them yourself |
| Ridge / lasso | Many columns, some correlated | `alpha` has to be tuned; lasso's zeros are a choice, not a fact |
| k-NN | Small, low-dimensional data; a quick baseline | Needs scaling; slow at predict time; weak with a rare class |
| Decision tree | You must read the rules out loud | Overfits badly unless depth is capped |
| Random forest | A strong, low-effort default on tabular data | Not readable; impurity importance is misleading |
| Gradient boosting | You want the best tabular accuracy | More settings to tune; will overfit if the rate and rounds are wrong |

**The habit worth keeping.** Start with the simplest model that could work, score it honestly, and
only add complexity when the score says the simple one is not enough. A logistic regression you can
explain and defend often beats a boosted ensemble nobody trusts.

## Your turn

1. Swap the target to `revenue_2025` and compare the regressors instead. Which of the regression
   models wins, and does the ranking match the classifiers?
2. Drop `revenue_2024` and refit the boosting model. How much AUC do you lose? That tells you how
   much of the signal is simply "big accounts stay".
3. Set the threshold from the cost of a mistake rather than a round number: if a retention call
   costs ₹500 and a lost account costs ₹40,000, which threshold minimises the total?
4. Re-run the whole notebook with `random_state=38` everywhere. How much do the scores move? That
   spread is the honest uncertainty on any single number above.
"""))

nb = nbf.v4.new_notebook(cells=cells)
nb.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
nb.metadata.language_info = {"name": "python", "version": "3.12.0"}

print(f"cells: {len(cells)} ({sum(1 for c in cells if c.cell_type=='markdown')} markdown, "
      f"{sum(1 for c in cells if c.cell_type=='code')} code)")
print("executing...")
NotebookClient(nb, timeout=900, kernel_name="python3",
               resources={"metadata": {"path": str(CH)}}).execute()
OUT.write_text(nbf.writes(nb), encoding="utf-8")
print("wrote", OUT)
