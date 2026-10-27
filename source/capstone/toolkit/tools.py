"""mhsec tools — deterministic, offline analysis functions over the Meridian world.
Each is a blackbox: stable signature + contract (see interface.md). The CLI (mhsec.py) and the
stage checks (../stages) call these. Students can reimplement any of them; assemble.py verifies.
"""
from collections import defaultdict
from typing import Dict, List

RISKY_SERVICES = {"telnet", "dicom", "ftp", "ssh"}   # exposed/legacy services worth flagging
URGENCY = ["urgent", "immediately", "24 hours", "act now", "locked", "verify"]
AUTHORITY = ["it department", "it-support", "administrator", "help desk", "official"]


# ---- recon / scan -------------------------------------------------------
def recon(network: Dict) -> List[Dict]:
    """Map the externally-reachable / risky surface. Returns sorted host findings:
    every DMZ host, plus any host exposing a RISKY_SERVICES port, with the flagged services."""
    out = []
    for h in network["hosts"]:
        risky = sorted({s["name"] for s in h.get("services", []) if s["name"] in RISKY_SERVICES})
        if h["subnet"] == "DMZ" or risky:
            out.append({"ip": h["ip"], "name": h["name"], "subnet": h["subnet"],
                        "risky_services": risky})
    return sorted(out, key=lambda x: x["ip"])


# ---- log analysis: password spray --------------------------------------
def detect_spray(auth_logs: List[Dict], min_users: int = 5, min_fails: int = 20) -> List[Dict]:
    """Detect password spraying: a single src_ip with failed logins across many distinct users.
    Returns sorted list of {src_ip, users, fails} for IPs over BOTH thresholds."""
    fails = defaultdict(int)
    users = defaultdict(set)
    for e in auth_logs:
        if not e.get("ok", True):
            fails[e["src_ip"]] += 1
            users[e["src_ip"]].add(e["user"])
    out = [{"src_ip": ip, "users": len(users[ip]), "fails": fails[ip]}
           for ip in fails if len(users[ip]) >= min_users and fails[ip] >= min_fails]
    return sorted(out, key=lambda x: (-x["fails"], x["src_ip"]))


# ---- phishing triage ----------------------------------------------------
def find_phish(emails: List[Dict], legit_domain: str = "meridian-health.org") -> List[Dict]:
    """Flag malicious emails by indicator, NOT by the synthetic 'malicious' field.
    Indicators: lookalike-domain (sender domain != legit but contains the brand),
    urgency, authority, credential-link (http link asking to verify/sign-in)."""
    out = []
    for m in emails:
        ind = []
        dom = m["from"].split("@")[-1].lower()
        if dom != legit_domain and "meridian" in dom:
            ind.append("lookalike-domain")
        text = (m.get("subject", "") + " " + m.get("body", "")).lower()
        if any(w in text for w in URGENCY):
            ind.append("urgency")
        if any(w in (m["from"].lower() + " " + text) for w in AUTHORITY):
            ind.append("authority")
        if m.get("link", "").startswith("http") and ("verify" in m["link"] or "owa" in m["link"]):
            ind.append("credential-link")
        if ind:
            out.append({"id": m["id"], "from": m["from"], "to": m["to"],
                        "indicators": sorted(set(ind))})
    return sorted(out, key=lambda x: x["id"])


# ---- incident response timeline ----------------------------------------
def ir_timeline(emails: List[Dict], auth_logs: List[Dict], meta: Dict) -> Dict:
    """Reconstruct the breach: which user, via which email, then suspicious login. Returns a
    deterministic summary used by the stage checker and the after-action report."""
    phish = [m for m in find_phish(emails) if "lookalike-domain" in m["indicators"]]
    victim_user = meta["victim"].split("@")[0]
    suspicious = [e for e in auth_logs
                  if e["user"] == victim_user and e.get("geo") == "unusual"]
    return {
        "victim": meta["victim"],
        "entry_email": phish[0]["id"] if phish else None,
        "lookalike_domain": meta["lookalike_domain"],
        "compromised_login_src": suspicious[0]["src_ip"] if suspicious else None,
        "recommendation": ["reset victim credentials", "enable MFA", "block lookalike domain",
                           "user awareness training"],
    }


# ---- network pivot / lateral movement (Unit 3) --------------------------
def find_lateral_movement(network_logs: List[Dict], meta: Dict) -> List[Dict]:
    """Trace the pivot chain starting from meta['compromised_host']'s IP. Returns the ordered
    list of {src_ip, dst_ip, service} hops originating from the compromised workstation."""
    host_ip = "10.20.5.40" if meta["compromised_host"] == "ws-nguyen" else meta["compromised_host"]
    hops = [e for e in network_logs if e["src_ip"] == host_ip]
    return [{"ts": e["ts"], "src_ip": e["src_ip"], "dst_ip": e["dst_ip"], "service": e["service"]}
            for e in sorted(hops, key=lambda e: e["ts"])]


# ---- device / endpoint compromise (Unit 4) -------------------------------
def detect_ioc(device_logs: List[Dict], meta: Dict) -> List[Dict]:
    """Flag endpoint processes matching the known-bad hash/process name (IOC). Returns sorted
    list of {host, process, hash} matches."""
    out = [{"host": e["host"], "process": e["process"], "hash": e["hash"]}
           for e in device_logs
           if e["hash"] == meta["ioc_hash"] or e["process"] == meta["ioc_process"]]
    return sorted(out, key=lambda x: x["host"])


# ---- application / data exfiltration (Unit 5) ----------------------------
def detect_exfil(app_logs: List[Dict], meta: Dict) -> List[Dict]:
    """Flag outbound transfers to external IPs exceeding meta['exfil_bytes_threshold']."""
    out = [{"host": e["host"], "dst_ip": e["dst_ip"], "bytes_out": e["bytes_out"]}
           for e in app_logs
           if e["dst_ip"] == meta["exfil_dst_ip"] and e["bytes_out"] >= meta["exfil_bytes_threshold"]]
    return sorted(out, key=lambda x: -x["bytes_out"])


# ---- final after-action report (Unit 5 / detection+IR) -------------------
def full_incident_report(emails, auth_logs, network_logs, device_logs, app_logs, meta) -> Dict:
    """Aggregate every stage's findings into one deterministic after-action report."""
    return {
        "ir_timeline": ir_timeline(emails, auth_logs, meta),
        "lateral_movement": find_lateral_movement(network_logs, meta),
        "ioc_matches": detect_ioc(device_logs, meta),
        "exfiltration": detect_exfil(app_logs, meta),
        "recommendation": ["isolate ws-nguyen", "rotate DC/fileserver credentials",
                           "block exfil destination IP", "restore from clean backup",
                           "patch/remove legacy telnet+dicom exposure on pacs"],
    }
