-- =====================================================================
-- Analyst to Architect · Chapter 12 · Section 12.13 lab, PostgreSQL version
-- Every statement from "Building and changing a database" and exercises 23-27, in book order.
-- Built from the chapter by sql/ch12_lab_companion.py; don't edit by hand.
-- Run it with psql:   psql -U postgres -d postgres -f ch12_lab_postgresql.sql
-- In DBeaver: run the CREATE DATABASE statement, connect to riverstone_lab, then run the rest
-- (skip the \c line, which only psql understands).
-- Statements that fail on purpose in the book are commented out, with the error you'd see.
-- Riverstone Supplies is fictional; every name and number is invented.
-- =====================================================================

DROP DATABASE IF EXISTS riverstone_lab;

-- Step 1: Create the database
CREATE DATABASE riverstone_lab;
\c riverstone_lab

-- Step 1: Create the database
SELECT datname
FROM pg_database
WHERE datname LIKE 'riverstone%'
ORDER BY datname;

-- Step 3: CREATE TABLE
CREATE TABLE suppliers (
    supplier_id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_name  VARCHAR(100) NOT NULL UNIQUE,
    city           VARCHAR(50),
    contact_email  VARCHAR(100),
    fax_number     VARCHAR(20),
    rating         SMALLINT CHECK (rating BETWEEN 1 AND 5),
    is_active      BOOLEAN NOT NULL DEFAULT TRUE,
    onboarded_on   DATE NOT NULL
);

-- Step 3: CREATE TABLE
CREATE TABLE purchase_orders (
    po_id        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    supplier_id  INTEGER NOT NULL,
    po_date      DATE NOT NULL,
    item         VARCHAR(100) NOT NULL,
    quantity     INTEGER NOT NULL CHECK (quantity > 0),
    unit_cost    NUMERIC(10,2) NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'Open',
    FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
);

-- Step 3: CREATE TABLE
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'suppliers'
ORDER BY ordinal_position;

-- Step 4: INSERT: adding rows
INSERT INTO suppliers (supplier_name, city, contact_email, rating, onboarded_on)
VALUES ('Western Polymers', 'Vapi', 'sales@westernpolymers.example', 4, '2025-06-01');

-- Step 4: INSERT: adding rows
INSERT INTO suppliers (supplier_name, city, contact_email, rating, onboarded_on)
VALUES ('Deccan Cartons',     'Pune',       'sales@deccancartons.example', 3,    '2025-08-15'),
       ('Kaveri Steel Works', 'Coimbatore', NULL,                          5,    '2025-09-10'),
       ('Sagar Labels',       'Mumbai',     'orders@sagarlabels.example',  NULL, '2026-01-05');

-- Step 4: INSERT: adding rows
SELECT supplier_id, supplier_name, city, rating, is_active, onboarded_on
FROM suppliers
ORDER BY supplier_id;

-- Step 4: INSERT: adding rows
INSERT INTO purchase_orders (supplier_id, po_date, item, quantity, unit_cost)
VALUES (1, '2026-03-02', 'Polypropylene granules (kg)', 2000, 118.50),
       (1, '2026-03-16', 'Polypropylene granules (kg)', 1500, 121.00),
       (2, '2026-03-05', 'Cardboard cartons',            800,  22.00),
       (3, '2026-03-09', 'Steel handles',                500,  14.75),
       (4, '2026-03-20', 'Printed labels',              3000,   1.20);

-- When the database says no
-- Fails on purpose: ERROR:  null value in column "supplier_name" of relation "suppliers" violates not-null constraint
-- INSERT INTO suppliers (city, onboarded_on)
-- VALUES ('Surat', '2026-02-01');

-- When the database says no
-- Fails on purpose: ERROR:  duplicate key value violates unique constraint "suppliers_supplier_name_key"
-- INSERT INTO suppliers (supplier_name, city, onboarded_on)
-- VALUES ('Deccan Cartons', 'Nashik', '2026-02-01');

-- When the database says no
-- Fails on purpose: ERROR:  new row for relation "suppliers" violates check constraint "suppliers_rating_check"
-- INSERT INTO suppliers (supplier_name, city, rating, onboarded_on)
-- VALUES ('Gujarat Pigments', 'Ahmedabad', 7, '2026-02-01');

-- When the database says no
-- Fails on purpose: ERROR:  insert or update on table "purchase_orders" violates foreign key constraint "purchase_orders_supplier_id_fkey"
-- INSERT INTO purchase_orders (supplier_id, po_date, item, quantity, unit_cost)
-- VALUES (99, '2026-03-21', 'Lids', 100, 9.00);

-- When the database says no
INSERT INTO suppliers (supplier_name, city, rating, onboarded_on)
VALUES ('Gujarat Pigments', 'Ahmedabad', 4, '2026-02-01');

-- When the database says no
SELECT supplier_id, supplier_name
FROM suppliers
ORDER BY supplier_id;

