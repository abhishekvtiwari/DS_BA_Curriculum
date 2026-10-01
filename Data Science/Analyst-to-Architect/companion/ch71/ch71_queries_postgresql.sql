-- Chapter 71. SQL Question Bank
-- Practice SQL for POSTGRESQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_postgresql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch71-sql-question-bank.md


-- =============================================================================================
-- Chapter 71. SQL Question Bank
-- =============================================================================================

-- Part 8 — Be Interview Ready

-- > Chapter at a glance > > You will learn to: answer the SQL questions that come up across
-- screening calls, live-coding rounds, and take-home exercises for every data role · reason
-- through the classic NULL and join traps that catch experienced candidates, not just beginners ·
-- write window-function solutions to the second-highest, top-N-per-group, running-total, streak
-- and retention problems that recur across companies · know exactly where PostgreSQL and MySQL
-- disagree · walk out with a 20-question final-week revision list. > > Before you start: Chapter
-- 69 (the three answer tiers and the twelve extra-point tags). The questions test Chapters 12 and
-- 13 (SQL), Chapter 14 (cleaning), Chapter 27 (NTILE) and Chapter 28 (recursive CTEs, window
-- frames, query plans, indexes, materialized views), plus Chapter 49, section 49.4 (ACID). This
-- chapter tests those skills; it doesn't teach them again. > > Time needed: 3–4 hours for a first
-- pass (about 5 minutes per core question, 1 minute per rapid-fire row); 6–8 hours more to run
-- every core question yourself in both databases; 1 hour for the final-week list. > > How this
-- chapter is built. Same format as every question bank in Part 8 (Chapters 70–82): every core
-- question leads with a "Remember it as…" memory hook, a one-line answer, and a compact tier
-- table, and every rapid-fire section is a scan table. After each question number comes its level:
-- Warm-up (sections 71.1–71.3), Core (CTEs, window functions, the classic problems, schema and
-- dialect questions) or Advanced (recursive CTEs, gaps-and-islands, window frames, transactions,
-- indexes). Rapid-fire tables take the level of their section. Extra-point moves are labelled with
-- Chapter 69's twelve tags, such as [+Edge cases]. > > Every query is shown in PostgreSQL and was
-- run on PostgreSQL 16. Where MySQL needs different syntax, a MySQL: block follows, and that
-- version was run on MySQL 8.4 LTS. Every result printed below is the database's real answer, kept
-- exactly as returned, including the surprising ones (an empty result, a tied ranking, an index
-- the planner declines to use). > > Which database. Most questions use riverstone_2025, the one-
-- year practice database from Chapter 13, section 13.1. Question Q71-072 uses the mini database
-- riverstone from Chapter 12, section 12.2, and says so. The questions that create tables (Q71-013
-- and section 71.7) run in riverstone_lab, the practice database you created in Chapter 12,
-- section 12.13, and drop their tables at the end. Each Verified line names its database. > >
-- Learn it in pointers name the chapter and section that teaches the idea. Questions and rapid-
-- fire rows marked Beyond the book go further than the teaching chapters; each of those carries
-- its own short explanation.

-- ---

-- <!-- db: riverstone_2025 -->

-- =============================================================================================
-- 71.1 Core concepts: SELECT, WHERE, and JOIN
-- =============================================================================================

-- =============================================================================================
-- Q71-001 · Find customers who have never placed an order · Warm-up
-- =============================================================================================

-- Remember it as: LEFT JOIN + IS NULL, or NOT EXISTS. Never NOT IN if the other side might have a
-- NULL.

-- The query:

SELECT c.customer_id, c.customer_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;


-- | Tier | What to say | |---|---| | Passes | WHERE customer_id NOT IN (SELECT customer_id FROM
-- orders): works on clean data, has a hidden flaw (Q71-002) | | Strong | The LEFT JOIN ... IS NULL
-- version above, filtering on the right table's primary key, not an arbitrary column | | Extra
-- points | [+Clarify] should a customer whose only order was cancelled count as "never ordered"? ·
-- [+Validate] total customers = customers with orders + customers without, checked: 24 = 23 + 1 ✓
-- · [+Business] add the signup date and sort by it, so sales can follow up the newest non-
-- converters first |

-- Likely follow-ups: No orders in the last 90 days, not ever? Products never sold? Rewrite without
-- a join? Red flag: WHERE o.customer_id = NULL (should be IS NULL); filtering a left join's right-
-- table column in WHERE in a way that silently turns it into an inner join. The one deliberate
-- exception is IS NULL on the right table's key: that is what makes this an anti-join (Chapter 12,
-- section 12.10). Any other condition on the right table belongs in ON. Learn it in: Chapter 12,
-- section 12.10 (the anti-join).

-- =============================================================================================
-- Q71-002 · Why is NOT IN dangerous with a subquery that might contain a NULL? · Warm-up
-- =============================================================================================

-- Remember it as: One NULL in a NOT IN subquery poisons the whole comparison: the query returns
-- nothing, silently.

