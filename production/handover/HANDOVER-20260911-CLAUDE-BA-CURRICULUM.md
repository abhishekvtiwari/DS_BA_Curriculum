# Full-Level Handover to Claude - Business Analyst Curriculum

- **Handover ID:** `HANDOVER-20260911-CLAUDE-BA-CURRICULUM`
- **Prepared:** 2026-09-11
- **Repository:** `C:\Users\jjppl\Desktop\Projects\Encyclopedia`
- **Remote:** `https://github.com/abhishekvtiwari/DS_BA_Curriculum.git`
- **Working branch:** `governance/iss-009-batch-rejection`
- **Recipient:** Claude Code, acting as the independent curriculum reviewer
- **Primary review scope:** BA-M01, BA-M02, and BA-M03 Phase 1 theory
- **Immediate starting point:** BA-M03-C01
**Current authority:** Independent review and correction proposals only; no owner acceptance, Phase 2 work, release, push, or merge is implied.

## 1. Read this before acting

This repository is a controlled curriculum-production system, not a loose collection of Markdown files. Do not infer status from a filename, a generated PDF, a self-audit stamp, or a passing automated gate. Read the controlling sources in this order:

1. `README.md`
2. `Single-Current-Version Authoring Policy (1).md` - currently present locally but untracked; preserve it and do not silently treat it as committed policy
3. `indexes/00-master-index.json`
4. `governance/02-open-issues.md`
5. `governance/05-content-gates.md`
6. The applicable module contract under `contracts/business-analyst/`
7. The latest applicable checkpoint under `production/checkpoints/`
8. The source chapter under `production/drafts/`

If these sources disagree, stop and record the conflict with exact paths and clauses. Do not resolve a material authority conflict by preference.

## 2. Non-negotiable authority boundaries

- The repository is the single authoritative source. PDFs under `output/` are generated review copies and are not authoritative.
- Work chapter by chapter. Do not use one chapter session to silently alter another chapter or another production phase.
- Phase 1 is theory. Phase 2 assessments, labs, assignments, later phases, and release work are not authorized by this handover.
- Do not push, merge, publish, release, or mark owner acceptance.
- Do not approve your own corrections. Claude may produce an independent verdict; final owner acceptance belongs to the user.
- Do not resurrect rejected or quarantined material by copying, paraphrasing, or using it as a quality reference.
- Do not modify the controlled hierarchy, IDs, contract scope, chapter count, topic count, titles, or prerequisites without an explicit owner decision.
- Individual working sources and chapter-wise working PDFs retain module, chapter, and topic codes for review and defect location.
- The final collated learner publication hides internal module, chapter, topic, audit, and production codes.
- Publication typography is fixed: module title 64 pt, chapter title 32 pt, topic title 24 pt, subtopic title 16 pt.
- Similarity gates and word counts are evidence, not semantic approval. Inspect the teaching itself.
- Preserve unrelated and untracked user files. In particular, do not delete, add, rename, or overwrite `Single-Current-Version Authoring Policy (1).md` without an owner instruction.

## 3. Repository state at handover

The working branch contains 18 commits not present on `origin/main`. The most recent relevant commits are:

```text
91ebb35 Complete BA-M03 theory and collated reader
6d540fd Rebuild BA-M03 requirements elicitation
8d32e28 Rebuild BA-M03 requirements concepts
da85642 Standardize publication title hierarchy
0c7d1e4 Record recreated BA-M01 and BA-M02 readers
6feab13 Recreate BA-M02 theory to strict reference standard
56bf5c4 Recreate BA-M01 theory to strict reference standard
34ba8ed Authorize BA-M01 through BA-M03 theory recreation
d60507f Record owner rejection of BA-M05-C03
2a3c8af Reject BA-M04-M15 theory, quarantine BA-M01/M02 assessments, add content gates
53e8d2b Quarantine stale rejected and quarantined PDF exports
```

Nothing has been pushed or merged as part of this work. At handover preparation, the only pre-existing worktree item outside the committed curriculum state was:

