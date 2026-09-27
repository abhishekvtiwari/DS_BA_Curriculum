-- Analyst to Architect · Chapter 7, The Data Landscape
-- What: the section 7.6 "quiet customers" query, in MySQL (the PostgreSQL version is printed in the chapter
--       and repeated at the bottom of this file as a comment).
-- How to run:  mysql -u root -t riverstone_2025 < ch07_queries_mysql.sql
--   (load the practice databases first: tools/setup_databases.sh, or Chapter 12, section 12.3)
-- Tested on: MySQL 8.0.46; PostgreSQL 16 for the PostgreSQL version. Results identical (5 rows).
-- Riverstone Supplies is fictional; every name and number is invented.

-- Customers with no non-cancelled order in the 60 days up to 31 December 2025,
-- including customers who have never ordered.
SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                         AS last_order_date,
       DATEDIFF('2025-12-31', MAX(o.order_date)) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < '2025-11-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date IS NOT NULL, last_order_date;

-- PostgreSQL version (run with: psql -d riverstone_2025):
-- SELECT c.customer_name,
--        c.segment,
--        MAX(o.order_date)                     AS last_order_date,
--        DATE '2025-12-31' - MAX(o.order_date) AS days_since_last_order
-- FROM customers AS c
-- LEFT JOIN orders AS o
--        ON c.customer_id = o.customer_id
--       AND o.status <> 'Cancelled'
-- GROUP BY c.customer_id, c.customer_name, c.segment
-- HAVING MAX(o.order_date) < DATE '2025-11-01'
--     OR MAX(o.order_date) IS NULL
-- ORDER BY last_order_date NULLS FIRST;
