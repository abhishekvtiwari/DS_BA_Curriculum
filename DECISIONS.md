# Decisions — Abhishek fills this in

Edit this file on github.com (open it → pencil icon → edit → **Commit changes**). Works on a phone browser.
Claude Code reads this file before every fix session and copies your decisions into `tracker/register.csv`.

Allowed words in the **Decision** column: **Approve** · **Modify** (write what to do in Notes) · **Reject** · **Defer** (later edition).

## A. Global rule

Tick **A1 or A2** by putting an `x` in the brackets, like `- [x]`. Tick **A3** as well if you want it.

- [ ] **A1.** Approve every finding as written, except themes or rows I mark below. *(fastest)*
- [ ] **A2.** Approve only the themes I mark Approve below; everything else waits for a row-by-row decision.
- [ ] **A3.** Also show me every **High** finding one by one before it is fixed (Claude Code lists them per part in the pull request for me to tick).

## B. Themes (one decision covers every matching row)

| # | Theme → fix | Decision | Notes |
|---|---|---|---|
| T1 | Code shown before it is taught (sequence rule) |  |  |
| T2 | Tools and libraries never installed → just-in-time install cell + first check in the chapter that first uses each |  |  |
| T3 | Big code blocks with many new ideas → one new idea per cell, output shown, every line and argument explained |  |  |
| T4 | No by-hand example before the method → plain idea → tiny by-hand example → spreadsheet → code |  |  |
| T5 | Foundations the book never teaches (logs, chain rule, classes, YAML, regex…) → short primers where first needed |  |  |
| T6 | Hidden companion code / black-box outputs → every output comes from code shown on the page |  |  |
| T7 | Printed outputs that are errors → re-run every chapter top to bottom, regenerate outputs |  |  |
| T8 | Wrong chapter/section cross-references → one cross-reference pass from a generated index |  |  |
| T9 | Part VIII pointers and numbering → renumber (see D2), every question points to a teaching section |  |  |
| T10 | Riverstone facts that disagree → one Riverstone fact sheet (see D3) every chapter is checked against |  |  |
| T11 | Drafting and authoring leftovers (Appendix G note, 'this chat', coordinator notes, build scripts named as reader files) → remove |  |  |
| T12 | Time needed estimates too low → re-measure after fixes; recompute Ch 6, Ch 9, Ch 83 tables from one source |  |  |
| T13 | Claims needing outside verification (prices, salaries, laws) → fact-check with dated sources |  |  |
| T14 | Integrity of examples and advice → label simulated results; interview advice uses only the reader's own work |  |  |
| V1 | Covers: remove draft/approval badges, versions and dates; one cover template |  |  |
| V2 | Contents pages: add page numbers |  |  |
| V3 | Figure text ≥ 7 pt: redraw figures at print width |  |  |
| V4 | Figures that contradict the text or overlap themselves: fix when redrawing |  |  |
| V5 | Figures in number order |  |  |
| V6 | No colour-only meaning: add labels/shapes, check in greyscale |  |  |
| V7 | Page breaks: split long code blocks, keep headings/lead-ins with what follows |  |  |
| V8 | Code lines: hard-wrap at ~80 characters with correct continuation, never soft-wrap |  |  |
| V9 | Two-digit list numbers clipped: widen list indent |  |  |
| V10 | Tables: no-wrap for code/IDs, right-aligned numbers, keep short tables together, fix white-on-white headers |  |  |
| V11 | Rendering: escape $, render formulas properly, lint Markdown/HTML, font with ₹ |  |  |
| V12 | Scale/resolution: Ch 19 at 100%, screenshots at 2×, rasters ≥ 300 ppi |  |  |

## C. Structural decisions

| # | Question | Recommended | Decision | Notes |
|---|---|---|---|---|
| D1 | Book structure changes already approved (25 Sep): just-in-time tool setup, Ch 6 tool-free, Power BI (Ch 16) before Python, Ch 34 split (terminal essentials → Ch 26 §26.0), regression basics = new last section of Ch 22, Python in Ch 14/15 moves to Ch 18 | Already approved | Approve |  |
| D2 | Part VIII renumbering (72A→73 … 82→84, Closing → 85) and stable question codes (SQL-001, DSA-001…) — details in `review/content/ch72A.md`, row 72A.2 | Renumber + stable codes |  |  |
| D3 | Riverstone fact sheet: one timeline for Meera (Ch 1 vs Ch 83), one loaded hourly rate (₹300 or ₹1,200), one exchange rate, one warehouse story (DuckDB vs Postgres+Delta) | Claude Code drafts `review/riverstone-facts.md` for you to approve before Part II fixes |  |  |
| D4 | Order of work | Style fixes for the whole book first, then Part 0 → Closing, one pull request per part |  |  |
| D5 | Output format of fixed chapters | Same format as your current sources, rebuilt to PDF |  |  |

## D. Rows where you must pick an option

These 34 findings offer options (a)/(b). **If you leave a row blank, Claude Code uses the option the finding marks as recommended (or option (a) if none) and says so in the change log.**

