import os
import sys
from time import sleep
from rich.box import ROUNDED
from impacket.smbconnection import SMBConnection
from rich.table import Table
from termcolor import colored
from rich.console import Console

console = Console()

def show_banner():
    banner1 = """
                📂 S  M  B --- E  N  U  M 📂
        To get your CTF-flag just enumerate SMB shares,
        then take share name and append it step 2 step)
    """
    banner2 = (colored("    ┌──(", "cyan") + colored("root㉿kali", "red") + colored(")-[", "cyan") + colored(
        "root/kali/Desktop", "white") + colored(']', "cyan"))
    banner3 = colored("    └─", "cyan") + colored('#', "red") + colored(" smbenum", "blue") + colored(" 192.168.1.111", "white")
    banner4 = colored("    [*] Enumerating SMB shares of 192.168.1.1...", "yellow")
    banner5 = colored("""
     📂) [y0ur_
     📂) fl@g_
     📂) 1s)
     📂) 7h1s(
     📂) t3xt{
     📂) :p}]
    """, "cyan")
    print(banner1)
    print(banner2)
    print(banner3)
    print(banner4)
    print(banner5)
    print(colored("    [📂] Script mode: ", "light_yellow") + colored("🟡 Deep detective", "yellow"))
    print(colored("    [📂] Function: ", "light_yellow") + colored("SMB shares enumeration\n", "red"))

def shares_enumerate(targetIP):
    table = Table(box=ROUNDED, border_style="bold red")
    table.title = "SMB shares"
    table.add_column("№")
    table.add_column("Share")
    print(colored(f"[*] Connecting to {targetIP}...", "yellow"))
    sleep(1)
    try:
        smb = SMBConnection(targetIP, targetIP)
        print(colored("[+] Connected!", "green"))
        sleep(0.5)
        print(colored("[*] Logining to SMB...", "yellow"))
        try:
            smb.login('', '')
            print(colored(f"[+] Enumerating shares of {targetIP}...", "light_yellow"))
            shares = smb.listShares()
            for id, share in enumerate(shares, start=1):
                table.add_row(str(id), share["shi1_netname"])
            print(colored(f"[+] {len(shares)} shares found!", "green") if len(shares) > 1 else colored("1 share found!", "green"))
            console.print(table)
            return True
        except:
            print(colored("[-] Failed to login (anonymous access denied)", "red"))
            return False
    except:
        return False

show_banner()
if len(sys.argv) > 1:
    targetIP = sys.argv[1]
else:
    targetIP = input(colored("[*] Enter the target IP: ", "yellow"))
result = shares_enumerate(targetIP)
if result:
    print(colored("[+] SMB shares enumerating was finished successfully!", "green"))
else:
    print(colored("[-] Failed to enumerate smb shares", "red"))

