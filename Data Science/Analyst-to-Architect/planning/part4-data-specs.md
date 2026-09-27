# Part IV data specs

One spec per dataset built in Part IV (Chapters 35-44). Written by the Part IV chat, accepted by the coordinator on 19 September 2026.


---

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


---

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


---

# Data spec: Riverstone CRM export (`riverstone-crm`)

**Built by:** Part IV (first used in Chapter 36). **Reused by:** Ch 37, 39, 44 (and available to Ch 23 in Part II).
**Generator:** `companion/generate_riverstone_crm.py` · **Seed:** 20236 · **Output:** `companion/crm/*.csv` · **Export time:** 2025-12-31 23:59
**Tested:** Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (17 Sep 2026). Runs in about 10 seconds.

## What it represents

Riverstone's full CRM export: every sales enquiry from 1 January 2023 to 31 December 2025, from all sources, including B2B marketplace leads and web-form leads handled by an inside sales desk.

## Tables

### `leads.csv` — 12,294 rows (12,026 enquiries + 268 planted duplicate submissions); grain: one CRM lead record

| Column | Type | Notes |
|---|---|---|
| lead_id | int | 100001+ for enquiries; 200001+ for duplicate resubmissions |
| created_at | datetime | 08:00–20:00; volume ~290/month (2023) → ~400/month (2025); seasonal peak Oct–Nov |
| company_name | text | Generated from 20 × 5 name parts per segment (300 distinct); carries no signal |
| email | text | Business domain (`slug.in`) or `gmail.com`; 4% upper-cased |
| source | text | Marketplace, Website, Trade fair, Referral, Cold call, Partner. Marketplace share 30% → 45% |
| segment | text | Retail, Hospitality, Wholesale; 5% blank |
| city | text | 17 cities; ~9% alternative spellings (Bombay, Bangalore, Poona, Madras, Calcutta, Panaji, case/space variants) |
| company_size | text | 1-10, 11-50, 51-200, 200+; 21% blank (random) |
| product_interest | text | Storage, Kitchen, Industrial, Furniture |
| est_quantity | float | Lognormal, median ~130; blank 28% for Marketplace, 7% otherwise (informative); 0.6% typos ×1000 |
| website_visits | int | Visits before the enquiry (Poisson; higher for Website) |
| enquiry_text | text | Phrase + product; strong / weak / neutral phrases |
| owner_id | int | 3 Neha Kulkarni, 4 Rahul Mehta, 5 Farah Khan, 9 Inside Sales Desk |
| first_response_hours | float | **Leakage trap.** Faster for leads reps sense are good; blank if never contacted |
| quote_sent_date | date | **Leakage trap.** Only for qualified leads; days to weeks after arrival |
| days_in_pipeline | float | **Leakage trap.** Arrival to close; many lost leads close at exactly 90 |
| status | text | Won, Lost, Open (Open = not closed by the export) |

### `activities.csv` — 25,682 rows; grain: one sales activity

activity_id · lead_id · activity_at (when it happened) · activity_type (Call, Email, Meeting, Sample sent, Quote sent) · logged_at (when recorded; ~10% logged 1–6 days late — **timestamp trap**)

### `stage_history.csv` — 39,275 rows; grain: one stage entry

lead_id · stage (New, Contacted, Qualified, Quote sent, Won, Lost) · entered_at

## Planted signal (win within 90 days)

Logistic model, intercept −3.05: source (Referral +1.35, Trade fair +0.85, Partner +0.6, Cold call +0.25, Website 0, Marketplace −0.75; extra −0.45 for Marketplace in 2025, the cheaper listing plan) · Wholesale +0.45, Hospitality +0.1 (+0.35 Aug–Oct) · size (1-10 −0.45 … 200+ +0.55) · +0.3 × log(quantity/120) · +0.12 per website visit (cap 6) · gmail −0.5 · strong text +0.6, weak −0.55 · inside desk −0.2. Overall win rate on settled, deduplicated leads: 7.7% (826 of 10,701).

## Planted messiness and traps

Duplicate web-form resubmissions within 2 days (268) · city spellings · blank segment/size/quantity (quantity blanks informative) · quantity typos · upper-case emails · three outcome-driven columns · late-logged activities · censored recent leads (Q4 2025 closed leads show an inflated win rate).

## Consistency with other Riverstone data

