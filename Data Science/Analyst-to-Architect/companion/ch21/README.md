# Chapter 21 companion files

## `delivery_times_2025.csv`

One row per delivered 2025 order: 45,040 rows, 8 columns.

| Column | Type | Meaning |
|---|---|---|
| `order_id` | whole number | The order, as in the Riverstone database |
| `order_date` | date (YYYY-MM-DD) | The day the order was placed |
| `branch` | text | The branch that shipped it: Mumbai HO, Bengaluru, Delhi, or Kolkata |
| `customer_id` | whole number | The customer who placed it |
| `order_value` | decimal | The order's net revenue in rupees (quantity × unit price × (1 − discount), summed over its lines) |
| `promised_days` | whole number | The branch's delivery promise: Mumbai HO 5, Bengaluru 5, Delhi 6, Kolkata 7 |
| `delivery_days` | decimal, one place | How many days the delivery took |
| `on_time` | True/False | True when `delivery_days` ≤ `promised_days` |

## Where the numbers come from

The orders, customers, and order values come from the full Riverstone dataset (`companion/full/`): every order with status Delivered and an order date in 2025. The branch is the region of the customer's city (West → Mumbai HO, South → Bengaluru, North → Delhi, East → Kolkata; customers with no city go to Mumbai HO).

Riverstone's ERP has no delivery dates, so **the delivery times are simulated** from this model:

1. **A lognormal delivery time per branch.** Median days: Mumbai HO 3.0, Bengaluru 3.6, Delhi 4.2, Kolkata 5.4. Log-scale spread (sigma): 0.30, 0.32, 0.36, 0.45.
2. **A festive-season delay.** Orders placed in October or November get an extra delay drawn from a gamma distribution (shape 2.0, scale 0.55 days; 1.1 days on average).
3. **Rare failures.** About 1.5% of orders go badly wrong and get a further delay drawn from a gamma distribution (shape 3.0, scale 3.0 days; 9 days on average).
4. The result is rounded to one decimal place, with a minimum of 1 day.

The random seed is fixed (202101), so the file is identical every time it is built. Riverstone Supplies is fictional; every name and number is invented.

## Rebuilding (not needed to follow the chapter)

`build_ch21_files.py` built the CSV file from the full dataset. You never need to run it; it is here so the model above can be checked. From this folder: `python3 build_ch21_files.py` (needs pandas, numpy, and pyarrow).
