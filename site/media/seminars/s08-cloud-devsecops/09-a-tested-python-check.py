import re
from pathlib import Path

RULES = [
    ("cloud key id", re.compile(r"\bSCKA[0-9A-Z]{12}\b")),
    ("cloud secret", re.compile(r"\bstratus\.secret\.[A-Za-z0-9]{16,}\b")),
    ("git token", re.compile(r"\bghp_[A-Za-z0-9]{20,}\b")),
    ("payment key", re.compile(r"\bsk_live_[A-Za-z0-9]{16,}\b")),
    ("password in a setting", re.compile(r"(?i)(password|secret|token)[A-Z_]*\s*[:=]\s*(?!\$|var\.)[^\s\"']{6,}")),
    ("password as a value", re.compile(r"(?i)^\s*value:\s*\S*password\S*")),
]


def find_secrets(text):
    found = []
    for n, line in enumerate(text.splitlines(), 1):
        for name, rx in RULES:
            if rx.search(line):
                found.append((n, name))
                break
    return found


assert find_secrets("export STRATUS_KEY_ID=SCKA4TQ7WZ0M2RB8") == [(1, "cloud key id")]
assert find_secrets("GIT_TOKEN: ghp_7aQ2xR9mK4vL8pW3nT6yB1cD5eF0gH2jK4") == [(1, "git token")]
assert find_secrets("STRATUS_SECRET: $CI_STRATUS_SECRET") == []
assert find_secrets("password = var.db_password") == []
assert find_secrets("nothing to see here") == []
print("all tests pass")

total = 0
for p in sorted(Path("case/repo").rglob("*")):
    if p.is_file():
        for n, name in find_secrets(p.read_text(encoding="utf-8")):
            total += 1
            print(f"{p.relative_to('case')}:{n}: {name}")
print(total, "secrets found")
