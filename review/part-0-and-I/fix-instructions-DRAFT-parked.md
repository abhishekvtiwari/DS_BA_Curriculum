# Fix Instructions — Part 0 (Ch 1–6) and Part I (Ch 7–9)

Status: v1, 2026-09-25. Written after Abhishek approved (a) Part 0/I findings, (b) just-in-time tool setup, (c) the whole-book sequence map and its three decisions:
- **D1** Power BI (Ch 16) stays before Python (Ch 17–18); no renumbering.
- **D2** Chapter 34 is split: terminal essentials move before Git; Linux and networking stay in Part III.
- **D3** Regression basics become a new section at the end of Ch 22.

Source register: `claude/findings-part-0-and-I.md`. Master order: `claude/sequence-map.md`.
**Updated 28 Sep 2026 for D6** (Abhishek): Chapter 6 is split into an unnumbered front section, "How to Use This Book", placed before Chapter 1, and Chapter 6, "Planning Your Learning". No chapter numbers change. The Chapter 6 section below replaces the earlier "How to Study This Book" plan. These instructions are carried out in the **Part 0 + I build** (CLAUDE.md §5).

Every instruction below names its finding ID, the exact location, the action, and an acceptance check the editor can tick.

**Action verbs:** DELETE (remove text) · REPLACE (swap for given text or spec) · MOVE (cut here, paste at named destination) · ADD (new text) · REWRITE (same purpose, new wording per spec).

---

## 0. Book-wide rules that apply to every chapter in Parts 0 and I

| Rule | What the editor does | Acceptance check |
|---|---|---|
| R1 No code before its chapter (S.1) | In Ch 1–9, no line of SQL, Python, spreadsheet formula, terminal command, DAX or VBA may appear. Data examples (tables, JSON records, an API reply shown as data) are allowed because Ch 1–2 teach them. | Search Ch 1–9 for `SELECT`, `=` followed by a capital function name, `print(`, `import `, `pip`, `python `, `git `: zero hits. |
| R2 No preview boxes (S.4, M.10) | Delete every "Spreadsheet link", "SQL link" and "Dialect note" box in Ch 1–9. Their content moves to the chapter that teaches the tool, rewritten to point **back** ("In Chapter 4 you worked this out by hand; here is the formula"). | Zero boxes with those titles in Ch 1–9. |
| R3 Forward references (0.7) | In the body of Ch 1–9, at most **one** forward reference per section, and only when the reader must know something is deliberately left out. All other pointers go into that chapter's "Where this leads" list. Current counts of references to Ch 10+ in body text: Ch 1: 14 · Ch 2: 15 · Ch 3: 14 · Ch 4: 11 · Ch 5: 10 · Ch 6: 37. | Body references to Ch 10+ ≤ number of sections in the chapter. |
| R4 Production notes (0.15, I.9) | DELETE "(In the finished book these move to Appendix G.)" under every "Answers to practice exercises" heading. The sentence in old Ch 6 §6.9, "The answers are at the end of each chapter in this draft and move to Appendix G in the finished book.", moves to the front section (F.3) and becomes: "Each chapter's answers follow its exercises." (Appendix G is not written, so the book must not send the reader there.) | Zero hits for "finished book" and "this draft". |
| R5 Dataset label (0.8) | Every table or figure with Riverstone numbers carries a one-line source label: "Mini database (Jan–Mar 2026)" or "One-year database (2025)". | Every Riverstone number table has a label. |
| R6 Arithmetic stays checkable | Every number changed by these instructions is recalculated and shown with its working, as the book already does. | Each changed number has a working line or ✓ check. |

---

## Chapter 1 — What Is Data?

| # | ID | Location | Action | Instruction |
|---|---|---|---|---|
| 1.1 | 0.8, 0.9 | End of "In plain English", before §1.1 | ADD | A box titled **"Meet Riverstone"** (about 150 words) with three parts: (1) the company in two sentences (it makes and sells storage boxes, kitchenware, industrial crates and furniture to shops, hotels and wholesalers; two plants, Taloja and Chakan, and one warehouse, Bhiwandi); (2) **the two practice datasets**: the *mini database*, 12 orders from Jan–Mar 2026, used in Chapters 1–5 and 12; and the *one-year database*, 173 orders from 2025, used from Chapter 4 onward; (3) **the people**: a six-line cast table with name, role and the chapter they first appear in (Meera Iyer, sales coordinator; Anita Rao, Sales Head; Vikram Singh, Sales Manager; Neha Kulkarni, Rahul Mehta, Farah Khan, sales executives; Suresh Menon, Finance Manager; Imran, former sales operations). Remove the partial company description from §1.2 so it isn't repeated. |
| 1.2 | 0.11 | §1.6 opening paragraph and Figure 1.3 footer | REPLACE | Paragraph: "Each level can do everything the level **before** it can, plus something new." Figure footer: "Each level keeps every calculation of the level before it and adds one more." |
| 1.3 | 0.12 | §1.6 Worked example 2 | REWRITE | Keep the point and drop the Kelvin arithmetic: "Riverstone's warehouse was 20 °C in the morning and 40 °C in the afternoon. A report says it was 'twice as hot'. It wasn't: 0 °C isn't 'no heat', so Celsius numbers can't be divided like that. The honest sentence is 'the temperature rose by 20 degrees'." |
| 1.4 | R3 | §1.2 Watch out (Ch 24), §1.4 (Ch 10, 12), §1.5 (Ch 15), §1.7 (Ch 18, 41, 55, 58, Part VI), §1.8, §1.9 (Ch 64), §1.10 (Ch 14, 47) | DELETE / MOVE | Keep only: §1.4 "Chapter 12 shows how NULL trips up calculations" (the reader needs to know NULL is deferred) and §1.9 personal data → Ch 64 (a legal-safety pointer). Move the rest to "Where this leads". Delete the "Where you'll work with it" column from the §1.7 table. |
| 1.5 | R4 | Answers heading | DELETE | Per R4. |

