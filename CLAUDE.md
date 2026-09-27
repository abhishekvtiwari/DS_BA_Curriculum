# CLAUDE.md: instructions for every Claude Code session in this repo

You are working on **Analyst to Architect**, a course book by Abhishek Tiwari. It takes a complete beginner from "what is data" to data architect, through a fictional company, Riverstone Supplies. It has 83 chapters in Parts 0–VIII plus a Closing chapter, including 72A, 76A and 76B.

A full review is finished: 3,758 findings, of which 2,534 are about content and 1,224 about page layout. **Your job is to apply the approved findings to the book's source files, rebuild the PDFs, check them, and keep the tracker current.** Read this whole file before doing anything.

---

## 0. First session only: bootstrap

If `review/visual/snaps/` is empty or `kit-*.zip` files sit at the repo root, the repo has just been set up from phone uploads. Do this:

1. Unzip every `kit-*.zip` at the repo root, keeping paths (`unzip -o kit-1-repo.zip`, then `kit-2-snapshots.zip`). Then unzip every zip in `source/` into `source/`, keeping each zip's folder name.
2. Delete the zip files after checking that the unzipped files are there.
3. Run `python tracker/make_tracker.py`.
4. Inspect `source/` and write `source/BUILD.md`. It must say: what format the chapters are in (Markdown, HTML, Word, Quarto…), where the stylesheet or template lives, how one chapter is built to PDF (exact command), where the figure scripts are, and what is missing. **Try building one chapter (Ch 12) and report whether it worked.** If the source files are missing, don't invent them: stop and say so in the PR description.
5. Commit on a branch `setup` and open a PR titled "Setup: unpack kits, document build". Stop there.

---

## 1. Repo map

| Path | What it is | Who edits |
|---|---|---|
| `DECISIONS.md` | Abhishek's decisions: global rule, themes, structural choices, option picks | **Abhishek only**. Never edit it, only read it |
| `tracker/register.csv` | Every finding, one row each, with `status` | You, in the same commit as the fix |
| `tracker/make_tracker.py` | Rebuilds `TRACKER.md` from the CSV | Run after every CSV change |
| `TRACKER.md` | Progress by part and chapter (generated) | Never by hand |
| `review/content/chNN.md` | Detailed content review per chapter (Ch 10–83): verdict, issues table, code audit, sequence notes, numbers checked | Read only |
| `review/part-0-and-I/findings.md` | Content findings for Ch 1–9 (approved). `fix-instructions-DRAFT-parked.md` is a draft plan; use it as guidance for Part 0/I | Read only |
| `review/visual/chNN.md` | Visual/layout review per chapter, with PDF page numbers (page 1 = cover) | Read only |
| `review/visual/snaps/` | Crops of every High/Medium visual finding, `V<ch>.<n>_p<page>.png` | Read only |
| `review/sequence-map.md` | Approved whole-book order and the structural breaks M.1–M.12 | Read only |
| `review/content-review-index.md`, `review/visual-review-summary.md` | Totals, per-chapter verdicts, themes | Read only |
| `review/briefs/` | The review briefs and `prescan.py` (automated layout checks) | Reuse for verification |
| `review/Book-Review-Action-Register.xlsx` | The same register as a workbook (read only; the CSV is the live tracker) | Read only |
| `source/` | The book's source files and build scripts | You edit, on a branch |
| `build/` | Rebuilt PDFs (gitignored except `build/README.md`) | Generated |
| `fixed/` | Final PDFs for each merged part, `fixed/Part-II/Ch12-….pdf` | You add in the part's PR |
| `changelog/` | One file per chapter: `changelog/chNN.md` | You write |

---

## 2. The reader, and the tests every fix must pass

The reader is a **first-time learner**. They know only what earlier chapters taught. The author's principle: *don't hand a 5-year-old a 16-year-old's problem.* Every idea unfolds in this order: **plain idea → worked by hand → in a tool already known → new tool, one line at a time.**

