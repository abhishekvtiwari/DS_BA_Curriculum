# The product ladder, and the project catalogue

*3 October 2026. Captured from Abhishek's design. Companion to
[Selling-the-books-strategy-and-red-team](Selling-the-books-strategy-and-red-team.md), which covers
pricing and go-to-market; this one covers what the products actually are.*

## The ladder

| | Product | Price | What it is |
|---|---|---|---|
| **1** | **The Interview Book** | ₹500 | Book 4 alone. 827 questions today, heading for ~1,160. The thing Instagram points at. |
| **2** | **The Interview Package** | *to set* | Everything: all four volumes, the Practice Arena (Excel files, SQL, notebooks, datasets), and the assignments to work through on your own. |
| **3** | **Projects** | ~₹150 each | Standalone, ready-made portfolio projects. Buy one, buy five. |

The shape is right, and the third tier is the interesting one. A ₹500 book is a single transaction
from each buyer. **₹150 projects are repeatable revenue from the same person**, they are small to
build relative to a book, and they answer the question every Indian job-seeker actually has, which
is not "what should I learn" but **"what do I put on my CV?"**

---

## The thing that makes a ₹150 project worth buying

This is the one design decision that decides whether tier 3 works, so it is worth being blunt about.

**GitHub is full of free code.** If what we sell is a script that sends an email, we are competing
with a thousand free repositories and we lose. Nobody needs another `smtplib` example.

What is genuinely scarce, and what each project must contain:

| | Why it is the value |
|---|---|
| **A realistic brief** | Written the way a manager would ask, vague in the places managers are vague |
| **Messy data** | Not a clean CSV. Dates in two formats, a trailing space in a key, a duplicate, a missing region |
| **The worked solution** | Commented, runnable, with every output produced by running it — the book's standard |
| **The reasoning** | Why this approach and not the obvious one. This is Chapter 69A applied to a project |
| **The interview narrative** | **The part nobody else sells.** How to describe this project in ninety seconds, what the interviewer will probe, and the honest answer to "what would you do differently" |

That last row is the product. A buyer is not paying ₹150 for code. They are paying for **something
true to say in an interview**, and for the confidence of having actually run it.

Chapter 76A already teaches how to talk about a project and Chapter 82 has the take-home format, so
the house style for that section already exists.

---

## The catalogue, from Abhishek's list

Captured as specified, with what each one would contain and what to watch.

### P1 · The daily report that sends itself
**Raw data → processed → Excel report → emailed to a list.**

The flagship, because it is the single most common real request a junior analyst gets, and because
it is the Chapter 18 automation payoff as a standalone artifact.

| | |
|---|---|
| Teaches | Reading messy raw data, aggregating, writing a formatted `.xlsx`, sending to a distribution list, scheduling it |
| Already in the book | Chapter 18 §18.15–18.18 (the report, the entry point, the `.bat`, Task Scheduler), Chapter 20 (delivery) |
| Interview narrative | "I automated a two-day manual month-end into a twenty-minute run" — the single most reusable line a junior analyst can have |

**The risk to design around: Outlook.** Driving Outlook needs Windows *and* an installed, configured
Outlook, which excludes Mac users, Linux users, anyone on Google Workspace, and most students. That
is a large share of the buyers, and every one of them becomes a support email.

**Recommendation:** build it **SMTP-first** — which works everywhere, including Gmail with an app
password — and ship the Outlook version as a clearly-labelled variant for people in a Microsoft
office. Same project, two delivery modules, one extra file. This is worth getting right because P1
is the one you will sell most.

### P2 · Excel dashboards, ready-made and explained
**A proper, good-looking dashboard, and how it was built.**

| | |
|---|---|
| Teaches | Model → pivots → charts → layout → interactivity, in the order you would build it |
| Already in the book | Chapter 11 (the spreadsheet mastered), Chapter 15 (what to plot), Chapter 70 §70.8 (dashboard critiques) |
| The hook | Most people have never seen a *well-built* dashboard file opened up. Shipping one that looks professional, with the build explained step by step, is genuinely rare |

Ship the finished workbook **and** a stripped version so the buyer can build it themselves. The
value is the gap between the two.

### P3 · Python dashboards
The same, in code — Streamlit or Plotly Dash. A different audience from P2 and a different CV line.

### P4 · The data-cleaning series
**Jumbled data in, trustworthy data out.** Abhishek is right that this is "an entirely different
saleable project" — and it may be better as a *series* of three or four small ones than one large
one, because each is a separate purchase.

| | |
|---|---|
| Teaches | Profiling, duplicates, inconsistent categories, dates and time zones, validation rules that must return zero |
| Already in the book | Chapter 14 is the whole method, and Chapter 77 §77.8 now has the traps that bite on the way in |
| The hook | Every job ad says "data cleaning". Almost no portfolio shows it, because clean data is boring to publish. A project built on genuinely nasty data stands out |

The Riverstone messy files already exist — `month_end_pack_2025_messy.xlsx`,
`sales_export_with_problems.csv` — so the raw material is in the repository.

### P5 · Logistics
Abhishek named this; the shape needs deciding. Likely candidates: delivery-route and cost analysis,
inventory and stockout analysis, or supplier performance. Riverstone already has orders, products,
suppliers and demand data, so it fits the house example without inventing a new company.

---

## What else the catalogue should probably include

Three gaps that follow from what the book already contains, offered for a decision rather than
assumed:

- **A SQL-only project.** A reporting layer built as a set of reviewed queries. Cheapest to build
  and support of anything on this list, because nothing has to run on the buyer's machine.
- **An end-to-end pipeline.** Ingest, clean, load, schedule, alert — the data-engineering CV line.
- **A first ML project done honestly.** With the baseline, the leakage check and the "would I ship
  this" verdict, which is what Chapter 74 argues for and what almost no portfolio project does.

---

## Three things to settle before building any of them

**1. The support boundary, written on the sales page.** At ₹150 the net is about ₹131 after platform
fees. **One support email per sale wipes out the margin.** The answer is not to refuse support, it
is to design it out: pin every version, ship a sample dataset so nothing depends on the buyer's
data, test on a clean machine, and state plainly what is and is not covered.

**2. How a project differs from the Practice Arena.** The Package (tier 2) already contains 643
practice files. If a ₹150 project looks like more of the same, a Package buyer will feel
double-charged. The line that holds: **the Arena teaches the book; a project is a finished piece of
work with a brief, messy data and an interview story.** Different purpose, different format. Say it
on the page.

**3. The projects Abhishek already has.** You mentioned having a few of your own. Those are
potentially the best items in the catalogue, because they are real work rather than teaching
examples — and real beats realistic. **Send them over and I will tell you honestly which stand up
as saleable projects and what each would need.**

---

## Sequence

Agreed with the earlier instruction — the book first, then the projects.

| | |
|---|---|
| **Now** | Finish the Interview Book: ~330 more questions to about 1,160, then the cover and back cover |
| **Then** | P1, built SMTP-first, as the template for the rest. Get one project completely right and the others follow a pattern |
| **Then** | P4, the cleaning series, since the messy data already exists |
| **In parallel** | Decide the Package price, and the support boundary |