-- When the database says no
INSERT INTO suppliers (supplier_name, city, onboarded_on)
VALUES ('Nilgiri Packaging', 'Ooty', '2026-03-01')
RETURNING supplier_id;

-- Step 5: UPDATE: changing rows
SELECT supplier_id, supplier_name, rating
FROM suppliers
WHERE supplier_name = 'Sagar Labels';

-- Step 5: UPDATE: changing rows
UPDATE suppliers
SET rating = 4
WHERE supplier_name = 'Sagar Labels';

-- Step 5: UPDATE: changing rows
UPDATE purchase_orders
SET unit_cost = ROUND(unit_cost * 1.05, 2)
WHERE supplier_id = 1
  AND status = 'Open';

-- Step 5: UPDATE: changing rows
UPDATE purchase_orders AS po
SET status = 'On hold'
FROM suppliers AS s
WHERE po.supplier_id = s.supplier_id
  AND s.rating < 4
  AND po.status = 'Open';

-- Step 5: UPDATE: changing rows
UPDATE purchase_orders
SET status = 'Received'
WHERE po_id = 1;

-- Step 5: UPDATE: changing rows
SELECT po_id, supplier_id, item, unit_cost, status
FROM purchase_orders
ORDER BY po_id;

-- Step 6: DELETE: removing rows
DELETE FROM purchase_orders
WHERE po_id = 5;

-- Step 6: DELETE: removing rows
SELECT COUNT(*) AS orders_left
FROM purchase_orders;

-- Step 6: DELETE: removing rows
-- Fails on purpose: ERROR:  update or delete on table "suppliers" violates foreign key constraint "purchase_orders_supplier_id_fkey" on table "purchase_orders"
-- DELETE FROM suppliers
-- WHERE supplier_name = 'Western Polymers';

-- Step 6: DELETE: removing rows
UPDATE suppliers
SET is_active = FALSE
WHERE supplier_name = 'Nilgiri Packaging';

-- Step 6: DELETE: removing rows
SELECT supplier_name, is_active
FROM suppliers
WHERE supplier_name = 'Nilgiri Packaging';

-- Step 7: Insert or update in one statement (upsert)
INSERT INTO suppliers (supplier_name, city, contact_email, onboarded_on)
VALUES ('Deccan Cartons', 'Pune', 'accounts@deccancartons.example', '2025-08-15')
ON CONFLICT (supplier_name)
DO UPDATE SET contact_email = EXCLUDED.contact_email;

-- Step 7: Insert or update in one statement (upsert)
SELECT supplier_name, city, contact_email, rating, is_active
FROM suppliers
ORDER BY supplier_name;

-- Step 8: Transactions: the undo button
BEGIN;
DELETE FROM purchase_orders WHERE status = 'Open';
SELECT COUNT(*) AS orders_left FROM purchase_orders;
ROLLBACK;
SELECT COUNT(*) AS orders_left FROM purchase_orders;

-- Step 8: Transactions: the undo button
BEGIN;
ALTER TABLE suppliers ADD COLUMN notes TEXT;
ROLLBACK;
SELECT COUNT(*) AS notes_column_exists
FROM information_schema.columns
WHERE table_name = 'suppliers' AND column_name = 'notes';

-- Step 9: ALTER TABLE: changing the structure
CREATE TABLE suppliers_backup AS
SELECT * FROM suppliers;

-- Step 9: ALTER TABLE: changing the structure
SELECT COUNT(*) AS rows_copied FROM suppliers_backup;

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE suppliers ADD COLUMN gst_number VARCHAR(15);

-- Step 9: ALTER TABLE: changing the structure
UPDATE suppliers SET gst_number = '24AAACW1234A1Z5' WHERE supplier_name = 'Western Polymers';
UPDATE suppliers SET gst_number = '27AAACD5678B1Z2' WHERE supplier_name = 'Deccan Cartons';

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE suppliers
ADD CONSTRAINT uq_suppliers_gst UNIQUE (gst_number);

-- Step 9: ALTER TABLE: changing the structure
-- Fails on purpose: ERROR:  duplicate key value violates unique constraint "uq_suppliers_gst"
-- UPDATE suppliers
-- SET gst_number = '24AAACW1234A1Z5'
-- WHERE supplier_name = 'Sagar Labels';

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE suppliers RENAME COLUMN contact_email TO email;

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE suppliers DROP COLUMN fax_number;

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE suppliers ALTER COLUMN city TYPE VARCHAR(80);

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE purchase_orders ALTER COLUMN status TYPE VARCHAR(30);

-- Step 9: ALTER TABLE: changing the structure
SELECT column_name, character_maximum_length, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'purchase_orders' AND column_name = 'status';

-- Step 9: ALTER TABLE: changing the structure
-- Fails on purpose: ERROR:  column "email" of relation "suppliers" contains null values
-- ALTER TABLE suppliers ALTER COLUMN email SET NOT NULL;

