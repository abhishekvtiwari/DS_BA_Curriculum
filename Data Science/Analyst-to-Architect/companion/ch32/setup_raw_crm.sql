-- setup_raw_crm.sql - stands in for the CRM's nightly customer extract (Chapter 32).
-- It copies today's customer details into their own schema, the way a loading tool would.
CREATE SCHEMA raw_crm;

CREATE TABLE raw_crm.customers AS
SELECT customer_id, customer_name, city, segment
FROM public.customers;
