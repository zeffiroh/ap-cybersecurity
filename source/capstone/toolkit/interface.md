# Interface, mhsec toolkit (blackbox contract)

Each tool is a pure, deterministic, offline function over the Meridian world (see `world/`).
A student reimplementation must keep these signatures and pass `source/capstone/tests`.

## recon(network: dict) -> list[dict]
Return sorted (by ip) findings for every DMZ host plus any host exposing a risky service
(`telnet, dicom, ftp, ssh`). Each finding: `{ip, name, subnet, risky_services: [sorted]}`.

## detect_spray(auth_logs: list[dict], min_users=5, min_fails=20) -> list[dict]
A src_ip with failed logins across >= min_users distinct users AND >= min_fails total failures is
a spray source. Return `[{src_ip, users, fails}]` sorted by (-fails, src_ip).

## find_phish(emails: list[dict], legit_domain='meridian-health.org') -> list[dict]
Flag emails by indicator (not the synthetic `malicious` field). Indicators:
`lookalike-domain` (sender domain != legit but contains "meridian"), `urgency`, `authority`,
`credential-link` (http link containing "verify"/"owa"). Return `[{id, from, to, indicators:[sorted]}]`
sorted by id, only for emails with >= 1 indicator.

## ir_timeline(emails, auth_logs, meta) -> dict
Reconstruct: `{victim, entry_email, lookalike_domain, compromised_login_src, recommendation:[...]}`.
entry_email = the lookalike-domain phish; compromised_login_src = the victim's `geo=="unusual"` login.

## Acceptance
From `source/capstone/`: `python -m pytest tests -q` (all green).
