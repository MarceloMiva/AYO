import requests
import os

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

DEFAULT_DIRS = [
    "admin","login","dashboard","panel","wp-admin","phpmyadmin",
    "api","v1","v2","backup","backups","db","database","config",
    "uploads","files","images","static","assets","js","css",
    "includes","src","app","lib","vendor","node_modules",
    "robots.txt","sitemap.xml",".env","config.php","config.yml",
    "readme.md","README.md","LICENSE","index.php","index.html",
    "shell","webshell","cmd","console","terminal","manager",
    "user","users","account","accounts","register","signup",
    "forgot","reset","password","auth","oauth","token",
    "test","testing","dev","development","staging","old","bak"
]

def dir_bruteforce(url, wordlist=None, extensions=None):
    if not url.startswith("http"):
        url = "http://" + url
    url = url.rstrip("/")
    words = wordlist if wordlist else DEFAULT_DIRS
    exts = extensions if extensions else ["", ".php", ".html", ".txt"]
    found = []
    total = len(words) * len(exts)

    print(f"\n  {ACC}[*] Target: {url}{RESET}")
    print(f"  {ACC}[*] Testing {total} paths...{RESET}\n")

    headers = {"User-Agent": "Mozilla/5.0 (AYO Scanner)"}
    count = 0

    for word in words:
        for ext in exts:
            path = f"{url}/{word}{ext}"
            try:
                r = requests.get(path, headers=headers, timeout=4,
                                 allow_redirects=False)
                count += 1
                if r.status_code in [200, 201, 301, 302, 403]:
                    color = GREEN if r.status_code == 200 else YELLOW
                    print(f"  {color}[{r.status_code}]{RESET} {path}")
                    found.append((r.status_code, path))
                if count % 20 == 0:
                    print(f"  {GRAY}[...] {count}/{total} tested{RESET}", end="\r")
            except requests.exceptions.ConnectionError:
                print(f"  {RED}[!] Cannot connect to {url}{RESET}")
                return
            except:
                pass

    print(f"\n  {ACC}[*] Found {len(found)} interesting paths.{RESET}")
    if found:
        save = input(f"  {GRAY}Save results? (y/n): {RESET}").strip().lower()
        if save == 'y':
            domain = url.replace("http://","").replace("https://","").replace("/","_")
            out = f"{domain}_dirs.txt"
            with open(out, 'w') as f:
                for code, path in found:
                    f.write(f"[{code}] {path}\n")
            print(f"  {GREEN}[+] Saved to {out}{RESET}")

def run_dir_bruteforce():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  DIR BRUTEFORCER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Scan with built-in wordlist
  {ACC}[2]{RESET} Scan with custom wordlist
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}""")
        choice = input(f"  {ACC}[dirbust]>{RESET} ").strip().lower()

        if choice == "1":
            url = input(f"  {GRAY}Enter URL (e.g. http://target.com): {RESET}").strip()
            if url: dir_bruteforce(url)

        elif choice == "2":
            url = input(f"  {GRAY}Enter URL: {RESET}").strip()
            path = input(f"  {GRAY}Wordlist path: {RESET}").strip()
            if url and os.path.exists(path):
                with open(path, 'r', errors='ignore') as f:
                    words = [l.strip() for l in f if l.strip()]
                dir_bruteforce(url, words)
            elif not os.path.exists(path):
                print(f"  {RED}[!] Wordlist not found.{RESET}")

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
