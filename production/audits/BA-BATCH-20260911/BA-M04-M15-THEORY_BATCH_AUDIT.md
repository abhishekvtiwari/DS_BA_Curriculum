# BA-M04 through BA-M15 - Theory Batch Audit

**Audit ID:** BA-BATCH-20260911-THEORY
**Scope:** 53 Phase 1 theory chapters, BA-M04 through BA-M15 (commits `1ea6c0c`, `a1f7abc`, `cfdee9a`)
**Method:** Measurement of the controlled Markdown source, contracts, checkpoints and rendered PDFs
**Result:** `REJECTED - TEMPLATE_ARTIFACT - REBUILD_REQUIRED`
**Issue:** `ISS-009`
**Date:** 2026-09-11

## Finding

The batch is not a set of substantive theory drafts. It is one fixed skeleton filled by topic-name
substitution. Rebuilding is required; proofreading cannot repair it.

## Measured evidence

| Measure | BA-M01-M03 | BA-M04-M15 |
|---|---:|---:|
| Chapters | 17 | 53 |
| Words | 74,693 | 76,282 |
| Topic-specific share of words | - | **~9%** (6,879) |
| Exact-duplicate body paragraphs | 1.2% | **39.6%** |
| Duplicates after collapsing name substitution | 1.2% | **53.5%** |
| Code blocks | 36 | **0** |
| Worked example / scenario mentions | 24 | **1** |
| Non-audit table rows | 206 | **0** |
| Inline citations | - | **0** |

- 364 topic sections share **52** "Analysis and application" templates; one template serves **222** of them.
- 364 "Concept" paragraphs close on **38** distinct sentences; the top two cover **328**.
- `BA-M15-C01.md` and `BA-M12-C02.md` place every heading on identical line numbers 1-160.
- Chapter line counts cluster on exactly 150 / 165 / 180.
- Delivery against the "approximately 10,000 words" allocation stated in every chapter header: **11-18%**.

## Voided certifications

All 364 topic rows were marked `COVERED` and every chapter stamped `SELF_AUDIT_PASSED`, with zero
exceptions and zero gap markers across 53 chapters. The audit verified heading presence only and never
inspected content, so it certified template output as complete. All stamps in scope are now
`SELF_AUDIT_VOIDED` and all topic rows are `UNVERIFIED`. See `ISS-010`.

## Defects carried into the rebuild backlog (`ISS-011`)

1. `BA-M08 - Business Intelligence and Reporting` cited 15 times; the module's contract title is
   **Lean, Six Sigma, and Quality**. `BA-M05` appears under two different titles.
2. 15 lowercase acronym and proper-noun defects rendered into shipped PDFs
   (`Integrated uat model`, `Integrated sql for analysts model`, `theory for bpmn`).
3. `https://stats.oecd.org/glossary/` returns **404** and is cited in all 5 BA-M06 chapters with a
   stated access date of 2026-09-11. The date is false. 37 other cited URLs resolve or are bot-blocked.
4. `BA-15-C01-T02` defines "assessment" as educational assessment inside a Risk and Controls chapter.
   31 further single-word topic labels are reused across chapters and are exposed to the same collision.
5. Tracker word counts are not reproducible by any documented rule (BA-M15-C01 claimed 1,393; measured
   1,232-1,475 depending on rule).
6. All 70 PDFs carry `(unspecified)` in `/Creator` and `/Subject`, use unembedded base-14 fonts, and
   split the ID scheme between filename `BA-M15-C03` and document ID `BA-15-C03`.

## Out of scope and unchanged

BA-M01 and BA-M02 remain the quality benchmark and were not modified. BA-M03 remains parked under
`ISS-005` with 46 of 95 contracted topics undrafted.
