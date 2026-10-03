# Chapter 71. SQL Question Bank

*Part 8 — Be Interview Ready*

> **Chapter at a glance**
>
> **You will learn to:** answer the SQL questions that come up across screening calls, live-coding rounds, and take-home exercises for every data role · reason through the classic NULL and join traps that catch experienced candidates, not just beginners · write window-function solutions to the second-highest, top-N-per-group, running-total, streak and retention problems that recur across companies · know exactly where PostgreSQL and MySQL disagree · predict the output of a query cold, from the warm-up cases to the brain-racking ones, which is the round that cannot be talked around · walk out with a 24-question final-week revision list.
>
> **Before you start:** Chapter 69 (the three answer tiers and the twelve extra-point tags). The questions test Chapters 12 and 13 (SQL), Chapter 14 (cleaning), Chapter 27 (`NTILE`) and Chapter 28 (recursive CTEs, window frames, query plans, indexes, materialized views), plus Chapter 49, section 49.4 (ACID). This chapter tests those skills; it doesn't teach them again.
>
> **Time needed:** 4½–6 hours for a first pass (about 5 minutes per core question, 1 minute per rapid-fire row); 8–10 hours more to run every core question yourself in both databases; 1 hour for the final-week list. Section 71.11 is worth its own sitting of 1½–2 hours, answering each question out loud before reading on.
>
> **How this chapter is built.** Same format as every question bank in Part 8 (Chapters 70–82): every core question leads with a **"Remember it as…"** memory hook, a one-line answer, and a compact tier table, and every rapid-fire section is a scan table. After each question number comes its level: **Warm-up** (sections 71.1–71.3), **Core** (CTEs, window functions, the classic problems, schema and dialect questions) or **Advanced** (recursive CTEs, gaps-and-islands, window frames, transactions, indexes). Section 71.11, the predict-the-output round, deliberately runs across all three and adds a **Brain-racking** level above them, so its questions carry their own level rather than their section's. Rapid-fire tables elsewhere take the level of their section. Extra-point moves are labelled with Chapter 69's twelve tags, such as **[+Edge cases]**.
>
> **Every query is shown in PostgreSQL and was run on PostgreSQL 16.** Where MySQL needs different syntax, a *MySQL:* block follows, and that version was run on MySQL 8.4 LTS. Every result printed below is the database's real answer, kept exactly as returned, including the surprising ones (an empty result, a tied ranking, an index the planner declines to use).
>
> **Section 71.11 was verified separately, and it is worth saying what that found.** The section was added after the rest of the chapter and its outputs were first produced against the same `riverstone_2025` data on a different engine. Re-running all of it on **PostgreSQL 16.2** found three figures that were wrong, and they are corrected: Q71-081's hand-rolled average, which PostgreSQL truncates to `3` by integer division; Q71-087's `ROWS` column, where the tie order differs by engine; and a precision difference in Q71-090. Eighteen of the twenty-two query blocks matched first time. The questions marked **Dialect split** give each engine's behaviour rather than one printed result.
>
> **Which database.** Most questions use `riverstone_2025`, the one-year practice database from Chapter 13, section 13.1. Question Q71-072 uses the mini database `riverstone` from Chapter 12, section 12.2, and says so. The questions that create tables (Q71-013 and section 71.7) run in `riverstone_lab`, the practice database you created in Chapter 12, section 12.13, and drop their tables at the end. Each **Verified** line names its database.
>
> **Learn it in** pointers name the chapter and section that teaches the idea. Questions and rapid-fire rows marked ***Beyond the book*** go further than the teaching chapters; each of those carries its own short explanation.

---

<!-- db: riverstone_2025 -->

## 71.1 Core concepts: SELECT, WHERE, and JOIN

### Q71-001 · Find customers who have never placed an order · *Warm-up*

**Remember it as:** *LEFT JOIN + IS NULL, or NOT EXISTS. Never NOT IN if the other side might have a NULL.*

**The query:**
```sql
SELECT c.customer_id, c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
```

**Verified (riverstone_2025):** 1 of 24 customers has never ordered.
```
 customer_id | customer_name
-------------+---------------
          16 | Home Plus
(1 row)
```

| Tier | What to say |
|---|---|
| Passes | `WHERE customer_id NOT IN (SELECT customer_id FROM orders)`: works on clean data, has a hidden flaw (Q71-002) |
| Strong | The `LEFT JOIN ... IS NULL` version above, filtering on the *right table's primary key*, not an arbitrary column |
| Extra points | **[+Clarify]** should a customer whose only order was cancelled count as "never ordered"? · **[+Validate]** total customers = customers with orders + customers without, checked: 24 = 23 + 1 ✓ · **[+Business]** add the signup date and sort by it, so sales can follow up the newest non-converters first |

**Likely follow-ups:** No orders in the last 90 days, not ever? Products never sold? Rewrite without a join?
**Red flag:** `WHERE o.customer_id = NULL` (should be `IS NULL`); filtering a left join's right-table column in `WHERE` in a way that silently turns it into an inner join. The one deliberate exception is `IS NULL` on the right table's key: that is what makes this an anti-join (Chapter 12, section 12.10). Any other condition on the right table belongs in `ON`.
**Learn it in:** Chapter 12, section 12.10 (the anti-join).

### Q71-002 · Why is `NOT IN` dangerous with a subquery that might contain a NULL? · *Warm-up*

**Remember it as:** *One NULL in a NOT IN subquery poisons the whole comparison: the query returns nothing, silently.*

**Answer in one line:** If the subquery's result contains even one NULL, `NOT IN` returns zero rows for *every* outer row, because SQL can't prove any value is "not equal to NULL": the comparison evaluates to UNKNOWN, not TRUE, and `NOT IN` needs every comparison to be TRUE. (Q71-009 shows the root cause: `NULL = NULL` isn't true either.)

**Verified (riverstone_2025):** the `orders.sales_rep_id` column has 11 NULL rows (unassigned orders). The trap, live:

```sql
SELECT count(*)
FROM employees
WHERE employee_id NOT IN (SELECT sales_rep_id FROM orders);
```
```
 count
-------
     0
(1 row)
```

The same question, asked correctly:

```sql
SELECT count(*)
FROM employees
WHERE employee_id NOT IN (SELECT sales_rep_id
                          FROM orders
                          WHERE sales_rep_id IS NOT NULL);
```
```
 count
-------
     2
(1 row)
```

| Tier | What to say |
|---|---|
| Passes | "`NOT IN` can behave oddly with NULLs" (vague, no mechanism) |
| Strong | The UNKNOWN-comparison explanation above, with the fix (`WHERE ... IS NOT NULL` inside the subquery) |
| Extra points | **[+Validate]** the exact live numbers above: 0 rows (wrong) vs. 2 rows (right) on the same data, same question · **[+Trade-offs]** `NOT EXISTS` and `LEFT JOIN ... IS NULL` don't have this problem at all, since they test whether a matching row exists rather than comparing a value against a list that holds a NULL: prefer them by default |

**Likely follow-ups:** Does `IN` (not `NOT IN`) have the same problem? *(No: `IN` with a NULL in the list just doesn't match the NULL; it doesn't empty the whole result.)* How would you find this bug in someone else's query?
**Red flag:** not knowing this is a real, live trap, not a theoretical one: 11 real NULL rows just demonstrated it.
**Learn it in:** Chapter 12, section 12.12 (the "NOT IN and NULLs" box).

### Rapid-fire, §71.1 (Warm-up)

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q71-003 | `WHERE` vs. `HAVING`? | Filters rows before grouping / filters groups after aggregation | **[+Edge cases]** you can't reference an aggregate function in `WHERE`: that's precisely what `HAVING` is for → Ch 12 §12.9 |
| Q71-004 | INNER JOIN vs. LEFT JOIN? | Only matching rows from both tables / all left-table rows, NULLs where there's no match | **[+Business]** a LEFT JOIN that unexpectedly shrinks the row count usually means a filter on the right table leaked into `WHERE` instead of `ON` → Ch 12 §12.10 |
| Q71-005 | What does `SELECT DISTINCT` actually do? | Removes duplicate *entire rows* from the result, not duplicates in one column alone | **[+Edge cases]** `SELECT DISTINCT a, b` removes duplicates of the combination of a and b, not of each column on its own → Ch 12 §12.5 |
| Q71-006 | `UNION` vs. `UNION ALL`? | `UNION` removes duplicate rows across the combined result / `UNION ALL` keeps everything, no duplicate check (verified: 2 identical rows → 2 with `UNION ALL`, 1 with `UNION`) | **[+Scale]** `UNION ALL` is faster, since it skips the duplicate check: use it whenever you know the two sets can't overlap → Ch 12 §12.12 |
| Q71-007 | `BETWEEN`: is it inclusive or exclusive? | Inclusive on both ends | **[+Edge cases]** `BETWEEN '2025-01-01' AND '2025-01-31'` on a `TIMESTAMP` column silently misses rows on the 31st after midnight: cast to `DATE` first, or use `< '2025-02-01'` → Ch 12 §12.6; the timestamp case is *beyond the book* |
| Q71-008 | What's a correlated subquery? | A subquery that references a column from the outer query, re-evaluated once per outer row (e.g., each customer's own most recent order date) | **[+Trade-offs]** correlated subqueries can be slow at scale (one execution per row); a window function or a join often expresses the same logic faster → Ch 12 §12.12 |

---

## 71.2 Basic questions that are trickier than they look

Every one of these sounds like a warm-up question. Every one of them has caught experienced candidates, because the trap is in something they assumed rather than something they didn't know. They mix theory and practice, and each one is shown live wherever a query can demonstrate the point.

### Q71-009 · Does `NULL = NULL` evaluate to true? · *Warm-up*

**Remember it as:** *NULL isn't a value, it's the absence of one. You can't ask whether two absences are "equal."*

**Answer in one line:** No: `NULL = NULL` evaluates to `NULL` (unknown), not `TRUE`, which is exactly why `WHERE column = NULL` never matches anything and `IS NULL` exists as a separate operator.

**Verified (riverstone_2025):**
```sql
SELECT (NULL = NULL) AS result,
       (NULL = NULL) IS NULL AS is_this_null;
```
```
 result | is_this_null
--------+--------------
        | t
(1 row)
```

PostgreSQL prints NULL as a blank and true as `t`. MySQL runs the same query and prints `NULL` and `1`, since it stores true as the number 1 (Q71-066).

| Tier | What to say |
|---|---|
| Passes | "NULL equals NULL" (the actual trap, stated as fact) |
| Strong | Correctly says no, it evaluates to NULL/unknown, and explains why `= NULL` in a `WHERE` clause silently matches nothing |
| Extra points | **[+Validate]** the query above proves it two ways at once: the comparison itself shows blank (NULL), and wrapping it in `IS NULL` confirms that blank really is NULL, not empty text · **[+Business]** this is exactly the mechanism behind Q71-002's `NOT IN` trap: one root cause, two different symptoms |

**Likely follow-ups:** How do you check for NULL correctly? What does `NULL AND FALSE` evaluate to? *(FALSE: one known-false input is enough to decide an AND, even with an unknown on the other side.)*
**Red flag:** confidently stating `NULL = NULL` is true.
**Learn it in:** Chapter 12, section 12.7.

### Q71-010 · Can you use a column alias from `SELECT` inside the same query's `WHERE` clause? · *Warm-up*

**Remember it as:** *WHERE runs before SELECT ever names anything. You can't filter on a name that doesn't exist yet.*

**Answer in one line:** No: SQL's logical order runs `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY`, so a `WHERE` clause runs before `SELECT` has assigned any alias, and referencing one errors.

**Verified (riverstone_2025):**
```sql
SELECT customer_name, city AS loc
FROM customers
WHERE loc = 'Mumbai';
```
```
ERROR:  column "loc" does not exist
```

*MySQL:* the same query fails with its own wording:
```mysql
SELECT customer_name, city AS loc
FROM customers
WHERE loc = 'Mumbai';
```
```
ERROR 1054 (42S22): Unknown column 'loc' in 'where clause'
```

| Tier | What to say |
|---|---|
| Passes | "You can't use an alias in WHERE" (correct, no reason given) |
| Strong | + explains the logical order, and that this is *why* the alias doesn't exist yet at the point `WHERE` runs |
| Extra points | **[+Validate]** the real error messages above, not a guess at what they might say · **[+Edge cases]** `ORDER BY` runs *after* `SELECT`, so aliases work fine there: the same alias that errors in `WHERE` is legal in `ORDER BY`, which is worth saying out loud since it looks inconsistent until you know the order |

**Likely follow-ups:** Does `GROUP BY` allow an alias? *(Yes, in PostgreSQL and MySQL, though not in every SQL engine.)* How would you filter on a computed value if not in WHERE? *(A CTE or subquery, filtering the outer layer: the same pattern Q71-033 and Q71-035 use for window functions.)*
**Red flag:** not knowing SQL has a logical order that differs from the order it's written in.
**Learn it in:** Chapter 12, section 12.11.

### Q71-011 · Why does sorting `'9'`, `'10'`, `'2'` as text give a different order than sorting them as numbers? · *Warm-up*

**Remember it as:** *Text sorts character by character. "10" starts with "1," which comes before "2" and "9": the number itself is never considered.*

**Answer in one line:** As text, comparison goes character by character, so `'10'` sorts before `'2'` because `'1'` < `'2'` as the very first character; as numbers, ordinary numeric comparison applies and 2 < 9 < 10 as expected.

**Verified (riverstone_2025), the same three values two ways.** As text:
```sql
SELECT val
FROM (VALUES ('9'), ('10'), ('2')) AS t(val)
ORDER BY val;
```
```
 val
-----
 10
 2
 9
(3 rows)
```

As integers:
```sql
SELECT val
FROM (VALUES (9), (10), (2)) AS t(val)
ORDER BY val;
```
```
 val
-----
   2
   9
  10
(3 rows)
```

*MySQL:* a list of literal rows is written `VALUES ROW(…)`, and its column is always called `column_0`:
```mysql
SELECT column_0
FROM (VALUES ROW('9'), ROW('10'), ROW('2')) AS t
ORDER BY column_0;
```
```
+----------+
| column_0 |
+----------+
| 10       |
| 2        |
| 9        |
+----------+
```

| Tier | What to say |
|---|---|
| Passes | "Text and numbers sort differently" (true, no mechanism) |
| Strong | The character-by-character explanation above, with the real output showing both orders on the same three values |
| Extra points | **[+Business]** this bug shows up whenever a numeric code gets stored as `VARCHAR`: order numbers, SKUs, PIN codes. A report silently sorts "wrong" with no error anywhere · **[+Validate]** cast to confirm: `ORDER BY val::int` on the text version recovers the numeric order (MySQL: `ORDER BY CAST(column_0 AS SIGNED)`), which is itself proof of what was happening |

**Likely follow-ups:** How would you fix a column that's the wrong type after the fact? What about sorting mixed codes like "A10" vs "A9"?
**Red flag:** unable to explain *why* it happens, only that it does.
**Learn it in:** Chapter 12, section 12.1 (why types matter) and section 12.8 (`CAST` and `::`).

### Q71-012 · What's the difference between `DELETE`, `TRUNCATE`, and `DROP`? · *Warm-up*

**Remember it as:** *DELETE removes rows, one at a time, with a WHERE if you want. TRUNCATE empties the whole table, fast, no WHERE. DROP removes the table itself, structure and all.*

**Answer in one line:** `DELETE FROM t WHERE ...` removes matching rows (or all rows with no `WHERE`), logged row by row, and can be rolled back inside a transaction; `TRUNCATE TABLE t` empties the entire table at once, much faster, minimally logged. In MySQL it also resets `AUTO_INCREMENT`; in PostgreSQL the identity or sequence keeps counting unless you write `TRUNCATE TABLE t RESTART IDENTITY`. `DROP TABLE t` removes the table's structure entirely, data and definition both gone.

| Tier | What to say |
|---|---|
| Passes | "They all delete data" |
| Strong | The three distinct scopes and behaviors above |
| Extra points | **[+Edge cases]** `TRUNCATE` can't take a `WHERE` clause: it's all rows or nothing, by design · **[+Business]** the classic production incident is a `DELETE` whose `WHERE` got lost in a copy-paste, which empties the table. Inside `BEGIN … ROLLBACK` you can undo it. `TRUNCATE` in MySQL commits immediately, so there is no undo · **[+Trade-offs]** `DELETE` fires row-level triggers (if any exist) and can be rolled back mid-transaction; `TRUNCATE` skips row triggers, and in MySQL it can't be rolled back |

**Likely follow-ups:** Can `TRUNCATE` be rolled back? *(In PostgreSQL, yes, inside a transaction; in MySQL, no: it commits implicitly.)* Does `TRUNCATE` restart the ID counter? *(MySQL: yes. PostgreSQL: only with `RESTART IDENTITY`; checked on both.)* What happens to foreign-key-referenced rows on each?
**Red flag:** treating all three as interchangeable ways to "clear a table."
**Learn it in:** Chapter 12, section 12.13 (Step 8, transactions, and Step 11, TRUNCATE and DROP). `RESTART IDENTITY` is *beyond the book*.

### Q71-013 · Does a `UNIQUE` constraint allow more than one `NULL` value in a column? · *Warm-up*

**Remember it as:** *NULL never equals NULL (Q71-009): so a UNIQUE constraint, which is really an equality check, can't call two NULLs "duplicates" of each other.*

**Answer in one line:** Yes, in both PostgreSQL and MySQL: a `UNIQUE` constraint allows any number of `NULL` values in that column, because uniqueness is checked by equality, and no two `NULL`s are ever equal to each other.

**Verified, in `riverstone_lab`** (same statements in both databases):

<!-- lab:start -->

<!-- Verifier setup, not printed: the lab database the reader made in Chapter 12.
```sql
CREATE DATABASE riverstone_lab;
```
```mysql
CREATE DATABASE riverstone_lab;
```
-->

<!-- run: both -->
```sql
CREATE TABLE test_unique (id INT, email VARCHAR(50) UNIQUE);
INSERT INTO test_unique VALUES (1, NULL);
INSERT INTO test_unique VALUES (2, NULL);
SELECT * FROM test_unique;
```
```
 id | email
----+-------
  1 |
  2 |
(2 rows)
```

*MySQL:*

<!-- out: mysql -->
```
+------+-------+
| id   | email |
+------+-------+
|    1 | NULL  |
|    2 | NULL  |
+------+-------+
```

Both inserts succeeded: a surprising result to anyone who reads "unique" as "no duplicates, including blanks." Tidy up (same in both):

<!-- run: both -->
```sql
DROP TABLE test_unique;
```

<!-- lab:end -->

| Tier | What to say |
|---|---|
| Passes | "UNIQUE means no duplicates" (true for non-NULL values, misses the NULL exception entirely) |
| Strong | Correctly states multiple NULLs are allowed, and ties it back to `NULL = NULL` being unknown, not true |
| Extra points | **[+Validate]** the live proof above: two NULL emails, one UNIQUE constraint, zero errors · **[+Business]** this is why a "unique email" constraint alone doesn't stop two customer records both missing an email address from silently coexisting: a data-quality gap that looks like the schema should prevent it, and doesn't |

**Likely follow-ups:** How would you actually prevent multiple blank emails if that's the real requirement? *(Add `NOT NULL` alongside `UNIQUE`, or use a partial unique index. PostgreSQL 15 and later also offer `email VARCHAR(50) UNIQUE NULLS NOT DISTINCT`, which treats NULLs as equal for this one constraint, so the second NULL is rejected; checked on PostgreSQL 16.)* Does a `PRIMARY KEY` allow NULLs the same way? *(No: a primary key is `UNIQUE` plus `NOT NULL`, so it never allows even one NULL.)*
**Red flag:** confidently claiming a `UNIQUE` column can never have more than one blank value.
**Learn it in:** Chapter 12, section 12.13 (Step 3, constraints) and section 12.7 (NULL). `NULLS NOT DISTINCT` is *beyond the book*.

