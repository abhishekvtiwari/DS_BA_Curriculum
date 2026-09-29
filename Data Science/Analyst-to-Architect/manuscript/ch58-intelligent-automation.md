# Chapter 58. Intelligent Automation

*Part 6 — Production ML, Generative AI & MLOps*

> **Chapter at a glance**
>
> **You will learn to:** tell the three generations of automation apart and pick the right one · choose what to automate using volume, variability, rules, and the cost of an error · assemble Chapters 54 to 57 into a pipeline that writes to a system of record · make writes **idempotent**, transactional, and auditable · design an approval threshold priced in money rather than guessed · classify exceptions so each one gets retried, held, escalated, or rejected · measure straight-through rate *and* silent error rate, which are the same system described two ways · do the ROI arithmetic honestly, including the review time and the cost of being wrong · roll out in stages with a gate at each one · and handle the conversation with the person whose job you just changed.
>
> **Before you start:** Chapter 54 (extraction, and validation in section 54.7), Chapter 57 (prompt versions, tolerant parsing, the meter, fallbacks), Chapter 55 (tools that act), Chapter 49 (SQLite from Python, section 49.2), Chapter 12 (constraints and transactions, section 12.13), Chapter 29 (idempotency, your own exceptions, tests), Chapter 22 (confidence intervals).
>
> **Time needed:** 16–20 hours, spread over three weeks, in three sittings: sections 58.0–58.4 (setup, choosing, and building the pipeline that writes), about 7 hours; sections 58.5–58.8 (gates, exceptions, measurement, money, rollout), about 6 hours; sections 58.9–58.10, the project and the exercises take the rest.
>
> **Tools:** Python with SQLite (the standard library's `sqlite3`), and the companion modules from Chapters 54 and 57. Nothing new to install, no API key, no account.
>
> **Practice system:** Riverstone's purchase-order intake. The 60 emails from Chapter 54, a real SQLite order book with an audit log, and the approval rules that decide what reaches it.

---

## Why this matters

This is the chapter Chapter 1 promised. Chapter 1 (section 1.7) described the order that arrives by email and is re-typed by hand, and Chapter 3 showed where that re-typing sits in Riverstone's order-to-cash process. Every part since has added a piece: SQL to store orders, Python to read them, a model to extract them, evaluation to trust the extraction, and operations to keep it running.

Now the last step, which is different in kind from all the others: **the pipeline writes.** Until now a wrong answer was a sentence on a screen. From here, a wrong answer is a row in the order book, a picking list in the warehouse, and a lorry going to the wrong address.

That change brings four questions that have nothing to do with models:

- **How do I make sure the same email never creates two orders?**
- **What gets written automatically, and what waits for a person?**
- **When it goes wrong, who is accountable, and what does the log say?**
- **Is this actually worth doing?** The honest arithmetic in section 58.7 says something this chapter's own pipeline does not want to hear.

---

## In plain English

**Automation is not replacing a person with a program. It is moving a person from typing to deciding.**

Riverstone's sales coordinator reads an email, works out what was ordered, types it into the ERP, and moves on. Three of those four steps are mechanical and one is judgment. A good automation does the mechanical three and hands the judgment back, with the evidence attached.

That framing decides everything else in the chapter:

- **The queue is the product.** A pipeline that hands 12% of emails to a person with clear reasons is doing its job. The danger is the other 88%: section 58.7 shows that 19% of the orders this pipeline loads without a human are quietly wrong. A number that says "88% automatic" says nothing about whether the 88% is right.
- **The write is the dangerous part.** Reading is reversible, writing is not, so the write needs uniqueness rules, a transaction, and a log.
- **The threshold is a business decision.** "Which orders can go straight through?" is a question about money, and section 58.5 computes an answer.
- **The person is not the obstacle.** They are the escalation path, the quality check, and the only one who knows when the model's confident answer is nonsense.

---

## 58.0 Setting up

Nothing new needs installing. SQLite, the small database that lives in one file, comes with Python as the `sqlite3` module, and Chapter 49 (section 49.2) already used it. What this chapter needs is Chapter 54's 60 practice emails and Chapter 57's two modules, `pipeline.py` and `provider.py`. Open a terminal, activate the book's virtual environment (Chapter 17, section 17.0), and go to the companion folder:

```
# terminal
$ cd companion/ch58
$ ls ../ch54/order_data
emails
ground_truth.json
$ python erp.py
erp.db rebuilt with tables: audit_log, order_lines, orders
```

- `ls ../ch54/order_data` checks that Chapter 54's emails are there (`..` is the folder above, Chapter 26, section 26.0). If it says *No such file or directory*, run Chapter 54's generator first: `cd ../ch54`, then `python generate_order_emails.py`, then `cd ../ch58`.
- `python erp.py` creates this chapter's order book, a file called `erp.db`, with three empty tables. Section 58.4 opens it up.

Start Jupyter from this folder and run every cell of the chapter in order, in one notebook: later cells use names that earlier cells made. The first cell brings in the pieces:

```python
import sys
sys.path.insert(0, ".")
import erp
import intake
from pipeline import build_prompt, load_emails, tolerant_parse
from provider import PINNED_MODEL, Meter, call

truth, emails = load_emails()
print(f"{len(emails)} emails, from {min(emails)} to {max(emails)}")
print(emails["email_004"])
```

```
60 emails, from email_001 to email_060
From: admin@coastal.example
To: orders@riverstone.example
Subject: PO attached (details below)
Date: 21 Feb 2026

Hello Riverstone,

Order reference: PO-52049

- Food Container Set (104) x 25 nos
- Lunch Box Set (107) x 30 nos

Required by: 2026-02-28

Thanks and regards,
P. Shah
Coastal Foods
```

- `sys.path.insert(0, ".")` lets Python import modules from the notebook's own folder, as in Chapter 55. `erp.py` is the order book; `intake.py` is the pipeline this chapter builds.
- Importing `intake` also tells Python where Chapters 54 and 57 keep their files: its first lines add `../ch57` and `../ch54` to `sys.path`. That is why the next line can import `build_prompt` and `tolerant_parse` from Chapter 57's `pipeline.py`, and `call`, `Meter` and `PINNED_MODEL` from its `provider.py`.
- `load_emails()` returns two dictionaries keyed by email name: `emails`, the text of each email, and `truth`, the correct order for each one, recorded in Chapter 54. **The pipeline never sees `truth`.** It gets the emails only, as it would in production. `truth` is for measuring the pipeline in sections 58.5 to 58.8, which is possible only because these 60 emails were labelled by hand.
- `min(emails)` and `max(emails)` give the first and last names in alphabetical order.

These 60 emails arrived in February 2026, and this chapter processes them as one run at 06:00 on Monday 2 March 2026. That is about a day and a half of Riverstone's real volume, so **the rates carry over to a real day and the counts do not**. The run's time is passed into the code rather than read from the clock, so your output matches the book's.

As in Chapters 54 and 57, the model is a **local stand-in**, not a language model: `call` answers with Chapter 54's text rules, so the pipeline runs with no account and every number repeats exactly. The pipeline around it, which is this chapter's subject, is real.

---

## 58.1 Three generations of automation

| Generation | How it works | Good at | Breaks when |
|---|---|---|---|
| **Macros and RPA** | software repeats the clicks and keystrokes a person would make, inside one application (a macro, Chapter 19) or across several (**RPA**, robotic process automation, which often reads data off the screen: **screen scraping**) | legacy systems with no API, where change is impossible | the screen changes, or the system is upgraded |
| **API and integration** | systems talk directly, with contracts | anything with an interface; the durable answer | the data is unstructured, so there is nothing to send |
| **Model-assisted** | a model turns unstructured input into structured data, then integration takes over | email, documents, photographs, free text | the model is confidently wrong and nothing checks it |

Riverstone's purchase orders need the third feeding the second: a model reads the email, and an ordinary insert writes the order. **The model is the smallest part of the system and the only part anyone wants to talk about.**

> **Watch out: RPA is a bridge, not a destination.** Screen-scraping robots are sold as "no integration needed" and their maintenance cost is real, ongoing, and invisible at purchase. They earn their place where a system truly has no API and cannot be changed, and every such deployment should carry an expiry date and a plan to replace it.

---

## 58.2 What to automate, and what to leave alone

Four questions, in this order:

| Question | Automate when | Leave alone when |
|---|---|---|
| **Volume** | it happens many times a day | it happens twice a month |
| **Variability** | inputs vary within a describable range | every case really is different |
| **Rules** | the decision can be written down | the decision needs context nobody has captured |
| **Cost of an error** | a wrong result is caught quickly and cheaply | a wrong result is expensive and silent |

**Riverstone's purchase orders score well on the first three and badly on the fourth**, which is exactly why this chapter ends where it does. Twenty to forty emails a day, five recognizable shapes, rules that finance already wrote, and an error that becomes a wrong delivery two days later. (Chapter 3's 40 orders a week at six minutes each were round numbers for illustration. By now Riverstone receives 20 to 40 a day, and a practised coordinator takes about three minutes each.)

The trap is to rank candidates by annoyance. The most-complained-about task is often low volume and high judgment, which makes it the worst candidate and the most requested one. Rank by **volume × time per item**, then filter by the cost of an error.

---

## 58.3 The pipeline, assembled

The pipeline's stages, and where each came from:

| Stage | What it does | From |
|---|---|---|
| Read | fetch the email | this chapter (a folder stands in for the mailbox) |
| Extract | model call, pinned version, prompt v3 | Chapters 54 and 57 |
| Parse | comments removed, dates normalized | Chapter 57 |
| Validate | PO shape, real product codes, plausible dates and quantities | Chapter 54 |
| Decide | load, wait for approval, or hold for a person | this chapter |
| Write | one transaction, idempotent, audited | this chapter |
| Report | counts, the queue with reasons, cost | Chapters 56 and 57 |

Follow one email through the first four stages. **Before you run it, predict:** email_004 (printed above) has two bulleted lines. How many items will the extracted order have?

```python
meter = Meter()
reply = call(build_prompt("v3", emails["email_004"]), meter=meter)
order = tolerant_parse(reply)
for key, value in order.items():
    print(f"{key}: {value}")
```

```
customer: Coastal Foods
po_number: PO-52049
delivery_date: 2026-02-28
items: [{'product_code': '104', 'quantity': 25}, {'product_code': '107', 'quantity': 30}]
```

- `build_prompt("v3", text)` is Chapter 57's prompt registry at work (section 57.2): version v3 is Chapter 54's prompt with one worked example, followed by the email.
- `call(...)` is the one function that talks to the model (Chapter 57). With no `model=` argument it uses the pinned version, `PINNED_MODEL`. Passing `meter=meter` counts the tokens, so the run can report its cost.
- `tolerant_parse(reply)` turns the reply into a Python dictionary, after removing comment lines and putting a day-first date right (Chapter 57, section 57.4). It returns `None` if the reply is not JSON at all.
- `for key, value in order.items():` prints one field per line. Two items, as the email has two bullets: this one is right. Section 58.7 counts how often that is true.

