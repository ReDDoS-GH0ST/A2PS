from rich.table import Table
from termcolor import colored
from rich.console import Console
from prettytable import PrettyTable

console = Console()
examples = ["scanp" + colored(" -p=4444", "light_green"), "scanp" + colored(" -p=all", "light_green"),
            "scanp" + colored(" -h", "light_green"), "scanp" + colored(" -sV", "light_green"),
            "scanp" + colored(" -vb", "light_green"), "scanp" + colored(" --script=vuln-hunt", "light_green"),
            "showtar" + colored(" -h", "light_green"), "showtar" + colored(" -vb", "light_green")]
commands = {
    "scanp": "Scan open ports",
    "showtar": "Scan the network and get available targets",
    "showscr": "Show available scripts",
    "restart": "Restart A2PS",
    "help": "Print the usage documentation",
    "doc": "Print the usage documentation",
    "--version": "Show A2PS version",
    "clear": "Clear the screen",
    "banner": "Show banner",
    "quit": "Exit the program",
    "exit": "Exit the program"
}
arguments = {
    "-p=": ["Scan define port", "scanp"],
    "-p=all": ["Scan all ports (1-65535)", "scanp"],
    "--script=": ["Use script", "scanp"],
    "--plugin": ["Use plugin", "scanp", "showtar"],
    "-sV": ["Scan service and version", "scanp"],
    "-h": ["Print the usage documentation", "scanp", "showtar", "a2pee", "a2set", "a2crypt"],
    "-vb": ["Verbose process", "scanp", "showtar"],
}
scripts = {
    "🟢 Base fingerprints": {
        "🩸 first-blood": "Scan the base ports (21-23, 25, 53, 80, 443, 445, 3389, 8080)",
        "⚡ pulse-host": "Check is host alive (ICMP ping)",
        "👓 ghost-scan": "Anonymous SYN-scan",
        "📄 case-file": "Save scan in file",
        "📃 scan-file": "Scan targets from file (specify path to file)",
        "🔍 recon-scan": "Get all available target's information",
    },
    "🟡 Deep detective": {
        "🎯 vuln-hunt": "Check for common vulnerabilities",
        "📂 smb-enum": "SMB shares enumeration",
        "📋 whois-secrets": "Gather WHOIS data",
        "🗄️ black-dirs": "Scan hidden directories & files",
        "🌐 git-exposed": "Check for having .git repos",
        "📊 report-view": "TUI dashboard for scan results (specify path to file with report)",
        "🌊 oscillo-waves": "Visualize ports as oscilloscope waves",
        "🛡️ firewall-observe": "Detect firewall"
    },
    "🔴 Red SWAT": {
        "🪲 xss-bug": "Set XSS-payload & bug the target",
        "🔓 brute-force": "Brute force on target open ports",
        "🔐 hash-crack": "Crack hash",
        "💀 skull-shell": "Use bind-shell",
        "☢️ dos-time": "Launch DoS attack",
        "💉 sql-injector": "Scan & use SQL-Injection",
        "⚒️ payload-forge": "Generate payload",
        "🕸️ arp-spoof": "Launch MITM-attack",
        "📻 traffic-sniff": "Intercept full traffic"
    }
}


def showGeneralDoc():
    #  ===== Commands table =====
    print("\n\t\t========================  A2PS General Documentation ========================\n")
    table = PrettyTable()
    table.title = "Commands"
    table.field_names = ["№", "Command", "Description"]

    for id, (cmd, desc) in enumerate(commands.items(), start=1):
        colored_id = colored(str(id), "light_cyan")
        colored_cmd = colored(cmd, "yellow")
        colored_desc = colored(desc, "white")
        table.add_row([colored_id, colored_cmd, colored_desc])

    print(table, "\n")
    table.clear()
    # ===== Arguments table =====
    table.title = "Arguments"
    table.field_names = ["№", "Argument", "Description", "For command"]

    for id, (arg, values) in enumerate(arguments.items(), start=1):
        desc = values[0]
        for_cmd = ', '.join(values[1:])

        colored_id = colored(id, "light_cyan")
        colored_arg = colored(arg, "light_green")
        colored_desc = colored(desc, "white")
        colored_for_cmd = colored(for_cmd, "yellow")

        table.add_row([colored_id, colored_arg, colored_desc, colored_for_cmd])

    print(table, "\n")

    table.clear_rows()
    print(colored("📝 Examples:", "light_yellow", attrs=["bold"]))
    for id, example in enumerate(examples, start=1):
        colored_id = colored(id, "light_cyan")
        colored_example = colored(example, "yellow")
        print('  ', f'{colored_id}.', colored_example)

    table.clear()
    table.field_names = []


def showScanpDoc():
    richTable = Table()
    print("\n\t\t========================  Command \"scanp\" Documentation ========================\n")
    print(colored("Use command \"scanp\" for scanning open ports of target\n", "white"))
    # ===== Arguments of command "scanp" =====
    richTable.title = colored("Available arguments", "white")
    richTable.add_column("№")
    richTable.add_column("Argument")
    richTable.add_column("Description")
    richTable.add_column("Example")

    richTable.add_row("[cyan]1[/cyan]", "[light_green]-p=[/light_green]", "Scan define port",
                      "[yellow]scanp[/yellow] [light_green]-p=4444[/light_green]")
    richTable.add_row("[cyan]2[/cyan]", "[light_green]-p=all[/light_green]", "Scan all ports (1-65535)",
                      "[yellow]scanp[/yellow] [light_green]-p=all[/light_green]")
    richTable.add_row("[cyan]3[/cyan]", "[light_green]--script=[/light_green]", "Use script",
                      "[yellow]scanp[/yellow] [light_green]--script=fist-blood[/light_green]")
    richTable.add_row("[cyan]4[/cyan]", "[light_green]-sV[/light_green]", "Scan service and version",
                      "[yellow]scanp[/yellow] [light_green]-sV[/light_green]")
    richTable.add_row("[cyan]5[/cyan]", "[light_green]-h[/light_green]", "Print the usage documentation",
                      "[yellow]scanp[/yellow] [light_green]-h[/light_green]")
    richTable.add_row("[cyan]6[/cyan]", "[light_green]-vb[/light_green]", "Verbose process",
                      "[yellow]scanp[/yellow] [light_green]-vb[/light_green]")

    console.print(richTable)


