"""Chapter 45 companion (copied for Chapter 46): a tiny local stand-in for the CRM's REST API (read-only).
GET /api/leads?page=N&page_size=K  -> JSON {"data": [...], "page": N, "next_page": N+1 or null}
Needs header  Authorization: Bearer practice-token-45
To show rate limiting, the first request for page 2 returns 429 with Retry-After: 1.
Riverstone Supplies is fictional; every name and number is invented."""
import json, os, threading, psycopg2
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
TOKEN = "practice-token-45"

class Handler(BaseHTTPRequestHandler):
    limited_once = set()
    def log_message(self, *args):            # keep the console quiet
        pass
    def send_json(self, code, body, headers=None):
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/api/leads":
            return self.send_json(404, {"error": "not found"})
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            return self.send_json(401, {"error": "missing or invalid token"})
        q = parse_qs(url.query)
        page = int(q.get("page", ["1"])[0]); size = min(int(q.get("page_size", ["20"])[0]), 50)
        if page == 2 and "p2" not in Handler.limited_once:
            Handler.limited_once.add("p2")
            return self.send_json(429, {"error": "rate limit exceeded"}, {"Retry-After": "1"})
        conn = psycopg2.connect(SRC)
        with conn, conn.cursor() as cur:
            cur.execute("SELECT lead_id, created_at, company_name, email, source, owner_id FROM leads "
                        "ORDER BY lead_id LIMIT %s OFFSET %s", (size + 1, (page - 1) * size))
            rows = cur.fetchall()
        conn.close()
        data = [{"lead_id": r[0], "created_at": r[1].isoformat(), "company_name": r[2],
                 "email": r[3], "source": r[4], "owner_id": r[5]} for r in rows[:size]]
        self.send_json(200, {"data": data, "page": page, "next_page": page + 1 if len(rows) > size else None})

def start_server(port=8045):
    Handler.limited_once = set()
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server

if __name__ == "__main__":
    s = start_server(); print("Mock CRM API on http://127.0.0.1:8045/api/leads  (Ctrl+C to stop)")
    threading.Event().wait()
