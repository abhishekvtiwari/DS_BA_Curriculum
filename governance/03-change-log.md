# Change Log

## 0.2.0 — Operational production layer

- Added explicit JSON module contracts for all 33 modules.
- Added output directories and required artifact paths.
- Separated pre-assessment content audit from assessment validation and final release audit.
- Added master index, glossary register, cross-reference register, open-issues register, and checkpoint schema.
- Added assessment validation rubric and machine-readable examples.
- Added version metadata and resumable production-state rules.

## 0.2.1 — Contract correction release

- Corrected all 33 module artifact paths to use the actual module ID.
- Replaced generic objectives with module-specific learning objectives.
- Added an objective-quality marker to every contract.
- Added repository-root `.gitignore` rules for generated archives and temporary files.
- Verified that the organized repository root contains no unintended duplicate artifacts.

## 0.2.2 — External roadmap coverage audit

- Added controlled coverage-gap report `REF-AUDIT-20260910-01` for the supplied roadmap.sh references.
- Classified candidate gaps by priority and separated core gaps from optional tool choices.
- Recorded `ISS-003` to prevent candidate topics from becoming curriculum scope without approval.
- Preserved all existing module, chapter, and topic IDs; no curriculum scope changed.
