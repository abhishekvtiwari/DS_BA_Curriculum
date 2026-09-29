# Chapter 51, Data Activation: summary

Part 5 build, 29 September 2026. Detailed record: `changelog/ch51.md`.

## What changed

- **New §51.0 "Setting up the practice environment".** Copy `companion/ch51` to `work/ch51`. Nothing new to install. `.env` gains `CRM_API_TOKEN` and `WEBHOOK_SECRET`. The first cells reset `riverstone_source`, start the sandbox CRM (port 8051) and the webhook receiver (8052), and seed the CRM with 43 leads and 23 accounts. This fixes the root cause of every `NameError` in the old PDF.
- **§51.2 shows the computation.** It states "today" (6 Jan 2026) and gives the stage and source point tables. Leads are worked by hand (2 → 65, 6 → 0, 7 → 100), then as SQL (`lead_scores.sql`) and loaded from Python. The "overdue" flag is now an honest **follow-up-due** flag (`follow_up_due.sql`, 6 customers). It is computed for all 24 customers and synced.
- **§51.3 covers writing through an API.** Scope and service account are defined, and there is a table of the four HTTP methods. A live PUT-vs-PATCH demo shows PUT wiping lead 1's fields. `idempotency_key()` is shown with outputs, then one write is built step by step. `sync_record()` retries timeouts, dropped connections, 429 and 503 (honouring `Retry-After`), and fails fast on other errors. The first full sync shows a real 429 retry.
- **§51.4 is about idempotency, proven.** An upsert creates the missing account 24. A slow answer after an applied write is replayed safely. Lead 4 goes to 21 and back to 20, which shows the content-only key bug. The fix is `run_key()`, which adds the run id to the key. There is a corrected key table (UUID row, Stripe checked) and a new watch-out.
- **§51.6 covers webhooks.** Registration output, the ₹2,00,000 threshold, and the explained polling loop are all shown. A new "Signatures: HMAC" part includes the receiver's handler; a genuine request is accepted, a duplicate skipped, and a forged one refused with 401.
- **§51.7 reconciles the writes.** Leads and accounts are read back page by page, and mismatches are found (lead 4, 20 vs 21). "Tomorrow's" run with the run-id key writes an audit log (JSON Lines) and prints the five-count report: 67 attempted, 67 confirmed, 0 mismatched.
- **Figures 51.1 and 51.2** were redrawn at print size (≥ 7.4 pt), with no labels crossed or clipped, and the link count is set as n(n−1)/2.
- **Tail.** The mistakes table has four new rows (retry-loop key, content-only key, retrying one failure kind, PUT). Project steps 3–5, the recap, key terms and Check yourself match the new content. Answers 4–7 and 13 were fixed. The Appendix G line is gone. "Where this leads" has the corrected Ch 63 title and adds Ch 78.

## Skipped, and why

- Nothing Approved for Ch 51 was left undone. RJ-S2-29's remaining fix is in Ch 64 (see the questions file).
- 51.11's suggestion to explain `requests.Session`: the chapter no longer uses a Session, so there is nothing to explain.
- Real SaaS APIs (Census, Hightouch, Stripe, OAuth providers) are not called. Every API call goes to the local sandbox, and no block is "not re-run".

## Option picks

- 51.5: **option A** (rename to a follow-up-due recency flag), the preferred option.
- 51.6: the run-id key (the finding's first suggestion), with the key-expiry note added as well.
- Everything else: the single fix each finding described.

## Time needed

**14–18 hours** (was 12–16), as the review suggested. The chapter grew from about 21 to 38 pages. It adds 25 run cells, two SQL queries, the PUT/PATCH demo, the HMAC receiver and the run-id reconciliation.

## Code verification

- `verify_python`: 25 blocks run, 24 outputs checked, **0 mismatches** (fresh `riverstone_source`, sandbox CRM and receiver running locally).
- `verify_sql`: 2 statements, **0 mismatches**. `verify_shell`: no shell blocks.
- `check_code_teaching`: 30 blocks, 0 flagged, 0 findings. `checks/ch51_check.py`: all checks pass.
- Build: 39 pages. `layout_check`: map 17/17, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0 (the one `draft_labels` hit, "for review", is reader text). `fig_check`: 0 figures under 7 pt. `restructure --check`: already in order.
