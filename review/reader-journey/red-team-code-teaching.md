# Red team: why the code-teaching system will fail the first-time reader

*Fable B, 22 September 2026. Devil's advocate pass over the whole system: the standard (§6.5), the checker, the audit method including my own Chapter 37 sample, the patches, and the process that applies them. Every flaw is written so it can be fixed from this file alone. Evidence is quoted or was run; where a claim is my judgment, it says so.*

**The question this file answers:** a first-time reader opens a chapter, types the code, and wants to understand it well enough to change it and predict what happens. What, in the system as it stands, stops that from happening?

**Severity:** **S1** the reader is blocked or misled · **S2** the reader memorizes instead of understands · **S3** the system reports success it has not earned · **S4** cost, drift, or maintenance risk.

---

## Part A. The reader's experience (top priority)

### A1. The reader cannot run section N without every section before it (S1)

**What.** Chapter 37's code is one long program cut into 32 pieces. `clf_report` is defined once in 37.3 and used in 37.4 through 37.11. `folds` is defined in 37.10 and used by every search and every exercise. `x_toy` is defined in 37.8 and used by exercise 9. A reader who opens section 37.7 to learn random forests and types its 13 lines gets `NameError: name 'clf_report' is not defined`, and nothing on the page tells them why or what to run first. The exercises preamble lists eighteen names the reader must already have, which is an admission of the problem, not a fix.

**Why it defeats the goal.** Playing with a setting means changing one thing and re-running. When re-running means "re-run the whole chapter", the reader stops playing after the second try. This is the single largest reason the book will be read rather than used.

**Fix.** (1) Every section that uses a name from an earlier section opens with one line: *"Needs: the setup from 37.0 and `clf_pipeline`, `clf_report` from 37.3."* (2) A companion notebook per section, or one per chapter with a clearly marked "run this first" cell, and a separate playground cell for each what-if with the setting on its first line. (3) The verify tool should be extended to prove that each section's companion cell runs on its own after the "run first" cell, so the dependency line is true rather than hoped.

### A2. The reader's numbers will not match the book's, and nobody tells them what "close enough" means (S1)

**What.** The chapter prints outputs to four decimals from xgboost 3.4.1, lightgbm 4.7.0, catboost 1.2.10, scikit-learn 1.8.0, on one CPU core. A reader in 2027 on newer versions, or on a Mac with a different BLAS, will get AUC 0.786 where the book says 0.788 and log loss 0.2718 where the book says 0.2731. The book says nothing about tolerance. The first-time reader's only available conclusion is "I did something wrong", and they will spend an hour looking for the mistake.

**Evidence.** The Tools section records the versions (good) and stops there. No sentence anywhere in Chapters 36 or 37 says how far a number may drift.

**Fix.** A standing block in every chapter that runs code, written once and reused: *"Your numbers may differ from these in the third decimal, and by more for the three boosting libraries between versions. A difference larger than 0.01 in AUC or than 5% in a rupee figure means something is different: check the versions printed in Tools, the seed, and that you ran every block in order."* And the settings tables should say which numbers are seed-sensitive (W14 in the findings file measures exactly this for the forest; that measurement should be quoted here).

### A3. The first error a reader will hit is never shown (S1)

**What.** §6.5 says "show the error", and the chapter shows none. The errors a beginner actually meets in Chapter 37, in order of likelihood: `pip install catboost` failing on a Python version it does not yet support; `import lightgbm` failing on macOS without `libomp`; `FileNotFoundError: ../accounts/accounts.csv` because the notebook was opened in the wrong folder; `ValueError: could not convert string to float: 'Retail'` from passing raw columns to a model without the pipeline; `NotFittedError` from calling `predict_proba` before `fit`; a shape error from `fit(y, X)` in the wrong order. Not one appears, and the "Common mistakes" table is about concepts, not error messages.

**Why it defeats the goal.** A reader who cannot get past the import line never reaches the teaching. Everything below it is wasted on them.

