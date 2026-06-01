import socket, struct, os, time

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

PROTOCOLS = {1: "ICMP", 6: "TCP", 17: "UDP"}

def parse_ethernet(data):
    dst = ':'.join(f'{b:02x}' for b in data[:6])
    src = ':'.join(f'{b:02x}' for b in data[6:12])
    proto = struct.unpack('!H', data[12:14])[0]
    return dst, src, proto, data[14:]

def parse_ip(data):
    ihl = (data[0] & 0xF) * 4
    proto = data[9]
    src = socket.inet_ntoa(data[12:16])
    dst = socket.inet_ntoa(data[16:20])
    return src, dst, proto, data[ihl:]

def parse_tcp(data):
    src_port = struct.unpack('!H', data[0:2])[0]
    dst_port = struct.unpack('!H', data[2:4])[0]
    offset = ((data[12] >> 4) * 4)
    payload = data[offset:]
    return src_port, dst_port, payload

def parse_udp(data):
    src_port = struct.unpack('!H', data[0:2])[0]
    dst_port = struct.unpack('!H', data[2:4])[0]
    payload = data[8:]
    return src_port, dst_port, payload

def sniff(iface=None, count=50, filter_proto=None, save_file=None):
    print(f"\n  {ACC}[*] Starting packet capture...{RESET}")
    print(f"  {GRAY}Press CTRL+C to stop.{RESET}\n")

    captured = []
    try:
        sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                             socket.ntohs(0x0003))
        if iface:
            sock.bind((iface, 0))
    except PermissionError:
        print(f"  {RED}[!] Root required for raw socket capture.{RESET}")
        print(f"  {GRAY}Try running with: sudo python ayo.py{RESET}")
        return
    except OSError as e:
        print(f"  {RED}[!] Error: {e}{RESET}")
        return

    pkt_count = 0
    try:
        while pkt_count < count:
            raw, addr = sock.recvfrom(65535)
            try:
                dst_mac, src_mac, eth_proto, ip_data = parse_ethernet(raw)
                if eth_proto != 0x0800:
                    continue
                src_ip, dst_ip, proto, transport = parse_ip(ip_data)
                proto_name = PROTOCOLS.get(proto, str(proto))

                if filter_proto and proto_name != filter_proto.upper():
                    continue

                pkt_count += 1
                ts = time.strftime("%H:%M:%S")

                if proto == 6:  # TCP
                    sp, dp, payload = parse_tcp(transport)
                    color = CYAN
                    info = f"{src_ip}:{sp} → {dst_ip}:{dp}"
                elif proto == 17:  # UDP
                    sp, dp, payload = parse_udp(transport)
                    color = YELLOW
                    info = f"{src_ip}:{sp} → {dst_ip}:{dp}"
                    payload = b""
                else:
                    color = GRAY
                    info = f"{src_ip} → {dst_ip}"
                    payload = b""

                print(f"  {color}[{proto_name}]{RESET} {GRAY}{ts}{RESET} {info}")

                # Show payload snippet if HTTP
                if proto == 6 and payload:
                    try:
                        text = payload.decode('utf-8', errors='ignore')
                        if any(k in text for k in ['GET ','POST ','HTTP','Host:','password','user']):
                            snippet = text[:120].replace('\n',' ').replace('\r','')
                            print(f"  {RED}  ↳ {snippet}{RESET}")
                    except:
                        pass

                captured.append(f"[{proto_name}] {ts} {info}")

            except Exception:
                continue

    except KeyboardInterrupt:
        print(f"\n\n  {ACC}[*] Capture stopped. {pkt_count} packets captured.{RESET}")
    finally:
        sock.close()

    if save_file and captured:
        with open(save_file, 'w') as f:
            f.write('\n'.join(captured))
        print(f"  {GREEN}[+] Saved to {save_file}{RESET}")

def run_packet_sniffer():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  PACKET SNIFFER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Sniff all packets
  {ACC}[2]{RESET} Sniff TCP only
  {ACC}[3]{RESET} Sniff UDP only
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}Requires root access.{RESET}""")
        choice = input(f"  {ACC}[sniff]>{RESET} ").strip().lower()

        if choice in ["1","2","3"]:
            iface = input(f"  {GRAY}Interface [wlan0]: {RESET}").strip() or "wlan0"
            try:
                count = int(input(f"  {GRAY}Packet limit [50]: {RESET}").strip() or "50")
            except:
                count = 50
            save = input(f"  {GRAY}Save to file? (filename or blank): {RESET}").strip()
            fmap = {"1": None, "2": "TCP", "3": "UDP"}
            sniff(iface, count, fmap[choice], save or None)

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
