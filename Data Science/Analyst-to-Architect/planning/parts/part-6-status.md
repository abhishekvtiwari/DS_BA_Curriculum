# Part VI — Status (Chapters 53–59)

Owner: Part VI chat (the same chat that wrote Part III). Instructions: `planning/chapter-writing-instructions.md` §14.1.
Last updated: 19 September 2026 — **Part VI complete: all seven chapters written and approved.**

## Chapters

| ID | No. | Title | Class | Status | Notes |
|---|---|---|---|---|---|
| P6-53 | 53 | Deep Learning in Depth | B | **Approved (v1), 19 Sep 2026** (~12.3k words) | `Ch53-Deep-Learning-in-Depth-v1-approved.pdf`, 36 pages |
| P6-54 | 54 | Generative AI & Large Language Models | B | **Approved (v1), 19 Sep 2026** (~11.4k words) | `Ch54-Generative-AI-and-LLMs-v1-approved.pdf`, 32 pages |
| P6-55 | 55 | Building AI Applications: RAG, Agents & Evaluation | B | **Approved (v1), 19 Sep 2026** (~10.7k words) | `Ch55-Building-AI-Applications-v1-approved.pdf`, 31 pages |
| P6-56 | 56 | MLOps: Making Models Survive Production | B | **Approved (v1), 19 Sep 2026** (~9.6k words) | `Ch56-MLOps-v1-approved.pdf`, 27 pages |
| P6-57 | 57 | LLMOps | B | **Approved (v1), 19 Sep 2026** (~8.7k words) | `Ch57-LLMOps-v1-approved.pdf`, 25 pages |
| P6-58 | 58 | Intelligent Automation | B | **Approved (v1), 19 Sep 2026** (~8.5k words) | `Ch58-Intelligent-Automation-v1-approved.pdf`, 25 pages |
| P6-59 | 59 | Industry Case Studies | C | **Approved (v1), 19 Sep 2026** (~5.0k words) | `Ch59-Industry-Case-Studies-v1-approved.pdf`, 14 pages |

## Environment constraints found (important for this part)

- **PyTorch cannot be installed here.** The PyPI wheel bundles CUDA libraries and needs about 3.5 GB; the container has ~2.7 GB free after clearing caches, and the CPU-only wheel index (download.pytorch.org) is outside the allowed domains. Chapter 53 therefore runs everything in **NumPy and scikit-learn 1.8.0**, which are installed, and shows PyTorch only as listings clearly marked as not run here. If the container gets more disk, those listings can be verified and the chapter reissued.
- **No model weights can be downloaded** (huggingface.co is not reachable), so Chapters 54, 55 and 57 cannot run a local open model. Plan, per the brief: **local mock servers and recorded responses, clearly labeled**, plus genuinely runnable components (tokenization, embeddings built locally with scikit-learn, vector search in NumPy, chunking, evaluation harnesses). The Anthropic API endpoint is reachable but needs a key, so no chapter will require one.
- **Sequencing:** the brief says to start after Part IV Chapters 36–39, which are not written. Chapter 53 assumes the blueprint's scope for them (train/test splits, overfitting, precision and recall, gradient boosting) and keeps every reference generic. **Assumptions to check against Part IV when it exists** are listed under Chapter 53 below.

## Chapter 59 report (approved v1)

**Structure:** how to read a case study · nine cases in one six-part frame (problem as stated, data, approach, architecture, result, what went wrong, lesson) · what the nine have in common · what changes by industry · how these projects actually start · common mistakes · recap · 2 figures. Class C: no exercises, no companion code, no practice data.

**The nine:** 1 manufacturing quality (Riverstone, Ch 53/56, measured) · 2 demand planning · 3 B2B lead scoring · 4 retail pricing · 5 banking fraud · 6 logistics routing · 7 customer support automation (Riverstone, Ch 55) · 8 predictive maintenance · 9 order-to-cash end to end (Riverstone, Ch 12/13/16/32/54/57/58, measured).

