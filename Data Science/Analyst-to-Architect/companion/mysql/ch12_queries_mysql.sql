-- =====================================================================
-- Analyst to Architect · Chapter 12 · Databases & SQL Foundations
-- Every query in the chapter, rewritten for MySQL, in book order.
--
-- Setup: run riverstone_setup_mysql.sql first (it creates the `riverstone` database).
-- Tested on MySQL 8.0; uses only features that work the same in MySQL 8.4 LTS and 9.x.
-- Results match the PostgreSQL outputs printed in the chapter, except where a
-- comment says otherwise (NULL sort order). Queries that fail on purpose in the
-- book are commented out, with the MySQL error you'd see.
-- Riverstone Supplies is fictional; every name and number is invented.
-- =====================================================================

-- ---------------------------------------------------------------
-- 12.4 Your first query: SELECT and FROM (book line 414)
USE riverstone;
SELECT customer_name, city
FROM customers;

-- ---------------------------------------------------------------
-- 12.4 Your first query: SELECT and FROM › SELECT * — every column (book line 447)
SELECT * FROM products;

-- ---------------------------------------------------------------
-- 12.4 Your first query: SELECT and FROM › Calculated columns and aliases (book line 457)
SELECT product_name,
       unit_price,
       ROUND(unit_price * 1.18, 2) AS price_incl_tax
FROM products;

-- ---------------------------------------------------------------
-- 12.4 Your first query: SELECT and FROM › DISTINCT — unique values only (book line 486)
-- MySQL lists the NULL (missing) city first; PostgreSQL lists it last. Write ORDER BY city IS NULL, city to match.
SELECT DISTINCT city
FROM customers
ORDER BY city;

-- ---------------------------------------------------------------
-- 12.5 WHERE: keeping only the rows you want (book line 512)
SELECT order_id, customer_id, order_date, status
FROM orders
WHERE status = 'Delivered';

-- ---------------------------------------------------------------
-- 12.5 WHERE: keeping only the rows you want › Combining conditions: AND, OR, NOT (book line 551)
SELECT customer_name, city, segment
FROM customers
WHERE segment = 'Retail' OR segment = 'Wholesale' AND city = 'Mumbai';

-- ---------------------------------------------------------------
-- 12.5 WHERE: keeping only the rows you want › Combining conditions: AND, OR, NOT (book line 572)
SELECT customer_name, city, segment
FROM customers
WHERE (segment = 'Retail' OR segment = 'Wholesale')
  AND city = 'Mumbai';

-- ---------------------------------------------------------------
-- 12.5 WHERE: keeping only the rows you want › IN, BETWEEN, and LIKE (book line 596)
SELECT order_id, order_date, status
FROM orders
WHERE order_date BETWEEN '2026-02-01' AND '2026-02-28'
  AND status IN ('Delivered', 'Shipped');

-- ---------------------------------------------------------------
-- 12.5 WHERE: keeping only the rows you want › IN, BETWEEN, and LIKE (book line 618)
SELECT product_name, unit_price
FROM products
WHERE product_name LIKE 'Storage%';

-- ---------------------------------------------------------------
-- 12.5 WHERE: keeping only the rows you want › Real-life example: which products barely make money? (book line 647)
SELECT product_name,
       unit_price,
       unit_cost,
       ROUND(100.0 * (unit_price - unit_cost) / unit_price, 1) AS margin_pct
FROM products
WHERE (unit_price - unit_cost) / unit_price < 0.30
ORDER BY margin_pct;

-- ---------------------------------------------------------------
-- 12.6 NULL: the value that isn't there › NULL is not equal to anything, not even NULL (book line 682)
SELECT customer_name
FROM customers
WHERE city = NULL;

-- ---------------------------------------------------------------
-- 12.6 NULL: the value that isn't there › NULL is not equal to anything, not even NULL (book line 698)
SELECT customer_name
FROM customers
WHERE city IS NULL;

