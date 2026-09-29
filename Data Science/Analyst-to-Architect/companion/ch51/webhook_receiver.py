"""Chapter 51 companion: a small, safe webhook receiver, standing in for your own receiving endpoint
(or a Slack/Teams incoming webhook, Chapter 20).

It does the four things section 51.6 asks of a receiver:
  1. verify the sender: the X-Signature header must be the HMAC-SHA256 of the raw body with WEBHOOK_SECRET,
     compared with hmac.compare_digest; otherwise it answers 401 and keeps nothing;
  2. de-duplicate by the event's own id: an event_id it has already seen is acknowledged and skipped;
  3. record the event in the inbox folder (one JSON file per event, with the time it arrived);
  4. answer 200 at once; any real work happens later, from the inbox.
Riverstone Supplies is fictional; every name and number is invented."""
import hashlib, hmac, json, os, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

INBOX = "webhook_inbox"
SECRET = os.environ.get("WEBHOOK_SECRET", "practice-secret-51").encode()


class Handler(BaseHTTPRequestHandler):
    seen = set()                      # event ids already received

    def log_message(self, *a):
        pass

    def reply(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    # --- the handler shown in section 51.6 ---
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        expected = hmac.new(SECRET, body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, self.headers.get("X-Signature", "")):
            return self.reply(401, {"ok": False, "error": "bad signature"})
        event = json.loads(body)
        if event["event_id"] in Handler.seen:
            return self.reply(200, {"ok": True, "duplicate": True})
        Handler.seen.add(event["event_id"])
        save_to_inbox(event)
        return self.reply(200, {"ok": True})
    # --- end of the handler ---


def save_to_inbox(event):
    os.makedirs(INBOX, exist_ok=True)
    name = os.path.join(INBOX, f"{time.time():.6f}.json")
    with open(name, "w") as f:
        json.dump({"received_at": time.time(), "body": event}, f)


def start_server(port=8052):
    Handler.seen = set()
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def read_inbox():
    if not os.path.isdir(INBOX):
        return []
    items = []
    for name in sorted(os.listdir(INBOX)):
        with open(os.path.join(INBOX, name)) as f:
            items.append(json.load(f))
    return items


if __name__ == "__main__":
    s = start_server()
    print("Webhook receiver on http://127.0.0.1:8052  (Ctrl+C to stop)")
    threading.Event().wait()
