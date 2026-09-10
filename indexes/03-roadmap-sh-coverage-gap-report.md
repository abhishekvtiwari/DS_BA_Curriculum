# roadmap.sh Coverage-Gap Report

**Report ID:** REF-AUDIT-20260910-01  
**Phase:** Phase 0 — scope and planning  
**Status:** REVIEW_REQUIRED  
**Reviewed on:** 2026-09-10  
**Scope:** Controlled Data Science (`DS`) and Business Analyst (`BA`) blueprints  
**Authority:** Advisory comparison only; this report does not approve new curriculum scope.

## Purpose

Compare the controlled curriculum against four roadmap.sh learning paths supplied by the repository owner. The roadmaps are external coverage references, not replacements for the approved blueprints, contracts, or stable IDs.

## External references

| Reference | Intended comparison | URL |
|---|---|---|
| Machine Learning AI Tutor | Machine-learning sequence and terminology | https://roadmap.sh/ai/roadmap-chat/machine-learning |
| AI and Data Scientist | End-to-end Data Science pathway | https://roadmap.sh/ai-data-scientist |
| Data Analyst | Shared analytical foundations and tools | https://roadmap.sh/data-analyst |
| BI Analyst | Business-intelligence specialization | https://roadmap.sh/bi-analyst |
| AI and Data Scientist PDF | Static roadmap details used where the interactive page is dynamic | https://roadmap.sh/pdfs/roadmaps/ai-data-scientist.pdf |
| Data Analyst PDF | Static roadmap details used where the interactive page is dynamic | https://roadmap.sh/pdfs/roadmaps/data-analyst.pdf |

External content is time-sensitive. Recheck the live sources before approving any proposed scope change.

## Executive finding

The controlled Data Science blueprint is materially broader than the core AI/Data Scientist and Data Analyst roadmaps. It already includes mathematics, statistics, Python, SQL, data wrangling, EDA, visualization, classical machine learning, deep learning, forecasting, NLP, computer vision, generative AI, agents, deployment, cloud, MLOps, distributed systems, responsible AI, and portfolio work.

The Business Analyst blueprint strongly covers business analysis and the analytical workflow, including Excel, Power Query, DAX, SQL, Python, Tableau, Power BI, Looker Studio, statistics, KPIs, experiments, requirements, processes, stakeholders, strategy, change, risk, and governance. Its largest benchmark gap is depth in dedicated BI architecture and operations.

No new module is justified solely by this comparison. Candidate additions should first be evaluated for placement inside existing modules and approved as new subtopic IDs only when existing IDs cannot cover them honestly.

## Data Science comparison

| Benchmark area | Controlled coverage | Finding | Candidate action |
|---|---|---|---|
| Mathematics and statistics | `DS-M06` | Strong coverage of algebra, calculus, optimization, probability, estimation, testing, regression, Bayesian reasoning, and experimental foundations | Retain current structure |
| Econometrics and advanced online experimentation | Partial across `DS-M06` and `DS-M10` | Econometrics, ratio-metric inference, CUPED/CUPAC, and sensitivity-improvement methods are not explicit | Review as advanced optional subtopics; do not add automatically |
| Python and SQL | `DS-M03` through `DS-M05` | Strong and deeper than the benchmark | Retain current structure |
| R ecosystem | Not explicit | roadmap.sh presents Python or R; the controlled pathway intentionally centers Python | Decide whether R is an elective; it is not a core gap if Python remains the declared language |
| Collection and acquisition | `DS-M03`, `DS-M05`, and `DS-M07` | Files, APIs, databases, and validation are represented; web scraping is not explicit | Consider a constrained acquisition subtopic with legal, robots.txt, privacy, and rate-limit controls |
| Wrangling, EDA, and visualization | `DS-M04` and `DS-M07` | Strong coverage | Retain current structure |
| Classical machine learning | `DS-M08` and `DS-M09` | Strong coverage of workflow, supervised and unsupervised learning, evaluation, tuning, and interpretation | Retain current structure |
| Deep learning, NLP, vision, and transformers | `DS-M11` through `DS-M13` | Stronger than the benchmark | Retain current structure |
| MLOps and deployment | `DS-M15` | Good model packaging, serving, cloud, Docker, CI/CD, monitoring, and operations coverage | Review explicit Kubernetes, orchestration, infrastructure-as-code, feature-store, and experiment-tracking coverage |
| Distributed data systems | `DS-M16` | Hadoop, Spark, streaming concepts, and lakehouse systems are covered | Review whether Kafka and Flink need explicit advanced coverage |
| AutoML | Not explicit | External skills guidance treats AutoML as useful, not foundational | Consider as optional advanced coverage under model selection and governance |
| Portfolio and communication | `DS-M18` and `DS-07-C05` | Strong guided projects, capstones, leadership, and executive communication | Retain; ensure released projects include reproducible READMEs and evidence |

