-- Analyst to Architect · Chapter 28 · Advanced SQL, Performance & Data Modeling
-- File: ch28_2025_addons.sql (PostgreSQL)
-- What: adds three tables to the one-year database riverstone_2025:
--         staff             the company's reporting lines (from the HRMS), 35 people, for recursive CTEs (section 28.2)
--         parts, bom_lines  a bill of materials for five products (section 28.2)
--         customer_changes  the ERP's audit log of customer city/segment changes in 2025 (section 28.10)
-- How:  run riverstone_2025_setup.sql first, then:  psql -d riverstone_2025 -f ch28_2025_addons.sql
-- Tested on: PostgreSQL 16 (Ubuntu 24.04). Safe to re-run (drops and recreates its own tables).
-- Riverstone Supplies is fictional; every name and number is invented.

DROP TABLE IF EXISTS customer_changes, bom_lines, parts, staff;

-- One row = one person on the payroll. employee_id links the five sales people to the ERP's employees table.
CREATE TABLE staff (
    staff_id     INTEGER PRIMARY KEY,
    staff_name   VARCHAR(100) NOT NULL,
    job_title    VARCHAR(60)  NOT NULL,
    department   VARCHAR(40)  NOT NULL,
    location     VARCHAR(40)  NOT NULL,
    manager_id   INTEGER REFERENCES staff(staff_id),
    employee_id  INTEGER REFERENCES employees(employee_id)
);

INSERT INTO staff VALUES
(100, 'Arvind Kapoor',   'Managing Director',             'Management',          'Head office',  NULL, NULL),
(110, 'Anita Rao',       'Sales Head',                    'Sales',               'Head office',  100,  1),
(120, 'Suresh Menon',    'Finance Manager',               'Finance',             'Head office',  100,  NULL),
(130, 'Harpreet Sethi',  'Head of Production',            'Production',          'Taloja',       100,  NULL),
(140, 'Joseph D''Souza', 'Purchasing Manager',            'Purchasing',          'Head office',  100,  NULL),
(150, 'Mahesh Yadav',    'Warehouse & Dispatch Manager',  'Warehouse',           'Bhiwandi Main',100,  NULL),
(160, 'Lakshmi Reddy',   'HR Manager',                    'HR',                  'Head office',  100,  NULL),
(170, 'Zoya Mirza',      'Marketing Manager',             'Marketing',           'Head office',  100,  NULL),
(180, 'Tenzin Dorji',    'Customer Support Lead',         'Customer support',    'Head office',  100,  NULL),
(111, 'Vikram Singh',    'Sales Manager, Key Accounts',   'Sales',               'Head office',  110,  2),
(112, 'Farah Khan',      'Sales Executive',               'Sales',               'Head office',  110,  5),
(113, 'Meera Iyer',      'Sales Coordinator',             'Sales',               'Head office',  110,  NULL),
(114, 'Neha Kulkarni',   'Sales Executive',               'Sales',               'Head office',  111,  3),
(115, 'Rahul Mehta',     'Sales Executive',               'Sales',               'Head office',  111,  4),
(121, 'Priya Nambiar',   'Accounts Executive',            'Finance',             'Head office',  120,  NULL),
(131, 'Ramesh Patil',    'Plant Manager, Taloja',         'Production',          'Taloja',       130,  NULL),
(132, 'Kiran Bhosale',   'Plant Manager, Chakan',         'Production',          'Chakan',       130,  NULL),
(133, 'Ajay Kumar',      'Shift Supervisor',              'Production',          'Taloja',       131,  NULL),
(134, 'Farhan Ali',      'Quality Inspector',             'Production',          'Taloja',       131,  NULL),
(135, 'Swati Joshi',     'Shift Supervisor',              'Production',          'Chakan',       132,  NULL),
(136, 'Gopal Sahu',      'Machine Operator',              'Production',          'Taloja',       133,  NULL),
(137, 'Sunita Pawar',    'Machine Operator',              'Production',          'Taloja',       133,  NULL),
(138, 'Farid Shaikh',    'Machine Operator',              'Production',          'Chakan',       135,  NULL),
(151, 'Mohan Das',       'Dispatch Supervisor',           'Warehouse',           'Bhiwandi Main',150,  NULL),
-- Regional sales: three regional managers and their executives, serving the customers outside the key accounts.
(116, 'Arjun Nair',      'Regional Sales Manager, South', 'Sales',               'Head office',  110,  NULL),
(117, 'Pooja Desai',     'Regional Sales Manager, West',  'Sales',               'Head office',  110,  NULL),
(118, 'Sandeep Gill',    'Regional Sales Manager, North', 'Sales',               'Head office',  110,  NULL),
(161, 'Divya Krishnan',  'Sales Executive',               'Sales',               'Head office',  116,  NULL),
(162, 'Vivek Chandran',  'Sales Executive',               'Sales',               'Head office',  116,  NULL),
(163, 'Sneha Pillai',    'Sales Executive',               'Sales',               'Head office',  116,  NULL),
(171, 'Nisha Bhatt',     'Sales Executive',               'Sales',               'Head office',  117,  NULL),
(172, 'Aditya Verma',    'Sales Executive',               'Sales',               'Head office',  117,  NULL),
(173, 'Rohit Kamat',     'Sales Executive',               'Sales',               'Head office',  117,  NULL),
(181, 'Karan Ahuja',     'Sales Executive',               'Sales',               'Head office',  118,  NULL),
(182, 'Ritu Bansal',     'Sales Executive',               'Sales',               'Head office',  118,  NULL);

