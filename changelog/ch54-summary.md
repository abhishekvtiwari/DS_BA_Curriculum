# Chapter 54 summary: Generative AI & Large Language Models

**Rows:** 62 for Ch 54 (40 content, 20 visual, 2 Reader's Journey). Verified 57 · Fixed 1 · Open 3 · Approved (fix elsewhere) 1.

## What changed

- **Honest about the stand-in.** New §54.0 "Setting up" runs the email generator (output shown) and lists the stand-in's four habits and what in a prompt switches each off. The Simplification note, the §54.6 table and Figure 54.3 all say the method is real and the numbers measure the stand-in's rules. `{name}` is gone from the prompts; `mock_llm.py` now breaks one reply in fifteen by a checksum of the email text. Headline numbers are now 13 → 35 → 47 of 60 (naive rose from 12 to 13 because a different set of replies breaks).
- **Bugs fixed and re-run.** BPE merges are boundary-safe ("order" is now one token, with a self-check); top-p is true nucleus sampling (top three tokens, 0.484/0.359/0.158); temperature 0 is greedy decoding; `parse` finds the JSON object and never crashes; the SVD is fitted once; Answers 4, 7 and 14 run.
- **Validation vs accuracy measured.** 59 of 60 load automatically; of those, 47 are right and 12 are wrong. Figure 54.4, the Recap and Answer 15 use these numbers.
- **Teaching.** Temperature worked by hand; `tokenize`, slice assignment, `**kwargs`, `np.cumsum`, `sys.path`, `.get`, `isinstance(bool)` explained; §54.6 split into five cells; LoRA arithmetic cell; every key term defined in the body; Ch 41/42/35/36/26/29 back-links checked against the current files.
- **New §54.13 "Your first real call" (optional).** Install, key and spend limit, bash/PowerShell/.env, the client, a real 401 error, the call argument by argument, reading text blocks and `usage`, a cost estimate, error handling, and a checked table of the same parts in `openai` and `google-genai`. `companion/ch54/api_example.py` is the script.
- **§54.12 landscape** reduced to dated price tiers with sources; named models moved to `companion/ch54/model-landscape-2026-09.md` (Anthropic and Google entries checked on 29 September 2026).
- **Exercise answers.** Answer 12 found a real hole: 9,999 passes section 54.7's range, so the answer adds a per-line limit. Answer 13 shows caching saves nothing for a 100-token prompt (512-token minimum).
- **Figures** redrawn at 720 px (smallest text 7.5 pt), renumbered in reading order, labels outside short bars, one colour per note.
- **New companion files:** `extraction.py`, `regression_test.py`, `api_example.py`, `model-landscape-2026-09.md`. `checks/ch54_check.py` rewritten (22 checks).

## Skipped or left Open, and why

- **54.2 (e)** and **54.5 step 7**: a real model's table and a successful call's output need an API key, and the book must not invent model outputs. The §54.13 cells that need a key are marked not-run.
- **54.4**: OpenAI's pricing page is blocked here and the other claims (Qwen3.7 Flash, MiniMax 80.2% SWE-bench, Grok, "prices fell 80%", "median ratio 4") have no primary source I could check. They're removed from print and listed for Abhishek.
- **54.13**: the optional `tiktoken` cell's output isn't shown because its vocabulary download is blocked here.

## Option picks

- 54.14: option (a), compute the instruction tokens from `WITH_EXAMPLE` after it exists (batching cell moved to §54.6).
- All other rows had one change and no options.

## Time needed

14–18 hours → **16–20 hours** over three weeks (new §54.0 and §54.13, by-hand work, split cells).

## Verification

- `verify_python`: 33 blocks run, 32 outputs checked, 0 mismatches (Python 3.11, NumPy 2, scikit-learn 1.9.1, anthropic 1.9.0). One cell calls api.anthropic.com with a wrong key and needs network access.
- `verify_shell`: 6 commands, 0 mismatches. `check_code_teaching`: remaining flags are length heuristics on the `validate` function and the answers.
- `checks/ch54_check.py`: 22 checks passed. `fig_check`: 0 figures under 7 pt. `restructure --check`: in order.
- Build: 49 pages; `layout_check` clean (map 20/20, no stranded heads or lead-ins, no sparse pages, tofu 0).
