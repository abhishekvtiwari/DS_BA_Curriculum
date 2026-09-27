\echo '### X2'
SELECT category,
       ROUND(SUM(net_revenue), 0)                                     AS revenue,
       ROUND(100.0 * SUM(net_revenue) / SUM(SUM(net_revenue)) OVER (), 1) AS pct_of_total
FROM sales_lines
GROUP BY category
ORDER BY revenue DESC;
\echo '### X3'
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
\echo '### X4'
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
\echo '### X5'
WITH rep_months AS (
    SELECT e.employee_name,
           DATE_TRUNC('month', s.order_date)::date AS month,
           SUM(s.net_revenue)                      AS revenue
    FROM sales_lines AS s
    JOIN employees   AS e ON s.sales_rep_id = e.employee_id
    GROUP BY e.employee_name, DATE_TRUNC('month', s.order_date)
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
\echo '### X6'
WITH quarterly AS (
    SELECT c.segment,
           EXTRACT(QUARTER FROM s.order_date) AS quarter,
           SUM(s.net_revenue)                 AS revenue
    FROM sales_lines AS s
    JOIN customers   AS c ON s.customer_id = c.customer_id
    GROUP BY c.segment, EXTRACT(QUARTER FROM s.order_date)
)
SELECT segment,
       'Q' || quarter                                                   AS quarter,
       ROUND(revenue, 0)                                                AS revenue,
       ROUND(LAG(revenue) OVER w, 0)                                    AS previous_quarter,
       ROUND(100.0 * (revenue - LAG(revenue) OVER w) / LAG(revenue) OVER w, 1) AS pct_change
FROM quarterly
WINDOW w AS (PARTITION BY segment ORDER BY quarter)
ORDER BY segment, quarter;
\echo '### X7'
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
       w.next_order_date - w.order_date AS days_to_second_order
FROM with_next AS w
JOIN customers AS c ON w.customer_id = c.customer_id
WHERE w.order_number = 1
  AND w.next_order_date IS NOT NULL
ORDER BY days_to_second_order DESC
LIMIT 5;
\echo '### X8'
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month,
           COUNT(DISTINCT order_id)              AS orders
    FROM sales_lines
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT month,
       orders,
       ROUND(AVG(orders) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1) AS moving_avg_3m
FROM monthly
ORDER BY month;
\echo '### X9'
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
\echo '### X10'
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
\echo '### X11'
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
    SELECT customer_id, gap_start, gap_end, gap_end - gap_start AS gap_days,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY gap_end - gap_start DESC, gap_start) AS rn
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
\echo '### X12'
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date)::date AS month, SUM(net_revenue) AS revenue
    FROM sales_lines
    GROUP BY DATE_TRUNC('month', order_date)
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
