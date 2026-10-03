# Selling the books: a strategy, and a red team

*3 October 2026. Written for Abhishek. Every price quoted is sourced and dated, because prices move.*

**The plan, as you have now defined it:** ₹500 for **Book 4, Be Interview Ready, alone**. The other
three volumes land later and cost extra. The course is deferred.

My first draft of this document argued hard against ₹500 — but it was arguing against ₹500 *for all
four books and the Practice Arena*, which is a much weaker plan than the one you are running. With
the interview book alone at that price, **the main objection falls away.** What is below is the red
team for the actual plan.

**The short version.** The structure is right: lead with the interview book, price it to be bought
without thinking, make the volumes the revenue. Two things will decide whether it works, and
neither is price. One is that **you have no audience**, and sales are audience times conversion. The
other is that **the product's one claim over the competition is currently contradicted inside the
product itself.** Fix the second, then spend everything on the first.

---

## 1. What you are selling at ₹500

Measured, not estimated:

| Book 4, Be Interview Ready | |
|---|---|
| Pages | **535** |
| Coded questions in Part VIII | **767** |
| Of those, predict-the-output | **202**, added in the last two days |
| Verified contents links / bookmarks | 169 of 169, 724 of 724 |

The differentiator is not the question count. It is that **every code answer was produced by running
the code.** Not transcribed, not remembered. In the last two days alone a dozen drafted questions
turned out to be wrong and were caught only because they were run — a `RANK` answer that was 4,4,4
rather than 1,1,1, a float-money trap that does not actually fire, a Parquet claim that was
backwards.

That is the moat. Section 3.1 is about how easily it breaks.

---

## 2. The market you are pricing into

Searched 3 October 2026. These are what a buyer compares you against.

