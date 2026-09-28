# Analyst to Architect — Chapter 24 worked example

**To:** Vikram Singh, Sales Manager
**Cc:** Anita Rao, Sales Head
**From:** Meera Iyer, Analytics
**Date:** 9 January 2026
**Re:** Why did December revenue fall from November?

## Bottom line
December's ₹8.73 crore is 44.1% below November's ₹15.60 crore, but this is the
expected post-festive fall, not a new problem: two-thirds of it came from smaller orders,
one-third from fewer customers and orders, and the segment mix did not shift. No corrective
action is needed.

## What we found
- Revenue fell ₹6.87 crore, from ₹15.60 crore (November) to ₹8.73 crore (December).
- Decomposed into its three drivers: customers contributed −₹1.26 crore, orders per
  customer −₹1.06 crore, and average order value −₹4.55 crore — AOV drove 66% of the fall.
- Segment mix was essentially unchanged (Retail 50.5% → 52.0% of orders, Wholesale 22.0% → 21.1%,
  Hospitality 27.5% → 26.8%), so this is not a shift toward smaller-spending segments.
- The shape mirrors the May-to-June dip earlier in the year (−40.4%), which was also led by
  smaller orders with the mix unchanged.
- December fell from November in every year of the data: by 42.2% in 2023,
  43.1% in 2024 and 44.1% in 2025.

## Why
Riverstone's festive season (October–November) pulls forward large bulk and gifting orders;
December's order book reverts to routine reordering: mostly smaller orders (two-thirds of the
fall), with somewhat fewer customers and orders (one-third). Both of this year's dips (May→June
and Nov→Dec) have the same shape: led by smaller orders, with the segment mix unchanged. That
repeated shape is evidence of seasonality rather than a customer or competitive problem, though
the causes differ (the June trough; the post-festive fall in December).

## What we recommend
No corrective action for December itself. For planning: build the 2026 monthly revenue plan
around this seasonal shape rather than a flat run rate (one month's revenue repeated for every
month), so December is never compared against November as if they should look similar.

## What could change this
If January 2026 also comes in well below its usual range, the seasonal explanation would be
wrong and this should be reopened.

## Appendix
Data: `companion/full/` order lines, non-cancelled, November and December 2025 (and the same
months of 2023 and 2024 for the year-on-year check). Method: chain-linked (sequential)
decomposition of Revenue = Customers × Orders/Customer × AOV (Chapter 23, section 23.11).
Every number above is computed from the order data, not typed.
