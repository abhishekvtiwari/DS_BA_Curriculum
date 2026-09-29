# Chapter 50, Streaming & Real-Time: summary

Part 5 build, 29 September 2026. Detailed record: `changelog/ch50.md`.

## What changed

- **New §50.0 "Setting up"**: copy `companion/ch50` next to `work/ch48`, and nothing new to install for the main thread. §50.1–50.8 keep their numbers.
- **The log (§50.2).** Figure 50.1 was redrawn so each key sits in one partition, and the machines match the companion's real hash. `sensor_events.readings()` is now half-open, like `range()`. There are tables for the helpers and for the `MessageLog` API with its Kafka equivalents. The committed offset is defined as the *next* offset to read. Short Python idioms are explained.
- **Delivery guarantees (§50.3).** A new by-hand crash trace comes first (at-least-once vs at-most-once). The in-memory `seen` set is replaced by a DuckDB table on disk, keyed by machine + event time, and a real restart prints 82, then 0. Sink and idempotent are defined. The Kafka code is split into producer, consumer and loop cells with parameter tables. A new optional section runs a **real single-node Kafka 4.3.1 broker**, so the Kafka cells now show real output: sent 300, read {0: 96, 1: 204}, 82 hot. The old "not executed" note is gone.
- **Spark streaming (§50.4–50.5).** Big cells are split one idea at a time: session, schema, readStream, windowed query, `run_once()`, `show_windows()`, progress keys. Three new pieces come before the code: "Three kinds of window, by hand" (tumbling, sliding and session, confirmed by real Spark cells), a boxed watermark rule with a hand table, and a "same word, different job" box that sets this watermark against Ch 45's. Figure 50.2 was rebuilt as a timeline plus three run cards. The progress report shows the watermark each batch *used*. The dropped-row count and the M-09 stragglers are explained correctly (1,506 rows, dropped 1).
- **Sink (§50.6).** Files and rows per file are printed (9 files, 5 of them empty). The Delta file sizes come from `get_add_actions(flatten=True)`, as Ch 49 does it. The file-count arithmetic is corrected.
- **Case, mistakes, answers.** §50.8 describes per-plant vs per-machine state correctly. The Common mistakes table adds both auto-commit symptoms and a row on keeping the de-dup record in memory. Answers 4, 8, 9 and 11 were corrected. Where this leads adds Ch 61/62. The "Appendix G" drafting note was deleted.

## Skipped, and why

- **RJ-S2-18** (Open in the register): dating the chapter's story needs the unapproved Riverstone fact sheet. The "on a Tuesday" story is unchanged.
- **50.8:** the suggested "Appendix E" pointer was not added, because there is no appendix file.
- **50.14:** "Chapter 52 shows the same broker in a container" was not added, because Ch 52 has no Kafka container.

## Option picks

- 50.1: the recommended redraw, adapted to the real hash. The finding's example machines (M-03/M-12) hash to partition 1, so M-04/M-08 (partition 0) and M-07/M-21 (partition 1) are used instead.
- 50.11: delete the `commit(…, {0: 0, 1: 0})` line.
- Everything else: the single fix each finding described.

## Time needed

**15–19 hours** (was 12–16). The chapter grew from about 7,900 to 13,700 words. It now has more cells and three new by-hand sections, plus an optional 30–45 minutes for the Kafka broker. The line suggests four sittings.

## Code verification

`checks/ch50_verify_all.sh`, re-run on 29 Sep after the container restart, from a clean scratch folder:
- `verify_shell`: 8 commands, 8 outputs checked, **0 mismatches** (download, format and start Kafka 4.3.1, create the topic).
- `verify_python`: 28 blocks run, 24 outputs checked, **0 mismatches**, including the Kafka producer and consumer against the live broker.
- `checks/ch50_check.py`: 33 facts, all OK.
- `check_code_teaching`: 30 blocks, 0 flagged. `fig_check`: 2 figures, min 7.14 pt. `restructure --check`: in order.
- PDF: 36 pages, map 15/15, toc_wrong empty, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0. The only `draft_labels` hit is the reader text "for review" in the §50.1 table.
