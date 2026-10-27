# In-class activity, 2.2.c Device theft and tampering

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Pairs act as the IT security triage desk, reviewing a stack of device incident reports (thefts
and tampering findings) and assigning each a risk level with a justification tied to encryption
status, seal status, and detection delay. Ties to LO 2.2.B, 2.2.C and the course skill Analyze
Risk.

## Materials (all local)
- the SimLab simulation on each machine, or the printed incident sheet below.
- One copy of the incident sheet per pair (print or display on screen).

## Incident sheet (print or project)

| # | Type | Encrypted? | Seal intact? | Sensitive data? | Hours since check | Risk level | Justification |
|---|------|-----------|--------------|-----------------|--------------------|-----------|----------------|
| 1 | theft | No | Yes | Yes | 2 | ? | ? |
| 2 | theft | Yes | Yes | Yes | 70 | ? | ? |
| 3 | theft | Yes | Yes | No | 100 | ? | ? |
| 4 | tampering | Yes | No | No | 3 | ? | ? |
| 5 | tampering | Yes | Yes | No | 60 | ? | ? |
| 6 | tampering | Yes | Yes | No | 12 | ? | ? |

## Steps
1. (5 min) Each pair reads incidents 1-3 (theft reports) independently and writes their risk
   level and one-sentence justification for each.
2. (5 min) Partners compare answers. Where they disagree, each must defend their call by citing
   the specific rule (encryption status, sensitivity, hours since check). Reach consensus.
3. (5 min) Repeat for incidents 4-6 (tampering reports), paying attention to why incident 5 is
   riskier than incident 6 despite both having an intact seal.
4. (5 min) Each pair opens the simulation and checks their triage decisions against the sim's scoring
   for equivalent scenarios; revise any incorrect calls and note which rule they misapplied.

## Collaborate (AP skill 4)
Assign roles: one partner is the "incident responder" (assigns the risk level and decides who to
notify), the other is the "policy auditor" (checks whether the responder's justification actually
matches the written rule rather than a gut feeling). For incident 5, the pair must specifically
discuss why an intact seal is not sufficient evidence that no tampering occurred. Swap roles
halfway through.

## Exit ticket
Each student writes one sentence: "Incident X is [risk level] because [rule applied], and
[control] would have reduced the risk by [mechanism]."

## Answer key (instructor only)

| # | Risk level | Justification |
|---|-----------|----------------|
| 1 | HIGH | Device not encrypted, data is exposed with no cryptographic barrier regardless of anything else. |
| 2 | MEDIUM | Encrypted, but sensitive data and 70 hours since check exceeds the 48-hour threshold, long detection delay raises risk. |
| 3 | LOW | Encrypted and not flagged as sensitive; long delay does not matter because the sensitivity condition is not met. |
| 4 | HIGH | Seal not intact, direct physical evidence the enclosure was opened. |
| 5 | MEDIUM | Seal intact, but 60 hours since check exceeds the 48-hour threshold, tampering that doesn't require opening the case (e.g., USB implant) could have gone unnoticed that long. |
| 6 | LOW | Seal intact and only 12 hours since check, within the normal monitoring window. |

## Instructor notes
- Timing: incidents 1 and 4 are unambiguous HIGH cases (clear rule violation); 2/5 are the
  intended teaching moment for the "detection delay" MEDIUM rule; 3/6 are the LOW baseline.
- Common stumble: students want to mark incident 3 as MEDIUM because "it was a theft," without
  checking that `contains_sensitive_data` is `False`, the MEDIUM rule for theft requires both
  conditions (sensitive AND long delay), not just a long delay.
- Reinforce that an intact seal is reassuring but not proof of no tampering, which is why the
  hours-since-check rule exists independently of the seal check.
- Feeds the unit project (threat modeling a small network/facility) and connects forward to 2.3
  (protecting physical spaces) and 2.4 (detecting physical attacks).
