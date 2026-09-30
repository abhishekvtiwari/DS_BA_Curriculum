# Chapter 72A: Data Structures & Algorithms Question Bank, changelog

One line per finding: `ID · what changed · where · option used`. Question IDs (Q72A-001 to Q72A-030) are unchanged, so every cross-reference from Ch 33 and Ch 77 still resolves.

- 72A.1 · Deleted the "A note on this chapter's numbering" paragraph; replaced by a "Chapter at a glance" box (You will practise, Before you start, Time needed, How built, Learn it in) and one reader-facing sentence in §72A.1 pointing to Ch 33 §33.10 · opening box, §72A.1 · —
- 72A.2 · Not applied here: Part 8 renumbering (72A → 73, Q-ID prefixes) is the final pass (D2, CLAUDE.md §5 step 4). IDs kept stable meanwhile · — · —
- 72A.3 · Every "Learn it in: Chapter 72" re-pointed to the current Ch 33 sections (33.1 Big-O, 33.2 structures, 33.3 hashing, 33.4 stacks/queues/deque, 33.5 recursion, 33.6 trees/graphs/cycles, 33.7 search/sort/bisect/heapq/Timsort, 33.8 memoization/lru_cache, 33.10 patterns), Ch 28 §28.4, Ch 40 §40.6, Ch 41 §41.3, Ch 29 §29.5; rapid-fire rows carry "Level · learn it in"; "this chat" sentence removed · every question · section numbers from Ch 33 as it stands after its reorder
- 72A.4 · "this chat…" sentence replaced by "Learn it in pointers name the chapter and section that teach each idea" · opening box · —
- 72A.5 · "this environment" replaced: every snippet run and outputs real, on Python 3.11.15 (the real version; the finding's "3.12" would have been untrue), book recommends 3.14, run them in a notebook (Ch 17) · opening box · modified wording to state the true version
- 72A.6 · Linked-list primer (node, .next, head, 3-node diagram, Node class, build/to_list walk, all run) before Q72A-025; Q72A-025 gets a printed trace (step, node, prev, head); Q72A-026 shows the test code, the set version and Floyd's version; both marked Beyond the book · §72A.7 · option (b); (a), a new Ch 33 section, needs Ch 33 (closed, not this chapter's file): question raised
- 72A.7 · Kept plain classes: Ch 29 §29.5 now teaches `__init__`/`self` ("Classes in twenty minutes"), so they are taught; added the 4-line reminder the finding offers and pointed to §29.5. Dataclasses not used: a default @dataclass sets `__hash__` to None, which would break the set-of-nodes version in Q72A-026 · §72A.7 primer, Q72A-025/027 · second alternative (reminder box)
- 72A.8 · BST primer (binary tree, invariant, insert 50/30/70/20 by hand with a drawing, in-order, sorted input degenerates) before Q72A-027; Q72A-027 now measures height 3 vs 7 for mixed vs sorted inserts · §72A.8 · primer here (the finding's alternative); a Ch 33 subsection would need Ch 33
- 72A.9 · Merge sort by hand box ([38, 27, 43, 3] split/merge diagram, 2 levels × 4 items); merge step split out as its own explained cell; merge_sort re-run; Q72A-023 now says bubble sort compares neighbours and swaps, up to n passes · Q72A-020, Q72A-023 · box placed here instead of Ch 33 §33.5 (Ch 33 not this chapter's file): question raised
- 72A.10 · Two-pointer/sliding-window primer at the start of §72A.3; printed trace for "racecar" (l, r) and for max_sum_subarray (i, in, out, sum, best: 8→7→9→6, best 9) · Q72A-008, Q72A-009 · trace tables here (the finding's alternative)
- 72A.11 · BFS `visited` is now a set (`{start}`, `.add`); Strong tier says O(V + E); output unchanged (A B C D E); new Common-mistakes row · Q72A-028 · —
- 72A.12 · Strong answer is `@lru_cache(maxsize=None)` (Ch 33 §33.8) with `cache_info()`; `cache={}` explained as Q72-001's trap in Extra points and a Common-mistakes row · Q72A-018 · lru_cache (first option)
- 72A.13 · "millions of times" → "hundreds of thousands of times"; call counts now printed by a counting cell: fib(2) computed 196,418 times (as the finding says) and 1,028,457 calls in total (the finding's 832,039 was wrong: 832,040 is fib(30)) · Q72A-018 · —
- 72A.14 · RecursionError on fib_memo(1500) shown in a run cell; bottom-up loop shown (fib(28), fib(1500) = 314 digits); pointer is Ch 33 §33.5 (the 1,000-frame limit lives there now, not §33.6) · Q72A-018 · —
- 72A.15 · "AVL, Red-Black exist in real database indexes" → in-memory libraries use red-black/AVL trees, databases use B-trees (Ch 28 §28.4) · Q72A-027 · —
- 72A.16 · "Chapter 12 for the database-index connection" → Ch 28 §28.4 (B-tree indexes) · Q72A-021 · —
- 72A.17 · Q72A-001 Learn it in → Ch 33 §33.1 (and Ch 48 for distributed scale) · Q72A-001 · —
- 72A.18 · "Big-O describes the worst case by default" → upper bound; worst case by convention; say "average case" (dict O(1) average) · Q72A-001 · —
- 72A.19 · Comparison count printed by a run cell: 12,497,500 = n(n−1)/2 vs 25,000,000; "Big-O drops the ½" · Q72A-002 · —
- 72A.20 · Quicksort sentence rewritten (O(log n) stack on average, unstable, O(n²) with bad pivots, random/median-of-three avoid it) · Q72A-020 · —
- 72A.21 · "stack overflow" → Python stops it with RecursionError (language-neutral name: stack overflow); same in Common mistakes · Q72A-019, Common mistakes · —
- 72A.22 · k > len(arr) shown by a run cell (returns 3); guard `if k <= 0 or k > len(arr): return None` in Extra points · Q72A-009 · —
- 72A.23 · "a tuple can" → only a tuple of hashable values; run cell shows `{(1, [2])}` → TypeError: unhashable type: 'list' · Q72A-014 · —
- 72A.24 · Q72A-015 answer rewritten (working __hash__, stable while in the set; built-in immutables yes; list/dict/set no; plain class instances hash by identity); Q72A-026's set version uses it · Q72A-015, Q72A-026 · —
- 72A.25 · "just at a smaller scale here" → "the same counting that builds Chapter 41's bag of words (section 41.3)" · Q72A-017 · —
- 72A.26 · Q70-041 references kept (the ID is unchanged in Ch 70, which now uses threshold 20000 and column K; the reference here is only to its never-ending loop); ID mapping belongs to the final pass · Q72A-019, Q72A-028 · —
- 72A.27 · "(see Q72A-018 below)", "(see Q72A-020 below)" · Q72A-005, Q72A-012 · first option (keep, mark as ahead)
- 72A.28 · Every question carries **Level** (Fresher/Mid/Senior) and **Roles** (DE, AE, MLE, DS, DA), legend in §72A.1; rapid-fire rows carry "Level · learn it in"; Karan's follow-up named Senior-level. Uses the Part 8 bank format adopted by Ch 70 (NOTES) rather than ●○○, so the banks share one scale · all questions · modified: Ch 70's scale
- 72A.29 · Time needed: 6–8 hours to run every snippet and answer aloud; 1 hour revision; +3–4 hours if the Ch 33 sections are new · opening box · —
- 72A.30 · "You will learn to … implement" → "You will practise …"; "do Chapter 33 first" in Before you start · opening box · —
- 72A.31 · Tools: "Python (Chapter 17, section 17.0), standard library only, as in Chapter 33", with the modules used and the version run · Project › Tools you'll need · —
- 72A.32 · Where this leads: "Looking back: Chapter 33 … Chapter 72 covers the Python gotchas"; 69, 74, 77 kept (numbers change in the final pass) · Where this leads · —
- 72A.33 · Retitled "In the real world: the DSA question that was really a scale question"; tag [Scale] → [+Scale] · In the real world · —
- V72A.1 · Both drafting passages deleted (see 72A.1, 72A.4); checked on the rebuilt p. 2 · opening box · before/after: `img/ch72a-V72A.1-before.png`, `img/ch72a-V72A.1-after.png`
- V72A.2 · (style pass) no stranded heading or half-empty page in the rebuild (layout_check: stranded_heads [], sparse_pages []) · —
- V72A.3 · (style pass) IDs such as Q72A-003 sit on one line in every rapid-fire table of the rebuild · —
- V72A.4, V72A.5, V72A.12 · (style pass) cover: no badge/date, full title, eyebrow; unchanged in the rebuild · —
- V72A.6 · (style pass) chapter map has page numbers (map_numbers 12/12) · —
- V72A.7 · (style pass) no pill spacing before punctuation in the rebuild · —
- V72A.8, V72A.9, V72A.10 · (style pass) no widows or split short tables in the rebuild · —
- V72A.11 · Big-O table column is now numbers only ("Steps for 5,000 items": 1, 13, 5,000, 61,439, 25,000,000) so the builder right-aligns it; "O(n log n)" kept on one line · Q72A-001 · —
- V72A.13 · (style pass) Python input and output styled differently in the rebuild · —

Other changes forced by the seven tests: every code answer now prints its own result in a run cell (26 outputs, all real) instead of a `# -> … (verified)` comment; timing cells marked as timings, with their numbers from a real run of `checks/ch72a_check.py`; Q72A-002 now times n = 2,500 and 5,000 to show the ×4 of O(n²); tags converted to Ch 69's twelve (`[Depth]` → [+Edge cases]/[+Signpost]); Q72A-021 shows the unsorted-input trap in a run cell and gets a predict-first prompt; Q72A-028 adds a DFS next to BFS (Ch 33 §33.6 teaches both); new Common-mistakes rows for the `visited` list and the mutable-default cache.
