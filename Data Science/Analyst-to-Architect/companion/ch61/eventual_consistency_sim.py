"""Analyst to Architect, Chapter 61 -- a tiny, runnable simulation of eventual
consistency: three replicas of one customer record receive the same sequence
of writes over an unreliable network (each copy of each write has its own
random delay), and we watch a wall-clock timeline where the replicas
genuinely disagree for a while, then converge once writes stop arriving.

Run:  python3 eventual_consistency_sim.py
Deterministic: seeded, so the printed output is the same on every run.
"""
import random


def run_simulation(seed: int = 61, num_replicas: int = 3) -> None:
    rng = random.Random(seed)
    writes = [(0, "v1"), (2, "v2"), (5, "v3"), (9, "v4")]     # (issued_at_tick, value)

    # schedule when each replica actually receives each write: issued_at + a random network delay
    deliveries = []                                            # (arrival_tick, replica_index, write_id, value)
    for write_id, (issued_at, value) in enumerate(writes, start=1):
        for replica_index in range(num_replicas):
            delay = rng.choice([0, 1, 1, 2, 3, 3, 6])          # most arrive soon; a few lag badly
            deliveries.append((issued_at + delay, replica_index, write_id, value))
    deliveries.sort()

    state = [(None, 0) for _ in range(num_replicas)]           # (value, highest write_id applied so far)
    last_tick = deliveries[-1][0]
    delivery_index = 0

    print("tick | replica 0 | replica 1 | replica 2 | agree?")
    for tick in range(0, last_tick + 3):
        while delivery_index < len(deliveries) and deliveries[delivery_index][0] == tick:
            _, replica_index, write_id, value = deliveries[delivery_index]
            current_value, current_write_id = state[replica_index]
            if write_id > current_write_id:                    # last-write-wins by write_id
                state[replica_index] = (value, write_id)
            delivery_index += 1
        values = [v for v, _ in state]
        agree = len(set(values)) == 1
        print(f" {tick:>3} | {values[0] or '-':>9} | {values[1] or '-':>9} | {values[2] or '-':>9} | "
              f"{'yes' if agree else 'NO'}")

    print(f"\nfinal state (no writes issued after tick {writes[-1][0]}): {[v for v, _ in state]}")
    print("converged:", len(set(v for v, _ in state)) == 1)


if __name__ == "__main__":
    run_simulation()
