import requests
import os, sys, time

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def username_lookup(username):
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Twitter/X": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Telegram": f"https://t.me/{username}",
        "Pinterest": f"https://pinterest.com/{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}",
        "YouTube": f"https://youtube.com/@{username}",
        "HackerNews": f"https://news.ycombinator.com/user?id={username}",
    }
    print(f"\n{ACC}{BOLD}[*] Searching for: {username}{RESET}\n")
    found = []
    for platform, url in platforms.items():
        try:
            r = requests.get(url, timeout=5, allow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                print(f"  {GREEN}[+] FOUND{RESET} {platform}: {url}")
                found.append(url)
            else:
                print(f"  {GRAY}[-] Not found{RESET} {platform}")
        except:
            print(f"  {YELLOW}[!] Timeout{RESET} {platform}")
    print(f"\n{ACC}[*] Found on {len(found)} platforms.{RESET}")

def email_breach_check(email):
    print(f"\n{ACC}[*] Checking breach status for: {email}{RESET}")
    try:
        r = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers={"User-Agent": "AYO-OSINT", "hibp-api-key": "free"},
            timeout=8
        )
        if r.status_code == 200:
            print(f"  {RED}[!] BREACHED! Found in data breaches.{RESET}")
            print(f"  {GRAY}Tip: Check haveibeenpwned.com for full details.{RESET}")
        elif r.status_code == 404:
            print(f"  {GREEN}[+] Good news — not found in known breaches.{RESET}")
        else:
            print(f"  {YELLOW}[!] API requires key. Visit haveibeenpwned.com manually.{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

def run_osint():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  OSINT MODULE{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Username Lookup
  {ACC}[2]{RESET} Email Breach Check
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}""")
        choice = input(f"  {ACC}[osint]>{RESET} ").strip().lower()
        if choice == "1":
            u = input(f"  {GRAY}Enter username: {RESET}").strip()
            if u: username_lookup(u)
        elif choice == "2":
            e = input(f"  {GRAY}Enter email: {RESET}").strip()
            if e: email_breach_check(e)
        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
