p='/home/claude/book/ch12-databases-and-sql-foundations.md'; s=open(p).read()
def rep(old,new):
    global s
    assert s.count(old)==1, (s.count(old), old[:100]); s=s.replace(old,new)

# ---- At a glance
rep("> **You will learn to:** explain what a database is and why businesses use one · read a table's structure (columns, data types, keys) ·",
    "> **You will learn to:** explain what a database is and why businesses use one · read a table's structure (columns, data types, keys) and an entity-relationship diagram ·")
rep("· rebuild a real monthly report in SQL.", "· answer real business questions (inactive customers, discount leakage, overdue payments, sales performance) step by step · rebuild a real monthly report in SQL.")
rep("> **Time needed:** 12–15 hours of reading and practice, spread over two to three weeks.", "> **Time needed:** 15–18 hours of reading and practice, spread over three weeks.")

# ---- Data types real-life
rep("When a report looks wrong, a mis-typed column is one of the first things to check.",
"""When a report looks wrong, a mis-typed column is one of the first things to check.

> **Real-life example: phone numbers are text, not numbers.** A mobile number looks numeric, but store it as `INTEGER` and trouble follows. The leading zero in `022 2345 6789` disappears, `+91` can't be stored at all, and nobody will ever add two phone numbers together. PIN codes, GST numbers, employee codes like `EMP-0042`, and bank account numbers are the same. **Rule of thumb: if you would never do arithmetic on it, store it as text.**""")

# ---- Primary keys real-life
rep("That's why nearly every business system you'll meet (ERP, CRM, billing) gives every customer, product, invoice, and employee an ID.",
"""That's why nearly every business system you'll meet (ERP, CRM, billing) gives every customer, product, invoice, and employee an ID.

> **Real-life example: keys you already use.** A train ticket's PNR number, an invoice number, a courier tracking number, your employee ID, a car's registration number: each identifies exactly one thing. When a customer-care agent asks for your *order number* instead of your name, they're asking for a primary key, because there may be a hundred customers called Rahul Sharma but only one order 5001.

A good primary key has three properties: it's **unique**, it's **never empty**, and it **never changes**. That's why a mobile number is a poor customer key even though it's usually unique: people change numbers, families share one, and some customers have two.

Sometimes no single column is unique, but a combination is. In a school attendance register, *student* alone repeats every day and *date* repeats for every student, but *student + date* identifies exactly one attendance mark. A key made of several columns is called a **composite key**.""")

# ---- Foreign keys real-life
rep("It's the customer number written on the order card.",
    "It's the customer number written on the order card. A restaurant bill that says *Table 7* works the same way: the bill doesn't describe the table, it *points* to it.")

# ---- Relationships
rep("""- **One-to-one:** one employee has one payroll record.
- **Many-to-many:** one order contains many products, and one product appears in many orders. A database handles this with a **bridge table** (also called a *junction* or *linking* table). At Riverstone, `order_items` is the bridge between `orders` and `products`.""",
"""- **One-to-one:** one employee has one payroll record; one passport belongs to one person.
- **Many-to-many:** one order contains many products, and one product appears in many orders. A database handles this with a **bridge table** (also called a *junction* or *linking* table). At Riverstone, `order_items` is the bridge between `orders` and `products`.

Many-to-many relationships are everywhere once you look for them, and they're always solved the same way, with a table in the middle:

| Many… | …to many | Bridge table | One row of the bridge means |
|---|---|---|---|
| Students | Courses | `enrolments` | this student takes this course |
| Doctors | Patients | `appointments` | this doctor sees this patient at this time |
| Movies | Actors | `cast_members` | this actor plays this role in this movie |
| Orders | Products | `order_items` | this order includes this product, in this quantity |

Notice that the bridge table usually carries facts of its own: the appointment time, the actor's role, the quantity ordered. Those facts belong to the *pair*, not to either side alone.""")
rep("That stitching is called a **join**, and it's the most important skill in this chapter (section 12.9).",
    "That stitching is called a **join**, and it's the most important skill in this chapter (section 12.10).")

# ---- 12.2 intro
rep("Throughout this book you'll work with the data of **Riverstone Supplies**, a *fictional* company that sells storage boxes, kitchenware, and industrial crates to shops, hotels, and wholesalers across India. (Every name in it is invented.)",
    "Throughout this book you'll work with the data of **Riverstone Supplies**, a *fictional* company that sells storage boxes, kitchenware, and industrial crates to shops, hotels, and wholesalers across India. Like any real business, it takes orders, bills its customers, and chases payments. (Every name and number in it is invented.)")

