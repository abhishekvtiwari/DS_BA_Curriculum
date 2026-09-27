# Chapter Map — Analyst to Architect

The single list of chapters, with stable IDs. **Numbers are provisional until final assembly; IDs never change.** Part chats update only the *Status* of their own rows by reporting to the coordinator (see `planning/chapter-writing-instructions.md`, section 14). New chapters get a new ID and a letter-suffixed provisional number (for example `19A`) until the coordinator renumbers the book.

Depth classes: **A** full-depth skill chapter · **B** technical teaching chapter · **C** foundation / overview / career chapter · **D** capstone project · **E** interview question bank (definitions in the instructions, section 3).

## Reading order decided 17 September 2026 (renumbering happens at assembly)

Parts II and III are reordered so that each tool is learned end to end (including cleaning and automation in that tool) before the next tool, and the cross-tool chapters come after all three. **Chapter files keep their current numbers while writing; the coordinator renumbers the whole book in one pass at assembly.** Use this table to know what comes before what.

| New no. | Old no. | Chapter | Block |
|---|---|---|---|
| 10 | 10 | Spreadsheet Fundamentals: Excel & Google Sheets | A. Spreadsheets |
| 11 | 11 | The Spreadsheet, Mastered | A |
| 12 | 19 | Spreadsheet Automation: Macros, VBA, Office Scripts & Apps Script | A |
| 13 | 12 | Databases & SQL Foundations | B. SQL |
| 14 | 13 | SQL for Real Analysis | B |
| 15 | 17 | Python from Zero | C. Python |
| 16 | 18 | Python for Analysts: pandas & Automation | C |
| 17 | 14 | Data Cleaning & Preparation | D. All tools together |
| 18 | 15 | Data Visualization Principles | D |
| 19 | 16 | Business Intelligence with Power BI | D |
| 20 | 20 | Automating Reports & Delivering Insights | D |
| 21–27 | 21–27 | Statistics, business, toolkit, capstone (unchanged) | E. Judgment |
| 28 | 28 | Advanced SQL, Performance & Data Modeling | Part III |
| 29 | 34 | The Command Line, Linux & Networking Basics | Part III |
| 30 | 29 | Python as Software, Not Scripts | Part III |
| 31 | 32 | Analytics Engineering with dbt | Part III |
| 32 | 33 | The Computer Science You Actually Need | Part III |
| 33 | 30 | Inference & Experiments | Part III |
| 34 | 31 | Causal Inference Without Experiments | Part III |

Consequences to honor while writing:

- **Old Ch 19 (spreadsheet automation) now comes before Python**, so it teaches its own programming basics (variables, `If`, loops) instead of building on Python.
- **Old Ch 14 (cleaning) and Ch 15 (visualization) now come after Python**, so pandas examples in them are legitimate. Until the renumbering pass, both should carry one line telling the reader where Python is taught.
- **Old Ch 16 (Power BI) comes after cleaning and visualization**, and after Power Query in Ch 11.
- Parts IV–VIII keep their numbers: Part II still ends at 27 and Part III at 34.

---

## Part 0 — First Principles: Data from Zero

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P0-01 | 1 | What Is Data? | C | 7,500 | Approved (v1) | `manuscript/ch01-what-is-data.md` |
| P0-02 | 2 | How Computers Store, Move and Protect Data | C | 8,000 | Approved (v1) | `manuscript/ch02-how-computers-store-move-protect-data.md` |
| P0-03 | 3 | How a Business Runs on Data | C | 4,500 | Approved (v1) | `manuscript/ch03-how-a-business-runs-on-data.md` |
| P0-04 | 4 | Numbers Without Fear | C | 4,500 | Approved (v1) | `manuscript/ch04-numbers-without-fear.md` |
| P0-05 | 5 | Thinking Like an Analyst | C | 3,500 | Approved (v1) | `manuscript/ch05-thinking-like-an-analyst.md` |
| P0-06 | 6 | Setting Up to Learn | C | 2,500 | Approved (v1) | `manuscript/ch06-setting-up-to-learn.md` |

