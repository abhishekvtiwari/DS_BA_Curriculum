# A tiny demonstration API for Chapter 2. Run: python3 api_demo.py   (listens on http://localhost:8000)
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
ORDERS = {
    5008: {"order_id": 5008, "customer_name": "Sunrise Caterers", "order_date": "2026-02-19",
           "status": "Delivered", "net_revenue": 23325.00},
    5009: {"order_id": 5009, "customer_name": "Northgate Distributors", "order_date": "2026-02-25",
           "status": "Shipped", "net_revenue": 76560.00},
}
API_KEY = "demo-key-123"
class Handler(BaseHTTPRequestHandler):
    server_version = "RiverstoneAPI/1.0"
    sys_version = ""
    # The Date header is fixed so that your output matches the book exactly.
    def date_time_string(self, timestamp=None):
        return "Wed, 16 Sep 2026 10:30:00 GMT"
    def reply(self, code, body):
        data = (json.dumps(body, indent=2) + "\n").encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.headers.get("X-API-Key") != API_KEY:
            return self.reply(401, {"error": "missing or invalid API key"})
        parts = self.path.strip("/").split("/")
        if len(parts) == 3 and parts[:2] == ["api", "orders"] and parts[2].isdigit():
            order = ORDERS.get(int(parts[2]))
            if order:
                return self.reply(200, order)
            return self.reply(404, {"error": f"order {parts[2]} not found"})
        return self.reply(404, {"error": "unknown address"})
    def log_message(self, *args):
        pass
if __name__ == "__main__":
    HTTPServer(("localhost", 8000), Handler).serve_forever()
