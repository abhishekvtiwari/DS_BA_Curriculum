-- Analyst to Architect · Chapter 28 · Advanced SQL, Performance & Data Modeling
-- File: ch28_queries_mysql.sql (MySQL)
-- What: the chapter's queries translated to MySQL, in chapter order. Statements that fail on purpose are
--       commented out with the error they produce. Timing experiments on riverstone_perf are in ch28_perf.py.
-- How:  load riverstone_2025_setup_mysql.sql and ch28_2025_addons_mysql.sql first, then:
--       mysql -uroot -t < ch28_queries_mysql.sql
--       (creates the databases dw and riverstone_lab; drops them first if they exist)
-- Tested on: MySQL 8.0.46 (Ubuntu 24.04); results compared with PostgreSQL 16.
-- Riverstone Supplies is fictional; every name and number is invented.

USE riverstone_2025;

-- ============ 28.2 Recursive CTEs ============
-- counting to five
WITH RECURSIVE numbers AS (
    SELECT 1 AS n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 5
)
SELECT n FROM numbers;

-- without the stop rule MySQL aborts after 1,000 passes:
-- ERROR 3636 (HY000): Recursive query aborted after 1001 iterations. Try increasing @@cte_max_recursion_depth to a larger value.

-- a list of months (MySQL keeps DATE + INTERVAL as a DATE, so no CAST is needed)
WITH RECURSIVE months AS (
    SELECT DATE '2025-01-01' AS month
    UNION ALL
    SELECT month + INTERVAL 1 MONTH FROM months WHERE month < DATE '2025-12-01'
)
SELECT COUNT(*) AS months, MIN(month) AS first_month, MAX(month) AS last_month FROM months;

-- org chart with levels
WITH RECURSIVE org AS (
    SELECT staff_id, staff_name, job_title, manager_id, 1 AS level
    FROM staff WHERE manager_id IS NULL
    UNION ALL
    SELECT s.staff_id, s.staff_name, s.job_title, s.manager_id, o.level + 1
    FROM staff AS s JOIN org AS o ON s.manager_id = o.staff_id
)
SELECT level, staff_name, job_title FROM org ORDER BY level, staff_id;

-- walking up
WITH RECURSIVE chain AS (
    SELECT staff_id, staff_name, manager_id, 0 AS steps_up FROM staff WHERE staff_name = 'Gopal Sahu'
    UNION ALL
    SELECT m.staff_id, m.staff_name, m.manager_id, c.steps_up + 1
    FROM staff AS m JOIN chain AS c ON m.staff_id = c.manager_id
)
SELECT steps_up, staff_name FROM chain ORDER BY steps_up;

-- people below each manager
WITH RECURSIVE under_mgr AS (
    SELECT staff_id AS manager_id, staff_id AS member_id FROM staff
    UNION ALL
    SELECT u.manager_id, s.staff_id FROM under_mgr AS u JOIN staff AS s ON s.manager_id = u.member_id
)
SELECT m.staff_name, m.job_title, COUNT(*) - 1 AS people_below
FROM under_mgr AS u JOIN staff AS m ON m.staff_id = u.manager_id
GROUP BY m.staff_id, m.staff_name, m.job_title
HAVING COUNT(*) > 1
ORDER BY people_below DESC, m.staff_id;

-- Anita Rao's team revenue (MySQL has no NULLS LAST: sort the NULL test first)
WITH RECURSIVE sales_team AS (
    SELECT staff_id, staff_name, employee_id FROM staff WHERE staff_name = 'Anita Rao'
    UNION ALL
    SELECT s.staff_id, s.staff_name, s.employee_id FROM staff AS s JOIN sales_team AS t ON s.manager_id = t.staff_id
)
SELECT t.staff_name, COUNT(DISTINCT sl.order_id) AS orders, ROUND(SUM(sl.net_revenue)) AS net_revenue
FROM sales_team AS t LEFT JOIN sales_lines AS sl ON sl.sales_rep_id = t.employee_id
WHERE t.employee_id IS NOT NULL      -- the ERP knows only the key accounts team
GROUP BY t.staff_name
ORDER BY SUM(sl.net_revenue) IS NULL, net_revenue DESC, t.staff_name;

