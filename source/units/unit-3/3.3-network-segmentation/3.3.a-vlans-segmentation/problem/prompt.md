# Coding problem, 3.3.a: VLAN segmentation flow filter

**Skill:** Mitigate Risk · **Maps to:** 3.3.A · **Language:** Python 3 (pytest)

## Problem
A network switch enforces VLAN segmentation using the following default-deny policy:

- Traffic between two hosts **on the same VLAN** is **allowed**.
- Traffic from VLAN 20 (Employee) to VLAN 30 (Server) is **allowed** (business policy exception).
- All other cross-VLAN traffic is **blocked**.

Given a mapping of host names to VLAN IDs and a list of traffic flows, return the list of flows that are **blocked** by these rules.

## Function contract
Implement `solve(vlan_map: dict, flows: list) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `vlan_map`: `dict[str, int]`, maps each host name to its VLAN ID (integer).
- `flows`: `list[tuple[str, str]]`, each tuple is `(src_host, dst_host)`.

## Output
A `list[tuple[str, str]]` of flows that are blocked, in the same order they appear in the input. Do not include allowed flows.

## Examples
```
vlan_map = {"WS-01": 20, "SRV-01": 30, "GUEST-01": 40, "MGMT-01": 10}
flows = [("WS-01","SRV-01"), ("GUEST-01","SRV-01"), ("WS-01","WS-01")]

solve(vlan_map, flows)
-> [("GUEST-01","SRV-01")]
# WS-01->SRV-01: VLAN 20->30, allowed by business exception
# GUEST-01->SRV-01: VLAN 40->30, blocked (no exception)
# WS-01->WS-01: same VLAN, allowed
```

## Constraints
- Deterministic, offline, standard library only.
- All host names in `flows` are guaranteed to be in `vlan_map`.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
