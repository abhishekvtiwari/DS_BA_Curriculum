"""Recompute every number Chapter 60 states in prose, figures and companion files.

Run from the book folder:  python3 checks/ch60_check.py
Each check prints PASS or FAIL; the exit code is 1 if anything fails."""
import pathlib, re, sys

BOOK = pathlib.Path(__file__).resolve().parents[1]
CH = (BOOK / "manuscript/ch60-designing-whole-systems.md").read_text(encoding="utf-8")
FIG = {p.name: p.read_text(encoding="utf-8") for p in (BOOK / "figures").glob("fig60-*.svg")}
WORKSHEET = (BOOK / "companion/ch60/nfr-worksheet.md").read_text(encoding="utf-8")
fails = 0

def check(label, ok):
    global fails
    print(("PASS " if ok else "FAIL ") + label)
    fails += not ok

def in_text(s, where=CH):
    return s in where

# Availability ("nines"): a year of 365 days
minutes = 365 * 24 * 60
check("minutes in a year 525,600", minutes == 525_600 and in_text("525,600"))
check("99.9% is 525.6 minutes, about 8.76 hours", round(minutes * 0.001, 1) == 525.6
      and round(minutes * 0.001 / 60, 2) == 8.76 and in_text("about 8.76 hours"))
def down(a): return minutes * (100 - a) / 100
check("99.95% a month 21.9 minutes (answer 11)", round(down(99.95) / 12, 1) == 21.9 and in_text("21.9 minutes a month"))
check("99.5% a month 3.65 hours", round(down(99.5) / 12 / 60, 2) == 3.65 and in_text("3.65 hours"))
check("3.65 h is ten times 21.9 min", round((down(99.5) / 12) / (down(99.95) / 12)) == 10 and in_text("ten times less"))
rows = {"99%": (down(99) / 60, "hours", down(99) / 12 / 60, "hours"),
        "99.5%": (down(99.5) / 60, "hours", down(99.5) / 12 / 60, "hours"),
        "99.9%": (down(99.9) / 60, "hours", down(99.9) / 12, "minutes"),
        "99.95%": (down(99.95) / 60, "hours", down(99.95) / 12, "minutes"),
        "99.99%": (down(99.99), "minutes", down(99.99) / 12, "minutes")}
for level, (y, yu, m, mu) in rows.items():
    line = re.search(rf"^\| {re.escape(level)} \| ~([\d.]+) (\w+)(?: \([^)]*\))? \| ~([\d.]+) (\w+) \|", WORKSHEET, re.M)
    ok = bool(line) and abs(float(line.group(1)) - y) < 0.06 and line.group(2) == yu \
         and abs(float(line.group(3)) - m) < 0.06 and line.group(4) == mu
    check(f"worksheet row {level}", ok)
check("worksheet 99% 3.65 days, 99.5% 1.8 days a year", round(down(99) / 60 / 24, 2) == 3.65
      and round(down(99.5) / 60 / 24, 1) == 1.8 and "(3.65 days)" in WORKSHEET and "(1.8 days)" in WORKSHEET)

# Reliability as a count
check("one failed run in 30 is 3.3%, success 96.7%", f"{1/30:.1%}" == "3.3%" and f"{1-1/30:.1%}" == "96.7%"
      and in_text("3.3% of the month") and in_text("96.7%"))
check("99.5% of 365 runs allows 1.8 failures", round(365 * 0.005, 1) == 1.8 and in_text("1.8 failures"))

# p95 by hand (Chapter 21's position rule)
sent = sorted([12, 9, 15, 11, 10, 14, 13, 9, 11, 42, 12, 10, 16, 11, 13, 12, 9, 18, 10, 14])
pos = 1 + 0.95 * (len(sent) - 1)
p95 = sent[18] + (pos - 19) * (sent[19] - sent[18])
check("position 19.05", round(pos, 2) == 19.05 and in_text("= 19.05"))
check("19th value 18, 20th 42", sent[18] == 18 and sent[19] == 42)
check("p95 by hand 19.2", round(p95, 1) == 19.2 and in_text("18 + 0.05 × 24 = 19.2"))

# Sensor archive (Chapters 48 and 49)
check("25 machines x 8,640 readings = 216,000 a day", 25 * 8640 == 216_000 and 86_400 // 10 == 8640
      and "216,000" in FIG["fig60-5-adr-example.svg"])
check("92 days of 216,000 = 19.87 million", 92 * 216_000 == 19_872_000 and "19.87 million" in FIG["fig60-5-adr-example.svg"])
check("11 fixed + 8 missing + 23 uncorrected = 42 days (six weeks)", 11 + 8 + 23 == 42 == 6 * 7)

# Consistency with the fixed facts of Parts 2, 5 and 6
for s in ["07:30 IST", "06:30", "previous working day", "₹1,00,000", "19% silent-error rate", "`ap-south-1`"]:
    check(f"chapter states {s}", in_text(s))
for s in ["Postgres", "Zoho", "fourteen", "Appendix G", "2026", "6:03", "four AI-adjacent", "System Design Question Bank"]:
    check(f"chapter no longer says {s!r}", not in_text(s))
check("figures no longer say Postgres or Zoho", not any("Postgres" in f or "Zoho" in f for f in FIG.values()))

print("all passed" if not fails else f"{fails} failed")
sys.exit(1 if fails else 0)
