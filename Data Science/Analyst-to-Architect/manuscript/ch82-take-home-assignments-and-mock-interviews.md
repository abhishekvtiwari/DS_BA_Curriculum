# Chapter 82. Take-Home Assignments & Mock Interviews

*Part 8 — The Interview Playbook*

> **Chapter at a glance**
>
> **You will learn to:** judge whether a take-home assignment is fair before you start it · complete a take-home the way a strong candidate actually would, not just technically correctly, but with the judgment and communication a reviewer is scoring · sit through a realistic mock interview and hear what a strong answer and a weaker one sound like at the same turn · read interviewer scoring notes and understand what actually moved the score.
>
> **Before you start:** Chapter 69 (the five-dimension rubric and the twelve extra-point tags). The take-homes use SQL from Chapters 12 and 13, the lead model from Chapters 36, 37 and 39, and the pipeline ideas from Chapters 45–47. The mocks draw on the banks in Chapters 71, 74, 76A, 76B, 77 and 81. This chapter rehearses those skills; it doesn't teach them again, and each section says where each one is taught.
>
> **Time needed:** 2–3 hours to read the chapter and run every query and cell; about 10–12 hours if you also do all three take-homes against the clock (2 + 3 + 2 hours), compare them with the scoring tables, and record one mock.
>
> **How this chapter is built.** Three complete take-homes and three scored mock interviews, one each for Data Analyst, Data Scientist and Data Engineer. Business analysts can adapt the Data Analyst take-home using Chapter 76B's elicitation questions; automation and BI candidates can adapt the Data Engineer one. Each take-home gives the assignment as a candidate would receive it, a model submission, a scoring table and what a weak submission looks like. **Every model submission was actually run:** the SQL on PostgreSQL 16 against the Riverstone databases, the Python on Python 3.11.15 with scikit-learn 1.9.1 (the book recommends Python 3.14, Chapter 17, section 17.0; nothing here depends on the version), and every output shown is the real one. The mocks are condensed transcripts: each long answer is written out once, in full, and each mock shows a weaker answer next to the stronger one at two of its turns, with Chapter 69's scores and tags.

---

## 82.0 Before you start: is this a fair take-home?

A take-home is unpaid work, so judge it before you begin. Chapter 8 promised this chapter would show what a fair one looks like.

**A fair take-home has:**

- a stated time limit, usually no more than about 4 hours;
- synthetic or public data, or a sample prepared for the exercise;
- a clear deliverable ("a one-page summary plus the queries"), and a named person to send questions to.

**Warning signs:**

- an open-ended brief such as "build our churn feature" or "redesign our pipeline";
- the company's real client data, or a problem that looks like their live backlog;
- no time limit, or an estimate of several days of unpaid work.

**What to do:**

- Ask for scope clarification **in writing**, early: "Should I assume X, or Y?" A reviewer reads that as good judgment, not weakness.
- Say how long you spent, at the top of your submission.
- It's fine to deliver the time-boxed version with a "what I'd do next" list, exactly as the Data Engineer submission in section 82.3 does. Over-delivering on a fair take-home rarely changes the result; over-delivering on an unfair one teaches the company that you'll work for free.

All three assignments below pass this test: each has a time limit, practice data from this book, and a one-page deliverable.

---

<!-- db: riverstone_2025 -->

## 82.1 Take-home assignment: Data Analyst

### The assignment, as given

> "Riverstone's sales leadership wants to understand which product categories are driving growth and which need attention. Using the attached order data, prepare a short analysis (a one-page summary plus supporting queries/code) answering: which categories are performing best and worst, what's driving the difference, and one specific recommendation. You have 2 hours."

**Practice data:** `riverstone_2025` (Chapter 13, section 13.1): all of 2025, 24 customers, 175 orders, 173 of them not cancelled.

### Model submission

**Step 1: the core numbers.** Revenue, orders and customers by category, leaving out cancelled orders:

```sql
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 2) AS revenue,
       COUNT(DISTINCT o.order_id)    AS orders,
       COUNT(DISTINCT o.customer_id) AS customers
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
JOIN products    AS p  ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY revenue DESC;
```

```
  category  |  revenue   | orders | customers
------------+------------+--------+-----------
 Storage    | 2297973.50 |    142 |        23
 Kitchen    | 1208030.00 |     85 |        16
 Industrial |  795830.00 |     23 |         5
 Furniture  |   33637.50 |      2 |         2
(4 rows)
```

- The revenue formula is Chapter 12's (section 12.9): quantity × price charged × (1 − discount). `ROUND(…, 2)` keeps two decimals; without it PostgreSQL prints the raw result of the division, with twenty decimal places.
- `COUNT(DISTINCT …)` counts each order and each customer once, however many lines they have (the fan-out trap, section 12.10).
- **Check it reconciles:** the four revenues add up to ₹43,35,471, Riverstone's 2025 revenue (Chapter 10). The order counts add up to 252, more than the 173 orders, because most orders contain more than one category. So "orders" here means *orders that include this category*.
- Industrial's 23 orders come from only **5 customers**.

**Step 2: one level deeper, checking whether Industrial's smaller order count is offset by more spend per order.** A first attempt averaged per order *line*, not per order: silently the wrong grain. The fix is to add up each order's spend in the category first, then average those order totals:

```sql
WITH order_category_revenue AS (
  SELECT o.order_id,
         p.category,
         SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
  FROM orders AS o
  JOIN order_items AS oi ON o.order_id = oi.order_id
  JOIN products    AS p  ON oi.product_id = p.product_id
  WHERE o.status <> 'Cancelled'
  GROUP BY o.order_id, p.category
)
SELECT category,
       ROUND(AVG(order_revenue), 2) AS avg_category_spend_per_order,
       COUNT(*) AS n_orders
FROM order_category_revenue
GROUP BY category
ORDER BY avg_category_spend_per_order DESC;
```

```
  category  | avg_category_spend_per_order | n_orders
------------+------------------------------+----------
 Industrial |                     34601.30 |       23
 Furniture  |                     16818.75 |        2
 Storage    |                     16182.91 |      142
 Kitchen    |                     14212.12 |       85
(4 rows)
```

- The CTE (Chapter 13, section 13.2) makes one row per order and category; the outer query averages those rows. Averaging order-level totals, not lines, is the grain rule from Chapter 12, section 12.12.
- The column name says what it is: the spend on *this category's items* in an order that includes it, not the size of the whole basket.
- **Check it agrees with Step 1:** ₹22,97,973.50 ÷ 142 = ₹16,182.91 ✓, and ₹7,95,830 ÷ 23 = ₹34,601.30 ✓.

**Step 3: growth, which is what the question actually asked.** Revenue by quarter, and the second half of the year against the first. This is the quarterly pivot from Chapter 12's exercise 32, with one column added:

