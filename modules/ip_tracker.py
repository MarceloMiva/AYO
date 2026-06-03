import requests
import json

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def check_ip(ip):
    try:
        # Try ipwhois.app (more reliable free API)
        r = requests.get(f"https://ipwhois.app/json/{ip}", timeout=6)
        data = r.json()
        
        if data.get("success"):
            print(f"\n  {GREEN}[+] IP Information for {ip}:{RESET}\n")
            print(f"  {CYAN}Location:{RESET}")
            print(f"    Country: {data.get('country')} ({data.get('country_code')})")
            print(f"    Region: {data.get('region')}")
            print(f"    City: {data.get('city')}")
            print(f"    Timezone: {data.get('timezone')}")
            print(f"    Coordinates: {data.get('latitude')}, {data.get('longitude')}")
            
            print(f"\n  {CYAN}Network:{RESET}")
            print(f"    ISP: {data.get('isp')}")
            print(f"    Type: {data.get('type')}")
            
            print(f"\n  {CYAN}Additional:{RESET}")
            print(f"    Continent: {data.get('continent_name')}")
            print(f"    Currency: {data.get('currency_code')}")
        else:
            print(f"  {RED}[!] Invalid IP or API error{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {str(e)[:60]}{RESET}")

def run_ip_tracker():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  IP TRACKER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Lookup single IP
  {ACC}[2]{RESET} Batch IP lookup (file)
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}Uses ipwhois.app (free, no rate limit){RESET}""")
        choice = input(f"  {ACC}[iptracker]>{RESET} ").strip().lower()

        if choice == "1":
            ip = input(f"  {GRAY}Enter IP address: {RESET}").strip()
            if ip:
                check_ip(ip)

        elif choice == "2":
            filepath = input(f"  {GRAY}Enter file path (one IP per line): {RESET}").strip()
            try:
                with open(filepath, 'r') as f:
                    ips = [line.strip() for line in f if line.strip()]
                print(f"  {YELLOW}[*] Processing {len(ips)} IPs...{RESET}")
                for ip in ips:
                    check_ip(ip)
                    input(f"  {GRAY}Press Enter for next...{RESET}")
            except FileNotFoundError:
                print(f"  {RED}[!] File not found.{RESET}")

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
