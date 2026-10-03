-- Chapter 27. Capstone: Your Analyst Portfolio
-- Practice SQL for MYSQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_mysql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch27-capstone-your-analyst-portfolio.md


-- =============================================================================================
-- Chapter 27. Capstone: Your Analyst Portfolio
-- =============================================================================================

-- Part 2 — The Analyst

-- > Chapter at a glance > > You will learn to: take one business question all the way from a
-- database to a memo, using only what Part 2 taught · write down the cleaning decisions you made,
-- and measure whether they changed the answer · find the check that turns a flattering result into
-- an honest one, and report both · wrap the analysis in a function so it can be re-run and argued
-- with · specify a one-page dashboard that serves a single decision · write the memo, including
-- the part that says what you did not find · recognize selective reporting in your own portfolio,
-- which is where it is most tempting · assemble three projects into a portfolio a hiring manager
-- will actually open · tell the story of a project in two minutes and in ten · judge for yourself
-- whether you are ready to apply. > > Before you start: all of Part 2. This chapter adds no new
-- tools and one new SQL function, NTILE (section 27.4). What is new is method: how to record and
-- measure your own decisions, how to test a headline before believing it, and how to present work
-- honestly. It uses Chapters 12 and 13 (SQL), 14 (cleaning), 17 and 18 (Python), 15 and 16
-- (visualization and Power BI), 20 (automation), 21 and 22 (statistics), 23 (metrics), 24 and 25
-- (requirements and stakeholders), and 26 (the repository this all lives in). > > Time needed:
-- reading and running the worked project, 2–3 hours. Your own portfolio, 20–30 hours over one to
-- two weeks (the deep project alone, 8–12 hours). > > Tools: PostgreSQL or MySQL in DBeaver
-- (Chapter 12), Python with pandas (Chapters 17 and 18) and SciPy (Chapter 21), Power BI Desktop
-- or any BI tool (Chapter 16), Git (Chapter 26). Nothing new to install. The outputs were checked
-- on PostgreSQL 16 and MySQL 8, and on Python 3.11 with pandas 3.0.6 and SciPy 1.17.1 (any Python
-- from 3.11 on runs every example, as Chapter 17 said). > > Practice data: riverstone_full, the
-- three-year database you loaded in Chapter 14: 5,027 customer records, 116,194 orders, 209,006
-- order lines, 2023 to 2025. The queries read its orders, order_items, customers and products
-- tables, whose statuses are already the four clean values (Delivered, Shipped, Pending,
-- Cancelled); the messy spellings Chapter 14 cleaned were in the branch export, not in these
-- tables. The 48 duplicate customer records are still in customers, and section 27.3 deals with
-- them using Chapter 14's clean_customers table. The Python reads the same tables from the CSV
-- files in companion/full/. Every number and every output in this chapter was produced by running
-- the query or the script shown.

-- ---

-- =============================================================================================
-- Why this matters
-- =============================================================================================

-- Seventeen chapters of Part 2 each taught one thing well. A hiring manager will not ask you about
-- one thing. They will ask you to talk about something you built, and then they will find out, in
-- about four minutes, whether you understand it.

-- This chapter is one worked pass through the whole analyst arc on a single question, and then a
-- second half that no other chapter in this book covers: what happens to that work when somebody
-- else looks at it.

-- The two halves belong together for a reason that becomes clear about halfway through. A
-- portfolio is, by construction, a highlight reel. You choose what goes in it. That choice is the
-- same choice you make when you decide which numbers go in a memo, and it is the point where
-- analysts most often stop being honest without ever deciding to be dishonest. Chapter 22 promised
-- that this chapter would deal with selective reporting. It does, in section 27.8, using a real
-- finding from this chapter's own project that did not survive being checked.

-- ---

-- =============================================================================================
-- In plain English
-- =============================================================================================

-- A portfolio is not a gallery. It is evidence.

