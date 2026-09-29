SELECT c.customer_id, c.customer_name,
       MAX(o.order_date) AS last_order,
       MAX(CASE WHEN o.status = 'Delivered' THEN o.order_date END) AS last_delivered
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING MAX(o.order_date) >= DATE '2026-01-06' - INTERVAL '6 months'
   AND COALESCE(MAX(CASE WHEN o.status = 'Delivered' THEN o.order_date END), DATE '1900-01-01')
       < DATE '2026-01-06' - 45
ORDER BY c.customer_id;
