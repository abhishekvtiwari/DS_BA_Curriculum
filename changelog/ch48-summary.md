# Chapter 48 — Big Data & Distributed Compute: summary

**Findings:** 31 content (48.1–48.31) and 3 open visual rows (V48.1–V48.3) applied; V48.4–V48.12 were already done by the layout pass and re-checked. RJ-S2-18 is `Open` in the register and was not touched.

## What changed
- **Setup, just in time (48.1):** a new §48.0 installs Java 21 (Windows, macOS, Linux), PySpark 4.2.0 and Polars 1.44.2 in the book's venv, generates the data, lists the Hive-style folders, starts the first SparkSession line by line, and has a troubleshooting box. It sits before §48.1, so no section number changed.
- **Polars taught before use (48.2):** "Polars in one page" opens §48.6: expressions, eager and lazy, `explain()`/`collect()`.
- **Plans through the public API (48.3, 48.4, 48.27, V48.3):** §48.4 shows raw `explain()` first; the optional `plan()` helper wraps `explain()` (no `_jdf`), keeps whole lines, and now prints the full PartitionFilters/PushedFilters the text reads.
- **Code taught like Jupyter (48.9–48.12, 48.14, 48.17, 48.19, 48.26):** big cells split; every new function explained; salting now runs with outputs and a correctness check (2,384,640 = 2,384,640); a Spark write cell added; a settings table added (what happens if you change it).
- **Timings (48.8, 48.15, 48.16):** the timing harness is shown; timings are in milliseconds from a shared 4-core test machine with every engine given two cores (DuckDB 213.0, Polars 262.3, Spark 1,211.8 ms on 19.87 M rows); Answer 8 recomputed (37×, 5.7×); the 8-core Try-it corrected.
- **Correctness (48.13, 48.18, 48.20–48.23, 48.30):** pruning on expressions over the partition column shown to work, and on `reading_ts` not to; file-size advice matches the 1.2 MB/day data; AQE "since 3.2"; small-files claim softened for AQE; story scaled to ~200 machines; "partitions by" in Ex 2; pushed-filter statistics claim corrected.
- **Polish and cross-references (48.6, 48.7, 48.24, 48.25, 48.28, 48.29, 48.31):** drafting leftovers gone; Where-this-leads no longer promises Spark in Ch 52/56; Ch 49 not a prerequisite; Spark UI moved into §48.5.
- **Figures (V48.1, V48.2):** both redrawn at 760 px (min 7.8 pt and 7.1 pt), with non-colour cues (solid vs dashed borders; text margin labels), arrows no longer strike labels; Fig 48.2 stacked and uses the real plan text.

## Skipped, and why
- Nothing Approved was skipped. Recording the Ch 40/48 dataset decision in `review/sequence-map.md` (part of 48.5) is not my file: it is under "For the integrator".
- The stretch idea in 48.5 (run Ch 40's rolling rule with a Spark window) was not added: Ch 40 already dropped the promise, and the generator has no `status` column.

## Option picks
- 48.5: the finding's recommendation (keep Ch 48's dataset; fix Ch 40, already done there). 48.22: the recommended first option (~200 machines).

## Time needed
12–16 h → **14–18 h**, over four sittings (setup 1–2 h; 48.1–48.4; 48.5–48.6; 48.7 on and the project).

## Code verification
- `verify_python --cwd companion/ch48`: 24 blocks run, 24 outputs checked, **0 mismatches** (run twice, with and without `JAVA_TOOL_OPTIONS`).
- `verify_shell --cwd companion/ch48`: 3 commands, **0 mismatches**.
- `check_code_teaching`: 30 blocks, 0 flagged. `checks/ch48_check.py`: all 12 checks pass.
- Not auto-verified: `java -version` (machine-specific; real output from the test machine), the two install commands, the timing cell (real run, times vary; marked run: none), Answer 9's one-liner.
- Build: 37 pages; layout_check clean (map 15/15, no stranded heads/lead-ins, no sparse pages, no small text, tofu 0); fig_check 0 under 7 pt; restructure "already in order".
