-- Chapter 82. Take-Home Assignments & Mock Interviews
-- Practice SQL for POSTGRESQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_postgresql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch82-take-home-assignments-and-mock-interviews.md


-- =============================================================================================
-- Chapter 82. Take-Home Assignments & Mock Interviews
-- =============================================================================================

-- Part 8 — Be Interview Ready

-- > Chapter at a glance > > You will learn to: judge whether a take-home assignment is fair before
-- you start it · complete a take-home the way a strong candidate actually would, not just
-- technically correctly, but with the judgment and communication a reviewer is scoring · sit
-- through a realistic mock interview and hear what a strong answer and a weaker one sound like at
-- the same turn · read interviewer scoring notes and understand what actually moved the score. > >
-- Before you start: Chapter 69 (the five-dimension rubric and the twelve extra-point tags). The
-- take-homes use SQL from Chapters 12 and 13, the lead model from Chapters 36, 37 and 39, and the
-- pipeline ideas from Chapters 45–47. The mocks draw on the banks in Chapters 71, 74, 76A, 76B, 77
-- and 81. This chapter rehearses those skills; it doesn't teach them again, and each section says
-- where each one is taught. > > Time needed: 2–3 hours to read the chapter and run every query and
-- cell; about 10–12 hours if you also do all three take-homes against the clock (2 + 3 + 2 hours),
-- compare them with the scoring tables, and record one mock. > > How this chapter is built. Three
-- complete take-homes and three scored mock interviews, one each for Data Analyst, Data Scientist
-- and Data Engineer. Business analysts can adapt the Data Analyst take-home using Chapter 76B's
-- elicitation questions; automation and BI candidates can adapt the Data Engineer one. Each take-
-- home gives the assignment as a candidate would receive it, a model submission, a scoring table
-- and what a weak submission looks like. Every model submission was actually run: the SQL on
-- PostgreSQL 16 against the Riverstone databases, the Python on Python 3.11.15 with scikit-learn
-- 1.9.1 (the book recommends Python 3.14, Chapter 17, section 17.0; nothing here depends on the
-- version), and every output shown is the real one. The mocks are condensed transcripts: each long
-- answer is written out once, in full, and each mock shows a weaker answer next to the stronger
-- one at two of its turns, with Chapter 69's scores and tags.

-- ---

-- =============================================================================================
-- 82.0 Before you start: is this a fair take-home?
-- =============================================================================================

-- A take-home is unpaid work, so judge it before you begin. Chapter 8 promised this chapter would
-- show what a fair one looks like.

-- A fair take-home has:

-- - a stated time limit, usually no more than about 4 hours; - synthetic or public data, or a
-- sample prepared for the exercise; - a clear deliverable ("a one-page summary plus the queries"),
-- and a named person to send questions to.

-- Warning signs:

-- - an open-ended brief such as "build our churn feature" or "redesign our pipeline"; - the
-- company's real client data, or a problem that looks like their live backlog; - no time limit, or
-- an estimate of several days of unpaid work.

-- What to do:

-- - Ask for scope clarification in writing, early: "Should I assume X, or Y?" A reviewer reads
-- that as good judgment, not weakness. - Say how long you spent, at the top of your submission. -
-- It's fine to deliver the time-boxed version with a "what I'd do next" list, exactly as the Data
-- Engineer submission in section 82.3 does. Over-delivering on a fair take-home rarely changes the
-- result; over-delivering on an unfair one teaches the company that you'll work for free.

-- All three assignments below pass this test: each has a time limit, practice data from this book,
-- and a one-page deliverable.

-- ---

-- <!-- db: riverstone_2025 -->

-- =============================================================================================
-- 82.1 Take-home assignment: Data Analyst
-- =============================================================================================

-- =============================================================================================
-- The assignment, as given
-- =============================================================================================

-- > "Riverstone's sales leadership wants to understand which product categories are driving growth
-- and which need attention. Using the attached order data, prepare a short analysis (a one-page
-- summary plus supporting queries/code) answering: which categories are performing best and worst,
-- what's driving the difference, and one specific recommendation. You have 2 hours."

-- Practice data: riverstone_2025 (Chapter 13, section 13.1): all of 2025, 24 customers, 175
-- orders, 173 of them not cancelled.

-- =============================================================================================
-- Model submission
-- =============================================================================================

-- Step 1: the core numbers. Revenue, orders and customers by category, leaving out cancelled
-- orders:

SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 2) AS revenue,
       COUNT(DISTINCT o.order_id)    AS orders,
       COUNT(DISTINCT o.customer_id) AS customers
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
JOIN products    AS p  ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY revenue DESC;

/* The chapter shows:
     category  |  revenue   | orders | customers
   ------------+------------+--------+-----------
    Storage    | 2297973.50 |    142 |        23
    Kitchen    | 1208030.00 |     85 |        16
    Industrial |  795830.00 |     23 |         5
    Furniture  |   33637.50 |      2 |         2
   (4 rows)
*/


-- - The revenue formula is Chapter 12's (section 12.9): quantity × price charged × (1 − discount).
-- ROUND(…, 2) keeps two decimals; without it PostgreSQL prints the raw result of the division,
-- with twenty decimal places. - COUNT(DISTINCT …) counts each order and each customer once,
-- however many lines they have (the fan-out trap, section 12.10). - Check it reconciles: the four
-- revenues add up to ₹43,35,471, Riverstone's 2025 revenue (Chapter 10). The order counts add up
-- to 252, more than the 173 orders, because most orders contain more than one category. So
-- "orders" here means orders that include this category. - Industrial's 23 orders come from only 5
-- customers.

-- Step 2: one level deeper, checking whether Industrial's smaller order count is offset by more
-- spend per order. A first attempt averaged per order line, not per order: silently the wrong
-- grain. The fix is to add up each order's spend in the category first, then average those order
-- totals:

WITH order_category_revenue AS (
  SELECT o.order_id,
         p.category,
         SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
  FROM orders AS o
  JOIN order_items AS oi ON o.order_id = oi.order_id
  JOIN products    AS p  ON oi.product_id = p.product_id
  WHERE o.status <> 'Cancelled'
  GROUP BY o.order_id, p.category
)
SELECT category,
       ROUND(AVG(order_revenue), 2) AS avg_category_spend_per_order,
       COUNT(*) AS n_orders
FROM order_category_revenue
GROUP BY category
ORDER BY avg_category_spend_per_order DESC;

/* The chapter shows:
     category  | avg_category_spend_per_order | n_orders
   ------------+------------------------------+----------
    Industrial |                     34601.30 |       23
    Furniture  |                     16818.75 |        2
    Storage    |                     16182.91 |      142
    Kitchen    |                     14212.12 |       85
   (4 rows)
*/


-- - The CTE (Chapter 13, section 13.2) makes one row per order and category; the outer query
-- averages those rows. Averaging order-level totals, not lines, is the grain rule from Chapter 12,
-- section 12.12. - The column name says what it is: the spend on this category's items in an order
-- that includes it, not the size of the whole basket. - Check it agrees with Step 1: ₹22,97,973.50
-- ÷ 142 = ₹16,182.91 ✓, and ₹7,95,830 ÷ 23 = ₹34,601.30 ✓.

-- Step 3: growth, which is what the question actually asked. Revenue by quarter, and the second
-- half of the year against the first. This is the quarterly pivot from Chapter 12's exercise 32,
-- with one column added:

WITH sales_lines AS (
  SELECT p.category,
         EXTRACT(QUARTER FROM o.order_date) AS qtr,
         oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS line_revenue
  FROM orders AS o
  JOIN order_items AS oi ON o.order_id = oi.order_id
  JOIN products    AS p  ON oi.product_id = p.product_id
  WHERE o.status <> 'Cancelled'
)
SELECT category,
       ROUND(SUM(CASE WHEN qtr = 1 THEN line_revenue ELSE 0 END), 0) AS q1,
       ROUND(SUM(CASE WHEN qtr = 2 THEN line_revenue ELSE 0 END), 0) AS q2,
       ROUND(SUM(CASE WHEN qtr = 3 THEN line_revenue ELSE 0 END), 0) AS q3,
       ROUND(SUM(CASE WHEN qtr = 4 THEN line_revenue ELSE 0 END), 0) AS q4,
       ROUND(100.0 * SUM(CASE WHEN qtr >= 3 THEN line_revenue ELSE 0 END)
                   / SUM(CASE WHEN qtr <= 2 THEN line_revenue ELSE 0 END) - 100, 0)
         AS h2_vs_h1_pct
FROM sales_lines
GROUP BY category
ORDER BY q4 DESC;

/* The chapter shows:
     category  |   q1   |   q2   |   q3   |   q4    | h2_vs_h1_pct
   ------------+--------+--------+--------+---------+--------------
    Storage    | 503257 | 342422 | 451179 | 1001116 |           72
    Kitchen    | 133888 | 219336 | 393660 |  461146 |          142
    Industrial |  80780 | 147560 | 275450 |  292040 |          149
    Furniture  |  16388 |  17250 |      0 |       0 |         -100
   (4 rows)
*/


