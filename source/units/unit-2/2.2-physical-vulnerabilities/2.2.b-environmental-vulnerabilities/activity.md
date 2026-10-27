# In-class activity, 2.2.b Environmental vulnerabilities (power, HVAC, fire, water)

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as a facilities/security triage team reviewing a day's worth of sensor alerts for a
fictional data center, decide which alerts require immediate escalation, and propose a control
for each category of environmental risk. Ties to LO 2.2.A (analyze environmental vulnerabilities)
and the course skill Analyze Risk.

## Materials (all local)
- the SimLab simulation on each machine, or the printed sensor-log sheet below.
- One copy of the sensor log per group (print or display on screen).

## Sensor log (print or project)

| # | Room | Sensor type | Reading | Escalate? | Likely cause | Control |
|---|------|------------|---------|-----------|--------------|---------|
| 1 | server-room-a | power | 0% (outage) | ? | ? | ? |
| 2 | server-room-a | temperature | 29°C | ? | ? | ? |
| 3 | server-room-a | humidity | 66% | ? | ? | ? |
| 4 | server-room-b | smoke | detected | ? | ? | ? |
| 5 | server-room-b | water | detected | ? | ? | ? |
| 6 | server-room-c | temperature | 22°C | ? | ? | ? |
| 7 | server-room-c | humidity | 48% | ? | ? | ? |

## Steps
1. (5 min) Each group reads readings 1-3 (server-room-a) and decides individually which readings
   should escalate to on-call staff immediately.
2. (5 min) Group discusses: readings 2 and 3 are both elevated in the same room, what does that
   combination suggest that either reading alone would not? Reach consensus and fill in
   "likely cause" and "control" for rows 1-3.
3. (5 min) Repeat for readings 4-5 (server-room-b) and 6-7 (server-room-c), including deciding
   whether row 6-7 needs any escalation at all.
4. (5 min) Each group opens the simulation and checks their triage decisions against the sim's scoring
   for the analogous scenarios; groups revise any incorrect calls.
5. (5 min) Report-out: each group states one row where they initially disagreed internally and how
   they resolved it.

## Collaborate (AP skill 4)
Assign roles: one member is the "on-call engineer" (decides whether to escalate and to whom), one
is the "budget owner" (must justify the cost of any proposed control against the risk it reduces),
and remaining members are "auditors" (challenge whether the proposed control actually addresses
the stated cause). For row 1 (total power outage), the group must specifically debate UPS runtime
versus generator start time and what the acceptable outage window is before escalation.

## Exit ticket
Each student writes one sentence: "Reading X should [escalate / not escalate] because [reasoning
tied to threshold or combined-signal rule], and [control] would reduce recurrence by [mechanism]."

## Answer key (instructor only)

| # | Escalate? | Likely cause | Control (sample) |
|---|-----------|--------------|-------------------|
| 1 | Yes, CRITICAL | Total power loss to server-room-a | UPS bridges immediately; generator should start within its rated window; verify via regular load testing |
| 2 | Yes, escalates to CRITICAL once combined with #3 | Rising temperature, likely HVAC strain | Check chiller/HVAC unit; verify redundant cooling capacity |
| 3 | Yes, escalates to CRITICAL once combined with #2 | Rising humidity alongside temperature, HVAC failure signature | Same HVAC repair; humidity control tied to same system |
| 4 | Yes, CRITICAL | Smoke detected, possible fire | Clean-agent suppression should trigger; evacuate; do not use water |
| 5 | Yes, CRITICAL | Water/moisture detected at floor level | Investigate plumbing above/near room; raised flooring should have limited spread |
| 6 | No, NORMAL | Temperature within normal operating range | No action; continue monitoring |
| 7 | No, NORMAL | Humidity within normal operating range | No action; continue monitoring |

## Instructor notes
- Timing: rows 1, 4, 5 are unambiguous single-sensor CRITICAL cases; rows 2-3 are the intended
  teaching moment for the combined-signal / HVAC-failure pattern from the lesson.
- Common stumble: students treat 2 and 3 as independent WARNING-level readings and under-escalate;
  push them to explain why the combination is worse than either alone (this mirrors the escalation
  rule implemented in `problem/`).
- Rows 6-7 exist to test whether groups over-escalate normal readings out of caution; a mature risk
  analysis should not treat everything as an emergency.
- Feeds the unit project (threat modeling a small network/facility) and connects forward to 2.3.d
  (environmental controls) and 2.4 (detecting physical attacks).