```sql
WITH sales_lines AS (
  SELECT p.category,
         EXTRACT(QUARTER FROM o.order_date) AS qtr,
         oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS line_revenue
  FROM orders AS o
  JOIN order_items AS oi ON o.order_id = oi.order_id
  JOIN products    AS p  ON oi.product_id = p.product_id
  WHERE o.status <> 'Cancelled'
)
SELECT category,
       ROUND(SUM(CASE WHEN qtr = 1 THEN line_revenue ELSE 0 END), 0) AS q1,
       ROUND(SUM(CASE WHEN qtr = 2 THEN line_revenue ELSE 0 END), 0) AS q2,
       ROUND(SUM(CASE WHEN qtr = 3 THEN line_revenue ELSE 0 END), 0) AS q3,
       ROUND(SUM(CASE WHEN qtr = 4 THEN line_revenue ELSE 0 END), 0) AS q4,
       ROUND(100.0 * SUM(CASE WHEN qtr >= 3 THEN line_revenue ELSE 0 END)
                   / SUM(CASE WHEN qtr <= 2 THEN line_revenue ELSE 0 END) - 100, 0)
         AS h2_vs_h1_pct
FROM sales_lines
GROUP BY category
ORDER BY q4 DESC;
```

```
  category  |   q1   |   q2   |   q3   |   q4    | h2_vs_h1_pct
------------+--------+--------+--------+---------+--------------
 Storage    | 503257 | 342422 | 451179 | 1001116 |           72
 Kitchen    | 133888 | 219336 | 393660 |  461146 |          142
 Industrial |  80780 | 147560 | 275450 |  292040 |          149
 Furniture  |  16388 |  17250 |      0 |       0 |         -100
(4 rows)
```

- `EXTRACT(QUARTER FROM o.order_date)` gives 1 to 4. Each `SUM(CASE WHEN qtr = 1 …)` adds only that quarter's lines: one pivot column per quarter.
- `h2_vs_h1_pct` divides July–December revenue by January–June revenue: 100 × H2 ÷ H1 − 100 is the percentage change. With one year of data, half-on-half is the fairest growth measure available; there's no 2024 in this database to compare with.
- Kitchen and Industrial both grew steadily, quarter after quarter. Storage's growth is mostly one quarter: Q4 is more than twice Q3. Furniture sold nothing after June.

**Step 4: revenue isn't profit.** Chapter 12's revenue-versus-profit query (section 12.10), with profit per order and the average discount added:

```sql
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost), 0) AS gross_profit,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost)
             / SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 1) AS margin_pct,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost)
             / COUNT(DISTINCT o.order_id), 0) AS profit_per_order,
       ROUND(AVG(oi.discount_pct), 1) AS avg_discount_pct
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
JOIN products    AS p  ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY gross_profit DESC;
```

```
  category  | gross_profit | margin_pct | profit_per_order | avg_discount_pct
------------+--------------+------------+------------------+------------------
 Storage    |       619174 |       26.9 |             4360 |              4.8
 Kitchen    |       401580 |       33.2 |             4724 |              1.7
 Industrial |       108330 |       13.6 |             4710 |              9.2
 Furniture  |         8138 |       24.2 |             4069 |              2.5
(4 rows)
```

- `gross_profit` is revenue minus `quantity × unit_cost`, and `margin_pct` divides total profit by total revenue, both exactly as in section 12.10.
- `profit_per_order` divides the category's gross profit by the orders that include it (Step 1's `orders`).
- `avg_discount_pct` is the average discount across the category's order lines.

**Reading it.** Industrial orders are more than twice as large, but at a 13.6% margin they earn about the same gross profit per order as Kitchen (₹4,710 against ₹4,724). Industrial is 18% of revenue but under 10% of gross profit (₹1,08,330 of ₹11,37,221), and it carries the deepest discounts.

**The one-page summary:**

