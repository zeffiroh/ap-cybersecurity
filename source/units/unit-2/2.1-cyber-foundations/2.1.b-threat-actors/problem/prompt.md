# Coding problem, 2.1.b: Threat actor log classifier

**Skill:** Analyze Risk · **Maps to:** 2.1.B · **Language:** Python 3 (pytest)

## Problem
In this challenge, you will implement an automated log classifier for the security team at Meridian University. You are given a list of alert logs, each containing an ID and a text description. You must classify each alert to identify the most likely threat actor category responsible for the attack based on key phrases present in the logs.

## Function contract
Implement `solve(logs: list) -> dict` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A list of log entries:
```python
[
    {"id": "ALT-01", "log": "Ransomware deployed. Files encrypted. Payment of 2.5 BTC demanded."},
    {"id": "ALT-02", "log": "FTP scan detected. Automated port scan looking for vulnerabilities."}
]
```

## Output
A dictionary mapping log IDs to their threat actor classification:
```python
{
    "ALT-01": "Cybercriminal",
    "ALT-02": "Script Kiddie"
}
```

## Classification Rules
Match log descriptions (case-insensitive) using the keywords:
- **Nation-State / APT**: `"zero-day"`, `"state-sponsored"`, `"espionage"`, `"sabotage"`, `"rootkit"`, `"lateral movement"`, `"exfiltrat"`
- **Cybercriminal**: `"ransomware"`, `"bitcoin"`, `"payment"`, `"extortion"`, `"payroll"`, `"fraud"`, `"financial"`
- **Hacktivist**: `"protest"`, `"deface"`, `"ideolog"`, `"political"`, `"publicity"`, `"equity"`
- **Insider Threat**: `"employee"`, `"disgruntled"`, `"exit interview"`, `"insider"`, `"negligent"`, `"usb"`
- **Script Kiddie**: `"script kiddie"`, `"coin-miner"`, `"coinminer"`, `"default password"`, `"port scan"`, `"ftp exploit"`, `"automated scan"`

Conflict Resolution:
If multiple rules match, prioritize in this order:
1. `Nation-State / APT`
2. `Cybercriminal`
3. `Hacktivist`
4. `Insider Threat`
5. `Script Kiddie`

If none matches, return `"Unknown"`.

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py`.

## How to run
```bash
cd problem && python -m pytest tests.py -q
```
