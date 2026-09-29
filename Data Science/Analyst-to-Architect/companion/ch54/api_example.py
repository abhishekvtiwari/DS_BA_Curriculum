#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 54 · Generative AI & Large Language Models
File: api_example.py - section 54.13's first real call: one order email, extracted by a hosted model.
Needs: an Anthropic account and key (section 54.13), `python -m pip install anthropic`, and the key in
  the ANTHROPIC_API_KEY environment variable. Costs a fraction of a cent per run.
How:  python api_example.py [email_012]
Not run in the book: it needs your own key, and its reply is the model's, not the book's.
Model and prices checked on 29 September 2026 (platform.claude.com/docs/en/about-claude/pricing).
Riverstone Supplies is fictional; every name and number here is invented.
"""
import sys

import anthropic

from extraction import WITH_EXAMPLE, emails, parse

name = sys.argv[1] if len(sys.argv) > 1 else "email_012"
client = anthropic.Anthropic()                 # reads ANTHROPIC_API_KEY from the environment

try:
    response = client.messages.create(
        model="claude-sonnet-5-5",             # a fixed model ID: re-run your evaluation before changing it
        max_tokens=1000,                       # a hard cap on the length (and cost) of the reply
        system=WITH_EXAMPLE,                   # the instructions, sent separately from the data
        messages=[{"role": "user", "content": "EMAIL:\n" + emails[name]}],
    )
except anthropic.RateLimitError:
    sys.exit("rate limited: wait a minute and run again")
except anthropic.APIError as error:
    sys.exit(f"the call failed: {error}")

reply = "".join(block.text for block in response.content if block.type == "text")
print(reply)
print("parsed:", parse(reply))
print(f"stop reason {response.stop_reason}, tokens in {response.usage.input_tokens}, "
      f"out {response.usage.output_tokens}")
