# ADR-021: PO-intake pipeline operating mode

**Status:** Accepted
**Date:** (Part VI, Chapter 58)
**Owner:** Automation team

## Context
A full pilot of straight-through PO-intake processing (email to ERP with no human step) was
measured at 88% of orders loading automatically — but of those auto-loaded orders, 19% were
silently wrong (10 of 53), each costing roughly Rs 2,000 in credit notes, re-delivery, and a
customer call to fix.

## Decision
Operate the pipeline in assisted mode: the model drafts an order, a person confirms it
(roughly 45 seconds per order) before it writes to the ERP. Fully automate only the segments
measured at 100% accuracy (bulleted, forwarded, and terse-style emails — 62% of volume).

## Alternatives considered
1. **Straight-through for all emails** — rejected: the 19% silent-error rate makes this more
   expensive than manual entry once error costs are included, not less.
2. **Manual entry, unchanged** — rejected: costs roughly 3x assisted mode per order with no
   accuracy benefit over the confirmed-draft approach.
3. **Straight-through only after a downstream confirmation loop is built** — deferred, not
   rejected: revisit once such a loop exists (see "Revisit when").

## Consequences
**Positive:** assisted mode's measured cost (~Rs 198/order) beats both alternatives; the
100%-accurate segments run fully automated today with no added risk.
**Negative / costs:** a human reviewer remains in the loop for 38% of volume, which is a
real, ongoing operating cost and a queue that has not yet been load-tested at higher volumes
(see Chapter 60's open risks).

## Revisit when
Extraction accuracy on prose-and-table-style emails improves to a silent-error rate around 2%,
or a reliable downstream confirmation mechanism (e.g., an automatic match against the original
email) is built and measured.
