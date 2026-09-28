# Parked: blocks removed from Chapter 6 (D6)

Not a reader-facing file and not built. Chapter 6 became "Planning Your Learning" in the Part 0 + I build (decision D6, CLAUDE.md §3; spec: `review/part-0-and-I/fix-instructions-DRAFT-parked.md`, Chapter 6, table 6-B). Every block removed from the old chapter ("Setting Up to Learn", Time needed 3–4 hours) is kept here **verbatim**, labelled with its destination. When the destination part is built, that build moves the block into its chapter (rewritten for that chapter, per 6-B) and deletes it from this file.

Labels: **→ Destination** (still to be placed) · **Landed** (already placed in this build; kept here for the record) · **Retired** (replaced, no destination; kept for reference).

---

## 1. Old Chapter at a glance: Practice data line

**→ Ch 12 (`riverstone_setup.sql`, at its §12.3) and Ch 17 §17.0 (`check_setup.py`).**

> **Practice data:** the Riverstone mini database (`riverstone_setup.sql`) and a small script, `check_setup.py`, both in the companion files (Appendix E). Every version, install method, and output in this chapter was checked against official sources or run, in September 2026.

---

## 2. Old §6.1 computer table

**→ Appendix B (as a table). Landed in Ch 6 §6.3 as plain text (this build).**

| | Enough to start | Comfortable |
|---|---|---|
| **Operating system** | Windows 10 or 11, or a recent macOS | Windows 11 or the latest macOS your Mac supports |
| **Memory (RAM)** | 8 GB | 16 GB |
| **Free disk space** | 20 GB | 50 GB or more |
| **Screen** | a laptop screen | a second monitor, so the book or documentation sits next to your work |
| **Internet** | enough to download installers | enough for video calls and cloud tools later |

Old locked-laptop bullet, before trimming (the Python install manager clause → Ch 17 §17.0):

- **A work laptop you can't install software on.** Many companies lock their laptops, for good security reasons. Ask your IT team; learning tools like PostgreSQL, Python, and DBeaver are commonly approved. Some tools install without administrator rights: Microsoft's documentation notes that Power BI Desktop from the Microsoft Store doesn't need admin rights, and Python's install manager installs for your own user. The story later in this chapter shows one way through.

---

## 3. Old §6.2 versions table and versions note

**→ Appendix B (the versions table lives only there, per 6-D).** Figure 6.1 and "A few words on these choices" stayed in Ch 6 (§6.3, now Figure 6.2).

| Tool | What it's for | First used | Cost | Runs on | Version at the time of writing |
|---|---|---|---|---|---|
| **Excel** or **Google Sheets** | spreadsheets | Chapter 10 | Excel for the web and Google Sheets are free with a Microsoft or Google account; desktop Excel needs a Microsoft 365 subscription | Windows, Mac, browser | always updated |
| **PostgreSQL** | the book's main database | Chapter 12 | free | Windows, Mac, Linux | 18 (the current major version, supported until November 2030) |
| **MySQL** Community Server | the second database | Chapter 12 | free | Windows, Mac, Linux | 9.7 LTS (8.4 LTS is also fine) |
| **DBeaver** Community | the app you type SQL into | Chapter 12 | free | Windows, Mac, Linux | 26.2 |
| **Power BI Desktop** | dashboards and data models | Chapter 16 | free (Microsoft describes the desktop app as free) | Windows only | updated monthly |
| **Python** | programming for data | Chapter 17 | free | Windows, Mac, Linux | 3.13 or 3.14 |
| **VS Code** | the editor for Python, SQL files, and notes | Chapter 17 | free | Windows, Mac, Linux | updated monthly |
| **Git** | saving versions of your work | Chapter 26 | free | Windows, Mac, Linux | 2.55 |

> **Simplification note: versions move.** Tools release new versions every few months. The book's examples were tested on PostgreSQL 16, MySQL 8.0, and Python 3.11 and 3.13, and use features that work the same way in the newer versions listed above. If a newer version than the table shows is available when you read this, install it. Appendix B keeps current instructions.

(RJ-S3-18, the one-sentence Python version rule, belongs with Ch 17 §17.0 when this lands.)

---

## 4. Old §6.3 Installing, in order

### 4.0 Section intro

**→ Appendix B (all-in-one install guide).**

## 6.3 Installing, in order

Install in this order. Each step ends with a check, so a problem shows up immediately, not three chapters later. Use the official website for every tool; download sites that repackage installers sometimes bundle unwanted software.

### 4.1 Step 1. A spreadsheet

**→ Ch 10, new first section "10.0 Getting a spreadsheet and checking it works"** (install or sign in, then a one-line first run). The "(Section 6.6 explains why…)" pointer must become a pointer inside Ch 10/17, where the rounding comparison lands.

