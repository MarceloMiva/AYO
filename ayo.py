# ================================================
#  AYO — Attack Your Offenders
#  By Fashipe Oluwadamilare Ayoola
#  For authorized testing & CTFs ONLY
# ================================================

import os, sys, time

GREEN      = "\033[92m"; GREEN_DIM = "\033[32m"
CYAN       = "\033[96m"; WHITE     = "\033[97m"
YELLOW     = "\033[93m"; RED       = "\033[91m"
GRAY       = "\033[90m"; BOLD      = "\033[1m"
DIM        = "\033[2m";  RESET     = "\033[0m"
ACC = CYAN; ACC2 = GREEN; BORDER = GREEN_DIM

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
    print(f"{BORDER}{'='*55}{RESET}")
    print(f"{BORDER}||{' '*53}||{RESET}")
    print(f"{BORDER}||{ACC}{BOLD}   ░█████╗░██╗░░░██╗░█████╗░{RESET}{BORDER}               ||{RESET}")
    print(f"{BORDER}||{ACC}{BOLD}   ██╔══██╗╚██╗░██╔╝██╔══██╗{RESET}{BORDER}               ||{RESET}")
    print(f"{BORDER}||{ACC}{BOLD}   ███████║░╚████╔╝░██║░░██║{RESET}{BORDER}               ||{RESET}")
    print(f"{BORDER}||{ACC}{BOLD}   ██╔══██║░░╚██╔╝░░██║░░██║{RESET}{BORDER}               ||{RESET}")
    print(f"{BORDER}||{ACC}{BOLD}   ██║░░██║░░░██║░░░╚█████╔╝{RESET}{BORDER}               ||{RESET}")
    print(f"{BORDER}||{' '*53}||{RESET}")
    print(f"{BORDER}{'='*55}{RESET}")
    slow_print(f"  {BOLD}{ACC}    A T T A C K   Y O U R   O F F E N D E R S{RESET}", 0.018)
    print()

def menu():
    print(f"""{BORDER}{'─'*55}{RESET}
{ACC}{BOLD}  OFFENSIVE MODULES{RESET}
{BORDER}{'─'*55}{RESET}
  {ACC}[1]{RESET}  Phishing Kit          {ACC}[2]{RESET}  Steganography
  {ACC}[3]{RESET}  Social Engineering    {ACC}[4]{RESET}  Password Tools
  {ACC}[5]{RESET}  Network Tools         {ACC}[6]{RESET}  Crypto Tools
{BORDER}{'─'*55}{RESET}
{ACC}{BOLD}  RECON & OSINT{RESET}
{BORDER}{'─'*55}{RESET}
  {ACC}[7]{RESET}  OSINT Lookup          {ACC}[8]{RESET}  Hash Cracker
  {ACC}[9]{RESET}  Wordlist Generator    {ACC}[10]{RESET} Subdomain Enum
  {ACC}[11]{RESET} Dir Bruteforcer
{BORDER}{'─'*55}{RESET}
{ACC}{BOLD}  WEB ATTACKS{RESET}
{BORDER}{'─'*55}{RESET}
  {ACC}[12]{RESET} SQLi Tester           {ACC}[13]{RESET} XSS Tester
  {ACC}[22]{RESET} Web Vuln Scanner
{BORDER}{'─'*55}{RESET}
{ACC}{BOLD}  NETWORK ATTACKS{RESET}
{BORDER}{'─'*55}{RESET}
  {ACC}[14]{RESET} SSH Bruteforce        {ACC}[15]{RESET} WiFi Scanner
  {ACC}[16]{RESET} ARP Spoof/MITM        {ACC}[17]{RESET} Packet Sniffer
  {ACC}[18]{RESET} Port Knocker
{BORDER}{'─'*55}{RESET}
{ACC}{BOLD}  EVASION & POST-EXPLOITATION{RESET}
{BORDER}{'─'*55}{RESET}
  {ACC}[19]{RESET} File Encryptor        {ACC}[20]{RESET} Metadata Cleaner
  {ACC}[21]{RESET} Payload Encoder
{BORDER}{'─'*55}{RESET}
  {ACC}[h]{RESET} Help   {ACC}[c]{RESET} Credits   {ACC}[q]{RESET} Quit
{BORDER}{'─'*55}{RESET}""")

