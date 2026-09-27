# DS_BA_Curriculum

This repository holds the **Analyst to Architect** data science book: manuscript, planning
documents, companion datasets and code, figures, and rendered chapter PDFs.

Everything lives under [`Data Science/`](Data%20Science/).

> **Note on history.** This repository previously held the Business Analyst curriculum
> (`business-analyst/`, `contracts/`, `governance/`, `production/`, `schemas/`, `templates/`).
> That content was removed from `main` on 27 September 2026 to make room for the book. It is
> not lost: it remains in this repository's git history (see commit `75b4657` and earlier) and
> on the `governance/iss-009-batch-rejection` branch. To recover any of it:
> `git checkout 75b4657 -- <path>`.

## What is in `Data Science/`

### The working tree

| Folder | What it is |
|---|---|
| `Analyst-to-Architect/` | **The main tree, and the one to work in.** Full manuscript, planning, companion code and data, figures, SQL, tools, checks. |
| `Analyst-to-Architect-complete/` | A companion-data-only snapshot: the `companion/` directory with the full generated datasets. |

Inside `Analyst-to-Architect/`:

- `manuscript/` — the chapters, one Markdown file each, `ch01` through `ch83` (85 files: the
  numbering includes `ch72a`, `ch76a` and `ch76b`, which are chapters added after the original
  plan and are renumbered at assembly).
- `planning/` — the chapter map (reading order lives here, and it differs from the numeric
  order in Parts II and III), the Riverstone story bible, part status files, and briefs.
- `companion/` — per-chapter runnable code and datasets (`ch12/`, `ch29/`, `ch32/riverstone_dbt/`
  and so on), plus `companion/full/` with the large generated CSVs and Parquet files.
- `figures/` — SVG figures referenced from the chapters.
- `sql/`, `tools/`, `checks/` — schema and seed scripts, build and export helpers, and the
  verification scripts that check chapter output against the companion code.

### Point-in-time snapshots

These are the bundles as they were approved, kept for reference. They overlap with the main
tree; nothing here is authoritative.

Each one carries its own `pdf/` directory holding one rendered PDF per chapter. Parts 0, I, IV
and VIII additionally include a single collated file with the whole part in one document, one
cover, one contents page and continuous page numbers. Parts II, III, V, VI and VII have no
collated file yet.

| Folder | Covers |
|---|---|
| `Analyst-to-Architect-Part-0-complete/` | Part 0, front matter and orientation |
| `Analyst-to-Architect-Part-I-complete/` | Part I, The Map |
| `Analyst-to-Architect-Part-II-complete/` | Part II, The Analyst |
| `Analyst-to-Architect-Part-III-complete/` | Part III |
| `Analyst-to-Architect-Part-IV-complete/` | Part IV |
| `Analyst-to-Architect-Part-V-complete/` | Part V |
| `Analyst-to-Architect-Part-VI-complete/` | Part VI, Production ML, Generative AI & MLOps |
| `Analyst-to-Architect-Part-VII-complete/` | Part VII, Architecture, Governance & Leadership |
| `Analyst-to-Architect-Part-VIII-complete/` | Part VIII, The Interview Playbook |
| `Analyst-to-Architect-Final-Chapters-25-26-27-83/` | Chapters 25, 26, 27 and 83 |

### Rendered output

| Folder | Contents |
|---|---|
| `Analyst-to-Architect-PDFs-Ch01-34/` | Chapter PDFs, 1 to 34 |
| `Analyst-to-Architect-PDFs-Ch35-83/` | Chapter PDFs, 35 to 83 |

PDFs are build output, not source. Edit the Markdown in `manuscript/` and re-render.

## Working on this

```bash
git clone https://github.com/abhishekvtiwari/DS_BA_Curriculum.git
cd DS_BA_Curriculum/"Data Science"/Analyst-to-Architect
```

The folder name contains a space, so quote it in shell commands.

Two things worth knowing before editing a chapter:

- **Reading order is not chapter order.** `planning/chapter-map.md` is the authority. In Part II
  the reading order runs 10, 11, 19, 12, 13, 17, 18, 14, 15, 16, 20, then 21 to 27; Part III runs
  28, 34, 29, 32, 33, 30, 31. Cross-references in the chapters still use pre-renumbering numbers
  in places.
- **Chapter output is verified, not typed.** Printed results in a chapter come from running the
  companion code. If you change a number in the prose, change the code and re-run it, and use
  `checks/` to confirm.

## Repository size

About 236 MB across roughly 2,660 files, mostly companion datasets, SVG figures and PDFs. A
shallow clone is faster if you only need the manuscript:

```bash
git clone --depth 1 https://github.com/abhishekvtiwari/DS_BA_Curriculum.git
```