-- - EXTRACT(QUARTER FROM o.order_date) gives 1 to 4. Each SUM(CASE WHEN qtr = 1 …) adds only that
-- quarter's lines: one pivot column per quarter. - h2_vs_h1_pct divides July–December revenue by
-- January–June revenue: 100 × H2 ÷ H1 − 100 is the percentage change. With one year of data, half-
-- on-half is the fairest growth measure available; there's no 2024 in this database to compare
-- with. - Kitchen and Industrial both grew steadily, quarter after quarter. Storage's growth is
-- mostly one quarter: Q4 is more than twice Q3. Furniture sold nothing after June.

-- Step 4: revenue isn't profit. Chapter 12's revenue-versus-profit query (section 12.10), with
-- profit per order and the average discount added:

SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost), 0) AS gross_profit,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost)
             / SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 1) AS margin_pct,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost)
             / COUNT(DISTINCT o.order_id), 0) AS profit_per_order,
       ROUND(AVG(oi.discount_pct), 1) AS avg_discount_pct
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
JOIN products    AS p  ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY gross_profit DESC;

/* The chapter shows:
     category  | gross_profit | margin_pct | profit_per_order | avg_discount_pct
   ------------+--------------+------------+------------------+------------------
    Storage    |       619174 |       26.9 |             4360 |              4.8
    Kitchen    |       401580 |       33.2 |             4724 |              1.7
    Industrial |       108330 |       13.6 |             4710 |              9.2
    Furniture  |         8138 |       24.2 |             4069 |              2.5
   (4 rows)
*/


-- - pd.concat([train, valid]) stacks the two tables, so the final models learn from every lead
-- before July 2025. - The loop is Step 2's, reusing the same two candidates: .fit retrains each on
-- the larger table, and roc_auc_score and log_loss score it on the test leads, which neither model
-- has seen. - On the test leads, logistic regression is ahead on both measures. The decision from
-- Step 2 stands.

-- The one-page summary:

-- > Model: logistic regression on Chapter 36's thirteen features, split by date. I compared it
-- with tuned gradient boosting: on validation they tied (ROC-AUC 0.823 against 0.826), and on the
-- held-out test leads logistic regression was ahead (0.838 against 0.830) with better-calibrated
-- probabilities. I'm shipping the simpler model: it's as accurate, faster, and easy to explain to
-- the sales team. > > Evaluation: at the default 0.5 threshold the model is nearly useless: it
-- flags 7 of 2,225 leads. Working the 627 leads that score above 0.077 gives an estimated ₹24.5
-- lakh of expected profit on the January–June leads, against ₹10.8 lakh for working all 2,225:
-- about 2.3 times the profit from 28% of the effort. The team can work only about 504 leads in
-- that period, so in practice I'd work the top 504 by score (a threshold of about 0.097): ₹23.3
-- lakh. > > Production use: score new leads nightly and hand the sales team a ranked call list
-- sized to their capacity, not a raw score. I'd rank by expected value (probability × deal value,
-- Chapter 44's lesson) once we have a per-lead deal estimate, such as the quoted value or company
-- size. Today every lead uses the same ₹30,255, so ranking by probability is equivalent, and
-- that's the first data gap I'd close. > > Limitations I'd flag before shipping: the model learns
-- from 2023–2024 patterns; if lead sources or the market shift (Chapter 36 showed the marketplace
-- share rising), retrain it, and watch how many leads each day's threshold flags. The ₹1,500 cost
-- and the ₹30,255 win value are assumptions to agree with finance, not facts; the profit figures
-- are expected values from the model, not money earned, and should be confirmed with a small trial
-- before anyone quotes them.

-- =============================================================================================
-- How this would be scored
-- =============================================================================================

-- | Dimension | What a strong submission does | |---|---| | Correctness | A real baseline-versus-
-- challenger comparison on the same split, chosen on validation and tested once; every number
-- comes from one model and one dataset | | Structure & communication | Model choice → evaluation →
-- production plan → limitations, in that order | | Depth & edge cases | Goes past AUC into a cost-
-- based threshold and the team's capacity, showing the metric-to-decision translation | | Business
-- judgment | Chooses the simpler model when the complex one doesn't win, and sizes the list to
-- what the team can actually work | | Collaboration | States real limitations unprompted and
-- doesn't oversell the model as a finished, permanent solution |