| Product | Price | What it is |
|---|---|---|
| [Data Analyst Interview Kit 2026](https://topmate.io/svnk/2033006) (Topmate) | ₹149 | A PDF kit |
| [Data Analyst Interview Kit 2026](https://topmate.io/aasifcodes/2163653) (Topmate) | ₹199 | A PDF kit |
| [400+ Data Analyst Interview Questions](https://topmate.io/analystinterviewprep/2143283) | ₹199 | 400+ questions |
| [Data Analyst Interview Kit 2026](https://topmate.io/prakash_r10/1429388) (Topmate) | ₹399 | A PDF kit |
| **[Cracking The Data Analyst Interview](https://www.amazon.in/Cracking-Data-Analyst-Interview-Situational-ebook/dp/B0CL2R478Y)** (Kindle) | **₹449** | **210 questions** |
| [Data Analyst Interview Q&A eBook](https://www.scholarhat.com/books/data-analyst-interview-questions-and-answers-book-pdf) (ScholarHat) | free | Listed ₹999, given away |
| [Ace the Data Science Interview](https://www.acethedatascienceinterview.com/pdf-download-of-ace-the-data-science-interview-ebook) (Amazon.in) | ₹3,500–5,000 | The premium reference |

**At ₹500 for the interview book alone, you have a clean comparison and you win it:**

> **₹449 buys 210 questions. ₹500 buys 767, and every answer was run.**

That is a sales page headline, and it is true. It needed the clarification to become available —
at ₹500 for 3,472 pages the same claim reads as implausible, because nobody believes that much
verified work costs ₹500. At ₹500 for 535 pages it reads as a good deal, which is what it is.

**The cost of sitting at ₹500.** You are in the commodity band, where buyers do not expect
correctness and will not pay a premium for it. Your best asset is partly wasted at this price. That
is a real trade and I think it is the right one *given no audience*: low friction buys you a list
faster than high margin buys you revenue. But it means **Book 4 is a lead product that pays for
itself, not the business.** The business is the volumes and, later, the course.

---

## 3. The red team

### 3.1 The one claim you are selling on is contradicted inside the book — and both instances are in Book 4

This is the finding that matters, and the clarification makes it **worse**, not better, because
Book 4 is now the entire product.

| Where | What it says |
|---|---|
| **§71.11, SQL — 32 questions** | Run against the chapter's own Riverstone data, but **never on real PostgreSQL 16 or MySQL 8.4.** Outputs are labelled *Run*, not *Verified*. Four questions marked *Dialect split*. |
| **§70.9, Excel — 16 questions** | **Never run in Excel**, because Excel is not installed here. Four carry a *Check in Excel* mark. |

I put those marks there and I stand by the honesty — a reader is told before they rely on it. **But
you cannot run a sales page on "every answer was run" while 48 questions in the product say
otherwise.** One buyer finds one wrong SQL answer, screenshots it, and the single thing you claimed
over the ₹199 kits is gone permanently.

Also open: **46 review findings**, and Book 4's visual check has not been redone since it grew from
400 to 535 pages.

**This is the gate. It is also about a day's work.** Install PostgreSQL and MySQL, run the 32 SQL
questions, run the 16 Excel ones in Excel. Or delete the claim from the marketing. One of the two.

### 3.2 You are deciding price when the constraint is distribution

Sales = audience × conversion. No list, no following, no channel, no placement-cell relationships.
At ₹500 and at ₹5,000 a cold launch sells roughly the same: very little.

₹500 is a sensible decision about a variable that is not currently binding. The binding one is that
nobody knows the book exists.

### 3.3 The arithmetic says ₹500 cannot be the business

Platform economics, searched 3 October 2026:
[Topmate](https://peerseek.io/blogs/creator-platform-fees-india-compared) takes about **12.9%
all-in** including payment processing. [Gumroad](https://ownstreet.in/blog/gumroad-fees-india-2026-guide)
takes 10% + $0.50 direct and **30%** through its marketplace, with PayPal fees on top for Indian
payouts. Razorpay on your own site is roughly 2–3%.

| | Net per sale | Sales for ₹1,00,000 | Sales for ₹5,00,000 |
|---|---|---|---|
| Book 4 at ₹500 (Topmate) | ~₹435 | 230 | **1,150** |
| Book 4 at ₹500 (own site, Razorpay) | ~₹487 | 205 | 1,027 |
| Volumes at ₹2,499 | ~₹2,177 | 46 | 230 |

At a 2% conversion — optimistic cold — 1,150 sales means reaching about **57,000 people**. That is
not a launch, that is a year of audience work.

**Which is the argument for the plan, not against it.** ₹500 is not there to make ₹5,00,000. It is
there to convert attention into a buyer list cheaply, and the volumes do the revenue. Just be
explicit with yourself that that is the design, so you are not disappointed by the first month.

### 3.4 "Volumes cost extra" needs to be on the page before the first sale

You have decided this, which is good. Now publish it.

A buyer who pays ₹500 for the interview book and later discovers the other three cost ₹2,500 will
feel the ₹500 was a tease — **unless they were told on the day they bought.** Two things make it
land well instead of badly:

- **Say it on the sales page**, with the price, even if the volumes do not exist yet.
- **Make Book 4 genuinely complete on its own.** It is: 535 pages, 767 questions, standalone. Say
  that too. The volumes are depth, not the missing half.

The question you have not answered yet: **does the ₹500 buyer get free updates to Book 4?** It will
change — the verification fixes alone will change it. My recommendation is yes, free updates to
Book 4 forever, because it costs you nothing and it is the single easiest trust-builder for a
first product from an unknown publisher.

### 3.5 A ₹500 PDF sets a ceiling you cannot raise

It will be shared. At ₹500 that is survivable and arguably useful early. But **once a free copy is
circulating you cannot raise Book 4's price later**, because the ₹500 version is already the
reference copy. Launching low is a one-way door — fine if you walk through it deliberately.

If you want the option open, launch at ₹500 as a **stated launch price with a published rise date**.
That is honest, it creates urgency, and it preserves the ceiling.

### 3.6 Support is the hidden cost, and Book 4 is the cheap one

Book 4 is mostly reading and drilling, which is why it is the right lead product. But the SQL and
Python questions do invite "it does not run on my machine," and at ₹435 net **two support emails
wipes out the margin.** The commodity kits have no support cost because nothing in them executes.

Decide now what support you are offering, and say it on the page. "Email support" with no bound is
a liability.

### 3.7 There may already be a ₹499 book bundle in the house

My notes record a **Northstar six-role book bundle at ₹499**, encyclopedia-based. If that is live
or planned, two ₹500 book products from the same house compete and confuse the channel. **I do not
know its current status.** Resolve it before launching.

### 3.8 Deferring the course is right, but it removes the only recurring revenue

You are right that a course is 6–8 months and expensive, and right to defer. But the course was the
business; book sales are cash flow. **The book should be positioned explicitly as the thing that
earns the audience that makes the course viable** — otherwise you have swapped a hard business for
no business.

---

## 4. What I would do

### Phase 0 — make it safe to sell (days, before anything is listed)

1. **Close the verification gap.** PostgreSQL and MySQL installed, §71.11's 32 questions run,
   §70.9's 16 run in Excel. Or drop the claim from the marketing and keep it only where true.
2. **Book 4 visual pass**, since it grew by a third.
3. **Close or accept the 46 open findings.**
4. **Publish the ladder and the update policy** on the page: ₹500 now, volumes at ₹X later, free
   Book 4 updates forever.
5. **The dull layer**: refund policy, licence terms, GST on digital goods, support boundaries.

### Phase 1 — the free wedge (this is the growth engine, not marketing decoration)

Give away **about 40 of the 202 predict-the-output questions** as a free PDF.

Why these: they are the only part of the product that proves the differentiator *in ten minutes*.
`int("25", 4)`. A `NOT IN` that silently returns nothing. A `VLOOKUP` that returns another
customer's row. **A 535-page book cannot go viral. A question that makes a senior engineer get it
wrong can.**

Give each one the full treatment — the hook, the real output, the tier table — so the sample
demonstrates the standard rather than teasing it.

Channel, in likely order of return: **LinkedIn** (post one question, answer it next day — this is
the highest-leverage habit available to you), **Telegram and WhatsApp placement groups**, **college
placement cells**, **YouTube Shorts** if you have the appetite.

Target before the paid launch: **an email list in the low thousands.** The list is the asset; the
book is inventory.

### Phase 2 — launch Book 4 at ₹500

Headline: **767 questions. Every answer was run. ₹500.**
Comparison, stated plainly: the nearest Kindle competitor is ₹449 for 210 questions.
Framing: **launch price, rising on a stated date.**

### Phase 3 — the ladder, published from day one

| | Product | Price |
|---|---|---|
| Entry | **Book 4, Be Interview Ready** | **₹500** (launch) |
| Core | Books 1–3 + the Practice Arena | ₹1,999–2,499 |
| Later | The course, once the audience exists | — |

---

## 5. Decisions only you can make

1. **Northstar** — is the ₹499 six-role bundle live, shelved, or this product renamed?
2. **Free updates to Book 4 for ₹500 buyers** — I recommend yes; it is your call.
3. **Launch price with a rise date, or ₹500 permanently?** The first keeps the ceiling, the second
   is simpler.
4. **Runway.** How much do you need and by when? It changes how much Phase 1 you can afford before
   Phase 2.
5. **Appetite for audience work.** Phase 1 is months of posting, not a weekend. If you will not do
   it, say so and we design a channel-partner route instead — placement cells, a training
   institute, an affiliate — lower margin, much faster.
6. **Verify, or drop the claim.** Both are honourable. Selling on a claim the book itself
   contradicts is not.

---

## 6. What I can do next

- **Install PostgreSQL and MySQL and close §71.11's verification gap.** Highest-value thing left in
  the project, roughly a day.
- **Build the free sample PDF** — 40 questions across tools, as a standalone piece.
- **Write the sales page copy** against the positioning above.
- **A 30-day LinkedIn content plan** drawn from questions already written, so Phase 1 is execution
  rather than invention.

If you only do one: **close the verification gap.** Everything else here is reversible. A buyer
finding a wrong answer in the interview book is not.
