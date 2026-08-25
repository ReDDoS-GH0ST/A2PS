import io
import sys
import socket
from rich.table import Table
from termcolor import colored
from rich.console import Console

console = Console()
base_ports = (21, 23, 25, 53, 80, 135, 139, 443, 445, 3389, 8080)

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def show_banner():
    banner = """
         [F]   [I]   [R]   [S]   [T]  ---   [B]  [L]  [O]  [O]  [D]  
         🩸    🩸    🩸    🩸   🩸   🩸    🩸  🩸   🩸   🩸   🩸   
       🩸   🩸    🩸    🩸    🩸   🩸   🩸   🩸   🩸   🩸   🩸   🩸
         🩸    🩸    🩸    🩸   🩸   🩸    🩸  🩸   🩸   🩸   🩸
     --------------------------------------------------------------------
   """
    print(colored(banner, 'red'))
    print(colored("       [🩸] Script mode: ", "light_yellow") + colored("🟢 Base fingerprints", "green"))
    print(colored("       [🩸] Function: ", "light_yellow") + colored(
        "Scan base ports (21-23, 25, 53, 80, 135, 139, 443, 445, 3389, 8080)\n", "red"))


def scan_base_ports(targetIP):
    table = Table()
    table.title = "Base ports scan"
    table.add_column("№", style="cyan")
    table.add_column("Opened ports", style="light_green")

    opened_count = 0
    for id, base_port in enumerate(base_ports, start=1):
        sock = socket.socket()
        sock.settimeout(0.5)
        try:
            sock.connect((targetIP, base_port))
            table.add_row(str(id), str(base_port))
            opened_count += 1
        except:
            pass
        finally:
            sock.close()

    if opened_count > 0:
        console.print(table)

show_banner()
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = input(colored("[*] Enter the target IP: ", "yellow"))
scan_base_ports(target)
