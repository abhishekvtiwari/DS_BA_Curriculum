# Chapter 42 · Recommender Systems & Ranking · summary

**What changed.** All 38 content findings and the two open visual findings were applied; the eight visual rows the layout pass had fixed were re-checked in the rebuilt PDF.

- **The metric is named correctly.** The chapter's "precision@5" was a hit rate. §42.3 now defines hit rate@k, recall@k, precision@k, NDCG@k and MRR@k (with MAP worked by hand), and `evaluate` returns hit rate, NDCG and MRR. Precision@5 is shown once (12.5%) to make the point.
- **§42.3 is taught in steps.** The metrics come first, worked by hand with 1-based positions. Then the hold-out, then one account scored by hand, and only then the `evaluate` function. A new cell compares item-CF on raw, yes/no and log quantities; yes/no is best, at 68.7% against 65.0%.
- **§42.4 has a by-hand factorization.** The toy table ≈ A × B, and the empty cell that gets a score is the recommendation. Then come TruncatedSVD on the toy, a shapes cell, a box on freezing a loop's value, and the ALS parameters and algorithm explained.
- **New §42.0 Setting up.** It installs `implicit` (with install help) and checks its version.
- **One scoreboard in §42.7.** It covers 10 methods on three measures, with segment-level popularity moved into the body. That baseline wins (71.5%), and the real-world story now says so.
- **Answers.** Answer 9 now runs (it used to print a `ValueError`). Answer 12 is a real time-based holdout of three methods, and there the ranking changes. Exercise 8 is now per-segment item-CF, and exercise 13 (LightFM) is marked optional.
- **Smaller fixes.** User-based CF, sparsity, explicit feedback and latent factors are now taught. Names replace product IDs in outputs. Cross-references were corrected (Ch 36 §36.6, Ch 38 §38.9, §42.5), the "block F" and "Appendix G" leftovers are gone, and "Before you start" is complete.

**Skipped, and why.**
- RJ-S3-46 is Open: it needs the story bible and fact sheet, which aren't approved yet.
- The two SVG figures in `figures/` are regenerated but still not placed in the chapter. No finding asked for them, and the scoreboard table carries the same numbers.

**Option picks.** No finding marks a recommended option, so the first option (a) was used for each:
- 42.1: rename, and also return all three measures.
- 42.19: compute item-CF on yes/no and log data, and report the results.
- 42.21: teach the terms rather than delete them.
- 42.34: mark LightFM optional rather than replace the exercise.

**Time needed.** It was 6–9 h and is now **8–10 hours over one week, in two sittings** (42.0–42.3, then 42.4–42.7). The chapter grew from 27 to 40 PDF pages, mostly short cells and their outputs.

**Code verification.**
- `verify_python.py`: 42 blocks run, 42 outputs checked, **0 mismatches**. It also passes with a different `PYTHONHASHSEED`, because set iteration is sorted wherever ties could print.
- `check_code_teaching.py`: 3 answer blocks flagged. They reuse code taught in the body.
- `checks/ch42_check.py`: all checks pass.
- `restructure.py --check`: the stages are already in order.
- `layout_check.py`: no stranded headings or lead-ins, no sparse pages, no small text, tofu 0, map numbers 14/14.
- `fig_check.py`: 0 figures under 7 pt.
- The shell cell is marked `run: none`, because it runs pip.
- Every number comes from the fixed Chapter 38 basket data: 34,013 orders, from `order_lines.csv` with md5 5445562274….