Code is taught **like Jupyter**. Show each cell, run it, show its real output, then explain every line and every parameter. Introduce one new idea per cell.

Every chapter you touch must pass the seven tests:
1. **First-time reader:** every term is defined before it is used.
2. **Line-by-line code:** every block is shown, run and has its output shown, and every line and argument is explained. No block introduces five new ideas at once.
3. **Flow:** the chapter depends only on earlier chapters.
4. **Load:** the new material per section is reasonable, and the "Time needed" line is re-estimated honestly.
5. **Consistency/correctness:** numbers, names and datasets agree with earlier chapters and with the Riverstone fact sheet. Recompute arithmetic with code. Re-run every code block.
6. **Reader-facing polish:** no drafting leftovers ("In the finished book these move to Appendix G", "this chat", "coordinator", "first edition", "blueprint", build scripts named as reader files), and no broken cross-references.
7. **Sequence:** nothing (code, function, keyword, library, term) appears before the section that teaches it, within the chapter or across the book.

Plus the **visual standard** (see `review/briefs/VISUAL_BRIEF.md`):
- figure text ≥ 7 pt;
- no clipped or overlapping labels;
- no colour-only meaning;
- no half-empty pages and no stranded headings or lead-ins;
- code hard-wrapped with correct continuation;
- tables with no mid-token wraps and right-aligned numbers;
- contents pages with page numbers;
- no draft badges on covers.

## 3. Decisions already approved (do not re-litigate)

- **Tools are installed just in time** in the chapter that first uses each one:
  - spreadsheet in Ch 10 (new §10.0);
  - database in Ch 12 §12.3;
  - Power BI at the start of Ch 16;
  - Python, VS Code, Jupyter and a minimal terminal in Ch 17 (new §17.0, first one-cell notebook);
  - Git in Ch 26, with a new §26.0 "The terminal in 20 minutes".

  **Chapter 6 becomes tool-free.**
- **D1:** Power BI (Ch 16) stays before Python (Ch 17–18). Ch 16 must not assume pandas.
- **D2:** Ch 34 is split. Terminal essentials move to Ch 26 §26.0; Linux and networking stay in Ch 34.
- **D3:** regression basics become a new final section of Ch 22.
- Python in Ch 14 §14.13 and Ch 15 §15.14 moves to Ch 18. A one-page NumPy basics section goes in Ch 18.
- Part 0 and Part I findings are approved (status `Approved` in the CSV).
- **Version rule:** where a chapter exists in several versions, the latest is final. Ch 12's final version is Draft v4 (96 pages, 19–23 h, expanded §12.13). The Blueprint files are out of scope.

## 4. What you may fix: the approval gate

Before each session, read `DECISIONS.md` and update `tracker/register.csv`:
- **Global rule A1:** every row becomes `Approved` unless its theme (section B) or its row (section E) says Reject, Defer or Modify.
- **Global rule A2:** a row becomes `Approved` only if its theme is marked Approve, or it is listed in E as Approve. Map each row to its theme by reading its issue text; if the fit is unclear, leave it `Open` and list it in the PR.
- **Global rule A3:** also list every High row of the part in the PR description as a checklist, and don't mark those rows `Verified` until Abhishek ticks them.
- Record where each decision came from in `decision_source` (e.g. `DECISIONS B:T3`, `DECISIONS A1`).
- **Section D (option picks):** use Abhishek's choice. If it's blank, use the option the finding marks as recommended, or option (a) if none is marked. Write which option you used in the changelog.
- **Never fix a row that is `Open`, `Rejected` or `Deferred`.** If `DECISIONS.md` has no global rule ticked, stop and ask in the PR.

## 5. Order of work

1. **Style pass (whole book, one PR `style-pass`):**
   - shared template and CSS fixes (themes V1, V2, V7, V8, V9, V10, V11, V12);
   - rebuild every chapter;
   - run `review/briefs/prescan.py` on each rebuilt PDF, then spot-render and compare with the snapshots;
   - mark the fixed visual rows `Fixed`.
