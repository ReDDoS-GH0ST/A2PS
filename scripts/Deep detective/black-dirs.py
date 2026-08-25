import os
import sys
import requests
from rich.table import Table
from termcolor import colored
from rich.console import Console

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bases.hidden_dirs import black_dirs

console = Console()


def show_banner():
    banner1 = """
    [B] [L] [A] [C] [K] --- [L] [I] [S] [T]
    ---------------------------------------
    """
    banner2 = colored("🗄️ Bustering http://lookatthislink.com...", "yellow")
    banner3 = colored("   [+]  ─────├── come_here", "green")
    banner4 = (colored("    ┌──(", "cyan") + colored("skull㉿shell", "red") + colored(")-[", "cyan") + colored(
        "root/kali/Desktop", "white") + colored(']', "cyan"))
    banner5 = colored("    └─", "cyan") + colored('#', "red") + colored(" firefox", "blue") + colored(
        " http://lookatthislink.com/come_here", "white")
    banner6 = colored("If you want to get the flag, think one more time ;p")
    print(banner1)
    print(banner2)
    print(banner3)
    print(banner4)
    print(banner5)
    print(banner6)
    print(colored("    [🗄️] Script mode: ", "light_yellow") + colored("🟡 Deep detective", "yellow"))
    print(colored("    [🗄️] Function: ", "light_yellow") + colored("Scan hidden directories & files\n", "red"))


def link_buster(link):
    table = Table()
    table.title = f"Hidden dirs on {link}"
    table.add_column("№", style="cyan")
    table.add_column("Dir", style="green")
    table.add_column("Status code", style="yellow")

    found_count = 0
    print(colored(f"[*] Bustering {link}...", "yellow"))

    for dir in black_dirs:
        try:
            response = requests.get(f"{link}/{dir}", timeout=2)
            code = response.status_code
            if code in [200, 301, 302, 403]:
                found_count += 1
                table.add_row(str(found_count), dir, str(code))
        except:
            pass

    if found_count > 0:
        console.print(table)
        print(colored(f"[+] {found_count} hidden dirs found!", "green"))
    else:
        print(colored("[-] No hidden directories found", "red"))


show_banner()
if len(sys.argv) > 1:
    link = sys.argv[1]
else:
    link = input(colored("[*] Enter the target link: ", "yellow"))
link_buster(link)
