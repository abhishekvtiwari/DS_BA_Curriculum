# Chapter 69A. Why This, Not That: Tool Choice & Judgement

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will practise:** answering the questions that open almost every data interview and that no syllabus covers — why Python and not Excel, why PostgreSQL and not MySQL, what the difference between SQL and Postgres even is · giving the honest trade-off instead of the fashionable answer, including the cases where the simple tool is the right one · recognising when a question is really asking "do you have judgement, or did you learn a list?" · defending a choice you did not make, which is most of the choices you will be asked about.
>
> **Before you start:** nothing technical. This chapter is about *choosing*, not using, so it can be read before the tool chapters rather than after. Where a question names a technique, it says where the book teaches it. Chapter 69 (the three answer tiers and the twelve extra-point tags) is the method every answer here is written against.
>
> **Time needed:** 3–4 hours to read and answer each question aloud; 1 hour for a revision pass. Shorter than the tool banks, and the questions in it are asked more often than any of them.
>
> **Who this is for:** every role in this book. The first ten minutes of a screening call for a fresher and the first ten minutes of an architect's panel are the same conversation at different scales.
>
> **How this chapter is built.** The format of every question bank in Part 8: a **"Remember it as…"** hook, a one-line answer, a tier table of what **passes**, what is **strong** and the **extra points** (Chapter 69's twelve tags), then the likely follow-ups, the red flag, and where to learn it. Levels are **Fresher**, **Mid** and **Senior**; roles are **DA** data analyst · **DS** data scientist · **DE** data engineer · **BA** business analyst · **MLE** ML engineer.
>
> **Where a claim can be measured, it is.** Most books answer "why not Excel?" with an opinion. The numbers in this chapter — Excel's real row limit against this book's real data, how long each format takes to write, what a join actually costs — were produced by running the code on Riverstone's full dataset, and several of them contradict the usual answer.

---

## 69A.1 Why these questions decide the first ten minutes

Almost every interview opens here, and almost nobody prepares for it.

The technical banks in this part test whether you can *do* the thing. This chapter tests whether you know *why you would*, and the two are not the same skill. A candidate who can write a window function but cannot say why the problem belongs in SQL rather than in a spreadsheet has learned a syllabus. A candidate who can say "this is three hundred rows that changes once a month, I would leave it in Excel" has judgement, and judgement is what is actually being hired.

Three things make these questions harder than they look.

**There is usually no right answer, and saying so is part of the answer.** "Postgres or MySQL" has no winner. What the interviewer wants is the shape of your reasoning and the conditions under which you would switch.

**The fashionable answer is often wrong.** "Excel does not scale" is the standard reply and it is false at the size most analysts work. Section 69A.3 has the measurement.

**You will be asked to defend choices you did not make.** "Why does your team use Airflow?" is a fair question even if it was chosen before you joined, and "I do not know, it was already there" is a worse answer than an honest reconstruction of the trade-off.

The move that works throughout this chapter is Chapter 69's **[+Clarify]**: name the conditions under which the answer changes, before you give the answer.

---

## 69A.2 The vocabulary that trips people up

These sound like trivia. They are not — they are how an interviewer checks in thirty seconds whether you understand the stack or have been copying commands.

### Q69A-001 · What is the difference between SQL and PostgreSQL?

**Level:** Fresher · **Roles:** DA, DS, DE, BA

**Remember it as:** *SQL is the language. PostgreSQL is a program that speaks it. Asking "SQL or Postgres" is like asking "English or a telephone".*

**Answer in one line:** SQL is a **query language**, a standard for describing what data you want; PostgreSQL is a **database management system** — an actual program that stores your data and answers SQL queries about it. MySQL, SQL Server, Oracle, SQLite, Snowflake and BigQuery are other such programs, and all of them speak SQL with their own accent.

Laid out plainly, because this is the mental model the rest of the stack hangs on:

| Layer | What it is | Examples |
|---|---|---|
| **The language** | A standard way to ask for data | SQL |
| **The dialect** | One system's variation on that standard | PostgreSQL's `\|\|`, MySQL's `CONCAT` |
| **The engine** | The program that stores data and runs queries | PostgreSQL, MySQL, SQLite |
| **The server** | That program running on a machine, reachable over a network | `db.riverstone.internal:5432` |
| **The database** | One named collection of tables inside it | `riverstone_2025` |

So the sentence "I know SQL" means you can write the language. It does not tell anyone which engines you have used, and the follow-up is always which.

The reason an interviewer asks is cheap and effective: someone who has only followed tutorials often thinks "SQL" is a product you install. It takes one question to find out, and it tells them how to pitch the next forty minutes.

Where it genuinely matters is portability. The language is standard enough that `SELECT`, `JOIN` and `GROUP BY` move between engines untouched. The accents are different enough that date functions, string concatenation, `LIMIT` against `TOP`, and the behaviour of `NULL` in sorting all vary — which is why this book shows every query in PostgreSQL and gives a MySQL version where it differs, and why Chapter 71's section 71.8 exists at all.

| Tier | What to say |
|---|---|
| Passes | "SQL is the language, Postgres is the database" |
| Strong | + the layers above: language, dialect, engine, server, database, with an example of where the dialects actually differ |
| Extra points | **[+Edge cases]** the standard is real but no engine implements all of it, and every engine adds to it · **[+Business]** this is why "we will just move to another database later" is more expensive than it sounds — the queries move, the dialect-specific parts do not · **[+Clarify]** when a job ad says "SQL", ask which engine, because that is what the team's habits are built on |

**Likely follow-ups:** Which engines have you used? Is NoSQL a kind of SQL? *(No — the name means "not only SQL"; the data model is different, not just the syntax.)* What does ANSI SQL mean?
**Red flag:** treating "SQL" and "MySQL" as the same word. It is the single fastest way to signal that your experience is shallower than your résumé says.
**Learn it in:** Chapter 12, section 12.1 (what a database actually is); Chapter 71, section 71.8 (where the dialects differ).

### Q69A-002 · Is pandas a different language from Python?

**Level:** Fresher · **Roles:** DA, DS, MLE

**Remember it as:** *pandas is a library you import. It is Python all the way down — but it is Python with a dialect of its own, and that dialect is the thing you are actually being hired for.*

**Answer in one line:** pandas is a **library**, written in Python and installed with `pip`; everything you write with it is still Python, and the confusion is understandable because pandas code looks almost nothing like the Python you learned first.

The honest version of this answer admits the confusion is reasonable:

```python
total = 0
for row in rows:
    if row['status'] == 'Delivered':
        total += row['amount']
```

```python
total = df.loc[df.status == 'Delivered', 'amount'].sum()
```

Same language, same result, and the second does not look like the first. That is because pandas works on **whole columns at once** rather than one row at a time, which is where its speed comes from and why a loop over a dataframe is nearly always the wrong instinct (Chapter 72, Q72-047).

Say the stack out loud and you cover the whole family:

- **Python** — the language.
- **NumPy** — arrays and fast numeric operations. pandas is built on it.
- **pandas** — tables with named columns. Built on NumPy.
- **scikit-learn, matplotlib, statsmodels** — modelling, charts, statistics. Built on both.

Which is why "do you know Python or pandas?" is a slightly confused question, and the gracious answer is to describe the stack rather than correct the asker.

| Tier | What to say |
|---|---|
| Passes | "pandas is a Python library" |
| Strong | + why it looks like a different language: column-at-a-time instead of row-at-a-time, with an example of each |
| Extra points | **[+Scale]** the vectorised form is not just tidier, it is one to two orders of magnitude faster, because the loop runs in C rather than in Python · **[+Edge cases]** which is why `.apply(axis=1)` is usually a disguised loop and not an improvement · **[+Business]** a team that says "we use Python" usually means pandas, notebooks and a handful of libraries, not the language in the abstract |

**Likely follow-ups:** What is NumPy for? Why is a loop over a dataframe slow? What is Polars, and why do people mention it? *(A newer dataframe library, faster on large data; the concepts transfer.)*
**Learn it in:** Chapter 17 (Python from zero); Chapter 18, section 18.1 (NumPy and pandas).

### Q69A-003 · What actually is a "notebook", and why does anyone object to them?

**Level:** Mid · **Roles:** DA, DS, DE, MLE

**Remember it as:** *A notebook is code, output and prose in one scrollable document, where the cells can be run in any order. The first half is why people love it. The second half is why people distrust it.*

**Answer in one line:** A Jupyter notebook interleaves code, its output and written explanation in one file, and runs cell by cell in whatever order you click — which makes it excellent for exploring and genuinely dangerous as a place to keep anything that matters.

The objection is specific and worth being able to state precisely, because "notebooks are bad" without it sounds like fashion:

**Hidden state.** The cells can be run out of order, so the notebook on your screen may depend on a variable created by a cell you have since edited or deleted. The document shows one thing and the kernel holds another. A notebook that works for you can fail for everyone else, including you tomorrow.

**It does not diff.** The file is JSON with outputs embedded, so a code review in Git shows a wall of noise. Two people editing one notebook is a merge conflict almost every time.

**It resists testing.** There is no obvious place to put a test, so there usually is not one.

None of which makes notebooks wrong. It makes them the wrong *final* home. The answer that lands is the progression:

| Stage | Where the code should live |
|---|---|
| Exploring, one-off analysis, teaching | **A notebook.** Nothing else is as good |
| It worked and someone wants it monthly | **A script**, with the logic in functions |
| Other people depend on it | **A package**, with tests and a command-line entry point |

That is the arc of Chapter 18 into Chapter 29, and describing it is a stronger answer than picking a side.

| Tier | What to say |
|---|---|
| Passes | "Notebooks are good for exploring, not for production" |
| Strong | + names hidden state, the diff problem and the testing gap as the three specific objections, and gives the notebook → script → package progression |
| Extra points | **[+Validate]** "Restart kernel and run all" before sharing is the one habit that catches hidden state · **[+Trade-offs]** tools like `jupytext`, `nbconvert` and papermill let a notebook be versioned or scheduled, which narrows the objection without removing it · **[+Business]** a monthly report living in a notebook on one analyst's laptop is a single point of failure with a person attached (Chapter 78, Q78-025) |

**Likely follow-ups:** How would you put a notebook into production? What is `nbconvert`? How do you review a notebook in a pull request?
**Learn it in:** Chapter 17, section 17.2 (notebooks); Chapter 29 (Python as software, not scripts).

### Rapid-fire, 69A.2: what each thing actually is

| # | Question | The answer | Extra point |
|---|---|---|---|
| Q69A-004 | A database against a data warehouse? | A database serves an application — many small reads and writes. A warehouse serves analysis — few huge reads. Different shapes, both SQL | **[+Edge cases]** which is why running reports on the production database is discouraged → Ch 49 §49.1 |
| Q69A-005 | A data lake against a warehouse? | A lake stores files in their original form and imposes structure when you read. A warehouse imposes structure when you write | **[+Trade-offs]** the lakehouse is the attempt to get both → Ch 49 §49.4 |
| Q69A-006 | ETL against ELT? | Transform before loading, or load raw and transform inside the warehouse. ELT won because warehouse compute got cheap | **[+Business]** ELT keeps the raw data, so a transformation bug is fixable → Ch 77 Q77-001 |
| Q69A-007 | What is NoSQL? | "Not only SQL" — a family of non-tabular stores: documents, key-value, graph, column-family. Not one product and not a SQL competitor | **[+Edge cases]** most of them have added a SQL-like language since → Ch 49 §49.5 |
| Q69A-008 | What is "big data", honestly? | Data too large for one machine to process comfortably. On a modern laptop that threshold is tens of millions of rows, not thousands | **[+Scale]** most companies calling it big data do not have it → Ch 48 §48.1 |
| Q69A-009 | Power BI against Tableau? | Both do the same job. Power BI is cheaper and wins where Microsoft already is; Tableau is stronger at visual exploration. The model matters more than either | **[+Business]** the right answer is usually "whichever your company already pays for" → Ch 16 §16.1 |
| Q69A-010 | BI tool against a notebook? | A BI tool is for questions you will ask repeatedly by people who will not write code. A notebook is for a question asked once | **[+Clarify]** "will this be asked again?" decides it → Ch 16 §16.2 |
| Q69A-011 | A script against a pipeline? | A script runs when you run it. A pipeline has a schedule, dependencies, retries, and tells you when it failed | **[+Edge cases]** the moment someone depends on the output, you need the second → Ch 46 §46.1 |
| Q69A-012 | A model against a rule? | A rule is a condition you wrote. A model is a condition fitted from data. Rules are explainable and brittle; models are the reverse | **[+Business]** start with the rule and measure it; it is often enough → Q69A-019 |
| Q69A-013 | An API against a database connection? | An API is a service you ask over HTTP and which decides what to give you. A database connection is direct access to the tables | **[+Trade-offs]** APIs survive the provider changing their schema; direct access does not → Ch 20 §20.5 |
| Q69A-014 | Git against GitHub? | Git is the version-control program on your machine. GitHub is a website that hosts Git repositories and adds reviews and issues | **[+Edge cases]** GitLab and Bitbucket are the same idea; the Git part is identical → Ch 26 §26.3 |

---

## 69A.3 Excel, or code?

This is the most-asked question in this chapter and the one most often answered badly — including by people who are right about the conclusion.

### Q69A-015 · "Why not just use Excel?"

**Level:** Fresher · **Roles:** DA, DS, BA

**Remember it as:** *Not because Excel is too small. At analyst scale it usually fits. Because Excel cannot tell you what it did last month.*

**Answer in one line:** The usual answer — "Excel cannot handle the data size" — is **wrong at the size most analysts work**, and giving it marks you as someone repeating a line; the real reasons are repeatability, auditability and the cost of doing the same thing again next month.

Start by killing the bad argument, with this book's own data:

| Riverstone table | Rows | Fits in Excel? |
|---|---|---|
| `order_items` | 209,006 | **Yes**, comfortably |
| `orders` | 116,194 | **Yes** |
| `customers` | 5,027 | Yes |
| *Excel's hard limit* | *1,048,576 rows × 16,384 columns* | |

A year of a real mid-sized business fits in a spreadsheet with 80% of the rows to spare. So if size is your argument, you have conceded the question for most of the work you will actually be given.

**The three real reasons**, in the order they bite:

**1. You cannot re-run it.** Next month's data arrives and someone repeats forty manual steps, slightly differently. A script runs again identically. This is the whole argument, and the other two are consequences of it.

**2. You cannot see what it did.** A cell contains a value; how it got there is in a formula, or in a sequence of pastes that left no trace. When Finance asks why the number moved, a spreadsheet often cannot say. A script is the answer to its own question.

**3. It gets slow in a way that wastes *your* time, not the computer's.** On 200,000 joined rows:

```
join + revenue + group by customer, in pandas:  62 ms
```

A spreadsheet does the same with 209,006 lookup formulas that recalculate on every edit. The file still works. Your afternoon does not.

Writing the result out is the same story:

```
csv       9.7 MB    0.4 s
xlsx      7.8 MB   14.1 s
parquet   2.8 MB    0.3 s
```

**Writing one Excel file took 35 times longer than the CSV**, and the Excel file is nearly three times the size of the Parquet one. Put that in a loop over twelve months and the format is the slowest thing in your pipeline.

**And now the part that earns the extra point:** say when Excel wins. Three hundred rows that change once a month, where a finance manager must be able to open it, change an assumption and see the result — that is a spreadsheet, and rewriting it in Python is the wrong call made confidently. Chapter 10 is in this book for a reason.

| Tier | What to say |
|---|---|
| Passes | "Excel does not scale" (the common answer, and the weakest) |
| Strong | + repeatability and auditability as the real reasons, and the correction that size is usually not the issue — 209,006 rows fit comfortably |
| Extra points | **[+Validate]** the measurements: 62 ms for the join and group, 14.1 s to write one xlsx against 0.4 s for a CSV · **[+Business]** names the case where Excel is correct — small, stable, and a non-technical owner who must change assumptions · **[+Clarify]** asks how often this will be run before answering, because once and monthly have different answers · **[+Trade-offs]** Power Query sits in between: repeatable steps, inside Excel, for a team that will not accept a script |

**Likely follow-ups:** When would you keep something in Excel? What is Power Query and where does it sit? How would you move an existing Excel process to Python without the team revolting? *(One step at a time, with the spreadsheet as the check on the script's output.)*
**Red flag:** contempt for spreadsheets. Most of the business runs on them, often correctly, and the attitude reads as inexperience rather than sophistication.
**Learn it in:** Chapter 10 (spreadsheet fundamentals); Chapter 18 (pandas); Chapter 11, section 11.9 (Power Query).

### Q69A-016 · Your stakeholder insists on Excel. Your pipeline is Python. What do you do?

**Level:** Mid · **Roles:** DA, DS, BA

**Remember it as:** *The argument is about the delivery format, not the processing. Give them Excel. Keep the Python.*

**Answer in one line:** Both, and it is not a compromise — the work happens in Python, where it is repeatable, and the **output** is written as a formatted `.xlsx`, because the stakeholder's requirement is about how they receive and use the answer, not about how it was computed.

This is the question's trick: it sounds like a conflict and is not one. Separating the two halves is the entire answer:

| | Where it belongs |
|---|---|
| Reading, joining, cleaning, calculating | Python — repeatable, reviewable, testable |
| What lands in their inbox | Excel — because that is where they work |

`pandas.DataFrame.to_excel` and `openpyxl` write a real workbook with formatting, several sheets and formulas if needed. Chapter 18, section 18.12 does exactly this, and Chapter 20 schedules it.

Two things turn a correct answer into a strong one.

**Take the requirement seriously rather than tolerating it.** They are not being difficult. They need to sort it, filter it, paste a column into a deck and send it to someone who will do the same. A PDF or a dashboard link does not do that. Excel is a *correct* delivery format for that need.

**Then ask the question underneath.** Sometimes "send it in Excel" means "I do not trust the dashboard", or "I need to add my own column", or "I have to forward it to someone outside the company". Each of those has a different and better answer, and you only find out by asking. That is Chapter 69's **[+Clarify]** doing real work.

| Tier | What to say |
|---|---|
| Passes | "Export to Excel at the end" |
| Strong | + separates processing from delivery explicitly, and treats the Excel requirement as legitimate rather than as a concession |
| Extra points | **[+Clarify]** ask what they do with the file after opening it; the answer often changes the design · **[+Business]** a file they can filter and forward is genuinely more useful than a dashboard they cannot · **[+Edge cases]** writing xlsx is slow (14.1 s for 200,000 rows), so for a large export send CSV or split the sheets · **[+Validate]** if they are pasting your output into their own model, you have found an integration, not a report |

**Likely follow-ups:** How would you format it so it is usable rather than a raw dump? What if they want it to update itself? *(Power Query against your output, or a scheduled email — Chapter 20.)* What if two stakeholders want different cuts?
**Learn it in:** Chapter 18, section 18.12 (writing Excel from pandas); Chapter 20 (delivering insights); Chapter 24 (stakeholders).

### Rapid-fire, 69A.3: spreadsheets and the alternatives

| # | Question | The answer | Extra point |
|---|---|---|---|
| Q69A-017 | When is Excel genuinely the right tool? | Small, stable data; a non-technical owner who must change assumptions and see the effect; a one-off. Scenario modelling is its home ground | **[+Business]** rewriting a working spreadsheet in Python with no other benefit is a cost, not a win → Ch 10 §10.1 |
| Q69A-018 | Google Sheets against Excel? | Sheets wins on collaboration and on pulling live data; Excel wins on size, speed and formula depth. Sheets slows noticeably far sooner | **[+Edge cases]** `IMPORTRANGE` and `QUERY` have no Excel equivalent → Ch 70 Q70-034 |
| Q69A-019 | Power Query against writing Python? | Power Query gives repeatable, reviewable steps without leaving Excel. It is the honest middle for a team that will not adopt a script | **[+Trade-offs]** it is harder to version-control and test than Python → Ch 11 §11.9 |
| Q69A-020 | A macro against a Python script? | A macro lives with the file and runs where the user already is. A script is testable, version-controlled and runs without Excel open | **[+Business]** macros also trigger security warnings in most corporate environments → Ch 19 §19.1 |
| Q69A-021 | Why do finance teams resist moving off spreadsheets? | Because they can see and change every number, and they are accountable for them. That is a reasonable position, not ignorance | **[+Clarify]** address the control concern, not the tooling → Ch 24 §24.4 |
| Q69A-022 | A dashboard against a spreadsheet sent by email? | A dashboard is one version of the truth that nobody can edit. An emailed file is forked the moment it is forwarded | **[+Business]** which is exactly why some stakeholders prefer the file → Q69A-016 |

---

## 69A.4 Which database, and why

### Q69A-023 · PostgreSQL or MySQL — how would you choose?

**Level:** Mid · **Roles:** DA, DE, DS

**Remember it as:** *For most work there is no difference that matters. The honest answer names what would actually decide it, and the existing team is usually the deciding factor.*

**Answer in one line:** For the work an analyst or a typical application does, **either is fine and the choice rarely matters** — so the strong answer is what *would* decide it: what your team already runs, what your cloud provider manages, and a short list of features where they genuinely differ.

Resist the urge to declare a winner. Then give the list, because this is a question where specifics separate a real answer from a confident one:

| Where they differ | PostgreSQL | MySQL |
|---|---|---|
| Analytical SQL | Richer: full window functions, `FILTER`, recursive CTEs, strong JSON | Caught up substantially in 8.0; still fewer corners |
| Data types | `jsonb`, arrays, ranges, geometry via PostGIS, custom types | A shorter list |
| Strictness | Rejects bad data by default | Historically permissive; stricter now, but legacy databases carry the old settings |
| Read-heavy simple workloads | Fine | Often marginally faster, and very widely deployed |
| Ecosystem | The default for analytics and for most new projects | The default under a great deal of existing web software |

The behaviours this book has already shown you are the concrete version of "different accents": `NULL` sorts last on an ascending sort in PostgreSQL and first in MySQL (Chapter 71, Q71-086); `\|\|` concatenates in PostgreSQL and means OR in MySQL; `7 / 2` is `3` in PostgreSQL and `3.5` in MySQL (Q71-090). None of those decides an architecture. All of them break a query you ported without reading.

**What actually decides it, in order:**

1. **What the team already runs.** One database your team knows beats a better one nobody can operate at 2am.
2. **What your cloud provider manages for you.** Managed service, backups, failover and patching matter far more day to day than feature lists.
3. **What the application framework expects**, if there is one.
4. **Then**, and only then, the feature differences above.

The answer that fails is a preference with no conditions attached. The answer that lands is "it depends, and here is specifically on what."

| Tier | What to say |
|---|---|
| Passes | "They're both relational databases, either works" |
| Strong | + names real differences — window-function and JSON depth, type system, strictness — and says the team and the managed service usually decide it |
| Extra points | **[+Business]** operational familiarity beats feature superiority, because the cost shows up during an incident · **[+Edge cases]** the dialect differences that break a ported query, with an example · **[+Trade-offs]** PostgreSQL is the safer default for analytics; MySQL is the safer default for inheriting an existing web application · **[+Clarify]** ask what it is for — an application database and an analytics database are different questions |

**Likely follow-ups:** What would make you choose a warehouse instead? What is MariaDB? *(A MySQL fork; mostly compatible.)* Have you migrated between them, and what broke?
**Red flag:** a strong preference with no conditions. It reads as taste rather than experience.
**Learn it in:** Chapter 12, section 12.16 and Chapter 71, section 71.8 (where the dialects differ); Chapter 49 (storage choices).

### Q69A-024 · Why not just use SQLite?

**Level:** Mid · **Roles:** DE, DS, DA

**Remember it as:** *One writer at a time. That is the whole answer, and it is a design decision rather than a weakness.*

**Answer in one line:** Because SQLite allows **many readers but only one writer**, and it has no server — so the moment two processes write, or the data must be reachable over a network with users and permissions, it is the wrong shape; for everything else it is excellent and under-used.

The design is the explanation. SQLite is a **library that reads and writes a file**, not a server. There is no process to connect to, no port, no user accounts. That gives it the properties people love:

- **Zero setup.** No install, no service, no credentials. It ships inside Python.
- **The whole database is one file.** Copy it, email it, commit it.
- **Genuinely fast** for single-process work, often faster than a server database, because there is no network between you and the data.

And the properties that rule it out:

- **One writer.** The file is locked for writing; concurrent writes wait, then time out.
- **No users or permissions.** Access to the file is access to everything.
- **No network access** without building a server around it, at which point you have made a worse PostgreSQL.

So the test is one question: **will more than one process write to it at the same time?** No, and SQLite is probably the right and simplest answer. Yes, and you need a server database.

The cases where it is right are more common than its reputation suggests: a local analysis cache, a desktop application, a test fixture that makes the suite fast, an embedded store on a device, and a single-user tool. It is reportedly the most widely deployed database in the world, because it is in every phone and browser.

| Tier | What to say |
|---|---|
| Passes | "SQLite doesn't handle concurrency" |
| Strong | + that it is a library rather than a server, with the single-writer lock and the absence of users as the specific consequences, and names where it is the right choice |
| Extra points | **[+Business]** "one file you can copy" is a real advantage for sharing an analysis or a test fixture · **[+Scale]** it is often *faster* than a server database single-process, because nothing crosses a network · **[+Edge cases]** WAL mode improves concurrent reading alongside a writer but does not give you multiple writers · **[+Trade-offs]** DuckDB is the analytical equivalent — same embedded simplicity, column-oriented, built for aggregation |

**Likely follow-ups:** What is DuckDB and when would you reach for it? What is WAL mode? Would you use SQLite in production? *(Yes — for the right shape of problem, and it is in production on billions of devices.)*
**Learn it in:** Chapter 12, section 12.1 (what a database is); Chapter 49, section 49.2.

### Rapid-fire, 69A.4: storage choices

| # | Question | The answer | Extra point |
|---|---|---|---|
| Q69A-025 | Why not run analytics on the production database? | Your long query competes with the application for the same resources, and can slow or lock the thing customers use | **[+Business]** a read replica or a warehouse costs less than an outage → Ch 49 §49.1 |
| Q69A-026 | Why a warehouse rather than a bigger Postgres? | Column storage and separated compute: a warehouse scans one column of a billion rows cheaply. Postgres stores rows together | **[+Scale]** it is the format, not the size, that is the difference → Ch 49 §49.3 |
| Q69A-027 | Why not keep everything in one wide table? | Updates become expensive and inconsistent, and the same fact lives in many rows. That is what normalisation is for | **[+Trade-offs]** analytics deliberately denormalises for read speed — different job, different rules → Ch 28 §28.7 |
| Q69A-028 | When is a NoSQL document store the right answer? | When the shape of each record genuinely varies and you query by key, not by joining. Not "when there is a lot of data" | **[+Edge cases]** most "we need NoSQL" turns out to be "we need an index" → Ch 49 §49.5 |
| Q69A-029 | Why not just use CSV files for everything? | No types, no constraints, no index, no concurrent access, and a quoted comma breaks naive parsing. Fine as an interchange format, poor as a store | **[+Validate]** Parquet keeps types and is 3× smaller → Ch 77 Q77-041 |
| Q69A-030 | Snowflake against BigQuery against Redshift? | Same job, different operating models and pricing. The decision is usually which cloud you are already in and how your costs behave | **[+Business]** the pricing model matters more than the benchmark → Ch 65 §65.2 |
| Q69A-031 | What is a read replica, and what does it not solve? | A copy kept in sync for reading, taking load off the primary. It does not fix a slow query, and it lags | **[+Edge cases]** reading your own write immediately after it may miss → Ch 61 §61.3 |

---

## 69A.5 Which language, and when

### Q69A-032 · Why Python and not R?

**Level:** Mid · **Roles:** DA, DS, MLE

**Remember it as:** *R was built by statisticians for statistics. Python is a general language that grew excellent data tools. Which matters depends on whether your work ends at the analysis.*

**Answer in one line:** Both are genuinely good at analysis, and Python usually wins on everything that happens **after** the analysis — putting a model behind an API, writing the pipeline, the engineering around it — while R remains stronger for deep statistics, and the honest answer says so rather than dismissing it.

Where each is genuinely better, without the tribalism:

| | R | Python |
|---|---|---|
| Statistical depth | Stronger. New methods appear in R first; the modelling output is richer by default | Good; statsmodels covers most of it |
| Data manipulation | `dplyr` is arguably more elegant than pandas | pandas is more widely known |
| Visualisation | `ggplot2` is still the benchmark | matplotlib is clunkier; seaborn and plotly narrow the gap |
| Reports and dashboards | R Markdown and Shiny are excellent and underrated | More tools, less coherent |
| **Everything that is not analysis** | Weak | **Strong — this is the decider** |

That last row is the answer. Pipelines, APIs, model serving, cloud SDKs, testing frameworks, orchestration: all of it is Python-first, because Python is a general-purpose programming language that acquired data tools, while R is a statistics environment that acquired general-purpose features.

So the division in practice: **if your work ends with the finding, R is a strong choice. If your work ends with something running, Python.** Most data jobs in industry are now the second kind, which is why Python dominates the job ads — and this book teaches Python for that reason and says so.

**Two moves that turn this into a strong answer.** First, do not disparage R; many excellent statisticians use it and the interviewer may be one. Second, point out that the concepts transfer almost entirely — a dataframe, a group-by, a join and a model are the same ideas in both — so the choice is far less consequential than it sounds in a job ad.

| Tier | What to say |
|---|---|
| Passes | "Python is more widely used in industry" |
| Strong | + where R is genuinely better — statistical depth, `ggplot2`, Shiny — and names the real divider: everything that happens after the analysis |
| Extra points | **[+Business]** the ecosystem outside analysis decides most industry roles, which is why job ads skew Python · **[+Trade-offs]** in academia, biostatistics and econometrics R is often still the better choice · **[+Edge cases]** the two interoperate — `reticulate`, Arrow — so it is rarely either/or at a team level · **[+Clarify]** ask what happens to the output after the analysis; that answers the question |

**Likely follow-ups:** Would you learn R if the team used it? *(Yes — a week, the concepts transfer.)* What about Julia or Scala? When does SQL do the job instead of either?
**Red flag:** dismissing R as outdated. It is widely used, actively developed, and the interviewer may have built their career on it.
**Learn it in:** Chapter 7, section 7.4 (the tool landscape); Chapter 17 (Python from zero).

### Q69A-033 · This could be done in SQL or in pandas. How do you choose?

**Level:** Mid · **Roles:** DA, DS, DE

**Remember it as:** *Do the filtering and aggregating where the data already lives. Pull the smallest thing that answers the question.*

**Answer in one line:** Do as much as possible **in the database** — filtering, joining and aggregating next to the data is faster and moves less of it — and switch to pandas when you need something SQL is bad at: iterative reshaping, modelling, plotting, or anything genuinely procedural.

The default and the reason behind it:

```sql
-- the right shape: the database returns 24 rows
SELECT customer_id, sum(quantity * unit_price) AS revenue
FROM order_items GROUP BY customer_id;
```

```python
# the wrong shape: 209,006 rows cross the network so pandas can do the same sum
df = pd.read_sql("SELECT * FROM order_items", conn)
df.groupby('customer_id').revenue.sum()
```

Both give the same answer. The second moves **209,006 rows** over a network and into memory to produce 24. On a laptop against a local database you will not notice; against a warehouse holding a hundred million rows it is the difference between a query and an outage.

**Where pandas is genuinely better:**

- Anything **iterative** — try a transformation, look, adjust. SQL makes you rewrite the whole statement.
- **Reshaping** — pivot, melt, fill, interpolate.
- **Modelling and plotting**, which SQL does not do.
- **Combining sources** that are not in the same database — a CSV, an API response and a table.

**Where SQL is genuinely better:**

- Filtering and aggregating at any size.
- Joins, which the engine optimises with indexes and statistics.
- Anything that must run on a schedule, where the result belongs in a table.
- Work other people will read — SQL is the lingua franca; a pandas chain is not.

The strong answer is the shape rather than a rule: **SQL to get the right rows, pandas to do things to them.**

| Tier | What to say |
|---|---|
| Passes | "Use SQL for big data, pandas for small" |
| Strong | + "push the work to the data": aggregate in SQL, pull the small result, reshape and model in pandas — with the row counts to show why |
| Extra points | **[+Scale]** `SELECT *` into pandas is the classic version of this mistake and it scales terribly (Chapter 77, Q77-026) · **[+Business]** SQL is readable by more of the company, so the logic is auditable by people who are not you · **[+Trade-offs]** dbt exists precisely to make transformation-in-SQL testable and version-controlled · **[+Edge cases]** very complex procedural logic becomes unreadable SQL; that is the signal to move it |

**Likely follow-ups:** What is predicate pushdown? How would you handle a join across two different databases? When would you use DuckDB over both?
**Learn it in:** Chapter 13 (SQL for real analysis); Chapter 18 (pandas); Chapter 32 (dbt).

### Rapid-fire, 69A.5: language and tool choice

| # | Question | The answer | Extra point |
|---|---|---|---|
| Q69A-034 | Do you still need SQL if you know pandas? | Yes. The data is in a database, the company's logic is written in SQL, and every data interview tests it | **[+Business]** SQL is the one skill every data role shares → Ch 12 §12.0 |
| Q69A-035 | Why learn the command line? | Because servers have no desktop, logs live in files, and the tools compose. Ten commands cover most of it | **[+Scale]** `grep` on a 10 GB file beats opening it anywhere → Ch 34 §34.1 |
| Q69A-036 | Why use Git for analysis work, not just software? | So you can answer "what did this script do in March" and recover from a bad change. Analysis is code | **[+Business]** it is also how two analysts work on the same thing → Ch 26 §26.3 |
| Q69A-037 | Why a virtual environment? | So one project's library versions cannot break another's. Two projects needing different pandas is normal | **[+Validate]** "works on my machine" is usually this → Ch 17 §17.0 |
| Q69A-038 | Why not just use the latest version of everything? | Because a minor version can change behaviour silently. Pin versions and upgrade deliberately | **[+Edge cases]** this book's own code changed behaviour between Python 3.11 and 3.12 → Ch 72A Q72A-042 |
| Q69A-039 | Why would a team choose Polars or DuckDB over pandas? | Speed and memory on larger-than-comfortable data, and DuckDB lets you write SQL against files directly | **[+Trade-offs]** pandas has a far larger ecosystem; the concepts transfer either way → Ch 48 §48.4 |
| Q69A-040 | Is Jupyter a language? | No — an interface for running code, mostly Python, in cells. The language is Python | **[+Edge cases]** it runs other kernels, including R and SQL → Ch 17 §17.2 |

---

## 69A.6 When not to use the clever thing

The questions in this section are where senior candidates separate themselves, because the expected answer is a recommendation and the right answer is often a refusal.

### Q69A-041 · "Should we use machine learning for this?"

**Level:** Senior · **Roles:** DS, MLE, DA

**Remember it as:** *A model earns its place by beating a rule you have already measured. If you have not measured the rule, you cannot know.*

**Answer in one line:** Usually **not first** — write the obvious rule, measure it honestly, and reach for a model only when the rule's errors are costing more than the model's maintenance will; most problems that arrive described as machine learning are solved by a definition, a query and a threshold.

The four questions to ask before saying yes, out loud and in this order:

**1. Is there a rule that is good enough?** "Flag an account with no order in 90 days" is a churn model a junior analyst can write in SQL by lunchtime. If it catches most of what matters, the ML project needs to beat *it*, not beat nothing.

**2. Do you have labelled outcomes?** Not data — *outcomes*. To predict churn you need to know who churned, which means a definition of churn everyone agrees on, and history of it. Most "we want to predict X" conversations end here, and should.

**3. Will anyone act on the prediction?** A churn score with no retention budget and nobody to call the customer is a number in a dashboard. The model's value is the action it triggers, not the AUC.

**4. Can you live with being wrong in this way?** A model is wrong sometimes by design. For a product recommendation that is fine. For a decision that denies someone credit, it is a regulated and explainable decision, and a rule may be required.

If all four pass, build the model — and still build the rule first, because the rule is your baseline and without it you cannot say whether the model is any good (Chapter 74).

**The move that marks a senior answer:** be willing to say no, and be specific about what would change your mind. "Not yet — we do not have an agreed churn definition. Give me three weeks to define it and label last year, and then it is a real question" is a better answer than any architecture.

| Tier | What to say |
|---|---|
| Passes | "It depends on the data" |
| Strong | + the four questions — rule, labels, action, tolerance for error — and insists on a measured baseline either way |
| Extra points | **[+Business]** the model's value is the action it enables, so a prediction nobody acts on is worth nothing however accurate · **[+Validate]** a simple baseline is non-negotiable; without it "85% accurate" means nothing (Chapter 74, Q74-007) · **[+Scale]** a model is a system to maintain, retrain and monitor — not a deliverable · **[+Clarify]** ask what decision changes as a result; if nobody can say, that is the finding |

**Likely follow-ups:** What baseline would you use for churn? How would you measure whether the model beat the rule? What if the business insists on ML for its own sake? *(Build the rule, show the numbers, let them choose with information.)*
**Red flag:** reaching for a model because the question mentioned prediction. It is the most expensive instinct in the field.
**Learn it in:** Chapter 36, section 36.1 (the ML workflow); Chapter 74, section 74.1.

### Q69A-042 · "Can we use an LLM for this?"

**Level:** Senior · **Roles:** DS, MLE, DE, DA

**Remember it as:** *If the task has one right answer that a rule can check, an LLM is the wrong tool. Its strength is language, not arithmetic.*

**Answer in one line:** An LLM is excellent at **language with no single correct answer** — summarising, drafting, classifying messy free text — and a poor and expensive choice for anything deterministic, which is most of what a data team is asked for.

The division that answers nearly every version of this question:

| Reach for an LLM when | Do not when |
|---|---|
| The input is unstructured text and the output is judgement | The answer is a number a query can produce |
| A regular expression would need fifty cases | A regular expression would need three |
| Being approximately right is useful | Being exactly right is required |
| The work is drafting that a human will check | The output goes straight into a report |

Three specific reasons to refuse, worth having ready:

**It cannot do arithmetic reliably**, and it will produce a confident number anyway. "Total our Q3 revenue" is a `SUM`. Asking a language model is slower, costs money per call, and is sometimes wrong in a way that looks right.

**It is not deterministic**, so the same question can give different answers — which makes testing hard and auditing harder (Chapter 79, Q79-011).

**It costs per call, forever.** A regex costs nothing after you write it. At a million rows a day that difference is the whole budget.

**Where it genuinely earns its place:** classifying support tickets by theme when the themes are not known in advance; summarising free-text survey answers; extracting structured fields from messy documents; drafting the first version of a report that a human edits. The common thread is **text in, judgement out, with a human or a check downstream.**

| Tier | What to say |
|---|---|
| Passes | "LLMs are good for text" |
| Strong | + the deterministic-against-judgement division, and names cost, non-determinism and arithmetic as the three specific reasons to refuse |
| Extra points | **[+Business]** per-call cost scales with volume forever, where a rule is written once · **[+Validate]** anything an LLM outputs that feeds a number needs a deterministic check around it · **[+Edge cases]** hybrid is often right: an LLM extracts structure, then ordinary code does the arithmetic · **[+Trade-offs]** a smaller fine-tuned classifier often beats an LLM on a fixed set of categories, at a fraction of the cost |

**Likely follow-ups:** How would you evaluate an LLM feature? *(Chapter 79, Q79-023.)* What is RAG for? When would you fine-tune instead of prompt?
**Red flag:** proposing an LLM for a task with one right answer. It is the 2026 version of reaching for ML.
**Learn it in:** Chapter 54 (LLMs); Chapter 79, section 79.1.

### Rapid-fire, 69A.6: restraint

| # | Question | The answer | Extra point |
|---|---|---|---|
| Q69A-043 | Should every manual task be automated? | No. Automation costs build time and maintenance forever. Frequency × time saved against build × upkeep | **[+Business]** a yearly 20-minute task is not worth two days of code → Ch 78 Q78-026 |
| Q69A-044 | Why not move everything to the cloud? | Cost, lock-in, and skills you may not have. Managed services are excellent and are not free | **[+Business]** cloud bills surprise people because they are usage-based → Ch 65 §65.1 |
| Q69A-045 | Why not use an orchestrator for a single daily script? | Because cron plus an alert may be the whole requirement. Airflow is infrastructure to run and keep alive | **[+Scale]** the case for an orchestrator is dependencies and backfills, not scheduling → Ch 46 §46.2 |
| Q69A-046 | Why not microservices? | Each one multiplies into the availability and the latency of every request through it. Five 99.9% services in series give 99.5% | **[+Validate]** the measurement is in Ch 80 Q80-031 |
| Q69A-047 | Why not a real-time pipeline? | Because almost nothing needs it. "Real time" usually means "by 9am", which is a batch job | **[+Clarify]** ask what decision is made faster as a result → Ch 50 §50.1 |
| Q69A-048 | Why not a data lake if storage is cheap? | Storage is cheap; finding, trusting and governing it is not. An ungoverned lake becomes a swamp | **[+Business]** the cost is discoverability, not disk → Ch 49 §49.4 |
| Q69A-049 | Why not deep learning on tabular data? | Gradient boosting usually wins on tables, trains in minutes and explains itself better | **[+Edge cases]** deep learning wins on text, images and audio → Ch 43 §43.1 |
| Q69A-050 | Why not just hire more analysts instead of building tooling? | Sometimes right. But manual work scales linearly and does not compound; a pipeline keeps paying | **[+Trade-offs]** the honest answer costs both out → Ch 66 §66.3 |
| Q69A-051 | Why not rewrite the legacy system? | Because it encodes years of edge cases nobody wrote down. Strangle it gradually instead | **[+Business]** rewrites famously overrun because the spec is the old code → Ch 62 §62.4 |

---

## 69A.7 Defending a choice you did not make

### Q69A-052 · "Why does your team use [tool]?" — and you were not there when it was chosen

**Level:** Mid · **Roles:** DA, DS, DE, BA, MLE

**Remember it as:** *"I do not know, it was already there" is honest and weak. Reconstruct the trade-off, then say what you have observed since.*

**Answer in one line:** Say plainly that it predates you, then **reconstruct the likely reasoning and evaluate it from what you have seen** — because the interviewer is testing whether you think about your tools at all, not whether you signed the purchase order.

The three-part shape that works for any tool:

**1. Be straight about it.** "That was chosen before I joined." One sentence, no apology. Pretending otherwise falls apart under one follow-up.

**2. Reconstruct the reasoning.** "Looking at it, I would guess it was chosen because we were already on Azure and the licence was bundled, and because the team came from a Microsoft background." This shows you have thought about why your environment is the way it is.

**3. Evaluate it honestly, both directions.** "It has worked well for the standard reports. Where it strains is ad-hoc analysis — people export to Excel to do anything unusual, which tells you something."

That third part is what the question is really for. An engineer who can see the limits of their own stack is far more valuable than one who defends it, and far safer than one who hates everything they have used.

**Two traps.** Do not trash it — you will sound like someone who will trash this team next year. And do not defend it unconditionally — that reads as not having noticed anything in two years.

| Tier | What to say |
|---|---|
| Passes | "It was already there when I joined" |
| Strong | + reconstructs the likely trade-off and evaluates it from observation, naming one thing that works and one that strains |
| Extra points | **[+Business]** the "people export to Excel to do anything unusual" kind of observation is evidence you watch how work really happens · **[+Clarify]** if you genuinely do not know, say what you would ask to find out · **[+Trade-offs]** name what you would choose today and what would have to be true to justify changing, which is a different and harder question than preference |

**Likely follow-ups:** What would you choose today? What would it cost to migrate? What have you changed since joining?
**Red flag:** criticising a previous employer's tooling with contempt. Interviewers hear a preview.
**Learn it in:** Chapter 69, section 69.3 (the extra-point moves); Chapter 80, section 80.5 (influence without authority).

### Rapid-fire, 69A.7: judgement under pressure

| # | Question | The answer | Extra point |
|---|---|---|---|
| Q69A-053 | "What's your favourite tool?" | Answer with a problem it solved, not a product. Favouritism about tools is a mild red flag | **[+Business]** "whichever the team can maintain" is a senior answer → Ch 69 §69.3 |
| Q69A-054 | "You have two days. SQL or Python?" | Whichever gets a trustworthy answer in two days. Constraint questions test whether you optimise for the constraint given | **[+Clarify]** ask what happens on day three → Ch 75 §75.1 |
| Q69A-055 | "Our stack is all X. You've only used Y." | Say so, name what transfers (most of it), and give an example of a tool you picked up quickly | **[+Validate]** concepts transfer; syntax is a week → Ch 76A Q76A-002 |
| Q69A-056 | "Would you have done this differently?" about their system | Yes, carefully: one specific thing, with the condition under which their choice was right | **[+Trade-offs]** "I would want to know X before saying" is a legitimate answer → Ch 80 Q80-017 |
| Q69A-057 | "Why are you not using AI for this?" from a senior stakeholder | Answer the business question under it: what would improve, and what it would cost to find out | **[+Business]** a cheap experiment beats an argument → Q69A-042 |
| Q69A-058 | "This should take an hour." It will take three days. | Say the number, then the breakdown, then what you could deliver in an hour that is genuinely useful | **[+Clarify]** often the hour version answers the real question → Ch 24 §24.3 |
| Q69A-059 | Asked to justify a tool you dislike | Give the honest case for it first. Being able to argue the other side is the senior signal | **[+Trade-offs]** then name the condition under which you would switch → Ch 80 §80.5 |
| Q69A-060 | "What would you do differently with no constraints?" | A trap worth taking seriously: unconstrained answers reveal whether you understand why constraints exist | **[+Business]** name the constraint you would remove first and why → Ch 80 §80.6 |

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Answering "why not Excel?" with "it doesn't scale" | Wrong at analyst scale, and it sounds rehearsed | Repeatability and auditability are the real reasons; 209,006 rows fit comfortably (Q69A-015) |
| Declaring a winner between two reasonable tools | Reads as taste, not experience | Name the conditions that would decide it, then say which usually wins and why (Q69A-023) |
| Treating "SQL" and "MySQL" as the same word | Signals shallow experience in one sentence | Language, dialect, engine, server, database — five distinct things (Q69A-001) |
| Reaching for a model because the question said "predict" | Expensive, slow, often beaten by a rule | Write the rule, measure it, make the model beat it (Q69A-041) |
| Proposing an LLM for a deterministic task | Costs per call forever and is sometimes confidently wrong | Text in, judgement out, with a check downstream (Q69A-042) |
| Trashing a previous employer's stack | Interviewers hear how you will talk about them | One thing that worked, one that strained, no contempt (Q69A-052) |
| Defending every tool you have used | Suggests you have not noticed anything | Evaluating your own stack honestly is the senior signal |
| Dismissing R, spreadsheets or anything "old" | The interviewer may have built a career on it | Judge tools by fit, and say what each is genuinely good at |

---

## In the real world: the question before the question

A data analyst candidate was asked, in the first five minutes of a screening call, "so why did your last team use Python rather than just doing it in Excel?"

She could have listed Python's advantages. Instead she said: "Honestly, a lot of it could have been done in Excel — the data was about forty thousand rows, which fits fine. The reason we moved was that the month-end pack took two days of manual work and nobody could reproduce last month's numbers when Finance queried them. After we moved it, the run was twenty minutes and we could show exactly how every figure was produced. The size was never the problem."

The interviewer told her afterwards that the answer decided the call. Not because it was clever, but because every other candidate had said "Excel can't handle large datasets", and she was the only one who had evidently watched why a team actually changed.

The question was never about Python. It was about whether she understood the problem her tools were solving.

---

## Project

**Goal:** be able to defend every tool in your own stack, including the ones you did not choose.

1. List every tool you use in a week. For each, write two sentences: what it is for, and what you would use instead if it vanished tomorrow.
2. Pick the three you did not choose. For each, reconstruct the likely trade-off (Q69A-052), then name one thing that works well and one that strains.
3. Take the one you like least. Write the honest case **for** it, as if you had to persuade someone. If you cannot, you do not understand it well enough to criticise it.
4. Answer Q69A-015 out loud, timed, in ninety seconds, without saying the word "scale".
5. Take one task you automated. Work out honestly whether it was worth building, using Chapter 78's frequency-against-build arithmetic. Write down the answer even if it is no.

---

## Key terms

query language · dialect · database engine · database server · library · vectorisation · hidden state · notebook → script → package · repeatability · auditability · Power Query · single-writer lock · MVCC · read replica · normalisation · denormalisation · column storage · push the work to the data · predicate pushdown · baseline · labelled outcome · determinism · per-call cost · build-against-upkeep · strangler pattern · lock-in · reconstructing a trade-off

---

## Final-week revision list

Q69A-001, Q69A-015, Q69A-016, Q69A-023, Q69A-024, Q69A-032, Q69A-033, Q69A-041, Q69A-042, Q69A-052.

Those ten cover the questions most likely to open an interview, in the order they are usually asked. Q69A-015 and Q69A-023 are the two worth having word-perfect: they come up in almost every screening call, and most candidates answer both badly.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric every answer here is written against; this chapter is where its **[+Clarify]** and **[+Trade-offs]** moves earn the most.
- **Chapters 70 to 82** test whether you can use the tools this chapter asks you to choose between.
- **Chapter 80, Architecture & Leadership,** is this chapter at a larger scale: the same judgement, applied to systems rather than to tools, and with a budget attached.
