# Part Brief — Part 0 — First Principles: Data from Zero

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-0-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 3–6; 1 and 2 are approved**.

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P0-01 | 1 | What Is Data? | C | 7,500 | Approved (v1) | `manuscript/ch01-what-is-data.md` |
| P0-02 | 2 | How Computers Store, Move and Protect Data | C | 8,000 | Approved (v1) | `manuscript/ch02-how-computers-store-move-protect-data.md` |
| P0-03 | 3 | How a Business Runs on Data | C | 4,500 | Not started | `manuscript/ch03-how-a-business-runs-on-data.md` |
| P0-04 | 4 | Numbers Without Fear | C | 4,500 | Not started | `manuscript/ch04-numbers-without-fear.md` |
| P0-05 | 5 | Thinking Like an Analyst | C | 3,500 | Not started | `manuscript/ch05-thinking-like-an-analyst.md` |
| P0-06 | 6 | Setting Up to Learn | C | 2,500 | Not started | `manuscript/ch06-setting-up-to-learn.md` |

## Reference chapters for this part

Chapters 1 and 2 (class C). Match their length, tone, worked examples, measured demonstrations, and story sections closely: these four chapters finish the same opening part of the book.

## Guidance specific to this part

- **Continuity with Chapters 1 and 2 is the top priority.** Reuse their characters (Meera, Imran, Kavya), habits (hand-checking, "what does one row mean?", data quality dimensions), and vocabulary. Don't re-teach what they already taught; refer back by section.
- **Chapter 3 is the business spine of the whole book.** Follow one Riverstone order from enquiry to cash (lead → quote → order → production → dispatch → invoice → payment → report), and make every system and document consistent with the existing databases. Follow a real order from the **mini database** for the order, invoice, and payment stages (for example Sharma Hardware's order 5001, invoice 9001, and its payment on 2 February 2026). The mini database has no lead or quote tables, so create the earlier stages to fit it (for example, Sharma Hardware's enquiry shortly before its 4 November 2025 signup) and register them as new facts; don't borrow rows from the one-year database's `leads` table, which is a separate slice (instructions, section 7.3). Chapter 3 is also where **Riverstone's two manufacturing plants, its business systems (ERP, CRM, billing, website, support desk), and its departments** get their canonical names: propose them in your first message and register them as new Riverstone facts (instructions, section 14.3). Blueprint Ch 3 also asks for "where manual work hides in a data flow": this is the first appearance of the automation thread, so show the copy-paste and re-keying steps explicitly.
- **Chapter 4 (Numbers Without Fear):** every number worked and checked by script; percentages vs percentage points; CAGR with a real worked example on Riverstone revenue; averages chosen by level of measurement (tie back to Chapter 1 section 1.6); estimation. Use Python only to check, not to teach.
- **Chapter 5 (Thinking Like an Analyst):** issue trees and MECE drawn as figures; use Riverstone questions that later chapters answer with SQL (for example "why did March revenue fall?", Chapter 1 section 1.2), so readers see the same question solved again later.
- **Chapter 6 (Setting Up to Learn):** the install list must match what later chapters use: Excel or Google Sheets, PostgreSQL and MySQL with DBeaver (Chapter 12 section 12.3 already has full steps; summarize and point there rather than duplicating), Python (state version), Power BI Desktop (Windows only; say what Mac users do), Git and VS Code, and the companion files. Verify every install step and version against official sources at the time of writing. Include the sample 6-month analyst plan and weekly schedule from the blueprint, and honest guidance on learning with AI assistants.
- **Data and tools:** no new databases needed. Use the mini and one-year databases for small examples; build any small CSVs in `companion/chNN/`.

## Sequencing and dependencies

Can start immediately. Chapter 3 should be written first, because Part II chapters (spreadsheets, KPIs, automation) reuse its systems and process map.

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

