# In-class activity, 5.2.c Credential theft prevention and lateral movement

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Students trace a fictional authentication log to identify which account(s) show lateral-movement
behavior and propose the access-control practice that would have limited the spread. Ties to LO
5.2.B, 5.2.C.

## Materials (all local)
- the SimLab simulation on each machine, or the printed authentication-log excerpt below.

## Steps
1. Each group opens the simulation and works through the network graph / authentication log,
   identifying which account's host-hopping pattern crosses the lateral-movement threshold.
2. For the flagged account, the group writes two sentences: what behavioral signal gave it away
   (host count, timing, first-time privileged-tool use), and which single access-control practice
   (MFA, unique local-admin passwords, network segmentation, least privilege) would have stopped
   or slowed the chain.
3. Groups sketch a simple before/after network diagram showing how segmentation would have
   contained the compromised account to a smaller blast radius.

## Collaborate (AP skill 4)
Assign roles: a "log analyst" scans the authentication events, a "defender" proposes the
access-control fix, and a "recorder" documents the diagram and justification. Rotate roles for a
second scenario if time allows.

## Exit ticket
Each student submits: the account they flagged + the signal that gave it away + the fix they'd
recommend.

## Instructor notes
- Expected reasoning: host count and timing anomalies are the primary tells; the fix should map
  directly to the specific weakness shown (shared credentials -> credential hygiene; broad access
  -> least privilege/segmentation; stolen password alone worked -> MFA).
- Common stumble: students propose "better passwords" as a universal fix, steer them toward MFA
  and segmentation, since pass-the-hash attacks bypass password strength entirely.
- Feeds the unit project (incident-response tabletop) and the coding problem's lateral-movement detector.
