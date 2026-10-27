"""Reference solution for 2.2.b. MUST pass 100% of tests.py.
Also the default 'blackbox' implementation students can swap out (see blackbox.yaml)."""


def _power_severity(value: float) -> str:
    if value == 0 or value < 90 or value > 110:
        return "CRITICAL"
    if (90 <= value < 95) or (105 < value <= 110):
        return "WARNING"
    return "NORMAL"


def _temperature_severity(value: float) -> str:
    if value > 30:
        return "CRITICAL"
    if (27 < value <= 30) or value < 15:
        return "WARNING"
    return "NORMAL"


def _humidity_severity(value: float) -> str:
    if value > 70 or value < 20:
        return "CRITICAL"
    if (60 < value <= 70) or (20 <= value < 40):
        return "WARNING"
    return "NORMAL"


def _binary_severity(value: float) -> str:
    return "CRITICAL" if value > 0 else "NORMAL"


_RANK = {"NORMAL": 0, "WARNING": 1, "CRITICAL": 2}


def solve(data: list[dict]) -> dict[str, str]:
    severities: dict[str, str] = {}

    for reading in data:
        rid = reading["id"]
        rtype = reading["type"]
        value = reading["value"]

        if rtype == "power":
            severities[rid] = _power_severity(value)
        elif rtype == "temperature":
            severities[rid] = _temperature_severity(value)
        elif rtype == "humidity":
            severities[rid] = _humidity_severity(value)
        elif rtype in ("smoke", "water"):
            severities[rid] = _binary_severity(value)
        else:
            severities[rid] = "NORMAL"

    # Combined-signal escalation: per room, if a temperature reading and a humidity
    # reading are both at least WARNING, escalate both to CRITICAL.
    rooms: dict[str, dict[str, list[str]]] = {}
    for reading in data:
        room = reading["room"]
        rtype = reading["type"]
        if rtype in ("temperature", "humidity"):
            rooms.setdefault(room, {}).setdefault(rtype, []).append(reading["id"])

    for room, by_type in rooms.items():
        temp_ids = by_type.get("temperature", [])
        hum_ids = by_type.get("humidity", [])
        temp_elevated = any(_RANK[severities[i]] >= _RANK["WARNING"] for i in temp_ids)
        hum_elevated = any(_RANK[severities[i]] >= _RANK["WARNING"] for i in hum_ids)
        if temp_elevated and hum_elevated:
            for i in temp_ids:
                if _RANK[severities[i]] >= _RANK["WARNING"]:
                    severities[i] = "CRITICAL"
            for i in hum_ids:
                if _RANK[severities[i]] >= _RANK["WARNING"]:
                    severities[i] = "CRITICAL"

    return severities
