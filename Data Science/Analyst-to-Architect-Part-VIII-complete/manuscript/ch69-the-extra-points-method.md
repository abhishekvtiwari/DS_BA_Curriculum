# Chapter 69. The Extra-Points Method

*Part VIII — The Interview Playbook*

> **Chapter at a glance**
>
> **You will learn to:** understand the five dimensions interviewers actually score, whatever the question · give a "strong" answer instead of a merely correct one, and know the difference · use twelve specific moves that turn a strong answer into an outstanding one, practiced on twenty short examples · carry a question through all three answer tiers yourself, live, under time pressure · recognize the red flags and over-corrections that cost points even when the technical content is right.
>
> **Before you start:** nothing technical: this chapter is about *how* you answer, not what you know. It works alongside whichever question bank you're using (Chapters 70–82).
>
> **Time needed:** 3–4 hours to read and drill once; return to it before every interview.
>
> **Who this is for:** every role this book covers, from a first analyst screening call to an architect-level system design round.

---

## Why this matters

Two candidates are asked the same SQL question. Both write a query that returns the right rows. One gets an offer; the other doesn't. The difference wasn't correctness: it was *everything around* the correct answer, whether they checked what "right" meant before diving in, whether they mentioned the one edge case that breaks their own query, whether they tied it back to something a business would actually do with the result.

Interviewers rarely score on a pass/fail switch. They score on a spread, usually without writing it down anywhere you'll see, and the gap between "we can move this person forward" and "we're not sure" is almost never about knowing more facts. It's about a small set of habits, repeated consistently, that this chapter teaches directly rather than leaving you to notice by accident after your fifth rejected interview.

---

## In plain English

**Think of two students answering the same exam question: "What causes seasons?"**

One writes: "The Earth's tilt." Correct. One sentence.

The other writes: "The Earth's axis is tilted about 23.5 degrees, so as it orbits the sun, each hemisphere leans toward the sun for part of the year and away for the rest, which is what causes summer and winter (not distance from the sun, a common misconception worth ruling out). Here's a quick sketch showing why the northern and southern hemispheres are always opposite."

Both are "correct." Only one shows the examiner that the student actually understands the topic, anticipated the obvious wrong turn, and could teach it to someone else. Interviews reward the second student, every time, and the extra sentences aren't padding: each one is doing a specific job. This chapter is a catalog of those jobs.

---

## 69.1 How interviewers actually score

Across data roles (analyst, BA, BI, analytics engineer, data scientist, data engineer, ML engineer, architect), interviewers judge answers on five dimensions, whether or not they've written a rubric down:

| Dimension | 1 (Weak) | 2 (Acceptable) | 3 (Strong) | 4 (Outstanding) |
|---|---|---|---|---|
| **Correctness** | Wrong or incomplete | Correct for the simple case | Correct, including common edge cases | Correct, and explains *why* alternatives fail |
| **Structure & communication** | Rambling, jumps around | Understandable | Clear steps, signposted | Simple first, then depth; easy to follow for any audience |
| **Depth & edge cases** | None considered | Mentions one when prompted | Raises the important ones unprompted | Tests them, and explains the risk each creates |
| **Business judgment** | Purely technical | Mentions the business | Ties the answer to a decision or metric | Quantifies impact; proposes next actions |
| **Collaboration** | Doesn't clarify; defensive with hints | Accepts hints | Asks good clarifying questions | Checks assumptions, adapts, summarizes agreement |

Every model answer in every bank chapter (70–82) is written against this table. When a bank labels an answer "strong" or "extra-points," it means the answer scores mostly 3s or mostly 4s on this rubric, not that it uses fancier words.

Notice what's *not* here: raw technical knowledge. That's assumed. The rubric measures what you do *with* what you know, which is exactly the part a candidate can improve in a week, unlike years of experience.

> **Interview extra point.** If you only remember one thing from this chapter, make it this: **every dimension above except correctness can be practiced on a question you already know the answer to.** You don't need harder questions to get better at this. You need to notice, on questions you can already solve, that you're stopping at "correct" instead of continuing to "outstanding."

---

## 69.2 The shape of a strong answer

Before the twelve individual moves, one overall shape matters more than any of them: **simple first, depth second.**

