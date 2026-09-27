# Analyst to Architect — Whole-Book Sequence Map

Status: built 2026-09-25 after Abhishek approved Part 0/I findings and the just-in-time setup direction. **Three decisions pending (below).**
Live doc: https://claude.ai/code/artifact/43dd9cc0-558e-4053-8e34-413426640130 (tab "Sequence map").

Method: all 80 chapters (Parts 0, II–VIII) machine-scanned for 35 code/tool families, ~2,700 key terms, every declared prerequisite, every "Chapter N (topic)" cross-reference, and drafting leftovers; flagged items checked in context. Part I and Closing checked by hand from the full read. Within-chapter line order is left to each part's full review.

Rule applied (test 7, sequence): nothing appears before the chapter that teaches it; tools introduced once, in the order by hand → spreadsheet → SQL → BI → Python → terminal/Git → engineering → ML → production → architecture.

## Structural breaks (M.1–M.12)

| ID | Break | Evidence | Sev | Proposed move |
|---|---|---|---|---|
| M.1 | Reading order ≠ chapter numbers | Ch 16: "the Python block (Chapters 17 and 18) comes before this chapter in the reading order"; Ch 6 plan puts 14–16 before 17–18 | High | One order; chapter number = reading order |
| M.2 | Python/pandas in Ch 14 (§14.13) and Ch 15 (§15.14) before Ch 17; Ch 17 lists Ch 14 as prerequisite (circular) | `import pandas as pd`, `pd.read_csv`, `plt.subplots` | High | Move §14.13 → Ch 18 §18.10; Python half of §15.14 → Ch 18 §18.11 |
| M.3 | All tools installed in Ch 6 | Approved just-in-time (S.3) | High | Spreadsheet 10, DB 12, Power BI 16, Python+Jupyter 17, Git 26 |
| M.4 | Terminal used before taught (Ch 34) | Ch 6, 17, 26 (32 lines), 28, 29, 32; Ch 29 & 32 list Ch 34 as prerequisite | High | Terminal basics in Ch 17 setup; Ch 34 essentials before Ch 26 |
| M.5 | Regression used before taught | §30.11 "Chapter 19 used regression to predict" (Ch 19 = VBA); Ch 31 statsmodels OLS/DiD; prediction taught Ch 37 | High | Regression basics section in Part II stats; fix refs |
| M.6 | SQL PERCENTILE_CONT in Ch 15 | Not in Ch 12–13; key term Ch 28 | Medium | Teach in Ch 13, or spreadsheet box plot |
| M.7 | Recursive CTE in Ch 13 | 3-line note in MySQL dialect (Pattern 5); taught Ch 28 | Medium | Calendar table in Ch 13 |
| M.8 | pytest in Ch 26 CI | `python -m pytest -q`; tests taught Ch 29 | Medium | Ch 26 CI runs plain script check |
| M.9 | NumPy used from Ch 18 without intro | `import numpy as np`, `np.where`; heavy in 21, 22, 30, 31; arrays taught Ch 35 | Medium | One-page NumPy basics in Ch 18 |
| M.10 | SQL/DAX bridge boxes ahead of tools | Ch 10–11 SQL links (GROUP BY, WHERE, LEFT JOIN, windows); Ch 11 → Ch 12 "helps"; Ch 13 DAX preview | Medium | Move bridges to target tool's chapter, pointing back |
| M.11 | MAE (9), SHAP (6) in Ch 37; evaluation Ch 39 | — | Low | Confirm in Part IV review |
| M.12 | "MLOps" ~100 uses in Ch 53–55; taught Ch 56 | — | Low | Confirm in Part VI review |

## Code/tool families before they are taught (13 real breaks of 35 scanned)

