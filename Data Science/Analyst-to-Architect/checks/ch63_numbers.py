"""Chapter 63: recompute every number the chapter quotes, and check the inventory.

Run from the book folder:  python3 checks/ch63_numbers.py
Inputs come from the chapters they are quoted from:
  Ch 19: the macro runs once a quarter; 4 minutes before the rewrite, 9 seconds after.
  Ch 20 section 20.14: 80 minutes -> 2 minutes, 250 runs a year, Rs 300 an hour.
  Ch 58 section 58.7: 60 emails, 53 loaded unattended, 10 of them wrong; 40 emails a day;
        3 minutes to type, 0.75 to review, 2 to handle a queued email; Rs 300 an hour;
        Rs 2,000 per wrong order; review catch rate 0.9 (an assumption).
"""
import csv
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DAYS = 250                                   # working days a year (Ch 20 section 20.14)
RATE = 300                                   # loaded cost per hour (Ch 20, Ch 58)


def lakh(n: float) -> str:
    """Indian digit grouping, whole rupees: 3195000 -> '31,95,000'."""
    s = f"{abs(round(n)):d}"
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = [head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]
        s = ",".join(parts) + "," + tail
    return ("-" if n < 0 else "") + s


# ---- Ch 20: the Flash
flash_hours = (80 - 2) * DAYS / 60
assert flash_hours == 325
assert flash_hours * RATE == 97_500
print(f"Flash: {flash_hours:.0f} h/yr, Rs {lakh(flash_hours * RATE)} a year")

# ---- Ch 19: the macro, four runs a year
minutes_saved = (4 * 60 - 9) * 4 / 60
print(f"Macro: {minutes_saved:.1f} minutes a year saved, Rs {minutes_saved / 60 * RATE:.0f} a year")
assert round(minutes_saved) == 15

# ---- Ch 58: PO intake, per day
EMAILS, LOADED, WRONG, TOTAL = 40, 53, 10, 60
straight = LOADED / TOTAL
error_rate = WRONG / LOADED
queue = 1 - straight
labour = {"manual": EMAILS * 3.0 / 60 * RATE,
          "assisted": (EMAILS * 0.75 + EMAILS * queue * 2.0) / 60 * RATE,
          "straight": EMAILS * queue * 2.0 / 60 * RATE}
unseen = EMAILS * straight * error_rate          # wrong orders a day nobody looks at
missed = unseen * (1 - 0.9)                      # the ones a reviewer misses
print({k: round(v) for k, v in labour.items()}, f"unseen {unseen:.2f}, missed {missed:.2f}")
assert [round(v) for v in labour.values()] == [600, 197, 47]
assert round(unseen * 2000) == 13_333 and round(missed * 2000) == 1_333
assisted_total = labour["assisted"] + missed * 2000
straight_total = labour["straight"] + unseen * 2000
assert round(assisted_total) == 1_530 and round(straight_total) == 13_380
print(f"loaded unattended a day {EMAILS * straight:.1f}; wrong {unseen:.2f}")
assert f"{EMAILS * straight:.1f}" == "35.3" and f"{unseen:.1f}" == "6.7"

# expected daily value against typing = labour saved - wrong orders a day x Rs 2,000
ev_straight = (labour["manual"] - labour["straight"]) - unseen * 2000
ev_assisted = {c: (labour["manual"] - labour["assisted"]) - unseen * (1 - c) * 2000
               for c in (0.9, 0.97, 0.99)}
print(f"expected value a day: straight {ev_straight:,.0f}; assisted",
      {c: round(v) for c, v in ev_assisted.items()})
assert round(labour["manual"] - labour["straight"]) == 553
assert round(labour["manual"] - labour["assisted"]) == 403
assert round(ev_straight) == -12_780
assert round(ev_assisted[0.9]) == -930 and round(ev_assisted[0.99]) == 270
catch_needed = 1 - (labour["manual"] - labour["assisted"]) / (unseen * 2000)
print(f"assisted breaks even with typing at a catch rate of {catch_needed:.1%}")
assert round(catch_needed * 100) == 97

# per year, 250 working days (whole-rupee daily figures, as the chapter prints them)
year = {"assisted labour saved": (600 - 197) * DAYS,
        "assisted, counting missed errors": (600 - 1_530) * DAYS,
        "straight through": (600 - 13_380) * DAYS}
for k, v in year.items():
    print(f"{k}: Rs {lakh(v)} a year")
assert year["assisted labour saved"] == 100_750
assert year["assisted, counting missed errors"] == -232_500
assert year["straight through"] == -3_195_000

# ---- the inventory behind Figure 63.4
rows = list(csv.DictReader(open(HERE / "companion/ch63/automation-inventory.csv", encoding="utf-8")))
counts = Counter(r["audit_category"] for r in rows)
print(len(rows), dict(counts))
assert len(rows) == 24
assert counts == {"documented and owned": 6, "working but no owner": 11,
                  "duplicated logic": 4, "single point of failure": 1, "actively broken": 2}
ungoverned = counts["working but no owner"] + counts["duplicated logic"] + counts["actively broken"]
assert ungoverned == 17 and len(rows) == 3 * 8          # 24 = three times Ch 60's eight containers

# the scores printed in section 63.2's table and plotted in Figure 63.1
plotted = {"Daily Sales Flash": (4, 1, 1), "Branch consolidation macro (MASTER_FINAL_v7)": (3, 1, 1),
           "PO intake (assisted)": (4, 3, 3), "Dagster ingestion pipeline": (5, 5, 3),
           "CRM reverse-ETL syncs": (3, 3, 3)}
by_name = {r["automation_name"]: r for r in rows}
for name, (v, e, k) in plotted.items():
    r = by_name[name]
    assert (int(r["value_score"]), int(r["effort_score"]), int(r["risk_score"])) == (v, e, k), name
cats = {r["tool_category"] for r in rows}
print("tool categories used:", sorted(cats))
assert "RPA" not in cats and "iPaaS" not in cats             # the two honest gaps in section 63.3
print("all Chapter 63 numbers check out")
