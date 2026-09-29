# Part 7: questions for Abhishek

These are the chapter agents' questions in reading order, each trimmed to the decision it needs. None of them blocks
the Part 7 PDF: every chapter builds, and the wording is chosen so it stays true whichever way you decide.

## Two decisions that several chapters wait on (fact sheet, PR #3)

1. **Book calendar (P-T2; RJ-S2-26, RJ-S3-77 and 67.10, held Open).** Every Part 7 story now prints no year:
   - Ch 60 opens "the January after the PO-intake pilot went live".
   - Ch 61 is still dated "February 2026".
   - Ch 62 says "a few months into Meera's time".
   - Ch 63 says "That April".
   - Ch 64 says "In June, five months into her role".
   - Ch 67 is undated.

   If you approve P-T2, the stories get dated in 2027 (e.g. Ch 61 "February 2027", Ch 62 "March 2027", Ch 67
   "late 2027"), each a one-line edit.
2. **Production warehouse engine (fact sheet §4 / C1).** The options are A, "practice DuckDB, production PostgreSQL
   on RDS", or B, "DuckDB everywhere".
   - Ch 60 names no engine.
   - Ch 61 follows finding 61.3's DuckDB wording.
   - Ch 65's bill prices an RDS instance.

   Once you choose, Ch 60, 61, 63, 65 and 80 get a one-line edit each.

## Money and scale

3. **Exchange rate.** Three rates are in use: ₹83 (Ch 49), ₹87 (Ch 65) and ₹88 (Ch 57). Each calculation now
   states the rate it uses. Should the book pick one rate, and if so which?
4. **The PO-intake conclusion.** Ch 58's rebuilt maths now appears in Ch 63, 65, 66 and 67. At a 90% review catch
   rate, assisted intake costs more than error-free typing, and it breaks even only at about a 97% catch rate. As a
   result, Ch 66's business case now reads "measured savings cover 22% of the platform cost, 44% once the catch
   rate is proven" (it was 45%). Happy for Part 7 to carry this message?
5. **Ch 65: invented bill details.**
   - The bill provisions 800 GB of warehouse storage, while the real database is 45 MB. Keep it, or shrink it to
     about 100 GB?
   - The sensor archive is priced as Ch 49's 1,460-sensor rollout having happened. OK?
   - Reserved pricing uses option (a) for 65.1, the review having leaned to (b).
   - Two volumes come from earlier chapters' planning figures: 1,000 RAG questions a month, and 500 parts a week.
6. **Ch 66, a build-vs-buy price (66.16, Open).** The vendor pages are blocked here. May a dated third-party listing
   be used (for example Secoda Starter at $99 a month), converted at the book rate?
7. **Ch 66: the hire.** Two things to confirm:
   - The ₹9,00,000 salary is framed as "Riverstone's budget for the role", not a market figure. Search snippets
     suggest ₹7.3–8.6 lakh.
   - "20 people × 1 hour a week" of time lost finding data is new, labelled estimate material.

   Keep both?

## Story details

8. **Ch 61: the outage now runs to 6:10 a.m.,** so that the 06:00 PO-intake run (Ch 58, Ch 60) meets it. Confirm?
   The CRM is no longer named "Zoho" anywhere, as in Ch 60.
9. **Ch 63: the RPA example** uses the transporters' delivery-status websites. The finding's Kolkata billing system
   can't be used, because Ch 14 says Kolkata moved off it.
10. **Ch 64: the story's close rate.** The review suggested "11% to 14%, n = 190", but no data supports it, so the
    story gives only the 41 h → 6 h response-time drop. Do you want to supply a close-rate figure?
11. **Ch 64: the fairness audit now runs on a real stand-in model** (RJ-S2-29). Every §64.7 number changed: West 29.0,
    East 15.0, a gap of 14.1 points. OK?
12. **Ch 67: the owning family (C13).** Ch 67 keeps "Riverstone's owning family", and adds the managing director
    Arvind Kapoor (from Ch 60). Keep the family, or make it "the board"?
13. **Ch 67: do the branch sales offices sit under sales (Anita Rao)?** The influencing scenario is aimed at "Vikram
    Singh's team and the branch sales offices".

## Legal review

14. **Ch 64 §64.5 (T13, rows 64.7–64.13).** It now states exact dates and duties, all checked on 29 Sep 2026
    through search results quoting the official texts, because the official sites are blocked here. Sources are
    listed in `companion/ch64/regulation-sources-2026-09.md`. The laws covered:
    - the DPDP Act and Rules 2025;
    - GDPR;
    - the EU AI Act and the Digital Omnibus on AI (Reg. (EU) 2026/1744);
    - CERT-In's 6-hour reporting rule.

    A lawyer's read is recommended before print.

## Not done here, for later passes

- **Glossary (Appendix A).** Every Part 7 chapter points to "Glossary, Appendix A", but there is no appendix file in
  the manuscript yet. The new key terms are listed in each chapter's changelog.
- **Hours (T12, final pass).** Part 7 is now 82–99 hours (was 76–93).
