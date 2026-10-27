"""Reference solution for 4.3.c. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""


def solve(vulns: list) -> list:
    """Assign an urgency label to each vulnerability per the patch-triage priority rules.

    Args:
        vulns: list of dicts with keys id (str), cvss (float), exploited_in_wild (bool),
            internet_facing (bool), end_of_life (bool).

    Returns:
        list of dicts, same order, each {"id": ..., "urgency": ...} where urgency is one of
        "emergency", "scheduled", "routine", "compensate".
    """
    results = []
    for v in vulns:
        vid = v["id"]
        cvss = v.get("cvss", 0.0)
        exploited = v.get("exploited_in_wild", False)
        internet_facing = v.get("internet_facing", False)
        end_of_life = v.get("end_of_life", False)

        if end_of_life:
            urgency = "compensate"
        elif exploited and internet_facing:
            urgency = "emergency"
        elif cvss >= 9.0 and internet_facing:
            urgency = "emergency"
        elif cvss >= 9.0:
            urgency = "scheduled"
        elif cvss >= 7.0 and internet_facing:
            urgency = "scheduled"
        else:
            urgency = "routine"

        results.append({"id": vid, "urgency": urgency})

    return results