### Q71-014 · What happens if you self-join a table without giving it two different aliases? · *Warm-up*

**Remember it as:** *The database can't tell which "employees" you mean if you never gave it two different names to tell them apart.*

**Answer in one line:** It errors. PostgreSQL rejects the `FROM` clause itself (`table name "employees" specified more than once`); MySQL says `Not unique table/alias`. Without two aliases there's no way to say which copy each column comes from.

**Verified (riverstone_2025):**
```sql
SELECT employee_id
FROM employees
JOIN employees ON employee_id = manager_id;
```
```
ERROR:  table name "employees" specified more than once
```

*MySQL:*
```mysql
SELECT employee_id
FROM employees
JOIN employees ON employee_id = manager_id;
```
```
ERROR 1066 (42000): Not unique table/alias: 'employees'
```

| Tier | What to say |
|---|---|
| Passes | "You need aliases for a self-join" (correct, no example of what breaks without one) |
| Strong | The explanation above, plus the correctly aliased version (`FROM employees e JOIN employees m ON e.manager_id = m.employee_id`), which is exactly Chapter 12's self-join (section 12.10), and the base of Q71-029's hierarchy query |
| Extra points | **[+Validate]** the real error messages above, which are a different, earlier failure than the "ambiguous column" error a beginner might expect (and that some other engines, such as SQLite, do report): worth knowing so you recognize it instantly |

**Likely follow-ups:** Would this also happen with a regular join between two *different* tables that share a column name? *(Only for the shared column: you'd get an "ambiguous column" error on that reference, not on the table.)*
**Red flag:** not immediately recognizing that a self-join needs two aliases.
**Learn it in:** Chapter 12, section 12.10 (the self-join).

### Q71-015 · Why does `SELECT *` with a `GROUP BY` often error, even though it "looks" fine? · *Warm-up*

**Remember it as:** *GROUP BY collapses many rows into one per group. SELECT * asks for every column, including ones that could hold many different values within that one group.*

**Answer in one line:** Every non-aggregated column in `SELECT` must also appear in `GROUP BY`, because the database can't know which single value to show for a column that wasn't grouped and might differ across the rows being collapsed into one.

**Verified (riverstone_2025):**
```sql
SELECT * FROM orders GROUP BY customer_id;
```
```
ERROR:  column "orders.order_id" must appear in the GROUP BY clause or be used in an aggregate function
```

*MySQL:*
```mysql
SELECT * FROM orders GROUP BY customer_id;
```
```
ERROR 1055 (42000): Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'riverstone_2025.orders.order_id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

| Tier | What to say |
|---|---|
| Passes | "`SELECT *` doesn't work well with `GROUP BY`" (true, no reason) |
| Strong | The collapsing-rows explanation above, plus the real error naming the exact offending column |
| Extra points | **[+Edge cases]** since MySQL 5.7.5, `ONLY_FULL_GROUP_BY` is on by default, so modern MySQL errors too; very old MySQL, or a server with that mode switched off, silently picks an arbitrary row's value instead, which is far more dangerous than an error. Both engines do accept ungrouped columns that depend on a grouped primary key: `SELECT * FROM orders GROUP BY order_id` runs in both (checked) · **[+Business]** a real reason `SELECT *` is a bad habit in any query with `GROUP BY`: list only the columns you need and can justify |

**Likely follow-ups:** What SQL mode controls this behavior in MySQL? How would you fix this query to actually work?
**Red flag:** not knowing that a MySQL server with `ONLY_FULL_GROUP_BY` switched off returns a plausible-looking but unreliable answer instead of an error.
**Learn it in:** Chapter 12, section 12.9 (its dialect note on `ONLY_FULL_GROUP_BY`).

### Rapid-fire, §71.2 (Warm-up): more basic-but-tricky theory and practice

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q71-016 | Is SQL case-sensitive? | Keywords (`SELECT`, `WHERE`) are not; whether your *data* comparisons are case-sensitive depends on the column's collation, which differs by engine and setup | **[+Edge cases]** `WHERE status = 'delivered'` matches `'Delivered'` in MySQL's default collation and not in PostgreSQL: never assume either way without checking → Ch 12 §12.6 and §12.16 |
| Q71-017 | `CHAR` vs. `VARCHAR`? | `CHAR(n)` is fixed-length, padded with spaces to exactly n characters; `VARCHAR(n)` is variable-length, up to n characters, no padding | **[+Business]** `CHAR` padding can break an exact-string comparison against a value that wasn't padded the same way in another system → *Beyond the book* |
| Q71-018 | Do you need a semicolon at the end of a SQL statement? | Required to separate multiple statements in one script; often optional for a single statement in an interactive client | **[+Edge cases]** in a multi-statement script a missing semicolon usually makes the next statement a syntax error, and the error points at the wrong line, which makes it confusing to debug → Ch 12 §12.4 |
| Q71-019 | Is a `FOREIGN KEY` required for a `JOIN` to work? | No: a `JOIN` is just a condition in `ON`; it works with or without a declared foreign-key constraint | **[+Business]** a missing foreign key doesn't stop joins; it stops the database from *rejecting* orphaned data before the join ever runs: the constraint is a data-quality guard, not a join requirement → Ch 12 §12.10 and §12.13 |
| Q71-020 | Can two rows be "duplicates" if they have different primary keys? | Yes: a primary key only guarantees that column is unique; every other column can be identical across two rows | **[+Edge cases]** this is why "remove duplicates" almost always means "duplicates ignoring the ID column," which needs to be said explicitly → Ch 14 §14.4 |
| Q71-021 | Does `LIKE '%text%'` match case-sensitively? | Depends on the collation, same root cause as Q71-016; PostgreSQL offers `ILIKE` for a guaranteed case-insensitive match | **[+Edge cases]** when in doubt, wrap both sides in `LOWER()` for a comparison that ignores case under any collation → Ch 12 §12.6 |
| Q71-022 | How does an empty string (`''`) compare with `NULL`? | They are not the same thing: `'' IS NULL` is false, and `'' = NULL` is (per Q71-009) unknown, never true | **[+Edge cases]** a form that saves a blank text field as `''` instead of `NULL` will silently slip past every `IS NULL` check written to catch missing data → Ch 12 §12.7 |

---

## 71.3 Aggregation: GROUP BY and HAVING

### Q71-023 · Total quantity sold per category, only categories over 500 units · *Warm-up*

**Remember it as:** *WHERE filters rows before the grouping happens. HAVING filters groups after.*

**The query:**
```sql
SELECT p.category, SUM(oi.quantity) AS total_qty
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
HAVING SUM(oi.quantity) > 500
ORDER BY total_qty DESC;
```

**Verified (riverstone_2025):** three of the four categories pass; Furniture sold 30 units and is correctly left out.
```
  category  | total_qty
------------+-----------
 Storage    |      5350
 Kitchen    |      3675
 Industrial |       625
(3 rows)
```

| Tier | What to say |
|---|---|
| Passes | The correct `GROUP BY` + `HAVING` query, but can't explain why `WHERE` can't do the same job |
| Strong | The query above, plus the reason: `WHERE` runs before the groups exist, so there is no `SUM` yet to test |
| Extra points | **[+Validate]** run it once without `HAVING`: four categories, Furniture at 30 units, so its absence is the filter working, not a bug · **[+Business]** this shape (group, sum, filter on the sum) is the core of almost every "which segments matter" business question |

**Likely follow-ups:** Same, but only the top 2 categories regardless of a fixed threshold? Add a customer-segment breakdown too?
**Red flag:** trying to filter an aggregate in `WHERE` (`WHERE SUM(quantity) > 500` errors, because aggregates can't appear in `WHERE`).
**Learn it in:** Chapter 12, section 12.9.

### Rapid-fire, §71.3 (Warm-up)

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q71-024 | Does `COUNT(*)` differ from `COUNT(column)`? | `COUNT(*)` counts all rows / `COUNT(column)` counts only the non-NULL values in that column | **[+Edge cases]** on riverstone_2025, `COUNT(*)` on orders is 175 and `COUNT(sales_rep_id)` is 164: the 11 NULL rows are silently left out (verified) → Ch 12 §12.9 |
| Q71-025 | Can you `GROUP BY` a column not in the `SELECT` list? | Yes, in both PostgreSQL and MySQL: you can group by something you don't display | **[+Edge cases]** the reverse is stricter: every non-aggregated `SELECT` column must appear in `GROUP BY`, or the query errors (Q71-015) → Ch 12 §12.9 |
| Q71-026 | What does `GROUP BY 1, 2` mean? | Groups by the 1st and 2nd columns of the `SELECT` list, by position, not by name | **[+Trade-offs]** convenient for a long expression, but fragile: reordering the `SELECT` columns silently changes what's grouped → *Beyond the book* |
| Q71-027 | How would you count DISTINCT customers per month? | `SELECT DATE_TRUNC('month', order_date)::date AS month, COUNT(DISTINCT customer_id) FROM orders GROUP BY 1` (MySQL: `DATE_FORMAT(order_date, '%Y-%m-01')` in place of `DATE_TRUNC('month', order_date)::date`); both give 5, 8 and 10 customers for January to March 2025 | **[+Business]** distinct customers per month, not the order count, is the number that answers "is our customer base growing" → Ch 12 §12.8 (`DATE_TRUNC`) and §12.9 (`COUNT(DISTINCT …)`) |

---

## 71.4 Subqueries, CTEs, and EXISTS vs. IN

### Q71-028 · Rewrite a nested subquery as a CTE, and explain why you would · *Core*

**Remember it as:** *A CTE is a subquery with a name and a place to breathe. Same result, easier to read and debug one step at a time.*

**Answer in one line:** `WITH name AS (...) SELECT ... FROM name` names an intermediate result so it can be read top to bottom and reused, instead of nesting parentheses inside parentheses.

**The query:**
```sql
WITH monthly_revenue AS (
  SELECT DATE_TRUNC('month', o.order_date)::date AS month,
         ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS revenue
  FROM orders o
  JOIN order_items oi ON o.order_id = oi.order_id
  WHERE o.status <> 'Cancelled'
  GROUP BY 1
)
SELECT month, revenue
FROM monthly_revenue
ORDER BY month
LIMIT 3;
```

**Verified (riverstone_2025),** the first three months:
```
   month    |  revenue
------------+-----------
 2025-01-01 | 202640.00
 2025-02-01 | 253664.00
 2025-03-01 | 278007.50
(3 rows)
```

*MySQL:* replace the month line with `DATE_FORMAT(o.order_date, '%Y-%m-01') AS month`; the rest is unchanged, and it returns the same three rows.

<!-- run: mysql -->
```mysql
WITH monthly_revenue AS (
  SELECT DATE_FORMAT(o.order_date, '%Y-%m-01') AS month,
         ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS revenue
  FROM orders o
  JOIN order_items oi ON o.order_id = oi.order_id
  WHERE o.status <> 'Cancelled'
  GROUP BY 1
)
SELECT month, revenue
FROM monthly_revenue
ORDER BY month
LIMIT 3;
```

| Tier | What to say |
|---|---|
| Passes | A nested subquery achieving the same result: correct, harder to read past two levels |
| Strong | The CTE version above, one logical step at a time |
| Extra points | **[+Validate]** the three months match Chapter 13's monthly revenue (₹2,02,640, ₹2,53,664, ₹2,78,007.50) · **[+Scale]** several CTEs can chain (`WITH a AS (...), b AS (...)`), each building on the last, which is how a long query stays readable (Q71-042 uses three) |

**Likely follow-ups:** Recursive CTE: when would you need one? (Q71-029.) Does a CTE get computed once, or folded into the main query, and does that matter for performance?
**Red flag:** nesting subqueries three or four levels deep when a CTE would make the same logic readable.
**Learn it in:** Chapter 13, section 13.2.

### Q71-029 · Write a recursive CTE to show Riverstone's full management hierarchy · *Advanced*

**Remember it as:** *A recursive CTE is a loop: start with the base case (the top of the tree), then repeatedly join back to itself for the next level down.*

**The query:**
```sql
WITH RECURSIVE hierarchy AS (
  SELECT employee_id, employee_name, manager_id, 1 AS level
  FROM employees
  WHERE manager_id IS NULL                      -- anchor: the top of the tree
  UNION ALL
  SELECT e.employee_id, e.employee_name, e.manager_id, h.level + 1
  FROM employees e
  JOIN hierarchy h ON e.manager_id = h.employee_id   -- recursive step
  WHERE h.level < 20                            -- safety stop
)
SELECT employee_name, level
FROM hierarchy
ORDER BY level, employee_name;
```

**Verified (riverstone_2025; the mini database has the same five employees):**
```
 employee_name | level
---------------+-------
 Anita Rao     |     1
 Farah Khan    |     2
 Vikram Singh  |     2
 Neha Kulkarni |     3
 Rahul Mehta   |     3
(5 rows)
```
MySQL 8 runs the same query unchanged and returns the same five rows.

| Tier | What to say |
|---|---|
| Passes | Writes the recursive CTE with help, but can't name the anchor and recursive parts or the stopping condition |
| Strong | The structure above: an anchor query, `UNION ALL`, and a recursive part that joins back to the CTE itself, stopping when a level finds no new rows |
| Extra points | **[+Validate]** the output is a correct three-level tree: Anita Rao at the top, her two direct reports, and Vikram Singh's two reports below him · **[+Edge cases]** a cycle in the data (A manages B, B manages A) makes the recursion run forever. MySQL stops a runaway recursion at `cte_max_recursion_depth` (1,000 by default); PostgreSQL has no limit, so add a cap such as `WHERE h.level < 20` |

**Likely follow-ups:** Find everyone reporting up to a specific manager, at any depth? What if the hierarchy has a cycle by mistake?
**Red flag:** not knowing the anchor / recursive-part structure at all.
**Learn it in:** Chapter 28, section 28.2.

### Rapid-fire, §71.4 (Core)

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q71-030 | `EXISTS` vs. `IN`: when do they differ in behavior? | `IN` and `EXISTS` return the same rows, even with NULLs. They differ when negated: `NOT IN` returns nothing if the subquery holds a NULL (Q71-002); `NOT EXISTS` doesn't. Verified: `EXISTS` and `IN` both give 23 customers | **[+Trade-offs]** `EXISTS` can stop at the first match for each row, which is often faster on a large subquery; prefer `NOT EXISTS` to `NOT IN` by default → Ch 12 §12.12 |
| Q71-031 | What's a scalar subquery? | A subquery that returns exactly one row and one column, used anywhere a single value is expected | **[+Edge cases]** if it returns more than one row, the query errors when it runs, not when you write it → Ch 12 §12.12 |
| Q71-032 | Each customer's most recent order date, without a `GROUP BY`? | A correlated scalar subquery: `SELECT c.customer_name, (SELECT MAX(order_date) FROM orders o WHERE o.customer_id = c.customer_id) FROM customers c` | **[+Trade-offs]** correct and simple to read; a `LEFT JOIN` to a pre-aggregated subquery is usually faster on a large table, since it avoids one execution per outer row → Ch 12 §12.12 |

---

## 71.5 Window functions: the classics

### Q71-033 · Find the second-highest-priced product · *Core*

**Remember it as:** *LIMIT/OFFSET breaks on ties. DENSE_RANK doesn't.*

**The query:**
```sql
SELECT product_name, unit_price
FROM (
  SELECT product_name, unit_price,
         DENSE_RANK() OVER (ORDER BY unit_price DESC) AS rnk
  FROM products
) t
WHERE rnk = 2;
```

**Verified (riverstone_2025):**
```
 product_name | unit_price
--------------+------------
 Garden Chair |    1150.00
(1 row)
```

| Tier | What to say |
|---|---|
| Passes | `ORDER BY unit_price DESC LIMIT 1 OFFSET 1`: gives the same right answer here, and silently breaks if two products tie for first place (OFFSET 1 would then return one of the *tied firsts*, not the second-highest price) |
| Strong | The `DENSE_RANK` version above, which is safe on ties |
| Extra points | **[+Edge cases]** `RANK` vs. `DENSE_RANK` matters here: `RANK` skips a number after a tie (1, 1, 3), so `rnk = 2` could return zero rows if two products tied for first; `DENSE_RANK` (1, 1, 2) has no gap · **[+Validate]** on Riverstone's real (untied) top prices both approaches agree, which is exactly why this bug hides until the data changes |

**Likely follow-ups:** Third-highest? Second-highest *per category*, not overall? What if there's a tie for second place itself: should both show?
**Red flag:** using `LIMIT`/`OFFSET` with no acknowledgment that it breaks on ties.
**Learn it in:** Chapter 13, section 13.4. (`OFFSET` itself is *beyond the book*.)

### Q71-034 · `ROW_NUMBER`, `RANK`, and `DENSE_RANK`: demonstrate the difference on real tied data · *Core*

**Remember it as:** *ROW_NUMBER never ties (1,2,3). RANK ties and skips (1,1,3). DENSE_RANK ties and doesn't skip (1,1,2).*

**Verified (riverstone_2025), on two customers tied at 16 orders each:**

```sql
SELECT c.customer_name, COUNT(*) AS order_count,
       ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC, c.customer_name) AS rn,
       RANK()       OVER (ORDER BY COUNT(*) DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS drnk
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY order_count DESC, c.customer_name
LIMIT 4;
```
```
     customer_name      | order_count | rn | rnk | drnk
------------------------+-------------+----+-----+------
 Green Leaf Hotels      |          17 |  1 |   1 |    1
 Metro Mart             |          16 |  2 |   2 |    2
 Sharma Hardware        |          16 |  3 |   2 |    2
 Northgate Distributors |          13 |  4 |   4 |    3
(4 rows)
```

The `ORDER BY` inside `ROW_NUMBER` ends with `c.customer_name`, a **tie-breaker**: without it, which of the two tied customers gets 2 and which gets 3 is up to the database. Grouping by `c.customer_id` as well as the name keeps two customers who happen to share a name apart.

| Tier | What to say |
|---|---|
| Passes | Names all three functions, can't explain how they differ on a tie |
| Strong | Reads the table above correctly: `RANK` gives both tied customers rank 2, then *skips* to 4; `DENSE_RANK` gives them both 2, then continues at 3 with no gap |
| Extra points | **[+Validate]** this is real tied data, not a made-up example: Metro Mart and Sharma Hardware really do have 16 orders each · **[+Edge cases]** `ROW_NUMBER` on a tie is non-deterministic unless you add a tie-breaker; two runs can disagree · **[+Business]** "top 3 customers" means something different depending on which function you pick when there's a tie at the boundary: worth clarifying with whoever asked for the list |

**Likely follow-ups:** Which one would you use for "top N per group," and why? What does `NTILE` do? (Q71-039.)
**Red flag:** claiming they're interchangeable, or unable to predict what happens at a tie without running it.
**Learn it in:** Chapter 13, section 13.4.

### Q71-035 · Top 2 products by revenue, within each category · *Core*

**Remember it as:** *PARTITION BY is GROUP BY for window functions: it restarts the ranking at each group boundary instead of collapsing rows.*

**The query:**
```sql
SELECT category, product_name, revenue, rn
FROM (
  SELECT p.category, p.product_name,
         ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS revenue,
         ROW_NUMBER() OVER (
           PARTITION BY p.category
           ORDER BY SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) DESC
         ) AS rn
  FROM order_items oi
  JOIN products p ON oi.product_id = p.product_id
  JOIN orders o   ON oi.order_id = o.order_id
  WHERE o.status <> 'Cancelled'
  GROUP BY p.category, p.product_name
) t
WHERE rn <= 2
ORDER BY category, rn;
```

**Verified (riverstone_2025):**
```
  category  |    product_name    |  revenue  | rn
