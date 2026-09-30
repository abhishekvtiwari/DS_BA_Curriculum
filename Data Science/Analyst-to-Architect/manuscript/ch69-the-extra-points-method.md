# Chapter 69. The Extra-Points Method

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** understand the five dimensions that interview rubrics score, whatever the question · give a "strong" answer instead of a merely correct one, and know the difference · use twelve specific moves that turn a strong answer into an outstanding one, each shown before and after on a short example · carry a question through all three answer tiers yourself, live, under time pressure · recognize the red flags and over-corrections that cost points even when the technical content is right.
>
> **Before you start:** the method needs nothing technical: this chapter is about *how* you answer, not what you know. The exercises draw on Chapters 4 and 12–51; each one names where its content is taught, so skip any you haven't studied. The method works alongside whichever question bank you use next (Chapters 70–82).
>
> **Time needed:** about 1½ hours to read; 4–6 hours to drill all twenty exercises (or 1–2 hours for the five nearest your role); return to it before every interview.
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

Across data roles (analyst, BA, BI, analytics engineer, data scientist, data engineer, ML engineer, architect), companies' written rubrics differ, but most score some version of these five dimensions. This book uses this table as its rubric:

| Dimension | 1 (Weak) | 2 (Acceptable) | 3 (Strong) | 4 (Outstanding) |
|---|---|---|---|---|
| **Correctness** | Wrong or incomplete | Correct for the simple case | Correct, including common edge cases | Correct, and explains *why* alternatives fail |
| **Structure & communication** | Rambling, jumps around | Understandable | Clear steps, signposted | Simple first, then depth; easy to follow for any audience |
| **Depth & edge cases** | None considered | Mentions one when prompted | Raises the important ones unprompted | Tests them, and explains the risk each creates |
| **Business judgment** | Purely technical | Mentions the business | Ties the answer to a decision or metric | Quantifies impact; proposes next actions |
| **Collaboration** | Doesn't clarify; defensive with hints | Accepts hints | Asks good clarifying questions | Checks assumptions, adapts, summarizes agreement |

> **Simplification.** Real rubrics often end in a plain "hire / no hire" with written notes. The five dimensions are what those notes are about.

In this book an answer that **passes** scores mostly 2s, a **strong** answer mostly 3s, and an **extra-points** answer mostly 4s; a 1 is a fail and gets no tier. Every core question in the banks (Chapters 70–81) is written against this table in those three tiers; the rapid-fire tables give a one-line answer plus one extra point, and Chapter 82 scores whole mock interviews on the same five dimensions. When a bank labels an answer "strong" or "extra-points," it means the answer scores mostly 3s or mostly 4s on this rubric, not that it uses fancier words.

Notice that four of the five dimensions aren't about how much you know. Correctness is assumed to be necessary; the other four are what separate candidates who are all correct. The rubric measures what you do *with* what you know, which is exactly the part a candidate can improve in a week, unlike years of experience.

> **Interview extra point.** If you only remember one thing from this chapter, make it this: **every dimension above except correctness can be practiced on a question you already know the answer to.** You don't need harder questions to get better at this. You need to notice, on questions you can already solve, that you're stopping at "correct" instead of continuing to "outstanding."

---

## 69.2 The shape of a strong answer

Before the twelve individual moves, one overall shape matters more than any of them: **simple first, depth second.**

Give the one-line answer immediately, the thing a manager skimming a transcript would want to read. Then, and only then, go deeper. Reversed, this fails badly: an interviewer who has to wait ninety seconds through background and caveats before hearing your actual answer starts wondering whether you *have* one.

**Weak shape:** "So there are a few ways to think about this, and it depends on the data, but generally speaking when we're dealing with duplicates there's a question of what counts as a duplicate in the first place, and… okay, so, to find duplicate customers I'd probably group by the fields that should be unique and then filter for count greater than one."

**Strong shape:** "I'd group by the fields that should be unique and filter for a count above one. [pause] The one thing that changes the answer is what 'duplicate' means here: same email, or same name and phone, or something fuzzier like similar names with typos. Which is Riverstone worried about?"

Same technical content. The second version leads with the answer, then earns its follow-up sentence by asking something specific. That's the shape every example in this chapter follows, and it's worth drilling on its own, separately from the twelve moves below: **answer first, in one sentence, every time**, even when you're about to say more.

---

## 69.3 The twelve extra-point moves

