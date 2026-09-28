# Chapter 18, Python for Analysts: pandas & Automation: summary (Part 2 build)

**Result:** 73 register rows touch Ch 18. All 59 `Approved` rows were handled: 48 content and 6 visual rows applied, 1 Reader's Journey row fixed (RJ-S3-22), and 4 Reader's Journey rows whose fix lies in other chapters or in the renumbering pass left `Approved` with a note. The 12 layout rows the style pass had already done were re-checked. The 2 `Open` rows (18.44, renumbering; RJ-S1-5, reading order) were left alone. Rebuilt PDF: 76 pages (was 36), `layout_check.py` clean (chapter map 22/22, no stranded headings or lead-ins, no sparse pages, no small text, tofu 0); `fig_check.py`: 4 figures, all text drawn as paths and measured by `make_figs18.py` at 8.2 pt or more; `restructure.py --check`: in order.

## What changed

- **It runs.** The three printed errors are gone: the pivot, the melt, and the Excel read-back now show their real results. Every one of the 106 Python outputs was regenerated from a real run and verified on Python 3.14.7 and on 3.11.15.
- **Taught like Jupyter.** The big blocks are split: loop against vectorized (2 cells), groupby by two keys (3), date repair (5), column fixes (4), the Excel workbook (4), and the 125-line script (6 functions, each run on December 2025 before the file is assembled). Every new method and argument is explained where it first appears, and the "what happens if you change it" cell shows which edge `pd.cut` includes.
- **Nothing used before it's taught.** `merge` is explained in §18.1; `lambda` gets its own subsection before `assign`; JSON moved to §18.14; one page of NumPy (arrays, dtype, `np.nan`, `np.where`, `np.select`) opens §18.1; status codes come before the first request; `logging`, `argparse` and `subprocess` are taught in §18.15, because the rebuilt Ch 17 no longer covers them.
- **Moved in, as approved.** Ch 14's pandas cleaning (§14.13's four profiling cells, the missing-values column, exercise 23, the second-quarter idea, the column comparison) is merged into §18.10, and each step points back to what Ch 14 did in SQL. Ch 15's chart code is rebuilt in §18.11 as step-by-step cells with Figure 18.1, `highlight_lines` becomes exercise 31 with a matching signature, and the 0.916 correlation is exercise 23. Ch 2's status-code rows go into §18.14.
- **A real API call.** `companion/ch18/api_demo.py` is a small local API that serves Riverstone's order lines with a token and pages. The reader runs requests, sees a real 401, pages through 296 lines, and runs a retry helper. It works offline.
- **Safe database code.** A `.env` file with `load_dotenv()` comes first. Environment variables and connection URLs are defined, and PowerShell and macOS/Linux instructions are given. There are no hard-coded passwords. The query has a MySQL version with real MySQL output. `to_sql` practice writes to a SQLite file, so nothing touches the shared database.
- **Consistent with Ch 15–16 and 19.** The regions come from Ch 16's 39-city table, with "City missing" shown in gray (₹38.4 / 31.9 / 27.9 / 14.2 / 2.3 crore). Size bands include the lower edge, as in Ch 19. The medians match Ch 15, and all rupee prose uses lakh grouping.
- **Figures.** Four charts now appear (there were none before), and each is exactly the output of the chapter's code.
- **Reader's folder.** The reader now works in `work/ch18`, following Ch 17's new layout, and reads data through `COMPANION = Path("../../companion")`.
- **Load.** There is a four-week sitting plan and a checkpoint at the end of each week.

## Skipped, and why

- **18.44** (Chapter 30 → 29 for "Python as Software"): held Open by the register for the renumbering pass; both references left as they are.
- **RJ-S1-5**: held Open by the register (reading-order row); not touched.
- **Screenshot** of the finished Excel workbook (18.29 suggests one per step): not possible without Excel. It is listed in the questions file for Abhishek to take.
- **18.39's build rule** (fail on printed tracebacks) is a tool change; it is passed to the integrator.

## Option picks

- 18.7 (a): explain `merge` in §18.1.
- 18.8 second option: move `lambda` to §18.6. Option (a) would have put a lambda box where lambda is no longer used.
- 18.9: NumPy goes inside §18.1, not in a new §18.2, so no section number changes.
- 18.11: the chart is built by hand before `style_axes`, not after it.
- 18.13: paging uses the live local API, not saved page files.
- 18.23: recommended `right=False`.
- 18.34 (a): a sixth check against last year, with a **50%** band. Real growth of 20–34% would fail a 20% band in 11 of 12 months, so the story now says 50%.

## Time needed

30–35 → **40–45 hours over four weeks**. The chapter grew from about 1,150 to about 3,150 source lines. It now includes the NumPy page, the moved Ch 14 and Ch 15 material, the API section, the stepwise script, `logging`, `argparse` and `subprocess`, four checkpoints, and seven new exercises. The review's own estimate for the smaller planned additions was 35–40 hours.

## Code verification

| Check | Result |
|---|---|
| `verify_python.py` on Python 3.11.15 | 106 blocks run, 106 outputs checked, **0 mismatches** |
| `verify_python.py` on Python 3.14.7 | 106 blocks run, 106 outputs checked, **0 mismatches** |
| `checks/ch18_extra_check.py` (MySQL cell, terminal run, script matches chapter, timing cells) | **0 mismatches** on both Pythons |
| `verify_shell.py` / `verify_sql.py` | no blocks to run (terminal blocks are `run: none`, checked by the extra check) |

The Python runs need `RIVERSTONE_DB`, `API_TOKEN=demo-token-18` and `api_demo.py` running, as the reader's setup does.

`check_code_teaching.py` flags 7 blocks. Six reuse ideas already taught earlier in the chapter (the styled chart, `region_table`, the script's imports and calls, the memory cell, and two answer cells). The seventh is `main()` at 29 lines. It only calls the five functions taught just before it, and every line is explained, so all seven are deliberate exceptions.
