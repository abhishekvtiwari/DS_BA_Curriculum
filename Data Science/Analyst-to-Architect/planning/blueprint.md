# Analyst to Architect — Expansion Blueprint

*Version 3 · 16 September 2026 · Working plan for turning the first-edition draft into the complete book · v2 added the automation and integration thread (sections 5, 6, 7) · v3 adds Excel and Google Sheets side by side, and spreadsheet automation with macros, VBA, Office Scripts and Google Apps Script*

---

## 1. The promise of the book

**Who it's for:** someone who knows roughly what "data" means but has never used a data tool, never written a formula beyond `SUM`, never seen SQL or Python.

**What it does:** takes that reader, one step at a time, from *"what is data?"* to a job-ready analyst, and then maps and teaches every step up to data architect: advanced analytics, data science, data engineering, process automation and system integration, production AI, architecture, and leadership. A final part prepares the reader to pass interviews for each role.

**The rules that follow from that promise:**

1. **Assume nothing.** Every term is explained in plain English the first time it appears, with an everyday analogy, before any jargon or code.
2. **Show, don't just tell.** Every concept comes with a worked example on the same fictional company's data, with real, tested output.
3. **Build a job-ready skill set, not a vocabulary.** Every chapter ends with a project and a self-check.
4. **Stay honest.** Keep the current draft's voice: this takes years, every tier is a real job, and here is when *not* to use a tool.
5. **Interview-ready.** A dedicated final part turns everything taught into question banks with graded model answers.

---

## 2. What changes from the current draft

The current draft (33 chapters, ~35k words) is a strong **skeleton**: the career map, the tier structure, the chapter template, and the voice all stay. What it lacks is depth, a true zero-knowledge on-ramp, hands-on examples, several core topics, and interview material.

| Area | Current draft | Expanded book |
|---|---|---|
| Starting point | Assumes the reader already uses spreadsheets at work | **New Part 0** starts from "what is data?" |
| Depth | ~1,000 words per chapter, survey level | 3,000–13,000 words per chapter, teaching level |
| Examples | 4 SQL snippets in the whole book | Tested code and real output in every technical chapter, all on one running dataset |
| Math and formulas | None | Formulas introduced gently, always with a worked numeric example |
| Chapters | 33 + 4 appendices | **83 chapters + 8 appendices** in 9 parts |
| Missing topics | Time series, NLP, recommenders, BA practice, business metrics, data cleaning, visualization, Linux, ingestion, data quality, **spreadsheet automation (macros, VBA, Office Scripts, Google Apps Script), report automation and delivery (including reports in the email body), system integration and reverse ETL, intelligent automation, automation architecture**, FinOps, data strategy | All added as chapters |
| Interview prep | None | **New Part VIII: The Interview Playbook** (15 chapters, ~715 questions, plus cases, take-homes and mock interviews) |
| Exercises | Open-ended projects only | Projects **plus** graded exercises with a full answer key |
| Length | ~35k words | **~480k words**, publishable as 4 volumes (section 4) |

**The sample chapter** delivered with this blueprint (Chapter 12, Databases & SQL Foundations, ~13k words) shows the new standard in practice. The draft's Chapter 4 became that chapter: the same core ideas and voice, but written for a reader who has never seen a database, with every query run and every result shown.

---

## 3. The new chapter standard

Every teaching chapter (Parts 0–VII) follows this structure. Part VIII has its own format (section 8).

| # | Section | Purpose |
|---|---|---|
| 1 | **Chapter at a glance** | What you'll learn, prerequisites (by chapter number), time needed, tools, practice data |
| 2 | **Why this matters** | The real-world stakes, before any theory (kept from the draft) |
| 3 | **In plain English** | An everyday analogy that explains the whole chapter with zero jargon |
| 4 | **Numbered concept sections** (e.g. 12.1, 12.2…) | The teaching, from basic to deeper, each with worked examples on Riverstone data |
| 5 | **Callout boxes** throughout | *Watch out* (traps), *Try it* (30-second exercises), *Dialect note* / *Tool note* (differences between tools), links back to spreadsheet, SQL, or Python equivalents |
| 6 | **Common mistakes and how to spot them** | Table: mistake → symptom → fix |
| 7 | **In the real world** | A realistic workplace scenario solved with the chapter's skills |
| 8 | **Tools** | What to install and use, with alternatives |
| 9 | **The project** | Step-by-step build with milestones and stretch goals; option to use your own work data or the Riverstone dataset |
| 10 | **You've got it when…** | A checklist the reader can tick honestly |
| 11 | **Recap** | The chapter in bullet points |
| 12 | **Practice exercises** | Warm-up, core, stretch, and "think about it" (no-code judgment questions) |
| 13 | **Key terms** | All defined in the Glossary |
| 14 | **Where this leads** | Next chapters, plus a pointer to the matching Part VIII question bank |

**Answers** to all exercises go in Appendix G.

**Quality rules for every chapter:**

- Every code sample is **run before publishing**; every output shown is real.
- Every formula has a **worked numeric example**.
- Every new term is defined **on first use** and added to the Glossary.
- Facts about fast-changing tools (versions, product names, pricing, regulations) are **checked against official sources at the time of writing**, and phrased to age well.
- No interview questions inside teaching chapters (per your decision). A "Where this leads" pointer links to Part VIII instead.

---

## 4. Book architecture at a glance

| Part | Title | Chapters | Target words |
|---|---|---|---|
| 0 | First Principles: Data from Zero | 1–6 | 30,500 |
| I | The Map | 7–9 | 11,500 |
| II | The Analyst | 10–27 | 136,500 |
| III | Advanced Analytics & Analytics Engineering | 28–34 | 34,000 |
| IV | Machine Learning & Data Science | 35–44 | 49,500 |
| V | Data Engineering, Integration & Scale | 45–52 | 37,000 |
| VI | Production ML, Generative AI & MLOps | 53–59 | 34,500 |
| VII | Architecture, Governance & Leadership | 60–67 | 32,000 |
| VIII | The Interview Playbook | 68–82 | 85,500 |
| — | Closing: The Long Game | 83 | 2,500 |
| — | Appendices A–H | — | 43,500 |
| | **Total** | **83 chapters** | **~497,000** |

Word targets include code, tables, and printed outputs. A code-heavy chapter reads faster than its word count suggests.

### Suggested volume split for publishing

One master manuscript; four books that each sell on their own and together form the complete path.

| Volume | Contents | Words | Approx. pages |
|---|---|---|---|
| **1. Foundations & The Analyst** | Parts 0, I, II + Appendices A, B, E, F (analyst sections) | ~187k | ~550 |
| **2. Advanced Analytics & Data Science** | Parts III, IV | ~85k | ~280 |
| **3. Engineering, AI & Architecture** | Parts V, VI, VII + Closing | ~106k | ~350 |
| **4. The Interview Playbook** | Part VIII + role profiles (Appendix H) | ~90k | ~300 |

Volume 4 is the easiest to sell on its own and can be marketed to readers of all three other volumes. Exercise answers (Appendix G) are printed in each volume for that volume's chapters.

---

## 5. Reader pathways

The book is a climb, but not everyone climbs to the top. Chapter 8 includes this table so readers can choose a route.

| Goal | Read fully | Skim | Interview chapters |
|---|---|---|---|
| **Complete beginner, exploring** | 0, I | II (first half) | — |
| **Data Analyst** | 0, I, II (all) | III (28, 30) | 68, 69, 70, 71, 72, 73, 75, 78, 81, 82 |
| **Business Analyst** | 0, I, 10–16, 19–27 | 17–18 | 68, 69, 70, 71, 75, 76, 78, 81 |
| **BI Developer** | 0, I, II, 28, 32 | 45–49, 51, 63 | 68, 69, 70, 71, 77, 78, 81 |
| **Analytics Engineer** | Through III | 45–49, 51 | 68, 69, 71, 72, 77, 81 |
| **Automation / Integration Engineer** | 0, I, 10–20, 25, 29, 34, 45–47, 51, 58, 63 | 52, 55 | 68, 69, 70, 71, 72, 76, 77, 78, 81, 82 |
| **Data Scientist** | Through IV | V, 53–56, 58 | 68, 69, 71–75, 79, 81, 82 |
| **Data Engineer** | Through III, V | IV (35–39), 56, 63 | 68, 69, 71, 72, 77, 78, 81, 82 |
| **ML / AI Engineer** | Through VI | VII | 68, 69, 71, 72, 74, 77, 78, 79, 81, 82 |
| **Data / ML Architect** | Everything | — | 68, 69, 77, 78, 79, 80, 81 |
| **Already an analyst** | Skim 0–II; start fully at III | — | Per target role |

### The automation thread: from source to action

At every tier of the climb, the same practical question comes up: *once the data is right, how does it reach the people and systems that act on it, without someone doing it by hand?* In real companies, a large share of data work is exactly this: moving data from source systems to a finished product (a report file, a report in the body of an email, a dashboard, an alert, or data written into another system such as a CRM or ERP) and keeping that flow running reliably.

