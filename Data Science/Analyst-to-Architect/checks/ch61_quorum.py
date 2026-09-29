"""Chapter 61 check: with N = 3 copies, W + R > N makes every read set meet every write set.

Run: python3 checks/ch61_quorum.py
"""
from itertools import combinations

N = 3
copies = range(N)
for W, R in ((2, 2), (1, 2), (3, 1), (1, 1)):
    always = all(set(w) & set(r) for w in combinations(copies, W) for r in combinations(copies, R))
    print(f"N={N} W={W} R={R}: W+R={W+R} {'>' if W+R > N else '<='} N, every read meets the latest write: {always}")