Each move below gets the same three lines on a realistic Riverstone-style question: the question, an answer without the move, and the same answer with it, so you see the exact sentence that earns the point, not just the name of the technique. Where an example leans on something technical, the chapter that teaches it is named in brackets. Practice each on a question of your own before moving to the next.

### Move 1: Clarify first

Restate the question and ask the one or two questions that actually change the answer. Not every question needs a clarification; asking one when nothing hinges on it wastes time and reads as stalling.

> **Question:** "Write a query to find our top customers."
>
> **Without the move:** Starts writing a query ranking by total order count.
>
> **With the move:** "Top by what: revenue, order count, or profit margin? And over what period? I'll assume revenue, all-time, unless you tell me otherwise." *(Then proceeds, having lost nothing.)*

### Move 2: State assumptions out loud when you can't ask

In take-home assignments and some live-coding platforms, nobody's there to answer a clarifying question. Say what you assumed and why, in one line, rather than silently picking one interpretation.

> **Question (take-home):** "Calculate Riverstone's 2025 revenue."
>
> **Without the move:** Adds up every order and reports ₹43,98,121, silently counting the two cancelled orders.
>
> **With the move:** "I'm treating a cancelled order as not a sale, since that matches how Riverstone's reports define revenue. That gives ₹43,35,471; counting the two cancelled orders (₹62,650) would give ₹43,98,121. I've noted this assumption in a comment in case that's wrong."

### Move 3: Signpost your structure

Before diving in, say the shape of what's coming. This costs three seconds and saves the interviewer from wondering whether you have a plan.

> **Question:** "How would you find churned customers?"
>
> **Without the move:** Starts writing a query at once, and the interviewer has to guess where it's heading and whether "churned" means what they mean.
>
> **With the move:** "I'll cover three things: how I'd define 'churned' here, the query itself, and one edge case that trips people up."

### Move 4: Simple answer first, depth second

Covered in full in section 69.2. The most common single mistake candidates make is skipping this and going straight to the caveats.

> **Question:** "How would you find duplicate customers?"
>
> **Without the move:** Two sentences about what might count as a duplicate before any answer at all (section 69.2's weak shape).
>
> **With the move:** "I'd group by the fields that should be unique and keep the groups with a count above one (Chapter 12, section 12.9). The thing that changes the answer is what 'duplicate' means here…"

### Move 5: Raise edge cases

The recurring list, worth memorizing: **NULLs, duplicates, ties, empty inputs, time zones, outliers, late-arriving data.** You don't need to check all seven every time; you need to scan the list and mention the one or two that actually apply.

> **Question:** "How would you calculate month-over-month growth?"
>
> **Without the move:** Gives the formula: (this month − last month) ÷ last month × 100 (Chapter 4, section 4.1; in SQL, Chapter 13, section 13.6).
>
> **With the move:** Gives the formula, then: "One thing that breaks this: if last month was zero (a brand-new product line, say), the percentage is undefined or misleadingly huge. I'd flag those rows separately rather than let a division by zero either crash the report or silently show 'infinity%.'"

### Move 6: Offer trade-offs and alternatives

Name a second approach and say why you picked the one you did. This shows you're choosing, not guessing.

> **Question:** "Find each customer's latest order."
>
> **Without the move:** Writes a correlated subquery (Chapter 12, section 12.12) and stops.
>
> **With the move:** "I could do this with a correlated subquery or a window function (Chapter 13, section 13.4). I'd use the window function: a correlated subquery can run once per row unless the database rewrites it; a window function reliably scans once, which matters once this table has millions of rows. I'd check the query plan to be sure (Chapter 28, section 28.5)."

### Move 7: Validate the result

A sanity check, a hand calculation, or a reconciliation to a known total. This is the single most under-used move by otherwise-strong candidates, and one of the cheapest to add.

> **Question:** "Show Riverstone's 2025 revenue by segment."
>
> **Without the move:** Shows the three segment totals and stops.
>
> **With the move:** "Before I trust these numbers, I'd check that the segments add up to the total: Retail plus Wholesale plus Hospitality should come to ₹43,35,471. If they don't, something's wrong with the join before I even look at the results."

### Move 8: Connect to business impact

Say what decision the answer feeds, or what it's worth. A number with no owner and no use is a fact, not an insight.

> **Question:** "Which accounts haven't ordered in the last 90 days?"
>
> **Without the move:** Returns the list of names.
>
> **With the move:** "At the end of 2025 this finds three accounts that ordered earlier in the year and then went quiet for more than 90 days, plus Home Plus, which never ordered at all. On its own that's a list. Paired with each account's revenue (the three bought about ₹1.7 lakh between them in 2025), it becomes a prioritized call list, which is what I'd actually hand to the sales head, not the raw rows."

### Move 9: Think about scale and maintenance

Who runs this again next month? What happens when the table is 100 times bigger?

> **Question:** "We'd like that at-risk query to run every Monday. Anything you'd change?"
>
> **Without the move:** "No, it works."
>
> **With the move:** "This query is fine at Riverstone's current size. If order volume grew 50x, I'd want an index on `order_date` and `customer_id` (Chapter 28, section 28.6), and I'd think about whether this needs to be a scheduled job with its own table (Chapter 46) instead of a query run fresh every time someone opens the dashboard."

### Move 10: Admit limits honestly

Say what you don't know, and how you'd find out. Bluffing is far more damaging than a gap.

> **Question:** "Have you used Spark?"
>
> **Without the move:** "Yes, a bit," hoping there's no follow-up; or a flat "No," and silence.
>
> **With the move:** "I haven't used Spark, but I've [split a large job into chunks, for example processed a year of order data month by month in Python]. The idea, splitting work so parts run in parallel, is the same. I'd expect to be productive within a couple of weeks, and I'd want to pair with someone on the team for the first real task."

Fill the brackets with something you have actually done. Only claim what you've done. (If you worked through Chapter 48, you've run Spark on one machine: say exactly that, and no more.)

