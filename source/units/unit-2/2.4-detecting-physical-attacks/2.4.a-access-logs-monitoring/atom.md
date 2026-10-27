# 2.4.a, Access logs and monitoring

> **Unit 2 · 2.4 Detecting Physical Attacks**
> **AP Learning Objective(s):** 2.4.A
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Interpret physical access log entries to identify anomalous patterns, after-hours entries, repeated failures, and tailgating gaps, and explain what each pattern signals to a security analyst.

## Lesson
Physical security controls, badge readers, key-card doors, biometric scanners, generate a continuous stream of timestamped records every time someone attempts or succeeds at entering a controlled area. That stream is called a **physical access log**, and it is one of the most powerful detective tools a security team has. Unlike a camera feed that requires a human to watch, a log can be searched, filtered, and analyzed automatically. Understanding what these records look like, what normal looks like, and how attacks distort that normal is the core skill here.

Every access log entry contains at least three pieces of information: *who* presented a credential (a badge ID or biometric template), *where* (which door or reader), and *when* (timestamp down to the second). Enterprise systems often add a fourth field: *outcome*, whether the credential was accepted or denied. A fifth field, sometimes called *anti-passback*, records whether the person who is marked as "in" is presenting their badge to enter again without having first exited, a strong indicator that a badge has been shared or cloned.

To understand why logs matter, consider a realistic scenario at a mid-sized company called Crestfield Analytics. The server room door requires a badge swipe. Normal behavior for that door: staff enter between 08:00 and 18:00, Monday through Friday; the same ten people account for 95% of all entries. Now suppose an attacker has cloned an employee's badge. The attack produces a signature in the log that is hard to fake away: the cloned badge appears at the server room door at 02:17 on a Saturday. The legitimate badge holder was also logged entering the front lobby at 07:55 the same morning, so the same credential shows two geographically implausible uses within the same night. This pattern is called a **location inconsistency** and is one of the clearest red flags in access log analysis.

A second common pattern is the **repeated denial burst**. An attacker who does not have a valid credential but is trying known badge IDs, or who has a revoked badge, will generate a cluster of ACCESS DENIED events in a short window. Five or more failures from the same badge within sixty seconds, especially at a high-value door, is the access-log equivalent of a network brute-force attack. Detection logic is almost identical: count failures per credential per time window, and alert when the threshold is crossed.

A subtler attack pattern is **tailgating** (also called piggybacking), where an unauthorized person follows an authorized one through a door without swiping. Logs alone do not catch tailgating directly, because the attacker never swipes. However, logs can reveal it indirectly: if the number of people recorded as "entered" on an anti-passback system is lower than the physical count recorded by an overhead people-counter sensor, the difference represents unlogged bodies, strong grounds for an alert or camera review.

**After-hours access** is the most frequently cited anomaly in physical security incident reports. Defining "after hours" requires a baseline: you must know what normal operating hours look like for each door, not just the building. A server room is expected to be empty at midnight even if the building itself has 24-hour cleaning staff. Any access to that room between 22:00 and 06:00 should generate an alert regardless of whether the badge is valid, because legitimate after-hours access should be pre-authorized and logged separately.

Building a practical monitoring system means aggregating log data across all readers into a **Security Information and Event Management (SIEM)** platform or a simpler custom pipeline. The pipeline applies detection rules, threshold rules for bursts, schedule rules for after-hours, correlation rules for location inconsistencies, and produces alerts ranked by severity. Tier-1 analysts triage alerts; confirmed anomalies escalate to investigation.

One point the AP framework emphasizes: logs are detective controls, not preventive ones. A log tells you *after the fact* that something happened. Their value lies in limiting the window between a breach and its discovery, enabling faster containment and forensic reconstruction of events. Combined with real-time alerting (covered in 2.4.b), logs transform from a static record into an active detection system.

In the coding problem for this skill, you will implement exactly this detection logic: given a list of timestamped access log entries, identify every badge ID that triggers any of the three alerting rules, repeated denial burst, after-hours valid access to a restricted door, or location inconsistency within a defined time gap. The simulation lets you step through a synthetic day's worth of log entries and practice flagging anomalies before you code the detector.

## Key terms
- **Physical access log**, a timestamped record of credential presentations at controlled entry points, including outcome (granted or denied).
- **Anti-passback**, a rule that prevents a credential from granting entry if it has not yet been used to exit, detecting shared or re-entered badges.
- **After-hours access**, any entry to a controlled area outside its defined authorized schedule, which warrants automatic alerting regardless of credential validity.
- **Repeated denial burst**, a cluster of ACCESS DENIED events for a single credential within a short time window, analogous to a brute-force attack.
- **Location inconsistency**, a single credential appearing at two geographically separated readers within an interval too short for legitimate travel.
- **SIEM**, Security Information and Event Management; a platform that aggregates and correlates security event data from multiple sources for real-time analysis.

## Common misconceptions
- "A valid badge swipe means the entry was authorized." → Badges can be cloned, stolen, or shared; a valid swipe only proves a credential was presented, not that the right person presented it. Context, time, location, frequency, is what determines legitimacy.
- "Logs are only useful after an incident." → Real-time rule evaluation against a live log stream is an active detective control; modern SIEM rules alert within seconds of a threshold crossing.

## Try it
- **Simulation:** Review a synthetic day's access log for Crestfield Analytics and correctly flag every anomalous entry before the timer runs out.
- **Coding problem:** Implement `solve(entries)` to return a sorted list of badge IDs that triggered one or more alert rules across the log.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-116 (physical access control), rebuilt as original prose above; key concepts cross-referenced with vendor notes.
- Reference: Wikiversity (information security / physical security controls), background context on log structures and SIEM integration.
- Practice: Cybrary (physical security monitoring micro-exercises), rebuilt locally as the simulation scenario.
- Repo: LetsDefend/Free-Cybersecurity-Resources, `vendor/repos/letsdefend-free-cybersecurity-resources`.
