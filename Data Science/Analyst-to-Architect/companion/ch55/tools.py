#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 55 · the tools the assistant is allowed to call.
A tool is an ordinary Python function plus a description the model can read. Nothing here is magic:
the "model" proposes a call, your code decides whether to run it, runs it, and hands the result back.
Sections 55.7 and 55.8 print every function in this file; checks/ch55_code_sync.py keeps them in step.
"""
import re

ORDERS = {                      # stands in for a read-only query against the ERP
    "SO-4471": dict(customer="Sharma Hardware", status="dispatched",
                    dispatched_on="2026-02-18", expected="2026-02-22",
                    items=[("101", 45), ("102", 20)]),
    "SO-4472": dict(customer="Green Leaf Hotels", status="packing",
                    dispatched_on=None, expected="2026-02-24", items=[("106", 75)]),
    "SO-4473": dict(customer="Metro Mart", status="on hold: credit limit",
                    dispatched_on=None, expected=None, items=[("108", 100)]),
}
PRICES = {"101": 430, "102": 750, "103": 115, "104": 620,
          "105": 1400, "106": 1150, "107": 380, "108": 290}
DISCOUNTS = [(5000, 0.12), (1000, 0.08), (500, 0.05), (0, 0.0)]


def order_status(order_id):
    """Look up one sales order. Read-only: it can never change anything."""
    order = ORDERS.get(order_id.upper())
    if order is None:
        return {"error": f"no such order {order_id}"}
    details = {k: v for k, v in order.items() if k != "items"}
    return {"order_id": order_id.upper(), **details, "lines": len(order["items"])}


def open_orders():
    """List the sales orders that have not been dispatched yet. Read-only."""
    return {"open_orders": [order_id for order_id, order in ORDERS.items()
                            if order["dispatched_on"] is None]}


def quote_price(product_code, quantity):
    """Price a quantity of one product, applying the published bulk discount policy."""
    if product_code not in PRICES:
        return {"error": f"unknown product code {product_code}"}
    if not isinstance(quantity, int) or quantity < 1:
        return {"error": f"invalid quantity {quantity!r}"}
    discount = next(rate for threshold, rate in DISCOUNTS if quantity >= threshold)
    unit = PRICES[product_code]
    net = round(unit * quantity * (1 - discount), 2)
    return {"product_code": product_code, "quantity": quantity, "list_price": unit,
            "discount_pct": round(discount * 100, 1), "net_amount": net,
            "gst_18_pct": round(net * 0.18, 2), "total_with_gst": round(net * 1.18, 2)}


TOOLS = {"order_status": order_status, "open_orders": open_orders,
         "quote_price": quote_price}


def propose_tool_call(question):
    """The stand-in model's tool choice; a real model returns structured output."""
    order = re.search(r"\bSO-\d{4}\b", question, re.IGNORECASE)
    if order:
        return {"tool": "order_status",
                "arguments": {"order_id": order.group(0).upper()}}
    price = re.search(r"\b(\d{2,5}) (?:units )?of (?:product )?(10[1-8])\b",
                      question, re.IGNORECASE)
    if price:
        return {"tool": "quote_price",
                "arguments": {"product_code": price.group(2),
                              "quantity": int(price.group(1))}}
    return None


def run_tool_call(call, allowed=None):
    """Your code, not the model, decides whether a proposed call may run."""
    if allowed is None:
        allowed = set(TOOLS)
    name = call.get("tool")
    if name not in TOOLS:
        return {"error": f"unknown tool {name!r}"}
    if name not in allowed:
        return {"error": f"tool {name!r} is not allowed here"}
    try:
        return TOOLS[name](**call["arguments"])
    except TypeError as problem:
        return {"error": f"bad arguments for {name}: {problem}"}