The book treats this as a thread through every tier, so the reader's automation skills grow alongside everything else:

| Tier | What automation looks like at this level | Taught in |
|---|---|---|
| **Foundations** | Seeing the manual steps hidden in a business process | Ch 3, 5 |
| **Analyst** | Refreshable spreadsheets; recorded macros, VBA, Office Scripts, and Google Apps Script; scheduled scripts; reports delivered by email (including in the email body); dashboard subscriptions and alerts; low-code flows | Ch 11, 16, 18, **19**, **20** |
| **Business Analyst** | Mapping processes, finding and prioritizing automation opportunities, writing automation requirements | Ch 25 |
| **Advanced analytics & analytics engineering** | Tested, version-controlled, maintainable automations; scheduled dbt jobs; command-line scheduling | Ch 29, 32, 34 |
| **Data engineering** | Orchestrated source-to-warehouse pipelines, data-quality gates before anything is delivered, pushing data back into business systems (reverse ETL, APIs, webhooks), integration platforms, RPA where there's no API | Ch 45–47, **51** |
| **Production ML & AI** | Models and AI agents working inside business workflows, with human approval where it matters | Ch 56, 57, **58** |
| **Architect** | Designing the whole source-to-action flow as one system, choosing the right automation tool for each job (including when to keep, document, or retire legacy macros), and governing every automation in the company | Ch 60, **63** |
| **Interviews** | Spreadsheet automation questions; automation, integration, and report-delivery questions and design cases | Ch 70, **78** |

**One flow, followed through the whole book.** Riverstone's *Daily Sales Flash* starts as a manual Excel report (Ch 11), becomes a SQL query (Ch 12), then a Python script (Ch 18). For teams that live in spreadsheets, it's also rebuilt as a VBA macro in Excel and as a Google Sheet driven by Apps Script (Ch 19). Then it becomes a scheduled HTML email in every manager's inbox (Ch 20), a monitored pipeline with quality checks (Ch 46–47), starts pushing credit-risk flags into the CRM (Ch 51), gains AI-written commentary checked by a person (Ch 58), and finally becomes part of Riverstone's designed reporting and automation platform (Ch 63). Readers see the same business need handled better at each tier, which is exactly how the job grows in real life.

---

## 6. The running example: Riverstone Supplies

A single **fictional** company threads through the whole book, so readers learn new skills on data they already understand, and every part builds on the last.

**Riverstone Supplies** makes and distributes storage boxes, kitchenware, industrial crates, and furniture. It sells to retailers, hotels, and wholesalers across India, runs two manufacturing plants, a sales team, a website, and a customer support desk. It's deliberately similar to a real mid-sized manufacturer, so the examples feel like real work, but every name and number is invented.

### Companion dataset (Appendix E)

Built once, versioned in a companion repository, and used by every chapter. Two sizes: **mini** (tiny tables printed in the book so readers can check answers by eye) and **full** (realistic volume for projects).

| Domain | Tables | Full size | First used in |
|---|---|---|---|
| Sales | customers, products, orders, order_items, employees, targets | mini (Q1 2026, built) · one-year 2025 (built) · full: ~5k customers, ~200k order lines, 3 years | Ch 10–13 |
| CRM | leads, opportunities, activities | ~40k leads | Ch 23, 37, 39 |
| Finance | invoices, payments, expenses, budget | ~60k invoices | Ch 23, 28 |
| Operations | plants, machines, production_runs, inventory, shipments, suppliers | ~300k rows | Ch 14, 40 |
| IoT / sensors | machine_readings (time series) | ~5M rows | Ch 40, 48, 50 |
| Digital | web_sessions, events, ab_test_assignments | ~2M events | Ch 30, 42 |
| Support | tickets, ticket_messages (free text) | ~30k tickets | Ch 41, 55 |
| People | departments, headcount (no personal data) | small | Ch 12, 28 |
| Documents | product manuals, policies, FAQ (text files) | ~200 documents | Ch 55, 57 |
| Automation sandbox | a mock CRM/ERP API, a local test mail server, a webhook receiver, sample purchase-order emails and PDFs | small | Ch 19, 20, 51, 58, 63 |

Data is generated by script with deliberate, documented messiness (missing values, duplicates, typos, late-arriving records, drifting sensors), because learning to handle mess is part of the skill.

**Companion repository contents:** setup scripts for PostgreSQL and MySQL (every SQL chapter also ships a tested MySQL version of its queries), CSV and Parquet files, an automation sandbox (so readers can send test emails, fire webhooks, and write to a mock CRM without touching real systems), one notebook or SQL file per chapter with every example, project starter templates, and the exercise answers.

---

## 7. Chapter-by-chapter plan

**Status key:** **NEW** = not in the draft · **EXPANDED** = the draft's chapter, substantially deepened · **REWRITTEN** = same topic, rebuilt for zero-knowledge readers · **KEPT** = light edit. "Draft Ch" refers to the current manuscript's numbering.

### Front matter

Title page, copyright, dedication, **About the author**, Preface (kept, lightly updated for the new scope), How to Use This Book (updated for the new chapter standard and pathways), Who This Book Is For (kept), Full Table of Contents with page numbers, Conventions used (callout boxes, code formatting, dialect notes), Setting up the companion files.

---

### PART 0 — FIRST PRINCIPLES: DATA FROM ZERO  *(all new)*

*Everything a complete beginner needs before touching a tool.*