```text
?? "Single-Current-Version Authoring Policy (1).md"
```

Recheck branch, status, and history before reviewing because this record is a snapshot, not a substitute for Git:

```powershell
Set-Location 'C:\Users\jjppl\Desktop\Projects\Encyclopedia'
git branch --show-current
git status --short
git log --oneline origin/main..HEAD
```

## 4. Corpus-level status: do not blur these categories

| Scope | Current status | Meaning |
|---|---|---|
| BA-M01 Phase 1 theory | Strict gates passed; independent semantic and owner review pending | Reviewable, not accepted by this handover |
| BA-M02 Phase 1 theory | Strict gates passed; independent semantic and owner review pending | Reviewable, not accepted by this handover |
| BA-M03 Phase 1 theory | Authoring complete; 12/12 strict gates passed; independent semantic and owner review pending | Primary review target |
| BA-M01/M02 Phase 2 assessments | `QUARANTINED` under `ISS-008` | Must not be published, piloted, scored, or used as a model |
| BA-M04-M15 Phase 1 theory | `REJECTED - TEMPLATE_ARTIFACT - REBUILD_REQUIRED` under `ISS-009` | Must be rebuilt; proofreading is insufficient |
| BA-M05-C03 rebuild | Owner rejected | Do not treat it as accepted calibration content |
| Phase 2+ for BA-M01-M03 | Unauthorized | Await independent review and explicit owner authorization |

### Critical evidence that must remain visible

`ISS-008`: all 400 BA-M01/M02 questions follow a fixed `A, B, C, D` answer-key cycle keyed to question number. A learner can score 100% without subject knowledge. The ten banks are quarantined. See `production/audits/BA-BATCH-20260911/BA-M01-M02-ASSESSMENT_INTEGRITY_AUDIT.md`.

`ISS-009`: 53 chapters in BA-M04-M15 were rejected as template artifacts. Only about 9% of 76,282 words was topic-specific; 53.5% of body paragraphs duplicated after topic-name masking; there were no code blocks and effectively no worked examples or content tables. See `production/audits/BA-BATCH-20260911/BA-M04-M15-THEORY_BATCH_AUDIT.md`.

`ISS-010`: heading-presence self-audits were voided and replaced by measurable gates. A passing gate result is necessary but never sufficient for acceptance.

`ISS-011`: corpus-wide cleanup remains open for citations, casing outside rebuilt chapters, dead sources, contextual definitions, count reconciliation, and future PDF metadata.

`ISS-014`: independent and owner review of the BA-M01-M03 recreation remains in progress. It is the controlling acceptance issue for this handover.

## 5. BA-M03 scope and evidence

The controlled contract is `contracts/business-analyst/BA-M03-contract.json`. It defines BA-M03 as **Requirements Engineering**, with 12 chapters and 95 controlled topics. The completed source set contains 61,166 gate-counted words.

| Chapter | Title | Topics | Gate-counted words | Strict gates |
|---|---|---:|---:|---|
| BA-03-C01 | Requirements Concepts | 8 | 6,133 | PASS |
| BA-03-C02 | Requirements Elicitation | 6 | 4,388 | PASS |
| BA-03-C03 | Acceptance and Quality | 6 | 3,663 | PASS |
| BA-03-C04 | Prioritization | 7 | 4,228 | PASS |
| BA-03-C05 | Traceability and Change | 6 | 3,605 | PASS |
| BA-03-C06 | Requirements for Digital Systems | 8 | 4,801 | PASS |
| BA-03-C07 | Requirements Documentation Foundations | 8 | 6,743 | PASS |
| BA-03-C08 | Business Requirements Document (BRD) | 10 | 6,005 | PASS |
| BA-03-C09 | Product Requirements Document (PRD) | 10 | 6,000 | PASS |
| BA-03-C10 | Functional Requirements Document (FRD) | 12 | 7,200 | PASS |
| BA-03-C11 | Documentation Quality, Traceability, and Governance | 8 | 4,800 | PASS |
| BA-03-C12 | Requirements Documentation Projects | 6 | 3,600 | PASS |

