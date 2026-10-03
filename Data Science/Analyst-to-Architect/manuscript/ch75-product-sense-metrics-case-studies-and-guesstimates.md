# Chapter 75. Product Sense, Metrics, Case Studies & Guesstimates

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** structure an ambiguous business case the way an interviewer actually wants, instead of jumping straight to an answer · diagnose a metric that moved, systematically, not by guessing at causes · design a KPI dashboard that answers real decisions, not just displays numbers · size a market or estimate a quantity with a defensible structure, not a guessed final number · settle five metric traps with arithmetic you can do in the room, including two where the measured answer contradicts the cliche · handle the product questions that have no clean answer — cannibalisation, network effects, low adoption, a price rise — by naming the evidence that would decide them.
>
> **Before you start:** Chapter 69 (the three answer tiers and the twelve extra-point moves). The questions test Chapters 3 (KPIs, dashboards), 4 (percentage points, estimation), 5 (precise questions, issue trees, MECE), 22 (A/B design, Simpson's paradox), 23 (KPI trees, diagnosing a change, guardrails) and 24 (turning an ask into a question), with a few links to Chapters 15, 16, 25 and 30. This chapter tests those skills; it doesn't teach them again. When you can't answer a question, its **Learn it in** line sends you to the section that teaches it.
>
> **Time needed:** 5–7 hours to read and drill every question once, out loud; 2–3 hours more for the project. Sections 75.7 and 75.8 are arithmetic rather than structure, and reward being done with a pen rather than read.
>
> **How this chapter is built.** Same format as every question bank in Part 8: a memory hook ("Remember it as…"), a one-line answer, and a tier table (**passes**, **strong**, **extra points**, tagged with Chapter 69's moves: **[+Clarify]**, **[+Signpost]** and so on), then follow-ups, the red flag, and where to learn it. Rapid-fire rows end with a level and the section that teaches the idea (a bare number such as 23.10 means that section). There is no code: a case is judged on structure and reasoning. Every number in a worked example is either an assumption, labelled as one, or a figure with its source, and the arithmetic is shown step by step. The chapter moves from the general case framework (section 75.1) through metric diagnosis (75.2), metrics and dashboards (75.3) and product decisions (75.4) to guesstimates (75.5) and two full cases (75.6). Guesstimates need only Chapter 4, so a first-job candidate can do section 75.5 straight after 75.1.
>
> **Section 75.8 is measured, not illustrated.** Every figure in it comes from Riverstone's October–December 2025 order data — `companion/ch14/clean_truth_orders_q4_2025.csv`, the cleaned file Chapter 14 produces and Chapter 72B interrogates: 25,832 order lines, 14,372 orders, ₹44.26 crore of net revenue. Two of its answers contradict what the received wisdom predicts. Revenue is **not** concentrated 80/20 here — the top 20% of customers produce 41.4% — and the branches differ 2.9× in total revenue while differing only 2.5% in revenue per order, so they differ in volume rather than in selling. Section 75.9 then takes the product questions where the honest answer is conditional, and the skill being tested is naming the evidence that would settle it.
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

## 75.7 Predict the number: metric arithmetic that is not what it looks like

Section 75.5 is about estimating a number you do not have. This section is the opposite: you are *given* the numbers, and the arithmetic is the trap. Every question below has an answer that most people get wrong on first instinct, and every one of them appears in real reporting.

These matter more than guesstimates, because a guesstimate is explicitly a guess and everyone treats it as one. A metric is presented as a fact. When a slide says churn is 60% and it is really 46%, nobody questions it, because arithmetic is not where people look for errors.

Say each answer out loud before reading on. They are short.

### Q75-032 · Revenue falls 50% in March and rises 50% in April. Where is it?

**Level:** Fresher · **Roles:** DA, PA, BA, DS

**Remember it as:** *A fall and a rise of the same percentage are not opposites, because they are percentages of different numbers.*

**Answer in one line:** **25% below where it started** — 100 falls to 50, and 50% of 50 is only 25, so April ends at 75; recovering a 50% fall takes a 100% rise.

```python
v = 100.0
v *= 0.5;  print(f"after -50%: {v:.2f}")
v *= 1.5;  print(f"after +50%: {v:.2f}")

for drop in (10, 20, 30, 50, 80, 90):
    need = (1 / (1 - drop/100) - 1) * 100
    print(f"a {drop:>2}% fall needs a {need:>5.1f}% rise to recover")
```

```
after -50%: 50.00
after +50%: 75.00

a 10% fall needs a  11.1% rise to recover
a 20% fall needs a  25.0% rise to recover
a 30% fall needs a  42.9% rise to recover
a 50% fall needs a 100.0% rise to recover
a 80% fall needs a 400.0% rise to recover
a 90% fall needs a 900.0% rise to recover
```

The asymmetry grows fast. A 90% crash needs a 900% recovery, which is why a stock or a metric that collapses almost never "bounces back" in the way the word implies.

Where this reaches a real meeting: a monthly deck that reports "−50% then +50%, so we've recovered" is wrong, and it is wrong in the direction that makes bad news sound finished. The honest line is "we are 25% below January", which is a different conversation.

The same arithmetic is why a column of month-on-month percentages cannot be added or averaged to get the period change. You multiply the growth factors, which is Q75-035.

| Tier | What to say |
|---|---|
| Passes | "Not back to the start" |
| Strong | + 75, with the reason — the percentages are of different bases — and the recovery rule |
| Extra points | **[+Business]** "we recovered" is the wrong summary and it understates the problem · **[+Edge cases]** the asymmetry is extreme at the tails: 90% down needs 900% up · **[+Validate]** compare against the absolute level, not the sequence of percentages |

**Likely follow-ups:** How would you present this honestly on one slide? What is the right way to combine monthly changes? *(Multiply the factors — Q75-035.)* Does the order matter? *(No: 0.5 × 1.5 = 1.5 × 0.5.)*
**Learn it in:** Chapter 23, section 23.6 (metric arithmetic); Chapter 4, section 4.5 (percentages).

### Q75-033 · 5% of customers churn each month. What is annual churn?

**Level:** Mid · **Roles:** DA, PA, BA, DS

**Remember it as:** *Churn compounds on a shrinking base. Each month's 5% is 5% of who is left, not of who you started with.*

**Answer in one line:** **46%**, not 60% — survival is 0.95¹², which is 54%, so 46% of the cohort is gone after a year; multiplying the monthly rate by twelve overstates it by 14 points.

```python
for m in (1, 2, 5, 10):
    annual = (1 - (1 - m/100)**12) * 100
    print(f"monthly {m:>2}% -> annual {annual:5.1f}%   (naive {m*12:>3}%)")
```

```
monthly  1% -> annual  11.4%   (naive  12%)
monthly  2% -> annual  21.5%   (naive  24%)
monthly  5% -> annual  46.0%   (naive  60%)
monthly 10% -> annual  71.8%   (naive 120%)
```

The 10% row is the one that shows why the naive method is not merely imprecise but impossible: 120% annual churn would mean losing more customers than you had.

The companion figure, and the one worth knowing by heart: at a constant monthly churn *r*, the average customer lifetime is **1/r months**. At 5% that is 20 months, which is what feeds the LTV calculation in Q75-037.

The reverse conversion catches people too. Annual churn of 46% is a monthly rate of 1 − 0.54^(1/12) = 5%, not 46 ÷ 12 = 3.8%. Converting between periods always goes through the survival rate, never through division.

| Tier | What to say |
|---|---|
| Passes | "You can't just multiply by 12" |
| Strong | + 46%, the survival-rate method, and that 1/r gives the average lifetime |
| Extra points | **[+Business]** the error always overstates churn, so it makes retention look worse and can trigger spending that is not needed · **[+Edge cases]** real churn is not constant — it is much higher in month one — so a single rate is itself an approximation, and a cohort curve is the honest version · **[+Validate]** a churn rate above 100% annualised is arithmetically impossible and is the giveaway |

**Likely follow-ups:** How would you convert annual churn back to monthly? Why is month-one churn usually much higher? How does this feed LTV? *(Q75-037.)*
**Learn it in:** Chapter 23, section 23.9 (retention and churn).

### Q75-034 · A four-step funnel, each step converting at 80%. End-to-end?

**Level:** Fresher · **Roles:** DA, PA, BA

**Remember it as:** *Funnel steps multiply. Four steps at 80% is 0.8⁴, and 80% four times over is not 80%.*

**Answer in one line:** **40.96%** — conversion multiplies rather than averaging, so four "good" steps of 80% lose nearly 60% of the traffic between them.

```python
p = 1.0
for i in range(1, 5):
    p *= 0.8
    print(f"after step {i}: {p*100:5.2f}%")

print(f"one step to 90%:  {0.8**3 * 0.9 * 100:.2f}%")
print(f"all steps to 90%: {0.9**4 * 100:.2f}%")
```

```
after step 1: 80.00%
after step 2: 64.00%
after step 3: 51.20%
after step 4: 40.96%
one step to 90%:  46.08%
all steps to 90%: 65.61%
```

Each step individually looks healthy. Nobody reviewing step 3 in isolation would flag 80%. End to end, three in five visitors are lost.

The two lines at the bottom are the ones that change a prioritisation conversation. Improving a single step from 80% to 90% — a substantial piece of work — buys **5.1 percentage points** end to end. Improving all four buys 24.7. So the honest answer to "which step should we fix?" is usually "the worst one", and the honest answer to "how much will this win get us?" is almost always smaller than the step-level improvement suggests.

It also explains why adding a step is so expensive. An extra confirmation screen converting at 95% — which sounds harmless — costs 5% of everything downstream of it.

| Tier | What to say |
|---|---|
| Passes | "You multiply them: 0.8⁴" |
| Strong | + 40.96%, and what a one-step improvement is worth end to end against a step-level reading |
| Extra points | **[+Business]** a 95% step added to a funnel costs 5% of all traffic below it, which is how funnels silently lengthen · **[+Validate]** step rates that look fine individually can still give a poor end-to-end number; always compute both · **[+Edge cases]** the steps must be conditional on reaching that step, which is why a "conversion rate" with no stated denominator is unusable |

**Likely follow-ups:** Which step would you fix first, and why? How would you find where users actually drop? What if users can skip a step?
**Learn it in:** Chapter 23, section 23.7 (funnels).

### Q75-035 · Revenue grows 5% month on month all year. What is annual growth?

**Level:** Mid · **Roles:** DA, PA, BA, DS

**Remember it as:** *Growth compounds. 5% a month is not 60% a year, it is 80% — and it doubles the business in about fourteen months.*

**Answer in one line:** **79.6%** — 1.05¹² is 1.796, so the business grows by four-fifths rather than the three-fifths that multiplying by twelve suggests.

```python
import math
for m in (1, 3, 5, 10):
    annual = ((1 + m/100)**12 - 1) * 100
    double = math.log(2) / math.log(1 + m/100)
    print(f"{m:>2}% MoM -> {annual:6.1f}% a year, doubling in {double:4.1f} months")
```

```
 1% MoM ->   12.7% a year, doubling in 69.7 months
 3% MoM ->   42.6% a year, doubling in 23.4 months
 5% MoM ->   79.6% a year, doubling in 14.2 months
10% MoM ->  213.8% a year, doubling in  7.3 months
```

Note that this error runs the *opposite* way to the churn one in Q75-033. Compounding growth makes the naive figure an **under**estimate; compounding churn makes it an **over**estimate. The mechanism is the same — the base changes each period — and the direction flips because one adds to the base and the other subtracts from it.

The doubling column is the useful mental tool. The rule of 72 gets you there without a calculator: 72 ÷ 5 ≈ 14 months, which matches the exact 14.2 closely enough for a conversation.

The practical trap in reporting is the mirror of Q75-032: a column of monthly growth percentages cannot be summed. To combine them you multiply the factors, and to get an average monthly rate from an annual one you take the twelfth root, not divide by twelve.

| Tier | What to say |
|---|---|
| Passes | "More than 60%, because it compounds" |
| Strong | + 79.6%, and the doubling time, with the rule of 72 as the mental shortcut |
| Extra points | **[+Business]** the error here understates growth, where the churn version overstates loss — same mechanism, opposite direction · **[+Validate]** an average monthly rate is the twelfth root of the annual factor, never the annual rate divided by 12 · **[+Edge cases]** sustained high MoM growth is rarely real for long; check whether the base period was unusually low |

**Likely follow-ups:** What is CAGR and how does it differ from this? What does the rule of 72 approximate? How would you report a growth rate that varied month to month? *(The geometric mean of the factors.)*
**Learn it in:** Chapter 23, section 23.6; Chapter 4, section 4.5.

### Q75-036 · DAU is 20,000 and MAU is 50,000. What does 0.40 mean, and what are the bounds?

**Level:** Mid · **Roles:** DA, PA, BA

**Remember it as:** *DAU/MAU is "how many days in the month does a typical active user show up", divided by thirty. It cannot go below 1/30.*

**Answer in one line:** **0.40**, meaning the average monthly user is active about **12 days out of 30** — and the ratio is bounded below by 1/30 ≈ 0.033, not by zero, because anyone counted in MAU came at least once.

```python
dau, mau = 20_000, 50_000
print(f"DAU/MAU = {dau/mau:.2f}")
print(f"lower bound = 1/30 = {1/30:.3f}")
print(f"0.40 means about {0.40*30:.0f} active days in 30")
```

```
DAU/MAU = 0.40
lower bound = 1/30 = 0.033
0.40 means about 12 active days in 30
```

The bound is the part that makes this a real question rather than a definition. A ratio of 0.05 is not "very low engagement on a 0-to-1 scale"; it is close to the arithmetic floor, meaning essentially nobody returns. And 0.40 is not "a bit below average" — it is a genuinely sticky product, around what a daily-habit app achieves.

Three caveats that separate a strong answer:

**It is an average over very different users.** A 0.40 made of 40% of users coming every day and 60% coming once looks identical to one where everyone comes 12 days. Those are different products, and only a distribution shows it.

**MAU is a trailing 30-day window in most definitions**, so the denominator moves. A campaign that brings a wave of one-time visitors inflates MAU and *drops* the ratio, making engagement look worse while the product got more users.

**It does not fit every product.** Daily stickiness is the wrong frame for anything with a natural weekly or monthly cadence — a payroll tool, a tax app, Riverstone's monthly reorder portal. Measuring those on DAU/MAU produces a low number that means nothing.

| Tier | What to say |
|---|---|
| Passes | "It's the stickiness ratio, 0.40" |
| Strong | + the interpretation in days (12 of 30) and the 1/30 floor |
| Extra points | **[+Business]** a growth campaign full of one-time visitors lowers the ratio while improving the business · **[+Edge cases]** the average hides the distribution; two very different products give the same number · **[+Clarify]** ask whether daily use is even the intended behaviour before using this metric at all |

**Likely follow-ups:** What would you use instead for a monthly-cadence product? How does MAU's window definition affect it? What is an L28 chart?
**Learn it in:** Chapter 23, section 23.8 (engagement metrics); Chapter 75, Q75-015 (vanity metrics).

### Q75-037 · LTV is ₹12,000 and CAC is ₹4,000. Is 3:1 good?

**Level:** Senior · **Roles:** DA, PA, BA, DS

**Remember it as:** *3:1 is a rule of thumb about contribution margin, not revenue. If your LTV is a revenue number, the real ratio is lower — and the payback period matters more than the ratio.*

**Answer in one line:** **It depends on whether that ₹12,000 is revenue or margin** — at a 70% margin the contribution LTV is ₹8,400 and the ratio is **2.1:1**, not 3:1, and the more decision-useful figure is the payback period of **11.4 months**.

```python
ltv, cac, margin, arpu = 12_000, 4_000, 0.70, 500

print(f"LTV:CAC as given        = {ltv/cac:.1f}:1")
print(f"contribution LTV        = {ltv*margin:,.0f}")
print(f"LTV:CAC on contribution = {ltv*margin/cac:.1f}:1")
print(f"payback months          = {cac/(arpu*margin):.1f}")
```

```
LTV:CAC as given        = 3.0:1
contribution LTV        = 8,400
LTV:CAC on contribution = 2.1:1
payback months          = 11.4
```

Two different companies can both report "3:1" and be in completely different health, because nothing in the ratio is standardised. Before accepting one, ask three things:

| Ask | Why it changes the answer |
|---|---|
| Is LTV revenue or contribution margin? | A 70% margin turns 3:1 into 2.1:1 |
| Is CAC fully loaded? | Blended CAC that includes organic signups understates it, often by a lot |
| Over what horizon is LTV computed? | A 5-year LTV on a 2-year-old company is a forecast, not a measurement |

**Payback is the better headline**, and the reason is cash. An 11.4-month payback means money spent on acquisition today comes back next year — so growth must be funded until then, and the faster you grow the more cash you consume. Two businesses with the same 3:1 ratio and payback periods of 3 months and 18 months are not comparable investments.

Tie it back to Q75-033: at 5% monthly churn the average customer lasts 20 months. A payback of 11.4 leaves about 8.6 months of profitable life — thin. If churn rose to 8% monthly, lifetime falls to 12.5 months and the customer barely pays for themselves.

| Tier | What to say |
|---|---|
| Passes | "3:1 is the usual benchmark, so yes" |
| Strong | + asks whether LTV is margin or revenue, recomputes to 2.1:1, and offers payback as the more useful number |
| Extra points | **[+Business]** payback drives cash needs, and fast growth with slow payback is how a profitable-looking company runs out of money · **[+Clarify]** blended against paid CAC can differ by several times · **[+Edge cases]** LTV over a horizon longer than the company has existed is a model output, not a measurement · **[+Validate]** cross-check LTV against the churn-implied lifetime, 1/r (Q75-033) |

**Likely follow-ups:** How would you compute LTV for a business with no churn data yet? What is blended against paid CAC? Why might a 10:1 ratio be a bad sign? *(Usually under-investment in growth.)*
**Learn it in:** Chapter 23, section 23.4 (unit economics); Chapter 23, section 23.9.

### Q75-038 · 60% promoters, 30% passives, 10% detractors. What is the NPS?

**Level:** Fresher · **Roles:** DA, PA, BA

**Remember it as:** *Promoters minus detractors, as whole numbers. Passives count in the denominator and score nothing. The scale is −100 to +100.*

**Answer in one line:** **50** — on a scale from −100 to +100, not a percentage out of 100, and the 30% of passives affect it only by taking up space in the denominator.

```
NPS = %promoters − %detractors = 60 − 10 = 50
```

Three things people get wrong, in order of how often:

**It is not a percentage.** "An NPS of 50%" is a sentence that reveals the speaker does not know what the number is. It is a net score on a −100 to +100 range.

**Passives are invisible to the arithmetic but not to the denominator.** Converting 10 points of passives into promoters moves NPS by +10 with no change in detractors at all. So a product can improve its NPS substantially without fixing anything a detractor complained about — which is worth knowing before treating the number as a measure of problems.

**The buckets are coarse.** A 9 and a 10 are both promoters; a 6 and a 0 are both detractors. A score of 6 — mildly lukewarm — counts exactly as badly as a 0. That makes NPS jumpy on small samples and insensitive to real movement within a bucket.

The grown-up version of the answer: NPS is useful for tracking a trend on a consistent population, and poor for comparing across companies or industries, because the bucketing and the sampling swamp the signal. If an interviewer offers it as the North Star metric, the extra-point move is to ask what decision it would change (Q75-017).

| Tier | What to say |
|---|---|
| Passes | "50" |
| Strong | + that the range is −100 to +100, not a percentage, and that passives dilute without scoring |
| Extra points | **[+Edge cases]** a 6 counts as badly as a 0, so the metric is insensitive within buckets and jumpy on small samples · **[+Business]** useful as a trend on a stable population, poor for cross-company comparison · **[+Validate]** always report the sample size and the response rate with it; a 15% response rate selects for the opinionated |

**Likely follow-ups:** What response rate would worry you? How would you detect a biased sample? What would you measure instead? *(A task-level satisfaction score tied to a specific action, usually.)*
**Learn it in:** Chapter 23, section 23.10 (customer metrics).

### Rapid-fire, 75.7: metric arithmetic

Roles: DA, PA and BA for every row.

| # | Question | The answer, and why | Extra point |
|---|---|---|---|
| Q75-039 | Conversion went from 2% to 3%. Is that "up 1%" or "up 50%"? | Both, and they are different claims: +1 percentage point, +50% relative. Saying "percent" when you mean "points" overstates or understates by 50× here | **[+Business]** always say "points" or "relative"; the ambiguity is expensive → Ch 23 §23.6 |
| Q75-040 | Average order value rose and total revenue fell. What happened? | Fewer orders, and probably the cheap ones stopped. A rising average can be a shrinking base — the mix changed, not the behaviour | **[+Validate]** always read an average beside its count → Q75-011 |
| Q75-041 | A cohort retention curve flattens at 40% after month 6. What does that mean? | You have a stable core. The flat part is the real business; the steep early part is onboarding failure, and they need different fixes | **[+Business]** a curve that never flattens means no product-market fit at any scale → Ch 23 §23.9 |
| Q75-042 | Two regions, each improved conversion this quarter, but the company total fell. Possible? | Yes — Simpson's paradox, if traffic shifted towards the lower-converting region. Both facts are true | **[+Validate]** check the mix before explaining the trend → Ch 73 §73.6 |
| Q75-043 | "Our users are 60% female" — from a survey with a 12% response rate | Says little about users, a lot about responders. Non-response is rarely random | **[+Edge cases]** report the response rate with every survey figure → Ch 73 Q73-033 |
| Q75-044 | Median order value ₹1,200, mean ₹3,400. What does the gap tell you? | A long right tail: a few very large orders. The mean describes revenue, the median describes a typical customer, and both belong in the report | **[+Business]** targeting the mean customer usually means targeting nobody → Ch 21 §21.2 |
| Q75-045 | A metric is defined as "active users". Two teams report different numbers. | Almost always the definition, not the data: active in what window, counting what action, including or excluding internal accounts | **[+Clarify]** a metric without a written definition is not a metric → Q75-017 |
| Q75-046 | Week-on-week comparison for a business with a weekly cycle | Compare like with like: the same weekday, or a 7-day trailing total. Week-on-week on a Tuesday against a Saturday is noise | **[+Edge cases]** also watch for 4- against 5-week months in monthly figures → Ch 23 §23.6 |

---

## 75.8 Metric traps you can measure your way out of

Sections 75.1 to 75.6 are about structure, and structure is most of what a case interview grades. This section is the other half: five traps that *sound* like judgement calls and are actually settled by arithmetic you can do in the room.

**Every figure in this section is measured on Riverstone's October–December 2025 order data** — `companion/ch14/clean_truth_orders_q4_2025.csv`, the cleaned file Chapter 14 produces and Chapter 72B interrogates. 25,832 order lines, 14,372 orders, ₹44.26 crore of net revenue. Nothing here is an illustrative round number, and two of the answers contradict what the cliché would have predicted.

### Q75-047 · December revenue is ₹9.11 crore against October's ₹18.85 crore. Diagnose it.

**Level:** Mid · **Roles:** DA, DS, BA, AE

**Remember it as:** *First ask whether the period is complete. Then decompose into count × value. Two subtractions beat an hour of speculation.*

**Answer in one line:** Check the period boundary first — the December data stops on the 28th, which explains about 10% of the gap — then decompose the remainder into **how many orders** against **how much per order**, which shows that order count fell 18% while value per order fell 41%, so this is a price-or-mix problem rather than a demand problem.

**Step 1 — is the period complete?** Always first, because it is free and it is the single most common cause of a scary-looking drop.

| Month | Net revenue | Last order date |
|---|---|---|
| October | ₹18.85 cr | 31st |
| November | ₹16.29 cr | 30th |
| **December** | **₹9.11 cr** | **28th** |

December is missing three days. Scaling it to a full 31 days gives ₹10.09 crore, which adds **₹0.98 crore** to a gap of **₹9.74 crore**. So incompleteness accounts for **10% of the fall and no more** — worth establishing in one minute, and worth not stopping there, which is the mistake the previous month's analyst usually makes.

**Step 2 — decompose.** Revenue is orders × value per order, so one of the two must have moved:

| | October | December | Change |
|---|---|---|---|
| Orders | 5,184 | 4,226 | **−18%** |
| Net revenue per order | ₹36,367 | ₹21,563 | **−41%** |
| Lines per order | 1.79 | 1.80 | unchanged |
| Net revenue per line | ₹20,368 | ₹11,976 | **−41%** |

**Both moved, and value moved more than twice as hard as count.** The third row is what makes the answer specific: basket size did not change, so customers are not buying fewer items per order. The fall is entirely in the **value of each line** — which points at price, product mix, or discount, and away from demand.

**Step 3 — name the next query, not the cause.** The honest end of this answer is not a conclusion, it is the one query that would separate the remaining candidates: revenue per line by product and by discount tier, October against December. If the mix shifted toward the ₹115 product, that is one story; if the same products are being sold at bigger discounts, that is a different and more urgent one.

| Tier | What to say |
|---|---|
| Passes | Suggests plausible causes — seasonality, fewer customers, a lost account |
| Strong | Checks period completeness first, decomposes into count × value, and reads the unchanged basket size as evidence that narrows the cause |
| Extra points | + **[+Validate]** quantify the incomplete-period effect rather than mentioning it: ₹0.98 crore of a ₹9.74 crore gap, so 90% is real + **[+Signpost]** the decomposition is Chapter 23's KPI tree used as a diagnostic, not a dashboard + **[+Business]** end with the single query that would discriminate between the surviving causes, which is what makes the answer actionable + **[+Edge cases]** a drop concentrated in one branch or one segment would change the story again, so check the breakdown before concluding anything about price |

**Likely follow-ups:** Which product-mix shift would produce exactly this pattern? How would you present this to a sales head in one slide?
**Red flag:** naming a cause before checking whether the period is even complete.
**Learn it in:** Chapter 23, §23.11 (diagnosing a change); Chapter 5, §5.4 (issue trees and MECE); Chapter 4, §4.3 (ratios and rates: always ask about the denominator).

### Q75-048 · "Our revenue is concentrated in a few big customers." Is it?

**Level:** Mid · **Roles:** DA, DS, BA

**Remember it as:** *80/20 is a slogan, not a property of your data. It takes one query to find out, and it is often wrong.*

**Answer in one line:** On this data, no — the top 20% of customers produce **41.4%** of revenue, not 80%, and the top 1% produce **3.5%** — so the business is far less concentrated than the Pareto cliché assumes, and the strategy implications are the opposite of what "a few big customers" would suggest.

**Measured, on 4,237 customers who ordered in the quarter:**

| Top share of customers | Share of revenue |
|---|---|
| 1% (42 customers) | **3.5%** |
| 5% (211) | **14.1%** |
| 10% (423) | **24.7%** |
| 20% (847) | **41.4%** |

**This is the answer interviewers are hoping someone will check.** "80/20" gets asserted in strategy conversations constantly, and here it is simply not true: revenue is spread broadly across a long tail of similar-sized wholesale customers. The consequences are concrete and they run the other way:

- **A key-account programme would not move the needle much.** The top 42 customers are 3.5% of revenue; winning 10% more from all of them is worth 0.35% of revenue.
- **Losing any single customer is not a material risk**, which is good news nobody had quantified.
- **Broad-based initiatives beat targeted ones here** — pricing, range, delivery reliability — precisely because no small group dominates.

**The general lesson, which is the point of the question.** A distributional claim is cheap to test and expensive to assume. Ask "has anyone measured that?" and then measure it, because the answer changes the strategy rather than decorating it.

| Tier | What to say |
|---|---|
| Passes | Says they would check the revenue by customer and sort it |
| Strong | Produces the cumulative-share table, states that 80/20 does not hold here, and draws the strategic consequence |
| Extra points | + **[+Business]** quantify the implication: a key-account push on the top 1% is worth 0.35% of revenue if it lifts them 10% + **[+Validate]** say which denominator you used — 4,237 customers who *ordered this quarter*, not the 5,027 on the master, and the choice matters + **[+Edge cases]** concentration can be real in margin while absent in revenue, so check both before advising + **[+Clarify]** ask what decision rests on the concentration claim, because that decides whether to measure by revenue, margin or volume |

**Likely follow-ups:** How would this change if you measured margin instead? What would genuine concentration imply for credit risk?
**Red flag:** repeating 80/20 as though it were a property of all businesses.
**Learn it in:** Chapter 23, §23.9 (customer metrics); Chapter 15, §15.7 (parts of a whole: stacked bars, pies, and waterfalls).

### Q75-049 · You suspect Simpson's paradox in the branch comparison. How do you check, and what if it is not there?

**Level:** Senior · **Roles:** DA, DS

**Remember it as:** *Check the mix, then the within-group rates. Ruling the paradox out is a finding, not a dead end.*

**Answer in one line:** Compare the **composition** of each group and the **within-segment rates**: a paradox needs the mix to differ between groups *and* the within-segment behaviour to run the other way — and on this data neither holds, so the branch comparison can be read at face value, which is itself worth reporting.

**Measured.** Segment mix by branch, as a percentage of each branch's lines:

| Branch | Retail | Hospitality | Wholesale |
|---|---|---|---|
| Bengaluru | 53.5 | 25.6 | 20.9 |
| Delhi | 49.4 | 28.4 | 22.2 |
| Kolkata | 50.2 | 29.8 | 20.0 |
| Mumbai HO | 50.7 | 27.1 | 22.3 |

Mean revenue per line, by branch and segment:

| Branch | Retail | Hospitality | Wholesale |
|---|---|---|---|
| Bengaluru | ₹15,806 | ₹15,853 | ₹22,076 |
| Delhi | ₹15,678 | ₹16,042 | ₹21,963 |
| Kolkata | ₹15,607 | ₹15,898 | ₹21,972 |
| Mumbai HO | ₹15,895 | ₹15,636 | ₹21,922 |

**Both conditions fail.** The mix is near-uniform — retail is about half of every branch — and within each segment the branches perform within about 3% of each other. So the paradox is absent, and the headline comparison is trustworthy.

**Why "it is not there" is a real answer.** It licenses the simple comparison. Without the check, any branch ranking is open to the objection "but Mumbai sells to different customers", and you cannot answer it. With the check, you can say the mix is uniform and the ranking stands. **An interviewer asking this is often testing whether you can accept a negative result** rather than hunting for an effect until you find one.

**And the thing the check did reveal.** Wholesale lines are worth about **40% more** than retail or hospitality lines in every branch, consistently. That is a stable, actionable fact that the paradox hunt turned up as a by-product, and it is more useful than the paradox would have been.

| Tier | What to say |
|---|---|
| Passes | Says they would break the comparison down by a confounder |
| Strong | Names both conditions a paradox requires, tests each, and reports the negative result as licensing the simple comparison |
| Extra points | + **[+Validate]** stating that the mix is uniform is what makes the headline ranking defensible against the obvious objection + **[+Business]** the by-product finding — wholesale lines worth about 40% more, consistently across branches — is the actionable output + **[+Edge cases]** a paradox can hide in a third variable you did not segment on, so say which confounders you checked and which you did not + **[+Trade-offs]** with many candidate confounders this becomes multiple comparisons, so prefer the few with a causal story over testing everything |

**Likely follow-ups:** Which other confounder would you check here? What would the tables look like if the paradox *were* present?
**Red flag:** continuing to segment until some subgroup shows a reversal, then reporting it.
**Learn it in:** Chapter 22, §22.6 (Simpson's paradox); Chapter 23, §23.11 (diagnosing a change).

### Q75-050 · Mumbai takes ₹15.73 crore and Kolkata ₹5.45 crore. Is Mumbai the better branch?

**Level:** Mid · **Roles:** DA, BA, DS

**Remember it as:** *A total measures size. Ask what you would do differently if the answer were yes, and the right denominator appears.*

**Answer in one line:** Not on that evidence — Mumbai is **2.9× larger**, but revenue per order differs by only **2.5%** across all four branches, so the branches differ almost entirely in volume rather than in how well they sell, and "better" needs a denominator before it means anything.

**Measured:**

| Branch | Orders | Revenue | Revenue per order |
|---|---|---|---|
| Mumbai HO | 5,075 | ₹15.73 cr | ₹30,994 |
| Bengaluru | 3,985 | ₹12.31 cr | ₹30,878 |
| Delhi | 3,511 | ₹10.78 cr | ₹30,694 |
| Kolkata | 1,801 | ₹5.45 cr | ₹30,241 |

**A 2.9× spread in total against a 2.5% spread per order.** The per-order column is almost flat, and that flatness is the finding: whatever differs between these branches, it is not how they sell. The question "which branch is better?" was really "which market is bigger?", and the two have entirely different implications — one is about headcount and territory, the other about coaching and process.

**What a strong answer asks for next.** Per-order value is the wrong denominator for a performance question anyway. The ones that would actually settle it:

- **Revenue per salesperson**, which is the efficiency question the original one was reaching for
- **Growth rate**, since the smallest branch may be the fastest-growing
- **Cost to serve**, because Kolkata's ₹5.45 crore may be more profitable per rupee than Mumbai's

None of those three is in this file, and saying so — naming the data you would need — is better than answering the question with the data you happen to have.

| Tier | What to say |
|---|---|
| Passes | Points out that Mumbai is bigger so the comparison is unfair |
| Strong | Produces the per-order column, reads its flatness as the finding, and names the denominators that would answer the real question |
| Extra points | + **[+Business]** "the branches differ in volume, not in selling" changes the decision from a performance conversation to a territory one + **[+Clarify]** ask what action rides on "better": headcount, bonus, investment and closure each want a different measure + **[+Validate]** the 2.5% spread is small enough to be noise at these volumes, so resist ranking on it + **[+Edge cases]** revenue per salesperson needs the headcount, which this file does not have; say that rather than substituting a proxy silently |

**Likely follow-ups:** How would you rank them for next year's investment? What if Kolkata had the highest growth?
**Red flag:** ranking branches on total revenue, or on a 2.5% difference.
**Learn it in:** Chapter 23, §23.8 (operations metrics); Chapter 23, §23.13 (defining a metric so two teams get the same number).

### Rapid-fire, 75.8

Roles: DA, DS, BA and AE for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q75-051 | What is a proxy metric, and when is one acceptable? | A measurable stand-in for something you actually care about but cannot observe — page views for interest, delivery time for satisfaction — acceptable when the link to the real outcome has been checked at least once and is stated, not assumed forever | **[+Validate]** a proxy's relationship to the real outcome decays, so re-check it rather than inheriting it | Mid · 23.12 |
| Q75-052 | What is a counter-metric, and why does every target need one? | A metric that would get worse if the main one were gamed — pair "orders shipped" with "orders returned", or "response time" with "issue reopened" — because any single target is optimised by the cheapest available route, which is often not the one you wanted | **[+Business]** Riverstone's cancellation rate (4.24% of lines, ₹1.87 crore) is the natural counter-metric to a revenue target | Mid · 23.12 |
| Q75-053 | What is survivorship bias, with a business example? | Drawing conclusions from the cases that remain while the ones that disappeared are invisible: analysing "our customers' satisfaction" tells you about the ones who stayed, and says nothing about everyone who already left for the reason you are trying to find | **[+Edge cases]** the churned-customer analysis is the one nobody has the data for, which is exactly why it matters | Mid · 22.7 |
| Q75-054 | How do you tell seasonality from a real decline? | Compare the same period last year, not the previous month, and check that the period is complete — without a prior year you cannot claim seasonality at all, and saying so is better than asserting it | **[+Signpost]** Q75-047 shows the completeness check settling 10% of a gap before any seasonality argument starts | Mid · 23.11 |
| Q75-055 | A metric improved right after you started measuring it. Suspicious? | Yes, in two ways: what gets measured gets managed, so some of the gain is real behaviour change, and some is usually definition drift or better recording of the same underlying activity | **[+Validate]** check whether the *count of records* changed as well as the rate, which separates recording changes from real ones | Senior · 23.12 |
| Q75-056 | Why is an average a bad headline for a skewed distribution? | Because the mean is pulled by the tail and describes nobody: on this data the mean order is ₹30,794 and the median ₹26,250, so a target set on the mean can be hit by a handful of large orders with no change in typical behaviour | **[+Signpost]** report both; the gap between them is the finding | Fresher · 21.4, 15.5 |
| Q75-057 | Your dashboard has 40 metrics. What would you do? | Ask which decision each one supports and remove every metric that has no answer; a dashboard with 40 numbers is a data dump, and the test of a metric is that somebody would act differently if it moved | **[+Business]** fewer, decision-linked numbers beat completeness, because nobody reads the fortieth | Mid · 23.10, 15.11 |

---

## 75.9 Product decisions with no clean answer

These are the questions where the interviewer is not looking for a recommendation at all. They are looking for whether you can see the second-order effect, say what evidence would decide it, and be comfortable that the honest answer is conditional.

### Q75-058 · You launch a cheaper version of your best product. Sales rise. Did it work?

**Level:** Senior · **Roles:** DA, DS, BA

**Remember it as:** *Unknown until you check what the new buyers would otherwise have bought. Cannibalisation is invisible in a total.*

**Answer in one line:** You cannot tell from total sales rising — the question is whether the new product brought **new** customers or moved existing ones down from a more expensive item, so you have to compare at the level of the customer and the margin, not the unit.

**The three outcomes a rising total could be hiding:**

| | What happened | How total sales look |
|---|---|---|
| **Genuine growth** | New customers who were not buying at all | Up, and margin up |
| **Cannibalisation** | Existing customers switching down from the dearer product | Up in units, **down in margin** |
| **A mix** | Both, in unknown proportion | Up, margin ambiguous |

**What to measure, in order:**

1. **Margin, not revenue.** Units and revenue can rise while contribution falls. This is the single check that distinguishes the first two rows.
2. **A cohort view of existing customers.** Did the people who bought the ₹1,400 product last quarter buy the cheap one this quarter, and did their total spend fall?
3. **New-customer count.** Genuine growth shows up as customers who had no prior orders at all.
4. **The counterfactual.** Sales might have risen anyway. Without a control — a region that did not get the new product, or a staged rollout — the honest answer is conditional, and saying so is the point.

**The judgement to volunteer.** Cannibalisation is not automatically bad. If the cheaper product defends against a competitor, or converts a customer who was about to leave, trading margin for retention can be right. **The failure is not knowing which is happening**, which is what makes this a measurement question rather than a strategy one.

| Tier | What to say |
|---|---|
| Passes | Says they would check whether sales of the expensive product fell |
| Strong | Distinguishes the three outcomes, puts margin before revenue, and uses a customer-level cohort rather than product totals |
| Extra points | + **[+Validate]** without a control region or a staged rollout you cannot attribute the rise at all, so name the counterfactual explicitly + **[+Business]** cannibalisation can be the right trade when it buys retention, so the recommendation is conditional on which it is + **[+Edge cases]** a cheaper version can also reset what customers think the dear one is worth, which shows up later as price resistance rather than in this quarter's numbers + **[+Clarify]** ask what the launch was *for*, because defending share and growing margin want different verdicts on the same data |

**Likely follow-ups:** How would you design the staged rollout? What if margin data is not available by product?
**Red flag:** declaring success from a rise in units or revenue.
**Learn it in:** Chapter 23, §23.5 (sales metrics) and §23.7 (finance metrics); Chapter 30, §30.8 (designing an experiment, and why a control matters).

### Q75-059 · A feature has 2% adoption after six months. Kill it?

**Level:** Mid · **Roles:** DA, DS, BA

**Remember it as:** *2% of whom, doing what, and worth how much? A low rate on a large valuable base can be the best feature you have.*

**Answer in one line:** Not on the rate alone — establish the denominator, whether the 2% is the segment the feature was built for, what those users are worth, and whether the cost of keeping it is real — because a feature used by 2% of all users may be used by 60% of the segment it was designed for.

**The questions, in order of how much they change the answer:**

| | |
|---|---|
| **Denominator** | 2% of all users, or of the users it was built for? A feature for wholesale customers should be measured against wholesale customers — 21% of Riverstone's lines — not everyone |
| **Who** | If the 2% are the largest accounts, the revenue they represent may dwarf a feature used by everyone |
| **Discoverability** | Low adoption can be a placement problem rather than a value problem, and that is cheap to test before killing anything |
| **Cost to keep** | Maintenance, support, and the constraint it puts on other changes. If it is near zero, the bar for removal is high |
| **What was the target?** | If 2% was the stated success criterion, it succeeded. If nobody set one, that is the finding |

**The last row is the one to say out loud.** A feature with no pre-agreed success measure cannot pass or fail, and the question is then really about how the organisation makes decisions. Chapter 75's own Q75-022 is the discipline that prevents it: fix the metric and a rough target *before* building.

**On sunsetting, when the answer is yes.** Removal is a project, not a deletion: tell the 2% first, give them a migration path or an explicit answer that there is none, keep it available long enough for them to adapt, and measure whether they churn. A feature removed quietly from under its only users costs more goodwill than it saves in maintenance.

| Tier | What to say |
|---|---|
| Passes | Asks for more context about who uses it before deciding |
| Strong | Interrogates the denominator first, then user value, discoverability, cost to keep, and whether a target existed |
| Extra points | + **[+Clarify]** "2% of whom?" is the single question that most often reverses the answer + **[+Business]** if the 2% are the largest accounts, the feature's revenue exposure can exceed anything used by the majority + **[+Validate]** test discoverability with a placement change before concluding the feature lacks value + **[+Edge cases]** sunsetting needs a notice period and a migration path, and the churn of the affected users is the metric that tells you whether the removal was handled well |

**Likely follow-ups:** How would you run the discoverability test? What would you tell the 2% on the day you remove it?
**Red flag:** killing or keeping it on the strength of the 2% alone.
**Learn it in:** Chapter 23, §23.10 (KPI trees and the North Star); Chapter 5, §5.2 (from a vague request to a precise question).

### Rapid-fire, 75.9

Roles: DA, DS and BA for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q75-060 | What is a network effect, and how would you detect one in the data? | A product that gets more valuable as more people use it; you detect it by checking whether a user's own value or retention rises with the number of *connected* users, not with total users, which would rise anyway with growth | **[+Edge cases]** growth and a network effect look identical in a total, so the test has to be at the level of the individual user's connections | Senior · 23.10 |
| Q75-061 | How would you estimate willingness to pay without running a price test? | Triangulate rather than guess: what customers pay for the nearest substitute, what the switching cost is, what they currently spend on the problem, and where existing discount tiers already cluster — then state it as a range with the method, not a number | **[+Validate]** Riverstone's four discount tiers (0, 5, 8, 10, 12%) are revealed-preference evidence sitting in the order data | Senior · 23.7 |
| Q75-062 | What is activation, and why is it the metric most teams get wrong? | The point at which a new user has done enough to get real value; teams get it wrong by defining it as something easy to measure (signed up, logged in twice) rather than as the action that actually predicts staying | **[+Validate]** define it by finding which early action correlates with retention, then sanity-check that the link is plausible rather than coincidental | Mid · 23.10 |
| Q75-063 | Two features, one helps 100,000 users slightly and one helps 500 users enormously. Which? | Neither without the goal: a growth goal favours the first, a retention goal on high-value accounts favours the second, and the honest answer names the goal that would decide it rather than picking | **[+Business]** quantify both in the same unit — revenue at risk, or hours saved — and the comparison stops being a matter of taste | Mid · 25.12, 23.10 |
| Q75-064 | A stakeholder wants a metric that always goes up. What do you say? | That a metric which can only rise is not measuring anything you can act on: cumulative totals always rise regardless of performance, so you need a rate, a ratio or a period comparison for the number to carry information | **[+Edge cases]** cumulative revenue-to-date is the classic example, and it looks healthy in every possible world | Mid · 23.12 |
| Q75-065 | How do you measure something that has not happened yet? | With a leading indicator plus an explicit statement of the lag: quotes sent predicts revenue weeks ahead, and the forecast is only as good as the historical relationship between the two, which you check rather than assume | **[+Validate]** state the lag and the historical hit rate, or the leading indicator is a guess with a chart | Senior · 23.11, 30.7 |
| Q75-066 | Your A/B test is flat but the team is sure the feature is better. What now? | Check whether the test could have detected the effect at all — the minimum detectable effect given the sample — because a flat result from an underpowered test is not evidence of no effect, it is absence of evidence | **[+Signpost]** practise it with Chapter 73, Q73-021; the distinction is the whole of Chapter 22 | Senior · 22.3, 30.7 |
| Q75-067 | How would you decide whether to raise prices by 3%? | Estimate volume sensitivity from whatever evidence exists, compute the break-even volume loss (at a 3% rise you can afford to lose roughly 3% of volume at constant margin before you are worse off), then test on a segment rather than everywhere | **[+Validate]** the break-even calculation is cheap, reversible-decision arithmetic and almost nobody does it before arguing | Senior · 23.7, 4.2 |
| Q75-068 | What would make you recommend doing nothing? | When the cost of the change exceeds the measured benefit, when the decision is cheap to defer and more information is arriving, or when the data cannot answer the question and acting would just be acting — and recommending it with reasons is a senior move, not a failure | **[+Business]** "do nothing, and here is what would change my mind" is a complete recommendation | Senior · 5.8, 23.13 |

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

MECE (Mutually Exclusive, Collectively Exhaustive) · diagnostic case · product-decision case · weekly active users · leading indicator · lagging indicator · North Star metric · vanity metric · guardrail metric · average handle time · service-level agreement (SLA) · RICE · Fermi estimation · total addressable market (TAM) · top-down vs. bottom-up estimate · pilot (as a decision-testing step) · percentage points against relative percent · recovery asymmetry · compounding · survival rate · average customer lifetime (1/r) · funnel multiplication · DAU/MAU stickiness · contribution margin · LTV:CAC · CAC payback period · blended against paid CAC · NPS scale (−100 to +100) · promoter / passive / detractor · geometric mean · rule of 72

---

## Final-week revision list

Q75-001, Q75-002, Q75-007, Q75-008, Q75-013, Q75-014, Q75-017, Q75-019, Q75-024, Q75-025, Q75-030, Q75-031, Q75-032, Q75-033, Q75-037.

The last three are the arithmetic most likely to be wrong in a real deck: a fall and a rise of the same percentage (Q75-032), monthly churn annualised by multiplication (Q75-033), and an LTV:CAC ratio whose LTV turns out to be revenue (Q75-037).

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against, especially Moves 1 (clarify), 3 (signpost), and 7 (validate).
- **Chapter 76A, Data Analyst & Data Scientist Question Bank,** and **Chapter 76B, Business Analyst Question Bank,** continue from this chapter's case reasoning: 76A into project narratives, 76B into requirements and process questions.
- **Chapter 70, section 70.8,** already covers dashboard critique from the other direction, judging one that's already built rather than designing one from scratch.
- **Chapter 73, Statistics, Probability & Experimentation Bank,** is where a "pilot" proposed in any of this chapter's cases would actually need to be designed properly before running.
- **Chapters 3, 4, 5, 23 and 24** teach every technique this bank draws on, in full; this chapter tests them, it doesn't re-teach them.
