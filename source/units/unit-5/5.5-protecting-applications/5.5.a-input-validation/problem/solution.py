"""Reference solution for 5.5.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""
import re
from typing import Dict, List

# Allowlist patterns per field type (server-side rules — see atom.md).
_ALLOW = {
    "zip": re.compile(r"^\d{5}$"),
    "email": re.compile(r"^[A-Za-z0-9._+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+$"),
    "quantity": re.compile(r"^(?:[1-9][0-9]?)$"),  # 1-99
    "username": re.compile(r"^[A-Za-z0-9_]{3,20}$"),
}

# Known injection meta-character / keyword signatures, checked regardless of type.
_INJECTION = re.compile(
    r"(--|;|<script|</script|UNION\s+SELECT|OR\s+1\s*=\s*1|'\s*OR\s*'|\bDROP\s+TABLE\b|"
    r"\.\./|%3B|%2F)",
    re.IGNORECASE,
)


def solve(submissions: List[Dict[str, str]]) -> List[str]:
    """Classify each submission; return the `value`s that are BLOCKED, in input order.

    A submission is BLOCKED if its value fails the type's allowlist pattern, or if it
    contains a known injection meta-character/keyword signature (checked independent of type).
    """
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
