-- Analyst to Architect, Chapter 14 — compare your cleaned order lines with the truth, every column of every line.
-- Run in riverstone_full after ch14_load_*.sql (which loads truth_order_lines) and your cleaning script.
-- Works in PostgreSQL and in MySQL 8.0.31 or later (EXCEPT). It lists the lines of clean_order_lines that differ
-- from the truth in any column; for the chapter's pipeline that is exactly the 20 quarantined lines.
SELECT order_item_id, order_date, customer_code, product_id, quantity,
       unit_price, discount_pct, status, branch, sales_rep
FROM clean_order_lines
EXCEPT
SELECT order_item_id, order_date, customer_code, product_id, quantity,
       unit_price, discount_pct, status, branch, sales_rep
FROM truth_order_lines
ORDER BY order_item_id;
