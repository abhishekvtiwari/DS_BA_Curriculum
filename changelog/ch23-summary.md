# Chapter 23, Business Acumen, KPIs & Metrics: summary (Part 2 build)

**What changed.** The chapter now teaches its finance from zero and its numbers agree with each other and with the data.
- **Vocabulary first.** §23.2 opens with a "Words Finance will use" table (depreciation, accrual, capex, leverage and eight more, each with a Riverstone example), and links accrual to Chapter 3's booked / billed / collected.
- **By hand, then code.** The P&L is walked by hand before its code; the cash flow's signs are a by-hand bridge table before its code; DIO, DSO, DPO and CCC now have formulas, a by-hand working from the balance sheet and a Python cell (§23.3 "Putting days on the cycle"); the May → June bridge has its formulas in symbols, one effect worked by hand, a reverse-order cell and a segment-mix cell.
- **Code taught like Jupyter.** The funnel and customer blocks are split into small cells (18 more cells in all), every line explained; every output is from a real run.
- **Consistency fixes.** Duplicate leads removed before the funnel (30 enquiries, not 43; win rate on all enquiries 20%, not 14%), as Chapter 13 did. The customer counts reconcile (3,827 + 772 = 4,599); the companion marketing file was regenerated to the real 772 new customers, so CAC is ₹8,141 and LTV:CAC 26.6. The KPI identity is now exact. Riverstone is a manufacturer and distributor; Chapter 21's delivery data is called simulated; "FY2025" became calendar 2025; the ratio 0.91 is called liabilities-to-equity; the real-world DSO story has a quarter-end table behind it.
- **Figures.** All four redrawn from the companion data, smallest text 7.4–8.5 pt (was 4.6–6.3 pt); Figure 23.1 is now a timeline that separates the operating cycle from the cash conversion cycle, and Figure 23.3 is a profit tree whose boxes multiply or add exactly.
- **Structure.** Part A "Money" (§23.1–23.4) ends with a checkpoint; Part B is §23.5–23.13. Exercises 13–14 and Timed-challenge Levels 5–6 moved off the December dip, which Chapter 24 now presents itself (finding 24.1).

**Skipped or changed from the finding, and why.**
- 23.36: no `BASE = Path("../")` setup cell; pandas is imported once and the glance box explains `../full/`, as other chapters do.
- 23.37: §23.7 (finance metrics) was not moved into Part A; moving it would renumber §23.5–23.7.
- 23.2: Figure 23.1 keeps Riverstone's day counts, with "worked out in section 23.3" in its title and caption.
- No row left Open.

**Option picks.** 23.6 (a) rename to liabilities-to-equity; 23.8 (a) quarterly table; 23.13 (a) print leads + reconciling sentence; 23.14 (a) compute payback in §23.9; 23.15 (a) delete the dead line; 23.20 (a) regenerate the marketing file to 772; 23.22 (a) caveat; RJ-S1-9 the first (deduplicate); RJ-S3-17 the first (say "calendar 2025", drop FY).

**New Time needed.** 17–20 hours (was 15–18): Part A about 8 h, Part B about 10 h, project 2 h, as finding 23.37 estimated for the added vocabulary, by-hand work and cells.

**Code verification.** `verify_python.py`: 28 blocks run, 28 outputs checked, 0 mismatches. `verify_sql.py`: 1 statement, 0 mismatches (PostgreSQL, `riverstone_full`). Prose numbers in answers recomputed from the data. PDF: 41 pages; layout_check clean (19/19 map numbers, no stranded heads, no sparse pages, no small text, no tofu); fig_check: 0 figures under 7 pt.
