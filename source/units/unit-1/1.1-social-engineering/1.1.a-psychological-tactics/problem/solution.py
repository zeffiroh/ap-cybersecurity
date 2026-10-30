from typing import List

INDICATORS = {
    "urgency": [
        "urgent", "act now", "immediately", "right now", "asap", "expires",
        "within 24 hours", "24 hours", "as soon as possible", "don't delay", "do not delay",
    ],
    "authority": [
        "it department", "ceo", "manager", "administrator", "irs", "bank", "police",
        "official", "help desk", "human resources", "hr department",
    ],
    "scarcity": [
        "limited", "only", "last chance", "running out", "few left", "exclusive",
        "while supplies last", "act fast",
    ],
    "intimidation": [
        "legal action", "account suspended", "account will be locked", "penalty", "arrested",
        "fired", "terminated", "lawsuit", "consequences", "reported",
    ],
}


def solve(text: str) -> List[str]:
    low = (text or "").lower()
    found = {tactic for tactic, phrases in INDICATORS.items()
             if any(p in low for p in phrases)}
    return sorted(found)
