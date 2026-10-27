"""Reference solution for 1.5.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List

# Rule set: each entry is (tag, list_of_trigger_substrings).
# A line triggers the tag if ANY trigger substring matches (case-insensitive).
RULES = [
    ("insecure:PermitRootLogin",      ["permitrootlogin yes"]),
    ("insecure:PasswordAuthentication", ["passwordauthentication yes"]),
    ("insecure:Port23",               ["port 23"]),
    ("insecure:SSLDisabled",          ["ssl false", "ssl off", "tls false", "tls off"]),
    ("insecure:X11Forwarding",        ["x11forwarding yes"]),
    ("insecure:PermitEmptyPasswords", ["permitemptypasswords yes"]),
]


def solve(config_lines: List[str]) -> List[str]:
    """Return sorted, de-duplicated security finding tags for insecure config directives."""
    findings = set()
    for raw in config_lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        low = line.lower()
        for tag, triggers in RULES:
            if any(t in low for t in triggers):
                findings.add(tag)
    return sorted(findings)