**Check:** Ch 1 has no forward references in the body except the two kept; the "Meet Riverstone" box exists; Figure 1.3 wording updated.

---

## Chapter 2 — How Computers Store, Move and Protect Data

Goal: cut the chapter from about 110 key terms to about 65, remove results produced by code the reader can't see, and keep every habit a beginner needs in week one.

| # | ID | Location | Action | Instruction |
|---|---|---|---|---|
| 2.1 | 0.5 | §2.1 "How numbers are stored": "Ask Python to add 0.1 and 0.2: 0.30000000000000004" and "Asked to add the same numbers as exact decimals, Python gives 0.3" | REWRITE | Replace with plain words and no program: "Most software stores decimals approximately. Add 0.1 and 0.2 in many programs and the true stored answer is 0.30000000000000004, a hair more than 0.3. That's why systems that handle money store it in an exact decimal type." Move the runnable Python demonstration to Ch 17 (its section on numbers), with the code shown and explained line by line. |
| 2.2 | 0.6 | §2.1 "How pictures and sound are stored" | DELETE | The 36 MB photo arithmetic isn't needed here. Keep one sentence under Compression in §2.5: "Photos and music are compressed by throwing away detail people won't notice." Exercise 12 is removed with it (see 2.14). |
| 2.3 | 0.6 | §2.2 "Why your 1 TB drive shows 931 GB" (KiB/MiB/GiB) | REWRITE | Shorten to a 3-sentence Watch out box, with no binary unit names: "A drive sold as 1 TB holds a trillion bytes. Windows divides by 1,024 at each step instead of 1,000, so it shows about 931 GB. Nothing is missing." Keep exercise 3. |
| 2.4 | 0.13 | Figure 2.1 footer "(Some software counts in steps of 1,024; see section 2.2.)" | REPLACE | "(Some software counts in steps of 1,024; see the Watch out box below.)" |
| 2.5 | 0.13 | §2.5 title "the same data, packed six ways" vs text "five data formats" | REPLACE | Title: "Data file formats: the same data, packed five ways" and text "…in five formats (and a note on PDF)". |
| 2.6 | 0.5, R1 | §2.5 CSV limits point 3: "Reading it back with Python's pandas library, order_date comes back as text while net_revenue is guessed to be a number." | DELETE | Keep the preceding sentence ("unless the program guesses or you tell it"). |
| 2.7 | 0.6 | §2.5 Parquet: Figure 2.2 plus "The same test at scale" (500,000-row timing table) | MOVE / REWRITE | Keep a 4-sentence Parquet paragraph and Figure 2.2 (row vs column storage). MOVE the timing table and the compression discussion to Ch 49 (Storage, Warehouses & Lakehouses), which teaches columnar storage. Keep the "Choosing a format" table, dropping its "Opens in Excel?" column. |
| 2.8 | R1 | §2.8 "sent with the curl command-line tool" | REWRITE | "Here's the full reply the demonstration API sends back when a program asks for order 5009:" (no tool named). The three responses (200, 404, 401) stay: they are data this chapter teaches. |
| 2.9 | 0.6 | §2.8 status-code table (8 rows) | REWRITE | Keep 5 rows: 200, 401, 404, 429, 500. Keep the "first digit tells you who is responsible" rule. MOVE 201, 400, 403 to Ch 18 §18.14 (Calling an API). |
| 2.10 | 0.6 | §2.7 IaaS / PaaS / SaaS table | REWRITE | Replace the table with 2 sentences: "Companies rent anything from bare computers to finished applications like Gmail or a CRM. The finished-application kind is called SaaS, software as a service, and it's the kind you'll meet first at work." MOVE the full three-level table to Ch 52. |
| 2.11 | 0.6 | §2.9 "Integrity checks: fingerprints for files" (SHA-256 hashes) | REWRITE | Keep the idea in 3 sentences with **one** short example (two payment lines give completely different fingerprints). Show the fingerprints truncated to 12 characters each ("f4251ff3fb71…" and "9d2f842c5011…"). Don't name SHA-256. MOVE the full version to Ch 45 (ingestion, where hashes detect changed files). Exercise 9 stays, reworded without "SHA-256". |
| 2.12 | R3 | Body references to Ch 12, 18, 20, 26, 45, 51, 58, 64, 65 | DELETE / MOVE | Keep in body: §2.5 Watch out on opening CSV in Excel (no pointer needed) and §2.9 personal data → Ch 64. Everything else goes to "Where this leads". |
| 2.13 | S.3 | Tools list: "api_demo.py … which you'll run yourself in Chapter 18" and the companion-file list | REWRITE | "The companion files (Appendix E): orders_feb_2026 in five formats, for the project." Remove api_demo.py from this chapter's tools (it belongs to Ch 18). |
| 2.14 | — | Exercises 12 (photo compression) and project stretch goal "Save the same data as a ZIP" | REWRITE | Exercise 12: "Why must a sales ledger only ever be compressed losslessly? Give one example of what lossy compression would do to it." Answer 12 updated to match. The ZIP stretch goal stays. |
| 2.15 | 0.6 | Key terms list | REWRITE | Remove the terms whose sections were moved or cut: pixel, KiB/MiB/GiB, IaaS, PaaS, packet, SHA-256, 201/400/403 codes, columnar storage (keep Parquet), region. Target: about 65 terms. |

