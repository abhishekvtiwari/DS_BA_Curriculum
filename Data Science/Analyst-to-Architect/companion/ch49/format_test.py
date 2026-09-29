"""Chapter 49 companion: the same day of sensor readings in five formats, sized and timed.
Writes storage/formats/ as CSV, gzip-compressed CSV, JSON, Excel and Parquet (216,000 readings,
8 columns), then reads each back with pandas and prints a table of sizes and read times.
Run:  python format_test.py        (after setup_ch49.py has built storage/day.parquet;
                                     about two minutes, most of it writing and reading Excel)
Times depend on your computer; the pattern doesn't. Each read is timed three times and the
fastest kept, so the first, slower read (files not yet in memory) doesn't count.
Riverstone Supplies is fictional; every name and number is invented."""
import os, time
import pandas as pd

FOLDER = os.path.join("storage", "formats")

def best_of_3(job):
    times = []
    for _ in range(3):
        start = time.perf_counter()
        job()
        times.append(time.perf_counter() - start)
    return min(times)

def main():
    os.makedirs(FOLDER, exist_ok=True)
    day = pd.read_parquet(os.path.join("storage", "day.parquet"))
    paths = {name: os.path.join(FOLDER, "day." + ext) for name, ext in
             [("CSV", "csv"), ("CSV, gzip", "csv.gz"), ("JSON", "json"), ("Excel", "xlsx"), ("Parquet", "parquet")]}
    day.to_csv(paths["CSV"], index=False)
    day.to_csv(paths["CSV, gzip"], index=False, compression="gzip")
    day.to_json(paths["JSON"], orient="records", lines=True, date_format="iso")
    day.to_excel(paths["Excel"], index=False)
    day.to_parquet(paths["Parquet"], index=False)

    readers = {
        "CSV":       (lambda: pd.read_csv(paths["CSV"]),
                      lambda: pd.read_csv(paths["CSV"], usecols=["temperature_c"])),
        "CSV, gzip": (lambda: pd.read_csv(paths["CSV, gzip"]),
                      lambda: pd.read_csv(paths["CSV, gzip"], usecols=["temperature_c"])),
        "JSON":      (lambda: pd.read_json(paths["JSON"], lines=True), None),
        "Excel":     (lambda: pd.read_excel(paths["Excel"]), None),
        "Parquet":   (lambda: pd.read_parquet(paths["Parquet"]),
                      lambda: pd.read_parquet(paths["Parquet"], columns=["temperature_c"])),
    }
    print(f"{'format':<10} {'size':>8}  {'read all':>9}  {'one column':>10}")
    for name, (read_all, read_one) in readers.items():
        size = os.path.getsize(paths[name]) / 1e6
        t_all = best_of_3(read_all)
        t_one = f"{best_of_3(read_one):.3f} s" if read_one else "-"
        print(f"{name:<10} {size:>5.1f} MB  {t_all:>7.3f} s  {t_one:>10}")

if __name__ == "__main__":
    main()