-- ---------------------------------------------------------------
-- 12.6 NULL: the value that isn't there › The silent disappearance (book line 715)
SELECT customer_name, city
FROM customers
WHERE city <> 'Mumbai';

-- ---------------------------------------------------------------
-- 12.6 NULL: the value that isn't there › The silent disappearance (book line 734)
-- A fragment shown in the text, not a complete query.
-- WHERE city <> 'Mumbai' OR city IS NULL;

-- ---------------------------------------------------------------
-- 12.6 NULL: the value that isn't there › Replacing NULLs with COALESCE (book line 746)
SELECT customer_name,
       COALESCE(city, 'Unknown') AS city
FROM customers
ORDER BY customer_id;

-- ---------------------------------------------------------------
-- 12.7 ORDER BY and LIMIT: sorting and top-N (book line 785)
SELECT customer_name, segment, signup_date
FROM customers
ORDER BY segment ASC, signup_date DESC;

-- ---------------------------------------------------------------
-- 12.7 ORDER BY and LIMIT: sorting and top-N (book line 809)
SELECT product_name, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 3;

-- ---------------------------------------------------------------
-- 12.8 Transforming values: CASE, dates, and text › CASE: if-then logic inside a query (book line 839)
SELECT product_name,
       unit_price,
       CASE
           WHEN unit_price >= 1000 THEN 'Premium'
           WHEN unit_price >= 500  THEN 'Mid-range'
           ELSE 'Budget'
       END AS price_band
FROM products
ORDER BY unit_price;

-- ---------------------------------------------------------------
-- 12.8 Transforming values: CASE, dates, and text › Real-life example: which invoices are overdue? (book line 871)
SELECT invoice_id,
       due_date,
       CASE
           WHEN due_date >= DATE '2026-03-31'             THEN 'Not yet due'
           WHEN DATEDIFF(DATE '2026-03-31', due_date) <= 30         THEN 'Overdue 1-30 days'
           WHEN DATEDIFF(DATE '2026-03-31', due_date) <= 60         THEN 'Overdue 31-60 days'
           ELSE 'Overdue 60+ days'
       END AS due_status
FROM invoices
ORDER BY due_date;

-- ---------------------------------------------------------------
-- 12.8 Transforming values: CASE, dates, and text › Working with dates (book line 915)
SELECT order_id,
       order_date,
       EXTRACT(MONTH FROM order_date)        AS month_no,
       CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS order_month
FROM orders
WHERE order_id <= 5004;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING › Aggregate functions (book line 976)
SELECT COUNT(*)                    AS total_orders,
       COUNT(sales_rep_id)         AS orders_with_rep,
       COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING › GROUP BY: one summary row per group (book line 1000)
SELECT status,
       COUNT(*) AS num_orders
FROM orders
GROUP BY status
ORDER BY num_orders DESC, status;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING › GROUP BY: one summary row per group (book line 1022)
SELECT order_id,
       ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS order_revenue
FROM order_items
GROUP BY order_id
ORDER BY order_id
LIMIT 5;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING › Real-life example: revenue is not profit (book line 1048)
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue,
       ROUND(SUM(oi.quantity * p.unit_cost), 0)                                  AS product_cost,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost), 0)                                  AS gross_profit,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)
               - oi.quantity * p.unit_cost)
             / SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 1) AS margin_pct
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY net_revenue DESC;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING › The GROUP BY rule (book line 1089)
-- Fails on purpose, as in the book. MySQL says: ERROR 1055: Expression #2 of SELECT list is not in GROUP BY clause ... incompatible with sql_mode=only_full_group_by
-- SELECT customer_id, order_date, COUNT(*)
-- FROM orders
-- GROUP BY customer_id;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING › Conditional aggregation: CASE inside SUM (book line 1108)
SELECT segment,
       COUNT(*)                                        AS customers,
       SUM(CASE WHEN city = 'Mumbai' THEN 1 ELSE 0 END) AS in_mumbai
