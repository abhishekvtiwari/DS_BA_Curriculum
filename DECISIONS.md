# Decisions — Abhishek fills this in

Edit this file on github.com (open it → pencil icon → edit → **Commit changes**). Works on a phone browser.
Claude Code reads this file before every fix session and copies your decisions into `tracker/register.csv`.

Allowed words in the **Decision** column: **Approve** · **Modify** (write what to do in Notes) · **Reject** · **Defer** (later edition).

> **Approved by Abhishek on 28 Sep 2026, in the Claude Code session ("This message is my approval").** This file records that message. Where it differs from the earlier draft, the message wins: no A3, V12 Modify (see its row), option picks strictly by "recommended, else (a)", reading order = `planning/chapter-map.md`, Reader's Journey rows approved.

## A. Global rule

Tick **A1 or A2** by putting an `x` in the brackets, like `- [x]`. Tick **A3** as well if you want it.

- [x] **A1.** Approve every finding as written, except themes or rows I mark below. *(fastest)*
- [ ] **A2.** Approve only the themes I mark Approve below; everything else waits for a row-by-row decision.
- [ ] **A3.** Also show me every **High** finding one by one before it is fixed (Claude Code lists them per part in the pull request for me to tick).

## B. Themes (one decision covers every matching row)

| # | Theme → fix | Decision | Notes |
|---|---|---|---|
| T1 | Code shown before it is taught (sequence rule) | Approve | Sequence rule is test 7; the book cannot teach beginners without it. Where the fix depends on reading order (Ch 12–20, 28–34), wait for the setup PR's reading-order answer. |
| T2 | Tools and libraries never installed → just-in-time install cell + first check in the chapter that first uses each | Approve | Already decided (just-in-time installs, CLAUDE.md §3). Install cells must be run for real in this environment, not typed. |
| T3 | Big code blocks with many new ideas → one new idea per cell, output shown, every line and argument explained | Approve | Core of the author's Jupyter-style teaching; one idea per cell with real output. |
| T4 | No by-hand example before the method → plain idea → tiny by-hand example → spreadsheet → code | Approve | Matches the book's own principle (idea → by hand → known tool → new tool). |
| T5 | Foundations the book never teaches (logs, chain rule, classes, YAML, regex…) → short primers where first needed | Approve | Keep primers short (half a page to a page) and place them where first needed; if a primer grows past ~2 pages, stop and list it in the part PR instead. |
| T6 | Hidden companion code / black-box outputs → every output comes from code shown on the page | Approve | Every printed output must come from code on the page; companion scripts stay as downloads, not as the only source of a result. |
| T7 | Printed outputs that are errors → re-run every chapter top to bottom, regenerate outputs | Approve | Re-running every chapter is needed anyway for T3/T6; outputs are pasted from real runs only. |
| T8 | Wrong chapter/section cross-references → one cross-reference pass from a generated index | Approve | Done in the final pass (CLAUDE.md §5.4) from a generated index, after all moves and any renumbering. |
| T9 | Part VIII pointers and numbering → renumber (see D2), every question points to a teaching section | Approve | Depends on D2; if D2 is rejected, only the pointer fixes apply, not the renumbering. |
| T10 | Riverstone facts that disagree → one Riverstone fact sheet (see D3) every chapter is checked against | Approve | Applied only after the Riverstone fact sheet (D3) is merged; each row is checked against it. |
| T11 | Drafting and authoring leftovers (Appendix G note, 'this chat', coordinator notes, build scripts named as reader files) → remove | Approve | Pure removals of drafting text; low risk, high polish value. |
| T12 | Time needed estimates too low → re-measure after fixes; recompute Ch 6, Ch 9, Ch 83 tables from one source | Approve | Re-estimated per chapter after its fixes; Ch 6, 9, 83 tables recomputed once, in the final pass. |
| T13 | Claims needing outside verification (prices, salaries, laws) → fact-check with dated sources | Approve | Only with a dated, citable source for each claim. Anything that cannot be verified stays Open with the reason in notes; nothing is invented (CLAUDE.md §8). |
| T14 | Integrity of examples and advice → label simulated results; interview advice uses only the reader's own work | Approve | Label simulated results as simulated; interview advice uses only the reader's own work. Protects the book's credibility. |
| V1 | Covers: remove draft/approval badges, versions and dates; one cover template | Approve | One clean cover template; also resolves V12.27-style title inconsistencies on covers. |
| V2 | Contents pages: add page numbers | Approve | Template change (pandoc TOC + page numbers); done once in the style pass. |
| V3 | Figure text ≥ 7 pt: redraw figures at print width | Approve | Figures redrawn from the 69 existing make_figs scripts at print width; text ≥ 7 pt. |
| V4 | Figures that contradict the text or overlap themselves: fix when redrawing | Approve | Fixed while redrawing (V3); each figure checked against caption and text. |
| V5 | Figures in number order | Approve | Renumber or reorder figures so they appear in number order; cross-refs updated with T8. |
| V6 | No colour-only meaning: add labels/shapes, check in greyscale | Approve | Add labels/shapes and check in greyscale; accessibility and print both need it. |
| V7 | Page breaks: split long code blocks, keep headings/lead-ins with what follows | Approve | CSS keep-with-next / split long code blocks; checked in the rebuilt PDFs with prescan.py. |
| V8 | Code lines: hard-wrap at ~80 characters with correct continuation, never soft-wrap | Approve | Hard-wrap code at ~80 characters with correct continuation, then re-run the code to prove it still works. |
| V9 | Two-digit list numbers clipped: widen list indent | Approve | One CSS change (wider list indent). |
| V10 | Tables: no-wrap for code/IDs, right-aligned numbers, keep short tables together, fix white-on-white headers | Approve | CSS for tables (no mid-token wraps, right-aligned numbers, keep short tables together, header contrast). |
| V11 | Rendering: escape $, render formulas properly, lint Markdown/HTML, font with ₹ | Approve | Escape $, render formulas, font with ₹; mostly build and CSS fixes. |
| V12 | Scale/resolution: Ch 19 at 100%, screenshots at 2×, rasters ≥ 300 ppi | Modify | Abhishek, 28 Sep: Claude Code does everything it can (Ch 19 rebuilt at 100%, every generated image re-exported at 300 ppi). The layout PR lists every screenshot Abhishek must retake (chapter, page, figure number, what it must show, required size) so they can be done in one sitting. |

