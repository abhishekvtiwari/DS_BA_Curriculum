# Chapter 60, Designing Whole Systems: summary

**Findings:** 44 rows (27 content, 13 visual, RJ-S2-25, RJ-S2-26, RJ-S3-68, RJ-S3-71). All applied to Ch 60; none left Open. Two multi-chapter rows (RJ-S2-26, RJ-S3-71) have their Ch 60 part done and stay Approved for the other chapters. 8 visual rows done by the style pass were re-checked in the rebuilt PDF.

## What changed
- **Consistent with Parts 5 and 6 as they now stand.** One timeline: PO intake runs at 06:00 on weekdays (Ch 57/58), the Dagster run at 06:30 (Ch 46), the Flash is sent by 07:30 IST after its four checks (Ch 20); freshness is "previous working day" (Ch 47 §47.5). The warehouse is described as Part 5 built it (raw, staging and mart tables plus the Delta sensor archive), without naming a production engine. The PO-intake NFR now matches assisted mode (a named person confirms every order; over ₹1,00,000 also approved). The ADR index, the story and the companion ADRs match Ch 47, 51, 55 and 58 (segment sync's PUT, absolute floors plus document status, Ch 58's final cost comparison).
- **Numbers computed, not typed.** New subsection "Reading a p95" (Ch 21's rule by hand, then pandas: 19.2 min; a what-if with p95 38.2 vs average 16.2). Availability worked by hand (525,600 min, 8.76 h) and printed by a short cell for four levels; reliability rewritten as a count (1 ÷ 30 = 3.3%; 365 × 0.005 = 1.8 → "at most 2 runs a year"). `checks/ch60_check.py` recomputes every stated number.
- **Figures redrawn** (680 px canvas, measured wrapping, ≥ 7.62 pt): C4 levels; context diagram with names under icons and every arrow crossing the platform edge; container diagram with numbered arrows 1–6 matching the §60.5 trace, AI/data tags, outside systems greyed; NFR figure; the ADR with its alternatives on separate lines. Files renamed so `fig60-4` is Figure 60.4 and `fig60-5` is Figure 60.5.
- **First-time reader:** concrete Before-you-start list; one-clause glosses with chapter pointers (FastAPI, RAG, UML, time travel, system of record, idempotency key, reconciliation, polling, shadow mode, greenfield, on-call, SLA); resume-driven design and big-bang rewrite defined in prose; "three AI and five data containers".
- **Story:** date- and tenure-neutral ("the January after the PO-intake pilot went live"), the managing director Arvind Kapoor creates the role on Anita Rao's recommendation, ADR-026 records Ch 51's rule, two CRM writers with different retry logic, the defect model migrated first because it is lower-risk; "twenty-six ADRs".
- **Polish:** ADR has seven parts (Nygard adapted); "Zoho" removed (Riverstone's CRM is never named in the book); Appendix G note removed; interview pointer → Ch 80 and Ch 77; Ch 65 added to Where this leads.
- **Companion** (`companion/ch60/`): design document, five ADRs, template and worksheet rewritten to match (no Postgres, no 2 h freshness, no 06:10 Flash, no invented dates; ADR-021 now quotes Ch 58's final numbers).

## Option picks
60.2 (a) honest to Part 5 · 60.5 count · 60.10 first option (two CRM writers) · 60.18 (a) add a seventh part · 60.13 the 06:00 run (Ch 57/58's fact) instead of the finding's "every 5 minutes" · 60.12 fallback = the QC inspector (Ch 53/56), not Ch 61's figure.

## Skipped or held
Nothing skipped. Held on open decisions, with engine- and calendar-neutral wording in the meantime: the production warehouse engine (60.1; fact sheet §4) and printing a year for Part 7 (RJ-S2-25/26, 60.8; fact sheet P-T1/P-T2). See `questions-ch60.md`.

## Time needed
12–15 hours over two weeks, **unchanged**: the additions (a p95 subsection with two short cells, one availability cell, a few glosses) add about half an hour of reading to roughly 3 hours; the project (8–10 hours) is the same.

## Verification
verify_python: 3 blocks, 3 outputs, **0 mismatches**; verify_shell: nothing to run; check_code_teaching: 3 blocks, 0 flagged; `checks/ch60_check.py`: all pass; fig_check: 0 figures under 7 pt (min 7.62); restructure: "already in order"; build 26 pages; layout_check: map 12/12, toc_wrong none, no stranded heads/lead-ins, no sparse pages, no small text, tofu 0 (draft_labels are reader text: "drafting the proposal", "draft order", "sales coordinator"). Pages with visual findings rendered and checked.
