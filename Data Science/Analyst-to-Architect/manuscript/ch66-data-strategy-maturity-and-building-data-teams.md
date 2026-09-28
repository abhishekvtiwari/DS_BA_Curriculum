# Chapter 66. Data Strategy, Maturity & Building Data Teams

*Part 7 — Architecture, Governance & Leadership*

> **Chapter at a glance**
>
> **You will learn to:** write a data strategy that fits on one page and actually gets used · score an organization's data maturity honestly, across the dimensions that matter, not just the ones that flatter it · build a real business case for data platform investment, including the uncomfortable parts a case usually leaves out · choose a team structure — centralized, embedded, or hybrid — that fits the organization's actual size, and hire against a named gap rather than a vague sense that "we need more people" · decide when to build a capability and when to buy it, with a real framework rather than a preference · lead change in an organization that doesn't yet trust data by default.
>
> **Before you start:** this chapter draws together every earlier Part 7 chapter into an organizational and strategic view: the platform (Chapter 60), its trade-offs (61), its architecture pattern (62), its governance (63), its security (64), and — directly — its real cost (65).
>
> **Time needed:** 8–10 hours, spread over a week.
>
> **Tools:** `pandas` for the maturity scorecard and ROI model (run here on Python 3.12, pandas 3.0.2).
>
> **Practice data:** `companion/ch66/`: `maturity_scorecard.csv` (a real five-dimension maturity assessment for Riverstone) and `roi_case.csv` (a real, honest business case built from figures already established in earlier chapters).

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
4. **How we'll know it's working** — a small number of measurable signals, in Chapter 21's vocabulary: real numbers, not adjectives.
5. **What we need to get there** — people, budget, and the single biggest risk to the plan.

**Riverstone's own, written at this point in its story:** *Where we are: a governed, secured, cost-transparent centralized platform (Chapters 60–65), serving one company well. Where we're going: closing the two gaps our own maturity assessment finds weakest — cost discipline as a routine habit, not a one-time model, and a data-driven culture that reaches for the platform by default. Why these: the platform's technical foundation is solid; the organization around it is the constraint now, not the technology. How we'll know: a monthly (not annual) cost review actually happening, and a rising share of decisions that cite a dashboard rather than a hunch, tracked deliberately. What we need: one governance hire (section 66.4), and continued executive attention through the next two budget cycles, since none of this compounds in under a year.*

---

## 66.2 Maturity models, scored honestly

A **maturity model** describes stages an organization's data capability typically passes through — usually something like *ad hoc* (nothing formalized, works by heroics), *reactive* (fixes problems after they occur), *proactive* (problems anticipated and designed against), *managed* (measured, monitored, continuously improved), and *optimized* (a genuine competitive advantage, not just table stakes). Its value isn't the taxonomy — it's the discipline of scoring yourself against it honestly, the same discipline Chapter 62's mesh-readiness check applied to one specific question, generalized here to the whole organization.

```python
import pandas as pd
pd.set_option("display.width", 100)

maturity = pd.read_csv("maturity_scorecard.csv")
print(maturity.to_string(index=False))
print(f"\naverage stage: {maturity['stage'].mean():.2f}")
print(f"weakest dimension: {maturity.loc[maturity['stage'].idxmin(), 'dimension']} ({maturity['stage'].min()})")
print(f"strongest dimension: {maturity.loc[maturity['stage'].idxmax(), 'dimension']} ({maturity['stage'].max()})")
```

```
                 dimension  stage                                                                                              evidence
Data quality & reliability    3.6        Automated tests (Ch 47), reconciled pipelines (Ch 14), but not every source has a contract yet
   Architecture & platform    3.2                           A designed, documented platform (Ch 60-62) — still centralized, still young
     Governance & security    3.4                 A real access model and fairness audits exist (Ch 63-64) — not yet company-wide habit
           Cost discipline    2.6                  A real cost model exists (Ch 65) — but it was built once, not yet a routine practice
       Data-driven culture    2.2 Individual wins (Ch 19, 24) — most decisions still made by habit and hierarchy, not routinely by data

average stage: 3.00
weakest dimension: Data-driven culture (2.2)
strongest dimension: Data quality & reliability (3.6)
```

![Five dimensions plotted against a five-stage maturity model: data quality at 3.6, architecture at 3.2, governance at 3.4, cost discipline at 2.6, and data-driven culture at 2.2 — Riverstone sits mostly in stage 3, Proactive](figures/fig66-1-maturity-model.svg)

