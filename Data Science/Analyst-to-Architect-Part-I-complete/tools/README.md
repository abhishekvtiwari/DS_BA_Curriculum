# Shared tools — Analyst to Architect

Used by every part chat. See `planning/chapter-writing-instructions.md`, section 9. Maintained by the coordinating chat only.

| Tool | What it does | Tested on |
|---|---|---|
| `setup_databases.sh <companion-dir>` | Loads the `riverstone` and `riverstone_2025` practice databases, plus the `sales_lines` view, into PostgreSQL and MySQL | PostgreSQL 16, MySQL 8.0.46 |
| `verify_sql.py chapter.md` | Runs every `sql` block in PostgreSQL and every `mysql` block in MySQL (including stateful lab regions) and compares with the printed outputs | Ch 12: 123 outputs, Ch 13: 44 outputs, 0 mismatches |
| `verify_python.py chapter.md --cwd companion/chNN` | Runs every `python` block in order in one namespace and compares with the printed outputs | sample chapter file |
| `extract_promises.py manuscript/ch*.md` | Lists every "Chapter N …" forward reference made by written chapters | Ch 1, 2, 12, 13 |
| `pdf/build_chapter.py` | Builds the styled chapter PDF (cover + body) from a manuscript; needs `book.css`, `template.html`, `cover.html` beside it, pandoc, Playwright (Chromium), pypdf, and the Poppins and Lora fonts | Ch 2: 27 pages, identical to the approved PDF |

Figure helpers live in `figures/make_figs.py` (tables, schema boxes, palette) and `figures/make_figs01.py` (`wrap` for multi-line text); each chapter adds its own `figures/make_figsNN.py`.