## C. Structural decisions

| # | Question | Recommended | Decision | Notes |
|---|---|---|---|---|
| D1 | Book structure changes already approved (25 Sep): just-in-time tool setup, Ch 6 tool-free, Power BI (Ch 16) before Python, Ch 34 split (terminal essentials → Ch 26 §26.0), regression basics = new last section of Ch 22, Python in Ch 14/15 moves to Ch 18 | Already approved | Approve |  |
| D2 | Part VIII renumbering (72A→73 … 82→84, Closing → 85) and stable question codes (SQL-001, DSA-001…) — details in `review/content/ch72A.md`, row 72A.2 | Renumber + stable codes | Approve | Renumber 72A→73 … 82→84, Closing → 85, plus stable question codes (SQL-001…). Done last (final pass) so only one renumbering touches the book; stable codes make future moves safe. |
| D3 | Riverstone fact sheet: one timeline for Meera (Ch 1 vs Ch 83), one loaded hourly rate (₹300 or ₹1,200), one exchange rate, one warehouse story (DuckDB vs Postgres+Delta) | Claude Code drafts `review/riverstone-facts.md` for you to approve before Part II fixes | Approve | Abhishek, 28 Sep: Claude Code drafts `review/riverstone-facts.md` (people, timeline, hourly rate, exchange rate, systems, warehouse story, datasets, flash time) and checks every chapter against it. Abhishek approves it before Part II. |
| D4 | Order of work | Style fixes for the whole book first, then Part 0 → Closing, one pull request per part | Approve | Style fixes are shared (template/CSS), so doing them once first avoids re-doing every part. Riverstone fact sheet PR before Part II content. |
| D5 | Output format of fixed chapters | Same format as your current sources, rebuilt to PDF | Approve | Keep Markdown + the existing pandoc/Chromium pipeline; the setup PR shows it rebuilds Ch 12 identical to the reviewed v4. |
| D6 | Chapter 6 structure: study-guide material must come before Chapter 1 | Abhishek's decision, 28 Sep | Approve | New unnumbered front section "How to Use This Book" before Chapter 1 (4–6 pp: chapter anatomy from old §6.9, reading code cells and outputs, the four exercise groups and answers, how the parts climb, rough time pointing to Ch 6, companion files). Chapter 6 keeps its number, renamed "Planning Your Learning" (honest hours table, weekly rhythm, tool timeline with no installs, AI assistants, reading documentation, project: plan your route and first 90 days). No renumbering. Also update the Part 0 contents, Ch 5 "Where this leads", Ch 9's references to Ch 6, and the Part 0/I fix instructions. Done in the Part 0 + I build. |
| D7 | Working mode | Abhishek's decision, 28 Sep | Approve | One part at a time, end to end, no check-ins mid-part; one package per part (single part PDF in `fixed/Part-X/`, one-page summary per chapter, one PR). Layout pass (V1–V12) and Riverstone fact sheet first. Order: Part 0 + I together, then II … VIII, Closing. Written into `CLAUDE.md` §5 and §7. |
| D8 | How the book is divided and named | Abhishek's decision, 28 Sep ("the division of the sections is also important") | Approve | **Chapters in six stages:** Start (Why this matters, In plain English) · Learn (numbered sections) · Apply (Common mistakes, In the real world, Project, with *Tools you'll need* folded in) · Review (Recap, Key terms, Check yourself) · Practise (Exercises, Answers) · Next (Where this leads). Each stage's first heading carries a label. Renamed: "Common mistakes and how to spot them" → "Common mistakes", "The project: …" → "Project: …", "You've got it when…" → "Check yourself", "Practice exercises" → "Exercises", "Answers to practice exercises" → "Answers". **Parts numbered 0 to 8** in reader text (Part II → Part 2, …). **Navigation:** a map of the stages and numbered sections with page numbers under each chapter's "Chapter at a glance"; two-level contents (chapters and numbered sections); one page count per package (front matter i, ii …, then 1, 2 … from Part 0). Not chosen: dropping the full stop in "Chapter 1." titles. Tools: `tools/restructure.py`, `tools/part_numerals.py`, `tools/pdf/build.py`. |

