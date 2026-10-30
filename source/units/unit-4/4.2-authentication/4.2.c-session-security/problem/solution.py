def solve(report: str) -> str:
    if not isinstance(report, str):
        return "unknown"

    report_lower = report.lower()


    fixation_indicators = [
        "fixation", "pre-set session", "attacker-supplied session",
        "session id unchanged after login", "id unchanged", "session id before",
        "known session id", "id was already set"
    ]
    if any(ind in report_lower for ind in fixation_indicators):
        return "fixation"

    hijacking_indicators = [
        "sniffed", "sniffing", "intercepted", "stolen session", "stole the session",
        "replayed", "captured token", "plain http", "plaintext",
        "read by an injected script", "read via injected", "malware read the",
        "xss", "reused by an attacker"
    ]
    if any(ind in report_lower for ind in hijacking_indicators):
        return "hijacking"

    insecure_cookie_indicators = [
        "missing httponly", "no httponly", "httponly flag", "missing secure flag",
        "no secure flag", "missing samesite", "no samesite", "cookie has no",
        "cookie is missing", "readable from client-side javascript",
        "not set to httponly"
    ]
    if any(ind in report_lower for ind in insecure_cookie_indicators):
        return "insecure_cookie"

    timeout_indicators = [
        "no idle timeout", "no timeout", "without a timeout", "left unattended",
        "no absolute timeout", "never expires", "does not expire",
        "session never times out", "unattended for", "abandoned", "kiosk"
    ]
    if any(ind in report_lower for ind in timeout_indicators):
        return "timeout_issue"

    secure_indicators = [
        "regenerated at login", "session id regenerated", "secure, httponly",
        "all secure flags", "properly secured", "secure flags set",
        "set secure", "set httponly", "samesite=strict",
        "session expired automatically"
    ]
    if any(ind in report_lower for ind in secure_indicators):
        return "secure"

    return "unknown"
