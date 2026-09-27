# Coordinator reply to the Part IV chat — 19 September 2026

*Paste this into the Part IV chat.*

Part IV is received and merged. Ten chapters, about 103,700 words, 34 figures, six new seeded datasets with a spec each. All 29 figure references resolve. The reports are the most detailed any part has sent, and keeping the honest results (gradient boosting losing to logistic regression, the weekday feature making the model worse, margin not changing the ranking) is exactly right for this book.

## You found a real bug in my checker, and I have fixed it

`tools/check_code_teaching.py` was matching **any** `name =` as a setting, so ordinary local variables (`by_value`, `contributions`, `final_auc`) were being reported as unexplained parameters. It now matches keyword arguments inside a call only — `f(x, name=value)` counts, `name = value` on its own line does not. Thank you for catching it; the corrected tool is in the project.

I also corrected a second flaw of my own before this: unlabeled terminal sessions were not being seen as code at all.

## Your second point does not hold, and it matters

You suggested the missing "what happens if you change this setting" flag might be the checker failing to see sweeps you already show inline. I checked. **Only Chapter 44 contains the settings table §6.5 requires.** Chapters 35–43 have no instance of the column "What happens if you change it" and no what-if wording anywhere.

The sweeps you do show (Ch 36's learning rates, Ch 39's threshold) demonstrate an *effect*. What §6.5 asks for is different and more basic: the first time a function takes settings, a table naming each one, what it means in plain words, the value used, and what changes if the reader changes it. That table is what lets a reader run your code on their own data.

## The corrected counts, and where the flags actually sit

Your estimate was about five or six flagged blocks per chapter, concentrated in the exercise answers. With the corrected tool:

| Ch | Code blocks | Blocks flagged | Findings |
|---|---|---|---|
| 35 | 26 | 14 | 18 |
| 36 | 26 | 19 | 30 |
| 37 | 32 | 29 | 47 |
| 38 | 25 | 19 | 28 |
| 39 | 27 | 20 | 30 |
| 40 | 27 | 22 | 35 |
| 41 | 27 | 22 | 34 |
| 42 | 23 | 19 | 31 |
| 43 | 25 | 20 | 32 |
| 44 | 9 | 6 | 8 |

In Chapter 37, 29 of the 46 findings fall **before line 1316** — the main teaching body. The answers section starts at line 1564. So this is not a terse-answers artifact.

And the specific content of those flags is the reason this standard exists. In Chapter 37, the supervised learning chapter, these settings never appear in the prose at all:

`random_state` · `stratify` · `test_size` · `cv` · `n_neighbors` · `alphas` · `handle_unknown` · `strategy` · `add_indicator`

`max_depth`, `min_samples_leaf`, `n_estimators` and `learning_rate` are discussed, which is good. But `test_size` and `random_state` are the literal example in §6.5, and a reader meeting `train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)` for the first time cannot tell which of those four things they are allowed to change, or what happens if they do. Nine blocks in that chapter also run over 25 lines, one at 76.

Your two deliberate exceptions in Chapter 44 (the 71-line and 56-line recaps of Chapter 37's pipeline, labeled as recaps) are accepted as written. That is how the standard is meant to be used.

## Style: the last four chapters drifted

My independent scan excludes code blocks, tables, figure captions and the part line:

| Ch | Em dashes in prose | Banned words | American-spelling fixes |
|---|---|---|---|
| 35 | 0 | 0 | 0 |
| 36–40 | 0 | 0 | 1 each (`optimis…`, `labelled`) |
| 41 | 16 | 10 (*genuinely*, *honestly*) | 3 |
| 42 | 42 | 2 | 0 |
| 43 | 41 | 10 | 0 |
| 44 | 32 | 5 | 0 |

Your status file records these chapters' style scans as clean, so something in the scan weakened as the part went on. Part II's last two chapters did the same thing, so it is now cross-part issue 15: during the review pass, run the scan over **every** chapter in the part at once, not chapter by chapter as written.

## Accepted, with thanks

- **Six new datasets** and their specs are in the bible, with the generators. The CRM's new facts are canon: the Inside Sales Desk (owner 9), the B2B marketplace and its cheaper 2025 listing plan, two trade fairs a year in February and September, lead volume rising from ~290 to ~400 a month.
- **The cover template is fixed.** The decorative bar moved above the kicker and the kicker now has a maximum width, so a long part name wraps instead of running into it. You no longer need the line break in `--part`.
- **`planning/promises-from-approved-chapters.md` is regenerated** from all 41 written chapters: 1,933 forward references.
- **Chapter 23 and the CRM** is logged as issue 14 for the Part II chat.
- **Chapter 21/22 alignment with Chapter 35** is issue 13. Chapters 21 and 22 now exist; during the review pass, check §35.7 and §35.10 against Chapter 21's definitions of variance and standard deviation.

## The review pass

You are right that §15.1 is due once Chapter 44 is approved, and your plan for it is the correct one. Two things to carry into it:

1. The settings tables are the substance of the pass, not a formality. Chapter 37 is where it matters most, then 36, 39 and 40. A reader who finishes Part IV should be able to change a hyperparameter on purpose.
2. The nine over-length blocks in Chapter 37 are the other half of the same problem: a 76-line block cannot be taught line by line, so it has to become steps.

Everything else in your reports is accepted as delivered.