- Same sales people (IDs 3, 4, 5 under Vikram Singh and Anita Rao), segments, sources (plus Marketplace and Partner), cities, and product categories as `riverstone` and `riverstone_2025`.
- **Unavoidable difference:** `riverstone_2025.leads` holds only the ~43 enquiries reps logged directly in 2025 (30 unique). This export holds every enquiry, including marketplace and inside-sales-desk leads, which the one-year teaching database leaves out. Lead IDs and company names don't join to the one-year database. Documented in Ch 36 §36.1.
- New Riverstone facts introduced (for the coordinator): an **Inside Sales Desk** (owner ID 9) handles web and marketplace leads; Riverstone lists on a **B2B marketplace** and switched to a **cheaper listing plan in 2025**; Riverstone attends **two trade fairs a year (February and September)**.


---

# Data spec: Chapter 43 deep learning assets (`riverstone-deeplearning`)

**Built by:** Part IV (first used in Chapter 43). No new Riverstone dataset.

## What Chapter 43 uses
- **Tabular network:** Chapter 37's `companion/accounts/accounts.csv` and identical preprocessing pipeline (same `CATS`/`NUMS`, same train/valid/test split, `random_state=37`), so results compare directly against Chapter 37's logistic regression and gradient-boosting numbers.
- **Image classifier and transfer learning:** scikit-learn's bundled `load_digits()` dataset (1,797 8×8 handwritten-digit images, 10 classes). No download, no external data, no seed needed beyond `random_state=43` for the train/test splits and `torch.manual_seed(43)` for model initialization. Digits 0–4 form the "base" task; digits 5–9 (relabeled 0–4) form the "new" task for transfer learning.

## Headline numbers
XOR: single neuron converges to log(2) ≈ 0.6931 (no better than guessing); a 4-neuron hidden layer reaches 0.00097. Tabular churn (validation AUC): logistic regression 0.764, small network (561 params) 0.773, tuned gradient boosting 0.788. Base CNN (digits 0–4, 675 training images): 98.7% test accuracy. Transfer vs. from-scratch on digits 5–9 (5 examples/class): 85.7% vs 94.2%; at 30 examples/class: 92.9% vs 98.2%; at the extremes (1 and 50 examples/class) the pattern is noisier at n=1 (58.9% vs 59.8%, effectively tied) and clearly favors from-scratch at n=50 (95.1% vs 98.2%).

## Why no new dataset was needed
The chapter's purpose is method (how a neuron, a layer, backpropagation, a CNN, and transfer learning work), not a new business question — reusing Chapter 37's churn data for the tabular comparison keeps the "deep learning vs. Chapter 37 methods" comparison honest and directly comparable, and `load_digits()` gives a real, tiny, fully offline image dataset for the CNN and transfer-learning sections without requiring internet access to download pretrained weights (torchvision's pretrained models need `download.pytorch.org`, outside this environment's allowed network domains).

