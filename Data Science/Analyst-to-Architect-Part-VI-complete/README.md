# Analyst to Architect — Part VI: Production ML, Generative AI & MLOps — complete bundle

Chapters 53–59, **all seven approved** (19 September 2026). About 66,400 words, 23 figures, 190 PDF pages. **86 Python outputs verified with 0 mismatches and 132 number checks.**

| Ch | Title | Class | PDF pages | Words |
|---|---|---|---|---|
| 53 | Deep Learning in Depth | B | 36 | ~12,300 |
| 54 | Generative AI & Large Language Models | B | 32 | ~11,400 |
| 55 | Building AI Applications: RAG, Agents & Evaluation | B | 31 | ~10,700 |
| 56 | MLOps: Making Models Survive Production | B | 27 | ~9,600 |
| 57 | LLMOps | B | 25 | ~8,700 |
| 58 | Intelligent Automation | B | 25 | ~8,500 |
| 59 | Industry Case Studies | C | 14 | ~5,000 |

## Read this before the chapters: what runs and what does not

The build container could not install PyTorch (the PyPI wheel bundles CUDA and needs about 3.5 GB; the CPU-only index is outside the allowed domains) and could not download model weights.

- **Chapter 53** runs on NumPy and scikit-learn, with hand-written convolution kernels, and shows PyTorch only as listings marked *not run here*. Its defect dataset is generated rather than photographed, which the chapter says twice, including in the model's limitations.
- **Chapters 54, 55 and 57** run against a local stand-in for a hosted model (`companion/ch54/mock_llm.py`, wrapped by `companion/ch57/provider.py`). The stand-in is labeled at every point of use, and each chapter carries a consolidated simplification note; Chapter 55 names the specific places where it falls short of production.
- **What does run for real:** scikit-learn, FastAPI 0.141.1 with uvicorn (a real endpoint, exercised in-process), MLflow 3.16.1 on a SQLite backend, SQLite as a system of record, BM25 and TF-IDF/SVD retrieval, and every measurement quoted in the chapters.

This is cross-part issue 18, open with the author. The coordinator's recommendation: reissue Chapter 53 with real PyTorch once about 4 GB of disk or an allowed CPU-only wheel index is available, and keep the stand-in for 54, 55 and 57 with its disclosure, since a book cannot require readers to hold a paid API key.

## What's where

| Folder | Contents |
|---|---|
| `manuscript/` | The seven chapters as Markdown |
| `pdf/` | The seven approved chapter PDFs |
| `figures/` | 25 figures as SVG, `png/` renders, and the `make_figs*.py` scripts |
| `companion/` | Generators, pipelines, the ML code, the SQLite ERP, and the stand-in provider |
| `checks/` | One number-check script per chapter (53–58) plus `py_fill.py` |
| `tools/` | The verifiers, `check_code_teaching.py`, `setup_databases.sh`, and the PDF builder |
| `planning/` | Chapter map, writing instructions, progress tracker, bible additions, cross-part issues, refresh list, promises, the §6.5 note, and the book-wide code-teaching baseline |
| `planning/parts/` | Part VI's brief, status file and the coordinator's reply |

Generated data, trained models, MLflow stores and the SQLite ERP are not included: every generator is deterministic and rebuilds them identically.

## Rebuilding

```
cd companion/ch53 && python3 generate_defect_images.py     # 6,000 images, seed 53
cd ../ch54 && python3 generate_order_emails.py             # 60 emails + ground truth, seed 54
cd ../ch55 && python3 generate_corpus.py                   # 28 documents, 65 questions, seed 55
cd ../ch56 && python3 simulate_production.py               # 24 weeks of line data, seed 56 (~1 min)

cd ../../figures && for f in make_figs5*.py; do python3 "$f"; done

python3 tools/verify_python.py manuscript/ch56-mlops.md --cwd companion/ch56
for f in checks/ch*_check.py; do python3 "$f"; done
python3 tools/check_code_teaching.py manuscript/ch54-generative-ai-and-large-language-models.md
```

## Coordinator checks on this part

All 23 figure references resolve. **Zero em dashes in prose across 66,400 words** — the cleanest in the book. To fix in the review pass: *honestly* twice each in Chapters 57 and 58, and one `optimis…` in Chapter 55.

This part applied §6.5's line-by-line rule well (45 explicit "line by line" sections) but not its settings table; no chapter has the column "What happens if you change it", and only Chapter 54 asks the reader to predict before running.

| Ch | Code blocks | Blocks flagged | Ch | Code blocks | Blocks flagged |
|---|---|---|---|---|---|
| 53 | 24 | 9 | 57 | 14 | 6 |
| 54 | 17 | 13 | 58 | 13 | 8 |
| 55 | 21 | 10 | 59 | 0 | 0 |
| 56 | 17 | 10 | | | |

Across the whole book, one chapter in 56 has that settings table. See `planning/code-teaching-baseline.md`.

## Open items

- **Cross-part issue 18** — the environment caveat above; the author's decision.
- **Cross-part issue 19** — the missing settings tables, book-wide, to be closed in each part's review pass.
- Chapter 53's assumptions about Part IV (train/test splits, overfitting, precision and recall, gradient boosting) were written before Chapters 36–39 existed. They exist now; check them during the review pass, along with Chapter 35's definitions.
- New Riverstone facts accepted into the bible: the Taloja plant moulds lids; QC prices a returned batch at about ₹4,000 and a re-inspection at about ₹40; the line runs day and night shifts on three machines.

`planning/parts/part-6-coordinator-reply.md` has the full reply; `planning/parts/part-6-status.md` has the per-chapter reports.

## The rules every chapter follows

`planning/chapter-writing-instructions.md` is the master brief. Two sections matter most:

- **§6.5** — teach code and formulas line by line: the question in plain words, the plan before any code, short code, the real output and how to read it, then one bullet per line, plus a settings table with "what happens if you change it" and at least one measured what-if.
- **§15.1** — the part-completion review pass: read the part straight through as a reader would, work out the cause of each problem at the level of the part, and only then fix in place.

Riverstone Supplies is fictional. Every person, customer, product and number in the data is invented.
