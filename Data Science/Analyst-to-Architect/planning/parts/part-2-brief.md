# Part Brief — Part II — The Analyst

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-2-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 10–27; 12 and 13 are written**.

**Suggested split into two chats:** II-A = Chapters 10, 11, 14, 15, 16 (spreadsheets, cleaning, visualization, Power BI); II-B = Chapters 17–27 (Python, automation, statistics, business, BA track, toolkit, capstone). Chapters 12 and 13 are done (Chapter 12 v4 is awaiting the author's review of section 12.13; don't edit either).

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P2-10 | 10 | Spreadsheet Fundamentals: Excel & Google Sheets | A | 6,000 | Not started | `manuscript/ch10-spreadsheet-fundamentals-excel-and-google-sheets.md` |
| P2-11 | 11 | The Spreadsheet, Mastered: Excel & Google Sheets | A | 7,000 | Not started | `manuscript/ch11-the-spreadsheet-mastered-excel-and-google-sheets.md` |
| P2-12 | 12 | Databases & SQL Foundations | A | 30,000 | v3 approved; v4 (§12.13 added) awaiting review | `manuscript/ch12-databases-and-sql-foundations.md` |
| P2-13 | 13 | SQL for Real Analysis | A | 16,500 | Approved (v1.1) | `manuscript/ch13-sql-for-real-analysis.md` |
| P2-14 | 14 | Data Cleaning & Preparation | A | 6,000 | Not started | `manuscript/ch14-data-cleaning-and-preparation.md` |
| P2-15 | 15 | Data Visualization Principles | B | 4,000 | Not started | `manuscript/ch15-data-visualization-principles.md` |
| P2-16 | 16 | Business Intelligence with Power BI | A | 7,000 | Not started | `manuscript/ch16-business-intelligence-with-power-bi.md` |
| P2-17 | 17 | Python from Zero | A | 6,000 | Not started | `manuscript/ch17-python-from-zero.md` |
| P2-18 | 18 | Python for Analysts: pandas & Automation | A | 8,000 | Not started | `manuscript/ch18-python-for-analysts-pandas-and-automation.md` |
| P2-19 | 19 | Spreadsheet Automation: Macros, VBA, Office Scripts & Google Apps Script | A | 7,000 | Not started | `manuscript/ch19-spreadsheet-automation-macros-vba-office-scripts-and-google-apps-script.md` |
| P2-20 | 20 | Automating Reports & Delivering Insights | A | 6,000 | Not started | `manuscript/ch20-automating-reports-and-delivering-insights.md` |
| P2-21 | 21 | Descriptive Statistics & Probability | B | 6,000 | Not started | `manuscript/ch21-descriptive-statistics-and-probability.md` |
| P2-22 | 22 | Statistics Without Fooling Yourself | B | 5,000 | Not started | `manuscript/ch22-statistics-without-fooling-yourself.md` |
| P2-23 | 23 | Business Acumen, KPIs & Metrics | B | 6,000 | Not started | `manuscript/ch23-business-acumen-kpis-and-metrics.md` |
| P2-24 | 24 | Requirements, Storytelling & Stakeholders | C | 4,000 | Not started | `manuscript/ch24-requirements-storytelling-and-stakeholders.md` |
| P2-25 | 25 | The Business Analyst Track | C | 5,000 | Not started | `manuscript/ch25-the-business-analyst-track.md` |
| P2-26 | 26 | The Professional Toolkit: Git, Agile, Documentation & AI Assistants | C | 4,000 | Not started | `manuscript/ch26-the-professional-toolkit-git-agile-documentation-and-ai-assistants.md` |
| P2-27 | 27 | Capstone: Your Analyst Portfolio | D | 3,000 | Not started | `manuscript/ch27-capstone-your-analyst-portfolio.md` |

## Reference chapters for this part

Chapters 12 and 13 (class A) for every class A chapter; Chapter 13 for class B chapters; Chapters 1–2 for class C chapters (24, 25, 26).

## Guidance specific to this part

