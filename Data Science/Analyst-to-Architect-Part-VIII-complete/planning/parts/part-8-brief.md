# Part Brief — Part VIII — The Interview Playbook

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-8-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 68–82**.

**Suggested split into two chats:** VIII-A = Chapters 68–71, 75, 76, 78, 81 (analyst and BA interview pack, matching roadmap phase 3); VIII-B = Chapters 72–74, 77, 79, 80, 82.

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P8-68 | 68 | How Data Hiring Works | E | 4,000 | Not started | `manuscript/ch68-how-data-hiring-works.md` |
| P8-69 | 69 | The Extra-Points Method | E | 5,000 | Not started | `manuscript/ch69-the-extra-points-method.md` |
| P8-70 | 70 | Excel, Google Sheets, VBA & BI Question Bank | E | 6,000 | Not started | `manuscript/ch70-excel-google-sheets-vba-and-bi-question-bank.md` |
| P8-71 | 71 | SQL Question Bank | E | 9,000 | Not started | `manuscript/ch71-sql-question-bank.md` |
| P8-72 | 72 | Python & pandas Question Bank | E | 6,000 | Not started | `manuscript/ch72-python-and-pandas-question-bank.md` |
| P8-73 | 73 | Statistics, Probability & Experimentation Bank | E | 6,000 | Not started | `manuscript/ch73-statistics-probability-and-experimentation-bank.md` |
| P8-74 | 74 | Machine Learning Question Bank | E | 8,000 | Not started | `manuscript/ch74-machine-learning-question-bank.md` |
| P8-75 | 75 | Product Sense, Metrics, Case Studies & Guesstimates | E | 7,000 | Not started | `manuscript/ch75-product-sense-metrics-case-studies-and-guesstimates.md` |
| P8-76 | 76 | Business Analyst Question Bank | E | 4,500 | Not started | `manuscript/ch76-business-analyst-question-bank.md` |
| P8-77 | 77 | Data Engineering & Data System Design Bank | E | 6,500 | Not started | `manuscript/ch77-data-engineering-and-data-system-design-bank.md` |
| P8-78 | 78 | Automation & Integration Question Bank | E | 4,500 | Not started | `manuscript/ch78-automation-and-integration-question-bank.md` |
| P8-79 | 79 | GenAI, LLM & MLOps Question Bank | E | 5,500 | Not started | `manuscript/ch79-genai-llm-and-mlops-question-bank.md` |
| P8-80 | 80 | Architecture & Leadership Question Bank | E | 3,500 | Not started | `manuscript/ch80-architecture-and-leadership-question-bank.md` |
| P8-81 | 81 | Behavioral, HR & Offer Conversations | E | 4,000 | Not started | `manuscript/ch81-behavioral-hr-and-offer-conversations.md` |
| P8-82 | 82 | Take-Home Assignments & Mock Interviews | E | 6,000 | Not started | `manuscript/ch82-take-home-assignments-and-mock-interviews.md` |

## Reference chapters for this part

Blueprint section 8 (the method, rubric, entry format, and three sample entries). For voice, Chapter 12.

## Guidance specific to this part

