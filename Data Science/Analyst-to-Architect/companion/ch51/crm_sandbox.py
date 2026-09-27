"""Chapter 51 companion: a sandbox CRM's write API, standing in for a real CRM/ERP.
Extends the read-only mock from Chapter 45 with writes that behave like a real system:
  PATCH /api/leads/<id>       partial update (e.g. lead_score); needs Idempotency-Key
  POST  /api/leads            create a lead; fires a webhook for high-value leads
  GET   /api/leads/<id>       read one lead, including whatever the sync has written
  POST  /api/webhooks         register a URL to be called on lead.created_high_value

Idempotency: the CRM remembers the last 200 (Idempotency-Key -> response) pairs. Replaying the
same key returns the SAME response without applying the change twice - this is what makes retries safe.
The first PATCH to lead 9001 and lead 9002 fails once with a 503, to exercise retry logic.

Riverstone Supplies is fictional; every name and number is invented.
"""
import json, os, threading, time
import psycopg2
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import requests

SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
TOKEN = "practice-token-51"
STATE_DIR = "sync_state"

def _load(name, default):
    path = os.path.join(STATE_DIR, name)
    return json.load(open(path)) if os.path.exists(path) else default

def _save(name, value):
    os.makedirs(STATE_DIR, exist_ok=True)
    json.dump(value, open(os.path.join(STATE_DIR, name), "w"))

class Handler(BaseHTTPRequestHandler):
    fail_once = set()          # lead ids whose next PATCH should fail with 503, once
    idempotency = {}           # Idempotency-Key -> response body already sent
    webhooks = []              # registered {"url": ..., "event": ...}
    next_lead_id = 9001

    def log_message(self, *a): pass

    def _auth(self):
        return self.headers.get("Authorization") == f"Bearer {TOKEN}"

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def _send(self, code, body):
        raw = json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.end_headers(); self.wfile.write(raw)

    def do_GET(self):
        url = urlparse(self.path)
        if not self._auth():
            return self._send(401, {"error": "missing or invalid token"})
        if url.path == "/api/leads":
            q = parse_qs(url.query)
            page, size = int(q.get("page", ["1"])[0]), min(int(q.get("page_size", ["20"])[0]), 50)
            leads = _load("crm_leads.json", {})
            ids = sorted(int(i) for i in leads)
            chunk = ids[(page - 1) * size: page * size]
            data = [leads[str(i)] for i in chunk]
            next_page = page + 1 if page * size < len(ids) else None
            return self._send(200, {"data": data, "page": page, "next_page": next_page})
        if url.path.startswith("/api/leads/"):
            lead_id = url.path.rsplit("/", 1)[-1]
            leads = _load("crm_leads.json", {})
            if lead_id not in leads:
                return self._send(404, {"error": "no such lead"})
            return self._send(200, leads[lead_id])
        return self._send(404, {"error": "not found"})

    def do_PATCH(self):
        if not self._auth():
            return self._send(401, {"error": "missing or invalid token"})
        lead_id = self.path.rsplit("/", 1)[-1]
        idem_key = self.headers.get("Idempotency-Key")
        body = self._read_json()
        if idem_key and idem_key in Handler.idempotency:
            cached = Handler.idempotency[idem_key]
            return self._send(200, {**cached, "replayed": True})
        if lead_id in Handler.fail_once:
            Handler.fail_once.discard(lead_id)
            return self._send(503, {"error": "temporarily unavailable, try again"})
        leads = _load("crm_leads.json", {})
        if lead_id not in leads:
            return self._send(404, {"error": "no such lead"})
        leads[lead_id].update(body)
        leads[lead_id]["last_synced_at"] = body.get("_sync_time", "")
        _save("crm_leads.json", leads)
        response = {"lead_id": lead_id, "updated_fields": list(body.keys()), "replayed": False}
        if idem_key:
            Handler.idempotency[idem_key] = response
        return self._send(200, response)

    def do_POST(self):
        if not self._auth():
            return self._send(401, {"error": "missing or invalid token"})
        if self.path == "/api/webhooks":
            body = self._read_json()
            Handler.webhooks.append(body)
            return self._send(201, {"registered": body})
        if self.path == "/api/leads":
            body = self._read_json()
            leads = _load("crm_leads.json", {})
            lead_id = str(Handler.next_lead_id); Handler.next_lead_id += 1
            record = {"lead_id": lead_id, **body}
            leads[lead_id] = record
            _save("crm_leads.json", leads)
            if body.get("deal_value", 0) >= 200000:
                for hook in Handler.webhooks:
                    if hook.get("event") == "lead.created_high_value":
                        try:
                            requests.post(hook["url"], json={"event": "lead.created_high_value", "lead": record}, timeout=2)
                        except requests.RequestException:
                            pass
            return self._send(201, record)
        return self._send(404, {"error": "not found"})

def seed_leads(n=6):
    """Load a handful of real Riverstone leads into the sandbox CRM, as if already synced once."""
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:
        cur.execute("SELECT lead_id, company_name, email, source FROM leads ORDER BY lead_id LIMIT %s", [n])
        rows = cur.fetchall()
    conn.close()
    leads = {str(r[0]): {"lead_id": str(r[0]), "company_name": r[1], "email": r[2], "source": r[3],
                          "lead_score": None, "last_synced_at": None} for r in rows}
    _save("crm_leads.json", leads)
    return leads

def start_server(port=8051):
    Handler.fail_once = set(); Handler.idempotency = {}; Handler.webhooks = []; Handler.next_lead_id = 9001
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server

if __name__ == "__main__":
    seed_leads()
    s = start_server(); print("Sandbox CRM on http://127.0.0.1:8051  (Ctrl+C to stop)")
    threading.Event().wait()
