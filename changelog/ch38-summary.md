# Chapter 38, Unsupervised Learning: summary

**Rows handled:** 59. There are 41 content rows, 17 visual rows and one Reader's Journey row. 58 are Verified, and RJ-S3-46 stays Approved because its remaining fix is in the fact sheet. No row is left Open.

## What changed

- **Setting up (38.1).** §38.0 now opens with the terminal steps: go to `companion/ch38`, run both generators, and `python -m pip install umap-learn mlxtend`. The notebook comes next. It also has a data dictionary for the seven features, which states the four categories and the 365-day cap.
- **By-hand steps added, as the review asked:**
  - the full k-means step-1 distance table and inertia;
  - k-means in NumPy as a plain loop first, then broadcasting with its (6, 2, 2) shape;
  - the silhouette for one account, then `silhouette_samples`;
  - two ARI demos;
  - single-linkage merging of the six accounts, with a new dendrogram figure and SciPy's `linkage`;
  - DBSCAN core, border and noise points on a line;
  - an isolation forest on five values;
  - Apriori pruning on five baskets, checked with mlxtend.
- **The drawing code is now shown** for the dendrogram, the k-distance curve and the PCA/t-SNE/UMAP panels. The PCA loadings are printed and read: PC1 is size and activity, PC2 is tenure.
- **The judgements are now measured:**
  - stability for k = 2 to 6: k = 5 is unstable, and the others can't be told apart, so k = 4 is stated as a business choice;
  - growth by cluster, which supports keeping "Growing regulars" (+10.7%);
  - a three-number rule a rep can apply: a depth-3 tree agrees with the clusters for 90.4% of accounts;
  - DBSCAN cluster sizes, with `min_samples` = 14 chosen from a k-distance plot.
- **Corrections:**
  - which raw columns dominate distance (recency, then tenure);
  - the drum-and-tap claim (now "7 in 10");
  - the story's churn comparison;
  - five cross-references;
  - `np.sort(axis=0)` replaced by a row-safe `argsort`;
  - `contamination` explained correctly;
  - the silhouette rule of thumb now attributed (Kaufman and Rousseeuw).
- **Two checkpoints**, after §38.3 and after §38.8, with answers.
- **Reader-facing polish:**
  - the Appendix G note and the planning file are gone;
  - the basket files now have a data dictionary;
  - Key terms list only what is taught;
  - Chapter 54 replaces a false reference to Chapters 55 and 58.
- **Basket data.** The shared generator was not reproducible: set order depends on Python's hash seed. The chapter now uses the one-line fix (`sorted(basket)`) and was fully re-run: 34,013 orders and 92,337 lines. The fix itself is for the integrator to apply.
- **Figures.** All six were redrawn in the book's style, with every text at 7.1 pt or more. The six-account dendrogram (38.3) and the k-distance curve (38.5) are new. The old dendrogram is now 38.4 and the projections are 38.6.
  - Figure 38.1 is two stacked panels instead of a dual axis.
  - The clusters use one colour and one marker shape each, in every figure.
  - The dendrogram's branches are coloured like their main k-means cluster.
- **Layout.** All pandas and mlxtend outputs fit the block (92 characters at most). Rupee amounts in lakh grouping.

## Option picks

38.5 used A (loop first). 38.13, 38.19, 38.32 and 38.39 used (a): measure growth, `min_samples` = 14, add the tree rule, and trim Key terms. 38.17 dropped `AgglomerativeClustering` from Tools. 38.26 defined Davies–Bouldin. The optional extras in 38.25 (a held-out AUC) and 38.33 (the SQL query) were not added.

## Skipped, and why

Nothing was skipped. RJ-S3-46 needs no Ch 38 edit: the agency is unnamed and isn't a person, and the name list belongs to the fact sheet, which is not approved yet.

## Time needed

It was **8–12 hours**; it is now **11–14 hours over two weeks**. The by-hand steps, two new figures, the extra cells and the checkpoints add about 3 hours. The PDF went from 33 to 50 pages.

## Verification

- `verify_python.py`: 48 blocks run, 46 outputs checked, **0 mismatches**. It was run twice, with PYTHONHASHSEED 1 and 99: set and frozenset outputs are printed sorted, and tied rules are sorted by name.
- `checks/ch38_check.py`: all checks pass. It now covers the new hand examples, the checkpoints, stability, growth, the tree rule, DBSCAN and the new basket numbers.
- `verify_shell.py`: nothing to run (the setup block is `run: none`).
- `fig_check`: 0 figures under 7 pt.
- `layout_check`: no stranded heads or lead-ins, no sparse pages, no small text, tofu 0, map 16/16.
- `restructure --check`: in order.
- `check_code_teaching`: 3 flags remain, all in Answers 7–9. They reuse ideas already taught in the body, and I left them as deliberate exceptions.