-- Step 9: ALTER TABLE: changing the structure
UPDATE suppliers SET email = 'info@kaveristeel.example'      WHERE supplier_name = 'Kaveri Steel Works';
UPDATE suppliers SET email = 'hello@gujaratpigments.example' WHERE supplier_name = 'Gujarat Pigments';
UPDATE suppliers SET email = 'contact@nilgiripack.example'   WHERE supplier_name = 'Nilgiri Packaging';

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE suppliers ALTER COLUMN email SET NOT NULL;

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE purchase_orders
ADD CONSTRAINT chk_po_status
CHECK (status IN ('Open', 'On hold', 'Received', 'Cancelled'));

-- Step 9: ALTER TABLE: changing the structure
-- Fails on purpose: ERROR:  new row for relation "purchase_orders" violates check constraint "chk_po_status"
-- UPDATE purchase_orders
-- SET status = 'Shipped'
-- WHERE po_id = 2;

-- Step 9: ALTER TABLE: changing the structure
ALTER TABLE purchase_orders ALTER COLUMN status SET DEFAULT 'Open';

-- Step 9: ALTER TABLE: changing the structure
SELECT column_name, data_type, character_maximum_length AS max_length, is_nullable
FROM information_schema.columns
WHERE table_name = 'suppliers'
ORDER BY ordinal_position;

-- Step 10: Rename tables and organize them
ALTER TABLE suppliers_backup RENAME TO suppliers_backup_2026_03_31;

-- Step 10: Rename tables and organize them
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Step 10: Rename tables and organize them
CREATE SCHEMA archive;
ALTER TABLE suppliers_backup_2026_03_31 SET SCHEMA archive;
SELECT COUNT(*) AS archived_rows FROM archive.suppliers_backup_2026_03_31;

-- Step 11: Empty and remove: TRUNCATE, DROP TABLE, DROP DATABASE
CREATE TABLE po_import_staging AS
SELECT * FROM purchase_orders;

-- Step 11: Empty and remove: TRUNCATE, DROP TABLE, DROP DATABASE
TRUNCATE TABLE po_import_staging;

-- Step 11: Empty and remove: TRUNCATE, DROP TABLE, DROP DATABASE
SELECT COUNT(*) AS rows_left FROM po_import_staging;

-- Step 11: Empty and remove: TRUNCATE, DROP TABLE, DROP DATABASE
DROP TABLE po_import_staging;

-- Step 11: Empty and remove: TRUNCATE, DROP TABLE, DROP DATABASE
-- Fails on purpose: ERROR:  cannot drop table suppliers because other objects depend on it
-- DROP TABLE suppliers;

-- Step 11: Empty and remove: TRUNCATE, DROP TABLE, DROP DATABASE
DROP TABLE IF EXISTS purchase_orders;
DROP TABLE IF EXISTS suppliers;

-- Step 11: Empty and remove: TRUNCATE, DROP TABLE, DROP DATABASE
DROP SCHEMA archive CASCADE;

-- Exercise 23
CREATE TABLE warehouses (
    warehouse_id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    warehouse_name  VARCHAR(100) NOT NULL UNIQUE,
    city            VARCHAR(50)  NOT NULL,
    capacity_units  INTEGER      NOT NULL CONSTRAINT chk_capacity CHECK (capacity_units > 0),
    opened_on       DATE
);

-- Exercise 24
INSERT INTO warehouses (warehouse_name, city, capacity_units, opened_on)
VALUES ('Bhiwandi Main', 'Bhiwandi', 12000, '2021-04-01'),
       ('Chakan',        'Pune',      8000, '2023-07-15'),
       ('Sriperumbudur', 'Chennai',   6000, NULL);

-- Exercise 24
SELECT * FROM warehouses ORDER BY warehouse_id;

-- Exercise 25
SELECT warehouse_id, warehouse_name, capacity_units
FROM warehouses
WHERE city = 'Chennai';

-- Exercise 25
UPDATE warehouses
SET capacity_units = capacity_units * 1.25
WHERE city = 'Chennai';

UPDATE warehouses
SET warehouse_name = 'Chakan Plant 2'
WHERE warehouse_name = 'Chakan';

-- Exercise 25
SELECT * FROM warehouses ORDER BY warehouse_id;

-- Exercise 26
ALTER TABLE warehouses ADD COLUMN manager_email VARCHAR(100);
ALTER TABLE warehouses RENAME COLUMN capacity_units TO capacity_boxes;
ALTER TABLE warehouses ALTER COLUMN city TYPE VARCHAR(80);

-- Exercise 27
DELETE FROM warehouses
WHERE warehouse_id = 3;

SELECT warehouse_id, warehouse_name, capacity_boxes
FROM warehouses
ORDER BY warehouse_id;

-- Exercise 27
DROP TABLE warehouses;

-- When you've finished the lab (PostgreSQL: connect to another database first):
-- DROP DATABASE IF EXISTS riverstone_lab;