-- What a weak submission looks like: reports only AUC, picks boosting because it's "more
-- advanced", recommends a 0.5 threshold with no cost reasoning, and has no limitations section at
-- all: technically functional, missing every dimension beyond raw correctness.

-- Learn it in: Chapter 36, sections 36.3 (a split by date) and 36.10 (baselines); Chapter 37,
-- section 37.12 (baseline versus boosting on the leads); Chapter 39, sections 39.1 (the confusion
-- matrix), 39.2 (ROC-AUC) and 39.5 (the cost threshold and capacity); Chapter 44, section 44.4
-- (ranking by value, not probability). Practise it with: Chapter 74, Q74-008 (a good AUC can still
-- be a bad choice), Q74-015 (ROC-AUC versus PR-AUC) and Q74-016 (the 0.5 threshold).

-- ---

-- =============================================================================================
-- 82.3 Take-home assignment: Data Engineer
-- =============================================================================================

-- =============================================================================================
-- The assignment, as given
-- =============================================================================================

-- > "Design and implement a small pipeline that loads daily order data into a summary table,
-- safely re-runnable if it fails partway through, with at least one automated data quality check.
-- You have 2 hours."

-- Practice data: the Riverstone mini database (12 orders, January to March 2026), loaded into
-- riverstone_lab, the practice database from Chapter 12, section 12.13, so that nothing you do
-- here touches the riverstone database itself. If you dropped riverstone_lab at the end of that
-- section, create it again with CREATE DATABASE riverstone_lab;. Then, connected to
-- riverstone_lab, run riverstone_setup.sql from the companion files (Appendix E) with Execute SQL
-- Script, as in section 12.3. It creates the mini database's seven tables in the lab.

-- <!-- Verifier setup, not printed: the lab database and the mini database's tables, as the reader
-- makes them above.

CREATE DATABASE riverstone_lab;


\i '/home/user/DS_BA_Curriculum/Data Science/Analyst-to-Architect/companion/postgresql/riverstone_setup.sql'


-- -->

-- =============================================================================================
-- Model submission
-- =============================================================================================

-- Step 1: the summary table, created once. The table's own rules are the first quality check:

CREATE TABLE IF NOT EXISTS daily_summary (
    order_date     DATE PRIMARY KEY,
    total_revenue  NUMERIC(12,2) NOT NULL CHECK (total_revenue >= 0),
    order_count    INTEGER       NOT NULL CHECK (order_count > 0)
);


-- - IF NOT EXISTS makes the setup safe to run twice. A plain CREATE TABLE stops the second time
-- with ERROR: relation "daily_summary" already exists; with IF NOT EXISTS, PostgreSQL prints a
-- notice and carries on. - PRIMARY KEY on order_date allows one row per day, so a duplicate day
-- can never be stored. - NOT NULL and the two CHECK rules (Chapter 12, section 12.13) reject a
-- missing or negative revenue, and a day with no orders. A load that breaks them fails with an
-- error instead of storing a wrong number.

-- Run the same statement a second time:

-- <!-- Verifier: the same statement again, as the reader runs it.

CREATE TABLE IF NOT EXISTS daily_summary (
    order_date     DATE PRIMARY KEY,
    total_revenue  NUMERIC(12,2) NOT NULL CHECK (total_revenue >= 0),
    order_count    INTEGER       NOT NULL CHECK (order_count > 0)
);


-- Step 2: the load, safe to repeat. Replace a whole window of days inside one transaction:

BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;


-- - BEGIN … COMMIT is a transaction (Chapter 12, section 12.13): the DELETE and the INSERT are
-- kept together or undone together. If anything fails in between, the table keeps its previous
-- contents. - The DELETE clears every day in the window; the INSERT rebuilds them from the source.
-- Chapter 46, section 46.4 proved this delete-and-insert pattern with a failure test. - The window
-- here is the whole of the mini database, the first quarter of 2026. A daily job would reload the
-- last few days, so that late changes (a cancellation, a corrected line) are picked up.

-- Check what arrived:

SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;

/* The chapter shows:
    days | orders |  revenue
   ------+--------+-----------
      11 |     11 | 323930.00
   (1 row)
*/


-- Eleven days, one order each: the twelve orders less the cancelled one. ₹3,23,930 is the same
-- total as Chapter 12's revenue-versus-profit query (section 12.10). ✓

-- Now run the whole load block (BEGIN to COMMIT) a second time, and count again:

