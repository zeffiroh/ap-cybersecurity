"""Reference solution for 1.5.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
from typing import List

# Each rule: (tag, trigger_string, case_sensitive)
RULES = [
    ("vuln:eval",                "eval(",        True),
    ("vuln:hardcoded_password",  "password =",   False),  # case-insensitive
    ("vuln:md5",                 "md5(",         True),
    ("vuln:os_system",           "os.system(",   True),
    ("vuln:pickle_loads",        "pickle.loads(", True),
    ("vuln:subprocess_shell",    "shell=True",   True),
]


def solve(code: str) -> List[str]:
    """Return sorted, de-duplicated vulnerability tags for dangerous patterns in Python source."""
    if not code:
        return []
    findings = set()
    for tag, trigger, case_sensitive in RULES:
        haystack = code if case_sensitive else code.lower()
        needle = trigger if case_sensitive else trigger.lower()
        if needle in haystack:
            findings.add(tag)
    return sorted(findings)
