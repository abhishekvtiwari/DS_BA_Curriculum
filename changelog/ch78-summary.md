# Ch 78 summary: Automation & Integration Question Bank

**What changed.** All 27 content rows and the open visual rows (V78.1, V78.2, V78.7) applied.
- **Code is real now.** The four "verified, live" claims are backed by code shown and run: webhook idempotency (ID now recorded *after* the work), a new rate-limiter worked example (deque, 3 calls/s, simulated times), retry with exponential backoff (three cells plus a "what if" give-up cell), and the CRM upsert (`sync_lead_score` defined, re-run proves idempotency). Every line explained; predict and what-if prompts added.
- **Pointers go to teaching chapters**, not other banks: Ch 19–20, 29 §29.9, 45 §45.9, 46 §46.4/46.6/46.7, 47 §47.5/47.9, 50 §50.3, 51 §51.1–51.10, 52 §52.6, 57 §57.8, 58 §58.1/58.2/58.6/58.10, 61 §61.6, 63 §63.2/63.3/63.7/63.8; banks appear as "Practise it with". Every section number was checked against the current files.
- **Correctness:** low-code hook (connectors wrap APIs), webhook ordering, column read by name, freshness vs. volume check, Ch 77 "retries" claim, Passes rows rewritten as partially right.
- **Structure:** basic-but-tricky moved to §78.2; stub design cases deleted; Q78-029 → **Q78-028**; drafting leftovers ("this chat", "blueprint") gone; Ch 76B cited as §76B.4 / Q76B-021.
- **Format:** Ch 69 tags, Level (Fresher/Mid/Senior) and roles (AUT, DA, BA, BI, DE), "Before you start", "Time needed".

**Option picks.** 78.5: (a) add a worked limiter block. 78.14: (a) delete stubs and renumber. 78.17: keep Q-numbers stable (first option). V78.2: drop the stubs.

**Skipped.** 78.15 moot (Q78-031 deleted by 78.14). Nothing else skipped.

**Time needed (new):** 2–2.5 hours for a first pass (8 core questions × ~10 min, 19 rapid-fire rows, 30 min for the code demos); 30 minutes for the final-week list. It had none before.

**Verification.** `verify_python.py`: 8 blocks run, 6 outputs checked, 0 mismatches (Python 3.11, 3.12, 3.13). `check_code_teaching.py`: 0 flagged. `restructure.py --check`: already in order. Build: 19 pages; layout_check clean (map 9/9, no stranded heads/lead-ins, no sparse pages, no small text, tofu 0, no draft labels); prescan clean; no figures.
