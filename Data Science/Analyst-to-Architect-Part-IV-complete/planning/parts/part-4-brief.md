# Part Brief — Part IV — Machine Learning & Data Science

Read `planning/chapter-writing-instructions.md` first. This brief adds what is specific to this part. Status and reports for this part go in `planning/parts/part-4-status.md` (instructions, section 14.1).

## Scope

This chat writes **Chapters 35–44**.

## Chapters

| ID | No. | Title | Class | Blueprint words | Status | Manuscript file |
|---|---|---|---|---|---|---|
| P4-35 | 35 | The Math Under the Models | B | 6,000 | Not started | `manuscript/ch35-the-math-under-the-models.md` |
| P4-36 | 36 | The Machine Learning Workflow & Feature Engineering | B | 5,000 | Not started | `manuscript/ch36-the-machine-learning-workflow-and-feature-engineering.md` |
| P4-37 | 37 | Supervised Learning Algorithms | B | 8,000 | Not started | `manuscript/ch37-supervised-learning-algorithms.md` |
| P4-38 | 38 | Unsupervised Learning | B | 4,500 | Not started | `manuscript/ch38-unsupervised-learning.md` |
| P4-39 | 39 | Evaluation, Tuning, Interpretation & Honesty | B | 5,500 | Not started | `manuscript/ch39-evaluation-tuning-interpretation-and-honesty.md` |
| P4-40 | 40 | Time Series & Forecasting | B | 6,000 | Not started | `manuscript/ch40-time-series-and-forecasting.md` |
| P4-41 | 41 | NLP Foundations | B | 4,000 | Not started | `manuscript/ch41-nlp-foundations.md` |
| P4-42 | 42 | Recommender Systems & Ranking | B | 3,500 | Not started | `manuscript/ch42-recommender-systems-and-ranking.md` |
| P4-43 | 43 | A First Look at Deep Learning | B | 4,500 | Not started | `manuscript/ch43-a-first-look-at-deep-learning.md` |
| P4-44 | 44 | Capstone: An End-to-End Data Science Project | D | 2,500 | Not started | `manuscript/ch44-capstone-an-end-to-end-data-science-project.md` |

## Reference chapters for this part

Chapter 13 (class B) and Chapter 2 (measured demonstrations). Capstone Chapter 44 is class D.

## Guidance specific to this part

- **Assumes Parts II–III**, especially Python (17–18) and statistics (21–22, 30).
- **Datasets:** this part is the first user of several blueprint domains (CRM leads for lead scoring and churn, sensor time series for forecasting, support tickets for NLP, digital events for recommenders). Build each as a seeded generator with planted signal and realistic noise, consistent with Riverstone's customers and products, and register the data specs (instructions, section 14.4). Keep datasets small enough to train in minutes on a laptop.
- **Every metric, plot, and table comes from a real, seeded run** (`random_state` fixed everywhere; library versions recorded). Show honest results, including models that don't beat a simple baseline; Chapter 39 is about honesty in evaluation.
- **Math (Chapter 35)** is explained with worked numbers first, notation second.
- **Deep learning (Chapter 43)** should run on CPU in minutes; say so.
- **Fast-changing facts** (library APIs, model families) are verified against official documentation.

## Sequencing and dependencies

Start after Part II Chapters 17–18 and 21–22 are written (read them for vocabulary).

## Blueprint scope for each chapter (verbatim)

Deliver at least this scope. If something important is missing or wrong, propose the change (instructions, section 13).

**Ch 35. The Math Under the Models** · EXPANDED from draft Ch 15 · 6,000 words
Now with formulas and worked numbers: vectors, dot product, matrices · derivatives and gradients · gradient descent computed by hand for three steps, then in NumPy · probability distributions, likelihood, maximum likelihood · entropy and cross-entropy · PCA worked on a small example.
*Project:* Gradient descent and PCA from scratch.

**Ch 36. The Machine Learning Workflow & Feature Engineering** · NEW (splits draft Ch 16) · 5,000 words
Framing problems · train/validation/test splits and cross-validation · data leakage with real examples · feature engineering: scaling, encoding categoricals, dates, text, aggregates · missing values in ML · scikit-learn pipelines · baselines.
*Project:* A leakage-free feature pipeline for Riverstone lead scoring.

