# Handover: Analyst to Architect

*Written 1 Oct 2026 by the Claude Code chat that applied the review fixes and built the books.*

**Who this is for:** the owner and final reviewer of the book, a senior data scientist and VP. They will make or
approve the remaining small changes. It is also for the next Claude chat that picks up the work.

**In one line:** the review fixes are done, the book is built as four PDFs, and what's left is small. This page
says what was done, where everything lives, which files to edit for a change, and how to start a new chat to
make it.

---

## 1. Where things stand

| | |
|---|---|
| Review findings | **3,761 of 3,822 closed (98%)**: 3,152 checked in the rebuilt PDFs and 609 fixed in the source. |
| Still open | **46** need a decision or a fact from you (listed in section 6). **15** are approved, but wait for the final pass (section 6). |
| The books | Four reader books plus one internal overview, all built and checked (section 2). |
| Pull requests | **12 open, none merged yet.** Merge them in order (section 3). |

Everything was done by the rules in `CLAUDE.md` and your decisions in `DECISIONS.md`:

- **Code outputs:** every code output in the book comes from really running the code; none was typed by hand.
- **Facts:** no facts, prices or laws were invented. Anything that couldn't be checked was left open, with the
  reason written down.
- **Author's voice:** kept. Only what the findings asked for was changed.

---

## 2. The finished books (what a reader gets)

The book is published as four books, split by part. No chapter is cut across two books.

| Book | Parts and chapters | Pages | File |
|---|---|---|---|
| **1. Theory** | How to Use This Book, Part 0 (Ch 1–6), Part 1 (Ch 7–9). The ideas; no software needed. | 218 | `fixed/Books/Analyst-to-Architect-Book-1-Theory.pdf` |
| **2. Practical** | Part 2 (Ch 10–27) and Part 3 (Ch 28–34). Excel, SQL, Power BI, Python, statistics, dbt. | 1,401 | `fixed/Books/Analyst-to-Architect-Book-2-Practical.pdf` |
| **3. Implementation** | Parts 4–7 (Ch 35–67), then Ch 83. ML, data engineering, production AI, architecture. | 1,318 | `fixed/Books/Analyst-to-Architect-Book-3-Implementation.pdf` |
| **4. Be Interview Ready** | Part 8 (Ch 68–82). How hiring works, plus a question bank for each role. | 400 | `fixed/Books/Analyst-to-Architect-Book-4-Be-Interview-Ready.pdf` |
| Book Overview (internal, not for readers) | Every chapter's skills, time, prerequisites and sections, a flow figure, and routes by role | 71 | `fixed/Books/Analyst-to-Architect-Book-Overview.pdf` |

**What every book has:**

- its own cover;
- a "whole book" map (every chapter, with its book and page);
- its own contents with page numbers;
- a part opening page, with each chapter starting on a new page;
- a chapter map at the start of each chapter, with page numbers.

Books 1–3 share one page count (1 to 2902). Book 4 keeps chapter numbers 68–82 (your decision of 30 Sep).

There is also one PDF per part, in `fixed/Part-0-1/` to `fixed/Part-8/` and `fixed/Closing/`. You chose to keep
them alongside the books.

> **Until the pull requests are merged**, these files are on the `books` branch, not on `main`:
> https://github.com/abhishekvtiwari/DS_BA_Curriculum/tree/books/fixed/Books

---

## 3. The pull requests, and the order to merge them