- **This part is the book's core promise: zero to job-ready analyst.** Most chapters are class A. Match Chapter 12's depth: Riverstone data throughout, real output for everything, "In the real world" sections at the level of Chapter 12's "Monday morning with the sales head", tool-difference sections, a lab, and 20–30 exercises.
- **Build the full Riverstone sales dataset first.** Chapters 12 and 13 already promise "the full-size version, with thousands of orders" for their projects, and Chapters 14, 16, 20, and 23 need realistic volume. Blueprint section 6 specifies it (about 5,000 customers, about 200,000 order lines, 3 years). Write a seeded generator in `companion/` that extends the existing one-year database's customers, products, people, and 2025 patterns (seasonality, targets, planted data problems), produce PostgreSQL, MySQL, CSV, and Parquet versions, and register the data spec (instructions, section 14.4). Report any unavoidable differences from the mini and one-year databases.
- **Chapters 10–11 (Excel and Google Sheets side by side).** Build the practice workbooks from the Riverstone databases with a script (`openpyxl`) into `companion/ch10/` and `companion/ch11/`. Teach every technique in both apps, with menu paths for each. Verify formulas as in instructions section 9.3 (LibreOffice recalculation; modern Excel-only functions such as `XLOOKUP` computed independently and listed as manual checks). Promised by Chapter 1: how to check what a cell really contains. Promised by Chapter 2: importing CSV without losing leading zeros or breaking dates.
- **Chapter 14 (Data Cleaning & Preparation)** needs a **messy dataset**. Build a seeded generator that produces a messy export of Riverstone customers and orders (spelling variants, trailing spaces, duplicates in different case, mixed date formats, impossible dates, missing values, codes that lost leading zeros), consistent with Chapter 1 section 1.10's examples. Clean it in spreadsheets, SQL, and a preview of pandas. Register the data spec (instructions, section 14.4).
- **Chapter 16 (Power BI)** can't be run in a sandbox. Build the model's tables from the Riverstone databases, compute every number the reader will see in a visual or DAX measure with SQL or pandas, and list every DAX formula and screen step under "Manual checks needed". Verify current Power BI feature names and menus against Microsoft's documentation.
- **Chapters 17–18 (Python):** verify with `tools/verify_python.py`; record versions; Chapter 18 must deliver the promises from Chapters 1–2 (flattening JSON, reading CSV/Excel/JSON/Parquet, calling APIs with `companion/ch02/api_demo.py`).
- **Chapter 19 (Macros, VBA, Office Scripts, Apps Script):** code can't run here. Keep scripts short and commented, based on current official documentation; show expected results computed independently; list every script under "Manual checks needed" so the author can test them in Excel and Google Sheets.
- **Chapter 20 (Automating Reports)** carries the most promises of any chapter (see below): the *Daily Sales Flash* email built from Chapter 12's monthly report query, numbers in the email body, alerts, failure warnings, the Friday file from Chapter 2 automated end to end, safe storage of API keys, the nightly upsert sync. Test email sending against a local SMTP test server in Python and show the real generated HTML; schedule with Task Scheduler/cron explained, and verify Power Automate and n8n steps against current documentation.
- **Chapters 21–22 (statistics):** every statistic computed with Python (`scipy`, `numpy`) on Riverstone data; tie averages to levels of measurement (Chapter 1). Chapter 13's cohort and small-sample warnings point here.
- **Chapter 23 (KPIs):** define Riverstone's KPIs consistently with Chapter 3's process and the metrics already used (net revenue, gross margin, receivables ageing, win rate).
- **Chapter 26 (Git and AI assistants):** Chapter 12 and 13 projects already tell readers to save queries in Git; show that workflow with the Riverstone SQL files.
- **SQL in this part** (Chapters 14, 16, 20, 23 and others): PostgreSQL and MySQL both, verified with `tools/verify_sql.py`.

## Sequencing and dependencies

Can start immediately (Part 0 Chapter 3 is a soft dependency for Chapters 20 and 23; read it when available). Chapter 20 should come after 17–19.

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

**Ch 10. Spreadsheet Fundamentals: Excel & Google Sheets** · NEW · 6,000 words
Every technique shown in **both Excel and Google Sheets**, side by side, with differences flagged · workbooks, sheets, cells, ranges · entering and formatting data · formulas and cell references (relative, absolute, mixed) · essential functions: `SUM`, `AVERAGE`, `COUNT`, `IF`, `COUNTIFS`, `SUMIFS`, text and date functions · sorting, filtering, tables · charts · data validation and conditional formatting · keyboard shortcuts for both · Google Sheets strengths: real-time collaboration, sharing and permissions, version history, Google Forms feeding a sheet · file formats and moving between Excel and Sheets without breaking things.
*Project:* Build a clean monthly sales tracker for Riverstone from a raw export.

