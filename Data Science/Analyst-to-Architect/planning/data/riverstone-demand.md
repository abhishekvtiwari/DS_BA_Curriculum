# Data spec: Riverstone demand history (`riverstone-demand`)

**Built by:** Part IV (first used in Chapter 40). **Planned reuse:** Ch 44 (capstone option), Ch 45 (business metrics), Ch 52 (monitoring a forecast).
**Generator:** `companion/generate_riverstone_demand.py` · **Seed:** 20240 · **Output:** `companion/demand/weekly_demand.csv` (1,461 rows), `monthly_demand.csv` (336 rows) · **Runs in:** under 1 s
**Tested:** Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (18 Sep 2026)

## What it represents
Units shipped per product category (Storage, Kitchen, Industrial, Furniture), 7 January 2019 to 29 December 2025. Weekly grain: one row per category per week starting Monday. Monthly grain: each week's units spread evenly over its days and summed by calendar month (so months are comparable regardless of how many Mondays they contain).

## Columns
`weekly_demand.csv`: week_start (Monday) · category · units (int; one NaN and one duplicated row planted for Storage).
`monthly_demand.csv`: category · month (first of month) · units (int; clean: the missing week is interpolated before aggregation).

## Planted structure (per category: base weekly level, yearly growth, festive peak, spring effect, noise sd)
Storage 9,000 / 6% / +35% / −10% / 0.07 · Kitchen 11,000 / 9% / +55% / −5% / 0.08 · Industrial 6,000 / 4% / +5% / 0 / 0.10 · Furniture 3,500 / 12% / +20% / +25% (spring garden season) / 0.12.
Festive peak is a Gaussian bump centred on day 300 (late October, width 22 days); the spring bump is centred on day 120. A slow 3.5-year cycle of ±3%. Noise is AR(1) with coefficient 0.45 on the log scale. **Shock:** −45% from 23 March to 30 June 2020 and −15% July–September 2020.

## Headline numbers used in Chapter 40 (Kitchen, monthly)
Seasonal factors Oct 1.43, Nov 1.30, Apr–Jun 0.82–0.85 · 2025 WAPE: naive 17.7%, seasonal naive 10.0%, moving average 14.1%, Holt–Winters 17.5%, SARIMA (1,1,1)(0,1,1)12 on logs 4.0%, Prophet 5.9% · five-fold backtest means: seasonal naive 12.8%, Holt–Winters 13.2%, SARIMA 11.3%, Prophet 13.3%.

## Consistency
Categories match the product catalog. Volumes are units shipped across all customers, far above the teaching databases' order lines (which are a small named subset); no join to other datasets.
