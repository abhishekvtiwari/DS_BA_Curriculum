"""Check the arithmetic of Chapter 62's mesh maturity scorecard (section 62.6, Figure 62.5,
the story, and companion/ch62/mesh-maturity-riverstone.md) against the rule the chapter states:
any question at 1, or a total under 15 out of 25, means not ready."""
first = {"domain teams": 1, "self-serve platform": 2, "federated governance": 2,
         "data-product mindset": 3, "appetite": 1}
rerun = dict(first, **{"domain teams": 2, "appetite": 3})

def verdict(scores):
    total = sum(scores.values())
    blockers = [q for q, s in scores.items() if s == 1]
    ready = not blockers and total >= 15
    return total, blockers, ready

for name, sc in [("first run", first), ("rerun", rerun)]:
    total, blockers, ready = verdict(sc)
    print(f"{name}: total {total}/25, blockers {blockers}, ready for a mesh: {ready}")

assert verdict(first) == (9, ["domain teams", "appetite"], False)
assert verdict(rerun) == (12, [], False)
print("ok")