**Ch 11. The Spreadsheet, Mastered: Excel & Google Sheets** · EXPANDED from draft Ch 5 · 7,000 words
Lookups (`XLOOKUP`, `INDEX`/`MATCH`, in both tools) · pivot tables and pivot charts in depth · dynamic arrays (`FILTER`, `UNIQUE`, `SORT`) · Power Query step by step · Power Pivot and a first taste of DAX · what-if analysis, Goal Seek · Google Sheets power features: `QUERY` (SQL-like formulas), `ARRAYFORMULA`, `IMPORTRANGE` across files, Sheets pivot tables, connecting Sheets to a data warehouse · what Excel does that Sheets can't (Power Query, Power Pivot) and the Sheets alternatives · spreadsheet hygiene and auditing · when to leave the spreadsheet. (Automating spreadsheets with macros and scripts: Ch 19.)
*Project:* Rebuild a messy monthly workbook so next month is one refresh.

**Ch 12. Databases & SQL Foundations** · REWRITTEN from draft Ch 4 · 30,000 words · ✅ **Approved v3 (16 Sep 2026); v4 adds §12.13, awaiting review**
Tables, types, keys, relationships, ER diagrams (drawn figures), normalization intuition · real-life examples throughout (profit and margin, overdue invoices, receivables ageing) · `SELECT`, `WHERE`, NULL logic, `ORDER BY`, `CASE`, dates, text · aggregates, `GROUP BY`, `HAVING` · every join type, anti-joins, self-joins, fan-out · execution order · subqueries, set operations · **§12.13 building and changing a database in PostgreSQL and MySQL side by side**: `CREATE DATABASE`/`TABLE`, types, constraints (`NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, foreign keys), `INSERT` (errors, ID gaps, `RETURNING`/`LAST_INSERT_ID`), CSV loading, `UPDATE` (with joins), `DELETE` and `ON DELETE` options, soft delete, upsert, transactions and MySQL's implicit commit, `ALTER TABLE` (add/rename/drop/modify columns, the MySQL `MODIFY` trap, constraints), renaming, schemas, `TRUNCATE`/`DROP`, safe production changes, cheat sheet · SQL style · a worked "Monday morning" section answering four business questions with a six-step method · **installing both PostgreSQL and MySQL** (current LTS; Windows MSI + MySQL Configurator, macOS DMG, Linux APT; DBeaver or MySQL Workbench; first-connection troubleshooting) · §12.16 *The same SQL in MySQL*: differences table, the three silent traps (date subtraction, case-insensitive collation, `||`), NULL ordering, `FULL OUTER JOIN` workaround, portable-SQL habits, MySQL exercise track.
*Project:* Rebuild a real report in SQL and reconcile it.

**Ch 13. SQL for Real Analysis** · NEW (absorbs part of draft Ch 10) · 16,500 words · ✅ **Approved (draft v1.1, 16 Sep 2026)**
CTEs · window functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`/`LEAD`, running totals, moving averages, `SUM() OVER ()`) · the analyst's pattern library: top-N per group, month-over-month and year-over-year, cumulative totals, deduplication, first/last event, funnels, basic cohort retention, gaps and islands (intro) · data-quality checks in SQL · building a SQL snippet library · §13.8 *Running this chapter in MySQL*: recursive-CTE date spine, `cte_max_recursion_depth`, `SUM(CASE)` pivots, reserved words.
*Project:* A reusable SQL pack for Riverstone's weekly sales review.

**Ch 14. Data Cleaning & Preparation** · NEW · 6,000 words
Why most analysis time is cleaning · profiling a new dataset · missing values (types and treatments) · duplicates and fuzzy duplicates · inconsistent categories and typos · outliers: error or reality? · dates, time zones, and units · joining messy sources · validation rules · documenting every cleaning decision. Shown side by side in Excel/Power Query, SQL, and (preview) pandas.
*Project:* Clean Riverstone's operations export and write a data-quality report.

**Ch 15. Data Visualization Principles** · NEW · 4,000 words
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

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 10

