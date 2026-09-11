from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

OUT = Path(__file__).resolve().parent

SCHEMA = """
CREATE TABLE customers (
  customer_id INTEGER PRIMARY KEY,
  customer_name TEXT NOT NULL,
  region TEXT
);
CREATE TABLE orders (
  order_id INTEGER PRIMARY KEY,
  customer_id INTEGER,
  order_date TEXT NOT NULL,
  status TEXT,
  total_amount NUMERIC,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
CREATE TABLE order_events (
  event_id INTEGER PRIMARY KEY,
  order_id INTEGER,
  event_type TEXT NOT NULL,
  event_at TEXT NOT NULL
);
CREATE TABLE customer_import (
  source_row INTEGER PRIMARY KEY,
  email TEXT,
  country_code TEXT,
  signup_date TEXT
);
"""

DATA = """
INSERT INTO customers VALUES
 (1,'Aster Stores','North'),
 (2,'Beacon Labs','South'),
 (3,'Cedar Works','North'),
 (4,'Delta Retail',NULL),
 (5,'Elm Services','West');
INSERT INTO orders VALUES
 (101,1,'2026-01-03','paid',120.00),
 (102,1,'2026-01-12','refunded',40.00),
 (103,2,'2026-01-15','paid',200.00),
 (104,2,'2026-02-02','pending',NULL),
 (105,3,'2026-02-08','paid',80.00),
 (106,99,'2026-02-09','paid',60.00),
 (107,3,'2026-02-20',NULL,150.00),
 (108,4,'2026-03-01','paid',90.00);
INSERT INTO order_events VALUES
 (1,101,'created','2026-01-03 09:00:00'),
 (2,101,'paid','2026-01-03 09:05:00'),
 (3,102,'created','2026-01-12 10:00:00'),
 (4,102,'paid','2026-01-12 10:02:00'),
 (5,102,'refunded','2026-01-13 08:00:00'),
 (6,103,'created','2026-01-15 12:00:00'),
 (7,103,'paid','2026-01-15 12:03:00');
INSERT INTO customer_import VALUES
 (1,'ana@example.test','IN','2026-01-03'),
 (2,'bob@example.test','US','2026-01-05'),
 (3,'ana@example.test','IN','2026-01-03'),
 (4,NULL,'GB','2026-01-08'),
 (5,'cara@example.test','ZZ','not-a-date'),
 (6,'  DEX@EXAMPLE.TEST  ','US','2026-02-01');
"""

