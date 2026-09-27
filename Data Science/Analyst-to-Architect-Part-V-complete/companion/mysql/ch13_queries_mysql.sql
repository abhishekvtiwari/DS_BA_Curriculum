-- =====================================================================
-- Analyst to Architect · Chapter 13 · SQL for Real Analysis
-- Every query in the chapter, rewritten for MySQL, in book order.
--
-- Setup: run riverstone_setup_mysql.sql and riverstone_2025_setup_mysql.sql first.
-- This file creates the sales_lines view in both databases (section 13.2).
-- Tested on MySQL 8.0; uses only features that work the same in MySQL 8.4 LTS and 9.x.
-- Results match the PostgreSQL outputs printed in the chapter.
-- Queries that fail on purpose in the book are commented out, with the MySQL error.
-- Riverstone Supplies is fictional; every name and number is invented.
-- =====================================================================

-- ---------------------------------------------------------------
-- 13.2 Common table expressions: queries in named steps › The problem CTEs solve (book line 71)
USE riverstone;
WITH customer_revenue AS (
    SELECT c.customer_name,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS revenue
    FROM customers   AS c
    JOIN orders      AS o  ON c.customer_id = o.customer_id
    JOIN order_items AS oi ON o.order_id    = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY c.customer_name
)
SELECT customer_name, ROUND(revenue, 0) AS revenue
FROM customer_revenue
WHERE revenue > (SELECT AVG(revenue) FROM customer_revenue)
ORDER BY revenue DESC;

-- ---------------------------------------------------------------
-- 13.2 Common table expressions: queries in named steps › Chaining several steps (book line 107)
WITH payments_per_invoice AS (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
),
invoice_balances AS (
    SELECT i.invoice_id,
           i.order_id,
           i.due_date,
           i.amount - COALESCE(p.paid, 0) AS balance,
           DATEDIFF(DATE '2026-03-31', i.due_date) AS days_past_due
    FROM invoices AS i
    LEFT JOIN payments_per_invoice AS p ON i.invoice_id = p.invoice_id
),
open_invoices AS (
    SELECT b.*, c.customer_name
    FROM invoice_balances AS b
    JOIN orders    AS o ON b.order_id    = o.order_id
    JOIN customers AS c ON o.customer_id = c.customer_id
    WHERE b.balance > 0
)
SELECT customer_name,
       SUM(balance)                                                         AS total_due,
       SUM(CASE WHEN days_past_due <= 0              THEN balance ELSE 0.00 END) AS not_yet_due,
       SUM(CASE WHEN days_past_due BETWEEN 1 AND 30  THEN balance ELSE 0.00 END) AS overdue_1_30,
       SUM(CASE WHEN days_past_due BETWEEN 31 AND 60 THEN balance ELSE 0.00 END) AS overdue_31_60,
       SUM(CASE WHEN days_past_due > 60              THEN balance ELSE 0.00 END) AS overdue_60_plus
FROM open_invoices
GROUP BY customer_name
ORDER BY total_due DESC;

-- ---------------------------------------------------------------
-- 13.2 Common table expressions: queries in named steps › Views: define it once, use it everywhere (book line 179)
CREATE OR REPLACE VIEW sales_lines AS
SELECT o.order_id,
       o.order_date,
       o.customer_id,
       o.sales_rep_id,
       o.status,
       oi.product_id,
       p.category,
       oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS net_revenue,
       oi.quantity * p.unit_cost                                  AS product_cost
FROM orders      AS o
JOIN order_items AS oi ON o.order_id    = oi.order_id
JOIN products    AS p  ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled';

-- The same view in the one-year database:
USE riverstone_2025;
CREATE OR REPLACE VIEW sales_lines AS
SELECT o.order_id,
       o.order_date,
       o.customer_id,
       o.sales_rep_id,
       o.status,
       oi.product_id,
       p.category,
       oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS net_revenue,
       oi.quantity * p.unit_cost                                  AS product_cost
FROM orders      AS o
JOIN order_items AS oi ON o.order_id    = oi.order_id
JOIN products    AS p  ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled';

-- ---------------------------------------------------------------
-- 13.2 Common table expressions: queries in named steps › Views: define it once, use it everywhere (book line 199)
USE riverstone;
SELECT category, ROUND(SUM(net_revenue), 0) AS net_revenue
FROM sales_lines
GROUP BY category
ORDER BY net_revenue DESC;

