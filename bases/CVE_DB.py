vulnerabilities = {
    21: {
        "vsFTPd 2.3.4": {
            "CVE": "CVE-2011-2523",
            "Type": "RCE",
            "Dangerous": "Critical",
            "Description": "Backdoor in vsFTPd 2.3.4"
        },
        "proFTPd 1.3c": {
            "CVE": "CVE-2010-4221",
            "Type": "Buffer Overflow",
            "Dangerous": "Critical",
            "Description": "Stack overflow in proFTPd"
        }
    },
    22: {
        "OpenSSH Double Free": {
            "CVE": "CVE-2021-28041",
            "Type": "DoS",
            "Dangerous": "High",
            "Description": "OpenSSH double-free vulnerability"
        }
    },
    80: {
        "ShellShock": {
            "CVE": "CVE-2014-6271",
            "Type": "RCE",
            "Dangerous": "Critical",
            "Description": "Bash environment variable RCE via CGI scripts"
        }
    },
    443: {
        "Heartbleed": {
            "CVE": "CVE-2014-0160",
            "Type": "Info Leak",
            "Dangerous": "Critical",
            "Description": "OpenSSL memory leak (private keys, passwords)"
        }
    },
    445: {
        "EternalBlue": {
            "CVE": "CVE-2017-0144",
            "Type": "RCE",
            "Dangerous": "Critical",
            "Description": "SMBv1 remote code execution"
        },
        "EternalRomance": {
            "CVE": "CVE-2017-0145",
            "Type": "RCE",
            "Dangerous": "Critical",
            "Description": "SMBv1 remote code execution via malformed packets"
        },
        "EternalChampion": {
            "CVE": "CVE-2017-0146",
            "Type": "RCE",
            "Dangerous": "Critical",
            "Description": "SMBv1 race condition in transaction handling"
        },
        "EternalSynergy": {
            "CVE": "CVE-2017-0147",
            "Type": "Info Leak",
            "Dangerous": "High",
            "Description": "SMBv1 information disclosure"
        },
        "EternalRocks": {
            "CVE": "Multiple CVEs",
            "Type": "Worm",
            "Dangerous": "Critical",
            "Description": "Worm using 7 NSA exploits"
        }
    },
    3389: {
        "BlueKeep": {
            "CVE": "CVE-2019-0708",
            "Type": "RCE",
            "Dangerous": "Critical",
            "Description": "RDP RCE without authentication (Windows XP/7/2008)"
        }
    }
}
