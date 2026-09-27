# Chapter 70 practice data

A 6-row order-lines table, used throughout this chapter's formula and Power Query questions.
Verified by loading into LibreOffice Calc headless and forcing recalculation (18 Sep 2026);
every result quoted in the chapter comes from that run, not hand arithmetic alone.

| order_id | customer | product | category | quantity | unit_price | discount_pct | order_date | net_revenue |
|---|---|---|---|---|---|---|---|---|
| 1001 | Sharma Hardware | Storage Crate 50L | Storage | 3 | 320 | 5 | 2025-01-05 | 912 |
| 1002 | Metro Mart | Food Container 2L | Kitchen | 10 | 85 | 0 | 2025-01-06 | 850 |
| 1003 | Sharma Hardware | Crate Lid 50L | Storage | 4 | 90 | 5 | 2025-01-12 | 342 |
| 1004 | Coastal Foods | Industrial Crate | Industrial | 5 | 980 | 10 | 2025-01-08 | 4410 |
| 1005 | Metro Mart | Chopping Board | Kitchen | 2 | 260 | 0 | 2025-01-09 | 520 |
| 1006 | Sharma Hardware | Storage Crate 50L | Storage | 2 | 320 | 0 | 2025-02-02 | 640 |

`net_revenue = quantity * unit_price * (1 - discount_pct/100)`. Total: 7,674.

Verified results (LibreOffice Calc, headless recalculation):
- `SUMIFS(net_revenue, customer, "Sharma Hardware")` = 1,894
- `COUNTIFS(category, "Storage", quantity, ">=3")` = 2
- `INDEX(unit_price_range, MATCH("Crate Lid 50L", product_range, 0))` = 90
- `AVERAGEIFS(net_revenue, category, "Storage")` = 631.33
- `SUMPRODUCT(quantity, unit_price, (1 - discount_pct/100))` = 7,674 (reconciles to `SUM(net_revenue)`)
- `IF(net_revenue>1000,"Large",IF(net_revenue>500,"Medium","Small"))` on row 2 (850) = "Medium"
- `TEXT(order_date, "MMMM")` on 2025-01-06 = "January"
