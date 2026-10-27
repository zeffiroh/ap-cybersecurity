# Coding problem, 3.1.a: TCP/IP fundamentals and network topology flaws

**Skill:** Analyze Risk · **Maps to:** 3.1.A · **Language:** Python 3 (pytest)

## Problem
A network monitoring tool has captured a log of IP packets on a corporate subnet. Each log entry
records the packet's source IP, destination IP, and an expected source subnet (CIDR notation).
Your job is to implement a spoofing detector: given a list of packet records, return the
zero-based indices of packets whose source IP address falls outside the expected source subnet,
which is a strong indicator of IP spoofing.

A packet is considered suspicious (spoofed) when `src_ip` does not belong to `expected_subnet`.
Only IPv4 addresses are present. Subnets are given as `"A.B.C.D/N"` CIDR strings.

## Function contract
Implement `solve(packets: list[dict]) -> list[int]` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A list of dicts. Each dict has three string keys:
- `"src_ip"`, e.g. `"10.0.1.55"`
- `"dst_ip"`, e.g. `"10.0.1.1"`
- `"expected_subnet"`, e.g. `"10.0.1.0/24"`

## Output
A sorted list of zero-based integer indices of the suspicious (spoofed) packets. Empty list if
none are suspicious.

## Examples
```
[{"src_ip": "10.0.1.55",  "dst_ip": "10.0.1.1", "expected_subnet": "10.0.1.0/24"},
 {"src_ip": "192.168.5.9","dst_ip": "10.0.1.1", "expected_subnet": "10.0.1.0/24"},
 {"src_ip": "10.0.1.200", "dst_ip": "10.0.1.1", "expected_subnet": "10.0.1.0/24"}]
-> [1]          # packet at index 1 has src_ip outside 10.0.1.0/24

[]  ->  []      # empty log: nothing to flag
```

## Constraints
- Deterministic, offline, standard library only (`ipaddress` module is standard library).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
