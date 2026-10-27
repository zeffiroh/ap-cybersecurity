# In-class activity, 4.4.c Identifying compromised devices (indicators of compromise)

**Format:** small group · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as an incident-response triage team: given a set of IOCs observed on several devices,
they compute a weighted compromise score by hand and decide a verdict and response action for
each device. Ties to LO 4.4.B and 4.4.C (combining multiple IOCs into a compromise decision).

## Materials (all local)
- the SimLab simulation / `problem/` / printed IOC weight table and device cards below.

## IOC weight table (printed reference)
| IOC type | Weight |
|---|---|
| Known-malicious file hash match | 6 |
| Antivirus/EDR disabled | 5 |
| New unauthorized admin account | 4 |
| Unusual outbound traffic | 3 |
| Unexpected scheduled task | 3 |
| Registry run-key persistence added | 2 |
| Cluster of failed logins | 1 |

Verdict thresholds: score < 4 = **clean**; 4-7 = **suspicious**; score >= 8 = **compromised**.

## Device cards
- **Device A:** antivirus disabled (5) + new unauthorized admin account (4).
- **Device B:** cluster of failed logins (1) only.
- **Device C:** known-malicious file hash match (6) + unusual outbound traffic (3) + registry
  run-key persistence added (2).
- **Device D:** unexpected scheduled task (3).
- **Device E:** new unauthorized admin account (4) + cluster of failed logins (1).

## Steps
1. **Score each device (10 min).** Each group sums the weights for Devices A-E using the table
   above and assigns a verdict (clean / suspicious / compromised).
2. **Check with the simulation (5 min).** Open the simulation and work through its device-triage queue to
   confirm your scores and verdicts.
3. **Response plan (10 min).** For every device scored "compromised," write the response action
   you would take (referencing the EDR response actions from 4.4.a: alert, kill process,
   quarantine, isolate). For every "suspicious" device, write what ADDITIONAL evidence you would
   look for before escalating.

## Collaborate (AP skill 4)
Assign roles: one member is the "Triage Analyst" (computes scores), one is the "Incident
Commander" (decides the response action for each verdict), and one is the "Skeptic" (challenges
whether a single IOC is being over-weighted or whether the group jumped to a conclusion too
fast). Reach group consensus on all five devices.

## Exit ticket
Each student submits: Device C's total score, its verdict, and one sentence justifying why three
weaker-looking IOCs combined outweigh one strong IOC in isolation (or vice versa, if applicable).

## Instructor notes
- Expected scores/verdicts: A = 9 (compromised), B = 1 (clean), C = 11 (compromised), D = 3
  (clean), E = 5 (suspicious).
- Common stumble: students assume any device with 2+ IOCs must be "compromised." Emphasize that
  the threshold is score-based, not count-based, Device E has two IOCs but is only
  "suspicious" because neither weight is very high.
- Device B and D are deliberate "clean" traps: a single low-weight IOC alone should not trigger
  an escalation, reinforcing the misconception correction in `atom.md`.
- Feeds the coding problem's exact weighted-scoring logic and reinforces the unit's EDR (4.4.a)
  response-action vocabulary.
