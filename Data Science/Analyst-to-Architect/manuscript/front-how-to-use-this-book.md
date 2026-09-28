# How to Use This Book

## Who this book is for, and how it's built

This book starts from "what is data?" and ends with the work of a data architect: the person who decides how a whole company's data is collected, stored, checked, and put to use. It assumes no technical knowledge at all. If you can use a phone and add up a shopping bill, you can start at Chapter 1.

One company runs through every chapter: **Riverstone Supplies**, a fictional company that makes and sells plastic storage boxes, kitchenware, crates, and furniture to shops, hotels, and wholesalers. You'll meet its people, follow its orders from enquiry to cash, and answer its questions, first by hand, then with each new tool. Because the company stays the same, each new skill lands on a problem you already understand, and you can check a new answer against one you worked out before.

Tools arrive one at a time, in the chapter that first needs them. Parts 0 and 1 need no software at all. From Chapter 10 on, each chapter that brings a new tool starts by installing it and checking it works with one small first step. Every idea follows the same order: the plain idea first, then worked by hand, then in a tool you already know, and only then in a new tool, one line at a time.

---

## How each chapter is laid out

Every teaching chapter has the same six stages, in the same order, so you always know where you are. A coloured label at the top of each stage names it, and the box at the start of the chapter lists them with their page numbers.