**Ch 1. What Is Data?** · NEW · 7,500 words · ✅ **Approved (draft v1, 16 Sep 2026)**
Data vs information vs knowledge vs insight · data all around you (a shopping receipt, a phone's step counter, a train timetable) · structured, semi-structured, unstructured · data types (numbers, text, dates, true/false) · qualitative vs quantitative · levels of measurement (nominal, ordinal, interval, ratio) and why they limit what maths you can do · a row, a column, a record, a dataset · metadata · where data comes from (people, machines, systems) · data quality in one page.
*Project:* Log a week of your own spending in a table and classify every column.

**Ch 2. How Computers Store, Move and Protect Data** · NEW · 8,000 words · ✅ **Approved (draft v1, 16 Sep 2026)**
Bits and bytes; KB → TB with real-world sizes · files, folders, file extensions · common formats: CSV, Excel, JSON, XML, PDF, images, Parquet (introduced only) · what a database is (one-page preview of Ch 12) · servers, the internet, and "the cloud" in plain English · what an API is (the waiter analogy) · backups, versions, passwords, and why data security matters.
*Project:* Open the same small dataset as CSV, Excel, and JSON, and describe the differences.

**Ch 3. How a Business Runs on Data** · NEW · 4,500 words
The departments of a company and the data each creates (sales, marketing, finance, operations, HR, support) · following one Riverstone order from enquiry to cash: lead → quote → order → production → dispatch → invoice → payment → report · business systems: ERP, CRM, HRMS, POS, e-commerce · transactions vs reports · what a KPI is · dashboards and meetings · who decides what, and why they need data · where manual work hides in a data flow (copy-paste, re-keying, emailing files around).
*Project:* Map the data flow of one process at your workplace, or of a local shop.

**Ch 4. Numbers Without Fear** · NEW · 4,500 words
Percentages, percentage points vs percent change · ratios and rates · growth, CAGR, compounding · averages (mean, median, mode) and weighted averages · rounding and significant figures · reading tables and charts correctly · basic probability as "how often, out of how many" · orders of magnitude and quick estimation · common number tricks in business news. Every idea is worked with numbers.
*Project:* Check five statistics quoted in news articles or company presentations.

**Ch 5. Thinking Like an Analyst** · NEW · 3,500 words
Curiosity and asking good questions · turning a vague request into a precise question · hypotheses · breaking problems down (issue trees, MECE) · fact vs opinion vs assumption · spotting misleading charts and claims · bias in how we see data · simple decision-making with data.
*Project:* Take a real business question and build an issue tree with the data each branch needs.

**Ch 6. Setting Up to Learn** · NEW · 2,500 words
The computer you need (and don't) · installing the book's tools, with links to Appendix B · the companion files · keyboard and file-management basics · how to read documentation · learning with AI assistants without letting them think for you · building a study habit: sample 6-month analyst plan and weekly schedule · how to use the exercises and answer key.
*Project:* Install everything, load the Riverstone mini dataset, and write your 90-day plan.

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 1

- *(from Ch 2)* Before you start: Chapter 1 (what data is: rows, columns, types, and quality).
- *(from Ch 2)* In Chapter 1 you learned what data *is*.
- *(from Ch 2)* The right-hand names follow four habits: a date first, written year-month-day, so files sort in time order automatically (Chapter 1); the same pattern every time; lower-case words joined with underscores or hyphens, which avoids problems in code and web links; and no words like "final", which are always eventually wrong.
- *(from Ch 2)* CSV can't tell "unknown", "not applicable", and an empty text value apart (Chapter 1).
- *(from Ch 2)* JSON (JavaScript Object Notation) is the semi-structured format from Chapter 1.
- *(from Ch 2)* Before Meera (Chapter 1) joined, Riverstone's weekly sales report worked like this.
- *(from Ch 2)* Option B: use your spending log from Chapter 1's project, and create the formats yourself: save it from your spreadsheet as `.xlsx` and as CSV (UTF-8), then type a JSON version of the first three rows by hand in a text editor, using section 2.5 as your model.
- *(from Ch 12)* Before you start: Chapter 1 (what data is), Chapter 3 (how a business runs on data), and Chapters 10–11 (spreadsheets).

#### Chapter 2

- *(from Ch 1)* Chapter 2 introduces these formats, and Chapter 18 shows how to flatten them in Python.
- *(from Ch 1)* | Semi-structured | JSON, XML, app and website logs | Chapters 2, 18, and Part V |
- *(from Ch 1)* Chapter 2, How Computers Store, Move and Protect Data, shows where data lives: files and formats (CSV, Excel, JSON, Parquet), databases, the cloud, and APIs.

#### Chapter 3

- *(from Ch 1)* That single observation explains why so much of a data team's work, and a whole thread of this book from Chapter 3 to the architecture chapters, is about capturing data once, at the source, and letting it flow automatically to reports, dashboards, and other systems.
- *(from Ch 1)* Chapter 3, How a Business Runs on Data, follows one Riverstone order from enquiry to cash, and shows every system that records data along the way.
- *(from Ch 2)* Chapter 3, How a Business Runs on Data, follows one Riverstone order through every system that stores and passes along its data.
- *(from Ch 12)* Before you start: Chapter 1 (what data is), Chapter 3 (how a business runs on data), and Chapters 10–11 (spreadsheets).

#### Chapter 4

- *(from Ch 1)* Chapter 4, Numbers Without Fear, builds the everyday math for working with quantitative data: percentages, growth, and averages.

#### Chapter 6

- *(from Ch 1)* Chapter 6 walks you through installing everything else the book uses.

## Kickoff prompt

```
You are writing Part 0 — First Principles: Data from Zero of the book "Analyst to Architect" (Chapters 3–6; 1 and 2 are approved).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-0-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-0-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```
