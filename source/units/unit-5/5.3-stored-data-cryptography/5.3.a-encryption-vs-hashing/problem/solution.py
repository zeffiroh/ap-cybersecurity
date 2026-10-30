import hashlib
import hmac
from typing import Union


def solve(action: str, password: str, param: str) -> Union[str, bool]:
    if action == "hash":
        salt = param
        hasher = hashlib.sha256()
        hasher.update((salt + password).encode("utf-8"))
        digest = hasher.hexdigest()
        return f"{salt}${digest}"
    elif action == "verify":
        stored_hash = param
        if "$" not in stored_hash:
            return False
        parts = stored_hash.split("$", 1)
        if len(parts) != 2:
            return False
        salt, expected_digest = parts
        hasher = hashlib.sha256()
        hasher.update((salt + password).encode("utf-8"))
        computed_digest = hasher.hexdigest()
        return hmac.compare_digest(computed_digest, expected_digest)
    else:
        raise ValueError("Invalid action. Must be 'hash' or 'verify'.")
