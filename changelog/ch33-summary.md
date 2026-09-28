# Chapter 33 summary: The Computer Science You Actually Need

**Findings handled:** 53 rows (43 content, 5 visual, 5 Reader's Journey). 27 Verified, 22 Fixed, 3 Approved (their remaining half belongs to other chapters), 1 left Open (33.21, held for reading order).

## What changed
- **Order (33.1):** sections now run Big-O, the four structures, hashing, stacks and queues, recursion, trees and graphs, searching and sorting, memoization/DP/greedy, memory, interviews. Recursion is taught before any recursive code, and figures appear in number order.
- **The slow code is shown (33.2, 33.10):** a new "The chapter's data" subsection runs the generator and prints one row of each file; the naive nested loop is a timed cell with its real output, followed by the re-measured 250–2,000 table.
- **Every timing re-measured on the build machine** (`checks/ch33_timings.py`, now with relative paths; log in `checks/ch33_timings_log.txt`). The naive loop is timed as the reader runs it (top-level cell), giving 11.62 s for 2,000 invoices, so about two minutes for the full file (was 75 s). Index: 0.050 s build, 0.007 s match. The text says timings vary by machine. Timed cells are marked `run: none` (as in Ch 18) and their outputs come from `checks/ch33_timed_cells.py`.
- **Python taught before use:** generator expressions, `key=` with a function, `lambda` (recalled from Ch 18 alongside a `def`), `_`, `any`, nested functions, decorators and `lru_cache` settings, `timeit`, heaps, lazy evaluation, node/edge.
- **Bugs fixed:** the exercise 12 test (1,000 identical cases), `band()` on negative amounts (guard plus a demonstration), "without sorting everything" now uses `heapq.nlargest`, the stability demonstration, the fake "iterative version", `if answer` on 0, the quadratic check in answer 5, the exponential cycle detector (now O(V+E), option b; the old one measured at 2.15 s on 18 diamonds).
- **Numbers and story:** "thirty times the work" arithmetic; a consistent Why this matters; the data declared synthetic and scaled-up; the counterparty is now the logistics partner (file `carrier_invoice_lines.csv`); Priya Nambiar named; the org chart extended to Gopal Sahu and checked against `riverstone_2025.staff`.
- **Figures redrawn** at a 700 px canvas (min 7.4 pt): Figure 33.1 on one true scale with ticks; Figure 33.2 from the real buckets (7, 6, 0, 7) with a real collision; Figure 33.3 with D1–D10 / B1–B10 badges and a key.
- **References:** JSON Ch 17; pandas/NumPy/merge Ch 18; ORDER BY/GROUP BY Ch 12; grain Ch 14; Ch 72A bank; Where this leads now points forward (35, 46, 48, 49, 55, 72A/72, 69) with a "Looking back" line.

## Skipped, and why
- **33.21** (pipes/`head` in the Tool note and answer 14): held Open for reading order; Ch 34 comes before Ch 33, so the text is already correct.
- **RJ-S3-46 / RJ-S2-15 / RJ-S3-34:** only the Ch 33 part is done; the rest belongs to Ch 41, Part 4 and an appendix.

## Option picks
33.5 first option; 33.9 first option (logistics partner, rename); 33.18 option (b) (recommended); 33.26 option (a) "Looking back"; 33.17 used Ch 17's rebate bands as suggested.

## Time needed
Was 12–16 hours; now **14–18 hours over three weeks, in four sittings**, because of the added data setup, naive-loop cell, hand-worked DP table, stability/heap/guard cells and the recursion reordering (the review's own estimate).

## Verification
- `verify_python.py`: 37 blocks run, 36 outputs checked, **0 mismatches** on Python 3.11.15, 3.12.3 and 3.13.12.
- `verify_shell.py`: 1 command, 0 mismatches. No SQL in the chapter.
- `checks/ch33_check.py`: 39 checks pass (data counts, timing log values, story arithmetic, DP table, greedy optimal with and without ₹2000 up to ₹5,000).
- `fig_check.py`: 0 figures under 7 pt. `restructure.py --check`: in order. `layout_check.py`: map 16/16, no stranded heads/lead-ins, no sparse pages, tofu 0, no draft labels. 40 pages.
