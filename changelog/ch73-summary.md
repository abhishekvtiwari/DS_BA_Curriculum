# Chapter 73, Statistics, Probability & Experimentation Bank: summary

**Findings:** 29 content (73.1–73.29) and 13 visual (V73.1–V73.13). 28 content rows fixed (9 of them verified by a code run or in the rebuilt PDF); 73.28 is left Approved for the Part 8 renumbering in the final pass. V73.1, V73.2 and V73.7 fixed and checked in the rebuilt PDF; the other ten visual rows were done by the style pass and still hold.

## What changed

- **No drafting leftovers, real pointers.** The "this chat doesn't have…" note and every "Chapter 21 or nearby (… to confirm)" are gone. Every question and every rapid-fire row names the section that teaches it, checked by heading against the current Ch 21, 22, 30 and 31. Where this leads no longer calls Ch 22 the causal-inference chapter, and no longer promises "bias/variance foundations" the chapter doesn't have.
- **Runnable from a blank notebook.** New §73.0 with the setup cell (imports and the seed) and the level and role legend. Every cell prints what its output shows; each simulation reseeds, so it gives the printed answer on its own.
- **Nothing tested before it's taught.** The two puzzles now point to Ch 21 §21.7, where they are taught, and begin "by hand first". Ideas the book doesn't teach are marked **Beyond the book** and explained on the spot: log-normal data, holdout groups, partial correlation (defined and run, plus the book's own regression version), and the winner's curse.
- **Corrections.** Bayes question retitled (sensitivity is not accuracy), with a 1,000-person table. Birthday tiers fixed. The Type I/II example is no longer backwards. Peeking text now says 9 looks, matching the code. Chi-square uses `correction=False` as Ch 22 does (9.023, p = 0.0027). Q73-020's MDE is a business choice (1.5 points, 6,466 per group) rather than the Q73-036 result. Q73-036 now carries the interval (+0.11 to +2.49 points) and the power (0.57 at 5,000 per arm) that make its point.
- **Format.** Level and roles on every question (the Ch 70 bank format), the Chapter 69 tags, and a Time needed line.

## Skipped or changed from the finding, and why

- **73.28:** the Q73- ID rename belongs to the Part 8 renumbering (72A.2, final pass). The text's "Chapters 70–72A" is gone.
- **73.23, 73.24:** handled in Ch 73 (Beyond the book; the rule stated in the answer). The optional sentences for Ch 30 §30.8 and Ch 22 §22.2 are listed for the integrator.
- **73.25:** the optional rebuild of Q73-036 on Ch 30's numbers wasn't done. Q73-026 links Ch 30's test instead.
- **73.15:** the rate across seeds is **16–18%**, not the finding's 15–16% (ten seeds, computed).
- **73.20:** Ch 22's formula gives **6,473** for the new MDE. The finding's 8,544 was for the old MDE.
- **73.27:** Fresher/Mid/Senior levels, not ●○○ dots (Part 8 bank format).

## Option picks

- 73.4 → (a), recommended; the Ch 21 half was done in Part 2.
- 73.15 → the first route (say 9 looks).
- 73.16 → the recommended route (match Ch 22).
- 73.23 → the finding's alternative ("New in this bank" as Beyond the book), because the other route edits Ch 30.
- No section D picks apply.

## Time needed

New: "about 8–10 hours for a first pass, running every cell and saying each answer aloud; 1 hour for the final-week list" (row 73.27; the chapter had none). The PDF grew from 19 to 27 pages because of the new cells and explanations.

## Code verification

- `tools/verify_python.py`: 17 blocks run, **16 outputs checked, 0 mismatches** (Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, statsmodels 0.15.0, pandas 3.0.6). Every output was written by running the cell.
- `checks/ch73_check.py` recomputes every number stated outside a cell, **0 mismatches**. That covers the 1,000-person table, accuracy 95.0%, 253 pairs, Ch 22's formula 6,473, the peeking rate across ten seeds, 9 looks, the 20-metric simulation 0.639 and 1 − 0.95²⁰ = 0.642, the relative lift 13.5%, z = −2.143 with the order swapped, Yates 8.431 / 0.0037, and Farah's SRM p < 0.001.
- `check_code_teaching.py`: 17 blocks, 0 flagged, 0 findings. `restructure.py --check`: already in order.
- Build: 27 pages. `layout_check`: no stranded heads or lead-ins, no sparse pages, no small text, tofu 0, map numbers 11/11. prescan: 0 sparse, 0 draft labels, 0 tofu. No figures.