# ---- schema figure
a=s.index("A **schema** is the blueprint of a database: which tables exist, their columns, and how they link.")
b=s.index("### The data")
s=s[:a]+"""A **schema** is the blueprint of a database: which tables exist, their columns, and how they link. Riverstone's mini database has seven tables.

![The Riverstone schema: seven tables linked by keys](figures/fig12-1-riverstone-schema.svg)

*Figure 12.1 — The Riverstone schema, drawn as an entity-relationship diagram.*

### How to read a schema diagram

Diagrams like Figure 12.1 are called **entity-relationship (ER) diagrams**. Every data team uses them, and you'll be handed one in your first week of almost any data job. Reading one takes three steps:

1. **Each box is a table.** Its name is in the blue header. The rows underneath are its columns, with each column's data type on the right.
2. **Find the keys.** The `PK` badge marks the table's primary key. `FK` badges mark foreign keys: columns that hold another table's primary key.
3. **Follow the lines.** Each line connects a primary key to a foreign key that points at it. The `1` sits next to the table with *one* matching row; the `N` sits next to the table that can have *many*. The dashed line from `employees` back to itself means an employee's manager is also an employee.

Now read the diagram out loud as sentences. If a sentence sounds wrong for the business, the design is probably wrong:

| Line in the diagram | Read it as | What it means in real life |
|---|---|---|
| `customers` → `orders` | one customer, many orders | Sharma Hardware has placed three orders |
| `employees` → `orders` (sales_rep_id) | one employee, many orders | Neha Kulkarni handles several orders |
| `orders` → `order_items` | one order, many lines | order 5001 contains two different products |
| `products` → `order_items` | one product, many lines | the Water Bottle appears in five orders |
| `orders` → `invoices` | one order, (usually) one invoice | each shipped order is billed |
| `invoices` → `payments` | one invoice, many payments | Coastal Foods paid invoice 9002 in two parts |
| `employees` → `employees` (manager_id) | one manager, many team members | Vikram Singh manages Neha and Rahul |

> **Why is orders → invoices drawn as one-to-many?** Today every order gets exactly one invoice. But businesses sometimes split an invoice (part-shipments) or re-issue one after a correction. Designing for "one or more" costs nothing now and avoids rebuilding the database later. Good database design plans for how the business really works, not just the usual case.

### One real order, spread across five tables

The diagram is abstract. Figure 12.2 makes it concrete. On the left is order 5001 the way Sharma Hardware's purchasing manager sees it: a single order slip. On the right is where each piece of that slip actually lives in the database.

![Order 5001 as a slip and as rows in five tables](figures/fig12-2-one-order-many-tables.svg)

*Figure 12.2 — One order slip, five tables. Each colored band on the slip is stored in the table of the same color.*

Three things to notice:

1. **Nothing is typed twice.** The slip shows the customer's name, but the `orders` row stores only `customer_id = 1`. The name lives once, in `customers`. If Sharma Hardware renames itself, every past and future order shows the new name automatically.
2. **The slip is a join.** Rebuilding it means combining five tables on their keys. By section 12.10 you'll write that query yourself.
3. **Calculated values aren't stored.** The line values (₹9,000 and ₹5,700) and the total (₹14,700) appear nowhere in the tables. They're calculated from quantity, price, and discount whenever someone asks. A stored total is a second copy of the truth that can drift out of date, for example when someone corrects a discount but forgets the total. (Invoices are the one deliberate exception: a tax invoice is a legal document, so `invoices.amount` records exactly what was billed.)

"""+s[b:]

# ---- data dumps: products + invoices + payments
rep("""**products**

```
 product_id |    product_name    |  category  | unit_price
------------+--------------------+------------+------------
        101 | Storage Box 10L    | Storage    |     450.00
        102 | Storage Box 25L    | Storage    |     780.00
        103 | Water Bottle 1L    | Kitchen    |     120.00
        104 | Food Container Set | Kitchen    |     650.00
        105 | Industrial Crate   | Industrial |    1450.00
        106 | Garden Chair       | Furniture  |    1200.00
```""","""**products**

```
 product_id |    product_name    |  category  | unit_price | unit_cost
------------+--------------------+------------+------------+-----------
        101 | Storage Box 10L    | Storage    |     450.00 |    300.00
        102 | Storage Box 25L    | Storage    |     780.00 |    540.00
        103 | Water Bottle 1L    | Kitchen    |     120.00 |     70.00
        104 | Food Container Set | Kitchen    |     650.00 |    430.00
        105 | Industrial Crate   | Industrial |    1450.00 |   1100.00
        106 | Garden Chair       | Furniture  |    1200.00 |    850.00
```""")
rep("""            19 |     5012 |        103 |       80 |     120.00 |         5.00
```

A few details are planted on purpose, because real data always has them:""","""            19 |     5012 |        103 |       80 |     120.00 |         5.00
```

**invoices**

```
 invoice_id | order_id | invoice_date |  due_date  |  amount
------------+----------+--------------+------------+----------
       9001 |     5001 | 2026-01-06   | 2026-02-05 | 14700.00
       9002 |     5002 | 2026-01-10   | 2026-02-09 | 73260.00
       9003 |     5003 | 2026-01-15   | 2026-02-14 | 16250.00
       9004 |     5005 | 2026-02-03   | 2026-03-05 | 14550.00
       9005 |     5006 | 2026-02-07   | 2026-03-09 | 14640.00
       9006 |     5007 | 2026-02-12   | 2026-03-14 | 32625.00
       9007 |     5008 | 2026-02-20   | 2026-03-22 | 23325.00
       9008 |     5009 | 2026-02-26   | 2026-03-28 | 76560.00
       9009 |     5010 | 2026-03-04   | 2026-04-03 | 20100.00
       9010 |     5011 | 2026-03-11   | 2026-04-10 | 11700.00
```

**payments**

```
 payment_id | invoice_id | payment_date |  amount  |    method
------------+------------+--------------+----------+---------------
          1 |       9001 | 2026-02-02   | 14700.00 | Bank transfer
          2 |       9002 | 2026-02-05   | 40000.00 | Bank transfer
          3 |       9002 | 2026-03-02   | 33260.00 | Bank transfer
          4 |       9003 | 2026-02-20   | 10000.00 | UPI
          5 |       9004 | 2026-03-01   | 14550.00 | Cheque
          6 |       9005 | 2026-03-05   |  7000.00 | UPI
          7 |       9005 | 2026-03-12   |  7640.00 | UPI
          8 |       9006 | 2026-03-10   | 20000.00 | Bank transfer
          9 |       9008 | 2026-03-20   | 30000.00 | Bank transfer
         10 |       9009 | 2026-03-25   | 20100.00 | UPI
```

A few details are planted on purpose, because real data always has them:""")
rep("- `order_items` stores the **price actually charged** at the time of sale, separately from today's list price in `products`. Prices change; history shouldn't.",
"""- `order_items` stores the **price actually charged** at the time of sale, separately from today's list price in `products`. Prices change; history shouldn't.
- `products.unit_cost` is the standard cost of making each product, so you can calculate **profit**, not just revenue.
- Invoices are raised when an order ships (the amount is net of discount; tax is left out to keep the numbers simple). **Customers often pay in parts:** invoices 9002 and 9005 were paid in two instalments, 9003, 9006, and 9008 are only partly paid, and 9007 and 9010 haven't been paid at all.
- Throughout the chapter, "today" is **31 March 2026**, the end of the quarter.""")