-- ---------------------------------------------------------------
-- 13.3 Window functions: calculations that keep every row › The idea (book line 232)
WITH order_totals AS (
    SELECT order_id, customer_id, order_date, SUM(net_revenue) AS order_revenue
    FROM sales_lines
    GROUP BY order_id, customer_id, order_date
)
SELECT ROUND(SUM(order_revenue), 0) AS quarter_total
FROM order_totals;

-- ---------------------------------------------------------------
-- 13.3 Window functions: calculations that keep every row › The idea (book line 251)
WITH order_totals AS (
    SELECT order_id, customer_id, order_date, SUM(net_revenue) AS order_revenue
    FROM sales_lines
    GROUP BY order_id, customer_id, order_date
)
SELECT order_id,
       ROUND(order_revenue, 0)                                  AS order_revenue,
       ROUND(SUM(order_revenue) OVER (), 0)                     AS quarter_total,
       ROUND(100.0 * order_revenue / SUM(order_revenue) OVER (), 1) AS pct_of_quarter
FROM order_totals
ORDER BY order_id;

-- ---------------------------------------------------------------
-- 13.3 Window functions: calculations that keep every row › PARTITION BY: a window for each group (book line 292)
WITH order_totals AS (
    SELECT order_id, customer_id, SUM(net_revenue) AS order_revenue
    FROM sales_lines
    GROUP BY order_id, customer_id
)
SELECT c.customer_name,
       t.order_id,
       ROUND(t.order_revenue, 0)                                              AS order_revenue,
       ROUND(SUM(t.order_revenue) OVER (PARTITION BY t.customer_id), 0)       AS customer_total,
       ROUND(100.0 * t.order_revenue
             / SUM(t.order_revenue) OVER (PARTITION BY t.customer_id), 1)     AS pct_of_customer
FROM order_totals AS t
JOIN customers    AS c ON t.customer_id = c.customer_id
ORDER BY c.customer_name, t.order_id;

-- ---------------------------------------------------------------
-- 13.3 Window functions: calculations that keep every row › Where windows run, and why you can't filter on them directly (book line 358)
-- Fails on purpose, as in the book. MySQL says: ERROR 3593: You cannot use the window function 'row_number' in this context.
-- SELECT order_id, customer_id, order_date
-- FROM orders
-- WHERE ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1;

-- ---------------------------------------------------------------
-- 13.4 Ranking: ROW_NUMBER, RANK, and DENSE_RANK › Three ways to number rows (book line 380)
WITH units AS (
    SELECT p.product_name, COALESCE(SUM(s.quantity), 0) AS units_sold
    FROM products AS p
    LEFT JOIN sales_lines AS s ON p.product_id = s.product_id
    GROUP BY p.product_name
)
SELECT product_name,
       units_sold,
       ROW_NUMBER() OVER (ORDER BY units_sold DESC, product_name) AS row_num,
       RANK()       OVER (ORDER BY units_sold DESC)               AS rank_no,
       DENSE_RANK() OVER (ORDER BY units_sold DESC)               AS dense_rank_no
FROM units
ORDER BY units_sold DESC, product_name;

-- ---------------------------------------------------------------
-- 13.4 Ranking: ROW_NUMBER, RANK, and DENSE_RANK › The latest record per group (book line 422)
WITH ranked AS (
    SELECT c.customer_name,
           o.order_id,
           o.order_date,
           o.status,
           ROW_NUMBER() OVER (PARTITION BY o.customer_id
                              ORDER BY o.order_date DESC, o.order_id DESC) AS recency_rank
    FROM orders    AS o
    JOIN customers AS c ON o.customer_id = c.customer_id
)
SELECT customer_name, order_id, order_date, status
FROM ranked
WHERE recency_rank = 1
ORDER BY order_date DESC;

-- ---------------------------------------------------------------
-- 13.5 LAG and LEAD: comparing a row with its neighbors › Looking back (book line 468)
SELECT c.customer_name,
       o.order_id,
       o.order_date,
       LAG(o.order_date) OVER (PARTITION BY o.customer_id ORDER BY o.order_date)                AS previous_order,
       DATEDIFF(o.order_date, LAG(o.order_date) OVER (PARTITION BY o.customer_id ORDER BY o.order_date)) AS days_since_previous
FROM orders    AS o
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE o.status <> 'Cancelled'
ORDER BY c.customer_name, o.order_date;