### Move 11: Use real evidence

A specific project from your own work beats a hypothetical every time it's available.

> **Question:** "Have you built anything like this?"
>
> **Without the move:** "Yes, similar things," with no detail; or a hypothetical "I would…".
>
> **With the move:** "I built something close to this at my last company: a weekly report that flagged accounts with no order in 30 days. The tricky part wasn't the query; it was agreeing with sales on what 'no order' should exclude, mainly trial accounts. I'd expect the same conversation here."

Use a project you actually did. Your Chapter 27 portfolio project counts.

### Move 12: Close the loop

Summarize your answer in one line at the end, and check it actually answered what was asked. Interviews run long; a candidate who trails off without a clear ending makes the interviewer do the work of deciding whether you finished.

> **Question:** "List customers who have never placed an order."
>
> **Without the move:** Writes the query and stops talking, leaving the interviewer to ask "is that it?"
>
> **With the move:** "So: left join from customers to orders, keep the rows where the order is NULL (Chapter 12, section 12.10), and watch out for cancelled orders depending on the definition. Does that answer what you were after, or did you want me to go further into the performance side?"

### The twelve tags

When an answer labels its moves, as section 69.4 and the banks that follow do, it uses one short tag per move, always written the same way:

| Move | Tag | Move | Tag |
|---|---|---|---|
| 1 Clarify first | **[+Clarify]** | 7 Validate the result | **[+Validate]** |
| 2 State assumptions | **[+Assume]** | 8 Business impact | **[+Business]** |
| 3 Signpost your structure | **[+Signpost]** | 9 Scale and maintenance | **[+Scale]** |
| 4 Simple answer first | **[+Simple first]** | 10 Admit limits honestly | **[+Limits]** |
| 5 Raise edge cases | **[+Edge cases]** | 11 Use real evidence | **[+Evidence]** |
| 6 Trade-offs and alternatives | **[+Trade-offs]** | 12 Close the loop | **[+Close]** |

---

## 69.4 One question, all three tiers

Here's a single question carried through the full arc, so you can see seven of the twelve moves working together rather than as an isolated list. Simple first sits underneath all of them, and the other four (assumptions, trade-offs, limits, evidence) fit other kinds of questions, as section 69.5 shows. Every core question in the banks uses this three-tier format; the rapid-fire tables give the strong answer plus one extra point.

**Q · Riverstone's monthly revenue dropped 12% last month. How would you investigate?**

**Answer that passes** *(scores ~2)*

"I'd look at revenue by product and by region to see where the drop happened, then ask the sales team what changed."

Reasonable instinct, no structure, and it skips the question of whether the number is even real.

**Strong answer** *(scores ~3)*

"First I'd confirm the 12% is measuring what I think it's measuring, then break it down to find where it came from, then look for causes. Revenue is orders times average order value, so I'd check which of those two moved. Then I'd cut by segment, region, product category, and sales rep to find where the drop is concentrated. Once I know where, I'd look at likely causes: pricing changes, a lost account, a stock shortage, competitor activity, or plain seasonality."

