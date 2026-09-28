-- =====================================================================
-- Analyst to Architect · Chapter 12 · Databases & SQL Foundations
-- Every reading query in the chapter, in PostgreSQL, in book order.
-- Built from the chapter by sql/ch12_companion.py; don't edit by hand.
--
-- Setup: section 12.3 (riverstone_setup.sql). Exercises 30 and 32 use the one-year database
-- (riverstone_2025_setup.sql); the file switches to it with \c, which works in psql. In DBeaver,
-- open those queries in an editor connected to riverstone_2025 instead.
-- Section 12.13's statements are in ch12_lab_postgresql.sql.
-- Queries that fail on purpose in the book are commented out, with the error you'd see.
-- Riverstone Supplies is fictional; every name and number is invented.
-- =====================================================================

-- ---------------------------------------------------------------
-- 12.3 Setting up your SQL laboratory
SELECT COUNT(*) FROM order_items;
SELECT * FROM products;

-- ---------------------------------------------------------------
-- 12.4 Your first query: SELECT and FROM
SELECT customer_name, city
FROM customers;
SELECT product_name,
       unit_price,
       unit_price * 1.18
FROM products;
SELECT product_name,
       unit_price,
       unit_price * 1.18 AS price_incl_tax
FROM products;
SELECT product_name,
       unit_price,
       ROUND(unit_price * 1.18, 2) AS price_incl_tax
FROM products;
SELECT 7 / 2   AS whole_numbers,
       7 / 2.0 AS with_a_decimal;

-- ---------------------------------------------------------------
-- 12.5 ORDER BY and LIMIT: sorting, top-N, and unique values
SELECT customer_name, segment, signup_date
FROM customers
ORDER BY segment ASC, signup_date DESC;
SELECT product_name, unit_price
FROM products
ORDER BY unit_price DESC
LIMIT 3;
SELECT DISTINCT city
FROM customers
ORDER BY city;

-- ---------------------------------------------------------------
-- 12.6 WHERE: keeping only the rows you want
SELECT order_id, customer_id, order_date, status
FROM orders
WHERE status = 'Delivered';
SELECT customer_name, city, segment
FROM customers
WHERE segment = 'Retail' OR segment = 'Wholesale' AND city = 'Mumbai';
SELECT customer_name, city, segment
FROM customers
WHERE (segment = 'Retail' OR segment = 'Wholesale')
  AND city = 'Mumbai';
SELECT order_id, order_date
FROM orders
WHERE order_date BETWEEN '2026-02-01' AND '2026-02-28';
SELECT order_id, status
FROM orders
WHERE status IN ('Delivered', 'Shipped');
SELECT order_id, order_date, status
FROM orders
WHERE order_date BETWEEN '2026-02-01' AND '2026-02-28'
  AND status IN ('Delivered', 'Shipped');
SELECT order_id, order_date, status
FROM orders
WHERE order_date >= '2026-02-01'
  AND order_date <  '2026-03-01'
  AND status IN ('Delivered', 'Shipped');
SELECT product_name, unit_price
FROM products
WHERE product_name LIKE 'Storage%';
SELECT product_name,
       unit_price,
       unit_cost,
       ROUND(100.0 * (unit_price - unit_cost) / unit_price, 1) AS margin_pct
FROM products
ORDER BY margin_pct;
SELECT product_name,
       unit_price,
       unit_cost,
       ROUND(100.0 * (unit_price - unit_cost) / unit_price, 1) AS margin_pct
FROM products
WHERE (unit_price - unit_cost) / unit_price < 0.30
ORDER BY margin_pct;

-- ---------------------------------------------------------------
-- 12.7 NULL: the value that isn't there
SELECT customer_name
FROM customers
WHERE city = NULL;
SELECT customer_name
FROM customers
WHERE city IS NULL;
SELECT customer_name, city
FROM customers
WHERE city <> 'Mumbai';
SELECT customer_name, city
FROM customers
WHERE city <> 'Mumbai' OR city IS NULL;
SELECT customer_name,
       COALESCE(city, 'Unknown') AS city
FROM customers
ORDER BY customer_id;

