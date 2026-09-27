# Analyst to Architect — complete working package

Everything written so far for the book, as of **19 September 2026**: 31 chapters, about **394,000 words**, 32 chapter PDFs, 135 figures, the full Riverstone companion dataset, every verification script, and all planning files.

**Delivered as three zips** (an upload size limit), which unpack into the same folder:

1. `Analyst-to-Architect-Complete-Book-bundle-1-of-3-manuscript-and-planning.zip` — `manuscript/`, `planning/`, `figures/`, `checks/`, `tools/`
2. `Analyst-to-Architect-Complete-Book-bundle-2-of-3-companion-data.zip` — `companion/`
3. `Analyst-to-Architect-Complete-Book-bundle-3-of-3-pdfs.zip` — `pdf/`

Single parts are also packaged on their own, each complete and self-contained: `Analyst-to-Architect-Part-0-complete-bundle.zip`, `-Part-I-`, `-Part-II-`, `-Part-III-`.

Riverstone Supplies is fictional. Every person, customer, product and number in the data is invented.

## Where the book stands

| Part | Chapters | Words | Status |
|---|---|---|---|
| **Part 0 — First Principles: Data from Zero** | 1–6 | 53,805 | Complete, all approved |
| **Part I — The Map** | 7–9 | 30,794 | Complete, all approved |
| **Part II — The Analyst** | 10–24 | 217,413 | 15 of 18 written; **25, 26, 27 not started**. Ch 12 v4 awaiting approval |
| **Part III — Advanced Analytics & Analytics Engineering** | 28–34 | 92,063 | Complete; 6 approved, **Ch 29 v1.1 awaiting review** |
| Parts IV–VIII and the appendices | 35–83 | — | Not started |
| **Total written** | **31 chapters** | **394,075** | |

The plan is 83 chapters and about 497,000 words (`planning/blueprint.md`).

## What's in each folder

| Folder | Contents |
|---|---|
| `manuscript/` | All 31 chapters as Markdown. This is the source of truth for the text |
| `pdf/` | One built PDF per chapter. `*-approved.pdf` is the approved version; `*-for-review.pdf` is waiting on the author (Ch 12 v4, Ch 29 v1.1) |
| `pdf/parts/` | The combined part books built so far: Part 0 and Part I |
| `figures/` | 135 figures as SVG, `png/` renders for slides, and the `make_figs*.py` scripts that draw them |
| `companion/` | Everything a reader downloads: the Riverstone datasets, generators, SQL setup scripts for PostgreSQL and MySQL, workbooks, messy exports, cleaning pipelines, the dbt project, the Python package |
| `checks/` | One number-check script per chapter, plus helpers and timing logs |
| `tools/` | The four verifiers (`verify_sql.py`, `verify_python.py`, `verify_shell.py`, `check_code_teaching.py`), `setup_databases.sh`, `extract_promises.py`, and the PDF builder |
| `planning/` | The blueprint (Markdown and PDF), chapter map, progress tracker, writing instructions, Riverstone bible additions, cross-part issues, promises, pre-publication refresh list |
| `planning/parts/` | One brief and one status file per part, plus the coordinator's replies |

## Reading order versus chapter numbers

Chapters keep the numbers they were written with. Parts II and III were reordered on 17 September 2026 so each tool is learned end to end before the next begins; **the renumbering happens in one pass at final assembly**. The mapping is at the top of `planning/chapter-map.md`. In short:

- **Part II:** 10 → 11 → 19 → 12 → 13 → 17 → 18 → 14 → 15 → 16 → 20 → 21 → 22 → 23 → 24
- **Part III:** 28 → 34 → 29 → 32 → 33 → 30 → 31

## The Riverstone databases

| Database | Covers | Used by |
|---|---|---|
| `riverstone` | the mini Q1 2026 slice | Chapter 12 |
| `riverstone_lab` | built by the reader | Chapter 12 §12.13 |
| `riverstone_2025` | one year, the key accounts' 2025 data | Chapters 13, 28, 29 |
| `riverstone_full` | three years, 2023–2025, the whole company | Chapters 14–24 |
| `riverstone_perf` | a synthetic volume dataset, **not canon** | Chapter 28's performance work |
| the digital domain, the causal datasets | website sessions and A/B test; three observational datasets | Chapters 30, 31 |

