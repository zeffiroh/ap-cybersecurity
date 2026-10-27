# In-class activity, 3.1.c Man-in-the-middle and ARP spoofing

**Format:** small group (3-4) · **Time:** 25 min · **Offline:** yes

## Goal
Groups act as network analysts reviewing ARP-watch logs for a small office LAN, decide which IP
addresses show the ARP spoofing signature, and design one mitigation for the network. Ties to LO
3.1.B and the course skill Analyze Risk.

## Materials (all local)
- the SimLab simulation on each machine, or the printed log below.

## ARP-watch log (print or project)

| # | Target IP | Reply sequence (MAC @ t=sec) | Verdict? |
|---|-----------|-------------------------------|----------|
| 1 | 192.168.1.1 (gateway) | aa:01 @0, aa:01 @30, aa:01 @60 | ? |
| 2 | 192.168.1.1 (gateway) | aa:01 @0, aa:01 @30, ff:99 @32 | ? |
| 3 | 192.168.1.40 | 12:34 @0 | ? |
| 4 | 192.168.1.60 | bb:02 @0, cc:03 @600 | ? |

(Row 4: the second reply arrives 10 minutes after the first, discuss whether the same rule
applies regardless of the time gap.)

## Steps
1. (5 min) Each group reads rows 1-2 individually and decides LEGIT or SPOOFED using the
   trusted-binding rule from the lesson (first reply establishes trust; a later reply with a
   different MAC for the same IP is spoofing).
2. (5 min) Group discusses row 3: with only one reply ever observed, is there enough evidence to
   call this SPOOFED? Why must a baseline exist first?
3. (7 min) Group works row 4 together: the MAC changes, but only after a 10-minute gap. Does a long
   time gap make the change more or less suspicious than a change seconds later (as in row 2)?
   Discuss legitimate reasons a MAC might change (e.g., a NIC replacement, DHCP lease to a new
   device) versus the spoofing explanation.
4. (5 min) Each group opens the simulation and checks their calls against the sim's scoring for
   analogous scenarios; groups revise any incorrect calls.
5. (3 min) Report-out: each group proposes one mitigation (Dynamic ARP Inspection, static ARP entry
   for the gateway, or VLAN segmentation) and explains which row it would have stopped.

## Collaborate (AP skill 4)
Assign roles: one member is the "arpwatch operator" (applies the trusted-binding rule literally),
one is the "attacker" (explains what a real attacker would need to do to reproduce each row), and
remaining members are "auditors" (challenge whether the binding-change evidence is strong enough to
call SPOOFED). For row 2 (the gateway), the group must specifically discuss why attackers usually
target the default gateway's IP rather than a random host, and what an attacker gains by doing so.

## Exit ticket
Each student writes one sentence: "Row X is [LEGIT / SPOOFED] because [the MAC did / did not]
change for [IP], and [reasoning about trusted binding or timing]."

## Answer key (instructor only)

| # | Verdict | Reasoning |
|---|---------|-----------|
| 1 | LEGIT | Same MAC (aa:01) across all three refreshes. |
| 2 | SPOOFED | A different MAC (ff:99) claims the gateway's IP shortly after the trusted binding was established. |
| 3 | LEGIT | Only one reply exists; there is no prior binding to contradict, so it cannot yet be called spoofing. |
| 4 | SPOOFED (discuss) | The binding did change; instructors should let groups argue both ways but land on: any unexplained binding change should be flagged and investigated, even if the timing alone is not conclusive proof. |

## Instructor notes
- Timing: rows 1-2 are the core matching-rule cases; row 3 tests "not enough evidence yet"; row 4
  is the deliberate ambiguous case meant to provoke discussion about false positives (legitimate
  MAC changes) versus real attacks.
- Common stumble: students treat every MAC change as automatically SPOOFED without considering
  legitimate causes (hardware replacement, DHCP reassignment), push them to explain what
  additional evidence (e.g., frequency, target being the gateway, timing) increases confidence.
- A second common stumble: students think a single observed reply (row 3) can be judged SPOOFED or
  LEGIT with confidence, reinforce that a baseline is required first.
- Feeds forward to 3.1.d (packet capture), where students learn to gather the actual evidence
  (captured ARP frames) that feeds this kind of analysis.
