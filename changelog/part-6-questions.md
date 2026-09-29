# Part 6: questions for Abhishek

These are the chapter agents' questions, in reading order, each trimmed to the decision it needs. None of them blocks
the Part 6 PDF: every chapter builds, and the text as it stands uses the option described.

## Facts that need a real run or a source

1. **Ch 54: real-model numbers (rows 54.2 (e), 54.5, left Open/Fixed).** §54.13 teaches the real API but shows no
   successful reply, because there is no API key here and outputs can't be invented.
   - If you run `companion/ch54/api_example.py` with your key, the real three-prompt table can be printed and dated
     next to the stand-in's.
   - Do you want that?
2. **Ch 54: model landscape (row 54.4, Open).** These claims could not be checked against a primary source
   (openai.com is blocked here), so they are out of print:
   - GPT-6 Astra and GPT-5.6 Sol prices and specifications;
   - Qwen3.7 Flash pricing;
   - MiniMax's 80.2% SWE-bench score;
   - Grok's long-context pricing;
   - "prices fell 80%".

   Named models now live on a dated companion page, `companion/ch54/model-landscape-2026-09.md`, with only the
   entries checked on 29 Sep 2026. Keep it there, or move it into an appendix?
3. **Ch 54: the optional `tiktoken` cell** has no printed output, because its vocabulary download is blocked here.
   Run it once on a laptop, or leave it as "run it yourself"?
4. **Exchange rate.** The chapters disagree:
   - Ch 57 uses ₹88 per dollar as one named constant, `USD_TO_INR`. If you pick ₹87, change it in two places and
     re-run: the golden-set run becomes ₹4.66.
   - Ch 55 shows its cost at both ₹83 and ₹88.

   Which book rate should they use (fact sheet C8)?

## Content choices

5. **Ch 53: choosing the threshold.**
   - The scikit-learn model chooses it on 5-fold out-of-fold predictions, because a 20% validation set would hold
     only about 70 defects.
   - The PyTorch model uses a three-way split.
   - The test set is scored once in both.

   OK?
6. **Ch 53: PyTorch numbers were produced on one CPU thread.** On more threads the last digits can differ. Should
   the chapter tell readers to call `torch.set_num_threads(1)`?
7. **Ch 54: the stand-in model's behaviour changed.** It now picks its broken replies by a checksum of the email
   text. The headline results read 13 → 35 → 47 of 60 (was 12 → 35 → 47), and Ch 57 and Ch 58 were re-run on it.
   OK?
8. **Ch 55: refusal costs.** A wrong answer is assumed to cost ₹2,000 and a handover ₹10. At those prices the
   strictest refusal rule is cheapest, by one question in ten. The chapter keeps the middle rule and says why.
   Confirm the costs?
9. **Ch 55: two numbers moved when the checks were corrected.**
   - "The answer contained the fact" is now 12, not 18 (whole-word match).
   - Sections + BM25 recall is now 0.89, not 0.76 (chunker fix).
10. **Ch 56: which threshold does version 1 ship with?**
    - Finding 56.2's recommended option has the plant manager choosing 0.1.
    - Ch 53's story says the plant then "wanted more false alarms rather than fewer misses", which points to 0.01.

    Please confirm.
11. **Ch 56: `httpx2`.** FastAPI 0.141.1's test client imports `httpx2` first. The finding had guessed it was a typo
    for `httpx`. Confirm this reading?
12. **Ch 56: `code_commit: none`** is printed because the practice folder isn't a Git repository, and the text
    explains why. Make it one in §56.0 instead? Then every reader's printed hash would differ.
13. **Ch 56: the re-run changed two conclusions.**
    - Shadow mode now shows 30 v 16 disagreements, not 17 v 16.
    - The predicted-vs-true gap never opens.

    The chapter now teaches "price disagreements; the fast proxy measures change, not correctness". Confirm the
    new emphasis?
14. **Ch 56: the 2% audit** checks only about 9 parts a week at the simulation's 500 parts a week. Should the text
    say the simulated stream is a sample of the real line?
15. **Ch 57: row 57.25** uses option (b): a pinned version reached its retirement date and the config fell back
    to the provider's floating alias. Option (a) no longer fits Ch 54's rewritten story. Keep (b)?
16. **Ch 58: the review catch rate changes a headline conclusion (58.18).**
    - At the approved 90% catch rate, assisted intake costs about ₹1,530 a day, more than error-free typing at
      ₹600.
    - It beats typing only if a reviewer catches more than 97% of wrong drafts, or typing gets more than 1.2% of
      orders wrong.
    - The chapter recommends starting in shadow mode to measure both.

    Ch 63, 65 and 66 follow this. Confirm the framing?
17. **Lakh in prose, thousands in program output.** Prose uses ₹1,00,000; Python output prints ₹100,000 (Ch 44,
    55 and 58). OK?
18. **Ch 59:**
    - Option A for 59.1: two measured Riverstone cases and seven composites.
    - A third modelling error (Case 4's confounded prices) was added to pattern 4.
    - Lead scoring (case 3) is named as pattern 1's exception.

    OK?

## Not done here, for later passes

- **Ch 79 and 74 rows:** updated numbers from Ch 55, 56 and 57 are listed in the build notes for the Part 8 agents.
- **`tools/verify_shell.py`** hangs on a command whose output has no trailing newline, and on backslash-continued
  commands. Ch 56 works around both. A one-line tool fix was suggested (print a newline before the end marker);
  not applied yet.
- **Glossary (Appendix A):** new key terms from Ch 53–58, listed in the chapters' changelogs.
- **Hours (T12, final pass):** Part 6 is now 109–134 hours (was 91–116).
