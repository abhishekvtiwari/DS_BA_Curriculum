#!/usr/bin/env python3
"""Chapter 71 checks: the SQL that verify_sql.py can't see.

    python3 checks/ch71_check.py                 # from the book folder, against the shared servers
    CH71_PG=127.0.0.1:5471 CH71_MY=127.0.0.1:3384 python3 checks/ch71_check.py   # other servers

verify_sql.py runs every ```sql / ```mysql block that has an output block after it. This script covers
the rest:
1. The blocks marked <!-- ch71-check: view --> (Q71-049) and <!-- ch71-check: index --> (Q71-068). They
   change riverstone_2025, so the chapter marks them <!-- run: none -->. Here PostgreSQL runs them inside
   BEGIN ... ROLLBACK, so the shared database is left exactly as it was, and the printed outputs are
   compared with the chapter.
2. The MySQL versions printed without an output block ("returns the same rows"): Q71-028, Q71-036,
   Q71-042, Q71-074, Q71-075, Q71-029. Each must give the same rows as its PostgreSQL version.
3. Numbers stated in prose and rapid-fire rows (Q71-006, Q71-012, Q71-013, Q71-015, Q71-024, Q71-027,
   Q71-029, Q71-030, Q71-035, Q71-037, Q71-041, Q71-043, Q71-044, Q71-046, Q71-060, Q71-074).
Throwaway tables go in a scratch database, scratch_ch71 (created if missing). Exit code 0 if all agree.
"""
import os, pathlib, re, subprocess, sys
from decimal import Decimal

MS = pathlib.Path(__file__).resolve().parent.parent / "manuscript" / "ch71-sql-question-bank.md"
md = MS.read_text(encoding="utf-8")
bad = 0


def pg(sql, db="riverstone_2025", fmt="-At"):
    hp = os.environ.get("CH71_PG")
    if hp:
        h, p = hp.split(":")
        cmd = ["psql", "-X", "-q"] + ([fmt] if fmt else []) + ["-h", h, "-p", p, "-U", "postgres", "-d", db]
        r = subprocess.run(cmd, input=sql, capture_output=True, text=True)
    else:
        r = subprocess.run(["su", "postgres", "-c", f"psql -X -q {fmt} -d {db}"], input=sql,
                           capture_output=True, text=True, cwd="/tmp")
    return (r.stdout + r.stderr).strip()


def my(sql, db="riverstone_2025", table=False):
    hp = os.environ.get("CH71_MY")
    args = ["mysql", "-uroot", "-t" if table else "-N"]
    if not table:
        args.append("-B")
    if hp:
        h, p = hp.split(":")
        args = ["/usr/bin/mysql", "-h", h, "-P", p] + args[1:]
    args.append(db)
    r = subprocess.run(args, input=sql, capture_output=True, text=True)
    return (r.stdout + re.sub(r" at line \d+", "", r.stderr)).strip()


def check(label, got, want):
    global bad
    ok = got == want
    bad += not ok
    print(f"{label}: {'ok' if ok else 'MISMATCH'}  {got!r}" + ("" if ok else f"  expected {want!r}"))


def rows(text):
    """Normalise tab/pipe separated rows to lists of stripped strings."""
    return [[c.strip() for c in re.split(r"\t|\|", l)] for l in text.splitlines() if l.strip()]


def block_after(marker_or_title, lang="sql", start=0):
    i = md.index(marker_or_title, start)
    m = re.compile(r"^```" + lang + r"\n(.*?)^```$", re.S | re.M).search(md, i)
    return m.group(1), m.end()


def output_after(pos):
    m = re.compile(r"^```\n(.*?)^```$", re.S | re.M).search(md, pos)
    return m.group(1)


def norm(s):
    return [re.sub(r"\s+", " ", l).strip() for l in s.strip().splitlines()
            if l.strip() and not re.fullmatch(r"[-+ |]+", l.strip())]


def section(qid):
    a = md.index(f"### {qid} ")
    b = md.find("\n### ", a + 5)
    return md[a:b]


def first_block(text, lang):
    return re.search(r"^```" + lang + r"\n(.*?)^```$", text, re.S | re.M).group(1)


# ---------------------------------------------------------------- 1. view and index (PostgreSQL)
q49 = section("Q71-049")
view_blocks = re.findall(r"<!-- ch71-check: view -->\n```sql\n(.*?)```", q49, re.S)
view_out = re.search(r"LIMIT 3;\n```\n```\n(.*?)```", q49, re.S).group(1)
got = pg("BEGIN;\n" + view_blocks[0] + view_blocks[1] + "ROLLBACK;\n", fmt="")
check("Q71-049 view (pg, rolled back)", norm(got), norm(view_out))
check("Q71-049 view left no trace", pg("SELECT to_regclass('customer_revenue') IS NULL;"), "t")
view_select = view_blocks[0].split(" AS\n", 1)[1].rstrip().rstrip(";")
got_my = my(f"SELECT * FROM ({view_select}) v ORDER BY revenue DESC LIMIT 3;")
check("Q71-049 view query (mysql)", rows(got_my),
      [["1", "Sharma Hardware", "502775.00"], ["11", "Harbour Traders", "412680.50"],
       ["7", "Northgate Distributors", "353088.50"]])