-- Answer in one line: If the subquery's result contains even one NULL, NOT IN returns zero rows
-- for every outer row, because SQL can't prove any value is "not equal to NULL": the comparison
-- evaluates to UNKNOWN, not TRUE, and NOT IN needs every comparison to be TRUE. (Q71-009 shows the
-- root cause: NULL = NULL isn't true either.)

-- Verified (riverstone_2025): the orders.sales_rep_id column has 11 NULL rows (unassigned orders).
-- The trap, live:

SELECT count(*)
FROM employees
WHERE employee_id NOT IN (SELECT sales_rep_id FROM orders);

/* The chapter shows:
    count
   -------
        0
   (1 row)
*/


-- The same question, asked correctly:

SELECT count(*)
FROM employees
WHERE employee_id NOT IN (SELECT sales_rep_id
                          FROM orders
                          WHERE sales_rep_id IS NOT NULL);

/* The chapter shows:
    count
   -------
        2
   (1 row)
*/


-- | Tier | What to say | |---|---| | Passes | "NOT IN can behave oddly with NULLs" (vague, no
-- mechanism) | | Strong | The UNKNOWN-comparison explanation above, with the fix (WHERE ... IS NOT
-- NULL inside the subquery) | | Extra points | [+Validate] the exact live numbers above: 0 rows
-- (wrong) vs. 2 rows (right) on the same data, same question · [+Trade-offs] NOT EXISTS and LEFT
-- JOIN ... IS NULL don't have this problem at all, since they test whether a matching row exists
-- rather than comparing a value against a list that holds a NULL: prefer them by default |

-- Likely follow-ups: Does IN (not NOT IN) have the same problem? (No: IN with a NULL in the list
-- just doesn't match the NULL; it doesn't empty the whole result.) How would you find this bug in
-- someone else's query? Red flag: not knowing this is a real, live trap, not a theoretical one: 11
-- real NULL rows just demonstrated it. Learn it in: Chapter 12, section 12.12 (the "NOT IN and
-- NULLs" box).

-- =============================================================================================
-- Rapid-fire, §71.1 (Warm-up)
-- =============================================================================================

-- | # | Question | One-line answer | Extra point | |---|---|---|---| | Q71-003 | WHERE vs. HAVING?
-- | Filters rows before grouping / filters groups after aggregation | [+Edge cases] you can't
-- reference an aggregate function in WHERE: that's precisely what HAVING is for → Ch 12 §12.9 | |
-- Q71-004 | INNER JOIN vs. LEFT JOIN? | Only matching rows from both tables / all left-table rows,
-- NULLs where there's no match | [+Business] a LEFT JOIN that unexpectedly shrinks the row count
-- usually means a filter on the right table leaked into WHERE instead of ON → Ch 12 §12.10 | |
-- Q71-005 | What does SELECT DISTINCT actually do? | Removes duplicate entire rows from the
-- result, not duplicates in one column alone | [+Edge cases] SELECT DISTINCT a, b removes
-- duplicates of the combination of a and b, not of each column on its own → Ch 12 §12.5 | |
-- Q71-006 | UNION vs. UNION ALL? | UNION removes duplicate rows across the combined result / UNION
-- ALL keeps everything, no duplicate check (verified: 2 identical rows → 2 with UNION ALL, 1 with
-- UNION) | [+Scale] UNION ALL is faster, since it skips the duplicate check: use it whenever you
-- know the two sets can't overlap → Ch 12 §12.12 | | Q71-007 | BETWEEN: is it inclusive or
-- exclusive? | Inclusive on both ends | [+Edge cases] BETWEEN '2025-01-01' AND '2025-01-31' on a
-- TIMESTAMP column silently misses rows on the 31st after midnight: cast to DATE first, or use <
-- '2025-02-01' → Ch 12 §12.6; the timestamp case is beyond the book | | Q71-008 | What's a
-- correlated subquery? | A subquery that references a column from the outer query, re-evaluated
-- once per outer row (e.g., each customer's own most recent order date) | [+Trade-offs] correlated
-- subqueries can be slow at scale (one execution per row); a window function or a join often
-- expresses the same logic faster → Ch 12 §12.12 |

-- ---

-- =============================================================================================
-- 71.2 Basic questions that are trickier than they look
-- =============================================================================================

-- Every one of these sounds like a warm-up question. Every one of them has caught experienced
-- candidates, because the trap is in something they assumed rather than something they didn't
-- know. They mix theory and practice, and each one is shown live wherever a query can demonstrate
-- the point.

-- =============================================================================================
-- Q71-009 · Does NULL = NULL evaluate to true? · Warm-up
-- =============================================================================================

-- Remember it as: NULL isn't a value, it's the absence of one. You can't ask whether two absences
-- are "equal."

-- Answer in one line: No: NULL = NULL evaluates to NULL (unknown), not TRUE, which is exactly why
-- WHERE column = NULL never matches anything and IS NULL exists as a separate operator.

-- Verified (riverstone_2025):

SELECT (NULL = NULL) AS result,
       (NULL = NULL) IS NULL AS is_this_null;

/* The chapter shows:
    result | is_this_null
   --------+--------------
           | t
   (1 row)
*/


-- PostgreSQL prints NULL as a blank and true as t. MySQL runs the same query and prints NULL and
-- 1, since it stores true as the number 1 (Q71-066).

-- | Tier | What to say | |---|---| | Passes | "NULL equals NULL" (the actual trap, stated as fact)
-- | | Strong | Correctly says no, it evaluates to NULL/unknown, and explains why = NULL in a WHERE
-- clause silently matches nothing | | Extra points | [+Validate] the query above proves it two
-- ways at once: the comparison itself shows blank (NULL), and wrapping it in IS NULL confirms that
-- blank really is NULL, not empty text · [+Business] this is exactly the mechanism behind
-- Q71-002's NOT IN trap: one root cause, two different symptoms |

-- Likely follow-ups: How do you check for NULL correctly? What does NULL AND FALSE evaluate to?
-- (FALSE: one known-false input is enough to decide an AND, even with an unknown on the other
-- side.) Red flag: confidently stating NULL = NULL is true. Learn it in: Chapter 12, section 12.7.

-- =============================================================================================
-- Q71-010 · Can you use a column alias from SELECT inside the same query's WHERE clause? · Warm-up
-- =============================================================================================

-- Remember it as: WHERE runs before SELECT ever names anything. You can't filter on a name that
-- doesn't exist yet.

-- Answer in one line: No: SQL's logical order runs FROM → WHERE → GROUP BY → HAVING → SELECT →
-- ORDER BY, so a WHERE clause runs before SELECT has assigned any alias, and referencing one
-- errors.

-- Verified (riverstone_2025):

SELECT customer_name, city AS loc
FROM customers
WHERE loc = 'Mumbai';

/* The chapter shows:
   ERROR:  column "loc" does not exist
*/


-- MySQL: the same query fails with its own wording:

SELECT customer_name, city AS loc
FROM customers
WHERE loc = 'Mumbai';

/* The chapter shows:
   ERROR 1054 (42S22): Unknown column 'loc' in 'where clause'
*/


-- | Tier | What to say | |---|---| | Passes | "You can't use an alias in WHERE" (correct, no
-- reason given) | | Strong | + explains the logical order, and that this is why the alias doesn't
-- exist yet at the point WHERE runs | | Extra points | [+Validate] the real error messages above,
-- not a guess at what they might say · [+Edge cases] ORDER BY runs after SELECT, so aliases work
-- fine there: the same alias that errors in WHERE is legal in ORDER BY, which is worth saying out
-- loud since it looks inconsistent until you know the order |

-- Likely follow-ups: Does GROUP BY allow an alias? (Yes, in PostgreSQL and MySQL, though not in
-- every SQL engine.) How would you filter on a computed value if not in WHERE? (A CTE or subquery,
-- filtering the outer layer: the same pattern Q71-033 and Q71-035 use for window functions.) Red
-- flag: not knowing SQL has a logical order that differs from the order it's written in. Learn it
-- in: Chapter 12, section 12.11.

-- =============================================================================================
-- Q71-011 · Why does sorting '9', '10', '2' as text give a different order than sorting them as numbers? · Warm-up
-- =============================================================================================

-- Remember it as: Text sorts character by character. "10" starts with "1," which comes before "2"
-- and "9": the number itself is never considered.

-- Answer in one line: As text, comparison goes character by character, so '10' sorts before '2'
-- because '1' < '2' as the very first character; as numbers, ordinary numeric comparison applies
-- and 2 < 9 < 10 as expected.

-- Verified (riverstone_2025), the same three values two ways. As text:

SELECT val
FROM (VALUES ('9'), ('10'), ('2')) AS t(val)
ORDER BY val;

/* The chapter shows:
    val
   -----
    10
    2
    9
   (3 rows)
*/


-- As integers:

SELECT val
FROM (VALUES (9), (10), (2)) AS t(val)
ORDER BY val;

/* The chapter shows:
    val
   -----
      2
      9
     10
   (3 rows)
*/


-- MySQL: a list of literal rows is written VALUES ROW(…), and its column is always called
-- column_0:

SELECT column_0
FROM (VALUES ROW('9'), ROW('10'), ROW('2')) AS t
ORDER BY column_0;

/* The chapter shows:
   +----------+
   | column_0 |
   +----------+
   | 10       |
   | 2        |
   | 9        |
   +----------+
*/


-- | Tier | What to say | |---|---| | Passes | "Text and numbers sort differently" (true, no
-- mechanism) | | Strong | The character-by-character explanation above, with the real output
-- showing both orders on the same three values | | Extra points | [+Business] this bug shows up
-- whenever a numeric code gets stored as VARCHAR: order numbers, SKUs, PIN codes. A report
-- silently sorts "wrong" with no error anywhere · [+Validate] cast to confirm: ORDER BY val::int
-- on the text version recovers the numeric order (MySQL: ORDER BY CAST(column_0 AS SIGNED)), which
-- is itself proof of what was happening |

-- Likely follow-ups: How would you fix a column that's the wrong type after the fact? What about
-- sorting mixed codes like "A10" vs "A9"? Red flag: unable to explain why it happens, only that it
-- does. Learn it in: Chapter 12, section 12.1 (why types matter) and section 12.8 (CAST and ::).

-- =============================================================================================
-- Q71-012 · What's the difference between DELETE, TRUNCATE, and DROP? · Warm-up
-- =============================================================================================

-- Remember it as: DELETE removes rows, one at a time, with a WHERE if you want. TRUNCATE empties
-- the whole table, fast, no WHERE. DROP removes the table itself, structure and all.

-- Answer in one line: DELETE FROM t WHERE ... removes matching rows (or all rows with no WHERE),
-- logged row by row, and can be rolled back inside a transaction; TRUNCATE TABLE t empties the
-- entire table at once, much faster, minimally logged. In MySQL it also resets AUTO_INCREMENT; in
-- PostgreSQL the identity or sequence keeps counting unless you write TRUNCATE TABLE t RESTART
-- IDENTITY. DROP TABLE t removes the table's structure entirely, data and definition both gone.

-- | Tier | What to say | |---|---| | Passes | "They all delete data" | | Strong | The three
-- distinct scopes and behaviors above | | Extra points | [+Edge cases] TRUNCATE can't take a WHERE
-- clause: it's all rows or nothing, by design · [+Business] the classic production incident is a
-- DELETE whose WHERE got lost in a copy-paste, which empties the table. Inside BEGIN … ROLLBACK
-- you can undo it. TRUNCATE in MySQL commits immediately, so there is no undo · [+Trade-offs]
-- DELETE fires row-level triggers (if any exist) and can be rolled back mid-transaction; TRUNCATE
-- skips row triggers, and in MySQL it can't be rolled back |

-- Likely follow-ups: Can TRUNCATE be rolled back? (In PostgreSQL, yes, inside a transaction; in
-- MySQL, no: it commits implicitly.) Does TRUNCATE restart the ID counter? (MySQL: yes.
-- PostgreSQL: only with RESTART IDENTITY; checked on both.) What happens to foreign-key-referenced
-- rows on each? Red flag: treating all three as interchangeable ways to "clear a table." Learn it
-- in: Chapter 12, section 12.13 (Step 8, transactions, and Step 11, TRUNCATE and DROP). RESTART
-- IDENTITY is beyond the book.

-- =============================================================================================
-- Q71-013 · Does a UNIQUE constraint allow more than one NULL value in a column? · Warm-up
-- =============================================================================================

-- Remember it as: NULL never equals NULL (Q71-009): so a UNIQUE constraint, which is really an
-- equality check, can't call two NULLs "duplicates" of each other.

-- Answer in one line: Yes, in both PostgreSQL and MySQL: a UNIQUE constraint allows any number of
-- NULL values in that column, because uniqueness is checked by equality, and no two NULLs are ever
-- equal to each other.

-- Verified, in riverstone_lab (same statements in both databases):

-- <!-- Verifier setup, not printed: the lab database the reader made in Chapter 12.

CREATE DATABASE riverstone_lab;


CREATE DATABASE riverstone_lab;


-- -->

CREATE TABLE test_unique (id INT, email VARCHAR(50) UNIQUE);
INSERT INTO test_unique VALUES (1, NULL);
INSERT INTO test_unique VALUES (2, NULL);
SELECT * FROM test_unique;

/* The chapter shows:
    id | email
   ----+-------
     1 |
     2 |
   (2 rows)
*/


-- Both inserts succeeded: a surprising result to anyone who reads "unique" as "no duplicates,
-- including blanks." Tidy up (same in both):

DROP TABLE test_unique;


-- | Tier | What to say | |---|---| | Passes | "UNIQUE means no duplicates" (true for non-NULL
-- values, misses the NULL exception entirely) | | Strong | Correctly states multiple NULLs are
-- allowed, and ties it back to NULL = NULL being unknown, not true | | Extra points | [+Validate]
-- the live proof above: two NULL emails, one UNIQUE constraint, zero errors · [+Business] this is
-- why a "unique email" constraint alone doesn't stop two customer records both missing an email
-- address from silently coexisting: a data-quality gap that looks like the schema should prevent
-- it, and doesn't |

-- Likely follow-ups: How would you actually prevent multiple blank emails if that's the real
-- requirement? (Add NOT NULL alongside UNIQUE, or use a partial unique index. PostgreSQL 15 and
-- later also offer email VARCHAR(50) UNIQUE NULLS NOT DISTINCT, which treats NULLs as equal for
-- this one constraint, so the second NULL is rejected; checked on PostgreSQL 16.) Does a PRIMARY
-- KEY allow NULLs the same way? (No: a primary key is UNIQUE plus NOT NULL, so it never allows
-- even one NULL.) Red flag: confidently claiming a UNIQUE column can never have more than one
-- blank value. Learn it in: Chapter 12, section 12.13 (Step 3, constraints) and section 12.7
-- (NULL). NULLS NOT DISTINCT is beyond the book.

-- =============================================================================================
-- Q71-014 · What happens if you self-join a table without giving it two different aliases? · Warm-up
-- =============================================================================================

-- Remember it as: The database can't tell which "employees" you mean if you never gave it two
-- different names to tell them apart.

-- Answer in one line: It errors. PostgreSQL rejects the FROM clause itself (table name "employees"
-- specified more than once); MySQL says Not unique table/alias. Without two aliases there's no way
-- to say which copy each column comes from.

-- Verified (riverstone_2025):

SELECT employee_id
FROM employees
JOIN employees ON employee_id = manager_id;

/* The chapter shows:
   ERROR:  table name "employees" specified more than once
*/


-- MySQL:

SELECT employee_id
FROM employees
JOIN employees ON employee_id = manager_id;

/* The chapter shows:
   ERROR 1066 (42000): Not unique table/alias: 'employees'
*/


-- | Tier | What to say | |---|---| | Passes | "You need aliases for a self-join" (correct, no
-- example of what breaks without one) | | Strong | The explanation above, plus the correctly
-- aliased version (FROM employees e JOIN employees m ON e.manager_id = m.employee_id), which is
-- exactly Chapter 12's self-join (section 12.10), and the base of Q71-029's hierarchy query | |
-- Extra points | [+Validate] the real error messages above, which are a different, earlier failure
-- than the "ambiguous column" error a beginner might expect (and that some other engines, such as
-- SQLite, do report): worth knowing so you recognize it instantly |

-- Likely follow-ups: Would this also happen with a regular join between two different tables that
-- share a column name? (Only for the shared column: you'd get an "ambiguous column" error on that
-- reference, not on the table.) Red flag: not immediately recognizing that a self-join needs two
-- aliases. Learn it in: Chapter 12, section 12.10 (the self-join).

-- =============================================================================================
-- Q71-015 · Why does SELECT  with a GROUP BY often error, even though it "looks" fine? · *Warm-up
-- =============================================================================================

-- Remember it as: GROUP BY collapses many rows into one per group. SELECT  asks for every column,
-- including ones that could hold many different values within that one group.*

-- Answer in one line: Every non-aggregated column in SELECT must also appear in GROUP BY, because
-- the database can't know which single value to show for a column that wasn't grouped and might
-- differ across the rows being collapsed into one.

-- Verified (riverstone_2025):

SELECT * FROM orders GROUP BY customer_id;

/* The chapter shows:
   ERROR:  column "orders.order_id" must appear in the GROUP BY clause or be used in an aggregate function
*/


-- MySQL:

SELECT * FROM orders GROUP BY customer_id;

/* The chapter shows:
   ERROR 1055 (42000): Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'riverstone_2025.orders.order_id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
*/


-- | Tier | What to say | |---|---| | Passes | "SELECT * doesn't work well with GROUP BY" (true, no
-- reason) | | Strong | The collapsing-rows explanation above, plus the real error naming the exact
-- offending column | | Extra points | [+Edge cases] since MySQL 5.7.5, ONLY_FULL_GROUP_BY is on by
-- default, so modern MySQL errors too; very old MySQL, or a server with that mode switched off,
-- silently picks an arbitrary row's value instead, which is far more dangerous than an error. Both
-- engines do accept ungrouped columns that depend on a grouped primary key: SELECT  FROM orders
-- GROUP BY order_id runs in both (checked) · [+Business] a real reason SELECT  is a bad habit in
-- any query with GROUP BY: list only the columns you need and can justify |

-- Likely follow-ups: What SQL mode controls this behavior in MySQL? How would you fix this query
-- to actually work? Red flag: not knowing that a MySQL server with ONLY_FULL_GROUP_BY switched off
-- returns a plausible-looking but unreliable answer instead of an error. Learn it in: Chapter 12,
-- section 12.9 (its dialect note on ONLY_FULL_GROUP_BY).

-- =============================================================================================
-- Rapid-fire, §71.2 (Warm-up): more basic-but-tricky theory and practice
-- =============================================================================================

-- | # | Question | One-line answer | Extra point | |---|---|---|---| | Q71-016 | Is SQL case-
-- sensitive? | Keywords (SELECT, WHERE) are not; whether your data comparisons are case-sensitive
-- depends on the column's collation, which differs by engine and setup | [+Edge cases] WHERE
-- status = 'delivered' matches 'Delivered' in MySQL's default collation and not in PostgreSQL:
-- never assume either way without checking → Ch 12 §12.6 and §12.16 | | Q71-017 | CHAR vs.
-- VARCHAR? | CHAR(n) is fixed-length, padded with spaces to exactly n characters; VARCHAR(n) is
-- variable-length, up to n characters, no padding | [+Business] CHAR padding can break an exact-
-- string comparison against a value that wasn't padded the same way in another system → Beyond the
-- book | | Q71-018 | Do you need a semicolon at the end of a SQL statement? | Required to separate
-- multiple statements in one script; often optional for a single statement in an interactive
-- client | [+Edge cases] in a multi-statement script a missing semicolon usually makes the next
-- statement a syntax error, and the error points at the wrong line, which makes it confusing to
-- debug → Ch 12 §12.4 | | Q71-019 | Is a FOREIGN KEY required for a JOIN to work? | No: a JOIN is
-- just a condition in ON; it works with or without a declared foreign-key constraint | [+Business]
-- a missing foreign key doesn't stop joins; it stops the database from rejecting orphaned data
-- before the join ever runs: the constraint is a data-quality guard, not a join requirement → Ch
-- 12 §12.10 and §12.13 | | Q71-020 | Can two rows be "duplicates" if they have different primary
-- keys? | Yes: a primary key only guarantees that column is unique; every other column can be
-- identical across two rows | [+Edge cases] this is why "remove duplicates" almost always means
-- "duplicates ignoring the ID column," which needs to be said explicitly → Ch 14 §14.4 | | Q71-021
-- | Does LIKE '%text%' match case-sensitively? | Depends on the collation, same root cause as
-- Q71-016; PostgreSQL offers ILIKE for a guaranteed case-insensitive match | [+Edge cases] when in
-- doubt, wrap both sides in LOWER() for a comparison that ignores case under any collation → Ch 12
-- §12.6 | | Q71-022 | How does an empty string ('') compare with NULL? | They are not the same
-- thing: '' IS NULL is false, and '' = NULL is (per Q71-009) unknown, never true | [+Edge cases] a
-- form that saves a blank text field as '' instead of NULL will silently slip past every IS NULL
-- check written to catch missing data → Ch 12 §12.7 |

-- ---

-- =============================================================================================
-- 71.3 Aggregation: GROUP BY and HAVING
-- =============================================================================================

-- =============================================================================================
-- Q71-023 · Total quantity sold per category, only categories over 500 units · Warm-up
-- =============================================================================================

-- Remember it as: WHERE filters rows before the grouping happens. HAVING filters groups after.

-- The query:

SELECT p.category, SUM(oi.quantity) AS total_qty
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
HAVING SUM(oi.quantity) > 500
ORDER BY total_qty DESC;


-- | Tier | What to say | |---|---| | Passes | The correct GROUP BY + HAVING query, but can't
-- explain why WHERE can't do the same job | | Strong | The query above, plus the reason: WHERE
-- runs before the groups exist, so there is no SUM yet to test | | Extra points | [+Validate] run
-- it once without HAVING: four categories, Furniture at 30 units, so its absence is the filter
-- working, not a bug · [+Business] this shape (group, sum, filter on the sum) is the core of
-- almost every "which segments matter" business question |

-- Likely follow-ups: Same, but only the top 2 categories regardless of a fixed threshold? Add a
-- customer-segment breakdown too? Red flag: trying to filter an aggregate in WHERE (WHERE
-- SUM(quantity) > 500 errors, because aggregates can't appear in WHERE). Learn it in: Chapter 12,
-- section 12.9.

-- =============================================================================================
-- Rapid-fire, §71.3 (Warm-up)
-- =============================================================================================

-- | # | Question | One-line answer | Extra point | |---|---|---|---| | Q71-024 | Does COUNT()
-- differ from COUNT(column)? | COUNT() counts all rows / COUNT(column) counts only the non-NULL
-- values in that column | [+Edge cases] on riverstone_2025, COUNT(*) on orders is 175 and
-- COUNT(sales_rep_id) is 164: the 11 NULL rows are silently left out (verified) → Ch 12 §12.9 | |
-- Q71-025 | Can you GROUP BY a column not in the SELECT list? | Yes, in both PostgreSQL and MySQL:
-- you can group by something you don't display | [+Edge cases] the reverse is stricter: every non-
-- aggregated SELECT column must appear in GROUP BY, or the query errors (Q71-015) → Ch 12 §12.9 |
-- | Q71-026 | What does GROUP BY 1, 2 mean? | Groups by the 1st and 2nd columns of the SELECT
-- list, by position, not by name | [+Trade-offs] convenient for a long expression, but fragile:
-- reordering the SELECT columns silently changes what's grouped → Beyond the book | | Q71-027 |
-- How would you count DISTINCT customers per month? | SELECT DATE_TRUNC('month', order_date)::date
-- AS month, COUNT(DISTINCT customer_id) FROM orders GROUP BY 1 (MySQL: DATE_FORMAT(order_date,
-- '%Y-%m-01') in place of DATE_TRUNC('month', order_date)::date); both give 5, 8 and 10 customers
-- for January to March 2025 | [+Business] distinct customers per month, not the order count, is
-- the number that answers "is our customer base growing" → Ch 12 §12.8 (DATE_TRUNC) and §12.9
-- (COUNT(DISTINCT …)) |

-- ---

-- =============================================================================================
-- 71.4 Subqueries, CTEs, and EXISTS vs. IN
-- =============================================================================================

-- =============================================================================================
-- Q71-028 · Rewrite a nested subquery as a CTE, and explain why you would · Core
-- =============================================================================================

-- Remember it as: A CTE is a subquery with a name and a place to breathe. Same result, easier to
-- read and debug one step at a time.

-- Answer in one line: WITH name AS (...) SELECT ... FROM name names an intermediate result so it
-- can be read top to bottom and reused, instead of nesting parentheses inside parentheses.

-- The query:

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


-- | Tier | What to say | |---|---| | Passes | A nested subquery achieving the same result:
-- correct, harder to read past two levels | | Strong | The CTE version above, one logical step at
-- a time | | Extra points | [+Validate] the three months match Chapter 13's monthly revenue
-- (₹2,02,640, ₹2,53,664, ₹2,78,007.50) · [+Scale] several CTEs can chain (WITH a AS (...), b AS
-- (...)), each building on the last, which is how a long query stays readable (Q71-042 uses three)
-- |

-- Likely follow-ups: Recursive CTE: when would you need one? (Q71-029.) Does a CTE get computed
-- once, or folded into the main query, and does that matter for performance? Red flag: nesting
-- subqueries three or four levels deep when a CTE would make the same logic readable. Learn it in:
-- Chapter 13, section 13.2.

-- =============================================================================================
-- Q71-029 · Write a recursive CTE to show Riverstone's full management hierarchy · Advanced
-- =============================================================================================

-- Remember it as: A recursive CTE is a loop: start with the base case (the top of the tree), then
-- repeatedly join back to itself for the next level down.

-- The query:

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


-- MySQL 8 runs the same query unchanged and returns the same five rows.

-- | Tier | What to say | |---|---| | Passes | Writes the recursive CTE with help, but can't name
-- the anchor and recursive parts or the stopping condition | | Strong | The structure above: an
-- anchor query, UNION ALL, and a recursive part that joins back to the CTE itself, stopping when a
-- level finds no new rows | | Extra points | [+Validate] the output is a correct three-level tree:
-- Anita Rao at the top, her two direct reports, and Vikram Singh's two reports below him · [+Edge
-- cases] a cycle in the data (A manages B, B manages A) makes the recursion run forever. MySQL
-- stops a runaway recursion at cte_max_recursion_depth (1,000 by default); PostgreSQL has no
-- limit, so add a cap such as WHERE h.level < 20 |

-- Likely follow-ups: Find everyone reporting up to a specific manager, at any depth? What if the
-- hierarchy has a cycle by mistake? Red flag: not knowing the anchor / recursive-part structure at
-- all. Learn it in: Chapter 28, section 28.2.

-- =============================================================================================
-- Rapid-fire, §71.4 (Core)
-- =============================================================================================

-- | # | Question | One-line answer | Extra point | |---|---|---|---| | Q71-030 | EXISTS vs. IN:
-- when do they differ in behavior? | IN and EXISTS return the same rows, even with NULLs. They
-- differ when negated: NOT IN returns nothing if the subquery holds a NULL (Q71-002); NOT EXISTS
-- doesn't. Verified: EXISTS and IN both give 23 customers | [+Trade-offs] EXISTS can stop at the
-- first match for each row, which is often faster on a large subquery; prefer NOT EXISTS to NOT IN
-- by default → Ch 12 §12.12 | | Q71-031 | What's a scalar subquery? | A subquery that returns
-- exactly one row and one column, used anywhere a single value is expected | [+Edge cases] if it
-- returns more than one row, the query errors when it runs, not when you write it → Ch 12 §12.12 |
-- | Q71-032 | Each customer's most recent order date, without a GROUP BY? | A correlated scalar
-- subquery: SELECT c.customer_name, (SELECT MAX(order_date) FROM orders o WHERE o.customer_id =
-- c.customer_id) FROM customers c | [+Trade-offs] correct and simple to read; a LEFT JOIN to a
-- pre-aggregated subquery is usually faster on a large table, since it avoids one execution per
-- outer row → Ch 12 §12.12 |

-- ---

-- =============================================================================================
-- 71.5 Window functions: the classics
-- =============================================================================================

-- =============================================================================================
-- Q71-033 · Find the second-highest-priced product · Core
-- =============================================================================================

-- Remember it as: LIMIT/OFFSET breaks on ties. DENSE_RANK doesn't.

-- The query:

SELECT product_name, unit_price
FROM (
  SELECT product_name, unit_price,
         DENSE_RANK() OVER (ORDER BY unit_price DESC) AS rnk
  FROM products
) t
WHERE rnk = 2;


-- | Tier | What to say | |---|---| | Passes | ORDER BY unit_price DESC LIMIT 1 OFFSET 1: gives the
-- same right answer here, and silently breaks if two products tie for first place (OFFSET 1 would
-- then return one of the tied firsts, not the second-highest price) | | Strong | The DENSE_RANK
-- version above, which is safe on ties | | Extra points | [+Edge cases] RANK vs. DENSE_RANK
-- matters here: RANK skips a number after a tie (1, 1, 3), so rnk = 2 could return zero rows if
-- two products tied for first; DENSE_RANK (1, 1, 2) has no gap · [+Validate] on Riverstone's real
-- (untied) top prices both approaches agree, which is exactly why this bug hides until the data
-- changes |

-- Likely follow-ups: Third-highest? Second-highest per category, not overall? What if there's a
-- tie for second place itself: should both show? Red flag: using LIMIT/OFFSET with no
-- acknowledgment that it breaks on ties. Learn it in: Chapter 13, section 13.4. (OFFSET itself is
-- beyond the book.)

-- =============================================================================================
-- Q71-034 · ROW_NUMBER, RANK, and DENSE_RANK: demonstrate the difference on real tied data · Core
-- =============================================================================================

-- Remember it as: ROW_NUMBER never ties (1,2,3). RANK ties and skips (1,1,3). DENSE_RANK ties and
-- doesn't skip (1,1,2).

-- Verified (riverstone_2025), on two customers tied at 16 orders each:

SELECT c.customer_name, COUNT(*) AS order_count,
       ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC, c.customer_name) AS rn,
       RANK()       OVER (ORDER BY COUNT(*) DESC) AS rnk,
       DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS drnk
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY order_count DESC, c.customer_name
LIMIT 4;

/* The chapter shows:
        customer_name      | order_count | rn | rnk | drnk
   ------------------------+-------------+----+-----+------
    Green Leaf Hotels      |          17 |  1 |   1 |    1
    Metro Mart             |          16 |  2 |   2 |    2
    Sharma Hardware        |          16 |  3 |   2 |    2
    Northgate Distributors |          13 |  4 |   4 |    3
   (4 rows)
*/


-- The ORDER BY inside ROW_NUMBER ends with c.customer_name, a tie-breaker: without it, which of
-- the two tied customers gets 2 and which gets 3 is up to the database. Grouping by c.customer_id
-- as well as the name keeps two customers who happen to share a name apart.

-- | Tier | What to say | |---|---| | Passes | Names all three functions, can't explain how they
-- differ on a tie | | Strong | Reads the table above correctly: RANK gives both tied customers
-- rank 2, then skips to 4; DENSE_RANK gives them both 2, then continues at 3 with no gap | | Extra
-- points | [+Validate] this is real tied data, not a made-up example: Metro Mart and Sharma
-- Hardware really do have 16 orders each · [+Edge cases] ROW_NUMBER on a tie is non-deterministic
-- unless you add a tie-breaker; two runs can disagree · [+Business] "top 3 customers" means
-- something different depending on which function you pick when there's a tie at the boundary:
-- worth clarifying with whoever asked for the list |

-- Likely follow-ups: Which one would you use for "top N per group," and why? What does NTILE do?
-- (Q71-039.) Red flag: claiming they're interchangeable, or unable to predict what happens at a
-- tie without running it. Learn it in: Chapter 13, section 13.4.

-- =============================================================================================
-- Q71-035 · Top 2 products by revenue, within each category · Core
-- =============================================================================================

-- Remember it as: PARTITION BY is GROUP BY for window functions: it restarts the ranking at each
-- group boundary instead of collapsing rows.

-- The query:

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


-- Note: Furniture and Industrial show only one row each, not two. That's real data, not a bug:
-- Furniture and Industrial each have only one product in the catalogue.

-- | Tier | What to say | |---|---| | Passes | A correlated subquery per category finding the top
-- product, then a second one for the runner-up: works, ugly, doesn't generalize past "top 2" | |
-- Strong | The PARTITION BY version above: one query, any N | | Extra points | [+Edge cases]
-- exactly this: two categories return fewer than 2 rows because they have only one product; rn <=
-- 2 never guarantees exactly 2 rows per group, and it's worth saying so before the result
-- surprises someone · [+Validate] run the inner query on its own: 8 rows, one per product, and
-- they add up to ₹43,35,471, Riverstone's 2025 revenue, so nothing was lost or double-counted
-- before the ranking |

-- Likely follow-ups: Same but by revenue share within category, not rank? What changes using RANK
-- instead of ROW_NUMBER here? Red flag: not expecting that some groups may have fewer members than
-- N. Learn it in: Chapter 13, section 13.7 (Pattern 1, top N per group).

-- =============================================================================================
-- Q71-036 · Month-over-month revenue change with LAG · Core
-- =============================================================================================

-- Remember it as: LAG looks backward one row. LEAD looks forward one row. Both need an ORDER BY to
-- mean anything.

-- The query:

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


-- MySQL: the same DATE_FORMAT swap as in Q71-028.

-- | Tier | What to say | |---|---| | Passes | A self-join on month = previous month (date
-- arithmetic): correct, even with gaps, but verbose | | Strong | LAG as above, noting that the
-- first row's change is NULL because there's no earlier month, plus a note that LAG needs a gap-
-- free month series: build one first (Chapter 13, section 13.8, Pattern 5, fill in the missing
-- months), or check that month - LAG(month) is exactly one month | | Extra points | [+Validate]
-- the real fall in April (−₹67,726) is kept as it is, a real month-over-month decline, rather than
-- picking a friendlier month to show · [+Edge cases] a month with no orders has no row at all, so
-- without a gap-free series LAG silently compares with a month that isn't the previous one |

-- Likely follow-ups: LAG two periods back instead of one? Percentage change, not absolute? LEAD
-- for "days until next order"? Red flag: forgetting ORDER BY inside the window (the function
-- becomes meaningless without a defined row order). Learn it in: Chapter 13, section 13.5.

-- =============================================================================================
-- Rapid-fire, §71.5 (Core)
-- =============================================================================================

-- | # | Question | One-line answer | Extra point | |---|---|---|---| | Q71-037 | What does SUM(x)
-- OVER (ORDER BY month) compute, with no PARTITION BY? | A running total across all rows, in that
-- order | [+Edge cases] without a frame clause, the default frame is RANGE BETWEEN UNBOUNDED
-- PRECEDING AND CURRENT ROW, so rows that tie on the ORDER BY value get the same running total.
-- Write ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW for a strict row-by-row running total →
-- Ch 13 §13.6 | | Q71-038 | What's the difference between a window function and GROUP BY? | GROUP
-- BY collapses rows into one per group; a window function keeps every row and adds a calculated
-- column beside it | [+Business] this is why window functions exist for reporting: you can show a
-- customer's single order next to their running total, in the same row → Ch 13 §13.3 | | Q71-039 |
-- What's NTILE(4) for? | Splits ordered rows into 4 roughly equal-sized groups (quartiles) |
-- [+Business] the SQL way to build a quartile or decile segmentation directly in a query → Ch 27
-- §27.4 (and Ch 28 §28.3) | | Q71-040 | Can you use a window function's result in the same query's
-- WHERE clause? | No: window functions are calculated after WHERE; wrap the query in a subquery or
-- CTE and filter the outer layer | [+Edge cases] this is exactly why Q71-033 and Q71-035 wrap the
-- window function in a subquery before filtering, and Q71-074 shows the real error → Ch 13 §13.3 |

-- Q71-037, run (riverstone_2025). The running total over Q71-028's CTE:

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

/* The chapter shows:
      month    |  revenue  | running_total
   ------------+-----------+---------------
    2025-01-01 | 202640.00 |     202640.00
    2025-02-01 | 253664.00 |     456304.00
    2025-03-01 | 278007.50 |     734311.50
   (3 rows)
*/


-- [+Validate] the running total reconciles: 2,02,640 + 2,53,664 = 4,56,304 ✓, and + 2,78,007.50 =
-- 7,34,311.50 ✓. Each month appears once here, so RANGE and ROWS give the same answer; they part
-- company only when two rows share a month.

-- ---

-- =============================================================================================
-- 71.6 Classic problems: duplicates, gaps-and-islands, retention
-- =============================================================================================

-- =============================================================================================
-- Q71-041 · Find any duplicate customer names · Core
-- =============================================================================================

-- Remember it as: GROUP BY the thing that should be unique, HAVING COUNT > 1.

SELECT customer_name, COUNT(*)
FROM customers
GROUP BY customer_name
HAVING COUNT(*) > 1;


-- | Tier | What to say | |---|---| | Passes | The query above, correctly, with no result to show |
-- | Strong | + says that an empty result here is the real answer on this data, not a broken query,
-- and how they'd confirm it (run the same query on a column known to have duplicates, such as
-- city) | | Extra points | [+Edge cases] exact-name matching misses near-duplicates: trailing
-- spaces, case differences, "Sharma Hardware" vs. "Sharma Hardware Pvt Ltd". Those need TRIM/LOWER
-- first, or fuzzy matching, which is a different, harder problem · [+Business] near-duplicate
-- customer records are one of the most common real data-quality issues in a CRM, and this exact-
-- match query is only the first, cheapest check |

-- Likely follow-ups: How would you catch near-duplicates, not just exact ones? What would you do
-- once you found real duplicates: merge them how? Red flag: assuming an empty result means the
-- query is wrong, rather than considering that it might be the honest answer. Learn it in: Chapter
-- 12, section 12.9; Chapter 14, section 14.4 (exact and fuzzy duplicates).

-- =============================================================================================
-- Q71-042 · Find every customer's longest streak of consecutive order-days · Advanced
-- =============================================================================================

-- Remember it as: The gaps-and-islands trick: subtract a row number from the date. Rows in the
-- same streak land on the exact same result.

-- The query:

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


-- | Tier | What to say | |---|---| | Passes | Solves it with LAG: flag a row when the gap to the
-- previous date is more than 1 day, then a running SUM of the flags numbers the streaks. Correct,
-- but longer | | Strong | The row-number-minus-date query above, with the mechanism explained:
-- within one streak the date goes up by 1 each row and so does the row number, so their difference
-- stays constant; a gap breaks that and starts a new group. The last step keeps each customer's
-- longest streak, not every streak | | Extra points | [+Validate] the real result, honestly
-- reported: only 2-day streaks exist in this dataset, nothing longer, rather than a more
-- impressive-looking (fake) example · [+Signpost] name the pattern: this "constant difference"
-- trick solves any gaps-and-islands problem: consecutive login days, consecutive shipped orders,
-- consecutive price rises |

-- Likely follow-ups: Same, but for consecutive calendar weeks, not days? What's the equivalent
-- trick if the sequence isn't dates but plain row order? What changes if order_date were a
-- TIMESTAMP? (Cast it to DATE first, or the subtraction and the grouping both break.) Red flag:
-- reaching for a procedural loop (a cursor, or code outside SQL) as the only solution they can
-- think of. Learn it in: Chapter 13, section 13.8 (Pattern 8, streaks).

-- =============================================================================================
-- Q71-043 · Which customers ordered in both January and February 2025? (a simple retention check) · Core
-- =============================================================================================

-- Remember it as: Two EXISTS clauses, ANDed together: "ordered in month A" AND "ordered in month
-- B."

SELECT c.customer_id, c.customer_name
FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o
              WHERE o.customer_id = c.customer_id
                AND o.order_date BETWEEN '2025-01-01' AND '2025-01-31')
  AND EXISTS (SELECT 1 FROM orders o
              WHERE o.customer_id = c.customer_id
                AND o.order_date BETWEEN '2025-02-01' AND '2025-02-28')