Give the one-line answer immediately, the thing a manager skimming a transcript would want to read. Then, and only then, go deeper. Reversed, this fails badly: an interviewer who has to wait ninety seconds through background and caveats before hearing your actual answer starts wondering whether you *have* one.

**Weak shape:** "So there are a few ways to think about this, and it depends on the data, but generally speaking when we're dealing with duplicates there's a question of what counts as a duplicate in the first place, and. Okay, so, to find duplicate customers I'd probably group by the fields that should be unique and then filter for count greater than one."

**Strong shape:** "I'd group by the fields that should be unique and filter for a count above one. [pause] The one thing that changes the answer is what 'duplicate' means here: same email, or same name and phone, or something fuzzier like similar names with typos. Which is Riverstone worried about?"

Same technical content. The second version leads with the answer, then earns its follow-up sentence by asking something specific. That's the shape every example in this chapter follows, and it's worth drilling on its own, separately from the twelve moves below: **answer first, in one sentence, every time**, even when you're about to say more.

---

## 69.3 The twelve extra-point moves

Each move below gets a short before/after on a realistic Riverstone-style question, so you see the exact sentence that earns the point, not just the name of the technique. Practice each on a question of your own before moving to the next.

### Move 1: Clarify first

Restate the question and ask the one or two questions that actually change the answer. Not every question needs a clarification; asking one when nothing hinges on it wastes time and reads as stalling.

> **Question:** "Write a query to find our top customers."
>
> **Without the move:** Starts writing a query ranking by total order count.
>
> **With the move:** "Top by what: revenue, order count, or profit margin? And over what period? I'll assume revenue, all-time, unless you tell me otherwise." *(Then proceeds, having lost nothing.)*

### Move 2: State assumptions out loud when you can't ask

In take-home assignments and some live-coding platforms, nobody's there to answer a clarifying question. Say what you assumed and why, in one line, rather than silently picking one interpretation.

> "I'm treating a 'cancelled' order as not a sale, since that matches how Riverstone's dashboard defines revenue. I've noted this assumption in a comment in case that's wrong."

### Move 3: Signpost your structure

Before diving in, say the shape of what's coming. This costs three seconds and saves the interviewer from wondering whether you have a plan.

> "I'll cover three things: how I'd define 'churned' here, the query itself, and one edge case that trips people up."

### Move 4: Simple answer first, depth second

Covered in full in section 69.2. The most common single mistake candidates make is skipping this and going straight to the caveats.

### Move 5: Raise edge cases

The recurring list, worth memorizing: **NULLs, duplicates, ties, empty inputs, time zones, outliers, late-arriving data.** You don't need to check all seven every time; you need to scan the list and mention the one or two that actually apply.

> **Question:** "How would you calculate month-over-month growth?"
>
> **Without the move:** Gives the formula: (this month − last month) ÷ last month.
>
> **With the move:** Gives the formula, then: "One thing that breaks this: if last month was zero (a brand-new product line, say), the percentage is undefined or misleadingly huge. I'd flag those rows separately rather than let a division by zero either crash the report or silently show 'infinity%.'"

### Move 6: Offer trade-offs and alternatives

Name a second approach and say why you picked the one you did. This shows you're choosing, not guessing.

> "I could do this with a correlated subquery or a window function. I'd use the window function: same result, and it scans the table once instead of once per row, which matters once this table has millions of rows."

### Move 7: Validate the result

A sanity check, a hand calculation, or a reconciliation to a known total. This is the single most under-used move by otherwise-strong candidates, and one of the cheapest to add.

> "Before I trust this number, I'd check that the segments add up to the total: if 'Retail' plus 'Wholesale' plus 'Hospitality' revenue doesn't equal total revenue, something's wrong with the join before I even look at the results."

### Move 8: Connect to business impact

Say what decision the answer feeds, or what it's worth. A number with no owner and no use is a fact, not an insight.

> "This tells us 40 accounts haven't ordered in 90+ days. On its own that's a list. Paired with each account's revenue, it becomes a prioritized call list, which is what I'd actually hand to the sales head, not the raw 40 rows."

### Move 9: Think about scale and maintenance

Who runs this again next month? What happens when the table is 100 times bigger?