-- BOM explosion of the Garden Chair (CAST in both parts fixes the column type)
WITH RECURSIVE explode AS (
    SELECT b.parent_part_id AS product_id, b.child_part_id,
           CAST(b.quantity AS DECIMAL(12,3)) AS qty_per_product, 1 AS depth
    FROM bom_lines AS b WHERE b.parent_part_id = 106
    UNION ALL
    SELECT e.product_id, b.child_part_id, CAST(e.qty_per_product * b.quantity AS DECIMAL(12,3)), e.depth + 1
    FROM explode AS e JOIN bom_lines AS b ON b.parent_part_id = e.child_part_id
)
SELECT e.depth, p.part_name, p.part_type, e.qty_per_product AS qty_per_chair, p.unit
FROM explode AS e JOIN parts AS p ON p.part_id = e.child_part_id
ORDER BY e.depth, p.part_id;

-- material cost roll-up
WITH RECURSIVE explode AS (
    SELECT b.parent_part_id AS product_id, b.child_part_id, CAST(b.quantity AS DECIMAL(12,3)) AS qty_per_product
    FROM bom_lines AS b
    WHERE b.parent_part_id IN (SELECT part_id FROM parts WHERE part_type = 'Product')
    UNION ALL
    SELECT e.product_id, b.child_part_id, CAST(e.qty_per_product * b.quantity AS DECIMAL(12,3))
    FROM explode AS e JOIN bom_lines AS b ON b.parent_part_id = e.child_part_id
)
SELECT p.part_id AS product_id, p.part_name AS product_name,
       CAST(SUM(e.qty_per_product * m.material_cost) AS DECIMAL(10,2)) AS material_cost,
       pr.unit_cost AS standard_cost
FROM explode AS e
JOIN parts AS m ON m.part_id = e.child_part_id AND m.part_type = 'Material'
JOIN parts AS p ON p.part_id = e.product_id
JOIN products AS pr ON pr.product_id = p.part_id
GROUP BY p.part_id, p.part_name, pr.unit_cost
ORDER BY p.part_id;

-- where-used for steel tube
WITH RECURSIVE uses AS (
    SELECT b.parent_part_id, CAST(b.quantity AS DECIMAL(12,3)) AS qty FROM bom_lines AS b WHERE b.child_part_id = 305
    UNION ALL
    SELECT b.parent_part_id, CAST(u.qty * b.quantity AS DECIMAL(12,3)) FROM uses AS u JOIN bom_lines AS b ON b.child_part_id = u.parent_part_id
)
SELECT p.part_name, SUM(u.qty) AS kg_steel_tube_per_unit
FROM uses AS u JOIN parts AS p ON p.part_id = u.parent_part_id
WHERE p.part_type = 'Product' GROUP BY p.part_name;

-- loop protection without CYCLE: carry a path and stop when an id repeats
WITH RECURSIVE bad_staff (staff_id, manager_id) AS (
    SELECT 1, 3 UNION ALL SELECT 2, 1 UNION ALL SELECT 3, 2
),
chain AS (
    SELECT staff_id, manager_id, CAST(CONCAT(',', staff_id, ',') AS CHAR(200)) AS visited
    FROM bad_staff WHERE staff_id = 1
    UNION ALL
    SELECT b.staff_id, b.manager_id, CONCAT(c.visited, b.staff_id, ',')
    FROM bad_staff AS b JOIN chain AS c ON b.staff_id = c.manager_id
    WHERE LOCATE(CONCAT(',', b.staff_id, ','), c.visited) = 0
)
SELECT * FROM chain;

-- indented org chart without SEARCH
WITH RECURSIVE org AS (
    SELECT staff_id, staff_name, 1 AS level, CAST(LPAD(staff_id, 4, '0') AS CHAR(200)) AS sort_path
    FROM staff WHERE manager_id IS NULL
    UNION ALL
    SELECT s.staff_id, s.staff_name, o.level + 1, CONCAT(o.sort_path, '/', LPAD(s.staff_id, 4, '0'))
    FROM staff AS s JOIN org AS o ON s.manager_id = o.staff_id
)
SELECT CONCAT(REPEAT('    ', level - 1), staff_name) AS org_chart FROM org ORDER BY sort_path;

-- ============ 28.3 Window frames ============
-- GROUPS frames are not supported:
-- ERROR 1235 (42000): This version of MySQL doesn't yet support 'GROUPS'
SELECT o.order_date, o.order_id,
       COUNT(*) OVER w_rows  AS rows_in_frame,
       COUNT(*) OVER w_range AS rows_in_2_days