> **2025 category performance**
>
> **Growth:** Kitchen and Industrial are driving growth. Both more than doubled from the first half of 2025 to the second (Kitchen +142%, Industrial +149%), rising every quarter. Storage is still the largest category (₹22.98 lakh of ₹43.35 lakh) and grew 72%, but most of that came in Q4 alone, so I'd check whether Q4 was a one-off before calling it a trend. Furniture sold nothing after June.
>
> **What's driving the difference:** Industrial orders are large (₹34,601 of Industrial items per order that includes them, against ₹14,212–₹16,183 for Kitchen and Storage), but they carry the deepest discounts (9.2% on average) and a 13.6% margin. So an Industrial order earns about the same gross profit as a Kitchen order (₹4,710 against ₹4,724). Kitchen grows almost as fast at a 33.2% margin, which makes it the most valuable growth in the business.
>
> **Recommendation:** Before funding any push to win more Industrial customers, review the discounts on crate orders (Chapter 12's revenue-versus-profit query already flagged them). Industrial volume is only worth growing if those discounts are controlled. In the meantime, put new sales effort behind Kitchen, where growth already comes with a healthy margin, and track both against this same breakdown next quarter.
>
> **Caveats:** one year and 24 customers. Industrial's revenue comes from 5 customers, so a single lost account would change its picture. Furniture's 2 orders are too few to judge it either way; I'm flagging it rather than ranking it or dismissing it.

### How this would be scored

| Dimension | What a strong submission does |
|---|---|
| Correctness | Numbers reconcile (Step 1 adds up to the year's revenue; Step 2 agrees with Step 1); SQL is real and runs without error |
| Structure & communication | One-page summary is scannable and leads with the finding, not the method |
| Depth & edge cases | Goes past the headline ranking: fixes the grain, measures growth over time, and checks profit, not just revenue |
| Business judgment | Ends in one specific, proportionate recommendation, not five vague ones, and ties it to margin |
| Collaboration | States the caveats (one year, five Industrial customers, two Furniture orders) explicitly and doesn't overclaim |

**What a weak submission looks like:** the revenue table alone, with a generic "Storage is doing well, Furniture needs improvement" observation, no growth measure, no recommendation and no caveat. Technically not wrong, just thin: exactly Chapter 69's core lesson applied to a whole assignment instead of one question. A *plausible-but-wrong* submission is worse: "Industrial orders are worth double, so win more Industrial customers", which reads revenue as profit.

**Learn it in:** Chapter 12, sections 12.9–12.10 (the revenue formula, joins, revenue versus profit) and 12.12 (the grain of an average); Chapter 13, sections 13.2 (CTEs) and 13.6 (time windows and growth). **Practise it with:** Chapter 71, Q71-072 (revenue by order, with a fan-out warning).

---

## 82.2 Take-home assignment: Data Scientist

### The assignment, as given

> "We want to predict which leads are likely to convert, using the attached lead data. Build a model, evaluate it properly, and explain in one page how you'd use it in production, including any limitation you'd flag before it ships. You have 3 hours."

**Practice data:** Riverstone's CRM export from Chapter 36, rebuilt by `lead_data.py`, a copy of Chapter 37's helper, in `companion/ch82/`. Open a Jupyter notebook in that folder and run each block below as its own cell, top to bottom. If `companion/crm/` is empty, first build the data with `python generate_riverstone_crm.py` in the companion folder (Chapter 36).

### Model submission

**Step 1: load the data and look at the split.**

```python
import sys
import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import confusion_matrix, log_loss, roc_auc_score

sys.path.append(".")
from lead_data import LEAD_CATS, LEAD_NUMS, load_leads, make_model

warnings.filterwarnings("ignore", category=UserWarning)

train, valid, test = load_leads()
X_cols = LEAD_CATS + LEAD_NUMS
for name, part in [("train", train), ("valid", valid), ("test", test)]:
    print(
        f"{name:<5} {len(part):>5,} leads, {part['won'].mean():.1%} won, "
        f"{part['created_at'].min():%b %Y} to {part['created_at'].max():%b %Y}"
    )
```

```
train 7,291 leads, 7.9% won, Jan 2023 to Dec 2024
valid 2,225 leads, 6.6% won, Jan 2025 to Jun 2025
test  1,185 leads, 8.8% won, Jul 2025 to Oct 2025
```

- `load_leads()` removes duplicate enquiries, builds Chapter 36's features and splits **by date** (Chapter 36, section 36.3): the model learns from 2023–2024, is chosen on the first half of 2025, and is tested once on later leads. `LEAD_CATS + LEAD_NUMS` are its thirteen feature columns.
- `sys.path.append(".")` and `warnings.filterwarnings(…)` are the same two lines as in Chapter 39, section 39.1.
- `{part['created_at'].min():%b %Y}` formats a date as a short month and year.
- **The base rate matters:** only 6.6% of validation leads were won. Every later number is read against it.

**Step 2: a baseline and a challenger, compared on validation.** The baseline is Chapter 36's logistic regression; the challenger is gradient boosting with the settings Chapter 37's random search chose (section 37.12):

```python
boosting = HistGradientBoostingClassifier(
    learning_rate=0.014,
    max_depth=3,
    max_iter=454,
    min_samples_leaf=67,
    l2_regularization=0.015,
    random_state=37,
)
candidates = {
    "logistic regression": make_model(LEAD_CATS, LEAD_NUMS),
    "gradient boosting": make_model(LEAD_CATS, LEAD_NUMS, boosting),
}
y_valid = valid["won"].to_numpy()
for label, model in candidates.items():
    model.fit(train[X_cols], train["won"])
    p = model.predict_proba(valid[X_cols])[:, 1]
    print(
        f"{label:<20} ROC-AUC {roc_auc_score(y_valid, p):.3f}   "
        f"log loss {log_loss(y_valid, p):.4f}"
    )
```

```
logistic regression  ROC-AUC 0.823   log loss 0.1948
gradient boosting    ROC-AUC 0.826   log loss 0.1964
```

- `make_model(LEAD_CATS, LEAD_NUMS)` is Chapter 36's pipeline with logistic regression; passing `boosting` as the third argument swaps the model and keeps the same preparation.
- The five settings are the ones Chapter 37's search picked (sections 37.8 and 37.11), rounded to three decimals: `max_iter=454` trees, each at most `max_depth=3` levels deep, each correcting only a small step of the error so far (`learning_rate=0.014`), no leaf with fewer than `min_samples_leaf=67` leads, and a gentle penalty on large leaf values (`l2_regularization=0.015`). `random_state=37` fixes boosting's random choices, so the run repeats exactly.
- `candidates` is a dictionary from name to model; `.items()` gives each pair in turn. Each model learns from `train` and is scored on `valid`.
- **ROC-AUC** measures ranking and **log loss** the honesty of the probabilities (Chapter 39, sections 39.2 and 39.4). Boosting ranks a hair better (0.826 against 0.823) and its probabilities are a hair worse. That's a tie, and a tie goes to the simpler, explainable model.

**Step 3: choose the threshold by cost, not 0.5.** Working a lead costs about ₹1,500, and a won lead is worth about ₹30,255 of margin; both are Chapter 39's stated assumptions (section 39.5):

```python
p_valid = candidates["logistic regression"].predict_proba(valid[X_cols])[:, 1]
WORK_COST = 1500  # ₹ to work one lead properly (Chapter 39, section 39.5)
WIN_VALUE = 30255  # ₹ margin from one won lead (Chapter 39, section 39.5)


def profit_at(threshold):
    worked = p_valid >= threshold
    wins = y_valid[worked].sum()
    return WIN_VALUE * wins - WORK_COST * worked.sum(), worked.sum(), wins


grid = np.linspace(0.0, 0.5, 501)
profits = [profit_at(t)[0] for t in grid]
best = grid[np.argmax(profits)]
for label, t in [("work every lead", 0.0), ("best threshold", best)]:
    profit, worked, wins = profit_at(t)
    print(f"{label:<16} {t:.3f}: {worked:>5,} worked, {wins} wins, profit ₹{profit:,.0f}")
```

```
work every lead  0.000: 2,225 worked, 146 wins, profit ₹1,079,730
best threshold   0.077:   627 worked, 112 wins, profit ₹2,448,060
```

- `p_valid` is the logistic model's probability of a win for each validation lead.
- `profit_at` is Chapter 39's function: every worked lead costs ₹1,500, every win among them earns ₹30,255. It returns the expected profit, the leads worked and the wins.
- `np.linspace(0.0, 0.5, 501)` tries every threshold from 0 to 0.5 in steps of 0.001, and `np.argmax` finds the one with the most profit.
- Working the 627 leads above 0.077 makes about ₹24.5 lakh of expected profit, against ₹10.8 lakh for working all 2,225: about 2.3 times the profit from 28% of the effort.

**Step 4: what the chosen threshold does, next to the default.**

```python
for t in [0.5, best]:
    tn, fp, fn, tp = confusion_matrix(y_valid, (p_valid >= t).astype(int)).ravel()
    print(
        f"threshold {t:.3f}: TP {tp:>3}  FP {fp:>3}  FN {fn:>3}  TN {tn:>4}   "
        f"precision {tp / (tp + fp):.3f}  recall {tp / (tp + fn):.3f}"
    )
```

```
threshold 0.500: TP   4  FP   3  FN 142  TN 2076   precision 0.571  recall 0.027
threshold 0.077: TP 112  FP 515  FN  34  TN 1564   precision 0.179  recall 0.767
```

- `(p_valid >= t).astype(int)` turns probabilities into 0/1 predictions; `confusion_matrix(…).ravel()` returns the four counts in scikit-learn's order, `tn, fp, fn, tp` (Chapter 39, section 39.1).
- At the default 0.5 the model flags 7 leads and finds 4 of the 146 wins. At 0.077 it finds 112 of them (recall 0.767), and about 1 worked lead in 6 is won (precision 0.179), which is expected when only 6.6% of leads convert.

**Step 5: the team's capacity.** Chapter 39 found the team can work about 4 leads a day, 504 in the 126 working days of the period. That's fewer than 627:

```python
budget = 126 * 4  # working days in Jan–Jun 2025 × leads the team can work a day
top = np.sort(p_valid)[::-1][:budget]
profit, worked, wins = profit_at(top.min())
print(f"capacity {budget}: work leads scoring above {top.min():.3f}")
print(f"{worked} worked, {wins} wins, profit ₹{profit:,.0f}")
```

```
capacity 504: work leads scoring above 0.097
504 worked, 102 wins, profit ₹2,330,010
```

- `np.sort(p_valid)[::-1]` sorts the scores from highest to lowest (`[::-1]` reverses the order), and `[:budget]` keeps the top 504.
- The lowest of those, `top.min()`, is the threshold that fills the team's capacity exactly.
- Working the top 504 still makes about ₹23.3 lakh. Chapter 39 compared this with the old rule of thumb (work referrals, trade fairs and partners: ₹17.4 lakh from a similar 531 leads).

**Step 6: the test set, once.** Refit both candidates on every lead before July 2025 and score the later leads:

```python
before_july = pd.concat([train, valid])
y_test = test["won"].to_numpy()
for label, model in candidates.items():
    model.fit(before_july[X_cols], before_july["won"])
    p = model.predict_proba(test[X_cols])[:, 1]
    print(
        f"{label:<20} test ROC-AUC {roc_auc_score(y_test, p):.3f}   "
        f"log loss {log_loss(y_test, p):.4f}"
    )
```

```
logistic regression  test ROC-AUC 0.838   log loss 0.2369
gradient boosting    test ROC-AUC 0.830   log loss 0.2422
```

- `pd.concat([train, valid])` stacks the two tables, so the final models learn from every lead before July 2025.
- The loop is Step 2's, reusing the same two `candidates`: `.fit` retrains each on the larger table, and `roc_auc_score` and `log_loss` score it on the test leads, which neither model has seen.
- On the test leads, logistic regression is ahead on both measures. The decision from Step 2 stands.

**The one-page summary:**

> **Model:** logistic regression on Chapter 36's thirteen features, split by date. I compared it with tuned gradient boosting: on validation they tied (ROC-AUC 0.823 against 0.826), and on the held-out test leads logistic regression was ahead (0.838 against 0.830) with better-calibrated probabilities. I'm shipping the simpler model: it's as accurate, faster, and easy to explain to the sales team.
>
> **Evaluation:** at the default 0.5 threshold the model is nearly useless: it flags 7 of 2,225 leads. Working the 627 leads that score above 0.077 gives an estimated ₹24.5 lakh of expected profit on the January–June leads, against ₹10.8 lakh for working all 2,225: about 2.3 times the profit from 28% of the effort. The team can work only about 504 leads in that period, so in practice I'd work the top 504 by score (a threshold of about 0.097): ₹23.3 lakh.
>
> **Production use:** score new leads nightly and hand the sales team a ranked call list sized to their capacity, not a raw score. I'd rank by expected value (probability × deal value, Chapter 44's lesson) once we have a per-lead deal estimate, such as the quoted value or company size. Today every lead uses the same ₹30,255, so ranking by probability is equivalent, and that's the first data gap I'd close.
>
> **Limitations I'd flag before shipping:** the model learns from 2023–2024 patterns; if lead sources or the market shift (Chapter 36 showed the marketplace share rising), retrain it, and watch how many leads each day's threshold flags. The ₹1,500 cost and the ₹30,255 win value are assumptions to agree with finance, not facts; the profit figures are expected values from the model, not money earned, and should be confirmed with a small trial before anyone quotes them.

### How this would be scored

| Dimension | What a strong submission does |
|---|---|
| Correctness | A real baseline-versus-challenger comparison on the same split, chosen on validation and tested once; every number comes from one model and one dataset |
| Structure & communication | Model choice → evaluation → production plan → limitations, in that order |
| Depth & edge cases | Goes past AUC into a cost-based threshold and the team's capacity, showing the metric-to-decision translation |
| Business judgment | Chooses the simpler model when the complex one doesn't win, and sizes the list to what the team can actually work |
| Collaboration | States real limitations unprompted and doesn't oversell the model as a finished, permanent solution |

**What a weak submission looks like:** reports only AUC, picks boosting because it's "more advanced", recommends a 0.5 threshold with no cost reasoning, and has no limitations section at all: technically functional, missing every dimension beyond raw correctness.

**Learn it in:** Chapter 36, sections 36.3 (a split by date) and 36.10 (baselines); Chapter 37, section 37.12 (baseline versus boosting on the leads); Chapter 39, sections 39.1 (the confusion matrix), 39.2 (ROC-AUC) and 39.5 (the cost threshold and capacity); Chapter 44, section 44.4 (ranking by value, not probability). **Practise it with:** Chapter 74, Q74-008 (a good AUC can still be a bad choice), Q74-015 (ROC-AUC versus PR-AUC) and Q74-016 (the 0.5 threshold).

---

## 82.3 Take-home assignment: Data Engineer

### The assignment, as given

> "Design and implement a small pipeline that loads daily order data into a summary table, safely re-runnable if it fails partway through, with at least one automated data quality check. You have 2 hours."

**Practice data:** the Riverstone mini database (12 orders, January to March 2026), loaded into `riverstone_lab`, the practice database from Chapter 12, section 12.13, so that nothing you do here touches the `riverstone` database itself. If you dropped `riverstone_lab` at the end of that section, create it again with `CREATE DATABASE riverstone_lab;`. Then, connected to `riverstone_lab`, run `riverstone_setup.sql` from the companion files (Appendix E) with *Execute SQL Script*, as in section 12.3. It creates the mini database's seven tables in the lab.

<!-- lab:start -->

<!-- Verifier setup, not printed: the lab database and the mini database's tables, as the reader makes them above.
```sql
CREATE DATABASE riverstone_lab;
```
```sql
\i '/home/user/DS_BA_Curriculum/Data Science/Analyst-to-Architect/companion/postgresql/riverstone_setup.sql'
```
-->

### Model submission

**Step 1: the summary table, created once.** The table's own rules are the first quality check:

```sql
CREATE TABLE IF NOT EXISTS daily_summary (
    order_date     DATE PRIMARY KEY,
    total_revenue  NUMERIC(12,2) NOT NULL CHECK (total_revenue >= 0),
    order_count    INTEGER       NOT NULL CHECK (order_count > 0)
);
```

- **`IF NOT EXISTS`** makes the setup safe to run twice. A plain `CREATE TABLE` stops the second time with `ERROR: relation "daily_summary" already exists`; with `IF NOT EXISTS`, PostgreSQL prints a notice and carries on.
- **`PRIMARY KEY`** on `order_date` allows one row per day, so a duplicate day can never be stored.
- **`NOT NULL`** and the two **`CHECK`** rules (Chapter 12, section 12.13) reject a missing or negative revenue, and a day with no orders. A load that breaks them fails with an error instead of storing a wrong number.

Run the same statement a second time:

<!-- Verifier: the same statement again, as the reader runs it.
```sql
CREATE TABLE IF NOT EXISTS daily_summary (
    order_date     DATE PRIMARY KEY,
    total_revenue  NUMERIC(12,2) NOT NULL CHECK (total_revenue >= 0),
    order_count    INTEGER       NOT NULL CHECK (order_count > 0)
);
```
-->

```
NOTICE:  relation "daily_summary" already exists, skipping
```

**Step 2: the load, safe to repeat.** Replace a whole window of days inside one transaction:

```sql
BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;
```

- **`BEGIN` … `COMMIT`** is a transaction (Chapter 12, section 12.13): the `DELETE` and the `INSERT` are kept together or undone together. If anything fails in between, the table keeps its previous contents.
- **The `DELETE`** clears every day in the window; **the `INSERT`** rebuilds them from the source. Chapter 46, section 46.4 proved this delete-and-insert pattern with a failure test.
- The window here is the whole of the mini database, the first quarter of 2026. A daily job would reload the last few days, so that late changes (a cancellation, a corrected line) are picked up.

Check what arrived:

```sql
SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;
```

```
 days | orders |  revenue
------+--------+-----------
   11 |     11 | 323930.00
(1 row)
```

Eleven days, one order each: the twelve orders less the cancelled one. ₹3,23,930 is the same total as Chapter 12's revenue-versus-profit query (section 12.10). ✓

Now run the whole load block (`BEGIN` to `COMMIT`) a second time, and count again:

<!-- Verifier: the load block again, as the reader runs it.
```sql
BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;
```
-->

```sql
SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;
```

```
 days | orders |  revenue
------+--------+-----------
   11 |     11 | 323930.00
(1 row)
```

The same eleven days and the same total: a second run changes nothing.

**Step 3: two failure tests.** A re-run of the same data is the easy case. The two that catch real pipelines out are a correction to data already loaded, and a bad row.

*Test 1, a correction.* The customer cancels order 5012, the only order on 15 March:

```sql
UPDATE orders SET status = 'Cancelled' WHERE order_id = 5012;
```

Run the load block again, then count:

<!-- Verifier: the load block again, as the reader runs it.
```sql
BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;
```
-->

```sql
SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;
```

```
 days | orders |  revenue
------+--------+-----------
   10 |     10 | 297710.00
(1 row)
```

15 March has gone, and the total fell by that order's ₹26,220. This is why the load deletes the window first. An upsert (`INSERT … ON CONFLICT (order_date) DO UPDATE`, Chapter 12, section 12.13) would also survive a re-run without duplicates, but it only touches the days its `SELECT` returns. A day that loses all its orders returns no row, so the upsert would leave 15 March at its old ₹26,220 forever.

*Test 2, a bad row.* A new order arrives with a typing slip: a discount of 150% instead of 15%:

```sql
INSERT INTO orders VALUES (5013, 1, '2026-03-20', 'Pending', 3);
INSERT INTO order_items VALUES (21, 5013, 101, 10, 450.00, 150);
```

Run the load block again:

<!-- Verifier: the load block again, as the reader runs it.
```sql
BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;
```
-->

```
ERROR:  new row for relation "daily_summary" violates check constraint "daily_summary_total_revenue_check"
DETAIL:  Failing row contains (2026-03-20, -2250.00, 1).
```

The line's revenue is 10 × ₹450 × (1 − 1.5) = −₹2,250, and the `CHECK` rule refuses it. The load **fails loudly**, and because the `DELETE` ran inside the same transaction, it is undone too:

```sql
SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;
```

```
 days | orders |  revenue
------+--------+-----------
   10 |     10 | 297710.00
(1 row)
```

The previous good table is still there, untouched. Fix the source, and the same load succeeds:

```sql
UPDATE order_items SET discount_pct = 15 WHERE order_item_id = 21;
```

Run the load block once more, then count:

<!-- Verifier: the load block again, as the reader runs it.
```sql
BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;
```
-->

```sql
SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;
```

```
 days | orders |  revenue
------+--------+-----------
   11 |     11 | 301535.00
(1 row)
```

Eleven days again: 20 March is in, with 10 × ₹450 × 0.85 = ₹3,825.

**Step 4: a data test after every load.** A data test is a query that returns the rows that *break* a rule; zero rows means it passed (Chapter 47, section 47.3). This one compares every day in the summary with the source, in both directions:

```sql
SELECT s.order_date, s.total_revenue, src.order_date AS source_date, src.revenue AS source_revenue
FROM daily_summary AS s
FULL OUTER JOIN (
    SELECT o.order_date,
           ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 2) AS revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_date
) AS src ON s.order_date = src.order_date
WHERE s.total_revenue IS DISTINCT FROM src.revenue;
```

```
 order_date | total_revenue | source_date | source_revenue
------------+---------------+-------------+----------------
(0 rows)
```

- The subquery in brackets is the load's revenue by day, straight from the source, rounded to two decimals like the table's `NUMERIC(12,2)` column.
- **`FULL OUTER JOIN`** keeps days from both sides (Chapter 12, section 12.10: the reconciliation join), so a day missing from the summary *or* a stale day left in it both show up.
- **`IS DISTINCT FROM`** (Chapter 28, section 28.10) is "not equal" that also treats a NULL on one side as a difference; a plain `<>` would silently skip those rows.
- Zero rows: every day matches its source. The pipeline's scheduler runs this after each load and **fails the run if any row comes back**, the way Chapter 47's `run_tests` does.

Clean up when you're done:

```sql
DROP TABLE daily_summary;
```

`DROP TABLE` removes the practice table (Chapter 12, section 12.13). The mini database's tables can stay in the lab for the next time you practice.

<!-- lab:end -->

**Step 5: the one-page design note:**

> **Idempotency:** the load deletes and re-inserts a window of days inside one transaction, so running it twice gives the same table, and a correction to data already loaded (a cancelled order, a fixed line) is picked up on the next run. I chose this over an upsert (`ON CONFLICT … DO UPDATE`) because an upsert never removes a day that has lost all its orders. One statement, or one transaction, is atomic: a failure partway through leaves the table unchanged, so there's nothing to clean up. What makes a *second* run safe is the delete-and-insert.
>
> **Data quality:** two layers, and both can fail. The table's own rules (`NOT NULL`, `CHECK`) stop a missing or negative revenue at write time, which also covers a NULL discount, since a NULL anywhere in the revenue formula makes the line's revenue NULL (Chapter 12, section 12.7). After each load, a data test reconciles every day with the source and fails the run on any mismatch. In a real deployment I'd add a volume check (today's order count far below the trailing average, Chapter 47, section 47.5), because a truncated source file passes both of these: fewer orders, all of them valid.
>
> **Scale:** each run recomputes the whole window, which is fine at Riverstone's size. At scale I'd reload only the last few days, sized to how late changes arrive.
>
> **What I'd add given more time:** a raw/staging layer (Chapter 45's raw → staging layers), so extracted data lands unmodified before transformation, letting a transformation bug be fixed and reprocessed without re-extracting from the source; and an explicit dependency declaration if this joins with other scheduled loads, rather than assuming execution order.

