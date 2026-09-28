# Chapter 19, Spreadsheet Automation: summary (Part 2 build)

**What changed.** The chapter now works for a reader who has finished only Chapters 1–11, as the approved reading order requires. It no longer depends on Chapters 14, 15 or 17. Every VBA, TypeScript and JavaScript example shows its output, and each output comes from a real run, not from typing. The six bugs the review found are fixed:
- LoopDemo crashed on the header row;
- customer codes lost their leading zeros;
- a sheet delete asked the user to confirm;
- `₹` turned into `?` in the VBA editor;
- the size bands had gaps;
- the Office Script set a row height instead of freezing panes.

The consolidation macro now has the checks its own story preaches: a per-file row log, a lock-file guard, and a stop when the count isn't 12 files. RunConsolidation is the whole job, from the files to the email, and it restores the user's settings. HTML gets a ten-minute primer before its first use. The Apps Script daily summary is built in four logged steps and reports everything since the last summary, with no weekend gap. Form input is escaped. Rupee amounts use lakh grouping, and the title matches the cover.

**New companion material.** `ch19_practice.xlsx` holds a Master sheet (Kolkata, December 2025) and a Scratch sheet for §19.2–19.5. There are three more sample enquiries (Friday, Saturday and early Monday). `expected_results.md` now uses Indian grouping. The `.bas`, `.ts` and `.gs` files are regenerated from the chapter.

**Skipped, and why.**
- **Held rows, not applied:** 19.1, 19.10, 19.15, 19.16, 19.21 and 19.35. Their fixes assume Ch 19 comes after Python. I made the order-neutral changes that the Flow, Sequence and line-by-line tests force: the prerequisites, the explanations at first use, and a short "Reading TypeScript when you know VBA" table in place of 19.10's Python table. The 19.16 month totals are still rounded and are now shown in lakh grouping (see questions).
- **19.24 left Open:** the macros must still be run in real Excel for Windows, Excel on the web and Google Sheets. That can't be done here.
- **RJ-S3-75:** the fix belongs to Ch 63 and Ch 66.

**Option picks.**
- 19.20: "since the last summary" (the first option) plus a weekend skip.
- 19.34: the first option (the table cell text).
- 19.8: `ChrW` (the only route).
- 19.14: error 513 instead of `vbObjectError + 1`, following Microsoft's documentation for standard modules.

**New Time needed.** 25–30 hours over three weeks (was 20–25): VBA 13–16 h, Office Scripts and Apps Script 6–8 h as a separate sitting, and the project about 6 h. The increase comes from the shown outputs, the HTML primer, the JS/TS line-by-line notes and the split daily summary.

**Code verification.**
- **LibreOffice 24.2 VBA mode** (`checks/ch19_run_vba_lo.py`): 14 test procedures, plus the procedures they call, run on the companion files, all outputs as printed. The consolidation was also run with a 13th file, which raised Error 513, and the handler text was checked.
- **Office Scripts** (`checks/ch19_run_scripts.py`): 2 of 2 compile under `tsc --strict`, and both outputs match.
- **Apps Script** (Node mocks): formatMaster, cleanStatuses, escapeHtml, REBATEPCT, onFormSubmit ×6, and sendDailySummary on Monday, Tuesday and Saturday. All outputs match.
- **Numbers** (`checks/ch19_numbers.py`): 14 of 14 pass.
- **Not run anywhere, checked against Microsoft's documentation instead:**
  - Dictionary-based procedures: CleanMaster, CleanStatusFast, and the second half of ArrayDemo. The same logic was run in Python, or the same expression with the stored value.
  - Excel-only procedures: the pivot, the PDF export, Outlook, `InputBox` and `FileDialog`.
  - `fetchOpenEnquiries`, because its CRM address is a placeholder.
- **Build:** `restructure --check` reports the chapter in order. The layout check is clean: 52 pages, chapter map 21/21, no stranded headings or lead-ins, no sparse pages, no small text, no tofu. "draft" appears only as "draft email".