-- ---------------------------------------------------------------
-- 13.6 Time windows: growth, targets, and moving averages (book line 514)
USE riverstone_2025;
SELECT COUNT(DISTINCT order_id)   AS orders,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(SUM(net_revenue), 0)  AS net_revenue
FROM sales_lines;

-- ---------------------------------------------------------------
-- 13.6 Time windows: growth, targets, and moving averages › Month-over-month growth (book line 534)
WITH monthly AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month,
           SUM(net_revenue)                      AS revenue
    FROM sales_lines
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
)
SELECT month,
       ROUND(revenue, 0)                                              AS revenue,
       ROUND(LAG(revenue) OVER w, 0)                                  AS previous_month,
       ROUND(revenue - LAG(revenue) OVER w, 0)                        AS change_amount,
       ROUND(100.0 * (revenue - LAG(revenue) OVER w) / LAG(revenue) OVER w, 1) AS pct_change
FROM monthly
WINDOW w AS (ORDER BY month)
ORDER BY month;

-- ---------------------------------------------------------------
-- 13.6 Time windows: growth, targets, and moving averages › Running totals: are we on track for the year? (book line 580)
WITH monthly AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
)
SELECT m.month,
       ROUND(m.revenue, 0)                                             AS revenue,
       ROUND(t.target_revenue, 0)                                      AS target,
       ROUND(SUM(m.revenue) OVER w, 0)                                 AS ytd_revenue,
       ROUND(SUM(t.target_revenue) OVER w, 0)                          AS ytd_target,
       ROUND(100.0 * SUM(m.revenue) OVER w / SUM(t.target_revenue) OVER w, 1) AS ytd_pct_of_target
FROM monthly       AS m
JOIN sales_targets AS t ON t.target_month = m.month
WINDOW w AS (ORDER BY m.month)
ORDER BY m.month;

-- ---------------------------------------------------------------
-- 13.6 Time windows: growth, targets, and moving averages › Moving averages: seeing the trend through the noise (book line 624)
WITH monthly AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
)
SELECT month,
       ROUND(revenue, 0) AS revenue,
       ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS moving_avg_3m,
       COUNT(*)          OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)      AS months_in_window
FROM monthly
ORDER BY month;