-- A gallery shows finished things, lit well, from their best angle. Evidence is different: it has
-- to survive somebody picking it up and turning it over. When a carpenter applies for work, they
-- do not bring a photograph of a finished house. They bring a joint. The joint is small, it can be
-- examined from every side, and it shows whether the person can cut to a line.

-- Your portfolio projects are joints. Small enough to be examined, honest enough to survive it.
-- The question a hiring manager is really asking is not "can you do impressive things?" It is "if
-- I give you a number to produce, will it be right, and will you tell me when it isn't?"

-- ---

-- =============================================================================================
-- 27.1 A question worth putting in a portfolio
-- =============================================================================================

-- Most portfolio projects fail before any code is written, because the question was never worth
-- answering.

-- Three tests. A question belongs in a portfolio if it passes all three:

-- | Test | Why it matters | A question that fails | |---|---|---| | There is a decision behind it
-- | Without one, no finding can be right or wrong, so nothing you conclude can be judged |
-- "Exploratory analysis of the sales dataset" | | The answer could come out either way | If you
-- know the answer before you start, you are illustrating, not analyzing | "Show that revenue grew
-- in 2025" | | Somebody would be annoyed if you got it wrong | That is what makes the care visible
-- | "Top 10 products by revenue" |

-- The question this chapter answers came from a real conversation of the kind Chapter 24 taught
-- you to have. Vikram Singh, the key accounts sales manager, said this at a Monday review:

-- > "We give Wholesale much deeper discounts than anyone else and they buy far more. Should we be
-- discounting harder in Retail to grow it the same way?"

-- That passes all three tests. There is a decision behind it, with rupees attached. The answer
-- could be yes or no. And getting it wrong is expensive in both directions: discount when you
-- should not and you give away margin, refuse when you should have and you leave growth on the
-- table.

-- Chapter 25 would call this an unwritten requirement, so before touching the database, write down
-- what has to be true for an answer to be usable:

-- | | This project | |---|---| | The claim to test | Deeper discounts cause customers to order
-- more | | Unit of analysis | One customer, one year | | Period | Calendar 2025, with 2024 held
-- back to check whatever we find | | Measures | Orders placed, and net revenue after discount | |
-- What would change the recommendation | Evidence that the same discount depth produces different
-- order counts in customers who are otherwise alike | | Out of scope | Whether discounting wins
-- new customers. Different question, different data |

-- That last row is the one people skip, and it is the row that stops a project sprawling.

-- The plan, which is also the shape of the rest of this chapter:

-- 1. SQL. Get the headline number out of the database. 2. Cleaning. Deal with what the data does
-- to that number, and record the decisions. 3. The check. Find out whether the headline survives
-- being split. 4. Python. Make the whole thing re-runnable, so the decisions can be argued with.
-- 5. The dashboard. One page that serves the decision, not the analysis. 6. The memo. What Vikram
-- actually receives.

-- Figure 27.1 — The tools are not new. The order is the lesson, and stage 3 is the one that
-- decides whether the project is honest.

-- ---

-- =============================================================================================
-- 27.2 SQL: the headline (a recap, not a re-teach)
-- =============================================================================================

-- Chapters 12 and 13 taught every piece of these queries; the point is the order things happen in.

-- <!-- db: riverstone_full -->

-- Start with the background question, because a claim about discounting should begin by checking
-- whether discounting has moved at all:

SELECT EXTRACT(YEAR FROM o.order_date)::int AS year,
       ROUND(100 * (1 - SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))
                      / SUM(oi.quantity * oi.unit_price)), 2)
           AS discount_pct,
       ROUND(100 * (SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))
                  - SUM(oi.quantity * p.unit_cost))
                  / SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 1)
           AS margin_pct
FROM   orders AS o
JOIN   order_items AS oi ON oi.order_id = o.order_id
JOIN   products AS p ON p.product_id = oi.product_id
WHERE  o.status <> 'Cancelled'
GROUP  BY year ORDER BY year;

