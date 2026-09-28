"""Chapter 25 checks: every number in the chapter that comes from data or arithmetic.

    python3 checks/ch25_check.py            # from the book folder (Data Science/Analyst-to-Architect)

The one SQL block (section 25.6) is checked by tools/verify_sql.py. This script checks the rest:
  1. Order 5001's journey (Chapter 3): order, invoice and payment dates in `riverstone`, and the
     day counts derived from them (order to invoice 1, invoice to payment 27, order to cash 28,
     enquiry to cash 103).
  2. The orders table has a status column and no delivery-date column (section 25.9).
  3. Volume NFR (section 25.5): 209,006 order lines in `riverstone_full`, 2025 lines 22% above 2024.
  4. Section 25.10: key-account 2025 revenue with and without the two cancelled orders
     (₹43,35,471 vs ₹43,98,121, difference ₹62,650) in `riverstone_2025`.
  5. Section 25.6: the at-risk rule, twice vs 1.5 times the usual gap, and the "too new to judge"
     count (7 of 24), plus the "what if" with a minimum of 2 order days (6 rows).
  6. The MySQL variant of the section 25.6 query (DATEDIFF) returns the same rows.
  7. Arithmetic: Chapter 3's re-keying (40 x 6 min = 4 h/week, 200 h/50-week year, ~17 h/month),
     exercise 9 (40 min x 5 x 50 = 10,000 min, ~167 h), the ranking scores, and the five lane
     crossings of the swimlane.
Exit code 0 if everything passes.
"""
import re, subprocess, sys
from datetime import date
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
MD = next((BOOK / "manuscript").glob("ch25-*.md")).read_text(encoding="utf-8")
ok = True


def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))


def pg(db, sql):
    r = subprocess.run(["su", "postgres", "-c", f"psql -X -q -A -t -F '|' -d {db}"], input=sql,
                       capture_output=True, text=True, cwd="/tmp")
    return [l.split("|") for l in r.stdout.strip().splitlines() if l]


def my(db, sql):
    r = subprocess.run(["mysql", "-uroot", "-N", "-B", db], input=sql, capture_output=True, text=True)
    return [l.split("\t") for l in r.stdout.strip().splitlines() if l]


def lakh(n):
    i, _, d = f"{n:.2f}".partition(".")
    if len(i) > 3:
        head, tail = i[:-3], i[-3:]
        i = ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail
    return i + ("" if d == "00" else "." + d)


# 1. order 5001
(od, st), = pg("riverstone", "SELECT order_date, status FROM orders WHERE order_id = 5001;")
(inv_d, amt), = pg("riverstone", "SELECT invoice_date, amount FROM invoices WHERE invoice_id = 9001;")
(pay_d,), = pg("riverstone", "SELECT MIN(payment_date) FROM payments WHERE invoice_id = 9001;")
d = lambda s: date.fromisoformat(s)
check("order 5001 dated 2026-01-05", od == "2026-01-05", od)
check("invoice 9001 dated 2026-01-06 for 14,700", inv_d == "2026-01-06" and float(amt) == 14700, (inv_d, amt))
check("payment for 9001 on 2026-02-02", pay_d == "2026-02-02", pay_d)
check("order to invoice 1 day", (d(inv_d) - d(od)).days == 1)
check("invoice to payment 27 days", (d(pay_d) - d(inv_d)).days == 27)
check("order to cash 28 days", (d(pay_d) - d(od)).days == 28)
check("enquiry (2025-10-22) to cash 103 days", (d(pay_d) - date(2025, 10, 22)).days == 103)
check("chapter quotes those day counts",
      all(x in MD for x in ["103 days", "only 28 days from order to cash", "only 1 day from order to invoice"]))

# 2. no delivery date column
for db in ("riverstone", "riverstone_2025", "riverstone_full"):
    cols = [r[0] for r in pg(db, "SELECT column_name FROM information_schema.columns WHERE table_name = 'orders';")]
    check(f"{db}.orders has status and no delivery column", "status" in cols and not any("deliver" in c for c in cols), cols)

# 3. volume
rows = dict(pg("riverstone_full", "SELECT EXTRACT(YEAR FROM o.order_date)::int, COUNT(*) FROM order_items oi "
                                  "JOIN orders o USING (order_id) GROUP BY 1;"))
total = sum(int(v) for v in rows.values())
growth = int(rows["2025"]) / int(rows["2024"]) - 1
check("209,006 order lines in riverstone_full", total == 209006, total)
check("2025 lines 22% above 2024", round(growth * 100) == 22, f"{growth:.3%}")
check("chapter quotes the volume figures", "209,006 order lines" in MD and "22% more lines in 2025" in MD)

