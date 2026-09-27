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
