#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 57 · LLMOps
File: provider.py - one function between your code and the model, with the three things production needs:
      a pinned model version, token accounting, and simulated failures.
The "provider" is Chapter 54's local stand-in (mock_llm.py), extended in two ways that make this chapter
runnable offline:
  * model='v2' behaves like a provider's next model version shipped behind the same name: same task,
    slightly different habits (it comments its answers, and on about 40% of emails it reverts to the
    date format the email itself used).
  * failure_rate makes a deterministic share of calls fail with RateLimitError or TimeoutError, so the
    retry and fallback code in section 57.8 runs for real.
None of this is a language model. Everything it teaches about versioning, cost, caching and fallback is.
Tested on: Python 3.12.3.
"""
from __future__ import annotations

import hashlib
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ch54'))
from mock_llm import complete as _complete            # Chapter 54's stand-in

PRICES = {                                            # US dollars per million tokens (Chapter 54, Sept 2026)
    'v1': {'input': 2.00, 'output': 10.00},
    'v2': {'input': 2.00, 'output': 10.00},
    'small': {'input': 0.75, 'output': 3.75},         # the cheaper fallback model
}
USD_TO_RUPEES = 88.0


class RateLimitError(RuntimeError):
    """The provider is throttling us. Retryable."""


class ProviderTimeout(RuntimeError):
    """The call took too long. Retryable, carefully."""


@dataclass
class Meter:
    """Every call, counted: this is where a monthly bill comes from."""
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    failures: int = 0
    by_model: dict = field(default_factory=dict)

    def record(self, model: str, prompt: str, reply: str) -> None:
        tokens_in, tokens_out = len(prompt) // 4, len(reply) // 4
        self.calls += 1
        self.input_tokens += tokens_in
        self.output_tokens += tokens_out
        bucket = self.by_model.setdefault(model, {'calls': 0, 'input': 0, 'output': 0})
        bucket['calls'] += 1
        bucket['input'] += tokens_in
        bucket['output'] += tokens_out

    def cost_rupees(self) -> float:
        total = 0.0
        for model, bucket in self.by_model.items():
            price = PRICES.get(model, PRICES['v1'])
            total += bucket['input'] / 1e6 * price['input'] + bucket['output'] / 1e6 * price['output']
        return total * USD_TO_RUPEES


def _should_fail(prompt: str, failure_rate: float) -> str | None:
    """Deterministic failures: the same prompt always fails the same way, so tests are reproducible."""
    if failure_rate <= 0:
        return None
    digest = int(hashlib.sha256(prompt.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    if digest < failure_rate * 0.6:
        return 'rate_limit'
    if digest < failure_rate:
        return 'timeout'
    return None


def call(prompt: str, model: str = 'v1', meter: Meter | None = None, failure_rate: float = 0.0) -> str:
    """The only place in the codebase that talks to a model. Swap providers here, nowhere else."""
    failure = _should_fail(prompt, failure_rate)
    if failure == 'rate_limit':
        if meter:
            meter.failures += 1
        raise RateLimitError('429 too many requests')
    if failure == 'timeout':
        if meter:
            meter.failures += 1
        raise ProviderTimeout('the request took longer than 10s')

    reply = _complete(prompt)
    if model == 'v2':
        # The next model version, shipped behind the same name: same task, slightly different habits.
        # It comments its answers, and on some emails it reverts to the date format the email used.
        digest = int(hashlib.sha256(prompt.encode()).hexdigest()[8:16], 16) / 0xFFFFFFFF
        if digest < 0.4:
            reply = re.sub(r'"delivery_date": "(\d{4})-(\d{2})-(\d{2})"',
                           lambda m: f'"delivery_date": "{m.group(3)}-{m.group(2)}-{m.group(1)}"', reply)
        reply = reply + '\n// extracted with care'
    if meter:
        meter.record(model, prompt, reply)
    return reply