FROM orders AS o
WHERE o.order_date BETWEEN '2025-02-14' AND '2025-02-21'
WINDOW w_rows  AS (ORDER BY o.order_date ROWS BETWEEN 1 PRECEDING AND CURRENT ROW),
       w_range AS (ORDER BY o.order_date RANGE BETWEEN INTERVAL 1 DAY PRECEDING AND CURRENT ROW)
ORDER BY o.order_date, o.order_id;

WITH daily AS (
    SELECT order_date, SUM(net_revenue) AS revenue FROM sales_lines
    WHERE order_date BETWEEN '2025-11-20' AND '2025-12-10' GROUP BY order_date
)
SELECT order_date, ROUND(revenue) AS revenue,
       ROUND(SUM(revenue) OVER (ORDER BY order_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS last_3_rows,
       ROUND(SUM(revenue) OVER (ORDER BY order_date RANGE BETWEEN INTERVAL 6 DAY PRECEDING AND CURRENT ROW)) AS last_7_days
FROM daily ORDER BY order_date;

-- EXCLUDE CURRENT ROW is not supported: subtract the current row instead
WITH monthly AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month, SUM(net_revenue) AS revenue
    FROM sales_lines GROUP BY 1
)
SELECT month, ROUND(revenue) AS revenue,
       ROUND((SUM(revenue) OVER q - revenue) / (COUNT(*) OVER q - 1)) AS avg_other_months_in_quarter
FROM monthly
WINDOW q AS (PARTITION BY YEAR(month), QUARTER(month))
ORDER BY month;

WITH order_values AS (
    SELECT o.customer_id, o.order_id, o.order_date, SUM(sl.net_revenue) AS order_value
    FROM orders AS o JOIN sales_lines AS sl ON sl.order_id = o.order_id
    WHERE o.customer_id = 2 GROUP BY o.customer_id, o.order_id, o.order_date
)
SELECT order_date, ROUND(order_value) AS order_value,
       ROUND(FIRST_VALUE(order_value) OVER w) AS first_order,
       ROUND(LAST_VALUE(order_value) OVER w) AS last_value_default,
       ROUND(LAST_VALUE(order_value) OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)) AS latest_order
FROM order_values
WINDOW w AS (PARTITION BY customer_id ORDER BY order_date, order_id)
ORDER BY order_date;

-- median without PERCENTILE_CONT
WITH order_values AS (SELECT order_id, SUM(net_revenue) AS order_value FROM sales_lines GROUP BY order_id),
ranked AS (SELECT order_value, ROW_NUMBER() OVER (ORDER BY order_value) AS rn, COUNT(*) OVER () AS n FROM order_values)
SELECT MAX(n) AS orders, ROUND(AVG(order_value)) AS median_value
FROM ranked WHERE rn IN (FLOOR((n + 1) / 2), CEIL((n + 1) / 2));

WITH order_values AS (SELECT order_id, SUM(net_revenue) AS order_value FROM sales_lines GROUP BY order_id),
banded AS (SELECT order_value, NTILE(4) OVER (ORDER BY order_value) AS quartile FROM order_values)
SELECT quartile, COUNT(*) AS orders, ROUND(MIN(order_value)) AS smallest, ROUND(MAX(order_value)) AS largest,
       ROUND(SUM(order_value)) AS revenue
FROM banded GROUP BY quartile ORDER BY quartile;

-- ============ 28.8 Grain ============
SELECT order_id, product_id, COUNT(*) AS copies FROM order_items GROUP BY order_id, product_id HAVING COUNT(*) > 1;

SELECT ROUND(SUM(t.target_revenue)) AS target_summed_after_join
FROM sales_lines AS sl
JOIN sales_targets AS t ON t.target_month = CAST(DATE_FORMAT(sl.order_date, '%Y-%m-01') AS DATE)
WHERE sl.order_date < '2025-02-01';

WITH monthly_sales AS (
    SELECT CAST(DATE_FORMAT(order_date, '%Y-%m-01') AS DATE) AS month, SUM(net_revenue) AS revenue
    FROM sales_lines GROUP BY 1
)
SELECT m.month, ROUND(m.revenue) AS revenue, ROUND(t.target_revenue) AS target,
       ROUND(100 * m.revenue / t.target_revenue, 1) AS pct_of_target
