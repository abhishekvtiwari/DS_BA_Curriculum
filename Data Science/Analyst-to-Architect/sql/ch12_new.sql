\echo '### DUMP products'
SELECT * FROM products ORDER BY 1;
\echo '### DUMP invoices'
SELECT * FROM invoices ORDER BY 1;
\echo '### DUMP payments'
SELECT * FROM payments ORDER BY 1;
\echo '### N2 margin filter'
SELECT product_name, unit_price, unit_cost,
       ROUND(100.0 * (unit_price - unit_cost) / unit_price, 1) AS margin_pct
FROM products
WHERE (unit_price - unit_cost) / unit_price < 0.30
ORDER BY margin_pct;
\echo '### N4 due status'
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
\echo '### N5 margin by category'
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
\echo '### N6 wrong'
SELECT SUM(i.amount)                   AS total_invoiced,
       SUM(p.amount)                   AS total_paid,
       SUM(i.amount) - SUM(p.amount)   AS outstanding
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id;
\echo '### N6 rows'
SELECT i.invoice_id, i.amount AS invoice_amount, p.payment_id, p.amount AS payment_amount
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE i.invoice_id IN (9001, 9002, 9007)
ORDER BY i.invoice_id, p.payment_id;
\echo '### N6 right'
SELECT SUM(i.amount)                        AS total_invoiced,
       SUM(COALESCE(p.paid, 0))             AS total_paid,
       SUM(i.amount - COALESCE(p.paid, 0))  AS outstanding
FROM invoices AS i
LEFT JOIN (
    SELECT invoice_id, SUM(amount) AS paid
    FROM payments
    GROUP BY invoice_id
) AS p ON i.invoice_id = p.invoice_id;
\echo '### N6 check'
SELECT (SELECT SUM(amount) FROM invoices) AS invoiced, (SELECT SUM(amount) FROM payments) AS paid;
\echo '### N7 latest payment'
SELECT p.invoice_id, p.payment_date, p.amount
FROM payments AS p
WHERE p.payment_date = (
    SELECT MAX(p2.payment_date)
    FROM payments AS p2
    WHERE p2.invoice_id = p.invoice_id
)
ORDER BY p.invoice_id;
\echo '### M1 inactive customers'
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
\echo '### M2 discounts'
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
\echo '### M3 ageing'
SELECT c.customer_name,
       SUM(inv.balance) AS total_due,
       SUM(CASE WHEN inv.due_date >= DATE '2026-03-31' THEN inv.balance ELSE 0 END) AS not_yet_due,
       SUM(CASE WHEN inv.due_date <  DATE '2026-03-31'
                 AND DATE '2026-03-31' - inv.due_date <= 30 THEN inv.balance ELSE 0 END) AS overdue_1_30,
       SUM(CASE WHEN DATE '2026-03-31' - inv.due_date BETWEEN 31 AND 60 THEN inv.balance ELSE 0 END) AS overdue_31_60,
       SUM(CASE WHEN DATE '2026-03-31' - inv.due_date > 60 THEN inv.balance ELSE 0 END) AS overdue_60_plus
FROM (
    SELECT i.invoice_id,
           i.order_id,
           i.due_date,
           i.amount - COALESCE(pay.paid, 0) AS balance
    FROM invoices AS i
    LEFT JOIN (
        SELECT invoice_id, SUM(amount) AS paid
        FROM payments
        GROUP BY invoice_id
    ) AS pay ON i.invoice_id = pay.invoice_id
) AS inv
JOIN orders    AS o ON inv.order_id   = o.order_id
JOIN customers AS c ON o.customer_id  = c.customer_id
WHERE inv.balance > 0
GROUP BY c.customer_name
ORDER BY total_due DESC;
\echo '### M4 leaderboard'
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
\echo '### E15'
SELECT method, COUNT(*) AS payments, SUM(amount) AS amount_received
FROM payments
GROUP BY method
ORDER BY amount_received DESC;
\echo '### E16'
SELECT i.invoice_id, i.amount, i.due_date
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
WHERE p.payment_id IS NULL
ORDER BY i.due_date;
\echo '### E17'
SELECT i.invoice_id,
       i.amount,
       COUNT(p.payment_id)              AS num_payments,
       COALESCE(SUM(p.amount), 0)       AS amount_paid,
       i.amount - COALESCE(SUM(p.amount), 0) AS balance
FROM invoices AS i
LEFT JOIN payments AS p ON i.invoice_id = p.invoice_id
GROUP BY i.invoice_id, i.amount
HAVING i.amount - COALESCE(SUM(p.amount), 0) > 0
ORDER BY balance DESC;
\echo '### E18 stuck orders'
SELECT order_id, order_date, status, DATE '2026-03-31' - order_date AS days_open
FROM orders
WHERE (status = 'Pending' AND DATE '2026-03-31' - order_date > 7)
   OR (status = 'Shipped' AND DATE '2026-03-31' - order_date > 14)
ORDER BY days_open DESC;
