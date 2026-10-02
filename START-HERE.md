# Start here

_Your local copy. Last updated 2 October 2026._

This folder is the whole project on your laptop: the books to read, the review state to track, and
the manuscript the fixes go into. GitHub holds the same thing as the permanent store. You do not
need to open GitHub to see where anything stands.

Everything below is a real file in this folder. Click it, or open it from Explorer.

---

## 0. The review bundle

Everything assembled in one place, outside this folder so it can be moved or sent:

**`Desktop\Projects\Analyst-to-Architect-Review-Bundle\`** — 794 files, 285 MB, in five numbered
folders. Open **`00-Read-me-first.pdf`** inside it. There is also a
**`…-Review-Bundle.zip`** (214 MB) beside it if you want to move it to another machine.

It holds the four books, the practice material, the topic guide, what changed recently, and the
review state. The read-me says what I would most like you to look at, and what I already know is
missing.

**The practice material is now arranged by tool, not by chapter.** `04-Practice-Arena/` has ten
tools — Excel, SQL, Python, statistics, machine learning, data engineering, GenAI, the command
line, architecture, take-homes — each running from the smallest idea to a finished thing you can
run. Chapter numbers are gone from the folder names, and `WHERE-IS-MY-CHAPTER.md` turns any
reference in the book back into a folder. The chapter-by-chapter view still exists in this
repository, unchanged, because the book refers to it by name.

The same documents are in [review/for-abhishek/](review/for-abhishek/) here, if you would rather
not leave this folder.

---

## 1. Read the books

The five PDFs with the fixed navigation are in **[fixed/Books/](fixed/Books/)**. These are the ones
to read. Each one's contents page lists only its own chapters, every line is clickable, and the
series map sits at the back.

| Book | File | Pages | Bookmarks |
|---|---|---|---|
| 1 · Theory | [Analyst-to-Architect-Book-1-Theory.pdf](fixed/Books/Analyst-to-Architect-Book-1-Theory.pdf) | 218 | 359 |
| 2 · Practical | [Analyst-to-Architect-Book-2-Practical.pdf](fixed/Books/Analyst-to-Architect-Book-2-Practical.pdf) | 1,401 | 1,616 |
| 3 · Implementation | [Analyst-to-Architect-Book-3-Implementation.pdf](fixed/Books/Analyst-to-Architect-Book-3-Implementation.pdf) | 1,318 | 1,447 |
| 4 · Be Interview Ready | [Analyst-to-Architect-Book-4-Be-Interview-Ready.pdf](fixed/Books/Analyst-to-Architect-Book-4-Be-Interview-Ready.pdf) | 535 | 724 |
| Overview (internal, not for sale) | [Analyst-to-Architect-Book-Overview.pdf](fixed/Books/Analyst-to-Architect-Book-Overview.pdf) | 71 | 99 |

**Book 4 was rebuilt on 3 October** and now carries ten new predict-the-output sections across
Part VIII; all 169 of its contents links and 724 bookmarks were checked to land on the right page. The others are the 1 October build.

Two reading notes, so the navigation behaves the way you expect:

- Use the **contents page**, or the PDF reader's own bookmark sidebar. Both now land on the right
  page at the right height.
- Book 2 and Book 3 are 80 MB each. They open fine in a desktop reader; a phone browser will be
  slow. For a phone, open the per-part PDFs in [fixed/](fixed/) instead — same content, split up.

Per-part PDFs, if you want a smaller file: [fixed/Part-0-1/](fixed/Part-0-1/),
[fixed/Part-2/](fixed/Part-2/), [fixed/Part-3/](fixed/Part-3/), [fixed/Part-4/](fixed/Part-4/),
[fixed/Part-5/](fixed/Part-5/), [fixed/Part-6/](fixed/Part-6/), [fixed/Part-7/](fixed/Part-7/),
[fixed/Part-8/](fixed/Part-8/), [fixed/Closing/](fixed/Closing/).

---

## 2. Track where the review stands

| What you want to know | Open this |
|---|---|
| How much is done, by part and by chapter | **[TRACKER.md](TRACKER.md)** |
| What you have already decided | **[DECISIONS.md](DECISIONS.md)** |
| What is still waiting on you | **[DECISIONS-BRIEFING.md](DECISIONS-BRIEFING.md)** |
| What was changed in a chapter, and why | **[changelog/](changelog/)** — one file per chapter |
| The findings as a spreadsheet | **[review/Book-Review-Action-Register.xlsx](review/Book-Review-Action-Register.xlsx)** |
| Whether the review inputs are complete | **[REVIEW-STATUS.md](REVIEW-STATUS.md)** · **[REVIEW-GAPS.md](REVIEW-GAPS.md)** |

**As of the last tracker run (30 September 2026): 3,761 of 3,822 findings closed, 98%.**
Verified 3,152 · Fixed 609 · Approved and ready to fix 15 · Open 46.

Your decisions are already recorded: global rule **A1** is ticked, all 26 themes (T1–T14, V1–V12)
carry a decision, and all eight structural decisions **D1–D8** are approved. Nothing in the fix
queue is blocked on you.

---

## 3. The reading review, in long form

[review/reader-journey/](review/reader-journey/) holds the chapter-by-chapter read-through.

- [journey-findings.docx](review/reader-journey/journey-findings.docx) — **the readable copy**, open
  this one
- [journey-findings.md](review/reader-journey/journey-findings.md) — the same text as markdown
- [register-candidates.csv](review/reader-journey/register-candidates.csv) — 130 findings proposed
  from that read, for the register
- [red-team-code-teaching.md](review/reader-journey/red-team-code-teaching.md) — where the code
  teaching is weakest

Covers Part 0 through Part VII. **Part VIII is not yet read**, which is the part now being
rewritten anyway.

---

## 4. What is being worked on right now

**Book 4, the interview book.** You asked for it to be ground down from very basic to very
detailed, with output-prediction and trick questions of the `int("25", 4)` kind.

**The measurement that set the task.** Thirteen of the fourteen Part VIII banks had no
predict-the-output section at all. The one that did — Chapter 72's §72.2 — became the template.

**Done: ten new sections, 202 new questions.** Part VIII goes from 565 coded questions to 767.
Chapters 70, 71, 72A, 73, 74, 75, 77, 78, 79 and 80 each gained a section aimed at what that
chapter genuinely lacked, rather than a fixed quota.

**Three banks were deliberately left alone** — 76A is career positioning with no technical content,
81's one numeric topic is already covered by its Q81-024, and 82 has no coded questions at all.

**One decision is yours:** whether Chapter 76B should get an ambiguity-drill section, which is the
BA equivalent but a different format. It is explained in
[the Part VIII summary](review/for-abhishek/Part-VIII-predict-the-output-summary.pdf).

Every answer was run before it was written down. About a dozen drafted questions turned out wrong
and the runs caught them — a `RANK` answer that was 4,4,4 rather than 1,1,1, a `257 is 257` that is
`True` because the compiler folds literals, and a float-money question cut entirely because the
trap does not fire at that scale. Each is recorded in its chapter's changelog.

Two things are honestly outstanding rather than finished:

- **PostgreSQL and MySQL are not installed here**, so §71.11's confirming run has not happened. Its
  outputs are labelled "Run (riverstone_2025)" rather than "Verified", and four questions are
  marked **Dialect split**. **Excel is not installed either**, so §70.9 carries the same kind of
  mark on four questions, reading **Check in Excel**. Both exceptions are stated in the chapters'
  own at-a-glance boxes, not buried in a changelog.
- **Book 4 has been rebuilt** — 535 pages, up from 400, with the series map regenerated from the
  page numbers printed on the pages. This machine does not reproduce the original build exactly (a
  test rebuild of Book 1 came out 217 pages against the shipped 218, because fonts resolve
  differently here), so only Book 4 was rebuilt and its visual check should be redone. Books 1–3
  still carry a series map whose Book 4 page numbers predate this.

---

## 5. How this folder and GitHub line up

- This folder is a full clone. The working branch is **`books`**, and it holds everything.
- It is currently **clean**: nothing changed locally that is not also on GitHub.
- To pull the latest after a work session: open a terminal here and run `git pull`.
- To see what changed since you last looked: `git log --oneline -20`.

If a file you expect is missing, it is almost certainly on a branch rather than gone. Nothing in
this project gets deleted.

---

## 6. The rest of the folder

One thing about the layout is genuinely confusing, so it is worth saying plainly: the **manuscript
and the practice files sit one level down**, inside
[Data Science/Analyst-to-Architect/](Data%20Science/Analyst-to-Architect/). So there are two folders
called `Analyst-to-Architect`, this one and that one. The inner one is the book's own working tree
and came in that shape with the delivered packages; the outer one is the clone. Nothing is wrong,
but if you go looking for `manuscript/` at this level you will not find it.

| Folder | What is in it |
|---|---|
| [Data Science/Analyst-to-Architect/manuscript/](Data%20Science/Analyst-to-Architect/manuscript/) | The 85 chapter source files. This is what edits are made to. |
| [Data Science/Analyst-to-Architect/companion/](Data%20Science/Analyst-to-Architect/companion/) | The practice material: notebooks, `.sql` files, datasets, the Riverstone databases |
| [Data Science/](Data%20Science/) | The original approved part-by-part packages, as delivered, plus their PDFs |
| [changelog/](changelog/) | One entry per chapter, recording every change and its verification |
| [tracker/](tracker/) | `register.csv`, the 3,822 findings, and the script that builds TRACKER.md |
| [review/](review/) | Every review pass: content, visual, sequence, reader journey |
| [source/](source/) | Where the sources are, and how to rebuild |
| [fixed/](fixed/) | The rebuilt PDFs, by part and as whole books |
| [build/](build/) | Build scratch space; nothing to read here |