def credits_screen():
    clear()
    print(f"""
{BORDER}{'='*55}{RESET}
{ACC}{BOLD}{'CREDITS':^55}{RESET}
{BORDER}{'='*55}{RESET}

  {WHITE}Tool    :{RESET} AYO — Attack Your Offenders
  {WHITE}Author  :{RESET} Fashipe Oluwadamilare Ayoola
  {WHITE}GitHub  :{RESET} github.com/MarceloMiva
  {WHITE}Purpose :{RESET} Authorized testing & CTFs ONLY
  {WHITE}Version :{RESET} 2.1 — 22 Modules, Web Scanner Added

{BORDER}{'─'*55}{RESET}
  {GRAY}22 modules | Built on Termux/Android{RESET}
{BORDER}{'='*55}{RESET}""")
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
            elif choice == "2":
                from modules.steganography import run_steganography
                run_steganography()
            elif choice == "3":
                from modules.social_engineering import run_social_engineering
                run_social_engineering()
            elif choice == "4":
                from modules.password_tools import run_password_tools
                run_password_tools()
            elif choice == "5":
                from modules.network_tools import run_network_tools
                run_network_tools()
            elif choice == "6":
                from modules.crypto_tools import run_crypto_tools
                run_crypto_tools()
            elif choice == "7":
                from modules.osint import run_osint
                run_osint()
            elif choice == "8":
                from modules.hash_cracker import run_hash_cracker
                run_hash_cracker()
            elif choice == "9":
                from modules.wordlist_gen import run_wordlist_gen
                run_wordlist_gen()
            elif choice == "10":
                from modules.subdomain_enum import run_subdomain_enum
                run_subdomain_enum()
            elif choice == "11":
                from modules.dir_bruteforce import run_dir_bruteforce
                run_dir_bruteforce()
            elif choice == "12":
                from modules.sqli_tester import run_sqli_tester
                run_sqli_tester()
            elif choice == "13":
                from modules.xss_tester import run_xss_tester
                run_xss_tester()
            elif choice == "14":
                from modules.ssh_bruteforce import run_ssh_bruteforce
                run_ssh_bruteforce()
            elif choice == "15":
                from modules.wifi_scanner import run_wifi_scanner
                run_wifi_scanner()
            elif choice == "16":
                from modules.arp_spoof import run_arp_spoof
                run_arp_spoof()
            elif choice == "17":
                from modules.packet_sniffer import run_packet_sniffer
                run_packet_sniffer()
            elif choice == "18":
                from modules.port_knocker import run_port_knocker
                run_port_knocker()
            elif choice == "19":
                from modules.file_encryptor import run_file_encryptor
                run_file_encryptor()
            elif choice == "20":
                from modules.metadata_cleaner import run_metadata_cleaner
                run_metadata_cleaner()
            elif choice == "21":
                from modules.payload_encoder import run_payload_encoder
                run_payload_encoder()
            elif choice == "22":
                from modules.web_vuln_scanner import run_web_vuln_scanner
                run_web_vuln_scanner()
            elif choice == "h":
                pass
            elif choice == "c":
                credits_screen()
            elif choice in ["q","quit","exit"]:
                print(f"\n  {ACC}[ AYO shutting down. Stay legal. ]{RESET}\n")
                sys.exit(0)
            else:
                print(f"  {YELLOW}[!] Invalid option.{RESET}\n")
                continue

            banner()
            menu()

        except KeyboardInterrupt:
            print(f"\n\n  {ACC}[ Interrupted. Exiting AYO. ]{RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main()