-- ---------------------------------------------------------------
-- 12.8 Transforming values: CASE, dates, and text
SELECT product_name,
       unit_price,
       CASE
           WHEN unit_price >= 1000 THEN 'Premium'
           WHEN unit_price >= 500  THEN 'Mid-range'
           ELSE 'Budget'
       END AS price_band
FROM products
ORDER BY unit_price;
SELECT order_id,
       order_date,
       EXTRACT(MONTH FROM order_date)        AS month_no,
       DATE_TRUNC('month', order_date)::date AS order_month
FROM orders
WHERE order_id <= 5004;
SELECT DATE '2026-03-31' - DATE '2026-02-05' AS days;
SELECT 0.1 + 0.2                                   AS exact_numeric,
       0.1::double precision + 0.2::double precision AS floating;
SELECT ROUND(2.5)                   AS exact_half,
       ROUND(3.5)                   AS exact_three_half,
       ROUND(2.5::double precision) AS float_half,
       ROUND(3.5::double precision) AS float_three_half;
SELECT invoice_id,
       due_date,
       CASE
           WHEN due_date >= DATE '2026-03-31'             THEN 'Not yet due'
           WHEN DATE '2026-03-31' - due_date <= 30         THEN 'Overdue 1-30 days'
           WHEN DATE '2026-03-31' - due_date <= 60         THEN 'Overdue 31-60 days'
           ELSE 'Overdue 60+ days'
       END AS due_status
FROM invoices
ORDER BY due_date;
SELECT customer_name,
       UPPER(city)                              AS city_upper,
       LENGTH(customer_name)                    AS name_length,
       SUBSTRING(customer_name FROM 1 FOR 3)    AS short_code,
       customer_name || ' (' || segment || ')'  AS label
FROM customers
ORDER BY customer_id
LIMIT 3;
SELECT customer_name,
       UPPER(city)                              AS city_upper,
       customer_name || ' (' || city || ')'     AS with_pipes,
       CONCAT(customer_name, ' (', city, ')')   AS with_concat
FROM customers
WHERE customer_id = 6;

-- ---------------------------------------------------------------
-- 12.9 Summarizing: aggregate functions, GROUP BY, and HAVING
SELECT SUM(amount)       AS invoiced,
       AVG(amount)       AS avg_invoice,
       MIN(invoice_date) AS first_invoice,
       MAX(invoice_date) AS last_invoice
FROM invoices;
SELECT COUNT(*)                    AS total_orders,
       COUNT(sales_rep_id)         AS orders_with_rep,
       COUNT(DISTINCT customer_id) AS unique_customers
FROM orders;
SELECT COUNT(*)    AS customers,
       COUNT(city) AS with_city
FROM customers;
SELECT order_id,
       quantity,
       unit_price,
       discount_pct,
       quantity * unit_price * (1 - discount_pct / 100) AS line_revenue
FROM order_items
WHERE order_id IN (5001, 5002);
SELECT ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 0) AS net_revenue_all_lines
FROM order_items;
SELECT status,
       COUNT(*) AS num_orders
FROM orders
GROUP BY status
ORDER BY num_orders DESC, status;
SELECT order_id,
       SUM(quantity * unit_price * (1 - discount_pct / 100)) AS order_revenue
FROM order_items
GROUP BY order_id
ORDER BY order_id
LIMIT 5;
SELECT order_id,
       ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS order_revenue
FROM order_items
GROUP BY order_id
ORDER BY order_id
LIMIT 5;
-- Fails on purpose in the book (ERROR:  column "orders.order_date" must appear in the GROUP BY clause):
-- SELECT customer_id, order_date, COUNT(*)
-- FROM orders
-- GROUP BY customer_id;
SELECT segment,
       COUNT(*)                                        AS customers,
       SUM(CASE WHEN city = 'Mumbai' THEN 1 ELSE 0 END) AS in_mumbai
FROM customers
GROUP BY segment
ORDER BY segment;
-- Fails on purpose in the book (ERROR:  column "num_orders" does not exist):
-- SELECT customer_id, COUNT(*) AS num_orders
-- FROM orders
-- WHERE num_orders > 1
-- GROUP BY customer_id;
SELECT customer_id, COUNT(*) AS num_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY customer_id;

-- ---------------------------------------------------------------
-- 12.10 JOIN: combining tables
SELECT o.order_id,
       c.customer_name,
       o.order_date
