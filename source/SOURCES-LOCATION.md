# The book's sources are already in this repo

`source/` is empty on purpose. The kit was written expecting the book to be uploaded from a phone
as zips, and `CLAUDE.md` section 0 tells you to unpack them here. **That is no longer needed.** The
full book, including the build tooling, was pushed to this repo on 27 September 2026 and lives at:

```
Data Science/Analyst-to-Architect/
```

Nothing was copied into `source/`, because duplicating roughly 200 MB inside the same repo would
mean two trees drifting apart. Edit the tree above; treat it as `source/`.

## What is there

| Path (under `Data Science/Analyst-to-Architect/`) | Contents |
|---|---|
| `manuscript/` | 87 Markdown files, `ch01` to `ch83`, including `ch72a`, `ch76a`, `ch76b` |
| `tools/pdf/` | `build.py` (the PDF builder), `book.css`, `template.html`, `cover.html` |
| `figures/` | The SVGs and 69 `make_figs*.py` scripts |
| `checks/` | 63 per-chapter verification scripts |
| `companion/` | Per-chapter runnable code and datasets; `companion/full/` holds the large CSVs and Parquet files |
| `sql/` | Schema and seed scripts |
| `planning/` | Chapter map, Riverstone bible, part status files |

The book's own `README.md` documents the commands. The relevant ones:

```bash
# build one chapter's PDF
python3 tools/pdf/build.py ch27

# redraw a chapter's figures
cd figures && python3 make_figs27.py

# verify a chapter's code, SQL or shell output
python3 tools/verify_python.py manuscript/ch27-*.md --cwd companion/full
python3 tools/verify_sql.py manuscript/ch13-*.md
python3 tools/verify_shell.py manuscript/ch34-*.md

# check a chapter against the section 6.5 code-teaching standard
python3 tools/check_code_teaching.py manuscript/ch26-*.md
```

## Known blocker before the first build

`tools/pdf/build.py` hardcodes an absolute path on line 4:

```python
D = pathlib.Path('/home/claude/book/pdf')
```

That directory is from the sandbox the book was written in and will not exist in a clone, so the
build fails immediately anywhere else. Make it relative to the script or the repo root before
attempting a build. This is the first thing to fix, and it is a source-tooling change, not a book
finding, so it does not belong in `tracker/register.csv`.

Build dependencies, from the script's imports and subprocess calls:

| Dependency | Used for |
|---|---|
| `pandoc` | Markdown to HTML5, with `--toc` |
| `playwright` with Chromium | HTML to PDF, via `page.pdf()` |
| `pypdf` | Merging the cover with the body |

## Bootstrap state

Against `CLAUDE.md` section 0:

| Step | State |
|---|---|
| 1. Unzip the kits | Done. Kit 1 is at the repo root, Kit 2's 762 snapshots are in `review/visual/snaps/` |
| 2. Delete the zips | Not applicable; the kits were committed already unpacked, so no `kit-*.zip` was ever pushed |
| 3. `python tracker/make_tracker.py` | Not run. `TRACKER.md` is the copy shipped in the kit |
| 4. Write `source/BUILD.md`, test-build Ch 12 | **Not done.** No build has been attempted, so nothing is claimed about whether it works |
| 5. Open the `setup` PR | Not done |

Because `review/visual/snaps/` is no longer empty and there are no `kit-*.zip` files at the root,
the trigger condition in section 0 will read as false. Steps 3 to 5 above are still outstanding.
