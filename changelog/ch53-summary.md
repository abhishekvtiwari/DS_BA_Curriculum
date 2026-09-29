# Chapter 53, Deep Learning in Depth: summary

**What changed.** The chapter now builds on Ch 43 instead of starting over, sets up its own data, and has an output behind every number it prints.

- **Setup first** (53.12): new §53.0 runs `generate_defect_images.py` in the terminal and shows its real output. It explains `.npy` files and loads them in the first cell.
- **Bridged to Ch 43** (53.2): §53.1 opens with what Ch 43 already did. Every reuse points to the Ch 43 section (float32, activations, chain rule, nudge check, Adam, `nn.Conv2d`, softmax, seeds).
- **The training step by hand, corrected and completed** (53.3–53.8): both wrong numbers are fixed (0.10 / −0.5, and neuron 1's sum of 0.2). New pieces: the chain rule worked on W2[0] (0.84 × 2.1 = 1.764), a nudge check, why this example uses squared error, and "Optimizers, one step by hand" (plain +0.6 against Adam +0.1, and +60 against +0.1 for a gradient 100 times larger).
- **Techniques shown, not listed** (53.9–53.11, 53.14): the scaling cell's comment and prose are corrected, and its ConvergenceWarning is shown and explained. Dropout, batch norm, He initialization and a step schedule are each worked in a cell, and weight decay is written out as `alpha`.
- **Convolution completed** (53.19): pooling by hand, loops and reshape, then stride and padding (the rule, confirmed in PyTorch).
- **The defect project, made honest** (53.13, 53.15–53.21, 53.25): one split of row numbers used everywhere. Early stopping is explained. The threshold is chosen on out-of-fold predictions for the training parts and the test set is scored once (same result as before: threshold 0.01, 116/119 caught, 46 false alarms, ₹13,840, against ₹40,080 at 0.5). The table prints accuracy, which is highest at the most expensive thresholds (the false "92% at every row" is gone).
- **New Attempt 3 in PyTorch** (53.30): a one-layer CNN learns 16 kernels, with mini-batches and its own validation split. Test cost is ₹4,200 at seed 53, and ₹4,480 / ₹8,080 / ₹16,240 at seeds 1–3, reported as a range.
- **Attention by hand** (53.26–53.28): raw scores are printed, *cracked·crate* = 1.24 is worked, softmax is worked by hand on one row, the 24-parameter count is given, and there is a new masking cell. Softmax is still built in §53.7.
- **Quantization matches the run** (53.29): the same 116 caught, 7 flips, 46 → 53 false alarms. Biases are left in 32-bit, and the text says so.
- **Answers and polish** (53.35–53.42): Exercise 10 is reworded. Answers 7, 9 and 10 are simplified. Answer 16 now says "which 99%?". Answers 8, 12 and 13 have real code and output, and Answer 8 has a new Figure 53.5 (PR curve). Cross-references are fixed (no Ch 19 or 38 for things they don't teach), titles are exact, and the Appendix G note is gone.
- **Figures** (53.33, V53.1–V53.3, V53.10–V53.12): all five are redrawn from `figures/make_figs53.py`, renumbered in reading order, at 7.1–9.2 pt. The cost chart and the PR curve are drawn from `checks/ch53_results.json`. The lids are the real 32×32 images at 10× nearest-neighbour. Arrows now show direction in Figure 53.1. The attention figure has a greyscale-safe ramp, and nothing depends on colour alone.

**Skipped, and why.** Nothing in Ch 53 was left undone. RJ-S2-24 and RJ-S3-58 are multi-chapter rows. Their Ch 53 part is done (the recall figure Ch 59 needs is printed; no authorial first person was found), and the rest belongs to Ch 59 and Ch 55 (see the questions file).

**Option picks.** 53.3: the finding's rewrite. 53.12: the setup box, as §53.0 (D8). 53.16: out-of-fold cross-validation for Attempt 2 and a three-way split for Attempt 3 (question raised). 53.22: (a), no chapter reference. 53.28: the optional cell included. 53.30: add the PyTorch listing (the finding's "better"). 53.31: (a), dropped from the reader list. 53.36: one split of row numbers. 53.41: add definitions. V53.10: 10× nearest-neighbour.

**Time needed.** 14–18 h → **17–20 h** over three weeks, in three sittings: §53.0–53.3 about 6 h; §53.4–53.6 about 6 h; §53.7–53.10 and the project about 5 h, plus the exercises. The chapter grew from about 12,300 to 20,500 words, much of it code and output.

**M.12.** "MLOps" appears only in the Part title and in "Where this leads", which now defines it.

**Verification.**
- `tools/verify_python.py` (Python 3.11, NumPy 2.4.6, scikit-learn 1.9.1, PyTorch 2.14.0, `OMP_NUM_THREADS=1`): 49 blocks run, 47 outputs checked, **0 mismatches**. `tools/verify_shell.py`: 2 commands, 0 mismatches (the generator's output was also checked byte for byte against a fresh run).
- `checks/ch53_check.py`: **49 checks pass**. They cover every number the prose states (hand arithmetic, CV table, test costs, the "two thirds", "1 in 12" and "1 in 8", 27,905 parameters, softmax by hand, quantization flips, answer figures), and the script writes the figure data.
- Build: 54 pages. `layout_check`: no stranded headings or lead-ins, no sparse pages, no small text, no clipped lists, no draft labels, tofu 0, map numbers 17/17. `prescan`: clean. `fig_check`: 0 figures under 7 pt. `restructure.py --check`: in order.
- `check_code_teaching.py`: 3 heuristic flags remain, all in Answers 7, 12 and 14. Each is explained in bullets and prose that reuse chapter code.
