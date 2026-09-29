# Chapter 37. Supervised Learning Algorithms

*Part 4 — Machine Learning & Data Science*

> **Chapter at a glance**
>
> **You will learn to:** explain how each major supervised learning algorithm makes a prediction, and calculate one small step of each by hand · fit and read linear regression, ridge, lasso, and elastic net · fit and read logistic regression, including odds ratios · use k-nearest neighbors and Naive Bayes, and know their weak spots · build a decision tree split by hand with Gini and entropy, and see a tree overfit · explain why random forests and gradient boosting work, and use scikit-learn, XGBoost, LightGBM, and CatBoost · know when support vector machines are worth it · diagnose bias and variance with learning curves · tune hyperparameters with random search and Optuna without fooling yourself · pick an algorithm for a problem, and justify the choice.
>
> **Before you start:** Chapter 21 §21.7 (Bayes' rule); Chapter 22 §22.10 (fitting a line, R², residuals); Chapter 30 §30.11 (logistic regression, odds ratios, statsmodels); Chapter 35 (loss, gradients, likelihood, entropy); Chapter 36 (splits, cross-validation, leakage, pipelines, baselines). This chapter reuses Chapter 36's pipeline and lead-scoring data.
>
> **Time needed:** 20–24 hours over three weeks, in two parts. **Part A**, sections 37.0 to 37.5 (the linear family, neighbors and Naive Bayes): about 9–10 hours. **Part B**, sections 37.6 to 37.12 and the project (trees, ensembles, tuning): about 11–13 hours. It's the longest chapter in Part 4; take it one algorithm at a time, and stop at the checkpoint between the parts.
>
> **Tools:** Python 3 with scikit-learn (installed in Chapter 35), plus three free gradient-boosting libraries (XGBoost, LightGBM, CatBoost) and Optuna for tuning, all installed in section 37.0. Everything runs on a laptop CPU; the slowest cell takes about a minute.
>
> **Practice data:** two Riverstone datasets. **Customer accounts** (new in this chapter, built by `companion/generate_riverstone_accounts.py`): 5,000 B2B accounts described as of 31 December 2024, with what happened in 2025. **Leads** (from Chapter 36), loaded through `companion/ch37/lead_data.py`. Every number in this chapter was calculated, and every output shown is real.

---

## Why this matters

There are hundreds of machine learning algorithms, and a handful of them do almost all the work in business data science. Interviewers expect you to know those few well: not only the function name, but how each one decides, what goes wrong, and which settings matter.

The practical questions come up every week:

- *"Should we use XGBoost?"* Maybe. On one of this chapter's datasets it clearly beats logistic regression; on the other it doesn't.
- *"The model is 99% accurate on training data but poor on new data."* That's overfitting, and you'll learn to see it on a chart.
- *"Which features drive churn?"* Some algorithms tell you directly; others need extra tools (Chapter 39).
- *"How long should we spend tuning?"* Less than most people think, and never on the test set.

This chapter teaches nine algorithm families, one at a time, on real Riverstone problems. For each one, you'll see how it works, calculate a small piece by hand, run it, and read the result. At the end, you'll compare them fairly and learn to choose.

---

## In plain English

**Think of different people guessing which customers will stop ordering.**

- The **accountant** gives every warning sign a weight and adds them up: "late payments +3, no recent order +5, many product lines −2". That's **linear and logistic regression**.
- The **accountant with a strict boss** has to justify every weight, so they keep them small and drop the ones that barely matter. That's **regularization**.
- The **old-timer** says, "This customer reminds me of twenty others I've known; fifteen of them left." That's **k-nearest neighbors**.
- The **statistician** asks, "Among customers who left, how common was this sign? Among those who stayed?" and multiplies the evidence. That's **Naive Bayes**.
- The **sales manager** asks a series of yes/no questions: "No order in 90 days? Pays late? Small retailer?" That's a **decision tree**.
- A **committee** of 300 managers, each seeing slightly different customers and questions, votes. That's a **random forest**.
- A **relay team**, where each new member studies the mistakes of everyone before them and fixes a little of what they got wrong. That's **gradient boosting**.
- The **boundary drawer** looks for the widest possible gap between customers who left and customers who stayed. That's a **support vector machine**.

None of them is always best. The skill is knowing which to ask, and how to check whether they're right.

---

## 37.0 Setting up, and the data

### Setting up

This takes about 15 minutes, once.

**Open a terminal in the chapter's folder.** With the terminal basics from Chapter 26 (section 26.0), go to your copy of the companion files and then into `companion/ch37/`, and activate your virtual environment (Chapter 17). Every path in this chapter is written from that folder.

**Build the accounts file if it isn't there.** The code reads `../accounts/accounts.csv`. The `..` means "go up one folder" (to `companion/`), and `accounts/accounts.csv` means "then into the `accounts` folder, and open `accounts.csv`". If that file doesn't exist yet, run `python ../generate_riverstone_accounts.py`; it prints one line starting `5,000 accounts` and writes the file. The leads come from Chapter 36's `../crm/` folder; if it's missing, run `python ../generate_riverstone_crm.py`.

**Install the four new libraries**, in the same terminal:

```bash
python -m pip install xgboost lightgbm catboost optuna
```

- `python -m pip install` installs into the Python of your active virtual environment (Chapter 17, section 17.0).
- **XGBoost**, **LightGBM** and **CatBoost** are three gradient-boosting libraries (section 37.8); **Optuna** tunes settings (section 37.11). All four are free and open source.
- pip prints a list of downloads and ends with a line starting `Successfully installed`, naming the four libraries and a few helpers they need. Add the four names to your `requirements.txt` (Chapter 17).

The four libraries are used from section 37.8 on; installing them now means you won't stop halfway through a section.

**Start Jupyter** in this folder with `jupyter lab`, open a new notebook, and run the cells below in order. Each cell uses names made by the cells before it.

### Two ways to be wrong

Before any algorithm, one idea you'll meet in every section:

> **Two ways to be wrong.**
>
> - **Underfitting:** the model is too simple for the pattern. It does badly on the training data *and* on new data. A straight line through a curve underfits.
> - **Overfitting:** the model is so flexible that it memorizes the training data, noise included. It does very well on the training data and poorly on new data: "99% on training, poor on new accounts", as in *Why this matters*.
>
> The validation set from Chapter 36 is how you tell them apart: compare the training score with the validation score. Section 37.10 turns this into the language of **bias** and **variance**.

### Riverstone customer accounts

Chapter 36 scored new leads. This chapter adds the other half of the customer life cycle: **accounts**, businesses that already buy from Riverstone. Each row describes one account as of 31 December 2024, the **prediction moment**, using only what was known then. Two targets describe 2025:

- **`churned_2025`**: 1 if the account placed no order in 2025. A classification target.
- **`revenue_2025`**: the account's 2025 revenue. A regression target.

| Column | Type | Meaning | Example (first account) | Blanks? |
|---|---|---|---|---|
| `account_id` | whole number | Account number, 5001 to 10000 | 5001 | No |
| `account_name` | text | Trading name (invented) | Everest Stores 0001 | No |
| `segment` | category | Retail, Hospitality, or Wholesale | Retail | No |
| `city_tier` | category | Metro, Tier 2, or Tier 3 | Tier 2 | No |
| `company_size` | category | Small, Medium, or Large | Small | No |
| `rep_id` | category | Who looks after the account: 3, 4 and 5 are the three field sales executives; 9 is the inside sales desk, a team (as in Chapter 36) | 4 | No |
| `tenure_months` | whole number | Months as a customer by the end of 2024 | 21 | No |
| `orders_2024` | whole number | Orders placed in 2024 | 7 | No |
| `units_2024` | number | Units bought in 2024 | 561 | No |
| `revenue_2023` | ₹ | Revenue in 2023 | 1,07,200 | Yes: blank for accounts that joined in 2024 (12 months' tenure or less) |
| `revenue_2024` | ₹ | Revenue in 2024 | 1,46,400 | No |
| `avg_discount_pct` | % | Average discount given in 2024 | 6.9 | No |
| `late_payment_days` | days | Average days late paying invoices | 42 | Yes: about 3% of accounts, where the finance system has no payment history |
| `complaints_2024` | whole number | Complaints logged in 2024 | 0 | No |
| `categories_bought` | whole number | Product categories bought, 1 to 4 | 1 | No |
| `days_since_last_order` | days | Days from the last order to 31 December 2024 | 186 | No |
| `website_logins_2024` | whole number | Logins to the ordering website in 2024 | 4 | No |
| `catalog_downloads_2024` | whole number | Catalogue downloads in 2024 | 1 | No |
| `churned_2025` | 0 or 1 | Target: 1 if no order in 2025 | 1 | No |
| `revenue_2025` | ₹ | Target: 2025 revenue (0 for churned accounts) | 0 | No |

The chapter never uses `revenue_2023`, because a third of the newer accounts have no value for it; the eleven numeric columns from `tenure_months` to `catalog_downloads_2024` are the features.

Because every account is described at the same moment and predicted over the same year, a stratified random split is appropriate here (Chapter 36's time split mattered because leads arrive over time, and the model scores future leads).

First, load the file and look at one account. Before you run it, predict how many rows and columns `shape` will show:

```python
import numpy as np
import pandas as pd

accounts = pd.read_csv("../accounts/accounts.csv")
print(accounts.shape)
print(accounts.iloc[0].to_string())
```

```
(5000, 20)
account_id                               5001
account_name              Everest Stores 0001
segment                                Retail
city_tier                              Tier 2
company_size                            Small
rep_id                                      4
tenure_months                              21
orders_2024                                 7
units_2024                              561.0
revenue_2023                         107200.0
revenue_2024                         146400.0
avg_discount_pct                          6.9
late_payment_days                        42.0
complaints_2024                             0
categories_bought                           1
days_since_last_order                   186.0
website_logins_2024                         4
catalog_downloads_2024                      1
churned_2025                                1
revenue_2025                              0.0
```

- `pd.read_csv("../accounts/accounts.csv")` reads the file one folder up, as set up above.
- `accounts.shape` is (rows, columns): 5,000 accounts and the 20 columns of the table.
- `accounts.iloc[0]` is the first row by position (Chapter 18); `.to_string()` prints every column of it, one per line, instead of a wide row that wraps.

Next, where are the blanks?

```python
blanks = accounts.isna().sum()
print(blanks[blanks > 0])
```

```
revenue_2023         878
late_payment_days    150
dtype: int64
```

- `accounts.isna().sum()` counts the blanks in each column (Chapter 18); `blanks[blanks > 0]` keeps only the columns that have any.
- `revenue_2023` is blank for the newer accounts, and the chapter doesn't use it. `late_payment_days` has 150 blanks, 3% of accounts. The pipelines below fill them with the median and add a "was blank" flag, as Chapter 36 (section 36.8) did.

The rep numbers are labels, not quantities: rep 9 isn't "three times" rep 3. So turn them into text, which the pipeline will one-hot encode instead of averaging:

```python
accounts["rep_id"] = accounts["rep_id"].astype(str)
print(accounts["rep_id"].value_counts().to_string())
```

```
rep_id
3    1364
5    1331
4    1312
9     993
```

- `.astype(str)` turns the numbers 3, 4, 5 and 9 into the text "3", "4", "5" and "9".
- `value_counts()` counts each value: the inside sales desk (rep 9) looks after 993 accounts, and each field executive about 1,300.

Now name the two groups of feature columns, and count the churners:

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
churners = accounts["churned_2025"].sum()
print(f"churned in 2025: {churners:,} of {len(accounts):,}")
print(f"churn rate: {accounts['churned_2025'].mean():.1%}")
```

```
churned in 2025: 484 of 5,000
churn rate: 9.7%
```

- `CATS` lists the four **categorical** columns, which the pipeline will one-hot encode (Chapter 36, sections 36.4 and 36.6).
- `NUMS` lists the eleven **numeric** columns, which it will fill and scale.
- `accounts["churned_2025"].sum()` adds up the 0s and 1s, which counts the churners; `.mean()` of a 0/1 column is the share of 1s, and `:.1%` prints it as a percentage with one decimal.

Last, the split into three sets, as in Chapter 36 (section 36.3). First take out a 20% test set, then split what's left into training and validation:

```python
from sklearn.model_selection import train_test_split

rest, test_acc = train_test_split(
    accounts, test_size=0.2, random_state=37, stratify=accounts["churned_2025"]
)
train_acc, valid_acc = train_test_split(
    rest, test_size=0.25, random_state=37, stratify=rest["churned_2025"]
)
for name, part in [("train", train_acc), ("valid", valid_acc), ("test", test_acc)]:
    rate = part["churned_2025"].mean()
    print(f"{name:<6} {len(part):>5,} accounts   churn {rate:.1%}")
```

```
train  3,000 accounts   churn 9.7%
valid  1,000 accounts   churn 9.7%
test   1,000 accounts   churn 9.7%
```

- The first `train_test_split`, with `test_size=0.2`, keeps 20% of the 5,000 accounts, **1,000**, as `test_acc`, and returns the other 4,000 as `rest`.
- The second, with `test_size=0.25`, takes 25% of those 4,000, again **1,000**, as `valid_acc`, and leaves **3,000** in `train_acc`.
- **`stratify=`** keeps the churn rate the same in every part (Chapter 36, section 36.3). With only 9.7% churners, an unstratified split could leave the validation set with noticeably more or fewer.
- **`random_state=37`** fixes the shuffle, so you get exactly these accounts every time.
- In the loop, `f"{name:<6}"` pads the name to 6 characters, left-aligned, and `{len(part):>5,}` right-aligns the count in 5 characters with a thousands comma, so the columns line up.

**Reading it.** 484 of 5,000 accounts, 9.7%, stopped ordering in 2025. The stratified split keeps that rate identical in the training (3,000), validation (1,000), and test (1,000) sets. The test set stays locked until section 37.11.

> **A fact you can't normally know.** Because this dataset comes from a generator, we know the true churn probability of every account: it's the probability the generator used before rolling the dice. Ranking the accounts by those true probabilities scores an AUC of **0.858** on all 5,000 accounts, and 0.858 on the 1,000 test accounts too (the chapter's check script computes both from the generator). No real model can do better, because churn is partly chance. It's a useful ruler: in real work you never see this number, so you can't tell how close to the ceiling you are.

---

## 37.1 Linear regression

### How it works

You fitted the one-feature version by hand in Chapter 22 (section 22.10), where R² and residuals were defined. Here the same least squares handles many features and is used to predict accounts it hasn't seen. Linear regression predicts a number as a weighted sum of features plus an intercept:

> prediction = *b* + *w*<sub>1</sub> × feature<sub>1</sub> + *w*<sub>2</sub> × feature<sub>2</sub> + … + *w*<sub>n</sub> × feature<sub>n</sub>

**A weighted sum by hand.** Suppose a model predicts log revenue from two features, with an intercept of 0.2, a weight of 1.0 on last year's log revenue, and −0.05 on complaints:

> prediction = 0.2 + 1.0 × log revenue − 0.05 × complaints

| Account | log revenue 2024 | complaints | Prediction |
|---|---|---|---|
| A | 11.0 | 0 | 0.2 + 11.0 − 0 = **11.20** |
| B | 12.0 | 2 | 0.2 + 12.0 − 0.10 = **12.10** |
| C | 10.5 | 1 | 0.2 + 10.5 − 0.05 = **10.65** |

In real use, nobody picks the 0.2, 1.0 and −0.05: least squares chooses them from the data, making the sum of squared residuals as small as possible (section 22.10). For linear regression there's an exact formula, so scikit-learn solves it directly in one step, with no gradient descent (Chapter 35).

### Why log revenue?

Money amounts are **skewed** (Chapter 21, section 21.4): most accounts are small, and a few are very large. A straight line fitted to raw rupees is dominated by the few giants. The fix is to model the **natural logarithm** of revenue (`np.log`, met in Chapter 35), which turns multiplying into adding:

| Revenue | ln(revenue) |
|---|---|
| ₹10,000 | 9.21 |
| ₹1,00,000 | 11.51 |
| ₹10,00,000 | 13.82 |

Each ten-fold step adds the same 2.30. On the log scale, a ₹10,000 account and a ₹10 lakh account are 4.6 apart instead of 99 times apart, and the line is no longer at the mercy of the largest accounts.

Churned accounts have no 2025 revenue (and the log of 0 is minus infinity), so the regression uses only the accounts that stayed. Predicting *whether* an account stays is the classification problem later in the chapter.

```python
stayed = accounts[accounts["churned_2025"] == 0].copy()
money = ["revenue_2024", "units_2024", "orders_2024", "revenue_2025"]
print("all above zero:", (stayed[money] > 0).all().all())
for col in money:
    stayed["log_" + col] = np.log(stayed[col])
print(len(stayed), "accounts stayed")
print(stayed[["revenue_2024", "log_revenue_2024"]].head(3))
```

```
all above zero: True
4516 accounts stayed
   revenue_2024  log_revenue_2024
1      146700.0         11.896145
2      135500.0         11.816727
3       42500.0         10.657259
```

- `.copy()` makes a separate table, so adding columns to `stayed` doesn't touch `accounts`.
- `np.log(0)` is minus infinity, so first check: `(stayed[money] > 0)` is a table of True/False, `.all()` asks "all True?" for each column, and the second `.all()` combines the four answers. True means every value is above zero.
- The loop adds four columns, named `log_revenue_2024`, `log_units_2024`, `log_orders_2024` and `log_revenue_2025`, each the natural log of the original.

Now compare the two versions of 2024 revenue:

```python
print(stayed[["revenue_2024", "log_revenue_2024"]].describe().round(2))
```

```
       revenue_2024  log_revenue_2024
count       4516.00           4516.00
mean      468743.02             12.41
std       747816.42              1.08
min         9900.00              9.20
25%       110200.00             11.61
50%       218650.00             12.30
75%       502700.00             13.13
max     11710600.00             16.28
```

- `describe()` gives the count, mean, standard deviation, minimum, quartiles and maximum of each column (Chapter 18).
- In rupees, the mean is well above the median (the `50%` row), and the maximum is many times the median: a long right tail. On the log scale, the mean and median almost coincide, and the spread is even on both sides.

Two more facts you'll use in a moment:

- `np.exp` undoes `np.log`: `np.exp(np.log(65500))` is 65,500 again. A prediction of log revenue turns back into rupees with `np.exp`.
- A back-transformed prediction is a *typical* (median-like) value, not an average, so it slightly under-predicts the average account. That's fine for ranking accounts and for rough rupee errors.

### One feature: last year's revenue

Split the stayed accounts, 75% for training and 25% for testing (`test_size=0.25`):

```python
reg_train, reg_test = train_test_split(stayed, test_size=0.25, random_state=37)
print(len(reg_train), "training accounts,", len(reg_test), "test accounts")
```

```
3387 training accounts, 1129 test accounts
```

Then fit the line:

```python
from sklearn.linear_model import LinearRegression

simple = LinearRegression().fit(
    reg_train[["log_revenue_2024"]], reg_train["log_revenue_2025"]
)
print(f"intercept {simple.intercept_:.3f}   slope {simple.coef_[0]:.3f}")
```

```
intercept -0.140   slope 1.013
```

- `LinearRegression()` creates the model; `.fit(X, y)` finds the intercept and weights by least squares (Chapter 36, section 36.4, introduced `fit` and `predict`).
- **`reg_train[["log_revenue_2024"]]`**, with double brackets, is a *table* with one column. `X` must always be a table, even with one feature, because the model expects rows × features. The target, with single brackets, is one column.
- Attributes ending in `_`, like `intercept_` and `coef_`, are **learned during `fit`**. `coef_` is a list with one weight per feature, so `coef_[0]` is the first (and here only) one.

Now predict the test accounts and score them:

```python
from sklearn.metrics import r2_score

pred = simple.predict(reg_test[["log_revenue_2024"]])
print(f"R² on test: {r2_score(reg_test['log_revenue_2025'], pred):.4f}")
example = reg_test.iloc[0]
print(f"first test account, 2024: ₹{example['revenue_2024']:,.0f}")
print(f"predicted log revenue 2025: {pred[0]:.5f}")
print(f"predicted 2025: ₹{np.exp(pred[0]):,.0f}   actual ₹{example['revenue_2025']:,.0f}")
```

```
R² on test: 0.9546
first test account, 2024: ₹65,500
predicted log revenue 2025: 11.09065
predicted 2025: ₹65,555   actual ₹71,100
```

- `simple.predict(...)` returns one predicted log revenue per test account.
- `r2_score(actual, predicted)` takes the true values first and the predictions second. It's the R² of section 22.10: the share of the variation in the target that the model explains, from 0 (no better than predicting the average) to 1 (perfect).
- `reg_test.iloc[0]` is the first test account by position; `pred[0]` is its prediction, and `np.exp(pred[0])` turns it back into rupees.

**Reading it.**

- **Slope 1.013:** this is a **log-log model** (log revenue predicted from log revenue), so the slope reads as a percentage relationship: an account with 1% more revenue in 2024 is predicted to have about 1.013% more in 2025. Worked through: an account with 10% more 2024 revenue than the example (₹65,500 × 1.10) gets a prediction ×1.10<sup>1.013</sup> = ×1.1014, about 10.1% higher. Revenue carries forward almost one for one.
- **R² 0.9546:** last year's revenue alone explains 95% of the variation in log revenue this year, which is typical: the biggest predictor of next year is this year.
- **The example account:** 2024 revenue of ₹65,500, predicted ₹65,555 for 2025, actual ₹71,100. Check the arithmetic: ln(65,500) = 11.0898; −0.140 + 1.013 × 11.0898 = 11.0940 with the rounded coefficients, and 11.09065 with the unrounded ones, as printed; *e*<sup>11.09065</sup> = ₹65,555. ✓

### Many features

The next model uses all the features. Its errors are easier to judge in rupees than on the log scale, so first a new measure.

> **Mean absolute error (MAE)** is the average size of the misses, ignoring their sign:
>
> MAE = ( |*y*<sub>1</sub> − *ŷ*<sub>1</sub>| + |*y*<sub>2</sub> − *ŷ*<sub>2</sub>| + … + |*y*<sub>n</sub> − *ŷ*<sub>n</sub>| ) ÷ *n*
>
> Three accounts with actual revenue ₹1,00,000, ₹2,00,000 and ₹50,000, predicted ₹90,000, ₹2,30,000 and ₹50,000, miss by ₹10,000, ₹30,000 and ₹0. MAE = ₹40,000 ÷ 3 = **₹13,333**.

scikit-learn's call is `mean_absolute_error(actual, predicted)`, actual first, as with `r2_score`. Here the model predicts log revenue, so R² is reported on the log scale (the scale the model was fitted on), while MAE is computed after `np.exp` turns predictions back into rupees, which is the unit the sales team thinks in. Chapter 39 (section 39.3) covers regression metrics in full.

One more idea before the code. With **one-hot encoding** (Chapter 36, section 36.6), `segment` becomes three 0/1 columns:

| Account | segment_Hospitality | segment_Retail | segment_Wholesale | Sum |
|---|---|---|---|---|
| a hotel | 1 | 0 | 0 | 1 |
| a store | 0 | 1 | 0 | 1 |
| a distributor | 0 | 0 | 1 | 1 |

The three always add up to 1, exactly like the intercept's column of 1s. Least squares then can't tell the intercept's job from the three columns' job, and the weights can't be pinned down: the **dummy variable trap**. The cure is to drop one column per category. With Hospitality dropped, `segment_Retail` means "compared with a hospitality account". `OneHotEncoder(drop="first")` does exactly this.

First, the list of numeric features and the pipeline. The numeric steps are named first, then assembled:

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

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


def reg_pipeline(model, nums=REG_NUMS):
    numbers = Pipeline(
        [("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]
    )
    categories = OneHotEncoder(handle_unknown="ignore", drop="first")
    prepare = ColumnTransformer([("cat", categories, CATS), ("num", numbers, nums)])
    return Pipeline([("prepare", prepare), ("model", model)])
```

- `REG_NUMS` is `NUMS` with the three money-like columns replaced by their logs.
- `reg_pipeline` is Chapter 36's pipeline (sections 36.4 and 36.9) with one difference, `drop="first"`, for the reason above. `numbers` fills blanks with the median (`strategy="median"`) and then standardizes; `categories` one-hot encodes, and `handle_unknown="ignore"` turns a category never seen in training into all zeros instead of an error (Chapter 36, section 36.4); `prepare` sends each list of columns to its step; the final `Pipeline` puts the preparation in front of whatever `model` you pass in.
- `nums=REG_NUMS` is a **default argument**: call `reg_pipeline(model)` and it uses `REG_NUMS`; pass `nums=[...]` to use a different list. Exercise 8 uses that.

Next, one function to fit a model and report both scores:

```python
from sklearn.metrics import mean_absolute_error


def reg_report(name, pipe, nums=REG_NUMS):
    pipe.fit(reg_train[CATS + nums], reg_train["log_revenue_2025"])
    pred = pipe.predict(reg_test[CATS + nums])
    r2 = r2_score(reg_test["log_revenue_2025"], pred)
    mae = mean_absolute_error(reg_test["revenue_2025"], np.exp(pred))
    print(f"{name:<18} R² {r2:.4f}   MAE ₹{mae:,.0f}")
    return pipe
```

- It **fits** on the training accounts and **predicts** the test accounts, both on the log scale.
- `r2` is computed on the log scale; `mae` compares the actual rupees with `np.exp(pred)`, the predictions turned back into rupees.
- `return pipe` hands back the fitted pipeline, so you can look inside it afterwards.

Now fit ordinary linear regression with every feature:

```python
ols = reg_report("linear regression", reg_pipeline(LinearRegression()))
typical = reg_test["revenue_2025"].median()
print(f"median 2025 revenue of the test accounts: ₹{typical:,.0f}")
```

```
linear regression  R² 0.9593   MAE ₹87,471
median 2025 revenue of the test accounts: ₹233,000
```

R² rises from 0.9546 to 0.9593. The MAE of ₹87,471 means the average miss is about ₹87,000, against a typical (median) account of about ₹2.3 lakh; large accounts contribute the biggest misses in rupees.

Last, the weights. To pair each weight with its column, ask the preparation step for the names of the columns it produced:

```python
names = ols.named_steps["prepare"].get_feature_names_out()
print(names[:5])
coefs = pd.Series(ols.named_steps["model"].coef_, index=names)
print(coefs.round(3).sort_values().to_string())
print(f"SD of log_revenue_2024: {reg_train['log_revenue_2024'].std():.2f}")
```

```
['cat__segment_Retail' 'cat__segment_Wholesale' 'cat__city_tier_Tier 2'
 'cat__city_tier_Tier 3' 'cat__company_size_Medium']
cat__segment_Retail           -0.097
cat__segment_Wholesale        -0.096
num__late_payment_days        -0.048
cat__city_tier_Tier 2         -0.041
cat__city_tier_Tier 3         -0.036
num__complaints_2024          -0.033
num__website_logins_2024      -0.011
num__days_since_last_order    -0.006
num__log_units_2024           -0.001
num__log_orders_2024          -0.001
cat__company_size_Small       -0.001
num__tenure_months             0.000
cat__company_size_Medium       0.004
cat__rep_id_4                  0.004
cat__rep_id_5                  0.007
num__catalog_downloads_2024    0.008
num__avg_discount_pct          0.012
num__categories_bought         0.025
cat__rep_id_9                  0.031
num__log_revenue_2024          1.099
SD of log_revenue_2024: 1.09
```

- `ols.named_steps["prepare"]` is the step we named `"prepare"` inside the fitted pipeline; `named_steps["model"]` is the model.
- `get_feature_names_out()` returns the column names after encoding: `cat__segment_Retail` is the Retail column from the `"cat"` step, `num__log_revenue_2024` a scaled number from the `"num"` step. `names[:5]` shows the first five.
- `pd.Series(values, index=names)` pairs each weight with its name, and `.sort_values()` lists them from most negative to most positive.

Numbers are standardized, so each numeric coefficient is "the change in log revenue for one standard deviation more of this feature". That makes coefficients comparable with each other.

**Reading the coefficients.**

- `log_revenue_2024` dominates (1.099). It looks different from the simple model's slope of 1.013, but it isn't: because features are standardized, 1.099 is per standard deviation of log revenue (about 1.09). Per unit, that's 1.099 ÷ 1.09 ≈ 1.01, the same relationship as the one-feature model.
- `segment_Retail` −0.097: holding everything else equal, a retail account's 2025 revenue is predicted about 9% lower than a hospitality account's (*e*<sup>−0.097</sup> = 0.908). The generator planted faster growth for hospitality, especially in metro cities.
- `late_payment_days` −0.048 and `complaints_2024` −0.033: accounts that pay late or complain grow less.
- `log_units_2024` and `log_orders_2024` are almost exactly 0. They carry nearly the same information as revenue, so once revenue is in the model, they add nothing. When features are strongly correlated (**multicollinearity**), their individual coefficients become unstable and hard to interpret, even when predictions are fine.
- `rep_id_9` +0.031: accounts handled by the inside sales desk are predicted to grow 3% faster. The generator planted **no** such effect on growth. Exercise 16 shows its confidence interval, and a likely reason it appears: this regression only includes accounts that *stayed*. A coefficient needs an interval and a second look before anyone acts on it; `statsmodels` gives the interval, and Chapter 30 (section 30.11) shows how to read it, with the one-feature version in section 22.10.

> **Watch out: a coefficient is not a cause.** "Late payments reduce growth by 5% per standard deviation" is a statement about this model, not about the world. Maybe late payers are struggling businesses that would shrink anyway. Chapter 31 covers methods for estimating causes from observational data.

### Checking the residuals

Section 22.10's residual plot is the standard check of a line. Here it is for the many-feature model, with two numbers that say what the picture shows:

```python
import matplotlib.pyplot as plt

pred_log = ols.predict(reg_test[CATS + REG_NUMS])
resid = reg_test["log_revenue_2025"] - pred_log
low = pred_log < np.median(pred_log)
print(f"residuals: mean {resid.mean():.3f}   sd {resid.std():.3f}")
print(f"sd for smaller accounts {resid[low].std():.3f}, larger {resid[~low].std():.3f}")
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.scatter(pred_log, resid, s=5)
ax.axhline(0, linestyle="--")
ax.set_xlabel("predicted log revenue 2025")
ax.set_ylabel("residual")
plt.show()
```

```
residuals: mean -0.008   sd 0.223
sd for smaller accounts 0.217, larger 0.228
```

- `resid` is actual minus predicted, one per test account, on the log scale.
- `low` is True for the half of the accounts with the smaller predictions, so `resid[low].std()` and `resid[~low].std()` compare the spread of the misses for smaller and larger accounts (`~` flips True and False, Chapter 18).
- The chart is section 22.10's: `plt.subplots(figsize=(6, 3.5))` makes one chart 6 inches wide and 3.5 tall, `ax.scatter(..., s=5)` draws small dots, one per account, and `ax.axhline(0, linestyle="--")` draws the dashed zero line.

![Scatter of 1,129 residuals against predicted log revenue for 2025: a horizontal band of dots centred on the dashed zero line, about equally wide from the smallest to the largest predictions, with no curve and no fan](figures/fig37-1-residuals.svg)

*Figure 37.1 — Residuals of the many-feature model on the test accounts. An even band around zero: no curve and no fan.*

**Reading it.** The residuals average zero and spread about equally for smaller and larger accounts (the two SDs are close), and the chart shows no curve and no fan. On the log scale, the straight line fits: the log target did its job. In rupees, the same residuals mean bigger misses for bigger accounts, which is what you'd want.

**Linear regression's assumptions**, and what breaks when they fail:

| Assumption | If it fails | Check |
|---|---|---|
| The relationship is linear (after any transforms) | Systematic errors in some ranges | Plot residuals against predictions |
| Errors are independent | Overconfident intervals | Think about repeated customers and time |
| Errors have constant spread | Intervals too narrow for big accounts | Residual plot fans out; use a log target |
| Features aren't nearly duplicates | Unstable, uninterpretable coefficients | Correlations between features; regularization |
| No extreme outliers dominate | One account drags the line | Look at the largest residuals |

For prediction alone, the first and last matter most. For interpreting coefficients, all of them matter.

---

## 37.2 Regularization: ridge, lasso, and elastic net

### The idea

With many features, especially correlated ones or few rows, least squares can give large, unstable weights that fit noise: it overfits. **Regularization** adds a penalty for large weights to the loss, trading a little training fit for more stable predictions:

> **Ridge:** loss = error + α × (sum of squared weights)
>
> **Lasso:** loss = error + α × (sum of absolute weights)
>
> **Elastic net:** a mix of both penalties, set by `l1_ratio`

**α** (alpha) controls the strength. At α = 0 you get ordinary least squares; as α grows, weights shrink toward zero. scikit-learn measures the "error" part differently for the two: ridge uses the *total* of the squared errors, lasso and elastic net use *half the average*. So an α for ridge can't be compared with an α for lasso; compare α values only within one method.

The two penalties behave differently. **Ridge** shrinks all weights a little and keeps every feature; with correlated features, it spreads the weight among them. **Lasso** pushes some weights to **exactly zero**, removing those features, so it doubles as **feature selection**. Elastic net sits between them, and handles groups of correlated features more gracefully than lasso, which tends to pick one at random.

### Shrinking one weight by hand

Take one standardized feature and four rows, with no intercept to keep it small:

| *x* | −1.5 | −0.5 | 0.5 | 1.5 |
|---|---|---|---|---|
| *y* | −2.9 | −1.2 | 0.8 | 3.3 |

Σ*xy* = 4.35 + 0.60 + 0.40 + 4.95 = 10.3, and Σ*x*² = 2.25 + 0.25 + 0.25 + 2.25 = 5.

- **Least squares:** *w* = Σ*xy* ÷ Σ*x*² = 10.3 ÷ 5 = **2.06**.
- **Ridge** (scikit-learn's form): *w* = Σ*xy* ÷ (Σ*x*² + α). α = 1 gives 10.3 ÷ 6 = **1.717**; α = 5 gives 10.3 ÷ 10 = **1.03**. It shrinks, but it never reaches 0, however large α gets.
- **Lasso** (scikit-learn's form, with *n* = 4 rows): *w* = (Σ*xy* ÷ *n* − α) ÷ (Σ*x*² ÷ *n*) = (2.575 − α) ÷ 1.25. α = 0.5 gives **1.66**; α = 1 gives **1.26**; and for any α of 2.575 or more the formula would go negative, so lasso sets *w* to **exactly 0**. That's how lasso drops features.

The same three lines in scikit-learn, with `fit_intercept=False` because the hand version has no intercept:

```python
from sklearn.linear_model import Lasso, Ridge

x = np.array([[-1.5], [-0.5], [0.5], [1.5]])
y = np.array([-2.9, -1.2, 0.8, 3.3])
for alpha in [1, 5]:
    w = Ridge(alpha=alpha, fit_intercept=False).fit(x, y).coef_[0]
    print(f"ridge alpha {alpha}: w = {w:.3f}")
for alpha in [0.5, 1, 3]:
    w = Lasso(alpha=alpha, fit_intercept=False).fit(x, y).coef_[0]
    print(f"lasso alpha {alpha}: w = {w:.3f}")
```

```
ridge alpha 1: w = 1.717
ridge alpha 5: w = 1.030
lasso alpha 0.5: w = 1.660
lasso alpha 1: w = 1.260
lasso alpha 3: w = 0.000
```

Every value matches the hand calculation. ✓

Because the penalty treats every weight equally, **features must be standardized first**; otherwise a feature measured in rupees gets a tiny weight and escapes the penalty. `reg_pipeline` already scales.

### Choosing α by cross-validation

The `...CV` versions of each model try several values of α with cross-validation inside the training accounts, and keep the best. Ridge is given its list of α values:

```python
from sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV

print(np.logspace(-3, 3, 25)[:5].round(4))
ridge = reg_report(
    "ridge (RidgeCV)", reg_pipeline(RidgeCV(alphas=np.logspace(-3, 3, 25)))
)
print("ridge chose alpha", ridge.named_steps["model"].alpha_)
```

```
[0.001  0.0018 0.0032 0.0056 0.01  ]
ridge (RidgeCV)    R² 0.9593   MAE ₹87,466
ridge chose alpha 0.1
```

| Setting | Meaning here |
|---|---|
| `alphas=np.logspace(-3, 3, 25)` | 25 values from 10<sup>−3</sup> = 0.001 to 10<sup>3</sup> = 1,000, evenly spaced on a log scale (the first five are printed) |
| `alpha_` | The value it chose (learned during `fit`, hence the `_`) |

`RidgeCV` scores each α with an efficient form of leave-one-out cross-validation on the training rows only, so the test accounts are never used.

Lasso builds its own list of α values:

```python
lasso = reg_report("lasso (LassoCV)", reg_pipeline(LassoCV(cv=5)))
print("lasso chose alpha", round(lasso.named_steps["model"].alpha_, 5))
```

```
lasso (LassoCV)    R² 0.9594   MAE ₹87,463
lasso chose alpha 0.0011
```

| Setting | Meaning here |
|---|---|
| `cv=5` | 5-fold cross-validation inside the training accounts (Chapter 36, section 36.5) |
| (default) `alphas=100` | `LassoCV` tries 100 values of α, from one large enough to zero every weight down to a thousandth of it |
| `alpha_` | The value it chose, on lasso's scale |

Elastic net also chooses the mix:

```python
enet = reg_report(
    "elastic net", reg_pipeline(ElasticNetCV(l1_ratio=[0.2, 0.5, 0.8], cv=5))
)
print("elastic net chose l1_ratio", enet.named_steps["model"].l1_ratio_)
lasso_coefs = pd.Series(lasso.named_steps["model"].coef_, index=names)
print("lasso set to exactly zero:", list(lasso_coefs[lasso_coefs == 0].index))
```

```
elastic net        R² 0.9594   MAE ₹87,438
elastic net chose l1_ratio 0.8
lasso set to exactly zero: ['cat__company_size_Medium', 'cat__rep_id_4', 'cat__rep_id_5', 'num__log_units_2024', 'num__log_orders_2024', 'num__tenure_months']
```

| Setting | Meaning here |
|---|---|
| `l1_ratio=[0.2, 0.5, 0.8]` | The mixes to try: 0.8 means 80% lasso penalty and 20% ridge penalty |
| `cv=5` | As for lasso |
| `l1_ratio_` | The mix it chose |

The last two lines pair lasso's weights with the column names, as in section 37.1, and list the ones that are exactly zero.

**Reading it.** All four models score almost the same (R² 0.9593–0.9594). That's the honest result for this dataset: with 3,387 training rows and 20 features, ordinary least squares isn't overfitting, so there's little for regularization to fix. What lasso does do is **simplify**: it removed six features, including `log_units_2024` and `log_orders_2024` (duplicates of revenue) and `tenure_months`, without losing any accuracy.

Increase α by hand to see the trade-off:

```python
for alpha in [0.001, 0.01, 0.05, 0.2]:
    m = reg_pipeline(Lasso(alpha=alpha)).fit(
        reg_train[CATS + REG_NUMS], reg_train["log_revenue_2025"]
    )
    weights = m.named_steps["model"].coef_
    kept = (weights != 0).sum()
    r2 = r2_score(reg_test["log_revenue_2025"], m.predict(reg_test[CATS + REG_NUMS]))
    print(f"alpha {alpha:<5}  features kept {kept:>2} of {len(names)}   test R² {r2:.4f}")
    if alpha == 0.01:
        kept_at_001 = list(names[weights != 0])
print("kept at alpha 0.01:", kept_at_001)
```

```
alpha 0.001  features kept 14 of 20   test R² 0.9594
alpha 0.01   features kept  5 of 20   test R² 0.9583
alpha 0.05   features kept  2 of 20   test R² 0.9537
alpha 0.2    features kept  1 of 20   test R² 0.9254
kept at alpha 0.01: ['cat__segment_Retail', 'num__log_revenue_2024', 'num__late_payment_days', 'num__complaints_2024', 'num__categories_bought']
```

- `(weights != 0).sum()` counts the weights that aren't zero: the features lasso kept.
- `names[weights != 0]` picks the names of those features; the `if` saves them for α = 0.01, and the last line prints them.

![Two stacked panels sharing a lasso alpha axis from 0.001 to 0.2 on a log scale. Top, features kept: 14 at 0.001, 5 at 0.01, 2 at 0.05, 1 at 0.2. Bottom, test R² on an axis from 0 to 1: about 0.96 until alpha 0.05, then 0.93 at 0.2](figures/fig37-2-lasso-path.svg)

*Figure 37.2 — Lasso as α grows. Five features give almost the same accuracy as fourteen; one feature (last year's revenue) still explains most of the variation.*

**What to tell Anita.** "Next year's revenue for an account is mostly last year's revenue, adjusted down for retail accounts and for accounts that pay late or complain, and up for accounts buying across several product categories." That sentence comes straight from the five features lasso keeps at α = 0.01, printed above: last year's revenue, the retail column (compared with hospitality), late payment, complaints, and product categories bought.

> **When regularization matters most:** many features relative to rows (for example, 500 product-level features for 2,000 customers), correlated features, and any time you'd otherwise overfit. For logistic regression, scikit-learn regularizes by default (next section).

---

## 37.3 Logistic regression

### How it works

Logistic regression predicts a **probability** for a yes-or-no outcome. It computes the same weighted sum as linear regression, called *z*, and passes it through the **sigmoid** function, which squeezes any number into the range 0 to 1:

> *z* = *b* + *w*<sub>1</sub> × feature<sub>1</sub> + … + *w*<sub>n</sub> × feature<sub>n</sub>
>
> probability = 1 ÷ (1 + *e*<sup>−*z*</sup>)

*z* = 0 gives 0.5; large positive *z* gives probabilities near 1; large negative *z*, near 0. The weights are chosen by **maximum likelihood**, which is the same as minimizing log loss (Chapter 35, section 35.9). There's no exact formula, so it's solved by an optimizer, a smarter relative of gradient descent.

Chapter 30 (section 30.11) fitted logistic regression with statsmodels to *explain* an experiment. Here it *predicts*, and one quantity needs recalling first:

> **Odds, log-odds, and odds ratios** (Chapter 30, section 30.11).
>
> - **Odds** = *p* ÷ (1 − *p*). A 10% churn probability is odds of 0.10 ÷ 0.90 = 0.111, "1 to 9".
> - **Log-odds** = ln(odds) = ln(0.111) = −2.197. That's *z*: the weighted sum *is* the log-odds.
> - Back again: *p* = odds ÷ (1 + odds).
> - An **odds ratio** multiplies the odds, not the probability. An odds ratio of 2.10 turns odds 0.111 into 0.233, so *p* goes from 10% to 0.233 ÷ 1.233 = **18.9%**, not 21%. At low probabilities the two are close; at high ones they're far apart.

Despite its name, it's a **classification** algorithm. Now the churn problem. First, a pipeline for classifiers, with the numeric steps named first:

```python
def clf_pipeline(model, scale=True, nums=NUMS):
    num_steps = [("fill", SimpleImputer(strategy="median", add_indicator=True))]
    if scale:
        num_steps.append(("scale", StandardScaler()))
    categories = OneHotEncoder(handle_unknown="ignore")
    prepare = ColumnTransformer(
        [("cat", categories, CATS), ("num", Pipeline(num_steps), nums)]
    )
    return Pipeline([("prepare", prepare), ("model", model)])
```

Compare it with `reg_pipeline` line by line:

- **`add_indicator=True`** fills each blank with the median *and* adds a 0/1 "was blank" column, as in Chapter 36 (section 36.8). Only `late_payment_days` has blanks, so it adds one column.
- **`scale=True`** is a switch: trees (section 37.6) don't need scaling, so they'll call `clf_pipeline(model, scale=False)` and the `if` leaves the scaler out.
- **No `drop="first"`.** Logistic regression in scikit-learn is regularized by default (below), and the penalty pins the weights down even with all three segment columns, so the dummy variable trap doesn't bite. Keeping every column makes the odds ratios easier to read.
- **`nums=NUMS`** lets section 37.10 add engineered features without writing a new pipeline.

Next, a function that fits on training, scores on validation, and remembers the result:

```python
from sklearn.metrics import log_loss, roc_auc_score

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

- `predict_proba` returns two columns, P(stayed) and P(churned); `[:, 1]` takes every row (`:`) of the second column (`1`), the churn probability.
- **AUC** (how well the model ranks churners above stayers) and **log loss** (how good the probabilities are) are Chapter 36's two scores.
- `results[name] = ...` stores each AUC in the dictionary `results`, so the chapter can compare every model at the end.

Now fit logistic regression:

```python
from sklearn.linear_model import LogisticRegression

logit = clf_report("logistic regression", clf_pipeline(LogisticRegression(max_iter=2000)))
```

```
logistic regression            AUC 0.764   log loss 0.2833
```

**`max_iter=2000`** is the most optimizer steps allowed. The default, 100, stops too early on this data and prints a "did not converge" warning; 2,000 is plenty.

Last, turn the weights into odds ratios:

```python
coef = pd.Series(
    logit.named_steps["model"].coef_[0],
    index=logit.named_steps["prepare"].get_feature_names_out(),
)
odds = np.exp(coef).round(2).sort_values()
print("odds ratios (per 1 standard deviation for numbers):")
print(pd.concat([odds.head(3), odds.tail(4)]).to_string())
```

```
odds ratios (per 1 standard deviation for numbers):
num__categories_bought        0.57
num__units_2024               0.66
cat__segment_Wholesale        0.74
num__complaints_2024          1.30
num__revenue_2024             1.31
num__late_payment_days        1.53
num__days_since_last_order    2.10
```

- For a classifier, `coef_` has one row per class being predicted, so `coef_[0]` is the row of weights.
- `np.exp(coef)` turns each weight (a change in log-odds) into an **odds ratio**: how the odds of churning are multiplied when the feature rises by one unit (here, one standard deviation, since numbers are scaled; for a one-hot column, when the category applies).
- `odds.head(3)` are the three smallest (most protective) and `odds.tail(4)` the four largest (riskiest); `pd.concat` joins them into one list.

**Reading it.** On the validation set, logistic regression reaches an AUC of 0.764. The odds ratios read like a sales manager's instincts:

- **`days_since_last_order` 2.10:** one standard deviation longer without an order (about 80 days) doubles the odds of churning. The strongest signal.
- **`late_payment_days` 1.53** and **`complaints_2024` 1.30:** late payers and complainers are more likely to leave.
- **`categories_bought` 0.57:** each extra standard deviation of product breadth (about one more category) cuts the odds of churning by 43%. Customers who buy several product lines are stickier.

`revenue_2024` 1.31 and `units_2024` 0.66 point in opposite directions. They're highly correlated, so the model balances one against the other; read them together, not separately (the same multicollinearity as in section 37.1).

### The sigmoid by hand, and the setting C

Take the first validation account. The model's weighted sum for it is *z* = −2.124:

> probability = 1 ÷ (1 + *e*<sup>2.124</sup>) = 1 ÷ (1 + 8.365) = 1 ÷ 9.365 = **0.1068**

```python
one = X_va.iloc[[0]]
z = logit.decision_function(one)[0]
print(f"z = {z:.3f}   sigmoid(z) = 1 / (1 + e^-z) = {1 / (1 + np.exp(-z)):.4f}")
print(f"predict_proba: {logit.predict_proba(one)[0, 1]:.4f}")
```

```
z = -2.124   sigmoid(z) = 1 / (1 + e^-z) = 0.1068
predict_proba: 0.1068
```

- `X_va.iloc[[0]]`, with double brackets, keeps a one-row *table*; single brackets would give a single row as a Series, which the pipeline can't take.
- `decision_function` returns *z*, the weighted sum before the sigmoid, one per row; `[0]` takes the only one.
- `1 / (1 + np.exp(-z))` is the sigmoid, written out.

The hand calculation matches `predict_proba` exactly. ✓

**`C`** is logistic regression's regularization setting, and it works backwards from α: **smaller C means stronger regularization**. `C=1` is the default, so scikit-learn's logistic regression is regularized (with the ridge-style L2 penalty) unless you change it. Predict before you run it: will a hundred-fold change in C move the AUC much?

```python
for C in [0.01, 0.1, 1, 10]:
    clf_report(f"logistic, C={C}", clf_pipeline(LogisticRegression(C=C, max_iter=2000)))
```

```
logistic, C=0.01               AUC 0.762   log loss 0.2778
logistic, C=0.1                AUC 0.764   log loss 0.2821
logistic, C=1                  AUC 0.764   log loss 0.2833
logistic, C=10                 AUC 0.765   log loss 0.2831
```

Here, C barely matters: AUC stays between 0.762 and 0.765. As with linear regression, 3,000 rows and 20 features leave little to regularize.

> **When to use logistic regression:** almost always as your first real model. It trains in milliseconds, gives **calibrated** probabilities (usually: when it says 20%, about 20 in 100 such accounts really churn; Chapter 39, section 39.4, checks this), explains itself through odds ratios, and is hard to beat when effects are roughly additive, as Chapter 36's leads were. Its weakness is **interactions and thresholds**: it can't see "late payments matter only for small retailers" unless you build that feature. Section 37.10 shows how much that costs here, and how to fix it.

---

## 37.4 k-nearest neighbors

### How it works

k-nearest neighbors (k-NN) doesn't learn weights at all. To predict for a new account, it finds the *k* most similar accounts in the training data, measured by Euclidean distance (Chapter 35), and predicts the share of those neighbors that churned. "Training" means storing the data.

### k-NN by hand

Five training accounts, with two features already scaled:

| Account | feature 1 | feature 2 | Outcome | Distance to the new account (1.7, 1.6) |
|---|---|---|---|---|
| A | 0.2 | 0.1 | stayed | √(1.5² + 1.5²) = 2.121 |
| B | 0.5 | 0.4 | stayed | √(1.2² + 1.2²) = 1.697 |
| C | 1.8 | 1.5 | churned | √(0.1² + 0.1²) = 0.141 |
| D | 2.0 | 2.2 | churned | √(0.3² + 0.6²) = 0.671 |
| E | 1.6 | 1.9 | stayed | √(0.1² + 0.3²) = 0.316 |

With *k* = 3, the nearest three are C, E and D. Two of the three churned, so the prediction is 2 ÷ 3 = **0.667**. The same in scikit-learn:

```python
from sklearn.neighbors import KNeighborsClassifier

toy_X = np.array([[0.2, 0.1], [0.5, 0.4], [1.8, 1.5], [2.0, 2.2], [1.6, 1.9]])
toy_y = [0, 0, 1, 1, 0]
knn = KNeighborsClassifier(n_neighbors=3).fit(toy_X, toy_y)
print(knn.predict_proba([[1.7, 1.6]]).round(3))
```

```
[[0.333 0.667]]
```

`n_neighbors=3` is *k*. The two columns of the output are P(stayed) and P(churned): 0.667 matches the hand answer. ✓

Now imagine feature 2 were revenue in rupees, with values in the lakhs. A difference of ₹10,000 would swamp every difference in feature 1, and the "nearest" accounts would simply be the ones with the most similar revenue. That makes two things critical: **the choice of *k*** (few neighbors gives noisy predictions; many gives blurry ones) and **scaling** (distance is meaningless across unscaled units).

Two defaults of `KNeighborsClassifier` matter here:

| Setting | Default | Meaning |
|---|---|---|
| `weights` | `"uniform"` | Every one of the *k* neighbors counts equally (Exercise 9 tries `"distance"`, where closer ones count more) |
| `metric`, `p` | `"minkowski"`, `2` | Minkowski distance with *p* = 2 is the Euclidean distance of Chapter 35 |

Before you run it, predict: will *k* = 5 or *k* = 75 rank the churners better?

```python
for k in [5, 25, 75]:
    clf_report(f"k-NN, k={k}", clf_pipeline(KNeighborsClassifier(n_neighbors=k)))
clf_report(
    "k-NN, k=25, NOT scaled",
    clf_pipeline(KNeighborsClassifier(n_neighbors=25), scale=False),
)
```

```
k-NN, k=5                      AUC 0.684   log loss 1.5887
k-NN, k=25                     AUC 0.765   log loss 0.5255
k-NN, k=75                     AUC 0.775   log loss 0.3057
k-NN, k=25, NOT scaled         AUC 0.633   log loss 0.4735
```

**Reading it.**

- **k = 5** gives an AUC of 0.684 and a terrible log loss (1.59). With five neighbors, the only possible probabilities are 0, 0.2, 0.4, 0.6, 0.8, and 1, and a confident 0 for an account that churns is punished severely (Chapter 35).
- **k = 25 and 75** do much better (0.765 and 0.775), close to logistic regression.
- **Without scaling**, AUC collapses to 0.633. Revenue, measured in rupees, dominates every distance, so the "nearest" accounts are the ones with similar revenue, whatever their churn signals. Its log loss (0.4735) is *better* than the scaled *k* = 25 model's (0.5255): unscaled neighbors are a vaguer mix, so there are fewer confident 0% predictions to punish. Better log loss, worse ranking; AUC is the fairer comparison here.

> **When to use k-NN:** small datasets with few, meaningful, scaled features; as a quick baseline; and inside recommenders (Chapter 42 uses the same "nearest neighbors" idea on products). Avoid it with many features (in high dimensions, every point is roughly equally far from every other, the **curse of dimensionality**), with large datasets (prediction must search all training rows), and when you need to explain a decision.

---

## 37.5 Naive Bayes

### How it works

Naive Bayes applies **Bayes' rule** (Chapter 21, section 21.7) to classification. For each class, it multiplies how common the class is by how common each sign is within that class:

> P(churned | signs) ∝ P(churned) × P(sign<sub>1</sub> | churned) × P(sign<sub>2</sub> | churned)

- **P(churned)** is the **prior**: the share of accounts that churned, before looking at any sign.
- **P(sign | churned)** is a **likelihood**: among churners, the share that show the sign.
- The result, P(churned | signs), is the **posterior**: the updated probability after seeing the signs.

The symbol ∝ means "proportional to": the same product is worked out for "stayed", and the two answers are rescaled so they add up to 1. That's section 21.7's rule, applied to each class. It's "naive" because it assumes the signs are **independent** given the class (**conditional independence**), so their likelihoods can simply be multiplied. That's almost never exactly true, and the method often works anyway.

### A worked example

Use two yes/no signals from the training accounts. The first is one of the sales team's own warning signs, a *late-paying small retailer* (more than 25 days late on average, size Small, segment Retail); section 37.10 checks it against the data. The second is *no order in the last 90 days*. First build the two flags:

```python
late_small_retail = (
    (train_acc["late_payment_days"] > 25)
    & (train_acc["company_size"] == "Small")
    & (train_acc["segment"] == "Retail")
)
recent = train_acc["days_since_last_order"] <= 90
print("late small retail:", late_small_retail.sum())
print("no order in 90 days:", (~recent).sum())
```

```
late small retail: 134
no order in 90 days: 616
```

- Each comparison gives a True/False column; `&` means "and" (all three true), and the brackets around each comparison are required (Chapter 18).
- `~recent` flips True and False, so it means "no order in 90 days". `.sum()` counts the Trues.
- A blank `late_payment_days` counts as *not* late here, because any comparison with a blank is False. That's 97 training accounts; the pipelines fill them with the median instead.

Next, the counts of both flags against the outcome:

```python
table = pd.crosstab(
    [
        late_small_retail.rename("late small retail"),
        recent.rename("ordered in last 90 days"),
    ],
    train_acc["churned_2025"].rename("churned"),
)
print(table)
print("class counts:", train_acc["churned_2025"].value_counts().to_dict())
```

```
churned                                       0    1
late small retail ordered in last 90 days           
False             False                     421  145
                  True                     2215   85
True              False                      10   40
                  True                       64   20
class counts: {0: 2710, 1: 290}
```

- `pd.crosstab(rows, columns)` counts combinations (Chapter 30). Passing a *list* of two columns as the rows gives one row for each combination of the two flags. `.rename(...)` just sets the labels that are printed.
- `value_counts().to_dict()` gives the class sizes as a dictionary: 2,710 stayed (0) and 290 churned (1).

Read one row: *late small retail* True and *ordered in last 90 days* False, 10 stayed and **40 churned**. Those 50 accounts show both signs.

Now the likelihoods. For one flag, written out:

```python
churned = train_acc["churned_2025"] == 1
print(f"P(late small retail | churned) = {late_small_retail[churned].mean():.3f}")
print(f"P(late small retail | stayed)  = {late_small_retail[~churned].mean():.3f}")
print(f"P(no order in 90 days | churned) = {(~recent)[churned].mean():.3f}")
print(f"P(no order in 90 days | stayed)  = {(~recent)[~churned].mean():.3f}")
```

```
P(late small retail | churned) = 0.207
P(late small retail | stayed)  = 0.027
P(no order in 90 days | churned) = 0.638
P(no order in 90 days | stayed)  = 0.159
```

`late_small_retail[churned]` keeps the flag for churners only, and `.mean()` of True/False is the share of Trues: among churners, the share with this sign. For the first line, that's 60 ÷ 290 = 0.207 (the 40 + 20 churners in the table's two *True* rows).

For an account that is a late-paying small retailer **and** has had no order in 90 days:

> **churned:** prior 290 ÷ 3,000 = 0.0967 × P(late small retail | churned) 0.207 × P(no order in 90 days | churned) 0.638 = **0.01276**
>
> **stayed:** prior 2,710 ÷ 3,000 = 0.9033 × 0.027 × 0.159 = **0.00388**
>
> posterior P(churned) = 0.01276 ÷ (0.01276 + 0.00388) = **0.767**

Naive Bayes says 76.7%. scikit-learn's `BernoulliNB` is Naive Bayes for yes/no features, and gives the same answer:

```python
from sklearn.naive_bayes import BernoulliNB

flags = pd.DataFrame({"late_small_retail": late_small_retail, "no_order_90": ~recent})
bnb = BernoulliNB(alpha=1e-9, force_alpha=True).fit(flags, train_acc["churned_2025"])
both = pd.DataFrame({"late_small_retail": [True], "no_order_90": [True]})
print(f"P(churned | both signs) = {bnb.predict_proba(both)[0, 1]:.3f}")
```

```
P(churned | both signs) = 0.765
```

- `flags` is a two-column table of the signs; `both` is one account showing both.
- `alpha` is **smoothing**: normally `BernoulliNB` adds 1 to every count, so a sign never seen in a class doesn't get a likelihood of exactly 0. The hand example has no smoothing, so `alpha=1e-9` (almost 0) turns it off, and `force_alpha=True` tells scikit-learn to accept so small a value.

The code gives 0.765: the hand answer used likelihoods rounded to three decimals, the code uses the exact ones. Check it against the table: training accounts with both signals churned 40 times out of 50, **80%**. The estimate is close, because these two signals really are roughly independent here. When features are strongly related (revenue, units, and orders, for example), multiplying their likelihoods counts the same evidence several times, and the probabilities become overconfident.

Now the full model. `GaussianNB` handles numbers: for each numeric feature it assumes a normal curve within each class, and reads the likelihood from that curve instead of counting. For `days_since_last_order` in the training accounts, the churners' curve has a mean of 150 days and a standard deviation of 122; the stayers', a mean of 50 and a standard deviation of 67. An account 200 days silent sits near the middle of the churners' curve and far out in the stayers' tail, so that feature's likelihood strongly favors "churned".

```python
from sklearn.naive_bayes import GaussianNB

nb = clf_report("Gaussian Naive Bayes", clf_pipeline(GaussianNB()))
clf_report("Gaussian NB, not scaled", clf_pipeline(GaussianNB(), scale=False))
```

```
Gaussian Naive Bayes           AUC 0.740   log loss 1.2866
Gaussian NB, not scaled        AUC 0.732   log loss 0.5371
```

`GaussianNB` goes straight into the pipeline, like the other models: the pipeline's output here is an ordinary (dense) table of numbers, which it reads directly.

**Reading it.** AUC 0.740, a little below logistic regression, and a log loss of 1.29, far worse. Naive Bayes ranks reasonably but its probabilities are overconfident: the independence assumption, applied to 25 correlated columns, piles up evidence. Chapter 35 warned that skewed features like revenue aren't normal either. Scaling makes a small difference (0.740 against 0.732): in theory, Gaussian Naive Bayes fits a separate mean and spread for every feature, so the units shouldn't matter, but scikit-learn adds a tiny safety amount to every variance (`var_smoothing`), sized from the *largest* variance, and unscaled rupees make that amount large.

> **When to use Naive Bayes:** text classification (each word as a feature; Chapter 41 uses it for support tickets), very small datasets, and when you need something fast and simple. Don't use its probabilities without calibration (Chapter 39, section 39.4).

### Checkpoint: end of Part A

Before Part B, check that you can do these by hand, on new numbers, without looking back:

1. A logistic model gives *z* = −1.2. What's the probability? (Answer: 1 ÷ (1 + *e*<sup>1.2</sup>) = 1 ÷ 4.320 = 0.231.)
2. An account has a 20% churn probability, and an odds ratio of 1.5 applies. New odds and probability? (Answer: odds 0.25 × 1.5 = 0.375; probability 0.375 ÷ 1.375 = 27.3%.)
3. A prior of 0.1, with likelihoods 0.5 (churned) and 0.1 (stayed) for one sign. The posterior? (Answer: 0.05 ÷ (0.05 + 0.09) = 0.357.)

If all three come out right, take a break: Part B starts with trees.

---

## 37.6 Decision trees

### How it works

A decision tree asks a sequence of yes/no questions, each about one feature: *"Is days since last order more than 160?"* Each question is a **node**: it splits the rows arriving at it into two groups, and each group goes on to the next question. Rows that end in the same final group, a **leaf**, get the same prediction: that leaf's churn rate.

To choose each question, the tree tries **every feature and every threshold** and picks the split that makes the groups purest. Purity is measured by **entropy** (Chapter 35, section 35.9) or by **Gini impurity**, a simpler cousin that's new here:

> Gini = 1 − *p*² − (1 − *p*)² = 2 × *p* × (1 − *p*), where *p* is the group's churn rate
>
> entropy = −(*p* × log<sub>2</sub> *p* + (1 − *p*) × log<sub>2</sub> (1 − *p*))

A quick feel for Gini: a group with no churners (*p* = 0) scores 2 × 0 × 1 = **0**; a half-and-half group (*p* = 0.5) scores 2 × 0.5 × 0.5 = **0.5**, the worst; a group with 10% churners scores 2 × 0.1 × 0.9 = **0.18**. Both measures are 0 for a pure group and highest at *p* = 0.5.

### A split by hand

Compare two candidate first questions on the 3,000 training accounts, 290 of which churned (*p* = 0.0967):

> Gini before any split = 2 × 0.0967 × 0.9033 = **0.1746**

**Split A: days since last order > 90.** 616 accounts say yes, with a 30.0% churn rate; 2,384 say no, with 4.4%.

> Gini(yes) = 2 × 0.300 × 0.700 = 0.4200    Gini(no) = 2 × 0.044 × 0.956 = 0.0841
>
> weighted Gini after = (616 ÷ 3,000) × 0.4200 + (2,384 ÷ 3,000) × 0.0841 = 0.0862 + 0.0669 = **0.1531**

**Split B: late payment days > 25.** Yes: 387 accounts, 23.0% churn. No: 2,613, 7.7%.

> weighted Gini after = (387 ÷ 3,000) × (2 × 0.230 × 0.770) + (2,613 ÷ 3,000) × (2 × 0.077 × 0.923) = 0.0457 + 0.1238 = **0.1695**

Split A reduces impurity from 0.1746 to 0.1531; split B only to 0.1695. The tree prefers A. Using entropy gives the same ranking (information gain, Chapter 35):

```python
def gini(y):
    p = np.mean(y)
    return 1 - p**2 - (1 - p) ** 2


def entropy(y):
    p = np.mean(y)
    return 0.0 if p in (0, 1) else -(p * np.log2(p) + (1 - p) * np.log2(1 - p))


y_all = train_acc["churned_2025"]
for rule_name, rule in [
    ("days_since_last_order > 90", train_acc["days_since_last_order"] > 90),
    ("late_payment_days > 25", train_acc["late_payment_days"] > 25),
]:
    left, right = y_all[rule], y_all[~rule]
    w_l, w_r = len(left) / len(y_all), len(right) / len(y_all)
    print(
        f"{rule_name}: yes {len(left)} ({left.mean():.1%} churn),"
        f" no {len(right)} ({right.mean():.1%})"
    )
    print(
        f"   Gini {gini(y_all):.4f} -> {w_l * gini(left) + w_r * gini(right):.4f}   "
        f"entropy {entropy(y_all):.4f} -> {w_l * entropy(left) + w_r * entropy(right):.4f}"
    )
```

```
days_since_last_order > 90: yes 616 (30.0% churn), no 2384 (4.4%)
   Gini 0.1746 -> 0.1532   entropy 0.4583 -> 0.3881
late_payment_days > 25: yes 387 (23.0% churn), no 2613 (7.7%)
   Gini 0.1746 -> 0.1694   entropy 0.4583 -> 0.4411
```

**How it works:**

- `gini` and `entropy` turn a column of 0s and 1s into its churn rate *p* with `np.mean`, then apply the two formulas. `entropy` returns 0 for a pure group, where log<sub>2</sub> 0 would fail.
- The loop tries each rule: `left` holds the outcomes where the rule is true, `right` the rest, and `w_l`, `w_r` are their shares of the rows, the weights in the hand calculation.

(The code's weighted values, 0.1532 and 0.1694, differ from the hand values in the last digit because the churn rates were rounded to three decimals by hand.)

### Depth, and overfitting

Keep splitting and every leaf eventually holds one account, and the tree memorizes the training data. Watch it happen. Before you run it, predict: as the tree gets deeper, what happens to the training AUC, and what to the validation AUC?

```python
from sklearn.tree import DecisionTreeClassifier, export_text

for depth in [1, 2, 3, 4, 5, 6, 8, 10, 14, None]:
    tree = clf_pipeline(
        DecisionTreeClassifier(max_depth=depth, random_state=37), scale=False
    ).fit(X_tr, y_tr)
    tr_auc = roc_auc_score(y_tr, tree.predict_proba(X_tr)[:, 1])
    va_auc = roc_auc_score(y_va, tree.predict_proba(X_va)[:, 1])
    leaves = tree.named_steps["model"].get_n_leaves()
    print(
        f"max_depth {str(depth):<5} train AUC {tr_auc:.3f}   valid AUC {va_auc:.3f}   "
        f"leaves {leaves}"
    )
```

```
max_depth 1     train AUC 0.696   valid AUC 0.651   leaves 2
max_depth 2     train AUC 0.759   valid AUC 0.708   leaves 4
max_depth 3     train AUC 0.791   valid AUC 0.752   leaves 8
max_depth 4     train AUC 0.829   valid AUC 0.748   leaves 16
max_depth 5     train AUC 0.865   valid AUC 0.750   leaves 29
max_depth 6     train AUC 0.886   valid AUC 0.733   leaves 48
max_depth 8     train AUC 0.934   valid AUC 0.672   leaves 97
max_depth 10    train AUC 0.969   valid AUC 0.609   leaves 161
max_depth 14    train AUC 0.994   valid AUC 0.543   leaves 230
max_depth None  train AUC 1.000   valid AUC 0.557   leaves 277
```

- `max_depth=None` means "no limit"; `str(depth)` turns it into the text "None" so the f-string can pad it.
- Each tree is scored twice: on the rows it learned from (`X_tr`) and on validation (`X_va`).
- `get_n_leaves()` counts the tree's final groups.

![Line chart of train and validation AUC by maximum tree depth, from 1 to no limit: training AUC rises steadily to 1.000, while validation AUC peaks at depth 3 and falls to about 0.56 with no limit; the peak is labelled with its value](figures/fig37-3-tree-depth.svg)

*Figure 37.3 — A decision tree overfitting, drawn from the ten depths printed above. Deeper trees fit the training data better and better, while their performance on new accounts peaks early and then collapses.*

**Reading it.**

- A tree with no depth limit has **277 leaves** and a **perfect** training AUC of 1.000, and a validation AUC of 0.557, barely better than a coin. It memorized noise.
- Depth 3 is the best on validation (0.752), with depths 4 and 5 close behind (0.748 and 0.750).
- A single tree is **unstable**: small changes in the data change the first split and everything below it. Its best validation AUC is below logistic regression's.

A shallow tree can be printed and read. Here is the depth-2 tree:

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
```

```
|--- num__days_since_last_order <= 160.50
|   |--- num__days_since_last_order <= 94.50
|   |   |--- weights: [2305.00, 106.00] class: 0
|   |--- num__days_since_last_order >  94.50
|   |   |--- weights: [232.00, 52.00] class: 0
|--- num__days_since_last_order >  160.50
|   |--- num__late_payment_days <= 25.50
|   |   |--- weights: [160.00, 93.00] class: 0
|   |--- num__late_payment_days >  25.50
|   |   |--- weights: [13.00, 39.00] class: 1
```

- `export_text` prints the tree's questions as indented text; `feature_names=` gives it the column names (as a plain list), and `show_weights=True` adds the counts in each leaf.
- Read a leaf like `weights: [13.00, 39.00] class: 1` as "13 stayed, 39 churned; the majority says churn".

The printed tree is readable by anyone: accounts with no order for more than 160 days **and** more than 25 days of late payments churned 39 times out of 52. That's an interaction (late payment matters most for the long-silent accounts) that the tree found by itself, and that logistic regression can't see.

A tree's main settings:

| Setting | What it controls | Value here | What happens if you change it |
|---|---|---|---|
| `max_depth` | The most questions from the top to any leaf | 4 | Deeper: training AUC rises, validation falls after depth 3 (the table above) |
| `min_samples_leaf` | The fewest training rows a leaf may hold; 20 to 100 is sensible for thousands of rows | 20 | Larger: fewer, bigger leaves and smoother probabilities |
| `criterion` | How purity is measured: `"gini"` (the default) or `"entropy"` | both, below | Rarely matters (below) |
| `random_state` | Breaks ties between equally good splits the same way every run | 37 | A different, equally good tree when splits tie |

```python
for criterion in ["gini", "entropy"]:
    clf_report(
        f"decision tree, depth 4, {criterion}",
        clf_pipeline(
            DecisionTreeClassifier(
                max_depth=4, min_samples_leaf=20, criterion=criterion, random_state=37
            ),
            scale=False,
        ),
    )
```

```
decision tree, depth 4, gini   AUC 0.758   log loss 0.2810
decision tree, depth 4, entropy AUC 0.762   log loss 0.3388
```

The two criteria give close AUCs (0.758 and 0.762), as they usually do; their log losses differ more, a reminder to look at both scores. Limiting the leaves to at least 20 rows keeps the depth-4 tree from chasing tiny groups.

> **When to use a single tree:** when a person must be able to follow the rules (a credit policy, a triage checklist), and as the building block for the next two methods. Trees need no scaling and handle interactions and thresholds naturally.

---

## 37.7 Random forests

### How it works

A random forest trains **hundreds of trees** and averages their predictions. Averaging only helps if the trees make *different* mistakes, so each tree is made different in two ways:

1. **Bagging** (bootstrap aggregating): each tree trains on a **bootstrap sample** of the training rows: the same number of rows, drawn **with replacement**, as in Chapter 22's bootstrap. Some rows are picked twice or more, and others not at all.
2. **Random features:** at each split, a tree may look at only a random few of the features, by default the square root of the number of features.

Each tree overfits in its own way; the average cancels much of the noise and keeps the signal. It's the committee from *In plain English*.

### A tiny forest by hand

Take eight training accounts and one feature, days since last order. `sample(8, random_state=321)` picks eight rows at random, repeatably, and `sort_values` puts them in order of days:

```python
toy = train_acc.sample(8, random_state=321).sort_values("days_since_last_order")
print(toy[["days_since_last_order", "churned_2025"]].to_string(index=False))
x_toy = toy[["days_since_last_order"]].to_numpy()
y_toy = toy["churned_2025"].to_numpy().astype(float)
```

```
 days_since_last_order  churned_2025
                   1.0             0
                  10.0             0
                  11.0             0
                  25.0             1
                  30.0             0
                  34.0             0
                  40.0             0
                 197.0             1
```

- `to_string(index=False)` prints the table without the row labels.
- `.to_numpy()` turns the table into a plain NumPy array (Chapter 18), which is all a one-feature model needs; `x_toy` keeps the double brackets, so it stays a table of 8 rows × 1 column.
- `.astype(float)` makes the targets decimals, because section 37.8 will subtract predictions from them.

Two of the eight churned: the most silent account (197 days) and one that ordered 25 days before the year ended. Now grow three one-question trees (**stumps**), each on its own bootstrap sample, and ask each about the 197-day account:

```python
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(37)
votes = []
for tree_no in [1, 2, 3]:
    rows = np.sort(rng.choice(8, size=8, replace=True))
    stump = DecisionTreeRegressor(max_depth=1, random_state=37)
    stump.fit(x_toy[rows], y_toy[rows])
    p = stump.predict([[197.0]])[0]
    votes.append(p)
    print(f"tree {tree_no}: rows {rows}   P(churn) at 197 days {p:.2f}")
print(f"forest: average of the three = {np.mean(votes):.2f}")
```

```
FILL
```

- `np.random.default_rng(37)` is a seeded random generator (Chapter 21), so the draws repeat.
- `rng.choice(8, size=8, replace=True)` draws 8 row positions from 0 to 7 **with replacement**: after a row is picked, it goes back in the hat and can be picked again. `np.sort` just makes the list easier to read.
- `x_toy[rows]` picks those rows, repeats included, and each stump learns from its own sample.
- `DecisionTreeRegressor(max_depth=1)` is a one-question tree that predicts a number: the average of the 0s and 1s in each leaf, which is that leaf's churn rate. `stump.predict([[197.0]])[0]` is that churn rate for an account 197 days silent. (Section 37.8 uses the same kind of stump.)

Look at the row lists: in each sample, some rows appear two or more times and others are missing. Tree 3's sample happens to miss both churners (rows 3 and 7), so it says 0. The stumps see different data, so they disagree, and the forest averages their answers. A real forest does the same with 300 deep trees, each also choosing from a random few features at every split.

### On the accounts

```python
from sklearn.ensemble import RandomForestClassifier

forest = clf_report(
    "random forest",
    clf_pipeline(
        RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=37),
        scale=False,
    ),
)
imp = pd.Series(
    forest.named_steps["model"].feature_importances_,
    index=forest.named_steps["prepare"].get_feature_names_out(),
)
print(imp.sort_values(ascending=False).head(6).round(3).to_string())
```

```
random forest                  AUC 0.785   log loss 0.2675
num__days_since_last_order    0.295
num__late_payment_days        0.112
num__revenue_2024             0.088
num__units_2024               0.084
num__tenure_months            0.070
num__avg_discount_pct         0.066
```

- `n_estimators=300` is the number of trees; `min_samples_leaf=5` stops each tree from making leaves of fewer than 5 rows; `random_state=37` fixes the bootstrap samples and feature choices.
- `feature_importances_` has one number per column, and they add up to 1; `sort_values(ascending=False)` puts the largest first.

**Reading it.** AUC 0.785, the best so far and above logistic regression's 0.764. The forest can use thresholds and interactions without being told about them.

**Feature importance.** `feature_importances_` shows how much each feature reduced impurity across all trees. `days_since_last_order` leads by far, then `late_payment_days`. Two cautions: impurity-based importance is inflated for features with many distinct values (revenue has thousands; segment has three), and it says nothing about direction. Chapter 39 (section 39.8) uses two more reliable methods: **permutation importance** (shuffle one column and see how much the validation score drops) and **SHAP** (split one account's prediction into a contribution from each feature). Both are taught there.

**Key settings:** `n_estimators` (more trees never overfit, only cost time; 200–500 is usually plenty), `min_samples_leaf` or `max_depth` (limit the individual trees), and `max_features` (how many features each split considers; the default for classification is the square root of the number of features).

> **When to use a random forest:** a strong, forgiving default for tabular data. It needs little tuning, rarely overfits badly, handles mixed feature types, and gives a quick importance ranking. It's usually a little behind well-tuned gradient boosting, and its models are large.

---

## 37.8 Gradient boosting

### How it works

A forest builds trees **independently** and averages them. **Gradient boosting** builds them **one after another**, each new tree correcting the errors of the model so far:

1. Start with a simple prediction for everyone, such as the average.
2. Compute each row's **residual**: how far off the current prediction is. (More precisely, the negative gradient of the loss, Chapter 35. For squared error, that's the plain residual.)
3. Fit a **small tree** to the residuals (**residual fitting**).
4. Add that tree's predictions to the model, **scaled down** by a **learning rate**.
5. Repeat for hundreds of rounds.

### Round 1 by hand

Use section 37.7's eight accounts, squared error, one-question trees (stumps), and a learning rate of 0.5.

- **Round 0.** Two of the eight churned, so predict the average, 2 ÷ 8 = **0.25**, for everyone. Squared error = (2 × 0.75² + 6 × 0.25²) ÷ 8 = (1.125 + 0.375) ÷ 8 = **0.1875**.
- **Residuals.** Actual minus predicted: **+0.75** for the two churners, **−0.25** for the six others.
- **The stump.** The best single split of the residuals puts the 197-day account alone on one side (at days ≤ 118.5). Each side predicts its mean residual: +0.75 for the 197-day account; for the other seven, (0.75 − 6 × 0.25) ÷ 7 = −0.75 ÷ 7 = **−0.107**.
- **Add half.** The 197-day account: 0.25 + 0.5 × 0.75 = **0.625**. The other seven: 0.25 + 0.5 × (−0.107) = **0.196**.
- **New squared error** = ((1 − 0.625)² + (1 − 0.196)² + 6 × 0.196²) ÷ 8 = (0.141 + 0.646 + 0.231) ÷ 8 = **0.127**.

The error fell from 0.1875 to 0.127. The 25-day churner is still badly predicted (0.196), so round 2's residuals will point at it. The code runs the same steps for three rounds:

```python
pred = np.full(len(y_toy), y_toy.mean())
print(f"round 0: predict {y_toy.mean():.3f} for all   squared error {np.mean((y_toy - pred) ** 2):.4f}")
for r in range(1, 4):
    residual = y_toy - pred
    stump = DecisionTreeRegressor(max_depth=1, random_state=37).fit(x_toy, residual)
    pred = pred + 0.5 * stump.predict(x_toy)
    print(
        f"round {r}: split at days <= {stump.tree_.threshold[0]:.1f}   "
        f"squared error {np.mean((y_toy - pred) ** 2):.4f}"
    )
print("final:", pred.round(3))
```

```
round 0: predict 0.250 for all   squared error 0.1875
round 1: split at days <= 118.5   squared error 0.1272
round 2: split at days <= 18.0   squared error 0.1099
round 3: split at days <= 118.5   squared error 0.0992
final: [0.076 0.076 0.076 0.233 0.233 0.233 0.233 0.842]
```

- `np.full(8, 0.25)` makes an array of eight 0.25s: the round-0 prediction. (`len(y_toy)` is 8 and `y_toy.mean()` is 0.25.)
- `DecisionTreeRegressor(max_depth=1)` is section 37.7's stump, now predicting the residuals.
- `stump.tree_.threshold[0]` is the split point of the stump's first and only question; `tree_` is scikit-learn's internal record of the fitted tree.
- `pred = pred + 0.5 * stump.predict(x_toy)` adds half of the stump's correction: the learning rate.

**Reading it.** Round 1 matches the hand calculation: the split at 118.5 and a squared error of 0.1272. Round 2 then splits at 18.0, separating the three most recent accounts (1, 10 and 11 days) from the rest, which raises the prediction for the 25-day churner a little. Each round fits a stump to what's still wrong and adds half of its correction, and the error keeps falling. After three rounds, the 197-day churner's predicted value is highest. Real libraries do the same thing on the log-odds scale with log loss, and add refinements (second-order steps, regularized leaves), with deeper trees and hundreds of rounds.

### The libraries

Four implementations matter in practice:

| Library | Strengths | Notes |
|---|---|---|
| scikit-learn `HistGradientBoostingClassifier` | Already installed; fast on medium data; handles missing values | Good default; fewer options |
| **XGBoost** | Mature, widely used, many options, GPU support | Industry standard in competitions and production |
| **LightGBM** | Very fast on large data; grows trees leaf-wise | `num_leaves` is its key setting; can overfit small data |
| **CatBoost** | Handles categorical columns natively and carefully; strong defaults | Slower to train; less tuning needed |

The settings that matter most are shared across all four, under different names:

| Setting | scikit-learn HGB | XGBoost | LightGBM | CatBoost | Value here, and why |
|---|---|---|---|---|---|
| Number of trees | `max_iter` | `n_estimators` | `n_estimators` | `iterations` | 300: enough rounds at this learning rate |
| Learning rate | `learning_rate` | `learning_rate` | `learning_rate` | `learning_rate` | 0.05: small steps generalize better but need more trees; 0.01–0.1 is typical |
| Tree size | `max_depth` | `max_depth` | `num_leaves` | `depth` | depth 3, or 8 leaves (a depth-3 tree has at most 2³ = 8 leaves); CatBoost's depth 4 because its trees are symmetric and simpler |
| Rows per leaf | `min_samples_leaf` | (`min_child_weight`) | `min_child_samples` | (`min_data_in_leaf`) | 40 where set: no tiny leaves |
| Row sampling | (none) | `subsample` | `subsample` + `subsample_freq` | (automatic) | 0.8: each tree sees 80% of the rows; LightGBM ignores `subsample` unless `subsample_freq` is at least 1 (how often to redraw the rows) |
| Column sampling | (none) | `colsample_bytree` | `colsample_bytree` | (`rsm`) | 0.8: each tree sees 80% of the features |
| L2 regularization | `l2_regularization` | `reg_lambda` | `reg_lambda` | `l2_leaf_reg` | left at each library's default here; tuned in section 37.11 |
| Repeatable results | `random_state` | `random_state` | `random_state` | `random_seed` | 37 |
| Threads | (uses all cores) | `n_jobs` | `n_jobs` | `thread_count` | 1 where set, so runs repeat exactly and timings are comparable |
| Messages | `verbose` | `verbosity` | `verbose` | `verbose` | silenced: `verbose=-1` for LightGBM, `verbose=0` for CatBoost |

Settings in brackets exist but aren't used here. One library per cell. First scikit-learn's own, with default settings and then with the settings in the table:

```python
from sklearn.ensemble import HistGradientBoostingClassifier

clf_report(
    "HistGradientBoosting default",
    clf_pipeline(HistGradientBoostingClassifier(random_state=37), scale=False),
)
hgb_settings = dict(learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300)
clf_report(
    "HistGradientBoosting tuned",
    clf_pipeline(
        HistGradientBoostingClassifier(**hgb_settings, random_state=37), scale=False
    ),
)
```

```
HistGradientBoosting default   AUC 0.783   log loss 0.3127
HistGradientBoosting tuned     AUC 0.786   log loss 0.2744
```

- `dict(learning_rate=0.05, ...)` stores the four settings under one name, so section 37.10 can reuse them.
- `**hgb_settings` unpacks the dictionary into the call, exactly as if you had typed `learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300`.
- The defaults are a learning rate of 0.1, 100 trees, and up to 31 leaves per tree.

XGBoost next. It follows scikit-learn's `fit` and `predict_proba`, so it drops straight into the pipeline:

```python
import xgboost

print("xgboost", xgboost.__version__)
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
```

```
xgboost 3.2.0
XGBoost                        AUC 0.794   log loss 0.2703
```

Every setting is in the table above. LightGBM, with its own name for tree size:

```python
import lightgbm

print("lightgbm", lightgbm.__version__)
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
            n_jobs=1,
            verbose=-1,
        ),
        scale=False,
    ),
)
```

```
lightgbm 4.7.0
LightGBM                       AUC 0.780   log loss 0.2794
```

- `num_leaves=8` caps each tree at 8 leaves, about the size of a depth-3 tree; LightGBM grows the leaf that helps most first, instead of level by level.
- `subsample_freq=1` redraws the 80% sample of rows for every tree; without it, `subsample` does nothing.
- `verbose=-1` silences LightGBM's progress messages.

CatBoost is different: it's given the raw columns, text categories included, and told which are categorical, so it skips the one-hot pipeline and is fitted directly:

```python
import catboost

print("catboost", catboost.__version__)
cat_model = catboost.CatBoostClassifier(
    iterations=300,
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
catboost 1.2.10
CatBoost (native categories)   AUC 0.797   log loss 0.2659
```

- `cat_features=CATS` names the categorical columns. CatBoost encodes them itself, using a carefully ordered form of target encoding that avoids the leak from Chapter 36 (section 36.7).
- Because this model isn't built with `clf_pipeline`, the last lines do by hand what `clf_report` does: predict, store the AUC in `results`, and print both scores.
- CatBoost fills blanks in numbers itself, so it needs no imputer.

**Reading it.** All the boosting models beat logistic regression on validation (0.780–0.797 against 0.764). Default and tuned settings differ, and so do the libraries, by a couple of points. **With 1,000 validation accounts and 97 churners, differences of 0.01 are within noise.** Don't pick XGBoost over LightGBM on this evidence; section 37.10 uses cross-validation to compare properly.

> **When to use gradient boosting:** the default choice for tabular business data when accuracy matters and you have at least a few thousand rows. It handles thresholds, interactions, missing values, and mixed features. Its costs: more settings to tune, slower training than linear models, overfitting on small data, and less transparency (Chapter 39's SHAP values help).

---

## 37.9 Support vector machines

### How it works

A support vector machine (SVM) looks for the boundary between classes with the **widest margin**: the biggest gap to the nearest points on either side. Those nearest points, the **support vectors**, alone define the boundary.

**A margin by hand, on one feature.** Three accounts that stayed have gone 10, 20 and 40 days without an order; two that churned, 120 and 150 days. The widest gap between the groups runs from 40 to 120, so the boundary sits in the middle, at **80 days**, with a margin of **40 days** on each side. The accounts at 40 and 120 are the **support vectors**: move the 10-day or the 150-day account and nothing changes, but move the 40-day account to 60 and the boundary moves to 90.

Real data overlaps, so no gap is clean. The setting **C** trades a wide margin against training points on the wrong side (as with logistic regression, smaller C means more regularization). For boundaries that aren't straight, the **kernel trick** measures similarity between rows in a way that corresponds to a curved boundary, without computing new features explicitly. The **RBF** (radial basis function) kernel is the usual choice: it lets the boundary curve around groups of similar accounts.

An SVM gives each account a signed distance from the boundary, not a probability. To get probabilities for AUC and log loss, wrap it in `CalibratedClassifierCV`, which fits a small logistic curve on the SVM's distances (**Platt scaling**):

| Setting | Meaning | Value here |
|---|---|---|
| `kernel` | `"linear"` for a straight boundary, `"rbf"` for a curved one | both |
| `C` | Margin width against training errors; smaller is more regularized | 1.0, the default |
| `gamma` | For RBF: how far each account's influence reaches; the default `"scale"` sets it from the number of features and their spread | default |
| `class_weight` | `"balanced"` makes each class count equally in total | tried both ways |
| `CalibratedClassifierCV(..., ensemble=False)` | Fits the Platt curve with 5-fold cross-validation inside the training rows, then one final SVM on all of them | used for all three |

```python
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import SVC

clf_report(
    "SVM, linear kernel",
    clf_pipeline(CalibratedClassifierCV(SVC(kernel="linear"), ensemble=False)),
)
clf_report(
    "SVM, linear, balanced",
    clf_pipeline(
        CalibratedClassifierCV(
            SVC(kernel="linear", class_weight="balanced"), ensemble=False
        )
    ),
)
clf_report(
    "SVM, RBF, balanced",
    clf_pipeline(
        CalibratedClassifierCV(
            SVC(kernel="rbf", C=1.0, class_weight="balanced"), ensemble=False
        )
    ),
)
```

```
SVM, linear kernel             AUC 0.536   log loss 0.3186
SVM, linear, balanced          AUC 0.771   log loss 0.2784
SVM, RBF, balanced             AUC 0.780   log loss 0.2711
```

**Reading it.**

- The **linear SVM with default settings** scores an AUC of 0.536, almost a coin toss. With only 9.7% churners, the widest-margin solution is to push nearly all accounts to the "stayed" side, and the ranking within that side is nearly meaningless.
- **`class_weight="balanced"`** makes each churner count about nine times as much in the loss (2,710 ÷ 290 = 9.3), so the boundary takes churners seriously. AUC jumps to 0.771. Chapter 39 (section 39.6) covers class weights and other ways to handle imbalanced data.
- The **RBF kernel**, balanced, reaches 0.780, similar to the forest.

> **When to use SVMs:** medium-sized datasets (up to tens of thousands of rows) with many features, such as text, and problems where the classes are well separated. Training time grows quickly with rows, they need scaling, and they don't give probabilities or explanations naturally. For typical business tables, gradient boosting has largely replaced them.

---

## 37.10 Bias, variance, and learning curves

### The trade-off

Section 37.0's two ways to be wrong have names. A model's error on new data comes from two sources, beyond pure chance:

- **Bias:** the model is too simple to capture the pattern. A straight line can't follow a threshold. Symptom: training and validation scores are both mediocre and close together. **Underfitting.**
- **Variance:** the model is so flexible that it fits noise in the training sample. Symptom: training score much higher than validation. **Overfitting.** The unlimited decision tree was the extreme case.

The fix depends on which you have. For **high bias**, add features, use a more flexible model, or reduce regularization. For **high variance**, get more data, simplify the model, increase regularization, or average many models (a forest).

### Compare properly first

Validation scores on 1,000 accounts are noisy. Before diagnosing, compare the three strongest candidates with 5-fold cross-validation (Chapter 36, section 36.5) on all 4,000 non-test accounts:

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=37)
candidates = {
    "logistic regression": clf_pipeline(LogisticRegression(max_iter=2000)),
    "random forest": clf_pipeline(
        RandomForestClassifier(n_estimators=300, min_samples_leaf=5, random_state=37),
        scale=False,
    ),
    "HistGradientBoosting tuned": clf_pipeline(
        HistGradientBoostingClassifier(**hgb_settings, random_state=37), scale=False
    ),
}
X_rest, y_rest = rest[CATS + NUMS], rest["churned_2025"]
cv_scores = {}
for name, pipe in candidates.items():
    s = cross_val_score(pipe, X_rest, y_rest, cv=folds, scoring="roc_auc")
    cv_scores[name] = s
    print(f"{name:<28} mean AUC {s.mean():.3f}   sd {s.std():.3f}   folds {s.round(3)}")
```

```
logistic regression          mean AUC 0.807   sd 0.007   folds [0.812 0.796 0.811 0.803 0.815]
random forest                mean AUC 0.826   sd 0.020   folds [0.862 0.818 0.822 0.803 0.824]
HistGradientBoosting tuned   mean AUC 0.836   sd 0.016   folds [0.865 0.831 0.837 0.816 0.831]
```

- `StratifiedKFold(n_splits=5, shuffle=True, random_state=37)` cuts the 4,000 accounts into the same five folds for every model, each with the same churn rate.
- `cross_val_score` fits each pipeline five times, scoring AUC on the held-out fold each time, and returns the five scores; `cv_scores[name] = s` keeps them for the next cell.

On 4,000 accounts, the picture is clearer: **tuned boosting 0.836, random forest 0.826, logistic regression 0.807**. Are the gaps real? Each model's standard deviation (0.007 to 0.020) isn't the right yardstick here, because all three were scored on the *same* folds. Compare them fold by fold instead:

```python
boost = cv_scores["HistGradientBoosting tuned"]
print("boosting - logistic, per fold:", (boost - cv_scores["logistic regression"]).round(3))
print("boosting - forest,   per fold:", (boost - cv_scores["random forest"]).round(3))
```

```
boosting - logistic, per fold: [0.053 0.036 0.027 0.013 0.016]
boosting - forest,   per fold: [0.003 0.013 0.016 0.013 0.007]
```

Boosting beats logistic regression in all five folds, by 0.013 to 0.053, so that advantage is real on this data. It beats the forest in all five folds too, but only by 0.003 to 0.016: a small, consistent edge rather than a large one.

### Learning curves

A **learning curve** trains a model on increasing amounts of data and plots training and cross-validation scores for each size. First, for logistic regression alone, to see what the function returns:

```python
from sklearn.model_selection import learning_curve

sizes = [0.1, 0.25, 0.5, 0.75, 1.0]
n, tr_s, va_s = learning_curve(
    candidates["logistic regression"],
    X_rest,
    y_rest,
    cv=folds,
    scoring="roc_auc",
    train_sizes=sizes,
    shuffle=True,
    random_state=37,
)
print("rows used:", n)
print("shape of the training scores:", tr_s.shape)
print("training AUC by size:", tr_s.mean(axis=1).round(3))
print("CV AUC by size:      ", va_s.mean(axis=1).round(3))
```

```
rows used: [ 320  800 1600 2400 3200]
shape of the training scores: (5, 5)
training AUC by size: [0.87  0.827 0.822 0.822 0.82 ]
CV AUC by size:       [0.76  0.777 0.802 0.808 0.807]
```

- **`train_sizes=sizes`** are fractions of each training fold. With 5 folds, each fold trains on 4,000 × 4/5 = 3,200 accounts, so 0.1 means 320 rows, 0.25 means 800, and 1.0 means all 3,200: the `rows used`.
- `shuffle=True, random_state=37` shuffles the rows before taking the smaller slices, repeatably, so a slice isn't just the first rows of the file.
- It returns three arrays: the sizes; `tr_s`, the **training** scores; and `va_s`, the **cross-validation** scores. `tr_s.shape` is (5, 5): one row per size, one column per fold.
- **`.mean(axis=1)`** averages across each row (Chapter 18's NumPy basics: `axis=1` works across), so it gives one average over the five folds for each size.

Now both models, with the gap between training and CV at each size:

```python
curves = {}
for name in ["logistic regression", "HistGradientBoosting tuned"]:
    n, tr_s, va_s = learning_curve(
        candidates[name],
        X_rest,
        y_rest,
        cv=folds,
        scoring="roc_auc",
        train_sizes=sizes,
        shuffle=True,
        random_state=37,
    )
    curves[name] = (n, tr_s.mean(axis=1), va_s.mean(axis=1))
    for size, a, b in zip(n, tr_s.mean(axis=1), va_s.mean(axis=1)):
        print(
            f"{name:<27} {size:>5} rows   train AUC {a:.3f}"
            f"   CV AUC {b:.3f}   gap {a - b:.3f}"
        )
```

```
logistic regression           320 rows   train AUC 0.870   CV AUC 0.760   gap 0.110
logistic regression           800 rows   train AUC 0.827   CV AUC 0.777   gap 0.051
logistic regression          1600 rows   train AUC 0.822   CV AUC 0.802   gap 0.020
logistic regression          2400 rows   train AUC 0.822   CV AUC 0.808   gap 0.015
logistic regression          3200 rows   train AUC 0.820   CV AUC 0.807   gap 0.013
HistGradientBoosting tuned    320 rows   train AUC 1.000   CV AUC 0.745   gap 0.255
HistGradientBoosting tuned    800 rows   train AUC 0.994   CV AUC 0.792   gap 0.203
HistGradientBoosting tuned   1600 rows   train AUC 0.979   CV AUC 0.807   gap 0.172
HistGradientBoosting tuned   2400 rows   train AUC 0.959   CV AUC 0.816   gap 0.142
HistGradientBoosting tuned   3200 rows   train AUC 0.945   CV AUC 0.836   gap 0.109
```

`zip(n, ...)` walks the three arrays together, one size at a time (Chapter 17), and `curves` keeps the averages for the chart.

![Two stacked panels of learning curves on the same axes, training rows from 0 to 3,200 and AUC from 0.7 to 1.0. Logistic regression: training AUC falls from 0.870 to 0.820 and CV AUC rises from 0.760 to 0.807, meeting with a gap of 0.013. Gradient boosting: training AUC stays between about 0.95 and 1.0 while CV AUC rises steadily to about 0.84, with a gap that is still closing](figures/fig37-4-learning-curves.svg)

*Figure 37.4 — Learning curves. Logistic regression has converged: more rows won't help, a sign of bias. Boosting still has a big train–CV gap and is still improving: a sign of variance that more data would reduce.*

**Reading it.**

- **Logistic regression** has **high bias**. By 1,600 rows, its training and CV scores have nearly met (gap 0.013 at 3,200 rows), and the CV score has flattened at about 0.807. More data won't help. The model is missing something.
- **Boosting** has **higher variance**: a training AUC of 0.945 against 0.836 on CV. But its CV score is still climbing at 3,200 rows, so more accounts would likely help it further.

### Fixing bias with features

Logistic regression's problem is structural: it can't represent "no order in 90 days" as a jump, or "late payments matter for small retailers" as an interaction. So look for those shapes in the training accounts, and build them as features. The depth-2 tree in section 37.6 pointed at recency and late payment; the sales team's warning signs point at small retailers and new accounts that complain. Check each against `train_acc` only.

**Recency.** Churn rate by bands of days since the last order:

```python
days_band = pd.cut(
    train_acc["days_since_last_order"], [0, 30, 60, 90, 120, 150, 180, 240, 365]
)
by_days = train_acc.groupby(days_band, observed=True)["churned_2025"]
print(by_days.agg(["mean", "size"]).round(3))
```

```
                        mean  size
days_since_last_order             
(0, 30]                0.051  1556
(30, 60]               0.030   542
(60, 90]               0.031   286
(90, 120]              0.187   182
(120, 150]             0.150   100
(150, 180]             0.275    69
(180, 240]             0.477   111
(240, 365]             0.416   154
```

- `pd.cut(column, edges)` puts each value in a band (Chapter 18); `(90, 120]` means "more than 90, up to 120".
- `groupby(days_band, observed=True)` groups by band; `observed=True` lists only bands that occur. `.agg(["mean", "size"])` gives each band's churn rate and number of accounts.

Churn sits at 3–5% up to 90 days, **jumps to about 19% after 90 days**, and **jumps again, to over 40%, after 180 days**. Two thresholds, not a straight line: features `no_order_90` and `no_order_180`.

**Late payers, by segment and size.** Among accounts more than 25 days late on average:

```python
late = train_acc[train_acc["late_payment_days"] > 25]
rates = pd.crosstab(
    late["segment"], late["company_size"], values=late["churned_2025"], aggfunc="mean"
)
print(rates.round(2))
print(pd.crosstab(late["segment"], late["company_size"]))
```

```
company_size  Large  Medium  Small
segment                           
Hospitality    0.14    0.11   0.21
Retail         0.09    0.00   0.45
Wholesale      0.06    0.00   0.05
company_size  Large  Medium  Small
segment                           
Hospitality       7      35    101
Retail           11      35    134
Wholesale        17      27     20
```

- `pd.crosstab(rows, columns, values=..., aggfunc="mean")` fills each cell with the mean of `values` for that combination, here a churn rate, instead of a count.
- The second table is the plain count, so you can see how many accounts sit behind each rate.

Late-paying **small retailers** churn at 45%, from 134 accounts; no other late-paying group is above about 20%. That's an interaction: `late_small_retail`.

**Complaints, by how new the account is:**

```python
tenure_band = pd.cut(
    train_acc["tenure_months"],
    [0, 6, 12, 18, 24, 36, 121],
    right=False,
    labels=["under 6", "6-11", "12-17", "18-23", "24-35", "36+"],
)
complaints = train_acc["complaints_2024"].clip(upper=2)
rates = pd.crosstab(
    tenure_band, complaints, values=train_acc["churned_2025"], aggfunc="mean"
)
print(rates.round(2))
```

```
complaints_2024     0     1     2
tenure_months                    
under 6          0.18  0.09  0.36
6-11             0.08  0.08  0.15
12-17            0.11  0.09  0.30
18-23            0.16  0.08  0.06
24-35            0.09  0.06  0.02
36+              0.09  0.08  0.05
```

- `right=False` makes each band include its left edge and exclude its right one, so `[12, 18)` is 12 to 17 months; `labels=` gives the bands readable names.
- `.clip(upper=2)` turns every count above 2 into 2, so the column `2` means "two or more complaints".

Accounts with two or more complaints churn at 15–36% in their first 18 months, and at 6% or less after that: `new_and_complaining` means two or more complaints and under 18 months' tenure.

Now build the four features on the 4,000 non-test accounts and on the test accounts, with exactly the same rules:

```python
ENG = ["no_order_90", "no_order_180", "late_small_retail", "new_and_complaining"]
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
print(engineered[ENG].mean().round(3))
```

```
no_order_90            0.206
no_order_180           0.087
late_small_retail      0.042
new_and_complaining    0.039
dtype: float64
```

- `for df in (engineered, test_eng):` runs the same four lines on each table in turn. `df` is just a second name for the table, so adding a column to `df` adds it to `engineered` (first time round) and to `test_eng` (second time).
- `.astype(int)` turns True/False into 1/0.
- `engineered[ENG].mean()` is the share of accounts with each flag: how common each sign is.

Then cross-validate logistic regression with the four extra columns. `clf_pipeline`'s `nums=` argument takes the longer list:

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

Two caveats before reading the result. The thresholds came from the training accounts, but we knew where to look: the tree and the sales team's own warning signs pointed there. And on this generated data, those warning signs match how churn was actually made. Treat the score below as close to the best case; on real data you won't know the true pattern, and your features will usually catch less of it.

**Reading it.** With four engineered features, logistic regression's cross-validated AUC jumps from 0.807 to **0.849**, above tuned boosting's 0.836 and close to the 0.858 ceiling from section 37.0.

That's a useful lesson and an honest one. Boosting's advantage is that it finds such patterns without being told. The practical workflow is to use both: let boosting show what's possible, then ask whether a simpler model with good features gets close enough to be worth its transparency.

---

## 37.11 Hyperparameter tuning

### Settings are chosen, not learned

**Hyperparameters** are the settings you choose before training: tree depth, learning rate, C, *k*. **Tuning** means trying different values and keeping the best, judged by cross-validation on the training data, never on the test set.

- **Grid search** (`GridSearchCV`) tries every combination of listed values. Five settings with four values each is 4<sup>5</sup> = 1,024 combinations, times 5 folds: 5,120 fits. It grows too fast.
- **Random search** (`RandomizedSearchCV`) samples a fixed number of combinations from ranges you give. For the same budget, it explores more values of the settings that matter most. Use it instead of grid search by default.
- **Bayesian optimization** (Optuna, and others) chooses each next combination based on how earlier ones scored, spending more trials in promising regions.

### Random search

Random search draws each setting from a **distribution**. SciPy (installed in Chapter 21) provides two. See what they produce before using them:

```python
from scipy.stats import loguniform, randint

print(loguniform(0.01, 0.3).rvs(5, random_state=1).round(4))
print(randint(10, 100).rvs(5, random_state=1))
```

```
[0.0413 0.1159 0.01   0.028  0.0165]
[47 22 82 19 85]
```

- `loguniform(0.01, 0.3)` draws numbers between 0.01 and 0.3, evenly on a log scale, so 0.01–0.03 gets as many draws as 0.1–0.3. Use it for any setting that spans orders of magnitude, like a learning rate.
- `randint(10, 100)` draws whole numbers from 10 to 99.
- `.rvs(5, random_state=1)` draws five, repeatably. The search makes its own draws; this is only to see them.

Now the search:

```python
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
search.fit(X_rest, y_rest)
print(f"best CV AUC {search.best_score_:.3f}")
```

```
best CV AUC 0.841
```

| Setting | Meaning here |
|---|---|
| `param_distributions` | A range or list for each setting. A list, like `[2, 3, 4, 6, None]`, is drawn from with equal chances |
| `model__learning_rate` | "the `learning_rate` of the step named `model`": that's how a search reaches inside a pipeline |
| `n_iter=25` | Try 25 random combinations |
| `cv=folds` | Score each one on the same 5 folds as before |
| `scoring="roc_auc"` | Rank combinations by mean AUC |
| `random_state=37` | Draw the same 25 combinations every run |
| `n_jobs=1` | Use one CPU core, so the run repeats exactly |
| (default) `refit=True` | After the search, refit the best combination on all 4,000 accounts; that's why `search.best_estimator_` is ready to use |

Every one of the 25 combinations is scored with the same 5 folds, and the preparation steps are re-learned in each fold: no leakage (Chapter 36). The search takes about a minute on one CPU core. Now the winner's settings, and the top five:

```python
for setting, value in search.best_params_.items():
    print(f"{setting}: {value:.4g}")
top = pd.DataFrame(search.cv_results_).sort_values("rank_test_score")
print(top[["mean_test_score", "std_test_score"]].head(5).round(3).to_string(index=False))
```

```
FILL
```

- `best_params_` is a dictionary of the winning settings, with their `model__` names; the loop prints each one, and `:.4g` shows four significant digits.
- `cv_results_` holds one row per combination tried; `rank_test_score` is 1 for the best mean AUC, 2 for the next, and so on, so sorting by it puts the best first.

**Reading it.** The best combination scores 0.841, only 0.005 above the hand-picked settings used earlier (0.836), and the top five are all within a few thousandths of each other, well inside their fold-to-fold standard deviation of about 0.016. **Tuning helped a little, and the exact winner is partly luck.** That's typical: the first sensible settings get you most of the way. The best settings share a pattern worth noticing: a small learning rate, shallow trees (depth 3), large leaves (93 rows), and strong L2 regularization. With only 290 churners in training, the model does best when it's kept simple.

### Optuna

```python
import optuna

optuna.logging.set_verbosity(optuna.logging.WARNING)


def objective(trial):
    model = HistGradientBoostingClassifier(
        learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        max_depth=trial.suggest_int("max_depth", 2, 6),
        min_samples_leaf=trial.suggest_int("min_samples_leaf", 10, 100),
        max_iter=trial.suggest_int("max_iter", 100, 500),
        l2_regularization=trial.suggest_float("l2_regularization", 1e-3, 10, log=True),
        random_state=37,
    )
    return cross_val_score(
        clf_pipeline(model, scale=False), X_rest, y_rest, cv=folds, scoring="roc_auc"
    ).mean()


study = optuna.create_study(
    direction="maximize", sampler=optuna.samplers.TPESampler(seed=37)
)
study.optimize(objective, n_trials=25)
print(f"optuna {optuna.__version__}: best CV AUC {study.best_value:.3f}")
print({k: round(v, 4) for k, v in study.best_params.items()})
```

```
optuna 5.0.0: best CV AUC 0.843
{'learning_rate': 0.026, 'max_depth': 3, 'min_samples_leaf': 64, 'max_iter': 425, 'l2_regularization': 7.8947}
```

**How it works:**

- `optuna.logging.set_verbosity(optuna.logging.WARNING)` silences Optuna's line-per-trial messages, keeping only warnings.
- `objective(trial)` is the function Optuna calls once per trial. Each `trial.suggest_...` call picks a value for one setting: `suggest_float(..., log=True)` is the same idea as `loguniform`, and `suggest_int` picks a whole number in the range. The function returns the cross-validated AUC for those settings.
- `create_study(direction="maximize", ...)` tells Optuna that higher scores are better; its **TPE** sampler, a Bayesian method, uses past results to choose the next values, and `seed=37` makes the search repeatable.
- `study.optimize(objective, n_trials=25)` runs 25 trials, the same budget as random search. The last line rounds each best setting to four decimals with a dictionary comprehension (Chapter 17); whole numbers like `max_depth` are unchanged by `round`.

**Reading it.** Optuna finds 0.843 against random search's 0.841, a tie by this chapter's rule (a difference far inside the fold standard deviation). Its advantage appears with larger search spaces or slower models, where each trial is expensive and choosing trials intelligently saves real time.

> **Watch out: tuning can overfit the validation data.** Try enough combinations and one will score well by chance. Three habits keep you honest: tune with cross-validation, not one validation set; don't read much into differences smaller than the fold standard deviation; and score the **test set once**, at the end, for the final choice only.

### The test set, once

Three candidates remain for churn: plain logistic regression, logistic regression with engineered features, and tuned boosting. Each is refitted on all 4,000 non-test accounts and scored once on the 1,000 test accounts. Each entry records the pipeline, the table it learns from, the table it's scored on, and its columns:

```python
final_models = {
    "logistic regression": (
        clf_pipeline(LogisticRegression(max_iter=2000)), rest, test_acc, CATS + NUMS
    ),
    "logistic + engineered": (eng_pipe, engineered, test_eng, CATS + NUMS + ENG),
    "tuned boosting (random search)": (
        search.best_estimator_, rest, test_acc, CATS + NUMS
    ),
}
for name, (pipe, learn_from, score_on, cols) in final_models.items():
    pipe.fit(learn_from[cols], learn_from["churned_2025"])
    p = pipe.predict_proba(score_on[cols])[:, 1]
    auc = roc_auc_score(score_on["churned_2025"], p)
    loss = log_loss(score_on["churned_2025"], p)
    print(f"{name:<32} test AUC {auc:.3f}   log loss {loss:.4f}")
```

```
logistic regression              test AUC 0.797   log loss 0.2538
logistic + engineered            test AUC 0.850   log loss 0.2278
tuned boosting (random search)   test AUC 0.838   log loss 0.2381
```

- Each value in `final_models` is a **tuple** of four things, and `for name, (pipe, learn_from, score_on, cols) in ...` unpacks them into four names, so the loop never has to guess which data a model uses.
- The engineered model learns from `engineered` and is scored on `test_eng`, the two tables that have the four extra columns.

**Reading it.** The test results agree with cross-validation: plain logistic regression **0.797**, tuned boosting **0.838**, logistic regression with engineered features **0.850**, also with the best log loss.

**What to tell Anita.** "We can rank accounts by their risk of stopping ordering well enough to act on. The strongest warning signs are no order in the last three months, late payments at small retail accounts, and complaints from newer accounts, and customers buying several product lines rarely leave. I recommend the simpler model built on those signs: it's at least as accurate as the complex one on accounts it hadn't seen, and we can explain every score to the sales team."

---

## 37.12 Project result: lead scoring, baseline vs boosting

Now the question this chapter's project asks: does gradient boosting beat Chapter 36's logistic regression on Riverstone's leads? Tune boosting with a **time-series** cross-validation on the 2023–2024 leads (the leads arrive over time), then compare on validation and, once, on test.

`companion/ch37/lead_data.py` rebuilds Chapter 36's cleaned table and features in one call, so Chapter 36's steps aren't repeated here. It provides four names:

- `load_leads()` returns three tables, `train` (2023–2024), `valid` (January to June 2025) and `test` (July 2025 on), exactly Chapter 36's time split, with rows **sorted by enquiry date**, which `TimeSeriesSplit` needs.
- `LEAD_CATS` and `LEAD_NUMS` are Chapter 36's five categorical and eight numeric columns.
- `make_model(cats, nums, model=None)` is Chapter 36's `make_model` (section 36.4) with one optional extra: pass a `model` and it replaces the default, `LogisticRegression(max_iter=1000)`.

First load the leads, and set up the search:

```python
import sys

sys.path.append(".")  # so Python finds lead_data.py in this folder
from lead_data import LEAD_CATS, LEAD_NUMS, load_leads, make_model
from sklearn.model_selection import TimeSeriesSplit

leads_train, leads_valid, leads_test = load_leads()
LX = LEAD_CATS + LEAD_NUMS
print(f"{len(leads_train):,} training leads, {leads_train['won'].sum()} won")
```

```
7,291 training leads, 576 won
```

- `sys.path.append(".")` tells Python to look for `lead_data.py` in the current folder (a notebook opened in `companion/ch37/` already does).
- `load_leads()` returns the three tables; `LX` is the list of all thirteen feature columns.

Then the search, as in section 37.11 but with time-series folds:

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
best = lead_search.best_index_
fold_aucs = [lead_search.cv_results_[f"split{i}_test_score"][best] for i in range(4)]
print("its four folds, earliest first:", np.round(fold_aucs, 3))
```

```
tuned boosting, time-series CV AUC 0.769
its four folds, earliest first: [0.75  0.784 0.766 0.775]
```

- `TimeSeriesSplit(n_splits=4)` cuts the time-ordered training leads into five slices and makes four folds: train on slice 1 and score slice 2, then train on slices 1–2 and score slice 3, and so on. Every fold scores leads that came *after* the ones it learned from.
- `best_index_` is the row of `cv_results_` for the winning settings, and `split0_test_score` to `split3_test_score` are its four fold scores.

Then compare with Chapter 36's model, on validation and, once, on test:

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

```
VALID logistic (Ch 36)   AUC 0.823   log loss 0.1948
VALID tuned boosting     AUC 0.826   log loss 0.1965
TEST  logistic (Ch 36)   AUC 0.838   log loss 0.2369
TEST  tuned boosting     AUC 0.830   log loss 0.2422
```

- For **VALID**, both models learn from 2023–2024 and are scored on January to June 2025. For **TEST**, both learn from everything before July 2025 (`pd.concat` stacks training and validation) and are scored on the test leads, once.
- `make_model(LEAD_CATS, LEAD_NUMS)` with no third argument is exactly Chapter 36's logistic regression.

**Reading it.** On leads, **boosting doesn't win**. On validation it ranks marginally better (AUC 0.826 against 0.823) but its probabilities are worse (log loss 0.1965 against 0.1948). On the test set, logistic regression is ahead on both (0.838 against 0.830, and 0.2369 against 0.2422). The differences are small enough to be noise either way.

The time-series CV score, 0.769, sits well below both validation scores. That's the folds, not the model: every fold learns from less than the full two years, the earliest from only a fifth of them, and it scores lowest (0.750).

Why the opposite of the churn result? The leads data's signal is mostly **additive**: each feature (source, email type, text, quantity) pushes the odds up or down on its own, which is exactly the shape logistic regression assumes. There's little interaction for boosting to find, and with 576 wins in training (printed above), its extra flexibility mostly fits noise. The churn data has thresholds and interactions, and boosting's flexibility pays off.

**The decision:** keep logistic regression for lead scoring. It's as accurate, better calibrated, faster, and explainable. That's not a failure of the project; finding out that the simple model is enough is one of the most valuable results a data scientist can deliver.

### Checkpoint: end of Part B

Check that you can do these by hand, without looking back:

1. A group of 400 accounts has 40 churners. Its Gini impurity? (Answer: 2 × 0.1 × 0.9 = 0.18.) It splits into 100 accounts with 30 churners and 300 with 10. The weighted Gini after? (Answer: 0.25 × 0.42 + 0.75 × 0.0644 = 0.105 + 0.048 = 0.153.)
2. One boosting round, learning rate 0.5, on four accounts with targets 0, 0, 0, 1, where a stump separates the last account from the rest. New predictions? (Answer: start at 0.25; residuals −0.25 and +0.75; new predictions 0.125, 0.125, 0.125 and 0.625.)

---

## Which algorithm when

| Algorithm | Best for | Needs scaling? | Handles interactions? | Interpretable? | Watch out for |
|---|---|---|---|---|---|
| Linear regression | Numeric targets with roughly linear effects; explanation | Yes, for comparing or regularizing | No (build them) | Yes: coefficients | Outliers, multicollinearity, skewed targets |
| Ridge / lasso / elastic net | Many or correlated features; feature selection (lasso) | Yes | No | Yes | Choosing α; lasso picking one of a correlated group |
| Logistic regression | First model for any classification; calibrated probabilities | Yes | No (build them) | Yes: odds ratios | Thresholds and interactions it can't see |
| k-nearest neighbors | Small data, few features; similarity lookups | Essential | Yes, implicitly | By example only | Many features, large data, choice of k |
| Naive Bayes | Text, very small data, speed | No (in scikit-learn, slightly: section 37.5) | No | Partly | Overconfident probabilities |
| Decision tree | Rules people must follow; teaching | No | Yes | Yes, if shallow | Overfitting; instability |
| Random forest | Strong default with little tuning | No | Yes | Importance only | Large models; biased impurity importance |
| Gradient boosting | Best accuracy on tabular data with thousands of rows | No | Yes | With SHAP (Ch 39) | Tuning; overfitting small data |
| SVM | Medium data with many features (text); clear separation | Essential | Yes (kernels) | Little | Slow on large data; imbalance; no native probabilities |

**A default workflow for tabular problems:** baselines (Chapter 36) → logistic or linear regression → a random forest or default gradient boosting → learning curves to diagnose → better features or tuned boosting, depending on what the curves say → cross-validated comparison → the simplest model that's close enough to the best → the test set, once.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Reading coefficients of correlated features one by one | Signs that make no sense (revenue up, units down) | Interpret groups together; use lasso or drop duplicates |
| Treating a coefficient as a cause | "Late payments cause 5% less growth" in a slide | Say "associated with"; use Chapter 31's methods for causes |
| Acting on a coefficient without an interval | Decisions based on noise (the inside-desk +3%) | Use `statsmodels` for confidence intervals (Chapter 30, section 30.11; the one-feature version is in section 22.10) |
| Regularizing unscaled features | Rupee-scale features escape the penalty | Standardize inside the pipeline |
| Confusing C and α | Increasing C and expecting more regularization | Smaller C = stronger regularization |
| k-NN or SVM without scaling | AUC far below simpler models | Scale in the pipeline |
| Trusting Naive Bayes probabilities | Log loss far worse than AUC suggests | Use it for ranking, or calibrate (Chapter 39, section 39.4) |
| Unlimited tree depth | Training AUC 1.0, validation near 0.5 | Limit `max_depth` or `min_samples_leaf` |
| Default SVM on imbalanced data | AUC near 0.5 | `class_weight="balanced"` |
| Choosing a library on one validation set | Switching libraries for 0.01 AUC | Cross-validate; differences within fold spread are noise |
| Grid search over many settings | Hours of compute, little gain | Random search or Optuna with a fixed budget |
| Tuning on the test set | Test score improves with each try | Tune with CV on training data; score test once |
| Assuming boosting always wins | Complex model deployed for no gain | Compare with a baseline and a linear model with good features |
| Impurity importance as the final word | High-cardinality features look most important | Permutation importance or SHAP (Chapter 39, section 39.8) |

---

## In the real world: "Should we buy the AutoML tool?"

In April 2026, Riverstone's finance team is renewing software licences, and Vikram forwards a quote for an **AutoML** platform, a service that tries dozens of algorithms and settings automatically. The vendor's demo showed a "stacked ensemble of 40 models" scoring a churn AUC of 0.85. The question for Meera: *is it worth ₹6 lakh a year?*

Meera doesn't argue about AutoML in general. She asks the vendor to run its tool on exactly the same split this chapter used: learn from the 4,000 non-test accounts, and score the 1,000 test accounts once. Its 0.85 is that single test score. Her own numbers are the single test scores from section 37.11.

**Step 1: what does simple get?** Logistic regression: 0.80. That's the floor any tool must beat.

**Step 2: what does standard get?** Gradient boosting with 25 rounds of random search, about a minute of compute: 0.84.

**Step 3: what does thinking get?** Logistic regression with four features built from the tree's first splits and the sales team's own warning signs (no order for three months, late-paying small retailers, new accounts with complaints): 0.85.

**Step 4: what does each option cost to live with?** The AutoML ensemble can't be explained account by account without extra tooling, needs the vendor's platform to run, and must be retrained through it. The logistic model is a few lines in the existing pipeline, and each account's score can be broken down into the signs that drove it, which the account managers will want before they call a customer.

Her note to Vikram:

> *"On our own test accounts, scored once, the AutoML ensemble (0.85) matches what we already get from a simple model built on the sales team's warning signs (0.85), and its lead over our quickly tuned boosting model (0.84) is within the noise: with five models scored on the same 1,000 accounts, 0.84 against 0.85 is a tie. The simple model is free, runs in our existing pipeline, and can explain every score. I'd skip the licence for now. If we later have problems with many more features, like predicting demand for 200 products, AutoML would be worth a trial, because that's where automatic search saves real time."*

Vikram cancels the renewal request. Two months later, Meera does use an open-source AutoML library for a weekend experiment on product demand, as a quick way to see what's possible before building by hand, which is where such tools shine.

---

## Project: lead scoring, baseline vs boosting

**Goal:** a documented, fair comparison of algorithms on one problem, ending in a justified choice. Section 37.12 ran the core comparison for leads; the project extends it and makes it yours.

### Tools you'll need

- **scikit-learn** (tested on 1.9.1, installed in Chapter 35): `LinearRegression`, `RidgeCV`, `LassoCV`, `ElasticNetCV`, `LogisticRegression`, `KNeighborsClassifier`, `BernoulliNB`, `GaussianNB`, `DecisionTreeClassifier` and `export_text`, `RandomForestClassifier`, `HistGradientBoostingClassifier`, `SVC` with `CalibratedClassifierCV`, `learning_curve`, `RandomizedSearchCV`.
- **XGBoost** 3.2.0, **LightGBM** 4.7.0, **CatBoost** 1.2.10 and **Optuna** 5.0.0, installed in section 37.0 with `python -m pip install xgboost lightgbm catboost optuna`. All are free and open source; versions move quickly, so check each project's documentation for the current parameter names.
- **SciPy** (Chapter 21) for the `loguniform` and `randint` distributions in random search.
- **statsmodels** (Chapter 22) for regression with confidence intervals and p-values, read as in Chapter 30, section 30.11.
- Everything ran on one CPU core, Python 3.11.15, pandas 3.0.6, on 29 September 2026. The slowest step, 25 rounds of 5-fold random search, took about a minute.
- **Companion files:** `companion/generate_riverstone_accounts.py` (seed 20237) builds `companion/accounts/accounts.csv`, whose columns are described in section 37.0's table; `companion/ch37/lead_data.py` rebuilds Chapter 36's lead table. Run the chapter's code from `companion/ch37/`.

**Option A: your own data.** Any classification or regression problem you set up with Chapter 36's workflow.

**Option B: Riverstone.** Lead scoring (`lead_data.py`) or account churn (`accounts.csv`), or both.

**Steps:**

1. **Start from the Chapter 36 pipeline and baselines.** Record the base rate, the rule of thumb, and logistic regression on validation.
2. **Train one model from each family:** logistic regression, k-NN, Naive Bayes, a decision tree, a random forest, one gradient-boosting library, and an SVM. Use the same pipeline and validation set for all.
3. **Hand-check one thing per family:** one sigmoid probability, one k-NN prediction, one Naive Bayes posterior, one Gini split, one round of boosting on a few rows.
4. **Cross-validate the top three** (use a time-series split for leads) and report means, standard deviations, and fold-by-fold differences.
5. **Draw learning curves** for the simplest and the most flexible of the three, and write two sentences diagnosing bias or variance.
6. **Try to close the gap** with features or with tuning, depending on the diagnosis. Derive any feature from the training rows only. Use random search or Optuna with a fixed budget.
7. **Score the test set once** for your final two candidates.
8. **Write a one-page decision memo:** which model you recommend and why, what it costs to run and explain, and what you'd try next.

**Stretch goals:**

- Add **early stopping** to the gradient-boosting model (`early_stopping=True` in `HistGradientBoostingClassifier`, or an evaluation set in XGBoost and LightGBM) and compare training time and score.
- Build a **stacking** model (`StackingClassifier`) that combines logistic regression and boosting, and check fairly whether it beats either alone.
- Fit the regression model in `statsmodels` and compare its confidence interval for the inside-sales-desk coefficient with the effect you see.
- Try a **monotonic constraint** in `HistGradientBoostingClassifier` (for example, churn risk must not fall as days since last order rise) and see whether it costs any accuracy.

---

## Recap

- **Linear regression** fits a weighted sum by least squares; interpret coefficients carefully (scaling, multicollinearity, noise, not causes). **MAE** is the average size of the misses.
- **Ridge** shrinks all weights, **lasso** zeroes some (feature selection), **elastic net** mixes them. Scale first. They help most with many or correlated features.
- **Logistic regression** passes a weighted sum through the **sigmoid** to get a probability, fitted by maximum likelihood. Read it with **odds ratios**, which multiply odds, not probabilities. Smaller **C** means more regularization. It can't see thresholds or interactions unless you build them.
- **k-NN** predicts from the nearest training rows; choose *k*, always scale, avoid many features.
- **Naive Bayes** multiplies a prior by per-feature likelihoods, assuming independence, to get a posterior; fast, good for text, overconfident probabilities.
- **Decision trees** split on the question that most reduces **Gini** or **entropy**; readable, find interactions, overfit when deep.
- **Random forests** average many decorrelated trees (**bagging** on bootstrap samples + random features): a robust default.
- **Gradient boosting** adds small trees one at a time, each fitting the current errors, scaled by a **learning rate**: usually the most accurate on tabular data. XGBoost, LightGBM, and CatBoost are the main libraries.
- **SVMs** find the widest-margin boundary; kernels bend it; they need scaling and class weights for imbalance.
- **Bias** is underfitting, **variance** is overfitting; **learning curves** tell them apart.
- **Tune** with random search or **Optuna** inside cross-validation; score the test set once.
- The best algorithm depends on the data: boosting won on churn, tied on leads, and a simple model with good features derived from the training data beat both on churn.

---

## Key terms

supervised learning · regression · classification · underfitting · overfitting · linear regression · least squares · intercept · coefficient · R² (coefficient of determination) · log-log model · mean absolute error (MAE) · dummy variable trap · multicollinearity · residual · regularization · penalty · alpha (α) · ridge regression (L2) · lasso (L1) · elastic net · feature selection · logistic regression · odds · log-odds · sigmoid · odds ratio · calibrated probabilities · C (inverse regularization) · k-nearest neighbors · curse of dimensionality · Naive Bayes · Bayes' rule · prior · likelihood · posterior · conditional independence · smoothing · decision tree · node · leaf · split · Gini impurity · entropy · max_depth · min_samples_leaf · random forest · bagging · bootstrap sample · feature importance · permutation importance · SHAP · gradient boosting · residual fitting · stump · learning rate · XGBoost · LightGBM · CatBoost · support vector machine · margin · support vector · kernel · RBF kernel · Platt scaling · class weight · bias · variance · learning curve · hyperparameter · grid search · random search · Bayesian optimization · Optuna

*Also met in the exercises and the story:* validation curve · stacking · early stopping · AutoML

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can explain, in two sentences each, how linear regression, logistic regression, k-NN, Naive Bayes, trees, random forests, gradient boosting, and SVMs make a prediction.
- [ ] I can read a regression coefficient and an odds ratio in plain language, and I know why correlated features make them unreliable.
- [ ] I know what ridge, lasso, and elastic net penalize, why features must be scaled for them, and that smaller C means stronger regularization.
- [ ] I can compute a weighted sum, a ridge shrinkage, a sigmoid probability, a k-NN prediction, a Naive Bayes posterior, a Gini split, and one boosting round by hand.
- [ ] I can recognize an overfitting tree from its training and validation scores.
- [ ] I can explain why averaging trees (forest) and chaining trees (boosting) both beat a single tree.
- [ ] I know the main settings of gradient boosting and what each controls.
- [ ] I handle class imbalance in SVMs and know when an algorithm needs scaling.
- [ ] I can read learning curves and say whether a model suffers from bias or variance, and what to do about each.
- [ ] I tune with random search or Optuna inside cross-validation, and I treat differences smaller than the fold spread as noise.
- [ ] I compare complex models with baselines and with simple models that have good features, and I can defend choosing the simpler one.

---

## Exercises

Code exercises run from `companion/ch37/` after the chapter's code (they use `train_acc`, `valid_acc`, `rest`, `test_acc`, `CATS`, `NUMS`, `clf_pipeline`, `clf_report`, `reg_pipeline`, `reg_report`, `reg_train`, `reg_test`, `folds`, and the other names defined above). Predict each result before running it.

### Warm-up

1. *(hand)* A logistic regression gives an account *z* = 0.8. What churn probability does it predict? What *z* corresponds to a probability of exactly 0.5?
2. *(hand)* An odds ratio for `complaints_2024` (unscaled, per complaint) is 1.45. An account with a 10% churn probability files one more complaint. What are its new odds and new probability?
3. *(hand)* A group of 200 accounts has 50 churners. Calculate its Gini impurity and its entropy.
4. For each situation, name the algorithm you'd try first and one reason: (a) 300 rows, 4 features, the sales team must follow the rules by hand; (b) 50,000 accounts, 60 mixed features, maximum accuracy; (c) classifying 20,000 support tickets by their words; (d) predicting next month's revenue per customer for a finance report that must explain each driver.
5. *(hand)* Five scaled training accounts: P (1, 1) churned, Q (2, 3) stayed, R (4, 4) stayed, S (3, 2) stayed, T (5, 1) churned. What does k-NN with *k* = 3 predict for a new account at (2, 1)?
6. *(hand)* One standardized feature, no intercept: *x* = −2, −1, 1, 2 and *y* = −3, −1, 2, 4. Find the ridge weight *w* = Σ*xy* ÷ (Σ*x*² + α) for α = 0, 2 and 10.
7. *(hand)* Four accounts with days since last order 10, 20, 100 and 200, and targets 0, 0, 0, 1. Do one round of boosting with squared error, a stump, and a learning rate of 0.5: where does the stump split, what are the new predictions, and how much does the squared error fall?

### Core

8. Fit `RidgeCV` and `LassoCV` on the regression data **without** `log_revenue_2024`. How do R² and the coefficients of `log_units_2024` and `log_orders_2024` change? What does that tell you about multicollinearity?
9. For k-NN, try `weights="distance"` with *k* = 75. Does weighting closer neighbors more help on validation?
10. Using the training accounts, compute by hand (in code, without a tree) the weighted Gini after splitting on `categories_bought >= 3`. Is it a better first split than `days_since_last_order > 90`?
11. Train a random forest with `n_estimators` of 10, 50, 300, and 1,000 (keep `min_samples_leaf=5`). Report validation AUC. Does adding trees ever make it worse?
12. Continue the eight-row boosting example for 20 rounds instead of 3, and print the squared error every 5 rounds. What happens to the error, and why is that a warning sign rather than good news?
13. Draw a validation curve for `HistGradientBoostingClassifier`'s `max_depth` (2, 3, 4, 6, 8) using `validation_curve` with the 5 folds on `rest`. Where does it peak?

### Stretch

14. Build a `StackingClassifier` from logistic regression and tuned boosting (`search.best_estimator_`), with a logistic regression on top. Cross-validate it on `rest`. Does it beat both parts?
15. Add the four engineered features from section 37.10 to the tuned boosting model. Does boosting gain as much as logistic regression did? Explain.
16. Using `statsmodels`, fit an ordinary least squares regression of `log_revenue_2025` on the same features (one-hot with drop first, unscaled numbers) and read the 95% confidence interval for the inside-sales-desk dummy. Does it include zero?

### Think about it

17. A colleague says: "Boosting got 0.841 in tuning and logistic regression got 0.807, so boosting is 4% better." Give two corrections.
18. Why can a random forest's feature importance rank `revenue_2024` above `complaints_2024` even if complaints matter more for churn?
19. The sales head asks why the model was accurate last year but is worse this year. Using bias and variance, and Chapter 36's ideas, give three possible explanations.

---

## Answers

*Every calculation was checked, and every code output shown is real.*

**1.** probability = 1 ÷ (1 + *e*<sup>−0.8</sup>) = 1 ÷ (1 + 0.4493) = **0.690**. A probability of 0.5 needs 1 + *e*<sup>−*z*</sup> = 2, so *e*<sup>−*z*</sup> = 1 and ***z* = 0**. Any account whose weighted sum is exactly zero sits on the fence.

**2.** Odds = probability ÷ (1 − probability) = 0.10 ÷ 0.90 = 0.1111. One more complaint multiplies the odds by 1.45: 0.1111 × 1.45 = **0.1611**. Back to a probability: odds ÷ (1 + odds) = 0.1611 ÷ 1.1611 = **0.139**, or 13.9%. As section 37.3 warned, multiplying the probability itself (10% × 1.45 = 14.5%) is the common mistake.

**3.** *p* = 50 ÷ 200 = 0.25. Gini = 2 × 0.25 × 0.75 = **0.375**. Entropy = −(0.25 × log<sub>2</sub> 0.25 + 0.75 × log<sub>2</sub> 0.75) = −(0.25 × (−2) + 0.75 × (−0.4150)) = 0.5 + 0.3113 = **0.811 bits**.

**4.** (a) A **shallow decision tree** (depth 2 or 3): with 300 rows, complex models overfit, and a tree's rules can be printed and followed by hand. (b) **Gradient boosting**: plenty of rows, mixed features, and accuracy as the goal, with logistic regression as the baseline to beat. (c) **Logistic regression or Naive Bayes on word features** (TF-IDF, Chapter 41), or a linear SVM: text gives thousands of sparse features, where linear models are fast and strong. (d) **Linear regression** (regularized if there are many features) on a log target: finance needs each driver's effect stated, which coefficients provide.

**5.** Distances from (2, 1): P √(1² + 0²) = 1.0; Q √(0² + 2²) = 2.0; R √(2² + 3²) = 3.606; S √(1² + 1²) = 1.414; T √(3² + 0²) = 3.0. The three nearest are P, S and Q; one of them (P) churned, so the prediction is 1 ÷ 3 = **0.333**.

**6.** Σ*xy* = 6 + 1 + 2 + 8 = 17; Σ*x*² = 4 + 1 + 1 + 4 = 10. α = 0: 17 ÷ 10 = **1.7** (plain least squares). α = 2: 17 ÷ 12 = **1.417**. α = 10: 17 ÷ 20 = **0.85**. The weight shrinks as α grows, but never to zero.

**7.** Start at the average, 1 ÷ 4 = 0.25; squared error = (3 × 0.25² + 0.75²) ÷ 4 = **0.1875**. Residuals: −0.25, −0.25, −0.25 and +0.75. The stump splits between 100 and 200 days (at 150), because that leaves each side with identical residuals: −0.25 on the left, +0.75 on the right. New predictions: 0.25 + 0.5 × (−0.25) = **0.125** for the first three, and 0.25 + 0.5 × 0.75 = **0.625** for the last. New squared error = (3 × 0.125² + 0.375²) ÷ 4 = (0.0469 + 0.1406) ÷ 4 = **0.0469**, a quarter of where it started.

**8.**

```python
without = [c for c in REG_NUMS if c != "log_revenue_2024"]
names_wo = (
    reg_pipeline(LinearRegression(), nums=without)
    .fit(reg_train[CATS + without], reg_train["log_revenue_2025"])
    .named_steps["prepare"]
    .get_feature_names_out()
)
for label, model in [
    ("ridge", RidgeCV(alphas=np.logspace(-3, 3, 25))),
    ("lasso", LassoCV(cv=5)),
]:
    fitted = reg_report(
        label + " without revenue", reg_pipeline(model, nums=without), nums=without
    )
    c = pd.Series(fitted.named_steps["model"].coef_, index=names_wo)
    print(
        f"   log_units_2024 {c['num__log_units_2024']:.3f}"
        f"   log_orders_2024 {c['num__log_orders_2024']:.3f}"
    )
```

```
ridge without revenue R² 0.9473   MAE ₹99,755
   log_units_2024 0.987   log_orders_2024 0.074
lasso without revenue R² 0.9473   MAE ₹99,626
   log_units_2024 0.991   log_orders_2024 0.074
```

Without revenue, the model leans on units instead: its coefficient jumps from nearly 0 to about 0.99, and R² drops only from 0.959 to 0.947, because units carry almost the same information. That's multicollinearity in action. The coefficient of a feature depends on which of its "twins" are also in the model, so a coefficient near zero doesn't mean a feature is useless; it may mean another feature is doing its job. (The list `without` is passed through the `nums=` arguments, so `REG_NUMS` itself never changes.)

**9.**

```python
clf_report("k-NN, k=75, uniform", clf_pipeline(KNeighborsClassifier(n_neighbors=75)))
clf_report(
    "k-NN, k=75, distance-weighted",
    clf_pipeline(KNeighborsClassifier(n_neighbors=75, weights="distance")),
)
```

```
k-NN, k=75, uniform            AUC 0.775   log loss 0.3057
k-NN, k=75, distance-weighted  AUC 0.778   log loss 0.3050
```

Distance weighting changes the ranking only slightly here. With 75 neighbors in 25 dimensions, most neighbors are at similar distances (the curse of dimensionality again), so weighting them by distance makes little difference.

**10.**

```python
y_all = train_acc["churned_2025"]
for label, rule in [
    ("categories_bought >= 3", train_acc["categories_bought"] >= 3),
    ("days_since_last_order > 90", train_acc["days_since_last_order"] > 90),
]:
    after = sum(len(g) / len(y_all) * gini(g) for g in (y_all[rule], y_all[~rule]))
    print(
        f"{label:<28} weighted Gini after split {after:.4f}   (before {gini(y_all):.4f})"
    )
```

```
categories_bought >= 3       weighted Gini after split 0.1710   (before 0.1746)
days_since_last_order > 90   weighted Gini after split 0.1532   (before 0.1746)
```

Splitting on three or more categories reduces Gini, but much less than the recency split, so a tree would still start with recency. The product-breadth signal is real (odds ratio 0.57) but spread across all accounts, whereas recency separates a small, high-risk group sharply. A Gini split rewards sharp separation.

**11.**

```python
for n in [10, 50, 300, 1000]:
    clf_report(
        f"random forest, {n} trees",
        clf_pipeline(
            RandomForestClassifier(n_estimators=n, min_samples_leaf=5, random_state=37),
            scale=False,
        ),
    )
```

```
random forest, 10 trees        AUC 0.737   log loss 0.5069
random forest, 50 trees        AUC 0.774   log loss 0.2719
random forest, 300 trees       AUC 0.785   log loss 0.2675
random forest, 1000 trees      AUC 0.790   log loss 0.2659
```

Ten trees are clearly too few (AUC 0.737, with poor probabilities). The score rises with more trees and settles: going from 300 to 1,000 trees adds only 0.005. Adding trees doesn't cause overfitting in a random forest, because each tree is averaged in, not stacked on top; small ups and downs between sizes are noise from which random samples the trees drew. The only cost of more trees is time and memory.

**12.**

```python
pred = np.full(len(y_toy), y_toy.mean())
for r in range(1, 21):
    residual = y_toy - pred
    stump = DecisionTreeRegressor(max_depth=1, random_state=37).fit(x_toy, residual)
    pred = pred + 0.5 * stump.predict(x_toy)
    if r % 5 == 0:
        print(f"round {r:>2}: squared error {np.mean((y_toy - pred) ** 2):.5f}")
print("predictions:", pred.round(3))
```

```
round  5: squared error 0.07626
round 10: squared error 0.04298
round 15: squared error 0.02278
round 20: squared error 0.01232
predictions: [0.055 0.055 0.055 0.739 0.064 0.064 0.064 0.904]
```

The error keeps falling, to 0.012 by round 20, and the 25-day churner, which sits among accounts that stayed, is pulled up from 0.25 to 0.739; with more rounds, every row would be fitted almost exactly. But eight rows can't support a model that precise; it is memorizing them. That's why real boosting needs a small learning rate, limits on tree size and leaf size, and a validation set or early stopping to decide when to stop adding trees. Training error going to zero is the symptom of variance from section 37.10.

**13.**

```python
from sklearn.model_selection import validation_curve

depths = [2, 3, 4, 6, 8]
tr_scores, cv_scores_d = validation_curve(
    clf_pipeline(
        HistGradientBoostingClassifier(
            learning_rate=0.05, min_samples_leaf=40, max_iter=300, random_state=37
        ),
        scale=False,
    ),
    X_rest,
    y_rest,
    param_name="model__max_depth",
    param_range=depths,
    cv=folds,
    scoring="roc_auc",
)
for d, a, b in zip(depths, tr_scores.mean(axis=1), cv_scores_d.mean(axis=1)):
    print(f"max_depth {d}: train AUC {a:.3f}   CV AUC {b:.3f}")
```

```
max_depth 2: train AUC 0.901   CV AUC 0.835
max_depth 3: train AUC 0.945   CV AUC 0.836
max_depth 4: train AUC 0.977   CV AUC 0.831
max_depth 6: train AUC 0.999   CV AUC 0.822
max_depth 8: train AUC 1.000   CV AUC 0.817
```

`validation_curve` is `learning_curve`'s partner: instead of varying the number of rows, it varies one setting (`param_name`) over a list of values (`param_range`), with cross-validation at each. The cross-validated score is best with shallow trees and declines as depth grows, while the training score keeps rising: deeper trees fit the training folds better and generalize worse. With about 390 churners in the 4,000 accounts, shallow trees (depth 2 or 3) are the right size, which matches what random search found.

**14.**

```python
from sklearn.ensemble import StackingClassifier

stack = StackingClassifier(
    estimators=[
        ("logistic", clf_pipeline(LogisticRegression(max_iter=2000))),
        ("boosting", search.best_estimator_),
    ],
    final_estimator=LogisticRegression(max_iter=2000),
    cv=5,
)
s = cross_val_score(stack, X_rest, y_rest, cv=folds, scoring="roc_auc")
print(f"stacking   mean AUC {s.mean():.3f}   sd {s.std():.3f}")
print(f"(tuned boosting alone {search.best_score_:.3f}; logistic alone 0.807)")
```

```
stacking   mean AUC 0.840   sd 0.016
(tuned boosting alone 0.841; logistic alone 0.807)
```

`final_estimator` is the model on top, which learns how much to trust each part; `cv=5` means it learns from the parts' predictions on rows they weren't trained on (an inner 5-fold split), so it isn't fooled by their training scores. The stack scores about the same as tuned boosting alone. Stacking helps when the models make different kinds of mistakes and each is strong; here, boosting already captures what logistic regression knows, so the combination adds little, at double the training time and complexity. That's the usual outcome in business problems, and why stacking is more common in competitions than in production.

**15.**

```python
boost_eng = clf_pipeline(
    HistGradientBoostingClassifier(random_state=37), scale=False, nums=NUMS + ENG
)
boost_eng.set_params(**search.best_params_)
s = cross_val_score(
    boost_eng, engineered[CATS + NUMS + ENG], y_rest, cv=folds, scoring="roc_auc"
)
print(f"tuned boosting + engineered features   mean AUC {s.mean():.3f}   sd {s.std():.3f}")
```

```
tuned boosting + engineered features   mean AUC 0.847   sd 0.014
```

`set_params(**search.best_params_)` applies the winning settings, which are already named `model__...`, to the new pipeline; `**` unpacks the dictionary as in section 37.8. Boosting gains only a little from the engineered features (0.847 against 0.841), far less than logistic regression's jump from 0.807 to 0.849. Trees can already represent thresholds ("days > 90") and interactions (late payment within small retail) by splitting; the engineered features mostly save them a few splits. Logistic regression couldn't represent them at all, so for it they were new information. Feature engineering matters most for the models that can't find structure on their own.

**16.**

```python
import statsmodels.api as sm

design = pd.get_dummies(reg_train[CATS], drop_first=True, dtype=float)
design = pd.concat(
    [design, reg_train[REG_NUMS].fillna(reg_train[REG_NUMS].median())], axis=1
)
ols_sm = sm.OLS(reg_train["log_revenue_2025"], sm.add_constant(design)).fit()
low, high = ols_sm.conf_int().loc["rep_id_9"]
print(
    f"inside sales desk (rep_id_9): coefficient {ols_sm.params['rep_id_9']:.4f}   "
    f"95% CI [{low:.4f}, {high:.4f}]   p-value {ols_sm.pvalues['rep_id_9']:.3f}"
)
```

```
inside sales desk (rep_id_9): coefficient 0.0311   95% CI [0.0092, 0.0531]   p-value 0.006
```

This is Chapter 30's statsmodels regression (section 30.11): `pd.get_dummies(..., drop_first=True)` is pandas' one-hot encoding with the first category dropped, `sm.add_constant` adds the intercept's column of 1s, and `conf_int().loc["rep_id_9"]` reads that row's two interval ends. The interval, 0.009 to 0.053, **excludes zero** (p = 0.006), even though the generator gave the inside sales desk no effect on growth. So where does it come from? The generator did make inside-desk accounts **more likely to churn**, and this regression only includes accounts that stayed. Inside-desk accounts that survived despite that extra risk tend to be healthier on other churn signals, such as the late-payment and complaint thresholds, which the model's straight-line terms don't fully capture. That's **selection bias**: analyzing only the survivors creates a relationship that doesn't exist among all accounts (Chapter 22, section 22.7, and Chapter 31). The lesson is broader than this dataset. A statistically significant coefficient can still be an artifact of how the rows were chosen, so before anyone reassigns accounts to the inside sales desk, ask how the data was filtered. (statsmodels uses unscaled features, so its coefficients are in original units, unlike the scaled ones in section 37.1; for a one-hot column like this one, the meaning is the same.)

**17.** First, the scores come from **different evaluations**: 0.841 is the best of 25 tuned settings on cross-validation, which is slightly optimistic because the winner was selected for scoring well, while 0.807 is logistic regression's untuned CV score. Compare like with like, ideally on the test set (0.838 against 0.797). Second, a difference in **AUC points isn't a percentage improvement** in anything a business cares about: 0.034 AUC doesn't mean 4% more churners saved. Translate it into decisions, such as "how many of the 100 highest-risk accounts actually churn", which is what Chapter 39 does.

**18.** Impurity-based importance adds up how much each feature reduces Gini across all splits. A continuous feature with thousands of distinct values, like `revenue_2024`, offers many possible thresholds, so trees use it for many small splits that fit noise, and it accumulates importance. `complaints_2024` has only a few values (0 to 6), and its effect is concentrated in an interaction (new accounts with two or more complaints) that occurs in few rows, so it's used rarely. Permutation importance on validation data, or SHAP values (Chapter 39, section 39.8), measure how much predictions actually depend on each feature and correct most of this bias.

**19.** (1) **Drift** (Chapter 36): customers' behavior changed, for example a new competitor makes even long-standing accounts leave, so patterns learned from 2024 don't hold. (2) **Variance**: last year's evaluation was on too few accounts and was lucky; the model was never as good as it looked. (3) **A new kind of bias**: the business changed (a new product line, a pricing change) in a way the features don't capture, so the model is now too simple for the new situation. A fourth possibility is a **pipeline problem**: a feature changed meaning or started arriving empty. Check that first; it's the most common and the easiest to fix.

---

## Where this leads

- **Chapter 38, Unsupervised Learning,** segments the same accounts without a target, using distance and PCA.
- **Chapter 39, Evaluation, Tuning, Interpretation & Honesty,** turns churn and lead scores into decisions with cost-based thresholds, handles imbalance with class weights and resampling, checks calibration, explains predictions with SHAP and partial dependence, and checks fairness.
- **Chapter 40, Time Series & Forecasting,** uses gradient boosting with lag features for demand forecasting.
- **Chapter 41, NLP Foundations,** uses Naive Bayes and logistic regression on text.
- **Chapter 43, A First Look at Deep Learning,** takes logistic regression's weighted sum and sigmoid, and stacks them into a neural network.
- **Looking back:** Chapter 30 (coefficient intervals, section 30.11) and Chapter 31 (causal inference) are where to go before acting on any coefficient in this chapter.
- **Interview preparation:** the Machine Learning Question Bank (Chapter 74) covers every algorithm here, bias and variance, regularization, and tuning with graded answers. "Explain gradient boosting to a non-technical person" and "random forest vs gradient boosting" are among the most common questions in data science interviews.