FROM monthly_sales AS m JOIN sales_targets AS t ON t.target_month = m.month
WHERE m.month < '2025-04-01' ORDER BY m.month;

-- ============ 28.9 Star schema (MySQL: a schema is a database, so dw is a database) ============
DROP DATABASE IF EXISTS dw;
CREATE DATABASE dw;

CREATE TABLE dw.dim_date (
    date_key INT PRIMARY KEY, full_date DATE NOT NULL UNIQUE, day_name VARCHAR(9) NOT NULL,
    month_start DATE NOT NULL, month_name VARCHAR(9) NOT NULL, quarter_label CHAR(7) NOT NULL, is_weekend BOOLEAN NOT NULL
);
INSERT INTO dw.dim_date
WITH RECURSIVE days AS (
    SELECT DATE '2025-01-01' AS d UNION ALL SELECT d + INTERVAL 1 DAY FROM days WHERE d < '2025-12-31'
)
SELECT CAST(DATE_FORMAT(d, '%Y%m%d') AS UNSIGNED), d, DAYNAME(d), CAST(DATE_FORMAT(d, '%Y-%m-01') AS DATE),
       MONTHNAME(d), CONCAT(YEAR(d), '-Q', QUARTER(d)), DAYOFWEEK(d) IN (1, 7)
FROM days;

CREATE TABLE dw.dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY, product_id INT NOT NULL UNIQUE,
    product_name VARCHAR(100) NOT NULL, category VARCHAR(30) NOT NULL
);
INSERT INTO dw.dim_product (product_id, product_name, category)
SELECT product_id, product_name, category FROM products ORDER BY product_id;

CREATE TABLE dw.dim_sales_rep (
    sales_rep_key INT AUTO_INCREMENT PRIMARY KEY, employee_id INT UNIQUE,
    rep_name VARCHAR(100) NOT NULL, job_title VARCHAR(50) NOT NULL
);
INSERT INTO dw.dim_sales_rep (employee_id, rep_name, job_title) VALUES (NULL, 'No rep recorded', 'Unknown');
INSERT INTO dw.dim_sales_rep (employee_id, rep_name, job_title)
SELECT employee_id, employee_name, job_title FROM employees ORDER BY employee_id;

CREATE TABLE dw.dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY, customer_id INT NOT NULL, customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50), segment VARCHAR(30) NOT NULL, valid_from DATE NOT NULL, valid_to DATE NOT NULL, is_current BOOLEAN NOT NULL
);
INSERT INTO dw.dim_customer (customer_id, customer_name, city, segment, valid_from, valid_to, is_current)
WITH version_starts AS (
    SELECT customer_id, signup_date AS valid_from FROM customers
    UNION
    SELECT customer_id, changed_on FROM customer_changes
),
versions AS (
    SELECT customer_id, valid_from,
           COALESCE(LEAD(valid_from) OVER (PARTITION BY customer_id ORDER BY valid_from), DATE '9999-12-31') AS valid_to
    FROM version_starts
)
SELECT v.customer_id, c.customer_name,
       COALESCE((SELECT ch.new_value FROM customer_changes AS ch WHERE ch.customer_id = v.customer_id AND ch.column_name = 'city'
                 AND ch.changed_on <= v.valid_from ORDER BY ch.changed_on DESC LIMIT 1),
                (SELECT ch.old_value FROM customer_changes AS ch WHERE ch.customer_id = v.customer_id AND ch.column_name = 'city'
                 ORDER BY ch.changed_on LIMIT 1), c.city),
       COALESCE((SELECT ch.new_value FROM customer_changes AS ch WHERE ch.customer_id = v.customer_id AND ch.column_name = 'segment'
                 AND ch.changed_on <= v.valid_from ORDER BY ch.changed_on DESC LIMIT 1),
                (SELECT ch.old_value FROM customer_changes AS ch WHERE ch.customer_id = v.customer_id AND ch.column_name = 'segment'
                 ORDER BY ch.changed_on LIMIT 1), c.segment),
       v.valid_from, v.valid_to, v.valid_to = DATE '9999-12-31'
FROM versions AS v JOIN customers AS c ON c.customer_id = v.customer_id
ORDER BY v.customer_id, v.valid_from;

