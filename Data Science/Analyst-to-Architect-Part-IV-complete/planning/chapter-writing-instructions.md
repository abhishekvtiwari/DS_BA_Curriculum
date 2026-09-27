# Chapter Writing Instructions — Analyst to Architect

**Read this whole file before writing anything.** It is the standing brief for every chat that writes part of the book. It exists so that many chats, working in parallel on different parts, produce chapters that read as if one careful author wrote them all, at the quality of the four approved reference chapters.

- **Version:** 1.0 · 16 September 2026
- **Owner:** Abhishek Tiwari (author). The coordinating chat maintains this file; part chats don't edit it.
- **Reference chapters (the quality bar):** Chapter 1 *What Is Data?* · Chapter 2 *How Computers Store, Move and Protect Data* · Chapter 12 *Databases & SQL Foundations* · Chapter 13 *SQL for Real Analysis*. All four are in the project under `manuscript/`. When this file and a reference chapter seem to disagree, follow the reference chapter and report the conflict.

---

## 0. How to use this file

### 0.1 The working model: one chat per part

The book is written **one part per chat**. Each part chat writes the chapters of its part **in order**, one after another, and hands each finished chapter to the author for approval. A separate **coordinating chat** owns the shared planning files, merges updates, and renumbers chapters when the structure changes.

| Chat | Writes | Part brief to read |
|---|---|---|
| Part 0 | Chapters 3–6 (1 and 2 are approved) | `planning/parts/part-0-brief.md` |
| Part I | Chapters 7–9 | `planning/parts/part-1-brief.md` |
| Part II | Chapters 10–27 (12 and 13 are written) | `planning/parts/part-2-brief.md` |
| Part III | Chapters 28–34 | `planning/parts/part-3-brief.md` |
| Part IV | Chapters 35–44 | `planning/parts/part-4-brief.md` |
| Part V | Chapters 45–52 | `planning/parts/part-5-brief.md` |
| Part VI | Chapters 53–59 | `planning/parts/part-6-brief.md` |
| Part VII | Chapters 60–67 | `planning/parts/part-7-brief.md` |
| Part VIII | Chapters 68–82 (question banks) | `planning/parts/part-8-brief.md` |
| Closing & appendices | Chapter 83, Appendices A–H (last) | `planning/parts/part-closing-appendices-brief.md` |

Part II (18 chapters) and Part VIII (15 chapters) are large. The author may split each into two chats; the part briefs show the suggested split.

### 0.2 Files every part chat reads at the start

