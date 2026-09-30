#!/usr/bin/env python3
"""ch74_check.py - checks Chapter 74 (Machine Learning Question Bank) against the chapters it cites.

Usage: python3 checks/ch74_check.py        (run from the book folder)

1. Every section number cited in Ch 74 ("section 37.6", "sections 36.3", "| Mid · 37.10", ...)
   exists as a "## NN.M" heading in the current manuscript.
2. Every number Ch 74 quotes from another chapter appears inside the section it is credited to.
3. The arithmetic Ch 74 does itself (base rates, precision/recall/F1, macro/weighted F1,
   adjusted R², the 0.5-threshold accuracies) is recomputed.
Exit code 1 on any failure.
"""
import glob, re, sys

MS = "manuscript"
ch74 = open(glob.glob(f"{MS}/ch74-*.md")[0], encoding="utf-8").read()
fails = 0


def chapter(n):
    return open(glob.glob(f"{MS}/ch{n}-*.md")[0], encoding="utf-8").read()


def section(n, sec):
    """Text of section 'n.sec' (from its ## heading to the next ## heading)."""
    text = chapter(n)
    m = re.search(rf"^## {n}\.{sec} .*?(?=^## )", text, re.S | re.M)
    return m.group(0) if m else None


def ok(cond, msg):
    global fails
    if not cond:
        fails += 1
        print("FAIL:", msg)


# 1. every cited section exists
cited = set()
for m in re.finditer(r"sections? ((?:\d{2}\.\d{1,2}(?:–\d{2}\.\d{1,2})?(?:,? (?:and )?)?)+)", ch74):
    cited.update(re.findall(r"\d{2}\.\d{1,2}", m.group(1)))
for m in re.finditer(r"· ([\d.;, a-z()`\"A-Z]+?) \|$", ch74, re.M):   # rapid-fire "Level · 37.2" cells
    cited.update(re.findall(r"\b\d{2}\.\d{1,2}\b", m.group(1)))
cited = {c for c in cited if not c.startswith("74.")}
for c in sorted(cited, key=lambda s: tuple(map(int, s.split(".")))):
    n, sec = c.split(".")
    ok(section(n, sec) is not None, f"section {c} not found")
print(f"sections cited: {len(cited)}")

# 2. quoted numbers are in the credited section
QUOTES = [
    ("35", "8", ["np.argmax"]),
    ("35", "9", ["Installing scikit-learn"]),
    ("37", "0", ["484 of 5,000", "9.7%", "Two ways to be wrong"]),
    ("37", "1", ["0.9546", "0.9593"]),
    ("37", "2", ["Figure 37.2", "14 at 0.001, 5 at 0.01", "1 at 0.2"]),
    ("37", "3", ["setting C"]),
    ("37", "4", ["AUC 0.765", "AUC 0.633"]),
    ("37", "6", ["train AUC 0.696   valid AUC 0.651   leaves 2", "train AUC 0.759   valid AUC 0.708   leaves 4",
                 "train AUC 0.791   valid AUC 0.752   leaves 8", "train AUC 0.829   valid AUC 0.748   leaves 16",
                 "train AUC 0.865   valid AUC 0.750   leaves 29", "train AUC 0.886   valid AUC 0.733   leaves 48",
                 "train AUC 0.934   valid AUC 0.672   leaves 97", "train AUC 0.969   valid AUC 0.609   leaves 161",
                 "train AUC 0.994   valid AUC 0.543   leaves 230", "train AUC 1.000   valid AUC 0.557   leaves 277"]),
    ("37", "7", ["n_estimators=300, min_samples_leaf=5", "days_since_last_order", "late_payment_days", "feature_importances_"]),
    ("37", "10", ["gap 0.013", "train AUC 0.945   CV AUC 0.836", "0.807 to **0.849**", "Fixing bias with features"]),
    ("37", "11", ["test AUC 0.797", "test AUC 0.850", "test AUC 0.838"]),
    ("37", "12", ["TEST  logistic (Ch 36)   AUC 0.838", "TEST  tuned boosting     AUC 0.830", "additive"]),
    ("36", "3", ["30.1", "44.5", "halved"]),
    ("36", "4", ['handle_unknown="ignore"']),
    ("36", "5", ["Cross-validation"]),
    ("36", "6", ["np.log1p", "8.9% vs other months 6.4%", "interaction", "as of the prediction moment", "Aggregates from activity logs", "high cardinality"]),
    ("36", "7", ["AUC 0.978", "AUC 0.845", "TargetEncoder inside the pipeline: AUC 0.823", "A leakage checklist", "Contamination"]),
    ("36", "8", ["5.71%", "8.06%"]),
    ("36", "9", ["mean AUC 0.82", "mean AUC 0.78"]),
    ("36", "10", ["Back to the random split", "AUC 0.791", "AUC 0.823"]),
    ("39", "1", ["TP  100  FP   386  FN   46  TN  1693", "**7** of 2,225", "no better than", "93.4%",
                 "More than two classes", "**0.633**", "**0.850**", "**0.317** (0.316"]),
    ("39", "2", ["ROC-AUC 0.823   PR-AUC (average precision) 0.302", "0.066"]),
    ("39", "3", ["92,933", "2,32,567", "₹37 lakh"]),
    ("39", "4", ["ROC-AUC 0.806   log loss 0.4830", "mean prediction 0.069", "mean prediction 0.180", "**94%**", "**27%**",
                 "0.483 to 0.202", "0.806 to 0.802"]),
    ("39", "5", ["₹10.8 lakh", "₹24.5 lakh", "627 leads", "504 leads", "0.05"]),
    ("39", "8", ["Permutation importance"]),
    ("39", "9", ["Fairness"]),
    ("39", "10", ["Model cards"]),
    ("40", "6", [".shift(1).rolling(4)", "most common leak"]),
    ("40", "7", ["Backtesting"]),
    ("43", "5", ["logistic regression      0.764", "small neural network     0.773", "gradient boosting        0.786",
                 "test AUC 0.797", "test AUC 0.818", "test AUC 0.821", "validation AUC"]),
    ("45", "5", ["What a hash is"]),
    ("53", "3", ["Early stopping"]),
    ("53", "6", ["early_stopping=True"]),
    ("56", "1", ["data drift", "concept drift"]),
    ("56", "7", ["Monitoring, in three layers", "labels arrive"]),
    ("56", "8", ["4.41", "(96.8%)", "(96.5%)", "(84.4%)"]),
    ("56", "9", ["Retraining"]),
    ("56", "11", ["training-serving skew", "feature store"]),
]
for n, sec, needles in QUOTES:
    text = section(n, sec)
    if text is None:
        ok(False, f"section {n}.{sec} missing"); continue
    for needle in needles:
        ok(needle.lower() in text.lower(), f"{n}.{sec}: '{needle}' not found")

