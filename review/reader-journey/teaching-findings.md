# Code-teaching audit: findings (instructions §6.5)

*Fable B, 22 September 2026. Standard: `planning/chapter-writing-instructions.md` §6.5, with Chapter 26 (sections 26.2 and 26.3) and Chapter 27 (section 27.5) as the reference pattern. Nothing in this file edits a manuscript; the part chats apply and re-verify.*

**Status:** Chapter 37 delivered as the worked sample. The Summary and every other chapter follow once the shape of the Chapter 37 entry is confirmed.

**How to read a patch.** Each patch is written to drop in as it stands: heading, prose, table, bullets. Where a patch needs a number that only a run can produce, the number is written as `[run]` and the run is listed under WHAT-IFS TO RUN with the data it needs. No output in this file is invented.

**A note on the checker.** `tools/check_code_teaching.py` was run on 22 September 2026 with Python 3.12. It reports 27 of 32 blocks flagged for Chapter 37 (the baseline of 20 September said 28; the difference is one block whose 40-line window now catches a later explanation). Two things it cannot see, and which the per-chapter entry corrects for: it does not recognize a loop over setting values as a measured what-if unless the prose uses the words "if you change it", and it does not see a table whose fourth column is missing. Chapter 37 has five measured what-ifs already (α, C, *k*, depth, n_estimators). What it lacks is the settings tables, the line-level explanation, and the framing that tells the reader those loops are what-ifs.

---

## Summary

*To be written after the full audit. It will hold: the five chapters where this matters most; the settings that recur across the book and deserve one canonical explanation; the patch count and an estimate of hours per part.*

---

## Per chapter

### Chapter 37. Supervised Learning Algorithms

- **Blocks flagged:** 27 of 32 (checker, 22 September). **Needing a patch:** 29 (the checker misses three that §6.5 still requires: the Naive Bayes worked example, the sigmoid block, and the test-set-once block). **Exceptions:** 3.
- **Blocks over 25 lines, which must be split, not bulleted:** 9 (lines 62, 176, 382, 674, 854, 1109, 1180, 1316, 1753). The 76-line block at line 854 is the longest in Part IV.
- **Estimated hours to apply, including the 14 runs, `verify_python.py`, and the PDF rebuild:** 12 to 16.

**What is already right, so it is not patched.** The chapter does hand calculations for the sigmoid, a Naive Bayes posterior, a Gini split, and three rounds of boosting, and each one reconciles to the library's number. It has a "Reading it" after almost every output, five loops over setting values with real outputs, a "predict each result before running it" line in the exercises, and changed-setting exercises (6, 8, 9, 10). The gap is specific: no block has a "How it works" that goes line by line, no function's settings are in a table, and the words `random_state`, `stratify`, `test_size`, `cv`, `n_neighbors`, `alphas`, and `handle_unknown` appear in code and never in prose.

**Settings used in code and never explained in the chapter's prose** (34):

`random_state` · `stratify` · `test_size` · `strategy` · `add_indicator` · `handle_unknown` (named once in Chapter 36, never here) · `alphas` · `cv` · `n_neighbors` · `max_iter` (as an optimizer limit on `LogisticRegression`; explained only as "number of trees" for boosting) · `feature_names` · `show_weights` · `n_jobs` · `verbose` · `random_seed` · `thread_count` · `subsample_freq` · `depth` (CatBoost) · `n_splits` · `shuffle` · `scoring` · `train_sizes` · `axis` · `n_iter` · `l2_regularization` (the argument; "L2 regularization" the idea is named) · `n_trials` · `direction` · `param_name` · `param_range` · `estimators` · `final_estimator` · `drop_first` · `dtype` · `refit` (used by default in both searches and never named)

**Settings named in prose but with no table and no "what happens if you change it":** `drop="first"`, `C`, `l1_ratio`, `max_depth`, `min_samples_leaf`, `criterion`, `n_estimators`, `max_features`, `learning_rate`, `subsample`, `colsample_bytree`, `num_leaves`, `min_child_samples`, `iterations`, `kernel`, `class_weight`, `probability`, `cat_features`, `param_distributions`, `seed`.

**Two things the part chat should know before starting.**

1. Chapter 36 section 36.9 uses `train_test_split` once, at the end, without explaining `test_size` or `stratify`. In Part IV's reading order, Chapter 37 section 37.0 is therefore the first taught use, and the settings table belongs here. If the Part IV review pass later adds a table to Chapter 36, shorten P1's table to a reference to it.
2. Patch P5 proposes adding one optional argument, `nums=NUMS`, to `clf_pipeline`. That is a code change, not a prose change. It is what turns the 46-line block in 37.10 and the 30-line block in exercise 12 into short blocks, because both of them re-type `clf_pipeline`'s recipe with `NUMS + ENG`. Every output should be unchanged, and the whole chapter must be re-run through `verify_python.py` to prove it. If the part chat prefers not to touch the function, P18 and P23 give the fallback.

---

#### PATCHES

##### P1. Section 37.0: split the 41-line block into three steps, add the split's settings table, the predict prompt, and the first what-if

Replace the single block at line 62 and its "Reading it" with the following. The code is identical; it is cut into three blocks with prose between them.

---

**The question:** *"Which accounts will stop ordering next year, and how much will the ones that stay spend?"*

**The plan, in words.** Load the tools this chapter needs. Read the accounts file. Name which columns are categories and which are numbers, because they are prepared differently. Then cut the 5,000 accounts into three sets: one to learn from, one to compare choices on, and one locked away for the end, keeping the churn rate the same in all three.

**Step 1: tools and data.**

```python
import warnings

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import log_loss, mean_absolute_error, r2_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore", category=UserWarning)

accounts = pd.read_csv("../accounts/accounts.csv")
accounts["rep_id"] = accounts["rep_id"].astype(str)
print(accounts.shape)
print(
    f"churned in 2025: {accounts['churned_2025'].sum():,} of {len(accounts):,} "
    f"({accounts['churned_2025'].mean():.1%})"
)
```

```
(5000, 20)
churned in 2025: 484 of 5,000 (9.7%)
```

**How it works:**

- **`import warnings`** and the **`filterwarnings`** line below it silence scikit-learn's advisory messages, which would otherwise appear between the outputs in this chapter. This also hides *convergence* warnings, which matter: section 37.3 turns one back on so you can see what it looks like.
- **`numpy as np`** does the arithmetic (logs, exponentials, means). **`pandas as pd`** holds the tables. Both were introduced in Chapter 17 and Chapter 18.
- **The six `sklearn` imports** are the pieces Chapter 36 section 36.8 assembled into a pipeline: `ColumnTransformer` (different recipes for different columns), `SimpleImputer` (fill blanks), `OneHotEncoder` (categories to 0/1 columns), `StandardScaler` (numbers to a common scale), `Pipeline` (chain them), and `train_test_split` (cut rows into sets). The four **metrics** score a model: `roc_auc_score` and `log_loss` for classification (Chapter 36), `r2_score` and `mean_absolute_error` for regression (section 37.1).
- **`pd.read_csv("../accounts/accounts.csv")`** reads the file from the folder above `companion/ch37/`, which is where the code runs. Change the path if you keep the file elsewhere.
- **`accounts["rep_id"].astype(str)`** turns the rep number into text. `rep_id` is 3, 4, 5, or 9, and a model given it as a number would treat rep 9 as "three times rep 3". As text it becomes a category, and the encoder gives each rep its own column.
- **`accounts.shape`** is (rows, columns). **`.sum()`** of a 0/1 column counts the ones; **`.mean()`** of it is the share, printed as a percentage by the `:.1%` format.

**Step 2: which columns are which.**

```python
CATS = ["segment", "city_tier", "company_size", "rep_id"]
NUMS = [
    "tenure_months",
    "orders_2024",
    "units_2024",
    "revenue_2024",
    "avg_discount_pct",
    "late_payment_days",
    "complaints_2024",
    "categories_bought",
    "days_since_last_order",
    "website_logins_2024",
    "catalog_downloads_2024",
]
```

- **`CATS`** and **`NUMS`** are plain Python lists of column names, in capitals because they do not change. Every pipeline in this chapter is told "encode these, scale those" by handing it these two lists. To use your own data, this is the first place you change: put your category columns in one list and your numeric columns in the other. Notice what is *not* here: `account_id`, `account_name`, `revenue_2023`, and the two 2025 target columns. A model given a target column as a feature scores perfectly and is useless (Chapter 36 section 36.5).

**Step 3: three sets, same churn rate in each.**

*Before you run this, write down what you expect: if 9.7% of all accounts churned, what churn rate should each of the three sets show? Then run it.*

```python
rest, test_acc = train_test_split(
    accounts, test_size=0.2, random_state=37, stratify=accounts["churned_2025"]
)
train_acc, valid_acc = train_test_split(
    rest, test_size=0.25, random_state=37, stratify=rest["churned_2025"]
)
for name, part in [("train", train_acc), ("valid", valid_acc), ("test", test_acc)]:
    print(
        f"{name:<6} {len(part):>5,} accounts   churn {part['churned_2025'].mean():.1%}"
    )
```

```
train  3,000 accounts   churn 9.7%
valid  1,000 accounts   churn 9.7%
test   1,000 accounts   churn 9.7%
```

**How it works:**

