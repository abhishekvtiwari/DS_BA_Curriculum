# Chapter 58, Intelligent Automation: summary

**Findings:** 34 content + 12 visual + 5 Reader's Journey rows naming Ch 58. All 34 content rows fixed; the 5 open visual rows fixed and checked in the rebuilt PDF (the other 7 were done by the style pass and re-confirmed); RJ-S2-23, S3-62 and S3-67 fixed; RJ-S2-21 consistent (its fix was Ch 57's); RJ-S2-26 needs no Ch 58 change. Nothing left Open.

## What changed

- **The pipeline is now taught, not described (58.8).** A new §58.0 sets up the companion folder. §58.3 runs one email through extract, parse, validate and the new `decide`. §58.4 shows the schema (money in paise, a CHECK, two UNIQUE keys, a `run_id`), `connect`, a runnable rollback demo, both `IntegrityError`s, `write` in full, and `run` as a loop, then the whole morning, the replay and the audit log. `truth` is no longer passed to the pipeline (58.7).
- **Counts reconcile.** The replay reports 59 ignored duplicates and the audit log agrees; held emails get an audit row; the replay is stamped 06:05:12 (58.9, 58.12, 58.13).
- **Resent POs are a separate case** with their own business key and queue route (58.10).
- **The threshold is priced in money** in §58.5 (58.24), and the circuit breaker is shown and demonstrated in §58.6 (58.33).
- **The arithmetic is right.** Break-even is computed in code: straight through needs about one wrong order in 424, or an error costing under ₹25 (58.2). Answers 9, 11 and 15 follow from the chapter's own model, and so do "80 minutes" and the queue share (58.3, 58.4, 58.19, 58.20).
- **A review catch rate (58.18)** changes the cost table: assisted ≈ ₹1,530 a day at a 90% catch rate, against ₹600 for typing that is assumed perfect. The chapter now says so. Assisted wins only if review catches more than 97% of wrong drafts, or if typing gets more than 1.2% of orders wrong. So the recommendation is to go assisted, start in shadow mode to measure both numbers, and design the review screen to raise the catch rate. Straight through stays out, by a factor of about 80.
- **The chapter no longer contradicts itself.** The In plain English framing, the Recap, the story, the §58.8 bullet and answers 10 and 17 now match the measured segments (bulleted, forwarded and terse emails: 37 of 37). The rule of three is added (up to about 8%), and so is a fresh-data check (58.1, 58.5, 58.6, 58.22, 58.23, 58.28).
- **Story:** Anita Rao is the Sales Head (RJ-S2-23). Meera's Chapter 1 job is named (RJ-S3-62). The March replay and the November pilot are both explained (RJ-S3-67). Review "feels" slower in the first weeks (58.29).
- **Polish:** the Chapter 78 question numbers, the Chapter 64 title and a pointer to Chapter 63 are fixed. The Appendix G line is gone, and `ch58_check.py` is no longer listed as a reader file (58.30–58.32). Macros and RPA are now told apart (58.34).
- **Figures:** all three are redrawn at 7.19 pt or more. The connectors in Figure 58.1 are corrected. The figures use blue and orange with hatching instead of green and red, and ₹ throughout (V58.1, V58.2, V58.8, V58.9).

## Option picks

58.7 (take `truth` out of the signature), 58.15 (integer paise), 58.20 (name the queue share), V58.8 (blue/orange plus hatching), 58.30 (quote questions that exist): each is the finding's recommended option, or (a).

## Skipped

None. RJ-S2-26 has no Ch 58 part.

## Time needed

It was 14–18 hours and is now **16–20 hours**, in three sittings (58.0–58.4, about 7 h; 58.5–58.8, about 6 h; the rest). The PDF grew from 25 to 40 pages, much of it code with its output.

## Verification

- verify_python: 30 blocks run, 28 outputs checked, 0 mismatches.
- verify_shell: 3 commands, 0 mismatches.
- checks/ch58_check.py: 36 checks pass, including that the chapter's code is `intake.py`'s.
- restructure --check: in order.
- fig_check: 0 figures under 7 pt.
- layout_check: 40 pages, 17/17 map numbers, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0.
- check_code_teaching flags 2 blocks. `write` is 31 lines, shown whole on purpose because the finding asks for it in full. Answer 7 is explained in prose.
- Re-run against Ch 54's new mock and Ch 57's final modules: outcomes unchanged (53/6/1, 43/10, segments). The model cost is now ₹4.71, down from ₹4.74, because Ch 57's prompt text changed.
