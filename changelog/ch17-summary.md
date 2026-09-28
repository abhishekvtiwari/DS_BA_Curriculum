# Chapter 17, Python from Zero: summary of the Parts 2–3 build

**Findings:** 42 content rows and 7 open visual rows for Ch 17, plus 5 multi-chapter Reader's Journey rows. 47 Verified and 1 Fixed (17.26, moved out to Ch 20), 1 held Open by the register (17.31), 3 multi-chapter rows done for Ch 17 and left Approved for other chapters (RJ-S2-7, RJ-S3-18, RJ-S3-31), and 2 RJ rows held Open (RJ-S1-5, RJ-S3-10). The layout pass had already closed V17.5–V17.10, V17.13–V17.15, V17.17 and V17.18.

## What changed

- **New §17.0 "Setting up Python, the terminal and Jupyter"** (Chapter 6 now installs nothing). It covers a minimal terminal (`pwd`, `ls`, `cd`, `cd ..`, Tab, ↑, Ctrl+C, quotes), Python 3.14 on each system, VS Code and its two extensions, and one `.venv` for the book. Every command is explained, including `-m`, activation per shell, the PowerShell execution-policy fix, `python -m pip`, `pip freeze > requirements.txt` and `deactivate`. Then `check_setup.py` shows one passing run and one failing run, and a first notebook runs `Hello, Riverstone` and `22`. Old §17.2–17.3 were merged into it, so the sections are renumbered: 17.0–17.13.
- **Rebuilt as notebook cells.** Nearly every block now teaches one idea, with its real output and an explanation of every part. The order is now variables → lists → conditions → loops → dictionaries, so nothing is used before it's taught. Methods, attributes, `+=`, keyword arguments, `:<10`/`:>7,`/`:,.0f`, `repr`, `start=2`, dictionary comprehensions, `from … import` and standard deviation (pointer to Ch 21) are each defined where they're first used. Six "Stop here" sittings are marked.
- **Parked from Ch 2 and Ch 6:** 0.1 + 0.2, the exact `Decimal` version, and how 2.5 rounds (`round()` vs spreadsheet `ROUND`), with the Python documentation's quotes (§17.3). Also the install steps, `check_setup.py`, Meera's setup episode and five old Ch 6 exercises.
- **§17.12 "From notebook to script"** now builds `summarize_exports.py` in VS Code in four stages. Each stage is run in the terminal, with `show_args.py`, `sys.argv`, `__name__`, `raise SystemExit`, and exit codes 0 and 1 (`echo $?`, `$LASTEXITCODE`). The `subprocess`/string-script approach is gone.
- **Moved out (→ Ch 20, `manuscript/_parked/ch17-moved-out.md`):** logging, `argparse`, and old stretch exercises 23–24. Ch 17 keeps one sentence.
- **Figures 17.1–17.3 redrawn** on 640 px canvases, with all text at 7.2 pt or more. Figure 17.1's arrow now runs from the notebook to the script. Figure 17.3 is a real traceback that keeps its indentation, with numbered markers and a key. The table that repeated Figure 17.2 is gone.
- **Consistency:** the real-world story now has 13 files and one duplicate worth ₹1.4 crore. Parts 3 to 5 are cited. Level 5 asks for 23 customers with non-cancelled revenue. The `=`/`==` symptom is fixed. Rupee amounts in the text use lakh grouping. The Appendix G note and the build script's name are gone from reader text.

## Option picks

17.12 (a) move Loops before Dictionaries · 17.15 (a) add the float note · 17.18 (a) use 284,530.75 · 17.29 (a) 12 files plus a thirteenth · V17.2 (a) redraw · V17.12 keep the figure, drop the table.

## Skipped, and why

- **17.31** ("Chapter 30" → 29): held Open in the register because the renumbering makes "Python as Software" Chapter 30. Both references are unchanged and listed for the final pass.
- **RJ-S1-5, RJ-S3-10:** held Open (reading-order rows). The Ch 17 half of RJ-S3-10 (credit Ch 19's VBA) is a question for Abhishek.
- **Exercise 2(c) from Ch 6:** not landed. It's a cross-tool matching exercise, and only its Python part would fit here.

## Time needed

It was 25–30 hours; it's now **28–32 hours**: about 2 hours of setup (§17.0), then five sittings of five or six hours each. Logging and argparse moving to Ch 20 saves about an hour, and the extra cells and explanations add about three.

## Code verification

- `verify_python.py`: 85 blocks run, 83 outputs checked, **0 mismatches**, on Python 3.14.7 and on 3.11.15.
- `verify_shell.py`: 20 commands, **0 mismatches**.
- `checks/ch17_check.py`: **0 problems**. It checks the 4 script stages, 3 terminal runs, the REPL session, 2 notebook cells, the Jupyter traceback, `requirements.txt`, Figure 17.3's traceback and 20 answer figures.
- The PDF has 61 pages. `layout_check.py` is clean (map 20/20, no stranded headings or lead-ins, no sparse pages, no small text, tofu 0). `fig_check.py` reports 0 figures under 7 pt. `restructure.py --check` reports the chapter already in order.
- Run these in the reader's folder built by `checks/ch17_setup_workdir.sh`, because the `Path.cwd()` cell prints `/home/meera/analyst-to-architect/work/ch17`. From a bare `companion/ch17` copy that one cell mismatches.
- Library versions: JupyterLab 4.6.4, ipykernel 7.3.0, pip 26.2.1.
