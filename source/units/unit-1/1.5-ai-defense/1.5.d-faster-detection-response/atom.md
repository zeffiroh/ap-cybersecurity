# 1.5.d, Faster, more accurate threat detection and response

> **Unit 1 · 1.5 Leveraging AI in Cyber Defense**
> **AP Learning Objective(s):** 1.5.B
> **Course skill(s):** Detect Attacks, Collaborate

## Learning objective (student-facing)
Explain how AI reduces Mean Time to Respond (MTTR) in a
security operations center, implement an incident-triage algorithm that prioritizes incidents
by severity and computes response-time metrics, and articulate the difference between
automated resolution and human-escalated response.

## Lesson
A security operations center is always racing against the clock. Every minute an attacker
spends inside a network is another minute of data exfiltration, lateral movement, or
credential harvesting. The time from the moment an incident is detected to the moment it is
resolved, Mean Time to Respond, or MTTR, is one of the most-watched metrics in cyber
defense. Industry benchmarks show that organizations with AI-assisted response pipelines cut
their MTTR by more than half compared to purely manual operations. Understanding *why* requires
understanding what the SOC analyst's workload looks like before automation.

**The pre-AI SOC workflow.** Before AI tooling, the sequence was: a SIEM generates an alert,
the alert lands in a queue, an analyst picks it up (maybe minutes later, maybe hours later if
the queue is long), the analyst manually looks up the affected asset, checks threat intelligence
feeds, reads the raw logs, decides whether the alert is a true positive or a false positive,
and, if true, initiates a response playbook. Each step is manual, slow, and prone to error
under fatigue. Alert queues routinely contain thousands of items. Studies from enterprise SOCs
found that analysts spent 25-50 percent of their time on false positives.

**What AI adds: triage scoring.** AI-assisted triage attaches a severity score to each
incoming incident based on signals the model has learned to weight: the type of event
(ransomware behavior scores higher than a single failed login), the criticality of the
affected asset (a domain controller is higher priority than a developer's laptop), the threat-
intelligence reputation of the source IP, and the historical false-positive rate for similar
alerts. This scoring lets the analyst queue be sorted by risk rather than arrival time, so the
most dangerous incidents surface first, even if they arrived after lower-severity noise.

**Automated resolution vs. human escalation.** Not all incidents need a human to close them.
AI playbooks can automatically resolve a class of incidents that are both high-confidence true
positives and have safe, reversible responses, for example: isolating a compromised endpoint,
forcing a password reset, or blocking a known-malicious IP at the firewall. These auto-resolved
incidents never enter the human queue at all. The result: analysts spend their limited time on
genuinely ambiguous or high-stakes decisions, while the AI handles the deterministic cases.
This is called *tiered response*: automated first tier, human second tier.

**MTTR decomposition.** MTTR has several sub-components: time to detect (TTD), time to triage
(TTT), time to contain (TTC), and time to eradicate (TTE). AI improves each. TTD shrinks
because AI continuously monitors telemetry without attention lapses. TTT shrinks because
severity scoring replaces manual prioritization. TTC shrinks because automated playbooks
execute in seconds rather than the minutes or hours it takes for a human to read a runbook and
issue commands. MTTR = TTD + TTT + TTC + TTE; AI applies leverage at each stage.

**The coding problem: computing triage metrics.** The `solve()` function in this skill takes a
list of incident records, each with a detection timestamp, a resolution timestamp, a severity
level, and an auto-resolution flag, and returns two numeric metrics:

- `mttr`: the mean (average) time to respond in seconds, computed across all incidents.
- `auto_resolved`: the count of incidents that were resolved automatically.

These metrics mirror the KPIs a real SOC dashboard would display to a manager assessing
whether the AI tooling is delivering value. The simulation lets you play the role of a SOC
analyst triaging incidents and watching MTTR improve as you prioritize correctly.

**Why severity-first triage matters.** If a queue of incidents is processed in arrival order,
a critical ransomware alert that arrives after a batch of low-severity port-scan alerts will
wait. Every second it waits, the attacker progresses. Sorting by severity ensures that critical
incidents are contained first, which has a nonlinear effect on damage: stopping an attacker
at lateral movement prevents credential harvest; stopping them at credential harvest prevents
data exfiltration. The "Detect Attacks" skill includes understanding that *when* you respond
matters as much as *how* you respond.

**Human factors and the limits of automation.** AI cannot replace the judgment required for
novel attack patterns that do not match training data, for incidents with significant
collateral risk (auto-blocking an IP that turns out to belong to a business partner), or for
scenarios requiring communication with legal, executive, or law-enforcement stakeholders. The
AP framework's "Collaborate" skill is directly engaged here: effective incident response is a
team activity where AI handles scale and humans handle judgment, ethics, and communication.

## Key terms
- **MTTR (Mean Time to Respond)**, the average time from incident detection to resolution;
  a primary KPI for SOC effectiveness.
- **Triage**, the process of prioritizing incidents by severity so the most dangerous are
  handled first.
- **Severity score**, a numeric rating assigned to an incident based on its potential impact
  and the criticality of the affected asset.
- **Auto-resolution**, automated closure of an incident by an AI playbook without human
  intervention, reserved for high-confidence cases with safe responses.
- **Tiered response**, a model where AI handles routine, high-confidence incidents
  automatically and escalates ambiguous or high-stakes cases to human analysts.
- **False positive**, an alert that fires for a benign event; high false-positive rates waste
  analyst time and cause alert fatigue.

## Common misconceptions
- "Lower MTTR always means better security." → MTTR must be balanced against accuracy. A system
  that auto-resolves everything has a very low MTTR but will also close real incidents
  prematurely. Precision matters.
- "AI replaces SOC analysts." → AI handles scale and speed; analysts handle judgment, ethics,
  and novel threats. The SOC becomes a human-AI team, not a human-free system.
- "All incidents should be auto-resolved to minimize MTTR." → Auto-resolution is only safe for
  incidents that are both high-confidence true positives and have reversible response actions.
  Incorrectly auto-resolving a critical incident can make it worse.

## Try it
- **Simulation:** Act as a SOC analyst, triage a queue of
  incidents by severity order, and watch MTTR improve as you handle the highest-severity cases
  first. Reach the target MTTR threshold to meet the objective.
- **Coding problem:** Implement `solve(incidents)` that returns MTTR and
  auto-resolved count for a list of incident records.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (incident response, security operations), rebuilt as original prose above.
- Reference: GeeksforGeeks (MTTR definition, SOC workflows, AI in cybersecurity).
- Practice: Cybrary / LetsDefend SOC Level 1 challenges, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
