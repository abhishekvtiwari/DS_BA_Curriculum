# Analyst to Architect — Part IV: Machine Learning & Data Science — complete bundle

Chapters 35–44. About 103,700 words, 34 figures, six new seeded datasets. Nine chapters approved; **Chapter 44 is draft v1 and awaiting the author's review**.

| Ch | Title | Class | Status | Words (with code) |
|---|---|---|---|---|
| 35 | The Math Under the Models | B | Approved v1 | ~15,900 |
| 36 | The Machine Learning Workflow & Feature Engineering | B | Approved v1 | ~11,900 |
| 37 | Supervised Learning Algorithms | B | Approved v1 | ~13,400 |
| 38 | Unsupervised Learning | B | Approved v1 | ~10,000 |
| 39 | Evaluation, Tuning, Interpretation & Honesty | B | Approved v1 | ~10,100 |
| 40 | Time Series & Forecasting | B | Approved v1 | ~10,400 |
| 41 | NLP Foundations | B | Approved v1 | ~8,900 |
| 42 | Recommender Systems & Ranking | B | Approved v1 | ~7,800 |
| 43 | A First Look at Deep Learning | B | Approved v1 | ~8,700 |
| 44 | Capstone: An End-to-End Data Science Project | D | **Draft v1, awaiting review** | ~4,300 |

Part IV was written before its prerequisites (Chapters 17–18 for Python, 21–22 for statistics), with the author's approval. Chapter 35 therefore defines variance, distributions and likelihood itself. Those chapters now exist; aligning them is cross-part issue 13.

## Not included, by design

- **Generated CSV and Parquet data.** Every generator is seeded and rebuilds its data in well under a minute. Run the generator before running a chapter's code.
- **Chapter PDFs.** In `pdf/`: one per chapter, ten of them, plus `Part-IV-all-ten-chapters.pdf`, the whole part in one file with a single cover, one contents page covering every chapter, and continuous page numbers. *(Added 27 September 2026; they were missing from the first build.)*

## The datasets this part builds

Each has a spec in `planning/data/`.

| Dataset | Generator | What it is | Chapters |
|---|---|---|---|
| CRM | `generate_riverstone_crm.py` (seed 20236) | 12,294 leads, 25,682 activities, 39,275 stage changes, 2023–2025 | 36 |
| Accounts | `generate_riverstone_accounts.py` | account-level features and churn outcomes | 37, 38, 39, 42, 43, 44 |
| Baskets | `generate_riverstone_baskets.py` | order lines for market-basket and recommender work | 38, 42 |
| Demand | `generate_riverstone_demand.py` | a demand series for forecasting | 40 |
| Sensors | `generate_riverstone_sensors.py` | plant sensor readings (`--full` gives the ~4.8M-row Ch 48 version) | 40 |
| Tickets | `generate_riverstone_tickets.py` | support tickets with free text | 41 |

Chapter 35's data comes from `companion/ch35/make_ch35_data.py`, derived from `generate_riverstone_2025.py`.

The CRM is an independent 2023–2025 dataset that reuses Riverstone's reps, segments, sources, cities and product categories, but is not joined row by row to `riverstone_2025`.

## Rebuilding

```
cd companion
python3 generate_riverstone_accounts.py      # Ch 37+
python3 generate_riverstone_crm.py           # Ch 36
python3 generate_riverstone_baskets.py       # Ch 38, 42
python3 generate_riverstone_demand.py        # Ch 40
python3 generate_riverstone_sensors.py       # Ch 40 (--full for the Ch 48 version)
python3 generate_riverstone_tickets.py       # Ch 41
cd ch35 && python3 make_ch35_data.py         # Ch 35

cd ../../figures && for f in make_figs3*.py make_figs4*.py; do python3 "$f"; done

python3 tools/verify_python.py manuscript/ch37-supervised-learning-algorithms.md --cwd companion
for f in checks/ch*_check.py; do python3 "$f"; done
python3 tools/check_code_teaching.py manuscript/ch37-supervised-learning-algorithms.md
```

Environment: Python 3.12.3, NumPy 2.4.4, pandas 3.0.2, scikit-learn 1.8.0, SciPy 1.17.1. Chapter 43 needs PyTorch (CPU build). `checks/fill_outputs.py` pastes real run output into a manuscript's output blocks; `verify_python.py` then re-checks it independently.

## Coordinator checks on this part

All 29 figure references resolve. Every file named in the chapters is either present or a documented generator output.

**Style scan** (code blocks, tables, figure captions and the part line excluded): Chapters 35–40 are effectively clean. Chapters 41, 42, 43 and 44 carry em dashes in prose (16, 42, 41, 32) and the banned words *genuinely* and *honestly*. Cross-part issue 15.

**`tools/check_code_teaching.py`** (§6.5), after two corrections the tool needed — it now sees unlabeled terminal sessions as code, and it matches keyword arguments only rather than every variable assignment, a bug this part reported:

| Ch | Code blocks | Blocks flagged | Ch | Code blocks | Blocks flagged |
|---|---|---|---|---|---|
| 35 | 26 | 14 | 40 | 27 | 22 |
| 36 | 26 | 19 | 41 | 27 | 22 |
| 37 | 32 | 29 | 42 | 23 | 19 |
| 38 | 25 | 19 | 43 | 25 | 20 |
| 39 | 27 | 20 | 44 | 9 | 6 |

Only Chapter 44, written under the standard, contains the settings table §6.5 requires. In Chapter 37 the flags fall mainly in the teaching body, not the exercise answers, and these settings are never named in its prose: `random_state`, `stratify`, `test_size`, `cv`, `n_neighbors`, `alphas`, `handle_unknown`, `strategy`, `add_indicator`. Nine of its blocks run over 25 lines, one at 76.

A flag is a question, not a verdict. Chapter 44's two long recap blocks are accepted deliberate exceptions.

## Open items

- **Chapter 44** needs the author's review.
- **Issue 13:** align Chapter 21's definitions of variance, standard deviation and probability distribution with Chapter 35 §35.7 and §35.10; if Ch 21 or 22 introduces the binomial and Poisson, Chapter 35 can shorten to a recap.
- **Issue 14:** Chapter 23 may reuse the CRM dataset and should point at `planning/data/riverstone-crm.md`.
- **Issue 15:** the style drift in Chapters 41–44.
- The part-completion review pass (§15.1) is due once Chapter 44 is approved. The settings tables are its substance, Chapter 37 first.

`planning/parts/part-4-coordinator-reply.md` has the full reply; `planning/parts/part-4-status.md` has the per-chapter reports.

## The rules every chapter follows

`planning/chapter-writing-instructions.md` is the master brief. Two sections matter most:

- **§6.5** — teach code and formulas line by line: the question in plain words, the plan before any code, short code, the real output and how to read it, then one bullet per line, plus a settings table with "what happens if you change it" and at least one measured what-if.
- **§15.1** — the part-completion review pass: read the part straight through as a reader would, work out the cause of each problem at the level of the part, and only then fix in place.

Riverstone Supplies is fictional. Every person, customer, product and number in the data is invented.
