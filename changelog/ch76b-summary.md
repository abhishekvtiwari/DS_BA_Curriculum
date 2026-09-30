# Chapter 76B, Business Analyst Question Bank: summary

**Result:** 26 content and 11 visual findings for the chapter; all 26 content rows applied, V76B.1 and V76B.2 fixed here, V76B.3–11 already done by the style pass and rechecked. Nothing skipped. Three fixes need a line of teaching text in Part 2 chapters (Ch 25 §25.3, §25.8; Ch 26 §26.10), handed to the integrator.

## What changed
- **Drafting leftovers gone** (76B.1, V76B.1): the "not yet written at the time of this draft" note is deleted, and the re-check it promised is done. Every answer now matches the Ch 24 and Ch 25 text as it stands.
- **Flagship answers re-based on Chapter 25:**
  - The gap analysis (Q76B-028) is now Ch 25's delivery-step row (FR-14 depends on NFR-09; the root cause is that drivers have no device at the customer's site). It no longer contradicts Ch 3's automatic invoicing.
  - The swimlane (Q76B-018) uses Figure 25.1's lanes, and the order is typed into the ERP, not the CRM.
  - The automation scenario (Q76B-038) is Ch 25 §25.12's payment matching, with a ₹1 tolerance, a named owner for exceptions, and an audit trail.
  - The user story (Q76B-013) names the actual rule and adds scope, edge-case and reconciliation criteria.
- **Wrong or unsafe answers fixed:**
  - The Product Owner owns the product backlog, not the sprint backlog (Q76B-025).
  - Silently changing a correct number is now the red flag, not a "passing" answer (Q76B-033).
  - The SDLC answer follows Ch 25's six phases (Q76B-023). The business rule answer covers both kinds (Q76B-003).
  - The FRD's audience is corrected (Q76B-007).
- **Navigation:**
  - Sections renumbered 76B.1–76B.8 and IDs Q76B-001–038. The numbers are unchanged, so every inbound citation keeps its meaning.
  - The basic-but-tricky section moved to the front.
  - Every question now has a level (Fresher/Mid/Senior), roles, and a section-level "Learn it in".
  - Added "Before you start" and "Time needed".
  - Tags now use Ch 69's twelve.
- **Smaller fixes:** new extra points (data NFRs, data UAT reconciliation, 15% exceptions); Farah's role (data analyst) and finance's real need; the Tools line points to Ch 11; the Ch 78 link is honest; the heading is "Full scenarios, talked through live".

## Option picks
- 76B.11: option (a), the recommended one: teach the terms in Ch 24/25/26 (the Ch 24 stakeholder register is already there; the Ch 25/26 text goes to the integrator).
- 76B.8: Ch 25's rule, not a model threshold, since Ch 39 sets no 0.30 churn threshold.
- 76B.19: first choice (add the one line to Ch 25).
- 76B.20: first choice (keep Farah).
- 76B.24: move the basic section to the front.
- 76B.2: follows Ch 25's option A.

## Time needed
New line: 2.5–3 hours to read and drill once, plus 4–6 hours for the project (as the review estimated; the chapter had none before).

## Verification
- The chapter has no code blocks: check_code_teaching reports 0.
- `checks/ch76b_check.py`: OK.
  - 24 cited sections all exist.
  - Every quoted fact was found in the section or figure it is credited to.
  - IDs run 1–38 with no gaps; only the twelve tags are used.
  - The at-risk rule recomputed on riverstone_2025 gives 3 flagged and 7 too new of 24 accounts, as quoted.
  - Five of the nine swimlane transitions cross a lane, as quoted.
- `restructure.py --check`: already in order.
- Build: 19 pages. layout_check shows contents 11/11, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0. The only draft_labels hits are the reader's words "draft/drafting a requirement" and "for review".
- fig_check: no figures.