------------+--------------------+-----------+----
 Furniture  | Garden Chair       |  33637.50 |  1
 Industrial | Industrial Crate   | 795830.00 |  1
 Kitchen    | Lunch Box Set      | 546630.00 |  1
 Kitchen    | Food Container Set | 523745.00 |  2
 Storage    | Storage Box 25L    | 908212.50 |  1
 Storage    | Storage Box 10L    | 860946.00 |  2
(6 rows)
```

Note: **Furniture and Industrial show only one row each**, not two. That's real data, not a bug: Furniture and Industrial each have only one product in the catalogue.

| Tier | What to say |
|---|---|
| Passes | A correlated subquery per category finding the top product, then a second one for the runner-up: works, ugly, doesn't generalize past "top 2" |
| Strong | The `PARTITION BY` version above: one query, any N |
| Extra points | **[+Edge cases]** exactly this: two categories return fewer than 2 rows because they have only one product; `rn <= 2` never guarantees exactly 2 rows per group, and it's worth saying so before the result surprises someone · **[+Validate]** run the inner query on its own: 8 rows, one per product, and they add up to ₹43,35,471, Riverstone's 2025 revenue, so nothing was lost or double-counted before the ranking |

**Likely follow-ups:** Same but by revenue *share* within category, not rank? What changes using `RANK` instead of `ROW_NUMBER` here?
**Red flag:** not expecting that some groups may have fewer members than N.
**Learn it in:** Chapter 13, section 13.7 (Pattern 1, top N per group).

### Q71-036 · Month-over-month revenue change with `LAG` · *Core*

**Remember it as:** *LAG looks backward one row. LEAD looks forward one row. Both need an ORDER BY to mean anything.*

**The query:**
```sql
WITH monthly_revenue AS (
  SELECT DATE_TRUNC('month', o.order_date)::date AS month,
         ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS revenue
  FROM orders o
  JOIN order_items oi ON o.order_id = oi.order_id
  WHERE o.status <> 'Cancelled'
  GROUP BY 1
)
SELECT month, revenue,
       revenue - LAG(revenue) OVER (ORDER BY month) AS mom_change
FROM monthly_revenue
ORDER BY month
LIMIT 4;
```

**Verified (riverstone_2025),** the first four months:
```
   month    |  revenue  | mom_change
------------+-----------+------------
 2025-01-01 | 202640.00 |
 2025-02-01 | 253664.00 |   51024.00
 2025-03-01 | 278007.50 |   24343.50
 2025-04-01 | 210281.50 |  -67726.00
(4 rows)
```

*MySQL:* the same `DATE_FORMAT` swap as in Q71-028.

| Tier | What to say |
|---|---|
| Passes | A self-join on month = previous month (date arithmetic): correct, even with gaps, but verbose |
| Strong | `LAG` as above, noting that the first row's change is `NULL` because there's no earlier month, plus a note that `LAG` needs a gap-free month series: build one first (Chapter 13, section 13.8, Pattern 5, fill in the missing months), or check that `month - LAG(month)` is exactly one month |
| Extra points | **[+Validate]** the real fall in April (−₹67,726) is kept as it is, a real month-over-month decline, rather than picking a friendlier month to show · **[+Edge cases]** a month with no orders has no row at all, so without a gap-free series `LAG` silently compares with a month that isn't the previous one |

**Likely follow-ups:** `LAG` two periods back instead of one? Percentage change, not absolute? `LEAD` for "days until next order"?
**Red flag:** forgetting `ORDER BY` inside the window (the function becomes meaningless without a defined row order).
**Learn it in:** Chapter 13, section 13.5.

### Rapid-fire, §71.5 (Core)

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q71-037 | What does `SUM(x) OVER (ORDER BY month)` compute, with no `PARTITION BY`? | A running total across all rows, in that order | **[+Edge cases]** without a frame clause, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, so rows that tie on the `ORDER BY` value get the same running total. Write `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` for a strict row-by-row running total → Ch 13 §13.6 |
| Q71-038 | What's the difference between a window function and `GROUP BY`? | `GROUP BY` collapses rows into one per group; a window function keeps every row and adds a calculated column beside it | **[+Business]** this is *why* window functions exist for reporting: you can show a customer's single order next to their running total, in the same row → Ch 13 §13.3 |
| Q71-039 | What's `NTILE(4)` for? | Splits ordered rows into 4 roughly equal-sized groups (quartiles) | **[+Business]** the SQL way to build a quartile or decile segmentation directly in a query → Ch 27 §27.4 (and Ch 28 §28.3) |
| Q71-040 | Can you use a window function's result in the same query's `WHERE` clause? | No: window functions are calculated after `WHERE`; wrap the query in a subquery or CTE and filter the outer layer | **[+Edge cases]** this is exactly why Q71-033 and Q71-035 wrap the window function in a subquery before filtering, and Q71-074 shows the real error → Ch 13 §13.3 |

**Q71-037, run (riverstone_2025).** The running total over Q71-028's CTE:
```sql
WITH monthly_revenue AS (
  SELECT DATE_TRUNC('month', o.order_date)::date AS month,
         ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS revenue
  FROM orders o
  JOIN order_items oi ON o.order_id = oi.order_id
  WHERE o.status <> 'Cancelled'
  GROUP BY 1
)
SELECT month, revenue,
       SUM(revenue) OVER (ORDER BY month) AS running_total
FROM monthly_revenue
ORDER BY month
LIMIT 3;
```
```
   month    |  revenue  | running_total
------------+-----------+---------------
 2025-01-01 | 202640.00 |     202640.00
 2025-02-01 | 253664.00 |     456304.00
 2025-03-01 | 278007.50 |     734311.50
(3 rows)
```
**[+Validate]** the running total reconciles: 2,02,640 + 2,53,664 = 4,56,304 ✓, and + 2,78,007.50 = 7,34,311.50 ✓. Each month appears once here, so `RANGE` and `ROWS` give the same answer; they part company only when two rows share a month.

---

## 71.6 Classic problems: duplicates, gaps-and-islands, retention

### Q71-041 · Find any duplicate customer names · *Core*

**Remember it as:** *GROUP BY the thing that should be unique, HAVING COUNT > 1.*

```sql
SELECT customer_name, COUNT(*)
FROM customers
GROUP BY customer_name
HAVING COUNT(*) > 1;
```

**Verified (riverstone_2025): 0 rows.** Riverstone's customer table has no exact-name duplicates.
```
 customer_name | count
---------------+-------
(0 rows)
```

| Tier | What to say |
|---|---|
| Passes | The query above, correctly, with no result to show |
| Strong | + says that an empty result here is the *real* answer on this data, not a broken query, and how they'd confirm it (run the same query on a column known to have duplicates, such as `city`) |
| Extra points | **[+Edge cases]** exact-name matching misses near-duplicates: trailing spaces, case differences, "Sharma Hardware" vs. "Sharma Hardware Pvt Ltd". Those need `TRIM`/`LOWER` first, or fuzzy matching, which is a different, harder problem · **[+Business]** near-duplicate customer records are one of the most common real data-quality issues in a CRM, and this exact-match query is only the first, cheapest check |

**Likely follow-ups:** How would you catch near-duplicates, not just exact ones? What would you do once you found real duplicates: merge them how?
**Red flag:** assuming an empty result means the query is wrong, rather than considering that it might be the honest answer.
**Learn it in:** Chapter 12, section 12.9; Chapter 14, section 14.4 (exact and fuzzy duplicates).

### Q71-042 · Find every customer's longest streak of consecutive order-days · *Advanced*

**Remember it as:** *The gaps-and-islands trick: subtract a row number from the date. Rows in the same streak land on the exact same result.*

**The query:**
```sql
WITH daily AS (
  SELECT DISTINCT customer_id, order_date
  FROM orders
),
numbered AS (
  SELECT customer_id, order_date,
         order_date - CAST(ROW_NUMBER() OVER (PARTITION BY customer_id
                                              ORDER BY order_date) AS INT) AS grp
  FROM daily
),
streaks AS (
  SELECT customer_id,
         MIN(order_date) AS streak_start,
         MAX(order_date) AS streak_end,
         COUNT(*)        AS streak_len
  FROM numbered
  GROUP BY customer_id, grp
)
SELECT customer_id, streak_start, streak_end, streak_len
FROM (
  SELECT s.*,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY streak_len DESC, streak_start) AS rn
  FROM streaks s
) t
WHERE rn = 1 AND streak_len >= 2
ORDER BY streak_len DESC, customer_id;
```

**Verified (riverstone_2025):** two customers have a streak of two consecutive order-days; no streak reaches three.
```
 customer_id | streak_start | streak_end | streak_len
-------------+--------------+------------+------------
           5 | 2025-01-12   | 2025-01-13 |          2
          15 | 2025-06-09   | 2025-06-10 |          2
(2 rows)
```

*MySQL:* a date minus a number is written `DATE_SUB`; the rest is unchanged, and it returns the same two rows:

<!-- run: mysql -->
```mysql
WITH daily AS (
  SELECT DISTINCT customer_id, order_date
  FROM orders
),
numbered AS (
  SELECT customer_id, order_date,
         DATE_SUB(order_date,
                  INTERVAL ROW_NUMBER() OVER (PARTITION BY customer_id
                                              ORDER BY order_date) DAY) AS grp
  FROM daily
),
streaks AS (
  SELECT customer_id,
         MIN(order_date) AS streak_start,
         MAX(order_date) AS streak_end,
         COUNT(*)        AS streak_len
  FROM numbered
  GROUP BY customer_id, grp
)
SELECT customer_id, streak_start, streak_end, streak_len
FROM (
  SELECT s.*,
         ROW_NUMBER() OVER (PARTITION BY customer_id
                            ORDER BY streak_len DESC, streak_start) AS rn
  FROM streaks s
) t
WHERE rn = 1 AND streak_len >= 2
ORDER BY streak_len DESC, customer_id;
```

| Tier | What to say |
|---|---|
| Passes | Solves it with `LAG`: flag a row when the gap to the previous date is more than 1 day, then a running `SUM` of the flags numbers the streaks. Correct, but longer |
| Strong | The row-number-minus-date query above, with the mechanism explained: within one streak the date goes up by 1 each row and so does the row number, so their difference stays constant; a gap breaks that and starts a new group. The last step keeps each customer's *longest* streak, not every streak |
| Extra points | **[+Validate]** the real result, honestly reported: only 2-day streaks exist in this dataset, nothing longer, rather than a more impressive-looking (fake) example · **[+Signpost]** name the pattern: this "constant difference" trick solves any gaps-and-islands problem: consecutive login days, consecutive shipped orders, consecutive price rises |

**Likely follow-ups:** Same, but for consecutive *calendar weeks*, not days? What's the equivalent trick if the sequence isn't dates but plain row order? What changes if `order_date` were a `TIMESTAMP`? *(Cast it to `DATE` first, or the subtraction and the grouping both break.)*
**Red flag:** reaching for a procedural loop (a cursor, or code outside SQL) as the only solution they can think of.
**Learn it in:** Chapter 13, section 13.8 (Pattern 8, streaks).

### Q71-043 · Which customers ordered in both January and February 2025? (a simple retention check) · *Core*

**Remember it as:** *Two EXISTS clauses, ANDed together: "ordered in month A" AND "ordered in month B."*

```sql
SELECT c.customer_id, c.customer_name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o
              WHERE o.customer_id = c.customer_id
                AND o.order_date BETWEEN '2025-01-01' AND '2025-01-31')
  AND EXISTS (SELECT 1 FROM orders o
              WHERE o.customer_id = c.customer_id
                AND o.order_date BETWEEN '2025-02-01' AND '2025-02-28')
ORDER BY c.customer_id;
```

**Verified (riverstone_2025): 4 customers** ordered in both months.
```
 customer_id |   customer_name
-------------+-------------------
           1 | Sharma Hardware
           3 | Green Leaf Hotels
           4 | Coastal Foods
           5 | Metro Mart
(4 rows)
```

| Tier | What to say |
|---|---|
| Passes | Two separate queries (January customers, February customers), compared by eye: works for a one-off check, doesn't scale to "for every pair of consecutive months" |
| Strong | The double-`EXISTS` version above, or two conditional counts compared in one row |
| Extra points | **[+Signpost]** this is retention at its simplest: full cohort retention extends it into a month-by-month grid, built with conditional aggregation (`SUM(CASE WHEN ... THEN 1 ELSE 0 END)`) rather than repeated `EXISTS` (Chapter 13's Pattern 7 builds the full grid) · **[+Business]** January had only 5 active customers (Q71-027), so 4 of them returning in February is a strong start; say what you'd compare it with before calling it good or bad |

**Likely follow-ups:** Build a full 12-month retention grid? What's the difference between this and a rolling "active in the last 30 days" count?
**Red flag:** confusing "ordered in both months" with "ordered at all in the date range" (missing the AND of two `EXISTS`).
**Learn it in:** Chapter 12, section 12.12 (`EXISTS`); Chapter 13, section 13.8 (Pattern 7, cohort retention).

### Rapid-fire, §71.6 (Core)

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q71-044 | Find products that have never been sold? | `LEFT JOIN` products to order_items `WHERE oi.product_id IS NULL`, or `NOT EXISTS` | **[+Validate]** verified on riverstone_2025: 0 rows, because all 8 products have sold. On the mini database `riverstone` the same query returns Garden Chair: check which database you're on → Ch 12 §12.10 |
| Q71-045 | Find the Nth highest value in general, not just the 2nd? | `DENSE_RANK() OVER (ORDER BY x DESC)`, then filter `WHERE rnk = N` in an outer query | **[+Edge cases]** the same tie-safety reasoning as Q71-033, for any N → Ch 13 §13.4 |
| Q71-046 | Compute a percentage of total per row? | `100.0 * x / SUM(x) OVER ()`: no `GROUP BY` needed, since a window with no `PARTITION BY` sees every row | **[+Edge cases]** multiply by `100.0` first: in PostgreSQL an integer column divided by an integer total gives 0 (verified: `quantity / SUM(quantity) OVER () * 100` is 0 on every order line). MySQL's `/` always returns a decimal, so the bug only shows when you port the query → Ch 13 §13.3 |

---

## 71.7 Schema, constraints, and transactions

The first three questions build small tables of their own. Run them in `riverstone_lab`, the practice database from Chapter 12, section 12.13; every demo drops its tables at the end. The foreign keys are written on their own line, as Chapter 12's dialect note in section 12.13 recommends: MySQL 8.4 and earlier silently ignore the shorter inline `REFERENCES` form, and InnoDB doesn't support foreign keys on temporary tables at all.

<!-- lab:start -->

### Q71-047 · Demonstrate the difference between `ON DELETE CASCADE` and the default (`NO ACTION`) behavior · *Core*

**Remember it as:** *CASCADE says "delete the children too." The default says "refuse to delete the parent while children still exist."*

**Answer in one line:** Without `ON DELETE CASCADE`, deleting a parent row is refused while any child rows still reference it; with `ON DELETE CASCADE`, deleting the parent automatically deletes those child rows too.

**Verified, in `riverstone_lab`. With CASCADE** (same statements in both databases):

<!-- run: both -->
```sql
CREATE TABLE parent_t (id INT PRIMARY KEY);
CREATE TABLE child_t (
  id        INT,
  parent_id INT,
  FOREIGN KEY (parent_id) REFERENCES parent_t (id) ON DELETE CASCADE
);
INSERT INTO parent_t VALUES (1), (2);
INSERT INTO child_t VALUES (10, 1), (11, 1), (12, 2);
DELETE FROM parent_t WHERE id = 1;
SELECT * FROM child_t;
```
```
 id | parent_id
----+-----------
 12 |         2
(1 row)
```

*MySQL:*

<!-- out: mysql -->
```
+------+-----------+
| id   | parent_id |
+------+-----------+
|   12 |         2 |
+------+-----------+
```

Rows 10 and 11, both children of parent 1, are gone too. **Without CASCADE, the default:**

<!-- run: both -->
```sql
CREATE TABLE parent_r (id INT PRIMARY KEY);
CREATE TABLE child_r (
  id        INT,
  parent_id INT,
  FOREIGN KEY (parent_id) REFERENCES parent_r (id)
);
INSERT INTO parent_r VALUES (1);
INSERT INTO child_r VALUES (10, 1);
DELETE FROM parent_r WHERE id = 1;
```
```
ERROR:  update or delete on table "parent_r" violates foreign key constraint "child_r_parent_id_fkey" on table "child_r"
DETAIL:  Key (id)=(1) is still referenced from table "child_r".
```

*MySQL:*

<!-- out: mysql -->
```
ERROR 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`riverstone_lab`.`child_r`, CONSTRAINT `child_r_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `parent_r` (`id`))
```

Tidy up (same in both):

<!-- run: both -->
```sql
DROP TABLE child_t, parent_t, child_r, parent_r;
```

| Tier | What to say |
|---|---|
| Passes | "`CASCADE` deletes related rows too" (correct, no comparison with the default) |
| Strong | Both behaviors above, contrasted: cascade silently removes children; the default blocks the delete with an error |
| Extra points | **[+Validate]** both real outcomes on parallel tables: 2 rows silently gone with CASCADE, 1 delete flatly refused without it, in both databases · **[+Edge cases]** PostgreSQL's default is `NO ACTION`, checked at the end of the statement (and deferrable); `RESTRICT` checks immediately. In MySQL the two are identical · **[+Business]** `CASCADE` is powerful and dangerous: deleting one customer with `CASCADE` on their orders would silently delete their whole order history. Keep it for truly dependent data (an order's own line items), not for a parent whose "children" are valuable records in their own right |

**Likely follow-ups:** What's `ON DELETE SET NULL`? When would you prefer it to CASCADE? What about `ON UPDATE CASCADE`?
**Red flag:** treating `CASCADE` as a safe default rather than a deliberate, case-by-case decision.
**Learn it in:** Chapter 12, section 12.13 (Step 6, the `ON DELETE` options, and the dialect note in Step 3). `ON UPDATE CASCADE` and deferrable constraints are *beyond the book*.

### Q71-048 · Write a `CHECK` constraint enforcing that a discount percentage is between 0 and 100, and show it rejecting bad data · *Core*

**Remember it as:** *A CHECK constraint is a rule the database enforces on every write, not a rule you hope the application remembers.*

**Verified, in `riverstone_lab`** (same statements in both databases):

<!-- run: both -->
```sql
CREATE TABLE tx_check (
  id           INT,
  discount_pct NUMERIC(5,2),
  CONSTRAINT chk_discount CHECK (discount_pct BETWEEN 0 AND 100)
);
INSERT INTO tx_check VALUES (1, 50);
INSERT INTO tx_check VALUES (2, 150);
```
```
ERROR:  new row for relation "tx_check" violates check constraint "chk_discount"
DETAIL:  Failing row contains (2, 150.00).
```

*MySQL:*

<!-- out: mysql -->
```
ERROR 3819 (HY000): Check constraint 'chk_discount' is violated.
```

The first insert (50) succeeded; the second (150) was refused. Tidy up (same in both):

<!-- run: both -->
```sql
DROP TABLE tx_check;
```

| Tier | What to say |
|---|---|
| Passes | "You'd validate the discount in the application code before saving it" |
| Strong | The `CHECK` constraint above, and why it's a stronger guarantee than application-level validation alone |
| Extra points | **[+Validate]** the real errors above, including PostgreSQL's `DETAIL` line with the exact rejected row · **[+Business]** application checks can be bypassed by a second application, a manual data fix, or a bug; a `CHECK` constraint can't be bypassed by anything that writes to the table: Consistency (Q71-051) enforced, not hoped for · **[+Edge cases]** MySQL before 8.0.16 accepted `CHECK` and ignored it. Always test that a constraint rejects a bad row |

