# ═══════════════════════════════════════════
#  AYO — Module [5]: Network Tools
# ═══════════════════════════════════════════

import socket
import subprocess
import platform
import concurrent.futures
import ipaddress

RED   = "\033[91m"
DRED  = "\033[31m"
WHITE = "\033[97m"
GRAY  = "\033[90m"
YELLOW= "\033[93m"
GREEN = "\033[92m"
DIM   = "\033[2m"
BOLD  = "\033[1m"
RESET = "\033[0m"

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

def net_banner():
    print(f"""
{DRED}╔══════════════════════════════════════════════╗
║          NETWORK TOOLS — MODULE [5]          ║
╚══════════════════════════════════════════════╝{RESET}
{DIM}Port scanning, DNS lookup, ping sweep, banner grabbing.{RESET}
""")

# ── Port scanner ─────────────────────────────
def scan_port(host, port, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except:
        return False

def grab_banner(host, port, timeout=2):
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((host, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner[:100] if banner else None
    except:
        return None

def port_scan(host, ports, threads=50):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as ex:
        future_map = {ex.submit(scan_port, host, p): p for p in ports}
        for future in concurrent.futures.as_completed(future_map):
            port = future_map[future]
            if future.result():
                open_ports.append(port)
    return sorted(open_ports)

# ── DNS lookup ───────────────────────────────
def dns_lookup(domain):
    results = {}
    try:
        results["A"] = socket.gethostbyname(domain)
    except:
        results["A"] = "Failed"
    try:
        info = socket.getaddrinfo(domain, None)
        results["All IPs"] = list(set(i[4][0] for i in info))
    except:
        pass
    try:
        results["Hostname"] = socket.getfqdn(domain)
    except:
        pass
    return results

# ── Reverse DNS ──────────────────────────────
def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "No PTR record"

# ── Ping ─────────────────────────────────────
def ping_host(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd = ["ping", param, "1", "-W", "1", host]
    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3)
        return result.returncode == 0
    except:
        return False

# ── Ping sweep ───────────────────────────────
def ping_sweep(cidr, max_workers=50):
    live = []
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        hosts = list(network.hosts())
        if len(hosts) > 256:
            print(f"  {YELLOW}[!] Limiting sweep to first 256 hosts.{RESET}")
            hosts = hosts[:256]
        print(f"  {DIM}[*] Sweeping {len(hosts)} hosts...{RESET}\n")
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            future_map = {ex.submit(ping_host, str(h)): str(h) for h in hosts}
            for future in concurrent.futures.as_completed(future_map):
                host = future_map[future]
                if future.result():
                    live.append(host)
                    print(f"  {RED}[+]{RESET} {WHITE}{host}{RESET} {GREEN}UP{RESET}")
    except ValueError as e:
        print(f"  {YELLOW}[!] Invalid CIDR: {e}{RESET}")
    return sorted(live)

def run_network_tools():
    net_banner()

    while True:
        print(f"  {RED}[1]{RESET} Port scan (common ports)")
        print(f"  {RED}[2]{RESET} Port scan (custom range)")
        print(f"  {RED}[3]{RESET} DNS lookup")
        print(f"  {RED}[4]{RESET} Reverse DNS")
        print(f"  {RED}[5]{RESET} Ping sweep (CIDR)")
        print(f"  {RED}[6]{RESET} Banner grab")
        print(f"  {RED}[b]{RESET} Back\n")

        choice = input(f"  {RED}[net]>{RESET} ").strip().lower()

        if choice == "1":
            host = input(f"\n  {WHITE}Target host/IP:{RESET} ").strip()
            print(f"  {DIM}[*] Scanning {len(COMMON_PORTS)} common ports on {host}...{RESET}\n")
            try:
                ip = socket.gethostbyname(host)
                open_ports = port_scan(ip, list(COMMON_PORTS.keys()))
                if open_ports:
                    print(f"  {'PORT':<10} {'SERVICE':<15} {'STATUS'}")
                    print(f"  {'─'*8} {'─'*13} {'─'*6}")
                    for p in open_ports:
                        svc = COMMON_PORTS.get(p, "Unknown")
                        print(f"  {RED}{p:<10}{RESET} {WHITE}{svc:<15}{RESET} {GREEN}OPEN{RESET}")
                else:
                    print(f"  {YELLOW}[-] No open ports found.{RESET}")
                print()
            except socket.gaierror:
                print(f"  {YELLOW}[!] Could not resolve host.{RESET}\n")

        elif choice == "2":
            host = input(f"\n  {WHITE}Target host/IP:{RESET} ").strip()
            try:
                start = int(input(f"  {WHITE}Start port:{RESET} ").strip())
                end   = int(input(f"  {WHITE}End port:{RESET} ").strip())
                ports = list(range(start, end + 1))
                print(f"  {DIM}[*] Scanning ports {start}-{end} on {host}...{RESET}\n")
                ip = socket.gethostbyname(host)
                open_ports = port_scan(ip, ports)
                if open_ports:
                    for p in open_ports:
                        svc = COMMON_PORTS.get(p, "Unknown")
                        print(f"  {RED}[+]{RESET} Port {WHITE}{p}{RESET} — {svc} {GREEN}OPEN{RESET}")
                else:
                    print(f"  {YELLOW}[-] No open ports in range.{RESET}")
                print()
            except (ValueError, socket.gaierror) as e:
                print(f"  {YELLOW}[!] Error: {e}{RESET}\n")

        elif choice == "3":
            domain = input(f"\n  {WHITE}Domain:{RESET} ").strip()
            results = dns_lookup(domain)
            print()
            for k, v in results.items():
                print(f"  {RED}{k:<12}{RESET} {WHITE}{v}{RESET}")
            print()

        elif choice == "4":
            ip = input(f"\n  {WHITE}IP address:{RESET} ").strip()
            hostname = reverse_dns(ip)
            print(f"  {RED}[+] PTR:{RESET} {WHITE}{hostname}{RESET}\n")

        elif choice == "5":
            cidr = input(f"\n  {WHITE}CIDR range (e.g. 192.168.1.0/24):{RESET} ").strip()
            live = ping_sweep(cidr)
            print(f"\n  {RED}[+] Live hosts: {len(live)}{RESET}\n")

        elif choice == "6":
            host = input(f"\n  {WHITE}Host:{RESET} ").strip()
            try:
                port = int(input(f"  {WHITE}Port:{RESET} ").strip())
                print(f"  {DIM}[*] Grabbing banner from {host}:{port}...{RESET}")
                banner = grab_banner(host, port)
                if banner:
                    print(f"\n  {RED}[+] Banner:{RESET}")
                    print(f"  {GRAY}{banner}{RESET}\n")
                else:
                    print(f"  {YELLOW}[-] No banner received.{RESET}\n")
            except ValueError:
                print(f"  {YELLOW}[!] Invalid port.{RESET}\n")

        elif choice in ["b", "back"]:
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}\n")
