# Chapter 72A summary: Data Structures & Algorithms Question Bank

**Findings:** 46 rows (33 content, 13 visual): 44 Verified (fixed and checked in the rebuilt PDF or by a passing verifier; 12 of the visual rows were done by the style pass and re-checked here), 2 left for the final pass (72A.2 renumbering, 72A.26 ID mapping).

## What changed
- **Drafting leftovers gone:** the "note on this chapter's numbering" (addressed to the coordinator), "this chat", "this environment". The opening is now a "Chapter at a glance" box: You will practise, Before you start (**do Chapter 33 first**), Time needed, How built, Learn it in.
- **Every Learn-it-in line re-pointed** from "Chapter 72" (a question bank that teaches none of this) to the Ch 33 sections as they stand now (33.1 to 33.10), plus Ch 28 §28.4 (B-trees), Ch 29 §29.5 (classes), Ch 40 §40.6 (`.rolling()`), Ch 41 §41.3 (bag of words).
- **Beyond the book primers** for the four topics no chapter teaches: two pointers and sliding windows (start of §72A.3, with printed traces), merge sort by hand (Q72A-020), linked lists (start of §72A.7, with a Node class and a printed reversal trace), binary search trees (start of §72A.8, with a hand drawing and a measured height 3 vs 7).
- **Code fixed:** BFS `visited` is a set (O(V + E)); Fibonacci uses `@lru_cache` instead of the `cache={}` mutable default, shows the RecursionError at fib(1500) and the bottom-up loop; sliding-window k > len trap shown; binary search's unsorted-input trap shown.
- **Code taught like Jupyter:** every snippet is a run cell with its real output (no more `# -> … (verified)` comments), each explained line by line; timings in marked cells.
- **Corrections:** Big-O is an upper bound (not "worst case by default"); 12,497,500 comparisons vs 25 million; quicksort wording; B-trees (not AVL/red-black) in databases; hashability; RecursionError vs stack overflow; "fib(2) computed 196,418 times" and 1,028,457 calls in total (the review's 832,039 was fib(30) − 1, not a call count).
- **Format:** Ch 69's twelve tags; Level (Fresher/Mid/Senior) and Roles (DE, AE, MLE, DS, DA) on every question, as in Ch 70; real-world story retitled "a scale question".

## Option picks
- 72A.6 and 72A.8: option (b), a primer in this bank. The recommended (a) adds sections to Ch 33, which is outside this chapter's files: raised as a question.
- 72A.9 and 72A.10: the by-hand box and trace tables are here, not in Ch 33 (same reason).
- 72A.7: kept plain classes (Ch 29 §29.5 now teaches `__init__`/`self`) plus the reminder box; dataclasses would make nodes unhashable.
- 72A.12: `@lru_cache`. 72A.27: keep forward references, marked "below". 72A.28: Ch 70's level scale rather than ●○○.

## Skipped, and why
- 72A.2 (renumber 72A → 73 and the Q-ID prefixes) and 72A.26 (ID mapping): final pass (D2). IDs are unchanged, so Ch 33's and Ch 77's references still resolve.

## Time needed
6–8 hours to run every snippet and answer aloud; 1 hour revision; +3–4 hours if the Ch 33 sections are new (there was no line before).

## Verification
- `tools/verify_python.py`: 28 blocks run, 26 outputs checked, **0 mismatches** (Python 3.11.15).
- `checks/ch72a_check.py`: re-runs everything including the two timing cells (doubling n gives ×3.8–4.1 for O(n²); memoized Fibonacci 5,000–8,000× faster), the Big-O table numbers, and the 12 rapid-fire answers without a cell: all pass.
- `check_code_teaching.py`: 30 blocks, 0 flagged. `restructure.py --check`: already in order. No figures.
- PDF: 31 pages; layout_check clean (map 12/12, no stranded heads/lead-ins, no sparse pages, no small text, tofu 0); prescan clean.
