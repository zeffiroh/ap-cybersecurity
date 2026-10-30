def solve(vulns: list) -> list:
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