# ---- WHERE real-life example (before 12.6)
rep("""## 12.6 NULL: the value that isn't there""","""### Real-life example: which products barely make money?

Riverstone's finance manager asks: *"Which products earn less than 30% gross margin at list price?"* **Gross margin** is the share of the selling price left after paying for the product: (price − cost) ÷ price.

```sql
SELECT product_name,
       unit_price,
       unit_cost,
       ROUND(100.0 * (unit_price - unit_cost) / unit_price, 1) AS margin_pct
FROM products
WHERE (unit_price - unit_cost) / unit_price < 0.30
ORDER BY margin_pct;
```

```
   product_name   | unit_price | unit_cost | margin_pct
------------------+------------+-----------+------------
 Industrial Crate |    1450.00 |   1100.00 |       24.1
 Garden Chair     |    1200.00 |    850.00 |       29.2
(2 rows)
```

How it works, line by line:

- **`SELECT … margin_pct`** calculates the margin for display, as a percentage rounded to one decimal. Multiplying by `100.0` rather than `100` keeps the maths in decimals.
- **`WHERE (unit_price - unit_cost) / unit_price < 0.30`** filters on a *calculation*, not a stored column. `WHERE` can test any expression.
- Notice the `WHERE` repeats the formula instead of writing `WHERE margin_pct < 30`. That's not laziness: the alias `margin_pct` doesn't exist yet when `WHERE` runs. Section 12.11 explains why.
- **`ORDER BY margin_pct`** puts the weakest product first, and `ORDER BY` *can* use the alias.

Check one row by hand: the crate sells for ₹1,450 and costs ₹1,100, leaving ₹350, and 350 ÷ 1,450 = 24.1%. ✓ Keep this result in mind. In section 12.9 you'll find that the Industrial Crate is also Riverstone's biggest seller, which makes its thin margin a much bigger story.

## 12.6 NULL: the value that isn't there""")

# ---- NULL real-life
rep("""### Replacing NULLs with COALESCE""","""> **Real-life example: unknown is not zero.** Imagine a blank "discount" box on an order form. It could mean *no discount was given*, or *nobody wrote the discount down*. Those are different facts, and a database keeps them apart: `0` means none; `NULL` means unknown. Riverstone's order 5008 has no sales rep. That doesn't mean nobody sold it; it means the record is incomplete. A report that silently drops it loses ₹23,325 of revenue (you'll meet that exact trap in exercise 6).

> **Try it.** Find the order with the missing sales rep: `SELECT order_id FROM orders WHERE sales_rep_id IS NULL;` You should get order 5008. Now try `= NULL` instead and watch it return nothing.

### Replacing NULLs with COALESCE""")

# ---- CASE real-life
rep("""### Working with dates""","""### Real-life example: which invoices are overdue?

Every business that sells on credit asks this weekly. Finance wants each invoice labelled by how late it is as of 31 March 2026:

```sql
SELECT invoice_id,
       due_date,
       CASE
           WHEN due_date >= DATE '2026-03-31'             THEN 'Not yet due'
           WHEN DATE '2026-03-31' - due_date <= 30         THEN 'Overdue 1-30 days'
           WHEN DATE '2026-03-31' - due_date <= 60         THEN 'Overdue 31-60 days'
           ELSE 'Overdue 60+ days'
       END AS due_status
FROM invoices
ORDER BY due_date;
```

```
 invoice_id |  due_date  |     due_status
------------+------------+--------------------
       9001 | 2026-02-05 | Overdue 31-60 days
       9002 | 2026-02-09 | Overdue 31-60 days
       9003 | 2026-02-14 | Overdue 31-60 days
       9004 | 2026-03-05 | Overdue 1-30 days
       9005 | 2026-03-09 | Overdue 1-30 days
       9006 | 2026-03-14 | Overdue 1-30 days
       9007 | 2026-03-22 | Overdue 1-30 days
       9008 | 2026-03-28 | Overdue 1-30 days
       9009 | 2026-04-03 | Not yet due
       9010 | 2026-04-10 | Not yet due
(10 rows)
```

How it works:

- **`DATE '2026-03-31'`** writes a fixed date directly into the query. Subtracting two dates gives the number of days between them. In a live report you'd use `CURRENT_DATE` (today) instead; a fixed date is used here so your results match the book.
- The `WHEN` conditions are checked **top to bottom**. An invoice 45 days late fails the first two tests and matches the third. Because the first match wins, each condition only has to handle what the earlier ones didn't.
- Grouping amounts into bands like 1–30, 31–60, and 60+ days is called **ageing**, and an ageing report is one of the most common reports in finance.

Now look closely at invoice 9001: *Overdue 31-60 days*. But Sharma Hardware paid it in full on 2 February. **This query is wrong for the business**, even though the SQL is perfect. It knows due dates but not payments. A real overdue report must also look at the `payments` table, and building it properly is the main event of section 12.15. It's a lesson worth learning early: **a technically correct query can still give the wrong business answer if it ignores data that changes the answer.**

### Working with dates""")