q68 = section("Q71-068")
idx_blocks = re.findall(r"<!-- ch71-check: index -->\n```sql\n(.*?)```", q68, re.S)
explain_after = re.findall(r"^```\n( +QUERY PLAN\n.*?)^```$", q68, re.S | re.M)[1]
got = pg("BEGIN;\n" + idx_blocks[0] + idx_blocks[1] + "ROLLBACK;\n", fmt="")
check("Q71-068 EXPLAIN after index (pg, rolled back)", norm(got), norm(explain_after))
check("Q71-068 index left no trace", pg("SELECT to_regclass('idx_orders_customer') IS NULL;"), "t")

# ---------------------------------------------------------------- 2. MySQL versions give the same rows
def pg_rows(sql):
    return rows(pg(sql))


def my_rows(sql):
    # mysql -B prints NULL where psql -At prints nothing
    return [["" if c == "NULL" else c for c in r] for r in rows(my(sql))]


for qid in ("Q71-028", "Q71-042"):
    s = section(qid)
    check(f"{qid} mysql = pg", my_rows(first_block(s, "mysql")), pg_rows(first_block(s, "sql")))

def to_mysql(sql):
    return sql.replace("DATE_TRUNC('month', o.order_date)::date", "DATE_FORMAT(o.order_date, '%Y-%m-01')")

for qid in ("Q71-036", "Q71-075"):
    s = section(qid)
    p = first_block(s, "sql")
    check(f"{qid} mysql (DATE_FORMAT swap) = pg", my_rows(to_mysql(p)), pg_rows(p))
s = section("Q71-074")
p = re.findall(r"^```sql\n(.*?)^```$", s, re.S | re.M)[1]
check("Q71-074 mysql (DATE_FORMAT swap) = pg", my_rows(to_mysql(p)), pg_rows(p))
wrong = re.findall(r"^```sql\n(.*?)^```$", s, re.S | re.M)[0]
got = my(to_mysql(wrong))
check("Q71-074 mysql error wording", got.splitlines()[0],
      "ERROR 3593 (HY000): You cannot use the window function 'avg' in this context.'")
p = first_block(section("Q71-029"), "sql")
check("Q71-029 mysql = pg", my_rows(p), pg_rows(p))
check("Q71-029 mini database = riverstone_2025", pg_rows(p), rows(pg(p, db="riverstone")))
check("Q71-029 cte_max_recursion_depth", my("SELECT @@cte_max_recursion_depth;"), "1000")

# ---------------------------------------------------------------- 3. numbers stated in the text
u = "SELECT 1 AS x UNION ALL SELECT 1;"
check("Q71-006 UNION ALL keeps 2", len(pg_rows(u)), 2)
check("Q71-006 UNION keeps 1", len(pg_rows(u.replace("UNION ALL", "UNION"))), 1)
check("Q71-006 UNION (mysql)", (len(my_rows(u)), len(my_rows(u.replace("UNION ALL", "UNION")))), (2, 1))

pg("DROP DATABASE IF EXISTS scratch_ch71;", db="postgres")
pg("CREATE DATABASE scratch_ch71;", db="postgres")
my("CREATE DATABASE IF NOT EXISTS scratch_ch71;", db="mysql")
ident = """CREATE TABLE t (id INT GENERATED ALWAYS AS IDENTITY, v TEXT);
INSERT INTO t (v) VALUES ('a'), ('b');
TRUNCATE TABLE t;
INSERT INTO t (v) VALUES ('c');
SELECT id FROM t;
TRUNCATE TABLE t RESTART IDENTITY;
INSERT INTO t (v) VALUES ('d');
SELECT id FROM t;
DROP TABLE t;"""
check("Q71-012 pg TRUNCATE keeps counting, RESTART IDENTITY resets", pg(ident, db="scratch_ch71").split(), ["3", "1"])
ai = """DROP TABLE IF EXISTS t;
CREATE TABLE t (id INT AUTO_INCREMENT PRIMARY KEY, v TEXT);
INSERT INTO t (v) VALUES ('a'), ('b');
TRUNCATE TABLE t;
INSERT INTO t (v) VALUES ('c');
SELECT id FROM t;
DROP TABLE t;"""
check("Q71-012 mysql TRUNCATE resets AUTO_INCREMENT", my(ai, db="scratch_ch71"), "1")
nnd = """CREATE TABLE u (id INT, email VARCHAR(50) UNIQUE NULLS NOT DISTINCT);
INSERT INTO u VALUES (1, NULL);
INSERT INTO u VALUES (2, NULL);
DROP TABLE u;"""
got = pg(nnd, db="scratch_ch71")
check("Q71-013 NULLS NOT DISTINCT rejects the second NULL", got.splitlines()[0],
      'ERROR:  duplicate key value violates unique constraint "u_email_key"')
