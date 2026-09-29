# Chapter 44. Capstone: An End-to-End Data Science Project

*Part 4 — Machine Learning & Data Science*

> **Chapter at a glance**
>
> **You will learn to:** walk one business question through the whole Part 4 lifecycle — frame, prepare, model, evaluate, and communicate — without skipping a stage · turn a model's probability into rupees, and see why ranking by probability alone can miss most of the value · decide which accounts are worth a call at all, and which are worth it first · split an analysis into small reusable functions, so the model is fitted once and the list can be rebuilt with one line · write a one-page, non-technical summary that a leader can act on, and know what belongs in it and what doesn't.
>
> **Before you start:** this chapter assumes everything from Chapters 35–43, and Chapter 30's experiments. It does not re-teach any of it; it uses it. If a step feels unfamiliar, the chapter says which earlier chapter and section taught it, so you can go back rather than guess.
>
> **Time needed:** 5–7 hours to read the chapter, re-run the code, and do exercises 1–4. The project, your own end-to-end pass, is another 6–10 hours.
>
> **Tools:** Python with pandas, scikit-learn and shap, installed in Chapters 18, 35 and 39 — nothing new.
>
> **Practice data:** Riverstone's customer accounts (Chapter 37): the same 5,000 accounts, the same churn target, the same split. Every number in this chapter was calculated, and every output shown is real.

---

## Why this matters

Every chapter in Part 4 taught one skill in isolation: a split, a model, a metric, an explanation. Real work rarely arrives in those tidy pieces. Someone asks a vague question, the data needs assembling, a dozen small decisions have to be made in order, and at the end somebody who has never heard of a confusion matrix needs to know what to do differently on Monday morning.

This chapter is one worked pass through that whole arc, start to finish, on a single question: ***which of Riverstone's at-risk accounts should the sales team call this month, and why those and not others?*** Nothing here is a new technique. What's new is the order, the joins between stages, and one habit most tutorials skip entirely: turning a probability into a decision that accounts for how much is actually at stake.

---

## In plain English

**Imagine a doctor doing a batch of check-ups with a limited number of follow-up appointments to hand out.**

A model that says "this patient has a 40% chance of a problem" is useful, but it's not yet a plan. Two patients might both sit at 40%: one whose problem, if missed, is minor, and one whose problem, if missed, is serious. Handing out follow-ups by risk percentage alone would treat those two patients identically. Handing them out by **risk times what's actually at stake** would not. That's the shift this chapter makes to Riverstone's churn model: a probability becomes a *decision* only once it's weighed against the size of the account behind it.

---

## 44.1 The question, and the plan

*"Which at-risk accounts should the sales team call this month?"*

That's a business request, not yet a data science question. Chapter 36 (section 36.1) taught five things to pin down before touching data; this project adds a sixth:

