"""Chapter 48 companion: generate Riverstone's plant sensor dataset.
25 machines across two plants, one reading every 10 seconds, 1 October to 31 December 2025:
25 x 92 x 8,640 = 19,872,000 readings, written as Parquet partitioned by reading_date.
Run: python3 make_sensor_data.py            (about 2-4 minutes, ~400 MB)
     python3 make_sensor_data.py --small    (one day only, for quick experiments)
Riverstone Supplies is fictional; every name and number is invented."""
import os, sys, shutil
import numpy as np, pyarrow as pa, pyarrow.parquet as pq

MACHINES = [(f"M-{i:02d}", "Bhiwandi Main" if i <= 15 else "Chakan Pune",
             ["Injection", "Extrusion", "Blow"][i % 3]) for i in range(1, 26)]
START, DAYS, PER_DAY = np.datetime64("2025-10-01"), 92, 8640   # one reading every 10 seconds

def write_day(day_index, folder, rng):
    day = START + np.timedelta64(day_index, "D")
    offsets = (np.arange(PER_DAY, dtype="int64") * 10).astype("timedelta64[s]")
    frames = []
    for m, (machine_id, plant, line_type) in enumerate(MACHINES):
        base_temp = 180.0 + 8 * ((m + day_index) % 5)
        temp = base_temp + rng.normal(0, 2.5, PER_DAY)
        if (day_index + m) % 17 == 0:                       # a drifting machine now and then
            temp += np.linspace(0, 12, PER_DAY)
        pressure = 95.0 + rng.normal(0, 3.0, PER_DAY) + (temp - base_temp) * 0.4
        units = rng.poisson(3, PER_DAY).astype("int32")
        scrap = (rng.random(PER_DAY) < np.where(temp > base_temp + 8, 0.06, 0.012))
        frames.append(pa.table({
            "machine_id": pa.array([machine_id] * PER_DAY),
            "plant": pa.array([plant] * PER_DAY),
            "line_type": pa.array([line_type] * PER_DAY),
            "reading_ts": pa.array(day.astype("datetime64[s]") + offsets),
            "temperature_c": pa.array(np.round(temp, 2)),
            "pressure_bar": pa.array(np.round(pressure, 2)),
            "units_made": pa.array(units),
            "scrap_flag": pa.array(scrap),
        }))
    table = pa.concat_tables(frames)
    out = os.path.join(folder, f"reading_date={str(day)}")
    os.makedirs(out, exist_ok=True)
    pq.write_table(table, os.path.join(out, "part-0.parquet"), compression="snappy")
    return table.num_rows

def build(folder="sensor_readings", days=DAYS, seed=48):
    shutil.rmtree(folder, ignore_errors=True); os.makedirs(folder)
    rng = np.random.default_rng(seed)
    total = sum(write_day(d, folder, rng) for d in range(days))
    return total

if __name__ == "__main__":
    small = "--small" in sys.argv
    folder = "sensor_readings_small" if small else "sensor_readings"
    n = build(folder, days=1 if small else DAYS)
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(folder) for f in fs)
    print(f"{folder}: {n:,} readings, {size / 1e6:.1f} MB")