## Business Analyst, Data Analyst, and BI comparison

| Benchmark area | Controlled coverage | Finding | Candidate action |
|---|---|---|---|
| Business questions and stakeholder context | `BA-M01`, `BA-M02`, `BA-M06`, `BA-M14` | Stronger than the Data Analyst benchmark | Retain current structure |
| Data literacy and quality | `BA-05-C01` | Strong foundations in grain, keys, missingness, duplicates, definitions, and lineage | Retain current structure |
| Excel analytics | `BA-05-C02` | Excel formulas, pivots, charts, Power Query, Power Pivot, DAX basics, and quality checks are covered | Retain; depth belongs in phase-level content rather than new scope unless audit proves otherwise |
| SQL and Python | `BA-05-C03` and `BA-05-C04` | Strong analyst-oriented coverage | Retain current structure |
| Visualization and dashboarding | `BA-05-C05` | Tableau, Power BI, Looker Studio, KPI cards, dashboards, storytelling, and governance are covered | Retain current structure |
| Statistics, regression, experiments, and decisions | `BA-M06` | Strong conceptual coverage | Retain; advanced statistical modelling should remain proportional to the BA role |
| Dimensional modelling | Not explicit | Star schema, snowflake schema, facts, dimensions, slowly changing dimensions, and conformed dimensions are not named | High-priority BI depth review |
| Semantic and analytical models | Partial through DAX and dashboards | Measures, calculation layers, semantic models, relationship direction, and model governance are not explicit | High-priority BI depth review |
| Data warehousing and OLAP | Partial through systems and analytics topics | Warehouse architecture, marts, OLAP operations, and refresh patterns are not explicit | Review for placement in `BA-M05` or `BA-M11` |
| BI security and administration | General security and governance exist | Row-level security, workspace governance, gateways, refresh credentials, deployment pipelines, and audit logs are not explicit | High-priority practical/governance review |
| BI performance and operations | Not explicit | Model size, query performance, refresh reliability, capacity, usage monitoring, and lifecycle operations are not named | Review as advanced BI operational coverage |
| Data acquisition | General APIs, data, and system integration are covered | Web extraction and ingestion patterns are not explicit | Add only if required for the target analyst role |
| Portfolio and career evidence | Distributed across professional-practice and project topics | The blueprint has relevant ingredients but should require demonstrable analytical artifacts during production | Enforce through project rubrics rather than new theory scope |

## Priority decisions

### Priority 1 — review for controlled inclusion

1. BI dimensional modelling and semantic models.
2. BI security, refresh, deployment, monitoring, and performance.
3. Modern MLOps orchestration: Kubernetes, infrastructure as code, feature stores, and experiment tracking.

### Priority 2 — evaluate as advanced or optional

1. Econometrics and advanced online-experiment sensitivity methods.
2. Kafka and Flink as named distributed-streaming technologies.
3. AutoML governance and limitations.
4. Safe and lawful web-data acquisition.

### Explicitly optional unless the pathway objective changes

1. R, dplyr, and ggplot2 as a parallel analytics stack.
2. Tool-by-tool duplication where an existing concept is already vendor-neutral.
3. Deep learning for the Business Analyst pathway.

## Scope-control decision

- Do not create new modules from this report.
- Do not copy roadmap.sh headings into the blueprints verbatim.
- Do not introduce vendor features without a durable underlying concept and a dated official reference.
- Do not treat roadmap popularity as evidence of required curriculum scope.
- Any approved addition must receive a stable ID, contract update, index/count update, change-log entry, and checkpoint record.

## Review questions

1. Is the Data Science pathway Python-first, or must it support a full R alternative?
2. Is the Business Analyst pathway intended to qualify learners for dedicated BI Analyst roles?
3. Should modern MLOps platform operations be core or an advanced elective?
4. What depth of data engineering belongs in a Data Science pathway rather than a separate Data Engineering pathway?

## Current disposition

`REVIEW_REQUIRED`: the comparison is complete, but no candidate gap is approved curriculum scope.

