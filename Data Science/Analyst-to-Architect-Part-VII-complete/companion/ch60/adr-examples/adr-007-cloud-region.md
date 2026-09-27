# ADR-007: Cloud provider and region

**Status:** Accepted
**Date:** 2026-09-19
**Owner:** Data platform team

## Context
Chapter 45 flagged cloud provider as an open decision; it became blocking once Chapter 52's
deployment work needed a concrete target.

## Decision
AWS, region ap-south-1 (Mumbai).

## Alternatives considered
1. **Provider-neutral, decide later** — rejected: Chapter 52's Terraform and IAM examples
   need a real provider to be concrete rather than abstract, and further delay blocks that work.
2. **Azure** — considered given some enterprise customers are Microsoft-heavy, but rejected as
   the primary choice: the team's existing familiarity and available documentation lean AWS.
3. **A non-Indian region on AWS** — rejected: data residency and latency to Riverstone's own
   operations both favor a Mumbai region for primary workloads.

## Consequences
**Positive:** concrete IAM, networking, and Terraform examples; low latency to Indian users
and systems; data resides in India.
**Negative / costs:** single-cloud dependency; region-specific service availability should be
checked before relying on newer AWS services that may launch in other regions first.

## Revisit when
A specific enterprise customer or partnership requires multi-cloud or a different region, or
AWS pricing/availability in ap-south-1 changes materially.