**Extra-points answer** *(scores ~4, moves labeled)*

- **[+Clarify]** "Is that 12% against last month, the same month last year, or a target? And is it invoiced revenue or collected revenue? Those tell different stories."
- **[+Validate]** "Before I look for a business cause, I'd rule out a data problem: a failed pipeline load, a changed status mapping, orders stuck in 'Pending' that used to auto-close. A surprising share of scary-looking drops turn out to be exactly this."
- **[+Signpost]** "I'd break it into a tree: revenue is orders times average order value; orders is active customers times orders per customer; average order value is units per order times average price per unit, and average price moves with list prices, discounts and product mix. Then I'd check each branch, and within whichever branch moved, look for concentration: is 80% of the drop from one region or one big account? Concentrated points to something specific; spread-out points to something broad, like a pricing change."
- **[+Edge cases]** "I'd also check calendar effects, such as fewer working days last month or a festival period shifting order timing, before assuming anything's actually wrong."
- **[+Business]** "I'd size each candidate cause in rupees, rank them, and bring back the two or three that explain most of the gap, each with a recommended action and an owner, not just a diagnosis."
- **[+Scale]** "And I'd suggest an early-warning metric, weekly new orders say, so the next time this happens, we catch it inside a week instead of at month-end."
- **[+Close]** "So: confirm it's real, find where, then why, then act, and I'd want that whole loop closed inside two or three days, not weeks."

**Likely follow-ups:** *You find one customer caused 60% of the drop: what next? How do you tell a data issue from a real one, fast? What would you put on a dashboard to catch this earlier next time?*

**Red flags:** jumping straight to a cause · never questioning whether the data is even right · no numbers, only narrative · a structure so elaborate it never actually answers the question.

**Learn it in:** Chapter 23, sections 23.10 (KPI trees) and 23.11 (diagnosing a change).

---

## 69.5 The same moves, under different rounds

Not every move fits every round equally. Knowing which to lean on saves time you don't have.

| Round | Moves that matter most | Why |
|---|---|---|
| **Screening call** | Simple first, close the loop | Fifteen minutes total; every question needs a fast, complete answer |
| **Live coding** | Clarify, edge cases, validate | The interviewer is watching your process, not just your final query |
| **Case / business** | Clarify, signpost, business impact | There's rarely one right answer; the structure you signpost is what's being graded |
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

## Common mistakes

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

Meera runs a mock interview for a friend, Ishita, who's moving from a BA role toward data analytics. Ishita answers every technical question correctly: her SQL is clean, her statistics are sound. Meera's feedback afterward has nothing to do with any of that.

"You know all of this," Meera says. "What you're not doing is telling me you know it. You answer the question and stop. When I asked about duplicate customers, you wrote a correct query and waited. I had to ask you what happens if the join finds a NULL; you knew the answer the second I asked, which means you already knew it before I asked. Say it before I have to ask."

They redo three questions. Same technical answers, word for word on the first sentence. The only change: after each answer, Ishita adds one sentence: an edge case, a validation check, or what she'd actually do with the result. The mock interview "feels" completely different to both of them, even though Ishita learned nothing new about SQL that afternoon.

Two weeks later, in a real screening call with another company, an interviewer asks her to find a distributor's top customers by revenue. She answers, then adds: "Top by revenue over what period, I'll assume this year unless you say otherwise, and I'd want to check that a handful of large customers aren't a data error before presenting this as a ranked list." When the offer comes, the hiring manager tells her on the call what stood out: *she checked her own work without being asked.* Nothing there was new knowledge. It was the twelve moves, or rather, three of them, used at the right moment.

---

## Project: score your own last answer

**Goal:** take an answer you've actually given, in a past interview, a work meeting, or a mock session, and rewrite it through all three tiers.

### Tools you'll need

No software for this chapter. The only "tool" worth naming: **record yourself** answering three questions from any bank chapter out loud, on your phone, then listen back and mark where you stopped at "correct" instead of continuing to "strong." Most people are surprised by how often that's the very first sentence.

**Steps:**

1. Write down, as close to verbatim as you can recall, an answer you gave to a real technical or case question.
2. Score it against the five-dimension rubric (69.1), one to four on each dimension, honestly.
3. Identify which of the twelve moves (69.3) were present and which were missing.
4. Rewrite the answer as a "strong" tier answer, then again as "extra-points," labeling each move you add with its tag.
5. Time yourself saying the extra-points version out loud. If it's over two minutes, cut it: extra points that take too long lose the "structure & communication" dimension you just gained.

