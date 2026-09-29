-- Analyst to Architect, Chapter 64, section 64.3: the access-control lab.
-- Run this while connected to the database riverstone_access (create it first:
-- CREATE DATABASE riverstone_access;). It is safe to run again: it starts from nothing.
-- Riverstone Supplies is fictional. The contact names, phone numbers and emails are invented;
-- the phone numbers use the 99999 00xxx pattern and the emails the reserved example.com domain.

DROP TABLE IF EXISTS orders, customers, staff_branch CASCADE;
DROP VIEW IF EXISTS customers_masked;
DROP ROLE IF EXISTS delhi_staff, kolkata_staff, mumbai_staff, branch_staff, analytics;  -- delhi_staff: exercise 13

CREATE TABLE customers (
    customer_id     INTEGER PRIMARY KEY,
    customer_name   VARCHAR(100) NOT NULL,
    contact_person  VARCHAR(60),
    phone           VARCHAR(15),
    email           VARCHAR(80),
    branch          VARCHAR(20)  NOT NULL
);

CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    branch       VARCHAR(20)   NOT NULL,
    order_date   DATE          NOT NULL,
    amount       NUMERIC(10,2) NOT NULL
);

-- which branch each branch-staff role belongs to (used by the row-level security policy)
CREATE TABLE staff_branch (
    role_name  VARCHAR(40) PRIMARY KEY,
    branch     VARCHAR(20) NOT NULL
);

INSERT INTO customers VALUES
 (1, 'Sharma Hardware',    'Ramesh Sharma',  '99999 00101', 'ramesh@sharma.example.com',   'Mumbai HO'),
 (2, 'Metro Mart',         'Neha Kulkarni',  '99999 00102', 'neha@metromart.example.com',  'Mumbai HO'),
 (3, 'Coastal Foods',      'Arvind Pillai',  '99999 00103', 'arvind@coastal.example.com',  'Bengaluru'),
 (4, 'Capital Stores',     'Pooja Malhotra', '99999 00104', 'pooja@capital.example.com',   'Delhi'),
 (5, 'Howrah Home Stores', 'Sourav Das',     '99999 00105', 'sourav@howrah.example.com',   'Kolkata'),
 (6, 'Salt Lake Caterers', 'Moumita Ghosh',  '99999 00106', 'moumita@saltlake.example.com','Kolkata');

INSERT INTO orders VALUES
 (9001, 1, 'Mumbai HO', '2026-03-02', 18400.00),
 (9002, 2, 'Mumbai HO', '2026-03-02',  7250.00),
 (9003, 3, 'Bengaluru', '2026-03-03', 12900.00),
 (9004, 4, 'Delhi',     '2026-03-03',  5600.00),
 (9005, 5, 'Kolkata',   '2026-03-04',  9800.00),
 (9006, 6, 'Kolkata',   '2026-03-04',  4350.00),
 (9007, 1, 'Mumbai HO', '2026-03-05', 21100.00),
 (9008, 5, 'Kolkata',   '2026-03-05',  6150.00);

INSERT INTO staff_branch VALUES
 ('kolkata_staff', 'Kolkata'),
 ('mumbai_staff',  'Mumbai HO');
