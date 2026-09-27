SELECT order_date, COUNT(*) FROM orders GROUP BY 1 HAVING COUNT(*)>1 ORDER BY 1 LIMIT 10;
SELECT * FROM leads ORDER BY lower(email), created_at LIMIT 14;
SELECT stage, COUNT(*) FROM lead_stage_history GROUP BY 1;
SELECT DATE_TRUNC('month', MIN(order_date))::date AS first_month, COUNT(*) FROM (SELECT customer_id, MIN(order_date) order_date FROM orders WHERE status<>'Cancelled' GROUP BY 1) x GROUP BY 1 ORDER BY 1;
