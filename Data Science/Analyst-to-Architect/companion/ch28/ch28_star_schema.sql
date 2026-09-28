-- Analyst to Architect · Chapter 28 · Advanced SQL, Performance & Data Modeling
-- File: ch28_star_schema.sql (PostgreSQL)
-- What: builds the dw star schema of section 28.9 (date, product, sales rep, and type 2 customer dimensions,
--       and fact_sales_line) inside riverstone_2025. Identical to the code printed in the chapter.
-- How:  after riverstone_2025_setup.sql and ch28_2025_addons.sql:  psql -d riverstone_2025 -f ch28_star_schema.sql
--       Safe to re-run: it drops and recreates the dw schema.
-- Check: SELECT ROUND(SUM(net_revenue)) FROM dw.fact_sales_line;  returns 4335471 (326 rows).
-- Tested on: PostgreSQL 16 (Ubuntu 24.04).
-- Riverstone Supplies is fictional; every name and number is invented.

DROP SCHEMA IF EXISTS dw CASCADE;
CREATE SCHEMA dw;

CREATE TABLE dw.dim_date (
    date_key      INTEGER PRIMARY KEY,
    full_date     DATE NOT NULL UNIQUE,
    day_name      VARCHAR(9) NOT NULL,
    month_start   DATE NOT NULL,
    month_name    VARCHAR(9) NOT NULL,
    quarter_label CHAR(7) NOT NULL,
    is_weekend    BOOLEAN NOT NULL
);

INSERT INTO dw.dim_date
SELECT TO_CHAR(d, 'YYYYMMDD')::INTEGER,
       d::date,
       TRIM(TO_CHAR(d, 'Day')),
       DATE_TRUNC('month', d)::date,
       TRIM(TO_CHAR(d, 'Month')),
       TO_CHAR(d, 'YYYY-"Q"Q'),
       EXTRACT(ISODOW FROM d) IN (6, 7)
FROM generate_series(DATE '2025-01-01', DATE '2025-12-31', INTERVAL '1 day') AS d;

CREATE TABLE dw.dim_product (
    product_key   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id    INTEGER NOT NULL UNIQUE,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(30) NOT NULL
);
INSERT INTO dw.dim_product (product_id, product_name, category)
SELECT product_id, product_name, category FROM products ORDER BY product_id;

CREATE TABLE dw.dim_sales_rep (
    sales_rep_key  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id    INTEGER UNIQUE,
    rep_name       VARCHAR(100) NOT NULL,
    job_title      VARCHAR(50) NOT NULL
);
INSERT INTO dw.dim_sales_rep (employee_id, rep_name, job_title)
VALUES (NULL, 'No rep recorded', 'Unknown');
INSERT INTO dw.dim_sales_rep (employee_id, rep_name, job_title)
SELECT employee_id, employee_name, job_title FROM employees ORDER BY employee_id;

CREATE TABLE dw.dim_customer (
    customer_key   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id    INTEGER NOT NULL,
    customer_name  VARCHAR(100) NOT NULL,
    city           VARCHAR(50),
    segment        VARCHAR(30) NOT NULL,
    valid_from     DATE NOT NULL,
    valid_to       DATE NOT NULL,
    is_current     BOOLEAN NOT NULL
);

INSERT INTO dw.dim_customer
    (customer_id, customer_name, city, segment, valid_from, valid_to, is_current)
WITH version_starts AS (
    SELECT customer_id, signup_date AS valid_from FROM customers
    UNION
    SELECT customer_id, changed_on FROM customer_changes
),
versions AS (
    SELECT customer_id,
           valid_from,
           LEAD(valid_from, 1, DATE '9999-12-31')
               OVER (PARTITION BY customer_id ORDER BY valid_from) AS valid_to
    FROM version_starts
)
SELECT v.customer_id,
       c.customer_name,
       COALESCE(
           (SELECT ch.new_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'city'
              AND ch.changed_on <= v.valid_from
            ORDER BY ch.changed_on DESC LIMIT 1),
           (SELECT ch.old_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'city'
            ORDER BY ch.changed_on LIMIT 1),
           c.city)                                   AS city,
       COALESCE(
           (SELECT ch.new_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'segment'
              AND ch.changed_on <= v.valid_from
            ORDER BY ch.changed_on DESC LIMIT 1),
           (SELECT ch.old_value FROM customer_changes AS ch
            WHERE ch.customer_id = v.customer_id AND ch.column_name = 'segment'
            ORDER BY ch.changed_on LIMIT 1),
           c.segment)                                AS segment,
       v.valid_from,
       v.valid_to,
       v.valid_to = DATE '9999-12-31'                AS is_current
FROM versions AS v
JOIN customers AS c ON c.customer_id = v.customer_id
ORDER BY v.customer_id, v.valid_from;

CREATE TABLE dw.fact_sales_line (
    order_item_id  INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL,
    date_key       INTEGER NOT NULL REFERENCES dw.dim_date (date_key),
    customer_key   INTEGER NOT NULL REFERENCES dw.dim_customer (customer_key),
    product_key    INTEGER NOT NULL REFERENCES dw.dim_product (product_key),
    sales_rep_key  INTEGER NOT NULL REFERENCES dw.dim_sales_rep (sales_rep_key),
    quantity       INTEGER NOT NULL,
    net_revenue    NUMERIC(12,2) NOT NULL,
    product_cost   NUMERIC(12,2) NOT NULL
);

INSERT INTO dw.fact_sales_line
SELECT oi.order_item_id,
       o.order_id,
       TO_CHAR(o.order_date, 'YYYYMMDD')::INTEGER,
       dc.customer_key,
       dp.product_key,
       dr.sales_rep_key,
       oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100),
       oi.quantity * p.unit_cost
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products    AS p  ON p.product_id = oi.product_id
JOIN dw.dim_customer AS dc
  ON dc.customer_id = o.customer_id
 AND o.order_date >= dc.valid_from AND o.order_date < dc.valid_to
JOIN dw.dim_product  AS dp ON dp.product_id = oi.product_id
JOIN dw.dim_sales_rep AS dr
  ON dr.employee_id IS NOT DISTINCT FROM o.sales_rep_id
WHERE o.status <> 'Cancelled';
