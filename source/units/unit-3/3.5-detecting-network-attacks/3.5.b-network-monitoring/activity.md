# In-class activity, 3.5.b Network monitoring and traffic analysis

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students compare a printed traffic baseline against an observed traffic window for a small set of
Meridian High School hosts and identify which hosts show a genuine anomaly (unusual port, volume
spike, or beaconing pattern) versus which are within normal variation. Ties to LO 3.5.B (read flow
data, apply a baseline, identify monitoring indicators of compromise).

## Materials (all local)
- the SimLab simulation on each machine, or the printed baseline/observed tables below.

## Steps
1. **Read the baseline (5 min).** Each pair reviews the baseline table: normal daily byte volume
   and allowed ports for five hosts.

2. **Score the observed window (12 min).** Pairs review the observed-traffic table (one school
   day) and, for each host, decide: within baseline, or anomalous? If anomalous, they name the
   specific indicator (unusual port, volume spike, or beaconing).

3. **Justify (8 min).** For each host they flag, pairs write one sentence citing the specific
   number or port that crossed the baseline.

## Printed baseline and observed traffic (deterministic)
```
Baseline (normal daily profile):
Host          Max bytes/day   Allowed ports
10.0.1.5      500,000,000     445, 139        (file server)
10.0.2.9      5,000,000       80, 443         (staff workstation)
10.0.2.14     5,000,000       80, 443         (staff workstation)
10.0.3.20     2,000,000       80, 443, 3389   (lab workstation, RDP allowed)
10.0.4.2      50,000,000      25, 587         (mail relay)

Observed traffic window (one school day):
Host          Total bytes sent   Ports used        Notes
10.0.1.5      420,000,000        445               Normal file-share load
10.0.2.9      4,800,000          80, 443           Normal browsing
10.0.2.14     1,200,000          443, 4444         Small volume but port 4444 never seen before
10.0.3.20     2,900,000          80, 443, 3389     Volume slightly over baseline
10.0.4.2      50,900 (x60, one connection every ~60 sec to same external IP)   587   Regular-interval beacon pattern
```

Expected classifications: 10.0.1.5 = normal, 10.0.2.9 = normal, 10.0.2.14 = ANOMALY (unusual port
4444), 10.0.3.20 = ANOMALY (volume 2.9M > 2M baseline), 10.0.4.2 = ANOMALY (beaconing pattern, regular ~60-second interval connections, even though total volume and port are within baseline).

## Collaborate (AP skill 4)
Assign roles: one partner is the "monitoring analyst" (applies the baseline mechanically), the
other is the "SOC lead" (challenges each call, is the deviation big enough to matter, or could it
be legitimate?). Swap roles for two instructor-supplied hosts.

## Exit ticket
Each student writes: one host from the table, its anomaly type (or "normal"), and one sentence
explaining what makes 10.0.4.2's case different from a simple volume or port anomaly (regular
timing, not just what/how much).

## Instructor notes
- Key learning moment: 10.0.4.2 passes both the volume check and the port check yet is still the
  most dangerous entry, this demonstrates that timing-pattern (beaconing) anomalies require a
  different kind of analysis than simple thresholds.
- Common stumble: students only check volume and port and miss that beaconing is about timing
  regularity, not amount.
- Feeds the unit project (building a traffic analyzer) and scenario stage 3 (network intrusion
  detection).
