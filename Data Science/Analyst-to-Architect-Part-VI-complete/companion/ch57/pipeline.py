#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 57 · the Chapter 54 extraction pipeline, instrumented for production.
Prompt versions, a tolerant parser, a cache, retries with a cheaper fallback, and a meter on every call.
"""
from __future__ import annotations

import json
import pathlib
import re
import time
from dataclasses import dataclass, field

from provider import Meter, ProviderTimeout, RateLimitError, call

DATA = pathlib.Path(__file__).resolve().parents[1] / 'ch54' / 'order_data'

PROMPTS = {                                   # a prompt is code: it has versions, and each has a score
    'v1': "Extract the order from this email ({name}).",
    'v2': ("Extract the order from this email ({name}). Return JSON only, no prose, with keys customer, "
           "po_number, delivery_date (YYYY-MM-DD), items (product_code, quantity). Use null when a value "
           "is missing."),
    'v3': ("Extract the order from this email ({name}). Return JSON only, no prose, with keys customer, "
           "po_number, delivery_date (YYYY-MM-DD), items (product_code, quantity). Use null when a value "
           "is missing.\n\nEXAMPLE\nEmail: PO-12345: 101 x 20, 107 x 5\nAnswer: "
           '{{"customer": null, "po_number": "PO-12345", "delivery_date": null, '
           '"items": [{{"product_code": "101", "quantity": 20}}, {{"product_code": "107", "quantity": 5}}]}}'),
}


def load_emails() -> tuple[dict, dict]:
    truth = json.load(open(DATA / 'ground_truth.json', encoding='utf-8'))
    emails = {name: (DATA / 'emails' / f'{name}.txt').read_text(encoding='utf-8') for name in truth}
    return truth, emails


def parse(reply: str, tolerant: bool = True) -> dict | None:
    """Get JSON out of whatever came back. Tolerant parsing is cheap insurance against a model's habits."""
    text = reply.split('```json')[-1].split('```')[0] if '```' in reply else reply
    if tolerant:
        text = '\n'.join(line for line in text.splitlines() if not line.strip().startswith('//'))
    try:
        order = json.loads(text)
    except json.JSONDecodeError:
        return None
    if tolerant:
        order['delivery_date'] = normalize_date(order.get('delivery_date'))
    return order


def normalize_date(value):
    """Never trust a model to format a date. Normalize it yourself, then validate."""
    if not isinstance(value, str):
        return value
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        return value
    match = re.fullmatch(r'(\d{2})-(\d{2})-(\d{4})', value)
    return f'{match.group(3)}-{match.group(2)}-{match.group(1)}' if match else value


@dataclass
class Cache:
    """Exact-match caching: the same prompt returns the stored reply, with no call and no cost."""
    store: dict = field(default_factory=dict)
    hits: int = 0
    misses: int = 0

    def get_or_call(self, prompt: str, **kwargs) -> str:
        if prompt in self.store:
            self.hits += 1
            return self.store[prompt]
        self.misses += 1
        reply = call(prompt, **kwargs)
        self.store[prompt] = reply
        return reply

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


def call_with_fallback(prompt: str, meter: Meter, failure_rate: float = 0.0,
                       attempts: int = 3, fallback_model: str = 'small') -> tuple[str | None, str]:
    """Retry the pinned model, then try the cheaper one, then give up honestly."""
    for attempt in range(attempts):
        try:
            return call(prompt, model='v1', meter=meter, failure_rate=failure_rate), 'primary'
        except RateLimitError:
            time.sleep(0.001 * 2 ** attempt)           # exponential backoff (Chapter 29)
        except ProviderTimeout:
            break                                       # a timeout twice is a slow prompt, not bad luck
    try:
        return call(prompt + ' ', model=fallback_model, meter=meter, failure_rate=failure_rate), 'fallback'
    except (RateLimitError, ProviderTimeout):
        return None, 'failed'


def evaluate(prompt_version: str, model: str = 'v1', tolerant: bool = True, meter: Meter | None = None) -> dict:
    """The golden set, run as a build step (section 57.3)."""
    truth, emails = load_emails()
    exact = unparseable = 0
    for name, want in truth.items():
        prompt = PROMPTS[prompt_version].format(name=name) + '\nEMAIL:\n' + emails[name]
        order = parse(call(prompt, model=model, meter=meter), tolerant=tolerant)
        if order is None:
            unparseable += 1
            continue
        checks = (order.get('customer') == want['customer'],
                  order.get('po_number') == want['po_number'],
                  order.get('delivery_date') == want['delivery_date'],
                  sorted((i['product_code'], i['quantity']) for i in order.get('items') or [])
                  == sorted((i['product_code'], i['quantity']) for i in want['items']))
        exact += all(checks)
    return {'prompt': prompt_version, 'model': model, 'exact': exact, 'of': len(truth),
            'unparseable': unparseable, 'accuracy': exact / len(truth)}
