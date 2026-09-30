# Chapter 80, Architecture & Leadership Question Bank: summary

**Findings:** 21 content (80.1–80.21) and 10 visual (V80.1–V80.10). All 31 applied and checked in the rebuilt PDF (16 pages) or by a verifier; none left Open. Detail: `changelog/ch80.md`.

## What changed
- **Drafting leftovers gone (80.1, V80.1, V80.2).** The "this chat doesn't have their approved text" paragraph and "Included on direct request" are deleted. Every **Learn it in** pointer now names a section, checked against the current headings of Ch 20, 23, 24, 39, 47, 49, 51, 60–67 by `checks/ch80_check.py`. Part 7's rebuild is reflected: CAP/CP/AP §61.2, PACELC §61.3, scaling up/out and quorum/consensus/leader election §61.5, the warehouse as the one true SPOF §61.7, Lambda/Kappa §62.2, mesh readiness §62.6, the ROI table §63.2, the inventory §63.8, fairness audit §64.7, showback §65.4, build vs buy §66.5, board/influencing/saying no/first 90 days §67.3–67.6, and Ch 39's renumbered §39.9 (fairness).
- **The design case no longer contradicts the book (80.2, 80.3).** Q80-022 is now set in the Riverstone of Parts 2 and 3 (the ERP's PostgreSQL database, Part 2's reports, Ch 20's scripted Flash), with no date. A new "Check your roadmap against what happened" paragraph sends the reader to Ch 60 §60.5's design document and ADR index. The warehouse engine isn't named.
- **Code taught like Jupyter, with real output (80.7–80.10, V80.6).** Q80-016 is now three cells, each with its real printed output (verify_python: 3 blocks, 3 outputs, 0 mismatches), a line-by-line "How it works", a predict prompt and a what-if (maintenance). It uses the book's ₹300/hour and prints ₹, not "Rs". Payback is defined and pointed to Ch 23 §23.9, where the book already teaches it.
- **New §80.2 Basic-but-tricky (80.19).** Core Q80-024 (nightly backups: still a SPOF?). Rapid-fire rows: Q80-025 (eventual consistency a bug?), Q80-026 (PACELC, the optional question from Ch 61's row 61.16), Q80-027 (partitioning vs sharding) and Q80-029 (a second copy always helps?). Q80-028 (is Kappa always simpler?) sits beside Lambda/Kappa in §80.3. Every question now carries **Level** (Mid/Senior) and **Roles** (DE, DS, ARC, LEAD), and the key says which roles are senior-IC and which are architect/lead.
- **Bank format.** There's a Chapter-at-a-glance box with Before you start and **Time needed** (80.18). Ch 69's twelve `**[+Tag]**` tags are used throughout, with the "[Learn it in]" pseudo-tags replaced by real moves. The rapid-fire tables have a "Level · learn it in" column. IC, TCO, durability and availability are defined where first used.
- **Smaller fixes.** ATM edge case on CAP (80.21). Replication lag on leader-follower (80.6). The story's Vikram is renamed Siddharth, with a plain timeline (80.16). Tools points to Ch 10–11 (80.17). Where this leads now says "Chapters 60–67" and points to Ch 81 (80.12, 80.20).

## Option picks
- 80.2: **(a)** reframe as history (DECISIONS D), without the finding's "early 2025" because the book calendar isn't decided.
- 80.5: **(a)** the box in Ch 61. Ch 61 had already added "Scaling up and scaling out" (row 61.15), so only the pointer changed here.
- 80.8: **(a)** use the book's loaded rate, at its current value of ₹300 (the finding's ₹1,200 predates the Ch 20 change).
- 80.19: **(a)** a Basic-but-tricky section, plus the level/role labels the bank format now uses.
- 80.4: the optional Strong-tier line taken. "TCO in Ch 67 §67.5" isn't in Ch 67 (no chapter teaches TCO), so TCO is defined in the answer.
- 80.16: "Siddharth", not the suggested "Rohan", which Ch 8 and Ch 68 already use.

## Skipped or left
- Nothing left Open.
- One layout fault remains, and it's the builder's: on p. 11 the "Rapid-fire, 80.5" heading and its Roles line end the page, and the table starts on p. 12. A fix for `layout.js` is proposed in questions-ch80.md.

## Numbers and code
- Q80-016: 3 × 52 × ₹300 = ₹46,800 a year. Payback on ₹60,000 = 15.4 months. Net of 2 h/month maintenance: ₹39,600 and 18.2 months. Over three years: ₹1,18,800 saved, a ₹58,800 gain.
- The story's 1 + 14 = 15 still holds.
- All numbers are recomputed by `checks/ch80_check.py` (ALL OK).
- Verifiers: verify_python 3/3, 0 mismatches. check_code_teaching 0 findings. restructure --check "already in order". fig_check: no figures.
- layout_check: map 9/9, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0. The only draft label is "Draft" in project step 3, which is reader text.

## Time needed
Now stated: **2–3 hours to read and drill once, plus 2–3 hours for the project** (none before). The chapter grew from 12 to 16 PDF pages: six new questions and the three ROI cells.
