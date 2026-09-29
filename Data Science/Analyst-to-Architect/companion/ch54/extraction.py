#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 54 · Generative AI & Large Language Models
File: extraction.py - section 54.6's prompts and marking code, saved as a module so a script can import them
  (Chapter 29, section 29.2: one job per function, code other files can reuse).
How:  from extraction import WITH_EXAMPLE, evaluate
Needs: order_data/ (run generate_order_emails.py first) and mock_llm.py in this folder.
Riverstone Supplies is fictional; every name and number here is invented.
"""
import json
import pathlib

from mock_llm import complete

HERE = pathlib.Path(__file__).resolve().parent
with open(HERE / "order_data" / "ground_truth.json", encoding="utf-8") as f:
    truth = json.load(f)
emails = {name: (HERE / "order_data" / "emails" / f"{name}.txt").read_text(encoding="utf-8")
          for name in truth}

NAIVE = "Extract the order from this email."

INSTRUCTED = ("Extract the order from this email. Return JSON only, no prose, with keys "
              "customer, po_number, delivery_date (YYYY-MM-DD), items (product_code, quantity). "
              "Use null when a value is missing.")

WITH_EXAMPLE = INSTRUCTED + """

EXAMPLE
Email: PO-12345: 101 x 20, 107 x 5
Answer: {"customer": null, "po_number": "PO-12345", "delivery_date": null,
 "items": [{"product_code": "101", "quantity": 20}, {"product_code": "107", "quantity": 5}]}"""


def parse(reply):
    """Get a JSON object out of whatever the model returned, or None if there isn't one."""
    start, end = reply.find("{"), reply.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        got = json.loads(reply[start:end + 1])
    except json.JSONDecodeError:
        return None
    return got if isinstance(got, dict) else None


def mark(got, want):
    """Four checks: customer, PO number, delivery date, and the items in any order."""
    def pairs(items):
        return sorted((item.get("product_code"), item.get("quantity")) for item in items)
    return (got.get("customer") == want["customer"],
            got.get("po_number") == want["po_number"],
            got.get("delivery_date") == want["delivery_date"],
            pairs(got.get("items") or []) == pairs(want["items"]))


def evaluate(template, names):
    """Score one prompt template on the named emails: (fully correct, fields right, unparseable)."""
    exact = fields = unparseable = 0
    for name in names:
        got = parse(complete(template + "\nEMAIL:\n" + emails[name]))
        if got is None:
            unparseable += 1
            continue
        checks = mark(got, truth[name])
        fields += sum(checks)
        exact += all(checks)
    return exact, fields, unparseable