**Check:** no code or tool commands; Ch 2 time estimate re-measured and updated (expected 3–4 hours instead of 4–5); the moved blocks exist in Ch 17, 18, 45, 49 and 52.

---

## Chapter 3 — How a Business Runs on Data

| # | ID | Location | Action | Instruction |
|---|---|---|---|---|
| 3.1 | R2 | §3.3 box titled "Spreadsheet link." | REWRITE | Retitle as "Watch out: a spreadsheet can become the system of record by accident." Same text. It's a business point, not a tool preview. |
| 3.2 | R5 | Order 5001 table, the §3.4 three-sales table, the §3.5 KPI table, the story's order table | ADD | Label "Mini database (Jan–Mar 2026)". |
| 3.3 | R3 | Body references to Ch 12, 15, 19, 25, 45, 49, 58, 75 | DELETE / MOVE | Keep §3.7 "Not every manual step should be automated": one sentence saying the book returns to each manual step later, without chapter numbers. Everything else goes to "Where this leads". |
| 3.4 | R3 | Interview extra point (Ch 75, 76) | KEEP | Interview boxes may name Part VIII chapters, since they point readers to practice, not to prerequisites. |

**Check:** no preview box titles; every Riverstone table labelled.

---

## Chapter 4 — Numbers Without Fear

| # | ID | Location | Action | Instruction |
|---|---|---|---|---|
| 4.1 | S.1, R2 | "Chapter at a glance" Tools line ("the Spreadsheet link notes show each calculation…") and the three "Spreadsheet link" boxes (§4.1, §4.4, §4.5) | DELETE / MOVE | The chapter stays calculator-only. MOVE the three boxes to Ch 10 §10.7 (Essential functions) and Ch 11 §11.3, framed as "Back to Chapter 4: now let the spreadsheet do it" exercises, including `RRI`, `SUMPRODUCT`, `AVERAGE`, `MEDIAN`, `COUNTIF`. The Tools line becomes: "A calculator with a power key (your phone's, turned sideways), a pen and a notebook." |
| 4.2 | S.1 | Companion workbook `numbers_practice.xlsx` in Tools and the chapter intro | MOVE | Keep the workbook, but introduce it in Ch 10 as the first practice file ("Open numbers_practice.xlsx: every number from Chapter 4 is here, now with formulas"). |
| 4.3 | 0.14 | §4.4 "The eleventh root sounds hard…" | ADD | Before the calculator key: "A root undoes a power. 1.073 multiplied by itself 11 times gives 2.17, so 1.073 is the 'eleventh root' of 2.17. You never work it out by hand: type `2.17`, press the power key (xʸ), then `(1 ÷ 11)`." Keep the xʸ key instruction only, no spreadsheet syntax. |
| 4.4 | 0.10 | §4.4 monthly revenue table, "Year ₹4,335,471" | ADD | Footnote under the table: "Monthly figures are rounded to the rupee, so they add to ₹4,335,473; the exact annual total is ₹4,335,471." |
| 4.5 | R5 | Every revenue/order table in Ch 4 | ADD | Label "One-year database (2025)". The §4.3 "Try it" box uses Q1 2026: label it "Mini database". |
| 4.6 | R3 | Body references to Ch 10, 13, 15, 21, 22, 73, 75 | DELETE / MOVE | Keep §4.7 "Chapter 15 covers chart design" and §4.8 "Chapter 22 shows whether a difference is bigger than chance", since the reader should know these are deferred. Move the rest. |

**Check:** no `=` formulas anywhere in Ch 4; the root explanation is present; the total footnote is present.

---

## Chapter 5 — Thinking Like an Analyst

| # | ID | Location | Action | Instruction |
|---|---|---|---|---|
| 5.1 | S.4, R2 | §5.4 "SQL link. Every number in this walk-through is a short query on the mini database (Chapter 12)…" | DELETE | Add to Ch 12's worked examples: "The March issue tree from Chapter 5, now as queries." |
| 5.2 | R5 | §5.4 tables (Feb/Mar invoiced orders, customers owing), §5.5, story tables | ADD | Labels: "Mini database" for §5.4; "One-year database (2025 CRM leads)" for the story. |
| 5.3 | R3 | Body references to Ch 12, 13, 20, 22, 23, 30, 36, 75, 76 | DELETE / MOVE | Keep §5.6 "Chapter 22 shows how to judge chance" (one pointer). Also replace "Chapter 20 does exactly that" at the end of the story with "(you'll build that reminder yourself later in the book)". |

---

## Front section — How to Use This Book (new, D6)

