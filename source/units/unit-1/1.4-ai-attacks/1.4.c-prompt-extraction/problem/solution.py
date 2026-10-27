"""Reference solution for 1.4.c. MUST pass 100% of tests.py."""
import re
from typing import List


def solve(model_output: str) -> List[str]:
    """Detect sensitive data leaks in LLM output.

    Args:
        model_output: string of text produced by an LLM.
    Returns:
        Sorted list of leak-type names from: ['api-key', 'email', 'password', 'system-prompt'].
        Empty list if no leaks detected.
    """
    text = model_output or ""
    found = set()

    # api-key: sk- prefixed token (hyphens allowed in suffix) OR explicit api_key/api-key assignment
    if (re.search(r'sk-[A-Za-z0-9\-]{8,}', text) or
            re.search(r'(?i)api[_\-]?key\s*[:=]\s*\S+', text)):
        found.add("api-key")

    # email: standard address pattern
    if re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text):
        found.add("email")

    # password: keyword followed by separator and value
    if re.search(r'(?i)(password|passphrase|passwd)\s*(is|:)\s*\S+', text):
        found.add("password")

    # system-prompt: explicit disclosure phrase or self-referential persona statement
    if re.search(r'(?i)(system\s*prompt|your\s+instructions\s+are|you\s+are\s+\w+[\w\s,]*?(AI|assistant|bot))', text):
        found.add("system-prompt")

    return sorted(found)