## Part I — The Map

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P1-07 | 7 | The Data Landscape | C | 4,000 | Approved (v1) | `manuscript/ch07-the-data-landscape.md` |
| P1-08 | 8 | The Career Tree: How Skills Unlock Roles | C | 5,000 | Approved (v1) | `manuscript/ch08-the-career-tree-how-skills-unlock-roles.md` |
| P1-09 | 9 | How Expertise Actually Forms | C | 2,500 | Approved (v1) | `manuscript/ch09-how-expertise-actually-forms.md` |

## Part II — The Analyst

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P2-10 | 10 | Spreadsheet Fundamentals: Excel & Google Sheets | A | 6,000 | Approved (v2, 16 Sep 2026; Part II-A) — in the Part II bundle | `manuscript/ch10-spreadsheet-fundamentals-excel-and-google-sheets.md` |
| P2-11 | 11 | The Spreadsheet, Mastered: Excel & Google Sheets | A | 7,000 | Approved (v2, 17 Sep 2026; Part II-A) — in the Part II bundle | `manuscript/ch11-the-spreadsheet-mastered-excel-and-google-sheets.md` |
| P2-12 | 12 | Databases & SQL Foundations | A | 30,000 | v3 approved 16 Sep 2026; **v4 awaiting review** (adds §12.13) | `manuscript/ch12-databases-and-sql-foundations.md` |
| P2-13 | 13 | SQL for Real Analysis | A | 16,500 | Approved (v1.1, 16 Sep 2026) | `manuscript/ch13-sql-for-real-analysis.md` |
| P2-14 | 14 | Data Cleaning & Preparation | A | 6,000 | Approved (v1.2, 17 Sep 2026; Part II-A) | `manuscript/ch14-data-cleaning-and-preparation.md` |
| P2-15 | 15 | Data Visualization Principles | B | 4,000 | Approved (v1.1, 17 Sep 2026; Part II-A) | `manuscript/ch15-data-visualization-principles.md` |
| P2-16 | 16 | Business Intelligence with Power BI | A | 7,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch16-business-intelligence-with-power-bi.md` |
| P2-17 | 17 | Python from Zero | A | 6,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch17-python-from-zero.md` |
| P2-18 | 18 | Python for Analysts: pandas & Automation | A | 8,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch18-python-for-analysts-pandas-and-automation.md` |
| P2-19 | 19 | Spreadsheet Automation: Macros, VBA, Office Scripts & Google Apps Script | A | 7,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch19-spreadsheet-automation.md` |
| P2-20 | 20 | Automating Reports & Delivering Insights | A | 6,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch20-automating-reports-and-delivering-insights.md` |
| P2-21 | 21 | Descriptive Statistics & Probability | B | 6,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch21-descriptive-statistics-and-probability.md` |
| P2-22 | 22 | Statistics Without Fooling Yourself | B | 5,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch22-statistics-without-fooling-yourself.md` |
| P2-23 | 23 | Business Acumen, KPIs & Metrics | B | 6,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch23-business-acumen-kpis-and-metrics.md` |
| P2-24 | 24 | Requirements, Storytelling & Stakeholders | C | 4,000 | Approved (v1, 18 Sep 2026; Part II-A) | `manuscript/ch24-requirements-storytelling-and-stakeholders.md` |
| P2-25 | 25 | The Business Analyst Track | C | 5,000 | Not started | `manuscript/ch25-the-business-analyst-track.md` |
| P2-26 | 26 | The Professional Toolkit: Git, Agile, Documentation & AI Assistants | C | 4,000 | Not started | `manuscript/ch26-the-professional-toolkit-git-agile-documentation-and-ai-assistants.md` |
| P2-27 | 27 | Capstone: Your Analyst Portfolio | D | 3,000 | Not started | `manuscript/ch27-capstone-your-analyst-portfolio.md` |

