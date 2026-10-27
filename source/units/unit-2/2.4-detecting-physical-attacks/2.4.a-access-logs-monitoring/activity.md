# In-class activity, 2.4.a Access logs and monitoring

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students practice reading physical access log data to identify anomalous patterns (after-hours access, repeated denial bursts, location inconsistencies) and articulate what each pattern indicates to a security analyst. Ties to LO 2.4.A (analyze access logs to detect physical attack indicators).

## Materials (all local)
- the SimLab simulation on each machine, or the printed log extract below.
- Paper and pencil for flagging entries.

## Printed log extract (use if machines are unavailable)

```
TIMESTAMP            BADGE    DOOR              OUTCOME
2024-03-12 07:58:02  B-0101   lobby-north       GRANTED
2024-03-12 08:03:14  B-0205   lobby-north       GRANTED
2024-03-12 08:45:30  B-0101   server-room-A     GRANTED
2024-03-12 12:10:05  B-0307   lobby-north       DENIED
2024-03-12 12:10:18  B-0307   lobby-north       DENIED
2024-03-12 12:10:29  B-0307   lobby-north       DENIED
2024-03-12 12:10:41  B-0307   lobby-north       DENIED
2024-03-12 12:10:55  B-0307   lobby-north       DENIED
2024-03-12 12:11:03  B-0307   lobby-north       DENIED
2024-03-12 17:55:00  B-0205   lobby-north       GRANTED
2024-03-12 23:41:17  B-0205   server-room-A     GRANTED
2024-03-13 00:05:44  B-0101   datacenter-offsite GRANTED
```

(Note: datacenter-offsite is 35 miles from the main building. B-0101 was last seen at server-room-A at 08:45.)

## Steps
1. Each pair reads through the log. For every row, decide: normal or anomalous? Write a one-word verdict in the margin.
2. For each anomalous row, write which rule it triggers: AFTER-HOURS, BURST, or LOCATION-INCONSISTENCY.
3. Discuss: which anomaly is the most serious, and what would you recommend the analyst do next?

## Collaborate (AP skill 4)
Assign roles: one partner is the "analyst" (flags entries and names the rule), the other is the "attacker's lawyer" (argues why the entry might be innocent). After classifying all entries, swap roles and revisit the two most disputed entries.

## Exit ticket
Each student submits: (1) which badge IDs you would report to security, (2) the rule that triggered each flag, and (3) one defensive countermeasure that would reduce the risk each flagged pattern represents.

## Instructor notes
- Expected flags: B-0307 (burst, 6 denials in 58 seconds), B-0205 (after-hours valid access to server-room-A at 23:41), B-0101 (location inconsistency, server-room-A at 08:45, datacenter-offsite at 00:05 next day is more than 15 hours apart so not a strict inconsistency, let students debate this one).
- Common stumble: students flag every DENIED entry. Clarify that a single denial is noise; the threshold for a burst is 5+ failures within 60 seconds.
- Common stumble: students miss that B-0205 at 23:41 is on the same calendar day as the 17:55 exit, walk through date arithmetic.
- Feeds the unit project (physical intrusion timeline reconstruction) and scenario stage 2 (detecting the inside threat).
