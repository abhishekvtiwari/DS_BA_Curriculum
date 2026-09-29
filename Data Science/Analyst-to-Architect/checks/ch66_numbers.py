"""Chapter 66: recompute every number the chapter quotes and check it appears in the text.

Run from the book folder:  python3 checks/ch66_numbers.py
Inputs come from the files and chapters they are quoted from:
  companion/ch66/maturity_scorecard.csv, companion/ch66/roi_case.csv (built by build_ch66_files.py)
  companion/ch65/monthly_cost_model.csv (Ch 65's monthly platform cost)
  Ch 20 section 20.14: 325 hours a year at Rs 300 an hour.
  Ch 19: the macro runs once a quarter; 240 s before the rewrite, 9 s after.
  Ch 58 section 58.7 / Ch 63: Rs 600 typing vs Rs 197 assisted a day; 250 working days;
        Rs -2,32,500 a year at a 90% catch rate (Ch 63).
  Ch 53: Rs 4,000 per missed defect.
"""
import glob
from pathlib import Path
import pandas as pd

BOOK = Path(__file__).resolve().parent.parent
TEXT = Path(glob.glob(str(BOOK / "manuscript" / "ch66-*.md"))[0]).read_text(encoding="utf-8")
failures = []


def lakh(n: float) -> str:
    s = f"{abs(round(n)):d}"
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        s = ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail
    return ("-" if n < 0 else "") + s


def expect(label, value, *snippets):
    for s in snippets:
        if s not in TEXT:
            failures.append(f"{label}: '{s}' not in chapter (value {value})")
    print(f"{label:38s} {value}")


# ---- maturity
m = pd.read_csv(BOOK / "companion/ch66/maturity_scorecard.csv")
m["score"] = m.stage_met + m.next_met / 5
for d, s in zip(m.dimension, m.score):
    expect(f"score {d}", round(s, 1), f"| {d} | {s:.1f} |")
expect("average", f"{m.score.mean():.2f}", f"average score: {m.score.mean():.2f}")
assert m.loc[m.score.idxmin(), "dimension"] == "Catalog & discoverability"
assert sorted(m.score)[1] == 2.2  # culture second-lowest (exercise 12)
assert (m.dimension == "Data quality & reliability").any() and m.loc[0, "score"] == 3.6

# ---- ROI
cost65 = pd.read_csv(BOOK / "companion/ch65/monthly_cost_model.csv")
monthly = int(cost65.monthly_inr.sum())
platform = monthly * 12
flash, macro, po = 325 * 300, round(4 * (240 - 9) / 3600 * 300), (600 - 197) * 250
roi = pd.read_csv(BOOK / "companion/ch66/roi_case.csv").set_index("item_id")
assert roi.amount_rs.to_dict() == {"platform_cost": platform, "flash": flash, "macro": macro,
                                   "po_intake": po, "hire_salary": 900000}, roi
measured = flash + macro
with_po = measured + po
expect("monthly platform", monthly, f"₹{monthly:,} a month")
expect("platform annual", platform, f"₹{lakh(platform)}")
expect("flash", flash, "₹97,500")
expect("macro", macro, f"₹{macro} a year")
expect("po intake", po, f"₹{lakh(po)}")
expect("measured", measured, f"₹{lakh(measured)}", f"{measured / platform * 100:.0f}%")
expect("with po", with_po, f"₹{lakh(with_po)}", f"{with_po / platform * 100:.0f}%")
expect("po at 90% catch (Ch 63)", (600 - 1530) * 250, f"₹{lakh(-(600 - 1530) * 250)}")
# ---- hire
floor = 20 * 1 * 50 * 300
expect("hire floor", floor, f"₹{floor / 1e5:.2f} lakh", f"{floor / 900000 * 100:.0f}% of the salary")
half = 20 * 0.5 * 50 * 300
expect("hire floor at 0.5 h", half, f"₹{half / 1e5:.2f} lakh, {half / 900000 * 100:.0f}%")
# ---- answer 13
defect = 150000
expect("answer 13 misses", defect / 4000, "37.5", "about 38")
expect("answer 13 total", with_po + defect, f"₹{lakh(with_po + defect)}",
       f"about {(with_po + defect) / platform * 100:.0f}%")

print("\nFAILURES:" if failures else "\nall numbers found in the chapter")
for f in failures:
    print(" ", f)
raise SystemExit(1 if failures else 0)
