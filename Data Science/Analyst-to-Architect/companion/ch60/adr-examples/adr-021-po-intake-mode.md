# ADR-021: PO-intake pipeline operating mode

**Status:** Accepted
**Date:** before the pilot went live on real email (Chapter 58)
**Owner:** Automation team

## Context
Chapter 58 measured the pipeline on 60 practice emails. Run straight through (email to ERP
with no person in between), it would load 88% of orders on its own, but 19% of those
auto-loaded orders were silently wrong (10 of 53): a wrong quantity, a missing line. A wrong
order costs roughly ₹2,000 to put right (credit note, re-delivery, a customer call). Nobody at
Riverstone had measured either the coordinator's typing error rate or how many errors a
reviewer catches, and the comparison between typing and assisted intake depends on both.

## Decision
Operate the pipeline in assisted mode: it drafts every order, and a person confirms each draft
before anything is written to the ERP. Orders over ₹1,00,000 also wait for approval. Start with
a shadow stage (the pipeline drafts, writes nothing, and its drafts are compared with what the
coordinator typed) to measure the typing error rate and the review catch rate.

## Alternatives considered
1. **Straight through for all emails** — rejected: at a 19% silent error rate it costs far more
   than typing once the cost of wrong orders is counted (Chapter 58, section 58.7).
2. **Typing, unchanged** — rejected, but narrowly: if typing were error-free it would be
   cheaper than assisted intake, which wins on cost only if reviewers catch over 97% of errors
   or typing gets more than 1.2% of orders wrong (Chapter 58, section 58.7). That is why the
   shadow stage measures both numbers before the decision is revisited.
3. **Auto-load a proven segment** (bulleted, forwarded and terse emails: 62% of the volume,
   0 errors in 37 so far) — deferred, not rejected: 0 in 37 still allows a true error rate of
   up to about 8% (the rule of three), so the segment must first pass on a fresh fortnight of
   real email.

## Consequences
**Positive:** no unreviewed order reaches the ERP; most silent errors become caught ones; the
coordinator stays in the loop and notices when the model starts behaving oddly.
**Negative / costs:** a person reviews every draft (about forty drafts in forty minutes a
day), and the exception queue has not yet been load-tested at higher volumes (see the design
document's risks).

## Revisit when
The shadow stage has measured the typing error rate and the review catch rate; or the proven
segment passes on fresh email; or a downstream confirmation (for example, an email to the
customer listing the lines) is built and measured.
