# Chapter 24 — summary

**What changed.**
- The chapter's running example was built on "Chapter 23's December diagnosis", which Ch 23 only has in its answer key (24.1). §24.1 now shows the November → December 2025 numbers itself: a table of customers, orders, orders per customer, AOV and revenue, plus the three effects and the mix check. They are computed from the data with Ch 23 §23.11's method. Every later use points back to §24.1.
- The model memo and BLUF no longer overstate the finding: two-thirds of the fall is smaller orders, one-third is fewer customers and orders (24.3). The "same mechanism" slip is fixed (24.4).
- One requester throughout: Vikram asks, the memo goes to him, Cc Anita, who decides (24.5). The story's weekdays are fixed (24.6).
- Wrong model answers fixed: 3, 8, 10, 11, 13 and 15. Answer 11's placeholders are filled with Ch 21's numbers; answer 10 uses Ch 21 Exercise 23's festive numbers.
- New: a RACI table and exercise 17 (24.11); a stakeholder register sentence (76B.11a); definitions of stakeholder, board pack, run rate and chat app; the BLUF vs pyramid distinction; explicit back-references to Ch 5 §5.2/§5.4 and Ch 15 §15.7/§15.11; a "Looking back" bullet; correct interview-bank chapters.
- The "Finance Controller" is now Suresh Menon, the Finance Manager (test 5: Ch 1 cast, Ch 3).
- All four figures are redrawn at 680 px, with text at 7.25–9.4 pt: no overprints or clipping, and placements match the text. Figure 24.3's waterfall is drawn from computed numbers.
- Companion: `build_ch24_files.py` now computes every number of the memo and slides from `companion/full`. The memo has To/Cc/From/Date/Re lines.

**Skipped / partial.**
- 24.1: Ch 23's side of the recommended option is for the integrator: add "§23.11 (continued): the December dip", then change Exercise 13 / Levels 5–6 so the answer key isn't duplicated.
- 24.13: "FY2026" is removed rather than defined, because it clashes with Ch 16's April–March financial year. See the question.

**Option picks.** 24.1 recommended (a) (Ch 24 side); 24.5 recommended (Vikram asks, Anita Cc); 76B.11 (a).

**Time needed.** Unchanged, 10–12 h.

**Verification.**
- `checks/ch24_check.py`: all pass. It covers every printed number of the example, recomputed in pandas and in PostgreSQL and MySQL `riverstone_full` (0 mismatches). It also checks the Ch 21 and Ch 23 numbers against their companion data, the weekdays, the segment-mix claims for both dips, and that the companion files regenerate byte-identically.
- The chapter has no code blocks: verify_sql, verify_python, verify_shell and check_code_teaching all report 0 checked, 0 mismatches.
- Build: 23 pages. layout_check is clean (map 15/15, toc_wrong empty, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0; draft_labels are all reader text). fig_check reports 0 under 7 pt. restructure --check says "already in order".
