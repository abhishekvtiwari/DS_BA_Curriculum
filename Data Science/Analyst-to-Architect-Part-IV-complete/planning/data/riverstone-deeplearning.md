# Data spec: Chapter 43 deep learning assets (`riverstone-deeplearning`)

**Built by:** Part IV (first used in Chapter 43). No new Riverstone dataset.

## What Chapter 43 uses
- **Tabular network:** Chapter 37's `companion/accounts/accounts.csv` and identical preprocessing pipeline (same `CATS`/`NUMS`, same train/valid/test split, `random_state=37`), so results compare directly against Chapter 37's logistic regression and gradient-boosting numbers.
- **Image classifier and transfer learning:** scikit-learn's bundled `load_digits()` dataset (1,797 8×8 handwritten-digit images, 10 classes). No download, no external data, no seed needed beyond `random_state=43` for the train/test splits and `torch.manual_seed(43)` for model initialization. Digits 0–4 form the "base" task; digits 5–9 (relabeled 0–4) form the "new" task for transfer learning.

## Headline numbers
XOR: single neuron converges to log(2) ≈ 0.6931 (no better than guessing); a 4-neuron hidden layer reaches 0.00097. Tabular churn (validation AUC): logistic regression 0.764, small network (561 params) 0.773, tuned gradient boosting 0.788. Base CNN (digits 0–4, 675 training images): 98.7% test accuracy. Transfer vs. from-scratch on digits 5–9 (5 examples/class): 85.7% vs 94.2%; at 30 examples/class: 92.9% vs 98.2%; at the extremes (1 and 50 examples/class) the pattern is noisier at n=1 (58.9% vs 59.8%, effectively tied) and clearly favors from-scratch at n=50 (95.1% vs 98.2%).

## Why no new dataset was needed
The chapter's purpose is method (how a neuron, a layer, backpropagation, a CNN, and transfer learning work), not a new business question — reusing Chapter 37's churn data for the tabular comparison keeps the "deep learning vs. Chapter 37 methods" comparison honest and directly comparable, and `load_digits()` gives a real, tiny, fully offline image dataset for the CNN and transfer-learning sections without requiring internet access to download pretrained weights (torchvision's pretrained models need `download.pytorch.org`, outside this environment's allowed network domains).

## Environment note for the coordinator
PyTorch 2.14.0 (CPU-compatible; installed via plain `pip install torch`, not the `--index-url download.pytorch.org` CPU wheel, which is unreachable from this network's allowed domains). Everything in the chapter trains in well under a minute total on one CPU core.
