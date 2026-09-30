#!/usr/bin/env python3
"""ch77_check.py - check the Riverstone facts and numbers Chapter 77 quotes.

Run as a user that can `su postgres` (the book's practice server):
    python3 checks/ch77_check.py
Checks:
  1. Q77-007: net revenue on 2025-01-05 in riverstone_2025 is 20900.00 (one order).
  2. Q77-013: customer_changes records Harbour Traders (11) Retail -> Wholesale on 2025-09-01,
     and customer 11 signed up on 2025-04-09.
  3. Q77-017 / junk-dimension note for Ch 28: riverstone_2025 has 4 order statuses, so
     status x discounted(yes/no) = 8 rows.
  4. Q77-027: 50 - 3 = 47 columns left unread.
The SQL and Python outputs printed in the chapter are checked by tools/verify_sql.py and
tools/verify_python.py.
"""
import subprocess, sys

def pg(sql, db="riverstone_2025"):
    r = subprocess.run(["su", "postgres", "-c", f"psql -X -A -t -d {db}"], input=sql,
                       capture_output=True, text=True, cwd="/tmp")
    return r.stdout.strip()

ok = True
def check(name, got, want):
    global ok
    status = "OK " if got == want else "BAD"
    ok &= got == want
    print(f"{status} {name}: got {got!r}, want {want!r}")

check("revenue 2025-01-05", pg("""
    SELECT COUNT(DISTINCT o.order_id) || ' ' ||
           SUM(i.quantity * i.unit_price * (1 - i.discount_pct / 100))::numeric(12,2)
    FROM orders o JOIN order_items i ON i.order_id = o.order_id
    WHERE o.status <> 'Cancelled' AND o.order_date = DATE '2025-01-05';"""), "1 20900.00")
check("Harbour Traders change", pg("""
    SELECT c.customer_name || '|' || ch.old_value || '|' || ch.new_value || '|' || ch.changed_on
           || '|' || c.signup_date
    FROM customer_changes ch JOIN customers c USING (customer_id)
    WHERE ch.customer_id = 11 AND ch.column_name = 'segment';"""),
      "Harbour Traders|Retail|Wholesale|2025-09-01|2025-04-09")
statuses = int(pg("SELECT COUNT(DISTINCT status) FROM orders;"))
check("order statuses x discounted flag", statuses * 2, 8)
check("columns not read", 50 - 3, 47)
sys.exit(0 if ok else 1)
