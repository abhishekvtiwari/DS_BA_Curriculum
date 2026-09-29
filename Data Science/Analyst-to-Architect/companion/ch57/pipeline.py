#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 57 · LLMOps
File: pipeline.py - Chapter 54's order extraction, instrumented for production. Every function here is
  written out in the chapter, one cell at a time; this module keeps them together so a script (the CI
  check in exercise 5, the digest in exercise 10, Chapter 58's intake) can import them.
What: the prompt registry (section 57.2), build_prompt and evaluate (57.2), normalize_date and
  tolerant_parse (57.4), Cache (57.6) and call_with_fallback (57.8).
How:  from pipeline import PROMPTS, build_prompt, evaluate, tolerant_parse, Cache, call_with_fallback
Needs: ../ch54 (mock_llm.py, extraction.py, order_data/) and provider.py in this folder.
Tested on: Python 3.11 and 3.12 (standard library only).
Riverstone Supplies is fictional; every name and number here is invented.
"""
from __future__ import annotations

import hashlib
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ch54"))
from extraction import INSTRUCTED, NAIVE, WITH_EXAMPLE, emails, mark, parse, truth   # Chapter 54
from provider import (FALLBACK_MODEL, PINNED_MODEL, ProviderTimeout, RateLimitError,  # this chapter
                      call)

# Section 57.2: the prompt registry. The texts are Chapter 54's three prompts.
PROMPTS = {
    "v1": {"text": NAIVE, "model": PINNED_MODEL, "max_tokens": 500,
           "author": "Meera", "status": "retired", "score": None},
    "v2": {"text": INSTRUCTED, "model": PINNED_MODEL, "max_tokens": 500,
           "author": "Meera", "status": "retired", "score": None},
    "v3": {"text": WITH_EXAMPLE, "model": PINNED_MODEL, "max_tokens": 500,
           "author": "Meera", "status": "live", "score": None},
}


def build_prompt(version, email):
    """The instructions of one prompt version, then the marker line, then the email (Chapter 54)."""
    return PROMPTS[version]["text"] + "\nEMAIL:\n" + email


def evaluate(version, model=PINNED_MODEL, parser=parse, meter=None):
    """Run the golden set: every email, one call each, marked against the truth."""
    exact = unparseable = 0
    for name in truth:
        reply = call(build_prompt(version, emails[name]), model=model, meter=meter)
        order = parser(reply)
        if order is None:
            unparseable += 1
            continue
        exact += all(mark(order, truth[name]))
    return {"exact": exact, "of": len(truth), "accuracy": exact / len(truth),
            "unparseable": unparseable}


# Section 57.4: parsing that survives a model's habits.
def normalize_date(value):
    """Turn a day-first DD-MM-YYYY date into YYYY-MM-DD; leave anything else as it was."""
    if not isinstance(value, str):
        return value
    match = re.fullmatch(r"(\d{2})-(\d{2})-(\d{4})", value)
    if match:
        return f"{match.group(3)}-{match.group(2)}-{match.group(1)}"
    return value


def tolerant_parse(reply):
    """Chapter 54's parse, after removing comment lines, with the delivery date put right."""
    lines = [line for line in reply.splitlines() if not line.strip().startswith("//")]
    order = parse("\n".join(lines))
    if order is not None and "delivery_date" in order:
        order["delivery_date"] = normalize_date(order["delivery_date"])
    return order


# Section 57.6: an exact-match cache.
class Cache:
    """The same prompt to the same model returns the stored reply, with no call and no cost."""

    def __init__(self):
        self.store = {}
        self.hits = 0
        self.misses = 0

    def get_or_call(self, prompt, model, meter):
        key = hashlib.sha256((model + "\n" + prompt).encode("utf-8")).hexdigest()
        if key in self.store:
            self.hits += 1
            return self.store[key]
        self.misses += 1
        reply = call(prompt, model=model, meter=meter)
        self.store[key] = reply
        return reply

    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


# Section 57.8: retry, fall back, or give up honestly.
BACKOFF_SECONDS = 0.5               # Chapter 29's first wait: 0.5 s, then 1 s, then 2 s


def call_with_fallback(prompt, meter, failure_rate=0.0, attempts=3, backoff=BACKOFF_SECONDS):
    """Retry the pinned model, then try the cheaper one, then give up honestly."""
    for attempt in range(attempts):
        try:
            return call(prompt, model=PINNED_MODEL, meter=meter, failure_rate=failure_rate), "primary"
        except RateLimitError:
            if attempt < attempts - 1:                  # no point waiting after the last try
                time.sleep(backoff * 2 ** attempt)      # exponential backoff (Chapter 29)
        except ProviderTimeout:
            break                                       # one timeout: the prompt is slow; stop waiting
    try:
        return call(prompt, model=FALLBACK_MODEL, meter=meter, failure_rate=failure_rate), "fallback"
    except (RateLimitError, ProviderTimeout):
        return None, "failed"


def load_emails():
    """The 60 golden-set emails and their correct answers, as (truth, emails) dictionaries."""
    return truth, emails
