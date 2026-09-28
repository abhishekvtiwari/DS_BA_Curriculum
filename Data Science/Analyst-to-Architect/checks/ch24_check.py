"""Chapter 24 checks. The chapter has no code blocks, so this checks every number it prints instead.

    python3 checks/ch24_check.py            # from the book folder (Data Science/Analyst-to-Architect)

1. Computes the December example (companion/ch24/build_ch24_files.py, dec_dip) from companion/full,
   and recomputes the same totals in SQL on PostgreSQL and MySQL riverstone_full: they must agree.
2. Checks that every number the chapter prints for the example (section 24.1 table, BLUF, memo,
   Figure 24.3, answers) appears in the chapter exactly as computed.
3. Checks the numbers quoted from Chapter 21 (delivery times) and Chapter 23 (marketing) against
   their companion data, and the weekdays in "In the real world".
4. Regenerates the companion files and checks they are unchanged (they come from the script).
Exit code 0 if everything passes.
"""
import datetime, subprocess, sys
from pathlib import Path

import pandas as pd

BOOK = Path(__file__).resolve().parents[1]
MD = next((BOOK / "manuscript").glob("ch24-*.md")).read_text(encoding="utf-8")
C24 = BOOK / "companion" / "ch24"
sys.path.insert(0, str(C24))
from build_ch24_files import dec_dip, cr  # noqa: E402

ok = True


def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(("PASS " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))


def in_md(s):
    check(f"chapter prints {s!r}", s in MD)


n = dec_dip()
b, nov, dec = n["bridge"], n["nov"], n["dec"]

# 1. the same totals from SQL, both engines
SQL = """SELECT DATE_FORMAT_M AS m, COUNT(DISTINCT o.customer_id), COUNT(DISTINCT o.order_id),
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct / 100)), 2)
FROM orders o JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status <> 'Cancelled' AND o.order_date >= '2025-11-01' AND o.order_date < '2026-01-01'
GROUP BY m ORDER BY m;"""
runs = {
    "PostgreSQL": (["su", "postgres", "-c", "psql -d riverstone_full -At -F '|' -f -"], SQL.replace("DATE_FORMAT_M", "to_char(o.order_date, 'YYYY-MM')")),
    "MySQL": (["mysql", "-uroot", "riverstone_full", "-N", "-B"], SQL.replace("DATE_FORMAT_M", "DATE_FORMAT(o.order_date, '%Y-%m')")),
}
for engine, (cmd, q) in runs.items():
    out = subprocess.run(cmd, input=q, capture_output=True, text=True).stdout.strip().splitlines()
    rows = [r.replace("\t", "|").split("|") for r in out]
    want = [["2025-11", str(nov["customers"]), str(nov["orders"]), f"{nov['revenue']:.2f}"],
            ["2025-12", str(dec["customers"]), str(dec["orders"]), f"{dec['revenue']:.2f}"]]
    check(f"{engine} riverstone_full agrees with companion/full for Nov and Dec 2025", rows == want, f"{rows} vs {want}")

# the decomposition adds up exactly
check("three effects sum to the total change", abs(b["customer"] + b["frequency"] + b["aov"] - b["total"]) < 0.01)

# 2. every printed number
for s in [f"| Active customers | {nov['customers']:,} | {dec['customers']:,} |",
          f"| Orders | {nov['orders']:,} | {dec['orders']:,} |",
          f"| Orders per customer | {nov['opc']:.3f} | {dec['opc']:.3f} |",
          f"| Average order value (AOV) | ₹{nov['aov']:,.2f} | ₹{dec['aov']:,.2f} |",
          f"| Net revenue | ₹{cr(nov['revenue'])} crore | ₹{cr(dec['revenue'])} crore |",
          f"Revenue fell ₹{cr(b['total'])} crore, or {abs(n['pct']):.1f}%",
          f"fewer customers −₹{cr(b['customer'])} crore, fewer orders per customer −₹{cr(b['frequency'])} crore, and smaller orders (lower AOV) −₹{cr(b['aov'])} crore, which is {n['aov_share']:.0f}% of the fall",
          f"December's revenue fall ({abs(n['pct']):.0f}%, to ₹{cr(dec['revenue'])} crore)",
          f"Revenue fell from ₹{cr(nov['revenue'])} crore to ₹{cr(dec['revenue'])} crore",
          f"average order value accounted for ₹{cr(b['aov'])} crore of the ₹{cr(b['total'])} crore fall",
          f"December's ₹{cr(dec['revenue'])} crore is {abs(n['pct']):.1f}% below November's ₹{cr(nov['revenue'])} crore",
          f"customers contributed −₹{cr(b['customer'])} crore, orders per customer −₹{cr(b['frequency'])} crore, and average order value −₹{cr(b['aov'])} crore — AOV drove {n['aov_share']:.0f}% of the fall",
          f"The shape mirrors the May-to-June dip earlier in the year (−{abs(n['pct_may_jun']):.1f}%)"]:
    in_md(s)
