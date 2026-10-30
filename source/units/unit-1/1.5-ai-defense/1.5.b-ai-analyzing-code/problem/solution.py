from typing import List

RULES = [
    ("vuln:eval",                "eval(",        True),
    ("vuln:hardcoded_password",  "password =",   False),
    ("vuln:md5",                 "md5(",         True),
    ("vuln:os_system",           "os.system(",   True),
    ("vuln:pickle_loads",        "pickle.loads(", True),
    ("vuln:subprocess_shell",    "shell=True",   True),
]


def solve(code: str) -> List[str]:
    if not code:
        return []
    findings = set()
    for tag, trigger, case_sensitive in RULES:
        haystack = code if case_sensitive else code.lower()
        needle = trigger if case_sensitive else trigger.lower()
        if needle in haystack:
            findings.add(tag)
    return sorted(findings)
