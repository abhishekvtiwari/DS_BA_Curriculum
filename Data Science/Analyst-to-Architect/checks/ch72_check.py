#!/usr/bin/env python3
"""Chapter 72 checks: the code that lives in tables and in timing cells, which verify_python.py can't see.

    python3 checks/ch72_check.py            # from the book folder

1. Runs every predict-the-output snippet in the rapid-fire tables (Q72-015 to Q72-028) and compares
   what it prints with the "Output" cell of the table row, read from the manuscript itself.
2. Checks the claims in other rapid-fire rows that aren't shown as cells (Q72-005, Q72-051's ValueError).
3. Runs the two timing cells (Q72-030, Q72-047), which are marked `<!-- run: none -->` in the chapter
   because timings change every run, and prints their output. Paste that output into the chapter.
Exit code 0 when every comparison matches.
"""
import contextlib, io, pathlib, re, sys, time

MS = pathlib.Path(__file__).resolve().parent.parent / "manuscript" / "ch72-python-and-pandas-question-bank.md"
md = MS.read_text(encoding="utf-8")
bad = 0


def run(snippet):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            exec(snippet, {})
        except Exception as e:  # the table shows "Type: message" for an error
            print(f"{type(e).__name__}: {e}")
    return buf.getvalue().strip()


# 1. predict-the-output tables: | Q72-0NN | `snippet` | `output` | why |
rows = re.findall(r"^\| (Q72-0(?:1[5-9]|2[0-8])) \| (.+?) \| (.+?) \| .+ \|$", md, re.M)
for qid, snip_cell, out_cell in rows:
    snippets = re.findall(r"`([^`]+)`", snip_cell)
    outputs = re.findall(r"`([^`]+)`", out_cell)
    code = snippets[0].replace("; ", "\n") if len(snippets) == 1 else None
    if qid == "Q72-017":                       # two separate prints in one row
        got = [run(s) for s in snippets]
    elif qid == "Q72-020":                     # "`class C: items = []` then `c1 = C(); …`"
        got = [run("class C:\n    items = []\n" + snippets[1].replace("; ", "\n"))]
    else:
        got = [run(code)]
    ok = got == outputs
    bad += not ok
    print(f"{qid}: {'ok' if ok else 'MISMATCH'}  {got}" + ("" if ok else f"  expected {outputs}"))

# 2. claims in answer cells
try:
    {([1], 2): "x"}
    print("Q72-005: MISMATCH, ([1], 2) was hashable"); bad += 1
except TypeError as e:
    print("Q72-005: ok  ([1], 2) as a key ->", e)

import pandas as pd
old = pd.Series(["Sharma Hardware", None, "Metro Mart"], dtype=object)
try:
    old[old.str.contains("Mart")]
    print("Q72-051: MISMATCH, no error"); bad += 1
except ValueError as e:
    ok = str(e) == "Cannot mask with non-boolean array containing NA / NaN values"
    bad += not ok
    print(f"Q72-051: {'ok' if ok else 'MISMATCH'}  ValueError: {e}")
print("pandas", pd.__version__, "| Python", sys.version.split()[0])

# 3. timing cells (output changes every run)
print("\n--- Q72-030 timing cell")
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        print(f"{func.__name__} took {t1 - t0:.6f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

result = slow_sum(1_000_000)
print("result:", result)

print("\n--- Q72-047 timing cell")
big = pd.DataFrame({"a": range(200_000), "b": range(200_000)})
t0 = time.perf_counter()
r1 = big.apply(lambda row: row["a"] * row["b"], axis=1)   # row by row
t1 = time.perf_counter()
r2 = big["a"] * big["b"]                                  # vectorized
t2 = time.perf_counter()
print(f"apply:      {t1 - t0:.4f} s")
print(f"vectorized: {t2 - t1:.6f} s")
print(f"speedup:    {(t1 - t0) / (t2 - t1):,.0f}x")

print(f"\n{len(rows)} table rows checked, {bad} mismatches")
sys.exit(1 if bad else 0)
