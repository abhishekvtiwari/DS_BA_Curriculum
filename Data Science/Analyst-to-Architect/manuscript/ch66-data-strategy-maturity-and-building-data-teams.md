# Chapter 66. Data Strategy, Maturity & Building Data Teams

*Part 7 — Architecture, Governance & Leadership*

> **Chapter at a glance**
>
> **You will learn to:** write a data strategy that fits on one page and actually gets used · score an organization's data maturity honestly, across the dimensions that matter, not just the ones that flatter it · build a real business case for data platform investment, including the uncomfortable parts a case usually leaves out · choose a team structure — centralized, embedded, or hybrid — that fits the organization's actual size, and hire against a named gap rather than a vague sense that "we need more people" · decide when to build a capability and when to buy it, with a real framework rather than a preference · lead change in an organization that doesn't yet trust data by default.
>
> **Before you start:** this chapter draws together every earlier Part 7 chapter into an organizational and strategic view: the platform (Chapter 60), its trade-offs (61), its architecture pattern (62), its governance (63), its security (64), and — directly — its real cost (65).
>
> **Time needed:** 9–11 hours, spread over a week: about 2 hours for sections 66.1–66.3 and their code, 1 hour for sections 66.4–66.6, 3 hours for the exercises, and 3–5 hours for the project.
>
> **Tools:** nothing new to install. The maturity scorecard and the business case use pandas (Chapter 18) in a notebook in your usual virtual environment. The outputs shown come from Python 3.11 and pandas 3.0.6.
>
> **Practice data:** `companion/ch66/`: `maturity_scorecard.csv` (a six-dimension maturity assessment for Riverstone) and `roi_case.csv` (the business case's inputs, each traced to the earlier chapter it comes from).

---

## Why this matters

Every technical skill in this book — the query, the pipeline, the model, the architecture diagram — eventually runs into a question none of them answer on their own: **is the organization around this system actually ready to use what's been built, and is anyone going to keep investing in it?**

A brilliant platform serving a company that doesn't trust it, staffed by a team that was never sized against a real need, defended by a business case nobody can actually check, is not a success story waiting to be written — it's a project one budget review away from being quietly deprioritized. The skills in this chapter are the ones that keep everything else in this Part alive past its first year: a strategy simple enough to be remembered, a maturity assessment honest enough to be trusted, a business case that survives scrutiny, a team built against real gaps, and a culture that reaches for the platform by habit rather than by mandate.

None of this is as technically demanding as the chapters before it. All of it is, in practice, what determines whether those chapters' work gets to matter for more than one budget cycle.

---

## In plain English

A well-built house still needs someone to decide which room gets renovated next, whether to hire a live-in caretaker or call a contractor when something breaks, and how to convince the family actually to use the new kitchen instead of ordering in out of habit.

**Strategy** is deciding which room gets attention next, and being able to say why in one sentence. **Maturity** is an honest walk through the house — this room is finished, that one still has exposed wiring, be honest about both. **The business case** is the sentence that gets the renovation budget approved, and it only works if it's checkable, not just optimistic. **Team structure** is deciding whether one skilled generalist handles everything or whether it's time for a specialist, and building the case for that hire from a specific leak, not a vague feeling that the house needs more hands. **Build versus buy** is deciding whether to build custom shelving or order something from a shop that already makes exactly what you need. **Culture** is whether the family actually uses the renovated kitchen, or keeps ordering in because the old habit is still easier than the new room.

None of these questions has a technical answer. All of them decide whether the technical work survives.

---

## 66.1 A data strategy on one page

A data strategy that takes more than a page to explain will not survive contact with a busy executive's attention span, and — more importantly — will not survive being remembered by the team that's supposed to execute it. **The discipline of fitting it on one page is not a formatting preference; it's a test of whether the strategy has actually been decided, rather than merely gestured at.**

A one-page strategy has five parts, each a sentence or two:

1. **Where we are** — one honest paragraph, backed by the maturity assessment in section 66.2, not aspiration.
2. **Where we're going** — the two or three capabilities that matter most over the next year, not a wish list of everything possible.
3. **Why these, and not others** — the explicit trade-off, because a strategy that doesn't say no to something isn't a strategy.
4. **How we'll know it's working** — a small number of measurable signals, in Chapter 60's vocabulary (section 60.3): numbers, not adjectives; Chapter 23's KPIs are the model.
5. **What we need to get there** — people, budget, and the single biggest risk to the plan.

**Riverstone's own, written at this point in its story:** *Where we are: a governed, secured, cost-transparent centralized platform (Chapters 60–65), serving one company well. Where we're going: closing the two gaps our own maturity assessment scores weakest — nobody owns making data easy to find and trust (catalog and discoverability), and a culture that still reaches for habit before the platform. Why these: the platform's technical foundation is solid; the organization around it is the constraint now, not the technology. Not this year: a new platform component, or a cost project; the cost model gets a standing monthly review instead. How we'll know: the time it takes to find the right table, measured before and after, and a rising share of decisions that cite a dashboard rather than a hunch, tracked deliberately. What we need: one catalog and governance owner (section 66.4), and continued executive attention through the next two budget cycles, since none of this compounds in under a year.*

---

## 66.2 Maturity models, scored honestly

A **maturity model** describes stages an organization's data capability typically passes through — usually something like *ad hoc* (nothing formalized, works by heroics), *reactive* (fixes problems after they occur), *proactive* (problems anticipated and designed against), *managed* (measured, monitored, continuously improved), and *optimized* (a genuine competitive advantage, not just the minimum expected). This is a simplified five-stage scale. Published models (CMMI, DAMA's data management maturity model, Gartner's) use different names and a different order; in CMMI, for example, "Managed" is stage 2. The scoring discipline is the same. Its value isn't the taxonomy — it's the discipline of scoring yourself against it honestly, the same discipline Chapter 62's mesh-readiness check (section 62.6) applied to one specific question, generalized here to the whole organization.

### How a score is worked out

A score needs a rule, or two people will score the same company differently. Riverstone's rule: **every stage of every dimension has five yes-or-no criteria. The score is the highest stage whose five criteria are all met, plus one-fifth for each criterion of the next stage that is met.** Here is one row worked by hand. Data quality meets every stage-3 criterion, and the table below checks its five stage-4 (Managed) criteria.

| Stage-4 criterion for data quality | Met? |
|---|---|
| Every pipeline has automated tests (Chapter 47) | Yes |
| Freshness is monitored, with an alert (Chapter 47) | Yes |
| Loaded totals are reconciled to the source (Chapter 14) | Yes |
| Every source has a data contract (Chapter 47) | No |
| Quality incidents are reviewed every month | No |

Three of five are met, so the score is 3 + 3 ÷ 5 = **3.6**. Riverstone scored six dimensions this way. The companion file keeps the two counts for each one: `stage_met`, the highest stage fully met, and `next_met`, how many of the next stage's five criteria are met.

```python
import pandas as pd

maturity = pd.read_csv("maturity_scorecard.csv")
print(maturity[["dimension", "stage_met", "next_met"]].to_string(index=False))
```

```
                 dimension  stage_met  next_met
Data quality & reliability          3         3
   Architecture & platform          3         1
         Security & access          3         4
 Catalog & discoverability          1         4
           Cost discipline          2         3
       Data-driven culture          2         1
```

- `pd.read_csv("maturity_scorecard.csv")` reads the file into a DataFrame, one row per dimension (Chapter 18).
- `maturity[[...]]` keeps just three columns. The file also has an `evidence` column, one sentence per dimension, which is too wide to print neatly; it's in the table below instead.
- `.to_string(index=False)` prints every row without the row numbers on the left.

Next, turn the two counts into a score with the rule above:

```python
maturity["score"] = maturity["stage_met"] + maturity["next_met"] / 5
print(maturity[["dimension", "score"]].to_string(index=False))
```

```
                 dimension  score
Data quality & reliability    3.6
   Architecture & platform    3.2
         Security & access    3.8
 Catalog & discoverability    1.8
           Cost discipline    2.6
       Data-driven culture    2.2
```

- `maturity["next_met"] / 5` divides every value in the column by 5, row by row, and `+` adds the `stage_met` of the same row.
- `maturity["score"] = ...` stores the result as a new column, so the next cell can use it.

Finally, the average, the weakest dimension and the strongest:

```python
print(f"average score: {maturity['score'].mean():.2f}")
weakest = maturity.loc[maturity["score"].idxmin()]
print(f"weakest: {weakest['dimension']} ({weakest['score']})")
strongest = maturity.loc[maturity["score"].idxmax()]
print(f"strongest: {strongest['dimension']} ({strongest['score']})")
```

```
average score: 2.87
weakest: Catalog & discoverability (1.8)
strongest: Security & access (3.8)
```

- `.mean()` averages the column; `:.2f` prints it with two decimals.
- `.idxmin()` returns the **row label** of the smallest value in the column, not the value itself (here 3, the fourth row, since labels start at 0). `.idxmax()` does the same for the largest.
- `maturity.loc[label]` picks out that whole row, so `weakest["dimension"]` and `weakest["score"]` read two of its fields.

![Six dimensions plotted against a five-stage maturity model: security and access 3.8, data quality 3.6, architecture 3.2, cost discipline 2.6, data-driven culture 2.2, and catalog and discoverability 1.8. The three technical dimensions sit in stage 3, Proactive; the three organizational ones sit in stages 1 and 2.](figures/fig66-1-maturity-model.svg)

*Figure 66.1 — The honest picture: the technical dimensions score well; the organizational ones (finding data, cost as a routine habit, a culture that reaches for data by default) lag behind. This is normal, not a failure — it's exactly the gap a strategy exists to close.*

**The average is a conversation starter, not a measurement.** The stages are ordered names, not equal distances, so "2.87" doesn't mean much on its own. Read the lowest scores first. Here is the whole scorecard, with the evidence behind each score:

| Dimension | Score | Evidence |
|---|---:|---|
| Data quality & reliability | 3.6 | Automated tests and freshness checks (Ch 47), reconciled totals (Ch 14); not every source has a contract yet |
| Architecture & platform | 3.2 | A designed, documented platform (Ch 60–62); still centralized, still young |
| Security & access | 3.8 | Roles, masked views, row-level security and a fairness audit (Ch 64); not yet a company-wide habit |
| Catalog & discoverability | 1.8 | No catalog: finding the right table means asking Meera's team; 11 of the 24 automations were unknown to it (Ch 63) |
| Cost discipline | 2.6 | A real cost model (Ch 65), built once, not yet reviewed every month |
| Data-driven culture | 2.2 | Individual wins (Ch 19, 20); most decisions still made by habit and hierarchy |

**What the low scores actually mean, read correctly:** catalog and discoverability scoring 1.8 doesn't mean the platform's data is bad — it means that finding the right table, and knowing it's the one everyone else uses, still depends on asking a person. Cost discipline scoring 2.6 doesn't mean Chapter 65's cost model was bad work — it means a model built once, brilliantly, is not the same thing as a *habit* of checking it every month, which is what a stage-4 organization would actually be doing. Data-driven culture scoring 2.2 doesn't mean nobody at Riverstone uses data — it means most decisions are still made the way they always were, by hierarchy and habit, with the platform consulted occasionally rather than by default. **A maturity assessment's job is distinguishing "we built the thing" from "the thing has become how we normally operate,"** and those are honestly different achievements, often separated by a year or more of consistent practice rather than any further engineering.

> **Watch out: a maturity model scored to flatter itself is worse than no assessment at all.** The temptation, especially when presenting to leadership, is to round every score up half a stage. A maturity assessment's only value is as an honest diagnostic; an inflated one actively prevents the organization from seeing the gap it most needs to close.

---

## 66.3 Building the business case — including the part it usually leaves out

A business case argues that a spend is worth its cost. Its core number is the **return on investment (ROI)**: the benefit divided by the cost. A business case for continued data platform investment is only as credible as its willingness to show its weakest number, not just its strongest one. Here is Riverstone's, built from figures already established in this book rather than invented for the occasion.

### Where each saving comes from

Every saving is time, priced at Riverstone's loaded staff cost of ₹300 an hour (salary plus overheads; Chapter 20, section 20.14). Work each one out before trusting the file:

```python
rate = 300                              # ₹ an hour, Riverstone's loaded staff cost
flash = 325 * rate                      # Chapter 20: 325 hours saved a year
macro = 4 * (240 - 9) / 3600 * rate     # Chapter 19: 4 runs a year, 240 s -> 9 s each
po_intake = (600 - 197) * 250           # Chapter 58: ₹ saved a day x 250 working days
print(flash, macro, po_intake)
```

```
97500 77.0 100750
```

- **The Daily Sales Flash** saves 325 hours a year (Chapter 20, section 20.14): 325 × ₹300 = ₹97,500.
- **The branch consolidation macro** runs once a quarter, four times a year, and Chapter 19's rewrite took it from about four minutes (240 seconds) to nine. That saves 231 seconds a run; `/ 3600` turns seconds into hours, and 4 × 231 ÷ 3,600 × ₹300 = **₹77 a year**. That tiny number is honest, and it's also the wrong measure of the macro: its real value was the ₹1.88 crore double count its new checks stopped (Chapter 19), which no time saving captures.
- **PO intake in assisted mode** costs ₹197 a day of review and queue time against ₹600 to type the orders by hand (Chapter 58, section 58.7): ₹403 a day × 250 working days = ₹1,00,750. **That is labour only, and it holds only if the reviewers catch at least about 97% of the wrong drafts** (Chapter 58). At a 90% catch rate, the wrong orders that slip through cost more than the time saved, and assisted mode loses about ₹2,32,500 a year (Chapter 63, section 63.2). Nobody has measured the catch rate yet; that is what the shadow-mode run is for.

### The case, from the file

The companion file keeps only these raw inputs: the platform's cost, the three savings and the proposed hire's salary. Every total is worked out in code, so none can drift out of step with its parts.

```python
roi = pd.read_csv("roi_case.csv")
print(roi[["item_id", "amount_rs", "kind"]].to_string(index=False))
```

```
      item_id  amount_rs               kind
platform_cost     453360               cost
        flash      97500    measured saving
        macro         77    measured saving
    po_intake     100750 conditional saving
  hire_salary     900000               cost
```

- Each row has a short, fixed `item_id`, so the code can find a row by its name rather than by searching its description.
- `kind` says what sort of number it is: a cost, a **measured** saving, or a **conditional** one that holds only if something not yet measured turns out true.
- The file's fourth column, `source`, names the chapter and the arithmetic behind each amount. The platform's cost is Chapter 65's monthly model, ₹37,780 a month × 12 = ₹4,53,360 a year.

Now total the measured savings and compare them with the cost:

```python
roi = roi.set_index("item_id")
platform = roi.loc["platform_cost", "amount_rs"]
measured = roi.loc[["flash", "macro"], "amount_rs"].sum()
print(f"platform cost:    ₹{platform / 100_000:.2f} lakh a year")
print(f"measured savings: ₹{measured / 100_000:.2f} lakh, "
      f"{measured / platform * 100:.0f}% of the cost")
```

```
platform cost:    ₹4.53 lakh a year
measured savings: ₹0.98 lakh, 22% of the cost
```

- `set_index("item_id")` makes the ids the row labels, so `roi.loc["platform_cost", "amount_rs"]` reads one cell: the row labelled `platform_cost`, the column `amount_rs`.
- `roi.loc[["flash", "macro"], "amount_rs"]` passes a **list** of labels, so it returns both rows' amounts, and `.sum()` adds them.
- `/ 100_000` turns rupees into lakh (the underscore is just a digit separator Python ignores), and `:.2f` keeps two decimals.
- The two strings inside `print(...)` sit side by side, so Python joins them into one; that keeps each line short.

Then add the conditional saving:

```python
with_po = measured + roi.loc["po_intake", "amount_rs"]
print(f"with PO intake:   ₹{with_po / 100_000:.2f} lakh, "
      f"{with_po / platform * 100:.0f}% of the cost")
```

```
with PO intake:   ₹1.98 lakh, 44% of the cost
```

![A horizontal bar chart. The top bar is the platform's annual cost, ₹4.53 lakh. The bar below is built up from savings: the Daily Sales Flash ₹97,500 and the branch macro ₹77, measured, 22% of the cost; then PO intake ₹1,00,750, hatched and labelled as counting only if reviewers catch at least 97% of wrong drafts, taking the total to 44%. The rest, up to the full cost, is an empty dashed box labelled the unmeasured ceiling.](figures/fig66-2-roi-case.svg)

*Figure 66.2 — The honest version of a business case: two measured savings cover about a fifth of the platform's cost, and a third, if its condition holds, takes that to 44%. The rest of the value is real but harder to put a number on — and a credible case says so.*

**This is the finding a less honest business case would have hidden, and it's the more useful one.** Two measured savings — the Daily Flash (Chapter 20) and the branch consolidation macro (Chapter 19) — add up to ₹97,577 a year, 22% of a platform that costs ₹4,53,360 a year to run. PO intake's assisted mode (Chapter 58) would add ₹1,00,750 and take the total to 44%, but only once shadow mode has shown the reviewers catch at least 97% of wrong drafts. **On the numbers alone, the platform looks like a net cost.**

**What a credible business case does with that finding is not hide it — it explains what the accounting is missing:**

- **The defect-detection model** (Chapter 53) prevents shipping defective product; its value is real but shows up as *avoided cost*, which is genuinely harder to quantify than *time saved*, because it requires estimating what would have happened without it.
- **The support assistant** (Chapter 55) and **CRM reverse-ETL sync** (Chapter 51) both save time that's diffused across many small interactions rather than concentrated in one measurable process, and diffused savings are real but resist a clean per-year number.
- **Checks that stop errors** are worth more than the time they save: the branch macro's ₹77 of time sits beside a ₹1.88 crore double count it now catches (Chapter 19).
- **The platform enables decisions that wouldn't otherwise be made at all** — Chapter 64's fairness audit of regional lead scoring produced value (East-region leads worked as fast as every other region's, a corrected way of ranking them) that has no "hours saved" analog whatsoever, because nothing was being done manually before to compare against.
- **Some value is optionality**, not immediate return: the platform being ready to support a new AI system, a new regulation, or a new region is worth something even in a year that value isn't drawn on.

**The honest version of the business case, stated the way it should actually be presented:** *"Two measured automations cover 22% of the platform's cost. A third, PO intake, takes that to 44% once we've shown its reviewers catch at least 97% of wrong drafts; we're measuring that now. The remainder is real value we haven't built a clean way to measure yet — avoided errors, diffused time savings, and decisions the platform makes possible that weren't happening at all before. We're not asking you to trust an unmeasured number; we're asking you to recognize that the measured floor is real, and so is the unmeasured ceiling."* That sentence survives a skeptical chief financial officer's (CFO's) question in a way that a single inflated ROI multiple never would.

### The case for the hire itself

The proposal this case supports is a new hire: a catalog and governance owner (section 66.4), budgeted at ₹9,00,000 a year. The first question a finance manager asks is what that ₹9 lakh buys. Nobody at Riverstone has measured the hire's main benefit yet, the time people lose finding the right table and checking it's the one everyone else uses, so the case states it as an **estimate**, with its assumptions in the open. Suppose 20 people pull data from the platform each week (the branch offices, sales, finance, the plant), and each loses one hour a week to it:

```python
people, hours_a_week, weeks = 20, 1, 50    # assumptions, to be measured
floor = people * hours_a_week * weeks * rate
salary = roi.loc["hire_salary", "amount_rs"]
print(f"time-to-find estimate: ₹{floor / 100_000:.2f} lakh, "
      f"{floor / salary * 100:.0f}% of the salary")
```

```
time-to-find estimate: ₹3.00 lakh, 33% of the salary
```

- `people, hours_a_week, weeks = 20, 1, 50` sets three names in one line. Fifty weeks is the same 250-day working year as above.
- `rate` is still ₹300 an hour from the first cell.

**Try changing one assumption.** Set `hours_a_week` to `0.5` and run the cell again: the estimate halves to ₹1.50 lakh, 17% of the salary. An estimate is only as good as its assumptions, which is why the case plans to measure them.

Even if the estimate is right, it covers a third of the salary. The rest is ceiling, and the case names it: a catalog that shows who owns each table and what it means is what stops the next pair of disagreeing macros (Chapter 63 found two such pairs); a catalog is how a company answers "where does this customer's personal data live?", the question every privacy request or breach report under India's DPDP Act starts from (Chapter 64); and a table nobody can find is a data product in name only (Chapter 62, section 62.7). **The case also says how the estimate becomes a measurement:** log time-to-find for a month before the hire starts, and again once the catalog is in use.

---

## 66.4 Hiring and structuring data teams

**Three team topologies**, each fitting a different scale, and Chapter 62's Conway's Law (section 62.8) governing the choice exactly as it governed the centralized-versus-mesh decision:

- **Centralized:** one team serves the whole organization — Riverstone's structure since Chapter 60, and the right fit while one team can serve without a persistent queue behind it.
- **Embedded:** data people sit inside each business function, reporting to that function rather than to a central data team. Scales domain expertise and responsiveness; risks exactly the duplicated, disagreeing logic Chapter 63's audit found when Delhi and Kolkata each built their own version of the consolidation macro.
- **Hybrid** (sometimes called "hub and spoke"): a central team owns the platform, standards, and shared services (Chapter 63); embedded specialists sit in each function, using that shared platform rather than building their own. This is where Riverstone is now visibly heading, one hire at a time.

![Three stages joined by arrows: the four-person team from Chapter 60, led by Meera as Head of Data Platform; then the Taloja plant's own data analyst added, owning one plant data product; then a proposed next hire, a catalog and governance owner, for the weakest dimension in section 66.2, catalog and discoverability at 1.8.](figures/fig66-3-team-evolution.svg)

*Figure 66.3 — Each hire is justified by a named gap, not a general sense that the team is stretched. That discipline is the whole difference between structured growth and headcount creep.*

**The Taloja plant's data analyst (Chapter 62) was Riverstone's first hybrid-model hire**, and it was justified by a specific, observed signal: a domain with a builder of its own that asked to own its own data, exactly the trigger section 62.6's maturity check said to wait for rather than guess at. Meera's rerun of that check scored 12 out of 25: still not a mesh, but enough for a first step, one plant data product owned by the plant. **The next proposed hire follows the same discipline**, not a general one: section 66.2's maturity assessment scores catalog and discoverability lowest of all six dimensions, at 1.8, and two earlier chapters found the same gap independently. Chapter 63's automation audit found 11 automations nobody on Meera's team had heard of, and Chapter 64's governance section (section 64.6) names a catalog as the piece that makes data discoverable; Riverstone doesn't have one. Nobody currently owns making data discoverable and consistently governed across the whole platform, as opposed to within any one pipeline.

**A hiring principle worth stating explicitly**, because it's the one this book's own story keeps demonstrating: **hire against a named, evidenced gap, not against a feeling that the team is busy.** A team that's busy building things nobody asked for is not understaffed; it's misdirected. A team that's turning away a specific, recurring, costly request is understaffed in a way a job description can be written against.

---

## 66.5 Build versus buy

Every capability this book has taught you to build has an alternative: **buy something that already does it.** The decision is not a preference for engineering purity versus pragmatism — it's a real trade-off, worth scoring the same disciplined way as any other architectural choice.

![A build-versus-buy scorecard for a managed data catalog, one row per dimension with the buy option, the build option and which side has the edge: time to a working solution, buy; fit to exact needs, build, eventually; maintenance burden, buy; cost at current scale, buy; lock-in risk, buy, narrowly. Buy wins on four of five dimensions.](figures/fig66-4-build-vs-buy.svg)

*Figure 66.4 — At a four-person team's scale, buying a catalog wins on nearly every dimension. The one place build wins — perfect fit — usually isn't worth what it costs to get there.*

**The worked example: Riverstone's data catalog**, the gap section 66.2's maturity assessment scores lowest and Chapter 64's governance section names. Scored honestly:

- **Time to a working solution:** a managed catalog tool is usable in weeks; a custom-built one is months of a four-person team's scarce time.
- **Fit to exact needs:** building wins here, eventually — a custom catalog can match Riverstone's exact workflow perfectly. The word "eventually" is doing real work: it means months of iteration a small team doesn't have to spare.
- **Ongoing maintenance:** a bought tool's maintenance is the vendor's problem; a built one's maintenance is the same four-person team that's already stretched thin, forever, on top of everything else they own.
- **Cost at current scale:** a subscription is predictable and budgetable; engineering time spent building and maintaining a catalog is real cost that simply doesn't show up as a line item on the bill Chapter 65 modeled.
- **Lock-in risk:** the one dimension where buying carries a real cost — switching away from a vendor's tool is expensive. But an internal tool that only one person on a four-person team understands is its own kind of lock-in, arguably a worse one, since nobody outside the company can be hired to fix it. So even here the edge goes, narrowly, to buying.

**The general rule the scorecard supports:** **buy when the capability is common enough that a vendor has already solved it well, and build when your need is genuinely different from everyone else's.** A data catalog, honestly, is not different at Riverstone from at any other mid-size company — which is exactly why buying wins here. It's the same judgment Chapter 62 made about data mesh: match the choice to the organization's actual size and needs, not to what's fashionable.

---

## 66.6 Change management and data culture

The hardest part of everything this Part has taught is not technical, and it's also not new information at this point in the book — it's a pattern this book's own stories have already shown you, repeatedly, without naming it as change management until now.

**Chapter 19's story** — a macro that had run for nine years, with no owner since its author left in 2020 — wasn't a technology failure. It was a culture where nobody felt empowered, or responsible, to ask "does this still work correctly?" **Chapter 63's shadow-IT audit** found 24 automations, 17 of them with no owner, no monitoring and no written plan for failure, not because anyone was careless, but because the *habit* of checking in with a central platform team had never been built — every team solved its own problem, quietly, because that was simply how things had always been done. **Chapter 62's vendor-pitch story** worked precisely because Anita Rao's culture already valued an honest scorecard over an exciting pitch — a culture that took real, deliberate effort to build, not a default state.

**Four habits that build a data-driven culture, none of them technical:**

1. **Make the easy path the governed path** (Chapter 63's own lesson, generalized): a shared service that's genuinely easier to use than the workaround gets adopted; a mandate that's harder to follow than the old way gets quietly routed around.
2. **Celebrate the audit finding, not just the fix** — Chapter 63's story treated every discovered gap as useful information, not a failure to be embarrassed about, which is exactly why the next round of questions got honest answers.
3. **Put the data where the decision is being made**, not in a separate report nobody opens — Chapter 20's Daily Flash succeeded specifically because it arrived where the decision-maker already was, rather than requiring them to go looking for it.
4. **Model the behavior from leadership** — Anita Rao, as Sales Head, declining the vendor's pitch on the strength of a scorecard, in front of the team, taught more about the culture Riverstone wanted than any policy document could have.

**The uncomfortable truth this section closes on:** a data platform this well-designed, this well-governed, this honestly costed, can still fail — not technically, but organizationally — if nobody changes how decisions actually get made day to day. The technical work in Chapters 60 through 65 was necessary. This chapter's work is what makes it sufficient.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| A strategy document longer than one page | Nobody on the team can recall what it actually says | Force it to one page; that constraint is the discipline |
| A strategy with no explicit "no" | Everything is a priority, so nothing is | State what you're deliberately not doing this year, and why |
| A maturity assessment scored to flatter itself | Leadership never sees the real gap that needs closing | Score honestly; the diagnostic's only value is accuracy |
| Scores with no rule behind them | Two people score the same company a whole stage apart | Write the criteria for each stage down, and score against them |
| A business case that hides its weak numbers | It collapses the moment someone asks a hard question | Show the measured floor and name the unmeasured ceiling explicitly |
| Counting an assumption as a measurement | A saving that depends on something nobody has checked is presented as fact | Label each number measured, conditional or estimated, and say what would confirm it |
| Treating unquantified value as if it doesn't exist | Real benefits (avoided errors, culture change) get left out of the case entirely | Name them explicitly, even without a precise number |
| Hiring because the team "feels busy" | Headcount grows without a specific gap it closes | Hire against a named, evidenced gap, the way Chapter 62's Taloja hire was |
| Building a capability a vendor already sells well | Months of a small team's time spent reinventing a data catalog | Score build vs. buy honestly; buy when the need isn't genuinely unique |
| Assuming the culture will follow the technology | A brilliant platform nobody routes decisions through | Make the governed path the easy path; put data where decisions happen |
| Punishing an audit finding instead of using it | The next audit gets less honest answers | Treat every gap found as useful information, the way Chapter 63's story did |
| Confusing "we built it" with "it's how we operate" | A capability exists but isn't yet a habit | Track adoption and routine use, not just deployment |

---

## In the real world: the business case that told the truth

When Meera prepared the proposal for Riverstone's next data-platform hire — the catalog and governance owner section 66.4 names — her first draft of the business case did what most first drafts do: it rounded every benefit up and left out everything hard to measure. The platform, by that draft's accounting, "paid for itself many times over," a sentence that felt true and that she couldn't actually defend line by line if anyone asked her to show the arithmetic.

She rewrote it after a conversation with Vikram Singh, who'd sat through enough budget reviews to know the difference between a number that survives questioning and one that only sounds confident. His question was simple: *"If Suresh Menon in finance asks you to walk through exactly how you got that multiple, can you?"* She couldn't, not for the inflated version.

The rewrite was the honest one: two measured automations covering 22% of the platform's annual cost, a real number, checkable in an afternoon by anyone who wanted to; a third, PO intake, that would take it to 44%, with its condition stated plainly, the reviewers' catch rate that shadow mode was still measuring; and, for the hire, an estimate of the time lost finding data, labelled as an estimate, with a plan to measure it. And then, deliberately, a section that didn't try to manufacture a number for everything else: the defect model's avoided losses, the support assistant's diffused time savings, the fairness-audit fix that had no "before" state to compare against because nothing was being measured that way previously.

The proposal went to Anita Rao with every part intact. Her response, reportedly, was that the honest version was more persuasive than the earlier draft's inflated multiple had ever been — not because the numbers were bigger, but because she could trust every rupee in them, and trusting the measured part made her willing to believe the unmeasured part was real too. The hire was approved within the month.

Once the catalog owner had been in place long enough to measure, Meera ran the same honest accounting again. The measured floor had grown — the new hire's own work was itself now a measured line, since time-to-find had been logged before the catalog and after it, and the estimate could be replaced by a measurement. The business case hadn't just paid for one hire; it had become a template Riverstone now used for every subsequent one.

What made the difference:

- **She showed the weak number rather than hiding it**, and it turned out to be more persuasive, not less, because it was checkable.
- **She said which numbers were measurements and which were conditions or estimates** — and what would turn each one into a measurement.
- **She named the unmeasured value explicitly, without pretending to quantify it** — the honest gap between what's measured and what's real became part of the case, not an embarrassment to paper over.
- **The rewritten case became reusable infrastructure of its own** — a template for every future proposal, not a one-time document.
- **Trust compounded**: the more honest the first case, the more credit the next one was given before anyone even checked its numbers.

---

## Project: write a one-page strategy and an honest business case

**Goal:** produce a real, one-page data strategy and a business case for one specific investment, both built to survive a skeptical reader's questions.

### Tools you'll need

- **Python with pandas**, in your usual virtual environment (Chapters 17 and 18), for the maturity scorecard and the business-case arithmetic.
- **No specialized software required** — a strategy on a page, a maturity scorecard, and a business case are documents and disciplined arithmetic, not tools to buy.
- **Companion files (`companion/ch66/`):**
  - `build_ch66_files.py`: builds both CSV files from figures already established in Chapters 19, 20, 58, and 65, and says where each number comes from.
  - `maturity_scorecard.csv`: the six-dimension assessment behind Figure 66.1, with the two counts behind each score and one sentence of evidence.
  - `roi_case.csv`: the business case's raw inputs behind Figure 66.2: the platform's cost, the three savings, and the proposed hire's salary, each with its source.

**Option A: your own organization.** Write the strategy for a team or function you actually work in.

**Option B: Riverstone.** Extend section 66.1's strategy with your own maturity assessment (reuse or re-score `maturity_scorecard.csv`), and build the business case for a different next investment — not the catalog-owner hire this chapter already made, but something else the maturity gaps suggest.

**Steps**

1. **Write the one-page strategy** using section 66.1's five parts. If it doesn't fit on one page, cut, don't shrink the font.
2. **Score maturity honestly** across at least four dimensions relevant to your context, using section 66.2's rule (five criteria per stage), each with a one-sentence piece of evidence — not a number alone.
3. **Identify the weakest dimension**, and make it the subject of the "where we're going" section of your strategy.
4. **Build a business case** for one specific investment the maturity gap justifies. Include at least one number you can defend line by line, label every number measured, conditional or estimated, and name at least one piece of value you explicitly can't quantify — named honestly, not hidden.
5. **Propose a hire, if relevant**, justified against a specific, evidenced gap — not a general sense of being stretched — and weigh its salary against what it would measurably save.
6. **Run a build-versus-buy scorecard** for one capability under consideration, using section 66.5's five dimensions.
7. **Name one change-management action** — not a policy, a specific habit-level change — that would move your weakest maturity dimension forward.

**What good looks like:** the strategy genuinely fits one page; the maturity scores include at least one uncomfortable finding; the business case shows its weakest number rather than hiding it; the hire or build/buy recommendation is traceable to a specific piece of evidence, not a feeling.

**Stretch goals**

- Take a business case you've actually written (or seen) at work, and rewrite it using this chapter's "show the floor, name the ceiling" method. Does it become more or less persuasive?
- Score Riverstone's maturity a year further into its story (imagine the effects of the catalog-owner hire and a year of monthly cost reviews) and redraw Figure 66.1.
- Interview someone who's led a data team's growth, and ask them to name one hire they made against a real, evidenced gap, and one they now recognize was made on a feeling alone.

---

## Recap

- **A one-page data strategy** — where we are, where we're going, why, how we'll know, what we need — is a discipline that forces real decisions, not a formatting preference.
- **A maturity model** needs a scoring rule to be honest. Scored with one, Riverstone is strongest on the technical dimensions (security, data quality, architecture) built across Chapters 60–64, and weakest on the organizational ones (finding data, cost as a routine habit, a genuinely data-driven culture) — a completely normal, expected gap. Read the lowest score first, not the average.
- **A credible business case shows its weakest number**: two measured Riverstone automations cover 22% of the platform's annual cost, a third takes it to 44% only if its stated condition holds, and the honest remainder is named explicitly rather than papered over with an inflated multiple. A hire's case weighs its salary the same way.
- **Team structure** — centralized, embedded, or hybrid — follows Conway's Law; Riverstone is visibly moving toward hybrid, one hire at a time, each justified against a specific, evidenced gap rather than general growth.
- **Build versus buy** is a real, scoreable trade-off; a capability common enough that vendors already solve it well (a data catalog) usually favors buying, especially for a small team.
- **Culture is the hardest, least technical part of everything this Part has built**, and this book's own earlier stories — the macro with no owner for nine years, the shadow-IT audit, the declined vendor pitch — were change-management lessons all along, before this chapter named them as such.

---

## Key terms

data strategy · one-page strategy · maturity model · maturity stage · maturity score · business case · return on investment (ROI) · measured floor · unmeasured ceiling · conditional saving · team topology · centralized team · embedded team · hybrid (hub and spoke) team · Conway's Law (Chapter 62) · build versus buy · vendor lock-in · change management · data culture · showback (Chapter 65)

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can write a data strategy that fits on one page and says no to something explicitly.
- [ ] You score maturity against written criteria, including dimensions that reflect poorly on work you're proud of.
- [ ] You build a business case that shows its weakest, most defensible number rather than an inflated one, says which numbers are measured and which are conditional, and names unquantified value explicitly instead of hiding it.
- [ ] You choose a team structure — centralized, embedded, or hybrid — that fits the organization's actual size, using Conway's Law deliberately.
- [ ] You hire against a specific, evidenced gap, not a general feeling that the team is busy.
- [ ] You run a real build-versus-buy scorecard before defaulting to either option.
- [ ] You can name the specific, non-technical habits that turn a well-built platform into one an organization actually uses by default.

---

## Exercises

Use `companion/ch66/maturity_scorecard.csv` and `roi_case.csv`.

### Warm-up

1. Write the five parts of a one-page data strategy from memory, in order.
2. Why is scoring a maturity assessment honestly more valuable than scoring it to look good in a presentation?
3. Name the three team topologies from section 66.4, and one advantage and one risk of each.
4. What's the difference between showback (Chapter 65) and a business case? Where do they overlap?
5. State the general build-versus-buy rule from section 66.5 in one sentence.

### Core

6. Reproduce section 66.2's maturity scorecard. Which dimension is weakest, and does the evidence given actually support that score?
7. Reproduce section 66.3's ROI calculation. What percentage of the platform's annual cost do the measured savings cover, what does PO intake add, and which single saving is largest?
8. Write the "unmeasured ceiling" paragraph for Riverstone's business case, naming at least three sources of real but unquantified value, each tied to a specific earlier chapter.
9. Using Conway's Law (Chapter 62, section 62.8), explain why Riverstone's move toward a hybrid team structure needs the Taloja plant's own analyst to exist before that structure can actually work, not just be diagrammed.
10. Score a build-versus-buy decision for a capability not covered in this chapter (a BI tool, a monitoring dashboard) using section 66.5's five dimensions.
11. A stakeholder asks why the data platform team needs another hire when "the last three months have looked fine." Using section 66.4's hiring principle, how do you respond?
12. Riverstone's maturity scores data-driven culture at 2.2, the second-lowest dimension. Propose one specific, non-technical action (not a new tool) that would move it toward 3.0 within six months.

### Stretch

13. Recompute the ROI case assuming the defect-detection model's avoided losses could be estimated (invent a reasonable, clearly-labelled figure) and add it to the savings total, PO intake included. How does the platform's cost-coverage percentage change?
14. Design the one-page strategy for Riverstone three years further into its story, assuming the catalog-owner hire succeeded and the AI applications team has grown. What would "where we're going" say at that later stage?
15. Interview (or imagine an interview with) someone who manages a data team, and ask them to score their own organization against section 66.2's six dimensions. Where does their honest score surprise you?

### Think about it

16. Is it ever appropriate to present an inflated business case, if you're confident the investment is right and worried an honest one won't get approved? What's the risk in doing so?
17. A vendor's "buy" option in a build-versus-buy scorecard is actually worse on every dimension except cost, for a capability your team considers core to its competitive advantage. When should "build" win despite that?

---

## Answers

**1.** Where we are; where we're going; why these and not others; how we'll know it's working; what we need to get there.

**2.** A flattering score hides the exact gap a strategy most needs to close, and leadership ends up investing in what already looks good rather than what actually needs attention — the assessment's entire value is as an honest diagnostic, and an inflated one is worse than none, because it creates false confidence.

**3.** Centralized: simple to govern, scales poorly past a certain size (queues form behind one team). Embedded: fast, close to domain expertise, risks duplicated/disagreeing work across domains (Chapter 63's audit found Delhi and Kolkata each running their own version of the consolidation macro). Hybrid: central platform and standards with embedded specialists using them — the best of both, but requires real domain capacity to exist first (Conway's Law).

**4.** Showback reports what a team is already spending, without judgment about whether it should continue. A business case argues for a *new* or *continued* spend, and must show the value against the cost, not just the cost alone. They overlap in that a credible business case should use the same real, checkable cost figures showback already reports, not a separately-estimated number.

**5.** Buy when the capability is common enough that a vendor has already solved it well; build when your need is genuinely, verifiably different from everyone else's.

**6.** Catalog and discoverability, at 1.8, is the weakest (stage 1 fully met, four of the five stage-2 criteria). The evidence supports a low score: finding the right table still depends on asking Meera's team, and Chapter 63's audit found 11 automations that team had never heard of — nothing about finding data works without a person. Data-driven culture (2.2) comes next; its evidence ("individual wins… most decisions still made by habit and hierarchy") distinguishes isolated successes from routine behavior, which is exactly what a stage 2–3 boundary should hinge on.

**7.** The measured savings, the Flash and the macro, are ₹97,577 of ₹4,53,360, about 22%. PO intake's ₹1,00,750 takes the total to ₹1,98,327, about 44%, but only if the reviewers catch at least 97% of wrong drafts. PO intake is the largest single saving, narrowly ahead of the Daily Flash (₹97,500); the branch macro is a distant third (₹77), because its real value is accuracy, not time.

**8.** For example: the defect model's avoided cost of shipping defective product (Chapter 53) — real but requires estimating a counterfactual; the support assistant's and CRM sync's diffused time savings (Chapters 51, 55) spread across many small interactions rather than concentrated enough to total cleanly; the value of decisions the platform newly makes possible, like the regional lead-scoring fix (Chapter 64), which has no "before" baseline to compare against because nothing equivalent was being measured previously.

**9.** Per Conway's Law, an organization's structure and its architecture end up mirroring each other; a hybrid structure diagrammed without a real domain team behind it is just a centralized team wearing a different label, exactly Chapter 62's point about the vendor's proposed three-domain mesh that had no actual domain teams underneath it. The Taloja analyst's real existence — actual capacity, actually reporting into that domain — is what makes the hybrid diagram describe something real rather than aspirational.

**10.** Personal exercise; check the scoring addresses all five dimensions (time to solution, fit, maintenance, cost, lock-in) individually rather than jumping to a single verdict.

**11.** Point to the specific, named gap the hire closes (section 66.2's maturity assessment, or a recurring, costly request the current team has had to turn away), not the team's general busyness — "the last three months looked fine" describes workload, not whether a specific capability gap is costing the organization something measurable. If no such specific gap exists yet, that's itself useful information: the hire isn't justified yet, per this chapter's own principle.

**12.** For example: require that any monthly leadership review include one slide sourced directly from a Riverstone dashboard rather than a manually-prepared summary — a small, concrete habit change that routes at least one recurring decision-making moment through the platform by default, rather than a broader "be more data-driven" initiative with no specific mechanism behind it.

**13.** With an invented, clearly-labelled figure — for example, ₹1,50,000 a year in avoided defective shipments, which is about 38 missed defects avoided a year at Chapter 53's ₹4,000 per miss (₹1,50,000 ÷ ₹4,000 = 37.5) — the savings total rises from ₹1,98,327 to ₹3,48,327, and coverage from 44% to about 77%. That is still short of 100%, which is itself worth noting: even adding one more estimable source doesn't fully close the gap, reinforcing that some value genuinely resists this kind of accounting. And the new line is an estimate, so it must be labelled as one.

**14.** At that later stage, "where we're going" would plausibly shift from closing foundational gaps (finding data, cost habits) toward genuine differentiation — perhaps extending the platform's AI capabilities to a new business line, or beginning a real, evidence-triggered move toward a data mesh (Chapter 62) now that a second and third domain team have their own capacity, if that trigger has by then actually arrived.

**15.** Personal exercise; there's no single correct answer, though most real organizations, scored honestly, show a similar pattern to Riverstone's: stronger on technical dimensions that were deliberately engineered, weaker on the organizational habits that require sustained practice rather than a single project to build.

**16.** It's rarely appropriate, and the risk is exactly what Meera's story illustrates in reverse: an inflated case that doesn't survive the first hard question damages trust in every future case from the same source, permanently, in a way that costs far more than one delayed or declined investment. If the investment is genuinely right, the honest case — showing the real floor and naming the real ceiling — is very often persuasive enough on its own, as it was for Riverstone's catalog-owner hire.

**17.** When the capability genuinely is core to competitive advantage — meaning competitors having access to the same vendor tool would erode a real, specific edge — cost and convenience legitimately take a back seat to control and differentiation. The test is whether "core to our competitive advantage" is actually true and specific, or a comfortable-sounding justification for a preference to build; a data catalog, honestly assessed, essentially never clears that bar, but a company's actual proprietary model or algorithm often does.

---

## Where this leads

- **Chapter 62, Data Architecture Patterns:** Conway's Law and the mesh-maturity method this chapter's assessment and team-structure sections directly extend.
- **Chapters 63 and 64:** the automation audit and the governance section that found the catalog gap this chapter's hire closes.
- **Chapter 65, FinOps:** the real cost figure this chapter's business case is measured against.
- **Chapters 19, 20, 58:** the three automations whose savings anchor the honest ROI case.
- **Chapter 67, The Architect as Leader:** the final chapter, where strategy, maturity, and the business case become one person's actual responsibility — leading the organization this chapter has been describing, not just analyzing it.
- **Interview preparation:** the Architecture & Leadership Question Bank asks directly about building a data team and justifying platform investment — "how would you make the case for headcount or budget" is this chapter's method.
