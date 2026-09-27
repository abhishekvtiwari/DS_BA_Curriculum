# Analyst to Architect: fix workspace

This repo holds the review of *Analyst to Architect* (3,758 findings), the book's source files, and the work of fixing them. Claude Code does the fixing and follows [`CLAUDE.md`](CLAUDE.md).

- **See progress:** [TRACKER.md](TRACKER.md)
- **Record decisions:** [DECISIONS.md](DECISIONS.md) (edit on github.com, works from a phone)
- **Review status and agreed process:** [REVIEW-STATUS.md](REVIEW-STATUS.md)
- **Review a part:** open its pull request, read the summary, check the PDFs in `fixed/`, then merge.

## How the work flows

1. Abhishek fills in `DECISIONS.md` (themes, structural choices, option picks).
2. Claude Code copies those decisions into `tracker/register.csv`.
3. Claude Code fixes one part at a time. For each chapter it edits the source, re-runs the code, redraws the figures, rebuilds the PDF, checks every page, then updates the tracker and writes a changelog.
4. Claude Code opens one pull request per part. Abhishek reviews and merges, and the next part starts.

## Folders

| Folder | Contents |
|---|---|
| `review/` | All findings: content review per chapter, visual review per chapter with 762 snapshots, sequence map, briefs |
| `tracker/` | `register.csv` (the live list of findings with status) and the script that builds `TRACKER.md` |
| `source/` | Where the kit expects the book's build inputs. **Read [`source/SOURCES-LOCATION.md`](source/SOURCES-LOCATION.md) first:** the sources are already in this repo, under `Data Science/`, not unpacked into `source/` |
| `fixed/` | Rebuilt PDFs, one folder per part |
| `changelog/` | What changed, finding by finding, per chapter |
| `Data Science/` | The book itself: manuscript, planning, companion code and data, figures, build tooling, and rendered chapter PDFs |

## `Data Science/`: the book archive

The book's own files were pushed here before the fix kits arrived, so the kit's `source/` folder
is empty and nothing needs uploading from a phone.

### The working tree

| Folder | What it is |
|---|---|
| `Data Science/Analyst-to-Architect/` | **The tree to edit.** Manuscript, planning, companion code and data, figures, SQL, tools, checks. |
| `Data Science/Analyst-to-Architect-complete/` | A companion-data-only snapshot, with the full generated datasets. |

Inside `Analyst-to-Architect/`:

- `manuscript/` — the chapters, one Markdown file each, `ch01` through `ch83` (87 files; the
  numbering includes `ch72a`, `ch76a` and `ch76b`).
- `planning/` — the chapter map (reading order lives here, and it differs from the numeric
  order in Parts II and III), the Riverstone story bible, part status files, and briefs.
- `companion/` — per-chapter runnable code and datasets, plus `companion/full/` with the large
  generated CSVs and Parquet files.
- `figures/` — SVG figures and the 69 `make_figs*.py` scripts that draw them.
- `tools/` — the PDF builder, the four verifiers, the code-teaching checker, the promise
  extractor, and the database setup script.
- `checks/` — 63 per-chapter verification scripts.
- `sql/` — schema and seed scripts.

### Point-in-time snapshots

The bundles as they were approved, kept for reference. They overlap with the working tree and
none of them is authoritative: `Analyst-to-Architect-Part-0-complete/` through
`-Part-VIII-complete/`, and `-Final-Chapters-25-26-27-83/`.

Each carries a `pdf/` directory with one rendered PDF per chapter. Parts 0, I, IV and VIII also
include a single collated file covering the whole part. Parts II, III, V, VI and VII have no
collated file yet.

### Rendered output

`Analyst-to-Architect-PDFs-Ch01-34/` and `-PDFs-Ch35-83/` hold the chapter PDFs. These are build
output, not source: edit the Markdown and re-render.

## Two things to know before editing a chapter

- **Reading order is not chapter order.** `planning/chapter-map.md` is the authority, and
  `review/sequence-map.md` holds the approved whole-book order. In Part II the reading order runs
  10, 11, 19, 12, 13, 17, 18, 14, 15, 16, 20, then 21 to 27; Part III runs 28, 34, 29, 32, 33, 30, 31.
- **Chapter output is verified, not typed.** Printed results come from running the companion code.
  Change the code and re-run it rather than editing a number in the prose, then use `checks/`.

## Notes on this repository

This repo previously held the Business Analyst curriculum (`business-analyst/`, `contracts/`,
`governance/`, `production/`, `schemas/`, `templates/`). That content was removed from `main` on
27 September 2026. It is not lost: it remains in git history at commit `75b4657` and earlier, and
on the `governance/iss-009-batch-rejection` branch. Recover any path with
`git checkout 75b4657 -- <path>`.

The repo is currently **public**. `CLAUDE.md` and the kit README both describe it as private, so
change the visibility or treat those lines as out of date.

The folder name `Data Science` contains a space, so quote it in shell commands. A shallow clone is
much faster if you do not need the full history:

```bash
git clone --depth 1 https://github.com/abhishekvtiwari/DS_BA_Curriculum.git
```