- **Format exactly as blueprint section 8** and instructions section 11. Chapter 69 teaches the Extra-Points Method itself; write it first so the banks can refer to its moves.
- **Every question entry points to where the topic is taught** ("Learn it in: Chapter 12, sections 12.6, 12.10"), checked against `planning/chapter-map.md` and the actual section numbers of written chapters. Where a chapter isn't written yet, use the blueprint plan and flag the entry for a re-check.
- **All code in answers runs on Riverstone data** and is verified with `tools/verify_sql.py` / `tools/verify_python.py`. SQL answers note MySQL differences where they change the answer.
- **Chapter 68 (How Data Hiring Works)** and **Chapter 81 (Behavioral, HR & Offers):** hiring practices, screening software, and offer norms change; verify and date them, and keep advice general.
- **Chapter 71 (SQL bank)** must include the MySQL dialect questions promised in Chapter 12 (section 12.16's interview extra point) and the window-function classics promised in Chapter 13.
- **Chapter 73 (Statistics bank)** and **Chapter 76 (BA bank)** must cover data types, levels of measurement, and data quality (promised by Chapter 1).
- **Chapters 77 and 78** must cover file formats, APIs, and data security (promised by Chapter 2).
- **Question IDs** are `Q<chapter>-<three digits>` (for example `Q71-014`). If chapter numbers change at assembly, the coordinator renumbers IDs.

## Sequencing and dependencies

Chapter 69 can start now. Each bank starts when its source chapters are written (or from the blueprint, with a re-check pass after approval).

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

**Ch 68. How Data Hiring Works** · NEW · 4,000 words
Interview rounds for each role · what each round tests · CVs that pass screening software and humans · portfolio and LinkedIn · referrals · preparing in 30/60/90 days

**Ch 69. The Extra-Points Method** · NEW · 5,000 words
The answer framework, scoring rubric, and extra-point moves (section 8), practiced on 20 examples

**Ch 70. Excel, Google Sheets, VBA & BI Question Bank** · NEW · 6,000 words
~75 questions: formulas and lookups in Excel and Sheets, pivots, Power Query, `QUERY` and `ARRAYFORMULA`, macros, VBA and Apps Script (including reading and fixing a broken macro), DAX, data modeling, dashboard critique

**Ch 71. SQL Question Bank** · NEW · 9,000 words
~100 questions: concepts, NULL and join puzzles, window functions, classic problems (Nth highest, duplicates, streaks, retention), PostgreSQL vs MySQL dialect questions, query optimization, live-coding walk-throughs

**Ch 72. Python & pandas Question Bank** · NEW · 6,000 words
~70 questions: language basics, data structures, pandas tasks, debugging, coding problems at data-role difficulty

**Ch 73. Statistics, Probability & Experimentation Bank** · NEW · 6,000 words
~70 questions: probability puzzles, distributions, hypothesis tests, A/B test design and debugging, causal questions

**Ch 74. Machine Learning Question Bank** · NEW · 8,000 words
~90 questions: algorithms, bias–variance, metrics, leakage, feature engineering, model debugging, ML case studies

**Ch 75. Product Sense, Metrics, Case Studies & Guesstimates** · NEW · 7,000 words
~40 business cases ("revenue fell 20%…", "design a KPI dashboard for…") + 20 guesstimates, all solved with a structure

**Ch 76. Business Analyst Question Bank** · NEW · 4,500 words
~50 questions: requirements, process mapping, user stories, SDLC, UAT, stakeholder scenarios

**Ch 77. Data Engineering & Data System Design Bank** · NEW · 6,500 words
~50 questions + 8 full design walk-throughs (e.g. "design a daily sales pipeline", "design real-time sensor monitoring")

**Ch 78. Automation & Integration Question Bank** · NEW · 4,500 words
~45 questions: choosing between macros, scripts, Python and low-code tools, report automation, email and alert delivery, scheduling, APIs and webhooks, reverse ETL, low-code vs code vs RPA, failure handling and monitoring · 4 design cases (e.g. "automate a daily MIS email for 200 managers", "sync lead scores into the CRM without duplicates", "an automation silently stopped last week: how do you find out and prevent it?")

**Ch 79. GenAI, LLM & MLOps Question Bank** · NEW · 5,500 words
~50 questions + 4 design cases (RAG assistant, model-serving platform)

**Ch 80. Architecture & Leadership Question Bank** · NEW · 3,500 words
~35 questions + 5 architecture cases for senior and architect roles

**Ch 81. Behavioral, HR & Offer Conversations** · NEW · 4,000 words
~40 behavioral questions with STAR examples, building your story bank, questions to ask interviewers, handling offers

**Ch 82. Take-Home Assignments & Mock Interviews** · NEW · 6,000 words
6 complete take-home assignments with model submissions · 8 full mock interview scripts (analyst, BA, DS, DE, ML, architect) with interviewer notes and scoring

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 69

- *(from Ch 12)* Chapter 69 explains this move, and Chapter 71 has more dialect questions.

#### Chapter 71

- *(from Ch 12)* This distinction comes up in interviews constantly (Chapter 71).
- *(from Ch 12)* Chapter 69 explains this move, and Chapter 71 has more dialect questions.
- *(from Ch 12)* Interview preparation: the SQL Question Bank (Chapter 71) tests everything in this chapter, from "explain the difference between WHERE and HAVING" to live join and NULL puzzles, with graded model answers.
- *(from Ch 13)* Interview preparation: the SQL Question Bank (Chapter 71) includes the classic window-function rounds: second-highest salary, top N per group, running totals, consecutive days, and deduplication, with graded model answers.

#### Chapter 73

- *(from Ch 1)* Interview preparation: questions on data types, levels of measurement, and data quality appear in the Statistics bank (Chapter 73) and the Business Analyst bank (Chapter 76), with model answers.

#### Chapter 76

- *(from Ch 1)* Interview preparation: questions on data types, levels of measurement, and data quality appear in the Statistics bank (Chapter 73) and the Business Analyst bank (Chapter 76), with model answers.

#### Chapter 77

- *(from Ch 2)* Interview preparation: file formats, APIs, and data security questions appear in the Data Engineering bank (Chapter 77) and the Automation & Integration bank (Chapter 78).

#### Chapter 78

- *(from Ch 2)* Interview preparation: file formats, APIs, and data security questions appear in the Data Engineering bank (Chapter 77) and the Automation & Integration bank (Chapter 78).

## Kickoff prompt

```
You are writing Part VIII — The Interview Playbook of the book "Analyst to Architect" (Chapters 68–82).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-8-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-8-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```

## Coordinator notes (added 17 Sep 2026, after Part I)

- **Role names:** use the ten role names and track names from Chapter 7 §7.2 (instructions §2) in every bank, especially Chapter 68.
- **Pay and offers:** Chapter 8 §8.6 already teaches salary sources (PayScale, Indeed), percentiles, thin data for new titles, and CTC vs in-hand pay. Chapters 68 and 81 should point back to §8.6 rather than repeat it.
- **Portfolios and plateaus:** Chapter 9 §9.5 (portfolio pieces) and §9.7 (plateaus) exist; Chapters 68, 81, and 82 can refer to them.
