"""Chapter 80: recompute every number the chapter quotes, and check its IDs and pointers.

Run from the book folder:  python3 checks/ch80_check.py
Inputs:
  Q80-016: 3 hours saved a run, 52 runs a year, Rs 300 an hour (Ch 20 section 20.14),
           Rs 60,000 one-time build, 2 hours of maintenance a month.
  Q80-022 / In the real world: 1 incident + 14 unmonitored automations = 15.
  Ch 61 section 61.5: quorum N=3, W=2, R=2.
  Ch 62 section 62.6: mesh maturity 1+2+2+3+1 = 9 of 25.
Every "Learn it in" section number is checked against the heading in the cited chapter.
"""
import re
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
MS = BOOK / "manuscript"
CH80 = next(MS.glob("ch80-*.md")).read_text(encoding="utf-8")
ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok &= good
    print(f"{'OK ' if good else 'BAD'} {label}: {got!r} (want {want!r})")


# ---- Q80-016: ROI and payback
hours, runs, rate, build, maint = 3, 52, 300, 60_000, 2
annual = hours * runs * rate
payback = build / (annual / 12)
net = annual - maint * 12 * rate
net_payback = build / (net / 12)
check("annual savings", f"₹{annual:,.0f}", "₹46,800")
check("payback months", f"{payback:.1f}", "15.4")
check("net annual", f"₹{net:,.0f}", "₹39,600")
check("net payback months", f"{net_payback:.1f}", "18.2")
check("maintenance a year", maint * 12 * rate, 7_200)
check("three years net saving", 3 * net, 118_800)   # written ₹1,18,800
check("three years net gain", 3 * net - build, 58_800)
check("build cost in hours at Rs 300", build / rate, 200.0)
for s in ["₹46,800", "15.4 months", "₹39,600", "18.2 months", "₹1,18,800", "₹58,800"]:
    check(f"chapter quotes {s}", s in CH80, True)

# ---- story arithmetic and quorum
check("fifteen single points of failure", 1 + 14, 15)
check("quorum overlap W+R>N", 2 + 2 > 3, True)
check("mesh maturity total", 1 + 2 + 2 + 3 + 1, 9)

# ---- IDs: unique, and every ID in the revision list exists
ids = re.findall(r"^(?:### |\| )(Q80-\d{3})", CH80, re.M)
check("IDs unique", len(ids) == len(set(ids)), True)
check("IDs 001..068 all present", sorted(ids) == [f"Q80-{i:03d}" for i in range(1, 69)], True)
rev = CH80.split("## Final-week revision list")[1].split("##")[0]
check("revision list IDs exist", all(i in ids for i in re.findall(r"Q80-\d{3}", rev)), True)

# ---- section pointers: "Chapter NN, section NN.N" and "NN.N" in the rapid-fire level column
heads = {}
for f in MS.glob("ch*.md"):
    for m in re.finditer(r"^#{2,3} (\d+[AB]?\.\d+) ", f.read_text(encoding="utf-8"), re.M):
        heads[m.group(1)] = f.name
cited = set(re.findall(r"sections? (\d{2}\.\d+)", CH80))
cited |= set(re.findall(r"(?:and|,|;) (\d{2}\.\d+)\b", CH80))
cited |= set(re.findall(r"· (\d{2}\.\d+)", CH80))
missing = sorted(c for c in cited if c not in heads and not c.startswith("80."))
check("every cited section exists", missing, [])
print("cited sections:", ", ".join(sorted(cited, key=lambda s: [int(x) for x in s.split('.')])))

print("ALL OK" if ok else "SOME CHECKS FAILED")
raise SystemExit(0 if ok else 1)
