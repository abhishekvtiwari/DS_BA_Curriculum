# Coordinator reply to the Part V chat — 19 September 2026

*Paste this into the chat that wrote Part V (the Part I chat).*

Part V is received and merged: eight chapters, about 75,100 words, 23 figures, eight approved PDFs. All 21 figure references resolve. Part V is **complete and fully approved**, and the chapter map and progress tracker now say so.

The verification standard here is the highest in the book. Demonstrating the failure rather than describing it — the ID watermark actually missing orders 10174 and 10175, the plain `INSERT` actually failing on the primary key, the append version of the pipeline actually doubling the flash to ₹77,420, a real 503-then-retry on a brand-new lead, a real webhook delivery timed to a local inbox — is what makes these chapters teach. Keep doing that.

## My error, not yours

**The §6.5 code-teaching standard never reached you.** I wrote it on 18 September and routed the note to the Part II-A and Part III chats only. Part V ran in the Part I chat and was never told, so Chapters 51 and 52, written on 19 September, were written without it. No Part V chapter has the settings table it requires, and only Chapter 48 has a predict-before-you-run prompt. That is a routing failure of mine and it is logged as cross-part issue 16. From now on the note goes to every chat that writes chapters, named one by one.

The note is attached separately. In short: the first time a function or command takes settings, a table naming each one, what it means in plain words, the value used, and what changes if the reader changes it — then at least one changed version actually run, with the real output. That is what lets a reader run your code on their own data rather than only on Riverstone's.

`tools/check_code_teaching.py` (corrected twice since it was written: it now sees unlabeled terminal sessions as code, and matches keyword arguments rather than every variable assignment):

| Ch | Code blocks | Blocks flagged | Findings |
|---|---|---|---|
| 45 | 24 | 8 | 12 |
| 46 | 17 | 15 | 22 |
| 47 | 14 | 6 | 8 |
| 48 | 12 | 8 | 11 |
| 49 | 9 | 6 | 8 |
| 50 | 10 | 7 | 11 |
| 51 | 9 | 5 | 8 |
| 52 | 7 | 2 | 4 |

In proportion these are the best counts of any part written before the standard. Chapter 46 is the one to look at first. This is input for the review pass, not a reason to reopen approved chapters now.

## Two things I have fixed for you

**`tools/verify_python.py` now puts `--cwd` on `sys.path`**, exactly as you suggested, so a chapter's code can import its own companion modules without `PYTHONPATH`. Good catch, and the kind of report the coordinator exists to act on.

**The PDF cover template** no longer runs a long part name into the decorative bar; the bar moved above the kicker and the kicker has a maximum width. Part IV reported the same thing.

## Style

The cleanest part in the book for em dashes: two in 75,100 words. Two things to fix in the review pass:

| Ch | *genuinely* / *honestly* | American-spelling fixes |
|---|---|---|
| 47, 48 | 1 each | — |
| 49 | 1 | `centre`, `labelled` |
| 50 | 2 | `behaviour` |
| 51 | 5 | — |
| 52 | 4 (incl. *honestly*) | — |

Fifteen uses of *genuinely* across the part. It is on the banned list in instructions §5.2 because it reads as persuasion rather than statement; in most of these the sentence is stronger without it.

## Chapter 52 needs a decision from the author

Chapter 52 is the **only chapter in the book whose code has never been run**. Your sandbox had no cloud access, so the Dockerfile, the Kubernetes manifest, the Terraform configuration and the GitHub Actions workflow are parser-validated and trigger-simulated but not executed. You were right to say so plainly rather than imply otherwise.

I have logged it as cross-part issue 17 and put it on the pre-publication refresh list. The resolution is one of two things, and it is the author's call: run the chapter's project once on a real account before publication, or say in the chapter that these examples are validated but unexecuted. Please add the one-sentence note to the chapter's "At a glance" during the review pass, so the reader knows either way.

The **cloud provider** decision is still open. Your recommendation — provider-neutral concepts with AWS as the primary named example — is on the author's list.

## Accepted

- The Part V Riverstone facts go into the bible, subject to the check against Part II's Chapter 20 timeline that Chapter 45's report asked for.
- Your promises to later chapters are recorded; `planning/promises-from-approved-chapters.md` was regenerated from all written chapters.
- Manual checks (the PostgreSQL logical decoding setup by OS, the DPDP Act and GDPR wording) are on the refresh list.

## The review pass

Part V is complete, so instructions **§15.1** applies: read the eight chapters straight through in order, list what is wrong, work out the cause at the level of the part before touching anything, then fix in place and re-verify. Three things to carry in: the settings tables (§6.5), the fifteen *genuinely*s, and the one-sentence note on Chapter 52's unexecuted code.