/* The chapter shows:
    year | discount_pct | margin_pct 
   ------+--------------+------------
    2023 |         3.49 |       21.1
    2024 |         3.43 |       24.7
    2025 |         3.51 |       27.5
   (3 rows)
*/


-- How it works:

-- - EXTRACT(YEAR FROM o.order_date) takes the year out of each order date (Chapter 12, section
-- 12.8). EXTRACT returns a decimal number type, and ::int is PostgreSQL's cast (the shorthand from
-- the same section) to a whole number, so year is an ordinary integer. GROUP BY year then makes
-- one row per year. - oi.quantity  oi.unit_price is a line's list value, before any discount, and
-- oi.quantity  oi.unit_price * (1 - oi.discount_pct / 100) is its net value, after the discount.
-- SUM adds each one up over the whole year. - 1 - net / list is the share of list value given
-- away: the year's discount, weighted by money. 100 * turns the share into a percentage and
-- ROUND(..., 2) keeps two decimals. The next query explains why it is weighted by money rather
-- than averaged. - The margin is (net revenue − product cost) ÷ net revenue. Product cost is
-- oi.quantity * p.unit_cost, which is why the query joins products. ROUND(..., 1) keeps one
-- decimal. - WHERE o.status <> 'Cancelled' leaves out cancelled orders, which were never sales.

-- Company-wide discounting has not moved in three years: 3.49%, 3.43%, 3.51%. Worth knowing before
-- anybody claims discounting is "getting out of hand", and it takes one query.

-- Margin, on the other hand, rose from 21.1% to 27.5% while discounts stood still. A reader will
-- ask why, so look before you answer: the products table holds one unit cost per product, today's,
-- and the query applies it to every year, while the prices on the order lines rose from year to
-- year. Part of that rise may be the measurement, not the business. It is a question for the
-- finance team, and it stays out of this project's scope.

-- > MySQL. Write YEAR(o.order_date) in place of EXTRACT(YEAR FROM o.order_date)::int. Every other
-- query in this chapter runs on MySQL 8 unchanged, except the ::int casts in section 27.3, which
-- become CAST(customer_code AS SIGNED).

-- Now the question itself. One row per customer for 2025, then the two groups compared:

WITH customer_year AS (
    SELECT o.customer_id,
           COUNT(DISTINCT o.order_id)                                     AS orders,
           SUM(oi.quantity * oi.unit_price)                               AS list_revenue,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))  AS net_revenue
    FROM   orders AS o
    JOIN   order_items AS oi ON oi.order_id = o.order_id
    WHERE  o.status <> 'Cancelled'
      AND  o.order_date >= DATE '2025-01-01' AND o.order_date < DATE '2026-01-01'
    GROUP  BY o.customer_id
)
SELECT CASE WHEN 100 * (1 - net_revenue / list_revenue) >= 5
            THEN '5% or deeper' ELSE 'under 5%' END AS discount_band,
       COUNT(*)                 AS customers,
       ROUND(AVG(orders), 1)    AS avg_orders,
       ROUND(AVG(net_revenue))  AS avg_revenue
FROM   customer_year
GROUP  BY discount_band
ORDER  BY discount_band;

/* The chapter shows:
    discount_band | customers | avg_orders | avg_revenue 
   ---------------+-----------+------------+-------------
    5% or deeper  |       681 |       14.8 |      459662
    under 5%      |      3918 |        9.3 |      212765
   (2 rows)
*/


-- How it works, and why it is built this way:

-- - The CTE computes the customer's own discount rate, rather than averaging the discount
-- percentages on their lines. Averaging percentages weights a ₹2,000 line the same as a ₹2,00,000
-- one. Dividing total net revenue by total list revenue weights by money, which is what the
-- question means. - COUNT(DISTINCT o.order_id) is necessary because the join to order_items puts a
-- customer's order on the table once per line. This is the fan-out trap of Chapter 12, section
-- 12.10, and it is the single most common way this query goes wrong. - The WHERE clause uses a
-- half-open date range, >= 2025-01-01 and < 2026-01-01, rather than BETWEEN. Chapter 12 section
-- 12.6 explains why: BETWEEN on a timestamp column silently drops the last day. - CASE WHEN ... >=
-- 5 THEN '5% or deeper' ELSE 'under 5%' END puts each customer into one of two bands by their own
-- discount rate (Chapter 12, section 12.8), and GROUP BY discount_band makes one row per band.
-- ROUND(AVG(orders), 1) and ROUND(AVG(net_revenue)) give the band's average orders and average
-- revenue per customer, to one decimal and to the rupee. - status <> 'Cancelled' is a business
-- rule, not a technical one, and it is the first entry in the decision log below. - >= 5 is a line
-- the analyst chose. Remember that. It becomes important in section 27.5.

-- The headline, in one sentence: customers on discounts of 5% or deeper placed 14.8 orders in 2025
-- and were worth ₹4,59,662 each, against 9.3 orders and ₹2,12,765 for everyone else. That is 59%
-- more orders and more than double the revenue.

-- If this were a portfolio project written by most people, that sentence would be the finding, the
-- chart would show those two bars, and the project would be finished. Hold on to it. It is wrong,
-- and section 27.4 is where it comes apart.

-- ---

-- =============================================================================================
-- 27.3 Cleaning: the decisions, and whether they mattered
-- =============================================================================================

-- Chapter 14 taught the techniques. What a portfolio needs, and what Chapter 14 section 14.11
-- called the cleaning log, is the record of what you decided and why.

-- =============================================================================================
-- First, reconcile
-- =============================================================================================

-- Before deciding anything about the data, check that the customer-year table holds all of it. The
-- same 2025 orders and net revenue can be counted a second way, from the sales_lines view (Chapter
-- 13, section 13.2), which knows nothing about customers. If the two routes disagree, the CTE has
-- lost or double-counted something:

WITH customer_year AS (
    SELECT o.customer_id,
           COUNT(DISTINCT o.order_id)                                     AS orders,
           SUM(oi.quantity * oi.unit_price)                               AS list_revenue,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))  AS net_revenue
    FROM   orders AS o
    JOIN   order_items AS oi ON oi.order_id = o.order_id
    WHERE  o.status <> 'Cancelled'
      AND  o.order_date >= DATE '2025-01-01' AND o.order_date < DATE '2026-01-01'
    GROUP  BY o.customer_id
)
SELECT (SELECT SUM(orders) FROM customer_year)                AS orders_in_table,
       (SELECT COUNT(DISTINCT order_id) FROM sales_lines
        WHERE  order_date >= DATE '2025-01-01'
          AND  order_date <  DATE '2026-01-01')               AS orders_in_view,
       (SELECT ROUND(SUM(net_revenue), 2) FROM customer_year) AS revenue_in_table,
       (SELECT ROUND(SUM(net_revenue), 2) FROM sales_lines
        WHERE  order_date >= DATE '2025-01-01'
          AND  order_date <  DATE '2026-01-01')               AS revenue_in_view;

/* The chapter shows:
    orders_in_table | orders_in_view | revenue_in_table | revenue_in_view 
   -----------------+----------------+------------------+-----------------
              46356 |          46356 |    1146641651.25 |   1146641651.25
   (1 row)
*/


-- How it works:

-- - The CTE is the one from section 27.2, unchanged. - Each (SELECT ...) in the list is a scalar
-- subquery (Chapter 12, section 12.12): a query that returns one value, used as a column. Four of
-- them put the two routes side by side in one row. - SUM(orders) adds up every customer's order
-- count. Because each order belongs to one customer, it must equal the number of distinct orders
-- in the view.