**Ch 1. What Is Data?** · NEW · 7,500 words · ✅ **Approved (draft v1, 16 Sep 2026)**
Data vs information vs knowledge vs insight · data all around you (a shopping receipt, a phone's step counter, a train timetable) · structured, semi-structured, unstructured · data types (numbers, text, dates, true/false) · qualitative vs quantitative · levels of measurement (nominal, ordinal, interval, ratio) and why they limit what maths you can do · a row, a column, a record, a dataset · metadata · where data comes from (people, machines, systems) · data quality in one page.
*Project:* Log a week of your own spending in a table and classify every column.

**Ch 2. How Computers Store, Move and Protect Data** · NEW · 8,000 words · ✅ **Approved (draft v1, 16 Sep 2026)**
Bits and bytes; KB → TB with real-world sizes · files, folders, file extensions · common formats: CSV, Excel, JSON, XML, PDF, images, Parquet (introduced only) · what a database is (one-page preview of Ch 12) · servers, the internet, and "the cloud" in plain English · what an API is (the waiter analogy) · backups, versions, passwords, and why data security matters.
*Project:* Open the same small dataset as CSV, Excel, and JSON, and describe the differences.

**Ch 3. How a Business Runs on Data** · NEW · 4,500 words · ✅ **Approved (draft v1, 16 Sep 2026; ~8.4k words)**
The departments of a company and the data each creates (sales, marketing, finance, operations, HR, support) · following one Riverstone order from enquiry to cash: lead → quote → order → production → dispatch → invoice → payment → report · business systems: ERP, CRM, HRMS, POS, e-commerce · transactions vs reports · what a KPI is · dashboards and meetings · who decides what, and why they need data · where manual work hides in a data flow (copy-paste, re-keying, emailing files around).
*Project:* Map the data flow of one process at your workplace, or of a local shop.

**Ch 4. Numbers Without Fear** · NEW · 4,500 words · ✅ **Approved (draft v1, 16 Sep 2026; ~8.4k words)**
Percentages, percentage points vs percent change · ratios and rates · growth, CAGR, compounding · averages (mean, median, mode) and weighted averages · rounding and significant figures · reading tables and charts correctly · basic probability as "how often, out of how many" · orders of magnitude and quick estimation · common number tricks in business news. Every idea is worked with numbers.
*Project:* Check five statistics quoted in news articles or company presentations.

**Ch 5. Thinking Like an Analyst** · NEW · 3,500 words · ✅ **Approved (draft v1, 17 Sep 2026; ~8.0k words)**
Curiosity and asking good questions · turning a vague request into a precise question · hypotheses · breaking problems down (issue trees, MECE) · fact vs opinion vs assumption · spotting misleading charts and claims · bias in how we see data · simple decision-making with data.
*Project:* Take a real business question and build an issue tree with the data each branch needs.

**Ch 6. Setting Up to Learn** · NEW · 2,500 words · ✅ **Approved (draft v1, 17 Sep 2026; ~7.6k words)**
The computer you need (and don't) · installing the book's tools, with links to Appendix B · the companion files · keyboard and file-management basics · how to read documentation · learning with AI assistants without letting them think for you · building a study habit: sample 6-month analyst plan and weekly schedule · how to use the exercises and answer key.
*Project:* Install everything, load the Riverstone mini dataset, and write your 90-day plan.

---

### PART I — THE MAP  *(expanded from draft Part I)*

**Ch 7. The Data Landscape** · EXPANDED from draft Ch 1 · 4,000 words · ✅ **Approved (draft v1, 16 Sep 2026; ~10.9k words; written by the Part I chat)**
Kept: the four questions and the tracks. Added: how data teams are organized (centralized, embedded, hub-and-spoke) · a single project walked through every role, from request to dashboard to model to platform · how AI assistants are changing each role · the process automation and integration track (automation analyst, RPA developer, integration engineer) and why every data role includes some automation · fixes the "three questions" vs four inconsistency.

**Ch 8. The Career Tree: How Skills Unlock Roles** · EXPANDED from draft Ch 2 · 5,000 words · ✅ **Approved (draft v1, 16 Sep 2026; ~11.3k words; written by the Part I chat)**
Kept: tiers, keys and doors. Added: a skills matrix per role · decoding a real-style job description · a day in the life of each role · the reader pathways table and the automation thread (section 5) · entry routes: fresher, career switcher, internal move · aligns the tier order with the book's part order (fixes the draft's tier 3 / tier 4 mismatch).

**Ch 9. How Expertise Actually Forms** · EXPANDED from draft Ch 3 · 2,500 words · ✅ **Approved (draft v1, 16 Sep 2026; ~8.2k words; written by the Part I chat)**
Kept: the honest timeline and the three ingredients. Added: deliberate practice · building a portfolio as you learn · finding feedback and mentors · handling plateaus (moved forward from the Closing chapter so readers get it early).

---

### PART II — THE ANALYST

> **Reading order (decided 17 September 2026).** Part II is taught in blocks: **A. Spreadsheets** (Ch 10, 11, then spreadsheet automation, old Ch 19) · **B. SQL** (old Ch 12, 13) · **C. Python** (old Ch 17, 18) · **D. All tools together** (cleaning, old Ch 14; visualization, old Ch 15; Power BI, old Ch 16; report automation, Ch 20) · **E. Judgment** (Ch 21–27). Part III order: advanced SQL (28), command line (old 34), Python as software (old 29), dbt (old 32), computer science (old 33), inference (old 30), causal inference (old 31). Chapter files keep their current numbers until the coordinator renumbers at assembly; `planning/chapter-map.md` holds the mapping.  *(heavily expanded: 6 draft chapters become 18)*

*Everything needed for a first job as a data analyst or business analyst.*

**Ch 10. Spreadsheet Fundamentals: Excel & Google Sheets** · NEW · 6,000 words · ✅ **Approved (v2, 16 Sep 2026; ~18.9k words; Part II-A chat)**
Every technique shown in **both Excel and Google Sheets**, side by side, with differences flagged · workbooks, sheets, cells, ranges · entering and formatting data · formulas and cell references (relative, absolute, mixed) · essential functions: `SUM`, `AVERAGE`, `COUNT`, `IF`, `COUNTIFS`, `SUMIFS`, text and date functions · sorting, filtering, tables · charts · data validation and conditional formatting · keyboard shortcuts for both · Google Sheets strengths: real-time collaboration, sharing and permissions, version history, Google Forms feeding a sheet · file formats and moving between Excel and Sheets without breaking things.
*Project:* Build a clean monthly sales tracker for Riverstone from a raw export.

**Ch 11. The Spreadsheet, Mastered: Excel & Google Sheets** · EXPANDED from draft Ch 5 · 7,000 words · ✅ **Approved (v2, 17 Sep 2026; ~26.0k words; Part II-A chat)**
Lookups (`XLOOKUP`, `INDEX`/`MATCH`, in both tools) · pivot tables and pivot charts in depth · dynamic arrays (`FILTER`, `UNIQUE`, `SORT`) · Power Query step by step · Power Pivot and a first taste of DAX · what-if analysis, Goal Seek · Google Sheets power features: `QUERY` (SQL-like formulas), `ARRAYFORMULA`, `IMPORTRANGE` across files, Sheets pivot tables, connecting Sheets to a data warehouse · what Excel does that Sheets can't (Power Query, Power Pivot) and the Sheets alternatives · spreadsheet hygiene and auditing · when to leave the spreadsheet. (Automating spreadsheets with macros and scripts: Ch 19.)
*Project:* Rebuild a messy monthly workbook so next month is one refresh.

**Ch 12. Databases & SQL Foundations** · REWRITTEN from draft Ch 4 · 30,000 words · ✅ **Approved v3 (16 Sep 2026); v4 adds §12.13, awaiting review**
Tables, types, keys, relationships, ER diagrams (drawn figures), normalization intuition · real-life examples throughout (profit and margin, overdue invoices, receivables ageing) · `SELECT`, `WHERE`, NULL logic, `ORDER BY`, `CASE`, dates, text · aggregates, `GROUP BY`, `HAVING` · every join type, anti-joins, self-joins, fan-out · execution order · subqueries, set operations · **§12.13 building and changing a database in PostgreSQL and MySQL side by side**: `CREATE DATABASE`/`TABLE`, types, constraints (`NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, foreign keys), `INSERT` (errors, ID gaps, `RETURNING`/`LAST_INSERT_ID`), CSV loading, `UPDATE` (with joins), `DELETE` and `ON DELETE` options, soft delete, upsert, transactions and MySQL's implicit commit, `ALTER TABLE` (add/rename/drop/modify columns, the MySQL `MODIFY` trap, constraints), renaming, schemas, `TRUNCATE`/`DROP`, safe production changes, cheat sheet · SQL style · a worked "Monday morning" section answering four business questions with a six-step method · **installing both PostgreSQL and MySQL** (current LTS; Windows MSI + MySQL Configurator, macOS DMG, Linux APT; DBeaver or MySQL Workbench; first-connection troubleshooting) · §12.16 *The same SQL in MySQL*: differences table, the three silent traps (date subtraction, case-insensitive collation, `||`), NULL ordering, `FULL OUTER JOIN` workaround, portable-SQL habits, MySQL exercise track.
*Project:* Rebuild a real report in SQL and reconcile it.

**Ch 13. SQL for Real Analysis** · NEW (absorbs part of draft Ch 10) · 16,500 words · ✅ **Approved (draft v1.1, 16 Sep 2026)**
CTEs · window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`/`LEAD`, running totals, moving averages, `SUM() OVER ()`) · the analyst's pattern library: top-N per group, month-over-month and year-over-year, cumulative totals, deduplication, first/last event, funnels, basic cohort retention, gaps and islands (intro) · data-quality checks in SQL · building a SQL snippet library · §13.8 *Running this chapter in MySQL*: recursive-CTE date spine, `cte_max_recursion_depth`, `SUM(CASE)` pivots, reserved words.
*Project:* A reusable SQL pack for Riverstone's weekly sales review.

**Ch 14. Data Cleaning & Preparation** · NEW · 6,000 words · ✅ **Approved (v1, 17 Sep 2026; ~17.3k words; Part II-A chat)**
Why most analysis time is cleaning · profiling a new dataset · missing values (types and treatments) · duplicates and fuzzy duplicates · inconsistent categories and typos · outliers: error or reality? · dates, time zones, and units · joining messy sources · validation rules · documenting every cleaning decision. Shown side by side in Excel/Power Query, SQL, and (preview) pandas.
*Project:* Clean Riverstone's operations export and write a data-quality report.

**Ch 15. Data Visualization Principles** · NEW · 4,000 words · ✅ **Approved (v1, 17 Sep 2026; ~14.1k words; Part II-A chat)**
How people read charts (perception basics) · choosing the right chart for the question · bar, line, scatter, histogram, box plot, heatmap, map: when each works · color with meaning · labels, titles that state the finding · misleading charts and how to avoid making them · accessibility · before-and-after makeovers.
*Project:* Redesign five poor charts from Riverstone's old management pack.

**Ch 16. Business Intelligence with Power BI** · EXPANDED from draft Ch 6 · 7,000 words
Power BI Desktop and Service · Power Query · star-schema modeling hands-on · DAX from zero: measures vs calculated columns, `CALCULATE`, filter context, time intelligence · report design · publishing, sharing, refresh, row-level security · translating concepts to Tableau, Looker, and the free Looker Studio (popular with Google Sheets users) · where BI tools are heading (verify current product state when writing).
*Project:* A live Riverstone sales dashboard that replaces the manual report.

**Ch 17. Python from Zero** · NEW · 6,000 words
What programming is · installing Python and Jupyter · variables and types · lists, dictionaries · conditions and loops · functions · reading and writing files · errors and how to read them · packages · writing your first useful script · getting unstuck.
*Project:* A script that reads a folder of CSVs and prints a summary of each.

**Ch 18. Python for Analysts: pandas & Automation** · EXPANDED from draft Ch 7 · 8,000 words
DataFrames · reading CSV, Excel, SQL, APIs · selecting and filtering · `groupby`, `merge`, `pivot_table`, `melt` · dates and time series basics · cleaning with pandas · charts with matplotlib and seaborn · exporting formatted Excel · automating a report end to end · vectorized thinking. (Delivery and scheduling continue in Ch 20.)
*Project:* Automate Riverstone's monthly report from database to formatted Excel.

**Ch 19. Spreadsheet Automation: Macros, VBA, Office Scripts & Google Apps Script** · NEW · 7,000 words
Why so much real-world automation still lives inside spreadsheets, and when that's the right choice (or the wrong one) · **Excel macros:** recording a macro, macro-enabled files (`.xlsm`), macro security and trusted locations, the Personal Macro Workbook, assigning macros to buttons · **VBA from zero**, building on the programming ideas from Ch 17: the editor, the object model (`Application`, `Workbook`, `Worksheet`, `Range`, `Cells`), variables, `If`, loops, `With` · the everyday VBA toolkit: finding the last row, looping through sheets, consolidating every file in a folder, cleaning and formatting, building a pivot, saving as PDF, sending Outlook emails with the report attached or in the body · custom worksheet functions (UDFs) · simple UserForms · debugging (breakpoints, the Immediate window) and error handling (`On Error`) · making VBA fast (turning off screen updating, working with arrays instead of cell by cell) · **Office Scripts** for Excel on the web and how they connect to Power Automate (availability depends on the Microsoft 365 plan; verified at time of writing) · **Google Sheets macros and Apps Script** (JavaScript): `SpreadsheetApp`, reading and writing ranges in batches, custom functions, menus, triggers (time-driven, on edit, on form submit), sending HTML emails with `MailApp`/`GmailApp`, calling APIs with `UrlFetchApp` to pull data from a CRM, quotas and authorization · **living with macros responsibly:** documentation, avoiding hard-coded paths and passwords, version control for scripts, the "only one person understands this macro" risk, and when to migrate to Python, Power Query, or a pipeline.
*Project (two parts):* (1) An Excel VBA macro that consolidates Riverstone's 12 branch sales files into one master sheet, builds a summary, saves a PDF, and emails it through Outlook. (2) A Google Sheets workflow: an order-enquiry Google Form fills a sheet, Apps Script sends each customer an acknowledgement email, and a time-driven trigger sends the sales team a 9 a.m. summary in the email body.

**Ch 20. Automating Reports & Delivering Insights** · NEW · 6,000 words
The analyst's automation ladder: manual → refreshable → scheduled → triggered → self-serve · mapping a report's flow from source to finished product and spotting the manual steps · output formats: formatted Excel, PDF, CSV extracts · **reports in the email body**: HTML tables, KPI tiles, and charts that display correctly in Outlook and Gmail · sending email safely from code (SMTP, Microsoft 365 and Google Workspace APIs) · dashboard subscriptions and data-driven alerts · chat notifications (Teams, Slack, WhatsApp Business) · scheduling: Task Scheduler, cron, cloud schedulers · low-code automation: Power Automate and n8n/Make/Zapier introduced (spreadsheet-based options were covered in Ch 19) · choosing how to deliver: VBA, Apps Script, Python, or a low-code flow · exception reports and threshold alerts ("only tell me when something is wrong") · making automations trustworthy: logging, failure alerts, "no data today" handling, managing recipient lists, never sending confidential data to the wrong people · documenting and handing over an automation · measuring hours saved. (Tool capabilities verified at time of writing.)
*Project:* Riverstone's *Daily Sales Flash*: SQL → pandas → an HTML email with KPI tiles, a table, and a chart, sent to managers every morning at 8 a.m., plus a low-stock exception alert and an alert to you if the job fails.

**Ch 21. Descriptive Statistics & Probability** · NEW (absorbs part of draft Ch 8) · 6,000 words
Mean, median, mode · spread: range, variance, standard deviation, IQR · percentiles · shapes of data: skew, outliers · key distributions with business examples: normal, binomial, Poisson, uniform · probability rules, conditional probability · Bayes' rule with a worked example · sampling and the central limit theorem, shown by simulation.
*Project:* Profile Riverstone's order values and delivery times statistically.

**Ch 22. Statistics Without Fooling Yourself** · EXPANDED from draft Ch 8 · 5,000 words
Kept: the "don't fool yourself" spirit. Added with worked examples: confidence intervals · hypothesis testing intuition · p-values done properly · Type I and Type II errors · correlation vs causation, confounders · Simpson's paradox with real numbers · survivorship, selection, and other biases · communicating uncertainty.
*Project:* Re-examine a past conclusion and rewrite it honestly.

**Ch 23. Business Acumen, KPIs & Metrics** · NEW · 6,000 words
How a business makes money · reading a P&L, balance sheet, and cash flow in plain English · metrics by function: sales (pipeline, win rate, AOV), marketing (funnel, CAC, ROAS), finance (margin, working capital, DSO), operations (OEE, inventory turns, OTIF), product and customer (retention, churn, LTV, NPS) · metric trees and North Star metrics · root-cause analysis of a metric change · good vs vanity metrics.
*Project:* Build a KPI tree for Riverstone and diagnose a revenue dip.

**Ch 24. Requirements, Storytelling & Stakeholders** · EXPANDED from draft Ch 9 (part) · 4,000 words
Requirements gathering: turning asks into questions, documenting business rules · stakeholder mapping · storytelling with data: bottom line up front, one message per slide · writing a one-page analysis memo · presenting to executives · handling pushback and "can you just change the number?"
*Project:* Turn one analysis into a memo and a three-slide story.

**Ch 25. The Business Analyst Track** · NEW · 5,000 words
What BAs do and how it differs from data analysts · the software development life cycle (SDLC) · process mapping (flowcharts, swimlanes, BPMN basics) · use cases and user stories, acceptance criteria · BRD, FRD, and SRS documents · gap analysis · UAT · working with IT and vendors · domain knowledge · identifying and prioritizing automation opportunities, and writing requirements for an automation.
*Project:* Map Riverstone's order-to-cash process and write user stories for one improvement.

**Ch 26. The Professional Toolkit: Git, Agile, Documentation & AI Assistants** · EXPANDED from draft Ch 9 (part) · 4,000 words
Git and GitHub hands-on · reproducibility · documentation that people read · Agile, Scrum, Kanban, Jira in practice · working with AI coding and writing assistants: what to delegate, how to check the output, data-privacy rules.
*Project:* Put all Part II work in one repository with a README.

**Ch 27. Capstone: Your Analyst Portfolio** · NEW · 3,000 words
End-to-end Sales Intelligence project: SQL → cleaning → Python automation → Power BI dashboard → statistical insight → memo · how to present portfolio projects · what "job-ready" looks like.

---

### PART III — ADVANCED ANALYTICS & ANALYTICS ENGINEERING

**Ch 28. Advanced SQL, Performance & Data Modeling** · EXPANDED from draft Ch 10 · 7,000 words
Recursive CTEs (org charts, bills of materials) · advanced window frames · indexes and `EXPLAIN` · normalization (1NF–3NF) worked properly · dimensional modeling: facts, dimensions, grain, star vs snowflake · slowly changing dimensions (types 1, 2, 3) with worked examples · denormalization trade-offs. Fixes the draft's incorrect "CTEs in Part II" reference. · schema migrations: versioned, reviewed change scripts and migration tools
*Project:* Model Riverstone's sales into a star schema with an SCD type 2 customer dimension.

**Ch 29. Python as Software, Not Scripts** · EXPANDED from draft Ch 11 · 5,000 words
Kept topics, now with full code: project structure, functions and modules, classes, virtual environments and lockfiles, `pytest`, type hints, logging, error handling, robust API clients (pagination, retries, rate limits), code review.
*Project:* Turn the Ch 18 script into a tested package.

**Ch 30. Inference & Experiments** · EXPANDED from draft Ch 12 · 6,000 words
Standard error and confidence intervals computed · t-test, chi-square, ANOVA with worked examples · effect size · power and sample size calculated step by step · A/B test design and analysis end to end · pitfalls (peeking, multiple testing, novelty, sample-ratio mismatch) · linear and logistic regression for inference.
*Project:* Design and analyze Riverstone's website A/B test.

**Ch 31. Causal Inference Without Experiments** · NEW · 3,500 words
Why observational data misleads · difference-in-differences · matching and propensity scores · regression discontinuity · synthetic control (intro) · instrumental variables (intuition only) · when to trust these methods.
*Project:* Estimate the effect of a regional price change with difference-in-differences.

**Ch 32. Analytics Engineering with dbt** · EXPANDED from draft Ch 13 · 5,000 words
ETL vs ELT · dbt models, sources, refs, the DAG · staging, intermediate, marts · tests, documentation, lineage · incremental models · macros (intro) · CI for dbt · SQL linting · semantic layers (verify current tooling when writing).
*Project:* A tested dbt project feeding the Power BI dashboard.

**Ch 33. The Computer Science You Actually Need** · EXPANDED from draft Ch 14 · 4,500 words
Big-O with timed experiments · lists, dictionaries, sets, stacks, queues, trees, graphs · searching and sorting · recursion · hashing · the dynamic programming and greedy ideas · what coding interviews test (pointer to Ch 72).
*Project:* Speed up a slow Riverstone matching script and measure it.

**Ch 34. The Command Line, Linux & Networking Basics** · NEW · 3,000 words
Why engineers live in the terminal · navigating files · pipes and redirection · `grep`, `head`, `wc`, `awk` basics · permissions · environment variables · SSH · shell scripts · networking in plain English: IP, DNS, ports, HTTP.
*Project:* A shell script that downloads, checks, and archives a daily file.

---

### PART IV — MACHINE LEARNING & DATA SCIENCE

**Ch 35. The Math Under the Models** · EXPANDED from draft Ch 15 · 6,000 words
Now with formulas and worked numbers: vectors, dot product, matrices · derivatives and gradients · gradient descent computed by hand for three steps, then in NumPy · probability distributions, likelihood, maximum likelihood · entropy and cross-entropy · PCA worked on a small example.
*Project:* Gradient descent and PCA from scratch.

**Ch 36. The Machine Learning Workflow & Feature Engineering** · NEW (splits draft Ch 16) · 5,000 words
Framing problems · train/validation/test splits and cross-validation · data leakage with real examples · feature engineering: scaling, encoding categoricals, dates, text, aggregates · missing values in ML · scikit-learn pipelines · baselines.
*Project:* A leakage-free feature pipeline for Riverstone lead scoring.

**Ch 37. Supervised Learning Algorithms** · EXPANDED from draft Ch 16 · 8,000 words
How each algorithm works, when to use it, key settings: linear regression, regularization (ridge, lasso, elastic net), logistic regression, k-nearest neighbors, Naive Bayes, decision trees (Gini, entropy, worked split), random forests, gradient boosting (XGBoost, LightGBM, CatBoost), support vector machines · bias–variance with learning curves · hyperparameter tuning.
*Project:* Lead-scoring model: baseline vs boosting.

**Ch 38. Unsupervised Learning** · NEW (splits draft Ch 16) · 4,500 words
k-means step by step, choosing k · hierarchical clustering · DBSCAN · dimensionality reduction: PCA, t-SNE, UMAP · anomaly detection (isolation forest) · market basket analysis (association rules) · evaluating unsupervised results.
*Project:* Customer segmentation and a product-bundle analysis.

**Ch 39. Evaluation, Tuning, Interpretation & Honesty** · EXPANDED from draft Ch 17 · 5,500 words
Confusion matrix with formulas and worked numbers · precision, recall, F1, ROC-AUC, PR-AUC · regression metrics · calibration · threshold selection by business cost (worked) · imbalanced data (class weights, resampling, SMOTE) · SHAP and partial dependence · fairness checks · model cards.
*Project:* Cost-based evaluation and explanation of the lead-scoring model.

**Ch 40. Time Series & Forecasting** · NEW · 6,000 words
Trend, seasonality, cycles, noise · stationarity · moving averages and exponential smoothing · ARIMA/SARIMA intuition and practice · forecasting libraries · machine learning for forecasting (lag features) · backtesting · forecast accuracy (MAPE, WAPE) · demand forecasting for a manufacturer · anomaly detection in sensor data.
*Project:* Forecast Riverstone's monthly demand by product category.

**Ch 41. NLP Foundations** · NEW · 4,000 words
Text as data · cleaning and tokenization · bag of words, TF-IDF · sentiment analysis · text classification · topic modeling · word embeddings as the bridge to LLMs.
*Project:* Classify and summarize Riverstone support tickets by topic.

**Ch 42. Recommender Systems & Ranking** · NEW · 3,500 words
Popularity baselines · content-based filtering · collaborative filtering and matrix factorization (intuition) · implicit feedback · evaluation (precision@k, NDCG) · cold start · business uses in B2B cross-selling.
*Project:* "Customers who bought this also bought" for Riverstone.

**Ch 43. A First Look at Deep Learning** · EXPANDED from draft Ch 18 · 4,500 words
Kept structure; added a neuron computed by hand, a small network in PyTorch with full code, and a transfer-learning walk-through.

**Ch 44. Capstone: An End-to-End Data Science Project** · NEW · 2,500 words
From business question to validated, explained, documented model, presented to non-technical leaders.

---

### PART V — DATA ENGINEERING, INTEGRATION & SCALE

**Ch 45. Data Ingestion & Integration** · NEW · 4,000 words
Sources: databases, files, APIs, events, SaaS tools · full vs incremental loads · change data capture · managed connectors vs custom code (build vs buy) · loading CSV and Parquet reliably · schema changes · web data and its legal and ethical limits.
*Project:* Incrementally ingest Riverstone orders and CRM data into a warehouse.

**Ch 46. Pipelines & Orchestration** · EXPANDED from draft Ch 19 · 4,500 words
Kept concepts; added a full Airflow (or Dagster) example, idempotency demonstrated with a failure test, backfills, alerting · triggering downstream delivery (reports, emails, syncs) only after the data passes its checks.

**Ch 47. Data Quality, Observability & Contracts** · NEW · 3,500 words
Dimensions of data quality · testing data in pipelines · anomaly and freshness monitoring · lineage · data contracts in practice · incident handling for data.
*Project:* Add quality checks and freshness alerts to the Ch 46 pipeline.

**Ch 48. Big Data & Distributed Compute** · EXPANDED from draft Ch 20 · 4,500 words
Kept "most big data isn't"; added PySpark code on the sensor dataset, reading a query plan, finding a shuffle, and a timed comparison with DuckDB and Polars.

**Ch 49. Storage, Warehouses & Lakehouses** · EXPANDED from draft Ch 21 · 5,000 words
Added ACID explained properly · row vs columnar storage demonstrated · partitioning and file sizing · table formats hands-on · warehouse cost and performance basics. Fixes the draft's broken "Chapter 2" reference.

**Ch 50. Streaming & Real-Time** · EXPANDED from draft Ch 22 · 4,500 words
Added a working Kafka producer/consumer example, windowing and late data demonstrated, and a plant sensor-monitoring case.

**Ch 51. Data Activation: Reverse ETL, APIs & System Integration** · NEW · 5,500 words
Why data sitting in a dashboard changes nothing on its own: closing the loop from source to action · the full flow: source systems → ingestion → warehouse → data products (reports, emails, dashboards) → **back into operational systems** · reverse ETL: syncing warehouse data (lead scores, customer health, credit limits, reorder flags) into CRM, ERP, and marketing tools · writing to systems through APIs: authentication (API keys, OAuth), upserts, pagination, rate limits, retries, idempotent writes, choosing the system of record and conflict rules · webhooks and event-driven triggers · integration patterns: point-to-point, hub-and-spoke, message queues, integration platforms (iPaaS) · choosing between custom code, orchestrator tasks, low-code/iPaaS tools, and enterprise integration platforms · RPA for systems with no API, and why it's fragile · file-based integrations (SFTP drops, EDI) that remain common in manufacturing and B2B · audit trails, reconciliation reports, and rollback · keeping credentials secure.
*Project:* A nightly, idempotent sync of Riverstone lead scores and overdue-invoice flags into a sandbox CRM through its API, with a reconciliation report, plus a webhook that alerts sales within a minute when a high-value lead arrives.

**Ch 52. The Cloud, Containers & Infrastructure as Code** · EXPANDED from draft Ch 23 · 5,500 words
Added cloud fundamentals (regions, identity and access, networking) · a Dockerfile built step by step · Kubernetes concepts · a small Terraform example · CI/CD with GitHub Actions. Fixes the "Parts V so far" typo and the FinOps forward reference (now to Ch 65).

---

### PART VI — PRODUCTION ML, GENERATIVE AI & MLOPS

**Ch 53. Deep Learning in Depth** · EXPANDED from draft Ch 24 · 5,500 words
Kept architectures; added training techniques (normalization, dropout, schedulers), **quantization and model compression** (fixes the draft's broken reference from LLMOps), computer vision for manufacturing defect detection, transformers explained step by step with a toy attention calculation.

**Ch 54. Generative AI & Large Language Models** · EXPANDED from draft Ch 25 (part) · 5,500 words
How LLMs are built and trained · tokens, context windows, sampling · prompting techniques with examples · embeddings · fine-tuning and parameter-efficient methods · multimodal models · limits and risks. (Model and vendor landscape verified at time of writing.)

**Ch 55. Building AI Applications: RAG, Agents & Evaluation** · NEW (splits draft Ch 25) · 5,500 words
RAG end to end: chunking, embeddings, vector search, reranking, grounding, citations · tool use and agents · evaluating AI applications (golden sets, LLM-as-judge, human review) · guardrails · a Riverstone product-support assistant built step by step.

**Ch 56. MLOps: Making Models Survive Production** · EXPANDED from draft Ch 26 · 5,000 words
Added full examples: MLflow tracking, model registry, FastAPI serving, Docker, drift detection computed, retraining triggers, feature stores.

**Ch 57. LLMOps** · EXPANDED from draft Ch 27 · 4,000 words
Kept components; added prompt versioning and regression tests, tracing, cost per request calculated, routing and caching examples, security (prompt injection) examples.

**Ch 58. Intelligent Automation: AI Inside Business Workflows** · NEW · 4,500 words
Where AI fits in a process: classify, extract, summarize, decide, act · processing documents and emails (purchase orders, invoices, customer requests) with extraction plus validation against master data · AI-written commentary for automated reports, checked against the numbers before sending · agents that take actions across systems: permissions, approval steps, and limits · human-in-the-loop design and confidence thresholds · measuring accuracy, time saved, and the cost of errors · failure modes (a wrong value written into the ERP) and guardrails · cost per automated transaction.
*Project:* Automated purchase-order intake: read incoming PO emails and PDFs, extract fields with an LLM, validate them against Riverstone's product and customer master, create draft orders in the sandbox system, and route low-confidence cases to a person.

**Ch 59. Industry Case Studies** · NEW · 4,500 words
Nine end-to-end cases, each showing problem → data → approach → architecture → results → lessons: manufacturing quality, demand planning, B2B lead scoring, retail pricing, banking fraud, logistics routing, customer support automation, predictive maintenance, end-to-end order-to-cash reporting and automation.

---

### PART VII — ARCHITECTURE, GOVERNANCE & LEADERSHIP

**Ch 60. Designing Whole Systems** · EXPANDED from draft Ch 28 · 4,500 words
Added a full worked design document for a Riverstone analytics and AI platform, with C4 diagrams and an architecture decision record.

**Ch 61. Distributed Systems & Trade-offs** · EXPANDED from draft Ch 29 · 4,000 words
Added PACELC · consistency models with concrete examples · a failure analysis of the Part V stack.

**Ch 62. Data Architecture Patterns** · EXPANDED from draft Ch 30 · 4,000 words
Added worked comparisons of Lambda/Kappa/medallion on one scenario, data mesh maturity checks, and data products in practice.

**Ch 63. Automation Architecture & Governance** · NEW · 4,500 words
Designing the flow from source to final product (report file, email report, dashboard, alert, write-back into another system) as one architecture rather than a pile of scripts · process discovery and prioritizing automations by value, risk, and effort, with an ROI worked example · choosing the right tool for each job (decision matrix): spreadsheet macro or script, scheduled script, BI subscription, low-code flow, orchestrated pipeline, integration platform, RPA, AI agent · a reference architecture: sources → ingestion → warehouse → semantic layer → delivery and activation layer → monitoring · scheduled vs event-driven designs · shared services: notification service, credential vault, run logs, alerting · ownership, runbooks, and support · controlling automation sprawl and shadow IT (including business-critical macros nobody owns): an automation inventory, standards, and a center of excellence · controls: approvals, segregation of duties, audit trails, change management · retiring automations safely.
*Project:* A design document for Riverstone's reporting and automation platform, replacing 40 manual reports, legacy VBA macros, Apps Script projects, and scattered scripts.

**Ch 64. Security, Privacy, Governance & Responsible AI** · EXPANDED from draft Ch 31 · 5,000 words
Added identity and access patterns · encryption basics · privacy laws by region, including India's data-protection law, GDPR, and AI regulation (all verified against official sources at writing time, with "not legal advice" framing) · data catalogs and stewardship · a fairness audit worked example.

**Ch 65. FinOps: The Economics of Data Platforms** · NEW · 3,000 words
How cloud billing works · cost drivers in warehouses, compute, and AI · unit economics (cost per report, per prediction, per AI request) · budgets, tagging, and showback · cost-aware architecture decisions.

**Ch 66. Data Strategy, Maturity & Building Data Teams** · NEW · 3,500 words
Data strategy on a page · maturity models · building the case and ROI for data projects · hiring and structuring teams · vendor selection · change management and data culture.

**Ch 67. The Architect as Leader** · KEPT/EXPANDED from draft Ch 32 · 3,500 words
Kept; added real-style scenarios (influencing without authority, saying no, presenting to a board), and a first-90-days plan for a new architect.

---

### PART VIII — THE INTERVIEW PLAYBOOK  *(all new; design in section 8)*

| Ch | Title | Contents | Words |
|---|---|---|---|
| 68 | How Data Hiring Works | Interview rounds for each role · what each round tests · CVs that pass screening software and humans · portfolio and LinkedIn · referrals · preparing in 30/60/90 days | 4,000 |
| 69 | The Extra-Points Method | The answer framework, scoring rubric, and extra-point moves (section 8), practiced on 20 examples | 5,000 |
| 70 | Excel, Google Sheets, VBA & BI Question Bank | ~75 questions: formulas and lookups in Excel and Sheets, pivots, Power Query, `QUERY` and `ARRAYFORMULA`, macros, VBA and Apps Script (including reading and fixing a broken macro), DAX, data modeling, dashboard critique | 6,000 |
| 71 | SQL Question Bank | ~100 questions: concepts, NULL and join puzzles, window functions, classic problems (Nth highest, duplicates, streaks, retention), PostgreSQL vs MySQL dialect questions, query optimization, live-coding walk-throughs | 9,000 |
| 72 | Python & pandas Question Bank | ~70 questions: language basics, data structures, pandas tasks, debugging, coding problems at data-role difficulty | 6,000 |
| 73 | Statistics, Probability & Experimentation Bank | ~70 questions: probability puzzles, distributions, hypothesis tests, A/B test design and debugging, causal questions | 6,000 |
| 74 | Machine Learning Question Bank | ~90 questions: algorithms, bias–variance, metrics, leakage, feature engineering, model debugging, ML case studies | 8,000 |
| 75 | Product Sense, Metrics, Case Studies & Guesstimates | ~40 business cases ("revenue fell 20%…", "design a KPI dashboard for…") + 20 guesstimates, all solved with a structure | 7,000 |
| 76 | Business Analyst Question Bank | ~50 questions: requirements, process mapping, user stories, SDLC, UAT, stakeholder scenarios | 4,500 |
| 77 | Data Engineering & Data System Design Bank | ~50 questions + 8 full design walk-throughs (e.g. "design a daily sales pipeline", "design real-time sensor monitoring") | 6,500 |
| 78 | Automation & Integration Question Bank | ~45 questions: choosing between macros, scripts, Python and low-code tools, report automation, email and alert delivery, scheduling, APIs and webhooks, reverse ETL, low-code vs code vs RPA, failure handling and monitoring · 4 design cases (e.g. "automate a daily MIS email for 200 managers", "sync lead scores into the CRM without duplicates", "an automation silently stopped last week: how do you find out and prevent it?") | 4,500 |
| 79 | GenAI, LLM & MLOps Question Bank | ~50 questions + 4 design cases (RAG assistant, model-serving platform) | 5,500 |
| 80 | Architecture & Leadership Question Bank | ~35 questions + 5 architecture cases for senior and architect roles | 3,500 |
| 81 | Behavioral, HR & Offer Conversations | ~40 behavioral questions with STAR examples, building your story bank, questions to ask interviewers, handling offers | 4,000 |
| 82 | Take-Home Assignments & Mock Interviews | 6 complete take-home assignments with model submissions · 8 full mock interview scripts (analyst, BA, DS, DE, ML, architect) with interviewer notes and scoring | 6,000 |

---

### CLOSING

**Ch 83. The Long Game** · KEPT from draft Ch 33 · 2,500 words
Kept almost entirely (it's one of the draft's strongest chapters). The "expect plateaus" material also appears early in Ch 9.

---

### APPENDICES

| | Title | Contents | Words |
|---|---|---|---|
| A | Glossary | ~400 terms, plain-English definitions, chapter reference for each | 8,000 |
| B | Tool Index & Installation Guide | Every tool by category; step-by-step install notes (including PostgreSQL and MySQL on Windows, macOS, and Linux), kept current in the companion repository | 3,000 |
| C | The Project Bank | Every project and capstone, as a portfolio roadmap per role | 3,000 |
| D | Choosing Good Resources | Kept from the draft, lightly expanded | 1,500 |
| E | Practice Datasets & Companion Repository | Riverstone data dictionary, schema diagrams, setup instructions | 2,000 |
| F | Cheat Sheets | Excel, SQL, DAX, pandas, Git, Linux, statistics formulas, ML metrics, one to two pages each | 8,000 |
| G | Answers to Chapter Exercises | Full worked answers for every exercise in Parts 0–VII | 14,000 |
| H | Role Profiles | One page per role: responsibilities, skills, tools, career moves, matching chapters | 4,000 |
| — | Index | Built at typesetting | — |

---

## 8. Part VIII design: the Extra-Points Method

Most interview-prep books give one "correct" answer per question. But interviewers rarely score answers as simply right or wrong. Two candidates can both give a correct answer and get very different marks. The difference is *how* they answer: whether they clarify, structure, handle edge cases, think about the business, and check their own work.

Part VIII teaches that difference explicitly. Every core question shows **three answers side by side**, so the reader can see exactly what earns extra points.

### 8.1 How interviewers score (taught in Ch 69)

Across data roles, answers are typically judged on five dimensions. Each bank's model answers are written against this rubric.

| Dimension | 1 — Weak | 2 — Acceptable | 3 — Strong | 4 — Outstanding |
|---|---|---|---|---|
| **Correctness** | Wrong or incomplete | Correct for the simple case | Correct, including common edge cases | Correct, and explains *why* alternatives fail |
| **Structure & communication** | Rambling, jumps around | Understandable | Clear steps, signposted | Simple first, then depth; easy to follow for any audience |
| **Depth & edge cases** | None considered | Mentions one when prompted | Raises the important ones unprompted | Tests them, and explains the risk each creates |
| **Business judgment** | Purely technical | Mentions the business | Ties the answer to a decision or metric | Quantifies impact; proposes next actions |
| **Collaboration** | Doesn't clarify; defensive with hints | Accepts hints | Asks good clarifying questions | Checks assumptions, adapts, summarizes agreement |

### 8.2 The twelve extra-point moves

These are the habits that lift an answer from "acceptable" to "outstanding". Ch 69 teaches each with examples, and the banks label them wherever they appear (e.g. **[+Edge cases]**).

1. **Clarify first.** Restate the question and ask the one or two questions that change the answer.
2. **State assumptions** out loud when you can't ask.
3. **Signpost your structure:** "I'll cover three things: the definition, an example, and when it breaks."
4. **Simple answer first, depth second.** Give the one-line version, then go deeper.
5. **Raise edge cases:** NULLs, duplicates, ties, empty inputs, time zones, outliers, late data.
6. **Offer trade-offs and alternatives:** "Option A is simpler; option B scales better. I'd choose A unless…"
7. **Validate the result:** a sanity check, a hand calculation, a reconciliation to a known total.
8. **Connect to business impact:** what decision this informs, what it's worth.
9. **Think about scale and maintenance:** performance, cost, who maintains it.
10. **Admit limits honestly** and say how you'd find out.
11. **Use real evidence:** a project from your portfolio or job.
12. **Close the loop:** summarize, and check that you answered what was asked.

### 8.3 The question entry format

Each **core question** (about a third of each bank) uses the full format below. The rest are **rapid-fire questions**: a model answer plus one "extra point" line. Each bank ends with a **Final-week revision list** of its 20 must-know questions.

```
Q[bank]-[number]  Question text
Level: Foundation | Intermediate | Advanced      Roles: DA · BA · BI · AE · DS · DE · MLE · Architect
Round: Screening | Technical | Live coding | Case | System design | Behavioral
What they're really testing: …
Answer that passes:          (scores ~2)
Strong answer:               (scores ~3)
Extra-points answer:         (scores ~4, with the moves labeled)
Likely follow-ups: …
Red flags that lose points: …
Learn it in: Chapter …
```

### 8.4 Three sample entries

---

**Q71-014 · Find customers who have never placed an order.**

**Level:** Foundation · **Roles:** DA, BA, BI, AE, DS, DE · **Round:** Live coding
**What they're really testing:** whether you understand joins beyond the inner join, and whether you know the NULL traps.

**Answer that passes**

```sql
SELECT customer_name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders);
```

It works on clean data. It says nothing about why, and it has a hidden flaw.

**Strong answer**

"I'll use a left join and keep only customers with no matching order:"

```sql
SELECT c.customer_id, c.customer_name
FROM customers AS c
LEFT JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

"A left join keeps every customer. Where there's no order, the order columns are NULL, so filtering on `o.order_id IS NULL` leaves exactly the customers without orders. I check the order's primary key because it can never be NULL on a real match."

**Extra-points answer**

- **[+Clarify]** "Should a customer whose only order was *cancelled* count as having ordered? That changes the query." *(If cancelled orders shouldn't count, add `AND o.status <> 'Cancelled'` to the `ON` clause, not the `WHERE`, or the left join breaks.)*
- Gives the left-join version, or `NOT EXISTS`, and explains both.
- **[+Edge cases]** "I'd avoid `NOT IN` here. If `orders.customer_id` ever contains a NULL, `NOT IN` returns no rows at all, silently. `NOT EXISTS` and the left-join pattern don't have that problem."
- **[+Scale]** "Both versions are usually optimized into an anti-join. An index on `orders.customer_id` keeps it fast on large tables."
- **[+Validate]** "I'd sanity-check that customers with orders plus customers without orders equals the total customer count."
- **[+Business]** "These are sign-ups that never converted. I'd add `signup_date` and the sales rep, sorted by recency, so sales can follow up the newest ones first."

**Likely follow-ups:** Customers with no order in the last 90 days? Products never sold? What if `orders.customer_id` can be NULL? Rewrite it without a join.
**Red flags:** `WHERE o.customer_id = NULL` · putting a right-table filter in `WHERE` after a left join · not being able to explain why `NOT IN` can fail.
**Learn it in:** Chapter 12 (sections 12.6, 12.10, 12.12).

---

**Q73-007 · Explain a p-value to a non-technical manager.**

**Level:** Intermediate · **Roles:** DA, DS, AE · **Round:** Technical / communication
**What they're really testing:** whether you understand the concept correctly *and* can explain it without jargon or overselling.

**Answer that passes**

"The p-value tells us whether the result is significant. If it's below 0.05, the result is real."

It's common, and partly wrong: a p-value below 0.05 doesn't prove the result is real.

**Strong answer**

"Suppose we test a new website layout and see 4% more enquiries. The p-value answers: *if the new layout actually made no difference, how often would we see a gap at least this big just by chance?* A p-value of 0.03 means about 3 times in 100. That's rare enough that we usually conclude the difference probably isn't just luck."

**Extra-points answer**

- **[+Simple first]** Gives the one-sentence version above, with the example.
- **[+Limits]** "What it *doesn't* tell us: it's not the probability that the new layout works, and it says nothing about whether 4% is big enough to matter."
- **[+Business]** "So alongside it I'd show the likely range of the effect, say between 1% and 7% more enquiries, and what that range is worth in revenue. That's what the decision should rest on."
- **[+Edge cases]** "Two things make p-values misleading: checking results every day and stopping when they look good, and testing twenty different metrics until one crosses the line. We agree the metric, sample size, and threshold *before* the test starts."
- **[+Close the loop]** "In one line: a small p-value means 'probably not luck'; the confidence interval tells us 'how big'; the business case tells us 'is it worth it'."

**Likely follow-ups:** What's a Type I error? Why 0.05? What would you do with p = 0.06? What's statistical power?
**Red flags:** "the probability the null hypothesis is true" · "p < 0.05 proves it works" · no mention of effect size.
**Learn it in:** Chapters 22 and 30.

---

**Q75-003 · Riverstone's revenue dropped 20% last month. How would you investigate?**

**Level:** Intermediate · **Roles:** DA, BA, DS, product and business roles · **Round:** Case
**What they're really testing:** structured thinking, business sense, and whether you check the data before you trust it.

**Answer that passes**

"I'd look at sales by region and product to find where it dropped, then talk to the sales team about why."

It's reasonable, but unstructured, and it skips the first question.

**Strong answer**

"First I'd confirm the drop is real, then break revenue down to find where it came from, then look for causes.
Revenue = number of orders × average order value, so I'd see which moved. Then I'd cut by customer segment, region, product category, and sales rep to locate it. Once I know where, I'd look at causes: pricing changes, a lost big customer, stock shortages, competitor activity, or seasonality."

**Extra-points answer**

- **[+Clarify]** "Is the 20% against the previous month, the same month last year, or the target? And is it invoiced, booked, or collected revenue?"
- **[+Validate first]** "Before analyzing the business, I'd rule out data problems: a failed pipeline load, a changed definition, orders stuck in Pending, a changed status mapping. Then calendar effects: fewer working days, a festival period, the timing of month-end invoicing. A surprising share of 'drops' end here."
- **[+Structure]** Draws the metric tree:

```
Revenue
├── Number of orders
│   ├── Active customers        (new · returning · lost)
│   └── Orders per customer
└── Average order value
    ├── Units per order
    ├── Price realized          (list price − discount)
    └── Product mix
```

- **[+Depth]** "Then I'd segment each branch: customer segment, region, category, channel, rep. I look for concentration. Is 80% of the drop from a few customers or one region? A drop spread evenly suggests something broad, like pricing or seasonality. A concentrated drop suggests a specific cause, like a lost account or a plant stock-out."
- **[+Business]** "I'd size each finding in rupees, rank them, and bring back two or three causes that explain most of the gap, with a recommended action and an owner for each."
- **[+Scale]** "Finally, I'd suggest an alert on the leading indicators, such as new orders and pipeline, so next time we see it within a week, not after month-end."

**Likely follow-ups:** You find one wholesale customer caused 60% of the drop; what next? How would you tell a data issue from a real drop? What would you put on a dashboard to catch this earlier?
**Red flags:** Jumping to a cause immediately · never checking data quality · no quantification · analyzing without a structure.
**Learn it in:** Chapters 5, 23, and 24.

---

### 8.5 Question counts

| Bank | Questions | Extras |
|---|---|---|
| 70 Excel, Google Sheets, VBA & BI | ~75 | 2 dashboard critiques · 2 broken-macro fixes |
| 71 SQL | ~100 | 5 live-coding walk-throughs |
| 72 Python & pandas | ~70 | 5 coding walk-throughs |
| 73 Statistics & Experimentation | ~70 | 3 A/B test debugging cases |
| 74 Machine Learning | ~90 | 4 model-debugging cases |
| 75 Product Sense & Cases | ~40 cases | 20 guesstimates |
| 76 Business Analyst | ~50 | 3 stakeholder role-plays |
| 77 Data Engineering & System Design | ~50 | 8 design walk-throughs |
| 78 Automation & Integration | ~45 | 4 design cases |
| 79 GenAI, LLM & MLOps | ~50 | 4 design cases |
| 80 Architecture & Leadership | ~35 | 5 architecture cases |
| 81 Behavioral & HR | ~40 | STAR story-bank template |
| 82 Take-homes & Mocks | — | 6 take-homes · 8 mock interviews |
| **Total** | **~715 questions + ~20 guesstimates** | **~81 worked cases, fixes, take-homes, and mocks** |

---

## 9. Fixes from the manuscript review

Every error found in the first-edition draft is resolved by the new structure:

| Draft issue | Resolved in |
|---|---|
| Ch 1 heading says "three questions" but lists four | Ch 7 |
| Ch 2 tier order (Engineering before Science) contradicts part order | Ch 8: tiers reordered to match the book, with the branches explicitly shown as peers |
| Ch 10 says CTEs were met in Part II, but they weren't | CTEs now genuinely taught in Ch 13; Ch 28 references it correctly |
| Ch 21 links Parquet to a storage idea in Chapter 2 that doesn't exist | Ch 2 now introduces file formats including Parquet; Ch 49 references it correctly |
| Ch 23 says FinOps returns in Part VII, but it didn't | New Ch 65 FinOps |
| Ch 23 typo "much of Parts V so far" | Ch 52 |
| Ch 27 cites quantization "from Chapter 24", which never covered it | Quantization now taught in Ch 53 |
| TOC and Project Bank lists collapsed into run-on paragraphs in Word/PDF | New build process (section 11) generates real lists and a page-numbered TOC |
| Claims to be "built on worked examples" with almost none | New chapter standard (section 3) |

---

## 10. Style sheet

- **Voice:** keep the draft's voice: warm, direct, second person ("you"), honest about difficulty, never hype.
- **Reading level:** explain as if to a smart friend with no technical background. Short sentences for new ideas; longer ones are fine once the idea has landed.
- **Jargon:** define on first use, in plain words, then use the term consistently.
- **Spelling:** American English, matching the draft (*analyze, modeling, color*). *(Open decision 2.)*
- **Currency and places:** ₹ and Indian cities in Riverstone examples, with universally understood business situations. *(Open decision 1.)*
- **Names:** every company and person in examples is fictional, with a mix of names reflecting a diverse workforce. No real companies in invented scenarios.
- **Code:** PostgreSQL as the primary SQL database, with MySQL shown alongside (installation in Ch 12, a dedicated "same SQL in MySQL" section in each core SQL chapter, and a tested MySQL companion file for every query), Python 3 with pandas/scikit-learn/PyTorch, Power BI for BI, Excel (Microsoft 365) and Google Sheets side by side, VBA and Google Apps Script for spreadsheet automation. Keywords in capitals, `snake_case` names, every sample runs.
- **Callouts:** *Watch out*, *Try it*, *Dialect note* / *Tool note*, *Spreadsheet link* / *SQL link* / *Python link*.
- **Numbers:** Indian digit grouping in prose is avoided for global readability (₹1,05,885 becomes ₹105,885); state units always.
- **Fast-changing facts:** product names, versions, prices, and laws are verified against official sources at time of writing, dated where needed, and kept out of core explanations so the book ages slowly.
- **Figures:** drafted as text diagrams or Mermaid in the manuscript; redrawn consistently for print.

---

## 11. Production workflow

### For every chapter

1. **Outline** from this blueprint; confirm prerequisites and cross-references.
2. **Data and code first:** extend the Riverstone dataset if needed, then write and run every example (PostgreSQL and MySQL / Python) before drafting prose.
3. **Draft** to the chapter standard (section 3).
4. **Verify** fast-changing facts against official documentation; keep a source list per chapter.
5. **Self-review checklist:** every template section present · every term defined · every output real · every cross-reference points to the right chapter · exercises and answers complete · spelling style consistent.
6. **Save** to the project as `manuscript/chNN-short-title.md`, with code in the companion repository, and update the progress tracker.

### For every volume

7. Build Word and PDF from the markdown (with a proper style template, real lists, and an automatic page-numbered TOC), redraw figures, compile the glossary and index, and do a full read-through for consistency.

### File organization in the project

```
planning/blueprint.md                     ← this document
planning/progress-tracker.md              ← status of every chapter
planning/style-sheet.md                   ← section 10, expanded as decisions are made
manuscript/ch01-what-is-data.md … ch83-the-long-game.md
manuscript/appendix-a-glossary.md …
manuscript/ch71-sql-question-bank.md …    ← Part VIII chapters, same folder
companion/                                ← dataset generator, setup SQL, notebooks
analyst-to-architect-book.md, .docx, .pdf ← original first-edition draft (kept for reference)
```

---

## 12. Writing roadmap

Ordered so something sellable exists as early as possible.

| Phase | What gets written | Why this order |
|---|---|---|
| **1. Foundations** | Riverstone dataset generator (mini + full) · style sheet · glossary seed · progress tracker | Every chapter depends on the data and conventions |
| **2. Volume 1** | Part 0 (Ch 1–6) → Part I (7–9) → Part II (10–27), including the automation sandbox in the companion files | The core promise: zero to job-ready analyst |
| **3. Analyst interview pack** | Ch 68, 69, 70, 71, 75, 76, 78, 81 | Lets Volume 1 launch with interview prep for analyst and BA roles |
| **4. Volume 2** | Part III (28–34) → Part IV (35–44) → Ch 72, 73, 74 | Science branch plus its interview banks |
| **5. Volume 3** | Part V (45–52) → Part VI (53–59) → Part VII (60–67) → Ch 83 → Ch 77, 79, 80 | Engineering, AI, and architecture plus banks |
| **6. Volume 4 completion** | Ch 82 (take-homes and mocks) · Appendix H · revision lists | Needs all other content to exist first |
| **7. Production** | Appendices, figures, index, Word/PDF builds, proofreading | Per volume, as each completes |

**Effort estimate:** roughly 2–3 chapters per focused working session once the dataset exists, so on the order of 40–50 sessions for the full manuscript, plus review time on your side.

---

## 13. Open decisions for you

Each has a default the writing will follow unless you choose otherwise.

| # | Decision | Default |
|---|---|---|
| 1 | **Market:** India-first (₹, Indian cities, Indian hiring context) or global (USD, neutral locations)? | India-first examples, globally understandable explanations |
| 2 | **Spelling:** American (as in the draft) or British/Indian English? | American |
| 3 | **Format:** one master book, 4 volumes, or both? | Master manuscript, published as 4 volumes |
| 4 | **Title and author details** for the front matter; keep "Analyst to Architect"? | Keep the title; new subtitle *"From Zero to Data Architect: The Complete Path, with the Interview Playbook"* |
| 5 | **Cloud provider** for engineering examples: AWS, Azure, or GCP? | Concepts provider-neutral; hands-on examples on one provider (suggest Azure if targeting Power BI/Microsoft-heavy employers, AWS otherwise) |
| 6 | **Publishing route** (self-publish ebook and print, platform, or a publisher)? Affects page size and formatting | Decide before Phase 7; writing is unaffected |
| 7 | **Companion repository:** public (free, drives sales) or buyers-only? | Public |
| 8 | **Automation tools** for hands-on examples | Python for code-based automation; Power Automate as the main low-code example (common in Microsoft-based companies) with n8n as the open-source alternative; concepts shown to transfer to Zapier and Make |
| 9 | **Spreadsheet versions** | Excel for Microsoft 365 on Windows as the main version (with Mac differences noted, since some VBA features differ), and Google Sheets side by side throughout |
| 10 | **SQL databases** | PostgreSQL as the primary teaching database; MySQL shown alongside (install guide, a MySQL section in each core SQL chapter, tested MySQL companion files). SQL Server, Snowflake and BigQuery differences covered in dialect notes and Ch 49 |
| 11 | **Chapter depth** | *Decided 16 Sep 2026:* depth varies. Core skill chapters (spreadsheets, SQL, Python, Power BI, automation) at the full depth of Ch 12–13; foundation, overview, and career chapters close to planned length, expanding only where beginners need worked examples |
