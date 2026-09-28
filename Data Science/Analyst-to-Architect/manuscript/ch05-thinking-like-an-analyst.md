# Chapter 5. Thinking Like an Analyst

*Part 0 — First Principles: Data from Zero*

> **Chapter at a glance**
>
> **You will learn to:** ask the questions that turn a request into useful analysis · rewrite a vague request as a precise question tied to a decision · write hypotheses that data can prove wrong · break a problem into an issue tree whose branches are MECE (no overlaps, no gaps) · tell facts from opinions and assumptions · check a claim or chart before believing it, including correlation that isn't causation · recognize the biases that bend how people read data, including your own · structure a decision so that data can inform it.
>
> **Before you start:** Chapter 1 (the data-to-insight ladder), Chapter 3 (booked, billed, and collected), and Chapter 4 (percentages, averages, and small numbers).
>
> **Time needed:** 3–4 hours, including the exercises and the project.
>
> **Tools:** a pen and paper, or a whiteboard. Issue trees are easiest to draw by hand first.
>
> **Practice data:** Riverstone's first quarter of 2026 (the mini database) for the worked example, and its 2025 CRM leads (the one-year database) for the story. Every number was checked by script.

---

## Why this matters

Two analysts get the same message from the Sales Head: *"March was terrible. Can you look into it?"*

The first opens the database, pulls every number about March, builds twelve charts, and sends a 15-slide deck two days later. It's accurate. Nobody knows what to do with it.

The second replies with one question: *"Do you mean billed revenue, and is this for the plan you're making with the team next week?"* Then she lists five possible reasons revenue could have fallen, checks each against the data in an afternoon, rules out three, and sends a half-page note: *"Most of the fall is three customers who ordered in February and not in March. All three owe us money. I'd call them before offering anything."*

Both know the same tools. The second knows how to **think about the problem before touching the data**, and that's what separates analysts people ask for by name from analysts who produce reports.

It's a method, not a talent: ask what the question is for, list the possible answers before looking, break the problem into pieces that don't overlap, test each piece, and notice when your own expectations are steering you. Every later chapter gives you a new tool. This chapter decides whether you point it at the right thing.

---

## In plain English

Think about a good doctor.

You walk in and say, *"I feel terrible."* A bad doctor prescribes something for "feeling terrible". A good doctor asks questions. *Since when? Where does it hurt? Any fever? Did you eat anything unusual?* In their head, they're listing possible causes and ruling them out one by one. Only then do they decide on treatment, and they tell you what to watch for in case they're wrong.

An analyst does the same thing with a business problem:

- **"I feel terrible"** is the vague request: *"Sales are down."*
- **The doctor's questions** turn it into a precise question: *which sales, compared with when, and what are you trying to decide?*
- **The list of possible causes** is a set of hypotheses, organized into an issue tree.
- **The tests** are queries, counts, and comparisons.
- **The diagnosis and treatment** are the conclusion and the recommendation.

A doctor who orders every test on every patient isn't thorough; they're lost. The same is true of an analyst who pulls every number.

---

## 5.1 Curiosity and asking good questions

### Four kinds of question

Chapter 1 (section 1.2) introduced the ladder from data to insight. Business questions climb the same ladder, and knowing which rung a question is on tells you what kind of work it needs.

| Kind | The question | Riverstone example | What it needs |
|---|---|---|---|
| **Descriptive** | What happened? | *What was billed revenue in March 2026?* | Counting and summarizing |
| **Diagnostic** | Why did it happen? | *Why did March fall 80.3% from February?* | Breaking down, comparing, testing hypotheses (this chapter) |
| **Predictive** | What will happen? | *What will April's revenue be?* | Patterns over time and models |
| **Prescriptive** | What should we do? | *Should sales offer a discount to customers who didn't reorder?* | Options, criteria, and judgment (section 5.8) |

Most requests arrive as descriptive questions but are really diagnostic or prescriptive underneath. *"What was March revenue?"* usually means *"Is March a problem, and what should we do about it?"* Answering only the surface question is the most common way to do correct work that doesn't help.

### The habit questions

Keep these in your head, or on a card next to your screen:

1. **What is this for?** What decision will the answer inform, and who makes it?
2. **Of what?** What exactly is being counted or measured? (Chapter 4)
3. **Compared with what?** Last month, last year, the target, another group? (Chapter 4)
4. **How do we know?** Where does the number come from, and can we trust it? (Chapter 1)
5. **So what?** If the answer is X, what changes? If nothing changes whatever the answer, why are we asking?
6. **What else could explain it?** Before accepting the first explanation, name at least one other.

The last one is the one people skip, and it catches the most mistakes.

---

## 5.2 From a vague request to a precise question

Real requests are almost always vague, because the people asking are busy and know what they mean. Your first job is to turn the request into a question precise enough that two analysts would answer it the same way.

![A vague request, "Sales are down. Find out why.", passes through five checks (metric and definition, period and comparison, scope, decision it serves, deadline and precision) and becomes a precise question about March 2026 billed revenue](figures/fig5-1-vague-to-precise-question.svg)

*Figure 5.1 — Five checks turn a vague request into a question with one answer.*

A precise question pins down five things:

1. **The metric and its definition.** "Sales" could be booked, billed, or collected (Chapter 3). Name one.
2. **The period and the comparison.** March 2026 compared with February? With January? With the quarter's average? Each gives a different story: March was 80.3% below February, 69.5% below January, and 68.0% below the quarter's monthly average of ₹99,237.
3. **The scope.** All customers? One segment? Including the pending order or not?
4. **The decision it serves.** *"What should the sales team do in the first week of April?"* needs a different depth from *"What do we tell the board?"*
5. **The deadline and precision.** An answer by Wednesday to the nearest ₹1,000 is a different job from a perfect answer next month.

