# Chapter 31. Causal Inference Without Experiments

*Part 3 — Advanced Analytics & Analytics Engineering*

> **Chapter at a glance**
>
> **You will learn to:** read a difference of logarithms as a percentage change · say what a causal claim would mean when nobody randomized anything · spot why the two obvious comparisons (before-and-after, and treated-versus-untreated) usually mislead · estimate an effect with difference-in-differences, by hand and as a regression with fixed effects · test the parallel-trends assumption it rests on · build a synthetic control from untreated groups · build a comparison group with matching and propensity scores, and check the balance you achieved · use a threshold in a business rule as a natural experiment (regression discontinuity) · recognize a valid instrumental variable, and why you'll rarely have one · judge how much to trust each method, and write the claim up with its assumptions attached.
>
> **Before you start:** Chapter 22 (correlation is not causation, section 22.5; fitting a line, section 22.10), Chapter 30 (confidence intervals, experiments, Cohen's d in section 30.4, and section 30.11's regression output, `C()` categories and logistic regression), Chapter 18 (pandas `groupby`, `pivot_table`, `pd.cut`, `lambda`, and the NumPy basics in section 18.1), Chapter 21 (standard deviation), and Chapter 11 (`SUMPRODUCT`). Section 31.0 below teaches the logarithms this chapter uses.
>
> **Time needed:** 15–18 hours, spread over two and a half weeks, in two parts. **Part A, comparisons over time** (sections 31.0–31.5: logs, difference-in-differences, parallel trends, synthetic control), about 8 hours, ending with a checkpoint. **Part B, comparisons across units** (sections 31.6–31.9: matching, regression discontinuity, instruments, and how much to trust each), about 8 hours. Allow 2 more for the project.
>
> **Tools:** Python as installed in Chapter 17 (any version from 3.11 on runs every example), with pandas, numpy, scipy, statsmodels, and matplotlib. The uv project from Chapter 30 (section 30.1) or your Chapter 17 environment has them all. A spreadsheet (Chapter 10) for two by-hand steps.
>
> **Practice data:** three datasets built by `generate_ch31_data.py` in the companion folder: 24 months of orders for Riverstone's four sales regions, 240 key accounts with a quarterly-review program, and 60,000 orders around the free-delivery threshold. Each one was generated with a **known true effect**, so every method in this chapter can be marked against the right answer. They are simulated at the scale of a much larger Riverstone, like Chapter 28's `riverstone_perf` and Chapter 30's website data, not the one-year database from Chapter 13; every number in them is invented.

---

## Why this matters

Chapter 30's tools need a coin flip. Most business questions never get one:

- *"What did the 6% price rise in the North region actually cost us in volume?"* The price rose for every North customer on the same day. There is no control group, and no going back.
- *"Do quarterly business reviews grow accounts?"* The accounts that got them were chosen because they were big and growing.
- *"Is free delivery above ₹25,000 bringing customers back?"* The threshold applies to everyone.
- *"Did the new warehouse cut delivery times?"* It opened once, in one place.

You can't randomize any of these, and you still have to answer them, because somebody is going to act on the answer. The methods in this chapter get closer to a causal answer than "revenue went up after we did it", by finding a comparison that stands in for the experiment you couldn't run. They are also what economists, policy analysts, and product data scientists spend most of their time on, and a favorite interview topic: *"you can't A/B test this. How would you measure it?"*

None of them is magic. Each replaces randomization with an **assumption**, and the discipline is to state the assumption, test what you can, and say what would break it.

---

## In plain English

**A causal claim is a comparison with a world that didn't happen.**

"The price rise cost us 8% of our order volume" means: North's volume with the price rise, against North's volume in the same months *without* it. The second half doesn't exist. Every method here is a way of building a stand-in for it, called the **counterfactual**.

- **Before-and-after** uses North's own past as the stand-in. It fails whenever anything else changed at the same time: the season, the economy, a competitor.
- **Difference-in-differences** uses the other regions' change over the same months to measure "anything else", and subtracts it. The assumption is that North *would have moved like them* if nothing had happened.
- **Synthetic control** builds a fake North out of a weighted blend of the other regions, chosen so the blend tracks North's history closely, and then compares the real North with its double.
- **Matching** builds the stand-in customer by customer: for each account in the program, find an account that looked the same beforehand and didn't get it.
- **Regression discontinuity** uses a rule. An order of ₹24,900 and one of ₹25,100 are nearly identical, except one gets free delivery. Just either side of a threshold, the rule does the randomizing for you.
- **Instrumental variables** find something that nudges the treatment without touching the outcome any other way, and use only the variation that nudge explains.

Every one of them is an argument about the counterfactual, not a calculation that settles the matter. That's why this chapter spends as much time on assumptions and checks as on formulas.

---

## 31.0 Logs in ten minutes

Every method in this chapter measures an effect as a *percentage*: "the price rise cost 8% of volume", "reviews add 7% to revenue". Percentages are awkward to subtract, and this chapter subtracts changes from changes all the time. The tool that makes percentages behave is the **logarithm**. Nothing earlier in the book needed it, so here it is from the start.

### The idea

The **natural logarithm** of a positive number x, written ln(x), is a second way of writing x in which **multiplying becomes adding**:

> **The one rule you need.** ln(a × b) = ln(a) + ln(b)
>
> - Growing by 5% means multiplying by 1.05. On the log scale it means **adding** ln(1.05) = 0.049.
> - The **log difference** d = ln(after) − ln(before) is therefore a measure of growth. For small changes it is close to the percentage change: 0.049 against 5%.
> - **exp**, the exponential function, undoes ln: exp(ln(x)) = x. So exp(d) − 1 turns a log difference back into an exact percentage change.

(The "natural" log is the one based on the number e ≈ 2.718. You won't need that fact here; spreadsheets and Python use it whenever they say `LN` or `log`.)

### By hand, with this chapter's numbers

Section 31.2 finds that North averaged 2,032 orders a month before its price rise and 2,067 after. Three ways to measure the change:

| Step | Arithmetic | Result |
|---|---|---|
| Ordinary percentage change | 2,067 ÷ 2,032 − 1 | 0.0172, or +1.72% |
| Log difference | ln(2,067) − ln(2,032) = 7.6339 − 7.6168 | 0.0171 |
| Back from logs | exp(0.0171) − 1 | 0.0172, or +1.72% |

The log difference, 0.0171, is almost the percentage itself, and converting it back gives exactly the ordinary answer.

### In a spreadsheet

Type 2032 in A1 and 2067 in A2. Then `=LN(A2)-LN(A1)` in B1 returns 0.0171, and `=EXP(B1)-1` in B2 returns 0.0172. `LN` and `EXP` work the same in Excel and Google Sheets.

### In Python

NumPy (section 18.1) has both functions. First the log difference:

```python
import numpy as np

before, after = 2032, 2067
d = np.log(after) - np.log(before)
print(f"ln(before) = {np.log(before):.4f}, ln(after) = {np.log(after):.4f}")
print(f"log difference d = {d:.4f}")
```

```
ln(before) = 7.6168, ln(after) = 7.6339
log difference d = 0.0171
```

- **`np.log(x)`** is the natural log, the spreadsheet's `LN`. (NumPy's name for it is `log`, not `ln`.)
- `d` is the log difference, 0.0171, as by hand.

Then back to a percentage, checked against the ordinary calculation:

```python
print(f"exp(d) - 1       = {np.exp(d) - 1:.4f}")
print(f"after/before - 1 = {after / before - 1:.4f}")
```

```
exp(d) - 1       = 0.0172
after/before - 1 = 0.0172
```

**`np.exp(d)`** is the spreadsheet's `EXP`. The two lines agree, so no information is lost by working in logs.

### Where the shortcut breaks

"A log difference is roughly the percentage" holds only for small changes. Before you run the next cell, predict: what percentage change is a log difference of 0.56?

```python
for d in [0.01, 0.05, 0.10, 0.56, -0.0729]:
    print(f"log difference {d:+.4f}  ->  {100 * (np.exp(d) - 1):+6.1f}%")
```

```
log difference +0.0100  ->    +1.0%
log difference +0.0500  ->    +5.1%
log difference +0.1000  ->   +10.5%
log difference +0.5600  ->   +75.1%
log difference -0.0729  ->    -7.0%
```

Up to 0.05 the two are nearly equal. At 0.10 they differ by half a point, and at 0.56 the change is **+75%, not +56%**. So this chapter never reads a log difference as a percentage directly: it always converts with exp(d) − 1. You'll meet both 0.56 and −0.0729 again.

### Why this chapter works in logs

Riverstone's West region sells about 3,300 orders a month and East about 1,500. If both grow by 8%, West gains about 264 orders and East about 120: different numbers of orders, the same growth. In logs, both rise by ln(1.08) = 0.077. So when a method asks whether North "moved like the other regions", comparing **changes in logs** asks whether they grew at the **same rate**, which is the fair question for regions of different sizes. That is why every comparison below is done in logs and converted back at the end.

---

## 31.1 The data, and the three true answers

### Building the data

The generator needs only the Python standard library. In a terminal, in the companion folder (with your Chapter 30 uv project, type `uv run python` instead of `python`, as in section 30.1):

```
# terminal, in companion/ch31
$ python generate_ch31_data.py
region_month 96 rows · qbr_program 240 customers (68 in the program) · delivery_threshold 60000 orders
$ ls causal_data
delivery_threshold.csv
qbr_program.csv
region_month.csv
```

The script writes a folder `causal_data` with three CSV files. The seed is fixed (31), so your files are identical to the book's.

### The first cell

Load all three and look at the first one:

```python
import numpy as np
import pandas as pd

panel = pd.read_csv("causal_data/region_month.csv", parse_dates=["month"])
qbr = pd.read_csv("causal_data/qbr_program.csv")
orders = pd.read_csv("causal_data/delivery_threshold.csv")

print(panel.head(3).to_string(index=False))
print(f"\npanel: {panel.shape[0]} region-months, {panel['region'].nunique()} regions, "
      f"{panel['month'].min():%b %Y} to {panel['month'].max():%b %Y}")
print(f"qbr:    {len(qbr)} accounts, {qbr['in_qbr_program'].sum()} in the program")
print(f"orders: {len(orders):,} orders around the ₹25,000 threshold")
```

```
region      month  orders     revenue  avg_order_value  price_rise_active  is_north  is_after
  West 2024-07-01    3125 77605843.75         24833.87                  0         0         0
  West 2024-08-01    3061 78519945.53         25651.73                  0         0         0
  West 2024-09-01    3419 85941317.41         25136.39                  0         0         0

panel: 96 region-months, 4 regions, Jul 2024 to Jun 2026
qbr:    240 accounts, 68 in the program
orders: 60,000 orders around the ₹25,000 threshold
```

- **`parse_dates=["month"]`** reads the `month` column as dates rather than text, so the code can compare and format them.
- **`.nunique()`** counts distinct values: four regions.
- The f-strings use some formats you haven't met; the box below lists every one this chapter uses.

> **Reading the f-string formats in this chapter.** Inside `{…}`, what follows the colon says how to show the value:
>
> - `:,.0f` adds thousands separators and no decimals: 2,032. `:.4f` gives four decimals: 0.0171.
> - `:+.1f` also shows the **sign**, even for positive numbers: +1.7 and −7.0. `:+d` does the same for whole numbers: +2.
> - `:%b %Y` formats a date as a short month and a year: Jul 2024.
> - `:>5` right-aligns the value in 5 characters, and `:6.1f` makes a number 6 characters wide, so columns of output line up.
> - Outside the braces, `'#' * 8` repeats a character: `########`. Section 31.4 uses it to draw a bar chart out of text.

The other two datasets, three rows each:

```python
print(qbr.head(3).to_string(index=False))
print()
print(orders.head(3).to_string(index=False))
```

```
 customer_id     segment region  years_as_customer  revenue_2024  growth_2024  in_qbr_program  revenue_2025
           1      Retail   East                  6    1015757.86       0.2296               0    1276212.05
           2      Retail  North                  3     169196.62       0.1483               0     174958.74
           3 Hospitality  North                  1     507678.95      -0.0138               1     577513.93

 order_id  order_value  free_delivery  repeat_within_90_days   segment region
        1     14813.32              0                      0    Retail  South
        2     25728.20              1                      1    Retail   East
        3     29660.00              1                      1 Wholesale  South
```

What each column means:

