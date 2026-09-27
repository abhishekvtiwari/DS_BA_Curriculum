# Code-teaching baseline (instructions §6.5)

Produced by `tools/check_code_teaching.py` on 20 September 2026, across every written chapter. This is the reading list for each part's review pass (§15.1), not a verdict on any chapter.

The tool has been corrected three times since it was written: it now recognizes unlabeled terminal sessions as code, matches keyword arguments rather than every variable assignment, and reads a 40-line explanation window so a long "Line by line" list counts.


## Part 0 — First Principles

| Ch | Code blocks | Blocks flagged | Findings | Settings table | Predict prompt |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | — | — |
| 2 | 0 | 0 | 0 | — | — |
| 3 | 0 | 0 | 0 | — | — |
| 4 | 0 | 0 | 0 | — | — |
| 5 | 0 | 0 | 0 | — | — |
| 6 | 5 | 2 | 3 | — | — |
| **total** | **5** | **2** | | | |

## Part I — The Map

| Ch | Code blocks | Blocks flagged | Findings | Settings table | Predict prompt |
|---|---|---|---|---|---|
| 7 | 2 | 1 | 2 | — | — |
| 8 | 0 | 0 | 0 | — | — |
| 9 | 0 | 0 | 0 | — | — |
| **total** | **2** | **1** | | | |

## Part II — The Analyst

| Ch | Code blocks | Blocks flagged | Findings | Settings table | Predict prompt |
|---|---|---|---|---|---|
| 10 | 28 | 1 | 2 | — | — |
| 11 | 58 | 5 | 5 | — | — |
| 12 | 167 | 25 | 26 | — | yes |
| 13 | 45 | 17 | 18 | — | — |
| 14 | 45 | 5 | 6 | — | — |
| 15 | 7 | 3 | 6 | — | — |
| 16 | 5 | 4 | 6 | — | — |
| 17 | 38 | 20 | 24 | — | — |
| 18 | 43 | 30 | 45 | — | — |
| 19 | 7 | 6 | 8 | — | — |
| 20 | 11 | 8 | 16 | — | — |
| 21 | 17 | 7 | 11 | — | — |
| 22 | 16 | 11 | 17 | — | yes |
| 23 | 12 | 6 | 10 | — | — |
| 24 | 0 | 0 | 0 | — | — |
| **total** | **499** | **148** | | | |

## Part III — Advanced Analytics

| Ch | Code blocks | Blocks flagged | Findings | Settings table | Predict prompt |
|---|---|---|---|---|---|
| 28 | 88 | 33 | 35 | — | — |
| 29 | 39 | 23 | 37 | — | — |
| 30 | 40 | 31 | 41 | — | yes |
| 31 | 32 | 22 | 30 | — | — |
| 32 | 33 | 14 | 15 | — | yes |
| 33 | 28 | 24 | 36 | — | — |
| 34 | 43 | 6 | 7 | — | yes |
| **total** | **303** | **153** | | | |

## Part IV — Machine Learning

| Ch | Code blocks | Blocks flagged | Findings | Settings table | Predict prompt |
|---|---|---|---|---|---|
| 35 | 26 | 12 | 15 | — | yes |
| 36 | 26 | 17 | 28 | — | — |
| 37 | 32 | 28 | 43 | — | — |
| 38 | 25 | 18 | 26 | — | — |
| 39 | 27 | 20 | 27 | — | — |
| 40 | 27 | 22 | 34 | — | — |
| 41 | 27 | 22 | 33 | — | — |
| 42 | 23 | 19 | 29 | — | — |
| 43 | 25 | 18 | 30 | — | — |
| 44 | 9 | 6 | 8 | yes | yes |
| **total** | **247** | **182** | | | |

## Part V — Data Engineering

| Ch | Code blocks | Blocks flagged | Findings | Settings table | Predict prompt |
|---|---|---|---|---|---|
| 45 | 24 | 6 | 10 | — | — |
| 46 | 17 | 15 | 21 | — | — |
| 47 | 14 | 4 | 6 | — | — |
| 48 | 12 | 7 | 10 | — | — |
| 49 | 9 | 6 | 8 | — | — |
| 50 | 10 | 7 | 10 | — | — |
| 51 | 9 | 5 | 7 | — | — |
| 52 | 7 | 2 | 4 | — | — |
| **total** | **102** | **52** | | | |

## Part VI — Production ML & GenAI

| Ch | Code blocks | Blocks flagged | Findings | Settings table | Predict prompt |
|---|---|---|---|---|---|
| 53 | 24 | 9 | 11 | — | — |
| 54 | 17 | 13 | 15 | — | yes |
| 55 | 21 | 9 | 11 | — | — |
| 56 | 17 | 10 | 12 | — | — |
| 57 | 14 | 6 | 9 | — | — |
| 58 | 13 | 7 | 12 | — | — |
| 59 | 0 | 0 | 0 | — | — |
| **total** | **106** | **54** | | | |

## What the columns mean

- **Blocks flagged** — code blocks where something in §6.5 may be missing: no plan in words before the block, nothing explaining it after, thin coverage of the identifiers used, or more than 25 lines in one block.
- **Findings** — the total count of issues, since one block can raise more than one.
- **Settings table** — whether the chapter contains the column "What happens if you change it" that §6.5 requires the first time a function takes settings.
- **Predict prompt** — whether the chapter asks the reader to write down what they expect before running something.