-- ---------------------------------------------------------------
-- 13.6 Time windows: growth, targets, and moving averages › The hidden frame trap: ROWS versus RANGE (book line 674)
WITH early_may AS (
    SELECT order_id, order_date, SUM(net_revenue) AS order_revenue
    FROM sales_lines
    WHERE order_date BETWEEN '2025-05-01' AND '2025-05-06'
    GROUP BY order_id, order_date
)
SELECT order_id,
       order_date,
       ROUND(order_revenue, 0) AS order_revenue,
       ROUND(SUM(order_revenue) OVER (ORDER BY order_date), 0) AS running_default,
       ROUND(SUM(order_revenue) OVER (ORDER BY order_date, order_id
                                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 0) AS running_rows
FROM early_may
ORDER BY order_date, order_id;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 1: Top N per group (book line 721)
WITH customer_revenue AS (
    SELECT c.segment, c.customer_name, SUM(s.net_revenue) AS revenue
    FROM sales_lines AS s
    JOIN customers   AS c ON s.customer_id = c.customer_id
    GROUP BY c.segment, c.customer_name
),
ranked AS (
    SELECT segment,
           customer_name,
           revenue,
           RANK() OVER (PARTITION BY segment ORDER BY revenue DESC)       AS rank_in_segment,
           100.0 * revenue / SUM(revenue) OVER (PARTITION BY segment)     AS pct_of_segment
    FROM customer_revenue
)
SELECT segment, rank_in_segment, customer_name, ROUND(revenue, 0) AS revenue, ROUND(pct_of_segment, 1) AS pct_of_segment
FROM ranked
WHERE rank_in_segment <= 3
ORDER BY segment, rank_in_segment;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 2: Pareto and ABC analysis (book line 769)
WITH customer_revenue AS (
    SELECT c.customer_name, SUM(s.net_revenue) AS revenue
    FROM sales_lines AS s
    JOIN customers   AS c ON s.customer_id = c.customer_id
    GROUP BY c.customer_name
),
cumulative AS (
    SELECT customer_name,
           revenue,
           100.0 * revenue / SUM(revenue) OVER () AS pct_of_total,
           100.0 * SUM(revenue) OVER (ORDER BY revenue DESC, customer_name
                                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                 / SUM(revenue) OVER ()           AS cumulative_pct
    FROM customer_revenue
)
SELECT customer_name,
       ROUND(revenue, 0)        AS revenue,
       ROUND(pct_of_total, 1)   AS pct_of_total,
       ROUND(cumulative_pct, 1) AS cumulative_pct,
       CASE WHEN cumulative_pct - pct_of_total < 80 THEN 'A'
            WHEN cumulative_pct - pct_of_total < 95 THEN 'B'
            ELSE 'C' END        AS abc_class
FROM cumulative
ORDER BY revenue DESC;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 3: Remove duplicates, keep one (book line 843)
WITH numbered AS (
    SELECT lead_id,
           company_name,
           email,
           created_at,
           ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY created_at, lead_id) AS submission_no,
           COUNT(*)     OVER (PARTITION BY LOWER(email))                              AS submissions
    FROM leads
)
SELECT lead_id, company_name, email, created_at, submission_no
FROM numbered
WHERE submissions > 1
ORDER BY email, submission_no;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 3: Remove duplicates, keep one (book line 886)
SELECT COUNT(*) AS lead_rows, COUNT(DISTINCT LOWER(email)) AS unique_enquiries
FROM leads;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 4: Funnel conversion (book line 916)
WITH first_submissions AS (
    SELECT lead_id
    FROM (
        SELECT lead_id,
               ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY created_at, lead_id) AS submission_no
        FROM leads
    ) AS numbered
    WHERE submission_no = 1
),
stage_counts AS (
    SELECT h.stage,
           CASE h.stage WHEN 'New' THEN 1 WHEN 'Contacted' THEN 2
                        WHEN 'Quoted' THEN 3 WHEN 'Won' THEN 4 END AS step,
           COUNT(*) AS leads
    FROM lead_stage_history AS h
    JOIN first_submissions  AS f ON h.lead_id = f.lead_id
    WHERE h.stage IN ('New', 'Contacted', 'Quoted', 'Won')
    GROUP BY h.stage
)
SELECT step,
       stage,
       leads,
       ROUND(100.0 * leads / LAG(leads) OVER (ORDER BY step), 1)         AS pct_of_previous_step,
       ROUND(100.0 * leads / FIRST_VALUE(leads) OVER (ORDER BY step), 1) AS pct_of_new_leads
FROM stage_counts
ORDER BY step;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 5: Fill in the missing months (book line 971)
WITH furniture AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE category = 'Furniture'
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
)
SELECT month, ROUND(revenue, 0) AS revenue, ROUND(LAG(revenue) OVER (ORDER BY month), 0) AS previous_month
FROM furniture
ORDER BY month;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 5: Fill in the missing months (book line 993)
WITH RECURSIVE months AS (
    SELECT DATE '2025-01-01' AS month
    UNION ALL
    SELECT month + INTERVAL 1 MONTH
    FROM months
    WHERE month < DATE '2025-12-01'
),
furniture AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE category = 'Furniture'
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
),
filled AS (
    SELECT m.month,
           COALESCE(f.revenue, 0)                                     AS revenue,
           LAG(COALESCE(f.revenue, 0)) OVER (ORDER BY m.month)        AS previous_month
    FROM months AS m
    LEFT JOIN furniture AS f ON f.month = m.month
)
SELECT month, ROUND(revenue, 0) AS revenue, ROUND(previous_month, 0) AS previous_month
FROM filled
WHERE month BETWEEN '2025-02-01' AND '2025-06-01'
ORDER BY month;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 6: At-risk customers (breaks in the rhythm) (book line 1046)
WITH order_days AS (
    SELECT DISTINCT customer_id, order_date
    FROM sales_lines
),
gaps AS (
    SELECT customer_id,
           order_date,
           DATEDIFF(order_date, LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)) AS gap_days
    FROM order_days
),
customer_rhythm AS (
    SELECT customer_id,
           COUNT(*)              AS orders,
           ROUND(AVG(gap_days))  AS usual_gap_days,
           MAX(order_date)       AS last_order
    FROM gaps
    GROUP BY customer_id
    HAVING COUNT(*) >= 4
)
SELECT c.customer_name,
       r.orders,
       r.usual_gap_days,
       r.last_order,
       DATEDIFF(DATE '2025-12-31', r.last_order) AS days_since_last,
       CASE WHEN DATEDIFF(DATE '2025-12-31', r.last_order) > 2 * r.usual_gap_days
            THEN 'At risk' ELSE 'On rhythm' END AS status