1. **This file**, in full.
2. **Your part brief** (`planning/parts/…`): your chapters, what earlier chapters promised about them, the data and tools you'll use, and your kickoff prompt.
3. `planning/chapter-map.md`: every chapter's stable ID, number, depth class, status, and file name.
4. `planning/blueprint.md`: the master plan, especially section 7 (your chapters' scope), section 6 (Riverstone datasets), section 8 (Part VIII format), and section 13 (decisions).
5. `planning/promises-from-approved-chapters.md`: every forward reference that written chapters make ("Chapter 20 takes this exact query…"). **Your chapters must deliver what was promised.**
6. At least one **reference chapter** of the same depth class as the chapter you're writing (section 3), read in full before your first chapter, and skimmed again before each new one.

### 0.3 Before you start each chapter

Say, in one short message to the author, which chapter you're starting, its depth class, its planned sections, and any decision you need from them (section 13). Then work through the **workflow in section 12**, and finish with the **definition of done in section 15**.

---

## 1. The book in one page

- **Title:** *Analyst to Architect* (working subtitle: *From Zero to Data Architect: The Complete Path, with the Interview Playbook*). Author: Abhishek Tiwari.
- **Promise:** take a reader who knows only roughly what data is, and has **no tool knowledge**, all the way to job-ready data analyst, then along the branches to data scientist, data engineer, AI engineer, and **data architect**, and make them **interview-ready** at every step. The book is for sale and for the author's own use, so it must be accurate, current, and useful at work.
- **Size and shape:** 83 chapters in 9 parts plus appendices, about 500,000 words, published as 4 volumes. See `planning/chapter-map.md`.
- **Running example:** **Riverstone Supplies**, a fictional Indian manufacturer and distributor. Every chapter uses its data and people where it can (section 7).
- **Threads that run through every part:**
  1. **Automation and data flow.** At every level, show how the manual work in a process (copy-paste, re-keying, emailed files) can be automated: refreshable queries, scheduled reports, reports in the email body, dashboards, alerts, and pushing data into other systems. Toward the architect level, this becomes automation architecture and governance.
  2. **Spreadsheets side by side.** Excel (Microsoft 365) and Google Sheets are taught together, including macros, VBA, Office Scripts, and Google Apps Script.
  3. **SQL in two databases.** PostgreSQL is primary; MySQL is shown alongside wherever SQL appears.
  4. **Business judgment.** Every technique ends in a decision someone can make.
  5. **Honest checking.** Hand-check a number, reconcile a total, question the data.
- **Interview preparation lives in Part VIII only.** Teaching chapters don't contain interview Q&A. They may end with a pointer to the matching question bank, and may include **at most one** short *Interview extra point* callout (as Chapters 12 and 13 do).

---

## 2. Decisions and defaults in force (don't reopen them)

| # (blueprint §13) | Decision or default | What it means for your writing |
|---|---|---|
| 1 | Market: India-first, globally understandable | ₹, Indian cities and business context; explanations that make sense anywhere |
| 2 | Spelling: **American English** | *analyze, color, modeling, center, license (noun), catalog* |
| 3 | Format: master manuscript, published as 4 volumes | One Markdown file per chapter; PDFs built per chapter |
| 4 | Title kept; new subtitle | as in section 1 |
| 7 | Companion repository: public | companion files contain nothing private |
| 8 | Automation tools | Python for code-based automation; Power Automate as the main low-code example, n8n as the open-source alternative |
| 9 | Spreadsheet versions | Excel for Microsoft 365 on Windows as the main version (Mac differences noted), Google Sheets side by side |
| 10 | SQL databases | PostgreSQL primary; MySQL alongside (install, dialect section, tested MySQL companion files) |
| 11 | Chapter depth | *Depth varies* (section 3) |
| — | Reader setup standard (Chapter 6) | Python 3.13 or 3.14 from python.org (Windows: Python install manager); one virtual environment `.venv` in the reader's `analyst-to-architect/` folder; install with `python -m pip install`; base packages pandas, openpyxl, matplotlib, jupyterlab; VS Code with the Python and Jupyter extensions; PostgreSQL 18 / MySQL 9.7 LTS with DBeaver Community; Power BI Desktop from the Microsoft Store (Mac: Windows VM); Git. Folder layout `companion/` (unedited), `work/chNN/`, `notes/`. Later chapters should assume this setup and add packages with `python -m pip install` |
| — | Role and track names (Chapter 7 §7.2) | Use these ten role names everywhere, including the Part VIII banks: data analyst, business analyst, BI developer, analytics engineer, data scientist, ML engineer, data engineer, AI engineer, automation analyst / RPA developer / integration engineer, data architect. Tracks: *Analytics & BI*; *Data science, ML & AI*; *Engineering & integration* (data engineer, analytics engineer, automation roles); *Architecture*. Tiers 0–6 as in Chapter 8 §8.2 |
| — | Facts that change | Date-stamp survey figures, salaries, versions, prices, and product availability ("retrieved 16 September 2026"), and add each to `planning/pre-publication-refresh.md` in your status report |
| — | Interview Q&A | Part VIII only |
| — | Build order | Blueprint first, then chapters; each chapter approved before the next is considered final |

Items without an explicit choice from the author follow the blueprint's stated default. **Still open** (blueprint section 13): the cloud provider for hands-on engineering examples (default: concepts provider-neutral; hands-on examples on one provider, Azure if targeting Microsoft-heavy employers, AWS otherwise, to be confirmed), and the publishing route. If your chapter depends on an open decision, use the default and flag it (section 13).

---

## 3. Depth classes and length

The author chose **"depth varies"**: full depth for core skills, close to planned length elsewhere. Each chapter's class is listed in `planning/chapter-map.md`.

| Class | Kind of chapter | Model to copy | Typical length | What "full quality" means |
|---|---|---|---|---|
| **A** | Full-depth skill chapter: spreadsheets, SQL, Power BI, Python, automation, dbt | **Ch 12, Ch 13** | As deep as the skill needs; usually 12,000–30,000 words | Taught from zero to working level; many runnable examples with real output; a worked "real work" section; dialect or tool-difference sections; a hands-on lab where the reader builds something; 20–30 exercises with tested answers |
| **B** | Technical teaching chapter: statistics, ML, data engineering, GenAI, advanced topics | **Ch 13** for structure, **Ch 2** for measured demonstrations | About 1.5–2 × the blueprint target (usually 7,000–12,000) | Concept first in plain English, then worked examples with real, run output; a pattern or decision table; 12–18 exercises |
| **C** | Foundation, overview, career, leadership, and architecture chapters | **Ch 1, Ch 2** | About 1.5–2 × the blueprint target (usually 5,000–9,000) | Concrete everyday examples, every number worked and checked, at least one measured or real demonstration where possible, a realistic workplace story; 12–15 exercises |
| **D** | Capstone project chapters (27, 44) | Ch 12's project + Ch 13's review pack | 4,000–7,000 | A complete project brief: milestones, a data spec, rubric, sample deliverables, common failure points |
| **E** | Interview question banks (Part VIII) | Blueprint section 8.4 sample entries | per blueprint | Section 11 of this file |

Length is a result, not a target. Don't pad; don't cut a worked example to hit a number. If a class A or B chapter is heading past **twice** the class's typical range, stop and ask the author whether to split it.

---

## 4. The chapter template (every teaching chapter)

Use these headings, in this order, with this exact Markdown. Look at Chapter 1 (class C) and Chapter 12 (class A) side by side to see the template at both depths.

```
# Chapter N. Title

*Part X — Part Name*

> **Chapter at a glance**
>
> **You will learn to:** skill · skill · skill …   (verbs; separated by " · ")
>
> **Before you start:** Chapter N (what), Chapter M (what). Or: nothing.
>
> **Time needed:** H–H hours of reading and practice[, spread over N weeks].
>
> **Tools:** what to install or open, with section reference for setup.
>
> **Practice data:** which Riverstone dataset or companion files. Every query/output… is real.

---

## Why this matters
## In plain English
## N.1 … ## N.k        (numbered teaching sections, with ### subsections)
## Common mistakes and how to spot them
## In the real world: <short title>
## Tools
## The project: <short title>
## You've got it when…
## Recap
## Practice exercises    (### Warm-up · ### Core · ### Stretch · ### Think about it (no … needed) · optional tool tracks)
## Key terms
## Where this leads
## Answers to practice exercises
```

Separate major blocks with `---` exactly as the reference chapters do.

### What each part must do

| Section | Must do | See |
|---|---|---|
| **Chapter at a glance** | Promise concrete abilities, not topics. Name prerequisite chapters by number. Give honest time. | Ch 12 |
| **Why this matters** | Real-world stakes before any theory: situations the reader will face at work. 2–4 short paragraphs or a short list. No history lessons. | Ch 2 |
| **In plain English** | One everyday analogy that explains the **whole chapter** with zero jargon, then map each part of the analogy to the real term (bold). | Ch 1 (shop notebook), Ch 12 (filing cabinets and clerk), Ch 13 (recipe card, train window) |
| **Numbered sections** | Teach from simple to deep. Every new term is **bold** and defined in plain words on first use. Every concept has a worked example on Riverstone data, with real output. Explain *how it works* line by line after any non-trivial code. End sections with a "reading it" or "what to tell the manager" interpretation where there's a result. | Ch 12 §12.5–12.10 |
| **Callouts** | Used sparingly, in the formats in section 6.4. Traps go in *Watch out*. | all |
| **Common mistakes** | A table: **Mistake · Symptom · Fix**. 8–20 rows, each a mistake real beginners make, with the symptom they'd actually notice. | Ch 12, Ch 2 |
| **In the real world** | A realistic workplace scenario at Riverstone (or a clearly fictional company), solved with the chapter's skills, showing the judgment, not just the syntax. Named characters from section 7. 400–1,500 words. | Ch 1 *Meera's first week*, Ch 2 *The Friday file*, Ch 12 *Monday morning with the sales head* |
| **Tools** | What to install or use, with free alternatives, and companion files by name. | Ch 12 |
| **The project** | Goal; Option A (own work data, with a privacy reminder) and Option B (Riverstone data); numbered steps; stretch goals. Something the reader could put in a portfolio. | Ch 12, Ch 13 |
| **You've got it when…** | 7–12 checkboxes (`- [ ]`) the reader can tick truthfully; abilities and habits, not topics. | Ch 2 |
| **Recap** | The chapter in 8–12 bullets, key terms in bold. | Ch 13 |
| **Practice exercises** | Warm-up (quick checks), Core (the main skills), Stretch (combined, harder), Think about it (judgment, no code). Tool tracks when relevant (for example *MySQL track*). Predict-the-result prompts where useful. | Ch 12 |
| **Key terms** | Every bold new term, separated by " · ", then `*(All terms are defined in the Glossary, Appendix A.)*` | Ch 1 |
| **Where this leads** | 4–7 bullets: the next chapters, related later chapters (by number and title), and the matching **Part VIII bank** (by number). | Ch 12 |
| **Answers** | Starts with `*(In the finished book these move to Appendix G.)*` Every answer worked, with real output for code, and an explanation of *why*, including the common wrong answer where there is one. | Ch 12, Ch 13 |

---

## 5. Voice and style

### 5.1 Voice

- **Warm, direct, second person** ("you"). Write to a smart friend with no technical background.
- **Honest about difficulty**, never hype. No "powerful", "seamless", "game-changing", "unlock your potential", "in today's fast-paced world".
- **Short sentences for new ideas.** Longer ones are fine once the idea has landed.
- **Concrete before abstract.** Show the example, then name the idea.
- **Respect the reader.** Never "simply", "just", "obviously", "easy" about something the reader is learning.
- **Don't use the words** *genuinely*, *honestly*, or *straightforward*.

### 5.2 Mechanics

- **American spelling** (section 2). Before finishing, search your chapter for British spellings (*-ise, -our, -tre, -ll-ed, maths, programme, licence, catalogue, judgement*) and fix them.
- **No em dashes (—) in running prose.** Use a colon, a comma, parentheses, or two sentences. Em dashes are only used in figure captions (`*Figure 2.1 — …*`), the part line under the title, and empty table cells.
- **Numbers:** digits with international grouping: **₹105,885**, not ₹1,05,885. The words *lakh* and *crore* may appear once in a while beside the number for Indian readers ("about ₹43 lakh"), as in Chapter 13. Always state units. Percentages to one decimal unless whole numbers are natural.
- **Dates:** in data and code, **YYYY-MM-DD**. In prose, "31 March 2026".
- **"Today" in examples** is fixed per dataset so outputs never change (section 7.3). Never use `CURRENT_DATE` or `now()` in an example whose output is printed; say what a live report would use instead.
- **Names:** every company and person in examples is **fictional**, with names reflecting India's diversity. No real companies in invented scenarios. Real products and tools (Excel, PostgreSQL, Power BI) are named normally.
- **Headings:** sentence case after the section number (`## 12.10 JOIN: combining tables`). Keep them short.
- **Lists:** a blank line before every list and after every heading.
- **Tables:** GitHub-flavored Markdown. A pipe inside a table cell must be escaped as `\|` (for example `` `a \|\| b` ``), or the table breaks.
- **Bold** for new terms and the one idea in a paragraph that matters most; *italics* for questions people ask and for emphasis. Don't bold whole sentences often.
- **Links to other chapters:** "Chapter 20", "section 12.10", "Figure 13.2". Never "see above/below".

### 5.3 How the reference chapters explain things (copy these moves)

1. **Plain question first.** Every example starts with the business question in quotes: *"Which customers have gone quiet?"*
2. **Then the idea, then the code, then the output, then "How it works"** as bullets that walk through each clause.
3. **Hand-check one number** in prose ("Check order 5001 by hand: 20 × ₹450 … = ₹14,700. ✓").
4. **Reconcile to a known total** whenever a breakdown is shown ("The three reps total ₹300,605 … exactly the total non-cancelled revenue. ✓").
5. **Show the trap by running the wrong version**, with its real, plausible-looking wrong output, then the fix. (Ch 12's AND/OR, fan-out, and LEFT-JOIN-in-WHERE examples.)
6. **Read the result like a manager** ("What to tell Anita", "Reading it", "The story in the numbers").
7. **Connect to the reader's other tools** with *Spreadsheet link* / *SQL link* / *Python link* callouts.
8. **Point forward accurately**: "Chapter 20 automates this" only if Chapter 20's plan covers it (check the blueprint and promises file).

---

## 6. Formatting conventions

### 6.1 Code and output blocks

| Content | Fence | Notes |
|---|---|---|
| PostgreSQL | ` ```sql ` | Primary SQL dialect |
| MySQL | ` ```mysql ` | Rendered with SQL highlighting in the PDF |
| Output of a query or program | ` ``` ` (no language) | Immediately after its code block, separated by one blank line |
| Python | ` ```python ` | Output in the next plain block |
| Excel / Google Sheets formulas | ` ```excel ` or inline `` `=XLOOKUP(…)` `` | State which app when they differ |
| VBA | ` ```vba ` | |
| Google Apps Script | ` ```javascript ` | |
| DAX / Power Query M | ` ```dax ` / ` ```powerquery ` | |
| Shell commands | ` ``` ` with a comment saying where to run them | |
| JSON / XML / YAML | ` ```json ` / ` ```xml ` / ` ```yaml ` | |

- **Output is pasted exactly as the tool prints it.** PostgreSQL output is `psql` format including `(N rows)`. MySQL output is `mysql -t` format (with `+---+` borders). Python output is what `print` shows. Trailing spaces may be trimmed.
- **Errors are shown when they teach something**, pasted exactly (first line and `DETAIL:` line for PostgreSQL; `ERROR nnnn (xxxxx): …` for MySQL, without "at line N").
- **Keywords in capitals, `snake_case` names**, one clause per line in SQL, 4-space indentation, aligned `AS` aliases where it helps reading.
- **Never alias a column with a reserved word** (`rank`, `change`, `order`, `group`, `rows`, `window`): use `rank_no`, `change_amount`.

### 6.2 Verification markers (invisible in the PDF)

These HTML comments let the verification tools (section 9) run every example. Put them on their own line directly before the block they affect.

| Marker | Meaning |
|---|---|
| `<!-- db: riverstone_2025 -->` | Later SQL blocks run in this database (default `riverstone`) |
| `<!-- lab:start -->` … `<!-- lab:end -->` | A stateful region: every statement runs in order in `riverstone_lab`, including `CREATE`, `INSERT`, `ALTER`, `DROP`. Use for build-and-change lessons (Ch 12 §12.13) |
| `<!-- run: pg -->` / `mysql` / `both` / `none` | Which engine runs the next block; `none` skips it (fragments, destructive commands) |
| `<!-- out: mysql -->` / `pg` | The next output block belongs to that engine (used when both outputs are shown) |
| `<!-- py: reset -->` | Start a fresh Python namespace for later blocks |

### 6.3 Figures

- **Every chapter needs 2–6 figures** where a picture explains faster than words: structures, flows, comparisons, before/after, anatomy of a technique.
- **Drawn as SVG by a Python script** `figures/make_figsNN.py`, which imports the shared helpers and palette from `figures/make_figs.py` (see `make_figs01.py` and `make_figs02.py` for simple examples, `make_figs.py` for tables and schemas). Never hand-edit SVG output.
- **File names:** `figures/figN-M-short-slug.svg`, numbered in order of appearance.
- **In the manuscript:** `![Alt text that describes the picture](figures/figN-M-slug.svg)` then a blank line and `*Figure N.M — Caption that says what to notice.*`
- **Palette and type:** use the helper constants (`INK`, `MUTED`, `ACC`, `RULE`, `GREEN #2f7d6d`, `PURPLE #7a4fa0`, `ORANGE #c0662b`, `RED #b23b3b`) and fonts (Poppins for headings, DejaVu Sans for labels, DejaVu Sans Mono for code). Width 900–1,040 px. Text never smaller than 11 px.
- **Check every figure visually** by rendering it to PNG (section 12) before using it: no overlapping labels, no text cut off, arrows pointing at the right things, numbers matching the chapter.
- **Numbers in figures come from the same runs** as the chapter's outputs.

### 6.4 Callouts (blockquotes)

Use these exact openings. Keep each to one idea, 1–5 sentences.

| Callout | Opening | Use for |
|---|---|---|
| Trap | `> **Watch out: short title.** …` | Mistakes that silently give wrong answers (styled in orange in the PDF) |
| Quick exercise | `> **Try it.** …` | A 30-second hands-on check |
| Tool or dialect difference | `> **Dialect note.** …` / `> **Dialect note: topic.** …` / `> **Tool note.** …` | Differences between databases, apps, versions |
| Cross-tool link | `> **Spreadsheet link.** …` / `> **SQL link.** …` / `> **Python link.** …` | The same idea in another tool |
| Real case | `> **Real-life example: short title.** …` | A short real-work illustration |
| Simplification | `> **Simplification note.** …` | Where the example is simpler than real life, and what the real version does |
| Interview tip | `> **Interview extra point.** …` | At most one per teaching chapter; how to use this knowledge in an interview, pointing to Part VIII |

### 6.5 Teaching code and formulas line by line (the beginner rule)

The reader has never seen this code before. A block of code followed by "as you can see" teaches nothing. **Every code block, formula, query, and script in this book is explained at the level of the line and the setting.** This is the book's core promise and the main reason someone would buy it instead of reading documentation.

**The five-part pattern for every first-time example**

1. **The question, in plain words.** *"Which customers are likely to stop ordering?"*
2. **The plan in words before any code.** Two to five sentences, or a numbered list, saying what the code will do, in the order it does it. A reader should be able to follow the plan without knowing the language.
3. **The code**, short enough to read in one screen (12 to 20 lines the first time an idea appears; split longer work into steps that each get their own explanation).
4. **The real output**, exactly as the tool prints it, and a sentence on **how to read it**: what the columns or numbers mean, what "good" looks like.
5. **"How it works": one bullet per line or per clause.** Name the thing, say what it does *here*, and say what it would do differently with other data. Never skip a line because it looks obvious: `import pandas as pd` is new to someone on their first day.

**Settings, arguments, and parameters**

Whenever a function, verb, or model takes settings, add a short table the first time it appears:

| Setting | What it means in plain words | Value used here | What happens if you change it |
|---|---|---|---|
| `test_size=0.2` | share of rows held back to test the model | 0.2 (20%) | smaller: less reliable test; larger: less data to learn from |

Then **run at least one changed version and show the real output**, so the effect is measured, not asserted. One "what if I change this?" demonstration per important setting is the standard; a small results table (setting value → result) is even better.

**Questions a first-time reader asks, which every example must answer**

- What does each line do, and why in this order?
- What are the words I didn't recognize (`fit`, `DataFrame`, `CTE`, `measure`)?
- Where do these numbers come from, and how do I check them?
- What do I change to use my own data?
- What does the output mean, and how do I know it's right?
- What are the common errors here, and what do they look like?

**Other rules**

- **First use is explained use.** Every function, keyword, argument, or file format gets its plain-English meaning the first time it appears in the book, and the chapter's *Key terms* list includes it. Later uses can be brief.
- **No silent magic.** No unexplained imports, no copied helper functions, no "don't worry about this for now" unless the chapter says exactly where it's explained.
- **Show the error.** For each common mistake, run the wrong version, paste the real error or the wrong answer, then fix it.
- **Predict before running.** At least once per teaching section: *"Before you run this, write down what you expect. Then run it."*
- **A changed-line exercise.** Every code-teaching section ends with at least one exercise that asks the reader to change one line or one setting and say what the result will be.
- **Class A and B chapters:** keep a short *"Code words you met in this chapter"* table (term, plain meaning, first section it appeared in).

**For statistics and machine learning chapters**, the same standard applies to the math: every formula gets a plain-English sentence, a worked example with real numbers, and a statement of what happens when its inputs change. A model is explained by what it does to one row of Riverstone data before any library is imported.
---

## 7. The Riverstone bible (shared facts)

These facts are canonical. **Check here before inventing anything about Riverstone.** If your chapter needs a new fact (a plant name, a new system, a new employee), follow section 14.3 to register it.

### 7.1 The company

- **Riverstone Supplies** makes and distributes plastic **storage boxes**, **kitchenware**, **industrial crates**, and a small range of **furniture**, selling to **retailers, hotels and caterers (hospitality), and wholesalers** across India. It runs two manufacturing plants, a sales team, a website, and a customer support desk. It is deliberately like a real mid-sized manufacturer; every name and number is invented.
- **Currency:** ₹. **Tax:** left out of examples unless a chapter teaches it (invoices are "net of discount; tax left out to keep numbers simple").

### 7.2 People (fictional)

| Name | Role | First appears |
|---|---|---|
| Anita Rao | Sales Head (employee 1; top of the sales team, no manager in the data) | Ch 12 |
| Vikram Singh | Sales Manager (employee 2; reports to Anita) | Ch 12 |
| Neha Kulkarni | Sales Executive (employee 3; reports to Vikram) | Ch 12 |
| Rahul Mehta | Sales Executive (employee 4; reports to Vikram) | Ch 12 |
| Farah Khan | Sales Executive (employee 5; reports to Anita) | Ch 12 |
| Meera Iyer | Sales coordinator; joined Riverstone in Chapter 1's story | Ch 1 |
| Imran | Ran sales operations before Meera joined; the "Friday file" | Ch 2 |
| The managing director | Asks for the year-end board review | Ch 13 |
| Rakesh | Buyer at Sharma Hardware (a customer) | Ch 1 |

People outside Riverstone used in examples: **Kavya**, a college student in Mumbai who logs her spending (Ch 1, 2); **Sai Krupa General Store**, Kothrud, Pune (Ch 1 receipt); delivery partners **Swift Movers** and **Rapid Wheels** (Ch 1).

Suppliers (Ch 12 lab): Western Polymers (Vapi), Deccan Cartons (Pune), Kaveri Steel Works (Coimbatore), Sagar Labels (Mumbai), Gujarat Pigments (Ahmedabad), Nilgiri Packaging (Ooty). Warehouses (Ch 12 exercises): Bhiwandi Main (Bhiwandi), Chakan Plant 2 (Pune), Sriperumbudur (Chennai, closed in the exercise).

### 7.3 Datasets that exist (in the project under `companion/`)

| Dataset | Database / files | Period and "today" | Contents | Used in |
|---|---|---|---|---|
| **Mini** | `riverstone` (PostgreSQL: `companion/riverstone_setup_mini.sql`; MySQL: `companion/mysql/riverstone_setup_mysql.sql`) | Q1 2026; **today = 31 March 2026** | 8 customers, 6 products, 5 employees, 12 orders, 19 order lines, 10 invoices, 10 payments | Ch 12, Ch 13 §13.1–13.5 |
| **One-year** | `riverstone_2025` (PostgreSQL: `companion/riverstone_2025_setup.sql`, generated by `companion/generate_riverstone_2025.py`, seed 20251; MySQL: `companion/mysql/riverstone_2025_setup_mysql.sql`) | Calendar 2025; **today = 31 December 2025** | 24 customers, 8 products, 5 employees, 175 orders, monthly `sales_targets`, 43 `leads` (30 unique, with deliberate duplicates), `lead_stage_history` | Ch 13 §13.6 onward |
| **Lab** | `riverstone_lab` (created by the reader) | — | suppliers, purchase orders, warehouses | Ch 12 §12.13 |
| **Formats** | `companion/ch02/` | Feb 2026 | 4 orders as CSV, XLSX, JSON, XML, Parquet; `api_demo.py` | Ch 2 |
| **View** | `sales_lines` in both databases | — | one row per non-cancelled order line with `net_revenue` and `product_cost` | Ch 13 onward |

**Planted facts in the mini database** (other chapters may rely on them): Sunrise Caterers has **no city**; Blue Bay Cafe has **never ordered**; the Garden Chair has **never sold**; order 5008 has **no sales rep**; order 5004 is **Cancelled**; order 5012 is **Pending**; invoices 9002 and 9005 were paid in two instalments, 9003, 9006, 9008 are part-paid, 9007 and 9010 unpaid.

**Key numbers you can quote** (all verified): mini database non-cancelled net revenue **₹323,930**; delivered and shipped revenue by month **Jan ₹104,210 · Feb ₹161,700 · Mar ₹31,800**; outstanding receivables **₹100,460** of ₹297,710 invoiced. One-year database: **173** non-cancelled orders from **23** customers, net revenue **₹4,335,471**, **102.3%** of the annual target; Home Plus signed up but never ordered; top customer Sharma Hardware ₹502,775.

**Products.** Mini (2026 list prices): 101 Storage Box 10L ₹450 · 102 Storage Box 25L ₹780 · 103 Water Bottle 1L ₹120 · 104 Food Container Set ₹650 · 105 Industrial Crate ₹1,450 · 106 Garden Chair ₹1,200. The one-year database uses 2025 list prices (₹430, ₹750, ₹115, ₹620, ₹1,400, ₹1,150) and adds 107 Lunch Box Set (₹380) and 108 Stackable Bin (₹290).

> **Watch out: the mini and one-year databases are separate teaching slices.** Signup dates, prices, and some customer details differ between them (for example, Sharma Hardware signs up in November 2025 in the mini database but orders all through 2025 in the one-year database). Never quote a fact from one as if it were in the other. The planned **full dataset** (blueprint section 6) will be generated to be consistent with both where possible; until then, say which database an example uses.

### 7.4 Datasets still to be built

Blueprint section 6 lists the domains (CRM, finance, operations, IoT sensors, digital events, support tickets, people, documents, automation sandbox) and the chapter that first uses each. **The part that first uses a domain builds it** (section 14.4), as a deterministic, seeded generator in `companion/`, with a short data spec in `planning/data/`, and documented messiness.

---

## 8. Accuracy rules

1. **Every code sample runs, and every output shown is real**, copied from an actual run. No invented output, ever. If something can't be run in your environment (VBA in Excel, Power BI, a paid cloud service, an LLM API), follow section 9.4.
2. **Every number in prose is checked.** Arithmetic in examples, percentages, totals, file sizes, timings: compute them with a script and save the script to the project under `checks/` (for example `checks/ch01_check.py`, `checks/ch02_exp_formats.py`).
3. **Hand-check one row** of any new calculation in the text, and **reconcile** breakdowns to totals.
4. **Fast-changing facts are verified against official sources at the time of writing**: software versions and features, installation steps, product names, prices, limits, laws, salaries, and market statistics. Use web search, prefer official documentation, and record the source links in your chapter report (section 12, step 9). Phrase such facts so they age well ("the current long-term-support release, 9.7 at the time of writing").
5. **No invented statistics** ("80% of data is unstructured") unless a verifiable source is cited in the chapter report. When unsure, describe the pattern without a number.
6. **Honesty about what was tested.** If you tested on one version (for example MySQL 8.0) and recommend another, say so in the companion file header and in your chapter report.
7. **Honor the reference chapters.** Don't contradict an approved chapter. If you find an error in one, report it (section 14.2); don't silently teach something different.
8. **Legal and financial content** (tax, data protection, salaries) is general information, clearly framed, never advice.

---

## 9. Verification tools and methods

The shared tools are in the project under `tools/`. Copy them into your workspace.

### 9.1 SQL (PostgreSQL and MySQL)

1. Install PostgreSQL 16+ and MySQL 8.0+ if they aren't available (`apt-get update && apt-get install -y postgresql mysql-server`, then start both services).
2. Load every practice database: `bash tools/setup_databases.sh <path-to-companion>` (it also creates the `sales_lines` view).
3. Write the chapter with the markers in section 6.2.
4. Run `python3 tools/verify_sql.py manuscript/chNN-….md` and fix every mismatch. It runs each `sql` block in PostgreSQL and each `mysql` block in MySQL, compares with the printed output, runs lab regions statefully, and reports errors raised. **Target: 0 mismatches.** Chapters 12 and 13 pass with 123 and 44 checked outputs.
5. For each SQL chapter, create **`companion/mysql/chNN_queries_mysql.sql`**: every query translated to MySQL, run end to end with no unexpected errors, and results compared with PostgreSQL. Add a **"The same SQL in MySQL"** section when the chapter's SQL uses dialect-specific features (see Ch 12 §12.16, Ch 13 §13.8).

### 9.2 Python

1. Record `python3 --version` and the versions of every library you use in the chapter's *Tools* section.
2. Put data files the code reads in `companion/chNN/`.
3. Run `python3 tools/verify_python.py manuscript/chNN-….md --cwd companion/chNN`. Blocks run in order in one namespace, like a notebook. **Target: 0 mismatches.**
4. Use fixed random seeds for anything random, and fixed dates instead of "today".

### 9.2b Terminal sessions (shell)

1. Write a terminal session as an unlabeled fenced block whose commands start with `$ `, with the real output below each command, exactly as printed.
2. Run `python3 tools/verify_shell.py manuscript/chNN-….md --cwd <a copy of the practice folder> --user <a normal user>`. It has the same contract as the SQL and Python verifiers. **Target: 0 mismatches.**
3. Regenerate the practice folder before each run if the chapter's commands change it, and never verify as root when the chapter shows a normal user's prompt.

### 9.3 Spreadsheets (Excel and Google Sheets)

1. Build every example workbook with a script (`openpyxl`) into `companion/chNN/`, so the data is reproducible.
2. Verify classic formulas by recalculating the workbook headlessly with LibreOffice (`soffice --headless --convert-to xlsx --outdir recalc file.xlsx`) and reading values back with `openpyxl` (`data_only=True`).
3. LibreOffice 24.2 **does not** support some modern Excel functions (for example `XLOOKUP` returns `#NAME?`). For those, and for Google Sheets–only functions (`QUERY`, `ARRAYFORMULA`, `IMPORTRANGE`), compute the expected result independently in Python or SQL and show that result; list those formulas under **"Manual checks needed"** in your chapter report so the author can confirm them in Excel or Sheets.
4. Describe menu paths for both apps (*Excel: Data → From Text/CSV*; *Google Sheets: File → Import*), and verify them against current official help pages.

### 9.4 Things that can't be run in a sandbox

VBA and Office Scripts in Excel, Google Apps Script, Power BI (DAX, Power Query refresh, visuals), Power Automate, paid cloud services, and real LLM or third-party API calls usually can't be executed where you write.

- **Compute the same result another way** (pandas or SQL) so every number in the text is still real.
- **Keep code small, idiomatic, and commented**, following official documentation you have checked.
- **Show outputs only if they're real.** Otherwise show the expected result as a table computed independently, labeled "expected result".
- For APIs, use **local mock servers or recorded responses** (like `companion/ch02/api_demo.py`), clearly labeled.
- **List every unrun item** under "Manual checks needed" in the chapter report, with what to check.

### 9.5 Figures and PDF

- Render figures to PNG and look at them: `tools/` has no figure checker, so use Playwright or `pdftoppm` as in section 12, step 7.
- Build the chapter PDF with `tools/pdf/build_chapter.py` (usage at the top of the file; needs pandoc, Playwright with Chromium, pypdf, and the Poppins and Lora fonts). Render a few pages to PNG and check: tables not broken, code not overflowing, figures sharp, callouts styled.

### 9.6 Cross-references

- Check every "Chapter N" you mention against `planning/chapter-map.md` and the blueprint's plan for that chapter.
- Run `python3 tools/extract_promises.py manuscript/ch*.md` on the written chapters to refresh the promises list, and confirm your chapter delivers every promise addressed to it.

---

## 10. Companion files

- **Folder per chapter:** `companion/chNN/` for data files, scripts, workbooks, and demos. SQL companion files for MySQL go in `companion/mysql/`, PostgreSQL lab scripts in `companion/postgresql/`.
- **Every script and SQL file starts with a header**: book, chapter, what the file is, how to run it, what it was tested on, and "Riverstone Supplies is fictional; every name and number is invented."
- **Deterministic:** generators use a fixed seed and say which.
- **Nothing private:** no real names, emails, keys, or company data. Use `example.com`-style or `.example` domains, and documentation IP ranges (`203.0.113.x`).
- **Runnable end to end:** a companion SQL or Python file must run start to finish without unexpected errors. Statements that fail on purpose are commented out with the error they produce (see `companion/mysql/ch12_lab_mysql.sql`).

---

## 11. Part VIII: question bank format

Question banks follow **blueprint section 8** exactly: the five-dimension rubric (8.1), the twelve extra-point moves (8.2), and the entry format (8.3) as shown in the sample entries (8.4). In short:

- About **a third of questions are core questions** in the full format: `Q[bank]-[number] · Question` · Level · Roles · Round · *What they're really testing* · **Answer that passes** · **Strong answer** · **Extra-points answer** (with moves labeled, for example **[+Clarify]**, **[+Edge cases]**, **[+Validate]**, **[+Business]**) · *Likely follow-ups* · *Red flags* · *Learn it in: Chapter N (sections)*.
- The rest are **rapid-fire questions**: a model answer and one "extra point" line.
- Each bank ends with a **Final-week revision list** of its 20 must-know questions.
- **All code in answers is run and verified** exactly as in teaching chapters, on Riverstone data.
- Every answer points back to the chapter and sections where the topic is taught (**Learn it in**), using `planning/chapter-map.md`.
- Banks are written **after** the chapters they draw on are written, or at the same time from the blueprint plan, and re-checked when those chapters are approved.

---

## 12. Workflow for one chapter

1. **Read** your part brief entry for the chapter, the blueprint entry, the promises addressed to it, and the neighboring chapters' plans. Re-skim the reference chapter of the same class.
2. **Plan** in a short message to the author: depth class, section list with one line each, the Riverstone data and figures you'll use, open decisions (section 13), and the promises you'll deliver. Proceed unless the author changes it.
3. **Research** fast-changing facts with web search and official docs **before** writing the parts that depend on them. Keep the source links.
4. **Build and run the examples first**: data, queries, code, experiments. Save reader-facing scripts and data in `companion/chNN/`, and your own checking scripts in `checks/`. Every printed number comes from these runs.
5. **Draw the figures** with `figures/make_figsNN.py`.
6. **Write the chapter** in the template (section 4), in the voice (section 5), with markers (section 6.2).
7. **Verify:** run the SQL and Python verifiers (0 mismatches); run your number-check script; recalculate spreadsheets; render figures and a sample of PDF pages to PNG and look at them; search for British spellings, em dashes in prose, and the banned words; check every cross-reference.
8. **Build the PDF** with `tools/pdf/build_chapter.py`, named `ChNN-Title-With-Hyphens.pdf`.
9. **Save and report:**
   - `project_write` the manuscript to `manuscript/chNN-slug.md`, the figure script to `figures/`, and companion files to `companion/…`.
   - Write your chapter report to **`planning/parts/<your-part>-status.md`** (section 14.1): status, word count, files, verification results, sources checked, manual checks needed, new Riverstone facts, promises made to other chapters, and issues found in other chapters.
   - Send the PDF (and a companion zip) to the author, with a short summary: what's in it, what was verified, what needs their decision or manual check.
10. **After approval**, mark the chapter approved in your part status file, save an approved copy of the PDF named `ChNN-Title-vX-approved.pdf`, and move to the next chapter.

---

## 13. When to ask the author (and when not to)

**Ask** (one concise question, with a recommended option) when:

- a blueprint decision is still open and changes what you write (cloud provider, a tool choice);
- your chapter would contradict an approved chapter, or needs a change to one;
- a chapter is heading past twice its class's typical length, or should be split, merged, or moved;
- the scope in the blueprint is clearly wrong, missing something important, or duplicates another chapter;
- you need a new Riverstone fact that other parts will depend on (a plant, a system, a key person).

**Don't ask** about things this file already decides (spelling, format, structure, depth class, voice). Make the reasonable choice, say what you chose in the chapter report, and continue.

---

## 14. Working in parallel without collisions

### 14.1 Who writes which files

| File | Written by |
|---|---|
| `manuscript/chNN-….md`, `figures/make_figsNN.py`, `companion/chNN/…` for **your** chapters | Your part chat only |
| `planning/parts/<your-part>-status.md` | Your part chat only (create it with your first chapter) |
| `planning/chapter-writing-instructions.md`, `planning/blueprint.md`, `planning/chapter-map.md`, `planning/progress-tracker.md`, `planning/promises-from-approved-chapters.md`, `planning/riverstone-bible-additions.md`, `tools/…` | **Coordinating chat only** |
| Another part's chapters or companion files | **Nobody but that part's chat.** Report issues instead (14.2) |

Project documents are replaced whole on every save, so two chats saving the same file will overwrite each other. That's why each chat writes only its own files.

### 14.2 Reporting changes other parts need

In your status file, keep a section **"Requests for the coordinator"**: errors found in other chapters, promises you're making to later chapters ("Chapter 47 will turn these checks into automated tests"), promises you can't keep, and proposed structure changes. The coordinator merges them.

### 14.3 New Riverstone facts

Before inventing, check section 7 and `planning/riverstone-bible-additions.md`. If you must add a fact other chapters may reuse (a plant's name and city, a new system, a new recurring person), add it to your status file under **"New Riverstone facts"**, use it, and flag it in your chapter report. The coordinator adds accepted facts to the bible additions file, and they become canonical.

### 14.4 New datasets

If your part is the first to use a domain from blueprint section 6, you build it: a seeded generator in `companion/`, the generated files (SQL, CSV, or Parquet), and a data spec `planning/data/riverstone-<domain>.md` (tables, columns, types, grain, row counts, planted messiness, seed). Keep it consistent with the existing customers, products, and people wherever the domains overlap, and list any unavoidable differences.

### 14.5 Adding, splitting, or moving chapters

The book may grow. **Don't renumber anything yourself.**

- Propose the change to the author (section 13). If approved, give the new chapter a **provisional number with a letter suffix** (for example `19A`, placed after Chapter 19) and a new ID (for example `P2-19A`), and record it in your status file.
- Refer to the new chapter as "Chapter 19A" until the coordinator renumbers. Other chapters keep their numbers.
- At assembly, the coordinator renumbers the whole book in one pass: chapter numbers, section numbers, figure numbers, cross-references, file names, and question-bank references, using `planning/chapter-map.md` as the source of truth.

### 14.6 Project storage limit

The project's knowledge store holds about **2 MB** in total, and was about 0.44 MB on 16 September 2026. A class A chapter's manuscript is 100–220 KB, so the full book will not fit. Until the author sets up larger storage (for example a GitHub repository or Google Drive for desktop), follow these rules:

- **Keep one current copy** of each file; never save versioned copies (`_v2`, `_old`) to the project.
- **Save generators, not generated data.** Put seeded generator scripts in the project; don't save large generated files (SQL dumps, CSVs, Parquet, workbooks over about 50 KB). Say in the data spec how to regenerate them.
- **Don't save PDFs, images, or build outputs** to the project; send PDFs to the author.
- **Check the size first:** before saving a large file, call `project_info` and look at `knowledge_size`. If saving would push it past about 1.8 MB, don't save; tell the author and the coordinator.

---

## 15. Definition of done (every chapter)

- [ ] Follows the template in section 4, with every section present and in order.
- [ ] Depth matches its class (section 3); length reported.
- [ ] Voice and mechanics (section 5): American spelling, no em dashes in prose, no banned words, fictional names, numbers formatted.
- [ ] Every new term bold and defined on first use; listed in Key terms.
- [ ] Every code sample run; every printed output real; verifiers report **0 mismatches**; number-check script passes.
- [ ] **Every code block, formula, and query explained line by line** (section 6.5): plan in words first, real output, "How it works" bullets, a settings table with "what changes if you change it", at least one measured what-if, and a changed-line exercise. `python3 tools/check_code_teaching.py manuscript/chNN-….md` reports no unexplained blocks.
- [ ] SQL chapters: MySQL companion file runs end to end; MySQL differences section where needed.
- [ ] Fast-changing facts verified, with sources recorded in the chapter report.
- [ ] Figures drawn by script, visually checked, captioned.
- [ ] Riverstone facts consistent with section 7; new facts reported.
- [ ] All promises addressed to this chapter delivered; new promises to other chapters reported.
- [ ] Cross-references checked against the chapter map; Part VIII pointer included.
- [ ] Exercises with fully worked answers; code answers verified.
- [ ] PDF built and spot-checked page by page.
- [ ] Manuscript, figures script, and companion files saved to the project; chapter report written; PDF delivered with a short summary and the manual-checks list.

### 15.1 Definition of done (every **part**): the part-completion review pass

A chapter is judged on its own. A part is judged on how it reads end to end. **When the last chapter of your part is approved, do not close the part.** Run one review pass over the whole part, in your own chat, where you still hold the full context of how the chapters connect. Fixes found in this pass are made **in place, inside the part**, so the flow is not disturbed.

Rules for the pass:

1. **Understand before you change.** Read the part straight through as a reader would, in order, without editing. Note problems in a list first. No edit is made from a checker flag alone; a checker flag is a pointer to a place to read.
2. **Diagnose at the level of the part, not the line.** For each problem ask: is this one sentence missing, or is the teaching order wrong, or was something promised in an earlier chapter and never paid off? Write down the cause before the fix. Shallow fixes that paper over a structural problem are worse than leaving it.
3. **Run the whole part through the checkers**, including `tools/check_code_teaching.py` on every chapter, and treat the flags as a reading list.
4. **Check the part's teaching arc:** every term, function, setting, and idea is explained the first time it appears *in the part's reading order*; nothing is used before it is taught; nothing is taught twice at full length; every "we'll come back to this" is paid off, in the chapter named.
5. **Fix in place, then re-verify.** Re-run every check script, verifier, and figure script for every chapter you touched, rebuild those PDFs, and report the before/after counts.
6. **Report to the coordinator**: what you found, the cause of each item, what you changed, what you deliberately left alone and why, and anything that needs a decision outside your part.

Only after this pass is the part complete and its chapters final.

---

## 16. Kickoff prompt for a part chat

Paste this into a new chat attached to the *Data Science* project, replacing the part name:

```
You are writing Part <X> of the book "Analyst to Architect".
1. Read planning/chapter-writing-instructions.md in full, then planning/parts/part-<x>-brief.md,
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) for the depth class of your first chapter
   (manuscript/ch01…, ch02…, ch12…, ch13…).
3. Copy tools/ into your workspace and set up what your part needs (section 9).
4. Start with the first unwritten chapter of Part <X>: send me your plan (section 12, step 2), then
   write, verify, build the PDF, save everything to the project, and report.
5. Continue chapter by chapter, in order. Wait for my approval before treating a chapter as final,
   but you may start planning the next chapter while I review.
Never edit files owned by the coordinator or by other parts; report needed changes in your
status file instead (section 14).
```
