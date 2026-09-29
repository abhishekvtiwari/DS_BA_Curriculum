# Chapter 61, Distributed Systems & Trade-offs: summary

**Rows:** 26 content (61.1–61.26) and 15 visual (V61.1–V61.15), plus RJ-S2-26 and RJ-S3-78. All 26 content rows are fixed and checked in the rebuilt PDF. The 5 open visual rows (V61.1, V61.2, V61.3, V61.13, V61.14) are fixed; the 10 the style pass had done still pass. RJ-S2-26 stays **Open**: it needs the book-calendar proposal. RJ-S3-78 has nothing to change in Ch 61; its fix is in Ch 65.

## What changed

- **Precision.** Four ideas are now used correctly:
  - *Idempotent* is defined at first use (§61.2), with Ch 58's one-email-one-order key, and credited to the right chapters (45, 51, 58).
  - *Partitioning* (Ch 48/49) is told apart from *sharding*. Riverstone partitions; it doesn't shard.
  - The three meanings of *consistency* (ACID, CAP, freshness) get a Watch-out. Atomicity is separated from "strong".
  - *Snapshot* and *read-your-writes* are two rows.
- **Grounded in Parts 5–6.**
  - The warehouse is the DuckDB file plus the Delta archive; there are no read replicas.
  - Replication and load balancing use Ch 52's `replicas: 2` Flash page and its Service.
  - The cache saving is Ch 57's 17%, not 81%.
  - Bounded staleness uses Ch 47's "previous working day" (30.5 h Tuesday, 78.5 h Monday). The banner reads "as of 06:35".
  - Circuit breakers point to Ch 57 §57.8 (described there) and Ch 58.
  - The CRM story's credit-hold lookup is set up in §61.2. The sync follows Ch 51's design and Ch 46 §46.10's runbook, not ADR-026.
- **New teaching (61.15):** CP/AP, scaling up vs out, and "Who is in charge? Quorum and consensus" (W + R > N, leader election, Raft, anchored on Ch 50's KRaft folder).
- **Code (61.11/12/23):** the 27-line simulation is split into three cells plus a what-if cell (seed 1). Each has its real output and a line-by-line list. The prose now says "eleven" ticks.
- **Timed-challenge answers:** Level 3 and the Bonus now match real runs. More replicas can converge sooner at one seed. Dropping the *last* write never converges.
- **Visual:**
  - Figure 61.4 is now a real table, with a "Risk" column in words.
  - Figures 61.1–61.3 are redrawn at 740 px, all text ≥ 7.3 pt, with no label collisions.
  - Figure 61.3 gains a sixth card, "Scaling up or out".
- **Polish:** ₹2,000 (not "Rs"), and the Appendix G line is removed. Where this leads now points to Ch 80, Q80-001.
- **Companion:**
  - `eventual_consistency_sim.py` has the chapter's two functions, plus `--seed` and `--replicas`. The old version printed only 3 columns even with 5 replicas.
  - `failure-analysis-riverstone.md` is rewritten to match the table.
  - The worksheet gains a Risk column.

## Skipped, adapted, and why

- **RJ-S2-26 (story dated February 2026)** is left Open. The fix, moving Part 7 to 2027, is fact-sheet proposal P-T2, which isn't approved.
- **61.3 and 61.19** are adapted. The review suggested replicating the pipeline container, but current Ch 52 says a scheduled job must not be replicated (you'd get two Flashes). So the replication example is the Flash *page*, and the ingestion row says the scheduler "must stay one".
- **61.10:** the "weekly digest (Chapter 47)" wording was not used, because no such digest exists in Ch 47.
- **Story timing** is adapted. Ch 58 and the rebuilt Ch 60 run PO intake once, at 06:00, so the CRM outage now runs 11:40 p.m. to 6:10 a.m. (it was to 2:15 a.m.). Otherwise the intake pipeline could not have met it. This is flagged as a question.
- **Zoho** is kept in the story. Fact-sheet proposal C27 ("the CRM") isn't approved.

## Option picks

None offered.

## Time needed

10–12 h → **11–13 h**. The three explained code cells add about 30 min, and scaling plus quorum/consensus add about 30 min.

## Verification

- `verify_python.py`: 4 blocks run, 4 outputs checked, **0 mismatches** (Python 3.11).
- `check_code_teaching.py`: 4 blocks, 0 flagged.
- `restructure.py --check`: already in order.
- `fig_check.py`: 0 figures under 7 pt.
- The build has 26 pages. `layout_check.py` reports no stranded heads or lead-ins, no sparse pages, no small text, tofu 0, map numbers 13/13 and toc_wrong empty. The only `draft_labels` hit is "coordinator", which is reader text ("sales coordinator").
- The numbers in the answers come from `checks/ch61_convergence.py` and `checks/ch61_quorum.py`.