FROM orders AS o
INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
ORDER BY o.order_id
LIMIT 4;
SELECT c.customer_name,
       o.order_id
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id;
-- Customers who have never placed an order
SELECT c.customer_name
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
-- Products that have never been sold
SELECT p.product_name
FROM products AS p
LEFT JOIN order_items AS oi
       ON p.product_id = oi.product_id
WHERE oi.order_item_id IS NULL;
SELECT c.customer_name, p.product_name
FROM customers AS c
CROSS JOIN products AS p
ORDER BY c.customer_id, p.product_id
LIMIT 6;
SELECT COUNT(*) AS pairs
FROM customers AS c
CROSS JOIN products AS p;
SELECT e.employee_name,
       e.job_title,
       m.employee_name AS manager_name
FROM employees AS e
LEFT JOIN employees AS m
       ON e.manager_id = m.employee_id
ORDER BY e.employee_id;
SELECT COUNT(*) AS row_count
FROM orders AS o;
SELECT COUNT(*) AS row_count
FROM orders AS o
JOIN customers AS c ON o.customer_id = c.customer_id;
SELECT COUNT(*) AS row_count
FROM orders AS o
JOIN customers   AS c  ON o.customer_id = c.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id;
SELECT COUNT(*) AS row_count
FROM orders AS o
JOIN customers   AS c  ON o.customer_id = c.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
WHERE o.status <> 'Cancelled';
SELECT COALESCE(c.city, 'Unknown') AS city,
       COUNT(DISTINCT o.order_id)  AS orders,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS revenue
FROM orders AS o
JOIN customers   AS c  ON o.customer_id = c.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
WHERE o.status <> 'Cancelled'
GROUP BY COALESCE(c.city, 'Unknown')
ORDER BY revenue DESC;
SELECT o.order_id,
       c.customer_name,
       e.employee_name AS sales_rep,
       p.product_name,
       oi.quantity,
       ROUND(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100), 2) AS line_value
FROM orders AS o
JOIN      customers   AS c  ON o.customer_id  = c.customer_id
LEFT JOIN employees   AS e  ON o.sales_rep_id = e.employee_id
JOIN      order_items AS oi ON oi.order_id    = o.order_id
JOIN      products    AS p  ON p.product_id   = oi.product_id
WHERE o.order_id = 5001
ORDER BY p.product_id;
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
SELECT c.customer_name, COUNT(*) AS num_orders
FROM customers AS c
JOIN orders      AS o  ON c.customer_id = o.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
GROUP BY c.customer_name
ORDER BY c.customer_name;
SELECT c.customer_name, COUNT(*) AS num_orders
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY c.customer_name;
SELECT c.customer_name, COUNT(DISTINCT o.order_id) AS num_orders
FROM customers AS c
JOIN orders      AS o  ON c.customer_id = o.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
GROUP BY c.customer_name
ORDER BY c.customer_name;
SELECT SUM(i.amount)                   AS total_invoiced,
       SUM(p.amount)                   AS total_paid,
       SUM(i.amount) - SUM(p.amount)   AS outstanding
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id;
SELECT i.invoice_id, i.amount AS invoice_amount, p.payment_id, p.amount AS payment_amount
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE i.invoice_id IN (9001, 9002, 9007)
ORDER BY i.invoice_id, p.payment_id;
-- Version A: condition in ON
SELECT c.customer_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status = 'Pending'
ORDER BY c.customer_id;
-- Version B: condition in WHERE
SELECT c.customer_name, o.order_id, o.status
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
WHERE o.status = 'Pending'
ORDER BY c.customer_id;