| Finding | Ch | The question | Your choice | Notes |
|---|---|---|---|---|
| V12.27 | 12 | The cover says "Chapter 12" with no full stop; the p. 3 heading and contents say "Chapter 12.". |  |  |
| 14.15 | 14 | Contradicts the table just above it: product 105 (Industrial Crate; ₹1,400 in §14.11 step 9) had a pre-Q4… |  |  |
| 16.5 | 16 | The reader is never told how to build Sales. Raw tables are imported; the text then says "use the view idea"… |  |  |
| 17.30 | 17 | This contradicts itself twice. A duplicate of a ~400-row file would have ~400 rows, not 1,900, and the… |  |  |
| 18.23 | 18 | The fact that bins include the right edge (25,000 is "medium", 50,000 is "large") is not stated. Ch 19's VBA… |  |  |
| 19.8 | 19 | The VBA editor is ANSI and can't hold "₹". It turns into "?" when typed or imported from a .bas file, so the… |  |  |
| 22.9 | 22 | Inconsistent and untested. (a) §22.3 says the email test "should have named revenue per recipient if the goal… |  |  |
| 23.8 | 23 | Inconsistent with the chapter's own figures. §23.4 says receivables rose by only ₹45.9 lakh. Opening… |  |  |
| 24.5 | 24 | The requester is inconsistent: the worked arc and memo say Anita asked; the real-world story says Vikram… |  |  |
| 25.1 | 25 | Contradicts Chapter 3, which the chapter promises to follow exactly ("Every figure and date here is the one… |  |  |
| 29.16 | 29 | config.py reads only os.environ, and nothing in the package loads .env. A reader who follows the advice and… |  |  |
| 39.1 | 39 | No hyperparameter tuning anywhere in the chapter: no GridSearchCV or RandomizedSearchCV, no… |  |  |
| 40.34 | 40 | This is false. Ch 48 uses "25 machines across two plants, one reading every 10 seconds from 1 October to 31… |  |  |
| 47.1 | 47 | freshness_check turns a DATE into midnight (datetime.combine(newest, datetime.min.time())). So yesterday's… |  |  |
| 51.5 | 51 | The placeholder is labelled, but it measures the wrong thing, and the "overdue-payment" name survives… |  |  |
| 52.22 | 52 | The role can only be assumed by ECS tasks. The chapter deploys to Kubernetes (§52.3, and CI's kubectl), which… |  |  |
| 56.2 | 56 | Contradiction. In Ch 53, 97.5% recall is the 0.01 threshold, but the packaged defect_v1 has threshold 0.1 and… |  |  |
| 56.16 | 56 | Three vs four layers. The figure has four rows, the (broken) table has three with output and outcome merged,… |  |  |
| V57.9 | 57 | Prose uses ₹ (₹4.74, ₹1,000, ₹0.08), while figures and code output use "Rs" (Fig 57.2 "Rs 23.62"; outputs "Rs… |  |  |
| V58.9 | 58 | Prose uses ₹ (₹100,000, ₹13,380), while figures and code output use "Rs" (Fig 58.1 "over Rs 100,000"; Fig… |  |  |
| 59.1 | 59 | Only Cases 1 and 9 are Riverstone's. Case 7 is "Customer support automation at a subscription business … A… |  |  |
| 59.12 | 59 | Every other chapter has exercises; this one tells the reader to spend an afternoon on a mapping it never… |  |  |
| 60.3 | 60 | Three different Flash timings in the book. Ch 20: Flash at 07:30 IST, after an overnight ERP load (L559,… |  |  |
| 63.1 | 63 | The duplicate count contradicts itself in five places. Figure: 4. §63.8 text: two branches, near-identical… |  |  |
| 66.3 | 66 | Contradiction. §66.2 scores Governance & security 3.4, second-highest; the weakest are Data-driven culture… |  |  |
| 66.5 | 66 | Ch 20 gives only 325 hours/yr, and Ch 63's ROI table values the same saving at ~₹3.9 lakh (₹1,200/hr loaded… |  |  |
| 67.9 | 67 | Inherits Ch 66's numbers, which depend on the unresolved hourly-rate conflict with Ch 63 (Ch 66 review 66.5:… |  |  |
| V67.7 | 67 | "₹2,03,775" and "₹4,56,168" use Indian lakh grouping. The same numbers print as "₹203,775" and "₹456,168" in… |  |  |
| 72.3 | 72 | These need material the book never teaches (0 hits in Ch 17/18/29/33): mutable default arguments, shallow vs… |  |  |
| 73.4 | 73 | Never taught anywhere in the book (0 mentions in Ch 21/22/30/31 or elsewhere). "Learn it in: Chapter 21 or… |  |  |
| 76B.11 | 76B | These are asked but never taught. Ch 25 §25.8 teaches Given/When/Then without the name "Gherkin"; Ch 26… |  |  |
| 80.2 | 80 | Contradicts the book. By Ch 60 §60.5 ("by early 2026, Riverstone has built a warehouse and orchestrator (Part… |  |  |
| 82.28 | 82 | Mixed units in one chapter (lakh vs million), and the summaries use both. |  |  |
| 83.1 | 83 | Contradicts Part 0: Ch 1 says Meera "has just joined Riverstone Supplies as a sales coordinator", and by Ch… |  |  |

## E. Exceptions (optional)

List any single finding you want handled differently from its theme:

| Finding | Decision | Notes |
|---|---|---|
|  |  |  |
