# Design Document: Riverstone Analytics & AI Platform

**Status:** Living document. **Owner:** Data Platform team (Meera Iyer). **First version:** the January
described in Chapter 60's story, when Meera drew the container diagram.
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

**In scope:** ingestion from the ERP, CRM, dispatch files and plant sensors; the warehouse and
semantic layer; the Daily Sales Flash and BI dashboards; the defect-detection model and its
serving infrastructure; the support document assistant; the purchase-order email intake
pipeline; the reverse-ETL syncs back to the CRM.

**Out of scope:** the ERP and CRM themselves (systems of record owned by their vendors and
the sales/operations teams, not this platform); the company website; HR and finance systems
unrelated to sales and operations data.

## 2. Requirements

### 2.1 Functional

- Ingest orders, sensor readings, and CRM records reliably, with reconciliation against source.
- Detect product defects from line-camera images at the Taloja plant, at line speed.
- Answer support and policy questions from current documents only, refusing rather than
  guessing when no document supports an answer.
- Read purchase-order emails, extract structured order data, and write each order to the ERP
  only after a named person has confirmed the draft (assisted mode, Chapter 58).
- Send the Daily Sales Flash by 07:30 IST on working days (Chapter 20).
- Keep CRM lead scores, follow-up flags and segments current, from the warehouse.

### 2.2 Non-functional

The table in Chapter 60, section 60.5, with an owner for each row:

| Requirement | Precise form | Measured how | Owner |
|---|---|---|---|
| Freshness | At the 06:30 run, the newest orders are from the previous working day | Freshness check on every run, before the Flash is built (Chapter 47, section 47.5) | Data platform |
| Pipeline reliability | At most 2 runs a year need a person to step in (99.5% of 365 daily runs would allow 1.8) | Counted monthly from Dagster's run history | Data platform |
| Flash delivery | Sent by 07:30 IST on working days, p95 over the month, and only after its four checks pass (Chapter 20) | From the send time in the run log | Data platform |
| Defect model latency | p95 under 50 ms per image at current line speed | Load test before each model deployment | AI applications |
| Assistant grounding | Refuses when no document's raw retrieval score clears the absolute floor (ADR-023) | Golden-set evaluation, every deploy | AI applications |
| PO-intake accuracy | No order is written to the ERP without a named person confirming it; orders over ₹1,00,000 also need approval | Daily count of ERP writes with no confirmer = 0; weekly sample of 20 confirmed orders checked against their emails | Automation |
| Cost ceiling | Platform cost under ₹0.50 per 1,000 order lines processed | Monthly cost review (Chapter 65 prices it bottom-up) | Data platform |
| Access control | No credential can read another branch's customer or order data | Quarterly access review (pending Chapter 64's model) | Security (to be named) |

## 3. Architecture

### 3.1 Context (C4 level 1)

See Chapter 60, Figure 60.2. The platform is one system among: branch managers and sales/
operations staff (readers of dashboards, recipients of flags, confirmers of PO drafts),
customers (senders of purchase-order and support emails, recipients of answers), the data and
analytics team (builders and operators), the ERP (source of orders, destination of confirmed
PO orders), the CRM (source of leads and segments, destination of lead scores and flags), the
plants (machine sensor readings; the Taloja line camera's images), and the email inbox (source
of purchase orders and support questions).

### 3.2 Containers (C4 level 2)

See Chapter 60, Figure 60.3. Eight containers:

1. **Ingestion (Dagster, Chapter 46)** — the 06:30 run that copies ERP orders, CRM leads, and
   the dispatch and sensor files into the warehouse; the shared entry point for everything the
   platform knows.
2. **Warehouse (Chapters 45, 47, 49)** — raw, staging, and mart tables for orders and customers;
   the sensor archive as a Delta table in object storage (ADR-014).