> "This query is fine at Riverstone's current size. If order volume grew 50x, I'd want an index on `order_date` and `customer_id`, and I'd think about whether this needs to be a scheduled job with its own table instead of a query run fresh every time someone opens the dashboard."

### Move 10: Admit limits honestly

Say what you don't know, and how you'd find out. Bluffing is far more damaging than a gap.

> "I haven't worked with Spark directly, but the concept (partitioning work across machines) is the same idea as parallelizing a `GROUP BY` across shards, which I have done. I'd expect to be productive within a couple of weeks, and I'd want to pair with someone on the team for the first real task."

### Move 11: Use real evidence

A specific project from your own work beats a hypothetical every time it's available.

> "I built something close to this at my last company: a weekly report that flagged accounts with no order in 30 days. The tricky part wasn't the query; it was agreeing with sales on what 'no order' should exclude, mainly trial accounts. I'd expect the same conversation here."

### Move 12: Close the loop

Summarize your answer in one line at the end, and check it actually answered what was asked. Interviews run long; a candidate who trails off without a clear ending makes the interviewer do the work of deciding whether you finished.

> "So: left join, filter on NULL, watch out for cancelled orders depending on the definition: does that answer what you were after, or did you want me to go further into the performance side?"

---

## 69.4 One question, all three tiers

Here's a single question carried through the full arc, so you can see the twelve moves working together rather than as an isolated list. This is the format every core question in Chapters 70–82 uses.

**Q · Riverstone's monthly revenue dropped 12% last month. How would you investigate?**

**Answer that passes** *(scores ~2)*

"I'd look at revenue by product and by region to see where the drop happened, then ask the sales team what changed."

Reasonable instinct, no structure, and it skips the question of whether the number is even real.

**Strong answer** *(scores ~3)*

"First I'd confirm the 12% is measuring what I think it's measuring, then break it down to find where it came from, then look for causes. Revenue is orders times average order value, so I'd check which of those two moved. Then I'd cut by segment, region, product category, and sales rep to find where the drop is concentrated. Once I know where, I'd look at likely causes: pricing changes, a lost account, a stock shortage, competitor activity, or plain seasonality."

**Extra-points answer** *(scores ~4, moves labeled)*

- **[+Clarify]** "Is that 12% against last month, the same month last year, or a target? And is it invoiced revenue or collected revenue? Those tell different stories."
- **[+Validate]** "Before I look for a business cause, I'd rule out a data problem: a failed pipeline load, a changed status mapping, orders stuck in 'Pending' that used to auto-close. A surprising share of scary-looking drops turn out to be exactly this."
- **[+Structure]** "I'd break it into a tree: revenue is orders times average order value; orders is active customers times orders per customer; average order value is units per order times price realized times product mix. Then I'd check each branch."
- **[+Edge cases]** "I'd also check calendar effects, such as fewer working days last month or a festival period shifting order timing, before assuming anything's actually wrong."
- **[+Depth]** "Within whichever branch moved, I'd look for concentration: is 80% of the drop from one region or one big account? Concentrated points to something specific; spread-out points to something broad, like a pricing change."
- **[+Business]** "I'd size each candidate cause in rupees, rank them, and bring back the two or three that explain most of the gap, each with a recommended action and an owner, not just a diagnosis."
- **[+Scale]** "And I'd suggest an early-warning metric, weekly new orders say, so the next time this happens, we catch it inside a week instead of at month-end."
- **[+Close the loop]** "So: confirm it's real, find where, then why, then act, and I'd want that whole loop closed inside two or three days, not weeks."

**Likely follow-ups:** *You find one customer caused 60% of the drop: what next? How do you tell a data issue from a real one, fast? What would you put on a dashboard to catch this earlier next time?*

**Red flags:** jumping straight to a cause · never questioning whether the data is even right · no numbers, only narrative · a structure so elaborate it never actually answers the question.

---

## 69.5 The same moves, under different rounds

Not every move fits every round equally. Knowing which to lean on saves time you don't have.

