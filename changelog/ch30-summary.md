# Ch 30 — Inference & Experiments: summary

**Rows handled:** 44 content (30.1–30.44), 15 visual (V30.1–V30.15), 4 Reader's Journey (RJ-S2-16, RJ-S3-32, RJ-S3-34, RJ-S3-42). All 44 content rows and V30.2–V30.6 and V30.13 are fixed. RJ-S3-32 is checked and clarified. RJ-S2-16 stays Open. RJ-S3-34 and RJ-S3-42 belong to other chapters.

## What changed
- **Builds on the rebuilt Ch 22.** A "What's new since Chapter 22" box sorts the chapter into recap (§22.1–22.4, §22.10, with pointers) and new material. The recap passages are labelled. The peeking result (25.5%) is reconciled with §22.4's 14.3% and 23.9%.
- **Just-in-time setup (§30.1).** A bare uv project (`uv init --bare`, `uv add …`, `uv add --dev ipykernel pytest`), with real terminal output. The generator runs with `uv run python`. One setup cell holds every import. A tool note says the Chapter 17 environment also works.
- **By hand first.** A five-session interval by hand and in a spreadsheet (§30.2). Welch's SE and df (§30.3). The Wald interval and the pooled SE (§30.5). F on a 3×3 toy (§30.6). The sample-size arithmetic, symbol by symbol (§30.7). The SRM chi-square (§30.9). Odds and the odds ratio (§30.11).
- **Regression for inference (§30.11), rebuilt from §22.10.** One x beside `linregress`, then one category, then several variables, then R². A formula-syntax box. Logistic regression built up from the hand odds ratio. The cluster-robust caveat.
- **Unit of analysis applied throughout.** ANOVA and novelty now run per visitor (novelty lifts +22% and +5%). The channel is taken from the visitor's first visit.
- **Corrections.** 35 → about 560 enquiries a month (interval 200 to 930). Tablet +20% → +35%. Once in 2,000 → 3,300. "Twenty" → nearly 200. MDE 1.5 → 1.3 points. Novelty common mistake. Wrong cross-references (Ch 19, 42, 55; Ch 17 pandas). Hard-coded password → `RIVERSTONE_DATABASE_URL`.
- **Tested code.** `companion/ch30/ab_summary.py` holds `two_proportion_summary`, and `test_ab_summary.py` pins the book's numbers. The Safari-excluded result is now computed in §30.10 with that function.
- **Checkpoint and what-if.** A what-if cell on the MDE. A checkpoint after the second sitting, with its answer.
- **Figures.** All four figures redrawn at 680 px (smallest text 7.6 pt), with their numbers computed from the data or statsmodels. The line in the experiment figure is drawn. The false winners are marked with ×. Figures 30.3 and 30.4 are renumbered into page order.

## Skipped, and why
- **RJ-S2-16 (story calendar):** stays Open. Moving Part 3's story dates needs the fact-sheet calendar, which isn't approved yet.
- **RJ-S3-34 (dataset list) and RJ-S3-42 (Ch 37/39 pointers):** these belong to other chapters. §30.11 now reads the coefficient intervals that those pointers will target.
- **Option-style choices:**
  - 30.9: option (a), the by-hand table;
  - 30.19: option (a), aggregating to visitors.
- **Recomputed numbers that differ from a finding's suggested wording:**
  - 30.27: the ends are 200 and 930, not 190 and 920;
  - 30.31: +22% against +14%, because it is now per visitor;
  - 30.32: 1.3 points (exact), not 1.25 (approximation).

## Time needed
It was 14–18 hours; it is now **18–22 hours over three weeks**, in four sittings:
- §30.1–30.4: about 5 h;
- §30.5–30.7: about 5 h, ending with a checkpoint;
- §30.8–30.10: about 5 h;
- §30.11–30.12: about 4 h;
- the project: 2 h.

The extra hours come from the regression and logistic build-up, the by-hand steps and the tested function (finding 30.40's estimate). The PDF grew from 37 to 55 pages.

## Verification
- `tools/verify_python.py`: 61 blocks run, 60 outputs checked, **0 mismatches**. This holds on Python 3.11.15 (numpy 2.4.6, scipy 1.17.1, statsmodels 0.15.0, matplotlib 3.10.8) and on Python 3.14.7 in the chapter's uv project (numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2). It needs `RIVERSTONE_DATABASE_URL` pointing at `riverstone_2025`, and `companion/ch30/web_data/` built by the generator.
- **Terminal blocks** are `run: none`: the uv installs need the network, and the timings vary. Their outputs were pasted from real runs on 28 Sep 2026. `uv run pytest -q` passes.
- `checks/ch30_check.py`: **44 checks passed**, 14 of them new for this rewrite. Its default path is now the repo's `companion/ch30`.
- **Layout:**
  - `tools/pdf/fig_check.py`: 0 figures under 7 pt;
  - `tools/restructure.py --check`: already in order;
  - `layout_check.py`: no stranded heads or lead-ins, no sparse or small-text pages, tofu 0, map 18/18;
  - prescan is clean. Its line-end hyphen breaks are real compounds.
- `check_code_teaching.py`: 6 remaining flags. They are the test file and answer cells that reuse code taught earlier in the chapter.
