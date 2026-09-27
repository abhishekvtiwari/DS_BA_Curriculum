# Data spec: Chapter 42 recommender assets (`riverstone-recommenders`)

**Built by:** Part IV (first used in Chapter 42). No new order data: reuses `riverstone-baskets` (Ch 38) and `riverstone-accounts` (Ch 37) directly.
**New file:** `companion/ch42/products_text.py` — adds a hand-written one-sentence `description` column to each of the 24 products in `../baskets/products.csv`, for content-based filtering and cold-start demonstrations. Not seeded/randomized; the 24 descriptions are fixed text, written once.

## Why no new dataset
Chapter 42 is entirely built from data already in the project: the account-by-product interaction matrix comes from `baskets/order_lines.csv` (33,931 orders, 4,516 accounts, 24 products), segments and other account attributes come from `accounts/accounts.csv`, and the TF-IDF/cosine-similarity machinery is Chapter 41's, unchanged.

## Headline numbers (leave-one-out evaluation, precision@5 / NDCG@5, seed 42)
Popularity 61.4% / 0.428 · Item-based CF 67.6% / 0.510 · SVD 4 factors 66.2% / 0.490, 12 factors 49.0% / 0.329 (more factors overfits a 24-item catalog) · ALS 8 factors 69.8% / 0.489 (best), 16 factors 46.6% / 0.348 · Content-based 54.0% / 0.367 · 50/50 hybrid 65.4% / 0.460 · Segment-level popularity (exercise 8) 71.9% / 0.534 — beats every method above on this small catalog.

## Consistency
`products_text.py` must be imported before `products.csv` is used for content-based work in this chapter; it does not modify `baskets/products.csv` itself. Any later chapter reusing product descriptions should import from this file rather than duplicating the text.
