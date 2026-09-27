# Data spec: Riverstone customer accounts (`riverstone-accounts`)

**Built by:** Part IV (first used in Chapter 37). **Planned reuse:** Ch 38 (segmentation), Ch 39 (cost-based thresholds, calibration, SHAP, fairness), Ch 44 (capstone).
**Generator:** `companion/generate_riverstone_accounts.py` · **Seed:** 20237 · **Output:** `companion/accounts/accounts.csv` (5,000 rows, ~430 KB) · **Runs in:** under 1 s
**Tested:** Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (17 Sep 2026)

## What it represents

Every B2B customer account Riverstone has served, described **as of 31 December 2024** (the prediction moment), with what happened in **2025**. Grain: one row per account.

## Columns

| Column | Type | Notes |
|---|---|---|
| account_id | int | 5001–10000 |
| account_name | text | Generated name + 4-digit number; no signal |
| segment | text | Retail 47%, Hospitality 33%, Wholesale 20% |
| city_tier | text | Metro 42%, Tier 2 38%, Tier 3 20% |
| company_size | text | Small / Medium / Large (Wholesale skews larger) |
| rep_id | int | 3 Neha Kulkarni, 4 Rahul Mehta, 5 Farah Khan, 9 Inside Sales Desk |
| tenure_months | int | 1–120 (gamma distributed; median ~26) |
| orders_2024, units_2024, revenue_2023, revenue_2024 | numbers | Lognormal spend scaled by size and segment; revenue_2023 blank if tenure ≤ 12 months; units and orders strongly correlated with revenue (planted multicollinearity) |
| avg_discount_pct | float | Higher for Wholesale and larger accounts |
| late_payment_days | float | Average days late; higher for Small; 3% blank |
| complaints_2024 | int | Poisson, rises with orders |
| categories_bought | int | 1–4 product categories |
| days_since_last_order | float | Recency at 31 Dec 2024 |
| website_logins_2024 | int | Slightly higher in Metro; no planted effect on churn |
| catalog_downloads_2024 | int | Pure noise feature |
| **churned_2025** | 0/1 | No order in 2025. Rate 9.7% (484 accounts) |
| **revenue_2025** | float | 0 if churned; otherwise log-growth model below |

## Planted signal

**Churn (logit, intercept −3.3):** no order for > 90 days +1.6, and > 180 days a further +1.5 (thresholds) · late payment > 25 days **and** Small **and** Retail +2.4 (interaction) · complaints ≥ 2 **and** tenure < 18 months +2.0 (interaction) · discount > 9% outside Wholesale +1.2 · −0.6 per extra category bought · tenure < 6 months +1.0 · Hospitality in Tier 3 +1.1 · Inside Sales Desk +0.3. True-probability ceiling AUC: 0.858.

**2025 revenue (stayers):** log(revenue_2025) = log(revenue_2024) + growth + N(0, 0.22), where growth = 0.04, +0.06 Hospitality, +0.08 Hospitality in Metro, +0.07 if ≥ 3 categories, −0.004 per late-payment day, −0.03 per complaint, +0.004 per discount point above 5. No rep effect (the inside-desk coefficient seen among stayers is selection bias; Ch 37 exercise 13).

## Consistency with other Riverstone data

Same reps, segments, and product categories as `riverstone`, `riverstone_2025`, and the CRM export. **Unavoidable differences:** 5,000 accounts is far more than the 24 customers in the teaching databases (which are a small named subset) and more than CRM wins since 2023 (accounts go back up to 10 years). Account IDs and names don't join to other datasets. New fact for the coordinator: Riverstone's customer base is about 5,000 active and recently active B2B accounts at the end of 2024.
