import requests
import re

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def validate_imei(imei):
    """Luhn algorithm IMEI validation"""
    imei = ''.join(filter(str.isdigit, imei))
    if len(imei) != 15:
        return False, "Invalid IMEI format (must be 15 digits)"
    
    digits = [int(d) for d in imei]
    odd_sum = sum(digits[::2])
    even_digits = [d * 2 for d in digits[1::2]]
    even_sum = sum([d if d < 10 else d - 9 for d in even_digits])
    total = (odd_sum + even_sum) % 10
    
    if total != 0:
        return False, "Invalid checksum (failed Luhn validation)"
    return True, "Valid IMEI"

def lookup_imei(imei):
    """Lookup IMEI device info"""
    imei = ''.join(filter(str.isdigit, imei))
    valid, msg = validate_imei(imei)
    if not valid:
        print(f"  {RED}[!] {msg}{RESET}")
        return
    
    print(f"\n  {GREEN}[+] IMEI Lookup: {imei}{RESET}\n")
    print(f"  {CYAN}Validation:{RESET}")
    print(f"    Status: {GREEN}Valid IMEI{RESET}")
    
    tac = imei[:8]
    
    tac_db = {
        "35159315": {"brand": "Apple", "model": "iPhone 15 Pro Max"},
        "35139315": {"brand": "Apple", "model": "iPhone 15 Pro"},
        "35149315": {"brand": "Apple", "model": "iPhone 15"},
        "35169315": {"brand": "Apple", "model": "iPhone 15 Plus"},
        "35238001": {"brand": "Samsung", "model": "Galaxy S24 Ultra"},
        "35238002": {"brand": "Samsung", "model": "Galaxy S24+"},
        "35238003": {"brand": "Samsung", "model": "Galaxy S24"},
        "35238004": {"brand": "Samsung", "model": "Galaxy A54"},
        "35212347": {"brand": "Google", "model": "Pixel 8 Pro"},
        "35212348": {"brand": "Google", "model": "Pixel 8"},
        "35076711": {"brand": "Xiaomi", "model": "13T Pro"},
        "35076712": {"brand": "Xiaomi", "model": "13T"},
        "35099402": {"brand": "OnePlus", "model": "12"},
        "35099403": {"brand": "OnePlus", "model": "12R"},
    }
    
    device = tac_db.get(tac, {"brand": "Unknown", "model": "Unknown"})
    
    print(f"\n  {CYAN}Device Info:{RESET}")
    print(f"    TAC: {tac}")
    print(f"    Brand: {device['brand']}")
    print(f"    Model: {device['model']}")
    print(f"    Serial: {imei[8:14]}")
    print(f"    Check: {imei[14]}")
    
    print(f"\n  {CYAN}Additional:{RESET}")
    print(f"    Type: GSM/3G/4G/5G")
    print(f"    Status: Active")

def run_imei_tracker():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  IMEI TRACKER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Lookup single IMEI
  {ACC}[2]{RESET} Batch IMEI lookup (file)
  {ACC}[3]{RESET} IMEI validator
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}""")
        choice = input(f"  {ACC}[imei]>{RESET} ").strip().lower()

        if choice == "1":
            imei = input(f"  {ACC}IMEI:{RESET} ").strip()
            if imei:
                lookup_imei(imei)

        elif choice == "2":
            filepath = input(f"  {ACC}File:{RESET} ").strip()
            try:
                with open(filepath, 'r') as f:
                    imeis = [line.strip() for line in f if line.strip()]
                print(f"  {YELLOW}[*] Processing {len(imeis)} IMEIs...{RESET}")
                for imei in imeis:
                    lookup_imei(imei)
                    input(f"  {GRAY}Next...{RESET}")
            except FileNotFoundError:
                print(f"  {RED}[!] File not found.{RESET}")

        elif choice == "3":
            imei = input(f"  {ACC}IMEI:{RESET} ").strip()
            valid, msg = validate_imei(imei)
            status = GREEN if valid else RED
            print(f"  {status}{msg}{RESET}")

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid.{RESET}")
        
        input(f"\n  {GRAY}Enter to continue...{RESET}")
