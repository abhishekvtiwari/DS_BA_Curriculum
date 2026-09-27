# Part Brief — Part I — The Map

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-1-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 7–9**.

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P1-07 | 7 | The Data Landscape | C | 4,000 | Not started | `manuscript/ch07-the-data-landscape.md` |
| P1-08 | 8 | The Career Tree: How Skills Unlock Roles | C | 5,000 | Not started | `manuscript/ch08-the-career-tree-how-skills-unlock-roles.md` |
| P1-09 | 9 | How Expertise Actually Forms | C | 2,500 | Not started | `manuscript/ch09-how-expertise-actually-forms.md` |

## Reference chapters for this part

Chapters 1 and 2 (class C) for voice and structure.

## Guidance specific to this part

- **These chapters expand the draft's Chapters 1–3.** The draft is in the project as `analyst-to-architect-book.md` (and the PDF/DOCX). Keep what the blueprint says to keep (the four questions and the tracks; tiers, keys and doors; the honest timeline) and fix the review issues listed in blueprint section 9: the "three questions" heading that lists four, and the tier order that doesn't match the part order.
- **Careers facts change fast.** Job titles, role definitions, tools in job descriptions, hiring trends, and especially **salaries** must be verified against current, reputable sources (surveys, official job-market reports) at the time of writing, with the date and source recorded in your chapter report. Prefer ranges and patterns over precise figures; never invent a salary. Say clearly that numbers vary by city, company, and year.
- **Role list must match the rest of the book:** data analyst, business analyst, BI developer, analytics engineer, data scientist, ML engineer, data engineer, AI engineer, automation analyst / RPA developer / integration engineer, data architect. The reader pathways table in the blueprint (section 5) is the source.
- **Decoding a job description** (Ch 8): write a realistic but fictional job description; don't copy a real company's posting.
- **Riverstone:** use a single Riverstone project walked through every role (blueprint Ch 7), consistent with the business process defined in Chapter 3.
- **Data and tools:** no databases needed. Figures matter here: the career tree, skills matrix, and team structures should be clear, drawn diagrams.

## Sequencing and dependencies

Can start immediately. Coordinate role names with Part VIII (Chapter 68) through the coordinator.

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

**Ch 7. The Data Landscape** · EXPANDED from draft Ch 1 · 4,000 words
Kept: the four questions and the tracks. Added: how data teams are organized (centralized, embedded, hub-and-spoke) · a single project walked through every role, from request to dashboard to model to platform · how AI assistants are changing each role · the process automation and integration track (automation analyst, RPA developer, integration engineer) and why every data role includes some automation · fixes the "three questions" vs four inconsistency.

**Ch 8. The Career Tree: How Skills Unlock Roles** · EXPANDED from draft Ch 2 · 5,000 words
Kept: tiers, keys and doors. Added: a skills matrix per role · decoding a real-style job description · a day in the life of each role · the reader pathways table and the automation thread (section 5) · entry routes: fresher, career switcher, internal move · aligns the tier order with the book's part order (fixes the draft's tier 3 / tier 4 mismatch).

**Ch 9. How Expertise Actually Forms** · EXPANDED from draft Ch 3 · 2,500 words
Kept: the honest timeline and the three ingredients. Added: deliberate practice · building a portfolio as you learn · finding feedback and mentors · handling plateaus (moved forward from the Closing chapter so readers get it early).

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 7

- *(from Ch 12)* It is the one skill shared by every role on the map from Chapter 7: analysts, business analysts, data scientists, data engineers, and architects all write SQL, often every day.

## Kickoff prompt

```
You are writing Part I — The Map of the book "Analyst to Architect" (Chapters 7–9).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-1-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-1-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```
