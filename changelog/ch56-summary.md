# Chapter 56 summary: MLOps: Making Models Survive Production

**Findings:** 33 content (56.1–56.33), 15 visual (V56.1–V56.15), 3 Reader's Journey rows touching Ch 56 (RJ-S2-24, RJ-S3-67, and RJ-S3-57 on the coordinator's request). All 33 content findings applied; 6 visual findings fixed in this pass (V56.3, V56.4, V56.9, V56.10, V56.13, plus V56.1 confirmed), the rest confirmed in the rebuilt PDF. Nothing left Open.

## What changed

- **Set up, for real (new §56.0).** Installs `fastapi==0.141.1 uvicorn==0.54.0 httpx2==2.13.1 mlflow==3.16.1`, checks Chapter 53's `defect_data`, runs `simulate_production.py` with its output, shows the folder tree, and opens the notebook with a version check. `httpx2` (not `httpx`) was confirmed from Starlette 1.7's test client source: finding 56.4's "typo" guess was wrong, and the chapter now says why.
- **One threshold story (56.2).** 97.5% / 0.01 / ₹13,840 is Chapter 53's cheapest point; v1 ships at the plant manager's 0.1 (95%, 6 false alarms per 1,500), and §56.3 explains why t0.05 isn't adopted until the retrain.
- **Every code block runs.** Experiment tracking is now five cells (split, store, `run_one` with the real trusted type, one run, three more); a real **registry** (register, alias `production`, load by alias); a **packaging** cell that builds the metadata (data hash, feature version, code commit, library version) and writes the bundle; **`serve.py` in four cells** (pydantic schema with a caught error, app and log, `/health`, `/predict`), then **run with uvicorn and called with curl**, `/docs` described, and TestClient as the CI way; a timing cell (95th percentile defined).
- **Conclusions rebuilt on the real re-run** (scikit-learn 1.9.1 shifted several numbers):
  - shadow mode: 46 disagreements, candidate "right" 30 v 16 by count; the new costed 2×2 shows the value is in 6 net defects caught (₹24,000 of ₹24,320). The "coin flip" conclusion is gone.
  - retrain: better on every line (recent recall 0.88→0.91, false alarms 28→20, cost ₹1,01,120→₹76,800; old weeks 0.97→0.99), and a threshold sweep on out-of-fold predictions finds 0.01 cheapest again, now a bigger gap: a plant-manager decision.
  - drift vs decay: PSI 4.4 in the lamp weeks with recall unchanged (96.8% → 96.5%); new mould: recall 84.4%, about 12 points down, 18 of 69 flash parts caught (new printed cell). Dates: late April / late June.
  - the fast proxy: the predicted-vs-true gap never opens (misses and extra false alarms cancel), so §56.7 now teaches "the fast proxy measures change, not correctness", Ex 7 reports "None" honestly, and the story no longer claims the gap was "visible to anyone glancing".
- **Drift, by hand.** KS computed with `searchsorted` and matched to SciPy (0.270); cumulative distribution defined; out-of-sample calibration (weeks 6–7 against weeks 0–5: 0.006, 0.013); a settings table for PSI.
- **Container and CI.** Optional Dockerfile box tied to Chapter 52 (§52.2, §52.3 readinessProbe); Ex 9 is a companion script with real output and exit code, plus a GitHub Actions workflow in Chapter 26 §26.8's form.
- **Answers.** Code and real output added to answers 1, 2, 4, 5, 6, 7, 8, 9, 10; answer 6 corrected (feature 0 does not move; feature 7 does); answer 12's loader shown. Appendix G parenthetical removed.
- **Figures.** All three redrawn at 720 px (smallest text 7.19 pt): Fig 56.2 now three layers with the third split into two streams; Fig 56.3 recall axis from 0.7, dates late April / late June, numbers from the re-run; Fig 56.1 with the new hash and size.
- **Terms.** MLOps defined in "In plain English" (M.12); alias, stage (deprecated), schema, input contract, liveness/readiness, test client, 95th percentile, cumulative distribution, training-serving skew added.

## Option picks

56.2 recommended (0.1 story) · 56.9 first option (real MLflow registry) · 56.12 recommended (add code_commit + feature_version) · 56.14 "four weeks" · 56.16 recommended (three layers) · 56.18 (a)–(d), adapted to the real numbers · 56.19 relabel · 56.20 late April / late June · 56.22 first option (reference weeks 0–5) · 56.28 first option (replace hyphen) · 56.31 second option (ML engineer role) · V56.4, V56.9, V56.10 first options.

## Skipped, and why

Nothing skipped. Two rows are "Approved" for other chapters: RJ-S3-67 (the fix is Ch 58's run date) and RJ-S3-57 (Ch 56's two titles done; the rest is in Ch 59/64/74/75/82).

## Time needed

16–20 h → **18–22 h**, three sittings (setup to serving ≈ 8 h; deployment to retraining ≈ 7 h; the rest). The chapter grew from 27 to 45 PDF pages.

## Verification

- `verify_python`: 36 blocks run, 35 outputs checked, **0 mismatches** (run in a scratch copy of `companion/ch56` so MLflow's store stays out of the book tree).
- `verify_shell`: 11 commands run, 11 outputs checked, **0 mismatches** (the `ls`, the simulator, uvicorn + three curl calls, `kill %1`, the CI check and `echo $?`).
- Three blocks are shown but not checked, each with a real output from this machine and a note in the text: the install command, the `/predict` curl with its log line (latency and timestamp vary), and the timing cell.
- `checks/ch56_check.py`: 29 checks pass (every number quoted in prose). `checks/ch59_check.py`: 23 checks pass.
- `fig_check`: 0 figures under 7 pt. `restructure --check`: already in order. `layout_check`: map numbers 18/18, no stranded heads or lead-ins, no sparse pages, no small text, tofu 0.