ORDER BY c.customer_id;


-- | Tier | What to say | |---|---| | Passes | Two separate queries (January customers, February
-- customers), compared by eye: works for a one-off check, doesn't scale to "for every pair of
-- consecutive months" | | Strong | The double-EXISTS version above, or two conditional counts
-- compared in one row | | Extra points | [+Signpost] this is retention at its simplest: full
-- cohort retention extends it into a month-by-month grid, built with conditional aggregation
-- (SUM(CASE WHEN ... THEN 1 ELSE 0 END)) rather than repeated EXISTS (Chapter 13's Pattern 7
-- builds the full grid) · [+Business] January had only 5 active customers (Q71-027), so 4 of them
-- returning in February is a strong start; say what you'd compare it with before calling it good
-- or bad |

-- Likely follow-ups: Build a full 12-month retention grid? What's the difference between this and
-- a rolling "active in the last 30 days" count? Red flag: confusing "ordered in both months" with
-- "ordered at all in the date range" (missing the AND of two EXISTS). Learn it in: Chapter 12,
-- section 12.12 (EXISTS); Chapter 13, section 13.8 (Pattern 7, cohort retention).

-- =============================================================================================
-- Rapid-fire, §71.6 (Core)
-- =============================================================================================

-- | # | Question | One-line answer | Extra point | |---|---|---|---| | Q71-044 | Find products
-- that have never been sold? | LEFT JOIN products to order_items WHERE oi.product_id IS NULL, or
-- NOT EXISTS | [+Validate] verified on riverstone_2025: 0 rows, because all 8 products have sold.
-- On the mini database riverstone the same query returns Garden Chair: check which database you're
-- on → Ch 12 §12.10 | | Q71-045 | Find the Nth highest value in general, not just the 2nd? |
-- DENSE_RANK() OVER (ORDER BY x DESC), then filter WHERE rnk = N in an outer query | [+Edge cases]
-- the same tie-safety reasoning as Q71-033, for any N → Ch 13 §13.4 | | Q71-046 | Compute a
-- percentage of total per row? | 100.0  x / SUM(x) OVER (): no GROUP BY needed, since a window
-- with no PARTITION BY sees every row | [+Edge cases] multiply by 100.0 first: in PostgreSQL an
-- integer column divided by an integer total gives 0 (verified: quantity / SUM(quantity) OVER ()
-- 100 is 0 on every order line). MySQL's / always returns a decimal, so the bug only shows when
-- you port the query → Ch 13 §13.3 |

