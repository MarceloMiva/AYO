# ═══════════════════════════════════════════════
#  AYO — Module [3]: Social Engineering Toolkit
# ═══════════════════════════════════════════════

RED   = "\033[91m"
DRED  = "\033[31m"
WHITE = "\033[97m"
GRAY  = "\033[90m"
YELLOW= "\033[93m"
DIM   = "\033[2m"
BOLD  = "\033[1m"
RESET = "\033[0m"

PRETEXTS = {
    "1": {
        "name": "IT Support Call",
        "script": """
  {DRED}── PRETEXT: IT Support Call ──────────────────────{RESET}

  {WHITE}SCENARIO:{RESET}
  You are calling as IT support responding to a "security alert"
  on the target's account.

  {WHITE}OPENER:{RESET}
  "Hi, this is [Name] from the IT Security team. We've detected
  unusual login activity on your account and need to verify your
  identity to prevent a lockout."

  {WHITE}KEY OBJECTIVES:{RESET}
  • Get them to confirm their username
  • Ask them to "verify" their password reset process
  • Request they disable 2FA temporarily for "maintenance"

  {WHITE}HANDLING RESISTANCE:{RESET}
  "I completely understand your concern — you can call our main
  helpdesk number to confirm this ticket is open. The ticket ID
  is [random number]. I'll hold while you verify."

  {WHITE}URGENCY TRIGGERS:{RESET}
  • "Your account will be locked in 15 minutes"
  • "We've already seen 3 failed login attempts"
  • "Your manager has been notified"

  {DRED}⚠ Use only in authorized social engineering assessments.{RESET}
"""
    },
    "2": {
        "name": "Vendor Invoice Scam",
        "script": """
  {DRED}── PRETEXT: Vendor Invoice Scam ──────────────────{RESET}

  {WHITE}SCENARIO:{RESET}
  Email-based pretext targeting accounts payable staff.

  {WHITE}EMAIL TEMPLATE:{RESET}
  Subject: URGENT — Updated Payment Details for Invoice #[NUM]

  "Dear [Name],
  Please note our banking details have changed effective immediately.
  Kindly update your records and process the attached invoice
  (#[NUM], $[AMOUNT]) to our new account:

  Bank: [FAKE BANK]
  Account: [NUMBER]
  Sort Code: [CODE]

  Please confirm receipt of this email.
  Regards, [Vendor Name]"

  {WHITE}SUCCESS INDICATORS:{RESET}
  • Target replies asking for confirmation
  • Target forwards to finance team
  • Target asks for callback number

  {DRED}⚠ For authorized red team & awareness training only.{RESET}
"""
    },
    "3": {
        "name": "Executive Impersonation",
        "script": """
  {DRED}── PRETEXT: Executive Impersonation (CEO Fraud) ──{RESET}

  {WHITE}SCENARIO:{RESET}
  Impersonate a senior executive via email to a junior employee.

  {WHITE}EMAIL TEMPLATE:{RESET}
  Subject: Quick Favor — Confidential

  "Hey [Target],
  I'm in a board meeting right now and can't take calls.
  I need you to process an urgent wire transfer of $[AMOUNT]
  to a new vendor. This is time-sensitive and confidential —
  please don't discuss with anyone until it's done.
  I'll explain everything later. Can you handle this?"

  {WHITE}SOCIAL PRESSURE ELEMENTS:{RESET}
  • Authority (CEO sending directly)
  • Urgency (time-sensitive)
  • Secrecy (don't tell anyone)
  • Flattery (I trust you specifically)

  {DRED}⚠ For authorized awareness training only.{RESET}
"""
    }
}

