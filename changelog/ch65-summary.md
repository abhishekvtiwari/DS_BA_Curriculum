# Chapter 65 summary — FinOps: The Economics of Data Platforms

**What changed.** The chapter's cost model is rebuilt from prices actually checked (AWS's Mumbai price list, 29 Sep 2026) and from volumes the earlier chapters establish. Three wrong inputs drove most findings: the monthly order-line volume (17,417 was three years' lines ÷ 12; 2025 has 87,011, 7,251 a month, now counted by a SQL cell), the t3.large price ($0.052 → $0.0896), and a sensor archive 40× Chapter 49's estimate (now Ch 49's 277 GB rollout, 68.3 GB hot / 208.7 GB Glacier Flexible Retrieval). LLM lines now use Ch 57's metered PO-intake cost (1,120 emails) and Ch 55's per-question cost.

New bill: **₹37,780 a month** (was ₹38,014; ₹4,53,360 a year). Warehouse 66.7%, LLM APIs 0.6%, all AI 15.6%. Fully-loaded **₹5,210.38 per 1,000 order lines, 10,421× Chapter 60's ₹0.50** (was 4,365×). New marginal-cost cell: **₹12 per 1,000 lines** (24× the target), so the story now says the ₹0.50 was neither cost, just unpriced. Corrected NFR: under ₹6,000 fully loaded (measured ₹5,210), under ₹15 marginal (measured ₹12).

Teaching added: an AWS-bill glossary box, a ten-line table of quantity × unit price, §65.2 split into four explained cells, "Where the volume comes from", "A unit cost by hand, then in pandas" (allocation rules, volumes, unit costs, a derived Flash cost), a showback `groupby`, a reserved-pricing cell with real rates, a price sheet with sources, "What this bill leaves out". All three figures redrawn with ₹ and ≥ 7 pt text.

**Skipped / not applied.** Nothing left Open. Kept, but raised as questions: the book's exchange rate (₹83/₹87/₹88), the invented 800 GB of warehouse storage (the real database is 45 MB), and treating Ch 49's hypothetical rollout as the archive.

**Option picks.** 65.1 (a) (two instances; not marked recommended); 65.4 (a); 65.6 (a); 65.7 (a); 65.16 `isin`; V65.3 dot plot.

**Time needed.** 8–10 h → 9–11 h.

**Verification.** verify_python 11 blocks, 11 outputs, 0 mismatches (cwd companion/ch65); verify_sql 1/1 (riverstone_full); check_code_teaching 0 findings; restructure --check in order; fig_check 0 under 7 pt (65.1/65.2 are matplotlib paths, checked by eye at 110 dpi); checks/ch65_numbers.py ALL OK (68 numbers); layout_check clean (25 pp, map 11/11, no stranded heads, no sparse pages, tofu 0; `v1.0` flag is the price-list URL).

**Other chapters affected** (for the integrator): Ch 66 (₹38,014/₹4,56,168 → ₹37,780/₹4,53,360, incl. its companion and chart) and Ch 67 (₹4,56,168; "4,400 times" → "about 10,000 times").