def showShowtarDoc():
    print("\n\t\t========================  Command \"showtar\" Documentation ========================\n")
    print(colored("Use command \"showtar\" for scanning available targets in the current network\n", "white"))
    # ===== Arguments of command "showtar" =====
    richTable = Table()
    richTable.title = colored("Available arguments", "white")
    richTable.add_column("№")
    richTable.add_column("Argument")
    richTable.add_column("Description")
    richTable.add_column("Example")

    richTable.add_row("[cyan]1[/cyan]", "[light_green]-h[/light_green]", "Print the usage documentation",
                      "[yellow]showtar[/yellow] [light_green]-h[/light_green]")
    richTable.add_row("[cyan]2[/cyan]", "[light_green]-vb[/light_green]", "Verbose process",
                      "[yellow]showtar[/yellow] [light_green]-vb[/light_green]")

    console.print(richTable)


def showA2peeDoc():
    print("\n\t\t========================  Command \"a2pee\" Documentation ========================\n")
    print(colored("Use command \"a2pee\" for using A2PEE\n", "white"))
    print(colored("A2PEE (A2PS Exploits Engine) is an powerful engine for launching exploits\n", "white"))
    # ===== Arguments of command "a2pee" =====
    richTable = Table()
    richTable.title = colored("Available arguments", "white")
    richTable.add_column("№")
    richTable.add_column("Argument")
    richTable.add_column("Description")
    richTable.add_column("Example")

    richTable.add_row("[cyan]1[/cyan]", "[light_green]-h[/light_green]", "Print the usage documentation","[yellow]a2pee[/yellow] [light_green]-h[/light_green]")
    richTable.add_row("[cyan]2[/cyan]", "[light_green]--use=[/light_green]", "Choose & use an exploit","[yellow]a2pee[/yellow] [light_green]--use=windows/smb/ms17010-eternal-blue[/light_green]")

    console.print(richTable)

def showA2setDoc():
    print("\n\t\t========================  Command \"a2set\" Documentation ========================\n")
    print(colored("Use command \"a2set\" for using A2SET\n", "white"))
    print(colored("A2SET (A2PS Social Engineering Toolkit) is an powerful engine for launching soc. eng. tools\n", "white"))
    # ===== Arguments of command "a2set" =====
    richTable = Table()
    richTable.title = colored("Available arguments", "white")
    richTable.add_column("№")
    richTable.add_column("Argument")
    richTable.add_column("Description")
    richTable.add_column("Example")

    richTable.add_row("[cyan]1[/cyan]", "[light_green]-h[/light_green]", "Print the usage documentation","[yellow]a2set[/yellow] [light_green]-h[/light_green]")
    richTable.add_row("[cyan]2[/cyan]", "[light_green]--use=[/light_green]", "Choose & use an tool","[yellow]a2set[/yellow] [light_green]--use=phishing/fakefacebook[/light_green]")

    console.print(richTable)


def showScripts():
    print("\n\t\t=========================  Scripts =========================\n")
    print(colored("🟢 Base fingerprints:", "green") + "\n\
            🩸 first-blood: Scan the base ports (21-23, 25, 53, 80, 135, 139, 443, 445, 3389, 8080)\n\
            👓 ghost-scan: Anonymous SYN-scan\n\
            ⚡ pulse-host: Check is host alive (ICMP ping)\n\
            📄 case-file: Save scan in file\n\
            📃 scan-file: Scan targets from file (specify path to file)\n\
            🔍 recon-scan: Get all available target's information")
    print("----------------------------------------------------------------------------------")
    print(colored("🟡 Deep detective:", "yellow") + "\n\
            🎯 vuln-hunt: Check for common vulnerabilities\n\
            📂 smb-enum: SMB shares enumeration\n\
            📋 whois-secrets: Gather WHOIS data\n\
            🗄️ black-dirs: Scan hidden directories & files\n\
            🌐 git-exposed: Check for having .git repos\n\
            🛡️ firewall-observe: Detect firewall\n\
            🌊 oscillo-waves: Visualize ports as oscilloscope waves\n\
            📊 report-view: TUI dashboard for scan results (specify path to file with report)")
    print("----------------------------------------------------------------------------------")
    print(colored("🔴 Red SWAT:", "red") + "\n\
            🪲 xss-bug: Set XSS-payload & bug the target\n\
            🔓 brute-force: Launch brute force on target open ports\n\
            🔐 hash-crack: Crack hash\n\
            💀 skull-shell: Use bind-shell\n\
            ☢️ dos-time: Launch DoS attack\n\
            💉 sql-injector: Scan & use SQL-Injection\n\
            ⚒️ payload-forge: Generate payload\n\
            🕸️ arp-spoof: Launch MITM-attack\n\
            📻 traffic-sniff: Intercept full traffic")
