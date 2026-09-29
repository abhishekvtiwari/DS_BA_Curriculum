"""Analyst to Architect · Chapter 42 · number check.
Runs the chapter's Python cells in order (as tools/verify_python.py does), then checks the numbers that the
chapter's prose quotes, and writes checks/ch42_results.json for figures/make_figs42.py.
Run from checks/: python3 ch42_check.py   (about 15 seconds; needs companion/baskets and companion/accounts).
Riverstone Supplies is fictional."""
import contextlib, io, json, os, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
BOOK = HERE.parent
CHAPTER = BOOK / "manuscript" / "ch42-recommender-systems-and-ranking.md"
os.chdir(BOOK / "companion" / "ch42")
sys.path.insert(0, os.getcwd())

md = CHAPTER.read_text(encoding="utf-8")
ns = {"__name__": "__main__"}
for block in re.findall(r"^```python\n(.*?)^```$", md, re.S | re.M):
    with contextlib.redirect_stdout(io.StringIO()):
        exec(block, ns)

fails = 0


def ok(label, got, want):
    global fails
    good = got == want
    fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")


r3 = lambda t: tuple(round(float(v), 3) for v in t)
lines, matrix = ns["lines"], ns["matrix"]
ok("lines / orders / accounts", (len(lines), lines.order_id.nunique(), lines.account_id.nunique()),
   (92337, 34013, 4516))
ok("density", round(float((matrix > 0).mean().mean()), 3), 0.386)
ok("eligible accounts", len(ns["eligible"]), 4283)
ok("popularity", r3(ns["evaluate"](lambda i: ns["pop_counts"])), (0.627, 0.434, 0.372))
ok("item CF", r3((ns["hit_cf"], ns["ndcg_cf"], ns["mrr_cf"])), (0.650, 0.495, 0.443))
ok("item CF yes/no", r3(ns["variant_results"]["bought yes/no"]), (0.687, 0.504, 0.443))
ok("SVD 4 / 12 hit rate", (round(ns["svd_results"][4][0], 3), round(ns["svd_results"][12][0], 3)), (0.647, 0.464))
ok("ALS 8 / 16 hit rate", (round(ns["als_results"][8][0], 3), round(ns["als_results"][16][0], 3)), (0.679, 0.460))
ok("content", r3((ns["hit_content"], ns["ndcg_content"], ns["mrr_content"])), (0.530, 0.357, 0.300))
ok("hybrid", r3((ns["hit_hybrid"], ns["ndcg_hybrid"], ns["mrr_hybrid"])), (0.637, 0.448, 0.386))
ok("segment popularity", r3((ns["hit_seg"], ns["ndcg_seg"], ns["mrr_seg"])), (0.715, 0.533, 0.473))
ok("P01 top similar", list(ns["top_similar"].index), ["P03", "P04", "P18", "P06"])

scoreboard = ns["scoreboard"]
names = ns["names"]
segment_top = {}
for seg in ["Retail", "Hospitality", "Wholesale"]:
    rows = matrix.index.isin(ns["accounts"].loc[ns["accounts"].segment == seg, "account_id"])
    segment_top[seg] = (matrix[rows] > 0).mean().sort_values(ascending=False).head(3).to_dict()
json.dump({
    "scoreboard": {m: [float(v) for v in scoreboard.loc[m]] for m in scoreboard.index},
    "segment_top": segment_top,
    "names": names.to_dict(),
}, open(HERE / "ch42_results.json", "w"), indent=1)
print("All checks passed." if not fails else f"FAILED: {fails}")
raise SystemExit(1 if fails else 0)
