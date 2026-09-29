"""
Analyst to Architect · Riverstone demand history (used in Chapter 40)
generate_riverstone_demand.py: units shipped per product category, weekly and monthly, 2019–2025.

Run:     python3 generate_riverstone_demand.py      (writes into companion/demand/)
Writes:  demand/weekly_demand.csv (365 weeks x 4 categories), demand/monthly_demand.csv (84 months x 4)
Seed:    20240
Tested:  Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (18 September 2026)

Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd

rng = np.random.default_rng(20240)
OUT = pathlib.Path(__file__).resolve().parent / "demand"
OUT.mkdir(exist_ok=True)

weeks = pd.date_range("2019-01-07", "2025-12-29", freq="W-MON")       # week starting Monday
n = len(weeks)
t = np.arange(n)
doy = weeks.dayofyear.to_numpy()

# planted structure per category: base level, yearly growth, festive peak (Oct–Nov), summer dip, noise
CATS = {
    "Storage":    dict(base=9000,  growth=0.06, festive=0.35, summer=-0.10, noise=0.07),
    "Kitchen":    dict(base=11000, growth=0.09, festive=0.55, summer=-0.05, noise=0.08),
    "Industrial": dict(base=6000,  growth=0.04, festive=0.05, summer=0.00,  noise=0.10),
    "Furniture":  dict(base=3500,  growth=0.12, festive=0.20, summer=0.25,  noise=0.12),
}
festive_curve = np.exp(-0.5 * ((doy - 300) / 22) ** 2)          # peak around late October
summer_curve = np.exp(-0.5 * ((doy - 120) / 30) ** 2)           # peak around late April
covid = np.where((weeks >= "2020-03-23") & (weeks < "2020-07-01"), -0.45, 0.0)
covid += np.where((weeks >= "2020-07-01") & (weeks < "2020-10-01"), -0.15, 0.0)

frames = []
for cat, p in CATS.items():
    level = p["base"] * (1 + p["growth"]) ** (t / 52)
    seasonal = 1 + p["festive"] * festive_curve + p["summer"] * summer_curve
    cycle = 1 + 0.03 * np.sin(2 * np.pi * t / 52 / 3.5)          # a slow business cycle, ~3.5 years
    ar_noise = np.zeros(n)
    for i in range(1, n):
        ar_noise[i] = 0.45 * ar_noise[i - 1] + rng.normal(0, p["noise"])
    units = level * seasonal * cycle * (1 + covid) * np.exp(ar_noise)
    units = np.round(units)
    frames.append(pd.DataFrame({"week_start": weeks, "category": cat, "units": units.astype(int)}))
weekly = pd.concat(frames)
# a couple of planted data problems: one missing week and one duplicated week for Storage
weekly.loc[(weekly["category"] == "Storage") & (weekly["week_start"] == "2023-08-14"), "units"] = np.nan
dup = weekly[(weekly["category"] == "Storage") & (weekly["week_start"] == "2022-02-07")]
weekly = pd.concat([weekly, dup]).sort_values(["category", "week_start"])
weekly.to_csv(OUT / "weekly_demand.csv", index=False)

# monthly totals: spread each week's units evenly over its 7 days, then sum by calendar month
clean = weekly.drop_duplicates(["category", "week_start"]).reset_index(drop=True)
clean["units"] = clean.groupby("category")["units"].transform(lambda u: u.interpolate())   # the monthly file is clean
daily = clean.loc[clean.index.repeat(7)].copy()
daily["day"] = daily["week_start"] + pd.to_timedelta(daily.groupby(level=0).cumcount(), unit="D")
daily["units"] = daily["units"] / 7
daily["month"] = daily["day"].dt.to_period("M").dt.to_timestamp()
monthly = daily[daily["day"] <= "2025-12-31"].groupby(["category", "month"], as_index=False)["units"].sum(min_count=7)
monthly = monthly[monthly["month"] >= "2019-01-01"]
monthly["units"] = monthly["units"].round().astype("Int64")
monthly.to_csv(OUT / "monthly_demand.csv", index=False)
print(f"{n} weeks x {len(CATS)} categories; {monthly['month'].nunique()} months")