Then validation, which is section 54.7's `validate` function, copied into `intake.py` with the processing day set to this run's morning:

```python
from intake import validate

problems = validate(order)
print("email_004:", problems or "no problems")
print("email_045:", validate(tolerant_parse(call(build_prompt("v3", emails["email_045"])))))
```

```
email_004: no problems
email_045: ['no items']
```

`validate` returns a list of problems, and an empty list counts as false, so `problems or "no problems"` prints the words when there are none. The second line runs a different email through all three steps at once: the model found no order lines in it, and validation says so in words a person can read.

Now the new stage. `decide` looks at one extracted order and returns where it goes, and why:

```python
APPROVAL_LIMIT = 100_000          # rupees: above this, a person signs the order off
PIPELINE_VERSION = f"intake-v1 (prompt v3, {PINNED_MODEL})"

def decide(order, problems, approval_limit=APPROVAL_LIMIT):
    """Where one extracted order goes, and why: held, awaiting_approval, or loaded."""
    if problems:
        return "held", "; ".join(problems)
    rupees = erp.order_value_paise(order["items"]) / 100
    if rupees > approval_limit:
        return "awaiting_approval", f"value ₹{rupees:,.0f} is over the ₹{approval_limit:,} limit"
    return "loaded", ""

print(decide(order, problems))
print(decide(order, problems, approval_limit=10_000))
print(decide(None, ["reply was not valid JSON"]))
```

```
('loaded', '')
('awaiting_approval', 'value ₹26,900 is over the ₹10,000 limit')
('held', 'reply was not valid JSON')
```

**Line by line:**

- `APPROVAL_LIMIT` is finance's rule: an order worth more than ₹1,00,000 needs a person's signature. `PIPELINE_VERSION` names this version of the pipeline, including the prompt and the pinned model. It goes on every audit row in section 58.4.
- `decide` returns **two values**, a status and a reason, as a tuple (Chapter 17). The three statuses are the three places an email can go: `held` (validation failed; nothing is written), `awaiting_approval` (written, but a person must approve it), and `loaded` (written, and on its way).
- `"; ".join(problems)` joins the list of problems into one line of text.
- `erp.order_value_paise(items)` prices the order from Riverstone's list prices (the `products` table of the `riverstone_2025` database) in whole **paise**, the hundredth part of a rupee; dividing by 100 gives rupees. Section 58.4 says why money is kept in paise.
- The three calls show all three outcomes: email_004's order is worth ₹26,900, so it loads; the same order with a ₹10,000 limit waits for approval; and a reply that was not JSON is held. **What happens if you change the limit** to ₹26,900 exactly? It loads, because the rule is "more than", not "at least". Rules like that belong in writing, because finance will ask.

---

## 58.4 Writing to a system of record

A **system of record** is the database a business treats as the truth (Chapter 45): here, Riverstone's order book. Writing to it safely needs three properties. This section builds each one, then runs the whole morning.

### The order book: three tables

Here is the schema `erp.py` creates, one table at a time. First the orders:

<!-- run: none -->
```sql
CREATE TABLE orders (
    order_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    po_number          TEXT    NOT NULL,
    customer           TEXT    NOT NULL,
    delivery_date      TEXT    NOT NULL,
    order_value_paise  INTEGER NOT NULL,         -- money as whole paise
    source_email       TEXT    NOT NULL UNIQUE,  -- the idempotency key
    status             TEXT    NOT NULL
        CHECK (status IN ('loaded', 'awaiting_approval')),
    created_at         TEXT    NOT NULL,
    UNIQUE (customer, po_number)                 -- one PO, one order
);
```

**Line by line:**

- `INTEGER PRIMARY KEY AUTOINCREMENT` is SQLite's automatic ID: the database hands out the next number itself, as `GENERATED ALWAYS AS IDENTITY` does in PostgreSQL (Chapter 12, section 12.13). You never type an ID.
- `po_number`, `customer` and `delivery_date` are the extracted fields, all `NOT NULL`: validation has already refused an order without them. `created_at` records when the row was written.
- `order_value_paise INTEGER`: **money as whole paise, never a floating-point number.** Chapter 12's watch-out explained why: a `REAL` column stores approximations, and sums of approximate rupees drift. ₹26,900 is stored as 2690000. (In PostgreSQL you would use `NUMERIC(12, 2)` instead.)
- `CHECK (status IN ('loaded', 'awaiting_approval'))` is a rule every row must pass (Chapter 12), so a typo such as `'laoded'` is refused rather than stored.
- `source_email ... UNIQUE` is the **idempotency key**: one email, at most one order. An operation is **idempotent** when doing it twice has the same effect as doing it once (Chapter 29). A retry, a replay of the whole morning, and two workers racing on the same email all end in the same state.
- `UNIQUE (customer, po_number)` covers a different case. **A customer who resends a PO sends a new email**, with a new name, so the first key cannot catch it. This second key refuses a second order for the same customer and PO number. A PO number is a **business key**: the identifier the business itself uses.

Then the lines of each order, and the audit log:

<!-- run: none -->
```sql
CREATE TABLE order_lines (
    line_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id          INTEGER NOT NULL REFERENCES orders (order_id),
    product_code      TEXT    NOT NULL,
    quantity          INTEGER NOT NULL,
    unit_price_paise  INTEGER NOT NULL
);

CREATE TABLE audit_log (
    entry_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        TEXT NOT NULL,   -- which run: the second it started
    source_email  TEXT NOT NULL,   -- which input
    action        TEXT NOT NULL,   -- proposed, loaded, held, ...
    actor         TEXT NOT NULL,   -- pipeline version, or a person
    detail        TEXT NOT NULL    -- the reason, in words
);
```

- `REFERENCES orders (order_id)` makes every order line belong to a real order, as in Chapter 12. The unit price is in paise too.
- The audit table has one row per step, and its columns answer who, what, when and why: `source_email` is the input, `action` what happened (`proposed`, `loaded`, `held` and so on), `actor` the pipeline version or the person, and `detail` the reason in words. `entry_id` numbers the rows in the order they were written. `run_id` holds the second the run started, so the rows of one run can be grouped and two runs told apart.

**Put the guarantee in the database**, because application-level checks lose races and get refactored away.

`erp.py` also opens the database. Its `connect` function has one line you have not seen:

<!-- run: none -->
```python
def connect():
    connection = sqlite3.connect(DB)
    connection.execute("PRAGMA foreign_keys = ON")    # make SQLite check REFERENCES
    connection.row_factory = sqlite3.Row              # rows you can read by column name
    return connection
```

- `PRAGMA foreign_keys = ON` switches on a setting: SQLite ignores `REFERENCES` unless you ask it to check them, once per connection.
- `connection.row_factory = sqlite3.Row` makes every row you fetch readable by column name, so you can write `row["n"]` instead of `row[0]`. Chapter 49 used positions; names are harder to get wrong.

`erp.rebuild()` drops the three tables and creates them empty. Rebuild, and list what the database holds:

```python
erp.rebuild()
connection = erp.connect()
for row in connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"):
    print(row["name"])
```

```
audit_log
order_lines
orders
sqlite_sequence
```

`sqlite_master` is SQLite's own list of what a database contains. The fourth table, `sqlite_sequence`, is where `AUTOINCREMENT` remembers the last number it handed out.

### A transaction: the header and the lines together

An order is written as one row in `orders` (the **header**) and one row per item in `order_lines`. If the program fails after the header and before the last line, the order book holds an order with two of its three lines. That is the worst possible outcome: it looks complete and ships short.

Chapter 12 (section 12.13) met the cure in SQL: a **transaction**, `BEGIN` … `COMMIT`, with `ROLLBACK` to undo everything since `BEGIN`. In Python's `sqlite3`, `with connection:` is that transaction: it begins, commits at the end of the block, and rolls back if anything inside raises an error. (It does not close the connection; `connection.close()` does that.)

See it undo a half-written order. The cell writes a header, then fails on purpose before any line is written:

```python
INSERT_ORDER = ("INSERT INTO orders (po_number, customer, delivery_date, order_value_paise, "
                "source_email, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)")
header = ("PO-00001", "Test Customer", "2026-03-10", 5_000_000, "test_email", "loaded",
          "2026-03-02T06:00:00")

try:
    with connection:
        cursor = connection.execute(INSERT_ORDER, header)
        print("header written as order", cursor.lastrowid)
        raise RuntimeError("the ERP stopped before the lines were written")
except RuntimeError as error:
    print("error:", error)

print("orders now:", connection.execute("SELECT COUNT(*) AS n FROM orders").fetchone()["n"])
```

```
header written as order 1
error: the ERP stopped before the lines were written
orders now: 0
```

**Line by line:**

- `INSERT_ORDER` holds the insert statement, and `header` one order's seven values in the same order as the columns. `5_000_000` paise is ₹50,000; the underscores only make the number easier to read.
- Each `?` in the SQL is a **placeholder**. `sqlite3` fills them, in order, from the tuple passed as the second argument, and it quotes each value safely. This is the `sqlite3` form of Chapter 18's `:name` parameters, and it is why you never build SQL by pasting values into a string (Chapter 29 showed how that goes wrong).
- `cursor.lastrowid` is the ID SQLite just gave the new row: the order number the lines must point to.
- `raise RuntimeError(...)` stands in for anything that can fail halfway: a bad product code, a full disk, the power. The error leaves the `with` block, so the transaction rolls back, and `except` catches the error so the notebook can carry on.
- The header was written, and printed its number, but the count afterwards is 0: **the rollback took it away.** Any write that spans more than one table belongs in one transaction.

### The two keys, and the error they raise

When a `UNIQUE` rule is broken, SQLite refuses the insert with `sqlite3.IntegrityError`. Try both keys. The first insert below is fine; the second reuses its email name with a new PO number; the third reuses its customer and PO number from a new email:

```python
import sqlite3

with connection:
    connection.execute(INSERT_ORDER, header)

same_email = ("PO-00002", "Test Customer", "2026-03-10", 5_000_000, "test_email", "loaded",
              "2026-03-02T06:00:00")
same_po = ("PO-00001", "Test Customer", "2026-03-10", 5_000_000, "test_email_resent",
           "loaded", "2026-03-02T06:00:00")
for attempt in (same_email, same_po):
    try:
        with connection:
            connection.execute(INSERT_ORDER, attempt)
    except sqlite3.IntegrityError as error:
        print("refused:", error)
```

```
refused: UNIQUE constraint failed: orders.source_email
refused: UNIQUE constraint failed: orders.customer, orders.po_number
```

