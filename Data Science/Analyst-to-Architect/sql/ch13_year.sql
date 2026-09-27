\echo '### VIEW25'
DROP VIEW IF EXISTS sales_lines;
CREATE VIEW sales_lines AS
SELECT o.order_id, o.order_date, o.customer_id, o.sales_rep_id, o.status, oi.product_id, p.category, oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS net_revenue,
       oi.quantity * p.unit_cost AS product_cost
FROM orders AS o JOIN order_items AS oi ON o.order_id = oi.order_id JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled';
\echo '### Y0 overview'
SELECT COUNT(DISTINCT order_id) AS orders, COUNT(DISTINCT customer_id) AS customers, ROUND(SUM(net_revenue), 0) AS net_revenue
FROM sales_lines;
\echo '### Y1'
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month,
           SUM(net_revenue)                      AS revenue
    FROM sales_lines
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT month,
       ROUND(revenue, 0)                                              AS revenue,
       ROUND(LAG(revenue) OVER w, 0)                                  AS previous_month,
       ROUND(revenue - LAG(revenue) OVER w, 0)                        AS change,
       ROUND(100.0 * (revenue - LAG(revenue) OVER w) / LAG(revenue) OVER w, 1) AS pct_change
FROM monthly
WINDOW w AS (ORDER BY month)
ORDER BY month;
\echo '### Y2'
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY DATE_TRUNC('month', order_date)
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
\echo '### Y3'
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT month,
       ROUND(revenue, 0) AS revenue,
       ROUND(AVG(revenue) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS moving_avg_3m,
       COUNT(*)          OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)      AS months_in_window
FROM monthly
ORDER BY month;
\echo '### Y4'
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
\echo '### Y5'
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
\echo '### Y7'
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
\echo '### Y7sum'
WITH customer_revenue AS (
    SELECT c.customer_name, SUM(s.net_revenue) AS revenue
    FROM sales_lines AS s JOIN customers AS c ON s.customer_id = c.customer_id
    GROUP BY c.customer_name
),
cumulative AS (
    SELECT customer_name, revenue,
           100.0 * revenue / SUM(revenue) OVER () AS pct_of_total,
           100.0 * SUM(revenue) OVER (ORDER BY revenue DESC, customer_name ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / SUM(revenue) OVER () AS cumulative_pct
    FROM customer_revenue
),
classified AS (
    SELECT *, CASE WHEN cumulative_pct - pct_of_total < 80 THEN 'A' WHEN cumulative_pct - pct_of_total < 95 THEN 'B' ELSE 'C' END AS abc_class
    FROM cumulative
)
SELECT abc_class, COUNT(*) AS customers, ROUND(SUM(pct_of_total), 1) AS pct_of_revenue
FROM classified GROUP BY abc_class ORDER BY abc_class;
\echo '### Y8'
WITH numbered AS (
    SELECT lead_id,
           company_name,
           email,
           created_at,
           ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY created_at) AS submission_no,
           COUNT(*)     OVER (PARTITION BY LOWER(email))                     AS submissions
    FROM leads
)
SELECT lead_id, company_name, email, created_at, submission_no
FROM numbered
WHERE submissions > 1
ORDER BY email, submission_no;
\echo '### Y8count'
SELECT COUNT(*) AS lead_rows, COUNT(DISTINCT LOWER(email)) AS unique_enquiries FROM leads;
\echo '### Y9'
WITH first_submissions AS (
    SELECT lead_id
    FROM (
        SELECT lead_id,
               ROW_NUMBER() OVER (PARTITION BY LOWER(email) ORDER BY created_at) AS submission_no
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
\echo '### Y9raw'
SELECT stage, COUNT(*) FROM lead_stage_history WHERE stage IN ('New','Contacted','Quoted','Won') GROUP BY stage ORDER BY COUNT(*) DESC;
\echo '### Y10naive'
WITH furniture AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE category = 'Furniture'
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT month, ROUND(revenue, 0) AS revenue, ROUND(LAG(revenue) OVER (ORDER BY month), 0) AS previous_month
FROM furniture
ORDER BY month;
\echo '### Y10'
WITH months AS (
    SELECT generate_series(DATE '2025-01-01', DATE '2025-12-01', INTERVAL '1 month')::date AS month
),
furniture AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE category = 'Furniture'
    GROUP BY DATE_TRUNC('month', order_date)
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
\echo '### Y11'
WITH order_days AS (
    SELECT DISTINCT customer_id, order_date
    FROM sales_lines
),
gaps AS (
    SELECT customer_id,
           order_date,
           order_date - LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS gap_days
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
       DATE '2025-12-31' - r.last_order AS days_since_last,
       CASE WHEN DATE '2025-12-31' - r.last_order > 2 * r.usual_gap_days
            THEN 'At risk' ELSE 'On rhythm' END AS status
FROM customer_rhythm AS r
JOIN customers       AS c ON r.customer_id = c.customer_id
ORDER BY (DATE '2025-12-31' - r.last_order) / r.usual_gap_days DESC
LIMIT 8;
\echo '### Y12'
WITH first_orders AS (
    SELECT customer_id, DATE_TRUNC('month', MIN(order_date))::date AS first_month
    FROM sales_lines
    GROUP BY customer_id
),
active_months AS (
    SELECT DISTINCT customer_id, DATE_TRUNC('month', order_date)::date AS month
    FROM sales_lines
),
cohort_activity AS (
    SELECT f.customer_id,
           'Q' || EXTRACT(QUARTER FROM f.first_month) AS cohort,
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
\echo '### Y13demo'
WITH months AS (
    SELECT DISTINCT customer_id, DATE_TRUNC('month', order_date)::date AS month
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
\echo '### Y13'
WITH months AS (
    SELECT DISTINCT customer_id, DATE_TRUNC('month', order_date)::date AS month
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
\echo '### Y14'
SELECT category,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(QUARTER FROM order_date) = 1), 0) AS q1,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(QUARTER FROM order_date) = 2), 0) AS q2,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(QUARTER FROM order_date) = 3), 0) AS q3,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(QUARTER FROM order_date) = 4), 0) AS q4,
       ROUND(SUM(net_revenue), 0)                                                     AS full_year
FROM sales_lines
GROUP BY category
ORDER BY full_year DESC;
\echo '### Y15'
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
