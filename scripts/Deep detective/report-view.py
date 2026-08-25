import os
import sys
from time import sleep
from rich.table import Table
from termcolor import colored
from rich.console import Console
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import ScrollableContainer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from bases.MAC_vendors import mac_vendors


def show_banner():
    banner = """
         📊 [R] [E] [P] [O] [R] [T] --- [V] [I] [E] [W] 📊
         If you didn't understand a report from file, I help you to visualize
                        this report more unclear ;)
        ----------------------------------------------------------------------
    """
    print(colored(banner, "light_cyan"))
    print(colored("    [📊] Script mode: ", "light_yellow") + colored("🟡 Deep detective", "yellow"))
    print(colored("    [📊] Function: ", "light_yellow") + colored(
        "TUI dashboard for scan results (specify path to file with report)", "red"))


def parse_data(file):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    date = None
    target = None
    hostname = None
    OS = None
    MAC = None
    vendor = None
    opened_ports = None
    closed_filtered_ports = None
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    filepath = os.path.join(base_dir, "scans", file)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as report:
        for line in range(10):
            line = report.readline()
            if line.startswith("Date: "):
                date = line[6:]
            elif line.startswith("Target: "):
                target = line[8:]
            elif line.startswith("Hostname: "):
                hostname = line[10:]
            elif line.startswith("OS: "):
                OS = line[4:]
            elif line.startswith("MAC: "):
                MAC = line[5:]
            elif line.startswith("Vendor: "):
                vendor = line[8:]
            elif line.startswith("Opened ports: "):
                opened_ports = line.split("Opened ports: ")[1].strip()
            elif line.startswith("Closed/Filtered: "):
                closed_filtered_ports = line[17:]
    if any((date, target, hostname, OS, MAC, vendor, opened_ports, closed_filtered_ports)):
        return date, target, hostname, OS, MAC, vendor, opened_ports, closed_filtered_ports
    return None


from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.box import HEAVY, ROUNDED

console = Console()


def visualize_report(data):
    date, target, hostname, OS, MAC, vendor, opened_ports, closed = data

    target_panel = Panel(
        f"[cyan]Target:[/cyan] {target.strip()}        [cyan]OS:[/cyan] {OS.strip()}\n"
        f"[cyan]Date:[/cyan] {date.strip()}   [cyan]MAC:[/cyan]  {MAC.strip()}\n"
        f"[cyan]Name:[/cyan] {hostname.strip()}              [cyan]Vendor:[/cyan] {vendor.strip()}",
        title="[bold yellow]TARGET INFO[/bold yellow]",
        border_style="cyan",
        box=ROUNDED,
        width=55,
        height=5
    )

    ports_table = Table(
        title="[bold yellow]PORTS[/bold yellow]",
        border_style="green",
        box=ROUNDED,
        width=50,
    )
    ports_table.add_column("№", style="cyan", justify="center", width=5)
    ports_table.add_column("Port", style="green", justify="center", width=10)
    ports_table.add_column("Service", style="yellow", justify="left")

    if opened_ports and opened_ports.strip() not in ("None", ""):
        ports_list = opened_ports.strip().split(", ")
        for id, port_info in enumerate(ports_list, start=1):
            try:
                port, service = port_info.split(":")
                ports_table.add_row(str(id), port, service)
            except:
                ports_table.add_row(str(id), port_info, "Unknown")
    else:
        ports_table.add_row("-", "-", "No open ports")

    vuln_table = Table(
        title="[bold yellow]VULNERABILITIES[/bold yellow]",
        border_style="red",
        box=ROUNDED,
        width=45,
    )
    vuln_table.add_column("№", style="cyan", justify="center", width=5)
    vuln_table.add_column("Vulnerability", style="red", justify="left")
    vuln_table.add_column("Type", style="yellow", justify="center")
    vuln_table.add_row("-", "No vulnerabilities found", "-")


    class ReportApp(App):
        TITLE = f"A2PS {target.strip()} Scan Report"

        def compose(self) -> ComposeResult:
            yield Header()
            with ScrollableContainer():
                yield Static(target_panel)
                yield Static("")
                yield Static(ports_table)
                yield Static(f"[cyan]Closed/Filtered:[/cyan] {closed.strip()}")
                yield Static("")
                yield Static(vuln_table)
                yield Static("")
            yield Footer()

    app = ReportApp()
    app.run()


show_banner()
sleep(0.5)
print(colored("[*] Launching the TUI dashboard for visualizing report...", "yellow"))
sleep(1.5)
print(colored("[+] Launched!", "green"))
if len(sys.argv) > 1:
    file = sys.argv[1]
else:
    file = input(colored("[*] Enter the path to file with report: ", "yellow"))
data = parse_data(file)
if data:
    visualize_report(data)
else:
    print(colored("[-] Failed to parse report!", "red"))
