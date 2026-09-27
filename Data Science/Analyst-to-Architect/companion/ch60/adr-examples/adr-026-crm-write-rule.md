# ADR-026: CRM write method and system-of-record rule

**Status:** Accepted
**Date:** (Part VI, Chapter 51)
**Owner:** Automation team

## Context
An earlier reverse-ETL sync (built by a different contractor) used HTTP PUT to update CRM
lead records, which replaces the entire record rather than the specific field intended. This
silently erased a negotiated discount field that the sync wasn't even meant to touch.

## Decision
All writes to the CRM use PATCH (partial update) exclusively, and every synced field has one
named system of record — the one place allowed to be the source of truth for that field.

## Alternatives considered
1. **Keep PUT, be more careful about including all fields in every request** — rejected:
   relies on every future developer remembering to do this correctly, forever; the same
   mistake will recur.
2. **Read-then-write (read the full record, modify one field, PUT it back)** — rejected:
   introduces a race condition if anything else updates the record between the read and
   the write; PATCH avoids this by construction.

## Consequences
**Positive:** a sync can never silently overwrite fields it wasn't meant to touch; the
system-of-record table makes it unambiguous which system wins on any future disagreement.
**Negative / costs:** requires the CRM's API to support PATCH semantics correctly for every
field type (verified during this migration); the system-of-record table itself needs an owner
and needs to be kept current as new synced fields are added.

## Revisit when
A new field needs to be synced and doesn't yet have a stated system of record — the table
must be updated as part of adding that field, not after an incident reveals the gap.
