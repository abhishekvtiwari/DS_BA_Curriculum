# Read me first

*The Analyst to Architect review bundle — 3 October 2026, second build*

Everything is here: the four books, the practice material that goes with them, a guide to where
every topic lives, and the review state. 928 files, 289 MB, in five folders you can read in order.

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
| **04-Practice-Arena** | Everything you practise with, **arranged by tool** — pick Excel, or SQL, or Python, and work down. |
| **05-Review-state** | The tracker, your decisions, and the per-chapter changelogs. |

---

## 01-Books — the four books

| Book | Pages | What it covers |
|---|---|---|
| **1 · Theory** | 218 | The ideas, no software to install. Parts 0 and 1. |
| **2 · Practical** | 1,401 | The analyst's tools, hands on: spreadsheets, SQL, cleaning, charts, Power BI, Python, statistics, business skills; then the advanced layer. Parts 2 and 3. |
| **3 · Implementation** | 1,318 | Machine learning, data engineering, production ML and generative AI, architecture and leadership, and the closing chapter. Parts 4 to 7. |
| **4 · Be Interview Ready** | 535 | Part 8: how hiring works, the extra-points method, and a question bank for every skill and role. |
| *Book Overview* | 71 | Internal, not for sale. Every chapter, what it covers, how long it takes, how the parts connect. |

**Book 4 is rebuilt — 535 pages, up from 400.** It now carries ten new predict-the-output sections across Part VIII. Everything else is the 1 October build.

Two reading notes:

- Use the contents page or your reader's bookmark sidebar. In Book 4 all **169 contents links and
  724 bookmarks** were checked to land on the right page.
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

**Part VIII now has ten predict-the-output sections, and 202 new questions.**

You asked for the interview material to be ground down from very basic to very detailed, with
brain-racking questions of the `int("25", 4)` kind. Thirteen of the fourteen banks had no such
section at all; the one that did — Chapter 72's §72.2 — became the template. You read §71.11 and
approved its depth, and this is that standard applied across the rest.

Part VIII goes from **565 coded questions to 767**.

Read these two, in this order:

- **Part-VIII-predict-the-output-summary.pdf** (4 pages) — what was built, the three banks I
  deliberately left alone and why, the one scope decision I would like from you, and the dozen
  drafted questions that turned out wrong and were caught by running them
- **Ch71-section-71.11-predict-the-output.pdf** (26 pages) — the section you already approved,
  as the worked example of the standard

`changelogs/` holds one file per chapter touched, recording every change and how it was verified.

Every answer in all ten sections was run. Nothing was typed from memory.

## 04-Practice-Arena — arranged by tool, not by chapter

This is the part that changed most. It used to be sixty-nine folders named `ch10`, `ch11`, `ch12`
— the book's filing system, handed to the reader. To practise Excel you had to already know that
chapters 02, 04, 08, 09, 10, 11, 15, 19, 22 and 70 were the ones with workbooks in them.

Now you pick a tool and work down. Ten tools, sixty stages, 643 files.

| | Tool | Stages | What it goes from, and to |
|---|---|---|---|
| 1 | **Excel & Google Sheets** | 8 | A first formula → lookups and Power Query → a dashboard → a macro that consolidates twelve branch workbooks |
| 2 | **SQL** | 10 | Load one database → SELECT → window functions → dbt → the question banks |
| 3 | **Python** | 6 | First line → pandas → a scheduled report → a packaged program with tests |
| 4 | **Statistics & experiments** | 6 | Describing data → tests → A/B design → causal inference |
| 5 | **Machine learning** | 7 | The workflow → algorithms → honest evaluation → deep learning → a capstone |
| 6 | **Data engineering** | 7 | Ingestion → orchestration → quality → scale → streaming |
| 7 | **GenAI & production ML** | 6 | Tokens and embeddings → RAG and agents → MLOps and LLMOps |
| 8 | **Command line, Git & toolkit** | 3 | The shell → version control → setup checks |
| 9 | **Architecture & the business** | 6 | Requirements → metrics → system design → governance |
| 10 | **Take-home assignments** | 1 | Timed, realistic briefs |

**Chapter numbers are gone from the folder names.** Where a stage draws on more than one chapter,
the sub-folder is named after what it teaches — `Numbers-Without-Fear`, not `ch04`.

Three things that make it usable rather than just rearranged:

- **Every stage has a README** saying what it covers, how many files are yours, and which chapter
  it came from.
- **`WHERE-IS-MY-CHAPTER.md`** at the Arena root turns any reference in the book — "see
  `companion/ch18/`" — into a folder, for all 71 chapters that have practice files.
- **`_build-scripts/` folders** hold the scripts that generate practice data, kept out of the way
  but not hidden, so nothing is a black box.

**The chapter-by-chapter view still exists** in the repository, unchanged, because the book refers
to it by name and breaking those references across 83 chapters would be worse than the problem it
solves. The Arena is a second view of the same files, not a replacement.

**It is generated and it proves itself.** The build refuses to finish if any chapter is unclaimed
by a tool, if two files would overwrite each other, or if any source file is missing from the
result — checked by content hash, not by counting. All 573 tracked practice files verified present.

**What is deliberately not here.** About 317 MB of generated data — the large files the
data-engineering chapters build. The `_build-scripts/` rebuild them in about a minute, which is how
the book is designed to work.

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

**1. Whether Chapter 76B should get a section.** It is the one open scope decision. "Predict the
output" does not fit a requirements bank, but there is a real BA equivalent — *given a written
requirement, what is ambiguous and what breaks when a developer reads it?* That is a different
format, so I did not build it unilaterally. The summary document explains the reasoning.

**2. Whether the guide is the reference you wanted.** You asked for somewhere you can see what
topics exist and where they are. The topic index is my answer. If you want it cut differently —
by role, by tool, by week of study — say so; it is generated, so re-cutting it is cheap.

**3. Whether the Arena is the shape you wanted.** Open `04-Practice-Arena/`, pick one tool, and
see whether the stages run small-to-full the way you described. The ordering within each tool is
my editorial judgement — it follows the book's teaching order — and it is the part most worth
correcting now, because it is one map in one file and cheap to change.

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
