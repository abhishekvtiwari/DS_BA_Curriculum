#!/usr/bin/env python3
"""ch73_check.py - recompute every number Chapter 73 states in prose or tables without a code cell of its own.

Usage: OMP_NUM_THREADS=1 python3 checks/ch73_check.py
Each line prints OK or MISMATCH with the value the chapter states. Exit code 1 on any mismatch.
(The code cells themselves are checked by tools/verify_python.py.)"""
import sys
import numpy as np
from scipy import stats
import statsmodels.stats.api as sms

bad = 0
def check(label, got, stated):
    global bad
    ok = got == stated
    bad += not ok
    print(f"{'OK      ' if ok else 'MISMATCH'} {label}: computed {got!r}, chapter says {stated!r}")

# Q73-005: the 1,000-person table and the accuracy of the test
sick, healthy = 1000 * 0.01, 1000 * 0.99
tp, fn = sick * 0.99, sick * 0.01
fp, tn = healthy * 0.05, healthy * 0.95
check("sick positive / negative", (round(tp, 1), round(fn, 1)), (9.9, 0.1))
check("healthy positive / negative", (round(fp, 1), round(tn, 1)), (49.5, 940.5))
check("total positive / negative", (round(tp + fp, 1), round(fn + tn, 1)), (59.4, 940.6))
check("share of positives sick", f"{tp / (tp + fp):.1%}", "16.7%")
check("accuracy", f"{0.99 * 0.01 + 0.95 * 0.99:.1%}", "95.0%")

# Q73-007: pairs among 23 people
check("pairs of 23", 23 * 22 // 2, 253)

# Q73-020: Chapter 22's hand formula (section 22.3, copied verbatim) for the same inputs
def sample_size_for_proportion(baseline, lift_points, alpha=0.05, power=0.80):
    p1 = baseline
    p2 = baseline + lift_points / 100
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    p_bar = (p1 + p2) / 2
    numerator = (z_alpha * np.sqrt(2 * p_bar * (1 - p_bar)) + z_beta * np.sqrt(p1*(1-p1) + p2*(1-p2))) ** 2
    return int(np.ceil(numerator / (p2 - p1) ** 2))
check("Ch 22 formula, 9.6% + 1.5 points", f"{sample_size_for_proportion(0.096, 1.5):,}", "6,473")
n15 = sms.NormalIndPower().solve_power(sms.proportion_effectsize(0.111, 0.096), power=0.8, alpha=0.05, ratio=1)
check("statsmodels unrounded, 1.5 points", f"{n15:,.1f}", "6,465.6")

# Q73-025: peeking rate across seeds (the chapter says between 16% and 18% across ten seeds; 0.163 with seed 73)
def peeking(seed):
    rng = np.random.default_rng(seed)
    fp = 0
    for _ in range(2000):
        a, b = [], []
        found = False
        for _ in range(10):
            a.extend(rng.normal(0, 1, 20)); b.extend(rng.normal(0, 1, 20))
            if len(a) >= 40:
                if stats.ttest_ind(a, b)[1] < 0.05:
                    found = True; break
        fp += found
    return fp / 2000
rates = [peeking(s) for s in range(70, 80)]
print("         peeking rate, seeds 70-79:", rates, "mean", round(float(np.mean(rates)), 3))
check("peeking rates within 0.16-0.18", all(0.16 <= r <= 0.18 for r in rates), True)
check("looks per experiment", len(range(40, 201, 20)), 9)
check("0.163 / 0.05 more than 3 times", 0.163 / 0.05 > 3, True)

# Q73-028: 20 unrelated metrics, no real effect, t-test each at alpha 0.05, 10,000 experiments
rng = np.random.default_rng(73)
a = rng.normal(0, 1, (10_000, 20, 100))
b = rng.normal(0, 1, (10_000, 20, 100))
p = stats.ttest_ind(a, b, axis=2).pvalue
check("simulated P(at least one of 20)", f"{(p < 0.05).any(axis=1).mean():.3f}", "0.639")
check("theoretical 1 - 0.95^20", f"{1 - 0.95 ** 20:.3f}", "0.642")

# Q73-036: relative lift
check("relative lift", f"{(0.109 - 0.096) / 0.096:.1%}", "13.5%")

# In the real world: Farah's split, 5,340 vs 4,660
chi2, pv = stats.chisquare([5340, 4660])
check("Farah SRM p below 0.001", pv < 0.001, True)

# Q73-036: swapping the order flips the sign of z; Q73-037: Yates' correction left on
z_swapped, p_swapped = sms.proportions_ztest(np.array([480, 545]), np.array([5000, 5000]))
check("z with control first", f"{z_swapped:.3f}, p = {p_swapped:.4f}", "-2.143, p = 0.0321")
chi2_y, p_y, _, _ = stats.chi2_contingency(np.array([[120, 80], [90, 110]]))
check("chi-square with Yates", f"{chi2_y:.3f}, p = {p_y:.4f}", "8.431, p = 0.0037")

print("mismatches:", bad)
sys.exit(1 if bad else 0)