CREATE TABLE dw.fact_sales_line (
    order_item_id INT PRIMARY KEY, order_id INT NOT NULL,
    date_key INT NOT NULL, customer_key INT NOT NULL, product_key INT NOT NULL, sales_rep_key INT NOT NULL,
    quantity INT NOT NULL, net_revenue DECIMAL(12,2) NOT NULL, product_cost DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (date_key) REFERENCES dw.dim_date (date_key),
    FOREIGN KEY (customer_key) REFERENCES dw.dim_customer (customer_key),
    FOREIGN KEY (product_key) REFERENCES dw.dim_product (product_key),
    FOREIGN KEY (sales_rep_key) REFERENCES dw.dim_sales_rep (sales_rep_key)
);
-- <=> is MySQL's null-safe equals (PostgreSQL: IS NOT DISTINCT FROM)
INSERT INTO dw.fact_sales_line
SELECT oi.order_item_id, o.order_id, CAST(DATE_FORMAT(o.order_date, '%Y%m%d') AS UNSIGNED),
       dc.customer_key, dp.product_key, dr.sales_rep_key, oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100), oi.quantity * p.unit_cost
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
JOIN dw.dim_customer AS dc ON dc.customer_id = o.customer_id AND o.order_date >= dc.valid_from AND o.order_date < dc.valid_to
JOIN dw.dim_product AS dp ON dp.product_id = oi.product_id
JOIN dw.dim_sales_rep AS dr ON dr.employee_id <=> o.sales_rep_id
WHERE o.status <> 'Cancelled';

SELECT (SELECT ROUND(SUM(net_revenue)) FROM sales_lines) AS view_total,
       (SELECT ROUND(SUM(net_revenue)) FROM dw.fact_sales_line) AS fact_total,
       (SELECT COUNT(*) FROM dw.dim_customer) AS customer_rows,
       (SELECT COUNT(*) FROM dw.fact_sales_line) AS fact_lines;

SELECT d.quarter_label, c.segment, ROUND(SUM(f.net_revenue)) AS net_revenue
FROM dw.fact_sales_line AS f
JOIN dw.dim_date AS d ON d.date_key = f.date_key
JOIN dw.dim_customer AS c ON c.customer_key = f.customer_key
GROUP BY d.quarter_label, c.segment ORDER BY d.quarter_label, c.segment;

WITH as_it_was AS (
    SELECT c.segment, SUM(f.net_revenue) AS revenue
    FROM dw.fact_sales_line AS f JOIN dw.dim_customer AS c ON c.customer_key = f.customer_key GROUP BY c.segment
),
as_it_is AS (
    SELECT cur.segment, SUM(f.net_revenue) AS revenue
    FROM dw.fact_sales_line AS f
    JOIN dw.dim_customer AS c ON c.customer_key = f.customer_key
    JOIN dw.dim_customer AS cur ON cur.customer_id = c.customer_id AND cur.is_current
    GROUP BY cur.segment
)
SELECT w.segment, ROUND(w.revenue) AS revenue_as_it_was, ROUND(i.revenue) AS revenue_as_it_is,
       ROUND(i.revenue - w.revenue) AS difference
FROM as_it_was AS w JOIN as_it_is AS i ON i.segment = w.segment ORDER BY w.segment;

-- ============ 28.7, 28.10, 28.12 Lab ============
DROP DATABASE IF EXISTS riverstone_lab;
CREATE DATABASE riverstone_lab;
USE riverstone_lab;

