# Chapter 72, Python & pandas Question Bank: summary

**Findings:** 29 content (72.1–72.29) and 11 visual (V72.1–V72.11). All 29 content rows fixed; V72.1, V72.2, V72.3, V72.5, V72.7 fixed and checked in the rebuilt PDF; V72.4, V72.6, V72.8–V72.11 were already done by the style pass and still hold in the rebuilt PDF. Nothing left open in this chapter (72.3 is fixed with option (b); option (a) is asked as a question).

## What changed

- **No drafting leftovers, real pointers.** The "this chat doesn't have…" note is gone. Every *Learn it in* line names a real chapter and section, checked against the current Ch 17, 18, 29, 33 (and 2, 12, 43, 54, 71). Each rapid-fire table has its own pointer line.
- **Nothing tested before it's taught.** Ideas the book never teaches (mutable defaults, aliasing and copies, closures and late binding, `*args/**kwargs` in a `def`, writing a decorator, `functools.wraps`, `__new__`, `@staticmethod`, class attributes, the walrus, the integer cache) are marked **Beyond the book**, each with a short worked explanation and real output. Ideas the book now teaches point there: `lambda` (Ch 18 §18.6), keyword-only `*` (Ch 29 §29.9), generators (Ch 29 §29.9, Ch 33 §33.9).
- **Two wrong pandas answers corrected** for pandas 3: chained assignment never updates `df` and warns `ChainedAssignmentError` (shown, then the `.loc` fix); `str.contains` gives `False` for a missing value on the `str` dtype, `None` on `object`/older pandas (both shown, plus `na=False`).
- **Every output reproducible.** A toy `orders`/`customers` setup cell before §72.5; broken or print-less cells split and given `print`; the generator question measures memory properly (`getsizeof` and `tracemalloc`: 40.4 MB vs 400 bytes); the `.apply` timing shows its setup, timer, and a verified match check; the messy-export walk-through shows the cleaned table and dtypes.
- **Order and labels.** Questions renumbered Q72-001…054 in reading order; rapid-fire headings match their sections; every question carries a level (Warm-up / Core / Advanced) and §72.2 runs easy to hard within each group.
- **Chapter at a glance** now has *Before you start* and *Time needed*. Extra-point tags use Chapter 69's twelve.

## Skipped or changed from the finding, and why

- **72.3:** option (b) applied (Beyond the book, in this chapter). Option (a) would add teaching to Ch 17, 18 and 29, which are finished; raised as a question.
- **72.9:** `customers` has 4 rows, not 7: the finding's own outputs need exactly four.
- **72.15:** easy-to-hard ordering is within each group (core questions, then each table); one interleaved order would break the core/table format.
- **72.17:** Python gives no `SyntaxWarning` for `is []` (checked on 3.11 and 3.13). The text quotes the real warning for `is 1000` instead, and says `is []` gets none.

## Option picks

72.3 → (b) (see above); 72.6 → the finding's second route (`tracemalloc`, as in Ch 33). No section D picks apply.

## Time needed

New: "about 4–6 hours to run every snippet yourself; 1 hour for a revision pass". The chapter had none. The PDF grew from 24 to 34 pages, because of the new cells and explanations.

## Code verification

- `tools/verify_python.py`: 44 blocks run, **42 outputs checked, 0 mismatches**, on Python 3.11.15 and pandas 3.0.6. Outputs were written by running the cells, never typed.
- `checks/ch72_check.py`: the 14 predict-the-output table rows (Q72-015–028) match a real run; the Q72-005 and Q72-051 claims hold; it prints the two timing cells (Q72-030, Q72-047), whose outputs in the chapter come from its run. **0 mismatches.**
- `tools/check_code_teaching.py`: 46 blocks, 0 flagged. `restructure.py --check`: already in order.
- Build (re-run 30 Sep after the final edit): 34 pages. `layout_check`: no stranded heads or lead-ins, no sparse pages, no small text, tofu 0, map numbers 10/10. prescan: 0 sparse pages, 0 draft labels, 0 tofu. No figures.
- Version note: generator `getsizeof` is 208 bytes on 3.11 and 200 on 3.12/3.13 (all checked); the text says so. Python 3.14 isn't installed here, so it wasn't run.
