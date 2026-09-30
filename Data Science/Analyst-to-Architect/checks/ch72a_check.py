#!/usr/bin/env python3
"""Chapter 72A checks: what tools/verify_python.py can't see.

    OMP_NUM_THREADS=1 python3 checks/ch72a_check.py            # from the book folder

1. Runs every python block of the chapter in order, in one namespace, INCLUDING the two timing cells marked
   `<!-- run: none -->` (Q72A-002, Q72A-018), and prints the timing cells' output. Timings change on every
   run; paste the printed output into the chapter's TIMING block when you re-time.
2. Checks the shape the text claims for the timings: doubling n roughly quadruples the O(n^2) version
   (ratio 3 to 5.5) and the memoized Fibonacci is at least 1,000x faster than the naive one.
3. Checks the rapid-fire answers that have no code cell (Q72A-003 to Q72A-024).
Exit code 0 when every check passes.
"""
import contextlib, heapq, io, pathlib, re, sys
from collections import Counter

MS = pathlib.Path(__file__).resolve().parent.parent / "manuscript" / "ch72a-data-structures-and-algorithms-question-bank.md"
md = MS.read_text(encoding="utf-8")
bad = 0


def check(label, ok, detail=""):
    global bad
    bad += not ok
    print(f"{label}: {'ok' if ok else 'FAIL'} {detail}")


# 1. all python blocks, in order; capture the run: none (timing) cells
token = re.compile(r"<!-- run: (none) -->|^```(\w*)\n(.*?)^```$", re.S | re.M)
ns = {"__name__": "__main__"}
skip = False
timing_out = []
for m in token.finditer(md):
    if m.group(1):
        skip = True
        continue
    if m.group(2) != "python":
        skip = False
        continue
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(m.group(3), ns)
    if skip:
        timing_out.append(buf.getvalue())
        skip = False

print("--- Q72A-002 timing cell\n" + timing_out[0])
print("--- Q72A-018 timing cell\n" + timing_out[1])

# 2. the shape of the timings
secs = [float(x) for x in re.findall(r"O\(n\^2\) ([\d.]+) s", timing_out[0])]
check("Q72A-002 doubling n ~ x4", 3 <= secs[1] / secs[0] <= 5.5, f"ratio {secs[1] / secs[0]:.2f}")
ratio = float(re.search(r"([\d,]+)x", timing_out[1]).group(1).replace(",", ""))
check("Q72A-018 memo >= 1,000x", ratio >= 1000, f"{ratio:,.0f}x")

# 3. the Big-O table (Q72A-001) and rapid-fire answers
import math
check("Q72A-001 table", [math.ceil(math.log2(5000)), round(5000 * math.log2(5000)), 5000 ** 2, len(str(2 ** 5000))]
      == [13, 61439, 25_000_000, 1506])
lst = [1, 2, 3, 4, 5]                                   # Q72A-010: reverse in place with two pointers
l, r = 0, len(lst) - 1
while l < r:
    lst[l], lst[r] = lst[r], lst[l]
    l += 1
    r -= 1
check("Q72A-010", lst == [5, 4, 3, 2, 1])

nums, n = [1, 2, 4, 5, 6], 6                            # Q72A-011: missing number
check("Q72A-011", n * (n + 1) // 2 - sum(nums) == 3)

check("Q72A-012", ns["merge"]([1, 4, 9], [2, 3, 10, 11]) == [1, 2, 3, 4, 9, 10, 11])

groups = {}                                             # Q72A-013: anagrams, both keys
for w in ["listen", "silent", "enlist", "google", "gogole", "cat"]:
    groups.setdefault("".join(sorted(w)), []).append(w)
counts = {}
for w in ["listen", "silent", "enlist", "google", "gogole", "cat"]:
    key = tuple(w.count(c) for c in "abcdefghijklmnopqrstuvwxyz")
    counts.setdefault(key, []).append(w)
check("Q72A-013", sorted(groups.values()) == sorted(counts.values()) and len(groups) == 3)

class Plain:                                            # Q72A-015: plain instances hash by identity
    pass
a, b = Plain(), Plain()
check("Q72A-015", len({a, a, b}) == 2 and hash(a) == hash(a))
for unhashable in ([1], {1: 2}, {1}):
    try:
        hash(unhashable)
        check("Q72A-015 unhashable", False, repr(unhashable))
    except TypeError:
        pass

s = "swiss"                                             # Q72A-016: first non-repeating
c = Counter(s)
check("Q72A-016", next(ch for ch in s if c[ch] == 1) == "w")

check("Q72A-017", Counter("to be or not to be".split()).most_common(1) == [("to", 2)])

try:                                                    # Q72A-019: missing base case
    def no_base(n):
        return no_base(n - 1)
    no_base(5)
    check("Q72A-019", False)
except RecursionError:
    check("Q72A-019", True)

data = [7, 2, 9, 4, 11, 5]                              # Q72A-022: kth largest
check("Q72A-022", heapq.nlargest(2, data)[-1] == sorted(data)[-2] == 9)

orders = [("2025-01-07", "B"), ("2025-01-06", "A"), ("2025-01-07", "A"), ("2025-01-06", "B")]
by_date = sorted(orders, key=lambda o: o[0])            # Q72A-024: stable, ties keep row order
check("Q72A-024", by_date == [("2025-01-06", "A"), ("2025-01-06", "B"), ("2025-01-07", "B"), ("2025-01-07", "A")])

print("all checks passed" if not bad else f"{bad} check(s) failed")
sys.exit(1 if bad else 0)
