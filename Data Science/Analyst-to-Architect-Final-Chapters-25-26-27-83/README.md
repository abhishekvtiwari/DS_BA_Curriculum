# The four final chapters — 25, 26, 27 and 83

Written in the coordinator chat, 21 September 2026. **All four are approved.** With these, every chapter of *Analyst to Architect* exists: 85 chapters, about 855,000 words.

| Chapter | Words | Pages | What it is |
|---|---|---|---|
| **25. The Business Analyst Track** | 11,996 | 29 | v2, re-aimed at the data domain: BA against data analyst, data scientist and data engineer; data non-functional requirements; the four things a data team is asked to build |
| **26. The Professional Toolkit** | 11,952 | 33 | Git, GitHub and pull requests, the four undos, secrets, one automated check, a README a stranger can follow, Agile and Jira, and working with an AI assistant |
| **27. Capstone: Your Analyst Portfolio** | 12,562 | 31 | One question from database to memo, the check that turns a flattering finding into an honest one, and the portfolio half: selective reporting, the ninety-second scan, telling the story |
| **83. The Long Game** | 6,531 | 17 | The arithmetic of the climb, the pace that survives a bad month, choosing your own summit, and the four plateaus that arrive after the first job |

## Contents

| Folder | Contents |
|---|---|
| `manuscript/` | the four chapters as Markdown |
| `figures/` | 13 figures as SVG, the four `make_figsNN.py` scripts that draw them, and the two shared helpers |
| `pdf/` | one PDF per chapter |
| `companion/ch27/` | `discount_report.py`, the script Chapter 27 teaches. Run it from `companion/full` |
| `planning/` | the status report with the full write-up of each chapter, the brief they were written from, the updated chapter map, the cross-part issue log, and the patched code-teaching checker |

## Three things worth knowing

**Everything was run.** Chapter 26's terminal sessions come from a real Git repository built with fixed commit dates so the hashes reproduce. Chapter 27's SQL was run against the three-year database in PostgreSQL 16 and its Python against the CSVs; `verify_sql.py` reports 4 of 4 outputs matching and `verify_python.py` 3 of 3. Chapter 83's hour totals were computed from the book's own chapter estimates.

**Chapters 26 and 27 are the only two chapters in the book that meet the section 6.5 code-teaching standard in full:** settings tables with a "what happens if you change it" column, and a measured what-if. The baseline in `planning/code-teaching-baseline.md` found one chapter in 81 with that table. These are the second and third.

**One tool was fixed.** `check_code_teaching.py` reported any two-letter keyword argument (`on=`, `by=`, `ax=`) as unexplained and could never do otherwise, because its identifier pattern requires three characters. The patched version is in `planning/`; it belongs at `tools/check_code_teaching.py`.

## Still open

The appendices, A through H. The brief is in `planning/final-chapters-brief.md` and in `part-closing-appendices-brief.md` in the full bundle. **Appendix G, the answers, is about 95,000 words that already exist inside the chapters** and should be moved by script at assembly rather than rewritten.

Cross-part issue 20 is now ready to apply: Chapter 67 still claims to be the final chapter and misnames Part VIII. The five exact replacements are written out at the end of `planning/cross-part-issues.md`.
