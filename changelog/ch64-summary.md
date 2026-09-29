# Chapter 64, Security, Privacy, Governance & Responsible AI: summary

**Rows:** 43 content (64.1–64.43), 12 visual (V64.1–V64.12), 5 Reader's Journey rows naming Ch 64. All Approved/Modify rows applied; none left Open. Status: 6 code rows and 6 visual rows Verified (verifiers / rebuilt PDF), 5 visual rows already Verified by the style pass and V64.11 already Fixed, 37 content rows Fixed, RJ-S2-29 Fixed, four multi-chapter RJ rows done for Ch 64 and left Approved for their other chapters.

## What changed

- **The access model now holds together and closes Chapter 60's risk for real.** Figure 64.1 redrawn with six roles (a pipelines/service-account row added) and new levels (masked, break-glass, load, admin-logged); matrix, prose, §64.9 and answer 10 agree. §64.9 checks the matrix against Ch 60's NFR wording role by role and records the one exception (load service accounts) as an explicit amendment. PII defined.
- **New SQL lab** in §64.3 ("From matrix to database"), promised by Ch 12: CREATE ROLE, GRANT/REVOKE, a SET ROLE test with the real permission error, a salted masked view, row-level security with two policies and per-role outputs, a refused cross-branch INSERT, and the grants query as the check; plus "The quarterly access review" (Ch 60's promised measure). New §64.0 sets up the `riverstone_access` database (`companion/ch64/access_lab_setup.sql`) and the audit files.
- **§64.5 rewritten against dated sources** (29 September 2026, listed in `companion/ch64/regulation-sources-2026-09.md`): DPDP scope, the three-phase Rules timeline (13 Nov 2025 / 13 Nov 2026 / 13 May 2027), Rule 7 breach intimation, legitimate uses, the public-data exemption, CERT-In's 6 hours; GDPR scope (Art. 3(2)), transfers, Arts. 6, 33, 34; EU AI Act dates and the Digital Omnibus (Reg. (EU) 2026/1744: Annex III → 2 Dec 2027, Annex I → 2 Aug 2028, Art. 50 not deferred). Riverstone's position stated once (no EU customers).
- **The fairness audit is real code on a real model.** `build_ch64_files.py` now trains a scikit-learn stand-in for the Part 4 lead model, scores 1,830 leads, saves the model bundle and writes a model card. §64.7 is six cells (load, gap, Welch test, `feature_names_in_` check, crosstab, full pivot), each explained line by line, with a data dictionary, definitions (protected attribute, disparate impact/treatment, proxy) and a Simplification note (RJ-S2-29). New numbers: West 29.0, East 15.0, gap 14.1 points, p 5.81e-37; within size bands the gap disappears.
- **§64.8 gains** the model card as a governance record (building on Ch 39 §39.10), explainability and accountability, and "Governing generative AI" (disclosure, logs and retention, owned hallucination/injection risks, a named human for every automated write).
- **§64.4:** pseudonymization vs anonymization with the legal consequence and salted hashes; differential privacy stated as a bounded limit; the Ch 57 log-hash example (replacing an invented Ch 56 one); a box on AI assistants as third parties.
- Cross-references fixed (Ch 32 §32.13, §62.7, Ch 62's fit-over-fashion, Ch 52 §52.1/§52.6, Ch 80), drafting leftovers removed, one tested environment stated, exercises extended (new SQL exercise 13), story year removed (no calendar decision needed).
- **Figures:** 64.1, 64.2, 64.4 redrawn on 680 px canvases (min 7.62 pt, text wrapped with the PDF font); 64.3 redrawn at print width (8 pt, shared scale labelled, East one colour, values on bars).

## Skipped or softened, and why

- 64.36: the reviewer's close-rate figures ("11% to 14%, n = 190") were not used, because nothing in the book supports them; the story gives the causal caveat instead (question 2).
- 64.35: the suggested `storage_encrypted = true` line is not in Ch 52's Terraform, so the text says "a setting you switch on, or one line in a Terraform file".
- Legal facts rest on search extracts of the official texts plus agreeing legal summaries; the official sites were blocked from the build machine. A lawyer's read before print is recommended (question 1).

## Option picks

64.1 masked (recommended); 64.2 option (a), plus the explicit amendment for service accounts; 64.3 both suggestions; 64.4 recommended lab (with a lookup table instead of `current_setting`); 64.16 load the artefact (first option); 64.32 add the section; 64.34 add rather than trim; RJ-S2-29 simplified stand-in.

## Time needed

15–18 hours over two weeks (was 14–16): about 7 for the sections and code (the SQL lab and six-cell audit are new), 4 for the exercises, 4–7 for the project.

## Code verification

- `checks/ch64_sql_check.py` (new): 11 SQL blocks run, 6 outputs checked, 0 mismatches, exercise 13's answer checked (PostgreSQL 16, private cluster).
- `verify_python`: 6 blocks, 6 outputs, 0 mismatches. `verify_shell`: 2 commands, 0 mismatches. `verify_sql`: lab blocks marked `run: none` (0 statements). `check_code_teaching`: 0 findings.
- Build: 34 pages; `layout_check` clean (map numbers 16/16, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0; "Draft"/"draft" hits are reader text); `fig_check` 0 figures under 7 pt; `restructure --check` in order.