FROM customers
GROUP BY segment
ORDER BY segment;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING › HAVING: filtering groups (book line 1130)
-- Fails on purpose, as in the book. MySQL says: ERROR 1054: Unknown column 'num_orders' in 'where clause'
-- SELECT customer_id, COUNT(*) AS num_orders
-- FROM orders
-- WHERE num_orders > 1
-- GROUP BY customer_id;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING › HAVING: filtering groups (book line 1143)
SELECT customer_id, COUNT(*) AS num_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY customer_id;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › INNER JOIN (book line 1180)
SELECT o.order_id,
       c.customer_name,
       o.order_date
FROM orders AS o
INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
ORDER BY o.order_id
LIMIT 4;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › LEFT JOIN: keep everything on the left (book line 1216)
SELECT c.customer_name,
       o.order_id
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The anti-join: finding what's missing (book line 1263)
-- Customers who have never placed an order
SELECT c.customer_name
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The anti-join: finding what's missing (book line 1279)
-- Products that have never been sold
SELECT p.product_name
FROM products AS p
LEFT JOIN order_items AS oi
       ON p.product_id = oi.product_id
WHERE oi.order_item_id IS NULL;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › RIGHT JOIN, FULL OUTER JOIN, and CROSS JOIN (book line 1303)
SELECT s.segment, p.category
FROM (SELECT DISTINCT segment  FROM customers) AS s
CROSS JOIN
     (SELECT DISTINCT category FROM products)  AS p
ORDER BY s.segment, p.category
LIMIT 5;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The self-join: a table joined to itself (book line 1329)
SELECT e.employee_name,
       e.job_title,
       m.employee_name AS manager_name
FROM employees AS e
LEFT JOIN employees AS m
       ON e.manager_id = m.employee_id
ORDER BY e.employee_id;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › Joining three or more tables (book line 1356)
SELECT COALESCE(c.city, 'Unknown') AS city,
       COUNT(DISTINCT o.order_id)  AS orders,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS revenue
FROM orders AS o
JOIN customers   AS c  ON o.customer_id = c.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
WHERE o.status <> 'Cancelled'
GROUP BY COALESCE(c.city, 'Unknown')
ORDER BY revenue DESC;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The fan-out trap: when joins inflate your numbers (book line 1386)
SELECT c.customer_name, COUNT(*) AS num_orders
FROM customers AS c
JOIN orders      AS o  ON c.customer_id = o.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
GROUP BY c.customer_name
ORDER BY c.customer_name;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The fan-out trap: when joins inflate your numbers (book line 1415)
SELECT c.customer_name, COUNT(DISTINCT o.order_id) AS num_orders
FROM customers AS c
JOIN orders      AS o  ON c.customer_id = o.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
GROUP BY c.customer_name
ORDER BY c.customer_name;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The same trap with money (book line 1441)
SELECT SUM(i.amount)                   AS total_invoiced,
       SUM(p.amount)                   AS total_paid,
       SUM(i.amount) - SUM(p.amount)   AS outstanding
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The same trap with money (book line 1458)
SELECT i.invoice_id, i.amount AS invoice_amount, p.payment_id, p.amount AS payment_amount
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE i.invoice_id IN (9001, 9002, 9007)
ORDER BY i.invoice_id, p.payment_id;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The same trap with money (book line 1484)
SELECT SUM(i.amount)                        AS total_invoiced,
       SUM(COALESCE(p.paid, 0))             AS total_paid,
       SUM(i.amount - COALESCE(p.paid, 0))  AS outstanding
FROM invoices AS i
LEFT JOIN (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
) AS p ON i.invoice_id = p.invoice_id;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The LEFT JOIN that quietly became an INNER JOIN (book line 1518)
-- Version A: condition in ON
SELECT c.customer_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status = 'Pending'
ORDER BY c.customer_id;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables › The LEFT JOIN that quietly became an INNER JOIN (book line 1542)
-- Version B: condition in WHERE
SELECT c.customer_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
WHERE o.status = 'Pending'
ORDER BY c.customer_id;

