"""Chapter 67: recompute every number the chapter quotes and check every section it cites exists.

Run from the book folder:  python3 checks/ch67_numbers.py
Chapter 67 has no code of its own. Its numbers come from other chapters' files:
  companion/ch66/roi_case.csv          (Ch 66's business case: platform cost and the three savings)
  companion/ch65/unit_economics.csv    (Ch 65's fully loaded cost per 1,000 order lines)
  Ch 60 section 60.3: the NFR target of Rs 0.50 per 1,000 order lines.
  Ch 64's story: East region's response time, 41 hours to 6.
"""
import glob, re
from pathlib import Path
import pandas as pd

BOOK = Path(__file__).resolve().parent.parent
MS = BOOK / "manuscript"
TEXT = Path(glob.glob(str(MS / "ch67-*.md"))[0]).read_text(encoding="utf-8")
failures = []


def lakh(n: float) -> str:
    s = f"{abs(round(n)):d}"
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        s = ",".join([head[max(0, k - 2):k] for k in range(len(head), 0, -2)][::-1]) + "," + tail
    return s


def expect(label, value, *snippets):
    for s in snippets:
        if s not in TEXT:
            failures.append(f"{label}: '{s}' not in chapter (value {value})")
    print(f"{label:40s} {value}")


# ---- the board speech and the story (section 67.3, In the real world)
roi = pd.read_csv(BOOK / "companion/ch66/roi_case.csv").set_index("item_id").amount_rs
platform, flash, macro, po = roi.platform_cost, roi.flash, roi.macro, roi.po_intake
measured = flash + macro
with_po = measured + po
expect("platform cost a year", platform, f"₹{lakh(platform)} a year to run")
expect("measured savings (Flash + macro)", measured, f"₹{lakh(measured)} a year")
expect("PO intake, conditional", po, f"₹{lakh(po)}")
share = measured / platform * 100
share_po = with_po / platform * 100
expect("measured share of cost, %", round(share, 1), f"{share:.0f}%", "about a fifth")
assert 19 <= share <= 23, share                      # "about a fifth"
expect("share with PO intake, %", round(share_po, 1), f"{share_po:.0f}%")
assert 40 <= share_po < 50, share_po                 # "close to half"

# ---- the NFR gap (Ch 65's story), quoted as "about 10,000 times"
ue = pd.read_csv(BOOK / "companion/ch65/unit_economics.csv").set_index("metric").value_inr
per1000 = ue["per 1,000 order lines"]
gap = per1000 / 0.50
expect("NFR gap (fully loaded / Rs 0.50)", round(gap), "about 10,000 times")
assert 9_000 <= gap <= 11_000, gap

# ---- facts quoted from other chapters
ch64 = Path(glob.glob(str(MS / "ch64-*.md"))[0]).read_text(encoding="utf-8")
assert "from 41 hours to 6" in ch64 and "from 41 hours to 6" in TEXT
print(f"{'East response time 41 h -> 6 h':40s} in Ch 64 and Ch 67")
ch20 = Path(glob.glob(str(MS / "ch20-*.md"))[0]).read_text(encoding="utf-8")
assert "325 hours" in ch20

# ---- every "Chapter NN, section NN.M" / "section NN.M" cited must exist
def sections(ch):
    t = Path(glob.glob(str(MS / f"ch{ch:02d}-*.md"))[0]).read_text(encoding="utf-8")
    return set(re.findall(rf"^## ({ch}\.\d+)\b", t, flags=re.M))

cited = set(re.findall(r"section (\d+)\.(\d+)", TEXT))
for ch, n in sorted(cited, key=lambda x: (int(x[0]), int(x[1]))):
    ok = f"{ch}.{n}" in sections(int(ch))
    print(f"{'section ' + ch + '.' + n:40s} {'exists' if ok else 'MISSING'}")
    if not ok:
        failures.append(f"section {ch}.{n} cited but not found")

# ---- the figures the chapter points to
for fig in ["Figure 66.2"]:
    ch66 = Path(glob.glob(str(MS / "ch66-*.md"))[0]).read_text(encoding="utf-8")
    assert f"*{fig} —" in ch66, fig
    print(f"{fig:40s} exists in Ch 66")

print("ALL OK" if not failures else "\n".join(failures))
raise SystemExit(1 if failures else 0)
