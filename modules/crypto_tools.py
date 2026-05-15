# ═══════════════════════════════════════════
#  AYO — Module [6]: Crypto Tools
# ═══════════════════════════════════════════

import base64
import os
import collections

RED   = "\033[91m"
DRED  = "\033[31m"
WHITE = "\033[97m"
GRAY  = "\033[90m"
YELLOW= "\033[93m"
GREEN = "\033[92m"
DIM   = "\033[2m"
BOLD  = "\033[1m"
RESET = "\033[0m"

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    AES_AVAILABLE = True
except ImportError:
    AES_AVAILABLE = False

def crypto_banner():
    print(f"""
{DRED}╔══════════════════════════════════════════════╗
║           CRYPTO TOOLS — MODULE [6]          ║
╚══════════════════════════════════════════════╝{RESET}
{DIM}Encrypt, decrypt, encode, decode, and break classical ciphers.{RESET}
""")

# ── Caesar cipher ────────────────────────────
def caesar(text, shift, decrypt=False):
    if decrypt: shift = -shift
    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

def caesar_bruteforce(text):
    results = []
    for shift in range(1, 26):
        results.append((shift, caesar(text, shift, decrypt=True)))
    return results

# ── Vigenère cipher ──────────────────────────
def vigenere(text, key, decrypt=False):
    key = key.upper()
    result = []
    ki = 0
    for c in text:
        if c.isalpha():
            shift = ord(key[ki % len(key)]) - ord('A')
            if decrypt: shift = -shift
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
            ki += 1
        else:
            result.append(c)
    return ''.join(result)

# ── XOR cipher ───────────────────────────────
def xor_cipher(text, key):
    result = []
    for i, c in enumerate(text):
        result.append(chr(ord(c) ^ ord(key[i % len(key)])))
    return ''.join(result)

def xor_hex(text, key):
    result = bytearray()
    key_bytes = key.encode()
    for i, b in enumerate(text.encode()):
        result.append(b ^ key_bytes[i % len(key_bytes)])
    return result.hex()

# ── Base64 ───────────────────────────────────
def b64_encode(text):
    return base64.b64encode(text.encode()).decode()

def b64_decode(text):
    try:
        return base64.b64decode(text).decode()
    except:
        return None

# ── Hex encode/decode ────────────────────────
def hex_encode(text):
    return text.encode().hex()

def hex_decode(h):
    try:
        return bytes.fromhex(h).decode()
    except:
        return None

# ── ROT13 ────────────────────────────────────
def rot13(text):
    return caesar(text, 13)

# ── Frequency analysis ───────────────────────
def frequency_analysis(text):
    text_clean = ''.join(c.upper() for c in text if c.isalpha())
    freq = collections.Counter(text_clean)
    total = sum(freq.values())
    return [(char, count, round(count/total*100, 1)) for char, count in freq.most_common(10)]

