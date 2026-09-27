# Design Document: Riverstone Analytics & AI Platform

**Status:** Living document. **Owner:** Data Platform team (Meera Iyer). **Last updated:** January 2026.
**Companion to:** Analyst to Architect, Chapter 60.

This is the expanded version of the design document walked through in Chapter 60, section
60.5. It follows the same spine — purpose, requirements, architecture, decisions, data flow,
risks — with more detail in each section than the chapter's prose could hold. Use it as a
template for your own design document (the project in Chapter 60 asks you to write one).

---

## 1. Purpose and scope

This document describes the Riverstone Analytics & AI Platform: the combined set of data
pipelines, models, and delivery systems that turn order, sensor, and document data into
reports, alerts, and automated actions across sales, operations, and support.

**In scope:** ingestion from the ERP, CRM, and plant sensors; the warehouse and semantic
layer; the daily sales flash and BI dashboards; the defect-detection model and its serving
infrastructure; the support document assistant; the purchase-order email intake pipeline;
the reverse-ETL sync back to the CRM.

**Out of scope:** the ERP and CRM themselves (systems of record owned by their vendors and
the sales/operations teams, not this platform); the company website; HR and finance systems
unrelated to sales and operations data.

## 2. Requirements

### 2.1 Functional

- Ingest orders, sensor readings, and CRM records reliably, with reconciliation against source.
- Detect product defects from line-camera images, in near-real time, at line speed.
- Answer support and policy questions from current documents only, refusing rather than
  guessing when no document supports an answer.
- Read purchase-order emails, extract structured order data, and write validated orders to
  the ERP with human confirmation for anything below a high-confidence threshold.
- Deliver a daily sales summary to management by 06:10 IST on business days.
- Keep CRM lead scores and account flags current, reflecting the latest order and support data.

### 2.2 Non-functional

See the table in Chapter 60, section 60.5. Reproduced here with additional detail:

| Requirement | Precise form | Measured how | Owner |
|---|---|---|---|
| Freshness | Orders no more than 2 hours stale during business hours (08:00-20:00 IST) | Automated freshness check, hourly | Data platform |
| Pipeline reliability | 99.5% of scheduled Dagster runs succeed without manual intervention | Monthly, from run history | Data platform |
| Flash delivery | Sent within 10 minutes of the 06:00 ERP load finishing, p95 over a rolling 30 days | Automated timestamp comparison | Data platform |
| Defect model latency | p95 under 50ms per image at current line speed (auto-scales if line speed increases) | Load test before each model deployment | AI applications |
| Assistant grounding | Refuses when no document's raw retrieval score clears the absolute floor (ADR-023) | Golden-set evaluation, every deploy | AI applications |
| PO-intake accuracy | No order auto-loads without either a 100%-accurate email style match or human confirmation | Per-style accuracy tracked monthly | Automation |
| Cost ceiling | Platform infrastructure cost under Rs 0.50 per 1,000 order lines processed | Monthly cost review against Chapter 65's model | Data platform |
| Access control | No credential can read another branch's customer or order data | Quarterly access review (pending Ch 64 model) | Security (TBD) |

## 3. Architecture

### 3.1 Context (C4 level 1)

See Chapter 60, Figure 60.2. The platform is one system among: branch managers and sales/
operations staff (readers of dashboards and recipients of flags), customers (senders of
purchase-order and support emails, recipients of answers), the data and analytics team
(builders and operators), the ERP (source and destination of orders), the CRM (source of
leads and segments, destination of scores), plant sensors (source of readings), and email
(source of purchase orders and support questions).

### 3.2 Containers (C4 level 2)

See Chapter 60, Figure 60.3. Eight containers:

1. **Ingestion (Dagster)** — pulls orders, sensor readings, CRM data, and dispatch files on
   schedule; the shared entry point for everything the platform knows.
2. **Warehouse (Postgres + Delta Lake)** — raw, staging, and modelled order and customer
   tables in Postgres; the sensor archive as a Delta table in object storage (ADR-014).
3. **Semantic layer** — dbt-style models providing one agreed definition of revenue, active
   customer, and other shared metrics (Chapter 23's discipline, enforced in code).
4. **BI & Flash (Power BI, email)** — dashboards and the automated daily sales flash.
5. **Defect model service (FastAPI)** — scores line-camera images in near-real time.
6. **Support assistant (RAG)** — answers questions from Riverstone's policy and spec documents.
7. **PO-intake pipeline** — reads order emails, extracts structured data, writes to the ERP.
8. **Reverse-ETL sync** — writes lead scores and account flags back to the CRM.

Plus shared services used by every container: a credential vault, centralized run logs,
and alerting/monitoring (drawn once, in the shared-services band of Figure 60.3).

## 4. Key decisions

Full index (see `adr-examples/` for six of these written out in full):

| ADR | Decision |
|---|---|
| ADR-002 | Orchestrator: Dagster |
| ADR-007 | Cloud provider and region: AWS ap-south-1 |
| ADR-014 | Sensor archive table format: Delta Lake |
| ADR-018 | Quality tooling: SQL tests in CI |
| ADR-021 | PO-intake operating mode: assisted, not straight-through |
| ADR-023 | Support assistant refusal: absolute score floor |
| ADR-026 | CRM writes: PATCH only, one system of record per field |

## 5. Data flow: traced examples

### 5.1 A purchase-order email (full trace)

See Chapter 60, section 60.5 for the six-step walkthrough. Summary: email arrives → PO-intake
pipeline extracts and validates → confirmed order writes to ERP with an idempotency key →
next ingestion cycle picks it up into the warehouse → semantic layer recomputes → flash,
dashboards, and the CRM sync all read the same updated semantic layer.

### 5.2 A defect detection (for comparison)

Camera captures an image on the line → defect model service scores it in under 50ms →
a score above threshold raises an immediate line alert (bypassing the warehouse entirely,
for latency) → the score is also logged asynchronously to the warehouse for later monitoring
and retraining analysis (Chapter 56's drift tracking).

Notice the deliberate asymmetry: the purchase-order flow goes through the warehouse before
anything acts on it (because correctness matters more than speed here); the defect-detection
flow acts immediately and logs afterward (because a missed real-time alert is worse than a
slightly-stale monitoring record). **This is itself an architectural decision worth its own
ADR** — different latency/correctness trade-offs for different containers, made deliberately
rather than by accident.

## 6. Risks and open questions

1. **PO-intake exception queue has no defined maximum wait time.** Not load-tested against
   festive-season email volume. *Next step: simulate 3x normal volume using Chapter 58's
   per-style timing data; define an SLA; add reviewers or an escalation path if it's breached.*
2. **Duplicated model-serving infrastructure** (partially resolved — see Chapter 60's story;
   the defect model and support assistant were consolidated onto one shared FastAPI service
   in Q1 2026). *Next step: monitor combined load; a third model would need this reassessed.*
3. **No defined access-control model.** The "no credential reads another branch's data"
   requirement is aspirational until Chapter 64's work defines roles and permissions.
   *Next step: pending Chapter 64.*
4. **The 06:00 ERP load and the PO-intake pipeline's writes are not yet formally sequenced**
   for the rare case both touch the same order at once. *Next step: define and test the
   collision-handling rule; candidate fix is a short write-lock window around the ERP load.*

## 7. Change log

- **Jan 2026:** Initial version, following the container-diagram exercise described in
  Chapter 60's real-world story.
- **[Future]:** Update after Chapter 64's access-control model is defined (risk 3).
- **[Future]:** Update after risk 1's load test is complete.
