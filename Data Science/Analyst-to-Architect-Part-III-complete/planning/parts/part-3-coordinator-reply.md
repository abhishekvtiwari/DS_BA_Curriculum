# Coordinator reply to the Part III chat — 19 September 2026

*Paste this into the Part III chat.*

Part III is received and merged. Seven chapters, about 92,000 words, 293 PDF pages, 29 figures. This is the cleanest delivery so far: every figure reference resolves, every companion file named in a chapter is present, and the independent style scan found two words in 92,000 (one `analyse` in Chapter 29 §29.14, one `honestly` in Chapter 30 exercise 3) and **no em dashes in prose anywhere**. Thank you for that.

## Decisions you asked for

**1. Chapter 28's performance dataset — keep `riverstone_perf`.** Do not switch the timings to `riverstone_full`. `riverstone_perf` exists to make index and plan differences visible; `riverstone_full` is six times smaller (116,194 orders against 714,285), so the timings would shrink toward noise and every plan and number in the chapter would have to be re-measured for a weaker demonstration. Your current framing is the right one: a volume dataset, not canon, with a note that the same commands work on the full dataset.

**2. `tools/verify_python.py` — fixed, using yours.** The one-line fix from `checks/py_fill.py` is applied in the project's copy: the skip flag is cleared when the next fence is not Python. Please re-run `verify_python.py` on Chapters 29, 30, 31 and 33 with the fixed version, because any block the bug was hiding has never been verified. Report the new totals.

**3. `tools/verify_shell.py` — adopted.** It is now the project's third verifier, written into instructions §9.2b alongside the SQL and Python ones, with your contract: terminal sessions as unlabeled fences with `$ ` prompts, regenerate the practice folder before each run, never verify as root.

**4. `tools/setup_databases.sh` — extended.** It now loads `ch28_2025_addons.sql` and `ch28_star_schema.sql` into `riverstone_2025` when the Part III companion files are present, and documents the `riverstone_perf` build rather than running it.

**5. Your new Riverstone facts are accepted into the bible** — the 35-person HRMS `staff` view and the two-system explanation, the department heads, the plants and operations staff, the bills of materials and suppliers, the 2025 customer-change audit log, `riverstone_perf` as explicitly non-canon, the digital domain, and the causal datasets.

## Two things to fix

**Issue 10 — Chapter 28's eight regional sales executives.** Your status file offered to follow Part II-A's names if they existed. They do. The full dataset has exactly eight, with IDs:

| `employee_id` | Name | Reports to |
|---|---|---|
| 9 | Kavitha Reddy | Arjun Nair (South) |
| 10 | Irfan Sheikh | Arjun Nair (South) |
| 11 | Meenal Joshi | Pooja Desai (West) |
| 12 | Rohit Verma | Pooja Desai (West) |
| 13 | Divya Menon | Arjun Nair (South) |
| 14 | Aakash Jain | Sandeep Gill (North) |
| 15 | Simran Kaur | Sandeep Gill (North) |
| 16 | Tarun Bose | Pooja Desai (West) |

Please adopt these in `ch28_2025_addons.sql` and fill `employee_id` 9–16 (currently NULL). *Divya Krishnan* against *Divya Menon* and *Rohit Kamat* against *Rohit Verma* are near-collisions, which read worse than clean differences. The names appear 24 times in printed query output, so the queries have to be re-run and the outputs replaced. Your three regional managers already match exactly, so nothing else moves.

**Issue 9 — Chapter 29's "before" script no longer matches Chapter 18** (author decision needed; do not act yet). Chapter 18 is now written, and its §18.15 `monthly_report.py` is already a reasonable script: `logging`, a command-line month argument, `--out`, reading `riverstone_full`. Chapter 29 opens by refactoring "the Chapter 18 script" but ships a deliberately poor one (hard-coded password, SQL by string concatenation, bare `except`, no functions, `riverstone_2025`). A reader who has just finished Chapter 18 will see the mismatch.

The coordinator's preferred resolution is that Chapter 29 takes Chapter 18's actual script as its starting point and refactors *its* real weaknesses — no package layout, no tests, no type checking, no config or secrets handling, no error taxonomy, no retries on the API call — which teaches more than starting from a straw man. The fallback is that Chapter 29 stops calling it the Chapter 18 script and presents `start/monthly_report.py` as a script of the kind analysts inherit. Either way the databases must agree: Chapter 18 uses `riverstone_full`. Both are in `planning/cross-part-issues.md` as issue 9, waiting on the author.

**D7 and D8** (venv + pip taught first then uv; `requests` with explicit retries, `httpx` mentioned): both approved as you proposed. Verify the current docs before the chapter is finalized; the versions are on the refresh list.

## The part-completion review pass is now due

Part III is complete, so instructions **§15.1** applies: read the part straight through as a reader would before editing anything, list the problems, work out the cause of each at the level of the part, then fix in place and re-verify. Chapter 29's review is part of this, since it is the one chapter still at draft.

Input for that pass — `tools/check_code_teaching.py`, which enforces §6.5. The tool has been improved since you last saw it: it now recognizes unlabeled terminal sessions as code (Chapter 34 was being reported as 3 code blocks when it has 43), and it reports blocks flagged separately from total findings.

| Chapter | Code blocks | Blocks flagged | Findings |
|---|---|---|---|
| 28 | 88 | 40 | 42 |
| 29 | 39 | 28 | 46 |
| 30 | 40 | 38 | 63 |
| 31 | 32 | 30 | 44 |
| 32 | 33 | 16 | 17 |
| 33 | 28 | 26 | 47 |
| 34 | 43 | **10** | 11 |

Chapter 34 is the model: `$ ` sessions followed by **How it works** bullets, one per command, saying what each flag does. Chapters 30, 31 and 33 are the ones to look at hardest, because they teach statistics and algorithms to readers meeting `fit`, `conf_int`, `lru_cache` and `maxsize` for the first time. Every chapter is flagged for having no measured "what happens if you change this setting" demonstration, which §6.5 now requires at least once per important setting.

Remember that a flag is a question, not a verdict. Record deliberate exceptions in your report with one line each.

## Small things

- Two style fixes for the pass: `analyse` → `analyze` (Ch 29 §29.14) and rewrite Chapter 30 exercise 3 without `honestly`.
- Your note on Chapter 13's "11 orders missing a sales rep" is right; it is logged as issue 12 and the coordinator owns the Chapter 13 edit.
- The PDF CSS suggestion (smaller mono font in very wide output blocks) is accepted; the coordinator will make it at assembly so every part's PDFs change together.
- Your promises to other chapters are recorded, including Chapter 32's to rebuild `dw` as dbt models with snapshots for SCD2.
