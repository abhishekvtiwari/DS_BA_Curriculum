# Analyst to Architect — complete manuscript

Snapshot of 21 September 2026. **All 85 chapters are written and approved.**

## What is here

| Folder | Contents |
|---|---|
| `manuscript/` | 85 chapters as Markdown, plus the two assembled part files for Parts 0 and I |
| `figures/` | every figure as SVG (and PNG where a chapter needs one), and the `make_figsNN.py` script that draws each set |
| `companion/` | all practice data: the three Riverstone databases, the per-chapter companion files, and the generator scripts that reproduce every row |
| `checks/` | the per-chapter verification scripts |
| `sql/` | setup and query files |
| `planning/` | the blueprint, the chapter map, the writing instructions, every part brief and status report, the cross-part issue log, and the go-to-market and coherence-pass strategies |
| `tools/` | the four verifiers, the code-teaching checker, the promise extractor, the database setup script, and the PDF builder |

## The state of the book

- **85 chapters, about 855,000 words.** Parts 0 through VIII plus the closing chapter.
- Every chapter is approved. Chapters 25, 26, 27 and 83 were written last, in the coordinator chat, and complete the book.
- **Numbers are still provisional.** At the renumbering pass the book becomes 85 chapters with Part VIII running 68 to 84 and The Long Game as Chapter 85. Chapter files keep their current numbers until then. See `planning/chapter-map.md` and cross-part issue 24.

## What is not here yet

The appendices, A through H. `planning/parts/part-closing-appendices-brief.md` has the specification. Appendix G, the answers, is about 95,000 words that already exist inside the chapters and should be moved by script at assembly rather than rewritten.

## Reproducing anything

```
# load the databases
bash tools/setup_databases.sh

# verify a chapter's SQL, Python and terminal output against real runs
python3 tools/verify_sql.py    manuscript/ch13-sql-for-real-analysis.md --db riverstone_2025
python3 tools/verify_python.py manuscript/ch27-capstone-your-analyst-portfolio.md --cwd companion/ch27
python3 tools/verify_shell.py  manuscript/ch34-the-command-line-linux-and-networking-basics.md

# check a chapter against the section 6.5 code-teaching standard
python3 tools/check_code_teaching.py manuscript/ch26-*.md

# redraw a chapter's figures
cd figures && python3 make_figs27.py

# build a chapter PDF
python3 tools/pdf/build.py ch27
```

Every number, query result and terminal transcript in the book was produced by running the thing shown. The verifiers are how that stays true.
