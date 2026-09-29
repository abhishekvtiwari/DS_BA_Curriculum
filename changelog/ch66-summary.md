# Chapter 66 summary: Data Strategy, Maturity & Building Data Teams

**Rows:** 37 handled: 34 Verified (26 content, 8 visual, plus the Ch 66 parts of RJ-S3-68 and RJ-S3-75) and 3 left Open (66.16, 66.20, RJ-S3-77). V66.7–9 and V66.11 were already Verified by the style pass.

## What changed
- **The business case is fixed and honest.** The IndexError is gone. `roi_case.csv` now holds only raw inputs (platform cost, three savings, the hire's salary), each with an `item_id`, a `kind` (cost / measured / conditional) and a source. Every total is worked out in short, explained cells.
- **The numbers now agree with Ch 19, 20, 58, 63 and 65.**
  - Platform ₹37,780 a month = ₹4,53,360 a year (Ch 65, read from its CSV).
  - Flash ₹97,500 (325 h × ₹300).
  - Macro ₹77: 4 quarterly runs × 231 s. This was ₹5,775 from an unstated 300 runs.
  - PO intake ₹1,00,750, labour only, and it counts only if reviewers catch at least 97% of wrong drafts. At a 90% catch rate it is −₹2,32,500 (Ch 63).
  - New headline: **measured savings cover 22%; with PO intake, 44%** (it was 45%).
- **The hire is weighed against its salary.** ₹9,00,000 is set against a clearly labelled estimate of the time people lose finding data (₹3.00 lakh, 33%). The case names the rest of the value it can't price and says how the estimate will be measured.
- **The maturity model has a rule.** The scoring rule is written down (five criteria per stage; score = stage fully met + one-fifth per next-stage criterion met), with one row worked by hand. Governance is split, as option (a) asks: Security & access scores 3.8 and Catalog & discoverability 1.8, the weakest. The strategy (§66.1), the hire (§66.4), the build-vs-buy example (§66.5), the recap and the answers now all point at the same gap. There is also a note that CMMI and DAMA name their stages differently.
- **Cross-references fixed:**
  - Conway's Law is §62.8.
  - The duplicated macros come from Ch 63's audit.
  - The fairness audit is Ch 64's.
  - "Numbers, not adjectives" is Ch 60 §60.3.
  - "Fit over fashion" is reworded to what Ch 62 actually says.
  - Ch 63 now says 17 of 24 automations were ungoverned.
  - The nine-year macro is described as Ch 63 describes it.
  - Anita Rao is named "as Sales Head".
  - The Taloja rerun scored 12 of 25 (one plant data product, not a mesh).
  - Meera is Head of Data Platform.
- **Figures** are renumbered in reading order (66.1 maturity, 66.2 ROI, 66.3 team, 66.4 build vs buy) and all redrawn: text at 7.6 pt or more, shapes and words alongside colour, ₹ with a lakh axis, and the Fit row reading "Build (eventually)".
- **Polish:**
  - The Appendix G note and the "run here on Python 3.12" wording are gone.
  - CFO and ROI are defined where first used; "table stakes" is replaced.
  - The story's CFO is now Suresh Menon, the Finance Manager.
  - Answer 13 shows the 37.5 ≈ 38 misses.

## Skipped and why
- **66.16** (numbers for build vs buy): a vendor's catalog price is a T13 fact. Vendor pricing pages are blocked by the proxy, and converting to ₹ needs the unapproved exchange rate. Left Open.
- **66.20 / RJ-S3-77** (one dated timeline): needs the book calendar (P-T2), which is not approved. The undated "Nine months later" jump and the "2026" label in the figure were removed. Left Open.
- **66.18:** the chart is rendered, but its matplotlib code is not printed in the chapter (optional in the finding).

## Option picks
66.3 option (a); 66.4 measured floor plus named ceiling (the finding's first option); 66.5 keep ₹300/hour (the book-wide rate).

## Time needed
Was 8–10 hours; now **9–11 hours over a week**. The chapter gained about an hour of reading: seven more short code cells (8 in all, up from 2), the scoring rubric and the hire's case.

## Verification
- `verify_python`: 8 blocks, 8 outputs checked, 0 mismatches.
- `check_code_teaching`: 0 findings.
- `checks/ch66_numbers.py`: every quoted number was recomputed and found in the text.
- `fig_check`: 0 figures under 7 pt.
- `restructure --check`: in order.
- `layout_check`: 22 pages, map 12/12, no stranded heads or lead-ins, no sparse pages, tofu 0. The "draft" hits are story text.