**Honesty decision, applied throughout:** the three Riverstone cases quote numbers measured in this book; the other six are labeled composites with representative numbers, and no real company is named or cited. Every case includes what went wrong, its cost, and the fix.

**The synthesis** (figure 59.2) is a grid of nine cases against five recurring patterns: the stated problem was the wrong one (8 of 9), data work dominated the schedule, the binding constraint was human attention, the failure was organizational, and the metric had to change. None is a modeling error.

**No verification applies** (no code blocks). Style checks clean; cross-references to Ch 5, 30, 31, 53, 55, 56, 57, 58, 75 and 79 all point at real chapters in the blueprint.

**Manual check needed:** none, beyond a read-through for consistency with the six chapters it summarizes.

## Chapter 58 report (approved v1)

**Sections:** 58.1 Three generations of automation · 58.2 What to automate · 58.3 The pipeline assembled · 58.4 Writing to a system of record · 58.5 The human in the loop · 58.6 Exceptions classified · 58.7 Measuring it honestly · 58.8 Rolling it out · 58.9 The people part · 58.10 When not to automate · full template · 18 exercises with answers · 3 figures.

**Pays off the promise made in Chapters 1 and 2** (the sales desk retyping purchase orders). New companion code: `erp.py` (a real SQLite order book with a UNIQUE idempotency key on the source email, transactional header-plus-lines writes, and an audit log) and `intake.py` (read, extract, parse, validate, decide, write, report).

**Measured results:**

| What | Number |
|---|---|
| Intake run, 60 emails | 53 loaded, 6 awaiting approval, 1 held; **88% straight through**; Rs 4.74 model cost |
| Replay of the same morning | 59 orders before and after; **59 duplicates ignored and logged** |
| Of the 53 auto-loaded orders | **43 correct, 10 silently wrong (19%)** |
| Approval limit sweep (Rs 0 / 50k / 100k / 200k) | 0 / 40 / 53 / 59 loaded; wrong value auto-loaded Rs 0 / 143,700 / 363,550 / 579,050 |
| ROI per day at 40 emails | manual Rs 600, **assisted Rs 198**, straight through **Rs 13,380** |
| Accuracy by email style | bulleted 13/13, forwarded 14/14, terse 10/10, table 7/11, prose 3/11 |

**The chapter's conclusion is one its own pipeline does not want:** straight-through processing is the wrong choice at a 19% silent error rate, and **assisted intake** (model drafts, person confirms in ~45 seconds) is what the arithmetic supports. It then shows the two things that would change the answer (extraction good enough for ~2% silent errors, or a downstream confirmation loop) and the tactic that works today: **automate the segment that is already perfect** (bulleted, forwarded, terse = 62% of volume at 100% accuracy) rather than everything at 80%.

**Verification:** `verify_python.py --cwd companion/ch58`: 10 blocks, 10 outputs, 0 mismatches. `ch58_check.py`: 24 checks passed, including idempotency, the per-style accuracy split, and the ROI arithmetic.

**Tooling bug found again:** `tools/verify_python.py`'s `<!-- run: none -->` marker is spent on the next *Python* block even when the marked block is SQL. Worked around by making the affected blocks self-contained; the one-line fix is in `checks/py_fill.py` (already flagged in Part III).

**Riverstone facts used (new, for the coordinator):** the approval limit is Rs 100,000; a coordinator's loaded cost is about Rs 300/hour; manual entry takes about 3 minutes an order, review about 45 seconds; a wrong order costs about Rs 2,000 in credit note, re-delivery and the customer call.

**Manual checks needed:** UiPath, Automation Anywhere, Power Automate, Camunda and Temporal are named but not run.

## Chapter 57 report (approved v1)

**Sections:** 57.1 What changes · 57.2 Prompts as code · 57.3 The golden set as a build step · 57.4 The day the provider changes the model · 57.5 Tokens, cost, the meter · 57.6 Caching · 57.7 Latency · 57.8 Failure and fallback · 57.9 Monitoring without ground truth · 57.10 Safety and logs · 57.11 The human loop · full template · 18 exercises with answers · 3 figures.

