# Lambda vs. Kappa vs. hybrid: the full worked comparison

Companion to Chapter 62, section 62.2. Scenario: Taloja's plant sensors need to
power both an instant line alert and a historical warehouse table.

## Lambda architecture

**How it works:** a batch layer reprocesses all sensor data periodically (in
Riverstone's case, this would be a nightly Dagster run reading the full day's
readings into the warehouse). A separate speed layer processes new readings
as they arrive, writing to a fast, low-latency store for immediate alerting.
A merge/serving layer reconciles the two views for anyone querying "current"
state.

**Cost:** the alerting logic (what counts as a defect-worthy reading) has to
be implemented once in the speed layer's fast path and again in the batch
layer's thorough pass — two implementations of the same business rule, which
can and do drift apart over time as one is updated without the other.

**Where it's still the right call:** when the speed layer's approximate
answer genuinely needs later correction by a slower, more thorough batch pass
— for example, financial reconciliation where an initial fast estimate is
routinely superseded by an end-of-day authoritative recompute.

## Kappa architecture

**How it works:** every sensor reading is written to one durable, replayable
stream. Historical reprocessing means replaying the stream from the
beginning (or from a checkpoint) through the same processing logic used for
new data — no separate batch code path.

**Cost:** needs real streaming infrastructure (a broker that retains history
and supports replay — Chapter 50's territory) operated to a standard where
replay is fast and reliable enough to actually use for reprocessing, not just
a theoretical capability.

**Where it's still the right call:** when the fast-path and slow-path
consumers of the data genuinely want the same guarantees and the same
processing logic — most modern streaming-first companies default here for
exactly this reason.

## What Riverstone actually built: a deliberate hybrid

**How it works:** the defect-model FastAPI service scores each image the
instant it arrives, raising a line alert directly, with no dependency on the
warehouse or any batch process. The same event is logged asynchronously into
the ordinary Dagster-orchestrated batch ingestion path, landing in the
warehouse on the normal schedule, for monitoring, drift analysis (Chapter 56),
and historical reporting.

**Why neither textbook pattern fit:** the line alert's consumer (a QC
operator on the floor) needs a response in well under 50ms and has zero use
for historical reprocessing. The warehouse's consumers (monitoring dashboards,
retraining pipelines) need completeness and historical depth and have zero
use for sub-second latency. Forcing both through one unified Kappa stream
would mean either compromising the alert's speed to fit the stream's overall
guarantees, or building special-cased fast-path logic inside the "unified"
stream anyway — at which point it's not really unified. Forcing both through
a Lambda merge step would add a reconciliation cost neither consumer actually
needs, since the two paths never need to agree with each other in the first
place — they're answering genuinely different questions on genuinely
different timescales.

**The general lesson:** Lambda and Kappa are both answers to "how do I keep
one shared view consistent across fast and slow paths." When your fast-path
and slow-path consumers don't need a shared view at all — because they're
different questions, not different speeds of the same question — building
the honest, deliberately separate hybrid is the better-engineered choice,
not a compromise.
