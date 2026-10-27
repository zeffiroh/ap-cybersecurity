"""Reference solution for 2.1.b. MUST pass 100% of tests.py."""
from typing import List, Dict, Any

CATEGORIES = [
    ("Nation-State / APT", ["zero-day", "state-sponsored", "espionage", "sabotage", "rootkit", "lateral movement", "exfiltrat"]),
    ("Cybercriminal", ["ransomware", "bitcoin", "payment", "extortion", "payroll", "fraud", "financial"]),
    ("Hacktivist", ["protest", "deface", "ideolog", "political", "publicity", "equity"]),
    ("Insider Threat", ["employee", "disgruntled", "exit interview", "insider", "negligent", "usb"]),
    ("Script Kiddie", ["script kiddie", "coin-miner", "coinminer", "default password", "port scan", "ftp exploit", "automated scan"]),
]

def solve(logs: List[Dict[str, Any]]) -> Dict[str, str]:
    """Classifies each alert log to identify the most likely threat actor category."""
    res = {}
    for entry in logs:
        lid = entry["id"]
        text = entry.get("log", "").lower()
        classified = "Unknown"
        
        for cat_name, keywords in CATEGORIES:
            if any(kw in text for kw in keywords):
                classified = cat_name
                break
        res[lid] = classified
    return res
