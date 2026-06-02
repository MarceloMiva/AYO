import requests
import ssl, socket, os, re
from urllib.parse import urlparse
from datetime import datetime

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

CRITICAL_HEADERS = {
    "X-Frame-Options": "Prevents clickjacking",
    "X-Content-Type-Options": "Prevents MIME sniffing",
    "Strict-Transport-Security": "Enforces HTTPS",
    "Content-Security-Policy": "Prevents XSS/injection",
    "X-XSS-Protection": "Legacy XSS protection",
}

VULNERABLE_VERSIONS = {
    "Apache": ["2.0", "2.2.0-2.2.15"],
    "nginx": ["1.0.0-1.11.0"],
    "IIS": ["5.0", "6.0"],
}

def check_ssl(url):
    try:
        hostname = urlparse(url).hostname
        port = urlparse(url).port or 443
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                expires = cert.get('notAfter', 'Unknown')
                print(f"\n  {GREEN}[+] SSL Certificate Info:{RESET}")
                print(f"      Subject: {cert.get('subject', 'N/A')}")
                print(f"      Expires: {expires}")
    except Exception as e:
        print(f"  {RED}[!] SSL Check Error: {e}{RESET}")

def check_headers(url):
    try:
        r = requests.get(url, timeout=6, allow_redirects=True)
        print(f"\n  {GREEN}[+] Security Headers Check:{RESET}\n")
        missing = []
        for header, desc in CRITICAL_HEADERS.items():
            if header in r.headers:
                print(f"  {GREEN}✓{RESET} {header}: {r.headers[header][:60]}")
            else:
                print(f"  {RED}✗{RESET} {header} — {GRAY}{desc}{RESET}")
                missing.append(header)
        if missing:
            print(f"\n  {YELLOW}[!] Missing {len(missing)} critical headers{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Headers Check Error: {e}{RESET}")

def fingerprint_server(url):
    try:
        r = requests.get(url, timeout=6)
        server = r.headers.get('Server', 'Unknown')
        powered_by = r.headers.get('X-Powered-By', 'Unknown')
        
        print(f"\n  {YELLOW}[*] Server Fingerprint:{RESET}")
        print(f"      Server: {server}")
        print(f"      Powered-By: {powered_by}")
        
        # Check for known vulnerabilities
        for product, versions in VULNERABLE_VERSIONS.items():
            if product.lower() in server.lower():
                for version in versions:
                    if version in server:
                        print(f"      {RED}[!] VULNERABLE VERSION DETECTED: {version}{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Fingerprint Error: {e}{RESET}")

def check_common_vulns(url):
    print(f"\n  {YELLOW}[*] Checking common vulnerabilities...{RESET}\n")
    vulns_found = []
    
    dangerous_paths = [
        "/admin", "/administrator", "/wp-admin",
        "/.git", "/.env", "/config.php", "/web.config",
        "/backup", "/sql", "/database.sql",
    ]
    
    for path in dangerous_paths:
        try:
            test_url = url.rstrip('/') + path
            r = requests.get(test_url, timeout=4, allow_redirects=False)
            if r.status_code in [200, 301, 302, 401, 403]:
                color = RED if r.status_code == 200 else YELLOW
                print(f"  {color}[{r.status_code}]{RESET} {path}")
                vulns_found.append((path, r.status_code))
        except:
            pass
    
    if not vulns_found:
        print(f"  {GREEN}[+] No obvious paths found{RESET}")
    else:
        print(f"\n  {RED}[!] Found {len(vulns_found)} potentially exposed paths{RESET}")

def scan_website(url):
    if not url.startswith("http"):
        url = "http://" + url
    
    print(f"\n  {ACC}[*] Web Vulnerability Scan: {url}{RESET}\n")
    
    # SSL Check
    if url.startswith("https"):
        check_ssl(url)
    
    # Headers Check
    check_headers(url)
    
    # Server Fingerprint
    fingerprint_server(url)
    
    # Common Vulnerabilities
    check_common_vulns(url)
    
    print(f"\n  {ACC}[*] Scan complete.{RESET}")
    save = input(f"  {GRAY}Save report? (y/n): {RESET}").strip().lower()
    if save == 'y':
        domain = urlparse(url).netloc.replace('.', '_')
        report = f"{domain}_vuln_report.txt"
        with open(report, 'w') as f:
            f.write(f"Web Vulnerability Scan Report\n")
            f.write(f"Target: {url}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"\nFor full results, refer to terminal output.\n")
        print(f"  {GREEN}[+] Report saved: {report}{RESET}")

def run_web_vuln_scanner():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  WEB VULNERABILITY SCANNER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Quick scan
  {ACC}[2]{RESET} Full detailed scan
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}Authorized testing only{RESET}""")
        choice = input(f"  {ACC}[webvuln]>{RESET} ").strip().lower()

        if choice == "1":
            url = input(f"  {GRAY}Enter URL (http://target.com): {RESET}").strip()
            if url:
                scan_website(url)

        elif choice == "2":
            url = input(f"  {GRAY}Enter URL: {RESET}").strip()
            if url:
                print(f"  {GRAY}(Full scan includes SSL, headers, fingerprinting, path discovery){RESET}")
                scan_website(url)

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