-- ---

-- =============================================================================================
-- 71.7 Schema, constraints, and transactions
-- =============================================================================================

-- The first three questions build small tables of their own. Run them in riverstone_lab, the
-- practice database from Chapter 12, section 12.13; every demo drops its tables at the end. The
-- foreign keys are written on their own line, as Chapter 12's dialect note in section 12.13
-- recommends: MySQL 8.4 and earlier silently ignore the shorter inline REFERENCES form, and InnoDB
-- doesn't support foreign keys on temporary tables at all.

-- =============================================================================================
-- Q71-047 · Demonstrate the difference between ON DELETE CASCADE and the default (NO ACTION) behavior · Core
-- =============================================================================================

-- Remember it as: CASCADE says "delete the children too." The default says "refuse to delete the
-- parent while children still exist."

-- Answer in one line: Without ON DELETE CASCADE, deleting a parent row is refused while any child
-- rows still reference it; with ON DELETE CASCADE, deleting the parent automatically deletes those
-- child rows too.

-- Verified, in riverstone_lab. With CASCADE (same statements in both databases):

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

/* The chapter shows:
    id | parent_id
   ----+-----------
    12 |         2
   (1 row)
*/


-- Rows 10 and 11, both children of parent 1, are gone too. Without CASCADE, the default:

