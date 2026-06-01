import os, itertools, random, string

GREEN = "\033[92m"; CYAN = "\033[96m"; YELLOW = "\033[93m"
RED = "\033[91m"; GRAY = "\033[90m"; RESET = "\033[0m"
BOLD = "\033[1m"; ACC = CYAN; BORDER = GREEN

def keyword_wordlist(keywords, output_file):
    words = set()
    leet = {'a':'4','e':'3','i':'1','o':'0','s':'5','t':'7'}
    years = [str(y) for y in range(1990, 2026)]
    specials = ['!','@','#','$','123','1234','!@#']

    for kw in keywords:
        kw = kw.strip()
        words.add(kw)
        words.add(kw.lower())
        words.add(kw.upper())
        words.add(kw.capitalize())
        # leet speak
        leet_kw = kw.lower()
        for k,v in leet.items():
            leet_kw = leet_kw.replace(k, v)
        words.add(leet_kw)
        # with years
        for y in years:
            words.add(kw + y)
            words.add(kw.lower() + y)
        # with specials
        for s in specials:
            words.add(kw + s)
            words.add(kw.lower() + s)
            words.add(s + kw)
        # combinations of keywords
    for combo in itertools.permutations(keywords, 2):
        words.add(''.join(combo))
        words.add('_'.join(combo))
        words.add('.'.join(combo))

    with open(output_file, 'w') as f:
        for w in sorted(words):
            f.write(w + '\n')
    print(f"\n  {GREEN}[+] Generated {len(words)} words → {output_file}{RESET}")

def bruteforce_wordlist(charset, min_len, max_len, output_file):
    count = 0
    print(f"  {ACC}[*] Generating combinations...{RESET}")
    with open(output_file, 'w') as f:
        for length in range(min_len, max_len + 1):
            for combo in itertools.product(charset, repeat=length):
                f.write(''.join(combo) + '\n')
                count += 1
                if count % 10000 == 0:
                    print(f"  {GRAY}[...] {count} words written{RESET}", end="\r")
    print(f"\n  {GREEN}[+] Generated {count} combinations → {output_file}{RESET}")

def run_wordlist_gen():
    while True:
        print(f"""
{BORDER}{'─'*45}{RESET}
{ACC}{BOLD}  WORDLIST GENERATOR{RESET}
{BORDER}{'─'*45}{RESET}
  {ACC}[1]{RESET} Keyword-based wordlist
  {ACC}[2]{RESET} Brute-force combinations
  {ACC}[b]{RESET} Back
{BORDER}{'─'*45}{RESET}""")
        choice = input(f"  {ACC}[wordlist]>{RESET} ").strip().lower()

        if choice == "1":
            kw = input(f"  {GRAY}Enter keywords (comma separated): {RESET}").strip()
            out = input(f"  {GRAY}Output file (e.g. custom.txt): {RESET}").strip()
            if kw and out:
                keyword_wordlist([k.strip() for k in kw.split(',')], out)

        elif choice == "2":
            print(f"  {GRAY}Charsets: [1] lowercase [2] digits [3] lower+digits [4] custom{RESET}")
            cs = input(f"  {GRAY}Choice: {RESET}").strip()
            charsets = {
                "1": string.ascii_lowercase,
                "2": string.digits,
                "3": string.ascii_lowercase + string.digits,
            }
            if cs == "4":
                charset = input(f"  {GRAY}Enter custom chars: {RESET}").strip()
            else:
                charset = charsets.get(cs, string.ascii_lowercase)
            try:
                min_l = int(input(f"  {GRAY}Min length: {RESET}").strip())
                max_l = int(input(f"  {GRAY}Max length: {RESET}").strip())
                out = input(f"  {GRAY}Output file: {RESET}").strip()
                if max_l > 4:
                    print(f"  {YELLOW}[!] Warning: large combinations may take long.{RESET}")
                bruteforce_wordlist(charset, min_l, max_l, out)
            except ValueError:
                print(f"  {RED}[!] Invalid length input.{RESET}")

        elif choice == "b":
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}")
        input(f"\n  {GRAY}Press Enter to continue...{RESET}")