- The first `with connection:` block writes the test order for real, so the next two inserts have something to clash with. `INSERT_ORDER` and `header` are the ones from the previous cell.
- `same_email` keeps the email name and changes the PO number; `same_po` keeps the customer and PO number and changes the email name.
- `for attempt in (same_email, same_po):` tries each in turn, in its own transaction. `except sqlite3.IntegrityError as error:` catches the refusal and prints SQLite's message, so the loop carries on to the second attempt.

The error names the rule that stopped it. When an insert breaks both rules at once, as a replayed email does, SQLite names only one of them, so the pipeline below asks the table which case it is instead of reading the message.

### `write`: one order, safely

Here is the function that does the writing, with all three properties:

```python
def write(connection, run_id, name, order, status, reason):
    """Write one order and its lines in one transaction. Returns (what happened, why)."""
    try:
        with connection:
            cursor = connection.execute(
                "INSERT INTO orders (po_number, customer, delivery_date, order_value_paise, "
                "source_email, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (order["po_number"], order["customer"], order["delivery_date"],
                 erp.order_value_paise(order["items"]), name, status, run_id))
            order_id = cursor.lastrowid
            for item in order["items"]:
                connection.execute(
                    "INSERT INTO order_lines (order_id, product_code, quantity, unit_price_paise) "
                    "VALUES (?, ?, ?, ?)",
                    (order_id, item["product_code"], item["quantity"],
                     erp.PRICES[item["product_code"]] * 100))
            detail = f"order {order_id}, {len(order['items'])} lines"
            erp.log(connection, run_id, name, status, PIPELINE_VERSION, detail)
        return status, reason
    except sqlite3.IntegrityError:
        same_email = connection.execute(
            "SELECT order_id FROM orders WHERE source_email = ?", (name,)).fetchone()
        if same_email:
            status = "duplicate_ignored"
            reason = f"this email is already order {same_email['order_id']}"
        else:
            status = "duplicate_po"
            reason = f"{order['customer']} already has an order for {order['po_number']}"
        with connection:
            erp.log(connection, run_id, name, status, PIPELINE_VERSION, reason)
        return status, reason
```

**Line by line:**