# ---- GROUP BY real-life (after hand check sentence)
rep("""**Always hand-check at least one row of any new calculation.** It takes a minute and catches most logic errors.""","""**Always hand-check at least one row of any new calculation.** It takes a minute and catches most logic errors.

### Real-life example: revenue is not profit

Sales teams love revenue. Owners care about profit. With `unit_cost` you can show both, by category, for all non-cancelled orders:

```sql
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue,
       ROUND(SUM(oi.quantity * p.unit_cost), 0)                                  AS product_cost,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost), 0)                                  AS gross_profit,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost)
             / SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 1) AS margin_pct
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY net_revenue DESC;
```

```
  category  | net_revenue | product_cost | gross_profit | margin_pct
------------+-------------+--------------+--------------+------------
 Industrial |      161385 |       137500 |        23885 |       14.8
 Storage    |       81810 |        57900 |        23910 |       29.2
 Kitchen    |       80735 |        52650 |        28085 |       34.8
(3 rows)
```

This query uses joins, which section 12.10 covers in detail; for now, read `JOIN … ON` as "bring in the matching rows from that table". Here's what each part does:

- **`net_revenue`** is the money actually charged: quantity × price charged × (1 − discount).
- **`product_cost`** is quantity × the product's cost. Cost comes from `products`, which is why that table is joined in.
- **`gross_profit`** is revenue minus cost, summed across every line in the category.
- **`margin_pct`** divides total profit by total revenue. Notice it divides two *sums*. Averaging each line's margin would give a different, misleading number, because a ₹50 line would count as much as a ₹50,000 one.

Now read it as a manager would. **Industrial crates bring in half of all revenue (₹161,385 of ₹323,930) but earn the lowest margin, 14.8%.** Kitchen products bring in the least revenue but the most profit. The earlier margin query showed that crates are thin even at list price (24.1%); the 10–12% discounts on crate orders cut that almost in half. A sales team rewarded on revenue will keep pushing discounted crates. This one query can start a real conversation about pricing and incentives, which is exactly what analysis is for.

> **Simplification note.** `unit_cost` here is today's standard cost. Real costs change over time, and serious profit reporting stores the cost at the time of sale, just as `order_items` stores the price at the time of sale. Chapter 23 covers how businesses define metrics like margin.""")

# ---- LEFT JOIN figure (after two things notice list)
rep("""2. The choice between `INNER` and `LEFT` is a **business decision**, not a technical one.""","""2. The choice between `INNER` and `LEFT` is a **business decision**, not a technical one.""")
rep("""### The anti-join: finding what's missing""","""Figure 12.3 shows both joins side by side on three customers.

![Inner join versus left join, row by row](figures/fig12-3-inner-vs-left-join.svg)

*Figure 12.3 — The same match, two results. An inner join keeps only matched rows; a left join also keeps unmatched left rows and fills the gaps with NULL.*

> **Real-life example: the attendance register.** HR has an `employees` list and a `leave_requests` table. "Show leave taken by each employee" with an inner join lists only people who took leave. Anyone with zero days vanishes, and the report can't answer "who hasn't taken a day off all year?", which is often the question HR actually cares about. Whenever the business question contains *every*, *all*, or *including those with none*, reach for a left join.

### The anti-join: finding what's missing""")

# ---- fan-out with money
rep("""The fan-out trap is far nastier with `SUM`. Suppose an `orders` table carried a shipping charge per order. Join it to `order_items` and sum the shipping, and every order with three lines has its shipping counted three times. There's no `SUM(DISTINCT ...)` rescue there, since two orders can have the same charge. The real fix is to aggregate each table to the right level *before* joining. That uses subqueries (section 12.12) and CTEs (Chapter 13).""",
"""### The same trap with money

Counting too many orders is embarrassing. Counting money twice can be expensive. Finance asks a simple question: *how much have we invoiced, how much has been paid, and how much is still owed?* Joining invoices to their payments seems natural:

```sql
SELECT SUM(i.amount)                   AS total_invoiced,
       SUM(p.amount)                   AS total_paid,
       SUM(i.amount) - SUM(p.amount)   AS outstanding
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id;
```

```
 total_invoiced | total_paid | outstanding
----------------+------------+-------------
      385610.00 |  197250.00 |   188360.00
(1 row)
```

The real total invoiced is ₹297,710 (just `SELECT SUM(amount) FROM invoices`). This query says ₹385,610, and it nearly **doubles** the amount owed to ₹188,360. A collections team chasing that number would be chasing money customers have already paid. To see why, look at the joined rows for three invoices:

```sql
SELECT i.invoice_id, i.amount AS invoice_amount, p.payment_id, p.amount AS payment_amount
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE i.invoice_id IN (9001, 9002, 9007)
ORDER BY i.invoice_id, p.payment_id;
```

```
 invoice_id | invoice_amount | payment_id | payment_amount
------------+----------------+------------+----------------
       9001 |       14700.00 |          1 |       14700.00
       9002 |       73260.00 |          2 |       40000.00
       9002 |       73260.00 |          3 |       33260.00
       9007 |       23325.00 |            |
(4 rows)
```

Invoice 9002 was paid in two parts, so the join produced **two rows, each carrying the full invoice amount of ₹73,260**. Summing that column counts the invoice twice. The same happens to invoice 9005. Payments aren't affected, because each payment appears once: payments are the finest grain in the join.

![Fan-out: joining before adding up](figures/fig12-4-fan-out.svg)

*Figure 12.4 — The fix is to bring payments to the invoice's grain (one row per invoice) before joining.*

The fix: **add up payments per invoice first**, in a subquery, and join that one-row-per-invoice result:

```sql
SELECT SUM(i.amount)                        AS total_invoiced,
       SUM(COALESCE(p.paid, 0))             AS total_paid,
       SUM(i.amount - COALESCE(p.paid, 0))  AS outstanding
FROM invoices AS i
LEFT JOIN (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
) AS p ON i.invoice_id = p.invoice_id;
```

```
 total_invoiced | total_paid | outstanding
----------------+------------+-------------
      297710.00 |  197250.00 |   100460.00
(1 row)
```

How it works:

- The subquery in parentheses runs first and returns **one row per invoice** with its total paid. (Subqueries get a full section in 12.12.)
- The left join now matches each invoice to at most one row, so nothing is repeated.
- `COALESCE(p.paid, 0)` turns "no payments" (NULL) into zero, so unpaid invoices still count in full. Without it, `i.amount - NULL` would be NULL and those invoices would silently drop out of `outstanding`.
- **Reconcile:** ₹297,710 invoiced minus ₹197,250 paid is ₹100,460. The totals now agree with each table summed on its own. ✓

There's no `SUM(DISTINCT ...)` shortcut here, by the way. `SUM(DISTINCT i.amount)` would add each *different amount* once, so two separate invoices that happened to be for the same amount would be counted as one. The only reliable fix is to aggregate to the right grain before joining. Chapter 13 shows a tidier way to write these steps, using CTEs.""")

