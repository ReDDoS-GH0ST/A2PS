import os
import sys
import hashlib
from time import sleep
from termcolor import colored

PASS_MASTER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "bases",
                        "passwords_master")


def show_banner():
    banner1 = """
            🔐 H  A  S  H --- C  R  A  C  K 🔐
            ----------------------------------
    """
    banner2 = (colored("    ┌──(", "cyan") + colored("root㉿kali", "red") + colored(")-[", "cyan") + colored(
        "root/kali/Desktop", "white") + colored(']', "cyan"))
    banner3 = colored("    └─", "cyan") + colored('#', "red") + colored(" a2ps", "blue") + colored(" scanp --script=hash-crack hash.txt", "white")
    banner4 = colored("[*] Cracking the hash \"0cb6b41fdbac850c04cba0456a0acba7fe80262c1f9ba4314d50b502fe1c8c1f\"...", "yellow")
    banner5 = colored("[+] Hash FOUND: pass123456Seven", "green")
    print(banner1)
    print(banner2)
    print(banner3)
    print(banner4)
    print(banner5)
    print(colored("    [🔐] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
    print(colored("    [🔐️] Function: ", "light_yellow") + colored("Crack hash\n", "red"))

def define_hash_type(hash):
    length = len(hash)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA1"
    elif length == 64:
        return "SHA256"
    elif length == 128:
        return "SHA512"
    else:
        return None


def crack_hash(hash, wordlist_master):
    hash_type = define_hash_type(hash)
    if not hash_type:
        print(colored("[-] Failed to define hash type", "red"))
        return None

    print(colored(f"[*] Hash type: {hash_type}", "cyan"))
    print(colored(f"[*] Using wordlist: {wordlist_master}", "magenta"))
    sleep(1)

    print(colored(f"[*] Starting the cracking of hash {hash}...", "yellow"))
    for filename in os.listdir(wordlist_master):
        try:
            filepath = os.path.join(PASS_MASTER, filename)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
                for word in file:
                    word = word.strip()
                    if hash_type == "MD5":
                        hashed = hashlib.md5(word.encode()).hexdigest()
                    elif hash_type == "SHA1":
                        hashed = hashlib.sha1(word.encode()).hexdigest()
                    elif hash_type == "SHA256":
                        hashed = hashlib.sha256(word.encode()).hexdigest()
                    elif hash_type == "SHA512":
                        hashed = hashlib.sha512(word.encode()).hexdigest()
                    if hashed == hash:
                        print(colored(f"[+] Hash FOUND: {word}", "green"))
                        return word
        except FileNotFoundError:
            print(colored(f"[-] Wordlist not found: {wordlist_master}", "red"))
            return None

    print(colored("[-] Password not found in wordlist", "red"))
    return None


show_banner()
if len(sys.argv) > 1:
    hash = sys.argv[1]
else:
    hash = input(colored("[*] Enter the hash: ", "yellow"))
crack_hash(hash, PASS_MASTER)