**Fix.** Each code chapter gets an "Errors you will see" table, standard format: the exact first line of the error, what it means in plain words, the fix. Five to eight rows. The verify tool can produce the real text of each by running the wrong version, which also satisfies "never type an output".

### A4. "What good looks like" is missing for the second number on every line (S2)

**What.** Every model prints `AUC 0.764   log loss 0.2833`. The reader is told what AUC is in Chapter 36 and is told that 0.764 is good. They are never told what log loss to expect. Chapter 36 printed the base rate's log loss for leads (0.2983) so its 0.2369 could be read; Chapter 37 never prints the base-rate log loss for accounts, so 0.2833 floats with no anchor. Is 0.5255 for k-NN at *k* = 25 bad? The text says *k* = 5's 1.5887 is "terrible" and says nothing about 0.5255.

**Evidence.** `grep -i "log loss"` over Chapter 37 finds no sentence that gives a benchmark; the only anchor is in Chapter 36 for a different dataset.

**Fix.** Section 37.0 prints the two baselines once, "predict the base rate for everyone" and "the Chapter 36 rule of thumb", with AUC and log loss, and the reading sentence says "a model earns its keep by beating both; anything above 0.32 on log loss here is worse than guessing the base rate". Then every later "Reading it" has a floor to refer to.

### A5. Terse names and out-of-sight helpers hide what the code does (S2)

**What.** `X_tr`, `y_va`, `p`, `s`, `m`, `n`, `a`, `b`, `c`, `f`, `r`, `g` all appear as variable names. `s = cross_val_score(...)` then `s.mean()`: a reader has to hold in their head that `s` is "five scores". `clf_report` hides fit, predict_proba, two metrics, a print, and a dictionary write behind one name used twenty-five times. That is good engineering and poor teaching: every time the reader sees `clf_report("k-NN, k=5", ...)`, the part they need to learn is inside a function they read once, two sections ago.

**Fix.** Names in teaching code carry their meaning: `scores` not `s`, `probabilities` not `p`, `model` not `m`. When a helper is used, the first use in each section reminds the reader in a half-line what it does: *"`clf_report` fits, scores on validation, prints (37.3)."* The book's own §5.3 says "name the thing"; single letters do not.

### A6. The prediction prompt is spoiled by the output printed under it (S2)

**What.** §6.5 requires "predict before running". In a printed book the output sits three lines below the code. The eye reads the answer before the reader has formed a prediction. The prompt becomes decoration. My P1 and P14 patches put the prompt above the code and the output directly below, so they have the same problem.

**Fix.** A layout rule in §6.5: the prediction prompt goes at the end of the *previous* block's reading, and the output it refers to is placed after a paragraph of explanation, or the prompt refers to a what-if whose result is in a table at the end of the section. Alternatively the prompt asks for a *direction* ("higher or lower than 0.764?") and the reading sentence names the answer, so seeing the number does not spoil the reasoning.

### A7. The reader is told what a setting does, not how to decide what to set (S2)

**What.** The settings tables, the chapter's and mine, describe each setting in isolation. Nothing says which knob to turn first, in which direction, and when to stop. A reader with a new dataset and `HistGradientBoostingClassifier` has eight settings and no order. Memorizing "learning_rate=0.05, max_depth=3" is exactly the memorization the author is worried about.

**Fix.** Every model gets a three-line "Where to start, and what to turn first" box: the starting values, the first knob to turn and which way, the sign that says stop (validation score falls, or the train-validation gap opens). The what-ifs then illustrate the box rather than float on their own. Chapter 37's own "default workflow" paragraph at the end is the right idea at chapter level; it needs to exist per model.

### A8. The book is silent about what happens when a reader plays and breaks something (S1)

**What.** The goal is a reader who changes settings. The first things they will try: `test_size=1.5`, `n_neighbors=0`, `max_depth=0`, `strategy="mode"`, `C=0`, `n_splits=1`, `learning_rate=0`. Each raises an error or a silent oddity, and none is shown. The "What happens if you change it" column only covers sensible values.