| PR | What it holds | Merge into |
|---|---|---|
| #1 | Your decisions of 28 Sep (`DECISIONS.md`) | `main` |
| #2 | Setup: unpacked files, `source/BUILD.md` | `main` |
| #3 | Riverstone fact sheet (draft for your approval) | `main` |
| #4 | Layout pass (fonts, covers, tables, contents pages) | `main` |
| #5 | Part 0 + 1, "How to Use This Book", the six-stage chapter structure | builds on #4 |
| #6 | Parts 2 and 3 (Ch 10–34) | builds on #5 |
| #7 | Part 4 (Ch 35–44) | builds on #6 |
| #8 | Part 5 (Ch 45–52) | builds on #7 |
| #9 | Part 6 (Ch 53–59) | builds on #8 |
| #10 | Part 7 (Ch 60–67) | builds on #9 |
| #11 | Part 8 + Closing (Ch 68–83) | builds on #10 |
| #12 | The four books and the overview | builds on #11 |

Merge #1, #2 and #3 first, then #4 to #12 in number order. PRs #5–#12 are stacked, which means each one contains
the one before it. So the **`books` branch (#12) already holds everything**. If you'd rather not merge yet, a new
chat should start from `books`.

---

## 4. Which files to edit for a change (the important part)

Everything for the book lives in **`Data Science/Analyst-to-Architect/`**. All paths below start there.

| You want to change… | Edit this | Format |
|---|---|---|
| Any wording in a chapter | `manuscript/chNN-<title>.md` (one file per chapter, e.g. `ch40-time-series-and-forecasting.md`) | Markdown: plain text, `#` headings, tables with `\|` |
| The "How to Use This Book" section | `manuscript/front-how-to-use-this-book.md` | Markdown |
| A part's opening page (Parts 2–8) | Don't edit it by hand. Edit `tools/make_part_intro.py`, then run it. | Python |
| Part 0 or Part 1 | Edit the chapter files (`ch01`–`ch09`), then run `python tools/collate_parts.py`. `part0-…md` and `part1-…md` are generated from them. | Markdown |
| A chart or diagram | Its script, `figures/make_figsNN.py` (NN = chapter number), then run it to redraw the `.svg` | Python |
| The numbers behind a chart | The checks script, `checks/chNN_check.py`, which writes the results the figure script reads | Python |
| Practice datasets and companion files | `companion/chNN/` (CSV, Excel, scripts the reader downloads) | CSV, XLSX, PY |
| SQL used in a chapter | `sql/` and the chapter's `companion/chNN/` folder | SQL |
| Hours ("Time needed") | `tools/hours_table.py`. This is the one source; Ch 6, Ch 9, Ch 83 and the part pages read from it. | Python |
| Fonts, colours, page layout | `tools/pdf/book.css` (style), `tools/pdf/cover.html` (cover), `tools/pdf/layout.js` (page-break rules) | CSS, HTML, JS |
| Which chapters go in which book, book titles | `tools/pdf/books.py` | Python |
| The internal overview | Don't edit `manuscript/book-overview.md` by hand. Run `python tools/make_overview.py`. | Python |

**Where the record of past changes lives (repo root):**

| File | What it is |
|---|---|
| `changelog/chNN.md` | Every change to chapter NN, one line each. `changelog/chNN-summary.md` is the one-page version. |
| `changelog/part-N-questions.md` | The open questions for you, by part (section 6). |
| `tracker/register.csv` | All 3,822 review findings and their status. After editing it, run `python tracker/make_tracker.py` to refresh `TRACKER.md`. |
| `review/` | The original review. Read only. |
| `DECISIONS.md` | Your decisions. Only you edit it. |
| `source/BUILD.md` | How the build works, with the exact commands. |

---

## 5. How a small change is made (the routine)

1. Edit the chapter's `.md` file. If you change a number, search the other chapters for the same number: the
   book's figures must agree everywhere (e.g. Riverstone 2025 revenue is ₹4,335,471).
2. If code or a chart is affected, re-run the code and paste the **real** output. Then redraw the figure with
   `python figures/make_figsNN.py`.
3. Rebuild and check the chapter:

   ```bash
   cd "Data Science/Analyst-to-Architect"
   python tools/pdf/build.py ch40                           # one chapter, to build/pdf/
   python tools/pdf/layout_check.py build/pdf/<file>.pdf    # page-number, spacing and font checks
   ```

4. Rebuild the books when you're ready to publish:

   ```bash
   python tools/pdf/books.py book1 book2 book3 book4 map    # about 2 hours in all
   python tools/pdf/books.py overview
   ```

   Then copy the PDFs from `build/pdf/` to `fixed/Books/`.
5. Add a line to `changelog/chNN.md`. If the change closes a review finding, update `tracker/register.csv` and
   run `python tracker/make_tracker.py`.

The build needs pandoc, Python with Playwright (Chromium), PyMuPDF and the Poppins and Lora fonts.
`source/setup-toolchain.sh` installs them. Re-running SQL needs PostgreSQL and MySQL;
`tools/setup_databases.sh` loads the practice databases.

---

## 6. What is left

**a) Your decisions (46 findings held "Open").** Each part's questions are in one short file:
`changelog/part-2-3-questions.md` and `part-4-questions.md` to `part-8-questions.md`. Part 0 + 1's questions
are in PR #5. Most come down to a few book-wide calls:

