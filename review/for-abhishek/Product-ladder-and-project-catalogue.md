# The product ladder, and the project catalogue

*Revised 4 October 2026. Companion to
[Selling-the-books-strategy-and-red-team](Selling-the-books-strategy-and-red-team.md), which covers
pricing and go-to-market; this one covers what the products are.*

## The ladder

| | Product | What it is |
|---|---|---|
| **Start here** | **The Interview Readiness Book** | *Be Interview Ready*, by Compounza: data science and analytics interview questions with worked answers, from the online test to the first 90 days. The thing Instagram points at. Working price ₹500 |
| **Add-on 1** | **The Three Volumes** | **First Principles** (Parts 0–1), **The Working Analyst** (Parts 2–3) and **Builder to Architect** (Parts 4–7), with the practice files arranged by tool. Turns the interview book from a rehearsal into a course. Price to set |
| **Add-on 2** | **Projects** | Standalone, ready-made portfolio projects, bought one at a time. Owner's working figure about ₹150 each, to confirm |

### Why the volumes are named this way

The series is *Analyst to Architect*, so the three names follow the climb:

| Volume | Name | Parts | Why the name fits |
|---|---|---|---|
| 1 | **First Principles** | 0–1 | Part 0 is already titled "First Principles: Data from Zero"; this is the ground floor, no software needed |
| 2 | **The Working Analyst** | 2–3 | Everything a first analyst job uses day to day, then the advanced analytics that makes a senior one |
| 3 | **Builder to Architect** | 4–7 | Machine learning, engineering, GenAI and architecture: from building systems to designing them |

Inside the PDFs the books still title themselves "Book 1" to "Book 4". Renaming them is a rebuild
of all four, waiting on a yes.

---

## What makes a project worth buying

GitHub is full of free code, so a project that is only code loses. Each project carries five
things, and the fifth is the product:

| | |
|---|---|
| **A realistic brief** | Written the way a manager asks, vague where managers are vague |
| **Messy data** | Dates in several formats, duplicates, a broken key, a missing value |
| **A worked, runnable solution** | Every output produced by running it, the book's standard |
| **The reasoning** | Why this approach and not the obvious one |
| **The interview story** | How to describe it in ninety seconds, what will be probed, and the honest answer to "what would you do differently" |

---

## The catalogue: eleven projects, by track

Every project below is grounded in material the book already contains: a chapter that teaches the
method and, where marked, data or a pipeline that already exists. That is what makes them quick to
build and hard to copy. **None is built yet.**

### Analyst track

| # | Project | What the buyer builds | Built on | Data ready? |
|---|---|---|---|---|
| **P1** | **The daily report that sends itself** | Raw export → cleaned → formatted Excel report → emailed to a list on a schedule. SMTP first, so it works on any laptop; an Outlook variant for Microsoft offices | Ch 18, Ch 20 | Yes |
| **P2** | **The Excel sales dashboard, built and explained** | A finished dashboard workbook plus a stripped version to build yourself, step by step | Ch 11, Ch 15 | Yes |
| **P3** | **The Python dashboard** | The same story in code, as an interactive dashboard | Ch 18, Ch 15 | Yes |
| **P4** | **The data-cleaning series** (three parts, sold separately) | 1 · dates and categories · 2 · keys and joins · 3 · validation and reconciliation to the rupee | Ch 14, Ch 72B | **Yes, with a truth file**, so buyers can check their own answer |
| **P5** | **Logistics: delivery and stockout analysis** | On-time delivery defined properly, stockouts measured from demand, and the branch view | Ch 23 §23.8, Ch 76B Q76B-087 | Yes, Riverstone orders and demand |
| **P6** | **The SQL reporting layer** | A set of reviewed, tested queries that a business runs every month; a dbt variant for analytics engineers | Ch 13, Ch 28, Ch 32 | Yes |

### Business analyst track

| # | Project | What the buyer builds | Built on | Data ready? |
|---|---|---|---|---|
| **P7** | **The requirements pack: order-to-cash** | A BRD, a swimlane map, user stories with acceptance criteria and a UAT plan for one real process — the BA's portfolio, which almost no BA candidate has | Ch 25, Ch 76B | Yes, the process is fully mapped in Ch 25 |

### Data science track

| # | Project | What the buyer builds | Built on | Data ready? |
|---|---|---|---|---|
| **P8** | **Customer churn, done honestly** | A first ML project with the baseline, the leakage check and a "would I ship this?" verdict | Ch 36, Ch 39, Ch 44 | Yes |
| **P9** | **The A/B test readout** | Design, analysis and a one-page decision memo for a real experiment | Ch 30 | Yes, Riverstone's website test |

### Engineering and AI track

| # | Project | What the buyer builds | Built on | Data ready? |
|---|---|---|---|---|
| **P10** | **The pipeline that tells you when it breaks** | Ingest, clean, load and schedule, with data checks and an alert — the data-engineering CV line | Ch 45, Ch 46, Ch 47 | Yes |
| **P11** | **The email-order intake with an honest evaluation** | An LLM pipeline that reads emailed orders, measured on both rates: how much it automates and how much of that is quietly wrong | Ch 55, Ch 58 | Yes; Ch 58 measured 88% automatic and 19% of those wrong |

### Suggested packs

Bundles let a buyer get a track for less than the parts, and they are a natural Instagram offer:

| Pack | Projects |
|---|---|
| **Analyst starter** | P1 + P2 + P4 (part 1) |
| **BA starter** | P7 + P4 (part 1) |
| **Data science starter** | P4 (part 1) + P8 + P9 |
| **Engineering starter** | P10 + P11 |

---

## Three things to settle before building any of them

**1. The support boundary, written on the sales page.** At about ₹150 the net is about ₹131 after
platform fees, and one support email per sale wipes out the margin. Design support out: pin every
version, ship sample data so nothing depends on the buyer's data, test on a clean machine, and state
plainly what is and is not covered.

**2. How a project differs from the practice files in the volumes.** The practice files teach the
book; a project is a finished piece of work with a brief, messy data and an interview story.
Different purpose, different format. Say it on the page, or a volumes buyer feels double-charged.

**3. The projects you already have.** Real work beats realistic examples. Send them over and each
will get an honest assessment of whether it stands up as a saleable project and what it would need.

## Build order

| | |
|---|---|
| **First** | **P1**, as the template every other project follows |
| **Then** | **P4**, part 1, because its data and truth file already exist |
| **Then** | **P7**, because no competitor sells a BA portfolio project and the material is ready |
| **In parallel** | Set the volumes and project prices, and the support boundary |