## Environment note for the coordinator
PyTorch 2.14.0 (CPU-compatible; installed via plain `pip install torch`, not the `--index-url download.pytorch.org` CPU wheel, which is unreachable from this network's allowed domains). Everything in the chapter trains in well under a minute total on one CPU core.


---

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


---

# Data spec: Chapter 42 recommender assets (`riverstone-recommenders`)

**Built by:** Part IV (first used in Chapter 42). No new order data: reuses `riverstone-baskets` (Ch 38) and `riverstone-accounts` (Ch 37) directly.
**New file:** `companion/ch42/products_text.py` — adds a hand-written one-sentence `description` column to each of the 24 products in `../baskets/products.csv`, for content-based filtering and cold-start demonstrations. Not seeded/randomized; the 24 descriptions are fixed text, written once.

## Why no new dataset
Chapter 42 is entirely built from data already in the project: the account-by-product interaction matrix comes from `baskets/order_lines.csv` (33,931 orders, 4,516 accounts, 24 products), segments and other account attributes come from `accounts/accounts.csv`, and the TF-IDF/cosine-similarity machinery is Chapter 41's, unchanged.

## Headline numbers (leave-one-out evaluation, precision@5 / NDCG@5, seed 42)
Popularity 61.4% / 0.428 · Item-based CF 67.6% / 0.510 · SVD 4 factors 66.2% / 0.490, 12 factors 49.0% / 0.329 (more factors overfits a 24-item catalog) · ALS 8 factors 69.8% / 0.489 (best), 16 factors 46.6% / 0.348 · Content-based 54.0% / 0.367 · 50/50 hybrid 65.4% / 0.460 · Segment-level popularity (exercise 8) 71.9% / 0.534 — beats every method above on this small catalog.

## Consistency
`products_text.py` must be imported before `products.csv` is used for content-based work in this chapter; it does not modify `baskets/products.csv` itself. Any later chapter reusing product descriptions should import from this file rather than duplicating the text.


---

# Data spec: Riverstone machine sensor readings (`riverstone-sensors`)

**Built by:** Part IV (first used in Chapter 40). **Planned reuse:** Ch 48 (big data; `--full`), Ch 50 (streaming).
**Generator:** `companion/generate_riverstone_sensors.py` · **Seed:** 20241 + machine number · **Output:** default `companion/sensors/machine_readings_week.csv` (10,080 rows, one machine, one week); `--full` writes `machine_readings_full.parquet` (12 machines × 40 weeks = 4,838,400 rows, ~5M as the blueprint asks). The one-week file is exactly machine M01's first week of the full run.
**Tested:** Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (18 Sep 2026). The full run takes a few minutes and needs pyarrow.

## Columns
timestamp (one-minute) · machine_id (M01–M12) · temperature_c · pressure_bar · cycle_seconds · status (running / stopped)

## Planted structure
Barrel temperature around 215 °C (+2 °C per machine number step), a ±1.5% day-shift warm-up cycle, a slow drift of +0.02 °C per day, and AR(1) noise (coefficient 0.8, sd 0.6). Pressure ≈ 118 bar + 0.15 × temperature deviation + noise 1.5; cycle time ≈ 18.5 s + 0.03 × temperature deviation + noise 0.25.
**Every week, every machine:** one heater fault (temperature ramps +12 °C over 50 minutes, then decays over 40), one pressure spike (3 readings, +25–40 bar), one stoppage (20–60 minutes; status stopped, pressure 0, cycle NaN). Sensor glitches: 0.2% of temperature readings missing.

## Week-one facts used in Chapter 40 (M01)
Stoppage Wed 22:02–22:33 (32 min) · heater fault peaks Wed 22:53 at 225.2 °C; z-score there only +2.8 (rolling 2-hour z-score misses it); slow-baseline rule (24-hour median, > 6 °C for 10 minutes) fires Wed 22:51 · pressure spikes Tue 12:00–12:02 · 18 missing temperature readings.

## Consistency
Machine IDs M01–M12 are new (the teaching databases don't model machines). New Riverstone fact for the coordinator: 12 injection-moulding machines logging one-minute sensor data from March 2025.


---

# Data spec: Riverstone support tickets (`riverstone-tickets`)

**Built by:** Part IV (first used in Chapter 41). **Delivers the Chapter 1 / Chapter 35 promise:** unstructured text, first used by Chapter 41.
**Generator:** `companion/generate_riverstone_tickets.py` · **Seed:** 20241 · **Output:** `companion/tickets/tickets.csv` (3,000 rows) · **Runs in:** under 1 s
**Tested:** Python 3.12.3, NumPy 2.4.4, pandas 3.0.2 (18 Sep 2026)

## What it represents
Free-text customer support tickets, January 2024 to December 2025. Grain: one row per ticket.

## Columns
ticket_id (700001+) · created_at · customer_name · subject · body (free text, 73–230 characters) · topic (Delivery 892, Product Defect 625, Billing 560, General Enquiry 514, Order Change 409) · sentiment (frustrated 988, neutral 1467, positive 545) · order_id · resolution_hours (gamma-distributed, faster for frustrated tickets) · satisfaction_score (1–5, correlated with sentiment).

## How it was built, and its known limitation
Each (topic, sentiment) pair draws from 1–3 hand-written sentence templates with random products/order numbers/amounts substituted in, occasional "Dear team," openers, "kindly do the needful" closers, and light random typos (letter drops, double spaces) on ~40% of tickets. 40 tickets are deliberately mixed (two issues in one message) to give classifiers and topic models something genuinely ambiguous.

**This makes topic and sentiment classification score far above what real support text would achieve** (accuracy above 99%, against a realistic 80s–low 90s), because a handful of templates per category is nearly a vocabulary fingerprint. Chapter 41 states this explicitly in section 41.1 and returns to it whenever a score is quoted. Anyone reusing this dataset for a different chapter should repeat that caveat rather than quote the accuracy as a benchmark.

## Consistency
Products drawn from the standard catalog; customer names from a fixed list of 10, reused across tickets (not linked to real accounts). Order IDs are random integers in the CRM's numbering range but don't join to `riverstone-crm` (no shared generation). New Riverstone fact for the coordinator: a support inbox with topic/sentiment tagging exists, run day to day by a support lead named in Chapter 41's story (Priya Menon).
