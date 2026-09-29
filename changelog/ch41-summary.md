# Chapter 41 · NLP Foundations · summary

**What changed.** The chapter now builds each idea by hand before the library does it. It gains a §41.0 "Setting up": NLTK and gensim are installed in the terminal, the NLTK data (`punkt_tab`, `stopwords`, `wordnet`, `omw-1.4`, `vader_lexicon`) is downloaded in a cell, and the tickets are built with the companion script. The chapter now runs from `companion/tickets/`, as Ch 36 does. New worked examples: a bag of words on paper, the idf arithmetic, row normalization, cosine similarity on the mini table, multinomial Naive Bayes with Laplace smoothing, n-grams, per-class precision/recall/F1 with macro and weighted averages, a topics-by-hand factorization, and word neighbours by hand. Big code blocks are split into Jupyter-style cells, and every line is explained. All the prose claims that contradicted the output are fixed (Ex 3, Ex 5, Ex 6, "crack", "Fifteen", the wrong topic in the error explanation, "mostly Delivery").

**Data.** The tickets generator was fixed and the data rebuilt. It had two template glitches ("The you was fine", "2ndrd time"). It now also plants repeat contacts on the same order (second seed, 20242, so every other column is unchanged). A new §41.6 cell uses that data to check a topic against information it never saw: 53% of the angry NMF cluster are second contacts, against 21% of all tickets. The real-world story now quotes those computed numbers. Every output was re-run on the new data.

**Figures.** Both figures were redrawn (min 7.5 pt). Fig 41.1 shows the LDA and NMF heat maps side by side, each with its topic words. Fig 41.2 is a full-width scatter with shape and colour groups, a key, and no overlapping labels.

**Option picks.** (a) everywhere a choice was offered: add the NMF panel (41.33/V41.2), plant and compute repeat contacts (41.40), change the Ex 6 code (41.48), add the decimal demo (41.6). Adapted: 41.3 (the path was removed rather than explaining `../`), 41.38 (the data spells it "catalogue"), 41.19 (softmax is taught in Ch 53, not Ch 54).

**Skipped.** RJ-S3-46 is left Open for the Priya Menon / Priya Nambiar name clash (fact sheet C15).

**Time needed.** 12–15 hours over two weeks, in two sittings (previously 8–10 h).

**Verification.**
- verify_python: 54 blocks run, 53 outputs checked, 0 mismatches (needs `NLTK_ALLOW_PROXIED_URLOPEN=1` behind this proxy).
- verify_shell: 3 of 3 match.
- checks/ch41_check.py: all hand numbers pass.
- fig_check: 0 figures under 7 pt.
- restructure --check: in order.
- layout_check: clean (47 pages, map 14/14, no sparse pages, no stranded heads or lead-ins, tofu 0).
- check_code_teaching: 5 flags, all in Answers blocks that reuse code the chapter already taught.
