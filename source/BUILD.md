# How the book builds

Written 28 September 2026, from reading the tooling and rewiring it. **No build has been run**,
because `pandoc` and a Chromium for Playwright are not installed in the machine this was set up on.
Everything below is verified by inspection and by import, not by producing a PDF. The first session
with the toolchain installed should build Ch 12 and correct anything here that turns out wrong.

The sources are not in `source/`. They are at `Data Science/Analyst-to-Architect/`, and
[`SOURCES-LOCATION.md`](SOURCES-LOCATION.md) explains why.

## Format

Chapters are **GitHub-flavoured Markdown**, one file per chapter in `manuscript/`, 87 files covering
`ch01` to `ch83` including `ch72a`, `ch76a` and `ch76b`. Two collated part files also exist,
`part0-first-principles.md` and `part1-the-map.md`; Parts II to VIII have no collated markdown, which
is why only Parts 0 and I ever had a whole-part PDF from this pipeline.

Each chapter opens with an H1 (`# Chapter 40. Time Series & Forecasting`) and, except the Closing
chapter, a part line (`*Part IV — Machine Learning & Data Science*`). The builder reads both.

## The pipeline

`tools/pdf/build.py`, in four stages:

1. **Markdown to HTML**, by `pandoc`, using `tools/pdf/template.html`, with `--toc` at a depth the
   job sets. A pre-pass rewrites ```` ```mysql ```` fences to ```` ```sql ````, and a post-pass tags
   "Watch out" blockquotes with `class="warn"` so the stylesheet can style them.
2. **Cover**, from `tools/pdf/cover.html`, a one-page A4 gradient with five placeholders:
   `{{KICKER}}`, `{{TITLE}}`, `{{SUB}}`, `{{DOC}}`, `{{META}}`.
3. **HTML to PDF**, by **Playwright** driving headless Chromium, honouring `@page` from
   `tools/pdf/book.css` and adding a footer with the chapter name and `page / total`.
4. **Merge**, by **pypdf**: cover then body, with `/Title` and `/Author` metadata.

## Requirements

| Requirement | Notes |
|---|---|
| `pandoc` | Not a Python package. Install from pandoc.org or a package manager |
| `playwright` plus Chromium | `pip install playwright` then `playwright install chromium`. The browser is a separate download |
| `pypdf` | `pip install pypdf` |
| Fonts | The cover asks for Poppins and Lora, the footer for DejaVu Sans, and the body needs a face carrying ₹. Missing fonts silently fall back and change line breaks, so page numbers can shift. Install them before comparing against the review's page references |

## Commands

```bash
cd "Data Science/Analyst-to-Architect"

python tools/pdf/build.py --list          # what jobs exist
python tools/pdf/build.py ch12            # one chapter
python tools/pdf/build.py ch12 ch13 ch40  # several
python tools/pdf/build.py all-chapters    # every chapter in manuscript/
python tools/pdf/build.py                 # every hand-written job (the old default)
```

Output goes to `build/pdf/` by default. Override with environment variables:

```bash
BOOK_BUILD_DIR=/tmp/scratch BOOK_OUT_DIR=../../fixed/Part-II python tools/pdf/build.py ch12
```

## What was changed to make it run outside its original sandbox

The script was written in the environment the book was drafted in and hardcoded paths from it. The
original is kept beside it as `tools/pdf/build.py.orig-sandbox`. Changes:

| Was | Now |
|---|---|
| `D = pathlib.Path('/home/claude/book/pdf')` | `HERE`, `ROOT`, `MS`, `D` and `OUT` derived from the script's own location, with `BOOK_BUILD_DIR` and `BOOK_OUT_DIR` overrides |
| `template.html` and `cover.html` read from the scratch dir | Read from `HERE`, where they actually live |
| 16 chapter sources as `/home/claude/book/<file>.md` | Bare filenames resolved against `manuscript/` |
| `out = f'/mnt/user-data/outputs/{name}.pdf'` | `OUT / f'{name}.pdf'`, created if absent |

It compiles, imports, and resolves all 85 chapters. It has not rendered anything.

## Coverage: 12 hand-written jobs, 73 derived

`JOBS` holds 16 entries, covering only 12 chapters (`ch01` to `ch06`, `ch12`, `ch13`, `ch25`,
`ch26`, `ch27`, `ch83`), plus `part0`, `part1`, `blueprint` and the superseded `ch12v3`. Those carry
hand-written cover blurbs. The other 73 chapters were built by other scripts in other sessions that
are not in this repo, so a generic path was added: it derives the cover from the chapter's H1 and
part line.

Two consequences worth knowing:

- **A derived cover is not the original cover.** The kicker and title match, but the `SUB` blurb is
  empty and `DOC` reads "Rebuilt". If a cover should match the released one exactly, add a job.
- **Page numbers are safe.** The cover is one page either way, so body page numbers still line up
  with the page references in `review/visual/`.

Two jobs cannot run here: `blueprint` (out of scope by the version rule, and `blueprint.md` is not in
the repo) and `ch12v3` (the superseded Ch 12; `ch12.v3.md` is not in the repo either). Both fail with
a missing-file error, which is correct.

Output filenames were pinned to match the released PDFs. All 85 derived names now equal the existing
filenames in `Analyst-to-Architect-PDFs-Ch01-34/` and `-Ch35-83/`, using a small `NAMES` table for
the eight chapters whose released filename is shorter than their full title.

## Verifying a chapter, not just building it

```bash
python tools/verify_python.py manuscript/ch27-*.md --cwd companion/full
python tools/verify_sql.py    manuscript/ch13-*.md
python tools/verify_shell.py  manuscript/ch34-*.md
python tools/check_code_teaching.py manuscript/ch26-*.md
cd figures && python make_figs27.py          # redraw a chapter's figures
```

`checks/` holds 63 per-chapter scripts. `review/briefs/prescan.py` runs the automated layout checks
against a built PDF, and `pdftoppm -r 110` renders pages for eyeballing. `pdftoppm` ships with
Poppler and is also not installed here.

## Still unknown

- Whether a build actually succeeds end to end. Nothing has been rendered.
- Whether a rebuilt chapter matches the reviewed PDF page for page. Fonts are the main risk.
- Which pandoc version the original used. Nothing pins it, and pandoc's GFM handling has changed
  across releases, so a different version may repaginate.
