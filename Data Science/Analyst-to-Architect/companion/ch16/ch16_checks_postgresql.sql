-- Analyst to Architect, Chapter 16 — check every DAX measure against SQL (PostgreSQL 16+).
-- Run from anywhere:  psql -d riverstone_full -f ch16_checks_postgresql.sql
-- Each block prints the value a Power BI card should show. Riverstone Supplies is fictional.
\echo ==A totals
SELECT ROUND(SUM(net_revenue)) AS all_years, ROUND(SUM(net_revenue) FILTER (WHERE order_date >= '2025-01-01')) AS y2025,
       COUNT(DISTINCT order_id) FILTER (WHERE order_date >= '2025-01-01') AS orders_2025,
       COUNT(DISTINCT customer_id) FILTER (WHERE order_date >= '2025-01-01') AS customers_2025,
       ROUND(SUM(net_revenue) FILTER (WHERE order_date >= '2025-01-01') / COUNT(DISTINCT order_id) FILTER (WHERE order_date >= '2025-01-01'), 2) AS aov_2025,
       ROUND(100*(1 - SUM(product_cost) FILTER (WHERE order_date >= '2025-01-01') / SUM(net_revenue) FILTER (WHERE order_date >= '2025-01-01')), 1) AS gm_2025
FROM sales_lines;
\echo ==B ytd june
SELECT ROUND(SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2025-01-01' AND '2025-06-30')) AS ytd_jun_2025,
       ROUND(SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2024-01-01' AND '2024-06-30')) AS ytd_jun_2024,
       ROUND(100.0*SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2025-01-01' AND '2025-06-30')/SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2024-01-01' AND '2024-06-30') - 100, 1) AS yoy_pct
FROM sales_lines;
\echo ==C quarterly 2025 with LY
SELECT 'Q' || EXTRACT(QUARTER FROM order_date) AS quarter,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2025)) AS rev_2025,
       ROUND(SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2024)) AS rev_2024,
       ROUND(100.0*SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2025)/SUM(net_revenue) FILTER (WHERE EXTRACT(YEAR FROM order_date)=2024)-100,1) AS yoy_pct
FROM sales_lines WHERE order_date >= '2024-01-01' GROUP BY 1 ORDER BY 1;
\echo ==D region 2025
SELECT r.region, ROUND(SUM(s.net_revenue)) AS rev_2025, COUNT(DISTINCT s.customer_id) AS customers
FROM sales_lines s JOIN customers c ON c.customer_id=s.customer_id
LEFT JOIN (VALUES
 ('Mumbai','West'),('Pune','West'),('Ahmedabad','West'),('Surat','West'),('Nashik','West'),('Nagpur','West'),('Indore','West'),('Goa','West'),('Vadodara','West'),('Rajkot','West'),('Thane','West'),('Aurangabad','West'),
 ('Bengaluru','South'),('Chennai','South'),('Hyderabad','South'),('Kochi','South'),('Coimbatore','South'),('Mysuru','South'),('Visakhapatnam','South'),('Madurai','South'),('Mangaluru','South'),('Thiruvananthapuram','South'),
 ('Delhi','North'),('Jaipur','North'),('Lucknow','North'),('Chandigarh','North'),('Udaipur','North'),('Kanpur','North'),('Ludhiana','North'),('Dehradun','North'),('Agra','North'),('Noida','North'),('Gurugram','North'),
 ('Kolkata','East'),('Bhubaneswar','East'),('Patna','East'),('Guwahati','East'),('Ranchi','East'),('Raipur','East')) AS r(city,region) ON r.city=c.city