FROM customer_rhythm AS r
JOIN customers       AS c ON r.customer_id = c.customer_id
ORDER BY (DATEDIFF(DATE '2025-12-31', r.last_order)) / r.usual_gap_days DESC
LIMIT 8;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 7: Cohort retention (book line 1112)
WITH first_orders AS (
    SELECT customer_id, CAST(DATE_FORMAT(MIN(order_date), '%Y-%m-01') AS DATE) AS first_month
    FROM sales_lines
    GROUP BY customer_id
),
active_months AS (
    SELECT DISTINCT customer_id, CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month
    FROM sales_lines
),
cohort_activity AS (
    SELECT f.customer_id,
           CONCAT('Q', EXTRACT(QUARTER FROM f.first_month)) AS cohort,
           (EXTRACT(YEAR FROM a.month) * 12 + EXTRACT(MONTH FROM a.month))
         - (EXTRACT(YEAR FROM f.first_month) * 12 + EXTRACT(MONTH FROM f.first_month)) AS months_since_first
    FROM first_orders  AS f
    JOIN active_months AS a ON f.customer_id = a.customer_id
    WHERE f.first_month < DATE '2025-10-01'
)
SELECT cohort,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN months_since_first = 1 THEN customer_id END) / COUNT(DISTINCT customer_id), 0) AS month_1_pct,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN months_since_first = 2 THEN customer_id END) / COUNT(DISTINCT customer_id), 0) AS month_2_pct,
       ROUND(100.0 * COUNT(DISTINCT CASE WHEN months_since_first = 3 THEN customer_id END) / COUNT(DISTINCT customer_id), 0) AS month_3_pct
FROM cohort_activity
GROUP BY cohort
ORDER BY cohort;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 8: Streaks (gaps and islands) (book line 1169)
WITH months AS (
    SELECT DISTINCT customer_id, CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month
    FROM sales_lines
    WHERE customer_id = 2
)
SELECT month,
       EXTRACT(YEAR FROM month) * 12 + EXTRACT(MONTH FROM month)                    AS month_number,
       ROW_NUMBER() OVER (ORDER BY month)                                           AS row_num,
       EXTRACT(YEAR FROM month) * 12 + EXTRACT(MONTH FROM month)
         - ROW_NUMBER() OVER (ORDER BY month)                                       AS island_id
FROM months
ORDER BY month;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 8: Streaks (gaps and islands) (book line 1203)
WITH months AS (
    SELECT DISTINCT customer_id, CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month
    FROM sales_lines
),
numbered AS (
    SELECT customer_id,
           month,
           EXTRACT(YEAR FROM month) * 12 + EXTRACT(MONTH FROM month)
             - ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY month) AS island_id
    FROM months
),
streaks AS (
    SELECT customer_id, island_id, MIN(month) AS streak_start, MAX(month) AS streak_end, COUNT(*) AS months_in_a_row
    FROM numbered
    GROUP BY customer_id, island_id
),
best AS (
    SELECT s.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY months_in_a_row DESC, streak_start) AS rn
    FROM streaks AS s
)
SELECT c.customer_name, b.streak_start, b.streak_end, b.months_in_a_row
FROM best      AS b
JOIN customers AS c ON b.customer_id = c.customer_id
WHERE b.rn = 1
ORDER BY b.months_in_a_row DESC, c.customer_name
LIMIT 6;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 9: Pivot rows into columns (book line 1256)
SELECT category,
       ROUND(SUM(CASE WHEN EXTRACT(QUARTER FROM order_date) = 1 THEN net_revenue END), 0) AS q1,
       ROUND(SUM(CASE WHEN EXTRACT(QUARTER FROM order_date) = 2 THEN net_revenue END), 0) AS q2,
       ROUND(SUM(CASE WHEN EXTRACT(QUARTER FROM order_date) = 3 THEN net_revenue END), 0) AS q3,
       ROUND(SUM(CASE WHEN EXTRACT(QUARTER FROM order_date) = 4 THEN net_revenue END), 0) AS q4,
       ROUND(SUM(net_revenue), 0)                                                     AS full_year
