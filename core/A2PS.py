# A2PS (APPS) - Advanced Powerful Pentest Suite. Nmap scanner, MSF Spirit
import os
import sys
import socket
import platform
import subprocess
import threading
import warnings
from queue import Queue

warnings.filterwarnings("ignore")
import scapy.all as scapy
from time import time, sleep
from rich.table import Table
from termcolor import colored
from rich.console import Console
from random import uniform as uf
from alive_progress import alive_it

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bases.MAC_vendors import mac_vendors

os_system = platform.system()
table = Table()
console = Console()
commands = {
    "scanp": "Scan open ports",
    "showtar": "Scan the network and get available targets",
    "showscr": "Show available scripts",
    "a2pee": "Use A2PS Exploits Engine",
    "a2set": "Use A2PS Social Engineering Toolkit",
    "a2crypt": "Use A2PS Cryptography Engine",
    "restart": "Restart A2PS",
    "help": "Print the usage documentation",
    "doc": "Print the usage documentation",
    "clear": "Clear the screen",
    "banner": "Show banner",
    "quit": "Exit the program",
    "exit": "Exit the program"
}
arguments = {
    "-p=": "Scan define port",
    "--script=": "Use script",
    "--plugin=": "Use plugin",
    "-sV": "Scan service and version",
    "-vb": "Verbose process",
    "--version": "Show A2PS version"
}
scripts = {
    "🟢 Base fingerprints": {
        "🩸 first-blood": "Scan the base ports (21-23, 25, 53, 80, 135, 139, 443, 445, 3389, 8080)",
        "⚡ pulse-host": "Check is host alive (ICMP ping)",
        "👓 ghost-scan": "Anonymous SYN-scan",
        "📄 case-file": "Save scan in file",
        "📃 scan-file": "Scan targets.txt from file (specify path to file)",
        "🔍 recon-scan": "Get all available target's information",
    },
    "🟡 Deep detective": {
        "🎯 vuln-hunt": "Check for common vulnerabilities",
        "📂 smb-enum": "SMB shares enumeration",
        "📋 whois-secrets": "Gather WHOIS data",
        "🗄️ black-dirs": "Scan hidden directories & files",
        "🌐 git-exposed": "Check for having .git repos",
        "📊 report-view": "TUI dashboard for scan results (specify path to file with report)",
        "🌊 oscillo-waves": "Visualize ports as oscilloscope waves",
        "🛡️ firewall-observe": "Detect firewall"
    },
    "🔴 Red SWAT": {
        "🪲 xss-bug": "Set XSS-payload & bug the target",
        "🔓 brute-force": "Launch brute force on target open ports",
        "🔐 hash-crack": "Crack hash",
        "💀 skull-shell": "Use bind-shell",
        "☢️ dos-time": "Launch DoS attack",
        "💉 sql-injector": "Scan & use SQL-Injection",
        "⚒️ payload-forge": "Generate payload",
        "🕸️ arp-spoof": "Launch MITM-attack",
        "📻 traffic-sniff": "Intercept full traffic"
    }
}