- The parameters: the open `connection`, the `run_id` (the run's start time, which also goes into `created_at`), the email's `name`, the extracted `order`, and the `status` and `reason` that `decide` chose.
- Inside one `with connection:` block: the header insert, `order_id = cursor.lastrowid`, one insert per item, and the audit row. `erp.log` inserts one row into `audit_log`; because it sits inside the block, **the audit row commits with the order or not at all**. The unit price is stored in paise too.
- `except sqlite3.IntegrityError:` is how a broken `UNIQUE` rule becomes a counted outcome instead of a crash. The rollback has already happened; the function then looks up the email name. If this email is already in the order book, the outcome is `duplicate_ignored`: a harmless repeat, recorded. Otherwise the clash was on the customer and PO number, and the outcome is `duplicate_po`. That is **possibly a resend and possibly a genuine amendment**, so it goes to a person rather than being ignored.
- The audit row for a duplicate has its own small transaction, `with connection:` again, because the first one was rolled back.

Try it on email_004, three times: the first write, the same email again five minutes later, and the same order arriving as a new email:

```python
erp.rebuild()
connection = erp.connect()
status, reason = decide(order, problems)
print(write(connection, "2026-03-02T06:00:00", "email_004", order, status, reason))
print(write(connection, "2026-03-02T06:05:12", "email_004", order, status, reason))
print(write(connection, "2026-03-02T06:05:12", "email_004_resent", order, status, reason))
```

```
('loaded', '')
('duplicate_ignored', 'this email is already order 1')
('duplicate_po', 'Coastal Foods already has an order for PO-52049')
```

### The whole morning: `run`

`run` puts the stages together for a dictionary of emails. It writes a `proposed` audit row for every email, whatever happens next, and a `held` row for every email that fails validation:

```python
from collections import Counter

QUEUED = ("held", "awaiting_approval", "duplicate_po")   # the outcomes a person must look at

def run(emails, run_id="2026-03-02T06:00:00", approval_limit=APPROVAL_LIMIT, meter=None):
    """One intake run over a dictionary of emails. Returns the counts and the queue."""
    connection = erp.connect()
    counts = Counter()
    queue = []
    for name, text in emails.items():
        order = tolerant_parse(call(build_prompt("v3", text), meter=meter))
        problems = ["reply was not valid JSON"] if order is None else validate(order)
        status, reason = decide(order, problems, approval_limit)
        with connection:
            erp.log(connection, run_id, name, "proposed", PIPELINE_VERSION,
                    "; ".join(problems) or "clean")
        if status == "held":
            with connection:
                erp.log(connection, run_id, name, "held", PIPELINE_VERSION, reason)
        else:
            status, reason = write(connection, run_id, name, order, status, reason)
        counts[status] += 1
        if status in QUEUED:
            queue.append({"email": name, "status": status, "reason": reason})
    connection.close()
    return {"counts": dict(counts), "queue": queue}
```

**Line by line:**

- `Counter()` counts things by name (Chapter 17): `counts["loaded"] += 1` works even before the first `loaded`, starting from 0.
- The loop body is the stage table in order: extract and parse, validate (a reply that isn't JSON becomes one problem), decide, log the proposal, then either log the hold or write.
- `"; ".join(problems) or "clean"`: an empty list joins to an empty string, which counts as false, so `or` supplies the word `clean`.
- `write` may change the status (to `duplicate_ignored` or `duplicate_po`), which is why its result is assigned back to `status, reason`.
- The **queue** is every email a person must look at, with its reason. `QUEUED` lists the three statuses that put an email there.
- `run_id` has a default, the first run's start time, and `meter=None` means "don't count tokens" unless a meter is passed.

Now the whole morning:

```python
erp.rebuild()
meter = Meter()
result = run(emails, meter=meter)

total = sum(result["counts"].values())
print(f"{total} test emails processed (Chapter 54's practice set)")
for status, count in sorted(result["counts"].items()):
    print(f"  {status.replace('_', ' '):<20} {count:>3}")
print(f"\nstraight-through rate: {result['counts']['loaded'] / total:.0%}")
print(f"model cost for the run: ₹{meter.cost_rupees():.2f}")
```

```
60 test emails processed (Chapter 54's practice set)
  awaiting approval      6
  held                   1
  loaded                53

straight-through rate: 88%
model cost for the run: ₹4.71
```

- `sorted(result["counts"].items())` lists the counts in alphabetical order of status, so the output is the same every time. `.replace('_', ' ')` turns `awaiting_approval` into words; `:<20` pads to 20 characters, and `:>3` right-aligns the count.
- The **straight-through rate** is the share of emails that became orders with no person involved: 53 of 60. The other 7 are the queue: 6 orders over the approval limit, written but waiting, and 1 email held because validation found no items.
- `meter.cost_rupees()` is Chapter 57's meter (section 57.5): what 60 model calls cost at the pinned model's price.

![A pipeline from email through extract, parse, validate and decide to write; decide sends 53 orders to loaded and 6 to awaiting approval, and validate sends 1 email to held for review](figures/fig58-1-intake-pipeline.svg)

*Figure 58.1 — The model is the second box. Everything that makes this safe is in the last one.*

### Replaying the morning

Prove the idempotency key works by running the entire morning again, as a scheduler that fires twice would:

```python
connection = erp.connect()
before = connection.execute("SELECT COUNT(*) AS n FROM orders").fetchone()["n"]
replay = run(emails, run_id="2026-03-02T06:05:12")      # the same emails again, by accident
after = connection.execute("SELECT COUNT(*) AS n FROM orders").fetchone()["n"]
dupes = connection.execute("SELECT COUNT(*) AS n FROM audit_log WHERE action = ?",
                           ("duplicate_ignored",)).fetchone()["n"]

print(f"orders before the replay: {before}")
print(f"orders after replaying every email: {after}")
print(f"what the replay did: {replay['counts']}")
print(f"audit rows recording an ignored duplicate: {dupes}")
```

```
orders before the replay: 59
orders after replaying every email: 59
what the replay did: {'duplicate_ignored': 59, 'held': 1}
audit rows recording an ignored duplicate: 59
```

- The `?` placeholder takes a tuple, and a tuple with one value needs a trailing comma: `("duplicate_ignored",)`. Without the comma, the brackets are just brackets and Python passes a string.
- The replay is stamped `06:05:12`, so its audit rows can be told apart from the 06:00 run's.

Nothing was written twice, and **the attempts were still recorded**: 59 ignored duplicates, and 59 audit rows saying so. It is 59, not 60, because the email held for review was never written, so there was nothing to duplicate; the replay held it again. That distinction matters in an audit: "we ignored 59 duplicate submissions" is a fact somebody will eventually need.

### The audit log: what was proposed, what was written, by what

```python
print("what the audit log holds after two runs:")
for row in connection.execute(
        "SELECT action, COUNT(*) AS n FROM audit_log GROUP BY action ORDER BY n DESC"):
    print(f"  {row['action']:<20} {row['n']:>4}")

print("\none email's history:")
for row in connection.execute(
        "SELECT run_id, action, detail FROM audit_log WHERE source_email = ? ORDER BY entry_id",
        ("email_004",)):
    print(f"  {row['run_id']}  {row['action']:<18} {row['detail']}")
actor = connection.execute("SELECT DISTINCT actor FROM audit_log").fetchone()["actor"]
print("actor on every row:", actor)
```

```
what the audit log holds after two runs:
  proposed              120
  duplicate_ignored      59
  loaded                 53
  awaiting_approval       6
  held                    2

one email's history:
  2026-03-02T06:00:00  proposed           clean
  2026-03-02T06:00:00  loaded             order 4, 2 lines
  2026-03-02T06:05:12  proposed           clean
  2026-03-02T06:05:12  duplicate_ignored  this email is already order 4
actor on every row: intake-v1 (prompt v3, workhorse-001)
```

`GROUP BY` and `ORDER BY` are Chapter 12's; `ORDER BY n DESC` puts the most common action first, and `ORDER BY entry_id` shows one email's rows in the order they were written. `SELECT DISTINCT actor` lists each different actor once, and `.fetchone()` takes the first, because there is only one. Two runs of 60 emails give 120 `proposed` rows; the first run wrote 53 `loaded` and 6 `awaiting_approval`; each run held the same email once; and the replay recorded 59 ignored duplicates. email_004's history reads like a story: proposed and loaded as order 4 at 06:00, proposed again and ignored at 06:05:12.

**What the log has to contain**, in any system that writes automatically:

| Field | The question it answers |
|---|---|
| Source identifier | which input caused this? |
| Action | proposed, loaded, awaiting approval, held, duplicate ignored, approved |
| Actor | which pipeline version, or which person |
| Detail | the reason, in words a person can read |
| Run and time | which run, and when, to the second |

**"The model proposed it" is not an accountable answer.** The pipeline version is the accountable answer, and the approval record names the human when there was one. Chapter 64 covers the governance; this is the minimum that makes it possible.

---

## 58.5 The human in the loop

Two gates, and they do different jobs.

- **Validation** (Chapter 54) catches malformed output: no PO number, an unknown product code, a date in 1926. Riverstone holds those for a person and writes nothing.
- **The approval threshold** catches *large* output. A correctly extracted order for ₹8 lakh is well-formed and worth a human glance, because the cost of being wrong scales with the value.

Sweep the limit and watch what changes:

```python
for limit in (0, 50_000, 100_000, 200_000):
    erp.rebuild()
    counts = run(emails, approval_limit=limit)["counts"]
    loaded = counts.get("loaded", 0)
    approvals = counts.get("awaiting_approval", 0)
    print(f"limit ₹{limit:>7,}: loaded {loaded:>2}, awaiting approval {approvals:>2}, "
          f"held {counts['held']}, straight through {loaded / len(emails):.0%}")
```

```
limit ₹      0: loaded  0, awaiting approval 59, held 1, straight through 0%
limit ₹ 50,000: loaded 40, awaiting approval 19, held 1, straight through 67%
limit ₹100,000: loaded 53, awaiting approval  6, held 1, straight through 88%
limit ₹200,000: loaded 59, awaiting approval  0, held 1, straight through 98%
```

**Line by line:** the limit is the only thing changing. `counts.get("loaded", 0)` returns 0 when a status never happened (at ₹0 nothing loads). At ₹0 everything waits for a person, which is not automation at all; with no limit everything is written unseen. The rows in between are the actual choice.

### Pricing the threshold

To put a price on each limit you need two costs: the review time each approval takes, and the cost of each wrong order that loads without a person. The second needs to know which loaded orders are wrong, and for these 60 emails you can check, because you have `truth`. (Section 58.7 looks at that number properly; here it is one input to the price.)

A function that compares one order in the order book with the right answer:

```python
def is_correct(connection, row, truth):
    """Does an order in the ERP match the right answer for its email?"""
    want = truth[row["source_email"]]
    lines = connection.execute("SELECT product_code, quantity FROM order_lines WHERE order_id = ?",
                               (row["order_id"],)).fetchall()
    got_items = sorted((line["product_code"], line["quantity"]) for line in lines)
    want_items = sorted((item["product_code"], item["quantity"]) for item in want["items"])
    return (row["po_number"] == want["po_number"] and row["customer"] == want["customer"]
            and row["delivery_date"] == want["delivery_date"] and got_items == want_items)

erp.rebuild()
run(emails)
connection = erp.connect()
first = connection.execute("SELECT * FROM orders WHERE source_email = ?", ("email_004",)).fetchone()
print(first["po_number"], first["customer"], is_correct(connection, first, truth))
```

```
PO-52049 Coastal Foods True
```

- `want` is the correct order for the email this row came from.
- The items are compared as **sorted lists of (product code, quantity) pairs**, because the order of lines in an email doesn't matter: `sorted` puts both lists in the same order first. `.fetchall()` returns every row of the query as a list.
- The function returns `True` only if the PO number, customer, delivery date and every line all match. It is the same test as Chapter 54's `mark`, applied to what actually reached the database.

Now the price. The rates are Riverstone's: a coordinator costs ₹300 an hour fully loaded, and handling one queued order properly takes about two minutes.

```python
COST_PER_HOUR = 300             # a coordinator's fully loaded cost per hour, rupees
MINUTES_QUEUE = 2.0             # handle one queued order properly: an estimate
COST_OF_A_WRONG_ORDER = 2_000   # credit note, re-delivery, the customer call: finance's estimate

print(f"{'limit ₹':>9}{'approvals':>11}{'wrong loaded':>14}"
      f"{'review ₹':>10}{'errors ₹':>10}{'total ₹':>9}")
for limit in (0, 50_000, 100_000, 200_000):
    erp.rebuild()
    counts = run(emails, approval_limit=limit)["counts"]
    connection = erp.connect()
    loaded_rows = connection.execute("SELECT * FROM orders WHERE status = 'loaded'").fetchall()
    wrong = sum(not is_correct(connection, row, truth) for row in loaded_rows)
    review = counts.get("awaiting_approval", 0) * MINUTES_QUEUE / 60 * COST_PER_HOUR
    errors = wrong * COST_OF_A_WRONG_ORDER
    print(f"{limit:>9,}{counts.get('awaiting_approval', 0):>11}{wrong:>14}"
          f"{review:>10,.0f}{errors:>10,}{review + errors:>9,.0f}")
```

```
  limit ₹  approvals  wrong loaded  review ₹  errors ₹  total ₹
        0         59             0       590         0      590
   50,000         19             7       190    14,000   14,190
  100,000          6            10        60    20,000   20,060
  200,000          0            12         0    24,000   24,000
```

**Line by line:**

- The three constants carry their sources in the comments. ₹300 an hour is the loaded rate the book has used since Part 2. The two-minute and ₹2,000 figures are estimates, which exercise 9 tests.
- `sum(not is_correct(...) for row in loaded_rows)` counts the wrong ones: `not` turns each `False` into `True`, and `sum` counts a `True` as 1.
- `review` is approvals × 2 minutes, converted to hours and priced. `errors` is the wrong orders that loaded with no one looking, at ₹2,000 each.

Read the `total` column. **At this pipeline's accuracy, every step up from ₹0 costs more in errors than it saves in review.** Each approval avoided saves ₹10 of review time (2 minutes at ₹5 a minute), and each wrong order that loads costs ₹2,000, so raising the limit pays only if fewer than 1 in 200 of the orders it releases is wrong. Here 7 of the 40 orders under ₹50,000 are wrong.

That is the rule for any threshold: **raise the limit only while the review time it saves is worth more than the errors it lets through.** Today the money says every order should be seen by a person, which is the conclusion section 58.7 reaches from the other side. The ₹1,00,000 limit starts to earn its keep once the orders under it are reliably right, which is section 58.8's subject.

**Designing the queue, which is where most automation projects are won or lost:**

- **One screen**, showing the email beside the proposed order. The reviewer's job is to compare, not to retype.
- **The reason, in words**: "delivery_date not YYYY-MM-DD: '04 Mar'", not "validation error 7".
- **Accept, correct, or reject**, with correction as the common case. A corrected order is also a training example and a golden-set candidate (Chapter 57).
- **Bounded**: if the queue is longer than a person can clear in a morning, the thresholds are wrong, not the person.
- **Measured**: queue length, time to clear, and correction rate per reason. The reason that generates the most corrections is your next engineering task.

---

## 58.6 Exceptions, classified

Every automation needs a taxonomy, because "it failed" is not an instruction.

| Class | Example | What the pipeline does |
|---|---|---|
| **Transient** | the provider rate-limits; the ERP is restarting | retry with backoff (Chapter 57), then queue |
| **Malformed input** | the email is a PDF photo, or an out-of-office reply | route to a different handler, or reject with a reason |
| **Uncertain extraction** | validation fails; two POs in one email | hold for a person, with the email attached |
| **Policy** | order value over the limit; a customer on credit hold | write as pending, notify the owner |
| **Unknown reference** | a product code that isn't ours | reject to a person: never guess a foreign key |
| **Duplicate** | the same email is read twice (a retry, a replay) | ignore, and record that you did |
| **Possible duplicate PO** | a customer resends or amends a PO in a new email | hold for a person: it may be a genuine amendment |
| **Systemic** | 60 of 60 replies unusable (Chapter 57's provider change) | stop the run, alert, process nothing more |

That last row deserves its own rule: **a pipeline should refuse to continue when the failure rate crosses a threshold.** Processing 60 emails wrongly is much worse than processing none, and a run that quietly sends every email to the queue is not much better: that was Chapter 57's Monday, when 52 of 52 replies were unparseable and nobody noticed until 11:00. Chapter 57 (section 57.8) met a **circuit breaker** that stops calling a failing provider; this one guards the whole batch, and it takes a few lines. Here they are as `intake.py` has them, at the end of `run`'s loop, with the settings and the error they raise:

<!-- run: none -->
```python
BREAKER_SHARE = 0.2               # stop when more than 20% of the batch has failed validation...
BREAKER_MINIMUM = 10              # ...once at least 10 emails have been processed

class BatchAborted(Exception):
    """Raised when so much of a batch fails that the run should stop and a person should look."""

        # inside run's loop, after counting each email:
        processed = sum(counts.values())
        if processed >= BREAKER_MINIMUM and counts["held"] > BREAKER_SHARE * processed:
            message = f"{counts['held']} of {processed} emails failed validation"
            with connection:
                erp.log(connection, run_id, "(batch)", "batch_aborted", PIPELINE_VERSION, message)
            connection.close()
            raise BatchAborted(message)
```

- `class BatchAborted(Exception)` makes a new kind of error with its own name, as Chapter 57 did for `RateLimitError` (Chapter 29 showed the pattern).
- After each email, the breaker compares the number held with 20% of the emails processed so far. It waits for at least 10, so that one bad email at the start of a run can't stop it.
- When it trips, it writes a `batch_aborted` audit row, closes the connection, and **raises**. A scheduled job that raises fails loudly: the scheduler (Chapter 46) marks the run failed and alerts someone, where a quiet `return` would look like success.

`intake.py`'s `run` is the `run` you wrote above plus these lines, so import it and feed it a bad morning: twelve out-of-office replies arriving before the real emails.

```python
from intake import run, BatchAborted

batch = {f"autoreply_{i:02d}": "I am out of the office until Monday." for i in range(1, 13)}
batch.update(emails)
erp.rebuild()
try:
    run(batch)
except BatchAborted as error:
    print("run stopped:", error)
connection = erp.connect()
print("orders written:", connection.execute("SELECT COUNT(*) AS n FROM orders").fetchone()["n"])
print("last audit row:", tuple(connection.execute(
    "SELECT source_email, action, detail FROM audit_log ORDER BY entry_id DESC").fetchone()))
```

```
run stopped: 10 of 10 emails failed validation
orders written: 0
last audit row: ('(batch)', 'batch_aborted', '10 of 10 emails failed validation')
```

- The dictionary comprehension makes twelve emails named `autoreply_01` to `autoreply_12` (`:02d` pads the number to two digits), each with the same useless text. `batch.update(emails)` adds the 60 real emails after them.
- `except BatchAborted as error:` catches the breaker's error and prints its message. The last line reads the newest audit row: `ORDER BY entry_id DESC` sorts newest first, and `tuple(...)` prints the row's three values.
- The run stopped at the tenth email, wrote nothing, and left a reason in the log. **Change it to** `range(1, 3)`, two autoreplies, and the breaker never trips: 2 failures in the first 10 is 20%, not more than 20%.

From here on, `run` is `intake.py`'s. It behaves exactly like yours on the 60 practice emails, where only one email is held.

---

## 58.7 Measuring it honestly

Here is the number everybody quotes, and the number that decides whether this should ship.

```python
erp.rebuild()
run(emails)
connection = erp.connect()
loaded_rows = connection.execute("SELECT * FROM orders WHERE status = 'loaded'").fetchall()
loaded = len(loaded_rows)
correct = sum(is_correct(connection, row, truth) for row in loaded_rows)
wrong = loaded - correct

print(f"orders loaded without a human: {loaded}")
print(f"  of those, correct:          {correct}")
print(f"  of those, silently wrong:   {wrong}  ({wrong / loaded:.0%})")
print(f"\nstraight-through rate: {loaded / len(emails):.0%}   "
      f"silent error rate: {wrong / loaded:.0%}")
```

```
orders loaded without a human: 53
  of those, correct:          43
  of those, silently wrong:   10  (19%)

straight-through rate: 88%   silent error rate: 19%
```

The **silent error rate** is the share of automatically loaded orders that are wrong: wrong in a way no check noticed, so no one hears about it until the customer does. `sum(is_correct(...) ...)` counts the `True` results, the correct orders.

**Those two percentages describe the same system, and only one of them appears in most business cases.** An 88% straight-through rate sounds like a success. A 19% silent error rate means roughly one order in five that nobody looks at is wrong: a wrong quantity, a missing line.

Now price it for a real day. First the inputs, each with its source:

```python
EMAILS_PER_DAY = 40             # section 58.2: twenty to forty a day; plan for the busy end
MINUTES_MANUAL = 3.0            # read the email, type it into the ERP (the story below timed it)
MINUTES_REVIEW = 0.75           # compare a draft with the email and accept it: an estimate
REVIEW_CATCH_RATE = 0.9         # a reviewer spots 9 wrong drafts in 10: an assumption to measure

straight_through = loaded / len(emails)
error_rate = wrong / loaded
queue_share = 1 - straight_through        # the emails that go to a person in every design

manual_minutes = EMAILS_PER_DAY * MINUTES_MANUAL
assisted_minutes = EMAILS_PER_DAY * MINUTES_REVIEW + EMAILS_PER_DAY * queue_share * MINUTES_QUEUE
auto_minutes = EMAILS_PER_DAY * queue_share * MINUTES_QUEUE

unattended_errors = EMAILS_PER_DAY * straight_through * error_rate   # wrong orders a day, unseen
assisted_errors = unattended_errors * (1 - REVIEW_CATCH_RATE)        # the ones a reviewer misses
print(f"queue share {queue_share:.1%}; wrong orders a day unseen {unattended_errors:.2f}, "
      f"missed by a reviewer {assisted_errors:.2f}")
```

```
queue share 11.7%; wrong orders a day unseen 6.67, missed by a reviewer 0.67
```

**Line by line:**

- Three designs are compared. **Manual**: the coordinator types every order. **Assisted**: the model drafts every order and a person reviews each one before it is written. **Straight through**: orders under the limit load unseen, and a person handles only the queue.
- `queue_share` is `1 - straight_through`, the 7 emails in 60 that reach a person in every design (the approvals and the hold). Assisted mode reviews every draft *and* works that queue.
- `REVIEW_CATCH_RATE` is the honest part. A person reviewing mostly-correct drafts does not catch every error: after a week of drafts that are right, attention drops (section 58.9 comes back to this). Nine in ten is an assumption, and the shadow stage in section 58.8 is where you measure it.
- `unattended_errors` is how many wrong orders a day would load with nobody looking; `assisted_errors` is how many of those a reviewer would miss.

Then the table:

```python
print(f"{'approach':<22}{'minutes/day':>12}{'labour ₹':>10}"
      f"{'errors/day':>12}{'error cost ₹':>14}{'total ₹':>9}")
for label, minutes, errors in [("manual (today)", manual_minutes, 0.0),
                               ("assisted: review each", assisted_minutes, assisted_errors),
                               ("straight through", auto_minutes, unattended_errors)]:
    labour = minutes / 60 * COST_PER_HOUR
    error_cost = errors * COST_OF_A_WRONG_ORDER
    print(f"{label:<22}{minutes:>12.0f}{labour:>10.0f}{errors:>12.2f}{error_cost:>14,.0f}"
          f"{labour + error_cost:>9,.0f}")
```

```
approach               minutes/day  labour ₹  errors/day  error cost ₹  total ₹
manual (today)                 120       600        0.00             0      600
assisted: review each           39       197        0.67         1,333    1,530
straight through                 9        47        6.67        13,333   13,380
```

![Two panels, 88% straight-through against 19% silently wrong, above a cost table: manual 600 rupees a day, assisted 1,530, straight through 13,380](figures/fig58-2-two-rates.svg)

*Figure 58.2 — The second panel is the one missing from most business cases.*

**Read the last column, not the second.** Straight-through processing saves the most labour and costs the most money, because 19% of unattended orders are wrong and a wrong order costs far more than the minutes it would have taken to check it.

The table has two more surprises, and both deserve numbers rather than adjectives. When would straight through win? And why does assisted cost more than typing?

```python
labour = {"manual": manual_minutes / 60 * COST_PER_HOUR,
          "assisted": assisted_minutes / 60 * COST_PER_HOUR,
          "straight": auto_minutes / 60 * COST_PER_HOUR}
saved = labour["assisted"] - labour["straight"]       # labour straight through saves over assisted
extra_errors_per_rate = EMAILS_PER_DAY * straight_through * REVIEW_CATCH_RATE
break_even_rate = saved / (extra_errors_per_rate * COST_OF_A_WRONG_ORDER)
break_even_cost = saved / (unattended_errors * REVIEW_CATCH_RATE)
print(f"labour straight through saves over assisted: ₹{saved:.0f} a day")
print(f"it wins only below a silent error rate of {break_even_rate:.2%} "
      f"(one order in {1 / break_even_rate:.0f})")
print(f"or, at today's {error_rate:.0%}, if an error costs under ₹{break_even_cost:.0f}")

assisted_total = labour["assisted"] + assisted_errors * COST_OF_A_WRONG_ORDER
catch_needed = 1 - ((labour["manual"] - labour["assisted"])
                    / (unattended_errors * COST_OF_A_WRONG_ORDER))
typing_errors = (assisted_total - labour["manual"]) / COST_OF_A_WRONG_ORDER
print(f"\nassisted beats error-free typing only if the reviewer catches over {catch_needed:.0%}")
print(f"or if typing itself gets more than {typing_errors / EMAILS_PER_DAY:.1%} of orders wrong")
```

```
labour straight through saves over assisted: ₹150 a day
it wins only below a silent error rate of 0.24% (one order in 424)
or, at today's 19%, if an error costs under ₹25

assisted beats error-free typing only if the reviewer catches over 97%
or if typing itself gets more than 1.2% of orders wrong
```

**Line by line:**

- Straight through and assisted differ in two ways: straight through saves `saved` rupees of review a day, and it lets through the errors a reviewer would have caught, `EMAILS_PER_DAY × straight_through × error rate × REVIEW_CATCH_RATE` of them. It wins when the second, priced at ₹2,000, is smaller than the first. `break_even_rate` solves that for the error rate, and `break_even_cost` solves it for the cost of an error at today's rate.
- `catch_needed` solves "assisted costs the same as typing" for the catch rate, with typing assumed perfect. `typing_errors` asks the other way round: how many typing mistakes a day would make assisted the cheaper option at a 90% catch rate.

**Straight-through processing is out by a factor of about 80**: it needs about one wrong order in 400, or an error that costs about as much as a cup of tea, and this pipeline is at one in five. Better prompts will not close a gap that size, which is why the real lever is the one in the next paragraph.

**Assisted intake beats typing only if review is sharp.** The table assumes typing is perfect, and it isn't: Chapter 1 (section 1.7) warned that "50 bottles becomes 500", and Chapter 3 listed wrong quantities and wrong codes as the price of re-keying. Nobody at Riverstone has measured either the coordinator's typing error rate or a reviewer's catch rate, so **the recommendation this chapter's numbers force** is: never straight through at 19%; move to assisted intake, starting in shadow mode to measure both numbers; and design the review screen to push the catch rate up, because that is where the money is. Assisted intake saves about 80 minutes of typing a day, turns most silent errors into caught ones, and keeps the coordinator in the loop who will notice when the model starts behaving oddly.

**Straight-through processing becomes right when one of two things changes:** the extraction gets good enough that the silent error rate falls to about one order in 400, which extraction accuracy alone will almost never reach, or **the cost of an error falls because something downstream catches it** (a warehouse check, or a confirmation email to the customer listing the lines). The second is the real lever. **Both are worth engineering, and neither is a better prompt.**

> **Watch out: most automation business cases omit three costs.** The exception queue (somebody works it, every day), the review and audit time (somebody samples the automatic ones), and the build and maintenance cost (this pipeline is a system that needs a version, tests, and an owner). Add those three and a lot of "80% cost reduction" slides become "30%", which is still excellent and is a number that survives contact with the finance team.

---

## 58.8 Rolling it out

Four stages, with a gate between each. Riverstone is at stage 1, assisted, and moves to stage 2 only for a measured segment, once a fresh-data check passes.

| Stage | What runs | What a person does | Gate to the next stage |
|---|---|---|---|
| **0. Shadow** | the pipeline processes every email and writes nothing | works normally, unaware | the proposed orders match what the coordinator typed, on a week of real email; the typing error rate is measured on the way |
| **1. Assisted** | the pipeline drafts every order | reviews and accepts each one | review takes under a minute, the correction rate is stable, and the catch rate is measured (for example, by a weekly sample re-checked by a second person) |
| **2. Assisted with auto-load** | orders in a proven segment load automatically | reviews the rest | **the silent error rate on auto-loaded orders is measured and acceptable** |
| **3. Straight through** | almost everything loads | samples, and works the queue | months of stable numbers, a downstream check, and an owner who watches |

**The gate to stage 3 is the one this chapter's data fails by a wide margin**, and the failure is not a reason to stop: assisted intake already takes most of the typing away. It is a reason to be specific about what would change the answer. Three things would:

- **Better extraction**, measured on the golden set. On its own it would have to reach about one wrong order in 400, so treat it as the slow lever.
- **A downstream check** that catches a wrong order before it ships: a confirmation email to the customer listing the lines, which costs little and turns a silent error into a loud one.
- **A narrower automatic class**: the orders from a segment where accuracy is near perfect. You might expect that to be the customers who send a tidy table. Measure it. **Automate the strong segment fully rather than everything partially**, which is the single most useful tactic in this chapter.

To measure by segment, first sort each email into a style. A small function does it with text rules:

```python
import re

def style(text):
    if "|" in text:
        return "table"
    if re.search(r"^- ", text, re.MULTILINE):
        return "bullets"
    if "Forwarded message" in text:
        return "forwarded"
    if "would like to order" in text:
        return "prose"
    return "terse"

for name in ("email_008", "email_004", "email_001", "email_003", "email_010"):
    print(name, style(emails[name]))
```

```
email_008 table
email_004 bullets
email_001 forwarded
email_003 prose
email_010 terse
```

- `"|" in text` finds the column bars of a table typed in an email.
- `re.search(r"^- ", text, re.MULTILINE)` looks for a line that starts with a dash and a space, a bullet. `re.MULTILINE` makes `^` match at the start of *every* line, not just the first (Chapter 55, section 55.2).
- **The order of the checks matters.** The function returns at the first match, so a forwarded email that contains a bulleted list counts as `bullets`, and one with a table counts as `table`. Any order is a choice; this one puts the layout of the items first, because that is what the extraction struggles with.
- Anything that matches none of the four is `terse`: a line such as "PO-12345: 101 x 20".

Now load every email, with a limit so high that nothing waits for approval, and score each style:

```python
styles = {name: style(text) for name, text in emails.items()}
erp.rebuild()
run(emails, approval_limit=10 ** 9)          # nothing waits, so every style is scored
connection = erp.connect()

right, wrong_by_style = Counter(), Counter()
for row in connection.execute("SELECT * FROM orders").fetchall():
    email_style = styles[row["source_email"]]
    if is_correct(connection, row, truth):
        right[email_style] += 1
    else:
        wrong_by_style[email_style] += 1

print(f"{'email style':<12}{'loaded':>8}{'correct':>9}{'wrong':>7}   automate?")
for name in ("table", "bullets", "forwarded", "prose", "terse"):
    total = right[name] + wrong_by_style[name]
    verdict = "candidate" if total and not wrong_by_style[name] else "no: review these"
    print(f"{name:<12}{total:>8}{right[name]:>9}{wrong_by_style[name]:>7}   {verdict}")
```

```
email style   loaded  correct  wrong   automate?
table             11        7      4   no: review these
bullets           13       13      0   candidate
forwarded         14       14      0   candidate
prose             11        3      8   no: review these
terse             10       10      0   candidate
```

- `styles` is a dictionary comprehension (Chapter 17): the style of every email, looked up by name.
- `10 ** 9` is ten to the power nine, a billion rupees. With a limit that high, every validated order loads, so every style is scored on all its emails.
- The loop reuses `is_correct` from section 58.5 instead of copying its comparison a second time: one definition, used everywhere, as Chapter 29 recommended. Each order adds 1 to the right or the wrong count for its style.
- A style is a `candidate` only if it loaded something and got none of it wrong.

![Five bars by email style: bulleted, forwarded and terse are entirely correct, tables are 7 right and 4 wrong, prose is 3 right and 8 wrong](figures/fig58-3-segments.svg)

*Figure 58.3 — Three styles, 62% of the volume, had no errors in this set: the candidates for automatic loading.*

**That is the case for segmenting, and it is not where anyone would have guessed.** Bulleted, forwarded, and terse emails were extracted perfectly: 37 of 37 correct. The failures are concentrated in **prose** (3 of 11 right) and, surprisingly, in **tables** (7 of 11), where several items on one row are the exact weakness Chapter 54 measured.

So the automatic class is not "tidy emails" but "bulleted, forwarded, and terse", which together are **62% of the volume, with 0 errors in 37 so far**, and the rest stays assisted. **Zero errors in 37 is encouraging, not proof.** When you have seen 0 failures in *n* tries, the upper end of a 95% confidence interval (Chapter 22) for the true failure rate is about 3 ÷ *n*: the **rule of three**. With 37 cases, the true error rate could still be as high as 3 ÷ 37, about 8%, far above the one in 400 that section 58.7 asked for. And the segments were chosen by looking at the same 60 emails they are scored on. So before automating, score the rule on a fresh fortnight of real emails it was not chosen on, and keep the weekly sample running after.

The general rule: **find the segment where you are already good enough, automate it completely, and leave the rest with a person**, rather than averaging your accuracy across both and being mediocre at everything. And note how you find that segment: by measuring, because the intuition that prose is hard and tables are easy is half wrong here.

---

## 58.9 The people part

Automating a task changes somebody's job, and pretending otherwise is both unkind and a good way to have your project quietly sabotaged.

**What actually happens at Riverstone.** The coordinator who typed forty orders a day now reviews forty drafts in about forty minutes, works the exception queue, and spends the rest of the day on things that were always being squeezed out: chasing the orders that never arrived, calling customers whose emails are consistently unreadable, and checking that the ones the system passed actually shipped. Her job got more interesting and more responsible, and she is now the person who notices when the model starts behaving oddly, which is a role the system needs. It is the job Meera Iyer was hired into in Chapter 1, sales coordinator, which is one reason Meera is the right person to run this pilot: she knows the desk.

**How to run the conversation:**

- **Talk to her before you build**, not after. She knows which emails are awkward, which customers resend, and which "rules" finance wrote down but nobody follows. Every one of those is a requirement you would otherwise discover in production.
- **Be honest about the direction.** If the intent is eventually to need fewer people, say so, with a timeframe. People discover it anyway, and discovering it late poisons everything.
- **Make her the owner of the queue and the quality sample.** That is real authority over the system, not a consolation.
- **Measure her time, not her output.** "Orders processed" rewards rubber-stamping. "Corrections caught" and "queue cleared" reward the behavior you want.
- **Expect the first weeks to *feel* slower.** Reviewing drafts while learning to trust them is tiring, and the saving is smaller than promised until the review screen is right. Say so in advance, or the pilot looks like a failure in week two.

> **Watch out: the person reviewing the queue is your best sensor, and the easiest one to break.** Give them forty items with unhelpful reasons and they will start accepting everything within a week, and your quality metric becomes a fiction. A short queue with clear reasons is not a nicety; it is what keeps the measurement real.

---

## 58.10 When not to automate

| Situation | Why not | Do instead |
|---|---|---|
| The process is broken | Automation makes bad outputs faster | Fix the process; it may then need no automation |
| Twice a month | Build cost never repays | A checklist, or a better template |
| Every case is judgment | There is no rule to encode | Give the person better information (Chapters 13, 16) |
| Silent, expensive errors | Exactly this chapter's finding | Assisted mode, or automate a narrow segment |
| The integration is the hard part | The model was never the problem | Fix the integration first; the model can wait |
| Nobody will own it | It decays, unobserved | Find an owner or don't build it |
| The input could be structured instead | A form beats extraction, every time | Ask the five biggest customers for a template or a portal |

That last row deserves emphasis, because it is the cheapest win in the chapter and the one engineers dislike. **If two customers send 40% of your orders, a shared spreadsheet template removes the extraction problem entirely for 40% of the volume**, at the cost of one phone call each. Riverstone's real program is: templates for the top customers, assisted intake for everyone else, and automatic loading only for the segment where accuracy is proven. Nothing in that sentence is a model decision.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| No idempotency key | Re-reading an email (a retry, a replay) writes a second order | A UNIQUE constraint on the source identifier, in the database |
| No business key | A customer's resent PO becomes two orders | UNIQUE on (customer, PO number); a clash goes to the queue |
| Application-level duplicate checks | Races create duplicates under load | Let the database enforce it |
| Writes without transactions | Orders with missing lines that look complete | One transaction per logical write |
| Money in a floating-point column | Totals that are off by a paisa | Whole paise as INTEGER, or NUMERIC |
| No audit log | "Who approved this?" has no answer | Source, action, actor, detail, run and time, on every step |
| "The model proposed it" as accountability | Nobody is responsible | The pipeline version is the actor; a person's name when they approved |
| Quoting straight-through rate alone | 88% sounds like success; 19% of it is wrong | Report the silent error rate beside it, always |
| ROI without the queue and review time | The business case disappoints in month two | Count every human minute the new process needs |
| ROI without the cost of being wrong | The most expensive option looks cheapest | Price an error and multiply |
| Assuming review catches everything | Assisted mode looks error-free on paper | Put a catch rate in the model, and measure it |
| Automating everything at 80% accuracy | Mediocre across the board | Automate the segment where you are excellent |
| Trusting 0 errors in a small sample | The "perfect" segment fails in month one | The rule of three; score it again on fresh data |
| Guessing a foreign key | Orders against products that don't exist | Never invent a reference; reject to a person |
| A queue with unreadable reasons | Reviewers rubber-stamp within a week | Reasons in words, one screen, short queue |
| No batch-level circuit breaker | Sixty wrong orders instead of zero | Stop the run when the failure rate crosses a threshold |
| Surprising the person whose job changes | Quiet resistance, and requirements you never learn | Talk first, be honest, give them the queue |
| Extraction where a form would do | Solving a problem you could have removed | Templates and portals for the biggest senders |

---

## In the real world: the week the pilot was nearly cancelled

Riverstone's PO intake goes live in assisted mode in November. (The runs in this chapter replay a March morning of practice emails; the pilot itself ran on live email.) In week two, Anita Rao, the Sales Head, wants it switched off.

Her complaint is specific: the coordinator is slower than she was. She processed forty orders a day by typing; now she reviews forty drafts and it feels slower, not faster, because she is checking every field against the email.

Meera does two things. First, she measures rather than argues: review time is averaging 95 seconds in week one and 62 seconds in week two, against three minutes to type from scratch. It is already faster and still improving as trust builds. Second, she looks at *why* the reviews are slow, and finds that the coordinator is re-checking the customer name and PO number on every order, because early in week one two PO numbers were wrong, both in prose emails that quoted an earlier PO in a reply chain.

That is the useful finding. Those two fields are **extracted with near-perfect accuracy**, measured on the golden set, where all 60 customer names and PO numbers were right. So the review screen changes: the fields with proven accuracy are shown in grey as confirmed, the ones that vary (the lines and quantities) are highlighted for checking, and emails that mention more than one PO number are routed to the queue automatically. Review time drops to 41 seconds.

By January the numbers are: 40 emails a day, 41 seconds of review each, about 27 minutes of coordinator time against two hours before, every order seen by a person before it reaches the ERP, and an exception queue averaging five emails. The straight-through question comes back in March, and the answer is the segment version: once a fresh fortnight of email confirms the result, bulleted, forwarded and terse emails load automatically, and tables and prose stay assisted.

**What Meera tells Anita:** *"It was slower in week one because she was checking things we had already proven were right. We've made the screen show her what actually needs checking. It's now under half an hour a day instead of two hours, and nothing reaches the ERP that a person hasn't seen."*

**The lesson is that the interface is part of the automation.** The model's accuracy was never the constraint in week two; the reviewer's uncertainty was, and that was fixed with layout and a routing rule.

---

## Project: the intake pipeline, end to end

**Goal:** an automation that writes to a system of record safely, and a business case that would survive a finance review.

### Tools you'll need

Checked in September 2026:

- **Python** and **sqlite3** from the standard library: the whole order book, transactions and audit log in this chapter.
- **Real systems of record**: PostgreSQL or the ERP's own API. The rules are identical: uniqueness constraints, a transaction, an audit table.
- **Workflow and orchestration**: Airflow, Dagster, Prefect, Temporal (Chapter 46). A daily intake run is a scheduled job with a queue in front of it.
- **Queue and review interfaces**: a simple internal web page, a shared spreadsheet, or a workflow tool such as Camunda or a low-code form. **The interface matters more than the tool**, as the story above shows.
- **RPA**, where there is no API: UiPath, Automation Anywhere, Power Automate. Treat as a bridge with an expiry date.
- **Document intake** for photographed POs: a cloud document API, or a vision model (Chapter 54's multimodal section), feeding the same validation and queue.
- **Companion files** in `companion/ch58`: `erp.py` (the SQLite order book: schema, keys, and the audit log) and `intake.py` (validation, `decide`, `write`, and `run` with its circuit breaker). They use `companion/ch54` and `companion/ch57`.

**Steps:**

1. **Build the target table** with a uniqueness constraint on your source identifier, a business key, and an audit table beside it.
2. **Assemble the pipeline**: read, extract, parse tolerantly, validate, decide, write in a transaction, log.
3. **Replay your whole input twice** and prove nothing is written twice.
4. **Measure both numbers**: straight-through rate and silent error rate, against ground truth.
5. **Sweep the approval threshold** and record what each level costs in review time and permits in wrong orders.
6. **Price it**: manual, assisted, and straight through, including queue time, review time, a review catch rate, and the cost of an error.
7. **Design the queue screen**: email beside proposal, reasons in words, accept/correct/reject.
8. **Find your good segment**, quantify how much of the volume it covers, and say how sure you are.
9. **Write the rollout plan** with the gate for each stage.
10. **Write the runbook**: what happens when the provider is down, when the ERP rejects a write, and when the failure rate crosses the batch threshold.

**Deliverables:** the pipeline, the replay proof, the two rates, the cost table, the queue design, the segment analysis, and the rollout plan.

**Stretch goals:**

- Add a confirmation email to the customer listing the lines, and argue how that changes the straight-through gate.
- Add a second source (a photographed PO) routed through the same validation and queue.
- Write a test that proves the circuit breaker stops a bad batch.
- Build the reviewer screen and time yourself reviewing twenty orders.
- Model the ROI at 4× the volume, and find where the queue becomes a full-time job.

---

## Recap

- **Three generations**: macros and RPA (a bridge), integration (the durable answer), and model-assisted (for unstructured input). Riverstone needs the third feeding the second.
- **Choose by volume, variability, rules, and the cost of an error.** Purchase orders score well on three and badly on the fourth.
- **Writing is different from reading.** Every automated write needs an **idempotency key in the database**, a **business key** for resent documents, a **transaction**, and an **audit log** naming the run and the pipeline version.
- **Two gates**: validation holds malformed output, and an **approval threshold** holds large output. Price the threshold: raise it only while the review it saves is worth more than the errors it lets through.
- **Classify exceptions**, and give the batch a circuit breaker: sixty wrong orders is worse than none.
- **Report both rates.** Riverstone's pipeline is **88% straight through and 19% silently wrong**, which are the same system described two ways.
- **Honest ROI** counts the queue, the review, a realistic catch rate, the build, and the errors. On Riverstone's numbers, manual costs ₹600 a day, assisted about ₹1,530, and straight through **₹13,380**, because unattended errors dominate everything. Assisted beats typing only if review is sharp, which is why the review screen matters.
- **Roll out in stages**: shadow, assisted, assisted with auto-load, straight through, with a measured gate at each.
- **Automate the segment you are excellent at.** Bulleted, forwarded and terse emails were extracted perfectly (37 of 37, 62% of volume) and are the candidates for automatic loading, once fresh data confirms it; tables and prose stay assisted.
- **The interface is part of the automation**, and the person reviewing the queue is your best sensor. Do not break them with a long queue and bad reasons.

---

## Key terms

intelligent automation · RPA · screen scraping · API integration · model-assisted intake · straight-through processing · silent error rate · system of record · idempotency · idempotency key · business key · unique constraint · transaction · rollback · placeholder · audit log · actor · pipeline version · run ID · human in the loop · assisted mode · approval threshold · review catch rate · exception queue · correction rate · exception taxonomy · transient failure · malformed input · unknown reference · batch circuit breaker · touch time · ROI · cost of an error · break-even · segmentation · rule of three · shadow rollout · gate · reviewer interface · confirmation loop · process redesign · structured input (templates and portals)

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] I can tell RPA, integration, and model-assisted automation apart and pick the right one.
- [ ] I rank candidates by volume × time, then filter by the cost of an error.
- [ ] Every automated write has a uniqueness key, a transaction, and an audit row.
- [ ] I can replay an entire day's input and prove nothing doubles.
- [ ] I report the silent error rate beside the straight-through rate.
- [ ] My approval threshold is chosen from money, not from habit.
- [ ] I classify exceptions, and each class has a defined action.
- [ ] My ROI arithmetic includes the queue, the review, a catch rate, the build, and the cost of being wrong.
- [ ] I roll out in stages with a gate at each, and I know which gate I am at.
- [ ] I automate the segment I am excellent at rather than everything I am mediocre at, and I know how sure I am that it is excellent.
- [ ] I talk to the person whose job changes before I build.

---

## Exercises

Work in `companion/ch58`, in the chapter's notebook: the answers use names the chapter's cells made (`emails`, `truth`, `run`, `is_correct`, and the cost constants).

### Warm-up

1. Rebuild the ERP, run the intake, and query the three tables. How many rows are in each, and why is the audit table the largest?
2. Run the intake twice without rebuilding. What changes in `orders`, and what changes in `audit_log`?
3. Find the largest order the pipeline loaded automatically, and the smallest it sent for approval. Is the boundary where you expected?
4. What is in the queue after one run, by status? Which validation reasons appear among the held emails, and how many of each?

### Core

5. Set the approval limit to ₹25,000 and to ₹5,00,000. Report straight-through rate, approvals, and the wrong value that would have been auto-loaded at each.
6. Remove `UNIQUE` from `source_email` in `erp.py`'s schema, rebuild, and replay the morning. What happens, and why? Then remove the `UNIQUE (customer, po_number)` line too and replay again. Put both back.
7. Make `write` fail halfway through an order's lines (give the second item a product code that isn't in `PRICES`, such as `"999"`), and prove the transaction rolls back the header too.
8. Compute the silent error rate separately for each email style (table, prose, forwarded, bullets, terse). Which segment would you automate?
9. Redo the ROI table with a cost of error of ₹500 and of ₹8,000. At what cost of error does straight-through processing become the cheapest option?
10. Add a rule that any email mentioning more than one PO number goes to the queue. How many does it catch?

### Stretch

11. Add a `confirmations` table and generate a customer confirmation email listing the lines. Argue, with numbers, how it changes the straight-through gate.
12. Write a pytest test (Chapter 29) for the circuit breaker: feed `run` a batch that starts with twelve out-of-office replies, and assert that it raises `BatchAborted` and writes no order.
13. Add an `approvals` table recording who approved each pending order and when, and produce the audit query a compliance officer would ask for.
14. Write the reviewer screen as a small HTML page showing the email beside the proposed order with the uncertain fields highlighted.

### Think about it (no code needed)

15. Your pipeline is 95% straight through and 3% silently wrong. Would you ship it? What would you need to know first?
16. The ERP team offers you an API that is slower but validates everything server-side. Do you take it?
17. Finance asks why the coordinator is still needed if the system is 88% automatic. What do you say?
18. Which parts of this chapter would change if the automation *sent money* rather than created an order?

---

## Answers

**1.**

```python
erp.rebuild()
run(emails)
connection = erp.connect()
for table in ("orders", "order_lines", "audit_log"):
    count = connection.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"]
    print(f"{table:<12}{count:>5}")
```

```
orders         59
order_lines    97
audit_log     120
```

The table name goes into the SQL with an f-string here, which is safe only because the three names are a fixed list in the code: placeholders can stand for values, not for table names. The audit table is the largest because **every email produces at least two audit rows, whether or not it produces an order**: a `proposed` entry for all sixty, then `loaded`, `awaiting_approval` or `held`. That ratio is healthy. An audit log the same size as the orders table means you are only recording successes, which is exactly the half you will not need during an incident.

**2.** `orders` and `order_lines` do not change at all; `audit_log` grows by a `proposed` row for every email, a `duplicate_ignored` row for every email that was written (59), and a second `held` row for the one that wasn't. That is the behavior to test for in CI: **run the pipeline twice in the test and assert the order count is unchanged**, because idempotency is the property most likely to be broken by a well-meaning refactor.

**3.**

```python
connection = erp.connect()
for status, direction in (("loaded", "DESC"), ("awaiting_approval", "ASC")):
    row = connection.execute(
        "SELECT po_number, customer, order_value_paise FROM orders WHERE status = ? "
        f"ORDER BY order_value_paise {direction} LIMIT 1", (status,)).fetchone()
    rupees = row["order_value_paise"] / 100
    print(f"{status:<18} {row['po_number']} {row['customer']:<20} ₹{rupees:>9,.0f}")
```

```
loaded             PO-92544 Green Leaf Hotels    ₹   89,150
awaiting_approval  PO-51316 Sunrise Caterers     ₹  100,500
```

The largest automatic order is ₹89,150; the smallest one sent for approval is ₹1,00,500, just over the limit. `DESC` sorts from largest down and `ASC` from smallest up; they go in with the f-string because, like table names, they can't be placeholders. The question to ask next is whether ₹1,00,000 is where the *risk* changes, and it usually isn't: risk tracks the customer, the product, and how unusual the order is, which is the argument for a richer rule (exercise 10) once the simple one is working.

**4.**

```python
erp.rebuild()
result = run(emails)
print("queue by status:", dict(Counter(item["status"] for item in result["queue"])))
held_reasons = Counter(item["reason"] for item in result["queue"] if item["status"] == "held")
for reason, count in held_reasons.most_common():
    print(f"  held {count:>2}  {reason}")
```

```
queue by status: {'awaiting_approval': 6, 'held': 1}
  held  1  no items
```

Most items in this queue are there for **value**, not for a defect, which is a healthy queue. A queue dominated by one validation reason is a signal to fix that reason in the pipeline rather than to hire another reviewer: the correction rate per reason (section 58.5) is the metric that tells you which one to fix first.

**5.**

```python
def wrong_value(limit):
    erp.rebuild()
    counts = run(emails, approval_limit=limit)["counts"]
    connection = erp.connect()
    loaded_rows = connection.execute("SELECT * FROM orders WHERE status = 'loaded'").fetchall()
    bad = sum(row["order_value_paise"] for row in loaded_rows
              if not is_correct(connection, row, truth)) / 100
    return counts.get("loaded", 0), counts.get("awaiting_approval", 0), bad

for limit in (25_000, 100_000, 500_000):
    loaded_count, approvals, bad = wrong_value(limit)
    print(f"limit ₹{limit:>7,}: straight through {loaded_count / len(emails):.0%}, "
          f"approvals {approvals:>2}, wrong value auto-loaded ₹{bad:>9,.0f}")
```

```
limit ₹ 25,000: straight through 27%, approvals 43, wrong value auto-loaded ₹   57,950
limit ₹100,000: straight through 88%, approvals  6, wrong value auto-loaded ₹  363,550
limit ₹500,000: straight through 98%, approvals  0, wrong value auto-loaded ₹  579,050
```

The wrong value auto-loaded rises steeply from the ₹25,000 limit to ₹1,00,000 (about six-fold) and then flattens (about 1.6 times more at ₹5,00,000), because most wrong orders are mid-sized. These figures are per run of the 60 emails, about a day and a half of volume; for a week, multiply by about 3.3. **That is the number to take to the business**, because "how much incorrectly-recorded order value are we willing to create per week?" is a question a finance director can answer and "what confidence threshold should we use?" is not.

**6.** With only the `source_email` rule removed, the replay still writes nothing and still reports 59 ignored duplicates, but for a weaker reason: the `(customer, po_number)` key refuses each insert, and `write`'s lookup then finds the same email already in the table. The protection now rests on the model extracting the same PO number twice. A new model version that read one PO number differently on the replay would write a second order, which is why the idempotency key belongs on the input itself. With both rules removed, the replay writes a second copy of every order, and the audit log shows `loaded` twice for the same email. The `duplicate_ignored` branch never fires, because it is triggered by the database refusing the insert (`sqlite3.IntegrityError`); with no UNIQUE constraint there is no refusal. The exercise is worth doing once, because seeing 118 orders where 59 belong is more persuasive than any explanation of why the constraint belongs in the database rather than in the application.

**7.**

```python
erp.rebuild()
connection = erp.connect()
bad_order = {"po_number": "PO-99999", "customer": "Test Customer", "delivery_date": "2026-03-10",
             "items": [{"product_code": "101", "quantity": 5},
                       {"product_code": "999", "quantity": 5}]}
try:
    write(connection, "2026-03-02T06:00:00", "test_email", bad_order, "loaded", "")
except KeyError as error:
    print("write failed on product code", error)
for table in ("orders", "order_lines"):
    print(table, connection.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"])
```

```
write failed on product code '999'
orders 0
order_lines 0
```

`bad_order` is a dictionary shaped like an extracted order, with a bad code on its second item. `erp.PRICES["999"]` raises `KeyError` while the second line is being written, after the header and the first line are already inserted. The error leaves the `with connection:` block, so the whole transaction rolls back: no header, no lines, and the email stays unprocessed, ready to retry. (`write` catches only `IntegrityError`, so the `KeyError` reaches the caller.) Without the transaction you would have an order with a header and one of its two lines, which is the failure that ships short and is discovered by a customer. In the real pipeline validation stops an unknown code before `write`; **test the rollback deliberately anyway**, because it is the one failure mode that never happens during development and always happens eventually.

**8.** Section 58.8 does this: bulleted, forwarded, and terse emails are 37 of 37 correct; prose is 3 of 11 and tables 7 of 11. Automate the first three, which is 62% of the volume, and keep the rest assisted, after checking the rule on fresh email. The reason tables fail is Chapter 54's: several items on one row, where the extraction takes the first and misses the rest. **That is also a fixable engineering task**, so the segment that is automatic should grow over time and the analysis should be rerun each quarter.

**9.**

```python
for cost in (500, 8_000):
    totals = {
        "manual": labour["manual"],
        "assisted": labour["assisted"] + assisted_errors * cost,
        "straight through": labour["straight"] + unattended_errors * cost,
    }
    listing = ", ".join(f"{name} ₹{total:,.0f}" for name, total in totals.items())
    print(f"₹{cost:>5,} an error: {listing}")
beats_assisted = (labour["assisted"] - labour["straight"]) / (unattended_errors - assisted_errors)
beats_typing = (labour["manual"] - labour["straight"]) / unattended_errors
print(f"straight through beats assisted below ₹{beats_assisted:.0f} an error, "
      f"and typing below ₹{beats_typing:.0f}")
```

```
₹  500 an error: manual ₹600, assisted ₹530, straight through ₹3,380
₹8,000 an error: manual ₹600, assisted ₹5,530, straight through ₹53,380
straight through beats assisted below ₹25 an error, and typing below ₹83
```

At ₹500 an error, straight through costs about ₹3,380 a day, far above the other two, and assisted (₹530) now beats typing, because the errors a reviewer misses are cheap. At ₹8,000 the gap becomes absurd, and typing wins. Straight through has to beat both: it beats assisted only below about ₹25 an error and typing below about ₹83, so it becomes the cheapest option only when an error costs under about ₹25. (`unattended_errors - assisted_errors` is the errors a reviewer would catch: the only ones that separate the two designs.) **The lever is the cost of an error, not the prompt**: nothing that costs ₹25 to put right exists in order intake unless something downstream catches the error first, which is exercise 11.

**10.**

```python
multi_po = [name for name, text in emails.items() if len(set(re.findall(r"PO-\d+", text))) > 1]
print(f"emails naming more than one PO number: {len(multi_po)}")
print("emails that mention a PO number twice:",
      sum(len(re.findall(r"PO-\d+", text)) > 1 for text in emails.values()))
```

```
emails naming more than one PO number: 0
emails that mention a PO number twice: 15
```

`re.findall` returns every match; `set(...)` removes repeats, so the rule counts **distinct** PO numbers. That matters: many emails mention their PO twice, in the subject line and the body, and counting matches would send all of them to the queue for nothing. In this set the rule catches nothing, because no practice email quotes two different POs. It is insurance against a pattern the golden set does not yet contain but real email does: a reply chain that quotes an earlier order, where the extraction can take the wrong PO number (the story in this chapter met two in its first week). **A cheap textual rule that routes a known-hard case to a person is worth more than a prompt change**, because it is deterministic, testable, and it cannot regress when the model changes.

**11.** The confirmation turns a silent error into a loud one: the customer reads the lines and replies when they are wrong, usually within a day and always before dispatch. That changes the cost of an error from a wrong delivery (₹2,000, plus goodwill) to an email exchange. But run the numbers before celebrating: even at ₹200 an error, straight through on everything costs about 47 + 6.67 × 200 ≈ ₹1,380 a day, still more than typing. The confirmation alone is not enough at 19% silent errors. Combine it with the segment rule: only bulleted, forwarded and terse emails load automatically (0 errors in 37 so far), and the confirmation catches what the sample missed. Then the expected error cost on the automatic segment is small, and the reviewer's time goes on the tables and prose, where the errors are. **The cheapest way to make automation safe is often to add a check outside your system**, and this one also improves the customer's experience.

**12.** The test builds the batch as section 58.6 did, runs it inside `with pytest.raises(BatchAborted):`, which passes only if that error is raised, then opens the database and asserts `SELECT COUNT(*) FROM orders` is 0. The subtlety worth getting right in the design, and worth a second test: **abort rather than pause**, and make the run resumable, so that when the cause is fixed the same emails are reprocessed from the start with idempotency protecting anything already written. A test that runs the batch twice after a fix, and asserts no order is doubled, proves both properties at once.

**13.** The compliance query is the one to design for: *"for order 4471, show me what was proposed, by which pipeline version, what was written, who approved it, and when."* A single join across `audit_log` and `approvals`, keyed on the source identifier, answers it. Two design points: store the approver's identity from your authentication system rather than a typed name, and never allow an approval row to be deleted, only superseded.

**14.** The layout is the lesson, not the code: the email on the left, the proposed order on the right, fields with proven accuracy shown in grey as confirmed, uncertain fields highlighted, and three buttons (accept, correct, reject). The real-world story in this chapter is entirely about this screen: review time fell from 95 seconds to 41 because the reviewer stopped checking fields that were already known to be right.

**15.** Not at Riverstone's cost of an error. At 40 emails a day, 95% straight through and 3% silently wrong is 40 × 0.95 × 0.03 ≈ 1.1 wrong orders a day, and at ₹2,000 each that is about ₹2,280 a day, far more than typing (₹600) or assisted intake. It becomes a yes only if the answers to three questions change the arithmetic. **What does one of those errors cost?** 3% of a low-value flow with a cheap fix can be fine. **Is there a downstream check** that catches errors before they matter? **Who samples the automatic ones, how often, and what happens when the rate moves?** If all three have good answers, ship it to the segment where it is strongest and keep the rest assisted. If nobody will own the sampling, do not ship it: an unmonitored 3% becomes an unknown 10% within a year.

**16.** Take it, almost always. Server-side validation means the ERP rejects what it cannot accept, which converts a class of silent errors into loud ones at the moment of writing, and it is a contract you do not have to maintain. Latency rarely matters for a batch intake, and if it does, parallelize. The only reason to decline is if "slower" means minutes per record at a volume that makes the run impossible, and even then the right conversation is with the ERP team, not a workaround.

**17.** *"It isn't 88% automatic in the sense you mean: 19% of the orders it would load on its own are wrong, and each one costs us about ₹2,000 to put right. So she reviews every draft, in well under a minute each, works the queue, and approves the large orders. Her time on the task has gone from two hours a day to under half an hour, and that half hour is the part that protects us from shipping the wrong thing."* If the real question is whether headcount can fall, answer it directly with the measured time saved and let the business decide, rather than letting the question live unasked.

**18.** Almost everything gets stricter. **Approval thresholds fall to near zero**, because the cost of an error is immediate and often unrecoverable. **Two-person authorization** becomes standard above small amounts. **Idempotency stops being a nicety** and becomes the property that prevents paying twice, and it must survive crashes, not just retries. The **audit trail becomes a legal record** with retention requirements. Reconciliation against the bank becomes a daily control, not a monthly one. And **you almost certainly do not let a model decide the amount**: it can read the invoice, and a rule, a match against a purchase order, and a person decide whether to pay it. The general principle: as the cost and irreversibility of an action rise, the model's role shrinks to reading, and the decision moves to rules and people.

---

## Where this leads

- **Chapter 59, Industry Case Studies,** puts this pipeline beside eight other end-to-end projects.
- **Chapter 57, LLMOps,** keeps the extraction honest once this is running daily.
- **Chapter 46, Pipelines & Orchestration,** schedules the intake run and the queue reminders.
- **Chapters 12 and 28, SQL,** are where the transaction, the constraints, and the audit table come from.
- **Chapter 63, Automation Architecture & Governance,** decides which automations to build across the business, using this pipeline's 19% as its worked example.
- **Chapter 64, Security, Privacy, Governance & Responsible AI,** covers accountability for an automated decision and what customers must be told.
- **Chapter 3, How a Business Runs on Data,** is where the order-to-cash process this automates was first explained; reread it with this chapter in mind.
- **Chapter 78, Automation & Integration Question Bank,** has the interview versions: processing the same event twice safely (Q78-012), an automation that fails silently (Q78-018), and automating a broken process (Q78-023).
