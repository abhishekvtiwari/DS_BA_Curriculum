# Chapter 16 — expected values for every measure

Built from the full Riverstone dataset (`companion/full/`, `riverstone_full`), checked in PostgreSQL 16.15 and
MySQL 8.0.46 while writing. Run `ch16_checks_postgresql.sql` (or `ch16_checks_mysql.sql`) to reproduce every line.
Riverstone Supplies is fictional; every name and number is invented.

## Company totals

| Measure | Filter | Expected |
|---|---|---|
| Net Revenue | none (2023–2025) | ₹2,663,490,235 |
| Net Revenue | Year = 2025 | ₹1,146,641,651 |
| Net Revenue | Year = 2024 | ₹903,015,475 |
| Net Revenue | Year = 2023 | ₹613,833,108 |
| Orders | 2025 | 46,356 |
| Customers | 2025 | 4,599 |
| Average Order Value | 2025 | ₹24,735.56 |
| Gross Margin % | 2025 | 27.5% |
| Target | 2025 | ₹1,166,950,000 |
| % of Target | 2025 | 98.3% |
| Gap to Target | 2025 | −₹20,308,349 |
| Revenue LY | 2025 | ₹903,015,475 |
| YoY Growth % | 2025 | +27.0% |
| Revenue YTD | 30 June 2025 | ₹499,203,925 |
| Revenue YTD LY | 30 June 2025 | ₹379,844,027 |
| Revenue no rep | 2025 | ₹33,630,135 (2.9% of the year) |
| Cancelled orders (excluded) | 2025 | ₹49,241,854 across 1,956 orders |
| Fact rows vs orders | 2025 | 83,444 lines, 46,356 orders |

## By quarter (Net Revenue and YoY Growth %)

| Quarter | 2025 | 2024 | YoY |
|---|---|---|---|
| Q1 | ₹264,787,166 | ₹200,889,263 | +31.8% |
| Q2 | ₹234,416,760 | ₹178,954,764 | +31.0% |
| Q3 | ₹223,564,918 | ₹175,230,767 | +27.6% |
| Q4 | ₹423,872,808 | ₹347,940,682 | +21.8% |

Q4 2025 also: 13,777 orders · 4,220 customers · AOV ₹30,766.70 · gross margin 27.6% · target ₹447,500,000 · 94.7% of target · gap −₹23,627,192.

## By region (2025)

| Region | Net Revenue | Customers |
|---|---|---|
| West | ₹383,840,549 | 1,506 |
| South | ₹318,624,642 | 1,289 |
| North | ₹279,250,231 | 1,127 |
| East | ₹142,256,284 | 586 |
| Region missing (no city) | ₹22,669,946 | 91 |

Q4 2025 by region: West ₹142,688,728 · South ₹117,726,527 · North ₹102,966,828 · East ₹52,120,934 · Region missing ₹8,369,792.

Row-level security tests: Pooja Desai (West + East) ₹526,096,833 and 2,092 customers · Arjun Nair (South) ₹318,624,642 and 1,289 · Sandeep Gill (North) ₹279,250,231 and 1,127 · no role ₹1,146,641,651 and 4,599.

## By segment (2025)

| Segment | 2025 | 2024 | YoY |
|---|---|---|---|
| Retail | ₹556,436,454 | ₹443,810,189 | +25.4% |
| Wholesale | ₹312,728,493 | ₹238,457,929 | +31.1% |
| Hospitality | ₹277,476,705 | ₹220,747,358 | +25.7% |

## By product (2025)

| Product | Net Revenue | Share |
|---|---|---|
| Storage Box 25L | ₹231,104,138 | 20.2% |
| Food Container Set | ₹214,380,655 | 18.7% |
| Storage Box 10L | ₹196,381,989 | 17.1% |
| Industrial Crate | ₹152,683,090 | 13.3% |

## Other checks

- October 2025: ₹180,620,103 (October 2024: ₹147,221,566, +22.7%).
- Top rep 2025: Rahul Mehta ₹167,315,885, then Simran Kaur ₹135,665,049 and Tarun Bose ₹127,930,306.
- Biggest single customer, 2025: about ₹10.7 lakh.
- Financial year to 31 December 2025 (FY2026, April–March): ₹881,854,486.
- Date table: 1,096 rows, 1 January 2023 to 31 December 2025.
- Model row counts: Sales 209,006 · Orders 116,194 · Customers 5,027 · Products 8 · Employees 16 · Targets 36.
