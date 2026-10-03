# Chapter 76A. Data Analyst & Data Scientist Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the role-specific questions a Data Analyst or Data Scientist interview actually asks, distinct from the skill-testing banks elsewhere in this part (SQL, Python, stats, ML) · walk an interviewer through a real project end to end, at the right level of depth for each role · handle the "what's the difference between a DA and a DS" question, and the harder version, "which one are you actually best suited for" · survive a portfolio deep-dive without getting caught flat-footed on a detail you glossed over.
>
> **Before you start:** Chapter 7, §7.2 (the tracks and the ten roles) · Chapter 8, §8.5 (decoding a job description) · Chapter 24, §24.4–24.8 (bottom line up front, the memo, handling pushback) · Chapter 25, §25.1 (the business analyst on a data team) · Chapters 36–39 (the lead-scoring project behind §76A.3) · Chapter 44 (the churn call list behind §76A.6) · Chapter 69 (the three answer tiers and the twelve extra-point moves).
>
> **Time needed:** 4–5 hours to read and drill every question aloud; 3–4 hours for the project (two five-line summaries, one defended metric, and rehearsed walkthroughs). Sections 76A.7 to 76A.10 are the situational half and are best drilled out loud with someone else reading the situation to you.
>
> **How this chapter is different from Chapters 70–75.** Those chapters test whether you *can do the work* (write SQL, debug pandas, reason about a p-value). This chapter tests whether you can *talk about the work you've done*, structure a project narrative, and demonstrate the specific judgment a DA or DS role requires beyond raw technical skill. Sections 76A.1 to 76A.6 are about work you have already finished; **sections 76A.7 to 76A.10 are about work that has just landed on you** — the Tuesday-morning situations that reveal whether someone has held the job or studied for it. Same format throughout: **"Remember it as…"** hooks, tier tables with extra points tagged by Chapter 69's moves (**[+Clarify]**, **[+Validate]**, **[+Limits]** and so on), and scan tables for rapid-fire.
>
> **Levels and roles.** Each question carries a level and the roles that usually ask it. **Fresher:** screening calls and first-job interviews. **Mid:** one to three years in the role. **Senior:** lead or specialist rounds. **DA** data analyst · **DS** data scientist · **BI** BI developer. Each **Learn it in** line names the section that teaches the skill; where a later bank drills it, a **Practise it with** pointer follows.

---

## 76A.1 What the two roles actually do, and how interviewers probe the line between them

### Q76A-001 · What's the actual difference between a Data Analyst and a Data Scientist, in a way that isn't just "DS does machine learning"?

**Level:** Fresher · **Roles:** DA, DS

**Remember it as:** *A Data Analyst answers questions that already exist. A Data Scientist often has to decide which question is even worth asking, and builds something that keeps answering it automatically.*

**Answer in one line:** A **Data Analyst** primarily investigates specific, often one-off business questions using existing data, producing reports, dashboards, and recommendations for human decision-makers; a **Data Scientist** more often builds systems (models, algorithms) that make or support decisions repeatedly and automatically, and spends more time on problem framing, experimentation, and statistical rigor before any model exists at all.

| Tier | What to say |
|---|---|
| Passes | "DA does reporting, DS does machine learning" (true often enough, misses the deeper distinction) |
| Strong | The one-off-question vs. repeatable-system distinction above, with a concrete example of each: a DA answering "why did Q3 sales drop in the East region" once, versus a DS building a churn model that scores every customer every day going forward |
| Extra points | + **[+Business]** the overlap is large and growing, especially at smaller companies where one person does both; naming that honestly, rather than presenting a rigid boundary, signals real experience over a textbook answer + **[+Edge cases]** a DA role at a company without a dedicated DS function often includes real modeling work, and a DS role at a data-mature company can be dominated by dashboarding and ad-hoc analysis, so the title alone doesn't fully predict the day-to-day |

**Likely follow-ups:** Which parts of your own experience map more to one role than the other? Where do you see yourself wanting to grow, toward more DA-style or more DS-style work?
**Red flag:** a rigid, textbook boundary with no acknowledgment of real-world overlap, or being unable to place your own experience on either side of it.
**Learn it in:** Chapter 7, §7.2 (the tracks and the ten roles this whole book is built around) and Chapter 25, §25.1 (the four-role table: BA, DA, DS, DE).

### Q76A-002 · An interviewer asks "why do you want this DA role and not a DS role, given your background touches both?" How do you answer honestly without talking yourself out of the job?

**Level:** Fresher · **Roles:** DA, DS

**Remember it as:** *This question is testing self-awareness and genuine fit, not loyalty. A specific, honest reason beats a generic "I love both equally."*

**Answer in one line:** Give a specific, honest reason tied to what you actually enjoy or want more of right now (closer to business stakeholders, faster feedback loops, breadth over depth, or the reverse for a DS answer), not a vague "I'm passionate about data" that could apply to either role equally.

**Worked example:**

> "I've done modeling work and enjoyed it, but what energizes me more day to day is the moment right after I hand someone an answer and watch them actually act on it, that feedback loop is faster and more visible in DA work than in a lot of DS work, where the payoff can be months away. That's a real, specific reason I'm choosing this role now, not a consolation prize."

