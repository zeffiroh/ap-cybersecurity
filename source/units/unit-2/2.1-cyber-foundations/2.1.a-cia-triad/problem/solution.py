from typing import List, Dict, Any

def solve(data: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """Classifies a list of security incidents into CIA pillars based on keywords."""
    res = {}
    conf_kws = ["leak", "expose", "disclose", "intercept", "steal", "stole", "read", "password", "credential"]
    integ_kws = ["modify", "alter", "change", "corrupt", "tamper", "edit", "forge", "spoof"]
    avail_kws = ["down", "offline", "unavailable", "flood", "crash", "lock", "ransomware", "denial"]
    
    for item in data:
        eid = item["id"]
        desc = item["description"].lower()
        violated = []
        if any(kw in desc for kw in conf_kws):
            violated.append("Confidentiality")
        if any(kw in desc for kw in integ_kws):
            violated.append("Integrity")
        if any(kw in desc for kw in avail_kws):
            violated.append("Availability")
        res[eid] = sorted(violated)
    return res
