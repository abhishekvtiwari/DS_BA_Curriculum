-- Analyst to Architect, Chapter 14 — terminal version of ch14_load_mysql.sql (LOAD DATA LOCAL INFILE reads the CSV files).
-- Run from companion/ch14:  mysql --local-infile=1 -u root -p riverstone_full < sql/terminal/ch14_load_mysql.sql
-- (server, once: SET GLOBAL local_infile = 1;). The exports have Windows line endings (\r\n).
DROP TABLE IF EXISTS stg_orders_raw, stg_customers_raw, map_status, map_branch, map_city, map_segment, truth_order_lines;
CREATE TABLE stg_orders_raw (
  order_item_id VARCHAR(20), order_id VARCHAR(20), order_date VARCHAR(20), customer_code VARCHAR(20), product_id VARCHAR(20),
  quantity VARCHAR(20), qty_unit VARCHAR(10), unit_price VARCHAR(30), discount_pct VARCHAR(20), status VARCHAR(30),
  sales_rep VARCHAR(100), branch VARCHAR(50), entered_at_utc VARCHAR(80)) CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'orders_q4_2025_export.csv' INTO TABLE stg_orders_raw CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;
CREATE TABLE stg_customers_raw (customer_code VARCHAR(20), customer_name VARCHAR(150), city VARCHAR(80), segment VARCHAR(40),
  email VARCHAR(150), signup_date VARCHAR(20)) CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'customers_crm_export.csv' INTO TABLE stg_customers_raw CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;
CREATE TABLE map_status (raw_value VARCHAR(30) PRIMARY KEY, clean_value VARCHAR(30) NOT NULL);
CREATE TABLE map_branch (raw_value VARCHAR(50) PRIMARY KEY, clean_value VARCHAR(50) NOT NULL);
CREATE TABLE map_city (raw_value VARCHAR(80) PRIMARY KEY, clean_value VARCHAR(80));
CREATE TABLE map_segment (raw_value VARCHAR(40) PRIMARY KEY, clean_value VARCHAR(40) NOT NULL);
INSERT INTO map_status VALUES ('delivered','Delivered'),('dlvd','Delivered'),('cancelled','Cancelled'),('canceled','Cancelled'),
  ('cxl','Cancelled'),('shipped','Shipped'),('pending','Pending');
INSERT INTO map_branch VALUES ('mumbai ho','Mumbai HO'),('mumbai h.o.','Mumbai HO'),('mumbai','Mumbai HO'),('bengaluru','Bengaluru'),
  ('bangalore','Bengaluru'),('blr','Bengaluru'),('delhi','Delhi'),('new delhi','Delhi'),('del','Delhi'),('kolkata','Kolkata'),
  ('calcutta','Kolkata'),('kol','Kolkata');
INSERT INTO map_city VALUES ('bombay','Mumbai'),('bangalore','Bengaluru'),('gurgaon','Gurugram'),('calcutta','Kolkata'),
  ('madras','Chennai'),('trivandrum','Thiruvananthapuram'),('vizag','Visakhapatnam'),('mysore','Mysuru'),('new delhi','Delhi'),
  ('poona','Pune'),('n/a',NULL),('-',NULL),('unknown',NULL),('null',NULL);
INSERT INTO map_segment VALUES ('retail','Retail'),('hospitality','Hospitality'),('hotel/restaurant','Hospitality'),('horeca','Hospitality'),
  ('wholesale','Wholesale'),('distributor','Wholesale');
CREATE TABLE truth_order_lines (order_item_id INTEGER PRIMARY KEY, order_id INTEGER, order_date DATE, customer_code VARCHAR(4),
  product_id INTEGER, quantity INTEGER, unit_price DECIMAL(10,2), discount_pct DECIMAL(5,2), status VARCHAR(20), sales_rep VARCHAR(100),
  branch VARCHAR(20), entered_at_utc DATETIME, net_revenue DECIMAL(14,2)) CHARACTER SET utf8mb4;
LOAD DATA LOCAL INFILE 'clean_truth_orders_q4_2025.csv' INTO TABLE truth_order_lines CHARACTER SET utf8mb4
  FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 LINES
  (order_item_id, order_id, @d, customer_code, product_id, quantity, unit_price, discount_pct, status, @rep, branch, entered_at_utc, net_revenue)
  SET order_date = DATE(@d), sales_rep = NULLIF(@rep, '');