*Figure 66.1 — The honest picture: technical dimensions score well; the organizational ones (cost as a routine habit, a culture that reaches for data by default) lag behind. This is normal, not a failure — it's exactly the gap a strategy exists to close.*

**What the low scores actually mean, read correctly:** cost discipline scoring 2.6 doesn't mean Chapter 65's cost model was bad work — it means a model built once, brilliantly, is not the same thing as a *habit* of checking it every month, which is what a stage-4 organization would actually be doing. Data-driven culture scoring 2.2 doesn't mean nobody at Riverstone uses data — it means most decisions are still made the way they always were, by hierarchy and habit, with the platform consulted occasionally rather than by default. **A maturity assessment's job is distinguishing "we built the thing" from "the thing has become how we normally operate,"** and those are honestly different achievements, often separated by a year or more of consistent practice rather than any further engineering.

> **Watch out: a maturity model scored to flatter itself is worse than no assessment at all.** The temptation, especially when presenting to leadership, is to round every score up half a stage. A maturity assessment's only value is as an honest diagnostic; an inflated one actively prevents the organization from seeing the gap it most needs to close.

---

## 66.3 Building the business case — including the part it usually leaves out

A business case for continued data platform investment is only as credible as its willingness to show its weakest number, not just its strongest one. Here is Riverstone's, built honestly from figures already established across this book rather than invented for the occasion.

```python
roi = pd.read_csv("roi_case.csv")
print(roi.to_string(index=False))

platform_cost = roi.loc[roi.item.str.contains("annual cost"), "amount_rs"].iloc[0]
three_known = roi.loc[roi.item.str.contains("three known automations, total"), "amount_rs"].iloc[0]
coverage_pct = three_known / platform_cost * 100
print(f"\nThree real, quantified automations cover {coverage_pct:.0f}% of the platform's annual cost.")
```

```
                                                             item  amount_rs
                         Riverstone platform, annual cost (Ch 65)  456168.00
                     Daily Flash time saved, annual value (Ch 20)   97500.00
      Branch macro time saved, annual value (Ch 19, conservative)    5775.00
  PO-intake assisted-mode saving vs. fully manual, annual (Ch 58)  100500.00
       Quantified savings, two automations only (incomplete case)  103275.00
   Quantified savings, three known automations (still incomplete)  203775.00
               Platform pays for itself, two automations only (x)       0.23
            Platform pays for itself, three known automations (x)       0.45
Proposed new hire: data governance / catalog owner, annual salary  900000.00
IndexError: single positional indexer is out-of-bounds
```

![A bar chart: the platform's Rs 456,168 annual cost against three real, individually quantified automations (Daily Flash Rs 97,500, branch macro Rs 5,775, PO-intake Rs 100,500), totaling Rs 203,775 — 45% of the platform's cost](figures/fig66-4-roi-case.svg)

*Figure 66.4 — The honest version of a business case: three real, checkable savings figures cover less than half the platform's cost, on paper. The rest of the value is real but harder to put a number on — and a credible case says so.*

**This is the finding a less honest business case would have hidden, and it's the more useful one.** Three individually verifiable, previously-computed savings figures — the Daily Flash (Chapter 20), the branch consolidation macro (Chapter 19), and PO-intake's assisted mode over fully manual entry (Chapter 58) — add up to ₹203,775 a year, against a platform that costs ₹456,168 a year to run. **On the numbers alone, the platform looks like a net cost.**

**What a credible business case does with that finding is not hide it — it explains what the accounting is missing:**

- **The defect-detection model** (Chapter 53) prevents shipping defective product; its value is real but shows up as *avoided cost*, which is genuinely harder to quantify than *time saved*, because it requires estimating what would have happened without it.
- **The support assistant** (Chapter 55) and **CRM reverse-ETL sync** (Chapter 51) both save time that's diffused across many small interactions rather than concentrated in one measurable process, and diffused savings are real but resist a clean per-year number.
- **The platform enables decisions that wouldn't otherwise be made at all** — Chapter 62's fairness-audit finding about regional lead scoring, or Chapter 64's own fairness audit, produced value (a faster-growing East region, a corrected model) that has no "hours saved" analog whatsoever, because nothing was being done manually before to compare against.
- **Some value is optionality**, not immediate return: the platform being ready to support a new AI system, a new regulation, or a new region is worth something even in a year that value isn't drawn on.