-- ---------------------------------------------------------------
-- 12.12 Queries inside queries: subqueries and set operations › Subqueries (book line 1611)
SELECT product_name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products)
ORDER BY unit_price;

-- ---------------------------------------------------------------
-- 12.12 Queries inside queries: subqueries and set operations › Subqueries (book line 1631)
SELECT customer_name
FROM customers
WHERE customer_id IN (
    SELECT o.customer_id
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE oi.product_id = 105
)
ORDER BY customer_name;

-- ---------------------------------------------------------------
-- 12.12 Queries inside queries: subqueries and set operations › Subqueries (book line 1653)
SELECT c.customer_name
FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
      AND o.status = 'Shipped'
)
ORDER BY c.customer_name;

-- ---------------------------------------------------------------
-- 12.12 Queries inside queries: subqueries and set operations › Subqueries (book line 1677)
SELECT p.invoice_id, p.payment_date, p.amount
FROM payments AS p
WHERE p.payment_date = (
    SELECT MAX(p2.payment_date)
    FROM payments AS p2
    WHERE p2.invoice_id = p.invoice_id
)
ORDER BY p.invoice_id;

-- ---------------------------------------------------------------
-- 12.12 Queries inside queries: subqueries and set operations › Subqueries (book line 1708)
SELECT ROUND(AVG(order_revenue), 2) AS avg_order_value
FROM (
    SELECT o.order_id,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_id
) AS per_order;

-- ---------------------------------------------------------------
-- 12.12 Queries inside queries: subqueries and set operations › Set operations: stacking results (book line 1736)
-- MySQL lists the NULL (missing) city first; PostgreSQL lists it last. Write ORDER BY city IS NULL, city to match.
SELECT city FROM customers WHERE segment = 'Retail'
UNION
SELECT city FROM customers WHERE segment = 'Hospitality'
ORDER BY city;

-- ---------------------------------------------------------------
-- 12.14 Writing SQL that humans can read (book line 2996)
select c.city,count(distinct o.order_id),sum(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)) from orders o join customers c on o.customer_id=c.customer_id join order_items oi on o.order_id=oi.order_id where o.status<>'Cancelled' group by c.city order by 3 desc;

-- ---------------------------------------------------------------
-- 12.15 Putting it all together: Monday morning with the sales head › Question 1: "Which customers have gone quiet?" (book line 3040)
SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                     AS last_order_date,
       DATEDIFF(DATE '2026-03-31', MAX(o.order_date)) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2026-03-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date IS NULL DESC, last_order_date;

-- ---------------------------------------------------------------
-- 12.15 Putting it all together: Monday morning with the sales head › Question 2: "How much are discounts costing us?" (book line 3078)
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price), 0)                           AS list_value,
       ROUND(SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100), 0)   AS discount_given,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100)
             / SUM(oi.quantity * oi.unit_price), 1)                         AS discount_pct_of_list
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY discount_given DESC;

-- ---------------------------------------------------------------
-- 12.15 Putting it all together: Monday morning with the sales head › Question 3: "Who owes us money, and how late is it?" (book line 3117)
SELECT i.invoice_id,
       i.amount,
       COALESCE(pay.paid, 0.00)            AS paid,
       i.amount - COALESCE(pay.paid, 0.00) AS balance
FROM invoices AS i
LEFT JOIN (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
) AS pay ON i.invoice_id = pay.invoice_id
ORDER BY i.invoice_id;