class PortScanner:

    def progressBar(self, title):
        print(colored(f"[*] {title}...", "yellow"))
        for _ in alive_it(list(range(100))):
            sleep(uf(0.01, 0.07))

    def greeting_animation(self,
                           text=colored("Starting the Advanced Powerful Pentest Suite...................", "yellow"),
                           delay=0.05):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            sleep(delay)

        sleep(1.6)
        sys.stdout.write('\r')
        sys.stdout.write(' ' * len(text))
        sys.stdout.write('\r')
        sys.stdout.write(text + colored("Done\n", "yellow"))
        sys.stdout.flush()
        sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        sleep(1)

        print(colored("""
 █████╗  ██████╗  ██████╗  ███████╗
██╔══██╗ ╚════██╗ ██╔══██╗ ██╔════╝
███████║  █████╔╝ ██████╔╝ ███████╗
██╔══██║ ██╔═══╝  ██╔═══╝  ╚════██║
██║  ██║ ███████╗ ██║      ███████║
╚═╝  ╚═╝ ╚══════╝ ╚═╝      ╚══════╝
                                   by R3DDoS_GH0$T""", "red"))

    def get_ports_value(self, parg):
        if parg == "all":
            return list(range(1, 65536))
        elif '-' in str(parg):
            from_, to = parg.split('-')
            return list(range(int(from_), int(to) + 1))
        else:
            return [int(parg)]

    def scan_ports(self, targetIP, ports=65535, verbose=False, sV=False):
        self.progressBar("Scanning ports")
        table = Table()
        table.add_column("Opened ports", style="cyan")
        if sV:
            table.add_column("Service", style="light_green")

        queue = Queue()
        ports_value = self.get_ports_value(ports)
        tlock = threading.Lock()

        for port in ports_value:
            queue.put(port)

        def get_service_banner(targetIP, port, sock):
            service = ''
            try:
                sock.settimeout(2)
                if port in [80, 443, 8080, 8443]:
                    sock.send(b"HEAD / HTTP/1.0\r\nHost: " + targetIP.encode() + b"\r\n\r\n")
                    response = sock.recv(4096).decode("utf-8", errors="ignore")
                    for line in response.split("\n"):
                        if line.lower().startswith("server:"):
                            service = line.strip()
                            break
                else:
                    sock.setblocking(True)
                    banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
                    if banner:
                        service = banner.split("\n")[0][:80]
            except:
                service = "Undefined"

            if not service:
                service = "Undefined"

            with tlock:
                table.add_row(str(port), service)

        def scan_port():
            while not queue.empty():
                port = queue.get()
                sock = socket.socket()
                try:
                    sock.settimeout(0.007)
                    sock.connect((targetIP, port))
                    if verbose:
                        print(colored(f"[+] Port {port} is opened!", "green"))
                    if sV:
                        get_service_banner(targetIP, port, sock)
                    else:
                        with tlock:
                            table.add_row(str(port))
                except:
                    if verbose:
                        print(colored(f"[-] Port {port} is closed", "red"))
                finally:
                    sock.close()
                    queue.task_done()
        threads = []
        for _ in range(556):
            thread = threading.Thread(target=scan_port)
            thread.start()
            threads.append(thread)

        for thr in threads:
            thr.join()

        if table.rows:
            console.print(table)
        else:
            print(colored("[-] Ports are closed or filtered", "red"))
        print(colored("[+] Scanning was finished successfully!", "green"))

    def get_available_targets(self, verbose=False):
        routers = {
            "192.168.1.1": "Router",
            "192.168.0.1": "Router",
            "10.0.0.1": "Router",
            "172.16.0.1": "Router",
            "255.255.255.255": "Broadcast",
        }

        self.progressBar("Scanning available targets")
        target_networks = ["192.168.0.1/24", "10.0.0.0/24", "192.168.1.1/24", "192.168.31.0/24", "172.16.0.0/24"]

        table = Table()
        table.add_column("№", style="cyan")
        table.add_column("Device name", style="green")
        table.add_column("IP Address", style="yellow")

        if verbose:
            table.add_column("MAC Address", style="magenta")
            table.add_column("Vendor", style="white")
            table.add_column("First Seen", style="yellow")

        devices = []

        if verbose:
            print(colored("[*] Generating packets...", "yellow"))
            sleep(1)
            print(colored("[*] Sending ARP requests...", "yellow"))

        for network in target_networks:
            start = time()
            arp_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(op=1, pdst=network)
            answered, unanswered = scapy.srp(arp_request, timeout=0.01, verbose=0)
            if answered:
                for sent, received in answered:
                    IP = received.psrc
                    MAC = received.hwsrc

                    if IP in routers:
                        hostname = routers[IP]
                    else:
                        try:
                            hostname = socket.gethostbyaddr(IP)[0]
                        except:
                            hostname = "Unknown"

                    if verbose:
                        response_time = f"{(time() - start) * 1000:.1f}ms"
                        OUI = MAC[:8].upper()
                        MAC_vendor = mac_vendors.get(OUI, "Unknown")

                        print(colored(f"[+] 1 packet got from {IP} — {response_time}", "green"))
                        devices.append({
                            "Device name": hostname,
                            "IP": IP,
                            "MAC": MAC,
                            "Vendor": MAC_vendor,
                            "First Seen": response_time
                        })
                    else:
                        devices.append({
                            "Device name": hostname,
                            "IP": IP
                        })

        if devices:
            for id, device in enumerate(devices, start=1):
                if verbose:
                    table.add_row(
                        str(id),
                        device["Device name"],
                        device["IP"],
                        device["MAC"],
                        device["Vendor"],
                        device["First Seen"]
                    )
                else:
                    table.add_row(
                        str(id),
                        device["Device name"],
                        device["IP"]
                    )

            print(colored(f"[+] {len(devices)} devices found!", "green"))
            console.print(table)
        else:
            print(colored("[-] No devices found", "red"))

    def launch_script(self, script, targetIP=None):
        print(colored(f"[*] Searching for script {script}...", "yellow"))
        for categ, scripts_list in scripts.items():
            for key in scripts_list:
                if script in key:
                    print(colored(f"[+] Script {script} was found!", "green"))
                    sleep(0.7)
                    print(colored(f"[*] Launching the script {script}...", "yellow"))

                    categ_formated = categ.split(" ", 1)[1] if " " in categ else categ
                    script_formated = key.split(" ", 1)[1] if " " in key else key

                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    path = os.path.join(base_dir, "..", "scripts", categ_formated, f"{script_formated}.py")

                    cmd = ["python", path]
                    if targetIP:
                        cmd.append(targetIP)
                    try:
                        print(colored(f"[+] Script {script} was launched!", "green"))
                        subprocess.run(cmd, text=True, encoding='utf-8', errors='replace')
                    except subprocess.SubprocessError as e:
                        print(colored(f"[-] Script error: {e}", "red"))
                    return
        print(colored(f"[-] Script {script} wasn't found", "red"))

    def launch_plugin(self, plugin, targetIP=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "..", "plugins", f"{plugin}.py")

        if not os.path.exists(path):
            print(colored(f"[-] Plugin {plugin} wasn't found", "red"))
            return

        print(colored(f"[*] Launching plugin {plugin}...", "yellow"))

        cmd = ["python", path]
        if targetIP:
            cmd.append(targetIP)

        try:
            subprocess.run(cmd, text=True, encoding='utf-8', errors='replace')
            print(colored(f"[+] Plugin {plugin} was launched!", "green"))
        except subprocess.SubprocessError as e:
            print(colored(f"[-] Error: {e}", "red"))

    def restart(self):
        print(colored("[*] Restarting A2PS...", "yellow"))
        sleep(1)
        os.system("cls" if os.name == "nt" else "clear")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "A2PS.py")
        subprocess.run([sys.executable, script_path])
        sys.exit(0)

    def check_admin(self):
        if os_system == 'Windows':
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            return os.geteuid() == 0