CREATE TABLE parent_r (id INT PRIMARY KEY);
CREATE TABLE child_r (
  id        INT,
  parent_id INT,
  FOREIGN KEY (parent_id) REFERENCES parent_r (id)
);
INSERT INTO parent_r VALUES (1);
INSERT INTO child_r VALUES (10, 1);
DELETE FROM parent_r WHERE id = 1;

/* The chapter shows:
   ERROR:  update or delete on table "parent_r" violates foreign key constraint "child_r_parent_id_fkey" on table "child_r"
   DETAIL:  Key (id)=(1) is still referenced from table "child_r".
*/


-- Tidy up (same in both):

DROP TABLE child_t, parent_t, child_r, parent_r;


-- | Tier | What to say | |---|---| | Passes | "CASCADE deletes related rows too" (correct, no
-- comparison with the default) | | Strong | Both behaviors above, contrasted: cascade silently
-- removes children; the default blocks the delete with an error | | Extra points | [+Validate]
-- both real outcomes on parallel tables: 2 rows silently gone with CASCADE, 1 delete flatly
-- refused without it, in both databases · [+Edge cases] PostgreSQL's default is NO ACTION, checked
-- at the end of the statement (and deferrable); RESTRICT checks immediately. In MySQL the two are
-- identical · [+Business] CASCADE is powerful and dangerous: deleting one customer with CASCADE on
-- their orders would silently delete their whole order history. Keep it for truly dependent data
-- (an order's own line items), not for a parent whose "children" are valuable records in their own
-- right |

-- Likely follow-ups: What's ON DELETE SET NULL? When would you prefer it to CASCADE? What about ON
-- UPDATE CASCADE? Red flag: treating CASCADE as a safe default rather than a deliberate, case-by-
-- case decision. Learn it in: Chapter 12, section 12.13 (Step 6, the ON DELETE options, and the
-- dialect note in Step 3). ON UPDATE CASCADE and deferrable constraints are beyond the book.

-- =============================================================================================
-- Q71-048 · Write a CHECK constraint enforcing that a discount percentage is between 0 and 100, and show it rejecting bad data · Core
-- =============================================================================================

-- Remember it as: A CHECK constraint is a rule the database enforces on every write, not a rule
-- you hope the application remembers.

-- Verified, in riverstone_lab (same statements in both databases):

CREATE TABLE tx_check (
  id           INT,
  discount_pct NUMERIC(5,2),
  CONSTRAINT chk_discount CHECK (discount_pct BETWEEN 0 AND 100)
);
INSERT INTO tx_check VALUES (1, 50);
INSERT INTO tx_check VALUES (2, 150);

/* The chapter shows:
   ERROR:  new row for relation "tx_check" violates check constraint "chk_discount"
   DETAIL:  Failing row contains (2, 150.00).
*/


-- The first insert (50) succeeded; the second (150) was refused. Tidy up (same in both):

DROP TABLE tx_check;


-- | Tier | What to say | |---|---| | Passes | "A view is like a virtual table" (true, doesn't
-- explain the "re-run every time" mechanism) | | Strong | + a plain view has no stored data of its
-- own; every SELECT against it runs the underlying query fresh, so it's always current, and it
-- costs the full query every time | | Extra points | [+Validate] the top three match what the
-- underlying GROUP BY query returns when you run it directly (Q71-073), since that's literally
-- what the view does · [+Trade-offs] a materialized view (CREATE MATERIALIZED VIEW, PostgreSQL
-- only; MySQL has none) stores the result, so it's fast to query but stale until you run REFRESH
-- MATERIALIZED VIEW: a trade between freshness and speed. In MySQL the equivalent is a summary
-- table refreshed by a scheduled job · [+Business] a view is also a clean way to hide a complex
-- join behind a simple name for less technical users, and to enforce row-level access (a view
-- showing only a rep's own accounts) without repeating the logic in every query |

-- Likely follow-ups: Can you INSERT into a view? (Sometimes, for simple views, with restrictions.)
-- What does querying a view built on another view cost? Red flag: believing a plain view stores a
-- copy of the data at creation time. Learn it in: Chapter 13, section 13.2 (views); Chapter 28,
-- section 28.11 (materialized views).

-- =============================================================================================
-- Q71-050 · Demonstrate that ROLLBACK actually undoes a change, not just "cancels" it · Core
-- =============================================================================================

-- Remember it as: Nothing inside BEGIN…COMMIT is permanent until COMMIT. ROLLBACK makes it as if
-- it never happened at all.

-- Answer in one line: A transaction's changes are only permanent once COMMIT runs; ROLLBACK
-- reverts every change made since BEGIN, restoring the exact earlier state.

-- Verified, in riverstone_lab (same statements in both databases; MySQL also accepts START
-- TRANSACTION for BEGIN):

CREATE TABLE tx_test (id INT, val VARCHAR(20));
INSERT INTO tx_test VALUES (1, 'original');


BEGIN;
UPDATE tx_test SET val = 'changed' WHERE id = 1;
SELECT * FROM tx_test;   -- inside the open transaction
ROLLBACK;
SELECT * FROM tx_test;   -- after ROLLBACK
DROP TABLE tx_test;

/* The chapter shows:
    id |   val
   ----+---------
     1 | changed
   (1 row)
   
    id |   val
   ----+----------
     1 | original
   (1 row)
*/


-- | Tier | What to say | |---|---| | Passes | "ROLLBACK undoes changes" (correct, no demonstration
-- of the mechanism) | | Strong | + explains that the UPDATE is visible within the same session
-- immediately, but is not permanent until COMMIT, and ROLLBACK discards it entirely | | Extra
-- points | [+Validate] the live proof above: the same SELECT, before and after ROLLBACK, gives two
-- different real answers on the same table · [+Business] this is why multi-step operations (move
-- money between two accounts, place an order and reduce stock together) belong in one transaction:
-- if step two fails, ROLLBACK guarantees step one never sticks around half-finished |

-- Likely follow-ups: What does COMMIT do that makes a change durable? What happens if the
-- connection drops before either COMMIT or ROLLBACK runs? (The transaction is rolled back
-- automatically.) Red flag: not knowing that changes are visible inside the same session before
-- commit, and invisible to other sessions until commit. Learn it in: Chapter 12, section 12.13
-- (Step 8, transactions).

-- =============================================================================================
-- Q71-051 · What does ACID stand for? Give one real example of each · Core
-- =============================================================================================

-- Remember it as: Atomic: all or nothing. Consistent: rules always hold. Isolated: transactions
-- don't see each other's half-finished work. Durable: once committed, it survives a crash.

-- Answer in one line: Atomicity (a transaction fully succeeds or fully fails, no partial state),
-- Consistency (every committed change leaves the data obeying its declared rules), Isolation
-- (concurrent transactions don't see each other's uncommitted changes), Durability (once
-- committed, a change survives a crash or power loss).

-- | Tier | What to say | |---|---| | Passes | Can name what the letters stand for, can't give a
-- concrete example of any of them | | Strong | + one real example each: Atomicity (Q71-050's
-- transfer example: both the debit and the credit happen, or neither does) · Consistency (a CHECK
-- constraint, Q71-048, refusing an invalid row) · Isolation (two people checking stock at once
-- shouldn't both believe the last unit is theirs) · Durability (a committed order survives the
-- database server crashing five seconds later) | | Extra points | [+Edge cases] isolation comes in
-- levels (Q71-056), so "isolated" isn't one fixed behavior but a range of trade-offs · [+Business]
-- these four properties are why a relational database, not a plain file, is the default for
-- anything involving money or stock, where a value must never silently go wrong |

-- Likely follow-ups: Which of the four is hardest to guarantee at scale? Which systems
-- deliberately relax some of them, and why? Red flag: reciting the acronym with no example for any
-- letter. Learn it in: Chapter 12, section 12.13 (Step 8, transactions); Chapter 49, section 49.4
-- (ACID).

-- =============================================================================================
-- Beyond the book: concurrency in five minutes
-- =============================================================================================

-- The last four rapid-fire rows below (Q71-056 to Q71-059) go beyond the teaching chapters, so
-- here is the short explanation they need. When two sessions work on the same table at once, the
-- isolation level decides what one session can see of the other's unfinished work. Each database
-- has a default. Check yours:

SHOW default_transaction_isolation;

/* The chapter shows:
    default_transaction_isolation
   -------------------------------
    read committed
   (1 row)
*/


-- MySQL:

SELECT @@transaction_isolation;

/* The chapter shows:
   +-------------------------+
   | @@transaction_isolation |
   +-------------------------+
   | REPEATABLE-READ         |
   +-------------------------+
*/


-- SHOW reads one of PostgreSQL's settings by name; in MySQL, @@ in front of a name reads a server
-- setting (a system variable) the same way. So PostgreSQL starts every transaction at Read
-- Committed, and MySQL at Repeatable Read.

-- A dirty read is the thing the weakest level allows. Picture two sessions, A and B, and an order
-- whose status is 'Pending':

-- | Step | Session A | Session B | What B sees | |---|---|---|---| | 1 | BEGIN; UPDATE orders SET
-- status = 'Shipped' WHERE order_id = 10001; | | | | 2 | | SELECT status FROM orders WHERE
-- order_id = 10001; | Read Uncommitted: 'Shipped' (a dirty read). Read Committed or stricter:
-- 'Pending' | | 3 | ROLLBACK; | | | | 4 | | the same SELECT again | 'Pending': the "Shipped" B may
-- have seen in step 2 never existed |

-- Neither database allows a dirty read by default. Both let a plain SELECT in B go ahead at step 2
-- without waiting for A: each keeps the last committed version of the row for readers, an idea
-- called MVCC (multi-version concurrency control).

-- =============================================================================================
-- Rapid-fire, §71.7 (Core; Q71-056 to Q71-059 Advanced)
-- =============================================================================================

-- | # | Question | One-line answer | Extra point | |---|---|---|---| | Q71-052 | ALTER TABLE ...
-- ADD COLUMN with a default value on a huge table: what should you know? | PostgreSQL 11 and later
-- add a column with a constant default instantly, without rewriting every row; older versions, and
-- some other engines, rewrite the whole table, which can lock it for a long time | [+Business]
-- check your engine and version before assuming a schema change on a huge production table is
-- "instant" → Ch 28 §28.12 (changing a live database); the version detail is beyond the book | |
-- Q71-053 | What's the difference between a PRIMARY KEY and a UNIQUE constraint? | A table has at
-- most one PRIMARY KEY (which also forbids NULL); it can have many UNIQUE constraints, and each
-- still allows multiple NULLs (Q71-013) | [+Edge cases] this is why an email UNIQUE constraint
-- doesn't stop multiple blank emails, but adding NOT NULL to the UNIQUE column would. (A CHECK
-- (email <> '') also blocks empty text, per Q71-022) → Ch 12 §12.13 | | Q71-054 | What does NOT
-- NULL enforce, and can you add it to a column that already has data? | It rejects any future NULL
-- in that column; adding it to an existing column needs every current value to be non-NULL
-- already, or the ALTER TABLE itself fails | [+Edge cases] run a check first, SELECT COUNT(*) FROM
-- t WHERE col IS NULL, before adding NOT NULL to a live table → Ch 12 §12.13 (Step 9) | | Q71-055
-- | What's a materialized-view refresh strategy, in one sentence? | Refresh on a schedule
-- (nightly, hourly), or refresh from a trigger or pipeline step after the source loads (PostgreSQL
-- has no automatic refresh), chosen by how stale the data may get | [+Business] the same
-- freshness-vs-cost trade as a Power BI scheduled refresh, one layer down → Ch 28 §28.11; Ch 46
-- (pipeline steps); Ch 16 §16.9 (Power BI refresh) | | Q71-056 | What's a transaction isolation
-- level, in plain terms? | A setting for how much of another transaction's unfinished work you can
-- see while your own transaction runs | [+Edge cases] from loosest to strictest: Read Uncommitted,
-- Read Committed (PostgreSQL's default), Repeatable Read (MySQL InnoDB's default), Serializable
-- (both checked above) → Beyond the book (the box above) | | Q71-057 | What's a "dirty read"? |
-- Reading another transaction's uncommitted change, which might still be rolled back and never
-- happen | [+Edge cases] only possible at Read Uncommitted; PostgreSQL doesn't implement that
-- level separately and behaves as Read Committed even if you ask for it → Beyond the book (the box
-- above) | | Q71-058 | What's a deadlock? | Two transactions each waiting for a lock the other one
-- holds, so neither can ever proceed | [+Business] the database detects it and rolls back one of
-- the two transactions rather than letting both hang forever; application code should catch that
-- error and retry → Beyond the book | | Q71-059 | Does a SELECT ever get blocked by another
-- transaction's write? | Under each engine's default level (Read Committed in PostgreSQL,
-- Repeatable Read in MySQL), a plain SELECT isn't blocked: it reads the last committed version |
-- [+Edge cases] the exception is a locking read, SELECT … FOR UPDATE, which does wait for the
-- writer. Plain reads don't wait because of MVCC → Beyond the book (the box above) |

-- ---

-- =============================================================================================
-- 71.8 PostgreSQL vs. MySQL: where the dialects actually differ
-- =============================================================================================

-- Every pair below was run on both databases against the same Riverstone data.

-- =============================================================================================
-- Q71-060 · String aggregation: STRING_AGG vs. GROUP_CONCAT · Core
-- =============================================================================================

-- Remember it as: Same job, different name, different separator syntax.

-- PostgreSQL:

SELECT category,
       STRING_AGG(DISTINCT product_name, ', ' ORDER BY product_name) AS products
FROM products
GROUP BY category
ORDER BY category;

/* The chapter shows:
     category  |                    products
   ------------+------------------------------------------------
    Furniture  | Garden Chair
    Industrial | Industrial Crate
    Kitchen    | Food Container Set, Lunch Box Set, Water Bottle 1L
    Storage    | Stackable Bin, Storage Box 10L, Storage Box 25L
   (4 rows)
*/


-- MySQL:

SELECT category,
       GROUP_CONCAT(DISTINCT product_name ORDER BY product_name SEPARATOR ', ') AS products
FROM products
GROUP BY category
ORDER BY category;

/* The chapter shows:
   +------------+----------------------------------------------------+
   | category   | products                                           |
   +------------+----------------------------------------------------+
   | Furniture  | Garden Chair                                       |
   | Industrial | Industrial Crate                                   |
   | Kitchen    | Food Container Set, Lunch Box Set, Water Bottle 1L |
   | Storage    | Stackable Bin, Storage Box 10L, Storage Box 25L    |
   +------------+----------------------------------------------------+
*/


-- | Tier | What to say | |---|---| | Passes | Knows one function, not the other engine's name for
-- it | | Strong | Both function names and their (slightly different) syntax for the separator | |
-- Extra points | [+Validate] the same four lines from both engines, above · [+Edge cases] MySQL's
-- GROUP_CONCAT has a length limit (group_concat_max_len, 1,024 bytes by default) and silently cuts
-- off longer results: worth knowing before it bites in production |

-- Learn it in: Chapter 14, section 14.4 (STRING_AGG, with MySQL's GROUP_CONCAT in the same
-- paragraph). group_concat_max_len is beyond the book.

-- =============================================================================================
-- Rapid-fire, §71.8 (Core): dialect differences
-- =============================================================================================

-- | # | Feature | PostgreSQL | MySQL | Extra point | |---|---|---|---|---| | Q71-061 | NULL
-- replacement | COALESCE(x, 'default') | IFNULL(x, 'default') or COALESCE (both work) | [+Edge
-- cases] MySQL supports COALESCE too; IFNULL is a MySQL shorthand for the two-argument case → Ch
-- 12 §12.7 (COALESCE); IFNULL is beyond the book | | Q71-062 | Auto-incrementing primary key |
-- GENERATED ALWAYS AS IDENTITY (older code: SERIAL) | AUTO_INCREMENT | [+Business] copy-pasting a
-- CREATE TABLE between engines without translating this is one of the most common cross-dialect
-- errors → Ch 12 §12.13 (Steps 2 and 3) | | Q71-063 | Limiting and skipping rows | LIMIT n OFFSET
-- m | LIMIT m, n (offset first!) or LIMIT n OFFSET m (also works) | [+Edge cases] MySQL's LIMIT m,
-- n puts the offset first, a common source of swapped-number bugs when porting a query → Ch 12
-- §12.5 (LIMIT); OFFSET is beyond the book | | Q71-064 | Current date and time | CURRENT_DATE,
-- NOW() | CURRENT_DATE (or CURDATE()), NOW() | [+Trade-offs] CURRENT_DATE and NOW() work in both;
-- prefer CURRENT_DATE for portability. The real difference is date arithmetic → Ch 12 §12.16
-- (DATEDIFF and INTERVAL) | | Q71-065 | Case of table and column names | Unquoted names are folded
-- to lower case | Table names are case-sensitive on Linux and case-insensitive on Windows and
-- macOS by default | [+Edge cases] a query that works on a laptop can fail on a Linux production
-- MySQL server purely because of table-name casing: use lower-case names everywhere → Ch 12 §12.13
-- (the "Naming" note) | | Q71-066 | Boolean type | Native BOOLEAN, true/false | BOOLEAN is an
-- alias for TINYINT(1) | [+Edge cases] MySQL's "boolean" columns are really small integers, which
-- is why 0/1 and FALSE/TRUE are interchangeable there (and why Q71-009 prints 1) → Ch 12 §12.13 |
-- | Q71-067 | Window functions | Full support since PostgreSQL 8.4 | Full support since MySQL 8.0
-- (not in 5.7 or earlier) | [+Business] if a company runs an older MySQL, ask whether window
-- functions are available before assuming this chapter's window questions (Q71-033 to Q71-040,
-- Q71-042, Q71-045, Q71-046 and Q71-074) apply as written → Ch 13 §13.9 |