**Likely follow-ups:** What's the difference between a `CHECK` constraint and a `NOT NULL` constraint? Can a `CHECK` constraint look at another table? *(No, not directly; a cross-table rule needs a trigger or a foreign key.)*
**Red flag:** relying entirely on application code to enforce a rule the database itself could guarantee.
**Learn it in:** Chapter 12, section 12.13 (Step 3, and "When the database says no").

<!-- lab:end -->

### Q71-049 · Build a view for "each customer's total revenue," and explain what a view actually is · *Core*

**Remember it as:** *A view isn't a copy of the data. It's a saved query with a name, re-run fresh every time you query it.*

**Answer in one line:** `CREATE VIEW` saves a query under a name; querying the view re-runs that query against the live data every time, it doesn't store a snapshot.

**Verified (riverstone_2025).** Create the view (same in MySQL):

<!-- run: none -->
<!-- ch71-check: view -->
```sql
CREATE VIEW customer_revenue AS
SELECT c.customer_id, c.customer_name,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS revenue
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name;
```

Query it like a table:

<!-- run: none -->
<!-- ch71-check: view -->
```sql
SELECT * FROM customer_revenue ORDER BY revenue DESC LIMIT 3;
```
```
 customer_id |     customer_name      |  revenue
-------------+------------------------+-----------
           1 | Sharma Hardware        | 502775.00
          11 | Harbour Traders        | 412680.50
           7 | Northgate Distributors | 353088.50
(3 rows)
```

Then remove it, so `riverstone_2025` stays as it was:

<!-- run: none -->
<!-- ch71-check: view -->
```sql
DROP VIEW customer_revenue;
```

| Tier | What to say |
|---|---|
| Passes | "A view is like a virtual table" (true, doesn't explain the "re-run every time" mechanism) |
| Strong | + a plain view has no stored data of its own; every `SELECT` against it runs the underlying query fresh, so it's always current, and it costs the full query every time |
| Extra points | **[+Validate]** the top three match what the underlying `GROUP BY` query returns when you run it directly (Q71-073), since that's literally what the view does · **[+Trade-offs]** a **materialized view** (`CREATE MATERIALIZED VIEW`, PostgreSQL only; MySQL has none) stores the result, so it's fast to query but stale until you run `REFRESH MATERIALIZED VIEW`: a trade between freshness and speed. In MySQL the equivalent is a summary table refreshed by a scheduled job · **[+Business]** a view is also a clean way to hide a complex join behind a simple name for less technical users, and to enforce row-level access (a view showing only a rep's own accounts) without repeating the logic in every query |

**Likely follow-ups:** Can you `INSERT` into a view? *(Sometimes, for simple views, with restrictions.)* What does querying a view built on another view cost?
**Red flag:** believing a plain view stores a copy of the data at creation time.
**Learn it in:** Chapter 13, section 13.2 (views); Chapter 28, section 28.11 (materialized views).

### Q71-050 · Demonstrate that `ROLLBACK` actually undoes a change, not just "cancels" it · *Core*

**Remember it as:** *Nothing inside BEGIN…COMMIT is permanent until COMMIT. ROLLBACK makes it as if it never happened at all.*

**Answer in one line:** A transaction's changes are only permanent once `COMMIT` runs; `ROLLBACK` reverts every change made since `BEGIN`, restoring the exact earlier state.

**Verified, in `riverstone_lab`** (same statements in both databases; MySQL also accepts `START TRANSACTION` for `BEGIN`):

<!-- lab:start -->

<!-- run: both -->
```sql
CREATE TABLE tx_test (id INT, val VARCHAR(20));
INSERT INTO tx_test VALUES (1, 'original');
```

<!-- run: both -->
```sql
BEGIN;
UPDATE tx_test SET val = 'changed' WHERE id = 1;
SELECT * FROM tx_test;   -- inside the open transaction
ROLLBACK;
SELECT * FROM tx_test;   -- after ROLLBACK
DROP TABLE tx_test;
```
```
 id |   val
----+---------
  1 | changed
(1 row)

 id |   val
----+----------
  1 | original
(1 row)
```

*MySQL:*

<!-- out: mysql -->
```
+------+---------+
| id   | val     |
+------+---------+
|    1 | changed |
+------+---------+
+------+----------+
| id   | val      |
+------+----------+
|    1 | original |
+------+----------+
```

<!-- lab:end -->

| Tier | What to say |
|---|---|
| Passes | "`ROLLBACK` undoes changes" (correct, no demonstration of the mechanism) |
| Strong | + explains that the `UPDATE` is visible *within* the same session immediately, but is not permanent until `COMMIT`, and `ROLLBACK` discards it entirely |
| Extra points | **[+Validate]** the live proof above: the same `SELECT`, before and after `ROLLBACK`, gives two different real answers on the same table · **[+Business]** this is *why* multi-step operations (move money between two accounts, place an order and reduce stock together) belong in one transaction: if step two fails, `ROLLBACK` guarantees step one never sticks around half-finished |

**Likely follow-ups:** What does `COMMIT` do that makes a change durable? What happens if the connection drops before either COMMIT or ROLLBACK runs? *(The transaction is rolled back automatically.)*
**Red flag:** not knowing that changes are visible inside the same session before commit, and invisible to *other* sessions until commit.
**Learn it in:** Chapter 12, section 12.13 (Step 8, transactions).

### Q71-051 · What does ACID stand for? Give one real example of each · *Core*

**Remember it as:** *Atomic: all or nothing. Consistent: rules always hold. Isolated: transactions don't see each other's half-finished work. Durable: once committed, it survives a crash.*

**Answer in one line:** **A**tomicity (a transaction fully succeeds or fully fails, no partial state), **C**onsistency (every committed change leaves the data obeying its declared rules), **I**solation (concurrent transactions don't see each other's uncommitted changes), **D**urability (once committed, a change survives a crash or power loss).

| Tier | What to say |
|---|---|
| Passes | Can name what the letters stand for, can't give a concrete example of any of them |
| Strong | + one real example each: Atomicity (Q71-050's transfer example: both the debit and the credit happen, or neither does) · Consistency (a `CHECK` constraint, Q71-048, refusing an invalid row) · Isolation (two people checking stock at once shouldn't both believe the last unit is theirs) · Durability (a committed order survives the database server crashing five seconds later) |
| Extra points | **[+Edge cases]** isolation comes in *levels* (Q71-056), so "isolated" isn't one fixed behavior but a range of trade-offs · **[+Business]** these four properties are why a relational database, not a plain file, is the default for anything involving money or stock, where a value must never silently go wrong |

**Likely follow-ups:** Which of the four is hardest to guarantee at scale? Which systems deliberately relax some of them, and why?
**Red flag:** reciting the acronym with no example for any letter.
**Learn it in:** Chapter 12, section 12.13 (Step 8, transactions); Chapter 49, section 49.4 (ACID).

### Beyond the book: concurrency in five minutes

The last four rapid-fire rows below (Q71-056 to Q71-059) go beyond the teaching chapters, so here is the short explanation they need. When two sessions work on the same table at once, the **isolation level** decides what one session can see of the other's unfinished work. Each database has a default. Check yours:

```sql
SHOW default_transaction_isolation;
```
```
 default_transaction_isolation
-------------------------------
 read committed
(1 row)
```

*MySQL:*
```mysql
SELECT @@transaction_isolation;
```
```
+-------------------------+
| @@transaction_isolation |
+-------------------------+
| REPEATABLE-READ         |
+-------------------------+
```

`SHOW` reads one of PostgreSQL's settings by name; in MySQL, `@@` in front of a name reads a server setting (a *system variable*) the same way. So PostgreSQL starts every transaction at Read Committed, and MySQL at Repeatable Read.

A **dirty read** is the thing the weakest level allows. Picture two sessions, A and B, and an order whose status is `'Pending'`:

| Step | Session A | Session B | What B sees |
|---|---|---|---|
| 1 | `BEGIN;` `UPDATE orders SET status = 'Shipped' WHERE order_id = 10001;` | | |
| 2 | | `SELECT status FROM orders WHERE order_id = 10001;` | Read Uncommitted: `'Shipped'` (a dirty read). Read Committed or stricter: `'Pending'` |
| 3 | `ROLLBACK;` | | |
| 4 | | the same `SELECT` again | `'Pending'`: the "Shipped" B may have seen in step 2 never existed |

Neither database allows a dirty read by default. Both let a plain `SELECT` in B go ahead at step 2 without waiting for A: each keeps the last committed version of the row for readers, an idea called **MVCC** (multi-version concurrency control).

### Rapid-fire, §71.7 (Core; Q71-056 to Q71-059 Advanced)

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q71-052 | `ALTER TABLE ... ADD COLUMN` with a default value on a huge table: what should you know? | PostgreSQL 11 and later add a column with a constant default instantly, without rewriting every row; older versions, and some other engines, rewrite the whole table, which can lock it for a long time | **[+Business]** check your engine and version before assuming a schema change on a huge production table is "instant" → Ch 28 §28.12 (changing a live database); the version detail is *beyond the book* |
| Q71-053 | What's the difference between a `PRIMARY KEY` and a `UNIQUE` constraint? | A table has at most one `PRIMARY KEY` (which also forbids NULL); it can have many `UNIQUE` constraints, and each still allows multiple NULLs (Q71-013) | **[+Edge cases]** this is why an email `UNIQUE` constraint doesn't stop multiple blank emails, but adding `NOT NULL` to the `UNIQUE` column would. (A `CHECK (email <> '')` also blocks empty text, per Q71-022) → Ch 12 §12.13 |
| Q71-054 | What does `NOT NULL` enforce, and can you add it to a column that already has data? | It rejects any future NULL in that column; adding it to an existing column needs every current value to be non-NULL already, or the `ALTER TABLE` itself fails | **[+Edge cases]** run a check first, `SELECT COUNT(*) FROM t WHERE col IS NULL`, before adding `NOT NULL` to a live table → Ch 12 §12.13 (Step 9) |
| Q71-055 | What's a materialized-view refresh strategy, in one sentence? | Refresh on a schedule (nightly, hourly), or refresh from a trigger or pipeline step after the source loads (PostgreSQL has no automatic refresh), chosen by how stale the data may get | **[+Business]** the same freshness-vs-cost trade as a Power BI scheduled refresh, one layer down → Ch 28 §28.11; Ch 46 (pipeline steps); Ch 16 §16.9 (Power BI refresh) |
| Q71-056 | What's a transaction isolation level, in plain terms? | A setting for how much of another transaction's unfinished work you can see while your own transaction runs | **[+Edge cases]** from loosest to strictest: Read Uncommitted, Read Committed (PostgreSQL's default), Repeatable Read (MySQL InnoDB's default), Serializable (both checked above) → *Beyond the book* (the box above) |
| Q71-057 | What's a "dirty read"? | Reading another transaction's uncommitted change, which might still be rolled back and never happen | **[+Edge cases]** only possible at Read Uncommitted; PostgreSQL doesn't implement that level separately and behaves as Read Committed even if you ask for it → *Beyond the book* (the box above) |
| Q71-058 | What's a deadlock? | Two transactions each waiting for a lock the other one holds, so neither can ever proceed | **[+Business]** the database detects it and rolls back one of the two transactions rather than letting both hang forever; application code should catch that error and retry → *Beyond the book* |
| Q71-059 | Does a `SELECT` ever get blocked by another transaction's write? | Under each engine's default level (Read Committed in PostgreSQL, Repeatable Read in MySQL), a plain `SELECT` isn't blocked: it reads the last committed version | **[+Edge cases]** the exception is a locking read, `SELECT … FOR UPDATE`, which does wait for the writer. Plain reads don't wait because of MVCC → *Beyond the book* (the box above) |

---

## 71.8 PostgreSQL vs. MySQL: where the dialects actually differ

Every pair below was run on both databases against the same Riverstone data.

### Q71-060 · String aggregation: `STRING_AGG` vs. `GROUP_CONCAT` · *Core*

**Remember it as:** *Same job, different name, different separator syntax.*

PostgreSQL:
```sql
SELECT category,
       STRING_AGG(DISTINCT product_name, ', ' ORDER BY product_name) AS products
FROM products
GROUP BY category
ORDER BY category;
```
```
  category  |                    products
------------+------------------------------------------------
 Furniture  | Garden Chair
 Industrial | Industrial Crate
 Kitchen    | Food Container Set, Lunch Box Set, Water Bottle 1L
 Storage    | Stackable Bin, Storage Box 10L, Storage Box 25L
(4 rows)
```

*MySQL:*
```mysql
SELECT category,
       GROUP_CONCAT(DISTINCT product_name ORDER BY product_name SEPARATOR ', ') AS products
FROM products
GROUP BY category
ORDER BY category;
```
```
+------------+----------------------------------------------------+
| category   | products                                           |
+------------+----------------------------------------------------+
| Furniture  | Garden Chair                                       |
| Industrial | Industrial Crate                                   |
| Kitchen    | Food Container Set, Lunch Box Set, Water Bottle 1L |
| Storage    | Stackable Bin, Storage Box 10L, Storage Box 25L    |
+------------+----------------------------------------------------+
```

| Tier | What to say |
|---|---|
| Passes | Knows one function, not the other engine's name for it |
| Strong | Both function names and their (slightly different) syntax for the separator |
| Extra points | **[+Validate]** the same four lines from both engines, above · **[+Edge cases]** MySQL's `GROUP_CONCAT` has a length limit (`group_concat_max_len`, 1,024 bytes by default) and silently cuts off longer results: worth knowing before it bites in production |

**Learn it in:** Chapter 14, section 14.4 (`STRING_AGG`, with MySQL's `GROUP_CONCAT` in the same paragraph). `group_concat_max_len` is *beyond the book*.

### Rapid-fire, §71.8 (Core): dialect differences

| # | Feature | PostgreSQL | MySQL | Extra point |
|---|---|---|---|---|
| Q71-061 | NULL replacement | `COALESCE(x, 'default')` | `IFNULL(x, 'default')` or `COALESCE` (both work) | **[+Edge cases]** MySQL supports `COALESCE` too; `IFNULL` is a MySQL shorthand for the two-argument case → Ch 12 §12.7 (`COALESCE`); `IFNULL` is *beyond the book* |
| Q71-062 | Auto-incrementing primary key | `GENERATED ALWAYS AS IDENTITY` (older code: `SERIAL`) | `AUTO_INCREMENT` | **[+Business]** copy-pasting a `CREATE TABLE` between engines without translating this is one of the most common cross-dialect errors → Ch 12 §12.13 (Steps 2 and 3) |
| Q71-063 | Limiting and skipping rows | `LIMIT n OFFSET m` | `LIMIT m, n` (offset first!) or `LIMIT n OFFSET m` (also works) | **[+Edge cases]** MySQL's `LIMIT m, n` puts the offset *first*, a common source of swapped-number bugs when porting a query → Ch 12 §12.5 (`LIMIT`); `OFFSET` is *beyond the book* |
| Q71-064 | Current date and time | `CURRENT_DATE`, `NOW()` | `CURRENT_DATE` (or `CURDATE()`), `NOW()` | **[+Trade-offs]** `CURRENT_DATE` and `NOW()` work in both; prefer `CURRENT_DATE` for portability. The real difference is date arithmetic → Ch 12 §12.16 (`DATEDIFF` and `INTERVAL`) |
| Q71-065 | Case of table and column names | Unquoted names are folded to lower case | Table names are case-sensitive on Linux and case-insensitive on Windows and macOS by default | **[+Edge cases]** a query that works on a laptop can fail on a Linux production MySQL server purely because of table-name casing: use lower-case names everywhere → Ch 12 §12.13 (the "Naming" note) |
| Q71-066 | Boolean type | Native `BOOLEAN`, `true`/`false` | `BOOLEAN` is an alias for `TINYINT(1)` | **[+Edge cases]** MySQL's "boolean" columns are really small integers, which is why `0`/`1` and `FALSE`/`TRUE` are interchangeable there (and why Q71-009 prints `1`) → Ch 12 §12.13 |
| Q71-067 | Window functions | Full support since PostgreSQL 8.4 | Full support since MySQL 8.0 (not in 5.7 or earlier) | **[+Business]** if a company runs an older MySQL, ask whether window functions are available before assuming this chapter's window questions (Q71-033 to Q71-040, Q71-042, Q71-045, Q71-046 and Q71-074) apply as written → Ch 13 §13.9 |

---

## 71.9 Query optimization and indexes

### Q71-068 · What does `EXPLAIN` show, and what did it show on Riverstone's orders table? · *Advanced*

**Remember it as:** *EXPLAIN tells you what the database plans to do, not what you assume it does.*

**Answer in one line:** `EXPLAIN` shows the query planner's chosen strategy (a sequential scan, an index scan, a join method) and its estimated cost, before running the query.

**Verified (riverstone_2025), on the 175-row orders table:**

```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 1;
```
```
                       QUERY PLAN
--------------------------------------------------------
 Seq Scan on orders  (cost=0.00..4.19 rows=16 width=25)
   Filter: (customer_id = 1)
(2 rows)
```

Now add an index on `customer_id`, and refresh the table's statistics:

<!-- run: none -->
<!-- ch71-check: index -->
```sql
CREATE INDEX idx_orders_customer ON orders (customer_id);
ANALYZE orders;
```

`ANALYZE` refreshes the table statistics the planner uses; without it the planner may be working from stale row counts. Ask for the plan again:

<!-- run: none -->
<!-- ch71-check: index -->
```sql
EXPLAIN SELECT * FROM orders WHERE customer_id = 1;
```

*(Unchanged: the table is too small for the index to pay off.)*
```
                       QUERY PLAN
--------------------------------------------------------
 Seq Scan on orders  (cost=0.00..4.19 rows=16 width=25)
   Filter: (customer_id = 1)
(2 rows)
```

Remove the index, so the database is left as it was:

<!-- run: none -->
<!-- ch71-check: index -->
```sql
DROP INDEX idx_orders_customer;
```

*MySQL:* InnoDB builds an index for every foreign key automatically, so MySQL already has one on `orders.customer_id` and uses it (`type` is `ref`, `key` is `customer_id`) before you add anything. `FORMAT=TRADITIONAL` asks for the plan as a table, which looks the same on every version; MySQL 9 otherwise prints the one-line tree that Chapter 28, section 28.13 reads (`-> Index lookup on orders using customer_id …`). Ending the statement with `\G` instead of `;` makes the `mysql` client print each column on its own line, which is easier to read for a wide result like this one:
```mysql
EXPLAIN FORMAT=TRADITIONAL SELECT * FROM orders WHERE customer_id = 1\G
```
```
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: orders
   partitions: NULL
         type: ref
possible_keys: customer_id
          key: customer_id
      key_len: 4
          ref: const
         rows: 16
     filtered: 100.00
        Extra: NULL
```

| Tier | What to say |
|---|---|
| Passes | "`EXPLAIN` shows you the query plan" |
| Strong | + explains what a sequential scan means (reads every row) versus an index scan (jumps straight to the matching rows) |
| Extra points | **[+Validate]** the real surprise above: even *with* an index, PostgreSQL's planner still chose a sequential scan on this table, and that's not a bug: on 175 rows, reading everything is cheaper than the extra work of using an index, and the planner knows it · **[+Edge cases]** this is the honest answer to "why isn't my index being used?": indexes pay off on large tables, not small ones, and a planner that ignores a small table's index is doing its job · **[+Trade-offs]** `rows=16` is the planner's *estimate*, and it matches Sharma Hardware's 16 orders (Q71-034); `EXPLAIN ANALYZE` runs the query and adds the real counts and timings |

**Likely follow-ups:** At what table size would you expect the planner to switch to the index? What's the difference between a sequential scan and an index scan in disk reads?
**Red flag:** assuming an index is always used just because it exists.
**Learn it in:** Chapter 28, sections 28.4–28.5 (and section 28.6 for indexes; Chapter 49 for storage at scale).

### Rapid-fire, §71.9 (Advanced)

| # | Question | One-line answer | Extra point |
|---|---|---|---|
| Q71-069 | Which columns usually benefit most from an index? | Columns often used in `WHERE`, `JOIN … ON` and `ORDER BY`, especially on large tables | **[+Trade-offs]** every index speeds up reads but slows down writes (`INSERT`/`UPDATE`/`DELETE` must keep it up to date too): indexing everything is not free → Ch 28 §28.6 |
| Q71-070 | What's a composite index, and when does column order matter? | An index on several columns together; it helps most when a query filters on the *leading* column(s), in the order the index was built | **[+Edge cases]** an index on `(customer_id, order_date)` speeds up `WHERE customer_id = X AND order_date > Y`, but doesn't help a query filtering on `order_date` alone → Ch 28 §28.6 |
| Q71-071 | What's a covering index? | An index that holds every column a query needs, so the database answers from the index alone without reading the table rows | **[+Business]** one of the highest-impact, lowest-effort fixes for a frequently run report query → Ch 28 §28.6 |

---

## 71.10 Live-coding walk-throughs

<!-- db: riverstone -->

### Q71-072 · Walk-through: revenue by order, with a fan-out warning · *Core*

**What they're really testing:** whether you notice a join that silently multiplies rows before you trust the total it produces.

**The setup, talked through live:** "I need each order's revenue. Orders join to order_items for the line amounts. If this business also has invoices and payments tables, and I'm tempted to join through both to get to 'paid revenue,' I need to check first whether an invoice can have more than one payment, because that join would then count the order's revenue once per payment."

**Verified (riverstone, the mini database):** it has exactly this shape: order 5006's invoice has 2 payment rows. The wrong way, joining through invoices and payments before adding up the line items:

```sql
SELECT o.order_id,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS wrong_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN invoices i     ON o.order_id = i.order_id
JOIN payments p     ON i.invoice_id = p.invoice_id
WHERE o.order_id = 5006
GROUP BY o.order_id;
```
```
 order_id | wrong_total
----------+-------------
     5006 |    29280.00
(1 row)
```

The right way, adding up the line items on their own, with payments left out:

```sql
SELECT o.order_id,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS correct_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_id = 5006
GROUP BY o.order_id;
```
```
 order_id | correct_total
----------+---------------
     5006 |      14640.00
(1 row)
```

**The order's revenue is ₹14,640. The fan-out join reports ₹29,280: exactly double, because its invoice has exactly 2 payments.**

**Extra-points moves demonstrated:** **[+Edge cases]** expected the fan-out before running anything, from knowing an invoice can have several payments. **[+Validate]** proved it with a real doubled number on this exact order, not a hypothetical. **[+Business]** stated the fix plainly: compute revenue from `order_items` alone, and join to payments (if at all) only for payment-status questions, never in the same sum as revenue.

**Likely follow-ups:** How would you check for this kind of fan-out risk *before* writing the query, on a schema you've never seen? How would you fix a report that has already shipped with this bug?
**Red flag:** trusting a multi-join total without asking whether any joined table could have more than one matching row per order.
**Learn it in:** Chapter 12, section 12.10 (join fan-out); Chapter 13, section 13.8 (Pattern 10, checks before you trust a report).

<!-- db: riverstone_2025 -->

### Q71-073 · Walk-through: "give me our top customers": the clarifying-question round · *Core*

**What they're really testing:** whether you ask before you build, on a question that's genuinely ambiguous.

**Talked through live:** "'Top customers' could mean several things, and each needs a different query: by total revenue, by revenue this year only, by order count, or by average order value. I'll ask which, and while I wait I'll build the total-revenue version, since that's the most common meaning."

```sql
SELECT c.customer_id, c.customer_name,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS total_revenue
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC
LIMIT 5;
```

**Verified (riverstone_2025):**
```
 customer_id |     customer_name      | total_revenue
-------------+------------------------+---------------
           1 | Sharma Hardware        |     502775.00
          11 | Harbour Traders        |     412680.50
           7 | Northgate Distributors |     353088.50
           3 | Green Leaf Hotels      |     331388.75
           5 | Metro Mart             |     329297.50
(5 rows)
```

**Extra-points moves demonstrated:** **[+Clarify]** named the real ambiguity instead of guessing silently. **[+Simple first]** still produced a working, reasonable default answer while waiting, rather than stalling on the clarifying question. **[+Edge cases]** left out cancelled orders, a decision stated out loud rather than assumed. **[+Validate]** the first three match Q71-049's view exactly.

**Likely follow-ups:** Now by average order value instead. Now for a specific date range. Now leaving out one large outlier customer: how would you handle that request?
**Red flag:** picking one interpretation silently and never mentioning that the ambiguity existed.
**Learn it in:** Chapter 12, sections 12.9–12.10; Chapter 69, Move 1 (clarify first).

### Q71-074 · Walk-through: does each customer's spend beat their own earlier average? · *Advanced*

**What they're really testing:** whether you can compare a row with the same customer's own history without a self-join, using a window frame most candidates have only seen in its default form.

**Talked through live:** "I need each customer-month's revenue, then the average of *that customer's own* earlier months only. A plain `AVG() OVER (PARTITION BY customer_id)` averages every month, future ones included. Adding `ORDER BY month` still includes the current row. I need a frame that ends at `1 PRECEDING`: everything before the current row, nothing after."

A common first attempt puts the window function straight into `WHERE`. That fails, for the reason in Q71-040: window functions run after `WHERE`.

```sql
SELECT customer_id, month, revenue
FROM (
  SELECT o.customer_id,
         DATE_TRUNC('month', o.order_date)::date AS month,
         SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS revenue
  FROM orders o
  JOIN order_items oi ON o.order_id = oi.order_id
  WHERE o.status <> 'Cancelled'
  GROUP BY 1, 2
) m
WHERE revenue > AVG(revenue) OVER (PARTITION BY customer_id ORDER BY month
                                   ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING);
```
```
ERROR:  window functions are not allowed in WHERE
```

(MySQL's wording: `ERROR 3593 (HY000): You cannot use the window function 'avg' in this context.'`) The fix: calculate the window in a CTE (`with_avg`) and filter the outer query, the same pattern as Q71-033 and Q71-035.

**Verified (riverstone_2025):**
```sql
WITH monthly AS (
  SELECT o.customer_id,
         DATE_TRUNC('month', o.order_date)::date AS month,
         SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS revenue
  FROM orders o
  JOIN order_items oi ON o.order_id = oi.order_id
  WHERE o.status <> 'Cancelled'
  GROUP BY 1, 2
),
with_avg AS (
  SELECT customer_id, month, revenue,
         AVG(revenue) OVER (
           PARTITION BY customer_id ORDER BY month
           ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
         ) AS prior_avg
  FROM monthly
)
SELECT customer_id, month,
       ROUND(revenue, 2)   AS revenue,
       ROUND(prior_avg, 2) AS prior_avg
FROM with_avg
WHERE prior_avg IS NOT NULL
  AND revenue > prior_avg
ORDER BY customer_id, month
LIMIT 3;
```
```
 customer_id |   month    | revenue  | prior_avg
-------------+------------+----------+-----------
           1 | 2025-03-01 | 64387.50 |  63656.25
           1 | 2025-10-01 | 96825.00 |  34443.89
           1 | 2025-11-01 | 82250.00 |  40682.00
(3 rows)
```

*MySQL:* the same `DATE_FORMAT` swap as in Q71-028 (`ROUND(x, 2)` already works in both); it returns the same three rows.

**Extra-points moves demonstrated:** **[+Edge cases]** caught the default-frame trap before writing any code, not after a wrong answer. **[+Validate]** customer 1's October revenue (₹96,825) against an earlier average of only ₹34,443.89: a real, large beat, and November's average checks by hand, (9 × 34,443.89 + 96,825) ÷ 10 = 40,682.00. **[+Business]** "is this customer trending up against their own history" is a useful account-health signal, different from comparing customers with each other.

**Likely follow-ups:** What if you wanted a 3-month trailing average instead of all earlier months? How would this change using `LAG` instead of a frame clause?
**Red flag:** using the default window frame and not noticing the current row leaking into its own comparison average.
**Learn it in:** Chapter 13, section 13.6; Chapter 28, section 28.3 (frames that end before the current row).

### Q71-075 · Walk-through: pivot monthly revenue by category into columns, live · *Core*

**What they're really testing:** whether conditional aggregation (`CASE` inside `SUM`) comes to mind, since standard SQL has no `PIVOT` keyword the way spreadsheets and a few database platforms do.

**Talked through live:** "There's no universal `PIVOT` in standard SQL. The standard trick is conditional aggregation: one `SUM(CASE WHEN category = X THEN revenue ELSE 0 END)` per category I want as a column, one column for each of the four categories."

**Verified (riverstone_2025),** the first three months:
```sql
SELECT DATE_TRUNC('month', o.order_date)::date AS month,
  ROUND(SUM(CASE WHEN p.category = 'Storage'
                 THEN oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)
                 ELSE 0 END), 2) AS storage,
  ROUND(SUM(CASE WHEN p.category = 'Kitchen'
                 THEN oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)
                 ELSE 0 END), 2) AS kitchen,
  ROUND(SUM(CASE WHEN p.category = 'Industrial'
                 THEN oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)
                 ELSE 0 END), 2) AS industrial,
  ROUND(SUM(CASE WHEN p.category = 'Furniture'
                 THEN oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)
                 ELSE 0 END), 2) AS furniture
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p     ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY 1
ORDER BY 1
LIMIT 3;
```
```
   month    |  storage  | kitchen  | industrial | furniture
