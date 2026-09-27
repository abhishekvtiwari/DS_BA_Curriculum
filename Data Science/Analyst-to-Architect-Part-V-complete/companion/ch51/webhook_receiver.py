"""Chapter 51 companion: a tiny inbox that stands in for a Slack/Teams incoming webhook.
Real alerting tools (Slack, Teams, PagerDuty) all accept a POST of JSON to a URL; this is that,
kept local so the chapter's timing (arrives within a minute) can be shown and checked precisely.
Riverstone Supplies is fictional; every name and number is invented."""
import json, os, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

INBOX = "webhook_inbox"

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        os.makedirs(INBOX, exist_ok=True)
        fname = os.path.join(INBOX, f"{time.time():.6f}.json")
        json.dump({"received_at": time.time(), "body": body}, open(fname, "w"))
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.end_headers(); self.wfile.write(b'{"ok": true}')

def start_server(port=8052):
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server

def read_inbox():
    if not os.path.isdir(INBOX):
        return []
    items = []
    for f in sorted(os.listdir(INBOX)):
        items.append(json.load(open(os.path.join(INBOX, f))))
    return items

if __name__ == "__main__":
    s = start_server(); print("Webhook inbox on http://127.0.0.1:8052  (Ctrl+C to stop)")
    threading.Event().wait()