-- ---

-- =============================================================================================
-- 71.9 Query optimization and indexes
-- =============================================================================================

-- =============================================================================================
-- Q71-068 · What does EXPLAIN show, and what did it show on Riverstone's orders table? · Advanced
-- =============================================================================================

-- Remember it as: EXPLAIN tells you what the database plans to do, not what you assume it does.

-- Answer in one line: EXPLAIN shows the query planner's chosen strategy (a sequential scan, an
-- index scan, a join method) and its estimated cost, before running the query.

-- Verified (riverstone_2025), on the 175-row orders table:

EXPLAIN SELECT * FROM orders WHERE customer_id = 1;

/* The chapter shows:
                          QUERY PLAN
   --------------------------------------------------------
    Seq Scan on orders  (cost=0.00..4.19 rows=16 width=25)
      Filter: (customer_id = 1)
   (2 rows)
*/


-- MySQL: InnoDB builds an index for every foreign key automatically, so MySQL already has one on
-- orders.customer_id and uses it (type is ref, key is customer_id) before you add anything.
-- FORMAT=TRADITIONAL asks for the plan as a table, which looks the same on every version; MySQL 9
-- otherwise prints the one-line tree that Chapter 28, section 28.13 reads (-> Index lookup on
-- orders using customer_id …). Ending the statement with \G instead of ; makes the mysql client
-- print each column on its own line, which is easier to read for a wide result like this one:

