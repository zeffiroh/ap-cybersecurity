# In-class activity, 2.3.d Environmental controls (HVAC, fire suppression, power)

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as facility-design consultants who must specify environmental controls for a new
three-room data center build (server room, network/telecom closet, and general office), and
justify every control choice against the hazard and equipment it protects. Ties to LO 2.3.C
(mitigate risk to physical spaces) and the course skill Mitigate Risk.

## Materials (all local)
- the SimLab simulation on each machine, or the printed design sheet below.
- One copy of the design sheet per group (print or display on screen).

## Design sheet (print or project)

| # | Room | Hazard to mitigate | Candidate controls | Chosen control | Justification |
|---|------|--------------------|--------------------|-----------------|----------------|
| 1 | server-room | Fire | water sprinkler / clean-agent (FM-200) / no suppression | ? | ? |
| 2 | server-room | Total utility power loss | UPS only / UPS + generator / generator only | ? | ? |
| 3 | server-room | Hot/cold air mixing raising inlet temp | containment curtains / lower ceiling / more fans | ? | ? |
| 4 | network-closet | Single point of failure in cooling | single HVAC unit / N+1 redundant HVAC units | ? | ? |
| 5 | server-room | Undetected floor-level leak | no sensor / raised floor + water sensor | ? | ? |
| 6 | office | Fire | water sprinkler / clean-agent (FM-200) | ? | ? |
| 7 | server-room | Locked-up server requiring reboot | send technician in person / managed PDU remote cycle | ? | ? |

## Steps
1. (5 min) Each group reads rows 1-3 (server room fire, power, and airflow) and individually
   picks a control for each, based on the atom.md lesson.
2. (5 min) Group discusses: why is a water sprinkler wrong for row 1 but acceptable for row 6?
   Reach consensus and fill in "justification" for rows 1, 3, 6.
3. (5 min) Repeat for rows 2, 4, 5, 7, the power, redundancy, leak-detection, and remote-access
   controls. Debate the UPS-vs-generator tradeoff for row 2 explicitly (speed of response vs.
   runtime).
4. (5 min) Each group opens the simulation and checks their control choices against the sim's
   scoring for the analogous scenarios; groups revise any incorrect picks.
5. (5 min) Report-out: each group states one control they initially picked wrong and what
   detail in the scenario changed their mind.

## Collaborate (AP skill 4)
Assign roles: one member is the "facilities lead" (owns the final control decision for each
row), one is the "budget owner" (must justify the added cost of redundancy, N+1 generators,
managed PDUs, against the outage risk it reduces), and remaining members are "inspectors"
(challenge whether the chosen control actually matches the room's contents and hazard). For
row 4 (single HVAC unit), the group must specifically debate what N+1 redundancy means and why
a single non-redundant HVAC unit is a design flaw even if it currently works.

## Exit ticket
Each student writes one sentence: "For room [X] and hazard [Y], the correct control is [Z]
because [reasoning tied to the equipment at risk or the redundancy principle], and choosing
[wrong alternative] would fail because [reason]."

## Answer key (instructor only)

| # | Chosen control | Justification (sample) |
|---|-----------------|--------------------------|
| 1 | Clean-agent (FM-200 or equivalent) | Water sprinklers destroy live electronics on contact; a clean agent extinguishes fire without residue or equipment damage. |
| 2 | UPS + generator (layered) | UPS responds in milliseconds to bridge the outage; generator takes over after 10-30s for extended runtime. Neither alone is sufficient. |
| 3 | Hot aisle / cold aisle containment | Physical separation stops hot exhaust air from mixing into cold intake air, which is the direct cause of rising inlet temperature. |
| 4 | N+1 redundant HVAC units | A single HVAC unit is a single point of failure; N+1 means a failure of one unit does not cause a cooling outage. |
| 5 | Raised floor + water sensor | Raised flooring limits how far shallow water spreads to reach equipment; a floor-level sensor gives early warning before visible flooding. |
| 6 | Water sprinkler | Office space has no sensitive electronics at floor level in the way a server room does; standard sprinklers are appropriate and cheaper. |
| 7 | Managed PDU remote cycle | A managed PDU lets staff remotely power-cycle a single outlet without a technician entering a restricted room. |

## Instructor notes
- Timing: rows 1, 6, and 7 are unambiguous single-answer picks; row 2 and row 4 are the intended
  teaching moments for layered defense and the N+1 redundancy principle.
- Common stumble: students pick "UPS only" for row 2 because it responds fastest, missing that
  UPS battery runtime is limited and a generator is required for anything beyond a few minutes.
- Row 6 exists to test whether groups over-apply clean-agent suppression everywhere out of
  caution; a mature risk analysis matches the control to the actual hazard and asset value,
  since clean-agent systems are far more expensive than sprinklers.
- Feeds forward into 2.4 (detecting physical attacks) and complements 2.2.b (environmental
  vulnerabilities), which covers identifying these hazards rather than mitigating them.
