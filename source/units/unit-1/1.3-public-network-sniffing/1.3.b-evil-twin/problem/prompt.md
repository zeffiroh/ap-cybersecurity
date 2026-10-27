# Coding problem, 1.3.b: Detect evil-twin access points

**Skill:** Analyze Risk, Detect Attacks · **Maps to:** 1.3.B · **Language:** Python 3 (pytest)

## Problem
A wireless scanner returns a list of detected access points. Each AP is a dict with keys:
- `ssid` (str), the human-readable network name
- `bssid` (str), the hardware MAC address of the radio (normalized to uppercase)
- `security` (str), one of `"OPEN"`, `"WEP"`, `"WPA"`, `"WPA2"`, `"WPA3"`
- `signal` (int), received signal strength in dBm (negative; stronger = closer to 0)

An AP is **suspicious** (potential evil twin) if ANY of the following holds:

1. **Duplicate SSID / multiple BSSIDs**, the same SSID is being broadcast by more than one
   BSSID in the scan. Every BSSID in such a group is flagged.
2. **Security downgrade**, an SSID appears with at least two different security levels and the
   AP in question does not have the strongest security level seen for that SSID. Those weaker
   entries are flagged.

Rules combine: an AP is flagged if either condition is true for it.

## Function contract
Implement `solve(aps: list[dict]) -> list[str]` in `starter.py`
(see `interface.md` / `blackbox.yaml`).

Return a **sorted, de-duplicated** list of suspicious BSSIDs.

## Input
A list of dicts, each with keys `ssid`, `bssid`, `security`, `signal`.
The list may be empty. BSSIDs are already uppercase.

## Output
A sorted list of BSSIDs (strings) that are suspicious. Empty list if none.

## Security ordering (weakest to strongest)
`OPEN` < `WEP` < `WPA` < `WPA2` < `WPA3`

## Examples
```
# Two APs share SSID "CafeGuest" — different BSSIDs -> both flagged (rule 1)
# The OPEN entry also has weaker security (rule 2)
aps = [
    {"ssid": "CafeGuest", "bssid": "AA:BB:CC:11:22:33", "security": "WPA2", "signal": -55},
    {"ssid": "CafeGuest", "bssid": "DE:AD:BE:EF:00:01", "security": "OPEN", "signal": -42},
    {"ssid": "HotelLobby","bssid": "11:22:33:44:55:66", "security": "WPA2", "signal": -65},
]
solve(aps) -> ["AA:BB:CC:11:22:33", "DE:AD:BE:EF:00:01"]

# Empty scan
solve([]) -> []

# Single SSID, single BSSID, no anomaly
solve([{"ssid": "HomeNet", "bssid": "00:11:22:33:44:55", "security": "WPA3", "signal": -50}]) -> []
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
