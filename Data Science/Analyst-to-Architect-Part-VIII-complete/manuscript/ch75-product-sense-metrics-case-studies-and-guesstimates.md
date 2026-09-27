# Chapter 75. Product Sense, Metrics, Case Studies & Guesstimates

*Part VIII — The Interview Playbook*

> **You will learn to:** structure an ambiguous business case the way an interviewer actually wants, instead of jumping straight to an answer · diagnose a metric that moved, systematically, not by guessing at causes · design a KPI dashboard that answers real decisions, not just displays numbers · size a market or estimate a quantity with a defensible structure, not a guessed final number.
>
> **How this chapter is built.** Same format as Chapters 70–74: every core question leads with a **"Remember it as…"** hook, a one-line answer, a compact tier table. Rapid-fire sections are scan tables. This chapter has no code to execute, since a case-interview or guesstimate answer is judged on structure and reasoning, not a computed output, but every number used in a worked example is arithmetically checked, and every framework is applied to a full worked case, not left abstract.
>
> **Section order was planned before writing:** the general case framework first, then the specific case type it applies to (metric drops, dashboard design, product decisions), then guesstimates as their own structured skill, then full live-coding-style walk-throughs pulling several moves together.

---

## 75.1 The general case framework

### Q75-001 · You're given a vague, one-sentence business question in an interview. Walk through your first sixty seconds

**Remember it as:** *Restate, clarify, structure, then answer, in that order, every single time, regardless of how simple the question sounds.*

**Answer in one line:** Restate the question in your own words to confirm you understood it, ask one or two clarifying questions that would genuinely change your approach, lay out a structure (a short list of the areas you'll investigate) before touching any specifics, and only then start filling in the structure with actual reasoning.

**Worked example**, applied to *"Our support team wants a way to know which customers to prioritize. How would you help them?"*:

> "Prioritize for what, exactly, retention risk, upsell potential, or urgency of a live issue? And is this a one-time list or a standing, updated view? I'll assume retention risk, updated regularly, unless you say otherwise. I'd look at this in three parts: what signals predict risk, how we'd turn those into a single prioritized list, and how support would actually act on it day to day."

| Tier | What to say |
|---|---|
| Passes | Jumps straight into an answer without restating or clarifying anything |
| Strong | Restates, asks one genuinely important clarifying question, states an assumption, and previews a structure before diving in |
| Extra points | + **[Clarify]** the clarifying question changes the actual approach, not a generic "what do you mean" + **[Structure]** the three-part preview above gives the interviewer a map of where the answer is going, so they can redirect early if it's the wrong direction, rather than sitting through five minutes before finding out |

**Likely follow-ups:** What if the interviewer won't answer your clarifying question? *(State your assumption explicitly and proceed; don't stall waiting for permission.)* How do you know when you've spent too long clarifying and not enough time actually answering?
**Red flag:** either no clarification at all, or clarifying so much it eats most of the available time without ever reaching a structured answer.
**Learn it in:** Chapter 69's Move 1 (clarify) and Move 3 (signpost), applied here to a full case instead of a single technical question.

### Q75-002 · What's the difference between a "diagnose a metric" case and a "should we build this" case, and why does mixing up the structure hurt you?

**Remember it as:** *A metric-drop case works backward from a number to a cause. A product-decision case works forward from a goal to a recommendation. Using the wrong shape wastes the whole case.*

**Answer in one line:** A metric-diagnosis case starts from an observed change and works backward through possible causes (data issue, external factor, internal change, segment-specific shift) to find what actually happened; a product-decision case starts from a goal or user need and works forward through options, trade-offs, and success metrics to reach a recommendation: using a diagnostic structure on a decision question (or vice versa) produces an answer that technically covers ground but never actually answers what was asked.

