import os, struct, json

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def read_exif_jpeg(filepath):
    metadata = {}
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        img = Image.open(filepath)
        exif_data = img._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[str(tag)] = str(value)[:80]
    except ImportError:
        metadata["note"] = "PIL not available — install python-pillow"
    except Exception as e:
        metadata["error"] = str(e)
    return metadata

def clean_jpeg(filepath):
    try:
        from PIL import Image
        img = Image.open(filepath)
        data = list(img.getdata())
        clean = Image.new(img.mode, img.size)
        clean.putdata(data)
        out = filepath.rsplit('.', 1)[0] + "_clean." + filepath.rsplit('.', 1)[-1]
        clean.save(out)
        print(f"  {GREEN}[+] Cleaned image saved: {out}{RESET}")
        return True
    except ImportError:
        print(f"  {RED}[!] PIL not available. Run: pkg install python-pillow{RESET}")
        return False
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")
        return False

def clean_pdf_metadata(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        # Remove common PDF metadata markers
        import re
        content = re.sub(b'/Author\s*\(.*?\)', b'/Author ()', content)
        content = re.sub(b'/Creator\s*\(.*?\)', b'/Creator ()', content)
        content = re.sub(b'/Producer\s*\(.*?\)', b'/Producer ()', content)
        content = re.sub(b'/Title\s*\(.*?\)', b'/Title ()', content)
        content = re.sub(b'/Subject\s*\(.*?\)', b'/Subject ()', content)
        content = re.sub(b'/Keywords\s*\(.*?\)', b'/Keywords ()', content)
        out = filepath.rsplit('.', 1)[0] + "_clean.pdf"
        with open(out, 'wb') as f:
            f.write(content)
        print(f"  {GREEN}[+] Cleaned PDF saved: {out}{RESET}")
    except Exception as e:
        print(f"  {RED}[!] Error: {e}{RESET}")

def show_metadata(filepath):
    ext = filepath.lower().rsplit('.', 1)[-1]
    print(f"\n  {ACC}[*] Metadata for: {filepath}{RESET}\n")

    # Basic file info
    stat = os.stat(filepath)
    print(f"  {GRAY}Size    : {stat.st_size} bytes{RESET}")
    print(f"  {GRAY}Modified: {os.path.getmtime(filepath)}{RESET}")

    if ext in ['jpg', 'jpeg']:
        meta = read_exif_jpeg(filepath)
        if meta:
            print(f"\n  {ACC}EXIF Data:{RESET}")
            for k, v in meta.items():
                print(f"  {GRAY}{k:<25}{RESET}: {v}")
        else:
            print(f"  {YELLOW}[!] No EXIF data found.{RESET}")
    elif ext == 'pdf':
        print(f"  {GRAY}PDF metadata scan...{RESET}")
        try:
            with open(filepath, 'rb') as f:
                content = f.read(4096).decode('latin-1')
            for field in ['/Author', '/Creator', '/Producer', '/Title']:
                idx = content.find(field)
                if idx != -1:
                    snippet = content[idx:idx+60].split(')')[0]
                    print(f"  {GRAY}{field:<15}{RESET}: {snippet}")
        except Exception as e:
            print(f"  {RED}[!] {e}{RESET}")
    else:
        print(f"  {YELLOW}[!] Unsupported type for deep metadata. Basic info shown above.{RESET}")

def run_metadata_cleaner():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  METADATA CLEANER{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} View file metadata
  {ACC}[2]{RESET} Clean image metadata (JPG/PNG)
  {ACC}[3]{RESET} Clean PDF metadata
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}
  {GRAY}Supports: JPG, PNG, PDF{RESET}""")
        choice = input(f"  {ACC}[meta]>{RESET} ").strip().lower()

        if choice == "1":
            fp = input(f"  {GRAY}File path: {RESET}").strip()
            if fp: show_metadata(fp)

        elif choice == "2":
            fp = input(f"  {GRAY}Image path (jpg/png): {RESET}").strip()
            if fp: clean_jpeg(fp)

        elif choice == "3":
            fp = input(f"  {GRAY}PDF path: {RESET}").strip()
            if fp: clean_pdf_metadata(fp)

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
