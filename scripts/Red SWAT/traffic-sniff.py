import os
import sys
import platform

import warnings
warnings.filterwarnings("ignore")

import scapy.all as scapy
from termcolor import colored
from time import sleep

os_system = platform.system()


def check_admin():
    if os_system == 'Windows':
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        return os.geteuid() == 0


def show_banner():
    banner1 = """
     ----------------------------------------------------------
     📻 [T] [R] [A] [F] [F] [I] [C] --- [S] [N] [I] [F] [F] 📻
     ----------------------------------------------------------
    """
    banner2 = colored("[+] 3 packets captured!")
    banner3 = colored("----------=Captured Packets Start\\=----------")
    banner4 = colored("U2FsdGVkX1/8xHm3kLpQ9vNw2RtyUioPAsdf7JkLmQwErTyUiOpLk=", "white")
    banner5 = colored("9jH3kLmN4bVcXzQwErTyUiOpLkM5nBvCxZ9aQwErTyUiOpLkM5nBvC", "white")
    banner6 = colored("TyUiOpLkM5nBvCxZ9aQwErTyUiOpLkRchWUI43egy5iiu356UGF82GO9582uhi", "white")
    banner7 = colored("----------=Captured Packets End\\=----------")
    banner8 = colored("It seem's AES-256 Cipher + MD5 salt...")
    print(banner1)
    print(banner2)
    print(banner3)
    print(banner4)
    print(banner5)
    print(banner6)
    print(banner7)
    print(banner8)
    print(colored("    [📻] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
    print(colored("    [📻] Function: ", "light_yellow") + colored("Intercept full traffic\n", "red"))


def intercept_traffic(packet, verbose='n'):
    if packet.haslayer(scapy.IP):
        src = packet[scapy.IP].src
        dst = packet[scapy.IP].dst

        print(colored(f"\n[+] 1 packet captured!", "green"))

        if packet.haslayer(scapy.TCP):
            print(colored(f"    From: {src}:{packet[scapy.TCP].sport}", "cyan"))
            print(colored(f"    To: {dst}:{packet[scapy.TCP].dport}", "cyan"))
            print(colored("    Protocol: TCP", "light_yellow"))
        elif packet.haslayer(scapy.UDP):
            print(colored(f"    From: {src}:{packet[scapy.UDP].sport}", "cyan"))
            print(colored(f"    To: {dst}:{packet[scapy.UDP].dport}", "cyan"))
            print(colored("    Protocol: UDP", "light_yellow"))

        if verbose == 'Y':
            print(colored("Packet:", "cyan"))
            print(packet.show())
        else:
            print(colored("Packet:", "cyan"))
            print(packet.summary())
        sleep(0.5)


if not check_admin():
    if os_system == "Windows":
        print(colored("[-] This script requires administrator privileges!", "red"))
    else:
        print(colored("[-] This script requires root privileges!", "red"))
    sys.exit(0)
else:
    show_banner()
    verbose = input(colored("[*] Show packets in verbose format (Y/n)?", "yellow"))
    print(colored("[*] Intercepting packets...", "yellow"))
    scapy.sniff(prn=lambda p: intercept_traffic(p, verbose), count=30)
    print(colored("[+] Sniffing was finished successfully!", "green"))
