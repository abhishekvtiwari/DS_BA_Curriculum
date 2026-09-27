# Failure analysis: the Riverstone Analytics & AI Platform (full version)

Companion to Chapter 61, Figure 61.4. One paragraph of reasoning per container,
expanding the figure's table.

## Ingestion (Dagster)
**Weakest link:** a single scheduler instance. **What breaks:** if the scheduler
process dies, no new pipeline runs are triggered, but nothing already loaded is
lost or corrupted — the warehouse simply stops receiving fresh data until the
scheduler restarts. **Degrades:** pipelines pause; last-good data remains fully
readable. Retries handle transient failures within a run; there's no automatic
failover to a second scheduler instance today (a candidate future investment,
sized against how often the scheduler itself has actually failed, not against
how bad it sounds in the abstract).

## Warehouse (Postgres + Delta Lake)
**Weakest link:** a single primary database instance. **What breaks:** every
container that reads or writes warehouse data fails simultaneously — this is a
genuine, full-platform outage, not a degraded state. **Degrades:** none — this
is the platform's one true single point of failure, and the finding that
justifies prioritizing warehouse redundancy (read replicas, automated failover)
ahead of any other reliability investment on this list.

## Semantic layer
**Weakest link:** none persistent — it's stateless, recomputed from warehouse
data on schedule. **What breaks:** if a recompute run fails, the layer simply
serves the last successful computation until the next run succeeds. **Degrades:**
gracefully — stale but clearly timestamped numbers, never wrong numbers.

## BI & Flash (Power BI, email)
**Weakest link:** the Power BI service itself, and separately, the SMTP path
for the flash email. **What breaks:** dashboards become unreachable, or the
flash email is delayed. **Degrades:** gracefully — the flash's retry logic
(Chapter 46) means a delayed send is queued, not silently dropped, and BI
outages are the vendor's, recoverable without any Riverstone-side data loss.

## Defect model service
**Weakest link:** currently a single FastAPI instance. **What breaks:** if it
goes down, real-time line alerts stop. **Degrades:** by documented fallback —
QC reverts to manual visual sampling at a known, pre-agreed sampling rate until
the service is restored. Load balancing across multiple instances (section 61.5)
is a natural next investment once a second plant or higher line speed makes a
single instance a real bottleneck rather than a hypothetical one.

## Support assistant (RAG)
**Weakest link:** the document index it retrieves from. **What breaks:** if the
index is unavailable or a query returns nothing above the confidence floor, the
assistant refuses to answer rather than guessing (ADR-023). **Degrades:** by
design — this is graceful degradation done correctly: the feature that can't be
trusted turns itself off cleanly rather than staying up and being confidently
wrong.

## PO-intake pipeline
**Weakest link:** the network link to the CRM (for account-status checks) and
to the ERP (for the final write). **What breaks:** new orders can't be
auto-confirmed or written while either link is down. **Degrades:** by design —
orders queue in the exception list rather than writing blind (ADR-021 and this
chapter's real-world story), choosing consistency over availability because a
wrong order write is measurably more expensive to unwind than a short delay.

## Reverse-ETL sync
**Weakest link:** the CRM's API availability. **What breaks:** lead scores and
account flags fall behind. **Degrades:** gracefully, and by design — this
container explicitly chose eventual consistency (section 61.2), so a multi-hour
CRM outage costs nothing beyond a delayed sync that catches up automatically
once the link returns, exactly as observed in this chapter's real-world story.

## Summary

One genuine single point of failure (the warehouse); two deliberate,
well-justified CAP choices favoring consistency (PO-intake, support assistant
refusal) and one favoring availability (reverse-ETL sync); the rest degrade
gracefully by construction. The prioritized fix this analysis supports:
warehouse redundancy first, load balancing for the defect model second (as
scale demands it), and a recurring chaos-test schedule to keep confirming that
"degrades gracefully" claims remain true as the platform changes.
