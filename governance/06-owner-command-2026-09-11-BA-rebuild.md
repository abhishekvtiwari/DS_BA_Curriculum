# Owner Command - BA Curriculum Rebuild Authority

**To:** Codex (curriculum lead)
**From:** Owner
**Date:** 2026-09-11
**Branch:** `governance/iss-009-batch-rejection` - 2 commits, **not pushed to origin**
**Status:** ISSUED

---

## 1. State you are inheriting

An independent review measured the BA corpus. Two batches are formally rejected or quarantined and the
records are committed on the branch above.

| Issue | Severity | Subject |
|---|---|---|
| `ISS-008` | CRITICAL | BA-M01/M02 Phase 2 question banks QUARANTINED |
| `ISS-009` | CRITICAL | BA-M04-M15 Phase 1 theory REJECTED, 53 chapters |
| `ISS-010` | HIGH | the chapter self-audit was a no-op; replaced by measurable gates |
| `ISS-011` | HIGH | 19 wrong cross-reference module titles, corpus-wide |

Read before acting:

- `governance/02-open-issues.md`
- `governance/05-content-gates.md`
- `production/audits/BA-BATCH-20260911/BA-M04-M15-THEORY_BATCH_AUDIT.md`
- `production/audits/BA-BATCH-20260911/BA-M01-M02-ASSESSMENT_INTEGRITY_AUDIT.md`

Reproduce every claim yourself before accepting it:

```
python tools/content_gates.py --all --quiet
python tools/content_gates.py production/drafts/BA-M05/BA-M05-C03.md
```

Do not take the prior review on trust. If a measurement is wrong, correct it in the audit record rather
than working around it.

## 2. Why the batch was rejected rather than corrected

BA-M04-M15 is template substitution, not authorship:

- ~9% of 76,282 words is topic-specific
- 39.6% of paragraphs are exact duplicates; 53.5% after collapsing name substitution
- one paragraph template serves 222 of 364 topic sections
- zero code blocks, zero worked examples, zero content tables across 53 chapters
- all 364 `SELF_AUDIT_PASSED` stamps voided; all topic rows `COVERED` to `UNVERIFIED`

The BA-M01/M02 question banks are disqualified outright: the correct answer follows a fixed `A, B, C, D`
cycle keyed to question number in **400 of 400** questions, so a learner scores 100% with no subject
knowledge. Do not repair these banks.

## 3. Root cause - the prompts were already correct

This is the most important item in this command, and it revises the earlier framing that the audit
*design* failed.

`prompts/02-chapter-generator.md` already requires, for every subtopic: beginner explanation,
terminology, conceptual model, **example**, practical method, **implementation or tool procedure**,
**expected result**, quality checks, **failure modes**, advanced note, **exercise**, answer criteria,
glossary terms, cross-references.

The rejected chapters deliver three section types - Concept, Analysis and application, Quality checks
and limitations. Verified absent across all 53: **worked examples (0/53), code blocks or tool
procedures (0/53), advanced notes (0/53)**.

`prompts/04-assessment-generator.md` already says "Avoid ambiguous questions and repeated wording."
`prompts/05-quality-audit.md` already requires identifying "repeated generic prose" and returning
critical blockers separately - it would have caught ISS-009.

**A correct instruction was not followed, and the specified independent audit was replaced by a weaker
self-audit the authoring run wrote for itself and then passed.**

Therefore: **do not rewrite these prompts. Apply them.** Run `prompts/05-quality-audit.md` as a separate
step against a chapter you did not just author. An in-chapter self-stamp is not an audit and will not be
accepted as one.

## 4. Directives

### 4.1 Allocation

Abolish the flat "approximately 10,000 words per chapter" allocation. It appears in every chapter header
and matches no chapter in the repository. Replace with density per controlled topic:

- planning target: **1,000 words per controlled topic**
- blocking floor: **600 words per controlled topic**

Rewrite G9 in `tools/content_gates.py` to measure words per controlled topic against the 600 floor
rather than 40% of a header figure. Strip the obsolete allocation line from chapter headers and
word-budget files. Close the `ISS-009` allocation contradiction on this basis.

Basis, reproducible with the gate tool: BA-M02 runs 691-1,466 words/topic; BA-M03-C07 787; the rejected
batch 205-212. The rejection verdict is invariant across floors of 450 / 600 / 750, so this threshold is
a remediation-cost decision, not a correctness one.

### 4.2 Gates

Adopt G3, G4, G6 and G8 as **blocking for rebuilt and new chapters** via `--strict`. They remain
advisory for existing chapters. Existing failures are a remediation backlog, not a regression.

### 4.3 BA-M01 backlog

`BA-M01-C03`, `C04` and `C05` fall below the 600 floor at 471, 309 and 413 words/topic. They pass every
structural gate and are **not rejected**. Open `ISS-012`, MEDIUM, deferred until the rebuild completes.
BA-M02 is the depth benchmark and is unaffected.

### 4.4 BA-M03 unparked

Lift the `ISS-005` park. **BA-M03 is not rejected and must not be rebuilt from scratch.** C01-C06 pass
G1, G2, G5 and G7 and fail only G9 depth - genuine writing, under-depth, categorically different from
the template artifacts in ISS-009.

| Scope | Classification |
|---|---|
| C01-C06 | **RETAINED** - deepen in place to the 600 floor. Preserve existing prose. Do not discard and regenerate. |
| C07 | **READY FOR INDEPENDENT REVIEW** - 787 words/topic, passes every blocking gate. |
| C08-C12 | **NOT DRAFTED** - 46 controlled topics, author per 4.5. |

Close `ISS-005`, open `ISS-013` for the top-up and the C08-C12 authoring.

### 4.5 Rebuild sequence

One chapter at a time. Gate each with `--strict`. **No batch authoring under any waiver.**

1. **`BA-M05-C03` SQL for Analysts** - calibration chapter. 8 controlled topics, target 8,000 words,
   floor 4,800. Must demonstrate executable SQL with worked results, data tables, dialect distinctions,
   failure analysis and inline sourcing. Every expected query result must be produced by running it,
   never typed.
2. On Owner acceptance of (1), **`BA-M03-C01`** as the first top-up, to prove the retain-and-deepen path
   before the remaining 51 chapters.
3. Remaining BA-M04-M15 chapters, module by module.

### 4.6 ISS-011

Correct the 19 wrong cross-reference module titles and the three competing BA-M05 titles as a standalone
mechanical pass **before** rebuild authoring starts. Do not fold it into chapter work.

### 4.7 ISS-008

No Phase 2 authoring for any module until that module's theory rebuild is accepted. Rebuild the banks
with randomised keys and misconception-based distractors; verify the key distribution and publish the
verification alongside the bank.

## 5. Acceptance

Gate output is the evidence. A chapter's own self-assessment is not, and that is precisely what produced
`ISS-009` and `ISS-010`.

Codex may mark: Selected, In Production, self-review states, Ready for Final Review. Codex may **not**
self-accept curriculum it authored or corrected. Owner acceptance is required for every rebuilt chapter.
Independent review of Codex-authored curriculum is assigned to Claude Code.

## 6. Not authorised by this command

Pushing to origin. Merging the branch to main. Any Phase 3 or later work. Regenerating PDFs. Deleting
anything under `output/_QUARANTINE/` or `production/drafts/`. Reinstating any voided
`SELF_AUDIT_PASSED` stamp.