EXPLAIN FORMAT=TRADITIONAL SELECT * FROM orders WHERE customer_id = 1\G

/* The chapter shows:
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
*/


-- | Tier | What to say | |---|---| | Passes | "EXPLAIN shows you the query plan" | | Strong | +
-- explains what a sequential scan means (reads every row) versus an index scan (jumps straight to
-- the matching rows) | | Extra points | [+Validate] the real surprise above: even with an index,
-- PostgreSQL's planner still chose a sequential scan on this table, and that's not a bug: on 175
-- rows, reading everything is cheaper than the extra work of using an index, and the planner knows
-- it · [+Edge cases] this is the honest answer to "why isn't my index being used?": indexes pay
-- off on large tables, not small ones, and a planner that ignores a small table's index is doing
-- its job · [+Trade-offs] rows=16 is the planner's estimate, and it matches Sharma Hardware's 16
-- orders (Q71-034); EXPLAIN ANALYZE runs the query and adds the real counts and timings |

-- Likely follow-ups: At what table size would you expect the planner to switch to the index?
-- What's the difference between a sequential scan and an index scan in disk reads? Red flag:
-- assuming an index is always used just because it exists. Learn it in: Chapter 28, sections
-- 28.4–28.5 (and section 28.6 for indexes; Chapter 49 for storage at scale).

-- =============================================================================================
-- Rapid-fire, §71.9 (Advanced)
-- =============================================================================================

-- | # | Question | One-line answer | Extra point | |---|---|---|---| | Q71-069 | Which columns
-- usually benefit most from an index? | Columns often used in WHERE, JOIN … ON and ORDER BY,
-- especially on large tables | [+Trade-offs] every index speeds up reads but slows down writes
-- (INSERT/UPDATE/DELETE must keep it up to date too): indexing everything is not free → Ch 28
-- §28.6 | | Q71-070 | What's a composite index, and when does column order matter? | An index on
-- several columns together; it helps most when a query filters on the leading column(s), in the
-- order the index was built | [+Edge cases] an index on (customer_id, order_date) speeds up WHERE
-- customer_id = X AND order_date > Y, but doesn't help a query filtering on order_date alone → Ch
-- 28 §28.6 | | Q71-071 | What's a covering index? | An index that holds every column a query
-- needs, so the database answers from the index alone without reading the table rows | [+Business]
-- one of the highest-impact, lowest-effort fixes for a frequently run report query → Ch 28 §28.6 |

-- ---

-- =============================================================================================
-- 71.10 Live-coding walk-throughs
-- =============================================================================================