FROM sales_lines
GROUP BY category
ORDER BY full_year DESC;

-- ---------------------------------------------------------------
-- 13.7 The analyst's pattern library › Pattern 10: Data-quality checks before you trust a report (book line 1290)
SELECT 'Duplicate order IDs' AS check_name, COUNT(*) AS problem_rows
FROM (SELECT order_id FROM orders GROUP BY order_id HAVING COUNT(*) > 1) AS d
UNION ALL
SELECT 'Order lines with no matching order', COUNT(*)
FROM order_items AS oi LEFT JOIN orders AS o ON oi.order_id = o.order_id
WHERE o.order_id IS NULL
UNION ALL
SELECT 'Orders with no lines', COUNT(*)
FROM orders AS o LEFT JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE oi.order_item_id IS NULL
UNION ALL
SELECT 'Non-positive quantities', COUNT(*)
FROM order_items WHERE quantity <= 0
UNION ALL
SELECT 'Orders with no sales rep', COUNT(*)
FROM orders WHERE sales_rep_id IS NULL
UNION ALL
SELECT 'Customers with no orders', COUNT(*)
FROM customers AS c LEFT JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
UNION ALL
SELECT 'Duplicate lead emails (extra rows)', COUNT(*) - COUNT(DISTINCT LOWER(email))
FROM leads;

-- ---------------------------------------------------------------
-- 13.8 Running this chapter in MySQL › Month-over-month growth in MySQL (book line 1365)
WITH monthly AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month,
           SUM(net_revenue)                                  AS revenue
    FROM sales_lines
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
)
SELECT month,
       ROUND(revenue, 0)                                              AS revenue,
       ROUND(LAG(revenue) OVER w, 0)                                  AS previous_month,
       ROUND(revenue - LAG(revenue) OVER w, 0)                        AS change_amount,
       ROUND(100.0 * (revenue - LAG(revenue) OVER w) / LAG(revenue) OVER w, 1) AS pct_change
FROM monthly
WINDOW w AS (ORDER BY month)
ORDER BY month;

-- ---------------------------------------------------------------
-- 13.8 Running this chapter in MySQL › A date spine with a recursive CTE (book line 1407)
WITH RECURSIVE months AS (
    SELECT DATE '2025-01-01' AS month           -- the first month
    UNION ALL
    SELECT month + INTERVAL 1 MONTH             -- add one month...
    FROM months
    WHERE month < DATE '2025-12-01'             -- ...until December
),
furniture AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month,
           SUM(net_revenue)                                  AS revenue
    FROM sales_lines
    WHERE category = 'Furniture'
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
),
filled AS (
    SELECT m.month,
           COALESCE(f.revenue, 0)                              AS revenue,
           LAG(COALESCE(f.revenue, 0)) OVER (ORDER BY m.month) AS previous_month
    FROM months AS m
    LEFT JOIN furniture AS f ON f.month = m.month
)
SELECT month, ROUND(revenue, 0) AS revenue, ROUND(previous_month, 0) AS previous_month
FROM filled
WHERE month BETWEEN '2025-02-01' AND '2025-06-01'
ORDER BY month;

-- ---------------------------------------------------------------
-- 13.8 Running this chapter in MySQL › Pivots without FILTER (book line 1466)
SELECT category,
       ROUND(SUM(CASE WHEN QUARTER(order_date) = 1 THEN net_revenue ELSE 0 END), 0) AS q1,
       ROUND(SUM(CASE WHEN QUARTER(order_date) = 2 THEN net_revenue ELSE 0 END), 0) AS q2,
       ROUND(SUM(CASE WHEN QUARTER(order_date) = 3 THEN net_revenue ELSE 0 END), 0) AS q3,
       ROUND(SUM(CASE WHEN QUARTER(order_date) = 4 THEN net_revenue ELSE 0 END), 0) AS q4,
       ROUND(SUM(net_revenue), 0)                                                    AS full_year
FROM sales_lines
GROUP BY category
ORDER BY full_year DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 1 (book line 1666)
USE riverstone;
WITH customer_units AS (
    SELECT c.customer_name, SUM(s.quantity) AS units
    FROM sales_lines AS s
    JOIN customers   AS c ON s.customer_id = c.customer_id
    GROUP BY c.customer_name
)
SELECT customer_name, units
FROM customer_units
WHERE units > 100
ORDER BY units DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 2 (book line 1689)
USE riverstone_2025;
SELECT category,
       ROUND(SUM(net_revenue), 0)                                     AS revenue,
       ROUND(100.0 * SUM(net_revenue) / SUM(SUM(net_revenue)) OVER (), 1) AS pct_of_total
