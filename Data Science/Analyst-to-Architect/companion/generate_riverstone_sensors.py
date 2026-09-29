"""
Analyst to Architect · Riverstone machine sensor readings (used in Chapter 40)
generate_riverstone_sensors.py: one-minute readings from injection-moulding machines.

Run:     python3 generate_riverstone_sensors.py            -> one week, one machine (10,080 rows) for Chapter 40
         python3 generate_riverstone_sensors.py --full     -> 12 machines x 40 weeks (~4.8M rows) for Chapters 48 and 50
Writes:  sensors/machine_readings_week.csv  (or sensors/machine_readings_full.parquet with --full)
Seed:    20241 (the one-week file is exactly the first week of machine M01 in the full run)
Tested:  Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (18 September 2026)

Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import sys
import numpy as np
import pandas as pd

OUT = pathlib.Path(__file__).resolve().parent / "sensors"
OUT.mkdir(exist_ok=True)
FULL = "--full" in sys.argv
MACHINES = 12 if FULL else 1
WEEKS = 40 if FULL else 1
MINUTES = WEEKS * 7 * 24 * 60
start = pd.Timestamp("2025-03-03 00:00")

frames = []
for m in range(1, MACHINES + 1):
    rng = np.random.default_rng(20241 + m)                     # each machine has its own seed
    t = np.arange(MINUTES)
    ts = start + pd.to_timedelta(t, unit="min")
    hour = ts.hour.to_numpy() + ts.minute.to_numpy() / 60
    shift_load = 1 + 0.015 * np.sin(2 * np.pi * (hour - 9) / 24)      # warmer in the day shift
    base_temp = 215 + 2 * m / 12
    temp = base_temp * shift_load + 0.02 * t / 1440                 # slow drift: +0.02 °C a day
    ar = np.zeros(MINUTES)
    for i in range(1, MINUTES):
        ar[i] = 0.8 * ar[i - 1] + rng.normal(0, 0.6)
    temp = temp + ar
    pressure = 118 + 0.15 * (temp - base_temp) + rng.normal(0, 1.5, MINUTES)
    cycle_seconds = 18.5 + 0.03 * (temp - base_temp) + rng.normal(0, 0.25, MINUTES)
    status = np.full(MINUTES, "running", dtype=object)
    # planted events in every week: a heater fault (temperature ramps for ~50 minutes), a pressure spike, a stoppage
    for w in range(WEEKS):
        base = w * 10080
        f = base + int(rng.integers(1500, 9000)); temp[f:f + 50] += np.linspace(0, 12, 50); temp[f + 50:f + 90] += np.linspace(12, 0, 40)
        s = base + int(rng.integers(500, 9500)); pressure[s:s + 3] += rng.uniform(25, 40, 3)
        z = base + int(rng.integers(200, 9800)); span = slice(z, z + int(rng.integers(20, 60)))
        status[span] = "stopped"; cycle_seconds[span] = np.nan; pressure[span] = 0
    # sensor glitch: a few readings dropped, and a few stuck values
    drop = rng.random(MINUTES) < 0.002; temp[drop] = np.nan
    frames.append(pd.DataFrame({"timestamp": ts, "machine_id": f"M{m:02d}", "temperature_c": np.round(temp, 2),
                                "pressure_bar": np.round(pressure, 2), "cycle_seconds": np.round(cycle_seconds, 2),
                                "status": status}))
readings = pd.concat(frames, ignore_index=True)
if FULL:
    readings.to_parquet(OUT / "machine_readings_full.parquet", index=False)
    print(f"{len(readings):,} rows -> machine_readings_full.parquet")
else:
    readings.to_csv(OUT / "machine_readings_week.csv", index=False)
    print(f"{len(readings):,} rows -> machine_readings_week.csv")