You don't always need to ask all five. Often you can choose sensibly, state it, and let the requester correct you: *"I'm reading 'sales' as billed revenue and comparing March with February; tell me if you meant something else."* That one sentence prevents most wasted work.

### Chapter 3's question, made precise

In Chapter 3's story, the managing director asked, *"Which one is right? And why did we collect nothing?"* about January. Meera's first move was to turn "January sales" into three precise questions: *What was booked in January? What was billed? What was collected?* Once the questions were precise, the "disagreement" disappeared, because the two reports were answering different ones. **A surprising number of business arguments are two people answering different questions with correct numbers.**

> **Try it.** Take this request from a store manager: *"Our customers aren't happy. Can you check?"* Write down three different precise questions it could mean, each with a metric, a period, and a comparison.

---

## 5.3 Hypotheses: possible answers you can test

A **hypothesis** is a possible answer to a question, stated clearly enough that data could show it's wrong. It's a guess with a test attached.

For *"Why did March 2026 billed revenue fall 80.3% from February?"* here are some hypotheses:

- **H1.** Fewer customers placed orders in March.
- **H2.** Customers placed orders of the same number but smaller size.
- **H3.** Orders were placed in March but haven't been invoiced yet.
- **H4.** Wholesale customers, who place the largest orders, didn't order in March.
- **H5.** March is always a slow month for this business.
- **H6.** A competitor cut prices and took our customers.

### What makes a hypothesis useful

| Weak | Strong | Why the strong one is better |
|---|---|---|
| "Something happened with customers." | "Customers who ordered in February didn't order in March." | It says which customers and what they did, so you can check it. |
| "Pricing is a problem." | "Customers who didn't reorder were offered smaller discounts than those who did." | It points to specific data (discounts by customer) that could prove it wrong. |
| "The market is tough." | "March is always slow: March revenue is lower than February in previous years too." | It names the evidence: March in earlier years. |

A strong hypothesis is **specific** (who, what, when), **testable** with data you have or could get, and **falsifiable**: you can say in advance what result would prove it wrong. "The market is tough" can't be proved wrong by any number, which is exactly why people like saying it.

### Write them down before you look

**List your hypotheses before you open the data.** If you look first, you'll find a pattern, build a story around it, and stop looking. Writing them first makes you check the ones you didn't expect, and records what you ruled out, which is often as valuable as what you found.

Some hypotheses can't be tested with the data you have. H5 needs March in earlier years, and the mini database only holds the first quarter of 2026. H6 needs information about competitors that no Riverstone table contains. Say so plainly, and name what would test them (last year's data from the ERP; a conversation with customers). **"This data can't answer that" is a legitimate finding.**

![A loop of six steps: question, hypotheses, data needed, test, conclude, act or ask](figures/fig5-2-hypothesis-loop.svg)

*Figure 5.2 — The hypothesis loop. Most loops end with a better question, which starts the next loop.*

Every analysis in this book follows the loop in Figure 5.2, whether the test is a pivot table, a SQL query, or a machine learning model.

---
## 5.4 Breaking problems down: issue trees and MECE

A list of six hypotheses is a start. But lists get long, overlap, and miss things. An **issue tree** organizes a question into branches, each branch into smaller branches, until every leaf is small enough to check with one piece of data.

### MECE: no overlaps, no gaps

The branches of a good tree are **MECE** (pronounced "mee-see"): **mutually exclusive** (no two branches cover the same thing) and **collectively exhaustive** (together they cover everything). The term comes from management consulting, but the idea is plain logic.

