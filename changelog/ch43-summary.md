# Chapter 43 — A First Look at Deep Learning: summary

**Findings handled:** 33 content, 10 visual, 1 reader-journey (RJ-S3-47, Ch 43 part). 42 Verified, 2 Fixed (43.31 checked and kept; RJ-S3-47). None skipped.

## What changed
- **New §43.0 Setting up.** PyTorch is installed just in time (`python -m pip install torch`; Linux/WSL adds the CPU-only `--index-url`), checked (`2.14.0`, GPU `False` is expected), and the first tensor is compared with a NumPy array. 32-bit numbers are introduced here, so later float32 tails make sense.
- **§43.1** now covers tanh next to ReLU and the sigmoid, and has a short cell on activation slopes that defines the vanishing gradient. The Sharma example gives its units and says the weights are made up.
- **§43.2** is taught one cell at a time: build, forward pass, BCELoss = log loss, one SGD step shown with the weights before and after, then the loop. A new Figure 43.1 shows XOR. A same-seed ReLU run (loss 0.3467, one dead neuron) shows why this toy uses tanh.
- **§43.3–43.4.** Figure 43.2 shows the 2-2-1 network. The promised backward pass is now done by hand with the chain rule (tied to Ch 35 §35.4) and matches autograd. The nudge is shown in 32-bit (−0.13500) and 64-bit (−0.13519939), and the gap is now explained correctly as float32 rounding.
- **§43.5.** Ch 37's preparation is split and labelled. The network is taught in four cells (shapes and `unsqueeze`, the model with its parameter count, the loss and Adam, and the training loop), and epoch, logit and `no_grad` are defined. The comparison is now worded as a tie with logistic regression and a gap to boosting (0.764 / 0.773 / 0.786 on validation). A new test-set-once cell gives 0.797 / 0.818 / 0.821. The blanket warnings filter is gone.
- **§43.6.** `np.unique` replaces the NumPy-2 label print. The full 6×6 feature map is computed and interpreted, with a new Figure 43.3. Pooling and feature map are defined. The CNN class is explained against Ch 29 §29.5 (inheritance, `super().__init__()`). New cells cover a shape trace, the parameter table, and multi-class output (logits, softmax, argmax, CrossEntropyLoss). A box links learned features to Ch 41's embeddings.
- **§43.7.** One transfer run is walked through first. The comparison is now controlled: the same sample goes to both methods, each is seeded, and each size runs over 5 seeds with mean and range. **The honest result changed:** training from scratch is ahead at every size, by 2–3 points. The old single-draw table (transfer ahead at n=3) was noise. Fine-tuning is defined.
- **Apply to Next.** The garbled Common-mistakes row is split in two. The real-world story no longer uses a vendor (RJ-S3-47): it's Vikram's own "should we upgrade?" question. Tools lists real versions and the run date. The Recap, Key terms and Check yourself are brought in line. Answers 5, 7, 8, 10, 11, 12 and 13 were rewritten from new runs (Ex 12 now has a from-scratch baseline and both bases on the same samples). The answer-heading leftover is removed, and Ch 53's title is fixed.

## Option picks
43.4: option (a), build in float64 (the 32-bit run is kept alongside to show the gap). All others used the change as described in the finding.

## Time needed
It was 8–12 h. It is now **12–15 h over two weeks, in three sittings** (≈5 h + 4 h + 4 h, plus exercises), because of the new setup section, the hand backward pass, and the cell-by-cell teaching. This matches the review's own estimate.

## Verification
- `tools/verify_python.py` from `companion/ch43`, with `OMP_NUM_THREADS=1`: **51 blocks run, 51 outputs checked, 0 mismatches.** With 4 threads, one long run (answer 8, epochs ≥ 350) differs in the last digit. Tools says so.
- `checks/ch43_check.py` (rewritten: runs the chapter cells, checks 38 prose numbers, writes the figure data): all pass.
- `restructure.py --check`: in order. `fig_check`: 0 figures under 7 pt (minimum 7.4 pt).
- Build: 50 pages. layout_check: no stranded heads or lead-ins, no sparse pages, no small text or tofu, map numbers 15/15. prescan: clean.
- `check_code_teaching`: remaining flags are Ch 37's re-used data cell (column names) and the 31-line `train_transfer`/`train_scratch` cell. That cell wraps code already taught one step at a time just above it, so it's a deliberate exception.
