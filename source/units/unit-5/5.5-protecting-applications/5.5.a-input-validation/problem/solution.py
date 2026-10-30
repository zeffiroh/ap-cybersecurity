import re
from typing import Dict, List

_ALLOW = {
    "zip": re.compile(r"^\d{5}$"),
    "email": re.compile(r"^[A-Za-z0-9._+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+$"),
    "quantity": re.compile(r"^(?:[1-9][0-9]?)$"),
    "username": re.compile(r"^[A-Za-z0-9_]{3,20}$"),
}

_INJECTION = re.compile(
    r"(--|;|<script|</script|UNION\s+SELECT|OR\s+1\s*=\s*1|'\s*OR\s*'|\bDROP\s+TABLE\b|"
    r"\.\./|%3B|%2F)",
    re.IGNORECASE,
)


def solve(submissions: List[Dict[str, str]]) -> List[str]:
    blocked = []
    for sub in submissions:
        field_type = sub["type"]
        value = sub["value"]
        pattern = _ALLOW.get(field_type)
        allow_ok = bool(pattern and pattern.match(value))
        has_injection = bool(_INJECTION.search(value))
        if not allow_ok or has_injection:
            blocked.append(value)
    return blocked
