import socket, time, os

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

COMMON_SEQUENCES = {
    "OpenSSH knock": [7000, 8000, 9000],
    "knockd default": [1234, 5678, 9012],
    "fail2ban bypass": [4000, 5000, 6000],
    "custom reverse": [9999, 8888, 7777],
}

def knock(host, ports, protocol="tcp", delay=0.3):
    print(f"\n  {ACC}[*] Knocking on {host}{RESET}")
    print(f"  {ACC}[*] Sequence: {ports}{RESET}\n")

    for port in ports:
        try:
            if protocol.lower() == "tcp":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                s.connect_ex((host, port))
                s.close()
                print(f"  {GREEN}[+]{RESET} Knocked TCP:{port}")
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(0.5)
                s.sendto(b'\x00', (host, port))
                s.close()
                print(f"  {YELLOW}[+]{RESET} Knocked UDP:{port}")
            time.sleep(delay)
        except Exception as e:
            print(f"  {GRAY}[*]{RESET} Port {port} — {GRAY}{e}{RESET}")
            time.sleep(delay)

    print(f"\n  {ACC}[*] Knock sequence complete.{RESET}")
    print(f"  {GRAY}Now try connecting to your target service.{RESET}")

def verify_port(host, port, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, int(port)))
        s.close()
        return result == 0
    except:
        return False

def run_port_knocker():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  PORT KNOCKER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Custom knock sequence
  {ACC}[2]{RESET} Use preset sequence
  {ACC}[3]{RESET} Verify port is open after knock
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}""")
        choice = input(f"  {ACC}[knock]>{RESET} ").strip().lower()

        if choice == "1":
            host = input(f"  {GRAY}Target host/IP: {RESET}").strip()
            ports_input = input(f"  {GRAY}Port sequence (comma separated e.g. 7000,8000,9000): {RESET}").strip()
            proto = input(f"  {GRAY}Protocol [tcp/udp]: {RESET}").strip().lower() or "tcp"
            try:
                delay = float(input(f"  {GRAY}Delay between knocks in sec [0.3]: {RESET}").strip() or "0.3")
                ports = [int(p.strip()) for p in ports_input.split(',')]
                if host and ports:
                    knock(host, ports, proto, delay)
            except ValueError:
                print(f"  {RED}[!] Invalid input.{RESET}")

        elif choice == "2":
            print(f"\n  {ACC}Available presets:{RESET}")
            for i, (name, seq) in enumerate(COMMON_SEQUENCES.items(), 1):
                print(f"  {ACC}[{i}]{RESET} {name}: {seq}")
            sel = input(f"\n  {GRAY}Choose preset: {RESET}").strip()
            host = input(f"  {GRAY}Target host/IP: {RESET}").strip()
            try:
                name = list(COMMON_SEQUENCES.keys())[int(sel)-1]
                ports = COMMON_SEQUENCES[name]
                if host:
                    knock(host, ports)
            except (ValueError, IndexError):
                print(f"  {RED}[!] Invalid selection.{RESET}")

        elif choice == "3":
            host = input(f"  {GRAY}Host: {RESET}").strip()
            port = input(f"  {GRAY}Port to verify: {RESET}").strip()
            if host and port:
                print(f"\n  {ACC}[*] Checking {host}:{port}...{RESET}")
                if verify_port(host, port):
                    print(f"  {GREEN}[+] Port {port} is OPEN!{RESET}")
                else:
                    print(f"  {RED}[-] Port {port} is CLOSED or filtered.{RESET}")

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