| Tier | What to say |
|---|---|
| Passes | Treats every case with the same generic checklist regardless of question type |
| Strong | Explicitly identifies which of the two shapes the question is (or names a case that's genuinely a hybrid) before choosing a structure |
| Extra points | + **[Business]** naming the case type out loud in the first thirty seconds ("this sounds like a diagnostic case, so I'll work backward from the number") itself signals structured thinking to the interviewer, before any content has even been delivered |

**Likely follow-ups:** What's a case that's genuinely a hybrid of both? How would you handle a case where the interviewer's question doesn't clearly signal which type it is?
**Red flag:** applying a rigid, memorized framework to every case regardless of fit, producing a technically thorough but off-target answer.
**Learn it in:** §75.2 (diagnostic cases) and §75.4 (product-decision cases) below.

### Rapid-fire, 75.1

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q75-003 | What's a MECE structure? | Mutually Exclusive, Collectively Exhaustive: a breakdown where categories don't overlap and together cover the whole space | **[Business]** a non-MECE structure (say, "large customers" and "enterprise customers" as separate buckets) leads to double-counting or gaps that quietly undermine the whole analysis |
| Q75-004 | Why state an assumption out loud instead of silently picking one? | It lets the interviewer correct you immediately if you assumed wrong, rather than watching you build fifteen minutes of analysis on the wrong foundation | **[Learn it in]** Chapter 69's Move 2 |
| Q75-005 | How much time should structuring take relative to the whole case? | Roughly 10–15%, enough to set direction, not so much that there's no time left to actually work through it | **[Edge cases]** over-structuring (a beautiful framework with no time left to fill it in) scores worse than a slightly rougher structure that's actually worked through |
| Q75-006 | What's the risk of a purely qualitative answer with zero numbers, in a case that clearly has data available? | It signals an inability or unwillingness to quantify, which is usually exactly what the interviewer is testing for in a data-adjacent role | **[Business]** even a rough, clearly-labeled estimate ("if I had to guess, maybe 20% of the drop") beats no number at all |

---

## 75.2 Diagnosing a metric that moved

### Q75-007 · "Weekly active users dropped 15% last week. Walk me through how you'd figure out why."

**Remember it as:** *Verify the number is real before you go hunting for a business reason it might not need.*

**Answer in one line:** Check data integrity first (a tracking bug, a reporting change, a timezone or date-boundary artifact), then check for an external or seasonal explanation (a holiday, a known outage, a competitor event), then look for an internal cause (a recent release, a pricing change, a removed feature), and only then drill into which segment of users actually drove the drop.

**Worked structure, applied out loud:**

> "First, I'd confirm the 15% is measured the same way it always is; a logging change or a shifted week boundary can produce a number that looks like a real business drop but isn't one. Assuming it's real, I'd check for anything external that week, a holiday, an outage, a competitor launch, before assuming it's something we did. Then I'd check what changed internally: a release, a pricing change, a removed feature, in roughly that order of likelihood. Finally, I'd segment the drop by platform, geography, and user tenure to see if it's broad or concentrated, since a drop concentrated in one segment points to a very different cause than a broad, even one."

| Tier | What to say |
|---|---|
| Passes | Jumps straight to guessing specific causes ("maybe it's a competitor" or "maybe the app is slow") with no verification step first |
| Strong | The four-stage funnel above: verify the data, check external factors, check internal changes, then segment |
| Extra points | + **[Validate]** explicitly proposes checking whether the drop is broad or concentrated in one segment, since that single fact rules out most hypotheses at once + **[Business]** ties the investigation to a concrete next action at each stage, not just a list of things to "look into" |

**Likely follow-ups:** The drop turns out to be concentrated entirely in one country. What does that suggest, and what would you check next? How would you distinguish a real user-behavior change from a measurement artifact, concretely?
**Red flag:** guessing a specific root cause before verifying the number and ruling out the broad categories.
**Learn it in:** Chapter 69's Move 5 (edge cases) and Move 7 (validate), applied to a full diagnostic case.

### Q75-008 · "Revenue is up 10% year over year, but our finance team is worried. Why might a rising number still be bad news?"

**Remember it as:** *A single headline number can hide a mix shift, a one-time event, or a sustainability problem underneath a technically true "growth" story.*

**Answer in one line:** Revenue growth can mask a worse underlying picture in several ways: it might be driven by a small number of large, unrepeatable deals rather than broad healthy demand; it might be coming at the cost of margin (revenue up, profit down); it might be masking customer churn (fewer, bigger customers replacing many smaller ones, a riskier concentration); or it might not be keeping pace with a cost base or a target that's growing even faster.

| Tier | What to say |
|---|---|
| Passes | Can't think of a reason growth would be concerning, treats "up" as automatically good |
| Strong | Names at least two of the mechanisms above with a concrete business reason each matters |
| Extra points | + **[Business]** ties each mechanism to a specific follow-up metric that would confirm or rule it out: margin trend for the profit concern, customer count and concentration for the mix-shift concern, cohort retention for the churn-masking concern |

**Likely follow-ups:** Which of these would you check first, and why? How would you present this nuance to a stakeholder who's happy about the headline number?
**Red flag:** treating "revenue is up" as inherently good news with no interrogation of what's underneath it.
**Learn it in:** §75.3 below (dashboard design), where the same underlying-mix problem shows up again.

### Rapid-fire, 75.2

| # | Scenario | Structure to reach for | Extra point |
|---|---|---|---|
| Q75-009 | Conversion rate on the checkout page dropped after a redesign | Data-first: confirm the drop wasn't caused by an analytics tagging change in the redesign itself before assuming the design is at fault | **[Edge cases]** a redesign that changes page structure very often breaks event tracking at the same time it changes the actual experience, tangling two separate questions together |
| Q75-010 | Customer support ticket volume spiked | Segment by ticket category first: a spike concentrated in one issue type points to a specific bug or change; a broad spike across categories points to something upstream (an outage, a billing run) | **[Business]** ticket *volume* alone doesn't say whether it's a new problem or a known one just getting reported more, worth checking against a "first time this issue" flag if one exists |
| Q75-011 | Average order value is flat, but total revenue fell | The drop is in order *count*, not order value; the investigation should shift entirely toward acquisition/traffic/conversion, not pricing or basket size | **[Depth]** this is the same decomposition discipline as Chapter 44's revenue tree (orders × average order value), just applied live under interview pressure |
| Q75-012 | A metric looks fine in aggregate but a stakeholder insists something's wrong in their area | Always check for Simpson's paradox (Chapter 73, Q73-031) before dismissing the stakeholder: an aggregate can hide a real, reversed trend in a specific subgroup | **[Real evidence]** the stakeholder closest to the data is often right about a localized problem an aggregate view genuinely can't show |

---

## 75.3 Designing metrics and dashboards

### Q75-013 · "Design a KPI dashboard for a customer support team's manager." Walk through your approach

**Remember it as:** *Ask what decision the dashboard needs to support before picking a single metric. A dashboard with no decision behind it is just numbers on a wall.*

**Answer in one line:** Start from the decisions the manager actually needs to make (staffing that day, which tickets need escalation, whether the team is meeting its service commitments), then pick the smallest set of metrics that supports those decisions, rather than starting from "what data do we have" and displaying all of it.

**Worked structure:**

> "I'd ask what decisions this manager makes weekly: probably staffing levels, escalation priority, and reporting up to their own leadership. For staffing, I'd want ticket volume trend and average handle time. For escalation, open tickets by age and by severity, so anything aging past a threshold is visible immediately. For reporting up, a service-level metric like % of tickets resolved within target time, trended over time, not just a snapshot. I'd deliberately leave off vanity metrics like total tickets ever handled, since it doesn't drive any decision this specific manager makes day to day."

| Tier | What to say |
|---|---|
| Passes | Lists metrics that "seem relevant" to customer support with no connection to a specific decision |
| Strong | The decisions-first structure above, with metrics explicitly tied to staffing, escalation, and reporting |
| Extra points | + **[Business]** explicitly excludes a plausible-sounding but decision-irrelevant metric, which signals real judgment, not just metric-generation + **[Edge cases]** flags that a single "tickets resolved" count can hide the exact Simpson's-paradox-style mix problem from Q75-012, an SLA breakdown by ticket type is more honest than one blended number |

**Likely follow-ups:** How would this dashboard differ for a frontline agent instead of a manager? What's one leading indicator (predicts a future problem) versus one lagging indicator (reports a past one) you'd include, and why have both?
**Red flag:** a dashboard design that's really just "every metric I can think of related to the topic," with no filter for what's actually decision-relevant.
**Learn it in:** Chapter 70, §70.7's dashboard critiques (Q70-069/070), the same "does this serve a real decision" discipline applied there to an already-built dashboard instead of a from-scratch design.

### Q75-014 · What's the difference between a leading and a lagging indicator, and why does a good dashboard need both?

**Remember it as:** *A lagging indicator tells you what already happened. A leading indicator gives you a chance to change what happens next.*

**Answer in one line:** A **lagging indicator** (revenue, churned customers, resolved tickets) reports an outcome after it's already occurred, useful for accountability and reporting; a **leading indicator** (website traffic, open pipeline, ticket backlog growth rate) signals a likely future outcome early enough to still act on it: a dashboard built entirely on lagging indicators can only ever confirm a problem after it's too late to prevent it.

| Tier | What to say |
|---|---|
| Passes | Defines the terms correctly, can't give a concrete pair from the same domain |
| Strong | A matched pair from one domain: e.g. churned customers (lagging) vs. a declining product-usage trend among still-active customers (leading, since it predicts churn before it happens) |
| Extra points | + **[Business]** a dashboard's real value often comes specifically from its leading indicators, since the lagging ones mostly confirm what a team already suspects by the time the number moves |

**Likely follow-ups:** Name a leading indicator for churn that isn't usage frequency. How would you validate that a proposed leading indicator actually predicts the lagging outcome, rather than just correlating with it?
**Red flag:** unable to distinguish the two, or naming a lagging indicator as an example of a leading one.
**Learn it in:** Chapter 73, §73.6 (correlation, causation, and what actually validates a leading indicator as predictive, not just correlated).

### Rapid-fire, 75.3

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q75-015 | What's a vanity metric? | A number that looks impressive and trends upward easily, but doesn't connect to a real business decision or outcome (total signups ever, cumulative downloads) | **[Business]** the test: "if this number changed, would anyone actually do anything differently?": if not, it's a vanity metric |
| Q75-016 | Why is a single blended average often a worse metric than a segmented breakdown? | It can hide Simpson's-paradox-style reversals (Q75-012) and mask the fact that different segments need entirely different actions | **[Learn it in]** Chapter 73, Q73-031 |
| Q75-017 | What's a North Star metric, and what's the risk of picking the wrong one? | The single metric a team optimizes above all others, chosen to represent genuine long-term value delivered; the wrong one (optimizing engagement time instead of a genuinely valuable outcome) can drive real behavior that technically hits the target while hurting the actual business | **[Business]** a North Star metric should be hard to "game" without also delivering real value, or it quietly becomes a target people optimize around instead of through |
| Q75-018 | How would you decide the right refresh frequency for a dashboard? | Match it to how often the decision it supports actually gets made: a daily staffing decision needs daily data; a quarterly strategy review doesn't need real-time numbers | **[Learn it in]** Chapter 70, §70.10 (Import mode vs. DirectQuery, the same freshness-vs-cost trade-off at the BI-tool level) |

---

## 75.4 Product sense and decision cases

### Q75-019 · "Should we build a loyalty program?" How do you approach a yes/no product decision with no data given upfront?

**Remember it as:** *A product decision case isn't "yes" or "no." It's "here's what would have to be true for yes to be right, and here's how I'd check."*

**Answer in one line:** Frame the decision around the conditions that would make it worthwhile (does the target segment actually respond to loyalty incentives, is the expected retention or spend lift big enough to cover the program's cost, is there a cheaper alternative that achieves the same goal), rather than trying to produce a confident yes/no with no data in hand.

**Worked structure:**

> "I'd start with what problem this is meant to solve: is retention the issue, average order value, or something else? Assuming retention, I'd want to know our current churn rate and whether we have any evidence, even anecdotal, that price or reward sensitivity is a real churn driver for our customers, versus something a loyalty program wouldn't fix, like product availability. Then I'd size it: rough cost of running the program against a plausible retention lift, even a rough one, to see if the economics could plausibly work before recommending we actually build it. I'd end with a recommendation to pilot on one segment first, rather than a company-wide commitment, given how much of this is still genuinely uncertain."

| Tier | What to say |
|---|---|
| Passes | Gives a confident "yes, loyalty programs are good for retention" with no structure or acknowledgment of uncertainty |
| Strong | The conditions-for-yes framing above, ending in a specific, proportionate recommendation (a pilot, not a full commitment) |
| Extra points | + **[Edge cases]** explicitly separates "would this help" from "is this the best use of the same budget," since a case that only evaluates one option in isolation misses cheaper alternatives that might solve the same problem + **[Business]** the pilot recommendation matches the actual level of confidence the analysis supports, rather than overclaiming certainty either direction |

**Likely follow-ups:** How would you design the pilot to actually produce a clear answer? What metric would tell you the pilot worked?
**Red flag:** a confident yes/no answer with no acknowledgment of what's actually unknown.
**Learn it in:** Chapter 73, §73.4–73.5 (A/B test design, exactly what a "pilot" here would need to be built well).

### Rapid-fire, 75.4

| # | Scenario | Key move | Extra point |
|---|---|---|---|
| Q75-020 | "Would you prioritize feature A or feature B?" with limited detail on either | Ask for the goal each feature serves and roughly how many users each would affect, before comparing; don't guess at relative value with no basis | **[Business]** reach for a simple, stated framework (reach × impact × confidence × effort, or similar) rather than an unstructured gut call |
| Q75-021 | "A competitor just launched a feature we don't have. Should we build it too?" | Ask whether the feature addresses a real, evidenced need of your own users, not just competitive parity, before recommending building it | **[Edge cases]** matching a competitor feature-for-feature with no evidence it matters to your own users is a common, costly trap |
| Q75-022 | "How would you know if a new feature is successful, before launch?" | Define the success metric and a rough target *before* building it, not after seeing what the number happens to be | **[Learn it in]** Chapter 73, Q73-021 (defining a Minimum Detectable Effect before running a test is the same discipline) |
| Q75-023 | "Our product has high engagement but low revenue. What would you investigate?" | Check whether the engaged users are the same users being monetized, or whether engagement and monetization are happening in two different, disconnected populations | **[Business]** a mismatch between who's engaged and who pays is one of the most common, fixable product-strategy problems this kind of question is fishing for |

---

## 75.5 Guesstimates: structured estimation

### Q75-024 · Estimate the number of gyms in Mumbai. Walk through your structure, not just a final number

**Remember it as:** *A guesstimate is judged on the chain of reasonable numbers, not on how close the final answer lands.*

**Answer in one line:** Break the target quantity into a chain of estimable factors (population → the fraction of that population who are gym-goers → the average size of a gym), state a defensible round number for each link, and multiply through, showing the full chain rather than a single guessed final number.

**Worked calculation, verified arithmetic:**
```
Mumbai population:                 ~20,000,000
% who regularly go to a gym:        ~3%
→ gym-going population:             600,000
average members per gym:            ~500
→ estimated number of gyms:         600,000 / 500 = 1,200
```

| Tier | What to say |
|---|---|
| Passes | States a single guessed number ("maybe a few thousand?") with no visible reasoning chain |
| Strong | The full chain above, with each factor justified in one sentence ("3% feels right for a mix of gym-goers and non-gym-goers across income levels in a big city") |
| Extra points | + **[Validate]** sanity-checks the final number against something known: "1,200 gyms across Mumbai's roughly 24 wards is about 50 per ward, which feels plausible for a dense city, not obviously too high or too low" + **[Edge cases]** flags the single most uncertain link in the chain (probably the 3% gym-going rate) as the one worth refining first if more precision were needed, rather than treating every link as equally solid |

**Likely follow-ups:** Which of your assumptions would you want real data to check first? How would the estimate change for a smaller city?
**Red flag:** a single number with no visible chain, or a chain so long and granular it becomes a guess wearing a structure's clothing.
**Learn it in:** Chapter 69's Move 6 (trade-offs) and Move 7 (validate), the sanity-check habit applied to an estimation chain instead of a query result.

### Q75-025 · Estimate the total addressable market, in rupees, for plastic storage containers sold to households across India

**Remember it as:** *Top-down (population → adoption → spend) and bottom-up (known sales × a growth multiplier) should land in the same rough neighborhood: if they don't, that gap itself is the interesting finding.*

**Answer in one line:** Chain population through the share of households who buy this category annually and average annual spend per buying household; where possible, sanity-check the top-down number against any bottom-up figure available (a known competitor's revenue, a known market report figure) rather than trusting one method alone.

**Worked calculation, verified arithmetic:**
```
Indian households:                          ~300,000,000
% buying plastic storage containers/year:    ~15%
→ buying households:                          45,000,000
average annual spend per buying household:    ~₹400
→ estimated market size:                      45,000,000 × ₹400 = ₹18,000,000,000  (₹18 billion)
```

| Tier | What to say |
|---|---|
| Passes | Guesses a round market-size number with no visible household-level reasoning |
| Strong | The full chain above, explicitly stated as top-down |
| Extra points | + **[Business]** notes this is a *category* size, not any one company's addressable share, and that a real answer would also need a bottom-up cross-check against known competitor or industry figures where available, exactly the kind of self-aware caveat that separates a strong guesstimate from an overconfident one + **[Depth]** ties the exercise back to Riverstone's own actual category (Chapter 3's business, storage and kitchen products) as the concrete anchor for why this specific market size would matter to a real company |

**Likely follow-ups:** How would you refine the 15% adoption figure if you had one real data point (say, Riverstone's own unit sales)? What's the biggest risk in this estimate being wrong by an order of magnitude?
**Red flag:** presenting a single top-down estimate as if it were precise, with no acknowledgment of the wide uncertainty band around it.
**Learn it in:** Chapter 73, §73.1 (the same "state each assumption, then compute" discipline as a Bayes' theorem calculation, just applied to market sizing instead of probability).

### Rapid-fire, 75.5

| # | Guesstimate | Structure to reach for | Extra point |
|---|---|---|---|
| Q75-026 | How many piano tuners are there in a city of 5 million? | Pianos owned → tunings needed per piano per year → tunings one tuner can do per year | **[Business]** the classic Fermi-problem format: every link should be a number you could defend in one sentence, not a fact you'd need to look up |
| Q75-027 | Daily revenue of a mid-size coffee shop | Customers per day (estimate from seating capacity and turnover, or foot traffic) × average ticket size | **[Validate]** verified arithmetic: 300 customers/day × ₹150 average ticket = ₹45,000/day, a number worth sanity-checking against a rough rent-and-staff cost estimate for the same shop |
| Q75-028 | Number of WhatsApp messages sent in India in one day | India's population → % of population on WhatsApp → average messages sent per active user per day | **[Edge cases]** "average" hides a skew (heavy users send far more than the median user); worth naming that the estimate is more uncertain because of it, rather than pretending the average is a clean single number |
| Q75-029 | How many gas stations does a country need? | Vehicles on the road → average fuel consumption → stations' typical daily throughput capacity | **[Depth]** this specific guesstimate is really a supply-demand balance question in disguise, not a pure counting one, worth naming explicitly |

---

## 75.6 Live-coding-style walk-throughs: full worked cases

### Q75-030 · Full case, talked through live: "Our email open rate dropped from 25% to 18% last month. What happened?"

**What they're really testing:** whether the full structure (verify, external, internal, segment) actually gets executed end to end under time pressure, not just described in the abstract.

**Talked through live, start to finish:**

> "First, I'd confirm the drop is measured consistently, same tracking pixel, same definition of 'open,' since email open-rate tracking is notoriously fragile, particularly around any change to how images load by default in major email clients, which can silently affect open tracking with nothing about the actual email changing at all. Assuming that checks out, I'd look for anything external: did a major email provider change its spam filtering or default image-blocking that month? Then internal: did we change our subject lines, sending time, sender name, or list composition (a big new batch of colder, less-engaged contacts added to the list would mechanically drop the average even with individually unchanged behavior)? Finally, I'd segment by list, by device, and by send time to see whether the drop is broad or concentrated. If it's concentrated in one email client, that points straight back to a client-side default-image-blocking change, not anything we did."

**Extra-points moves demonstrated:** **[Edge cases]** named a specific, real, well-known confound (email client default image-blocking changes) rather than a generic "maybe it's a tracking issue." **[Structure]** ran the full verify → external → internal → segment funnel completely, out loud, in order. **[Business]** connected the list-composition hypothesis to a concrete mechanism (a mechanical average effect from adding colder contacts) rather than just naming it as a possibility.

**Likely follow-ups:** The drop turns out to be broad, not concentrated in one client or segment. What does that change about your next hypothesis? How would you recommend recovering the open rate?
**Red flag:** listing possible causes without ever proposing how to actually distinguish between them.
**Learn it in:** §75.2 above, and Chapter 69's Move 5.

### Q75-031 · Full case, talked through live: "Design a single metric to measure whether Riverstone's new self-service reorder portal is succeeding"

**What they're really testing:** whether a single metric can be chosen and defended, or whether the answer collapses into an undifferentiated list of "things you could measure."

**Talked through live, start to finish:**

> "The portal's real goal is probably reducing manual reorder friction for repeat customers, not just 'more orders.' I'd propose **% of eligible repeat orders placed through the self-service portal, without needing a call or email to a rep**, as the single metric, since it directly measures adoption of the thing being built, not a proxy for it. I'd deliberately avoid 'total orders' as the top metric, since that's driven by far more than this one feature and wouldn't isolate the portal's actual contribution. I'd pair it with one guardrail metric, order accuracy or error rate through the portal, so we're not accidentally rewarding adoption that comes at the cost of more mistakes."

**Extra-points moves demonstrated:** **[Business]** explicitly rejected a plausible-sounding but poorly-isolated metric (total orders) and explained why. **[Edge cases]** added a guardrail metric unprompted, anticipating that optimizing the primary metric alone could create a hidden downside. **[Depth]** the chosen metric is a *rate* (self-service share of eligible orders), not a raw count, which is what makes it comparable over time regardless of overall business growth.

**Likely follow-ups:** How would you define "eligible" precisely? What would make you recommend killing the portal rather than iterating on it?
**Red flag:** naming several metrics with no commitment to a single primary one, or picking a metric that's really measuring overall business health rather than this specific feature.
**Learn it in:** §75.3 above (North Star metrics, Q75-017) and Chapter 70, §70.7's dashboard-design discipline.

---

## Common mistakes and how to spot them

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

Karan, interviewing for a Business Analyst role, is given the case: "Our biggest customer's order volume dropped 40% last quarter. What do you do?" He starts to ask his usual battery of clarifying questions, then stops and asks one specific one instead: "Is this customer still ordering at all, just less, or have they effectively gone dark?"

The interviewer's answer changes everything: the customer had placed exactly one small order the entire quarter, down from a steady weekly cadence. Karan immediately shifts his structure from a "why did volume decline gradually" diagnostic (checking pricing, product mix, competitor activity) to a "why did this relationship nearly stop" one (checking for a specific triggering event: a contract dispute, a champion leaving the customer's organization, a competitor winning an exclusive deal). He asks two more targeted questions and correctly guesses, out loud, that the most likely explanation is a champion departure, exactly what the interviewer had in mind.

The interviewer's note afterward: *"Most candidates ask five generic clarifying questions and get five generic answers. Karan asked one that actually changed his whole approach, and used the answer immediately."* The lesson isn't "ask fewer questions." It's that a clarifying question earns its place only if the answer would genuinely change what you do next, exactly Chapter 69's Move 1, and this case shows what it looks like when that discipline is followed for real, under pressure, rather than performed as a checklist item.

---

## Tools

No software specific to this chapter. A notebook or whiteboard to sketch a structure before speaking is the single most useful habit; interviewers consistently rate a candidate who visibly organizes their thinking (even three bullet points jotted down) higher than one who reasons entirely out loud with no visible structure.

---

## The project

**Goal:** run this chapter's full method on cases of your own choosing.

1. Pick a real metric from your own work that changed recently, and run the full verify → external → internal → segment funnel on it, even if you already know the answer, to practice the structure itself.
2. Design a one-page dashboard for a real team you're familiar with, starting explicitly from the decisions it needs to support, and cut anything that doesn't serve one.
3. Take a real "should we do X" question from your own workplace and write the "what would have to be true" framing for it, ending in a specific, proportionate recommendation.
4. Practice three guesstimates out loud, timed to under three minutes each, showing your full chain of reasoning, not just a final number.

---

## Final-week revision list

Q75-001, Q75-002, Q75-007, Q75-008, Q75-013, Q75-014, Q75-017, Q75-019, Q75-024, Q75-025, Q75-030, Q75-031.

---

## Key terms

MECE (Mutually Exclusive, Collectively Exhaustive) · diagnostic case · product-decision case · leading indicator · lagging indicator · North Star metric · vanity metric · guardrail metric · Fermi estimation · top-down vs. bottom-up estimate · pilot (as a decision-testing step)

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against, especially Moves 1 (clarify), 3 (signpost), and 7 (validate).
- **Chapter 76, Business Analyst Question Bank,** continues directly from this chapter's case and stakeholder-facing reasoning into BA-specific requirements and process questions.
- **Chapter 70, §70.7,** already covers dashboard critique from the other direction, judging one that's already built rather than designing one from scratch.
- **Chapter 73** (statistics and experimentation) is where a "pilot" proposed in any of this chapter's cases would actually need to be designed properly before running.
