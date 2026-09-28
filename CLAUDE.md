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
- **Reading order (Abhishek, 28 Sep): `planning/chapter-map.md`, with D1 kept.** So Ch 14–16 come before Python (17–18); everything else follows the chapter map.
  - Part II reads 10, 11, 19, 12, 13, 14, 15, 16, 17, 18, 20, then 21–27.
  - Part III reads 28, 34, 29, 32, 33, 30, 31.
  - Where a finding assumes a different order, it stays `Open` with the reason in `notes` (listed in `review/reading-order-conflicts.md`). Don't guess.
- **Renumbering (Abhishek, 28 Sep): Parts II and III are renumbered to match the reading order**, in the final pass (section 5, step 4), together with the Part VIII renumbering (D2) and the cross-reference pass. Until then every file, finding and part build keeps the current numbers.

  | Old | 10 | 11 | 19 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 20–27 | 28 | 34 | 29 | 32 | 33 | 30 | 31 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | **New** | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20–27 | 28 | 29 | 30 | 31 | 32 | 33 | 34 |
- **D1:** Power BI (Ch 16) stays before Python (Ch 17–18). Ch 16 must not assume pandas. (Kept by Abhishek, 28 Sep.)
- **D2:** Ch 34 is split. Terminal essentials move to Ch 26 §26.0; Linux and networking stay in Ch 34.
- **D3:** regression basics become a new final section of Ch 22.
- **D6:** Chapter 6 is split, with no renumbering.
  - A new **unnumbered front section, "How to Use This Book"**, goes before Chapter 1 (4–6 pages). It covers how each chapter is laid out, how to read the code cells and their outputs, the four exercise groups and the answers, how the parts climb, a rough sense of time (pointing to Ch 6), and where the companion files are. It takes old §6.9 (chapter anatomy, exercises) and adds the rest new.
  - **Chapter 6 keeps its number and becomes "Planning Your Learning"**: the honest hours table, the weekly rhythm, a tool timeline (no installs), learning with AI assistants, reading documentation, and a project to plan your route and first 90 days.
  - Also update the Part 0 contents, Ch 5's "Where this leads" and Ch 9's references to Ch 6. The spec is Chapter 6 of `review/part-0-and-I/fix-instructions-DRAFT-parked.md`.
