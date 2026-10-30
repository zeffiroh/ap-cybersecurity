def validate_password(password: str, policy: dict) -> list:
    min_length = policy.get("min_length", 0)
    require_upper = policy.get("require_upper", False)
    require_lower = policy.get("require_lower", False)
    require_digit = policy.get("require_digit", False)
    require_symbol = policy.get("require_symbol", False)
    banned_list = policy.get("banned_list", [])
    history = policy.get("history", [])

    violations = []

    if len(password) < min_length:
        violations.append("too_short")

    if require_upper and not any(c.isupper() for c in password):
        violations.append("no_upper")

    if require_lower and not any(c.islower() for c in password):
        violations.append("no_lower")

    if require_digit and not any(c.isdigit() for c in password):
        violations.append("no_digit")

    if require_symbol and not any(not c.isalnum() for c in password):
        violations.append("no_symbol")

    if any(password.lower() == banned.lower() for banned in banned_list):
        violations.append("in_banned_list")

    if any(password == prior for prior in history):
        violations.append("reused_password")

    return violations
