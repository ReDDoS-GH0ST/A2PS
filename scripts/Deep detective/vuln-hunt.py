import os
import sys
import ssl
import ftplib
import socket
import logging

logging.getLogger("paramiko").setLevel(logging.CRITICAL)
import paramiko
import requests
import threading
from queue import Queue
from rich.box import ROUNDED
from rich.table import Table
from termcolor import colored
from rich.console import Console
from impacket.smbconnection import SMBConnection

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bases.CVE_DB import vulnerabilities

console = Console()
table = Table(box=ROUNDED, border_style="bold red")
vulnerabilities_count = 0
vuln_ports = (21, 22, 23, 25, 53, 80, 443, 445, 3389)

table.title = colored("Vulnerabilities", "white")
table.add_column("Vulnerability", style="bold red")
table.add_column("On port", style="cyan")
table.add_column("CVE", style="yellow")
table.add_column("Type", style="magenta")
table.add_column("Danger", style="red")
table.add_column("Description", style="green")


def show_banner():
    banner = """
                            🎯 V  U  L  N --- H  U  N  T 🎯
     -------------------------------------------------------------------------------------
     | 🖥️: Doctor, I've some head ake!<═══>🖨️: May You get it up?<═                      |
     |═>🖥️: Of course!<═══>🖨️: Let's look at it...<═══>🖥️: Well, what's                  |
     |there?<═══>💀: You'd better not know it...<═══>🖥️ It’s just a small vuln...right?  |
     -------------------------------------------------------------------------------------
    """
    print(banner)
    print(colored("       [🎯] Script mode: ", "light_yellow") + colored("🟡 Deep detective", "yellow"))
    print(colored("       [🎯] Function: ", "light_yellow") + colored("Check for common vulnerabilities\n", "red"))


def scan_opened_ports(targetIP):
    opened_ports = []
    for port in vuln_ports:
        sock = socket.socket()  # ← Новый сокет!
        sock.settimeout(0.05)
        try:
            sock.connect((targetIP, port))
            opened_ports.append(port)
        except:
            pass
        finally:
            sock.close()
    return opened_ports


def check_for_port21_vulns(targetIP, opened_ports):
    global vulnerabilities_count
    if 21 in opened_ports:
        try:
            ftp = ftplib.FTP(targetIP, timeout=4.5)
            banner = ftp.getwelcome()

            if "vsFTPd 2.3.4" in banner:
                table.add_row("vsFTPd 2.3.4", "21", "CVE-2011-2523", "RCE", "Critical", "Backdoor")
                vulnerabilities_count += 1
            if "ProFTPD 1.3c" in banner or "proFTPd 1.3c" in banner.lower():
                for vuln_name, vuln_data in vulnerabilities[21].items():
                    if vuln_name == "proFTPd 1.3c":
                        table.add_row(vuln_name, "21", vuln_data["CVE"], vuln_data["Type"], vuln_data["Dangerous"],
                                      vuln_data["Description"])
                        vulnerabilities_count += 1
        except:
            pass


def check_for_port22_vulns(targetIP, opened_ports):
    global vulnerabilities_count
    if 22 in opened_ports:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(targetIP, timeout=2.5, disabled_algorithms={"keys": ["ssh-rsa"]})
            banner = ssh.get_transport().remote_version
            ssh.close()

            if "OpenSSH 8.2" in banner or "OpenSSH_8.2" in banner:
                for vuln_name, vuln_data in vulnerabilities[22].items():
                    table.add_row(vuln_name, "22", vuln_data["CVE"], vuln_data["Type"], vuln_data["Dangerous"],
                                  vuln_data["Description"])
                    vulnerabilities_count += 1
        except:
            pass


def check_for_port80_vulns(targetIP, opened_ports):
    global vulnerabilities_count
    if 80 in opened_ports:
        try:
            headers = {"User-Agent": "() { :; }; echo; echo vulnerable"}
            response = requests.get(f"http://{targetIP}/", headers=headers, timeout=2.5)

            if "vulnerable" in response.text:
                for vuln_name, vuln_data in vulnerabilities[80].items():
                    table.add_row(vuln_name, "80", vuln_data["CVE"], vuln_data["Type"], vuln_data["Dangerous"],
                                  vuln_data["Description"])
                    vulnerabilities_count += 1
        except:
            pass


def check_for_port443_vulns(targetIP, opened_ports):
    global vulnerabilities_count
    if 443 in opened_ports:
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.5)
            ssl_sock = context.wrap_socket(sock, server_hostname=targetIP)
            ssl_sock.connect((targetIP, 443))

            heartbeat_response = b"\x18\x03\x02\x00\x03\x01\x40\x00"
            ssl_sock.send(heartbeat_response)
            response = ssl_sock.recv(4096)

            if len(response) > 3:
                for vuln_name, vuln_data in vulnerabilities[443].items():
                    table.add_row(vuln_name, "443", vuln_data["CVE"], vuln_data["Type"], vuln_data["Dangerous"],
                                  vuln_data["Description"])
                    vulnerabilities_count += 1
        except:
            pass


def check_for_port445_vulns(targetIP, opened_ports):
    global vulnerabilities_count
    if 445 in opened_ports:
        try:
            smb = SMBConnection(targetIP, targetIP)
            version = smb.getDialect()

            if "SMB1" in version.upper() or "NT LM 0.12" in version.upper():
                for vuln_name, vuln_data in vulnerabilities[445].items():
                    table.add_row(vuln_name, "445", vuln_data["CVE"], vuln_data["Type"], vuln_data["Dangerous"],
                                  vuln_data["Description"])
                    vulnerabilities_count += 1
        except:
            pass


def check_for_port3389_vulns(targetIP, opened_ports):
    global vulnerabilities_count
    if 3389 in opened_ports:
        try:
            sock = socket.socket()
            sock.settimeout(2.5)
            sock.connect((targetIP, 3389))
            RDP_response = b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00"
            sock.send(RDP_response)
            response = sock.recv(4096)

            if response:
                for vuln_name, vuln_data in vulnerabilities[3389].items():
                    table.add_row(vuln_name, "3389", vuln_data["CVE"], vuln_data["Type"], vuln_data["Dangerous"],
                                  vuln_data["Description"])
                    vulnerabilities_count += 1
        except:
            pass


def main(targetIP):
    global vulnerabilities_count
    print(colored(f"[*] Scanning {targetIP} for vulnerabilities...", "yellow"))
    opened_ports = scan_opened_ports(targetIP)
    check_for_port21_vulns(targetIP, opened_ports)
    check_for_port22_vulns(targetIP, opened_ports)
    check_for_port80_vulns(targetIP, opened_ports)
    check_for_port443_vulns(targetIP, opened_ports)
    check_for_port445_vulns(targetIP, opened_ports)
    check_for_port3389_vulns(targetIP, opened_ports)
    if vulnerabilities_count:
        print(colored(f"[+] {vulnerabilities_count} vulnerabilities FOUND!", "green"))
        console.print(table)
    else:
        print(colored("[-] No vulnerabilities found", "red"))
    print(colored("[+] Scanning was finished successfully!", "green"))


show_banner()
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = input(colored("[*] Enter the target IP: ", "yellow"))
main(target)
