"""Reference solution for 1.2.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""

COMMON_WORDS = {
    "password", "password1", "password123", "123456", "123456789", "12345678",
    "qwerty", "qwerty123", "letmein", "iloveyou", "admin", "welcome",
    "monkey", "dragon", "master", "abc123", "sunshine", "princess",
    "shadow", "superman", "football", "baseball", "login", "passw0rd",
    "pa$$word", "access", "mustang", "1234567890", "starwars", "hello",
}


def solve(password: str) -> dict:
    """Return a weakness report dict for the given password.

    Returns:
        {"weak": bool, "reasons": list[str]} where reasons is a sorted list of
        triggered rule labels from {"too_short","in_dictionary","only_lowercase",
        "sequential_or_repeated"}.
    """
    reasons = []

    # Rule 1: too_short
    if len(password) < 12:
        reasons.append("too_short")

    # Rule 2: in_dictionary
    if password.lower() in COMMON_WORDS:
        reasons.append("in_dictionary")

    # Rule 3: only_lowercase
    # Triggered iff every character is a lowercase ASCII letter (non-empty)
    if password and password.isalpha() and password == password.lower():
        reasons.append("only_lowercase")

    # Rule 4: sequential_or_repeated
    # Scan every window of 3 consecutive characters
    triggered = False
    for i in range(len(password) - 2):
        a, b, c = password[i], password[i + 1], password[i + 2]
        oa, ob, oc = ord(a), ord(b), ord(c)
        if a == b == c:
            triggered = True
            break
        if ob - oa == 1 and oc - ob == 1:
            triggered = True
            break
    if triggered:
        reasons.append("sequential_or_repeated")

    reasons.sort()
    return {"weak": len(reasons) > 0, "reasons": reasons}