### How this would be scored

| Dimension | What a strong submission does |
|---|---|
| Correctness | The load genuinely re-runs safely: no duplicates, no stale days, and a bad row can't reach the table |
| Structure & communication | Table, load, tests and design note clearly separated, not tangled together |
| Depth & edge cases | Tests the hard cases (a correction and a bad row), not just a second run, and names a *second* check type (volume) unprompted |
| Business judgment | Explains *why* a pipeline should fail loudly rather than silently store a wrong number |
| Collaboration | States what's missing given more time, rather than presenting the 2-hour version as fully production-ready |

**What a weak submission looks like:** a plain `INSERT` with no conflict handling, which fails the core "safely re-runnable" requirement entirely; or a quality check that only counts bad rows and logs a warning, so nothing ever fails.

**Learn it in:** Chapter 12, section 12.13 (constraints, transactions, the upsert); Chapter 45, section 45.1 (raw and staging layers); Chapter 46, section 46.4 (idempotency, proven with a failure test); Chapter 47, sections 47.3 (data tests) and 47.5 (volume checks). **Practise it with:** Chapter 77, Q77-007 (the re-run that duplicates rows) and Q77-028 (a check that would have caught negative revenue).

---

## 82.4 Mock interview: Data Analyst (entry level)

*A 20-minute mock for an entry-level Data Analyst role, condensed. Interviewer notes appear in brackets, with Chapter 69's tags. At two turns, a weaker answer to the same question follows, with its score. The scoring table at the end uses Chapter 69's scale, 1 (weak) to 4 (outstanding).*

