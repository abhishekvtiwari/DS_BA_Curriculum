#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 29 · Python as Software, Not Scripts
File: mock_crm_api.py - a local stand-in for Riverstone's CRM leads API, for practicing robust clients (section 29.9).
What it does: serves the 43 leads in leads.json (exported from riverstone_2025) at GET /leads?page=N&page_size=M,
  requires the header X-API-Key: demo-key, and fails on purpose: the first request for page 2 gets 503, and the
  first request for page 3 gets 429 with Retry-After: 1. Every later request succeeds.
How:  python3 mock_crm_api.py            (serves on http://127.0.0.1:8029 until Ctrl+C)
      or from Python: server, url = start_server()   ...   server.shutdown()
Tested on: Python 3.12.3 (standard library only). Nothing leaves your machine.
Riverstone Supplies is fictional; every name and number is invented.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

LEADS = json.loads((Path(__file__).parent / "leads.json").read_text())
API_KEY = "demo-key"


def make_handler(failures: dict[int, list[int]]) -> type[BaseHTTPRequestHandler]:
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: object) -> None:  # keep the console quiet
            pass

        def send_json(self, status: int, body: dict, headers: dict[str, str] | None = None) -> None:
            payload = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            for key, value in (headers or {}).items():
                self.send_header(key, value)
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self) -> None:
            url = urlparse(self.path)
            if url.path != "/leads":
                return self.send_json(404, {"error": "not found"})
            if self.headers.get("X-API-Key") != API_KEY:
                return self.send_json(401, {"error": "invalid or missing API key"})
            query = parse_qs(url.query)
            page = int(query.get("page", ["1"])[0])
            size = min(int(query.get("page_size", ["10"])[0]), 50)
            with lock:
                planned = failures.get(page, [])
                status = planned.pop(0) if planned else 200
            if status == 429:
                return self.send_json(429, {"error": "rate limit exceeded"}, {"Retry-After": "1"})
            if status != 200:
                return self.send_json(status, {"error": "temporarily unavailable"})
            start = (page - 1) * size
            items = LEADS[start:start + size]
            more = start + size < len(LEADS)
            self.send_json(200, {"page": page, "items": items, "next_page": page + 1 if more else None,
                                 "total": len(LEADS)})

    return Handler


class MockServer(ThreadingHTTPServer):
    daemon_threads = True

    def shutdown(self) -> None:
        """Stop serving and release the port, so a new server can start on it straight away."""
        super().shutdown()
        self.server_close()


def start_server(port: int = 0, failures: dict[int, list[int]] | None = None) -> tuple[MockServer, str]:
    plan = {2: [503], 3: [429]} if failures is None else failures
    server = MockServer(("127.0.0.1", port), make_handler(plan))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


if __name__ == "__main__":
    srv, base = start_server(8029)
    print(f"mock CRM API on {base}/leads (key: {API_KEY}); Ctrl+C to stop")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        srv.shutdown()
