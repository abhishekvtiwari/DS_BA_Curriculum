# Chapter 21. Descriptive Statistics & Probability

*Part 2 — The Analyst*

> **Chapter at a glance**
>
> **You will learn to:** work out the mean, median, mode, variance, standard deviation, and quartiles by hand, in a spreadsheet, and in pandas · choose between mean, median, and mode, and say why they differ · measure spread with range, variance, standard deviation, and the interquartile range, and know which to quote · read percentiles and use them in service levels · describe the shape of data: skew, tails, and outliers · recognize the four distributions an analyst meets most (normal, binomial, Poisson, uniform) and what each implies · apply the rules of probability, including conditional probability and independence · use Bayes' rule on a real business question and explain the answer to a manager · understand sampling, sampling error, and the central limit theorem by simulating it · put all of it together to profile a dataset statistically.
>
> **Before you start:** Chapter 4 (averages, percentages, and probability by counting), Chapter 15 (histograms, box plots, and quartiles by hand), and Chapters 17 and 18 (Python and pandas). No mathematics beyond Chapter 4 is assumed. Section 21.0 shows how to read the few symbols this chapter uses, and every formula is written once in symbols and then explained in words.
>
> **Time needed:** 18–21 hours, spread over two to three weeks, in two halves: describing data (sections 21.0–21.4, about 8–9 hours) and probability and sampling (sections 21.5–21.9, about 10–12 hours). Each half ends with a short checkpoint.
>
> **Tools:** Python 3.13 or 3.14 as installed in Chapter 17, with `pandas`, `numpy`, and `matplotlib` (Chapter 18) and `scipy`, which section 21.5 installs. The outputs shown were checked on Python 3.11 with pandas 3.0.6, numpy 2.4.6, and scipy 1.17.1. The spreadsheet steps use the functions from Chapters 10 and 11 plus a few new ones (`STDEV.S`, `NORM.DIST`, `BINOM.DIST`, `POISSON.DIST`), which work the same in Excel and Google Sheets.
>
> **Practice data:** the full Riverstone dataset, plus `companion/ch21/delivery_times_2025.csv`: one row per delivered 2025 order, with its value, the branch that shipped it, the promised days, and the actual delivery time. Section 21.1 lists its eight columns. (Delivery times are invented for this chapter, because the ERP data has no delivery dates. They are simulated from a documented model, described in the companion folder's README; you never need to rebuild the file.)

---

## Why this matters

Every number you report is a summary, and every summary throws information away. Statistics is the discipline of throwing away the right information, and of knowing what you've lost.

Two examples from earlier chapters. Chapter 15's box plots showed that Riverstone's Wholesale orders have a median of ₹25,762 while Retail sits at ₹19,425 — but the *averages* would have told a different story, because a handful of enormous orders drag a mean upward. Chapter 20's alert asked whether today's revenue was "within 60% of the recent median", which is a statistical judgment dressed as a business rule: how much variation is normal?

That question — **how much variation is normal?** — is the one this chapter answers. Without it, you can't tell a real change from noise, you can't set a threshold, you can't promise a delivery time, and you can't say whether a test worked. Chapter 22 is about the ways people fool themselves with these tools; this chapter is the tools themselves.

It's also the part of the analyst's job that transfers furthest. Every forecasting, experimentation, and machine-learning chapter in Parts 3, 4, and 6 assumes the ideas here: distributions, sampling, and the difference between what you measured and what's true.

---

## In plain English

A cricket commentator never says "the batsman's runs were 12, 0, 45, 3, 88, 1, 67, 0". They say "he averages 32, but he's either out cheaply or he scores big". That sentence has three statistics in it, and it's a better description than the list.

- **The average (32)** is the centre: one number standing in for many.
- **"Either cheaply or big"** is the spread and the shape: the scores aren't clustered around 32; they're at both ends.
- **"Out cheaply"** implies a probability: it happens often enough to expect it.

Descriptive statistics is that sentence, done carefully. Probability is the next step: *given* what we've seen, how surprised should we be by tomorrow? If a batsman averages 32 and scores 0, nobody calls a meeting. If a branch's delivery time averages 3.2 days and one order takes 19, is that a bad week or a broken process?

The whole chapter is about answering that without either panicking or shrugging.

---

## 21.0 Seven deliveries, by hand

Chapter 4 worked out means and medians of real orders, and Chapter 15 found the quartiles of nine orders by hand. This section does the same for the new measures in this chapter, on numbers small enough to check with a pencil. Then it repeats them in a spreadsheet and in pandas. Everything after this section is the same arithmetic on 45,040 rows.

One week, seven deliveries. The days each one took, sorted from fastest to slowest:

**2, 3, 3, 4, 5, 6, 19**

### Reading the symbols

Statistics writes its formulas with a few symbols. These are all you need for this chapter; the rest are introduced where they're used.

| Symbol | Say it | Means | In the seven deliveries |
|---|---|---|---|
| *n* | "n" | how many values there are | *n* = 7 |
| xᵢ | "x sub i" | the value in position *i*; *i* counts 1, 2, … up to *n* | x₁ = 2, x₂ = 3, …, x₇ = 19 |
| Σ | "sigma" (a capital Greek S) | "add up": add the thing after it for every *i* from 1 to *n* | Σxᵢ = 2 + 3 + 3 + 4 + 5 + 6 + 19 = 42 |
| x̄ | "x-bar" | the mean of a **sample** (the values you have) | 6 days |
| μ | "mu" | the mean of a whole **population** (every value there is) | — |
| *s* | "s" | the standard deviation of a sample | 5.89 days |
| σ | "sigma" (a small Greek s) | the standard deviation of a whole population | — |
| √ | "the square root of" | the number that, times itself, gives what's inside | √9 = 3 |

A **sample** is the part you measured; the **population** is everything you'd like to know about. Section 21.8 comes back to the difference.

### The centre: mean, median, and mode

**Mean:** x̄ = Σxᵢ ÷ *n*. In words: add every value, then divide by how many there are. Here 42 ÷ 7 = **6.0 days**.

**Median:** sort the values and take the middle one. With *n* = 7 the middle is the 4th value: **4 days**. (With an even count, take the mean of the two middle values, as in Chapter 4.)

**Mode:** the most common value: **3 days**, which appears twice.

**Range:** the largest minus the smallest: 19 − 2 = **17 days**.

Now take the slow delivery away. The other six (2, 3, 3, 4, 5, 6) have a mean of 23 ÷ 6 = 3.8 days and a median of 3.5. One slow delivery moved the mean by more than two days and the median by half a day. That difference is the reason this chapter keeps putting the two side by side.

### The spread: variance and standard deviation

The mean says where the values sit. The next question is how far they typically are from it. Each value's distance from the mean, x − x̄, is called its **deviation**:

| Delivery days, x | Deviation, x − x̄ | Squared deviation, (x − x̄)² |
|---:|---:|---:|
| 2 | −4 | 16 |
| 3 | −3 | 9 |
| 3 | −3 | 9 |
| 4 | −2 | 4 |
| 5 | −1 | 1 |
| 6 | 0 | 0 |
| 19 | 13 | 169 |
| **Total** | **0** | **208** |

The deviations always add up to zero: the values below the mean cancel the ones above it, by the definition of the mean. So you can't average them directly. Squaring each one makes every deviation positive, and then the total means something.

**Sample variance:** *s*² = Σ(xᵢ − x̄)² ÷ (*n* − 1). Reading it from the inside out: take each value's deviation (xᵢ − x̄), square it, add all the squares (Σ), and divide by one less than the count. Here 208 ÷ 6 = **34.67**. Its unit is "days squared", which is why nobody quotes it in a report.

**Why *n* − 1 and not *n*?** The deviations are measured from x̄, and x̄ was calculated from these same seven values, so the values sit a little closer to x̄ than to the true mean of all deliveries. Dividing by one less than *n* makes up for that slight underestimate. When you have the whole population and its true mean μ, divide by *n*: σ² = Σ(xᵢ − μ)² ÷ *n*.

**Standard deviation:** *s* = √*s*². In words: the square root of the variance, which puts the answer back into days. √34.67 = **5.89 days**. The population version divides by 7 instead: √(208 ÷ 7) = √29.71 = **5.45 days**. We'll write **sd** for "standard deviation" in code and tables.

Look at where the 208 came from: the slow delivery alone contributes 169 of it. Squaring makes big deviations count far more than small ones, so the standard deviation is very sensitive to a single extreme value.

### Quartiles and the interquartile range

Use Chapter 15's method. The median is the 4th value, 4. The lower half is positions 1 to 4, up to and including the median: 2, 3, 3, 4. Its middle falls between 3 and 3, so **Q1 = 3**. The upper half is positions 4 to 7: 4, 5, 6, 19. Its middle falls between 5 and 6, so **Q3 = 5.5**.

**Interquartile range:** IQR = Q3 − Q1 = 5.5 − 3 = **2.5 days**: the width of the middle half. The 19 doesn't touch it. The upper fence from Chapter 15 is Q3 + 1.5 × IQR = 5.5 + 3.75 = 9.25 days, so the 19-day delivery is an outlier on a box plot.

A **percentile** generalizes the idea: the 25th percentile is Q1, the 50th is the median, the 75th is Q3, and the 90th is the value 90% of the way through the sorted list. Spreadsheets and pandas find it with one rule: the position is 1 + *p* × (*n* − 1), where *p* is the share (0.25 for Q1), counting from the smallest value. When the position falls between two values, take the point that far between them. For Q1: 1 + 0.25 × 6 = 2.5, halfway between the 2nd value (3) and the 3rd (3), so 3. For Q3: 1 + 0.75 × 6 = 5.5, halfway between the 5th (5) and the 6th (6), so 5.5. With seven values, as with Chapter 15's nine, the two methods land on the same numbers.

### The same in a spreadsheet

Type `days` in cell A1 and the seven values in `A2:A8`. Then, in any empty cells:

```excel
=AVERAGE(A2:A8)          → 6
=MEDIAN(A2:A8)           → 4
=MODE.SNGL(A2:A8)        → 3
=MAX(A2:A8)-MIN(A2:A8)   → 17
=VAR.S(A2:A8)            → 34.6666667
=STDEV.S(A2:A8)          → 5.88784058
=STDEV.P(A2:A8)          → 5.45108115
=QUARTILE.INC(A2:A8,1)   → 3
=QUARTILE.INC(A2:A8,3)   → 5.5
```

What each one does:

- `AVERAGE`, `MEDIAN`, `MAX`, and `MIN` are the functions from Chapter 10. `MAX(...)-MIN(...)` is the range.
- `MODE.SNGL` returns the most common value. "SNGL" means single: if two values tie, it returns the one that appears first.
- `VAR.S` and `STDEV.S` are the **sample** variance and standard deviation: they divide by *n* − 1, like the hand calculation. `STDEV.P` is the **population** version, which divides by *n*.
- `QUARTILE.INC(range, 1)` is Q1 and `QUARTILE.INC(range, 3)` is Q3, as in Chapter 15. It uses the position rule above.

Excel shows as many decimals as the column is wide; the numbers here are rounded to what fits.

### The same in pandas

**Before you run the next cell, predict** what each number will be. You've just worked them all out.

<!-- py: reset -->
```python
import pandas as pd

week = pd.Series([2, 3, 3, 4, 5, 6, 19])
print(week.mean(), week.median(), week.max() - week.min())
print(week.mode())
```

```
6.0 4.0 17
0    3
dtype: int64
```

How it works:

- `pd.Series([...])` makes a pandas Series (Chapter 18) from a list of the seven numbers. `week` is its name.
- `.mean()`, `.median()`, `.max()`, and `.min()` do what `AVERAGE`, `MEDIAN`, `MAX`, and `MIN` do. The mean prints as `6.0` because dividing always gives a decimal number.
- `.mode()` returns a Series, not a single number, because a list can have several modes (two values that tie). Here there's one, the value 3, at position 0.

```python
print(week.var(), week.std())
print(week.quantile(0.25), week.quantile(0.75))
```

```
34.666666666666664 5.887840577551898
3.0 5.5
```

- `.var()` and `.std()` divide by *n* − 1, like `VAR.S` and `STDEV.S`. The long decimals are the full precision of the calculation; round only when you report.
- `.quantile(0.25)` is the 25th percentile, Q1, and `.quantile(0.75)` is Q3. pandas uses the same position rule as `QUARTILE.INC`, so the answers match.

### What happens if you change it

Suppose the slow delivery had taken 9 days instead of 19. Predict which of the mean, the standard deviation, and the IQR will change, then run it:

```python
week_faster = pd.Series([2, 3, 3, 4, 5, 6, 9])
print(round(week_faster.mean(), 2), round(week_faster.std(), 2))
print(week_faster.quantile(0.75) - week_faster.quantile(0.25))
```

```
4.57 2.37
2.5
```

- `round(value, 2)` (Chapter 17) keeps two decimals, so the result is easier to read.
- The mean fell from 6.0 to 4.57 and the standard deviation from 5.89 to 2.37. The IQR stayed at 2.5, because the change happened outside the middle half.

That is the chapter in miniature: the mean and the standard deviation feel every value, while the median and the IQR describe the typical case and ignore the extremes.

---

## 21.1 The centre: mean, median, and mode

Now the same measures on Riverstone's full year of deliveries. First, the libraries:

```python
import pandas as pd
import numpy as np
print(pd.__version__, np.__version__)
```

```
3.0.6 2.4.6
```

- `import numpy as np` loads NumPy under its usual short name. This chapter uses it for a few calculations pandas doesn't have: `np.sqrt` (square root), `np.std`, and random numbers.
- Printing `__version__` tells you which version you have. If you're continuing in the same notebook, `import pandas as pd` again does nothing new.

Then the data:

```python
deliveries = pd.read_csv("delivery_times_2025.csv", parse_dates=["order_date"])
print(deliveries.shape)
print(deliveries.dtypes)
```

```
(45040, 8)
order_id                  int64
order_date       datetime64[us]
branch                      str
customer_id               int64
order_value             float64
promised_days             int64
delivery_days           float64
on_time                    bool
dtype: object
```

- `parse_dates=["order_date"]` tells `read_csv` to read that column as dates rather than text, so you can pick out months later (section 21.4's festive season).
- `.shape` is (rows, columns): 45,040 delivered orders and 8 columns.
- `.dtypes` shows each column's type: whole numbers (`int64`), decimals (`float64`), text (`str`), dates (`datetime64`), and True/False (`bool`).

The eight columns:

| Column | Type | Meaning |
|---|---|---|
| `order_id` | whole number | The order, as in the Riverstone database |
| `order_date` | date | The day the order was placed |
| `branch` | text | The branch that shipped it: Mumbai HO, Bengaluru, Delhi, or Kolkata |
| `customer_id` | whole number | The customer who placed it |
| `order_value` | decimal | The order's net revenue, in rupees |
| `promised_days` | whole number | The branch's delivery promise: 5, 5, 6, or 7 days |
| `delivery_days` | decimal | How many days the delivery actually took |
| `on_time` | True/False | True when `delivery_days` is less than or equal to `promised_days` |

The first three rows, with every column shown:

```python
print(deliveries.head(3).to_string())
```

```
   order_id order_date     branch  customer_id  order_value  promised_days  delivery_days  on_time
0     10001 2025-01-02  Mumbai HO            2       2900.0              5            2.9     True
1     10002 2025-01-05  Mumbai HO            3      20900.0              5            3.3     True
2     10003 2025-01-12  Mumbai HO            5      45712.5              5            3.0     True
```

`.head(3)` takes the first three rows, and `.to_string()` prints all of them in full; without it, pandas hides middle columns behind `...` when a table is wider than the screen.

The mean and median order value:

```python
values = deliveries["order_value"]
print(f"mean   ₹{values.mean():,.2f}")
print(f"median ₹{values.median():,.2f}")
```

```
mean   ₹24,839.53
median ₹20,700.00
```

- `values` is the `order_value` column, kept under a short name.
- Inside the f-string (Chapter 17), `:,.2f` formats the number: `,` adds thousands separators and `.2f` shows two decimals.

The mode takes two steps. First look at what `.mode()` returns:

```python
print(values.mode())
```

```
0    1725.0
1    5800.0
Name: order_value, dtype: float64
```

It's a Series with **two** values: ₹1,725 and ₹5,800 tie as the most common order value. pandas lists tied modes from smallest to largest. Take the first one out, then count how often it appears:

```python
m = values.mode().iloc[0]
is_mode = values == m
print(is_mode.head(3).tolist())
print(f"mode ₹{m:,.2f}, appears {is_mode.sum()} times")
```

```
[False, False, False]
mode ₹1,725.00, appears 219 times
```

- `.iloc[0]` takes the value at position 0 (Chapter 18), so `m` is a plain number.
- `values == m` compares every order with it and gives a Series of True and False, one per order. `.head(3).tolist()` shows the first three as a list: none of those orders is worth ₹1,725.
- `.sum()` on True and False counts the Trues, because Python treats True as 1 and False as 0.

Why these two values? Each is one small order that keeps repeating: ₹1,725 is fifteen 1-litre water bottles at ₹115 each, and ₹5,800 is twenty stackable bins at ₹290, both with no discount. Each appears 219 times out of 45,040, under half a percent, and the next most common values appear 217 times. The spreadsheet's `MODE.SNGL` would return ₹5,800, because it appears first in the file. A "most common value" that depends on which tool you ask is why the mode says little about continuous money values.

- The **mean** adds everything up and divides by the count. It uses every value, which is its strength and its weakness: one enormous order moves it.
- The **median** is the middle value when they're sorted: half above, half below. A single huge order doesn't move it at all.
- The **mode** is the most common value. For continuous measures it's usually meaningless, as ₹1,725 shows; for categories ("the most common status") it's the only average that makes sense.

![Two histograms: order values with the mean above the median, and delivery times with a long right tail pulling the mean above the median](figures/fig21-1-mean-vs-median.svg)

*Figure 21.1 — When data has a long right tail, the mean sits above the median. Both are correct; they answer different questions.*

### Which one to report

| Situation | Use | Why |
|---|---|---|
| Money totals that must add up (revenue per order × orders = revenue) | **Mean** | Only the mean is consistent with the total |
| "What does a typical order look like?" | **Median** | Not dragged by a few large orders |
| Skewed data: incomes, order values, delivery times, waiting times | **Median**, with the mean alongside | The gap between them is information |
| Categories | **Mode** | There's nothing to average |
| Anything a target is set on | Say which one, explicitly | "Average delivery 4.4 days" and "median 3.8 days" are both true and imply different promises |

The gap itself is a finding: Riverstone's mean order value is about 20% above its median, which says a minority of large orders carry a disproportionate share of revenue. Chapter 15's advice applies — **show the distribution, don't only report its centre.**

> **Watch out: the average of averages.** The average of four branches' averages is not the company's average, unless the branches have the same number of orders. Weight by the count, or compute from the raw data. This mistake appears in real management packs constantly.

Chapter 4 met this mistake with discounts. Here it is with delivery days. The four branch means are 4.17 (Bengaluru, 12,562 orders), 4.82 (Delhi, 10,990), 6.33 (Kolkata, 5,626), and 3.51 days (Mumbai HO, 15,862). Their plain average is (4.17 + 4.82 + 6.33 + 3.51) ÷ 4 = 4.71 days. But Kolkata, the slowest branch, has the fewest orders, so it shouldn't count as much as Mumbai HO. The **weighted mean** multiplies each branch's mean by its count, adds those up, and divides by the total count: Σ(countᵢ × meanᵢ) ÷ Σcountᵢ. In pandas:

```python
by_branch = deliveries.groupby("branch")["delivery_days"].agg(["count", "mean"])
print(by_branch.round(2))
naive = by_branch["mean"].mean()
weighted = (by_branch["count"] * by_branch["mean"]).sum() / by_branch["count"].sum()
print(f"average of the four branch averages: {naive:.2f} days")
print(f"weighted by each branch's orders:    {weighted:.2f} days")
print(f"straight from the 45,040 rows:       {deliveries['delivery_days'].mean():.2f} days")
```

```
           count  mean
branch
Bengaluru  12562  4.17
Delhi      10990  4.82
Kolkata     5626  6.33
Mumbai HO  15862  3.51
average of the four branch averages: 4.71 days
weighted by each branch's orders:    4.37 days
straight from the 45,040 rows:       4.37 days
```

- `.agg(["count", "mean"])` gives each branch's number of orders and mean delivery time (Chapter 18).
- `by_branch["mean"].mean()` is the naive average of the four averages.
- `by_branch["count"] * by_branch["mean"]` multiplies row by row; `.sum()` adds the four products, and dividing by the total count gives the weighted mean. It matches the mean of all 45,040 rows exactly.

The naive figure is a third of a day too slow. On order value, the same mistake costs only about ₹45 (₹24,794 against ₹24,840), because the four branches' average orders are nearly equal. The mistake bites when the groups differ both in size and in value.

---

## 21.2 Spread: range, variance, standard deviation, and IQR

A centre without a spread is half an answer. "Delivery takes about four days" means something very different if every order arrives in 3–5 days than if a quarter arrive in nine.

```python
days = deliveries["delivery_days"]
q1, q3 = days.quantile(0.25), days.quantile(0.75)
print(f"range          {days.min():.1f} to {days.max():.1f} days")
print(f"variance       {days.var():.2f} (days squared, which is why nobody quotes it)")
print(f"std deviation  {days.std():.2f} days")
print(f"IQR            {q3 - q1:.2f} days (from {q1:.1f} to {q3:.1f})")
print(f"mean ± 1 sd    {days.mean() - days.std():.1f} to {days.mean() + days.std():.1f} days")
```

```
range          1.0 to 37.9 days
variance       5.21 (days squared, which is why nobody quotes it)
std deviation  2.28 days
IQR            2.10 days (from 3.0 to 5.1)
mean ± 1 sd    2.1 to 6.6 days
```

- `q1, q3 = ..., ...` stores two results in one line: the first goes into `q1`, the second into `q3`.
- `.1f` and `.2f` in the f-strings show one or two decimals.
- The last line is the mean minus and plus one standard deviation.

The same measures as in section 21.0, now on 45,040 values:

- **Range** (max − min) is simple and fragile: one bad order defines it.
- **Variance**, *s*² = Σ(xᵢ − x̄)² ÷ (*n* − 1), is the average squared distance from the mean. Squaring removes the signs, and leaves the answer in "days squared", which means nothing to anyone.
- **Standard deviation**, *s* = √*s*², is the square root of the variance, back in the original units. It's the default measure of spread, and it assumes a roughly symmetric distribution to be interpretable.
- **The interquartile range**, IQR = Q3 − Q1, where Q1 and Q3 are the 25th and 75th percentiles, is the width of the middle half. It ignores the tails entirely, which is why it's the right measure for skewed business data.

### Sample or population?

pandas' `.std()` divides by *n* − 1 (the sample standard deviation, like `STDEV.S`). NumPy's `np.std()` divides by *n* unless you tell it otherwise (like `STDEV.P`). On the seven deliveries from section 21.0 the difference is easy to see:

```python
print(f"pandas  week.std()            {week.std():.2f}   (divides by n - 1 = 6)")
print(f"numpy   np.std(week)          {np.std(week):.2f}   (divides by n = 7)")
print(f"numpy   np.std(week, ddof=1)  {np.std(week, ddof=1):.2f}")
```

```
pandas  week.std()            5.89   (divides by n - 1 = 6)
numpy   np.std(week)          5.45   (divides by n = 7)
numpy   np.std(week, ddof=1)  5.89
```

- `np.std(week)` is the population formula, σ = √(Σ(xᵢ − μ)² ÷ *n*): 5.45, as by hand.
- `ddof` stands for "delta degrees of freedom": the divisor is *n* − `ddof`. The default `ddof=0` divides by *n*; `ddof=1` divides by *n* − 1, which gives pandas' answer, 5.89.

Now the same three on all 45,040 delivery times:

```python
print(f"pandas  days.std()            {days.std():.4f}   (divides by n - 1)")
print(f"numpy   np.std(days)          {np.std(days):.4f}   (divides by n)")
print(f"numpy   np.std(days, ddof=1)  {np.std(days, ddof=1):.4f}")
```

```
pandas  days.std()            2.2823   (divides by n - 1)
numpy   np.std(days)          2.2823   (divides by n)
numpy   np.std(days, ddof=1)  2.2823
```

With 45,040 rows, dividing by 45,039 or 45,040 makes no difference you can see; with seven it's 5.89 against 5.45. Use the sample version unless you really have the whole population.

### Comparing spread across groups

![Horizontal box plots of delivery time by branch, with medians, IQRs, the 95th percentile, and the promised days as a dashed line](figures/fig21-2-spread-by-branch.svg)

*Figure 21.2 — Four branches, four different spreads. Kolkata's median is 2.5 days above Mumbai's, and its middle half is 2.5 times as wide.*

The numbers behind the figure take three steps. First, the measures `.agg` can name directly:

```python
by_branch = deliveries.groupby("branch")["delivery_days"].agg(["count", "median", "mean", "std"])
print(by_branch.round(2))
```

```
           count  median  mean   std
branch
Bengaluru  12562     3.8  4.17  1.89
Delhi      10990     4.4  4.82  2.16
Kolkata     5626     5.7  6.33  3.11
Mumbai HO  15862     3.2  3.51  1.74
```

There's no ready-made name for "the 25th percentile", so you give `.agg` a small function instead. Check the calculation on one branch first:

```python
kolkata_days = deliveries.loc[deliveries["branch"] == "Kolkata", "delivery_days"]
print(kolkata_days.quantile(0.25), kolkata_days.quantile(0.75))

q1_of = lambda s: s.quantile(0.25)
print(q1_of(kolkata_days))
```

```
4.2 7.7
4.2
```

- `deliveries.loc[condition, "delivery_days"]` (Chapter 18) keeps Kolkata's rows and only the delivery-time column.
- `lambda s: s.quantile(0.25)` is a **lambda**: a function written in one line, with no name and no `def`. It reads "given a column `s`, return its 25th percentile". It does the same as `def q1_of(s): return s.quantile(0.25)` from Chapter 17.
- `q1_of(kolkata_days)` calls it on Kolkata's column and gives the same 4.2 as the line above.

Now hand `.agg` one function per measure, each under the name you want as its column:

```python
summary = (deliveries.groupby("branch")["delivery_days"]
           .agg(orders="count", median="median", mean="mean", sd="std",
                q1=lambda s: s.quantile(0.25), q3=lambda s: s.quantile(0.75),
                p95=lambda s: s.quantile(0.95))
           .assign(iqr=lambda d: d["q3"] - d["q1"])
           .round(2))
print(summary[["orders", "median", "mean", "sd", "iqr", "p95"]])
```

```
           orders  median  mean    sd   iqr   p95
branch
Bengaluru   12562     3.8  4.17  1.89  1.88   6.9
Delhi       10990     4.4  4.82  2.16  2.20   8.4
Kolkata      5626     5.7  6.33  3.11  3.50  12.0
Mumbai HO   15862     3.2  3.51  1.74  1.40   5.7
```

- `orders="count"` is **named aggregation**: the name on the left becomes the column, and the calculation on the right fills it. The ready-made names are text (`"count"`, `"median"`); the percentiles are lambdas, run once per branch.
- `.assign(iqr=lambda d: d["q3"] - d["q1"])` adds a column to the result: here `d` is the whole summary table, and the new `iqr` column is Q3 minus Q1 for each branch.
- `.round(2)` rounds every number to two decimals, and the list in `summary[[...]]` picks the columns to print and their order.
- The brackets around the whole chain let it run over several lines, one step per line.

The averages differ, but the spreads differ more. Kolkata's mean is 1.8 times Mumbai HO's (6.33 against 3.51 days), but its middle half is 2.5 times as wide: Mumbai HO's spans 1.4 days, Kolkata's 3.5. That's the difference between a promise you can keep and a promise you can only hope for.

### The coefficient of variation

To compare spread between things measured in different units, divide the standard deviation by the mean. The **coefficient of variation** is CV = *s* ÷ x̄, and it has no unit:

```python
for name, series in [("order value", deliveries["order_value"]), ("delivery days", days)]:
    print(f"{name:>14}: mean {series.mean():,.2f}, sd {series.std():,.2f}, CV {series.std()/series.mean():.2f}")
```

```
   order value: mean 24,839.53, sd 18,220.98, CV 0.73
 delivery days: mean 4.37, sd 2.28, CV 0.52
```

- The list holds two pairs, each a label and a column. `for name, series in ...` unpacks each pair into two names, as with the tuples in Chapter 17, so the loop runs once for order value and once for delivery days.
- `{name:>14}` right-aligns the label in 14 characters, so the two lines line up (`<` aligns left, as in Chapter 17; `>` aligns right).
- By hand: 18,220.98 ÷ 24,839.53 = 0.73 for order value, and 2.28 ÷ 4.37 = 0.52 for delivery days.

A CV above about 0.5 says "this measure is volatile relative to its size", which is a useful, tool-free way to tell a stakeholder that an average alone will mislead them. Treat 0.5 as a rough rule of thumb, not a standard. And use the CV only for measures with a true zero (money, days, counts), never for temperatures or scores that can be negative, where dividing by the mean means nothing.

---

## 21.3 Percentiles and service levels

A **percentile** is the value below which a given share of the data falls. The 90th percentile of delivery time is the number that 90% of orders beat. It's found with the position rule from section 21.0.

```python
for p in [0.5, 0.75, 0.9, 0.95, 0.99]:
    print(f"p{int(p*100):<3} {days.quantile(p):>5.1f} days")
print()
print("share of orders delivered within the promise:", f"{deliveries['on_time'].mean()*100:.1f}%")
print(deliveries.groupby("branch")["on_time"].mean().mul(100).round(1).to_dict())
```

```
p50    3.8 days
p75    5.1 days
p90    6.8 days
p95    8.2 days
p99   13.1 days

share of orders delivered within the promise: 81.8%
{'Bengaluru': 78.0, 'Delhi': 80.0, 'Kolkata': 68.1, 'Mumbai HO': 90.8}
```

- The loop runs once per percentile. `int(p*100)` turns 0.9 into the whole number 90 for the label, and `:<3` pads it to three characters so the columns line up. `:>5.1f` right-aligns the answer in five characters with one decimal.
- `print()` with nothing inside prints an empty line.
- `deliveries['on_time'].mean()` is the share of Trues, because True counts as 1 and False as 0; times 100 it's a percentage.
- The last line goes step by step: the on-time share per branch (`.mean()`), times 100 (`.mul(100)`), rounded to one decimal, then turned into a dictionary (`.to_dict()`, Chapter 17) so it prints on one line.

Percentiles are how service levels are written, because they say what customers actually experience:

- **"We deliver in 4.4 days on average"** describes nobody: half the orders are slower.
- **"95% of orders arrive within 8.2 days"** is a promise you can check, and a customer can plan around.

Riverstone promises 5 days (Mumbai HO and Bengaluru), 6 (Delhi), and 7 (Kolkata). At those promises, 81.8% of orders arrive on time overall, and Kolkata is worst at 68.1%. Two ways to fix a number like that: make the process faster, or make the promise honest. Analysts should present both.

> **Tool note: percentile methods differ.** pandas and NumPy interpolate between the two nearest values by default (the position rule in section 21.0). The spreadsheet has `PERCENTILE.INC` and `QUARTILE.INC` (inclusive, matching pandas) and `PERCENTILE.EXC` (exclusive, which uses a slightly different position rule). PostgreSQL has `PERCENTILE_CONT` (interpolated, Chapter 15, section 15.5) and `PERCENTILE_DISC` (always an actual data value). On thousands of rows they agree to a rounding; on twenty rows they don't. State which you used.

### The same measures in SQL (optional, PostgreSQL)

PostgreSQL can compute the centre and spread in one query. On the three-year database (`riverstone_full`, from Chapter 14), one row per delivered 2025 order:

<!-- db: riverstone_full -->
```sql
WITH delivered AS (
  SELECT order_id, SUM(net_revenue) AS order_value
  FROM sales_lines
  WHERE status = 'Delivered' AND order_date >= '2025-01-01'
  GROUP BY order_id
)
SELECT COUNT(*) AS orders,
       ROUND(AVG(order_value), 2) AS mean,
       ROUND(STDDEV_SAMP(order_value), 2) AS sd_sample,
       ROUND(STDDEV_POP(order_value), 2) AS sd_population,
       ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY order_value)::numeric, 2) AS p99_cont,
       ROUND(PERCENTILE_DISC(0.99) WITHIN GROUP (ORDER BY order_value), 2) AS p99_disc
FROM delivered;
```

```
 orders |   mean   | sd_sample | sd_population | p99_cont | p99_disc 
--------+----------+-----------+---------------+----------+----------
  45040 | 24839.53 |  18220.98 |      18220.78 | 82790.08 | 82812.50
(1 row)
```

How it works:

- The CTE `delivered` (Chapter 13) makes one row per delivered 2025 order, the same 45,040 orders as the CSV file.
- `STDDEV_SAMP` is the sample standard deviation (divides by *n* − 1, like pandas and `STDEV.S`); `STDDEV_POP` is the population version (divides by *n*, like `np.std` and `STDEV.P`).
- `PERCENTILE_CONT(0.99)` interpolates, so it matches pandas' 99th percentile, ₹82,790.08. `PERCENTILE_DISC(0.99)` returns the first actual order value at or above the 99% mark, ₹82,812.50, an order that really exists.
- `PERCENTILE_CONT` returns a type `ROUND` won't take with two decimals, so `::numeric` converts it first (the `::` cast from Chapter 12).

MySQL has `STDDEV_SAMP` and `STDDEV_POP` too, but no percentile functions (Chapter 15, section 15.5 shows the workarounds).

---

## 21.4 Shape: skew, tails, and outliers

```python
for name, series in [("order value", deliveries["order_value"]), ("delivery days", days)]:
    print(f"{name:>14}: skew {series.skew():+.2f}, excess kurtosis {series.kurt():+.2f}, "
          f"mean/median {series.mean()/series.median():.2f}")
```

```
   order value: skew +1.27, excess kurtosis +2.03, mean/median 1.20
 delivery days: skew +3.13, excess kurtosis +18.45, mean/median 1.15
```

- `.skew()` and `.kurt()` are pandas' skew and excess kurtosis, defined below. The spreadsheet's `SKEW` and `KURT` use the same adjusted formulas, so they give the same answers.
- `:+.2f` shows two decimals and always prints the sign, `+` or `−`.
- Two f-strings side by side inside the brackets join into one; that's how a long line is split in two.

What the numbers mean:

- **Skew** measures asymmetry. Roughly, it takes each value's distance from the mean, measured in standard deviations, cubes it, and averages. Cubing keeps the sign, so a long tail of large values, far above the mean, makes the skew positive. Positive (right) skew means a long tail of large values: money, waiting times, and durations almost always have it, as Figure 21.1 shows. Negative skew (a long left tail) is rarer in business: exam scores near a ceiling, or ages at retirement. A symmetric distribution has a skew of 0.
- **Kurtosis** describes the weight of the tails. The normal distribution (section 21.5) has a kurtosis of 3, so analysts usually quote **excess kurtosis** = kurtosis − 3, which is 0 for a normal distribution. High excess kurtosis means extreme values are more common than a normal distribution would suggest, which matters when you're setting limits. Delivery days, at +18.45, have far heavier tails than a normal distribution.
- **The quickest check of all:** compare the mean and the median. Equal means symmetric; mean well above median means right skew.

### Outliers

Chapter 14 treated outliers as a data-quality question (is it an error?). Here they're a statistical one (is it *unusual*?). Two standard rules. The first is Chapter 15's fence. The second uses the **z-score**: z = (x − x̄) ÷ *s*, which says how many standard deviations a value sits from the mean. A delivery of 8.93 days has z = (8.93 − 4.37) ÷ 2.28 = 2.

```python
q1, q3 = days.quantile(0.25), days.quantile(0.75)
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr
z_scores = (days - days.mean()) / days.std()

print(f"lower fence {lower_fence:.2f} days, upper fence {upper_fence:.2f} days")
print(f"IQR rule: above {upper_fence:.2f} days → {(days > upper_fence).sum():,} orders "
      f"({(days > upper_fence).mean()*100:.1f}%)")
print(f"z > 3   : above {days.mean() + 3*days.std():.2f} days → {(z_scores > 3).sum():,} orders "
      f"({(z_scores > 3).mean()*100:.1f}%)")
print(f"the slowest five: {sorted(days.nlargest(5).round(1).tolist())}")
```

```
lower fence -0.15 days, upper fence 8.25 days
IQR rule: above 8.25 days → 2,220 orders (4.9%)
z > 3   : above 11.21 days → 772 orders (1.7%)
the slowest five: [29.9, 30.7, 31.6, 37.6, 37.9]
```

How it works:

- `lower_fence` and `upper_fence` are Q1 − 1.5 × IQR and Q3 + 1.5 × IQR. The lower fence is below zero, and no delivery takes less than zero days, so nothing can be an outlier on the low side. That in itself is a sign of right skew.
- `z_scores` applies the z-score formula to every delivery at once: subtract the mean, divide by the standard deviation.
- `days > upper_fence` gives True for each order beyond the fence; `.sum()` counts them and `.mean()` gives their share, as in section 21.1. `:,` puts a thousands separator in the count.
- `days.nlargest(5)` takes the five largest values; `.round(1).tolist()` rounds them and makes a list, and `sorted(...)` puts it in order from smallest to largest.

The two rules:

- **The IQR rule** (below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR) is what a box plot draws. It's distribution-free, which makes it the safer default for skewed data.
- **The z-score rule** (more than 3 standard deviations from the mean) assumes roughly normal data. On right-skewed data it flags no small values at all (the mean minus 3 sd is below zero) and, because the long tail inflates the standard deviation, it flags fewer large values than the IQR rule: here 772 against 2,220.

Both rules produce **candidates**, not verdicts. A 38-day delivery is a question for operations, not a row to delete. And note what the numbers say here: on right-skewed data the IQR rule flags several percent of orders, which is a lot of questions. Tune the multiplier (2.0 or 3.0 instead of 1.5) to the number of investigations you can actually do.

### Checkpoint: the first half

Before moving on to probability, check that the descriptive measures are yours. Take ten minutes, with a pencil, no computer. Nine deliveries took 1, 2, 2, 3, 4, 4, 5, 6, and 9 days. Work out the mean, the median, the sample standard deviation, Q1, Q3, and the IQR, using the methods in section 21.0. Then check your answers in a spreadsheet or with `pd.Series`. (Answers at the end of the chapter.)

---

## 21.5 Four distributions worth knowing

A **distribution** describes how likely each value is. Knowing which one a measure follows tells you what's normal, what's rare, and which formula to use.

![Four small charts: a normal bell curve, a binomial distribution of late deliveries out of 40, a Poisson distribution of weekly complaints, and a flat uniform distribution](figures/fig21-3-distributions.svg)

*Figure 21.3 — The four distributions an analyst meets most, with a business example of each.*

| Distribution | Describes | Riverstone example | Key numbers |
|---|---|---|---|
| **Normal** | A measure pushed around by many small independent influences | Filling weight of a moulded crate; measurement error | mean, standard deviation |
| **Binomial** | The count of successes in *n* independent yes/no trials | How many of 40 deliveries are late | *n*, *p* |
| **Poisson** | The count of events in a fixed window, at a steady average rate | Complaints per week; orders per hour | λ (the average rate) |
| **Uniform** | Every outcome equally likely | A random sample; a die | min, max |

### Installing scipy

The distributions live in **scipy**, a library of scientific functions; its `scipy.stats` part holds distributions and statistical tests. It isn't part of the packages installed so far. In a terminal, activate your project's virtual environment (Chapter 17, section 17.3), then install it:

```bash
python -m pip install scipy
```

Then check it in your notebook:

```python
import scipy
from scipy import stats
print(scipy.__version__)
```

```
1.17.1
```

- `import scipy` loads the library, and `__version__` confirms which version you have.
- `from scipy import stats` loads the part this chapter uses, under the name `stats`. Every distribution below is `stats.` followed by its name: `stats.norm`, `stats.binom`, `stats.poisson`.

### Four questions, four functions

Every scipy distribution answers the same four questions, with the same four function names:

| Function | Question it answers | Example |
|---|---|---|
| `pmf(k)` | For counts: what's the probability of **exactly** *k*? ("probability mass function") | P(exactly 7 late) |
| `pdf(x)` | For a smooth measure: how tall is the curve at *x*? ("probability density function") It's not a probability by itself; only areas under the curve are | Drawing the bell curve |
| `cdf(x)` | What's the probability of **x or less**? ("cumulative distribution function") | P(weight ≤ 494 g) |
| `ppf(q)` | Which value has a share *q* at or below it? It's `cdf` backwards ("percent point function") | The weight only 1% of crates fall below |

For "more than", use the complement: P(more than *x*) = 1 − P(*x* or less) = `1 - cdf(x)`. scipy also has `sf(x)`, the "survival function", which is the same thing.

### Normal

The **normal distribution** is the bell curve: symmetric around its mean μ, with its spread set by the standard deviation σ. Riverstone's moulded crates are filled to a target weight of 500 g, and the process varies with a standard deviation of 4 g. What share of crates weigh less than 494 g?

```python
print(stats.norm.cdf(494, loc=500, scale=4))
print(stats.norm.cdf(494, 500, 4))
```

```
0.06680720126885807
0.06680720126885807
```

- `stats.norm.cdf(x, loc=..., scale=...)` is P(weight ≤ x). For the normal distribution, `loc` is the mean and `scale` is the standard deviation.
- The second line gives the same answer with the arguments by position: x first, then the mean, then the standard deviation. The rest of this section uses the shorter form.

About 6.7% of crates are under 494 g. The spreadsheet equivalent is `=NORM.DIST(494,500,4,TRUE)`, where `TRUE` asks for the cumulative probability (the `cdf`); `FALSE` would give the height of the curve (the `pdf`).

```python
mu, sigma = 500.0, 4.0          # a moulded crate: target weight 500 g, process sd 4 g
print(f"P(weight < 494 g) = {stats.norm.cdf(494, mu, sigma):.4f}")
print(f"P(494 g ≤ weight ≤ 506 g) = {stats.norm.cdf(506, mu, sigma) - stats.norm.cdf(494, mu, sigma):.4f}")
print(f"the weight only 1% of crates fall below: {stats.norm.ppf(0.01, mu, sigma):.2f} g")
for k in (1, 2, 3):
    inside = stats.norm.cdf(mu + k*sigma, mu, sigma) - stats.norm.cdf(mu - k*sigma, mu, sigma)
    print(f"within ±{k} sd: {inside*100:.1f}%")
```

```
P(weight < 494 g) = 0.0668
P(494 g ≤ weight ≤ 506 g) = 0.8664
the weight only 1% of crates fall below: 490.69 g
within ±1 sd: 68.3%
within ±2 sd: 95.4%
within ±3 sd: 99.7%
```

- `mu, sigma = 500.0, 4.0` names the mean and standard deviation after their symbols, μ and σ. The `#` comment says what they are.
- The share **between** two weights is P(≤ 506) − P(≤ 494): everything up to 506, minus everything up to 494.
- `stats.norm.ppf(0.01, mu, sigma)` runs the question backwards: the weight with 1% of crates at or below it. In the spreadsheet, `=NORM.INV(0.01,500,4)`.
- The loop does the same "between" calculation for one, two, and three standard deviations either side of the mean.

That last block is the **68–95–99.7 rule**, worth memorizing: about 68% of a normal distribution lies within one standard deviation of the mean, 95% within two, and 99.7% within three. It's why "three sigma" became shorthand for "shouldn't happen".

**Most business data is not normal.** Order values, delivery times, and revenue are right-skewed. The normal distribution earns its place because of the central limit theorem (section 21.8), which makes *averages* behave normally even when the underlying data doesn't.

### Binomial

The **binomial distribution** counts successes in *n* independent yes/no trials, each with the same probability *p*. Here a "success" is a late delivery, and 18.2% of Riverstone's deliveries are late.

Start small, by hand: three deliveries, each late with probability 0.182. What's the chance **exactly one** is late? Write L for late and O for on time. There are three ways: LOO, OLO, OOL. Each way has probability 0.182 × 0.818 × 0.818, by Chapter 4's rule for independent events (multiply). So:

P(exactly 1 late) = 3 × 0.182 × 0.818² = 3 × 0.182 × 0.669 = **0.365**

The general formula does the same counting:

**P(X = *k*) = C(*n*, *k*) × *p*ᵏ × (1 − *p*)ⁿ⁻ᵏ**

- X is the number of late deliveries; *k* is the count you're asking about.
- *p*ᵏ is the chance that *k* particular deliveries are late, and (1 − *p*)ⁿ⁻ᵏ the chance that the other *n* − *k* are on time.
- C(*n*, *k*), said "*n* choose *k*", is the number of ways to choose which *k* of the *n* deliveries are the late ones. Above, C(3, 1) = 3: LOO, OLO, OOL.

The spreadsheet has `=COMBIN(3,1)` → 3 for C(*n*, *k*), but you'll rarely need it, because the function does it all:

```python
print(f"{stats.binom.pmf(1, 3, 0.182):.4f}")
```

```
0.3653
```

`stats.binom.pmf(k, n, p)` is P(exactly *k*) for *n* trials with probability *p*: the hand answer. The spreadsheet's version is `=BINOM.DIST(1,3,0.182,FALSE)`, where `FALSE` means "exactly", not "or fewer".

Now a real day, with 40 deliveries:

```python
n, p = 40, 0.182                 # 40 deliveries in a day; 18.2% arrive late overall
print(f"expected late: {n*p:.1f}, sd {(n*p*(1-p))**0.5:.2f}")
print(f"P(exactly 7 late)   = {stats.binom.pmf(7, n, p):.4f}")
print(f"P(10 or more late)  = {1 - stats.binom.cdf(9, n, p):.4f}")
print(f"P(3 or fewer late)  = {stats.binom.cdf(3, n, p):.4f}")
```

```
expected late: 7.3, sd 2.44
P(exactly 7 late)   = 0.1629
P(10 or more late)  = 0.1791
P(3 or fewer late)  = 0.0509
```

- A binomial count has mean *n* × *p* and standard deviation √(*n* × *p* × (1 − *p*)). `**0.5` raises to the power one half, which is the square root.
- `stats.binom.cdf(9, n, p)` is P(9 or fewer). "10 or more" is everything else, so it's `1 - cdf(9)`. On a number line of possible counts:

  | 0, 1, 2, …, 9 | 10, 11, …, 40 |
  |---|---|
  | 9 or fewer: `cdf(9)` | 10 or more: `1 - cdf(9)` |

- Spreadsheet equivalents: `=BINOM.DIST(7,40,0.182,FALSE)` for exactly 7, and `=1-BINOM.DIST(9,40,0.182,TRUE)` for 10 or more.

So on a normal day with 40 deliveries, seeing 10 late is not alarming (it happens about 18% of the time: roughly one day in five or six), and seeing 3 or fewer is real good news. That's how you set an alert threshold that doesn't fire every week: work out what "normal" produces before you pick a number.

### Poisson

The **Poisson distribution** counts events in a fixed window (a week, an hour) when they happen independently at a steady average rate, written λ ("lambda"). Riverstone receives 9.4 complaints a week on average. The formula:

**P(X = *k*) = λᵏ × e^(−λ) ÷ *k*!**

- *k*! ("*k* factorial") is *k* × (*k* − 1) × … × 1, so 3! = 3 × 2 × 1 = 6; by definition 0! = 1.
- *e* is a fixed number, about 2.718, that appears wherever growth or decay is continuous. The spreadsheet writes e^(−λ) as `=EXP(-9.4)`.
- By hand, a week with no complaints: λ⁰ = 1 and 0! = 1, so P(0) = e^(−9.4) ≈ 0.000083. About one week in 12,000.

```python
lam = 9.4                        # complaints per week, on average
print(f"P(no complaints)        = {stats.poisson.pmf(0, lam):.4f}")
print(f"P(15 or more)           = {1 - stats.poisson.cdf(14, lam):.4f}")
print(f"P(more than 15)         = {1 - stats.poisson.cdf(15, lam):.4f}")
print(f"smallest count with at least 95% of weeks at or below it: {stats.poisson.ppf(0.95, lam):.0f}")
```

```
P(no complaints)        = 0.0001
P(15 or more)           = 0.0559
P(more than 15)         = 0.0309
smallest count with at least 95% of weeks at or below it: 15
```

- `lam` is λ; the name `lambda` itself is taken by Python (section 21.2), hence the shorter spelling.
- `stats.poisson.pmf(0, lam)` is P(exactly 0). Printed to four decimals it's 0.0001; the hand value, 0.000083, rounds to that.
- `1 - stats.poisson.cdf(14, lam)` is P(15 or more), and `1 - stats.poisson.cdf(15, lam)` is P(more than 15). For counts, "15 or more" and "more than 15" differ by one, and here the difference is 5.6% against 3.1%.
- `stats.poisson.ppf(0.95, lam)` is 15: at least 95% of weeks have 15 complaints or fewer, so more than 15 happens in about 3% of weeks.
- Spreadsheet equivalents: `=POISSON.DIST(0,9.4,FALSE)` and `=1-POISSON.DIST(14,9.4,TRUE)`.

The Poisson distribution is the right model for counts of independent events at a steady rate: complaints, machine stoppages, orders arriving at a call centre. Its striking property is that its variance equals its mean, so a count with much more variation than that is telling you the events aren't independent (complaints cluster when a batch goes wrong).

### Uniform, and where randomness comes from

In a **uniform distribution** every outcome is equally likely, like the six faces of a fair die. A computer makes random numbers with a **random number generator**, and you can roll a die 6,000 times in one line:

```python
rng = np.random.default_rng(21)
rolls = pd.Series(rng.integers(1, 7, size=6000))
print(rolls.value_counts().sort_index().to_dict())
print(f"mean of the rolls: {rolls.mean():.3f}")
```

```
{1: 973, 2: 1030, 3: 978, 4: 973, 5: 1036, 6: 1010}
mean of the rolls: 3.517
```

- `np.random.default_rng(21)` makes a NumPy random number generator. The 21 is its **seed**: the same seed gives the same "random" numbers every time, so anyone can reproduce your result.
- `rng.integers(1, 7, size=6000)` draws 6,000 whole numbers from 1 up to, but not including, 7: the faces 1 to 6. `pd.Series(...)` turns them into a Series.
- `.value_counts().sort_index()` counts each face and sorts by face; each is close to 1,000, as a uniform distribution predicts.

The mean of a distribution is called its **expected value**: the long-run average of many draws. A die's expected value is (1 + 2 + 3 + 4 + 5 + 6) ÷ 6 = 3.5, and 6,000 rolls come very close to it.

The uniform distribution also underlies sampling: when you draw a random sample, every row must have the same chance of selection. `DataFrame.sample` does that, and its `random_state` is the seed:

```python
print(deliveries.sample(n=3, random_state=42)["order_id"].tolist())
print(deliveries.sample(n=3, random_state=42)["order_id"].tolist())
print(deliveries.sample(n=3, random_state=7)["order_id"].tolist())
```

```
[271646, 280957, 286797]
[271646, 280957, 286797]
[287038, 286314, 301940]
```

- `deliveries.sample(n=3, random_state=42)` picks three rows at random; `["order_id"].tolist()` lists their order numbers.
- The first two lines use the same seed and pick the same three orders; the third, with a different seed, picks others. That repeatability matters when someone asks you to reproduce a number.

---

## 21.6 Probability rules

**Probability** is a number between 0 and 1 giving the long-run share of times something happens. Chapter 4 worked it out by counting: "how often, out of how many". Start there with the deliveries. Every order is either late or on time, and either Kolkata's or another branch's, so there are four kinds of order:

| | Late | On time | Total |
|---|---:|---:|---:|
| **Kolkata** | 1,792 | 3,834 | 5,626 |
| **Other branches** | 6,422 | 32,992 | 39,414 |
| **Total** | 8,214 | 36,826 | 45,040 |

Every probability in this section comes from these counts:

- P(late) = 8,214 ÷ 45,040 = **0.1824**
- P(Kolkata) = 5,626 ÷ 45,040 = **0.1249**
- P(late and Kolkata) = 1,792 ÷ 45,040 = **0.0398**
- P(late, given Kolkata) = 1,792 ÷ 5,626 = **0.3185**: only Kolkata's row counts, so the denominator shrinks, as in Chapter 4.
- P(Kolkata, given late) = 1,792 ÷ 8,214 = **0.2182**: only the late column counts.

The bar in P(B | A) is read "given": the probability of B **given** A. Four rules cover almost everything an analyst needs.

1. **Complement:** P(not A) = 1 − P(A). The probability a delivery is *not* late is 1 minus the probability it is: 1 − 0.1824 = 0.8176.
2. **Addition:** P(A or B) = P(A) + P(B) − P(A and B). Subtract the overlap, or you count it twice: the 1,792 late Kolkata orders are in both the late column and the Kolkata row. If A and B can't both happen (they're **mutually exclusive**, like "delivered by Kolkata" and "delivered by Delhi"), P(A and B) = 0 and the rule becomes P(A) + P(B).
3. **Multiplication:** P(A and B) = P(A) × P(B | A). If A and B are **independent**, P(B | A) = P(B), and it simplifies to P(A) × P(B).
4. **Conditional:** P(B | A) = P(A and B) ÷ P(A). That's the counting above, written with shares instead of counts: 0.0398 ÷ 0.1249 = 0.3185.

pandas builds the count table with `pd.crosstab`:

```python
late = ~deliveries["on_time"]
kolkata = deliveries["branch"] == "Kolkata"
print(pd.crosstab(kolkata, late, rownames=["Kolkata?"], colnames=["late?"], margins=True))
```

```
late?     False  True    All
Kolkata?
False     32992  6422  39414
True       3834  1792   5626
All       36826  8214  45040
```

- `~` means NOT: it flips every True to False and every False to True, so `late` is True for each late order.
- `deliveries["branch"] == "Kolkata"` is True for each Kolkata order.
- `pd.crosstab(rows, columns)` counts every combination of the two, like a pivot table with a count (Chapter 11). `rownames` and `colnames` label the two sides, and `margins=True` adds the `All` totals.

The same probabilities, straight from the True/False columns:

```python
p_late = late.mean()
p_kolkata = kolkata.mean()
p_both = (late & kolkata).mean()

print(f"P(late)                 = {p_late:.4f}")
print(f"P(Kolkata)              = {p_kolkata:.4f}")
print(f"P(late and Kolkata)     = {p_both:.4f}")
print(f"P(late or Kolkata)      = {p_late + p_kolkata - p_both:.4f}")
print(f"P(late | Kolkata)       = {p_both / p_kolkata:.4f}")
print(f"P(Kolkata | late)       = {p_both / p_late:.4f}")
print(f"independent? P(late)×P(Kolkata) = {p_late * p_kolkata:.4f} vs P(both) = {p_both:.4f}")
```

```
P(late)                 = 0.1824
P(Kolkata)              = 0.1249
P(late and Kolkata)     = 0.0398
P(late or Kolkata)      = 0.2675
P(late | Kolkata)       = 0.3185
P(Kolkata | late)       = 0.2182
independent? P(late)×P(Kolkata) = 0.0228 vs P(both) = 0.0398
```

- `.mean()` of a True/False column is the share of Trues, so `late.mean()` is P(late).
- `&` means AND: `late & kolkata` is True only where both are True. Keep each side a named column, or wrap it in brackets, because `&` is applied before `==`.
- The next lines are the rules: the addition rule for "or", the conditional rule for "given" (divide by the probability of what's given), and the independence check.

Read those last three lines carefully, because they're the most misread numbers in business analysis:

- **P(late | Kolkata) = 31.9%** — about a third of Kolkata's orders are late.
- **P(Kolkata | late) = 21.8%** — about a fifth of late orders are Kolkata's.

They answer different questions and they're not interchangeable. The first is a statement about Kolkata's process; the second is a statement about where your late deliveries come from. Confusing them is called the **confusion of the inverse** (in law, the **prosecutor's fallacy**). Its close cousin, ignoring how common something is in the first place, is the **base rate fallacy**, and it's the engine of the next section.

And because P(late) × P(Kolkata) ≠ P(late and Kolkata), lateness and branch are **not independent**: knowing the branch changes the odds. That's exactly what makes branch a useful column in a model (Part 4).

---

## 21.7 Bayes' rule

Bayes' rule updates a probability when new evidence arrives. Start with counts, as in section 21.6, and the formula will follow.

### A worked Riverstone example

Riverstone's quality team tests moulded crates with a quick visual check. From history:

- **2%** of crates have a defect.
- The check flags **90%** of truly defective crates.
- It also flags **5%** of good crates, by mistake.

A crate is flagged. What's the probability it's actually defective? Most people say about 90%. Count it out for 10,000 crates:

- 2% of 10,000 = **200** are defective; the other **9,800** are good.
- The check flags 90% of the 200 defective crates: **180**.
- It flags 5% of the 9,800 good crates: **490**.
- So **670** crates are flagged, and only 180 of them are defective: 180 ÷ 670 = **26.9%**.

![A tree: 10,000 crates split into 200 defective and 9,800 good; the 200 split into 180 flagged and 20 not flagged; the 9,800 into 490 flagged and 9,310 not flagged; the 180 and 490 flagged crates are grouped as 670 flags, of which 180 (26.9%) are defective](figures/fig21-4-bayes-tree.svg)

*Figure 21.4 — The crate check as a tree of counts. Follow the two branches that end in "flagged": 180 + 490 = 670 flags, and 180 of them are real.*

Now name the parts, with A = "the crate is defective" and B = "the check flags it":

| Name | Symbol | Value | In the tree |
|---|---|---|---|
| **Prior**: how common the cause is before any evidence | P(A) | 0.02 | 200 of 10,000 |
| **Likelihood** (here, the **sensitivity**): how often the evidence appears when the cause is there | P(B \| A) | 0.90 | 180 of 200 |
| **False-positive rate**: how often the evidence appears without the cause | P(B \| not A) | 0.05 | 490 of 9,800 |
| **Evidence**: how common the evidence is overall | P(B) | 0.067 | 670 of 10,000 |
| **Posterior**: the updated probability of the cause, given the evidence | P(A \| B) | 0.269 | 180 of 670 |

The evidence, P(B), needs a fifth rule, because a flag can come from either branch of the tree:

5. **Total probability:** P(B) = P(B | A) × P(A) + P(B | not A) × P(not A). In the tree: 0.90 × 0.02 + 0.05 × 0.98 = 0.018 + 0.049 = 0.067, which is 180 + 490 = 670 flags out of 10,000.

And **Bayes' rule** is the last line of the counting, written with probabilities:

**P(A | B) = P(B | A) × P(A) ÷ P(B)**

In English: *the probability of the cause given the evidence equals the probability of the evidence given the cause, times how common the cause is, divided by how common the evidence is.* In the tree: the top of the fraction, 0.90 × 0.02 = 0.018, is the 180 true flags; the bottom, 0.067, is all 670 flags.

In Python, one line per symbol:

```python
p_defect = 0.02
p_flag_given_defect = 0.90
p_flag_given_good = 0.05

p_flag = p_flag_given_defect * p_defect + p_flag_given_good * (1 - p_defect)
p_defect_given_flag = p_flag_given_defect * p_defect / p_flag

print(f"P(flag)                 = {p_flag:.4f}")
print(f"P(defect | flag)        = {p_defect_given_flag:.4f}  ({p_defect_given_flag*100:.1f}%)")
print(f"P(no defect | flag)     = {1 - p_defect_given_flag:.4f}")
print(f"out of 10,000 crates: {10000*p_defect*p_flag_given_defect:.0f} true flags, "
      f"{10000*(1-p_defect)*p_flag_given_good:.0f} false flags")
```

```
P(flag)                 = 0.0670
P(defect | flag)        = 0.2687  (26.9%)
P(no defect | flag)     = 0.7313
out of 10,000 crates: 180 true flags, 490 false flags
```

- `p_defect` is the prior, P(A); `p_flag_given_defect` is the likelihood, P(B | A); `p_flag_given_good` is the false-positive rate, P(B | not A).
- `p_flag` is rule 5, total probability: the two ways a flag can happen, added.
- `p_defect_given_flag` is Bayes' rule, the posterior.
- The last print turns the probabilities back into counts out of 10,000, the tree's 180 and 490.

**Most flagged crates are fine.** That result surprises nearly everyone, and the counts are the way to explain it to a manager: out of 10,000 crates, 180 defective ones are flagged and 490 good ones are flagged too, so a flag is right only 27% of the time. Nothing is wrong with the test; defects are rare, and 5% of a large number of good crates is bigger than 90% of a small number of bad ones.

The same arithmetic explains why a "95% accurate" fraud model can produce mostly false alarms, why rare-disease screening needs a second test, and why an alert on a rare event needs a much lower false-positive rate than people expect (the alerts in Chapter 20, section 20.8, are exactly this situation).

**What to do with it as an analyst:**

- **Always ask for the base rate.** "How often does this happen anyway?" is the single most useful question in a meeting about a predictive test.
- **Express it as counts**, not probabilities, when explaining. "Out of 10,000: 180 and 490" persuades; "0.269" doesn't.
- **Chain it.** A second, independent check on the flagged crates raises the probability sharply, which is why two-stage screening is standard.

### Two famous puzzles

Two probability puzzles come up in interviews again and again. Both give way to the same method: count the cases.

**The Monty Hall problem.** A car is behind one of three doors, goats behind the other two. You pick door 1. The host, who knows where the car is, opens another door that has a goat, and offers you a switch. Should you switch? List every case:

| Car behind | Host opens | Stay with door 1 | Switch |
|---|---|---|---|
| Door 1 | Door 2 or 3 | Car | Goat |
| Door 2 | Door 3 | Goat | Car |
| Door 3 | Door 2 | Goat | Car |

Each row has probability 1/3. Staying wins in one row, switching in two: **switch, and win 2/3 of the time.** The host's choice isn't random; it carries information.

**The birthday problem.** In a room of 23 people, what's the chance at least two share a birthday (ignoring leap years)? "At least one" is easier through the complement rule: P(at least one shared) = 1 − P(all different). The second person misses the first's birthday with probability 364/365, the third misses both with 363/365, and so on down to 343/365 for the 23rd. Multiply them all (multiplication rule, each step given the ones before):

```python
p_all_different = 1.0
for k in range(23):
    p_all_different = p_all_different * (365 - k) / 365
print(f"P(all 23 birthdays different) = {p_all_different:.4f}")
print(f"P(at least two share one)     = {1 - p_all_different:.4f}")
```

```
P(all 23 birthdays different) = 0.4927
P(at least two share one)     = 0.5073
```

- `range(23)` counts *k* from 0 to 22. Each step multiplies by (365 − *k*)/365: 365/365 for the first person, 364/365 for the second, down to 343/365 for the 23rd.
- The last line is the complement rule.

Just over half. It surprises people because they think of *their own* birthday; the question is about any pair, and 23 people make 253 pairs.

### Checkpoint: the second half

Ten minutes, pencil only. (1) A branch's late rate is 20%. For two independent deliveries, what's the probability both are late? At least one? (2) A check catches 80% of late orders and flags 10% of on-time orders; 20% of orders are late. Out of 1,000 orders, how many are flagged, and what share of the flagged orders are really late? Draw the tree. (Answers at the end of the chapter.)

---

## 21.8 Sampling and the central limit theorem

You almost never measure everything. You measure a **sample** and reason about the **population**. The gap between them is **sampling error**, and it's not a mistake: it's the ordinary variation you get from asking 200 people instead of 200,000.

To see it, treat the 45,040 orders as the population and draw samples from it. One sample first:

```python
population = deliveries["order_value"]
rng = np.random.default_rng(21)
one = rng.choice(population, size=30, replace=False)
print(f"population mean: ₹{population.mean():,.2f} (n = {len(population):,})")
print(f"one sample of 30: ₹{one.mean():,.2f}")
```

```
population mean: ₹24,839.53 (n = 45,040)
one sample of 30: ₹24,526.97
```

- `rng = np.random.default_rng(21)` makes a fresh, seeded generator, as in section 21.5.
- `rng.choice(population, size=30, replace=False)` picks 30 order values at random. `replace=False` means "without putting any back": no order can be picked twice, as in a real sample.
- `len(population)` is the number of rows.

One sample of 30 came within about ₹300 of the true mean. Is that typical, or luck? Draw five more:

```python
for i in range(5):
    sample = rng.choice(population, size=30, replace=False)
    print(f"sample {i + 1}: ₹{sample.mean():,.0f}")
```

```
sample 1: ₹20,158
sample 2: ₹19,981
sample 3: ₹25,761
sample 4: ₹24,403
sample 5: ₹25,529
```

Every sample gives a different mean, from under ₹20,000 to almost ₹26,000. That variation is sampling error. To measure it, repeat 2,000 times for each sample size, and compare the spread of the 2,000 means with a formula (next part of this section):

```python
print(f"population mean: ₹{population.mean():,.2f}")
for n in (30, 200, 1000):
    sample_means = pd.Series([rng.choice(population, size=n, replace=False).mean() for _ in range(2000)])
    print(f"samples of {n:>4}: mean of means ₹{sample_means.mean():,.0f}, "
          f"sd of means ₹{sample_means.std():,.0f} (formula ₹{population.std() / np.sqrt(n):,.0f}), "
          f"90% between ₹{sample_means.quantile(0.05):,.0f} and ₹{sample_means.quantile(0.95):,.0f}")
```

```
population mean: ₹24,839.53
samples of   30: mean of means ₹24,943, sd of means ₹3,250 (formula ₹3,327), 90% between ₹19,926 and ₹30,558
samples of  200: mean of means ₹24,865, sd of means ₹1,267 (formula ₹1,288), 90% between ₹22,812 and ₹26,980
samples of 1000: mean of means ₹24,837, sd of means ₹574 (formula ₹576), 90% between ₹23,899 and ₹25,785
```

How it works:

- `[... for _ in range(2000)]` is a list comprehension (Chapter 17): it draws a sample and takes its mean, 2,000 times, and collects the 2,000 means in a list. `_` is the usual name for a loop counter you don't use.
- `pd.Series(...)` turns the list into a Series, so `.mean()`, `.std()`, and `.quantile()` work on it.
- `sample_means.std()` is the spread of the 2,000 means. The "formula" value is the population's standard deviation divided by √*n*, explained below.
- `.quantile(0.05)` and `.quantile(0.95)` bracket the middle 90% of the sample means.

Three things that output shows, and they're the whole of sampling theory in practice:

1. **Sample means cluster around the true mean.** The average of many sample means is the population mean: the sample mean is an **unbiased** estimate.
2. **Bigger samples are tighter.** The spread of sample means (the **standard error**) shrinks with the square root of *n*: to halve it, you need four times the data. That's why going from 200 to 1,000 helps a lot and from 10,000 to 50,000 rarely does. Simulated and formula values agree within a few percent; the gap is itself sampling noise, and with samples of 1,000 from 45,040 the simulated spread is also slightly smaller because each sample is a noticeable share of the whole.
3. **The distribution of sample means is roughly normal**, even though order values are strongly right-skewed. That's the **central limit theorem**, and it's why normal-based methods work on business data that is nothing like normal.

![Four panels: the skewed distribution of order values, then the distribution of means of samples of 5, 30, and 100, becoming narrower and more symmetric](figures/fig21-5-central-limit.svg)

*Figure 21.5 — The data is skewed; the averages are not. Larger samples give narrower, more bell-shaped distributions of the mean.*

### The standard error

The **standard error** of the mean is the standard deviation of the sample mean:

**SE = *s* ÷ √*n***

In words: the spread of the individual values, divided by the square root of the sample size. For samples of 200 orders:

```python
n = 200
# with 45,040 rows, .std() and np.std() agree to the rupee (section 21.2)
standard_error = population.std() / np.sqrt(n)
print(f"population sd: ₹{population.std():,.2f}")
print(f"standard error of the mean for n = {n}: ₹{standard_error:,.2f}")
print(f"roughly 95% of sample means fall within ±₹{1.96*standard_error:,.0f} of the true mean")
```

```
population sd: ₹18,220.98
standard error of the mean for n = 200: ₹1,288.42
roughly 95% of sample means fall within ±₹2,525 of the true mean
```

- `np.sqrt(n)` is √*n*, so `standard_error` is the formula.
- The comment explains a small choice: this is the population, so strictly σ (divide by *n*) is the right standard deviation, but at this size the two versions differ by less than a rupee.
- `1.96 * standard_error`: in a normal distribution, 95% of values lie within 1.96 standard deviations of the mean (the "about two" of the 68–95–99.7 rule, made exact). Because sample means are roughly normal, 95% of them fall within 1.96 standard errors of the true mean.

The standard error is the bridge to Chapter 22's confidence intervals: a sample of 200 Riverstone orders puts the mean within about ±₹2,500 of the truth, 95% of the time. Quoting a sample mean without that range is how "our average order value rose to ₹25,100" becomes a decision it can't support.

### Sampling in practice

- **Random means random.** "The first 200 rows" is not a sample; it's the oldest 200 orders, or one branch's file. Use `df.sample(n=200, random_state=42)`.
- **Stratify when groups differ.** If Kolkata is about one order in eight (12.5%) and you need branch-level answers, sample within each branch rather than hoping.
- **Beware survivorship and self-selection.** A satisfaction survey answered by 3% of customers measures the 3% who answer surveys.
- **Record the seed and the date.** A sample you can't reproduce is a number nobody can check.

---

## 21.9 Putting it together: profiling a measure

A repeatable routine for describing any numeric column, which is the project in miniature. First the function, and one run of it:

```python
def profile(series, name):
    """Describe a numeric column the way a report should: centre, spread, shape, extremes."""
    s = series.dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    return {
        "measure": name, "n": len(s),
        "mean": round(s.mean(), 2), "median": round(s.median(), 2),
        "sd": round(s.std(), 2), "iqr": round(q3 - q1, 2),
        "p90": round(s.quantile(0.90), 2), "p99": round(s.quantile(0.99), 2),
        "min": round(s.min(), 2), "max": round(s.max(), 2),
        "skew": round(s.skew(), 2),
        "cv": round(s.std() / s.mean(), 2),
    }

print(pd.Series(profile(deliveries["delivery_days"], "delivery days")))
```

```
measure    delivery days
n                  45040
mean                4.37
median               3.8
sd                  2.28
iqr                  2.1
p90                  6.8
p99                 13.1
min                  1.0
max                 37.9
skew                3.13
cv                  0.52
dtype: object
```

- `def profile(series, name):` defines a function (Chapter 17) that takes a column and a label. The text in triple quotes is its docstring, saying what it does.
- `series.dropna()` drops blank values first, so every measure uses the same rows.
- The function **returns a dictionary**: one key per statistic, each value rounded to two decimals with `round(value, 2)`. Every measure in it is one you've met in this chapter.
- `pd.Series(...)` turns the dictionary into a Series (Chapter 18), so it prints one statistic per line. `dtype: object` at the end means the Series holds a mix of text and numbers.

Now profile three columns and set the results side by side:

```python
profiles = pd.DataFrame([profile(deliveries["order_value"], "order value (₹)"),
                         profile(deliveries["delivery_days"], "delivery days"),
                         profile(deliveries.loc[deliveries["branch"] == "Kolkata", "delivery_days"],
                                 "Kolkata days")])
print(profiles.set_index("measure").T.to_string())
```

```
measure  order value (₹)  delivery days  Kolkata days
n               45040.00       45040.00       5626.00
mean            24839.53           4.37          6.33
median          20700.00           3.80          5.70
sd              18220.98           2.28          3.11
iqr             23135.25           2.10          3.50
p90             49800.00           6.80         10.20
p99             82790.08          13.10         17.55
min               546.25           1.00          1.00
max            143175.00          37.90         29.20
skew                1.27           3.13          1.70
cv                  0.73           0.52          0.49
```

- `pd.DataFrame([dict, dict, dict])` turns a list of dictionaries into a table: one row per dictionary, one column per key.
- `.set_index("measure")` uses the measure names as row labels instead of 0, 1, 2.
- `.T` **transposes** the table, swapping rows and columns, so each statistic is a row and each measure a column. Twelve statistics fit down a page far better than across it.
- `.to_string()` prints every row in full. The counts in the `n` row show two decimals because, once flipped, each column holds one type of value, and a column of decimals shows its whole numbers as decimals too.

Then say it in sentences, because a table is not a finding:

> *Riverstone delivered 45,040 orders in 2025. A typical order was ₹20,700 (median), though the mean of ₹24,840 is higher because a minority of large orders pull it up; 10% of orders exceeded ₹49,800. Delivery took a median of 3.8 days and a mean of 4.4, with a long tail: 5% of orders took more than 8.2 days, and the slowest took 38. Kolkata is the outlier branch, with a median of 5.7 days, an interquartile range 2.5 times Mumbai's, and only 68% of orders inside its 7-day promise.*

That paragraph is what statistics is for: a handful of numbers, chosen deliberately, that let someone act.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Reporting the mean of skewed data alone | "Typical" order value nobody recognizes | Median alongside, and a histogram |
| Averaging averages | The company figure doesn't match the branches | Weight by count, or compute from raw rows |
| Quoting a centre with no spread | A promise that's broken half the time | Add IQR or a percentile |
| Using standard deviation on skewed data | "Mean ± sd" goes below zero | IQR and percentiles |
| Confusing sample and population sd | Small differences in small samples | `ddof=1` unless you have everything |
| Treating percentiles as interchangeable | Two tools, two answers | State the method (`PERCENTILE.INC`, `PERCENTILE_CONT`) |
| Deleting outliers to "clean" the data | The biggest customers vanish | Investigate; Chapter 14 decides, not the rule |
| Assuming normality | z-scores flag the wrong rows | Check skew; use distribution-free rules |
| Poisson for clustered events | Far more extreme weeks than predicted | Check whether variance ≈ mean |
| Confusing P(A\|B) with P(B\|A) (the confusion of the inverse) | "A third of late orders are Kolkata's" when the data says a fifth | Write both, with counts |
| Ignoring the base rate (the base rate fallacy) | A "95% accurate" test that's mostly false alarms | Bayes, expressed as counts out of 10,000 |
| Treating sampling error as error | Panic at a 2% move in a survey | Standard error, and Chapter 22's intervals |
| Non-random samples | "The first 200 rows" | `sample(random_state=…)`, stratify if needed |
| Reporting more precision than the data supports | ₹24,839.53 from a sample of 30 | Round to what the standard error justifies |

---

## In the real world: one promise, four branches

Riverstone's sales team wanted a single delivery promise for the website: *"Delivered in 5 days."* The operations head objected on the grounds that Kolkata could not do it. The meeting went round twice on averages: sales quoting a company mean of 4.4 days, operations quoting the days they remembered.

Meera profiled it instead, and brought three numbers per branch: the median, the 95th percentile, and the share inside the current promise.

| Branch | Median | 95th percentile | Current promise | Inside it |
|---|---:|---:|---:|---:|
| Mumbai HO | 3.2 days | 5.7 days | 5 days | 90.8% |
| Bengaluru | 3.8 days | 6.9 days | 5 days | 78.0% |
| Delhi | 4.4 days | 8.4 days | 6 days | 80.0% |
| Kolkata | 5.7 days | 12.0 days | 7 days | 68.1% |

Three things became obvious in about a minute:

1. **A single five-day promise would be kept for Mumbai and broken for everyone else.** The company average was never the relevant number; the branch distributions were.
2. **The right unit for a promise is a percentile, not an average.** "95% of orders within X days" is checkable; "average 4.4 days" tells a customer nothing about their order.
3. **Kolkata's problem was variability more than speed.** Its median was 2.5 days behind Mumbai's, but its interquartile range was 2.5 times as wide, and its 95th percentile was more than twice Mumbai's. Fixing the average would mean nothing; narrowing the spread would mean everything.

The team settled on branch-level promises at the 90th percentile, rounded up, and a monthly report of the share inside promise rather than the average. Operations opened an investigation into the Kolkata tail, which turned out to be dominated by consignments routed through a single transporter during the festive weeks.

Six months later the tail had shortened and the promise held at 92% company-wide. The statistics didn't fix anything; they changed what the meeting was about, from whose memory was right to which part of the distribution needed work.

---

## Project: profile Riverstone's order values and delivery times

**Goal:** a one-page statistical profile that changes what a meeting argues about.

### Tools you'll need

- **Python 3.13 or 3.14** (Chapter 17) with `pandas`, `numpy`, `scipy` (section 21.5), and `matplotlib`. The outputs in this chapter were checked on Python 3.11, pandas 3.0.6, numpy 2.4.6, scipy 1.17.1, and matplotlib 3.10.8.
- **Spreadsheet equivalents** (Excel or Google Sheets): `AVERAGE`, `MEDIAN`, `MODE.SNGL`, `STDEV.S`/`STDEV.P`, `VAR.S`, `QUARTILE.INC`, `PERCENTILE.INC`/`.EXC`, `SKEW`, `KURT`, `NORM.DIST`, `NORM.INV`, `BINOM.DIST`, `POISSON.DIST`, `RAND`, and `RANDBETWEEN`. Excel's Analysis ToolPak adds Descriptive Statistics and Random Number Generation in one dialog.
- **SQL (PostgreSQL):** `AVG`, `STDDEV_SAMP`, `STDDEV_POP`, `PERCENTILE_CONT`, and `PERCENTILE_DISC` (section 21.3; `PERCENTILE_CONT` first appeared in Chapter 15).
- **Companion files (`companion/ch21/`):** `delivery_times_2025.csv` (45,040 delivered 2025 orders; its eight columns are listed in section 21.1) and a README describing how the delivery times were simulated. The delivery times are invented because Riverstone's ERP data has no delivery dates; everything else comes from the full dataset. The folder also holds the script that built the file; you never need to run it.

**Option A: your own data.** Any measure you report regularly: ticket resolution time, days sales outstanding, machine downtime, basket size.

**Option B: Riverstone.** Use `delivery_times_2025.csv` and the full dataset.

**Steps**

1. **Profile both measures** with the `profile()` function from section 21.9: n, mean, median, sd, IQR, p90, p99, min, max, skew, CV.
2. **Draw the distributions:** a histogram with sensible bins (Chapter 15) and a box plot per branch, with the promise marked.
3. **Describe the shape in words.** Is it skewed? How heavy is the tail? What does the gap between mean and median mean for anyone setting a target?
4. **Quantify the tail:** what share of orders exceed the promise, and how much revenue sits behind them?
5. **Set a defensible promise:** for each branch, the 90th percentile rounded up, and the share of orders that would meet it. Compare with the current promise.
6. **Probability questions:** given a day with 40 deliveries at each branch's late rate, what's the chance of more than 10 late? (Binomial.) If complaints average 9.4 a week, how often would you see 15 or more? (Poisson.)
7. **A Bayes question:** the branch flags orders it expects to be late, catching 80% of truly late orders and flagging 10% of on-time ones. If an order is flagged, what's the probability it's actually late? Express it as counts out of 10,000.
8. **Sampling:** take random samples of 30, 200, and 1,000 orders; report the sample mean and its standard error, and state how far a sample of 200 can be from the truth.
9. **Write the page:** six to eight sentences, three numbers per branch, one chart, and one recommendation.

**What good looks like:** the profile matches section 21.9 (order values: median ₹20,700, mean ₹24,840, skew 1.27; delivery days: median 3.8, mean 4.37, p95 8.2, skew 3.13), the branch table matches the story, and the recommendation is stated as a percentile promise rather than an average.

**Stretch goals**

- Split delivery times by month and test whether the festive season (October and November) is slower, and by how much.
- Fit a lognormal distribution to delivery days and compare its 95th percentile with the empirical one.
- Work out the sample size needed to estimate the mean order value within ±₹500 with 95% confidence (Chapter 22 gives the formula; the standard error in section 21.8 gives you enough to try).
- Repeat the whole profile for order values by segment, and say which segment's promise would be hardest to keep.

---

## Timed challenge: forty minutes

Use `delivery_times_2025.csv`. Answers at the end of the chapter.

- **Level 1:** Mean, median, and mode of order value; mean and median of delivery days.
- **Level 2:** Standard deviation and IQR of delivery days, company-wide.
- **Level 3:** The 90th and 99th percentiles of delivery days, and the slowest single delivery.
- **Level 4:** Median, IQR, and 95th percentile of delivery days for each branch.
- **Level 5:** The share of orders inside the promise, company-wide and per branch.
- **Level 6:** Using the IQR rule, how many orders are outliers on delivery days, and what share is that?
- **Level 7:** P(late), P(late | Kolkata), and P(Kolkata | late).
- **Bonus:** Take 2,000 random samples of 200 orders; report the standard deviation of the sample means, and compare it with the standard error formula.

---

## Recap

- **By hand first:** x̄ = Σxᵢ ÷ *n*; *s*² = Σ(xᵢ − x̄)² ÷ (*n* − 1) and *s* = √*s*²; IQR = Q3 − Q1. The spreadsheet (`AVERAGE`, `VAR.S`, `STDEV.S`, `QUARTILE.INC`) and pandas (`.mean()`, `.var()`, `.std()`, `.quantile()`) give the same answers.
- **Centre:** mean uses everything and is dragged by extremes; median is the middle and isn't; mode is for categories. On Riverstone's orders the mean is ₹24,840 and the median ₹20,700, and the gap is the story.
- **Spread:** range is fragile, variance is in squared units, standard deviation is the default for symmetric data, IQR is the honest choice for skewed data. Averages hide spread: Kolkata's middle half is 2.5 times as wide as Mumbai HO's.
- **Percentiles** describe what customers actually get, which is why service levels use them: 95% of Riverstone's orders arrive within 8.2 days.
- **Shape:** positive skew is the norm for money and durations. Compare mean with median as a quick test. Outlier rules (IQR, z-score) produce candidates, not verdicts.
- **Distributions:** normal for many small influences, binomial for counts of yes/no trials, Poisson for event counts at a steady rate, uniform for equal likelihood. scipy's `pmf`, `cdf`, and `ppf` answer "exactly", "or less", and "which value".
- **Probability rules:** complement, addition (subtract the overlap), multiplication (with conditioning), conditional probability, and total probability. P(A | B) ≠ P(B | A).
- **Bayes' rule** updates a prior with evidence, and the base rate usually dominates: with a 2% defect rate and a 5% false-positive rate, most flagged crates are fine. Draw the tree of counts.
- **Sampling:** sample means are unbiased, their spread is the standard error, SE = *s* ÷ √*n*, and the central limit theorem makes them roughly normal even when the data is not.
- **A profile** is n, mean, median, sd, IQR, p90, p99, min, max, skew, CV — and then two or three sentences that tell someone what to do.

---

## Key terms

descriptive statistics · sample · population · Σ (sum) · x̄ (sample mean) · μ (population mean) · mean · median · mode · weighted average · average of averages · spread · range · deviation · variance · standard deviation · *s* and σ · sample versus population (ddof) · interquartile range · quartile · percentile · interpolation method · service level · coefficient of variation · skew · kurtosis · excess kurtosis · tail · outlier · IQR rule · z-score · distribution · probability mass function (pmf) · probability density function (pdf) · cumulative distribution function (cdf) · percent point function (ppf) · normal distribution · 68–95–99.7 rule · binomial distribution · n choose k · Poisson distribution · rate (λ) · factorial · uniform distribution · random number generator · seed · expected value · probability · complement rule · addition rule · mutually exclusive · multiplication rule · conditional probability · independence · total probability · base rate · confusion of the inverse · base rate fallacy · Bayes' rule · prior · likelihood · posterior · sensitivity · false-positive rate · random sample · stratified sample · sampling error · unbiased estimate · standard error · central limit theorem · lambda (Python)

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can work out a mean, median, variance, standard deviation, and IQR by hand for a short list, and read x̄, Σ, *s*, and σ.
- [ ] You choose between mean, median, and mode for a reason you can state.
- [ ] You never quote a centre without a spread.
- [ ] You use IQR and percentiles on skewed data, and standard deviation where it's meaningful.
- [ ] You can explain why the mean sits above the median in most money data.
- [ ] You write service levels as percentiles.
- [ ] You can name the distribution a measure is likely to follow and what that implies.
- [ ] You know which of `pmf`, `cdf`, and `ppf` answers a question, and can compute a binomial or Poisson probability to set a sensible threshold.
- [ ] You never confuse P(A | B) with P(B | A), and you ask for the base rate.
- [ ] You can explain a Bayes result as counts out of 10,000, with a tree.
- [ ] You know that sample means cluster normally around the truth, that the spread shrinks with the square root of n, and roughly how far a sample of 200 can be off.
- [ ] You profile a new measure the same way every time, and turn the table into sentences.

---

## Exercises

Use `companion/ch21/delivery_times_2025.csv` and the full dataset.

### Warm-up

1. For each, say whether you'd report the mean, the median, or the mode, and why: order value; delivery days; the most common product in an order; total revenue per month; salary in a small team including the owner.
2. A branch's four monthly averages are 3.1, 3.4, 3.0, and 6.2 days. What's suspicious about reporting 3.9 as the year's average?
3. Explain variance and standard deviation to a sales manager in two sentences, without the word "squared" in the second one.
4. Riverstone's mean order value is ₹24,840 and the median ₹20,700. What does that tell you about the shape, and what would it look like if the two were equal?
5. Why is "average delivery 4.4 days" a bad promise, and what would you write instead?
6. What's the difference between P(late | Kolkata) and P(Kolkata | late)? Give a sentence for each using the real numbers.

### Core

7. Compute the mean, median, mode, standard deviation, and IQR of order value. Which two would you put in a management pack, and why?
8. Compute the same statistics for delivery days per branch, and rank the branches by median and by IQR. Does the ranking change?
9. What is the 90th percentile of delivery days for each branch? If each promise were set there and rounded up, what would the promises be?
10. What share of orders would meet those new promises? Compare with the current 81.8%.
11. Using the IQR rule on delivery days, how many outliers are there, and which branch has the most as a share of its orders?
12. Compute the skew of order value and of delivery days. Which is more skewed, and what does that imply for reporting an average?
13. What share of 2025 revenue sits in orders that were delivered late?
14. With 40 deliveries in a day and Kolkata's late rate, what's the probability that more than 15 are late? (Binomial.)
15. If complaints average 9.4 a week, what's the probability of a week with 15 or more? Of a week with none?
16. A crate's weight is normal with mean 500 g and standard deviation 4 g. What share falls outside 492–508 g? What limit would only 1 in 1,000 crates fall below?
17. Compute P(late), P(late | festive months), and P(festive | late) using October and November as the festive season. Are lateness and season independent?
18. The branch flags orders it expects to be late: it catches 80% of late orders and flags 10% of on-time ones. Given the real late rate, what's P(late | flagged)? Express it as counts out of 10,000.
19. Take 2,000 samples of 200 orders and plot the distribution of the sample means. What is its standard deviation, and how close is it to the standard-error formula?
20. How large a sample would you need for the standard error of the mean order value to be under ₹500?
21. Write the `profile()` function from section 21.9 and run it on order value, delivery days, and delivery days for each branch. Present it as a table a manager could read.
22. Turn that table into four sentences with a recommendation.

### Stretch

23. Split delivery days by month. How much slower are October and November than the rest of the year, at the median and at the 95th percentile?
24. Fit a lognormal distribution to delivery days (`scipy.stats.lognorm.fit`) and compare its 90th and 99th percentiles with the empirical ones. Where does the fit fail?
25. Simulate a day of 40 deliveries 10,000 times using each branch's late rate, and report how often more than a quarter are late. Compare with the binomial answer.
26. Using the delivery data, estimate the probability that a customer's next two orders are both late, first assuming independence and then conditioning on branch. Which is bigger, and why does that matter for a customer-experience metric?

### Think about it

27. A manager says "our average delivery time improved from 4.6 to 4.4 days this month; the process is working". What three questions do you ask?
28. When is it legitimate to remove an outlier from a reported statistic, and what must you disclose?
29. A dashboard shows a 95% "on-time" figure; a customer survey says a third of customers experienced a late delivery in the last year. Can both be true?

---

## Answers

**1.** Order value: **median** (skewed), with the mean if totals matter. Delivery days: **median** plus a percentile. Most common product: **mode**. Total revenue per month: neither — it's a total, and you'd compare it with last year. Small team's salary including the owner: **median**, because one salary dominates the mean.

**2.** 3.9 is the average of four monthly averages, so it ignores how many orders each month had, and it hides that one month (6.2) was very different. Report the median with the range, or compute from the orders, and show the monthly series.

**3.** "Variance measures how far orders sit from the average, on average. The standard deviation puts that back into days, so you can say most orders land within about so many days either side."

**4.** A long right tail: a minority of large orders. If they were equal, the distribution would be roughly symmetric, and the mean would describe a typical order.

**5.** Because half the orders are slower than the mean, and a fifth are much slower. Write **"90% of orders arrive within X days"**, per branch.

**6.** P(late | Kolkata) = **31.9%**: about a third of Kolkata's orders arrive late. P(Kolkata | late) = **21.8%**: about a fifth of the company's late orders come from Kolkata. The first is about Kolkata's process; the second is about where the lateness sits.

**7.** Mean ₹24,839.53, median ₹20,700.00, mode ₹1,725.00 and ₹5,800.00 (tied at 219 orders each), sd ₹18,220.98, IQR ₹23,135.25. Put the **median** (typical order) and the **mean** (consistent with revenue) in the pack, and note the skew.

**8.** By median: Mumbai HO 3.2, Bengaluru 3.8, Delhi 4.4, Kolkata 5.7. By IQR: Mumbai HO 1.4, Bengaluru 1.9, Delhi 2.2, Kolkata 3.5. The ranking is the same here, which is itself worth saying: Kolkata is both slower and less predictable.

**9.** Branch 90th percentiles are 5.0 (Mumbai HO), 6.0 (Bengaluru), 7.2 (Delhi) and 10.2 (Kolkata) days, so rounded-up promises would be 5, 6, 8, and 11 days.

**10.** Mumbai HO's promise stays at 5 days, so its share stays 90.8%. Bengaluru moves from 5 to 6 days (90.4% kept), Delhi from 6 to 8 (93.9%), and Kolkata from 7 to 11 (92.9%). Company-wide, 91.7% of orders would meet the new promises, against 81.8% today. The honest framing: the promise gets longer for three branches, and the share kept rises to a consistent 90% or more.

**11.** 2,220 orders (4.9%) are above the company-wide fence of 8.25 days. By branch: Kolkata 1,130 (20.1% of its orders), Delhi 599 (5.5%), Bengaluru 258 (2.1%), and Mumbai HO 233 (1.5%). Kolkata has the most, both in number and as a share, which is what the fat tail in Figure 21.2 shows. (A fence set per branch would flag fewer Kolkata orders, because Kolkata's own IQR is wider.)

**12.** Delivery days (skew 3.13) is far more skewed than order value (1.27). The more skewed the measure, the more misleading a bare average is, and the more important percentiles become.

**13.** Compute `deliveries.loc[~deliveries["on_time"], "order_value"].sum() / deliveries["order_value"].sum()`: **19.9%** of delivered revenue arrived late, which is the number that makes the operations case in money rather than percentages.

**14.** With n = 40 and p = 0.319, `1 - stats.binom.cdf(15, 40, 0.319)` ≈ **0.18**: nearly one day in five. An alert set at "more than 15 late" would fire about once a week in Kolkata, which is too often to be useful.

**15.** P(15 or more) ≈ 0.0559; P(none) ≈ 0.00008. A complaint-free week would be a real surprise.

**16.** Outside 492–508 g is ±2 sd, so about **4.6%**. The 1-in-1,000 lower limit is `stats.norm.ppf(0.001, 500, 4)` ≈ **487.6 g**.

**17.** P(late) = **18.2%**. P(late | festive) = **33.6%**, against 14.0% in the other ten months. P(festive | late) = **39.7%**, although October and November hold only 21.6% of orders. Lateness and season are not independent: P(late | festive) is far above P(late). That's exactly why a company-wide annual late rate is a poor baseline for a festive-season alert.

**18.** With a late rate of 18.2%: out of 10,000 orders, 1,820 are late and 8,180 are not; the flag catches 1,456 late ones and 818 on-time ones, so P(late | flagged) = 1,456 ÷ 2,274 ≈ **64%**. Better than the 27% in the crate example, because lateness is far more common than defects: the base rate does the work.

**19.** The standard deviation of the 2,000 sample means comes out around **₹1,260–1,300** depending on the seed (₹1,267 in section 21.8), and the formula `population sd / √200` gives ₹1,288. They agree, which is the central limit theorem doing its job.

**20.** SE = *s* ÷ √*n* < 500 means √*n* > *s* ÷ 500, so *n* > (18,221 ÷ 500)² ≈ **1,329** orders. Note this is a standard error under ₹500. For a 95% interval of ±₹500 (the stretch goal in the project), the half-width is 1.96 × SE, so *n* ≥ (1.96 × 18,221 ÷ 500)² ≈ **5,102** orders.

**21.** See section 21.9. Present it with the measure in the first column and round sensibly: nobody needs `order_value` to the paisa in a management pack.

**22.** For example: *"A typical order is ₹20,700, but the mean of ₹24,840 shows a minority of large orders. Delivery takes a median of 3.8 days, with 5% of orders beyond 8.2. Kolkata is the exception on both speed and consistency: median 5.7 days and an interquartile range 2.5 times Mumbai's. Recommendation: set branch-level promises at the 90th percentile and report the share inside promise, not the average."*

**23.** October and November: median **4.7 days** and 95th percentile **9.2 days**. The other ten months: median **3.6** and 95th percentile **7.8**. So the festive months are 1.1 days slower at the median and 1.4 days slower at the 95th percentile: slower at every point of the distribution, and most in the tail. Report both, because the tail is what customers complain about.

**24.** A lognormal fits the body of the delivery-time distribution well and typically understates the extreme tail, because the real data includes a small share of badly broken deliveries that aren't part of the same process. That mismatch is a finding: two processes, not one.

**25.** The simulation and the binomial agree closely, which is the point of the exercise: the binomial *is* the model of that simulation. Simulation earns its place when the situation is too complicated for a formula.

**26.** Assuming independence, P(both late) = P(late)² = 0.1824² ≈ **3.3%**. Conditioning on branch, a Kolkata customer's two orders are each late 31.9% of the time, so ≈ 0.319² = **10.1%** for a Kolkata customer. Across all customers, conditioning on branch gives **3.9%** (each branch's late rate squared, weighted by its share of orders) against 3.3% under independence. The conditional version is larger and more honest: lateness clusters by customer because customers belong to branches, and a customer-experience metric built on the independent assumption will understate how many customers see repeated failures.

**27.** (1) How much does delivery time vary month to month anyway — is 0.2 days inside the normal range? (2) Did the mix change: more Mumbai orders and fewer Kolkata ones would improve the average with no process change. (3) What happened at the 90th percentile, where customers feel it? A median and a percentile per branch answer all three.

**28.** When the value is a known error (Chapter 14), when it comes from a different process that you state clearly ("excluding the two consignments lost in transit"), or when a rule agreed in advance excludes it. You must disclose the rule, the count removed, and the effect on the number, and you should show the figure both ways.

**29.** Yes. A 95% on-time rate measures **orders**; the survey measures **customers**, and a customer who places twenty orders a year has a much higher chance of seeing at least one late delivery: 1 − 0.95²⁰ ≈ 64%. Per-order and per-customer metrics answer different questions, and the customer's experience is usually the one that drives complaints.

**Checkpoint, first half (section 21.4).** The nine values add up to 36, so the mean is 36 ÷ 9 = **4**; the median is the 5th value, **4**. Deviations: −3, −2, −2, −1, 0, 0, 1, 2, 5; squared: 9, 4, 4, 1, 0, 0, 1, 4, 25, total 48. Sample variance 48 ÷ 8 = **6**, so *s* = √6 ≈ **2.45** days. Lower half 1, 2, 2, 3, 4: **Q1 = 2**. Upper half 4, 4, 5, 6, 9: **Q3 = 5**. **IQR = 3** days. `QUARTILE.INC` and pandas give the same quartiles.

**Checkpoint, second half (section 21.7).** (1) Both late: 0.2 × 0.2 = **0.04**. At least one: 1 − P(neither) = 1 − 0.8 × 0.8 = **0.36**. (2) Out of 1,000 orders, 200 are late and 800 on time. The check flags 80% of 200 = 160 late orders and 10% of 800 = 80 on-time ones: **240 flags**, of which 160 ÷ 240 = **2 in 3 (66.7%)** are really late.

**Timed challenge answers.** Level 1: order value mean ₹24,839.53, median ₹20,700.00, mode ₹1,725.00 and ₹5,800.00 (tied); delivery days mean 4.37, median 3.8. Level 2: sd 2.28 days, IQR 2.10 days (Q1 3.0, Q3 5.1). Level 3: p90 6.8 days, p99 13.1 days, slowest 37.9 days. Level 4: medians 3.2 / 3.8 / 4.4 / 5.7 and IQRs 1.4 / 1.9 / 2.2 / 3.5 for Mumbai HO, Bengaluru, Delhi, Kolkata; p95s 5.7 / 6.9 / 8.4 / 12.0. Level 5: 81.8% company-wide; Mumbai HO 90.8%, Delhi 80.0%, Bengaluru 78.0%, Kolkata 68.1%. Level 6: 2,220 orders, 4.9%. Level 7: P(late) 18.2%, P(late | Kolkata) 31.9%, P(Kolkata | late) 21.8%. Bonus: around ₹1,260–1,300 depending on the seed, against a formula value of ₹1,288.

---

## Where this leads

- **Chapter 22, Statistics Without Fooling Yourself:** confidence intervals, hypothesis tests, p-values, A/B tests, and the traps around all of them.
- **Chapter 15** already used these ideas visually: histograms, box plots, and the quartiles behind them.
- **Chapter 20:** thresholds and alerts that are set from a distribution rather than a round number.
- **Chapter 40, Time Series & Forecasting:** trend, seasonality, and prediction intervals, which are standard errors in a different coat.
- **Part 4:** every model assumes distributions, sampling, and the difference between training data and the world.
- **Interview preparation:** the Statistics, Probability & Experimentation Bank (Chapter 73) covers exactly this ground, including Bayes and the central limit theorem.
