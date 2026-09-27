# Chapter 73. Statistics, Probability & Experimentation Bank

*Part VIII — The Interview Playbook*

> **You will learn to:** answer probability puzzles that show up across every data role's interviews, and explain *why* the surprising answer is correct, not just what it is · reason correctly about distributions, p-values, and confidence intervals, including the ways almost everyone misinterprets them at first · design an A/B test's sample size before running it, and debug one that's already gone wrong · spot Simpson's paradox and correlation-masquerading-as-causation in real-looking data.
>
> **How this chapter is built.** Same format as Chapters 70–72A: every core question leads with a **"Remember it as…"** hook, a one-line answer, a compact tier table. Rapid-fire sections are scan tables. **Every numeric claim in this chapter was computed by running real Python (NumPy, SciPy, statsmodels), not recalled from memory or asserted**: simulations, real test statistics, real p-values, real sample-size calculations. Section order was planned before writing, not fixed afterward: basics first, puzzles right after (since they test the same basics from an angle), then testing, then experimentation design and debugging, then causal reasoning, then integrative walkthroughs.
>
> **Learn it in** pointers are at chapter level (this chat doesn't have this book's statistics/experimentation/causal-inference chapters' approved text to check exact section numbers against: flagged for a re-check once available, the same convention used for Chapters 10, 11, 16, and 19 elsewhere in this part).

---

## 73.1 Core probability concepts

### Q73-001 · Explain Bayes' theorem, and why "95% accurate" doesn't mean what most people assume

**Remember it as:** *A rare disease and an imperfect test: even a good test is mostly wrong about rare things, because there are so many more healthy people to false-positive on than sick people to correctly catch.*

**Answer in one line:** Bayes' theorem updates a prior probability using new evidence: `P(A|B) = P(B|A) × P(A) / P(B)`, and it matters most when the thing you're testing for is rare, because the base rate can overwhelm even a very accurate test.

**Verified, live:** a disease with 1% prevalence, a test that's 99% sensitive (catches 99% of true cases) and has a 5% false-positive rate:

```python
p_disease = 0.01
p_pos_given_disease = 0.99
p_pos_given_no_disease = 0.05

p_positive = p_pos_given_disease * p_disease + p_pos_given_no_disease * (1 - p_disease)
p_disease_given_positive = (p_pos_given_disease * p_disease) / p_positive
```
```
P(positive) = 0.0594
P(disease | positive) = 0.1667
```

Someone testing positive on a "99% accurate" test actually has the disease only **16.7%** of the time.

| Tier | What to say |
|---|---|
| Passes | States the formula correctly, can't apply it to a concrete number |
| Strong | Works through the disease example above, arriving at 16.7%, and explains *why* it's so much lower than 99%: the 5% false-positive rate applies to the 99% of people who are healthy, a much bigger group than the 1% who are sick |
| Extra points | + **[Validate]** the real computed numbers above, not a remembered rule of thumb + **[Business]** this exact reasoning is why a fraud-detection or churn-flagging model's "95% accurate" claim needs the base rate before it means anything, exactly Chapter 39's evaluation discipline, here traced back to its probability root |

**Likely follow-ups:** How would a higher-prevalence disease change the answer? What test characteristic matters more for a rare event, sensitivity or specificity?
**Red flag:** stating "99% accurate test → 99% chance of having the disease" as if they were the same number.
**Learn it in:** Chapter 21 or nearby (statistics foundations; exact number to confirm).

### Q73-002 · Walk through the Monty Hall problem, and prove your answer

**Remember it as:** *The host's choice isn't random: he always avoids the car. That single fact is why switching wins twice as often.*

**Answer in one line:** Switching doors wins the car **2/3** of the time; staying wins only **1/3**: because the host's forced choice (he always opens a goat door, never the car) concentrates the other 2/3 probability onto the one remaining unopened door.

**Verified, live, by simulation (100,000 trials):**
```python
rng = np.random.default_rng(73)
wins_switch = wins_stay = 0
for _ in range(100_000):
    car = rng.integers(0, 3)
    choice = rng.integers(0, 3)
    remaining = [d for d in range(3) if d != choice and d != car]
    host_opens = rng.choice(remaining) if len(remaining) > 1 else remaining[0]
    switch_choice = [d for d in range(3) if d != choice and d != host_opens][0]
    wins_stay += (choice == car)
    wins_switch += (switch_choice == car)
```
```
stay wins:   0.332
switch wins: 0.668
```

| Tier | What to say |
|---|---|
| Passes | States "switching is better" from memory, can't explain why |
| Strong | The reasoning: your original pick has a 1/3 chance of being right; the other two doors together have a 2/3 chance; once the host removes one (always a goat, never the car), that whole 2/3 collapses onto the single remaining door |
| Extra points | + **[Validate]** a real 100,000-trial simulation landing almost exactly on the theoretical 1/3 and 2/3 + **[Depth]** the key, often-missed detail: this only works because the host's action is *not* random: he has certain knowledge and always avoids the car; if he opened a random unopened door and it happened to reveal a goat, switching would no longer help |

**Likely follow-ups:** What if there were 100 doors instead of 3? What changes if the host sometimes opens the car by accident?
**Red flag:** claiming it's 50/50 after one door is removed, the single most common wrong answer to this exact question.
**Learn it in:** Chapter 21 or nearby.

### Q73-003 · The birthday problem: how many people need to be in a room before it's more likely than not that two share a birthday?

**Remember it as:** *It's not about matching one specific date: it's about how many *pairs* of people exist, and pairs grow far faster than people do.*

**Answer in one line:** Just **23** people, computed as 1 minus the probability that all birthdays are distinct.

**Verified, live:**
```python
def birthday_prob(n):
    p_no_match = 1.0
    for i in range(n):
        p_no_match *= (365 - i) / 365
    return 1 - p_no_match
```
```
23 people: 0.5073
50 people: 0.9704
70 people: 0.9992
```

| Tier | What to say |
|---|---|
| Passes | Guesses a much larger number (180, "half of 365" is the most common wrong intuition) |
| Strong | Correctly says 23, and explains the pairs insight: with 23 people there are `23 × 22 / 2 = 253` distinct pairs, each a chance for a shared birthday, and 253 chances is a lot even at low odds per pair |
| Extra points | + **[Validate]** the real computed curve above: from 50% at 23 people to over 99.9% at 70 + **[Business]** this exact "how many pairwise comparisons exist" reasoning is why testing 20 unrelated metrics in an A/B test (§73.7) racks up false positives fast: many pairs, many chances, even at low odds each |

**Likely follow-ups:** What's the exact formula, not just the simulation/loop? How does the answer change for a 50% chance of *three* people sharing a birthday?
**Red flag:** answering close to 183 (half of 365), confusing "matching one specific date" with "any two people matching each other."
**Learn it in:** Chapter 21 or nearby.

### Rapid-fire, 73.1

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q73-004 | Independent vs. mutually exclusive events? | Independent: one doesn't affect the other's probability / mutually exclusive: they can't both happen | **[Edge cases]** two mutually exclusive events with nonzero probability are automatically *not* independent: one happening tells you the other definitely didn't |
| Q73-005 | What's the difference between P(A and B) and P(A or B)? | `P(A)×P(B)` if independent / `P(A)+P(B)-P(A and B)` always | **[Edge cases]** forgetting to subtract the overlap in "or" is the single most common probability arithmetic mistake |
| Q73-006 | What's a conditional probability, in one sentence? | The probability of A, given that B is already known to be true: `P(A\|B)` | **[Business]** almost every real business probability question is secretly conditional ("what's the chance this customer churns" really means "given what we know about them") |
| Q73-007 | Expected value of a fair six-sided die roll? | `(1+2+3+4+5+6)/6 = 3.5`: a value the die itself can never actually show | **[Edge cases]** expected value doesn't have to be a possible outcome; it's a long-run average, not a prediction for one roll |

---

## 73.2 Distributions

### Q73-008 · When would you use a Binomial distribution vs. a Poisson distribution?

**Remember it as:** *Binomial counts successes out of a known, fixed number of tries. Poisson counts events with no fixed "number of tries" at all, just a rate over time or space.*

**Answer in one line:** Binomial models the count of successes in a fixed number of independent yes/no trials (10 coin flips, 100 leads contacted); Poisson models the count of events in a fixed interval when there's no natural "number of trials," only an average rate (customer support tickets per hour, defects per meter of cable).

| Tier | What to say |
|---|---|
| Passes | "Binomial is for two outcomes, Poisson is for counting things" |
| Strong | The trials-vs-rate distinction above, with a concrete example of each |
| Extra points | + **[Depth]** Poisson is actually the limiting case of Binomial as the number of trials grows very large and the per-trial probability gets very small, while their product (the expected count) stays fixed: the two aren't unrelated, one is a special-case simplification of the other + **[Business]** a support team staffing model, "how many tickets will arrive in the next hour," is a textbook Poisson use case; "what fraction of these 500 leads will convert" is Binomial |

**Likely follow-ups:** What does the Poisson distribution's single parameter (λ) represent? When does Binomial start to look like a Normal distribution?
**Red flag:** treating the two as interchangeable, or not knowing which applies to a described scenario.
**Learn it in:** Chapter 21 or nearby.

### Q73-009 · State the Central Limit Theorem in plain English, and say why it matters even if your underlying data isn't normally distributed

**Remember it as:** *It doesn't matter what shape the data is. Average enough of it together, and the average's own distribution becomes bell-shaped anyway.*

**Answer in one line:** The Central Limit Theorem says that the distribution of a *sample mean* approaches a Normal distribution as sample size grows, regardless of the shape of the underlying data it's drawn from: which is why so much of statistics (t-tests, confidence intervals) can lean on Normal-distribution math even when real-world data (revenue, wait times) is skewed, not bell-shaped at all.

| Tier | What to say |
|---|---|
| Passes | "Averages tend to be normal" (true, no mechanism, no "why it matters") |
| Strong | + explicitly separates the individual data points (which can be any shape) from the *sample mean's* distribution (which becomes Normal), and connects this to why t-tests and z-tests are valid on skewed real-world data as long as the sample is reasonably large |
| Extra points | + **[Business]** this is exactly why Chapter 71's real revenue data (heavily right-skewed, a few huge orders) can still be safely compared between two groups with a t-test on the *means*, even though the raw order values themselves look nothing like a bell curve + **[Edge cases]** "large enough" sample size depends on how skewed the underlying data is; a very heavy-tailed distribution needs a bigger sample before the CLT's approximation is trustworthy |

**Likely follow-ups:** How large does a sample need to be for CLT to "kick in"? What happens to inference if you ignore CLT and the sample is too small?
**Red flag:** claiming the underlying *data* becomes normal, rather than the sample *mean's* distribution.
**Learn it in:** Chapter 21 or nearby.

### Rapid-fire, 73.2

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q73-010 | What does a distribution's variance measure? | The average squared distance of values from the mean: how spread out the data is | **[Edge cases]** squaring means variance is in squared units (₹² for revenue); standard deviation (variance's square root) is back in the original, interpretable units |
| Q73-011 | Normal vs. log-normal distribution: when does each apply? | Symmetric, bell-shaped data / data that's the *exponential* of something normal, common for values that can't go negative and are right-skewed (revenue, wait times) | **[Business]** most real business "amount" data (order value, salary, session length) is closer to log-normal than Normal: check before assuming symmetry |
| Q73-012 | What's a uniform distribution, and give one real business example? | Every outcome in a range is equally likely | **[Business]** the position of a random number generator's seed, or a truly random A/B assignment before any group differences emerge |
| Q73-013 | What does "long-tailed" or "heavy-tailed" mean? | Extreme values occur more often than a Normal distribution would predict | **[Edge cases]** heavy-tailed data can make sample means unstable and confidence intervals misleadingly narrow if treated as Normal without checking |

