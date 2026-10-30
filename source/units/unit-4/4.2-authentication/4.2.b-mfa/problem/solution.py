from typing import List, Optional

_CATEGORY = {
    "password": "knowledge",
    "pin": "knowledge",
    "security_question": "knowledge",
    "sms_code": "possession",
    "totp_code": "possession",
    "authenticator_app": "possession",
    "push_approved": "possession",
    "backup_code": "possession",
    "hardware_key": "possession",
    "fido2": "possession",
    "biometric": "inherence",
}

_PHISHING_RESISTANT = {"hardware_key", "fido2"}


def _category_of(factor: str) -> Optional[str]:
    return _CATEGORY.get(factor)


def solve(factors: List[str]) -> str:
    if not factors:
        return "single_factor"

    distinct_categories = set()
    has_phishing_resistant = False

    for factor in factors:
        category = _category_of(factor)
        if category is None:
            continue
        distinct_categories.add(category)
        if factor in _PHISHING_RESISTANT:
            has_phishing_resistant = True

    if len(distinct_categories) < 2:
        return "single_factor"

    if has_phishing_resistant:
        return "mfa_phishing_resistant"

    return "mfa_phishable"
