# Chapter 76B, Business Analyst Question Bank: changelog

Branch `part-VIII`. One line per finding: `ID · what changed · where · option used`.
Section map (old → new): 76.1 Requirements gathering → **76B.2**; 76.2 Basic-but-tricky → **76B.1** (moved to the front); 76.3–76.8 → **76B.3–76B.8**. Question IDs: Q76-NNN → **Q76B-NNN** (same number, so Q76B-001 is still "make the report better" and Q76B-033 still "can you just change the number?").

## Content
- 76B.1 · "A note on sourcing" deleted; "Where this leads" drafting half replaced by "Chapters 24 and 25 teach every technique this bank tests…; each question's 'Learn it in' names the section"; the re-check was done (76B.2–76B.8, 76B.12, 76B.13) · front matter, Where this leads · —
- 76B.2 · Q76B-028's gap example switched to the one Ch 25 chose under row 25.1 option A: step 8, the delivery (paper POD, no delivery date); no longer claims manual invoicing, so no clash with Ch 3 §3.2 step 7 · §76B.6 Q76B-028 · followed Ch 25's option A
- 76B.3 · Root cause now matches Ch 25 §25.9 / Figure 25.4 ("not 'the warehouse is slow'… the driver has no device"); requirement FR-14 plus the NFR it depends on (NFR-09), same numbers as Ch 25; extra point [+Validate] "asks 'why' once more than feels necessary"; follow-up reworded · §76B.6 Q76B-028 · —
- 76B.4 · Q76B-033 Passes tier rewritten (politely holds the number, no diagnosis); "quietly changes the number" moved to the red flag as an integrity failure; Learn it in Ch 24 §24.8 (Figure 24.4) · §76B.7 · —
- 76B.5 · Q76B-025 rewritten: product backlog (Product Owner orders it) vs sprint backlog (developers own it); one-line definition of Product Owner · §76B.5 rapid-fire · —
- 76B.6 · Q76B-018 swimlane uses Ch 25 Figure 25.1's lanes and step numbers (order typed into the ERP, not CRM); new [+Evidence] extra point: five of nine transitions cross a lane (recomputed in checks/ch76b_check.py) · §76B.4 · — (the finding said "Figure 25.2"; the swimlane is Figure 25.1 in the current Ch 25)
- 76B.7 · Q76B-038 re-based on Ch 25 §25.12's payment matching (bank line → invoice, step 9); draft requirement has the ₹1 tolerance, a named exception owner and an audit trail; new [+Scale] move · §76B.8 · —
- 76B.8 · Q76B-013 criteria name the actual rule (Ch 25's 1.5× own-gap rule, FR-01), add scope (AC-1), too-new edge case (AC-3), empty state kept (AC-4), reconciliation (AC-5); counts quoted (3 flagged, 7 too new of 24, recomputed on riverstone_2025); the model-specific "top factors" and "24 hours" criteria became a follow-up and a [+Limits] point (NFR-01) · §76B.3 · used the finding's second choice (Ch 25's rule): no 0.30 churn threshold exists in Ch 39 §39.5
- 76B.9 · Sections renumbered 76B.1–76B.8, IDs Q76B-001–038, all internal refs and the final-week list updated · whole chapter · — (inbound refs in Ch 76A/78/81/82: see questions file)
- 76B.10 · "user stories (§76.4)" → "(section 76B.3)" · Q76B-007 · —
- 76B.11 · Pointers for INVEST, spike, Definition of Done, Product Owner → Ch 26 §26.10; Gherkin → Ch 25 §25.8; stakeholder register → Ch 24 §24.3 (already added there in Part 2). The teaching text for Ch 26 §26.10 and Ch 25 §25.8 is handed to the integrator · rapid-fire 76B.1/3/5 · option (a) (recommended)
- 76B.12 · Q76B-003 business rule: two kinds (constraints and definitions), matching Ch 24 §24.2; Learn it in 24.2 and 23.13 · §76B.2 · —
- 76B.13 · Every question has a section-level Learn it in (core: line; rapid-fire: "Level · learn it in" column); pointers into the bank itself or to Ch 69 only replaced; 24 cited sections all checked to exist (checks/ch76b_check.py) · whole chapter · —
- 76B.14 · Q76B-023 uses Ch 25 §25.2's six phases and verbs (write/review the UAT plan in Test; users run UAT in Deploy, BA facilitates); "phase names vary; the sequence doesn't"; extra point on not driving the mouse · §76B.5 · —
- 76B.15 · Q76B-029 new [+Validate] extra point: reconcile one complete period against a trusted source at more than one level of aggregation · §76B.6 · —
- 76B.16 · Passes rows rewritten for Q76B-001, Q76B-013, Q76B-018 as the finding gives · §76B.2–76B.4 · —
- 76B.17 · Q76B-007 FRD now "written for developers and testers… two developers build the same thing"; BRD "readable by someone who will never log in"; SRS per Ch 25 §25.7 · §76B.1 · —
- 76B.18 · Q76B-002 new extra point naming a data-specific NFR (freshness, reconciliation), tagged [+Edge cases] · §76B.2 · —
- 76B.19 · Technique list kept in Q76B-004; one-line addition to Ch 25 §25.3 handed to the integrator · §76B.2 · first choice (add the line to Ch 25)
- 76B.20 · Farah is "now a data analyst whose first project turned out to be requirements work"; finance's need is dormant accounts with open balances for a bad-debt review · In the real world · first choice (keeps Farah, whom Ch 81 cites)
- 76B.21 · Ch 78 bullet: "takes automation from the requirement (Q76B-038) to the build: choosing the tool, retries, idempotency, and alerting" (checked in Ch 78) · Where this leads · —
- 76B.22 · Tools: Chapter 11's spreadsheet skills (as Ch 25 §25.7 says) · Project · —
- 76B.23 · "Chapter at a glance" gains Before you start and Time needed (2.5–3 h drill + 4–6 h project) · front matter · —
- 76B.24 · Level (Fresher/Mid/Senior, the scale of Ch 70, 74, 75, 76A) and roles on every question; basic-but-tricky section moved to the front (76B.1); one line on where an entry-level candidate starts · whole chapter · first choice (move the basic section to the front)
- 76B.25 · Heading "76B.8 Full scenarios, talked through live" (same wording as Ch 75 and 76A, per coordinator) · §76B.8 · —
- 76B.26 · Q76B-038 says what 15% implies (about 85% of lines unattended, worth building if the rest go to a named person) · §76B.8 · —

## Visual
- V76B.1 (High) · sourcing note deleted; rebuilt p. 2 shows the glance box without it · before/after: img/ch76b-V76B.1-before.png, img/ch76b-V76B.1-after.png
- V76B.2 · 76B.x sections and Q76B- IDs; contents page shows 76B.1–76B.8 with page numbers
- V76B.3–V76B.11 · done by the style pass; rechecked on the rebuilt PDF (swimlane on four lines, no ID wraps, cover clean, contents numbered 11/11, no stranded heads)

## Also
- Old tags converted to Chapter 69's twelve (`**[+Tag]**`): [Real evidence] → [+Evidence]; the five "[Learn it in]" extra points (Q76B-010, 016, 030, 035, 036) became real tags ([+Assume], [+Signpost], [+Validate], [+Edge cases]) with the pointer moved to the learn-it-in column.
- New check: `checks/ch76b_check.py` (sections exist, quoted facts in the credited section/figure, IDs 1–38, tag set, at-risk counts from riverstone_2025).

---

# 3 October 2026 · Five new sections, 38 questions to 95

57 questions, Q76B-039 to 095. Nothing renumbered. Book 4 rebuilt: **648 → 680 pages**, 416
internal links all resolving, 881 bookmarks all landing correctly, no missing glyphs.
`checks/ch76b_check.py` passes (its expected ID range updated 1..38 → 1..95; all 35 cited sections
verified to exist). `check_bank.py`: 95 questions, range 001–095, no duplicates or gaps, 0 uneven
tables.

**Part VIII is now 1,113 questions**, which passes the "more than 1100 questions" claim.

76B was the thinnest bank in Part VIII — 38 questions across 8 sections, 5 or 6 each, and §76B.8 had
one. It also matters more than its size suggested: the BA audience is who the interview book is
sold to.

## The gap that set the scope

Measured against the chapter, not estimated. Absent entirely before this: **every** prioritisation
framework (MoSCoW, RICE, Kano, WSJF), most Agile vocabulary (epic, velocity, burndown, refinement,
MVP, planning poker, t-shirt sizing, WIP limit), the tools (Jira, Confluence, wireframes,
prototypes), the analysis frameworks (SWOT, RAID, fishbone, CRUD matrix), estimation, data
dictionaries, ERDs, certification (BABOK/CBAP), and domain scenarios of any kind.

| | |
|---|---|
| 76B.9 Prioritisation | MoSCoW, RICE, Kano, WSJF, value-vs-effort, dependencies, technical debt |
| 76B.10 Agile in practice | Points, velocity, burndown, refinement, MVP, ceremonies, estimation |
| **76B.11 The ambiguity drill** | **Produce the questions, not the answer** |
| 76B.12 Tools, artifacts and estimation | Jira, wireframes, data dictionary, ERD, CRUD, RACI, RAID |
| 76B.13 Domain scenarios | Logistics, e-commerce, financial services |

## 76B.11 is the section that exists in no other bank

Owner decision, 3 October: include it. Every other bank in Part VIII asks for an answer; this one
asks for the **questions**, because that is the BA skill and it is what an interviewer tests by
handing over a vague request and watching.

**The drills run on Riverstone's Q4 2025 order data** — the file Chapter 14 cleans and Chapter 72B
interrogates — so the cost of not asking is measured rather than asserted:

- **"Send me last month's revenue"** has four defensible answers spanning **₹6.25 crore (16%)**:
  gross ₹45.89 cr, net all lines ₹44.26 cr, net excluding cancelled ₹42.39 cr, delivered only
  ₹39.63 cr. The cancelled-orders question alone is worth **₹1.87 crore**.
- **"How many orders?"** is 25,832 lines or 14,372 orders — **80%**, with no symptom.
- **"Top five customers"** by revenue and by order count share **zero names**. Not a different
  order: a different set of customers, both lists correct.
- **"Average order value"** is ₹17,133 per line or ₹30,794 per order, median ₹26,250.
- **"Your December doesn't match finance's"** — dating the same lines by UTC rather than IST moves
  December by **₹1.42 lakh** with no bug anywhere and both figures correctly computed.

Each drill gives the questions, says which move the number most, and ends with the reply to send.
The rule is stated up front: ask the three questions that change the answer, not the eleven you
could think of.

## The named frameworks are marked Beyond the book

Chapter 25, §25.12 teaches this book's own ranking method (frequency, time per occurrence, cost of
errors caused, effort and risk) and not MoSCoW, RICE, Kano or WSJF. Rather than pretend otherwise,
§76B.9 marks them **Beyond the book** with a one-line primer each, the convention Chapter 72A
already uses for the DSA topics past Chapter 33. The questions then test them honestly, including
what each is bad at — MoSCoW has no forcing function so everything becomes a Must; RICE invites
false precision; Kano produces categories rather than an order.

## Errors caught before they shipped

- **A figure was quoted as measured when the book calls it illustrative.** The RICE example
  justified its 80% Confidence with "Chapter 3 measured the 6 minutes per order". Chapter 3, §3.7
  says "round numbers for illustration". Rewritten so Confidence rests on the volume being
  *countable from the sales inbox*, with a warning added against exactly the error the draft made —
  which is the subject of Q76B-043.
- **Six ambiguity drills lacked `Answer in one line:`**, caught by `check_bank.py`. The omission was
  deliberate (the answer *is* the questions) but the house format requires all five parts, so each
  now opens with one line naming what the ask is hiding.
- **Five malformed tier-table cells** (`| Extra points + **[+…]**`, missing the separator).
- **§63.2 was cited for access control**; it is "Process discovery and prioritization". Corrected to
  §63.9, "Controls: approvals, segregation of duties, audit trails, change management".
- **Q76B-038**, the pre-existing "Full scenario, talked through live", still lacks three of the five
  house parts. A walk-through by design, the same deviation other banks carry; not touched.

## Also in this commit: ch72b's section pointers were wrong, and are fixed

`checks/ch76b_check.py` already validates that every cited section exists — the house tool I should
have used on ch72b this morning. Running the equivalent check against ch72b found a systematic
error in the chapter committed earlier today.

**Root cause: Chapter 25 is the Business Analyst track, not pandas. Pandas is Chapter 18.** Eleven
`Chapter 25, §25.x` pointers meant to send a reader to pandas sent them to BA material.

Also corrected: **§14.14 and §14.15 do not exist** (the cleaning log is §14.11; the CRM matching
rules are in Chapter 14's timed challenge, not a numbered section). Validation rules are §14.10 not
§14.12; reconciliation §14.11 not §14.13; duplicates §14.4 not §14.6; categories and mapping tables
§14.5 not §14.8; joining §14.8 not §14.10; units and currency §14.7 not §14.9. Outside Chapter 14:
grain is **§28.8** not §28.4; defining a metric is **Chapter 23, §23.13** not §10.6 ("Formulas and
cell references"); `TRIM` and time zones in SQL are **§12.8**; join types **§12.10** not §13.3; how a
cell stores a date **§10.3** not §11.4. Two pointers citing material the book does not contain
(§29.7 for blocking, §36.4 for outliers) were replaced with Chapter 14's own sections.

**62 pointer corrections in ch72b.** Every claim in both chapters now matches the real heading of
the section it names, checked mechanically.

## New: checks/ch72b_check.py

Chapter 72B argues that a cleaning figure is only trustworthy if something was run to produce it.
This applies that to the chapter itself: **116 assertions**, all passing, re-deriving every number
from the three companion files and then confirming the chapter quotes the result. It covers the row
accounting, the four date shapes and all four NaT counts, the ISO corruption under `dayfirst`, the
category funnels, the three gross totals and the `Rs. 1,400` → `0.14` trap, the key repair, the
carton factor of 10, Q72B-069's decomposition, and the four `answer_key.json` differences the
chapter documents. A future edit, or a pandas change that alters a behaviour, now fails here.

## Not done

- ~47 questions remain to reach ~1,160: ch75 (46) and ch80 (43) next, per the 3 October split.
- §70.9 is still the only unverified section in Part VIII (needs Excel).
- Cover and back cover still to design.