**Interviewer:** Let's start with something practical. Write a query to find customers who haven't placed an order in the last 90 days.

**Candidate:** Sure. Two quick checks first. When you say "last 90 days," is that from today, or from the most recent order date in the data? If this is historical data, "today" might not mean what I'd assume. And should a cancelled order count as activity, and do you want customers who've never ordered at all?

*[Interviewer note: **[+Clarify]** caught a real ambiguity most candidates miss, plus two scope questions that change the answer.]*

**Interviewer:** From the most recent date in the data. Cancelled orders don't count, and yes, include customers who've never ordered.

**Candidate:** Got it.

```sql
SELECT c.customer_id, c.customer_name
FROM customers AS c
WHERE NOT EXISTS (
  SELECT 1
  FROM orders AS o
  WHERE o.customer_id = c.customer_id
    AND o.status <> 'Cancelled'
    AND o.order_date > (SELECT MAX(order_date) FROM orders) - INTERVAL '90 days'
);
```

The inner `SELECT MAX(order_date)` is the latest date in the data, and `- INTERVAL '90 days'` moves 90 days back from it. I used `NOT EXISTS` on purpose. The obvious version is `NOT IN` with a subquery, but if that subquery ever returns a NULL customer ID, the whole query silently returns zero rows, because "x is not in a list containing NULL" can never be confirmed true. `NOT EXISTS` asks "is there no recent order for this customer?", and a NULL can't spoil it. It also keeps customers with no orders at all, which you said you want.

