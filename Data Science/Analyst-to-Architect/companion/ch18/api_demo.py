"""A tiny demonstration API for Chapter 18 (section 18.14). It runs on your own computer.

Start it in its own terminal, from your copy of this folder (work/ch18), and leave it running:

    python api_demo.py

It listens on http://localhost:8018 and answers one kind of request:

    GET /v1/orders?from=2025-12-01&to=2025-12-01&page=1&page_size=100
    header  Authorization: Bearer demo-token-18

It replies with Riverstone's order lines for those dates, one page at a time, as JSON:
{"page": 1, "pages": 3, "count": 296, "results": [...]}. The data comes from companion/full/*.parquet.
Stop it with Ctrl+C. Riverstone Supplies is fictional; every name and number is invented.
"""
import json
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import pandas as pd

HERE = Path(__file__).resolve().parent
TOKEN = "demo-token-18"
MAX_PAGE_SIZE = 500
PORT = 8018


def load_lines():
    """All order lines with their order's date, customer, and status, sorted by date."""
    full = HERE.parent.parent / "companion" / "full"     # works from work/ch18 and from companion/ch18
    orders = pd.read_parquet(full / "orders.parquet")
    items = pd.read_parquet(full / "order_items.parquet")
    lines = items.merge(orders, on="order_id").sort_values(["order_date", "order_id", "order_item_id"])
    return lines


LINES = load_lines()


def orders_page(query):
    """Return (status code, reply) for a query dictionary such as {"from": "2025-12-01", ...}."""
    try:
        start = date.fromisoformat(query.get("from", ""))
        end = date.fromisoformat(query.get("to", ""))
        page = int(query.get("page", "1"))
        page_size = int(query.get("page_size", "100"))
    except ValueError:
        return 400, {"error": "from and to must be dates (YYYY-MM-DD); page and page_size must be whole numbers"}
    if page < 1 or not 1 <= page_size <= MAX_PAGE_SIZE:
        return 400, {"error": f"page must be 1 or more, and page_size between 1 and {MAX_PAGE_SIZE}"}
    chosen = LINES[(LINES["order_date"] >= pd.Timestamp(start)) & (LINES["order_date"] <= pd.Timestamp(end))]
    count = len(chosen)
    pages = max(1, -(-count // page_size))             # rounds up: 296 lines in pages of 100 is 3 pages
    rows = chosen.iloc[(page - 1) * page_size: page * page_size]
    results = [
        {"order_item_id": int(r.order_item_id), "order_id": int(r.order_id),
         "order_date": r.order_date.strftime("%Y-%m-%d"), "customer_id": int(r.customer_id),
         "product_id": int(r.product_id), "quantity": int(r.quantity), "unit_price": float(r.unit_price),
         "discount_pct": float(r.discount_pct), "status": r.status}
        for r in rows.itertuples()
    ]
    return 200, {"page": page, "pages": pages, "count": count, "results": results}


class Handler(BaseHTTPRequestHandler):
    server_version = "RiverstoneDemoAPI/1.0"
    sys_version = ""

    def reply(self, code, body):
        data = (json.dumps(body, indent=2) + "\n").encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            return self.reply(401, {"error": "missing or invalid token"})
        if url.path != "/v1/orders":
            return self.reply(404, {"error": f"no such address: {url.path}"})
        query = {key: values[0] for key, values in parse_qs(url.query).items()}
        return self.reply(*orders_page(query))

    def log_message(self, *args):          # keep the terminal quiet
        pass


if __name__ == "__main__":
    print(f"Riverstone demo API on http://localhost:{PORT}  (Ctrl+C to stop)", flush=True)
    HTTPServer(("localhost", PORT), Handler).serve_forever()
