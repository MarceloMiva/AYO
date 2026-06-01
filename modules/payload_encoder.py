import base64, urllib.parse, html, binascii, codecs

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def encode_all(payload):
    results = {}
    b = payload.encode('utf-8')
    results["Base64"]         = base64.b64encode(b).decode()
    results["Base64 URL-safe"]= base64.urlsafe_b64encode(b).decode()
    results["Base32"]         = base64.b32encode(b).decode()
    results["Hex"]            = binascii.hexlify(b).decode()
    results["URL encoded"]    = urllib.parse.quote(payload)
    results["Double URL"]     = urllib.parse.quote(urllib.parse.quote(payload))
    results["HTML entities"]  = html.escape(payload)
    results["ROT13"]          = codecs.encode(payload, 'rot_13')
    results["Binary"]         = ' '.join(format(byte,'08b') for byte in b)
    results["Octal"]          = ' '.join(oct(byte) for byte in b)
    results["Unicode escape"] = payload.encode('unicode_escape').decode()
    results["Reverse"]        = payload[::-1]
    results["XOR key=0x41"]   = ''.join(chr(ord(c)^0x41) for c in payload)
    return results

def decode_base64(data):
    try:
        return base64.b64decode(data).decode('utf-8')
    except:
        try:
            return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception as e:
            return f"Error: {e}"

def decode_hex(data):
    try:
        return bytes.fromhex(data.replace(' ','')).decode('utf-8')
    except Exception as e:
        return f"Error: {e}"

def decode_url(data):
    try:
        return urllib.parse.unquote(data)
    except Exception as e:
        return f"Error: {e}"

def decode_binary(data):
    try:
        bits = data.strip().split()
        return ''.join(chr(int(b, 2)) for b in bits)
    except Exception as e:
        return f"Error: {e}"

def run_payload_encoder():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  PAYLOAD ENCODER/DECODER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Encode payload (all formats)
  {ACC}[2]{RESET} Encode single format
  {ACC}[3]{RESET} Decode payload
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}""")
        choice = input(f"  {ACC}[encode]>{RESET} ").strip().lower()

        if choice == "1":
            payload = input(f"  {GRAY}Enter payload: {RESET}").strip()
            if payload:
                print(f"\n  {ACC}[*] Encodings for: {YELLOW}{payload}{RESET}\n")
                for name, encoded in encode_all(payload).items():
                    print(f"  {GREEN}{name:<18}{RESET}: {encoded}")

        elif choice == "2":
            print(f"""
  {ACC}[1]{RESET} Base64    {ACC}[2]{RESET} Hex
  {ACC}[3]{RESET} URL       {ACC}[4]{RESET} Double URL
  {ACC}[5]{RESET} HTML      {ACC}[6]{RESET} ROT13
  {ACC}[7]{RESET} Binary    {ACC}[8]{RESET} Reverse""")
            fmt = input(f"  {GRAY}Format: {RESET}").strip()
            payload = input(f"  {GRAY}Payload: {RESET}").strip()
            if payload:
                b = payload.encode()
                fmap = {
                    "1": base64.b64encode(b).decode(),
                    "2": binascii.hexlify(b).decode(),
                    "3": urllib.parse.quote(payload),
                    "4": urllib.parse.quote(urllib.parse.quote(payload)),
                    "5": html.escape(payload),
                    "6": codecs.encode(payload,'rot_13'),
                    "7": ' '.join(format(byte,'08b') for byte in b),
                    "8": payload[::-1],
                }
                result = fmap.get(fmt, "Invalid format")
                print(f"\n  {GREEN}[+] Result:{RESET} {result}")

        elif choice == "3":
            print(f"""
  {ACC}[1]{RESET} Base64    {ACC}[2]{RESET} Hex
  {ACC}[3]{RESET} URL       {ACC}[4]{RESET} Binary""")
            fmt = input(f"  {GRAY}Format: {RESET}").strip()
            data = input(f"  {GRAY}Data to decode: {RESET}").strip()
            if data:
                dmap = {
                    "1": decode_base64,
                    "2": decode_hex,
                    "3": decode_url,
                    "4": decode_binary,
                }
                fn = dmap.get(fmt)
                if fn:
                    print(f"\n  {GREEN}[+] Decoded:{RESET} {fn(data)}")
                else:
                    print(f"  {RED}[!] Invalid format.{RESET}")

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
