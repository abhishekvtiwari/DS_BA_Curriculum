# Curriculum Blueprint Governance

## Status labels

- PLANNED: listed in blueprint, no prose written.
- OUTLINED: module contract and chapter/subtopic scope approved.
- DRAFTED: prose, examples, and labs written.
- PRE_ASSESSMENT_AUDITED: content coverage and technical checks passed before assessment generation.
- ASSESSMENT_DRAFTED: assessment bank generated and mapped.
- ASSESSMENT_VALIDATED: assessment bank passed correctness, coverage, duplicate, difficulty, and practical checks.
- FINAL_AUDITED: final release audit passed with no critical blockers.
- RELEASED: approved module package with release record.
- BLOCKED: work cannot proceed until listed issues are resolved.

## Non-negotiable rules

1. Do not invent modules, chapters, topics, or subtopics outside the blueprint.
2. Do not write prose until the module contract is approved.
3. Do not mark a topic complete because it is mentioned.
4. Every technical topic needs implementation, expected output, validation, and troubleshooting.
5. Every code example must identify runtime, dependencies, input, expected output, and safety limits.
6. Every SQL example must identify dialect, grain, joins, null handling, date logic, and validation.
7. Provider-specific AI information must be dated and checked against official documentation.
8. Do not use confidential or personal data in examples.
9. Maintain indexes, glossary, cross-reference map, open-issues list, change log, and checkpoints.
10. Use the output directories and naming convention defined in the README.

## Required production sequence

```text
1. Approve module contract
2. Draft chapters, topics, examples, labs, and assignments
3. Run PRE_ASSESSMENT_AUDIT
4. Revise content until the pre-assessment audit passes
5. Generate assessment bank
6. Run assessment validation
7. Revise assessment bank until validation passes
8. Run FINAL_RELEASE_AUDIT across content and assessments
9. Resolve critical issues
10. Create release record and mark RELEASED
```

## Module release gate

A module may be released only when all planned chapters and subtopics are addressed; labs run or are clearly marked pseudocode; assignments have answer criteria; assessment items are validated; terminology and cross-references are consistent; security, privacy, and ethics are covered where relevant; and the final release audit has no unresolved critical issue.