CREATE TABLE order_lines_1nf (
    order_id INT, order_date DATE, customer VARCHAR(100), city VARCHAR(50), sales_rep VARCHAR(100),
    product_id INT, product_name VARCHAR(100), quantity INT, unit_price DECIMAL(10,2), discount_pct DECIMAL(5,2),
    PRIMARY KEY (order_id, product_id)
);
INSERT INTO order_lines_1nf VALUES
(10001, '2025-01-02', 'Patel Kitchenware', 'Ahmedabad', 'Neha Kulkarni', 108, 'Stackable Bin',   10, 290, 0),
(10002, '2025-01-05', 'Green Leaf Hotels', 'Pune',      'Farah Khan',    107, 'Lunch Box Set',   55, 380, 0),
(10005, '2025-01-20', 'Green Leaf Hotels', 'Pune',      'Farah Khan',    101, 'Storage Box 10L', 15, 430, 5),
(10006, '2025-01-21', 'Coastal Foods',     'Chennai',   'Rahul Mehta',   102, 'Storage Box 25L', 25, 750, 5),
(10007, '2025-01-24', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 101, 'Storage Box 10L', 45, 430, 0),
(10007, '2025-01-24', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 102, 'Storage Box 25L', 20, 750, 0),
(10007, '2025-01-24', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 108, 'Stackable Bin',   20, 290, 0),
(10008, '2025-01-26', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 101, 'Storage Box 10L', 30, 430, 0),
(10008, '2025-01-26', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 102, 'Storage Box 25L', 25, 750, 0),
(10008, '2025-01-26', 'Sharma Hardware',   'Mumbai',    'Neha Kulkarni', 107, 'Lunch Box Set',   25, 380, 0);

CREATE TABLE orders_2nf AS SELECT DISTINCT order_id, order_date, customer, city, sales_rep FROM order_lines_1nf;
CREATE TABLE products_2nf AS SELECT DISTINCT product_id, product_name FROM order_lines_1nf;
CREATE TABLE order_lines_2nf AS SELECT order_id, product_id, quantity, unit_price, discount_pct FROM order_lines_1nf;
CREATE TABLE customers_3nf (customer_id INT PRIMARY KEY, customer VARCHAR(100) NOT NULL UNIQUE, city VARCHAR(50));
INSERT INTO customers_3nf
SELECT ROW_NUMBER() OVER (ORDER BY customer), customer, city FROM (SELECT DISTINCT customer, city FROM orders_2nf) AS c;
CREATE TABLE orders_3nf AS
SELECT o.order_id, o.order_date, c.customer_id, o.sales_rep FROM orders_2nf AS o JOIN customers_3nf AS c ON c.customer = o.customer;

SELECT 'flat 1NF table' AS source, ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS net_revenue FROM order_lines_1nf
UNION ALL
SELECT '3NF tables joined', ROUND(SUM(l.quantity * l.unit_price * (1 - l.discount_pct / 100)), 2)
FROM order_lines_2nf AS l JOIN orders_3nf AS o ON o.order_id = l.order_id
JOIN customers_3nf AS c ON c.customer_id = o.customer_id JOIN products_2nf AS p ON p.product_id = l.product_id;

-- SCD type 1 with INSERT ... ON DUPLICATE KEY UPDATE (MySQL has no MERGE)
CREATE TABLE dim_customer_t1 (customer_id INT PRIMARY KEY, customer VARCHAR(100) NOT NULL, city VARCHAR(50), segment VARCHAR(30));
INSERT INTO dim_customer_t1 VALUES (1, 'Sharma Hardware', 'Mumbai', 'Retail'), (3, 'Green Leaf Hotels', 'Pune', 'Hospitality');
CREATE TABLE customer_extract (customer_id INT PRIMARY KEY, customer VARCHAR(100) NOT NULL, city VARCHAR(50), segment VARCHAR(30));
INSERT INTO customer_extract VALUES (1, 'Sharma Hardware', 'Thane', 'Retail'), (3, 'Green Leaf Hotels', 'Pune', 'Hospitality'),
                                    (4, 'Coastal Foods', 'Chennai', 'Wholesale');
INSERT INTO dim_customer_t1 (customer_id, customer, city, segment)
SELECT customer_id, customer, city, segment FROM customer_extract AS x
ON DUPLICATE KEY UPDATE city = x.city, segment = x.segment;
SELECT * FROM dim_customer_t1 ORDER BY customer_id;

