# roadmap.sh Coverage-Gap Report

**Report ID:** REF-AUDIT-20260910-01  
**Phase:** Phase 0 — scope and planning  
**Status:** REVIEW_REQUIRED  
**Reviewed on:** 2026-09-10  
**Revised on:** 2026-09-11 — node-level verification of the AI and Data Scientist reference, merged in place  
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

| AI and Data Scientist node graph | Structural re-verification on 2026-09-11 | https://roadmap.sh/api/v1-official-roadmap/ai-data-scientist |

External content is time-sensitive. Recheck the live sources before approving any proposed scope change.

The AI and Data Scientist page is client-rendered and returns no usable structure to a plain fetch; search-result summaries of it are marketing copy. The 2026-09-11 revision therefore read that roadmap from the site's own data endpoint — **130 nodes, 76 labelled, 49 resource links, 10 numbered stages** — and compared it against module **contracts** rather than blueprints. Word-boundary matching was used: an unbounded search for `rag` matches *storage*, *average* and *leverage*, and generic terms such as *pipeline*, *power* and *experiment* inflate apparent coverage. Every surviving match was checked by hand.

## Executive finding

The controlled Data Science blueprint is materially broader than the core AI/Data Scientist and Data Analyst roadmaps. It already includes mathematics, statistics, Python, SQL, data wrangling, EDA, visualization, classical machine learning, deep learning, forecasting, NLP, computer vision, generative AI, agents, deployment, cloud, MLOps, distributed systems, responsible AI, and portfolio work.

The Business Analyst blueprint strongly covers business analysis and the analytical workflow, including Excel, Power Query, DAX, SQL, Python, Tableau, Power BI, Looker Studio, statistics, KPIs, experiments, requirements, processes, stakeholders, strategy, change, risk, and governance. Its largest benchmark gap is depth in dedicated BI architecture and operations.

The 2026-09-11 re-verification confirms the econometrics and CUPED/ratio-metric findings already recorded below; independent measurement reproduces them and contradicts nothing in this report. It also measured the reference's own weighting: **24 of its 49 resource links sit in the stages 1–3 band** (mathematics, statistics, econometrics, experimentation), deep learning carries three, and mathematics, coding and vibe coding are numbered stages with no resources at all. The depth in that band is specific — Booking.com on CUPED, DoorDash on CUPAC, Netflix on stratification, Microsoft on the Delta Method. This is a **product-experimentation** reference, strong on online experimentation and thin elsewhere, which gives the scope-control rule below an evidence basis rather than a stylistic one.

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
| AI-assisted development (Vibe Coding) | Not explicit | Stage 10 of the AI and Data Scientist roadmap — AI coding assistants and AI app builders — has no counterpart in any of the 18 DS contracts. Not present in the 2026-09-10 pass; either new to the roadmap or not reached by the earlier method | Evaluate for placement inside `DS-M14` or `DS-M03` as a candidate subtopic; do not create a module |
| Online experiment placement | `DS-M18` only | A/B testing resolves to `DS-M18` (Projects, Portfolio, and Leadership) and not to `DS-M06` (Statistics, Probability, and Mathematics) | Placement question inside existing scope, not new scope. Review whether controlled experimentation belongs in `DS-M06` beside hypothesis testing, with `DS-M18` retaining the applied project use |

### Node-level coverage, AI and Data Scientist reference, 2026-09-11

Eighteen of the roadmap's twenty-four leaf nodes resolve to existing DS contracts. Three of the remaining six are the econometrics, CUPED/sensitivity and ratio-metric candidates already recorded above under `ISS-003`. One is the Vibe Coding row added above. One is the `DS-M18` placement question. One — calculus and derivatives — resolves to `DS-M06` alone and is recorded as thin rather than missing.

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

### Contract hygiene found during the 2026-09-11 pass

Every BA contract declares `"tools_and_environment": [..., "Python 3.11+"]`, including `BA-M13` (Change Management and Transformation) and `BA-M14` (Strategy, Enterprise Analysis, and Leadership), where Python is implausible. It is boilerplate repeated across all fifteen contracts and had to be discounted by hand during comparison, because it initially made the BA track appear to teach Python in every module. Python is **not** a controlled topic anywhere in `BA`. This is unrelated to any roadmap and is recorded here because it was found here.

### Mapping boundary for the Business Analyst pathway

The AI and Data Scientist roadmap touches only three BA modules — `BA-M05` (SQL, EDA), `BA-M06` (distributions, A/B testing) and `BA-M11` (transformers, prompts). Twelve of fifteen have no counterpart. **Do not map `BA` onto that reference.** Forcing the pathway onto a data-scientist frame would pull it toward modelling and away from the analysis, elicitation and governance work that defines the role. The BA-relevant comparisons are the Data Analyst and BI Analyst roadmaps already covered in this report, and the BI depth findings above remain the open BA question.

## Priority decisions

### Priority 1 — review for controlled inclusion

1. BI dimensional modelling and semantic models.
2. BI security, refresh, deployment, monitoring, and performance.
3. Modern MLOps orchestration: Kubernetes, infrastructure as code, feature stores, and experiment tracking.

### Priority 2 — evaluate as advanced or optional

1. Econometrics and advanced online-experiment sensitivity methods.
2. AI-assisted development: AI coding assistants and AI app builders (added 2026-09-11).
3. Kafka and Flink as named distributed-streaming technologies.
4. AutoML governance and limitations.
5. Safe and lawful web-data acquisition.

### Explicitly optional unless the pathway objective changes

1. R, dplyr, and ggplot2 as a parallel analytics stack.
2. Tool-by-tool duplication where an existing concept is already vendor-neutral.
3. Deep learning for the Business Analyst pathway.

### Placement and hygiene — no new scope required

1. A/B testing placement, `DS-M18` to `DS-M06`.
2. `tools_and_environment` accuracy audit across all 33 contracts.

These two items sit inside approved scope and do not need the Priority 1 approval path.

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

`REVIEW_REQUIRED`: the comparison is complete, but no candidate gap is approved curriculum scope. The 2026-09-11 revision added node-level verification for one of the four references and did not change any curriculum ID, contract, blueprint or count. `ISS-003` continues to govern the econometrics and experimentation candidates it already records.

