# In-class activity, 4.3.c Patching and regular updates

**Format:** small group · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as a patch-management triage board: given a queue of pending vulnerabilities, they
decide deployment order and timing using CVSS severity, exploitation status, and exposure. Ties
to LO 4.3.B (patch lifecycle) and 4.3.C (prioritization tradeoffs).

## Materials (all local)
- the SimLab simulation / `problem/` / printed vulnerability cards below.

## Steps
1. **Read the queue (5 min).** Each group receives the five vulnerability cards below. For each,
   record the CVSS score, whether it is being actively exploited in the wild, and whether the
   affected system is internet-facing.

   - **Card A:** Internal HR file server, CVSS 9.8, no known exploitation in the wild yet,
     patch requires a scheduled reboot.
   - **Card B:** Public-facing customer web portal, CVSS 9.1, CISA has confirmed active
     exploitation in the wild starting this week.
   - **Card C:** Internal developer workstation, CVSS 4.2, no known exploitation, low business
     impact if compromised.
   - **Card D:** Public-facing VPN gateway, CVSS 7.5, no confirmed in-the-wild exploitation yet,
     but a working proof-of-concept exploit was published publicly two days ago.
   - **Card E:** Legacy internal print server, CVSS 8.8, vendor has marked the product
     end-of-life, no patch will ever be released.

2. **Rank the queue (10 min).** As a group, produce a single ranked list (1 = patch first) for
   Cards A-E, with a one-sentence justification for each ranking decision.

3. **Check with the simulation (10 min).** Open the simulation and work through its patch-triage queue.
   Compare the urgency labels the simulation assigns with your own ranking. Discuss any
   disagreements.

## Collaborate (AP skill 4)
Assign roles: one member is the "Security Analyst" (argues from pure exploitability/severity),
one is "IT Operations" (raises downtime/compatibility costs of patching), and one is "Business
Risk Owner" (weighs impact if each system is breached). Negotiate a final ranked list the whole
group agrees on, and note any card where the roles disagreed.

## Exit ticket
Each student submits: their final ranking for Card E (the end-of-life system) plus a
one-sentence explanation of what control should be used since no patch will ever exist.

## Instructor notes
- Expected priority order (highest urgency first): B (public-facing, actively exploited, patch
  immediately/emergency), D (public-facing, working exploit published, patch urgently), A
  (critical severity but internal and not yet exploited, patch on an accelerated but not
  emergency timeline), E (high severity but no patch will ever exist, apply compensating
  controls, e.g. network isolation/segmentation, not patching), C (low severity, low exposure, routine cadence).
- Common stumble: students rank purely by CVSS number and miss that exposure (internet-facing)
  and exploitation status (already being exploited) matter as much as or more than raw severity.
  A high CVSS score on an isolated internal system can be less urgent than a moderate score on
  an actively-exploited public system.
- Card E is the deliberate trick card: it forces students to realize "patch" is not always the
  answer, end-of-life systems require compensating controls instead.
- Feeds the coding problem's exact triage logic (severity + exploitation + exposure -> urgency
  label) and reinforces the unit's defense-in-depth theme.
