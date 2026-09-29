# Failure analysis: the Riverstone Analytics & AI Platform (full version)

Companion to Chapter 61, section 61.7. One paragraph of reasoning per container,
expanding the chapter's failure-analysis table.

## Ingestion (Dagster)
**Weakest link:** a single scheduler, and it has to stay single: two copies
would each run the 6:30 schedule and send the Flash twice (Chapter 52, section
52.3). **What breaks:** if the scheduler process dies, no new pipeline runs are
triggered, but nothing already loaded is lost or corrupted — the warehouse
simply stops receiving fresh data until the scheduler restarts. **Degrades:**
pipelines pause; last-good data remains fully readable. Retries and alerts
(Chapter 46) handle transient failures within a run; there's no automatic
failover to a standby scheduler today (a candidate future investment, sized
against how often the scheduler itself has actually failed, not against how bad
it sounds in the abstract).

## Warehouse (DuckDB file + Delta archive)
**Weakest link:** the warehouse is one DuckDB file on one machine (Chapter 45),
with the sensor archive as a Delta table in object storage (Chapter 49).
**What breaks:** every container that reads or writes warehouse data fails at
once — this is a genuine, full-platform outage, not a degraded state. Chapter
52's story is the proof: one deleted network rule cut the pipeline off from the
database, and the dashboard and the Flash both stopped. **Degrades:** it
doesn't — this is the platform's one true single point of failure, and the
finding that justifies making the warehouse redundant (a second copy that can
take over, and a way for the copies to agree which one is in charge: section
61.5's quorum and consensus) ahead of any other reliability investment on this
list.

## Semantic layer
**Weakest link:** none of its own — it keeps no data, and is recomputed from
warehouse data on a schedule. **What breaks:** if a recompute run fails, the
layer simply serves the last successful computation until the next run
succeeds. **Degrades:** gracefully — stale but clearly timestamped numbers,
never wrong numbers.

## BI & Flash (Power BI, email)
**Weakest link:** the BI service itself, and separately, the email path for the
Flash. **What breaks:** dashboards become unreachable, or the Flash is delayed.
**Degrades:** gracefully — the Flash is sent only after its checks pass and is
retried by the orchestrator (Chapter 46), so a delayed send is late, not
silently dropped, and BI outages are the vendor's, recoverable without any
Riverstone-side data loss.

## Defect model service
**Weakest link:** currently a single FastAPI instance (Chapter 56). **What
breaks:** if it goes down, line alerts stop. **Degrades:** by documented
fallback — Chapter 56's runbook (section 56.10) switches the line to manual
inspection until the service is restored. Load balancing across more than one
copy (section 61.5) is a natural next investment once a second plant or higher
line speed makes a single instance a real bottleneck rather than a hypothetical
one.

## Support assistant (RAG)
**Weakest link:** the document index it retrieves from. **What breaks:** if the
index is unavailable or a question finds nothing above the confidence floor, the
assistant refuses to answer rather than guessing (Chapter 55, ADR-023).
**Degrades:** by design — this is graceful degradation done correctly: the
feature that can't be trusted turns itself off cleanly rather than staying up
and being confidently wrong. There's no partition and no copy involved, so this
is not a CAP choice.

## PO-intake pipeline
**Weakest link:** two links — the CRM, where the Decide stage looks up each
customer's credit-hold flag, and the ERP, for the final write. **What breaks:**
new orders can't be checked or written while either link is down.
**Degrades:** by design — orders are held in the exception queue rather than
written blind (a Policy exception, Chapter 58, section 58.6; this chapter's
story), choosing consistency over availability (CP) because a wrong order costs
about ₹2,000 to unwind (Chapter 58), far more than a short delay. The retry is
safe because the write is idempotent: one email, one order.

## Reverse-ETL syncs
**Weakest link:** the CRM's API. **What breaks:** lead scores and account flags
fall behind. **Degrades:** gracefully, and by design — this container accepts
eventual consistency (sections 61.2 and 61.4): a failed write stays unsynced,
the next run sends it again with its idempotency key, and the reconciliation
check (Chapter 51, section 51.7) confirms it landed. A multi-hour CRM outage
costs nothing beyond a delayed sync, exactly as observed in this chapter's
story.

## Summary

One genuine single point of failure (the warehouse); one deliberate CAP choice
favoring consistency (PO-intake) and one favoring availability (the reverse-ETL
sync); one graceful-degradation choice (the assistant's refusal); the rest
degrade gracefully by construction. The prioritized fix this analysis supports:
warehouse redundancy first, load balancing for the defect model second (as
scale demands it), and a recurring chaos-test schedule to keep confirming that
"degrades gracefully" claims remain true as the platform changes.
