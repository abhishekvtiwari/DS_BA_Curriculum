# Part Brief — The Final Chapters: 25, 26, 27, 83 and the Appendices

*Coordinator, 21 September 2026. One assignment, one owner, one chat.*

---

## 0. Why this brief exists, and why it is late

Every other part of this book is written. Eighty-one chapters and 811,645 words exist and are approved. These four chapters are the hole, and the reason is worth stating plainly so it does not happen again.

The original Part II brief assigned Chapters 10 to 27 to a single chat and suggested splitting it in two. Only one chat was ever started. It wrote its slice, continued through Chapter 24, and on 19 September was asked to write Part VII instead. It did that well, eight chapters in two days. But it was the chat that owned 25, 26 and 27, and nothing was reassigned when it moved. The gap stayed invisible because the three chapters sit at the *end* of Part II, the bundle arrived labelled complete, and nothing downstream failed.

Chapter 83 and the appendices are a separate failure: `planning/parts/part-closing-appendices-brief.md` has existed since the plan was written and no chat was ever started from it. That is also how Chapter 67 came to declare itself the final chapter of the book.

The coordinator recorded the gap on 19 September and repeated it in six bundle READMEs without ever turning it into an assignment. This brief is that assignment.

## 1. You have an advantage nobody else had

Every previous part chat wrote forward into a book that did not exist yet. You are writing into a finished one. All 81 chapters are in your bundle. **Read what points at you before you write a word.** Three of your four chapters are more heavily promised than anything else unwritten:

| Chapter | Named in other chapters | Times | The problem this creates |
|---|---|---|---|
| **26** The Professional Toolkit | 21 chapters | 46 | The most-promised chapter in the entire book |
| **25** The Business Analyst Track | 8 chapters | 24 | An approved question bank (76B) was written against it |
| **27** Capstone: Your Analyst Portfolio | 4 chapters | 10 | Every Part II project was designed to feed it |
| **83** The Long Game | 1 chapter | 1 | Chapter 67 currently claims its job |

Your first task is not writing. It is reading every one of those references and building a list of what you owe. `planning/promises-from-approved-chapters.md` has them all, extracted; the chapter files are in `manuscript/`.

## 2. Scope and order

Write in this order. Each one depends on the one before it.

1. **Chapter 25 — The Business Analyst Track** (class C, blueprint 5,000 words)
2. **Chapter 26 — The Professional Toolkit: Git, Agile, Documentation & AI Assistants** (class C, blueprint 4,000; expect to need more, see §4)
3. **Chapter 27 — Capstone: Your Analyst Portfolio** (class D, blueprint 3,000)
4. **Chapter 83 — The Long Game** (class C, blueprint 2,500) and **Appendices A to H**, per `planning/parts/part-closing-appendices-brief.md`, which already exists and stands

Chapter 25 first because it unblocks a re-check on an approved chapter. Chapter 27 last of the three because it collects the other two.

## 3. Chapter 25 — The Business Analyst Track

**Blueprint scope, verbatim:** What BAs do and how it differs from data analysts · the software development life cycle (SDLC) · process mapping (flowcharts, swimlanes, BPMN basics) · use cases and user stories, acceptance criteria · BRD, FRD, and SRS documents · gap analysis · UAT · working with IT and vendors · domain knowledge · identifying and prioritizing automation opportunities, and writing requirements for an automation.
**Project:** Map Riverstone's order-to-cash process and write user stories for one improvement.

**Read first, and this one is not optional: `manuscript/ch76b-business-analyst-question-bank.md`.** It is approved, and it was written against a Chapter 25 that did not exist, including its section numbers. That is backwards, and it is also useful: the bank tells you exactly what a reader is expected to be able to answer after your chapter. Make the chapter deliver what the bank tests. Where the bank assumed something you disagree with, say so in your report and the coordinator will fix the bank instead. This is cross-part issue 23.

**Promises you must keep, quoted:**

- *Ch 3:* "The book returns to each of Riverstone's manual steps … and the full process map in Chapter 25." Chapter 3 also ends a section with "Keep it for Chapter 25." **Chapter 3 built the order-to-cash walk and figure 3-2. Your process map is the formal version of that same journey, not a new one.**
- *Ch 8:* the skills matrix has a Business Analyst row pointing at you for "mapping processes, finding and prioritizing automation opportunities, writing automation requirements".
- *Ch 22:* "Chapter 25: experimentation in practice, where the constraints are organizational as much as statistical."
- *Ch 23:* "process mapping and requirements gathering, which is how a KPI tree gets built collaboratively rather than assumed."
- *Ch 24:* "requirements gathering formalized further, with process mapping, user stories, and the documents (BRD, FRD, SRS) that a full BA role produces."