# ---- execution order figure
rep("""This order explains:""","""![Written order versus the order the database runs a query](figures/fig12-5-execution-order.svg)

*Figure 12.5 — You write SELECT first, but the database gets to it fifth.*

This order explains:""")

# ---- correlated subquery real life
rep("""> **Watch out: NOT IN and NULLs.**""","""**A correlated subquery with a real use.** *For each invoice, show the most recent payment.* It's the kind of thing a collections team asks daily: *when did we last hear from this customer?*

```sql
SELECT p.invoice_id, p.payment_date, p.amount
FROM payments AS p
WHERE p.payment_date = (
    SELECT MAX(p2.payment_date)
    FROM payments AS p2
    WHERE p2.invoice_id = p.invoice_id
)
ORDER BY p.invoice_id;
```

```
 invoice_id | payment_date |  amount
------------+--------------+----------
       9001 | 2026-02-02   | 14700.00
       9002 | 2026-03-02   | 33260.00
       9003 | 2026-02-20   | 10000.00
       9004 | 2026-03-01   | 14550.00
       9005 | 2026-03-12   |  7640.00
       9006 | 2026-03-10   | 20000.00
       9008 | 2026-03-20   | 30000.00
       9009 | 2026-03-25   | 20100.00
(8 rows)
```

Read it as: *keep a payment if its date equals the latest payment date for the same invoice.* The inner query uses `p.invoice_id` from the outer row, so for payment 2 it finds the latest date among invoice 9002's payments (2 March), and payment 2 (5 February) is dropped. The table uses two aliases, `p` and `p2`, for the same `payments` table, just like the self-join. Invoices 9007 and 9010 don't appear because they have no payments at all. "Latest record per group" is such a common need that Chapter 13 gives it a cleaner tool, `ROW_NUMBER()`.

> **Watch out: NOT IN and NULLs.**""")

