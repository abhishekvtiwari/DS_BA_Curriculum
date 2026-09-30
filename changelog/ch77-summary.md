# Ch 77 summary: Data Engineering & Data System Design Bank

**Rows:** 29 content (77.1–77.29) and 13 visual (V77.1–V77.13). All 29 content rows applied, plus V77.1 and V77.11; the other 11 visual rows were done by the style pass and were rechecked in the rebuilt PDF. Nothing was skipped. Details are in `changelog/ch77.md`.

## What changed

- **Opening.** The drafting note ("since this chat doesn't have Part 5's approved text") is gone. The opening is now a "Chapter at a glance" box like Ch 70, 72A and 76A. It has Before you start, a new Time needed line, How this chapter is built ("other question banks in Part 8, Chapters 70 onward"), and Levels and roles.
- **Pointers.** Every core question and every rapid-fire row now names the exact chapter and section. They were checked against the current files of Part 5 (rebuilt), Ch 12, 14, 16, 20, 28, 32, 33, 36, 47, 61, 70, 71 (renumbered) and 72A. Examples of what was wrong: SCD pointed to Ch 16, but it is taught in Ch 28 §28.10. §70.9 doesn't exist. Q71-023 and Q71-053 are now Q71-041 and Q71-015. Ch 72A doesn't teach topological sort.
- **Code, taught like Jupyter.** There are now 22 code blocks, each shown with its real output:
  - **Upsert (Q77-007):** a primary key, then the upsert run twice with a count after, then what happens with no key (the real ERROR).
  - **SCD Type 2 (Q77-013):** uses the real Harbour Traders change from `customer_changes`. It adds a surrogate key, a transaction and half-open dates, and shows there is no gap.
  - **Topological sort (Q77-018):** built with Kahn's algorithm in seven cells, including a cycle check.
  - **Partitioning (Q77-023):** the new syntax is explained. The load is shown, rows are routed to their partitions, the plan is shown after ANALYZE, and a what-if plan shows a query with no partition key scanning both partitions.
- **Answers.**
  - The Passes tier is now a partly-right answer, not the red flag.
  - Exactly-once now covers the transactional route too.
  - The sensor and partition bridges link these answers to how Ch 46, 48 and 50 use the same words.
  - Backpressure is linked to consumer lag. The heartbeat has its own name.
  - Watermark and write–audit–publish are named.
  - The baseline edge case is added.
  - Q77-034 now says "plant machines", as in Ch 50 §50.8.
- **Tags.** The tags are Ch 69's twelve, written [+Tag]. The IDs Q77-001…035 are unchanged.

## Option picks

- **77.4:** option (a), topological sort taught in this chapter. No option was marked recommended.
- **77.16:** option (a), a junk-dimension note in Ch 28 §28.9. It goes to the integrator with exact text, and Q77-017 points to it.

## Time needed

New: 3–4 hours for a first pass, plus 1 hour for the final-week list. The chapter had no Time needed line before.

## Verification

- `verify_sql.py`: 15 statements run, 8 outputs checked, 0 mismatches. It ran against a private copy of the lab database so it wouldn't collide with other agents; the chapter's hidden setup block follows Ch 71's pattern.
- `verify_python.py`: 7 blocks, 7 outputs, 0 mismatches.
- `checks/ch77_check.py`: 4 of 4 OK. It checks ₹20,900 on 5 Jan 2025, the Harbour Traders change, 4 statuses × 2 = 8, and 50 − 3 = 47.
- `restructure.py --check`: "already in order".
- `fig_check`: no figures.
- Build: 25 pages. `layout_check` is clean: map 10/10, `toc_wrong` empty, no stranded headings or lead-ins, no sparse pages, no small text, tofu 0.
- `prescan`: no draft labels. Its hyphen breaks all fall on real hyphens.