FROM sales_lines
GROUP BY category
ORDER BY revenue DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 3 (book line 1710)
WITH metro_orders AS (
    SELECT DISTINCT order_id, order_date
    FROM sales_lines
    WHERE customer_id = 5
)
SELECT ROW_NUMBER() OVER (ORDER BY order_date, order_id) AS order_number,
       order_id,
       order_date
FROM metro_orders
ORDER BY order_number
LIMIT 5;

-- ---------------------------------------------------------------
-- Answer to exercise 4 (book line 1739)
WITH product_revenue AS (
    SELECT p.category, p.product_name, SUM(s.net_revenue) AS revenue
    FROM sales_lines AS s
    JOIN products    AS p ON s.product_id = p.product_id
    GROUP BY p.category, p.product_name
),
ranked AS (
    SELECT category, product_name, revenue,
           RANK() OVER (PARTITION BY category ORDER BY revenue DESC) AS rank_in_category
    FROM product_revenue
)
SELECT category, rank_in_category, product_name, ROUND(revenue, 0) AS revenue
FROM ranked
WHERE rank_in_category <= 2
ORDER BY category, rank_in_category;

-- ---------------------------------------------------------------
-- Answer to exercise 5 (book line 1773)
WITH rep_months AS (
    SELECT e.employee_name,
           CAST(DATE_FORMAT(s.order_date, '%Y-%m-01') AS DATE) AS month,
           SUM(s.net_revenue)                      AS revenue
    FROM sales_lines AS s
    JOIN employees   AS e ON s.sales_rep_id = e.employee_id
    GROUP BY e.employee_name, CAST(DATE_FORMAT(s.order_date, '%Y-%m-01') AS DATE)
),
ranked AS (
    SELECT employee_name, month, revenue,
           ROW_NUMBER() OVER (PARTITION BY employee_name ORDER BY revenue DESC, month) AS rn
    FROM rep_months
)
SELECT employee_name, month AS best_month, ROUND(revenue, 0) AS revenue
FROM ranked
WHERE rn = 1
ORDER BY revenue DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 6 (book line 1804)
WITH quarterly AS (
    SELECT c.segment,
           EXTRACT(QUARTER FROM s.order_date) AS quarter,
           SUM(s.net_revenue)                 AS revenue
    FROM sales_lines AS s
    JOIN customers   AS c ON s.customer_id = c.customer_id
    GROUP BY c.segment, EXTRACT(QUARTER FROM s.order_date)
)
SELECT segment,
       CONCAT('Q', quarter)                                                   AS quarter,
       ROUND(revenue, 0)                                                AS revenue,
       ROUND(LAG(revenue) OVER w, 0)                                    AS previous_quarter,
       ROUND(100.0 * (revenue - LAG(revenue) OVER w) / LAG(revenue) OVER w, 1) AS pct_change
FROM quarterly
WINDOW w AS (PARTITION BY segment ORDER BY quarter)
ORDER BY segment, quarter;

-- ---------------------------------------------------------------
-- Answer to exercise 7 (book line 1845)
WITH customer_orders AS (
    SELECT DISTINCT s.customer_id, s.order_id, s.order_date
    FROM sales_lines AS s
),
with_next AS (
    SELECT customer_id,
           order_date,
           LEAD(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS next_order_date,
           ROW_NUMBER()     OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS order_number
    FROM customer_orders
)
SELECT c.customer_name,
       w.order_date                     AS first_order,
       w.next_order_date                AS second_order,
       DATEDIFF(w.next_order_date, w.order_date) AS days_to_second_order
FROM with_next AS w
JOIN customers AS c ON w.customer_id = c.customer_id
WHERE w.order_number = 1
  AND w.next_order_date IS NOT NULL
ORDER BY days_to_second_order DESC
LIMIT 5;

-- ---------------------------------------------------------------
-- Answer to exercise 8 (book line 1884)
WITH monthly AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month,
           COUNT(DISTINCT order_id)              AS orders
    FROM sales_lines
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
)
SELECT month,
       orders,
       ROUND(AVG(orders) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1) AS moving_avg_3m
