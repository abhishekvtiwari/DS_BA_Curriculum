# Chapter 75. Product Sense, Metrics, Case Studies & Guesstimates

*Part 8 — The Interview Playbook*

> **Chapter at a glance**
>
> **You will learn to:** structure an ambiguous business case the way an interviewer actually wants, instead of jumping straight to an answer · diagnose a metric that moved, systematically, not by guessing at causes · design a KPI dashboard that answers real decisions, not just displays numbers · size a market or estimate a quantity with a defensible structure, not a guessed final number.
>
> **Before you start:** Chapter 69 (the three answer tiers and the twelve extra-point moves). The questions test Chapters 3 (KPIs, dashboards), 4 (percentage points, estimation), 5 (precise questions, issue trees, MECE), 22 (A/B design, Simpson's paradox), 23 (KPI trees, diagnosing a change, guardrails) and 24 (turning an ask into a question), with a few links to Chapters 15, 16, 25 and 30. This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** 2½–3½ hours to read and drill every question once, out loud; 2–3 hours more for the project.
>
> **How this chapter is built.** Same format as every question bank in Part 8: a memory hook ("Remember it as…"), a one-line answer, and a tier table (**passes**, **strong**, **extra points**, tagged with Chapter 69's moves: **[+Clarify]**, **[+Signpost]** and so on), then follow-ups, the red flag, and where to learn it. Rapid-fire rows end with a level and the section that teaches the idea (a bare number such as 23.10 means that section). There is no code: a case is judged on structure and reasoning. Every number in a worked example is either an assumption, labelled as one, or a figure with its source, and the arithmetic is shown step by step. The chapter moves from the general case framework (section 75.1) through metric diagnosis (75.2), metrics and dashboards (75.3) and product decisions (75.4) to guesstimates (75.5) and two full cases (75.6). Guesstimates need only Chapter 4, so a first-job candidate can do section 75.5 straight after 75.1.
>
> **Levels and roles.** **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds. **DA** data analyst · **BA** business analyst · **PA** product analyst · **BI** BI developer. Do every Fresher question first.

---

## 75.1 The general case framework

### Q75-001 · You're given a vague, one-sentence business question in an interview. Walk through your first sixty seconds

**Level:** Fresher · **Roles:** DA, BA, PA

**Remember it as:** *Restate, clarify, structure, then answer, in that order, every single time, regardless of how simple the question sounds.*

**Answer in one line:** Restate the question in your own words to confirm you understood it, ask one or two clarifying questions that would genuinely change your approach, lay out a structure (a short list of the areas you'll investigate) before touching any specifics, and only then start filling in the structure with actual reasoning.

**Worked example**, applied to *"Our support team wants a way to know which customers to prioritize. How would you help them?"*:

> "Prioritize for what, exactly, retention risk, upsell potential, or urgency of a live issue? And is this a one-time list or a standing, updated view? I'll assume retention risk, updated regularly, unless you say otherwise. I'd look at this in three parts: what signals predict risk, how we'd turn those into a single prioritized list, and how support would actually act on it day to day."

| Tier | What to say |
|---|---|
| Passes | Restates the question, then starts answering with a sensible but unstructured list |
| Strong | Restates, asks one genuinely important clarifying question, states an assumption, and previews a structure before diving in |
| Extra points | **[+Clarify]** the clarifying question changes the actual approach, not a generic "what do you mean"<br>**[+Signpost]** the three-part preview above gives the interviewer a map of where the answer is going, so they can redirect early if it's the wrong direction, rather than sitting through five minutes before finding out |

**Likely follow-ups:** What if the interviewer won't answer your clarifying question? *(State your assumption explicitly and proceed; don't stall waiting for permission.)* How do you know when you've spent too long clarifying and not enough time actually answering?
**Red flag:** either no clarification at all, or clarifying so much it eats most of the available time without ever reaching a structured answer.
**Learn it in:** Chapter 24 §24.1 (turning an ask into a question) and Chapter 5 §5.2 (from a vague request to a precise question). **Practise it with:** Chapter 69, Move 1 (clarify) and Move 3 (signpost).

### Q75-002 · What's the difference between a "diagnose a metric" case and a "should we build this" case, and why does mixing up the structure hurt you?

**Level:** Mid · **Roles:** DA, BA, PA

**Remember it as:** *A metric-drop case works backward from a number to a cause. A product-decision case works forward from a goal to a recommendation. Using the wrong shape wastes the whole case.*

**Answer in one line:** A metric-diagnosis case starts from an observed change and works backward through possible causes (data issue, external factor, internal change, segment-specific shift) to find what actually happened; a product-decision case starts from a goal or user need and works forward through options, trade-offs, and success metrics to reach a recommendation: using a diagnostic structure on a decision question (or vice versa) produces an answer that technically covers ground but never actually answers what was asked.

| Tier | What to say |
|---|---|
| Passes | Describes both kinds of case sensibly, but doesn't say which structure each one needs |
| Strong | Explicitly identifies which of the two shapes the question is (or names a case that's genuinely a hybrid) before choosing a structure |
| Extra points | **[+Signpost]** naming the case type out loud in the first thirty seconds ("this sounds like a diagnostic case, so I'll work backward from the number") itself signals structured thinking to the interviewer, before any content has even been delivered |

**Likely follow-ups:** What's a case that's genuinely a hybrid of both? How would you handle a case where the interviewer's question doesn't clearly signal which type it is?
**Red flag:** applying a rigid, memorized framework to every case regardless of fit, producing a technically thorough but off-target answer.
**Learn it in:** Chapter 5 §5.1 (descriptive, diagnostic, predictive and prescriptive questions). Both shapes are worked in this chapter: diagnostic cases in section 75.2, product decisions in section 75.4.

### Rapid-fire, 75.1

Roles: DA, BA and PA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q75-003 | What's a MECE structure? | Mutually Exclusive, Collectively Exhaustive: a breakdown where categories don't overlap and together cover the whole space | **[+Business]** a non-MECE structure (say, "large customers" and "enterprise customers" as separate buckets) leads to double-counting or gaps that quietly undermine the whole analysis | Fresher · 5.4 |
| Q75-004 | Why state an assumption out loud instead of silently picking one? | It lets the interviewer correct you immediately if you assumed wrong, rather than watching you build fifteen minutes of analysis on the wrong foundation | **[+Assume]** "I'll assume we mean billed revenue; tell me if not": one sentence that invites the correction before it costs you anything | Fresher · 5.5 |
| Q75-005 | How much time should structuring take relative to the whole case? | As a rule of thumb, roughly 10–15% (one to two minutes of a fifteen-minute case): enough to set direction, not so much that there's no time left to actually work through it | **[+Edge cases]** over-structuring (a beautiful framework with no time left to fill it in) scores worse than a slightly rougher structure that's actually worked through | Mid · 69.2 |
| Q75-006 | What's the risk of a purely qualitative answer with zero numbers, in a case that clearly has data available? | It signals an inability or unwillingness to quantify, which is usually exactly what the interviewer is testing for in a data-adjacent role | **[+Business]** even a rough, clearly-labeled estimate ("if I had to guess, maybe 20% of the drop") beats no number at all | Fresher · 4.9 |

---

## 75.2 Diagnosing a metric that moved

### Q75-007 · "Weekly active users dropped 15% last week. Walk me through how you'd figure out why."

**Level:** Fresher · **Roles:** DA, PA, BA

*Weekly active users* (WAU) counts the distinct users who used the product at least once in the week: the same idea as Chapter 3's active customers, counted weekly.

**Remember it as:** *Verify the number is real before you go hunting for a business reason it might not need.*

**Answer in one line:** Check data integrity first (a tracking bug, a reporting change, a timezone or date-boundary artifact), then check for an external or seasonal explanation (a holiday, a known outage, a competitor event), then look for an internal cause (a recent release, a pricing change, a removed feature), and only then drill into which segment of users actually drove the drop.

**Worked structure, applied out loud:**

> "First, I'd confirm the 15% is measured the same way it always is; a logging change or a shifted week boundary can produce a number that looks like a real business drop but isn't one. Assuming it's real, I'd check for anything external that week, a holiday, an outage, a competitor launch, before assuming it's something we did. Then I'd check what changed internally: a release, a pricing change, a removed feature, in roughly that order of likelihood. Finally, I'd segment the drop by platform, geography, and user tenure to see if it's broad or concentrated, since a drop concentrated in one segment points to a very different cause than a broad, even one."

| Tier | What to say |
|---|---|
| Passes | Checks one or two plausible causes (a release, a holiday) and segments by platform, but never asks whether the number itself is right |
| Strong | The four-stage funnel above: verify the data, check external factors, check internal changes, then segment |
| Extra points | **[+Validate]** explicitly proposes checking whether the drop is broad or concentrated in one segment, since that single fact rules out most hypotheses at once<br>**[+Business]** ties the investigation to a concrete next action at each stage, not just a list of things to "look into" |

**Likely follow-ups:** The drop turns out to be concentrated entirely in one country. What does that suggest, and what would you check next? How would you distinguish a real user-behavior change from a measurement artifact, concretely?
**Red flag:** guessing a specific root cause before verifying the number and ruling out the broad categories.
**Learn it in:** Chapter 23 §23.11 (a general method for diagnosing a KPI move: confirm it's real, walk down the tree, check for a mix effect) and Chapter 5 §5.4 (issue trees and MECE). **Practise it with:** Chapter 69, Move 5 (edge cases) and Move 7 (validate), and section 69.4's worked revenue drop.

### Q75-008 · "Revenue is up 10% year over year, but our finance team is worried. Why might a rising number still be bad news?"

**Level:** Mid · **Roles:** DA, BA, PA

**Remember it as:** *A single headline number can hide a mix shift, a one-time event, or a sustainability problem underneath a technically true "growth" story.*

**Answer in one line:** Revenue growth can mask a worse underlying picture in several ways: it might be driven by a small number of large, unrepeatable deals rather than broad healthy demand; it might be coming at the cost of margin (revenue up, profit down); it might be masking customer churn (fewer, bigger customers replacing many smaller ones, a riskier concentration); it might be price-driven (list-price rises masking falling units or fewer active customers); or it might not be keeping pace with a cost base or a target that's growing even faster.

| Tier | What to say |
|---|---|
| Passes | Names one reason (usually "profit could be down") without a way to check it |
| Strong | Names at least two of the mechanisms above with a concrete business reason each matters |
| Extra points | **[+Business]** ties each mechanism to a specific follow-up metric that would confirm or rule it out: margin trend for the profit concern, customer count and concentration for the mix-shift concern, cohort retention for the churn-masking concern, units and the active-customer trend for the price concern |

**Likely follow-ups:** Which of these would you check first, and why? How would you present this nuance to a stakeholder who's happy about the headline number?
**Red flag:** treating "revenue is up" as inherently good news with no interrogation of what's underneath it.
**Learn it in:** Chapter 23 §23.10–23.11 (the KPI tree: active customers × orders per customer × average order value, and walking a change down it) and Chapter 4 §4.10 (a headline number without its context). Section 75.3 below meets the same mix problem again, in dashboard design.

### Rapid-fire, 75.2

Roles: DA, PA and BA for every row.

| # | Scenario | Structure to reach for | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q75-009 | Conversion rate on the checkout page dropped after a redesign | Data-first: confirm the drop wasn't caused by an analytics tagging change in the redesign itself before assuming the design is at fault | **[+Edge cases]** a redesign that changes page structure very often breaks event tracking at the same time it changes the actual experience, tangling two separate questions together | Fresher · 23.11 |
| Q75-010 | Customer support ticket volume spiked | Segment by ticket category first: a spike concentrated in one issue type points to a specific bug or change; a broad spike across categories points to something upstream (an outage, a billing run) | **[+Business]** ticket *volume* alone doesn't say whether it's a new problem or a known one just getting reported more, worth checking against a "first time this issue" flag if one exists | Mid · 5.4 |
| Q75-011 | Average order value is flat, but total revenue fell | The drop is in order *count*, not order value. Split order count into active customers × orders per customer: fewer customers points to acquisition or churn; the same customers ordering less often points to frequency or retention. Pricing and basket size are ruled out | **[+Signpost]** the same decomposition as Chapter 23's KPI tree (section 23.10, Figure 23.3), walked in section 23.11, just applied live under interview pressure | Mid · 23.10, 23.11 |
| Q75-012 | A metric looks fine in aggregate but a stakeholder insists something's wrong in their area | Always check for Simpson's paradox before dismissing the stakeholder: an aggregate can hide a real, reversed trend in a specific subgroup | **[+Evidence]** the stakeholder closest to the data is often right about a localized problem an aggregate view genuinely can't show; practise it with Chapter 73, Q73-031 | Mid · 22.6 |

---

## 75.3 Designing metrics and dashboards

### Q75-013 · "Design a KPI dashboard for a customer support team's manager." Walk through your approach

**Level:** Mid · **Roles:** DA, BI, BA

**Remember it as:** *Ask what decision the dashboard needs to support before picking a single metric. A dashboard with no decision behind it is just numbers on a wall.*

**Answer in one line:** Start from the decisions the manager actually needs to make (staffing that day, which tickets need escalation, whether the team is meeting its service commitments), then pick the smallest set of metrics that supports those decisions, rather than starting from "what data do we have" and displaying all of it.

Two support terms used below: **average handle time** (AHT) is the average minutes an agent spends on one ticket, and a **service-level agreement** (SLA) is the promised time to respond to or resolve a ticket.

**Worked structure:**

> "I'd ask what decisions this manager makes weekly: probably staffing levels, escalation priority, and reporting up to their own leadership. For staffing, I'd want ticket volume trend and average handle time, shown next to repeat-contact rate so a push for speed can't hide unresolved tickets. For escalation, open tickets by age and by severity, so anything aging past a threshold is visible immediately. For reporting up, a service-level metric like % of tickets resolved within target time, trended over time, not just a snapshot. I'd deliberately leave off vanity metrics like total tickets ever handled, since it doesn't drive any decision this specific manager makes day to day."

| Tier | What to say |
|---|---|
| Passes | A sensible list of support metrics (volume, handle time, SLA) not tied to decisions |
| Strong | The decisions-first structure above, with metrics explicitly tied to staffing, escalation, and reporting |
| Extra points | **[+Business]** explicitly excludes a plausible-sounding but decision-irrelevant metric, which signals real judgment, not just metric-generation<br>**[+Edge cases]** flags that a single "tickets resolved" count can hide the exact Simpson's-paradox-style mix problem from Q75-012, so an SLA breakdown by ticket type is more honest than one blended number |

**Likely follow-ups:** How would this dashboard differ for a frontline agent instead of a manager? What's one leading indicator (predicts a future problem) versus one lagging indicator (reports a past one) you'd include, and why have both?
**Red flag:** a dashboard design that's really just "every metric I can think of related to the topic," with no filter for what's actually decision-relevant.
**Learn it in:** Chapter 3 §3.6 (dashboards and the decisions they serve), Chapter 15 §15.2 (start from the question) and Chapter 16 §16.7 (designing the report page); the handle-time guardrail is Chapter 23 §23.12. **Practise it with:** Chapter 70 §70.8 (Q70-069/070), the same "does this serve a real decision" discipline applied to an already-built dashboard instead of a from-scratch design.

### Q75-014 · What's the difference between a leading and a lagging indicator, and why does a good dashboard need both?

**Level:** Fresher · **Roles:** DA, BA, PA, BI

**Remember it as:** *A lagging indicator tells you what already happened. A leading indicator gives you a chance to change what happens next.*

**Answer in one line:** A **lagging indicator** (revenue, churned customers, resolved tickets) reports an outcome after it's already occurred, useful for accountability and reporting; a **leading indicator** (website traffic, open pipeline, ticket backlog growth rate) signals a likely future outcome early enough to still act on it: a dashboard built entirely on lagging indicators can only ever confirm a problem after it's too late to prevent it. To trust a leading indicator, check that it moves *before* the outcome across several periods, then test it: does intervening on it change the outcome?

| Tier | What to say |
|---|---|
| Passes | Defines the terms correctly, can't give a concrete pair from the same domain |
| Strong | A matched pair from one domain: e.g. churned customers (lagging) vs. a declining product-usage trend among still-active customers (leading, since it predicts churn before it happens) |
| Extra points | **[+Business]** a dashboard's real value often comes specifically from its leading indicators, since the lagging ones mostly confirm what a team already suspects by the time the number moves |

**Likely follow-ups:** Name a leading indicator for churn that isn't usage frequency. How would you validate that a proposed leading indicator actually predicts the lagging outcome, rather than just correlating with it?
**Red flag:** unable to distinguish the two, or naming a lagging indicator as an example of a leading one.
**Learn it in:** Chapter 3 §3.5 (leading and lagging) and Chapter 23 §23.12 (pairing a leading metric with a guardrail); for checking that it predicts, Chapter 22 §22.5 (correlation, causation, and confounders) and Chapter 31 (causal inference without experiments). **Practise it with:** Chapter 73, Q73-032.

### Rapid-fire, 75.3

Roles: DA, BA, PA and BI for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q75-015 | What's a vanity metric? | A number that looks impressive and trends upward easily, but doesn't connect to a real business decision or outcome (total signups ever, cumulative downloads) | **[+Business]** the test: "if this number changed, would anyone actually do anything differently?": if not, it's a vanity metric | Fresher · 23.12 |
| Q75-016 | Why is a single blended average often a worse metric than a segmented breakdown? | It can hide Simpson's-paradox-style reversals (Q75-012) and mask the fact that different segments need entirely different actions | **[+Validate]** show the segmented table next to the blended number, so the reader can see whether the segments agree with the total | Mid · 22.6 |
| Q75-017 | What's a North Star metric, and what's the risk of picking the wrong one? | A single number, upstream of revenue, that captures whether customers are getting value (Riverstone: active customers). It is the one branch leadership watches weekly, not a replacement for the KPI tree, and it needs a guardrail because any single target can be gamed. The wrong one (engagement time instead of a genuinely valuable outcome) can hit its target while hurting the business | **[+Business]** a North Star metric should be hard to "game" without also delivering real value, or it quietly becomes a target people optimize around instead of through | Mid · 23.10, 23.12 |
| Q75-018 | How would you decide the right refresh frequency for a dashboard? | Match it to how often the decision it supports actually gets made: a daily staffing decision needs daily data; a quarterly strategy review doesn't need real-time numbers | **[+Trade-offs]** fresher data costs more: in Power BI it's Import with a scheduled refresh against DirectQuery; practise it with Chapter 70, Q70-063 | Mid · 16.2 |

---

## 75.4 Product sense and decision cases

### Q75-019 · "Should we build a loyalty program?" How do you approach a yes/no product decision with no data given upfront?

**Level:** Senior · **Roles:** PA, BA, DA

**Remember it as:** *A product decision case isn't "yes" or "no." It's "here's what would have to be true for yes to be right, and here's how I'd check."*

**Answer in one line:** Frame the decision around the conditions that would make it worthwhile (does the target segment actually respond to loyalty incentives, is the expected retention or spend lift big enough to cover the program's cost, is there a cheaper alternative that achieves the same goal), rather than trying to produce a confident yes/no with no data in hand.

**Worked structure:**

> "I'd start with what problem this is meant to solve: is retention the issue, average order value, or something else? Assuming retention, I'd want to know our current churn rate and whether we have any evidence, even anecdotal, that price or reward sensitivity is a real churn driver for our customers, versus something a loyalty program wouldn't fix, like product availability. Then I'd size it: rough cost of running the program against a plausible retention lift, even a rough one, to see if the economics could plausibly work before recommending we actually build it. I'd end with a recommendation to pilot on one segment first, rather than a company-wide commitment, given how much of this is still genuinely uncertain."

| Tier | What to say |
|---|---|
| Passes | Lists pros and cons of loyalty programs and leans yes, with no sizing or pilot |
| Strong | The conditions-for-yes framing above, ending in a specific, proportionate recommendation (a pilot, not a full commitment) |
| Extra points | **[+Trade-offs]** explicitly separates "would this help" from "is this the best use of the same budget," since a case that only evaluates one option in isolation misses cheaper alternatives that might solve the same problem<br>**[+Business]** the pilot recommendation matches the actual level of confidence the analysis supports, rather than overclaiming certainty either direction |

**Likely follow-ups:** How would you design the pilot to actually produce a clear answer? What metric would tell you the pilot worked?
**Red flag:** a confident yes/no answer with no acknowledgment of what's actually unknown.
**Learn it in:** Chapter 22 §22.3 (designing an A/B test) and Chapter 30 §30.7–30.8 (power and sample size; designing an experiment, with a primary metric and guardrails): exactly what a "pilot" here would need to be built well. **Practise it with:** Chapter 73 §73.4–73.5 (A/B test design and debugging).

### Rapid-fire, 75.4

Roles: PA, BA and DA for every row.

| # | Scenario | Key move | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q75-020 | "Would you prioritize feature A or feature B?" with limited detail on either | Ask for the goal each feature serves and roughly how many users each would affect, before comparing; don't guess at relative value with no basis | **[+Signpost]** reach for a simple, stated framework, for example RICE = (Reach × Impact × Confidence) ÷ Effort, so a feature scores higher when it helps more people, more, with more certainty, for less work (see the note below) | Mid · 25.9, 25.12 |
| Q75-021 | "A competitor just launched a feature we don't have. Should we build it too?" | Ask whether the feature addresses a real, evidenced need of your own users, not just competitive parity, before recommending building it | **[+Edge cases]** matching a competitor feature-for-feature with no evidence it matters to your own users is a common, costly trap | Mid · 5.3 |
| Q75-022 | "How would you know if a new feature is successful, before launch?" | Define the success metric and a rough target *before* building it, not after seeing what the number happens to be | **[+Validate]** fix the smallest effect worth detecting before launch, the same discipline as an A/B test's minimum detectable effect; practise it with Chapter 73, Q73-021 | Mid · 22.3, 30.8 |
| Q75-023 | "Our product has high engagement but low revenue. What would you investigate?" | Check whether the engaged users are the same users being monetized, or whether engagement and monetization are happening in two different, disconnected populations | **[+Business]** a mismatch between who's engaged and who pays is one of the most common, fixable product-strategy problems this kind of question is fishing for | Senior · 5.4, 23.10 |

**Beyond the book: RICE (Q75-020).** RICE is the product-team version of the ranking score in Chapter 25: section 25.9 ranks gaps by hours saved × error weight ÷ build effort, and section 25.12 ranks automations on frequency, time, error cost and effort. RICE scores a feature on **Reach** (how many users it touches in a period), **Impact** (how much it helps each one, on a small scale such as 1 to 3), **Confidence** (how sure you are of those two, as a percentage) and **Effort** (person-weeks of work). Effort divides, because the same benefit for less work should rank higher. A feature that reaches 1,000 users a quarter, with impact 2, confidence 80% and effort 2 person-weeks, scores (1,000 × 2 × 0.8) ÷ 2 = 800. The same feature at 10 person-weeks scores 1,600 ÷ 10 = 160. Multiply by effort instead of dividing and you get 3,200 against 16,000: the expensive feature wins, which is the opposite of what the score is for.

---

## 75.5 Guesstimates: structured estimation

Every number in a guesstimate is an assumption you choose and say out loud; the interviewer is grading the chain, not the facts. Where a real figure exists, the worked answers below give it with its source, so you can see how close a sensible assumption lands.

### Q75-024 · Estimate the number of gyms in Mumbai. Walk through your structure, not just a final number

**Level:** Fresher · **Roles:** DA, BA, PA

**Remember it as:** *A guesstimate is judged on the chain of reasonable numbers, not on how close the final answer lands.*

**Answer in one line:** Say which Mumbai you mean, then break the target quantity into a chain of estimable factors (population → the fraction of that population who are gym-goers → the average size of a gym), state a defensible round number for each link, and multiply through, showing the full chain rather than a single guessed final number.

**Worked calculation:**
```
Greater Mumbai population (BMC area):  ~12,500,000
share who regularly go to a gym:        ~3%
→ gym-going population:                 12,500,000 × 3% = 375,000
average members per gym:                ~500
→ estimated number of gyms:             375,000 ÷ 500 = 750
```

The geography is itself an assumption to state: this chain uses **Greater Mumbai**, the area the city corporation (BMC) runs, not the wider metropolitan region around it, which has millions more people. The 2011 census counted 12,442,373 people there (Census of India 2011, Primary Census Abstract, ward-level tables), so 1.25 crore is a sensible round number; it has grown since, which is one more reason to keep only one or two significant figures. The 3% and the 500 are assumptions.

| Tier | What to say |
|---|---|
| Passes | A chain of two factors with round numbers but no justification or sanity check |
| Strong | The full chain above, with each factor justified in one sentence ("3% feels right for a mix of gym-goers and non-gym-goers across income levels in a big city") |
| Extra points | **[+Assume]** names the geography first: "I'll take Greater Mumbai, the BMC area, about 1.25 crore people, not the whole metropolitan region"<br>**[+Validate]** sanity-checks the final number against something known: "750 gyms across the BMC's 24 wards is about 31 per ward, or one gym for roughly every 17,000 people, which feels plausible for a dense city, not obviously too high or too low"<br>**[+Edge cases]** flags the single most uncertain link in the chain (probably the 3% gym-going rate) as the one worth refining first if more precision were needed, rather than treating every link as equally solid |

**Likely follow-ups:** Which of your assumptions would you want real data to check first? How would the estimate change for a smaller city?
**Red flag:** a single number with no visible chain, or a chain so long and granular it becomes a guess wearing a structure's clothing.
**Learn it in:** Chapter 4 §4.9 (the four-step estimation method: break it down, write each assumption with a round number, multiply, sanity-check). **Practise it with:** Chapter 69, Move 2 (state assumptions) and Move 7 (validate).

### Q75-025 · Estimate the total addressable market, in rupees, for plastic storage containers sold to households across India

**Level:** Mid · **Roles:** DA, BA, PA

The **total addressable market** (TAM) is the total yearly spend on a category if every possible buyer is counted, whoever they buy from.

**Remember it as:** *Top-down (population → adoption → spend) and bottom-up (built from the supply side: sellers × units each sells × price) should land in the same rough neighborhood: if they don't, that gap itself is the interesting finding.*

**Answer in one line:** Top-down, chain the number of households through the share who buy this category each year and the average annual spend per buying household; then cross-check with a bottom-up estimate built from the supply side (the number of shops selling the category × containers each sells a year × average price, or the sum of known brands' sales), rather than trusting one method alone.

**Worked calculation, top-down:**
```
Indian households:                      ~300,000,000 (30 crore)
share buying storage containers a year:  ~15%
→ buying households:                     300,000,000 × 15% = 45,000,000
average spend per buying household:      ~₹400 a year
→ market size:                           45,000,000 × ₹400
                                         = ₹18,00,00,00,000 (₹1,800 crore)
```

Every link is an assumption. A quick check on the first: 30 crore households at about 4.5 people each is about 135 crore people; the 2011 census counted 121 crore (1,210,854,977), and the population has grown since, so the order of magnitude fits.

**Worked calculation, bottom-up:**
```
shops selling household plastics:        ~500,000 (5 lakh)
containers each sells a year:            ~250 (about 5 a week)
→ containers sold a year:                500,000 × 250 = 125,000,000
average price per container:             ~₹150
→ market size:                           125,000,000 × ₹150
                                         = ₹18,75,00,00,000 (₹1,875 crore)
```

The two routes land within about 4% of each other (₹1,875 crore against ₹1,800 crore). They agree on units too: ₹400 a year at ₹150 a container is about 2.7 containers per buying household, or about 12 crore containers a year, close to the bottom-up 12.5 crore.

| Tier | What to say |
|---|---|
| Passes | A top-down chain with round numbers, stated as if it were precise, with no cross-check |
| Strong | The full top-down chain above, explicitly stated as top-down, and said in the unit the audience uses: "about ₹1,800 crore" |
| Extra points | **[+Validate]** adds the bottom-up estimate from the supply side and compares the two, in rupees and in units<br>**[+Business]** notes this is a *category* size, not any one company's addressable share, and ties it to Riverstone (Chapter 3): Riverstone sells to retailers, hospitality and wholesalers, not to households, but its retail customers sell into exactly this household market, so the figure bounds what Riverstone's retail segment could grow into<br>**[+Signpost]** states the answer in the unit the interviewer uses: ₹1,800 crore, not "₹18 billion" or a string of zeros (Chapter 4 §4.9) |

**Likely follow-ups:** How would Riverstone's unit sales plus an assumed market share cross-check the 15%? What's the biggest risk in this estimate being wrong by an order of magnitude?
**Red flag:** presenting a single top-down estimate as if it were precise, with no acknowledgment of the wide uncertainty band around it.
**Learn it in:** Chapter 4 §4.9 (the four-step estimation method, with the storage-box example this question scales up, and lakh and crore). **Practise it with:** Chapter 69, Move 2 (state assumptions) and Move 7 (validate).

### Rapid-fire, 75.5

Roles: DA, BA and PA for every row. Every number in this table is an assumption.

| # | Guesstimate | Structure to reach for | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q75-026 | How many piano tuners are there in a city of 5 million? | Pianos owned → tunings needed per piano per year → tunings one tuner can do per year | **[+Signpost]** the classic Fermi-problem format: every link should be a number you could defend in one sentence, not a fact you'd need to look up | Fresher · 4.9 |
| Q75-027 | Daily revenue of a mid-size coffee shop | Customers per day (estimate from seating capacity and turnover, or foot traffic) × average ticket size | **[+Validate]** 300 customers a day × ₹150 average ticket = ₹45,000 a day, a number worth sanity-checking against a rough rent-and-staff cost estimate for the same shop | Fresher · 4.9 |
| Q75-028 | Number of WhatsApp messages sent in India in one day | India's population → % of population on WhatsApp → average messages sent per active user per day | **[+Edge cases]** "average" hides a skew (heavy users send far more than the median user); worth naming that the estimate is more uncertain because of it, rather than pretending the average is a clean single number | Mid · 4.9 |
| Q75-029 | How many gas stations does a country need? | Vehicles on the road → average fuel consumption → stations' typical daily throughput capacity | **[+Signpost]** this specific guesstimate is really a supply-demand balance question in disguise, not a pure counting one, worth naming explicitly | Senior · 4.9 |

---

## 75.6 Full cases, talked through live

### Q75-030 · Full case, talked through live: "Our email open rate dropped from 25% to 18% last month. What happened?"

**Level:** Mid · **Roles:** DA, PA

**What they're really testing:** whether the full structure (verify, external, internal, segment) actually gets executed end to end under time pressure, not just described in the abstract.

**Talked through live, start to finish:**

> "So that's 7 percentage points, or a 28% relative drop, month on month; is that against last month only, or also the same month last year? First, I'd confirm the drop is measured consistently, same tracking pixel, same definition of 'open,' since email open-rate tracking is notoriously fragile, particularly around any change to how images load by default in major email clients, which can silently affect open tracking with nothing about the actual email changing at all. Assuming that checks out, I'd look for anything external: did a major email provider change its spam filtering or default image-blocking that month? Then internal: did we change our subject lines, sending time, sender name, or list composition (a big new batch of colder, less-engaged contacts added to the list would mechanically drop the average even with individually unchanged behavior)? Finally, I'd segment by list, by device, and by send time to see whether the drop is broad or concentrated. If it's concentrated in one email client, that points straight back to a client-side default-image-blocking change, not anything we did."

**Extra-points moves demonstrated:** **[+Clarify]** restated the drop with its base and period, in points and as a relative change (25 − 18 = 7 points; 7 ÷ 25 = 28%), before using it. **[+Edge cases]** named a specific, well-known confound (email clients changing how they load images by default) rather than a generic "maybe it's a tracking issue." **[+Signpost]** ran the full verify → external → internal → segment funnel completely, out loud, in order. **[+Business]** connected the list-composition hypothesis to a concrete mechanism (a mechanical average effect from adding colder contacts) rather than just naming it as a possibility.

**Likely follow-ups:** The drop turns out to be broad, not concentrated in one client or segment. What does that change about your next hypothesis? How would you recommend recovering the open rate?
**Red flag:** listing possible causes without ever proposing how to actually distinguish between them.
**Learn it in:** Chapter 4 §4.2 (percentage points and percent change), Chapter 23 §23.11 (diagnosing a change, including the mix check) and Chapter 5 §5.4 (issue trees). **Practise it with:** section 75.2 above, and Chapter 69, Move 5.

### Q75-031 · Full case, talked through live: "Design a single metric to measure whether Riverstone's new self-service reorder portal is succeeding"

**Level:** Senior · **Roles:** PA, BA, DA

**What they're really testing:** whether a single metric can be chosen and defended, or whether the answer collapses into an undifferentiated list of "things you could measure."

**Talked through live, start to finish:**

> "The portal's real goal is probably reducing manual reorder friction for repeat customers, not just 'more orders.' I'd propose **% of eligible repeat orders placed through the self-service portal, without needing a call or email to a rep**, as the single metric, since it directly measures adoption of the thing being built, not a proxy for it. I'd deliberately avoid 'total orders' as the top metric, since that's driven by far more than this one feature and wouldn't isolate the portal's actual contribution. I'd pair it with one guardrail metric, order accuracy or error rate through the portal, so we're not accidentally rewarding adoption that comes at the cost of more mistakes."

**Extra-points moves demonstrated:** **[+Business]** explicitly rejected a plausible-sounding but poorly-isolated metric (total orders) and explained why. **[+Edge cases]** added a guardrail metric unprompted, anticipating that optimizing the primary metric alone could create a hidden downside. **[+Signpost]** the chosen metric is a *rate* (self-service share of eligible orders), not a raw count, which is what makes it comparable over time regardless of overall business growth.

**Likely follow-ups:** How would you define "eligible" precisely? What would make you recommend killing the portal rather than iterating on it?
**Red flag:** naming several metrics with no commitment to a single primary one, or picking a metric that's really measuring overall business health rather than this specific feature.
**Learn it in:** Chapter 23 §23.12 (a rate instead of a count, and pairing a metric with a guardrail) and Chapter 30 §30.8 (a primary metric and its guardrail metrics). **Practise it with:** section 75.3 above (North Star metrics, Q75-017) and Chapter 70 §70.8 (Q70-069/070).

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Answering before clarifying or structuring | A technically correct answer to the wrong specific question | Restate, clarify, preview a structure, in that order, every time |
| Guessing a root cause before verifying the metric itself | Chasing a business explanation for what's actually a tracking bug | Always check data integrity first in a diagnostic case |
| A dashboard built from "all available data" | A wall of numbers nobody actually uses to decide anything | Start from the decisions the dashboard needs to support |
| A confident yes/no on a product decision with no data given | Overclaiming certainty the case doesn't support | Frame it as "what would have to be true," recommend a pilot where genuinely uncertain |
| A guesstimate with no visible reasoning chain | Impossible for the interviewer to assess whether the thinking was sound | Show every link in the chain, one defensible number at a time |
| Naming a metric with no guardrail against gaming it | A metric that technically improves while the real goal suffers | Pair a primary metric with at least one guardrail |
| Treating every case with the same rigid memorized framework | A technically thorough but off-target answer | Identify the case type (diagnostic vs. decision) before choosing a structure |

---

## In the real world: the case that hinged on one clarifying question

Kabir, interviewing for a Business Analyst role, is given the case: "Our biggest customer's order volume dropped 40% last quarter. What do you do?" He starts to ask his usual battery of clarifying questions, then stops and asks one specific one instead: "Is this customer still ordering at all, just less, or have they effectively gone dark?"

The interviewer's answer changes everything: the customer had placed exactly one small order the entire quarter, down from a steady weekly cadence. Kabir immediately shifts his structure from a "why did volume decline gradually" diagnostic (checking pricing, product mix, competitor activity) to a "why did this relationship nearly stop" one (checking for a specific triggering event: a contract dispute, a champion leaving the customer's organization, a competitor winning an exclusive deal). He asks two more targeted questions and correctly guesses, out loud, that the most likely explanation is a champion departure, exactly what the interviewer had in mind.

The interviewer's note afterward: *"Most candidates ask five generic clarifying questions and get five generic answers. Kabir asked one that actually changed his whole approach, and used the answer immediately."* The lesson isn't "ask fewer questions." It's that a clarifying question earns its place only if the answer would genuinely change what you do next, exactly Chapter 69's Move 1, and this case shows what it looks like when that discipline is followed for real, under pressure, rather than performed as a checklist item.

---

## Project

**Goal:** run this chapter's full method on cases of your own choosing.

### Tools you'll need

No software specific to this chapter. A notebook or whiteboard to sketch a structure before speaking is the single most useful habit; interviewers consistently rate a candidate who visibly organizes their thinking (even three bullet points jotted down) higher than one who reasons entirely out loud with no visible structure.

1. Pick a real metric from your own work that changed recently, and run the full verify → external → internal → segment funnel on it, even if you already know the answer, to practice the structure itself.
2. Design a one-page dashboard for a real team you're familiar with, starting explicitly from the decisions it needs to support, and cut anything that doesn't serve one.
3. Take a real "should we do X" question from your own workplace and write the "what would have to be true" framing for it, ending in a specific, proportionate recommendation.
4. Practice three guesstimates out loud, timed to under three minutes each, showing your full chain of reasoning, not just a final number.

---

## Key terms

MECE (Mutually Exclusive, Collectively Exhaustive) · diagnostic case · product-decision case · weekly active users · leading indicator · lagging indicator · North Star metric · vanity metric · guardrail metric · average handle time · service-level agreement (SLA) · RICE · Fermi estimation · total addressable market (TAM) · top-down vs. bottom-up estimate · pilot (as a decision-testing step)

---

## Final-week revision list

Q75-001, Q75-002, Q75-007, Q75-008, Q75-013, Q75-014, Q75-017, Q75-019, Q75-024, Q75-025, Q75-030, Q75-031.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against, especially Moves 1 (clarify), 3 (signpost), and 7 (validate).
- **Chapter 76A, Data Analyst & Data Scientist Question Bank,** and **Chapter 76B, Business Analyst Question Bank,** continue from this chapter's case reasoning: 76A into project narratives, 76B into requirements and process questions.
- **Chapter 70, section 70.8,** already covers dashboard critique from the other direction, judging one that's already built rather than designing one from scratch.
- **Chapter 73, Statistics, Probability & Experimentation Bank,** is where a "pilot" proposed in any of this chapter's cases would actually need to be designed properly before running.
- **Chapters 3, 4, 5, 23 and 24** teach every technique this bank draws on, in full; this chapter tests them, it doesn't re-teach them.
