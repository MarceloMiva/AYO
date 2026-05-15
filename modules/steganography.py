# ═══════════════════════════════════════════
#  AYO — Module [2]: Steganography Suite
# ═══════════════════════════════════════════

RED   = "\033[91m"
DRED  = "\033[31m"
WHITE = "\033[97m"
GRAY  = "\033[90m"
YELLOW= "\033[93m"
DIM   = "\033[2m"
RESET = "\033[0m"

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def stego_banner():
    print(f"""
{DRED}╔══════════════════════════════════════════════╗
║        STEGANOGRAPHY SUITE — MODULE [2]      ║
╚══════════════════════════════════════════════╝{RESET}
{DIM}Hide and extract secret data inside image files using LSB encoding.{RESET}
""")

# ── LSB Hide ────────────────────────────────
def hide_message(image_path, message, output_path):
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())

    message += "<<END>>"
    bits = ''.join(format(ord(c), '08b') for c in message)

    if len(bits) > len(pixels) * 3:
        print(f"  {YELLOW}[!] Message too long for this image.{RESET}")
        return False

    new_pixels = []
    bit_idx = 0

    for pixel in pixels:
        r, g, b = pixel
        if bit_idx < len(bits):
            r = (r & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            g = (g & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < len(bits):
            b = (b & ~1) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((r, g, b))

    out_img = Image.new("RGB", img.size)
    out_img.putdata(new_pixels)
    out_img.save(output_path)
    return True

# ── LSB Extract ─────────────────────────────
def extract_message(image_path):
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())

    bits = []
    for pixel in pixels:
        for channel in pixel:
            bits.append(str(channel & 1))

    chars = []
    for i in range(0, len(bits), 8):
        byte = ''.join(bits[i:i+8])
        if len(byte) < 8:
            break
        char = chr(int(byte, 2))
        chars.append(char)
        msg_so_far = ''.join(chars)
        if msg_so_far.endswith("<<END>>"):
            return msg_so_far[:-7]

    return None

# ── Text-only stego (no PIL) ─────────────────
def text_stego_hide(cover_text, secret, output_file):
    """Hide secret in whitespace — zero-width chars"""
    ZWS = "\u200b"  # zero-width space = 0
    ZWJ = "\u200d"  # zero-width joiner = 1

    bits = ''.join(format(ord(c), '08b') for c in secret + "<<END>>")
    encoded = ''.join(ZWJ if b == '1' else ZWS for b in bits)

    words = cover_text.split(' ')
    result = words[0] + encoded + ' ' + ' '.join(words[1:])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    return True

def text_stego_extract(input_file):
    ZWS = "\u200b"
    ZWJ = "\u200d"
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    bits = ''
    for ch in content:
        if ch == ZWJ:   bits += '1'
        elif ch == ZWS: bits += '0'

    if not bits:
        return None

    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) < 8: break
        chars.append(chr(int(byte, 2)))
        if ''.join(chars).endswith("<<END>>"):
            return ''.join(chars)[:-7]
    return None

def run_steganography():
    stego_banner()

    if not PIL_AVAILABLE:
        print(f"  {YELLOW}[!] Pillow not installed. Image stego unavailable.{RESET}")
        print(f"  {DIM}Install with: pip install Pillow{RESET}\n")
        print(f"  {WHITE}Text-based steganography is still available (zero-width chars).{RESET}\n")

    while True:
        print(f"  {WHITE}IMAGE STEGANOGRAPHY (requires Pillow){RESET}")
        print(f"  {RED}[1]{RESET} Hide message in image (LSB)")
        print(f"  {RED}[2]{RESET} Extract message from image")
        print(f"\n  {WHITE}TEXT STEGANOGRAPHY (no dependencies){RESET}")
        print(f"  {RED}[3]{RESET} Hide message in text file (zero-width chars)")
        print(f"  {RED}[4]{RESET} Extract message from text file")
        print(f"\n  {RED}[b]{RESET} Back\n")

        choice = input(f"  {RED}[stego]>{RESET} ").strip().lower()

        if choice == "1":
            if not PIL_AVAILABLE:
                print(f"  {YELLOW}[!] Install Pillow first: pip install Pillow{RESET}\n")
                continue
            img_path = input(f"  {RED}[stego]>{RESET} Image path (PNG recommended): ").strip()
            message  = input(f"  {RED}[stego]>{RESET} Secret message: ").strip()
            out_path = input(f"  {RED}[stego]>{RESET} Output image path (e.g. output.png): ").strip()
            try:
                if hide_message(img_path, message, out_path):
                    print(f"  {RED}[+] Message hidden → {out_path}{RESET}\n")
            except FileNotFoundError:
                print(f"  {YELLOW}[!] Image file not found.{RESET}\n")
            except Exception as e:
                print(f"  {YELLOW}[!] Error: {e}{RESET}\n")

        elif choice == "2":
            if not PIL_AVAILABLE:
                print(f"  {YELLOW}[!] Install Pillow first: pip install Pillow{RESET}\n")
                continue
            img_path = input(f"  {RED}[stego]>{RESET} Image path: ").strip()
            try:
                msg = extract_message(img_path)
                if msg:
                    print(f"\n  {RED}[+] Hidden message found:{RESET}")
                    print(f"  {WHITE}{msg}{RESET}\n")
                else:
                    print(f"  {YELLOW}[!] No hidden message found.{RESET}\n")
            except FileNotFoundError:
                print(f"  {YELLOW}[!] Image file not found.{RESET}\n")
            except Exception as e:
                print(f"  {YELLOW}[!] Error: {e}{RESET}\n")

        elif choice == "3":
            cover = input(f"  {RED}[stego]>{RESET} Cover text (the visible message): ").strip()
            secret = input(f"  {RED}[stego]>{RESET} Secret message to hide: ").strip()
            out_file = input(f"  {RED}[stego]>{RESET} Output filename (e.g. message.txt): ").strip()
            try:
                text_stego_hide(cover, secret, out_file)
                print(f"  {RED}[+] Secret embedded → {out_file}{RESET}\n")
                print(f"  {DIM}The file looks like normal text but carries hidden data.{RESET}\n")
            except Exception as e:
                print(f"  {YELLOW}[!] Error: {e}{RESET}\n")

        elif choice == "4":
            in_file = input(f"  {RED}[stego]>{RESET} File to extract from: ").strip()
            try:
                msg = text_stego_extract(in_file)
                if msg:
                    print(f"\n  {RED}[+] Hidden message:{RESET}")
                    print(f"  {WHITE}{msg}{RESET}\n")
                else:
                    print(f"  {YELLOW}[!] No hidden message found.{RESET}\n")
            except FileNotFoundError:
                print(f"  {YELLOW}[!] File not found.{RESET}\n")
            except Exception as e:
                print(f"  {YELLOW}[!] Error: {e}{RESET}\n")

        elif choice in ["b", "back"]:
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}\n")
