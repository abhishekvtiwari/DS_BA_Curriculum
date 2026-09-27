-- Riverstone Supplies (fictional company) — mini practice database for Chapter 12
-- Every name and number is invented.
DROP TABLE IF EXISTS payments, invoices, order_items, orders, products, customers, employees;

CREATE TABLE customers (
    customer_id    INTEGER PRIMARY KEY,
    customer_name  VARCHAR(100) NOT NULL,
    city           VARCHAR(50),
    segment        VARCHAR(30)  NOT NULL,
    signup_date    DATE         NOT NULL
);

CREATE TABLE products (
    product_id     INTEGER PRIMARY KEY,
    product_name   VARCHAR(100)  NOT NULL,
    category       VARCHAR(30)   NOT NULL,
    unit_price     NUMERIC(10,2) NOT NULL,
    unit_cost      NUMERIC(10,2) NOT NULL
);

CREATE TABLE employees (
    employee_id    INTEGER PRIMARY KEY,
    employee_name  VARCHAR(100) NOT NULL,
    job_title      VARCHAR(50)  NOT NULL,
    manager_id     INTEGER REFERENCES employees(employee_id)
);

CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY,
    customer_id    INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date     DATE    NOT NULL,
    status         VARCHAR(20) NOT NULL,
    sales_rep_id   INTEGER REFERENCES employees(employee_id)
);

CREATE TABLE order_items (
    order_item_id  INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders(order_id),
    product_id     INTEGER NOT NULL REFERENCES products(product_id),
    quantity       INTEGER NOT NULL,
    unit_price     NUMERIC(10,2) NOT NULL,
    discount_pct   NUMERIC(5,2)  NOT NULL DEFAULT 0
);

CREATE TABLE invoices (
    invoice_id     INTEGER PRIMARY KEY,
    order_id       INTEGER NOT NULL REFERENCES orders(order_id),
    invoice_date   DATE    NOT NULL,
    due_date       DATE    NOT NULL,
    amount         NUMERIC(12,2) NOT NULL
);

CREATE TABLE payments (
    payment_id     INTEGER PRIMARY KEY,
    invoice_id     INTEGER NOT NULL REFERENCES invoices(invoice_id),
    payment_date   DATE    NOT NULL,
    amount         NUMERIC(12,2) NOT NULL,
    method         VARCHAR(20)   NOT NULL
);

INSERT INTO customers VALUES
 (1, 'Sharma Hardware',       'Mumbai',    'Retail',      '2025-11-04'),
 (2, 'Patel Kitchenware',     'Ahmedabad', 'Retail',      '2025-12-15'),
 (3, 'Green Leaf Hotels',     'Pune',      'Hospitality', '2026-01-08'),
 (4, 'Coastal Foods',         'Chennai',   'Wholesale',   '2025-10-20'),
 (5, 'Metro Mart',            'Mumbai',    'Retail',      '2026-01-22'),
 (6, 'Sunrise Caterers',      NULL,        'Hospitality', '2026-02-03'),
 (7, 'Northgate Distributors','Delhi',     'Wholesale',   '2026-02-17'),
 (8, 'Blue Bay Cafe',         'Pune',      'Hospitality', '2026-03-01');

INSERT INTO products VALUES
 (101, 'Storage Box 10L',    'Storage',     450.00,  300.00),
 (102, 'Storage Box 25L',    'Storage',     780.00,  540.00),
 (103, 'Water Bottle 1L',    'Kitchen',     120.00,   70.00),
 (104, 'Food Container Set', 'Kitchen',     650.00,  430.00),
 (105, 'Industrial Crate',   'Industrial', 1450.00, 1100.00),
 (106, 'Garden Chair',       'Furniture',  1200.00,  850.00);

INSERT INTO employees VALUES
 (1, 'Anita Rao',     'Sales Head',      NULL),
 (2, 'Vikram Singh',  'Sales Manager',   1),
 (3, 'Neha Kulkarni', 'Sales Executive', 2),
 (4, 'Rahul Mehta',   'Sales Executive', 2),
 (5, 'Farah Khan',    'Sales Executive', 1);