## Part III — Advanced Analytics & Analytics Engineering

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P3-28 | 28 | Advanced SQL, Performance & Data Modeling | A | 7,000 | Approved (v1.1, 18 Sep 2026; Part III) | `manuscript/ch28-advanced-sql-performance-and-data-modeling.md` |
| P3-29 | 29 | Python as Software, Not Scripts | B | 5,000 | **Draft v1.1 awaiting review** (Part III) | `manuscript/ch29-python-as-software-not-scripts.md` |
| P3-30 | 30 | Inference & Experiments | B | 6,000 | Approved (v1, 18 Sep 2026; Part III) | `manuscript/ch30-inference-and-experiments.md` |
| P3-31 | 31 | Causal Inference Without Experiments | B | 3,500 | Approved (v1, 18 Sep 2026; Part III) | `manuscript/ch31-causal-inference-without-experiments.md` |
| P3-32 | 32 | Analytics Engineering with dbt | A | 5,000 | Approved (v1, 18 Sep 2026; Part III) | `manuscript/ch32-analytics-engineering-with-dbt.md` |
| P3-33 | 33 | The Computer Science You Actually Need | B | 4,500 | Approved (v1, 18 Sep 2026; Part III) | `manuscript/ch33-the-computer-science-you-actually-need.md` |
| P3-34 | 34 | The Command Line, Linux & Networking Basics | B | 3,000 | Approved (v1, 18 Sep 2026; Part III) | `manuscript/ch34-the-command-line-linux-and-networking-basics.md` |

## Part IV — Machine Learning & Data Science

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P4-35 | 35 | The Math Under the Models | B | 6,000 | Approved (v1, 17 Sep 2026; Part IV) | `manuscript/ch35-the-math-under-the-models.md` |
| P4-36 | 36 | The Machine Learning Workflow & Feature Engineering | B | 5,000 | Approved (v1, 17 Sep 2026; Part IV) | `manuscript/ch36-the-machine-learning-workflow-and-feature-engineering.md` |
| P4-37 | 37 | Supervised Learning Algorithms | B | 8,000 | Approved (v1, 18 Sep 2026; Part IV) | `manuscript/ch37-supervised-learning-algorithms.md` |
| P4-38 | 38 | Unsupervised Learning | B | 4,500 | Approved (v1, 18 Sep 2026; Part IV) | `manuscript/ch38-unsupervised-learning.md` |
| P4-39 | 39 | Evaluation, Tuning, Interpretation & Honesty | B | 5,500 | Approved (v1, 18 Sep 2026; Part IV) | `manuscript/ch39-evaluation-tuning-interpretation-and-honesty.md` |
| P4-40 | 40 | Time Series & Forecasting | B | 6,000 | Approved (v1, 18 Sep 2026; Part IV) | `manuscript/ch40-time-series-and-forecasting.md` |
| P4-41 | 41 | NLP Foundations | B | 4,000 | Approved (v1, 18 Sep 2026; Part IV) | `manuscript/ch41-nlp-foundations.md` |
| P4-42 | 42 | Recommender Systems & Ranking | B | 3,500 | Approved (v1, 18 Sep 2026; Part IV) | `manuscript/ch42-recommender-systems-and-ranking.md` |
| P4-43 | 43 | A First Look at Deep Learning | B | 4,500 | Approved (v1, 18 Sep 2026; Part IV) | `manuscript/ch43-a-first-look-at-deep-learning.md` |
| P4-44 | 44 | Capstone: An End-to-End Data Science Project | D | 2,500 | **Draft v1 awaiting review** (18 Sep 2026; Part IV) | `manuscript/ch44-capstone-an-end-to-end-data-science-project.md` |