-- ---------------------------------------------------------------
-- 12.15 Putting it all together: Monday morning with the sales head › Question 3: "Who owes us money, and how late is it?" (book line 3149)
SELECT c.customer_name,
       SUM(inv.balance) AS total_due,
       SUM(CASE WHEN inv.due_date >= DATE '2026-03-31' THEN inv.balance ELSE 0.00 END) AS not_yet_due,
       SUM(CASE WHEN inv.due_date <  DATE '2026-03-31'
                 AND DATEDIFF(DATE '2026-03-31', inv.due_date) <= 30 THEN inv.balance ELSE 0.00 END) AS overdue_1_30,
       SUM(CASE WHEN DATEDIFF(DATE '2026-03-31', inv.due_date) BETWEEN 31 AND 60 THEN inv.balance ELSE 0.00 END) AS overdue_31_60,
       SUM(CASE WHEN DATEDIFF(DATE '2026-03-31', inv.due_date) > 60 THEN inv.balance ELSE 0.00 END) AS overdue_60_plus
FROM (
    SELECT i.invoice_id, i.order_id, i.due_date,
           i.amount - COALESCE(pay.paid, 0) AS balance
    FROM invoices AS i
    LEFT JOIN (SELECT invoice_id, SUM(amount) AS paid FROM payments GROUP BY invoice_id) AS pay
           ON i.invoice_id = pay.invoice_id
) AS inv
JOIN orders    AS o ON inv.order_id  = o.order_id
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE inv.balance > 0
GROUP BY c.customer_name
ORDER BY total_due DESC;

-- ---------------------------------------------------------------
-- 12.15 Putting it all together: Monday morning with the sales head › Question 4: "How is each sales rep doing, and who do they report to?" (book line 3199)
SELECT e.employee_name                         AS sales_rep,
       COALESCE(m.employee_name, '(none)')     AS reports_to,
       COUNT(DISTINCT o.order_id)              AS orders,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM employees AS e
LEFT JOIN employees   AS m  ON e.manager_id   = m.employee_id
JOIN      orders      AS o  ON o.sales_rep_id = e.employee_id
JOIN      order_items AS oi ON oi.order_id    = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY e.employee_name, m.employee_name
ORDER BY net_revenue DESC;

-- ---------------------------------------------------------------
-- 12.16 The same SQL in MySQL › Trap 1: subtracting dates gives a number, not days (book line 3266)
SELECT DATE '2026-03-31' - DATE '2026-02-05'         AS looks_like_days,
       DATEDIFF(DATE '2026-03-31', DATE '2026-02-05') AS actual_days;

-- ---------------------------------------------------------------
-- 12.16 The same SQL in MySQL › Trap 1: subtracting dates gives a number, not days (book line 3285)
SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                              AS last_order_date,
       DATEDIFF(DATE '2026-03-31', MAX(o.order_date)) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2026-03-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date IS NULL DESC, last_order_date;

-- ---------------------------------------------------------------
-- 12.16 The same SQL in MySQL › Trap 2: MySQL ignores capital letters when comparing text (book line 3321)
SELECT COUNT(*) AS delivered_orders
FROM orders
WHERE status = 'delivered';

-- ---------------------------------------------------------------
-- 12.16 The same SQL in MySQL › Trap 3: `||` means OR, not "join text" (book line 3347)
SELECT 'Riverstone' || ' Supplies'      AS pipes,
       CONCAT('Riverstone', ' Supplies') AS concat_result;

-- ---------------------------------------------------------------
-- 12.16 The same SQL in MySQL › No FULL OUTER JOIN: reconciliation the MySQL way (book line 3385)
-- PostgreSQL-only version (MySQL has no FULL OUTER JOIN); the MySQL version follows.
-- SELECT o.order_id, o.status, i.invoice_id
-- FROM orders AS o
-- FULL OUTER JOIN invoices AS i ON o.order_id = i.order_id
-- WHERE o.order_id IS NULL OR i.invoice_id IS NULL
-- ORDER BY o.order_id;

