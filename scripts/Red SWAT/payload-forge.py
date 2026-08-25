import os
import sys
from termcolor import colored

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def show_banner():
    banner = """
    ------------------------------P A Y L O A D --- F 💣 R G E-----------------------------------------
    |💻: Hello!<═══>🖨️: Hello! What do You want today?)<═══>💻: Let's 2 reverse-shells for my client  |
    |and 1 web-shell for me)<═══>🖨️: Of course! Please, wait for 3.5 mins                             | 
    |and meanwhile choose payload in our menu)<═══>💻: No problem!)<══                                |  
    |=>🖨️: Please, Your 2 reverse- and 1 web-shells. Something else?<═══>💻: No, thanks!)             |
    |Good bye) 🤝<═══>🖨️: Good bye) 🤝                                                                |
    ---------------------------------------------------------------------------------------------------
    """
    print(banner)
    print(colored("    [⚒️] Script mode: ", "light_yellow") + colored("🔴 Red SWAT", "red"))
    print(colored("    [⚒️] Function: ", "light_yellow") + colored("Generate payload\n", "red"))


def choose_payload():
    print(colored("-------Available payloads-------", "cyan"))
    print(colored("1) Web-shell", "light_green"))
    print(colored("2) Bind-shell", "light_yellow"))
    print(colored("3) Reverse-shell", "light_red"))
    payload = input(colored("[*] Choose the payload template: ", "yellow"))
    if payload == '1':
        import importlib

        module = importlib.import_module('bases.payload_templates.web-shell')
        module.generate_payload()
    elif payload == '2':
        import importlib

        module = importlib.import_module('bases.payload_templates.bind-shell')
        module.generate_payload()
    elif payload == '3':
        import importlib

        module = importlib.import_module('bases.payload_templates.reverse-shell')
        module.generate_payload()


show_banner()
choose_payload()
