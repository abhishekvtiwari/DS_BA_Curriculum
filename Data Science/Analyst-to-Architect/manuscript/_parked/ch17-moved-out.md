# Parked: text moved out of Chapter 17 (Parts 2 and 3 build, 28 Sep 2026)

Not a book chapter and not built. Each block below was cut from Chapter 17 (Python from Zero) by finding 17.39 ("Move `logging` (and argparse, Stretch 23–24) to Ch 20, which already covers 'logging properly', keeping one sentence here") and is kept verbatim, labelled with its destination. Ch 17 now keeps one sentence in section 17.12 that points to Chapter 20 for `logging` and `argparse`. The destination chapter's agent places each block (rewritten to pass the seven tests there) and reports it.

---

## Block 1 → Ch 20 (Automating Reports & Delivering Insights), its logging section (§20.11 "Logging and run history")

**Landed** in Ch 20 §20.11, "Logging and run history", with the 17.26 output fix (Part 2/3 build). Ch 18 §18.15 now introduces `logging` first, and Ch 20 recaps it.

Cut from Ch 17 §17.14 "From notebook to script" (now §17.12). **Finding 17.26 applies wherever this lands:** the output shown is wrong. `basicConfig` sends the two log lines to stderr, and both a terminal and Jupyter show them (`HH:MM:SS INFO starting`, `HH:MM:SS WARNING 3 rows could not be read`), so the real output has three lines, not one. In a notebook, `basicConfig` can also do nothing if the kernel has already configured logging (use `force=True`). Run it as a small script from the terminal and paste the real output, or use `force=True` in a notebook; explain each `basicConfig` argument (`level`, the `format` placeholders `%(asctime)s`, `%(levelname)s`, `%(message)s`, `datefmt`) and `getLogger`. Ch 20 §20.11 has a block with the same pattern and the same output problem.

### Logging instead of printing

`print()` is fine while you're watching. A script that runs at 6 a.m. should write to a log:

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("summary")
log.info("starting")
log.warning("3 rows could not be read")
print("(the log lines above go to stderr, so they don't mix with the report on stdout)")
```

```
(the log lines above go to stderr, so they don't mix with the report on stdout)
```

Logging gives you levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`), timestamps, and the option to write to a file instead of the screen, all without changing the code that calls it.

---

## Block 2 → Ch 20, exercises (Stretch) and their answers

**Landed** in Ch 20 as Stretch exercises 25 (`argparse`) and 26 (`logging`) with answers (Part 2/3 build).

Cut from Ch 17's Stretch exercises (old numbers 23 and 24) and their answers. Ch 17's remaining exercises were renumbered. Exercise 23's script is the one Ch 17 §17.12 builds (`summarize_exports.py`, now in `companion/ch17/`), so in Ch 20 it can say "Chapter 17's `summarize_exports.py`".

23. Turn your folder summary into a script with `argparse`: `python summarize.py sales_exports --month 2025-10 --output summary.md`. Include a docstring, functions, and an exit code.
24. Add `logging` at INFO level to the script: one line when it starts, one per file processed, one warning per unreadable row, one line with the total at the end.

**23.** The script needs a module docstring, `argparse` with a positional `folder` and optional `--month` and `--output`, functions for reading and summarizing, `if __name__ == "__main__":`, and `raise SystemExit(main(args))` so the exit code reaches the shell.

**24.** `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")`, then `log.info("reading %s", path)` per file and `log.warning("row %s unreadable: %r", line_no, value)` for bad rows. Use `%s` placeholders rather than f-strings in logging calls, so the formatting happens only if the message is actually emitted.

---

## Block 3 → Ch 20, with Block 2 (a project stretch goal)

**Landed** in Ch 20 exercise 25 (the `--month` option) and §20.7 (Part 2/3 build).

Cut from Ch 17's project "Stretch goals" list:

- Add a `--month 2025-10` option with `argparse` that summarizes one month.

And from the bullet list after the script in old §17.14 (Ch 17 now says "Arguments from `sys.argv`, with a sensible default"), the `argparse` clause:

> - **Arguments** come from `sys.argv` (or the `argparse` module for anything more than one), with a sensible default. Nothing is hard-coded to your laptop.

Key terms removed from Ch 17 with these blocks: `logging` · `argparse` (Ch 20's Key terms should carry them).