**The honest version of the business case, stated the way it should actually be presented:** *"Three individually quantified automations alone justify 45% of the platform's cost. The remainder is real value we haven't built a clean way to measure yet — avoided errors, diffused time savings, and decisions the platform makes possible that weren't happening at all before. We're not asking you to trust an unmeasured number; we're asking you to recognize that the measured floor is already substantial, and the unmeasured ceiling is real."* That sentence survives a skeptical CFO's question in a way that a single inflated ROI multiple never would.

---

## 66.4 Hiring and structuring data teams

**Three team topologies**, each fitting a different scale, and Chapter 62's Conway's Law (section 62.7) governing the choice exactly as it governed the centralized-versus-mesh decision:

- **Centralized:** one team serves the whole organization — Riverstone's structure since Chapter 60, and the right fit while one team can serve without a persistent queue behind it.
- **Embedded:** data people sit inside each business function, reporting to that function rather than to a central data team. Scales domain expertise and responsiveness; risks exactly the duplicated, disagreeing logic Chapter 62's story found when two branches each built their own version of the same macro.
- **Hybrid** (sometimes called "hub and spoke"): a central team owns the platform, standards, and shared services (Chapter 63); embedded specialists sit in each function, using that shared platform rather than building their own. This is where Riverstone is now visibly heading, one hire at a time.