-- Both routes agree to the paisa: 46,356 orders and ₹1,14,66,41,651.25, the 2025 net revenue
-- Chapter 14 reported for the whole company. Nothing was lost on the way into the table, and that
-- sentence goes in the memo's back pocket for the question "how do you know the number is right?"

-- =============================================================================================
-- The four problems, and the decisions
-- =============================================================================================

-- One query counts the known problems in the order data. The data ends in December 2025, so "from
-- 1 January 2025" means 2025:

SELECT SUM(CASE WHEN status = 'Cancelled' THEN 1 ELSE 0 END)      AS cancelled,
       SUM(CASE WHEN sales_rep_id IS NULL THEN 1 ELSE 0 END)      AS no_rep,
       SUM(CASE WHEN sales_rep_id IS NULL
                 AND order_date >= DATE '2025-01-01'
                THEN 1 ELSE 0 END)                                AS no_rep_2025,
       SUM(CASE WHEN status = 'Pending'
                 AND order_date < DATE '2025-06-01'
                THEN 1 ELSE 0 END)                                AS old_pending,
       SUM(CASE WHEN status = 'Pending'
                 AND order_date >= DATE '2025-01-01'
                 AND order_date < DATE '2025-06-01'
                THEN 1 ELSE 0 END)                                AS old_pending_2025,
       (SELECT COUNT(*) FROM customers WHERE city IS NULL)        AS no_city
FROM   orders;

/* The chapter shows:
    cancelled | no_rep | no_rep_2025 | old_pending | old_pending_2025 | no_city 
   -----------+--------+-------------+-------------+------------------+---------
         4766 |   3414 |        1404 |          60 |               14 |     100
   (1 row)
*/


-- Each SUM(CASE WHEN ... THEN 1 ELSE 0 END) counts the orders that meet one condition (conditional
-- aggregation, Chapter 12 section 12.9), so one pass over orders gives five counts. An order still
-- marked Pending more than six months before the data ends was, in practice, never updated. The
-- last column is a scalar subquery on customers, as in the reconciliation above.

-- This dataset has four known problems. Each one is a decision, not a fix:

-- | What is in the data | The decision | Why | |---|---|---| | 4,766 cancelled orders | Excluded |
-- A cancelled order is not revenue and was never a purchase decision | | 48 duplicate customer
-- records, the same business entered twice with a name variant, holding 621 orders between them |
-- Measured both ways, merged and as loaded; the rest of the analysis uses the data as loaded | Two
-- records for one business understate that business's order count and inflate the customer count,
-- so the merge has to be measured. It moved the headline by 0.2 orders (below) | | 100 customers
-- with no city | Kept | The question does not use city. Dropping rows to tidy a column you do not
-- need is how analyses lose data for no reason | | 3,414 orders across 2023–2025 with no sales rep
-- (1,404 of them in 2025), and 60 Pending orders dated before June 2025 that were never updated
-- (14 of them in 2025) | Kept, flagged in the memo | A missing rep does not touch a customer-level
-- measure. The stale Pendings are counted (a Pending order passes the cancelled filter), but 14
-- orders out of 2025's 46,356 cannot move a customer average; the decision log says so. Both are
-- worth telling the source system's owner about |

-- The duplicate decision is the interesting one, because it is the kind that sounds important.
-- Chapter 14 section 14.4 built the matching: every record in its clean_customers table has a
-- match_key, the normalized name, and two records with the same key are one business. (If you
-- skipped Chapter 14's following-along step, run companion/ch14/sql/ch14_clean_postgresql.sql, or
-- the MySQL version, to create that table.) The honest thing to do with a decision like this is to
-- measure it. First, give every record the ID of the business it belongs to:

WITH merged_id AS (
    SELECT customer_code::int                                    AS customer_id,
           MIN(customer_code::int) OVER (PARTITION BY match_key) AS merged_id
    FROM   clean_customers
)
SELECT COUNT(DISTINCT m.customer_id) AS duplicate_records,
       COUNT(o.order_id)             AS their_orders
