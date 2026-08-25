import os
import sys
import socket
from time import sleep
from datetime import datetime
from termcolor import colored

import warnings
warnings.filterwarnings("ignore")

import scapy.all as scapy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bases.MAC_vendors import mac_vendors

common_services = {
    20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPCBind", 135: "MS-RPC",
    139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS",
    995: "POP3S", 1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    5900: "VNC", 8080: "HTTP-Alt",
}


def show_banner():
    banner1 = (colored("┌──(", "cyan") + colored("root㉿kali", "red") + colored(")-[", "cyan") + colored("/home/kali",
                                                                                                        "white") +
               colored(']', "cyan"))
    banner2 = colored("└─", "cyan") + colored('#', "red") + colored(" cat file.txt", "white")
    banner3 = """
    --------------------------------------------
    |     📄 C  A  S  E --- F  I  L  E 📄      |
    --------------------------------------------
    Oops! Here's no some info about me ;)
    """
    print(banner1)
    print(banner2)
    print(banner3)
    print(colored("    [📄] Script mode: ", "light_yellow") + colored("🟢 Base fingerprints", "green"))
    print(colored("    [📄] Function: ", "light_yellow") + colored("Save scan in file", "red"))


def get_hostname(targetIP):
    try:
        return socket.gethostbyaddr(targetIP)[0]
    except:
        return "Unknown"


def get_mac(targetIP):
    try:
        arp_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=targetIP)
        answered, _ = scapy.srp(arp_request, timeout=2, verbose=0)
        if answered:
            return answered[0][1].hwsrc
    except:
        pass
    return "Unknown"


def get_vendor(mac):
    if mac != "Unknown":
        return mac_vendors.get(mac[:8].upper(), "Unknown")
    return "Unknown"


def get_os(targetIP):
    try:
        packet = scapy.IP(dst=targetIP, ttl=64) / scapy.ICMP()
        response = scapy.sr1(packet, timeout=2, verbose=0)
        if response:
            ttl = response.ttl
            if ttl <= 64:
                return "Linux/UNIX"
            elif ttl <= 128:
                return "Windows"
            else:
                return "Unknown"
    except:
        pass
    return "Unknown"


def scan_ports(targetIP, ports=1000):
    if not targetIP:
        return []
    opened_ports = []
    sock = socket.socket()
    sock.settimeout(0.05)
    for port in range(1, ports + 1):
        try:
            sock.connect((targetIP, port))
            service = common_services.get(port, "Unknown")
            opened_ports.append(f"{port}:{service}")
        except:
            pass
    sock.close()
    return opened_ports


def save_scan(targetIP, file="scan"):
    hostname = get_hostname(targetIP)
    mac = get_mac(targetIP)
    vendor = get_vendor(mac)
    os_info = get_os(targetIP)
    report_time = datetime.now().strftime("%Y.%m.%d | %H:%M")
    opened_ports = scan_ports(targetIP)
    report = f"""
---------------A2PS Scan Report---------------
Date: {report_time}
Target: {targetIP}
Hostname: {hostname}
OS: {os_info}
MAC: {mac}
Vendor: {vendor}
Opened ports: {', '.join(opened_ports) if opened_ports else 'No'}
Closed/Filtered: {65535 - len(opened_ports)}
----------------------------------------------
"""
    print(colored(f"\n[*] Writing the report in file {file}.txt...", "yellow"))
    sleep(0.6)
    fname = "scan_" + datetime.now().strftime("%Y%m%d") + '_' + datetime.now().strftime("%H%M")
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    scan_dir = os.path.join(base_dir, "scans")
    os.makedirs(scan_dir, exist_ok=True)
    filepath = os.path.join(scan_dir, f"{fname}.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)
    print(colored(f"[+] File saved: {filepath}", "green"))


show_banner()
if len(sys.argv) > 1:
    targetIP = sys.argv[1]
else:
    targetIP = input(colored("[*] Enter the target IP: ", "yellow"))
save_scan(targetIP)
