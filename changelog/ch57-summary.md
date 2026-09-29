# Chapter 57, LLMOps: summary

**Findings:** 50 rows (35 content, 13 visual, RJ-S2-21, RJ-S3-61). All applied; none left Open. 13 already done by the style pass were checked in the rebuilt PDF.

## What changed
- **The machinery is now built, not imported.** New §57.0 (files, paths, what the stand-in provider does). §57.2 builds the prompt registry as data, `build_prompt` and `evaluate`; §57.5 the `Meter` and its price table; §57.6 the `Cache`; §57.8 `call_with_fallback` and shows the stand-in's failure rule. `pipeline.py`/`provider.py` hold exactly this code.
- **Consistent with Ch 54 (re-run on its new mock).** The three prompts, `parse` and `mark` come from `companion/ch54/extraction.py`, so the scores are Ch 54's: 13 (3 unparseable) → 35 → 47 of 60. Tokens per call (180 in / 53 out) match Ch 54's answer 13.
- **Provider change (§57.4).** Model names `workhorse-001`/`-002`/`volume-001`. The new version writes a comment line inside its JSON and some day-first dates: 0 of 60 with Ch 54's parse, 47 with `tolerant_parse` (Ch 54's parse after dropping comment lines, then `normalize_date`). The fence bug is gone.
- **Honest numbers.** Golden-set run ₹4.71 (worked by hand at ₹88/$); month forecast ₹88 (22 working days), ceiling ₹283; cache on a real day 17% (was "81% on a realistic day"); support questions 28% a week; fallback 44/13/3 through 41 errors, reconciled.
- **Story (In the real world)** moved to the assisted pilot's draft run (RJ-S2-21), caused by a retired pin falling through to an alias (57.25, option b), 52 emails, four process lessons including "the run should have failed".
- **Figures** redrawn at print width (min 7.3 pt), numbers computed by `make_figs57.py` from the companion; Fig 57.3 as two panels; file names match captions.
- Cross-references fixed (Ch 79 §79.7, Ch 64 title, Ch 45 §45.5, Ch 28 regex); ₹ everywhere; Appendix G note removed.

## Option picks
57.3 (a) · 57.5 recommended names · 57.25 (b) (Ch 54's story was already rewritten to a pinning story) · V57.2 separate panel (no dual axis) · V57.9 (a) ₹ · 57.6 fixed with Ch 54's brace parser instead of the finding's regex.

## Skipped
Nothing. Rate ₹88/$ kept pending the fact-sheet decision (P-M1 proposes ₹87); one constant to change.

## Time needed
14–18 h → **16–20 h**, in three sittings (§57.0–57.4, §57.5–57.8, §57.9–57.11 + project): about fifteen new cells.

## Verification
verify_python: 30 blocks, 27 outputs, **0 mismatches**; verify_shell: 3 commands, 0 mismatches; checks/ch57_check.py 18/18; fig_check 0 under 7 pt; restructure "already in order"; layout_check: map 18/18, no stranded heads/lead-ins, no sparse pages, tofu 0 (draft_labels are reader text: prompt status "draft", "drafts", "coordinator").
