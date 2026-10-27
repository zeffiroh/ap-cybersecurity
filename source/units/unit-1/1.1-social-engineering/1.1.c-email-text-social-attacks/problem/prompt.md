# Coding problem, 1.1.c: Phishing indicator extractor

**Skill:** Analyze Risk, Detect Attacks · **Maps to:** 1.1.A, 1.1.C · **Language:** Python 3 (pytest)

## Problem
Build the indicator extractor a security-awareness tool would use to screen incoming messages
across channels. Given a message dict with channel, sender, text, and link fields, return
the sorted list of phishing indicator labels that the message triggers.

A message may trigger zero, one, or several indicators. The result is the sorted, de-duplicated
list of triggered label strings.

## Function contract
Implement `solve(message: dict) -> list[str]` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A dict with the following keys (all strings):
- `"channel"`, one of `"email"`, `"sms"`, `"dm"` (social media direct message)
- `"sender"`, the sender address, phone number, or handle
- `"text"`, the message body text
- `"link"`, a URL or empty string

## Output
A **sorted, de-duplicated** `list[str]` drawn from the five indicator labels:
- `"lookalike-domain"`, sender contains a mangled brand domain
- `"urgent-money-request"`, text requests an urgent financial transaction
- `"credential-request"`, text requests credentials or account verification
- `"mismatched-sender"`, text claims a brand the sender address does not belong to
- `"shortened-link"`, link uses a URL shortener or bare IP address

See `interface.md` for the precise indicator rule sets.

## Examples
```python
{
  "channel": "email",
  "sender": "security@paypa1.com",
  "text": "Verify your PayPal account now.",
  "link": ""
}
-> ["credential-request", "lookalike-domain", "mismatched-sender"]

{
  "channel": "sms",
  "sender": "+1-555-0192",
  "text": "Reminder: dentist at 2pm tomorrow. Reply YES.",
  "link": ""
}
-> []

{
  "channel": "email",
  "sender": "ceo@corp-executive.net",
  "text": "Wire $50k today, do not loop in finance, keep this confidential.",
  "link": ""
}
-> ["urgent-money-request"]

{
  "channel": "dm",
  "sender": "@IT_support99",
  "text": "Your account expires tonight, verify here.",
  "link": "http://192.168.1.1/login"
}
-> ["credential-request", "shortened-link"]

{
  "channel": "sms",
  "sender": "NETFLIX",
  "text": "Your Netflix payment failed. Update your payment at netflix.com/billing",
  "link": "https://bit.ly/3xAmPle"
}
-> ["credential-request", "shortened-link"]
```

## Constraints
- Deterministic, offline, standard library only.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
