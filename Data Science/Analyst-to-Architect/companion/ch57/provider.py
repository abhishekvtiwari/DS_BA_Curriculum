#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 57 · LLMOps
File: provider.py - the one function between your code and the model, plus the meter that counts every call.
What: `call(prompt, model, meter, failure_rate)` answers with Chapter 54's local stand-in (mock_llm.py) and
  adds the two things this chapter needs to simulate offline:
    * model="workhorse-002" behaves like the provider's next version: the same task, with two new habits.
      It puts a comment line inside its JSON, and on about 40% of emails it writes the delivery date
      day first (DD-MM-YYYY) instead of YYYY-MM-DD. Which emails is decided by a checksum of the prompt.
    * failure_rate makes a share of calls fail with RateLimitError or ProviderTimeout. The failures are
      deterministic: the same prompt sent to the same model always fails, or succeeds, the same way, so
      every run gives the same numbers (section 57.8).
  `Meter` is section 57.5's meter, and PRICES and USD_TO_INR are its price table.
None of this is a language model. What it teaches about versions, cost, caching and fallback is real.
How:  from provider import call, Meter, RateLimitError, ProviderTimeout
Tested on: Python 3.11 and 3.12 (standard library only).
Riverstone Supplies is fictional; every name and number here is invented.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch54"))
from mock_llm import complete                         # Chapter 54's stand-in model

PINNED_MODEL = "workhorse-001"      # the version Riverstone tested and pinned
NEW_MODEL = "workhorse-002"         # the provider's next version (section 57.4)
FALLBACK_MODEL = "volume-001"       # a cheaper model for when the pinned one fails (section 57.8)

# Section 57.5. US dollars per million tokens (input, output): the workhorse and volume tiers of
# Chapter 54's section 54.12, checked 29 September 2026.
PRICES = {
    "workhorse-001": (2.00, 10.00),
    "workhorse-002": (2.00, 10.00),
    "volume-001": (0.75, 3.75),
}
USD_TO_INR = 88.0                   # rupees per US dollar; check today's rate before you quote a bill


class Meter:
    """Every call, counted: tokens in and out per model, and every provider error by kind."""

    def __init__(self):
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.by_model = {}          # model -> [tokens in, tokens out]
        self.errors = {}            # kind of error -> how many

    def record(self, model, prompt, reply):
        tokens_in, tokens_out = len(prompt) // 4, len(reply) // 4    # Chapter 54's four characters a token
        self.calls += 1
        self.input_tokens += tokens_in
        self.output_tokens += tokens_out
        if model not in self.by_model:
            self.by_model[model] = [0, 0]
        self.by_model[model][0] += tokens_in
        self.by_model[model][1] += tokens_out

    def record_error(self, kind):
        self.errors[kind] = self.errors.get(kind, 0) + 1

    def cost_rupees(self):
        dollars = 0.0
        for model, (tokens_in, tokens_out) in self.by_model.items():
            price_in, price_out = PRICES[model]
            dollars += tokens_in / 1_000_000 * price_in + tokens_out / 1_000_000 * price_out
        return dollars * USD_TO_INR


class RateLimitError(Exception):
    """429: the provider is throttling us. Wait, then try again."""


class ProviderTimeout(Exception):
    """The call took longer than the time we allow. Retrying at once rarely helps."""


def _share(model, prompt, salt):
    """A number between 0 and 1 fixed by the model and the prompt: the same input always gives the same number."""
    digest = hashlib.sha256(f"{salt}|{model}|{prompt}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) / 0xFFFFFFFF


def _new_habits(reply, prompt):
    """What workhorse-002 does differently: a comment line inside the JSON, and some dates day first."""
    lines = reply.splitlines()
    if _share(NEW_MODEL, prompt, "date") < 0.4:
        for i, line in enumerate(lines):
            if line.strip().startswith('"delivery_date": "'):
                value = line.split('"')[3]
                if len(value) == 10 and value[4] == "-":
                    lines[i] = line.replace(value, f"{value[8:10]}-{value[5:7]}-{value[0:4]}")
    for i, line in enumerate(lines):
        if line.strip() == "{":
            lines.insert(i + 1, "  // fields extracted from the email body")
            break
    return "\n".join(lines)


def call(prompt, model=PINNED_MODEL, meter=None, failure_rate=0.0):
    """The only place in the code that talks to a model. Swap providers here, nowhere else."""
    if model not in PRICES:
        raise ValueError(f"unknown model {model!r}")
    share = _share(model, prompt, "failure")
    if share < failure_rate * 0.6:                    # three failures in five are rate limits
        if meter is not None:
            meter.record_error("rate limit")
        raise RateLimitError("429 too many requests")
    if share < failure_rate:                          # the other two are timeouts
        if meter is not None:
            meter.record_error("timeout")
        raise ProviderTimeout("no reply within 10 seconds")
    reply = complete(prompt)
    if model == NEW_MODEL:
        reply = _new_habits(reply, prompt)
    if meter is not None:
        meter.record(model, prompt, reply)
    return reply