## Rebuilding everything

```
# 1. datasets (all generators are seeded, so the numbers match the chapters exactly)
cd companion && python3 generate_riverstone_2025.py && python3 generate_riverstone_full.py
cd ch30 && python3 generate_riverstone_web.py
cd ../ch31 && python3 generate_ch31_data.py
cd ../ch28 && python3 generate_riverstone_perf.py

# 2. databases
bash tools/setup_databases.sh companion            # riverstone, riverstone_2025, Ch 28 add-ons, star schema
createdb riverstone_full && psql -d riverstone_full -f companion/full/riverstone_full_setup_postgresql.sql
mysql --local-infile=1 -u root -p < companion/full/riverstone_full_setup_mysql.sql
createdb riverstone_perf && psql -d riverstone_perf -f companion/ch28/perf_data/load_postgresql.sql

# 3. per-chapter companion files
cd companion/ch14 && python3 build_ch14_files.py   # and the same in ch10, ch11, ch15, ch17…ch24, ch34

# 4. figures
cd figures && python3 make_figs.py && for f in make_figs1*.py make_figs2*.py make_figs3*.py; do python3 "$f"; done

# 5. verify a chapter
python3 tools/verify_sql.py    manuscript/ch13-sql-for-real-analysis.md --db riverstone_2025
python3 tools/verify_python.py manuscript/ch18-python-for-analysts-pandas-and-automation.md --cwd companion/ch18
python3 tools/verify_shell.py  manuscript/ch34-the-command-line-linux-and-networking-basics.md --cwd <copy of companion/ch34> --user <a normal user>
python3 tools/check_code_teaching.py manuscript/ch18-python-for-analysts-pandas-and-automation.md
for f in checks/ch*_check.py; do python3 "$f"; done

# 6. build a PDF
cd tools/pdf && python3 build_chapter.py ../../manuscript/ch13-sql-for-real-analysis.md \
  --figures ../../figures --out-dir ../../pdf --name Ch13 --part "Part II — The Analyst" \
  --title "Chapter 13. SQL for<br>Real Analysis" --sub "..." --doc "Approved chapter v1.1" --meta "..."
```

Generated data is **not** included where it is large (Chapter 28's `riverstone_perf`, Chapter 30's web data). Every generator is deterministic, so rebuilding reproduces the exact numbers printed in the chapters.

Tested with Python 3.12, PostgreSQL 16, MySQL 8.0.46, LibreOffice 24.2 and Playwright.

## What needs the author

1. **Chapter 12 v4** — approve or reject the added §12.13, the hands-on lab where the reader builds and changes their own database. v3 is the approved version; both PDFs are in `pdf/`.
2. **Chapter 29 v1.1** — review, and decide cross-part issue 9: whether Chapter 29 should refactor Chapter 18's real script instead of its own deliberately poor one.
3. **Cross-part issue 3** — the two-channel sales structure (a Key Accounts team alongside the regional teams). Already built into the data; needs a one-line edit to Chapter 5 once approved.
4. **Chapters 25, 26, 27** — the last of Part II; no chat is writing them yet.
5. **A repository.** The project's knowledge store is close to its limit, so only planning files live there. This package is the whole book; putting it in GitHub would let every part chat read and write the same files instead of passing zips.

`planning/cross-part-issues.md` has all twelve issues with proposed resolutions and owners; `planning/progress-tracker.md` has the full decisions log.

## The rules every chapter follows

`planning/chapter-writing-instructions.md` is the master brief: the 14-section chapter template, depth classes, voice and style rules, verification methods, and the Definition of Done. Two sections matter most for what comes next:

- **§6.5 — teach code and formulas line by line.** The question in plain words, the plan before any code, short code, the real output and how to read it, then one bullet per line. A settings table with "what happens if you change it", and at least one measured what-if. Enforced by `tools/check_code_teaching.py`.
- **§15.1 — the part-completion review pass.** When a part's last chapter is approved, read the part straight through as a reader would, work out the cause of each problem at the level of the part, and only then fix in place. A checker flag is a pointer to a place to read, never a reason on its own to edit.