# ── AES-256 ──────────────────────────────────
def aes_encrypt(plaintext, key):
    key_bytes = key.encode().ljust(32)[:32]
    iv = os.urandom(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(iv + ct).decode()

def aes_decrypt(ciphertext, key):
    try:
        key_bytes = key.encode().ljust(32)[:32]
        data = base64.b64decode(ciphertext)
        iv, ct = data[:16], data[16:]
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()
    except Exception as e:
        return f"Error: {e}"

def run_crypto_tools():
    crypto_banner()

    while True:
        print(f"  {WHITE}CLASSICAL CIPHERS{RESET}")
        print(f"  {RED}[1]{RESET} Caesar cipher (encrypt/decrypt/bruteforce)")
        print(f"  {RED}[2]{RESET} Vigenère cipher")
        print(f"  {RED}[3]{RESET} XOR cipher")
        print(f"  {RED}[4]{RESET} ROT13")
        print(f"\n  {WHITE}ENCODING{RESET}")
        print(f"  {RED}[5]{RESET} Base64 encode/decode")
        print(f"  {RED}[6]{RESET} Hex encode/decode")
        print(f"\n  {WHITE}ANALYSIS{RESET}")
        print(f"  {RED}[7]{RESET} Frequency analysis")
        print(f"\n  {WHITE}MODERN{RESET}")
        print(f"  {RED}[8]{RESET} AES-256 encrypt/decrypt {'(requires pycryptodome)' if not AES_AVAILABLE else ''}")
        print(f"\n  {RED}[b]{RESET} Back\n")

        choice = input(f"  {RED}[crypto]>{RESET} ").strip().lower()

        if choice == "1":
            text  = input(f"\n  {WHITE}Text:{RESET} ").strip()
            mode  = input(f"  {WHITE}Mode — [e]ncrypt / [d]ecrypt / [b]ruteforce:{RESET} ").strip().lower()
            if mode == "b":
                print(f"\n  {RED}[+] All Caesar shifts:{RESET}\n")
                for shift, result in caesar_bruteforce(text):
                    print(f"  {GRAY}Shift {shift:<3}{RESET} {result}")
                print()
            else:
                try:
                    shift = int(input(f"  {WHITE}Shift (1-25):{RESET} ").strip())
                    result = caesar(text, shift, decrypt=(mode == "d"))
                    print(f"\n  {RED}[+] Result:{RESET} {WHITE}{result}{RESET}\n")
                except ValueError:
                    print(f"  {YELLOW}[!] Invalid shift.{RESET}\n")

        elif choice == "2":
            text = input(f"\n  {WHITE}Text:{RESET} ").strip()
            key  = input(f"  {WHITE}Key (letters only):{RESET} ").strip()
            mode = input(f"  {WHITE}[e]ncrypt / [d]ecrypt:{RESET} ").strip().lower()
            result = vigenere(text, key, decrypt=(mode == "d"))
            print(f"\n  {RED}[+] Result:{RESET} {WHITE}{result}{RESET}\n")

        elif choice == "3":
            text = input(f"\n  {WHITE}Text:{RESET} ").strip()
            key  = input(f"  {WHITE}Key:{RESET} ").strip()
            result = xor_cipher(text, key)
            hex_result = xor_hex(text, key)
            print(f"\n  {RED}[+] XOR Result (text):{RESET} {WHITE}{result}{RESET}")
            print(f"  {RED}[+] XOR Result (hex) :{RESET} {GRAY}{hex_result}{RESET}\n")

        elif choice == "4":
            text = input(f"\n  {WHITE}Text:{RESET} ").strip()
            print(f"\n  {RED}[+] ROT13:{RESET} {WHITE}{rot13(text)}{RESET}\n")

        elif choice == "5":
            text = input(f"\n  {WHITE}Text:{RESET} ").strip()
            mode = input(f"  {WHITE}[e]ncode / [d]ecode:{RESET} ").strip().lower()
            if mode == "e":
                print(f"\n  {RED}[+] Base64:{RESET} {WHITE}{b64_encode(text)}{RESET}\n")
            else:
                result = b64_decode(text)
                if result:
                    print(f"\n  {RED}[+] Decoded:{RESET} {WHITE}{result}{RESET}\n")
                else:
                    print(f"  {YELLOW}[!] Invalid Base64.{RESET}\n")

        elif choice == "6":
            text = input(f"\n  {WHITE}Text:{RESET} ").strip()
            mode = input(f"  {WHITE}[e]ncode / [d]ecode:{RESET} ").strip().lower()
            if mode == "e":
                print(f"\n  {RED}[+] Hex:{RESET} {WHITE}{hex_encode(text)}{RESET}\n")
            else:
                result = hex_decode(text)
                if result:
                    print(f"\n  {RED}[+] Decoded:{RESET} {WHITE}{result}{RESET}\n")
                else:
                    print(f"  {YELLOW}[!] Invalid hex.{RESET}\n")

        elif choice == "7":
            text = input(f"\n  {WHITE}Ciphertext to analyze:{RESET} ").strip()
            freq = frequency_analysis(text)
            print(f"\n  {RED}[+] Top letter frequencies:{RESET}")
            print(f"  {GRAY}(English: E=12.7%, T=9.1%, A=8.2%, O=7.5%, I=7.0%){RESET}\n")
            for char, count, pct in freq:
                bar = "█" * int(pct / 2)
                print(f"  {WHITE}{char}{RESET}  {RED}{bar:<20}{RESET}  {pct}%  ({count})")
            print()

        elif choice == "8":
            if not AES_AVAILABLE:
                print(f"  {YELLOW}[!] pycryptodome not installed.{RESET}")
                print(f"  {DIM}Install: pip install pycryptodome{RESET}\n")
                continue
            mode = input(f"\n  {WHITE}[e]ncrypt / [d]ecrypt:{RESET} ").strip().lower()
            text = input(f"  {WHITE}Text:{RESET} ").strip()
            key  = input(f"  {WHITE}Key (any length, padded to 32 bytes):{RESET} ").strip()
            if mode == "e":
                result = aes_encrypt(text, key)
                print(f"\n  {RED}[+] AES-256 Encrypted:{RESET}\n  {WHITE}{result}{RESET}\n")
            else:
                result = aes_decrypt(text, key)
                print(f"\n  {RED}[+] Decrypted:{RESET} {WHITE}{result}{RESET}\n")

        elif choice in ["b", "back"]:
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}\n")
