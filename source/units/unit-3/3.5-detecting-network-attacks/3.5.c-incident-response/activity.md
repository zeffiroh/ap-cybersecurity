# In-class activity, 3.5.c Incident response sequence

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups reconstruct the correct NIST SP 800-61 phase order for a shuffled set of response actions
taken during a Meridian High School ransomware incident, and articulate why two "obviously
sensible" out-of-order actions would actually make the incident worse. Ties to LO 3.5.C (order
incident-response actions correctly; explain the risk of skipping or reordering phases).

## Materials (all local)
- the SimLab simulation on each machine, or the printed action cards below (cut into strips).

## Steps
1. **Sort the cards (10 min).** Each group receives the 9 shuffled action cards below. Working
   together, they sort them into the correct 6-phase NIST order (some phases have more than one
   action; keep same-phase actions grouped but their internal order does not need to be graded).

2. **Spot the trap (8 min).** Two of the cards are deliberately written to tempt an out-of-order
   placement (see "trap" notes below, not shown to students). Groups discuss why each trap action
   must wait for an earlier phase to finish first.

3. **Present (7 min).** Each group presents their final order and defends the placement of the two
   trap actions to the class.

## Printed action cards (deterministic, shuffled)
```
Card 1: "Rebuild the file server from a verified clean backup and reconnect it to the network."
Card 2: "Delete the attacker's backdoor scheduled task from the domain controller."
Card 3: "Draft and rehearse the school's incident response plan with IT staff."
Card 4: "Confirm that the ransomware alert is a real compromise, not a false positive."
Card 5: "Disconnect the infected lab subnet from the rest of the network."
Card 6: "Write an incident timeline and update the response plan based on what was learned."
Card 7: "Immediately wipe and reinstall the infected machine while it is still on the live network." [TRAP]
Card 8: "Patch the vulnerability the attacker used to gain initial access."
Card 9: "Monitor the recovered systems closely for any sign the compromise persists." [TRAP if placed too early]
```

Correct order (by phase):
- Preparation: Card 3
- Identification: Card 4
- Containment: Card 5
- Eradication: Card 2, Card 8 (Card 7 belongs here too, but ONLY after containment, see trap notes)
- Recovery: Card 1, Card 9
- Lessons Learned: Card 6

## Collaborate (AP skill 4)
Assign roles: a "recorder" (writes the final order), a "skeptic" (challenges any placement without
a clear phase justification), and a "presenter" (defends the group's order to the class).

## Exit ticket
Each student writes: which two cards are the "traps," and one sentence each explaining what goes
wrong if Card 7's action happens before the subnet is disconnected (Card 5), and if Card 9's
monitoring is treated as optional after recovery.

## Instructor notes
- Card 7 is written to sound proactive ("wipe and reinstall right away") but is a containment
  violation if the host is still connected, reinfection or attacker awareness can result. It only
  belongs in Eradication AFTER Card 5 (Containment) is complete.
- Card 9 tests whether students remember Recovery includes active monitoring, not just restoration, a system brought back online without monitoring may still be compromised.
- Common stumble: groups place Card 2 (removing the backdoor) before Card 5 (isolating the
  subnet); walk them back to the general principle, contain first, always.
- Feeds the unit project and the scenario's incident-response stage.