---

## Recap

- Most interview rubrics score some version of **five dimensions** (correctness, structure, depth, business judgment, collaboration), not technical correctness alone.
- **Simple answer first, depth second** is the single most important shape, underneath every other move.
- The **twelve extra-point moves** (clarify, state assumptions, signpost, simple-first, edge cases, trade-offs, validate, business impact, scale, admit limits, real evidence, close the loop) are specific, practicable habits, not vague advice to "communicate better."
- Different **rounds reward different subsets** of the twelve moves; matching effort to round matters under time pressure.
- Every move can be **overused**: over-clarifying, caveat overload, and vague business talk all cost points just as surely as saying nothing.
- The banks that follow (Chapters 70–82) write their model answers against this same rubric and label moves with the twelve tags from section 69.3, e.g. **[+Edge cases]**, so you'll see this pattern hundreds of times; the goal is for it to become automatic well before your next interview.

---

## Key terms

extra-point moves · five-dimension rubric · correctness · structure & communication · depth & edge cases · business judgment · collaboration · simple-first · clarifying question · stated assumption · signposting · edge case · trade-off · validation (sanity check) · business impact · scale and maintenance · admitting limits · real evidence · closing the loop · move tag · red flag (interview) · over-correction

---

## Check yourself

- [ ] I can name the five scoring dimensions without looking, and I know none of them is "technical knowledge" alone.
- [ ] I lead every answer with one sentence that actually answers the question, before any caveat.
- [ ] I can name all twelve moves, and I can give an example of each from memory.
- [ ] I know which moves matter most in which round, and I don't spend full-depth time on a fifteen-second warm-up question.
- [ ] I can catch myself over-clarifying or caveat-padding, and stop.
- [ ] I've rewritten at least one of my own real answers through all three tiers.

---

## Exercises

Each exercise below is a short question. Answer it three times (passing, strong, extra-points), labeling your moves on the third pass with the tags from section 69.3, exactly as section 69.4 modeled. After each question, in brackets, are the roles that most often hear it (DA data analyst, BA business analyst, BI BI developer, DS data scientist, DE data engineer; "all" means every role) and where its content is taught. Skip any whose chapter you haven't studied yet.

### Definitions (Easy)

1. What's the difference between `WHERE` and `HAVING`? *(DA, BI, DE · Chapter 12, section 12.9)*
2. Explain a left join to someone non-technical. *(DA, BA, BI · Chapter 12, section 12.10)*
3. What's the difference between mean and median, and when would you use each? *(all · Chapter 4, section 4.5; Chapter 21, section 21.1)*
4. What's the difference between a data warehouse and a data lake? *(DE, DS, architect · Chapter 49, sections 49.1 and 49.5)*
5. How would you decide between a bar chart and a line chart for a given dataset? *(DA, BI · Chapter 15, sections 15.3 and 15.4)*
6. Explain overfitting to someone who's never trained a model. *(DS · Chapter 37, sections 37.6 and 37.10)*
7. What's the difference between correlation and causation, with a Riverstone-style example? *(DA, DS · Chapter 22, section 22.5)*

### Diagnosis (Medium)

8. How would you find duplicate rows in a customer table? *(DA, DE · Chapter 14, section 14.4)*
9. How would you detect an outlier in monthly sales data? *(DA, DS · Chapter 14, section 14.6; Chapter 21, section 21.4)*
10. A dashboard number looks wrong. Walk me through how you'd check it. *(DA, BI · Chapter 14, sections 14.10 and 14.11; Chapter 47, section 47.8)*
11. Write a query to find each customer's most recent order. *(DA, DE · Chapter 13, section 13.4. Sketch the query in words, then apply the moves to your explanation of it.)*
12. What would you do if two source systems disagree about the same number? *(DA, BA, DE · Chapter 14, section 14.11; Chapter 23, section 23.13; Chapter 51, section 51.5)*
13. A scheduled report failed to send this morning. Walk me through how you'd find out why. *(DA, BI, DE · Chapter 20, section 20.11; Chapter 46, section 46.6)*

### Design and judgment (Hard)

