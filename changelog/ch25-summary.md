# Chapter 25, The Business Analyst Track: summary

**Findings handled:** 18 content (25.1–25.18), 19 visual (V25.1–V25.19), and the Ch 25 part of three Reader's Journey rows (RJ-S3-23, RJ-S3-24, RJ-S2-7).
**Result:** 36 Verified (all content and visual rows except those below, checked in the rebuilt PDF or by the checks), 2 Open (25.18, RJ-S3-24), 1 Approved with the remaining work elsewhere (RJ-S2-7). RJ-S3-23's Ch 25 half is Verified.

## What changed

- **Consistency with Chapter 3 (25.1, High).** The chapter's worked gap analysis was built on a manual invoicing delay that Chapter 3 says does not exist. It now uses step 8, the delivery: paper proof of delivery, status changed by hand, no delivery date. The BR/FR examples, the gap figure, the ranking row and exercise 4 follow. The data backs it up: Riverstone's `orders` tables have a status but no delivery-date column.
- **Chapter 58 quoted correctly (25.3, High).** 88% straight through, and 19% of those loaded orders quietly wrong. Exercise and answer 15 are rebuilt on the right numbers.
- **One requirement register (25.2, V25.1).** BR-01 to BR-06, FR-01 to FR-17, NFR-01 to NFR-10; the figure and the text agree; BR-06 exists.
- **The at-risk rule, checked against the data (RJ-S3-23, 25.7).** FR-01 now points to Chapter 13 Pattern 6 and says why it uses 1.5× and writes down the four-order-day minimum. One new SQL cell runs both rules on the 24 key accounts. 2× flags two accounts, 1.5× adds Green Leaf Hotels, and 7 of the 24 are too new to judge. That count is why AC-3 now counts them separately.
- **First-time reader (25.4, 25.5, 25.6, 25.17).** QA/UAT, the ML words in the model spec, "data warehouse", "data product" and "baseline" are defined where they are first used.
- **Ranking you can reproduce (25.8).** A score formula with weights, and the re-ranking it produces (re-keying first, pointing to Chapter 58).
- **Small consistency fixes:** 25.9 to 25.15, plus two the tests forced (the wrong-dashboard example now uses the real ₹62,650 cancelled-order gap; the volume NFR uses the real 209,006 lines and 22% growth).
- **Figures (V25.2 to V25.6, V25.14 to V25.16).** Four figures redrawn at print width, with text at 7.1 to 9.0 pt, no in-figure titles, handoffs marked with an H badge as well as colour, and a 2 × 2 layout. The SDLC figure duplicated its table, so it is folded into the table as a "BA effort" column. Figures are renumbered 25.1 to 25.4.

## Skipped, and why

- **25.18 (Open):** Ch 25 now says "Sales Manager", like Ch 3, Ch 24 and the brief. The book-wide form ("Sales Manager (Key Accounts)" in Ch 3, 24, 25, 27) needs fact-sheet proposal C17 to be approved, and it touches other chapters.
- **RJ-S3-24 (Open):** Ayesha Qureshi. Option (a), adding her to the Riverstone bible, is fact-sheet proposal C42 (not approved) and is outside this chapter's files.
- **RJ-S2-7 (Approved, elsewhere):** Ch 25 already uses current file numbers and titles. The remaining work is the renumbering pass.
- **25.11:** I used the softer wording the finding offers. The alternative claim about orders 5004 and 9002 has no support in Chapter 3.

## Option picks

- 25.1: A (recommended).
- 25.2: BR-06 as written.
- 25.3: self-contained illustration with the Chapter 58 pointer ("better still").
- 25.8: score column.
- 25.15: 50 weeks.
- 25.16: keep the figures.
- V25.15: (a), keep one (the table).
- RJ-S3-23: keep 1.5× and explain the change.

## Time needed

It changes from 5–7 hours to **6–8 hours**, with two suggested sittings (25.1–25.5, then 25.6 to the end). This follows the content review's estimate for a first-timer, plus about 15 minutes for the new query.

## Code verification

- `verify_sql.py`: 1 statement run, 1 output checked, 0 mismatches (PostgreSQL, `riverstone_2025`).
- `checks/ch25_check.py` (new): 33 checks, all pass. It covers order 5001's dates and day counts, the missing delivery-date column, the volume figures, the ₹43,35,471 / ₹43,98,121 / ₹62,650 revenue figures, both at-risk rules, the what-if, the MySQL `DATEDIFF` variant (same rows), and all the chapter's arithmetic.
- `check_code_teaching.py` flags the one block as 36 lines long. This exception is deliberate: its first three steps are Chapter 13's Pattern 6, which is reused and explained in one bullet, and every new line is explained.
- Build: 32 pages. `layout_check`: map 18/18, no stranded headings or lead-ins, no sparse pages, no small text, no tofu. `draft_labels` hits are all reader text ("first draft", "for review by a named person").
