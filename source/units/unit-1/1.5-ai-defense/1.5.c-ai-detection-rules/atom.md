# 1.5.c, AI suggesting detection rules

> **Unit 1 · 1.5 Leveraging AI in Cyber Defense**
> **AP Learning Objective(s):** 1.5.A
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Explain how AI-assisted tools generate detection rules from log
data, implement a rule-generation algorithm that converts repeated suspicious events into
structured rule strings, and evaluate what makes a generated rule operationally useful versus
noisy.

## Lesson
A security operations center (SOC) can receive millions of log events per day from firewalls,
servers, identity providers, and endpoint agents. No human team can read every line. The first
line of defense is a set of *detection rules*: machine-readable conditions that trigger an alert
when log events match a pattern known to be suspicious. Writing and maintaining those rules has
historically been a manual expert task, a senior analyst watches for a pattern, writes a Snort
signature or a SIEM query, and checks it in. AI tools now accelerate both steps: they ingest log
streams and *propose* new rules automatically when the data reveals something the analyst has not
yet captured.

**Where logs come from and why they matter.** Every networked system emits logs: authentication
events (who logged in, from where, success or failure), network flows (source IP, destination,
port, bytes), DNS queries, web requests, process executions. These logs are the raw evidence from
which attacks are reconstructed. A log entry on its own is usually unremarkable, one failed login
is normal. The pattern across thousands of log entries is where the threat hides.

**What a detection rule is.** A detection rule is a formal statement of a suspicious condition.
In plain English: "alert when the same IP address generates five or more failed login attempts
within one minute." In a SIEM (Security Information and Event Management system), this might
appear as a structured query or a YAML policy. The rule has three parts: a *condition* (what event
pattern to look for), a *threshold* (how many times, in what window), and an *action* (emit an
alert, block, notify). The coding problem in this skill implements the condition-and-threshold layer
in pure Python.

**How AI generates rules from logs.** Manually reviewing logs to spot a pattern is slow. An AI
system can instead apply statistical analysis and anomaly detection across historical logs, then
propose rules wherever it finds a cluster of events that would have reliably signaled a known
attack. The process: ingest a labeled log set (events tagged as "attack" vs. "normal"), count how
often each condition co-occurs with the attack label, generate candidate rules for conditions that
exceed a precision threshold, and surface them to the analyst for review and sign-off. The
analyst is still in the loop, AI generates candidates, humans approve. This is sometimes called
*assisted detection engineering*.

**The brute-force rule as a worked example.** The most basic and widely deployed detection rule
is the brute-force login detector: count failed authentication events per source IP per minute
(or hour), and raise an alert when the count crosses a threshold (commonly five failures per
minute). This rule appears in nearly every intrusion detection system because the pattern is
highly reliable: legitimate users mistype their password rarely, while password-spraying tools
attempt hundreds of guesses per second. The rule string format used here is:

  `ALERT brute_force src=<IP> count=<N> window=60s`

This format is deterministic and machine-parseable: the keyword `ALERT` signals it is an
actionable finding, `brute_force` names the rule type, `src=` pins the offending IP, `count=`
gives the event count that triggered it, and `window=60s` records the detection window. Well-
structured rule strings like this can be ingested directly by a SIEM or ticketing system.

**Threshold tuning and the precision-recall tradeoff.** A threshold of one failure would generate
an alert for every mistyped password, overwhelming the SOC with noise and causing analysts to
ignore real alerts (alert fatigue). A threshold of one hundred would miss slow, low-volume
attacks. The right threshold balances *precision* (most alerts are real threats) against *recall*
(most threats generate alerts). AI tools help find this balance by testing candidate thresholds
against historical labeled data. For this skill the threshold is fixed at five failures: a clean
pedagogical default that matches industry practice.

**What AI does not do.** AI generates rule *candidates*. It cannot:
- verify that a proposed rule complies with your organization's legal or privacy requirements;
- determine whether an IP belongs to a known partner or a critical internal system;
- assess the business risk of blocking a false positive.

Those judgments require a human analyst. The AP framework's "Detect Attacks" skill therefore
includes both the technical ability to understand how rules are generated *and* the critical
thinking to evaluate whether a generated rule is appropriate to deploy.

**From the sim to the real world.** The simulation in this skill presents a scrolling log stream
and asks you to observe when a rule fires. The coding problem implements the rule-generation
engine from scratch. Together they model the full pipeline: raw logs in, structured alert rules
out. In a real SOC, this pipeline might feed a tool like Splunk, Elastic SIEM, or a custom
detection-as-code framework where rules are version-controlled and tested like software.

## Key terms
- **Detection rule**, a formal condition-and-threshold statement that triggers an alert when a
  log pattern matches; the fundamental unit of automated threat detection.
- **SIEM**, Security Information and Event Management; a platform that aggregates logs from
  many sources, applies detection rules, and surfaces alerts to analysts.
- **Brute-force attack**, an attack that tries many credential combinations in rapid succession
  to guess a password or key.
- **Threshold**, the minimum count of events required before a detection rule fires; tuned to
  balance precision and recall.
- **Alert fatigue**, the desensitization of analysts when too many low-quality alerts are
  generated, causing real threats to be missed.
- **Detection engineering**, the discipline of writing, testing, and maintaining detection rules
  for a security operations environment.

## Common misconceptions
- "More rules = better security." → More rules means more alerts. If rules are not precise,
  analysts are buried in noise and real threats get lost. Quality and tuning matter more than
  quantity.
- "An AI-generated rule is ready to deploy as-is." → AI proposes candidates; a human analyst
  must review each rule for precision, compliance, and context before it goes live.
- "One failed login is suspicious." → A single failure is normal. The pattern of repeated
  failures from the same source in a short window is the signal. Context and threshold are
  everything.

## Try it
- **Simulation:** Observe a live log stream and correctly
  identify which IP addresses the rule engine should flag before the AI announces its findings.
- **Coding problem:** Implement `solve(logs)` that returns sorted detection-rule
  strings for every source IP that exceeds the brute-force threshold.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: MIT OCW (intrusion detection systems, anomaly detection), rebuilt as original prose above.
- Reference: GeeksforGeeks (SIEM overview, detection rules, brute-force detection).
- Practice: Cybrary / LetsDefend SOC analyst challenges, rebuilt locally as the simulation.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity-resources`.