FROM   merged_id AS m
LEFT   JOIN orders AS o ON o.customer_id = m.customer_id
WHERE  m.customer_id <> m.merged_id;

/* The chapter shows:
    duplicate_records | their_orders 
   -------------------+--------------
                   48 |          621
   (1 row)
*/


-- How it works:

-- - customer_code::int turns Chapter 14's text code ('0001') back into the number that
-- orders.customer_id uses. - MIN(customer_code::int) OVER (PARTITION BY match_key) is a window
-- function (Chapter 13, section 13.3): for every record, the smallest ID among the records with
-- the same match key. A business entered once keeps its own ID. A duplicate gets the ID of the
-- earlier record, which Chapter 14's answer key confirms is the original in all 48 groups. - WHERE
-- m.customer_id <> m.merged_id keeps only the duplicate records, and the LEFT JOIN to orders
-- counts their orders (a duplicate with no orders would still be counted as a record).

-- Now re-run section 27.2's headline with the merged IDs. The only change is in the CTE: it joins
-- merged_id and groups by m.merged_id instead of o.customer_id:

WITH merged_id AS (
    SELECT customer_code::int                                    AS customer_id,
           MIN(customer_code::int) OVER (PARTITION BY match_key) AS merged_id
    FROM   clean_customers
), customer_year AS (
    SELECT m.merged_id                                                    AS customer_id,
           COUNT(DISTINCT o.order_id)                                     AS orders,
           SUM(oi.quantity * oi.unit_price)                               AS list_revenue,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))  AS net_revenue
    FROM   orders AS o
    JOIN   order_items AS oi ON oi.order_id = o.order_id
    JOIN   merged_id AS m ON m.customer_id = o.customer_id
    WHERE  o.status <> 'Cancelled'
      AND  o.order_date >= DATE '2025-01-01' AND o.order_date < DATE '2026-01-01'
    GROUP  BY m.merged_id
)
SELECT CASE WHEN 100 * (1 - net_revenue / list_revenue) >= 5
            THEN '5% or deeper' ELSE 'under 5%' END AS discount_band,
       COUNT(*)                 AS customers,
       ROUND(AVG(orders), 1)    AS avg_orders,
       ROUND(AVG(net_revenue))  AS avg_revenue
FROM   customer_year
GROUP  BY discount_band
ORDER  BY discount_band;

/* The chapter shows:
    discount_band | customers | avg_orders | avg_revenue 
   ---------------+-----------+------------+-------------
    5% or deeper  |       674 |       15.0 |      464414
    under 5%      |      3881 |        9.3 |      214797
   (2 rows)
*/


-- Merging the duplicates moved the deep-discount group from 14.8 orders to 15.0 and from ₹4,59,662
-- to ₹4,64,414. The conclusion is untouched.

-- That is worth writing down, and most people do not. "I cleaned the data" is an assertion. "I
-- merged 48 duplicate customer records holding 621 orders, and it changed the headline by 0.2
-- orders and 1%" is evidence, and it takes one paragraph. It also tells a reviewer something more
-- useful than the number itself: that you check whether your own work mattered.

-- Because the merge changes the headline by only 0.2 orders, the rest of the chapter uses the data
-- as loaded, which keeps the SQL short. That is a decision too, so the decision log records it,
-- with the measurement beside it. A reviewer who disagrees can see exactly what the other choice
-- would have given.

-- ---

-- =============================================================================================
-- 27.4 The check that changes the answer
-- =============================================================================================

-- Here is the discipline Chapter 22 section 22.5 asked for: before believing that A causes B, look
-- for the thing that could cause both.

-- The candidate here appears the moment you ask the question out loud. Who gets 5% discounts at
-- Riverstone? Chapter 3's approval ladder (section 3.6) sets the rules: up to 5% needs no
-- approval, over 5% needs Vikram, and over 10% needs Anita. Discounts are given customer by
-- customer, so the obvious suspect is the kind of customer. Split the same two bands by segment:

