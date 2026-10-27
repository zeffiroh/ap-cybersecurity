# 3.5.c, Incident response sequence

> **Unit 3 · 3.5 Detecting Network Attacks**
> **AP Learning Objective(s):** 3.5.C
> **Course skill(s):** Detect Attacks, Collaborate

## Learning objective (student-facing)
Name the six phases of the NIST incident-response lifecycle in
order, classify a given response action into its correct phase, and explain why performing actions
out of order (for example, eradicating before containing) can make an incident worse.

## Lesson
Detecting an attack, via a firewall log, an IDS alert, or a traffic anomaly, is only the
beginning. What an organization does in the minutes, hours, and days after detection determines
whether the incident is a contained inconvenience or a catastrophic breach. Incident response (IR)
is the structured process for handling that aftermath, and it is not improvised: security teams
follow a defined sequence of phases so that critical steps are never skipped under pressure.

**The NIST lifecycle.** The most widely taught model, from NIST Special Publication 800-61 ("Computer
Security Incident Handling Guide"), defines the process as six phases: **Preparation**,
**Identification**, **Containment**, **Eradication**, **Recovery**, and **Lessons Learned**
(also called Post-Incident Activity). Some texts fold Preparation into a separate ongoing readiness
category and describe the remaining five as the "incident lifecycle," but the AP framework treats
all six as the sequence to know, in this order.

**Preparation.** This phase happens before any incident occurs: writing an incident response plan,
defining roles and an escalation chain, deploying logging and monitoring tools, and running
tabletop exercises so the team is not improvising for the first time during a real breach. An
organization with no incident response plan is not "skipping" preparation, it is guaranteeing that
its first real incident will also be its first rehearsal.

**Identification.** The team determines that an incident is actually occurring, distinguishing a
genuine security event from routine noise, then confirming scope: which systems, which data, which
timeframe. This phase draws directly on the detection tools from earlier atoms in this unit, IDS
alerts (3.5.a) and traffic-monitoring anomalies (3.5.b) are common triggers that start
identification. A false positive from an over-sensitive sensor should be filtered out here, before
resources are committed to a full response.

**Containment.** Once an incident is confirmed, the immediate priority is to stop it from spreading
or getting worse, without necessarily fixing the root cause yet. Containment often means isolating
an infected host from the network, disabling a compromised account, or blocking a malicious IP at
the firewall. NIST distinguishes short-term containment (an immediate, possibly temporary measure,
such as unplugging a network cable) from long-term containment (a more durable fix, such as
rebuilding a system on a segmented VLAN, that can hold while eradication is planned). Containment
happens BEFORE eradication because removing malware from a system that is still connected to the
network gives the attacker a chance to notice and react, or simply re-infect the system a moment
later.

**Eradication.** With the incident contained, the team removes the actual cause: deleting malware,
disabling backdoor accounts the attacker created, patching the vulnerability that was exploited.
Eradication that happens before containment is a common and costly mistake, cleaning a host that
is still on the live network can tip off an attacker or allow immediate reinfection from another
already-compromised host.

**Recovery.** Systems are restored to normal operation: rebuilding from clean backups, reconnecting
to the network, and closely monitoring the restored systems for any sign that the compromise
persists. Recovery only begins once eradication is verified complete, bringing a system back online
before its root cause is removed just restarts the incident.

**Lessons Learned (Post-Incident Activity).** After the dust settles, the team documents a timeline
of what happened, evaluates how well the response plan worked, and updates that plan, tooling, or
training based on what was learned. Skipping this phase is how organizations end up repeating the
same incident: the technical fix from Eradication addressed this instance, but the process gap that
allowed it (a missing patch policy, an under-monitored segment) goes unaddressed.

**Why order matters.** Every phase depends on the one before it being substantially complete.
Identification without Preparation means the team has no plan to follow. Eradication before
Containment risks tipping off the attacker or allowing reinfection. Recovery before Eradication
just restarts the incident. Lessons Learned skipped entirely means the same gap gets exploited
again. The AP exam and this skill's exercises focus on exactly this: given a shuffled list of
response actions, can you place each one in its correct phase and, more importantly, recognize when
an action is being performed out of the correct sequence?

**Simulation.** The simulation gives you a shuffled list of response actions taken
during a Meridian High School ransomware incident; you assign each action to its correct
NIST IR phase and order the phases correctly.

**Coding problem.** The `problem/` directory implements a phase classifier: given a list of
response-action strings tagged with a phase label, verify the ordering, and given an unordered list
of the six canonical phase names, return them in correct lifecycle order.

## Key terms
- **Incident response (IR)**, the structured process an organization follows to detect, contain,
  and recover from a security incident.
- **NIST SP 800-61 lifecycle**, the six-phase model: Preparation, Identification, Containment,
  Eradication, Recovery, Lessons Learned.
- **Containment (short-term / long-term)**, actions that stop an incident from spreading,
  performed before the root cause is removed.
- **Eradication**, removing the actual cause of the incident (malware, backdoor accounts,
  unpatched vulnerability) after containment.
- **Lessons Learned (Post-Incident Activity)**, the closing phase where the team documents the
  incident and updates its plan, tools, or training to prevent recurrence.

## Common misconceptions
- "You should remove the malware as soon as you find it." → Removing malware before containment
  can tip off the attacker or allow reinfection; contain first, then eradicate.
- "Incident response starts when the incident happens." → Preparation is itself a phase, performed
  continuously before any incident, and is what determines how effective the rest of the response
  will be.
- "Recovery means the incident is over." → Recovery restores operations, but Lessons Learned is
  still required, without it, the organizational gap that allowed the incident often persists.

## Try it
- **Simulation:** Correctly assign every shuffled response action
  to its NIST IR phase and confirm the six phases are in correct lifecycle order.
- **Coding problem:** Implement a phase classifier/orderer: given phase-tagged actions
  and a shuffled phase-name list, validate/produce the correct NIST IR sequence.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (incident response fundamentals), rebuilt as original prose above;
  see `vendor/web/opensecuritytraining/` notes.
- Reference: NIST SP 800-61 Rev. 2 "Computer Security Incident Handling Guide", phase definitions
  rebuilt from primary text.
- Practice: Cybrary incident-response micro-challenges, rebuilt locally as the simulation
  phase-ordering exercise.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