| Dataset | Column | Meaning |
|---|---|---|
| `region_month.csv` | `region`, `month` | one row per region per month; `month` is the first day of the month |
| | `orders`, `revenue`, `avg_order_value` | that month's orders, revenue (₹) and revenue per order (₹) |
| | `price_rise_active` | 1 for North from October 2025, when its prices were higher; otherwise 0 |
| | `is_north`, `is_after` | 1 for the North region; 1 for October 2025 onwards |
| `qbr_program.csv` | `customer_id`, `segment`, `region` | one row per key account |
| | `years_as_customer` | how long the account has bought from Riverstone |
| | `revenue_2024`, `revenue_2025` | the account's revenue (₹) in each year |
| | `growth_2024` | 2024 revenue growth over 2023, as a fraction: 0.052 is 5.2% |
| | `in_qbr_program` | 1 if the account got quarterly business reviews during 2025 |
| `delivery_threshold.csv` | `order_id`, `order_value` | one row per order; its value in ₹ |
| | `free_delivery` | 1 if the order value is ₹25,000 or more |
| | `repeat_within_90_days` | 1 if the customer ordered again within 90 days |
| | `segment`, `region` | the customer's segment and region |

Because the data is generated, the chapter can do something no real dataset allows: mark each method's homework.

| What happened | True effect | Method |
|---|---|---|
| North's list prices rose about 6% on 1 October 2025 | order volume **−8.0%** | difference-in-differences, synthetic control |
| Some key accounts were given quarterly business reviews during 2025 | revenue **+7.0%** | matching and propensity scores |
| Orders of ₹25,000 or more get free delivery | repeat-order rate **+6.0 points** | regression discontinuity |

Keep those three numbers in mind. Every estimate below should be judged against them, and none of them lands exactly.

---

## 31.2 Why the two obvious comparisons mislead

### Before and after

```python
panel["log_orders"] = np.log(panel["orders"])
north = panel[panel["region"] == "North"]
before = north.loc[north["is_after"] == 0, "orders"].mean()
after = north.loc[north["is_after"] == 1, "orders"].mean()

print(f"North, 15 months before the price rise: {before:,.0f} orders a month")
print(f"North, 9 months after:                  {after:,.0f} orders a month")
print(f"change: {100 * (after / before - 1):+.1f}%")
```

```
North, 15 months before the price rise: 2,032 orders a month
North, 9 months after:                  2,067 orders a month
change: +1.7%
```

- The first line adds a column of log orders (section 31.0) for every region-month. This comparison doesn't need it yet; every method after it does.
- `north` keeps North's 24 rows; `is_after` splits them into the 15 months before the change and the 9 after.

North's volume *went up* after a price rise that truly cost it 8% of its orders. Two things hide the damage: the business is growing by roughly three-quarters of a percent a month, and the price rose on 1 October, which is the start of the festive season. A before-and-after comparison credits the price rise with both.

### Treated against untreated

```python
post = panel[panel["is_after"] == 1]
north_post = post.loc[post["region"] == "North", "orders"].mean()
others_post = post.loc[post["region"] != "North", "orders"].mean()
print(f"North after:       {north_post:,.0f} orders a month")
print(f"Other regions after: {others_post:,.0f} orders a month")
print(f"difference: {100 * (north_post / others_post - 1):+.1f}%")
```

```
North after:       2,067 orders a month
Other regions after: 2,683 orders a month
difference: -23.0%
```

Worse. North is a smaller region than West or South and always was, so most of that gap is history, not the price rise. The comparison measures the wrong thing entirely.

These two failures have names worth knowing:

- **Confounding**: something else moved at the same time as the treatment (the season, the growth trend) and gets counted as the treatment's effect.
- **Selection**: the treated group differs from the untreated one for reasons that already affected the outcome (North was always smaller; the biggest accounts were chosen for the program).

The methods in this chapter are all attempts to remove one or both.

---

## 31.3 Difference-in-differences

**Difference-in-differences (DiD)** takes the change in the treated group and subtracts the change in an untreated group over the same period. Whatever moved both groups (season, growth, the economy) cancels out.

Work it as a two-by-two table of average log orders:

```python
panel["group"] = np.where(panel["region"] == "North", "North (treated)", "Other regions")
panel["period"] = np.where(panel["is_after"] == 1, "after", "before")
cells = panel.pivot_table(index="group", columns="period", values="log_orders", aggfunc="mean")
cells = cells[["before", "after"]]
cells["change"] = cells["after"] - cells["before"]

print(cells.round(4).to_string())
did = cells.loc["North (treated)", "change"] - cells.loc["Other regions", "change"]
print(f"\ndifference-in-differences (log): {did:+.4f}")
print(f"as a percentage change in orders: {100 * (np.exp(did) - 1):+.1f}%")
print("true effect: -8.0%")
```

```
period           before   after  change
group
North (treated)  7.6156  7.6328  0.0171
Other regions    7.7475  7.8375  0.0900

difference-in-differences (log): -0.0729
as a percentage change in orders: -7.0%
true effect: -8.0%
```

**How it works:**

- `np.where(test, a, b)` (section 18.1) labels each row: "North (treated)" or "Other regions", and "after" or "before".
- `pivot_table` (section 18.8) averages log orders for each group in each period, the four cells of the table. `cells[["before", "after"]]` puts the columns in time order.
- `cells.loc[row, column]` reads one cell. North's own change is small and positive (0.0171); the other regions' change over the same months is larger (0.0900). The *gap between the two changes*, 0.0171 − 0.0900 = −0.0729, is the estimate.
- Section 31.0's rule converts it: exp(−0.0729) − 1 = −7.0%. That's an honest result for 24 months of noisy data, against a true −8.0%, and a different universe from the +1.7% that before-and-after suggested.

### The same thing as a regression

The two-by-two table only works for one treated group and two periods. Written as a regression, DiD extends to many groups, many periods, and controls. It uses the **dummy variables** of section 22.10, columns that are 1 when something is true and 0 when it isn't, and one new column made by multiplying two of them. First, look at the three columns for each of the four cells:

```python
panel["treated"] = (panel["region"] == "North").astype(int)
dummies = panel.groupby(["group", "period"])[["treated", "is_after"]].first()
dummies["treated x is_after"] = dummies["treated"] * dummies["is_after"]
print(dummies.to_string())
```

```
                        treated  is_after  treated x is_after
group           period                                       
North (treated) after         1         1                   1
                before        1         0                   0
Other regions   after         0         1                   0
                before        0         0                   0
```

- `treated` is 1 for North; `is_after` is 1 from October 2025. `.first()` shows each cell's value once, since every row in a cell has the same values.
- `treated x is_after` is the two multiplied together. It is 1 in exactly one cell: **North, after the change**. That column is where the price rise lives.

In a statsmodels formula (section 30.11), `a:b` means "add a column that is a times b": an **interaction term**. So the regression is:

```python
import statsmodels.formula.api as smf

simple = smf.ols("log_orders ~ treated + is_after + treated:is_after", data=panel).fit()
print(simple.summary().tables[1])
```

```
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
Intercept            7.7475      0.045    171.944      0.000       7.658       7.837
treated             -0.1318      0.090     -1.463      0.147      -0.311       0.047
is_after             0.0900      0.074      1.224      0.224      -0.056       0.236
treated:is_after    -0.0729      0.147     -0.495      0.622      -0.365       0.219
====================================================================================
```

`.summary()` prints several tables; `.tables[1]` is the second, the coefficient table, which is all this chapter needs. Each coefficient is one piece of the two-by-two table, exactly as in section 22.10, where a 0/1 x made the slope a difference in means:

| Coefficient | Value | In the table |
|---|---|---|
| `Intercept` | 7.7475 | other regions, before: every dummy is 0 |
| `treated` | −0.1318 | North minus the others, before: 7.6156 − 7.7475 |
| `is_after` | 0.0900 | the other regions' change |
| `treated:is_after` | −0.0729 | the extra change in North: the DiD |

The interaction coefficient *is* difference-in-differences. Read its row aloud, as section 30.11 does: estimate −0.0729, standard error 0.147, t = −0.0729 ÷ 0.147 = −0.495, p = 0.622, and a 95% interval from −0.365 to +0.219. That interval is uselessly wide, because this model explains every difference between the 96 rows with three dummies, and everything else (the months, the regions' own levels) is left in the noise.

### Fixed effects: one dummy per region and per month

**Fixed effects** give every region its own dummy and every month its own dummy, so the model can soak up "West is always bigger" and "October is always busy" before it looks at the price rise. `C(region)` and `C(month)` do it, as `C()` did for categories in section 30.11:

```python
fe = smf.ols("log_orders ~ treated:is_after + C(region) + C(month)", data=panel).fit()
names = pd.Series(fe.params.index)
print(len(names), "coefficients")
print(names.str.split("[").str[0].value_counts().to_string())
```

```
28 coefficients
C(month)            23
C(region)            3
Intercept            1
treated:is_after     1
```

- The model has 28 coefficients: the intercept, 3 region dummies (one region is the baseline, as in section 30.11), 23 month dummies (one month is the baseline), and the interaction.
- Each `C(month)` coefficient is **that month's shared shock**: how far every region's log orders sat from the baseline month. Each `C(region)` coefficient is that region's usual level.
- `names.str.split("[").str[0]` keeps the part of each name before the first `[`, so the counts group `C(month)[T.Timestamp('2024-08-01 00:00:00')]` and its 22 siblings together.
- `treated` and `is_after` are left out on purpose. `C(region)` already knows which region is North, and `C(month)` already knows which months are after the change, so the two columns would repeat information the dummies hold. They are **absorbed** by the fixed effects.

The estimate and its interval:

```python
effect = fe.params["treated:is_after"]
ci = fe.conf_int().loc["treated:is_after"]
print(f"effect (log): {effect:+.4f}")
print(ci.round(4).to_string())
```

```
effect (log): -0.0729
0   -0.1064
1   -0.0394
```

`fe.params[...]` reads one coefficient. `fe.conf_int()` is a table of every coefficient's 95% interval, and `.loc["treated:is_after"]` takes its row: two numbers, labelled `0` (the lower end) and `1` (the upper end). So `ci[0]` is the lower end and `ci[1]` the upper. Converted to percentages:

```python
print(f"as a percentage: {100 * (np.exp(effect) - 1):+.1f}%  "
      f"(CI {100 * (np.exp(ci[0]) - 1):+.1f}% to {100 * (np.exp(ci[1]) - 1):+.1f}%)")
print(f"R-squared: {fe.rsquared:.3f}")
```

```
as a percentage: -7.0%  (CI -10.1% to -3.9%)
R-squared: 0.991
```

Same estimate, a far tighter interval, and the true −8% sits comfortably inside it. **Region fixed effects** absorb "North is smaller"; **month fixed effects** absorb the festive season and everything else that hit all regions at once. **R²** (section 22.10) is 0.991: regions and months explain almost all of the variation in log orders, which leaves a small residual, and a small residual gives a tight interval.

> **Watch out: four regions is not many.** The interval above treats all 96 region-months as independent pieces of evidence. They aren't: a region's months are related to each other, since whatever made North unusual in March probably still applies in April. **Clustering** tells the formula to treat each region as one block of evidence: `smf.ols("log_orders ~ treated:is_after + C(region) + C(month)", data=panel).fit(cov_type="cluster", cov_kwds={"groups": panel["region"]})`. Here `cov_type="cluster"` asks for clustered standard errors, and `cov_kwds={"groups": ...}` names the column that says which block each row belongs to. But the clustering formula itself needs many clusters, and with only four it is unreliable in both directions (exercise 7 shows it). The honest options are resampling methods designed for few groups, of which the placebo test in exercise 6 is the simplest, or a clearly stated caveat. If your DiD has a handful of groups, say so in the write-up rather than quoting a tidy p-value.

---

## 31.4 The assumption: parallel trends

DiD rests on one assumption: **without the price rise, North's orders would have moved like the other regions' orders.** That world doesn't exist, so it can't be tested. What can be tested is whether the two moved together *before* the change.

First, a table with one row per month: North's log orders, the other regions' average, and the gap between them:

```python
monthly = (panel.assign(side=np.where(panel["treated"] == 1, "North", "Others"))
                .pivot_table(index="month", columns="side", values="log_orders", aggfunc="mean"))
monthly["gap"] = monthly["North"] - monthly["Others"]
print(monthly.round(3).head(3).to_string())
```

```
side        North  Others    gap
month                           
2024-07-01  7.533   7.654 -0.121
2024-08-01  7.578   7.734 -0.157
2024-09-01  7.623   7.791 -0.168
```

- `.assign(side=...)` (section 18.6) adds a column labelling each row "North" or "Others", without changing `panel` itself.
- The `pivot_table` averages log orders by month and side: for "Others" that's the mean of three regions.
- `gap` is North minus the others. It is negative because North is smaller; what matters is whether it **stays level**.

Split the months at the change:

```python
pre = monthly[monthly.index < "2025-10-01"]
post = monthly[monthly.index >= "2025-10-01"]
print(len(pre), "months before,", len(post), "after")
```

```
15 months before, 9 after
```

The index holds dates, and pandas compares a date with a date written as text, so `< "2025-10-01"` keeps the months before October 2025.

Now the summary numbers:

```python
print("gap between North and the other regions (log orders)")
print(f"  before the price rise: mean {pre['gap'].mean():+.4f}, sd {pre['gap'].std():.4f}")
print(f"  after:                 mean {post['gap'].mean():+.4f}")
```

```
gap between North and the other regions (log orders)
  before the price rise: mean -0.1318, sd 0.0446
  after:                 mean -0.2047
```

The gap's average falls from −0.1318 to −0.2047, a change of −0.0729: the DiD again. Its standard deviation before the change (Chapter 21) says how much it wanders month to month: about 4.5%.

Is the gap drifting? Fit a straight line through the fifteen pre-change gaps, against month number 0, 1, 2 … 14, with section 22.10's `linregress`, and read its slope:

```python
from scipy import stats

drift = stats.linregress(range(len(pre)), pre["gap"]).slope
print(f"drift per month before the change: {drift:+.5f}")
print(pre["gap"].round(3).tail(4).to_string())
```

```
drift per month before the change: -0.00175
month
2025-06-01   -0.044
2025-07-01   -0.170
2025-08-01   -0.182
2025-09-01   -0.196
```

- `range(len(pre))` is the month numbers 0 to 14, the x; `pre["gap"]` is the y. `.slope` is the change in the gap per month.
- `.tail(4)` shows the last four pre-change months.

**Reading it:** before the change, the gap wanders with a standard deviation of about 4.5% and drifts by −0.18% a month, which over fifteen months comes to about a third of the effect being measured: small, but not zero. After the change the gap drops by about 7 points and stays there. The last three pre-change months (July to September 2025) all sit below the pre-change average of −0.132, which is why the next check tracks the gap over time instead of comparing two averages.

![A line chart of log orders for North and the average of the other regions over 24 months: the two lines move together until October 2025, when North steps down and stays lower](figures/fig31-1-parallel-trends.svg)

*Figure 31.1 — Parallel before, a step at the change, parallel again after. This picture belongs in every DiD write-up.*

### A quarter-by-quarter view

A stricter look tracks the gap over time rather than averaging the whole period. Single months are too noisy for one region, so group them into quarters around the change, measured against the average gap in the fifteen months before it:

```python
monthly["rel"] = ((monthly.index.year - 2025) * 12 + monthly.index.month - 10)
baseline = monthly.loc[monthly["rel"] < 0, "gap"].mean()          # the whole pre-change period
monthly["quarter"] = np.floor(monthly["rel"] / 3).astype(int)
view = (monthly.groupby("quarter")["gap"].mean() - baseline).round(3)
for quarter, value in view.items():
    when = "before" if quarter < 0 else "after "
    print(f"quarter {quarter:+d} ({when}): {value:+.3f} {'#' * int(abs(value) * 100)}")
```

```
quarter -5 (before): -0.016 #
quarter -4 (before): +0.010 #
quarter -3 (before): +0.040 ####
quarter -2 (before): +0.017 #
quarter -1 (before): -0.051 #####
quarter +0 (after ): -0.082 ########
quarter +1 (after ): -0.041 ####
quarter +2 (after ): -0.096 #########
```

- `rel` counts months relative to the change: October 2025 is 0, September 2025 is −1, July 2024 is −15.
- `np.floor(rel / 3)` rounds down to whole quarters, so months −3 to −1 are quarter −1 and months 0 to 2 are quarter 0. `.astype(int)` makes them whole numbers.
- `view` is each quarter's average gap minus the pre-change baseline. The loop prints it, with one `#` per point (section 31.1's box).