The existing automated evidence records:

- 12 of 12 chapters pass all gates under `--strict`.
- 907 substantive body paragraphs were included in a cross-chapter semantic screen.
- Zero paragraph pairs were at or above similarity 0.55 in that screen.
- These measurements do not prove factual correctness, pedagogical quality, sensible sequencing, or freedom from subtler repetition.

Reproduce the controlled gate result:

```powershell
$chapters = Get-ChildItem -LiteralPath 'production/drafts/BA-M03' -Filter 'BA-M03-C*.md' |
  Sort-Object Name |
  Select-Object -ExpandProperty FullName
python tools/content_gates.py --strict @chapters
if ($LASTEXITCODE -ne 0) { throw 'BA-M03 strict gates failed' }
```

Gate expectations are defined in `governance/05-content-gates.md`. For rebuilt and new chapters, blocking and advisory gates both determine success under `--strict`.

## 6. Review artifacts and immutable identity checks

### Learner-facing collated publication

```text
output/pdf/BA-M03/BA-M03-Requirements-Engineering.pdf
Pages: 147
SHA-256: DFA7B294E97C20CE09A7D2B806EDD3517FE636F98F82BD750D8685B0F592C0B1
Internal codes visible: no
Typography: 64 / 32 / 24 / 16 pt
Recorded visual QA: all 147 pages passed
Approval: pending user review
```

### Coded chapter-wise working PDFs

| Chapter | Pages | SHA-256 |
|---|---:|---|
| BA-03-C01 | 16 | `E04688D65FE35E17987D4DC30D9A300FE1548E564EFB334A0F75EA3AC5E9834A` |
| BA-03-C02 | 12 | `07B91EB25CC8F4BB62BF5CA0032C52BE3B083D0A9DAA783BA66BC51363F2FC54` |
| BA-03-C03 | 11 | `8E59D2FCCB34BD1639C4E76DFA378F92BE24BD5AA6CFE7A4CA011CEC94A2FDD3` |
| BA-03-C04 | 12 | `613D84DA887C9A14561569357776E0742AEA1DDF10C2C01594DB9513CA37336D` |
| BA-03-C05 | 11 | `F11DFE1EFFEB6B45CC2F406BB3F808CCA53E8D1E14C56E9E982ED02BF2CFDD9F` |
| BA-03-C06 | 14 | `79DA32698F5F9335F0771622EC581D5557937C215A99ECB31F148E0CCD106E9A` |
| BA-03-C07 | 20 | `0C2B40A31E77C6A135E08D3AB5A99758A00BA4A02F5F6C87C176E7D97805C565` |
| BA-03-C08 | 17 | `EDA6088F330936CEBD1B5FC0D235D7BE0CA6D8385170B7302DD25856037CE627` |
| BA-03-C09 | 17 | `2C211AE9036B7EBDD62DE9323CD1C510F9F0FD9013F711760146AB2223C34404` |
| BA-03-C10 | 21 | `DB23A2335181E079EB52860E1023B20E03F902F4327213D1C22D9EE2D32A0929` |
| BA-03-C11 | 15 | `F2F6A058135FEC48FB8C3B14EDA710256394D0878E1505B02F51F356481E089B` |
| BA-03-C12 | 12 | `A0657D25B97CCDC9747443B1B61B62EBD3FEE4C6F207D6B125C7DDEF5FDE04F0` |

The working PDFs are under `output/pdf/BA-M03/chapters/`. Verify hashes before relying on visual-QA history:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'output/pdf/BA-M03/BA-M03-Requirements-Engineering.pdf'
Get-ChildItem -LiteralPath 'output/pdf/BA-M03/chapters' -Filter '*.pdf' |
  Sort-Object Name |
  Get-FileHash -Algorithm SHA256