-- ---------------------------------------------------------------
-- 12.12 Queries inside queries: subqueries and set operations
SELECT product_name, unit_price
FROM products
WHERE unit_price > (SELECT AVG(unit_price) FROM products)
ORDER BY unit_price;
SELECT customer_name
FROM customers
WHERE customer_id IN (
    SELECT o.customer_id
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE oi.product_id = 105
)
ORDER BY customer_name;
SELECT c.customer_name
FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
      AND o.status = 'Shipped'
)
ORDER BY c.customer_name;
SELECT p.invoice_id, p.payment_date, p.amount
FROM payments AS p
WHERE p.payment_date = (
    SELECT MAX(p2.payment_date)
    FROM payments AS p2
    WHERE p2.invoice_id = p.invoice_id
)
ORDER BY p.invoice_id;
SELECT employee_name
FROM employees
WHERE employee_id NOT IN (SELECT manager_id FROM employees);
SELECT e.employee_name
FROM employees AS e
WHERE NOT EXISTS (
    SELECT 1
    FROM employees AS m
    WHERE m.manager_id = e.employee_id
)
ORDER BY e.employee_id;
SELECT employee_name
FROM employees
WHERE employee_id NOT IN (SELECT manager_id
                          FROM employees
                          WHERE manager_id IS NOT NULL)
ORDER BY employee_id;
SELECT SUM(i.amount)                        AS total_invoiced,
       SUM(COALESCE(p.paid, 0))             AS total_paid,
       SUM(i.amount - COALESCE(p.paid, 0))  AS outstanding
FROM invoices AS i
LEFT JOIN (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
) AS p ON i.invoice_id = p.invoice_id;
SELECT ROUND(AVG(order_revenue), 2) AS avg_order_value
FROM (
    SELECT o.order_id,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_id
) AS per_order;
SELECT s.segment, p.category
FROM (SELECT DISTINCT segment  FROM customers) AS s
CROSS JOIN
     (SELECT DISTINCT category FROM products)  AS p
ORDER BY s.segment, p.category
LIMIT 5;
SELECT city FROM customers WHERE segment = 'Retail'
UNION
SELECT city FROM customers WHERE segment = 'Hospitality'
ORDER BY city;
SELECT city FROM customers WHERE segment = 'Retail'
UNION ALL
SELECT city FROM customers WHERE segment = 'Hospitality'
ORDER BY city;
SELECT c.customer_name
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE '2026-02-01'
  AND o.order_date <  DATE '2026-03-01'
EXCEPT
SELECT c.customer_name
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE '2026-03-01'
  AND o.order_date <  DATE '2026-04-01'
  AND o.status <> 'Cancelled'
ORDER BY customer_name;

-- ---------------------------------------------------------------
-- 12.14 Writing SQL that humans can read
select c.city,count(distinct o.order_id),sum(oi.quantity*oi.unit_price*(1-oi.discount_pct/100)) from orders o join customers c on o.customer_id=c.customer_id join order_items oi on o.order_id=oi.order_id where o.status<>'Cancelled' group by c.city order by 3 desc;

-- ---------------------------------------------------------------
-- 12.15 Putting it all together: Tuesday morning with the sales head
SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                     AS last_order_date,
       DATE '2026-03-31' - MAX(o.order_date) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2026-03-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date NULLS FIRST;
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price), 0)                           AS gross_value,
       ROUND(SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100), 0)   AS discount_given,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * oi.discount_pct / 100)
             / SUM(oi.quantity * oi.unit_price), 1)                         AS discount_pct_of_gross
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY discount_given DESC;
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
SELECT c.customer_name,
       SUM(inv.balance) AS total_due,
       SUM(CASE WHEN inv.due_date >= DATE '2026-03-31' THEN inv.balance ELSE 0.00 END) AS not_yet_due,
       SUM(CASE WHEN inv.due_date <  DATE '2026-03-31'
                 AND DATE '2026-03-31' - inv.due_date <= 30 THEN inv.balance ELSE 0.00 END) AS overdue_1_30,
       SUM(CASE WHEN DATE '2026-03-31' - inv.due_date BETWEEN 31 AND 60 THEN inv.balance ELSE 0.00 END) AS overdue_31_60,
       SUM(CASE WHEN DATE '2026-03-31' - inv.due_date > 60 THEN inv.balance ELSE 0.00 END) AS overdue_60_plus
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
GROUP BY c.customer_id, c.customer_name
ORDER BY total_due DESC;
SELECT e.employee_name                         AS sales_rep,
       COALESCE(m.employee_name, '(none)')     AS reports_to,
       COUNT(DISTINCT o.order_id)              AS orders,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM employees AS e