Four of the five quarters before the change sit within four points of the baseline, with no direction to them. But the quarter just before the change is already 5 points low, about two-thirds of the effect. That could be noise (single quarters of one region move this much: see quarter −3 at +4) or the start of the fall. It is why exercise 13 re-estimates with a trend for North, and why the write-up should say "parallel for twelve of the fifteen months, with a dip in the last quarter". Every quarter after the change sits between four and ten points below.

Done properly as a regression, with a confidence interval for each period, this quarter-by-quarter view is called an **event study**. With one treated region and 24 months there isn't enough data for a formal event-study regression with trustworthy intervals, and pretending otherwise would be exactly the kind of tidy-looking mistake this chapter warns about.

> **Watch out: parallel trends can fail quietly.** Common causes: the treated group was picked *because* it was already declining (Riverstone might have raised prices in North precisely because volume was soft); a different event hit only the treated group at the same time; or the groups have different seasonal patterns. Check what you can, and name what you can't: *"we assume the North region would have grown like the others, which held for most of the fifteen months we can see, with a dip in the last quarter before the change."*

---

## 31.5 Synthetic control

DiD compares North with the *average* of the other regions. But West is over one and a half times North's size and East is smaller; why should their plain average be the right stand-in?

**Synthetic control** builds a better one: a weighted blend of the untreated regions, with the weights chosen so the blend tracks the treated region as closely as possible *before* the change. Then it carries those weights forward and compares. The untreated regions it can draw on are the **donor pool**.

### The idea, by hand

A blend is a weighted sum: with weights 0.2 for West, 0.3 for South and 0.5 for East, the synthetic North in a month is 0.2 × West + 0.3 × South + 0.5 × East, in log orders. The weights are never negative and add up to 1, so the blend is a genuine mixture of the donors. To score a set of weights, compare the blend with the real North in each of the fifteen months before the change, square each miss, and average the squares: that average is the **loss**. The best weights are the ones with the smallest loss.

Start with one row per month and one column per region, and save the pre-change months for the spreadsheet:

```python
wide_panel = panel.pivot_table(index="month", columns="region", values="log_orders")
pre_period = wide_panel[wide_panel.index < "2025-10-01"]
print(len(pre_period), "months before the change")
print(pre_period.round(3).head(3).to_string())
pre_period.to_csv("causal_data/pre_period_logs.csv")
```

```
15 months before the change
region       East  North  South   West
month                                 
2024-07-01  7.224  7.533  7.690  8.047
2024-08-01  7.315  7.578  7.861  8.026
2024-09-01  7.347  7.623  7.888  8.137
```

`to_csv` writes the fifteen rows to `causal_data/pre_period_logs.csv`.

### In a spreadsheet

Open `pre_period_logs.csv`. The months are in A2:A16, and the columns are in alphabetical order: East in B, North in C, South in D, West in E.

1. Put the three weights in H2 (East), I2 (South), and J2 (West), each `=1/3` to start. In K2, `=SUM(H2:J2)` checks they add up to 1.
2. The blend in F2: `=B2*$H$2+D2*$I$2+E2*$J$2`, filled down to F16. (`SUMPRODUCT`, section 11.2, does the same in one function when the columns sit side by side.)
3. The squared miss in G2: `=(C2-F2)^2`, filled down.
4. The loss in G18: `=AVERAGE(G2:G16)`. With equal weights it is 0.0192.
5. Now think: North's average log orders, 7.62, sits between South's 7.82 and East's 7.31, and West, at 8.11, is far above it. Try 0.5 for East, 0.5 for South and 0 for West. The loss drops to 0.0044.

In Excel, the **Solver** add-in (section 11.9) can search for the best weights: set the objective to G18, **To: Min**, by changing H2:J2, add the constraint K2 = 1, tick **Make Unconstrained Variables Non-Negative**, and choose the **GRG Nonlinear** method. Python does the same search below.

### The same blend in Python

First the equal-weight blend, exactly as in the spreadsheet:

```python
donors = ["West", "South", "East"]
w = np.array([1/3, 1/3, 1/3])
blend = (pre_period[donors] * w).sum(axis=1)
loss_equal = ((pre_period["North"] - blend) ** 2).mean()
print(f"loss with equal weights: {loss_equal:.4f}")
```

```
loss with equal weights: 0.0192
```