14. Riverstone wants a single "health score" per customer. How would you design it? *(DA, DS, BA · Chapter 23, section 23.9; Chapter 51, section 51.1)*
15. How would you explain a confidence interval to a sales manager? *(DA, DS · Chapter 22, section 22.1)*
16. Design a KPI dashboard for a customer support team. *(DA, BI · Chapter 23, sections 23.8 and 23.12; Chapter 16, section 16.7)*
17. How would you handle a stakeholder who wants a report you think is misleading? *(all · Chapter 24, section 24.8; Chapter 15, section 15.12)*
18. How would you prioritize which of ten dashboard requests to build first? *(DA, BA, BI · Chapter 24, section 24.1; Chapter 25, section 25.12)*
19. How would you onboard a new analyst onto a report you built and then left? *(DA, BI · Chapter 20, section 20.13; Chapter 26, section 26.9)*

### Behavioral

20. Tell me about a time you disagreed with a decision at work. *(all · Chapter 24, section 24.8. A behavioral question: apply moves 3, 11, and 12 especially.)*

---

## Answers

Five answers are worked in full, in all three tiers (exercises 1, 3, 10, 12 and 20: one from each group, plus a second diagnosis question). The other fifteen give the strong answer and the extra points most worth adding; write the other tiers yourself and compare. Every number below is quoted from the chapter named beside it. The Riverstone order figures come from the one-year database, `riverstone_2025` (Chapter 13, section 13.1), with cancelled orders left out unless the answer says otherwise, and were re-run for this chapter.

**1. `WHERE` and `HAVING`** *(worked in full)*

- **Passes:** "`WHERE` filters rows; `HAVING` filters groups."
- **Strong:** "`WHERE` filters individual rows before they're grouped; `HAVING` filters the groups after aggregation, so it's the only place you can test a count or a sum. To find customers with more than ten orders in 2025, the status filter goes in `WHERE` and `COUNT(*) > 10` goes in `HAVING`."
- **Extra points:**
  - **[+Simple first]** Lead with that one-line difference before any detail.
  - **[+Edge cases]** "`WHERE` can't use an aggregate, because at that step no counts exist yet: the database works through `FROM`, `WHERE`, `GROUP BY`, `HAVING`, then `SELECT` (Chapter 12, section 12.11)."
  - **[+Trade-offs]** "A condition on a plain column, such as the status, belongs in `WHERE`: rows are removed before the grouping work, and the intent is clearer."
  - **[+Validate]** "On Riverstone's 2025 data that query returns seven customers, led by Green Leaf Hotels with 17 orders. I'd check one of them by counting its orders directly."

**2.** Strong: "Start from a complete list and bring in matching details where they exist. Every customer stays on the list; a customer with no orders just shows blanks in the order columns." Extra points: **[+Business]** that's exactly how you find customers who have never ordered (Home Plus, in Riverstone's 2025 data); **[+Edge cases]** a customer with three orders appears three times, so count customers, not rows.

**3. Mean and median** *(worked in full)*

- **Passes:** "The mean is the average; the median is the middle value."
- **Strong:** "The mean adds everything up and divides by the count; the median is the middle value once the values are sorted. Use the median when a few large values pull the mean up, as with order values or salaries; use the mean when totals must work, because the mean times the count gives back the total."
- **Extra points:**
  - **[+Business]** "On Riverstone's 2025 orders the mean is ₹25,061 but the median is ₹21,375, and only 70 of the 173 orders are above the mean. Tell a sales executive 'the average order is ₹25,061' and most of their orders will feel below average (Chapter 4, section 4.5)."
  - **[+Edge cases]** "Check for outliers first: the largest order, ₹1,00,278, moves the mean but hardly moves the median."
  - **[+Trade-offs]** "For budgets and forecasts, use the mean, because it adds up; for 'what does a typical order look like', use the median."
  - **[+Close]** "So: median for typical, mean for totals, and report both when they disagree."

**4.** Strong: "A warehouse holds cleaned, structured tables for analysis, with a schema and transactions; a lake holds raw files of any format cheaply in object storage. A lakehouse puts a table format such as Delta Lake on top of the lake so the files behave like tables." Extra points: **[+Trade-offs]** a lake without discipline becomes a swamp, with no transactions, no schema and no history; **[+Business]** Riverstone keeps orders in the warehouse and its sensor archive as Parquet in object storage, because each suits its job (Chapter 49, section 49.1).

**5.** Strong: "A line for a sequence over time, where the trend is the message; bars for comparing separate categories. Monthly revenue is a line; revenue by segment is a bar." Extra points: **[+Edge cases]** a bar's axis must start at zero, because its length is its value; a line's axis needn't, if you label it clearly (Chapter 15, sections 15.3 and 15.4); **[+Clarify]** ask what the reader should notice first: change over time, or which is biggest.