![Two ways to split Riverstone's eight customers: "big, in Mumbai, new in 2026" overlaps and leaves Patel Kitchenware out; "retail, wholesale, hospitality" puts every customer in exactly one group](figures/fig5-3-mece-bad-and-good-splits.svg)

*Figure 5.3 — The left split double-counts two customers and misses one. The right split is MECE.*

In Figure 5.3, splitting customers into "big", "in Mumbai", and "new in 2026" puts Metro Mart and Northgate in two groups each and Patel Kitchenware in none, so group totals won't match the company's revenue, and a conclusion like "the problem is new customers" might really be about Mumbai. Split by segment instead, and every customer sits in exactly one group.

Four reliable ways to get MECE branches:

| Split by | Example | Why it's MECE |
|---|---|---|
| **A formula** | billed revenue = number of invoiced orders × average order value | math can't overlap or leave gaps |
| **A category with one value per record** | segment, product category, region | each customer or product has exactly one |
| **A process** | lead → quote → order → invoice → payment (Chapter 3) | each step follows the last |
| **Opposites** | inside our control / outside it; new customers / existing | "not A" covers everything that isn't A |

Splits like "people, process, technology" feel MECE but usually overlap. When in doubt, use a formula or a single-valued category.

### Working through March

Here is the question from section 5.2, answered with an issue tree. All the numbers come from the mini database.

![An issue tree for why March 2026 billed revenue fell 80.3%: fewer invoiced orders (main cause), smaller orders (contributes), and timing or season (partly), with second-level branches for which customers stopped, overdue balances, wholesale mix, the pending order, and seasonality](figures/fig5-4-issue-tree-march-revenue.svg)

*Figure 5.4 — The March issue tree, with what the data says about each branch.*

**Step 1. Split with a formula.** Billed revenue = number of invoiced orders × average invoiced order value.

| | Invoiced orders | Average order value | Billed revenue |
|---|---|---|---|
| February 2026 | 5 | ₹32,340 | ₹161,700 |
| March 2026 | 2 | ₹15,900 | ₹31,800 |

*Source: Mini database (Jan–Mar 2026).*

Both parts fell. How much of the ₹129,900 fall does each explain? If March had kept February's average order value, 2 orders would have brought ₹64,680. So the drop in the **number** of orders accounts for ₹161,700 − ₹64,680 = **₹97,020** (74.7% of the fall), and the smaller **size** of March's orders accounts for the remaining ₹64,680 − ₹31,800 = **₹32,880** (25.3%). ✓ ₹97,020 + ₹32,880 = ₹129,900.

> **Simplification note.** The shares depend slightly on whether you change count or size first; the ranking doesn't.

**Step 2. Fewer orders: which customers?** Five customers had orders invoiced in February: Sharma Hardware, Metro Mart, Coastal Foods, Sunrise Caterers, and Northgate Distributors. In March, only Sharma Hardware and Green Leaf Hotels were invoiced. Metro Mart ordered in March, but its order is still pending. So three customers ordered in February and not at all in March: **Coastal Foods, Sunrise Caterers, and Northgate Distributors**.

Is that unusual? Coastal Foods ordered on 9 January and 11 February, 33 days apart; by 31 March it's been 48 days. Worth noticing, though two orders are a thin pattern (Chapter 4).

**Step 3. Timing: is something stuck?** Order 5012 from Metro Mart, worth ₹26,220, was placed on 15 March and is still *Pending*. It's booked, not billed. With it, March would be ₹58,020, still 64.1% below February. **H3 is true but explains only a part.**

**Step 4. Smaller orders: the mix.** February's two wholesale orders (Coastal Foods ₹32,625 and Northgate ₹76,560) were ₹109,185, or 67.5% of February's billed revenue. No wholesale customer ordered in March. Wholesale orders are the largest, so losing them shrinks both the count and the average. **H4 is supported.**

**Step 5. Why didn't they reorder?** The ERP's orders can't answer "why", but the invoices and payments can add a clue. On 31 March:

| Customer | Ordered in March? | Owed | Overdue |
|---|---|---|---|
| Northgate Distributors | no | ₹46,560 | ₹46,560 |
| Sunrise Caterers | no | ₹23,325 | ₹23,325 |
| Coastal Foods | no | ₹12,625 | ₹12,625 |
| Patel Kitchenware | no (last order in January) | ₹6,250 | ₹6,250 |
| Sharma Hardware | yes | ₹11,700 | ₹0 (not yet due) |
| Green Leaf Hotels | yes | ₹0 | ₹0 |
| Metro Mart | yes (pending) | ₹0 | ₹0 |

*Source: Mini database (Jan–Mar 2026).*

Every customer with an overdue balance placed no order in March, and no customer who ordered in March had anything overdue. The three customers from step 2 owe ₹82,510 between them, all of it overdue.

That's a striking pattern, and it's exactly the moment to slow down. It doesn't say *which way* the connection runs, or whether there is one. A customer short of cash might stop ordering until it pays. A customer unhappy with a delivery might both withhold payment and stop ordering, so a single cause would explain both (section 5.6). Or, with seven customers, it could be coincidence. One detail points to a specific question: Northgate's February order still shows *Shipped*, not *Delivered*. If the crates never arrived, Northgate isn't a late payer; it's a customer waiting for its goods.

This branch ends as a **hypothesis to test outside the data**: a phone call to each of the three customers, and a check of the delivery records for Northgate.

**Step 6. The branches the data can't reach.** H5 (March is always slow) needs last year's March, which isn't in the mini database. H6 (a competitor) needs information from customers. Both go on the list of open questions, not in the conclusion.

**What to tell Anita.** A good answer is short, ranked, and honest about confidence:

> *"March billed revenue was ₹31,800, down 80.3% from February. About three-quarters of the fall is fewer orders: Coastal Foods, Sunrise Caterers, and Northgate didn't reorder in March, and February's two wholesale orders alone were 67.5% of that month. Metro Mart's ₹26,220 order is still pending; shipping it brings March to ₹58,020. All three customers who didn't reorder have overdue balances (₹82,510 in total), and Northgate's order still shows as not delivered. I'd call all three this week, starting with Northgate, before offering any discounts. I can't tell yet whether March is seasonally slow; that needs last year's data."*

---

## 5.5 Fact, opinion, and assumption

Meetings mix three kinds of statement, often in the same sentence. Separating them is one of the quickest ways to make a discussion productive.

- A **fact** is a statement that can be checked against a record, and has been. *"March billed revenue was ₹31,800."* (It still depends on a definition, so a good fact states it.)
- An **opinion** is a judgment. It may be wise, but it isn't checkable as stated. *"Northgate is a difficult customer."*
- An **assumption** is something treated as true without checking, usually because checking is hard or slow. *"Northgate will pay next week."*

Here are statements from Riverstone's Monday sales review, sorted:

| Statement | Type | What to do with it |
|---|---|---|
| "March billed revenue was ₹31,800." | fact | Use it, with its definition. |
| "Coastal Foods orders about once a month." | a claim from very little data | Treat as a hypothesis: two orders, one gap of 33 days. |
| "Our prices are too high for wholesalers." | opinion | Turn it into a testable hypothesis: *wholesale customers who didn't reorder were quoted higher prices than those who did.* |
| "Northgate will pay next week." | assumption | Write it down, give it an owner, and check it by a date. |
| "Northgate is a difficult customer." | opinion | Ask what experience it's based on; check the delivery status first. |

*Source: Mini database (Jan–Mar 2026).*

Businesses run on opinions and assumptions, because there's never time to check everything. The danger is when they're **presented as facts**, or an old assumption quietly becomes "what we know". List your assumptions in one place, so anyone can challenge them.

---

## 5.6 Checking claims and charts

Chapter 4 (section 4.10) covered number tricks. This section is about the reasoning behind a claim. Before accepting one, from anyone including yourself, ask five questions:

1. **Who says so, and how do they know?** A measured count, a survey, a guess, or an anecdote?
2. **Compared with what?** A number with no comparison can't be "high" or "low".
3. **How many cases, and which ones?** Five customers or five thousand? Chosen how?
4. **What's the mechanism?** Is there a believable reason why A would cause B?
5. **What else could explain it?** Chance, reverse causation, a common cause, or selection.

**Correlation is not causation.** Two things that move together are **correlated**. That doesn't mean one causes the other. There are three common alternatives:

- **Reverse causation: B causes A.** *"Order lines with bigger discounts are bigger lines, so discounts make customers buy more."* In the mini database, the four order lines worth ₹20,000 or more had an average discount of 10.5%; the other fifteen averaged 1.67%. But Riverstone's own rules (Chapter 3, section 3.6) give larger discounts to larger orders. The size comes first; the discount follows. The data can't show that discounts grow orders.
- **A common cause: C causes both.** In section 5.4, overdue balances and missing reorders went together. A delivery problem could cause both: the customer won't pay for goods it hasn't received, and won't reorder either. Chasing payment harder would then make things worse.
- **Selection: the cases were chosen in a way that creates the pattern.** *"Customers who attend our trade fair order more."* Maybe the ones who attend were already the most engaged customers.

And sometimes it's **chance**: with seven customers, patterns appear by accident. Chapter 22 shows how to judge whether a pattern is bigger than chance.

> **Watch out: your own analysis is a claim too.** The five questions apply to what you're about to send. The note to Anita in section 5.4 states a measured fact ("about three-quarters of the fall is fewer orders") and a recommendation ("I'd call them"), but it's careful not to say "customers stopped ordering *because* they owe us money".

---

## 5.7 Bias in how we see data

A **cognitive bias** is a predictable way in which people's judgment drifts from the evidence. Everyone has them, including experienced analysts. You can't switch them off, but you can recognize the common ones and build habits that catch them.

| Bias | What it looks like at Riverstone | Antidote |
|---|---|---|
| **Confirmation bias**: noticing evidence that fits what you already believe | Vikram is sure a competitor is undercutting prices, so he asks for lost deals that mention price, and not for the ones that don't | Write hypotheses first (section 5.3); look for evidence that would prove your favorite wrong |
| **Anchoring**: judging a number against the first number you saw | March looks like a disaster against February's ₹161,700. But February was unusual: Northgate's first order alone was ₹76,560, 47.3% of the month. Against the quarter's monthly average of ₹99,237, March is still weak, but the comparison is fairer | Compare against several baselines: the previous month, the average, the same month last year, the target |
| **Regression to the mean**: an unusually high or low value tends to be followed by a more ordinary one | A month boosted by one big first order is likely to be followed by a lower month, even if nothing went wrong | Before explaining a change, ask whether the starting point was unusual |
| **Survivorship bias**: studying only the cases that made it through | Studying won deals to learn "what works", without looking at the lost and never-contacted leads that went through the same steps | Always include the cases that dropped out |
| **Availability and recency**: overweighting what's vivid or recent | One angry phone call from a customer on Friday becomes "customers are unhappy" on Monday | Count: how many complaints, out of how many customers, over what period? |
| **Small numbers**: trusting patterns from very few cases | "All the customers who owe us stopped ordering" is based on four customers | Give the counts; call it a hypothesis until more cases agree (Chapter 4, section 4.8) |
| **The analyst's own bias**: wanting an interesting finding | A clean story about overdue balances is more exciting than "one big order made February unusual", so it's tempting to lead with it | State the ordinary explanation first if it's the bigger one |

*Source for the Riverstone numbers: Mini database (Jan–Mar 2026).*

The last row matters most. Analysts are rewarded for insights, so there's a pull toward the surprising story; a good reputation rests on being right, which often means reporting the ordinary explanation clearly.

---

## 5.8 Deciding with data

Analysis exists to help someone decide. Data rarely decides by itself; it narrows the options, estimates consequences, and shows where the uncertainty is.

| Part | Question | For the three customers who didn't reorder |
|---|---|---|
| **Decision** | What exactly is being decided, and by whom? | What sales does about Coastal Foods, Sunrise Caterers, and Northgate this week (Anita decides) |
| **Options** | What are the choices, including doing nothing? | A. Wait. B. Call each customer to ask why, and check Northgate's delivery. C. Offer 5% off their next order. D. Put overdue accounts on hold until they pay. |
| **Criteria** | What matters in choosing? | Revenue, margin, cash owed, the customer relationship |
| **Evidence** | What does the data say about each option? | All three owe ₹82,510, all overdue. Northgate's order isn't marked delivered. A 5% discount on an Industrial Crate cuts its margin from 24.1% to 20.1%. |
| **Reversibility** | How costly is it to be wrong? | A call is cheap and can't do much harm. A discount sets a price expectation that's hard to take back. A hold could lose a customer whose goods never arrived. |
| **Recommendation and confidence** | What should we do, and how sure are we? | B this week; decide on C or D after the calls. Medium confidence: the pattern is clear, but it's four customers and the cause is unknown. |
| **What would change my mind** | Which new fact would change the recommendation? | If customers say price is the reason and their balances are paid, reconsider C. If goods weren't delivered, fix the delivery before anything else. |

*Source: Mini database (Jan–Mar 2026).*

Three principles sit behind the table:

- **Match the effort to the decision.** A reversible, cheap decision (a phone call) needs less evidence than an irreversible, expensive one (a price change or a hire).
- **Include "do nothing".** It's often the real alternative, and it has costs too.
- **Say what would change your mind.** It shows where the uncertainty is and what to watch.

> **Interview extra point.** In a case interview or a take-home question ("Revenue fell 20%. Why?"), don't start calculating. Spend the first minute restating the question precisely, then sketch a MECE split out loud (for example, number of orders × average order value, then by segment), and say which branch you'd check first and why. Interviewers are grading the structure of your thinking more than the final number. Chapter 75 (product sense, metrics, and case studies) and Chapter 76 (the Business Analyst question bank) have practice cases with model answers.

---
## Common mistakes and how to spot them

| Mistake | Symptom | Fix |
|---|---|---|
| Answering the surface question | correct numbers nobody can act on | Ask what the answer is for, and who decides |
| Starting with the data instead of the question | a pile of charts and no conclusion | Write the precise question and hypotheses first |
| Hypotheses that can't be wrong | "the market is tough" survives any evidence | Make each one specific, testable, and falsifiable |
| Branches that overlap or leave gaps | group totals don't add up to the whole | Split by a formula, a single-valued category, or a process |
| Stopping at the first explanation | a confident story that's partly true | Name at least one other explanation and check it |
| Reading correlation as causation | "discounts make customers buy more" | Check reverse causation, common causes, selection, chance |
| Comparing against one unusual baseline | a normal month looks like a disaster | Use several baselines: average, target, same month last year |
| Over-analyzing a small, reversible decision | a week spent on something a phone call would settle | Match the effort to the cost of being wrong |

---

## In the real world: do we need another sales executive?

It's the first week of January 2026. Vikram Singh, the Sales Manager, has asked the managing director for a fourth sales executive. His reason: *"Leads are piling up. The CRM shows 43 enquiries last year, and my team can't keep up."* The MD forwards it to Anita with one line: *"Is this right?"* Anita asks Meera Iyer to look before Friday.

**1. What's the decision, and what's the precise question?** The decision is whether to hire. The question underneath: *"Did Riverstone lose new business in 2025 because the sales team didn't have time to handle its leads?"* A hire fixes capacity, not a slow process, poor routing, or poor leads, so the question must separate those.

**2. The issue tree**, following the lead's journey:

- **Too many leads?** How many real enquiries arrived, per executive?
- **Leads missed or handled slowly?** How many were never contacted, and how long did first contact take?
- **Leads contacted but lost?** What share of contacted leads were won?
- **Capacity or something else?** If the team is too busy, the busiest people should be the ones missing leads.

**3. The tests.** All from the one-year database.

- **Volume.** The 43 rows include duplicates: the same enquiry submitted two or three times. There were **30 real enquiries** in the year, about 2.5 a month, or fewer than one a month per sales executive. "Piling up" isn't about volume.
- **Missed and slow.** **8 of the 30 (26.7%) were never contacted at all.** The other 22 waited an average of **9.7 days** for a first contact. One referral, Tulip Mart, has been waiting since 23 September, 99 days.
- **Lost after contact.** 6 of the 22 contacted leads were won (27.3%). Of the leads contacted within a week, 3 of 8 were won; of those contacted later, 3 of 14. That fits "faster is better", but with numbers this small it's a hypothesis, not a finding.
- **Capacity.** If the team were overloaded, the executives handling the most customer orders should miss the most leads. The data says the opposite:

| Sales executive | Orders handled in 2025 | Leads assigned | Never contacted | Average days to first contact |
|---|---|---|---|---|
| Farah Khan | 64 | 5 | 0 | 7.7 |
| Rahul Mehta | 53 | 10 | 3 | 10.9 |
| Neha Kulkarni | 46 | 15 | 5 | 9.8 |

*Source: One-year database (2025 CRM leads).*

Farah, with the most orders, missed none of her leads. Neha, with the fewest orders, was assigned half of all leads, including 9 of the 14 website enquiries, and missed 5. Website leads were the most often missed: 5 of 14 were never contacted.

**4. Checking herself.** The CRM doesn't record time spent on visits, calls, or complaints, so orders aren't the whole workload. And reading the table as "Neha is the problem" would be unfair: she got as many leads as Rahul and Farah combined, including most website enquiries. The pattern points at **how leads are routed and followed up**, not at a person.

**5. The recommendation.** She sends Anita a half-page note:

> *"The data doesn't support hiring for lead volume: 30 real enquiries came in last year (the CRM's 43 includes duplicates), fewer than one a month per executive. The problem is follow-up: 8 enquiries were never contacted and the rest waited almost 10 days on average. Missed leads are concentrated among website enquiries and in the largest lead list, not with the busiest executive. I'd (1) call the 8 uncontacted leads this week, starting with the Tulip Mart referral, (2) spread website leads evenly, (3) set a two-working-day rule for first contact with a daily reminder, and (4) fix the duplicate website submissions. What would change my mind: if leads grow sharply, or if response times are still slow after a quarter of the new routing, a hire is worth revisiting. The CRM doesn't record time spent, so I can't rule out that the team is busy with work outside orders and leads."*

Anita forwards it to the MD and Vikram. Vikram's first reaction is irritation. His second, after reading the table, is to ask Meera how to set up the daily reminder (you'll build that reminder yourself later in the book).