# ---- New section 12.15
rep("""## Common mistakes and how to spot them""","""## 12.15 Putting it all together: Monday morning with the sales head

It's Monday, 31 March 2026, the last day of the quarter. Before the 10 a.m. review, Anita Rao, Riverstone's Sales Head, sends you four questions. None of them mentions SQL. This is what real analysis work looks like, so we'll answer each one the way an experienced analyst would, with a method rather than guesswork.

### A six-step method for any business question

1. **Restate the question precisely.** What exactly is being counted? As of when? Which records are included or excluded (cancelled orders, unpaid invoices)? Write the business rules down.
2. **Decide the shape of the answer.** What does one row of the result represent: one customer, one month, one invoice? Which columns will the reader need?
3. **Find the tables.** Which tables hold each piece? What is the **grain** (one row = what?) of each?
4. **Plan the joins.** Which keys connect them? Inner or left join? Will any join multiply rows (fan-out)?
5. **Build in small steps.** Start with one table, add one join at a time, then filters, then grouping. Run the query after every step and check the row count.
6. **Check the answer.** Hand-check one row. Reconcile a total to a number you already trust. Then ask: *does this make business sense?*

### Question 1: "Which customers have gone quiet?"

**Restate.** Customers with no order in the 30 days up to 31 March 2026, meaning no order since 1 March. Cancelled orders don't count as activity. Customers who have *never* ordered must be included, because they're the easiest to miss.

**Shape.** One row per customer: name, segment, last order date, days since that order.

**Tables and joins.** `customers` and `orders`. It must be a **left join**, or never-ordered customers disappear. The "not cancelled" rule goes in the `ON` clause, for the reason you saw in section 12.10.

**Filter.** "Last order before 1 March" is a condition on `MAX(order_date)`, an aggregate, so it belongs in `HAVING`, not `WHERE`.

```sql
SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                     AS last_order_date,
       DATE '2026-03-31' - MAX(o.order_date) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2026-03-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date NULLS FIRST;
```

```
     customer_name      |   segment   | last_order_date | days_since_last_order
------------------------+-------------+-----------------+-----------------------
 Blue Bay Cafe          | Hospitality |                 |
 Patel Kitchenware      | Retail      | 2026-01-14      |                    76
 Coastal Foods          | Wholesale   | 2026-02-11      |                    48
 Sunrise Caterers       | Hospitality | 2026-02-19      |                    40
 Northgate Distributors | Wholesale   | 2026-02-25      |                    34
(5 rows)
```

**How it works.** `GROUP BY c.customer_id, …` makes one group per customer (grouping by the ID as well as the name protects against two customers sharing a name). `MAX(o.order_date)` finds each customer's latest valid order; for Blue Bay Cafe there are no matching orders, so it's NULL. `HAVING … OR MAX(o.order_date) IS NULL` keeps the never-ordered customers, because "NULL < 1 March" is unknown, not true (section 12.6). `NULLS FIRST` puts them at the top.

**Check.** Green Leaf Hotels isn't listed. Its January order was cancelled, but it ordered again on 3 March, so it's active. ✓ Sharma Hardware (10 March) and Metro Mart (15 March) are active too. ✓

**What to tell Anita.** Five of eight customers haven't ordered this month. Blue Bay Cafe signed up on 1 March and has never ordered: a warm lead to call today. Patel Kitchenware has gone 76 days, far longer than any other customer.

### Question 2: "How much are discounts costing us?"

**Restate.** For non-cancelled orders, compare what products would have sold for at the price charged before discount (the *list value*) with the discount given, by category.

**Shape.** One row per category. **Tables:** `order_items` (quantities, prices, discounts), `products` (category), `orders` (status). Every join goes from a line to its one order and one product, so nothing fans out.

```sql
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price), 0)                           AS list_value,
       ROUND(SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100), 0)   AS discount_given,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100)
             / SUM(oi.quantity * oi.unit_price), 1)                         AS discount_pct_of_list
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY discount_given DESC;
```

```
  category  | list_value | discount_given | discount_pct_of_list
------------+------------+----------------+----------------------
 Industrial |     181250 |          19865 |                 11.0
 Storage    |      85050 |           3240 |                  3.8
 Kitchen    |      82850 |           2115 |                  2.6
(3 rows)
```

**Check.** List value minus discount should equal the net revenue from section 12.9: for Industrial, 181,250 − 19,865 = 161,385. ✓

**What to tell Anita.** Riverstone gave away ₹19,865 on crates this quarter, 11% of their value, against under 4% elsewhere. Put that next to the gross profit query from section 12.9: crates earned only ₹23,885 of gross profit. **The discounts on crates were worth about 83% of the profit the crates actually made.** That's a finding worth a meeting.

### Question 3: "Who owes us money, and how late is it?"

This is the classic **receivables ageing report**, and it pulls together almost everything in this chapter.

**Restate.** As of 31 March 2026, for each customer: the total unpaid balance, split by how overdue it is (not yet due, 1–30, 31–60, 60+ days past the due date). Only invoices with money still owed.

**Shape.** One row per customer, with one column per ageing band.

**Tables and grain.** `invoices` (one row per invoice), `payments` (one row per payment, **many per invoice**), `orders` (to reach the customer), `customers` (names). The payments join would fan out, so payments must be summed per invoice first.

**Build in steps.** First, the balance for every invoice:

```sql
SELECT i.invoice_id,
       i.amount,
       COALESCE(pay.paid, 0.00)            AS paid,
       i.amount - COALESCE(pay.paid, 0.00) AS balance
FROM invoices AS i
LEFT JOIN (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
) AS pay ON i.invoice_id = pay.invoice_id
ORDER BY i.invoice_id;
```

```
 invoice_id |  amount  |   paid   | balance
------------+----------+----------+----------
       9001 | 14700.00 | 14700.00 |     0.00
       9002 | 73260.00 | 73260.00 |     0.00
       9003 | 16250.00 | 10000.00 |  6250.00
       9004 | 14550.00 | 14550.00 |     0.00
       9005 | 14640.00 | 14640.00 |     0.00
       9006 | 32625.00 | 20000.00 | 12625.00
       9007 | 23325.00 |     0.00 | 23325.00
       9008 | 76560.00 | 30000.00 | 46560.00
       9009 | 20100.00 | 20100.00 |     0.00
       9010 | 11700.00 |     0.00 | 11700.00
(10 rows)
```

Invoice 9001, which section 12.8 wrongly flagged as overdue, now correctly shows a zero balance. Next, wrap that result as a derived table, join it to orders and customers, and use conditional aggregation (section 12.9) to spread balances into ageing columns:

```sql
SELECT c.customer_name,
       SUM(inv.balance) AS total_due,
       SUM(CASE WHEN inv.due_date >= DATE '2026-03-31' THEN inv.balance ELSE 0.00 END) AS not_yet_due,
       SUM(CASE WHEN inv.due_date <  DATE '2026-03-31'
                 AND DATE '2026-03-31' - inv.due_date <= 30 THEN inv.balance ELSE 0.00 END) AS overdue_1_30,
       SUM(CASE WHEN DATE '2026-03-31' - inv.due_date BETWEEN 31 AND 60 THEN inv.balance ELSE 0.00 END) AS overdue_31_60,
       SUM(CASE WHEN DATE '2026-03-31' - inv.due_date > 60 THEN inv.balance ELSE 0.00 END) AS overdue_60_plus
FROM (
    SELECT i.invoice_id, i.order_id, i.due_date,
           i.amount - COALESCE(pay.paid, 0) AS balance
    FROM invoices AS i
    LEFT JOIN (SELECT invoice_id, SUM(amount) AS paid FROM payments GROUP BY invoice_id) AS pay
           ON i.invoice_id = pay.invoice_id
) AS inv
JOIN orders    AS o ON inv.order_id  = o.order_id
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE inv.balance > 0
GROUP BY c.customer_name
ORDER BY total_due DESC;
```

```
     customer_name      | total_due | not_yet_due | overdue_1_30 | overdue_31_60 | overdue_60_plus
------------------------+-----------+-------------+--------------+---------------+-----------------
 Northgate Distributors |  46560.00 |        0.00 |     46560.00 |          0.00 |            0.00
 Sunrise Caterers       |  23325.00 |        0.00 |     23325.00 |          0.00 |            0.00
 Coastal Foods          |  12625.00 |        0.00 |     12625.00 |          0.00 |            0.00
 Sharma Hardware        |  11700.00 |    11700.00 |         0.00 |          0.00 |            0.00
 Patel Kitchenware      |   6250.00 |        0.00 |         0.00 |       6250.00 |            0.00
(5 rows)
```

**How it works.**

- The innermost subquery totals payments per invoice (the fan-out fix). The next layer computes each invoice's `balance`. The outer query joins balances to customers and aggregates.
- `WHERE inv.balance > 0` removes fully paid invoices *before* grouping.
- Each `SUM(CASE WHEN … THEN inv.balance ELSE 0.00 END)` adds up only the balances that fall into one ageing band. Five `CASE` columns turn one list of invoices into a five-column report, the same result you'd build with a pivot table in Chapter 11.
- `ELSE 0.00` (rather than leaving out the `ELSE`) makes empty bands show zero instead of NULL, which matters when someone totals the columns in Excel.

**Check.** The `total_due` column adds up to 46,560 + 23,325 + 12,625 + 11,700 + 6,250 = ₹100,460, exactly the outstanding total from section 12.10. ✓ And each row's bands add up to its total. ✓

**What to tell Anita.** ₹88,760 is overdue, and more than half of it is Northgate Distributors (₹46,560). Northgate is *also* on the "gone quiet" list from Question 1, so before sales chases them for a new order, finance should chase the old one. Sunrise Caterers hasn't paid anything, has no city recorded, and has no sales rep assigned: a credit risk and a data-quality problem at the same time.

### Question 4: "How is each sales rep doing, and who do they report to?"

**Restate.** For each sales rep: number of orders and net revenue on non-cancelled orders, with their manager's name.

**Tables and joins.** `employees` twice (the rep, and the rep's manager, a self-join), `orders`, `order_items`. The manager join is a left join, so a rep with no manager still appears.

```sql
SELECT e.employee_name                         AS sales_rep,
       COALESCE(m.employee_name, '(none)')     AS reports_to,
       COUNT(DISTINCT o.order_id)              AS orders,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM employees AS e
LEFT JOIN employees   AS m  ON e.manager_id   = m.employee_id
JOIN      orders      AS o  ON o.sales_rep_id = e.employee_id
JOIN      order_items AS oi ON oi.order_id    = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY e.employee_name, m.employee_name
ORDER BY net_revenue DESC;
```

```
   sales_rep   |  reports_to  | orders | net_revenue
---------------+--------------+--------+-------------
 Rahul Mehta   | Vikram Singh |      4 |      146745
 Farah Khan    | Anita Rao    |      2 |       96660
 Neha Kulkarni | Vikram Singh |      4 |       57200
(3 rows)
```

**How it works.** `COUNT(DISTINCT o.order_id)` avoids the fan-out from joining to order lines. Both names are in `GROUP BY` because both appear in `SELECT`. Anita Rao and Vikram Singh don't appear as reps because they have no orders of their own; the inner join to `orders` removes them, which is what this question wants.

**Check.** The three reps total ₹300,605. Order 5008 has no rep and is worth ₹23,325. 300,605 + 23,325 = ₹323,930, exactly the total non-cancelled revenue. ✓ **Reconciling to a known total is how you prove a report hasn't lost anything.** Mention the unassigned ₹23,325 in a footnote so nobody wonders where it went.

**What to tell Anita.** Rahul Mehta leads on revenue with ₹146,745, largely from two big Coastal Foods orders. Neha Kulkarni handled as many orders but at a much smaller average size, which is worth understanding before judging performance. Ranking reps, showing each one's share of team revenue, and comparing this quarter with last all need **window functions**, the headline tool of Chapter 13.

### What just happened

Four questions, four queries, and each answer came with a number *and* a reason to act. None of the SQL was new; every piece came from sections 12.4 to 12.12. What made the difference was the method: restating the question, knowing the grain of each table, choosing joins deliberately, building in steps, and checking every result against something you already trusted. That habit, far more than syntax, is what makes an analyst trusted.

## Common mistakes and how to spot them""")

