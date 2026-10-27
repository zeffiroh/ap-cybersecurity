# In-class activity, 1.5.c AI suggesting detection rules

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students practice the detection-engineering loop: read a log stream, identify suspicious
patterns manually, propose rule strings, then verify their rules against the sim and the coding
problem. Ties to LO 1.5.A (explain how AI-assisted tools generate and apply detection rules).

## Materials (all local)
- the SimLab simulation on each machine, or the printed log excerpt below.
- `problem/`, student implements `solve()` as part of the activity.

## Printed log excerpt (if devices unavailable)
```
ts=0   src=10.0.0.5  event=login_fail
ts=8   src=10.0.0.5  event=login_fail
ts=17  src=10.0.0.5  event=login_fail
ts=25  src=10.0.0.5  event=login_fail
ts=33  src=10.0.0.5  event=login_fail
ts=41  src=10.0.0.5  event=login_fail
ts=0   src=172.16.1.9 event=login_fail
ts=200 src=172.16.1.9 event=login_fail
ts=5   src=10.0.0.7  event=login_ok
ts=90  src=10.0.0.3  event=login_fail
ts=100 src=10.0.0.3  event=login_fail
```

## Steps
1. **Manual scan (8 min).** Each pair reads the printed log or the sim's log stream and marks
   every IP they think is suspicious. They write down a plain-English rule: "Flag IP X because
   it had N failures in Y seconds."

2. **Rule formalization (5 min).** Convert each plain-English rule into the structured format
   defined in `interface.md`:
   `ALERT brute_force src=<IP> count=<N> window=60s`
   Decide which IPs to include and which to exclude, and justify each decision.

3. **Sim verification (7 min).** Open the simulation. Step through the log stream and observe which
   IPs the engine flags. Compare to your manual findings. Note any discrepancies.

4. **Discussion (5 min).** Answer: If you lowered the threshold from 5 to 2, what would change?
   If you raised it to 10? Which threshold produces the best outcome for a real SOC?

## Collaborate (AP skill 4)
Assign roles: one partner is the **AI engine** (applies the rule mechanically, counts events),
the other is the **analyst** (decides whether each flagged IP is actually suspicious or a known
safe host). Swap roles between the printed and sim exercises.

## Exit ticket
Each student submits:
- The rule string(s) they generated for the printed log.
- One sentence explaining why the threshold value matters and what goes wrong when it is set too
  low or too high.

## Instructor notes
- Expected flagged IP from printed log: `10.0.0.5` (6 failures within 41s, well inside 60s window).
- `172.16.1.9` has only 2 failures spread 200s apart -- below threshold, correct answer is no rule.
- `10.0.0.3` has only 2 failures total -- no rule.
- Common stumble: students count all failures ever rather than within a rolling window. Use the
  sim to show what the window-based count looks like.
- Feeds the unit project (threat detection pipeline) and scenario stage 3 (SOC triage).
