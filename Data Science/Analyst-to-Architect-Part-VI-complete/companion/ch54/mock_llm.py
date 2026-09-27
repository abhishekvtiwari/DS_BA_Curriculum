#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 54 · Generative AI & Large Language Models
File: mock_llm.py - a local stand-in for a hosted language model, so the chapter's code runs offline.
What it is: NOT a language model. It is a deterministic function that reads the prompt, extracts the
  order with ordinary text rules, and replies in the shape a real model would - including the habits
  that make prompting matter:
    * it wraps its JSON in chat and markdown fences unless the prompt says to return JSON only;
    * it copies dates in whatever format the email used unless the prompt names an output format;
    * it omits a field it could not find unless the prompt says to use null;
    * it takes only the first item on a line unless the prompt shows an example with several;
    * it occasionally returns broken JSON (email 7, 23, 41 and 58), as real models occasionally do.
Why: model weights cannot be downloaded in the book's sandbox and no reader should need a paid key to
  follow the chapter. Every prompting lesson here is real; the "model" is not. Section 54.12 lists the
  provider code you would use instead, and the companion file api_example.py shows it.
How:  from mock_llm import complete;  complete(prompt)  ->  str
Tested on: Python 3.12.3 (standard library only).
Riverstone Supplies is fictional; every name and number here is invented.
"""
from __future__ import annotations

import json
import re

PRODUCT_CODES = {'101', '102', '103', '104', '105', '106', '107', '108'}
MONTHS = {m.lower(): i for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
     'September', 'October', 'November', 'December'], start=1)}


def _po_number(text: str) -> str | None:
    match = re.search(r'PO-\d{4,6}', text)
    return match.group(0) if match else None


def _customer(text: str) -> str | None:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    return lines[-1] if lines else None


def _raw_date(text: str) -> str | None:
    for pattern in (r'(?:by|Required by:|deliver|Delivery|delivery)\s*:?\s*'
                    r'(\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+\w+\s+\d{4}|\d{1,2}\s+\w+)',):
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None


def _normalize_date(raw: str | None) -> str | None:
    """Turn any of the shapes customers write into YYYY-MM-DD, or None if the year is missing."""
    if raw is None:
        return None
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', raw):
        return raw
    match = re.fullmatch(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', raw)
    if match:
        day, month, year = (int(part) for part in match.groups())
        return f'{year:04d}-{month:02d}-{day:02d}'
    match = re.fullmatch(r'(\d{1,2})\s+(\w+)\s+(\d{4})', raw)
    if match and match.group(2).lower() in MONTHS:
        return f'{int(match.group(3)):04d}-{MONTHS[match.group(2).lower()]:02d}-{int(match.group(1)):02d}'
    match = re.fullmatch(r'(\d{1,2})\s+(\w{3,})', raw)          # "04 Mar": the year is missing
    if match:
        for name, number in MONTHS.items():
            if name.startswith(match.group(2).lower()[:3]):
                return f'2026-{number:02d}-{int(match.group(1)):02d}'
    return None


def _items(text: str, every_match: bool = False) -> list[dict]:
    found: list[dict] = []
    patterns = [r'\b(10[1-8])\b[^\n\d]{0,30}?(\d{1,4})\s*(?:nos|units|pcs)?\b',
                r'(\d{1,4})\s+of the [^(\n]+\(code\s*(10[1-8])\)']
    for line in text.splitlines():
        matches = list(re.finditer(patterns[0], line)) if every_match else list(re.finditer(patterns[0], line))[:1]
        if matches:
            for match in matches:
                if match.group(1) in PRODUCT_CODES:
                    found.append({'product_code': match.group(1), 'quantity': int(match.group(2))})
            continue
        for match in re.finditer(patterns[1], line):
            found.append({'product_code': match.group(2), 'quantity': int(match.group(1))})
    seen, unique = set(), []
    for item in found:
        if item['product_code'] not in seen:
            seen.add(item['product_code'])
            unique.append(item)
    return unique


def complete(prompt: str, temperature: float = 0.0) -> str:
    """Return what a language model would return for this prompt, given this email."""
    email = prompt.split('EMAIL:', 1)[-1] if 'EMAIL:' in prompt else prompt
    wants_json_only = 'json only' in prompt.lower() or 'no prose' in prompt.lower()
    wants_iso = 'yyyy-mm-dd' in prompt.lower()
    wants_null = 'null' in prompt.lower()

    raw_date = _raw_date(email)
    result = {
        'customer': _customer(email),
        'po_number': _po_number(email),
        'delivery_date': _normalize_date(raw_date) if wants_iso else raw_date,
        'items': _items(email, every_match='EXAMPLE' in prompt),
    }
    if not wants_null:
        result = {key: value for key, value in result.items() if value is not None}

    body = json.dumps(result, indent=2)

    number = re.search(r'email_(\d{3})', prompt)
    troublesome = number and number.group(1) in {'007', '023', '041', '058'}
    if troublesome and not wants_json_only:
        body = body.rstrip('}') + ',\n}'                      # a trailing comma: valid to a human, not to json.loads
    if not wants_json_only:
        return ("Sure! Here's the order extracted from that email:\n\n"
                f"```json\n{body}\n```\n\nLet me know if you'd like anything changed.")
    return body


if __name__ == '__main__':
    import sys
    print(complete(sys.stdin.read()))