FROM monthly
ORDER BY month;

-- ---------------------------------------------------------------
-- Answer to exercise 9 (book line 1920)
WITH product_revenue AS (
    SELECT p.product_name, SUM(s.net_revenue) AS revenue
    FROM sales_lines AS s
    JOIN products    AS p ON s.product_id = p.product_id
    GROUP BY p.product_name
),
cumulative AS (
    SELECT product_name,
           revenue,
           100.0 * revenue / SUM(revenue) OVER () AS pct_of_total,
           100.0 * SUM(revenue) OVER (ORDER BY revenue DESC, product_name
                                      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                 / SUM(revenue) OVER ()           AS cumulative_pct
    FROM product_revenue
)
SELECT product_name,
       ROUND(revenue, 0)        AS revenue,
       ROUND(cumulative_pct, 1) AS cumulative_pct,
       CASE WHEN cumulative_pct - pct_of_total < 80 THEN 'A'
            WHEN cumulative_pct - pct_of_total < 95 THEN 'B'
            ELSE 'C' END        AS abc_class
FROM cumulative
ORDER BY revenue DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 10 (book line 1962)
WITH first_submissions AS (
    SELECT lead_id, source
    FROM (
        SELECT lead_id, source,
               ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY created_at, lead_id) AS submission_no
        FROM leads
    ) AS numbered
    WHERE submission_no = 1
)
SELECT f.source,
       COUNT(*)                                                  AS unique_leads,
       COUNT(w.lead_id)                                          AS won,
       ROUND(100.0 * COUNT(w.lead_id) / COUNT(*), 1)             AS win_rate_pct
FROM first_submissions AS f
LEFT JOIN lead_stage_history AS w
       ON w.lead_id = f.lead_id
      AND w.stage   = 'Won'
GROUP BY f.source
ORDER BY win_rate_pct DESC, unique_leads DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 11 (book line 1999)
WITH customer_orders AS (
    SELECT DISTINCT customer_id, order_id, order_date
    FROM sales_lines
),
gaps AS (
    SELECT customer_id,
           LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date, order_id) AS gap_start,
           order_date                                                                   AS gap_end,
           COUNT(*) OVER (PARTITION BY customer_id)                                     AS total_orders
    FROM customer_orders
),
ranked AS (
    SELECT customer_id, gap_start, gap_end, DATEDIFF(gap_end, gap_start) AS gap_days,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY DATEDIFF(gap_end, gap_start) DESC, gap_start) AS rn
    FROM gaps
    WHERE gap_start IS NOT NULL
      AND total_orders >= 3
)
SELECT c.customer_name, r.gap_start, r.gap_end, r.gap_days
FROM ranked    AS r
JOIN customers AS c ON r.customer_id = c.customer_id
WHERE r.rn = 1
ORDER BY r.gap_days DESC, c.customer_name
LIMIT 5;

-- ---------------------------------------------------------------
-- Answer to exercise 12 (book line 2041)
WITH monthly AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE)
),
smoothed AS (
    SELECT month,
           revenue,
           AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 3 PRECEDING AND 1 PRECEDING) AS avg_prev_3m
    FROM monthly
)
SELECT month,
       ROUND(revenue, 0)                                   AS revenue,
       ROUND(avg_prev_3m, 0)                               AS avg_previous_3_months,
       ROUND(100.0 * (revenue - avg_prev_3m) / avg_prev_3m, 1) AS pct_vs_recent_average
FROM smoothed
WHERE revenue < 0.8 * avg_prev_3m
ORDER BY month;

-- ---------------------------------------------------------------
-- Answer to exercise 16 (book line 2080)
WITH RECURSIVE days AS (
    SELECT DATE '2025-12-01' AS day
    UNION ALL
    SELECT day + INTERVAL 1 DAY
    FROM days
    WHERE day < DATE '2025-12-31'
),
daily_sales AS (
    SELECT order_date, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE order_date >= '2025-12-01' AND order_date < '2026-01-01'
    GROUP BY order_date
)
SELECT COUNT(*)                                          AS days_in_month,
       SUM(CASE WHEN s.order_date IS NULL THEN 1 ELSE 0 END) AS days_without_orders,
       ROUND(SUM(COALESCE(s.revenue, 0)), 0)             AS month_revenue
FROM days AS d
LEFT JOIN daily_sales AS s ON s.order_date = d.day;
