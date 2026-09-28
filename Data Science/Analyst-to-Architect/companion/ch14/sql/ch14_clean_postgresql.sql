-- Analyst to Architect, Chapter 14 — the cleaning pipeline (PostgreSQL 16+). Run after ch14_load_postgresql.sql.
-- In DBeaver: make riverstone_full the active database, open this file, Execute SQL Script (Alt+X).
-- Builds clean_order_lines, dq_order_issues (quarantine and repairs), and clean_customers.
-- Section 14.9 of the chapter prints and explains every statement below.
DROP TABLE IF EXISTS clean_order_lines, dq_order_issues, clean_customers;

CREATE TABLE clean_order_lines AS
WITH data_rows AS (                          -- 1. drop repeated headers and the footer
  SELECT * FROM stg_orders_raw WHERE order_item_id ~ '^[0-9]+$'
), deduped AS (                              -- 2. keep one copy of each exported line
  SELECT DISTINCT * FROM data_rows
), parts AS (                                -- 3. split each date format; entry time in IST
  SELECT d.*,
    CASE WHEN order_date ~ '^\d{2}[-/]\d{2}[-/]\d{4}$' THEN substr(order_date, 7, 4)::int
         WHEN order_date ~ '^\d{4}-\d{2}-\d{2}$'        THEN substr(order_date, 1, 4)::int END AS y,
    CASE WHEN order_date ~ '^\d{2}[-/]\d{2}[-/]\d{4}$' THEN substr(order_date, 4, 2)::int
         WHEN order_date ~ '^\d{4}-\d{2}-\d{2}$'        THEN substr(order_date, 6, 2)::int END AS m,
    CASE WHEN order_date ~ '^\d{2}[-/]\d{2}[-/]\d{4}$' THEN substr(order_date, 1, 2)::int
         WHEN order_date ~ '^\d{4}-\d{2}-\d{2}$'        THEN substr(order_date, 9, 2)::int END AS dd,
    entered_at_utc::timestamptz AT TIME ZONE 'Asia/Kolkata' AS entered_at_ist
  FROM deduped d
), typed AS (                                -- 4. build and check the date
  SELECT p.*,
    CASE WHEN order_date ~ '^\d{5}$' THEN DATE '1899-12-30' + order_date::int
         WHEN y IS NOT NULL AND m BETWEEN 1 AND 12 AND dd >= 1
              AND EXTRACT(MONTH FROM make_date(y, m, 1) + (dd - 1)) = m
         THEN make_date(y, m, 1) + (dd - 1) END AS parsed_date,
    regexp_replace(regexp_replace(unit_price, '^[^0-9]+', ''), ',', '', 'g')::numeric AS price
  FROM parts p
)
SELECT                                       -- 5. the finished columns
  order_item_id::int                                   AS order_item_id,
  order_id::int                                        AS order_id,
  COALESCE(parsed_date, entered_at_ist::date)          AS order_date,
  (parsed_date IS NULL)                                AS date_repaired,
  LPAD(TRIM(customer_code), 4, '0')                    AS customer_code,
  COALESCE(NULLIF(product_id, '')::int,
           CASE price WHEN 430 THEN 101 WHEN 750 THEN 102 WHEN 115 THEN 103
                      WHEN 620 THEN 104 WHEN 1400 THEN 105 WHEN 1150 THEN 106
                      WHEN 380 THEN 107 WHEN 290 THEN 108 END) AS product_id,
  (product_id IS NULL OR product_id = '')              AS product_repaired,
  NULLIF(quantity, '')::int * CASE WHEN qty_unit = 'CTN' THEN 10 ELSE 1 END AS quantity,
  price                                                AS unit_price,
  CASE WHEN discount_pct::numeric > 0 AND discount_pct::numeric < 1
       THEN discount_pct::numeric * 100
       ELSE discount_pct::numeric END                  AS discount_pct,
  ms.clean_value                                       AS status,
  NULLIF(TRIM(sales_rep), '')                          AS sales_rep,
  mb.clean_value                                       AS branch,
  entered_at_ist
FROM typed t
LEFT JOIN map_status ms ON ms.raw_value = LOWER(TRIM(t.status))
LEFT JOIN map_branch mb ON mb.raw_value = LOWER(TRIM(t.branch));

CREATE TABLE dq_order_issues AS
SELECT order_item_id, 'quantity missing' AS issue, 'quarantined' AS action
FROM clean_order_lines WHERE quantity IS NULL
UNION ALL
SELECT order_item_id, 'quantity above historical maximum', 'quarantined'
FROM clean_order_lines
WHERE quantity > (SELECT MAX(oi.quantity) FROM order_items oi JOIN orders o USING (order_id)
                  WHERE o.order_date < '2025-10-01')
UNION ALL
SELECT order_item_id, 'impossible or unreadable date', 'repaired from entry time (IST)'
FROM clean_order_lines WHERE date_repaired
UNION ALL
SELECT order_item_id, 'product_id missing', 'repaired from unit price'
FROM clean_order_lines WHERE product_repaired;

CREATE TABLE clean_customers AS
WITH typed AS (
  SELECT LPAD(TRIM(s.customer_code), 4, '0')                      AS customer_code,
         TRIM(regexp_replace(s.customer_name, '\s+', ' ', 'g'))   AS customer_name,
         CASE WHEN mc.raw_value IS NOT NULL THEN mc.clean_value
              WHEN TRIM(s.city) = '' THEN NULL
              ELSE INITCAP(TRIM(s.city)) END                      AS city,
         mg.clean_value                                           AS segment,
         NULLIF(TRIM(s.email), '')                                AS email,
         CASE WHEN s.signup_date ~ '^\d{4}-\d{2}-\d{2}$' THEN to_date(s.signup_date, 'YYYY-MM-DD')
              WHEN s.signup_date ~ '^\d{2}/\d{2}/\d{4}$' THEN to_date(s.signup_date, 'DD/MM/YYYY')
         END                                                      AS signup_date
  FROM stg_customers_raw s
  LEFT JOIN map_city mc    ON mc.raw_value = LOWER(TRIM(s.city))
  LEFT JOIN map_segment mg ON mg.raw_value = LOWER(TRIM(s.segment))
)
SELECT t.*,
       (email IS NOT NULL AND email !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$') AS email_invalid,
       (signup_date > DATE '2025-12-31')                              AS signup_in_future,
       LOWER(regexp_replace(regexp_replace(customer_name,
             '\s+(pvt\.?\s*ltd\.?|private limited)$', '', 'i'), '\s+', ' ', 'g')) AS match_key
FROM typed t;
