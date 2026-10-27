# Interface, 2.1.b-threat-actor-classifier (blackbox contract, human-readable)

Any implementation that satisfies this interface can be swapped in (reference, student, or composite) and must pass `tests.py` unchanged.

## Entry point
```python
def solve(logs: list) -> dict:
```

## Input (`logs`)
A list of dictionaries, where each dictionary represents an alert log:
```python
[
    {"id": "ALT-101", "log": "Detected a zero-day exploit and quiet rootkit installation targeting research databases."},
    {"id": "ALT-102", "log": "Attacker ran an automated scan looking for default passwords on port 80."}
]
```

## Output (`result`)
A dictionary mapping each alert ID to its classified threat actor category:
```python
{
    "ALT-101": "Nation-State / APT",
    "ALT-102": "Script Kiddie"
}
```

## Guarantees / rules
- Pure function, deterministic, no I/O, no network.
- Standard library only.
- Categorization is based on substring matches (case-insensitive) in the `log` text:
  - **Nation-State / APT**: `"zero-day"`, `"state-sponsored"`, `"espionage"`, `"sabotage"`, `"rootkit"`, `"lateral movement"`, `"exfiltrat"`
  - **Cybercriminal**: `"ransomware"`, `"bitcoin"`, `"payment"`, `"extortion"`, `"payroll"`, `"fraud"`, `"financial"`
  - **Hacktivist**: `"protest"`, `"deface"`, `"ideolog"`, `"political"`, `"publicity"`, `"equity"`
  - **Insider Threat**: `"employee"`, `"disgruntled"`, `"exit interview"`, `"insider"`, `"negligent"`, `"usb"`
  - **Script Kiddie**: `"script kiddie"`, `"coin-miner"`, `"coinminer"`, `"default password"`, `"port scan"`, `"ftp exploit"`, `"automated scan"`
- If multiple categories match a log, prioritize the classification in this order:
  1. `"Nation-State / APT"`
  2. `"Cybercriminal"`
  3. `"Hacktivist"`
  4. `"Insider Threat"`
  5. `"Script Kiddie"`
- If no keywords match, the classification should be `"Unknown"`.

## Acceptance
`python -m pytest tests.py -q` passes (visible + hidden cases).
