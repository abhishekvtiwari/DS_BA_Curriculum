# Analyst to Architect — Part I: The Map — complete bundle

Chapters 7–9, **all approved**. About 30,800 words, 13 figures, 4 PDFs including the combined part book.

| Ch | Title | Status |
|---|---|---|
| 7 | The Data Landscape | Approved v1 |
| 8 | The Career Tree: How Skills Unlock Roles | Approved v1 |
| 9 | How Expertise Actually Forms | Approved v1 |

Part I shows the whole field before the reader starts climbing it: who does which data work, which skills open which doors, and how long expertise actually takes.

## Rebuilding

```
bash tools/setup_databases.sh companion        # riverstone_2025, used by Chapter 7's one query
cd figures && for f in make_figs0[789].py; do python3 "$f"; done
for f in checks/ch0[789]_check.py; do python3 "$f"; done
mysql -u root -t riverstone_2025 < companion/mysql/ch07_queries_mysql.sql
```

## Open items

- Salary figures (Chapter 8) and the Stack Overflow and World Economic Forum figures (Chapter 7) are on the pre-publication refresh list.
- Meera's story arc across Chapters 6, 7 and 8 (cross-part issue 6).

## What's where

| Folder | Contents |
|---|---|
| `manuscript/` | The chapters as Markdown (the source of truth for the text) |
| `pdf/` | One built PDF per chapter; `*-approved.pdf` is the approved version |
| `figures/` | `fig*.svg` as used in the PDFs, `png/` renders for slides, and the `make_figs*.py` scripts that draw them |
| `companion/` | Everything a reader downloads for these chapters |
| `checks/` | Number-check scripts: every figure quoted in the text is recomputed from the data |
| `tools/` | The verifiers (`verify_sql.py`, `verify_python.py`, `verify_shell.py`, `check_code_teaching.py`), `setup_databases.sh`, and the PDF builder |
| `planning/` | Chapter map, progress tracker, writing instructions, Riverstone bible additions, cross-part issues, pre-publication refresh list |
| `planning/parts/` | This part's brief and status file |

## Reading order versus chapter numbers

Chapters keep the numbers they were written with; the coordinator renumbers the whole book in one pass at final assembly. The mapping is at the top of `planning/chapter-map.md`.

## The rules every chapter follows

`planning/chapter-writing-instructions.md` is the master brief. Two sections matter most:

- **§6.5** — teach code and formulas line by line: the question in plain words, the plan before any code, short code, the real output and how to read it, then one bullet per line, plus a settings table with "what happens if you change it" and at least one measured what-if.
- **§15.1** — the part-completion review pass: when a part's last chapter is approved, read it straight through as a reader would, work out the cause of each problem at the level of the part, and only then fix in place.

Riverstone Supplies is fictional. Every person, customer, product and number in the data is invented.