```

If a hash differs, treat the PDF as regenerated or altered and repeat visual QA. Never change source merely to match a stale export.

## 7. Claude's full-level independent review assignment

Review BA-M03-C01 through BA-M03-C12 in order, one chapter at a time. Begin with `production/drafts/BA-M03/BA-M03-C01.md`. For each chapter, compare the contract, coded source, coded working PDF, and its position in the code-free collated publication.

The review must go beyond wording and automated gates. Test all of the following:

### Scope and traceability

- Every controlled topic is substantively taught, not merely named.
- Nothing material is introduced outside the contract without a justified cross-reference.
- Topic IDs, headings, source coverage, working-PDF navigation, and contract entries agree.
- BRD, PRD, and FRD are part of BA-M03's Requirements Engineering continuation, not a separate BA-M16.
- The abbreviation is **PRD**, not the transposed **PDR**, except where PDR is explicitly discussed as a different term.

### Technical and professional accuracy

- Definitions distinguish need, requirement, business requirement, stakeholder requirement, functional requirement, non-functional requirement, data requirement, and transition requirement.
- Elicitation methods are chosen by context and acknowledge bias, evidence limits, conflict, and validation.
- Acceptance criteria are measurable and do not collapse into design instructions or test cases.
- Prioritization methods, including MoSCoW, value-effort, cost of delay, and WSJF, are calculated and interpreted correctly.
- Baselines, versioning, traceability, impact analysis, change requests, and scope control preserve decision history.
- Digital-system requirements accurately handle APIs, reports, dashboards, automation, AI, security, privacy, and accessibility.
- BRD, PRD, and FRD have distinct purposes, audiences, ownership boundaries, and levels of detail.
- Cross-document derivation is traceable; information is not duplicated merely to fill templates.
- Examples, formulas, tables, requirement statements, scenarios, and expected outcomes are internally consistent.
- Claims and recommendations are supported by credible sources, and citations actually support the nearby claim.

### Pedagogy and progression

- The text teaches from basic to advanced without assuming unexplained prior knowledge.
- Each topic adds a distinct learning outcome; repeated purpose/value/definition passages are not presented as new content.
- Names and headings are unambiguous. Avoid near-duplicate labels that make learners think the same topic has been repeated.
- Worked examples expose reasoning, inputs, decisions, outputs, failure modes, and corrections.
- Tables teach or compare content; they are not decorative gate-satisfiers.
- C12 projects genuinely integrate earlier knowledge and include realistic evidence, constraints, defects, and decision trade-offs.

### Publication integrity

- Working sources and chapter-wise PDFs retain codes.
- The collated learner PDF contains no module, chapter, topic, audit, checkpoint, or production codes.
- Title hierarchy remains 64 / 32 / 24 / 16 pt.
- No orphan headings, clipped text, blank or suspiciously sparse pages, broken tables, incorrect page order, duplicate sections, or missing chapters.
- The contents page, chapter openings, headings, and page flow use clear, non-confusing names.

### Adversarial checks

- Search for formulaic paragraph skeletons that survive topic-name substitution.
- Compare conceptually adjacent topics for disguised repetition, especially purpose, value, scope, ownership, approval, traceability, and change.
- Look for statements that are plausible but unsupported, oversimplified, jurisdiction-dependent, vendor-dependent, or falsely universal.
- Try to falsify calculations and example conclusions.
- Confirm that citations are real, reachable where practical, appropriately authoritative, and not attached to claims they do not support.
- Distinguish defects in authoritative Markdown from defects introduced only during PDF generation.

## 8. Required finding format

Record every finding in a review artifact under `production/audits/BA-M03/`. Use one row per independently correctable defect:

| Field | Required content |
|---|---|
| Finding ID | Stable ID such as `BA-M03-REV-C01-001` |
| Severity | `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` |
| Location | Exact module, chapter, topic, heading, and source line where possible |
| Evidence | Concise quotation or reproducible observation |
| Why it matters | Learner, correctness, governance, traceability, or publication impact |
| Required correction | Specific outcome, without silently expanding scope |
| Related locations | Any repeated or downstream occurrence |
| Source/PDF scope | Source defect, render defect, or both |
| Status | `OPEN`, `CORRECTED_PENDING_REVIEW`, or `VERIFIED` |

Severity meanings:

- `CRITICAL`: unsafe, materially false, disqualifying integrity failure, corrupted authority, or publication must stop.
- `HIGH`: wrong learning outcome, major omission, invalid method, pervasive repetition, or broken traceability.
- `MEDIUM`: meaningful ambiguity, incomplete explanation, weak example, localized duplication, or citation mismatch.
- `LOW`: editorial or visual defect that does not alter the taught meaning.

For every chapter, issue exactly one reviewer verdict:

- `ACCEPT` - no corrections required.
- `ACCEPT_WITH_CORRECTIONS` - no critical/high defect, but listed corrections must be verified before owner acceptance.
- `REJECT` - critical/high defect or the chapter requires structural rebuilding.

Do not use `PASS`, `SELF_AUDIT_PASSED`, or a gate result as the semantic verdict.

## 9. Required review outputs

Claude should produce:

1. A chapter review file for each reviewed chapter, or one rigorously indexed module review containing all chapter verdicts.
2. A module-level BA-M03 verdict that summarizes defects without erasing chapter-level evidence.
3. A cross-chapter repetition and progression assessment.
4. A citation-verification register identifying checked, unsupported, dead, and provider-dependent sources.
5. A publication-integrity report comparing source, chapter PDFs, and collated PDF.
6. A checkpoint update that states the exact last verified artifact and next authorized action.
7. A concise owner decision list. Do not manufacture an owner decision.

If Claude edits a source after finding a defect, the reviewer who verifies that correction must be independent of the edit. At minimum, separate authoring and verification passes and record both; do not mark a correction verified merely because a gate passes.

## 10. Stop conditions

Stop and report instead of continuing when:

- contract, policy, checkpoint, and source disagree materially;
- a critical defect is found;
- correction would change controlled scope, IDs, hierarchy, prerequisite, module ownership, or publication policy;
- the branch or artifact hashes do not match this handover and the cause cannot be established;
- a source required for a material claim cannot be verified;
- completing the next step would enter Phase 2, rebuild BA-M04+, push, merge, publish, release, or claim owner acceptance.

## 11. Definition of a complete handover review

The independent review is complete only when all 12 BA-M03 chapters have a recorded semantic verdict; cross-chapter repetition, citations, and publication integrity have been assessed; every open finding has an owner-visible status; the checkpoint names the exact next action; and Claude has clearly separated its recommendation from the owner's acceptance decision.

After BA-M03, review BA-M01 and BA-M02 theory under the same standard because `ISS-014` still requires their separate semantic owner review. Do not review or rehabilitate their quarantined Phase 2 assessments unless the owner explicitly authorizes an assessment rebuild.

## 12. Ready-to-use instruction for Claude

```text
You are the independent curriculum reviewer for the controlled DS_BA_Curriculum repository. Read production/handover/HANDOVER-20260911-CLAUDE-BA-CURRICULUM.md completely, then read every controlling source it names before acting. Begin with BA-M03-C01 and review one chapter at a time against the contract, source, coded working PDF, collated learner PDF, content gates, and governance issues. Perform a full semantic, technical, pedagogical, citation, repetition, traceability, and publication-integrity review. Do not trust self-audits or automated gates as acceptance. Preserve codes in working artifacts and ensure they remain hidden only in the final collated publication. Record exact coded findings and issue ACCEPT, ACCEPT_WITH_CORRECTIONS, or REJECT per chapter. Do not push, merge, publish, release, start Phase 2, alter controlled scope, or claim owner acceptance. Stop on authority conflicts or critical defects and present the evidence to the owner.
```

## 13. Authoritative continuation pointer

The active BA-M03 checkpoint is `production/checkpoints/RUN-20260911-BA-M03-PHASE1.json`. Its current next action is independent semantic and owner review of the code-free collated BA-M03 publication. Phase 2 remains unauthorized until acceptance.
