# Coding problem, 4.4.a: EDR telemetry analyzer

**Skill:** Detect Attacks · **Maps to:** 4.4.A · **Language:** Python 3 (pytest)

## Problem
An EDR agent streams process-event telemetry from an endpoint. Each event records a process, its
parent process, whether it opened an external network connection, and how many bytes it
transferred. Build the analyzer that flags processes exhibiting either of the two classic
red flags an EDR platform's behavioral detection looks for: a "living off the land" parent-child
relationship, or unusual outbound data transfer.

## Function contract
Implement `def solve(events: list) -> list` in `starter.py` (see `interface.md` / `blackbox.yaml`).

## Input
A list of dicts, each with keys `pid` (int), `process` (str), `parent_process` (str),
`external_connection` (bool), `bytes_transferred` (int).

## Output
A sorted list of `pid` (int) for every event that is flagged.

## Detection rules (a process is flagged if EITHER rule fires)
1. **Living-off-the-land parent-child pair:** `process` (case-insensitive) is one of the script
   interpreters `{"powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe", "mshta.exe"}` AND
   `parent_process` (case-insensitive) is **not** `"explorer.exe"` (the only parent considered a
   normal, user-initiated launch of an interpreter). Any other parent, including
   `winword.exe`, `outlook.exe`, `svchost.exe`, or a browser, is treated as suspicious, matching
   the living-off-the-land pattern where a document or script silently spawns a shell.
2. **Unusual outbound transfer:** `external_connection` is `True` AND `bytes_transferred > 1000000`
   (strictly greater than 1,000,000 bytes).

## Examples
```
[{"pid": 501, "process": "powershell.exe", "parent_process": "winword.exe",
  "external_connection": True, "bytes_transferred": 500},
 {"pid": 502, "process": "chrome.exe", "parent_process": "explorer.exe",
  "external_connection": True, "bytes_transferred": 200000},
 {"pid": 503, "process": "backup.exe", "parent_process": "explorer.exe",
  "external_connection": True, "bytes_transferred": 5000000}]
    -> [501, 503]
```
*(pid 501 flagged for the living-off-the-land parent; pid 503 flagged for excessive outbound
transfer; pid 502 is a normal browser launch under the transfer threshold.)*

## Constraints
- Deterministic, offline, standard library only.
- Case-insensitive matching of process/parent names.
- Return a de-duplicated, ascending-sorted list of pids (each pid appears at most once even if
  both rules fire).
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
