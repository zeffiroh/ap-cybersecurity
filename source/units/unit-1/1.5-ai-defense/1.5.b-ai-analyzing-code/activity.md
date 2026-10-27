# In-class activity, 1.5.b AI analyzing code for vulnerabilities

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students practice reading Python code with a security analyst's eye: identifying dangerous
patterns, naming the vulnerability class each pattern creates, and explaining why AI scanning
cannot replace human code review. Ties to LO 1.5.A (explain how AI tools support vulnerability
detection in code).

## Materials (all local)
- the SimLab simulation on each machine.
- Code snippets below (printed or displayed).

## Code snippets for review

**Snippet A, authentication module**
```python
import hashlib, pickle

def verify_user(username, token_bytes):
    user = pickle.loads(token_bytes)          # deserialize session
    pw_hash = hashlib.md5(user['pw'].encode()).hexdigest()
    password = "fallback_admin"               # emergency access
    return pw_hash == user['hash']
```

**Snippet B, command runner**
```python
import os, subprocess

def run_scan(target):
    os.system("nmap -sV " + target)
    result = subprocess.run("ping " + target, shell=True, capture_output=True)
    return result.stdout
```

**Snippet C, data processor**
```python
import json

def process_request(payload_str):
    data = json.loads(payload_str)
    name = data.get("name", "")
    value = data.get("value", 0)
    return {"name": name, "doubled": value * 2}
```

## Steps
1. Each pair reads Snippet A. List every dangerous pattern and the vulnerability tag it would
   get from a scanner (e.g., `vuln:pickle_loads`). Write one sentence per finding: what could
   an attacker do to exploit it?
2. Repeat for Snippet B. Note that BOTH os.system and subprocess shell=True appear, explain
   why both are flagged even though they do similar things.
3. Read Snippet C. The scanner finds zero findings. Discuss: does "no findings" mean "secure"?
   What other vulnerabilities might exist that static analysis cannot detect?
4. Open the simulation and reach the target score in the code review simulation.

## Collaborate (AP skill 4)
Assign roles: one partner is the "AI scanner" (applies the rule set mechanically), the other is
the "security engineer" (reviews each finding and drafts the fix). The engineer must justify every
fix: what is the safer replacement for each dangerous pattern?

## Exit ticket
Each student submits: one vulnerable code snippet they found + the tag + one sentence describing
the safer replacement (e.g., "replace md5 with sha256 for password hashing").

## Instructor notes
- Snippet A: expected tags are vuln:pickle_loads, vuln:md5, vuln:hardcoded_password.
- Snippet B: expected tags are vuln:os_system, vuln:subprocess_shell.
- Snippet C: zero findings, use this to drive the "static analysis has limits" discussion.
  Business-logic bugs, insecure deserialization with json (usually safe), authorization gaps, none are caught by pattern matching.
- Common stumble: students may flag `hashlib` import as suspicious. It is not a finding; only
  the use of md5() within it triggers the rule.
- Feeds the unit project (secure code review for the scenario's web application) and the scenario
  stage where attackers exploit a pickle endpoint.