- *(from Ch 1)* Chapter 10 shows how to check what a cell really contains.
- *(from Ch 1)* | Structured | spreadsheets, database tables, CSV files | Chapters 10–13 and most of Part II |
- *(from Ch 1)* Chapter 10 teaches both from the beginning.
- *(from Ch 1)* Chapters 10 and 12 put this chapter's ideas into tools: data types and tables in spreadsheets, then in databases.
- *(from Ch 2)* Chapters 10 and 11 teach spreadsheets properly, including importing CSV files without damage.
- *(from Ch 12)* Before you start: Chapter 1 (what data is), Chapter 3 (how a business runs on data), and Chapters 10–11 (spreadsheets).
- *(from Ch 12)* In Chapters 10 and 11 you worked with spreadsheets, where the data sits right in front of you and you can see every cell.
- *(from Ch 12)* `CASE` works like the spreadsheet `IF` function from Chapter 10, but it can check many conditions in order.
- *(from Ch 12)* Spreadsheet link. In Chapter 10 you used `XLOOKUP` to fetch a customer's name from another sheet, one cell at a time.

#### Chapter 11

- *(from Ch 2)* Chapters 10 and 11 teach spreadsheets properly, including importing CSV files without damage.
- *(from Ch 12)* Before you start: Chapter 1 (what data is), Chapter 3 (how a business runs on data), and Chapters 10–11 (spreadsheets).
- *(from Ch 12)* In Chapters 10 and 11 you worked with spreadsheets, where the data sits right in front of you and you can see every cell.
- *(from Ch 12)* If you built pivot tables in Chapter 11, this is the same idea: `GROUP BY` is the pivot table's "Rows" area, and the aggregate is its "Values" area.
- *(from Ch 12)* Five `CASE` columns turn one list of invoices into a five-column report, the same result you'd build with a pivot table in Chapter 11.

#### Chapter 12

- *(from Ch 1)* Chapter 12 shows how getting the grain wrong makes totals double-count.
- *(from Ch 1)* Databases use a special marker, NULL, for "unknown", and Chapter 12 shows how it trips up calculations.
- *(from Ch 1)* Chapters 10 and 12 put this chapter's ideas into tools: data types and tables in spreadsheets, then in databases.
- *(from Ch 2)* The tiny error is invisible in most charts, but it's why `0.1 + 0.2 = 0.3` can come out as *false* in a program, and why financial systems store money in exact decimal types instead (you'll meet `NUMERIC` in Chapter 12).
- *(from Ch 2)* A dataset with millions of rows belongs in a database (Chapter 12) or a format such as Parquet (section 2.5).
- *(from Ch 2)* Chapter 12 teaches databases and SQL properly, from creating your first table onward.
- *(from Ch 2)* That's why, as Chapter 12 mentions, many companies give analysts read-only accounts.
- *(from Ch 2)* Chapter 12, Databases & SQL Foundations, turns the one-page preview in section 2.6 into a full, hands-on skill.
- *(from Ch 13)* Before you start: Chapter 12.
- *(from Ch 13)* Tools: PostgreSQL and DBeaver, as in Chapter 12.
- *(from Ch 13)* Chapter 12 taught you to ask a database questions.
- *(from Ch 13)* The mini database (`riverstone`) is the one from Chapter 12: eight customers and twelve orders in the first quarter of 2026, plus invoices and payments.
- *(from Ch 13)* Here is the answer to exercise 13 from Chapter 12, *which customers' revenue is above the average customer's revenue?*, written with nested subqueries.
- *(from Ch 13)* The result is identical to Chapter 12's, but the query now reads like the method you'd explain to a colleague:
- *(from Ch 13)* Calculating `days_past_due` once in step 2 also made the `CASE` conditions in step 4 much simpler than in Chapter 12.
- *(from Ch 13)* In Chapter 12 you typed the net revenue formula, `quantity * unit_price * (1 - discount_pct / 100)`, more than a dozen times, along with the rule "exclude cancelled orders".
- *(from Ch 13)* A very common request: *"Show each customer's most recent order."* Chapter 12 solved a version of this with a correlated subquery. `ROW_NUMBER()` is cleaner and handles ties safely:
- *(from Ch 13)* Like the Chapter 12 script, it creates its own database (`riverstone_2025`), so there's no separate `CREATE DATABASE` step.
- *(from Ch 13)* PostgreSQL and DBeaver, as in Chapter 12.

#### Chapter 13