-- =============================================================================================
-- Q71-072 · Walk-through: revenue by order, with a fan-out warning · Core
-- =============================================================================================

-- What they're really testing: whether you notice a join that silently multiplies rows before you
-- trust the total it produces.

-- The setup, talked through live: "I need each order's revenue. Orders join to order_items for the
-- line amounts. If this business also has invoices and payments tables, and I'm tempted to join
-- through both to get to 'paid revenue,' I need to check first whether an invoice can have more
-- than one payment, because that join would then count the order's revenue once per payment."

-- Verified (riverstone, the mini database): it has exactly this shape: order 5006's invoice has 2
-- payment rows. The wrong way, joining through invoices and payments before adding up the line
-- items:

SELECT o.order_id,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS wrong_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN invoices i     ON o.order_id = i.order_id
JOIN payments p     ON i.invoice_id = p.invoice_id
WHERE o.order_id = 5006
GROUP BY o.order_id;

/* The chapter shows:
    order_id | wrong_total
   ----------+-------------
        5006 |    29280.00
   (1 row)
*/


-- The right way, adding up the line items on their own, with payments left out:

SELECT o.order_id,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS correct_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_id = 5006
GROUP BY o.order_id;

/* The chapter shows:
    order_id | correct_total
   ----------+---------------
        5006 |      14640.00
   (1 row)
*/


-- The order's revenue is ₹14,640. The fan-out join reports ₹29,280: exactly double, because its
-- invoice has exactly 2 payments.

-- Extra-points moves demonstrated: [+Edge cases] expected the fan-out before running anything,
-- from knowing an invoice can have several payments. [+Validate] proved it with a real doubled
-- number on this exact order, not a hypothetical. [+Business] stated the fix plainly: compute
-- revenue from order_items alone, and join to payments (if at all) only for payment-status
-- questions, never in the same sum as revenue.

-- Likely follow-ups: How would you check for this kind of fan-out risk before writing the query,
-- on a schema you've never seen? How would you fix a report that has already shipped with this
-- bug? Red flag: trusting a multi-join total without asking whether any joined table could have
-- more than one matching row per order. Learn it in: Chapter 12, section 12.10 (join fan-out);
-- Chapter 13, section 13.8 (Pattern 10, checks before you trust a report).

-- <!-- db: riverstone_2025 -->

-- =============================================================================================
-- Q71-073 · Walk-through: "give me our top customers": the clarifying-question round · Core
-- =============================================================================================

-- What they're really testing: whether you ask before you build, on a question that's genuinely
-- ambiguous.

-- Talked through live: "'Top customers' could mean several things, and each needs a different
-- query: by total revenue, by revenue this year only, by order count, or by average order value.
-- I'll ask which, and while I wait I'll build the total-revenue version, since that's the most
-- common meaning."

SELECT c.customer_id, c.customer_name,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 2) AS total_revenue
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_revenue DESC
LIMIT 5;


-- Extra-points moves demonstrated: [+Clarify] named the real ambiguity instead of guessing
-- silently. [+Simple first] still produced a working, reasonable default answer while waiting,
-- rather than stalling on the clarifying question. [+Edge cases] left out cancelled orders, a
-- decision stated out loud rather than assumed. [+Validate] the first three match Q71-049's view
-- exactly.

-- Likely follow-ups: Now by average order value instead. Now for a specific date range. Now
-- leaving out one large outlier customer: how would you handle that request? Red flag: picking one
-- interpretation silently and never mentioning that the ambiguity existed. Learn it in: Chapter
-- 12, sections 12.9–12.10; Chapter 69, Move 1 (clarify first).

-- =============================================================================================
-- Q71-074 · Walk-through: does each customer's spend beat their own earlier average? · Advanced
-- =============================================================================================

-- What they're really testing: whether you can compare a row with the same customer's own history
-- without a self-join, using a window frame most candidates have only seen in its default form.

-- Talked through live: "I need each customer-month's revenue, then the average of that customer's
-- own earlier months only. A plain AVG() OVER (PARTITION BY customer_id) averages every month,
-- future ones included. Adding ORDER BY month still includes the current row. I need a frame that
-- ends at 1 PRECEDING: everything before the current row, nothing after."

-- A common first attempt puts the window function straight into WHERE. That fails, for the reason
-- in Q71-040: window functions run after WHERE.

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

/* The chapter shows:
   ERROR:  window functions are not allowed in WHERE
*/


-- (MySQL's wording: ERROR 3593 (HY000): You cannot use the window function 'avg' in this
-- context.') The fix: calculate the window in a CTE (with_avg) and filter the outer query, the
-- same pattern as Q71-033 and Q71-035.

-- Verified (riverstone_2025):

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

/* The chapter shows:
    customer_id |   month    | revenue  | prior_avg
   -------------+------------+----------+-----------
              1 | 2025-03-01 | 64387.50 |  63656.25
              1 | 2025-10-01 | 96825.00 |  34443.89
              1 | 2025-11-01 | 82250.00 |  40682.00
   (3 rows)
*/


-- MySQL: the same DATE_FORMAT swap as in Q71-028 (ROUND(x, 2) already works in both); it returns
-- the same three rows.

-- Extra-points moves demonstrated: [+Edge cases] caught the default-frame trap before writing any
-- code, not after a wrong answer. [+Validate] customer 1's October revenue (₹96,825) against an
-- earlier average of only ₹34,443.89: a real, large beat, and November's average checks by hand,
-- (9 × 34,443.89 + 96,825) ÷ 10 = 40,682.00. [+Business] "is this customer trending up against
-- their own history" is a useful account-health signal, different from comparing customers with
-- each other.

-- Likely follow-ups: What if you wanted a 3-month trailing average instead of all earlier months?
-- How would this change using LAG instead of a frame clause? Red flag: using the default window
-- frame and not noticing the current row leaking into its own comparison average. Learn it in:
-- Chapter 13, section 13.6; Chapter 28, section 28.3 (frames that end before the current row).

-- =============================================================================================
-- Q71-075 · Walk-through: pivot monthly revenue by category into columns, live · Core
-- =============================================================================================

-- What they're really testing: whether conditional aggregation (CASE inside SUM) comes to mind,
-- since standard SQL has no PIVOT keyword the way spreadsheets and a few database platforms do.

-- Talked through live: "There's no universal PIVOT in standard SQL. The standard trick is
-- conditional aggregation: one SUM(CASE WHEN category = X THEN revenue ELSE 0 END) per category I
-- want as a column, one column for each of the four categories."

-- Verified (riverstone_2025), the first three months:

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

/* The chapter shows:
      month    |  storage  | kitchen  | industrial | furniture
   ------------+-----------+----------+------------+-----------
    2025-01-01 | 172240.00 | 30400.00 |       0.00 |      0.00
    2025-02-01 | 150231.50 | 54152.50 |   49280.00 |      0.00
    2025-03-01 | 180785.00 | 49335.00 |   31500.00 |  16387.50
   (3 rows)
*/


-- MySQL: the same DATE_FORMAT swap as in Q71-028; it returns the same three rows.

-- Extra-points moves demonstrated: [+Edge cases] January's Industrial column shows 0, not a blank
-- or an error: a real month with no Industrial sales, handled by the ELSE 0 in each CASE. And
-- leave a category out and its revenue silently disappears from the row total. [+Trade-offs] this
-- only works for a category list known in advance, written into the query; a changing set of
-- categories needs pivoting in the application or engine-specific dynamic SQL. [+Validate] each
-- row's four columns add up to that month's total in Q71-028: January 1,72,240 + 30,400 = 2,02,640
-- ✓; February 1,50,231.50 + 54,152.50 + 49,280 = 2,53,664 ✓; March 1,80,785 + 49,335 + 31,500 +
-- 16,387.50 = 2,78,007.50 ✓, and March only reconciles because the Furniture column is there.

-- Likely follow-ups: What if the list of categories isn't known ahead of time? How would you do
-- this in a BI tool instead of raw SQL? Red flag: reaching for a non-standard PIVOT keyword
-- without checking whether the engine supports it. Learn it in: Chapter 13, section 13.8 (Pattern
-- 9, pivot rows into columns); Chapter 11, section 11.5 (pivot tables) for the spreadsheet
-- version.

-- =============================================================================================
-- Q71-076 · Walk-through: profile a table you've never seen before, in one query · Core
-- =============================================================================================

-- What they're really testing: whether you have a fast, repeatable first move for an unfamiliar
-- table, rather than guessing or scrolling through raw rows.

-- Talked through live: "Before I write anything specific, I want a quick health check: the row
-- count, how many NULLs in the columns that matter, the distinct count of what should be a key,
-- and the date range. One query, several aggregates at once."

-- Verified (riverstone_2025), on the orders table:

SELECT
  COUNT(*)                                     AS total_rows,
  COUNT(*) - COUNT(sales_rep_id)               AS null_sales_rep,
  COUNT(DISTINCT customer_id)                  AS distinct_customers,
  MIN(order_date)                              AS earliest,
  MAX(order_date)                              AS latest,
  COUNT(*) FILTER (WHERE status = 'Cancelled') AS cancelled_count
FROM orders;

/* The chapter shows:
    total_rows | null_sales_rep | distinct_customers |  earliest  |   latest   | cancelled_count
   ------------+----------------+--------------------+------------+------------+-----------------
           175 |             11 |                 23 | 2025-01-02 | 2025-12-23 |               2
   (1 row)
*/


-- MySQL: there is no FILTER; count with SUM(CASE … THEN 1 ELSE 0 END) instead:

SELECT
  COUNT(*)                                              AS total_rows,
  COUNT(*) - COUNT(sales_rep_id)                        AS null_sales_rep,
  COUNT(DISTINCT customer_id)                           AS distinct_customers,
  MIN(order_date)                                       AS earliest,
  MAX(order_date)                                       AS latest,
  SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_count
FROM orders;

/* The chapter shows:
   +------------+----------------+--------------------+------------+------------+-----------------+
   | total_rows | null_sales_rep | distinct_customers | earliest   | latest     | cancelled_count |
   +------------+----------------+--------------------+------------+------------+-----------------+
   |        175 |             11 |                 23 | 2025-01-02 | 2025-12-23 |               2 |
   +------------+----------------+--------------------+------------+------------+-----------------+
*/

