-- Analyst to Architect, Chapter 14 — load the messy exports into riverstone_full (PostgreSQL 16+).
-- Run from companion/ch14 (the folder with the CSV files):  psql -d riverstone_full -f sql/ch14_load_postgresql.sql
-- Every column is loaded as text first: a staging table must accept anything the export contains.
-- Riverstone Supplies is fictional; every name and number is invented.
DROP TABLE IF EXISTS stg_orders_raw, stg_customers_raw, map_status, map_branch, map_city, map_segment;
CREATE TABLE stg_orders_raw (
  order_item_id TEXT, order_id TEXT, order_date TEXT, customer_code TEXT, product_id TEXT, quantity TEXT,
  qty_unit TEXT, unit_price TEXT, discount_pct TEXT, status TEXT, sales_rep TEXT, branch TEXT, entered_at_utc TEXT);
\copy stg_orders_raw FROM 'orders_q4_2025_export.csv' WITH (FORMAT csv, HEADER true)
CREATE TABLE stg_customers_raw (customer_code TEXT, customer_name TEXT, city TEXT, segment TEXT, email TEXT, signup_date TEXT);
\copy stg_customers_raw FROM 'customers_crm_export.csv' WITH (FORMAT csv, HEADER true)
CREATE TABLE map_status (raw_value TEXT PRIMARY KEY, clean_value TEXT NOT NULL);
INSERT INTO map_status VALUES ('delivered','Delivered'),('dlvd','Delivered'),('cancelled','Cancelled'),('canceled','Cancelled'),
  ('cxl','Cancelled'),('shipped','Shipped'),('pending','Pending');
CREATE TABLE map_branch (raw_value TEXT PRIMARY KEY, clean_value TEXT NOT NULL);
INSERT INTO map_branch VALUES ('mumbai ho','Mumbai HO'),('mumbai h.o.','Mumbai HO'),('mumbai','Mumbai HO'),('bengaluru','Bengaluru'),
  ('bangalore','Bengaluru'),('blr','Bengaluru'),('delhi','Delhi'),('new delhi','Delhi'),('del','Delhi'),('kolkata','Kolkata'),
  ('calcutta','Kolkata'),('kol','Kolkata');
CREATE TABLE map_city (raw_value TEXT PRIMARY KEY, clean_value TEXT);
INSERT INTO map_city VALUES ('bombay','Mumbai'),('bangalore','Bengaluru'),('gurgaon','Gurugram'),('calcutta','Kolkata'),
  ('madras','Chennai'),('trivandrum','Thiruvananthapuram'),('vizag','Visakhapatnam'),('mysore','Mysuru'),('new delhi','Delhi'),
  ('poona','Pune'),('n/a',NULL),('-',NULL),('unknown',NULL),('null',NULL);
CREATE TABLE map_segment (raw_value TEXT PRIMARY KEY, clean_value TEXT NOT NULL);
INSERT INTO map_segment VALUES ('retail','Retail'),('hospitality','Hospitality'),('hotel/restaurant','Hospitality'),('horeca','Hospitality'),
  ('wholesale','Wholesale'),('distributor','Wholesale');
