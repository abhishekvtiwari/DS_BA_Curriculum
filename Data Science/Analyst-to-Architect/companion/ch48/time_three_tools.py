"""Chapter 48 companion: time the same question in DuckDB, Polars, and Spark (section 48.6).
Each engine gets two cores, and each timing is the fastest of three runs, in milliseconds.
Run from the practice folder after make_sensor_data.py and make_sensor_data.py --small:
    python time_three_tools.py
Your numbers will differ from the book's: they depend on your computer.
Riverstone Supplies is fictional; every name and number is invented."""
import os, time
os.environ["POLARS_MAX_THREADS"] = "2"          # must be set before polars is imported
import duckdb, polars as pl
from pyspark.sql import SparkSession, functions as F

QUESTION = """
    SELECT plant,
           ROUND(AVG(temperature_c), 2)                 AS avg_temp_c,
           ROUND(AVG(CAST(scrap_flag AS INT)) * 100, 2) AS scrap_pct,
           SUM(units_made)::BIGINT                      AS units
    FROM readings
    WHERE temperature_c > 190
    GROUP BY plant
    ORDER BY plant"""


def best_of_3(job):
    """Run job three times; return the fastest time, in milliseconds."""
    times = []
    for _ in range(3):
        start = time.perf_counter()
        job()
        times.append(time.perf_counter() - start)
    return min(times) * 1000


spark = (SparkSession.builder.appName("riverstone-timings").master("local[2]")
         .config("spark.ui.showConsoleProgress", "false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
spark.conf.set("spark.sql.shuffle.partitions", 8)

for folder in ["sensor_readings_small", "sensor_readings"]:
    con = duckdb.connect()
    con.execute("SET threads = 2")
    con.execute(f"CREATE VIEW readings AS SELECT * FROM read_parquet('{folder}/*/*.parquet')")
    readings = spark.read.parquet(folder)
    rows = readings.count()

    duckdb_job = lambda: con.execute(QUESTION).fetchall()
    polars_job = lambda: (pl.scan_parquet(f"{folder}/*/*.parquet")
                            .filter(pl.col("temperature_c") > 190).group_by("plant")
                            .agg(pl.col("temperature_c").mean(), pl.col("scrap_flag").cast(pl.Int8).mean(),
                                 pl.col("units_made").sum())
                            .collect())
    spark_job = lambda: (readings.filter(F.col("temperature_c") > 190).groupBy("plant")
                            .agg(F.avg("temperature_c"), F.avg(F.col("scrap_flag").cast("int")),
                                 F.sum("units_made"))
                            .collect())

    print(f"{folder} ({rows:,} readings)")
    for name, job in [("DuckDB", duckdb_job), ("Polars", polars_job), ("Spark", spark_job)]:
        print(f"  {name:<7}{best_of_3(job):8.1f} ms")

print("cores on this computer:", os.cpu_count())
spark.stop()