**Do not re-teach:** stakeholder mapping, the pyramid principle, the one-page memo or handling pushback. Chapter 24 did all of that thoroughly. You pick up where it stops, at the formal artifacts.

**Riverstone material to use:** the order-to-cash process from Chapter 3, the four branch sales offices from Chapter 14, the manual steps listed across Chapter 3 and Chapter 19, and the automation inventory template in `companion/ch63/`. Chapter 63 covers automation *governance* at architect level; you cover finding and writing requirements for one automation at analyst level.

## 4. Chapter 26 — The Professional Toolkit

**Blueprint scope, verbatim:** Git and GitHub hands-on · reproducibility · documentation that people read · Agile, Scrum, Kanban, Jira in practice · working with AI coding and writing assistants: what to delegate, how to check the output, data-privacy rules.
**Project:** Put all Part II work in one repository with a README.

**This is the hardest chapter of the four.** Twenty-one chapters send the reader here, and they ask for different things:

| What is promised | Who promised it |
|---|---|
| Git and GitHub hands-on, version control for scripts and queries | Ch 2, 5, 6, 12, 13, 17, 18, 19, 20 |
| Pull requests and review | Ch 28, 29, 32 |
| `.env` files and keeping secrets out of the repository | Ch 19, 20, 29 |
| A README and a repository that another person can run | Ch 13, 20, 27 |
| Continuous integration, with GitHub Actions named | Ch 29, 32, 52 |
| Documentation that is findable months later | Ch 23, 24 |
| A SQL pattern library kept in Git, one file per pattern | Ch 13 |
| AI assistants at work: what to delegate, how to check | Ch 5, 6, 7 |
| A place for the portfolio to live | Ch 8, 9, 27 |
| The terminal, used for Git | Ch 34 |

**The blueprint's 4,000 words will not carry that.** Write it at the length it needs, which is likely 6,000 to 8,000, and report the number. Length is not the risk here; scope creep into other chapters is.

**Do not re-teach, and say where each lives instead:**

- **The command line** belongs to Chapter 34. You use `git` commands at a terminal; you do not teach the shell.
- **Packaging, tests, type checking and project layout** belong to Chapter 29. You teach a repository with a README, not a Python package.
- **CI/CD, Docker, Kubernetes and Terraform** belong to Chapter 52. You may show one small GitHub Actions workflow that runs a check on push, because three chapters promise it, and then point at Chapter 52.
- **How large language models work, and building with them,** belong to Chapters 54 and 55. You cover working *with* an assistant professionally.

**The sequencing constraint that matters most.** In reading order this chapter sits inside Part II, so it is written for someone who has finished Parts 0 to II and has never seen Chapters 29, 34 or 52. Everything must work at that level. Forward references are fine and expected; assumed knowledge is not.

**On AI assistants,** Chapter 6 already set rules for learning with an assistant. Yours is the professional version: what to delegate, how to verify output you did not write, what must never be pasted into a third-party tool, and how that interacts with the privacy rules in Chapter 64. Keep it concrete and keep it about judgment.

## 5. Chapter 27 — Capstone: Your Analyst Portfolio

**Blueprint scope, verbatim:** End-to-end Sales Intelligence project: SQL → cleaning → Python automation → Power BI dashboard → statistical insight → memo · how to present portfolio projects · what "job-ready" looks like.

**Read `manuscript/ch44-capstone-an-end-to-end-data-science-project.md` before you start.** Chapter 44 is Part IV's capstone and it is good. Yours must be visibly a different thing: Chapter 44 is a machine-learning project ending in a call list; yours is the *analyst* arc, ending in a dashboard and a memo, using only what Parts 0 to II taught. Read it so you do not repeat its shape, its framing table, or its ending.

**Promises:**

- *Ch 8:* "The projects at the end of every chapter in Part II are designed for this, and Chapter 27 turns them into a portfolio."
- *Ch 9:* "Every chapter project in this book is designed to become a portfolio piece."
- *Ch 22:* "Chapter 27: the ethics of analysis, including selective reporting." **This one is easy to miss and it is the most interesting thing in your chapter.** A portfolio is where selective reporting is most tempting: showing the model that worked, hiding the four that did not.

**Class D means a project chapter, not a teaching chapter.** Recap is explicitly allowed and should be labelled as recap, the way Chapter 44 §44.2 does. Nothing new is taught except the presentation of work.

