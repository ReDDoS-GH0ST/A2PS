import io
import platform
import sys
import subprocess
from time import sleep
from termcolor import colored
from rich.console import Console

console = Console()

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def show_banner():
    banner = """
            ⚡ P  U  L  S  E --- H  O  S  T ⚡
     💻: Hey, James!<═══>🖥️: What?<═══>💻: Are you alive?<═══>🖥️: Of course!)
    """
    print(colored(banner, "light_yellow"))
    print(colored("       [⚡] Script mode: ", "light_yellow") + colored("🟢 Base fingerprints", "green"))
    print(colored("       [⚡] Function: ", "light_yellow") + colored(
        "Check is host alive (ICMP ping)\n", "red"))

def ping_host(host):
    print(colored(f"[*] Pinging the host {host}...", "yellow"))
    sleep(0.7)
    packs_count = "-n" if platform.system() == "Windows" else "-c"
    try:
        ping = subprocess.run(["ping", packs_count, '1', host], capture_output=True, text=True, timeout=2.5)
        if ping.returncode == 0:
            print(colored("[+] Host is ALIVE!", "green"))
        else:
            print(colored("[-] Host is down", "red"))
    except subprocess.TimeoutExpired:
        print(colored("[-] Host is down - timeout", "red"))
    except:
        print(colored("[-] Host is down", "red"))



show_banner()
if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = input(colored("[*] Enter the target IP: ", "yellow"))
ping_host(host)
