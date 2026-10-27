# In-class activity, 2.4.b Alarm systems

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as an alarm-monitoring central station reviewing a batch of sensor events for a small
office, decide the correct classification and response tier for each, and design one improvement
to reduce false alarms. Ties to LO 2.4.B (alarm systems) and the course skill Detect Attacks.

## Materials (all local)
- the SimLab simulation on each machine, or the printed event log below.
- One copy of the event log per group (print or display on screen).

## Event log (print or project)

| # | Zone | Sensor | Arm state | Seconds since armed | Classification? | Response? |
|---|------|--------|-----------|----------------------|------------------|-----------|
| 1 | front-lobby | contact | ARMED_AWAY | 8 | ? | ? |
| 2 | file-room | contact | DISARMED | 0 | ? | ? |
| 3 | loading-dock | glass_break | ARMED_AWAY | 300 | ? | ? |
| 4 | reception-desk | panic | ARMED_STAY | 0 | ? | ? |
| 5 | rear-hallway | contact | ARMED_AWAY | 310 | ? | ? |
| 6 | side-door | contact | ARMED_AWAY | 44 | ? | ? |

(Rows 3 and 5 occur 10 seconds apart in the same batch, decide whether that matters.)

## Steps
1. (5 min) Each group reads rows 1-2 individually and decides classification (SUPPRESSED,
   FALSE_ALARM, LOCAL_ONLY, or DISPATCH) using the exit-delay and arm-state rules from the lesson.
2. (5 min) Group discusses row 4 (panic button): does arm state matter here at all? Why does this
   sensor type break the normal rules?
3. (7 min) Group works rows 3 and 5 together: both are real trips (past exit delay) in different
   zones only 10 seconds apart. Decide whether cross-zone verification applies and what the
   combined classification should be, then classify row 6 (boundary case) on its own.
4. (5 min) Each group opens the simulation and checks their calls against the sim's scoring for
   analogous scenarios; groups revise any incorrect calls.
5. (3 min) Report-out: each group states which row was hardest to agree on and why.

## Collaborate (AP skill 4)
Assign roles: one member is the "panel operator" (makes the classification call in real time), one
is the "dispatcher" (decides, given a classification, whether police get called), and remaining
members are "auditors" (challenge whether the exit-delay or verification rule was applied
correctly). For row 6 (44 seconds, one second inside the 45-second boundary), the group must
specifically debate what happens if the exit-delay constant were shortened, and what tradeoff that
creates between response speed and false-alarm rate.

## Exit ticket
Each student writes one sentence: "Row X should be classified as [SUPPRESSED / FALSE_ALARM /
LOCAL_ONLY / DISPATCH] because [reasoning tied to arm state, exit delay, or cross-zone
verification]."

## Answer key (instructor only)

| # | Classification | Response | Reasoning |
|---|-----------------|----------|-----------|
| 1 | FALSE_ALARM | none | 8s since arming, inside the 45s exit delay |
| 2 | SUPPRESSED | none | system disarmed |
| 3 | DISPATCH (paired with row 5) | monitoring center dispatches | real trip, corroborated by row 5 in a different zone within the verification window |
| 4 | DISPATCH | monitoring center dispatches immediately | panic button bypasses arm state and verification entirely |
| 5 | DISPATCH (paired with row 3) | monitoring center dispatches | real trip, corroborated by row 3 within the verification window |
| 6 | FALSE_ALARM | none | 44s since arming, still inside the 45s exit delay (boundary is >= 45) |

## Instructor notes
- Timing: rows 1, 2, 4 are unambiguous single-rule cases; rows 3/5 are the intended teaching
  moment for cross-zone verification, and row 6 is a deliberate off-by-one boundary case.
- Common stumble: students treat row 4 (panic) like a normal contact sensor and check arm state or
  exit delay for it, push them to explain why a human-triggered duress signal is handled
  differently from an automated sensor trip.
- A second common stumble: students classify rows 3 and 5 independently as LOCAL_ONLY instead of
  recognizing the cross-zone pairing that promotes both to DISPATCH.
- Feeds forward to 2.4.c (motion sensors) and the unit project (designing a detection layer for a
  small facility).
