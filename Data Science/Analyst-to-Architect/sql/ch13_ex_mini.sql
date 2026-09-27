\echo '### X1'
WITH customer_units AS (
    SELECT c.customer_name, SUM(s.quantity) AS units
    FROM sales_lines AS s
    JOIN customers   AS c ON s.customer_id = c.customer_id
    GROUP BY c.customer_name
)
SELECT customer_name, units
FROM customer_units
WHERE units > 100
ORDER BY units DESC;
