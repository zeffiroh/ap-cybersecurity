# In-class activity, 2.3.b Surveillance systems (CCTV, monitoring)

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as a physical-security consultant team reviewing a proposed CCTV camera layout for a
fictional office floor plan, identify blind spots and monitoring/logical weaknesses, and propose
fixes. Ties to LO 2.3.A (surveillance systems) and the course skills Mitigate Risk and Detect
Attacks.

## Materials (all local)
- the SimLab simulation on each machine, or the printed camera plan sheet below.
- One copy of the camera layout sheet per group (print or display on screen).

## Camera layout sheet (print or project)

**Floor plan (top-down, ASCII):** the building has one main entrance (west), a loading dock
(south), a server room (northeast corner), and a long back hallway (east edge).

| # | Camera | Location | Type | Coverage note | Blind spot / issue? | Fix |
|---|--------|----------|------|----------------|----------------------|-----|
| 1 | CAM-01 | Main entrance (west) | Fixed | Faces the door, well-lit lobby | ? | ? |
| 2 | CAM-02 | Loading dock (south) | Fixed | Points at the dock doors only | ? | ? |
| 3 | CAM-03 | Server room (NE) | Fixed | Mounted 6 ft high, admin creds still default `admin`/`admin` | ? | ? |
| 4 | CAM-04 | Back hallway (east edge) | PTZ, sweeps hallway every 45s | Currently pointed north when guard checked | ? | ? |
| 5 | (none) | Loading dock side door | — | No camera covers the side door next to the dock | ? | ? |

## Steps
1. (5 min) Each group reviews the floor plan and camera list individually and marks which rows
   describe a blind spot, a logical/credential vulnerability, or both.
2. (5 min) Group discusses row 3 (server room camera): why is a low mounting height plus default
   credentials a compounding risk, not just two separate minor issues? Fill in "issue" and "fix."
3. (5 min) Repeat for row 4 (PTZ hallway camera), explain in the group's own words why a PTZ
   camera's wide *average* coverage does not guarantee coverage at any single *instant*, and what
   an intruder who studies the sweep timing could do.
4. (5 min) Discuss row 5, a completely uncovered door. Propose where a new camera (or an
   overlapping field of view from an existing one) should go to close the gap.
5. (5 min) Each group opens the simulation and checks their blind-spot / vulnerability calls against
   the sim's scoring for the analogous scenarios; groups revise any incorrect calls.

## Collaborate (AP skill 4)
Assign roles: one member is the "site surveyor" (identifies physical blind spots from the floor
plan), one is the "network auditor" (flags logical/credential weaknesses on IP cameras), and
remaining members are "budget owners" (must justify each proposed fix, new camera, re-aim,
credential change, VLAN isolation, against its cost and the risk it reduces). For row 4, the
group must specifically debate whether the fix is a second camera, a different sweep pattern, or
switching to a fixed camera.

## Exit ticket
Each student writes one sentence: "Camera/location X has [blind spot / logical vulnerability]
because [reasoning tied to the lesson], and [fix] would close it by [mechanism]."

## Instructor notes
- Timing: row 1 is a clean baseline (no issue) to test whether groups over-flag everything; rows
  2 and 5 are meant to be contrasted (row 2 has *a* camera but narrow coverage, row 5 has *no*
  camera at all) so groups articulate the difference between "narrow FOV" and "true blind spot."
- Row 3 is the intended teaching moment for compounding physical + logical vulnerabilities (low
  mount height enabling tampering, PLUS default credentials enabling remote takeover), push
  groups to name both issues, not just one.
- Row 4 (PTZ blind spot) is the hardest row; if groups struggle, prompt them to reread the atom's
  "Camera types" section on PTZ cameras before revisiting the row.
- Feeds forward to 2.4 (detecting physical attacks) and connects to 2.3.b's coding problem, which
  formalizes after-hours detection and "ghost motion" alerting logic from a camera event log.