# ---- common mistakes rows
rep("""| Fan-out from joining a finer-grain table | Counts and sums too high | Ask "what is one row?"; `COUNT(DISTINCT)`; aggregate before joining |""",
"""| Fan-out from joining a finer-grain table | Counts and sums too high | Ask "what is one row?"; `COUNT(DISTINCT)`; aggregate before joining |
| Summing a parent amount after joining to child rows (invoices → payments) | Invoiced or outstanding totals inflated | Aggregate the child table per parent first, then join |
| Storing phone numbers, PIN codes, or account numbers as numbers | Leading zeros vanish; `+91` rejected | Store identifiers as text |
| Answering with only part of the relevant data (due dates without payments) | "Overdue" invoices that are already paid | Ask which other tables change the answer, and join them |
| Not reconciling totals | A report silently loses a customer or an unassigned order | Compare report totals with a simple `SUM` on the source table |""")

# ---- exercises renumbering and additions
rep("""8. What is the average net order value across non-cancelled orders?

### Stretch

9. For each customer who has ordered, show their first order date, most recent order date, and the number of days between them. Largest gap first.
10. Show net revenue by product category and each category's percentage of total net revenue (non-cancelled orders), to one decimal place.
11. Which customers' total net revenue is above the average customer's total net revenue?

### Think about it (no SQL needed)

12. A colleague's report says Riverstone had "19 orders" in Q1 2026. Where might that number have come from, and what's the right figure?
13. The business wants to know revenue by city. Sunrise Caterers has no city. Should the report drop it, show it as "Unknown", or something else? Who should decide?
14. Explain to a non-technical manager, in three sentences, why the sales report must not overwrite old prices when the price list changes.""",
"""8. What is the average net order value across non-cancelled orders?
9. Show the number of payments and total amount received by payment method, largest amount first.
10. List the invoices that haven't received any payment at all, with their amount and due date, earliest due date first.

### Stretch

11. For each customer who has ordered, show their first order date, most recent order date, and the number of days between them. Largest gap first.
12. Show net revenue by product category and each category's percentage of total net revenue (non-cancelled orders), to one decimal place.
13. Which customers' total net revenue is above the average customer's total net revenue?
14. For every invoice with money still owed, show the invoice amount, the number of payments, the amount paid, and the balance. Largest balance first.
15. Operations wants to chase stuck orders as of 31 March 2026: orders Pending for more than 7 days, or Shipped for more than 14 days (and not yet Delivered). Show the order, date, status, and days open, oldest first.

### Think about it (no SQL needed)

16. A colleague's report says Riverstone had "19 orders" in Q1 2026. Where might that number have come from, and what's the right figure?
17. The business wants to know revenue by city. Sunrise Caterers has no city. Should the report drop it, show it as "Unknown", or something else? Who should decide?
18. Explain to a non-technical manager, in three sentences, why the sales report must not overwrite old prices when the price list changes.
19. In exercise 14 you can safely join invoices to payments and use `SUM(p.amount)`, but in section 12.10 the same join gave a wrong total. What's the difference? Use invoice 9005 in your explanation.""")