- *(from Ch 1)* | Structured | spreadsheets, database tables, CSV files | Chapters 10–13 and most of Part II |
- *(from Ch 12)* "Top 3 with ties" is a real business requirement and a favorite interview follow-up; Chapter 13 solves it properly with `RANK()`.
- *(from Ch 12)* (Chapter 13 shows a neater tool for that last case.)
- *(from Ch 12)* Chapter 13 shows a tidier way to write these steps, using CTEs.
- *(from Ch 12)* "Latest record per group" is such a common need that Chapter 13 gives it a cleaner tool, `ROW_NUMBER()`.
- *(from Ch 12)* Once subqueries nest more than one level deep they become hard to read, and Chapter 13 introduces common table expressions (CTEs), which do the same job with named, top-to-bottom steps.
- *(from Ch 12)* Ranking reps, showing each one's share of team revenue, and comparing this quarter with last all need window functions, the headline tool of Chapter 13.
- *(from Ch 12)* Chapter 13, SQL for Real Analysis, builds on this chapter with common table expressions, window functions (rankings, running totals, month-over-month growth), and the report patterns analysts use every week.
- *(from Ch 12)* In Chapter 13, a window function does this far more neatly: `SUM(...) OVER ()`.
- *(from Ch 12)* That repetition is exactly the problem CTEs solve in Chapter 13, where this becomes a short, readable query.

#### Chapter 14

- *(from Ch 1)* This is why analysts check data before they trust it. Chapter 14 teaches how to find and fix these problems at scale, and Chapter 47 shows how data teams catch them automatically before a report goes out.
- *(from Ch 1)* Chapter 14, Data Cleaning & Preparation, fixes the quality problems from section 1.10 at scale.
- *(from Ch 12)* Where it doesn't, the data needs fixing, and Chapter 14 covers how.
- *(from Ch 12)* You'll use these heavily in Chapter 14, where real-world text is full of extra spaces, inconsistent capitals, and typos.
- *(from Ch 12)* Chapter 14, Data Cleaning & Preparation, tackles the messy data that real databases are full of.
- *(from Ch 13)* Ask the CRM owner before deleting anything, and never delete from the source system as part of an analysis; clean in your query or in a separate cleaned table (Chapter 14).
- *(from Ch 13)* Chapter 14, Data Cleaning & Preparation, goes deeper into duplicates, missing values, and messy text, the problems Patterns 3 and 10 only flag.

#### Chapter 15

- *(from Ch 1)* It decides which chart fits (a bar chart for categories, a histogram for continuous amounts, Chapter 15) and which summary makes sense (a count of each payment method, but an average of prices).

#### Chapter 16

- *(from Ch 13)* Later: Power BI's DAX language (Chapter 16) has its own versions of running totals, ranking, and time comparisons.
- *(from Ch 13)* Chapter 16, Business Intelligence with Power BI, shows the same ideas (running totals, rankings, time comparisons) in DAX, and how to turn these queries into interactive dashboards.

#### Chapter 18

- *(from Ch 1)* Chapter 2 introduces these formats, and Chapter 18 shows how to flatten them in Python.
- *(from Ch 1)* | Semi-structured | JSON, XML, app and website logs | Chapters 2, 18, and Part V |
- *(from Ch 2)* You'll call real APIs from Python in Chapter 18, automate reports with them in Chapter 20, and design how whole systems exchange data in Chapter 51.
- *(from Ch 2)* The companion files (Appendix E): `orders_feb_2026` in `.csv`, `.xlsx`, `.json`, `.xml`, and `.parquet`; and `api_demo.py`, the demonstration API used in section 2.8, which you'll run yourself in Chapter 18.
- *(from Ch 2)* Chapter 18 reads CSV, Excel, JSON, and Parquet files in Python, and calls real APIs.
- *(from Ch 12)* Chapter 18 shows the same idea again in Python as `pandas.merge`.

#### Chapter 20

