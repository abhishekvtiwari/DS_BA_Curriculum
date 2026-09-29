"""Chapter 50 companion: replay Riverstone sensor readings as a stream of events.

It reads one day (1 December 2025) of the Chapter 48 Parquet archive and hands the readings back
as events: small dictionaries with an event time. Two functions:

    readings(minute_from, minute_to, machine=None)
        Every reading taken from minute_from up to, but not including, minute_to, counted in
        minutes after midnight, like range(). 25 machines send 6 readings a minute (one every
        10 seconds), so readings(0, 2) returns 25 x 6 x 2 = 300 events, from 00:00:00 to 00:01:50.
        machine="M-07" keeps one machine's readings only: readings(2, 3, machine="M-07") returns 6.

    write_batch(folder, name, events)
        Writes the events into one file of JSON lines (one event per line), the way a source
        system would drop a file of new events into a folder. Returns the file's path.

The archive is expected in ../ch48/sensor_readings (Chapter 48, section 48.0, step 4); set the
environment variable CH48_SENSORS to use another folder.
Riverstone Supplies is fictional; every name and number is invented."""
import json, os
import duckdb

SENSORS = os.environ.get("CH48_SENSORS", os.path.join("..", "ch48", "sensor_readings"))
DAY = "2025-12-01"


def readings(minute_from, minute_to, machine=None):
    """Events for minutes minute_from, minute_from + 1, ..., minute_to - 1 of 1 December 2025."""
    where = ["EXTRACT(hour FROM reading_ts) * 60 + EXTRACT(minute FROM reading_ts) >= ?",
             "EXTRACT(hour FROM reading_ts) * 60 + EXTRACT(minute FROM reading_ts) < ?"]
    params = [minute_from, minute_to]
    if machine:
        where.append("machine_id = ?")
        params.append(machine)
    path = os.path.join(SENSORS, f"reading_date={DAY}", "*.parquet").replace("\\", "/")
    sql = f"""SELECT machine_id, plant, reading_ts, temperature_c, units_made, scrap_flag
              FROM read_parquet('{path}')
              WHERE {' AND '.join(where)}
              ORDER BY reading_ts, machine_id"""
    rows = duckdb.connect().execute(sql, params).fetchall()
    return [{"machine_id": r[0], "plant": r[1], "event_time": r[2].isoformat(sep=" "),
             "temperature_c": float(r[3]), "units_made": int(r[4]), "scrap": bool(r[5])}
            for r in rows]


def write_batch(folder, name, events):
    """Write events as JSON lines into folder/name; return the file's path."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    with open(path, "w") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")
    return path
