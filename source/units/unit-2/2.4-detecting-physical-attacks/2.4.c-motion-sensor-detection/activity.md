# In-class activity, 2.4.c Motion detectors and sensor-based detection

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as a physical-security design team laying out motion-sensor coverage for a small
server room, choosing sensor technology per zone and tuning sensitivity to balance detection
against false-positive risk. Ties to LO 2.4.B/2.4.C and the course skill Detect Attacks.

## Materials (all local)
- the SimLab simulation on each machine, or the printed room diagram/event log below.
- One copy of the room diagram and event log per group (print or display on screen).

## Room diagram (describe or sketch on paper)
A rectangular server room, 8m x 6m. One door on the south wall. One window on the east wall.
An HVAC supply vent is mounted on the north wall ceiling. Two equipment racks run down the
center of the room. The room is unoccupied outside business hours; no pets are permitted.

## Event log (print or project)

| # | Sensor type | Zone | Cause tag | True detection? | Reasoning |
|---|------------|------|-----------|-----------------|-----------|
| 1 | PIR | near window | sunlight | ? | ? |
| 2 | PIR | near door | person | ? | ? |
| 3 | microwave | near HVAC vent | hvac_airflow | ? | ? |
| 4 | dual-tech | central aisle | PIR=person, MW=person | ? | ? |
| 5 | dual-tech | central aisle | PIR=person, MW=vibration | ? | ? |
| 6 | PIR | near vent | hvac_airflow | ? | ? |

## Steps
1. (5 min) Each group reviews the room diagram and marks, on paper, where they would place a
   motion sensor to cover the door and the central aisle without pointing directly at the window
   or the HVAC vent. Note any zone where a blind spot seems unavoidable.
2. (8 min) Group works through the event log rows 1-6, deciding TRUE DETECTION or FALSE POSITIVE
   for each using the AND-logic rule for dual-tech sensors and the false-positive cause list from
   the lesson (sunlight, hvac_airflow, pet, insect, vibration, foliage).
3. (5 min) Group decides: given the false-positive causes seen in rows 1 and 3, would you
   recommend upgrading the window-adjacent and vent-adjacent zones to dual-technology sensors?
   Justify with the AND-logic reasoning from the lesson.
4. (4 min) Each group opens the simulation and checks their event-log verdicts against the sim's
   scoring for the analogous scenarios; groups revise any incorrect calls.
5. (3 min) Report-out: each group states one sensor-placement decision and one sensitivity-tuning
   decision they made, and why.

## Collaborate (AP skill 4)
Assign roles: one member is the "sensor installer" (proposes physical placement and mounting
height), one is the "tuning engineer" (proposes sensitivity level per zone and defends it against
the room's known false-positive risks), and remaining members are "auditors" (challenge whether a
proposed placement or sensitivity leaves a blind spot or an unacceptable false-positive rate). For
row 5 (dual-tech with a mixed cause), the group must specifically debate whether the AND-logic
call (false positive) is the right operational response, or whether a person should still check
the room in person.

## Exit ticket
Each student writes one sentence: "Event X is a [true detection / false positive] because
[AND-logic reasoning or false-positive cause tag], and I would [keep / change] the sensor's
placement or sensitivity because [reasoning]."

## Instructor notes

| # | True detection? | Reasoning |
|---|-----------------|-----------|
| 1 | No, FALSE POSITIVE | Sunlight is a known PIR false-positive cause; the window-adjacent sensor should be re-angled or paired with a dual-tech unit. |
| 2 | Yes, TRUE DETECTION | Person cause, no competing false-positive tag. |
| 3 | No, FALSE POSITIVE | HVAC airflow is a known microwave/ultrasonic false-positive cause. |
| 4 | Yes, TRUE DETECTION | Both dual-tech elements independently agree the cause is a person (AND-logic satisfied). |
| 5 | No, FALSE POSITIVE | Microwave element's cause (vibration) is a known false-positive tag, so AND-logic fails even though the PIR element correctly saw a person. |
| 6 | No, FALSE POSITIVE | Same HVAC airflow issue as row 3, now on a PIR sensor, reinforces that placement near a vent is the root cause, not the sensor technology alone. |

- Timing: rows 2 and 4 are the unambiguous true-detection cases; rows 1, 3, 5, 6 are the intended
  teaching moment for false-positive causes and AND-logic.
- Common stumble: students assume a dual-tech sensor is a true detection whenever *either* element
  reports "person", push them back to the lesson's AND-logic rule (both elements must agree).
- Rows 1, 3, and 6 exist to reinforce that placement near a window or HVAC vent is a root cause of
  false positives regardless of sensor technology, the fix is often re-placement, not just tuning.
- Feeds forward to the unit project (threat modeling a small facility) and connects to 2.4.b
  (alarm systems, which consume this sensor's verdict) and 2.3 (protecting physical spaces).