pg("DROP DATABASE scratch_ch71;", db="postgres")
my("DROP DATABASE scratch_ch71;", db="mysql")

g = "SELECT * FROM orders GROUP BY order_id ORDER BY order_id LIMIT 1;"
check("Q71-015 GROUP BY primary key runs (pg)", "ERROR" in pg(g), False)
check("Q71-015 GROUP BY primary key runs (mysql)", "ERROR" in my(g), False)

check("Q71-024 COUNT(*) vs COUNT(sales_rep_id)", pg("SELECT COUNT(*), COUNT(sales_rep_id) FROM orders;"), "175|164")
check("Q71-002 mini database has 1 NULL rep", pg("SELECT COUNT(*) - COUNT(sales_rep_id) FROM orders;", db="riverstone"), "1")
q27 = re.search(r"`(SELECT DATE_TRUNC\('month', order_date\)::date AS month, COUNT\(DISTINCT customer_id\) FROM orders GROUP BY 1)`", md).group(1)
check("Q71-027 distinct customers Jan-Mar (pg)", [r[1] for r in pg_rows(q27 + " ORDER BY 1 LIMIT 3;")], ["5", "8", "10"])
q27m = q27.replace("DATE_TRUNC('month', order_date)::date", "DATE_FORMAT(order_date, '%Y-%m-01')")
check("Q71-027 distinct customers Jan-Mar (mysql)", [r[1] for r in my_rows(q27m + " ORDER BY 1 LIMIT 3;")], ["5", "8", "10"])

ex = "SELECT COUNT(*) FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id);"
inn = "SELECT COUNT(*) FROM customers WHERE customer_id IN (SELECT customer_id FROM orders);"
check("Q71-030 EXISTS and IN both 23", (pg(ex), pg(inn), my(ex), my(inn)), ("23",) * 4)
check("Q71-001 24 customers = 23 + 1", pg("SELECT COUNT(*) FROM customers;"), "24")

inner = re.search(r"FROM \(\n(  SELECT p\.category.*?)\) t\nWHERE rn <= 2", section("Q71-035"), re.S).group(1)
r35 = pg_rows(inner)
check("Q71-035 inner query rows", len(r35), 8)
check("Q71-035 inner query sums to 2025 revenue", sum(Decimal(r[2]) for r in r35), Decimal("4335471.00"))

p = first_block(section("Q71-028"), "sql").replace("LIMIT 3;", ";")
rng = pg(p.replace("SELECT month, revenue", "SELECT month, SUM(revenue) OVER (ORDER BY month)"))
rws = pg(p.replace("SELECT month, revenue",
                   "SELECT month, SUM(revenue) OVER (ORDER BY month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)"))
check("Q71-037 RANGE = ROWS on monthly totals", rng == rws, True)

check("Q71-041 city does have duplicates", int(pg("SELECT COUNT(*) FROM (SELECT city FROM customers GROUP BY city HAVING COUNT(*) > 1) t;")) > 0, True)
check("Q71-023 Furniture sold 30 units", pg("SELECT SUM(oi.quantity) FROM order_items oi JOIN products p ON oi.product_id = p.product_id WHERE p.category = 'Furniture';"), "30")

never = ("SELECT p.product_name FROM products p LEFT JOIN order_items oi ON p.product_id = oi.product_id "
         "WHERE oi.product_id IS NULL;")
check("Q71-044 never sold (riverstone_2025)", pg(never), "")
check("Q71-044 never sold (mini riverstone)", pg(never, db="riverstone"), "Garden Chair")
check("Q71-044 8 products", pg("SELECT COUNT(*) FROM products;"), "8")

z = pg("SELECT COUNT(*), SUM(CASE WHEN pct = 0 THEN 1 ELSE 0 END) FROM "
       "(SELECT quantity / SUM(quantity) OVER () * 100 AS pct FROM order_items) t;")
n, zeros = z.split("|")
check("Q71-046 integer percent is 0 on every line (pg)", n == zeros, True)
check("Q71-046 mysql / gives a decimal", my("SELECT 1 / 3;"), "0.3333")

check("Q71-060 group_concat_max_len default", my("SELECT @@global.group_concat_max_len;"), "1024")

# Q71-074: customer 1's months before November, and the hand check
m = pg("""SELECT COUNT(DISTINCT DATE_TRUNC('month', order_date)) FROM orders
          WHERE customer_id = 1 AND status <> 'Cancelled' AND order_date < '2025-11-01';""")
check("Q71-074 customer 1 has 10 months before November", m, "10")
check("Q71-074 hand check", round((9 * Decimal("34443.89") + Decimal("96825")) / 10, 2), Decimal("40682.00"))

print(f"ch71_check: {'all ok' if not bad else f'{bad} mismatches'}")
sys.exit(1 if bad else 0)