LEFT JOIN employees   AS m  ON e.manager_id   = m.employee_id
JOIN      orders      AS o  ON o.sales_rep_id = e.employee_id
JOIN      order_items AS oi ON oi.order_id    = o.order_id
WHERE o.status <> 'Cancelled'
GROUP BY e.employee_id, e.employee_name, m.employee_name
ORDER BY net_revenue DESC;
SELECT DATE_TRUNC('month', invoice_date)::date AS month,
       COUNT(*)                                AS invoices,
       SUM(amount)                             AS billed,
       ROUND(AVG(amount), 0)                   AS avg_invoice
FROM invoices
WHERE invoice_date >= DATE '2026-02-01'
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY month;
SELECT c.customer_name
FROM customers AS c
JOIN orders   AS o ON c.customer_id = o.customer_id
JOIN invoices AS i ON i.order_id    = o.order_id
WHERE i.invoice_date >= DATE '2026-02-01'
  AND i.invoice_date <  DATE '2026-03-01'
EXCEPT
SELECT c.customer_name
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE '2026-03-01'
  AND o.order_date <  DATE '2026-04-01'
  AND o.status <> 'Cancelled'
ORDER BY customer_name;
SELECT c.customer_name
FROM customers AS c
JOIN orders   AS o ON c.customer_id = o.customer_id
JOIN invoices AS i ON i.order_id    = o.order_id
WHERE i.invoice_date >= DATE '2026-02-01'
  AND i.invoice_date <  DATE '2026-03-01'
EXCEPT
SELECT c.customer_name
FROM customers AS c
JOIN orders   AS o ON c.customer_id = o.customer_id
JOIN invoices AS i ON i.order_id    = o.order_id
WHERE i.invoice_date >= DATE '2026-03-01'
  AND i.invoice_date <  DATE '2026-04-01'
ORDER BY customer_name;
SELECT o.order_id,
       o.order_date,
       o.status,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS order_revenue
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
LEFT JOIN invoices AS i ON i.order_id = o.order_id
WHERE i.invoice_id IS NULL
  AND o.status <> 'Cancelled'
GROUP BY o.order_id, o.order_date, o.status;
SELECT SUM(i.amount)                                                   AS billed,
       SUM(CASE WHEN c.segment = 'Wholesale' THEN i.amount ELSE 0 END) AS wholesale,
       ROUND(100.0 * SUM(CASE WHEN c.segment = 'Wholesale' THEN i.amount ELSE 0 END)
             / SUM(i.amount), 1)                                       AS wholesale_pct
FROM invoices AS i
JOIN orders    AS o ON o.order_id    = i.order_id
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE i.invoice_date >= DATE '2026-02-01'
  AND i.invoice_date <  DATE '2026-03-01';
SELECT c.customer_name,
       EXISTS (SELECT 1
               FROM orders AS m
               WHERE m.customer_id = c.customer_id
                 AND m.order_date >= DATE '2026-03-01'
                 AND m.status <> 'Cancelled')           AS ordered_in_march,
       COALESCE(SUM(inv.balance), 0.00)                 AS owed,
       SUM(CASE WHEN inv.due_date < DATE '2026-03-31'
                THEN inv.balance ELSE 0.00 END)          AS overdue
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
LEFT JOIN (
    SELECT i.order_id, i.due_date,
           i.amount - COALESCE(pay.paid, 0) AS balance
    FROM invoices AS i
    LEFT JOIN (SELECT invoice_id, SUM(amount) AS paid
               FROM payments
               GROUP BY invoice_id) AS pay
           ON i.invoice_id = pay.invoice_id
) AS inv ON inv.order_id = o.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY overdue DESC, owed DESC, c.customer_name;

-- ---------------------------------------------------------------
-- 12.16 The same SQL in MySQL
SELECT COUNT(*) AS delivered_orders
FROM orders
WHERE status = 'delivered';
SELECT o.order_id, o.status, i.invoice_id
FROM orders AS o
FULL OUTER JOIN invoices AS i ON o.order_id = i.order_id
WHERE o.order_id IS NULL OR i.invoice_id IS NULL
ORDER BY o.order_id;

-- ---------------------------------------------------------------
-- In the real world: Riverstone's monthly sales report
-- Monthly sales summary
-- Revenue counts Delivered and Shipped orders (finance policy);
-- Pending and Cancelled orders are excluded.
SELECT DATE_TRUNC('month', o.order_date)::date AS month,
       COUNT(DISTINCT o.order_id)             AS orders,
       COUNT(DISTINCT o.customer_id)          AS active_customers,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi
  ON o.order_id = oi.order_id
