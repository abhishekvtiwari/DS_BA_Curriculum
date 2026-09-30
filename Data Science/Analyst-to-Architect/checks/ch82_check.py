#!/usr/bin/env python3
"""
checks/ch82_check.py - recompute every number Chapter 82's prose quotes, from the real databases and data.

Run from the book folder:  python3 checks/ch82_check.py
Needs: PostgreSQL 16 with riverstone_2025 (psql as user postgres), and companion/crm/ built by
companion/generate_riverstone_crm.py. Creates and drops a scratch database, scratch_ch82, for the upsert test.
Exit code 0 if every check passes.
"""
import pathlib, subprocess, sys

BOOK = pathlib.Path(__file__).resolve().parent.parent
MINI = BOOK / "companion" / "postgresql" / "riverstone_setup.sql"
ok = bad = 0


def check(name, got, want, tol=0.0):
    global ok, bad
    good = abs(got - want) <= tol if isinstance(want, (int, float)) else got == want
    ok += good; bad += not good
    print(("PASS " if good else "FAIL ") + f"{name}: got {got!r}, want {want!r}")


def pg(sql, db):
    r = subprocess.run(["su", "postgres", "-c", f"psql -X -q -A -t -F '|' -d {db}"], input=sql,
                       capture_output=True, text=True, cwd="/tmp")
    return [line.split("|") for line in r.stdout.strip().splitlines() if line]


def lakh(n):
    n = f"{n:.2f}" if isinstance(n, float) and n != int(n) else str(int(n))
    i, _, d = n.partition(".")
    if len(i) <= 3:
        out = i
    else:
        head, tail = i[:-3], i[-3:]
        out = ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail
    return out + ("." + d if d else "")


# ---------------- 82.1 Data Analyst (riverstone_2025) ----------------
REV = "oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)"
FROM = """FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
          JOIN products p ON oi.product_id = p.product_id WHERE o.status <> 'Cancelled'"""
rows = pg(f"""SELECT p.category, SUM({REV}), COUNT(DISTINCT o.order_id), COUNT(DISTINCT o.customer_id),
                     SUM({REV} - oi.quantity * p.unit_cost),
                     SUM(CASE WHEN EXTRACT(QUARTER FROM o.order_date) <= 2 THEN {REV} ELSE 0 END),
                     SUM(CASE WHEN EXTRACT(QUARTER FROM o.order_date) >= 3 THEN {REV} ELSE 0 END),
                     SUM(CASE WHEN EXTRACT(QUARTER FROM o.order_date) = 3 THEN {REV} ELSE 0 END),
                     SUM(CASE WHEN EXTRACT(QUARTER FROM o.order_date) = 4 THEN {REV} ELSE 0 END),
                     AVG(oi.discount_pct)
              {FROM} GROUP BY p.category""", "riverstone_2025")
c = {r[0]: [float(x) for x in r[1:]] for r in rows}
total = sum(v[0] for v in c.values())
check("2025 revenue ₹43,35,471", round(total, 2), 4335471.0)
check("order-category pairs 252", sum(v[1] for v in c.values()), 252)
check("non-cancelled orders 173", int(pg("SELECT COUNT(*) FROM orders WHERE status <> 'Cancelled'", "riverstone_2025")[0][0]), 173)
check("Industrial customers 5", c["Industrial"][2], 5)
check("Storage ₹22,97,973.50 ÷ 142 = 16,182.91", round(c["Storage"][0] / c["Storage"][1], 2), 16182.91)
check("Industrial ₹7,95,830 ÷ 23 = 34,601.30", round(c["Industrial"][0] / c["Industrial"][1], 2), 34601.30)
check("Kitchen per order 14,212.12", round(c["Kitchen"][0] / c["Kitchen"][1], 2), 14212.12)
check("Industrial more than twice Storage", c["Industrial"][0] / c["Industrial"][1] / (c["Storage"][0] / c["Storage"][1]) > 2, True)
check("Kitchen H2 vs H1 +142%", round(100 * c["Kitchen"][5] / c["Kitchen"][4] - 100), 142)
check("Industrial H2 vs H1 +149%", round(100 * c["Industrial"][5] / c["Industrial"][4] - 100), 149)
check("Storage H2 vs H1 +72%", round(100 * c["Storage"][5] / c["Storage"][4] - 100), 72)
check("Storage Q4 more than twice Q3", c["Storage"][7] / c["Storage"][6] > 2, True)
check("Furniture H2 revenue 0", c["Furniture"][5], 0.0)
gp_total = sum(v[3] for v in c.values())
check("total gross profit ₹11,37,221", round(gp_total), 1137221)
check("Industrial share of revenue ~18%", round(100 * c["Industrial"][0] / total), 18)
check("Industrial share of gross profit under 10%", 100 * c["Industrial"][3] / gp_total < 10, True)
check("Industrial profit per order ₹4,710", round(c["Industrial"][3] / c["Industrial"][1]), 4710)
check("Kitchen profit per order ₹4,724", round(c["Kitchen"][3] / c["Kitchen"][1]), 4724)
check("Industrial margin 13.6%", round(100 * c["Industrial"][3] / c["Industrial"][0], 1), 13.6)
check("Kitchen margin 33.2%", round(100 * c["Kitchen"][3] / c["Kitchen"][0], 1), 33.2)
check("Industrial average discount 9.2%", round(c["Industrial"][8], 1), 9.2)
check("lakh: ₹22.98 lakh", round(c["Storage"][0] / 1e5, 2), 22.98)
check("lakh: ₹43.35 lakh", round(total / 1e5, 2), 43.35)
check("lakh grouping of total", lakh(4335471), "43,35,471")
check("lakh grouping of Industrial GP", lakh(round(c["Industrial"][3])), "1,08,330")