**Fix.** One row per table, "Values that break it", listing the range and the error the reader will see. This is where the checker could help: it could list, per setting, whether a breaking value is documented.

### A9. Dead code teaches a bad habit and raises a question nobody answers (S2)

**What.** `results = {}` in 37.3 is filled by every `clf_report` call and by the CatBoost block. It is only ever read back on the same line it was written. Nothing later compares `results`. A first-time reader asks "what is this for?", finds no answer, and learns that code contains things you do not question. **Verified:** two writes, no read outside the same line.

**Fix.** Either use it (print a sorted table of `results` at the end of 37.9 as the chapter's validation-set league table, which the text then reads) or remove it. Using it is better: it gives the reader the "all models on one screen" view the chapter currently lacks.

### A10. Chapter 37 is 14 to 18 hours and the patches add about a third, with no route through it (S4, becomes S2)

**What.** The chapter is 1,820 lines. My 24 patches add roughly 600 lines of tables and bullets. §6.5 applied in full to a chapter this size produces a chapter a first-time reader cannot finish. The standard says "explain every line" and "short enough to read on one screen" and does not say what to cut.

**Fix.** (1) A "first pass" route at the top of each long chapter: the sections a first-time reader does, in order, and the sections to return to (37.9 SVM and 37.12 can wait). (2) A removal budget with every patch: a table added means a paragraph that repeats it removed. (3) The "Code words" table and a settings reference (B3) so that later chapters stop re-explaining.

### A11. The one-row explanation comes after the library, not before, and three models never get one (S2)

**What.** §6.5: "A model is explained by what it does to one row of Riverstone data before any library is imported." Chapter 37 does the hand calculations for the sigmoid, Naive Bayes, Gini, and boosting *after* the library has been fitted, using the library's numbers. k-NN, random forest, and SVM get no one-row example at all. My findings file adds a k-NN one-row check (W5), also after the library, and leaves the forest and SVM as they are.

**Fix.** Part IV decides, once, whether the order in §6.5 is binding. If it is, each model section opens with the one-row walk-through on one account and its two or three features before any `import`. If it is not, §6.5 is amended to say "beside", and the forest and SVM still get a one-row example (a forest of three tiny trees voting on one account is four lines).

### A12. Cross-references the reader will follow and not find (S1)

**What.** Chapters send the reader elsewhere for an explanation. When the target does not contain it, the reader concludes they missed it and loses trust. My own patches did this three times in one chapter: "`**best` unpacks a dictionary (Chapter 17)" but Chapter 17 teaches tuple unpacking only; "parentheses because `&` binds tighter (Chapter 18 section 18.3)" but 18.3 is "Looking at a DataFrame"; "changing a global to steer a function is a habit to avoid (Chapter 29)" but Chapter 29 mentions global variables only in passing. **Verified by grep.** If an auditor with the manuscript open gets three of four wrong, the part chats writing from memory get more wrong.

**Fix.** No cross-reference ships without a grep that finds the term in the target section. `tools/extract_promises.py` exists for forward references; it should also verify backward references to a section number and the term claimed, and the findings file's patches must pass it before they are applied.

### A13. There is no playground (S2)

**What.** A book can print code; it cannot let the reader drag a slider. The companion files are the only place "playing" can happen, and the chapter's companion is one folder with a data loader. There is no notebook where each what-if is a cell with the setting at the top and a comment "change this and re-run".

**Fix.** One notebook per code chapter, generated from the manuscript by a tool (the verify tool already parses the blocks), with a "run first" cell, one cell per section, and one cell per what-if. This is the artifact that turns the book from reading into doing, and it costs less than the prose patches.

---

## Part B. The standard, §6.5

### B1. "One bullet per line" is neither what the reference chapters do nor what a reader can absorb (S2)

**What.** §6.5 says "one bullet per line or per clause. Never skip a line because it looks obvious." Chapter 27 section 27.5, held up as the model, groups a 20-line function into nine bullets by idea. A literal reading of the rule produces twenty bullets for a twenty-line block, which nobody reads. The two are in conflict and the part chats will follow one or the other at random.

**Fix.** Rewrite the rule: "one bullet per *idea*, and every line is covered by some bullet. A bullet may cover three lines that do one thing; no line may be covered by none." Then the checker's coverage test (identifiers named) is the right proxy and the reference chapters comply.

### B2. The fourth column mixes measured and asserted effects and the reader cannot tell which is which (S3)

**What.** "What happens if you change it" invites an opinion in every cell. §6.5 then asks for *one* changed version to be run. So a five-row table has one measured row and four asserted ones, presented identically. My own P16 table says "more folds: steadier estimate", which is contested in the literature and unmeasured here; my P14 translation table states that XGBoost's `min_child_weight` is "minimum rows per leaf", which is wrong (it is a sum of second derivatives; equal to rows only for squared error), and that CatBoost's `min_data_in_leaf` corresponds, which is only true for its non-default tree-growing policy. Both would have shipped as fact.

**Fix.** Two marks in every table: **measured** (with the run's label, e.g. "W6") or **expected**. A cell with neither cannot be published. The checker can enforce this: a table with the fourth column and no "measured" cell is flagged.

### B3. "The first time it appears in the book" cannot be known by chats writing parts in parallel (S4, becomes S2)

**What.** Part II-A, Part III, and Part IV are written by different chats at the same time. `random_state` is explained in Chapters 21, 30, 36, and 37, each in its own words, none referring to the others. The reader gets four explanations of one idea, slightly different, and no place to look it up. The rule as written guarantees this, because "first" is undefined across parallel authors.

**Fix.** A canonical **Settings reference** appendix, owned by the coordinator, one entry per recurring setting (the findings file will list them: `random_state`, `test_size`, `stratify`, `cv`/`n_splits`/`shuffle`, `scoring`, `max_iter`, `n_jobs`, `verbose`, `handle_unknown`, `strategy`, `add_indicator`, `learning_rate`, `max_depth`, `min_samples_leaf`, `n_estimators`). Each chapter's table gives the value used here and the what-if, and links to the appendix for the plain-words meaning. Part chats stop re-explaining, chapters shrink, and the reader has one place to look.

### B4. "What do I change to use my own data?" has no required artifact (S2)

**What.** It is one of the six questions §6.5 lists. Nothing in the five-part pattern or the checklist produces an answer. Chapter 37 answers it only implicitly, through `CATS` and `NUMS`. My P1 patch adds one sentence. A reader with their own CSV does not know the path, the target column, the date, the seed, or which of the 1,820 lines depend on the Riverstone column names.

**Fix.** A required "Your own data" box per code chapter: the lines to change, in order, with the column names that must be renamed and the checks to run before trusting the result (row count, target rate, no target leakage).

### B5. "What are the common errors here, and what do they look like?" has no required artifact (S1)

Same as A3, at the level of the standard: the question is listed and no section of the template holds the answer. Add "Errors you will see" to the template in §4.

### B6. "Explained" is undefined, so naming counts as teaching (S2, S3)

**What.** §6.5 never defines what makes an explanation sufficient. The checker equates "the identifier appears in prose" with "explained". A bullet saying "`.sum()` sums the column" passes and teaches nothing a reader could not guess. My own bullets do this in places ("`get_n_leaves()` counts the final groups").

**Fix.** Define it by the reader: an explanation is sufficient when a reader who has never seen the line can say (a) what it produces, (b) what would happen if it were removed, and (c) one thing they could change in it. A bullet that answers only (a) is a caption, not an explanation. This definition is also the cold-reader rubric in E1.

### B7. The prediction rule ignores the printed page (S2)

See A6. §6.5 should specify placement, not only presence.

### B8. The length rule creates the state problem it does not mention (S2)

**What.** "12 to 20 lines the first time; split longer work into steps" is right for reading and wrong for running unless each step is runnable. Splitting a 41-line block into three makes three blocks that share names, which is A1 in miniature. The rule says nothing about keeping each step runnable or about the "Needs:" line.

**Fix.** Add to §6.5: "Each step must run on its own after the chapter's 'run first' block, and says what it needs."

### B9. The mathematics standard has no checker and no template (S3)

**What.** §6.5's last paragraph sets a standard for formulas: plain-English sentence, worked example with real numbers, statement of what changes when inputs change. Nothing checks it. Chapter 37's Gini and entropy formulas meet it; the regularization loss formulas ("loss = mean squared error + α × sum of squared weights") have no worked example with numbers, and the sigmoid's "what happens when *z* changes" is one sentence.

**Fix.** A formula checker is cheap: every blockquote containing `=` and a Greek letter or `×` must be followed within 30 lines by a line containing "=" and digits (a worked example). Rough, but it points a reader at the right places, which is all the code checker does too.

### B10. "Later uses can be brief" has no measure of brief (S2)

**What.** Without it, part chats either re-teach everything (chapter bloat, A10) or nothing (the current state). The 40-line explanation window in the checker becomes the de facto rule.

**Fix.** "Later use: one half-line reminder with the section where it was taught." Written in §6.5, enforced by the "Code words" table (term, meaning, first section), which then becomes the index the reminder points to.

---

## Part C. The checker (each item verified by running it)

### C1. The predict-before-running test passes on the word "prediction" in ordinary prose (S3)

**Evidence.** The regex is `before you run|predict|write down what you expect`, case-insensitive, applied to the whole file including code. I removed Chapter 37's one real prompt and the test still passed, on "makes a prediction" in the opening bullet. Every chapter that uses `predict_proba` passes automatically. The "Predict prompt" column in the baseline is meaningless for Parts IV and VI.

**Fix.** Match only `before you run` and `write down what you expect`, on prose outside code blocks and outside the Key terms list, and require it *per teaching section*, not per chapter.

### C2. The what-if test passes on "change it to" in ordinary prose (S3)

**Evidence.** Chapters 11, 13, and 39 contain "change it to" in sentences that are not what-ifs ("I can change it to count each order separately"). A chapter with no settings table and no measurement passes if it contains that phrase once.

**Fix.** Require the table header `What happens if you change it` and, within 60 lines after it, a code block followed by an output block. Count tables per chapter and report the count, not a boolean.

### C3. "Reading it" counts as code explanation, so output interpretation excuses unexplained code (S3)

**Evidence.** The EXPLAIN regex includes `reading it`. A block followed by "Reading it. AUC 0.740, a little below..." passes the coverage test whether or not any line of code is named. That is why the Naive Bayes worked example, the sigmoid block, and the test-set-once block in Chapter 37 were not flagged, though none has a line-level explanation.

**Fix.** Remove `reading it` from the EXPLAIN regex; it is the *output* explanation and §6.5 requires both. Add a separate check that an output block is followed by a "Reading it".

### C4. Two-letter settings are invisible, including the most important one in the chapter (S3)

**Evidence.** The identifier regex requires three characters, so `cv=`, `C=`, `on=`, `by=`, `ax=` can never be matched in prose and are excluded from the settings check. `C` is logistic regression's and the SVM's central setting; `cv` decides how every search is judged. The baseline note that Chapter 37 "never names `cv`" was made by a human reading, not by the tool, and the tool could not have found it.

**Fix.** Handle short arguments with a separate exact-match search for `` `cv=`` and `` `C=`` and `` `C` `` in prose, or lower the identifier length for keyword arguments only.

### C5. A setting named anywhere in the chapter counts as explained, including inside exercise answers (S3)

**Evidence.** `prose_words` is built from the whole chapter. `random_state` explained once in an exercise answer would clear every block in the body. The order of teaching, which §15.1 point 4 makes binding, is not checked at all.

**Fix.** Count a setting as explained only if it appears in prose *before* its first use in code, and report the line of first code use against the line of first prose mention.

### C6. One settings table anywhere clears the whole chapter (S3)

**Evidence.** The test is a single search for the phrase. After the patches, a chapter with one table for `train_test_split` and nine other functions with no table reports clean.

**Fix.** Per function: for every call `Name(arg=...)` whose class name is capitalized (a model or transformer), require a table within the section that first calls it. Report the list of functions with and without.

### C7. Coverage counts variable names as explanation (S3)

**Evidence.** `names` includes every identifier in the code: `X_tr`, `y_va`, `pipe`, `name`, `print`. A bullet list that names the variables and none of the functions or settings can reach 50%.

**Fix.** Weight settings and called functions above plain variables, or compute two coverages and report the settings one separately.

### C8. "0 flagged" does not mean "meets §6.5", and the Definition of Done says it does (S3)

**Evidence.** Chapter-level findings (no table, no prompt) are not counted in "blocks flagged". Chapters 26 and 27 show 0 flagged. They are good chapters, and the number would also be 0 for a chapter with fully bulleted blocks and no table at all. The DoD line "reports no unexplained blocks" is the only acceptance test, and C1 to C7 show it can be met without teaching.

**Fix.** The DoD item becomes two: (a) the checker's report is clean **and** (b) a cold reader (E1) answers the six questions for two examples chosen by the reviewer. The checker's output should say, in its first line, "this is a pointer, not a pass".

### C9. A what-if with no output passes (S3)

**Evidence.** Nothing checks that the block after a what-if is an output block with content. My findings file's `[run: W1]` placeholders, if pasted in as they are, would pass the checker and fail only `verify_python`, and only if the part chat runs it.

**Fix.** After any block introduced by "measured what-if", require a non-empty unlabeled block within 5 lines.

### C10. Config languages are not code to the checker, so Parts V and VI are under-counted (S3)

**Evidence.** `LANGS` contains sql, python, bash, dax, vba, and others, and not `yaml`, `json`, `toml`, `dockerfile`, `hcl`. Chapter 26's GitHub Actions workflow is a `yaml` block and was not examined. Part V (dbt `schema.yml`, Airflow, Docker, Terraform) and Part VI (model configs, prompts as JSON) are where a first-time reader meets the most settings per line, and the checker skips every one of them. The 52 and 54 flagged blocks reported for those parts are floors.

**Fix.** Add `yaml`, `yml`, `json`, `toml`, `dockerfile`, `hcl`, `ini` to `LANGS`, and treat each `key: value` line as a setting for the coverage test.

### C11. The 25-line rule is satisfied by the letter and broken by careful people (S3)

**Evidence.** My P14 Step 3 is 32 code lines, written while enforcing a 25-line limit. If the auditor overshoots, the part chats will. Also, the count excludes comment lines, so a 40-line block with 16 comments passes.

**Fix.** Run the checker on the patch file itself before patches are applied (it works on any markdown). Count comment lines at half weight.

### C12. Formulas are not examined (S3)

See B9. The checker reads only fenced blocks. The blockquote formulas that §6.5's last paragraph governs are invisible to it.

---

## Part D. The audit method and the Chapter 37 sample (my own work, red-teamed)

### D1. The auditor never ran anything; the runs and their reading sentences go to the chat that wrote the gap (S3)

**What.** Fourteen what-ifs are delegated to the Part IV chat because the companion data is not in the copy I can see (E5). That chat then writes the sentence that reads each result. The same author who left `random_state` unexplained for 1,820 lines writes the explanation of what changing it did. Nothing in the loop is independent, and Codex, the former independent reviewer, is gone.

**Fix.** Give the auditor the data (E5) so the what-ifs are run and read by a second pair of eyes, or route the reading sentences through a cold reader (E1) before they are accepted.

### D2. My tables contain unverified assertions, and at least two are wrong (S3)

Listed in B2: `min_child_weight` is not rows; CatBoost `min_data_in_leaf` only applies to non-symmetric growth; "`penalty=None` needs `drop='first'`" is overstated (lbfgs converges to one of many equivalent solutions and the model still predicts correctly; only the coefficients are unidentifiable); "more folds: steadier" is a common belief, not a measurement. I marked none of them as expected rather than measured. The fix is B2's marking rule, applied to my own file before it is used.

### D3. My cross-references were wrong (S1)

Listed in A12. Three of four unverified references pointed to sections that do not contain the claim. Fix: A12's grep rule, applied to the findings file before any patch is applied.

### D4. My explanations contain jargon the first-time reader has not met (S2)

"Coordinate-descent update order", "out-of-fold predictions", "leaf values", "minimum-norm", "bootstrap sample", "second derivatives" all appear in my bullets or tables without being explained. This is the curse of knowledge in the person auditing for it. Fix: a banned-term scan for the findings file, seeded from the Key terms lists of the chapters that come *before* the one being patched; any term not in those lists and not defined in the patch is a defect.

### D5. My P14 Step 3 breaks the 25-line rule (S3)

Verified: 32 code lines. It must be split into XGBoost and LightGBM as separate steps. C11 covers the process fix.

### D6. Patch dependencies are undeclared and line anchors will move (S4, becomes S1 for the applier)

`clone` is imported in P3 and used in P19 and P22; P22 does not say so. `nums=` is introduced in P5 and required by P18 and P23; if P5's code change is declined, both fall back, and P23's shortened exercise 12 must not be used. Line numbers in the findings file are correct for the current file and wrong after the first patch is applied. Fix: every patch lists "Requires: P3, P5" at its head; anchors are given as section plus the first code line of the block, never a line number alone; patches are applied in the listed order.

### D7. "29 needing a patch" is a judgment with no rubric, so a second auditor would get a different number (S3)

The findings file classifies each block by my reading. Another reader would count the sigmoid block as an exception and the GaussianNB block as fine. Without a rubric, the counts across 85 chapters are not comparable and the "hours per part" estimate is a guess dressed as a figure. Fix: the classification rule is B6's three questions; a block needs a patch if any first-use line fails (a), (b), or (c).

### D8. The order of work serves the auditor, not the reader (S2)

The brief orders parts by flag density: Part IV first. The first-time reader meets Chapter 6 (setup), Chapter 12 (167 SQL blocks), Chapter 17 (Python from zero) and Chapter 18 (pandas) first. If Chapter 17 does not teach `import pandas as pd` and `for` loops to the §6.5 standard, no reader reaches Chapter 37 to benefit from its 24 patches. Chapter 17 has 20 flagged blocks and Chapter 18 has 30; both are on the critical path of every reader. Fix: audit and patch in the reader's order for the first code the reader sees (6, 12, 17, 18), then by density. The density order is right for the *rest*, because Part IV is where the gap hurts most for someone who got there.

### D9. Patches add and never remove (S4, becomes S2)

See A10. Every patch in the findings file adds text. A removal budget was not part of the brief and should be.

### D10. The arithmetic of the whole plan (S4)

Chapter 37: 12 to 16 hours estimated, for 27 flagged blocks. The book has 611 flagged blocks and, after C1 to C10 are fixed, more. At Chapter 37's rate that is 300 to 400 hours of part-chat work plus runs, PDFs, and reviews, with no reviewer. The realistic failure mode is not "the standard is wrong" but "half the book meets it and half does not", and a book that switches teaching register between chapters reads worse than one that is consistently thin, because the reader learns to expect the tables and then loses them. Fix: decide the scope now. Options, in order of value per hour: (1) the Settings reference appendix and the "run first / Needs / your numbers may differ / errors you will see" standing blocks, applied to all 85 chapters by a tool, which fixes A1 to A4 everywhere for a few days' work; (2) full §6.5 for the reader's critical path (6, 12, 17, 18, 36, 37); (3) full §6.5 for the rest of Part IV and Part III; (4) the remainder as time allows, with the checker's report published in the chapter report so the gap is recorded rather than hidden.

---

## Part E. The process

### E1. There is no cold-reader test, so the standard is a regex (S3)

Nothing in the DoD asks whether a person who has not seen the code can now explain it. Fix: for each chapter, a chat or person who has not read it is given two examples chosen by the reviewer and asked the six §6.5 questions plus B6's three. Written answers are attached to the chapter report. This is the only check in the system that measures the thing the author is worried about.

### E2. One chat writes, patches, runs, reads, and verifies (S3)

With Codex gone, the Part IV chat is author, applier, and reviewer of its own chapters. §15.1 assumes a review pass "in your own chat" because that chat holds the context, which is true and is also why it cannot see what a stranger cannot follow. Fix: E1's cold reader, and the findings file's runs done by the auditor (D1).

### E3. Parallel chats produce inconsistent canonical explanations (S2)

See B3. The Settings reference appendix is the fix; it needs the owner's decision now, not after the audit, because every patch written before it exists will re-explain.

### E4. Version drift will silently invalidate outputs (S4, becomes S1 over time)

The outputs are pinned to library versions as of 17 September 2026. `verify_python.py` will start reporting mismatches on the boosting blocks the first time a library updates, and the choice will be to re-run everything or to freeze an environment file. No `requirements.txt` with exact pins is mentioned in the Tools section. Fix: a pinned environment file in `companion/`, named in Chapter 6, and the tolerance sentence of A2.

### E5. The auditor cannot see the companion data (S3)

The work copy of the project has `manuscript/`, `planning/`, `tools/`, `figures/` and no `companion/`. Every what-if in the findings file is therefore delegated. Fix: include `companion/` in the auditor's copy, or the audit produces patches only and never measurements, and the file should say so at the top.

### E6. No first-time reader has read any chapter (S2)

The whole system reasons about a first-time reader and has never watched one. Fix: one pilot reader per part, given the "first pass" route of A10 and the notebook of A13, asked to keep a log of every place they stopped. Their log is the real baseline; the checker's is a proxy.

### E7. The checker is the Definition of Done and it is edited by the coordinator without tests (S3)

The tracker records three corrections to the checker in a week, each of which changed every chapter's count. There is no test file with a known-good and a known-bad chapter. Fix: `tools/tests/` with one markdown fixture that must report 0 findings and one that must report each finding type once. Every edit to the checker runs both.

---

## The fixes that matter most, in the order to do them

1. **Define "taught" by the reader, not the regex** (B6, E1, C8). Three questions per first-use line; a cold reader answers them for two examples per chapter. Until this exists, every "0 flagged" is unearned.
2. **Fix the checker's demonstrated blind spots** (C1, C2, C3, C4, C6, C9, C10) and give it a test fixture (E7). Half a day. Then re-run the baseline; the numbers will go up, and they will be true.
3. **Create the Settings reference appendix** (B3) before any more patches are written, so patches link rather than re-explain, and the reader has one place to look.
4. **Add the four standing blocks to every code chapter by tool** (A1 "Needs", A2 "your numbers may differ", A3 "errors you will see", B4 "your own data"). This is the cheapest large improvement in the whole plan and it is not in §6.5 today.
5. **Generate a playground notebook per chapter from the manuscript** (A13). The verify tool already parses the blocks.
6. **Mark every table cell measured or expected** (B2), and grep every cross-reference (A12), including in the findings file before it is used.
7. **Re-order the work to the reader's path** (D8): Chapters 6, 12, 17, 18 alongside Part IV, not after Part VIII.
8. **Fix the sample before it is used as the pattern** (D2 to D6): split P14 Step 3, correct the two wrong table rows, mark assertions, fix the three cross-references, declare patch dependencies.
9. **Decide the scope with the arithmetic in front of you** (D10). Full §6.5 across 85 chapters is 300 to 400 hours with no reviewer. Choose the tiers.
