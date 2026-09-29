# Chapter 49 summary: Storage, Warehouses & Lakehouses

**Rows:** 43 Approved rows for Ch 49 (38 content, 5 visual) → all 43 **Verified** (code by `verify_python`, 0 mismatches; text and figures in the rebuilt PDF). 12 visual rows were already Fixed/Verified by the style pass and re-checked. RJ-S2-18 (multi-chapter, `Open`) left untouched.

## What changed
- **New §49.0 Setting up:** practice folder `work/ch49`, `python -m pip install deltalake==1.6.6` (one install line everywhere, 49.38), notebook, first cell with each import explained (49.12). "Rust" dropped (49.36).
- **§49.1:** "Object storage in five sentences" (bucket, object, key, whole-object operations, network calls, the three services) (49.8).
- **§49.2:** the dense first cell split into small cells with line-by-line notes (49.12–49.14); SQLite introduced in its own cell; new "The same test across formats, with timing": a `time.perf_counter` cell and a five-format table from a new companion script `format_test.py` (49.7, parked Ch 2 Block 2 landed).
- **§49.3:** hand-worked "Two layers of shrinking" box (dictionary, run-length, bit-packing; codecs defined) (49.6); metadata code split into four cells, printing encodings, sizes before/after compression and distinct counts; the wrong claims fixed (temperature_c "every value differs" → 4,729 distinct values, 13-bit codes; "0.80 MB on disk" → 0.80 MB before compression, 0.69 MB on disk) (49.4, 49.5, 49.15); row-group knob, codec/splitting and sorted-file notes (49.16–49.18).
- **§49.4:** Consistency row corrected, Ch 12 reference corrected, what table formats do and don't guarantee (49.9, 49.10).
- **§49.5:** every cell split and explained (49.19–49.22, 49.24); raw log shown; optimistic concurrency paragraph (49.11); new Restore and Vacuum cells (49.23); schema error shown before `schema_mode="merge"`, NULLs shown; compaction now uses 24 distinct hourly appends (1.41 MB → 0.82 MB, not the duplicate-driven 2.73 → 0.53) with sizes read from the log (49.3, 49.25, 49.26); new "Iceberg in one page" (49.35).
- **§49.6:** partitioned-write cell (49.28); small-table rule: Riverstone partitions by month (49.29, also §49.9, Answer 10, Project step 2).
- **§49.7:** plain-word glosses for warehouse product terms (49.30).
- **§49.8:** cost estimate rebuilt as two code cells: honest scenario (1,460 sensors at 1/s → 126 M readings a day → 277 GB/yr; today 0.47 GB/yr), current prices with dated sources, $6.37/month storage, $0.030 vs $1.58 a scan, ratio 52 (49.1, 49.2, 49.32, 49.33).
- **Figures 49.1 and 49.2 redrawn** (760 px canvas, min 7.46 pt; 49.1 with a key and cross/tick icons; 49.2 now shows the four versions the code builds, arrows to the files each adds) (49.27, 49.37, V49.3, V49.4, V49.5, V49.15).
- Exercises 7, 9, 10, 12 and Answers 3, 4, 7, 8, 9, 10, 11, 12 updated; Appendix G note deleted (49.34, V49.18); Where this leads fixed (49.31); Recap, Key terms, Check yourself extended.

## Option picks
49.33 (a) $6.25 per TiB, recomputed · 49.35 (a) Iceberg half page · 49.5, 49.25, 49.26, 49.27, 49.30: the first option named.

## Deviations and things skipped
- **49.7:** the old Ch 2 table (500,000 sales lines, "two-processor cloud computer") couldn't be reproduced: no 500,000-line dataset exists in the book, and the parked note says to re-run before reusing the numbers. The test was re-run on the chapter's own sensor day (216,000 readings, 8 columns) with `format_test.py`. The pattern holds (Parquet smallest and about 9× faster than CSV; Excel about 73× slower than CSV; JSON largest). The gzip CSV is 1.8 MB, not 4.7 MB.
- **₹83 to the dollar** kept as written (exchange rate is a fact-sheet proposal; question raised).

## Prices (T13), checked 29 September 2026
Amazon S3 Standard, US East (N. Virginia), first 50 TB: $0.023 per GB-month (AWS Price List API, publication date 28 Sep 2026). BigQuery on-demand queries: $6.25 per TiB, first 1 TiB a month free (cloud.google.com/bigquery/pricing).

## Time needed
12–16 h → **14–17 h** (new setup, object-storage primer, encoding box, timing test, restore/vacuum/partition cells, Iceberg page: about +1.5 h, as the review estimated).

## Verification
`verify_python`: 32 blocks run, 32 outputs checked, **0 mismatches** (OMP_NUM_THREADS=1). `verify_shell`: nothing to run (the two terminal blocks are install commands, marked `run: none`). `check_code_teaching`: 34 blocks, 0 flagged. `checks/ch49_check.py`: all 28 checks pass. `restructure --check`: in order. `fig_check`: 0 under 7 pt. `layout_check`: 36 pages, map numbers 16/16, no stranded heads/lead-ins, no sparse pages, no small text, tofu 0.
