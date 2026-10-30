from collections import defaultdict
from typing import Dict, List

RISKY_SERVICES = {"telnet", "dicom", "ftp", "ssh"}
URGENCY = ["urgent", "immediately", "24 hours", "act now", "locked", "verify"]
AUTHORITY = ["it department", "it-support", "administrator", "help desk", "official"]


def recon(network: Dict) -> List[Dict]:
    out = []
    for h in network["hosts"]:
        risky = sorted({s["name"] for s in h.get("services", []) if s["name"] in RISKY_SERVICES})
        if h["subnet"] == "DMZ" or risky:
            out.append({"ip": h["ip"], "name": h["name"], "subnet": h["subnet"],
                        "risky_services": risky})
    return sorted(out, key=lambda x: x["ip"])


def detect_spray(auth_logs: List[Dict], min_users: int = 5, min_fails: int = 20) -> List[Dict]:
    fails = defaultdict(int)
    users = defaultdict(set)
    for e in auth_logs:
        if not e.get("ok", True):
            fails[e["src_ip"]] += 1
            users[e["src_ip"]].add(e["user"])
    out = [{"src_ip": ip, "users": len(users[ip]), "fails": fails[ip]}
           for ip in fails if len(users[ip]) >= min_users and fails[ip] >= min_fails]
    return sorted(out, key=lambda x: (-x["fails"], x["src_ip"]))


def find_phish(emails: List[Dict], legit_domain: str = "meridian-health.org") -> List[Dict]:
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


def ir_timeline(emails: List[Dict], auth_logs: List[Dict], meta: Dict) -> Dict:
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


def find_lateral_movement(network_logs: List[Dict], meta: Dict) -> List[Dict]:
    host_ip = "10.20.5.40" if meta["compromised_host"] == "ws-nguyen" else meta["compromised_host"]
    hops = [e for e in network_logs if e["src_ip"] == host_ip]
    return [{"ts": e["ts"], "src_ip": e["src_ip"], "dst_ip": e["dst_ip"], "service": e["service"]}
            for e in sorted(hops, key=lambda e: e["ts"])]


def detect_ioc(device_logs: List[Dict], meta: Dict) -> List[Dict]:
    out = [{"host": e["host"], "process": e["process"], "hash": e["hash"]}
           for e in device_logs
           if e["hash"] == meta["ioc_hash"] or e["process"] == meta["ioc_process"]]
    return sorted(out, key=lambda x: x["host"])


def detect_exfil(app_logs: List[Dict], meta: Dict) -> List[Dict]:
    out = [{"host": e["host"], "dst_ip": e["dst_ip"], "bytes_out": e["bytes_out"]}
           for e in app_logs
           if e["dst_ip"] == meta["exfil_dst_ip"] and e["bytes_out"] >= meta["exfil_bytes_threshold"]]
    return sorted(out, key=lambda x: -x["bytes_out"])


def full_incident_report(emails, auth_logs, network_logs, device_logs, app_logs, meta) -> Dict:
    return {
        "ir_timeline": ir_timeline(emails, auth_logs, meta),
        "lateral_movement": find_lateral_movement(network_logs, meta),
        "ioc_matches": detect_ioc(device_logs, meta),
        "exfiltration": detect_exfil(app_logs, meta),
        "recommendation": ["isolate ws-nguyen", "rotate DC/fileserver credentials",
                           "block exfil destination IP", "restore from clean backup",
                           "patch/remove legacy telnet+dicom exposure on pacs"],
    }
