# Analyst to Architect — Part II: The Analyst — complete working bundle (19 September 2026)

Every chapter of Part II written so far: **Chapters 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 and 24**, with manuscripts, PDFs, figures (source and rendered), companion data and the scripts that generate it, verification tools and checks, and the merged status file.

This replaces the Part II-A bundle of 17 September. What is new here: **Chapters 12 and 13 (the SQL chapters), which were written in the coordinator chat**, plus the merged Part II status file and the packaging checks below. Riverstone Supplies is fictional; every name and number in the data is invented.

## Reading order (decided 17 September 2026)

Chapters keep their current numbers while writing; the coordinator renumbers the whole book in one pass at final assembly. The **teaching order** is:

| Block | Order |
|---|---|
| A. Spreadsheets, end to end | 10 → 11 → 19 |
| B. SQL, end to end | 12 → 13 |
| C. Python, end to end | 17 → 18 |
| D. All tools together | 14 → 15 → 16 → 20 |
| E. Judgment | 21 → 22 → 23 → 24 |

Each tool is learned end to end, including its automation, before the next tool starts, so that nothing uses pandas before Python is taught or VBA before its own programming basics are covered.

**Still unwritten:** Chapter 25 (The Business Analyst Track), Chapter 26, Chapter 27.

## What's where

| Folder | Contents |
|---|---|
| `manuscript/` | The 15 chapters as Markdown (the source of truth for the text) |
| `pdf-out/` | Built PDFs. `*-approved.pdf` are the current approved versions. `Ch12-…-v4-for-review.pdf` is the one chapter not yet re-approved (see Open items) |
| `figures/` | `make_figs*.py` draw the figures; `fig*.svg` are the figures used in the PDFs; `png/` holds PNG renders for quick viewing or pasting into slides |
| `companion/full/` | The full Riverstone dataset 2023–2025 (CSV + Parquet + PostgreSQL and MySQL setup scripts) and `DATA_SPEC.md` |
| `companion/postgresql/`, `companion/mysql/` | Database setup and chapter query files for both engines, including the Chapter 12 lab scripts |
| `companion/chNN/` | Per-chapter workbooks, exports, mapping tables, pipelines and the scripts that build them |
| `checks/` | Verification scripts: dataset checks, per-chapter expected values, and comparison scripts |
| `tools/` | `verify_sql.py`, `verify_python.py`, `check_code_teaching.py`, and the PDF builder |
| `planning/parts/part-2-status.md` | The merged status file: approvals, chapter reports, manual checks still open, data specs, coordinator notes |

## Which database each chapter uses

| Chapters | Database |
|---|---|
| 12 | `riverstone` (the mini Q1 2026 slice) and `riverstone_lab` (built by the reader in §12.13) |
| 13 | `riverstone_2025` (the one-year dataset) |
| 14–24 | `riverstone_full` (the three-year dataset, 2023–2025) |

## Rebuilding anything

```
# 1. the datasets
cd companion && python3 generate_riverstone_2025.py && python3 generate_riverstone_full.py

# 2. the SQL chapters' databases
createdb riverstone      && psql -d riverstone      -f postgresql/riverstone_setup.sql
createdb riverstone_2025 && psql -d riverstone_2025 -f postgresql/riverstone_2025_setup.sql
mysql -u root < mysql/riverstone_setup_mysql.sql
mysql -u root < mysql/riverstone_2025_setup_mysql.sql

# 3. the full dataset (from companion/full)
createdb riverstone_full && psql -d riverstone_full -f riverstone_full_setup_postgresql.sql
mysql --local-infile=1 -u root -p < riverstone_full_setup_mysql.sql

# 4. per-chapter companion files
cd companion/ch14 && python3 build_ch14_files.py      # and the same in ch10, ch11, ch15, ch17…ch24

# 5. Chapter 14's staging tables and cleaning pipeline
psql -d riverstone_full -f companion/ch14/sql/ch14_load_postgresql.sql \
                        -f companion/ch14/sql/ch14_clean_postgresql.sql

# 6. figures
cd figures && python3 make_figs.py && for f in make_figs1*.py make_figs2*.py; do python3 $f; done

# 7. verify a chapter
python3 tools/verify_sql.py manuscript/ch13-sql-for-real-analysis.md --db riverstone_2025
python3 tools/verify_python.py manuscript/ch14-data-cleaning-and-preparation.md --cwd companion/ch14
python3 tools/check_code_teaching.py manuscript/ch18-python-for-analysts-pandas-and-automation.md

# 8. build a PDF
cd tools/pdf && python3 build_chapter.py ../../manuscript/ch13-sql-for-real-analysis.md \
  --figures ../../figures --out-dir ../../pdf-out --name Ch13 --part "Part II — The Analyst" \
  --title "Chapter 13. SQL for<br>Real Analysis" --sub "..." --doc "Approved chapter v1.1" --meta "..."
```

Note: the MySQL companion files must be run against the right database, for example
`mysql -u root -t riverstone_2025 < companion/mysql/ch13_queries_mysql.sql`.

Tested with Python 3.12 (pandas 3.0.2, pyarrow, openpyxl, matplotlib 3.10, playwright), PostgreSQL 16.15,
MySQL 8.0.46, LibreOffice 24.2 (for the spreadsheet checks in Chapters 10, 11 and 19).

## Packaging checks run on this merged bundle

- All 71 figure references across the 15 chapters resolve to a file in `figures/`.
- Every companion file named in the chapters is present, with one naming mismatch: Chapter 16 refers to `ch16_checks.sql`, while the folder holds `ch16_checks_postgresql.sql` and `ch16_checks_mysql.sql`.
- Independent style scan of all 15 chapters (code blocks, tables, figure captions and the part line excluded): Chapters 10, 11, 14, 15 and 17 are clean; Chapters 12, 16, 18, 19, 20, 21, 22, 23 and 24 carry em dashes in prose, American-spelling fixes, or the word *genuinely*. Counts are in the status file. These are held for the part-completion review pass, not fixed here.

## Open items

- **Chapter 12 v4 is not approved.** v3 is the approved version; v4 adds §12.13 "Building and changing a database" (`CREATE`, `INSERT`, `UPDATE`, `DELETE`, `ALTER`, `DROP` in a separate `riverstone_lab` database) and exercises 23–29. Both PDFs are in `pdf-out/`.
- Chapter 13 needs one sentence saying what the one-year `riverstone_2025` database represents now that the three-year dataset exists.
- Manual checks for Chapters 10 (14), 11 (20), 14 (5), 15 (4) and the later chapters are listed in the status file.
- Author decision still open on the sales structure (a Key Accounts team alongside regional teams), which would change the sales rep on regional orders and four rep-level items in Chapter 15. No revenue figure would change.
- The style and code-teaching findings above are the input to the Part II review pass described in `planning/chapter-writing-instructions.md` §15.1.
- Chapters 25, 26 and 27 are not written.
