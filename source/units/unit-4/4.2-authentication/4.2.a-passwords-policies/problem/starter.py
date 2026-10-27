"""Starter code for 4.2.a. Student completes the TODO.
This file intentionally FAILS the tests until implemented."""


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
    # TODO: implement per prompt.md
    raise NotImplementedError("implement validate_password() — see prompt.md")