| Decision | This project |
|---|---|
| Unit of analysis | One customer account |
| Target | Will this account place no order in 2025? (Chapter 37's `churned_2025`) |
| Prediction moment | 31 December 2024 |
| Allowed information | Only account data recorded by 31 December 2024: no 2025 orders, no complaints logged after the cut-off |
| Success measure | Rupees of expected gross margin the call list targets, against the cost of the calls |
| Capacity (new here) | The sales team can make 40 retention calls this month |

The plan, in the order the rest of the chapter follows it:

1. **Refit** Chapter 37's churn model, check that its probabilities are honest, and score the untouched test accounts once.
2. **Turn each account's probability into rupees**: how much margin is at risk, not just how likely the account is to leave; and decide which accounts are worth a call at all.
3. **Build the call list** from that value, not from probability alone, and see how much it differs.
4. **Explain** two accounts on the list well enough that a sales executive could open the call with something specific to say.
5. **Wrap the steps in two small functions**, so the model is fitted once and the list can be rebuilt with one line.
6. **Write the one-page summary** a non-technical leader actually receives.

---

## 44.2 Refitting the model (a recap, not a re-teach)

### Setting up

Open a terminal (Chapter 26, section 26.0), go to your copy of the companion files, then into `companion/ch44/`, and activate your virtual environment (Chapter 17). The code reads `../accounts/accounts.csv`, Chapter 37's accounts file. If it isn't there, run `python ../generate_riverstone_accounts.py` from this folder; the generator is seeded, so it writes the same 5,000 accounts every time. scikit-learn was installed in Chapter 35 (section 35.9) and shap in Chapter 39 (section 39.8), so there is nothing to install. Start `jupyter lab`, open a new notebook, and run the cells below in order.

### The data and the split

First, the accounts and Chapter 37's split (section 37.0), unchanged:

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

accounts = pd.read_csv("../accounts/accounts.csv")
accounts["rep_id"] = accounts["rep_id"].astype(str)
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

rest, test_acc = train_test_split(
    accounts, test_size=0.2, random_state=37, stratify=accounts["churned_2025"]
)
train_acc, valid_acc = train_test_split(
    rest, test_size=0.25, random_state=37, stratify=rest["churned_2025"]
)
print(f"train {len(train_acc):,}   valid {len(valid_acc):,}   test {len(test_acc):,}")
```

```
train 3,000   valid 1,000   test 1,000
```

**How it works:** every line is Chapter 37's (section 37.0): `rep_id` becomes text because a rep number is a label, not a quantity; `CATS` and `NUMS` name the four categorical and eleven numeric columns, all known on 31 December 2024; and the two splits give the same 3,000 training, 1,000 validation and 1,000 test accounts: `test_size=0.2` holds out a fifth for testing, `test_size=0.25` takes a quarter of the remaining 4,000 for validation, `stratify=` keeps the 9.7% churn rate in every part, and `random_state=37` fixes the shuffle. If any of that reads unfamiliar, go back to Chapter 37 before continuing.

### The model

Next, the model: Chapter 37's gradient boosting with its hand-set settings (section 37.8), in Chapter 37's pipeline with the scaler left out, as `clf_pipeline(..., scale=False)` did (trees don't need scaling). Chapter 39 (section 39.8) rebuilt the same model the same way. This time it goes inside a function, so section 44.6 can build it again without retyping it:

```python
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def make_churn_model(cats, nums):
    prepare = ColumnTransformer(
        [
            ("cat", OneHotEncoder(handle_unknown="ignore"), cats),
            ("num", SimpleImputer(strategy="median", add_indicator=True), nums),
        ]
    )
    booster = HistGradientBoostingClassifier(
        learning_rate=0.05, max_depth=3, min_samples_leaf=40, max_iter=300, random_state=37
    )
    return Pipeline([("prepare", prepare), ("model", booster)])


model = make_churn_model(CATS, NUMS)
model.fit(train_acc[CATS + NUMS], train_acc["churned_2025"])
valid = valid_acc.copy()
valid["p_churn"] = model.predict_proba(valid[CATS + NUMS])[:, 1]
print(f"validation AUC: {roc_auc_score(valid['churned_2025'], valid['p_churn']):.3f}")
```

```
validation AUC: 0.786
```

**How it works:**

- `make_churn_model(cats, nums)` returns a **fresh, unfitted** pipeline: one-hot encoding for the categories (`handle_unknown="ignore"` gives a category the model never saw all zeros instead of an error), median filling for the numbers with `add_indicator=True` adding a "was blank" column (Chapter 36, section 36.8), then boosting with Chapter 37's four settings: `learning_rate=0.05` (small steps), `max_depth=3` (shallow trees), `min_samples_leaf=40` (no tiny leaves) and `max_iter=300` (300 rounds). The column lists come in as arguments, so the function doesn't depend on names defined elsewhere in the notebook.
- `model.fit(...)` learns from the 3,000 training accounts only.
- `valid = valid_acc.copy()` makes a separate table, so adding columns doesn't touch `valid_acc`. `valid["p_churn"] = ...` **adds a column** holding each account's predicted churn probability (`[:, 1]` is the "churned" column of `predict_proba`, Chapter 36, section 36.4), so every later step sees each account's score next to its other columns.

**Reading it.** The validation AUC is the same as Chapter 37's "HistGradientBoosting tuned" result: this is the same model on the same accounts.

### Are the probabilities honest?

Section 44.3 will multiply each probability by rupees. Chapter 39 (section 39.4) said calibration matters "whenever the probability is used as a number", so check it before using it. Before you run this, predict: will the average predicted probability be close to the 9.7% of validation accounts that actually churned?

```python
from sklearn.calibration import calibration_curve

print(
    f"mean predicted {valid['p_churn'].mean():.1%}   "
    f"actually churned {valid['churned_2025'].mean():.1%}"
)
actual, predicted = calibration_curve(
    valid["churned_2025"], valid["p_churn"], n_bins=5, strategy="quantile"
)
print("predicted  actual   (5 bins of 200 accounts)")
for p, a in zip(predicted, actual):
    print(f"{p:>9.1%}  {a:>6.1%}")
```

```
mean predicted 8.9%   actually churned 9.7%
predicted  actual   (5 bins of 200 accounts)
     0.5%    3.0%
     1.7%    2.5%
     3.5%    4.5%
     7.6%    8.5%
    31.3%   30.0%
```

**How it works:** `calibration_curve` is Chapter 39's reliability table (section 39.4). It returns the actual churn rate in each bin first, then the average prediction, so the names `actual, predicted` follow its order. `n_bins=5` asks for five bins and `strategy="quantile"` gives each the same number of accounts (200), sorted from the lowest predictions to the highest, and the loop prints each bin as one row.

**Reading it.** The average prediction is within a point of the actual rate, and every bin is close: the accounts given about 31% churned at about 30%. The probabilities are honest enough to multiply by rupees. If they weren't, Chapter 39's `CalibratedClassifierCV` (section 39.4) would be the next step.

### The test set, once

One more evaluation step, done once, as Chapter 37 (section 37.11) did for its finalists: refit the same settings on all 4,000 non-test accounts and score the 1,000 test accounts. This hand-set model wasn't one of section 37.11's three finalists, so this is its only look at them.

```python
final_check = make_churn_model(CATS, NUMS)
final_check.fit(rest[CATS + NUMS], rest["churned_2025"])
p_test = final_check.predict_proba(test_acc[CATS + NUMS])[:, 1]
test_auc = roc_auc_score(test_acc["churned_2025"], p_test)
print(f"test AUC: {test_auc:.3f}")
```

```
test AUC: 0.829
```

**How it works:** `make_churn_model` builds a second, separate pipeline; it learns from `rest` (training plus validation) and is scored on `test_acc`, which nothing in this chapter has used before. `test_auc` keeps the number for the summary in section 44.7.

**Reading it.** On accounts it has never seen, the model ranks a random churner above a random stayer about 83% of the time. That's the figure to quote, and nothing below is allowed to change the model because of it.

---

## 44.3 From probability to rupees

A probability alone doesn't say what to do. Riverstone loses far more by ignoring a large wholesale account with a modest churn risk than by ignoring a small retailer who's almost certain to leave. The fix is to multiply the probability by what the account is worth.

**The plan in words:** for each account, take its churn probability, multiply by its 2024 revenue, then multiply by the share of that revenue Riverstone keeps as gross profit (its margin). The result is the **expected margin at risk**: the gross margin Riverstone should expect to lose from that account if nothing is done.

> expected margin at risk = P(churn) × 2024 revenue × margin

```python
CALL_COST = 1500  # ₹ for one retention call and its follow-up: Chapter 39's WORK_COST
MARGIN = 0.15  # gross margin, the same assumption Chapter 39 used

valid["margin_at_risk"] = valid["p_churn"] * valid["revenue_2024"] * MARGIN
columns = ["account_id", "segment", "revenue_2024", "p_churn", "margin_at_risk"]
first_three = valid[columns].head(3).round({"p_churn": 3, "margin_at_risk": 0})
print(first_three.astype({"revenue_2024": int, "margin_at_risk": int}).to_string(index=False))
total = valid["margin_at_risk"].sum()
print(f"\nexpected margin at risk, all {len(valid):,} validation accounts: ₹{total:,.0f}")
```

```
 account_id     segment  revenue_2024  p_churn  margin_at_risk
       7881      Retail         80400    0.060             726
       8530 Hospitality        185500    0.060            1682
       5016      Retail        264800    0.114            4544

expected margin at risk, all 1,000 validation accounts: ₹3,174,893
```

**How it works:**

- `CALL_COST` and `MARGIN` are named constants, not numbers buried in a formula: Chapter 39's habit (section 39.5) of writing business assumptions as variables a reader can see, question, and change. `CALL_COST` is Chapter 39's `WORK_COST`, ₹1,500 for about two hours of a sales executive's time; we assume a retention call with its follow-up costs about the same as working a lead.
- `valid["p_churn"] * valid["revenue_2024"] * MARGIN` multiplies two columns and a number, row by row, for all 1,000 accounts in one line: pandas column arithmetic (Chapter 18, section 18.5), the same **element-by-element arithmetic** Chapter 35 did with NumPy arrays.
- `.round({"p_churn": 3, "margin_at_risk": 0})` rounds each named column to its own number of decimals, so the probabilities show three and the rupees none. `.astype({...: int})` then turns the two rupee columns into whole numbers, so they print without a trailing `.0`.

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `CALL_COST` | Rupees to make one retention call and follow up | 1,500 | Higher: fewer accounts clear the break-even bar below; lower: more do |
| `MARGIN` | Share of revenue that's gross profit, not just turnover | 0.15 (15%) | Higher: every account's margin at risk rises, so more accounts clear the bar; lower: fewer do |

**Reading the output.** Check the first row by hand: 0.060 × ₹80,400 × 0.15 = ₹724; the printed ₹726 uses the unrounded probability. The third account, at ₹2,64,800 of 2024 revenue and an 11.4% churn probability, has ₹4,544 of margin at risk: modest on its own. Add this up across the 1,000 validation accounts and it comes to about ₹31.7 lakh of expected gross margin at risk, which is about ₹2.1 crore of revenue (divide by the 15% margin). These are 20% of Riverstone's accounts, so across all of them it would be roughly five times that.

> **Watch out: two meanings of "value at risk".** In everyday speech, "value at risk" means the expected amount you'd lose, and you'll hear it used that way for lists like this one. Finance uses **VaR** for something different: a worst-case loss at a stated confidence level ("in a bad month, one in twenty, we lose at most ₹X"). To avoid the clash, this chapter says **expected margin at risk**, and means p × revenue × margin.

**The full rule, and the number we don't have yet.** The formula treats a call as if it saved the whole account. A call is really worth making when

> P(churn) × revenue × margin × **save rate** > call cost

where the **save rate** is the share of would-be churners a call actually keeps. For example, p = 0.30, revenue ₹5,00,000, margin 15%, save rate 20%: 0.30 × 5,00,000 × 0.15 × 0.20 = ₹4,500, which is more than ₹1,500, so call. We don't know Riverstone's save rate yet; the experiment in section 44.7's summary is how we'd measure it (Chapter 30). Until then, ranking by expected margin at risk gives the same order, as long as the save rate is about the same for every account.

### Break-even per account

A call is worth making only if what it could save is more than it costs. Chapter 39 (section 39.5) found that point for leads, where every lead had the same value: work a lead when *p* × ₹30,255 > ₹1,500. Here each account has its own value, so the test is per account: **call when the expected margin at risk is more than the call cost**. At ₹1,500 and a 15% margin, that's P(churn) × revenue > ₹10,000.

```python
valid["worth_calling"] = valid["margin_at_risk"] > CALL_COST
print(f"{valid['worth_calling'].sum()} of {len(valid):,} accounts clear break-even")
```

```
447 of 1,000 accounts clear break-even
```

**How it works:** `valid["margin_at_risk"] > CALL_COST` compares every row with ₹1,500 and gives `True` or `False`; the new column keeps the answer. `.sum()` counts the `True` values, because Python counts `True` as 1.

**Reading it.** Fewer than half the validation accounts clear break-even, even before any save rate. With only 40 calls, the capacity will bind long before break-even does; section 44.6 shows where break-even starts to matter.

---

## 44.4 Building the call list: probability isn't the same as value

**A rehearsal, not yet the real list.** We build the list from the 1,000 validation accounts because they're the ones the model didn't learn from and whose 2025 outcome we could check afterwards. That makes this a rehearsal: *what would we have sent on 1 January 2025?* For a real list you would (1) refit the pipeline on all 5,000 labelled accounts, and (2) score every active account using its 2025 figures, as of 31 December 2025. Riverstone's companion data stops at the 2024 features, so this chapter can't show step (2) with real output; section 44.6 builds the ranking so that it works unchanged on such a table.

With only 40 calls available, which 40 accounts? Rank by expected margin at risk, drop any account below break-even, and take the top 40. For comparison, also take the top 40 by probability alone:

```python
CAPACITY = 40  # the sales team's capacity: 40 retention calls this month

eligible = valid[valid["worth_calling"]]
by_value = eligible.sort_values("margin_at_risk", ascending=False).head(CAPACITY)
by_probability = valid.sort_values("p_churn", ascending=False).head(CAPACITY)
overlap = len(set(by_value["account_id"]) & set(by_probability["account_id"]))

print(
    f"ranked by margin at risk:    top {CAPACITY} carry "
    f"₹{by_value['margin_at_risk'].sum():,.0f} of expected margin at risk"
)
print(
    f"ranked by probability alone: top {CAPACITY} carry "
    f"₹{by_probability['margin_at_risk'].sum():,.0f}"
)
print(f"the two lists share only {overlap} of {CAPACITY} accounts")
```

```
ranked by margin at risk:    top 40 carry ₹1,200,524 of expected margin at risk
ranked by probability alone: top 40 carry ₹386,008
the two lists share only 10 of 40 accounts
```

**How it works:**

- `valid[valid["worth_calling"]]` keeps only the rows where the column is `True` (Chapter 18, section 18.4).
- `.sort_values(..., ascending=False).head(CAPACITY)` puts the largest first and keeps 40 rows (Chapter 18).
- `set(...)` turns each list's account numbers into a set, and `&` keeps the numbers that are in both (Chapter 17, section 17.7); `len` counts them.

**Reading it.** Ranking by expected margin at risk targets about **₹12.0 lakh**; ranking by churn probability alone targets about **₹3.9 lakh**, less than a third as much, from the same model and the same 40 calls. The two lists barely overlap: 10 accounts appear on both. This isn't a modelling improvement; the predictions haven't changed at all. It's a **decision** improvement. A probability-only ranking spends the sales team's scarce time on accounts that are *likely* to leave regardless of how little they'd cost Riverstone, and misses large accounts whose departure would be expensive even at a lower probability. This is the most important habit in the chapter: **a score is not a decision until it's weighed against what's at stake**. Chapter 39 (section 39.5) made the same argument with one value for every lead; here the value changes from row to row.

> **Predict before you run this.** Before reading on, guess: will the account at the very top of the list have a *high* or a *moderate* churn probability? Then look at section 44.5's output.

---

## 44.5 Explaining two accounts

A call list with no reason attached is hard for a sales executive to use. Chapter 39 (section 39.8) taught SHAP for exactly this. First, the explainer, and the **base value** every explanation starts from:

```python
import shap

prepare = model.named_steps["prepare"]
feature_names = prepare.get_feature_names_out()
X_valid_prepared = prepare.transform(valid[CATS + NUMS])
explainer = shap.TreeExplainer(model.named_steps["model"])
shap_values = explainer.shap_values(X_valid_prepared)
base = explainer.expected_value[0]
print(f"base value: log-odds {base:.3f} = probability {1 / (1 + np.exp(-base)):.3f}")
```

```
base value: log-odds -3.226 = probability 0.038
```

**How it works:** these lines are Chapter 39's (section 39.8). `named_steps["prepare"]` is the fitted preparation step; `get_feature_names_out()` names its output columns; `transform` prepares the validation accounts without refitting; `TreeExplainer` explains the boosting step, and `shap_values` holds one contribution per account per column, in **log-odds units** (Chapter 37, section 37.3). For this model, shap returns the base value inside a one-item array, so `[0]` takes it out. `1 / (1 + np.exp(-base))` is the sigmoid, which turns log-odds into a probability.

Now the two accounts at the top of the call list. For each, the four largest pushes, and a check that the base value plus *all* the pushes gives the model's prediction:

```python
for label in by_value.index[:2]:
    account = valid.loc[label]
    row_position = valid.index.get_loc(label)
    contributions = pd.Series(shap_values[row_position], index=feature_names)
    largest = contributions.abs().sort_values(ascending=False).head(4).index
    total = base + contributions.sum()
    print(
        f"account {account['account_id']} ({account['segment']}, "
        f"₹{account['revenue_2024']:,.0f} revenue): churn probability {account['p_churn']:.1%}"
    )
    print(contributions[largest].round(3).to_string())
    print(f"base {base:.3f} + all 25 pushes = {total:.3f} -> {1 / (1 + np.exp(-total)):.1%}\n")
```

```
account 7001 (Wholesale, ₹7,966,300 revenue): churn probability 8.2%
num__late_payment_days    0.885
num__avg_discount_pct     0.661
num__complaints_2024      0.501
num__tenure_months       -0.446
base -3.226 + all 25 pushes = -2.416 -> 8.2%

account 8564 (Retail, ₹1,388,500 revenue): churn probability 45.4%
num__late_payment_days    1.311
num__complaints_2024      1.132
num__tenure_months        0.975
num__orders_2024         -0.271
base -3.226 + all 25 pushes = -0.183 -> 45.4%
```

**How it works:**

- `by_value.index[:2]` is the row labels of the first two accounts on the list. `valid.loc[label]` looks the account up by its label (Chapter 18).
- The SHAP array has no labels, only positions: row 0, 1, 2 … in the order of `valid`. `valid.index.get_loc(label)` answers "at what position in `valid` is the row with this label?", which is the row to read from `shap_values`.
- `pd.Series(..., index=feature_names)` labels the account's 25 contributions with the column names. `contributions.abs().sort_values(ascending=False).head(4).index` finds the names of the four largest in size, whatever their sign, and `contributions[largest]` shows them with their signs: positive pushes toward churning, negative toward staying.
- `total` adds the base value and **all** 25 contributions, not just the four shown; the sigmoid turns it back into a probability.

**Reading it.** The account at the very top of the list, a Wholesale account with ₹79,66,300 of 2024 revenue, has a churn probability of only about 8%, below the overall rate. It's first purely because 8% of nearly ₹80 lakh is a large number. Its largest pushes toward churning are late payments (40 days, against a typical 12), a high average discount (11.7%, against about 5%), and two complaints; its long tenure (53 months) pulls the other way. Base −3.226 plus all 25 pushes gives the model's prediction exactly, so the four largest pushes don't tell the whole story: many small ones pull in both directions. SHAP compares this account with the typical account, not with its own past: the data is one snapshot of 2024, so it can't say the payments *got* later. That gives the sales executive a specific, true opening: *"Their payments run later than most accounts', and they get a higher average discount than most — worth asking whether anything's straining the relationship."* The second account is a much riskier retail account (about 45%), pushed up by late payments, three complaints, and being new: 13 months as a customer. An explanation doesn't need to be exhaustive to be useful; it needs to give the caller one true, specific thing to ask about.

---

## 44.6 Two functions, not six steps

Everything so far has been separate cells, run once, by hand. The next stage of any real project is making it **repeatable**. There are two different jobs here, and they change at different speeds:

- **Scoring** needs the fitted model. Fitting is slow and should happen once, when the data changes.
- **Deciding** needs the scores and three settings: the margin, the call cost, and the capacity. A sales head will ask "what if we had 80 calls?" many times, and none of those questions should refit the model.

So: **fit once, decide many times.** `make_churn_model` from section 44.2 already builds the model. Two small functions do the rest.

**The plan in words:** `score_accounts` takes a fitted model and a table of accounts and returns a copy with a `p_churn` column. `make_call_list` takes a scored table and the three settings, works out the expected margin at risk, drops the accounts below break-even, and returns the top of the list and how many accounts were dropped.

```python
def score_accounts(fitted_model, accounts_df):
    scored = accounts_df.copy()
    columns = list(fitted_model.feature_names_in_)
    scored["p_churn"] = fitted_model.predict_proba(scored[columns])[:, 1]
    return scored


def make_call_list(scored, margin=0.15, call_cost=1500, capacity=40):
    scored = scored.copy()
    scored["margin_at_risk"] = scored["p_churn"] * scored["revenue_2024"] * margin
    worth_calling = scored[scored["margin_at_risk"] > call_cost]
    call_list = worth_calling.sort_values("margin_at_risk", ascending=False).head(capacity)
    return call_list, len(scored) - len(worth_calling)


scored = score_accounts(model, valid_acc)
call_list, dropped = make_call_list(scored)
print(
    f"{len(call_list)} accounts on the list, ₹{call_list['margin_at_risk'].sum():,.0f} "
    f"of expected margin at risk; {dropped} accounts below break-even"
)
```

```
40 accounts on the list, ₹1,200,524 of expected margin at risk; 553 accounts below break-even
```

**How it works, line by line:**

- `score_accounts(fitted_model, accounts_df)`: `accounts_df.copy()` works on a copy, so the function never changes the table you passed in. A fitted pipeline remembers the columns it learned from in `feature_names_in_`, so the function reads them from the model instead of from `CATS` and `NUMS` somewhere else in the notebook. The last line is section 44.2's scoring line.
- `def make_call_list(scored, margin=0.15, call_cost=1500, capacity=40):` gives the three settings **default values** (Chapter 17, section 17.8), so it can be called with none of them, or with any of them changed by name.
- Its body repeats section 44.3's calculation with the function's own `margin`, section 44.3's break-even test with its own `call_cost`, and section 44.4's ranking with its own `capacity`.
- `return call_list, len(scored) - len(worth_calling)` sends back two values; `call_list, dropped = ...` unpacks them in the same order (Chapter 17).
- `score_accounts(model, valid_acc)` scores the validation accounts with the model fitted in section 44.2; nothing is refitted.

Everything each function needs comes in through its arguments. That's what makes them safe to copy into another notebook, hand to a colleague, or schedule (Chapter 29, section 29.2). For the real monthly list, the same three lines would read: `model = make_churn_model(CATS, NUMS).fit(...)` on all labelled accounts, `scored = score_accounts(model, current_accounts)` on this month's table, and `make_call_list(scored)`.

**Reading it.** The same 40 accounts and the same total as section 44.4, so the functions reproduce the cells they replace. Now the question a sales head asks: what would more calls buy? Each call to `make_call_list` below takes a moment, because the model isn't refitted:

```python
previous_total, previous_size = 0, 0
for capacity in [20, 40, 80]:
    call_list, _ = make_call_list(scored, capacity=capacity)
    size, total = len(call_list), call_list["margin_at_risk"].sum()
    average = (total - previous_total) / (size - previous_size)
    print(
        f"capacity {capacity:>2}: total ₹{total:>9,.0f}   "
        f"calls {previous_size + 1}-{size}: ₹{average:>6,.0f} each"
    )
    previous_total, previous_size = total, size
```

```
capacity 20: total ₹  892,015   calls 1-20: ₹44,601 each
capacity 40: total ₹1,200,524   calls 21-40: ₹15,425 each
capacity 80: total ₹1,567,814   calls 41-80: ₹ 9,182 each
```

**How it works:** `_` is Python's name for a value you don't need (Chapter 35 used it the same way); here, the count of dropped accounts. `previous_total` and `previous_size` remember the last row, so `average` is the expected margin at risk each *extra* call adds. `size` is the list's real length, which can be shorter than `capacity` if fewer accounts clear break-even.

**Reading it.** Doubling capacity from 40 to 80 calls targets more (₹15.7 lakh against ₹12.0 lakh), about 31% more, not twice as much. The first 20 calls average about ₹44,600 each; calls 21 to 40 about ₹15,400; calls 41 to 80 about ₹9,200. The most valuable accounts are already on a short list, so each extra call is worth less than the one before, and at some length the next account falls below the ₹1,500 break-even. That's the answer to "what if we gave you more calls?", in one line rather than a rebuilt analysis.

> **Changed-line exercise.** In the capacity loop, change `[20, 40, 80]` to `[40, 200, 600]`. Before running it, predict: will the list at capacity 600 have 600 accounts? (Look back at section 44.3's break-even count.) Then check.

---

## 44.7 The one-page summary

Everything above is for you. What a leader receives is shorter, and every number in it must trace back to something computed. Collect them in one cell:

```python
call_list, _ = make_call_list(scored)
revenue_at_risk = (call_list["p_churn"] * call_list["revenue_2024"]).sum()
print(f"test AUC {test_auc:.3f}")
print(
    f"call list: {len(call_list)} accounts, ₹{call_list['margin_at_risk'].sum():,.0f} "
    f"expected margin at risk, ₹{revenue_at_risk:,.0f} expected revenue at risk"
)
print(f"risk-only list: ₹{by_probability['margin_at_risk'].sum():,.0f} expected margin at risk")
print("by segment:", call_list["segment"].value_counts().to_dict())
print(
    f"median 2024 revenue: list ₹{call_list['revenue_2024'].median():,.0f}, "
    f"all validation accounts ₹{scored['revenue_2024'].median():,.0f}"
)
```

```
test AUC 0.829
call list: 40 accounts, ₹1,200,524 expected margin at risk, ₹8,003,494 expected revenue at risk
risk-only list: ₹386,008 expected margin at risk
by segment: {'Wholesale': 17, 'Retail': 13, 'Hospitality': 10}
median 2024 revenue: list ₹744,350, all validation accounts ₹222,850
```

**How it works:** `revenue_at_risk` is the same sum without the margin: probability × revenue, for the revenue the list's accounts are expected to take with them. `value_counts()` counts the accounts in each segment, and `.to_dict()` prints the counts as a dictionary (Chapter 18). `median` is the middle value (Chapter 21).

That table of numbers becomes a page of prose, not a slide of metrics:

> **To:** Anita Rao, Sales Head
>
> **From:** Analytics
>
> **Re:** Pilot: retention call list (rehearsed on 2025 outcomes)
>
> **Recommendation:** each month, call the 40 accounts with the most gross margin at risk, not the 40 most likely to leave. Rehearsed on a fifth of our accounts as they stood at the end of 2024, the 40 accounts on this list carry about **₹12.0 lakh** of expected gross margin at risk (roughly **₹80 lakh** of revenue) if nothing changes. A list ranked by risk alone would have targeted about **₹3.9 lakh** of margin at risk: the same number of calls, less than a third of the value targeted.
>
> **How much to trust it:** on accounts it had never seen, the model picks out the account that leaves from a pair (one that leaves, one that stays) about 83% of the time. A solid, usable model, not a perfect one.
>
> The list skews toward larger accounts: its median 2024 revenue is **₹7,44,350**, against **₹2,22,850** for a typical account. That's intended; the list exists to catch valuable accounts a simple risk ranking would miss. It does mean the smaller, high-risk accounts need a separate, lower-touch process (an email campaign, say) rather than a personal call.
>
> By segment, the list is 17 Wholesale, 13 Retail, and 10 Hospitality accounts. Each sales executive will get their own accounts flagged with the two or three factors driving that account's risk, so every call opens with something specific rather than a generic "how's everything going?"
>
> **What this list is not:** proof that calling these accounts will keep them. It estimates what's at risk if nobody calls. Whether calls change the outcome, and by how much, is a question for a proper test (Chapter 30): call a random half of a larger list, and compare how many accounts in each half keep ordering. We recommend running that test before scaling this to every account every month.

Notice what's there and what isn't. The decision comes first; the model's quality appears once, in plain words, with no metric name; there is no code, no confusion matrix, and no mention of gradient boosting or SHAP. The reader needs to know what to do and how confident to be, not how it was built. The **limitations paragraph is not optional**: a summary that only reports the upside is the kind of overclaiming Chapters 22, 30 and 39 warned against.

---

## 44.8 The Part 4 toolkit, applied

Here is where each step came from:

| Chapter | What it contributed here |
|---|---|
| 35 | Probability thinking and log loss (section 35.9); element-by-element arithmetic on whole columns (section 35.1) |
| 36 | The framing table (section 36.1), the train/validation/test split (section 36.3), pipelines (section 36.9), and the leakage rule that every feature must be known at the prediction moment (section 36.7) |
| 37 | The accounts, the split and the gradient-boosting model with its settings (sections 37.0 and 37.8); scoring the test set once (section 37.11) |
| 39 | The calibration check (section 39.4), break-even from costs (section 39.5), and SHAP for one prediction (section 39.8) |
| 42 | Judging a ranked list by what's at the top of it, as precision@k does (section 42.3), applied to a call list instead of a product list |
| 43 | The decision to stay with gradient boosting: on tabular data like this, a neural network wasn't worth its complexity (section 43.8) |
| 30 | The experiment the summary recommends, to measure whether calls work |
| 38, 40, 41 | Not needed for this question. Clustering, forecasting and text are the right tools for other questions; a capstone uses what its question needs, and that's normal |

Nothing here required a new algorithm. It required using the ones already learned, in the right order, without skipping the step that turns a number into a decision.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Ranking purely by model probability | Large, moderately at-risk accounts never make the list | Multiply probability by what's actually at stake |
| Calling margin "revenue", or "at risk" "protected" | A leader reads a figure several times too large, or as money already saved | Say which quantity it is (margin or revenue) and that it's at risk, not saved |
| Treating the call list as proof calls work | "We'll definitely save this revenue" | State plainly that this is an estimate of risk, not a measured effect (Chapter 30) |
| A summary full of model metrics | The reader can't find the actual recommendation | Lead with the decision; state the model's quality once, in plain words |
| No cost or capacity constraint | A list of thousands, useless to a team that can make 40 calls | Tie the list to a real capacity and a real cost |
| Refitting the model to change a setting | Every "what if" takes minutes and risks small differences between runs | Fit once, then decide many times, as section 44.6 does |
| No limitations section | Leadership overtrusts the list | Always state what the model does not prove |

---

## In the real world: what happened to the call list

Meera shows the rehearsal list to Anita and her three field sales executives. Farah, looking at her Wholesale accounts, questions one immediately: a large account flagged for late payments. "That's their plant shutdown," she says. "They told me in January; the payments were late for a few months and they're normal again now."

That's not a flaw in the list; it's exactly why the list is a starting point for a conversation, not a verdict. The model has no way to know about a plant shutdown it was never shown. Farah's local knowledge and the model's account-wide pattern-matching do different jobs, and the useful outcome is combining them: for the first real list, Farah still makes the call, but she opens it with the shutdown, not the payments. Anita agrees to the test the summary recommended, so that in a few months Riverstone will have its first evidence of whether calling changes anything at all.

---

## Project: your own end-to-end pass

**Goal:** run this chapter's six-step lifecycle on a question of your own, ending in a one-page summary someone outside data science could act on.

### Tools you'll need

Nothing new. Every tool used in this chapter (pandas, scikit-learn's pipeline and gradient boosting, `calibration_curve`, shap's `TreeExplainer`) was introduced and explained in Chapters 18, 36, 37 and 39.

**Steps:**

1. Pick a question with a real decision behind it and a real constraint (a budget, a headcount, a number of hours) — not just "predict X."
2. Frame it with Chapter 36's five rows (unit, target, prediction moment, allowed information, success measure), and add a sixth for capacity.
3. Reuse a model you've already built in this part rather than building a new one from scratch. Check its calibration if you'll use its probabilities as numbers, and score its test set once.
4. Turn its output into a value, not just a probability or a score, and set a break-even rule from a stated cost.
5. Write the fitting and the deciding as separate functions, and show one "what if we changed the capacity or cost" result with real numbers.
6. Explain two individual cases well enough that someone could act on them immediately.
7. Write the one-page summary, leading with the decision and including a limitations paragraph that isn't an afterthought.

---

## Recap

- A **probability is not a decision**. Multiplying it by what's at stake (the expected margin at risk) can completely reorder a priority list, as it did here: three times the value targeted, from the same model and the same 40 calls.
- Before using probabilities as numbers, **check calibration**; before quoting a model's quality, **score the test set once**.
- **Capacity and cost constraints** belong in the analysis from the start: break-even says which accounts are worth a call at all, capacity says how many you can make.
- **Fit once, decide many times**: separate the slow step (fitting) from the fast one (ranking), and pass every setting in as an argument.
- A **one-page summary** leads with the decision, states the model's quality once in plain words, says which quantity each rupee figure is, and always includes what the analysis does *not* prove.
- An end-to-end project is not a new skill; it's the discipline of using Chapters 35–43's tools in the right order and not skipping the step that turns a number into an action.

---

## Key terms

expected margin at risk · save rate · break-even per account · capacity constraint · rehearsal (back-test) · fit once, decide many times · default argument · executive summary · limitations statement

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can name, for any model I've built, what decision it actually feeds — not just what it predicts.
- [ ] I never rank purely by probability when the things being ranked have different value.
- [ ] I can say whether a rupee figure is revenue or margin, and expected or saved.
- [ ] I can separate fitting from deciding, and write each as a function with sensible defaults.
- [ ] I write a one-page summary that leads with the decision, not the metric, and always states a limitation.
- [ ] I can point to which earlier chapter taught any given step in my own pipeline.

---

## Exercises

Code exercises run in the same notebook, after the chapter's code: they use `scored`, `make_call_list` and the constants. Predict each answer before running it.

1. *(hand)* An account has a 30% churn probability and ₹5,00,000 in 2024 revenue. At a 15% margin, what's its expected margin at risk? Is it worth a ₹1,500 call by section 44.3's break-even rule? Would it still be worth it with a save rate of 10%?
2. Call `make_call_list(scored, margin=0.25)`. Does the same set of 40 accounts appear as at 0.15? Does the number of accounts below break-even change? Why might margin differ by segment in reality, and what would that do to the list?
3. Call `make_call_list(scored, call_cost=15000)`. How long is the list now, and why isn't it 40? What does that tell you about the difference between *ranking* by value and *filtering* by break-even?
4. Write the one-paragraph "what this list is not" limitation section for your own project from this chapter's project brief. What is the one thing a reader might wrongly conclude from your summary if you left that paragraph out?

---

## Answers

**1.** Expected margin at risk = 0.30 × ₹5,00,000 × 0.15 = **₹22,500**. That's well above the ₹1,500 call cost, so yes, it clears section 44.3's break-even rule. With a 10% save rate the expected gain from a call is ₹22,500 × 0.10 = ₹2,250, still above ₹1,500, so still worth calling, but only just.

**2.**

```python
list_25, dropped_25 = make_call_list(scored, margin=0.25)
list_15, dropped_15 = make_call_list(scored, margin=0.15)
same = set(list_25["account_id"]) == set(list_15["account_id"])
print(f"same 40 accounts at margin 0.25 and 0.15? {same}")
print(f"below break-even: {dropped_25} at 0.25, {dropped_15} at 0.15")
```

```
same 40 accounts at margin 0.25 and 0.15? True
below break-even: 399 at 0.25, 553 at 0.15
```

The same 40 accounts appear either way. Margin multiplies every account's margin at risk by the same number, so it stretches the whole scale without changing anyone's position: the **ranking** is unaffected, though the rupee figures in the summary change. But margin *does* change who clears break-even: at 25%, 601 accounts are worth a call instead of 447 (399 fall below break-even instead of 553), because ₹1,500 is now a smaller share of each account's value. In reality, margin differs by segment (wholesale often runs thinner margins than hospitality, say). One margin for every account then distorts the ranking, favouring segments whose margin is overstated. A more careful version would use each segment's own margin.

**3.**

```python
list_high_cost, dropped_high_cost = make_call_list(scored, call_cost=15000)
print(f"call list at a ₹15,000 call cost: {len(list_high_cost)} accounts")
print(f"lowest expected margin at risk on it: ₹{list_high_cost['margin_at_risk'].min():,.0f}")
```

```
call list at a ₹15,000 call cost: 31 accounts
lowest expected margin at risk on it: ₹15,048
```

At a ₹15,000 call cost, only 31 accounts clear break-even, so the list stops at 31, not 40: the other 9 of the top 40 by value wouldn't pay for their call **even if every call saved the account**, and with a realistic save rate still fewer would. **Ranking** by expected margin at risk answers "which accounts matter most, relative to each other?"; **filtering** by break-even answers a different question, "which accounts are worth acting on at all, given what it costs to act?" A sensible list applies both, which is why `make_call_list` filters before it ranks.

**4.** *(No single correct answer — this asks you to write your own project's limitations paragraph.)* Whatever the project, the paragraph should separate what the analysis shows (a risk estimate, a ranking, a pattern in past data) from what it does not prove (that acting on it changes the outcome, that the pattern will hold as conditions change, that no other factor explains what the model found). Without it, the most common wrong conclusion is treating a **correlational risk score** as if it were a **measured effect of taking action** — exactly the gap this chapter's own summary calls out in its final paragraph, and exactly what a proper experiment (Chapter 30) is needed to close.

---

## Where this leads

This chapter closes Part 4. The call list is a one-off analysis on last year's file; running it every month needs fresh data and a model that survives outside a notebook. Part 5 (Chapters 45–52) builds the data systems that would feed this model fresh accounts every month: ingestion (Chapter 45), pipelines and scheduling (Chapter 46), and data quality (Chapter 47). Part 6 takes the model itself into production: MLOps, deployment and drift monitoring (Chapter 56). And whether a retention call actually works is an experiment, the Chapter 30 test the summary recommends.