-- <!-- Verifier: the load block again, as the reader runs it.

BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;


-- -->

SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;

/* The chapter shows:
    days | orders |  revenue
   ------+--------+-----------
      11 |     11 | 323930.00
   (1 row)
*/


-- The same eleven days and the same total: a second run changes nothing.

-- Step 3: two failure tests. A re-run of the same data is the easy case. The two that catch real
-- pipelines out are a correction to data already loaded, and a bad row.

-- Test 1, a correction. The customer cancels order 5012, the only order on 15 March:

UPDATE orders SET status = 'Cancelled' WHERE order_id = 5012;


-- Run the load block again, then count:

-- <!-- Verifier: the load block again, as the reader runs it.

BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;


-- -->

SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;

/* The chapter shows:
    days | orders |  revenue
   ------+--------+-----------
      10 |     10 | 297710.00
   (1 row)
*/


-- 15 March has gone, and the total fell by that order's ₹26,220. This is why the load deletes the
-- window first. An upsert (INSERT … ON CONFLICT (order_date) DO UPDATE, Chapter 12, section 12.13)
-- would also survive a re-run without duplicates, but it only touches the days its SELECT returns.
-- A day that loses all its orders returns no row, so the upsert would leave 15 March at its old
-- ₹26,220 forever.

-- Test 2, a bad row. A new order arrives with a typing slip: a discount of 150% instead of 15%:

INSERT INTO orders VALUES (5013, 1, '2026-03-20', 'Pending', 3);
INSERT INTO order_items VALUES (21, 5013, 101, 10, 450.00, 150);


-- Run the load block again:

-- <!-- Verifier: the load block again, as the reader runs it.

BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;


-- The line's revenue is 10 × ₹450 × (1 − 1.5) = −₹2,250, and the CHECK rule refuses it. The load
-- fails loudly, and because the DELETE ran inside the same transaction, it is undone too:

SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;

/* The chapter shows:
    days | orders |  revenue
   ------+--------+-----------
      10 |     10 | 297710.00
   (1 row)
*/


-- The previous good table is still there, untouched. Fix the source, and the same load succeeds:

UPDATE order_items SET discount_pct = 15 WHERE order_item_id = 21;


-- Run the load block once more, then count:

-- <!-- Verifier: the load block again, as the reader runs it.

BEGIN;

DELETE FROM daily_summary
WHERE order_date BETWEEN '2026-01-01' AND '2026-03-31';

INSERT INTO daily_summary (order_date, total_revenue, order_count)
SELECT o.order_date,
       SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),
       COUNT(DISTINCT o.order_id)
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status <> 'Cancelled'
  AND o.order_date BETWEEN '2026-01-01' AND '2026-03-31'
GROUP BY o.order_date;

COMMIT;


-- -->

SELECT COUNT(*) AS days, SUM(order_count) AS orders, SUM(total_revenue) AS revenue
FROM daily_summary;

/* The chapter shows:
    days | orders |  revenue
   ------+--------+-----------
      11 |     11 | 301535.00
   (1 row)
*/


-- Eleven days again: 20 March is in, with 10 × ₹450 × 0.85 = ₹3,825.

-- Step 4: a data test after every load. A data test is a query that returns the rows that break a
-- rule; zero rows means it passed (Chapter 47, section 47.3). This one compares every day in the
-- summary with the source, in both directions:

SELECT s.order_date, s.total_revenue, src.order_date AS source_date, src.revenue AS source_revenue
FROM daily_summary AS s
FULL OUTER JOIN (
    SELECT o.order_date,
           ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 2) AS revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_date
) AS src ON s.order_date = src.order_date
WHERE s.total_revenue IS DISTINCT FROM src.revenue;

/* The chapter shows:
    order_date | total_revenue | source_date | source_revenue
   ------------+---------------+-------------+----------------
   (0 rows)
*/


-- - The subquery in brackets is the load's revenue by day, straight from the source, rounded to
-- two decimals like the table's NUMERIC(12,2) column. - FULL OUTER JOIN keeps days from both sides
-- (Chapter 12, section 12.10: the reconciliation join), so a day missing from the summary or a
-- stale day left in it both show up. - IS DISTINCT FROM (Chapter 28, section 28.10) is "not equal"
-- that also treats a NULL on one side as a difference; a plain <> would silently skip those rows.
-- - Zero rows: every day matches its source. The pipeline's scheduler runs this after each load
-- and fails the run if any row comes back, the way Chapter 47's run_tests does.

-- Clean up when you're done:

