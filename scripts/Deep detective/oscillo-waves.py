# oscillo-waves.py
import sys
import math
import time
import socket
from time import sleep
from termcolor import colored
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import ScrollableContainer

common_services = {
    20: "FTP-Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP-Server",
    68: "DHCP-Client",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    111: "RPCBind",
    123: "NTP",
    135: "MS-RPC",
    137: "NetBIOS-NS",
    138: "NetBIOS-DGM",
    139: "NetBIOS-SSN",
    143: "IMAP",
    161: "SNMP",
    162: "SNMP-Trap",
    179: "BGP",
    194: "IRC",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    514: "Syslog",
    515: "LPR",
    520: "RIP",
    554: "RTSP",
    587: "SMTP-Submission",
    631: "IPP",
    636: "LDAPS",
    873: "Rsync",
    993: "IMAPS",
    995: "POP3S",
    1025: "NFS-or-IIS",
    1080: "SOCKS-Proxy",
    1194: "OpenVPN",
    1433: "MSSQL",
    1434: "MSSQL-Browser",
    1521: "Oracle",
    1701: "L2TP",
    1723: "PPTP",
    1812: "RADIUS",
    1883: "MQTT",
    2049: "NFS",
    2082: "cPanel-HTTP",
    2083: "cPanel-HTTPS",
    2181: "ZooKeeper",
    2222: "SSH-Alt",
    2375: "Docker-REST",
    2376: "Docker-TLS",
    2483: "Oracle-SSL",
    3000: "Grafana/Node.js",
    3128: "Squid-Proxy",
    3260: "iSCSI",
    3306: "MySQL",
    3389: "RDP",
    3478: "STUN",
    3690: "SVN",
    4000: "ICQ/Diablo",
    4369: "Erlang-EPMD",
    4443: "HTTPS-Alt",
    4444: "Metasploit",
    4567: "Sinatra/Webrick",
    5000: "UPnP/Flask",
    5001: "Synology",
    5038: "Asterisk-AMI",
    5060: "SIP",
    5222: "XMPP",
    5269: "XMPP-Server",
    5353: "mDNS",
    5432: "PostgreSQL",
    5555: "Android-ADB",
    5601: "Kibana",
    5672: "RabbitMQ",
    5700: "Node-RED",
    5800: "VNC-HTTP",
    5900: "VNC",
    5901: "VNC-1",
    5984: "CouchDB",
    5985: "WinRM-HTTP",
    5986: "WinRM-HTTPS",
    5999: "CVS",
}


def show_banner():
    banner = """
          🌊 O S C I L L O --- W A V E S 🌊
        Why are you carrying this oscillo-TV when 
        You may look at the same picture just in terminal?)
    """
    print(colored(banner, "light_cyan"))
    print(colored("       [🌊] Script mode: ", "light_yellow") + colored("🟡 Deep detective", "yellow"))
    print(colored("       [🌊] Function: ", "light_yellow") + colored("Visualize ports as oscilloscope waves\n", "red"))


class WaveWidget(Static):
    def __init__(self, port, service, response_time=0.0):
        super().__init__("")
        self.port = port
        self.service = service
        self.response_time = response_time
        # Частота зависит от времени ответа (замедленная)
        self.freq = 10.0 / (response_time + 1.0)
        self.start_time = time.time()

    def on_mount(self):
        self.set_interval(0.1, self.update_wave)

    def get_wave_symbol(self, distance):
        if distance == 0:
            return "[bold white]█[/bold white]"
        elif distance == 1:
            return "[cyan]█[/cyan]"
        elif distance == 2:
            return "[blue]█[/blue]"
        else:
            return " "

    def update_wave(self):
        t = time.time() - self.start_time

        # Цвет частоты
        if self.freq > 0.5:
            freq_color = "green"
        elif self.freq > 0.1:
            freq_color = "yellow"
        else:
            freq_color = "red"

        # Цвет времени ответа
        if self.response_time < 10:
            time_color = "green"
        elif self.response_time < 50:
            time_color = "yellow"
        else:
            time_color = "red"

        wave = ""
        for y in range(11, 0, -1):
            line = ""
            for x in range(50):
                wave_y = int(5 + 3 * math.sin(x / 5 + t * self.freq))  # Амплитуда 3
                distance = abs(y - wave_y)
                line += self.get_wave_symbol(distance)
            wave += line + "\n"

        self.update(
            f"[bold cyan]Port {self.port}[/bold cyan]\n"
            f"┌─────────────────────────────────────────────────┐   Service: [yellow]{self.service}[/yellow]\n"
            f"│{wave[:-1]}│\n"
            f"└─────────────────────────────────────────────────┘   Response: [{time_color}]{self.response_time:.1f}ms[/{time_color}]\n"
            f"[{freq_color}]Freq: {self.freq:.3f} Hz[/{freq_color}] | [dim]Time: {time.strftime('%H:%M:%S')}[/dim]\n"
        )


class OscilloWavesApp(App):
    TITLE = "A2PS Oscillo-Waves"

    def scan_opened_ports(self, targetIP):
        opened_ports = []
        sock = socket.socket()
        sock.settimeout(0.001)
        for port in range(1, 6001):
            start = time.time()
            try:
                sock.connect((targetIP, port))
                response_time = (time.time() - start) * 1000
                opened_ports.append((port, response_time))
            except:
                pass
            finally:
                sock.close()
        return opened_ports

    def compose(self) -> ComposeResult:
        yield Header()
        with ScrollableContainer():
            ports = self.scan_opened_ports(self.target)
            if not ports:
                yield Static("[red]No open ports found![/red]")
            else:
                for port, response_time in ports:
                    service = common_services.get(port, "Unknown")
                    yield WaveWidget(port, service, response_time)
        yield Footer()


if __name__ == "__main__":
    show_banner()
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input(colored("Enter the target IP: ", "yellow"))

    app = OscilloWavesApp()
    app.target = target
    print(colored("[*] Launching TUI oscilloscope...", "yellow"))
    sleep(2.5)
    print(colored("[+] TUI Oscilloscope launched!", "green"))
    sleep(0.5)
    app.run()