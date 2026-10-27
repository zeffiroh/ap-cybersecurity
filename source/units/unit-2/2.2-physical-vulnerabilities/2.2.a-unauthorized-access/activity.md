# In-class activity, 2.2.a Unauthorized physical access

**Format:** pairs · **Time:** 25 min · **Offline:** yes

## Goal
Students analyze a printed building access log, identify records that indicate tailgating or impossible-speed violations, and propose one countermeasure for each flagged event. Ties to LO 2.2.A (identify indicators of unauthorized physical access) and 2.2.B (explain how physical attacks bypass access controls).

## Materials (all local)
- the SimLab simulation on each machine, or the printed log table below.
- Pencils / highlighters for marking suspicious entries.

## Printed log (use if machines unavailable)

| Event ID | Time     | Badge ID | Door | Result  | Notes            |
|----------|----------|----------|------|---------|------------------|
| E001     | 08:03:11 | B-204    | D1   | GRANTED |                  |
| E002     | 08:03:14 | B-204    | D2   | GRANTED | D2 is 50 m away  |
| E003     | 08:07:45 | B-117    | D1   | GRANTED |                  |
| E004     | 08:07:48 | NONE     | D1   | —       | sensor: 2 people |
| E005     | 08:22:01 | B-099    | D3   | DENIED  |                  |
| E006     | 08:22:04 | B-099    | D3   | DENIED  |                  |
| E007     | 08:22:07 | B-099    | D3   | GRANTED | badge not changed |

## Steps
1. (10 min) Each pair reviews the log table (or uses the simulation). For each event, decide: legitimate, suspicious, or impossible. Write "L", "S", or "I" next to the event ID and a one-sentence reason.
2. (8 min) For every suspicious or impossible event, write the name of the attack technique it most likely represents (tailgating, piggybacking, RFID cloning, lock bypass, etc.) and one specific countermeasure the organization could deploy.
3. (7 min) Pairs compare findings with the pair next to them. Resolve any disagreements: if you classified the same event differently, which argument is stronger?

## Collaborate (AP skill 4)
Assign roles: one partner is the "security analyst" (flags records and names the attack), the other is the "CISO" (approves or challenges each flag and selects the countermeasure). Swap roles halfway through the log.

## Exit ticket
Each student submits: the event ID they found most ambiguous, the attack technique it represents, and the countermeasure they would implement, in two sentences or fewer.

## Instructor notes
- Expected flags: E001-E002 = impossible speed (B-204 cannot reach D2 in 3 s across 50 m; likely badge pass-back or clone); E003-E004 = tailgating (one swipe, sensor detects two people); E005-E007 = credential stuffing / replay, three attempts, third granted without changing the badge (may indicate a cloned badge being tried at slightly different angles, or a timing-based attack on the reader).
- Common stumble: students may not flag E001-E002 if they do not calculate the implied walking speed. Prompt: "How fast would you need to walk to cover 50 meters in 3 seconds?"
- Feeds the unit project (physical-pen-test report) and scenario stage 2 (attacker gaining server-room access).
