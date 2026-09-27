import time, statistics, duckdb, polars as pl
from pyspark.sql import SparkSession, functions as F
Q = """SELECT plant, ROUND(AVG(temperature_c),2) a, ROUND(AVG(CAST(scrap_flag AS INT))*100,2) s, SUM(units_made)::BIGINT u
FROM readings WHERE temperature_c > 190 GROUP BY plant ORDER BY plant"""
def bench(fn, n=3):
    ts=[]
    for _ in range(n):
        t=time.perf_counter(); fn(); ts.append(time.perf_counter()-t)
    return round(min(ts),2), round(statistics.median(ts),2)
for folder,label in [("sensor_readings_small","1M rows (216,000 x 1 day)"),("sensor_readings","19.87M rows")]:
    con=duckdb.connect(); con.execute(f"CREATE VIEW readings AS SELECT * FROM read_parquet('{folder}/*/*.parquet')")
    d=bench(lambda: con.execute(Q).fetchall())
    p=bench(lambda: (pl.scan_parquet(f"{folder}/*/*.parquet").filter(pl.col("temperature_c")>190)
        .group_by("plant").agg([pl.col("temperature_c").mean(), pl.col("scrap_flag").cast(pl.Int8).mean(), pl.col("units_made").sum()]).sort("plant").collect()))
    print(label, "duckdb", d, "polars", p)
spark=(SparkSession.builder.master("local[*]").config("spark.sql.shuffle.partitions","8").config("spark.ui.showConsoleProgress","false").getOrCreate())
spark.sparkContext.setLogLevel("ERROR")
for folder,label in [("sensor_readings_small","1M"),("sensor_readings","19.87M")]:
    df=spark.read.parquet(folder)
    f=lambda: (df.filter(F.col("temperature_c")>190).groupBy("plant")
        .agg(F.avg("temperature_c"), F.avg(F.col("scrap_flag").cast("int")), F.sum("units_made")).orderBy("plant").collect())
    print(label, "spark", bench(f))
print("startup: new SparkSession + first count")
t=time.perf_counter(); spark.read.parquet("sensor_readings_small").count(); print(round(time.perf_counter()-t,2))
import os; print("cores:", os.cpu_count())
