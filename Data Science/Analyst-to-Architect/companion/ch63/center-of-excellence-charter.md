# Automation Center of Excellence — charter template

Companion to Chapter 63, section 63.8. Riverstone's own charter, established
following the April 2026 audit, as a worked example.

## Purpose
Maintain a true, current inventory of every automation Riverstone depends on;
publish and evolve the standards new automations should follow; offer shared
services that make following those standards the easiest option, not the
hardest; run the inventory review on a fixed schedule rather than once.

## Membership
The data platform team, formalized in this role rather than as an informal
side responsibility. Not a gatekeeper for every change — a resource teams
choose to use because it makes their own work easier and safer.

## Responsibilities
- Maintain `automation-inventory.csv` (or its equivalent), reviewed quarterly.
- Own and evolve the shared services: notification, credential vault, run
  logs, alerting (Chapter 63, section 63.6).
- Publish the handover-note and runbook templates, and the risk-scoring
  method (section 63.2), for any team to use.
- Run the company-wide "what do you depend on weekly?" inventory question
  at least once a year, more often while sprawl is still being discovered.
- Review any automation scoring high-risk (section 63.2) before it goes to
  production, applying the controls appropriate to its actual risk level
  (section 63.9) — not a blanket process for everything.

## What this charter is not
Not a requirement that every spreadsheet formula be reviewed. Not a rule
that only the platform team may build automation. Not a one-time project —
the charter exists as long as the review cadence keeps happening.

## Review cadence
Quarterly inventory review. Annual charter review: does membership, scope,
or the standards themselves need to change as the company grows?
