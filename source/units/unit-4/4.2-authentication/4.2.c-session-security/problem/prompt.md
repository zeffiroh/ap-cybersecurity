# Coding problem, 4.2.c: Classify session-security incidents

**Skill:** Mitigate Risk · **Maps to:** 4.2.B · **Language:** Python 3 (pytest)

## Problem
A security analyst receives short incident-report strings describing observed session behavior.
Build the classifier that maps each description to the correct session-security category.

Categories:
- `"hijacking"`, an already-authenticated session token is stolen (XSS read, network sniffing,
  malware) and reused by an attacker
- `"fixation"`, an attacker supplies a session ID to the victim before login, then reuses that
  same ID after the victim authenticates
- `"insecure_cookie"`, the session cookie is missing a secure attribute (HttpOnly, Secure, or
  SameSite) that would have prevented exposure or misuse
- `"timeout_issue"`, a session remains valid far longer than it should because of a missing or
  misconfigured idle/absolute timeout
- `"secure"`, the report describes a session that is properly protected (regeneration, secure
  flags, timeouts all present) with no vulnerability
- `"unknown"`, nothing in the report matches any category

A report may match exactly one category. If no category matches, return `"unknown"`.

## Function contract
Implement `solve(report: str) -> str` in `starter.py` (see `interface.md` / `blackbox.yaml`).
Return the single category label string. Matching is case-insensitive substring detection using
the indicator sets defined in `interface.md`.

## Input
A single string describing observed session behavior on a device, browser, or server.

## Output
One of: `"hijacking"`, `"fixation"`, `"insecure_cookie"`, `"timeout_issue"`, `"secure"`, `"unknown"`.

## Examples
```
"Session token was sniffed over unencrypted HTTP and replayed by an attacker"        -> "hijacking"
"Attacker sent a link with a pre-set session id; victim logged in and id unchanged"  -> "fixation"
"Session cookie has no HttpOnly flag configured; automated scan flagged the issue"    -> "insecure_cookie"
"Logged-in kiosk left unattended for hours with no idle timeout configured"          -> "timeout_issue"
"Session id regenerated at login; cookie set Secure, HttpOnly, SameSite=Strict"      -> "secure"
"User changed their display name in account settings"                                -> "unknown"
```

## Constraints
- Deterministic, offline, standard library only.
- Detection by case-insensitive substring match against indicator sets in `interface.md`.
- Exactly one label returned (string, not list).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
