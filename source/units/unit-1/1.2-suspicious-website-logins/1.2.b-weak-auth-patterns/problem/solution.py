COMMON_WORDS = {
    "password", "password1", "password123", "123456", "123456789", "12345678",
    "qwerty", "qwerty123", "letmein", "iloveyou", "admin", "welcome",
    "monkey", "dragon", "master", "abc123", "sunshine", "princess",
    "shadow", "superman", "football", "baseball", "login", "passw0rd",
    "pa$$word", "access", "mustang", "1234567890", "starwars", "hello",
}


def solve(password: str) -> dict:
    reasons = []

    if len(password) < 12:
        reasons.append("too_short")

    if password.lower() in COMMON_WORDS:
        reasons.append("in_dictionary")

    if password and password.isalpha() and password == password.lower():
        reasons.append("only_lowercase")

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
