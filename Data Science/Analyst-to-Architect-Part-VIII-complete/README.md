# Analyst to Architect — Part VIII: The Interview Playbook — complete bundle

Seventeen chapters, **all approved** (20 September 2026). About 110,400 words. No figures, which is correct for question banks.

With Part VIII, **every part of the book has been written**. What remains is Chapters 25, 26 and 27, the closing chapter, and Appendices A to H.

| Ch | Title | Words |
|---|---|---|
| 68 | How Data Hiring Works | 8,029 |
| 69 | The Extra-Points Method | 4,255 |
| 70 | Excel, Google Sheets, VBA & BI Question Bank | 7,498 |
| 71 | SQL Question Bank | 12,764 |
| 72 | Python & pandas Question Bank | 8,838 |
| **72A** | **Data Structures & Algorithms Question Bank** (new) | 5,926 |
| 73 | Statistics, Probability & Experimentation Bank | 7,507 |
| 74 | Machine Learning Question Bank | 6,135 |
| 75 | Product Sense, Metrics, Case Studies & Guesstimates | 6,089 |
| **76A** | **Data Analyst & Data Scientist Question Bank** (new) | 5,062 |
| 76B | Business Analyst Question Bank (was 76) | 6,522 |
| 77 | Data Engineering & Data System Design Bank | 6,507 |
| 78 | Automation & Integration Question Bank | 5,377 |
| 79 | GenAI, LLM & MLOps Question Bank | 6,789 |
| 80 | Architecture & Leadership Question Bank | 4,200 |
| 81 | Behavioral, HR & Offer Conversations | 5,110 |
| 82 | Take-Home Assignments & Mock Interviews | 3,800 |

## Numbering

**72A** and **76A** are new chapters, accepted into the plan and recorded in the chapter map with provisional letters per instructions §14.5. The original Chapter 76 is now **76B**.

At the renumbering pass the book becomes **85 chapters**: Part VIII runs 68 to 84, and The Long Game becomes Chapter 85. Every forward reference above Chapter 72 is re-checked in that same pass.

**Why 72A was accepted:** Chapter 33 teaches the computer science an analyst needs and nothing in the plan tested it. A candidate interviewing for data engineering or data science at a product company meets these questions.

**Why both 76A and 76B were kept:** the narrowed Data Analyst, Data Scientist and Data Engineer focus is right for where depth goes, but the business analyst track is the subject of Chapter 25 and a core reader of this book.

## What makes this part worth its price

Every answer traces back to the chapter that taught it. That link is what separates this from every other question bank, and preserving it is the first thing to check in the review pass.

## What's where

| Folder | Contents |
|---|---|
| `manuscript/` | The seventeen chapters as Markdown |
| `companion/` | The Riverstone practice data every SQL and spreadsheet question runs against: `riverstone_setup_mini.sql` and `riverstone_2025_setup.sql` for PostgreSQL, `mysql/` for the MySQL equivalents, and `ch70/riverstone_orders_mini.md`, the small verified table Chapter 70's formula questions use |
| `tools/` | The verifiers, `check_code_teaching.py`, and the PDF builder |
| `planning/` | Chapter map, writing instructions, progress tracker, bible additions, cross-part issues, refresh list, promises, the code-teaching baseline, and the coherence-pass and go-to-market strategies |
| `planning/parts/` | Part VIII's brief, status file and the coordinator's reply |

Chapter PDFs are delivered separately. Load the companion SQL into PostgreSQL 16 or MySQL 8.0 to re-run any query in Chapters 70 to 82.

## Coordinator checks on this part

**Zero em dashes in prose across 110,400 words**, matching Part VI as the cleanest in the book. No missing references.

**To fix in the review pass:**

1. **Two established characters reused in generic stories.** Chapter 73's real-world story uses **Farah** at "a mid-size company" and Chapter 80's uses **Vikram**. Farah Khan's arc runs from Chapter 8 to Chapter 44; Vikram Singh is the Sales Manager, Key Accounts. Rename both to names used nowhere else. Cross-part issue 22.
2. **Seventy-seven uses of *genuinely* or *honestly***, across fourteen chapters. Chapter 68 has fourteen, Chapter 77 has ten, Chapters 71 and 81 seven each. Both are banned in §5.2.
3. **Chapter 76B was written against a Chapter 25 that does not exist.** The coordinator re-checks its cross-references and section numbers when Chapter 25 is written. Cross-part issue 23.

**Code teaching.** Most of the part has no code, which is right. Where it does, the proportions are the best in the book. A question bank's standard differs: an answer needs no settings table, but every code answer must be runnable and every answer must be checkable against the chapter that taught it. Chapters 72A (6 of 13 blocks flagged) and 73 (7 of 11) are the two to look at.

| Ch | Code blocks | Blocks flagged | Ch | Code blocks | Blocks flagged |
|---|---|---|---|---|---|
| 71 | 32 | 8 | 78 | 3 | 1 |
| 72 | 22 | 5 | 79 | 4 | 2 |
| 72A | 13 | 6 | 80 | 1 | 1 |
| 73 | 11 | 7 | 82 | 5 | 3 |
| 74 | 3 | 1 | | | |
| 77 | 4 | 1 | | | |

`planning/parts/part-8-coordinator-reply.md` has the full reply; `planning/parts/part-8-status.md` has the per-chapter reports, including every self-caught error and its fix.

## The rules every chapter follows

`planning/chapter-writing-instructions.md` is the master brief. Two sections matter most:

- **§6.5** — teach code and formulas line by line. For a question bank this means runnable code answers that trace to the chapter that taught them.
- **§15.1** — the part-completion review pass: read the part straight through, work out the cause at the level of the part, and only then fix in place.

Riverstone Supplies is fictional. Every person, customer, product and number in the data is invented.
