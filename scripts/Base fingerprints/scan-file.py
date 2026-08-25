import os
import sys
import socket
from time import sleep
from rich.table import Table
from termcolor import colored
from rich.console import Console
from random import uniform as uf
from alive_progress import alive_it

targets = []
console = Console()


def progressBar(title):
    print(colored(f"[*] {title}...", "yellow"))
    for _ in alive_it(list(range(100))):
        sleep(uf(0.01, 0.06))


def show_banner():
    banner = """
    --------------------===== 📃 S  C  A  N --- F  I  L  E 📃 =====--------------------
    💻: Hey!<═══>🖥️: What?<═══>💻: May I scan your ports? You just in my hosts list)<═══>🖥️: Okay?...
    """
    print(colored(banner, "white"))
    print(colored("       [📃] Script mode: ", "light_yellow") + colored("🟢 Base fingerprints", "green"))
    print(colored("       [📃] Function: ", "light_yellow") + colored(
        "Scan targets from file (specify path to file)\n", "red"))


def scan_target(IP, ports=1000):
    table = Table()
    table.add_column("№", style="cyan")
    table.add_column("Opened ports", style="light_green")

    def scan_port(IP, port):
        sock = socket.socket()
        sock.settimeout(0.0002)
        try:
            sock.connect((IP, port))
            table.add_row(str(port))
        except:
            pass
        finally:
            sock.close()

    for id, port in range(1, ports + 1):
        scan_port(IP, port)

    if table.rows:
        console.print(table)
    else:
        print(colored("[-] All ports are closed", "red"))


def scan_file(path):
    if not os.path.isabs(path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file = os.path.join(script_dir, path)
    else:
        file = path
    with open(file, "r") as tars_file:
        for target in tars_file:
            target = target.strip()
            if '.' in target:
                targets.append(target)

    if not targets:
        print(colored("[-] No targets found in file", "red"))
        return

    for target in targets:
        progressBar(f"Scanning the target {target}")
        scan_target(target)


show_banner()

if len(sys.argv) > 1:
    path = sys.argv[1]
    if not os.path.isfile(path):
        path = input(colored("[*] Enter the path to file with targets: ", "yellow"))
else:
    path = input(colored("[*] Enter the path to file with targets: ", "yellow"))

if not os.path.isabs(path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, path)

if not os.path.isfile(path):
    print(colored(f"[-] File not found: {path}", "red"))
    sys.exit(1)

scan_file(path)