QUERIES = {
"E01": ("Projection, aliasing, and deterministic ordering", """
SELECT order_id,
       order_date,
       total_amount AS booked_amount
FROM orders
ORDER BY order_date, order_id
LIMIT 4;
"""),
"E02": ("Filter a half-open reporting period with explicit NULL handling", """
SELECT order_id, status, total_amount
FROM orders
WHERE order_date >= '2026-02-01'
  AND order_date <  '2026-03-01'
  AND (status = 'paid' OR status IS NULL)
ORDER BY order_id;
"""),
"E03": ("Preserve the customer population with a LEFT JOIN", """
SELECT c.customer_id,
       c.customer_name,
       COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
  ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY c.customer_id;
"""),
"E04": ("Aggregate paid revenue at region grain", """
SELECT COALESCE(c.region, 'Unknown') AS region,
       COUNT(*) AS paid_orders,
       ROUND(SUM(o.total_amount), 2) AS paid_revenue
FROM orders AS o
JOIN customers AS c
  ON c.customer_id = o.customer_id
WHERE o.status = 'paid'
GROUP BY COALESCE(c.region, 'Unknown')
ORDER BY paid_revenue DESC, region;
"""),
"E05": ("Decompose customer revenue with CTEs", """
WITH paid_orders AS (
  SELECT customer_id, total_amount
  FROM orders
  WHERE status = 'paid'
),
customer_revenue AS (
  SELECT customer_id, SUM(total_amount) AS revenue
  FROM paid_orders
  GROUP BY customer_id
)
SELECT c.customer_name, cr.revenue
FROM customer_revenue AS cr
JOIN customers AS c
  ON c.customer_id = cr.customer_id
ORDER BY cr.revenue DESC, c.customer_name;
"""),
"E06": ("Rank orders and calculate a running customer total", """
SELECT customer_id,
       order_id,
       total_amount,
       ROW_NUMBER() OVER (
         PARTITION BY customer_id
         ORDER BY total_amount DESC, order_id
       ) AS amount_rank,
       SUM(total_amount) OVER (
         PARTITION BY customer_id
         ORDER BY order_date, order_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_amount
FROM orders
WHERE total_amount IS NOT NULL
  AND customer_id IN (1, 2, 3)
ORDER BY customer_id, order_date, order_id;
"""),
"E07": ("Find duplicate normalized email keys", """
SELECT LOWER(TRIM(email)) AS normalized_email,
       COUNT(*) AS row_count
FROM customer_import
WHERE email IS NOT NULL
GROUP BY LOWER(TRIM(email))
HAVING COUNT(*) > 1
ORDER BY normalized_email;
"""),
"E08": ("Find orphan foreign keys", """
SELECT o.order_id, o.customer_id
FROM orders AS o
LEFT JOIN customers AS c
  ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
ORDER BY o.order_id;
"""),
"E09": ("Profile missing and invalid domain values", """
SELECT
  SUM(CASE WHEN email IS NULL OR TRIM(email) = '' THEN 1 ELSE 0 END) AS missing_email,
  SUM(CASE WHEN country_code NOT IN ('IN','US','GB') THEN 1 ELSE 0 END) AS invalid_country,
  COUNT(*) AS total_rows
FROM customer_import;
"""),
"E10": ("Reconcile joined paid revenue to the source population", """
WITH source_total AS (
  SELECT SUM(total_amount) AS amount
  FROM orders
  WHERE status = 'paid'
),
matched_total AS (
  SELECT SUM(o.total_amount) AS amount
  FROM orders AS o
  JOIN customers AS c ON c.customer_id = o.customer_id
  WHERE o.status = 'paid'
)
SELECT source_total.amount AS source_paid,
       matched_total.amount AS matched_paid,
       source_total.amount - matched_total.amount AS unmatched_paid
FROM source_total CROSS JOIN matched_total;
"""),
}


def md_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).replace("|", "\\|")


def md_table(columns, rows):
    out = ["| " + " | ".join(columns) + " |",
           "|" + "|".join(["---"] * len(columns)) + "|"]
    out.extend("| " + " | ".join(md_value(v) for v in row) + " |" for row in rows)
    return "\n".join(out)


def main():
    con = sqlite3.connect(":memory:")
    con.executescript(SCHEMA)
    con.executescript(DATA)
    records = []
    md = ["# BA-05-C03 SQL execution audit", "", "**Runtime:** Python sqlite3 / SQLite " + sqlite3.sqlite_version,
          "**Fixture:** synthetic, non-personal training data created in memory", "**Transaction:** read-only SELECT examples after fixture creation", ""]
    for query_id, (purpose, sql) in QUERIES.items():
        cur = con.execute(sql)
        columns = [d[0] for d in cur.description]
        rows = cur.fetchall()
        digest = hashlib.sha256(sql.strip().encode("utf-8")).hexdigest()
        records.append({"id": query_id, "purpose": purpose, "sha256": digest, "columns": columns, "rows": rows})
        md.extend([f"## {query_id} - {purpose}", "", f"Query SHA-256: `{digest}`", "", md_table(columns, rows), ""])
    con.close()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "BA-M05-C03-SQL-EXECUTION-AUDIT.md").write_text("\n".join(md), encoding="utf-8")
    manifest = {"chapter": "BA-05-C03", "runtime": "Python sqlite3", "sqlite_version": sqlite3.sqlite_version,
                "fixture_kind": "synthetic non-personal in-memory data", "query_count": len(records), "queries": records}
    (OUT / "BA-M05-C03-SQL-EXECUTION-AUDIT.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"runtime": sqlite3.sqlite_version, "queries_executed": len(records), "audit_dir": str(OUT)}))


if __name__ == "__main__":
    main()
