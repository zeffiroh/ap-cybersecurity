# 4.4.a, Endpoint detection and response (EDR)

> **Unit 4 · 4.4 Detecting Attacks on Devices**
> **AP Learning Objective(s):** 4.4.A
> **Course skill(s):** Detect Attacks

## Learning objective (student-facing)
Describe how an EDR platform collects telemetry from a device,
explain how it classifies process and file activity as suspicious or clean, and identify the core
actions an EDR takes when it detects a threat.

## Lesson
Every device on a network, laptop, server, or workstation, is a potential entry point for an
attacker. A firewall guards the boundary, but once malicious code is running inside a machine, a
boundary control cannot see it. **Endpoint Detection and Response (EDR)** is the category of
security software that watches activity *on the device itself* rather than at the network edge.
Understanding EDR is central to AP Learning Objective 4.4.A: identifying how attacks on devices
are detected.

### What an endpoint is
In security terminology, an "endpoint" is any device that can be an origin or destination for
network traffic, desktops, laptops, servers, smartphones, and increasingly IoT devices. EDR
software runs as a lightweight agent (background process) on each managed endpoint. That agent
is the eyes of the security team on that machine.

### What EDR collects (telemetry)
The agent continuously records raw events from the operating system. The major telemetry streams
are:

- **Process events:** every program that starts, stops, or spawns a child process. Attacker
  tools almost always manifest as processes, a script interpreter launching a reconnaissance
  command, or ransomware forking child processes to encrypt files.
- **File system events:** files created, modified, renamed, or deleted. Malware writing a new
  executable to disk or a ransomware variant renaming thousands of documents shows up here.
- **Registry events** (Windows): changes to the Windows Registry, which attackers use to achieve
  persistence so their malware restarts after a reboot.
- **Network connections:** which processes open network sockets, to which IP addresses and ports,
  and how much data they transfer. A process that normally never touches the network suddenly
  contacting an external server is a strong signal.
- **User account events:** logins, privilege escalation (e.g., running as administrator), account
  creation. An attacker who steals credentials will often trigger unusual logon patterns.

This telemetry stream is dense, a busy workstation generates thousands of events per minute. The
EDR platform must make fast decisions about which events are worth flagging.

### How EDR detects threats
EDR platforms use two complementary strategies:

**Signature matching** compares observed file hashes, process names, or network destinations
against a list of known-bad indicators, the same principle as traditional antivirus, but applied
to behavior events rather than just static files. Signature matching is fast and produces very
few false positives for known threats, but it cannot catch entirely new ("zero-day") attacks.

**Behavioral detection** is more powerful. The platform builds a model of what normal looks like
on that host, which programs run, which directories they access, what network connections are
routine, and flags deviations from that baseline. For example: the PDF-viewer process normally
reads PDF files. If it suddenly writes an executable to the system folder and opens a network
connection, the behavior model raises an alert even if the payload has no known signature. This
technique is how EDR catches novel malware, fileless attacks that live entirely in memory, and
"living off the land" techniques where attackers misuse legitimate system tools like PowerShell
or Windows Management Instrumentation (WMI).

### What EDR does when it detects a threat
Detection is only the first step. EDR platforms are distinguished from older tools by their
**response** capability. When the confidence in a threat is high enough, the agent can:

- **Alert** the security operations center (SOC) with full telemetry context, so analysts see
  the entire attack chain rather than a single event in isolation.
- **Isolate the endpoint** from the network, cutting all connections except to the EDR management
  console, to stop the attacker from moving laterally to other systems while leaving the analyst
  able to investigate remotely.
- **Kill the malicious process** automatically, halting encryption or data exfiltration.
- **Quarantine a file**, move it to a protected area where it cannot execute.
- **Preserve forensic evidence** by capturing a memory snapshot or full disk image.

The combination of collect-detect-respond in one agent is what makes EDR different from simple
antivirus (collect + signature-detect only) and different from a SIEM (which correlates logs but
cannot respond at the endpoint).

### A concrete scenario
Imagine an employee at Meridian High School opens an email attachment that runs a malicious
macro. The macro uses PowerShell (a legitimate Windows tool) to download a second-stage payload.
Traditional antivirus might miss this because PowerShell itself is not malicious. The EDR agent,
however, records that the Office application spawned PowerShell (unusual parent-child
relationship), that PowerShell made an outbound network connection (unusual for this host), and
that a new executable was written to a temp directory. The behavioral model scores this chain as
high-risk, alerts the SOC, and automatically isolates the laptop, all before the payload can
reach any other system. The analyst can then replay the full event timeline from the EDR console
without touching the physical machine.

### EDR in the detection landscape
EDR is one layer in a defense-in-depth strategy. It complements the log analysis skills you will
study in atom 4.4.b and the indicators-of-compromise framework in atom 4.4.c. Larger
organizations often feed EDR alerts into a Security Information and Event Management (SIEM)
platform for correlation across many endpoints simultaneously.

## Key terms
- **Endpoint**, any device (laptop, server, workstation) that is an origin or destination for
  network traffic and hosts a security agent.
- **EDR (Endpoint Detection and Response)**, security software that collects device telemetry,
  detects malicious behavior using signatures and behavioral models, and can respond automatically
  to contain threats.
- **Telemetry**, the stream of raw event data (process, file, network, registry events) that the
  EDR agent reports from the device.
- **Behavioral detection**, flagging activity that deviates from a learned baseline, even when
  no matching signature exists.
- **Isolation**, the EDR response action that cuts a device's network connections to prevent
  lateral movement while preserving remote analyst access.
- **Living off the land**, attacker technique of using legitimate OS tools (PowerShell, WMI,
  certutil) to carry out malicious actions, making detection harder for signature-based tools.

## Common misconceptions
- "EDR is just better antivirus." -> Antivirus primarily checks files against known signatures
  at rest. EDR monitors continuous runtime behavior across process, file, network, and registry
  streams and can respond by isolating, killing, or quarantining, not just scanning.
- "If nothing alerts, the device is clean." -> EDR relies on behavioral baselines and signatures
  that may not cover every possible attack. No detection tool guarantees completeness; layered
  defenses and regular threat-hunting are still required.
- "Isolation means the device is wiped." -> Isolation cuts network access but does not destroy
  data. The analyst can still connect to the isolated device through the EDR console to
  investigate and recover.

## Try it
- **Simulation:** Review a stream of synthetic EDR telemetry
  events and correctly classify each one as benign or suspicious, then choose the right EDR
  response action to reach the target score.
- **Coding problem:** Given a list of EDR process-event records, implement
  `solve()` to detect which processes exhibit suspicious parent-child relationships or unusual
  network behavior, returning a sorted list of flagged process IDs.
- **Quiz:** self-check on the skill's key ideas.

## Sources (local / vendor / rebuilt)
- Deep: Open Security Training (endpoint security fundamentals), rebuilt as original prose above;
  see `vendor/web/open-security-training/` notes.
- Reference: NIST SP 800-137 (Information Security Continuous Monitoring), defines continuous
  monitoring concepts underlying EDR telemetry collection.
- Practice: PortSwigger / LetsDefend SOC analyst labs, rebuilt as the simulation scenario.
- Repo: LetsDefend/Free-Cybersecurity-Resources -> `vendor/repos/letsdefend-free-cybersecurity`.
