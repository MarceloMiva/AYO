# AYO — Attack Your Offenders

> **⚠ For authorized penetration testing and CTF competitions ONLY.**

```
   ▄▄▄  ▄   ▄  ▄▄▄
  █   █  ▀▄▀  █   █
  █████   █   █   █
  █   █   █   █   █
  █   █   █    ▀▀▀
```

![Python](https://img.shields.io/badge/Python-3.x-red?style=flat-square&logo=python&logoColor=white)
![Modules](https://img.shields.io/badge/Modules-6-darkred?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)
![CTF](https://img.shields.io/badge/CTF-Ready-red?style=flat-square)

**Built by Fashipe Oluwadamilare Ayoola**  
CS/Cybersecurity · MIVA Open University

---

## About

AYO — **Attack Your Offenders** is a modular offensive security framework

## Modules
Offensive Modules (5 modules)
| # | Module | Description |
|---|--------|-------------|
| 1 | **Phishing Kit Generator** | HTML credential lure pages + Python capture server |
| 2 | **Steganography Suite** | LSB image encoding + zero-width character text steganography |
| 3 | **Social Engineering Toolkit** | Pretexting scripts, vishing guides, OSINT checklists |
| 4 | **Password Tools** | Hash ID, generator, strength analyzer, wordlist builder, cracker |
| 5 | **Network Tools** | Port scanner, DNS lookup, ping sweep, banner grabbing |
| 6 | **Crypto Tools** | Caesar, Vigenère, XOR, AES-256, Base64, Hex, ROT13, frequency analysis |
### Recon & OSINT (5 modules)
| # | Module | Description |
|---|--------|-------------|
| 7 | **OSINT Lookup** | Username enumeration across 10 platforms + email breach checking (HaveIBeenPwned API) |
| 8 | **Hash Cracker** | MD5/SHA1/SHA256/SHA512 identification + wordlist-based cracking |
| 9 | **Wordlist Generator** | Keyword-based wordlist with leet speak, years (1990-2025), special chars, permutations |
| 10 | **Subdomain Enumerator** | Built-in + custom wordlist subdomain discovery via DNS |
| 11 | **Dir Bruteforcer** | Directory/file enumeration with status code filtering (200/301/302/403) |

### Web Attacks (3 modules)
| # | Module | Description |
|---|--------|-------------|
| 12 | **SQLi Tester** | 25 SQL injection payloads + error signature detection |
| 13 | **XSS Tester** | 20 XSS payloads (script tags, onerror, javascript: URIs, encoded variants) |
| 22 | **Web Vuln Scanner** | SSL/TLS certs, security headers audit, server fingerprinting, path discovery |

### Network Attacks (5 modules)
| # | Module | Description |
|---|--------|-------------|
| 14 | **SSH Bruteforcer** | Paramiko-based SSH credential testing (authorized only) |
| 15 | **WiFi Scanner** | Termux API-powered SSID/BSSID/signal/security enumeration |
| 16 | **ARP Spoof/MITM** | ARP poisoning via dsniff + IP forwarding, nmap ARP scan |
| 17 | **Packet Sniffer** | Raw socket packet capture + Ethernet/IP/TCP/UDP header parsing |
| 18 | **Port Knocker** | TCP/UDP port knocking with preset sequences + verification |

### Evasion & Post-Exploitation (4 modules)
| # | Module | Description |
|---|--------|-------------|
| 19 | **File Encryptor** | AES-256-CBC encryption with PBKDF2 key derivation (100k iterations) |
| 20 | **Metadata Cleaner** | EXIF removal (JPEG via PIL) + PDF metadata regex cleaning |
| 21 | **Payload Encoder** | Base64, Hex, URL, Binary, Octal, Unicode, ROT13, XOR, Base32, HTML entities |



---

## Quick Start

```bash
git clone https://github.com/MarceloMiva/AYO.git
cd AYO
pip install -r requirements.txt
python ayo.py
```

## Optional Dependencies

| Package | Module |
|---------|--------|
| `Pillow` | Steganography (image LSB) |
| `pycryptodome` | Crypto Tools (AES-256) |

Core modules work without these. Install only what you need.

---

## Legal Disclaimer

AYO is intended **strictly** for:
- Authorized penetration testing
- CTF competitions
- Personal lab environments

The author takes no responsibility for misuse.

---

**Fashipe Oluwadamilare Ayoola** · MIVA Open University · Lagos, Nigeria