**6.** Strong: "Overfitting is a model memorizing its training examples, noise included, instead of learning the pattern. It scores well on data it has seen and poorly on new data, like a student who memorized last year's answers." Extra points: **[+Validate]** you catch it by comparing training and validation scores: a big gap is the symptom (Chapter 37, section 37.10); **[+Trade-offs]** the fixes are more data, a simpler model, or regularization, each at some cost.

**7.** Strong: "Two things moving together doesn't mean one causes the other. Customers who get slower deliveries might order less, or the customers who order irregularly might get worse service: that's reverse causation. And a third thing can drive both, like summer driving ice-cream sales and drownings." Extra points: **[+Validate]** on Riverstone's 2025 customers, orders and average delivery days barely correlate (r = −0.086), which neither proves nor disproves that slow delivery costs orders (Chapter 22, section 22.5); **[+Business]** to test a cause, run an experiment or use a method from Chapter 31.

**8.** Strong: "Group by the fields that should be unique and keep the groups with `COUNT(*) > 1`; then decide which record in each group to keep." Extra points: **[+Clarify]** exact duplicates or fuzzy ones (same email, or similar names with typos)? (Chapter 14, section 14.4); **[+Edge cases]** trim spaces and match case before comparing, and remember that blank emails all group together.

**9.** Strong: "Plot the months first. Then flag any month outside the fences, 1.5 × IQR beyond the quartiles, and find out whether each flagged month is an error or real." Extra points: **[+Edge cases]** a festive-season spike is real, not an error, so compare each month with the same month last year too (Chapter 14, section 14.6; Chapter 21, section 21.4); **[+Business]** never delete an outlier just because it's big: fix it if it's an error, explain it if it's real.

**10. A dashboard number looks wrong** *(worked in full)*

- **Passes:** "I'd rerun the query and see whether the number changes."
- **Strong:** "First I'd pin down what 'wrong' means: wrong compared with what, and by how much. Then I'd reconcile the dashboard to its source one step at a time, with the same filters, dates and definition in a direct query, until the two agree or I find the step where they split."
- **Extra points:**
  - **[+Clarify]** "Who noticed, and what number did they expect? A finance total and a sales total often differ by definition, not by error."
  - **[+Validate]** "I'd check against a known total: Riverstone's 2025 revenue is ₹43,35,471, and December's is ₹4,39,823.50."
  - **[+Edge cases]** "The usual suspects: cancelled orders counted as sales (that alone turns ₹43,35,471 into ₹43,98,121), a join that duplicates rows, a date or time-zone boundary, or a refresh that didn't run."
  - **[+Business]** "I'd tell the people who use the number what's wrong and when it'll be fixed, before they find out for themselves (Chapter 47, section 47.8)."
  - **[+Scale]** "Once it's fixed, I'd add a check that would have caught it: a reconciliation that must return zero (Chapter 14, section 14.10)."
  - **[+Close]** "So: define the gap, reconcile step by step, fix, tell people, and add the check."

**11.** Strong: "Number each customer's orders newest first with `ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC)`, and keep row 1 (Chapter 13, section 13.4)." Extra points: **[+Edge cases]** two orders on the same day are a tie: add `order_id` to the `ORDER BY` so the choice is repeatable, or use `RANK()` to keep both; **[+Trade-offs]** a correlated subquery gives the same result; say why you chose the window function (Move 6).

**12. Two source systems disagree** *(worked in full)*

- **Passes:** "I'd use the system I trust more."
- **Strong:** "I'd find out why they differ before choosing one. I'd compare the definitions (what each counts, which statuses, which dates), then the timing (when each was last updated), then match the records one by one to find the rows that differ. Usually the gap is a definition or timing difference, not a bug."
- **Extra points:**
  - **[+Clarify]** "Which number is being used for a decision, and by whom? That tells me which gap matters."
  - **[+Signpost]** "Definitions first, then timing, then row-by-row matching."
  - **[+Validate]** "To match records, I'd join the two on their shared key with a full outer join (Chapter 12, section 12.10); rows that exist on only one side usually explain most of the gap (Chapter 14, section 14.11)."
  - **[+Business]** "Then I'd agree which system is the system of record for this number (Chapter 51, section 51.5) and write the definition down so both teams get the same number from now on (Chapter 23, section 23.13)."
  - **[+Close]** "So: explain the gap, fix the definition, and name one source of truth."