OSINT_CHECKLIST = """
  {DRED}── OSINT PRE-ENGAGEMENT CHECKLIST ───────────────{RESET}

  {WHITE}TARGET: INDIVIDUAL{RESET}
  {RED}[ ]{RESET} Full name & known aliases
  {RED}[ ]{RESET} LinkedIn profile & job title
  {RED}[ ]{RESET} Email format (firstname.lastname@company.com?)
  {RED}[ ]{RESET} Social media (Twitter/X, Facebook, Instagram)
  {RED}[ ]{RESET} Public photos (for context/building rapport)
  {RED}[ ]{RESET} Phone number (truecaller, pipl)
  {RED}[ ]{RESET} Known colleagues / manager name
  {RED}[ ]{RESET} Recent activity / posts / interests

  {WHITE}TARGET: ORGANIZATION{RESET}
  {RED}[ ]{RESET} Company website & About page
  {RED}[ ]{RESET} Org chart / key personnel
  {RED}[ ]{RESET} Email domain & format
  {RED}[ ]{RESET} Job postings (reveals tech stack)
  {RED}[ ]{RESET} LinkedIn company page
  {RED}[ ]{RESET} News / press releases
  {RED}[ ]{RESET} Vendors & partners (for pretext)
  {RED}[ ]{RESET} Physical locations

  {WHITE}TOOLS:{RESET}
  {GRAY}• theHarvester   — email/domain OSINT
  • Maltego         — relationship mapping
  • Shodan          — exposed infrastructure
  • Hunter.io       — email discovery
  • SpiderFoot      — automated OSINT
  • Google Dorks    — site:company.com filetype:pdf{RESET}
"""

VISHING_GUIDE = """
  {DRED}── VISHING CALL GUIDE ────────────────────────────{RESET}

  {WHITE}BEFORE THE CALL:{RESET}
  • Research target thoroughly (use OSINT checklist)
  • Prepare your pretext story fully
  • Have answers ready for likely questions
  • Spoof number if authorized (carrier-level or app)
  • Record the call (with authorization)

  {WHITE}DURING THE CALL:{RESET}
  • Speak confidently — hesitation = suspicion
  • Use target's name early to build rapport
  • Mirror their tone and pace
  • Create urgency without panic
  • Never break character

  {WHITE}HANDLING OBJECTIONS:{RESET}
  {GRAY}"I need to verify you first"
  → "Of course — what info do you need from me?"

  "I should check with my manager"
  → "Totally fine — do you want me to loop them in now?"

  "Can you send this in writing?"
  → "Already sent — check your inbox, subject line [X]"{RESET}

  {WHITE}AFTER THE CALL:{RESET}
  • Document what worked / what didn't
  • Note any info gathered
  • Include in engagement report

  {DRED}⚠ Only use with written authorization from target org.{RESET}
"""

def se_banner():
    print(f"""
{DRED}╔══════════════════════════════════════════════╗
║    SOCIAL ENGINEERING TOOLKIT — MODULE [3]   ║
╚══════════════════════════════════════════════╝{RESET}
{DIM}Pretexting scripts, vishing guides & OSINT checklists for authorized engagements.{RESET}
""")

def run_social_engineering():
    se_banner()

    while True:
        print(f"  {RED}[1]{RESET} Pretext Scripts")
        print(f"  {RED}[2]{RESET} OSINT Pre-Engagement Checklist")
        print(f"  {RED}[3]{RESET} Vishing Call Guide")
        print(f"  {RED}[b]{RESET} Back\n")

        choice = input(f"  {RED}[se]>{RESET} ").strip().lower()

        if choice == "1":
            print(f"\n  {WHITE}Select pretext:{RESET}")
            for k, v in PRETEXTS.items():
                print(f"  {RED}[{k}]{RESET} {v['name']}")
            print()
            sel = input(f"  {RED}[se]>{RESET} ").strip()
            if sel in PRETEXTS:
                print(PRETEXTS[sel]["script"].format(
                    DRED=DRED, WHITE=WHITE, RED=RED, RESET=RESET, GRAY=GRAY
                ))
            else:
                print(f"  {YELLOW}[!] Invalid option.{RESET}\n")

        elif choice == "2":
            print(OSINT_CHECKLIST.format(
                DRED=DRED, WHITE=WHITE, RED=RED, RESET=RESET, GRAY=GRAY
            ))

        elif choice == "3":
            print(VISHING_GUIDE.format(
                DRED=DRED, WHITE=WHITE, RED=RED, RESET=RESET, GRAY=GRAY
            ))

        elif choice in ["b", "back"]:
            break
        else:
            print(f"  {YELLOW}[!] Invalid option.{RESET}\n")