*[Interviewer note: **[+Edge cases]** chose the safe form and explained why the alternative fails, which is Chapter 69's definition of a 4 on Correctness.]*

> *A weaker answer to the same turn:* writes `WHERE c.customer_id NOT IN (SELECT customer_id FROM orders WHERE …)` straight away, with no NULL filter and no question about cancelled orders. It happens to work on this table, because `orders.customer_id` is never NULL, but asked "could this ever return nothing?", the candidate can't say why. *[Correctness 2: correct for the simple case only.]*

**Interviewer:** Let's say this returns 40 customers. Sales wants to know which to call first. How would you prioritize?

**Candidate:** I'd rank by revenue at risk, not just recency: the probability they've stopped buying times their value, if there's a model, or at minimum their revenue over the last year as a proxy if there isn't. Ranking by "most overdue" alone would put a small customer who's very overdue ahead of a large account that's only slightly overdue.

*[Interviewer note: **[+Business]** connects a simple query to a real prioritization decision without being asked.]*

> *A weaker answer to the same turn:* "I'd call the most overdue first." Reasonable, but it ties the list to nothing the business values. *[Business judgment 2: mentions the business, doesn't tie the answer to a decision.]*

**Interviewer:** Last one. Walk me through a project where an analysis you did led to an actual decision.

**Candidate** (about 90 seconds, which suits a round with this many follow-ups; Chapter 81, Q81-002):

> **Situation:** "In my portfolio project, on a practice dataset from a supplies distributor, the key accounts manager asked whether deeper discounts would grow Retail. Customers on discounts of 5% or more placed 14.8 orders in 2025, against 9.3 for everyone else."
> **Task:** "I had to say whether that gap was a reason to discount harder."
> **Action:** "I built a customer-year table from the order lines and reconciled it to the year's total before trusting it. Then I split the discount bands by segment, and the headline fell apart: 662 of the 681 discounted customers were Wholesale. Inside Wholesale, where customers are comparable, the shallowest discounts placed 14.1 orders and the deepest 13.6, no real difference. And Wholesale runs at an 18.6% margin against 30.2% for Retail."
> **Result:** "My memo recommended no, not on this evidence, and proposed a two-quarter test on a random group of Retail customers instead, which is the only way to answer a cause-and-effect question and far cheaper than a policy change. It was a portfolio project, so the decision was my recommendation. What I'd do differently: write the analysis plan, with the segment split in it, before the first query."

*[Interviewer note: **[+Evidence]** quantified and specific; **[+Limits]** says plainly that it was portfolio work, and what it would change. Most of the time went on Action, where it belongs.]*

### Scoring

| Dimension | Score | Why |
|---|---|---|
| Correctness | 4 | Correct query, and explained why the `NOT IN` alternative fails with a NULL |
| Structure & communication | 4 | Signposted: scope questions, then the query, then why `NOT IN` fails; the STAR answer put its time into Action and Result |
| Depth & edge cases | 4 | Raised the NULL trap, cancelled orders and never-ordered customers unprompted |
| Business judgment | 3 | Revenue-at-risk framing ties the call list to a decision; no attempt to size the revenue involved |
| Collaboration | 4 | Clarified before writing anything and adapted the query to the answers |

**Overall: extra-points level (mostly 4s). Hire.** Not flawless in a dramatic way, just consistently a step past "correct" at every turn. For a mid-level analyst role, expect the interviewer to push further: the same list with a window function (Chapter 13, section 13.8, Pattern 6, at-risk customers), and how you'd check it against what sales already knows.

**Learn it in:** Chapter 12, section 12.12 (`NOT EXISTS`, and why `NOT IN` fails with NULLs); Chapter 13, section 13.8 (Pattern 6, at-risk customers); Chapter 27, sections 27.7 and 27.10 (the memo, and telling the story); Chapter 81, section 81.1 (STAR). **Practise it with:** Chapter 71, Q71-002.

---

## 82.5 Mock interview: Data Scientist (mid level)

*A 25-minute mock for a mid-level Data Scientist role, condensed, in the same format.*

**Interviewer:** Tell me about a model you're proud of.

**Candidate:** "It's a portfolio project: lead scoring on a supplies distributor's CRM data, about 7,300 training leads from two years, where 6.6% of the next half-year's leads were won. The question was which leads the sales team should work. I split by date, so the model was always judged on leads that came after the ones it learned from. I compared logistic regression with tuned gradient boosting: they tied on validation, and on the test leads logistic regression was slightly ahead, 0.838 against 0.830, with better-calibrated probabilities. So I kept the simpler model. Then I set the threshold from costs, not 0.5: about ₹1,500 to work a lead and about ₹30,000 of margin from a win. The team can work only about 504 leads in six months, so I sized the list to that. Working the top 504 by score gave an expected ₹23.3 lakh, against ₹17.4 lakh for the old rule of thumb at about the same effort. The limitation I flagged: those are expected values from the model, not money earned, so I recommended a small trial before anyone quoted them."

*[Interviewer note: **[+Simple first]** baseline before the complex model; **[+Business]** quantified at the team's real capacity; **[+Limits]** separated expected from earned. Chapter 76A, Q76A-007 structure, unprompted.]*

**Interviewer:** You mentioned a test AUC of 0.838. Walk me through what that number actually means, and whether it's "good."

**Candidate:** AUC is the probability that the model ranks a randomly chosen won lead above a randomly chosen lost one. 0.838 means it gets that order right about 84% of the time: solid, not exceptional. Whether it's good enough depends on the decision it feeds, not on the number alone. Here the base rate is 6.6%, so the number sales actually feels is precision: on the 504-lead list, about one worked lead in five is won. Pairing the model with a cost-based threshold mattered more than the AUC itself.

*[Interviewer note: correct definition, and **[+Business]** resists treating the number as meaningful without the decision and the base rate.]*

> *A weaker answer to the same turn:* "It means the model is 84% accurate." That confuses ranking with accuracy; on these leads, predicting "lost" for everyone is already 93.4% accurate. *[Correctness 1: wrong.]*

**Interviewer:** What would you do if a stakeholder asked you to make the model "more accurate" with no further detail?

**Candidate:** I'd ask what's actually driving that request. Is a specific kind of error causing a real problem: missed high-value leads, or too many false positives wasting sales time? "More accurate" could mean better precision, better recall, or a better AUC, and those often trade off against each other, so I'd want to know which error matters more before doing anything.

*[Interviewer note: **[+Clarify]** the same diagnose-before-acting instinct as Chapter 76B's "make the report better" question (Q76B-001), applied to a model instead of a report.]*

**Interviewer:** Your model's feature importance shows a customer ID column ranking unusually high. What's your first reaction?

**Candidate:** That's a red flag, not a finding. An ID shouldn't predict anything on its own. Two likely mechanisms. Either IDs were assigned in sequence, so the ID is really a proxy for signup date, and with a random split the model learns era effects it can't use on future leads. Or the same customer's rows sit on both sides of the split, so the model recognizes customers instead of learning a pattern. I'd drop the ID, split by time or by customer (Chapter 36), and see whether the AUC falls.

*[Interviewer note: **[+Edge cases]** two real leakage mechanisms, and **[+Validate]** a test that tells them apart, not just "that's suspicious."]*

> *A weaker answer to the same turn:* "Great, the ID carries signal, so I'd keep it in." *[Correctness 1 and Depth & edge cases 1: treats a leak as a feature.]*

### Scoring

| Dimension | Score | Why |
|---|---|---|
| Correctness | 4 | Accurate AUC definition; both leakage mechanisms real, with the test that separates them |
| Structure & communication | 4 | The project story hit every beat unprompted: question, split, baseline, threshold, limitation |
| Depth & edge cases | 4 | Named two specific leakage mechanisms, not a vague "that's odd" |
| Business judgment | 4 | Quantified the model's value at the team's real capacity, against the rule it would replace |
| Collaboration | 3 | Strong throughout; could have asked one more clarifying question on the "more accurate" request before answering as fully as they did |

**Overall: extra-points level (mostly 4s). Hire,** with one small, realistic note: even a very strong candidate doesn't need a 4 everywhere. A fresher's version of this interview would stop at the confusion matrix and the threshold; a senior candidate would also be asked how to monitor the model and design the trial (Chapter 30).

**Learn it in:** Chapter 36, sections 36.3 and 36.7 (splits and leakage); Chapter 39, sections 39.2 and 39.5 (AUC, the cost threshold, capacity); Chapter 76A, Q76A-007 (telling a project story). **Practise it with:** Chapter 74, Q74-016, Q74-020 and Q74-031.

---

## 82.6 Mock interview: Data Engineer (mid level)

*A 25-minute mock for a mid-level Data Engineer role, condensed. This one is a borderline pass, so the scoring ends with the interviewer's hire decision and the reasoning behind it.*

**Interviewer:** Walk me through how you'd design a pipeline that loads daily sales data, and make it safe to re-run if it fails.

**Candidate:** "Four stages. First, extract yesterday's orders and order lines from the source system and land them unchanged in a raw layer, with the load date on every row, so I can always reprocess without going back to the source. Second, transform in staging: fix types, drop cancelled orders, apply the revenue formula. Third, load the summary table with an upsert keyed on the date, so if the job is retried, the day's row is updated instead of duplicated. Fourth, checks after every load: revenue can't be negative or missing, and today's order count shouldn't be far below the trailing average, because a truncated file passes every row-level check. A scheduler runs the stages in order, retries a failed step, and alerts a person when a check fails. And I'd monitor freshness against when people need the numbers: if a morning report goes out at 7:30, the summary must be complete well before that."

*[Interviewer note: **[+Signpost]** complete, staged answer, not just the load step; **[+Edge cases]** the volume check, unprompted.]*

**Interviewer:** An order from last Tuesday is cancelled today. What does your summary table show for Tuesday tomorrow morning?

**Candidate:** The upsert updates Tuesday's row with the new total.

**Interviewer:** Does tomorrow's run read Tuesday at all?

**Candidate:** No, you're right: it only loads yesterday, so Tuesday keeps its old total. I'd reload a window, say the last seven days, on every run. And if a day loses *all* its orders, the upsert has no row to update it with, so I'd delete and re-insert the window inside one transaction instead.

*[Interviewer note: reached the right design, but only after a hint. Late corrections are the classic edge case of this task. **[+Trade-offs]** once prompted, the upsert-versus-delete-and-insert reasoning was sound.]*

> *A stronger answer to the same turn:* the delete-and-insert window from the start, with the reason, as in section 82.3's design note. *[Depth & edge cases 4.]*

**Interviewer:** Your pipeline ran successfully last night, no errors, but this morning the numbers look wrong. Walk me through debugging this.

**Candidate:** First I'd separate two possibilities: did it process the right data and compute something wrong, or did it succeed technically while processing something incomplete, like a source file that arrived truncated? I'd check the row counts it processed against a trailing average first, since a silent volume drop is a common cause of "ran fine, wrong numbers" that a pure success-or-failure check wouldn't catch. If the volume looks normal, I'd trace the transformation logic for a recent change.

*[Interviewer note: **[+Signpost]** two hypotheses, cheapest check first, not a random guess.]*

> *A weaker answer to the same turn:* "I'd rerun it and see if the numbers change." A rerun of an idempotent pipeline on the same bad input gives the same bad output. *[Depth & edge cases 1: no hypothesis at all.]*

**Interviewer:** Say you find the issue: a source column got renamed upstream, and your pipeline was silently defaulting the missing column to zero instead of erroring. What do you change, beyond fixing this one instance?

**Candidate:** Two things, not just the immediate fix. I'd change the load to fail loudly if an expected column is missing, rather than defaulting silently: that's the actual root cause, not the rename itself. And I'd add a step that checks the pipeline's own output against a rough expected range before the run counts as successful, so a similar silent failure is caught the same day, not whenever someone notices the numbers look off.

*[Interviewer note: **[+Business]** separated the specific bug from the systemic gap that let it go unnoticed, exactly the depth this question is fishing for.]*

**Interviewer:** How would you decide whether this pipeline should be batch or streaming?

**Candidate:** By how fresh the downstream decision needs to be, not by which is more modern. A daily sales summary doesn't need sub-minute freshness, so batch is the right, simpler choice here. I'd only reach for streaming if there were a real decision that couldn't wait for the next batch window.

*[Interviewer note: **[+Trade-offs]** correctly resisted recommending streaming as the more impressive answer.]*

### Scoring

| Dimension | Score | Why |
|---|---|---|
| Correctness | 3 | Re-runs are safe and batch is the right call; the first design would have kept stale totals after a late correction |
| Structure & communication | 3 | Clear, staged design and a two-hypothesis debugging plan |
| Depth & edge cases | 2 | Needed a hint to see that a late cancellation never reaches yesterday-only loads |
| Business judgment | 3 | Fail-loudly root cause, and freshness tied to when the report is needed; batch because the decision is daily |
| Collaboration | 3 | Took the hint without defensiveness and adapted the design straight away |

**Overall: borderline pass (mostly 3s, one 2). Hire, with a note.** The interviewer's reasoning: "The debugging and root-cause answers are what this job needs every week. The late-correction gap is teachable, and the candidate closed it within one hint. For a senior role, the same gap would be a no-hire: seniors are expected to raise late-arriving changes themselves." A fresher would pass comfortably with the staged design and the batch answer alone; for them the root-cause answer would be an extra point.

**Learn it in:** Chapter 45, section 45.1 (raw and staging layers) and 45.8 (when the source changes shape); Chapter 46, sections 46.4–46.6 (idempotency, backfills, retries and alerting); Chapter 47, section 47.5 (volume and freshness); Chapter 50, section 50.1 (what "real-time" actually means). **Practise it with:** Chapter 77, Q77-002, Q77-007 and Q77-009.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Starting an unbounded take-home without asking anything | Days of unpaid work, and a submission that answers a different question from the one the reviewer meant | Check it against section 82.0; ask your scope questions in writing, and state the time you spent |
| A take-home with no summary, just code and output | Reviewer has to reverse-engineer the finding themselves | Always include a one-page summary leading with the answer |
| A take-home with no stated limitation | Reads as overconfident or unaware of real gaps | State at least one honest limitation, even under time pressure |
| Reporting revenue as if it were profit, or one model's numbers under another's name | The reviewer checks one figure, finds it doesn't match, and stops trusting the rest | Reconcile every number to its source query or cell, and say which model and which data each one comes from |
| A mock answer that's technically correct but thin | Passes on correctness, scores low on depth and business judgment | Practice adding at least one unprompted extra-point move per answer |
| Treating every mock question as isolated | Missed chances to connect answers into a coherent story | Notice when a later question connects to an earlier answer, and say so |
| Defensiveness under a "why did this go wrong" follow-up | Reads as fragility, costs the collaboration dimension | Engage with the question directly, as problem-solving, not a personal challenge |

---

## Project

**Goal:** complete one of this chapter's three take-homes yourself, from scratch, before reading the model submission again.

### Tools you'll need

**PostgreSQL 16** with `riverstone_2025` and `riverstone_lab` (Chapters 12 and 13), and **Python** in the book's virtual environment with scikit-learn (installed in Chapter 35) and the Chapter 82 companion folder. A timer, for practicing take-homes and mock answers under the same time pressure a real interview or assignment imposes.

1. Check the assignment against section 82.0, and write down the scope questions you'd ask.
2. Set a timer matching the stated time limit, and attempt the assignment cold.
3. Compare your submission with this chapter's scoring table, dimension by dimension, not just "was I right."
4. Record yourself doing one of the three mock interviews, playing both roles if needed, and compare your answers with the scored transcript and its weaker answers.
5. Identify the one dimension (correctness, structure and communication, depth and edge cases, business judgment, collaboration) you scored lowest on, and practice that one deliberately on your next three questions from any earlier chapter in this part.
6. *Business analysts:* before touching any data, rewrite section 82.1's assignment as a list of requirements questions for the sales head, using Chapter 76B, Q76B-001.

---

## Key terms

take-home assignment · fair take-home · model submission · mock interview · interviewer scoring notes · one-page summary (take-home) · cost-based threshold (reused) · idempotent load (reused) · data test (reused) · volume-anomaly check (reused)

---

## Final-week revision list

- Section 82.0: the three marks of a fair take-home, and the three warning signs.
- Section 82.1: Steps 2 to 4 (the grain of an average, growth by half-year, profit per order), and the one-page summary.
- Section 82.2: why the simpler model shipped; the cost threshold (0.077) and the capacity limit (504 leads).
- Section 82.3: the two failure tests, and why delete-and-insert beats an upsert for a window of days.
- Sections 82.4–82.6: each weaker answer, and the one move that would have lifted it.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric every scoring table in this chapter is built from.
- **Every other chapter in Part 8** supplied the questions these take-homes and mocks draw on: Chapter 71 (SQL), Chapter 74 (machine learning), Chapter 76A (telling a project story), Chapter 76B (requirements), Chapter 77 (pipeline design) and Chapter 81 (STAR answers). The skills themselves were taught earlier: Chapters 12 and 13 (SQL), Chapters 36, 37, 39 and 44 (the lead model and ranking by value), and Chapters 45–47 (pipelines and data quality).
- This is the last chapter in Part 8, The Interview Playbook. The reader who has worked through this part end to end has, in effect, already sat through the mocks in this chapter once, for real, one question at a time. **Chapter 83, The Long Game,** closes the book.