-- SCD type 2 (MySQL has no partial unique index; enforce one current row in the load instead)
CREATE TABLE dim_customer_t2 (
    customer_key INT AUTO_INCREMENT PRIMARY KEY, customer_id INT NOT NULL, customer VARCHAR(100) NOT NULL,
    city VARCHAR(50), segment VARCHAR(30), valid_from DATE NOT NULL, valid_to DATE NOT NULL DEFAULT '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE
);
INSERT INTO dim_customer_t2 (customer_id, customer, city, segment, valid_from) VALUES
(1, 'Sharma Hardware', 'Mumbai', 'Retail', '2024-11-04'), (3, 'Green Leaf Hotels', 'Pune', 'Hospitality', '2024-09-08');
START TRANSACTION;
UPDATE dim_customer_t2 AS d JOIN customer_extract AS x ON d.customer_id = x.customer_id
SET d.valid_to = '2026-04-01', d.is_current = FALSE   -- valid_to = the new version's start (half-open)
WHERE d.is_current AND (NOT (d.city <=> x.city) OR NOT (d.segment <=> x.segment));
INSERT INTO dim_customer_t2 (customer_id, customer, city, segment, valid_from)
SELECT x.customer_id, x.customer, x.city, x.segment, '2026-04-01'
FROM customer_extract AS x LEFT JOIN dim_customer_t2 AS d ON d.customer_id = x.customer_id AND d.is_current
WHERE d.customer_id IS NULL;
COMMIT;
SELECT customer_key, customer_id, customer, city, valid_from, valid_to, is_current
FROM dim_customer_t2 ORDER BY customer_id, valid_from;

-- migrations by hand (remember: each CREATE/ALTER commits immediately in MySQL)
CREATE TABLE schema_migrations (
    version INT PRIMARY KEY, description VARCHAR(100) NOT NULL, checksum CHAR(32) NOT NULL,
    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE suppliers (supplier_id INT PRIMARY KEY, supplier_name VARCHAR(100) NOT NULL, city VARCHAR(50) NOT NULL);
INSERT INTO schema_migrations (version, description, checksum) VALUES (1, 'create suppliers', MD5('V1__create_suppliers.sql contents'));
INSERT INTO suppliers VALUES (1, 'Western Polymers', 'Vapi'), (2, 'Deccan Cartons', 'Pune'), (3, 'Sagar Labels', 'Mumbai');
INSERT INTO schema_migrations (version, description, checksum) VALUES (2, 'seed suppliers', MD5('V2__seed_suppliers.sql contents'));
ALTER TABLE suppliers ADD COLUMN payment_terms_days INT NOT NULL DEFAULT 30;
INSERT INTO schema_migrations (version, description, checksum) VALUES (3, 'add payment terms', MD5('V3__add_payment_terms.sql contents'));
-- MySQL does not fail here, even in strict mode: ADD COLUMN fills existing rows with the type's implicit default ('' for VARCHAR).
-- ALTER TABLE suppliers ADD COLUMN gst_number VARCHAR(15) NOT NULL;
SELECT version, description FROM schema_migrations ORDER BY version;

-- ============ Exercises (MySQL track) ============
USE riverstone_2025;
WITH RECURSIVE org AS (
    SELECT staff_id, 1 AS level FROM staff WHERE manager_id IS NULL
    UNION ALL
    SELECT s.staff_id, o.level + 1 FROM staff AS s JOIN org AS o ON s.manager_id = o.staff_id
)
SELECT level, COUNT(*) AS people FROM org GROUP BY level ORDER BY level;

-- exercise 23: a daily date spine for December 2025
WITH RECURSIVE days AS (
    SELECT DATE '2025-12-01' AS day
    UNION ALL
    SELECT day + INTERVAL 1 DAY FROM days WHERE day < DATE '2025-12-31'
),
daily_sales AS (
    SELECT order_date, SUM(net_revenue) AS revenue
    FROM sales_lines
    WHERE order_date >= '2025-12-01' AND order_date < '2026-01-01'
    GROUP BY order_date
)
SELECT COUNT(*) AS days_in_month,
       SUM(CASE WHEN s.order_date IS NULL THEN 1 ELSE 0 END) AS days_without_orders,
       ROUND(SUM(COALESCE(s.revenue, 0)), 0) AS month_revenue
FROM days AS d LEFT JOIN daily_sales AS s ON s.order_date = d.day;

WITH RECURSIVE uses AS (
    SELECT b.parent_part_id, CAST(b.quantity AS DECIMAL(12,3)) AS qty FROM bom_lines AS b WHERE b.child_part_id = 306
    UNION ALL
    SELECT b.parent_part_id, CAST(u.qty * b.quantity AS DECIMAL(12,3)) FROM uses AS u JOIN bom_lines AS b ON b.child_part_id = u.parent_part_id
)
SELECT p.part_name, SUM(u.qty) AS packs_per_unit
FROM uses AS u JOIN parts AS p ON p.part_id = u.parent_part_id
WHERE p.part_type = 'Product' GROUP BY p.part_name;
