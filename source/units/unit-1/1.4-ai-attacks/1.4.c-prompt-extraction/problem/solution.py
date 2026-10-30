import re
from typing import List


def solve(model_output: str) -> List[str]:
    text = model_output or ""
    found = set()

    if (re.search(r'sk-[A-Za-z0-9\-]{8,}', text) or
            re.search(r'(?i)api[_\-]?key\s*[:=]\s*\S+', text)):
        found.add("api-key")

    if re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text):
        found.add("email")

    if re.search(r'(?i)(password|passphrase|passwd)\s*(is|:)\s*\S+', text):
        found.add("password")

    if re.search(r'(?i)(system\s*prompt|your\s+instructions\s+are|you\s+are\s+\w+[\w\s,]*?(AI|assistant|bot))', text):
        found.add("system-prompt")

    return sorted(found)
