import os, struct, hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def derive_key(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, 32)

def encrypt_file(filepath, password):
    if not os.path.exists(filepath):
        print(f"  {RED}[!] File not found.{RESET}")
        return
    try:
        salt = get_random_bytes(16)
        key = derive_key(password, salt)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        with open(filepath, 'rb') as f:
            data = f.read()

        # Pad to 16 bytes
        pad_len = 16 - (len(data) % 16)
        data += bytes([pad_len] * pad_len)
        encrypted = cipher.encrypt(data)

        out_path = filepath + ".ayo"
        with open(out_path, 'wb') as f:
            f.write(salt + iv + encrypted)

        os.remove(filepath)
        size = os.path.getsize(out_path)
        print(f"\n  {GREEN}[+] Encrypted: {out_path}{RESET}")
        print(f"  {GRAY}Size: {size} bytes | Algorithm: AES-256-CBC{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

def decrypt_file(filepath, password):
    if not os.path.exists(filepath):
        print(f"  {RED}[!] File not found.{RESET}")
        return
    if not filepath.endswith(".ayo"):
        print(f"  {YELLOW}[!] Warning: file doesn't have .ayo extension.{RESET}")
    try:
        with open(filepath, 'rb') as f:
            salt = f.read(16)
            iv = f.read(16)
            encrypted = f.read()

        key = derive_key(password, salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted)

        # Remove padding
        pad_len = decrypted[-1]
        if pad_len > 16:
            raise ValueError("Bad padding — wrong password?")
        decrypted = decrypted[:-pad_len]

        out_path = filepath.replace(".ayo", "")
        if os.path.exists(out_path):
            out_path = out_path + ".decrypted"

        with open(out_path, 'wb') as f:
            f.write(decrypted)

        os.remove(filepath)
        print(f"\n  {GREEN}[+] Decrypted: {out_path}{RESET}")
    except ValueError as e:
        print(f"  {RED}[!] Decryption failed: {e}{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

def encrypt_folder(folder, password):
    if not os.path.isdir(folder):
        print(f"  {RED}[!] Folder not found.{RESET}")
        return
    count = 0
    for root, dirs, files in os.walk(folder):
        for fname in files:
            if not fname.endswith(".ayo"):
                fpath = os.path.join(root, fname)
                encrypt_file(fpath, password)
                count += 1
    print(f"\n  {GREEN}[+] Encrypted {count} files.{RESET}")

def run_file_encryptor():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  FILE ENCRYPTOR (AES-256){RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Encrypt a file
  {ACC}[2]{RESET} Decrypt a file
  {ACC}[3]{RESET} Encrypt entire folder
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}Encrypted files get .ayo extension{RESET}""")
        choice = input(f"  {ACC}[encrypt]>{RESET} ").strip().lower()

        if choice == "1":
            fp = input(f"  {GRAY}File path: {RESET}").strip()
            pw = input(f"  {GRAY}Password: {RESET}").strip()
            if fp and pw: encrypt_file(fp, pw)

        elif choice == "2":
            fp = input(f"  {GRAY}File path (.ayo): {RESET}").strip()
            pw = input(f"  {GRAY}Password: {RESET}").strip()
            if fp and pw: decrypt_file(fp, pw)

        elif choice == "3":
            folder = input(f"  {GRAY}Folder path: {RESET}").strip()
            pw = input(f"  {GRAY}Password: {RESET}").strip()
            confirm = input(f"  {YELLOW}Encrypt ALL files in {folder}? (yes/no): {RESET}").strip().lower()
            if confirm == "yes" and folder and pw:
                encrypt_folder(folder, pw)

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
