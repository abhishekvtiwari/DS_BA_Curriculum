# Part Brief — Part VII — Architecture, Governance & Leadership

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-7-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 60–67**.

## Chapters

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

## Reference chapters for this part

Chapters 1 and 2 (class C) for voice; Chapter 13 for pattern tables.

## Guidance specific to this part

- **Case-based architecture writing.** Every pattern is shown on Riverstone at a realistic scale (plants, sales, website, support), with diagrams drawn by script, trade-off tables, and a decision record.
- **Chapter 63 (Automation Architecture & Governance)** is the architect-level end of the automation thread: inventory of Riverstone's automations from Chapters 19–20, 46, 51, and 58; ownership, monitoring, credentials, and change control.
- **Chapter 64 (Security, Privacy, Governance & Responsible AI)** delivers what Chapters 1, 2, and 12 promised: privacy and governance in depth, DCL (`GRANT`/`REVOKE`) and access models, data protection laws (verify current status of India's DPDP Act rules, GDPR, and others at the time of writing; general information, not legal advice).
- **Chapter 65 (FinOps)** delivers Chapter 2's promise about cloud bills growing quietly; any prices must be verified and dated, or shown as clearly illustrative.
- **Leadership chapters** avoid generic management advice: ground every point in a Riverstone situation.

## Sequencing and dependencies

Start after Parts V and VI are mostly written.

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

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

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 64

- *(from Ch 1)* Chapter 64 covers privacy and governance properly.
- *(from Ch 2)* Chapter 64 covers privacy and governance in depth.
- *(from Ch 2)* Part V (Chapters 45–52) builds on formats, compression, the cloud, and APIs at company scale; Chapter 64 covers security, privacy, and governance in depth.
- *(from Ch 12)* Chapter 64 covers it.

#### Chapter 65

- *(from Ch 2)* The trade-offs: bills that grow quietly if nobody watches them (Chapter 65), dependence on one provider, and questions about where the data is physically stored.

## Kickoff prompt

```
You are writing Part VII — Architecture, Governance & Leadership of the book "Analyst to Architect" (Chapters 60–67).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-7-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-7-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```

## Coordinator notes (added 17 Sep 2026, after Part I)

- **Chapter 66 (data strategy and teams):** Chapter 7 §7.5 introduces centralized, embedded, and hub-and-spoke teams, and Chapter 7's story shows Riverstone choosing an analyst-who-automates before a data scientist. Build on both; use the role names in instructions §2.
- **Chapter 63 (automation governance):** Chapter 7 §7.4 introduces the automation and integration track and "who owns an automation".
