-- Analyst to Architect, Chapter 16 — the same checks in MySQL 8.0+.
-- Run:  mysql -u root -p riverstone_full < ch16_checks_mysql.sql
SELECT ROUND(SUM(net_revenue)) AS all_years,
       ROUND(SUM(CASE WHEN order_date >= '2025-01-01' THEN net_revenue END)) AS y2025,
       COUNT(DISTINCT CASE WHEN order_date >= '2025-01-01' THEN order_id END) AS orders_2025,
       COUNT(DISTINCT CASE WHEN order_date >= '2025-01-01' THEN customer_id END) AS customers_2025
FROM sales_lines;
SELECT ROUND(SUM(CASE WHEN order_date BETWEEN '2025-01-01' AND '2025-06-30' THEN net_revenue END)) AS ytd_jun_2025,
       ROUND(SUM(CASE WHEN order_date BETWEEN '2024-01-01' AND '2024-06-30' THEN net_revenue END)) AS ytd_jun_2024
FROM sales_lines;
SELECT CONCAT('Q', QUARTER(order_date)) AS quarter,
       ROUND(SUM(CASE WHEN YEAR(order_date)=2025 THEN net_revenue END)) AS rev_2025,
       ROUND(SUM(CASE WHEN YEAR(order_date)=2024 THEN net_revenue END)) AS rev_2024
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY 1 ORDER BY 1;
SELECT c.segment, ROUND(SUM(CASE WHEN s.order_date>='2025-01-01' THEN s.net_revenue END)) AS rev_2025,
       ROUND(SUM(CASE WHEN s.order_date BETWEEN '2024-01-01' AND '2024-12-31' THEN s.net_revenue END)) AS rev_2024
FROM sales_lines s JOIN customers c ON c.customer_id = s.customer_id WHERE s.order_date>='2024-01-01' GROUP BY 1 ORDER BY 2 DESC;
SELECT p.product_name, ROUND(SUM(s.net_revenue)) AS rev_2025
FROM sales_lines s JOIN products p ON p.product_id = s.product_id
WHERE s.order_date >= '2025-01-01' GROUP BY 1 ORDER BY 2 DESC;
