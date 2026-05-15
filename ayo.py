# ═══════════════════════════════════════════════════
#  AYO — Attack Your Offenders
#  By Fashipe Oluwadamilare Ayoola
#  For authorized testing & CTFs ONLY
# ═══════════════════════════════════════════════════

import os
import sys
import time

# ── Color Palette (DARE-style) ───────────────────────
GREEN       = "\033[92m"
GREEN_DIM   = "\033[32m"
CYAN        = "\033[96m"
WHITE       = "\033[97m"
YELLOW      = "\033[93m"
RED         = "\033[91m"
GRAY        = "\033[90m"
BOLD        = "\033[1m"
DIM         = "\033[2m"
RESET       = "\033[0m"

# ── Accent colors ────────────────────────────────────
ACC    = CYAN
ACC2   = GREEN
BORDER = GREEN_DIM

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.012):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner():
    clear()
    print(f"{BORDER}")
    print(f"  ╔{'═'*55}╗")
    print(f"  ║{' '*55}║")
    print(f"  ║{ACC}{BOLD}    ░█████╗░██╗░░░██╗░█████╗░                         {RESET}{BORDER}║")
    print(f"  ║{ACC}{BOLD}    ██╔══██╗╚██╗░██╔╝██╔══██╗                         {RESET}{BORDER}║")
    print(f"  ║{ACC}{BOLD}    ███████║░╚████╔╝░██║░░██║                         {RESET}{BORDER}║")
    print(f"  ║{ACC}{BOLD}    ██╔══██║░░╚██╔╝░░██║░░██║                         {RESET}{BORDER}║")
    print(f"  ║{ACC}{BOLD}    ██║░░██║░░░██║░░░╚█████╔╝                         {RESET}{BORDER}║")
    print(f"  ║{ACC}{BOLD}    ╚═╝░░╚═╝░░░╚═╝░░░░╚════╝                         {RESET}{BORDER}║")
    print(f"  ║{' '*55}║")
    print(f"  ╚{'═'*55}╝{RESET}")
    print()
    slow_print(f"  {BOLD}{ACC}    A T T A C K   Y O U R   O F F E N D E R S{RESET}", 0.018)
    print()
    print(f"  {DIM}{WHITE}    By Fashipe Oluwadamilare Ayoola{RESET}")
    print(f"  {DIM}{WHITE}    CS/Cybersecurity · MIVA Open University{RESET}")
    print()
    print(f"  {YELLOW}  ⚠  Authorized Testing & CTFs ONLY — Unauthorized use is illegal{RESET}")
    print()
    print(f"  {BORDER}{'─'*57}{RESET}")

def menu():
    print(f"""
  {ACC}{BOLD}[ MODULES ]{RESET}
  {BORDER}{'─'*57}{RESET}

  {ACC}[1]{RESET}  {WHITE}Phishing Kit Generator{RESET}
       {GRAY}Craft convincing credential harvest pages{RESET}

  {ACC}[2]{RESET}  {WHITE}Steganography Suite{RESET}
       {GRAY}Hide & extract data inside images and text{RESET}

  {ACC}[3]{RESET}  {WHITE}Social Engineering Toolkit{RESET}
       {GRAY}Pretexting scripts, vishing guides, OSINT checklists{RESET}

  {ACC}[4]{RESET}  {WHITE}Password Tools{RESET}
       {GRAY}Generate, analyze, identify, and crack hashes{RESET}

  {ACC}[5]{RESET}  {WHITE}Network Tools{RESET}
       {GRAY}Port scan, DNS lookup, ping sweep, banner grab{RESET}

  {ACC}[6]{RESET}  {WHITE}Crypto Tools{RESET}
       {GRAY}Caesar, Vigenère, XOR, Base64, AES-256 & more{RESET}

  {BORDER}{'─'*57}{RESET}
  {GRAY}[h]{RESET} Help    {GRAY}[c]{RESET} Credits    {GRAY}[q]{RESET} Quit
  {BORDER}{'─'*57}{RESET}
""")