**No new dataset:** the chapter operates Chapter 54's 60 emails and Chapter 55's assistant. New companion code: `provider.py` (one metered call site wrapping Ch 54's stand-in, with a simulated model upgrade and deterministic rate-limit/timeout failures), `pipeline.py` (prompt registry, tolerant parser, cache, retry/fallback, golden-set evaluation), `questions_stream.py` (8 weeks of support questions with topic drift from week 5).

**Measured results:**

| What | Number |
|---|---|
| Prompt versions v1 / v2 / v3 | 21 / 35 / **47** of 60 |
| Provider "upgrade", existing parser | **0 of 60, 60 unparseable** |
| Same upgrade, tolerant parser | back to 47 of 60 |
| Cost of one golden-set run | 11,006 in / 3,184 out tokens, **Rs 4.74** |
| Caching, 300-request day | **81% hit rate, Rs 23.62 → Rs 4.52** |
| Fallback at a 20% provider failure rate | 48 primary, 9 fallback, 3 escalated; **95% served** through 29 errors |
| Topic drift (assistant unchanged) | refusal rate **15% → 42%**, confidence 0.587 → 0.450 |

**The chapter's spine** is that a provider can change a model behind the same name and take a pipeline to zero with no code change on your side; that the fix is tolerant parsing in your own code, not a better prompt; and that with no accuracy to monitor, the assistant's own refusal rate is the early warning (its rise is a content gap, not a model problem).

**Verification:** `verify_python.py --cwd companion/ch57`: 11 blocks, 11 outputs, 0 mismatches. `ch57_check.py`: 25 checks passed. Style checks clean; line-by-line walkthroughs throughout.

**Manual checks needed:** LangSmith, Langfuse, Braintrust, W&B Weave, LiteLLM, OpenRouter, Redis, OpenTelemetry, NeMo Guardrails and Guardrails AI are named but not run.

**Promises made:** Ch 58 (tools that write), Ch 47, Ch 64, Ch 74.

## Chapter 56 report (approved v1)

**Sections:** 56.1 What breaks after launch · 56.2 Versioning (five things) · 56.3 Experiment tracking · 56.4 Packaging · 56.5 Serving · 56.6 Deployment patterns · 56.7 Three-layer monitoring · 56.8 Drift, measured · 56.9 Retraining · 56.10 Incidents · 56.11 The maturity ladder · full template · 18 exercises with answers · 3 figures.

**First Part VI chapter where the production tools themselves run:** FastAPI 0.141.1 + uvicorn (real endpoint, exercised in-process with `fastapi.testclient`), MLflow 3.16.1 with a **SQLite** backend (MLflow 3 deprecated the plain-folder store; the chapter says so), joblib packaging, SciPy for the KS statistic.

**New data:** `companion/ch56/simulate_production.py` (seed 56): 12,000 parts over 24 weeks, 1,053 defective. Lamps replaced in week 8 (data drift); a new mould produces 69 unlabeled "flash" defects from week 16 (concept drift).

**The chapter's central measured finding, which contradicts the usual advice:**

| Weeks | Event | PSI (brightness) | Recall |
|---|---|---|---|
| 0–7 | baseline | ~0.01 | 0.95–1.00 |
| 8–15 | new lamps | **rises to 4.41** | **0.94–0.98 (fine)** |
| 16–23 | new mould | **flat ~4.2** | **falls to 0.79–0.88** |

Input drift fired hard when nothing was wrong and was silent when the model actually broke. The chapter builds the three-layer monitoring argument on this, including the fast proxy (predicted-defective rate vs the QC tally, which opens a gap in week 16) and a 2% audit of passed parts.

**Other measured results:** four tracked runs where sorting by `cost_rupees` puts a different model first than precision does; the service at 1.8 ms median / 2.1 ms p95 with the model itself 0.2 ms; shadow mode where the candidate is right 17 times and the current model 16 on the 33 disagreements (explicitly *not* a case for shipping); a retrain lifting recent recall 0.85 → 0.91 with false alarms doubling, used to argue that **threshold re-tuning is part of retraining**.

**Verification:** `verify_python.py --cwd companion/ch56`: 12 blocks, 12 outputs, 0 mismatches. `ch56_check.py`: 23 checks passed (stream, artifact metadata, PSI/KS, per-period recall, retrain behaviour, and three live service assertions).

**Manual checks needed:** Weights & Biases, DVC, BentoML, Seldon, Evidently, NannyML, SageMaker/Vertex/Azure ML are named but not run; no containers or orchestration (stated in a simplification note).

**Promises made:** Ch 57 (LLMOps), Ch 46 (scheduling), Ch 47 (data-layer quality), Ch 64 (model cards, accountability), Ch 74.

## Chapter 55 report (approved v1)

**Sections:** 55.1 Why retrieval · 55.2 What is in the documents · 55.3 Chunking · 55.4 Two ways to search (BM25 from scratch, vectors) · 55.5 Hybrid search and measurement · 55.6 Grounding, citations, refusal · 55.7 Tools · 55.8 Agents, without the hype · 55.9 Evaluating the application · 55.10 Guardrails · 55.11 Shipping it · full template · 18 exercises with answers · 4 figures.

**New shared asset (Part VI owns it; Ch 58 and the case studies can reuse it):** `companion/ch55/generate_corpus.py` (seed 55) builds 28 Riverstone documents (8 spec sheets, 9 policies including **one superseded delivery policy left in the folder on purpose**, a price list, contacts, 10 FAQs) and 65 questions, 55 with a recorded correct source and **10 deliberately unanswerable**. Also `retrieval.py` (three chunkers, BM25, vector index, hybrid), `assistant.py` (grounding, citation, absolute-score refusal), `tools.py` (two read-only tools).

**Measured retrieval (55 answerable questions):**

| Chunking | Search | Chunks | recall@1 | recall@5 | MRR |
|---|---|---|---|---|---|
| fixed 400 | hybrid | 52 | 0.85 | 1.00 | 0.918 |
| sentences | **bm25** | 70 | **0.91** | 1.00 | **0.949** |
| sentences | vector | 70 | 0.87 | 1.00 | 0.932 |
| sections | vector | 60 | 0.85 | 0.98 | 0.912 |

**Findings the chapter keeps rather than tidies away:** chunking moves the number more than the algorithm; plain BM25 beats vectors on this corpus, contradicting the usual advice; the vector search ranks the **superseded** policy first for a delivery question (the hook for section 55.10); a refusal threshold on *normalized* scores does nothing, because the top score is always 1.0 (absolute floors are used instead, with the bug written up as a lesson).

**End-to-end ladder:** answered 50/55, cited the right document 38, answer contained the fact 18, correctly refused 7/10. The chapter says plainly that the third number is the one a real model would move most, and that the others would barely change.

**Verification:** `verify_python.py --cwd companion/ch55`: 15 blocks, 15 outputs, 0 mismatches (run twice to confirm stability after removing a timing-dependent line). `ch55_check.py`: 19 checks passed. Style checks clean; every code block has a line-by-line walkthrough.

**Stand-ins, labeled in one consolidated note plus at each use:** the embedding model (TF-IDF + SVD), the generator (returns a sentence from the retrieved text, cannot paraphrase), the reranker (described, not run), and LLM-as-judge (rules instead of a model).

**Riverstone facts used (new, for the coordinator):** support desk support@riverstone.example and quality@riverstone.example; escalation to the Customer Support Lead after 3 working days; delivery free above Rs 25,000 (revision 4, 1 Jan 2026), previously Rs 40,000; 12-month warranty, 24 months on the Industrial Crate; bulk discounts 5/8/12% at 500/1,000/5,000 units; 18% GST; payment terms 100% advance, 30 days, 45 days for key accounts.

**Manual checks needed:** vector databases, rerankers, LangChain/LlamaIndex, RAGAS/TruLens are named but not run.

**Promises made:** Ch 56 and 57 (serving, monitoring, cost), Ch 58 (tools that write), Ch 47 (document owners and statuses), Ch 64, Ch 74.

## Chapter 54 report (approved v1)

**Sections:** 54.1 What the model computes · 54.2 Tokens (a BPE tokenizer trained on Riverstone's own emails) · 54.3 How a chat model is built · 54.4 Context windows · 54.5 Sampling · 54.6 Prompting, measured · 54.7 Structured output you can trust · 54.8 Embeddings · 54.9 Prompt, retrieve, or fine-tune · 54.10 Multimodal · 54.11 Limits and risks · 54.12 The landscape as of September 2026 · full template · 18 exercises with answers · 4 figures.

**New dataset and stand-in:** `companion/ch54/generate_order_emails.py` (seed 54) builds 60 purchase-order emails in five shapes (table, prose, forwarded, bullets, terse) with ground truth for each, 110 order lines in total. `mock_llm.py` is the local stand-in for a hosted model: deterministic, rule-based, and deliberately imperfect in the ways that make prompting matter (chat wrappers, copied date formats, items missed on a crowded line, broken JSON on four emails). Its limitations are documented in the file, in a simplification note at the top of the chapter, and again at each point where they matter. `api_example.py` shows the real provider call.

**The measured spine:**

| Prompt | Fully correct | Fields right | Unparseable |
|---|---|---|---|
| Naive | 12 / 60 | 156 / 240 | 4 |
| With instructions | 35 / 60 | 215 / 240 | 0 |
| Plus one example | 47 / 60 | 227 / 240 | 0 |

Validation plus one retry loads **59 of 60** automatically while only **47** are actually right: the chapter states that gap explicitly, because it is the difference between a pipeline that looks safe and one that is. Sampling is measured over 10,000 draws (top token 81.6% at temperature 0.2, 34.9% at 1.8, tail removed entirely at top_p 0.9). Embeddings are real (TF-IDF + SVD, cosine similarity), with working semantic search.

**Sources for the September 2026 landscape** (searched 19 Sep 2026, all prices per million tokens, framed in the text as "verify before you quote"): mungomash.com/ai/models (GPT-6 Astra $10/$50, 1.05M context, cutoff 30 Apr 2026; Claude Opus 5 $5/$25); morphllm.com/llm-api (Fable 5.1 $10/$50, GPT-5.6 Sol $4/$20, Sonnet 5 $2/$10, Gemini 3.1 Pro $2/$12, verified 2 Sep 2026); developersdigest.tech (Sonnet 5 pricing made permanent, 15 Aug 2026); benchlm.ai/llm-pricing (Gemini 3.8 Flash $0.75/$3.75, Qwen3.7 Flash $0.03/$0.13, 15 Sep 2026); alphacorp.ai (Anthropic cache reads cut 75% to $0.25/M on 1 Sep 2026); spheron.network (Gemini 3.1 Pro doubles past 200k tokens); iternal.ai (prices fell ~80% 2025→2026; output 3–8× input; MiniMax M2.5 at 80.2% SWE-bench).

**Verification:** `verify_python.py --cwd companion/ch54`: 14 blocks, 14 outputs, 0 mismatches. `ch54_check.py`: 16 checks passed, including the three prompt scores, the softmax and sampling numbers, and the mock's three documented failure modes. Style checks clean; every code block has a line-by-line walkthrough.

**Manual checks needed:** all of section 54.12 (prices and model names change weekly, and this is the chapter's biggest refresh liability); `tiktoken`, `transformers`, `pydantic`, `instructor`, Ollama, vLLM and llama.cpp are named but not run; `api_example.py` is not executed, since it needs a key.

**Riverstone facts used (new, for the coordinator):** 20–40 purchase orders arrive by email daily and are re-keyed by hand; about one in six arrives as a phone photo of a printed PO; the pilot ends with 78% of orders loading automatically and an exception queue of about nine a day.

**Promises made:** Ch 55 (retrieval, agents, evaluation), Ch 57 (cost and version monitoring), Ch 58 (the ERP end of the order pipeline), Ch 64, Ch 74.

## Chapter 53 report (approved v1)

**Sections:** 53.1 From regression to a network · 53.2 Training, worked by hand · 53.3 The techniques that make training work · 53.4 The architectures · 53.5 Convolution step by step · 53.6 The defect-detection project · 53.7 Attention step by step · 53.8 Why transformers took over · 53.9 Quantization and compression · 53.10 When not to use deep learning · full template · 18 exercises with answers · 4 figures.

**New dataset:** `companion/ch53/generate_defect_images.py` (seed 53, NumPy only, no downloads): 6,000 32×32 images of moulded lids on Riverstone's conveyor, 476 defective (7.93%), with three faults the QC team logs — scratch (162), void (157), short shot (157). Belt, part, rim, lighting gradient and sensor noise are all generated, so the images are reproducible on any machine in seconds.

**The teaching spine, all measured:**
- One training step by hand: loss 0.176 → 0.000 after a single update; every gradient printed.
- Convolution computed by hand: +1.5 at the left edge, −1.5 at the right, 0 in the flat middle.
- **Raw pixels into a network: 92.07% accuracy, zero defects caught.** Convolution features into the same network: 91.6% recall, 98.2% precision.
- Threshold priced from the business (₹4,000 a miss, ₹40 a false alarm): cheapest at 0.01, 97.5% recall, ₹13,840 per 1,500 parts against ₹40,080 at the default threshold.
- Attention on four tokens: *cracked* puts 0.396 of its attention on *crate*, more than on any other token including itself.
- Quantization to int8: 4× smaller, largest weight error 0.005, **1 decision in 1,500 flips**; at 4 bits, 6 flip.
- Robustness: brightening every test image 10% costs 1.7 points of recall and nearly quadruples false alarms — the evidence behind the chapter's night-shift story.

**Verification:** `verify_python.py --cwd companion/ch53`: 24 blocks, 24 outputs, 0 mismatches. `ch53_check.py`: 25 checks passed. Style checks clean. Every code block carries a line-by-line walkthrough, per the author's standing instruction.

**Performance note:** section 53.6 saves `defect_data/features.npy` (about a minute of convolution) and later sections and answers reuse it; without the cache a full verification run exceeds five minutes.

**Assumptions about Part IV (check when Chapters 36–39 exist):** that they teach train/validation/test splits and `train_test_split`, overfitting and regularization, the confusion matrix with precision and recall, class imbalance, data leakage, and gradient boosting as the tabular default. Chapter 53 cites them generically and re-explains anything it relies on.

**Manual checks needed:** the PyTorch listings (not run here); torchvision model names; Label Studio and CVAT.

**Promises made:** Ch 54 (attention scaled up), Ch 55, Ch 56 (serving and drift for this model), Ch 64 (model cards, explainability), Ch 74 (interview questions).

## Decisions taken

- Chapter 53 uses hand-written convolution kernels rather than a learned CNN, so it runs anywhere in seconds; a simplification note says exactly what that changes and what it doesn't.
- The defect dataset is generated, not photographed, and the chapter says so twice, including in the model's limitations.
- Riverstone facts used: the Taloja plant moulds lids; QC prices a returned batch at about ₹4,000 and a re-inspection at about ₹40; the line runs day and night shifts on three machines. **New; for the coordinator to accept.**

## Requests for the coordinator

- **Disk.** If Part VI is to verify PyTorch code, the container needs roughly 4 GB free, or an allowed CPU-only wheel index.
- **Chapter 55's documents dataset** (manuals, policies, FAQ) will be built when Chapter 55 is written unless you want it earlier for other parts.
- **Ch 58** needs the automation sandbox (sample PO emails and PDFs); Part VI will build it unless another part already has.
