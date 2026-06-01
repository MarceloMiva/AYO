import os, json, subprocess

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def scan_wifi_termux():
    print(f"\n  {ACC}[*] Scanning nearby WiFi networks...{RESET}\n")
    try:
        result = subprocess.run(
            ["termux-wifi-scaninfo"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0 or not result.stdout.strip():
            print(f"  {RED}[!] termux-api not installed or no results.{RESET}")
            print(f"  {GRAY}Fix: pkg install termux-api{RESET}")
            print(f"  {GRAY}Also install Termux:API app from F-Droid.{RESET}")
            return

        networks = json.loads(result.stdout)
        if not networks:
            print(f"  {YELLOW}[!] No networks found.{RESET}")
            return

        print(f"  {BORDER}{'─'*55}{RESET}")
        print(f"  {ACC}{BOLD}{'SSID':<25} {'BSSID':<20} {'RSSI':>5} {'SEC'}{RESET}")
        print(f"  {BORDER}{'─'*55}{RESET}")

        for net in sorted(networks, key=lambda x: x.get('rssi', -999), reverse=True):
            ssid = net.get('ssid', 'Hidden')[:24]
            bssid = net.get('bssid', 'N/A')
            rssi = net.get('rssi', '?')
            freq = net.get('frequency', 0)
            caps = net.get('capabilities', '')

            # Signal strength bar
            if isinstance(rssi, int):
                if rssi >= -50: bar = f"{GREEN}████ Excellent{RESET}"
                elif rssi >= -60: bar = f"{GREEN}███  Good{RESET}"
                elif rssi >= -70: bar = f"{YELLOW}██   Fair{RESET}"
                else: bar = f"{RED}█    Weak{RESET}"
            else:
                bar = GRAY + "Unknown" + RESET

            # Security type
            if "WPA3" in caps: sec = f"{GREEN}WPA3{RESET}"
            elif "WPA2" in caps: sec = f"{YELLOW}WPA2{RESET}"
            elif "WPA" in caps: sec = f"{YELLOW}WPA{RESET}"
            elif "WEP" in caps: sec = f"{RED}WEP{RESET}"
            else: sec = f"{RED}OPEN{RESET}"

            band = "5GHz" if freq > 3000 else "2.4GHz"

            print(f"  {WHITE if 'WHITE' in dir() else ''}{ssid:<25}{RESET} {GRAY}{bssid}{RESET}")
            print(f"  {GRAY}  Signal: {bar}  ({rssi}dBm)  Band: {band}  Security: {sec}{RESET}")
            print()

        print(f"  {ACC}[*] Total networks found: {len(networks)}{RESET}")

        save = input(f"\n  {GRAY}Save results? (y/n): {RESET}").strip().lower()
        if save == 'y':
            with open('wifi_scan.txt', 'w') as f:
                for net in networks:
                    f.write(f"{net.get('ssid','Hidden')} | {net.get('bssid')} | {net.get('rssi')}dBm | {net.get('capabilities','')}\n")
            print(f"  {GREEN}[+] Saved to wifi_scan.txt{RESET}")

    except FileNotFoundError:
        print(f"  {RED}[!] termux-wifi-scaninfo not found.{RESET}")
        print(f"  {GRAY}Run: pkg install termux-api{RESET}")
        print(f"  {GRAY}Then install Termux:API app from F-Droid.{RESET}")
    except json.JSONDecodeError:
        print(f"  {RED}[!] Could not parse scan results.{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

def get_current_wifi():
    print(f"\n  {ACC}[*] Getting current WiFi info...{RESET}\n")
    try:
        result = subprocess.run(
            ["termux-wifi-connectioninfo"],
            capture_output=True, text=True, timeout=8
        )
        if result.stdout.strip():
            info = json.loads(result.stdout)
            print(f"  {GREEN}SSID    :{RESET} {info.get('ssid','N/A')}")
            print(f"  {GREEN}BSSID   :{RESET} {info.get('bssid','N/A')}")
            print(f"  {GREEN}IP      :{RESET} {info.get('ip','N/A')}")
            print(f"  {GREEN}Speed   :{RESET} {info.get('link_speed_mbps','N/A')} Mbps")
            print(f"  {GREEN}Signal  :{RESET} {info.get('rssi','N/A')} dBm")
            print(f"  {GREEN}Freq    :{RESET} {info.get('frequency_mhz','N/A')} MHz")
        else:
            print(f"  {RED}[!] Not connected or termux-api missing.{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

def run_wifi_scanner():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  WIFI SCANNER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Scan nearby networks
  {ACC}[2]{RESET} Current connection info
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}Requires: pkg install termux-api{RESET}""")
        choice = input(f"  {ACC}[wifi]>{RESET} ").strip().lower()

        if choice == "1":
            scan_wifi_termux()
        elif choice == "2":
            get_current_wifi()
        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
