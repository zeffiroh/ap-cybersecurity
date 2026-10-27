# In-class activity, 5.6.a Application monitoring and logging

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal
Pairs read a synthetic application log excerpt, identify which source IP is exhibiting
brute-force behavior, and state the exact rule that flags it. Ties to LO 5.6.A.

## Materials (all local)
- the SimLab simulation / `problem/` / printed log excerpt below.

## Steps
1. Each pair opens the simulation and works through the log-burst cases, deciding ALERT or OK for
   each source IP based on the >=5 failed logins / 60-second-window rule.
2. For one ALERT case, the pair writes the exact evidence: how many 401s, over what time span,
   from which IP.
3. The pair proposes one additional log field or signal (e.g. distinct usernames targeted, user
   agent string) that would make the alert even more confident, and explains why.

## Collaborate (AP skill 4)
Assign roles: a "log analyst" scans the burst for the qualifying window, and a "SIEM engineer"
states the alert rule in plain English and checks the analyst's math. Swap roles for the next case.

## Exit ticket
Each pair submits: the IP they flagged, the count/window evidence, and the one extra signal
they'd add to strengthen the alert.

## Instructor notes
- Expected reasoning: students should identify the qualifying 60-second window and count exactly
  5+ 401 events inside it, not just "a lot of failures somewhere in the log."
- Common stumble: students count all events in the whole log rather than checking whether any
  single 60-second window meets the threshold; walk through the sliding-window idea explicitly.
- Feeds the coding problem's brute-force detector and the unit's SOC-analyst framing.
