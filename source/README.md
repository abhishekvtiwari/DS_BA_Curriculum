# source/

Put the book's **source files** here: the files the chapter PDFs are built from.

- Chapter text (Markdown / HTML / Word / Quarto… whatever you use)
- The stylesheet, template or build script that turns them into PDFs
- Figure scripts (for example `figures/make_figs08.py`) and `checks/` scripts
- Companion data and code (the Riverstone datasets, `companion/…`)

**Uploading from a phone:** github.com only accepts files up to **25 MB** each. Upload one zip per part (e.g. `part-II.zip`). If a zip is over 25 MB, split it (e.g. `part-II-a.zip`, `part-II-b.zip`). Claude Code unzips them in its first session.

After unpacking, Claude Code writes `source/BUILD.md` explaining how the build works.