DROP TABLE daily_summary;


-- DROP TABLE removes the practice table (Chapter 12, section 12.13). The mini database's tables
-- can stay in the lab for the next time you practice.

-- Step 5: the one-page design note:

-- > Idempotency: the load deletes and re-inserts a window of days inside one transaction, so
-- running it twice gives the same table, and a correction to data already loaded (a cancelled
-- order, a fixed line) is picked up on the next run. I chose this over an upsert (ON CONFLICT … DO
-- UPDATE) because an upsert never removes a day that has lost all its orders. One statement, or
-- one transaction, is atomic: a failure partway through leaves the table unchanged, so there's
-- nothing to clean up. What makes a second run safe is the delete-and-insert. > > Data quality:
-- two layers, and both can fail. The table's own rules (NOT NULL, CHECK) stop a missing or
-- negative revenue at write time, which also covers a NULL discount, since a NULL anywhere in the
-- revenue formula makes the line's revenue NULL (Chapter 12, section 12.7). After each load, a
-- data test reconciles every day with the source and fails the run on any mismatch. In a real
-- deployment I'd add a volume check (today's order count far below the trailing average, Chapter
-- 47, section 47.5), because a truncated source file passes both of these: fewer orders, all of
-- them valid. > > Scale: each run recomputes the whole window, which is fine at Riverstone's size.
-- At scale I'd reload only the last few days, sized to how late changes arrive. > > What I'd add
-- given more time: a raw/staging layer (Chapter 45's raw → staging layers), so extracted data
-- lands unmodified before transformation, letting a transformation bug be fixed and reprocessed
-- without re-extracting from the source; and an explicit dependency declaration if this joins with
-- other scheduled loads, rather than assuming execution order.

-- =============================================================================================
-- How this would be scored
-- =============================================================================================

-- | Dimension | What a strong submission does | |---|---| | Correctness | The load genuinely re-
-- runs safely: no duplicates, no stale days, and a bad row can't reach the table | | Structure &
-- communication | Table, load, tests and design note clearly separated, not tangled together | |
-- Depth & edge cases | Tests the hard cases (a correction and a bad row), not just a second run,
-- and names a second check type (volume) unprompted | | Business judgment | Explains why a
-- pipeline should fail loudly rather than silently store a wrong number | | Collaboration | States
-- what's missing given more time, rather than presenting the 2-hour version as fully production-
-- ready |

-- What a weak submission looks like: a plain INSERT with no conflict handling, which fails the
-- core "safely re-runnable" requirement entirely; or a quality check that only counts bad rows and
-- logs a warning, so nothing ever fails.

-- Learn it in: Chapter 12, section 12.13 (constraints, transactions, the upsert); Chapter 45,
-- section 45.1 (raw and staging layers); Chapter 46, section 46.4 (idempotency, proven with a
-- failure test); Chapter 47, sections 47.3 (data tests) and 47.5 (volume checks). Practise it
-- with: Chapter 77, Q77-007 (the re-run that duplicates rows) and Q77-028 (a check that would have
-- caught negative revenue).

-- ---

-- =============================================================================================
-- 82.4 Mock interview: Data Analyst (entry level)
-- =============================================================================================

-- A 20-minute mock for an entry-level Data Analyst role, condensed. Interviewer notes appear in
-- brackets, with Chapter 69's tags. At two turns, a weaker answer to the same question follows,
-- with its score. The scoring table at the end uses Chapter 69's scale, 1 (weak) to 4
-- (outstanding).

-- Interviewer: Let's start with something practical. Write a query to find customers who haven't
-- placed an order in the last 90 days.

-- Candidate: Sure. Two quick checks first. When you say "last 90 days," is that from today, or
-- from the most recent order date in the data? If this is historical data, "today" might not mean
-- what I'd assume. And should a cancelled order count as activity, and do you want customers
-- who've never ordered at all?

-- [Interviewer note: [+Clarify] caught a real ambiguity most candidates miss, plus two scope
-- questions that change the answer.]

-- Interviewer: From the most recent date in the data. Cancelled orders don't count, and yes,
-- include customers who've never ordered.

-- Candidate: Got it.

SELECT c.customer_id, c.customer_name
FROM customers AS c
WHERE NOT EXISTS (
  SELECT 1
  FROM orders AS o
  WHERE o.customer_id = c.customer_id
    AND o.status <> 'Cancelled'
    AND o.order_date > (SELECT MAX(order_date) FROM orders) - INTERVAL '90 days'
);

