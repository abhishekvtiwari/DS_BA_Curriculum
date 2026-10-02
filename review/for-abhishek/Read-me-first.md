# Read me first

*The Analyst to Architect review bundle — 3 October 2026*

Everything is here: the four books, the practice material that goes with them, a guide to where
every topic lives, and the review state. 781 files, 280 MB, in five folders you can read in order.

The point of this bundle is for you to tell me **what is lapsing and what is not**. There is a
section at the end on exactly that — what I would most like you to look at, and what I already
know is missing.

---

## The five folders

| Folder | What is in it |
|---|---|
| **01-Books** | The four books as PDFs, plus the internal overview. Start here if you want to read. |
| **02-Guide** | *Where everything is* — the map of every chapter, section and topic. Start here if you want to find something. |
| **03-Whats-new** | What changed since you last looked, as a short review copy rather than a whole book. |
| **04-Practice** | The files a reader actually works with: notebooks, SQL, spreadsheets, datasets. |
| **05-Review-state** | The tracker, your decisions, and the per-chapter changelogs. |

---

## 01-Books — the four books

| Book | Pages | What it covers |
|---|---|---|
| **1 · Theory** | 218 | The ideas, no software to install. Parts 0 and 1. |
| **2 · Practical** | 1,401 | The analyst's tools, hands on: spreadsheets, SQL, cleaning, charts, Power BI, Python, statistics, business skills; then the advanced layer. Parts 2 and 3. |
| **3 · Implementation** | 1,318 | Machine learning, data engineering, production ML and generative AI, architecture and leadership, and the closing chapter. Parts 4 to 7. |
| **4 · Be Interview Ready** | 433 | Part 8: how hiring works, the extra-points method, and a question bank for every skill and role. |
| *Book Overview* | 71 | Internal, not for sale. Every chapter, what it covers, how long it takes, how the parts connect. |

**Book 4 is new today — 433 pages, up from 400.** Everything else is the 1 October build.

Two reading notes:

- Use the contents page or your reader's bookmark sidebar. In Book 4 all **160 contents links and
  629 bookmarks** were checked to land on the right page.
- Books 2 and 3 are around 80 MB each. They are fine in a desktop reader and slow in a phone
  browser.

---

## 02-Guide — where everything is

A 192-page map of the whole book, in four formats, generated from the manuscript itself so it
cannot drift out of step.

- **Where-Everything-Is.pdf** — read it
- **Where-Everything-Is.docx** — same, if you want to write in it
- **Where-Everything-Is.xlsx** — three sortable sheets: 85 chapters, 821 sections, 3,294 terms.
  This is the one to use if you want to filter, sort by time, or search.
- **Where-Everything-Is.md** — the source

It answers three questions:

1. *Which book do I open?* — the four-books table at the front.
2. *Where is topic X taught?* — **the topic index**, alphabetical, 3,294 terms, each pointing at
   its chapter. Built from every chapter's own Key terms list.
3. *What do I actually do in this chapter?* — each chapter lists the practice files that ship
   with it.

---

## 03-Whats-new — what changed

**Chapter 71 has a new section, §71.11, "Predict the output: from basic to brain-racking."**

You asked for the interview material to be ground down from very basic to very detailed, with
brain-racking questions of the `int("25", 4)` kind. I measured Part VIII first: of its 619
questions, only **19** were output-prediction, and **17 of those sat in one section** of Chapter
72. Thirteen of the fourteen banks had none.

§71.11 is the answer for SQL, and the template for the other thirteen banks. 16 core questions and
16 rapid-fire rows, taking Chapter 71 from 76 questions to 108. A new *Brain-racking* level sits
above Warm-up and Core.

In this folder:

- **Ch71-section-71.11-predict-the-output.pdf** (26 pages) — read this one
- the same as **.docx**, if you want to comment in it
- **changelog-ch71.md** — what changed and why, including the six questions that were wrong in
  draft
- **changelog-ch18.md** — the object-oriented Python work you approved on 1 October

---

## 04-Practice — the material a reader works with

580 files across 71 chapter folders, 92 MB.

| | |
|---|---|
| **49 notebooks** (`.ipynb`) | Each chapter's code, with the book's own explanation beside it, already run so the outputs are there before you start |
| **86 SQL files** | The queries, written for PostgreSQL and MySQL. 13 chapters ship both dialects |
| **127 Python scripts** | The finished programs the chapters build |
| **29 Excel workbooks** | The spreadsheet exercises |
| **152 CSVs and 9 parquet files** | Riverstone Supplies, the worked example used all the way through |

