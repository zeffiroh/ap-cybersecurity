# Coding problem, 1.5.b: AI analyzing code for vulnerabilities

**Skill:** Detect Attacks, Collaborate · **Maps to:** 1.5.A · **Language:** Python 3 (pytest)

## Problem
Build the pattern-matching core of an AI code security scanner. Given a string of Python source
code, return a sorted list of vulnerability tags for every dangerous pattern found. This is the
rule-evaluation layer that tools like Bandit and Semgrep implement under the hood.

## Function contract
Implement `solve(code: str) -> list[str]` in `starter.py` (see `interface.md` / `blackbox.yaml`).
Return a sorted, de-duplicated list of finding tag strings.

## Input
A single string, the entire source code to scan. May be multi-line or empty.

## Output
A sorted `list[str]` of vulnerability tags drawn from:
- `"vuln:eval"`
- `"vuln:hardcoded_password"`
- `"vuln:md5"`
- `"vuln:os_system"`
- `"vuln:pickle_loads"`
- `"vuln:subprocess_shell"`

## Examples
```
'result = eval(user_input)'
    -> ["vuln:eval"]

'os.system("ls " + path)\nsubprocess.run(cmd, shell=True)'
    -> ["vuln:os_system", "vuln:subprocess_shell"]

'import hashlib\nhashlib.md5(data)\npickle.loads(blob)'
    -> ["vuln:md5", "vuln:pickle_loads"]

'x = 1 + 2'
    -> []
```

## Constraints
- Deterministic, offline, standard library only.
- `password =` matching is case-insensitive; all other patterns are case-sensitive.
- Must pass all cases in `tests.py` (visible + hidden).

## How to run
```
cd problem && python -m pytest tests.py -q
```