-- One row = one part: a finished product (same id as products), a made-in-house assembly, or a bought material.
CREATE TABLE parts (
    part_id        INTEGER PRIMARY KEY,
    part_name      VARCHAR(60)  NOT NULL,
    part_type      VARCHAR(10)  NOT NULL CHECK (part_type IN ('Product', 'Assembly', 'Material')),
    unit           VARCHAR(5)   NOT NULL,
    material_cost  NUMERIC(10,2),          -- cost per unit, bought materials only
    supplier_name  VARCHAR(60)
);

INSERT INTO parts VALUES
(101, 'Storage Box 10L',     'Product',  'each', NULL,   NULL),
(102, 'Storage Box 25L',     'Product',  'each', NULL,   NULL),
(104, 'Food Container Set',  'Product',  'each', NULL,   NULL),
(106, 'Garden Chair',        'Product',  'each', NULL,   NULL),
(108, 'Stackable Bin',       'Product',  'each', NULL,   NULL),
(201, 'Box body 10L',        'Assembly', 'each', NULL,   NULL),
(202, 'Lid 10L',             'Assembly', 'each', NULL,   NULL),
(203, 'Box body 25L',        'Assembly', 'each', NULL,   NULL),
(204, 'Lid 25L',             'Assembly', 'each', NULL,   NULL),
(205, 'Container 500ml',     'Assembly', 'each', NULL,   NULL),
(206, 'Lid 500ml',           'Assembly', 'each', NULL,   NULL),
(207, 'Seat shell',          'Assembly', 'each', NULL,   NULL),
(208, 'Steel frame',         'Assembly', 'each', NULL,   NULL),
(209, 'Leg assembly',        'Assembly', 'each', NULL,   NULL),
(301, 'Polypropylene granules', 'Material', 'kg',   110.00, 'Western Polymers'),
(302, 'Color masterbatch',   'Material', 'kg',   260.00, 'Gujarat Pigments'),
(303, 'Product label',       'Material', 'each',   2.00, 'Sagar Labels'),
(304, 'Shipping carton',     'Material', 'each',  18.00, 'Deccan Cartons'),
(305, 'Steel tube',          'Material', 'kg',    95.00, 'Kaveri Steel Works'),
(306, 'Fastener pack',       'Material', 'each',  14.00, 'Kaveri Steel Works');

-- One row = "one unit of parent needs quantity units of child".
CREATE TABLE bom_lines (
    parent_part_id  INTEGER NOT NULL REFERENCES parts(part_id),
    child_part_id   INTEGER NOT NULL REFERENCES parts(part_id),
    quantity        NUMERIC(8,3) NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (parent_part_id, child_part_id)
);

INSERT INTO bom_lines VALUES
(101, 201, 1), (101, 202, 1), (101, 303, 1), (101, 304, 1),
(201, 301, 0.550), (201, 302, 0.020),
(202, 301, 0.200), (202, 302, 0.010),
(102, 203, 1), (102, 204, 1), (102, 303, 1), (102, 304, 1),
(203, 301, 1.100), (203, 302, 0.040),
(204, 301, 0.400), (204, 302, 0.015),
(104, 205, 3), (104, 206, 3), (104, 303, 1), (104, 304, 1),
(205, 301, 0.080), (205, 302, 0.003),
(206, 301, 0.030), (206, 302, 0.001),
(106, 207, 1), (106, 208, 1), (106, 303, 1), (106, 304, 1),
(207, 301, 2.200), (207, 302, 0.080),
(208, 209, 2), (208, 305, 1.000), (208, 306, 1),
(209, 305, 1.200), (209, 306, 1),
(108, 301, 0.450), (108, 302, 0.015), (108, 303, 1);

-- One row = one change to one customer attribute, as recorded by the ERP. customers holds the values after all changes.
CREATE TABLE customer_changes (
    change_id    INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    changed_on   DATE NOT NULL,
    column_name  VARCHAR(20) NOT NULL,
    old_value    VARCHAR(50) NOT NULL,
    new_value    VARCHAR(50) NOT NULL
);

INSERT INTO customer_changes VALUES
(1, 2,  '2025-04-01', 'segment', 'Wholesale', 'Retail'),
(2, 5,  '2025-07-01', 'city',    'Thane',     'Mumbai'),
(3, 11, '2025-09-01', 'segment', 'Retail',    'Wholesale');