- `pre_period[donors] * w` multiplies each donor's column by its weight: West by the first number, South by the second, East by the third.
- `.sum(axis=1)` adds across each row (section 18.6's `axis=1`), giving one blended value per month: column F of the spreadsheet.
- The last calculation squares each month's miss and averages: the loss, 0.0192, as in G18.

Wrap the loss in a function, so any weights can be scored:

```python
def loss(weights):
    blend = (pre_period[donors] * weights).sum(axis=1)
    return ((pre_period["North"] - blend) ** 2).mean()

print(f"equal weights:            {loss(np.array([1/3, 1/3, 1/3])):.4f}")
print(f"South and East, half each: {loss(np.array([0, 0.5, 0.5])):.4f}")
```

```
equal weights:            0.0192
South and East, half each: 0.0044
```

The spreadsheet's two numbers again. Row by row, the blend is a `SUMPRODUCT` of the three donors and the three weights. NumPy has an operator for exactly that, applied to every row at once: **`@`**, the **matrix product**. Chapter 35 explains it fully; here it only needs to mean "multiply each row by the weights and add up". Check that it gives the same numbers:

```python
by_columns = (pre_period[donors] * w).sum(axis=1)
by_matrix = pre_period[donors].to_numpy() @ w
print(by_columns.head(3).round(4).to_list())
print(by_matrix[:3].round(4))
```

```
[7.6537, 7.7342, 7.7907]
[7.6537 7.7342 7.7907]
```

`.to_numpy()` turns the three columns into a plain NumPy array, which `@` needs. The two lines agree, so from here on either form will do.

### Letting the computer search: `minimize`

Trying weights by hand is slow. SciPy's **`minimize`** tries weights for you, moving them in whichever direction lowers the loss, until it can't go lower. It needs the rules, too: each weight between 0 and 1, and the three adding up to 1.

```python
from scipy.optimize import minimize

start = np.array([1/3, 1/3, 1/3])
bounds = [(0, 1)] * 3
constraint = {"type": "eq", "fun": lambda w: w.sum() - 1}   # zero when weights add up to 1
best = minimize(loss, start, bounds=bounds, constraints=[constraint], method="SLSQP")
print(best.success)
weights = {d: round(float(x), 3) for d, x in zip(donors, best.x)}
print("synthetic North =", weights)
print(f"loss at these weights: {best.fun:.5f}")
```

```
True
synthetic North = {'West': 0.187, 'South': 0.303, 'East': 0.509}
loss at these weights: 0.00184
```

- **`minimize(loss, start, ...)`** takes the function to make small and the weights to start from, the spreadsheet's `=1/3` cells.
- **`bounds`** gives each weight a lowest and highest value. `[(0, 1)] * 3` repeats the pair three times, as `'#' * 8` repeats a character.
- **`constraint`** is a rule the weights must obey. `"type": "eq"` means "must equal zero", and the `lambda` (section 18.6) returns the weights' sum minus 1, which is zero exactly when they add up to 1: Solver's K2 = 1.
- **`method="SLSQP"`** picks a search method that can handle bounds and an equality rule together.
- **`best.success`** is `True` when the search finished properly; **`best.x`** holds the weights it found, and **`best.fun`** the loss there, far below the 0.0044 found by hand. The dictionary comprehension (section 17.7) pairs each donor with its weight, and `round(float(x), 3)` turns each into a plain number with three decimals.

The weights add up to 0.999 only because each is rounded to three places.

### The estimate

Carry the weights forward over all 24 months, and measure how far North sits from its double:

```python
synthetic = (wide_panel[donors] * best.x).sum(axis=1)
gap = wide_panel["North"] - synthetic
fit_before = np.sqrt((gap[gap.index < "2025-10-01"] ** 2).mean())
print(f"pre-change fit (root mean squared error, log orders): {fit_before:.4f}")
```

```
pre-change fit (root mean squared error, log orders): 0.0429
```

`fit_before` is the square root of the pre-change loss, the **root mean squared error**: the typical miss before the change, in log orders. About 0.043 is a close fit. Now the months after:

```python
gap_after = gap[gap.index >= "2025-10-01"].mean()
print(f"average gap after the change: {gap_after:+.4f} log points "
      f"= {100 * (np.exp(gap_after) - 1):+.1f}%")
print("true effect: -8.0%")
```

```
average gap after the change: -0.0685 log points = -6.6%
true effect: -8.0%
```

![A line chart of North's log orders against its synthetic control: the two track closely for fifteen months, then separate at the price rise, with the gap shaded](figures/fig31-2-synthetic-control.svg)

*Figure 31.2 — The synthetic region is built only from pre-change data. Everything after the line is the estimate.*

**How it works and what to watch:**

- The weights are non-negative and sum to 1, so the synthetic region is a genuine blend, not an extrapolation. That restraint is what keeps the method honest.
- **Judge it by the pre-change fit first.** A synthetic control that doesn't track the treated unit before the change has no claim to track it after.
- With four regions there are only three donors, so the method is doing little more than a weighted DiD. Synthetic control earns its keep with dozens of candidate donors: shops, cities, states, or customers.
- **Inference** is done by pretending each untreated unit was treated (a **placebo test**) and asking how unusual the real gap looks against theirs. Exercise 11 does this.

> **Watch out: donors must be untouched.** If the price rise spilled into a neighboring region (customers near the border ordering from West instead), West is contaminated and the estimate shrinks toward zero. Ask, every time: could the treatment have affected the comparison group? The same question ruins many DiD studies, and it has a name: **interference** between units.

### Checkpoint: the end of Part A

Before Part B, do one difference-in-differences entirely by hand, with East as the only comparison region. The average log orders are:

| | before | after |
|---|---|---|
| North | 7.6156 | 7.6328 |
| East | 7.3118 | 7.3924 |

Compute each region's change, subtract East's from North's, and convert with exp(d) − 1. Then check your answer against exercise 5, which fits the same comparison as a regression. (The answer: 0.0172 − 0.0806 = −0.0634, which is −6.1%; exercise 5 prints −6.2%, because the table is rounded to four decimals.) If that felt routine, go on. If not, reread sections 31.0 and 31.3 first: everything in Part B builds on them.

---

## 31.6 Matching and propensity scores

Quarterly business reviews went to 68 of Riverstone's 240 key accounts. The naive comparison is spectacular and wrong:

```python
qbr["log_2025"] = np.log(qbr["revenue_2025"])
qbr["log_2024"] = np.log(qbr["revenue_2024"])
naive = (qbr.groupby("in_qbr_program")
            .agg(accounts=("customer_id", "count"),
                 revenue_2024=("revenue_2024", "mean"),
                 revenue_2025=("revenue_2025", "mean"),
                 growth_2024=("growth_2024", "mean")))
print(naive.round(3).to_string())
```

```
                accounts  revenue_2024  revenue_2025  growth_2024
in_qbr_program                                                   
0                    172    755520.916    824816.990        0.052
1                     68   1225516.825   1420723.119        0.062
```

The accounts in the program were already about 1.6 times the size of the others *before* it started (₹12.3 lakh against ₹7.6 lakh on average), and growing faster. Selection, in one table. Now the naive estimate, in logs as always:

```python
means = qbr.groupby("in_qbr_program")["log_2025"].mean()
print(means.round(4).to_string())
gap = means[1] - means[0]
print(f"\nnaive difference in 2025 revenue: {100 * (np.exp(gap) - 1):+.1f}%")
print("true effect: +7.0%")
```

```
in_qbr_program
0    13.3138
1    13.8733

naive difference in 2025 revenue: +75.0%
true effect: +7.0%
```

- `means` holds the average log 2025 revenue of non-participants (row `0`) and participants (row `1`).
- `means[1] - means[0]` is the difference, converted to a percentage as in section 31.0.

The +75% compares average *log* revenue, which weights every account equally in percentage terms. The plain averages in the table give ₹14,20,723 ÷ ₹8,24,817 − 1 = +72%. Either way, the gap is mostly selection.

**Matching** answers a narrower question: for each account that joined, what happened to a similar account that didn't? A **propensity score** compresses "similar" into one number: the modelled probability of joining, given what was known beforehand.

### A propensity score, by hand first

Section 30.11 used logistic regression to read odds ratios. Here it is used for its other job: **turning a score into a probability**. The model adds up a score, z = b₀ + b₁ × log_2024 + b₂ × growth_2024 + …, exactly like a linear regression, and then squeezes z into the range 0 to 1 with the S-shaped **logistic function**:

> p = 1 / (1 + e^(−z))
>
> A z of 0 gives p = 0.5; large positive z gives p near 1; large negative z gives p near 0.

The model uses only things known **before** the program started: 2024 revenue, 2024 growth, tenure, and segment (Common mistakes and exercise 16 say why that matters). Fit it and look at its coefficients:

```python
score_model = smf.logit("in_qbr_program ~ log_2024 + growth_2024 + years_as_customer + C(segment)",
                        data=qbr).fit(disp=False)
print(score_model.params.round(4).to_string())
```

```
Intercept                 -12.9603
C(segment)[T.Retail]       -0.3170
C(segment)[T.Wholesale]     0.4500
log_2024                    0.8544
growth_2024                 0.8568
years_as_customer           0.0964
```

`smf.logit` is section 30.11's logistic regression; `disp=False` stops it printing its fitting progress. Hospitality is the baseline segment, so a Retail account adds the `C(segment)[T.Retail]` coefficient and a Hospitality account adds nothing.

Now work the first account by hand: a Retail account with ₹10,15,758 of 2024 revenue, 2024 growth of 0.2296, and 6 years as a customer:

```python
first = qbr.iloc[0]
b = score_model.params
z = (b["Intercept"] + b["C(segment)[T.Retail]"] + b["log_2024"] * first["log_2024"]
     + b["growth_2024"] * first["growth_2024"] + b["years_as_customer"] * first["years_as_customer"])
p = 1 / (1 + np.exp(-z))
print(f"account {first['customer_id']}: log_2024 = {first['log_2024']:.4f}, z = {z:.4f}, p = {p:.4f}")
print(f"the model's predict gives: {score_model.predict(qbr.iloc[[0]]).iloc[0]:.4f}")
```

```
account 1: log_2024 = 13.8311, z = -0.6851, p = 0.3351
the model's predict gives: 0.3351
```

- `z` adds up the coefficients times the account's values, one term per line of the formula.
- `p` is the logistic function; in a spreadsheet, with z in A1, it is `=1/(1+EXP(-A1))`, which turns z = −0.6851 into 0.3351.
- **`score_model.predict(...)`** does the same arithmetic for any rows you give it. `qbr.iloc[[0]]` (double brackets) passes a one-row table, and the result matches the hand calculation.

So the propensity score is nothing more mysterious than a weighted sum passed through the S-curve. Chapter 37 teaches logistic regression as a prediction model in its own right. Now score every account:

```python
qbr["propensity"] = score_model.predict(qbr)
summary = qbr.groupby("in_qbr_program")["propensity"].describe()
print(summary[["count", "mean", "min", "max"]].round(3).to_string())
```

```
                count   mean    min    max
in_qbr_program
0               172.0  0.255  0.032  0.686
1                68.0  0.354  0.130  0.802
```

`predict(qbr)` returns one probability per account. `.describe()` summarizes each group, and the list in brackets keeps four of its columns.

The two groups overlap but sit in different parts of the range, which is exactly what a selected program looks like. **Overlap** (also called **common support**) is the part of the range where both groups have accounts. A participant scored above every non-participant (above 0.686 here) has no comparable control, which is why the matching below refuses matches that aren't close.

### Matching, by hand

The rule: take the participants from the highest score down; give each the non-participant with the nearest score, provided it is within 0.05 (the **caliper**); and remove that control so nobody is used twice (**matching without replacement**). A toy example with four participants and six controls:

| Participant | Score | Nearest available control | Distance | Result |
|---|---|---|---|---|
| A | 0.60 | P (0.57) | 0.03 | matched; P removed |
| B | 0.48 | Q (0.51) | 0.03 | matched; Q removed (R, at 0.44, is 0.04 away) |
| C | 0.35 | S (0.33) | 0.02 | matched; S removed |
| D | 0.20 | T (0.10) | 0.10 | **unmatched**: over the 0.05 caliper |

The controls were P 0.57, Q 0.51, R 0.44, S 0.33, T 0.10, and U 0.70. Three pairs; D goes unmatched, and R and U are never used. Now the same steps in Python, one at a time.

First, the two groups, and the controls as a dictionary of `customer_id: score`, from which matched controls can be deleted:

```python
participants = qbr[qbr["in_qbr_program"] == 1].copy()
controls = qbr[qbr["in_qbr_program"] == 0].copy()
available = controls.set_index("customer_id")["propensity"].to_dict()
print(len(participants), "participants,", len(available), "controls available")
print({cid: round(score, 3) for cid, score in list(available.items())[:3]})
```

```
68 participants, 172 controls available
{1: 0.335, 2: 0.071, 4: 0.155}
```

`set_index("customer_id")["propensity"]` makes a Series whose labels are customer ids, and `.to_dict()` turns it into a dictionary (Chapter 17). The last line shows its first three entries.

Second, match the highest-scoring participant only:

```python
ordered = participants.sort_values("propensity", ascending=False)
top = ordered.iloc[0]
best = min(available, key=lambda cid: abs(available[cid] - top["propensity"]))
print(f"participant {top['customer_id']}: score {top['propensity']:.3f}")
print(f"nearest control {best}: score {available[best]:.3f}, "
      f"distance {abs(available[best] - top['propensity']):.3f}")
```

```
participant 74: score 0.802
nearest control 133: score 0.686, distance 0.116
```

- `ordered` puts participants from the highest score down.
- **`min(available, key=...)`** looks at every key of the dictionary and returns the one whose `key` value is smallest. The `lambda` gives each control id its distance from this participant's score, so `best` is **the control whose distance is smallest**.
- The distance is well over 0.05. This participant, with the highest score of all, sits outside the overlap: the caliper will refuse the match.

Third, the loop, which does that for every participant in turn:

```python
pairs = []
for row in ordered.itertuples():
    if not available:
        break
    best = min(available, key=lambda cid: abs(available[cid] - row.propensity))
    if abs(available[best] - row.propensity) <= 0.05:     # the caliper
        pairs.append((row.customer_id, best))
        del available[best]                               # without replacement
print(f"matched pairs: {len(pairs)} of {len(participants)} participants")
print(f"unmatched participants: {len(participants) - len(pairs)} (no close enough comparison existed)")
for participant_id, control_id in pairs[:3]:
    print(f"  participant {participant_id} <-> control {control_id}")
```

```
matched pairs: 64 of 68 participants
unmatched participants: 4 (no close enough comparison existed)
  participant 67 <-> control 133
  participant 126 <-> control 112
  participant 239 <-> control 187
```

- **`.itertuples()`** (section 18.1) hands over one participant at a time, so `row.propensity` is that participant's score. A row loop is fine here: 68 rows, and each step depends on the ones before it, because matched controls are removed.
- **`if not available: break`** stops early if the controls run out (section 17.6's `break`).
- **`<= 0.05`** is the caliper: a pair is kept only if the scores are close.
- **`del available[best]`** removes the matched control from the dictionary, so it can't be matched again.

Fourth, collect every matched account and keep those rows:

```python
matched_ids = []
for participant_id, control_id in pairs:
    matched_ids.append(participant_id)
    matched_ids.append(control_id)
matched = qbr[qbr["customer_id"].isin(matched_ids)]
print(len(matched), "accounts in the matched sample")
print(matched["in_qbr_program"].value_counts().to_string())
```

```
128 accounts in the matched sample
in_qbr_program
0    64
1    64
```

`isin` (section 18.4) keeps the rows whose id is in the list: 64 participants and their 64 controls.

### Check balance before believing anything

Matching is only worth something if the matched groups now look alike on everything you matched on. The usual measure is the **standardized mean difference** (SMD), the same idea as section 30.4's Cohen's d:

> **SMD = (mean₁ − mean₀) ÷ √((s₁² + s₀²) ÷ 2)**
>
> - mean₁ and mean₀ are the participants' and the non-participants' averages.
> - s₁² and s₀² are their variances (Chapter 21: the standard deviation squared). The bottom line is the **pooled standard deviation**: the square root of the average of the two variances, so the gap is measured in standard deviations.
> - The common rule of thumb: **|SMD| under 0.1** means the groups are balanced on that variable. The sign only says which group is higher.

By hand for 2024 revenue (in logs), before matching:

```python
print(qbr.groupby("in_qbr_program")["log_2024"].agg(["mean", "std"]).round(4).to_string())
```

```
                   mean     std
in_qbr_program                 
0               13.2417  0.7658
1               13.7154  0.7256
```

(13.7154 − 13.2417) ÷ √((0.7256² + 0.7658²) ÷ 2) = 0.4737 ÷ √0.5565 = 0.4737 ÷ 0.7460 = **0.635**. Now the same formula as a function, for every variable, before and after matching:

```python
def smd(data, column):
    a = data.loc[data["in_qbr_program"] == 1, column]
    b = data.loc[data["in_qbr_program"] == 0, column]
    return (a.mean() - b.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)

rows = []
for column in ["log_2024", "growth_2024", "years_as_customer", "propensity"]:
    rows.append({"variable": column, "before matching": smd(qbr, column),
                 "after matching": smd(matched, column)})
print(pd.DataFrame(rows).round(3).to_string(index=False))
```

```
         variable  before matching  after matching
         log_2024            0.635           0.002
      growth_2024            0.082          -0.098
years_as_customer            0.239           0.106
       propensity            0.683           0.033
```

`a` and `b` are the two groups' values; `.var(ddof=1)` is the sample variance, as in section 30.4. The first row is the hand answer, 0.635, falling to 0.002 after matching.

Two variables are borderline: tenure is still 0.106, just over the rule, and 2024 growth is −0.098, just under it. Report that, and include them in the outcome regression below as a second line of defence. Segment is a category, so compare its shares instead:

```python
for label, data in (("before matching", qbr), ("after matching", matched)):
    print(label)
    print(pd.crosstab(data["in_qbr_program"], data["segment"], normalize="index").round(3).to_string())
```

```
before matching
segment         Hospitality  Retail  Wholesale
in_qbr_program                                
0                     0.297   0.506      0.198
1                     0.309   0.412      0.279
after matching
segment         Hospitality  Retail  Wholesale
in_qbr_program                                
0                     0.281   0.438      0.281
1                     0.281   0.438      0.281
```

`pd.crosstab` (section 21.6) counts each combination; `normalize="index"` turns each row's counts into shares that add up to 1. Before matching, participants were less often Retail (41% against 51%) and more often Wholesale (28% against 20%); after matching the two groups' shares are identical. Segment goes into the outcome regression too.

![Standardized mean differences before and after matching for prior revenue, growth, tenure, and propensity, drawn as hollow and filled markers on a scale from -0.2 to 0.8 with the ±0.1 band shaded](figures/fig31-3-matching-balance.svg)

*Figure 31.3 — Balance is the checkable part of matching. Report it, or the estimate means nothing.*

### The estimate

Two corrections: the difference in log 2025 revenue within the matched sample, and a **regression adjustment** on all 240 accounts that holds the pre-program variables fixed (section 22.10's "more than one x"):

```python
matched_means = matched.groupby("in_qbr_program")["log_2025"].mean()
matched_effect = matched_means[1] - matched_means[0]
model = smf.ols("log_2025 ~ in_qbr_program + log_2024 + growth_2024 + years_as_customer + C(segment)",
                data=qbr).fit()
adjusted = model.params["in_qbr_program"]
ci = model.conf_int().loc["in_qbr_program"]

print(f"naive:                  {100 * (np.exp(gap) - 1):+.1f}%")
print(f"after matching:         {100 * (np.exp(matched_effect) - 1):+.1f}%")
print(f"regression adjustment:  {100 * (np.exp(adjusted) - 1):+.1f}%  "
      f"(95% CI {100 * (np.exp(ci[0]) - 1):+.1f}% to {100 * (np.exp(ci[1]) - 1):+.1f}%)")
print("true effect:            +7.0%")
```

```
naive:                  +75.0%
after matching:         +7.1%
regression adjustment:  +7.5%  (95% CI +4.4% to +10.7%)
true effect:            +7.0%
```

Both corrections land near the truth, and both are a world away from the naive +75%. Note what made this work: every variable that drove selection (size, growth, tenure) was **measured and available**. That is the assumption matching rests on, and it has a name.

> **Watch out: matching only fixes what you measured.** The assumption is **no unmeasured confounding**: nothing you left out of the score influenced both joining and the outcome. Here it holds by construction, because the data was generated that way. In real life, the sales team's judgment about which accounts "had potential" is exactly the kind of unmeasured variable that ruins it. That's why matching is weaker evidence than a threshold rule or an experiment, and why sensitivity analysis (section 31.9) matters.

---

## 31.7 Regression discontinuity: let the rule do the randomizing

Riverstone's delivery policy: orders of ₹25,000 or more ship free; smaller orders pay a delivery charge. Does free delivery bring customers back?

Comparing all orders above the threshold with all orders below it is hopeless: big orders come from big customers, who reorder anyway. But an order of ₹24,900 and one of ₹25,100 are placed by much the same kind of customer, in much the same mood. One gets free delivery and one doesn't, for a reason that has nothing to do with either. **Just around the threshold, the rule is as good as a coin flip.** That's **regression discontinuity (RD)**.

The number that decides which side of the rule an order falls on, here the order value, is called the **running variable**. Measure it from the cut-off, in thousands of rupees, so that 0 means exactly ₹25,000:

```python
orders["centred"] = (orders["order_value"] - 25_000) / 1000     # ₹ thousands from the cut-off
wide = orders[orders["centred"].abs() <= 5]
below = wide[wide["centred"] < 0]["repeat_within_90_days"]
above = wide[wide["centred"] >= 0]["repeat_within_90_days"]

print(f"orders within ₹5,000 of the threshold: {len(wide):,}")
print(f"just below: {100 * below.mean():.1f}% reorder within 90 days  (n = {len(below):,})")
print(f"just above: {100 * above.mean():.1f}%                          (n = {len(above):,})")
print(f"raw gap: {100 * (above.mean() - below.mean()):+.1f} points")
```

```
orders within ₹5,000 of the threshold: 46,054
just below: 31.4% reorder within 90 days  (n = 22,958)
just above: 42.4%                          (n = 23,096)
raw gap: +11.0 points
```

- `centred` is −0.1 for a ₹24,900 order and +0.1 for ₹25,100. `25_000` is 25,000; Python ignores the underscore, which is there for reading.
- `wide` keeps orders within ₹5,000 either side; `below` and `above` split them at the cut-off, with exactly ₹25,000 counted above, as the rule says.
- The mean of a 0/1 column is a share, so `below.mean()` is the reorder rate.

The raw gap overstates things, because the chance of reordering rises with order value anyway. RD fits a line on each side and measures the **jump at the cut-off**, not the level. One regression does both lines, using an interaction as in section 31.3:

```python
rd = smf.ols("repeat_within_90_days ~ free_delivery + centred + free_delivery:centred", data=wide).fit()
print(rd.params.round(4).to_string())
```

```
Intercept                0.3312
free_delivery            0.0726
centred                  0.0079
free_delivery:centred    0.0013
```

With b₀ to b₃ the four coefficients in that order, the two fitted lines are:

- **below the cut-off** (free_delivery = 0): ŷ = b₀ + b₂ × centred
- **above it** (free_delivery = 1): ŷ = (b₀ + b₁) + (b₂ + b₃) × centred

So `free_delivery:centred` lets the slope differ above the cut-off, and because centred = 0 *is* ₹25,000, **b₁, the `free_delivery` coefficient, is the gap between the two lines exactly at the threshold**: the jump. The outcome is 0 or 1, so a straight-line regression on it (a **linear probability model**) gives answers in probability points; that's fine near the middle of the range, where these rates sit. The jump, its interval, and both slopes:

```python
jump = rd.params["free_delivery"]
ci = rd.conf_int().loc["free_delivery"]
slope_above = rd.params["centred"] + rd.params["free_delivery:centred"]
print(f"jump at the threshold: {100 * jump:+.1f} points  "
      f"(95% CI {100 * ci[0]:+.1f} to {100 * ci[1]:+.1f})")
print(f"slope below the cut-off: {100 * rd.params['centred']:+.2f} points per ₹1,000")
print(f"slope above the cut-off: {100 * slope_above:+.2f} points per ₹1,000")
print("true effect: +6.0 points")
```

```
jump at the threshold: +7.3 points  (95% CI +5.6 to +8.9)
slope below the cut-off: +0.79 points per ₹1,000
slope above the cut-off: +0.92 points per ₹1,000
true effect: +6.0 points
```

![Binned reorder rates against order value, with a fitted line either side of the ₹25,000 threshold and a step upward at the cut-off, dots below and above the cut-off drawn with different shapes](figures/fig31-4-discontinuity.svg)

*Figure 31.4 — The estimate is the size of the step, not the difference between the two sides.*

### Bandwidth: how close is close enough?

The width of the window either side of the cut-off is the **bandwidth**. Narrow windows are more credible and noisier; wide ones are precise and lean more on the straight lines. Report several:

```python
rows = []
for bandwidth in (0.5, 1, 2, 3, 5):
    window = orders[orders["centred"].abs() <= bandwidth]
    fit = smf.ols("repeat_within_90_days ~ free_delivery + centred + free_delivery:centred",
                  data=window).fit()
    low, high = fit.conf_int().loc["free_delivery"]
    rows.append({"bandwidth (₹000)": bandwidth, "orders": len(window),
                 "estimate (pts)": 100 * fit.params["free_delivery"],
                 "ci_low": 100 * low, "ci_high": 100 * high})
print(pd.DataFrame(rows).round(2).to_string(index=False))
print("true effect: +6.0 points")
```

```
 bandwidth (₹000)  orders  estimate (pts)  ci_low  ci_high
              0.5    5686            6.34    1.29    11.38
              1.0   11331            8.30    4.75    11.84
              2.0   22095            8.05    5.54    10.57
              3.0   31502            7.65    5.57     9.72
              5.0   46054            7.26    5.61     8.90
true effect: +6.0 points
```

Every window puts the jump between 6 and 9 points, and every interval contains the true 6. That stability across bandwidths is part of the evidence; an estimate that swings when the window changes is a warning, not a result. What happens if you change the bandwidth? The table is the answer: going from ₹500 either side to ₹5,000 uses eight times as many orders and narrows the interval from about 10 points wide (1.29 to 11.38) to about 3 (5.61 to 8.90).

### The check that matters: can people move themselves across the line?

RD works only if nobody can precisely control which side of the threshold they land on. If customers nudge a ₹24,400 order up to ₹25,000 to get free delivery, the two sides stop being comparable, because the ones who nudged are the keen ones. The test is to look for **bunching** just above the cut-off: count orders in ₹500 bands and see whether the bands just above are fuller than those just below.

```python
bins = pd.cut(orders["centred"], bins=np.arange(-5, 5.5, 0.5), right=False)
density = orders.groupby(bins, observed=True).size()
print(density.iloc[6:14].to_string())
```

```
centred
[-2.0, -1.5)    2620
[-1.5, -1.0)    2738
[-1.0, -0.5)    2837
[-0.5, 0.0)     2831
[0.0, 0.5)      2855
[0.5, 1.0)      2808
[1.0, 1.5)      2770
[1.5, 2.0)      2636
```

- **`np.arange(-5, 5.5, 0.5)`** makes the band edges −5, −4.5, … 5. It stops *before* 5.5, so 5 is the last edge.
- **`right=False`** (section 18.5) makes each band include its left edge, `[0.0, 0.5)`, so an order of exactly ₹25,000, which gets free delivery, is counted above the cut-off, as in the rule. Without it, it would land in the band just below.
- **`observed=True`** lists only bands that have orders in them. `.iloc[6:14]` shows the eight bands from −₹2,000 to +₹2,000.

Now the ₹1,000 either side, with ordinary filters:

```python
just_below = ((orders["centred"] >= -1) & (orders["centred"] < 0)).sum()
just_above = ((orders["centred"] >= 0) & (orders["centred"] < 1)).sum()
print(f"orders in the ₹1,000 below: {just_below:,}")
print(f"orders in the ₹1,000 above: {just_above:,}")
print(f"ratio: {just_above / just_below:.3f}  (bunching would push this well above 1)")
```

```
orders in the ₹1,000 below: 5,668
orders in the ₹1,000 above: 5,663
ratio: 0.999  (bunching would push this well above 1)
```

Adding up a True/False column counts the Trues. Smooth: the counts either side are nearly equal. In real data this check often fails: sales reps round orders up to hit thresholds, and expense claims cluster below approval limits. When it fails, RD is not available, and the bunching itself becomes the finding.

> **Watch out: RD only measures the effect at the cut-off.** This estimate says what free delivery does for orders near ₹25,000. It says nothing about ₹5,000 orders, where the delivery cost is a much larger share of the order, or ₹2,00,000 ones, where nobody cares. That narrowness is the price of the credibility: a **local** answer you can trust more than a global one you can't.

---

## 31.8 Instrumental variables: the idea

Sometimes nothing above is available, because the thing you care about is chosen by the people you're studying. *"Do site visits by a sales rep increase orders?"* Reps visit the customers most likely to buy, and no threshold or clean before-and-after exists.

An **instrumental variable** is something that shifts the treatment but affects the outcome *only* through it. Suppose reps visit customers in their own city far more often, because travel time decides the day's route. Distance from the rep's office then nudges the number of visits without, in itself, making a customer buy more plastic crates. The method uses only the variation in visits that distance explains, and discards the rest, which is the part contaminated by the rep's judgment.

A valid instrument needs three things:

| Requirement | What it means | For "distance to the rep's office" |
|---|---|---|
| **Relevance** | it really moves the treatment | nearby customers do get more visits: check it, don't assume it |
| **Exclusion** | it affects the outcome *only* through the treatment | distance must not affect orders any other way, which is doubtful: nearby customers may also get faster delivery |
| **Independence** | it isn't driven by something that also drives the outcome | offices were placed near big customers, so distance is already related to size |

The last two are assumptions, and cannot be tested. The estimation itself is routine (two-stage least squares: predict the treatment from the instrument, then use the prediction), and it is never the hard part. **Finding a defensible instrument is.** Classic examples earned their fame because they're rare: distance to the nearest college for the effect of education on earnings, quarter of birth for years of schooling, rainfall for economic shocks.

For an analyst, the useful skill is recognizing the shape of the argument: *"we are using only the part of the variation caused by something unrelated to the outcome"*. That lets you read a study, ask the exclusion question in a meeting, and sometimes spot an instrument hiding in your own systems: a policy that applied to some customers by an accident of timing, a system migration that happened alphabetically, an outage that hit one region's warehouse.

---

## 31.9 How much to trust each answer

| Method | The comparison it builds | Key assumption | What you can check | Strength of evidence |
|---|---|---|---|---|
| Before and after | the group's own past | nothing else changed | other series over the same period | weak |
| Treated vs untreated | another group, right now | the groups were alike already | pre-period levels and trends | weak |
| **Difference-in-differences** | the untreated group's change | parallel trends | pre-trends, event study, placebo periods | moderate to strong |
| **Synthetic control** | a weighted blend of untreated units | the blend tracks the treated unit for the right reasons | pre-change fit, placebo units | moderate to strong |
| **Matching / propensity** | similar-looking untreated units | no unmeasured confounding | balance, overlap, sensitivity analysis | moderate |
| **Regression discontinuity** | units just either side of a rule | no precise manipulation of the running variable | bunching, covariate smoothness, bandwidth stability | strong, but local |
| **Instrumental variables** | variation caused by the instrument | relevance, exclusion, independence | relevance only | strong if the instrument is valid, which is rare |
| **Randomized experiment** (Chapter 30) | a coin flip | the randomization worked | sample-ratio and balance checks | strongest |

**Covariate smoothness**, in the RD row, means that the other characteristics of the orders (segment, region) don't jump at the cut-off either; exercise 12 checks it.

![A decision list: can you randomize, is there a threshold rule, do you have before-and-after for both groups, many untreated units, only cross-sectional data, an instrument, or none of the above, each paired with the method it points to, its main caveat, and a strength label](figures/fig31-5-which-method.svg)

*Figure 31.5 — Work down the list; the first row you can answer yes to is usually the strongest evidence available.*

### Sensitivity: how wrong could you be?

The question to ask of any observational estimate is not *"is it right?"* but *"how strong would the thing I've missed have to be, to overturn this?"* Start with how much of the naive gap the measured variables explained:

```python
naive_pct = 100 * (np.exp(gap) - 1)
adjusted_pct = 100 * (np.exp(adjusted) - 1)
print(f"quarterly reviews, unadjusted: {naive_pct:+.1f}%")
print(f"after controlling for size, growth, tenure and segment: {adjusted_pct:+.1f}%")
print(f"share of the naive gap that was selection: {100 * (1 - adjusted_pct / naive_pct):.0f}%")
```

```
quarterly reviews, unadjusted: +75.0%
after controlling for size, growth, tenure and segment: +7.5%
share of the naive gap that was selection: 90%
```

Most of the apparent effect was selection. Now measure how strong the variables you *did* measure are, by leaving each out in turn and watching the estimate move. An unmeasured confounder as strong as one of them could move it about as far:

```python
formulas = {
    "all four": "log_2025 ~ in_qbr_program + log_2024 + growth_2024 + years_as_customer + C(segment)",
    "without prior size": "log_2025 ~ in_qbr_program + growth_2024 + years_as_customer + C(segment)",
    "without 2024 growth": "log_2025 ~ in_qbr_program + log_2024 + years_as_customer + C(segment)",
}
for label, formula in formulas.items():
    estimate = smf.ols(formula, data=qbr).fit().params["in_qbr_program"]
    print(f"{label:20s}: {100 * (np.exp(estimate) - 1):+5.1f}%")
```

```
all four            :  +7.5%
without prior size  : +75.1%
without 2024 growth :  +8.7%
```

Leaving out prior size moves the estimate by about 68 points; leaving out 2024 growth moves it by about one. So a missing variable as strong as growth would barely matter, but one as strong as prior size would swamp the +7.5% that's left. The honest sentence is: *"about +7%, and that estimate depends on the sales team's choices being driven by things we can see."* Formal versions of this reasoning exist (Rosenbaum bounds, E-values); the informal version, said out loud with these numbers, is already most of the value.

### Writing up a causal claim

Four sentences, in this order:

1. **The estimate, with its interval and its unit.** *"North's order volume fell about 7% (95% CI 4% to 10%) after the price rise."*
2. **The comparison that produced it.** *"Measured against the other three regions over the same months, with region and month effects removed."*
3. **The assumption it rests on, and the check you ran.** *"This assumes North would otherwise have grown like the others; their trends ran parallel for twelve of the fifteen months before the change, with a dip in the last quarter."*
4. **What would change your mind.** *"If something else hit North in October, such as a competitor or a lost distributor, this would overstate the price effect. I checked the sales log and found nothing, but it's the risk."*

> **Interview extra point.** Asked *"how would you measure something you can't A/B test?"*, name the method, then immediately name its assumption and the check: *"difference-in-differences, assuming parallel trends, which I'd test on the pre-period and show as a chart."* Chapter 69's method rewards exactly this: the claim, then the check. It separates people who have read about these methods from people who have used them.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Reading a log difference as a percentage | "+0.56 in logs, so +56%" when it is +75% | Always convert with exp(d) − 1 |
| Before-and-after with no comparison group | The season, the trend, or a campaign gets credited to your change | Find an untreated group and use DiD |
| Comparing treated with untreated as they are | Differences that existed beforehand read as effects | Match, or use each group's *change* |
| Skipping the parallel-trends check | A DiD that measures a divergence already under way | Plot the pre-period; show the chart in the write-up |
| Reading a DiD from few clusters as precise | Tidy p-values from four regions | Cluster, then say plainly that the number of groups is small |
| Matching on variables measured after the treatment | The control variable is itself an effect; the estimate collapses | Only use what was known before treatment began |
| Not checking balance after matching | Matching that didn't work, reported as if it did | Standardized mean differences, before and after |
| Matching outside the region of overlap | Participants with no comparable control get matched anyway | A caliper, and report how many went unmatched |
| Treating matching as equal to an experiment | Confident causal language on shaky ground | Say "assuming nothing unmeasured drove selection" |
| RD with a manipulable threshold | Bunching just above the cut-off | Check the density; if it bunches, don't use RD |
| RD generalized beyond the cut-off | "Free delivery raises reorders by 7 points" for all orders | Say "for orders near ₹25,000" |
| One bandwidth, chosen after seeing results | An estimate the reader can't audit | Report a table of bandwidths |
| Synthetic control with a poor pre-change fit | A "control" that never tracked the treated unit | Judge the fit first; abandon the method if it's bad |
| Contaminated comparison groups | Effects that leak into the control and shrink the estimate | Ask whether the treatment could have touched the comparison |
| An instrument that affects the outcome directly | A causal claim resting on an untestable assumption nobody stated | State exclusion out loud; most instruments fail it |
| Causal language without the assumption | "The price rise cost us 7%" with nothing attached | Estimate, comparison, assumption, and what would change your mind |
| Chasing significance instead of magnitude | A statistically significant 0.4% effect driving a big decision | Chapter 30's rule: effect, interval, and sample size |

---

## In the real world: the price rise nobody wanted to measure

Riverstone's North region raised list prices 6% on 1 October 2025, to protect margin after a polymer price shock. In April 2026 the board asks the obvious question, and gets three answers in one meeting.

North's regional manager says volume is up 1.7% since the rise, so customers clearly accepted it. The finance manager says North sells 23% less than the other regions, so the rise has done real damage. Both are reading the same table.

Meera's answer takes an afternoon. She builds the region-month panel, plots North against the other three, and shows that the lines ran parallel for most of the fifteen months and then stepped apart in October. Her estimate is a 7% fall in order volume, with an interval from 4% to 10%. Combined with the 6% price rise, revenue is roughly flat (exercise 2). And since North now ships 7% fewer orders, each costing the same to make, gross margin is up: at Riverstone's 2025 gross margin of 26.2% (section 11.6), North's gross profit rises about 14%.

Then the useful part of the meeting. Anita Rao, the Sales Head, asks what else changed in North in October. Meera has checked: no distributor was lost, no competitor opened a depot, the festive season affected all four regions alike. She also says what she can't rule out: with one treated region and four groups in total, the interval is wider than it looks, a single unusual month moves it, and North was already a little low in the quarter before the rise.

The decision is not "the price rise failed". It is to hold the new prices, and to run a proper experiment on the next change: a randomized price test across a sample of customers in two regions, designed with Chapter 30's arithmetic, so that next year's version of this meeting has a coin flip behind it instead of an argument.

**What she tells the board:** *"Volume fell about 7%, not rose 1.7%. The 1.7% was the festive season and our overall growth, which every region got. Revenue is flat and margin is up, so the rise worked, at the cost of about 7% of volume. I'd like the next price change to go out as a proper test, because this method costs us an afternoon and a wide interval, and a test would cost a fortnight and give a straight answer."*

---

## Project: measure the regional price change

**Goal:** a causal estimate you can defend in a meeting, with its assumption stated and checked.

### Tools you'll need

Outputs in this chapter were checked with Python 3.11.15, pandas 3.0.6, numpy 2.4.6, scipy 1.17.1, and statsmodels 0.15.0, in September 2026; any Python from 3.11 on, with these libraries or newer, gives the same numbers.

- **pandas and numpy** for shaping the data. Nothing else is needed for the estimates: DiD, matching, and RD are all ordinary regressions once the data is shaped correctly.
- **statsmodels** for the regressions, including `cov_type="cluster"` for clustered standard errors and `smf.logit` for propensity scores.
- **scipy** for `linregress` (the pre-trend drift) and `scipy.optimize.minimize` (the synthetic control weights).
- **matplotlib** (Chapter 18) for the parallel-trends chart.
- **Worth knowing about:** `linearmodels` (panel models and two-stage least squares), `DoWhy` and `EconML` (causal graphs, sensitivity analysis, and heterogeneous effects), and `CausalImpact` (a Bayesian time-series version of the synthetic-control idea). They automate the arithmetic, not the argument.
- **Companion files** in `ch31/`: `generate_ch31_data.py` (all three datasets, seed 31, with the true effects in its header).

**Option A: your own data.** Any change that hit one group and not another, at a known date: a price change, a new opening hour, a policy in one branch, a product that shipped to one country first. Work on a copy, and keep customer data out of anything you share.

**Option B: Riverstone.** Estimate the effect of North's price rise on order volume, then extend it.

**Steps:**

1. **Write the counterfactual in one sentence** before touching the data: *"North's order volume in October 2025 to June 2026 if prices had not risen."*
2. **Compute both naive answers** (before-and-after, and treated-versus-untreated) and say in a line each why they're wrong here.
3. **Estimate the effect with DiD**, first as a two-by-two table, then as a regression with region and month fixed effects, with clustered standard errors.
4. **Check parallel trends**: the chart, and the quarter-by-quarter view.
5. **Run a placebo**: pretend the change happened on 1 January 2025 and re-estimate, using only the months before the real change (6 months before the fake date, 9 after). The placebo must sit entirely before the real change and leave enough months on each side. You should find nothing. If you find something, your design is picking up noise.
6. **Build a synthetic control** and compare it with the DiD estimate. Report the pre-change fit.
7. **Convert to money**: lost orders = the volume effect × North's average monthly orders before the change × 9 months; the revenue effect from a DiD on log revenue (exercise 2); and the margin effect, using Riverstone's 2025 gross margin of 26.2% (section 11.6) as the cost share of revenue before the rise: new gross profit ÷ old = (1 + volume effect) × (1.06 − 0.738) ÷ 0.262.
8. **Write four sentences** in section 31.9's shape: estimate, comparison, assumption and check, what would change your mind.

**Deliverables:** the analysis, the parallel-trends chart, the placebo result, and the four-sentence summary.

**Stretch goals:**

- Estimate the effect on revenue rather than volume, and explain why the two differ.
- Run the DiD dropping one comparison region at a time. How much does the estimate move?
- Use the QBR data to estimate the program's effect with matching, and separately with a DiD on 2024 versus 2025 revenue. Do the two agree?
- Design the randomized price test Meera asked for, using Chapter 30: unit, metric, MDE, sample size, duration.

---

## Recap

- Work in **logs**: a **log difference** is a growth rate, and exp(d) − 1 turns it back into an exact percentage.
- A causal claim compares the world that happened with a **counterfactual** that didn't. Every method here is a way of building a stand-in for it.
- **Before-and-after** is ruined by **confounding**; **treated-versus-untreated** is ruined by **selection**. In Riverstone's data they gave +1.7% and −23% for an effect that was −8%.
- **Difference-in-differences** subtracts the untreated group's change. As a regression, it is the **interaction** of two dummies; add **region and month fixed effects**, and **cluster** standard errors, remembering that few groups means wide, fragile intervals.
- DiD rests on **parallel trends**: untestable for the future, checkable for the past. Show the chart and a period-by-period view, and report a dip when you see one.
- **Synthetic control** blends untreated units to track the treated one before the change, with weights found by minimizing the pre-change loss. Judge it by **pre-change fit**; infer with **placebo** units.
- **Matching** and **propensity scores** build comparison units one at a time. Use only pre-treatment variables, apply a **caliper**, report **balance** and how many units went unmatched, and state the **no unmeasured confounding** assumption.
- **Regression discontinuity** uses a threshold rule as a natural experiment. Fit a line either side of the **running variable**'s cut-off, measure the **jump**, check for **bunching**, report several **bandwidths**, and remember the answer is **local** to the cut-off.
- **Instrumental variables** need **relevance**, **exclusion**, and **independence**; only the first is testable, which is why good instruments are rare.
- Evidence ranks roughly: experiment, then RD, then DiD and synthetic control, then matching, then naive comparisons. **Sensitivity analysis** asks how strong a missing confounder would have to be to overturn the result.
- Write causal claims in four sentences: estimate with interval, comparison used, assumption and check, and what would change your mind.

---

## Key terms

logarithm · natural log · log difference · causal claim · counterfactual · confounding · selection · treated and untreated groups · before-and-after · difference-in-differences · two-by-two table · dummy variable · interaction term · fixed effects · absorbed · clustered standard errors · parallel trends · event study · placebo test · synthetic control · donor pool · loss · root mean squared error · pre-change fit · interference between units · matching · propensity score · logistic function · overlap (common support) · caliper · matching without replacement · balance · standardized mean difference · pooled standard deviation · regression adjustment · no unmeasured confounding · regression discontinuity · running variable · cut-off · linear probability model · bandwidth · local effect · bunching · manipulation check · covariate smoothness · instrumental variable · relevance · exclusion restriction · independence · two-stage least squares · sensitivity analysis

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can convert a log difference to a percentage change, and I know why the shortcut fails for large changes.
- [ ] I state the counterfactual in words before choosing a method.
- [ ] I can explain why before-and-after and treated-versus-untreated usually mislead, with an example.
- [ ] I can compute DiD as a table and as a regression, map each coefficient to a cell, and say what the fixed effects absorb.
- [ ] I check parallel trends and show the chart, and I know what to do when they aren't parallel.
- [ ] I can build a synthetic control and judge it by its pre-change fit.
- [ ] I can fit a propensity model, work one score by hand, match with a caliper, and report balance before and after.
- [ ] I know that matching assumes no unmeasured confounding, and I say so.
- [ ] I can spot a threshold rule in a business process and use it for regression discontinuity, including the bunching check.
- [ ] I understand that an RD estimate is local to the cut-off.
- [ ] I can state the three requirements for an instrument and explain why exclusion is usually the weak one.
- [ ] Every causal claim I write carries its assumption and what would change my mind.

---

## Exercises

Work in `companion/ch31`, with the data built by `generate_ch31_data.py`, in the same notebook as the chapter's code. Predict each answer before running it.

### Warm-up

1. Compute average monthly orders for each region, before and after October 2025. Which regions grew, and by how much?
2. Run the DiD on **revenue** instead of order volume. Why is the answer so different from the volume effect, and which one answers "did the price rise work"?
3. For the QBR program, compare the average 2024 revenue of participants and non-participants. What does that tell you before you estimate anything?
4. How many orders in the threshold dataset are within ₹500 of the cut-off, and what share of them got free delivery?

### Core

5. Re-estimate the price effect using only West and South as comparison regions. Then only East. How much does the estimate move, and what does that tell you?
6. Run a **placebo test**: pretend the price rise happened on 1 January 2025 and estimate a DiD using only the months before the real change (6 months before the fake date, 9 after). What should you find, and what do you find?
7. Add clustered standard errors to the fixed-effects DiD (`cov_type="cluster"` grouped by region). How does the interval change, and why shouldn't you trust it too far?
8. Estimate the QBR effect with a DiD on the same customers (2024 versus 2025 revenue, participants versus not) instead of matching. Compare with section 31.6's estimates.
9. Redo the matching with a tighter caliper of 0.01 and with no caliper at all. Report pairs matched, balance, and the estimate for each.
10. Fit the RD with a quadratic on each side of the threshold at a bandwidth of ₹5,000. Does the estimate change? Which specification would you report?

### Stretch

11. Run the synthetic-control **placebo**: build a synthetic West, South, and East in turn, and compare their post-October gaps with North's. Is North's gap unusual?
12. The RD dataset contains segment and region. Check that these are **smooth** across the threshold, and explain why that check matters.
13. Estimate the price effect with a regression that also lets North follow its own straight-line trend. Does the effect survive?
14. Write the "what would change your mind" sentence for each of the three estimates in this chapter, and rank the three by how much you'd trust them.

### Think about it (no code needed)

15. Riverstone's warehouse in Bhiwandi was expanded in March 2026, serving mostly West-region customers. How does that affect the price-rise DiD, and what would you do about it?
16. A colleague proposes matching customers on their 2025 revenue to estimate the 2025 effect of the QBR program. What's wrong with that?
17. Give one threshold rule in a business you know that could serve as a regression discontinuity, and one reason it might fail the bunching check.
18. When would you prefer a weaker method with data you have over a stronger one that would take six months to arrange?

---

## Answers

**1.**

```python
change = (panel.pivot_table(index="region", columns="is_after", values="orders", aggfunc="mean")
               .rename(columns={0: "before", 1: "after"}))
change["change_%"] = 100 * (change["after"] / change["before"] - 1)
print(change.round(1).to_string())
```

```
is_after  before   after  change_%
region
East      1500.9  1625.4       8.3
North     2031.7  2067.1       1.7
South     2501.3  2697.9       7.9
West      3334.9  3725.3      11.7
```

Every region grew, North least of all. The gap between North's growth and the others' is the DiD estimate, seen in levels rather than logs.

**2.**

```python
panel["log_revenue"] = np.log(panel["revenue"])
rev = smf.ols("log_revenue ~ treated:is_after + C(region) + C(month)", data=panel).fit()
vol = smf.ols("log_orders ~ treated:is_after + C(region) + C(month)", data=panel).fit()
print(f"effect on volume:  {100 * (np.exp(vol.params['treated:is_after']) - 1):+.1f}%")
print(f"effect on revenue: {100 * (np.exp(rev.params['treated:is_after']) - 1):+.1f}%")
print(f"price rise applied: +6.0%")
```

```
effect on volume:  -7.0%
effect on revenue: +0.7%
price rise applied: +6.0%
```

Volume fell about 7%, and revenue is close to flat. If only the price had changed, revenue would have moved by 0.93 × 1.06 − 1 = −1.4%. The estimate is +0.7%, so the average order value rose about 8%, more than the 6% price rise: the orders North lost were smaller ones. That mix shift is itself a finding; check it with a DiD on the log of `avg_order_value`. Both effects are true and they answer different questions: the volume effect measures how customers responded, the revenue effect what it did to the top line. For "did the price rise work", the revenue (and ideally margin) effect is the one the board wants, with the volume effect as the explanation.

**3.**

```python
by_group = qbr.groupby("in_qbr_program")[["revenue_2024", "growth_2024", "years_as_customer"]].mean()
print(by_group.round(3).to_string())
ratio = by_group.loc[1, "revenue_2024"] / by_group.loc[0, "revenue_2024"]
print(f"ratio of average 2024 revenue: {ratio:.2f}x")
```

```
                revenue_2024  growth_2024  years_as_customer
in_qbr_program
0                 755520.916        0.052              5.023
1                1225516.825        0.062              5.632
ratio of average 2024 revenue: 1.62x
```

Participants were already 1.6 times the size of non-participants *before* the program began, and growing faster. Any raw comparison of 2025 revenue will mostly measure that. This table is the argument for matching, and it belongs at the top of the write-up.

**4.**

```python
near = orders[orders["centred"].abs() <= 0.5]
print(f"orders within ₹500 of the cut-off: {len(near):,}")
print(f"share with free delivery: {near['free_delivery'].mean():.3f}")
print(f"reorder rate below: {near.loc[near['free_delivery'] == 0, 'repeat_within_90_days'].mean():.3f}")
print(f"reorder rate above: {near.loc[near['free_delivery'] == 1, 'repeat_within_90_days'].mean():.3f}")
```

```
orders within ₹500 of the cut-off: 5,686
share with free delivery: 0.502
reorder rate below: 0.328
reorder rate above: 0.412
```

Almost exactly half, which is what a smooth running variable around a threshold should give. It's also the cleanest comparison in the chapter: two groups of orders differing by a few hundred rupees and a delivery charge.

**5.**

```python
for comparison in (["West", "South"], ["East"], ["West"], ["South"]):
    subset = panel[panel["region"].isin(["North"] + comparison)]
    fit = smf.ols("log_orders ~ treated:is_after + C(region) + C(month)", data=subset).fit()
    effect = fit.params["treated:is_after"]
    low, high = fit.conf_int().loc["treated:is_after"]
    print(f"comparison {str(comparison):22s}: {100 * (np.exp(effect) - 1):+5.1f}%  "
          f"(CI {100 * (np.exp(low) - 1):+5.1f}% to {100 * (np.exp(high) - 1):+5.1f}%)")
```

```
comparison ['West', 'South']     :  -7.5%  (CI -10.9% to  -3.8%)
comparison ['East']              :  -6.2%  (CI  -9.8% to  -2.4%)
comparison ['West']              :  -9.1%  (CI -13.1% to  -4.9%)
comparison ['South']             :  -5.8%  (CI -10.0% to  -1.4%)
```

The estimate moves by a couple of points depending on the comparison group, and every version is clearly negative. That spread is honest information: report the main specification, and say how much it moves when the comparison changes. An estimate that flips sign when you swap comparison regions is not a finding.

**6.**

```python
placebo_data = panel[panel["month"] < "2025-10-01"].copy()
placebo_data["fake_after"] = (placebo_data["month"] >= "2025-01-01").astype(int)
placebo = smf.ols("log_orders ~ treated:fake_after + C(region) + C(month)", data=placebo_data).fit()
effect = placebo.params["treated:fake_after"]
low, high = placebo.conf_int().loc["treated:fake_after"]
print(f"placebo effect: {100 * (np.exp(effect) - 1):+.1f}%  "
      f"(95% CI {100 * (np.exp(low) - 1):+.1f}% to {100 * (np.exp(high) - 1):+.1f}%)")
print("a clean design finds nothing here")
```

```
placebo effect: +0.5%  (95% CI -3.9% to +5.1%)
a clean design finds nothing here
```

The placebo effect is small and its interval comfortably includes zero, so the design isn't manufacturing effects out of noise. Run this before you trust any DiD: it costs three lines and catches designs that would "find" something whatever the data.

**7.**

```python
clustered = smf.ols("log_orders ~ treated:is_after + C(region) + C(month)", data=panel).fit(
    cov_type="cluster", cov_kwds={"groups": panel["region"]})
plain = smf.ols("log_orders ~ treated:is_after + C(region) + C(month)", data=panel).fit()
for name, fit in (("plain", plain), ("clustered", clustered)):
    low, high = fit.conf_int().loc["treated:is_after"]
    print(f"{name:10s}: effect {fit.params['treated:is_after']:+.4f}, "
          f"CI {low:+.4f} to {high:+.4f}, se {fit.bse['treated:is_after']:.4f}")
```

```
plain     : effect -0.0729, CI -0.1064 to -0.0394, se 0.0168
clustered : effect -0.0729, CI -0.0978 to -0.0480, se 0.0127
```

`fit.bse` holds the standard errors. Notice that the clustered interval is *narrower*, the opposite of what clustering is supposed to do. With four clusters the formula is unreliable in both directions, and a narrower "corrected" interval is itself the warning sign. Quote the plain interval, and add the caveat: with four regions, treat any interval as indicative. The fixes are resampling methods built for few groups, such as the placebo test of exercise 6 run for every region in turn, and a write-up should say which one you used.

**8.**

```python
long = pd.concat([
    qbr.assign(year=2024, log_revenue=qbr["log_2024"]),
    qbr.assign(year=2025, log_revenue=qbr["log_2025"])])
long["after"] = (long["year"] == 2025).astype(int)
did_qbr = smf.ols("log_revenue ~ in_qbr_program:after + C(customer_id) + C(year)", data=long).fit()
effect = did_qbr.params["in_qbr_program:after"]
print(f"DiD estimate: {100 * (np.exp(effect) - 1):+.1f}%")
print(f"matching:     {100 * (np.exp(matched_effect) - 1):+.1f}%")
print("true effect:  +7.0%")
```

```
DiD estimate: +9.0%
matching:     +7.1%
true effect:  +7.0%
```

`pd.concat` (section 18.7) stacks two copies of the accounts, one labelled 2024 and one 2025, so each account has a before row and an after row. The DiD uses each customer as their own control, which removes every fixed difference between accounts, measured or not. It lands two points high. Participants were chosen partly because they were already growing faster (2024 growth 6.2% against 5.2%), so they would have out-grown the others anyway: a parallel-trends failure. Prefer DiD when selection was on *levels* (size); when it was on *trends* (growth), combine the two: match on 2024 growth, then take the difference.

**9.**

```python
def match(caliper):
    available = qbr[qbr["in_qbr_program"] == 0].set_index("customer_id")["propensity"].to_dict()
    ids = []
    ordered = qbr[qbr["in_qbr_program"] == 1].sort_values("propensity", ascending=False)
    for row in ordered.itertuples():
        if not available:
            break
        best = min(available, key=lambda cid: abs(available[cid] - row.propensity))
        if caliper is None or abs(available[best] - row.propensity) <= caliper:
            ids += [row.customer_id, best]
            del available[best]
    subset = qbr[qbr["customer_id"].isin(ids)]
    means = subset.groupby("in_qbr_program")["log_2025"].mean()
    return len(ids) // 2, smd(subset, "log_2024"), 100 * (np.exp(means[1] - means[0]) - 1)

for caliper in (0.01, 0.05, None):
    pairs_n, balance, effect = match(caliper)
    print(f"caliper {str(caliper):>5}: {pairs_n:2d} pairs, "
          f"balance on log_2024 {balance:+.3f}, effect {effect:+.1f}%")
print("true effect: +7.0%")
```

```
caliper  0.01: 56 pairs, balance on log_2024 -0.082, effect +0.4%
caliper  0.05: 64 pairs, balance on log_2024 +0.002, effect +7.1%
caliper  None: 68 pairs, balance on log_2024 +0.071, effect +12.2%
true effect: +7.0%
```

Look at how much the answer moves: +0.4%, +7.1%, +12.2%, for the same data and the same method. With no caliper, every participant gets matched, including the largest accounts whose nearest "comparison" isn't close, and balance drifts. With a caliper of 0.01, only 56 pairs survive and the ones that do are a peculiar subset. The middle setting balances well and lands near the truth, but you couldn't have known that in advance without the answer key. This is the honest reason matching ranks below the other methods in section 31.9: several defensible choices give materially different answers, so report the choice, the balance, and how much the estimate moves when you change it.

**10.**

```python
window = orders[orders["centred"].abs() <= 5]
linear = smf.ols("repeat_within_90_days ~ free_delivery + centred + free_delivery:centred",
                 data=window).fit()
quad = smf.ols("repeat_within_90_days ~ free_delivery + centred + I(centred ** 2) + "
               "free_delivery:centred + free_delivery:I(centred ** 2)", data=window).fit()
for name, fit in (("linear", linear), ("quadratic", quad)):
    low, high = fit.conf_int().loc["free_delivery"]
    print(f"{name:10s}: {100 * fit.params['free_delivery']:+.2f} points "
          f"(CI {100 * low:+.2f} to {100 * high:+.2f})")
print("true effect: +6.0 points")
```

```
linear    : +7.26 points (CI +5.61 to +8.90)
quadratic : +8.31 points (CI +5.87 to +10.74)
true effect: +6.0 points
```

In a formula, `I(...)` means "compute this inside the formula": `I(centred ** 2)` adds a column of centred squared, which lets each side curve. (Without `I()`, `**` has a different meaning in formulas.) The quadratic sits about a point higher with a wider interval, and the two overlap comfortably, so the finding doesn't depend on the shape you fit. Report the linear fit at a narrow bandwidth as the main result and the others as robustness: high-order polynomials are known to produce strange jumps at the boundary, and "we tried several and they agree" is a stronger sentence than any single specification.

**11.**

```python
def synthetic_gap(target):
    donors = [r for r in ["West", "South", "East", "North"] if r != target]
    pre = wide_panel[wide_panel.index < "2025-10-01"]
    fit = minimize(lambda w: float(np.mean((pre[target].to_numpy() - pre[donors].to_numpy() @ w) ** 2)),
                   np.repeat(1 / 3, 3), bounds=[(0, 1)] * 3,
                   constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}], method="SLSQP")
    blend = wide_panel[donors].to_numpy() @ fit.x
    after = wide_panel.index >= "2025-10-01"
    pre_fit = np.sqrt(np.mean((pre[target].to_numpy() - blend[:len(pre)]) ** 2))
    return pre_fit, (wide_panel[target].to_numpy() - blend)[after].mean()

for region in ["North", "West", "South", "East"]:
    pre_fit, gap_r = synthetic_gap(region)
    flag = "  <-- the treated region" if region == "North" else ""
    print(f"{region:6s}: pre-change fit {pre_fit:.4f}, "
          f"post-change gap {100 * (np.exp(gap_r) - 1):+5.1f}%{flag}")
```

```
North : pre-change fit 0.0429, post-change gap  -6.6%  <-- the treated region
West  : pre-change fit 0.2918, post-change gap +38.2%
South : pre-change fit 0.0415, post-change gap  -0.0%
East  : pre-change fit 0.3074, post-change gap -21.4%
```

The function is section 31.5 in one piece, with the `@` form of the blend and `np.repeat(1 / 3, 3)` for the three starting weights. `blend[:len(pre)]` takes the pre-change months, and `after` marks the months from October 2025.

Read the fit column first. West and East can't be reproduced by a blend of the others at all (pre-change errors of 0.29 and 0.31 against North's 0.043): West is the biggest region and East the smallest, so no blend of the rest can reach them, and their gaps are noise that tell you nothing. South fits as well as North does, and its post-change gap is zero. So only South is a usable placebo. With North and South the only well-fitted units, the most extreme result North could have is "first of two", so the smallest p-value this test can give is 1/2 = 0.5. Four regions cannot deliver significance by this route, which is another way of saying four regions is a very small dataset.

**12.**

```python
window = orders[orders["centred"].abs() <= 2].copy()
for column in ["segment", "region"]:
    share = pd.crosstab(window["free_delivery"], window[column], normalize="index")
    print(share.round(3).to_string())
    print()
```

```
segment        Hospitality  Retail  Wholesale
free_delivery
0                    0.338   0.326      0.336
1                    0.332   0.336      0.332

region          East  North  South   West
free_delivery
0              0.254  0.248  0.248  0.250
1              0.254  0.256  0.245  0.245
```

The mix of segments and regions is nearly identical either side of the cut-off. If it weren't, the two sides would differ in ways beyond the rule, and the jump could be that difference rather than the free delivery. Covariate smoothness is to RD what balance is to matching, and what the sample-ratio check is to an A/B test: the test of whether the comparison is fair.

**13.**

```python
panel["t"] = ((panel["month"].dt.year - 2024) * 12 + panel["month"].dt.month)
trend = smf.ols("log_orders ~ treated:is_after + C(region) + C(month) + treated:t", data=panel).fit()
effect = trend.params["treated:is_after"]
low, high = trend.conf_int().loc["treated:is_after"]
print(f"with a North-specific trend: {100 * (np.exp(effect) - 1):+.1f}% "
      f"(CI {100 * (np.exp(low) - 1):+.1f}% to {100 * (np.exp(high) - 1):+.1f}%)")
print("without it: -7.0%")
```

```
with a North-specific trend: -4.8% (CI -10.5% to +1.3%)
without it: -7.0%
```

`t` numbers the months; `treated:t` is 0 for the other regions and the month number for North, so its coefficient is a straight-line trend in North *relative to* the others, which the month effects already handle. The effect shrinks to about −5% and its interval now crosses zero. Don't read that as "the result failed": with 24 months and a change two-thirds of the way through, a trend fitted on the whole period soaks up much of the post-change drop, which is exactly the effect being measured, and section 31.4's dip in the last pre-change quarter pulls the trend down. It is still a useful warning. The honest summary is: −7% in the main specification, −5% and not distinguishable from zero when North is allowed its own trend, and the two are not far apart in business terms. Report both, and let the reader see the range.

**14.** One sentence each, ranked by how much they'd survive an argument:

- **Regression discontinuity (free delivery, +7 points):** *"This would change if customers could steer their order values across ₹25,000, which the density check says they don't."* Strongest, because the comparison group is almost mechanical, and weakest in scope: it speaks only for orders near the threshold.
- **Difference-in-differences (price rise, −7%):** *"This would change if something else hit North around October 2025, or if North was already drifting away from the other regions."* Strong on the evidence available, with the caveats that four regions is few and the last pre-change quarter dipped.
- **Matching (quarterly reviews, +7%):** *"This would change if the sales team chose accounts using something we can't see, such as their sense of which accounts had potential."* Weakest, because that judgment is exactly the sort of thing that isn't in a table.

**15.** The expansion helps West-region customers from March 2026, which is *after* the price rise, so the comparison group's behavior changes partway through the post period. That inflates the other regions' growth and makes North look worse than it is. Three responses, in order of preference: end the analysis window in February 2026; drop West and use South and East as the comparison (exercise 5 shows the estimate holds); or add a control for the expansion period and report both. Whatever you choose, say it, because a reader who knows about the warehouse will ask.

**16.** Revenue in 2025 is measured *after* the program ran, so it's partly an effect of the thing being measured. Matching on it would pair participants with the non-participants who happened to reach the same revenue, throwing away the very difference the program caused, and biasing the estimate toward zero. The rule is absolute: match only on what was known before treatment began, which here means 2024 revenue, 2024 growth, tenure, and segment.

**17.** Any rule with a sharp edge: free shipping above a value, a discount tier at a volume, a credit check above an order size, a bonus for hitting a monthly target, an SLA that applies above a ticket priority. Bunching is likely wherever the person affected can see the threshold and control the number: sales reps write orders at exactly the discount tier, expense claims come in just under the approval limit, and salespeople hit their target by a rupee in the last week of the month. If the histogram spikes at the edge, the rule is being gamed, and that spike is itself worth reporting to the business.

**18.** Almost always, when the decision is soon and reversible. A DiD that takes an afternoon and gives ±3 points is worth more than a perfect experiment that reports after the decision is made. The reverse holds when the decision is expensive, hard to undo, or repeated: a pricing policy for every region, a system everyone will use for five years. The practical answer is usually both: measure what you can now with the weaker method, and design the experiment for the next change, which is exactly what Riverstone did after the price rise.

---

## Where this leads

- **Chapter 30, Inference & Experiments,** is the method to reach for whenever randomizing is possible; this chapter is what you do when it isn't.
- **Chapter 22, Statistics Without Fooling Yourself,** is the intuition behind the warnings here, and its section 22.10 is the regression every method in this chapter was built on.
- **Chapter 35, The Math Under the Models,** explains the `@` of section 31.5: vectors, matrices, and the dot product.
- **Chapter 37, Supervised Learning Algorithms,** fits the same regressions, linear and logistic, to *predict* rather than to explain; **Chapter 40, Time Series & Forecasting,** fits lines through time. The machinery is shared: the difference is entirely in what you claim from it.
- **Chapter 56, MLOps,** keeps models honest in production, where telling "the model is good" from "the model was given the easy cases" needs this chapter's causal thinking.
- **Chapter 73, Statistics, Probability & Experimentation Bank,** has causal-inference questions in section 73.6: confounders, selection bias, and natural experiments.
