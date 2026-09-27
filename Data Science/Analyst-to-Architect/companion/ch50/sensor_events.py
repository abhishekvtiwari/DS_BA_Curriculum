"""Chapter 50 companion: replay Riverstone sensor readings as a stream of events.
Reads the Chapter 48 Parquet archive and produces events with an event time, in batches,
including a few that arrive late (their event time is older than the batch they arrive in).
Riverstone Supplies is fictional; every name and number is invented."""
import json, os, shutil
import duckdb

SENSORS = os.environ.get("CH48_SENSORS", "../ch48/sensor_readings")
DAY = "2025-12-01"

def _rows(limit, offset=0, machine=None, minute_from=None, minute_to=None):
    where = [f"reading_date = DATE '{DAY}'"] if False else []
    if machine: where.append(f"machine_id = '{machine}'")
    if minute_from is not None:
        where.append(f"EXTRACT(hour FROM reading_ts) * 60 + EXTRACT(minute FROM reading_ts) BETWEEN {minute_from} AND {minute_to}")
    sql = f"""SELECT machine_id, plant, reading_ts, temperature_c, units_made, scrap_flag
              FROM read_parquet('{SENSORS}/reading_date={DAY}/*.parquet')
              {'WHERE ' + ' AND '.join(where) if where else ''}
              ORDER BY reading_ts, machine_id LIMIT {limit} OFFSET {offset}"""
    return duckdb.connect().execute(sql).fetchall()

def event(row):
    return {"machine_id": row[0], "plant": row[1], "event_time": row[2].isoformat(sep=" "),
            "temperature_c": float(row[3]), "units_made": int(row[4]), "scrap": bool(row[5])}

def batch(n, offset=0, **kw):
    return [event(r) for r in _rows(n, offset, **kw)]

def write_batch(folder, name, events):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, name), "w") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")
    return os.path.join(folder, name)

def reset(folder):
    shutil.rmtree(folder, ignore_errors=True); os.makedirs(folder, exist_ok=True)
