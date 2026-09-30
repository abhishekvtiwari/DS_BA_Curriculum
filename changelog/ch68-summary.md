# Ch 68 How Data Hiring Works: summary

**What changed.** 35 content findings applied (68.1–68.35). The main ones:
- Farah's story now follows Ch 8's internal move and Ch 9's twelve-week SQL log. Her re-score is shown as a working line (8 of 10 = 80%).
- The 30/60/90-day plans are now checked against the book's own Time needed lines, and the 90-day plan is triaged honestly.
- A new §68.6 on pay holds the Data Scientist and Data Engineer rows and the growth discussion moved from Ch 8 (parked block 5 of `_parked/ch07-08-moved-out.md` landed). Old §68.6–68.8 are now §68.7–68.9.
- Example 3 now totals 12 / 24.
- The resume Skills lines now match their annotations. CBAP became ECBA. "Peeking" replaces "stopping-time bias".
- Company "tiers" were replaced with plain wording.
- The rounds table covers every bank.
- LinkedIn and ATS claims were softened and dated.
- The worked examples are grouped. Examples 9–10 got honest hours.
- The chapter now has an Answers section and a new exercise 6 (data engineer pay growth, 56.4%).

**Visual.** V68.1–V68.6 were confirmed in the rebuilt PDF (26 pages). The layout check is clean: map 15/15, no stranded headings or lead-ins, no sparse pages, no small text, no tofu. The draft-label hits are reader text ("coordinator", "Draft the…"). There are no figures and no High visual findings, so there are no before/after crops. V68.7 (a white panel for resumes) needs a builder change and was passed to the integrator.

**Skipped or partial.**
- 68.17: the PayScale figures are the 16 Sep 2026 retrieval. They were **not re-verified live**, because payscale.com is blocked by the proxy. Search snippets agree on the DE row, the DS entry pay and the DS range. They disagree on the DS profile count and update date (1,342 profiles, 28 May, against 1,267 in the table). This is a question for Abhishek.
- 68.13 and 68.21 were verified only through search-result text of the official pages (IIBA handbooks, May 2026; LinkedIn Help a507508). iiba.org and linkedin.com are blocked.
- 68.5, 68.16 and 68.35 use the current numbers (72A, 76A, 76B). They need a recheck in the D2 renumbering pass.

**Option picks.** None had lettered options. Where a finding offered alternatives, the recommended one was used: fix the resumes (68.7, 68.9), replace "tier" (68.15), add group headings (68.24).

**Time needed.** It was "2–3 hours to read". It is now "2.5–3.5 hours to read; allow 3–5 hours more for the project", because of the new §68.6, the Answers section and longer plans.

**Code verification.** The chapter has no code. All arithmetic was recomputed in Python:
- growth 36.9 / 68.9 / 56.4%, and the ratio 1.73;
- runway weeks and hours 12.9 / 8.6 / 4.3 and 77 / 51 / 26;
- chapter-hour sums 104–127, 37–46, 54–67, 169–209, 122–147 and 86–103;
- Example 3's maximum of 24.

`restructure.py --check`: already in order.
