# Chapter 16 — expected values for every measure

Built from the full Riverstone dataset (`companion/full/`, `riverstone_full`), checked in PostgreSQL 16.15 and
MySQL 8.0.46 while writing. Run `ch16_checks_postgresql.sql` (or `ch16_checks_mysql.sql`) to reproduce every line.
Riverstone Supplies is fictional; every name and number is invented.

## Company totals

| Measure | Filter | Expected |
|---|---|---|
| Net Revenue | none (2023–2025) | ₹2,66,34,90,235 |
| Net Revenue | Year = 2025 | ₹1,14,66,41,651 |
| Net Revenue | Year = 2024 | ₹90,30,15,475 |
| Net Revenue | Year = 2023 | ₹61,38,33,108 |
| Orders | 2025 | 46,356 |
| Customers | 2025 | 4,599 |
| Average Order Value | 2025 | ₹24,735.56 |
| Product Cost | 2025 | ₹83,18,03,000 |
| Gross Margin | 2025 | ₹31,48,38,651 |
| Gross Margin % | 2025 | 27.5% |
| Target | 2025 | ₹1,16,69,50,000 |
| % of Target | 2025 | 98.3% |
| Gap to Target | 2025 | −₹2,03,08,349 |
| Revenue LY | 2025 | ₹90,30,15,475 |
| YoY Growth % | 2025 | +27.0% |
| Revenue YTD | 30 June 2025 | ₹49,92,03,925 |
| Revenue YTD LY | 30 June 2025 | ₹37,98,44,027 |
| Revenue no rep | 2025 | ₹3,36,30,135 (2.9% of the year) |
| Cancelled orders (excluded) | 2025 | ₹4,92,41,854 across 1,956 orders |
| Fact rows vs orders | 2025 | 83,444 lines, 46,356 orders |
| Avg Customer Revenue | 2025 | ₹2,49,324.13 |
| Retail Revenue (every Segment row) | 2025 | ₹55,64,36,454 |
| Retail Only (KEEPFILTERS) | 2025 | Retail row ₹55,64,36,454 other rows blank |
| All-Customer Revenue (every Segment row) | 2025 | ₹1,14,66,41,651 |
| Share of Selection (Storage Box 25L and 10L ticked) | 2025 | 54.1% and 45.9% |
| Overview Title | Year = 2025 | Riverstone sales — 2025 — ₹114.7 cr at 98.3% of target |
| Overview Title | no year | Riverstone sales — all years — ₹266.3 cr at 99.2% of target |
| Last Refreshed (data date) | any | Data to 28 Dec 2025 |

## By quarter (Net Revenue and YoY Growth %)

| Quarter | 2025 | 2024 | YoY |
|---|---|---|---|
| Q1 | ₹26,47,87,166 | ₹20,08,89,263 | +31.8% |
| Q2 | ₹23,44,16,760 | ₹17,89,54,764 | +31.0% |
| Q3 | ₹22,35,64,918 | ₹17,52,30,767 | +27.6% |
| Q4 | ₹42,38,72,808 | ₹34,79,40,682 | +21.8% |

Q4 2025 also: 13,777 orders · 4,220 customers · AOV ₹30,766.70 · gross margin 27.6% · target ₹44,75,00,000 · 94.7% of target · gap −₹2,36,27,192.

## By region (2025)

| Region | Net Revenue | Customers |
|---|---|---|
| West | ₹38,38,40,549 | 1,506 |
| South | ₹31,86,24,642 | 1,289 |
| North | ₹27,92,50,231 | 1,127 |
| East | ₹14,22,56,284 | 586 |
| City missing (no city) | ₹2,26,69,946 | 91 |

Q4 2025 by region: West ₹14,26,88,728 · South ₹11,77,26,527 · North ₹10,29,66,828 · East ₹5,21,20,934 · City missing ₹83,69,792.

Row-level security tests: Pooja Desai (West + East) ₹52,60,96,833 and 2,092 customers · Arjun Nair (South) ₹31,86,24,642 and 1,289 · Sandeep Gill (North) ₹27,92,50,231 and 1,127 · All regions role (Anita Rao) ₹1,14,66,41,651 and 4,599. A Viewer in no role sees nothing.

## By segment (2025)

| Segment | 2025 | 2024 | YoY |
|---|---|---|---|
| Retail | ₹55,64,36,454 | ₹44,38,10,189 | +25.4% |
| Wholesale | ₹31,27,28,493 | ₹23,84,57,929 | +31.1% |
| Hospitality | ₹27,74,76,705 | ₹22,07,47,358 | +25.7% |

## By product (2025)

| Product | Net Revenue | Share |
|---|---|---|
| Storage Box 25L | ₹23,11,04,138 | 20.2% |
| Food Container Set | ₹21,43,80,655 | 18.7% |
| Storage Box 10L | ₹19,63,81,989 | 17.1% |
| Industrial Crate | ₹15,26,83,090 | 13.3% |

## Other checks

- October 2025: ₹18,06,20,103 (October 2024: ₹14,72,21,566 +22.7%).
- Top rep 2025: Rahul Mehta ₹16,73,15,885 then Simran Kaur ₹13,56,65,049 and Tarun Bose ₹12,79,30,306.
- Biggest single customer, 2025 (Top Customer): Galaxy Logistics Patna, ₹10,73,806.50 (0.34% of Wholesale, the Share of Segment value).
- Financial year to 31 December 2025 (FY2026, April–March): ₹88,18,54,486.
- Date table: 1,096 rows, 1 January 2023 to 31 December 2025.
- Model row counts: Sales 200,381 (the `sales_lines` view: 209,006 source lines less the cancelled ones) · Customer 5,027 · Product 8 · Employee 16 · Targets 36 · Date 1,096.
- Customer by Region (all records, after the merge with `city_region.csv`): West 1,660 · South 1,400 · North 1,224 · East 643 · City missing 100.
- Customers by segment (section 16.0, `customers.csv`): Hospitality 1,513 · Retail 2,791 · Wholesale 723 · total 5,027.

## Month matrix, January–June 2025 (section 16.6)

| Month | Net Revenue | Revenue YTD | Revenue LY | Revenue YTD LY | YoY Growth % | Revenue 3M Rolling |
|---|---|---|---|---|---|---|
| Jan | ₹8,51,95,521 | ₹8,51,95,521 | ₹6,40,63,515 | ₹6,40,63,515 | 33.0% | ₹28,59,14,637 |
| Feb | ₹7,85,82,579 | ₹16,37,78,100 | ₹5,86,32,364 | ₹12,26,95,879 | 34.0% | ₹23,66,00,651 |
| Mar | ₹10,10,09,066 | ₹26,47,87,166 | ₹7,81,93,384 | ₹20,08,89,263 | 29.2% | ₹26,47,87,166 |
| Apr | ₹9,51,94,709 | ₹35,99,81,875 | ₹7,25,34,870 | ₹27,34,24,133 | 31.2% | ₹27,47,86,355 |
| May | ₹8,72,49,568 | ₹44,72,31,443 | ₹6,68,88,391 | ₹34,03,12,524 | 30.4% | ₹28,34,53,343 |
| Jun | ₹5,19,72,483 | ₹49,92,03,925 | ₹3,95,31,504 | ₹37,98,44,027 | 31.5% | ₹23,44,16,760 |