### Step 1. A spreadsheet

If you already have Excel through work or a Microsoft 365 subscription, you're done. If not, either works:

- **Google Sheets**: sign in to a Google account and open Google Sheets in your browser.
- **Excel for the web**: sign in with a free Microsoft account at Microsoft 365 on the web. Files are saved in OneDrive, which comes with 5 GB of free storage.

**Check:** create a sheet, type `2.5` in A1 and `=ROUND(A1,0)` in B1. You should see `3`. (Section 6.6 explains why that's worth checking.)

> **Tool note.** Microsoft ran a free *desktop* Excel editing preview in some markets until July 2026. It has ended: the free desktop apps now open and view files, and editing is free only in the web versions. Chapters 10 and 11 point out the few features that need desktop Excel.

### 4.2 Step 2. The databases and DBeaver

**→ Ch 12 §12.3 (already has full, tested steps).** Nothing here needs to be added there except, if wanted, the order_items check. Finding 0.4: the "do them now, and come back" loop is gone from Ch 6. Visual V6.8: if the two `SELECT COUNT(*)` blocks are reused, label them "PostgreSQL:" and "MySQL:".

### Step 2. The databases and DBeaver

Chapter 12, section 12.3, has full, tested steps for both databases and DBeaver on Windows, macOS, and Linux. You don't need to repeat them here; do them now, and come back. A summary:

1. **Install PostgreSQL** from the official PostgreSQL website. On Windows, the page recommends the interactive installer by EDB, which also includes pgAdmin and StackBuilder (you won't need either). On a Mac, the same installer works, or Postgres.app, a small app that runs PostgreSQL from the menu bar. Choose the current version, and **write down the password** you set for the `postgres` user.
2. **Install DBeaver Community.** It includes its own Java, so there's nothing else to install.
3. **Install MySQL** (optional until Chapter 12's MySQL sections). Choose the current LTS release, and write down the `root` password.
4. **Create the database and load the data**, as in section 12.3: `CREATE DATABASE riverstone;` in PostgreSQL, then run `riverstone_setup.sql`; in MySQL, run `riverstone_setup_mysql.sql`, which creates the database for you.

**Check:** in DBeaver, connected to `riverstone`, run the same query in each database.

```sql
SELECT COUNT(*) FROM order_items;
```

```
 count
-------
    19
(1 row)
```

```mysql
SELECT COUNT(*) FROM order_items;
```

```
+----------+
| COUNT(*) |
+----------+
|       19 |
+----------+
```

Nineteen order lines: the same twelve orders you followed through Chapters 1 to 5. If you see an error instead, the troubleshooting notes in section 12.3 cover the common ones, including MySQL's "Public Key Retrieval is not allowed".

### 4.3 Step 3. Python and the analyst's packages

**→ Ch 17, new first section "17.0 Setting up Python, the terminal and Jupyter".** Every command explained line by line (what `python -m venv .venv` does and each part; what "activate" changes; what `pip` is; why `python -m pip`; what the PowerShell policy line does and whether you need it). Outputs must be re-run, not copied.

### Step 3. Python and the analyst's packages

**Install Python** from python.org:

- **Windows:** python.org now recommends the **Python install manager**, available from the python.org downloads page or the Microsoft Store (they're the same tool). The older full installer is being retired. After installing, open a terminal (section 6.5) and run `py install 3.14` if it didn't install a version for you. The commands `python` and `py` then start Python.
- **Mac:** download the macOS installer package from python.org and run it. When it finishes, open the new *Python 3.14* folder in *Applications* and double-click **Install Certificates.command**, which lets Python download packages securely. On a Mac, the command is `python3`.
- **Linux:** use your distribution's packages or python.org's source; most distributions already include a recent Python 3.

**Create a folder and a virtual environment for the book.** A **virtual environment** is a private copy of Python's package list for one project, so installing something for this book can't break anything else on your computer. Chapter 17 explains it properly; for now, follow the steps. In a terminal, go to your book folder (section 6.4) and run:

```
# Windows (PowerShell or Command Prompt)
python -m venv .venv
.venv\Scripts\activate
python -m pip install pandas openpyxl matplotlib jupyterlab

# macOS or Linux (Terminal)
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pandas openpyxl matplotlib jupyterlab
```

When the environment is active, your terminal prompt starts with `(.venv)`. Each time you open a new terminal to work on the book, run the `activate` line again. If PowerShell refuses to run the activation script, the Python documentation's fix is to run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once, or to use Command Prompt instead.

**Check:** run the companion script `check_setup.py` from the `ch06` folder:

```
python check_setup.py
```

On a correctly set-up computer, it prints:

```
python       3.13.13  OK
pandas       3.0.5    OK
openpyxl     3.1.5    OK
matplotlib   3.11.2   OK
jupyterlab   4.6.3    OK
All set.
```

Your version numbers may be newer; that's fine. If something is missing, the script says exactly what to run. Here's a real run on a computer where only one package had been installed:

```
python       3.11.15  OK
pandas       -        MISSING: run  python -m pip install pandas
openpyxl     3.1.5    OK
matplotlib   -        MISSING: run  python -m pip install matplotlib
jupyterlab   -        MISSING: run  python -m pip install jupyterlab
Fix the lines above, then run this script again.
```

> **Watch out: "pip installed it, but Python can't find it."** This almost always means the package went into a different Python from the one running your script, often because the virtual environment wasn't active. Activate `.venv`, then install with `python -m pip install …` rather than plain `pip install …`, so the package goes into the Python you're actually using.

**Also → Ch 17 §17.0:** the folder line `.venv/  the Python environment from section 6.3` from the old §6.4 folder tree (the front section's tree has no `.venv/`), and the first notebook (JupyterLab, one cell, Shift+Enter, a markdown cell), which is new writing there.

### 4.4 Step 4. VS Code

**→ Ch 17 §17.0.**

### Step 4. VS Code

**Install VS Code** from its official website. Open it, go to the *Extensions* view, and install two extensions published by Microsoft: **Python** and **Jupyter**. Then use *File → Open Folder* to open your book folder.

**Check:** press `Ctrl+Shift+P` (`Cmd+Shift+P` on a Mac), type *Python: Select Interpreter*, and choose the one inside `.venv`. Create a file called `hello.py` containing `print("ready")`, and run it with the play button. The terminal at the bottom should print `ready`.

### 4.5 Step 5. Git

**→ Ch 26 (install plus `git --version`), with the new §26.0 "The terminal in 20 minutes" (D2) or §26.2 "Your first repository".**

### Step 5. Git

- **Windows:** install **Git for Windows** from the official Git website, accepting the default options.
- **Mac:** the Git website lists three ways; the simplest is to run `xcode-select --install` in Terminal, which installs Apple's command line tools, including Git. (Homebrew users can run `brew install git`.)
- **Linux:** install the `git` package from your distribution.

**Check:** in a terminal, run `git --version`. You'll see a version number such as `git version 2.55.0`. Chapter 26 teaches how to use it.

### 4.6 Step 6. Power BI Desktop

**→ Ch 16, first section (install from the Microsoft Store; the Mac options).**

### Step 6. Power BI Desktop (Windows)

On Windows, install **Power BI Desktop** from the **Microsoft Store**. Microsoft recommends the Store version because it updates itself and doesn't need administrator rights. Microsoft lists at least 2 GB of free memory (4 GB or more recommended) and a screen of at least 1440×900. Signing in matters later, when you publish and share reports through the Power BI service (Chapter 16).

On a Mac, skip this step for now, and decide before Chapter 16 whether to use a Windows virtual machine, a Windows computer at work or college, or to follow Chapter 16 by reading and doing its exercises on a borrowed machine.

**Check:** open Power BI Desktop, close the welcome screen, and you should see an empty report canvas.

---

## 5. Old §6.4 The companion files and a folder that stays tidy

**Landed: front section "How to Use This Book", "The companion files and a tidy folder" (this build)** for the idea of the companion files, the folder tree (without `.venv/`) and the two rules. **The table rows → the chapters that use them:** `ch02/` row → Ch 2's own Tools line (already there); SQL rows and the Ch 12 lab rows → Ch 12; the Ch 13 rows → Ch 13; `ch04/numbers_practice.xlsx` → Ch 10 §10.0 (with Ch 4's moved formula exercises); `ch06/check_setup.py` → Ch 17 §17.0. The complete list → Appendix E. RJ-S3-34 (one table of every Riverstone dataset) → Appendix E or B.

## 6.4 The companion files and a folder that stays tidy

The **companion files** (Appendix E) hold every dataset, script, and workbook the book uses. So far that includes:

| Folder or file | What it is | Used in |
|---|---|---|
| `ch02/` | four orders as CSV, Excel, JSON, XML, and Parquet; `api_demo.py` | Chapter 2 |
| `riverstone_setup.sql` and `mysql/riverstone_setup_mysql.sql` | the mini database (first quarter of 2026) | Chapters 12, 13, and many examples |
| `riverstone_2025_setup.sql` and its MySQL twin | the one-year database (2025) | Chapter 13 onward |
| `postgresql/ch12_lab_postgresql.sql`, `mysql/ch12_lab_mysql.sql`, `new_suppliers.csv` | the build-a-database lab | Chapter 12 |
| `mysql/ch12_queries_mysql.sql`, `mysql/ch13_queries_mysql.sql` | every query in Chapters 12 and 13, tested in MySQL | Chapters 12, 13 |
| `ch04/numbers_practice.xlsx` | the numbers workbook | Chapter 4 |
| `ch06/check_setup.py` | the setup checker | this chapter |

Later chapters add their own folders. Appendix E gives the address to download them from and lists every file.

Set up one home for everything, and keep it that way:

```
analyst-to-architect/
    companion/            the downloaded companion files, unchanged
    work/
        ch10/             your own files for each chapter
        ch12/
        ...
    notes/                your study log, plans, and questions
    .venv/                the Python environment from section 6.3
```

Two rules keep it useful. **Never edit the companion files themselves**: copy what you need into `work/` first, so you can always start again from a clean copy. And **name your files the way Chapter 2 (section 2.4) taught**: dates as year-month-day, lower-case words joined with hyphens or underscores, and no "final".

---

## 6. Old §6.5 Keyboard, files, and the terminal

### 6.1 Keyboard shortcuts

**→ Ch 10 §10.0 (the general rows; the first chapter at a keyboard) and Ch 17 §17.0 (the VS Code row).** Question for Abhishek in the Part 0 + I PR (6-B): confirm Ch 10 as the home for the general rows.

## 6.5 Keyboard, files, and the terminal: the basics that save hours

### Keyboard shortcuts worth learning this week

| Action | Windows | Mac |
|---|---|---|
| Copy, cut, paste | `Ctrl+C`, `Ctrl+X`, `Ctrl+V` | `Cmd+C`, `Cmd+X`, `Cmd+V` |
| Undo, redo | `Ctrl+Z`, `Ctrl+Y` | `Cmd+Z`, `Cmd+Shift+Z` |
| Find in a page or file | `Ctrl+F` | `Cmd+F` |
| Save | `Ctrl+S` | `Cmd+S` |
| Switch between apps | `Alt+Tab` | `Cmd+Tab` |
| Open the search for apps and files | `Windows` key, then type | `Cmd+Space`, then type |
| Take a screenshot of part of the screen | `Windows+Shift+S` | `Cmd+Shift+4` |
| Command palette in VS Code | `Ctrl+Shift+P` | `Cmd+Shift+P` |

Chapters 10, 12, and 17 add the shortcuts for spreadsheets, DBeaver, and VS Code. Learn a few at a time: use one new shortcut deliberately for a week, until your hands do it on their own.

### 6.2 Files

**Landed: front section, "The companion files and a tidy folder", the three file habits (this build).**

### Files

From Chapter 2, make sure you can: **show file extensions** (so `orders.csv` doesn't appear as plain `orders`); **find a file's full path** (Windows: hold `Shift`, right-click the file, *Copy as path*; Mac: select the file, then `Option+Cmd+C`); and **unzip** a download before opening what's inside it, because opening files directly from inside a zip is a common cause of "my changes disappeared".

### 6.3 The terminal

**→ Ch 17 §17.0 (the minimum needed to run Python) and Ch 26 new §26.0 "The terminal in 20 minutes" (D2).** Explained command by command there.

### The terminal

A **terminal** is a window where you type commands instead of clicking. You'll use it for Python, Git, and later for much more (Chapter 34 teaches it properly). For now, four things are enough:

| To do this | Type | Example |
|---|---|---|
| Open a terminal | Windows: search for *Terminal* or *PowerShell*. Mac: search for *Terminal*. In VS Code: *Terminal → New Terminal* (opens in your current folder). | |
| See where you are | `pwd` (PowerShell, Mac, Linux); `cd` on its own in Command Prompt | |
| Move into a folder | `cd` followed by the folder name | `cd analyst-to-architect` |
| Run a Python script | `python` (Mac: `python3`) followed by the file name | `python check_setup.py` |

The most common beginner error is running a command in the wrong folder, which gives *"No such file or directory"* or *"can't open file"*. When you see that, check where you are first.

---

## 7. Old §6.6 Reading documentation: the rounding comparison

**→ Ch 17, section on numbers (the Python and spreadsheet parts: `round(2.5)`, `round(2.675, 2)`, `=ROUND(2.5,0)`, `=ROUND(2.675,2)`, the Python documentation quote, banker's rounding) and → Ch 12 (the SQL part, as a documentation Watch out: the PostgreSQL and MySQL queries, outputs and manual quotes).** Finding S.2: each part only where the reader knows that tool. Re-run every block there; don't copy these outputs. The method ("How to read a documentation page") stayed in Ch 6 §6.4, rewritten for a non-code page; its original, code-flavoured wording is kept at the end of this block for the tool chapters.

## 6.6 Reading documentation

Every tool in this book has **official documentation**: the manual written by the people who make it. When a tutorial, a colleague, and an AI assistant disagree, the documentation settles it.

### A real question: how does 2.5 round?

Chapter 4 said to round at the end, not in the middle. Here's a follow-up question that sounds trivial: *what does rounding 2.5 to a whole number give?* The same question, in three of the book's tools.

In PostgreSQL:

```sql
SELECT ROUND(2.5)                    AS exact_half,
       ROUND(3.5)                    AS exact_three_half,
       ROUND(2.5::double precision)  AS float_half,
       ROUND(3.5::double precision)  AS float_three_half;
```

```
 exact_half | exact_three_half | float_half | float_three_half
------------+------------------+------------+------------------
          3 |                4 |          2 |                4
(1 row)
```

In MySQL:

```mysql
SELECT ROUND(2.5)   AS exact_half,
       ROUND(3.5)   AS exact_three_half,
       ROUND(2.5E0) AS float_half,
       ROUND(3.5E0) AS float_three_half;
```

```
+------------+------------------+------------+------------------+
| exact_half | exact_three_half | float_half | float_three_half |
+------------+------------------+------------+------------------+
|          3 |                4 |          2 |                4 |
+------------+------------------+------------+------------------+
```

In Python:

<!-- py: reset -->
```python
print(round(2.5), round(3.5), round(2.675, 2))
```

```
2 4 2.67
```

And in a spreadsheet, `=ROUND(2.5,0)` gives `3` and `=ROUND(2.675,2)` gives `2.68`.

So 2.5 rounds to 3 in some places and to 2 in others, and 2.675 rounds to 2.68 in a spreadsheet but 2.67 in Python. Who's right? This is exactly the kind of question to settle in the documentation, not by guessing:

- **The PostgreSQL manual** (*Mathematical Functions and Operators*, `round`): *"For `numeric`, ties are broken by rounding away from zero. For `double precision`, the tie-breaking behavior is platform dependent, but 'round to nearest even' is the most common rule."* `2.5` typed on its own is `numeric`, so it goes to 3; converted to `double precision`, it goes to the even number, 2.
- **The MySQL manual** (`ROUND()`): exact-value numbers round *"away from zero"*; for approximate-value numbers, *"the result depends on the C library"*, and on many systems that means *"round to nearest even"*. `2.5E0` is written in scientific notation, which makes it an approximate value.
- **The Python documentation** (built-in `round`): *"if two multiples are equally close, rounding is done toward the even choice"*. And a note: *"`round(2.675, 2)` gives `2.67` instead of the expected `2.68`. This is not a bug"*: 2.675 can't be stored exactly as a floating-point number (Chapter 2, section 2.1), and the stored value is a hair below 2.675.

Rounding halves to the nearest even number is called **banker's rounding**, or round-half-to-even. It's used because, over many values, rounding every half up nudges totals upward, while rounding to even balances out. Neither rule is wrong. What's wrong is not knowing which one your tool uses, and then wondering why a Python report and an Excel report differ by a rupee.

### How to read a documentation page

You don't read documentation front to back. You go in with a question and look for five things:

1. **The signature**: the name and what goes in, such as `ROUND(number, num_digits)`.
2. **The description**: what it returns, in one or two sentences. Read every word; the details (like "for `numeric`") are usually the point.
3. **Examples**: run one yourself, exactly as written, before changing it.
4. **Notes and warnings**: often in a box. This is where `round(2.675, 2)` was explained.
5. **The version**: documentation sites usually cover several versions. Make sure you're reading the one you installed (for example, PostgreSQL's pages have a version switcher at the top).

If the documentation doesn't answer it, try the tool's official forums, then a well-asked search.

---

## 8. Old §6.8 sample six-month plan (Figure 6.2)

**Retired: replaced by Ch 6 §6.1's hours table (findings 0.1, I.8).** Figure file `figures/fig6-2-six-month-plan.svg` is no longer used by Ch 6 (delete it once the Part 0 collated file is regenerated). RJ-S1-1 and RJ-S3-9 (redraw this plan to another reading order) are moot: the plan is gone.

### A sample six-month plan

![A six-month plan: month 1, Chapters 1–9; month 2, spreadsheets (Chapters 10–11); month 3, SQL (Chapters 12–13); month 4, cleaning, charts, and Power BI (Chapters 14–16); month 5, Python and statistics (Chapters 17–18, 21–22); month 6, automation, business skills, and the portfolio (Chapters 19–20, 23–27), with interview practice starting](figures/fig6-2-six-month-plan.svg)

*Figure 6.2 — One way through the analyst path (Parts 0 to II) in six months, at about 8 hours a week.*

Figure 6.2 is a sample, not a rule. It's ambitious: about 8 hours a week for 26 weeks. At 5 hours a week, stretch it to nine or ten months, and nothing is lost. A few choices behind it:

- **Spreadsheets before SQL, SQL before Python.** Each builds on the last, and together they cover most day-to-day analyst work.
- **Power BI in month 4**, once you can shape data, so the dashboards have something good to show.
- **Automation (Chapters 19–20) after Python**, because Chapter 20 uses it.
- **Interview practice in month 6, not at the end.** Answering questions from Part VIII (Chapters 68–71) while you build your portfolio shows you what to revise.
- **Business analysts** can swap some Python time for Chapters 24 and 25, which cover requirements, stakeholders, and process mapping.

---

## 9. Old §6.9 How to use the exercises and answers

**Landed: front section, "How each chapter is laid out" and "The four exercise groups, and the answers" (this build).** The answers sentence became "Each chapter's answers follow its exercises." (R4).

## 6.9 How to use the exercises and answers

Every teaching chapter ends with practice exercises in four groups:

| Group | What it's for | How to use it |
|---|---|---|
| **Warm-up** | checks you understood the basics | do them right after reading; they should take a few minutes each |
| **Core** | the skills the chapter exists to teach | do all of them; this is where most of the learning happens |
| **Stretch** | harder, closer to real work | do at least one; come back to the rest on a second pass |
| **Think about it** | judgment, with no single right answer | write a short answer, then compare it with the model answer |

The answers are at the end of each chapter in this draft and move to **Appendix G** in the finished book. To get the most from them:

- **Write your answer before you look.** Even a partial answer. Reading an answer you haven't attempted feels like learning and isn't.
- **Compare the reasoning, not only the number.** Many answers show a method or a check (like "✓ reconciles to the total"); copy the method.
- **Mark the ones you got wrong or guessed**, and redo them on Sunday from a blank page.
- **For code exercises, run your version.** If it gives the same result by a different route, that's often fine; if it gives a different result, find out why before moving on.

---

## 10. Old common-mistakes rows (installing)

**→ Ch 10 §10.0 and Ch 16 (installer row), Ch 12 §12.3 (password row), Ch 17 §17.0 (virtual environment row, wrong-folder row), Ch 26 §26.0 (wrong-folder row).**

| Mistake | Symptom | Fix |
|---|---|---|
| Downloading installers from third-party sites | unwanted extra software; outdated versions | Use each tool's official website or the Microsoft Store |
| Forgetting the database password | can't connect to PostgreSQL or MySQL | Write it down during installation, somewhere safe |
| Installing packages without the virtual environment active | "pip installed it, but Python can't find it" | Activate `.venv`; use `python -m pip install …` |
| Running commands in the wrong folder | "No such file or directory" | Check where you are (`pwd`) before running |

---

## 11. Old story "Meera sets up": the install episode

**→ Ch 17 §17.0 as its real-life example (the `check_setup.py` / "matplotlab" episode).** Items 2 and 4 were rewritten as planning in Ch 6's "Meera makes a plan"; item 3 is parked whole. RJ-S1-4: when this lands in Ch 17, Meera is setting up her home computer to go further, not starting SQL from scratch.

**3. The Mac.** She installs Postgres.app, DBeaver, MySQL, Python from python.org (remembering *Install Certificates.command*), VS Code with its Python and Jupyter extensions, and Git with `xcode-select --install`. She creates the `analyst-to-architect` folder, the `.venv`, and runs `check_setup.py`. It reports matplotlib missing: she had typed `matplotlab`. One command later: *All set.* In DBeaver, `SELECT COUNT(*) FROM order_items;` returns 19 in both databases.

Old items 2 and 4 and the old item 5 sentence, for the record:

**2. The work laptop.** She emails IT with a short, specific request: *"I'd like to install Power BI Desktop from the Microsoft Store for learning and for building sales reports. It doesn't need admin rights. I won't connect it to any company data without approval."* IT approves the same week, and adds that she should use the company's Microsoft 365 account for sign-in when she's ready to share reports.

**4. The 8 GB question.** Her Mac slows down with DBeaver, VS Code, twenty browser tabs, and a video call all open. The fix costs nothing: close what she isn't using while studying.

At that pace, Figure 6.2 becomes a nine-month plan. She writes her first 90 days in `notes/plan.md`: Chapters 7 to 11 by the end of month 2, Chapters 12 and 13 in month 3.

She matched tools to computers, asked IT the right way, fixed the one problem the checker found, and wrote a plan for her real week, not an ideal one.

---

## 12. Old Tools section

**→ Appendix B (the official websites line) and Ch 17 §17.0 (`check_setup.py`).**

- **The official websites** for each tool: PostgreSQL, MySQL, DBeaver, python.org, VS Code, Git, and Microsoft for Excel and Power BI. Appendix B lists the current download pages and install steps.
- **`check_setup.py`** (companion files, `ch06/`): checks your Python version and the four packages. Tested on Python 3.11.15 and 3.13.13, with pandas 3.0.5, openpyxl 3.1.5, matplotlib 3.11.2, and JupyterLab 4.6.3.

---

## 13. Old project Step 1 (install and check), Step 3 and the deliverable

**→ Each tool's first-run check in Ch 10, 12, 16, 17, 26; the whole table → Appendix B.** Step 3 (documentation of a spreadsheet function such as `MEDIAN` or `RRI`) → Ch 10 or 11.

**Goal:** a working toolkit, verified, and a study plan you can keep.

**Step 1. Install and check.** Work through section 6.3. For each tool, record the version and the result of its check:

| Tool | Version installed | Check | Result |
|---|---|---|---|
| Spreadsheet | | `=ROUND(2.5,0)` gives 3 | |
| PostgreSQL + DBeaver | | `SELECT COUNT(*) FROM order_items;` gives 19 | |
| MySQL (optional for now) | | the same query gives 19 | |
| Python + packages | | `check_setup.py` prints *All set.* | |
| VS Code | | `hello.py` prints `ready` | |
| Git | | `git --version` prints a version | |
| Power BI Desktop (Windows) | | opens to an empty report | |

**Step 3. Test the documentation habit.** Pick one function you used in Chapter 4 (for example, `MEDIAN` or `RRI`) and find its official documentation page for your spreadsheet. Write down its signature, one example, and one note or warning.

**Deliverable:** the completed check table, a screenshot of `check_setup.py` printing *All set.*, and your 90-day plan.

---

## 14. Old "You've got it when…" lines (installing)

**→ The chapter that installs each tool (Ch 10, 12, 17, 26).**

- [ ] Every core tool is installed from its official source, and each check passed.
- [ ] `SELECT COUNT(*) FROM order_items;` returns 19 in the Riverstone database.
- [ ] `check_setup.py` prints *All set.*
- [ ] My companion files are in one place, unedited, with my own work in a separate folder.
- [ ] I can open a terminal, see where I am, move into a folder, and run a script.
- [ ] I can find and read the official documentation for a function in each tool.

---

## 15. Old recap bullets (installing)

**→ Ch 12, 17, 26 recaps as they apply.**

- **The core toolkit is free:** a spreadsheet, PostgreSQL and MySQL with DBeaver, Power BI Desktop, Python with VS Code and Jupyter, and Git. Later parts add their own tools.
- **Install in order, from official sources, and check each tool** before moving on. Chapter 12, section 12.3, has the full database steps.
- **Use a virtual environment** for the book's Python packages, and install with `python -m pip install`. `check_setup.py` confirms your setup.
- **Keep the companion files unedited** and your own work in a separate folder, with file names that sort and search well.
- **A few shortcuts and four terminal commands** save hours over the course of the book.
- **Documentation settles disagreements.** Rounding 2.5 gives 3 or 2 depending on the tool and the number type, and each tool's manual says exactly why.
- **A plan and a rhythm finish books.** About 8 hours a week covers the analyst path in six months; fewer hours stretch it, and a missed week moves the plan instead of doubling the load.

---

## 16. Old exercises 2, 3, 5, 6, 7, 10, 11 and their answers

**Destinations (6-B), each reworded for the chapter that receives it:** 2(a) → Ch 26; 2(b) → Ch 12; 2(c) → Ch 17; 2(d) → Ch 10; 3 → Ch 17; 5 → Ch 17; 6 → Ch 17 (parts c, d) and Ch 12 (parts a, b, e); 7 → Ch 17; 10 → Ch 12; 11 → Ch 17 (Python) or Ch 12 (PostgreSQL). **S.2:** when exercise 6 lands, check part (e) still reads `ROUND(45E-1)` (it does here) and that the double-precision/approximate-value rule has been taught before it.

2. Match each check to the tool it confirms: (a) `git --version`; (b) `SELECT COUNT(*) FROM order_items;` returning 19; (c) `check_setup.py` printing *All set.*; (d) `=ROUND(2.5,0)` returning 3.
3. A friend's terminal shows `python: can't open file 'check_setup.py': No such file or directory`. List two likely causes and how to check each.
5. After installing pandas, a script fails with `ModuleNotFoundError: No module named 'pandas'`. Explain the most likely reason, and write the two commands (for your operating system) that would fix it.
6. Using the documentation quotes in section 6.6, predict the result of each, and explain your reasoning: (a) PostgreSQL `SELECT ROUND(4.5);` (b) PostgreSQL `SELECT ROUND(4.5::double precision);` (c) Python `round(4.5)` (d) a spreadsheet `=ROUND(4.5,0)` (e) MySQL `SELECT ROUND(45E-1);`
7. A Python report and an Excel report of the same invoices show totals that differ by ₹1. Using section 6.6, give one possible explanation, and describe how you'd confirm it.
10. Write a short, specific request to your IT team asking permission to install PostgreSQL, DBeaver, and Python on a work laptop for learning. Include what each tool is for, what data you will and won't connect to, and one question for them.
11. Find the official documentation page for Python's `round()` or PostgreSQL's `ROUND` for the version you installed. Write down its signature, one example you ran yourself, and one note or warning. Then find one tutorial or video that explains rounding, and say whether it matches the documentation.

**2.** (a) Git. (b) The database and DBeaver (with the Riverstone data loaded). (c) Python and the four packages. (d) The spreadsheet.

**3.** (1) The terminal is in a different folder from the script: check with `pwd`, then `cd` into the `ch06` folder. (2) The file name is different, such as `check_setup.py.txt` because extensions are hidden, or the file is still inside a zip: show file extensions (Chapter 2) and unzip the download.

**5.** pandas was installed into a different Python from the one running the script, usually because the virtual environment wasn't active. On Windows: `.venv\Scripts\activate`, then `python -m pip install pandas`. On macOS or Linux: `source .venv/bin/activate`, then `python -m pip install pandas`. (Also make sure VS Code's selected interpreter is the one in `.venv`.)

**6.** (a) `5`: `4.5` is `numeric`, and PostgreSQL breaks ties away from zero. (b) `4`: as `double precision`, the common rule is round half to even, and 4 is even. (c) `4`: Python rounds halves to the even choice. (d) `5`: spreadsheets round halves away from zero. (e) `4`: `45E-1` is an approximate value, so on most systems MySQL rounds to the nearest even number. (All five were run for this chapter, with exactly these results.)

**7.** The two tools may round halves differently: Python's `round()` rounds halves to even (and floating-point values like 2.675 are stored slightly below the half), while Excel's `ROUND` rounds halves away from zero. If each invoice is rounded before the totals are added, small differences can add up to a rupee. To confirm: find invoices whose unrounded values end in exactly .5 of the rounding unit, compare each line's rounded value in both reports, and check whether the differences add up to ₹1. The lasting fix is to agree on one rule and round at the end (Chapter 4).

**10.** One good version: *"Hello, I'd like permission to install three free tools on my work laptop for learning data analysis: PostgreSQL (a database, used to practice SQL on sample data), DBeaver Community (an app for writing SQL), and Python from python.org (for data analysis scripts). I'll only use practice datasets from a textbook, and I won't connect them to any company system or customer data without your approval. Could you tell me whether there's an approved way to connect to company data later, if my manager asks for reports?"*

**11.** Answers vary. A complete answer includes the signature (for example, `round(number, ndigits=None)` in Python), an example the reader ran themselves, and the note about `round(2.675, 2)` or PostgreSQL's tie-breaking rule. Many tutorials say "Python rounds .5 up", which doesn't match the documentation; noticing that is the point of the exercise.

---

## 17. Old key terms removed from Ch 6

**→ The chapter that teaches each (6-E):** operating system, RAM stays in Ch 6; virtual machine, Microsoft Store, admin rights → Ch 16; installer, LTS, PostgreSQL, MySQL, DBeaver → Ch 12; Python install manager, virtual environment, pip, package, VS Code, extension, Jupyter, terminal, command, banker's rounding, round half away from zero, floating-point number → Ch 17 (banker's rounding also Ch 12's Watch out); Git, terminal, command → Ch 26; path, keyboard shortcut, companion files → front section (described there, not as key terms); signature → Ch 17; warm-up, core, stretch exercises → front section.

operating system · virtual machine · installer · Microsoft Store · administrator (admin) rights · LTS (long-term support) · PostgreSQL · MySQL · DBeaver · Power BI Desktop · Python install manager · virtual environment · pip · package · VS Code · extension · Jupyter · Git · companion files · terminal · command · path · keyboard shortcut · signature · banker's rounding (round half to even) · round half away from zero · floating-point number · warm-up, core, stretch exercises

---

## 18. Old "Where this leads" bullets replaced

**Retired (rewritten per 6-E).** Kept for the record.

- **Chapters 10 and 11** use your spreadsheet; **Chapters 12 and 13** use the databases and DBeaver you installed, starting with the Riverstone data you loaded.
- **Chapter 16** uses Power BI Desktop; **Chapters 17 and 18** use Python, VS Code, and Jupyter, and explain virtual environments properly.
- **Chapter 26** puts Git to work and covers AI assistants in a professional setting; **Chapter 34** teaches the command line in depth.
- **Appendix B** keeps current install steps for every tool; **Appendix E** lists all companion files; **Appendix G** holds the answers.