| Tier | What to say |
|---|---|
| Passes | "I like both, but this role sounded interesting" (generic, doesn't actually answer why this one specifically) |
| Strong | The specific, honest framing above, tied to a real preference, not a rehearsed line |
| Extra points | + **[+Trade-offs]** naming a genuine trade-off (faster feedback vs. deeper technical depth) rather than pretending one role is strictly better shows the kind of self-aware judgment interviewers are actually screening for here |

**Likely follow-ups:** What would make you consider a DS role again in the future? What's one thing from DS work you'd want to bring into a DA role?
**Red flag:** an answer so generic it could be copy-pasted into an interview for the opposite role with no changes.
**Learn it in:** Chapter 8, §8.9 (pick your door, then learn backward) and Chapter 7, §7.8 (where you are right now).

### Rapid-fire, 76A.1

Roles: DA and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76A-003 | Where does a Data Analyst's work typically end and a Data Engineer's begin? | A DA typically works with data already made accessible (a warehouse, a clean table); a DE builds and maintains the pipelines that get it there in the first place | **[+Edge cases]** at a small company with no data engineer, the analyst often builds the first pipelines too; say so if that was you | Fresher · 7.2, 25.1 |
| Q76A-004 | Is "Business Intelligence Analyst" the same role as "Data Analyst"? | Largely overlapping: "BI analyst" is a common title for the role Chapter 7 calls the BI developer, leaning more heavily toward dashboards and reporting tools, while DA sometimes implies more ad-hoc, code-based analysis | **[+Business]** titles vary enormously by company; always check the actual JD's must-have list rather than assuming from the title alone | Fresher · 7.2, 8.5 |
| Q76A-005 | What's the most common reason a DA candidate is passed over for being "too DS," or vice versa? | Over-indexing the interview on technical depth (model internals, algorithm choice) when the role is really about stakeholder-facing analysis, or the reverse: under-demonstrating statistical rigor in a DS interview by staying purely descriptive | **[+Business]** matching your answer's depth and focus to the actual role, not just showcasing everything you know, is itself part of what's being evaluated | Mid · 8.3, 8.5 |
| Q76A-006 | Does a Data Scientist need to know SQL as well as a Data Analyst does? | Yes, in almost every real DS role; the depth of Python/ML skill differs sharply between the two roles, but SQL fluency is close to a shared baseline | **[+Evidence]** name one real query you wrote to build a model's training table (a join and a date cut-off), not just "I know SQL" | Fresher · 7.2; Ch 12–13 (practise: Ch 71) |

---

## 76A.2 Walking through a Data Analyst project, end to end

### Q76A-007 · "Walk me through a data analysis project you're proud of." Give a strong, structured answer

**Level:** Mid · **Roles:** DA

**Remember it as:** *Business question first, method second, impact last, and the impact needs a number, even a rough one.*

**Answer in one line:** Structure the narrative as: the business question and why it mattered, what data and method you used (briefly, not a code walkthrough unless asked), what you found, and critically, what changed as a result, ideally with a quantified impact.

**Worked example:**

> "Riverstone's sales team was manually pulling lead data weekly to decide who to call, taking about three hours every Monday. I built a prioritized call list instead: I pulled two years of closed leads and worked out the win rate for each lead source and company size. The gaps were large: referral leads were won about 19% of the time and marketplace leads about 3%, and bigger companies won more often too. So I built a simple scoring rule the sales lead could act on without needing a model explained to them: call referral, trade-fair and partner leads first. It cut their weekly prep time from three hours to about twenty minutes, and conversion on the leads called first rose from about 7% to about 12%, against the same number of leads called first under the old first-come-first-served order. The part I'm most proud of isn't the analysis itself, it's that I checked back a month later and it was still being used daily, which isn't always true of analysis work."

| Tier | What to say |
|---|---|
| Passes | Names the business problem and the method, but the impact is vague ("it helped the team"), with no number |
| Strong | The business-question-first, quantified-impact structure above |
| Extra points | + **[+Business]** the closing line, "I checked back a month later," directly answers the unspoken follow-up every interviewer wants to ask but often doesn't: did this actually stick, or was it a one-time deliverable nobody used again + **[+Validate]** the specific before/after numbers (three hours to twenty minutes, 7% to 12%) give the interviewer something concrete to probe further, rather than a vague "it really helped" |

**Likely follow-ups:** What would you do differently if you started this project again today? What was the hardest part, and how did you get past it?
**Red flag:** a project narrative that never states a business impact, or states one with no number attached at all.
**Learn it in:** Chapter 24, §24.4–24.6 (bottom line up front, one message per slide, the one-page memo); Chapter 27, §27.10 (telling the story, in two minutes and in ten); Chapter 36, §36.10 (the "referrals first" rule; its exercise 5 works out the win rate by source). **Practise it with:** Chapter 69, §69.4 (one question, all three tiers).

### Rapid-fire, 76A.2

Roles: DA and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76A-008 | An interviewer asks "what was the hardest technical challenge in that project?" What are they actually testing? | Whether you can go one level deeper than the polished summary, showing real problem-solving under a specific constraint, not just reciting the project again | **[+Business]** have one specific, technical sticking point ready for every project in your portfolio, not just the smooth headline version | Mid · 27.10 |
| Q76A-009 | How would you handle being asked to present the same project to a technical panel and then to a business stakeholder, back to back? | Keep the core findings identical; adjust the depth of method explanation and vocabulary for each audience, exactly Chapter 24's storytelling discipline | **[+Signpost]** tell each audience at the start what you'll cover and how long it will take, then keep to it | Mid · 24.4–24.7 |
| Q76A-010 | What if your proudest project doesn't have a clean, positive outcome to report? | Report it honestly, including what you learned from a result that didn't pan out; a thoughtful account of a project that taught you something is often more convincing than a suspiciously perfect success story | **[+Limits]** interviewers are often more interested in how you handle an ambiguous or negative result than in a flawless win | Fresher · 27.8 |
| Q76A-011 | Should you mention tools and technologies by name in a project walkthrough, or focus purely on the business story? | Both, but in order: lead with the business story, mention tools briefly and naturally as part of the "how," not as a checklist recited up front | **[+Business]** a walkthrough that opens with a tool list ("I used Python, pandas, and Tableau") before explaining what problem it solved reads as technical-first, not business-first | Fresher · 27.10 |

---

## 76A.3 Walking through a Data Science project, end to end

### Q76A-012 · "Walk me through an ML project you've built." Give a strong, structured answer

**Level:** Senior · **Roles:** DS

**Remember it as:** *Problem framing and evaluation choice matter as much as the model itself. A DS project narrative that jumps straight to "I used gradient boosting" skips the parts that actually show judgment.*

**Answer in one line:** Structure the narrative as: the business problem and why it needed a model (not just a rule or a report), how the target and evaluation metric were chosen and why, what approach was tried and what it was compared against, and what happened once it was in front of real users or real data, including any honest limitation.

**Worked example:** the same lead problem as Q76A-007, one step further. The analyst's rule became the baseline the model had to beat.

> "The business problem was deciding which leads the inside sales desk should call first. The team already called referral, trade-fair and partner leads first, and the question was whether a model could do better than that rule. I framed it as binary classification: won within 90 days, predicted 24 hours after the lead arrives, using only what's in the CRM by then. Logistic regression beat the rule clearly: on the untouched test set it scored 0.838 AUC against the rule's 0.727. Then I tried tuned gradient boosting, to see whether the extra complexity earned its keep. It didn't: boosting scored 0.830 on the same test set, and logistic had the better log loss, so I kept the simpler, better-calibrated model. Then I set the call threshold by cost, not at 0.5: working a lead costs about ₹1,500, and a won lead is worth about ₹30,000 in first-year margin, so any lead with better than about a 5% chance of winning is worth a call. The honest limitation: it's a static model, so a shift in the lead mix between retrainings wouldn't be caught automatically; that monitoring is the next thing I'd build."

| Tier | What to say |
|---|---|
| Passes | Explains the problem and the model and gives an AUC, but no baseline and no link from the metric to a business decision |
| Strong | The full structure above: framing, baseline-vs-complex comparison, evaluation choice tied to real cost, and an honest limitation |
| Extra points | + **[+Business]** naming the cost-based threshold as the thing that turned a score into a call list, not the raw AUC, shows the exact judgment a DS interview is probing for: knowing that a good metric and a useful model aren't automatically the same thing + **[+Trade-offs]** *reporting that the complex model lost*, and keeping the simpler one, is itself the strongest signal of judgment + **[+Limits]** volunteering a real limitation (a static model with no drift check) unprompted, rather than waiting to be asked, signals honest self-assessment instead of oversell |

**Likely follow-ups:** How would you detect the model going stale between retrainings? (Drift monitoring: Chapter 56, §56.8.) Why do you think boosting didn't win here? (Chapter 37, §37.12: the signal is mostly additive, and there were only 576 wins in training.)
**Red flag:** a project narrative dominated by algorithm names with no mention of why that algorithm, what it was compared against, or how success was actually measured.
**Learn it in:** Chapter 36, §36.1 (framing: the 90-day target and the prediction moment) and §36.10 (baselines, and the rule's 0.727); Chapter 37, §37.12 (lead scoring, baseline vs boosting); Chapter 39, §39.5 (choosing the threshold by business cost). **Practise it with:** Chapter 74, §74.7 (ML case studies).

### Rapid-fire, 76A.3

Roles: DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76A-013 | "What would you do if you had ten times more data for this project?" What's this really testing? | Whether you understand what's actually limiting your current model, more data helps most with variance/overfitting problems, not with a fundamentally wrong feature set or framing | **[+Clarify]** ask whether "more data" means more rows or more columns: more rows help a model that overfits; only new information helps a model that's missing signal | Senior · 37.10 (practise: Q74-001) |
| Q76A-014 | How do you decide when a DS project is "done" versus needing more iteration? | When the marginal improvement from further work no longer justifies its cost against the business need, not when the model can't technically be improved any further at all | **[+Business]** "done" is a business judgment call as much as a technical one; naming that explicitly is itself a strong answer | Senior · 39.5, 44.6 |
| Q76A-015 | An interviewer asks you to defend a modeling choice you'd actually reconsider today. How do you answer honestly? | Say so directly: explain the original reasoning, then state plainly what you'd do differently now and why, rather than defending a choice you no longer believe in | **[+Limits]** say what changed your mind (a later result, a problem you missed), so the change reads as learning, not guessing | Mid · 69.3 (Move 10) |
| Q76A-016 | Should a DS candidate be able to explain their model to a non-technical stakeholder, or is that a DA-specific skill? | It's expected of both: a DS who can't translate model output into a decision a business person can act on is significantly less valuable regardless of model quality | **[+Business]** end the explanation with the decision it supports ("so this account goes on Monday's call list"), not with the score | Mid · 39.8, 44.5 |

---

## 76A.4 Stakeholder communication for DA and DS specifically

### Q76A-017 · A stakeholder asks you to make a dashboard "simpler" with no further detail. As a DA, how do you respond, live?

**Level:** Mid · **Roles:** DA, BI

**Remember it as:** *"Simpler" almost always means "I can't find the thing I actually need," not "there's too much visual complexity."*

**Answer in one line:** Ask what they're specifically trying to find or decide when they open it, since "simpler" is usually a proxy for "I can't quickly find what I need," a findability problem, not necessarily a raw information-density problem.

**Worked example:**

> "I'd ask: 'When you say simpler, is it that there's too much on the page, or that it's hard to find the one number you actually check first?' Those need very different fixes. If it's the second, reorganizing what's prominent versus what's secondary might solve it without removing any real information at all."

| Tier | What to say |
|---|---|
| Passes | Asks one question, then removes the least-used charts |
| Strong | The diagnostic question above, distinguishing a findability problem from a genuine information-overload one |
| Extra points | + **[+Clarify]** one specific question ("too much on the page, or can't find the number you check first?") before touching the dashboard, the same instinct Chapter 76B's Q76B-001 applies to "make the report better": a vague complaint needs one specific clarifying question before any change is made |

**Likely follow-ups:** What if simplifying for this stakeholder makes the dashboard worse for a different stakeholder who uses the same one?
**Red flag:** treating "simpler" as a literal instruction to delete content, with no diagnosis of the real underlying complaint.
**Learn it in:** Chapter 24, §24.1 (turning an ask into a question); Chapter 25, §25.3 (from a vague ask to a written requirement); Chapter 15, §15.2 (start from the question); Chapter 16, §16.7 (designing the report page). **Practise it with:** Chapter 76B, Q76B-001, and Chapter 70, §70.8 (Q70-069/070, dashboard critiques).

### Rapid-fire, 76A.4

Roles: DA and DS, except where a row names one.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76A-018 | A DS candidate is asked to explain a model's prediction to someone who's never heard of a p-value. What's the winning move? (DS) | Skip statistical vocabulary entirely; explain in terms of the specific factors driving *this* prediction, using SHAP-style "this account scored high risk because of X and Y," concrete and case-specific | **[+Simple first]** one plain sentence first, then the two or three factors, and numbers only if they ask | Mid · 39.8, 44.5 |
| Q76A-019 | How would a DA and a DS each respond differently to "can you just change the number"? | The underlying discipline (diagnose before responding) is identical; a DA more often faces this on a reporting number, a DS more often faces a variant of it as "can you make the model say what we expect" | **[+Trade-offs]** offer an honest alternative they can accept, such as a clearly labelled different cut, or a note explaining the dip | Mid · 24.8 (practise: Q76B-033) |
| Q76A-020 | What's the risk of a DS presenting only the model's strongest result and omitting a weaker segment's performance? (DS) | It's a form of the same overclaiming problem Chapter 39 warns against; a stakeholder who later discovers the omitted weak segment loses trust in every future result, not just that one | **[+Limits]** put the weak segment in the summary yourself, with what you'd do about it | Senior · 39.9, 44.7 |
| Q76A-021 | How would you push back on a stakeholder who wants a specific chart type you think is misleading for their data? | Show, don't just tell: build the alternative chart alongside the requested one and let the clearer version make the case, rather than only arguing abstractly against the original request | **[+Trade-offs]** say what the requested chart does well before what it hides, so the stakeholder isn't made wrong in front of others | Mid · 15.2, 15.12, 16.7 (practise: 70.8, Q70-069/070) |

---

## 76A.5 Portfolio deep-dives and handling scrutiny

### Q76A-022 · An interviewer picks one number from your resume ("you say this raised conversion from 7% to 12%") and asks you to defend it in detail. What do they actually want?

**Level:** Senior · **Roles:** DA, DS

**Remember it as:** *A resume number is a claim. The interviewer is checking whether you actually understand how you measured it, not whether the number itself was impressive.*

**Answer in one line:** They want to know exactly how that number was measured (against what baseline, over what time period, with what confounders considered), since a candidate who can't explain their own headline metric in detail either didn't do the analysis rigorously or is inflating the claim.

**Worked example:** the resume line is "raised conversion on prioritized leads from 7% to 12%", from the project in Q76A-007.

> "That figure compares the leads we called first under the scoring rule with the same number of leads called first under the old first-come-first-served order, the quarter before. Comparing the top-scored leads with *all* leads would have flattered it, because top-ranked leads convert better by construction. I also checked conversion across all leads, not just the ones called first, and it rose too, so the gain wasn't just a reshuffle of who got called first. And I checked seasonality: the same quarter a year earlier was flat. What I can't rule out without a holdout is that the reps simply tried harder on the flagged list. The clean test would be to randomly keep half the reps on the old order for a month and compare."

| Tier | What to say |
|---|---|
| Passes | Can restate the number but can't explain the comparison baseline or any confounders considered |
| Strong | The full explanation above: the baseline, a like-for-like comparison, and at least one confound checked; and it says whether the change is in points or percent: 5 percentage points, about 71% relative (Chapter 4, §4.2) |
| Extra points | + **[+Validate]** naming the selection trap yourself (top-ranked leads would beat the average even if the ranking changed nothing) before the interviewer asks "but could it have been X instead," shows the rigor was applied before the metric was ever put on a resume |

**Likely follow-ups:** How would you know if that 5-point rise wasn't statistically significant, just noise? What would make you distrust your own number here?
**Red flag:** unable to state the exact baseline a resume metric was measured against, or visible defensiveness rather than genuine engagement with the scrutiny.
**Learn it in:** Chapter 4, §4.2 (percentage points and percent change); Chapter 22, §22.5 (correlation, causation, and confounders) and §22.7 (selection bias); Chapter 30, §30.8 (designing an experiment); Chapter 31, §31.2 (why the before-and-after comparison misleads). **Practise it with:** Chapter 69, §69.3 (Move 7, validate the result).

### Rapid-fire, 76A.5

Roles: DA and DS for every row.

| # | Question | One-line answer | Extra point | Level · learn it in |
|---|---|---|---|---|
| Q76A-023 | An interviewer finds a small inconsistency between two things you said about the same project. How do you handle it live? | Acknowledge it directly and clarify which version is accurate, rather than doubling down or getting flustered; a small, honestly-corrected inconsistency is far less damaging than visible defensiveness about it | **[+Limits]** say which version is right and why the other slipped ("earlier I gave the validation number; the test number is this one") | Fresher · 69.3 (Move 10) |
| Q76A-024 | What's the risk of over-preparing a polished, memorized project narrative? | It can sound rehearsed and brittle under a genuine follow-up question that deviates from the memorized script, revealing the narrative was recited rather than truly understood | **[+Business]** know the underlying facts cold; don't memorize the exact wording | Fresher · 27.10 |
| Q76A-025 | An interviewer asks about a project on your resume from three years ago, in specific detail. How do you handle gaps in your memory honestly? | Say plainly what you remember clearly and what's genuinely fuzzy after this long, rather than fabricating confident-sounding detail you don't actually have | Red flag: confidently inventing specifics for a memory gap is far more damaging if caught than an honest "I don't recall that exact detail, but here's what I do remember" | Fresher · 69.3 (Move 10) |
| Q76A-026 | Should you bring a laptop with your actual project code to an interview, in case you're asked to show it? | Generally yes if the interview is portfolio-focused and it's practical, but only code and data you own or that is public (portfolio projects, synthetic data). Never show an employer's code, data or dashboards without permission; say "I can't show that, but here's the same technique on public data" | **[+Business]** if you do, make sure it actually runs before the interview, nothing undercuts credibility faster than a live demo failing | Fresher · 27.9 |

---

## 76A.6 Full scenarios, talked through live

### Q76A-027 · Full scenario, talked through live: an interviewer says "your resume says you 'used machine learning to improve retention.' What does that actually mean?"

**Level:** Senior · **Roles:** DS

**What they're really testing:** whether a vague, resume-friendly phrase can be unpacked into the real, specific work behind it, live, without stalling.

**Talked through live, start to finish:**

> "Fair to push on that, it's a compressed phrase covering a few specific things. Concretely: I built a churn prediction model, gradient boosting, trained on one year of account activity, predicting whether an account places no order in the following year. The 'improve retention' part specifically means: I turned the scores into a monthly call list of 40 accounts for the sales team, ranked by expected margin at risk (churn probability × last year's revenue × margin) rather than probability alone, since a large account with a modest risk score is worth more attention than a small account with a high one. What I can't fully claim is that retention definitively improved *because of* the model; what I can say is the accounts on the list were called, and a good share of them didn't churn, but proving causation would need a proper holdout test I haven't run yet, and I'd say that honestly if asked."

**Extra-points moves demonstrated:** **[+Signpost]** unpacked the vague phrase into its specific, real components rather than restating it more confidently. **[+Business]** distinguished expected-value ranking from probability-alone ranking, exactly Chapter 44's own capstone lesson. **[+Limits]** stated the actual causal limitation honestly rather than overclaiming the resume phrase's implied certainty.

**Likely follow-ups:** How would you design that holdout test to actually prove causation? What would you change about how you'd phrase this on a resume, now that you've unpacked it?
**Red flag:** doubling down on the vague resume phrase instead of engaging with the specific unpacking the question is asking for.
**Learn it in:** Chapter 44, §44.3–44.4 (from probability to rupees, and the call list) and Chapter 30, §30.8 (designing the holdout test). **Practise it with:** Chapter 73, §73.4 (A/B test design).

---

## 76A.7 The analyst's Tuesday: requests as they actually arrive

The questions so far in this chapter are about work you have already done. These are about work that has just landed on you, and they are how an interviewer finds out whether you have held the job or only studied for it.

The pattern throughout: **the request as stated is rarely the request.** A candidate who answers the literal question has done the task. A candidate who finds the question underneath has done the job.

### Q76A-028 · "Can you just pull me a list of all our customers?"

**Level:** Fresher · **Roles:** DA, DS, BI

**Remember it as:** *"Just pull" is never just a pull. Nobody wants a list of 5,027 rows; they want to do something with it.*

**Answer in one line:** Ask **what they are going to do with it** before writing anything — because "all our customers" has at least four reasonable meanings and the right one depends entirely on the purpose, which takes one question to find out and hours to guess wrong.

The four meanings, all defensible, all different:

| They might mean | Which gives |
|---|---|
| Every row in the customers table | 5,027 |
| Everyone who has ever ordered | Fewer — some never did |
| Everyone who ordered this year | Fewer again |
| Everyone *currently active*, however the business defines that | A different number entirely, and nobody has defined it |

Hand over the wrong one and the work is wasted, except that you will not find out for three days.

**The question that resolves it is not "which do you mean?"** — they do not know, which is why they asked loosely. It is **"what are you going to do with the list?"** Because the answer tells you the definition:

- *"Send them a campaign"* → active, contactable, opted in, and you need email addresses, which changes the query entirely.
- *"Work out how many we have"* → they want a number, not a list, and you can answer in the chat window.
- *"Find the ones we have lost"* → they want an anti-join and the opposite of what they asked for.
- *"Give it to the sales team"* → it needs owner, region and last-order date, or it is useless to them.

Three more habits that turn a competent answer into a strong one.

**Ask when they need it**, because "today" and "this week" produce different work and it is unfair to both of you to guess.

**Confirm the shape before you build it.** "I'll send a CSV with customer id, name, city, last order date and total revenue — is that the right set of columns?" takes thirty seconds and prevents the second round.

**Say what you excluded, in writing, when you deliver.** "This is 4,812 customers: everyone with an order in the last 24 months, excluding the 215 marked as test accounts." That one sentence is what separates a data pull from an analysis, and it is what stops the number being quietly wrong in someone's deck next quarter.

| Tier | What to say |
|---|---|
| Passes | "I'd ask them to clarify which customers they mean" |
| Strong | + asks what they will *do* with it rather than which definition they want, and shows how the purpose determines the definition |
| Extra points | **[+Clarify]** "what will you do with it" beats "what do you mean", because they can answer the first · **[+Validate]** state the filters you applied when you deliver, so the number can be reproduced and challenged · **[+Business]** sometimes the honest answer is that they want a number, not a list, and you can give it immediately · **[+Edge cases]** test accounts, internal accounts and duplicates are in almost every customer table and almost never wanted |

**Likely follow-ups:** What if they say "just give me everything"? *(Give it, with the caveats written down — but ask once.)* How would you handle the same request from three people in a week? *(That is a dashboard, or a saved query.)* What if the list contains personal data?
**Red flag:** writing the query immediately. It is the most common junior mistake and the most expensive.
**Learn it in:** Chapter 24, section 24.2 (eliciting a requirement); Chapter 12, section 12.10 (the anti-join).

### Q76A-029 · Finance says revenue is ₹4.21 crore. Your query says ₹4.34 crore. Who is wrong?

**Level:** Mid · **Roles:** DA, DS, BI

**Remember it as:** *Neither, usually. Two correct numbers from two different definitions. Find the definition before you defend the number.*

**Answer in one line:** **Probably neither of you** — a gap of about 3% between two revenue figures is almost always a definitional difference rather than an error, and the job is to find *which* definition differs, not to prove your query right.

The move is to stop arguing about the total and start comparing the parts. Reconcile from one end to the other:

| Likely cause | How to check |
|---|---|
| **Cancellations** — do they include cancelled orders? | Riverstone's own data: 2 of 175 orders are cancelled, 1.14% |
| **Returns**, netted off or not | Is there a returns table nobody mentioned? |
| **Tax** — gross or net of GST | A 5–18% gap is usually this |
| **Discounts** — list price or realised | `discount_pct` is in the line, not the header |
| **Date boundary** — order date, ship date, or invoice date | A month-end order shipped in the next month sits in different months for each |
| **Currency or rounding** | Rare, but it compounds |
| **Scope** — one entity, one region, one channel? | The easiest to miss and the biggest |

**Then do the arithmetic that proves it.** Take the difference — ₹13 lakh — and find a cut of the data that equals it. If cancelled orders in the period total ₹13 lakh, you have your answer in one query and nobody needs to be wrong.

Three things about *how* to handle it, which is really what is being tested.

**Assume you are the one who is wrong**, out loud. Finance has been producing this number monthly for years and it goes to the board. You wrote your query on Tuesday. That is not deference, it is base rates.

**Never present a number that contradicts an official one without reconciling it first.** Walking into a meeting with a different figure and no explanation damages trust in you, not in them, and the damage outlasts the meeting.

**Write the definition down when you have found it**, and put it where the next person will see it. This same gap will reappear in six months with a different pair of people, and the only thing that stops it is a written definition attached to the metric.

| Tier | What to say |
|---|---|
| Passes | "I'd check my query" |
| Strong | + assumes a definitional difference first, lists the usual suspects, and reconciles by finding a cut that equals the gap |
| Extra points | **[+Business]** Finance's number is the official one; yours is a hypothesis until reconciled · **[+Validate]** finding a subset whose total equals the difference turns an argument into a finding · **[+Clarify]** ask what they include before showing your figure, not after · **[+Edge cases]** the date boundary is the most common cause and the least suspected |

**Likely follow-ups:** What if you genuinely are right and Finance is wrong? *(Show the reconciliation privately first, and let them correct it.)* How would you prevent it recurring? *(A documented, single definition — Chapter 77, Q77-004.)* What if the gap is 40%, not 3%?
**Learn it in:** Chapter 23, section 23.3 (revenue definitions); Chapter 24, section 24.7 (handling pushback).

### Q76A-030 · You have four requests and time for two. How do you choose?

**Level:** Mid · **Roles:** DA, DS, BI

**Remember it as:** *Rank by the decision each one changes, not by who shouted. Then tell everyone where they are, including the two who lost.*

**Answer in one line:** Rank by **what decision each piece of work changes and when that decision is made** — a report nobody will act on until next quarter loses to a number a pricing decision needs on Thursday, whoever asked for which — and then tell all four people where they sit, because the communication matters more than the ordering.

Four questions that order almost any queue:

1. **What decision does this change?** If none, it goes last, and that is worth saying kindly.
2. **When is that decision made?** Work needed Thursday beats better work needed next month.
3. **What does it cost if it is late?** A regulatory filing and a curiosity are different.
4. **How long will it actually take?** A twenty-minute answer that unblocks someone should usually jump the queue regardless of rank.

That fourth one is the practical move most people miss. If request three is twenty minutes, do it first — not because it is important but because the queue gets shorter and a stakeholder stops waiting.

**Then the part that is actually being tested: what you say to the two who did not make it.** Silence is what makes people escalate. "I can get to this on Thursday — if it needs to be sooner, tell me what it would displace" does three things at once: it gives a date, it treats them as an adult, and it hands the prioritisation conflict to the people who should own it rather than carrying it yourself.

**And escalate rather than quietly dropping something.** If two genuinely cannot wait, that is your manager's decision, not yours. Bringing it to them with the trade-off already laid out is the senior version; going silent and missing both is the junior one.

| Tier | What to say |
|---|---|
| Passes | "I'd ask my manager to prioritise" |
| Strong | + the decision-and-deadline test, and does the quick one first because it shortens the queue |
| Extra points | **[+Business]** a request nobody will act on is worth saying no to, politely and once · **[+Clarify]** "what would this displace" hands the conflict to the people who own it · **[+Validate]** telling the losers a date is what prevents escalation · **[+Edge cases]** a recurring request is a signal to automate it rather than reprioritise it every week (Chapter 78, Q78-005) |

**Likely follow-ups:** What if the loudest stakeholder is the most senior? What if everything is "urgent"? *(Then nothing is, and that is the conversation to have with your manager.)* How do you handle the fourth repeat of the same request?
**Learn it in:** Chapter 24, section 24.3 (scoping); Chapter 26, section 26.9.

### Q76A-031 · The dashboard you built is not being used. What do you do?

**Level:** Mid · **Roles:** DA, BI

**Remember it as:** *A dashboard nobody opens is not a communication failure. It answered a question nobody was asking.*

**Answer in one line:** **Go and watch someone try to use it**, because the cause is almost never what you would guess from your desk — and the most common finding is that it answers a question they do not have, which is a scoping failure rather than a design one.

The order to investigate, cheapest first:

**1. Check whether it is true.** Most BI tools log views. "Nobody uses it" sometimes means one person stopped.

**2. Ask three users to open it while you watch.** Not "do you find it useful" — they will be polite. Watch where they hesitate, what they export, and what they do *next* in another tool. The thing they export to Excel is the thing the dashboard should have given them (Chapter 69A, Q69A-016).

**3. Then look for the usual causes**, in rough order of frequency:

| Cause | The tell |
|---|---|
| **It answers the wrong question** | They look at one tile and leave |
| They do not trust the numbers | They cross-check against their own sheet |
| It is too slow | They open it, wait, and close it |
| They cannot find it | It is not where they already work |
| It needs a login they do not have | They never got past the first screen |
| The old spreadsheet still exists | They use that instead, because it still works |

That last one is the most under-rated. **A new dashboard competes with whatever it was meant to replace**, and if the old thing still runs, people use the thing they trust. Switching off the old report is often the entire adoption strategy.

**Be willing to conclude it should not exist.** If the question it answers is not a question anyone has, the right outcome is to retire it rather than redesign it, and saying so is a stronger answer than promising to add filters.

| Tier | What to say |
|---|---|
| Passes | "I'd ask for feedback" |
| Strong | + watches people use it rather than asking, and names "it answers the wrong question" as the likeliest cause |
| Extra points | **[+Validate]** usage logs first; "nobody uses it" is often one person · **[+Business]** what they export to Excel tells you what they actually needed · **[+Edge cases]** the old report still existing is a complete explanation on its own · **[+Clarify]** be prepared to retire it; not every dashboard should be rescued |

**Likely follow-ups:** How would you have prevented this at the start? *(Agree the decision it supports before building — Chapter 75, Q75-013.)* How do you measure dashboard success? What if the sponsor insists it is fine?
**Learn it in:** Chapter 16, section 16.9 (dashboard design); Chapter 75, Q75-013.

### Rapid-fire, 76A.7: the analyst's week

Roles: DA, DS and BI for every row unless stated.

| # | Situation | What you do | Extra point |
|---|---|---|---|
| Q76A-032 | A request arrives with no deadline | Ask for one. "When do you need it" is not pushy; it is how you avoid doing it twice | **[+Clarify]** no deadline often means no decision → Ch 24 §24.3 |
| Q76A-033 | The request says "quick question" and is not | Say so, kindly, with an estimate: "that is about a day — shall I start it?" | **[+Business]** silently absorbing scope is how analysts get overloaded invisibly → Q76A-030 |
| Q76A-034 | You are asked for a number you know is misleading | Give it with the caveat attached, in the same message. Refusing looks obstructive; giving it bare is worse | **[+Validate]** put the caveat above the number, not in a footnote → Ch 24 §24.5 |
| Q76A-035 | Halfway through, you realise the data cannot answer the question | Say so immediately, not at the deadline. Offer what it *can* answer | **[+Business]** early bad news is a service; late bad news is a failure → Ch 24 §24.7 |
| Q76A-036 | Someone asks you to re-run last month's report with one tweak | Do it, then ask whether this will recur. Twice is a pattern; three times is a job for automation | **[+Scale]** frequency times time saved against build cost → Ch 78 Q78-005 |
| Q76A-037 | Your query is slow and the stakeholder is waiting | Send the partial answer with the caveat, keep optimising. Do not make them wait in silence | **[+Clarify]** "here is the shape, exact numbers in an hour" is usually enough to unblock → Ch 28 §28.5 |
| Q76A-038 | You find a bug in a report that has been wrong for months | Tell someone today, with the size of the error and who saw it. The delay is what becomes the problem | **[+Business]** quantify the impact before you report it, so the conversation is about the fix → Ch 47 §47.4 |
| Q76A-039 | A stakeholder asks for a metric that does not exist yet | Define it with them in writing before building it, including the edge cases | **[+Validate]** a metric without a written definition is two metrics → Ch 75 Q75-045 |
| Q76A-040 | You are asked to analyse something you think is the wrong question | Do the analysis, and add the question you think they should have asked | **[+Trade-offs]** answering only your own question is arrogant; answering only theirs is passive → Ch 24 §24.7 |
| Q76A-041 | The data has a gap — a month missing entirely | Flag it before analysing, and say what it does to the conclusion. Do not interpolate silently | **[+Validate]** a chart with a silent gap filled in is a lie told with a line → Ch 15 §15.6 |
| Q76A-042 | Two stakeholders want contradictory definitions of the same metric | Give both, named differently, and escalate the choice. Do not pick for them | **[+Business]** one word of naming prevents a year of confusion → Ch 23 §23.2 |
| Q76A-043 | You are asked to "make the chart look better" | Ask what decision it supports. Usually the fix is fewer things, not prettier ones | **[+Clarify]** "better" means "I cannot see the point of it" → Ch 15 §15.2 |
| Q76A-044 | A one-off analysis gets referenced in a board deck | Harden it: name the source, pin the date, write the definition, and say it is a point-in-time figure | **[+Business]** one-off numbers become permanent the moment they are quoted → Ch 20 §20.7 |
| Q76A-045 | Someone outside the team asks for direct database access | Find out what they need. Usually it is one report, not access, and access is hard to take back | **[+Business]** least privilege, and a view rather than a login → Ch 64 §64.3 |

---

## 76A.8 The data scientist's Tuesday

The same shape, with the problems that come from the work being probabilistic rather than exact.

### Q76A-046 · When do you stop improving a model?

**Level:** Mid · **Roles:** DS, MLE

**Remember it as:** *When the next point of accuracy is worth less than what it costs to get, or changes no decision. Both of those are business questions, not modelling ones.*

**Answer in one line:** When the improvement **stops changing a decision** or **costs more than it returns** — and the honest answer names the point before you started modelling, because deciding when to stop afterwards is how projects run for months.

Four stopping conditions, and a good answer names at least two:

**1. The decision stops moving.** If the retention team can call 200 customers a month, a model that ranks the top 200 better is valuable and a model that ranks positions 900 to 1,100 better is not. The business constraint sets the precision you need.

**2. The gain is inside the noise.** An improvement from 0.842 to 0.847 AUC on one test split is probably nothing (Chapter 74, Q74-052). If repeated cross-validation cannot distinguish the two models, you have not improved anything.

**3. The next gain costs more than it returns.** Three weeks of work for half a point, on a model whose errors cost a few thousand rupees a month, is not a trade worth making — and saying so out loud is the senior move.

**4. You have hit the ceiling of the data.** Sometimes the signal is not there. More features will not fix a target nobody has defined consistently.

**The move that marks experience: set the threshold before you start.** "We will ship if it beats the current rule by five points of recall at the same precision" turns an endless project into a finite one, and it is the thing almost nobody does.

And **the baseline is the other half** of the answer. A model is finished when it beats the simple rule by enough to be worth maintaining — not when it stops getting better. A model that cannot beat `no order in 90 days` is finished too, in the other direction (Chapter 69A, Q69A-041).

| Tier | What to say |
|---|---|
| Passes | "When the improvements get small" |
| Strong | + ties stopping to the decision and the cost, and names setting the threshold in advance |
| Extra points | **[+Business]** the business constraint — how many customers can actually be called — sets the precision you need · **[+Validate]** a gain inside cross-validation noise is not a gain (Chapter 74, Q74-052) · **[+Scale]** a model is a system to maintain, so a marginal gain carries a permanent cost · **[+Edge cases]** sometimes the right answer is that the data cannot support the question |

**Likely follow-ups:** How would you know if the gain was noise? What if the business keeps asking for more accuracy? How does this change for a model already in production?
**Learn it in:** Chapter 39 (evaluation and honesty); Chapter 74, section 74.1.

### Q76A-047 · Explain your model to someone who will not understand the algorithm

**Level:** Mid · **Roles:** DS, MLE, DA

**Remember it as:** *They do not need to know how it works. They need to know what it does, how often it is wrong, and what it will cost them when it is.*

**Answer in one line:** Explain **what it predicts, what it gets right, how it is wrong, and what decision it should change** — and say nothing about the algorithm unless asked, because the algorithm is the one part that does not affect their decision.

The four things to say, in this order:

**1. What it does, in their words.** "It ranks accounts by how likely they are to stop ordering in the next quarter." Not "a gradient-boosted classifier on 40 features."

**2. How good it is, in their units.** Not AUC. "If you call the top 200 accounts it flags, about 60 of them would have left. Calling 200 at random would have found about 12." That is the same information as a lift chart, in a sentence a sales director can act on.

**3. How it is wrong, specifically.** "It misses about a third of the accounts that do leave, and about 70% of the ones it flags would have stayed anyway. So it is a prioritisation tool, not a verdict." Saying this *first*, before being asked, is what builds trust — and it pre-empts the moment someone finds a wrong prediction and concludes the whole thing is useless.

**4. What should change because of it.** "Work the list top-down instead of alphabetically." If nothing changes, the model should not ship (Chapter 69A, Q69A-041).

**Two things to avoid.** Do not reach for an analogy about how the algorithm works — nobody needs the decision-tree-as-flowchart picture, and it invites questions about the mechanism instead of the use. And do not oversell: "85% accurate" on an imbalanced problem is both true and misleading (Chapter 74, Q74-007), and when someone works that out you lose the model and your credibility together.

| Tier | What to say |
|---|---|
| Passes | "I'd avoid technical jargon" |
| Strong | + the four-part structure, with performance expressed as lift over doing nothing rather than as a metric |
| Extra points | **[+Business]** "60 of 200 against 12 at random" is a lift chart in one sentence · **[+Validate]** describing the errors before being asked is what makes the model survive its first visible mistake · **[+Edge cases]** quoting accuracy on an imbalanced problem is technically true and will be found out · **[+Clarify]** ask what they will do with the output, and shape the explanation around that |

**Likely follow-ups:** How would you explain a false positive to them? What if they ask why a specific customer was flagged? *(SHAP, or the honest "this model does not explain individual cases well.")* What if they want certainty?
**Learn it in:** Chapter 39, section 39.6 (interpretation); Chapter 24, section 24.5 (the memo).

### Rapid-fire, 76A.8: the data scientist's week

Roles: DS and MLE for every row unless stated.

| # | Situation | What you do | Extra point |
|---|---|---|---|
| Q76A-048 | A stakeholder asks for "the probability this customer churns" | Give the ranking, not the probability, unless the model is calibrated. Most are not | **[+Validate]** good AUC does not mean good probabilities → Ch 74 Q74-039 |
| Q76A-049 | Your model is worse in production than in testing | Check leakage, drift and training-serving skew, in that order. Leakage is the most common and the most embarrassing | **[+Validate]** the permuted-target check proves the pipeline → Ch 74 Q74-043 |
| Q76A-050 | A stakeholder wants the model to predict something you have no labels for | Say so plainly. No labels, no supervised model — and defining the label is the real project | **[+Business]** most "we want to predict X" conversations should end here → Ch 69A Q69A-041 |
| Q76A-051 | Asked to explain why one specific prediction was made | SHAP or a surrogate, with the caveat that a per-case explanation from a complex model is approximate | **[+Edge cases]** if per-case explanation is a requirement, use a model that gives it → Ch 39 §39.6 |
| Q76A-052 | The model is accurate but the business ignores it | The project failed. Find out what would have to be true for them to act | **[+Business]** adoption is part of the work, not someone else's job → Q76A-047 |
| Q76A-053 | Asked to re-run an analysis from six months ago | Can you? Pinned data, pinned seed, pinned versions. If not, say so and fix it going forward | **[+Validate]** reproducibility is a property you build in, not find later → Ch 72 Q72-089 |
| Q76A-054 | Someone asks if the result is statistically significant | Ask what decision it supports, then answer with the effect size and interval as well as the p-value | **[+Business]** significance without effect size is not a decision → Ch 73 §73.3 |
| Q76A-055 | Your A/B test is inconclusive | That is a result. Report the interval and what it rules out, rather than calling it a failure | **[+Validate]** "no difference detected, and we could have detected 5%" is informative → Ch 73 Q73-040 |
| Q76A-056 | A model needs retraining and nobody owns it | Raise it as a risk with a date. An unowned model in production degrades quietly | **[+Scale]** model ownership is a staffing question, not a technical one → Ch 79 Q79-031 |
| Q76A-057 | You are asked to use a technique you have not used before | Say so, say what you would do to get competent, and name the simpler thing you would try first | **[+Trade-offs]** honesty plus a plan beats bluffing, and interviewers test for it → Ch 76A Q76A-023 |

---

## 76A.9 Working with everyone else

### Q76A-058 · Engineering says your query is slowing down the production database

**Level:** Mid · **Roles:** DA, DS, DE

**Remember it as:** *They are right. Stop the query first, apologise second, and fix the access pattern third — not the other way round.*

**Answer in one line:** Stop running it, immediately and without arguing — then work out whether the fix is a better query, a replica, or a warehouse, because an analyst's query competing with the application that customers use is a problem you caused and can prevent permanently.

The order matters and is most of what is being tested.

**First, stop.** Not "let me check whether it is really mine." If there is doubt, stop anyway and find out after. A slow application is costing money while you investigate.

**Second, take it.** "Sorry, that is mine" costs nothing and buys a great deal. Analysts who argue with engineering about whether their query was really the cause get access removed.

**Third, fix the pattern, not the instance.** The query was a symptom; the cause is an analyst running analytical workloads against a transactional database (Chapter 69A, Q69A-025). The options, cheapest first:

| Fix | When it is the right one |
|---|---|
| Write a better query | It was genuinely a bad query — missing index, `SELECT *`, a cartesian join |
| Run it off-hours | One-off, large, and not urgent |
| **A read replica** | You need current data regularly. The usual answer |
| **A warehouse** | Analysis is a continuing need, which it always turns out to be |

**And ask for a guardrail**, which is the senior move: a statement timeout on your account, so the next mistake stops itself. Asking to be constrained is unusual and it is the thing that gets your access kept.

| Tier | What to say |
|---|---|
| Passes | "I'd optimise the query" |
| Strong | + stops it first, accepts it without arguing, and separates the instance from the access pattern |
| Extra points | **[+Business]** a slow application costs money per minute, which is why investigating before stopping is the wrong order · **[+Scale]** the real fix is a replica or a warehouse; the query was the symptom · **[+Validate]** ask for a statement timeout on your own account · **[+Edge cases]** `EXPLAIN` before running anything large against shared infrastructure (Chapter 28, section 28.5) |

**Likely follow-ups:** How would you have known in advance? What is a read replica, and what does it not solve? *(Chapter 69A, Q69A-031.)* What would you ask for if a replica is refused?
**Learn it in:** Chapter 28, section 28.5 (query plans); Chapter 49, section 49.1.

### Rapid-fire, 76A.9: the rest of the company

| # | Situation | What you do | Extra point |
|---|---|---|---|
| Q76A-059 | Product wants a number for a launch deck, today | Give it with the confidence you actually have, and say what would make it firmer | **[+Business]** a caveated number today beats a perfect one next week → Ch 24 §24.5 |
| Q76A-060 | Engineering changed a column name and your pipeline broke | Fix it, then ask to be told next time — a data contract, or at minimum a Slack channel | **[+Business]** this is schema drift, and the fix is process not code → Ch 77 Q77-009 |
| Q76A-061 | Finance wants the report in their format, not yours | Give it in their format. The format is their requirement; the processing is yours | **[+Clarify]** ask what they do with it after opening → Ch 69A Q69A-016 |
| Q76A-062 | Marketing asks you to prove a campaign worked | Ask what the counterfactual is. Without one you can describe, not prove | **[+Validate]** a holdout group decided in advance is the whole answer → Ch 30 §30.2 |
| Q76A-063 | A senior leader quotes your number back to you, wrong | Correct it privately and immediately, with the right figure and its source | **[+Business]** a wrong number repeated twice becomes the official one → Ch 24 §24.7 |
| Q76A-064 | You are the only data person and everyone asks you directly | Create one intake route and publish it. A queue you can see is the first step to prioritising it | **[+Scale]** also makes your workload visible when you ask for help → Q76A-030 |
| Q76A-065 | A team builds their own spreadsheet because yours was slow | Find out what they needed. They have told you a requirement by building it | **[+Business]** shadow reporting is feedback, not disobedience → Q76A-031 |
| Q76A-066 | Legal asks whether you can use a dataset | Do not guess. Ask, and record the answer where the next person will find it | **[+Edge cases]** personal data has rules that differ by jurisdiction → Ch 64 §64.2 |

---

## 76A.10 What changes as you get senior

### Q76A-067 · What is the difference between a mid-level and a senior analyst?

**Level:** Senior · **Roles:** DA, DS, BI, MLE

**Remember it as:** *Not harder SQL. A senior person changes what gets asked, not just what gets answered.*

**Answer in one line:** A mid-level analyst answers the question well; a **senior analyst changes the question, owns the definition, and is trusted without checking** — the technical gap between the two is far smaller than most candidates assume, and saying so is itself a senior answer.

What actually changes, and none of it is syntax:

| | Mid-level | Senior |
|---|---|---|
| The question | Answers it well | Works out whether it is the right one |
| Scope | Given | Negotiated |
| Trust | Work is reviewed | Work is relied on |
| Failure | Fixes their own | Prevents the class of it for everyone |
| Others | Works alongside | Makes the people around them better |
| Ambiguity | Asks what to do | Decides, and says what they decided |

**The clearest single marker is ambiguity.** Given a vague request, a mid-level analyst asks for clarification — which is correct. A senior analyst makes a reasonable call, states the assumption out loud, and carries on: *"I have assumed active means ordered in the last 90 days; tell me if that is wrong."* That sentence is worth more than any technical skill in the comparison, because it removes work from everyone else rather than adding it.

**The under-rated one is preventing a class of error.** A mid-level analyst finds the revenue discrepancy and fixes it. A senior analyst writes the definition down, puts it where the metric is used, and the discrepancy stops happening to other people too.

**And the honest part:** seniority is partly about having been wrong enough times to recognise the shapes. Someone who has shipped a report that was quietly wrong for three months checks differently afterwards. That is not a thing you can study for, and acknowledging it in an interview reads as experience rather than modesty.

| Tier | What to say |
|---|---|
| Passes | "Seniors handle more complex work" |
| Strong | + changing the question rather than answering it, owning definitions, and operating under ambiguity by deciding and stating the assumption |
| Extra points | **[+Business]** preventing a class of error, not just fixing an instance, is the clearest marker · **[+Clarify]** "I have assumed X, tell me if that is wrong" is the single most senior sentence in the job · **[+Trade-offs]** the technical gap is smaller than candidates expect, and saying so is itself a senior answer · **[+Edge cases]** seniority partly comes from having been wrong in ways you now check for |

**Likely follow-ups:** What would you need to do to reach the next level? Give an example of changing the question. How do you make the people around you better?
**Learn it in:** Chapter 9 (how expertise forms); Chapter 80, section 80.5 (influence without authority).

### Rapid-fire, 76A.10: seniority

| # | Question | The answer | Extra point |
|---|---|---|---|
| Q76A-068 | "Where do you see yourself in five years?" for a data role | Answer with the kind of problems you want, not a title. Titles differ by company; problems do not | **[+Business]** naming a direction shows thought; naming a title shows a ladder → Ch 81 Q81-017 |
| Q76A-069 | Do you need to manage people to be senior? | No. Most data organisations have an individual-contributor track, and the two require different things | **[+Clarify]** ask which track the role is on, and what the next step looks like → Ch 66 §66.4 |
| Q76A-070 | "What would you do in your first 90 days?" | Learn the data, find one thing that is quietly broken, fix it, and tell people. Credibility before ambition | **[+Business]** one visible fix buys you the licence for the larger project → Ch 80 Q80-020 |
| Q76A-071 | Asked to mentor a junior while delivering your own work | Say yes and account for it. Mentoring absorbed silently is how it stops happening | **[+Trade-offs]** it is also the fastest way to find the gaps in your own understanding → Ch 9 §9.5 |
| Q76A-072 | You disagree with a decision already made | Disagree once, clearly, in writing, then commit. Re-litigating is what makes people stop asking you | **[+Business]** "I disagreed and here is why, and I am behind it" is a senior position → Ch 80 Q80-017 |
| Q76A-073 | How do you keep current without chasing every new tool? | Depth in fundamentals, awareness of the rest. The fundamentals have not moved in twenty years | **[+Trade-offs]** the half-life of a tool is short; the half-life of SQL and statistics is not → Ch 83 §83.2 |
| Q76A-074 | What makes a data team trusted? | Numbers that reconcile, definitions that are written down, and bad news delivered early | **[+Business]** trust is the asset; everything else is output → Ch 66 §66.2 |
| Q76A-075 | Asked what you are weakest at | Name a real one with what you are doing about it. A fake weakness is transparent and costs more than the real one | **[+Validate]** pick something true but not disqualifying for this role → Ch 81 Q81-013 |

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| A project narrative that opens with tools, not the business problem | Interviewer struggles to follow why the work mattered | Business question first, method second, impact last |
| No quantified impact in a project walkthrough | A vague "it really helped the team" with nothing to probe further | Always have at least a rough number, honestly caveated if it's rough |
| A rigid DA-vs-DS boundary with no acknowledgment of overlap | Sounds like a textbook definition, not real experience | Name where your own work actually sits, including the overlap |
| Defending a resume metric with no memory of its actual baseline | Signals the number may have been inflated or poorly measured | Know exactly how every headline number on your resume was calculated |
| A DS narrative dominated by algorithm names | Misses the framing, evaluation, and judgment an interviewer actually wants to see | Lead with problem framing and evaluation choice, not the model name |
| Doubling down when caught in a small inconsistency | Reads as defensiveness, damages trust more than the original slip | Acknowledge it plainly and move on |
| A memorized, over-polished project script | Breaks under a genuine follow-up that deviates from the script | Know the facts; don't memorize the wording |

---

## In the real world: the resume line that became the whole interview

Kavita, interviewing for a Data Analyst role after a career transition, has one line on her resume: "Automated a weekly report, saving the team 3 hours a week." The interviewer spends nearly ten minutes on that single line, not because it's the most impressive thing on the page, but because it's specific and checkable, and specific claims are exactly what a good interviewer knows how to probe.

She's asked: which report, what was manual about it before, how exactly was "3 hours" measured, did anyone verify the automated version was actually correct before it replaced the manual one, and what happened the one time it broke. Because she'd genuinely done the work and understood it, not just summarized it for a resume, she has a real, specific answer to each question, including an honest one about the time it broke: a source file's format changed upstream without warning, and she'd since added a validation check specifically because of that failure.

The interviewer's note afterward: *"The resume line was modest. The depth behind it was not. Ten minutes on one bullet point told us more than the rest of the resume combined."* The lesson generalizes: every single claim on a resume should be able to survive exactly this kind of sustained, specific scrutiny, not because interviewers are trying to catch you out, but because depth on a real claim is one of the fastest, most reliable signals of real work versus a polished summary of someone else's.

---

## Project

**Goal:** prepare two full project narratives, one DA-style and one DS-style (or two of whichever type matches your own background), to the standard this chapter models.

### Tools you'll need

No new tools beyond what earlier chapters in this part already cover. The one habit worth building specifically for this chapter: after finishing any real project, write a five-line summary immediately (business question, method, finding, impact number, one honest limitation) while it's fresh, so months later in an interview you're recalling a summary you already wrote carefully once, not reconstructing the whole thing from memory under pressure.

1. For each project, write the five-line summary described above: business question, method, finding, quantified impact, honest limitation.
2. Practice defending your single most impressive resume metric out loud: state its exact baseline, a like-for-like comparison, and one confound you checked, and say whether the change is in points or percent.
3. Write your honest, specific answer to "why this role and not the other one," using Q76A-002's structure.
4. Have someone else interrupt your project walkthrough with an unexpected follow-up question, and practice answering it without falling back on a memorized script.

---

## Key terms

Data Analyst vs. Data Scientist (role distinction) · business-question-first narrative structure · quantified impact · baseline (for a claimed metric) · confound (in a resume claim) · problem framing (DS) · cost-based threshold · honest limitation · portfolio deep-dive · resume scrutiny · the request underneath the request · reconciliation · definitional difference · intake route · scope creep · shadow reporting · counterfactual · holdout · stopping condition · lift over baseline · calibration · training-serving skew · read replica · statement timeout · schema drift · least privilege · stating the assumption · preventing a class of error · disagree and commit · individual-contributor track

---

## Final-week revision list

Q76A-001, Q76A-002, Q76A-007, Q76A-012, Q76A-017, Q76A-022, Q76A-027, Q76A-028, Q76A-029, Q76A-047, Q76A-067.

The last four are the situational ones most likely to decide an interview: the request that is never just a pull (Q76A-028), the number that disagrees with Finance (Q76A-029), explaining a model to someone who will not understand the algorithm (Q76A-047), and what actually separates mid from senior (Q76A-067).

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 76B, Business Analyst Question Bank,** covers the same "diagnose before responding" and stakeholder-pushback discipline from the BA angle.
- **Chapters 36–39** (lead scoring) and **Chapter 44** (the churn call list) are the projects behind this chapter's DS examples; if you did them, you can tell these stories as your own practice work.
- **Chapter 81, Behavioral, HR & Offer Conversations,** is where this chapter's project-narrative skills extend into full STAR-format behavioral stories.
