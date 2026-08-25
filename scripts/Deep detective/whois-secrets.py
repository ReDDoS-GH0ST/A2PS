import sys
import whois
from rich.table import Table
from termcolor import colored
from rich.console import Console

console = Console()


def show_banner():
    banner = """
    ┌───────────────────────────────────────────────────────────────┐
    │  📋 [W] [H] [O]  [I] [S] --- [S] [E] [C] [R] [E] [T] [S] 📋   │
    │ Appeal to me, when you need to get not understanding info ;)  │
    └───────────────────────────────────────────────────────────────┘"""
    print(banner)
    print(colored("    [📋] Script mode: ", "light_yellow") + colored("🟡 Deep detective", "yellow"))
    print(colored("    [📋] Function: ", "light_yellow") + colored("Gather WHOIS data", "red"))


def whois_lookup(domain):
    print(colored(f"[*] Gathering WHOIS data about {domain}...", "yellow"))
    try:
        who = whois.whois(domain)

        # Приводим к строкам
        domain_name = who.domain_name
        if isinstance(domain_name, list):
            domain_name = domain_name[0]

        registrar = who.registrar or "Unknown"

        creation_date = who.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        expiration_date = who.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        name_servers = who.name_servers
        if isinstance(name_servers, list):
            name_servers = ", ".join(name_servers)

        country = who.country or "Unknown"

        table = Table()
        table.title = "WHOIS Data"
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Domain", str(domain_name))
        table.add_row("Registrar", str(registrar))
        table.add_row("Creation date", str(creation_date))
        table.add_row("Expiration date", str(expiration_date))
        table.add_row("Name servers", str(name_servers))
        table.add_row("Country", str(country))

        console.print(table)
    except Exception as e:
        print(colored(f"[-] Failed to find WHOIS info: {e}", "red"))


show_banner()
if len(sys.argv) > 1:
    domain = sys.argv[1]
else:
    domain = input(colored("[*] Enter the domain: ", "yellow"))
whois_lookup(domain)