**Ch 37. Supervised Learning Algorithms** · EXPANDED from draft Ch 16 · 8,000 words
How each algorithm works, when to use it, key settings: linear regression, regularization (ridge, lasso, elastic net), logistic regression, k-nearest neighbors, Naive Bayes, decision trees (Gini, entropy, worked split), random forests, gradient boosting (XGBoost, LightGBM, CatBoost), support vector machines · bias–variance with learning curves · hyperparameter tuning.
*Project:* Lead-scoring model: baseline vs boosting.

**Ch 38. Unsupervised Learning** · NEW (splits draft Ch 16) · 4,500 words
k-means step by step, choosing k · hierarchical clustering · DBSCAN · dimensionality reduction: PCA, t-SNE, UMAP · anomaly detection (isolation forest) · market basket analysis (association rules) · evaluating unsupervised results.
*Project:* Customer segmentation and a product-bundle analysis.

**Ch 39. Evaluation, Tuning, Interpretation & Honesty** · EXPANDED from draft Ch 17 · 5,500 words
Confusion matrix with formulas and worked numbers · precision, recall, F1, ROC-AUC, PR-AUC · regression metrics · calibration · threshold selection by business cost (worked) · imbalanced data (class weights, resampling, SMOTE) · SHAP and partial dependence · fairness checks · model cards.
*Project:* Cost-based evaluation and explanation of the lead-scoring model.

**Ch 40. Time Series & Forecasting** · NEW · 6,000 words
Trend, seasonality, cycles, noise · stationarity · moving averages and exponential smoothing · ARIMA/SARIMA intuition and practice · forecasting libraries · machine learning for forecasting (lag features) · backtesting · forecast accuracy (MAPE, WAPE) · demand forecasting for a manufacturer · anomaly detection in sensor data.
*Project:* Forecast Riverstone's monthly demand by product category.

**Ch 41. NLP Foundations** · NEW · 4,000 words
Text as data · cleaning and tokenization · bag of words, TF-IDF · sentiment analysis · text classification · topic modeling · word embeddings as the bridge to LLMs.
*Project:* Classify and summarize Riverstone support tickets by topic.

**Ch 42. Recommender Systems & Ranking** · NEW · 3,500 words
Popularity baselines · content-based filtering · collaborative filtering and matrix factorization (intuition) · implicit feedback · evaluation (precision@k, NDCG) · cold start · business uses in B2B cross-selling.
*Project:* "Customers who bought this also bought" for Riverstone.

**Ch 43. A First Look at Deep Learning** · EXPANDED from draft Ch 18 · 4,500 words
Kept structure; added a neuron computed by hand, a small network in PyTorch with full code, and a transfer-learning walk-through.

**Ch 44. Capstone: An End-to-End Data Science Project** · NEW · 2,500 words
From business question to validated, explained, documented model, presented to non-technical leaders.

## Promises already made to these chapters

Generated from the approved and written chapters (Chapters 1, 2, 12, 13) by `tools/extract_promises.py`. Each line is something a reader has already been told your chapter will do. Deliver it, or report that it can't be delivered.

#### Chapter 41

- *(from Ch 1)* | Unstructured | emails, PDFs, images, audio, free-text reviews | Chapters 41, 55, and 58 |

## Kickoff prompt

```
You are writing Part IV — Machine Learning & Data Science of the book "Analyst to Architect" (Chapters 35–44).
1. Read planning/chapter-writing-instructions.md in full, then this brief (planning/parts/part-4-brief.md),
   planning/chapter-map.md, the relevant sections of planning/blueprint.md, and
   planning/promises-from-approved-chapters.md.
2. Read the reference chapter(s) named in this brief for the depth class of your first chapter.
3. Copy tools/ from the project into your workspace and set up what this part needs (instructions, section 9).
4. Create planning/parts/part-4-status.md and start with the first unwritten chapter: send me your plan
   (instructions, section 12, step 2), then write, verify, build the PDF, save to the project, and report.
5. Continue chapter by chapter, in order. Never edit files owned by the coordinator or other parts.
```