- *(from Ch 2)* You'll call real APIs from Python in Chapter 18, automate reports with them in Chapter 20, and design how whole systems exchange data in Chapter 51.
- *(from Ch 2)* Chapter 20 shows how to store them safely.
- *(from Ch 2)* Chapter 20 takes this exact report and automates it end to end.
- *(from Ch 2)* Chapter 20 automates the Friday report from this chapter, including storing API keys safely.
- *(from Ch 12)* You'll build this kind of job in Chapter 20.
- *(from Ch 12)* Chapter 20 takes this exact query and turns it into a *Daily Sales Flash*: an email that lands in every manager's inbox at 8 a.m., with the numbers in the body of the email, an alert when stock runs low, and a warning to you if the job ever fails.
- *(from Ch 12)* After Chapter 20, schedule the query and deliver its result automatically by email.
- *(from Ch 12)* Chapter 20, Automating Reports & Delivering Insights, puts your queries on a schedule and delivers the results to people's inboxes, chats, and dashboards.
- *(from Ch 13)* Run it before any important report, and make it the first step of any automated one (Chapter 20).
- *(from Ch 13)* Turn the headline query into a single CTE query that outputs all the headline numbers in one row, ready to paste into an email (Chapter 20 automates exactly this).
- *(from Ch 13)* Chapter 20, Automating Reports & Delivering Insights, schedules your review pack and emails the headline numbers every month.
- *(from Ch 13)* This is a simple version of the anomaly alert you'll automate in Chapter 20.

#### Chapter 21

- *(from Ch 1)* Chapter 21 goes deeper into choosing averages.
- *(from Ch 1)* Chapter 21, Descriptive Statistics & Probability, explains which averages and charts suit each level of measurement.

#### Chapter 22

- *(from Ch 13)* With only 4 to 11 customers per cohort, though, a single customer moves a percentage by 9 to 25 points, so treat differences between cohorts as questions, not conclusions (Chapter 22).
- *(from Ch 13)* Chapter 22 explains why small samples mislead, and Chapter 30 shows how to run a proper test.

#### Chapter 23

- *(from Ch 12)* Chapter 23 covers how businesses define metrics like margin.

#### Chapter 24

- *(from Ch 1)* Chapter 24 shows how to write the "so what" that turns a number into a decision.
- *(from Ch 12)* Your first job on any report is to find out and write it down. Chapter 24 covers how to have that conversation.
- *(from Ch 13)* Write the story. A one-page memo: three findings, each with a number, what it means, and a suggested action (Chapter 24).

#### Chapter 26

- *(from Ch 2)* If you need versions, use the version history in Google Drive, OneDrive, or SharePoint, or, for queries and code, Git (Chapter 26).
- *(from Ch 2)* For SQL queries and code, Git does the same job more precisely (Chapter 26).
- *(from Ch 12)* Save the script in version control (Chapter 26).
- *(from Ch 12)* Save it in a Git repository (Chapter 26) with a short README: what the report is, the rules, and how to run it.
- *(from Ch 13)* A snippets file or repository. Keep your pattern library in a Git repository (Chapter 26), one file per pattern, with a comment at the top saying what question it answers.

## Kickoff prompt

```
You are writing Part II — The Analyst of the book "Analyst to Architect" (Chapters 10–27; 12 and 13 are written).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-2-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-2-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```

## Coordinator note (17 September 2026): new reading order for Part II

Part II is now taught in blocks, so that each tool is learned end to end before the next one, and the cross-tool chapters come last. The mapping table is in `planning/chapter-map.md`; the short version:

**A. Spreadsheets:** Ch 10 → Ch 11 → **old Ch 19 (spreadsheet automation) moves here**, becoming the third spreadsheet chapter.
**B. SQL:** old Ch 12 → old Ch 13.
**C. Python:** old Ch 17 → old Ch 18.
**D. All tools together:** old Ch 14 (cleaning) → old Ch 15 (visualization) → old Ch 16 (Power BI) → Ch 20 (report automation and delivery).
**E. Judgment:** Ch 21–27, unchanged.

What this means for writing:

- **Keep current file numbers.** The coordinator renumbers the whole book in one pass at assembly. Refer to chapters by their current numbers, as the approved chapters do.
- **Old Ch 19 now precedes Python**, so it must teach its own programming basics (variables, `If`, loops, debugging) rather than building on Ch 17. Update its plan accordingly.
- **Old Ch 14 and Ch 15 are read after Python** in the new order, so their pandas examples are fine. Add one line to each ("pandas is taught in Chapter 18 / the Python block") so readers of the current draft aren't lost.
- **Old Ch 16 (Power BI)** is read after cleaning and visualization; assume both when writing it.
- Pipeline orchestration stays in Part V (Ch 46). Part II goes as far as scheduled scripts and refreshable reports.
