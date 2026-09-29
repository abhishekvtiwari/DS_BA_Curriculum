"""Analyst to Architect, Chapter 61 (section 61.4): a small, runnable simulation of
eventual consistency. Copies (replicas) of one customer record receive the same four
writes over an unreliable network; each copy of each write has its own random delay.
We watch the replicas disagree for a while, then converge once writes stop arriving.

The two functions are the ones built cell by cell in section 61.4.

Run:   python eventual_consistency_sim.py
       python eventual_consistency_sim.py --seed 7 --replicas 5
Seeded, so the same seed and replica count always print the same output.
"""
import argparse
import random


def schedule_deliveries(seed=61, num_replicas=3):
    """Return every delivery as (arrival_tick, replica, write_id, value), sorted by arrival."""
    rng = random.Random(seed)
    writes = [(0, "v1"), (2, "v2"), (5, "v3"), (9, "v4")]      # (tick issued, value)
    deliveries = []
    for write_id, (issued_at, value) in enumerate(writes, start=1):
        for replica in range(num_replicas):
            delay = rng.choice([0, 1, 1, 2, 3, 3, 6])          # most arrive soon; a few lag badly
            deliveries.append((issued_at + delay, replica, write_id, value))
    deliveries.sort()
    return deliveries


def replay(deliveries, num_replicas=3):
    """Apply the deliveries tick by tick; return (tick, values, agree) for every tick."""
    state = [(None, 0) for _ in range(num_replicas)]    # per replica: (value, highest write id so far)
    rows = []
    next_one = 0
    last_tick = deliveries[-1][0]
    for tick in range(last_tick + 3):
        while next_one < len(deliveries) and deliveries[next_one][0] == tick:
            _, replica, write_id, value = deliveries[next_one]
            if write_id > state[replica][1]:            # highest version wins
                state[replica] = (value, write_id)
            next_one += 1
        values = [value for value, _ in state]
        rows.append((tick, values, len(set(values)) == 1))
    return rows


def main():
    parser = argparse.ArgumentParser(description="Watch replicas converge.")
    parser.add_argument("--seed", type=int, default=61, help="random seed (default 61)")
    parser.add_argument("--replicas", type=int, default=3, help="number of replicas (default 3)")
    args = parser.parse_args()

    rows = replay(schedule_deliveries(args.seed, args.replicas), args.replicas)
    for tick, values, agree in rows:
        print(f"tick {tick:>2}: {values}  {'agree' if agree else 'DISAGREE'}")
    disagreements = sum(1 for _, _, agree in rows if not agree)
    final_agrees = rows[-1][2]
    print(f"{disagreements} of {len(rows)} ticks disagree; the final state agrees: {final_agrees}")


if __name__ == "__main__":
    main()
