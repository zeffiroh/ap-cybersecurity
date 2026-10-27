# Coding problem, 3.1.d: Packet capture credential-leak detector

**Skill:** Detect Attacks · **Maps to:** 3.1.B, 3.1.C · **Language:** Python 3 (pytest)

## Problem
You are triaging a captured packet log at Crestfield Analytics. For each entry, determine whether
it exposes a plaintext credential ("LEAK") or not ("SAFE"):

- **Encrypted ports are always "SAFE"**, regardless of payload content: port `443` (HTTPS) and
  port `22` (SSH) encrypt their payload, so nothing in the payload text can be treated as an
  actual leaked credential.
- **Cleartext-capable ports** are `80` (HTTP), `23` (Telnet), and `21` (FTP). An entry on one of
  these ports is **"LEAK"** if its payload contains any credential indicator string (case-sensitive
  substring match), otherwise it is **"SAFE"**.
- Credential indicator strings to check for (substring match anywhere in the payload):
  `"password="`, `"Password:"`, `"PASS "`.
- Any other port not listed above is treated as `"SAFE"` (out of scope for this detector).

## Function contract
Implement `solve(packets)` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
- `packets`: `list[dict]`, each with:
  - `"port"`: `int`, destination port
  - `"payload"`: `str`, the captured payload text

## Output
A `list[str]` of classifications, **one per input packet, in the same order as the input**. Each
entry is one of `"LEAK"`, `"SAFE"`.

## Examples
```python
packets = [
    {"port": 80, "payload": "POST /login HTTP/1.1\r\n\r\nuser=alice&password=Pass123!"},
    {"port": 443, "payload": "\\x16\\x03\\x03 encrypted application data"},
]
solve(packets)  ->  ["LEAK", "SAFE"]

packets2 = [
    {"port": 23, "payload": "login: admin\r\nPassword: R0uterAdmin!"},
    {"port": 80, "payload": "GET /index.html HTTP/1.1"},
]
solve(packets2)  ->  ["LEAK", "SAFE"]
```

## Constraints
- Deterministic, offline, standard library only.
- Port check first: if `port` is `443` or `22`, the result is always `"SAFE"`.
- Otherwise, if `port` is `80`, `23`, or `21`: check for any of `"password="`, `"Password:"`,
  `"PASS "` as a substring of `payload`; if found, `"LEAK"`, else `"SAFE"`.
- Any other port: always `"SAFE"`.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