------------+-----------+----------+------------+-----------
 2025-01-01 | 172240.00 | 30400.00 |       0.00 |      0.00
 2025-02-01 | 150231.50 | 54152.50 |   49280.00 |      0.00
 2025-03-01 | 180785.00 | 49335.00 |   31500.00 |  16387.50
(3 rows)
```

*MySQL:* the same `DATE_FORMAT` swap as in Q71-028; it returns the same three rows.

**Extra-points moves demonstrated:** **[+Edge cases]** January's Industrial column shows 0, not a blank or an error: a real month with no Industrial sales, handled by the `ELSE 0` in each `CASE`. And leave a category out and its revenue silently disappears from the row total. **[+Trade-offs]** this only works for a category list known in advance, written into the query; a changing set of categories needs pivoting in the application or engine-specific dynamic SQL. **[+Validate]** each row's four columns add up to that month's total in Q71-028: January 1,72,240 + 30,400 = 2,02,640 ✓; February 1,50,231.50 + 54,152.50 + 49,280 = 2,53,664 ✓; March 1,80,785 + 49,335 + 31,500 + 16,387.50 = 2,78,007.50 ✓, and March only reconciles because the Furniture column is there.

**Likely follow-ups:** What if the list of categories isn't known ahead of time? How would you do this in a BI tool instead of raw SQL?
**Red flag:** reaching for a non-standard `PIVOT` keyword without checking whether the engine supports it.
**Learn it in:** Chapter 13, section 13.8 (Pattern 9, pivot rows into columns); Chapter 11, section 11.5 (pivot tables) for the spreadsheet version.

### Q71-076 · Walk-through: profile a table you've never seen before, in one query · *Core*

**What they're really testing:** whether you have a fast, repeatable first move for an unfamiliar table, rather than guessing or scrolling through raw rows.

**Talked through live:** "Before I write anything specific, I want a quick health check: the row count, how many NULLs in the columns that matter, the distinct count of what should be a key, and the date range. One query, several aggregates at once."

**Verified (riverstone_2025), on the `orders` table:**
```sql
SELECT
  COUNT(*)                                     AS total_rows,
  COUNT(*) - COUNT(sales_rep_id)               AS null_sales_rep,
  COUNT(DISTINCT customer_id)                  AS distinct_customers,
  MIN(order_date)                              AS earliest,
  MAX(order_date)                              AS latest,
  COUNT(*) FILTER (WHERE status = 'Cancelled') AS cancelled_count
FROM orders;
```
```
 total_rows | null_sales_rep | distinct_customers |  earliest  |   latest   | cancelled_count
------------+----------------+--------------------+------------+------------+-----------------
        175 |             11 |                 23 | 2025-01-02 | 2025-12-23 |               2
(1 row)
```

*MySQL:* there is no `FILTER`; count with `SUM(CASE … THEN 1 ELSE 0 END)` instead:
```mysql
SELECT
  COUNT(*)                                              AS total_rows,
  COUNT(*) - COUNT(sales_rep_id)                        AS null_sales_rep,
  COUNT(DISTINCT customer_id)                           AS distinct_customers,
  MIN(order_date)                                       AS earliest,
  MAX(order_date)                                       AS latest,
  SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_count
FROM orders;
```
```
+------------+----------------+--------------------+------------+------------+-----------------+
| total_rows | null_sales_rep | distinct_customers | earliest   | latest     | cancelled_count |
+------------+----------------+--------------------+------------+------------+-----------------+
|        175 |             11 |                 23 | 2025-01-02 | 2025-12-23 |               2 |
+------------+----------------+--------------------+------------+------------+-----------------+
```

**Extra-points moves demonstrated:** **[+Business]** this one query answers, in seconds, what would otherwise take five: is the table roughly the size I expect, is there missing data to account for, does the date range match what I was told, are there statuses (like Cancelled) to filter in every later query. **[+Signpost]** `COUNT(*) - COUNT(col)` as a NULL count and `COUNT(*) FILTER (WHERE ...)` as a conditional count are small idioms worth having memorized, not rebuilt each time. **[+Validate]** the 11 NULL `sales_rep_id` rows match the number Q71-002 found independently, a small consistency check that the profiling query itself can be trusted.

**Likely follow-ups:** How would you extend this to profile every column in a table automatically? What would you check differently for a table with no date column?
**Red flag:** starting with `SELECT * LIMIT 10` and eyeballing it as the only exploration step, with no aggregate health check at all.
**Learn it in:** Chapter 14, section 14.2 (profiling a new dataset); Chapter 13, section 13.8 (Pattern 10).

---

## 71.11 Predict the output: from basic to brain-racking

The hardest SQL round is not "write a query." It is a six-line query on the screen and one question: **what does this return?** You cannot hedge, you cannot talk around it, and the interviewer can see whether you know the rules or have been getting away with guessing.

Almost every question in this section turns on one of three things. SQL's NULL is not a value and does not behave like one. A join can quietly change how many rows you are aggregating. And a window function has a frame, whether or not you wrote one. Learn those three and the rest is arithmetic.

Work through these the way the round actually goes: read the query, say your answer out loud, *then* read on. An answer you guessed and an answer you reasoned to feel identical on the page and nothing like each other in the room.

**How these were verified.** Every output below was produced by running the query against `riverstone_2025` — the same 24-customer database the rest of this chapter uses — on **PostgreSQL 16.2**, so the figures agree with the numbers already printed earlier in the chapter and with the engine the chapter names. Four questions are marked **Dialect split**: PostgreSQL and MySQL genuinely disagree about them, and those four give each engine's documented behaviour rather than one printed result. Where a result depends on something the standard leaves to the engine, the question says so instead of pretending there is one right answer.

One reminder, because it is the single most useful fact in this section: in SQL, `NULL` means *unknown*. Any comparison with an unknown is itself unknown, and `WHERE` keeps a row only when its condition is **true** — not when it is unknown. Nearly every surprise below is that one sentence, wearing a different hat.

### Q71-077 · `count(*)`, `count(city)` and `count(DISTINCT city)` on the same column: what are the three numbers? · *Warm-up*

**Remember it as:** *`count(*)` counts rows. `count(col)` counts values that are not NULL. `count(DISTINCT col)` counts different values.*

**Answer in one line:** 24, 24 and 17: there are 24 customers, all 24 have a city recorded, but those 24 customers sit in only 17 different cities.

```sql
SELECT count(*) AS star, count(city) AS col, count(DISTINCT city) AS distinct_col
FROM customers;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
 star | col | distinct_col
------+-----+--------------
   24 |  24 |           17
(1 row)
```

The gap between 24 and 17 is the one people miss. `count(DISTINCT city)` is not "how many customers have a city" — it is "how many cities appear at all." Mumbai and Pune each have three customers, and Ahmedabad, Bengaluru and Delhi two each, which is where the seven duplicates go.

The gap between `star` and `col` is zero here only because this table happens to be complete. On a column with gaps the two diverge, and that divergence is the subject of most of this section.

| Tier | What to say |
|---|---|
| Passes | "`count(*)` counts rows and `count(col)` counts non-NULLs" (right rule, no numbers) |
| Strong | All three numbers with the reason for each, and the observation that `star = col` only tells you this particular column has no NULLs |
| Extra points | **[+Validate]** `count(*) - count(col)` is exactly the number of missing values in a column, which makes a one-line completeness check across a table · **[+Business]** 24 customers in 17 cities is a concentration fact a sales head would want to hear before a territory plan |

**Likely follow-ups:** Which is faster, `count(*)` or `count(1)`? *(No difference on any current engine; the planner treats them the same.)* What does `count(DISTINCT a, b)` do? How would you count the NULLs themselves? *(`count(*) - count(col)`, or `count(*) FILTER (WHERE col IS NULL)`.)*
**Red flag:** saying `count(*)` skips NULL rows. It counts rows; it never looks inside them.
**Learn it in:** Chapter 12, section 12.9 (aggregate functions); Chapter 12, section 12.7 (NULL).

### Q71-078 · `SELECT sum(quantity) FROM order_items WHERE quantity > 100000`: what does it return? · *Warm-up*

**Remember it as:** *`sum` of nothing is NULL, not zero. `count` of nothing is zero. The two aggregates disagree about emptiness.*

**Answer in one line:** `NULL`, not `0`: no row matches, and `sum` over an empty set has nothing to add up, so it returns NULL — while `count(*)` over the same empty set returns 0.

```sql
SELECT sum(quantity) AS total, count(*) AS rows_seen
FROM order_items
WHERE quantity > 100000;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
 total | rows_seen
-------+-----------
       |         0
(1 row)
```

That blank under `total` is a NULL. The largest quantity in the table is nowhere near 100,000, so nothing matches and the sum is undefined rather than empty-and-therefore-zero.

This is the bug that quietly breaks dashboards. A revenue tile for a region with no sales this month shows "—" instead of "₹0", or a calculation downstream touches the NULL and the whole figure disappears. The fix is one function:

```sql
SELECT coalesce(sum(quantity), 0) AS total
FROM order_items
WHERE quantity > 100000;
```
```
 total
-------
     0
(1 row)
```

`avg` behaves the same way: over zero rows it is NULL, and there is no sensible number it could return instead.

| Tier | What to say |
|---|---|
| Passes | "It returns NULL" |
| Strong | NULL for `sum` and `avg`, 0 for `count`, with the reason: an empty set has no total but it does have a row count of zero. Then `coalesce(sum(...), 0)` as the fix |
| Extra points | **[+Edge cases]** `sum` also returns NULL when rows *do* match but every matching value is NULL, which is a different cause with the same symptom · **[+Business]** wrap `sum` in `coalesce` in anything feeding a report, so an empty month reads ₹0 rather than blank · **[+Validate]** the two columns above prove the behaviour side by side in one query |

**Likely follow-ups:** What does `avg` return over no rows? Does `count(col)` return 0 or NULL? *(0.)* How would a NULL here affect a later `WHERE total > 0`? *(The row is dropped: unknown is not true.)*
**Red flag:** asserting `sum` returns 0 over an empty set. It is the most common wrong answer to this question and it is a real production bug.
**Learn it in:** Chapter 12, section 12.9 (aggregates); Chapter 12, section 12.7 (NULL); Chapter 14, section 14.3 (missing values).

### Q71-079 · 175 orders, 46 of them rep 3. Why does `WHERE sales_rep_id <> 3` return 118 and not 129? · *Core*

**Remember it as:** *`<>` keeps only rows it can prove are different. An unknown rep is not provably different from 3, so it is dropped — by both `= 3` and `<> 3`.*

**Answer in one line:** 11 orders have no sales rep recorded, and `NULL <> 3` is unknown rather than true, so those 11 rows fail both tests: 46 + 118 = 164, not 175, and the 11 unassigned orders fall through the gap between the two filters.

```sql
SELECT count(*)                                   AS all_orders,
       count(*) FILTER (WHERE sales_rep_id = 3)   AS rep_3,
       count(*) FILTER (WHERE sales_rep_id <> 3)  AS not_rep_3
