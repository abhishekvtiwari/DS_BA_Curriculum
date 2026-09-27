#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 28 · Advanced SQL, Performance & Data Modeling
File: generate_riverstone_perf.py
What: generates riverstone_perf, a large practice database (2023-2025) for the performance sections
      (28.4-28.6, 28.11). Same table layout as riverstone_2025, with no indexes except primary keys.
How:  python3 generate_riverstone_perf.py [--lines 2000000] [--out perf_data]
      then load it:  PostgreSQL  psql -d riverstone_perf -f perf_data/load_postgresql.sql
                     MySQL       mysql --local-infile=1 < perf_data/load_mysql.sql
      (run the load scripts from the folder that contains perf_data/)
Seed: 28 (fixed), so every reader gets identical data. "Today" is 31 December 2025.
Tested on: Python 3.12.3, PostgreSQL 16, MySQL 8.0.46 (Ubuntu 24.04, 1 vCPU, 3 GB RAM).
Riverstone Supplies is fictional; every name and number is invented.
"""
import argparse, csv, os, random
from datetime import date, timedelta

ap = argparse.ArgumentParser()
ap.add_argument('--lines', type=int, default=2_000_000, help='approximate number of order lines')
ap.add_argument('--out', default='perf_data')
a = ap.parse_args()
rng = random.Random(28)
os.makedirs(a.out, exist_ok=True)

CITIES = ['Mumbai', 'Pune', 'Delhi', 'Bengaluru', 'Chennai', 'Hyderabad', 'Ahmedabad', 'Kolkata', 'Jaipur',
          'Lucknow', 'Surat', 'Indore', 'Nagpur', 'Kochi', 'Nashik', 'Goa', 'Udaipur', 'Thane', 'Coimbatore',
          'Bhopal', 'Vadodara', 'Chandigarh', 'Guwahati', 'Mysuru', 'Visakhapatnam']
FIRST = ['Sai', 'Shree', 'New', 'Royal', 'Green', 'Blue', 'Golden', 'City', 'Metro', 'Sunrise', 'Lotus',
         'Coastal', 'Western', 'Eastern', 'Prime', 'Star', 'Crystal', 'Silver', 'Ganga', 'Kaveri']
LAST = {'Retail': ['Hardware', 'Stores', 'Mart', 'Traders', 'Emporium', 'Home Needs'],
        'Hospitality': ['Hotels', 'Caterers', 'Restaurants', 'Kitchens', 'Banquets', 'Resorts'],
        'Wholesale': ['Distributors', 'Wholesale', 'Agencies', 'Supply Co', 'Logistics', 'Enterprises']}
PRODUCTS = [(101, 'Storage Box 10L', 'Storage', 430, 300), (102, 'Storage Box 25L', 'Storage', 750, 540),
            (103, 'Water Bottle 1L', 'Kitchen', 115, 70), (104, 'Food Container Set', 'Kitchen', 620, 430),
            (105, 'Industrial Crate', 'Industrial', 1400, 1100), (106, 'Garden Chair', 'Furniture', 1150, 850),
            (107, 'Lunch Box Set', 'Kitchen', 380, 240), (108, 'Stackable Bin', 'Storage', 290, 190)]
EMPLOYEES = [(1, 'Anita Rao', 'Sales Head', ''), (2, 'Vikram Singh', 'Sales Manager', 1),
             (3, 'Neha Kulkarni', 'Sales Executive', 2), (4, 'Rahul Mehta', 'Sales Executive', 2),
             (5, 'Farah Khan', 'Sales Executive', 1)]

N_CUST = 5000
START, END = date(2023, 1, 1), date(2025, 12, 31)
days = (END - START).days + 1

customers, weights = [], []
for cid in range(1, N_CUST + 1):
    seg = rng.choices(['Retail', 'Hospitality', 'Wholesale'], [0.5, 0.3, 0.2])[0]
    name = f"{rng.choice(FIRST)} {rng.choice(LAST[seg])} {cid:04d}"
    signup = START - timedelta(days=rng.randint(0, 700)) + timedelta(days=rng.randint(0, days - 30))
    customers.append((cid, name, rng.choice(CITIES), seg, signup))
    weights.append(rng.paretovariate(1.3))          # a few customers order far more than the rest

with open(f'{a.out}/customers.csv', 'w', newline='') as f:
    w = csv.writer(f); [w.writerow(c) for c in customers]
with open(f'{a.out}/products.csv', 'w', newline='') as f:
    w = csv.writer(f); [w.writerow(p) for p in PRODUCTS]
with open(f'{a.out}/employees.csv', 'w', newline='') as f:
    w = csv.writer(f); [w.writerow(e) for e in EMPLOYEES]

n_orders = a.lines * 10 // 28                       # about 2.8 lines per order
cust_pick = rng.choices(customers, weights, k=n_orders)
order_rows, item_rows, item_id = [], 0, 0
fo = open(f'{a.out}/orders.csv', 'w', newline=''); wo = csv.writer(fo)
fi = open(f'{a.out}/order_items.csv', 'w', newline=''); wi = csv.writer(fi)
dates = sorted(START + timedelta(days=int(days * (rng.random() ** 0.8))) for _ in range(n_orders))  # business grows
for oid, (c, d) in enumerate(zip(cust_pick, dates), start=1):
    d_use = d
    r = rng.random()
    status = 'Cancelled' if r < 0.02 else ('Pending' if (END - d_use).days < 10 and r < 0.5
                                           else ('Shipped' if (END - d_use).days < 20 and r < 0.7 else 'Delivered'))
    rep = rng.choices([2, 3, 4, 5, ''], [0.15, 0.3, 0.3, 0.2, 0.05])[0]
    wo.writerow((oid, c[0], d_use.isoformat(), status, rep))
    k = rng.choices([1, 2, 3, 4, 5], [0.25, 0.25, 0.2, 0.15, 0.15])[0]
    for p in rng.sample(PRODUCTS, k):
        item_id += 1
        qty = rng.choice([5, 10, 10, 20, 25, 50, 100]) if c[3] != 'Hospitality' else rng.choice([2, 5, 10, 12, 20])
        price = round(p[3] * (0.95 if d_use.year == 2023 else 0.98 if d_use.year == 2024 else 1.0))
        disc = rng.choices([0, 5, 10, 12], [0.7, 0.18, 0.1, 0.02])[0]
        wi.writerow((item_id, oid, p[0], qty, price, disc))
fo.close(); fi.close()

pg = f"""-- Load riverstone_perf into PostgreSQL. Create the database first: CREATE DATABASE riverstone_perf;
DROP TABLE IF EXISTS order_items, orders, employees, products, customers;
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, customer_name VARCHAR(100) NOT NULL, city VARCHAR(50), segment VARCHAR(30) NOT NULL, signup_date DATE NOT NULL);
CREATE TABLE products (product_id INTEGER PRIMARY KEY, product_name VARCHAR(100) NOT NULL, category VARCHAR(30) NOT NULL, unit_price NUMERIC(10,2) NOT NULL, unit_cost NUMERIC(10,2) NOT NULL);
CREATE TABLE employees (employee_id INTEGER PRIMARY KEY, employee_name VARCHAR(100) NOT NULL, job_title VARCHAR(50) NOT NULL, manager_id INTEGER REFERENCES employees(employee_id));
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(customer_id), order_date DATE NOT NULL, status VARCHAR(20) NOT NULL, sales_rep_id INTEGER REFERENCES employees(employee_id));
CREATE TABLE order_items (order_item_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(order_id), product_id INTEGER NOT NULL REFERENCES products(product_id), quantity INTEGER NOT NULL, unit_price NUMERIC(10,2) NOT NULL, discount_pct NUMERIC(5,2) NOT NULL DEFAULT 0);
\\copy customers FROM '{a.out}/customers.csv' CSV
\\copy products FROM '{a.out}/products.csv' CSV
\\copy employees FROM '{a.out}/employees.csv' CSV NULL ''
\\copy orders FROM '{a.out}/orders.csv' CSV NULL ''
\\copy order_items FROM '{a.out}/order_items.csv' CSV
ANALYZE;
"""
open(f'{a.out}/load_postgresql.sql', 'w').write(pg)
my = f"""-- Load riverstone_perf into MySQL: mysql --local-infile=1 < {a.out}/load_mysql.sql  (server needs local_infile=ON)
DROP DATABASE IF EXISTS riverstone_perf; CREATE DATABASE riverstone_perf; USE riverstone_perf;
CREATE TABLE customers (customer_id INT PRIMARY KEY, customer_name VARCHAR(100) NOT NULL, city VARCHAR(50), segment VARCHAR(30) NOT NULL, signup_date DATE NOT NULL);
CREATE TABLE products (product_id INT PRIMARY KEY, product_name VARCHAR(100) NOT NULL, category VARCHAR(30) NOT NULL, unit_price DECIMAL(10,2) NOT NULL, unit_cost DECIMAL(10,2) NOT NULL);
CREATE TABLE employees (employee_id INT PRIMARY KEY, employee_name VARCHAR(100) NOT NULL, job_title VARCHAR(50) NOT NULL, manager_id INT, FOREIGN KEY (manager_id) REFERENCES employees(employee_id));
CREATE TABLE orders (order_id INT PRIMARY KEY, customer_id INT NOT NULL, order_date DATE NOT NULL, status VARCHAR(20) NOT NULL, sales_rep_id INT, FOREIGN KEY (customer_id) REFERENCES customers(customer_id), FOREIGN KEY (sales_rep_id) REFERENCES employees(employee_id));
CREATE TABLE order_items (order_item_id INT PRIMARY KEY, order_id INT NOT NULL, product_id INT NOT NULL, quantity INT NOT NULL, unit_price DECIMAL(10,2) NOT NULL, discount_pct DECIMAL(5,2) NOT NULL DEFAULT 0, FOREIGN KEY (order_id) REFERENCES orders(order_id), FOREIGN KEY (product_id) REFERENCES products(product_id));
SET FOREIGN_KEY_CHECKS = 0;
LOAD DATA LOCAL INFILE '{a.out}/customers.csv' INTO TABLE customers FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"';
LOAD DATA LOCAL INFILE '{a.out}/products.csv' INTO TABLE products FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"';
LOAD DATA LOCAL INFILE '{a.out}/employees.csv' INTO TABLE employees FIELDS TERMINATED BY ',' (employee_id, employee_name, job_title, @m) SET manager_id = NULLIF(@m, '');
LOAD DATA LOCAL INFILE '{a.out}/orders.csv' INTO TABLE orders FIELDS TERMINATED BY ',' (order_id, customer_id, order_date, status, @r) SET sales_rep_id = NULLIF(@r, '');
LOAD DATA LOCAL INFILE '{a.out}/order_items.csv' INTO TABLE order_items FIELDS TERMINATED BY ',';
SET FOREIGN_KEY_CHECKS = 1;
ANALYZE TABLE customers, products, employees, orders, order_items;
"""
open(f'{a.out}/load_mysql.sql', 'w').write(my)
print(f'customers {N_CUST:,}  orders {n_orders:,}  order lines {item_id:,}  (seed 28)')
