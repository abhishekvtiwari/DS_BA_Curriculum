# DS_BA_Curriculum

Controlled Data Science and Business Analyst encyclopedia blueprints with AI-authoring prompts, module contracts, practical projects, assessments, audits, governance, and GitHub-ready production workflows.

## Controlled Data Science and Business Analyst Pathway Blueprint

This repository is a controlled AI-authoring specification and operational production layer. It defines what an AI authoring system is allowed to write and how work is resumed, audited, and released. It intentionally keeps the pathway outlines separate from later chapter prose.

## Repository contents

- `data-science/`: 18-module Data Science outline with 96 chapters and 661 topic/subtopic control points.
- `business-analyst/`: 16-module Business Analyst outline with 75 chapters and 529 topic/subtopic control points.
- `contracts/`: one explicit JSON contract for every module across 34 controlled modules.
- `production/`: fixed output directories for drafts, labs, assignments, assessments, audits, checkpoints, and releases.
- `prompts/`: controlled prompts for orchestration, chapter writing, labs, assessments, audits, and checkpoints.
- `schemas/`: JSON schemas and examples for checkpoints and assessment items.
- `indexes/`: master index, glossary register, and cross-reference register.
- `governance/`: rules, issue register, change log, and version metadata.
- `templates/`: word/page budget and release-record templates.

## Controlled hierarchy

```text
Pathway → Module → Chapter → Topic → Subtopic → Lesson → Lab → Assignment → Assessment
```

## Production sequence

```text
Blueprint → module contract → approval → chapter batch → labs → assignments
→ PRE_ASSESSMENT_AUDIT → revision → assessment bank → ASSESSMENT_VALIDATION
→ revision → FINAL_RELEASE_AUDIT → release record → module release
```

Assessments are deliberately generated **after** the pre-assessment content audit and are validated before the final release audit. This resolves the former circular dependency.

## Naming convention

- Blueprint: `data-science/00-data-science-blueprint.md`
- Contract: `contracts/data-science/DS-M01-contract.json`
- Chapter draft: `production/drafts/DS-M01/DS-M01-C01.md`
- Lab: `production/labs/DS-M01/DS-M01-LAB-01.md`
- Assignment: `production/assignments/DS-M01/DS-M01-ASSIGN-01.md`
- Assessment bank: `production/assessments/DS-M01/DS-M01-assessment.jsonl`
- Audit: `production/audits/DS-M01/DS-M01-PRE_ASSESSMENT_AUDIT.md`
- Release audit: `production/audits/DS-M01/DS-M01-FINAL_RELEASE_AUDIT.md`
- Release record: `production/release/DS-M01/DS-M01-release.md`
- Checkpoint: `production/checkpoints/RUN-YYYYMMDD-TASK-TRACK.json`

## Resumability

Every production run must write a checkpoint conforming to `schemas/checkpoint.schema.json`. A new run reads the latest valid checkpoint, verifies the referenced files exist, and continues from `next_action`. Never infer completion from filenames alone.

## Encoding and portability

All files are UTF-8 without a BOM. For older Windows PowerShell environments, use `Get-Content -Encoding UTF8` or a modern editor. Do not alter punctuation or IDs during conversion.