portScanner = PortScanner()
portScanner.greeting_animation()


def main():
    while True:
        try:
            if not portScanner.check_admin():
                command = input(colored("[A][2][P][S]:~$ ", "cyan"))
            else:
                command = input(colored("[A][2][P][S]:~# ", "light_red"))
            if command.startswith("scanp"):
                parts = command.split()[1:]
                if "-h" in parts:
                    from documentation import showScanpDoc
                    showScanpDoc()
                    continue

                targetIP = None
                port = None
                hash = None
                verbose = "-vb" in command
                sV = "-sV" in command
                noIPscripts = ("payload-forge", "case-file", "hash-crack", "scan-file", "whois-secrets", "black-dirs",
                               "git-exposed", "report-view")

                for part in parts:
                    if part.startswith(("-p=", "-h", "-sV", "--script=", "-vb", "--plugin=")):
                        continue
                    if '.' in part:
                        targetIP = part
                    elif len(part) >= 32:
                        hash = part
                if "-p=" in command:
                    port = command.split("-p=")[1].split()[0]
                if "--script=hash-crack" in command:
                    if not hash:
                        hash = input(colored("[*] Enter the hash: ", "yellow"))
                    targetIP = hash
                elif not any(scr in command for scr in noIPscripts):
                    if not targetIP:
                        targetIP = input(colored("[*] Enter the target IP: ", "yellow"))

                if "--script=" in command:
                    if any(scr in command for scr in noIPscripts):
                        port = "skip"
                    elif not port:
                        port = input(colored("[*] Enter the ports range: ", "yellow"))
                else:
                    if not port:
                        port = input(colored("[*] Enter the ports range: ", "yellow"))

                if port != "skip":
                    if port == "all" or "-p=all" in command:
                        portScanner.scan_ports(targetIP, "all", verbose=verbose, sV=sV)
                    else:
                        portScanner.scan_ports(targetIP, port, verbose=verbose, sV=sV)

                if "--script=" in command:
                    scripts_list = []
                    parts = command.split()
                    for part in parts:
                        if part.startswith("--script="):
                            script = part.split('=', 1)[1]
                            scripts_list.append(script)
                    for script in scripts_list:
                        sleep(1)
                        try:
                            portScanner.launch_script(script, targetIP)
                        except:
                            print(colored("[-] Script wasn't found or unknown script was entered", "red"))
                if "--plugin=" in command:
                    plugin = command.split("--plugin=")[1].split()[0]
                    portScanner.launch_plugin(plugin, targetIP)
            elif command.startswith("showtar"):
                if "-h" in command:
                    from documentation import showShowtarDoc
                    showShowtarDoc()
                    continue
                elif "-vb" in command:
                    portScanner.get_available_targets(verbose=True)
                else:
                    portScanner.get_available_targets()

            elif command == "showscr":
                import documentation
                documentation.showScripts()

            elif command.startswith("a2pee"):
                if "-h" in command:
                    from documentation import showA2peeDoc
                    showA2peeDoc()
                    continue

            elif command.startswith("a2set"):
                if "-h" in command:
                    from documentation import showA2setDoc
                    showA2setDoc()
                    continue

            elif command.startswith("a2crypt"):
                if "-h" in command:
                    from documentation import showA2setDoc
                    showA2setDoc()
                    continue

            elif command == "restart":
                portScanner.restart()

            elif command == "--version":
                print(colored("A2PS v1.0", "light_yellow"))
                print(colored("Nmap scanner, MSF spirit"))

            elif command in ["help", "doc"]:
                from documentation import showA2setDoc, showA2peeDoc, showGeneralDoc, showScanpDoc, showShowtarDoc, \
                    showScripts
                showGeneralDoc()
                showScanpDoc()
                showShowtarDoc()
                showA2peeDoc()
                showA2setDoc()
                showScripts()
                print(colored("To use A2PS just write a command, as well as arguments and/or scripts if necessary",
                              "white"))
            elif command == "clear":
                os.system("cls" if os_system == "Windows" else "clear")
            elif command == "banner":
                print(colored("""
 █████╗  ██████╗  ██████╗  ███████╗
██╔══██╗ ╚════██╗ ██╔══██╗ ██╔════╝
███████║  █████╔╝ ██████╔╝ ███████╗
██╔══██║ ██╔═══╝  ██╔═══╝  ╚════██║
██║  ██║ ███████╗ ██║      ███████║
╚═╝  ╚═╝ ╚══════╝ ╚═╝      ╚══════╝
                                   by R3DDoS_GH0$T""", "red"))
            elif command in ["quit", "exit"]:
                sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)


main()
