# Analyst to Architect — Chapter 24 worked example

**To:** Anita Rao, Sales Head   **From:** Meera Iyer, Analytics   **Date:** 8 January 2026
**Re:** Why did December revenue fall from November?

## Bottom line
December's ₹8.73 crore is 44.1% below November's ₹15.60 crore, but this is the expected
post-festive normalisation, not a new problem: order values fell broadly across every
segment, with no drop in active customers or orders per customer beyond the usual seasonal
pattern. No corrective action is needed; December's figure is in line with January and
February's typical range.

## What we found
- Revenue fell ₹6.87 crore, from ₹15.60 crore (November) to ₹8.73 crore (December).
- Decomposed into its three drivers: customers contributed −₹1.26 crore, orders per
  customer −₹1.06 crore, and average order value −₹4.55 crore — AOV drove 66% of the fall.
- Segment mix was essentially unchanged (Retail 50.5% → 52.0% of orders, Wholesale 22.0% →
  21.1%, Hospitality 27.5% → 26.8%), so this is not a shift toward smaller-spending segments.
- The same pattern — a large AOV-led fall — repeated the May-to-June dip earlier in the year
  (−40.4%), which is the known seasonal trough after Q1's stocking cycle.

## Why
Riverstone's festive season (October–November) pulls forward large bulk and gifting orders;
December's order book reverts to routine reordering, which is smaller per order but not
fewer in number. This is the same mechanism in both dips this year, which is itself evidence
it's structural seasonality rather than a customer or competitive problem.

## What we recommend
No corrective action for December itself. For planning: build the FY2026 monthly revenue
plan around this seasonal shape rather than a flat run rate, so December is never compared
against November as if they should look similar.

## What could change this
If January 2026 also comes in well below its typical range, the seasonal explanation would
be wrong and this would need re-opening — the two-month test proposed at the end of this memo.

## Appendix
Data: `companion/full/` order lines, non-cancelled, 1 Jan – 31 Dec 2025. Method: chain-linked
(sequential) decomposition of Revenue = Customers × Orders/Customer × AOV (Chapter 23,
section 23.11). Compared months: November 2025 and December 2025.
