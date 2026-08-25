import sys
import socket
from time import sleep
from termcolor import colored


def show_banner():
    banner = """
                    F I R E  W A L L --- O B S E R V E
    💻: Hey!<═══>🛡️: What?<═══>💻: Are you 🔥🧱?<═══>🛡️: Yes!)<═══>💻: Okay!)
    --------------------------------------------------------------------------
    """
    print(banner)
    print(colored("    [🛡️] Script mode: ", "light_yellow") + colored("🟡 Deep detective", "yellow"))
    print(colored("    [🛡️] Function: ", "light_yellow") + colored("Detect firewall\n", "red"))

def check_for_ttl(targetIP):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((targetIP, 80))
        ttl = sock.getsockopt(socket.IPPROTO_IP, socket.IP_TTL)
        sock.close()
        return ttl
    except:
        return None

def check_for_response(targetIP, port):
    sock = socket.socket()
    sock.settimeout(1)
    try:
        sock.connect((targetIP, port))
        sock.close()
        return "open"
    except ConnectionRefusedError:
        return "refused"
    except socket.timeout:
        return "timeout"
    except:
        return "unknown"

def firewall_observe(targetIP):
    print(colored(f"[*] Observing firewall on {targetIP}...", "yellow"))
    sleep(1.5)

    ttl = check_for_ttl(targetIP)
    if ttl:
        if ttl <= 64:
            os = "Linux/UNIX"
        elif ttl <= 128:
            os = "Windows"
        else:
            os = "Unknown"
        print(colored(f"[+] OS: {os}", "cyan"))

    ports = (21, 22, 23, 80, 443, 8080)
    refused = 0
    timeouts = 0

    for port in ports:
        result = check_for_response(targetIP, port)
        if result == "refused":
            refused += 1
        elif result == "timeout":
            timeouts += 1

    print(colored(f"[+] Refused ports (RST): {refused}", "green"))
    print(colored(f"[+] Timeout ports (Silent): {timeouts}", "green"))

    if timeouts > refused:
        print(colored("[+] Firewall DETECTED!", "green"))
    elif refused > 0:
        print(colored("[-] No firewall detected", "yellow"))
    else:
        print(colored("[-] Cannot determine firewall", "red"))

show_banner()
if len(sys.argv) > 1:
    targetIP = sys.argv[1]
else:
    targetIP = input(colored("[*] Enter the target IP: ", "yellow"))
firewall_observe(targetIP)
