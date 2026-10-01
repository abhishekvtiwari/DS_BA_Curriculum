-- Chapter 32. Analytics Engineering with dbt
-- Practice SQL for MYSQL, extracted from the chapter.
--
-- Riverstone Supplies is the worked example throughout the book. Load the database
-- first (companion/riverstone_setup_mini.sql, riverstone_2025_setup.sql, or
-- companion/full/riverstone_full_setup_mysql.sql), then run these statements in order.
--
-- Each statement keeps the chapter's explanation above it and the chapter's own
-- result below it, marked as the chapter's. Run it yourself to see your own.
-- Source: manuscript/ch32-analytics-engineering-with-dbt.md


-- 326 lines and ₹43,35,471: the same numbers Chapter 28's hand-built star schema produced, which
-- is the point. What changed is that the build order, the tests, and the documentation now come
-- from the code itself. The 23 customer versions are 23 customers with one version each (the 24th,
-- Home Plus, placed no orders in 2025), where Chapter 28's dimension has 27 rows for the same 24
-- customers.

SELECT d.quarter_label,
       c.segment,
       ROUND(SUM(f.net_revenue)) AS net_revenue
FROM dbt_dev_marts.fct_sales_line AS f
JOIN dbt_dev_marts.dim_date AS d ON d.date_key = f.date_key
JOIN dbt_dev_marts.dim_customer AS c ON c.customer_key = f.customer_key
GROUP BY d.quarter_label, c.segment
ORDER BY d.quarter_label, c.segment;

/* The chapter shows:
    quarter_label |   segment   | net_revenue
   ---------------+-------------+-------------
    2025-Q1       | Hospitality |      149040
    2025-Q1       | Retail      |      394328
    2025-Q1       | Wholesale   |      190944
    2025-Q2       | Hospitality |      252170
    2025-Q2       | Retail      |      198474
    2025-Q2       | Wholesale   |      275925
    2025-Q3       | Hospitality |      307278
    2025-Q3       | Retail      |      333973
    2025-Q3       | Wholesale   |      479039
    2025-Q4       | Hospitality |      435551
    2025-Q4       | Retail      |      562000
    2025-Q4       | Wholesale   |      756751
   (12 rows)
*/

