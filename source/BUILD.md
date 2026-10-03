# How the book builds

**Verified by building, 28 September 2026.** Ch 12 was built and compared page by page with the
reviewed Draft v4. Then all 85 chapters were built and compared with the released PDFs in
`Data Science/Analyst-to-Architect-PDFs-Ch01-34/` and `-Ch35-83/`. Results are under
[Verification](#verification-28-september-2026) below.

The sources are not in `source/`. They are at `Data Science/Analyst-to-Architect/`, and
[`SOURCES-LOCATION.md`](SOURCES-LOCATION.md) explains why.

## Format

Chapters are **GitHub-flavoured Markdown**, one file per chapter in `manuscript/`. There are 85
chapter files, `ch01` to `ch83` including `ch72a`, `ch76a` and `ch76b`, plus two collated part files,
`part0-first-principles.md` and `part1-the-map.md`. Parts II to VIII have no collated markdown, which
is why only Parts 0 and I ever had a whole-part PDF from this pipeline.

Each chapter opens with an H1 (`# Chapter 40. Time Series & Forecasting`) and, except the Closing
chapter, a part line (`*Part IV — Machine Learning & Data Science*`). The builder reads both.

| What | Where (under `Data Science/Analyst-to-Architect/`) |
|---|---|
| Chapter text | `manuscript/chNN-*.md` |
| Builder | `tools/pdf/build.py` |
| Stylesheet | `tools/pdf/book.css` |
| Page template (pandoc) | `tools/pdf/template.html` |
| Cover template | `tools/pdf/cover.html` |
| Figures (SVG) and their scripts | `figures/`, drawn by `figures/make_figs*.py` (69 scripts) |
| Per-chapter checks | `checks/` (63 scripts) |
| Companion code and data | `companion/`, full datasets in `companion/full/` |

## The pipeline

`tools/pdf/build.py`, in four stages:

1. **Markdown to HTML**, by `pandoc`, using `tools/pdf/template.html`, with `--toc` at a depth the
   job sets. A pre-pass rewrites ```` ```mysql ```` fences to ```` ```sql ````. A post-pass tags
   "Watch out" blockquotes with `class="warn"` and points the stylesheet and figure links at their
   real locations (see below).
2. **Cover**, from `tools/pdf/cover.html`, a one-page A4 gradient with five placeholders:
   `{{KICKER}}`, `{{TITLE}}`, `{{SUB}}`, `{{DOC}}`, `{{META}}`.
3. **HTML to PDF**, by **Playwright** driving headless Chromium. It honours `@page` from
   `tools/pdf/book.css` and adds a footer with the chapter name and `page / total`.
4. **Merge**, by **pypdf**: cover then body, with `/Title` and `/Author` metadata.

## Requirements

Install everything with one script:

```bash
bash source/setup-toolchain.sh      # as root; takes about a minute
```

| Requirement | Version that reproduces the released PDFs |
|---|---|
| `pandoc` | 3.1.3 (Ubuntu 24.04 package) |
| Playwright + Chromium | Playwright **1.56.0** with Chromium 141 (`chromium-1194`, preinstalled in `/opt/pw-browsers` in the cloud container). A newer Playwright looks for a Chromium that is not there. Elsewhere, run `playwright install chromium` |
| `pypdf` | 6.x. On the cloud image the distro `cryptography` is broken and pypdf fails to import. `pip install --ignore-installed cryptography` fixes it |
| Poppler (`pdftoppm`, `pdffonts`) | 24.02, for checking pages, not for building |
| Fonts | **Poppins Regular, Bold and Bold Italic; Lora (regular and italic); DejaVu Sans, Serif and Mono including the oblique and italic faces** (`fonts-dejavu-extra`) |

**Fonts decide whether page numbers match the review.** The released PDFs were made on a machine
with *no* Poppins SemiBold, Medium or Italic. The stylesheet asks for weight 600, which fell back to
Bold. With SemiBold installed, headings get narrower, lines break differently, and 67 of Ch 12's 96
pages changed visibly. The setup script installs exactly the faces the released PDFs embed, and
removes the three that must be absent. Check with `pdffonts <file>.pdf`.

## Commands

```bash
cd "Data Science/Analyst-to-Architect"

python tools/pdf/build.py --list          # what jobs exist
python tools/pdf/build.py ch12            # one chapter
python tools/pdf/build.py ch12 ch13 ch40  # several
python tools/pdf/build.py all-chapters    # every chapter in manuscript/ (about 6 minutes)
python tools/pdf/build.py package-2       # one part as a single PDF (package-0-1, package-2 … package-8)

python tools/make_overview.py             # regenerate manuscript/book-overview.md and its flow figure
python tools/pdf/books.py book1 book2 book3 book4 map   # the four books, in order, then the whole-book map
python tools/pdf/books.py overview        # the internal Book Overview
```

The four books (`tools/pdf/books.py`) split the book by part; chapters stay whole:

| Book | Parts |
|---|---|
| 1. Theory | How to Use This Book, Parts 0–1 |
| 2. Practical | Parts 2–3 |
| 3. Implementation | Parts 4–7, then Ch 83 |
| 4. Be Interview Ready | Part 8 |

Books 1–3 share one page count, so build them in order: each saves its page labels to
`build/pdf/<name>-heads.json`, and the next book starts where the last one ended. `map` then inserts
"The whole book" (every part and chapter with its book and page) after the cover of all four. Book 2 and
Book 3 each take about an hour to render. The Book Overview is internal.

Output goes to `build/pdf/` under the book root by default, which is gitignored. Override with
environment variables:

```bash
BOOK_BUILD_DIR=/tmp/scratch BOOK_OUT_DIR=../../fixed/Part-II python tools/pdf/build.py ch12
```

Do not run two builds at once, or change fonts or Playwright while a build runs. That produces
`Page.pdf: Protocol error (Page.printToPDF): Printing failed`.

## Changes to the builder

The script was written in the environment the book was drafted in and hardcoded paths from it. The
original is kept beside it as `tools/pdf/build.py.orig-sandbox`.

| Was | Now | When |
|---|---|---|
| `D = pathlib.Path('/home/claude/book/pdf')` | `HERE`, `ROOT`, `MS`, `D` and `OUT` derived from the script's own location, with `BOOK_BUILD_DIR` and `BOOK_OUT_DIR` overrides | 28 Sep, before the kits |
| `template.html` and `cover.html` read from the scratch dir | Read from `HERE`, where they actually live | 28 Sep, before the kits |
| 16 chapter sources as `/home/claude/book/<file>.md` | Bare filenames resolved against `manuscript/` | 28 Sep, before the kits |
| `out = f'/mnt/user-data/outputs/{name}.pdf'` | `OUT / f'{name}.pdf'`, created if absent | 28 Sep, before the kits |
| Only 12 chapters had a job | A generic job derives the cover from each chapter's H1 and part line | 28 Sep, before the kits |
| **HTML links `book.css` and `figures/…` relatively.** The HTML is written to the scratch dir, so neither resolved: the first Ch 12 build came out unstyled at 43 pages instead of 96, with no figures | The post-pass rewrites both to absolute `file://` URLs | Setup PR |
| Generic footer read "Chapter 40. Time Series…" | "Chapter 40 · Time Series…", as released; `FOOTER_NAMES` pins the shorter footer titles of Ch 19 and Ch 51 | Setup PR |

## Covers: hand-written jobs and derived ones

`JOBS` holds 16 entries covering 12 chapters (`ch01` to `ch06`, `ch12`, `ch13`, `ch25`, `ch26`,
`ch27`, `ch83`), plus `part0`, `part1`, `blueprint` and the superseded `ch12v3`. Those carry
hand-written cover blurbs. The other 73 chapters get a **derived cover**: the kicker and title match
the release, but the blurb is empty and the badge reads "Rebuilt". This affects page 1 only. Theme V1
replaces every cover with one template anyway.

`blueprint` and `ch12v3` cannot run (their sources are not in the repo, and both are out of scope),
and fail with a missing-file error, which is correct.

Output filenames are pinned to the released ones through the `NAMES` table.

## Verification, 28 September 2026

| Check | Result |
|---|---|
| Ch 12 page count | **96**, the same as Draft v4 (`…PDFs-Ch01-34/Ch12-Databases-and-SQL-Foundations.pdf`) |
| Ch 12 text, page by page | 96 of 96 pages identical, footers included |
| Ch 12 pixels, page by page | 95 of 96 identical; one difference on the cover (below) |
| Ch 12 embedded fonts | Same set as v4 |
| All 85 chapters build | Yes, in about 6 minutes |
| Page counts | 85 of 85 the same as the released PDFs (2,455 pages) |
| Body text (all pages but covers) | 2,370 of 2,370 pages identical, footers included |
| Body pixels at 40 dpi | **2,370 of 2,370 pages identical** (with the font set above; before Poppins Bold Italic was added, one page, Ch 35 p. 19, differed by 8 pixels) |

**So the page numbers in `review/visual/` point at the same content in a rebuilt PDF.**

The one known difference: on the Ch 12 cover, the short decorative bar at the top right sits about
8 mm higher than in the release. `cover.html` places it at `top: 30mm`. The release shows it level with
the kicker (≈ 38 mm), so the sandbox's cover template or Chromium differed slightly. It is cosmetic,
and V1 replaces the covers.

## Layout pass (style-pass branch, 28 Sep 2026)

The builder now fixes the book's layout themes (V1–V12) for every chapter. What changed and why is in [`changelog/style-pass.md`](../changelog/style-pass.md). After the pass, **page numbers no longer match the released PDFs** (the book is 2,419 pages instead of 2,455), so page references in `review/visual/` point at the old layout.

| File | Role |
|---|---|
| `tools/pdf/build.py` | Markdown pre-pass (bold-label lines), pandoc without `$`-maths, HTML post-pass (sub/superscripts, caret powers, unbroken IDs), two-pass render that writes contents page numbers from the PDF's bookmarks, one cover template |
| `tools/pdf/layout.js` | Runs in the page before printing: fits code to the width (not below 7 pt), then hanging-indents and marks (↩) any line still too long; keeps headings, lead-ins, answer numbers and captions with what follows; right-aligns numeric table columns; keeps short tables and code blocks whole; drops redundant section rules and empty output boxes; reports anything wider than the text block |
| `tools/pdf/book.css`, `cover.html` | The matching styles |
| `tools/pdf/layout_check.py` | Checks a built PDF: contents numbers (and that each one is right), stranded headings and lead-ins, half-empty pages, clipped list numbers, draft labels, missing glyphs |

Each build also writes `<name>-layout.json` beside the HTML: how many code blocks were shrunk, how many lines wrapped, how many groups were kept together, and any overflow.

## Checking a chapter, not just building it

```bash
python tools/verify_python.py manuscript/ch27-*.md --cwd companion/full
python tools/verify_sql.py    manuscript/ch13-*.md
python tools/verify_shell.py  manuscript/ch34-*.md
python tools/check_code_teaching.py manuscript/ch26-*.md
cd figures && python make_figs27.py          # redraw a chapter's figures
```

`tools/pdf/layout_check.py` and `review/briefs/prescan.py` run the automated layout checks against a built PDF, and
`pdftoppm -r 110` renders pages for eyeballing. The SQL verifier needs PostgreSQL and MySQL with the
Riverstone databases loaded, which the setup script does not install. That comes with the first
chapter whose SQL is changed.

## Still unknown

- Which pandoc version the original used. 3.1.3 reproduces every page exactly, so it is at least
  equivalent for this book.
- Whether the SQL, Python and shell verifiers run cleanly in this environment. Not needed to build,
  and not yet run.
