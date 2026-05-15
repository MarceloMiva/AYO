# ═══════════════════════════════════════════
#  AYO — Module [4]: Password Tools
# ═══════════════════════════════════════════

import hashlib
import itertools
import string
import random
import re

RED   = "\033[91m"
DRED  = "\033[31m"
WHITE = "\033[97m"
GRAY  = "\033[90m"
YELLOW= "\033[93m"
GREEN = "\033[92m"
DIM   = "\033[2m"
BOLD  = "\033[1m"
RESET = "\033[0m"

def pw_banner():
    print(f"""
{DRED}╔══════════════════════════════════════════════╗
║         PASSWORD TOOLS — MODULE [4]          ║
╚══════════════════════════════════════════════╝{RESET}
{DIM}Generate, analyze, identify, and crack password hashes.{RESET}
""")

# ── Hash identifier ──────────────────────────
def identify_hash(h):
    h = h.strip()
    length = len(h)
    patterns = {
        32:  "MD5",
        40:  "SHA-1",
        56:  "SHA-224",
        64:  "SHA-256",
        96:  "SHA-384",
        128: "SHA-512",
    }
    if length in patterns:
        return patterns[length]
    if h.startswith("$2b$") or h.startswith("$2a$"):
        return "bcrypt"
    if h.startswith("$6$"):
        return "SHA-512 crypt (Linux shadow)"
    if h.startswith("$1$"):
        return "MD5 crypt"
    return "Unknown"

# ── Hash generator ───────────────────────────
def generate_hash(text):
    results = {}
    for algo in ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]:
        h = hashlib.new(algo)
        h.update(text.encode())
        results[algo.upper()] = h.hexdigest()
    return results

# ── Password strength analyzer ───────────────
def analyze_strength(pw):
    score = 0
    feedback = []

    if len(pw) >= 8:  score += 1
    else: feedback.append("Too short (min 8 chars)")

    if len(pw) >= 12: score += 1
    if len(pw) >= 16: score += 1

    if re.search(r'[A-Z]', pw): score += 1
    else: feedback.append("Add uppercase letters")

    if re.search(r'[a-z]', pw): score += 1
    else: feedback.append("Add lowercase letters")

    if re.search(r'\d', pw): score += 1
    else: feedback.append("Add numbers")

    if re.search(r'[^A-Za-z0-9]', pw): score += 1
    else: feedback.append("Add special characters (!@#$...)")

    common = ["password", "123456", "qwerty", "admin", "letmein", "welcome", "monkey"]
    if pw.lower() in common:
        score = 0
        feedback = ["This is a commonly used password — change it immediately"]

    if score <= 2:   rating = f"{RED}WEAK{RESET}"
    elif score <= 4: rating = f"{YELLOW}FAIR{RESET}"
    elif score <= 6: rating = f"{YELLOW}GOOD{RESET}"
    else:            rating = f"{GREEN}STRONG{RESET}"

    return score, rating, feedback

