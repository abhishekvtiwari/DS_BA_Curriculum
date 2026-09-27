"""Chapter 49 companion: build the storage examples from the Chapter 48 sensor data.
Creates, for one day (2025-12-01, 216,000 readings):
  storage/day.csv          the same data as CSV (row oriented, text)
  storage/day.parquet      the same data as Parquet (columnar, compressed)
  storage/day.sqlite       the same data in a row-store database table
Run: python3 setup_ch49.py        (needs ../ch48/sensor_readings; run make_sensor_data.py there first)
Riverstone Supplies is fictional; every name and number is invented."""
import os, shutil, sqlite3
import duckdb

SENSORS = os.environ.get("CH48_SENSORS", "../ch48/sensor_readings")
DAY = "2025-12-01"

def build(folder="storage"):
    shutil.rmtree(folder, ignore_errors=True); os.makedirs(folder)
    con = duckdb.connect()
    con.execute(f"""CREATE VIEW day AS
        SELECT machine_id, plant, line_type, reading_ts, temperature_c, pressure_bar, units_made, scrap_flag
        FROM read_parquet('{SENSORS}/reading_date={DAY}/*.parquet')""")
    con.execute(f"COPY day TO '{folder}/day.csv' (FORMAT csv, HEADER true)")
    con.execute(f"COPY day TO '{folder}/day.parquet' (FORMAT parquet, COMPRESSION snappy)")
    rows = con.execute("SELECT * FROM day").fetchall()
    lite = sqlite3.connect(os.path.join(folder, "day.sqlite"))
    lite.execute("""CREATE TABLE readings (machine_id TEXT, plant TEXT, line_type TEXT, reading_ts TEXT,
                    temperature_c REAL, pressure_bar REAL, units_made INTEGER, scrap_flag INTEGER)""")
    lite.executemany("INSERT INTO readings VALUES (?,?,?,?,?,?,?,?)",
                     [(r[0], r[1], r[2], str(r[3]), r[4], r[5], r[6], int(r[7])) for r in rows])
    lite.commit(); lite.execute("VACUUM"); lite.close()
    return len(rows)

if __name__ == "__main__":
    n = build()
    for f in sorted(os.listdir("storage")):
        print(f"{f:<14} {os.path.getsize(os.path.join('storage', f)) / 1e6:>8.1f} MB")
    print(f"{n:,} readings for {DAY}")