FROM orders;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
 all_orders | rep_3 | not_rep_3
------------+-------+-----------
        175 |    46 |       118
(1 row)
```

Do the arithmetic the way a reviewer would. 175 − 46 = **129**. The query says **118**. The missing 11 are the orders whose `sales_rep_id` is NULL — the same 11 unassigned orders behind the `NOT IN` trap in Q71-002.

This is the most dangerous question in the section, because nothing fails. You get a number, it looks plausible, and it is wrong. An analyst asked "how many orders did someone other than rep 3 handle?" answers 118 and under-reports by 11 — and if the same report also counts rep 3's 46, the two figures do not reconcile to the total, which is the only clue anything is wrong.

The three ways to ask the question, and the three answers:

```sql
SELECT (SELECT count(*) FROM orders WHERE sales_rep_id <> 3)                         AS plain,
       (SELECT count(*) FROM orders WHERE sales_rep_id <> 3 OR sales_rep_id IS NULL) AS with_or_null,
       (SELECT count(*) FROM orders WHERE sales_rep_id IS DISTINCT FROM 3)           AS is_distinct_from;
```
```
 plain | with_or_null | is_distinct_from
-------+--------------+------------------
   118 |          129 |              129
(1 row)
```

`IS DISTINCT FROM` is the clean way to say "different, and treat unknown as different." It is one comparison instead of two, and it cannot be got subtly wrong the way an `OR` can when someone later adds an `AND` beside it.

| Tier | What to say |
|---|---|
| Passes | "NULLs are excluded" (correct, no numbers, no fix) |
| Strong | The arithmetic — 175 − 46 = 129 but the query says 118, so 11 rows satisfy neither filter — plus `IS DISTINCT FROM` or the explicit `OR ... IS NULL` |
| Extra points | **[+Validate]** the reconciliation itself is the test: if "is" plus "is not" does not add to the total, a nullable column is involved · **[+Trade-offs]** `IS DISTINCT FROM` is clearer than `OR ... IS NULL` but is spelled differently in MySQL, which uses `<=>` for the NULL-safe *equals* and therefore `NOT (a <=> b)` for this test · **[+Clarify]** ask the business whether "not rep 3" is meant to include unassigned orders at all; often the real answer is that they should be reported as their own line |

**Likely follow-ups:** Does the same thing happen with `>` and `<`? *(Yes: every comparison with NULL is unknown.)* What about `NOT LIKE`? *(Same.)* How would you catch this in review? *(Check that the positive and negative filters sum to the row count.)*
**Red flag:** "SQL treats NULL as zero" or "NULL is just an empty string." Neither is true, and a candidate who believes either will write this bug repeatedly.
**Learn it in:** Chapter 12, section 12.7 (NULL: the value that isn't there); Chapter 12, section 12.6 (WHERE).

### Q71-080 · Building a label with `||` when one piece is NULL: what comes out? · *Core* · **Dialect split**

**Remember it as:** *Concatenating anything onto an unknown gives an unknown. One NULL swallows the whole string.*

**Answer in one line:** The whole label is NULL, not the text with a gap in it: `||` propagates NULL, so a missing rep id erases the order number and the words around it too.

```sql
SELECT order_id,
       sales_rep_id,
       'Order ' || order_id || ' / rep ' || sales_rep_id AS label
FROM orders
WHERE sales_rep_id IS NULL
LIMIT 3;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
 order_id | sales_rep_id | label
----------+--------------+-------
    10015 |              |
    10036 |              |
    10038 |              |
(3 rows)
```

The `label` column is empty for every row. Not "Order 10015 / rep " — nothing at all. The literal text you typed is gone, because one unknown operand makes the whole expression unknown.

The repair names the gap instead of hiding it:

```sql
SELECT order_id,
       'Order ' || order_id || ' / rep ' || coalesce(sales_rep_id::text, 'unassigned') AS label
FROM orders
WHERE sales_rep_id IS NULL
LIMIT 3;
```
```
 order_id |            label
----------+------------------------------
    10015 | Order 10015 / rep unassigned
    10036 | Order 10036 / rep unassigned
    10038 | Order 10038 / rep unassigned
(3 rows)
```

Note the cast. `coalesce` needs both arguments to be the same type, and `sales_rep_id` is an integer while `'unassigned'` is text.

**Dialect split.** The same intent gives three different-looking answers:

| | Behaviour with a NULL argument |
|---|---|
| PostgreSQL `a \|\| b` | returns NULL |
| MySQL `CONCAT(a, b)` | returns NULL — same as PostgreSQL |
| MySQL `CONCAT_WS(sep, a, b)` | **skips** the NULL and returns the rest |

So a query ported from MySQL's `CONCAT_WS` to PostgreSQL's `||` changes behaviour silently: labels that used to be partially filled become entirely empty. MySQL does not have `||` as a concatenation operator at all by default — it reads `||` as logical OR unless `PIPES_AS_CONCAT` is set, which is its own portability trap.

| Tier | What to say |
|---|---|
| Passes | "You get NULL" |
| Strong | NULL for the whole expression, with the reason, plus `coalesce` and the cast it needs |
| Extra points | **[+Edge cases]** `CONCAT_WS` in MySQL skips NULLs, so the same report differs by engine · **[+Business]** a NULL label in a dropdown or an export shows as a blank row that nobody can click or trace, which is worse than the word "unassigned" · **[+Trade-offs]** `coalesce` at the point of display, not in the stored data: the fact that the rep is unknown is real and should not be overwritten |

**Likely follow-ups:** Does `CONCAT` behave differently from `||` in PostgreSQL? *(Yes — PostgreSQL's `CONCAT` ignores NULLs, unlike its `||`.)* What about `format()`? How would you find every such column before a release?
**Red flag:** expecting the literal text to survive. It does not, and a candidate who assumes it does has not watched this happen.
**Learn it in:** Chapter 12, section 12.8 (transforming values); Chapter 12, section 12.7 (NULL); Chapter 12, section 12.16 (the same SQL in MySQL).

### Q71-081 · `avg(sales_rep_id)` and `sum(sales_rep_id) / count(*)` on the same column: why do they differ? · *Core*

**Remember it as:** *`avg` divides by the count of values, not the count of rows. Hand-rolling it with `count(*)` changes the denominator.*

**Answer in one line:** `avg` ignores NULLs on both the top and the bottom, so it divides 674 by 164; dividing by `count(*)` divides the same 674 by 175 and gives a smaller, meaningless number.

```sql
SELECT avg(sales_rep_id)                  AS avg_builtin,
       sum(sales_rep_id) / count(*)       AS divided_by_all_rows,
       count(*)                           AS all_rows,
       count(sales_rep_id)                AS non_null
FROM orders;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
     avg_builtin     | divided_by_all_rows | all_rows | non_null
---------------------+---------------------+----------+----------
  4.1097560975609756 |                   3 |      175 |      164
(1 row)
```

**Read that second column again: it is `3`, not 3.85.** Two traps have fired at once, and the
second one is the subject of Q71-090 four questions from here. `sum(sales_rep_id)` is a `bigint`
and `count(*)` is a `bigint`, so PostgreSQL divides integer by integer and **truncates**: 674 ÷ 175
is 3.8514, and the column reports 3.

Force the division to be decimal and the number the question is about appears:

```sql
SELECT round(avg(sales_rep_id), 4)                        AS avg_builtin,
       round(sum(sales_rep_id)::numeric / count(*), 4)    AS divided_by_all_rows,
       count(*)                                           AS all_rows,
       count(sales_rep_id)                                AS non_null
FROM orders;
```

```
 avg_builtin | divided_by_all_rows | all_rows | non_null
-------------+---------------------+----------+----------
      4.1098 |              3.8514 |      175 |      164
(1 row)
```

674 ÷ 164 = 4.1098. 674 ÷ 175 = 3.8514. Same numerator, different denominator, and only the first
is the average of the values that exist.

So the hand-rolled version is wrong *twice*: wrong denominator, and then truncated to an integer on
the way out. That is worth saying out loud in an interview, because it is the honest shape of the
bug — these things rarely arrive one at a time.

Averaging a rep id is nonsense as a business figure — it is used here because it is this database's nullable numeric column, and the arithmetic is the point. The same mechanism decides a real one: the average order value across orders where some values are missing, or an average score where some candidates were not scored. Whether the denominator should be 164 or 175 is a *business* question, not a SQL one, and the two numbers differ by 6%.

| Tier | What to say |
|---|---|
| Passes | "`avg` ignores NULLs" |
| Strong | The two denominators, 164 and 175, named explicitly, the point that `avg` chose one of them for you, and that the hand-rolled version also truncates to `3` because both operands are integers |
| Extra points | **[+Clarify]** ask which denominator the business means: "average across orders that have a rep" and "average across all orders, counting unassigned as zero" are different questions with different answers · **[+Validate]** print `count(*)` and `count(col)` beside any average over a column that might have gaps · **[+Edge cases]** if every value is NULL, `avg` is NULL, not 0 and not an error |

**Likely follow-ups:** How would you get an average that treats missing as zero? *(`sum(col) / count(*)`, or `avg(coalesce(col, 0))`.)* Which is correct? *(Whichever the business asked for — say so.)* Does `avg` of an empty set error?
**Red flag:** reporting an average over a column with gaps without knowing the gaps are there.
**Learn it in:** Chapter 12, section 12.9 (aggregates); Chapter 14, section 14.3 (missing values).

### Q71-082 · The same LEFT JOIN, filtered in `WHERE` and then in `ON`: 1 row or 24? · *Core*

**Remember it as:** *`ON` decides what matches. `WHERE` decides what survives. A `WHERE` on the right-hand table deletes the unmatched rows a LEFT JOIN just went to the trouble of keeping.*

**Answer in one line:** 1 and 24: putting the status test in `WHERE` throws away every row where the join found no pending order, which turns the LEFT JOIN into an inner join, while putting it in `ON` keeps all 24 customers and simply shows no order for the 23 without one.

```sql
-- version A: the filter in WHERE
SELECT count(*) AS rows_kept
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.status = 'Pending';
```
```
 rows_kept
-----------
         1
(1 row)
```

```sql
-- version B: the same filter, moved into ON
SELECT count(*) AS rows_kept
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'Pending';
```
```
 rows_kept
-----------
        24
(1 row)
```

One pending order exists in the whole database, so version A returns a single row and version B returns all 24 customers with that one order attached to its customer and nothing attached to the other 23.

The mechanism is order of operations. The join runs first and produces the matched rows plus a NULL-filled row for every customer with no pending order. Then `WHERE o.status = 'Pending'` tests those NULL-filled rows: `NULL = 'Pending'` is unknown, not true, so they are all discarded. The LEFT JOIN did its job and the `WHERE` undid it.

Which one you want depends entirely on the question. "How many pending orders are there?" wants A. "Show me every customer and their pending order, if any" wants B — and B is the one people write A for by mistake.

There is exactly one condition on the right table that belongs in `WHERE`: `IS NULL` on its key, which is how you deliberately ask for the non-matches. That is the anti-join in Q71-001, and it works precisely *because* it tests for the NULL-filled rows instead of against them.

| Tier | What to say |
|---|---|
| Passes | "`WHERE` can turn a LEFT JOIN into an inner join" |
| Strong | Both counts, the order of operations that explains them, and which question each version answers |
| Extra points | **[+Edge cases]** the one legitimate right-table `WHERE` is `IS NULL` on its key, the anti-join · **[+Validate]** a LEFT JOIN whose result has fewer rows than the left table is the symptom; compare against `count(*)` from the left table alone · **[+Business]** version A answers a volume question and version B answers a coverage question; a "customers with no pending order" follow-up needs B plus `IS NULL` |

**Likely follow-ups:** What if the filter is on the left table instead? *(Then `WHERE` and `ON` agree, for a LEFT JOIN.)* Does this apply to RIGHT and FULL joins? *(Yes, mirrored.)* Rewrite B's intent as an aggregate per customer.
**Red flag:** believing `ON` and `WHERE` are interchangeable. They are, for an inner join, and that is exactly why the habit forms and then breaks on the first outer join.
**Learn it in:** Chapter 12, section 12.10 (JOIN); Chapter 12, section 12.11 (how the database reads your query).

### Q71-083 · On a LEFT JOIN, why does the customer with no orders show a count of 1? · *Core*

**Remember it as:** *`count(*)` counts the NULL-filled row too. `count(right_table_column)` does not.*

**Answer in one line:** The LEFT JOIN manufactures one row for a customer with no match, and `count(*)` counts that row, so the answer is 1 instead of 0; counting a column from the right table gives the correct 0, because that column is NULL in the manufactured row.

```sql
SELECT c.customer_name,
       count(*)          AS wrong,
       count(o.order_id) AS right_way
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_name
HAVING count(*) <= 1
ORDER BY c.customer_name;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
 customer_name | wrong | right_way
---------------+-------+-----------
 Home Plus     |     1 |         0
(1 row)
```

Home Plus is the one customer in this database who has never ordered — the same customer Q71-001 finds. The LEFT JOIN gives it one row with every `orders` column NULL. `count(*)` sees a row and says 1. `count(o.order_id)` looks at the value, finds NULL, and says 0.

A "orders per customer" report built with `count(*)` therefore reports every dormant customer as having one order. The error is small, uniform, and invisible: the number is never zero, so nobody notices that nobody is ever at zero.

The same rule explains why `HAVING count(*) = 0` never matches anything after a LEFT JOIN, and why the right way to find non-matches is `WHERE o.order_id IS NULL` before any grouping.

| Tier | What to say |
|---|---|
| Passes | "Use `count(column)` instead of `count(*)`" |
| Strong | The reason — the join manufactures a NULL-filled row and `count(*)` counts rows — plus both numbers, and which column to count (the right table's key) |
| Extra points | **[+Validate]** on a correct "activity per customer" report at least one customer should be at zero; if none is, suspect `count(*)` · **[+Edge cases]** `sum` of a right-table column over a non-match is NULL, not 0, which is the Q71-078 problem arriving by a different road · **[+Business]** dormant customers are usually the point of the report, so turning their 0 into a 1 destroys exactly the signal that was wanted |

**Likely follow-ups:** What does `count(DISTINCT o.order_id)` give here? *(0.)* What about `sum(oi.quantity)`? *(NULL.)* How do you list only the customers at zero?
**Red flag:** using `count(*)` after an outer join without noticing. It is the most common silent error in reporting SQL.
**Learn it in:** Chapter 12, section 12.10 (JOIN); Chapter 12, section 12.9 (GROUP BY and HAVING).

### Q71-084 · A self-join to show each employee's manager returns 4 rows from a 5-row table. Where did the fifth go? · *Core*

**Remember it as:** *The person at the top has no manager. An inner self-join has nothing to match her to, so it deletes the boss.*

**Answer in one line:** Anita Rao's `manager_id` is NULL because she runs the company, so the inner join finds no matching employee row for her and drops her — the classic way a hierarchy report loses its own root.

```sql
SELECT count(*) AS inner_join_rows
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id;
```
```
 inner_join_rows
-----------------
               4
(1 row)
```

Five employees in, four out. The missing row is the one the organisation chart most obviously needs.

```sql
SELECT e.employee_name,
       coalesce(m.employee_name, '(nobody)') AS reports_to
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY e.employee_id;
```
```
 employee_name | reports_to
---------------+--------------
 Anita Rao     | (nobody)
 Vikram Singh  | Anita Rao
 Neha Kulkarni | Vikram Singh
 Rahul Mehta   | Vikram Singh
 Farah Khan    | Anita Rao
(5 rows)
```

A LEFT JOIN plus `coalesce` keeps all five and labels the root honestly. Note also that the two aliases are doing real work: `e` is the employee and `m` is the manager, and the same table is playing both parts. Q71-014 covers what happens when you forget to give them different names.

This generalises past org charts to every parent-child structure: a category tree whose top-level categories have no parent, a comment thread whose first comment replies to nothing, an account hierarchy whose holding company sits above everything. In each case the inner join silently removes the top of the tree.

| Tier | What to say |
|---|---|
| Passes | "The join drops the top-level employee" |
| Strong | 4 against 5, named — Anita Rao, `manager_id` NULL — with the LEFT JOIN plus `coalesce` fix and the two-alias point |
| Extra points | **[+Validate]** row count out must equal row count in for a report that claims to list every employee · **[+Scale]** this shows only one level; a full hierarchy of unknown depth needs a recursive CTE, which is Q71-029 · **[+Edge cases]** a cycle in the data (two employees managing each other) breaks the recursive version and needs a depth guard |

**Likely follow-ups:** How would you show the whole chain to the top for any employee? *(Recursive CTE — Chapter 28, section 28.2.)* What if someone's manager has left and the id now points nowhere? How would you find employees with no reports?
**Red flag:** not noticing the count dropped. The query runs, returns rows, and looks right.
**Learn it in:** Chapter 12, section 12.10 (JOIN); Chapter 28, section 28.2 (recursive CTEs).

### Q71-085 · `GROUP BY` on a column with 11 NULLs: how many groups come back? · *Core*

**Remember it as:** *`GROUP BY` puts all the NULLs in one group together, even though no NULL equals any other NULL.*

**Answer in one line:** Four — one for each of the three reps plus a single group holding all 11 unassigned orders, because `GROUP BY` treats NULLs as *not distinct from each other* even though `=` says otherwise.

```sql
SELECT sales_rep_id, count(*) AS orders
FROM orders
GROUP BY sales_rep_id
ORDER BY sales_rep_id;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
 sales_rep_id | orders
--------------+--------
            3 |     46
            4 |     54
            5 |     64
              |     11
(4 rows)
```

46 + 54 + 64 + 11 = 175, the full table. Unlike nearly every other question in this section, `GROUP BY` loses nothing: the NULLs get their own group rather than being discarded.

This is worth holding onto precisely because it cuts against the pattern. `WHERE` drops unknowns. `<>` drops unknowns. `NOT IN` collapses on one unknown. But `GROUP BY` gathers them up, and so do `DISTINCT` and `UNION`. The rule those three follow is "not distinct from", which is the `IS DISTINCT FROM` logic of Q71-079, not the `=` logic of everything else.

The practical consequence is that a per-rep report has a nameless fourth row. Label it rather than letting it appear as a blank:

```sql
SELECT coalesce(sales_rep_id::text, 'unassigned') AS rep, count(*) AS orders
FROM orders
GROUP BY sales_rep_id
HAVING count(*) > 10
ORDER BY orders DESC;
```
```
    rep     | orders
------------+--------
 5          |     64
 4          |     54
 3          |     46
 unassigned |     11