def credits_screen():
    clear()
    print(f"""
  {BORDER}╔{'═'*55}╗
  ║{'CREDITS':^55}║
  ╚{'═'*55}╝{RESET}

  {ACC}Framework   :{RESET}  AYO — Attack Your Offenders
  {ACC}Author      :{RESET}  Fashipe Oluwadamilare Ayoola
  {ACC}Institution :{RESET}  MIVA Open University
  {ACC}Program     :{RESET}  CS / Cybersecurity
  {ACC}Internship  :{RESET}  Pintop Technologies Limited, Lagos
  {ACC}GitHub      :{RESET}  github.com/MarceloMiva/AYO

  {BORDER}{'─'*57}{RESET}
  {DIM}Built for learning, CTFs, and authorized engagements.
  Inspired by the tools of the trade.{RESET}

  {YELLOW}  [ Use responsibly. You are accountable for your actions. ]{RESET}
""")
    input(f"  {GRAY}Press Enter to return...{RESET}")

def help_screen():
    clear()
    print(f"""
  {BORDER}╔{'═'*55}╗
  ║{'HELP':^55}║
  ╚{'═'*55}╝{RESET}

  {WHITE}Each module is self-contained with its own menu.{RESET}
  {GRAY}Use [b] inside any module to return here.{RESET}

  {BORDER}{'─'*57}{RESET}

  {ACC}[1] Phishing Kit{RESET}
      {GRAY}Generate HTML lure pages mimicking login portals.
      Captures credentials to a local log (lab use only).{RESET}

  {ACC}[2] Steganography{RESET}
      {GRAY}Hide text in PNG/JPG via LSB encoding.
      Also supports zero-width character text stego.{RESET}

  {ACC}[3] Social Engineering{RESET}
      {GRAY}Pretext scripts, vishing call guides, OSINT checklists
      and awareness training scenarios.{RESET}

  {ACC}[4] Password Tools{RESET}
      {GRAY}Wordlist generator, hash identifier, strength analyzer,
      and dictionary-based hash cracker.{RESET}

  {ACC}[5] Network Tools{RESET}
      {GRAY}Port scanner, ping sweep, DNS lookup,
      reverse DNS, and banner grabbing.{RESET}

  {ACC}[6] Crypto Tools{RESET}
      {GRAY}Caesar, Vigenère, XOR, Base64, Hex, AES-256,
      ROT13, and frequency analysis.{RESET}

  {BORDER}{'─'*57}{RESET}
""")
    input(f"  {GRAY}Press Enter to return...{RESET}")

def main():
    banner()
    menu()

    while True:
        try:
            choice = input(f"  {ACC}[ayo]>{RESET} ").strip().lower()

            if choice == "1":
                from modules.phishing import run_phishing
                run_phishing()
                banner()
                menu()
            elif choice == "2":
                from modules.steganography import run_steganography
                run_steganography()
                banner()
                menu()
            elif choice == "3":
                from modules.social_engineering import run_social_engineering
                run_social_engineering()
                banner()
                menu()
            elif choice == "4":
                from modules.password_tools import run_password_tools
                run_password_tools()
                banner()
                menu()
            elif choice == "5":
                from modules.network_tools import run_network_tools
                run_network_tools()
                banner()
                menu()
            elif choice == "6":
                from modules.crypto_tools import run_crypto_tools
                run_crypto_tools()
                banner()
                menu()
            elif choice == "h":
                help_screen()
                banner()
                menu()
            elif choice == "c":
                credits_screen()
                banner()
                menu()
            elif choice in ["q", "quit", "exit"]:
                print(f"\n  {ACC}[ AYO shutting down. Stay legal. ]{RESET}\n")
                sys.exit(0)
            else:
                print(f"  {YELLOW}[!] Invalid option. Type a number or [h] for help.{RESET}\n")

        except KeyboardInterrupt:
            print(f"\n\n  {ACC}[ Interrupted. Exiting AYO. ]{RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