---

## 73.3 Hypothesis testing fundamentals

### Q73-014 · Explain a p-value to a non-technical stakeholder, without saying "probability that the null hypothesis is true"

**Remember it as:** *A p-value answers "how surprising is this result, if nothing real were going on?" It never answers "how likely is it that something real is going on?"*

**Answer in one line:** A p-value is the probability of seeing a result at least as extreme as what you observed, *if the null hypothesis were actually true*: it's a statement about how surprising your data is under "nothing changed," not a statement about the probability that something changed.

| Tier | What to say |
|---|---|
| Passes | "It tells you if the result is significant" (technically true, doesn't explain the mechanism, invites the classic misreading) |
| Strong | The correct definition above, explicitly distinguishing it from "probability the null hypothesis is true," which is the single most common misinterpretation |
| Extra points | + **[Business]** a non-technical framing that avoids the trap: "if our change actually did nothing, we'd see a result this extreme only 3% of the time by chance, which is why we're treating it as a real effect" + **[Edge cases]** a p-value says nothing about the *size* of an effect, only its surprise value under the null: a tiny, practically meaningless effect can still have a very small p-value with enough data |

**Likely follow-ups:** What's the difference between statistical significance and practical significance? Why is p < 0.05 the conventional threshold, and is it always the right one?
**Red flag:** defining a p-value as "the probability the null hypothesis is true" or "the probability the result is due to chance," both common, both wrong.
**Learn it in:** Chapter 21 or nearby.

### Q73-015 · Demonstrate that underpowered tests miss real effects far more often than people expect

**Remember it as:** *A small sample doesn't just make you less sure: it makes you actively likely to miss a real, meaningful effect entirely.*

**Answer in one line:** With a real effect but too small a sample, a test's **Type II error rate** (missing a real effect) can be dramatically higher than most people's intuition suggests, and it falls sharply as sample size grows.

**Verified, live:** a true underlying difference of 0.3 standard deviations, tested with a standard t-test, 2,000 simulated experiments at each sample size:

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
    print(n, misses / 2000)
```
```
n=30 per group:  Type II error rate = 0.800
n=200 per group: Type II error rate = 0.138
```

With only 30 people per group, a real effect is **missed 80% of the time**: the test says "no significant difference" four times out of five, even though a real difference genuinely exists. At 200 per group, that drops to 13.8%.

| Tier | What to say |
|---|---|
| Passes | "Bigger samples are more reliable" (true, no sense of *how much* more reliable) |
| Strong | Explains Type II error and power correctly, and that underpowered tests systematically under-detect real effects, not just "add noise" |
| Extra points | + **[Validate]** the dramatic real numbers above: 80% miss rate collapsing to 14% from sample size alone, nothing else changed + **[Business]** a team that runs an underpowered A/B test and concludes "no effect" when there actually was one has made a real, costly, invisible mistake, not a safe, conservative call: this is exactly why sample-size planning (§73.5) happens *before* a test runs, not after |

**Likely follow-ups:** What's the relationship between power, effect size, sample size, and significance level? How do you choose a target power before running a test?
**Red flag:** treating "not statistically significant" as proof "there's no effect," rather than "we may not have had enough data to detect one."
**Learn it in:** Chapter 21/30 or nearby (statistics and experimentation).

### Rapid-fire, 73.3

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q73-016 | Type I vs. Type II error? | Rejecting a true null (a false alarm) / failing to reject a false null (a miss) | **[Business]** which error costs more depends on context: a fraud check favors avoiding Type II (missing real fraud); a drug side-effect check favors avoiding Type I (a false alarm halting a good drug) |
| Q73-017 | What's statistical power? | The probability of correctly detecting a real effect when one exists, i.e. `1 - Type II error rate` | **[Business]** 80% power is the conventional target, meaning you accept a 1-in-5 chance of missing a real effect even when your test is well-designed |
| Q73-018 | t-test vs. z-test, when does it matter which you use? | t-test for an unknown population standard deviation (the usual real-world case, estimated from the sample); z-test when the true population standard deviation is actually known | **[Edge cases]** with a large sample, the t-distribution converges to the normal distribution anyway, so the practical difference shrinks as n grows |
| Q73-019 | What does a 95% confidence interval actually mean? | If you repeated the sampling process many times, 95% of the resulting intervals would contain the true population value | **[Edge cases]** it does *not* mean "95% probability the true value is in this specific interval": the true value either is or isn't in any single interval; the 95% describes the *procedure's* long-run reliability |

---

## 73.4 A/B test design

### Q73-020 · Calculate the required sample size for an A/B test, before running it

**Remember it as:** *You need four numbers before you can answer "how many": baseline rate, the smallest change worth detecting, your significance level, and your desired power.*

**Answer in one line:** Sample size depends on the baseline conversion rate, the **minimum detectable effect (MDE)** you actually care about, the significance level (usually 0.05), and the desired power (usually 0.80): smaller effects and higher confidence both require larger samples.

**Verified, live:** baseline conversion 9.6%, wanting to detect a rise to 10.9% (a realistic MDE), at 80% power:

```python
import statsmodels.stats.api as sms
effect_size = sms.proportion_effectsize(0.096, 0.109)
n_required = sms.NormalIndPower().solve_power(effect_size, power=0.8, alpha=0.05, ratio=1)
```
```
Required sample size per group: 8,537
```

| Tier | What to say |
|---|---|
| Passes | "You need a big enough sample" with no method for computing it |
| Strong | Names the four required inputs, and correctly identifies that MDE is a *business* decision (how small a change is still worth caring about), not a purely statistical one |
| Extra points | + **[Validate]** the real computed number above, 8,537 per group, not a guessed round number + **[Business]** this number directly answers "how long will this test need to run," by dividing 8,537 by expected daily traffic per arm: the single most common follow-up question from a stakeholder, and one this calculation answers directly |

**Likely follow-ups:** How does the required sample size change if the MDE gets smaller (harder to detect)? What if traffic is limited, how would you trade off test duration against detectable effect size?
**Red flag:** picking a sample size arbitrarily ("let's run it for two weeks") with no power calculation behind it.
**Learn it in:** Chapter 30.

### Q73-021 · What's a Minimum Detectable Effect (MDE), and who should decide it?

**Remember it as:** *MDE isn't a statistics question. It's "how small a change would we actually act on?": a business question dressed in statistical clothing.*

**Answer in one line:** The MDE is the smallest true effect size a test is designed to reliably detect; choosing too small an MDE demands an impractically large sample, while choosing too large a one risks missing real, meaningful improvements that are just below the threshold.

| Tier | What to say |
|---|---|
| Passes | "It's the effect size you're testing for" (correct, misses who should set it and why) |
| Strong | + explicitly: the MDE should come from the business ("would we actually change anything for a 0.5 percentage point lift? For 2 points?"), not be back-calculated from whatever sample size happens to be convenient |
| Extra points | + **[Business]** setting the MDE by working backward from "what sample size can we get in two weeks" instead of forward from "what change would we actually act on" is a common, subtle mistake: it optimizes for a schedule, not for a decision worth making + **[Edge cases]** an MDE set too small can make a test run for months chasing statistical significance on an effect too tiny to matter commercially even if proven real |

**Likely follow-ups:** How would you choose an MDE with no historical baseline data at all? What happens if the observed effect is smaller than the MDE but still "significant"?
**Red flag:** treating MDE as a purely mathematical input with no connection to what the business would actually do differently.
**Learn it in:** Chapter 30.

### Rapid-fire, 73.4

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q73-022 | Why randomize which users see which variant? | Randomization is what makes the two groups comparable on everything else (known and unknown factors alike), so any observed difference can be attributed to the treatment | **[Depth]** this is the entire logic of a controlled experiment versus an observational comparison (§73.8): randomization is what earns the right to say "caused," not just "correlated" |
| Q73-023 | One-tailed vs. two-tailed test, when would you use each? | One-tailed tests only for an effect in one specific direction; two-tailed tests for either direction | **[Edge cases]** using a one-tailed test to make a marginal result "significant" after seeing the data is a form of p-hacking; the choice should be made before looking at results, based on whether a decrease genuinely wouldn't matter |
| Q73-024 | What's a holdout group, and why keep one even after shipping a winning test? | A group deliberately excluded from a rollout, to measure the change's real ongoing impact against a true baseline | **[Business]** without a holdout, a genuinely working feature's impact becomes impossible to separate from seasonal trends or other changes happening at the same time |

---

## 73.5 A/B test debugging

### Q73-025 · A dashboard shows a "statistically significant" result after checking it daily throughout the test. What's wrong, and prove it?

**Remember it as:** *Checking significance every day and stopping the moment it looks good is like flipping a coin until it lands on heads, then calling the coin biased.*

**Answer in one line:** Checking for significance repeatedly and stopping as soon as p < 0.05 appears (**"peeking"**) inflates the true false-positive rate far above the nominal 5%, because each additional look is another chance for random noise to cross the threshold.

**Verified, live:** 2,000 simulated experiments, **no real effect at all** (both groups drawn from the identical distribution), checked every 20 new observations for 10 checks:

```python
false_positives = 0
for _ in range(2000):
    data_a, data_b = [], []
    found_sig = False
    for _ in range(10):
        data_a.extend(rng.normal(0, 1, 20)); data_b.extend(rng.normal(0, 1, 20))
        if len(data_a) >= 40:
            t, p = stats.ttest_ind(data_a, data_b)
            if p < 0.05:
                found_sig = True; break
    false_positives += found_sig
```
```
false positive rate with repeated peeking: 0.163   (nominal alpha was 0.05)
```

With **no real effect whatsoever**, repeatedly peeking and stopping at the first significant-looking result gives a false "win" **more than 3 times as often** as the stated 5% significance level promises.

| Tier | What to say |
|---|---|
| Passes | "You shouldn't check too often" (correct instinct, no quantified reason) |
| Strong | Explains the mechanism: each check is another roll of the dice against a 5% threshold, and repeated rolls compound the chance of a false positive somewhere along the way |
| Extra points | + **[Validate]** the real, striking simulated number above: 16.3% actual false-positive rate against a claimed 5%, from peeking alone, on data with zero true effect + **[Business]** the fix isn't "never check early," it's using a sequential testing method (group sequential design, or Bayesian methods designed for continuous monitoring) that's built to allow early looks without inflating the error rate: or committing to a single, pre-planned sample size and analysis date and holding to it |

**Likely follow-ups:** What's a sequential testing correction, in concept? How would you explain this risk to a PM who wants a "quick check" on day 2 of a two-week test?
**Red flag:** not recognizing peeking as a real statistical problem, treating it as a minor process nitpick.
**Learn it in:** Chapter 30.

### Q73-026 · An A/B test's traffic split is supposed to be 50/50, but you're seeing 5,200 vs. 4,800. Is that a problem?

**Remember it as:** *A Sample Ratio Mismatch is a smoke alarm for the whole experiment, not a statistics problem to explain away.*

**Answer in one line:** Run a chi-square goodness-of-fit test against the expected 50/50 split; if it's significant, you have a **Sample Ratio Mismatch (SRM)**, which almost always means something is broken in how users were assigned to groups, not real random variation, and the experiment's other results shouldn't be trusted until it's found and fixed.

**Verified, live, two scenarios:**
```python
chi2, p = stats.chisquare([5200, 4800], [5000, 5000])
```
```
observed [5200, 4800]: chi2 = 16.000, p = 0.0001   -> real SRM, investigate immediately
observed [5100, 4900]: chi2 = 4.000,  p = 0.0455   -> borderline, worth watching closely
```

| Tier | What to say |
|---|---|
| Passes | "That's probably just random variation, it's close to 50/50" |
| Strong | Runs the chi-square test rather than eyeballing it, and correctly treats a significant result as a red flag about the experiment's plumbing, not a metric to report on |
| Extra points | + **[Validate]** the real test: the 5,200/4,800 split is a genuine, significant SRM (p = 0.0001), while the smaller 5,100/4,900 split sits right at the edge (p = 0.0455): a real illustration that "looks close to 50/50" and "is actually statistically expected under 50/50" are different questions + **[Business]** common real causes: a bug in the randomization code, a caching layer serving one variant more, bot traffic disproportionately hitting one arm, or a redirect that silently drops some users from one variant before they're even counted |

**Likely follow-ups:** If you find an SRM, do you throw out the whole test? How would you debug which stage of the pipeline caused it?
**Red flag:** treating a skewed split as a minor curiosity rather than a signal the whole experiment's data may be unreliable.
**Learn it in:** Chapter 30.

### Rapid-fire, 73.5

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q73-027 | What's a novelty effect in an A/B test? | Users react to a change simply because it's *new*, not because it's actually better, and the effect fades over time | **[Business]** a test that shows a strong early lift can be entirely novelty; running long enough to see the effect stabilize (or a holdout, Q73-024) separates the two |
| Q73-028 | Why test 20 different success metrics in one experiment problematic? | Multiple comparisons: testing many unrelated metrics multiplies the chance that at least one looks "significant" purely by chance | **[Validate]** verified live: testing 20 truly unrelated metrics with no real effects, `P(at least one false positive) = 0.634`, matching the theoretical `1 − 0.95²⁰ = 0.642` almost exactly |
| Q73-029 | What's a Bonferroni correction, in one sentence? | Divide the significance threshold by the number of comparisons, so the *combined* false-positive risk across all of them stays at the original level | **[Trade-offs]** simple and conservative, but it can make genuinely real effects harder to detect (lower power) when many comparisons are tested at once |
| Q73-030 | What's a network effect / interference problem in A/B testing? | When a treated user's behavior affects a control user's outcome (e.g., a social feature, a marketplace with shared inventory), violating the assumption that groups are independent | **[Business]** standard A/B math assumes no spillover between groups; a marketplace or social feature test may need a different design (geographic or time-based splitting) to avoid contaminating the control group |

---

## 73.6 Causal inference and Simpson's paradox

### Q73-031 · Construct a real Simpson's Paradox: show two sales reps, each individually better in every category, yet one appears worse overall

**Remember it as:** *When the group sizes are unbalanced across categories, "better in every group" and "better overall" can point in opposite directions at the same time.*

**Answer in one line:** Simpson's paradox occurs when a trend present in every subgroup reverses when the subgroups are combined, because the subgroups are weighted very differently in size.

**Verified, live:**
```python
rep_a = {"easy": (9, 10), "hard": (30, 100)}     # (won, total)
rep_b = {"easy": (80, 100), "hard": (2, 10)}
```
```
Rep A: easy 90% (9/10),   hard 30% (30/100)
Rep B: easy 80% (80/100), hard 20% (2/10)

Rep A overall: 35.5% (39/110)
Rep B overall: 74.5% (82/110)
```

**Rep A wins both categories** (90% beats 80% on easy leads; 30% beats 20% on hard leads) **but Rep B's overall win rate is more than double Rep A's** (74.5% vs. 35.5%). The reversal happens because Rep A worked mostly hard leads (where everyone's rate is lower) and Rep B worked mostly easy leads (where everyone's rate is higher): the mix, not the skill, is driving the overall number.

| Tier | What to say |
|---|---|
| Passes | Can define Simpson's paradox abstractly, can't construct or recognize a real example |
| Strong | The worked example above, correctly identifying that unequal group sizes (Rep A mostly on hard leads, Rep B mostly on easy ones) is the mechanism, not some statistical trick |
| Extra points | + **[Validate]** the real, checkable numbers above, both the subgroup rates and the reversed overall rates + **[Business]** this is exactly why comparing two sales reps', two ad campaigns', or two hospitals' raw overall success rates can be actively misleading if their underlying mix of harder and easier cases differs: always check the subgroup breakdown before ranking on an aggregate number |

**Likely follow-ups:** How would you fix the comparison to be fair? *(Compare like-for-like within each category, or weight by a standardized mix: the same logic behind a standardized/risk-adjusted rate.)* Can you think of a real Simpson's paradox from your own work?
**Red flag:** not recognizing that the paradox is *always* about the mix/weighting, not about the individual category numbers being wrong.
**Learn it in:** Chapter 22 or nearby (causal inference).

### Q73-032 · A strong correlation between website logins and revenue disappears almost entirely once you control for account size. What happened?

**Remember it as:** *A confounder is a hidden variable pulling the strings on both sides of a correlation you're looking at.*

**Answer in one line:** Account size is a **confounder**: bigger accounts naturally log in more *and* naturally generate more revenue, creating a strong correlation between logins and revenue that has nothing to do with logins actually driving revenue.

**Verified, live:**
```python
account_size = rng.uniform(1, 10, 200)
logins = account_size * 2 + rng.normal(0, 2, 200)
revenue = account_size * 50000 + rng.normal(0, 20000, 200)

r_raw, _ = stats.pearsonr(logins, revenue)
r_partial = partial_corr(logins, revenue, account_size)   # controlling for account_size
```
```
raw correlation(logins, revenue)          = 0.922
partial correlation, controlling for size = 0.029
```

The raw correlation of **0.92** (very strong) collapses to essentially **zero (0.03)** once account size is accounted for, in data that was constructed with *no direct causal link* between logins and revenue at all, only a shared cause.

| Tier | What to say |
|---|---|
| Passes | "Correlation isn't causation" (true, doesn't diagnose *this specific* case) |
| Strong | Correctly names account size as a likely confounder and proposes checking a partial correlation or controlling for it in a regression |
| Extra points | + **[Validate]** the real numbers above: a genuinely constructed example with zero true login→revenue effect, where the naive correlation (0.92) would badly mislead anyone who stopped there + **[Business]** this is precisely the trap in a claim like "customers who log in more spend more, so let's push login frequency": the real driver (account size) isn't something a login-nudge campaign can change at all, and the campaign would likely show no revenue impact despite the strong raw correlation |

**Likely follow-ups:** How would you actually test whether logins *cause* more revenue, not just correlate with it? What's the difference between controlling for a confounder and running a randomized experiment?
**Red flag:** citing "correlation isn't causation" as a complete answer without identifying what the actual confounder is or how to check for one.
**Learn it in:** Chapter 22 or nearby.

### Rapid-fire, 73.6

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q73-033 | What's selection bias, with one business example? | The sample you're analyzing isn't representative of the population you're trying to draw conclusions about | **[Business]** analyzing only customers who responded to a survey, and concluding "customers are satisfied," ignores the (likely more dissatisfied) customers who didn't bother responding at all |
| Q73-034 | What's a natural experiment? | A real-world situation where something close to random assignment happens without anyone deliberately designing an experiment (a policy change hitting some regions and not others, say) | **[Business]** useful exactly when a true randomized test isn't ethical or possible, though weaker than a real RCT since the "randomness" is only approximate |
| Q73-035 | Why is "the data speaks for itself" a red flag phrase in a causal claim? | Data alone never distinguishes correlation from causation; that distinction always requires an assumption about the process that generated the data (randomization, a natural experiment, or a stated causal model) | **[Business]** anyone claiming pure data-driven causal certainty with no discussion of confounders or study design is skipping the hardest, most important part of the analysis |

---

## 73.7 Live-coding and live-analysis walk-throughs

### Q73-036 · Walk-through: is this A/B test result real, worth shipping, and safe to trust?

**What they're really testing:** whether you run the full checklist (significance, effect size, SRM, practical relevance) rather than stopping at the first "p < 0.05."

**The setup, talked through live:** "I've got control at 480/5,000 conversions and treatment at 545/5,000. Before I say anything about shipping this, I want to check four things in order: is the split itself sane (no SRM), is the difference statistically significant, how big is the effect in business terms, and does the sample size match what a proper power calculation would have called for."

**Verified, live:**
```python
count = np.array([545, 480]); nobs = np.array([5000, 5000])
z_stat, p_value = sms.proportions_ztest(count, nobs)
```
```
control:   9.60%
treatment: 10.90%
z = 2.143, p = 0.0321
```

**Talked through, live:** "p = 0.032, under the usual 0.05 threshold, so it's statistically significant. The lift is 1.3 percentage points, about a 13.5% relative improvement, which sounds meaningful, but I'd want to know the actual revenue or cost tied to a conversion before calling it worth shipping: statistical significance isn't the same question as 'is this worth the engineering cost to keep.' I'd also want the sample-ratio check on 5,000 vs. 5,000 (that's an exact 50/50 split here, so no SRM concern), and I'd check this sample size against what a proper power calculation for this baseline and MDE would have called for, to make sure this wasn't stopped early."

**Extra-points moves demonstrated:** **[Structure]** ran a defined checklist instead of stopping at the first significant p-value. **[Validate]** the real z-test output, not an assumed conclusion. **[Business]** explicitly separated "statistically significant" from "worth shipping," which are different questions with different owners.

**Likely follow-ups:** What if the sample sizes were very different between arms? How would you incorporate a cost estimate into the shipping decision?
**Red flag:** treating a single p-value as a complete answer to "should we ship this."
**Learn it in:** Chapter 30.

### Q73-037 · Walk-through: a stakeholder shows you a chi-square test result and asks what it means

**What they're really testing:** whether a chi-square test's actual question (independence between two categorical variables) is understood, not just its p-value.

**Talked through live:** "A chi-square test of independence checks whether two categorical variables are related at all, not the direction or size of the relationship, just whether the pattern of counts differs from what independence would predict."

**Verified, live**, on a segment-by-conversion table:
```python
observed = np.array([[120, 80], [90, 110]])   # rows: segment; columns: converted, not converted
chi2, p, dof, expected = stats.chi2_contingency(observed)
```
```
chi2 = 8.431, p = 0.0037, dof = 1
expected counts under independence: [[105, 95], [105, 95]]
```

**Talked through, live:** "p = 0.0037 says the segments and conversion aren't independent, real evidence of a relationship. But chi-square alone doesn't say *which* segment converts better or by how much, only that a relationship exists. I'd follow it with the actual conversion rates per segment to answer the business question, and I'd check the expected-counts table, shown here, to make sure no cell had too few expected observations for the test to be reliable, a common chi-square validity issue with small samples."

**Extra-points moves demonstrated:** **[Depth]** correctly distinguished "a relationship exists" (what chi-square tests) from "here's the relationship" (a separate follow-up). **[Edge cases]** flagged the small-expected-count validity concern unprompted.

**Likely follow-ups:** What test would you use for two continuous variables instead? What's Cramér's V, and when would you report it alongside the p-value?
**Red flag:** interpreting a significant chi-square result as telling you the direction or size of an effect, which it doesn't.
**Learn it in:** Chapter 21 or nearby.

---

## Common mistakes and how to spot them

| Mistake | Symptom | Fix |
|---|---|---|
| Reading "99% accurate" as "99% chance you have it" | Wildly overestimating a positive result's reliability on a rare condition | Always ask for the base rate; run Bayes' theorem (Q73-001) |
| Defining a p-value as "probability the null is true" | Confidently wrong explanations to stakeholders | It's the probability of the *data*, assuming the null, never the reverse |
| Treating "not significant" as "no effect" | Shipping decisions based on an underpowered test's false negative | Check power before concluding there's no effect (Q73-015) |
| Skipping a sample-size calculation before running a test | A test that ends inconclusive, or runs far longer than needed | Compute required sample size from baseline, MDE, alpha, and power (Q73-020) |
| Checking significance daily and stopping at the first p < 0.05 | A real, inflated false-positive rate far above the stated 5% | Pre-commit to a sample size and check date, or use a sequential method (Q73-025) |
| Ignoring a skewed traffic split as "probably fine" | Trusting results from a broken randomization pipeline | Run a chi-square SRM check before trusting anything else (Q73-026) |
| Ranking groups on an aggregate rate with very different underlying mixes | A real Simpson's paradox reversal going unnoticed | Always check subgroup rates before trusting an aggregate comparison (Q73-031) |
| Citing a strong correlation as if it were causal | Acting on a relationship driven entirely by a confounder | Look for (and control for) a plausible confounder before any causal claim (Q73-032) |

---

## In the real world: the A/B test that was actually broken plumbing

Farah, running a pricing experiment at a mid-size company, sees a strong, statistically significant lift in the treatment group after ten days and is ready to recommend shipping it. Before doing so, she runs the sample-ratio check this chapter teaches, almost as a formality: and gets a real SRM: 5,340 users in control against 4,660 in treatment, a split that shouldn't happen by chance at that scale.

She doesn't ship the pricing change. She traces the mismatch and finds that the treatment variant's page loaded slightly slower, and a fraction of mobile users on slower connections were timing out before the assignment even completed, silently dropping out of the treatment group specifically. Those dropped users, it turns out, were disproportionately price-sensitive mobile shoppers, exactly the segment least likely to convert. The "lift" wasn't from the new pricing at all; it was from quietly excluding the users least likely to buy.

The fix took two days: a loading-performance bug, unrelated to pricing entirely. The re-run test, with the SRM resolved, showed no significant pricing effect at all. Farah's manager's reaction was the right one: relief that the SRM check happened before the change shipped, not after, when the "successful" pricing test would have been cited as evidence for a change that did nothing, while the real bug (a broken experience for a whole segment of mobile users) went unnoticed and unfixed.

---

## Tools

**Python** with **SciPy** (`scipy.stats`) and **statsmodels** (`statsmodels.stats.api`), both free, both used throughout this chapter for every simulation, test statistic, and sample-size calculation. **R** offers equivalent functionality (`prop.test`, `power.t.test`, `chisq.test`) and is common in some analytics teams; the underlying statistics are identical regardless of language. Everything in this chapter ran on Python 3.12, SciPy 1.17.1, statsmodels 0.15.0.

---

## The project

**Goal:** run, not just read, this chapter's core demonstrations on your own numbers.

1. Compute Bayes' theorem for a real base-rate scenario from your own work (a fraud flag, a churn flag, a quality-control test) and see how far the "accuracy" number is from the true positive-predictive value.
2. Run a real sample-size calculation for an A/B test you'd actually want to run, using your own baseline rate and a business-justified MDE.
3. Simulate the peeking problem yourself (or reason through why it happens) on a metric relevant to your own work.
4. Find (or construct) a Simpson's paradox in your own data: two groups, a category where the aggregate ranking reverses the subgroup rankings.
5. Take one correlation you've observed in your own work and name a plausible confounder, then say how you'd check whether it explains the relationship.

---

## Final-week revision list

Q73-001, Q73-002, Q73-003, Q73-008, Q73-009, Q73-014, Q73-015, Q73-016, Q73-017, Q73-019, Q73-020, Q73-021, Q73-025, Q73-026, Q73-028, Q73-031, Q73-032, Q73-036, Q73-037.

---

## Key terms

Bayes' theorem · base rate · conditional probability · Monty Hall problem · birthday problem · independent vs. mutually exclusive events · expected value · Binomial distribution · Poisson distribution · Central Limit Theorem · variance · standard deviation · Normal / log-normal distribution · heavy-tailed distribution · p-value · null hypothesis · Type I error · Type II error · statistical power · t-test vs. z-test · confidence interval · minimum detectable effect (MDE) · randomization · one-tailed vs. two-tailed test · holdout group · peeking (repeated significance testing) · Sample Ratio Mismatch (SRM) · novelty effect · multiple comparisons · Bonferroni correction · network effect (interference) · Simpson's paradox · confounder · partial correlation · selection bias · natural experiment

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 71, SQL Question Bank,** already covered the mechanics of building the aggregated tables (retention counts, group-by rates) that feed many of this chapter's tests.
- **Chapter 74, Machine Learning Question Bank,** builds directly on this chapter's hypothesis-testing and bias/variance foundations for model evaluation.
- **Chapter 30 and Chapter 22** (experimentation and causal inference) teach every technique this bank draws on, in full; this chapter tests it, it doesn't re-teach it from scratch.
