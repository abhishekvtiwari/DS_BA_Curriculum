-- Analyst to Architect, Chapter 15: every query in the chapter, in its MySQL 8.0 form.
-- Run against riverstone_full:   mysql -u root -t riverstone_full < ch15_queries_mysql.sql
-- Each result matches the PostgreSQL output printed in the chapter (section 15.15 lists the differences).

-- Section 15.1: 2025 revenue and share by segment (runs unchanged)
SELECT c.segment, ROUND(SUM(s.net_revenue)) AS net_revenue,
       ROUND(100 * SUM(s.net_revenue) / SUM(SUM(s.net_revenue)) OVER (), 1) AS share_pct
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY c.segment
ORDER BY net_revenue DESC;

-- Section 15.4: month x year pivot (FILTER becomes SUM(CASE ...); EXTRACT becomes MONTH()/YEAR())
SELECT MONTH(order_date) AS month,
       ROUND(SUM(CASE WHEN YEAR(order_date) = 2024 THEN net_revenue END)) AS rev_2024,
       ROUND(SUM(CASE WHEN YEAR(order_date) = 2025 THEN net_revenue END)) AS rev_2025
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY 1 ORDER BY 1;

-- Section 15.5: histogram, 25,000 and 5,000 bins (run unchanged)
WITH order_values AS (
  SELECT order_id, SUM(net_revenue) AS order_value FROM sales_lines
  WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31' GROUP BY order_id
)
SELECT FLOOR(order_value / 25000) * 25000 AS bin_start, COUNT(*) AS orders
FROM order_values GROUP BY 1 ORDER BY 1;

WITH order_values AS (
  SELECT order_id, SUM(net_revenue) AS order_value FROM sales_lines
  WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31' GROUP BY order_id
)
SELECT FLOOR(order_value / 5000) * 5000 AS bin_start, COUNT(*) AS orders
FROM order_values GROUP BY 1 ORDER BY 1;

-- Section 15.5: median order value per segment (MySQL has no PERCENTILE_CONT; exercise 21)
WITH order_values AS (
  SELECT s.order_id, c.segment, SUM(s.net_revenue) AS order_value
  FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id
  WHERE s.order_date BETWEEN '2025-01-01' AND '2025-12-31'
  GROUP BY s.order_id, c.segment
), ranked AS (
  SELECT segment, order_value,
         ROW_NUMBER() OVER (PARTITION BY segment ORDER BY order_value) AS rn,
         COUNT(*) OVER (PARTITION BY segment) AS n
  FROM order_values
)
SELECT segment, ROUND(AVG(order_value)) AS median
FROM ranked WHERE rn IN (FLOOR((n + 1) / 2), CEIL((n + 1) / 2))
GROUP BY segment ORDER BY median;

-- Section 15.11: monthly revenue against target (DATE_TRUNC(...)::date becomes CAST(DATE_FORMAT(...) AS DATE))
WITH monthly AS (
  SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS m, SUM(net_revenue) AS revenue
  FROM sales_lines
  GROUP BY 1
)
SELECT t.target_month, ROUND(a.revenue) AS net_revenue, t.target_revenue,
       ROUND(100 * a.revenue / t.target_revenue, 1) AS pct_of_target
FROM sales_targets t
JOIN monthly a ON a.m = t.target_month
WHERE t.target_month >= '2025-01-01'
ORDER BY t.target_month;
