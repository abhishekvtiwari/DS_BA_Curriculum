"""Ch 76A has no code; this checks that every number its answers quote matches the chapter it comes from.

Run from the book folder:  python3 checks/ch76a_numbers.py
"""
import pathlib
import re

M = pathlib.Path(__file__).resolve().parent.parent / "manuscript"


def text(prefix):
    return next(M.glob(prefix + "-*.md")).read_text(encoding="utf-8")


ch36, ch37, ch39, ch44 = text("ch36"), text("ch37"), text("ch39"), text("ch44")
checks = {
    "Ch 36 target is won within 90 days": "Won within 90 days" in ch36,
    "Ch 36 rule test AUC 0.727": "rule (3 sources):     AUC 0.727" in ch36,
    "Ch 36 referral 19.33% / marketplace 2.98% (2023-24)": re.search(r"Referral\s+838\s+290\s+19\.33", ch36) and re.search(r"Marketplace\s+2381\s+1516\s+2\.98", ch36),
    "Ch 37 test logistic 0.838": "TEST  logistic (Ch 36)   AUC 0.838   log loss 0.2369" in ch37,
    "Ch 37 test boosting 0.830": "TEST  tuned boosting     AUC 0.830   log loss 0.2422" in ch37,
    "Ch 37 576 wins in training": "7,291 training leads, 576 won" in ch37,
    "Ch 39 work cost 1500": "WORK_COST = 1500" in ch39,
    "Ch 39 win value 30,255 and break-even 0.0496": "₹30,255" in ch39 and "0.0496" in ch39,
    "Ch 44 term 'expected margin at risk'": "expected margin at risk" in ch44,
    "Ch 44 capacity 40": "CAPACITY = 40" in ch44,
    "Ch 44 target: no order in 2025": "place no order in 2025" in ch44,
}
for name, ok in checks.items():
    print(("OK   " if ok else "FAIL ") + name)
print(f"7% -> 12%: {12 - 7} percentage points, {(12 - 7) / 7:.1%} relative")
