import sys
from time import sleep
import scapy.all as scapy
from rich.table import Table
from termcolor import colored
from random import uniform as uf
from rich.console import Console
from alive_progress import alive_it

console = Console()


def show_banner():
    banner = """
    ┌─────────────────────────────────┐
    │             👓                  │
    │        Incognito Mode           │
    │  [Enter the target request] 🔍  │
    │  G  H  O  S  T --- S  C  A  N   │
    └─────────────────────────────────┘
    """
    print(colored(banner, "white"))
    print(colored("       [👓] Script mode: ", "light_yellow") + colored("🟢 Base fingerprints", "green"))
    print(colored("       [👓] Function: ", "light_yellow") + colored("Anonymous SYN-scan\n", "red"))


def progressBar(title):
    print(colored(f"[*] {title}...", "yellow"))
    for _ in alive_it(list(range(100))):
        sleep(uf(0.01, 0.07))


def SYN_scan(targetIP, ports=100):
    table = Table()
    table.add_column('№', style="bold cyan")
    table.add_column("Opened ports", style="bold light_green")
    opened_ports = []
    progressBar(f"Starting SYN-scan on target {targetIP}")
    for port in range(ports + 1):
        packet = scapy.IP(dst=targetIP) / scapy.TCP(dport=port, flags="S")
        response = scapy.sr1(packet, timeout=0.5, verbose=0)

        if response and response.haslayer(scapy.TCP):
            flags = response.getlayer(scapy.TCP).flags
            if flags == 0x12:
                table.add_row(str(port))
                opened_ports.append(port)
                scapy.sr1(scapy.IP(dst=targetIP) / scapy.TCP(dport=port, flags='R'), timeout=0.1, verbose=0)
    if opened_ports:
        console.print(table)
        print(colored(f"[+] {len(opened_ports)} ports open!", "green"))
    else:
        print(colored("[-] All port are closed", "red"))

show_banner()
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = input(colored("[*] Enter the target IP: ", "yellow"))
SYN_scan(target)
