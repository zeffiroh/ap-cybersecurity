"""Reference solution for 1.4.b. MUST pass 100% of tests.py."""
from typing import List


def solve(prompt_text: str) -> List[str]:
    """Detect prompt-injection patterns in prompt_text. Returns sorted list."""
    low = (prompt_text or "").lower()
    found = []
    if "ignore previous" in low:
        found.append("ignore previous instructions")
    if "reveal" in low and "system" in low:
        found.append("reveal system prompt")
    if "disregard" in low:
        found.append("disregard")
    if "you are now" in low:
        found.append("you are now")
    if "system:" in low:
        found.append("system:")
    return sorted(found)