# exercise answers cited: Ch 40 exercise 10, Ch 43 exercise 8; stories in Ch 35 and Ch 43
ok("leaky one-week-ahead WAPE: 8.9%" in chapter(40) and "9.4%" in chapter(40), "Ch 40 ex 10")
ok("0.730 by epoch 500" in chapter(43) and "8. Train the tabular network for 500 epochs" in chapter(43), "Ch 43 ex 8")
ok("91%" in chapter(43).split("## In the real world")[1][:3000] and "conference" in chapter(43).split("## In the real world")[1][:3000], "Ch 43 story")
ok("91% accuracy" in chapter(35).split("## In the real world")[1][:3000], "Ch 35 story")

# 3. arithmetic
ok(round(1 - 484 / 5000, 3) == 0.903, "90.3%")
tp, fp, fn, tn = 100, 386, 46, 1693
p, r = tp / (tp + fp), tp / (tp + fn)
ok((round(p, 3), round(r, 3)) == (0.206, 0.685), "precision/recall")
ok(round(2 * 0.206 * 0.685 / (0.206 + 0.685), 3) == 0.317 and round(2 * p * r / (p + r), 3) == 0.316, "F1")
ok(round((4 + 2076) / 2225, 3) == 0.935 and round(2079 / 2225, 3) == 0.934, "0.5-threshold accuracy vs all-no")
ok(round((0.9 + 0.8 + 0.2) / 3, 3) == 0.633 and round((0.9 * 800 + 0.8 * 150 + 0.2 * 50) / 1000, 3) == 0.85, "macro/weighted F1")
adj = lambda r2, n, k: 1 - (1 - r2) * (n - 1) / (n - k - 1)
ok(round(adj(0.90, 50, 10), 3) == 0.874 and round(adj(0.901, 50, 11), 3) == 0.872, "adjusted R²")
ok(round(0.838 - 0.797, 2) == 0.04, "boosting beats plain logistic by 0.04")

# 4. tags: only Chapter 69's twelve
TAGS = {"Clarify", "Assume", "Signpost", "Simple first", "Edge cases", "Trade-offs", "Validate", "Business",
        "Scale", "Limits", "Evidence", "Close"}
used = set(re.findall(r"\*\*\[\+([^\]]+)\]\*\*", ch74))
ok(used <= TAGS, f"unknown tags {used - TAGS}")
ok(not re.search(r"\[(Learn it in|Real evidence|Business|Depth|Practical|Structure)\]", ch74), "old-style tag left")
print(f"tags used: {sorted(used)}")
print("ch74_check:", "OK" if not fails else f"{fails} failure(s)")
sys.exit(1 if fails else 0)