Unnumbered, placed before Chapter 1 (file `manuscript/front-how-to-use-this-book.md`, H1 `# How to Use This Book`, no part line). **Length:** 4–6 printed pages, about 1,500–2,200 words. **No code, no tool commands** (R1 applies: the reader hasn't met any tool yet). Build it with a hand-written job in `tools/pdf/build.py` (`front`), and put it first in the Part 0 collated file.

| # | Section | Content | Source |
|---|---|---|---|
| F.1 | Who this book is for, and how it's built | Two or three paragraphs: from "what is data" to architect; one fictional company, Riverstone Supplies, all the way through; tools are introduced one at a time, in the chapter that first needs them | New |
| F.2 | How each chapter is laid out | The anatomy in order: Chapter at a glance (You will learn to · Before you start · Time needed · Tools · Practice data), Why this matters, In plain English, numbered sections, the boxes (Watch out, Try it, Simplification note, Real-life example, Interview extra point: check each name against the manuscript before listing it), Common mistakes, In the real world, Tools, The project, You've got it when…, Recap, Practice exercises, Key terms, Where this leads, Answers | New paragraph + old §6.9 framing |
| F.3 | The four exercise groups, and the answers | Old §6.9 table (Warm-up, Core, Stretch, Think about it) and its four bullets, unchanged. Answers sentence per R4 | Old §6.9, moved |
| F.4 | How to read code and its output | Part 0 and Part I have no code. From Chapter 10 on, each code block is followed by the output it actually produced when run, then a line-by-line explanation; one new idea per block; PostgreSQL and MySQL shown side by side where they differ; run it yourself and compare. A code block and an output block are shown as they will look, with **no real code** (use a placeholder labelled as such, or describe it in words) | New |
| F.5 | How the parts climb | One line per part, 0 → VIII and Closing, with the part titles exactly as in the chapter files; where job-ready ends (end of Part II); that later parts are optional branches (Chapter 8's career tree) | New |
| F.6 | A rough sense of time | Two sentences: the book's own estimates put the end of Part II at about 320 to 400 hours; Chapter 6 turns that into a plan for your week | New; must match 6.1's table |
| F.7 | The companion files and a tidy folder | What the companion files are and that each chapter's Tools and Practice data lines name the files it uses; the folder layout from old §6.4 **without** `.venv/`; the two rules (never edit the originals; name files as in Chapter 2 §2.4); the "Files" habits from old §6.5 (show extensions, copy a full path, unzip before opening). Pointer to Appendix E for the download address. **Open issue: the address itself doesn't exist yet (RJ-S1-3); do not invent one** | Old §6.4, §6.5 "Files" |

**Check:** 4–6 pages in the built PDF; zero code; every box name listed exists in the manuscript; part titles match the chapter files.

---

## Chapter 6 — Setting Up to Learn → becomes "Planning Your Learning" (D6)

The chapter keeps its number and its study-planning half, and loses every install. It becomes tool-free, so Part 0 needs no software. Chapter anatomy and the exercise guide (old §6.9) move to the front section.

### 6-A. New title, new outline

**H1:** `# Chapter 6. Planning Your Learning`. **Before you start:** Chapters 1–5, and "How to Use This Book". **Time needed:** 2–3 hours, including the exercises and the project (re-measure after writing). **Tools:** a notebook or a notes app, and a calendar. **Practice data:** none; you plan with your own week.

| New § | Content | Source |
|---|---|---|
| Why this matters / In plain English | Keep the author's framing; the kitchen analogy keeps only the meal-plan half (a cook plans the week and gets each utensil when a recipe calls for it) | Old openings, trimmed |
| 6.1 How long it really takes | Honest hours table (6-C), the weekly-hours arithmetic, "chapter hours are not fluency hours" (pointer to Ch 9 §9.1) | New; replaces Figure 6.2 |
| 6.2 A weekly rhythm you can keep | Old Figure 6.3 (becomes Figure 6.1), its three ideas, and "When you fall behind", unchanged | Old §6.8 second half |
| 6.3 What you'll need, and when | Computer requirements from old §6.1 as plain text (8 GB / 16 GB, Mac and Power BI, Chromebook, locked work laptop, the Windows 10 Watch out), the tool timeline table (6-D) and old Figure 6.1 (becomes Figure 6.2). **No install steps, no versions table** | Old §6.1, §6.2, trimmed |
| 6.4 Reading documentation | The five-part method for reading a documentation page, practiced on a **non-code** page the reader already has (a phone-plan or bank fee page: find the exact rule, read every word, find the exception box, check the date or version). One sentence keeps the lesson that tools disagree (for example on rounding a half), with the demonstration deferred to the tool chapters | Old §6.6, rewritten |
| 6.5 Learning with AI assistants | Old §6.7 unchanged, except rule 3's pointer (now to §6.4) | Old §6.7 |

### 6-B. Where each removed piece goes

Removed text is moved verbatim to `manuscript/_parked/ch06-moved-out.md` in the Part 0 + I build, each block labelled with its destination, so nothing is lost before the destination part is built. The destination part's build pulls it from there and deletes it from the parked file.

| Removed from Ch 6 | Goes to | Form there |
|---|---|---|
| §6.3 Step 1 spreadsheet access and `=ROUND(A1,0)` check | Ch 10, new first section "10.0 Getting a spreadsheet and checking it works" | Install or sign in, then a one-line first run |
| §6.3 Step 2 PostgreSQL, MySQL, DBeaver, loading riverstone data, `SELECT COUNT(*)` check | Ch 12 §12.3 (already has full steps) | Remove the "Chapter 6 → come back" loop (0.4) |
| §6.3 Step 3 Python, virtual environment, pip, `check_setup.py` | Ch 17, new first section "17.0 Setting up Python, the terminal and Jupyter" | Every command explained line by line: what `python -m venv .venv` does and what each part means; what "activate" changes; what `pip` is; why `python -m pip`; what the PowerShell policy line does and whether you need it |
| §6.3 Step 4 VS Code and extensions | Ch 17 §17.0 | Same |
| Jupyter (only installed before) | Ch 17 §17.0 | **First notebook**: launch JupyterLab, create a notebook, one cell `print("hello")`, Shift+Enter, read the output, then a markdown cell. This is where the book's line-by-line cell habit starts |
| §6.3 Step 5 Git | Ch 26 §26.2 (Your first repository) | Install plus `git --version` |
| §6.3 Step 6 Power BI | Ch 16, first section | Install from the Microsoft Store; the Mac options |
| §6.5 terminal basics (open, `pwd`, `cd`, run a script) | Ch 17 §17.0 (minimum needed to run Python) **and** Ch 26 new §26.0 "The terminal in 20 minutes" (D2) | Explained command by command |
| §6.5 keyboard shortcuts table | General rows: front section is too short for it, so Ch 10 §10.0 (the first chapter at a keyboard); VS Code row: Ch 17 | Question for Abhishek in the Part 0 + I PR |
| §6.5 "Files" habits | Front section F.7 | — |
| §6.6 rounding comparison (PostgreSQL, MySQL, Python, spreadsheet) and exercises 6, 7, 11 | Ch 17, section on numbers (the Python and spreadsheet parts); Ch 12 (the SQL part, as a documentation Watch out) | Each shown only where the reader knows that tool (S.2) |
| §6.4 companion rows for SQL, Python and Ch 12 labs | Ch 12, Ch 17 | Listed where used |
| §6.9 chapter anatomy, exercise groups, answers | Front section F.2, F.3 | — |
| Exercises 2, 3, 5, 10 and their answers (install checks, terminal, pip, IT request to install) | Ch 12 (2b, 10), Ch 17 (2c, 3, 5), Ch 10 (2d), Ch 26 (2a) | Reworded for the chapter that receives them |
| Meera's `check_setup.py` / "matplotlab" episode | Ch 17 §17.0 as its real-life example | — |

### 6-C. Honest hours (fixes 0.1, I.8)

REPLACE Figure 6.2 ("six months at 8 hours") with a table computed **with code** from every chapter's *Time needed* line, the same way Chapter 83 §83.1 does. It counts Chapter 8's extra 2–3 hours for its project and Chapter 67's "about two hours" as 2–4. Group the rows **by part**, not by topic block, so the table does not depend on the open Part II/III reading-order question.

Numbers as of 28 Sep 2026, with the new Chapter 6 at 2–3 hours:

| | Chapters | Hours | Weeks at 6 h | Weeks at 8 h | Weeks at 10 h |
|---|---|---|---|---|---|
| Parts 0 and I | 1–9 | 28–38 | 5–6 | 4–5 | 3–4 |
| Part II | 10–27 | 290–357 | 48–60 | 36–45 | 29–36 |
| **Job-ready (Parts 0–II)** | **1–27** | **318–395** | **53–66 (12–15 months)** | **40–49** | **32–40** |
| Parts III–VII | 28–67 | 445–584 | — | — | — |
| **All teaching chapters** | **1–67** | **763–979** | **2.4 to 3.1 years** | | |

Recompute these in the build, and again in the final pass (T12), because every chapter's *Time needed* is re-estimated after its fixes. Add the sentence: "These are reading-and-exercise hours. Fluency takes more practice on top (Chapter 9)."

**Knock-on, same build:** Chapter 83 §83.1 uses the old Chapter 6 figure (3–4 h). Update its table, prose and Figure 83.1 (`make_figs83.py`) to the recomputed totals (currently 29–39 → 28–38, 319–396 → 318–395, 764–980 → 763–979). The rounded weeks, months and years there don't change. Note it in `changelog/ch83.md`.

Also REWRITE the Meera story (§"In the real world: Meera sets up" → "Meera makes a plan"). Keep her two-computer decision, framed as *planning* rather than installing: "she decided which tools would live on which computer when she reached them". Replace "At that pace, Figure 6.2 becomes a nine-month plan" with the hours arithmetic from 6.1. Her 90-day chapter targets must follow from 6 hours a week × 13 weeks ≈ 78 hours, counted from Chapter 7 with the *Time needed* lines. Stop at the end of Chapter 11 plus "the next chapter", so the story doesn't depend on the reading-order question. Delete the check_setup/matplotlab episode (parked for Ch 17).

### 6-D. Tool timeline table (new §6.3)

| Tool | You first need it in | Cost | Runs on |
|---|---|---|---|
| Spreadsheet (Excel or Google Sheets) | Ch 10 | Free on the web | Windows, Mac, browser |
| PostgreSQL + DBeaver (MySQL optional) | Ch 12 | Free | Windows, Mac, Linux |
| Power BI Desktop | Ch 16 | Free | Windows only (Mac: see Ch 16) |
| Python, VS Code, Jupyter | Ch 17 | Free | Windows, Mac, Linux |
| Git | Ch 26 | Free | Windows, Mac, Linux |

Add the line: "You'll install each tool at the start of the chapter that first uses it, and check it works with one small first step. Appendix B will gather all the install steps in one place." Keep the versions table in Appendix B only. Until the Part II build moves the installs into Ch 10, 16, 17 and 26, those chapters still say "Chapter 6 set up the tools". List that in the Part 0 + I PR as a known interim gap. Ch 12 §12.3 already has its install steps.

### 6-E. Exercises, project, self-check, recap, key terms

| Item | Action |
|---|---|
| Exercises 1 (which tools a computer can run) and 4 (AI requests) | KEEP; exercise 1 reworded to "which chapters could you do on each computer?" |
| Exercises 2, 3, 5, 6, 7, 10, 11 (install checks, terminal, pip, rounding, IT request, rounding documentation) | MOVE per 6-B. S.2: when exercise 6 lands in Ch 12/17, check part (e) reads `ROUND(45E-1)` (the current text already does) |
| Exercise 8 (5-hour rhythm) | KEEP; its answer uses the new hours table: 318–395 h ÷ 5 = 64–79 weeks |
| Exercises 9 (AI without real data), 12 (90-day plan), 13–15 | KEEP; 14 points to the front section instead of §6.9 |
| New exercises | "Using the table in 6.1 and the hours you really studied last week, write the month you expect to finish Part II. Show your division." And a non-code documentation exercise: "Find the official page for one rule that affects you (your phone plan's data limit, a bank fee) and write down the exact rule, one example, one exception, and the date or version." |
| Project | REWRITE as "Plan your route and your first 90 days": the hours calculation, the weekly rhythm put in a calendar, the folder set up and the companion files downloaded (front section F.7), the AI rule written, one documentation page read (the non-code example), which chapter you'll install each tool in. No install table |
| You've got it when… | Remove the install and check lines; add "I know which chapter I'll install each tool in" and "My finish date comes from arithmetic, not hope" |
| Key terms | Remove operating system, virtual machine, installer, Microsoft Store, admin rights, LTS, PostgreSQL, MySQL, DBeaver, Power BI Desktop, Python install manager, virtual environment, pip, package, VS Code, extension, Jupyter, Git, terminal, command, banker's rounding, round half away from zero, floating-point number, warm-up/core/stretch exercises (now front section). Add study hours, weekly rhythm, tool timeline |
| Where this leads | Ch 7–9; the chapters that install each tool (10, 12, 16, 17, 26); Ch 83 (the long game, the same hours); Appendix B; interview chapters 68 and 81 |

**Check for all of Ch 6:** zero install steps, zero commands, zero code; hours computed by code and equal in Ch 6, Ch 83 and the front section; every removed block is in `_parked/ch06-moved-out.md` with its destination.

### 6-F. References to Chapter 6 elsewhere (D6)

| Where | Now says | Change to |
|---|---|---|
| Part 0 contents (`part0-first-principles.md` intro and table; `planning/chapter-map.md` P0-06) | "you'll have every core tool installed"; row "6. Setting Up to Learn … install and check the book's tools…"; "In total, allow 20–26 hours" | "…and you'll have a plan for how and when you'll learn the rest"; row "6. Planning Your Learning · estimate your hours honestly; set a weekly rhythm; know which chapter brings each tool; read documentation; learn with AI assistants; plan your first 90 days · 2–3 hours"; total recomputed (19–25 hours with Ch 6 at 2–3). Add a line above the table naming "How to Use This Book". Regenerate the collated file from the chapter files |
| Ch 1, line ~382 | "Chapter 6 walks you through installing everything else the book uses." | "Each tool is installed in the chapter that first uses it; Chapter 6 shows when." |
| Ch 3, Tools | "Not needed yet; Chapter 6 installs it and Chapter 12 queries…" | "Not needed yet; Chapter 12 installs it and queries…" |
| Ch 5, "Where this leads" | "Chapter 6, Setting Up to Learn, installs the tools you'll use to test hypotheses, and helps you build a study plan." | "Chapter 6, Planning Your Learning, turns the book's hours into a plan for your week, and shows which chapter brings each tool you'll use to test hypotheses." |
| Ch 7 §7.9, Ch 9 §9.4 Watch out | "Chapter 6 covers learning with AI assistants…" | No change (still true) |
| Ch 9, "Where this leads" | "Chapter 6, Setting Up to Learn, covers your study setup, a sample 6-month analyst plan, and learning with AI…" | "Chapter 6, Planning Your Learning, turns this chapter's timeline into hours and weeks for your own plan, and covers learning with AI assistants without letting them think for you." |
| Ch 9 §9.1 (I.8) | — | ADD one sentence after the table: "Chapter 6's hours table uses the same Time needed lines, so your plan and this chapter agree." (replaces instruction 9.10) |
| Ch 17 (Before you start, §17.1), Ch 26 (intro, Git table), Ch 34 (Before you start, Git Bash row) | "Chapter 6 set up / installed…" | Fixed in the Part II and III builds, when the installs arrive there |

---

## Chapter 7 — The Data Landscape

| # | ID | Location | Action | Instruction |
|---|---|---|---|---|
| 7.1 | I.3, S.1 | §7.6 Step 2 SQL query, "How it works, in plain words", the "SQL link" box, the "Dialect note" and the MySQL query and result | REPLACE | Delete both queries, the SQL link and the dialect note. Replace with: (1) the analyst's method as 4 numbered plain-English steps ("start from every customer, including those who never ordered; for each one, find the latest order that wasn't cancelled; count the days from that date to 31 December; keep those over 60 days, or with no order at all"); (2) **keep the result table** (5 customers, labelled "One-year database (2025)"); (3) keep the hand check for Tasty Tiffins (66 days). Add one sentence: "In Chapter 12 you'll write this yourself." |
| 7.2 | I.4 | §7.6 order of steps 5–7 and Figure 7.5 | REWRITE | New order: 1 business analyst, 2 data analyst, 3 BI developer, 4 analytics engineer, **5 data engineer** (fresh, checked data from payments, support and CRM), **6 data scientist**, **7 ML engineer**, 8 integration engineer, 9 AI engineer, 10 data architect. Edit the data engineer's text so it no longer says "the model needs more than orders"; open instead with "Before anyone can predict, the data has to be complete: …". Figure 7.5 groups become: Clarify and answer (BA, DA) · Share and standardize (BI, AE) · **Supply trusted data (DE)** · Predict (DS, MLE) · Act (integration, AI) · Architect across the top. Caption: "prediction is worth building only after the question is clear, the definition is agreed and the data is trusted." Recap bullet: "clarify, answer, share, standardize, supply trusted data, predict, then act." |
| 7.3 | S.1 | Chapter at a glance "Practice data: one short query… You don't need to run it yet; Chapter 12 teaches every line" | REPLACE | "Practice data: one result from the Riverstone one-year database (2025), so you can see what an analyst's answer looks like." |
| 7.4 | S.1 | Tools: "Companion file (optional): companion/mysql/ch07_queries_mysql.sql…" | MOVE | To Ch 12's companion list. |
| 7.5 | — | Exercises 4, 5, 6, 11, 12 (reference the query result) | KEEP / REWRITE | Keep 4, 5, 6 and 11 (they use the result table). REWRITE 12: "An AI assistant's list shows four quiet customers, not five. Without looking at any code, give three reasons the list could differ (for example, never-ordered customers dropped, cancelled orders counted as activity, a different 'today'), and how you'd check each against the result table." The answer drops the inner-join and `<=` wording in favour of plain descriptions. |
| 7.6 | R3 | Body references (Ch 12, 13, 32, 46–47, 51, 56, 58, 63, 66) | TRIM | Figure 7.1 and the §7.2 "Taught in" column stay: they are the book map and are allowed in Part I. Pointers inside paragraphs move to "Where this leads", except the Daily Sales Flash journey in §7.4 (it's the book's automation thread, so keep it). |

---

## Chapter 8 — The Career Tree

| # | ID | Location | Action | Instruction |
|---|---|---|---|---|
| 8.1 | I.1 | §8.1 first sentence "The draft of this book introduced one idea that stays at the center of this chapter:" | REPLACE | "One idea sits at the center of this chapter:" |
| 8.2 | I.1 | §8.2 "This is the fix for the first edition's tier order, which put engineering before science while the book taught them the other way round. Now tier numbers, part numbers, and the tree agree, and the figure shows the two branches side by side." | REPLACE | "Tier numbers match the book's part numbers, so the figure shows the two branches side by side." |
| 8.3 | I.1 | §8.2 "These rules from the first edition still hold, and the rest of the chapter depends on them." | REPLACE | "Three rules make the tree work, and the rest of the chapter depends on them." |
| 8.4 | I.1 | Answer 1: "The common wrong answer puts data engineering at tier 3, as the first edition did; the tier numbers now follow the book's parts." | REPLACE | "The common wrong answer puts data engineering at tier 3; the tier numbers follow the book's parts, and tiers 3 and 4 are peers." |
| 8.5 | I.2 | Tools: "Companion files: none for this chapter. The skills matrix values are listed in checks/ch08_check.py and in figures/make_figs08.py, if you'd like to rebuild or change it." | REPLACE | "Companion file: skills_matrix.xlsx, the matrix in section 8.3 as a spreadsheet you can filter and extend." Produce that file from the matrix; if it won't be produced, write "Companion files: none for this chapter." |
| 8.6 | I.5 | §8.6 salary table header "Median base salary" vs text "PayScale's average base salary … ₹577,472" | REPLACE (verify first) | Recheck the PayScale Data Analyst India page. If the ₹577k figure is the **average**, rename the column "Average base salary" and fix the three rows. If it is the **median**, change the text and answer 7 to "median". Either way the table and text must use the same word. Also check that the "1.73 times" comparison uses like with like. |
| 8.7 | I.6 | §8.6 length and staleness | REWRITE | Keep: the two kinds of source, how to read a percentile and a median, CTC vs in-hand, and the 5-step "check salaries yourself". Reduce the three-role table to **one** row (data analyst) as a worked reading example, with a dated "As retrieved September 2026" label. MOVE the other two rows and the growth-percentage discussion to Ch 68 (How Data Hiring Works), where pay is discussed for the job search. Exercises 6 and 7 keep working from the kept row and Ch 68's table. |
| 8.8 | I.10 | Figure 8.1 | ADD caption line | "Names in the tiers that aren't among Chapter 7's ten roles (reporting/MIS assistant, BI analyst, senior analyst) are common entry titles for those roles." |
| 8.9 | R3 | JD decoding §8.5: "At-risk list: Ch 13 · dashboard: Ch 16 · automation: Ch 20" | KEEP | Mapping duties to chapters is the purpose of this section (a reader planning a route), so it is allowed. Tool names inside the job posting (SQL, window functions, pandas) stay: a JD is shown as a document to decode, not as code to run. |

---

## Chapter 9 — How Expertise Actually Forms

| # | ID | Location | Action | Instruction |
|---|---|---|---|---|
| 9.1 | I.1 | §9.2 "It's kept from the first edition of this book, because it's still true." | DELETE | The paragraph opens with "Here's the reframe that makes the long timeline an advantage instead of a punishment." |
| 9.2 | I.1 | §9.7 "The first edition of this book saved this topic for its closing chapter. It's here now, because you'll meet your first plateau long before the end of the book." | REPLACE | "This section comes early on purpose: you'll meet your first plateau long before the end of the book." |
| 9.3 | I.2 | Tools: "Farah's log is listed in checks/ch09_check.py and figures/make_figs09.py if you'd like to chart your own the same way." | REPLACE | "Companion file: practice_log_template.xlsx, with Farah's 12 weeks already filled in and a chart that updates as you add your own weeks." Produce the file; otherwise "Companion files: none." |
| 9.4 | I.7 | §9.7 "Reading it" bullets | REPLACE | "In weeks 1–4, Farah practiced 810 minutes and her score rose from 3 to 6. In weeks 5–8, she practiced 1,010 minutes and her score didn't move. She responded the way most people do: she practiced more, from 220 minutes in week 4 to 270 in week 7, an increase of 22.7%, with no gain. In weeks 9–12 she practiced 980 minutes, slightly less than in the plateau, and her score rose from 6 to 9." Working: 240 + 260 + 270 + 240 = 1,010; 240 + 250 + 240 + 250 = 980 ✓. The 2,800-minute total is unchanged. |
| 9.5 | I.7 | Story: "She also cut her minutes back. The late nights stopped." | REPLACE | "She kept her minutes about the same, but the late nights stopped." |
| 9.6 | S.1 | §9.4 Figure 9.2 row: "Write a LEFT JOIN that keeps never-ordered customers" | REPLACE | "Build a monthly total of your spending log and check it against the sum of every row". Also in the five features: "write a query that keeps customers who have never ordered" → "work out, by hand, which customers in a list of 20 have never ordered". |
| 9.7 | S.1 | §9.6 asking-for-help example with `LEFT JOIN` / `WHERE o.status <> 'Cancelled'` | REPLACE | A spreadsheet-free, code-free example: "I'm totalling my spending log by category. My Food total is ₹1,230, but when I add the Food receipts by hand I get ₹1,380. I expected them to match. Here are the eight Food rows." Remove the pointer to Ch 12 §12.10. |
| 9.8 | S.1 | "In the real world: Farah's week seven": "her join kept dropping them", "the difference between an inner and a left join and where the filter goes", "rebuilt its LEFT JOIN examples" | REWRITE | Keep the story's logic in plain words: "her answers kept leaving out customers who had never ordered", "one idea: how to keep the rows that have no match in the other table", "rebuilt that section's examples without looking". Keep one pointer: "(Chapter 12, section 12.10, teaches this exact idea.)" |
| 9.9 | S.1 | Answer 2(b) "Write three queries that keep customers with no orders" and answer 10 (window functions week) | REWRITE | 2(b): "Answer three questions about customers with no orders on the practice data, predicting each result first." Exercise 10 becomes: "Design one week of deliberate practice for someone who has finished Chapter 4 and struggles with percentage points versus percent change." Answer rewritten to match. |
| 9.10 | I.8 | §9.1 | ADD one sentence | See 6-F (D6): "Chapter 6's hours table uses the same Time needed lines, so your plan and this chapter agree." |
| 9.11 | D6 | "Where this leads", Chapter 6 bullet | REPLACE | See 6-F. |

---

## Moves that land outside Parts 0 and I (tracked so nothing is lost)

| Destination | What arrives | From |
|---|---|---|
| Ch 10 new §10.0 | Spreadsheet access and the `=ROUND` first-run check; numbers_practice.xlsx; the "Back to Chapter 4" formula exercises (RRI, SUMPRODUCT, AVERAGE/MEDIAN/COUNTIF) | Ch 6 §6.3; Ch 4 |
| Ch 11 §11.3 | Remaining Ch 4 spreadsheet exercises | Ch 4 |
| Ch 12 §12.3 and examples | DB install (no Ch 6 loop); March issue-tree queries; ch07 MySQL file; ROUND documentation Watch out (SQL part) | Ch 6, 5, 7 |
| Ch 16 first section | Power BI install and Mac options | Ch 6 |
| Ch 17 new §17.0 | Python, venv, pip, VS Code, Jupyter first notebook, terminal minimum, `check_setup.py` (with the matplotlab typo story), `0.1 + 0.2` demo, Python/spreadsheet rounding comparison, moved exercises | Ch 6, 2 |
| Ch 18 §18.14 | Status codes 201, 400, 403 | Ch 2 |
| Ch 22 new final section | Regression basics (D3; specified separately in the Part II instructions) | — |
| Ch 26 new §26.0 | "The terminal in 20 minutes" (D2) plus Git install | Ch 6; Ch 34 essentials |
| Ch 45 | Full hashing section | Ch 2 |
| Ch 49 | Format timing table, compression detail | Ch 2 |
| Ch 52 | IaaS / PaaS / SaaS table | Ch 2 |
| Ch 68 | Two salary rows and the growth discussion | Ch 8 |
| Appendix B | All-in-one install guide and versions table | Ch 6 |
| Front section "How to Use This Book" (D6) | Chapter anatomy, exercise groups, companion folder, "Files" habits | Ch 6 §6.9, §6.4, §6.5 |
| Ch 83 §83.1 | Recomputed hours totals (new Ch 6 at 2–3 h) | Ch 6 (D6) |
| `manuscript/_parked/ch06-moved-out.md` | Every block removed from Ch 6, labelled with its destination, until that part is built | Ch 6 |

## Order of work for the editor

1. R4 and the Ch 8 and Ch 9 first-edition and build-script lines. These don't depend on anything else.
2. Ch 7 §7.6 rewrite, Ch 9 plain-word rewrites, Ch 1 "Meet Riverstone".
3. Ch 2 cuts and moves.
4. Ch 4 and Ch 5 box removals (their destinations in Ch 10–12 are written when Part II is fixed).
5. Ch 6 rebuild and the front section (D6). The removed install material goes to `_parked/` because its destinations (Ch 10, 16, 17, 26) are built in the Part II build; Ch 12 §12.3 already has its steps. Then the D6 reference updates (6-F), Ch 83's hours, and the regenerated Part 0 and Part I collated files.
6. Re-measure every Part 0 and I "Time needed" line, then update the Ch 6 table and the Closing's hours table if totals change.
