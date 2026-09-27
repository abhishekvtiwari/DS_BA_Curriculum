\pset footer on
\echo '### Q1'
SELECT customer_name, city FROM customers;
\echo '### Q3'
SELECT product_name, unit_price, ROUND(unit_price * 1.18, 2) AS price_incl_tax FROM products;
\echo '### Q4'
SELECT DISTINCT city FROM customers;
\echo '### Q5'
SELECT product_name, unit_price FROM products ORDER BY unit_price DESC LIMIT 3;
\echo '### Q6'
SELECT order_id, customer_id, order_date, status FROM orders WHERE status = 'Delivered';
\echo '### Q7a'
SELECT customer_name, city, segment FROM customers WHERE segment = 'Retail' OR segment = 'Wholesale' AND city = 'Mumbai';
\echo '### Q7b'
SELECT customer_name, city, segment FROM customers WHERE (segment = 'Retail' OR segment = 'Wholesale') AND city = 'Mumbai';
\echo '### Q8'
SELECT order_id, order_date, status FROM orders WHERE order_date BETWEEN '2026-02-01' AND '2026-02-28' AND status IN ('Delivered','Shipped');
\echo '### Q9'
SELECT product_name, unit_price FROM products WHERE product_name LIKE 'Storage%';
\echo '### Q10a'
SELECT customer_name FROM customers WHERE city = NULL;
\echo '### Q10b'
SELECT customer_name FROM customers WHERE city IS NULL;
\echo '### Q10c'
SELECT customer_name, city FROM customers WHERE city <> 'Mumbai';
\echo '### Q11'
SELECT customer_name, COALESCE(city, 'Unknown') AS city FROM customers ORDER BY customer_id;
\echo '### Q12'
SELECT customer_name, segment, signup_date FROM customers ORDER BY segment ASC, signup_date DESC;
\echo '### Q13'
SELECT product_name, unit_price,
       CASE WHEN unit_price >= 1000 THEN 'Premium'
            WHEN unit_price >= 500  THEN 'Mid-range'
            ELSE 'Budget' END AS price_band
FROM products ORDER BY unit_price;
\echo '### Q14'
SELECT order_id, order_date, EXTRACT(MONTH FROM order_date) AS month_no, DATE_TRUNC('month', order_date)::date AS order_month FROM orders WHERE order_id <= 5004;
\echo '### Q15'
SELECT COUNT(*) AS total_orders, COUNT(sales_rep_id) AS orders_with_rep, COUNT(DISTINCT customer_id) AS unique_customers FROM orders;
\echo '### Q16'
SELECT status, COUNT(*) AS num_orders FROM orders GROUP BY status ORDER BY num_orders DESC;
\echo '### Q17'
SELECT order_id, SUM(quantity * unit_price * (1 - discount_pct/100)) AS order_revenue FROM order_items GROUP BY order_id ORDER BY order_id LIMIT 5;
\echo '### Q18'
SELECT customer_id, COUNT(*) AS num_orders FROM orders GROUP BY customer_id HAVING COUNT(*) > 1 ORDER BY customer_id;
\echo '### Q18err'
SELECT customer_id, COUNT(*) AS num_orders FROM orders WHERE num_orders > 1 GROUP BY customer_id;
\echo '### Q19'
SELECT o.order_id, c.customer_name, o.order_date FROM orders AS o INNER JOIN customers AS c ON o.customer_id = c.customer_id ORDER BY o.order_id LIMIT 4;
\echo '### Q20'
SELECT c.customer_name, o.order_id FROM customers AS c LEFT JOIN orders AS o ON c.customer_id = o.customer_id ORDER BY c.customer_id, o.order_id;
\echo '### Q21'
SELECT c.customer_name FROM customers AS c LEFT JOIN orders AS o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL;
\echo '### Q22'
SELECT p.product_name FROM products AS p LEFT JOIN order_items AS oi ON p.product_id = oi.product_id WHERE oi.order_item_id IS NULL;
\echo '### Q23a'
SELECT c.customer_name, COUNT(*) AS num_orders FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.customer_name ORDER BY c.customer_name;
\echo '### Q23b'
SELECT c.customer_name, COUNT(DISTINCT o.order_id) AS num_orders FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN order_items oi ON o.order_id = oi.order_id GROUP BY c.customer_name ORDER BY c.customer_name;
\echo '### Q24'
SELECT COALESCE(c.city,'Unknown') AS city, COUNT(DISTINCT o.order_id) AS orders, ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 0) AS revenue
FROM orders AS o
JOIN customers   AS c  ON o.customer_id = c.customer_id
JOIN order_items AS oi ON o.order_id    = oi.order_id
WHERE o.status <> 'Cancelled'
GROUP BY COALESCE(c.city,'Unknown')
ORDER BY revenue DESC;
\echo '### Q25'
SELECT e.employee_name, e.job_title, m.employee_name AS manager_name FROM employees AS e LEFT JOIN employees AS m ON e.manager_id = m.employee_id ORDER BY e.employee_id;
\echo '### Q26a'
SELECT c.customer_name, o.order_id, o.status FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id AND o.status = 'Pending' ORDER BY c.customer_id;
\echo '### Q26b'
SELECT c.customer_name, o.order_id, o.status FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id WHERE o.status = 'Pending' ORDER BY c.customer_id;
\echo '### Q27'
SELECT COUNT(*) AS combos FROM (SELECT DISTINCT segment FROM customers) s CROSS JOIN (SELECT DISTINCT category FROM products) p;
\echo '### Q27b'
SELECT s.segment, p.category FROM (SELECT DISTINCT segment FROM customers) s CROSS JOIN (SELECT DISTINCT category FROM products) p ORDER BY 1,2 LIMIT 5;
\echo '### Q28'
SELECT product_name, unit_price FROM products WHERE unit_price > (SELECT AVG(unit_price) FROM products) ORDER BY unit_price;
\echo '### Q28avg'
SELECT ROUND(AVG(unit_price),2) FROM products;
\echo '### Q29'
SELECT customer_name FROM customers WHERE customer_id IN (SELECT o.customer_id FROM orders o JOIN order_items oi ON o.order_id = oi.order_id WHERE oi.product_id = 105) ORDER BY customer_name;
\echo '### Q30'
SELECT c.customer_name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'Shipped');
\echo '### Q31a'
SELECT city FROM customers WHERE segment = 'Retail' UNION SELECT city FROM customers WHERE segment = 'Hospitality';
\echo '### Q31b'
SELECT city FROM customers WHERE segment = 'Retail' UNION ALL SELECT city FROM customers WHERE segment = 'Hospitality';
\echo '### Q32'
SELECT DATE_TRUNC('month', o.order_date)::date AS month,
       COUNT(DISTINCT o.order_id)    AS orders,
       COUNT(DISTINCT o.customer_id) AS active_customers,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 0) AS net_revenue
FROM orders AS o
JOIN order_items AS oi ON o.order_id = oi.order_id
WHERE o.status IN ('Delivered', 'Shipped')
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY month;
\echo '### Q33'
BEGIN;
UPDATE orders SET status = 'Delivered' WHERE order_id = 5011;
SELECT order_id, status FROM orders WHERE order_id = 5011;
ROLLBACK;
SELECT order_id, status FROM orders WHERE order_id = 5011;
