# Chapter 34 — summary of changes (Part 3 build)

**What changed.** D2 is in: the terminal basics (old §34.1–34.2: opening a terminal, navigation, paths, make/copy/move/remove) now live in Ch 26 §26.0. The chapter opens with **§34.0 "Where Chapter 26 left you"** (a recap table, more keys, how backslash continuations are printed, what's new). Next is **§34.1 "Setting up for this chapter"** (WSL install in five steps from Microsoft Learn, `bash` on macOS, building the practice folder in `~/ch34`). Then come **§34.2 Pipes, redirection, and exit codes** and **§34.3 Looking inside files, and finding them**. §34.4–34.9 keep their numbers, so Ch 28/29/32's references (§34.6 PATH, §34.9 localhost) still resolve. RJ-S1-11 is done: the body no longer treats Ch 29 as finished (self-contained `test -f` exit codes, status codes explained in place, the Ch 29 mock-API Try-it removed; Ch 29 appears only as forward pointers).

Other changes:
- awk is split into four run cells, with the NR/FNR bug explained.
- Figure 34.2's count is now 16.
- The log is regenerated: empty days are WARNINGs and there is one real ERROR.
- The generator writes LF line endings (header 123 bytes) and 644 data files.
- The SSH section gains a practice-server setup, a real `ssh-keygen` transcript, a `~/.ssh/config` created by the reader, and the rsync trailing-slash rule with a real dry run.
- `fetch_daily.sh` is printed in full with How it works, after mini-demos of `sha256sum`/`gzip`/`zcat`/`date`.
- The disk story's numbers are recomputed (84 files since 10 Nov; 52 deleted, 21G; disk 48%) and its commands explained.
- `LINES` becomes `ORDER_LINES`, and the output format is "order lines 7, customers 3".
- macOS/WSL notes; wrong chapter pointers (52, 77, pandas 18); drafting leftovers removed.

**Figures.** All four were redrawn at 700 px (min 7.4 pt). 34.1 is now "channels + exit code" (the anatomy half moved to Fig 26.1). 34.3's leaders no longer cross their labels.

**Skipped / open.** 34.2, 34.12, 34.15, 34.19 and 34.20 are held (reading order). The just-in-time part of 34.2 (no Ch 6) and the correctness half of 34.12 (`.env` loading) were applied anyway, because tests 1 and 5 forced them (see questions). The title change ("Part 2") was not made.

**Option picks.** 34.8 → (a) regenerate the log. 34.17(b) → keep 84 files and explain them (switched on 10 Nov). 34.23 → the generator writes LF. 34.27 → a label format with no plural problem. 34.31 → measured (~8.6× on the practice CSV).

**Time needed:** 10–14 h → **9–12 h**, three sittings.

**Verification.** `checks/ch34_run.sh SCRATCH` runs the chapter as a user `meera` in a private mount namespace (passwd overlay, clean env, umask 002, private /tmp). It uses `checks/ch34_shell_session.py`, which handles `\` continuations, keeps `$?` across commands, and ignores `ls -l` dates. The result: **113 commands, 113 outputs checked, 0 mismatches**, plus `ch34_check.py` 27 checks passed. The SSH blocks that need a server are `run: none`; their outputs are either the author's earlier real run (unchanged paths) or, for `ssh-keygen`, a real run saved in `checks/ch34_keygen_transcript.txt`. The stock `tools/verify_shell.py` doesn't suit this chapter (it expects `--user meera` and `/home/meera`, and hangs on the background server). Build: 41 pages, layout_check clean (map 16/16).