sh = lambda k, s: f"{n[k]['segment_share'][s]:.1f}%"
in_md(f"Retail's share of orders went from {sh('nov','Retail')} to {sh('dec','Retail')}, Wholesale's from {sh('nov','Wholesale')} to {sh('dec','Wholesale')}, and Hospitality's from {sh('nov','Hospitality')} to {sh('dec','Hospitality')}")
y = n["dec_fall_by_year"]
in_md(f"by {abs(y[2023]):.1f}% in 2023, {abs(y[2024]):.1f}% in 2024, and {abs(y[2025]):.1f}% in 2025")
check("two-thirds / one-third split", 64 < n["aov_share"] < 70 and 30 < 100 - n["aov_share"] < 36, f"{n['aov_share']:.1f}")
check("AOV fell in every segment", all(dec["segment_aov"][s] < nov["segment_aov"][s] for s in nov["segment_aov"]))
check("December fell from November in every year of the data", all(v < 0 for v in y.values()))
for a_, b_ in (("nov", "dec"), ("may", "jun")):
    moves = [abs(n[b_]["segment_share"][s] - n[a_]["segment_share"][s]) for s in n[a_]["segment_share"]]
    check(f"segment mix {a_} -> {b_} moves under 2 points (the 'mix unchanged' claim)", max(moves) < 2, f"{moves}")

# 3. numbers quoted from Chapter 21 and Chapter 23
d = pd.read_csv(BOOK / "companion" / "ch21" / "delivery_times_2025.csv", parse_dates=["order_date"])
k = d[d.branch == "Kolkata"].delivery_days; m = d[d.branch == "Mumbai HO"].delivery_days
iqr = lambda x: x.quantile(.75) - x.quantile(.25)
in_md(f"median {k.median():.1f} days against Mumbai HO's {m.median():.1f}; interquartile range {iqr(k):.1f} days against {iqr(m):.1f}; 95th percentile {k.quantile(.95):.1f} days against {m.quantile(.95):.1f}; {d[d.branch == 'Kolkata'].on_time.mean() * 100:.1f}% of orders inside the 7-day promise")
fest = d.order_date.dt.month.isin([10, 11])
a, o_ = d[fest].delivery_days, d[~fest].delivery_days
in_md(f"(Chapter 21, Exercise 23: {a.median():.1f} against {o_.median():.1f} days, and {a.quantile(.95):.1f} against {o_.quantile(.95):.1f})")
in_md(f"{a.median() - o_.median():.1f} days slower at the median and {a.quantile(.95) - o_.quantile(.95):.1f} days slower at the 95th percentile")
in_md(f"are met for {d.on_time.mean() * 100:.0f}% of orders, but only {d[d.branch == 'Kolkata'].on_time.mean() * 100:.0f}% in Kolkata")
mk = pd.read_csv(BOOK / "companion" / "ch23" / "marketing_2025.csv")
best = mk.loc[mk.cac.idxmin()]
check("March has the lowest CAC and the highest ROAS of 2025",
      best.month == "2025-03" and mk.loc[mk.roas.idxmax()].month == "2025-03")
in_md(f"ROAS {best.roas:.1f}x and CAC ₹{best.cac:,.0f}, the best of the year on both")
for day, name in [((2026, 1, 2), "Friday 2 January"), ((2026, 1, 8), "Thursday the 8th"), ((2026, 1, 9), "Friday the 9th")]:
    check(f"{name} is a {datetime.date(*day):%A}", name.split()[0] == f"{datetime.date(*day):%A}")
    in_md(name)
check("Monday 12 January 2026 is a Monday", datetime.date(2026, 1, 12).weekday() == 0)

# 4. companion files come from the script
before = {p.name: p.read_bytes() for p in C24.glob("*.md")}
subprocess.run([sys.executable, "build_ch24_files.py"], cwd=C24, check=True, capture_output=True)
after = {p.name: p.read_bytes() for p in C24.glob("*.md")}
check("companion files are exactly what build_ch24_files.py writes", before == after)

print("ALL PASS" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
