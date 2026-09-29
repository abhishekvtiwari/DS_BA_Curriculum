# Chapter 63: summary

**What changed.** The numbers in §63.2 now agree with the rebuilt Ch 19, Ch 20 and Ch 58. The ROI table is a real table with a common "₹ a year" column:

| Automation | Value in ₹ a year |
|---|---|
| Flash | ₹97,500 at ₹300/h (D 66.5) |
| Branch macro | about ₹77 of time; its value is accuracy (the ₹1.88 crore double count) |
| PO intake, assisted | +₹1,00,750 in labour, but −₹2,32,500 counting missed errors at an assumed 90% catch rate |
| PO intake, straight through | −₹31,95,000 |

Other changes:
- New 1–5 scoring scales, a score table, and a worked expected-value calculation (−₹12,780 a day for straight through; assisted breaks even at about 97% catch).
- The inventory CSV now has the 24 rows the chapter claims (6/11/4/1/2, with two pairs of duplicates).
- The ungoverned count is now seventeen, since the Ch 19 macro has an owner.
- §63.3 defines iPaaS, citing Ch 51. The two honest gaps are RPA and iPaaS. The RPA example is now the transporters' websites.
- §63.5 separates polling (PO intake, 06:00 weekdays) from event-driven (webhook, defect model). The PACELC wording is corrected, and Ch 46 §46.10 runbooks are credited.
- The story no longer prints a year, and is consistent with Ch 60 ("three months into her role", "three times the eight systems").
- The warehouse is described without naming an engine, and no CRM brand is named.
- All four figures were redrawn at 680 px (min 7.6 pt). Figure files are renamed to match their numbers.

**Skipped.** Nothing among the Approved rows. RJ-S2-26 stays Open because the book calendar (P-T2) is not approved; Ch 63 now prints no year either way. Finding 63.11's first option (Kolkata billing system) was not used because it contradicts Ch 14; the finding's own alternative (a transporter portal) was used instead.

**Option picks.**
- 63.1: Option A (DECISIONS D).
- 63.6: Flash valued at ₹300/h per D 66.5, overriding the finding's ₹1,200 figure.
- 63.11: the alternative candidate, for the reason above.
- 63.9: PO intake is polling at the 06:00 weekday run, following Ch 58/60 and the coordinator, not "every few minutes".

**Time needed.** 12–14 h → **13–15 h**. The reading grows by about an hour: the scoring scales, the score table, the expected-value arithmetic, and the polling and iPaaS definitions. The project is unchanged.

**Verification.**
- The chapter has no code blocks. verify_python, verify_sql and verify_shell each ran 0 blocks, 0 mismatches; check_code_teaching reported 0.
- Every number in the chapter is recomputed by `checks/ch63_numbers.py`, which passes. It also asserts the CSV counts and scores.
- fig_check: 0 figures under 7 pt.
- restructure --check: in order.
- Build: 25 pp. layout_check clean (map 16/16, no stranded, sparse, small or clipped items, tofu 0). The draft_labels hits are reader text ("coordinator's time", "wrong draft").
- prescan: no sparse pages, and no code-token hyphen breaks.