3. **Semantic layer (Chapter 32, section 32.13)** — dbt models providing one tested definition of
   revenue, active customer, and other shared metrics (Chapter 23's definitions, enforced in code).
4. **BI and Flash (Chapters 16 and 20)** — Power BI dashboards and the Daily Sales Flash email.
5. **Defect model service (Chapters 53 and 56)** — scores line-camera images behind a FastAPI service.
6. **Support assistant (Chapter 55)** — answers questions from Riverstone's policy and spec
   documents with retrieval-augmented generation (RAG).
7. **PO-intake pipeline (Chapter 58)** — the 06:00 weekday run that reads order emails, drafts
   orders for a person to confirm, and writes confirmed orders to the ERP.
8. **Reverse-ETL syncs (Chapter 51)** — write lead scores, follow-up flags and customer segments
   back to the CRM.

Three are AI containers (5, 6, 7) and five are data containers (1, 2, 3, 4, 8). Plus shared
services used by every container: a credential vault, centralized run logs, and
alerting/monitoring (drawn once, in the shared-services band of Figure 60.3).

## 4. Key decisions

Index (five of these are written out in full in `adr-examples/`; ADR-014 is Figure 60.5 in the chapter):

| ADR | Decision |
|---|---|
| ADR-002 | Orchestrator: Dagster |
| ADR-007 | Cloud provider and region: AWS ap-south-1 (Mumbai) |
| ADR-014 | Sensor archive table format: Delta Lake |
| ADR-018 | Data quality: SQL tests inside the pipeline (write–audit–publish), not a dedicated observability platform (yet) |
| ADR-021 | PO-intake operating mode: assisted, not straight-through |
| ADR-023 | Support assistant: refuse on absolute score floors; mark superseded documents at index time |
| ADR-026 | CRM writes: PATCH only, one system of record per field, one retry policy for every sync |

## 5. Data flow: traced examples

### 5.1 A purchase-order email (full trace)

See Chapter 60, section 60.5, for the six-step walkthrough, numbered to match Figure 60.3.
Summary: email arrives → the PO-intake pipeline's 06:00 run drafts the order → a person
confirms it → the order is written to the ERP with the source email as its idempotency key →
the next 06:30 ingestion run copies it into the warehouse → the semantic layer recomputes →
the Flash, the dashboards, and the CRM syncs all read the same updated semantic layer.

### 5.2 A defect detection (for comparison)

The camera captures an image on the line → the defect model service scores it within its 50 ms
budget → a score above the threshold raises an immediate line alert (bypassing the warehouse
entirely, for latency) → the score is also logged to the warehouse afterwards for monitoring and
retraining analysis (Chapter 56's drift tracking).

Notice the deliberate asymmetry: the purchase-order flow goes through a person and the warehouse
before anything downstream acts on it (because correctness matters more than speed here); the
defect-detection flow acts immediately and logs afterward (because a missed real-time alert is
worse than a slightly stale monitoring record). **This is itself an architectural decision worth
its own ADR** — different latency/correctness trade-offs for different containers, made
deliberately rather than by accident.

## 6. Risks and open questions

1. **The PO-intake exception queue has no defined maximum wait time.** Not load-tested against
   festive-season email volume. *Next step: simulate 3 times normal volume using Chapter 58's
   measured review times; define an SLA; add reviewers or an escalation path if it's breached.*
2. **Duplicated model-serving infrastructure.** Partly resolved: in the two months after this
   document's first version, the defect model and the support assistant were consolidated onto
   one shared FastAPI service (Chapter 60's story). *Next step: monitor combined load; a third
   model would need this reassessed.*
3. **No defined access-control model.** The "no credential reads another branch's data"
   requirement is aspirational until Chapter 64's work defines roles and permissions.
   *Next step: pending Chapter 64.*
4. **The PO-intake run and the ingestion run are not formally sequenced.** On a heavy morning the
   06:00 PO-intake run can still be writing orders to the ERP when the 06:30 ingestion run starts
   reading them. *Next step: define and test the rule; candidates are starting ingestion only
   after PO intake reports done, or counting orders by the time they were confirmed.*
5. **The cost ceiling was set top-down and has never been priced bottom-up.** *Next step:
   Chapter 65 adds up what the platform's servers, storage and services actually cost.*

## 7. Change log

- **January (first version):** following the container-diagram exercise described in
  Chapter 60's real-world story.
- **Two months later:** ADR-026 written; model serving consolidated (risk 2).
- **[Future]:** update after Chapter 64's access-control model is defined (risk 3).
- **[Future]:** update after risk 1's load test is complete.