The request was a solution ("hire"). Meera turned it into a question about a cause, tested each branch, avoided blaming one person, stated what she couldn't see, and recommended cheap, reversible steps first, with a clear condition for revisiting the expensive one.

---

## Tools

- **Pen and paper, or a whiteboard.** Issue trees are fastest by hand. Draw the first version in five minutes; tidy it later.
- **A spreadsheet or document** for the hypothesis log: one row per hypothesis, with the data needed, the result, and the status (supported, rejected, open).
- **A diagram tool** (optional): diagrams.net, PowerPoint, or Google Slides for sharing a tree.
- **SQL and spreadsheets** for the tests, from Chapter 10 onward. This chapter's numbers came from short queries on the Riverstone databases.

---

## The project: an issue tree for a real question

**Goal:** take one real business question, make it precise, and build an issue tree that shows exactly which data would answer each branch.

**Step 1. Choose a question** from your work, a local business, or your Chapter 4 project: turn one checked claim into an analyst's question. *"Sales up 40% in three years"* becomes *"Did the company's revenue grow faster than its market over those three years, and where did the growth come from?"*

**Step 2. Make it precise.** Write the metric and its definition, the period and the comparison, the scope, the decision it serves, and the deadline (section 5.2).

**Step 3. Write at least five hypotheses** before looking at any data. Make each specific and testable (section 5.3).