INSERT INTO orders VALUES
 (5001, 1, '2026-01-05', 'Delivered', 3),
 (5002, 4, '2026-01-09', 'Delivered', 4),
 (5003, 2, '2026-01-14', 'Delivered', 3),
 (5004, 3, '2026-01-20', 'Cancelled', 5),
 (5005, 1, '2026-02-02', 'Delivered', 3),
 (5006, 5, '2026-02-06', 'Delivered', 4),
 (5007, 4, '2026-02-11', 'Delivered', 4),
 (5008, 6, '2026-02-19', 'Delivered', NULL),
 (5009, 7, '2026-02-25', 'Shipped',   5),
 (5010, 3, '2026-03-03', 'Delivered', 5),
 (5011, 1, '2026-03-10', 'Shipped',   3),
 (5012, 5, '2026-03-15', 'Pending',   4);

INSERT INTO order_items VALUES
 ( 1, 5001, 101, 20,  450.00,  0),
 ( 2, 5001, 103, 50,  120.00,  5),
 ( 3, 5002, 105, 40, 1450.00, 10),
 ( 4, 5002, 102, 30,  780.00, 10),
 ( 5, 5003, 104, 25,  650.00,  0),
 ( 6, 5004, 103, 100, 120.00,  0),
 ( 7, 5005, 101, 15,  450.00,  0),
 ( 8, 5005, 102, 10,  780.00,  0),
 ( 9, 5006, 103, 60,  120.00,  5),
 (10, 5006, 104, 12,  650.00,  0),
 (11, 5007, 105, 25, 1450.00, 10),
 (12, 5008, 104, 30,  650.00,  5),
 (13, 5008, 103, 40,  120.00,  0),
 (14, 5009, 105, 60, 1450.00, 12),
 (15, 5010, 102, 20,  780.00,  0),
 (16, 5010, 101, 10,  450.00,  0),
 (17, 5011, 104, 18,  650.00,  0),
 (18, 5012, 101, 40,  450.00,  5),
 (19, 5012, 103, 80,  120.00,  5);

-- Invoices are raised when an order ships (net of discount, before tax).
INSERT INTO invoices VALUES
 (9001, 5001, '2026-01-06', '2026-02-05', 14700.00),
 (9002, 5002, '2026-01-10', '2026-02-09', 73260.00),
 (9003, 5003, '2026-01-15', '2026-02-14', 16250.00),
 (9004, 5005, '2026-02-03', '2026-03-05', 14550.00),
 (9005, 5006, '2026-02-07', '2026-03-09', 14640.00),
 (9006, 5007, '2026-02-12', '2026-03-14', 32625.00),
 (9007, 5008, '2026-02-20', '2026-03-22', 23325.00),
 (9008, 5009, '2026-02-26', '2026-03-28', 76560.00),
 (9009, 5010, '2026-03-04', '2026-04-03', 20100.00),
 (9010, 5011, '2026-03-11', '2026-04-10', 11700.00);

-- Customers often pay in parts.
INSERT INTO payments VALUES
 ( 1, 9001, '2026-02-02', 14700.00, 'Bank transfer'),
 ( 2, 9002, '2026-02-05', 40000.00, 'Bank transfer'),
 ( 3, 9002, '2026-03-02', 33260.00, 'Bank transfer'),
 ( 4, 9003, '2026-02-20', 10000.00, 'UPI'),
 ( 5, 9004, '2026-03-01', 14550.00, 'Cheque'),
 ( 6, 9005, '2026-03-05',  7000.00, 'UPI'),
 ( 7, 9005, '2026-03-12',  7640.00, 'UPI'),
 ( 8, 9006, '2026-03-10', 20000.00, 'Bank transfer'),
 ( 9, 9008, '2026-03-20', 30000.00, 'Bank transfer'),
 (10, 9009, '2026-03-25', 20100.00, 'UPI');