| Round | Moves that matter most | Why |
|---|---|---|
| **Screening call** | Simple first, close the loop | Fifteen minutes total; every question needs a fast, complete answer |
| **Live coding** | Clarify, edge cases, validate | The interviewer is watching your process, not just your final query |
| **Case / business** | Clarify, structure, business impact | There's rarely one right answer; structure is what's being graded |
| **System design** | Trade-offs, scale, admit limits | No design is free of trade-offs; pretending otherwise is the tell |
| **Behavioral** | Real evidence, close the loop | A concrete story beats a general philosophy every time |

Rapid-fire, low-stakes questions in any round rarely need more than moves 3, 4, and 7: signpost, lead with the answer, validate. Save the full twelve-move treatment for the two or three questions per interview that are clearly the ones being weighed most heavily; you can usually tell, because the interviewer leans in, takes notes, or asks a follow-up.

---

## 69.6 What not to do

Extra points are easy to over-apply. Three common over-corrections cost points just as fast as saying nothing:

- **Clarifying everything.** Asking a clarifying question about a question with an obvious, single interpretation reads as stalling, not diligence. Reserve it for questions where the answer genuinely changes.
- **Caveat overload.** Hedging every sentence ("it depends," "in most cases," "generally speaking") without ever committing to an answer scores *worse* on correctness than a clean, slightly-too-simple answer, because the interviewer can't tell if you actually know it.
- **Padding with business talk that isn't specific.** "This is important for the business" is not the business-judgment move; naming the decision it feeds, or estimating its size, is. A vague gesture at "impact" with no number attached earns nothing.

The twelve moves are seasoning, not the whole meal. A technically wrong answer with six moves labeled on it still scores as wrong.

---

## Common mistakes and how to spot them

| Mistake | Symptom | Fix |
|---|---|---|
| Leading with caveats instead of the answer | Interviewer looks confused or impatient partway through | Answer first, in one sentence; depth after |
| Clarifying a question with an obvious meaning | Feels like stalling; wastes shared time | Reserve clarifying questions for genuine ambiguity |
| Listing edge cases with no explanation | Sounds like reciting a checklist | Explain *why* each edge case you raise actually matters here |
| Business talk with no number | "This helps the business" and nothing else | Attach a rough size, a decision, or an owner |
| No ending | Trails off; interviewer has to ask "is that it?" | Close the loop: one summary sentence, check you answered the actual question |
| Overusing every move on every question | Runs out of time; low-stakes questions take too long | Match the moves to the round (69.5); save full depth for the questions that matter most |

---

## In the real world: the mock interview that changed nothing technical

Meera runs a mock interview for a colleague, Sneha, who's moving from a BA role toward data analytics. Sneha answers every technical question correctly: her SQL is clean, her statistics are sound. Meera's feedback afterward has nothing to do with any of that.

"You know all of this," Meera says. "What you're not doing is telling me you know it. You answer the question and stop. When I asked about duplicate customers, you wrote a correct query and waited. I had to ask you what happens if the join finds a NULL; you knew the answer the second I asked, which means you already knew it before I asked. Say it before I have to ask."

They redo three questions. Same technical answers, word for word on the first sentence. The only change: after each answer, Sneha adds one sentence: an edge case, a validation check, or what she'd actually do with the result. The mock interview "feels" completely different to both of them, even though Sneha learned nothing new about SQL that afternoon.

Two weeks later, in a real screening call, an interviewer asks her to find Riverstone's top customers by revenue. She answers, then adds: "Top by revenue over what period, I'll assume this year unless you say otherwise, and I'd want to check that a handful of large customers aren't a data error before presenting this as a ranked list." The interviewer's note, which Sneha sees months later after getting the offer, reads: *"Strong technical answer, but what stood out was she checked her own work without being asked."* Nothing there was new knowledge. It was the twelve moves, or rather, three of them, used at the right moment.

---

## Tools

No software for this chapter. The only "tool" worth naming: **record yourself** answering three questions from any bank chapter out loud, on your phone, then listen back and mark where you stopped at "correct" instead of continuing to "strong." Most people are surprised by how often that's the very first sentence.

---

## The project: score your own last answer

**Goal:** take an answer you've actually given, in a past interview, a work meeting, or a mock session, and rewrite it through all three tiers.

**Steps:**

