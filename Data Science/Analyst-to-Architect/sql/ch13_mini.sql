\echo '### A1'
WITH customer_revenue AS (
    SELECT c.customer_name,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS revenue
    FROM customers   AS c
    JOIN orders      AS o  ON c.customer_id = o.customer_id
    JOIN order_items AS oi ON o.order_id    = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY c.customer_name
)
SELECT customer_name, ROUND(revenue, 0) AS revenue
FROM customer_revenue
WHERE revenue > (SELECT AVG(revenue) FROM customer_revenue)
ORDER BY revenue DESC;
\echo '### VIEW'
DROP VIEW IF EXISTS sales_lines;
CREATE VIEW sales_lines AS
SELECT o.order_id,
       o.order_date,
       o.customer_id,
       o.sales_rep_id,
       o.status,
       oi.product_id,
       p.category,
       oi.quantity,
       oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS net_revenue,
       oi.quantity * p.unit_cost                                  AS product_cost
FROM orders      AS o
JOIN order_items AS oi ON o.order_id    = oi.order_id
JOIN products    AS p  ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled';
\echo '### VIEWUSE'
SELECT category, ROUND(SUM(net_revenue), 0) AS net_revenue
FROM sales_lines
GROUP BY category
ORDER BY net_revenue DESC;
\echo '### A3'
WITH payments_per_invoice AS (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
),
invoice_balances AS (
    SELECT i.invoice_id,
           i.order_id,
           i.due_date,
           i.amount - COALESCE(p.paid, 0) AS balance,
           DATE '2026-03-31' - i.due_date AS days_past_due
    FROM invoices AS i
    LEFT JOIN payments_per_invoice AS p ON i.invoice_id = p.invoice_id
),
open_invoices AS (
    SELECT b.*, c.customer_name
    FROM invoice_balances AS b
    JOIN orders    AS o ON b.order_id    = o.order_id
    JOIN customers AS c ON o.customer_id = c.customer_id
    WHERE b.balance > 0
)
SELECT customer_name,
       SUM(balance)                                                         AS total_due,
       SUM(CASE WHEN days_past_due <= 0              THEN balance ELSE 0.00 END) AS not_yet_due,
       SUM(CASE WHEN days_past_due BETWEEN 1 AND 30  THEN balance ELSE 0.00 END) AS overdue_1_30,
       SUM(CASE WHEN days_past_due BETWEEN 31 AND 60 THEN balance ELSE 0.00 END) AS overdue_31_60,
       SUM(CASE WHEN days_past_due > 60              THEN balance ELSE 0.00 END) AS overdue_60_plus
FROM open_invoices
GROUP BY customer_name
ORDER BY total_due DESC;
\echo '### W0'
WITH order_totals AS (
    SELECT order_id, customer_id, order_date, SUM(net_revenue) AS order_revenue
    FROM sales_lines
    GROUP BY order_id, customer_id, order_date
)
SELECT ROUND(SUM(order_revenue), 0) AS quarter_total
FROM order_totals;
\echo '### W1'
WITH order_totals AS (
    SELECT order_id, customer_id, order_date, SUM(net_revenue) AS order_revenue
    FROM sales_lines
    GROUP BY order_id, customer_id, order_date
)
SELECT order_id,
       ROUND(order_revenue, 0)                                  AS order_revenue,
       ROUND(SUM(order_revenue) OVER (), 0)                     AS quarter_total,
       ROUND(100.0 * order_revenue / SUM(order_revenue) OVER (), 1) AS pct_of_quarter
FROM order_totals
ORDER BY order_id;
\echo '### W2'
WITH order_totals AS (
    SELECT order_id, customer_id, SUM(net_revenue) AS order_revenue
    FROM sales_lines
    GROUP BY order_id, customer_id
)
SELECT c.customer_name,
       t.order_id,
       ROUND(t.order_revenue, 0)                                              AS order_revenue,
       ROUND(SUM(t.order_revenue) OVER (PARTITION BY t.customer_id), 0)       AS customer_total,
       ROUND(100.0 * t.order_revenue
             / SUM(t.order_revenue) OVER (PARTITION BY t.customer_id), 1)     AS pct_of_customer
FROM order_totals AS t
JOIN customers    AS c ON t.customer_id = c.customer_id
ORDER BY c.customer_name, t.order_id;
\echo '### W3'
WITH units AS (
    SELECT p.product_name, COALESCE(SUM(s.quantity), 0) AS units_sold
    FROM products AS p
    LEFT JOIN sales_lines AS s ON p.product_id = s.product_id
    GROUP BY p.product_name
)
SELECT product_name,
       units_sold,
       ROW_NUMBER() OVER (ORDER BY units_sold DESC, product_name) AS row_num,
       RANK()       OVER (ORDER BY units_sold DESC)               AS rank,
       DENSE_RANK() OVER (ORDER BY units_sold DESC)               AS dense_rank
FROM units
ORDER BY units_sold DESC, product_name;
\echo '### W4err'
SELECT order_id, customer_id, order_date
FROM orders
WHERE ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) = 1;
\echo '### W4'
WITH ranked AS (
    SELECT c.customer_name,
           o.order_id,
           o.order_date,
           o.status,
           ROW_NUMBER() OVER (PARTITION BY o.customer_id
                              ORDER BY o.order_date DESC, o.order_id DESC) AS recency_rank
    FROM orders    AS o
    JOIN customers AS c ON o.customer_id = c.customer_id
)
SELECT customer_name, order_id, order_date, status
FROM ranked
WHERE recency_rank = 1
ORDER BY order_date DESC;
\echo '### W5'
SELECT c.customer_name,
       o.order_id,
       o.order_date,
       LAG(o.order_date) OVER (PARTITION BY o.customer_id ORDER BY o.order_date)                AS previous_order,
       o.order_date - LAG(o.order_date) OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS days_since_previous
FROM orders    AS o
JOIN customers AS c ON o.customer_id = c.customer_id
WHERE o.status <> 'Cancelled'
ORDER BY c.customer_name, o.order_date;