-- ---------------------------------------------------------------
-- 12.16 The same SQL in MySQL › No FULL OUTER JOIN: reconciliation the MySQL way (book line 3403)
SELECT o.order_id, o.status, i.invoice_id
FROM orders AS o
LEFT JOIN invoices AS i ON o.order_id = i.order_id
WHERE i.invoice_id IS NULL
UNION ALL
SELECT o.order_id, o.status, i.invoice_id
FROM orders AS o
RIGHT JOIN invoices AS i ON o.order_id = i.order_id
WHERE o.order_id IS NULL
ORDER BY order_id;

-- ---------------------------------------------------------------
-- 12.16 The same SQL in MySQL › The monthly report, in MySQL (book line 3433)
-- Monthly sales summary (MySQL)
-- Revenue counts Delivered and Shipped orders (finance policy).
SELECT CAST(DATE_FORMAT(o.order_date, '%Y-%m-01') AS DATE) AS month,
       COUNT(DISTINCT o.order_id)                          AS orders,
       COUNT(DISTINCT o.customer_id)                       AS active_customers,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi
  ON o.order_id = oi.order_id
WHERE o.status IN ('Delivered', 'Shipped')
GROUP BY month
ORDER BY month;

-- ---------------------------------------------------------------
-- In the real world: Riverstone's monthly sales report (book line 3514)
-- Monthly sales summary
-- Revenue counts Delivered and Shipped orders (finance policy);
-- Pending and Cancelled orders are excluded.
SELECT CAST(DATE_FORMAT(o.order_date, '%Y-%m-01') AS DATE) AS month,
       COUNT(DISTINCT o.order_id)             AS orders,
       COUNT(DISTINCT o.customer_id)          AS active_customers,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi
  ON o.order_id = oi.order_id
WHERE o.status IN ('Delivered', 'Shipped')
GROUP BY CAST(DATE_FORMAT(o.order_date, '%Y-%m-01') AS DATE)
ORDER BY month;

-- ---------------------------------------------------------------
-- Answer to exercise 1 (book line 3702)
SELECT product_name, unit_price
FROM products
WHERE category = 'Kitchen'
ORDER BY unit_price ASC;

-- ---------------------------------------------------------------
-- Answer to exercise 2 (book line 3719)
SELECT segment, COUNT(*) AS num_customers
FROM customers
GROUP BY segment
ORDER BY num_customers DESC, segment;

-- ---------------------------------------------------------------
-- Answer to exercise 3 (book line 3739)
SELECT order_id, customer_id, order_date
FROM orders
WHERE order_date >= '2026-03-01'
  AND order_date <  '2026-04-01'
ORDER BY order_date;

-- ---------------------------------------------------------------
-- Answer to exercise 4 (book line 3758)
SELECT customer_name
FROM customers
WHERE customer_name LIKE '%Foods%'
   OR customer_name LIKE '%Mart%';

-- ---------------------------------------------------------------
-- Answer to exercise 5 (book line 3775)
SELECT p.product_name,
       COALESCE(s.units_sold, 0) AS units_sold
FROM products AS p
LEFT JOIN (
    SELECT oi.product_id, SUM(oi.quantity) AS units_sold
    FROM order_items AS oi
    JOIN orders AS o ON oi.order_id = o.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY oi.product_id
) AS s ON p.product_id = s.product_id
ORDER BY units_sold DESC, p.product_name;

-- ---------------------------------------------------------------
-- Answer to exercise 6 (book line 3805)
SELECT COALESCE(e.employee_name, 'Unassigned') AS sales_rep,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
LEFT JOIN employees AS e ON o.sales_rep_id = e.employee_id
WHERE o.status <> 'Cancelled'
GROUP BY COALESCE(e.employee_name, 'Unassigned')
ORDER BY net_revenue DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 7 (book line 3830)
SELECT c.customer_name
FROM customers AS c
WHERE EXISTS (SELECT 1 FROM orders AS o
              WHERE o.customer_id = c.customer_id)
  AND NOT EXISTS (SELECT 1 FROM orders AS o
                  WHERE o.customer_id = c.customer_id
                    AND o.status = 'Delivered');

