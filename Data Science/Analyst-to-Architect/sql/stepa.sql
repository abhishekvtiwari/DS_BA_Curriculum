SELECT i.invoice_id,
       i.amount,
       COALESCE(pay.paid, 0)            AS paid,
       i.amount - COALESCE(pay.paid, 0) AS balance
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
GROUP BY c.customer_name
ORDER BY total_due DESC;
SELECT order_id, sales_rep_id FROM orders WHERE sales_rep_id IS NULL;
