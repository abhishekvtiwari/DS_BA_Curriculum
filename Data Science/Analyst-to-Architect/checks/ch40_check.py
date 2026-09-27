"""Analyst to Architect · Chapter 40 · number check.
Recomputes the numbers quoted in Chapter 40's prose and writes checks/ch40_results.json for the figures.
Run from checks/: python3 ch40_check.py   (about 1 minute). Riverstone Supplies is fictional."""
import json, logging, pathlib, warnings
import numpy as np, pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import acf, adfuller, pacf
warnings.filterwarnings("ignore"); logging.getLogger("cmdstanpy").setLevel(logging.ERROR)
HERE = pathlib.Path(__file__).resolve().parent; COMP = HERE.parent / "companion"
fails = 0
def ok(label, got, want):
    global fails
    good = got == want; fails += not good
    print(("OK  " if good else "BAD ") + f"{label}: {got} (text: {want})")

weekly = pd.read_csv(COMP / "demand" / "weekly_demand.csv", parse_dates=["week_start"])
monthly = pd.read_csv(COMP / "demand" / "monthly_demand.csv", parse_dates=["month"])
ok("weekly rows", len(weekly), 1461); ok("missing", int(weekly.units.isna().sum()), 1); ok("dups", int(weekly.duplicated(["category", "week_start"]).sum()), 1)
k = monthly[monthly.category == "Kitchen"].set_index("month").units.astype(float).asfreq("MS")
yearly = k.groupby(k.index.year).sum(); ok("2019/2025 totals (thousands)", (round(yearly[2019] / 1000), round(yearly[2025] / 1000)), (657, 1051))
parts = seasonal_decompose(k, model="multiplicative", period=12); si = parts.seasonal[:12]
ok("Oct/Nov factors", (round(si.iloc[9], 2), round(si.iloc[10], 2)), (1.43, 1.30))
ok("Apr-Jun range", (round(si.iloc[3:6].min(), 2), round(si.iloc[3:6].max(), 2)), (0.82, 0.85))
ok("ADF raw p", round(adfuller(k)[1], 2), 0.98)
train, test = k[:"2024-12"], k["2025"]
wape = lambda a, f: np.abs(np.asarray(a) - np.asarray(f)).sum() / np.asarray(a).sum()
ok("naive", round(wape(test, np.repeat(train.iloc[-1], 12)) * 100, 1), 17.7); ok("seasonal naive", round(wape(test, train["2024"].to_numpy()) * 100, 1), 10.0)
ok("moving average", round(wape(test, np.repeat(train.iloc[-12:].mean(), 12)) * 100, 1), 14.1); ok("mean 2024", round(train.iloc[-12:].mean()), 80171)
hw = ExponentialSmoothing(train, trend="add", seasonal="mul", seasonal_periods=12).fit()
ok("HW wape", round(wape(test, hw.forecast(12)) * 100, 1), 17.5); ok("HW alpha/gamma", (round(hw.params["smoothing_level"], 3), round(hw.params["smoothing_seasonal"], 3)), (0.725, 0.0))
st = np.log(train).diff().diff(12).dropna(); a = acf(st, nlags=24); pa = pacf(st, nlags=24)
ok("lag12 acf/pacf", (round(a[12], 2), round(pa[12], 2)), (-0.34, -0.48)); ok("band", round(2 / np.sqrt(len(st)), 2), 0.26)
sar = SARIMAX(np.log(train), order=(1, 1, 1), seasonal_order=(0, 1, 1, 12)).fit(disp=False); fc = np.exp(sar.forecast(12))
ok("SARIMA wape", round(wape(test, fc) * 100, 1), 4.0); ok("coefs", (round(sar.params["ar.L1"], 2), round(sar.params["ma.S.L12"], 2)), (0.7, -0.64))
ci = np.exp(sar.get_forecast(12).conf_int(alpha=0.2)); ok("Dec interval", (round(ci.iloc[-1, 0], -3), round(ci.iloc[-1, 1], -3)), (71000.0, 116000.0))
err = test.to_numpy() - fc.to_numpy(); ok("abs error sum ~42,000", round(np.abs(err).sum(), -3), 42000.0); ok("bias", round(err.mean()), 776)
ok("July error", (round(np.abs(err).max()), test.index[np.abs(err).argmax()].month), (10464, 7)); ok("July pct", round(10464 / 74926 * 100), 14)
naive_ins = np.abs(train.to_numpy()[12:] - train.to_numpy()[:-12]).mean(); ok("MASE", round(np.abs(err).mean() / naive_ins, 2), 0.37)
ok("annual under", round((fc.sum() - test.sum()) / test.sum() * 100, 1), -0.9)
def backtest(series, fn, horizon=12, folds=5):
    out = []
    for f in range(folds):
        cut = len(series) - horizon * (folds - f); out.append(wape(series.iloc[cut:cut + horizon], fn(series.iloc[:cut], horizon)))
    return np.array(out)