1. Write down, as close to verbatim as you can recall, an answer you gave to a real technical or case question.
2. Score it against the five-dimension rubric (69.1), one to four on each dimension, honestly.
3. Identify which of the twelve moves (69.3) were present and which were missing.
4. Rewrite the answer as a "strong" tier answer, then again as "extra-points," labeling each move you add.
5. Time yourself saying the extra-points version out loud. If it's over two minutes, cut it: extra points that take too long lose the "structure & communication" dimension you just gained.

---

## You've got it when…

- [ ] I can name the five scoring dimensions without looking, and I know none of them is "technical knowledge" alone.
- [ ] I lead every answer with one sentence that actually answers the question, before any caveat.
- [ ] I can name all twelve moves, and I can give an example of each from memory.
- [ ] I know which moves matter most in which round, and I don't spend full-depth time on a fifteen-second warm-up question.
- [ ] I can catch myself over-clarifying or caveat-padding, and stop.
- [ ] I've rewritten at least one of my own real answers through all three tiers.

---

## Recap

- Interviewers score on **five dimensions** (correctness, structure, depth, business judgment, collaboration), not on technical correctness alone.
- **Simple answer first, depth second** is the single most important shape, underneath every other move.
- The **twelve extra-point moves** (clarify, state assumptions, signpost, simple-first, edge cases, trade-offs, validate, business impact, scale, admit limits, real evidence, close the loop) are specific, practicable habits, not vague advice to "communicate better."
- Different **rounds reward different subsets** of the twelve moves; matching effort to round matters under time pressure.
- Every move can be **overused**: over-clarifying, caveat overload, and vague business talk all cost points just as surely as saying nothing.
- The banks that follow (Chapters 70–82) write every model answer against this same rubric and label moves with the same tags, e.g. **[+Edge cases]**, so you'll see this pattern hundreds of times; the goal is for it to become automatic well before your next interview.

---

## Practice exercises

Each exercise below is a short question. Answer it three times (passing, strong, extra-points), labeling your moves on the third pass, exactly as section 69.4 modeled. These twenty, plus the worked example in 69.4, are this chapter's full set of practiced examples.

1. What's the difference between `WHERE` and `HAVING`?
2. How would you find duplicate rows in a customer table?
3. Explain a left join to someone non-technical.
4. Riverstone wants a single "health score" per customer. How would you design it?
5. What's the difference between mean and median, and when would you use each?
6. How would you detect an outlier in monthly sales data?
7. A dashboard number looks wrong. Walk me through how you'd check it.
8. How would you explain a confidence interval to a sales manager?
9. Design a KPI dashboard for a customer support team.
10. What's the difference between a data warehouse and a data lake?
11. How would you handle a stakeholder who wants a report you think is misleading?
12. Write a query to find each customer's most recent order. *(Sketch the query in words, then apply the moves to your explanation of it.)*
13. What would you do if two source systems disagree about the same number?
14. How would you decide between a bar chart and a line chart for a given dataset?
15. Explain overfitting to someone who's never trained a model.
16. A scheduled report failed to send this morning. Walk me through how you'd find out why.
17. How would you prioritize which of ten dashboard requests to build first?
18. What's the difference between correlation and causation, with a Riverstone-style example?
19. How would you onboard a new analyst onto a report you built and then left?
20. Tell me about a time you disagreed with a decision at work. *(A behavioral question: apply moves 3, 11, and 12 especially.)*

*(In the finished book, one worked answer per exercise, at all three tiers, appears in Appendix G, cross-referenced to the bank chapter that teaches its underlying content.)*

---

## Key terms

extra-point moves · five-dimension rubric · correctness · structure & communication · depth & edge cases · business judgment · collaboration · simple-first · clarifying question · stated assumption · signposting · edge case · trade-off · validation (sanity check) · business impact · scale and maintenance · admitting limits · real evidence · closing the loop · red flag (interview) · over-correction

---

## Where this leads

- **Chapters 70–82**, every bank in this part, write their core-question model answers against this chapter's rubric and label moves with the same tags introduced here.
- **Chapter 68, How Data Hiring Works**, covers what happens before you're in the room (screening, portfolios, referrals), which this chapter doesn't touch.
- **Chapter 82, Take-Home Assignments & Mock Interviews**, is where you apply this chapter under realistic time pressure, end to end.
