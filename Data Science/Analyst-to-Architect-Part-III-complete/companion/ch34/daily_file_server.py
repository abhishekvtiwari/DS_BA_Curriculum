#!/usr/bin/env python3
"""
Analyst to Architect · Chapter 34 · The Command Line, Linux & Networking Basics
File: daily_file_server.py - a local stand-in for the partner's file server used in the chapter's project.
What: serves the files in practice/exports/ at http://127.0.0.1:8034/exports/<name>, plus a matching
      <name>.sha256 checksum file for each, and returns 404 for a day that hasn't been published.
      GET /health returns "ok". Nothing leaves your machine.
How:  python3 daily_file_server.py       (Ctrl+C to stop; add --port to change the port)
Tested on: Python 3.12.3 (standard library only).
Riverstone Supplies is fictional; every name and number is invented.
"""
from __future__ import annotations

import argparse, hashlib, pathlib, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

EXPORTS = pathlib.Path(__file__).parent / 'practice' / 'exports'


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass

    def reply(self, status: int, body: bytes, content_type: str = 'text/plain') -> None:
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if not getattr(self, 'head_only', False):
            self.wfile.write(body)

    def do_HEAD(self) -> None:
        self.head_only = True
        self.do_GET()

    def do_GET(self) -> None:
        if self.path == '/health':
            return self.reply(200, b'ok\n')
        if not self.path.startswith('/exports/'):
            return self.reply(404, b'not found\n')
        name = self.path.removeprefix('/exports/')
        wants_checksum = name.endswith('.sha256')
        source = EXPORTS / (name.removesuffix('.sha256') if wants_checksum else name)
        if source.name != source.name.replace('..', '') or not source.is_file():
            return self.reply(404, b'not found\n')
        data = source.read_bytes()
        if wants_checksum:
            return self.reply(200, f'{hashlib.sha256(data).hexdigest()}  {source.name}\n'.encode())
        self.reply(200, data, 'text/csv')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--port', type=int, default=8034)
    port = ap.parse_args().port
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f'daily file server on http://127.0.0.1:{port}/exports/ (Ctrl+C to stop)')
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        server.shutdown()
