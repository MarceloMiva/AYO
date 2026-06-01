import requests
import os, socket

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

DEFAULT_WORDLIST = [
    "www","mail","ftp","admin","api","dev","staging","test","blog",
    "shop","store","portal","vpn","remote","secure","login","app",
    "mobile","static","cdn","media","img","images","video","docs",
    "support","help","status","monitor","dashboard","panel","cpanel",
    "webmail","smtp","pop","imap","ns1","ns2","mx","beta","alpha",
    "internal","intranet","git","gitlab","jenkins","ci","jira","wiki"
]

def subdomain_enum(domain, wordlist=None):
    words = wordlist if wordlist else DEFAULT_WORDLIST
    found = []
    print(f"\n  {ACC}[*] Enumerating subdomains for: {domain}{RESET}")
    print(f"  {GRAY}[*] Testing {len(words)} subdomains...{RESET}\n")

    for word in words:
        subdomain = f"{word}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            print(f"  {GREEN}[+] FOUND{RESET} {subdomain} → {ip}")
            found.append((subdomain, ip))
        except socket.gaierror:
            pass
        except Exception as e:
            pass

    print(f"\n  {ACC}[*] Found {len(found)} subdomains.{RESET}")
    if found:
        save = input(f"  {GRAY}Save results? (y/n): {RESET}").strip().lower()
        if save == 'y':
            out = f"{domain}_subdomains.txt"
            with open(out, 'w') as f:
                for s, ip in found:
                    f.write(f"{s} → {ip}\n")
            print(f"  {GREEN}[+] Saved to {out}{RESET}")

def run_subdomain_enum():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  SUBDOMAIN ENUMERATOR{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Enumerate with built-in wordlist
  {ACC}[2]{RESET} Enumerate with custom wordlist file
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}""")
        choice = input(f"  {ACC}[subdomain]>{RESET} ").strip().lower()

        if choice == "1":
            domain = input(f"  {GRAY}Enter domain (e.g. example.com): {RESET}").strip()
            if domain: subdomain_enum(domain)

        elif choice == "2":
            domain = input(f"  {GRAY}Enter domain: {RESET}").strip()
            path = input(f"  {GRAY}Wordlist path: {RESET}").strip()
            if domain and os.path.exists(path):
                with open(path, 'r', errors='ignore') as f:
                    words = [l.strip() for l in f if l.strip()]
                subdomain_enum(domain, words)
            elif not os.path.exists(path):
                print(f"  {RED}[!] Wordlist not found.{RESET}")

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