## 6. Chapter 83 and the Appendices

`planning/parts/part-closing-appendices-brief.md` already covers these and stands. Three additions:

1. **Chapter 67 currently claims to be the final chapter of the book**, five times, and misnames Part VIII. That is cross-part issue 20, owned by the Part VII chat, not by you. Write Chapter 83 as the closing chapter it is.
2. **After renumbering, Chapter 83 becomes Chapter 85.** Part VIII grew from 15 chapters to 17. Write "the closing chapter" rather than a number wherever you can.
3. **Appendix G is bigger than it looks.** Sixty-two chapters carry an answers section, about **95,636 words** in total. Collating them is a mechanical but substantial job, and it should be scripted rather than done by hand. Raise it with the coordinator before starting; it may be better done at assembly, by script, than written now.

## 7. The standards that apply

All of `planning/chapter-writing-instructions.md`, and three sections especially:

- **§4** the fourteen-section chapter template.
- **§5.2** the mechanics. American spelling, no em dashes in prose, and none of *genuinely*, *honestly*, *straightforward*, *just*, *simply*, *easy*, *obviously*, *powerful*. Two parts drifted badly on this and are being repaired; do not add to it. Run the scan yourself over each chapter before you call it done.
- **§6.5** teach code line by line. Chapter 26 is the one of yours with real code, and it matters there: `git` commands are code, and a reader meeting `git rebase` or `--force` for the first time needs to know what each part does and what happens if they change it. **A settings table and a measured what-if are required.** One chapter in 81 currently has that table. Be the second.
- **§15** the Definition of Done, including `python3 tools/check_code_teaching.py` reporting no unexplained blocks.

## 8. What to report back

A status file, `planning/parts/final-chapters-status.md`, in the shape the other parts used: one report per chapter with word count, sections, what was verified and how, manual checks still open, promises delivered, promises made, new Riverstone facts proposed, and anything found wrong in other chapters.

Two specific things the coordinator needs from you:

- **For Chapter 25:** whether Chapter 76B's assumptions hold, and which of its questions your chapter does not answer.
- **For Chapter 26:** the final word count and what you cut to stay inside the scope boundaries in §4.

## 9. Kickoff prompt

Paste this into a new chat attached to the *Data Science* project, with the complete book bundles attached.

```
You are writing the last four chapters of the book "Analyst to Architect": Chapters 25, 26, 27
and 83, plus Appendices A to H. Every other chapter is written: 81 chapters, 811,645 words, all
approved. You are filling the only hole left in the book.

1. Read planning/parts/final-chapters-brief.md in full. It is your assignment.
2. Read planning/chapter-writing-instructions.md in full, then planning/chapter-map.md (note the
   reading order at the top, which is not the chapter numbers), planning/cross-part-issues.md,
   and planning/riverstone-bible-additions.md.
3. Before writing anything, build your list of what you owe. Chapter 26 is named 46 times across
   21 chapters; Chapter 25, 24 times across 8; Chapter 27, 10 times across 4. Read every one of
   those references in the manuscripts and write down what each one promised the reader.
4. Read the reference chapters for your classes: ch01 and ch02 for class C, ch44 for the class D
   capstone. Read ch24 before Chapter 25, ch76b before Chapter 25, and ch34, ch29 and ch52 before
   Chapter 26 so you know exactly where your scope stops.
5. Write Chapter 25 first and send it for approval before starting Chapter 26.

Rules that matter here more than usual:
- You are writing into a finished book. Every chapter you reference exists and can be checked.
  Quote section numbers, not chapters, wherever you can.
- Do not re-teach what another chapter owns. Section 4 of your brief lists the boundaries for
  Chapter 26, which is the chapter most at risk of sprawling.
- Section 6.5 applies: code taught line by line, a settings table with "what happens if you change
  it", and one measured what-if. One chapter in 81 has that table. Be the second.
- Run the style scan yourself before calling a chapter done: no em dashes in prose, no banned words.
```

## 10. Sequencing

| When | What |
|---|---|
| Now | Chapter 25 written, approved, and Chapter 76B re-checked against it |
| Then | Chapter 26, at whatever length its 46 promises need |
| Then | Chapter 27, after reading Chapter 44 |
| Then | Chapter 83, and a decision with the coordinator on whether Appendix G is written or scripted at assembly |
| Alongside | The coherence pass (`planning/coherence-pass-strategy.md`) runs on the other 81 chapters. These four join the second reading, once written |
| After | Renumbering and assembly: the book becomes 85 chapters |