| Family | Taught in | Earlier in (lines) | Verdict |
|---|---|---|---|
| SQL basics | 12 | 6 (11), 10 (1), 11 (2) | Break (S.1, M.10) |
| SQL GROUP BY, joins | 12 | 10 (2), 11 (9) | Break (M.10) |
| SQL windows | 13 | 11 (2), 12 (2) | Minor |
| Recursive CTE | 28 | 13 (6) | Break (M.7) |
| SQL percentiles | 28 | 15 (9) | Break (M.6) |
| Spreadsheet formulas | 10 | 4 (6), 6 (5) | Break (S.1) |
| Power Query | 11 | 2, 6, 10 | Mentions; fine |
| DAX | 11 §11.8, then 16 | 13 (3) | Minor |
| Python code | 17 | 2, 6, 14, 15 (19) | Break (S.1, M.2) |
| pandas | 18 | 14, 15, 17 (9) | Break (M.2) |
| matplotlib | 18 | 15 | Break (M.2) |
| venv/pip/Jupyter | 17 | 6 (28) | Break (S.3) |
| Terminal | 34 | 2, 26, 28, 29, 32 (71) | Break (M.4) |
| pytest | 29 | 26 (2) | Break (M.8) |
| NumPy | 35 | 18, 21, 22, 23, 30, 31 (101) | Break (M.9) |
| statsmodels regression | none before 30 | 30, 31 (21) | Break (M.5) |
| scikit-learn, Spark, PyTorch, LLM APIs | 36, 48, 43, 54 | mentions | Fine |
| cron/Task Scheduler | 20 | — | Fine |
| dbt | 32 | 6, 13, 14, 16, 25, 26, 28, 29 (17) | Forward refs; trim |
| VBA, Git, Kafka, Docker | 19, 26, 50, 52 | — | Clean |

## Broken cross-references and numbering

| Where | Says | Should be |
|---|---|---|
| Ch 30 §30.11 | "Chapter 19 used regression to predict" | none earlier; Ch 37 (M.5) |
| Ch 31 prereqs | "Chapter 19's regression mechanics"; "Chapter 17's pandas" | Ch 30 §30.11; Ch 18 |
| Ch 53 prereqs | "Chapter 19 (regression)"; "Chapters 37 and 38 (splits, overfitting, precision/recall)"; "Chapter 17 (NumPy and pandas)" | 37; 36 & 39; 18 & 35 |
| Ch 53, 59 | "Chapter 38" for leakage | 36 |
| Ch 54, 55, 56 prereqs | "Chapter 38 (evaluation)" | 39 |
| Ch 16 | "dbt's semantic layer (Chapter 31)" | 32 |
| Ch 49 | "Chapter 62 (economics of data platforms)" | 65 |
| Ch 70 | "Chapter 5's visualization principles, pending that chapter's confirmed…" | 15; remove note |
| Ch 73 | "Chapter 22 (experimentation and causal inference)" | 30, 31 |

Part VIII numbering: 72, 72A, 73, 74, 75, 76A, 76B, 77 — no Ch 76; 72A/76A contain "coordinator should renumber" notes.
Forward prerequisites: 29 → 34, 32 → 34, 11 → 12, 16 → 17/18.

## Drafting leftovers (fixable now)

| Leftover | Where | Count |
|---|---|---|
| "(In the finished book these move to Appendix G.)" | every teaching chapter | 59 |
| "first edition" / "the draft of this book" | Ch 6, 8, 9, 48 (+ Part I) | 8 |
| "coordinator… renumber" notes | 72A, 76A | 3 |
| "pending that chapter's confirmed" / "to be confirmed pointers" | 70, 74 | 2 |
| Build scripts as reader files (checks/, figures/make_figs) | 8, 9, 14, 15 | 7 |
| "₹X … to be confirmed by the ERP team" (maybe intentional template) | 14 | 1 (check) |

## Proposed master order

| Stage | Chapters (reading order) | Changes |
|---|---|---|
| Foundations | 1–9 | No code/formulas (S.1); Ch 2 lightened (0.6); Ch 6 tool-free study chapter, honest hours (S.3, 0.1) |
| Spreadsheets | 10, 11 | Install + first run Ch 10; bridge boxes removed (M.10) |
| SQL | 12, 13 | DB install Ch 12; percentiles in 13 (M.6); calendar table (M.7) |
| Clean, chart, BI | 14, 15, 16 | Spreadsheet + SQL only; Python sections → Ch 18 (M.2); Power BI without pandas (M.1) |
| Python | 17, 18 | Python + Jupyter + terminal basics installed Ch 17, first one-cell notebook; NumPy basics Ch 18 (M.9) |
| Automation, stats, business | 19–25 | Regression basics added (M.5) |
| Terminal, Git, portfolio | 34 (essentials), 26, 27 | Command-line essentials before Git (M.4); CI without pytest (M.8) |
| Advanced analytics | 28–33, 34 (Linux & networking) | pytest in 29; 30/31 point to new regression section |
| ML → architecture | 35–67 | Order unchanged; refs fixed; M.11, M.12 checked in part reviews |
| Interviews, Closing | 68–82, 83 | Renumber 72A/76A/76B; remove coordinator notes |

## Decisions pending (Abhishek)

1. Power BI before Python (recommended; no renumbering) or renumber 17–18 before 16. (M.1)
2. Chapter 34: split — essentials before Git, Linux/networking stay in Part III (recommended) — or move whole chapter. (M.4)
3. Regression basics: end of Ch 22 after correlation (recommended). (M.5)

