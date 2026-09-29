# Chapter 45 · Data Ingestion & Integration · one-page summary

**Findings:** 39 content (45.1–45.39), 13 visual (V45.1–V45.13), 1 Reader's Journey row naming Ch 45 (RJ-S2-18). Fixed: all 39 content rows, V45.1–V45.4 and V45.13 (the other visual rows were already done by the style pass and were re-checked). Left Open: RJ-S2-18's Ch 45 part that needs a story year (fact sheet not approved).

## What changed

- **Hashing moved in from Chapter 2 (45.1):** a new "What a hash is" subsection opens §45.5: SHA-256 in three cells, the four properties, where hashes are used (checksums, backups, salted slow password hashes), MD5 vs SHA-256, then row hashes by hand on the §45.4 toy table before the SQL version.
- **Setup a first-timer can follow (45.2, 45.3, 45.5, 45.6, 45.38):** numbered steps (copy the folder, activate the Ch 17 venv, pinned install, import check, `.env` connection string, notebook), a DuckDB API cell and a psycopg2 connection/cursor cell before any helper, a `%s` vs `?` table. `reset()` now reads the same `RIVERSTONE_SOURCE` string (companion changed).
- **Code that obeys the chapter's own rules:** reconciliation sees warehouse-only statuses (now four mismatches, with Shipped 0 vs 1); placeholders instead of f-strings; NULL-safe row hashes; `compare_hashes()` defined once; a load log keyed on (fingerprint, day) that records only after a successful load; `raw.dispatch` with `source_file` and `loaded_at`, loaded idempotently by file; retries for 429, 503, timeouts and dropped connections with backoff; the token from the environment.
- **By hand first (45.9):** a five-order watermark example with questions, Figure 45.2 moved above the code.
- **CDC:** `ALTER SYSTEM` plus per-OS restarts; autocommit explained truthfully; how to read change lines, including DELETE; slot lag taught here with a real query (the Ch 47 promise dropped).
- **Wrong claims corrected:** DuckDB *guessed* the day-first dates; positional matching; Parquet pointer now Ch 49; Part 8 pointer Ch 77/78; answer 13's skip/duplicate logic; answer 1's real column `entered_at`; answer 9's attempts; story customer and scale.
- **Figures:** 45.1 and 45.2 redrawn at ≥ 7.1 pt with ✓/✗/hatching; the strategies figure became a normal table with ✓/✗; the file-loading figure (now 45.3) redrawn 3 × 2. `fig_check`: 0 under 7 pt.
- **Exercises:** new warm-up 4 (hash with a trailing space); old 4–14 renumbered 5–15; exercise 9 now asks for jitter because the chapter's retry already backs off.

## Option picks
No finding marks a recommended option. Option (a) used for 45.19 (teach slot lag here) and 45.25 (extend the retry code).

## Skipped or changed from the finding, and why
- RJ-S2-18: the story's year needs the book calendar in the unapproved fact sheet → Open, question asked.
- 45.1: no Ch 64 pointer for password hashing (Ch 64 has none).
- 45.17: the finding's reason (the slot bookmark doesn't advance without autocommit) didn't reproduce on PostgreSQL 16; the explanation uses a verified reason instead.
- 45.34: the finding suggested `changed_at`; the real column is `entered_at`.
- 45.14: the two runs are shown where the file is really loaded (§45.7), not in §45.5.

## Time needed
14–18 h → **15–20 h**, four sittings (45.1–45.4; 45.5–45.6; 45.7–45.8; 45.9–45.11 and the project). The chapter grew from 33 to 46 printed pages (hashing section, setup steps, split cells).

## Verification
`verify_python.py`: 40 blocks run, 38 outputs checked, **0 mismatches** (DuckDB 1.5.6, psycopg2 2.9.13, PostgreSQL 16.13 with `wal_level = logical`). `verify_shell.py`: 1/1, 0 mismatches. `verify_sql.py`: nothing to run. `checks/ch45_check.py`: all pass. Sample answers 6, 9 and 11 were run against the chapter's state and work. Build: 47 pages; `layout_check` clean (map 17/17, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0); `restructure --check` in order.