- **The Riverstone fact sheet (PR #3).**
  - The story calendar: which year the later chapters are set in.
  - The production warehouse engine.
  - One exchange rate for the whole book (₹83, ₹87 and ₹88 are all used now).
  - Some names and roles.
- **Facts that need a dated source.** Salaries, prices, laws and model prices that couldn't be checked from here,
  because those websites were blocked. A lawyer's read of Ch 64 (privacy law) is recommended before print.
- **One question-bank level scale** for all of Part 8.
- **Glossary (Appendix A).** Chapters point to it, but it doesn't exist yet.

**b) The final pass (15 approved findings, done in one go at the end):**

- Renumber Parts 2 and 3 to match the reading order. The map is in `CLAUDE.md` §3: for example, old Ch 19
  becomes Ch 12.
- Fix the Part 8 numbering for 72A/76A/76B (D2). Book 4 keeps 68–82, as you decided.
- Rebuild every cross-reference from one generated index.
- Recompute the "Time needed" tables one last time.

**c) Housekeeping.** `fixed/Part-8/` still holds the PDF under its old name ("The Interview Playbook"). Rebuild
it with `python tools/pdf/build.py package-8`, which now names it `Part-8-Be-Interview-Ready`.

---

## 7. Starting a new chat (copy and paste this)

> You are continuing work on the book *Analyst to Architect* in the repo `abhishekvtiwari/DS_BA_Curriculum`.
> The review fixes are finished. Read `HANDOVER.md` first, then `CLAUDE.md` and `DECISIONS.md`. Follow them
> exactly.
>
> **Who you're working with:** a senior data scientist who is also a VP. They know data science well and want
> short, plain answers: what changed, where, and what it affects. No jargon about the tooling unless they ask.
> Give a recommendation when there's a choice.
>
> **Rules that don't change:**
> - Never type a code output by hand. Run the code and paste the real output.
> - Never invent facts, prices, salaries or laws.
> - Keep numbers consistent across chapters.
> - Don't rewrite beyond what was asked; keep the author's voice.
> - Never edit `DECISIONS.md`.
>
> **Where to work:** start from the `books` branch if the pull requests aren't merged yet, otherwise from `main`.
> Make a new branch for your change. For every change:
> 1. Edit the source file named in `HANDOVER.md` §4.
> 2. Rebuild the chapter and run `layout_check.py`.
> 3. Add a line to `changelog/chNN.md`.
> 4. Update `tracker/register.csv` if a review finding is closed, then run `python tracker/make_tracker.py`.
> 5. Commit, push, and open one pull request with a short summary on top.
>
> Rebuild the four books (`tools/pdf/books.py`) only when asked, since it takes about 2 hours.
>
> **My request:** <write the change you want here, e.g. "In Ch 40 §40.4, simplify the explanation of the
> smoothing parameter" or "Apply my answers to the Part 6 questions: …">