# DA mock: the NOT EXISTS query and the NOT IN version agree on this table (customer_id is never NULL)
q_exists = """SELECT COUNT(*) FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id
              AND o.status <> 'Cancelled' AND o.order_date > (SELECT MAX(order_date) FROM orders) - INTERVAL '90 days')"""
q_in = """SELECT COUNT(*) FROM customers c WHERE c.customer_id NOT IN (SELECT customer_id FROM orders o
          WHERE o.status <> 'Cancelled' AND o.order_date > (SELECT MAX(order_date) FROM orders) - INTERVAL '90 days')"""
check("NOT IN happens to agree with NOT EXISTS here", pg(q_in, "riverstone_2025"), pg(q_exists, "riverstone_2025"))
check("orders.customer_id has no NULLs", pg("SELECT COUNT(*) FROM orders WHERE customer_id IS NULL", "riverstone_2025")[0][0], "0")

# ---------------- 82.2 Data Scientist (printed outputs are checked by verify_python) ----------------
check("2.3 times the profit", round(2448060 / 1079730, 1), 2.3)
check("28% of the effort", round(100 * 627 / 2225), 28)
check("₹24.5 lakh / ₹10.8 lakh / ₹23.3 lakh", (round(2448060 / 1e5, 1), round(1079730 / 1e5, 1), round(2330010 / 1e5, 1)), (24.5, 10.8, 23.3))
check("one worked lead in five (504 list)", round(504 / 102), 5)
check("capacity 126 x 4", 126 * 4, 504)
check("all-lost accuracy 93.4%", round(100 * (2225 - 146) / 2225, 1), 93.4)
check("recall 112/146 = 0.767", round(112 / 146, 3), 0.767)

# ---------------- 82.3 Data Engineer: the arithmetic, and the upsert claim ----------------
check("bad line revenue 10 x 450 x (1 - 1.5)", 10 * 450 * (1 - 1.5), -2250.0)
check("fixed line revenue 10 x 450 x 0.85", 10 * 450 * 0.85, 3825.0)
check("297,710 + 3,825 = 301,535", 297710 + 3825, 301535)
check("323,930 - 26,220 = 297,710", 323930 - 26220, 297710)
subprocess.run(["su", "postgres", "-c", "psql -X -q -d postgres -c 'DROP DATABASE IF EXISTS scratch_ch82' -c 'CREATE DATABASE scratch_ch82'"],
               capture_output=True, cwd="/tmp")
UPSERT = f"""INSERT INTO daily_summary SELECT o.order_date, SUM({REV}), COUNT(DISTINCT o.order_id)
             FROM orders o JOIN order_items oi ON o.order_id = oi.order_id WHERE o.status <> 'Cancelled'
             GROUP BY o.order_date
             ON CONFLICT (order_date) DO UPDATE SET total_revenue = EXCLUDED.total_revenue, order_count = EXCLUDED.order_count;"""
res = pg(f"""\\i '{MINI}'
CREATE TABLE daily_summary (order_date DATE PRIMARY KEY, total_revenue NUMERIC(12,2) NOT NULL, order_count INT NOT NULL);
{UPSERT}
UPDATE orders SET status = 'Cancelled' WHERE order_id = 5012;
{UPSERT}
SELECT total_revenue FROM daily_summary WHERE order_date = '2026-03-15';""", "scratch_ch82")
check("upsert keeps the stale 15 March row at 26,220", res[-1][0] if res else None, "26220.00")
subprocess.run(["su", "postgres", "-c", "psql -X -q -d postgres -c 'DROP DATABASE IF EXISTS scratch_ch82'"], capture_output=True, cwd="/tmp")

print(f"\n{ok} passed, {bad} failed")
sys.exit(1 if bad else 0)
