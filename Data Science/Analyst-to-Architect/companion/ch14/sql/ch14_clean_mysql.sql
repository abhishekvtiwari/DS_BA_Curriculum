-- Analyst to Architect, Chapter 14 — the cleaning pipeline (MySQL 8.0+). Run after ch14_load_mysql.sql.
DROP TABLE IF EXISTS clean_order_lines, dq_order_issues, clean_customers;

CREATE TABLE clean_order_lines AS
WITH data_rows AS (
  SELECT * FROM stg_orders_raw WHERE order_item_id REGEXP '^[0-9]+$'
), deduped AS (
  SELECT DISTINCT * FROM data_rows
), parts AS (
  SELECT d.*,
    CASE WHEN order_date REGEXP '^[0-9]{2}[-/][0-9]{2}[-/][0-9]{4}$' THEN CAST(SUBSTR(order_date,7,4) AS UNSIGNED)
         WHEN order_date REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'       THEN CAST(SUBSTR(order_date,1,4) AS UNSIGNED) END AS y,
    CASE WHEN order_date REGEXP '^[0-9]{2}[-/][0-9]{2}[-/][0-9]{4}$' THEN CAST(SUBSTR(order_date,4,2) AS UNSIGNED)
         WHEN order_date REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'       THEN CAST(SUBSTR(order_date,6,2) AS UNSIGNED) END AS m,
    CASE WHEN order_date REGEXP '^[0-9]{2}[-/][0-9]{2}[-/][0-9]{4}$' THEN CAST(SUBSTR(order_date,1,2) AS UNSIGNED)
         WHEN order_date REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'       THEN CAST(SUBSTR(order_date,9,2) AS UNSIGNED) END AS dd,
    STR_TO_DATE(entered_at_utc, '%Y-%m-%dT%H:%i:%sZ') + INTERVAL 330 MINUTE AS entered_at_ist
  FROM deduped d
), typed AS (
  SELECT p.*,
    CASE WHEN order_date REGEXP '^[0-9]{5}$' THEN DATE '1899-12-30' + INTERVAL CAST(order_date AS UNSIGNED) DAY
         WHEN y IS NOT NULL AND m BETWEEN 1 AND 12 AND dd >= 1
              AND MONTH(MAKEDATE(y, 1) + INTERVAL (m - 1) MONTH + INTERVAL (dd - 1) DAY) = m
         THEN MAKEDATE(y, 1) + INTERVAL (m - 1) MONTH + INTERVAL (dd - 1) DAY END AS parsed_date
  FROM parts p
)
SELECT
  CAST(order_item_id AS UNSIGNED)                          AS order_item_id,
  CAST(order_id AS UNSIGNED)                               AS order_id,
  COALESCE(parsed_date, DATE(entered_at_ist))              AS order_date,
  (parsed_date IS NULL)                                    AS date_repaired,
  LPAD(TRIM(customer_code), 4, '0')                        AS customer_code,
  COALESCE(CAST(NULLIF(product_id,'') AS UNSIGNED),
           CASE CAST(REPLACE(REGEXP_REPLACE(unit_price, '^[^0-9]+', ''), ',', '') AS DECIMAL(10,2))
                WHEN 430 THEN 101 WHEN 750 THEN 102 WHEN 115 THEN 103 WHEN 620 THEN 104
                WHEN 1400 THEN 105 WHEN 1150 THEN 106 WHEN 380 THEN 107 WHEN 290 THEN 108 END) AS product_id,
  (product_id IS NULL OR product_id = '')                  AS product_repaired,
  CAST(NULLIF(quantity,'') AS UNSIGNED) * CASE WHEN qty_unit = 'CTN' THEN 10 ELSE 1 END AS quantity,
  CAST(REPLACE(REGEXP_REPLACE(unit_price, '^[^0-9]+', ''), ',', '') AS DECIMAL(10,2)) AS unit_price,
  CASE WHEN CAST(discount_pct AS DECIMAL(6,3)) > 0 AND CAST(discount_pct AS DECIMAL(6,3)) < 1
       THEN CAST(discount_pct AS DECIMAL(6,3)) * 100 ELSE CAST(discount_pct AS DECIMAL(6,3)) END AS discount_pct,
  ms.clean_value                                           AS status,
  NULLIF(TRIM(sales_rep), '')                              AS sales_rep,
  mb.clean_value                                           AS branch,
  entered_at_ist
FROM typed t
LEFT JOIN map_status ms ON ms.raw_value = LOWER(TRIM(t.status))
LEFT JOIN map_branch mb ON mb.raw_value = LOWER(TRIM(t.branch));

CREATE TABLE dq_order_issues AS
SELECT order_item_id, 'quantity missing' AS issue, 'quarantined' AS action FROM clean_order_lines WHERE quantity IS NULL
UNION ALL
SELECT order_item_id, 'quantity above historical maximum', 'quarantined'
FROM clean_order_lines WHERE quantity > (SELECT MAX(oi.quantity) FROM order_items oi JOIN orders o ON o.order_id = oi.order_id WHERE o.order_date < '2025-10-01')
UNION ALL
SELECT order_item_id, 'impossible or unreadable date', 'repaired from entry time (IST)' FROM clean_order_lines WHERE date_repaired
UNION ALL
SELECT order_item_id, 'product_id missing', 'repaired from unit price' FROM clean_order_lines WHERE product_repaired;

CREATE TABLE clean_customers AS
WITH typed AS (
  SELECT LPAD(TRIM(s.customer_code),4,'0') AS customer_code,
         TRIM(REGEXP_REPLACE(s.customer_name, '[[:space:]]+', ' ')) AS customer_name,
         CASE WHEN mc.raw_value IS NOT NULL THEN mc.clean_value
              WHEN TRIM(s.city) = '' THEN NULL
              ELSE CONCAT(UPPER(LEFT(TRIM(s.city),1)), LOWER(SUBSTR(TRIM(s.city),2))) END AS city,
         mg.clean_value AS segment,
         NULLIF(TRIM(s.email),'') AS email,
         CASE WHEN s.signup_date REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN STR_TO_DATE(s.signup_date,'%Y-%m-%d')
              WHEN s.signup_date REGEXP '^[0-9]{2}/[0-9]{2}/[0-9]{4}$' THEN STR_TO_DATE(s.signup_date,'%d/%m/%Y') END AS signup_date
  FROM stg_customers_raw s
  LEFT JOIN map_city mc ON mc.raw_value = LOWER(TRIM(s.city))
  LEFT JOIN map_segment mg ON mg.raw_value = LOWER(TRIM(s.segment))
)
SELECT t.*,
       (email IS NOT NULL AND email NOT REGEXP '^[^@[:space:]]+@[^@[:space:]]+\\.[^@[:space:]]+$') AS email_invalid,
       (signup_date > DATE '2025-12-31') AS signup_in_future,
       LOWER(REGEXP_REPLACE(REGEXP_REPLACE(customer_name, '[[:space:]]+(pvt\\.?[[:space:]]*ltd\\.?|private limited)$', ''), '[[:space:]]+', ' ')) AS match_key
FROM typed t;
