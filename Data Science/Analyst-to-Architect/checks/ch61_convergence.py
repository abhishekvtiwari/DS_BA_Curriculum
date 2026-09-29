"""Chapter 61 checks: the numbers quoted about the eventual-consistency simulation.

Run from the book folder:  python3 checks/ch61_convergence.py
Uses the chapter's own functions from companion/ch61/eventual_consistency_sim.py.
"""
import statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "companion" / "ch61"))
from eventual_consistency_sim import schedule_deliveries, replay


def first_all_v4(rows):
    """First tick at which every replica holds the last write, v4."""
    return next(tick for tick, values, _ in rows if all(v == "v4" for v in values))


# Level 1 and the prose: default run
rows = replay(schedule_deliveries())
bad = [t for t, _, agree in rows if not agree]
print("default: disagreeing ticks", bad, "count", len(bad), "converged at", first_all_v4(rows))

# Level 3: five replicas at the default seed, and seven more seeds
for n in (3, 5):
    per_seed = {s: first_all_v4(replay(schedule_deliveries(s, n), n)) for s in (1, 2, 3, 7, 42, 61, 100)}
    print(f"{n} replicas, all hold v4 at tick:", per_seed)
rows5 = replay(schedule_deliveries(61, 5), 5)
print("5 replicas seed 61: disagreeing ticks", sum(1 for *_, a in rows5 if not a))

# chance that at least one replica draws the 6-tick delay for v4
for n in (3, 5):
    print(f"P(some replica waits 6 ticks for v4), {n} replicas: {1 - (6/7) ** n:.1%}")

# many seeds
for n in (3, 5):
    ticks = [first_all_v4(replay(schedule_deliveries(s, n), n)) for s in range(1, 1001)]
    print(f"{n} replicas, seeds 1-1000: mean tick all hold v4 = {statistics.mean(ticks):.1f}")

# Bonus: a dropped message
def drop(deliveries, write_id, replica):
    return [d for d in deliveries if not (d[2] == write_id and d[1] == replica)]

for w, r in ((3, 2), (4, 0)):
    rows_d = replay(drop(schedule_deliveries(), w, r))
    print(f"drop write {w} at replica {r}: final {rows_d[-1][1]}, agrees {rows_d[-1][2]}")