2. **Riverstone fact sheet (D3):** draft `review/riverstone-facts.md` from the chapters and the findings under theme T10. Cover people and roles, the timeline, systems, rates, datasets, file names and the flash time. Open it as a PR for Abhishek to approve before Part II content work starts.
3. **Content, part by part, one PR per part:** Part 0 → I → II → … → VIII → Closing. Branch name `part-II`, etc. Within a part, go chapter by chapter in order.
4. **Final pass:** book-wide cross-references (T8), then the Time needed tables in Ch 6, 9 and 83 recomputed from one source (T12), then renumbering (D2) if approved.

## 6. How to fix one chapter

1. Read `review/content/chNN.md` (or the Part 0/I findings) and `review/visual/chNN.md`. Filter `tracker/register.csv` to the chapter's `Approved`/`Modify` rows.
2. Apply the fixes in the source, in finding order, but group edits by section. For code:
   - split big blocks into cells;
   - run every cell in a fresh environment with the book's datasets;
   - paste the **real** output;
   - explain every line and argument.

   Never type an output by hand.
3. Redraw the chapter's figures from the figure scripts at print width (text ≥ 7 pt). Check each figure against its caption and the text.
4. Build the chapter PDF into `build/`. Then:
   - run `python review/briefs/prescan.py build/<file>.pdf build/<file>.json`;
   - render the pages that had visual findings (`pdftoppm -r 110`) and look at them;
   - confirm each visual finding is gone.
5. Re-read the chapter as the first-time reader against the seven tests.
6. Update the CSV: each fixed row becomes `Fixed`, with `fixed_in` set to the commit or PR and a short note. Rows you checked in the rebuilt PDF become `Verified`. If a fix proves wrong or impossible, set it back to `Open` and explain why in `notes`.
7. Write `changelog/chNN.md`, with one line per finding: `ID · what changed · where (section/page) · option used if any`. Add before/after page crops for High visual findings to `changelog/img/`.
8. Run `python tracker/make_tracker.py` and commit the source, CSV, `TRACKER.md` and changelog **together**. Commit message: `Ch NN: fix <n> findings (<ids range>)`.

## 7. Pull request for a part

- **Title:** `Part II fixes: Ch 10–27 (<n> findings)`.
- **Body:**
  - a summary table per chapter (fixed / verified / skipped with reason);
  - the option picks used (section D);
  - rows left `Open` and why;
  - the High checklist if rule A3 is ticked;
  - links to `changelog/` files and the rebuilt PDFs in `fixed/Part-II/`.
- **Keep PRs reviewable on a phone:** short summary first, details in collapsible `<details>` blocks.
- Don't merge your own PR. Abhishek merges.

## 8. Rules

- **Don't invent facts, prices, laws, salaries or outputs.** Rows under theme T13 need dated sources. If you can't verify something, leave the row `Open` and say why.
- **Don't delete content** unless a finding says so. Don't rewrite beyond what the approved findings ask. The author's voice stays.
- **Keep numbers reconciled.** For example, Riverstone 2025 revenue is ₹4,335,471 and December is ₹439,823.50, as confirmed across chapters. If a fix changes a number, find every other place it appears.
- **Every chapter must still build** after each commit.
- **Bigger scope needs a comment.** If a fix needs changes in another chapter (cross-refs, moved sections), make them in the same PR and note them in both changelogs. Moves across parts (e.g. Ch 14 Python → Ch 18) are done in the later part's PR, with a placeholder note in the earlier part's changelog.
- **Keep the tracker true.** `TRACKER.md` must always match the CSV. Statuses allowed: Open, Approved, Modify, Rejected, Deferred, Fixed, Verified.
- **Ask when unsure.** Put the question in the PR description under "Questions for Abhishek" rather than guessing.
