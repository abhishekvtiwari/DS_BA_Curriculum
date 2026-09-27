"""
Analyst to Architect · Riverstone customer accounts dataset (first used in Chapter 37; reused in Chapters 38, 39, 44)
generate_riverstone_accounts.py: one row per B2B customer account, described as of 31 December 2024,
with what happened in 2025 (revenue and churn).

Run:     python3 generate_riverstone_accounts.py        (writes into companion/accounts/)
Writes:  accounts/accounts.csv
Seed:    20237 (the same seed always produces the same file)
Tested:  Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (17 September 2026)
Spec:    planning/data/riverstone-accounts.md

Riverstone Supplies is fictional; every name and number is invented.
"""
import pathlib
import numpy as np
import pandas as pd

rng = np.random.default_rng(20237)
OUT = pathlib.Path(__file__).resolve().parent / "accounts"
OUT.mkdir(exist_ok=True)
N = 5000

segment = rng.choice(["Retail", "Hospitality", "Wholesale"], size=N, p=[0.47, 0.33, 0.20])
city_tier = rng.choice(["Metro", "Tier 2", "Tier 3"], size=N, p=[0.42, 0.38, 0.20])
rep_id = rng.choice([3, 4, 5, 9], size=N, p=[0.27, 0.27, 0.26, 0.20])
size_band = np.where(segment == "Wholesale", rng.choice(["Small", "Medium", "Large"], size=N, p=[0.25, 0.45, 0.30]),
                     rng.choice(["Small", "Medium", "Large"], size=N, p=[0.55, 0.33, 0.12]))
tenure_months = np.clip(np.round(rng.gamma(2.2, 14, N)), 1, 120).astype(int)
size_scale = pd.Series(size_band).map({"Small": 1.0, "Medium": 2.6, "Large": 7.0}).to_numpy()
seg_scale = pd.Series(segment).map({"Retail": 1.0, "Hospitality": 1.2, "Wholesale": 3.0}).to_numpy()
base_rev = rng.lognormal(np.log(90_000), 0.55, N) * size_scale * seg_scale          # "true" annual spend level

orders_2024 = np.maximum(1, rng.poisson(np.clip(base_rev / 22_000, 1, 60)))
revenue_2024 = np.round(base_rev * rng.lognormal(0, 0.18, N), -2)
revenue_2023 = np.where(tenure_months > 12, np.round(base_rev * rng.lognormal(-0.05, 0.25, N), -2), np.nan)
units_2024 = np.round(revenue_2024 / rng.normal(310, 40, N))
avg_discount_pct = np.round(np.clip(rng.normal(4, 2, N) + np.where(segment == "Wholesale", 3.5, 0) + 1.2 * np.log(size_scale), 0, 18), 1)
late_payment_days = np.round(np.clip(rng.gamma(1.3, 9, N) + np.where(size_band == "Small", 6, 0), 0, 120), 0)
complaints_2024 = rng.poisson(0.25 + orders_2024 * 0.02)
categories_bought = np.clip(rng.poisson(1.2 + np.log(size_scale)), 1, 4)
days_since_last_order = np.round(np.clip(rng.exponential(365 / (orders_2024 + 1.5) * 1.4), 1, 365))
website_logins_2024 = rng.poisson(6 + 2 * (city_tier == "Metro"))
catalog_downloads_2024 = rng.poisson(1.5, N)                                        # no real effect (planted noise feature)

# ---------------- churn in 2025 (no order in 2025): non-linear, with interactions ----------------
logit = np.full(N, -3.3)
logit += np.where(days_since_last_order > 90, 1.6, 0) + np.where(days_since_last_order > 180, 1.5, 0)   # thresholds, not a straight line
logit += np.where((late_payment_days > 25) & (size_band == "Small") & (segment == "Retail"), 2.4, 0)     # interaction
logit += np.where((complaints_2024 >= 2) & (tenure_months < 18), 2.0, 0)                               # interaction
logit += np.where((avg_discount_pct > 9) & (segment != "Wholesale"), 1.2, 0)                           # deep discounts outside wholesale: price shoppers
logit += -0.6 * (categories_bought - 1)
logit += np.where(tenure_months < 6, 1.0, 0)
logit += np.where((segment == "Hospitality") & (city_tier == "Tier 3"), 1.1, 0)
logit += np.where(rep_id == 9, 0.3, 0)
p_churn = 1 / (1 + np.exp(-logit))
churned_2025 = (rng.random(N) < p_churn).astype(int)

# ---------------- revenue in 2025 for accounts that stayed ----------------
growth = 0.04 + np.where(segment == "Hospitality", 0.06, 0) + np.where((segment == "Hospitality") & (city_tier == "Metro"), 0.08, 0)
growth += np.where(categories_bought >= 3, 0.07, 0) - 0.004 * late_payment_days - 0.03 * complaints_2024
growth += 0.004 * (avg_discount_pct - 5)
log_rev_25 = np.log(revenue_2024) + growth + rng.normal(0, 0.22, N)
revenue_2025 = np.where(churned_2025 == 1, 0.0, np.round(np.exp(log_rev_25), -2))

prefix = ["Shree", "Metro", "Royal", "Green", "Sunrise", "Coastal", "Prime", "City", "Golden", "Everest", "Lotus", "Kaveri",
          "Silver", "Sagar", "Ganesh", "Classic", "Star", "Heritage", "Deccan", "Western"]
suffix = {"Retail": ["Stores", "Mart", "Traders", "Hardware"], "Hospitality": ["Hotels", "Caterers", "Restaurants", "Banquets"],
          "Wholesale": ["Distributors", "Wholesale", "Packaging", "Logistics"]}
names = [f"{rng.choice(prefix)} {rng.choice(suffix[s])} {i:04d}" for i, s in enumerate(segment, start=1)]

df = pd.DataFrame({
    "account_id": np.arange(5001, 5001 + N), "account_name": names, "segment": segment, "city_tier": city_tier,
    "company_size": size_band, "rep_id": rep_id, "tenure_months": tenure_months, "orders_2024": orders_2024,
    "units_2024": units_2024, "revenue_2023": revenue_2023, "revenue_2024": revenue_2024,
    "avg_discount_pct": avg_discount_pct, "late_payment_days": late_payment_days, "complaints_2024": complaints_2024,
    "categories_bought": categories_bought, "days_since_last_order": days_since_last_order,
    "website_logins_2024": website_logins_2024, "catalog_downloads_2024": catalog_downloads_2024,
    "churned_2025": churned_2025, "revenue_2025": revenue_2025,
})
# planted messiness: a few blanks
df.loc[rng.random(N) < 0.03, "late_payment_days"] = np.nan
df.to_csv(OUT / "accounts.csv", index=False)
print(f"{len(df):,} accounts · churn rate {df['churned_2025'].mean():.1%} · median 2024 revenue ₹{df['revenue_2024'].median():,.0f}")
