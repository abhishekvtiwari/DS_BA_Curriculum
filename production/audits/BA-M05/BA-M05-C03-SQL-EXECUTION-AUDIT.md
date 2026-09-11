# BA-05-C03 SQL execution audit

**Runtime:** Python sqlite3 / SQLite 3.42.0
**Fixture:** synthetic, non-personal training data created in memory
**Transaction:** read-only SELECT examples after fixture creation

## E01 - Projection, aliasing, and deterministic ordering

Query SHA-256: `efce38e41c5f02708811f4e103760540366e1943681b8d96e2d65c36a3becb33`

| order_id | order_date | booked_amount |
|---|---|---|
| 101 | 2026-01-03 | 120 |
| 102 | 2026-01-12 | 40 |
| 103 | 2026-01-15 | 200 |
| 104 | 2026-02-02 | NULL |

## E02 - Filter a half-open reporting period with explicit NULL handling

Query SHA-256: `89f35df04e04112abc13eb737e7029e737d36ac76f8095308325f087cb46ffc2`

| order_id | status | total_amount |
|---|---|---|
| 105 | paid | 80 |
| 106 | paid | 60 |
| 107 | NULL | 150 |

## E03 - Preserve the customer population with a LEFT JOIN

Query SHA-256: `80349679836f37ffc508556344004f6f260a24ad2bd6ec295c02f81a34c942d6`

| customer_id | customer_name | order_count |
|---|---|---|
| 1 | Aster Stores | 2 |
| 2 | Beacon Labs | 2 |
| 3 | Cedar Works | 2 |
| 4 | Delta Retail | 1 |
| 5 | Elm Services | 0 |

## E04 - Aggregate paid revenue at region grain

Query SHA-256: `d8defa8418da7a8a1de55f75bf4a31d3a882564e85ec8f8500222f5027e3d7d6`

| region | paid_orders | paid_revenue |
|---|---|---|
| North | 2 | 200 |
| South | 1 | 200 |
| Unknown | 1 | 90 |

## E05 - Decompose customer revenue with CTEs

Query SHA-256: `b99aa34917c4392ba1b1a6eb264e00e3e28399278f3318c7c463ee8dc9d66220`

| customer_name | revenue |
|---|---|
| Beacon Labs | 200 |
| Aster Stores | 120 |
| Delta Retail | 90 |
| Cedar Works | 80 |

## E06 - Rank orders and calculate a running customer total

Query SHA-256: `22a7280349e950161adef3504b77431d3a1d437b872cc4a0b5aabaf3a73c7a82`

| customer_id | order_id | total_amount | amount_rank | running_amount |
|---|---|---|---|---|
| 1 | 101 | 120 | 1 | 120 |
| 1 | 102 | 40 | 2 | 160 |
| 2 | 103 | 200 | 1 | 200 |
| 3 | 105 | 80 | 2 | 80 |
| 3 | 107 | 150 | 1 | 230 |

## E07 - Find duplicate normalized email keys

Query SHA-256: `4a833f2dad257f24ed822b2814f6aba9261145859a00e9ac50e4a35ef6a3c54e`

| normalized_email | row_count |
|---|---|
| ana@example.test | 2 |

## E08 - Find orphan foreign keys

Query SHA-256: `2b0ffd678b0cc3e79cad0b8d1964cb03811360643483b4ae575a2de66751efc1`

| order_id | customer_id |
|---|---|
| 106 | 99 |

## E09 - Profile missing and invalid domain values

Query SHA-256: `5a917f1b50deeba60622ffb6559c99d1ddf5868e9904260dc5e7649619a0b17a`

| missing_email | invalid_country | total_rows |
|---|---|---|
| 1 | 1 | 6 |

## E10 - Reconcile joined paid revenue to the source population

Query SHA-256: `1c843e59997958fc72b11c0c5e347ae221f88e52774bb470f60d0eaca544faa3`

| source_paid | matched_paid | unmatched_paid |
|---|---|---|
| 550 | 490 | 60 |