**Step 4. Build the tree** two or three levels deep, starting with a MECE split (section 5.4). Check each split for overlaps and gaps.

**Step 5. Add the data to every leaf.** For each leaf, write:

| Column | What to write |
|---|---|
| `branch` | the leaf's question |
| `hypothesis` | what you expect, stated so it could be wrong |
| `data_needed` | the table, file, report, or conversation that would test it |
| `available` | yes, no, or "needs to be collected" |
| `test` | the count, comparison, or query you'd run |
| `result_that_rejects_it` | what you'd have to see to drop this branch |

**Step 6. Label facts, opinions, and assumptions** in anything the question's owner has said about it.

**Step 7. Name one bias** that could affect this analysis (yours or the requester's), and how you'll guard against it.

**Deliverable:** the precise question, the tree, the data table, and a three-sentence plan for which branch you'd test first and why. If you have access to the data, test one branch and write a half-page note like Meera's.

---

## You've got it when…

- [ ] I ask what an analysis is for before I start it.
- [ ] I can turn a vague request into a precise question with a metric, period, comparison, scope, and decision.
- [ ] I write hypotheses before looking at the data, and each one could be proved wrong.
- [ ] I can build an issue tree with MECE branches, and I know four reliable ways to split.
- [ ] I label statements as fact, opinion, or assumption.
- [ ] I check claims for reverse causation, common causes, selection, and chance.
- [ ] I can name the common biases and the habit that counters each one.
- [ ] I can structure a decision with options, criteria, evidence, reversibility, confidence, and what would change my mind.
- [ ] I've built an issue tree for a real question, with the data for every branch.

---

## Recap

- Questions are **descriptive, diagnostic, predictive, or prescriptive**. Most requests are diagnostic or prescriptive underneath.
- Keep asking: *what is this for? of what? compared with what? how do we know? so what? what else could explain it?*
- A **precise question** pins down the metric, the period and comparison, the scope, the decision it serves, and the deadline.
- A **hypothesis** is a possible answer that data could prove wrong. **Write hypotheses before you look.** "This data can't answer that" is a legitimate finding.
- An **issue tree** breaks a question into branches until each leaf can be tested. Branches should be **MECE**: no overlaps, no gaps. Split by a formula, a single-valued category, a process, or opposites.
- March 2026's 80.3% fall split into **fewer orders (₹97,020)** and **smaller orders (₹32,880)**, then into three customers who didn't reorder, the missing wholesale orders, and a pending order, ending in a hypothesis to test by phone.
- Separate **facts, opinions, and assumptions**, and list assumptions where everyone can see them.
- **Correlation isn't causation.** Check for reverse causation, a common cause, selection, and chance.
- **Biases** (confirmation, anchoring, regression to the mean, survivorship, availability, small numbers, and the analyst's own) bend everyone's judgment; counter them with habits.
- **Decide with data** by laying out options (including doing nothing), criteria, evidence, reversibility, a recommendation with confidence, and what would change your mind.

---

## Practice exercises

### Warm-up

1. Label each question as descriptive, diagnostic, predictive, or prescriptive: (a) *How many orders did Sunrise Caterers place in February?* (b) *Should we stop offering 12% discounts?* (c) *Why did Kitchen revenue grow every quarter of 2025?* (d) *How much will we collect in April?* (e) *Which customers owe us money?*
2. Label each statement as fact, opinion, or assumption, and say what you'd do with it: (a) "Invoice 9007 hasn't been paid." (b) "Sunrise Caterers is a bad customer." (c) "The new price list will be ready by Monday." (d) "Hotels don't care about price." (e) "Blue Bay Cafe signed up on 1 March 2026."
3. Is each split MECE? If not, say whether it overlaps, leaves gaps, or both. (a) Orders: Pending, Shipped, Delivered, Cancelled. (b) Customers: large, loyal, new. (c) Revenue: Storage, Kitchen, Industrial, Furniture. (d) Reasons for a late delivery: warehouse delay, truck problem, customer not available, bad weather. (e) Leads: from the website, from referrals, from Mumbai.
4. Rewrite each vague request as a precise question with a metric, period, comparison, and the decision it might serve: (a) "How are we doing with hotels?" (b) "Is the website worth it?" (c) "Check if customers are paying on time."

### Core

5. For the question *"Why did hospitality customers bring in less revenue in March 2026 than in February?"*, write three hypotheses that data could prove wrong, and for each, name the data you'd use. (Hospitality billed ₹23,325 in February and ₹20,100 in March in the mini database.)
6. Billed revenue rose from ₹104,210 in January 2026 (3 invoiced orders) to ₹161,700 in February (5 invoiced orders). (a) Calculate each month's average invoiced order value. (b) Split the ₹57,490 increase into the part from more orders (holding January's average order value) and the part from the change in order size. (c) Which explains more?
7. Chapter 3 showed that Riverstone collected ₹197,250 of ₹297,710 billed in the first quarter of 2026 (66.3%). Build a two-level MECE issue tree for *"Why did we collect only two-thirds of what we billed?"* For each leaf, name the data that would test it.
8. Name the bias in each situation and suggest one habit that would counter it: (a) After one customer complains about a cracked crate, a manager says, "Our quality has slipped." (b) An analyst studies the five best customers to learn why customers stay. (c) Revenue drops after a record month, and the team spends a week looking for what went wrong. (d) A manager who wanted a new CRM highlights only the figures that make the old one look bad.
9. A manager says: *"Customers with overdue balances order less. So chasing payments hurts sales, and finance should send fewer reminders."* Give three other explanations for the pattern, and describe what data would help decide between them.

### Stretch

10. Using the table from the story: Farah handled 64 orders and missed none of her 5 leads; Neha handled 46 orders and missed 5 of her 15. (a) What does this data support? (b) What doesn't it support? (c) What additional data would you want before saying anything about individual performance?
11. In the story, leads contacted within a week were won 3 times out of 8 (37.5%); leads contacted later were won 3 times out of 14 (21.4%). (a) Why isn't this proof that faster contact wins more deals? (b) Name one alternative explanation. (c) How could Riverstone test the idea properly?
12. Blue Bay Cafe signed up on 1 March 2026 and hadn't placed an order by 31 March. Structure the decision *"What should sales do about Blue Bay Cafe?"* using the table in section 5.8: at least three options (including doing nothing), criteria, the evidence you'd look for, reversibility, and what would change your mind.

### Think about it (no calculation needed)

13. When should you stop analyzing and give an answer? Describe two signals that you've done enough, and one signal that you haven't.
14. A senior manager says, "I've already decided to cut the Furniture range. Can you find me some numbers that support it?" How would you respond, and what would you offer to do instead?
15. You ask an AI assistant why March revenue fell, and it gives a fluent, confident explanation. Using this chapter, list three things you'd check before repeating it.

---

## Key terms

descriptive question · diagnostic question · predictive question · prescriptive question · habit questions · precise question · hypothesis · testable · falsifiable · issue tree · MECE · mutually exclusive · collectively exhaustive · decomposition (count × size) · fact · opinion · assumption · claim · correlation · causation · reverse causation · common cause · selection · chance · cognitive bias · confirmation bias · anchoring · regression to the mean · survivorship bias · availability bias · recency · small-numbers bias · decision rights · reversibility · confidence · "what would change my mind"

*(All terms are defined in the Glossary, Appendix A.)*

---

## Where this leads

- **Chapter 6, Planning Your Learning,** turns the book's hours into a plan for your week, and shows which chapter brings each tool you'll use to test hypotheses.
- **Chapters 10–13** give you the tests: spreadsheets and SQL to count, compare, and break down numbers the way section 5.4 did.
- **Chapter 14, Data Cleaning & Preparation,** handles the "is the data even right?" branch that every issue tree should include.
- **Chapter 22, Statistics Without Fooling Yourself,** shows whether a pattern like "3 of 8 versus 3 of 14" is bigger than chance.
- **Chapter 23, Business Acumen, KPIs & Metrics,** builds full KPI trees for Riverstone and diagnoses a revenue dip with more careful breakdowns.
- **Chapter 24, Requirements, Storytelling & Stakeholders,** turns notes like Meera's into memos and presentations, and covers handling "can you find numbers that support this?"
- **Chapters 30 and 31** test cause and effect properly: experiments, and methods for when experiments aren't possible.
- **Chapters 36 and 40** take on predictive questions like *"What will April's revenue be?"*: the machine learning workflow, and forecasting over time.
- **Interview preparation:** case questions ("revenue fell; why?"), structuring, and hypothesis-driven thinking appear in Chapter 75 (product sense, metrics, and case studies) and Chapter 76 (the Business Analyst question bank), with model answers.

---

## Answers to practice exercises

**1.** (a) Descriptive. (b) Prescriptive. (c) Diagnostic. (d) Predictive. (e) Descriptive.

**2.** (a) Fact (checkable in the payments table); use it. (b) Opinion; ask what it's based on and turn it into something checkable, such as "Sunrise pays later than other customers". (c) Assumption (a plan); give it an owner and confirm it. (d) Opinion, and a sweeping one; turn it into a hypothesis, such as "hotel customers accept price increases as often as retailers". (e) Fact (the `signup_date` in the customers table); use it.

**3.** (a) MECE, as long as every order has exactly one of these four statuses. (b) Not MECE: it overlaps (a new customer can be large; a large customer can be loyal) and has gaps (a small, occasional, long-standing customer is none of them). (c) MECE: each product belongs to one category, and the four cover every product. (d) Not MECE: it can overlap (a truck problem caused by bad weather) and has gaps (a wrong address, missing stock, a paperwork delay). Add "other" and define each reason so that one is chosen. (e) Not MECE: "Mumbai" is a location, not a source, so a website lead from Mumbai is in two groups, and leads from trade fairs or cold calls are in none.

**4.** One good version of each: (a) *"What was billed revenue from hospitality customers in the first quarter of 2026, compared with the previous quarter, and which customers drove the change? (For deciding on an April hotel promotion.)"* (b) *"How many 2025 website enquiries became customers, and how much revenue did they bring, compared with referrals and trade fairs? (For next year's website budget.)"* (c) *"What share of first-quarter 2026 invoices were paid by their due date, and which customers are most often late? (For deciding whom finance calls first.)"*

**5.** Examples: (1) *Fewer hospitality customers ordered in March than in February.* Data: orders by customer and month (Sunrise Caterers ordered in February, Green Leaf Hotels in March). (2) *Hospitality customers who ordered placed smaller orders.* Data: order values by customer and month. (3) *The hospitality order that would have made the difference is still pending or was cancelled.* Data: order status for hospitality customers in March. Note that the gap is small (₹3,225) and each month has one order, so almost any difference is normal variation.

**6.** (a) January: ₹104,210 ÷ 3 = **₹34,737**. February: ₹161,700 ÷ 5 = **₹32,340**. (b) Holding January's average order value, 5 orders would bring 5 × ₹34,736.67 = ₹173,683, which is ₹69,473 more than January: that's the **count effect, +₹69,473**. The change in size is 5 × (₹32,340 − ₹34,736.67) = **−₹11,983**. Check: ₹69,473 − ₹11,983 = ₹57,490. ✓ (c) The increase came entirely from **more orders**; the average order actually got a little smaller.

**7.** One good tree:

- **Collected only 66.3% of billings**
  - **Not yet due** (the amount billed recently, within 30-day terms). Data: invoices by due date as of 31 March (invoice 9010's ₹11,700 isn't due until 10 April).
  - **Due but unpaid (overdue)**
    - *Customers can't or won't pay.* Data: overdue by customer; payment history; credit checks.
    - *Customers dispute the invoice.* Data: support tickets, delivery status, proof of delivery.
    - *Riverstone hasn't chased.* Data: reminder logs from finance.
  - **Paid but not recorded yet.** Data: bank statement lines not yet matched to invoices.

The first split (not yet due / overdue / paid but unrecorded) is MECE for the money not collected. From Chapter 3: ₹100,460 is unpaid, of which ₹88,760 is overdue and ₹11,700 is not yet due.

**8.** (a) **Availability** (one vivid complaint). Habit: count complaints over a period, out of how many deliveries. (b) **Survivorship** (studying only customers who stayed). Habit: compare with customers who left. (c) **Regression to the mean** (after a record month, a lower one is normal). Habit: compare with the average and the same month last year before searching for a cause. (d) **Confirmation bias**. Habit: write down in advance what evidence would show the old CRM is fine, and look for it.

**9.** (1) **Common cause**: a delivery or quality problem makes customers both withhold payment and stop ordering. (2) **Reverse causation**: customers who order less have less reason to keep their account current. (3) **Cash-strapped customers** pay late and order less, whatever the reminders. Data that helps: complaints and delivery records for overdue customers; whether ordering fell before or after the balance became overdue; and a few customer conversations.

**10.** (a) Missed leads weren't concentrated with the executive handling the most orders, so "too busy with orders" isn't supported, and lead assignment was very uneven. (b) Nothing about individual effort or ability: the numbers are tiny, Neha got most website leads, and orders aren't all of anyone's work. (c) Time spent on other work, each person's lead sources, how leads were assigned, and absences over the year.

**11.** (a) The counts are very small (6 wins in total), so the difference could well be chance (Chapter 22), and the leads weren't assigned a response time at random. (b) Executives may contact the most promising leads first, such as referrals, so the leads contacted quickly were already more likely to be won (selection, or a common cause: lead quality affects both speed and winning). (c) Run a simple experiment (Chapter 30): for a quarter, randomly assign new leads to "contact within two working days" or "normal process", then compare win rates, or at least compare fast and slow contact within the same lead source.

**12.** **Decision:** what sales does about Blue Bay Cafe in April. **Options:** A. wait; B. call or visit to understand its needs; C. a first-order offer; D. send the catalog and a sample. **Criteria:** chance of a first order, cost, margin, fit. **Evidence:** 30 days since signup without an order; what it enquired about; how long other new customers took (Green Leaf Hotels signed up on 8 January and placed its first order on 20 January). **Reversibility:** a call is cheap; a discount sets an expectation. **Recommendation:** B first, then D if interest is confirmed. **What would change my mind:** a specific, large first order that depends on price would make C worth considering.

**13.** Enough: more precision wouldn't change the decision; the remaining branches can't be answered with available data, and you've said so. Not enough: you can't yet explain most of the change, or the recommendation would flip on a branch you haven't checked.

**14.** Don't cherry-pick; it risks your credibility and the manager's. Offer a fair picture instead: *"I'll look at Furniture's revenue, margin, and trend. If it supports cutting the range, that's a stronger case; if not, better you hear it from me than from the board."* Chapter 24 covers handling this kind of pressure.

**15.** (1) **Are its numbers right?** Check the metric, definition, and figures against the database. (2) **Is it presenting hypotheses as facts?** Order tables can't tell you *why* customers behaved as they did. (3) **What has it left out?** Compare with your own issue tree: timing, mix, and the limits of the data. Chapter 26 covers working with AI assistants.