# ---- key terms
rep("primary key · foreign key · referential integrity ·", "entity-relationship (ER) diagram · primary key · composite key · foreign key · referential integrity ·")
rep("· anti-join · fan-out ·", "· anti-join · fan-out · reconciliation ·")
rep("· derived table ·", "· derived table · gross margin · ageing report ·")

# ---- answers renumber: old 9,10,11 -> 11,12,13 ; old 12,13,14 -> 16,17,18
import re
for old,new in [("**14.**","**18.**"),("**13.**","**17.**"),("**12.**","**16.**"),("**11.**","**13.**"),("**10.**","**12.**"),("**9.**","**11.**")]:
    assert s.count("\n"+old)==1, old
    s=s.replace("\n"+old,"\n"+new)
# insert new answers 9,10 before 11 ; 14,15 before 16 ; 19 at end
rep("\n**11.**\n", """
**9.**

```sql
SELECT method, COUNT(*) AS payments, SUM(amount) AS amount_received
FROM payments
GROUP BY method
ORDER BY amount_received DESC;
```

```
    method     | payments | amount_received
---------------+----------+-----------------
 Bank transfer |        5 |       137960.00
 UPI           |        4 |        44740.00
 Cheque        |        1 |        14550.00
(3 rows)
```

The three amounts add up to ₹197,250, the total of the `payments` table. ✓

**10.** An anti-join from invoices to payments:

```sql
SELECT i.invoice_id, i.amount, i.due_date
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE p.payment_id IS NULL
ORDER BY i.due_date;
```

```
 invoice_id |  amount  |  due_date
------------+----------+------------
       9007 | 23325.00 | 2026-03-22
       9010 | 11700.00 | 2026-04-10
(2 rows)
```

Invoice 9007 is already overdue; 9010 isn't due until April.

**11.**
""")
rep("\n**16.** ", """
**14.**

```sql
SELECT i.invoice_id,
       i.amount,
       COUNT(p.payment_id)                   AS num_payments,
       COALESCE(SUM(p.amount), 0)            AS amount_paid,
       i.amount - COALESCE(SUM(p.amount), 0) AS balance
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
GROUP BY i.invoice_id, i.amount
HAVING i.amount - COALESCE(SUM(p.amount), 0) > 0
ORDER BY balance DESC;
```

```
 invoice_id |  amount  | num_payments | amount_paid | balance
------------+----------+--------------+-------------+----------
       9008 | 76560.00 |            1 |    30000.00 | 46560.00
       9007 | 23325.00 |            0 |           0 | 23325.00
       9006 | 32625.00 |            1 |    20000.00 | 12625.00
       9010 | 11700.00 |            0 |           0 | 11700.00
       9003 | 16250.00 |            1 |    10000.00 |  6250.00
(5 rows)
```

`COUNT(p.payment_id)` counts only real payments, so unpaid invoices show 0; `COUNT(*)` would wrongly show 1 for them, because the left join still produces one row. The balances add up to ₹100,460. ✓

**15.**

```sql
SELECT order_id,
       order_date,
       status,
       DATE '2026-03-31' - order_date AS days_open
FROM orders
WHERE (status = 'Pending' AND DATE '2026-03-31' - order_date > 7)
   OR (status = 'Shipped' AND DATE '2026-03-31' - order_date > 14)
ORDER BY days_open DESC;
```

```
 order_id | order_date | status  | days_open
----------+------------+---------+-----------
     5009 | 2026-02-25 | Shipped |        34
     5011 | 2026-03-10 | Shipped |        21
     5012 | 2026-03-15 | Pending |        16
(3 rows)
```

The parentheses matter: each status has its own day limit (section 12.5). Order 5009 has been "Shipped" for 34 days, which almost certainly means someone forgot to mark it Delivered, or it's lost. Either way, somebody should find out today.

**16.** """)
s = s.rstrip("\n") + """

**19.** In exercise 14, the query groups by invoice and uses `i.amount` only as a grouping column: it's never *summed*, so repeating it on two rows does no harm. In section 12.10, the query summed `i.amount` across the joined rows. Invoice 9005 (₹14,640) was paid in two instalments, so the join produced two rows for it, and `SUM(i.amount)` counted ₹29,280. **Repeated rows are only a problem when you add up a column from the table that got repeated.**
"""
open(p,'w').write(s)
print("ok")