## D. Rows where you must pick an option

These 34 findings offer options (a)/(b). **If you leave a row blank, Claude Code uses the option the finding marks as recommended (or option (a) if none) and says so in the change log.**

| Finding | Ch | The question | Your choice | Notes |
|---|---|---|---|---|
| V12.27 | 12 | The cover says "Chapter 12" with no full stop; the p. 3 heading and contents say "Chapter 12.". | "Chapter 12." with the full stop, everywhere | Matches the H1 of all 85 manuscript files and the contents; only the cover template changes (V1). |
| 14.15 | 14 | Contradicts the table just above it: product 105 (Industrial Crate; ₹1,400 in §14.11 step 9) had a pre-Q4… | (a) | No option is marked recommended, so (a) per the rule: name a product whose history reaches 85–90, and make the overall-vs-per-product rule explicit. |
| 16.5 | 16 | The reader is never told how to build Sales. Raw tables are imported; the text then says "use the view idea"… | Recommended: import the sales_lines view as Sales | One path with every click; reuses the Ch 13 view the reader already built. Keep the CSV route as the alternative the finding describes. |
| 17.30 | 17 | This contradicts itself twice. A duplicate of a ~400-row file would have ~400 rows, not 1,900, and the… | The finding's version (412-row duplicate, ₹1.4 crore) | Only story that is internally consistent; change both sentences. |
| 18.23 | 18 | The fact that bins include the right edge (25,000 is "medium", 50,000 is "large") is not stated. Ch 19's VBA… | right=False, Ch 16, 18, 19 agree | Matches "≥ 50,000 is very large" and Ch 19's VBA; counts recomputed by code. |
| 19.8 | 19 | The VBA editor is ANSI and can't hold "₹". It turns into "?" when typed or imported from a .bas file, so the… | ChrW(8377) & Format(...); Indian lakh grouping | The fix is the only one offered. Grouping follows 67.9's recommendation (Indian lakh grouping book-wide), for consistency. |
| 22.9 | 22 | Inconsistent and untested. (a) §22.3 says the email test "should have named revenue per recipient if the goal… | Option A (open rate is primary) | Keeps the recommendation and the chapter's logic; no new statistics needed at this point. |
| 23.8 | 23 | Inconsistent with the chapter's own figures. §23.4 says receivables rose by only ₹45.9 lakh. Opening… | (a) | Changes less (the finding says so); adds a small quarterly table computed by code; §23.4's cash-flow numbers stay intact. |
| 24.5 | 24 | The requester is inconsistent: the worked arc and memo say Anita asked; the real-world story says Vikram… | Vikram raises the ask; memo to Vikram, cc Anita | Matches Ch 3 roles (Vikram = Sales Manager, Anita = Sales Head, decision-maker). |
| 25.1 | 25 | Contradicts Chapter 3, which the chapter promises to follow exactly ("Every figure and date here is the one… | (A) | Keeps Ch 3, whose figures are reused in Ch 12–13; moves the gap analysis to the genuinely manual step 8 (POD). |
| 29.16 | 29 | config.py reads only os.environ, and nothing in the package loads .env. A reader who follows the advice and… | (a) uv run --env-file .env | Ch 29 already uses uv; one flag, no new dependency, nothing written into library code. |
| 39.1 | 39 | No hyperparameter tuning anywhere in the chapter: no GridSearchCV or RandomizedSearchCV, no… | (b) add §39.6a "Tuning honestly" | The chapter title promises tuning; recommended by the finding; no retitle ripple through Ch 36/37/44/74. |
| 40.34 | 40 | This is false. Ch 48 uses "25 machines across two plants, one reading every 10 seconds from 1 October to 31… | (a) | Fixes the false claim in Ch 40 only; Ch 48 is left alone. |
| 47.1 | 47 | freshness_check turns a DATE into midnight (datetime.combine(newest, datetime.min.time())). So yesterday's… | (A) business days | Recommended; also fixes the weekend problem (47.2). |
| 51.5 | 51 | The placeholder is labelled, but it measures the wrong thing, and the "overdue-payment" name survives… | (A) rename to "follow-up due" | Honest, no new data to invent; option B would need a payments table the book has never had. |
| 52.22 | 52 | The role can only be assumed by ECS tasks. The chapter deploys to Kubernetes (§52.3, and CI's kubectl), which… | ECS Fargate throughout | Follows §52.8's own recommendation; the trust policy is already correct for it. |
| 56.2 | 56 | Contradiction. In Ch 53, 97.5% recall is the 0.01 threshold, but the packaged defect_v1 has threshold 0.1 and… | Recommended: plant manager chose 0.1 (95%) | No re-runs needed; one explanatory sentence in 56.3. |
| 56.16 | 56 | Three vs four layers. The figure has four rows, the (broken) table has three with output and outcome merged,… | Keep three layers, third has two streams | Matches the text, glance, recap and "You've got it"; only the figure changes. |
| V57.9 | 57 | Prose uses ₹ (₹4.74, ₹1,000, ₹0.08), while figures and code output use "Rs" (Fig 57.2 "Rs 23.62"; outputs "Rs… | ₹ in figures and in printed code output | No option is marked, so (a) per the rule: one convention (₹) for printed output and figures. Code is changed to print ₹ and re-run. |
| V58.9 | 58 | Prose uses ₹ (₹100,000, ₹13,380), while figures and code output use "Rs" (Fig 58.1 "over Rs 100,000"; Fig… | ₹ in figures | No option is marked; (a) per the rule, and the same convention as V57.9. |
| 59.1 | 59 | Only Cases 1 and 9 are Riverstone's. Case 7 is "Customer support automation at a subscription business … A… | (A) | Keeps the honest composite label; no numbers are invented or re-measured. (B) would be a larger rewrite. |
| 59.12 | 59 | Every other chapter has exercises; this one tells the reader to spend an afternoon on a mapping it never… | Add the Practice section as specified | The only option given; every other chapter has exercises. |
| 60.3 | 60 | Three different Flash timings in the book. Ch 20: Flash at 07:30 IST, after an overnight ERP load (L559,… | Flash by 07:30 IST after the 06:30 Dagster run | Suggested by the finding; matches Ch 20 and Ch 46; Ch 61 becomes "as of 06:35". |
| 63.1 | 63 | The duplicate count contradicts itself in five places. Figure: 4. §63.8 text: two branches, near-identical… | Option A (two pairs, keep 4) | Totals stay 24, so no ripple into the other categories or figures. |
| 66.3 | 66 | Contradiction. §66.2 scores Governance & security 3.4, second-highest; the weakest are Data-driven culture… | (a) split the governance dimension | Keeps the governance/catalog hire and Ch 67's story; only the scorecard gains a row. |
| 66.5 | 66 | Ch 20 gives only 325 hours/yr, and Ch 63's ROI table values the same saving at ~₹3.9 lakh (₹1,200/hr loaded… | ₹300/hour loaded rate, book-wide | Keeps Ch 66's "45%" story and Ch 67's board speech; only Ch 63's "~₹3.9 lakh" changes to "~₹97,500". Recorded in the fact sheet (D3). |
| 67.9 | 67 | Inherits Ch 66's numbers, which depend on the unresolved hourly-rate conflict with Ch 63 (Ch 66 review 66.5:… | Follow 66.5 (₹300); Indian lakh grouping (₹2,03,775) book-wide | Recommended by the finding: "Indian lakh grouping suits an Indian audience". See the question in the setup PR about the scale of this change. |
| V67.7 | 67 | "₹2,03,775" and "₹4,56,168" use Indian lakh grouping. The same numbers print as "₹203,775" and "₹456,168" in… | Indian lakh grouping book-wide | No option is marked; follows 67.9's recommendation so the book has one convention. |
| 72.3 | 72 | These need material the book never teaches (0 hits in Ch 17/18/29/33): mutable default arguments, shallow vs… | (a) teach each topic in Ch 17/18/29 | Option (a) per the rule. |
| 73.4 | 73 | Never taught anywhere in the book (0 mentions in Ch 21/22/30/31 or elsewhere). "Learn it in: Chapter 21 or… | (a) box in Ch 21 | Recommended; Ch 21's complement rule is the exact tool the birthday problem needs. |
| 76B.11 | 76B | These are asked but never taught. Ch 25 §25.8 teaches Given/When/Then without the name "Gherkin"; Ch 26… | (a) teach in Ch 24/25/26 | Recommended; three short additions cover all six terms. |
| 80.2 | 80 | Contradicts the book. By Ch 60 §60.5 ("by early 2026, Riverstone has built a warehouse and orchestrator (Part… | (a) reframe as history | Keeps the model answer, adds a self-check against Ch 60; recommended. |
| 82.28 | 82 | Mixed units in one chapter (lakh vs million), and the summaries use both. | "₹22.98 lakh" (lakh, spelled out) | Suits a sales-leadership memo; no bare "L". |
| 83.1 | 83 | Contradicts Part 0: Ch 1 says Meera "has just joined Riverstone Supplies as a sales coordinator", and by Ch… | Recommended: Ch 1 timeline (just joined as sales coordinator) | Part 0 is approved; Ch 83 adapts, and Ch 8 §8.8 / Ch 68 / Ch 81 are aligned. Recorded in the fact sheet (D3). |

## E. Exceptions (optional)

List any single finding you want handled differently from its theme:

| Finding | Decision | Notes |
|---|---|---|
| RJ-* (Reader's Journey rows) | Approve | Abhishek, 28 Sep. The 64 new RJ rows are approved; the 66 duplicates are recorded against their originals and not added twice. |
| Reading order | chapter-map.md, with D1 kept | Abhishek, 28 Sep: follow `planning/chapter-map.md`, but keep D1 and the move of Python out of Ch 14/15 ("d1 keep them"). Part II: 10, 11, 19, 12, 13, 14, 15, 16, 17, 18, 20–27. Part III: 28, 34, 29, 32, 33, 30, 31. Findings that assume another order stay `Open`. |
| Renumbering Parts II and III | Approve | Abhishek, 28 Sep ("Renumbering yes"): chapter numbers follow the reading order. Done in the final pass with D2 and the cross-reference pass; map in `CLAUDE.md` §3. |
| Any finding that assumes the sequence-map order | Open (held) | Listed in `review/reading-order-conflicts.md` and in the setup PR. |