- **D8 (Abhishek, 28 Sep): how the book is divided and named.**
  - Every chapter reads in six stages: **Start** (Why this matters, In plain English) · **Learn** (numbered sections) · **Apply** (Common mistakes, In the real world, Project with *Tools you'll need* inside it, Timed challenge) · **Review** (Recap, Key terms, Check yourself, Final-week revision list) · **Practise** (Exercises, Answers) · **Next** (Where this leads). `tools/restructure.py` puts a chapter in this order; the builder labels each stage and adds the chapter map. Ch 67 and Ch 83 have their own closing sections and are placed in their part builds.
  - Reader text numbers the parts **0 to 8** ("Part 2", "Parts 3 to 7"); `tools/part_numerals.py` converts. Internal files (the register's `part` column, review files, branch names) keep the Roman numerals.
  - Navigation: a chapter map ("In this chapter") with page numbers under each chapter's glance box; two-level contents in part builds; one page count per part package (front matter i, ii …). Build a part package with a `package-…` job in `tools/pdf/build.py` (e.g. `package-0-1`).
  - New or rewritten chapter text must use the new section names and the stage order.
- Python in Ch 14 §14.13 and Ch 15 §15.14 moves to Ch 18. (Kept by Abhishek, 28 Sep.)
- A one-page NumPy basics section goes in Ch 18.
- Part 0 and Part I findings are approved (status `Approved` in the CSV).
- **Version rule:** where a chapter exists in several versions, the latest is final. Ch 12's final version is Draft v4 (96 pages, 19–23 h, expanded §12.13). The Blueprint files are out of scope.

## 4. What you may fix: the approval gate

**In force since 28 Sep 2026:**
- **Global rules:** A1 is ticked and A3 is not. All themes T1–T14 and V1–V11 are Approve; V12 is Modify (see `DECISIONS.md`: Claude Code does what it can, and screenshots are listed for Abhishek to retake).
- **Structural decisions:** D2–D7 are Approve.
- **Option picks:** strictly the recommended option, else (a).
- **Reader's Journey rows:** approved.
- **Exception:** rows that assume a reading order other than the approved one are held `Open` (see §3).

Before each session, read `DECISIONS.md` and update `tracker/register.csv`:
- **Global rule A1:** every row becomes `Approved` unless its theme (section B) or its row (section E) says Reject, Defer or Modify.
- **Global rule A2:** a row becomes `Approved` only if its theme is marked Approve, or it is listed in E as Approve. Map each row to its theme by reading its issue text; if the fit is unclear, leave it `Open` and list it in the PR.
- **Global rule A3:** also list every High row of the part in the PR description as a checklist, and don't mark those rows `Verified` until Abhishek ticks them.
- Record where each decision came from in `decision_source` (e.g. `DECISIONS B:T3`, `DECISIONS A1`).
- **Section D (option picks):** use Abhishek's choice. If it's blank, use the option the finding marks as recommended, or option (a) if none is marked. Write which option you used in the changelog.
- **Never fix a row that is `Open`, `Rejected` or `Deferred`.** If `DECISIONS.md` has no global rule ticked, stop and ask in the PR.

## 5. Working mode and order of work (Abhishek, 28 Sep 2026: the standing rule)

**The book is built one part at a time, end to end.**
- **Trigger:** when Abhishek says **"Build Part X"**, work through every chapter of that part in reading order. For each chapter, apply all approved fixes, re-run all code, redraw the figures, and rebuild and check every page (section 6). Then go straight to the next chapter **without stopping to ask**.
- **Stop only for a true blocker:** a missing source, or a build that won't run. Collect every other question under **"Questions for Abhishek"** in the part's PR and carry on. A finding that can't be applied without an answer stays `Open`, with the reason in `notes`.
- **Commit and push as you go on long runs**, so no work is lost. Don't ask Abhishek anything until the part is finished.
- **When the part is finished, deliver one package** (section 7):
  - the whole part as a **single PDF** in `fixed/Part-X/`;
  - a **one-page summary per chapter** (what changed, and what was skipped and why);
  - **one pull request**.

  Abhishek reviews once and merges.

Order:

1. **Whole-book layout pass (once, before any part; one PR `style-pass`):**
   - themes **V1–V12** wherever one shared change fixes them: the builder (`tools/pdf/build.py`, `layout.js`), stylesheet and cover template, plus source fixes that change no wording (broken table pipes, escapes), and V12 (Ch 19 scale, rasters re-exported at 300 ppi). **Figure redraws (V3–V6: text under 7 pt, overlaps, colour-only meaning, figure order) are done per chapter in the part builds** (section 6 step 3), because each figure must be checked against its caption and text;
   - rebuild every chapter;
   - run `review/briefs/prescan.py` and `tools/pdf/layout_check.py` on each rebuilt PDF, then spot-render and compare with the snapshots;
   - mark the fixed visual rows `Fixed`.
2. **Riverstone fact sheet (D3):** draft `review/riverstone-facts.md` from the chapters and the findings under theme T10. Cover people and roles, the timeline, systems, rates, datasets, file names and the flash time. Open it as a PR for Abhishek to approve before Part II content work starts.
3. **Content, part by part, one PR per part, in this order: Part 0 + Part I together** (branch `part-0-I`, which includes D6), then II, III, IV, V, VI, VII, VIII, Closing (branch `part-II`, etc.). Within a part, go chapter by chapter in reading order. Findings that assume another reading order (`review/reading-order-conflicts.md`) stay `Open`.
4. **Final pass:** renumber Parts II and III to the reading order (map in section 3) and Part VIII (D2), then book-wide cross-references (T8) from a generated index, then the Time needed tables in Ch 6, 9 and 83 recomputed from one source (T12).

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
   - check `tools/restructure.py --check` reports the chapter in stage order (D8);
   - run `python review/briefs/prescan.py build/<file>.pdf build/<file>.json` and `python "Data Science/Analyst-to-Architect/tools/pdf/layout_check.py" build/<file>.pdf` (contents numbers, stranded headings and lead-ins, half-empty pages, clipped list numbers, draft labels);
   - render the pages that had visual findings (`pdftoppm -r 110`) and look at them;
   - confirm each visual finding is gone.
5. Re-read the chapter as the first-time reader against the seven tests.
6. Update the CSV: each fixed row becomes `Fixed`, with `fixed_in` set to the commit or PR and a short note. Rows you checked in the rebuilt PDF become `Verified`. If a fix proves wrong or impossible, set it back to `Open` and explain why in `notes`.
7. Write `changelog/chNN.md`, with one line per finding: `ID · what changed · where (section/page) · option used if any`. Add before/after page crops for High visual findings to `changelog/img/`.
8. Run `python tracker/make_tracker.py` and commit the source, CSV, `TRACKER.md` and changelog **together**. Commit message: `Ch NN: fix <n> findings (<ids range>)`.

## 7. The package for a part: one PDF, one summary per chapter, one pull request

- **One PDF for the whole part** in `fixed/Part-X/` (e.g. `fixed/Part-II/Part-II-The-Analyst.pdf`), built from the fixed chapters. Chapter PDFs can sit beside it.
- **One page per chapter**, `changelog/chNN-summary.md`: what changed, what was skipped and why, and the option picks used. The line-by-line `changelog/chNN.md` stays as the detailed record.
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
- **Ask when unsure, but don't pause.** Put the question in the PR description under "Questions for Abhishek" rather than guessing, and keep working on everything else (section 5).