# ── Password generator ───────────────────────
def generate_password(length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    chars = ""
    if use_upper:   chars += string.ascii_uppercase
    if use_lower:   chars += string.ascii_lowercase
    if use_digits:  chars += string.digits
    if use_special: chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    if not chars:
        return None
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

# ── Wordlist generator ───────────────────────
def generate_wordlist(base_words, output_file):
    count = 0
    with open(output_file, 'w') as f:
        for word in base_words:
            variants = set()
            variants.add(word)
            variants.add(word.lower())
            variants.add(word.upper())
            variants.add(word.capitalize())
            variants.add(word + "123")
            variants.add(word + "!")
            variants.add(word + "2024")
            variants.add(word + "2025")
            variants.add(word + "1")
            variants.add(word + "01")
            variants.add("@" + word)
            variants.add(word.replace("a", "@").replace("e", "3").replace("o", "0").replace("i", "1"))
            for v in variants:
                f.write(v + "\n")
                count += 1
    return count

# ── Hash cracker ─────────────────────────────
def crack_hash(target_hash, wordlist_file, algo="md5"):
    target_hash = target_hash.strip().lower()
    try:
        with open(wordlist_file, 'r', errors='ignore') as f:
            words = f.read().splitlines()
    except FileNotFoundError:
        print(f"  {YELLOW}[!] Wordlist file not found.{RESET}")
        return None

    print(f"  {DIM}[*] Trying {len(words)} words with {algo.upper()}...{RESET}")

    for i, word in enumerate(words):
        h = hashlib.new(algo)
        h.update(word.encode())
        if h.hexdigest() == target_hash:
            return word
        if i % 1000 == 0 and i > 0:
            print(f"  {GRAY}[*] Tried {i}/{len(words)}...{RESET}", end='\r')

    return None

def run_password_tools():
    pw_banner()

    while True:
        print(f"  {RED}[1]{RESET} Identify hash type")
        print(f"  {RED}[2]{RESET} Generate hashes from text")
        print(f"  {RED}[3]{RESET} Analyze password strength")
        print(f"  {RED}[4]{RESET} Generate strong password")
        print(f"  {RED}[5]{RESET} Build custom wordlist")
        print(f"  {RED}[6]{RESET} Crack hash with wordlist")
        print(f"  {RED}[b]{RESET} Back\n")

        choice = input(f"  {RED}[pw]>{RESET} ").strip().lower()

        if choice == "1":
            h = input(f"\n  {WHITE}Enter hash:{RESET} ").strip()
            result = identify_hash(h)
            print(f"  {RED}[+] Detected:{RESET} {WHITE}{result}{RESET}\n")

        elif choice == "2":
            text = input(f"\n  {WHITE}Enter text to hash:{RESET} ").strip()
            hashes = generate_hash(text)
            print()
            for algo, val in hashes.items():
                print(f"  {RED}{algo:<10}{RESET} {GRAY}{val}{RESET}")
            print()

        elif choice == "3":
            pw = input(f"\n  {WHITE}Enter password to analyze:{RESET} ").strip()
            score, rating, feedback = analyze_strength(pw)
            print(f"\n  {RED}[+] Strength:{RESET} {rating}  {DIM}(score: {score}/7){RESET}")
            if feedback:
                print(f"  {WHITE}Suggestions:{RESET}")
                for tip in feedback:
                    print(f"  {GRAY}  • {tip}{RESET}")
            print()

        elif choice == "4":
            try:
                length = int(input(f"\n  {WHITE}Length (default 16):{RESET} ").strip() or "16")
            except ValueError:
                length = 16
            pw = generate_password(length)
            print(f"\n  {RED}[+] Generated:{RESET} {WHITE}{BOLD}{pw}{RESET}\n")
            score, rating, _ = analyze_strength(pw)
            print(f"  {RED}[+] Strength:{RESET} {rating}\n")

        elif choice == "5":
            raw = input(f"\n  {WHITE}Enter base words (comma separated):{RESET} ").strip()
            words = [w.strip() for w in raw.split(",") if w.strip()]
            out = input(f"  {WHITE}Output filename (default: wordlist.txt):{RESET} ").strip() or "wordlist.txt"
            count = generate_wordlist(words, out)
            print(f"  {RED}[+] Wordlist generated:{RESET} {count} entries → {out}\n")

        elif choice == "6":
            h = input(f"\n  {WHITE}Enter hash to crack:{RESET} ").strip()
            algo_detected = identify_hash(h)
            print(f"  {DIM}[*] Detected: {algo_detected}{RESET}")

            algo_map = {"MD5": "md5", "SHA-1": "sha1", "SHA-256": "sha256", "SHA-512": "sha512"}
            algo = algo_map.get(algo_detected, "md5")

            wordlist = input(f"  {WHITE}Wordlist path:{RESET} ").strip()
            result = crack_hash(h, wordlist, algo)

            if result:
                print(f"\n  {RED}[+] CRACKED:{RESET} {WHITE}{BOLD}{result}{RESET}\n")
            else:
                print(f"\n  {YELLOW}[-] Not found in wordlist.{RESET}\n")

        elif choice in ["b", "back"]:
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}\n")
