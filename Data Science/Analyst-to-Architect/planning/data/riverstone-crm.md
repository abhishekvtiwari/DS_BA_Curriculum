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