# 4. cancelled orders in the key-account revenue
(valid, allrev), = pg("riverstone_2025",
                      "SELECT SUM(net) FILTER (WHERE status <> 'Cancelled'), SUM(net) FROM (SELECT o.status, "
                      "oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100) AS net FROM orders o "
                      "JOIN order_items oi USING (order_id)) t;")
valid, allrev = float(valid), float(allrev)
check("2025 key-account revenue 43,35,471", lakh(valid) == "43,35,471", lakh(valid))
check("with cancelled orders 43,98,121", lakh(allrev) == "43,98,121", lakh(allrev))
check("difference 62,650", round(allrev - valid, 2) == 62650, allrev - valid)
check("chapter quotes those revenue figures", all(x in MD for x in ["₹43,98,121", "₹43,35,471", "₹62,650"]))

# 5. the at-risk rule
BASE = """
WITH order_days AS (SELECT DISTINCT customer_id, order_date FROM sales_lines),
gaps AS (SELECT customer_id, order_date,
                order_date - LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS gap_days
         FROM order_days),
rhythm AS (SELECT customer_id, COUNT(*) AS order_days, ROUND(AVG(gap_days)) AS usual_gap,
                  DATE '2025-12-31' - MAX(order_date) AS days_quiet FROM gaps GROUP BY customer_id)
SELECT c.customer_name,
       CASE WHEN r.order_days IS NULL OR r.order_days < {minimum} THEN 'new'
            WHEN r.days_quiet > 2 * r.usual_gap THEN '2x'
            WHEN r.days_quiet > 1.5 * r.usual_gap THEN '1.5x'
            ELSE 'ok' END
FROM customers c LEFT JOIN rhythm r ON r.customer_id = c.customer_id;"""
v = pg("riverstone_2025", BASE.format(minimum=4))
by = lambda k: sorted(n for n, x in v if x == k)
check("24 key accounts", len(v) == 24, len(v))
check("twice the gap flags Om Sai Provisions and Sunrise Caterers", by("2x") == ["Om Sai Provisions", "Sunrise Caterers"], by("2x"))
check("1.5 times adds only Green Leaf Hotels", by("1.5x") == ["Green Leaf Hotels"], by("1.5x"))
check("seven accounts too new to judge, Home Plus among them", len(by("new")) == 7 and "Home Plus" in by("new"), by("new"))
check("chapter says seven of the 24", "Seven of the 24 key accounts are too new to judge" in MD and "seven of Riverstone's 24 key accounts" in MD)
v = pg("riverstone_2025", BASE.format(minimum=2))
check("what-if: minimum 2 leaves six rows off rhythm", sum(1 for _, x in v if x != "ok") == 6)
check("what-if: City Needs Store and Prime Wholesale join, only Home Plus new",
      sorted(n for n, x in v if x in ("2x", "1.5x")) == ["City Needs Store", "Green Leaf Hotels", "Om Sai Provisions",
                                                          "Prime Wholesale", "Sunrise Caterers"]
      and [n for n, x in v if x == "new"] == ["Home Plus"])

# 6. MySQL variant of the chapter's query
block = re.search(r"```sql\n(WITH order_days.*?)```", MD, re.S).group(1)
mysql_sql = (block.replace("order_date - LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)",
                           "DATEDIFF(order_date, LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date))")
             .replace("DATE '2025-12-31' - MAX(order_date)", "DATEDIFF(DATE '2025-12-31', MAX(order_date))"))
pg_rows = pg("riverstone_2025", block)
my_rows = [[("" if c == "NULL" else c) for c in r] for r in my("riverstone_2025", mysql_sql)]
check("MySQL (DATEDIFF) returns the same rows as PostgreSQL", pg_rows == my_rows, (pg_rows[:2], my_rows[:2]))

# 7. arithmetic
check("re-keying: 40 x 6 min = 4 h/week", 40 * 6 / 60 == 4)
check("re-keying: 200 h per 50-week year", 4 * 50 == 200)
check("re-keying: about 17 h a month", round(200 / 12) == 17)
check("exercise 9: 40 x 5 x 50 = 10,000 min, about 167 h", 40 * 5 * 50 == 10000 and round(10000 / 60) == 167)
check("exercise 9: a little over four 40-hour weeks", 4 < 10000 / 60 / 40 < 4.5)
check("ranking scores 17, 8, 6", (17 * 3 / 3, 8 * 2 / 2, 6 * 3 / 3) == (17, 8, 6))
lanes = [0, 1, 1, 1, 2, 2, 3, 2, 3, 3]
check("five of nine transitions cross a lane", sum(a != b for a, b in zip(lanes, lanes[1:])) == 5)

print("ALL PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
