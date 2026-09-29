"""Chapter 51 companion: a sandbox CRM's write API, standing in for a real CRM.
It extends Chapter 45's read-only practice API with writes that behave like a real system's:

  GET   /api/leads?page=N&page_size=K     one page of leads: {"data": [...], "page": N, "next_page": N+1 or null}
  GET   /api/leads/<id>                   one lead
  PATCH /api/leads/<id>                   change only the fields sent (a partial update); 404 if no such lead
  PUT   /api/leads/<id>                   replace the whole record with what's sent
  POST  /api/leads                        create a lead; fires lead.created_high_value for deal_value >= 200000
  GET   /api/accounts?page=N&page_size=K  one page of customer accounts
  GET   /api/accounts/<id>                one account
  PATCH /api/accounts/<id>                upsert by the ERP's customer id: update the account, or create it if
                                          it doesn't exist yet ("action": "created" or "updated")
  POST  /api/webhooks                     register {"url": ..., "event": ...}

Every request needs the header  Authorization: Bearer <token>  (default token practice-token-51).
Idempotency: a PATCH may carry an Idempotency-Key header. The sandbox remembers the response for each key;
a request that repeats a key gets that same response back with "replayed": true, and changes nothing.
Webhooks are signed: header X-Signature is the HMAC-SHA256 of the raw body with WEBHOOK_SECRET.

Test scaffolding a real CRM doesn't have: simulate_failure(path, kind) makes the next write to that path fail
once, with kind "503", "429" (with Retry-After: 1), or "slow" (the change is applied, but the answer comes
3 seconds late, so a client with a shorter timeout gives up waiting).

State lives in sync_state/crm_leads.json and sync_state/crm_accounts.json, so it survives a restart.
Riverstone Supplies is fictional; every name and number is invented.
"""
import hashlib, hmac, json, os, threading, time
import psycopg2
import requests
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

SRC = os.environ.get("RIVERSTONE_SOURCE", "dbname=riverstone_source")
TOKEN = os.environ.get("CRM_API_TOKEN", "practice-token-51")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "practice-secret-51")
STATE_DIR = "sync_state"
KINDS = {"leads": "crm_leads.json", "accounts": "crm_accounts.json"}
SLOW_SECONDS = 3
_lock = threading.Lock()


def _load(kind):
    path = os.path.join(STATE_DIR, KINDS[kind])
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def _save(kind, records):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(os.path.join(STATE_DIR, KINDS[kind]), "w") as f:
        json.dump(records, f)


