# ADR-026: CRM write method, system-of-record rule, and retry policy

**Status:** Accepted
**Date:** the week after the container diagram was drawn (Chapter 60's story)
**Owner:** Automation team

## Context
Chapter 51's incident: a "customer segment" sync, built by a different contractor, used HTTP
PUT to update CRM customer records. PUT replaces the entire record, so it silently erased a
negotiated discount field the sync was never meant to touch. The fixes (PATCH only, a named
system of record per field, reconciliation after every sync) were recorded in a small internal
document, which newer jobs were never checked against. When the container diagram was drawn,
two jobs wrote to the CRM (the lead-score sync and the segment sync) with different retry logic.

## Decision
All writes to the CRM use PATCH (partial update) exclusively, naming only the fields the sync
owns. Every synced field has one named system of record: the one place allowed to be the
source of truth for that field (a negotiated discount belongs to the CRM and is never written
by a pipeline). Every sync uses the same retry policy: retry only transient failures (HTTP 429,
503, timeouts, dropped connections), with the same idempotency key on every attempt, and alert
a person after the last retry fails.

## Alternatives considered
1. **Keep PUT, be more careful about including all fields in every request** — rejected:
   relies on every future developer remembering to do this correctly, forever; the same
   mistake will recur.
2. **Read-then-write (read the full record, modify one field, PUT it back)** — rejected:
   introduces a race condition if anything else updates the record between the read and
   the write; PATCH avoids this by construction.
3. **Leave the rule in the internal document** — rejected: nobody checks new jobs against a
   document that isn't part of the design.

## Consequences
**Positive:** a sync can never silently overwrite fields it wasn't meant to touch; the
system-of-record table makes it unambiguous which system wins on any disagreement; both syncs
fail and recover the same way.
**Negative / costs:** requires the CRM's API to support PATCH correctly for every field type;
the system-of-record table needs an owner and must be kept current as new synced fields are
added.

## Revisit when
A new field needs to be synced and doesn't yet have a stated system of record — the table
must be updated as part of adding that field, not after an incident reveals the gap.