- **Chapter at a glance.** A box at the top with five lines: *You will learn to* (what you'll be able to do by the end), *Before you start* (the chapters it builds on), *Time needed* (an honest estimate, including the exercises and the project), *Tools* (what you need, often only a pen and paper), and *Practice data* (the files the chapter uses). Under it, **In this chapter** maps the stages below, with page numbers.

**Start**

- **Why this matters.** Why the chapter's skill is worth your hours, in a work setting.
- **In plain English.** The chapter's main idea through an everyday picture, such as a kitchen, a hospital, or a shop receipt, before any technical words.

**Learn**

- **Numbered sections** (1.1, 1.2, and so on). The teaching itself, one idea at a time, each worked through with Riverstone's data.
- **Boxes** inside the sections, each with a label that tells you what kind it is:
  - **Watch out:** a mistake that's easy to make, and how to avoid it.
  - **Try it:** a short task to do right now, before reading on.
  - **Simplification note:** where the book has simplified something on purpose, and what the fuller picture is.
  - **Real-life example:** the idea at work in a real kind of job or company.
  - **Tool note:** a detail about one tool or version, such as a feature that only some versions have.
  - **Interview extra point:** something that sets an answer apart in a job interview.

**Apply**

- **Common mistakes.** A table of the usual errors, the symptom each one shows, and the fix.
- **In the real world.** A short story from Riverstone in which someone uses the chapter's ideas on a real problem.
- **Project.** A larger piece of work that uses the whole chapter, with a clear goal and a deliverable. It opens with *Tools you'll need*: the software and files it uses, and where to get them.

**Review**

- **Recap.** The chapter's main points in a few lines, to revise from.
- **Key terms.** Every new term the chapter introduced. Use it to test yourself: can you explain each one out loud?
- **Check yourself.** A checklist. If you can tick every line, you're ready for the next chapter.

**Practise**

- **Exercises.** Four groups of exercises (see the next section).
- **Answers.** Worked answers to every exercise.

**Next**

- **Where this leads.** Which later chapters build on this one, and which parts of the interview chapters it prepares you for.

A few chapters, such as the capstones and the interview chapters, adapt this layout to their job. They say so at the start.

---

## The four exercise groups, and the answers

Every teaching chapter's Practise stage has exercises in four groups:

| Group | What it's for | How to use it |
|---|---|---|
| **Warm-up** | checks you understood the basics | do them right after reading; they should take a few minutes each |
| **Core** | the skills the chapter exists to teach | do all of them; this is where most of the learning happens |
| **Stretch** | harder, closer to real work | do at least one; come back to the rest on a second pass |
| **Think about it** | judgment, with no single right answer | write a short answer, then compare it with the model answer |

Each chapter's answers follow its exercises. To get the most from them:

- **Write your answer before you look.** Even a partial answer. Reading an answer you haven't attempted feels like learning and isn't.
- **Compare the reasoning, not only the number.** Many answers show a method or a check (like "✓ reconciles to the total"); copy the method.
- **Mark the ones you got wrong or guessed**, and redo them on Sunday from a blank page.
- **For code exercises, run your version.** If it gives the same result by a different route, that's often fine; if it gives a different result, find out why before moving on.

---

## How to read code and its output

Parts 0 and 1 contain no code. You'll work everything out by hand, with a pen, a calculator, and the tables on the page.

From Chapter 10 on, you'll meet **code**: short instructions you type for a spreadsheet, a database, or a programming language. The book shows code the way you'll use it, one small step at a time. Each step has three parts, always in this order.

**1. The code block.** The instructions you type, in a shaded box with a coloured bar down its left edge:

```code
[Placeholder: from Chapter 10 on, the instructions you type appear in a box like this one.]
```

**2. The output block.** What the computer printed when that code was run, in a plain white box with a dashed border, directly below it:

```text
[Placeholder: the output appears here, exactly as the computer printed it.]
```

**3. How it works.** The explanation, line by line: what each line does, and what each part of it means.

Four promises come with every code block.

- **The output is real.** Every block was run, and the output is what it actually printed. Nothing was typed in by hand.
- **One new idea per block.** A block adds one thing to what you already know, never five at once.
- **Every line is explained.** If a line appears, the text says what it does and what each part of it means.
- **Differences are shown side by side.** The book uses two databases, called PostgreSQL and MySQL (Chapter 12 introduces both). Where they need different code for the same job, you'll see both versions next to each other, labelled.

The best way to read a code block is to type it yourself, run it, and compare your output with the book's. If yours is different, the difference is worth finding before you move on: it's usually a typo, and sometimes it's a lesson.

---

## How the parts climb

The book has nine parts and a closing chapter. Each part assumes the ones before it.

- **Part 0 — First Principles: Data from Zero** (Chapters 1–6). What data is, how computers store and move it, how a business runs on it, numbers without fear, thinking like an analyst, and planning your learning.
- **Part 1 — The Map** (Chapters 7–9). The data jobs, how skills unlock them, and how expertise forms.
- **Part 2 — The Analyst** (Chapters 10–27). Spreadsheets, SQL (the language for asking a database questions), cleaning data, charts, Power BI dashboards, the Python programming language, statistics, business skills, and a portfolio. **The end of Part 2 is where "job-ready" ends**: it covers the skills of a first analyst job.
- **Part 3 — Advanced Analytics & Analytics Engineering** (Chapters 28–34).
- **Part 4 — Machine Learning & Data Science** (Chapters 35–44).
- **Part 5 — Data Engineering, Integration & Scale** (Chapters 45–52).
- **Part 6 — Production ML, Generative AI & MLOps** (Chapters 53–59).
- **Part 7 — Architecture, Governance & Leadership** (Chapters 60–67).
- **Part 8 — The Interview Playbook** (Chapters 68–82). How data hiring works, and question banks for each role.
- **Closing** (Chapter 83). The long game: what the whole path costs, and how to keep going.

Parts 3 to 7 are branches, not a ladder you must climb to the top. Which ones you need depends on the job you want, and Chapter 8 shows which parts lead to which roles. Complete beginners should start at Chapter 1 and read in order. If you already work as an analyst, skim Parts 0 to 2 and start fully at Part 3. Chapter 8, section 8.7, has a route for each role.

---

## A rough sense of time

Adding up every chapter's *Time needed* line, the book's own estimates put the end of Part 2 at **317 to 394 hours**: at six hours a week, about 12 to 15 months. Chapter 6 turns that into a plan for your week.

---

## The companion files and a tidy folder

The **companion files** hold every dataset, spreadsheet, and script the book uses. Each chapter's *Tools* and *Practice data* lines name the files that chapter needs, so you never have to guess. Appendix E gives the address to download them from and lists every file.

Two sets of Riverstone data run through the early chapters. The **mini database** has Riverstone's first three months of 2026: twelve orders, small enough to check by hand. The **one-year database** has all of 2025: 173 orders, big enough to show real patterns. Every table of Riverstone numbers in the book says which one it comes from.

Set up one home for everything on your computer, and keep it that way:

```text
analyst-to-architect/
    companion/            the downloaded companion files, unchanged
    work/
        ch10/             your own files for each chapter
        ch12/
        ...
    notes/                your study log, plans, and questions
```

Two rules keep it useful. **Never edit the companion files themselves**: copy what you need into `work/` first, so you can always start again from a clean copy. And **name your own files the way Chapter 2 (section 2.4) will show you**: dates as year-month-day, lower-case words joined with hyphens or underscores, and no "final".

Three habits with files save hours. Chapter 2 explains the ideas behind them; set them up now.

- **Show file extensions.** An extension is the short ending of a file's name, such as `.csv` or `.xlsx`, that says what kind of file it is. Many computers hide it, so `orders.csv` appears as plain `orders`. Turn that off in your computer's file settings.
- **Know how to copy a file's full path.** A path is a file's complete address, from the drive down through each folder to the file. On Windows, hold `Shift`, right-click the file, and choose *Copy as path*. On a Mac, select the file and press `Option+Cmd+C`.
- **Unzip a download before opening what's inside it.** Opening a file directly from inside a zip file is a common cause of "my changes disappeared".
