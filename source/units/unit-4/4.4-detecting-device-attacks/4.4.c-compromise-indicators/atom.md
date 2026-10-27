# 4.4.c, Identifying compromised devices (indicators of compromise)

> **Unit 4 · 4.4 Detecting Attacks on Devices**
> **AP Learning Objective(s):** 4.4.B, 4.4.C
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Define an indicator of compromise (IOC), classify common IOC
categories, and combine multiple IOCs on a single device into an overall compromise verdict using
weighted scoring.

## Lesson
EDR (4.4.a) watches live behavior on a device, and log analysis (4.4.b) correlates events over
time. Both techniques ultimately produce the same kind of output: individual clues that something
is wrong. An **indicator of compromise (IOC)** is a piece of forensic evidence, an artifact left
behind on a system or network, that suggests a device has been breached. A single IOC rarely
proves compromise on its own; the analyst's job (and the skill behind AP Learning Objective 4.4.C)
is combining multiple IOCs into a confident verdict.

### What counts as an IOC
IOCs come from many different layers of a system, and organizing them by category helps analysts
know where to look:

- **File-based IOCs**, a file matching a known-malicious hash, an unexpected executable in a
  temp or startup directory, or a legitimate file that has been silently modified.
- **Network-based IOCs**, a connection to a known command-and-control (C2) IP address or domain,
  unusually large outbound data transfers, or DNS lookups for algorithmically generated domain
  names (a technique malware uses to find its C2 server without hardcoding one address).
- **Host-based IOCs**, a new administrator account nobody remembers creating, a scheduled task
  that runs at every boot without an owner, a registry "run key" added to achieve persistence, or
  antivirus/EDR protection being silently disabled.
- **Behavioral IOCs**, patterns rather than single artifacts: a spike in failed logins (4.4.b), a
  process spawning an unusual child process (4.4.a), or a login at 3 AM from an account that has
  never logged in outside business hours.

Security teams and vendors publish and share IOCs (hashes, IPs, domains) through **threat
intelligence feeds**, so that a technique discovered against one organization can be checked for
across every other subscribing organization before it causes damage there too.

### Why one IOC is rarely enough
Consider a new administrator account appearing on a server. On its own, this could be a
legitimate action, an IT technician creating an account during scheduled maintenance, or it
could be an attacker establishing **persistence** (a durable way to regain access even if their
initial foothold is discovered and closed). The IOC alone cannot distinguish these two
possibilities. But if that same new admin account appears *alongside* a disabled antivirus
service and a connection to a known-malicious IP address, the combination becomes far more
convincing: three independent artifacts pointing toward the same conclusion is much stronger
evidence than any one of them in isolation. This is the same correlation principle from log
analysis (4.4.b), applied to compromise evidence broadly rather than just login timestamps.

### Weighted scoring
Because different IOCs carry different levels of severity, mature detection systems do not just
count how many IOCs are present, they assign each IOC type a **weight** reflecting how strongly
it, by itself, suggests compromise. A confirmed match against a known-malicious file hash is very
strong evidence and gets a high weight. A handful of failed logins is comparatively weak evidence
on its own and gets a lower weight. Summing the weights of every IOC observed on a device produces
a **compromise score**, which is then compared against thresholds to produce a verdict, for
example: below a low threshold, the device is likely **clean**; in a middle band, it is
**suspicious** and warrants investigation; above a high threshold, the device should be treated as
**compromised** and isolated immediately. This weighted-scoring approach mirrors how CVSS scores
vulnerabilities (4.3.c) and is exactly the logic you will implement in `problem/`.

### A concrete scenario
A workstation at Meridian High School shows: (1) a new local administrator account created
outside of any change-management ticket, (2) the endpoint's antivirus service silently disabled,
and (3) an outbound connection to an IP address matching a known-malicious threat intelligence
feed entry. Any one of these alone might have an innocent explanation. Together, they describe a
coherent attack narrative: an attacker gained access, disabled the security tooling that might
catch them, created a persistent account to survive a reboot or password reset, and is now
communicating with external infrastructure. A weighted-scoring system would sum these three IOCs'
weights, cross a "compromised" threshold, and trigger an immediate isolation response, the same
action you studied in 4.4.a.

### IOCs vs. indicators of attack (IOA)
It is worth briefly distinguishing IOCs from a related concept: an **indicator of attack (IOA)**
focuses on the attacker's *intent and technique* while it is happening (e.g., "a process is
attempting to enumerate all files with a specific extension," which is what ransomware does right
before encrypting them), whereas an IOC is typically evidence left *after* a step has already
occurred (e.g., "a file with a `.locked` extension already exists"). IOAs aim to catch an attack
in progress; IOCs confirm that something already happened. Both matter, and real detection
programs use both.

## Key terms
- **Indicator of compromise (IOC)**, forensic evidence (a file, network connection, account,
  configuration change, or behavior) suggesting a device has been breached.
- **Persistence**, an attacker technique for maintaining access to a compromised system even
  after the initial foothold is discovered or the system is rebooted.
- **Threat intelligence feed**, a shared, continuously updated source of known-malicious
  indicators (hashes, IPs, domains) that organizations subscribe to.
- **Compromise score**, a numeric value produced by summing the weights of every IOC observed
  on a device, used to classify overall risk.
- **Indicator of attack (IOA)**, evidence of an attacker's intent or technique while an attack is
  actively in progress, as opposed to after-the-fact evidence (IOC).

## Common misconceptions
- "Any single suspicious artifact proves a device is compromised." → One IOC alone is usually
  ambiguous and may have an innocent explanation. Confident verdicts come from combining multiple
  independent IOCs, similar to correlating multiple log entries in 4.4.b.
- "All IOCs are equally serious." → A confirmed known-malicious file hash is far stronger evidence
  than a single failed login. Weighted scoring reflects that different IOC types carry very
  different levels of severity.
- "IOCs and IOAs are the same thing." → An IOC is typically after-the-fact evidence that something
  already happened; an IOA focuses on catching the attacker's technique while it is still in
  progress.

## Try it
- **Simulation:** Review the IOCs observed on several devices
  and classify each device's overall compromise verdict to reach the target score.
- **Coding problem:** Implement a weighted IOC-scoring engine that sums the weights
  of observed indicators for a device and returns a `"clean"`, `"suspicious"`, or `"compromised"`
  verdict.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: NIST SP 800-61 (Computer Security Incident Handling Guide), rebuilt as original prose
  above.
- Reference: MITRE ATT&CK framework concepts (persistence, defense evasion tactics), rebuilt
  locally.
- Practice: LetsDefend SOC IOC-triage labs, rebuilt as the simulation challenge.
- Repo: LetsDefend/Free-Cybersecurity-Resources → `vendor/repos/letsdefend-free-cybersecurity`.