(4 rows)
```

Grouping by `sales_rep_id` and selecting the `coalesce` of it is deliberate: group on the real column, label at the point of display.

| Tier | What to say |
|---|---|
| Passes | "You get an extra row for the NULLs" |
| Strong | Four groups, the counts, the fact that they reconcile to 175, and the "not distinct from" rule that `GROUP BY`, `DISTINCT` and `UNION` share |
| Extra points | **[+Validate]** the group counts summing to `count(*)` proves no rows were lost, which is the check that would have caught Q71-079 · **[+Business]** 11 unassigned orders out of 175 is 6% of the book with no owner: a finding, not a footnote · **[+Edge cases]** `GROUP BY` on two columns groups on the combination, and a NULL in either still groups rather than vanishing |

**Likely follow-ups:** Does `DISTINCT` keep one NULL or none? *(One.)* Does `UNION` deduplicate NULLs against each other? *(Yes.)* Why does `GROUP BY` disagree with `=` about NULL?
**Red flag:** expecting three groups. It suggests a candidate has internalised "NULLs disappear" as a universal rule rather than a property of comparison.
**Learn it in:** Chapter 12, section 12.9 (GROUP BY); Chapter 12, section 12.7 (NULL).

### Q71-086 · `ORDER BY manager_id` on a column with one NULL: does the NULL come first or last? · *Core* · **Dialect split**

**Remember it as:** *PostgreSQL sorts NULL as the largest value. MySQL sorts it as the smallest. Same query, opposite first row.*

**Answer in one line:** It depends on the engine, and this is one of the few places where PostgreSQL and MySQL give flatly opposite answers to identical SQL: ascending, PostgreSQL puts the NULL **last** and MySQL puts it **first**.

```sql
SELECT employee_id, employee_name, manager_id
FROM employees
ORDER BY manager_id;
```

**PostgreSQL 16** — NULLs sort as though larger than any value, so ascending puts them at the end:
```
 employee_id | employee_name | manager_id
-------------+---------------+------------
           2 | Vikram Singh  |          1
           5 | Farah Khan    |          1
           3 | Neha Kulkarni |          2
           4 | Rahul Mehta   |          2
           1 | Anita Rao     |
(5 rows)
```

**MySQL 8.4** — NULLs sort as though smaller than any value, so ascending puts them first:
```
+-------------+---------------+------------+
| employee_id | employee_name | manager_id |
+-------------+---------------+------------+
|           1 | Anita Rao     |       NULL |
|           2 | Vikram Singh  |          1 |
|           5 | Farah Khan    |          1 |
|           3 | Neha Kulkarni |          2 |
|           4 | Rahul Mehta   |          2 |
+-------------+---------------+------------+
```

Both are permitted. The SQL standard leaves NULL ordering to the implementation, so neither engine is wrong and a query that relies on either is not portable.

It matters more than a tidiness point, because `ORDER BY` plus `LIMIT` is how a "top 5" is written. On the engine that sorts NULLs first, an ascending top-5 can be five rows of nothing at all.

Say what you want explicitly. PostgreSQL has the direct form:

```sql
SELECT employee_id, manager_id FROM employees ORDER BY manager_id NULLS FIRST;
```

MySQL has no `NULLS FIRST`, so the portable form — which works identically on both — sorts on a boolean first:

```sql
SELECT employee_id, manager_id FROM employees ORDER BY manager_id IS NULL, manager_id;
```
```
 employee_id | manager_id
-------------+------------
           2 |          1
           5 |          1
           3 |          2
           4 |          2
           1 |
(5 rows)
```

`manager_id IS NULL` is false (0) for the rows with a manager and true (1) for the row without, so sorting on it ascending puts the real values first on either engine. Reverse it with `IS NULL DESC` for the other arrangement.

| Tier | What to say |
|---|---|
| Passes | "It depends on the database" |
| Strong | Which way each engine goes, that the standard permits both, and the portable `ORDER BY col IS NULL, col` form |
| Extra points | **[+Edge cases]** `ORDER BY` plus `LIMIT` on a nullable column can return an all-NULL top-N on MySQL · **[+Trade-offs]** `NULLS FIRST`/`NULLS LAST` is clearer where you only target PostgreSQL; the boolean form is the one to use in anything that has to run on both · **[+Validate]** an index on the column may or may not be usable depending on the null ordering you ask for, which is worth an `EXPLAIN` on a large table |

**Likely follow-ups:** What about `DESC`? *(Each engine reverses, so PostgreSQL puts NULLs first and MySQL last.)* Does `NULLS FIRST` work in MySQL? *(No.)* How does this interact with an index?
**Red flag:** asserting one answer confidently without naming an engine. The whole point of the question is that there is no single answer.
**Learn it in:** Chapter 12, section 12.5 (ORDER BY and LIMIT); Chapter 12, section 12.16 and Chapter 13, section 13.9 (the same SQL in MySQL).

### Q71-087 · A running total over a column with ties: why does it stall at 68 for three months in a row? · *Brain-racking*

**Remember it as:** *A window with an `ORDER BY` and no frame gets `RANGE`, which treats tied rows as one. Ties share a total. Write `ROWS` when you want one row at a time.*

**Answer in one line:** The default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, and under `RANGE` "current row" means *every row tied with the current row*, so the three months that all have 13 orders are treated as a single step and all three report the same cumulative 68.

This is the question that separates people who have read about window functions from people who have debugged one.

```sql
WITH monthly AS (
  SELECT date_trunc('month', order_date)::date AS month, count(*) AS orders
  FROM orders
  GROUP BY 1
)
SELECT to_char(month, 'YYYY-MM') AS month,
       orders,
       sum(orders) OVER (ORDER BY orders) AS running
FROM monthly
ORDER BY orders, month;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
  month  | orders | running
---------+--------+---------
 2025-01 |      8 |       8
 2025-02 |     10 |      18
 2025-03 |     11 |      29
 2025-04 |     13 |      68
 2025-06 |     13 |      68
 2025-07 |     13 |      68
 2025-08 |     14 |      82
 2025-05 |     15 |      97
 2025-09 |     18 |     133
 2025-12 |     18 |     133
 2025-10 |     21 |     175
 2025-11 |     21 |     175
