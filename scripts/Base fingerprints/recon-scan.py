import os
import sys
import socket
import requests
import subprocess
from time import sleep

import warnings
warnings.filterwarnings("ignore")

import scapy.all as scapy
from rich.table import Table
from termcolor import colored
from rich.console import Console

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bases.MAC_vendors import mac_vendors

console = Console()
common_services = {
            20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPCBind", 135: "MS-RPC",
            139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS",
            995: "POP3S", 1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            5900: "VNC", 8080: "HTTP-Alt",
        }


def show_banner():
    banner = """
                        🔍 R  E  C  O  N --- S  C  A  N 🔎
       💻: Hey!<═══>🖥️: What?<═══>💻: Send me all available info about You, it's checking.
        I'm finding the hacker, who is asking everyone info about them<═
        ══>🖥️: Okay?...<═══>💻: Thank You!)<═══>🖥️:💀...
    """
    print(banner)
    print(colored("       [🔍] Script mode: ", "light_yellow") + colored("🟢 Base fingerprints", "green"))
    print(colored("       [🔍] Function: ", "light_yellow") + colored("Get all available target's information\n", "red"))


def getMAC(targetIP):
    arp_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(op=1, pdst=targetIP)
    answered, unanswered = scapy.srp(arp_request, timeout=2, verbose=0)

    if answered:
        return answered[0][1].hwsrc
    else:
        return None


def getGeoIP(targetIP):
    try:
        response = requests.get(f"http://ip-api.com/json/{targetIP}", timeout=5)
        data = response.json()
        if data.get("status") == "success":
            return {
                "country": data.get("country"),
                "city": data.get("city"),
                "provider": data.get("isp"),
            }
    except:
        pass

    try:
        response = requests.get(f"https://ipinfo.io/{targetIP}/json", timeout=5)
        data = response.json()
        return {
            "country": data.get("country"),
            "city": data.get("city"),
            "provider": data.get("org"),
        }
    except:
        return None


def get_opened_ports(targetIP, ports=1000):
    opened_ports = []
    sock = socket.socket()
    sock.settimeout(0.05)
    for port in range(1, ports + 1):
        try:
            sock.connect((targetIP, port))
            opened_ports.append(port)
        except:
            pass
    sock.close()
    return opened_ports


def get_ping(targetIP):
    param = "-n" if sys.platform == "win32" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", targetIP], capture_output=True, timeout=3)
        if result.returncode == 0:
            return colored(f"[+] Host status: {targetIP} is ALIVE!", "green")
        return colored(f"[-] Host status: {targetIP} is DOWN", "red")
    except:
        return colored("[-] UNKNOWN", "yellow")


def get_reverse_DNS(targetIP):
    try:
        return socket.gethostbyaddr(targetIP)[0]
    except:
        return "Unknown"


def get_ttl(targetIP):
    try:
        packet = scapy.IP(dst=targetIP, ttl=64) / scapy.ICMP()
        response = scapy.sr1(packet, timeout=2, verbose=0)
        if response:
            return response.ttl
    except:
        pass
    return None


def recon_scan(targetIP):
    print(colored("[*] Starting OSINT reconnaissance...", "yellow"))
    sleep(1)

    ping = get_ping(targetIP)
    print(ping)
    hostname = get_reverse_DNS(targetIP)
    ttl = get_ttl(targetIP)
    MAC = getMAC(targetIP)
    geoIP = getGeoIP(targetIP)
    if MAC:
        vendor = mac_vendors.get(MAC[:8].upper(), "Unknown")
        print(colored(f"[+] MAC Address: {MAC}", "green"))
        print(colored(f"[+] Vendor: {vendor}"))
    else:
        print(colored("[-] MAC: unavailable", "red"))
        print(colored("[-] Vendor: unavailable", "red"))
    print(colored(f"[+] Host name: {hostname}", "cyan"))  # правильно
    if ttl:
        if ttl <= 64:
            os = "Linux/UNIX"
        elif ttl <= 128:
            os = "Windows"
        else:
            os = "Unknown"
        print(colored(f"[+] OS: {os}", "green"))
    else:
        print(colored("[-] OS: unavailable", "red"))
    if geoIP and geoIP.get('country'):
        print(colored(f"[+] Country: {geoIP.get('country')}", "green"))
        print(colored(f"[+] City: {geoIP.get('city')}", "green"))
        print(colored(f"[+] Provider: {geoIP.get('provider')}", "green"))
    else:
        print(colored("[-] Geo: unavailable for local IP", "red"))
    print(colored("[*] Scanning ports...", "yellow"))
    ports = get_opened_ports(targetIP)
    if ports:
        table = Table()
        table.title = "Opened ports"
        table.add_column("Port")
        table.add_column("Service")

        for port in ports:
            service = common_services.get(port, "Unknown")
            table.add_row(str(port), service)
        console.print(table)
    else:
        print(colored("[-] No open ports found", "red"))

show_banner()
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = input(colored("[*] Enter the target IP: ", "yellow"))
recon_scan(target)