class Handler(BaseHTTPRequestHandler):
    planned = {}        # "leads/4" -> ["429", ...]: failures to produce on the next writes to that path
    idempotency = {}    # Idempotency-Key -> the response already sent for it
    webhooks = []       # registered {"url": ..., "event": ...}
    next_lead_id = 9001
    next_event = 1

    def log_message(self, *a):
        pass

    def _auth(self):
        return self.headers.get("Authorization") == f"Bearer {TOKEN}"

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length) or b"{}")

    def _send(self, code, body, headers=None):
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def _route(self):
        """'/api/leads/4' -> ('leads', '4'); '/api/leads' -> ('leads', None)."""
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "api" and parts[1] in KINDS:
            return parts[1], (parts[2] if len(parts) > 2 else None)
        return None, None

    def do_GET(self):
        if not self._auth():
            return self._send(401, {"error": "missing or invalid token"})
        kind, rid = self._route()
        if kind is None:
            return self._send(404, {"error": "not found"})
        records = _load(kind)
        if rid is not None:
            if rid not in records:
                return self._send(404, {"error": "no such record"})
            return self._send(200, records[rid])
        q = parse_qs(urlparse(self.path).query)
        page, size = int(q.get("page", ["1"])[0]), min(int(q.get("page_size", ["20"])[0]), 50)
        ids = sorted(records, key=int)
        chunk = ids[(page - 1) * size: page * size]
        next_page = page + 1 if page * size < len(ids) else None
        return self._send(200, {"data": [records[i] for i in chunk], "page": page, "next_page": next_page})

    def _planned_failure(self, path):
        todo = Handler.planned.get(path)
        return todo.pop(0) if todo else None

    def do_PATCH(self):
        if not self._auth():
            return self._send(401, {"error": "missing or invalid token"})
        kind, rid = self._route()
        if kind is None or rid is None:
            return self._send(404, {"error": "not found"})
        path = f"{kind}/{rid}"
        body = self._read_json()
        key = self.headers.get("Idempotency-Key")
        with _lock:
            if key and key in Handler.idempotency:
                return self._send(200, {**Handler.idempotency[key], "replayed": True})
            failure = self._planned_failure(path)
            if failure == "503":
                return self._send(503, {"error": "temporarily unavailable, try again"})
            if failure == "429":
                return self._send(429, {"error": "rate limit exceeded"}, {"Retry-After": "1"})
            records = _load(kind)
            if rid not in records and kind == "leads":
                return self._send(404, {"error": "no such record"})
            action = "updated" if rid in records else "created"
            if action == "created":
                records[rid] = {"customer_id": rid}
            records[rid].update(body)
            _save(kind, records)
            response = {"record": path, "action": action, "fields": sorted(body), "replayed": False}
            if key:
                Handler.idempotency[key] = response
        if failure == "slow":
            time.sleep(SLOW_SECONDS)
        return self._send(201 if action == "created" else 200, response)

    def do_PUT(self):
        if not self._auth():
            return self._send(401, {"error": "missing or invalid token"})
        kind, rid = self._route()
        if kind is None or rid is None:
            return self._send(404, {"error": "not found"})
        body = self._read_json()
        with _lock:
            records = _load(kind)
            if rid not in records:
                return self._send(404, {"error": "no such record"})
            id_field = "lead_id" if kind == "leads" else "customer_id"
            records[rid] = {id_field: rid, **body}          # PUT: the record becomes exactly what was sent
            _save(kind, records)
        return self._send(200, {"record": f"{kind}/{rid}", "action": "replaced"})

    def do_POST(self):
        if not self._auth():
            return self._send(401, {"error": "missing or invalid token"})
        path = urlparse(self.path).path
        if path == "/api/webhooks":
            body = self._read_json()
            Handler.webhooks.append(body)
            return self._send(201, {"registered": body})
        if path == "/api/leads":
            body = self._read_json()
            with _lock:
                records = _load("leads")
                lead_id = str(Handler.next_lead_id)
                Handler.next_lead_id += 1
                record = {"lead_id": lead_id, **body}
                records[lead_id] = record
                _save("leads", records)
            if body.get("deal_value", 0) >= 200000:
                _fire("lead.created_high_value", {"lead": record})
            return self._send(201, record)
        return self._send(404, {"error": "not found"})


def sign(raw_body, secret=WEBHOOK_SECRET):
    """HMAC-SHA256 of the raw body, as hex: what the X-Signature header carries."""
    return hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()


def _fire(event, data):
    """Call every URL registered for this event. (Called inside the request, to keep the sandbox simple;
    a real provider queues the event and sends it separately.)"""
    for hook in Handler.webhooks:
        if hook.get("event") != event:
            continue
        payload = {"event_id": f"evt_{Handler.next_event}", "event": event, **data}
        Handler.next_event += 1
        raw = json.dumps(payload).encode()
        try:
            requests.post(hook["url"], data=raw, timeout=2,
                          headers={"Content-Type": "application/json", "X-Signature": sign(raw)})
        except requests.RequestException:
            pass


def simulate_failure(path, kind):
    """Test scaffolding: make the next write to `path` (e.g. "leads/4") fail once with `kind`."""
    Handler.planned.setdefault(path, []).append(kind)


def seed_crm():
    """Fill the sandbox CRM from riverstone_source: every lead, and an account for every customer except
    the newest one (customer 24 signed up in December and has no CRM account yet)."""
    conn = psycopg2.connect(SRC)
    with conn, conn.cursor() as cur:
        cur.execute("SELECT lead_id, company_name, email, source, owner_id FROM leads ORDER BY lead_id")
        leads = {str(r[0]): {"lead_id": str(r[0]), "company_name": r[1], "email": r[2], "source": r[3],
                             "owner_id": r[4]} for r in cur.fetchall()}
        cur.execute("SELECT customer_id, customer_name, city FROM customers WHERE customer_id <> 24 "
                    "ORDER BY customer_id")
        accounts = {str(r[0]): {"customer_id": str(r[0]), "name": r[1], "city": r[2]} for r in cur.fetchall()}
    conn.close()
    _save("leads", leads)
    _save("accounts", accounts)
    Handler.planned = {}
    Handler.idempotency = {}
    return len(leads), len(accounts)


def start_server(port=8051):
    Handler.planned = {}; Handler.idempotency = {}; Handler.webhooks = []
    Handler.next_lead_id = 9001; Handler.next_event = 1
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


if __name__ == "__main__":
    seed_crm()
    s = start_server()
    print("Sandbox CRM on http://127.0.0.1:8051  (Ctrl+C to stop)")
    threading.Event().wait()
