# In-class activity, 1.3.d War driving; protecting yourself (verify SSIDs, avoid open networks, VPN)

**Format:** small groups (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Students apply the three-step personal safety protocol (verify SSID, avoid open networks,
use VPN) to a set of network scenarios and produce a risk-flag report for each. They also
discuss how to respond when no safe option exists. Ties to LO 1.3.B (identify indicators of
wireless attack exposure) and 1.3.C (describe mitigation strategies for public-Wi-Fi risk).

## Materials (all local)
- the SimLab simulation, network risk assessor
- `problem/`, coding challenge
- Scenario card set below (read aloud or printed)

## Scenario cards

**Card 1, Airport departure lounge**
Network visible: "AirportFreeWifi" (OPEN). You did not ask staff. You have your VPN installed
but it is not connected. You need to check work email.
Question: What flags does this network carry? What do you do?

**Card 2, Hotel lobby**
Network: "HotelGuest" (WPA2). You confirmed the name with the front desk. Your VPN is active.
Question: What flags (if any)? Is it safe to proceed?

**Card 3, Coffee shop**
Network: "CafeNet" (WPA2). You did not ask staff. Your VPN is active.
Question: What flags? What is the residual risk?

**Card 4, Study hall**
Network: "StudyNet" (OPEN). You confirmed the SSID with the librarian. You have no VPN.
Question: What flags? What is the safest course of action?

**Card 5, Street outside a building**
Your device auto-connected to "CorporateWifi" (WPA2) while you walked past. You did not
verify the SSID. Your VPN is not running.
Question: Should you continue using this connection? What flags apply?

## Steps
1. (5 min) Each group reads all five cards and assigns a preliminary flag list to each.
2. (10 min) Groups use the simulation to run each scenario through the sim's risk assessor. Compare
   sim output to the group's preliminary assessment. Reconcile any differences.
3. (5 min) Each group selects the scenario where the user faces the hardest trade-off (no good
   option) and drafts a written recommendation: what to do, what not to do, and why.
4. (5 min) One group presents their recommendation; others add or challenge.

## Collaborate (AP skill 4)
Assign roles per group: **risk analyst** (applies the flag rules), **user advocate** (argues
for usability, what if you really must connect?), **security officer** (enforces policy
regardless of inconvenience). Rotate roles across cards.

## Exit ticket
Each student submits a three-sentence personal Wi-Fi policy they would follow on a school
trip: one sentence per step (verify, avoid open, VPN).

## Instructor notes
- Expected flags by card: Card 1: open-network, unverified-ssid, no-vpn. Card 2: none (clean).
  Card 3: unverified-ssid. Card 4: open-network, no-vpn (ssid IS verified, that flag clears).
  Card 5: unverified-ssid, no-vpn.
- Common stumble: students think WPA2 without verification is safe. Clarify: security type
  addresses encryption, but an evil twin can use WPA2 too, verification is a separate check.
- Card 2 is intentionally clean to check that students do not over-flag.
- Feeds the unit project (personal security policy) and scenario stage 4 (user connects to
  evil twin due to missing verification step).
