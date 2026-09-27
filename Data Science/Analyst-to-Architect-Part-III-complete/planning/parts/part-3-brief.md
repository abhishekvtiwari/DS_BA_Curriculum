# Part Brief — Part III — Advanced Analytics & Analytics Engineering

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-3-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 28–34**.

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P3-28 | 28 | Advanced SQL, Performance & Data Modeling | A | 7,000 | Not started | `manuscript/ch28-advanced-sql-performance-and-data-modeling.md` |
| P3-29 | 29 | Python as Software, Not Scripts | B | 5,000 | Not started | `manuscript/ch29-python-as-software-not-scripts.md` |
| P3-30 | 30 | Inference & Experiments | B | 6,000 | Not started | `manuscript/ch30-inference-and-experiments.md` |
| P3-31 | 31 | Causal Inference Without Experiments | B | 3,500 | Not started | `manuscript/ch31-causal-inference-without-experiments.md` |
| P3-32 | 32 | Analytics Engineering with dbt | A | 5,000 | Not started | `manuscript/ch32-analytics-engineering-with-dbt.md` |
| P3-33 | 33 | The Computer Science You Actually Need | B | 4,500 | Not started | `manuscript/ch33-the-computer-science-you-actually-need.md` |
| P3-34 | 34 | The Command Line, Linux & Networking Basics | B | 3,000 | Not started | `manuscript/ch34-the-command-line-linux-and-networking-basics.md` |

## Reference chapters for this part

Chapter 13 (class B structure, pattern-library style); Chapter 12 for Chapters 28 and 32 (class A).

## Guidance specific to this part

- **Assumes all of Part II.** Don't re-teach joins, window functions, or pandas basics; build on Chapters 12–13 and 17–18 with explicit back-references.
- **Chapter 28 must deliver what Chapters 12 and 13 promised:** recursive CTEs (org charts from the `employees` table, bills of materials), advanced frames, indexes and `EXPLAIN` with real query plans from PostgreSQL (and MySQL where they differ), normalization 1NF–3NF worked on Riverstone tables, the grain discipline, and schema migrations (versioned change scripts; the author added this after section 12.13). Performance examples need data large enough to matter: generate a larger seeded Riverstone orders table and report real timings and plans, noting the machine.
- **Chapter 30 (Inference & Experiments):** Chapter 13 exercise 15 promises a proper test design; use Riverstone lead-source or website data, seeded, computed with Python.
- **Chapter 32 (dbt):** Chapters 12 and 13 promise SQL linting and dbt models replacing shared views like `sales_lines`. Build a small, runnable dbt project on the Riverstone PostgreSQL database (dbt-core with the Postgres adapter can run locally), verify commands and outputs, and check current dbt terminology against official docs ("verify current tooling when writing", per the blueprint).
- **Chapters 33–34** are class B: runnable examples in Python and the shell, real output.

## Sequencing and dependencies

Start after Part II Chapters 12–13 (done) and ideally after 17–18. Chapter 28 can start now.

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

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

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 28

- *(from Ch 12)* You'll study its formal rules (first, second, and third normal form) in Chapter 28.
- *(from Ch 12)* Chapter 28 builds a whole discipline on this idea.
- *(from Ch 12)* Chapter 28 shows how to see what it actually does.)
- *(from Ch 12)* You'll meet them in Chapter 28.
- *(from Ch 12)* Chapter 28 returns to databases from the designer's side: normalization rules, indexes, and query performance.
- *(from Ch 13)* Chapter 28 uses recursive CTEs for another classic job: walking an org chart from the managing director down, however many levels deep it goes.
- *(from Ch 13)* Chapter 28, Advanced SQL, Performance & Data Modeling, covers recursive CTEs, advanced frames, indexes, and query plans, for when these queries meet millions of rows.

#### Chapter 30

- *(from Ch 13)* Chapter 22 explains why small samples mislead, and Chapter 30 shows how to run a proper test.

#### Chapter 32

- *(from Ch 12)* You'll see that layout in Chapter 32.
- *(from Ch 12)* You'll meet that in Chapter 32.
- *(from Ch 13)* A shared view (and, later, the dbt models of Chapter 32) is how data teams end that argument.
- *(from Ch 13)* DBeaver's *Format SQL* command is a good start; Chapter 32 introduces automatic formatting ("linting") for teams.

## Kickoff prompt

```
You are writing Part III — Advanced Analytics & Analytics Engineering of the book "Analyst to Architect" (Chapters 28–34).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-3-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-3-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```

## Coordinator note (17 September 2026): new reading order for Part III

Part III is reordered so tools come before the work that needs them, and the two statistics chapters stay together at the end. The mapping is in `planning/chapter-map.md`; the reading order is:

1. **Advanced SQL, Performance & Data Modeling** (Ch 28)
2. **The Command Line, Linux & Networking Basics** (old Ch 34) — moved up, because dbt, Git and Python packaging all assume a terminal
3. **Python as Software, Not Scripts** (old Ch 29)
4. **Analytics Engineering with dbt** (old Ch 32) — builds on SQL modeling, the terminal and Git
5. **The Computer Science You Actually Need** (old Ch 33)
6. **Inference & Experiments** (old Ch 30) — continues Chapters 21–22
7. **Causal Inference Without Experiments** (old Ch 31)

What this means for writing:

- **Keep current file numbers**; the coordinator renumbers at assembly.
- Write each chapter assuming the chapters **above it in this list** are done, not the old numeric order. For example, dbt may assume the command line and Git; Python as software may assume the terminal.
- Part II's blocks (spreadsheets, SQL, Python, then cross-tool chapters) are the foundation: assume a reader who can write SQL and pandas, clean data in three tools, and build a dashboard.
- Chapter 28 must not repeat Chapter 13's window functions; it goes further (recursive queries, indexes, `EXPLAIN`, star schemas, slowly changing dimensions, migrations).