- **`train_test_split(accounts, ...)`** shuffles the rows and returns two tables. The first call cuts off the **test set** (1,000 accounts) and leaves `rest` (4,000). The second call cuts `rest` into **training** (3,000) and **validation** (1,000). Two calls, because the function only ever makes two pieces.
- **Why 0.2 and then 0.25:** 20% of 5,000 is 1,000 for the test set. Of the remaining 4,000, 25% is 1,000 for validation. The result is the 60/20/20 split Chapter 36 section 36.3 described.
- **`for name, part in [...]`** loops over three (label, table) pairs and prints a line for each. `{len(part):>5,}` right-aligns the count in five characters with a thousands comma.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `test_size=0.2` | share of the rows to hold back in the second table | 0.2 (20%), then 0.25 of what was left | smaller: fewer rows to score on, so the score is noisier; larger: fewer rows to learn from. A whole number (`test_size=1000`) means that many rows rather than a share |
| `random_state=37` | the seed for the shuffle, so the same rows land in the same sets every time the code runs | 37 (this chapter's number; Chapter 36 used 36) | any other number gives a different but equally fair split, and every score in this chapter moves a little. Leave it out and the split changes on every run, so no result can be reproduced |
| `stratify=accounts["churned_2025"]` | keep the share of churners the same in both pieces | the churn column | leave it out and the churn rates drift apart by chance. See the measurement below. Always stratify on the target for classification; never for regression, where there is no class to balance |
| `shuffle=True` | shuffle before cutting | the default, not written | `shuffle=False` takes the first 80% of rows as is. Only right when the rows are already in a random order, and wrong for time-ordered data, where Chapter 36's time split is the tool |

**A measured what-if: `stratify` and `random_state`.** The same cut, made without stratifying and with a different seed:

```python
for seed, strat in [(37, None), (1, accounts["churned_2025"]), (1, None)]:
    a, b = train_test_split(accounts, test_size=0.2, random_state=seed, stratify=strat)
    print(
        f"seed {seed}  stratify={'yes' if strat is not None else 'no ':<3}  "
        f"rest churn {a['churned_2025'].mean():.2%}   test churn {b['churned_2025'].mean():.2%}"
    )
```

```
[run: W1]
```

[Reading sentence to be written from the real output. The point to make: with `stratify` the two rates match to the second decimal whatever the seed; without it they differ, and by how much is a matter of luck. With 484 churners in 5,000 rows the drift is small; with 50 in 500 it would not be.]

The test set stays locked until section 37.11.

---

##### P2. Section 37.1, first block (line 137): add "How it works" for the regression's first fit

Keep the code and output. Insert the following between the output and the existing "Reading it".

---

**How it works:**

- **`accounts[accounts["churned_2025"] == 0].copy()`** keeps only the stayers. **`.copy()`** makes a separate table, so the new log columns added next do not touch `accounts`, which the classification sections still need whole.
- **The `for col in [...]` loop** adds a log column for each of four columns. `np.log` is the natural log (Chapter 35). The name is built as `"log_" + col`, so `revenue_2024` becomes `log_revenue_2024`. The `.replace("_2025", "_next")` and the `rename` on the next line together give the target the name `log_revenue_2025`; the detour exists only so the loop can treat the target like the other three, and the two lines could be one direct assignment.
- **`train_test_split(stayed, test_size=0.25, random_state=37)`** cuts the 4,516 stayers into 3,387 for fitting and 1,129 for testing. There is no `stratify` because this is regression: there is no class to balance. The settings are the ones in section 37.0's table.
- **`LinearRegression().fit(X, y)`** is the first model fitted in this chapter. `fit` means "learn the weights from these rows". `X` is the features, given as `reg_train[["log_revenue_2024"]]` with double brackets so it is a one-column *table*, which scikit-learn requires, rather than a single column. `y` is the target, a single column.
- **`.intercept_` and `.coef_`** are what `fit` learned. The trailing underscore is scikit-learn's convention for "this exists only after fitting". `coef_` is an array with one entry per feature, so `[0]` picks the only one.
- **`.predict(...)`** applies the learned line to new rows and returns an array of predictions, here for the 1,129 test accounts.
- **`r2_score(actual, predicted)`** takes the true values first and the predictions second. Swapping them gives a different, wrong number without any error.
- **`reg_test.iloc[0]`** is the first test row by position. **`np.exp(pred[0])`** undoes the log, so the prediction reads in rupees.

---

##### P3. Section 37.1 "Many features" (line 176): split the 43-line block into three steps, with the preparation settings table

Replace the block with the following three blocks and their prose. Code unchanged.

---

**The plan, in words.** List the numeric columns for the regression (the log versions replace the raw ones). Write a function that builds the same preparation-plus-model pipeline for any model, so every regression in this section is prepared identically. Write a second function that fits a pipeline, scores it, and prints one line. Then fit ordinary least squares and read its weights.

**Step 1: the numeric columns for regression.**

```python
REG_NUMS = [
    "log_revenue_2024",
    "log_units_2024",
    "log_orders_2024",
    "tenure_months",
    "avg_discount_pct",
    "late_payment_days",
    "complaints_2024",
    "categories_bought",
    "days_since_last_order",
    "website_logins_2024",
    "catalog_downloads_2024",
]
```

- **`REG_NUMS`** is `NUMS` with the three money-and-volume columns swapped for their logs. The categories list `CATS` is reused as it is.

**Step 2: one recipe for every regression.**

```python
def reg_pipeline(model):
    prepare = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), CATS),
            (
                "num",
                Pipeline(
                    [
                        ("fill", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                REG_NUMS,
            ),
        ]
    )
    return Pipeline([("prepare", prepare), ("model", model)])
```

**How it works:**

- **`def reg_pipeline(model):`** takes any scikit-learn model and returns it wrapped in the same preparation. Sections 37.1 and 37.2 call it five times with five different models; the preparation never varies, which is the point.
- **`ColumnTransformer([...])`** applies a different recipe to each group of columns and joins the results side by side (Chapter 36 section 36.8). Each entry is `(name, what to do, which columns)`.
- **`("cat", OneHotEncoder(...), CATS)`** turns each category column into 0/1 columns, one per category value.
- **`("num", Pipeline([...]), REG_NUMS)`** runs two steps on the numeric columns in order: fill blanks, then scale.
- **`Pipeline([("prepare", prepare), ("model", model)])`** chains preparation and model into one object with one `fit` and one `predict`. The step names, `"prepare"` and `"model"`, are how later code reaches inside: `named_steps["model"]` in Step 3, and `model__max_depth` in section 37.11.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `OneHotEncoder(drop="first")` | leave out one category per column, so the others are read against it | `"first"`: Hospitality, Metro, Large, and rep 3 are the dropped baselines | `drop=None` keeps every category. For plain linear regression the columns then always add up to 1 and the weights cannot be pinned down (the **dummy variable trap**); see the measurement below. Regularized models and trees do not care, which is why section 37.3's pipeline leaves it out |
| `OneHotEncoder(handle_unknown="ignore")` | what to do with a category value never seen in training | `"ignore"`: the row gets all zeros for that column | the default, `"error"`, stops the program on the first new value. Right during development, wrong in production, where a new city tier should not crash the report (Chapter 36 section 36.8) |
| `SimpleImputer(strategy="median")` | how to fill a blank number | the column's median, learned from training rows | `"mean"` uses the average, which a few large accounts pull upward; `"most_frequent"` uses the commonest value; `"constant"` with `fill_value=0` fills with a number you choose. Here only `late_payment_days` has blanks (3%), so the choice barely moves the score: see the measurement |
| `StandardScaler()` | put every numeric column on the same scale: subtract its mean, divide by its standard deviation | no settings | remove it and the weights are in mixed units (rupees, days, counts), so they cannot be compared and the penalties in section 37.2 fall unevenly |

**Step 3: fit, score, print.**

```python
def reg_report(name, pipe):
    pipe.fit(reg_train[CATS + REG_NUMS], reg_train["log_revenue_2025"])
    pred = pipe.predict(reg_test[CATS + REG_NUMS])
    mae = mean_absolute_error(reg_test["revenue_2025"], np.exp(pred))
    print(
        f"{name:<18} R² {r2_score(reg_test['log_revenue_2025'], pred):.4f}   "
        f"MAE ₹{mae:,.0f}"
    )
    return pipe


ols = reg_report("linear regression", reg_pipeline(LinearRegression()))
names = ols.named_steps["prepare"].get_feature_names_out()
coefs = pd.Series(ols.named_steps["model"].coef_, index=names)
print(coefs.round(3).sort_values().to_string())
```

[existing output, unchanged]

**How it works:**

- **`reg_report(name, pipe)`** fits the pipeline on the training rows, predicts the test rows, prints one line, and hands the fitted pipeline back so the caller can look inside it. Every model in sections 37.1 and 37.2 goes through this one function, so their lines are comparable.
- **`reg_train[CATS + REG_NUMS]`** selects the feature columns by joining the two lists. The target is a separate column.
- **`mean_absolute_error(reg_test["revenue_2025"], np.exp(pred))`** compares real rupees with predictions converted back from logs by `np.exp`, so the MAE reads in rupees. R² is computed on the log scale, where the model was fitted.
- **`ols.named_steps["prepare"].get_feature_names_out()`** asks the fitted preparation step what it called each output column: `cat__segment_Retail`, `num__late_payment_days`, and so on. The prefix is the `ColumnTransformer` entry's name.
- **`pd.Series(coef_, index=names)`** pairs each weight with its column name; `index=` sets the labels. **`.sort_values()`** orders them from most negative to most positive, and **`.to_string()`** prints all rows rather than pandas's shortened view.

**A measured what-if: `drop="first"` and `strategy`.**

```python
from sklearn.base import clone

variants = {
    "drop=None": reg_pipeline(LinearRegression()).set_params(prepare__cat__drop=None),
    "strategy=mean": reg_pipeline(LinearRegression()).set_params(
        prepare__num__fill__strategy="mean"
    ),
}
for label, pipe in variants.items():
    fitted = reg_report(label, pipe)
    c = pd.Series(fitted.named_steps["model"].coef_, index=fitted.named_steps["prepare"].get_feature_names_out())
    print("   segment weights:", c.filter(like="segment").round(3).to_dict())
```

```
[run: W2]
```

[Reading sentence from the real output. Expected shape, to be confirmed by the run: with `drop=None` the R² and MAE are the same to four decimals and the three `segment` weights are different numbers that tell the same story only when read relative to each other; with `strategy="mean"` the score moves in the fourth decimal or not at all, because only 3% of one column is blank.]

- **`.set_params(prepare__cat__drop=None)`** changes one setting inside a built pipeline without rebuilding it. The double underscore walks down the names: the step `prepare`, its entry `cat`, its setting `drop`. Section 37.11 uses the same naming to tune a model inside a pipeline.

---

##### P4. Section 37.2 (line 302): settings table for the `...CV` models, "How it works", and a heading over the existing α loop

Insert after the existing "Reading it" of the `RidgeCV`/`LassoCV`/`ElasticNetCV` block:

---

**How it works:**

- **`RidgeCV(alphas=np.logspace(-3, 3, 25))`** fits ridge once per candidate α and keeps the best by cross-validation. `np.logspace(-3, 3, 25)` makes 25 values evenly spaced on a log scale from 10⁻³ to 10³, so 0.001 to 0.01 gets as many candidates as 100 to 1,000. For a setting that spans orders of magnitude, that is the right spacing; `np.linspace` would waste almost every candidate above 100.
- **`LassoCV(cv=5, random_state=37)`** builds its own grid of 100 α values and picks the best by 5-fold cross-validation.
- **`ElasticNetCV(l1_ratio=[0.2, 0.5, 0.8], cv=5, random_state=37)`** does the same over a grid of α for each of the three mixes.
- **`.alpha_` and `.l1_ratio_`** are what the cross-validation chose, read from the fitted model inside the pipeline through `named_steps["model"]`.
- **`lasso_coefs[lasso_coefs == 0].index`** lists the features whose weight lasso pushed to exactly zero, which is the feature-selection result.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `alphas` (RidgeCV) | the candidate penalty strengths to try | 25 values from 0.001 to 1,000 | a narrower range can miss the best value; the default is only three values (0.1, 1, 10). Check that the chosen α is not at either end of the range, or the range was too small |
| `cv=5` | how many folds to judge each α on | 5 | more folds: a steadier choice, more time; `cv=None` uses an efficient leave-one-out shortcut for ridge only |
| `l1_ratio` (ElasticNetCV) | the mix: 1 is pure lasso, 0 is pure ridge | three candidates, 0.2, 0.5, 0.8 | a single number fixes the mix; a list lets cross-validation choose it. Here it chose 0.8, close to lasso |
| `random_state=37` | seed for the coordinate-descent update order | 37 | with the default `selection="cyclic"` it has no effect at all. It is written from habit, and leaving it out changes nothing here. Its only use is with `selection="random"`, which updates weights in a random order and can be faster on wide data |

Then change the line "Increase α by hand to see the trade-off:" to a heading and two bullets:

**A measured what-if: α.** The `...CV` models chose α; here the plain `Lasso` is given four values by hand to see what the choice trades off.

[existing loop block and output, unchanged]

- **`Lasso(alpha=alpha)`** is the fixed-α model; `LassoCV` above chose α for itself. Using the plain model is how you see the whole path, not only the winner.
- **`(coef_ != 0).sum()`** counts the surviving features: a True/False array summed as 1/0.

---

##### P5. Section 37.3 (line 382): split the 31-line block into three steps, add the `LogisticRegression` settings table, show the convergence error, and (recommended) give `clf_pipeline` a `nums` argument

Replace the block with the following. The only code change is the optional `nums=NUMS` argument, which is used by P18 and P23; everything else is the same code cut into steps.

---

**The plan, in words.** Build the preparation recipe for classification, which differs from the regression one in two ways: blanks get a flag column as well as a fill, and one-hot encoding keeps every category. Name the training and validation features and targets. Write a function that fits a pipeline and prints its AUC and log loss on the validation accounts. Then fit logistic regression and turn its weights into odds ratios.

**Step 1: the classification recipe.**

```python
from sklearn.linear_model import LogisticRegression


def clf_pipeline(model, scale=True, nums=NUMS):
    num_steps = [("fill", SimpleImputer(strategy="median", add_indicator=True))]
    if scale:
        num_steps.append(("scale", StandardScaler()))
    prepare = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATS),
            ("num", Pipeline(num_steps), nums),
        ]
    )
    return Pipeline([("prepare", prepare), ("model", model)])
```

**How it works:**

- **`clf_pipeline(model, scale=True, nums=NUMS)`** is section 37.1's `reg_pipeline` with two switches. `scale` turns the scaler off for models that do not need it (trees, forests, boosting: sections 37.6 to 37.8). `nums` lets section 37.10 pass a longer list of numeric columns without re-typing the recipe. Both have defaults, so `clf_pipeline(LogisticRegression())` is all most calls need.
- **`num_steps = [("fill", ...)]`** starts the numeric recipe as a list with one step, and **`num_steps.append(("scale", ...))`** adds the scaler only if asked. Building the list in two moves is how a function offers a choice.
- **`SimpleImputer(strategy="median", add_indicator=True)`** fills blanks with the median *and* adds a 0/1 column saying "this was blank". Chapter 36 section 36.7 explained why: a blank can itself be a signal.
- **`OneHotEncoder(handle_unknown="ignore")`** with no `drop`: every category gets a column. Logistic regression is regularized by default (see `C` below), so the dummy variable trap of section 37.1 does not arise.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `add_indicator=True` | add a 0/1 column marking which values were blank | on | off: the fill is silent, and the model cannot tell a real 25 days late from a blank filled with 25. Here only `late_payment_days` has blanks, so one indicator column is added, which is why the odds table has 25 columns and not 24 |
| `scale` (this function's own switch) | whether to standardize the numbers | `True` for logistic regression, k-NN, SVM; `False` for trees | section 37.4 measures what happens to k-NN without it: AUC 0.765 to 0.633 |

**Step 2: features, targets, and the scoring function.**

```python
X_tr, y_tr = train_acc[CATS + NUMS], train_acc["churned_2025"]
X_va, y_va = valid_acc[CATS + NUMS], valid_acc["churned_2025"]
results = {}


def clf_report(name, pipe):
    pipe.fit(X_tr, y_tr)
    p = pipe.predict_proba(X_va)[:, 1]
    results[name] = roc_auc_score(y_va, p)
    print(f"{name:<30} AUC {results[name]:.3f}   log loss {log_loss(y_va, p):.4f}")
    return pipe
```

**How it works:**

- **`X_tr, y_tr = ...`** names the training features and target once, so every model in the chapter is fitted on exactly the same rows. `X` for features and `y` for target is the convention across scikit-learn and this book.
- **`results = {}`** is an empty dictionary that `clf_report` fills with each model's AUC, keyed by name, so later sections can compare without re-running.
- **`pipe.predict_proba(X_va)`** returns two columns per row: the probability of class 0 (stayed) and class 1 (churned). **`[:, 1]`** keeps the second, which is the churn probability. `predict` without `proba` would return 0 or 1 by cutting at 0.5, which throws away the ranking that AUC measures.
- **`roc_auc_score(y_va, p)`** and **`log_loss(y_va, p)`** take the true labels first, then the probabilities, as in Chapter 36.

**Step 3: logistic regression, and its weights as odds ratios.**

```python
logit = clf_report(
    "logistic regression", clf_pipeline(LogisticRegression(max_iter=2000))
)
coef = pd.Series(
    logit.named_steps["model"].coef_[0],
    index=logit.named_steps["prepare"].get_feature_names_out(),
)
odds = np.exp(coef).round(2).sort_values()
print("odds ratios (per 1 standard deviation for numbers):")
print(pd.concat([odds.head(3), odds.tail(4)]).to_string())
```

[existing output, unchanged]

- **`LogisticRegression(max_iter=2000)`** is the model, with its settings in the table below.
- **`coef_[0]`**: for a two-class model, `coef_` has one row, so `[0]` takes it. (A model with five classes would have five rows.)
- **`np.exp(coef)`** turns each weight into an odds ratio, as the existing "How it works" says. **`pd.concat([odds.head(3), odds.tail(4)])`** shows the three smallest and four largest without the middle.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `max_iter=2000` | how many rounds the optimizer may take to settle on the weights | 2,000 | the default is 100. Too few and the model stops before it has finished, and warns; see the error below. More rounds cost nothing once it has converged, because it stops early |
| `C=1.0` | regularization strength, backwards: smaller C is a stronger penalty | 1.0, the default | measured in "The sigmoid by hand, and the setting C" below: 0.01 to 10 moves AUC by 0.003 here |
| `penalty="l2"` | which penalty: ridge-style (`"l2"`), lasso-style (`"l1"`), or none | `"l2"`, the default | `"l1"` zeroes some weights, as lasso did in section 37.2, and needs `solver="liblinear"` or `"saga"`; `None` is plain maximum likelihood, and needs `drop="first"` in the encoder to avoid the dummy variable trap |
| `class_weight=None` | whether rare classes count for more in the loss | `None`: every account counts once | `"balanced"` makes each churner count about nine times as much. Section 37.9 shows what that does to an SVM; Chapter 39 covers it for every model |
| `solver="lbfgs"` | the optimization method | the default | others exist for large or sparse data; the answer is the same to several decimals when they all converge |

**Show the error: too few iterations.** Section 37.0 silenced warnings. Turn this one back on and give the optimizer almost no time:

```python
from sklearn.exceptions import ConvergenceWarning

warnings.simplefilter("always", ConvergenceWarning)
clf_report("logistic, max_iter=10", clf_pipeline(LogisticRegression(max_iter=10)))
warnings.simplefilter("ignore", ConvergenceWarning)
```

```
[run: W4]
```

[Reading sentence from the real output: what the warning says, and whether the AUC is worse. If `max_iter=10` converges without a warning on these scaled features, try `max_iter=3`; if that also converges, drop this demonstration and say so in the chapter report.]

Then change "The sigmoid by hand, and the setting C" so that its C loop is introduced as **A measured what-if: `C`.** (the existing text after the output already reads the result correctly).

---

##### P6. Section 37.3, the sigmoid block (line 452): two bullets

Insert after "The hand calculation matches `predict_proba` exactly. ✓":

- **`X_va.iloc[[0]]`** with double brackets is the first validation row as a one-row *table*, which the pipeline needs; `X_va.iloc[0]` would be a single column of values and the pipeline would refuse it.
- **`logit.decision_function(one)`** returns *z*, the weighted sum before the sigmoid, for each row given. `predict_proba` is the sigmoid of that number, which is what the printed check confirms.

---

##### P7. Section 37.4 (line 486): settings table for k-NN, bullets, and the *k* loop named as a what-if

Replace "That makes two things critical..." through to the block with:

That makes two things critical: **the choice of *k*** and **scaling**. Both are measured below, so this loop is the section's what-if.

[existing block and output, unchanged]

**How it works:**

- **`KNeighborsClassifier(n_neighbors=k)`** stores the training rows at `fit` and, at `predict_proba`, finds the `k` closest training accounts to each validation account and returns the share of them that churned.
- **`clf_pipeline(..., scale=False)`** on the last line is the same model with the scaler switched off, which is the "NOT scaled" line.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `n_neighbors=k` | how many nearest training rows vote | 5, 25, 75 | measured above: 5 gives coarse probabilities and a log loss of 1.59; 75 is best here. Beyond a point, more neighbors blur the local pattern into the base rate. The default is 5, which is rarely right for thousands of rows |
| `weights="uniform"` | whether every neighbor's vote counts the same | `"uniform"`, the default | `"distance"` lets closer neighbors count for more. Exercise 6 measures it: AUC 0.775 to 0.778 at *k* = 75 |
| `metric="minkowski"` with `p=2` | how distance is measured | Euclidean, the default | `p=1` is Manhattan distance (sum of absolute differences), which is less dominated by one very different feature |
| the scaler (`scale=`) | whether distances are measured on comparable units | on | measured above: off, AUC drops from 0.765 to 0.633, because revenue in rupees swamps every other column |

---

##### P8. Section 37.5, the worked-example block (line 528): "How it works"

Insert between the output and "For an account that is a late-paying small retailer...":

**How it works:**

- **`late_small_retail`** is three True/False conditions joined with `&`. Each condition sits in parentheses because `&` binds tighter than `>` or `==` in Python; without them the line is an error (Chapter 18 section 18.3).
- **`recent = train_acc["days_since_last_order"] <= 90`** is a fourth condition, and **`~recent`** is its opposite: `~` means "not" for a True/False column.
- **`.rename("late small retail")`** gives each condition a label, which `pd.crosstab` uses as the row and column headings.
- **`pd.crosstab([rows, rows], columns)`** counts how many accounts fall in each combination: two conditions down the side, the churn flag across the top. It is the pivot table of Chapter 10 in one line.
- **`.value_counts().to_dict()`** counts stayers and churners, as a plain dictionary.
- **`flag[train_acc["churned_2025"] == 1].mean()`** is a conditional probability computed directly: keep only the churners, then take the share of them for which the flag is True. The `.mean()` of a True/False column is the share of Trues.

---

##### P9. Section 37.5, the `GaussianNB` block (line 579): two bullets on the conversion line

Add to the existing "How it works":

- **`lambda X: X.toarray() if hasattr(X, "toarray") else X`** is a one-line function with no name (Chapter 18 introduced `lambda`). It converts `X` to a dense array if `X` has a `toarray` method, which sparse matrices do, and passes anything else through unchanged. `hasattr` asks "does this object have a method of that name?"
- **`nb.steps.insert(1, ("dense", to_dense))`** puts the new step at position 1, between `"prepare"` (position 0) and `"model"`. A pipeline's `steps` is an ordinary list.

---

##### P10. Section 37.6, the `gini`/`entropy` block (line 633): "How it works"

Insert after the output and before the parenthetical about rounding:

**How it works:**

- **`def gini(y):`** and **`def entropy(y):`** are the two formulas above as functions. Each takes a column of 0/1 labels, computes `p = np.mean(y)`, the churn rate, and returns the impurity.
- **`0.0 if p in (0, 1) else ...`** guards `entropy`: log₂ of 0 is undefined, so a pure group is returned as 0 directly. `gini` needs no guard because it has no log.
- **`rule`** is a True/False column, one per candidate question. **`y_all[rule]`** is the labels of accounts that answer yes, **`y_all[~rule]`** those that answer no.
- **`w_l` and `w_r`** are the two groups' shares of the rows, which are the weights in the weighted impurity after the split.
- **`w_l * gini(left) + w_r * gini(right)`** is the weighted Gini after the split, the same arithmetic as the hand calculation above it. The `:.1%` and `:.4f` formats print a share as a percentage and a number to four decimals.

---

##### P11. Section 37.6 "Depth, and overfitting" (line 674): split the 28-line block into two, settings table for the tree, and one more what-if

Replace the block with:

---

**Step 1: the same tree at five depths.** This loop is the section's what-if for `max_depth`.

```python
from sklearn.tree import DecisionTreeClassifier, export_text

for depth in [2, 4, 6, 10, None]:
    tree = clf_pipeline(
        DecisionTreeClassifier(max_depth=depth, random_state=37), scale=False
    ).fit(X_tr, y_tr)
    tr_auc = roc_auc_score(y_tr, tree.predict_proba(X_tr)[:, 1])
    va_auc = roc_auc_score(y_va, tree.predict_proba(X_va)[:, 1])
    print(
        f"max_depth {str(depth):<5} train AUC {tr_auc:.3f}   valid AUC {va_auc:.3f}   "
        f"leaves {tree.named_steps['model'].get_n_leaves()}"
    )
```

```
max_depth 2     train AUC 0.759   valid AUC 0.708   leaves 4
max_depth 4     train AUC 0.829   valid AUC 0.748   leaves 16
max_depth 6     train AUC 0.886   valid AUC 0.733   leaves 48
max_depth 10    train AUC 0.969   valid AUC 0.609   leaves 161
max_depth None  train AUC 1.000   valid AUC 0.557   leaves 277
```

**How it works:**

- **`DecisionTreeClassifier(max_depth=depth, random_state=37)`** grows a tree no deeper than `depth` questions. `None` means no limit.
- **`scale=False`**: a tree compares each feature with a threshold, so the units do not matter and scaling is switched off.
- **This loop scores the training rows as well as the validation rows**, which no earlier block did. The gap between the two AUCs is the overfitting signal that section 37.10 names variance.
- **`get_n_leaves()`** counts the final groups. **`str(depth)`** is needed because `None` cannot be formatted with `:<5` directly.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `max_depth` | the most questions any account is asked before reaching a leaf | 2, 4, 6, 10, none | measured above: validation AUC peaks at a shallow depth and collapses to 0.557 with no limit, while training AUC climbs to 1.000 |
| `min_samples_leaf` | the fewest accounts a leaf may hold | 1 (the default) in the loop; 20 in Step 2 | larger: the tree cannot carve out tiny groups, so it overfits less. Measured below |
| `criterion` | how purity is scored | `"gini"`, the default | `"entropy"` uses information gain (Chapter 35). The split-by-hand above shows both rank the candidates the same way, and they rarely disagree |
| `random_state=37` | seed for tie-breaks between equally good splits and for the order features are tried | 37 | a different seed can change which of two equally good splits is chosen, and everything below that split. That is the instability the "Reading it" describes; the seed makes the instability repeatable |

**Step 2: read the depth-2 tree, then fit the depth-4 model the chapter keeps.**

```python
small_tree = clf_pipeline(
    DecisionTreeClassifier(max_depth=2, random_state=37), scale=False
).fit(X_tr, y_tr)
print(
    export_text(
        small_tree.named_steps["model"],
        feature_names=list(small_tree.named_steps["prepare"].get_feature_names_out()),
        show_weights=True,
    )
)
clf_report(
    "decision tree, depth 4",
    clf_pipeline(
        DecisionTreeClassifier(max_depth=4, min_samples_leaf=20, random_state=37),
        scale=False,
    ),
)
```

[existing tree printout and depth-4 line, unchanged]

- **`export_text(model, feature_names=..., show_weights=True)`** prints the tree as indented rules. `feature_names` supplies the column names the preparation step produced, so the rules say `days_since_last_order` rather than `feature_12`; it must be a plain list, hence `list(...)`. `show_weights=True` prints, at each leaf, how many training accounts of each class landed there, `[stayed, churned]`, which is how you read "39 out of 52".
- **`min_samples_leaf=20`** in the depth-4 model is the second brake on overfitting: no leaf may hold fewer than 20 accounts.

**A measured what-if: `min_samples_leaf`.**

```python
for leaf in [1, 20, 100]:
    clf_report(
        f"tree, depth 4, min_samples_leaf={leaf}",
        clf_pipeline(
            DecisionTreeClassifier(max_depth=4, min_samples_leaf=leaf, random_state=37),
            scale=False,
        ),
    )
```

```
[run: W6]
```

[Reading sentence from the real output.]

---

##### P12. Section 37.7 (line 754): settings table for the forest, bullets, and the seed what-if

Insert after the existing "Reading it" and "Feature importance" paragraphs, replacing the "Key settings" paragraph:

**How it works:**

- **`RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=37)`** grows 300 trees, each on its own bootstrap sample and its own random feature subsets, and averages their churn probabilities.
- **`feature_importances_`** is one number per input column, adding up to 1, read from the fitted model through `named_steps["model"]`.
- **`pd.Series(..., index=names)`** labels each importance with its column name, **`.sort_values(ascending=False)`** puts the largest first (the default, `ascending=True`, would put the smallest first), and **`.head(6)`** keeps six.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `n_estimators=300` | how many trees | 300 | exercise 8 measures 10, 50, 300, and 1,000: AUC 0.737, 0.774, 0.785, 0.790. More trees never overfit; they cost time and memory, and the gain flattens |
| `min_samples_leaf=5` | the fewest accounts a leaf may hold, in every tree | 5 | the default is 1, so each tree grows until its leaves are pure. Larger values make each tree smoother and the forest a little less flexible |
| `max_features="sqrt"` | how many features each split may consider | the default: the square root of the number of columns, 5 of 25 | `None` lets every split see every feature, which makes the trees more alike and the averaging less useful. This setting is what "random" in the name refers to |
| `max_depth=None` | depth limit per tree | none | a forest usually limits its trees by leaf size rather than depth |
| `random_state=37` | seed for the bootstrap samples and the feature subsets | 37 | measured below |
| `n_jobs=None` | how many processor cores to use | one core | `n_jobs=-1` uses all of them; each tree is independent, so 300 trees on eight cores take about an eighth of the time. Results do not change |

**A measured what-if: the seed.** Everything in a forest is random except the data, so how much does the seed alone move the score?

```python
for seed in [1, 2, 3]:
    clf_report(
        f"random forest, random_state={seed}",
        clf_pipeline(
            RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=seed),
            scale=False,
        ),
    )
```

```
[run: W14]
```

[Reading sentence from the real output. The point: the spread across seeds is the smallest difference worth talking about. Section 37.8's "differences of 0.01 are within noise" then has a number behind it.]

---

##### P13. Section 37.8 "Three rounds by hand" (line 807): "How it works" and the learning-rate what-if

Insert after the existing "Reading it":

**How it works:**

- **`train_acc.head(8)`** takes the first eight training accounts. **`to_numpy()`** turns the one-column table into a plain array, which the tree expects; **`.astype(float)`** turns the 0/1 labels into 0.0/1.0 so subtraction gives decimals.
- **`np.full(len(y_toy), y_toy.mean())`** makes the round-0 prediction: an array of eight copies of the average.
- **`residual = y_toy - pred`** is what is still wrong for each account after the rounds so far.
- **`DecisionTreeRegressor(max_depth=1, random_state=37)`** is a **stump**: one question, two leaves. It is fitted to the *residuals*, not to the targets, which is the whole idea of boosting.
- **`pred = pred + 0.5 * stump.predict(x_toy)`** adds half of the stump's correction. The `0.5` is the **learning rate**, written as a plain number here and as `learning_rate=` in every library.
- **`stump.tree_.threshold[0]`** reads the question the stump chose: the first (and only) split's cut-off in days.

**A measured what-if: the learning rate.** Same eight accounts, three rounds, three step sizes:

```python
for rate in [0.1, 0.5, 1.0]:
    pred = np.full(len(y_toy), y_toy.mean())
    for r in range(1, 4):
        stump = DecisionTreeRegressor(max_depth=1, random_state=37).fit(x_toy, y_toy - pred)
        pred = pred + rate * stump.predict(x_toy)
    print(f"learning rate {rate}: squared error after 3 rounds {np.mean((y_toy - pred) ** 2):.4f}   churner's prediction {pred[2]:.3f}")
```

```
[run: W7]
```

[Reading sentence from the real output. The point: a bigger step reaches a lower training error sooner, which on eight rows is memorizing faster, not learning better; exercise 9 continues to 20 rounds.]

---

##### P14. Section 37.8 "The libraries" (line 854): split the 76-line block into four steps, one shared settings table, one name-translation table, a predict prompt, and the learning-rate what-if

Replace the prose paragraph beginning "The settings that matter most are shared..." and the 76-line block with the following. Code unchanged apart from being cut.

---

**The plan, in words.** Import the three libraries and print their versions, because their settings change between versions. Fit scikit-learn's own boosting model twice, once with defaults and once with chosen settings. Fit XGBoost and LightGBM through the same pipeline. Fit CatBoost outside the pipeline, because it prepares categories itself. Score all five on the validation accounts.

**The settings, and what each library calls them.** Five settings do most of the work in every gradient-boosting library:

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| number of trees | how many rounds of "fit a tree to the errors" | 300 (500 for CatBoost) | too few: underfits; too many at a high learning rate: overfits. The pair below is what matters, not either alone. Measured below |
| `learning_rate` | how much of each tree's correction is added | 0.05 | smaller: needs more trees and usually generalizes better; larger: fits fast and overfits fast. The library defaults (0.1 for scikit-learn, 0.3 for XGBoost) are on the fast side. Measured below |
| tree size | how big each tree may grow: depth, or number of leaves | depth 3, or 8 leaves | deeper trees see more interactions and overfit more. 2 to 6 covers almost every business table |
| minimum rows per leaf | the fewest accounts a leaf may hold | 40 | larger: smoother, less able to fit tiny groups. With 290 churners in training, 40 is a sensible floor |
| row and column sampling | the share of rows, and of features, each tree sees | 0.8 and 0.8 | below 1.0 adds the random forest's trick to boosting: the trees differ more, and it trains faster. 1.0 turns it off |
| L2 regularization | penalty on leaf values, as ridge penalized weights | 0 (the default) | larger: leaf values shrink toward zero; section 37.11's search finds values around 3 help here |

| Setting | scikit-learn `HistGradientBoostingClassifier` | XGBoost | LightGBM | CatBoost |
|---|---|---|---|---|
| number of trees | `max_iter` | `n_estimators` | `n_estimators` | `iterations` |
| learning rate | `learning_rate` | `learning_rate` | `learning_rate` | `learning_rate` |
| tree size | `max_depth` | `max_depth` | `num_leaves` | `depth` |
| minimum rows per leaf | `min_samples_leaf` | `min_child_weight` | `min_child_samples` | `min_data_in_leaf` |
| row sampling | not available | `subsample` | `subsample`, needs `subsample_freq=1` | `subsample` |
| column sampling | `max_features` (1.4+) | `colsample_bytree` | `colsample_bytree` | `rsm` |
| L2 regularization | `l2_regularization` | `reg_lambda` | `reg_lambda` | `l2_leaf_reg` |
| seed | `random_state` | `random_state` | `random_state` | `random_seed` |
| quiet | (silent) | `verbosity=0` | `verbose=-1` | `verbose=0` |
| cores | (all) | `n_jobs` | `n_jobs` | `thread_count` |

**Step 1: the libraries and their versions.**

```python
import catboost
import lightgbm
import xgboost
from sklearn.ensemble import HistGradientBoostingClassifier

print(
    "versions: xgboost",
    xgboost.__version__,
    "| lightgbm",
    lightgbm.__version__,
    "| catboost",
    catboost.__version__,
)
```

```
versions: xgboost 3.4.1 | lightgbm 4.7.0 | catboost 1.2.10
```

- **`__version__`** is the version string every well-behaved library exposes. It is printed because parameter names in these three libraries have changed between versions, and a reader on a newer version needs to know which one produced these outputs.

**Step 2: scikit-learn's boosting, default and chosen.**

*Before you run this, write down which of the two you expect to score higher on validation, and why. Then run it.*

```python
clf_report(
    "HistGradientBoosting default",
    clf_pipeline(HistGradientBoostingClassifier(random_state=37), scale=False),
)
clf_report(
    "HistGradientBoosting tuned",
    clf_pipeline(
        HistGradientBoostingClassifier(
            learning_rate=0.05,
            max_depth=3,
            min_samples_leaf=40,
            max_iter=300,
            random_state=37,
        ),
        scale=False,
    ),
)
```

```
HistGradientBoosting default   AUC 0.780   log loss 0.3151
HistGradientBoosting tuned     AUC 0.788   log loss 0.2731
```

- **The default** is `learning_rate=0.1`, `max_iter=100`, no depth limit, `min_samples_leaf=20`, `l2_regularization=0`. **The "tuned" version** halves the learning rate, triples the rounds, caps depth at 3, and doubles the leaf minimum. The log loss improves more than the AUC, which says the chosen settings mostly made the probabilities less overconfident.
- **`early_stopping`** is `"auto"`, which is *off* below 10,000 rows, so all 300 rounds run. The project's stretch goal turns it on.

**Step 3: XGBoost and LightGBM, in the same pipeline.**

```python
clf_report(
    "XGBoost",
    clf_pipeline(
        xgboost.XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=3,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=37,
            n_jobs=1,
        ),
        scale=False,
    ),
)
clf_report(
    "LightGBM",
    clf_pipeline(
        lightgbm.LGBMClassifier(
            n_estimators=300,
            learning_rate=0.05,
            num_leaves=8,
            min_child_samples=40,
            subsample=0.8,
            subsample_freq=1,
            colsample_bytree=0.8,
            random_state=37,
            verbose=-1,
        ),
        scale=False,
    ),
)
```

```
XGBoost                        AUC 0.793   log loss 0.2700
LightGBM                       AUC 0.780   log loss 0.2794
```

- **Both drop into `clf_pipeline`** because they follow scikit-learn's `fit` and `predict_proba` interface, as the existing "How it works" says.
- **`num_leaves=8`** is LightGBM's tree-size setting; it grows trees leaf by leaf rather than level by level, so it counts leaves, not depth. A depth-3 tree has at most 8 leaves, so this matches the others.
- **`subsample_freq=1`**: LightGBM ignores `subsample` unless told how often to resample. `1` means every tree. Leave it out and `subsample=0.8` silently does nothing, which is the kind of setting that looks applied and is not.
- **`verbose=-1`** stops LightGBM printing a line per round. **`n_jobs=1`** in XGBoost keeps it on one core so the timings in the text are comparable.

**Step 4: CatBoost, outside the pipeline.**

```python
cat_model = catboost.CatBoostClassifier(
    iterations=500,
    learning_rate=0.05,
    depth=4,
    random_seed=37,
    verbose=0,
    thread_count=1,
)
cat_model.fit(X_tr, y_tr, cat_features=CATS)
p_cat = cat_model.predict_proba(X_va)[:, 1]
results["CatBoost"] = roc_auc_score(y_va, p_cat)
print(
    f"{'CatBoost (native categories)':<30} AUC {results['CatBoost']:.3f}"
    f"   log loss {log_loss(y_va, p_cat):.4f}"
)
```

```
CatBoost (native categories)   AUC 0.796   log loss 0.2710
```

- **`iterations`, `depth`, `random_seed`, `thread_count`** are CatBoost's names for trees, tree size, seed, and cores (see the translation table). **`verbose=0`** silences it.
- **`cat_model.fit(X_tr, y_tr, cat_features=CATS)`** is given the *raw* columns, blanks and text included, and told which are categories. It encodes them itself, as the existing "How it works" explains, and it fills numeric blanks on its own, which is why there is no imputer.
- **The last four lines** do by hand what `clf_report` does, because `clf_report` would have wrapped the model in the pipeline. `results["CatBoost"] = ...` stores its AUC beside the others.

**A measured what-if: learning rate and number of trees, together.** The two settings trade off, so change them together:

```python
for rate, rounds in [(0.3, 100), (0.05, 100), (0.05, 300), (0.05, 1000), (0.01, 1000)]:
    clf_report(
        f"HGB, learning_rate={rate}, max_iter={rounds}",
        clf_pipeline(
            HistGradientBoostingClassifier(
                learning_rate=rate, max_iter=rounds, max_depth=3,
                min_samples_leaf=40, random_state=37,
            ),
            scale=False,
        ),
    )
```

```
[run: W8]
```

[Reading sentences from the real output. The points to make, if the numbers support them: a small rate with too few rounds underfits; a small rate with many rounds is close to the chosen setting; a large rate with many rounds overfits, seen in the log loss before the AUC.]

Keep the existing "How it works" (XGBoost and LightGBM follow the interface; CatBoost encodes itself) and "Reading it" paragraphs after Step 4.

---

##### P15. Section 37.9 (line 960): settings table for `SVC`, bullets, and a what-if on `C`

Insert after the existing "Reading it" and before the "How it works" about `probability=True`:

**How it works:**

- **`SVC(kernel="linear")`** draws a straight boundary; **`kernel="rbf"`** draws a curved one. Every other setting is in the table.
- **The three calls are this section's what-if** for `class_weight` and `kernel`: the first two differ only in `class_weight`, the last two only in `kernel`.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `kernel` | the shape of boundary allowed: `"linear"` straight, `"rbf"` curved | both | measured above: 0.771 to 0.780 on the balanced model. `"poly"` and `"sigmoid"` exist and are rarely better |
| `C=1.0` | how much a misclassified training point costs against a wider margin; smaller is more regularized | 1.0, the default | measured below |
| `class_weight` | whether the rare class counts for more | `None`, then `"balanced"` | measured above: from 0.536 to 0.771. With 9.7% churners, unbalanced is close to useless |
| `probability=True` | fit an extra step that turns distances into probabilities | on | off is faster, but `predict_proba` then does not exist and `clf_report` fails. Chapter 39 covers the calibration this step performs |
| `gamma="scale"` | for RBF only: how far each training point's influence reaches | the default, set from the data | larger: a wigglier boundary that overfits; smaller: nearly straight |
| `random_state=37` | seed for the internal cross-validation that `probability=True` runs | 37 | with `probability=False` it does nothing. The boundary itself is not random |

**A measured what-if: `C` on the RBF kernel.**

```python
for C in [0.1, 1.0, 10.0]:
    clf_report(
        f"SVM, RBF, balanced, C={C}",
        clf_pipeline(
            SVC(kernel="rbf", C=C, class_weight="balanced", probability=True, random_state=37)
        ),
    )
```

```
[run: W9]
```

[Reading sentence from the real output.]

---

##### P16. Section 37.10 "Compare properly first" (line 1020): settings table for the folds, bullets, and a what-if on `n_splits`

Insert after the output and before "On 4,000 accounts, the picture is clearer":

**How it works:**

- **`StratifiedKFold(n_splits=5, shuffle=True, random_state=37)`** describes how to cut the 4,000 non-test accounts into five folds with the churn rate preserved in each (Chapter 36 section 36.4). It is built once as `folds` and reused by every cross-validation in the rest of the chapter, so every comparison uses the same five cuts.
- **`candidates = {...}`** is a dictionary of name to unfitted pipeline. The three are built fresh here rather than reused from earlier sections, because a fitted pipeline must not be cross-validated: `cross_val_score` refits it in every fold anyway, but starting clean removes any doubt.
- **`X_rest, y_rest`** are the 4,000 training-plus-validation accounts, which is what cross-validation gets: the test set is still locked.
- **`cross_val_score(pipe, X_rest, y_rest, cv=folds, scoring="roc_auc")`** does the five fit-and-score rounds and returns an array of five AUCs. **`s.mean()`** and **`s.std()`** are the estimate and its wobble; **`s.round(3)`** prints the five.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `n_splits=5` | how many folds, so each model is fitted this many times | 5 | more folds: each fit sees more rows and the estimate is steadier, at proportionally more time; 10 is common. Fewer: faster, noisier. Measured below |
| `shuffle=True` | mix the rows before cutting | on | off takes rows in file order, which is fine only if the file is already in random order. Never off for time-ordered rows, where `TimeSeriesSplit` (section 37.12) is the tool |
| `random_state=37` | seed for the shuffle | 37 | a different seed gives different folds and slightly different means. Because `folds` is shared, changing it moves every comparison together, which is what you want |
| `scoring="roc_auc"` | which number to compute on each held-out fold | AUC | `"neg_log_loss"` scores probabilities rather than ranking (negated so that higher is better, as every scorer must be); `"accuracy"` is the wrong choice with 9.7% churners, because "nobody churns" scores 90.3% |

**A measured what-if: `n_splits`.**

```python
for k in [3, 5, 10]:
    f = StratifiedKFold(n_splits=k, shuffle=True, random_state=37)
    s = cross_val_score(candidates["logistic regression"], X_rest, y_rest, cv=f, scoring="roc_auc")
    print(f"{k:>2} folds   mean AUC {s.mean():.3f}   sd {s.std():.3f}")
```

```
[run: W10]
```

[Reading sentence from the real output.]

---

##### P17. Section 37.10 "Learning curves" (line 1059): settings table and bullets

Insert after the output and before the figure:

**How it works:**

- **`learning_curve(model, X, y, ...)`** repeats cross-validation at several training sizes and returns three arrays: the sizes actually used, the training scores, and the held-out scores. Each score array has one row per size and one column per fold.
- **`tr_s.mean(axis=1)`** averages across the five folds for each size. `axis=1` means "across the columns"; `axis=0` would average across sizes instead, which is not what is wanted.
- **`curves[name] = (...)`** keeps the three arrays for the figure. **`zip(n, ..., ...)`** walks the three in step so each printed line has a size, a training AUC, and a cross-validated AUC.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `train_sizes` | which shares of the training fold to try | 0.1, 0.25, 0.5, 0.75, 1.0 | the printed sizes are these shares of 3,200 rows (four folds of 4,000). More points: a smoother curve, more fits. Whole numbers are absolute row counts |
| `cv=folds` | the same five folds as everywhere else | `folds` | a different splitter changes the held-out rows and the curve moves a little |
| `scoring="roc_auc"` | what to compute | AUC | as in the table above |
| `shuffle=True`, `random_state=37` | shuffle each training fold before taking the first 10%, 25%, and so on | on, 37 | off: the smallest subsets are whichever rows happen to come first in the fold. On, with a seed, makes each subset a fair sample and repeatable |

---

##### P18. Section 37.10 "Fixing bias with features" (line 1109): split the 46-line block into two steps, using `clf_pipeline(nums=...)`

Replace the block with:

---

**Step 1: four features built from what the tree and the odds ratios showed.**

```python
engineered = rest.copy()
test_eng = test_acc.copy()
for df in (engineered, test_eng):
    df["no_order_90"] = (df["days_since_last_order"] > 90).astype(int)
    df["no_order_180"] = (df["days_since_last_order"] > 180).astype(int)
    df["late_small_retail"] = (
        (df["late_payment_days"] > 25)
        & (df["company_size"] == "Small")
        & (df["segment"] == "Retail")
    ).astype(int)
    df["new_and_complaining"] = (
        (df["complaints_2024"] >= 2) & (df["tenure_months"] < 18)
    ).astype(int)
ENG = ["no_order_90", "no_order_180", "late_small_retail", "new_and_complaining"]
```

**How it works:**

- **`rest.copy()` and `test_acc.copy()`** make separate tables to add columns to, so the originals used by every other section stay as they were.
- **`for df in (engineered, test_eng):`** applies the same four lines to both tables. Writing the rules once and looping is what guarantees the test set gets *exactly* the same features as the training data; two hand-typed copies drift.
- **`(df["days_since_last_order"] > 90).astype(int)`** is a True/False column turned into 1/0, which is what a model needs. The 90 and 180 are the two thresholds the data spec planted and the tree found; the 25-day, Small, Retail rule is the depth-2 tree's leaf from section 37.6; the complaints-and-tenure rule came from the sales team.
- **`ENG`** lists the four new names, so they can be added to `NUMS` wherever needed.

**Step 2: the same logistic regression, with the four extra columns.**

```python
eng_pipe = clf_pipeline(LogisticRegression(max_iter=2000), nums=NUMS + ENG)
s = cross_val_score(
    eng_pipe, engineered[CATS + NUMS + ENG], y_rest, cv=folds, scoring="roc_auc"
)
print(f"logistic + 4 engineered features   mean AUC {s.mean():.3f}   sd {s.std():.3f}")
```

```
logistic + 4 engineered features   mean AUC 0.849   sd 0.015
```

- **`clf_pipeline(..., nums=NUMS + ENG)`** is section 37.3's recipe with the four new columns added to the numeric list. Nothing else about the model changed, which is what makes the comparison with 0.807 fair: the only difference is the features.

**A measured what-if: which feature carried the gain?** Leave each one out in turn:

```python
for drop in ENG:
    keep = [c for c in ENG if c != drop]
    pipe = clf_pipeline(LogisticRegression(max_iter=2000), nums=NUMS + keep)
    s = cross_val_score(pipe, engineered[CATS + NUMS + keep], y_rest, cv=folds, scoring="roc_auc")
    print(f"without {drop:<20} mean AUC {s.mean():.3f}")
```

```
[run: W11]
```

[Reading sentence from the real output.]

*Fallback if `clf_pipeline` is not given a `nums` argument:* keep the existing `eng_pipe` definition as its own Step 2 block with the sentence "This is `clf_pipeline`'s recipe written out again with `NUMS + ENG` in place of `NUMS`; nothing else differs", and drop the what-if's use of `nums=`.

---

##### P19. Section 37.11 "Random search" (line 1180): split the 29-line block into two, settings table, and a what-if on `n_iter`

Replace the block with:

---

**Step 1: describe the search.**

```python
from scipy.stats import loguniform, randint
from sklearn.model_selection import RandomizedSearchCV

search = RandomizedSearchCV(
    clf_pipeline(HistGradientBoostingClassifier(random_state=37), scale=False),
    param_distributions={
        "model__learning_rate": loguniform(0.01, 0.3),
        "model__max_depth": [2, 3, 4, 6, None],
        "model__min_samples_leaf": randint(10, 100),
        "model__max_iter": randint(100, 500),
        "model__l2_regularization": loguniform(1e-3, 10),
    },
    n_iter=25,
    cv=folds,
    scoring="roc_auc",
    random_state=37,
    n_jobs=1,
)
```

- **`loguniform(0.01, 0.3)`** and **`randint(10, 100)`** are *distributions* to draw from, not values: each of the 25 tries draws a fresh learning rate between 0.01 and 0.3 on a log scale, and a fresh whole number between 10 and 99. A plain list, as for `max_depth`, is drawn from evenly.
- **`"model__learning_rate"`** reaches the setting inside the pipeline, as the existing "How it works" says. Nothing is fitted yet: `search` is a description.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `param_distributions` | for each setting, the range or list to draw from | five settings | a setting left out keeps the model's own value. Ranges that are too wide waste tries on hopeless values; too narrow can miss the best. If the winner sits at the edge of a range, widen it |
| `n_iter=25` | how many combinations to try | 25 | each costs 5 fits (one per fold). Measured below |
| `cv=folds` | the folds every combination is judged on | the shared five | the same folds for every try is what makes the tries comparable |
| `scoring="roc_auc"` | what "best" means | AUC | `"neg_log_loss"` would choose for probability quality instead |
| `random_state=37` | seed for which combinations are drawn | 37 | a different seed tries 25 different combinations and finds a different, similar winner. That is why "the exact winner is partly luck" |
| `n_jobs=1` | cores | one | `-1` runs the folds in parallel; same answer, faster |
| `refit=True` | after the search, refit the winner on all the rows given | the default, not written | this is what makes `search.best_estimator_` a usable fitted model; `refit=False` saves the time and leaves you with only the scores |

**Step 2: run it and read the winner.**

```python
search.fit(X_rest, y_rest)
print(f"best CV AUC {search.best_score_:.3f}")
print(
    {
        k.replace("model__", ""): (round(float(v), 4) if isinstance(v, float) else v)
        for k, v in search.best_params_.items()
    }
)
top = pd.DataFrame(search.cv_results_).sort_values("rank_test_score")
print(
    top[["mean_test_score", "std_test_score"]].head(5).round(3).to_string(index=False)
)
```

[existing output, unchanged]

- **`search.fit(X_rest, y_rest)`** runs all 125 fits, then refits the winner on all 4,000 rows.
- **`best_score_`** is the winner's mean cross-validated AUC. **`best_params_`** is a dictionary of its settings, with the `model__` prefix stripped by `.replace` and floats rounded by the dictionary comprehension so it fits on one line.
- **`cv_results_`** holds every try; as a DataFrame sorted by `rank_test_score`, its top five rows show how close the runners-up were, which is the evidence for "within noise".

**A measured what-if: `n_iter`.** Same search, three budgets:

```python
import time

for budget in [5, 25, 60]:
    t = time.time()
    s = clone(search).set_params(n_iter=budget).fit(X_rest, y_rest)
    print(f"n_iter={budget:<3} best CV AUC {s.best_score_:.3f}   {time.time() - t:.0f} s")
```

```
[run: W12]
```

[Reading sentence from the real output. `clone` is imported in P3; if P3 is not applied, add `from sklearn.base import clone` here.]

---

##### P20. Section 37.11 "Optuna" (line 1234): settings table and two bullets

Add to the existing "How it works":

- **`trial.suggest_float("learning_rate", 0.01, 0.3, log=True)`** is Optuna's version of `loguniform`: `log=True` samples evenly on a log scale. **`suggest_int`** draws a whole number.
- **`study.optimize(objective, n_trials=25)`** runs the loop; **`study.best_value`** and **`study.best_params`** are the winner's score and settings.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `direction="maximize"` | whether a higher or lower score is better | maximize (AUC) | for log loss you would write `"minimize"`; get it wrong and Optuna diligently finds the worst settings |
| `sampler=TPESampler(seed=37)` | the strategy for choosing the next trial, and its seed | TPE, seed 37 | the default sampler is TPE anyway; the seed is what makes the search repeatable. `RandomSampler` would make this the same as random search |
| `n_trials=25` | how many combinations | 25, matching the random search | more trials help Optuna more than random search, because later trials use what earlier ones learned. Not measured separately here: the `n_iter` measurement above shows the shape |
| `log=True` in `suggest_float` | sample on a log scale | on for learning rate and L2 | off, most draws land near the top of the range, and 0.01 to 0.03 is barely explored |
| `optuna.logging.set_verbosity(WARNING)` | how much Optuna prints | warnings only | the default prints a line per trial |

---

##### P21. Section 37.11 "The test set, once" (line 1282): three bullets

Insert between the output and "Reading it":

**How it works:**

- **`final_models`** maps three names to three unfitted pipelines. `search.best_estimator_` is the random-search winner, already fitted, but it is refitted below anyway.
- **`cols = CATS + NUMS + (ENG if "engineered" in name else [])`** adds the four engineered columns only for the model whose name contains "engineered". The two lines after it choose the matching tables the same way. It is a compact way of running three models that need slightly different inputs through one loop.
- **`pipe.fit(source[cols], source["churned_2025"])`** fits on all 4,000 non-test accounts, more than the 3,000 the validation runs used, which is why these test scores are higher than the earlier validation scores. Then **`predict_proba` on the test set**, once, and the numbers are final.

---

##### P22. Section 37.12 (line 1316): split the 35-line block into three steps, with `TimeSeriesSplit` in the table and one what-if

Replace the block with:

---

**The plan, in words.** Load Chapter 36's lead table through the companion helper, so its cleaning and features are not repeated here. Run the same random search as section 37.11 on the leads, but with a cross-validation that respects time. Then fit both the Chapter 36 baseline and the tuned boosting model on the training leads, score them on validation, refit both on training-plus-validation, and score them once on test.

**Step 1: the leads, from Chapter 36.**

```python
import sys

sys.path.append(".")  # so Python finds lead_data.py in this folder
from lead_data import LEAD_CATS, LEAD_NUMS, load_leads, make_model
from sklearn.model_selection import TimeSeriesSplit

leads_train, leads_valid, leads_test = load_leads()
LX = LEAD_CATS + LEAD_NUMS
```

- **`sys.path.append(".")`** and **`from lead_data import ...`** are explained in the existing "How it works". **`load_leads()`** returns the three time-based sets of Chapter 36 section 36.3, and **`make_model`** is Chapter 36's pipeline builder. **`LX`** is the full feature list.

**Step 2: the search, with time-ordered folds.**

```python
lead_search = RandomizedSearchCV(
    make_model(LEAD_CATS, LEAD_NUMS, HistGradientBoostingClassifier(random_state=37)),
    param_distributions={
        "model__learning_rate": loguniform(0.01, 0.3),
        "model__max_depth": [2, 3, 4, 6, None],
        "model__min_samples_leaf": randint(20, 200),
        "model__max_iter": randint(100, 500),
        "model__l2_regularization": loguniform(1e-3, 10),
    },
    n_iter=20,
    cv=TimeSeriesSplit(n_splits=4),
    scoring="roc_auc",
    random_state=37,
    n_jobs=1,
)
lead_search.fit(leads_train[LX], leads_train["won"])
print(f"tuned boosting, time-series CV AUC {lead_search.best_score_:.3f}")
```

```
tuned boosting, time-series CV AUC 0.769
```

- **Two things differ from section 37.11's search.** `min_samples_leaf` ranges up to 200 rather than 100, because there are 7,291 training leads; and `cv=TimeSeriesSplit(n_splits=4)` replaces the shuffled folds.
- **`TimeSeriesSplit(n_splits=4)`** cuts the rows, *in the order they are given*, into five blocks and makes four folds: train on block 1, score on block 2; train on 1 and 2, score on 3; and so on. Every score is on leads later than the ones trained on, as in real use. Because it trusts the row order, `load_leads` must return rows sorted by date; if it did not, the folds would be meaningless and no error would tell you.
- **The CV AUC of 0.769 is lower than the validation AUC that follows** because the early folds train on a few hundred leads from early 2023. That is expected with time-ordered folds and is not a sign of a problem.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `TimeSeriesSplit(n_splits=4)` | how many forward-in-time folds | 4 | more folds: more scores, but the earliest ones train on very little. `max_train_size` caps the training window; `gap` leaves a buffer between training and scoring rows when outcomes take time to settle |
| shuffled `StratifiedKFold` instead | folds that ignore time | not used | measured below |

**Step 3: baseline against boosting, on validation and then once on test.**

```python
for name, fit_rows, eval_rows in [
    ("VALID", leads_train, leads_valid),
    ("TEST", pd.concat([leads_train, leads_valid]), leads_test),
]:
    base = make_model(LEAD_CATS, LEAD_NUMS).fit(fit_rows[LX], fit_rows["won"])
    boost = lead_search.best_estimator_.fit(fit_rows[LX], fit_rows["won"])
    for label, m in [("logistic (Ch 36)", base), ("tuned boosting", boost)]:
        p = m.predict_proba(eval_rows[LX])[:, 1]
        print(
            f"{name:<5} {label:<18} AUC {roc_auc_score(eval_rows['won'], p):.3f}   "
            f"log loss {log_loss(eval_rows['won'], p):.4f}"
        )
```

[existing output, unchanged]

- **The outer loop runs twice**: first fitting on training leads and scoring validation, then fitting on **`pd.concat([leads_train, leads_valid])`**, training and validation stacked into one table, and scoring test. Refitting on more rows before the final test is standard; what is never done is choosing anything by the test score.
- **`make_model(LEAD_CATS, LEAD_NUMS)`** with no model argument is Chapter 36's logistic regression, the baseline. **`lead_search.best_estimator_`** is the boosting winner with its chosen settings; `.fit` refits it on the rows given.
- **The inner loop** scores the two models the same way `clf_report` did, written out because the lead sets are not the account sets.

**A measured what-if: what a shuffled cross-validation would have said.** Run the same search with section 37.10's `folds` in place of `TimeSeriesSplit`, and compare the CV AUC it reports with the 0.769 above:

```python
shuffled = clone(lead_search).set_params(cv=StratifiedKFold(n_splits=4, shuffle=True, random_state=37))
shuffled.fit(leads_train[LX], leads_train["won"])
print(f"tuned boosting, shuffled CV AUC {shuffled.best_score_:.3f}   (time-series CV: {lead_search.best_score_:.3f})")
```

```
[run: W13]
```

[Reading sentence from the real output. The point: a shuffled CV on time-ordered leads reports a more flattering number because it lets the model learn from the future; the time-series number is the honest one, and it is the one that agreed with the test set.]

---

##### P23. Exercise answers: bullets for 5, 7, 10, 11, 12, 13, and a shorter 12

**Exercise 5 (line 1578).** Add after the output:

- **`REG_NUMS = [c for c in REG_NUMS_FULL if c != "log_revenue_2024"]`** drops one column with a list comprehension. It rebinds the name `REG_NUMS` because `reg_pipeline` reads that global name; the last line puts it back so later code is unaffected. Changing a global to steer a function is a habit to avoid in real code (Chapter 29), and it is done here to reuse `reg_pipeline` unchanged.
- **`names_wo`** is rebuilt because the preparation step now produces one fewer column, and the old `names` would mislabel every weight.

**Exercise 7 (line 1628).** Add after the output:

- **`sum(len(g) / len(y_all) * gini(g) for g in (y_all[rule], y_all[~rule]))`** is the weighted Gini in one line: a **generator expression** (Chapter 33) that computes weight × impurity for the yes group and the no group and adds them. It is the same arithmetic as section 37.6's `w_l * gini(left) + w_r * gini(right)`.

**Exercise 10 (line 1694).** Add after the output:

- **`validation_curve(model, X, y, param_name=..., param_range=..., cv=..., scoring=...)`** is `learning_curve`'s sibling: instead of varying the amount of data, it varies one setting and returns training and held-out scores for each value. `param_name="model__max_depth"` names the setting inside the pipeline; `param_range=depths` gives the values to try. Everything else matches section 37.10's tables.

**Exercise 11 (line 1728).** Add after the output:

- **`StackingClassifier(estimators=[...], final_estimator=..., cv=5)`**: `estimators` is a list of (name, model) pairs whose predictions become the inputs of `final_estimator`, a logistic regression that learns how much to trust each. `cv=5` makes those inputs out-of-fold predictions, so the final model never sees a base model's prediction on a row that base model trained on; without it, the stack would learn to trust the overfitted one.

**Exercise 12 (line 1753), shorter version using `clf_pipeline(nums=...)`:**

```python
best = {k.replace("model__", ""): v for k, v in search.best_params_.items()}
boost_eng = clf_pipeline(
    HistGradientBoostingClassifier(**best, random_state=37),
    scale=False,
    nums=NUMS + ENG,
)
s = cross_val_score(
    boost_eng, engineered[CATS + NUMS + ENG], y_rest, cv=folds, scoring="roc_auc"
)
print(
    f"tuned boosting + engineered features   mean AUC {s.mean():.3f}   sd {s.std():.3f}"
)
```

- **`best = {...}`** strips the `model__` prefix from the winning settings, as section 37.11 did for printing. **`**best`** unpacks that dictionary into keyword arguments (Chapter 17), so `HistGradientBoostingClassifier(**best, random_state=37)` is the same as typing each setting out.
- **`nums=NUMS + ENG`** adds the four features, exactly as for the logistic model in section 37.10, so the two gains are comparable.

The output must be re-run and should match the existing `0.846   sd 0.013` exactly, because the pipeline is unchanged; if it does not, the pipelines were not identical and the difference must be found before the shorter version is used. *Fallback without the `nums` argument:* keep the existing block and add the `**best` bullet plus "the pipeline is section 37.10's `eng_pipe` with the imputer's scaler removed and boosting in place of logistic regression".

**Exercise 13 (line 1794).** Add after the output, before "The interval, 0.009 to 0.053":

- **`pd.get_dummies(reg_train[CATS], drop_first=True, dtype=float)`** is pandas's one-hot encoder: one 0/1 column per category value, with the first value of each column dropped (the baseline, as `drop="first"` did in section 37.1). `dtype=float` matters: statsmodels rejects True/False columns.
- **`pd.concat([design, ...], axis=1)`** glues the dummy columns and the numeric columns side by side; `axis=1` means "as new columns" (`axis=0` would stack rows). **`.fillna(median)`** fills blanks with the training medians, by hand, because there is no pipeline here.
- **`sm.add_constant(design)`** adds a column of ones for the intercept. statsmodels does not add one for you, and a regression without it is a different, wrong model.
- **`sm.OLS(y, X).fit()`** takes the **target first, then the features**, the opposite order from scikit-learn's `fit(X, y)`. Swapping them is the most common statsmodels mistake and produces an error about shapes rather than a wrong answer.
- **`.conf_int().loc["rep_id_9"]`** is the 95% interval for that one coefficient, as a low and a high; **`.params`** and **`.pvalues`** hold the estimate and the p-value by the same names.

---

##### P24. "Code words you met in this chapter" table (new, before Key terms)

## Code words you met in this chapter

| Word | Plain meaning | First section |
|---|---|---|
| `train_test_split` | shuffle rows and cut them into two tables | 37.0 |
| `stratify` | keep the share of each class the same in both pieces | 37.0 |
| `random_state` | the seed that makes anything random repeatable | 37.0 |
| `fit` | learn from these rows | 37.1 |
| `predict` / `predict_proba` | apply what was learned; the second returns probabilities | 37.1, 37.3 |
| `coef_`, `intercept_`, `alpha_` | what a model learned, readable after `fit` (the underscore says so) | 37.1, 37.2 |
| `named_steps` | reach one step inside a fitted pipeline | 37.1 |
| `get_feature_names_out` | the column names a preparation step produced | 37.1 |
| `set_params`, `model__setting` | change a setting inside a pipeline by its path | 37.1, 37.11 |
| `np.logspace` | evenly spaced values on a log scale | 37.2 |
| `max_iter` | how long an optimizer may run (logistic regression), or how many trees (boosting) | 37.3, 37.8 |
| `C` | logistic regression's and SVM's regularization, backwards | 37.3, 37.9 |
| `decision_function` | the weighted sum before the sigmoid | 37.3 |
| `n_neighbors` | *k* in k-NN | 37.4 |
| `pd.crosstab` | a count table of two conditions | 37.5 |
| `~` | "not", for a True/False column | 37.5 |
| `lambda` | a one-line function without a name | 37.5 |
| `max_depth`, `min_samples_leaf`, `criterion` | a tree's depth limit, leaf-size floor, and purity measure | 37.6 |
| `export_text` | print a tree as rules | 37.6 |
| `n_estimators`, `max_features` | number of trees; features each split may see | 37.7 |
| `feature_importances_` | how much each feature reduced impurity, summed over trees | 37.7 |
| `learning_rate` | how much of each tree's correction boosting keeps | 37.8 |
| `subsample`, `colsample_bytree` | share of rows and of features each tree sees | 37.8 |
| `kernel`, `class_weight`, `probability` | an SVM's boundary shape, class weighting, and probability step | 37.9 |
| `StratifiedKFold`, `cross_val_score`, `scoring` | the folds, the loop that scores them, and the score used | 37.10 |
| `learning_curve`, `train_sizes` | scores at increasing data sizes | 37.10 |
| `RandomizedSearchCV`, `n_iter`, `param_distributions` | try settings drawn from ranges | 37.11 |
| `loguniform`, `randint` | ranges to draw from, on a log scale or as whole numbers | 37.11 |
| `best_score_`, `best_params_`, `best_estimator_`, `cv_results_` | what a search found | 37.11 |
| `optuna.create_study`, `suggest_float`, `n_trials` | Optuna's search, its settings, and its budget | 37.11 |
| `TimeSeriesSplit` | forward-in-time folds | 37.12 |
| `validation_curve`, `param_name`, `param_range` | scores as one setting varies | exercise 10 |
| `StackingClassifier`, `final_estimator` | models whose predictions feed one more model | exercise 11 |
| `**best` | unpack a dictionary into keyword arguments | exercise 12 |
| `sm.OLS`, `add_constant`, `conf_int` | statsmodels regression, its intercept column, its intervals | exercise 13 |

---

#### WHAT-IFS TO RUN

All runs happen in `companion/ch37/` after the chapter's code has run, so `accounts`, `train_acc`, `valid_acc`, `rest`, `test_acc`, `X_tr`, `y_tr`, `X_va`, `y_va`, `X_rest`, `y_rest`, `folds`, `clf_pipeline`, `clf_report`, `reg_pipeline`, `reg_report`, `candidates`, `search`, `lead_search`, `engineered`, `ENG`, `x_toy`, `y_toy`, and the imports exist. Data: `companion/accounts/accounts.csv` (generator seed 20237) for W1 to W12 and W14; `companion/ch37/lead_data.py` for W13. Paste the printed output exactly, then write the reading sentence from it. Where the outcome I expect is stated, it is a prediction to be checked, not a result.

| Run | Section | Setting | Values | Code | Output to capture |
|---|---|---|---|---|---|
| W1 | 37.0 | `stratify`, `random_state` | (37, none), (1, stratified), (1, none) | P1 | rest and test churn rates, two decimals, for each |
| W2 | 37.1 | `drop`, `strategy` | `drop=None`; `strategy="mean"` | P3 | R², MAE, and the three segment weights for each |
| W4 | 37.3 | `max_iter` | 10 (then 3 if 10 converges) | P5 | the `ConvergenceWarning` text and the AUC line. If neither warns, record that and drop the demonstration |
| W5 | 37.4 | one row by hand | *k* = 5 | below | the five nearest training accounts' churn flags and their share, against `predict_proba` |
| W6 | 37.6 | `min_samples_leaf` | 1, 20, 100 at depth 4 | P11 | AUC and log loss for each |
| W7 | 37.8 | learning rate (by hand) | 0.1, 0.5, 1.0 | P13 | squared error after 3 rounds and the churner's prediction, for each |
| W8 | 37.8 | `learning_rate` × `max_iter` | (0.3, 100), (0.05, 100), (0.05, 300), (0.05, 1000), (0.01, 1000) | P14 | AUC and log loss for each |
| W9 | 37.9 | `C` | 0.1, 1, 10 on RBF balanced | P15 | AUC and log loss for each |
| W10 | 37.10 | `n_splits` | 3, 5, 10 | P16 | mean and sd of AUC for each |
| W11 | 37.10 | leave-one-feature-out | each of `ENG` | P18 | mean CV AUC without each |
| W12 | 37.11 | `n_iter` | 5, 25, 60 | P19 | best CV AUC and seconds for each |
| W13 | 37.12 | `cv` | shuffled `StratifiedKFold(4)` against `TimeSeriesSplit(4)` | P22 | the two CV AUCs |
| W14 | 37.7 | `random_state` | 1, 2, 3 | P12 | AUC and log loss for each |

**W5, the k-NN one-row check (code for the part chat):**

```python
from sklearn.neighbors import NearestNeighbors

knn5 = clf_pipeline(KNeighborsClassifier(n_neighbors=5)).fit(X_tr, y_tr)
prep = knn5.named_steps["prepare"]
one = X_va.iloc[[0]]
finder = NearestNeighbors(n_neighbors=5).fit(prep.transform(X_tr))
dist, idx = finder.kneighbors(prep.transform(one))
print("neighbors' churn flags:", y_tr.iloc[idx[0]].to_list())
print(f"share churned {y_tr.iloc[idx[0]].mean():.1f}   predict_proba {knn5.predict_proba(one)[0, 1]:.1f}")
```

Capture both printed lines. They should agree; if they do not, the difference is worth a sentence (ties in distance are the usual reason). This gives section 37.4 the "one row of Riverstone data" that §6.5 asks for and that k-NN currently lacks.

**Runtime.** W12 at `n_iter=60` is about 100 seconds on one core; everything else is seconds. Total under five minutes.

---

#### EXCEPTIONS

- **Exercise 6 (line 1611):** the only new setting is `weights="distance"`, which the answer's prose explains; the rest is a repeat of section 37.4.
- **Exercise 8 (line 1649):** a deliberate repeat of section 37.7's forest with `n_estimators` looped; it is that setting's measured what-if and is referenced from the P12 table.
- **Exercise 9 (line 1671):** a deliberate repeat of section 37.8's three-rounds block run to 20 rounds; `%` (remainder) was taught in Chapter 17. No new setting.

---

#### Verification the part chat owes after applying

1. `python tools/verify_python.py manuscript/ch37-supervised-learning-algorithms.md --cwd companion/ch37` reports 0 mismatches, including on every block that was split (splitting must not change any output) and on the shortened exercise 12.
2. `python tools/check_code_teaching.py manuscript/ch37-supervised-learning-algorithms.md` reports 0 blocks over 25 lines and no "settings never explained" line. Any block it still flags gets an exception line in the chapter report.
3. A style scan of the new prose: American spelling, no em dashes, none of the banned words.
4. PDF rebuilt; the two new tables in 37.8 checked for width at the page size.
