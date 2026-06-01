import hashlib
import os, sys

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def identify_hash(h):
    l = len(h)
    if l == 32: return "MD5"
    elif l == 40: return "SHA1"
    elif l == 64: return "SHA256"
    elif l == 128: return "SHA512"
    else: return "Unknown"

def crack_hash(target_hash, wordlist_path):
    target_hash = target_hash.strip().lower()
    hash_type = identify_hash(target_hash)
    print(f"\n  {ACC}[*] Hash type: {hash_type}{RESET}")
    print(f"  {ACC}[*] Starting crack...{RESET}\n")

    if not os.path.exists(wordlist_path):
        print(f"  {RED}[!] Wordlist not found: {wordlist_path}{RESET}")
        return

    algos = {
        "MD5": hashlib.md5,
        "SHA1": hashlib.sha1,
        "SHA256": hashlib.sha256,
        "SHA512": hashlib.sha512,
    }

    algo = algos.get(hash_type)
    if not algo:
        print(f"  {RED}[!] Unsupported hash type.{RESET}")
        return

    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            count = 0
            for line in f:
                word = line.strip()
                hashed = algo(word.encode()).hexdigest()
                count += 1
                if count % 1000 == 0:
                    print(f"  {GRAY}[...] Tried {count} words{RESET}", end="\r")
                if hashed == target_hash:
                    print(f"\n  {GREEN}[+] CRACKED! Password: {BOLD}{word}{RESET}")
                    return
            print(f"\n  {RED}[-] Not found after {count} attempts.{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

def generate_hash(text):
    print(f"\n  {ACC}[*] Hashes for: {text}{RESET}")
    print(f"  {GRAY}MD5    :{RESET} {hashlib.md5(text.encode()).hexdigest()}")
    print(f"  {GRAY}SHA1   :{RESET} {hashlib.sha1(text.encode()).hexdigest()}")
    print(f"  {GRAY}SHA256 :{RESET} {hashlib.sha256(text.encode()).hexdigest()}")
    print(f"  {GRAY}SHA512 :{RESET} {hashlib.sha512(text.encode()).hexdigest()}")

def run_hash_cracker():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  HASH CRACKER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Crack a hash with wordlist
  {ACC}[2]{RESET} Generate hash from text
  {ACC}[3]{RESET} Identify hash type
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}""")
        choice = input(f"  {ACC}[hash]>{RESET} ").strip().lower()
        if choice == "1":
            h = input(f"  {GRAY}Enter hash: {RESET}").strip()
            w = input(f"  {GRAY}Wordlist path (e.g. /sdcard/rockyou.txt): {RESET}").strip()
            if h and w: crack_hash(h, w)
        elif choice == "2":
            t = input(f"  {GRAY}Enter text: {RESET}").strip()
            if t: generate_hash(t)
        elif choice == "3":
            h = input(f"  {GRAY}Enter hash: {RESET}").strip()
            if h: print(f"\n  {ACC}[*] Type: {identify_hash(h)}{RESET}")
        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
