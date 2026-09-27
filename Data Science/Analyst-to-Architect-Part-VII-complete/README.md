# Analyst to Architect — Part VII: Architecture, Governance & Leadership — complete bundle

Chapters 60–67, **all eight approved** (19–20 September 2026). About 61,900 words, 32 figures, 8 approved PDFs.

| Ch | Title | Class | Status | Words |
|---|---|---|---|---|
| 60 | Designing Whole Systems | C | Approved v1 | 8,073 |
| 61 | Distributed Systems & Trade-offs | C | Approved v1 | 8,209 |
| 62 | Data Architecture Patterns | C | Approved v2 | 8,130 |
| 63 | Automation Architecture & Governance | C | Approved v1 | 8,753 |
| 64 | Security, Privacy, Governance & Responsible AI | C | Approved v1 | 8,669 |
| 65 | FinOps: The Economics of Data Platforms | C | Approved v1 | 6,760 |
| 66 | Data Strategy, Maturity & Building Data Teams | C | Approved v1 | 6,494 |
| 67 | The Architect as Leader | C | Approved v1 | 5,750 |

Written in the Part II chat at the author's request, after Parts V and VI were both confirmed complete. With Part VII, the book's teaching arc from Chapter 1 to the architect's chair exists end to end.

## The shape of this part

Almost code-free by design: seven code blocks across eight chapters. Architecture and leadership are taught through worked decisions, templates and figures rather than through programs, so §6.5 barely applies here and the deliverables are documents a reader fills in: ADRs, an NFR worksheet, a failure analysis, a mesh-readiness scorecard, an automation inventory, an access-control matrix, a cost model, a maturity score, a first-90-days plan.

It carries the Part V and Part VI platform decisions as canon: Dagster as the orchestrator, AWS `ap-south-1`, Delta Lake for the sensor table, plain SQL tests for quality.

## What's where

| Folder | Contents |
|---|---|
| `manuscript/` | The eight chapters as Markdown |
| `pdf/` | The eight approved chapter PDFs |
| `figures/` | 32 figures as SVG plus the `make_figs6*.py` scripts |
| `companion/` | Per-chapter templates, worksheets and data: ADR examples and template, NFR worksheet, consistency simulator, failure-analysis worksheets, mesh-maturity scorecard, automation inventory, runbook and charter templates, access-control matrix, classification worksheet, cost model |
| `tools/` | The verifiers, `check_code_teaching.py`, and the PDF builder |
| `planning/` | Chapter map, writing instructions, progress tracker, bible additions, cross-part issues, refresh list, promises, the code-teaching baseline and the coherence-pass strategy |
| `planning/parts/` | Part VII's brief, status file and the coordinator's reply |

## Coordinator checks on this part

All 32 figure references resolve. Every companion file named in the chapters is present.

**Two issues are open, both recorded in `planning/cross-part-issues.md`.**

**Issue 20: Chapter 67 states five times that it is the final chapter of the book**, and describes Part VIII as "the Question Banks in the appendices (Chapters 70 through 79)". The chapter map has Part VIII as Chapters 68–82, fifteen question banks; the Architecture & Leadership bank is Chapter 80; the appendices are A to H; and **Chapter 83, The Long Game, is the closing chapter**. Chapter 67 remains the last chapter of the path, but it has to hand off rather than close. Five framing sentences, no content change. The alternative, dropping Chapter 83, is the author's decision.

**Issue 21: the worst style drift in the book.** 773 em dashes in prose and 93 uses of *genuinely* or *honestly* across the eight chapters, against §5.2, and four American-spelling fixes:

| Ch | Em dashes in prose | *genuinely* / *honestly* |
|---|---|---|
| 60 | 87 | 9 |
| 61 | 93 | 6 |
| 62 | 120 | 11 |
| 63 | 117 | 13 |
| 64 | 107 | 8 |
| 65 | 92 | 13 |
| 66 | 80 | 25 |
| 67 | 77 | 8 |

The same chat wrote Part II's Chapters 23 and 24, which carry 53 and 84. Every other part in the book sits between zero and fifteen, and Part VI managed zero across 66,400 words. This is one chat's style scan rather than eight chapters' writing, and it is fixed in one pass across all ten of that chat's chapters. Each em dash needs the punctuation the sentence actually wants; a blind search and replace makes the prose worse.

**Approved:** Chapter 67's departure from the exercises-and-answers format. A chapter whose own project says "there is no answer key" should not carry a drill section, and "Questions to sit with" is the right substitute, provided the *Key terms* list and recap stay and one sentence explains why the format differs.

**Code teaching (§6.5):** Chapters 61, 64, 65 and 66 have one or two flagged blocks each; 60, 62, 63 and 67 have no code at all.

## Open items

- Issues 20 and 21 above.
- The review pass (§15.1) for this chat covers **both** its parts, II and VII, with the style scan run across all ten chapters in one pass.
- **Chapters 25, 26 and 27 are still unwritten.** They are the only hole left in the book's teaching spine.

`planning/parts/part-7-coordinator-reply.md` has the full reply; `planning/parts/part-7-status.md` has the per-chapter reports.

## The rules every chapter follows

`planning/chapter-writing-instructions.md` is the master brief. Two sections matter most:

- **§6.5** — teach code and formulas line by line, with a settings table and a measured what-if.
- **§15.1** — the part-completion review pass: read the part straight through, work out the cause at the level of the part, and only then fix in place.

Riverstone Supplies is fictional. Every person, customer, product and number in the data is invented.
