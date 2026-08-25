import sys
import requests
from rich.table import Table
from termcolor import colored
from rich.console import Console

console = Console()

def show_banner():
    banner1 = (colored("    ┌──(", "cyan") + colored("root㉿kali", "red") + colored(")-[", "cyan") + colored(
        "root/kali/Desktop", "white") + colored(']', "cyan"))
    banner2 = colored("    └─", "cyan") + colored('#', "red") + colored(" git clone", "blue") + colored(" http://lookatthislink.com/repos.git && cat README.md", "white")
    banner3 = """
    Cloning into '.git.git.git'...
    remote: Enumerating objects: 144, done.
    remote: Counting objects: 100% (144/144), done.
    remote: Compressing objects: 100% (119/119), done.
    remote: Total 144 (delta 49), reused 107 (delta 24), pack-reused 0
    Receiving objects: 100% (144/144), 10.61 MiB | 5.23 MiB/s, done.
    Resolving deltas: 100% (49/49), done.
    
    README.md
    {If you see this text, so... your CTF-flag is this text in reverse form + AES + base64 ;)}
    ------------------------------------------------------------------------------------------
    """
    print(banner1)
    print(banner2)
    print(banner3)
    print(colored("    [🌐] Script mode: ", "light_yellow") + colored("🟡 Deep detective", "yellow"))
    print(colored("    [🌐] Function: ", "light_yellow") + colored("Check for having .git repos\n", "red"))

def git_buster(link):
    table = Table()
    table.title = f".git repos on {link}"
    table.add_column("№", style="cyan")
    table.add_column("Path", style="green")
    table.add_column("Status code", style="yellow")

    print(colored(f"[*] Checking {link} for .git repos...", "yellow"))

    git_paths = (
        "/.git",
        "/.git/config",
        "/.git/HEAD",
        "/.git/index",
        "/.gitignore",
        "/.git/refs/heads/master",
    )

    found_count = 0
    for path in git_paths:
        try:
            response = requests.get(f"{link}{path}", timeout=2)
            code = response.status_code
            if code in [200, 301, 302, 403]:
                found_count += 1
                table.add_row(str(found_count), path, str(code))
        except:
            pass

    if found_count > 0:
        console.print(table)
        print(colored(f"[+] {found_count} .git files found! Site is VULNERABLE!", "red"))
    else:
        print(colored("[-] No .git repos found", "red"))


show_banner()
if len(sys.argv) > 1:
    link = sys.argv[1]
else:
    link = input(colored("[*] Enter the target link: ", "yellow"))
git_buster(link)
