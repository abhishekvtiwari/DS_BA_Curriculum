# The model landscape, 29 September 2026

*Analyst to Architect · Chapter 54 · companion page for section 54.12*

Model names and prices change within weeks. This page lists the models behind section 54.12's price tiers **as they stood on 29 September 2026**, each with the page it was checked against. Before you quote any number from it, open the provider's pricing page and check again.

All prices are US dollars per million tokens, input / output, at the standard (not batch) rate.

## Checked models

| Tier | Model | Price (input / output) | Notes | Source, checked 29 Sep 2026 |
|---|---|---|---|---|
| Frontier | Claude Fable 5.1 (`claude-fable-5-1`) | $10 / $50 | 1M-token context; cache reads $0.25 (2.5% of input) | Anthropic pricing page; models overview |
| Strong and cheaper | Claude Opus 5.5 (`claude-opus-5-5`) | $4 / $20 | 1M-token context; cache reads $0.20 (5% of input) | Anthropic pricing page; models overview |
| Strong and cheaper | Claude Opus 5 (`claude-opus-5`) | $5 / $25 | cache reads $0.50 (10%) | Anthropic pricing page |
| Workhorse | Claude Sonnet 5.5 (`claude-sonnet-5-5`) | $2 / $10 | released 28 September 2026; 1M-token context; rejects non-default `temperature`, `top_p`, `top_k`; minimum cacheable prompt 512 tokens | Anthropic Sonnet 5.5 model page |
| Workhorse | Claude Sonnet 5 (`claude-sonnet-5`) | $2 / $10 | the launch price, announced as introductory until 31 August 2026, is now the standard price | Anthropic pricing page (footnote 3) |
| Workhorse | Gemini 3.1 Pro (Preview) | $2 / $12 | $4 / $18 for input over 200,000 tokens; cache reads $0.20 | Google Cloud Vertex AI pricing page |
| Volume | Gemini 3.8 Flash | $0.75 / $3.75 | introductory price through 31 December 2026; $1.50 / $7.50 from 1 January 2027 | Google Cloud Vertex AI pricing page |

Other facts used in section 54.12, from the same pages:

- **Batch:** Anthropic's Batch API is 50% off input and output.
- **Cache reads:** 10% of the input price on most Claude models and on the Gemini models above; 2.5% on Claude Fable 5.1 and 5% on Claude Opus 5.5.
- **Long context:** Anthropic's Claude 4.6 and later models charge the same rate across the full 1M-token window; Gemini 3.1 Pro charges more above 200,000 input tokens.
- **Model IDs:** every current Claude model ID is a pinned snapshot, including IDs without a date; for models before the 4.6 generation, an alias such as `claude-haiku-4-5` points at a dated ID, `claude-haiku-4-5-20251001`.
- **Knowledge cutoff:** Anthropic gives a reliable knowledge cutoff of June 2026 for Claude Fable 5.1, Opus 5.5 and Sonnet 5.5.

## Sources

- Anthropic, *Pricing*: https://platform.claude.com/docs/en/about-claude/pricing (checked 29 September 2026)
- Anthropic, *Models overview*: https://platform.claude.com/docs/en/about-claude/models/overview (checked 29 September 2026)
- Anthropic, *Claude Sonnet 5.5*: https://platform.claude.com/docs/en/models/sonnet-5-5/overview (checked 29 September 2026)
- Google Cloud, *Vertex AI pricing* (generative AI): https://cloud.google.com/vertex-ai/generative-ai/pricing (checked 29 September 2026)

## Not listed here

OpenAI's models, and open-weight families such as Qwen, DeepSeek, Kimi, MiniMax and Llama, belong in this table too, but their pricing pages could not be checked for this edition. Look them up on the providers' own pages, and add a row with the date you checked.