WHERE o.status IN ('Delivered', 'Shipped')
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;

-- ---------------------------------------------------------------
-- Answers
SELECT product_name, unit_price
FROM products
WHERE category = 'Kitchen'
ORDER BY unit_price ASC;
SELECT segment, COUNT(*) AS num_customers
FROM customers
GROUP BY segment
ORDER BY num_customers DESC, segment;
SELECT order_id, customer_id, order_date
FROM orders
WHERE order_date >= '2026-03-01'
  AND order_date <  '2026-04-01'
ORDER BY order_date;
SELECT customer_name
FROM customers
WHERE customer_name LIKE '%Foods%'
   OR customer_name LIKE '%Mart%';
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
SELECT COALESCE(e.employee_name, 'Unassigned') AS sales_rep,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
LEFT JOIN employees AS e ON o.sales_rep_id = e.employee_id
WHERE o.status <> 'Cancelled'
GROUP BY COALESCE(e.employee_name, 'Unassigned')
ORDER BY net_revenue DESC;
SELECT c.customer_name
FROM customers AS c
WHERE EXISTS (SELECT 1 FROM orders AS o
              WHERE o.customer_id = c.customer_id)
  AND NOT EXISTS (SELECT 1 FROM orders AS o
                  WHERE o.customer_id = c.customer_id
                    AND o.status = 'Delivered');
SELECT ROUND(AVG(order_revenue), 2) AS avg_order_value
FROM (
    SELECT o.order_id,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_id
) AS per_order;
SELECT method, COUNT(*) AS payments, SUM(amount) AS amount_received
FROM payments
GROUP BY method
ORDER BY amount_received DESC;
SELECT i.invoice_id, i.amount, i.due_date
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE p.payment_id IS NULL
ORDER BY i.due_date;
SELECT c.customer_name,
       MIN(o.order_date)                     AS first_order,
       MAX(o.order_date)                     AS latest_order,
       MAX(o.order_date) - MIN(o.order_date) AS days_between
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
WHERE o.status <> 'Cancelled'
GROUP BY c.customer_name
ORDER BY days_between DESC, c.customer_name;
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
SELECT order_id,
       order_date,
       status,
       DATE '2026-03-31' - order_date AS days_open
FROM orders
WHERE (status = 'Pending' AND DATE '2026-03-31' - order_date > 7)
   OR (status = 'Shipped' AND DATE '2026-03-31' - order_date > 14)
ORDER BY days_open DESC;
\c riverstone_2025
SELECT c.customer_name,
       c.segment,
       MAX(o.order_date)                     AS last_order_date,
       DATE '2025-12-31' - MAX(o.order_date) AS days_since_last_order
FROM customers AS c
LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id
      AND o.status <> 'Cancelled'
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING MAX(o.order_date) < DATE '2025-11-01'
    OR MAX(o.order_date) IS NULL
ORDER BY last_order_date NULLS FIRST;
SELECT ROUND(4.5)                   AS exact_numeric,
       ROUND(4.5::double precision) AS floating;
\c riverstone_2025
SELECT segment,
       ROUND(SUM(CASE WHEN qtr = 1 THEN line_revenue ELSE 0 END), 2) AS q1,
       ROUND(SUM(CASE WHEN qtr = 2 THEN line_revenue ELSE 0 END), 2) AS q2,
       ROUND(SUM(CASE WHEN qtr = 3 THEN line_revenue ELSE 0 END), 2) AS q3,
       ROUND(SUM(CASE WHEN qtr = 4 THEN line_revenue ELSE 0 END), 2) AS q4,
       ROUND(SUM(line_revenue), 2)                                  AS grand_total
FROM (
    SELECT c.segment,
           EXTRACT(QUARTER FROM o.order_date)                  AS qtr,
           oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS line_revenue
    FROM order_items AS oi
    JOIN orders    AS o ON oi.order_id   = o.order_id
    JOIN customers AS c ON o.customer_id = c.customer_id
    WHERE o.status <> 'Cancelled'
) AS sales_lines
GROUP BY segment
ORDER BY segment;
