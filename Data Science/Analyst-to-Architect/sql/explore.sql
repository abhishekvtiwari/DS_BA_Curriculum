SELECT DATE_TRUNC('month',o.order_date)::date m, COUNT(DISTINCT o.order_id) orders, COUNT(DISTINCT o.customer_id) cust,
 ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100))) rev
FROM orders o JOIN order_items oi USING(order_id) WHERE o.status<>'Cancelled' GROUP BY 1 ORDER BY 1;
SELECT p.category, DATE_TRUNC('month',o.order_date)::date m, ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100))) rev FROM orders o JOIN order_items oi USING(order_id) JOIN products p USING(product_id) WHERE p.category='Furniture' GROUP BY 1,2 ORDER BY 2;
SELECT c.customer_name, c.segment, COUNT(DISTINCT o.order_id) n, ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100))) rev, MIN(order_date), MAX(order_date) FROM customers c LEFT JOIN orders o USING(customer_id) LEFT JOIN order_items oi USING(order_id) GROUP BY 1,2 ORDER BY rev DESC NULLS LAST;
SELECT status, COUNT(*) FROM orders GROUP BY 1;
