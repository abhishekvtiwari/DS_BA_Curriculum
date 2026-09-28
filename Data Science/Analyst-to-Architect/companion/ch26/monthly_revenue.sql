-- Monthly net revenue (sales_lines excludes cancelled orders)
SELECT date_trunc('month', order_date) AS mon,
       SUM(net_revenue)                AS revenue
FROM   sales_lines
GROUP  BY mon
ORDER  BY mon;
