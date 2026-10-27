# In-class activity, 2.3.a Physical access controls (locks, badges, biometrics, mantraps)

**Format:** pairs · **Time:** 20 min · **Offline:** yes

## Goal

Each pair produces a completed facility audit worksheet: a table listing which controls are present or absent at a fictional facility, the gaps those absences create, and a ranked recommendation list of the two most important controls to add first. This ties directly to LO 2.3.A (explain how physical access controls mitigate risk).

## Materials (all local)

- the SimLab simulation, open in browser for reference during rounds 1-3.
- `problem/`, students may read `prompt.md` to see the gap-detection rules.
- Printed handout below (or displayed on screen if printing is not available).

---

## Printed handout (cut here or project on screen)

### Facility audit worksheet

**Facility name (fictional):** Northgate Data Center, Building C, Server Floor

**Scenario description:** The server floor houses 12 racks of equipment for a fictional regional bank. The floor is accessed from a lobby on the ground level. A receptionist sits in the lobby during business hours only (8 a.m. to 6 p.m., weekdays). The building has a perimeter fence with a gate that is unlocked during business hours.

**Control inventory** (circle one for each row):

| Control | Present? | Notes |
|---|---|---|
| Keyed or cipher lock on server-floor door | Yes / No | |
| Badge/RFID reader on server-floor door | Yes / No | |
| Biometric reader inside server-floor entrance | Yes / No | |
| Mantrap between lobby and server floor | Yes / No | |
| CCTV cameras covering the server floor entrance | Yes / No | |
| Security guard present 24/7 | Yes / No | |

**Step 1, Scenario A (5 min):** Your instructor reads the following configuration aloud. Circle Yes or No for each control above.

> Scenario A: The server-floor door has a keyed deadbolt. There is a badge reader mounted beside the door. There is no mantrap. A fixed CCTV camera covers the hallway outside the door. There is no dedicated security guard; the receptionist monitors a lobby camera during business hours only. There is no biometric reader.

**Step 2, Gap analysis (5 min):** Using the rules below, list every gap present in Scenario A.

Gap rules (apply ALL that match):
- If keyed lock is absent AND badge reader is absent: gap "no_key_control"
- If badge reader is absent AND biometric is absent: gap "no_electronic_access"
- If mantrap is absent: gap "no_tailgating_prevention"
- If CCTV is absent: gap "no_visual_monitoring"
- If security guard is absent AND biometric is absent: gap "no_identity_verification"

Gaps found in Scenario A (list them):

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

**Step 3, Prioritize (5 min):** Rank the gaps from most critical to least critical for this bank scenario. Write a one-sentence justification for your top pick.

Most critical gap: _______________________________________________

Justification: _______________________________________________

Second most critical gap: _______________________________________________

**Step 4, Scenario B (5 min):** Your instructor reads a second configuration. Repeat the gap analysis.

> Scenario B: No keyed lock. No badge reader. No biometric. No mantrap. CCTV is present. One licensed security guard is stationed at the door 24/7.

Gaps found in Scenario B:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## Steps

1. (2 min) One partner opens the simulation and quickly reads the objective panel so both partners understand the audit model. The other partner reads the gap rules in `problem/prompt.md`.
2. (5 min) Together, complete Step 1 and Step 2 on the handout for Scenario A.
3. (5 min) Complete Step 3: agree on a priority ranking. If you disagree, each writes a one-sentence argument and you pick the stronger one.
4. (5 min) Complete Step 4 for Scenario B independently (each partner fills in their own sheet), then compare answers.
5. (3 min) Prepare a one-sentence summary to share with the class: "The most dangerous gap in Scenario A/B is ___ because ___."

## Collaborate (AP skill 4)

Assign roles before starting: one partner is the **Security Auditor** (reads controls off the scenario and checks Yes/No), the other is the **Risk Analyst** (applies the gap rules and writes the gap list). For Step 3, switch roles so the Risk Analyst argues for the priority ranking and the Security Auditor challenges it. Both names go on the sheet.

## Exit ticket

Each student submits (on a half-sheet or typed into the class portal): "Name one physical control that prevents tailgating and explain in one sentence why a badge reader alone cannot solve the tailgating problem."

Expected answer: A mantrap (access vestibule) prevents tailgating by interlocking two doors so only one person can pass through per cycle. A badge reader authenticates the person who presents the badge but cannot physically stop a second person from following them through the door before it closes.

## Instructor notes

**Expected Scenario A gaps:** `no_tailgating_prevention`, `no_identity_verification`. (Badge reader is present so `no_key_control` and `no_electronic_access` do not apply. CCTV is present so `no_visual_monitoring` does not apply. Guard is absent and biometric is absent, so `no_identity_verification` applies. Mantrap is absent, so `no_tailgating_prevention` applies.)

**Expected Scenario B gaps:** `no_key_control`, `no_electronic_access`, `no_tailgating_prevention`. (Guard present covers `no_identity_verification`. CCTV present covers `no_visual_monitoring`. No lock and no badge reader trigger `no_key_control`. No badge reader and no biometric trigger `no_electronic_access`. No mantrap triggers `no_tailgating_prevention`.)

**Common stumbles:**
- Students apply `no_key_control` even when a badge reader is present. Remind them the rule requires BOTH keyed lock and badge reader to be absent.
- Students confuse CCTV (detective) with prevention. Use it to reinforce the detective/preventive control distinction.
- Students may not realize that a security guard present 24/7 satisfies the identity-verification requirement (the guard checks ID), so `no_identity_verification` does not apply in Scenario B.

**Timing:** Steps 1-2 typically take 8-9 minutes for pairs who read carefully. Step 3 usually surfaces the best discussion. If time is short, skip Step 4 and debrief Scenario A only.

**Feed-forward to unit project:** The gap-detection logic students practice here is exactly the `solve()` function they implement in `problem/`. Encourage fast finishers to open `problem/starter.py` and sketch pseudocode.
