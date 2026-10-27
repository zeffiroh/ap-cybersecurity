"""Reference solution for 4.2.a. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""


def validate_password(password: str, policy: dict) -> list:
    """Validate a candidate password against a policy dict.

    Args:
        password: The candidate password string.
        policy: A dict describing the policy. Recognized keys (all optional):
            min_length (int, default 0)          — minimum required length.
            require_upper (bool, default False)  — require an uppercase letter.
            require_lower (bool, default False)  — require a lowercase letter.
            require_digit (bool, default False)  — require a digit.
            require_symbol (bool, default False) — require a non-alphanumeric symbol.
            banned_list (list[str], default [])  — forbidden/breached passwords,
                matched case-insensitively.
            history (list[str], default [])      — previously used passwords, matched
                case-sensitively (exact match) to prevent reuse.

    Returns:
        A list of violated rule-name strings, in this fixed order:
        ["too_short", "no_upper", "no_lower", "no_digit", "no_symbol",
         "in_banned_list", "reused_password"]. Only the names of violated rules
        are included. Returns [] if the password is fully compliant.
    """
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
