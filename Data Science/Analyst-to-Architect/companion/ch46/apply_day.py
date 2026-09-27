"""Chapter 45 companion (copied for Chapter 46): simulate what happens in the ERP on later business days.
apply_day(1): 2 January 2026 - two new orders; order 10175 Shipped -> Delivered; order 10174 Pending -> Cancelled.
apply_day(2): 5 January 2026 - order 10176 Pending -> Shipped; one new order 10178.
Riverstone Supplies is fictional; every name and number is invented."""
import os, psycopg2
SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")

DAYS = {
 1: ["INSERT INTO orders VALUES (10176, 9, '2026-01-02', 'Pending', 5)",
     "INSERT INTO order_items VALUES (331, 10176, 101, 40, 430.00, 0.00)",
     "INSERT INTO order_items VALUES (332, 10176, 103, 120, 115.00, 5.00)",
     "INSERT INTO orders VALUES (10177, 12, '2026-01-02', 'Pending', 3)",
     "INSERT INTO order_items VALUES (333, 10177, 105, 6, 1400.00, 0.00)",
     "UPDATE orders SET status = 'Delivered' WHERE order_id = 10175",
     "UPDATE orders SET status = 'Cancelled' WHERE order_id = 10174"],
 2: ["UPDATE orders SET status = 'Shipped' WHERE order_id = 10176",
     "INSERT INTO orders VALUES (10178, 17, '2026-01-05', 'Pending', 3)",
     "INSERT INTO order_items VALUES (334, 10178, 102, 25, 750.00, 0.00)"],
}

def apply_day(n):
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:          # one transaction: all of the day, or none of it
        for stmt in DAYS[n]:
            cur.execute(stmt)
    conn.close()
