# Chapter 73. Statistics, Probability & Experimentation Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer probability puzzles that show up across every data role's interviews, and explain *why* the surprising answer is correct, not just what it is · reason correctly about distributions, p-values, and confidence intervals, including the ways almost everyone misinterprets them at first · design an A/B test's sample size before running it, and debug one that's already gone wrong · spot Simpson's paradox and correlation-masquerading-as-causation in real-looking data.
>
> **Before you start:** Chapter 69 (the three answer tiers and the twelve extra-point moves). The questions test Chapter 21 (probability and distributions), Chapter 22 (confidence intervals, tests, A/B basics, confounders, Simpson's paradox, and regression basics in section 22.10), Chapter 30 (inference, power, experiment design, the sample-ratio check) and Chapter 31 (causal inference without experiments). This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** about 9–12 hours for a first pass, running every cell and saying each answer aloud (the simulations take time to run and to understand); 1 hour for the final-week list. Section 73.8 adds about an hour and is best done in one sitting.
>
> **How this chapter is built.** Same format as every question bank in Part 8: every core question gives a memory hook ("Remember it as…"), a one-line answer, and a tier table: what **passes**, what's **strong**, and the **extra points** (Chapter 69's moves, one per line, tagged the same way: **[+Validate]**, **[+Business]** and so on). Then come the likely follow-ups, the red flag, and where to learn it. Rapid-fire sections are scan tables. **Every number in this chapter comes from running the code shown** (NumPy, SciPy, statsmodels): simulations, test statistics, p-values, sample sizes. The order: probability warm-ups first, then the famous puzzles (they test the same basics from an angle), then distributions, testing, experiment design and debugging, causal reasoning, and two walk-throughs that put it all together. Section 73.8 closes the chapter with a different kind of question: not whether you understand the statistics, but whether the number you reported is the number you think you computed — the defaults, weightings and measures that change an answer without raising anything.
>
> **Learn it in** pointers name the chapter and section that teach each idea: Chapter 21 (probability and distributions), Chapter 22 (tests, A/B basics, confounders, Simpson's paradox), Chapter 30 (inference, power, experiment design, the sample-ratio check) and Chapter 31 (causal inference without experiments). The few ideas marked **Beyond the book** go further than those chapters and carry their own short explanation, so you can learn them here.

---

## 73.0 The setup cell, and how to use this bank

**Levels and roles.** Each question carries a level and the roles that usually ask it:

- **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds.
- **DA** data analyst · **DS** data scientist · **PA** product analyst (the role that runs A/B tests most) · **BA** business analyst.

Within each section the core questions run from easier to harder. If you're preparing for a first analyst job, do every Fresher question first, then come back for the Mid ones.

**The setup cell.** Open a new notebook in your Chapter 17 environment and run this cell first. Every later cell in the chapter assumes it ran, and the cells run in order, like a notebook:

```python
import numpy as np
from scipy import stats
import statsmodels.stats.api as sms

rng = np.random.default_rng(73)
```

This cell prints nothing; if it runs without an error, you're ready.

- `import numpy as np` loads NumPy (Chapter 18, section 18.1) for arrays and random numbers.
- `from scipy import stats` loads SciPy's statistics module: the distributions, `ttest_ind`, `chisquare`, `chi2_contingency` and `pearsonr`. You installed SciPy in Chapter 21, section 21.5.
- `import statsmodels.stats.api as sms` loads statsmodels' collection of tests and power tools under the short name `sms`: the proportion tests (`proportions_ztest`, `confint_proportions_2indep`) and the power calculators (`proportion_effectsize`, `NormalIndPower`) used in Q73-020 and Q73-036. You installed statsmodels in Chapter 22, section 22.2.
- `rng = np.random.default_rng(73)` makes a random number generator with seed 73 (Chapter 21, section 21.5), so your "random" numbers match the ones printed here. Each simulation cell below starts the generator again with the same seed, so it prints the same answer even if you run it on its own.

---

## 73.1 Core probability concepts

### Warm-ups, 73.1

Roles: DA, DS, PA and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q73-001 | Independent vs. mutually exclusive events? | Independent: one doesn't affect the other's probability / mutually exclusive: they can't both happen | **[+Edge cases]** two mutually exclusive events with nonzero probability are automatically *not* independent: one happening tells you the other definitely didn't | Fresher · 21.6 |
| Q73-002 | What's the difference between P(A and B) and P(A or B)? | `P(A)×P(B)` if independent / `P(A)+P(B)-P(A and B)` always | **[+Edge cases]** forgetting to subtract the overlap in "or" is the single most common probability arithmetic mistake | Fresher · 21.6 |
| Q73-003 | What's a conditional probability, in one sentence? | The probability of A, given that B is already known to be true: `P(A\|B)` | **[+Business]** almost every real business probability question is secretly conditional ("what's the chance this customer churns" really means "given what we know about them") | Fresher · 21.6 |
| Q73-004 | Expected value of a fair six-sided die roll? | `(1+2+3+4+5+6)/6 = 3.5`: a value the die itself can never actually show | **[+Edge cases]** expected value doesn't have to be a possible outcome; it's a long-run average, not a prediction for one roll | Fresher · 21.5 |

### Q73-005 · Explain Bayes' theorem, and why a "99% sensitive" test can still be wrong most of the time

**Level:** Mid · **Roles:** DA, DS, PA

**Remember it as:** *A rare disease and an imperfect test: even a good test is mostly wrong about rare things, because there are so many more healthy people to false-positive on than sick people to correctly catch.*

**Answer in one line:** Bayes' theorem updates a prior probability using new evidence: `P(A|B) = P(B|A) × P(A) / P(B)`, and it matters most when the thing you're testing for is rare, because the base rate can overwhelm even a very good test.

**By hand first, with 1,000 people.** A disease with 1% prevalence, a test that catches 99% of cases (its **sensitivity**) and wrongly flags 5% of healthy people (its **false-positive rate**). Out of 1,000 people, 10 are sick and 990 are healthy:

| | Test positive | Test negative | Total |
|---|---:|---:|---:|
| **Sick** | 9.9 | 0.1 | 10 |
| **Healthy** | 49.5 | 940.5 | 990 |
| **Total** | 59.4 | 940.6 | 1,000 |

Of the 59.4 people who test positive, only 9.9 are sick: 9.9 ÷ 59.4 = 16.7%. Counting people like this (**natural frequencies**) is the easiest way to explain the answer aloud. The same in Python:

```python
p_disease = 0.01                 # prevalence: the base rate
p_pos_given_disease = 0.99       # sensitivity
p_pos_given_no_disease = 0.05    # false-positive rate

p_positive = p_pos_given_disease * p_disease + p_pos_given_no_disease * (1 - p_disease)
p_disease_given_positive = (p_pos_given_disease * p_disease) / p_positive
print(f"P(positive) = {p_positive:.4f}")
print(f"P(disease | positive) = {p_disease_given_positive:.4f}")
```

```
P(positive) = 0.0594
P(disease | positive) = 0.1667
```

- `p_positive` is the **Total** row of the table as a share: the sick who test positive plus the healthy who test positive (total probability, Chapter 21, section 21.7).
- `p_disease_given_positive` is Bayes' rule: the sick positives divided by all positives.

Someone testing positive on a test that catches 99% of cases and wrongly flags 5% of healthy people has the disease only **16.7%** of the time.

| Tier | What to say |
|---|---|
| Passes | States the formula correctly, can't apply it to a concrete number |
| Strong | Works through the disease example above, arriving at 16.7%, and explains *why* it's so much lower than 99%: the 5% false-positive rate applies to the 99% of people who are healthy, a much bigger group than the 1% who are sick |
| Extra points | **[+Validate]** the 1,000-person table and the computed numbers agree<br>**[+Edge cases]** calling this test "99% accurate" is itself the loose word: its accuracy (the share of everyone it gets right) is 0.99 × 0.01 + 0.95 × 0.99 = 95.0%, and neither number is the chance that a positive is sick<br>**[+Business]** this is why a fraud or churn model's headline accuracy needs the base rate before it means anything: it's precision (Chapter 39, section 39.1), traced back to its probability root |

**Likely follow-ups:** How would a higher-prevalence disease change the answer? What test characteristic matters more for a rare event, sensitivity or specificity?
**Red flag:** treating sensitivity as P(disease | positive): "it's 99% sensitive, so a positive means 99% likely".
**Learn it in:** Chapter 21, section 21.7 (Bayes' rule, "A worked Riverstone example").

### Q73-006 · Walk through the Monty Hall problem, and prove your answer

**Level:** Mid · **Roles:** DA, DS

**Remember it as:** *The host's choice isn't random: he always avoids the car. That single fact is why switching wins twice as often.*

**Answer in one line:** Switching doors wins the car **2/3** of the time; staying wins only **1/3**: because the host's forced choice (he always opens a goat door, never the car) concentrates the other 2/3 probability onto the one remaining unopened door.

**By hand first.** Chapter 21, section 21.7 lists the three places the car can be, in a three-row table: staying wins in one row, switching in two. In an interview, draw that table first. Then offer a simulation as the check, 100,000 games. Before you run it, predict the two numbers it will print:

```python
rng = np.random.default_rng(73)
wins_switch = wins_stay = 0
for _ in range(100_000):
    car = rng.integers(0, 3)
    choice = rng.integers(0, 3)
    remaining = [d for d in range(3) if d != choice and d != car]
    host_opens = rng.choice(remaining)
    switch_choice = [d for d in range(3) if d != choice and d != host_opens][0]
    wins_stay += (choice == car)
    wins_switch += (switch_choice == car)
print(f"stay wins:   {wins_stay / 100_000:.3f}")
print(f"switch wins: {wins_switch / 100_000:.3f}")
```

```
stay wins:   0.332
switch wins: 0.668
```

- `rng = np.random.default_rng(73)` starts the generator again with seed 73, so you get the numbers printed here. `wins_switch = wins_stay = 0` sets both counters to 0 in one line.
- `100_000` is 100000: Python ignores the underscore, which is there to make the number easy to read.
- `rng.integers(0, 3)` draws a whole number from 0 up to, but not including, 3: the three doors, numbered 0, 1 and 2 (Chapter 21, section 21.5 rolled a die the same way).
- `remaining` is a list comprehension with two conditions (Chapter 17, section 17.6): the doors that are neither your pick nor the car, which the host may open. There are two when you picked the car, one otherwise.
- `rng.choice(remaining)` picks one of those doors at random.
- `switch_choice` is the one door that is neither your pick nor the opened one; `[0]` takes it out of its one-item list.
- `wins_stay += (choice == car)` adds the comparison to the counter. When Python adds `True` or `False` to a number it counts them as 1 and 0, so the counter goes up only on a win.

| Tier | What to say |
|---|---|
| Passes | States "switching is better" from memory, can't explain why |
| Strong | The reasoning: your original pick has a 1/3 chance of being right; the other two doors together have a 2/3 chance; once the host removes one (always a goat, never the car), that whole 2/3 collapses onto the single remaining door |
| Extra points | **[+Validate]** a 100,000-game simulation lands almost exactly on the theoretical 1/3 and 2/3<br>**[+Edge cases]** the key, often-missed detail: this only works because the host's action is *not* random: he knows where the car is and always avoids it; if he opened a random unopened door and it happened to reveal a goat, switching would no longer help |

**Likely follow-ups:** What if there were 100 doors instead of 3? What changes if the host sometimes opens the car by accident?
**Red flag:** claiming it's 50/50 after one door is removed, the single most common wrong answer to this exact question.
**Learn it in:** Chapter 21, section 21.7 ("Two famous puzzles").

### Q73-007 · The birthday problem: how many people need to be in a room before it's more likely than not that two share a birthday?

**Level:** Mid · **Roles:** DA, DS

**Remember it as:** *It's not about matching one specific date: it's about how many *pairs* of people exist, and pairs grow far faster than people do.*

**Answer in one line:** Just **23** people, computed as 1 minus the probability that all birthdays are different (the complement rule).

**By hand first.** Chapter 21, section 21.7 builds the answer step by step: the second person misses the first's birthday with probability 364/365, the third misses both with 363/365, and so on, and 1 minus the product is the chance of a match. Here the same loop becomes a function, so you can see the whole curve:

```python
def birthday_prob(n):
    p_no_match = 1.0
    for i in range(n):
        p_no_match *= (365 - i) / 365
    return 1 - p_no_match

for n in (22, 23, 50, 70):
    print(f"{n} people: {birthday_prob(n):.4f}")
```

```
22 people: 0.4757
23 people: 0.5073
50 people: 0.9704
70 people: 0.9992
```

- `birthday_prob(n)` starts with `p_no_match = 1.0` and multiplies in one factor per person. `p_no_match *= x` is short for `p_no_match = p_no_match * x`, as `+=` is for adding (Chapter 17, section 17.6).
- `return 1 - p_no_match` is the complement rule (Chapter 21, section 21.6).
- The loop prints the curve: just under a half at 22 people, just over at 23.

| Tier | What to say |
|---|---|
| Passes | Says 23, from memory, can't explain why |
| Strong | Explains the complement (1 minus the chance all birthdays differ) and the pairs insight: with 23 people there are `23 × 22 / 2 = 253` distinct pairs, each a chance for a shared birthday, and 253 chances is a lot even at low odds per pair |
| Extra points | **[+Validate]** the computed curve above: from under 50% at 22 people to over 99.9% at 70<br>**[+Business]** the same "count the chances, not the people" logic is behind multiple comparisons: 20 metrics at α = 0.05 give 20 chances of a false alarm, 64% overall (Q73-028) |

**Likely follow-ups:** What's the exact formula, not just the loop? How does the answer change for a 50% chance of *three* people sharing a birthday?
**Red flag:** answering close to 183 (half of 365), confusing "matching one specific date" with "any two people matching each other."
**Learn it in:** Chapter 21, section 21.7 ("Two famous puzzles"); the complement rule is section 21.6.

---

## 73.2 Distributions

### Q73-008 · When would you use a Binomial distribution vs. a Poisson distribution?

**Level:** Fresher · **Roles:** DA, DS

**Remember it as:** *Binomial counts successes out of a known, fixed number of tries. Poisson counts events with no fixed "number of tries" at all, just a rate over time or space.*

**Answer in one line:** Binomial models the count of successes in a fixed number of independent yes/no trials (how many of 40 deliveries are late, how many of 100 leads convert); Poisson models the count of events in a fixed interval when there's no natural "number of trials," only an average rate (complaints per week, support tickets per hour, defects per metre of cable).

| Tier | What to say |
|---|---|
| Passes | "Binomial is for two outcomes, Poisson is for counting things" |
| Strong | The trials-vs-rate distinction above, with a concrete example of each |
| Extra points | **[+Edge cases]** a step beyond Chapter 21: Poisson is the limiting case of Binomial as the number of trials grows very large and the per-trial probability gets very small, while their product (the expected count) stays fixed; the two aren't unrelated<br>**[+Business]** Riverstone's 9.4 complaints a week (Chapter 21) is a textbook Poisson count, and so is "how many tickets will arrive in the next hour" for staffing; "what fraction of these 500 leads will convert" is Binomial |

**Likely follow-ups:** What does the Poisson distribution's single parameter (λ) represent? When does Binomial start to look like a Normal distribution?
**Red flag:** treating the two as interchangeable, or not knowing which applies to a described scenario.
**Learn it in:** Chapter 21, section 21.5 (Binomial, Poisson).

### Q73-009 · State the Central Limit Theorem in plain English, and say why it matters even if your underlying data isn't normally distributed

**Level:** Fresher · **Roles:** DA, DS, PA

**Remember it as:** *It doesn't matter what shape the data is. Average enough of it together, and the average's own distribution becomes bell-shaped anyway.*

**Answer in one line:** The Central Limit Theorem says that the distribution of a *sample mean* approaches a Normal distribution as sample size grows, regardless of the shape of the underlying data it's drawn from: which is why so much of statistics (t-tests, confidence intervals) can lean on Normal-distribution math even when real-world data (revenue, wait times) is skewed, not bell-shaped at all.

| Tier | What to say |
|---|---|
| Passes | "Averages tend to be normal" (true, no mechanism, no "why it matters") |
| Strong | + explicitly separates the individual data points (which can be any shape) from the *sample mean's* distribution (which becomes Normal), and connects this to why t-tests and z-tests are valid on skewed real-world data as long as the sample is reasonably large |
| Extra points | **[+Business]** this is why Riverstone's order values (right-skewed, Chapter 21, section 21.4) can still be compared between two groups with a t-test on the means (Chapter 30, section 30.3), even though the raw order values look nothing like a bell curve<br>**[+Edge cases]** "large enough" depends on how skewed the underlying data is; a very heavy-tailed distribution needs a bigger sample before the CLT's approximation is trustworthy |

**Likely follow-ups:** How large does a sample need to be for CLT to "kick in"? What happens to inference if you ignore CLT and the sample is too small?
**Red flag:** claiming the underlying *data* becomes normal, rather than the sample *mean's* distribution.
**Learn it in:** Chapter 21, section 21.8 (sampling and the central limit theorem); skew is section 21.4.

### Rapid-fire, 73.2

Roles: DA and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q73-010 | What does a distribution's variance measure? | The average squared distance of values from the mean: how spread out the data is | **[+Edge cases]** squaring means variance is in squared units (₹² for revenue); standard deviation (variance's square root) is back in the original, interpretable units | Fresher · 21.2 |
| Q73-011 | Normal vs. log-normal distribution: when does each apply? | Normal: symmetric, bell-shaped data / log-normal: data whose *logarithm* is normal, common for values that can't go negative and are right-skewed (revenue, wait times) | **[+Business]** most real business "amount" data (order value, salary, session length) is closer to log-normal than Normal: check before assuming symmetry | Mid · beyond the book (skew 21.4; logs 31.0) |
| Q73-012 | What's a uniform distribution, and give one real business example? | Every outcome in a range is equally likely | **[+Business]** a well-built A/B assignment: each user's hash bucket 0–99 is equally likely, which is what lets you check a 50/50 split (Q73-026); also `rng.uniform(1, 10, 200)` in Q73-032, where every account size from 1 to 10 is equally likely | Fresher · 21.5 |
| Q73-013 | What does "long-tailed" or "heavy-tailed" mean? | Extreme values occur more often than a Normal distribution would predict | **[+Edge cases]** heavy-tailed data can make sample means unstable and confidence intervals misleadingly narrow if treated as Normal without checking | Mid · 21.4 |

---

## 73.3 Hypothesis testing fundamentals

### Q73-014 · Explain a p-value to a non-technical stakeholder, without saying "probability that the null hypothesis is true"

**Level:** Fresher · **Roles:** DA, DS, PA, BA

**Remember it as:** *A p-value answers "how surprising is this result, if nothing real were going on?" It never answers "how likely is it that something real is going on?"*

**Answer in one line:** A p-value is the probability of seeing a result at least as extreme as what you observed, *if the null hypothesis were actually true*: it's a statement about how surprising your data is under "nothing changed," not a statement about the probability that something changed.

| Tier | What to say |
|---|---|
| Passes | "It tells you if the result is significant" (technically true, doesn't explain the mechanism, invites the classic misreading) |
| Strong | The correct definition above, explicitly distinguishing it from "probability the null hypothesis is true," which is the single most common misinterpretation |
| Extra points | **[+Business]** a non-technical framing that avoids the trap: "if our change actually did nothing, we'd see a result this extreme only 3% of the time by chance, which is why we're treating it as a real effect"<br>**[+Edge cases]** a p-value says nothing about the *size* of an effect, only its surprise value under the null: a tiny, practically meaningless effect can still have a very small p-value with enough data |

**Likely follow-ups:** What's the difference between statistical significance and practical significance? Why is p < 0.05 the conventional threshold, and is it always the right one?
**Red flag:** defining a p-value as "the probability the null hypothesis is true" or "the probability the result is due to chance," both common, both wrong.
**Learn it in:** Chapter 22, section 22.2 ("What a p-value is not"); Chapter 30, section 30.3 ("What the p-value does not say"); practical significance is Chapter 22, section 22.8.

### Q73-015 · Demonstrate that underpowered tests miss real effects far more often than people expect

**Level:** Mid · **Roles:** DA, DS, PA

**Remember it as:** *A small sample doesn't just make you less sure: it makes you actively likely to miss a real, meaningful effect entirely.*

**Answer in one line:** With a real effect but too small a sample, a test's **Type II error rate** (missing a real effect) can be dramatically higher than most people's intuition suggests, and it falls sharply as sample size grows.

**Verified, live:** a true underlying difference of 0.3 standard deviations, tested with a t-test, 2,000 simulated experiments at each sample size:

```python
rng = np.random.default_rng(73)
for n in [30, 200]:
    misses = 0
    for _ in range(2000):
        a = rng.normal(0, 1, n)
        b = rng.normal(0.3, 1, n)
        t, p = stats.ttest_ind(a, b)
        if p >= 0.05:
            misses += 1
    print(f"n={n} per group: Type II error rate = {misses / 2000:.3f}")
```

```
n=30 per group: Type II error rate = 0.800
n=200 per group: Type II error rate = 0.138
```

- `rng.normal(0, 1, n)` draws `n` values from a normal distribution with mean 0 and standard deviation 1: group A. Group B has mean 0.3, so a real difference of 0.3 standard deviations always exists.
- `stats.ttest_ind(a, b)` is the two-sample t-test (Chapter 22, section 22.2; Chapter 30, section 30.3). It returns the t statistic and the p-value, which `t, p = ...` unpacks. Without `equal_var=False` it's the ordinary t-test, which is fine here because both groups have the same spread.
- `if p >= 0.05: misses += 1` counts the experiments that fail to find the difference: each one is a Type II error.

With only 30 people per group, a real effect is **missed 80% of the time**: the test says "no significant difference" four times out of five, even though a real difference exists. At 200 per group, that drops to 13.8%.

| Tier | What to say |
|---|---|
| Passes | "Bigger samples are more reliable" (true, no sense of *how much* more reliable) |
| Strong | Explains Type II error and power correctly, and that underpowered tests systematically under-detect real effects, not just "add noise" |
| Extra points | **[+Validate]** the simulated numbers above: an 80% miss rate falling to 14% from sample size alone, nothing else changed<br>**[+Business]** a team that runs an underpowered A/B test and concludes "no effect" when there actually was one has made a real, costly, invisible mistake, not a safe, conservative call: this is exactly why sample-size planning (section 73.4, Q73-020) happens *before* a test runs, not after |

**Likely follow-ups:** What's the relationship between power, effect size, sample size, and significance level? How do you choose a target power before running a test?
**Red flag:** treating "not statistically significant" as proof "there's no effect," rather than "we may not have had enough data to detect one."
**Learn it in:** Chapter 22, section 22.3 (Type II error and power); Chapter 30, section 30.7 (power and sample size).

### Rapid-fire, 73.3

Roles: DA, DS and PA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q73-016 | Type I vs. Type II error? | Rejecting a true null (a false alarm) / failing to reject a false null (a miss) | **[+Business]** which error costs more depends on context: a fraud check favours avoiding Type II (missing real fraud); an automatic account-freeze rule favours avoiding Type I (freezing an honest customer's account) | Fresher · 22.3 |
| Q73-017 | What's statistical power? | The probability of correctly detecting a real effect when one exists, i.e. `1 - Type II error rate` | **[+Business]** 80% power is the conventional target, meaning you accept a 1-in-5 chance of missing a real effect even when your test is well-designed | Fresher · 22.3, 30.7 |
| Q73-018 | t-test vs. z-test, when does it matter which you use? | t-test when the population standard deviation is unknown and estimated from the sample (the usual real-world case); z-test when it's known, or for proportions with large samples | **[+Edge cases]** with a large sample, the t-distribution converges to the normal distribution anyway, so the practical difference shrinks as n grows | Mid · 22.1, 22.2 |
| Q73-019 | What does a 95% confidence interval actually mean? | If you repeated the sampling process many times, 95% of the resulting intervals would contain the true population value | **[+Edge cases]** it does *not* mean "95% probability the true value is in this specific interval": the true value either is or isn't in any single interval; the 95% describes the *procedure's* long-run reliability | Fresher · 22.1 |

---

## 73.4 A/B test design

### Q73-020 · Calculate the required sample size for an A/B test, before running it

**Level:** Mid · **Roles:** DA, DS, PA

**Remember it as:** *You need four numbers before you can answer "how many": baseline rate, the smallest change worth detecting, your significance level, and your desired power.*

**Answer in one line:** Sample size depends on the baseline conversion rate, the **minimum detectable effect (MDE)** you actually care about, the significance level (usually 0.05), and the desired power (usually 0.80): smaller effects and higher confidence both require larger samples.

**Verified, live:** baseline conversion 9.6%, and the business says the smallest lift worth acting on is 1.5 percentage points (to 11.1%), at 80% power and α = 0.05:

```python
effect_size = sms.proportion_effectsize(0.111, 0.096)
n_required = sms.NormalIndPower().solve_power(effect_size, power=0.8, alpha=0.05, ratio=1)
print(f"Cohen's h = {effect_size:.4f}")
print(f"Required sample size per group: {np.ceil(n_required):,.0f}")
```

```
Cohen's h = 0.0493
Required sample size per group: 6,466
```

- `sms.proportion_effectsize(0.111, 0.096)` turns the two rates into **Cohen's h**, an effect size for proportions built on an arcsine scale (Chapter 30, section 30.7). The rate you hope for goes first, the baseline second, as in Chapter 30.
- `sms.NormalIndPower()` is a power calculator for two independent groups. `.solve_power(...)` solves for whichever number you leave out: here the sample size, given `power=0.8`, `alpha=0.05`, and `ratio=1` (the second group is the same size as the first).
- `np.ceil` rounds **up**, because 6,465.6 people would leave the test slightly short of its power; `:,.0f` prints a whole number with a thousands comma.

Chapter 22's hand formula, `sample_size_for_proportion(0.096, 1.5)` from section 22.3, gives 6,473 for the same inputs. The small difference is the effect-size scale (statsmodels works on Cohen's h, an arcsine transform). Either answer is fine in an interview; say which one you used.

| Tier | What to say |
|---|---|
| Passes | "You need a big enough sample" with no method for computing it |
| Strong | Names the four required inputs, and correctly identifies that MDE is a *business* decision (how small a change is still worth caring about), not a purely statistical one |
| Extra points | **[+Validate]** the computed number above, 6,466 per group, checked against Chapter 22's formula, not a guessed round number<br>**[+Business]** this number directly answers "how long will this test need to run": divide 6,466 by the expected daily traffic per arm. It's the most common follow-up question from a stakeholder, and this calculation answers it |

**Likely follow-ups:** How does the required sample size change if the MDE gets smaller (harder to detect)? What if traffic is limited, how would you trade off test duration against detectable effect size?
**Red flag:** picking a sample size arbitrarily ("let's run it for two weeks") with no power calculation behind it.
**Learn it in:** Chapter 22, section 22.3 (designing an A/B test, the sample-size formula); Chapter 30, section 30.7 (power and sample size, Cohen's h).

### Q73-021 · What's a Minimum Detectable Effect (MDE), and who should decide it?

**Level:** Mid · **Roles:** DA, DS, PA, BA

**Remember it as:** *MDE isn't a statistics question. It's "how small a change would we actually act on?": a business question dressed in statistical clothing.*

**Answer in one line:** The MDE is the smallest true effect size a test is designed to reliably detect; choosing too small an MDE demands an impractically large sample, while choosing too large a one risks missing real, meaningful improvements that are just below the threshold.

| Tier | What to say |
|---|---|
| Passes | "It's the effect size you're testing for" (correct, misses who should set it and why) |
| Strong | + explicitly: the MDE should come from the business ("would we actually change anything for a 0.5 percentage point lift? For 2 points?"), not be back-calculated from whatever sample size happens to be convenient |
| Extra points | **[+Business]** setting the MDE by working backward from "what sample size can we get in two weeks" instead of forward from "what change would we actually act on" is a common, subtle mistake: it optimizes for a schedule, not for a decision worth making<br>**[+Edge cases]** an MDE set too small can make a test run for months chasing statistical significance on an effect too tiny to matter commercially even if proven real |

**Likely follow-ups:** How would you choose an MDE with no historical baseline data at all? What happens if the observed effect is smaller than the MDE but still "significant"?
**Red flag:** treating MDE as a purely mathematical input with no connection to what the business would actually do differently.
**Learn it in:** Chapter 22, section 22.3; Chapter 30, sections 30.7 and 30.8 (designing an experiment).

### Rapid-fire, 73.4

Roles: DA, DS and PA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q73-022 | Why randomize which users see which variant? | Randomization is what makes the two groups comparable on everything else (known and unknown factors alike), so any observed difference can be attributed to the treatment | **[+Edge cases]** this is the entire logic of a controlled experiment versus an observational comparison (section 73.6): randomization is what earns the right to say "caused," not just "correlated" | Fresher · 22.3, 30.8 |
| Q73-023 | One-tailed vs. two-tailed test, when would you use each? | Two-tailed for a change in either direction (the book's default); one-tailed only when chosen before seeing the data, and only when a change in the other direction would lead to the same decision | **[+Edge cases]** switching to a one-tailed test after seeing the data, to make a marginal result "significant," is a form of p-hacking | Mid · 22.2 |
| Q73-024 | What's a holdout group, and why keep one even after shipping a winning test? | Beyond the book: a small group (say 5% of users) deliberately kept on the old version after launch, to measure the change's lasting effect against a true baseline | **[+Business]** without a holdout, a genuinely working feature's impact becomes impossible to separate from seasonal trends or other changes happening at the same time | Mid · beyond the book (design: 30.8) |

---

## 73.5 A/B test debugging

### Q73-025 · A dashboard shows a "statistically significant" result after checking it daily throughout the test. What's wrong, and prove it?

**Level:** Mid · **Roles:** DA, DS, PA

**Remember it as:** *Checking significance every day and stopping the moment it looks good is like flipping a coin until it lands on heads, then calling the coin biased.*

**Answer in one line:** Checking for significance repeatedly and stopping as soon as p < 0.05 appears (**"peeking"**) inflates the true false-positive rate far above the nominal 5%, because each additional look is another chance for random noise to cross the threshold.

**Verified, live:** 2,000 simulated experiments with **no real effect at all** (both groups drawn from the identical distribution). Data arrives 20 per group at a time, and a t-test runs at every look from 40 to 200 per group: 9 looks in all:

```python
rng = np.random.default_rng(73)
false_positives = 0
for _ in range(2000):
    data_a, data_b = [], []
    found_sig = False
    for _ in range(10):
        data_a.extend(rng.normal(0, 1, 20))
        data_b.extend(rng.normal(0, 1, 20))
        if len(data_a) >= 40:
            t, p = stats.ttest_ind(data_a, data_b)
            if p < 0.05:
                found_sig = True
                break
    false_positives += found_sig
print(f"false positive rate with repeated peeking: {false_positives / 2000:.3f}")
```

```
false positive rate with repeated peeking: 0.163
```

- `data_a.extend(...)` adds 20 new values to the list: one more batch of visitors per group. Ten batches take each group to 200.
- `if len(data_a) >= 40` skips a test on the very first batch, so the looks come at 40, 60, …, 200 per group: 9 of them.
- `found_sig = True` and `break` stop the experiment at the first p below 0.05: that's the peeking.
- `false_positives += found_sig` counts `True` as 1, as in Q73-006.

With **no real effect whatsoever**, peeking and stopping at the first significant-looking result gives a false "win" **more than 3 times as often** as the stated 5% significance level promises. The exact rate moves a little with the seed (between 16% and 18% across ten seeds), and it grows with the number of looks: Chapter 22, section 22.4 found 14.3% with five looks and 23.9% with twenty.

| Tier | What to say |
|---|---|
| Passes | "You shouldn't check too often" (correct instinct, no quantified reason) |
| Strong | Explains the mechanism: each check is another roll of the dice against a 5% threshold, and repeated rolls compound the chance of a false positive somewhere along the way |
| Extra points | **[+Validate]** the simulated number above: a false-positive rate of about 16% against a claimed 5%, from peeking alone, on data with zero true effect<br>**[+Business]** the fix isn't "never check early," it's using a sequential testing method (group sequential design, or Bayesian methods designed for continuous monitoring) that's built to allow early looks without inflating the error rate: or committing to a single, pre-planned sample size and analysis date and holding to it |

**Likely follow-ups:** What's a sequential testing correction, in concept? How would you explain this risk to a PM who wants a "quick check" on day 2 of a two-week test?
**Red flag:** not recognizing peeking as a real statistical problem, treating it as a minor process nitpick.
**Learn it in:** Chapter 22, section 22.4 ("Peeking"); Chapter 30, section 30.10 ("Peeking").

### Q73-026 · An A/B test's traffic split is supposed to be 50/50, but you're seeing 5,200 vs. 4,800. Is that a problem?

**Level:** Mid · **Roles:** DA, DS, PA

**Remember it as:** *A Sample Ratio Mismatch is a smoke alarm for the whole experiment, not a statistics problem to explain away.*

**Answer in one line:** Run a chi-square goodness-of-fit test against the expected 50/50 split; if it's significant, you have a **Sample Ratio Mismatch (SRM)**, which almost always means something is broken in how users were assigned to groups, not real random variation, and the experiment's other results shouldn't be trusted until it's found and fixed.

**Verified, live, two scenarios:**

```python
for observed in ([5200, 4800], [5100, 4900]):
    chi2, p = stats.chisquare(observed, f_exp=[5000, 5000])
    print(f"observed {observed}: chi2 = {chi2:.3f}, p = {p:.4f}")
```

```
observed [5200, 4800]: chi2 = 16.000, p = 0.0001
observed [5100, 4900]: chi2 = 4.000, p = 0.0455
```

- `stats.chisquare(observed, f_exp=[5000, 5000])` is the goodness-of-fit test from Chapter 30, section 30.9 (Step 2). `f_exp` is the list of **expected** counts: an exact 50/50 split of 10,000. Leave it out and SciPy assumes equal counts anyway, which is what Chapter 30 did; writing it makes the 50/50 assumption visible, and lets you test a 90/10 split the same way.
- The loop runs the test on both splits and prints the statistic and the p-value.

The 5,200/4,800 split is a real SRM (p = 0.0001): investigate before reading any result. The 5,100/4,900 split gives p = 0.0455: under 0.05, but not under the stricter alarm teams usually use (below), so it's worth a look at the assignment logs, not an alarm. Chapter 30's Riverstone website test (24,036 vs 23,250 visitors, p = 0.0003) is exactly the first case, and section 30.10 finds its cause.

| Tier | What to say |
|---|---|
| Passes | "That's probably just random variation, it's close to 50/50" |
| Strong | Runs the chi-square test rather than eyeballing it, and correctly treats a significant result as a red flag about the experiment's plumbing, not a metric to report on |
| Extra points | **[+Validate]** the test itself: 5,200/4,800 is a significant SRM (p = 0.0001), while 5,100/4,900 is not under a strict rule (p = 0.0455): "looks close to 50/50" and "is statistically expected under 50/50" are different questions<br>**[+Edge cases]** teams usually alarm on SRM at p < 0.001, not 0.05, because they check every experiment daily. At 0.05, one healthy test in 20 would trip the alarm (Q73-028's logic)<br>**[+Business]** common real causes: a bug in the randomization code, a caching layer serving one variant more, bot traffic disproportionately hitting one arm, or a redirect that silently drops some users from one variant before they're even counted |

**Likely follow-ups:** If you find an SRM, do you throw out the whole test? How would you debug which stage of the pipeline caused it?
**Red flag:** treating a skewed split as a minor curiosity rather than a signal the whole experiment's data may be unreliable.
**Learn it in:** Chapter 30, section 30.9 (Step 2, the sample-ratio check) and section 30.10 ("Sample-ratio mismatch: finding the cause").

### Rapid-fire, 73.5

Roles: DA, DS and PA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q73-027 | What's a novelty effect in an A/B test? | Users react to a change simply because it's *new*, not because it's actually better, and the effect fades over time | **[+Business]** a test that shows a strong early lift can be entirely novelty; running long enough to see the effect stabilize (or a holdout, Q73-024) separates the two | Mid · 30.10 |
| Q73-028 | Why is testing 20 different success metrics in one experiment a problem? | Multiple comparisons: testing many unrelated metrics multiplies the chance that at least one looks "significant" purely by chance | **[+Validate]** 20 metrics with no real effect, each tested at α = 0.05: P(at least one false positive) = 1 − 0.95<sup>20</sup> = 0.642; a simulation of 10,000 such experiments (seed 73) gives 0.639 | Mid · 22.4 |
| Q73-029 | What's a Bonferroni correction, in one sentence? | Divide the significance threshold by the number of comparisons, so the *combined* false-positive risk across all of them stays at the original level | **[+Trade-offs]** simple and conservative, but it can make genuinely real effects harder to detect (lower power) when many comparisons are tested at once | Mid · 22.4 |
| Q73-030 | What's a network effect / interference problem in A/B testing? | When a treated user's behavior affects a control user's outcome (e.g., a social feature, a marketplace with shared inventory), violating the assumption that groups are independent | **[+Business]** standard A/B math assumes no spillover between groups; a marketplace or social feature test may need a different design (geographic or time-based splitting) to avoid contaminating the control group | Senior · 31.5 |

---

## 73.6 Causal inference and Simpson's paradox

### Q73-031 · Construct a Simpson's paradox: show a sales rep who is better in every category yet worse overall

**Level:** Mid · **Roles:** DA, DS, PA, BA

**Remember it as:** *When the group sizes are unbalanced across categories, "better in every group" and "better overall" can point in opposite directions at the same time.*

**Answer in one line:** Simpson's paradox occurs when a trend present in every subgroup reverses when the subgroups are combined, because the subgroups are weighted very differently in size.

**Verified, live.** Two reps, easy and hard leads, each stored as (won, total):

```python
rep_a = {"easy": (9, 10), "hard": (30, 100)}     # (won, total)
rep_b = {"easy": (80, 100), "hard": (2, 10)}
for kind in ["easy", "hard"]:
    won_a, total_a = rep_a[kind]
    won_b, total_b = rep_b[kind]
    print(f"{kind}: Rep A {won_a / total_a:.0%} ({won_a}/{total_a}), Rep B {won_b / total_b:.0%} ({won_b}/{total_b})")
```

```
easy: Rep A 90% (9/10), Rep B 80% (80/100)
hard: Rep A 30% (30/100), Rep B 20% (2/10)
```

- Each dictionary maps a lead type to a pair of numbers, (won, total). `won_a, total_a = rep_a[kind]` unpacks the pair into two names.
- `:.0%` prints a share as a whole percentage.

Now add up each rep's leads across both types:

```python
won_a = rep_a["easy"][0] + rep_a["hard"][0]
total_a = rep_a["easy"][1] + rep_a["hard"][1]
won_b = rep_b["easy"][0] + rep_b["hard"][0]
total_b = rep_b["easy"][1] + rep_b["hard"][1]
print(f"Rep A overall: {won_a / total_a:.1%} ({won_a}/{total_a})")
print(f"Rep B overall: {won_b / total_b:.1%} ({won_b}/{total_b})")
```

```
Rep A overall: 35.5% (39/110)
Rep B overall: 74.5% (82/110)
```

- `rep_a["easy"][0]` is the first number of the easy pair, the leads won; `[1]` is the second, the total.

**Rep A wins both categories** (90% beats 80% on easy leads; 30% beats 20% on hard leads) **but Rep B's overall win rate is more than double Rep A's** (74.5% vs. 35.5%). The reversal happens because Rep A worked mostly hard leads (where everyone's rate is lower) and Rep B worked mostly easy leads (where everyone's rate is higher): the mix, not the skill, is driving the overall number.

| Tier | What to say |
|---|---|
| Passes | Can define Simpson's paradox abstractly, can't construct or recognize a real example |
| Strong | The worked example above, correctly identifying that unequal group sizes (Rep A mostly on hard leads, Rep B mostly on easy ones) is the mechanism, not some statistical trick |
| Extra points | **[+Validate]** the checkable numbers above, both the subgroup rates and the reversed overall rates<br>**[+Business]** this is exactly why comparing two sales reps', two ad campaigns', or two hospitals' raw overall success rates can be actively misleading if their underlying mix of harder and easier cases differs: always check the subgroup breakdown before ranking on an aggregate number |

**Likely follow-ups:** How would you fix the comparison to be fair? *(Compare like-for-like within each category, or weight by a standardized mix: the same logic behind a standardized/risk-adjusted rate.)* Can you think of a real Simpson's paradox from your own work?
**Red flag:** not recognizing that the paradox is *always* about the mix/weighting, not about the individual category numbers being wrong.
**Learn it in:** Chapter 22, section 22.6 (Simpson's paradox; "Standardizing, by hand" answers the first follow-up).

### Q73-032 · A strong correlation between website logins and revenue disappears almost entirely once you control for account size. What happened?

**Level:** Senior · **Roles:** DA, DS, PA

**Remember it as:** *A confounder is a hidden variable pulling the strings on both sides of a correlation you're looking at.*

**Answer in one line:** Account size is a **confounder**: bigger accounts naturally log in more *and* naturally generate more revenue, creating a strong correlation between logins and revenue that has nothing to do with logins actually driving revenue.

**Verified, live.** First, build 200 accounts where size drives both logins and revenue, and measure the raw correlation:

```python
rng = np.random.default_rng(73)
account_size = rng.uniform(1, 10, 200)
logins = account_size * 2 + rng.normal(0, 2, 200)
revenue = account_size * 50000 + rng.normal(0, 20000, 200)

r_raw, _ = stats.pearsonr(logins, revenue)
print(f"raw correlation(logins, revenue) = {r_raw:.3f}")
```

```
raw correlation(logins, revenue) = 0.922
```

- `rng.uniform(1, 10, 200)` draws 200 account sizes, each equally likely to be anywhere from 1 to 10 (a uniform distribution, Chapter 21, section 21.5).
- `logins` is 2 per unit of size plus random noise; `revenue` is 50,000 per unit of size plus noise. `rng.normal(0, 2, 200)` is the noise: 200 values with mean 0 and standard deviation 2.
- `stats.pearsonr(logins, revenue)` returns Pearson's r and a p-value (Chapter 22, section 22.5); `r_raw, _ = ...` keeps r and throws the p-value away (`_` is the usual name for a value you don't need).

Revenue is built from size only, and logins from size only. Logins never enter the revenue formula, so any logins→revenue correlation must come through size.

**Beyond the book: partial correlation.** Chapter 22 doesn't teach it, and the idea fits in one sentence: partial correlation is the correlation of what's left in logins and revenue once account size is removed from both. Remove size with a straight line (section 22.10), keep what's left over (the **residuals**), and correlate those:

```python
def partial_corr(x, y, z):
    slope_x, intercept_x = np.polyfit(z, x, 1)
    slope_y, intercept_y = np.polyfit(z, y, 1)
    resid_x = x - (slope_x * z + intercept_x)
    resid_y = y - (slope_y * z + intercept_y)
    r, _ = stats.pearsonr(resid_x, resid_y)
    return r

print(f"partial correlation, controlling for size = {partial_corr(logins, revenue, account_size):.3f}")
```

```
partial correlation, controlling for size = 0.029
```

- `np.polyfit(z, x, 1)` fits a straight line (a polynomial of degree `1`) that predicts `x` from `z`, and returns its slope and intercept: the least-squares line of Chapter 22, section 22.10.
- `resid_x = x - (slope_x * z + intercept_x)` is each account's actual logins minus the logins its size predicts: the part of logins that size doesn't explain. `resid_y` does the same for revenue.
- `stats.pearsonr(resid_x, resid_y)` correlates the two leftovers.

The book's own tool gives the same verdict. A regression with both variables (Chapter 22, section 22.10, "More than one x"; Chapter 30, section 30.11) reads each coefficient "holding the others fixed":

```python
import pandas as pd
import statsmodels.formula.api as smf

accounts = pd.DataFrame({"revenue": revenue, "logins": logins, "account_size": account_size})
model = smf.ols("revenue ~ logins + account_size", data=accounts).fit()
print(model.params.round(0))
print(f"p-value for logins: {model.pvalues['logins']:.2f}")
```

```
Intercept        2099.0
logins            248.0
account_size    49596.0
dtype: float64
p-value for logins: 0.68
```

- `pd.DataFrame({...})` puts the three arrays into one table, one column each, because `smf.ols` reads its columns by name.
- `smf.ols("revenue ~ logins + account_size", data=accounts).fit()` fits revenue on logins and account size together, exactly as in Chapter 30, section 30.11.
- `model.params` holds the intercept and the two coefficients; `.round(0)` rounds them to whole numbers. `model.pvalues['logins']` is the p-value for the logins coefficient.

The raw correlation of **0.92** (very strong) collapses to essentially **zero (0.03)** once account size is accounted for, in data that was built with *no direct causal link* between logins and revenue at all, only a shared cause. The regression says the same: with size held fixed, one extra login goes with only 248 more revenue, and that coefficient is nowhere near significant (p = 0.68), while size carries about 50,000 per unit (49,596), the number the data was built with.

| Tier | What to say |
|---|---|
| Passes | "Correlation isn't causation" (true, doesn't diagnose *this specific* case) |
| Strong | Correctly names account size as a likely confounder and proposes checking a partial correlation or controlling for it in a regression |
| Extra points | **[+Validate]** the numbers above: a constructed example with zero true login→revenue effect, where the naive correlation would badly mislead anyone who stopped there<br>**[+Business]** this is precisely the trap in a claim like "customers who log in more spend more, so let's push login frequency": the real driver (account size) isn't something a login-nudge campaign can change at all, and the campaign would likely show no revenue impact despite the strong raw correlation |

**Likely follow-ups:** How would you actually test whether logins *cause* more revenue, not just correlate with it? What's the difference between controlling for a confounder and running a randomized experiment?
**Red flag:** citing "correlation isn't causation" as a complete answer without identifying what the actual confounder is or how to check for one.
**Learn it in:** Chapter 22, section 22.5 (confounders) and section 22.10 ("More than one x"); Chapter 30, section 30.11 ("Several variables at once"). Partial correlation is Beyond the book, explained above.

### Rapid-fire, 73.6

Roles: DA, DS, PA and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q73-033 | What's selection bias, with one business example? | The sample you're analyzing isn't representative of the population you're trying to draw conclusions about | **[+Business]** analyzing only customers who responded to a survey, and concluding "customers are satisfied," ignores the (likely more dissatisfied) customers who didn't bother responding at all | Fresher · 22.7 |
| Q73-034 | What's a natural experiment? | A real-world situation where something close to random assignment happens without anyone deliberately designing an experiment (a policy change hitting some regions and not others, or a threshold in a business rule) | **[+Business]** useful exactly when a true randomized test isn't ethical or possible, though weaker than a real randomized experiment since the "randomness" is only approximate | Mid · 31.3, 31.7 |
| Q73-035 | Why is "the data speaks for itself" a red flag phrase in a causal claim? | Data alone never distinguishes correlation from causation; that distinction always requires an assumption about the process that generated the data (randomization, a natural experiment, or a stated causal model) | **[+Business]** anyone claiming pure data-driven causal certainty with no discussion of confounders or study design is skipping the hardest, most important part of the analysis | Senior · 22.5, 31.9 |

---

## 73.7 Live-coding and live-analysis walk-throughs

### Q73-036 · Walk-through: is this A/B test result real, worth shipping, and safe to trust?

**Level:** Senior · **Roles:** DA, DS, PA

**What they're really testing:** whether you run the full checklist (significance, effect size, SRM, power, practical relevance) rather than stopping at the first "p < 0.05."

**The setup, talked through live:** "I've got control at 480/5,000 conversions and treatment at 545/5,000. Before I say anything about shipping this, I want to check four things in order: is the split itself sane (no SRM), is the difference statistically significant, how big is the effect in business terms, and was the test big enough to trust a result this size."

**Verified, live.** First, the two-proportion z-test:

```python
count = np.array([545, 480])     # conversions: treatment, control
nobs = np.array([5000, 5000])    # visitors:    treatment, control
z_stat, p_value = sms.proportions_ztest(count, nobs)
print(f"control:   {480 / 5000:.2%}")
print(f"treatment: {545 / 5000:.2%}")
print(f"z = {z_stat:.3f}, p = {p_value:.4f}")
```

```
control:   9.60%
treatment: 10.90%
z = 2.143, p = 0.0321
```

- `sms.proportions_ztest(count, nobs)` is the two-proportion z-test from Chapter 22, section 22.2: `count` holds the conversions and `nobs` the visitors, in the same order.
- The order matters for the sign. Treatment comes first, so a positive z means treatment converted more; swap the two and z becomes −2.143 with the same p-value.

Next, how big the lift is, with its uncertainty:

```python
low, high = sms.confint_proportions_2indep(545, 5000, 480, 5000, method="wald")
print(f"lift: {(545 / 5000 - 480 / 5000) * 100:.1f} points, 95% interval {low * 100:+.2f} to {high * 100:+.2f} points")
```

```
lift: 1.3 points, 95% interval +0.11 to +2.49 points
```

- `confint_proportions_2indep(545, 5000, 480, 5000, method="wald")` gives the 95% interval for the first rate minus the second, with the textbook formula, as in Chapter 30, section 30.5. Multiplying by 100 turns shares into percentage points; `:+.2f` prints the sign.

Last, was the test big enough? Power for the lift we saw, and the sample that 80% power would have needed:

```python
observed_h = sms.proportion_effectsize(0.109, 0.096)
power = sms.NormalIndPower().power(observed_h, nobs1=5000, alpha=0.05, ratio=1)
needed = sms.NormalIndPower().solve_power(observed_h, power=0.8, alpha=0.05, ratio=1)
print(f"power at 5,000 per arm for a 1.3-point lift: {power:.2f}")
print(f"per arm for 80% power: {np.ceil(needed):,.0f}")
```

```
power at 5,000 per arm for a 1.3-point lift: 0.57
per arm for 80% power: 8,537
```

- `.power(observed_h, nobs1=5000, ...)` is the same calculator as Q73-020, run the other way: given the sample size, it returns the power.
- `.solve_power(...)` is Q73-020's call, for the lift this test actually saw.

**Talked through, live:** "p = 0.032, under the usual 0.05 threshold, so it's statistically significant. The lift is 1.3 percentage points, about a 13.5% relative improvement, which sounds meaningful, but I'd want to know the actual revenue or cost tied to a conversion before calling it worth shipping: statistical significance isn't the same question as 'is this worth the engineering cost to keep.' The split is exactly 5,000 vs. 5,000, so there's no SRM concern. And this is where it gets interesting: for a 1.3-point lift on 9.6%, 80% power needs about 8,500 per arm, and even the 1.5-point MDE of Q73-020 needs 6,466. We have 5,000, so power was only about 57% for the lift we saw. Either the test was stopped early, or it was never sized. A 'significant' result from an underpowered test is more likely to overstate the true lift, so I'd report the 95% interval for the difference, +0.11 to +2.49 points, and recommend running to the planned size before shipping."

**Why "overstate"?** Beyond the book, in one paragraph: when a test is too small, only the runs where chance pushed the lift *up* clear the significance bar. So among the significant results of small tests, the lift is, on average, larger than the truth, and it tends to shrink when the test is rerun at full size. This is sometimes called the **winner's curse**.

**Extra-points moves demonstrated:** **[+Signpost]** named a four-step checklist up front, then ran it in order. **[+Validate]** the real z-test, the interval, and the power (0.57 at 5,000 per arm), not an assumed conclusion. **[+Business]** explicitly separated "statistically significant" from "worth shipping," which are different questions with different owners. **[+Limits]** said plainly what an underpowered test can't show, and what would settle it.

**Likely follow-ups:** What if the sample sizes were very different between arms? How would you incorporate a cost estimate into the shipping decision?
**Red flag:** treating a single p-value as a complete answer to "should we ship this."
**Learn it in:** Chapter 30, section 30.9 (Riverstone's website test, end to end), section 30.7 (power and sample size), and section 30.5 (the interval for two proportions).

### Q73-037 · Walk-through: a stakeholder shows you a chi-square test result and asks what it means

**Level:** Mid · **Roles:** DA, DS, PA, BA

**What they're really testing:** whether a chi-square test's actual question (independence between two categorical variables) is understood, not just its p-value.

**Talked through live:** "A chi-square test of independence checks whether two categorical variables are related at all, not the direction or size of the relationship, just whether the pattern of counts differs from what independence would predict."

**Verified, live**, on a segment-by-conversion table:

```python
observed = np.array([[120, 80], [90, 110]])   # rows: segment; columns: converted, not converted
chi2, p, dof, expected = stats.chi2_contingency(observed, correction=False)
print(f"chi2 = {chi2:.3f}, p = {p:.4f}, dof = {dof}")
print("expected counts under independence:", expected.tolist())
```

```
chi2 = 9.023, p = 0.0027, dof = 1
expected counts under independence: [[105.0, 95.0], [105.0, 95.0]]
```

- `stats.chi2_contingency(observed, correction=False)` is the test from Chapter 22, section 22.2. It returns four things, which `chi2, p, dof, expected = ...` unpacks: the statistic, the p-value, the degrees of freedom, and the table of counts you'd expect if segment and conversion were unrelated.
- `correction=False` turns off **Yates' continuity correction**, a small, conservative adjustment SciPy applies to 2×2 tables by default. Chapter 22 turned it off too, so the result matches the hand sum and the two-proportion z-test. **What happens if you change it:** drop `correction=False`, and this table gives 8.431 (p = 0.0037) instead. In an interview, say which one you used.
- `expected.tolist()` prints the expected table as a plain list of rows.

**Talked through, live:** "p = 0.0027 says the segments and conversion aren't independent, real evidence of a relationship. But chi-square alone doesn't say *which* segment converts better or by how much, only that a relationship exists. I'd follow it with the actual conversion rates per segment to answer the business question, and I'd check the expected-counts table, shown here, to make sure no cell had too few expected observations for the test to be reliable, a common chi-square validity issue with small samples."

**Extra-points moves demonstrated:** **[+Limits]** said what chi-square can't tell you: "a relationship exists" (what it tests) is not "here's the relationship" (a separate follow-up). **[+Edge cases]** flagged the small-expected-count validity concern unprompted.

**Likely follow-ups:** What test would you use for two continuous variables instead? What's Cramér's V, and when would you report it alongside the p-value?
**Red flag:** interpreting a significant chi-square result as telling you the direction or size of an effect, which it doesn't.
**Learn it in:** Chapter 22, section 22.2 ("The chi-square test, by hand first"); Chapter 30, section 30.5 (chi-square and Cramér's V).

---

## 73.8 Predict the number: the arithmetic that quietly goes wrong

Everything so far in this chapter has tested whether you understand the *statistics*: base rates, power, peeking, Simpson's paradox. This section tests something narrower and just as costly — whether the number you reported is the number you think you computed.

These are not conceptual traps. Every one of them is an analysis that runs without error, produces a plausible figure, and is wrong. A standard deviation that differs by library. An average conversion rate that is three times too high. A correlation of exactly zero on a perfect relationship. None of them raises anything; all of them end up in a slide.

So the format is: here is the setup, what is the number? Say it out loud, then read on.

What they have in common is that a tool made a choice on your behalf — a default divisor, an unweighted mean, a linear measure of association — and did not mention it. The habit worth building is to ask, of any number you did not compute by hand, *which formula did this use?*

**How these were run.** Every figure below was produced by running the code, using the chapter's setup cell (section 73.0) with `rng = np.random.default_rng(73)` reseeded in each cell, so each one reproduces on its own. Run them yourself and you will get the same numbers.

**What is not here.** The famous probability traps are already in this chapter and are not repeated: Bayes and the rare-disease test is Q73-005, the birthday problem Q73-007, peeking Q73-025, testing twenty metrics Q73-028, Simpson's paradox section 73.6. Two questions below deliberately go deeper into ground a rapid-fire row already touched, and say so.

### Q73-038 · `np.std(x)` and `pd.Series(x).std()` on the same numbers

**Level:** Fresher · **Roles:** DA, DS, PA, BA

**Remember it as:** *NumPy divides by n, pandas divides by n − 1. Same data, different answer, and neither tells you.*

**Answer in one line:** **2.000 and 2.138** — NumPy's default is the population standard deviation (`ddof=0`) and pandas' default is the sample one (`ddof=1`), a 6.5% difference on eight numbers and a silent one.

```python
x = [2, 4, 4, 4, 5, 5, 7, 9]
print(f"np.std(x)          = {np.std(x):.6f}")
print(f"np.std(x, ddof=1)  = {np.std(x, ddof=1):.6f}")
print(f"pd.Series(x).std() = {pd.Series(x).std():.6f}")
```

```
np.std(x)          = 2.000000
np.std(x, ddof=1)  = 2.138090
pd.Series(x).std() = 2.138090
```

The divisor is the whole story. The population formula divides the sum of squared deviations by **n**; the sample formula divides by **n − 1**, because using the sample's own mean uses up one degree of freedom and dividing by n would bias the estimate downward.

Which is right depends on your question, not your library. If those eight numbers are the entire population you care about — the eight regions you operate in — `ddof=0` is correct. If they are a sample you are generalising from, `ddof=1` is.

The trap is that the two libraries disagree **by default**, so the same analysis gives two different numbers depending on whether a column arrived as a NumPy array or a pandas Series. On eight numbers that is 6.5%. On 1,000 it is 0.05% and you will never notice — which is worse, because it means the discrepancy only shows up in small-sample work, where it matters most.

It propagates: a confidence interval, a t-statistic and a z-score all contain this number.

| Tier | What to say |
|---|---|
| Passes | "One is the sample standard deviation and one is the population one" |
| Strong | + both figures, which library defaults to which, and that the choice depends on whether the data is a sample or the whole population |
| Extra points | **[+Edge cases]** the gap shrinks as n grows, so it hides in exactly the large datasets where it does not matter and bites in the small ones where it does · **[+Validate]** pass `ddof` explicitly in anything shared, so the reader does not have to know the default · **[+Business]** two analysts reporting different volatility for the same series, both "correct", is usually this |

**Likely follow-ups:** Why n − 1? *(Bessel's correction: the sample mean sits closer to the sample than the true mean does, so deviations are understated.)* What does `.var()` default to in each? *(The same split.)* Does `describe()` use ddof=1? *(Yes, in pandas.)*
**Red flag:** not knowing there is a choice at all.
**Learn it in:** Chapter 21, section 21.3 (spread); Chapter 18, section 18.1 (NumPy).

### Q73-039 · Three days of conversion data. What is the average conversion rate?

**Level:** Mid · **Roles:** DA, DS, PA, BA

**Remember it as:** *The mean of the rates is not the rate. Add the tops and add the bottoms; never average the ratios.*

**Answer in one line:** **10.8%**, not 36.7% — averaging the three daily rates gives each day equal weight regardless of traffic, so two ten-visit days drown out a thousand-visit day.

| Day | Visits | Conversions | Rate |
|---|---|---|---|
| 1 | 10 | 5 | 50.0% |
| 2 | 1,000 | 100 | 10.0% |
| 3 | 10 | 5 | 50.0% |

```python
days = pd.DataFrame({'visits': [10, 1000, 10], 'conversions': [5, 100, 5]})
days['rate'] = days.conversions / days.visits
print(f"mean of the daily rates  : {days.rate.mean():.4f}")
print(f"total conv / total visits: {days.conversions.sum() / days.visits.sum():.4f}")
```

```
mean of the daily rates  : 0.3667
total conv / total visits: 0.1078
```

**36.7% against 10.8%.** The first number is wrong by a factor of three and a half, and it is the one a `groupby(...).mean()` on a rate column produces.

The right calculation sums the numerators and the denominators: 110 conversions out of 1,020 visits. Every row then carries the weight it earned.

This is the single most common arithmetic error in analyst work, because the wrong version is so natural to write — compute a rate per day, then average it. It appears in weighted averages of any kind: average order value across stores, average margin across products, average latency across services. Wherever a per-unit figure is averaged across units of different size, this is waiting.

If you genuinely need the average of the rates — "what does a typical day look like?" — that is a different question and you should say so, because the number answers it and nothing else.

| Tier | What to say |
|---|---|
| Passes | "You should weight by visits" |
| Strong | + both numbers, 36.7% against 10.8%, and the rule: sum the numerators and denominators, do not average the ratios |
| Extra points | **[+Business]** the same error inflates average order value, margin and latency whenever the units differ in size · **[+Clarify]** "average rate" is ambiguous — the pooled rate and the mean of daily rates answer different questions, so ask which · **[+Validate]** if an average rate sits outside the range you would expect from the totals, this is why · **[+Edge cases]** a weighted mean with the denominator as weights gives the pooled figure back, which is a useful cross-check |

**Likely follow-ups:** When would the mean of rates be the right answer? How does this connect to Simpson's paradox? *(Closely — section 73.6 is the same weighting problem with a reversal in it.)* How would you write the pooled version in SQL?
**Red flag:** `df.groupby('day')['rate'].mean()` in a report, with no weighting.
**Learn it in:** Chapter 21, section 21.2 (averages); Chapter 73, section 73.6 (Simpson's paradox); Chapter 23, section 23.6.

### Q73-040 · "95% confidence interval." What is 95% of what?

**Level:** Mid · **Roles:** DA, DS, PA, BA

**Remember it as:** *95% of intervals built this way contain the true value. This one either does or it does not.*

**Answer in one line:** (Q73-019 gives the one-line version; this is the proof.) 95% is the long-run success rate **of the procedure**, not the probability that the parameter is inside the particular interval you are looking at — the parameter is a fixed number, so for any given interval the answer is already yes or no.

```python
rng = np.random.default_rng(73)
true_mu, trials, covered = 100, 5000, 0
for _ in range(trials):
    s = rng.normal(true_mu, 15, 30)
    lo, hi = stats.t.interval(0.95, len(s)-1, loc=s.mean(), scale=stats.sem(s))
    covered += lo <= true_mu <= hi
print(f"{covered/trials*100:.1f}% of {trials:,} intervals contain the true mean")
```

```
94.9% of 5,000 intervals contain the true mean
```

94.9% is what the "95%" refers to. Repeat the whole exercise — draw a sample, build an interval — and about 95 in 100 of those intervals will have captured the true value.

Here is one of them:

```python
rng = np.random.default_rng(73)
s = rng.normal(100, 15, 30)
lo, hi = stats.t.interval(0.95, 29, loc=s.mean(), scale=stats.sem(s))
print(f"[{lo:.2f}, {hi:.2f}]")
```

```
[92.34, 104.03]
```

For *that* interval the probability of containing 100 is not 95%. It is 1, because 100 is in it. Had the sample come out differently it might have been 0. The randomness lives in the sampling, not in the parameter.

Does the distinction matter in practice? Mostly no — and saying so is part of a good answer, rather than pretending the frequentist reading changes your decisions. Where it does matter is in how you talk to stakeholders. "There is a 95% chance the lift is between 2% and 8%" is the Bayesian credible-interval statement, and if you want to make it, use a Bayesian method and say so. With a frequentist interval the honest version is "our method captures the truth 95% of the time, and this is what it gave us."

| Tier | What to say |
|---|---|
| Passes | "It's a range the true value is probably in" |
| Strong | + 95% is a property of the procedure across repeated samples, this interval either contains the value or does not, with the coverage simulation as evidence |
| Extra points | **[+Trade-offs]** a Bayesian credible interval *does* support "95% probability it is in here", which is usually what the stakeholder wanted · **[+Business]** the practical difference is small; the communication difference is not · **[+Edge cases]** coverage is only 95% if the assumptions hold — the simulation above draws from a normal, and real data may not |

**Likely follow-ups:** What makes an interval wider? *(More variance, less data, higher confidence.)* What is a credible interval? If I run 20 experiments, how many intervals miss? *(About one.)*
**Red flag:** "there is a 95% chance the true value is in this interval" stated as the definition. Common, usually harmless, and precisely what the question is checking.
**Learn it in:** Chapter 22, section 22.3 (confidence intervals); Chapter 30, section 30.6.

### Q73-041 · You halve the effect you want to detect. What happens to the sample size?

**Level:** Senior · **Roles:** DA, DS, PA

**Remember it as:** *Sample size goes as one over the effect squared. Half the effect, four times the data.*

**Answer in one line:** (Q73-020 computes a sample size; this is how that number moves.) It roughly **quadruples** — 14,744 per arm to detect a 10% relative lift becomes 57,756 to detect 5%, because the required n scales with 1/effect².

```python
power = sms.NormalIndPower()
for mde in (0.10, 0.05, 0.025):
    es = sms.proportion_effectsize(0.10 + mde * 0.10, 0.10)
    n = power.solve_power(effect_size=es, alpha=0.05, power=0.8, ratio=1)
    print(f"relative MDE {mde*100:>4.1f}%  ->  n per arm = {n:,.0f}")
```

```
relative MDE 10.0%  ->  n per arm = 14,744
relative MDE  5.0%  ->  n per arm = 57,756
relative MDE  2.5%  ->  n per arm = 228,547
```

Each halving multiplies by just under four. Going from a 10% lift to a 2.5% lift — all three of which sound like small numbers in a meeting — multiplies the traffic you need by **fifteen and a half**.

This is the single most useful fact to have ready when someone asks for an experiment, because it converts an ambition into a schedule. At 5,000 visitors a day per arm, detecting a 10% lift takes three days, and detecting a 2.5% lift takes forty-six.

The full relationship, worth being able to state:

| Change | Effect on n |
|---|---|
| Halve the detectable effect | × 4 |
| Raise power from 80% to 90% | × 1.34 |
| Tighten alpha from 0.05 to 0.01 | × 1.49 |
| Halve the baseline rate | roughly × 2 |

The honest conversation that follows is usually the valuable one: either the effect worth detecting is bigger than people claimed, or the test needs to run for two months, or it should not be run as an A/B test at all.

| Tier | What to say |
|---|---|
| Passes | "You need more data" |
| Strong | + "about four times, because n goes as 1/effect²", with a worked number |
| Extra points | **[+Business]** converts directly to calendar time, which is the form the decision actually takes · **[+Trade-offs]** you can buy back sample size with variance reduction (CUPED) or a better unit of randomisation, rather than waiting · **[+Clarify]** ask what lift would actually change the decision; teams routinely ask to detect effects far smaller than they would act on · **[+Edge cases]** the four-times rule is for a difference in means or proportions; ratio metrics with their own variance need the delta method |

**Likely follow-ups:** Where does the square come from? What is CUPED? How does the baseline rate affect it? What if the metric is revenue per user rather than a proportion? *(Much higher variance, so a larger n.)*
**Learn it in:** Chapter 30, section 30.3 (sample size and power); Chapter 22, section 22.4.

### Q73-042 · There is no effect at all. What does the distribution of p-values look like?

**Level:** Senior · **Roles:** DS, PA

**Remember it as:** *Under the null, a p-value is uniform. Every value from 0 to 1 is equally likely — which is exactly why 5% of them land below 0.05.*

**Answer in one line:** **Flat** — p-values are uniformly distributed between 0 and 1 when the null is true, so each 10% band holds about 10% of them, and the 5% false positive rate is not a coincidence but the definition.

```python
rng = np.random.default_rng(73)
ps = np.array([stats.ttest_ind(rng.normal(0, 1, 200), rng.normal(0, 1, 200)).pvalue
               for _ in range(5000)])
for lo in np.arange(0, 1, 0.1):
    print(f"p in [{lo:.1f}, {lo+0.1:.1f}): {((ps >= lo) & (ps < lo+0.1)).mean()*100:5.1f}%")
print(f"p < 0.05: {(ps < 0.05).mean()*100:.1f}%")
```

```
p in [0.0, 0.1):   9.7%
p in [0.1, 0.2):  10.0%
p in [0.2, 0.3):   8.8%
p in [0.3, 0.4):  10.4%
p in [0.4, 0.5):  10.6%
p in [0.5, 0.6):  10.6%
p in [0.6, 0.7):  10.3%
p in [0.7, 0.8):   9.8%
p in [0.8, 0.9):   9.7%
p in [0.9, 1.0):  10.1%
p < 0.05: 5.0%
```

Ten bands, about 10% each, and exactly 5.0% below 0.05.

Two consequences follow, and they are what the question is really after.

**First, a large p-value is not evidence of no effect.** If p were clustered near 1 when nothing was happening, p = 0.8 would be reassuring. It is not — p = 0.8 is exactly as likely as p = 0.1 under the null. Absence of evidence is not evidence of absence, and the tool for the latter is an equivalence test or a confidence interval narrow enough to exclude anything you would care about.

**Second, this is the foundation under Q73-028 and Q73-025.** Multiple comparisons inflate false positives because each test is an independent draw from a uniform distribution, so more draws means more values below 0.05. Peeking, in Q73-025, works the same way: more looks, more draws, more crossings.

It is also a diagnostic. Plot the p-values from a large family of tests you believe are null — your A/A tests, your pre-experiment checks — and the histogram should be flat. A spike near zero means real effects, or a bug in the randomisation. A histogram that is *not* flat under A/A conditions is one of the best signals that your experimentation platform is broken.

| Tier | What to say |
|---|---|
| Passes | "Uniform" |
| Strong | + why that gives the 5% rate by construction, and that a large p-value is therefore not evidence of no effect |
| Extra points | **[+Validate]** an A/A p-value histogram that is not flat means the platform is broken, and is a standard health check · **[+Edge cases]** the uniformity needs a continuous test statistic; discrete tests on small counts give a lumpy distribution · **[+Business]** to argue *for* no effect, use an equivalence test, not a big p-value |

**Likely follow-ups:** What does the distribution look like when there *is* an effect? *(Skewed towards zero, more so with more power.)* How would you test for equivalence? What would a spike at 0.04–0.05 across published studies suggest? *(P-hacking.)*
**Learn it in:** Chapter 22, section 22.4 (p-values); Chapter 30, section 30.5.

### Q73-043 · Four datasets, same mean, same variance, same correlation, same regression line

**Level:** Mid · **Roles:** DA, DS, PA, BA

**Remember it as:** *Summary statistics are a compression, and compression loses things. Plot it.*

**Answer in one line:** They are **completely different** — Anscombe's quartet matches on every summary statistic to two decimal places while containing a straight line, a curve, a line with one outlier, and a vertical stack with one far-off point.

```python
x_common = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
anscombe = {
    'I':   (x_common, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    'II':  (x_common, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    'III': (x_common, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    'IV':  ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
            [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}

print(f"{'set':<5}{'mean x':>8}{'mean y':>8}{'sd y':>7}{'corr':>7}{'slope':>8}")
for k, (xs, ys) in anscombe.items():
    xs, ys = np.array(xs), np.array(ys)
    slope = np.polyfit(xs, ys, 1)[0]
    print(f"{k:<5}{xs.mean():>8.2f}{ys.mean():>8.2f}{ys.std(ddof=1):>7.3f}"
          f"{np.corrcoef(xs, ys)[0,1]:>7.3f}{slope:>8.3f}")
```

```
set    mean x  mean y   sd y   corr   slope
I        9.00    7.50  2.032  0.816   0.500
II       9.00    7.50  2.032  0.816   0.500
III      9.00    7.50  2.030  0.816   0.500
IV       9.00    7.50  2.031  0.817   0.500
```

Identical on every number anyone would put in a summary table. What the numbers do not say:

| Set | What it actually is |
|---|---|
| I | A genuine noisy linear relationship — the only one the statistics describe honestly |
| II | A clean curve. A straight line is the wrong model, and r = 0.816 hides that completely |
| III | A perfect straight line with one outlier, which drags the fitted slope away from the real one |
| IV | Every x is 8 except one. The "correlation" is produced entirely by a single point; delete it and the slope is undefined |

Each set needs a different response: trust the model, change the model, investigate the outlier, get more data. The summary statistics cannot distinguish between them, and neither can anyone who only reads the summary.

This is why "plot the data" is the first step in every cleaning and modelling chapter in this book, and why a correlation coefficient quoted without a scatterplot is a claim rather than evidence.

| Tier | What to say |
|---|---|
| Passes | "It's Anscombe's quartet — you should plot your data" |
| Strong | + describes what the four actually are, and what each one implies you should do differently |
| Extra points | **[+Validate]** the Datasaurus Dozen makes the same point harder: identical statistics, one of them a dinosaur · **[+Business]** set IV is the shape of a metric driven by one big customer, which is common and is a real risk, not a data-quality problem · **[+Edge cases]** set III is why robust regression and Spearman exist |

**Likely follow-ups:** What would Spearman give for each? How would you detect set IV automatically? *(Leverage, or Cook's distance.)* What is the Datasaurus Dozen?
**Learn it in:** Chapter 15, section 15.1 (why plot first); Chapter 22, section 22.10 (regression).

### Q73-044 · Two groups, SE 0.77 and 0.68. What is the standard error of the difference?

**Level:** Senior · **Roles:** DA, DS, PA

**Remember it as:** *Variances add, standard errors do not. Square, add, square-root.*

**Answer in one line:** **1.03**, not 1.45 — variances add for independent groups, so the standard errors combine as √(0.77² + 0.68²); adding them overstates the uncertainty by 41% and hides real effects.

```python
rng = np.random.default_rng(73)
a = rng.normal(100, 15, 400)
b = rng.normal(103, 15, 400)
sea, seb = stats.sem(a), stats.sem(b)
print(f"SE(a) = {sea:.4f}   SE(b) = {seb:.4f}")
print(f"added:       {sea + seb:.4f}")
print(f"root sum sq: {np.sqrt(sea**2 + seb**2):.4f}")
print(f"ratio:       {(sea+seb)/np.sqrt(sea**2+seb**2):.3f}x")
```

```
SE(a) = 0.7742   SE(b) = 0.6790
added:       1.4532
root sum sq: 1.0298
ratio:       1.411x
```

Getting it wrong in this direction is the conservative error — you overstate the uncertainty, your interval is 41% too wide, and you fail to detect effects that are really there. That is better than the opposite, and it is still wrong, and in a test that cost six weeks of traffic it is expensive.

The underlying rule is worth stating as a rule, because it generalises: for independent random variables, **Var(A − B) = Var(A) + Var(B)**. Note the plus: subtracting the means *adds* the uncertainty, which surprises people. You cannot cancel noise by taking a difference.

It stops being true when the groups are not independent. Paired data — the same users before and after — shares variance, and the paired test uses the variance of the per-user *differences*, which is usually much smaller. That is the whole reason paired designs are more powerful, and the reason CUPED works.

| Tier | What to say |
|---|---|
| Passes | "You add the variances, not the standard errors" |
| Strong | + both numbers, that the error is conservative but still wrong, and that it costs you power rather than giving a false positive |
| Extra points | **[+Edge cases]** only for independent groups; paired data uses the variance of the differences and is usually tighter · **[+Business]** a 41% too-wide interval means a real effect reported as "not significant" after six weeks of traffic · **[+Scale]** this is why CUPED reduces variance rather than increasing n, which is far cheaper |

**Likely follow-ups:** What if the groups are paired? Why does subtracting add the variance? What is the SE of a sum? *(The same — variances add either way.)*
**Learn it in:** Chapter 22, section 22.3 (standard errors); Chapter 30, section 30.4.

### Q73-045 · `y = x²` over a symmetric range. What is the correlation between x and y?

**Level:** Mid · **Roles:** DA, DS, PA

**Remember it as:** *Pearson measures straight-line association only. A perfect curve with no straight-line trend scores zero.*

**Answer in one line:** **0.000000** — exactly zero, even though y is completely determined by x, because Pearson correlation measures only the linear component and a symmetric parabola has none.

```python
x = np.linspace(-3, 3, 601)
y = x**2
print(f"Pearson  r = {np.corrcoef(x, y)[0,1]:.6f}")
print(f"Spearman   = {stats.spearmanr(x, y).statistic:.6f}")
print(f"R^2 of y on x**2 = {np.corrcoef(x**2, y)[0,1]**2:.4f}")
```

```
Pearson  r = 0.000000
Spearman   = 0.000674
R^2 of y on x**2 = 1.0000
```

The relationship is perfect — give me x and I will give you y exactly. The correlation is zero.

Spearman does not rescue it either, because Spearman measures *monotonic* association and this relationship is not monotonic: y falls and then rises. Both coefficients are doing their job and both report nothing.

So "r = 0" means **no linear relationship**, and nothing more. It does not mean no relationship, and it certainly does not mean independence. The converse that *is* true: if two variables are independent, their correlation is zero. The implication runs one way only.

The practical move is the one from Q73-043 — plot it. A feature-selection step that drops every feature with low correlation to the target will throw away exactly the U-shaped relationships that matter: the effect of price on volume at the extremes, the effect of time-of-day on traffic, the effect of tenure on churn where both the newest and the longest-tenured customers leave.

| Tier | What to say |
|---|---|
| Passes | "Zero, because it's not linear" |
| Strong | + that Spearman is also near zero because the relationship is not monotonic, and that r = 0 means no *linear* relationship, not independence |
| Extra points | **[+Business]** correlation-based feature selection silently drops U-shaped drivers, which are common — price, tenure, time of day · **[+Trade-offs]** mutual information or distance correlation catch non-linear dependence; a scatterplot catches it faster · **[+Edge cases]** independence implies zero correlation, but not the reverse |

**Likely follow-ups:** What would catch this relationship? What does Spearman measure? Does a tree model care? *(No — trees split on thresholds and handle this naturally.)*
**Learn it in:** Chapter 22, section 22.9 (correlation); Chapter 36, section 36.5 (feature selection).

### Rapid-fire, 73.8, part A: predict the number

Roles: DA, DS and PA for every row unless stated.

| # | Question | The answer, and why | Extra point |
|---|---|---|---|
| Q73-046 | A coin lands heads 5 times running. P(heads) next? | 0.5. The coin has no memory; the gambler's fallacy is believing it does | **[+Edge cases]** if you are unsure the coin is fair, 5 heads *is* evidence it is not — a different question → Ch 21 §21.5 |
| Q73-047 | A test has 80% power. The effect is real. P(you miss it)? | 20%. Power is the chance of detecting a real effect, so 1 − power is the false negative rate | **[+Business]** at 80% power, one real win in five is thrown away → Ch 30 §30.3 |
| Q73-048 | p = 0.03. What is the probability the null is true? | Unknown. p is P(data this extreme \| null), not P(null \| data). Inverting it needs a prior | **[+Validate]** the inversion is the same error as Q73-038 → Ch 22 §22.4 |
| Q73-049 | Median of `[1, 2, 3, 4, 100]`, and the mean? | Median 3, mean 22. One outlier moves the mean by a factor of seven and the median not at all | **[+Business]** report the median for salary, latency and order value → Ch 21 §21.2 |
| Q73-050 | 90th percentile of 10 numbers — which one? | It depends on the interpolation method; numpy has nine, and they disagree on small samples | **[+Edge cases]** quote the method when n is small, or results will not reconcile across tools → Ch 21 §21.3 |
| Q73-051 | Flip a fair coin 10 times. P(exactly 5 heads)? | 24.6%, not 50% — `stats.binom.pmf(5, 10, 0.5)`. The most likely single outcome is still uncommon | **[+Edge cases]** "most likely" and "likely" are different claims → Ch 21 §21.7 |
| Q73-052 | Revenue per user is heavily skewed. Is the t-test still valid? | At large n, yes — the CLT applies to the *mean*, not the data. At small n or with extreme outliers, no | **[+Trade-offs]** trim, wins'orise, or bootstrap; or test a capped metric agreed in advance → Ch 22 §22.6 |
| Q73-053 | Sample size for a proportion at the same relative lift: baseline 10% against 1%? | The 1% baseline needs roughly ten times more, because rare events carry more relative variance | **[+Business]** which is why conversion tests on rare actions rarely finish → Ch 30 §30.3 |
| Q73-054 | A/B test, p = 0.049 against p = 0.051. How different are the findings? | Essentially identical. The threshold is a convention, not a boundary in nature | **[+Trade-offs]** report the effect size and interval; the decision rarely hinges on the third decimal → Ch 22 §22.4 |

### Rapid-fire, 73.8, part B: experiment arithmetic

| # | Question | The answer, and why | Extra point |
|---|---|---|---|
| Q73-055 | Control 10.0%, variant 10.5%. Absolute and relative lift? | +0.5 percentage points, +5% relative. Confusing the two overstates or understates by 20× at this baseline | **[+Business]** always say which; "5% lift" is ambiguous and expensive → Ch 23 §23.6 |
| Q73-056 | Test wins at 5% lift. What will you see in production? | Less, usually. The winner's curse: conditioning on significance selects for overestimates, worse at low power | **[+Edge cases]** shrink the estimate, or hold out a slice to measure the real effect → Ch 30 §30.7 |

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Reading a "99% sensitive" test as "99% chance you have it" | Wildly overestimating a positive result's reliability on a rare condition | Always ask for the base rate; run Bayes' theorem (Q73-005) |
| Defining a p-value as "probability the null is true" | Confidently wrong explanations to stakeholders | It's the probability of the *data*, assuming the null, never the reverse |
| Treating "not significant" as "no effect" | Shipping decisions based on an underpowered test's false negative | Check power before concluding there's no effect (Q73-015) |
| Skipping a sample-size calculation before running a test | A test that ends inconclusive, or runs far longer than needed | Compute required sample size from baseline, MDE, alpha, and power (Q73-020) |
| Checking significance daily and stopping at the first p < 0.05 | A real, inflated false-positive rate far above the stated 5% | Pre-commit to a sample size and check date, or use a sequential method (Q73-025) |
| Ignoring a skewed traffic split as "probably fine" | Trusting results from a broken randomization pipeline | Run a chi-square SRM check before trusting anything else (Q73-026) |
| Ranking groups on an aggregate rate with very different underlying mixes | A real Simpson's paradox reversal going unnoticed | Always check subgroup rates before trusting an aggregate comparison (Q73-031) |
| Citing a strong correlation as if it were causal | Acting on a relationship driven entirely by a confounder | Look for (and control for) a plausible confounder before any causal claim (Q73-032) |

---

## In the real world: the A/B test that was actually broken plumbing

Farah, running a pricing experiment at a mid-size company, sees a strong, statistically significant lift in the treatment group after ten days and is ready to recommend shipping it. Before doing so, she runs the sample-ratio check (Q73-026), almost as a formality: and gets a real SRM: 5,340 users in control against 4,660 in treatment, a split that shouldn't happen by chance at that scale.

She doesn't ship the pricing change. She traces the mismatch and finds that the treatment variant's page loaded slightly slower, and a fraction of mobile users on slower connections were timing out before the assignment even completed, silently dropping out of the treatment group specifically. Those dropped users, it turns out, were disproportionately price-sensitive mobile shoppers, exactly the segment least likely to convert. The "lift" wasn't from the new pricing at all; it was from quietly excluding the users least likely to buy.

The fix took two days: a loading-performance bug, unrelated to pricing entirely. The re-run test, with the SRM resolved, showed no significant pricing effect at all. Farah's manager's reaction was the right one: relief that the SRM check happened before the change shipped, not after, when the "successful" pricing test would have been cited as evidence for a change that did nothing, while the real bug (a broken experience for a whole segment of mobile users) went unnoticed and unfixed.

---

## Project

**Goal:** run, not just read, this chapter's core demonstrations on your own numbers.

### Tools you'll need

**Python** with **SciPy** (`scipy.stats`) and **statsmodels** (`statsmodels.stats.api`), both free and both already in your Chapter 17 environment (installed in Chapter 21, section 21.5 and Chapter 22, section 22.2), used throughout this chapter for every simulation, test statistic, and sample-size calculation. **R** offers equivalent functionality (`prop.test`, `power.t.test`, `chisq.test`) and is common in some analytics teams; the underlying statistics are identical regardless of language. Everything in this chapter ran on Python 3.11.15 with NumPy 2.4.6, SciPy 1.17.1, statsmodels 0.15.0 and pandas 3.0.6 (the book recommends Python 3.14, Chapter 17, section 17.0); a recent SciPy and statsmodels should give the same numbers to three decimals.

1. Compute Bayes' theorem for a real base-rate scenario from your own work (a fraud flag, a churn flag, a quality-control test) and see how far the "accuracy" number is from the true positive-predictive value.
2. Run a real sample-size calculation for an A/B test you'd actually want to run, using your own baseline rate and a business-justified MDE.
3. Simulate the peeking problem yourself (or reason through why it happens) on a metric relevant to your own work.
4. Find (or construct) a Simpson's paradox in your own data: two groups, a category where the aggregate ranking reverses the subgroup rankings.
5. Take one correlation you've observed in your own work and name a plausible confounder, then say how you'd check whether it explains the relationship.

---

## Key terms

Bayes' theorem · base rate · sensitivity · false-positive rate · natural frequencies · conditional probability · Monty Hall problem · birthday problem · independent vs. mutually exclusive events · expected value · Binomial distribution · Poisson distribution · Central Limit Theorem · variance · standard deviation · Normal / log-normal distribution · heavy-tailed distribution · p-value · null hypothesis · Type I error · Type II error · statistical power · t-test vs. z-test · confidence interval · minimum detectable effect (MDE) · Cohen's h · randomization · one-tailed vs. two-tailed test · holdout group · peeking (repeated significance testing) · Sample Ratio Mismatch (SRM) · novelty effect · multiple comparisons · Bonferroni correction · network effect (interference) · Simpson's paradox · confounder · partial correlation · residual · selection bias · natural experiment · Yates' continuity correction · winner's curse · `ddof` (degrees of freedom) · Bessel's correction · population against sample standard deviation · pooled rate · mean of ratios against ratio of means · weighted average · coverage · uniform distribution of p-values · equivalence test · Anscombe's quartet · leverage · variance of a difference · paired design · CUPED · Pearson against Spearman · monotonic association · percentile interpolation method

---

## Final-week revision list

Q73-005, Q73-006, Q73-007, Q73-008, Q73-009, Q73-014, Q73-015, Q73-016, Q73-017, Q73-019, Q73-020, Q73-021, Q73-025, Q73-026, Q73-028, Q73-031, Q73-032, Q73-036, Q73-037, Q73-038, Q73-039, Q73-042.

The last three are the arithmetic that most often reaches a slide uncorrected: the `ddof` split between NumPy and pandas (Q73-038), averaging rates instead of pooling them (Q73-039), and what a flat p-value distribution tells you about your own platform (Q73-042).

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 71, SQL Question Bank,** already covered the mechanics of building the aggregated tables (retention counts, group-by rates) that feed many of this chapter's tests.
- **Chapter 74, Machine Learning Question Bank,** builds on this chapter's hypothesis testing and base-rate reasoning (Q73-005) for model evaluation.
- **Chapters 21 and 22** (probability, distributions, the two famous puzzles in section 21.7, and tests), **Chapter 30** (inference and experiments) and **Chapter 31** (causal inference without experiments) teach what this bank draws on; this chapter tests it, it doesn't re-teach it. The few ideas marked Beyond the book (log-normal data, holdout groups, partial correlation, the winner's curse) are explained where they appear.