WITH customer_year AS (
    SELECT o.customer_id,
           COUNT(DISTINCT o.order_id)                                     AS orders,
           SUM(oi.quantity * oi.unit_price)                               AS list_revenue,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))  AS net_revenue
    FROM   orders AS o
    JOIN   order_items AS oi ON oi.order_id = o.order_id
    WHERE  o.status <> 'Cancelled'
      AND  o.order_date >= DATE '2025-01-01' AND o.order_date < DATE '2026-01-01'
    GROUP  BY o.customer_id
)
SELECT c.segment,
       CASE WHEN 100 * (1 - cy.net_revenue / cy.list_revenue) >= 5
            THEN '5% or deeper' ELSE 'under 5%' END AS discount_band,
       COUNT(*)                    AS customers,
       ROUND(AVG(cy.orders), 1)    AS avg_orders,
       ROUND(AVG(cy.net_revenue))  AS avg_revenue
FROM   customer_year AS cy
JOIN   customers AS c ON c.customer_id = cy.customer_id
GROUP  BY c.segment, discount_band
ORDER  BY c.segment, discount_band;


-- Read the bottom of that table first. Wholesale has no "under 5%" row at all. Every Wholesale
-- customer in 2025 sits at 5% or deeper, and 662 of the 681 deep-discount customers in the whole
-- company are Wholesale.

-- So the two groups in section 27.2 were not "customers on deep discounts" and "customers on
-- shallow discounts". They were "Wholesale" and "everyone else", wearing a different label. The
-- headline said nothing about discounting. It said that Wholesale buys in bulk, which everybody
-- already knew.

-- Look at the two remaining rows and it gets worse for the original claim. In Retail, the ten
-- customers who did reach 5% averaged 1.1 orders against 9.3 for everyone else. In Hospitality,
-- 1.2 against 9.1. Those are customers who placed one big order and took a volume discount on it,
-- not customers the discount made loyal.

-- The fair comparison is inside a single segment, where the customers are alike in the way that
-- matters. Start with Wholesale, where the deep discounts are; section 27.5 does the same for
-- Retail, which is the segment Vikram's decision is about.

-- Inside Wholesale every customer is above 5%, so the 5% line is useless there. The comparison
-- needs groups made from the customers' own spread, and SQL has one function for that which you
-- have not met yet. NTILE(n) is a window function, like the ROW_NUMBER and RANK of Chapter 13
-- section 13.4: it sorts the rows and deals them into n groups of equal size, numbered 1 to n. Try
-- it on nine made-up customers, few enough to check by eye:

SELECT customer, discount_pct,
       NTILE(4) OVER (ORDER BY discount_pct) AS quartile
FROM  (SELECT 'A' AS customer, 7.1 AS discount_pct
       UNION ALL SELECT 'B', 9.8
       UNION ALL SELECT 'C', 8.2
       UNION ALL SELECT 'D', 11.5
       UNION ALL SELECT 'E', 6.9
       UNION ALL SELECT 'F', 8.8
       UNION ALL SELECT 'G', 10.4
       UNION ALL SELECT 'H', 9.1
       UNION ALL SELECT 'I', 7.6) AS sample
ORDER  BY discount_pct;

/* The chapter shows:
    customer | discount_pct | quartile 
   ----------+--------------+----------
    E        |          6.9 |        1
    A        |          7.1 |        1
    I        |          7.6 |        1
    C        |          8.2 |        2
    F        |          8.8 |        2
    H        |          9.1 |        3
    B        |          9.8 |        3
    G        |         10.4 |        4
    D        |         11.5 |        4
   (9 rows)
*/


-- How it works:

