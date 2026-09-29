# ADR-002: Orchestrator for scheduled data pipelines

**Status:** Accepted
**Date:** when the Daily Sales Flash pipeline moved from cron to Dagster (Chapter 46)
**Owner:** Data platform team

## Context
Riverstone's daily sales flash and supporting pipelines had outgrown a single cron-scheduled
script (Chapter 20, section 20.7). Failures were invisible until someone checked email; there was no shared
view of what had run, what had failed, or what depended on what.

## Decision
Adopt Dagster as the orchestrator for all scheduled data pipelines.

## Alternatives considered
1. **Stay with cron + custom logging** — rejected: no dependency graph, no built-in retry or
   backfill support, failures require manually reading log files.
2. **Apache Airflow** (Chapter 46, section 46.8) — rejected for this team's first orchestrator: heavier operational
   footprint (a scheduler, webserver, and metadata database to run), and its DAG-of-tasks model
   is a less natural fit than Dagster's asset-based model for a small team thinking in terms of
   "which tables get produced," not "which tasks run."
3. **A managed workflow service (cloud-vendor specific)** — rejected: ties pipeline logic to
   one cloud provider before the cloud provider decision (ADR-007) was even final.

## Consequences
**Positive:** dependency graphs, retries, backfills, and a single place to see run history;
asset-based model matches how the team already thinks about tables.
**Negative / costs:** a new tool for the team to learn and operate; Dagster-specific concepts
(assets, jobs, sensors) that don't transfer directly to Airflow, which many candidates and
contractors already know.

## Revisit when
The team grows past the point where Dagster's simpler operational model is the limiting factor,
or if company-wide standardization on Airflow is mandated from above.
