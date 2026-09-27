# Part Brief — Part VI — Production ML, Generative AI & MLOps

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-6-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 53–59**.

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P6-53 | 53 | Deep Learning in Depth | B | 5,500 | Not started | `manuscript/ch53-deep-learning-in-depth.md` |
| P6-54 | 54 | Generative AI & Large Language Models | B | 5,500 | Not started | `manuscript/ch54-generative-ai-and-large-language-models.md` |
| P6-55 | 55 | Building AI Applications: RAG, Agents & Evaluation | B | 5,500 | Not started | `manuscript/ch55-building-ai-applications-rag-agents-and-evaluation.md` |
| P6-56 | 56 | MLOps: Making Models Survive Production | B | 5,000 | Not started | `manuscript/ch56-mlops-making-models-survive-production.md` |
| P6-57 | 57 | LLMOps | B | 4,000 | Not started | `manuscript/ch57-llmops.md` |
| P6-58 | 58 | Intelligent Automation: AI Inside Business Workflows | B | 4,500 | Not started | `manuscript/ch58-intelligent-automation-ai-inside-business-workflows.md` |
| P6-59 | 59 | Industry Case Studies | C | 4,500 | Not started | `manuscript/ch59-industry-case-studies.md` |

## Reference chapters for this part

Chapter 13 (class B), Chapter 2 (APIs and local demos).

## Guidance specific to this part

- **The fastest-changing part of the book.** Verify every model name, library API, pricing statement, and platform feature against official sources at the time of writing, record the date, and write so the concepts outlive the tools. Avoid naming specific model versions unless essential.
- **LLM calls:** don't require paid API keys to follow the examples. Use small open models that run locally where feasible, or recorded responses and local mock servers clearly labeled; never present an unrun response as real output.
- **Chapter 58 (Intelligent Automation)** must deliver the purchase-order intake project promised by Chapter 1 and Chapter 2: extracting fields from emails and PDFs, validating against Riverstone's product and customer master, and routing low-confidence cases to a person. Build sample PO emails and PDFs in the automation sandbox domain.
- **Chapter 55 (RAG):** the Riverstone product-support assistant uses a documents dataset (manuals, policies, FAQ) that this part builds and registers.
- **Responsible AI** points to Chapter 64 for governance.

## Sequencing and dependencies

Start after Part IV Chapters 36–39 are written.

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

**Ch 53. Deep Learning in Depth** · EXPANDED from draft Ch 24 · 5,500 words
Kept architectures; added training techniques (normalization, dropout, schedulers), **quantization and model compression** (fixes the draft's broken reference from LLMOps), computer vision for manufacturing defect detection, transformers explained step by step with a toy attention calculation.

**Ch 54. Generative AI & Large Language Models** · EXPANDED from draft Ch 25 (part) · 5,500 words
How LLMs are built and trained · tokens, context windows, sampling · prompting techniques with examples · embeddings · fine-tuning and parameter-efficient methods · multimodal models · limits and risks. (Model and vendor landscape verified at time of writing.)

**Ch 55. Building AI Applications: RAG, Agents & Evaluation** · NEW (splits draft Ch 25) · 5,500 words
RAG end to end: chunking, embeddings, vector search, reranking, grounding, citations · tool use and agents · evaluating AI applications (golden sets, LLM-as-judge, human review) · guardrails · a Riverstone product-support assistant built step by step.

**Ch 56. MLOps: Making Models Survive Production** · EXPANDED from draft Ch 26 · 5,000 words
Added full examples: MLflow tracking, model registry, FastAPI serving, Docker, drift detection computed, retraining triggers, feature stores.

**Ch 57. LLMOps** · EXPANDED from draft Ch 27 · 4,000 words
Kept components; added prompt versioning and regression tests, tracing, cost per request calculated, routing and caching examples, security (prompt injection) examples.

**Ch 58. Intelligent Automation: AI Inside Business Workflows** · NEW · 4,500 words
Where AI fits in a process: classify, extract, summarize, decide, act · processing documents and emails (purchase orders, invoices, customer requests) with extraction plus validation against master data · AI-written commentary for automated reports, checked against the numbers before sending · agents that take actions across systems: permissions, approval steps, and limits · human-in-the-loop design and confidence thresholds · measuring accuracy, time saved, and the cost of errors · failure modes (a wrong value written into the ERP) and guardrails · cost per automated transaction.
*Project:* Automated purchase-order intake: read incoming PO emails and PDFs, extract fields with an LLM, validate them against Riverstone's product and customer master, create draft orders in the sandbox system, and route low-confidence cases to a person.

**Ch 59. Industry Case Studies** · NEW · 4,500 words
Nine end-to-end cases, each showing problem → data → approach → architecture → results → lessons: manufacturing quality, demand planning, B2B lead scoring, retail pricing, banking fraud, logistics routing, customer support automation, predictive maintenance, end-to-end order-to-cash reporting and automation.

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 55

- *(from Ch 1)* | Unstructured | emails, PDFs, images, audio, free-text reviews | Chapters 41, 55, and 58 |

#### Chapter 58

- *(from Ch 1)* Turning that unstructured message into a structured order automatically is a classic automation project, and you'll build one in Chapter 58.
- *(from Ch 2)* (When it doesn't, Chapter 58 shows how AI tools can extract tables from documents, with checks.)

## Kickoff prompt

```
You are writing Part VI — Production ML, Generative AI & MLOps of the book "Analyst to Architect" (Chapters 53–59).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-6-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-6-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```