## Chapter-by-chapter spine (current order)

| Ch | Part | Title | Introduces (first key terms) | Declared prerequisites |
| --- | --- | --- | --- | --- |
| 1 | 0 | What Is Data? | data, datum, information, knowledge, insight | — |
| 2 | 0 | How Computers Store, Move and Protect Data | bit, byte, binary, ASCII, Unicode | 1 |
| 3 | 0 | How a Business Runs on Data | department, lead, quote / quotation, order, delivery challan / delivery note | 1, 2 |
| 4 | 0 | Numbers Without Fear | percentage, percent of, share / proportion, percent change, reverse percentage | 1, 3 |
| 5 | 0 | Thinking Like an Analyst | descriptive question, diagnostic question, predictive question, prescriptive question, habit questions | 1, 3, 4 |
| 6 | 0 | Setting Up to Learn | operating system, RAM (memory), virtual machine, installer, Microsoft Store | 1, 2, 3, 4, 5 |
| 7 | I | The Data Landscape | four questions, ten roles, tracks, team structures | 1, 2 |
| 8 | I | The Career Tree | tiers, skills matrix, JD decoding, salary reading, entry routes | 7 |
| 9 | I | How Expertise Actually Forms | honest timeline, deliberate practice, portfolio, plateaus | 8 |
| 10 | II | Spreadsheet Fundamentals: Excel & Google Sheets | spreadsheet application, workbook, worksheet (sheet), cell, cell address | 1, 2, 3 |
| 11 | II | The Spreadsheet, Mastered: Excel & Google Sheets | lookup array, return array, match mode, search mode, exact match | 10, 12 |
| 12 | II | Databases & SQL Foundations | attribute/column, row/record, table, relational database, DBMS | 1, 3, 10, 11 |
| 13 | II | SQL for Real Analysis | common table expression (CTE), WITH, view, temporary table, window function | 12 |
| 14 | II | Data Cleaning & Preparation | data cleaning, data preparation, staging table, profiling, grain | 1, 10, 11, 12, 13 |
| 15 | II | Data Visualization Principles | data visualization, encoding, graphical perception, pre-attentive attributes, working memory | 1, 4, 10, 11, 13, 14 |
| 16 | II | Business Intelligence with Power BI | business intelligence, Power BI Desktop, Power BI Service, workspace, semantic model (dataset) | 11, 13, 14, 15 |
| 17 | II | Python from Zero | program, Python, interpreter, REPL, script | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 |
| 18 | II | Python for Analysts: pandas & Automation | pandas, DataFrame, Series, index, vectorized operation | 11, 12, 13, 14, 15, 17 |
| 19 | II | Spreadsheet Automation: Macros, VBA, Office Scripts & Google Apps Script | macro, macro recorder, .xlsm, .xlsb, macro security | 10, 11, 14, 15 |
| 20 | II | Automating Reports & Delivering Insights | automation ladder, refreshable, scheduled, triggered, self-serve | 13, 14, 15, 16, 18, 19 |
| 21 | II | Descriptive Statistics & Probability | descriptive statistics, mean, median, mode, weighted average | 4, 15, 17, 18 |
| 22 | II | Statistics Without Fooling Yourself | sampling error, confidence interval, confidence level, margin of error, standard error | 4, 14, 15, 18, 21 |
| 23 | II | Business Acumen, KPIs & Metrics | operating cycle, DIO, DSO, DPO, cash conversion cycle | 4, 18, 21, 22 |
| 24 | II | Requirements, Storytelling & Stakeholders | requirements gathering, clarifying question, business rule, stakeholder mapping, power–interest grid | 15, 23 |
| 25 | II | The Business Analyst Track | business analyst, elicitation, software development life cycle (SDLC), waterfall, Agile | 3, 23, 24 |
| 26 | II | The Professional Toolkit: Git, Agile, Documentation & AI Assistants | version control, repository, working directory, staging area, commit | 6, 12, 13, 17, 18, 20 |
| 27 | II | Capstone: Your Analyst Portfolio | portfolio project, analysis plan, decision log, confounder, segment effect | 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26 |
| 28 | III | Advanced SQL, Performance & Data Modeling | recursive CTE, anchor, recursive part, hierarchy, bill of materials (BOM) | 12, 13 |
| 29 | III | Python as Software, Not Scripts | software, script, pure function, module, package | 2, 12, 17, 18, 26, 34 |
| 30 | III | Inference & Experiments | inference, population, sample, standard error, confidence interval | 17, 21, 22, 29 |
| 31 | III | Causal Inference Without Experiments | causal claim, counterfactual, confounding, selection, treated and untreated groups | 17, 19, 22, 30 |
| 32 | III | Analytics Engineering with dbt | analytics engineering, ETL, ELT, dbt Core, dbt Cloud | 12, 13, 26, 28, 29, 34 |
| 33 | III | The Computer Science You Actually Need | algorithm, complexity, Big-O, constant time, logarithmic time | 17, 28, 29 |
| 34 | III | The Command Line, Linux & Networking Basics | shell, bash, zsh, WSL, prompt | 2, 6, 28 |
| 35 | IV | The Math Under the Models | vector, component, dimension, feature, Euclidean distance | 4, 13, 17, 21 |
| 36 | IV | The Machine Learning Workflow & Feature Engineering | supervised learning, binary classification, regression, target, unit of analysis | 13, 17, 18, 21, 35 |
| 37 | IV | Supervised Learning Algorithms | supervised learning, regression, classification, linear regression, least squares | 35, 36 |
| 38 | IV | Unsupervised Learning | unsupervised learning, clustering, k-means, centroid, inertia | 35, 36, 37 |
| 39 | IV | Evaluation, Tuning, Interpretation & Honesty | confusion matrix, true positive, false positive, false negative, true negative | 35, 36, 37 |
| 40 | IV | Time Series & Forecasting | time series, trend, seasonality, cycle, noise (residual) | 18, 21, 36, 37, 39 |
| 41 | IV | NLP Foundations | unstructured text, tokenization, stop words, stemming, Porter stemmer | 35, 36, 37, 38 |
| 42 | IV | Recommender Systems & Ranking | recommender system, interaction matrix, density (sparsity), popularity baseline, content-based filtering | 35, 37, 38, 41 |
| 43 | IV | A First Look at Deep Learning | neuron, activation function, sigmoid, ReLU (rectified linear unit), vanishing gradient | 35, 36, 37, 41 |
| 44 | IV | Capstone: An End-to-End Data Science Project | value at risk, break-even per row, capacity constraint, reusable pipeline function, default argument | 35, 36, 37, 38, 39, 40, 41, 42, 43 |
| 45 | V | Data Ingestion & Integration | ingestion, source system, system of record, raw layer, staging layer | 2, 12, 13, 18, 29, 32 |
| 46 | V | Pipelines & Orchestration | orchestrator, pipeline, cron, directed acyclic graph (DAG), task | 20, 29, 45 |
| 47 | V | Data Quality, Observability & Contracts | data quality dimensions (accuracy, completeness, validity, uniqueness, consistency, timeliness), data test, failing rows, severity (error, warning), raw, staging, mart layers | 14, 45, 46 |
| 48 | V | Big Data & Distributed Compute | distributed computing, partition, worker (executor), driver, narrow operation | 18, 29, 45, 46, 49 |
| 49 | V | Storage, Warehouses & Lakehouses | row-oriented storage, columnar storage, Parquet, row group, column chunk | 45, 46, 47, 48 |
| 50 | V | Streaming & Real-Time | batch, streaming, latency, event log, topic | 45, 46, 47, 48, 49 |
| 51 | V | Data Activation: Reverse ETL, APIs & System Integration | data activation, reverse ETL, lead score, customer health score, credit hold | 12, 45, 46, 47 |
| 52 | V | The Cloud, Containers & Infrastructure as Code | region, availability zone, shared responsibility model, IAM (identity and access management), least privilege | 46, 47, 49, 51 |
| 53 | VI | Deep Learning in Depth | neuron, weight, bias, activation function, ReLU | 17, 19, 29, 37, 38 |
| 54 | VI | Generative AI & Large Language Models | large language model, next-token prediction, logits, softmax, token | 29, 34, 38, 53 |
| 55 | VI | Building AI Applications: RAG, Agents & Evaluation | retrieval-augmented generation (RAG), corpus, document metadata, chunk, chunking strategy | 29, 33, 38, 54 |
| 56 | VI | MLOps: Making Models Survive Production | MLOps, model lifecycle, data versioning, feature versioning, model artifact | 29, 32, 34, 38, 53 |
| 57 | VI | LLMOps | LLMOps, prompt registry, prompt version, golden set, evaluation floor | 29, 54, 55, 56 |
| 58 | VI | Intelligent Automation | intelligent automation, RPA, screen scraping, API integration, model-assisted intake | 12, 29, 54, 55, 57 |
| 59 | VI | Industry Case Studies | case study, project frame, decision-first framing, baseline, label scarcity | — |
| 60 | VII | Designing Whole Systems | architecture, non-functional requirement (NFR), functional requirement, C4 model, context diagram | — |
| 61 | VII | Distributed Systems & Tradeoffs | distributed system, network partition, CAP theorem, consistency, availability | 45, 46, 49, 50, 51, 57, 60 |
| 62 | VII | Data Architecture Patterns | data architecture pattern, Lambda architecture, batch layer, speed layer, Kappa architecture | 45, 47, 60, 61 |
| 63 | VII | Automation Architecture & Governance | automation architecture, process discovery, value/risk/effort prioritization, tool decision matrix, RPA (robotic process automation) | 19, 20, 46, 51, 58 |
| 64 | VII | Security, Privacy, Governance & Responsible AI | encryption at rest, encryption in transit, least privilege, authentication, authorization | 56, 60, 62, 63 |
| 65 | VII | FinOps: The Economics of Data Platforms | FinOps, cloud billing, on-demand pricing, reserved pricing, compute meter | 1, 60, 64 |
| 66 | VII | Data Strategy, Maturity & Building Data Teams | data strategy, one-page strategy, maturity model, maturity stage, business case | 60, 61, 62, 63, 64, 65 |
| 67 | VII | The Architect as Leader | leverage, business alignment, portfolio thinking, executive storytelling, architecture decision record (institutional memory) | — |
| 68 | VIII | How Data Hiring Works | applicant tracking system (ATS), resume screen, keyword match, recruiter call, hiring-manager round | 7, 8 |
| 69 | VIII | The Extra-Points Method | extra-point moves, five-dimension rubric, correctness, structure & communication, depth & edge cases | 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82 |
| 70 | VIII | Excel, Google Sheets, VBA & BI Question Bank | ATS-safe formatting, SUMIFS / COUNTIFS, XLOOKUP, INDEX / MATCH, absolute vs. relative reference | — |
| 71 | VIII | SQL Question Bank | LEFT JOIN / INNER JOIN, NOT IN NULL trap, NOT EXISTS, WHERE vs. HAVING, correlated subquery | — |
| 72 | VIII | Python & pandas Question Bank | mutable default argument, is vs. ==, object identity, shallow copy, deep copy | — |
| 72A | VIII | Data Structures & Algorithms Question Bank | Big-O notation, time complexity, space complexity, O(1)/O(log n)/O(n)/O(n log n)/O(n²)/O(2ⁿ), amortized complexity | — |
| 73 | VIII | Statistics, Probability & Experimentation Bank | Bayes' theorem, base rate, conditional probability, Monty Hall problem, birthday problem | — |
| 74 | VIII | Machine Learning Question Bank | bias-variance trade-off, underfitting, overfitting, regularization (L1/L2), learning curve | — |
| 75 | VIII | Product Sense, Metrics, Case Studies & Guesstimates | MECE (Mutually Exclusive, Collectively Exhaustive), diagnostic case, product-decision case, leading indicator, lagging indicator | — |
| 76A | VIII | Data Analyst & Data Scientist Question Bank | Data Analyst vs. Data Scientist (role distinction), business-question-first narrative structure, quantified impact, baseline (for a claimed metric), confound (in a resume claim) | — |
| 76B | VIII | Business Analyst Question Bank | elicitation, business requirement, functional requirement, non-functional requirement, business rule | — |
| 77 | VIII | Data Engineering & Data System Design Bank | ETL vs. ELT, batch vs. streaming, data warehouse vs. data lake vs. lakehouse, data contract, CDC (Change Data Capture) | — |
| 78 | VIII | Automation & Integration Question Bank | macro vs. script vs. low-code vs. RPA, report automation, alert fatigue, polling vs. webhook, webhook idempotency | — |
| 79 | VIII | GenAI, LLM & MLOps Question Bank | token, context window, temperature, fine-tuning vs. prompting, embedding | — |
| 80 | VIII | Architecture & Leadership Question Bank | CAP theorem, CP vs. AP, eventual consistency, single point of failure, horizontal vs. vertical scaling | — |
| 81 | VIII | Behavioral, HR & Offer Conversations | STAR method (Situation, Task, Action, Result), story bank, behavioral theme, self-aware weakness, gap explanation | — |
| 82 | VIII | Take-Home Assignments & Mock Interviews | take-home assignment, model submission, mock interview, interviewer scoring notes, one-page summary (take-home) | — |
| 83 | Closing | The Long Game | pace, depth vs breadth, career plateaus, learning how to learn | whole book |