(12 rows)
```

Look at what happens at every tie. Three months have 13 orders, and all three show 68 — which is 29 + 13 + 13 + 13, the total *through the end of the tie group*, not through each row. The same at 18 (September and December both show 133) and at 21 (October and November both show 175). The column jumps 29 → 68 in one step and never shows 42 or 55 at all.

Nothing is broken. `RANGE` works on *values*, not positions: the frame is "every row whose `orders` value is less than or equal to mine", and all three 13s qualify for each other. Asking for `ROWS` instead changes the question to "every row up to and including my position":

```sql
       sum(orders) OVER (ORDER BY orders
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running
```
**Verified (riverstone_2025, PostgreSQL 16):**
```
  month  | orders | running
---------+--------+---------
 2025-01 |      8 |       8
 2025-02 |     10 |      18
 2025-03 |     11 |      29
 2025-04 |     13 |      42
 2025-06 |     13 |      68
 2025-07 |     13 |      55
 2025-08 |     14 |      82
 2025-05 |     15 |      97
 2025-09 |     18 |     133
 2025-12 |     18 |     115
 2025-10 |     21 |     175
 2025-11 |     21 |     154
(12 rows)
```

Now it increments one row at a time — 42, 55, 68 — and the column no longer stalls.

**But look at which month got which.** The running totals climb 42, 68, 55 down the page, not 42,
55, 68, and September shows 133 while December shows 115. The totals are right; the *order they are
attached to* is not the order the rows are displayed in.

That is not a misprint, and it is the whole second half of this question.

**One more turn of the screw.** Under `ROWS`, *which* of the three tied months gets 42 and which
gets 68 is not determined by anything you wrote. The engine may order tied rows however it likes,
so that assignment can change between runs, between versions, and between engines. This very table
is the proof: run on another engine it came out 42, 55, 68 in display order, and on PostgreSQL 16
it comes out as printed above. Same query, same data, both correct, different answer. If you want `ROWS` and you have ties, you must break the tie inside the window:

```sql
       sum(orders) OVER (ORDER BY orders, month
                         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running
```

With `month` as a tiebreak the result above is reproducible — and note that adding the tiebreak also makes `RANGE` and `ROWS` agree, because once no two rows tie there are no peer groups left for them to disagree about.

The practical lesson is short. Order a running total by something unique — a date, an id — and the default frame never bites. Order it by a measure that can tie, and you must choose a frame deliberately.

| Tier | What to say |
|---|---|
| Passes | "There's something about the window frame" |
| Strong | Names the default as `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`, explains that `RANGE` includes all peers of the current row, and reads the actual numbers off both versions |
| Extra points | **[+Edge cases]** under `ROWS` with ties the per-row assignment is engine-determined, so a tiebreak in the window's `ORDER BY` is required for a reproducible answer · **[+Validate]** both versions must end at the same grand total, 175, which is the check that the frame is the only difference · **[+Trade-offs]** `RANGE` is the right default for "cumulative through this value" questions such as a price percentile; `ROWS` is right for "cumulative through this row" such as a ledger balance · **[+Scale]** `RANGE` has to identify peer groups and is generally slower than `ROWS` on a large partition |

**Likely follow-ups:** What is the default frame when there is no `ORDER BY` in the window? *(The whole partition — which is why `sum(x) OVER ()` gives a grand total.)* What does `RANGE BETWEEN INTERVAL '7 days' PRECEDING AND CURRENT ROW` do on a date column? Does `ROW_NUMBER` care about the frame? *(No — ranking functions ignore the frame.)*
**Red flag:** insisting the output is a bug. It is documented, standard behaviour, and a candidate who calls it broken will not find it in their own code.
**Learn it in:** Chapter 13, section 13.3 (window functions); Chapter 28, section 28.3 (advanced window frames).

### Q71-088 · `ORDER BY count(*) DESC LIMIT 5` on the busiest order days: is the answer reliable? · *Brain-racking*

**Remember it as:** *A `LIMIT` is only as deterministic as its `ORDER BY`. If rows tie at the cut-off, which ones you get is arbitrary.*

**Answer in one line:** No: one day has 4 orders and **five** days have 3, so a top-5 has to pick four of those five tied days, and nothing in the query says which four — the result can differ between runs and between engines without any of them being wrong.

```sql
SELECT order_date, count(*) AS orders
FROM orders
GROUP BY order_date
ORDER BY count(*) DESC
LIMIT 5;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
 order_date | orders
------------+--------
 2025-06-10 |      4
 2025-05-04 |      3
 2025-11-09 |      3
 2025-07-26 |      3
 2025-11-16 |      3
(5 rows)
```

The shape of the tie, which is what makes the answer unsafe:

```sql
WITH d AS (SELECT order_date, count(*) AS n FROM orders GROUP BY order_date)
SELECT n AS orders_that_day, count(*) AS how_many_days
FROM d GROUP BY n ORDER BY n DESC;
```
```
 orders_that_day | how_many_days
-----------------+---------------
               4 |             1
               3 |             5
               2 |            29
               1 |            98
(4 rows)
```

One day at 4, five days at 3. The top-5 takes the 4 and then four of the five 3s, leaving one out for no stated reason. Re-run it after the data changes, or run it on a different engine, and a different day may be the one omitted — while the report still says "top 5 busiest days" with a straight face.

Two ways out, and they answer different questions:

```sql
-- A: make it deterministic. Still 5 rows, but always the same 5.
ORDER BY count(*) DESC, order_date
LIMIT 5;
```

```sql
-- B: include the whole tie. May return more than 5 rows, and should.
SELECT order_date, orders FROM (
  SELECT order_date, count(*) AS orders,
         rank() OVER (ORDER BY count(*) DESC) AS rnk
  FROM orders GROUP BY order_date
) t
WHERE rnk <= 5
ORDER BY orders DESC, order_date;
```

Version A is honest but arbitrary: it picks by date because something has to pick, and at least it picks the same way every time. Version B says what a business person usually means by "the top days" — if five days tie for second place, all five are in the answer. `rank()` is the right function here precisely because it shares a rank among ties, which is Q71-034's distinction put to work.

Worth saying out loud in the interview: *this is a question about the data, not just the query.* You cannot tell whether a top-N is safe without checking whether anything ties at the boundary, which is a one-line check nobody runs.

| Tier | What to say |
|---|---|
| Passes | "Ties make `LIMIT` unpredictable" |
| Strong | The tie structure — one day at 4, five at 3 — and both fixes, with the point that a deterministic tiebreak and including the whole tie are different answers to different questions |
| Extra points | **[+Validate]** before trusting any top-N, count how many rows sit at the boundary value · **[+Business]** dropping one of five equally busy days from an operations report is the kind of error that is never caught because the output always looks plausible · **[+Edge cases]** the same applies to `ROW_NUMBER() = 1` for "the latest row per group": with two rows at the same timestamp, which one you get is arbitrary |

**Likely follow-ups:** How would you return exactly 5 rows but choose the tie fairly? Does `FETCH FIRST 5 ROWS WITH TIES` help? *(Yes where supported — PostgreSQL 13+; MySQL has no equivalent.)* What is the cost of the window-function version on a large table?
**Red flag:** treating the printed five rows as *the* answer. The query does not have one answer, and saying so is the whole point.
**Learn it in:** Chapter 12, section 12.5 (ORDER BY and LIMIT); Chapter 13, section 13.4 (RANK and DENSE_RANK).

### Q71-089 · `SELECT 10 / 0`: what happens? · *Brain-racking* · **Dialect split**

**Remember it as:** *PostgreSQL raises an error and takes the transaction with it. MySQL returns NULL and carries on. Same expression, different blast radius.*

**Answer in one line:** PostgreSQL raises `division by zero` and the statement fails — inside a transaction, that aborts it — while MySQL returns NULL without complaint, which means the same ETL step either stops loudly or produces quiet nonsense depending on the engine.

**PostgreSQL 16:**
```
ERROR:  division by zero
```

**MySQL 8.4:**
```
+-----------+
| 10 / 0    |
+-----------+
|      NULL |
+-----------+
```

MySQL's behaviour follows from its default `ERROR_FOR_DIVISION_BY_ZERO` handling in `sql_mode`; with strict mode configured to raise, it errors instead. So "MySQL returns NULL" is a statement about a default, not about the engine forever — worth saying, because it shows you know the behaviour is configurable rather than fundamental.

Neither default is good news in a report. An error at least tells you something is wrong. A NULL flows downstream, lands in a percentage column, and reads as a missing figure rather than an impossible one.

The guard is the same on both engines, and it is what the interviewer is listening for:

```sql
SELECT round(100.0 * delivered / nullif(total, 0), 1) AS pct_delivered
FROM (
  SELECT count(*) FILTER (WHERE status = 'Delivered') AS delivered,
         count(*)                                      AS total
  FROM orders
) t;
```

`nullif(total, 0)` turns a zero denominator into NULL *before* the division, so the result is NULL by your decision rather than by an error or an engine default. Pair it with `coalesce` if the report should read 0% rather than blank — but only if 0% is actually true, which for "percentage of nothing" it usually is not.

This is the single most common guard in production analytics SQL. A denominator that is non-zero in every test dataset becomes zero the first week a new region launches with no orders yet.

| Tier | What to say |
|---|---|
| Passes | "You should guard against dividing by zero" |
| Strong | Both behaviours named by engine, that MySQL's depends on `sql_mode`, and `nullif(denominator, 0)` as the portable guard |
| Extra points | **[+Edge cases]** in PostgreSQL inside a transaction the error aborts everything after it, so one bad row can roll back a whole batch load · **[+Business]** a new region with no orders yet is the usual trigger, and it arrives in production rather than in test · **[+Trade-offs]** `nullif` then `coalesce` to 0 only when zero is the honest answer; "no data" and "zero percent" are different facts |

**Likely follow-ups:** What about `0 / 0`, or modulo by zero? What does a `NUMERIC` versus `FLOAT` division do differently? *(Floating-point division by zero can give infinity rather than an error, depending on type and engine.)* How would you find every unguarded division in a codebase?
**Red flag:** confident that it errors everywhere, or that it returns NULL everywhere. It is exactly the sort of question where one answer marks you as having used one database and assumed it was SQL.
**Learn it in:** Chapter 12, section 12.8 (transforming values); Chapter 12, section 12.16 and Chapter 13, section 13.9 (MySQL differences).

### Q71-090 · `SELECT 7 / 2`: does it give 3 or 3.5? · *Brain-racking* · **Dialect split**

**Remember it as:** *PostgreSQL keeps integer division integer and gives 3. MySQL converts and gives 3.5. The decimal point moves when you change database.*

**Answer in one line:** PostgreSQL returns **3**, because dividing an integer by an integer produces an integer and the remainder is discarded; MySQL returns **3.5000**, because it converts to a decimal first — and the same report therefore differs by engine.

**PostgreSQL 16:**
```
 ?column?
----------
        3
(1 row)
```

**MySQL 8.4:**
```
+--------+
| 7 / 2  |
+--------+
| 3.5000 |
+--------+
```

PostgreSQL is following the SQL standard here: the result type of `integer / integer` is integer, and 3.5 is not one, so the remainder is discarded. Note that it **truncates rather than rounds**: `7 / 2` is 3, not the 4 you would get by rounding 3.5. The two differ by one whenever there is a remainder of a half or more, so a figure computed this way is not even reliably the nearest whole number.

The fix is to make at least one operand non-integer, and there are three common spellings:

```sql
SELECT 7.0 / 2        AS decimal_literal,   -- 3.5
       7::numeric / 2 AS cast_numeric,      -- 3.5
       7 * 1.0 / 2    AS multiply_first;    -- 3.5
```

The one that bites in real work is a percentage:

```sql
SELECT count(*) FILTER (WHERE status = 'Cancelled') / count(*) AS wrong,
       100.0 * count(*) FILTER (WHERE status = 'Cancelled') / count(*) AS right_way
FROM orders;
```

**PostgreSQL 16** — the integer division happens before anything else can save it:
```
 wrong |     right_way
-------+--------------------
     0 | 1.1428571428571429
(1 row)
```

Two cancelled orders out of 175 is 1.14%. The integer version reports **0** — not "about 1%", not a rounding error, but zero, which reads as "no cancellations at all." Every rate below 50% truncates to 0 this way, so the bug is invisible on good data and catastrophic on the exact figure a manager asked for.

On MySQL the same query returns 0.0114 in the `wrong` column rather than 0, because it converts instead of truncating. That is not a reprieve: the column is then a fraction where a percentage was intended, which is wrong by a factor of a hundred rather than wrong by everything. Both engines need the `100.0`.

Put the `100.0` at the front, before the division, and the whole expression is decimal from the start.

| Tier | What to say |
|---|---|
| Passes | "Integer division truncates" |
| Strong | 3 on PostgreSQL, 3.5 on MySQL, that truncation is toward zero rather than rounding, and a fix that makes one operand decimal |
| Extra points | **[+Business]** every rate under 50% becomes 0, so a cancellation rate, a conversion rate or a margin silently reads as nothing · **[+Validate]** the two columns above side by side, 0 against 1.14%, on real data · **[+Edge cases]** `-7 / 2` is −3 in PostgreSQL, truncating toward zero rather than toward negative infinity, which differs from Python's `//` · **[+Trade-offs]** `100.0 *` first rather than casting afterwards: casting the already-truncated result cannot recover the lost remainder |

**Likely follow-ups:** How do you get the remainder? *(`%` or `mod()`.)* What does `-7 / 2` give, and how does that compare with Python? What is `div` in MySQL? *(Explicit integer division, the opposite problem.)*
**Red flag:** "SQL always returns a decimal." Half the engines do not, and the half that do not include the one most analytics runs on.
**Learn it in:** Chapter 12, section 12.8 (transforming values); Chapter 12, section 12.16 (the same SQL in MySQL).

### Q71-091 · `sum(count(*)) OVER ()` beside a `GROUP BY`: is that even legal? · *Brain-racking*

**Remember it as:** *Aggregates run first, window functions run after. So a window function can take an aggregate as its input, and that is how you get a share-of-total in one pass.*

**Answer in one line:** Yes, it is legal and it is the idiomatic way to compute each group's share of the whole: the `GROUP BY` collapses the rows first, and the window function then runs over those already-aggregated rows, so `sum(count(*)) OVER ()` is "the total of all the group counts."

```sql
SELECT segment,
       count(*)                                              AS in_segment,
       sum(count(*)) OVER ()                                 AS all_customers,
       round(100.0 * count(*) / sum(count(*)) OVER (), 1)    AS pct
FROM customers
GROUP BY segment
ORDER BY segment;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
   segment   | in_segment | all_customers | pct
-------------+------------+---------------+------
 Hospitality |          9 |            24 | 37.5
 Retail      |          9 |            24 | 37.5
 Wholesale   |          6 |            24 | 25.0
(3 rows)
```

Most candidates say this errors, and the instinct is understandable: "you can't nest aggregates" is a real rule, and `sum(count(*))` looks exactly like nesting. It is not. The two run in different phases. `count(*)` is computed as part of the `GROUP BY`, producing three rows; `sum(... ) OVER ()` is then evaluated across those three rows, in the window phase that comes after grouping. `sum(sum(x))` would be the illegal version — two aggregates in the *same* phase.

The payoff is that a share-of-total needs no subquery, no CTE and no second scan of the table. The alternative people reach for first is strictly more work:

```sql
-- the same answer, the long way
WITH per_segment AS (
  SELECT segment, count(*) AS in_segment FROM customers GROUP BY segment
)
SELECT segment, in_segment,
       round(100.0 * in_segment / (SELECT sum(in_segment) FROM per_segment), 1) AS pct
FROM per_segment ORDER BY segment;
```

Note the `100.0`, for the reason Q71-090 just gave: written as `100 *` with integer inputs, every percentage here would be 0 or 1.

The empty `OVER ()` is doing specific work. No `PARTITION BY` means one partition containing every row, and no `ORDER BY` means the frame is the whole partition — so it is a grand total. Add `PARTITION BY region` and you get share-within-region instead, which is the same idiom one step up.

| Tier | What to say |
|---|---|
| Passes | "I think that errors" (the common answer, and wrong) |
| Strong | Legal, with the phase argument: `GROUP BY` aggregates first, window functions run over the grouped rows, so this is not nesting — and reads the percentages off |
| Extra points | **[+Scale]** one pass instead of the CTE-plus-subquery version, and no second scan · **[+Edge cases]** `sum(sum(x))` *is* illegal, because both are in the aggregate phase; the legality comes entirely from `OVER ()` moving the outer one to a later phase · **[+Business]** share-of-total is what nearly every management report actually wants, and this is the one-line form · **[+Validate]** the `pct` column should sum to 100, allowing for rounding: 37.5 + 37.5 + 25.0 = 100.0 ✓ |

**Likely follow-ups:** What does `PARTITION BY` change here? What is the default frame with no `ORDER BY`? *(The whole partition.)* Can you use a window function in `WHERE`? *(No — `WHERE` runs before the window phase; wrap it in a subquery or use `QUALIFY` where supported.)*
**Red flag:** "you can never put an aggregate inside another function." The rule is about phases, not about syntax, and this is the question that tests whether a candidate knows which.
**Learn it in:** Chapter 13, section 13.3 (window functions); Chapter 13, section 13.7 (patterns for ranking and shares); Chapter 12, section 12.11 (how the database reads your query).

### Q71-092 · `WHERE city NOT IN ('Mumbai', NULL)`: how many rows? · *Core*

**Remember it as:** *A literal NULL in a `NOT IN` list is the same trap as a NULL from a subquery. Zero rows, every time, silently.*

**Answer in one line:** Zero — not the 21 non-Mumbai customers — because `NOT IN` requires the row to be provably different from *every* list member, and nothing is provably different from NULL; meanwhile plain `IN` with the same list returns the 3 Mumbai customers quite happily.

```sql
SELECT (SELECT count(*) FROM customers WHERE city IN ('Mumbai', NULL))     AS in_list,
       (SELECT count(*) FROM customers WHERE city NOT IN ('Mumbai', NULL)) AS not_in_list,
       (SELECT count(*) FROM customers WHERE city = 'Mumbai')              AS plain_equals;
```

**Verified (riverstone_2025, PostgreSQL 16):**
```
 in_list | not_in_list | plain_equals
---------+-------------+--------------
       3 |           0 |            3
(1 row)
```

The asymmetry is the lesson. `IN` is a chain of `OR`s: `city = 'Mumbai' OR city = NULL`. For a Mumbai customer the first test is true, and true-OR-unknown is true, so the row is kept — the NULL in the list is harmless. `NOT IN` is a chain of `AND`s: `city <> 'Mumbai' AND city <> NULL`. The second test is unknown for *every* row, and anything-AND-unknown is never true, so every row is rejected.

So one NULL in the list is invisible to `IN` and fatal to `NOT IN`. Q71-002 showed this arriving from a subquery, which is how it happens in production; this version shows it written down in plain sight, which is how it appears in an interview. Both have the same cause and the same two fixes: filter the NULLs out of the list, or use `NOT EXISTS`, which asks whether a matching row exists rather than comparing against a list.

A literal NULL in a hand-written list looks contrived until you have seen a list built by a code generator, a reporting tool's "selected values" parameter, or a string of ids pasted from a spreadsheet with one blank cell in it.

| Tier | What to say |
|---|---|
| Passes | "`NOT IN` with a NULL returns nothing" |
| Strong | Zero against 3, with the `AND`-chain versus `OR`-chain explanation for why `NOT IN` breaks and `IN` does not |
| Extra points | **[+Edge cases]** the asymmetry is the memorable part: the same NULL is harmless in `IN` and fatal in `NOT IN` · **[+Trade-offs]** `NOT EXISTS` is immune by construction and is the better default · **[+Validate]** "is" plus "is not" failing to reconcile to the row count is the same symptom as Q71-079 |

**Likely follow-ups:** Rewrite it safely. Does `NOT IN` against an *empty* subquery return everything or nothing? *(Everything — there is nothing to fail against.)* What about `ALL` and `ANY`? *(`<> ALL` has the identical problem.)*
**Red flag:** answering 21. It is the arithmetic answer and it is the one the trap is built to extract.
**Learn it in:** Chapter 12, section 12.7 (NULL); Chapter 12, section 12.12 (subqueries and set operations).

### Rapid-fire, §71.11, part A: predict the output, warm-up to core

Say the answer before you read it. Every figure below was run on `riverstone_2025`.

| # | Query | What it returns, and why | Extra point |
|---|---|---|---|
| Q71-093 | `SELECT NULL = NULL;` | NULL, not true: an unknown compared with an unknown is unknown. Use `IS NULL` | **[+Edge cases]** `NULL IS NULL` *is* true; it is the only test that works → Ch 12 §12.7 |
| Q71-094 | `SELECT count(*) FROM orders WHERE sales_rep_id = NULL;` | 0 rows, no error: the condition is unknown for all 175 rows, including the 11 that are NULL | **[+Validate]** 0 where you expected 11 is the signature of `= NULL` → Ch 12 §12.7 |
| Q71-095 | `SELECT sum(sales_rep_id) FROM orders WHERE sales_rep_id IS NULL;` | NULL, with `count(*)` on the same rows giving 11: eleven rows matched, none had a value to add | **[+Edge cases]** `sum` is NULL both when no rows match and when no values do; the symptom hides two causes → Ch 12 §12.9 |
| Q71-096 | `SELECT count(CASE WHEN city = 'Mumbai' THEN 1 END) FROM customers;` | 3, not 24: `CASE` with no `ELSE` returns NULL for non-matches, and `count` skips NULLs. This is the conditional-count idiom | **[+Trade-offs]** `count(*) FILTER (WHERE ...)` is clearer in PostgreSQL; `CASE` is the portable spelling → Ch 12 §12.8 |
| Q71-097 | `SELECT sum(CASE WHEN city = 'Mumbai' THEN 1 ELSE 0 END) FROM customers;` | 3 as well, by a different route: `ELSE 0` makes every row contribute, and the zeros add nothing | **[+Edge cases]** drop the `ELSE 0` and `sum` still gives 3, since it skips the NULLs — but it returns NULL instead of 0 when nothing matches → Ch 12 §12.8 |
| Q71-098 | `SELECT count(*) FROM orders o JOIN order_items i ON i.order_id = o.order_id;` | 330, not 175: each order has several lines, so joining multiplies the order rows. `count(DISTINCT o.order_id)` is still 175 | **[+Validate]** a row count that rises after a join is fan-out; any `sum` of an order-level column is now inflated → Ch 12 §12.10 |
| Q71-099 | `SELECT count(DISTINCT segment) FROM customers;` where one segment is NULL | Counts only the real segments; `DISTINCT` in `count` skips NULL even though `GROUP BY` would give it a group. (No NULL segments in this database: the rule, not a run) | **[+Edge cases]** `count(DISTINCT col)` and `GROUP BY col` disagree about NULL by exactly one group → Ch 12 §12.9 |
| Q71-100 | `SELECT 'abc' = 'abc  ';` | False in PostgreSQL for `varchar`; **true** in MySQL's default collation, which ignores trailing spaces. `CHAR(n)` pads and compares equal on both | **[+Edge cases]** a join key with a stray trailing space matches on one engine and not the other → Ch 12 §12.16 |
| Q71-101 | `SELECT count(*) FROM customers GROUP BY segment;` | Three rows (9, 9, 6), not one: `GROUP BY` returns one row per group, so a bare `count(*)` is a count *per segment* | **[+Business]** reading only the first row of a grouped result is how a segment total gets reported as a company total → Ch 12 §12.9 |
| Q71-102 | `SELECT segment, count(*) FROM customers GROUP BY 1 ORDER BY 2 DESC;` | Works: `1` and `2` are ordinal positions in the select list, not literals. Returns 9, 9 and 6 — but Hospitality and Retail both have 9, so which of the two comes first is arbitrary | **[+Trade-offs]** fine for ad-hoc work, poor in stored code: inserting a column silently changes the grouping · **[+Edge cases]** the tie makes the row order unstable, the Q71-088 problem in miniature → Ch 12 §12.14 |

### Rapid-fire, §71.11, part B: going deeper

| # | Query or question | What it returns, and why | Extra point |
|---|---|---|---|
| Q71-103 | `sum(x) OVER ()` with no `ORDER BY` — what frame? | The whole partition, so every row shows the grand total. Adding an `ORDER BY` changes the default frame to `RANGE ... CURRENT ROW` and turns it into a running total | **[+Edge cases]** this is why adding an `ORDER BY` to a working `OVER ()` total silently changes every number → Ch 28 §28.3 |
| Q71-104 | The three months tied on 13 orders, ranked by `ORDER BY orders` | `ROW_NUMBER` gives 4, 5, 6 — it never ties, so which tied month gets which number is arbitrary. `RANK` gives 4, 4, 4 and then jumps to 7. `DENSE_RANK` gives 4, 4, 4 and then 5 | **[+Validate]** `RANK` skips numbers after a tie and `DENSE_RANK` does not, so the two diverge from that point on: at 14 orders they read 7 and 5 → Ch 13 §13.4 |
| Q71-105 | `WHERE row_number() OVER (...) = 1` | An error: window functions are evaluated after `WHERE`. Wrap it in a subquery or CTE and filter outside | **[+Edge cases]** the same reason an alias from `SELECT` is unavailable in `WHERE` → Ch 12 §12.11, Q71-010 |
| Q71-106 | `NOT IN` against a subquery that returns **no rows at all** | Every outer row: there is nothing for the comparison to fail against, so it is vacuously true. The opposite failure mode to one NULL | **[+Edge cases]** `NOT IN` returns everything on an empty subquery and nothing on a subquery with one NULL → Ch 12 §12.12 |
| Q71-107 | `LEFT JOIN` then `WHERE right_table.key IS NULL` | The anti-join: the non-matching left rows only. The one right-table condition that belongs in `WHERE` rather than `ON` | **[+Trade-offs]** compare with `NOT EXISTS`, which expresses the same intent without relying on the NULL-filled row → Ch 12 §12.10, Q71-001 |
| Q71-108 | `SELECT count(*) FROM orders WHERE order_date BETWEEN '2025-01-01' AND '2025-01-31';` | On this `DATE` column, every January order — `BETWEEN` is inclusive on both ends. On a `TIMESTAMP` column the same query drops anything after midnight on the 31st | **[+Edge cases]** the half-open form `>= '2025-01-01' AND < '2025-02-01'` is correct for both types; Riverstone's own column is a `DATE`, which is exactly why the bug survives review elsewhere → Ch 12 §12.6, Q71-007 |

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `NOT IN` with a subquery that can contain NULL | Query silently returns zero rows | Filter NULLs in the subquery, or use `NOT EXISTS` / `LEFT JOIN ... IS NULL` |
| Filtering `WHERE` on an aggregate | Query errors | Use `HAVING` for aggregate conditions |
| `LIMIT`/`OFFSET` for "Nth highest" | Silently wrong on a tie | `DENSE_RANK` instead |
| Joining through a one-to-many table before aggregating | Totals inflate (fan-out), exactly Q71-072's doubled revenue | Aggregate the base fact table first; join only tables that don't fan out |
| Assuming an index is always used | Confusion when `EXPLAIN` shows a sequential scan anyway | Check the table size; small tables genuinely don't benefit |
| Forgetting `ORDER BY` inside a window function | `LAG`/`LEAD`/running totals become meaningless or change between runs | Give every window function an explicit row order, with a tie-breaker |
| Assuming PostgreSQL and MySQL syntax is interchangeable | A query that works on one engine errors or misbehaves on the other | Check the dialect differences (section 71.8) before porting |
| A `<>` or `NOT IN` filter on a nullable column | The positive and negative filters do not add up to the row count, and nobody checks | `IS DISTINCT FROM`, or an explicit `OR col IS NULL` (Q71-079) |
| `count(*)` after an outer join | Every non-matching row reports 1 instead of 0, so nothing is ever at zero | Count a column from the right-hand table (Q71-083) |
| Integer division in a percentage | Any rate below 50% reads as 0 on PostgreSQL | Put `100.0 *` at the front, before the division (Q71-090) |
| `sum` over rows that might not exist | A blank tile instead of ₹0, or a NULL that spreads downstream | `coalesce(sum(...), 0)` wherever a report reads it (Q71-078) |

---

## In the real world: the interview that hinged on one word

Deepak, interviewing for an Analytics Engineer role, is given a live SQL round: "Write a query showing each customer's total spend." He writes a clean, correct query joining customers to orders to order_items, summing revenue, in under three minutes.

The interviewer says: "Good. Now, what if I told you a customer can have order line items marked as returned, and 'total spend' should exclude those?" Deepak hadn't seen a `returned` flag in the schema he was shown, so instead of guessing, he asks: "Is there a status or flag column on order_items I should filter on, or does 'returned' show up somewhere else, like a separate returns table?" The interviewer, satisfied, describes a `returned` boolean column Deepak hadn't been shown, and Deepak adds one line: `WHERE returned = FALSE` (or `AND NOT oi.returned`, depending on how it's stored), explaining the change out loud as he types it.

What made this a strong round wasn't the original query, it was correct and unremarkable. It was that Deepak's first reaction to new information was a clarifying question, not a guess, and once given the real answer, resumed working with essentially no wasted motion, since the underlying query structure didn't need to change, only one filter needed to be added. That's Chapter 69's Move 1, live, under real pressure, and it's the single most common thing separating a "pass" from a "strong pass" in this specific kind of round.

---

## Project

**Goal:** verified, real answers to the classic SQL problems, on your own data or Riverstone's.

### Tools you'll need

**PostgreSQL** and **MySQL**, both free, both open source, installed as in Chapter 12, section 12.3 (the current releases: PostgreSQL 18 and MySQL 9.7 LTS, or 8.4 LTS). `psql` (PostgreSQL's command-line client) and the `mysql` client, or DBeaver for either. `EXPLAIN` (both engines) and `EXPLAIN ANALYZE` (runs the query and reports real timings, not just estimates) for reading query plans. Everything in this chapter was run on PostgreSQL 16 and MySQL 8.4 LTS, on Riverstone's `riverstone`, `riverstone_2025` and `riverstone_lab` databases, and run again on PostgreSQL 18 and MySQL 9.7 with the same results. One difference to know: MySQL 9.0 and later enforce the inline `REFERENCES` form that 8.4 ignores (Q71-047 avoids it).

1. Write and run the "customers with no orders" query (Q71-001), and reconcile the count against total customers minus customers with orders, the way this chapter did.
2. Demonstrate the `NOT IN` NULL trap yourself: find a nullable foreign key in your data, and show the same query returning zero rows with `NOT IN` and the correct count with `NOT EXISTS`.
3. Write one "top N per group" window-function query, and check whether any group returns fewer than N rows, reporting it honestly if so.
4. Run `EXPLAIN` on one of your own queries before and after adding an index, and report what actually changed, not what you expected to change. Drop the index afterwards.
5. Find one place in your own data (or Riverstone's) where a join could fan out unexpectedly, and prove the doubled or tripled total the way Q71-072 did.

---

## Key terms

`LEFT JOIN` / `INNER JOIN` · anti-join · `NOT IN` NULL trap · `NOT EXISTS` · `WHERE` vs. `HAVING` · correlated subquery · scalar subquery · CTE (`WITH`) · recursive CTE · `EXISTS` vs. `IN` · `ROW_NUMBER` / `RANK` / `DENSE_RANK` · tie-breaker · `PARTITION BY` · `LAG` / `LEAD` · running total · default frame (`RANGE` vs. `ROWS`) · gaps-and-islands · fan-out (join cardinality) · `ON DELETE CASCADE` / `NO ACTION` · isolation level · dirty read · MVCC · `EXPLAIN` / `ANALYZE` · sequential scan vs. index scan · composite index · covering index · `STRING_AGG` / `GROUP_CONCAT` · `COALESCE` / `IFNULL` · `IDENTITY` / `AUTO_INCREMENT` · three-valued logic (true / false / unknown) · `IS DISTINCT FROM` · `<=>` (MySQL NULL-safe equals) · `NULLIF` · `count(*)` vs. `count(col)` · `count(DISTINCT col)` · `FILTER (WHERE …)` · NULL propagation in `||` · `CONCAT_WS` · `CASE` without `ELSE` · empty-set aggregate · integer division · truncation vs. rounding · division by zero · `NULLS FIRST` / `NULLS LAST` · `ORDER BY col IS NULL` · peer group · ordinal `GROUP BY` · non-deterministic `LIMIT` · `FETCH FIRST … WITH TIES` · aggregate inside a window function

---

## Final-week revision list

Q71-001, Q71-002, Q71-006, Q71-009, Q71-023, Q71-028, Q71-029, Q71-030, Q71-033, Q71-034, Q71-035, Q71-036, Q71-042, Q71-043, Q71-060, Q71-063, Q71-067, Q71-068, Q71-072, Q71-073, Q71-079, Q71-082, Q71-087, Q71-090.

The last four are the predict-the-output questions worth most per minute: the `<>` filter that loses rows (Q71-079), the LEFT JOIN undone by its own `WHERE` (Q71-082), the default window frame (Q71-087), and integer division (Q71-090). Between them they cover the three mechanisms the whole of section 71.11 runs on.

---

## Where this leads

- **Chapter 69, The Extra-Points Method,** is the rubric and move set every answer above is written against.
- **Chapter 70, Excel/Sheets/VBA/BI Question Bank,** picks up the same Merge/Append and `QUERY` logic in spreadsheet form.
- **Chapter 77, Data Engineering & Data System Design Bank,** takes indexing and query optimization (section 71.9) to production scale.
- **Chapters 12, 13 and 28** teach the techniques this bank draws on (Chapter 14 for cleaning, Chapter 49 for ACID). Questions marked *Beyond the book* go further; each carries its own short explanation.
