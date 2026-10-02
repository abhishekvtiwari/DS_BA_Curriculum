# Review export

Three small tools for getting a section of the book in front of a reviewer, and for checking SQL
answers before they are written down.

These are **not** part of the book build. The book builds with pandoc to HTML and then Playwright
to PDF (`Data Science/Analyst-to-Architect/tools/pdf/build.py`). Pandoc is not installed in every
environment, and a reviewer usually wants one section rather than a 400-page book, so these take a
narrower path.

## `export_section.py` — one section as DOCX and PDF

```bash
python tools/review-export/export_section.py \
  "Data Science/Analyst-to-Architect/manuscript/ch71-sql-question-bank.md" \
  "## 71.11" "## Common mistakes" \
  "review/for-abhishek/Ch71-section-71.11-predict-the-output"
```

Takes the chapter file, the heading to start at, the heading to stop before, and an output stem.
Writes `<stem>.html` and `<stem>.docx`. Run `html_to_pdf.py` on the HTML for the PDF.

It parses the Markdown directly and handles what the question banks use: headings, paragraphs with
bold, italic and inline code, fenced code blocks, pipe tables, bullet lists and rules. Two details
are deliberate:

- **Code spans are protected before emphasis is matched.** The book's code contains asterisks —
  `count(*)`, `SELECT *` — and matching `*italic*` first tears those apart.
- **A line opening with a bold lead-in starts its own paragraph**, so *Likely follow-ups*, *Red
  flag* and *Learn it in* stay on separate lines instead of running together.

Output blocks (a fence with no language) are tinted differently from SQL blocks, so a reviewer can
tell a query from its result at a glance.

## `html_to_pdf.py` — print the HTML

```bash
python tools/review-export/html_to_pdf.py <in.html> <out.pdf>
```

Playwright/Chromium, A4, with a footer carrying the page number. Needs `playwright` and its
Chromium download.

## `load_riverstone_2025_duckdb.py` — a bench for checking SQL answers

```bash
python tools/review-export/load_riverstone_2025_duckdb.py bench.duckdb
```

Loads `companion/riverstone_2025_setup.sql` into DuckDB and then checks four figures Chapter 71
already prints — 11 NULL `sales_rep_id`, the `NOT IN` trap answering 0, the corrected answer 2, and
1 of 24 customers with no orders. If those four do not match, it says so and the bench should not
be trusted.

`FOREIGN KEY` clauses are stripped on the way in, because DuckDB checks a foreign key as each row
is inserted and the self-referencing `employees.manager_id` fails there although PostgreSQL accepts
it.

**This is a convenience, not a substitute.** DuckDB follows PostgreSQL's semantics for most of what
these chapters test, but not all of it: it does not truncate integer division, and it differs on
division by zero. Anything where the engines might disagree still needs a run on PostgreSQL 16 and
MySQL 8.4 before it goes in the book, and until then it is labelled as unconfirmed rather than
Verified. Section 71.11 is in exactly that state; see `changelog/ch71.md`.
