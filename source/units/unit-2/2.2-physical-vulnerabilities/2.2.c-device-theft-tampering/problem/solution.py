"""Reference solution for 2.2.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""


def _theft_risk(incident: dict) -> str:
    if not incident["encrypted"]:
        return "HIGH"
    if incident["contains_sensitive_data"] and incident["hours_since_check"] > 48:
        return "MEDIUM"
    return "LOW"


def _tampering_risk(incident: dict) -> str:
    if not incident["seal_intact"]:
        return "HIGH"
    if incident["hours_since_check"] > 48:
        return "MEDIUM"
    return "LOW"


def solve(data: list[dict]) -> dict[str, str]:
    results = {}
    for incident in data:
        rid = incident["id"]
        itype = incident["type"]
        if itype == "theft":
            results[rid] = _theft_risk(incident)
        elif itype == "tampering":
            results[rid] = _tampering_risk(incident)
        else:
            results[rid] = "LOW"
    return results
