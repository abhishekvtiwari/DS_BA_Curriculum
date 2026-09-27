# Part Brief — Closing & Appendices

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-closing-appendices-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapter 83 and Appendices A–H**.

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| PC-83 | 83 | The Long Game | C | 2,500 | Not started | `manuscript/ch83-the-long-game.md` |

### Appendices (blueprint)

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

## Reference chapters for this part

Chapters 1 and 2 for voice.

## Guidance specific to this part

- **Written last**, after the teaching chapters they compile.
- **Chapter 83 (The Long Game)** is kept almost entirely from the draft's Chapter 33 (`analyst-to-architect-book.md`); update references and remove the "expect plateaus" material now covered in Chapter 9.
- **Appendix A (Glossary):** compile every term from every chapter's Key terms, with a plain-English definition consistent with the chapter's first-use definition and the chapter where it's taught.
- **Appendix B (Tools & installation):** compile and re-verify install steps from Chapter 6 and Chapter 12 section 12.3, dated.
- **Appendix E (Datasets):** compile the data specs from `planning/data/` and the existing Riverstone databases (instructions, section 7.3), with schema diagrams drawn by script.
- **Appendix G (Answers):** move every chapter's "Answers to practice exercises" section here, unchanged except numbering.
- **Appendix F (Cheat sheets):** one or two pages each, every snippet verified.
- **Appendix H (Role profiles):** consistent with Chapters 7–8 and Chapter 68.

## Sequencing and dependencies

Start when Parts 0–VII are written.

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

**Ch 83. The Long Game** · KEPT from draft Ch 33 · 2,500 words
Kept almost entirely (it's one of the draft's strongest chapters). The "expect plateaus" material also appears early in Ch 9.

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

_No approved chapter makes a specific promise about these chapters yet. Re-run `tools/extract_promises.py` as chapters are approved._

#### Appendix A

- *(from Ch 1)* (All terms are defined in the Glossary, Appendix A.)*
- *(from Ch 2)* (All terms are defined in the Glossary, Appendix A.)*
- *(from Ch 12)* (All terms are defined in the Glossary, Appendix A.)*
- *(from Ch 13)* (All terms are defined in the Glossary, Appendix A.)*

#### Appendix B

- *(from Ch 12)* Installation steps and screens change over time; Appendix B keeps current, step-by-step instructions for both databases.

#### Appendix E

- *(from Ch 2)* Practice data: four Riverstone orders saved in five formats, and a demonstration API, both in the companion files (Appendix E).
- *(from Ch 2)* The companion files include a tiny demonstration API for Riverstone that runs on your own computer (Appendix E).
- *(from Ch 2)* The companion files (Appendix E): `orders_feb_2026` in `.csv`, `.xlsx`, `.json`, `.xml`, and `.parquet`; and `api_demo.py`, the demonstration API used in section 2.8, which you'll run yourself in Chapter 18.
- *(from Ch 12)* Practice data: the Riverstone Supplies database (Appendix E), in PostgreSQL and MySQL versions.
- *(from Ch 12)* The full-size version, with thousands of orders, is in the companion files (Appendix E).
- *(from Ch 12)* Load the data. Open `riverstone_setup.sql` from the companion files (Appendix E) and run the whole script (*Execute SQL Script*, not *Execute Statement*).
- *(from Ch 12)* The Riverstone practice files (Appendix E): `riverstone_setup.sql` (the small database used in this chapter), its MySQL twin `riverstone_setup_mysql.sql`, `ch12_queries_mysql.sql` (every query in this chapter, tested in MySQL), `ch12_lab_postgresql.sql` and `ch12_lab_mysql.sql` (every statement from section 12.13 and exercises 23–27, in order), and the full-size version with thousands of orders, f
- *(from Ch 12)* Option B: the full Riverstone dataset from Appendix E, if you don't have suitable work data.
- *(from Ch 13)* To set it up, create a database called `riverstone_2025` and run `riverstone_2025_setup.sql` from the companion files (Appendix E), exactly as you did in section 12.3.

#### Appendix G

- *(from Ch 1)* (In the finished book these move to Appendix G.)*
- *(from Ch 2)* (In the finished book these move to Appendix G.)*
- *(from Ch 12)* (In the finished book these move to Appendix G.
- *(from Ch 13)* (In the finished book these move to Appendix G.

## Kickoff prompt

```
You are writing Closing & Appendices of the book "Analyst to Architect" (Chapter 83 and Appendices A–H).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-closing-appendices-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-closing-appendices-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```

## Coordinator notes (added 17 Sep 2026, after Part I)

- **Chapter 83 (The Long Game):** plateau material now lives in Chapter 9 §9.7 (Farah's 12-week log). Chapter 83 should refer back and cover later-career plateaus rather than repeat it.
- **Appendix B:** Chapter 6 §6.2–6.3 lists the verified versions and install methods (17 Sep 2026); start Appendix B from those.