**13.** Strong: "Check the run log first: did the job start, did it fail, and at which step: getting the data, building the report, or sending it? Then fix it, resend, and tell the recipients." Extra points: **[+Edge cases]** "no data today" and "the job failed" need different fixes, and a rerun must not send the report twice (Chapter 20, section 20.11); **[+Scale]** an alert on failure and automatic retries, so next time you hear about it before the recipients do (Chapter 46, section 46.6); **[+Business]** for the Daily Sales Flash, due by 07:30 IST, tell the readers first, then investigate.

**14.** Strong: "Start from the decision it serves, such as which accounts the account managers call first. Pick a few signals that predict that outcome (order frequency against the customer's own usual rhythm, the recent revenue trend, support tickets, payment history), score each simply, combine them, and check the score against customers who actually stopped ordering." Extra points: **[+Simple first]** start with a rule-based score before any model; **[+Validate]** test it on last year: did the low scores really go quiet? (Chapter 13, section 13.8, pattern 6); **[+Scale]** write the score back into the CRM where account managers already work (Chapter 51).

**15.** Strong: "It's a range that probably contains the true value, and its width tells you how sure we are. '62% of customers are satisfied, give or take about five points' is the honest report from a survey of 400 customers (Chapter 22, section 22.1)." Extra points: **[+Business]** ask whether the decision changes anywhere in that range: if it doesn't, the width doesn't matter; **[+Edge cases]** the method is right 95% of the time, so about one interval in twenty misses the truth.

**16.** Strong: "Start from what the team is trying to achieve, then a handful of KPIs: tickets opened and closed, time to first response and to resolution (the median and the 90th percentile, not only the mean), the age of the open backlog, and customer satisfaction. One headline row, trends underneath, and a breakdown by channel or category." Extra points: **[+Clarify]** who looks at it, and what do they decide from it?; **[+Edge cases]** speed can be gamed by closing tickets too early, so pair it with the reopen rate (Chapter 23, section 23.12).

**17.** Strong: "Ask what decision the report is for. Show them, with the numbers side by side, why the requested version would mislead, and offer a version that answers their real question. If they still want it, label it clearly and put my concern in writing (Chapter 24, section 24.8)." Extra points: **[+Business]** name the decision that could go wrong and what it could cost; **[+Close]** agree the next step out loud.

**18.** Strong: "Score each request on value (which decision it feeds, how many people use it, how often), effort, and urgency; build the high-value, low-effort ones first; and agree the order with the people asking rather than deciding alone (Chapter 25, section 25.12)." Extra points: **[+Clarify]** turn each ask into its question first (Chapter 24, section 24.1): several requests often turn out to be the same question, or one an existing report already answers.

**19.** Strong: "Hand over a short written guide: what the report answers and for whom, where the data comes from, how and when it runs, the known quirks and checks, and who to ask. Then run it together once, and let them run it next time while I watch (Chapter 20, section 20.13)." Extra points: **[+Validate]** they run it alone and match the last output exactly; **[+Scale]** keep it in a repository a stranger can run (Chapter 26, section 26.9).

**20. A time you disagreed** *(worked in full)*

Use your own story; the one below only shows the shape.

- **Passes:** "My manager wanted a different approach from mine. I explained my view, and in the end we went with theirs." True, but vague: no specifics, no result.
- **Strong:** "In my last job, my manager wanted the monthly sales report to count cancelled orders as revenue, because that's what the order system showed. I disagreed, because finance left them out and the two reports never matched. I showed both totals side by side with the cancelled orders listed, and we agreed to report revenue without them and add a footnote. From then on, the two reports matched."
- **Extra points:**
  - **[+Signpost]** "I'll give you the situation, what I did, and how it turned out."
  - **[+Evidence]** Real, specific details: the report, the two totals, and what you did yourself, not what "we" did.
  - **[+Business]** Say what changed because of it: the reports matched, and the monthly argument about which number is right stopped.
  - **[+Close]** "So: I disagreed with evidence rather than opinion, and I'd do it the same way again, though next time I'd raise it before the report went out, not after."

Chapter 81 turns this shape into the STAR method and works this same question in full.

---

## Where this leads

- **Chapters 70–82**, every bank in this part, write their core-question model answers against this chapter's rubric and label moves with the twelve tags introduced here.
- **Chapter 68, How Data Hiring Works**, covers what happens before you're in the room (screening, portfolios, referrals), which this chapter doesn't touch.
- **Chapter 82, Take-Home Assignments & Mock Interviews**, is where you apply this chapter under realistic time pressure, end to end.