WHERE s.order_date >= '2025-01-01' GROUP BY 1 ORDER BY 2 DESC;
\echo ==E top products 2025
SELECT p.product_name, ROUND(SUM(s.net_revenue)) AS rev_2025, ROUND(100*SUM(s.net_revenue)/SUM(SUM(s.net_revenue)) OVER (),1) AS share
FROM sales_lines s JOIN products p ON p.product_id=s.product_id WHERE s.order_date >= '2025-01-01' GROUP BY 1 ORDER BY 2 DESC LIMIT 4;
\echo ==F oct
SELECT ROUND(SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2025-10-01' AND '2025-10-31')) AS oct25,
       ROUND(SUM(net_revenue) FILTER (WHERE order_date BETWEEN '2024-10-01' AND '2024-10-31')) AS oct24 FROM sales_lines;
\echo ==G attainment 2025 and q4
SELECT ROUND(100*SUM(a.rev)/SUM(t.target_revenue),1) AS pct_2025 FROM sales_targets t JOIN (SELECT DATE_TRUNC('month',order_date)::date m, SUM(net_revenue) rev FROM sales_lines GROUP BY 1) a ON a.m=t.target_month WHERE t.target_month>='2025-01-01';
\echo ==H date table
SELECT COUNT(*) AS days, MIN(d)::date AS first_day, MAX(d)::date AS last_day FROM generate_series('2023-01-01'::date,'2025-12-31'::date,'1 day') AS d;
\echo ==I top 10 customers 2025 share
WITH c AS (SELECT customer_id, SUM(net_revenue) rev FROM sales_lines WHERE order_date>='2025-01-01' GROUP BY 1)
SELECT ROUND(100*SUM(rev) FILTER (WHERE rnk<=10)/SUM(rev),1) AS top10_share, ROUND(MAX(rev)) AS biggest_customer
FROM (SELECT rev, RANK() OVER (ORDER BY rev DESC) rnk FROM c) x;
\echo ==J rows in model
SELECT (SELECT COUNT(*) FROM order_items) AS order_items, (SELECT COUNT(*) FROM orders) AS orders, (SELECT COUNT(*) FROM customers) AS customers;
\echo ==K q4 2025 detail
SELECT COUNT(DISTINCT order_id) AS orders_q4, COUNT(DISTINCT customer_id) AS customers_q4, ROUND(SUM(net_revenue)) AS rev_q4,
       ROUND(SUM(net_revenue)/COUNT(DISTINCT order_id),2) AS aov_q4, ROUND(100*(1-SUM(product_cost)/SUM(net_revenue)),1) AS gm_q4
FROM sales_lines WHERE order_date BETWEEN '2025-10-01' AND '2025-12-31';
\echo ==L q4 attainment
SELECT ROUND(SUM(t.target_revenue)) AS target_q4, ROUND(100*SUM(a.rev)/SUM(t.target_revenue),1) AS pct
FROM sales_targets t JOIN (SELECT DATE_TRUNC('month',order_date)::date m, SUM(net_revenue) rev FROM sales_lines GROUP BY 1) a ON a.m=t.target_month
WHERE t.target_month BETWEEN '2025-10-01' AND '2025-12-31';
\echo ==M segment 2025 with LY
SELECT c.segment, ROUND(SUM(s.net_revenue) FILTER (WHERE s.order_date>='2025-01-01')) AS rev_2025,
       ROUND(SUM(s.net_revenue) FILTER (WHERE s.order_date BETWEEN '2024-01-01' AND '2024-12-31')) AS rev_2024,
       ROUND(100.0*SUM(s.net_revenue) FILTER (WHERE s.order_date>='2025-01-01')/SUM(s.net_revenue) FILTER (WHERE s.order_date BETWEEN '2024-01-01' AND '2024-12-31')-100,1) AS yoy
FROM sales_lines s JOIN customers c USING (customer_id) WHERE s.order_date>='2024-01-01' GROUP BY 1 ORDER BY 2 DESC;
\echo ==N top rep 2025
SELECT e.employee_name, ROUND(SUM(s.net_revenue)) AS rev_2025 FROM sales_lines s JOIN employees e ON e.employee_id=s.sales_rep_id
WHERE s.order_date>='2025-01-01' GROUP BY 1 ORDER BY 2 DESC LIMIT 3;
\echo ==O no rep 2025
SELECT ROUND(SUM(net_revenue)) AS rev_no_rep, COUNT(*) AS lines FROM sales_lines WHERE sales_rep_id IS NULL AND order_date>='2025-01-01';
\echo ==P lines vs orders 2025
SELECT COUNT(*) AS lines_2025, COUNT(DISTINCT order_id) AS orders_2025 FROM sales_lines WHERE order_date>='2025-01-01';
\echo ==Q monthly 2025 oct row
SELECT ROUND(SUM(net_revenue)) AS oct_2025, ROUND(SUM(product_cost)) AS cost_oct FROM sales_lines WHERE order_date BETWEEN '2025-10-01' AND '2025-10-31';
\echo ==R cancelled impact 2025
SELECT ROUND(SUM(oi.quantity*oi.unit_price*(1-oi.discount_pct/100))) AS cancelled_value_2025, COUNT(DISTINCT o.order_id) AS cancelled_orders
FROM order_items oi JOIN orders o USING (order_id) WHERE o.status='Cancelled' AND o.order_date>='2025-01-01';