## Part V — Data Engineering, Integration & Scale

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P5-45 | 45 | Data Ingestion & Integration | B | 4,000 | Approved (v1, 16 Sep 2026; Part V) | `manuscript/ch45-data-ingestion-and-integration.md` |
| P5-46 | 46 | Pipelines & Orchestration | B | 4,500 | Approved (v1, 17 Sep 2026; Part V) | `manuscript/ch46-pipelines-and-orchestration.md` |
| P5-47 | 47 | Data Quality, Observability & Contracts | B | 3,500 | Approved (v1, 17 Sep 2026; Part V) | `manuscript/ch47-data-quality-observability-and-contracts.md` |
| P5-48 | 48 | Big Data & Distributed Compute | B | 4,500 | Approved (v1, 18 Sep 2026; Part V) | `manuscript/ch48-big-data-and-distributed-compute.md` |
| P5-49 | 49 | Storage, Warehouses & Lakehouses | B | 5,000 | Approved (v1, 18 Sep 2026; Part V) | `manuscript/ch49-storage-warehouses-and-lakehouses.md` |
| P5-50 | 50 | Streaming & Real-Time | B | 4,500 | Approved (v1, 18 Sep 2026; Part V) | `manuscript/ch50-streaming-and-real-time.md` |
| P5-51 | 51 | Data Activation: Reverse ETL, APIs & System Integration | B | 5,500 | Approved (v1, 19 Sep 2026; Part V) | `manuscript/ch51-data-activation-reverse-etl-apis-and-system-integration.md` |
| P5-52 | 52 | The Cloud, Containers & Infrastructure as Code | B | 5,500 | Approved (v1, 19 Sep 2026; Part V) | `manuscript/ch52-the-cloud-containers-and-infrastructure-as-code.md` |

## Part VI — Production ML, Generative AI & MLOps

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P6-53 | 53 | Deep Learning in Depth | B | 5,500 | Not started | `manuscript/ch53-deep-learning-in-depth.md` |
| P6-54 | 54 | Generative AI & Large Language Models | B | 5,500 | Not started | `manuscript/ch54-generative-ai-and-large-language-models.md` |
| P6-55 | 55 | Building AI Applications: RAG, Agents & Evaluation | B | 5,500 | Not started | `manuscript/ch55-building-ai-applications-rag-agents-and-evaluation.md` |
| P6-56 | 56 | MLOps: Making Models Survive Production | B | 5,000 | Not started | `manuscript/ch56-mlops-making-models-survive-production.md` |
| P6-57 | 57 | LLMOps | B | 4,000 | Not started | `manuscript/ch57-llmops.md` |
| P6-58 | 58 | Intelligent Automation: AI Inside Business Workflows | B | 4,500 | Not started | `manuscript/ch58-intelligent-automation-ai-inside-business-workflows.md` |
| P6-59 | 59 | Industry Case Studies | C | 4,500 | Not started | `manuscript/ch59-industry-case-studies.md` |

## Part VII — Architecture, Governance & Leadership

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P7-60 | 60 | Designing Whole Systems | C | 4,500 | Not started | `manuscript/ch60-designing-whole-systems.md` |
| P7-61 | 61 | Distributed Systems & Trade-offs | C | 4,000 | Not started | `manuscript/ch61-distributed-systems-and-trade-offs.md` |
| P7-62 | 62 | Data Architecture Patterns | C | 4,000 | Not started | `manuscript/ch62-data-architecture-patterns.md` |
| P7-63 | 63 | Automation Architecture & Governance | C | 4,500 | Not started | `manuscript/ch63-automation-architecture-and-governance.md` |
| P7-64 | 64 | Security, Privacy, Governance & Responsible AI | C | 5,000 | Not started | `manuscript/ch64-security-privacy-governance-and-responsible-ai.md` |
| P7-65 | 65 | FinOps: The Economics of Data Platforms | C | 3,000 | Not started | `manuscript/ch65-finops-the-economics-of-data-platforms.md` |
| P7-66 | 66 | Data Strategy, Maturity & Building Data Teams | C | 3,500 | Not started | `manuscript/ch66-data-strategy-maturity-and-building-data-teams.md` |
| P7-67 | 67 | The Architect as Leader | C | 3,500 | Not started | `manuscript/ch67-the-architect-as-leader.md` |

## Part VIII — The Interview Playbook

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

## Closing

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| PC-83 | 83 | The Long Game | C | 2,500 | Not started | `manuscript/ch83-the-long-game.md` |

## Appendices

| ID | Appendix | Title | Status |
|---|---|---|---|
| APX-A | A | Glossary | Not started |
| APX-B | B | Tool Index & Installation Guide | Not started |
| APX-C | C | The Project Bank | Not started |
| APX-D | D | Choosing Good Resources | Not started |
| APX-E | E | Practice Datasets & Companion Repository | Not started |
| APX-F | F | Cheat Sheets | Not started |
| APX-G | G | Answers to Chapter Exercises | Not started |
| APX-H | H | Role Profiles | Not started |
