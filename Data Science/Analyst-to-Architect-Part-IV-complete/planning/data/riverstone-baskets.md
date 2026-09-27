# Data spec: Riverstone order baskets (`riverstone-baskets`)

**Built by:** Part IV (first used in Chapter 38). **Planned reuse:** Ch 42 (recommenders), Ch 44.
**Generator:** `companion/generate_riverstone_baskets.py` · **Seed:** 20238 · **Output:** `companion/baskets/order_lines.csv` (92,359 rows, ~2.7 MB) and `products.csv` (24 rows) · **Runs in:** a few seconds
**Tested:** Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (18 Sep 2026)

## What it represents

Riverstone's 2025 order lines across the full 24-product catalog, for the 4,516 accounts that did not churn in 2025 (from `riverstone-accounts`). One **basket** is one order. Built because market basket analysis needs tens of thousands of baskets; the one-year teaching database has 173 orders.

## Tables

### `products.csv` — 24 rows
product_id (P01–P24) · product_name · category (Storage, Kitchen, Industrial, Furniture; 6 products each) · unit_price (₹60–₹4,600)

### `order_lines.csv` — 92,359 rows; grain: one product in one order
order_id (900001+; 33,931 orders) · account_id (joins `accounts.csv`) · order_date (2025) · product_id · quantity (lognormal, 1–400)

Order lines carry no product name or segment: join `products.csv` for names and `accounts.csv` for segment, as Chapter 38 does.

## Planted structure

- **Basket size:** 1 + Poisson(1.3) chosen products, capped at 6, plus partners from the rules below. Mean 2.72 lines, median 2, max 10.
- **Segment tastes** decide which category a basket starts from: Retail 40% Storage / 35% Kitchen; Hospitality 62% Kitchen; Wholesale 50% Industrial.
- **Co-purchase rules** (probability a partner joins the basket): Storage Crate 50L → Crate Lid (50L) 0.62 · Storage Crate 80L → Crate Lid (80L) 0.58 · Food Container 2L/5L → Airtight Seal Pack 0.55/0.50 · Industrial Crate 200L → Dolly Wheels 0.34 · Pallet Box → Dolly Wheels 0.30 · Drum 60L → Drum Tap Fitting 0.66 · Garden Chair → Chair Cushion Set 0.45 and Garden Table 0.28 · Garden Table → Garden Chair 0.40 · Stacking Bin Small → Stacking Bin Large 0.30.
- **Order counts per account** scale with the account's 2025 revenue, so key accounts place many baskets.

Resulting headline numbers used in Chapter 38: support(Storage Crate 50L) 0.1229, support(Crate Lid 50L) 0.1916, both 0.0821, confidence 0.668, lift 3.49; 1,001 of 3,412 Drum 60L orders (29.3%) have no tap fitting.

## Consistency

Accounts and segments come from `riverstone-accounts`. The 24-product catalog extends the 8 products in the teaching databases (those are the subset used for the SQL chapters); product IDs are P01–P24 and don't join to the teaching databases' product IDs.
