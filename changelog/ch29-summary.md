# Chapter 29, Python as Software, Not Scripts: summary of the Part 3 build

**Findings handled:** 37 content (29.1–29.37), 17 visual (V29.1–V29.17), 4 Reader's Journey rows.
Fixed and verified: 35 of 37 content rows (29.1 and 29.2 are held Open for the reading order and were left alone,
apart from what other fixes forced), all 17 visual rows, RJ-S2-11. Open: RJ-S2-16 and RJ-S3-35 (need the fact sheet).
RJ-S1-11 needs nothing in Ch 29 (its fix is in Ch 34).

## What changed

- **Nothing is used before it's taught.** §29.2 now builds the report's functions in notebook cells on five
  hand-checkable lines (a dictionary first, then an error for an empty month), then shows the plain first
  `transform.py`, then runs the read functions against `riverstone_2025`. Classes get a twenty-minute primer at the
  start of §29.5 (seven cells: instance, `self`, methods, decorators, `@property`, data classes, `frozen`, inheritance,
  `@classmethod`); `MonthSummary` arrives there, type hints in §29.6, `NoDataError` in §29.8. TOML gets a one-minute box
  and a table. pytest is taught in real runs, one step at a time. The API client is built in five runnable steps
  (`try/except/else` and generators taught with toys) before the class.
- **Every output is real.** Python: 38 blocks, 0 mismatches. Terminal sessions (uv, pytest, mypy, the command line)
  were re-run with uv 0.12.19 and Python 3.14.7, the book's Python since Ch 17's rebuild; long outputs are shortened
  only by leaving out whole lines (they show the author's folder path), always said under the block.
- **Correct and consistent.** Package counts reconciled (16 / 53 / 58); `uv sync --no-dev`; the real mypy message in
  exercise 9; the `.env` route that works (`uv run --env-file`); `getLogger(__name__)` with its real output; December
  cited correctly (₹4,39,823.50, 115.7% of ₹3,80,000 from Ch 28); lakh grouping in prose and figures; Ch 20 no longer
  called a later chapter (a crontab line in Ch 20's style instead); Ch 30's pointer matches Ch 30.
- **The chapter closes Ch 26's loop.** "Run the tests on every push" extends Ch 26 §26.8's workflow with
  `astral-sh/setup-uv@v10.2.0`, `uv sync --locked`, pytest and mypy; it's now a core project step.
- **Reader-facing polish.** Appendix G note and the author check gone from the reader's list; Imran's script is
  called his, not the reader's Ch 18 script; a sentence tells the reader to put their own password in it before running.
- **Figures.** All four redrawn at 800 px (smallest text 7.4 pt, was 5.2–6.6); 29.2 now precedes 29.3; colour keys
  and non-colour cues (✗ marks, EDGE/CORE labels); Figure 29.4's rules as bullets.
- **Companion.** `riverstone-report` rebuilt with the chapter's own uv commands (new lockfile, Python 3.14,
  `.env.example`, README, `.gitignore` for caches, `.env`, reports); the client test checks the exact waits.

## Skipped, and why

- **29.1, 29.2:** held Open (they assume Ch 34 comes after Ch 29; recommended Reject). Only forced edits: Ch 26 is now
  a prerequisite (29.20 extends its workflow), `python -c` is glossed, `--project` is no longer used.
- **RJ-S2-16, RJ-S3-35:** depend on the unapproved fact sheet (book calendar; Imran's departure). No text change.

## Option picks

29.7 (b) (remove `from __future__`; (a)'s explanation is false on Python 3.14; see questions) · 29.9 (a) tenth
problem row · 29.16 (a) `uv run --env-file` · 29.24 (a) `getLogger(__name__)` · 29.29 (a) soften to Ch 30's stretch
goal · 29.30 (a) drop the check from the list · 29.31 (a) remove the figure · 29.37 (a) "Where this leads" · V29.2 swap
the figures.

## Time needed

Was 12–16 hours; now **20–24 hours over three weeks, in four sittings** (29.33). The chapter grew from 43 to 68 pages
with the class primer, the step-by-step pytest runs and the five-step client.

## Checks

`verify_python.py` 38/38, 0 mismatches · all terminal lines found in the real run logs · `checks/ch29_check.py` 35/35 ·
`restructure.py --check` in order · `fig_check.py` 0 figures under 7 pt · `layout_check.py`: no stranded heads or
lead-ins, no sparse pages, no small text, tofu 0, contents 16/16 (only "v10.2", the GitHub Action's version, is
flagged as a draft label) · `verify_shell.py`: every session is `run: none` (they need uv, a database or GitHub).