![Three stages: the four-person team from Chapter 60, today with the Taloja plant's own data analyst added, and a proposed next hire — a data governance and catalog owner, justified by a specific gap this book already found](figures/fig66-2-team-evolution.svg)

*Figure 66.2 — Each hire is justified by a named gap, not a general sense that the team is stretched. That discipline is the whole difference between structured growth and headcount creep.*

**The Taloja plant's data analyst (Chapter 62) was Riverstone's first hybrid-model hire**, and it was justified by a specific, observed signal: a domain with real capacity that wanted to own its own data, exactly the trigger section 62.6's maturity check said to wait for rather than guess at. **The next proposed hire follows the same discipline**, not a general one: section 66.2's maturity assessment names governance and cataloging as a specific, scored weak point, and Chapter 63's automation audit and Chapter 64's access-control work both surfaced the same gap independently — nobody currently owns making data discoverable and consistently governed across the whole platform, as opposed to within any one pipeline.

**A hiring principle worth stating explicitly**, because it's the one this book's own story keeps demonstrating: **hire against a named, evidenced gap, not against a feeling that the team is busy.** A team that's busy building things nobody asked for is not understaffed; it's misdirected. A team that's turning away a specific, recurring, costly request is understaffed in a way a resume can be written against.

---

## 66.5 Build versus buy

Every capability this book has taught you to build has an alternative: **buy something that already does it.** The decision is not a preference for engineering purity versus pragmatism — it's a real trade-off, worth scoring the same disciplined way as any other architectural choice.

![A build-versus-buy scorecard for a managed data catalog: time to working solution, fit to exact needs, maintenance burden, cost at current scale, and lock-in risk — buy wins on four of five dimensions](figures/fig66-3-build-vs-buy.svg)

*Figure 66.3 — At a four-person team's scale, buying a catalog wins on nearly every dimension. The one place build wins — perfect fit — usually isn't worth what it costs to get there.*

**The worked example: Riverstone's data catalog**, the specific gap section 66.2's maturity assessment and Chapter 64's own governance section both identified. Scored honestly:

- **Time to a working solution:** a managed catalog tool is usable in weeks; a custom-built one is months of a four-person team's scarce time.
- **Fit to exact needs:** building wins here, eventually — a custom catalog can match Riverstone's exact workflow perfectly. The word "eventually" is doing real work: it means months of iteration a small team doesn't have to spare.
- **Ongoing maintenance:** a bought tool's maintenance is the vendor's problem; a built one's maintenance is the same four-person team that's already stretched thin, forever, on top of everything else they own.
- **Cost at current scale:** a subscription is predictable and budgetable; engineering time spent building and maintaining a catalog is real cost that simply doesn't show up as a line item on the bill Chapter 65 modeled.
- **Lock-in risk:** genuinely the one point in the vendor's favor to weigh honestly — a bought tool creates real switching cost. But an unbought, unmaintained internal tool that only one person on a four-person team understands is its own kind of lock-in, arguably a worse one, since nobody outside the company can be hired to fix it.

**The general rule the scorecard supports:** **buy when the capability is common enough that a vendor has already solved it well, and build when your need is genuinely different from everyone else's.** A data catalog, honestly, is not different at Riverstone from at any other mid-size company — which is exactly why buying wins here, and exactly the kind of judgment call Chapter 60's fit-over-fashion principle was always really about.

---

## 66.6 Change management and data culture

The hardest part of everything this Part has taught is not technical, and it's also not new information at this point in the book — it's a pattern this book's own stories have already shown you, repeatedly, without naming it as change management until now.

**Chapter 19's story** — a macro that ran unowned for nine years — wasn't a technology failure. It was a culture where nobody felt empowered, or responsible, to ask "does this still work correctly?" **Chapter 63's shadow-IT audit** found 24 automations, 18 of them ungoverned, not because anyone was careless, but because the *habit* of checking in with a central platform team had never been built — every team solved its own problem, quietly, because that was simply how things had always been done. **Chapter 62's vendor-pitch story** worked precisely because Anita Rao's culture already valued an honest scorecard over an exciting pitch — a culture that took real, deliberate effort to build, not a default state.

**Four habits that build a data-driven culture, none of them technical:**

1. **Make the easy path the governed path** (Chapter 63's own lesson, generalized): a shared service that's genuinely easier to use than the workaround gets adopted; a mandate that's harder to follow than the old way gets quietly routed around.
2. **Celebrate the audit finding, not just the fix** — Chapter 63's story treated every discovered gap as useful information, not a failure to be embarrassed about, which is exactly why the next round of questions got honest answers.
3. **Put the data where the decision is being made**, not in a separate report nobody opens — Chapter 20's Daily Flash succeeded specifically because it arrived where the decision-maker already was, rather than requiring them to go looking for it.
4. **Model the behavior from the top** — Anita Rao declining the vendor's pitch on the strength of a scorecard, in front of the team, taught more about the culture Riverstone wanted than any policy document could have.

**The uncomfortable truth this section closes on:** a data platform this well-designed, this well-governed, this honestly costed, can still fail — not technically, but organizationally — if nobody changes how decisions actually get made day to day. The technical work in Chapters 60 through 65 was necessary. This chapter's work is what makes it sufficient.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| A strategy document longer than one page | Nobody on the team can recall what it actually says | Force it to one page; that constraint is the discipline |
| A strategy with no explicit "no" | Everything is a priority, so nothing is | State what you're deliberately not doing this year, and why |
| A maturity assessment scored to flatter itself | Leadership never sees the real gap that needs closing | Score honestly; the diagnostic's only value is accuracy |
| A business case that hides its weak numbers | It collapses the moment someone asks a hard question | Show the measured floor and name the unmeasured ceiling explicitly |
| Treating unquantified value as if it doesn't exist | Real benefits (avoided errors, culture change) get left out of the case entirely | Name them explicitly, even without a precise number |
| Hiring because the team "feels busy" | Headcount grows without a specific gap it closes | Hire against a named, evidenced gap, the way Chapter 62's Taloja hire was |
| Building a capability a vendor already sells well | Months of a small team's time spent reinventing a data catalog | Score build vs. buy honestly; buy when the need isn't genuinely unique |
| Assuming the culture will follow the technology | A brilliant platform nobody routes decisions through | Make the governed path the easy path; put data where decisions happen |
| Punishing an audit finding instead of using it | The next audit gets less honest answers | Treat every gap found as useful information, the way Chapter 63's story did |
| Confusing "we built it" with "it's how we operate" | A capability exists but isn't yet a habit | Track adoption and routine use, not just deployment |

---

## In the real world: the business case that told the truth

When Meera prepared the proposal for Riverstone's next data-platform hire — the governance and catalog owner section 66.4 names — her first draft of the business case did what most first drafts do: it rounded every benefit up and left out everything hard to measure. The platform, by that draft's accounting, "paid for itself many times over," a sentence that felt true and that she couldn't actually defend line by line if anyone asked her to show the arithmetic.

She rewrote it after a conversation with Vikram Singh, who'd sat through enough budget reviews to know the difference between a number that survives questioning and one that only sounds confident. His question was simple: *"If the CFO asks you to walk through exactly how you got that multiple, can you?"* She couldn't, not for the inflated version.

The rewrite was the honest one: three real, individually verifiable automations, adding up to 45% of the platform's annual cost — a real number, checkable in an afternoon by anyone who wanted to. And then, deliberately, a second section that didn't try to manufacture a number for everything else: the defect model's avoided losses, the support assistant's diffused time savings, the fairness-audit fixes that had no "before" state to compare against because nothing was being measured that way previously.

The proposal went to Anita Rao with both halves intact. Her response, reportedly, was that the honest 45% was more persuasive than the earlier draft's inflated multiple had ever been — not because the number was bigger, but because she could trust every rupee in it, and trusting the measured part made her willing to believe the unmeasured part was real too. The hire was approved within the month.

Nine months later, with the catalog owner in place and Chapter 64's cataloging gap closed, Meera ran the same honest accounting again. The measured floor had grown — the new hire's own work was itself now a quantifiable line, since a data catalog's discoverability gains could finally be measured in time-to-find, before and after. The business case hadn't just paid for one hire; it had become a template Riverstone now used for every subsequent one.

What made the difference:

- **She showed the weak number rather than hiding it**, and it turned out to be more persuasive, not less, because it was checkable.
- **She named the unmeasured value explicitly, without pretending to quantify it** — the honest gap between what's measured and what's real became part of the case, not an embarrassment to paper over.
- **The rewritten case became reusable infrastructure of its own** — a template for every future proposal, not a one-time document.
- **Trust compounded**: the more honest the first case, the more credit the next one was given before anyone even checked its numbers.

---

## Project: write a one-page strategy and an honest business case

**Goal:** produce a real, one-page data strategy and a business case for one specific investment, both built to survive a skeptical reader's questions.

### Tools you'll need

- **Python 3.13 or 3.14** with `pandas` for the maturity scorecard and business-case model (run here on Python 3.12, pandas 3.0.2).
- **No specialized software required** — a strategy on a page, a maturity scorecard, and a business case are documents and disciplined arithmetic, not tools to buy.
- **Companion files (`companion/ch66/`):**
  - `build_ch66_files.py`: builds both the maturity scorecard and the ROI model from figures already established in Chapters 19, 20, 58, and 65.
  - `maturity_scorecard.csv`: the five-dimension assessment behind Figure 66.1.
  - `roi_case.csv`: the honest business case behind Figure 66.4, including both the measured floor and the explicit gap to the platform's full cost.

**Option A: your own organization.** Write the strategy for a team or function you actually work in.

**Option B: Riverstone.** Extend section 66.1's strategy with your own maturity assessment (Option: reuse or re-score `maturity_scorecard.csv`), and build the business case for a different next investment — not the governance hire this chapter already made, but something else the maturity gaps suggest.

**Steps**

1. **Write the one-page strategy** using section 66.1's five parts. If it doesn't fit on one page, cut, don't shrink the font.
2. **Score maturity honestly** across at least four dimensions relevant to your context, each with a one-sentence piece of evidence — not a number alone.
3. **Identify the weakest dimension**, and make it the subject of the "where we're going" section of your strategy.
4. **Build a business case** for one specific investment the maturity gap justifies. Include at least one number you can defend line by line, and at least one piece of value you explicitly can't quantify — named honestly, not hidden.
5. **Propose a hire, if relevant**, justified against a specific, evidenced gap — not a general sense of being stretched.
6. **Run a build-versus-buy scorecard** for one capability under consideration, using section 66.5's five dimensions.
7. **Name one change-management action** — not a policy, a specific habit-level change — that would move your weakest maturity dimension forward.

**What good looks like:** the strategy genuinely fits one page; the maturity scores include at least one uncomfortable finding; the business case shows its weakest number rather than hiding it; the hire or build/buy recommendation is traceable to a specific piece of evidence, not a feeling.

**Stretch goals**

- Take a business case you've actually written (or seen) at work, and rewrite it using this chapter's "show the floor, name the ceiling" method. Does it become more or less persuasive?
- Score Riverstone's maturity a year further into its story (imagine the effects of the governance hire, a year of monthly cost reviews) and redraw Figure 66.1.
- Interview someone who's led a data team's growth, and ask them to name one hire they made against a real, evidenced gap, and one they now recognize was made on a feeling alone.

---

## Recap

- **A one-page data strategy** — where we are, where we're going, why, how we'll know, what we need — is a discipline that forces real decisions, not a formatting preference.
- **A maturity model** scored honestly shows Riverstone strongest on the technical dimensions (data quality, architecture, governance) built across Chapters 60–64, and weakest on the organizational ones (cost as a routine habit, a genuinely data-driven culture) — a completely normal, expected gap.
- **A credible business case shows its weakest number**: three real, quantified Riverstone automations cover 45% of the platform's annual cost, and the honest remainder is named explicitly rather than papered over with an inflated multiple.
- **Team structure** — centralized, embedded, or hybrid — follows Conway's Law; Riverstone is visibly moving toward hybrid, one hire at a time, each justified against a specific, evidenced gap rather than general growth.
- **Build versus buy** is a real, scoreable trade-off; a capability common enough that vendors already solve it well (a data catalog) usually favors buying, especially for a small team.
- **Culture is the hardest, least technical part of everything this Part has built**, and this book's own earlier stories — the nine-year-old unowned macro, the shadow-IT audit, the declined vendor pitch — were change-management lessons all along, before this chapter named them as such.

---

## Key terms

data strategy · one-page strategy · maturity model · maturity stage · business case · measured floor · unmeasured ceiling · team topology · centralized team · embedded team · hybrid (hub and spoke) team · Conway's Law (Chapter 62) · build versus buy · vendor lock-in · change management · data culture · showback (Chapter 65)

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can write a data strategy that fits on one page and says no to something explicitly.
- [ ] You score maturity plainly, including dimensions that reflect poorly on work you're proud of.
- [ ] You build a business case that shows its weakest, most defensible number rather than an inflated one, and names unquantified value explicitly instead of hiding it.
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
7. Reproduce section 66.3's ROI calculation. What percentage of the platform's annual cost do the three known automations cover, and which one contributes most?
8. Write the "unmeasured ceiling" paragraph for Riverstone's business case, naming at least three sources of real but unquantified value, each tied to a specific earlier chapter.
9. Using Conway's Law (Chapter 62, section 62.7), explain why Riverstone's move toward a hybrid team structure needs the Taloja plant's own analyst to exist before that structure can actually work, not just be diagrammed.
10. Score a build-versus-buy decision for a capability not covered in this chapter (a BI tool, a monitoring dashboard) using section 66.5's five dimensions.
11. A stakeholder asks why the data platform team needs another hire when "the last three months have looked fine." Using section 66.4's hiring principle, how do you respond?
12. Riverstone's maturity scores data-driven culture at 2.2, the lowest dimension. Propose one specific, non-technical action (not a new tool) that would move it toward 3.0 within six months.

### Stretch

13. Recompute the ROI case assuming the defect-detection model's avoided losses could be estimated (invent a reasonable, clearly-labelled figure) and add it to the "known, quantified savings" total. How does the platform's cost-coverage percentage change?
14. Design the one-page strategy for Riverstone three years further into its story, assuming the governance hire succeeded and the AI applications team has grown. What would "where we're going" say at that later stage?
15. Interview (or imagine an interview with) someone who manages a data team, and ask them to score their own organization against section 66.2's five dimensions. Where does their honest score surprise you?

### Think about it

16. Is it ever appropriate to present an inflated business case, if you're confident the investment is right and worried an honest one won't get approved? What's the risk in doing so?
17. A vendor's "buy" option in a build-versus-buy scorecard is actually worse on every dimension except cost, for a capability your team considers core to its competitive advantage. When should "build" win despite that?

---

## Answers

*(In the finished book these move to Appendix G.)*

**1.** Where we are; where we're going; why these and not others; how we'll know it's working; what we need to get there.

**2.** A flattering score hides the exact gap a strategy most needs to close, and leadership ends up investing in what already looks good rather than what actually needs attention — the assessment's entire value is as an honest diagnostic, and an inflated one is worse than none, because it creates false confidence.

**3.** Centralized: simple to govern, scales poorly past a certain size (queues form behind one team). Embedded: fast, close to domain expertise, risks duplicated/disagreeing work across domains (Chapter 62's two-macro story). Hybrid: central platform and standards with embedded specialists using them — the best of both, but requires real domain capacity to exist first (Conway's Law).

**4.** Showback reports what a team is already spending, without judgment about whether it should continue. A business case argues for a *new* or *continued* spend, and must show the value against the cost, not just the cost alone. They overlap in that a credible business case should use the same real, checkable cost figures showback already reports, not a separately-estimated number.

**5.** Buy when the capability is common enough that a vendor has already solved it well; build when your need is genuinely, verifiably different from everyone else's.

**6.** Data-driven culture, at 2.2, is the weakest. The evidence given ("individual wins... most decisions still made by habit and hierarchy") does support a low score specifically because it distinguishes isolated successes from routine organizational behavior, which is exactly what a stage 2-3 boundary should hinge on.

**7.** ₹203,775 of ₹456,168, about 45%. PO-intake contributes the most (₹100,500), narrowly ahead of the Daily Flash (₹97,500); the branch macro is a distant third (₹5,775).

**8.** For example: the defect model's avoided cost of shipping defective product (Chapter 53) — real but requires estimating a counterfactual; the support assistant's and CRM sync's diffused time savings (Chapters 51, 55) spread across many small interactions rather than concentrated enough to total cleanly; the value of decisions the platform newly makes possible, like the regional lead-scoring fix (Chapter 62, 64), which has no "before" baseline to compare against because nothing equivalent was being measured previously.

**9.** Per Conway's Law, an organization's structure and its architecture end up mirroring each other; a hybrid structure diagrammed without a real domain team behind it is just a centralized team wearing a different label, exactly Chapter 62's point about the vendor's proposed three-domain mesh that had no actual domain teams underneath it. The Taloja analyst's real existence — actual capacity, actually reporting into that domain — is what makes the hybrid diagram describe something real rather than aspirational.

**10.** Personal exercise; check the scoring addresses all five dimensions (time to solution, fit, maintenance, cost, lock-in) individually rather than jumping to a single verdict.

**11.** Point to the specific, named gap the hire closes (section 66.2's maturity assessment, or a recurring, costly request the current team has had to turn away), not the team's general busyness — "the last three months looked fine" describes workload, not whether a specific capability gap is costing the organization something measurable. If no such specific gap exists yet, that's itself useful information: the hire isn't justified yet, per this chapter's own principle.

**12.** For example: require that any monthly leadership review include one slide sourced directly from a Riverstone dashboard rather than a manually-prepared summary — a small, concrete habit change that routes at least one recurring decision-making moment through the platform by default, rather than a broader "be more data-driven" initiative with no specific mechanism behind it.

**13.** With an invented, clearly-labeled figure (for example, ₹150,000/year in avoided defective-shipment costs, sized plausibly against the ₹4,000-per-miss figure established in Part 6), the total known savings would rise to roughly ₹353,775, moving coverage from 45% to about 78% — still short of 100%, which is itself worth noting: even adding one more real, estimable source doesn't fully close the gap, reinforcing that some value genuinely resists this kind of accounting.

**14.** At that later stage, "where we're going" would plausibly shift from closing foundational gaps (governance, cost habits) toward genuine differentiation — perhaps extending the platform's AI capabilities to a new business line, or beginning a real, evidence-triggered move toward a data mesh (Chapter 62) now that a second and third domain team have their own capacity, if that trigger has by then actually arrived.

**15.** Personal exercise; there's no single correct answer, though most real organizations, scored honestly, show a similar pattern to Riverstone's: stronger on technical dimensions that were deliberately engineered, weaker on the organizational habits that require sustained practice rather than a single project to build.

**16.** It's rarely appropriate, and the risk is exactly what Meera's story illustrates in reverse: an inflated case that doesn't survive the first hard question damages trust in every future case from the same source, permanently, in a way that costs far more than one delayed or declined investment. If the investment is genuinely right, the honest case — showing the real floor and naming the real ceiling — is very often persuasive enough on its own, as it was for Riverstone's governance hire.

**17.** When the capability genuinely is core to competitive advantage — meaning competitors having access to the same vendor tool would erode a real, specific edge — cost and convenience legitimately take a back seat to control and differentiation. The test is whether "core to our competitive advantage" is actually true and specific, or a comfortable-sounding justification for a preference to build; a data catalog, honestly assessed, essentially never clears that bar, but a company's actual proprietary model or algorithm often does.

---

## Where this leads

- **Chapter 62, Data Architecture Patterns:** Conway's Law and the mesh-maturity method this chapter's assessment and team-structure sections directly extend.
- **Chapter 65, FinOps:** the real cost figure this chapter's business case is measured against.
- **Chapters 19, 20, 58:** the three real automations whose savings anchor the honest ROI case.
- **Chapter 67, The Architect as Leader:** the final chapter, where strategy, maturity, and the business case become one person's actual responsibility — leading the organization this chapter has been describing, not just analyzing it.
- **Interview preparation:** the Architecture & Leadership Question Bank asks directly about building a data team and justifying platform investment — "how would you make the case for headcount or budget" is this chapter's method.