meths = {"seasonal naive": lambda h, n: h.iloc[-12:].to_numpy()[:n],
         "Holt-Winters": lambda h, n: ExponentialSmoothing(h, trend="add", seasonal="mul", seasonal_periods=12).fit().forecast(n).to_numpy(),
         "SARIMA": lambda h, n: np.exp(SARIMAX(np.log(h), order=(1, 1, 1), seasonal_order=(0, 1, 1, 12)).fit(disp=False).forecast(n)).to_numpy()}
bt = {n: backtest(k, f) for n, f in meths.items()}
ok("backtest means", {n: round(v.mean() * 100, 1) for n, v in bt.items()}, {"seasonal naive": 12.8, "Holt-Winters": 13.2, "SARIMA": 11.3})
ok("worst folds", (round(bt["seasonal naive"][0] * 100, 1), round(bt["SARIMA"][0] * 100, 1)), (20.7, 16.6))
allow = bt["SARIMA"].mean() + bt["SARIMA"].std(); ok("allowance", round(allow * 100, 1), 15.7)
# sensors
r = pd.read_csv(COMP / "sensors" / "machine_readings_week.csv", parse_dates=["timestamp"]); ok("readings", len(r), 10080)
temp = r.set_index("timestamp").temperature_c.interpolate(); ok("hottest", (f"{temp.idxmax():%a %H:%M}", round(temp.max(), 1)), ("Wed 22:53", 225.2))
m2 = temp.rolling("120min").mean().shift(1); s2 = temp.rolling("120min").std().shift(1); z = (temp - m2) / s2
ok("z alerts", int((z.abs() > 4).sum()), 3); ok("z at hottest", round(z[temp.idxmax()], 1), 2.8)
base = temp.rolling("24h").median().shift(1); ex = temp - base; sus = (ex > 6).rolling(10).sum() == 10
ok("first alert", f"{sus[sus].index.min():%a %H:%M}", "Wed 22:51")
stops = r[r.status == "stopped"]; ok("stoppage", (f"{stops.timestamp.min():%a %H:%M}", f"{stops.timestamp.max():%H:%M}", len(stops)), ("Wed 22:02", "22:33", 32))
json.dump({"kitchen": {str(d.date()): v for d, v in k.items()}, "trend": {str(d.date()): (None if np.isnan(v) else v) for d, v in parts.trend.items()},
           "seasonal": si.tolist(), "resid": {str(d.date()): (None if np.isnan(v) else v) for d, v in parts.resid.items()},
           "acf": a.tolist(), "pacf": pa.tolist(), "band": 2 / np.sqrt(len(st)), "n": len(k),
           "temp": {str(t): v for t, v in temp.items()}, "baseline": {str(t): (None if np.isnan(v) else v) for t, v in base.items()},
           "pressure": {str(t): v for t, v in r.set_index("timestamp").pressure_bar.items()}, "status": r.status.tolist()},
          open(HERE / "ch40_results.json", "w"))
print("All checks passed." if not fails else f"FAILED: {fails}"); raise SystemExit(1 if fails else 0)