-- - The derived table sample stacks nine one-row SELECTs with UNION ALL (Chapter 12, section
-- 12.12), so the example needs no table of its own. - NTILE(4) asks for four groups, OVER (ORDER
-- BY discount_pct) says in which order to deal the rows out: shallowest discount first. The group
-- number is the quartile. - Nine rows do not split evenly into four. NTILE gives the leftover rows
-- to the first groups, one each, so the sizes are 3, 2, 2, 2: group sizes never differ by more
-- than one. On 662 customers it makes groups of 166, 166, 165 and 165.

-- > Predict before running. What would NTILE(3) give the same nine customers? Write down the three
-- group sizes, then change the 4 to a 3 and run it.

-- Now the real comparison, inside Wholesale:

WITH customer_year AS (
    SELECT o.customer_id,
           COUNT(DISTINCT o.order_id)                                     AS orders,
           SUM(oi.quantity * oi.unit_price)                               AS list_revenue,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))  AS net_revenue
    FROM   orders AS o
    JOIN   order_items AS oi ON oi.order_id = o.order_id
    JOIN   customers AS c ON c.customer_id = o.customer_id
    WHERE  o.status <> 'Cancelled'
      AND  o.order_date >= DATE '2025-01-01' AND o.order_date < DATE '2026-01-01'
      AND  c.segment = 'Wholesale'
    GROUP  BY o.customer_id
), banded AS (
    SELECT orders, net_revenue,
           100 * (1 - net_revenue / list_revenue)                              AS discount_pct,
           NTILE(4) OVER (ORDER BY 100 * (1 - net_revenue / list_revenue))     AS quartile
    FROM   customer_year
)
SELECT quartile,
       COUNT(*)                        AS customers,
       ROUND(AVG(discount_pct), 1)     AS avg_discount_pct,
       ROUND(AVG(orders), 1)           AS avg_orders,
       ROUND(AVG(net_revenue))         AS avg_revenue
FROM   banded
GROUP  BY quartile
ORDER  BY quartile;

/* The chapter shows:
    quartile | customers | avg_discount_pct | avg_orders | avg_revenue 
   ----------+-----------+------------------+------------+-------------
           1 |       166 |              7.9 |       14.1 |      431573
           2 |       166 |              8.5 |       16.7 |      519663
           3 |       165 |              9.0 |       16.4 |      511059
           4 |       165 |              9.7 |       13.6 |      427265
   (4 rows)
*/


-- The more-discounted half of Retail placed 9.5 orders against 9.1: a gap of 0.4 orders, where the
-- headline had 5.5. Across the range of discounts Retail customers really get, a deeper discount
-- goes with barely more ordering. What this cannot tell you is what a discount of 8% or 10% would
-- do in Retail, because only 10 Retail customers reached even 5%. That is a gap in the data, not
-- evidence either way, and the memo has to say so.

-- The answer to Vikram's question is no, and the reason is more useful to him than the answer:
-- discount depth at Riverstone is a label for what segment a customer is in, not a lever that
-- changes how they behave.

-- ---

-- =============================================================================================
-- 27.6 The dashboard: one page, one decision
-- =============================================================================================

-- Chapter 15 gave the principles and Chapter 16 built the thing. The capstone question is narrower
-- than either: what should be on the page, given that a specific person has a specific decision to
-- make?

-- One of those objects needs a number the analysis has not produced yet: the margin each segment
-- earns, which is the cost side of the decision. One query on the sales_lines view (Chapter 13,
-- section 13.2) gives it:

SELECT c.segment,
       ROUND(100 * (SUM(s.net_revenue) - SUM(s.product_cost))
                  / SUM(s.net_revenue), 1)                    AS margin_pct
FROM   sales_lines AS s
JOIN   customers AS c ON c.customer_id = s.customer_id
WHERE  s.order_date >= DATE '2025-01-01' AND s.order_date < DATE '2026-01-01'
GROUP  BY c.segment
ORDER  BY c.segment;

/* The chapter shows:
      segment   | margin_pct 
   -------------+------------
    Hospitality |       31.8
    Retail      |       30.2
    Wholesale   |       18.6
   (3 rows)
*/