**What is deliberately not here.** About 317 MB of generated data — the large files the
data-engineering chapters build, such as Chapter 28's 52 MB of order items and Chapter 30's web
events. The chapter scripts rebuild them in about a minute, which is how the book is designed to
work, and shipping them would have tripled the bundle. Any chapter that needs them says so and
names the script that makes them.

---

## 05-Review-state — where the work stands

- **TRACKER.md** — **3,761 of 3,822 findings closed, 98%.** Verified 3,152 · Fixed 609 · Approved
  and waiting to be fixed 15 · Open 46.
- **DECISIONS.md** — your decisions. Global rule A1 is ticked, all 26 themes carry a decision, and
  all eight structural decisions D1–D8 are approved. Nothing in the fix queue is waiting on you.
- **DECISIONS-BRIEFING.md** — the decisions explained, if you want the reasoning again.
- **Book-Review-Action-Register.xlsx** — the findings as a spreadsheet.
- **changelog/** — one file per chapter, recording every change and how it was verified.
- **START-HERE.md** — the same orientation page that sits in the project folder.

---

## What I would most like you to look at

**1. The depth of §71.11.** This matters more than anything else in the bundle, because the same
standard is about to be applied to thirteen more question banks — roughly 260 more questions. If
the depth is wrong, I would much rather fix it once than fourteen times. Read a few questions and
tell me: too long, too short, or right? Is the tier table earning its place? Are the
*Brain-racking* ones actually hard enough?

**2. Whether the guide is the reference you wanted.** You asked for somewhere you can see what
topics exist and where they are. The topic index is my answer. If you want it cut differently —
by role, by tool, by week of study — say so; it is generated, so re-cutting it is cheap.

**3. The practice material against the theory.** Open any chapter in Book 2, then open the same
chapter's folder in `04-Practice`. Does the practice match what the chapter taught? That pairing
is the thing I can least check for myself.

---

## What I already know is missing

Recorded so you do not have to find it:

1. **Section 71.11 has not been run on PostgreSQL 16 and MySQL 8.4.** Neither is installed on this
   machine. Every answer was run, against the chapter's own `riverstone_2025` data on a bench that
   was first checked to reproduce four figures the chapter already prints. But the chapter's
   standard is a run on both engines, so the new outputs are labelled **Run (riverstone_2025)**
   rather than **Verified**, and the chapter's own at-a-glance box now states the exception. Four
   questions where the engines genuinely disagree are marked **Dialect split** and give each
   engine's documented behaviour instead of one answer.

2. **Thirteen question banks still have no predict-the-output section:** Chapters 70, 72a, 73–82.

3. **Books 1, 2 and 3 still carry a series map whose Book 4 page numbers predate today.** Book 4's
   own map is correct and was rebuilt. Fixing the other three means rebuilding them, and I did not,
   for the reason below.

4. **This machine does not reproduce the original build exactly.** I test-rebuilt Book 1 and got
   217 pages against the shipped 218, with the cover's letter-spacing visibly different — the fonts
   resolve differently here. So I rebuilt only Book 4, whose content actually changed, rather than
   re-paginating three unchanged books for a cosmetic reason. Book 4's own pagination therefore
   moved slightly more than the new section alone explains: Chapters 69 and 70 shifted by one and
   two pages without their content changing. Book 4's visual check should be redone before release.

5. **Chapter 15 was missing its PostgreSQL query file** while shipping a hand-written MySQL one.
   Generated today, consistent with the thirteen other chapters that ship both.

6. **The hours tables in Chapters 6, 9 and 83 are out of date**, and have been since the Chapter 18
   work. Theme T12 schedules that as a single final pass, so it is deliberately not done piecemeal.

---

## If you want to run the practice material

Nothing in the bundle needs installing to *read*. To run it:

- **Notebooks:** Python 3.11 or newer, then `pip install jupyter pandas numpy matplotlib`. Open
  any `.ipynb` in `04-Practice/chNN/`. The outputs are already saved, so you can read without
  running.
- **SQL:** PostgreSQL is the book's primary database, MySQL the supported alternative. Load
  `04-Practice/riverstone_2025_setup.sql` first, then run the chapter's `_queries_postgresql.sql`.
- **Excel:** the workbooks open in Excel or Google Sheets and none of them carries a macro, so
  nothing will prompt you to enable one. Chapter 19 is the macro chapter, and there the macros are
  what you write rather than what ships.

The large generated datasets are rebuilt by the scripts named in each chapter.