-- ---------------------------------------------------------------
-- Answer to exercise 8 (book line 3851)
SELECT ROUND(AVG(order_revenue), 2) AS avg_order_value
FROM (
    SELECT o.order_id,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_id
) AS per_order;

-- ---------------------------------------------------------------
-- Answer to exercise 9 (book line 3874)
SELECT method, COUNT(*) AS payments, SUM(amount) AS amount_received
FROM payments
GROUP BY method
ORDER BY amount_received DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 10 (book line 3894)
SELECT i.invoice_id, i.amount, i.due_date
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE p.payment_id IS NULL
ORDER BY i.due_date;

-- ---------------------------------------------------------------
-- Answer to exercise 11 (book line 3914)
SELECT c.customer_name,
       MIN(o.order_date)                     AS first_order,
       MAX(o.order_date)                     AS latest_order,
       DATEDIFF(MAX(o.order_date), MIN(o.order_date)) AS days_between
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY days_between DESC, c.customer_name;

-- ---------------------------------------------------------------
-- Answer to exercise 12 (book line 3942)
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))
             / (SELECT SUM(oi2.quantity * oi2.unit_price * (1 - oi2.discount_pct / 100))
                FROM order_items AS oi2
                JOIN orders AS o2 ON oi2.order_id = o2.order_id
                WHERE o2.status <> 'Cancelled'), 1) AS pct_of_total
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY net_revenue DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 13 (book line 3971)
SELECT customer_name, ROUND(customer_revenue, 0) AS customer_revenue
FROM (
    SELECT c.customer_name,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS customer_revenue
    FROM customers AS c
    JOIN orders      AS o  ON c.customer_id = o.customer_id
    JOIN order_items AS oi ON o.order_id    = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY c.customer_name
) AS t
WHERE customer_revenue > (
    SELECT AVG(customer_revenue)
    FROM (
        SELECT o.customer_id,
               SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS customer_revenue
        FROM orders AS o
        JOIN order_items AS oi ON o.order_id = oi.order_id
        WHERE o.status <> 'Cancelled'
        GROUP BY o.customer_id
    ) AS x
)
ORDER BY customer_revenue DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 14 (book line 4008)
SELECT i.invoice_id,
       i.amount,
       COUNT(p.payment_id)                   AS num_payments,
       COALESCE(SUM(p.amount), 0)            AS amount_paid,
       i.amount - COALESCE(SUM(p.amount), 0) AS balance
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
GROUP BY i.invoice_id, i.amount
HAVING i.amount - COALESCE(SUM(p.amount), 0) > 0
ORDER BY balance DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 15 (book line 4036)
SELECT order_id,
       order_date,
       status,
       DATEDIFF(DATE '2026-03-31', order_date) AS days_open
FROM orders
WHERE (status = 'Pending' AND DATEDIFF(DATE '2026-03-31', order_date) > 7)
   OR (status = 'Shipped' AND DATEDIFF(DATE '2026-03-31', order_date) > 14)
ORDER BY days_open DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 20 (book line 4068)
SELECT order_id,
       order_date,
       status,
       DATEDIFF(DATE '2026-03-31', order_date) AS days_open
FROM orders
WHERE (status = 'Pending' AND DATEDIFF(DATE '2026-03-31', order_date) > 7)
   OR (status = 'Shipped' AND DATEDIFF(DATE '2026-03-31', order_date) > 14)
ORDER BY days_open DESC;

-- ---------------------------------------------------------------
-- Answer to exercise 21 (book line 4093)
SELECT CONCAT(e.employee_name, ' (', e.job_title, ')') AS employee,
       COALESCE(m.employee_name, '(none)')             AS reports_to
FROM employees AS e
LEFT JOIN employees AS m ON e.manager_id = m.employee_id
ORDER BY e.employee_id;
