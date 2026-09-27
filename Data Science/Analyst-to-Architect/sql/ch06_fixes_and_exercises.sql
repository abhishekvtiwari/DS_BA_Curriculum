\echo '### Q4'
SELECT DISTINCT city FROM customers ORDER BY city;
\echo '### Q17'
SELECT order_id, ROUND(SUM(quantity * unit_price * (1 - discount_pct / 100)), 2) AS order_revenue FROM order_items GROUP BY order_id ORDER BY order_id LIMIT 5;
\echo '### Q31a'
SELECT city FROM customers WHERE segment = 'Retail' UNION SELECT city FROM customers WHERE segment = 'Hospitality' ORDER BY city;
\echo '### Q31b'
SELECT city FROM customers WHERE segment = 'Retail' UNION ALL SELECT city FROM customers WHERE segment = 'Hospitality' ORDER BY city;
\echo '### E1'
SELECT product_name, unit_price FROM products WHERE category = 'Kitchen' ORDER BY unit_price ASC;
\echo '### E2'
SELECT segment, COUNT(*) AS num_customers FROM customers GROUP BY segment ORDER BY num_customers DESC, segment;
\echo '### E3'
SELECT order_id, customer_id, order_date FROM orders WHERE order_date >= '2026-03-01' AND order_date < '2026-04-01' ORDER BY order_date;
\echo '### E4'
SELECT customer_name FROM customers WHERE customer_name LIKE '%Foods%' OR customer_name LIKE '%Mart%';
\echo '### M1'
SELECT p.product_name, COALESCE(SUM(oi.quantity), 0) AS units_sold
FROM products AS p
LEFT JOIN order_items AS oi ON p.product_id = oi.product_id
LEFT JOIN orders      AS o  ON oi.order_id  = o.order_id AND o.status <> 'Cancelled'
WHERE oi.order_item_id IS NULL OR o.order_id IS NOT NULL
GROUP BY p.product_name
ORDER BY units_sold DESC;
\echo '### M1alt'
SELECT p.product_name, COALESCE(s.units_sold, 0) AS units_sold
FROM products AS p
LEFT JOIN (
    SELECT oi.product_id, SUM(oi.quantity) AS units_sold
    FROM order_items AS oi
    JOIN orders AS o ON oi.order_id = o.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY oi.product_id
) AS s ON p.product_id = s.product_id
ORDER BY units_sold DESC;
\echo '### M2'
SELECT COALESCE(e.employee_name, 'Unassigned') AS sales_rep,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
LEFT JOIN employees AS e ON o.sales_rep_id = e.employee_id
WHERE o.status <> 'Cancelled'
GROUP BY COALESCE(e.employee_name, 'Unassigned')
ORDER BY net_revenue DESC;
\echo '### M3'
SELECT c.customer_name
FROM customers AS c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
  AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'Delivered');
\echo '### M4'
SELECT ROUND(AVG(order_revenue), 2) AS avg_order_value
FROM (
    SELECT o.order_id, SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS order_revenue
    FROM orders AS o
    JOIN order_items AS oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY o.order_id
) AS per_order;
\echo '### H1'
SELECT c.customer_name, MIN(o.order_date) AS first_order, MAX(o.order_date) AS latest_order,
       MAX(o.order_date) - MIN(o.order_date) AS days_between
FROM customers AS c
JOIN orders AS o ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY days_between DESC, c.customer_name;
\echo '### H2'
SELECT p.category,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue,
       ROUND(100.0 * SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100))
             / (SELECT SUM(oi2.quantity * oi2.unit_price * (1 - oi2.discount_pct / 100))
                FROM order_items oi2 JOIN orders o2 ON oi2.order_id = o2.order_id
                WHERE o2.status <> 'Cancelled'), 1) AS pct_of_total
FROM order_items AS oi
JOIN orders   AS o ON oi.order_id   = o.order_id
JOIN products AS p ON oi.product_id = p.product_id
WHERE o.status <> 'Cancelled'
GROUP BY p.category
ORDER BY net_revenue DESC;
\echo '### H3'
SELECT customer_name, ROUND(customer_revenue, 0) AS customer_revenue
FROM (
    SELECT c.customer_name, SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS customer_revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status <> 'Cancelled'
    GROUP BY c.customer_name
) AS t
WHERE customer_revenue > (
    SELECT AVG(customer_revenue) FROM (
        SELECT o.customer_id, SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) AS customer_revenue
        FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status <> 'Cancelled'
        GROUP BY o.customer_id
    ) AS x
)
ORDER BY customer_revenue DESC;
\echo '### H3avg'
SELECT ROUND(AVG(r),0) FROM (SELECT o.customer_id, SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)) r FROM orders o JOIN order_items oi ON o.order_id=oi.order_id WHERE o.status<>'Cancelled' GROUP BY o.customer_id) x;
\echo '### total'
SELECT ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)),0) FROM order_items oi JOIN orders o ON oi.order_id=o.order_id WHERE o.status<>'Cancelled';
