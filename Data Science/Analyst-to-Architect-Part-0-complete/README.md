# Analyst to Architect — Part 0: First Principles: Data from Zero — complete bundle

Chapters 1–6, **all approved**. About 53,800 words, 23 figures, 7 PDFs including the combined part book.

| Ch | Title | Status |
|---|---|---|
| 1 | What Is Data? | Approved v1 |
| 2 | How Computers Store, Move and Protect Data | Approved v1 |
| 3 | How a Business Runs on Data | Approved v1 |
| 4 | Numbers Without Fear | Approved v1 |
| 5 | Thinking Like an Analyst | Approved v1 |
| 6 | Setting Up to Learn | Approved v1 |

Part 0 takes a reader with no background at all to the point where they can install the book's tools, read a number honestly, and frame a question an analyst would recognize.

## Rebuilding

```
bash tools/setup_databases.sh companion        # the mini riverstone database
cd companion/ch04 && python3 make_ch04_workbook.py
cd ../ch06 && python3 check_setup.py
cd ../../figures && for f in make_figs0*.py; do python3 "$f"; done
for f in checks/ch0*_check.py; do python3 "$f"; done
```

## Open items

- Chapter 5 v1.1: one line on the sales team, once the two-channel sales structure is approved (cross-part issue 3).
- Chapter 6 v1.1: Meera's story arc and the SQL hours in the six-month plan (issues 6 and 7).
- Chapter 6's tool versions are on the pre-publication refresh list.

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
